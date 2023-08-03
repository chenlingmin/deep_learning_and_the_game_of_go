import argparse
from collections import namedtuple

import h5py

from dlgo import agent, rl
from dlgo.goboard_fast import GameState
from dlgo.gotypes import Player
from dlgo.scoring import compute_game_result
from dlgo.utils import print_board_plus

BOARD_SIZE = 19


class GameRecord(namedtuple('GameRecord', 'moves winner margin')):
    pass


def simulate_game(black_player, white_player):
    moves = []
    game = GameState.new_game(BOARD_SIZE)
    agents = {
        Player.black: black_player,
        Player.white: white_player
    }

    while not game.is_over():
        next_move = agents[game.next_player].select_move(game)
        moves.append(next_move)
        game = game.apply_move(next_move)

    print_board_plus(game.board)
    game_result = compute_game_result(game)
    print(game_result)

    return GameRecord(
        moves=moves,
        winner=game_result.winner,
        margin=game_result.winning_margin,
    )


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--board-size', type=int, required=True)
    # parser.add_argument('--learning-agent', required=True)
    # parser.add_argument('--num-games', '-n', type=int, default=10)
    # parser.add_argument('--experience-out', required=True)
    #
    # args = parser.parse_args()
    # agent_filename = args.learning_agent
    # experience_filename = args.experience_out
    # num_games = args.num_games
    # global BOARD_SIZE
    # BOARD_SIZE = args.board_size
    agent_filename="deep_bot.h5"
    experience_filename="experience.h5"
    num_games = 10

    agent1 = agent.load_policy_agent(h5py.File(agent_filename))
    agent2 = agent.load_policy_agent(h5py.File(agent_filename))
    collector1 = rl.ExperienceCollector()
    collector2 = rl.ExperienceCollector()
    agent1.set_collector(collector1)
    agent2.set_collector(collector2)

    for i in range(num_games):
        print('Simulating game %d/%d...' % (i + 1, num_games))
        collector1.begin_episode()
        collector2.begin_episode()

        game_record = simulate_game(agent1, agent2)
        if game_record.winner == Player.black:
            collector1.complete_episode(reward=1)
            collector2.complete_episode(reward=-1)
        else:
            collector2.complete_episode(reward=1)
            collector1.complete_episode(reward=-1)

    experience = rl.combine_experience([collector1, collector2])
    with h5py.File(experience_filename, 'w') as experience_outf:
        experience.serialize(experience_outf)


if __name__ == '__main__':
    main()