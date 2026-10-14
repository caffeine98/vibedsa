import random

import pytest

from dsa.dynamic_array import DynamicArray


def make(*values):
    arr = DynamicArray()
    for v in values:
        arr.append(v)
    return arr


def test_empty():
    arr = DynamicArray()
    assert len(arr) == 0
    assert list(arr) == []
    with pytest.raises(IndexError):
        arr.pop()
    with pytest.raises(IndexError):
        arr.get(0)
    with pytest.raises(IndexError):
        arr.delete(0)


def test_get_set():
    arr = make(3, 7, 9)
    assert arr.get(1) == 7
    arr.set(1, 8)
    assert list(arr) == [3, 8, 9]
    with pytest.raises(IndexError):
        arr.get(3)
    with pytest.raises(IndexError):
        arr.get(-1)  # no negative indexes here, unlike Python's list


def test_insert_shifts_right():
    arr = make(3, 7, 9)
    arr.insert(1, 5)
    assert list(arr) == [3, 5, 7, 9]
    arr.insert(0, 1)  # front
    arr.insert(5, 11)  # end
    assert list(arr) == [1, 3, 5, 7, 9, 11]
    with pytest.raises(IndexError):
        arr.insert(8, 0)


def test_delete_shifts_left():
    arr = make(3, 5, 7, 9)
    assert arr.delete(1) == 5
    assert list(arr) == [3, 7, 9]
    assert arr.delete(2) == 9
    assert list(arr) == [3, 7]


def test_capacity_doubles():
    arr = DynamicArray()
    seen = []
    for i in range(20):
        arr.append(i)
        seen.append(arr.capacity)
    assert sorted(set(seen)) == [1, 2, 4, 8, 16, 32]


def test_appends_copy_fewer_than_2n_items(monkeypatch):
    # The amortized O(1) claim: n appends copy fewer than 2n items in total.
    arr = DynamicArray()
    copied = 0
    original = arr._resize

    def counting_resize(new_capacity):
        nonlocal copied
        copied += arr.size
        original(new_capacity)

    monkeypatch.setattr(arr, "_resize", counting_resize)
    n = 1000
    for i in range(n):
        arr.append(i)
    assert copied < 2 * n


def test_random_operations_match_list():
    rng = random.Random(0)
    arr, ref = DynamicArray(), []
    for _ in range(3000):
        op = rng.choice(["append", "insert", "pop", "delete", "set"])
        v = rng.randint(0, 99)
        if op == "append":
            arr.append(v)
            ref.append(v)
        elif op == "insert":
            i = rng.randint(0, len(ref))
            arr.insert(i, v)
            ref.insert(i, v)
        elif op == "pop" and ref:
            assert arr.pop() == ref.pop()
        elif op == "delete" and ref:
            i = rng.randrange(len(ref))
            assert arr.delete(i) == ref.pop(i)
        elif op == "set" and ref:
            i = rng.randrange(len(ref))
            arr.set(i, v)
            ref[i] = v
        assert list(arr) == ref
        assert arr.size <= arr.capacity
