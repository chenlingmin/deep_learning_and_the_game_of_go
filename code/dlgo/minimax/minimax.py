__all__ = [
    'GameResult',
    'MinimaxAgent'
]

import enum
import random

from dlgo.agent import Agent


class GameResult(enum.Enum):
    loss = 1
    draw = 2
    win = 3


def reverse_game_result(game_result):
    if game_result == GameResult.loss:
        return game_result.win
    if game_result == GameResult.win:
        return game_result.loss
    return GameResult.draw


def best_result(game_state):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return GameResult.win
        elif game_state.winner() is None:
            return GameResult.draw
        else:
            return GameResult.loss
    best_result_so_far = GameResult.loss
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)  # 看看如果走这一步，棋局会变成什么样
        opponent_best_result = best_result(next_state)  # 找到对方最佳的动作
        our_result = reverse_game_result(opponent_best_result)  # 无论对方想要什么，我们想要的就是他的反面
        if our_result.value > best_result_so_far.value:
            best_result_so_far = our_result
    return best_result_so_far


class MinimaxAgent(Agent):
    def select_move(self, game_state):
        winning_moves = []
        draw_moves = []
        losing_moves = []
        for possible_move in game_state.legal_moves():  # 循环遍历所有合法动作
            next_state = game_state.apply_move(possible_move)  # 计算如果选择这个动作，会导致什么样的游戏状态
            opponent_best_outcome = best_result(next_state)  # 由于下一回合对方执子，因此需要找到对方可能获得的最佳结果，这个结果的反面就是己方的结果
            our_best_outcome = reverse_game_result(opponent_best_outcome)
            if our_best_outcome == GameResult.win:  # 根据这个动作导致的最终结果来给他分类
                winning_moves.append(possible_move)
            elif our_best_outcome == GameResult.draw:
                draw_moves.append(possible_move)
            else:
                losing_moves.append(possible_move)
        if winning_moves:
            return random.choice(winning_moves)
        if draw_moves:
            return random.choice(draw_moves)
        return random.choice(losing_moves)
