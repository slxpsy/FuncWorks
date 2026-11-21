from __future__ import annotations

from model import Dish, Ingredient, make_meta


def get_sample_menu() -> tuple[Dish, ...]:
    """Повертає приклад меню ресторану для демонстрації."""

    return (
        Dish(1, "Паста з соусом", 165.0,
             (Ingredient("Паста", 120.0), Ingredient("Соус", 80.0)),
             frozenset({"глютен", "молоко"}),
             make_meta(category="основна страва", kitchen="гаряча кухня")),
        Dish(2, "Овочевий салат", 120.0,
             (Ingredient("Томат", 90.0), Ingredient("Огірок", 70.0)),
             frozenset(), make_meta(category="салат", kitchen="холодна кухня")),
        Dish(3, "Мигдалевий десерт", 95.0,
             (Ingredient("Мигдаль", 40.0), Ingredient("Вершки", 60.0)),
             frozenset({"горіхи", "молоко"}),
             make_meta(category="десерт", kitchen="кондитерська")),
    )


def render_menu(dishes: tuple[Dish, ...]) -> str:
    lines = ["Меню ресторану", "=" * 15]
    for dish in dishes:
        allergens = ", ".join(sorted(dish.allergens)) or "немає"
        lines.append(f"{dish.name} — {dish.price:.2f} грн | алергени: {allergens}")
    return "\n".join(lines)
