import random
from collections import deque

import pytest

from dsa.doubly_linked_list import DoublyLinkedList


def test_empty():
    lst = DoublyLinkedList()
    assert len(lst) == 0
    assert list(lst) == []
    with pytest.raises(IndexError):
        lst.pop_front()
    with pytest.raises(IndexError):
        lst.pop_back()


def test_push_and_pop_both_ends():
    lst = DoublyLinkedList()
    lst.push_back(7)
    lst.push_front(3)
    lst.push_back(9)
    assert list(lst) == [3, 7, 9]
    assert lst.pop_back() == 9
    assert lst.pop_front() == 3
    assert list(lst) == [7]


def test_remove_node_in_middle():
    lst = DoublyLinkedList()
    lst.push_back(1)
    middle = lst.push_back(2)
    lst.push_back(3)
    assert lst.remove(middle) == 2
    assert list(lst) == [1, 3]
    assert len(lst) == 2


def test_links_are_consistent_backwards():
    lst = DoublyLinkedList()
    for v in [1, 2, 3]:
        lst.push_back(v)
    values = []
    node = lst.tail.prev
    while node is not lst.head:
        values.append(node.value)
        node = node.prev
    assert values == [3, 2, 1]


def test_random_operations_match_deque():
    rng = random.Random(0)
    lst, ref = DoublyLinkedList(), deque()
    for _ in range(2000):
        op = rng.choice(["front", "back", "pop_front", "pop_back"])
        v = rng.randint(0, 99)
        if op == "front":
            lst.push_front(v)
            ref.appendleft(v)
        elif op == "back":
            lst.push_back(v)
            ref.append(v)
        elif op == "pop_front" and ref:
            assert lst.pop_front() == ref.popleft()
        elif op == "pop_back" and ref:
            assert lst.pop_back() == ref.pop()
        assert list(lst) == list(ref)
        assert len(lst) == len(ref)
