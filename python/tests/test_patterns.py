import itertools
import random

import pytest

from dsa.backtracking import count_queens, permutations, subsets
from dsa.dynamic_programming import climb_stairs, climb_stairs_memo, min_coins
from dsa.dynamic_programming_2d import knapsack, lcs, lcs_table
from dsa.greedy import greedy_coins, max_meetings
from dsa.linked_list import Node
from dsa.prefix_sums import build_prefix, count_subarrays_with_sum, range_sum
from dsa.sliding_window import (
    longest_unique_run,
    max_window_sum,
    shortest_sum_at_least,
)
from dsa.two_pointers import has_cycle, is_palindrome, pair_with_sum, remove_duplicates

rng = random.Random(0)


def random_list(lo=-10, hi=10, max_len=12):
    return [rng.randint(lo, hi) for _ in range(rng.randint(0, max_len))]


# Two pointers


def test_pair_with_sum_lesson_example():
    assert pair_with_sum([1, 3, 4, 6, 8, 11], 10) == (4, 6)
    assert pair_with_sum([1, 3, 4, 6, 8, 11], 100) is None
    assert pair_with_sum([], 1) is None
    assert pair_with_sum([5], 10) is None  # can't use one item twice


def test_pair_with_sum_matches_brute_force():
    for _ in range(500):
        items = sorted(random_list())
        target = rng.randint(-20, 20)
        found = pair_with_sum(items, target)
        exists = any(a + b == target for a, b in itertools.combinations(items, 2))
        assert (found is not None) == exists
        if found:
            assert sum(found) == target


def test_palindromes():
    assert is_palindrome("A man, a plan, a canal: Panama")
    assert is_palindrome("")
    assert is_palindrome("x")
    assert not is_palindrome("ab")


def test_remove_duplicates():
    items = [1, 1, 2, 3, 3, 3, 5]
    assert remove_duplicates(items) == 4
    assert items == [1, 2, 3, 5]
    for _ in range(300):
        items = sorted(random_list(0, 5))
        expected = sorted(set(items))
        assert remove_duplicates(items) == len(expected)
        assert items == expected


def make_list(n, loop_to=None):
    nodes = [Node(i) for i in range(n)]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if loop_to is not None and nodes:
        nodes[-1].next = nodes[loop_to]
    return nodes[0] if nodes else None


def test_linked_list_cycle():
    assert not has_cycle(None)
    assert not has_cycle(make_list(1))
    assert not has_cycle(make_list(10))
    assert has_cycle(make_list(1, loop_to=0))  # a node pointing at itself
    for n in range(1, 30):
        for k in range(n):
            assert has_cycle(make_list(n, loop_to=k))


# Sliding window


def test_sliding_window_lesson_examples():
    assert max_window_sum([2, 1, 5, 1, 3, 2], 3) == 9
    assert longest_unique_run("abcabcbb") == 3
    assert longest_unique_run("pwwkew") == 3
    assert longest_unique_run("") == 0
    assert shortest_sum_at_least([2, 3, 1, 2, 4, 3], 7) == 2
    assert shortest_sum_at_least([1, 1], 5) == 0
    with pytest.raises(ValueError):
        max_window_sum([1, 2], 3)


def test_sliding_window_matches_brute_force():
    for _ in range(300):
        nums = random_list(-10, 10, 15)
        if nums:
            k = rng.randint(1, len(nums))
            brute = max(sum(nums[i:i + k]) for i in range(len(nums) - k + 1))
            assert max_window_sum(nums, k) == brute

        text = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 15)))
        brute = max((j - i for i in range(len(text) + 1)
                     for j in range(i, len(text) + 1)
                     if len(set(text[i:j])) == j - i), default=0)
        assert longest_unique_run(text) == brute

        positives = random_list(1, 9, 15)
        target = rng.randint(1, 30)
        lengths = [j - i for i in range(len(positives))
                   for j in range(i + 1, len(positives) + 1)
                   if sum(positives[i:j]) >= target]
        assert shortest_sum_at_least(positives, target) == min(lengths, default=0)


# Prefix sums


def test_prefix_sums_lesson_example():
    prefix = build_prefix([3, 1, 4, 1, 5, 9])
    assert prefix == [0, 3, 4, 8, 9, 14, 23]
    assert range_sum(prefix, 1, 3) == 6
    assert range_sum(prefix, 0, 5) == 23
    assert count_subarrays_with_sum([1, 2, 3, -2, 2], 3) == 4


def test_prefix_sums_match_brute_force():
    for _ in range(300):
        nums = random_list()
        prefix = build_prefix(nums)
        for i in range(len(nums)):
            for j in range(i, len(nums)):
                assert range_sum(prefix, i, j) == sum(nums[i:j + 1])
        k = rng.randint(-10, 10)
        brute = sum(1 for i in range(len(nums)) for j in range(i, len(nums))
                    if sum(nums[i:j + 1]) == k)
        assert count_subarrays_with_sum(nums, k) == brute


