from dlgo.goboard import GameState, Move
from dlgo.gotypes import Point, Player
from dlgo.minimax import AlphaBetaAgent
from dlgo.utils import print_board_plus, point_from_coords, print_move

BOARD_SIZE = 5


def capture_diff(game_state):
    black_stones = 0
    white_stones = 0
    for r in range(1, game_state.board.num_rows + 1):
        for c in range(1, game_state.board.num_cols + 1):
            p = Point(r, c)
            color = game_state.board.get(p)
            if color == Player.black:
                black_stones += 1
            elif color == Player.white:
                white_stones += 1
    diff = black_stones - white_stones  # 计算棋盘上黑子和白子的数量差，这和计算双方提子数量差事一致的，除非某一方提前跳过回合
    if game_state.next_player == Player.black:  # 如果是黑方落子的回合，那么返回"黑子数量-白子数量"
        return diff
    return -1 * diff  # 如果是白方落子的回合，那么返回"白子数量-黑子数量"


def main():
    game = GameState.new_game(BOARD_SIZE)
    bot = AlphaBetaAgent(3, capture_diff)

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
