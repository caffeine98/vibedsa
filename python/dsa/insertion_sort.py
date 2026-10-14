"""Insertion sort: grow a sorted part on the left, one item at a time."""


def insertion_sort(items: list[int]) -> None:
    """Sort items in place."""
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1
        while j >= 0 and items[j] > current:
            items[j + 1] = items[j]  # shift bigger items one slot right
            j -= 1
        items[j + 1] = current  # drop current into the gap