# Backtracking


def test_subsets_lesson_example():
    assert subsets([1, 2, 3]) == [
        [], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]
    ]


def test_subsets_and_permutations_match_itertools():
    for n in range(6):
        items = list(range(n))
        expected = [list(c) for r in range(n + 1)
                    for c in itertools.combinations(items, r)]
        assert sorted(subsets(items)) == sorted(expected)
        assert sorted(permutations(items)) == sorted(
            list(p) for p in itertools.permutations(items)
        )


def test_n_queens_known_counts():
    assert [count_queens(n) for n in range(1, 9)] == [1, 0, 0, 2, 10, 4, 40, 92]


# Greedy


def test_meetings_lesson_example():
    meetings = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9),
                (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    assert max_meetings(meetings) == [(1, 4), (5, 7), (8, 11), (12, 16)]


def test_meetings_greedy_is_optimal():
    def compatible(chosen):
        chosen = sorted(chosen)
        return all(a[1] <= b[0] for a, b in zip(chosen, chosen[1:]))

    for _ in range(200):
        meetings = []
        for _ in range(rng.randint(0, 8)):
            start = rng.randint(0, 10)
            meetings.append((start, start + rng.randint(1, 5)))
        best = max(r for r in range(len(meetings) + 1)
                   for combo in itertools.combinations(meetings, r)
                   if compatible(combo))
        chosen = max_meetings(meetings)
        assert compatible(chosen) and len(chosen) == best


def test_greedy_coins_works_for_us_coins_but_not_all_coins():
    us = [1, 5, 10, 25]
    for amount in range(200):
        assert len(greedy_coins(us, amount)) == min_coins(us, amount)
    assert greedy_coins([1, 3, 4], 6) == [4, 1, 1]  # 3 coins...
    assert min_coins([1, 3, 4], 6) == 2  # ...but 3 + 3 uses 2
    assert greedy_coins([5, 10], 3) is None


# Dynamic programming


def test_climb_stairs():
    assert [climb_stairs(n) for n in range(7)] == [1, 1, 2, 3, 5, 8, 13]
    for n in range(40):
        assert climb_stairs(n) == climb_stairs_memo(n)
    assert climb_stairs(90) == 4660046610375530309


def brute_min_coins(coins, amount):
    for count in range(amount + 1):
        for combo in itertools.combinations_with_replacement(coins, count):
            if sum(combo) == amount:
                return count
    return None


def test_min_coins_lesson_table():
    assert [min_coins([1, 3, 4], a) for a in range(7)] == [0, 1, 2, 1, 1, 2, 2]
    assert min_coins([2], 3) is None
    assert min_coins([], 0) == 0


def test_min_coins_matches_brute_force():
    for _ in range(100):
        coins = sorted(set(rng.randint(1, 9) for _ in range(rng.randint(1, 3))))
        amount = rng.randint(0, 15)
        assert min_coins(coins, amount) == brute_min_coins(coins, amount)


def test_lcs_lesson_example():
    assert lcs_table("ABCDE", "ACE")[-1][-1] == 3
    assert lcs_table("ABCDE", "ACE") == [
        [0, 0, 0, 0], [0, 1, 1, 1], [0, 1, 1, 1],
        [0, 1, 2, 2], [0, 1, 2, 2], [0, 1, 2, 3],
    ]
    assert lcs("ABCDE", "ACE") == "ACE"
    assert lcs("", "ABC") == ""


def is_subsequence(small, big):
    it = iter(big)
    return all(ch in it for ch in small)


def test_lcs_matches_brute_force():
    for _ in range(200):
        a = "".join(rng.choice("ABC") for _ in range(rng.randint(0, 7)))
        b = "".join(rng.choice("ABC") for _ in range(rng.randint(0, 7)))
        best = max((r for r in range(len(a) + 1)
                    for combo in itertools.combinations(a, r)
                    if is_subsequence(combo, b)), default=0)
        result = lcs(a, b)
        assert len(result) == best == lcs_table(a, b)[-1][-1]
        assert is_subsequence(result, a) and is_subsequence(result, b)


def test_knapsack_lesson_example():
    assert knapsack([(1, 1), (3, 4), (4, 5), (5, 7)], 7) == 9
    assert knapsack([], 10) == 0
    assert knapsack([(5, 10)], 4) == 0


def test_knapsack_matches_brute_force():
    for _ in range(200):
        items = [(rng.randint(1, 6), rng.randint(0, 9))
                 for _ in range(rng.randint(0, 7))]
        capacity = rng.randint(0, 15)
        best = max(sum(v for _, v in combo)
                   for r in range(len(items) + 1)
                   for combo in itertools.combinations(items, r)
                   if sum(w for w, _ in combo) <= capacity)
        assert knapsack(items, capacity) == best
