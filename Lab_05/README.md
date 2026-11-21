# Лабораторна робота №5

## Ліниві обчислення: генератори та itertools

Варіант 12 присвячено потоку трикутних чисел. Послідовність утворюється як префіксні суми нескінченного потоку натуральних чисел: `1, 3, 6, 10, ...`. Результати обмежуються заданою межею, а різниці сусідніх чисел обчислюються через ковзне вікно розміру 2.

## Структура проєкту

```text
Lab_05/
├── core.py
├── main.py
├── streams.py
├── mypy.ini
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
├── report/
│   ├── lab5.pdf
│   ├── build_report.py
│   └── screenshots/
│       ├── core.png
│       ├── main.png
│       ├── streams.png
│       └── tests_triangular.png
└── tests/
    ├── __init__.py
    ├── test_accumulate.py
    ├── test_sliding_window.py
    ├── test_take_drop.py
    └── test_triangular_stream.py
```

## Запуск

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest -q
python main.py
```

## Лінивість і обмеження

`triangular_numbers()` використовує `yield from accumulate(count(1))`, тому не зберігає повну послідовність. `triangular_numbers_up_to(limit)` зупиняє читання через `takewhile`, а `take` та `drop` обмежують кількість запитаних елементів. `sliding_window` зберігає лише поточне вікно в `deque(maxlen=k)`. Нескінченні джерела в демонстрації обмежуються `take`.

Тести перевіряють правильність перших значень, обмеження потоку, поведінку `take`/`drop`, межі розміру вікна, порожні джерела та кількість значень, фактично прочитаних лінивим ітератором.
