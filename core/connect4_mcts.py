import copy
from mcts_core import make_mcts

ROWS, COLS = 4, 5

def player(state):
    return state[1]

def actions(state):
    board = state[0]
    moves = []
    for c in range(COLS):
        if board[0][c] == ' ':
            moves.append(c)
    return moves

def result(state, col):
    board = copy.deepcopy(state[0])
    piece = 'X' if state[1] == 'MAX' else 'O'
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ' ':
            board[r][col] = piece
            break
    return (board, 'MIN' if state[1] == 'MAX' else 'MAX')

def winner(board):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == ' ':
                continue
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
                count = 1
                for k in range(1, 4):
                    x, y = r + dr * k, c + dc * k
                    if 0 <= x < ROWS and 0 <= y < COLS and board[x][y] == board[r][c]:
                        count += 1
                if count == 4:
                    return board[r][c]
    return None

def terminal(state):
    return winner(state[0]) is not None or len(actions(state)) == 0

def utility(state):
    w = winner(state[0])
    if w == 'X':
        return 1
    if w == 'O':
        return -1
    return 0

def display(board):
    for row in board:
        print(" | ".join(row))
    print("-" * (COLS * 4 - 3))

mcts = make_mcts(player, actions, result, terminal, utility)

if __name__ == "__main__":
    state = ([[' '] * COLS for _ in range(ROWS)], 'MAX')
    while not terminal(state):
        if player(state) == 'MAX':
            col = mcts(state, 2000)
            print("AI plays column", col)
        else:
            col = int(input("Enter column: "))
            if col not in actions(state):
                print("Invalid move!")
                continue
        state = result(state, col)
        display(state[0])
    w = winner(state[0])
    print("X wins!" if w == 'X' else "O wins!" if w == 'O' else "Draw!")
