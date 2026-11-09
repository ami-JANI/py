import math
import copy
import tkinter as tk


def player(state):
    x_count = 0
    o_count = 0
    for row in state:
        for cell in row:
            if cell == 'X':
                x_count += 1
            elif cell == 'O':
                o_count += 1
    if x_count == o_count:
        return 'X'
    else:
        return 'O'


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


def terminal(state):
    lines = []
    for row in state:
        lines.append(row)
    for j in range(3):
        column = []
        for i in range(3):
            column.append(state[i][j])
        lines.append(column)
    lines.append([state[0][0], state[1][1], state[2][2]])
    lines.append([state[0][2], state[1][1], state[2][0]])
    for line in lines:
        if line == ['X', 'X', 'X'] or line == ['O', 'O', 'O']:
            return True
    for row in state:
        for cell in row:
            if cell == ' ':
                return False
    return True


def utility(state):
    lines = []
    for row in state:
        lines.append(row)
    for j in range(3):
        column = []
        for i in range(3):
            column.append(state[i][j])
        lines.append(column)
    lines.append([state[0][0], state[1][1], state[2][2]])
    lines.append([state[0][2], state[1][1], state[2][0]])
    for line in lines:
        if line == ['X', 'X', 'X']:
            return 1
        if line == ['O', 'O', 'O']:
            return -1
    return 0


def max_value(state):
    if terminal(state):
        return utility(state)
    value = -math.inf
    for action in actions(state):
        new_state = result(state, action)
        eval_value = min_value(new_state)
        if eval_value > value:
            value = eval_value
    return value


def min_value(state):
    if terminal(state):
        return utility(state)
    value = math.inf
    for action in actions(state):
        new_state = result(state, action)
        eval_value = max_value(new_state)
        if eval_value < value:
            value = eval_value
    return value


def minimax(state):
    best_action = None
    if player(state) == 'X':
        best_value = -math.inf
        for action in actions(state):
            new_state = result(state, action)
            value = min_value(new_state)
            if value > best_value:
                best_value = value
                best_action = action
    else:
        best_value = math.inf
        for action in actions(state):
            new_state = result(state, action)
            value = max_value(new_state)
            if value < best_value:
                best_value = value
                best_action = action
    return best_action


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        root.title("Tic-Tac-Toe: Minimax")
        root.resizable(False, False)

        self.status = tk.Label(root, font=("Arial", 14), pady=8)
        self.status.grid(row=0, column=0, columnspan=3)

        self.buttons = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                b = tk.Button(root, text=" ", font=("Arial", 32, "bold"),
                              width=4, height=2,
                              command=lambda r=i, c=j: self.click(r, c))
                b.grid(row=i + 1, column=j)
                self.buttons[i][j] = b

        tk.Button(root, text="Restart", font=("Arial", 12),
                  command=self.reset).grid(row=4, column=0, columnspan=3, pady=8)

        self.reset()

    def reset(self):
        self.state = [[' '] * 3 for _ in range(3)]
        self.refresh()
        self.status.config(text="You are O, AI is X. AI is thinking...")
        self.root.after(300, self.ai_move)  # X (AI) moves first

    def refresh(self):
        over = terminal(self.state)
        for i in range(3):
            for j in range(3):
                c = self.state[i][j]
                self.buttons[i][j].config(
                    text=c,
                    disabledforeground="red" if c == 'X' else "blue",
                    state="disabled" if (c != ' ' or over) else "normal")

    def finish_if_over(self):
        if not terminal(self.state):
            return False
        score = utility(self.state)
        msg = "X (AI) wins!" if score == 1 else "O (You) win!" if score == -1 else "It's a draw!"
        self.status.config(text=f"{msg}")
        return True

    def click(self, row, col):
        if terminal(self.state) or player(self.state) != 'O':
            return
        if (row, col) not in actions(self.state):
            return
        self.state = result(self.state, (row, col))
        self.refresh()
        if not self.finish_if_over():
            self.status.config(text="AI is thinking...")
            self.root.after(300, self.ai_move)

    def ai_move(self):
        if terminal(self.state): #or player(self.state) != 'X':
            return
        action = minimax(self.state)
        self.state = result(self.state, action)
        self.refresh()
        if not self.finish_if_over():
            # self.status.config(text=f"AI played {action}. Your turn (O).")
            self.status.config(text=f"AI played {action}.")
            self.root.after(1000, self.ai_move)


if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()