from mcts_core import make_mcts

def player(state):
    return state[1]

def actions(state):
    moves = []
    for t in [1, 2, 3]:
        if t <= state[0]:
            moves.append(t)
    return moves

def result(state, action):
    return (state[0] - action, 'MIN' if state[1] == 'MAX' else 'MAX')

def terminal(state):
    return state[0] == 0

def utility(state):
    return -1 if state[1] == 'MIN' else 1

mcts = make_mcts(player, actions, result, terminal, utility)

if __name__ == "__main__":
    state = (10, 'MAX')
    while not terminal(state):
        action = mcts(state, 3000)
        print(player(state), "takes", action, "->", state[0] - action, "left")
        state = result(state, action)
    print("MAX wins" if utility(state) == 1 else "MIN wins")
