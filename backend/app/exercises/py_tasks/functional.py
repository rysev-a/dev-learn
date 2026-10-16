"""Задачи «Python как первый язык»: функциональное программирование (главы 20–23).

Функции, замыкания и декораторы нельзя передать через JSON-тесты, поэтому
многие задачи проверяются скрытым драйвером.
"""

TASKS: dict[int, list[dict]] = {
    25: [
        {
            "id": "apply-all",
            "mode": "stdout",
            "title": "Применить все функции",
            "statement": (
                "Напишите функцию apply_all(funcs, x): список результатов "
                "вызова каждой функции из funcs от x, в том же порядке."
            ),
            "starter": "def apply_all(funcs, x):\n    pass\n",
            "driver": (
                "print(apply_all([abs, float, str], -3))\nprint(apply_all([], 5))\n"
                "print(apply_all([str.upper, str.title, len], 'привет мир'))\n"
            ),
            "expected": ["[3, -3.0, '-3']", "[]", "['ПРИВЕТ МИР', 'Привет Мир', 10]"],
            "hint": "Функции — обычные значения: [f(x) for f in funcs].",
        },
        {
            "id": "sort-length-desc",
            "mode": "func",
            "func": "by_length_desc",
            "title": "Самые длинные вперёд",
            "statement": (
                "Напишите функцию by_length_desc(words): слова от самых "
                "длинных к самым коротким; слова одной длины остаются в "
                "исходном порядке. Используйте sorted и lambda."
            ),
            "starter": "def by_length_desc(words):\n    pass\n",
            "tests": [
                {"args": [["bb", "a", "ccc"]], "expected": ["ccc", "bb", "a"]},
                {"args": [["aa", "b", "cc"]], "expected": ["aa", "cc", "b"]},
                {"args": [[]], "expected": []},
            ],
            "hint": "sorted(words, key=lambda w: len(w), reverse=True) — сортировка устойчива и с reverse.",
        },
        {
            "id": "oldest-user",
            "mode": "func",
            "func": "oldest",
            "title": "Самый старший",
            "statement": (
                "Напишите функцию oldest(users): users — список словарей "
                "{'name': ..., 'age': ...}. Верните имя самого старшего. "
                "Список не пустой. Используйте max с параметром key."
            ),
            "starter": "def oldest(users):\n    pass\n",
            "tests": [
                {"args": [[{"name": "Аня", "age": 31}, {"name": "Боря", "age": 25}]], "expected": "Аня"},
                {"args": [[{"name": "Вера", "age": 5}]], "expected": "Вера"},
                {"args": [[{"name": "А", "age": 20}, {"name": "Б", "age": 40}, {"name": "В", "age": 30}]], "expected": "Б"},
            ],
            "hint": "max(users, key=lambda u: u['age'])['name'].",
        },
        {
            "id": "even-squares-map",
            "mode": "func",
            "func": "even_squares",
            "title": "map и filter",
            "statement": (
                "Напишите функцию even_squares(nums): СПИСОК квадратов чётных "
                "чисел, в исходном порядке. Решите через filter и map (с "
                "lambda), а затем оберните результат в list."
            ),
            "starter": "def even_squares(nums):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3, 4]], "expected": [4, 16]},
                {"args": [[1, 3]], "expected": []},
                {"args": [[]], "expected": []},
                {"args": [[0, -2, 5]], "expected": [0, 4]},
            ],
            "hint": "list(map(lambda x: x * x, filter(lambda x: x % 2 == 0, nums))).",
        },
        {
            "id": "compose-fn",
            "mode": "stdout",
            "title": "Композиция функций",
            "statement": (
                "Напишите функцию compose(f, g): возвращает новую функцию, "
                "которая сначала применяет g, затем f к результату: "
                "compose(f, g)(x) == f(g(x))."
            ),
            "starter": "def compose(f, g):\n    pass\n",
            "driver": (
                "clean = compose(str.strip, str.lower)\nprint(repr(clean('  АБВ ')))\n"
                "inc_then_double = compose(lambda x: x * 2, lambda x: x + 1)\nprint(inc_then_double(5))\n"
                "print(compose(len, str)(12345))\n"
            ),
            "expected": ["'абв'", "12", "5"],
            "hint": "return lambda x: f(g(x)).",
        },
        {
            "id": "count-args",
            "mode": "stdout",
            "title": "Сколько аргументов",
            "statement": (
                "Напишите функцию describe(*args, **kwargs): возвращает "
                "строку вида «2 позиционных, 1 именованных» — сколько "
                "позиционных и сколько именованных аргументов получено."
            ),
            "starter": "def describe(*args, **kwargs):\n    pass\n",
            "driver": (
                "print(describe(1, 2, a=3))\nprint(describe())\nprint(describe('x', 'y', 'z'))\n"
                "print(describe(k=1, m=2))\nprint(describe(*[1, 2, 3], **{'q': 1}))\n"
            ),
            "expected": [
                "2 позиционных, 1 именованных",
                "0 позиционных, 0 именованных",
                "3 позиционных, 0 именованных",
                "0 позиционных, 2 именованных",
                "3 позиционных, 1 именованных",
            ],
            "hint": 'return f"{len(args)} позиционных, {len(kwargs)} именованных".',
        },
        {
            "id": "pure-append",
            "mode": "stdout",
            "title": "Чистое добавление",
            "statement": (
                "Напишите чистую функцию pure_append(items, x): возвращает "
                "НОВЫЙ список с добавленным x, не меняя исходный."
            ),
            "starter": "def pure_append(items, x):\n    pass\n",
            "driver": (
                "a = [1, 2]\nb = pure_append(a, 3)\nprint(a, b)\nprint(a is b)\n"
                "print(pure_append([], 'x'))\n"
            ),
            "expected": ["[1, 2] [1, 2, 3]", "False", "['x']"],
            "hint": "return items + [x] — оператор плюс создаёт новый список.",
        },
        {
            "id": "product-reduce",
            "mode": "func",
            "func": "product",
            "title": "Произведение через reduce",
            "statement": (
                "Напишите функцию product(nums): произведение всех чисел "
                "списка, для пустого списка — 1. Используйте reduce из "
                "functools с начальным значением."
            ),
            "starter": "from functools import reduce\n\n\ndef product(nums):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3, 4]], "expected": 24},
                {"args": [[]], "expected": 1},
                {"args": [[5]], "expected": 5},
                {"args": [[2, -3]], "expected": -6},
            ],
            "hint": "reduce(lambda acc, x: acc * x, nums, 1) — единица как начальное значение даёт 1 для пустого списка.",
        },
    ],
    26: [
        {
            "id": "make-multiplier",
            "mode": "stdout",
            "title": "Фабрика умножителей",
            "statement": (
                "Напишите функцию make_multiplier(n): возвращает функцию, "
                "умножающую свой аргумент на n."
            ),
            "starter": "def make_multiplier(n):\n    pass\n",
            "driver": (
                "triple = make_multiplier(3)\nfive = make_multiplier(5)\nprint(triple(10), five(10), triple(0))\n"
                "print(make_multiplier(-1)(7))\n"
            ),
            "expected": ["30 50 0", "-7"],
            "hint": "Опишите внутри def mul(x): return x * n и верните mul.",
        },
        {
            "id": "make-counter",
            "mode": "stdout",
            "title": "Счётчик с состоянием",
            "statement": (
                "Напишите функцию make_counter(start=0): возвращает функцию, "
                "каждый вызов которой возвращает следующее число, начиная с "
                "start + 1. Состояние хранится в замыкании (nonlocal); у "
                "каждого счётчика своё."
            ),
            "starter": "def make_counter(start=0):\n    pass\n",
            "driver": (
                "a = make_counter()\nb = make_counter(10)\nprint(a(), a(), a())\nprint(b(), b())\nprint(a())\n"
            ),
            "expected": ["1 2 3", "11 12", "4"],
            "hint": "count = start; внутри inner: nonlocal count; count += 1; return count.",
        },
        {
            "id": "make-accumulator",
            "mode": "stdout",
            "title": "Накопитель",
            "statement": (
                "Напишите функцию make_accumulator(): возвращает функцию, "
                "которая принимает число, прибавляет его к накопленной сумме "
                "(в замыкании) и возвращает текущую сумму."
            ),
            "starter": "def make_accumulator():\n    pass\n",
            "driver": (
                "acc = make_accumulator()\nprint(acc(10), acc(5), acc(-3))\nother = make_accumulator()\nprint(other(1), acc(0))\n"
            ),
            "expected": ["10 15 12", "1 12"],
            "hint": "total = 0 во внешней функции; nonlocal total во внутренней.",
        },
        {
            "id": "count-calls-deco",
            "mode": "stdout",
            "title": "Декоратор-счётчик вызовов",
            "statement": (
                "Напишите декоратор count_calls: после каждого вызова "
                "декорированной функции атрибут wrapper.calls увеличивается "
                "на единицу (начиная с 0). Результат и аргументы функции "
                "должны сохраняться."
            ),
            "starter": "def count_calls(func):\n    pass\n",
            "driver": (
                "@count_calls\ndef add(a, b=0):\n    return a + b\n\n"
                "print(add.calls)\nprint(add(1, b=2), add(5))\nprint(add.calls)\n"
            ),
            "expected": ["0", "3 5", "2"],
            "hint": "Заведите wrapper.calls = 0 после описания wrapper; внутри wrapper: wrapper.calls += 1.",
        },
        {
            "id": "logged-deco",
            "mode": "stdout",
            "title": "Декоратор с журналом",
            "statement": (
                "Напишите декоратор logged: перед каждым вызовом печатает "
                "«вызов <имя функции>», затем вызывает функцию и возвращает "
                "её результат. Имя и докстринг функции должны сохраняться "
                "(functools.wraps)."
            ),
            "starter": "from functools import wraps\n\n\ndef logged(func):\n    pass\n",
            "driver": (
                "@logged\ndef greet(name):\n    \"\"\"Поздороваться.\"\"\"\n    return f'Привет, {name}!'\n\n"
                "print(greet('Аня'))\nprint(greet.__name__, greet.__doc__)\n"
            ),
            "expected": ["вызов greet", "Привет, Аня!", "greet Поздороваться."],
            "hint": "@wraps(func) над wrapper(*args, **kwargs); print(f'вызов {func.__name__}'); return func(*args, **kwargs).",
        },
        {
            "id": "repeat-deco",
            "mode": "stdout",
            "title": "Декоратор с параметром",
            "statement": (
                "Напишите декоратор repeat(times): вызывает функцию times "
                "раз подряд и возвращает результат последнего вызова."
            ),
            "starter": "def repeat(times):\n    pass\n",
            "driver": (
                "@repeat(3)\ndef hello(name):\n    print('привет,', name)\n    return name.upper()\n\n"
                "print(hello('аня'))\n"
            ),
            "expected": ["привет, аня", "привет, аня", "привет, аня", "АНЯ"],
            "hint": "Три уровня: repeat(times) -> decorator(func) -> wrapper(*args, **kwargs).",
        },
        {
            "id": "memoize-deco",
            "mode": "stdout",
            "title": "Кеширование",
            "statement": (
                "Напишите декоратор memoize: запоминает результаты функции "
                "одного аргумента в словаре; повторный вызов с тем же "
                "аргументом не вызывает функцию заново."
            ),
            "starter": "def memoize(func):\n    pass\n",
            "driver": (
                "calls = []\n\n@memoize\ndef slow(n):\n    calls.append(n)\n    return n * n\n\n"
                "print(slow(4), slow(4), slow(5), slow(4))\nprint(calls)\n"
            ),
            "expected": ["16 16 25 16", "[4, 5]"],
            "hint": "cache = {} в декораторе; в wrapper: if n not in cache: cache[n] = func(n); return cache[n].",
        },
        {
            "id": "positive-args-deco",
            "mode": "stdout",
            "title": "Только положительные",
            "statement": (
                "Напишите декоратор positive_only: если хотя бы один "
                "позиционный аргумент меньше нуля, поднимает ValueError, "
                "иначе вызывает функцию и возвращает результат."
            ),
            "starter": "def positive_only(func):\n    pass\n",
            "driver": (
                "@positive_only\ndef total(*nums):\n    return sum(nums)\n\n"
                "print(total(1, 2, 3))\n"
                "try:\n    total(1, -2)\nexcept ValueError:\n    print('отрицательное')\n"
                "print(total())\n"
            ),
            "expected": ["6", "отрицательное", "0"],
            "hint": "В wrapper: for a in args: if a < 0: raise ValueError(...).",
        },
    ],
    27: [
        {
            "id": "merge-dicts-reduce",
            "mode": "func",
            "func": "merge_all",
            "title": "Слить много словарей",
            "statement": (
                "Напишите функцию merge_all(dicts): сливает список словарей "
                "в один; при совпадении ключей побеждает словарь, который "
                "стоит позже в списке. Используйте reduce (начальное "
                "значение — пустой словарь)."
            ),
            "starter": "from functools import reduce\n\n\ndef merge_all(dicts):\n    pass\n",
            "tests": [
                {"args": [[{"a": 1}, {"b": 2}, {"a": 3}]], "expected": {"a": 3, "b": 2}},
                {"args": [[]], "expected": {}},
                {"args": [[{"x": 1}]], "expected": {"x": 1}},
            ],
            "hint": "reduce(lambda acc, d: {**acc, **d}, dicts, {}).",
        },
        {
            "id": "int-parser-partial",
            "mode": "stdout",
            "title": "Парсер чисел",
            "statement": (
                "Напишите функцию int_parser(base): возвращает функцию, "
                "которая переводит строку в целое по основанию base. "
                "Используйте functools.partial."
            ),
            "starter": "from functools import partial\n\n\ndef int_parser(base):\n    pass\n",
            "driver": (
                "from_bin = int_parser(2)\nfrom_hex = int_parser(16)\n"
                "print(from_bin('1010'), from_hex('ff'), from_hex('10'))\n"
                "print(list(map(int_parser(8), ['7', '10', '17'])))\n"
            ),
            "expected": ["10 255 16", "[7, 8, 15]"],
            "hint": "return partial(int, base=base).",
        },
        {
            "id": "fib-cache",
            "mode": "func",
            "func": "fib",
            "title": "Быстрый Фибоначчи",
            "statement": (
                "Напишите рекурсивную функцию fib(n): n-е число Фибоначчи "
                "(fib(0) = 0, fib(1) = 1). Без кеша она не уложится во "
                "время на больших n — добавьте декоратор lru_cache."
            ),
            "starter": "from functools import lru_cache\n\n\ndef fib(n):\n    pass\n",
            "tests": [
                {"args": [10], "expected": 55},
                {"args": [50], "expected": 12586269025},
                {"args": [80], "expected": 23416728348467685},
                {"args": [0], "expected": 0},
            ],
            "hint": "@lru_cache(maxsize=None) над def fib(n): return n if n < 2 else fib(n - 1) + fib(n - 2).",
        },
        {
            "id": "sort-by-fields",
            "mode": "func",
            "func": "sort_people",
            "title": "Сортировка по двум полям",
            "statement": (
                "Напишите функцию sort_people(people): people — список "
                "словарей {'city': ..., 'age': ...}. Отсортируйте по городу "
                "(по алфавиту), а при равных городах — по возрасту (по "
                "возрастанию). Используйте operator.itemgetter с двумя "
                "ключами."
            ),
            "starter": "from operator import itemgetter\n\n\ndef sort_people(people):\n    pass\n",
            "tests": [
                {"args": [[{"city": "Омск", "age": 30}, {"city": "Тверь", "age": 20}, {"city": "Омск", "age": 25}]],
                 "expected": [{"city": "Омск", "age": 25}, {"city": "Омск", "age": 30}, {"city": "Тверь", "age": 20}]},
                {"args": [[]], "expected": []},
                {"args": [[{"city": "А", "age": 1}]], "expected": [{"city": "А", "age": 1}]},
            ],
            "hint": 'sorted(people, key=itemgetter("city", "age")).',
        },
        {
            "id": "total-ordering-class",
            "mode": "stdout",
            "title": "Класс с total_ordering",
            "statement": (
                "Опишите класс Card(rank) с декоратором total_ordering: "
                "определите только __eq__ и __lt__ (по рангу), а остальные "
                "сравнения (<=, >, >=) должны заработать сами."
            ),
            "starter": "from functools import total_ordering\n\n\nclass Card:\n    def __init__(self, rank):\n        self.rank = rank\n",
            "driver": (
                "a, b = Card(3), Card(7)\nprint(a < b, a <= b, a > b, a >= b, a == Card(3))\n"
                "print(max(a, b).rank, sorted([b, a, Card(5)])[1].rank)\n"
            ),
            "expected": ["True True False False True", "7 5"],
            "hint": "@total_ordering над class; __eq__: сравнить ранги; __lt__: self.rank < other.rank.",
        },
        {
            "id": "single-dispatch-describe",
            "mode": "stdout",
            "title": "Перегрузка по типу",
            "statement": (
                "Напишите функцию describe(x) на singledispatch: для int — "
                "«целое <x>», для str — «строка из <n> символов», для list — "
                "«список из <n> элементов», для остальных — «что-то»."
            ),
            "starter": "from functools import singledispatch\n\n\ndef describe(x):\n    pass\n",
            "driver": "print(describe(5))\nprint(describe('привет'))\nprint(describe([1, 2, 3]))\nprint(describe(2.5))\n",
            "expected": ["целое 5", "строка из 6 символов", "список из 3 элементов", "что-то"],
            "hint": "@singledispatch над базовой describe; @describe.register(int) def _(x): ... — и так для str и list.",
        },
        {
            "id": "cmp-to-key-sort",
            "mode": "func",
            "func": "sort_words",
            "title": "Сортировка через сравнение",
            "statement": (
                "Напишите функцию sort_words(words): сначала короткие слова, "
                "при равной длине — по алфавиту. Реализуйте через функцию "
                "сравнения двух слов и functools.cmp_to_key."
            ),
            "starter": "from functools import cmp_to_key\n\n\ndef compare(a, b):\n    pass\n\n\ndef sort_words(words):\n    pass\n",
            "tests": [
                {"args": [["bb", "a", "cc", "b"]], "expected": ["a", "b", "bb", "cc"]},
                {"args": [["ccc", "aa", "b", "aaa"]], "expected": ["b", "aa", "aaa", "ccc"]},
                {"args": [[]], "expected": []},
            ],
            "hint": "compare возвращает отрицательное, 0 или положительное число; sorted(words, key=cmp_to_key(compare)).",
        },
        {
            "id": "column-itemgetter",
            "mode": "func",
            "func": "column",
            "title": "Столбец таблицы",
            "statement": (
                "Напишите функцию column(rows, i): список значений i-го "
                "столбца таблицы (rows — список списков). Используйте map и "
                "operator.itemgetter."
            ),
            "starter": "from operator import itemgetter\n\n\ndef column(rows, i):\n    pass\n",
            "tests": [
                {"args": [[[1, 2, 3], [4, 5, 6]], 1], "expected": [2, 5]},
                {"args": [[[1, "а"], [2, "б"]], 0], "expected": [1, 2]},
                {"args": [[], 0], "expected": []},
            ],
            "hint": "list(map(itemgetter(i), rows)).",
        },
    ],
    28: [
        {
            "id": "first-squares",
            "mode": "func",
            "func": "first_squares",
            "title": "Первые квадраты",
            "statement": (
                "Напишите функцию first_squares(n): список первых n "
                "квадратов натуральных чисел: 1, 4, 9, … Используйте "
                "itertools.count и islice."
            ),
            "starter": "from itertools import count, islice\n\n\ndef first_squares(n):\n    pass\n",
            "tests": [
                {"args": [4], "expected": [1, 4, 9, 16]},
                {"args": [0], "expected": []},
                {"args": [1], "expected": [1]},
            ],
            "hint": "list(islice((x * x for x in count(1)), n)).",
        },
        {
            "id": "chain-all",
            "mode": "func",
            "func": "chain_all",
            "title": "Склеить списки",
            "statement": (
                "Напишите функцию chain_all(*lists): один список из элементов "
                "всех переданных списков по порядку. Используйте itertools.chain."
            ),
            "starter": "from itertools import chain\n\n\ndef chain_all(*lists):\n    pass\n",
            "tests": [
                {"args": [[1, 2], [3], []], "expected": [1, 2, 3]},
                {"args": [], "expected": []},
                {"args": [["а"], ["б", "в"]], "expected": ["а", "б", "в"]},
            ],
            "hint": "list(chain(*lists)) — звёздочка раскладывает аргументы дальше.",
        },
        {
            "id": "running-max",
            "mode": "func",
            "func": "running_max",
            "title": "Рекорды по ходу",
            "statement": (
                "Напишите функцию running_max(nums): список нарастающего "
                "максимума: для 3, 1, 4, 1, 5 — 3, 3, 4, 4, 5. Используйте "
                "accumulate с функцией max."
            ),
            "starter": "from itertools import accumulate\n\n\ndef running_max(nums):\n    pass\n",
            "tests": [
                {"args": [[3, 1, 4, 1, 5]], "expected": [3, 3, 4, 4, 5]},
                {"args": [[]], "expected": []},
                {"args": [[5, 4, 3]], "expected": [5, 5, 5]},
            ],
            "hint": "list(accumulate(nums, max)).",
        },
        {
            "id": "group-sizes",
            "mode": "func",
            "func": "group_sizes",
            "title": "Размеры групп",
            "statement": (
                "Напишите функцию group_sizes(words): словарь «первая буква "
                "→ сколько слов начинается с неё». Используйте groupby — "
                "помните, что данные нужно отсортировать."
            ),
            "starter": "from itertools import groupby\n\n\ndef group_sizes(words):\n    pass\n",
            "tests": [
                {"args": [["арбуз", "банан", "абрикос", "берёза", "вишня"]], "expected": {"а": 2, "б": 2, "в": 1}},
                {"args": [[]], "expected": {}},
                {"args": [["я"]], "expected": {"я": 1}},
            ],
            "hint": "for k, g in groupby(sorted(words), key=lambda w: w[0]): result[k] = len(list(g)).",
        },
        {
            "id": "all-pairs",
            "mode": "func",
            "func": "all_pairs",
            "title": "Все пары",
            "statement": (
                "Напишите функцию all_pairs(items): список всех пар разных "
                "элементов (каждая пара один раз, порядок как в списке) — "
                "кортежами. Используйте itertools.combinations."
            ),
            "starter": "from itertools import combinations\n\n\ndef all_pairs(items):\n    pass\n",
            "tests": [
                {"args": [["а", "б", "в"]], "expected": [("а", "б"), ("а", "в"), ("б", "в")]},
                {"args": [[1]], "expected": []},
                {"args": [[]], "expected": []},
            ],
            "hint": "list(combinations(items, 2)).",
        },
        {
            "id": "passwords-product",
            "mode": "func",
            "func": "passwords",
            "title": "Все пароли",
            "statement": (
                "Напишите функцию passwords(alphabet, length): список всех "
                "строк заданной длины из символов alphabet (с повторами), в "
                "лексикографическом порядке алфавита. Используйте "
                "itertools.product."
            ),
            "starter": "from itertools import product\n\n\ndef passwords(alphabet, length):\n    pass\n",
            "tests": [
                {"args": ["ab", 2], "expected": ["aa", "ab", "ba", "bb"]},
                {"args": ["xy", 1], "expected": ["x", "y"]},
                {"args": ["01", 3], "expected": ["000", "001", "010", "011", "100", "101", "110", "111"]},
            ],
            "hint": '[\"\".join(p) for p in product(alphabet, repeat=length)].',
        },
        {
            "id": "rle-groupby",
            "mode": "func",
            "func": "rle",
            "title": "Сжатие повторов",
            "statement": (
                "Напишите функцию rle(s): сжатие подряд идущих повторов "
                "строки — список кортежей (символ, сколько раз подряд): для "
                "«aaabcc» — [('a', 3), ('b', 1), ('c', 2)]. Используйте "
                "groupby без сортировки."
            ),
            "starter": "from itertools import groupby\n\n\ndef rle(s):\n    pass\n",
            "tests": [
                {"args": ["aaabcc"], "expected": [("a", 3), ("b", 1), ("c", 2)]},
                {"args": [""], "expected": []},
                {"args": ["abab"], "expected": [("a", 1), ("b", 1), ("a", 1), ("b", 1)]},
            ],
            "hint": "[(k, len(list(g))) for k, g in groupby(s)].",
        },
        {
            "id": "pairwise-diffs",
            "mode": "func",
            "func": "diffs",
            "title": "Разности соседних",
            "statement": (
                "Напишите функцию diffs(nums): список разностей соседних "
                "элементов: для 1, 4, 9, 16 — 3, 5, 7. Используйте "
                "itertools.pairwise."
            ),
            "starter": "from itertools import pairwise\n\n\ndef diffs(nums):\n    pass\n",
            "tests": [
                {"args": [[1, 4, 9, 16]], "expected": [3, 5, 7]},
                {"args": [[5]], "expected": []},
                {"args": [[10, 7]], "expected": [-3]},
            ],
            "hint": "[b - a for a, b in pairwise(nums)].",
        },
        {
            "id": "small-prefix",
            "mode": "func",
            "func": "small_prefix",
            "title": "Пока числа маленькие",
            "statement": (
                "Напишите функцию small_prefix(nums, limit): начальный кусок "
                "списка, пока элементы меньше limit; на первом большем или "
                "равном — стоп. Используйте itertools.takewhile."
            ),
            "starter": "from itertools import takewhile\n\n\ndef small_prefix(nums, limit):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 9, 3], 5], "expected": [1, 2]},
                {"args": [[10, 1], 5], "expected": []},
                {"args": [[1, 2], 5], "expected": [1, 2]},
            ],
            "hint": "list(takewhile(lambda x: x < limit, nums)).",
        },
    ],
}
