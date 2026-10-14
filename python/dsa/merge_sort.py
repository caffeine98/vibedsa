"""Merge sort: split in half, sort each half, merge the two sorted halves."""


def merge_sort(items: list[int]) -> list[int]:
    """Return a new sorted list. The input is not changed."""
    if len(items) <= 1:  # base case: 0 or 1 items are already sorted
        return items[:]
    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    return merge(left, right)


def merge(left: list[int], right: list[int]) -> list[int]:
    """Combine two sorted lists into one sorted list."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= keeps equal items in order: stable
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])  # one side ran out; the rest of the
    result.extend(right[j:])  # other side is already sorted
    return result
