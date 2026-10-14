"""Dynamic programming with a 2D table: two indexes describe each problem."""


def lcs_table(a: str, b: str) -> list[list[int]]:
    """table[i][j] = LCS length of the first i chars of a, first j of b."""
    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1  # extend a match
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])  # skip one
    return table


def lcs(a: str, b: str) -> str:
    """One longest common subsequence of a and b."""
    table = lcs_table(a, b)
    out = []
    i, j = len(a), len(b)
    while i > 0 and j > 0:  # walk back from the bottom-right corner
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(out))


def knapsack(items: list[tuple[int, int]], capacity: int) -> int:
    """Best total value that fits. Each item is (weight, value), used once.

    table[i][c] = best value using the first i items with capacity c.
    """
    table = [[0] * (capacity + 1) for _ in range(len(items) + 1)]
    for i, (weight, value) in enumerate(items, start=1):
        for c in range(capacity + 1):
            table[i][c] = table[i - 1][c]  # skip item i
            if weight <= c:  # or take it, if it fits
                take = table[i - 1][c - weight] + value
                table[i][c] = max(table[i][c], take)
    return table[len(items)][capacity]
