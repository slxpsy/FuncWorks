from itertools import islice

from core import triangular_differences, triangular_numbers_up_to
from streams import take, triangular_numbers


def test_first_ten_triangular_numbers() -> None:
    assert take(10, triangular_numbers()) == [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]


def test_triangular_numbers_are_bounded_lazily() -> None:
    assert list(triangular_numbers_up_to(20)) == [1, 3, 6, 10, 15]
    assert list(triangular_numbers_up_to(0)) == []


def test_neighboring_differences() -> None:
    assert list(triangular_differences(20)) == [2, 3, 4, 5]
    assert list(triangular_differences(1)) == []


def test_infinite_stream_is_only_consumed_as_requested() -> None:
    stream = triangular_numbers()
    assert list(islice(stream, 3)) == [1, 3, 6]
    assert next(stream) == 10
