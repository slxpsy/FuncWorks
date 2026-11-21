from __future__ import annotations

import pytest

from app import get_sample_menu
from core import add_allergen, add_ingredient, discounted, filter_by_allergen, freeze, remove_ingredient, with_price
from model import Dish, Ingredient, make_meta


@pytest.fixture
def dish() -> Dish:
    return Dish(12, "Паста з соусом", 165.0,
                (Ingredient("Паста", 120.0), Ingredient("Соус", 80.0)),
                frozenset({"глютен"}), make_meta(category="основна страва"))


def test_add_ingredient_does_not_mutate_original(dish: Dish) -> None:
    extra = Ingredient("Песто", 25.0)
    updated = add_ingredient(dish, extra)
    assert updated is not dish
    assert updated.ingredients == dish.ingredients + (extra,)
    assert len(dish.ingredients) == 2


def test_remove_ingredient_returns_new_dish(dish: Dish) -> None:
    updated = remove_ingredient(dish, "Соус")
    assert updated is not dish
    assert tuple(x.name for x in updated.ingredients) == ("Паста",)
    assert len(dish.ingredients) == 2


def test_remove_missing_ingredient_fails(dish: Dish) -> None:
    with pytest.raises(ValueError, match="не знайдено"):
        remove_ingredient(dish, "Базилік")


def test_add_allergen_does_not_mutate_original(dish: Dish) -> None:
    changed = add_allergen(dish, "молоко")
    assert changed.allergens == frozenset({"глютен", "молоко"})
    assert dish.allergens == frozenset({"глютен"})


def test_with_price_validates_and_copies(dish: Dish) -> None:
    changed = with_price(dish, 189.0)
    assert changed is not dish and changed.price == 189.0
    with pytest.raises(ValueError):
        with_price(dish, -1.0)


def test_metadata_is_read_only(dish: Dish) -> None:
    with pytest.raises(TypeError):
        dish.meta["category"] = "десерт"  # type: ignore[index]


def test_metadata_is_copied_on_construction() -> None:
    source = {"category": "салат"}
    dish = Dish(13, "Салат", 100.0, (), frozenset(), source)
    source["category"] = "десерт"
    assert dish.meta["category"] == "салат"


def test_filter_by_allergen() -> None:
    result = filter_by_allergen(get_sample_menu(), "молоко")
    assert {dish.dish_id for dish in result} == {1, 3}


def test_models_are_frozen(dish: Dish) -> None:
    with pytest.raises((AttributeError, TypeError)):
        dish.price = 200.0  # type: ignore[misc]


def test_ingredient_is_hashable() -> None:
    ingredient = Ingredient("Паста", 120.0)
    assert ingredient in {ingredient}


def test_dish_hash_is_unavailable_due_to_mappingproxy(dish: Dish) -> None:
    # Dish містить MappingProxyType, тому dataclass не може створити хеш.
    with pytest.raises(TypeError):
        hash(dish)


def test_discount_is_a_pure_update(dish: Dish) -> None:
    reduced = discounted(dish, 10)
    assert reduced.price == 148.5
    assert dish.price == 165.0
    with pytest.raises(ValueError):
        discounted(dish, 101)


def test_freeze_recursively_copies_and_freezes() -> None:
    source = {"tags": ["гаряче"], "flags": {"new"}}
    frozen = freeze(source)
    source["tags"].append("змінено")
    assert frozen["tags"] == ("гаряче",)  # type: ignore[index]
    with pytest.raises(TypeError):
        frozen["other"] = 1  # type: ignore[index]
