"""Small demonstration of lazy triangular-number pipelines."""

from __future__ import annotations

from itertools import accumulate
from operator import add

from core import triangular_differences, triangular_numbers_up_to
from streams import drop, sliding_window, take, triangular_numbers


def main() -> None:
    print(f"First 10 triangular numbers: {take(10, triangular_numbers())}")
    print(f"Triangular numbers up to 100: {list(triangular_numbers_up_to(100))}")
    print(f"Neighboring differences up to 100: {list(triangular_differences(100))}")
    print(f"After dropping 5 values: {take(5, drop(5, triangular_numbers()))}")
    print(f"Windows of size 3: {list(sliding_window(range(1, 7), 3))}")
    print(f"Prefix sums: {list(accumulate([1, 2, 3, 4], add))}")


if __name__ == "__main__":
    main()
