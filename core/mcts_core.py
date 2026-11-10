import math
import random

def make_mcts(player, actions, result, terminal, utility):

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
        exploitation = node.total_value / node.visits
        exploration = C * math.sqrt(math.log(node.parent.visits) / node.visits)
        return exploitation + exploration

    def lcb1(node, C=1.41):
        exploitation = node.total_value / node.visits
        exploration = C * math.sqrt(math.log(node.parent.visits) / node.visits)
        return exploitation - exploration

    def selection(node):
        while not terminal(node.state):
            if len(node.untried_actions) > 0:
                return node
            if player(node.state) == 'MAX':
                node = max(node.children, key=ucb1)
            else:
                node = min(node.children, key=lcb1)
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
            node = expansion(selection(root))
            backpropagation(node, simulation(node))
        return max(root.children, key=lambda c: c.visits).action

    return mcts
