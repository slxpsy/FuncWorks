"""Рекурсивні алгоритми та ітеративні альтернативи для лабораторної роботи №4."""

from __future__ import annotations

from collections import deque
from collections.abc import Generator
from dataclasses import dataclass
from functools import lru_cache
from random import choice


def quicksort(values: list[int]) -> list[int]:
    """Повертає відсортовану копію списку методом рекурсивного quicksort."""
    if len(values) <= 1:
        return values[:]

    pivot = choice(values)
    lower = [value for value in values if value < pivot]
    equal = [value for value in values if value == pivot]
    greater = [value for value in values if value > pivot]
    return quicksort(lower) + equal + quicksort(greater)


@dataclass(slots=True)
class Node:
    """Вузол бінарного дерева цілих чисел."""

    key: int
    left: Node | None = None
    right: Node | None = None


def preorder(tree: Node | None) -> Generator[int, None, None]:
    """Рекурсивно обходить дерево у порядку корінь-ліво-право."""
    if tree is None:
        return
    yield tree.key
    yield from preorder(tree.left)
    yield from preorder(tree.right)


def inorder(tree: Node | None) -> Generator[int, None, None]:
    """Рекурсивно обходить дерево у порядку ліво-корінь-право."""
    if tree is None:
        return
    yield from inorder(tree.left)
    yield tree.key
    yield from inorder(tree.right)


def postorder(tree: Node | None) -> Generator[int, None, None]:
    """Рекурсивно обходить дерево у порядку ліво-право-корінь."""
    if tree is None:
        return
    yield from postorder(tree.left)
    yield from postorder(tree.right)
    yield tree.key


def bfs_level_order(tree: Node | None) -> list[int]:
    """Повертає обхід дерева в ширину з чергою."""
    if tree is None:
        return []
    queue = deque([tree])
    result: list[int] = []
    while queue:
        node = queue.popleft()
        result.append(node.key)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return result


def dfs_preorder_iter(tree: Node | None) -> list[int]:
    """Повертає прямий обхід дерева з явним стеком."""
    if tree is None:
        return []
    stack = [tree]
    result: list[int] = []
    while stack:
        node = stack.pop()
        result.append(node.key)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return result


@lru_cache(maxsize=None)  # noqa: UP033 - lru_cache є вимогою лабораторної
def fib(n: int) -> int:
    """Обчислює n-те число Фібоначчі рекурсивно з мемоізацією."""
    if n < 0:
        raise ValueError("n має бути невід'ємним")
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


def fib_iter(n: int) -> int:
    """Ітеративно обчислює n-те число Фібоначчі без рекурсивного стеку."""
    if n < 0:
        raise ValueError("n має бути невід'ємним")
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


def lcs_length_naive(first: str, second: str) -> int:
    """Обчислює довжину LCS без кешу; придатна для короткого порівняння."""

    def solve(i: int, j: int) -> int:
        if i == len(first) or j == len(second):
            return 0
        if first[i] == second[j]:
            return 1 + solve(i + 1, j + 1)
        return max(solve(i + 1, j), solve(i, j + 1))

    return solve(0, 0)


@lru_cache(maxsize=None)  # noqa: UP033 - демонструємо керований кеш станів
def _lcs_length_cached(first: str, second: str, i: int, j: int) -> int:
    if i == len(first) or j == len(second):
        return 0
    if first[i] == second[j]:
        return 1 + _lcs_length_cached(first, second, i + 1, j + 1)
    return max(
        _lcs_length_cached(first, second, i + 1, j),
        _lcs_length_cached(first, second, i, j + 1),
    )


def lcs_length(first: str, second: str) -> int:
    """Повертає довжину найдовшої спільної підпослідовності двох рядків."""
    return _lcs_length_cached(first, second, 0, 0)


def lcs_cache_info() -> object:
    """Повертає статистику кешу LCS для демонстрації повторних станів."""
    return _lcs_length_cached.cache_info()


def lcs_cache_clear() -> None:
    """Очищає кеш LCS між незалежними вимірюваннями."""
    _lcs_length_cached.cache_clear()


def lcs_length_iter(first: str, second: str) -> int:
    """Обчислює довжину LCS табуляцією без рекурсії."""
    previous = [0] * (len(second) + 1)
    for char_first in first:
        current = [0]
        for index, char_second in enumerate(second, start=1):
            if char_first == char_second:
                current.append(previous[index - 1] + 1)
            else:
                current.append(max(previous[index], current[-1]))
        previous = current
    return previous[-1]
