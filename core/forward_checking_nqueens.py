def is_safe(row, col, assignment):
    for r, c in assignment.items():
        if col == c or abs(row - r) == abs(col - c):
            return False
    return True

def forward_check(row, col, domains, n):
    new_domains = {r: domains[r].copy() for r in domains}
    for r in range(row + 1, n):
        for c in list(new_domains[r]):
            if c == col or abs(row - r) == abs(col - c):
                new_domains[r].remove(c)
        if len(new_domains[r]) == 0:
            return None
    return new_domains

def backtrack_fc(row, n, assignment, domains, stats):
    if row == n:
        return True
    for col in sorted(domains[row]):
        stats["attempts"] += 1
        if is_safe(row, col, assignment):
            assignment[row] = col
            new_domains = forward_check(row, col, domains, n)
            if new_domains is not None:
                if backtrack_fc(row + 1, n, assignment, new_domains, stats):
                    return True
            del assignment[row]
            stats["backtracks"] += 1
    return False

def print_board(assignment, n):
    for row in range(n):
        print(" ".join("Q" if assignment[row] == col else "." for col in range(n)))

n = 4
assignment = {}
domains = {row: set(range(n)) for row in range(n)}
stats = {"attempts": 0, "backtracks": 0}
if backtrack_fc(0, n, assignment, domains, stats):
    print("Solution:", assignment)
    print_board(assignment, n)
else:
    print("No solution found")
print("Attempts:", stats["attempts"], "Backtracks:", stats["backtracks"])
