import heapq

def manhattan_distance(cell, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

def greedy_f(cell, goal, path_cost):
    return manhattan_distance(cell, goal)

def astar_f(cell, goal, path_cost):
    return path_cost + manhattan_distance(cell, goal)

def get_neighbors(cell, grid):
    r, c = cell
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != -1:
            neighbors.append((nr, nc))
    return neighbors

def reconstruct_path(parent, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()
    return path

def best_first_search(grid, start, goal, F):
    frontier = []
    heapq.heappush(frontier, (F(start, goal, 0), start))
    explored = set()
    parent = {start: None}
    path_cost = {start: 0}
    while frontier:
        f, current = heapq.heappop(frontier)
        if current == goal:
            return reconstruct_path(parent, start, goal)
        explored.add(current)
        for cell in get_neighbors(current, grid):
            new_cost = path_cost[current] + 1
            if cell not in explored:
                parent[cell] = current
                path_cost[cell] = new_cost
                heapq.heappush(frontier, (F(cell, goal, new_cost), cell))
    return None

grid = [
    [-1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [-1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0],
    [-1,  0, -1,  0,  0,  0,  0,  0,  0,  0, -1,  0],
    [-1,  0, -1,  0, -1, -1, -1, -1, -1,  0, -1,  0],
    [-1,  0,  0,  0, -1,  0,  0,  0,  0,  0, -1,  0],
    [-1, -1, -1,  0, -1,  0, -1, -1, -1, -1, -1,  0],
    [ 0,  0,  0,  0, -1,  0,  0,  0,  0,  0,  0,  0]
]
start = (6, 0)
goal = (0, 11)

path = best_first_search(grid, start, goal, greedy_f)
print("Greedy cost:", len(path) - 1, path)
path = best_first_search(grid, start, goal, astar_f)
print("A* cost:", len(path) - 1, path)
