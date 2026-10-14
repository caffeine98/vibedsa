"""Recursion examples: a simple chain, halving, and repeated work."""


def factorial(n: int) -> int:
    """n! = n * (n - 1) * ... * 1"""
    if n <= 1:  # base case
        return 1
    return n * factorial(n - 1)  # recursive case: a smaller problem


def power(base: int, exp: int) -> int:
    """base ** exp in O(log exp) multiplications."""
    if exp == 0:  # base case
        return 1
    half = power(base, exp // 2)  # solve half the problem once
    if exp % 2 == 0:
        return half * half
    return half * half * base


def fib(n: int) -> int:
    """The n-th Fibonacci number. Exponential time: it repeats work."""
    if n < 2:  # base cases: fib(0) = 0, fib(1) = 1
        return n
    return fib(n - 1) + fib(n - 2)


def fib_memo(n: int) -> int:
    """The same, but each answer is saved and reused. Linear time."""
    memo: dict[int, int] = {}

    def solve(k: int) -> int:
        if k < 2:
            return k
        if k not in memo:
            memo[k] = solve(k - 1) + solve(k - 2)
        return memo[k]

    return solve(n)
