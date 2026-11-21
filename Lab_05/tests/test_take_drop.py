from itertools import count, islice

import pytest

from streams import drop, take


def test_take_uses_only_the_requested_part_of_a_stream() -> None:
    values = count(1)
    assert take(5, values) == [1, 2, 3, 4, 5]
    assert take(3, values) == [6, 7, 8]


def test_drop_then_take_from_an_infinite_stream() -> None:
    assert list(islice(drop(10, count()), 3)) == [10, 11, 12]


def test_zero_and_empty_inputs() -> None:
    assert take(0, count()) == []
    assert list(drop(0, [])) == []
    assert take(5, []) == []


@pytest.mark.parametrize("n", [-1, -10])
def test_negative_take_and_drop_are_rejected(n: int) -> None:
    with pytest.raises(ValueError):
        take(n, [1, 2])
    with pytest.raises(ValueError):
        drop(n, [1, 2])
