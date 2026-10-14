"""Задачи «Изучаем Python»: раздел «Основы» (главы 1–4)."""

TASKS: dict[int, list[dict]] = {
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
    4: [
        {
            "id": "hello-twice",
            "mode": "stdout",
            "title": "Своя функция",
            "statement": (
                "Опишите функцию hello(name), которая печатает «Привет, <имя>!», "
                "и вызовите её дважды: для «Аня» и для «Борис»."
            ),
            "starter": "# def hello(name): ...\n# два вызова\n",
            "expected": ["Привет, Аня!", "Привет, Борис!"],
            "hint": 'def hello(name): print(f"Привет, {name}!") — а ниже hello("Аня") и hello("Борис").',
        },
        {
            "id": "average3",
            "mode": "func",
            "func": "average3",
            "title": "Среднее трёх",
            "statement": (
                "Напишите функцию average3(a, b, c): среднее арифметическое "
                "трёх чисел. Функция должна вернуть результат, а не печатать его."
            ),
            "starter": "def average3(a, b, c):\n    pass\n",
            "tests": [
                {"args": [1, 2, 3], "expected": 2.0},
                {"args": [10, 20, 30], "expected": 20.0},
                {"args": [0, 0, 1], "expected": 1 / 3},
                {"args": [-3, 3, 0], "expected": 0.0},
            ],
            "hint": "return (a + b + c) / 3 — именно return, а не print.",
        },
        {
            "id": "clamp",
            "mode": "func",
            "func": "clamp",
            "title": "Ограничить число",
            "statement": (
                "Напишите функцию clamp(x, low, high): если x меньше low — "
                "верните low, если больше high — high, иначе сам x."
            ),
            "starter": "def clamp(x, low, high):\n    pass\n",
            "tests": [
                {"args": [5, 0, 10], "expected": 5},
                {"args": [-3, 0, 10], "expected": 0},
                {"args": [42, 0, 10], "expected": 10},
                {"args": [10, 0, 10], "expected": 10},
            ],
            "hint": "Два ранних выхода: if x < low: return low; if x > high: return high; затем return x.",
        },
        {
            "id": "power-default",
            "mode": "func",
            "func": "power",
            "title": "Степень с умолчанием",
            "statement": (
                "Напишите функцию power(x, n=2): x в степени n. Если n не "
                "передали, возводим в квадрат."
            ),
            "starter": "def power(x, n=2):\n    pass\n",
            "tests": [
                {"args": [5], "expected": 25},
                {"args": [2, 10], "expected": 1024},
                {"args": [3, 0], "expected": 1},
                {"args": [-2, 3], "expected": -8},
            ],
            "hint": "return x ** n — значение по умолчанию уже стоит в заголовке.",
        },
        {
            "id": "is-leap",
            "mode": "func",
            "func": "is_leap",
            "title": "Високосный год",
            "statement": (
                "Напишите функцию is_leap(year): True для високосного года. "
                "Год високосный, если он делится на 4, кроме годов, которые "
                "делятся на 100, но не делятся на 400."
            ),
            "starter": "def is_leap(year):\n    pass\n",
            "tests": [
                {"args": [2024], "expected": True},
                {"args": [2023], "expected": False},
                {"args": [1900], "expected": False},
                {"args": [2000], "expected": True},
            ],
            "hint": "return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0).",
        },
        {
            "id": "fizzbuzz",
            "mode": "func",
            "func": "fizzbuzz",
            "title": "Физзбазз",
            "statement": (
                "Напишите функцию fizzbuzz(n): «FizzBuzz», если n делится на 3 "
                "и на 5; «Fizz», если только на 3; «Buzz», если только на 5; "
                "иначе — само число в виде строки."
            ),
            "starter": "def fizzbuzz(n):\n    pass\n",
            "tests": [
                {"args": [15], "expected": "FizzBuzz"},
                {"args": [9], "expected": "Fizz"},
                {"args": [10], "expected": "Buzz"},
                {"args": [7], "expected": "7"},
            ],
            "hint": "Сначала самый строгий случай (оба), потом по одному; в конце return str(n).",
        },
        {
            "id": "triangle-kind",
            "mode": "func",
            "func": "triangle_kind",
            "title": "Вид треугольника",
            "statement": (
                "Напишите функцию triangle_kind(a, b, c): «равносторонний», "
                "если все три стороны равны, «равнобедренный», если равны "
                "ровно две, иначе «разносторонний»."
            ),
            "starter": "def triangle_kind(a, b, c):\n    pass\n",
            "tests": [
                {"args": [3, 3, 3], "expected": "равносторонний"},
                {"args": [3, 3, 5], "expected": "равнобедренный"},
                {"args": [3, 5, 3], "expected": "равнобедренный"},
                {"args": [3, 4, 5], "expected": "разносторонний"},
            ],
            "hint": "Сначала проверьте a == b == c, затем «хоть одна пара равна»: a == b or b == c or a == c.",
        },
        {
            "id": "factorial-rec",
            "mode": "func",
            "func": "fact",
            "title": "Факториал рекурсией",
            "statement": (
                "Напишите функцию fact(n): факториал n, но через рекурсию — "
                "функция должна вызывать саму себя. Базовый случай: "
                "fact(0) = 1."
            ),
            "starter": "def fact(n):\n    pass\n",
            "tests": [
                {"args": [0], "expected": 1},
                {"args": [1], "expected": 1},
                {"args": [5], "expected": 120},
                {"args": [8], "expected": 40320},
            ],
            "hint": "if n == 0: return 1; иначе return n * fact(n - 1).",
        },
    ],
}
