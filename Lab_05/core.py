"""Variant 12 pipelines for triangular numbers."""

from __future__ import annotations

from collections.abc import Iterator
from itertools import takewhile

from streams import sliding_window, triangular_numbers


def triangular_numbers_up_to(limit: int) -> Iterator[int]:
    """Yield triangular numbers not greater than ``limit``."""
    return takewhile(lambda value: value <= limit, triangular_numbers())


def triangular_differences(limit: int) -> Iterator[int]:
    """Yield differences between neighboring triangular numbers up to a limit."""
    windows = sliding_window(triangular_numbers_up_to(limit), 2)
    yield from (right - left for left, right in windows)
