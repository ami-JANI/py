import math
from ttt_game import player, actions, result, terminal, utility

def max_value(state, alpha, beta):
    if terminal(state):
        return utility(state)
    value = -math.inf
    for action in actions(state):
        value = max(value, min_value(result(state, action), alpha, beta))
        if value >= beta:
            return value
        alpha = max(alpha, value)
    return value

def min_value(state, alpha, beta):
    if terminal(state):
        return utility(state)
    value = math.inf
    for action in actions(state):
        value = min(value, max_value(result(state, action), alpha, beta))
        if value <= alpha:
            return value
        beta = min(beta, value)
    return value

def alphabeta(state):
    best_action = None
    alpha, beta = -math.inf, math.inf
    if player(state) == 'X':
        best_value = -math.inf
        for action in actions(state):
            value = min_value(result(state, action), alpha, beta)
            if value > best_value:
                best_value, best_action = value, action
            alpha = max(alpha, best_value)
    else:
        best_value = math.inf
        for action in actions(state):
            value = max_value(result(state, action), alpha, beta)
            if value < best_value:
                best_value, best_action = value, action
            beta = min(beta, best_value)
    return best_action

if __name__ == "__main__":
    state = [[' '] * 3 for _ in range(3)]
    while not terminal(state):
        state = result(state, alphabeta(state))
    print(state, "score:", utility(state))
