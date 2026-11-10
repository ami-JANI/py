import heapq

def heuristic(node, goal):
    h = {"S": 4, "A": 1, "B": 2, "G": 0}
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
    heapq.heappush(frontier, (F(start, goal, 0), start))
    explored = set()
    parent = {start: None}
    path_cost = {start: 0}
    while frontier:
        f, current = heapq.heappop(frontier)
        if current == goal:
            return path_cost[current], reconstruct_path(parent, start, goal)
        explored.add(current)
        for neighbor, cost in graph[current]:
            new_cost = path_cost[current] + cost
            if neighbor not in explored:
                parent[neighbor] = current
                path_cost[neighbor] = new_cost
                heapq.heappush(frontier, (F(neighbor, goal, new_cost), neighbor))
    return None

graph = {
    "S": [("A", 2), ("B", 2)],
    "A": [("S", 2), ("G", 5)],
    "B": [("S", 2), ("G", 2)],
    "G": [("A", 5), ("B", 2)]
}

cost, path = best_first_search(graph, "S", "G", greedy_f)
print("Greedy:", path, "cost:", cost)
cost, path = best_first_search(graph, "S", "G", astar_f)
print("A*:", path, "cost:", cost)
