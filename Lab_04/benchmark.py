"""Порівняння рекурсивної, мемоізованої та ітеративної реалізацій."""

from collections.abc import Callable
from timeit import repeat

from algorithms import (
    fib,
    fib_iter,
    lcs_cache_clear,
    lcs_length,
    lcs_length_iter,
    lcs_length_naive,
)


def best_time(statement: Callable[[], object], number: int = 1, repeat_count: int = 5) -> float:
    return min(repeat(statement, number=number, repeat=repeat_count)) / number


def memoized_fib() -> int:
    fib.cache_clear()
    return fib(30)


def memoized_lcs(first: str, second: str) -> int:
    lcs_cache_clear()
    return lcs_length(first, second)


def main() -> None:
    print("Fibonacci, n=30, секунди (найкращий результат з 5 повторів)")
    print(f"  memoized: {best_time(memoized_fib):.6f}")
    print(f"  iterative: {best_time(lambda: fib_iter(30)):.6f}")

    first, second = "ABCD" * 3, "BACD" * 3
    print("LCS, рядки довжини 12, секунди (найкращий результат з 5 повторів)")
    print(f"  recursive without cache: {best_time(lambda: lcs_length_naive(first, second)):.6f}")
    print(f"  memoized: {best_time(lambda: memoized_lcs(first, second)):.6f}")
    print(f"  iterative: {best_time(lambda: lcs_length_iter(first, second)):.6f}")


if __name__ == "__main__":
    main()
