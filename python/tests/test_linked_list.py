import random
from collections import deque

import pytest

from dsa.linked_list import LinkedList


def make(*values):
    lst = LinkedList()
    for v in values:
        lst.push_back(v)
    return lst


def test_empty():
    lst = LinkedList()
    assert len(lst) == 0
    assert list(lst) == []
    assert not lst.find(1)
    assert not lst.remove(1)
    with pytest.raises(IndexError):
        lst.pop_front()


def test_push_front_and_back():
    lst = LinkedList()
    lst.push_back(7)
    lst.push_front(3)
    lst.push_back(9)
    assert list(lst) == [3, 7, 9]
    assert len(lst) == 3
    assert lst.head.value == 3
    assert lst.tail.value == 9


def test_pop_until_empty_resets_tail():
    lst = make(1, 2)
    assert lst.pop_front() == 1
    assert lst.pop_front() == 2
    assert lst.head is None and lst.tail is None
    lst.push_back(5)  # must still work after emptying
    assert list(lst) == [5]


def test_remove_head_middle_tail():
    lst = make(1, 2, 3, 4)
    assert lst.remove(1)  # head
    assert lst.remove(3)  # middle
    assert lst.remove(4)  # tail
    assert list(lst) == [2]
    assert lst.tail.value == 2
    lst.push_back(5)  # tail pointer must still be right
    assert list(lst) == [2, 5]


def test_remove_only_first_duplicate():
    lst = make(1, 2, 1)
    assert lst.remove(1)
    assert list(lst) == [2, 1]


def test_remove_missing():
    lst = make(1, 2)
    assert not lst.remove(9)
    assert list(lst) == [1, 2]


def test_random_operations_match_deque():
    rng = random.Random(0)
    lst, ref = LinkedList(), deque()
    for _ in range(2000):
        op = rng.choice(["front", "back", "pop", "remove", "find"])
        v = rng.randint(0, 9)
        if op == "front":
            lst.push_front(v)
            ref.appendleft(v)
        elif op == "back":
            lst.push_back(v)
            ref.append(v)
        elif op == "pop" and ref:
            assert lst.pop_front() == ref.popleft()
        elif op == "remove":
            found = v in ref
            assert lst.remove(v) == found
            if found:
                ref.remove(v)
        elif op == "find":
            assert lst.find(v) == (v in ref)
        assert list(lst) == list(ref)
        assert len(lst) == len(ref)
        assert (lst.tail.value if lst.tail else None) == (ref[-1] if ref else None)
