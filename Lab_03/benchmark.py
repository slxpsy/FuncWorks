from __future__ import annotations

import statistics
import timeit
from collections.abc import Callable
from app import get_sample_menu
from core import add_allergen


def main() -> None:
    dish = get_sample_menu()[0]
    mutable = {"allergens": {"глютен", "молоко"}}

    def mutable_update() -> dict[str, set[str]]:
        result = dict(mutable)
        result["allergens"] = mutable["allergens"] | {"соєві боби"}
        return result

    def immutable_update():
        return add_allergen(dish, "соєві боби")

    def median_ms(function: Callable[[], object]) -> float:
        return statistics.median(timeit.repeat(function, number=20_000, repeat=7)) * 1000

    print(f"Python: {__import__('sys').version.split()[0]}")
    print(f"Mutable dict/set update: {median_ms(mutable_update):.2f} ms / 20,000")
    print(f"Frozen dataclass/frozenset update: {median_ms(immutable_update):.2f} ms / 20,000")


if __name__ == "__main__":
    main()
