import argparse
import datetime
from collections import namedtuple

import h5py

from dlgo import agent
from dlgo import scoring
from dlgo.goboard_fast import GameState, Player, Point
from dlgo.utils import print_board_plus

BOARD_SIZE = 19
COLS = 'ABCDEFGHJKLMNOPQRST'
STONE_TO_CHAR = {
    None: '.',
    Player.black: 'x',
    Player.white: 'o',
}


def avg(items):
    if not items:
        return 0.0
    return sum(items) / float(len(items))



class GameRecord(namedtuple('GameRecord', 'moves winner margin')):
    pass


def name(player):
    if player == Player.black:
        return 'B'
    return 'W'


def simulate_game(black_player, white_player):
    moves = []
    game = GameState.new_game(BOARD_SIZE)
    agents = {
        Player.black: black_player,
        Player.white: white_player,
    }
    while not game.is_over():
        next_move = agents[game.next_player].select_move(game)
        moves.append(next_move)
        #if next_move.is_pass:
        #    print('%s passes' % name(game.next_player))
        game = game.apply_move(next_move)

    print_board_plus(game.board)
    game_result = scoring.compute_game_result(game)
    print(game_result)

    return GameRecord(
        moves=moves,
        winner=game_result.winner,
        margin=game_result.winning_margin,
    )


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--agent1', required=True)
    # parser.add_argument('--agent2', required=True)
    # parser.add_argument('--num-games', '-n', type=int, default=10)
    #
    # args = parser.parse_args()

    agent1 = agent.load_policy_agent(h5py.File('deep_bot.h5'))
    agent2 = agent.load_policy_agent(h5py.File('deep_bot_pg.h5'))

    # agent1 = agent.load_policy_agent(h5py.File(args.agent1))
    # agent2 = agent.load_policy_agent(h5py.File(args.agent2))
    num_games = 100

    wins = 0
    losses = 0
    color1 = Player.black
    for i in range(num_games):
        print('Simulating game %d/%d...' % (i + 1, num_games))
        if color1 == Player.black:
            black_player, white_player = agent1, agent2
        else:
            white_player, black_player = agent1, agent2
        game_record = simulate_game(black_player, white_player)
        if game_record.winner == color1:
            wins += 1
        else:
            losses += 1
        color1 = color1.other
    print('Agent 1 record: %d/%d' % (wins, wins + losses))


if __name__ == '__main__':
    main()