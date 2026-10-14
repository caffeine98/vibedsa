"""Bubble sort: swap neighbors that are out of order, pass after pass."""


def bubble_sort(items: list[int]) -> None:
    """Sort items in place."""
    for end in range(len(items) - 1, 0, -1):
        swapped = False
        for i in range(end):  # items after `end` are already in place
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
        if not swapped:  # a pass with no swaps: everything is in order
            return
