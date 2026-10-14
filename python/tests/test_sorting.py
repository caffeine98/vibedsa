import random

import pytest

from dsa.bubble_sort import bubble_sort
from dsa.counting_sort import counting_sort
from dsa.insertion_sort import insertion_sort
from dsa.merge_sort import merge, merge_sort
from dsa.quicksort import partition, quicksort


# Wrap every sort so each one takes a list and returns a sorted list.
def in_place(sort):
    def run(items):
        copy = list(items)
        sort(copy)
        return copy

    return run


SORTS = {
    "bubble": in_place(bubble_sort),
    "insertion": in_place(insertion_sort),
    "merge": merge_sort,
    "quick": in_place(quicksort),
    "counting": counting_sort,
}
STABLE = ["bubble", "insertion", "merge"]

CASES = [
    [],
    [1],
    [2, 1],
    [1, 2, 3, 4, 5],  # already sorted
    [5, 4, 3, 2, 1],  # reversed
    [3, 3, 3, 3],  # all equal
    [4, -1, 0, -7, 4, 2],  # negatives and duplicates
]


@pytest.mark.parametrize("name", SORTS)
@pytest.mark.parametrize("items", CASES)
def test_edge_cases(name, items):
    assert SORTS[name](items) == sorted(items)


@pytest.mark.parametrize("name", SORTS)
def test_random_lists(name):
    rng = random.Random(0)
    for _ in range(300):
        items = [rng.randint(-50, 50) for _ in range(rng.randint(0, 40))]
        assert SORTS[name](items) == sorted(items)


def test_merge_sort_leaves_input_alone():
    items = [3, 1, 2]
    merge_sort(items)
    assert items == [3, 1, 2]


class Item:
    """Compares by key only, so we can see if equal keys keep their order."""

    def __init__(self, key, tag):
        self.key, self.tag = key, tag

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __le__(self, other):
        return self.key <= other.key


@pytest.mark.parametrize("name", STABLE)
def test_stable(name):
    items = [Item(2, "a"), Item(1, "b"), Item(2, "c"), Item(1, "d")]
    result = SORTS[name](items)
    assert [x.tag for x in result] == ["b", "d", "a", "c"]


def test_quicksort_handles_large_sorted_and_equal_inputs():
    # A fixed pivot would make these O(n^2) and hit the recursion limit.
    for items in [list(range(5000)), [7] * 5000, list(range(5000, 0, -1))]:
        assert SORTS["quick"](items) == sorted(items)


# The examples traced on the lesson pages.


def test_partition_example():
    items = [7, 2, 9, 4, 7, 1, 8]
    assert partition(items, 0, 6, 7) == (3, 4)
    assert items == [2, 1, 4, 7, 7, 8, 9]


def test_merge_example():
    assert merge([27, 38, 43], [3, 9, 10, 82]) == [3, 9, 10, 27, 38, 43, 82]


def count_bubble_comparisons(values):
    comparisons = 0

    class Counted:
        def __init__(self, v):
            self.v = v

        def __gt__(self, other):
            nonlocal comparisons
            comparisons += 1
            return self.v > other.v

    items = [Counted(v) for v in values]
    bubble_sort(items)
    assert [x.v for x in items] == sorted(values)
    return comparisons


def test_bubble_stops_early():
    # Sorted input: one pass of n - 1 comparisons, no swaps, stop.
    assert count_bubble_comparisons(list(range(10))) == 9
    # The lesson example: passes of 4, 3 and 2 comparisons. The third
    # pass has no swaps, so the last pass (1 comparison) never runs.
    assert count_bubble_comparisons([5, 1, 4, 2, 8]) == 4 + 3 + 2


def test_counting_sort_example():
    assert counting_sort([4, 1, 3, 4, 1, 4]) == [1, 1, 3, 4, 4, 4]
