# def reverse_game_result(game_result):
#     if game_result == GameResult.loss:
import random

from dlgo.agent import Agent

__all__ = [
    'DepthPrunedAgent'
]

MAX_SCORE = 999999
MIN_SCORE = -999999


def best_result(game_state, max_depth, eval_fn):
    if game_state.is_over():  # 如果游戏已经结束，就可以立即得知哪一方获胜
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        else:
            return MIN_SCORE

    if max_depth == 0:  # 已达到最大搜索深度，使用启发式规则来确定当前动作序列的好坏
        return eval_fn(game_state)

    best_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves():  # 遍历所有可能动作
        next_state = game_state.apply_move(candidate_move)  # 如果采取这个动作，看看棋局会变成什么样
        opponent_best_result = best_result(  # 从当前棋局开始，找到对方的最佳结果
            next_state, max_depth - 1, eval_fn
        )
        our_result = -1 * opponent_best_result
        if our_result > best_so_far:
            best_so_far = our_result
    return best_so_far


class DepthPrunedAgent(Agent):
    def __init__(self, max_depth, eval_fn):
        Agent.__init__(self)
        self.max_depth = max_depth
        self.eval_fn = eval_fn

    def select_move(self, game_state):
        best_moves = []
        best_score = None

        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)

            opponent_best_outcome = best_result(next_state, self.max_depth, self.eval_fn)
            our_best_outcome = -1 * opponent_best_outcome
            if (not best_moves) or our_best_outcome > best_score:
                best_moves = [possible_move]
                best_score = our_best_outcome
            elif our_best_outcome == best_score:
                best_moves.append(possible_move)
        return random.choice(best_moves)
