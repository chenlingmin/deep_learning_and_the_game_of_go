from dlgo.goboard_fast import GameState, Move
from dlgo.gotypes import Point, Player
from dlgo.mcts import MCTSAgent
from dlgo.utils import print_board_plus, point_from_coords, print_move

BOARD_SIZE = 9


def main():
    game = GameState.new_game(BOARD_SIZE)
    bot = MCTSAgent(500, temperature=1.2)

    while not game.is_over():
        print_board_plus(game.board)
        if game.next_player == Player.black:
            human_move = input('-- ')
            point = point_from_coords(human_move.strip())
            move = Move.play(point)
        else:
            move = bot.select_move(game)
        print_move(game.next_player, move)
        game = game.apply_move(move)


if __name__ == '__main__':
    main()
