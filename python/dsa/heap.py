"""A min-heap stored in a list, and heap sort.

The tree lives in the list by index. For the node at index i:
    parent = (i - 1) // 2,  left child = 2i + 1,  right child = 2i + 2
"""

from typing import Any


class MinHeap:
    """The smallest item is always at index 0."""

    def __init__(self, items: list[Any] | None = None) -> None:
        self.items = list(items or [])
        # Build the heap: sift down every node that has children,
        # from the last one back to the root. O(n) in total.
        for i in range(len(self.items) // 2 - 1, -1, -1):
            self._sift_down(i)

    def push(self, item: Any) -> None:
        self.items.append(item)
        self._sift_up(len(self.items) - 1)

    def pop(self) -> Any:
        """Remove and return the smallest item."""
        if not self.items:
            raise IndexError("pop from empty heap")
        smallest = self.items[0]
        last = self.items.pop()
        if self.items:  # move the last item to the top, then sift it down
            self.items[0] = last
            self._sift_down(0)
        return smallest

    def peek(self) -> Any:
        if not self.items:
            raise IndexError("peek at empty heap")
        return self.items[0]

    def _sift_up(self, i: int) -> None:
        a = self.items
        while i > 0:
            parent = (i - 1) // 2
            if a[i] >= a[parent]:
                break  # parent is smaller: heap is fine
            a[i], a[parent] = a[parent], a[i]
            i = parent

    def _sift_down(self, i: int) -> None:
        a = self.items
        n = len(a)
        while True:
            smallest = i
            for child in (2 * i + 1, 2 * i + 2):
                if child < n and a[child] < a[smallest]:
                    smallest = child
            if smallest == i:
                break  # both children are bigger: heap is fine
            a[i], a[smallest] = a[smallest], a[i]
            i = smallest

    def __len__(self) -> int:
        return len(self.items)


def heap_sort(items: list[Any]) -> None:
    """Sort in place. Builds a max-heap, then moves the max to the end."""
    n = len(items)
    for i in range(n // 2 - 1, -1, -1):
        _sift_down_max(items, i, n)
    for end in range(n - 1, 0, -1):
        items[0], items[end] = items[end], items[0]  # max goes to its spot
        _sift_down_max(items, 0, end)  # the heap is now items[:end]


def _sift_down_max(a: list[Any], i: int, n: int) -> None:
    """Same as MinHeap._sift_down, but bigger items rise, within a[:n]."""
    while True:
        largest = i
        for child in (2 * i + 1, 2 * i + 2):
            if child < n and a[child] > a[largest]:
                largest = child
        if largest == i:
            break
        a[i], a[largest] = a[largest], a[i]
        i = largest
