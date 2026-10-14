"""Упражнения с проверкой в Docker: определения задач.

Ключ — глава книги «Изучаем Python» (book 13). Режимы проверки:
- stdout: программа запускается, сравнивается построчный вывод;
- func: из решения вызывается функция с аргументами тестов и
  сравнивается возвращённое значение.

Клиенту отдаются только statement/starter/hint — тесты остаются на бэкенде.
"""

PY_TASKS: dict[int, list[dict]] = {
    1: [
        {
            "id": "hello",
            "mode": "stdout",
            "title": "Первая строка",
            "statement": (
                "Напишите программу, которая печатает ровно одну строку: "
                "Привет, Python!"
            ),
            "starter": "# Ваша первая программа\n",
            "expected": ["Привет, Python!"],
            "hint": "Одна команда print, текст — в кавычках внутри скобок.",
        },
        {
            "id": "two-lines",
            "mode": "stdout",
            "title": "Две строки",
            "statement": (
                "Выведите две строки друг за другом: сначала «Меня зовут Python», "
                "потом «Мне 34 года»."
            ),
            "starter": "# Две команды print\n",
            "expected": ["Меня зовут Python", "Мне 34 года"],
            "hint": "Каждая строка — своя команда print; они выполняются сверху вниз.",
        },
        {
            "id": "calc",
            "mode": "stdout",
            "title": "Считает print",
            "statement": (
                "Печатайте результат умножения шести на семь — но посчитайте его "
                "прямо внутри print, а не готовым числом в кавычках."
            ),
            "starter": "# Пусть Python посчитает сам\n",
            "expected": ["42"],
            "hint": "Внутри скобок print можно написать арифметику: print(6 * 7).",
        },
        {
            "id": "repeat",
            "mode": "stdout",
            "title": "Повтор строки",
            "statement": (
                "Выведите «ляляля» — но получите эту строку умножением строки "
                "«ля» на три, а не вписыванием готового слова."
            ),
            "starter": "# Умножение строки\n",
            "expected": ["ляляля"],
            "hint": "Звёздочка повторяет строку: «ля» * 3.",
        },
        {
            "id": "repeat-big",
            "mode": "stdout",
            "title": "Повтор всерьёз",
            "statement": (
                "Выведите строку i234_34$ ровно 344 раза подряд — одной строкой, "
                "без пробелов и переносов. Умножением строки на число: вручную "
                "такое не перепечатать."
            ),
            "starter": "# Без копипасты: строка * число\n",
            "expected": ["i234_34$" * 344],
            "hint": "print('i234_34$' * 344) — звёздочка повторит строку нужное число раз.",
        },
    ],
    2: [
        {
            "id": "greet",
            "mode": "func",
            "func": "greet",
            "title": "Приветствие",
            "statement": (
                "Напишите функцию greet(name), которая возвращает строку вида "
                "«Привет, Аня!» — то есть «Привет, » + имя + восклицательный знак. "
                "Используйте f-строку."
            ),
            "starter": (
                "def greet(name):\n    # верните f-строку с именем внутри\n    pass\n"
            ),
            "tests": [
                {"args": ["Аня"], "expected": "Привет, Аня!"},
                {"args": ["Python"], "expected": "Привет, Python!"},
                {"args": ["world"], "expected": "Привет, world!"},
            ],
            "hint": 'f"Привет, {name}!" — фигурные скобки подставят значение.',
        },
        {
            "id": "area",
            "mode": "func",
            "func": "area",
            "title": "Площадь прямоугольника",
            "statement": (
                "Напишите функцию area(a, b), которая возвращает площадь "
                "прямоугольника со сторонами a и b."
            ),
            "starter": "def area(a, b):\n    pass\n",
            "tests": [
                {"args": [3, 4], "expected": 12},
                {"args": [5, 5], "expected": 25},
                {"args": [2, 10], "expected": 20},
            ],
            "hint": "Площадь — произведение сторон: return a * b.",
        },
        {
            "id": "to-celsius",
            "mode": "func",
            "func": "to_celsius",
            "title": "Фаренгейты в цельсии",
            "statement": (
                "Напишите функцию to_celsius(f), которая переводит температуру "
                "из Фаренгейтов в Цельсии по формуле (f - 32) * 5 / 9 и "
                "возвращает результат."
            ),
            "starter": "def to_celsius(f):\n    pass\n",
            "tests": [
                {"args": [32], "expected": 0.0},
                {"args": [212], "expected": 100.0},
                {"args": [50], "expected": 10.0},
            ],
            "hint": "Формула уже в условии: return (f - 32) * 5 / 9. В Python скобки задают порядок.",
        },
    ],
    3: [
        {
            "id": "sign",
            "mode": "func",
            "func": "sign",
            "title": "Знак числа",
            "statement": (
                "Напишите функцию sign(x), которая возвращает слово "
                "«положительное» для x > 0, «отрицательное» для x < 0 и "
                "«ноль» для x = 0."
            ),
            "starter": (
                "def sign(x):\n    # if / elif / else — три дороги\n    pass\n"
            ),
            "tests": [
                {"args": [5], "expected": "положительное"},
                {"args": [-3], "expected": "отрицательное"},
                {"args": [0], "expected": "ноль"},
                {"args": [100], "expected": "положительное"},
            ],
            "hint": "Три ветки: if x > 0: ... elif x < 0: ... else: ...",
        },
        {
            "id": "is-even",
            "mode": "func",
            "func": "is_even",
            "title": "Чётное ли число",
            "statement": (
                "Напишите функцию is_even(n), которая возвращает True, если n "
                "чётное, и False — если нечётное. Подсказка: остаток от деления "
                "— оператор %."
            ),
            "starter": "def is_even(n):\n    pass\n",
            "tests": [
                {"args": [4], "expected": True},
                {"args": [7], "expected": False},
                {"args": [0], "expected": True},
                {"args": [13], "expected": False},
            ],
            "hint": "Сравнение само даёт bool: return n % 2 == 0.",
        },
        {
            "id": "max2",
            "mode": "func",
            "func": "max2",
            "title": "Максимум из двух",
            "statement": (
                "Напишите функцию max2(a, b), которая возвращает большее из "
                "двух чисел. Встроенную функцию max() использовать нельзя — "
                "только if и else."
            ),
            "starter": "def max2(a, b):\n    pass\n",
            "tests": [
                {"args": [3, 7], "expected": 7},
                {"args": [10, 2], "expected": 10},
                {"args": [5, 5], "expected": 5},
                {"args": [-1, -9], "expected": -1},
            ],
            "hint": "if a > b: вернуть a, иначе — вернуть b. Равные числа: подойдёт любая ветка else.",
        },
        {
            "id": "ticket-price",
            "mode": "func",
            "func": "ticket_price",
            "title": "Цена билета",
            "statement": (
                "Кинотеатр ставит цену по возрасту: до 7 лет включительно — 0, "
                "от 8 до 17 включительно — 200, от 18 и старше — 400. Напишите "
                "функцию ticket_price(age), возвращающую цену."
            ),
            "starter": (
                "def ticket_price(age):\n    # цепочка if / elif / else\n    pass\n"
            ),
            "tests": [
                {"args": [3], "expected": 0},
                {"args": [7], "expected": 0},
                {"args": [8], "expected": 200},
                {"args": [17], "expected": 200},
                {"args": [18], "expected": 400},
                {"args": [65], "expected": 400},
            ],
            "hint": "Проверяйте сверху вниз от младших: if age <= 7 ... elif age <= 17 ... else ...",
        },
    ],
}


def chapter_tasks(book_id: int, chapter: int) -> list[dict] | None:
    """Публичные определения задач (без тестов) для клиента."""
    if book_id != 13:
        return None
    tasks = PY_TASKS.get(chapter)
    if not tasks:
        return None
    return [
        {k: t[k] for k in ("id", "mode", "title", "statement", "starter", "hint")}
        for t in tasks
    ]


def find_task(book_id: int, chapter: int, task_id: str) -> dict | None:
    if book_id != 13:
        return None
    for t in PY_TASKS.get(chapter, []):
        if t["id"] == task_id:
            return t
    return None
