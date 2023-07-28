import subprocess
import re
import h5py

from dlgo.goboard_fast import GameState, Move
from dlgo.agent.predict import load_prediction_agent
from dlgo.gotypes import Player
from dlgo.gtp.board import gtp_position_to_coords, coords_to_gtp_position
from dlgo.gtp.termination import TerminationAgent, PassWhenOpponentPasses
from dlgo.gtp.utils import SGFWriter
from dlgo.scoring import compute_game_result
from dlgo.utils import print_board_plus


class LocalGtpBot:
    def __init__(self, go_bot, termination=None, handicap=0,
                 opponent='gnugo', output_sgf="out.sgf",
                 our_color='b'):
        self.bot = TerminationAgent(go_bot, termination)
        self.handicap = handicap
        self._stopped = False
        self.game_state = GameState.new_game(19)
        self.sgf = SGFWriter(output_sgf)

        self.our_color = Player.black if our_color == 'b' else Player.white
        self.their_color = self.our_color.other

        cmd = self.opponent_cmd(opponent)
        pipe = subprocess.PIPE
        self.gtp_stream = subprocess.Popen(
            cmd, stdin=pipe, stdout=pipe, bufsize=0
        )

    @staticmethod
    def opponent_cmd(opponent):
        if opponent == 'gnugo':
            return ["gnugo", "--mode", "gtp"]
        elif opponent == 'pachi':
            return ["pachi"]
        else:
            raise ValueError("Unknown bot name {}".format(opponent))

    def send_command(self, cmd):
        self.gtp_stream.stdin.write(cmd.encode('utf-8'))

    def get_response(self):
        succeeded = False
        result = ''
        while not succeeded:
            line = self.gtp_stream.stdout.readline().decode('utf-8')
            if line[0] == '=':
                succeeded = True
                line = line.strip()
                result = re.sub('^= ?', '', line)
        return result

    def command_and_response(self, cmd):
        self.send_command(cmd)
        return self.get_response()

    def run(self):
        self.command_and_response("boardsize 19\n")
        self.set_handicap()
        self.play()
        self.sgf.write_sgf()

    def set_handicap(self):
        if self.handicap == 0:
            self.command_and_response("komi 7.5\n")
            self.sgf.append("KM[7.5]\n")
        else:
            stones = self.command_and_response("fixed_handicap {}\n".format(self.handicap))
            sgf_handicap = "HA[{}]AB".format(self.handicap)
            for pos in stones.split(" "):
                move = gtp_position_to_coords(pos)
                self.game_state = self.game_state.apply_move(move)
                sgf_handicap = sgf_handicap + "[" + self.sgf.coordinates(move) + "]"
            self.sgf.append(sgf_handicap + "\n")

    def play(self):
        while not self._stopped:
            if self.game_state.next_player == self.our_color:
                self.play_our_move()
            else:
                self.play_their_move()
            print(chr(27) + "[2J")
            print_board_plus(self.game_state.board)
            print("Estimated result: ")
            print(compute_game_result(self.game_state))

    def play_our_move(self):
        move = self.bot.select_move(self.game_state)
        self.game_state = self.game_state.apply_move(move)

        our_name = self.our_color.name
        our_letter = our_name[0].upper()
        sgf_move = ""
        if move.is_pass:
            self.command_and_response("play {} pass\n".format(our_name))
        elif move.is_resign:
            self.command_and_response("play {} resign\n".format(our_name))
        else:
            pos = coords_to_gtp_position(move)
            self.command_and_response("play {} {}\n".format(our_name, pos))
            sgf_move = self.sgf.coordinates(move)
        self.sgf.append(";{}[{}]\n".format(our_letter, sgf_move))

    def play_their_move(self):
        their_name = self.their_color.name
        their_letter = their_name[0].upper()

        pos = self.command_and_response("genmove {}\n".format(their_name))
        if pos.lower() == 'resign':
            self.game_state = self.game_state.apply_move(Move.resign())
            self._stopped = True
        elif pos.lower() == 'pass':
            self.game_state = self.game_state.apply_move(Move.pass_turn())
            self.sgf.append(";{}[]\n".format(their_letter))
            if self.game_state.last_move.is_pass:
                self._stopped = True
        else:
            move = gtp_position_to_coords(pos)
            self.game_state = self.game_state.apply_move(move)
            self.sgf.append(";{}[{}]\n".format(their_letter, self.sgf.coordinates(move)))


if __name__ == "__main__":
    bot = load_prediction_agent(h5py.File("../../deep_bot.h5", "r"))
    gnu_go = LocalGtpBot(go_bot=bot, termination=PassWhenOpponentPasses(),
                         handicap=0, opponent='gnugo', )
    gnu_go.run()
