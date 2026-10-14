"""One small function for each common growth rate."""


# O(1): the work does not depend on the input size.
def first_item(items: list[int]) -> int:
    return items[0]


# O(log n): the problem halves each step.
def halvings(n: int) -> int:
    """How many times n can be halved before it reaches 1."""
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps


# O(n): one pass over the input.
def contains(items: list[int], target: int) -> bool:
    for item in items:
        if item == target:
            return True
    return False


# The same question, answered three ways with three different costs.

# O(n^2): compare every pair.
def has_duplicate_pairs(items: list[int]) -> bool:
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False


# O(n log n): sort, then duplicates sit next to each other.
def has_duplicate_sorted(items: list[int]) -> bool:
    ordered = sorted(items)  # the sort is the O(n log n) part
    for i in range(1, len(ordered)):
        if ordered[i] == ordered[i - 1]:
            return True
    return False


# O(n): remember what you have seen in a set.
def has_duplicate_set(items: list[int]) -> bool:
    seen = set()
    for item in items:
        if item in seen:  # O(1) on average
            return True
        seen.add(item)
    return False


# O(2^n): every item is either in or out of each subset.
def all_subsets(items: list[int]) -> list[list[int]]:
    subsets: list[list[int]] = [[]]
    for item in items:
        subsets += [subset + [item] for subset in subsets]  # doubles the count
    return subsets
