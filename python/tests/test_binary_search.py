import bisect
import random

from dsa.binary_search import binary_search, lower_bound

EXAMPLE = [2, 5, 8, 12, 16, 23, 38]


def test_finds_every_item():
    for i, value in enumerate(EXAMPLE):
        assert binary_search(EXAMPLE, value) == i


def test_missing_values():
    for value in [0, 3, 13, 20, 40]:
        assert binary_search(EXAMPLE, value) == -1


def test_empty_and_single():
    assert binary_search([], 1) == -1
    assert binary_search([7], 7) == 0
    assert binary_search([7], 3) == -1
    assert binary_search([7], 9) == -1


def test_duplicates_return_a_matching_index():
    items = [1, 3, 3, 3, 3, 9]
    assert items[binary_search(items, 3)] == 3


def test_lower_bound_basics():
    assert lower_bound(EXAMPLE, 12) == 3  # exact match
    assert lower_bound(EXAMPLE, 13) == 4  # between two values
    assert lower_bound(EXAMPLE, 0) == 0  # before all values
    assert lower_bound(EXAMPLE, 99) == len(EXAMPLE)  # after all values
    assert lower_bound([], 5) == 0


def test_lower_bound_finds_first_duplicate():
    assert lower_bound([1, 3, 3, 3, 3, 9], 3) == 1


def test_random_lists_match_reference():
    rng = random.Random(0)
    for _ in range(500):
        items = sorted(rng.randint(-20, 20) for _ in range(rng.randint(0, 30)))
        target = rng.randint(-25, 25)

        index = binary_search(items, target)
        if target in items:
            assert items[index] == target
        else:
            assert index == -1

        assert lower_bound(items, target) == bisect.bisect_left(items, target)
