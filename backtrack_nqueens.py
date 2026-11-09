
# Check whether a queen can be placed
def is_safe(row, col, assignment):
    for r, c in assignment.items():
        if col == c:                       # Same column
            return False
        if abs(row - r) == abs(col - c):   # Same diagonal
            return False
    return True


# Recursive backtracking
def backtrack(row, n, assignment, stats):

    if row == n:
        return True  # All queens placed

    for col in range(n):
        stats["attempts"] += 1

        if is_safe(row, col, assignment):
            assignment[row] = col

            if backtrack(row + 1, n, assignment, stats):
                return True

            # Undo the assignment
            del assignment[row]
            stats["backtracks"] += 1

    return False


# Display the chessboard
def print_board(assignment, n):
    for row in range(n):
        for col in range(n):
            if assignment[row] == col:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()


# Main program
n = 4
assignment = {}
stats = {"attempts": 0, "backtracks": 0}

if backtrack(0, n, assignment, stats):
    print("Solution:", assignment)
    print_board(assignment, n)
else:
    print("No solution found")

print("Attempts:", stats["attempts"])
print("Backtracks:", stats["backtracks"])
