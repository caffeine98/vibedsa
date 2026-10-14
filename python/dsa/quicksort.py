"""Quicksort: split around a pivot into smaller, equal and bigger groups."""

import random


def quicksort(items: list[int]) -> None:
    """Sort items in place."""
    _sort(items, 0, len(items) - 1)


def _sort(items: list[int], lo: int, hi: int) -> None:
    if lo >= hi:  # base case: 0 or 1 items
        return
    pivot = items[random.randint(lo, hi)]  # random: no input is reliably slow
    lt, gt = partition(items, lo, hi, pivot)
    _sort(items, lo, lt - 1)  # the smaller group
    _sort(items, gt + 1, hi)  # the bigger group. The equal group is done.


def partition(
    items: list[int], lo: int, hi: int, pivot: int
) -> tuple[int, int]:
    """Rearrange items[lo..hi] into  < pivot | == pivot | > pivot.

    Returns (lt, gt): the first and last index of the == pivot group.
    """
    lt, i, gt = lo, lo, hi
    while i <= gt:
        if items[i] < pivot:
            items[lt], items[i] = items[i], items[lt]
            lt += 1
            i += 1
        elif items[i] > pivot:
            items[i], items[gt] = items[gt], items[i]
            gt -= 1  # don't move i: the swapped-in item is unchecked
        else:
            i += 1
    return lt, gt
