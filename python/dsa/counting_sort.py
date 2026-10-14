"""Counting sort: count how often each value appears, then write them out."""


def counting_sort(items: list[int]) -> list[int]:
    """Return a new sorted list of integers."""
    if not items:
        return []
    lo, hi = min(items), max(items)
    counts = [0] * (hi - lo + 1)  # one slot per possible value
    for x in items:
        counts[x - lo] += 1
    result = []
    for offset, count in enumerate(counts):
        result.extend([lo + offset] * count)
    return result
