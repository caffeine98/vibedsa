import math
import sys

import pytest

import dsa.recursion as rec
from dsa.recursion import factorial, fib, fib_memo, power

FIBS = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]


def test_factorial():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(3) == 6
    for n in range(20):
        assert factorial(n) == math.factorial(n)


def test_power():
    assert power(2, 0) == 1
    assert power(2, 10) == 1024
    assert power(3, 5) == 243
    assert power(0, 0) == 1
    for base in range(-3, 6):
        for exp in range(15):
            assert power(base, exp) == base**exp


def test_fib():
    assert [fib(n) for n in range(len(FIBS))] == FIBS


def test_fib_memo():
    assert [fib_memo(n) for n in range(len(FIBS))] == FIBS
    assert fib_memo(90) == 2880067194370816120


def count_fib_calls(n, monkeypatch):
    calls = 0
    original = rec.fib

    def counted(k):
        nonlocal calls
        calls += 1
        return original(k)

    monkeypatch.setattr(rec, "fib", counted)  # fib looks itself up at call time
    rec.fib(n)
    return calls


def test_naive_fib_call_counts(monkeypatch):
    # These numbers are quoted on the lesson page.
    assert count_fib_calls(4, monkeypatch) == 9
    assert count_fib_calls(30, monkeypatch) == 2_692_537


def test_deep_recursion_hits_the_limit():
    with pytest.raises(RecursionError):
        factorial(sys.getrecursionlimit() + 10)
