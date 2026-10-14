import random
from collections import deque

import pytest

from dsa.circular_queue import CircularQueue


def test_first_in_first_out():
    q = CircularQueue()
    for v in [1, 2, 3]:
        q.enqueue(v)
    assert q.peek() == 1
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == [1, 2, 3]
    assert q.is_empty()


def test_empty_queue_errors():
    q = CircularQueue()
    with pytest.raises(IndexError):
        q.dequeue()
    with pytest.raises(IndexError):
        q.peek()


def test_wraps_around_without_growing():
    q = CircularQueue(capacity=4)
    for v in [1, 2, 3, 4]:
        q.enqueue(v)
    q.dequeue()
    q.dequeue()
    q.enqueue(5)  # goes into slot 0
    q.enqueue(6)  # goes into slot 1
    assert len(q.slots) == 4
    assert q.slots == [5, 6, 3, 4]
    assert [q.dequeue() for _ in range(4)] == [3, 4, 5, 6]


def test_grows_while_wrapped():
    q = CircularQueue(capacity=4)
    for v in [1, 2, 3, 4]:
        q.enqueue(v)
    q.dequeue()
    q.enqueue(5)  # wrapped: slots are [5, 2, 3, 4], head = 1
    q.enqueue(6)  # full, so it grows and unwraps first
    assert len(q.slots) == 8
    assert [q.dequeue() for _ in range(5)] == [2, 3, 4, 5, 6]


def test_capacity_zero_still_works():
    q = CircularQueue(capacity=0)
    q.enqueue(1)
    assert q.dequeue() == 1


def test_random_operations_match_deque():
    rng = random.Random(0)
    q, ref = CircularQueue(capacity=2), deque()
    for _ in range(3000):
        if rng.random() < 0.55:
            v = rng.randint(0, 99)
            q.enqueue(v)
            ref.append(v)
        elif ref:
            assert q.dequeue() == ref.popleft()
        assert len(q) == len(ref)
        if ref:
            assert q.peek() == ref[0]
