import time

from dlgo import goboard, agent
from dlgo import gotypes
from dlgo.agent import RandomBot
from dlgo.utils import print_board, print_move, print_board_plus, point_from_coords


def main():
    board_size = 9
    game = goboard.GameState.new_game(board_size)
    bot = RandomBot()

    while not game.is_over():
        print(chr(27) + "[2J")
        print_board_plus(game.board)
        # print_board(game.board)
        if game.next_player == gotypes.Player.black:
            human_move = input("-- ")
            point = point_from_coords(human_move.strip())
            move = goboard.Move.play(point)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        game = game.apply_move(move)


if __name__ == "__main__":
    main()
