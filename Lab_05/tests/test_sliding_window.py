import pytest

from streams import sliding_window


def test_basic_windows() -> None:
    assert list(sliding_window([1, 2, 3, 4], 3)) == [(1, 2, 3), (2, 3, 4)]


def test_window_larger_than_source_and_empty_source() -> None:
    assert list(sliding_window([1, 2], 3)) == []
    assert list(sliding_window([], 2)) == []


def test_window_size_one() -> None:
    assert list(sliding_window([4, 5], 1)) == [(4,), (5,)]


@pytest.mark.parametrize("k", [0, -1])
def test_non_positive_window_size_is_rejected(k: int) -> None:
    with pytest.raises(ValueError):
        list(sliding_window([1, 2, 3], k))


def test_window_consumes_source_only_as_needed() -> None:
    seen: list[int] = []

    def source():
        for value in range(5):
            seen.append(value)
            yield value

    windows = sliding_window(source(), 3)
    assert seen == []
    assert next(windows) == (0, 1, 2)
    assert seen == [0, 1, 2]
    assert next(windows) == (1, 2, 3)
    assert seen == [0, 1, 2, 3]
