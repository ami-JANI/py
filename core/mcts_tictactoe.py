import math
import random
from ttt_game import player, actions, result, terminal, utility, display

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
    exploration = C * math.sqrt(math.log(node.parent.visits) / node.visits)
    return exploitation + exploration

def selection(node):
    while not terminal(node.state):
        if len(node.untried_actions) > 0:
            return node
        if player(node.state) == 'X':
            node = max(node.children, key=ucb1)
        else:
            node = min(node.children, key=ucb1)
    return node

def expansion(node):
    if terminal(node.state):
        return node
    action = random.choice(node.untried_actions)
    node.untried_actions.remove(action)
    child = MCTSNode(result(node.state, action), node, action)
    node.children.append(child)
    return child

def simulation(node):
    state = node.state
    while not terminal(state):
        state = result(state, random.choice(actions(state)))
    return utility(state)

def backpropagation(node, value):
    while node is not None:
        node.visits += 1
        node.total_value += value
        node = node.parent

def mcts(state, iterations=1000):
    root = MCTSNode(state)
    for _ in range(iterations):
        node = selection(root)
        node = expansion(node)
        value = simulation(node)
        backpropagation(node, value)
    return max(root.children, key=lambda c: c.visits).action

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
            action = mcts(state, 1000)
            print("AI plays:", action)
            state = result(state, action)
        display(state)
    score = utility(state)
    print("X wins!" if score == 1 else "O wins!" if score == -1 else "Draw!")

if __name__ == "__main__":
    play()
