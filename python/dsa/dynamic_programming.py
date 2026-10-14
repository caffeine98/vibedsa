"""Dynamic programming: solve each smaller problem once, and reuse it."""

from functools import cache


def climb_stairs_memo(n: int) -> int:
    """Ways to climb n stairs taking 1 or 2 steps at a time. Top-down."""

    @cache  # remember every answer: each n is solved once
    def ways(i: int) -> int:
        if i <= 1:
            return 1  # 0 or 1 stairs: one way
        return ways(i - 1) + ways(i - 2)  # last step was 1, or was 2

    return ways(n)


def climb_stairs(n: int) -> int:
    """The same answer, bottom-up: fill a table from the smallest case."""
    table = [1] * (n + 1)  # table[i] = ways to climb i stairs
    for i in range(2, n + 1):
        table[i] = table[i - 1] + table[i - 2]
    return table[n]


def min_coins(coins: list[int], amount: int) -> int | None:
    """Fewest coins that add up to amount, or None if impossible."""
    INF = float("inf")
    best = [0] + [INF] * amount  # best[a] = fewest coins for amount a
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and best[a - coin] + 1 < best[a]:
                best[a] = best[a - coin] + 1  # use coin, then pay a - coin
    return None if best[amount] == INF else int(best[amount])
