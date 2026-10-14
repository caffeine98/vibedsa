"""A stack, and a classic use for one: checking brackets."""

from typing import Any


class Stack:
    """Last in, first out. The end of a Python list is the top."""

    def __init__(self) -> None:
        self.items: list[Any] = []

    def push(self, item: Any) -> None:
        self.items.append(item)

    def pop(self) -> Any:
        if not self.items:
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self) -> Any:
        if not self.items:
            raise IndexError("peek at empty stack")
        return self.items[-1]

    def is_empty(self) -> bool:
        return not self.items

    def __len__(self) -> int:
        return len(self.items)


PAIRS = {")": "(", "]": "[", "}": "{"}


def is_balanced(text: str) -> bool:
    """True if every bracket is closed, in the right order."""
    stack = Stack()
    for ch in text:
        if ch in "([{":
            stack.push(ch)
        elif ch in PAIRS:
            if stack.is_empty() or stack.pop() != PAIRS[ch]:
                return False
    return stack.is_empty()  # anything left was opened but never closed
