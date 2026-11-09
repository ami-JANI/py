import math
import copy
import random

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

def display(state):
    for row in state:
        print(" | ".join(row))
    print("-" * 9)

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

class MCTSNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.total_value = 0
        self.untried_actions = actions(state)

def ucb1(node, C=1.41):
    if node.visits == 0:
        return math.inf
    exploitation = node.total_value / node.visits
    exploration = (C * math.sqrt(math.log(node.parent.visits) / node.visits))
    return exploitation + exploration

def selection(node):
    while not terminal(node.state):
        if len(node.untried_actions) > 0:
            return node
        if(player(node.state) == 'X'):
          best_child = max(node.children,key=ucb1)
        else:
          best_child = min(node.children,key=ucb1)
        node = best_child
    return node

def expansion(node):
    if terminal(node.state):
        return node
    action = random.choice(node.untried_actions)
    node.untried_actions.remove(action)
    new_state = result(node.state, action)
    child = MCTSNode(state=new_state, parent=node, action=action)
    node.children.append(child)
    return child

def simulation(node):
    current_state = copy.deepcopy(node.state)
    while not terminal(current_state):
        possible_actions = actions(current_state)
        random_action = random.choice(possible_actions)
        current_state = result(current_state, random_action)
    return utility(current_state)

def backpropagation(node, result_value):
    while node is not None:
        node.visits += 1
        node.total_value += result_value
        node = node.parent

def mcts(state, iterations=1000):
    root = MCTSNode(state)
    for i in range(iterations):
        node = selection(root)
        node = expansion(node)
        result_value = simulation(node)
        backpropagation(node, result_value)

    best_child = max(root.children, key=lambda child: child.visits)
    return best_child.action

def play():
    state = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]
    print("Welcome to Tic-Tac-Toe! You are O, AI is X.")
    display(state)
    while not terminal(state):
        if player(state) == 'O':
            position = input("Enter row and col: ").split()
            row = int(position[0])
            col = int(position[1])
            action = (row, col)
            if action not in actions(state):
                print("Invalid move! Try again.")
                continue
            state = result(state, action)
        else:
            action = mcts(state, iterations=100)
            print(f"AI plays: {action}")
            state = result(state, action)
        display(state)

    score = utility(state)
    if score == 1:
        print("X wins!")
    elif score == -1:
        print("O wins!")
    else:
        print("It's a draw!")

play()