"""Binary search on a sorted list."""


def binary_search(items: list[int], target: int) -> int:
    """Return the index of target in items, or -1 if it is not there.

    items must be sorted in ascending order.
    """
    lo, hi = 0, len(items) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if items[mid] == target:
            return mid
        if items[mid] < target:
            lo = mid + 1  # target can only be to the right
        else:
            hi = mid - 1  # target can only be to the left
    return -1


def lower_bound(items: list[int], target: int) -> int:
    """Return the first index whose value is >= target.

    Returns len(items) if every value is smaller than target.
    Use it to find the first copy of a value, or where to insert one.
    """
    lo, hi = 0, len(items)  # hi starts one past the end
    while lo < hi:
        mid = (lo + hi) // 2
        if items[mid] < target:
            lo = mid + 1
        else:
            hi = mid  # mid might be the answer, so keep it
    return lo
