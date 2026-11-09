import heapq
import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph, start, goal, path=None):
    G = nx.DiGraph()

    for node in graph:
        for neighbor, cost in graph[node]:
            G.add_edge(node, neighbor, weight=cost)

    pos = nx.spring_layout(G, seed=34)
    labels = {}
    for node in G.nodes:
        labels[node] = node + "\nh=" + str(heuristic(node, goal))

    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw(G, pos, labels = labels, with_labels=True, node_size=2000, node_color="white", edgecolors="black", font_size=14)

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

    if path:
        path_edges = []
        for i in range(len(path) - 1):
            path_edges.append((path[i], path[i + 1]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color="lightgreen", alpha=0.8)

    plt.show()


def heuristic(node, goal):
    h = {
        "S": 4,
        "A": 1,
        "B": 2,
        "G": 0
    }
    return h[node]


def greedy_f(node, goal, path_cost):
    return heuristic(node, goal)

def astar_f(node, goal, path_cost):
    return path_cost + heuristic(node, goal)

def reconstruct_path(parent, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()
    return path

def best_first_search(graph, start, goal, F):
    frontier = []
    f_value = F(start, goal, 0)
    heapq.heappush(frontier, (f_value, start))
    explored = set()
    parent = {start: None}
    path_cost = {start: 0}

    while frontier:
        dummy, current = heapq.heappop(frontier)
        if current == goal:
            final_path = reconstruct_path(parent, start, goal)
            final_cost = path_cost[current]
            return final_cost, final_path

        explored.add(current)
        for neighbor, cost in graph[current]:
            new_path_cost = path_cost[current] + cost
            if neighbor not in explored:
                parent[neighbor] = current
                path_cost[neighbor] = new_path_cost
                f_value = F(neighbor, goal, new_path_cost)
                heapq.heappush(frontier, (f_value, neighbor))

    return None


##     Main Function ↓↓↓↓↓↓↓↓      ##

graph = {
    "S": [("A", 2), ("B", 2)],
    "A": [("S", 2), ("G", 5)],
    "B": [("S", 2), ("G", 2)],
    "G": [("A", 5), ("B", 2)]
}

start = "S"
goal = "G"
draw_graph(graph, start, goal)

cost, path = best_first_search(graph, start, goal, greedy_f)
if path:
    print("Greedy Best-First Search")
    print("Path:", path)
    print("Path cost:", cost)
    draw_graph(graph, start, goal, path)
else:
    print("No path found.")


cost, path = best_first_search(graph, start, goal, astar_f)
if path:
    print("A* Search")
    print("Path:", path)
    print("Path cost:", cost)
    draw_graph(graph, start, goal, path)
else:
    print("No path found.")