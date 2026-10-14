"""A dynamic array: a fixed block, replaced by a bigger one when full."""

from typing import Any, Iterator


class DynamicArray:
    def __init__(self) -> None:
        self.capacity = 1
        self.size = 0
        # Stands in for one fixed block of memory. We never grow it in place.
        self.slots: list[Any] = [None] * self.capacity

    def _check_index(self, i: int) -> None:
        if not 0 <= i < self.size:
            raise IndexError("index out of range")

    def get(self, i: int) -> Any:
        self._check_index(i)
        return self.slots[i]

    def set(self, i: int, value: Any) -> None:
        self._check_index(i)
        self.slots[i] = value

    def _resize(self, new_capacity: int) -> None:
        new_slots = [None] * new_capacity
        for i in range(self.size):  # copy every item: O(n)
            new_slots[i] = self.slots[i]
        self.slots = new_slots
        self.capacity = new_capacity

    def append(self, value: Any) -> None:
        if self.size == self.capacity:
            self._resize(2 * self.capacity)  # double, so resizes stay rare
        self.slots[self.size] = value
        self.size += 1

    def insert(self, i: int, value: Any) -> None:
        if not 0 <= i <= self.size:
            raise IndexError("index out of range")
        if self.size == self.capacity:
            self._resize(2 * self.capacity)
        for j in range(self.size, i, -1):  # shift right, starting from the end
            self.slots[j] = self.slots[j - 1]
        self.slots[i] = value
        self.size += 1

    def pop(self) -> Any:
        if self.size == 0:
            raise IndexError("pop from empty array")
        self.size -= 1
        value = self.slots[self.size]
        self.slots[self.size] = None
        return value

    def delete(self, i: int) -> Any:
        self._check_index(i)
        value = self.slots[i]
        for j in range(i, self.size - 1):  # shift left to close the gap
            self.slots[j] = self.slots[j + 1]
        self.size -= 1
        self.slots[self.size] = None
        return value

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[Any]:
        for i in range(self.size):
            yield self.slots[i]
