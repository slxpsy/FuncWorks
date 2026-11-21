"""Lazy iterator utilities and streams for Laboratory Work 5, variant 12."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable, Iterator
from itertools import accumulate, count, islice
from typing import TypeVar

T = TypeVar("T")


def naturals(start: int = 1) -> Iterator[int]:
    """Yield positive natural numbers beginning at ``start`` indefinitely."""
    if start < 1:
        raise ValueError("start must be a positive integer")
    yield from count(start)


def triangular_numbers() -> Iterator[int]:
    """Yield 1, 3, 6, 10, ... lazily from partial sums of natural numbers."""
    yield from accumulate(count(1))


def take(n: int, iterable: Iterable[T]) -> list[T]:
    """Return at most the first ``n`` values from an iterable."""
    if n < 0:
        raise ValueError("n must be non-negative")
    return list(islice(iterable, n))


def drop(n: int, iterable: Iterable[T]) -> Iterator[T]:
    """Return an iterator after lazily skipping its first ``n`` values."""
    if n < 0:
        raise ValueError("n must be non-negative")
    iterator = iter(iterable)
    next(islice(iterator, n, n), None)
    return iterator


def sliding_window(iterable: Iterable[T], k: int) -> Iterator[tuple[T, ...]]:
    """Yield consecutive windows of size ``k`` using bounded memory."""
    if k <= 0:
        raise ValueError("window size k must be positive")

    iterator = iter(iterable)
    window: deque[T] = deque(maxlen=k)
    for _ in range(k):
        try:
            window.append(next(iterator))
        except StopIteration:
            return

    yield tuple(window)
    for value in iterator:
        window.append(value)
        yield tuple(window)
