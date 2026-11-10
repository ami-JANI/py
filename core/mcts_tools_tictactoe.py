import time
from ttt_game import player, result, terminal, utility
from mcts_tictactoe import MCTSNode, selection, expansion, simulation, backpropagation, mcts
from minimax_tictactoe import minimax

def mcts_stats(state, iterations=1000):
    root = MCTSNode(state)
    for _ in range(iterations):
        node = expansion(selection(root))
        backpropagation(node, simulation(node))
    for child in root.children:
        print(child.action, "visits:", child.visits, "avg:", round(child.total_value / child.visits, 2))
    return max(root.children, key=lambda c: c.visits).action

def mcts_time(state, seconds=1.0):
    root = MCTSNode(state)
    start = time.time()
    while time.time() - start < seconds:
        node = expansion(selection(root))
        backpropagation(node, simulation(node))
    return max(root.children, key=lambda c: c.visits).action

def mcts_best_average(state, iterations=1000):
    root = MCTSNode(state)
    for _ in range(iterations):
        node = expansion(selection(root))
        backpropagation(node, simulation(node))
    if player(state) == 'X':
        return max(root.children, key=lambda c: c.total_value / c.visits).action
    return min(root.children, key=lambda c: c.total_value / c.visits).action

def ai_vs_ai(games=5, iterations=500):
    score = {1: 0, -1: 0, 0: 0}
    for _ in range(games):
        state = [[' '] * 3 for _ in range(3)]
        while not terminal(state):
            if player(state) == 'X':
                action = mcts(state, iterations)
            else:
                action = minimax(state)
            state = result(state, action)
        score[utility(state)] += 1
    print("MCTS wins:", score[1], "Minimax wins:", score[-1], "Draws:", score[0])

if __name__ == "__main__":
    s = [['X', 'X', ' '], ['O', 'O', ' '], [' ', ' ', ' ']]
    print(mcts_stats(s, 500))
    print(mcts_time([[' '] * 3 for _ in range(3)], 0.5))
    print(mcts_best_average(s, 500))
    ai_vs_ai(3, 500)
