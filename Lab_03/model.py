from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True, slots=True)
class Ingredient:
    """Незмінний інгредієнт страви."""

    name: str
    quantity_g: float

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Назва інгредієнта не може бути порожньою")
        if self.quantity_g <= 0:
            raise ValueError("Кількість інгредієнта має бути додатною")


@dataclass(frozen=True, slots=True)
class Dish:
    """Незмінна позиція ресторанного меню."""

    dish_id: int
    name: str
    price: float
    ingredients: tuple[Ingredient, ...]
    allergens: frozenset[str]
    meta: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))

    def __post_init__(self) -> None:
        if self.dish_id <= 0:
            raise ValueError("Ідентифікатор страви має бути додатним")
        if not self.name.strip():
            raise ValueError("Назва страви не може бути порожньою")
        if self.price < 0:
            raise ValueError("Ціна не може бути від’ємною")
        if not isinstance(self.ingredients, tuple):
            raise TypeError("Інгредієнти мають зберігатися у tuple")
        if not isinstance(self.allergens, frozenset):
            raise TypeError("Алергени мають зберігатися у frozenset")
        object.__setattr__(self, "meta", MappingProxyType(dict(self.meta)))


def make_meta(**values: str) -> Mapping[str, str]:
    """Створює незмінні метадані на основі приватної копії словника."""

    return MappingProxyType(dict(values))
