"""Задачи «Python как первый язык»: итераторы и генераторы (главы 18–19).

Итераторы и генераторы нельзя передать через JSON-тесты, поэтому проверка идёт
скрытым драйвером: он вызывает функции ученика и печатает результат.
"""

TASKS: dict[int, list[dict]] = {
    18: [
        {
            "id": "countdown-iterator",
            "mode": "stdout",
            "title": "Итератор-отсчёт",
            "statement": (
                "Опишите класс Countdown(n): итератор (методы __iter__ и "
                "__next__), который выдаёт числа от n до 1 и затем "
                "останавливается (StopIteration). Для n = 0 — сразу пусто."
            ),
            "starter": "class Countdown:\n    def __init__(self, n):\n        pass\n",
            "driver": (
                "print(list(Countdown(3)))\nprint(list(Countdown(0)))\n"
                "c = Countdown(2)\nprint(list(c), list(c))\n"
                "for x in Countdown(2):\n    print(x)\n"
            ),
            "expected": ["[3, 2, 1]", "[]", "[2, 1] []", "2", "1"],
            "hint": "__iter__ возвращает self; в __next__: если self.n <= 0 — raise StopIteration, иначе уменьшить и вернуть прежнее.",
        },
        {
            "id": "repeater-iterable",
            "mode": "stdout",
            "title": "Многоразовый итерируемый",
            "statement": (
                "Опишите класс Repeater(word, times): его можно перебирать "
                "много раз, и каждый раз он выдаёт слово word ровно times раз. "
                "__iter__ должен каждый раз возвращать НОВЫЙ итератор."
            ),
            "starter": "class Repeater:\n    def __init__(self, word, times):\n        pass\n",
            "driver": (
                'r = Repeater("а", 3)\nprint(list(r))\nprint(list(r))\n'
                "print(len(list(Repeater('б', 0))))\n"
            ),
            "expected": ["['а', 'а', 'а']", "['а', 'а', 'а']", "0"],
            "hint": "def __iter__(self): return iter([self.word] * self.times) — каждый вызов строит новый итератор.",
        },
        {
            "id": "take-n",
            "mode": "stdout",
            "title": "Взять первые n",
            "statement": (
                "Напишите функцию take(iterator, n): список из первых n "
                "элементов итератора (или меньше, если элементов не хватило). "
                "Используйте next с запасным значением или цикл по итератору."
            ),
            "starter": "def take(iterator, n):\n    pass\n",
            "driver": (
                "print(take(iter(range(10)), 3))\nprint(take(iter([1]), 5))\n"
                "it = iter('abcdef')\nprint(take(it, 2), take(it, 2))\nprint(take(iter([]), 3))\n"
            ),
            "expected": ["[0, 1, 2]", "[1]", "['a', 'b'] ['c', 'd']", "[]"],
            "hint": "n раз пробуйте next(iterator) внутри try; на StopIteration выходите из цикла.",
        },
        {
            "id": "first-even",
            "mode": "func",
            "func": "first_even",
            "title": "Первое чётное",
            "statement": (
                "Напишите функцию first_even(nums): первое чётное число в "
                "списке или None. Используйте next со значением по умолчанию "
                "и генераторное выражение — без цикла и без индексов."
            ),
            "starter": "def first_even(nums):\n    pass\n",
            "tests": [
                {"args": [[1, 3, 4, 6]], "expected": 4},
                {"args": [[1, 3, 5]], "expected": None},
                {"args": [[]], "expected": None},
                {"args": [[2]], "expected": 2},
            ],
            "hint": "next((x for x in nums if x % 2 == 0), None).",
        },
        {
            "id": "fib-iterator",
            "mode": "stdout",
            "title": "Бесконечный итератор Фибоначчи",
            "statement": (
                "Опишите класс Fib: бесконечный итератор, который выдаёт "
                "числа Фибоначчи 1, 1, 2, 3, 5, 8, …"
            ),
            "starter": "class Fib:\n    def __init__(self):\n        pass\n",
            "driver": (
                "res = []\nfor i, x in enumerate(Fib()):\n    if i == 10:\n        break\n    res.append(x)\nprint(res)\n"
                "it = iter(Fib())\nprint(next(it), next(it), next(it))\n"
            ),
            "expected": ["[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]", "1 1 2"],
            "hint": "Храните два числа a, b; в __next__: a, b = b, a + b; return a (стартуйте с a=0, b=1).",
        },
        {
            "id": "evens-iterator",
            "mode": "stdout",
            "title": "Чётные до предела",
            "statement": (
                "Опишите класс Evens(limit): итератор чётных неотрицательных "
                "чисел 0, 2, 4, … строго меньше limit."
            ),
            "starter": "class Evens:\n    def __init__(self, limit):\n        pass\n",
            "driver": "print(list(Evens(9)))\nprint(list(Evens(1)))\nprint(list(Evens(0)))\nprint(sum(Evens(11)))\n",
            "expected": ["[0, 2, 4, 6, 8]", "[0]", "[]", "30"],
            "hint": "Храните текущее число; в __next__: если оно >= limit — StopIteration, иначе вернуть и прибавить 2.",
        },
        {
            "id": "count-items",
            "mode": "stdout",
            "title": "Сколько элементов",
            "statement": (
                "Напишите функцию count_items(iterable): сколько элементов "
                "выдаёт любой итерируемый объект (список, рэндж, генератор, "
                "файл). len использовать нельзя — работайте циклом."
            ),
            "starter": "def count_items(iterable):\n    pass\n",
            "driver": (
                "print(count_items([1, 2, 3]))\nprint(count_items(range(5)))\n"
                "print(count_items(c for c in 'привет' if c != 'в'))\nprint(count_items(iter([])))\n"
            ),
            "expected": ["3", "5", "5", "0"],
            "hint": "n = 0; for _ in iterable: n += 1; return n.",
        },
    ],
    19: [
        {
            "id": "countdown-gen",
            "mode": "stdout",
            "title": "Генератор отсчёта",
            "statement": (
                "Напишите генераторную функцию countdown(n): отдаёт числа от "
                "n до 1 (для n = 0 — ничего). Используйте yield."
            ),
            "starter": "def countdown(n):\n    pass\n",
            "driver": "print(list(countdown(3)))\nprint(list(countdown(0)))\ng = countdown(2)\nprint(next(g), next(g))\n",
            "expected": ["[3, 2, 1]", "[]", "2 1"],
            "hint": "while n > 0: yield n; n -= 1.",
        },
        {
            "id": "fib-gen",
            "mode": "stdout",
            "title": "Генератор Фибоначчи",
            "statement": (
                "Напишите бесконечный генератор fib_gen(): числа Фибоначчи "
                "0, 1, 1, 2, 3, 5, …"
            ),
            "starter": "def fib_gen():\n    pass\n",
            "driver": (
                "res = []\nfor i, x in enumerate(fib_gen()):\n    if i == 10:\n        break\n    res.append(x)\nprint(res)\n"
            ),
            "expected": ["[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]"],
            "hint": "a, b = 0, 1; while True: yield a; a, b = b, a + b.",
        },
        {
            "id": "evens-gen",
            "mode": "stdout",
            "title": "Чётные до предела",
            "statement": (
                "Напишите генератор evens(limit): чётные неотрицательные "
                "числа строго меньше limit."
            ),
            "starter": "def evens(limit):\n    pass\n",
            "driver": "print(list(evens(9)))\nprint(list(evens(0)))\nprint(sum(evens(11)))\n",
            "expected": ["[0, 2, 4, 6, 8]", "[]", "30"],
            "hint": "for x in range(0, limit, 2): yield x.",
        },
        {
            "id": "chunks-gen",
            "mode": "stdout",
            "title": "Пачки",
            "statement": (
                "Напишите генератор chunks(items, n): отдаёт список по частям "
                "по n элементов (последняя может быть короче)."
            ),
            "starter": "def chunks(items, n):\n    pass\n",
            "driver": "print(list(chunks([1, 2, 3, 4, 5], 2)))\nprint(list(chunks([], 3)))\nprint(list(chunks('abcdef', 3)))\n",
            "expected": ["[[1, 2], [3, 4], [5]]", "[]", "['abc', 'def']"],
            "hint": "for i in range(0, len(items), n): yield items[i:i + n].",
        },
        {
            "id": "flatten-gen",
            "mode": "stdout",
            "title": "Выпрямить вложенные списки",
            "statement": (
                "Напишите генератор flatten(items): отдаёт все не-списковые "
                "элементы произвольно вложенных списков по порядку. Используйте "
                "yield from и рекурсию."
            ),
            "starter": "def flatten(items):\n    pass\n",
            "driver": "print(list(flatten([1, [2, [3, [4]], 5], [], 6])))\nprint(list(flatten([])))\nprint(list(flatten([[['а']]])))\n",
            "expected": ["[1, 2, 3, 4, 5, 6]", "[]", "['а']"],
            "hint": "if isinstance(x, list): yield from flatten(x); else: yield x.",
        },
        {
            "id": "read-numbers",
            "mode": "stdout",
            "title": "Числа из строк",
            "statement": (
                "Напишите генератор read_numbers(lines): из последовательности "
                "строк отдаёт целые числа. Пустые строки и строки, которые "
                "не являются числом (после strip состоят не только из цифр), "
                "пропускаются."
            ),
            "starter": "def read_numbers(lines):\n    pass\n",
            "driver": (
                "print(list(read_numbers(['1', '', ' 2 ', 'x', '3', '4a'])))\n"
                "g = read_numbers(iter(['10', '20']))\nprint(next(g), next(g))\n"
            ),
            "expected": ["[1, 2, 3]", "10 20"],
            "hint": "s = line.strip(); if s.isdigit(): yield int(s).",
        },
        {
            "id": "running-sum",
            "mode": "stdout",
            "title": "Накопленные суммы",
            "statement": (
                "Напишите генератор running_sum(nums): после каждого "
                "элемента отдаёт сумму всех элементов до него включительно: "
                "для 1, 2, 3, 4 — 1, 3, 6, 10."
            ),
            "starter": "def running_sum(nums):\n    pass\n",
            "driver": "print(list(running_sum([1, 2, 3, 4])))\nprint(list(running_sum([])))\nprint(list(running_sum(range(1, 6))))\n",
            "expected": ["[1, 3, 6, 10]", "[]", "[1, 3, 6, 10, 15]"],
            "hint": "total = 0; for x in nums: total += x; yield total.",
        },
        {
            "id": "tag-manager",
            "mode": "stdout",
            "title": "Свой менеджер контекста",
            "statement": (
                "С помощью декоратора contextmanager из contextlib опишите "
                "менеджер tag(name): при входе печатает «<name>», при выходе "
                "(даже при ошибке) — «</name>»."
            ),
            "starter": "from contextlib import contextmanager\n\n\ndef tag(name):\n    pass\n",
            "driver": (
                "with tag('p'):\n    print('текст')\n"
                "try:\n    with tag('b'):\n        raise ValueError('сбой')\nexcept ValueError:\n    print('поймали')\n"
            ),
            "expected": ["<p>", "текст", "</p>", "<b>", "</b>", "поймали"],
            "hint": "@contextmanager; print вход; try: yield; finally: print выход.",
        },
    ],
}
