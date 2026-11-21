from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from types import MappingProxyType

from model import Dish, Ingredient


def add_ingredient(dish: Dish, ingredient: Ingredient) -> Dish:
    """Повертає нову страву з доданим інгредієнтом."""

    return replace(dish, ingredients=dish.ingredients + (ingredient,))


def remove_ingredient(dish: Dish, name: str) -> Dish:
    """Повертає копію страви без інгредієнта із заданою назвою."""

    remaining = tuple(item for item in dish.ingredients if item.name != name)
    if len(remaining) == len(dish.ingredients):
        raise ValueError(f"Інгредієнт {name!r} не знайдено")
    return replace(dish, ingredients=remaining)


def add_allergen(dish: Dish, allergen: str) -> Dish:
    """Повертає нову страву з позначеним алергеном."""

    if not allergen.strip():
        raise ValueError("Назва алергену не може бути порожньою")
    return replace(dish, allergens=dish.allergens | frozenset({allergen}))


def with_price(dish: Dish, price: float) -> Dish:
    """Повертає копію страви з оновленою ціною."""

    return replace(dish, price=price)


def filter_by_allergen(dishes: tuple[Dish, ...], allergen: str) -> tuple[Dish, ...]:
    """Вибирає страви, що містять вказаний алерген."""

    return tuple(dish for dish in dishes if allergen in dish.allergens)


def discounted(dish: Dish, percent: float) -> Dish:
    """Повертає нову страву зі знижкою, не змінюючи оригінал."""

    if not 0 <= percent <= 100:
        raise ValueError("Знижка має бути від 0 до 100 відсотків")
    return replace(dish, price=round(dish.price * (1 - percent / 100), 2))


def freeze(value: object) -> object:
    """Рекурсивно перетворює вкладені змінні колекції на незмінні."""

    if isinstance(value, Mapping):
        return MappingProxyType({key: freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(freeze(item) for item in value)
    if isinstance(value, (set, frozenset)):
        return frozenset(freeze(item) for item in value)
    return value
