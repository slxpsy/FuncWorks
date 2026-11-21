from __future__ import annotations

import argparse

from app import get_sample_menu, render_menu
from core import filter_by_allergen


def main() -> None:
    parser = argparse.ArgumentParser(description="Перегляд незмінного меню ресторану")
    parser.add_argument("--allergen", help="показати страви з указаним алергеном")
    args = parser.parse_args()
    menu = get_sample_menu()
    if args.allergen:
        menu = filter_by_allergen(menu, args.allergen)
    print(render_menu(menu))


if __name__ == "__main__":
    main()
