from itertools import accumulate
from operator import mul


def test_prefix_sums_and_products() -> None:
    values = [1, 2, 3, 4]
    assert list(accumulate(values)) == [1, 3, 6, 10]
    assert list(accumulate(values, mul)) == [1, 2, 6, 24]
