"""Prefix sums: precompute running totals to answer range sums in O(1)."""


def build_prefix(nums: list[int]) -> list[int]:
    """prefix[i] is the sum of the first i items. prefix[0] is 0."""
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    return prefix


def range_sum(prefix: list[int], i: int, j: int) -> int:
    """Sum of nums[i..j], both ends included."""
    return prefix[j + 1] - prefix[i]


def count_subarrays_with_sum(nums: list[int], k: int) -> int:
    """How many runs of neighbors add up to exactly k. Works with negatives.

    A run ending here sums to k when an earlier prefix equals running - k.
    """
    seen = {0: 1}  # prefix sum -> how many times it has appeared
    running = count = 0
    for x in nums:
        running += x
        count += seen.get(running - k, 0)
        seen[running] = seen.get(running, 0) + 1
    return count
