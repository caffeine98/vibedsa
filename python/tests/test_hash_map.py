import random

import pytest

from dsa.hash_map import HashMap, HashSet


class SameHash:
    """Every instance hashes to the same value, so they all collide."""

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return 42

    def __eq__(self, other):
        return isinstance(other, SameHash) and self.name == other.name


def test_put_get_replace():
    m = HashMap()
    m.put("cat", 3)
    m.put("dog", 1)
    assert m.get("cat") == 3
    m.put("cat", 4)  # replace, not a second entry
    assert m.get("cat") == 4
    assert len(m) == 2


def test_missing_key():
    m = HashMap()
    with pytest.raises(KeyError):
        m.get("nope")
    with pytest.raises(KeyError):
        m.remove("nope")
    assert not m.contains("nope")


def test_remove():
    m = HashMap()
    m.put("a", 1)
    m.put("b", 2)
    m.remove("a")
    assert not m.contains("a")
    assert m.get("b") == 2
    assert len(m) == 1


def test_bucket_example_from_lesson():
    # Integers hash to themselves, so 12 and 20 share bucket 4 of 8.
    m = HashMap(num_buckets=8)
    for key in [12, 7, 20]:
        m.put(key, str(key))
    assert [k for k, _ in m.buckets[4]] == [12, 20]
    assert [k for k, _ in m.buckets[7]] == [7]
    assert m.get(20) == "20"


def test_collisions_still_work():
    m = HashMap()
    keys = [SameHash(i) for i in range(20)]
    for i, k in enumerate(keys):
        m.put(k, i)
    for i, k in enumerate(keys):
        assert m.get(k) == i
    m.remove(keys[5])
    assert not m.contains(keys[5])
    assert len(m) == 19


def test_resizes_to_keep_load_low():
    m = HashMap(num_buckets=8)
    for i in range(100):
        m.put(i, i)
    assert len(m) / len(m.buckets) <= 0.75
    assert all(m.get(i) == i for i in range(100))


def test_unhashable_key():
    m = HashMap()
    with pytest.raises(TypeError):
        m.put([1, 2], "lists can't be keys")


def test_random_operations_match_dict():
    rng = random.Random(0)
    m, ref = HashMap(num_buckets=2), {}
    for _ in range(5000):
        key = rng.choice([rng.randint(0, 60), f"k{rng.randint(0, 60)}"])
        op = rng.choice(["put", "put", "get", "remove"])
        if op == "put":
            m.put(key, rng.random())
            ref[key] = m.get(key)
        elif op == "get":
            if key in ref:
                assert m.get(key) == ref[key]
            else:
                assert not m.contains(key)
        elif op == "remove" and key in ref:
            m.remove(key)
            del ref[key]
        assert len(m) == len(ref)
    assert sorted(map(str, m)) == sorted(map(str, ref))


def test_hash_set():
    s = HashSet()
    s.add("a")
    s.add("a")
    s.add("b")
    assert len(s) == 2
    assert s.contains("a")
    s.remove("a")
    assert not s.contains("a")
