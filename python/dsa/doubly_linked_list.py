"""A doubly linked list with sentinel nodes.

The two sentinels sit before the first item and after the last one.
They hold no value. Because they always exist, every real node has a
prev and a next, so insert and remove need no special cases.
"""

from typing import Any, Iterator


class DNode:
    def __init__(self, value: Any = None) -> None:
        self.value = value
        self.prev: DNode | None = None
        self.next: DNode | None = None


class DoublyLinkedList:
    def __init__(self) -> None:
        self.head = DNode()  # sentinel before the first item
        self.tail = DNode()  # sentinel after the last item
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _insert_between(
        self, value: Any, before: DNode, after: DNode
    ) -> DNode:
        """Link a new node in between two neighbors. Used by both pushes."""
        node = DNode(value)
        node.prev = before
        node.next = after
        before.next = node
        after.prev = node
        self.size += 1
        return node

    def push_front(self, value: Any) -> DNode:
        """Add value at the front: between the head sentinel and item 1."""
        return self._insert_between(value, self.head, self.head.next)

    def push_back(self, value: Any) -> DNode:
        """Add value at the back: between the last item and tail sentinel."""
        return self._insert_between(value, self.tail.prev, self.tail)

    def remove(self, node: DNode) -> Any:
        """Unlink a node in O(1). The node must be in this list."""
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        return node.value

    def pop_front(self) -> Any:
        if self.size == 0:
            raise IndexError("pop from empty list")
        return self.remove(self.head.next)

    def pop_back(self) -> Any:
        if self.size == 0:
            raise IndexError("pop from empty list")
        return self.remove(self.tail.prev)

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[Any]:
        node = self.head.next
        while node is not self.tail:
            yield node.value
            node = node.next
