import math
from ttt_game import player, actions, result, terminal, utility, display

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
    if player(state) == 'X':
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

def play():
    state = [[' '] * 3 for _ in range(3)]
    display(state)
    while not terminal(state):
        if player(state) == 'O':
            row, col = map(int, input("Enter row and col: ").split())
            if (row, col) not in actions(state):
                print("Invalid move!")
                continue
            state = result(state, (row, col))
        else:
            action = minimax(state)
            print("AI plays:", action)
            state = result(state, action)
        display(state)
    score = utility(state)
    print("X wins!" if score == 1 else "O wins!" if score == -1 else "Draw!")

if __name__ == "__main__":
    play()
