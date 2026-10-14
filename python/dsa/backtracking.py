"""Backtracking: build an answer one choice at a time, and undo choices."""


def subsets(items: list[int]) -> list[list[int]]:
    """Every subset of items."""
    result: list[list[int]] = []
    current: list[int] = []

    def explore(start: int) -> None:
        result.append(current[:])  # record a copy of this subset
        for i in range(start, len(items)):
            current.append(items[i])  # choose
            explore(i + 1)  # explore with that choice
            current.pop()  # un-choose, so we can try the next one

    explore(0)
    return result


def permutations(items: list[int]) -> list[list[int]]:
    """Every ordering of items."""
    result: list[list[int]] = []
    current: list[int] = []
    used = [False] * len(items)

    def explore() -> None:
        if len(current) == len(items):
            result.append(current[:])
            return
        for i, x in enumerate(items):
            if not used[i]:
                used[i] = True
                current.append(x)
                explore()
                current.pop()
                used[i] = False

    explore()
    return result


def count_queens(n: int) -> int:
    """Ways to place n queens on an n x n board so none attack each other.

    Place one queen per row. Skip any square already under attack.
    """
    cols: set[int] = set()
    diagonals: set[int] = set()  # row - col is the same along a diagonal
    anti_diagonals: set[int] = set()  # row + col along the other way

    def place(row: int) -> int:
        if row == n:
            return 1  # every row has a queen: one full solution
        count = 0
        for col in range(n):
            attacked = (
                col in cols
                or row - col in diagonals
                or row + col in anti_diagonals
            )
            if attacked:
                continue  # prune: no solution can use this square
            cols.add(col)
            diagonals.add(row - col)
            anti_diagonals.add(row + col)
            count += place(row + 1)
            cols.remove(col)
            diagonals.remove(row - col)
            anti_diagonals.remove(row + col)
        return count

    return place(0)
