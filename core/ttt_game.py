import copy

def player(state):
    x = sum(row.count('X') for row in state)
    o = sum(row.count('O') for row in state)
    return 'X' if x == o else 'O'

def actions(state):
    moves = []
    for i in range(3):
        for j in range(3):
            if state[i][j] == ' ':
                moves.append((i, j))
    return moves

def result(state, action):
    i, j = action
    new_state = copy.deepcopy(state)
    new_state[i][j] = player(state)
    return new_state

def get_lines(state):
    lines = [row for row in state]
    for j in range(3):
        lines.append([state[i][j] for i in range(3)])
    lines.append([state[0][0], state[1][1], state[2][2]])
    lines.append([state[0][2], state[1][1], state[2][0]])
    return lines

def utility(state):
    for line in get_lines(state):
        if line == ['X', 'X', 'X']:
            return 1
        if line == ['O', 'O', 'O']:
            return -1
    return 0

def terminal(state):
    return utility(state) != 0 or len(actions(state)) == 0

def display(state):
    for row in state:
        print(" | ".join(row))
    print("-" * 9)
