import math

def player(state):
    return state[1]

def actions(state):
    piles = state[0]
    moves = []
    for i in range(len(piles)):
        for take in range(1, piles[i] + 1):
            moves.append((i, take))
    return moves

def result(state, action):
    piles, turn = state
    i, take = action
    new_piles = list(piles)
    new_piles[i] -= take
    return (tuple(new_piles), 'MIN' if turn == 'MAX' else 'MAX')

def terminal(state):
    return sum(state[0]) == 0

def utility(state):
    return 1 if state[1] == 'MIN' else -1

def max_value(state):
    if terminal(state):
        return utility(state)
    value = -math.inf
    for action in actions(state):
        value = max(value, min_value(result(state, action)))
    return value

def min_value(state):
    if terminal(state):
        return utility(state)
    value = math.inf
    for action in actions(state):
        value = min(value, max_value(result(state, action)))
    return value

def minimax(state):
    best_action = None
    if player(state) == 'MAX':
        best_value = -math.inf
        for action in actions(state):
            value = min_value(result(state, action))
            if value > best_value:
                best_value, best_action = value, action
    else:
        best_value = math.inf
        for action in actions(state):
            value = max_value(result(state, action))
            if value < best_value:
                best_value, best_action = value, action
    return best_action

if __name__ == "__main__":
    state = ((1, 3, 5), 'MAX')
    while not terminal(state):
        action = minimax(state)
        print(player(state), "takes", action[1], "from pile", action[0])
        state = result(state, action)
    print("MAX wins" if utility(state) == 1 else "MIN wins")
