import random

import pytest

from dsa.big_o import (
    all_subsets,
    contains,
    first_item,
    halvings,
    has_duplicate_pairs,
    has_duplicate_set,
    has_duplicate_sorted,
)

DUPLICATE_CHECKS = [has_duplicate_pairs, has_duplicate_sorted, has_duplicate_set]


def test_first_item():
    assert first_item([4, 5, 6]) == 4


def test_halvings():
    assert halvings(1) == 0
    assert halvings(2) == 1
    assert halvings(8) == 3
    assert halvings(1000) == 9
    assert halvings(1_000_000) == 19


def test_contains():
    assert contains([3, 1, 4], 4)
    assert not contains([3, 1, 4], 2)
    assert not contains([], 1)


@pytest.mark.parametrize("check", DUPLICATE_CHECKS)
def test_duplicate_checks_edge_cases(check):
    assert not check([])
    assert not check([1])
    assert check([1, 1])
    assert check([3, 1, 4, 1, 5])
    assert not check([3, 1, 4, 2, 5])


@pytest.mark.parametrize("check", DUPLICATE_CHECKS)
def test_duplicate_checks_match_reference(check):
    rng = random.Random(0)
    for _ in range(300):
        items = [rng.randint(0, 40) for _ in range(rng.randint(0, 15))]
        assert check(items) == (len(set(items)) != len(items))


def test_all_subsets():
    assert all_subsets([]) == [[]]
    result = all_subsets([1, 2, 3])
    assert len(result) == 8
    assert sorted(map(sorted, result)) == sorted(
        [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
    )


def test_subsets_double_with_each_item():
    for n in range(8):
        assert len(all_subsets(list(range(n)))) == 2**n
