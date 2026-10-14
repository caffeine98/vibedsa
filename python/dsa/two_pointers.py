"""Two pointers: two indexes that move through the data in one pass."""

from dsa.linked_list import Node


def pair_with_sum(items: list[int], target: int) -> tuple[int, int] | None:
    """Two values in a sorted list that add up to target, or None."""
    lo, hi = 0, len(items) - 1  # start at both ends
    while lo < hi:
        total = items[lo] + items[hi]
        if total == target:
            return items[lo], items[hi]
        if total < target:
            lo += 1  # need a bigger sum: drop the smallest
        else:
            hi -= 1  # need a smaller sum: drop the biggest
    return None


def is_palindrome(text: str) -> bool:
    """Same forwards and backwards, ignoring case and non-letters."""
    chars = [c.lower() for c in text if c.isalnum()]
    lo, hi = 0, len(chars) - 1
    while lo < hi:
        if chars[lo] != chars[hi]:
            return False
        lo += 1
        hi -= 1
    return True


def remove_duplicates(items: list[int]) -> int:
    """Remove repeats from a sorted list in place. Return the new length.

    `write` marks where the next new value goes. `read` scans ahead.
    """
    if not items:
        return 0
    write = 1
    for read in range(1, len(items)):
        if items[read] != items[write - 1]:  # a value we haven't kept yet
            items[write] = items[read]
            write += 1
    del items[write:]
    return write


def has_cycle(head: Node | None) -> bool:
    """Does a linked list loop back on itself? (Floyd's algorithm)

    `fast` moves two nodes per step and `slow` moves one. If there's a
    loop, fast eventually laps slow and they meet.
    """
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False  # fast reached the end, so there's no loop
