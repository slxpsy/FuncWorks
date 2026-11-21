from __future__ import annotations

import pytest

from algorithms import (
    Node,
    bfs_level_order,
    dfs_preorder_iter,
    fib,
    fib_iter,
    inorder,
    lcs_cache_clear,
    lcs_cache_info,
    lcs_length,
    lcs_length_iter,
    lcs_length_naive,
    postorder,
    preorder,
    quicksort,
)


def sample_tree() -> Node:
    return Node(4, Node(2, Node(1), Node(3)), Node(6, None, Node(7)))


@pytest.mark.parametrize(
    ("values", "expected"),
    [([], []), ([1], [1]), ([3, 2, 1], [1, 2, 3]), ([2, 2, 1, 3, 2], [1, 2, 2, 2, 3])],
)
def test_quicksort_boundaries_and_duplicates(values: list[int], expected: list[int]) -> None:
    original = values[:]
    assert quicksort(values) == expected
    assert values == original


def test_quicksort_matches_sorted_for_mixed_values() -> None:
    values = [9, -4, 0, 8, 8, 3, -12, 1]
    assert quicksort(values) == sorted(values)


def test_recursive_tree_traversals() -> None:
    tree = sample_tree()
    assert list(preorder(tree)) == [4, 2, 1, 3, 6, 7]
    assert list(inorder(tree)) == [1, 2, 3, 4, 6, 7]
    assert list(postorder(tree)) == [1, 3, 2, 7, 6, 4]


def test_iterative_tree_traversals_and_empty_tree() -> None:
    tree = sample_tree()
    assert bfs_level_order(tree) == [4, 2, 6, 1, 3, 7]
    assert dfs_preorder_iter(tree) == [4, 2, 1, 3, 6, 7]
    assert bfs_level_order(None) == []
    assert dfs_preorder_iter(None) == []
    assert list(preorder(None)) == []


def test_memoized_fibonacci_and_cache_api() -> None:
    fib.cache_clear()
    assert [fib(n) for n in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert fib(30) == 832040
    assert fib.cache_info().hits > 0
    fib.cache_clear()
    assert fib.cache_info().currsize == 0


def test_fibonacci_iterative_matches_and_rejects_negative() -> None:
    assert all(fib(n) == fib_iter(n) for n in range(50))
    with pytest.raises(ValueError):
        fib(-1)
    with pytest.raises(ValueError):
        fib_iter(-1)


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        ("", "abc", 0),
        ("abc", "", 0),
        ("abc", "abc", 3),
        ("abcde", "ace", 3),
        ("AGGTAB", "GXTXAYB", 4),
    ],
)
def test_lcs_examples(first: str, second: str, expected: int) -> None:
    lcs_cache_clear()
    assert lcs_length(first, second) == expected
    assert lcs_length_iter(first, second) == expected


def test_lcs_cache_and_naive_reference() -> None:
    first, second = "ABCBDAB", "BDCABA"
    lcs_cache_clear()
    assert lcs_length(first, second) == 4
    assert lcs_length(first, second) == 4
    assert lcs_cache_info().hits > 0
    assert lcs_length_naive("ABC", "BAC") == lcs_length("ABC", "BAC")
