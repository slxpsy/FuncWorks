# Лабораторна робота №3

## Опис

Незмінна модель ресторанного меню (варіант 12). Для позицій `Dish` та складників `Ingredient` застосовано `dataclass(frozen=True, slots=True)`, кортежі `tuple`, множини алергенів `frozenset` і метадані лише для читання через `MappingProxyType` із копіюванням джерела.

Оновлення страви реалізовано як чисті функції, що повертають нові об'єкти: додавання/видалення інгредієнта, додавання алергену, зміна ціни та застосування знижки. Додатково реалізовано рекурсивну функцію `freeze` та фільтрацію меню за алергеном.

## Структура проєкту

```text
Lab_03/
├── app.py
├── benchmark.py
├── core.py
├── main.py
├── model.py
├── mypy.ini
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
├── report/
│   ├── lab3.pdf
│   └── screenshots/
└── tests/
    ├── __init__.py
    └── test_core.py
```

## Запуск

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
python main.py --allergen молоко
python -m pytest -q --durations=5
python benchmark.py
```

## Перевірки стилю та типів

```powershell
black --check .
ruff check .
mypy .
```

## Результат

Початкова страва не змінюється: кожна операція повертає новий екземпляр `Dish`. `Ingredient` хешується, бо містить лише незмінні поля. `Dish` не хешується через поле `MappingProxyType`; це обмеження явно перевіряється тестом. Невелика вартість копіювання колекцій під час оновлення компенсується передбачуваністю стану й простішим тестуванням.
