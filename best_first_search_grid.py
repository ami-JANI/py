# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 22:32:14 2026

@author: 00wal
"""

import copy
import heapq
import matplotlib.pyplot as plt

def draw_grid(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])
    fig, ax = plt.subplots(figsize=(12, 7))
    # Draw cells
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == -1:
                color = "dimgray"   # Blocked
            elif grid[r][c] == 1:
                color = "green"     # Path
            else:
                color = "white"     # Free
            rect = plt.Rectangle((c, rows - 1 - r), 1, 1, facecolor=color, edgecolor="black")
            ax.add_patch(rect)

    # Mark start and goal
    ax.text(start[1] + 0.5, rows - 1 - start[0] + 0.5, "A", ha="center", va="center", fontsize=20)
    ax.text(goal[1] + 0.5,rows - 1 - goal[0] + 0.5,"B",ha="center",va="center",fontsize=20)
    # Formatting
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.set_xticks(range(cols + 1))
    ax.set_yticks(range(rows + 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(False)
    plt.show()

def manhattan_distance(cell, goal):
    r1, c1 = cell
    r2, c2 = goal
    return abs(r1 - r2) + abs(c1 - c2)

def greedy_f(cell, goal, path_cost):
    return manhattan_distance(cell, goal)

def astar_f(cell, goal, path_cost):
    return path_cost + manhattan_distance(cell, goal)

def get_neighbors(cell, grid):
    r, c = cell
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    rows = len(grid)
    cols = len(grid[0])
    for mv in moves:
        nr = r + mv[0]
        nc = c + mv[1]
        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] != -1:
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

def draw_grid_with_path(grid, path, start, goal):
    grid_copy = copy.deepcopy(grid)
    for r, c in path:
        grid_copy[r][c] = 1
    draw_grid(grid_copy, start, goal)
    

def best_first_search(grid, start, goal, F):
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
            return final_path

        explored.add(current)
        for cell in get_neighbors(current, grid):
            cost = 1
            new_path_cost = path_cost[current] + cost
            if cell not in explored:
                parent[cell] = current
                path_cost[cell] = new_path_cost
                f_value = F(cell, goal, new_path_cost)
                heapq.heappush(frontier, (f_value, cell))

    return None

##     Main Function ↓↓↓↓↓↓↓↓      ##

# -1 = blocked, 0 = free
grid = [
    [-1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],  # Row 1
    [-1,  0, -1, -1, -1, -1, -1, -1, -1, -1, -1,  0],  # Row 2
    [-1,  0, -1,  0,  0,  0,  0,  0,  0,  0, -1,  0],  # Row 3
    [-1,  0, -1,  0, -1, -1, -1, -1, -1,  0, -1,  0],  # Row 4
    [-1,  0,  0,  0, -1,  0,  0,  0,  0,  0, -1,  0],  # Row 5
    [-1, -1, -1,  0, -1,  0, -1, -1, -1, -1, -1,  0],  # Row 6
    [ 0,  0,  0,  0, -1,  0,  0,  0,  0,  0,  0,  0]   # Row 7
]
start = (6, 0)
goal = (0, 11)
draw_grid(grid, start, goal)

path = best_first_search(grid, start, goal, greedy_f)
if path:
    print("Greedy Best-First Search")
    print("Path cost:", len(path) - 1)
    draw_grid_with_path(grid, path, start, goal)
else:
    print("No path found.")

path = best_first_search(grid, start, goal, astar_f)
if path:
    print("A* Search")
    print("Path cost:", len(path) - 1)
    draw_grid_with_path(grid, path, start, goal)
else:
    print("No path found.")






