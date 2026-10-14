"""Greedy algorithms: take the best-looking choice and never look back."""


def max_meetings(meetings: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Most meetings that don't overlap. Each meeting is (start, end).

    Greedy rule: always take the meeting that ends first.
    """
    chosen = []
    free_at = float("-inf")  # when the room is free again
    for start, end in sorted(meetings, key=lambda m: m[1]):
        if start >= free_at:
            chosen.append((start, end))
            free_at = end
    return chosen


def greedy_coins(coins: list[int], amount: int) -> list[int] | None:
    """Pay amount with the biggest coin that fits, again and again.

    Fewest coins for some coin sets, like 1, 5, 10, 25. Not for all.
    """
    used = []
    for coin in sorted(coins, reverse=True):
        while amount >= coin:
            amount -= coin
            used.append(coin)
    return used if amount == 0 else None
