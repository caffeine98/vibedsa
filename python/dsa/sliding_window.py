"""Sliding window: track a range of neighbors as it moves along."""


def max_window_sum(nums: list[int], k: int) -> int:
    """Largest sum of any k items in a row. Fixed-size window."""
    if not 0 < k <= len(nums):
        raise ValueError("need 0 < k <= len(nums)")
    window = sum(nums[:k])
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]  # add the new, drop the old
        best = max(best, window)
    return best


def longest_unique_run(text: str) -> int:
    """Length of the longest stretch with no repeated characters."""
    last_seen: dict[str, int] = {}  # character -> its latest index
    left = best = 0
    for right, ch in enumerate(text):
        if last_seen.get(ch, -1) >= left:  # ch repeats inside the window
            left = last_seen[ch] + 1  # shrink: start just past the repeat
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


def shortest_sum_at_least(nums: list[int], target: int) -> int:
    """Shortest run of positive numbers with sum >= target. 0 if none."""
    left = total = 0
    best = len(nums) + 1
    for right, x in enumerate(nums):
        total += x  # grow the window to the right
        while total >= target:  # big enough: shrink from the left
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return best if best <= len(nums) else 0
