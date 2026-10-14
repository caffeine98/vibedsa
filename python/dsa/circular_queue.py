"""A queue on a circular buffer. Both ends are O(1). Nothing shifts."""

from typing import Any


class CircularQueue:
    def __init__(self, capacity: int = 4) -> None:
        self.slots: list[Any] = [None] * max(1, capacity)
        self.head = 0  # index of the front item
        self.size = 0

    def enqueue(self, item: Any) -> None:
        if self.size == len(self.slots):
            self._grow()
        tail = (self.head + self.size) % len(self.slots)  # wraps to 0
        self.slots[tail] = item
        self.size += 1

    def dequeue(self) -> Any:
        if self.size == 0:
            raise IndexError("dequeue from empty queue")
        item = self.slots[self.head]
        self.slots[self.head] = None
        self.head = (self.head + 1) % len(self.slots)
        self.size -= 1
        return item

    def peek(self) -> Any:
        if self.size == 0:
            raise IndexError("peek at empty queue")
        return self.slots[self.head]

    def _grow(self) -> None:
        """Copy the items, front first, into a block twice the size."""
        old = self.slots
        self.slots = [None] * (2 * len(old))
        for i in range(self.size):
            self.slots[i] = old[(self.head + i) % len(old)]
        self.head = 0

    def is_empty(self) -> bool:
        return self.size == 0

    def __len__(self) -> int:
        return self.size
