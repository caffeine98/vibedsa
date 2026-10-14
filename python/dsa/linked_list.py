"""A singly linked list with head and tail pointers."""

from typing import Any, Iterator


class Node:
    def __init__(self, value: Any) -> None:
        self.value = value
        self.next: Node | None = None


class LinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None
        self.tail: Node | None = None
        self.size = 0

    def push_front(self, value: Any) -> None:
        node = Node(value)
        node.next = self.head
        self.head = node
        if self.tail is None:  # list was empty
            self.tail = node
        self.size += 1

    def push_back(self, value: Any) -> None:
        node = Node(value)
        if self.tail is None:  # list was empty
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def pop_front(self) -> Any:
        if self.head is None:
            raise IndexError("pop from empty list")
        node = self.head
        self.head = node.next
        if self.head is None:  # list is now empty
            self.tail = None
        self.size -= 1
        return node.value

    def find(self, value: Any) -> bool:
        node = self.head
        while node is not None:
            if node.value == value:
                return True
            node = node.next
        return False

    def remove(self, value: Any) -> bool:
        """Remove the first node holding value. Return False if not found."""
        prev = None
        node = self.head
        while node is not None and node.value != value:
            prev = node
            node = node.next
        if node is None:
            return False

        if prev is None:  # removing the head
            self.head = node.next
        else:
            prev.next = node.next  # skip over node
        if node is self.tail:
            self.tail = prev
        self.size -= 1
        return True

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[Any]:
        node = self.head
        while node is not None:
            yield node.value
            node = node.next
