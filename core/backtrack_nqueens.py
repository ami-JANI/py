def is_safe(row, col, assignment):
    for r, c in assignment.items():
        if col == c or abs(row - r) == abs(col - c):
            return False
    return True

def backtrack(row, n, assignment, stats):
    if row == n:
        return True
    for col in range(n):
        stats["attempts"] += 1
        if is_safe(row, col, assignment):
            assignment[row] = col
            if backtrack(row + 1, n, assignment, stats):
                return True
            del assignment[row]
            stats["backtracks"] += 1
    return False

def print_board(assignment, n):
    for row in range(n):
        print(" ".join("Q" if assignment[row] == col else "." for col in range(n)))

n = 4
assignment = {}
stats = {"attempts": 0, "backtracks": 0}
if backtrack(0, n, assignment, stats):
    print("Solution:", assignment)
    print_board(assignment, n)
else:
    print("No solution found")
print("Attempts:", stats["attempts"], "Backtracks:", stats["backtracks"])
