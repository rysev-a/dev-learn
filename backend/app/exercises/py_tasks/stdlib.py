"""Задачи «Python как первый язык»: стандартная библиотека (главы 24–30).

Задачи, где результат — словарь с нестроковыми ключами или объекты модулей,
проверяются скрытым драйвером (JSON-тесты умеют только строковые ключи).
"""

TASKS: dict[int, list[dict]] = {
    24: [
        {
            "id": "top-words",
            "mode": "func",
            "func": "top_words",
            "title": "Самые частые слова",
            "statement": (
                "Напишите функцию top_words(text, n): список из n самых "
                "частых слов текста (слова разделены пробелами, регистр не "
                "учитывать) в виде кортежей (слово, сколько раз) по убыванию "
                "частоты. Используйте Counter."
            ),
            "starter": "from collections import Counter\n\n\ndef top_words(text, n):\n    pass\n",
            "tests": [
                {"args": ["да нет Да нет ДА может", 2], "expected": [("да", 3), ("нет", 2)]},
                {"args": ["а б б в в в", 1], "expected": [("в", 3)]},
                {"args": ["", 3], "expected": []},
            ],
            "hint": "Counter(text.lower().split()).most_common(n).",
        },
        {
            "id": "anagram-counter",
            "mode": "func",
            "func": "is_anagram",
            "title": "Анаграммы",
            "statement": (
                "Напишите функцию is_anagram(a, b): True, если слова состоят "
                "из одних и тех же букв (регистр и пробелы не важны). "
                "Сравните счётчики букв."
            ),
            "starter": "from collections import Counter\n\n\ndef is_anagram(a, b):\n    pass\n",
            "tests": [
                {"args": ["Лотос", "столо"], "expected": True},
                {"args": ["кот", "ток "], "expected": True},
                {"args": ["кот", "кит"], "expected": False},
                {"args": ["аа", "а"], "expected": False},
            ],
            "hint": "Приведите к нижнему регистру, уберите пробелы и сравните Counter(a) == Counter(b).",
        },
        {
            "id": "group-by-length",
            "mode": "stdout",
            "title": "Группы по длине",
            "statement": (
                "Напишите функцию group_by_length(words): словарь «длина → "
                "список слов этой длины» в исходном порядке. Используйте "
                "defaultdict(list) и верните обычный dict."
            ),
            "starter": "from collections import defaultdict\n\n\ndef group_by_length(words):\n    pass\n",
            "driver": (
                "r = group_by_length(['кот', 'пёс', 'слон', 'мышь', 'жук'])\n"
                "print(sorted(r.items()))\nprint(type(r).__name__)\nprint(group_by_length([]))\n"
            ),
            "expected": ["[(3, ['кот', 'пёс', 'жук']), (4, ['слон', 'мышь'])]", "dict", "{}"],
            "hint": "groups[len(w)].append(w); в конце return dict(groups).",
        },
        {
            "id": "moving-average",
            "mode": "func",
            "func": "moving_average",
            "title": "Скользящее среднее",
            "statement": (
                "Напишите функцию moving_average(nums, k): среднее каждого "
                "окна из k подряд идущих чисел (только полные окна). "
                "Используйте deque с maxlen=k."
            ),
            "starter": "from collections import deque\n\n\ndef moving_average(nums, k):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3, 4], 2], "expected": [1.5, 2.5, 3.5]},
                {"args": [[10, 20, 30], 3], "expected": [20.0]},
                {"args": [[1, 2], 3], "expected": []},
            ],
            "hint": "window = deque(maxlen=k); на каждом x: append; если len(window) == k — добавить sum(window) / k.",
        },
        {
            "id": "bfs-order",
            "mode": "func",
            "func": "bfs_order",
            "title": "Обход в ширину",
            "statement": (
                "Напишите функцию bfs_order(graph, start): порядок вершин "
                "при обходе графа в ширину. graph — словарь «вершина → "
                "список соседей». Используйте deque; каждую вершину "
                "посещайте один раз."
            ),
            "starter": "from collections import deque\n\n\ndef bfs_order(graph, start):\n    pass\n",
            "tests": [
                {"args": [{"А": ["Б", "В"], "Б": ["Г"], "В": ["Г"], "Г": []}, "А"], "expected": ["А", "Б", "В", "Г"]},
                {"args": [{"1": ["2"], "2": ["1"]}, "1"], "expected": ["1", "2"]},
                {"args": [{"x": []}, "x"], "expected": ["x"]},
            ],
            "hint": "queue = deque([start]); seen — словарь посещённых; popleft, добавить соседей, которых ещё не было.",
        },
        {
            "id": "namedtuple-distance",
            "mode": "stdout",
            "title": "Точка как namedtuple",
            "statement": (
                "Создайте именованный кортеж Point с полями x и y и функцию "
                "distance(p, q) — евклидово расстояние между двумя точками "
                "(используйте math.hypot)."
            ),
            "starter": "from collections import namedtuple\nimport math\n\nPoint = None\n\n\ndef distance(p, q):\n    pass\n",
            "driver": (
                "p = Point(3, 4)\nprint(p, p.x, p.y)\nprint(distance(Point(0, 0), p))\n"
                "print(p == (3, 4), p._replace(y=0))\n"
            ),
            "expected": ["Point(x=3, y=4) 3 4", "5.0", "True Point(x=3, y=0)"],
            "hint": 'Point = namedtuple("Point", ["x", "y"]); distance: math.hypot(p.x - q.x, p.y - q.y).',
        },
        {
            "id": "k-largest-heap",
            "mode": "func",
            "func": "k_largest",
            "title": "k наибольших",
            "statement": (
                "Напишите функцию k_largest(nums, k): k наибольших чисел по "
                "убыванию. Используйте модуль heapq."
            ),
            "starter": "import heapq\n\n\ndef k_largest(nums, k):\n    pass\n",
            "tests": [
                {"args": [[5, 1, 9, 3, 7, 8], 3], "expected": [9, 8, 7]},
                {"args": [[4, 4, 1], 2], "expected": [4, 4]},
                {"args": [[1, 2], 5], "expected": [2, 1]},
                {"args": [[], 2], "expected": []},
            ],
            "hint": "heapq.nlargest(k, nums) уже возвращает по убыванию.",
        },
        {
            "id": "grade-bisect",
            "mode": "func",
            "func": "grade",
            "title": "Оценка по баллам",
            "statement": (
                "Напишите функцию grade(score): 0–59 → «E», 60–69 → «D», "
                "70–79 → «C», 80–89 → «B», 90–100 → «A». Используйте "
                "bisect и список границ — без цепочки if."
            ),
            "starter": "import bisect\n\n\ndef grade(score):\n    pass\n",
            "tests": [
                {"args": [59], "expected": "E"},
                {"args": [60], "expected": "D"},
                {"args": [79], "expected": "C"},
                {"args": [80], "expected": "B"},
                {"args": [100], "expected": "A"},
            ],
            "hint": 'bounds = [60, 70, 80, 90]; "EDCBA"[bisect.bisect(bounds, score)].',
        },
        {
            "id": "merge-sorted-heap",
            "mode": "func",
            "func": "merge_sorted",
            "title": "Слить отсортированные",
            "statement": (
                "Напишите функцию merge_sorted(lists): один отсортированный "
                "список из нескольких уже отсортированных. Используйте "
                "heapq.merge."
            ),
            "starter": "import heapq\n\n\ndef merge_sorted(lists):\n    pass\n",
            "tests": [
                {"args": [[[1, 4, 7], [2, 5], [3, 6]]], "expected": [1, 2, 3, 4, 5, 6, 7]},
                {"args": [[[], [1]]], "expected": [1]},
                {"args": [[]], "expected": []},
            ],
            "hint": "list(heapq.merge(*lists)).",
        },
    ],
    25: [
        {
            "id": "lcm-all",
            "mode": "func",
            "func": "lcm_all",
            "title": "Общее кратное списка",
            "statement": (
                "Напишите функцию lcm_all(nums): наименьшее общее кратное "
                "всех чисел списка; для пустого списка — 1. Используйте "
                "math.lcm."
            ),
            "starter": "import math\n\n\ndef lcm_all(nums):\n    pass\n",
            "tests": [
                {"args": [[4, 6]], "expected": 12},
                {"args": [[2, 3, 5]], "expected": 30},
                {"args": [[]], "expected": 1},
                {"args": [[7]], "expected": 7},
            ],
            "hint": "math.lcm(*nums) — у lcm без аргументов результат 1.",
        },
        {
            "id": "nearly-equal",
            "mode": "func",
            "func": "nearly_equal",
            "title": "Почти равны",
            "statement": (
                "Напишите функцию nearly_equal(a, b): True, если дробные "
                "числа равны с учётом погрешности (math.isclose)."
            ),
            "starter": "import math\n\n\ndef nearly_equal(a, b):\n    pass\n",
            "tests": [
                {"args": [0.30000000000000004, 0.3], "expected": True},
                {"args": [1.0, 1.1], "expected": False},
                {"args": [1e-12, 0.0], "expected": False},
                {"args": [100.0, 100.0], "expected": True},
            ],
            "hint": "return math.isclose(a, b).",
        },
        {
            "id": "round-half-up",
            "mode": "func",
            "func": "round_half_up",
            "title": "Школьное округление",
            "statement": (
                "Напишите функцию round_half_up(text, digits): число задано "
                "СТРОКОЙ; верните строку, округлённую до digits знаков после "
                "запятой по школьным правилам (0.5 — вверх). Используйте "
                "Decimal и quantize с ROUND_HALF_UP."
            ),
            "starter": "from decimal import Decimal, ROUND_HALF_UP\n\n\ndef round_half_up(text, digits):\n    pass\n",
            "tests": [
                {"args": ["2.675", 2], "expected": "2.68"},
                {"args": ["2.5", 0], "expected": "3"},
                {"args": ["3.14159", 3], "expected": "3.142"},
                {"args": ["1.005", 2], "expected": "1.01"},
            ],
            "hint": 'str(Decimal(text).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP)) — либо Decimal("0.01") для двух знаков.',
        },
        {
            "id": "total-decimal",
            "mode": "func",
            "func": "total_price",
            "title": "Сумма чека",
            "statement": (
                "Напишите функцию total_price(prices): prices — список цен "
                "СТРОКАМИ («19.99»). Верните сумму строкой с двумя знаками "
                "после запятой. Используйте Decimal (никаких float)."
            ),
            "starter": "from decimal import Decimal\n\n\ndef total_price(prices):\n    pass\n",
            "tests": [
                {"args": [["19.99", "0.01"]], "expected": "20.00"},
                {"args": [["0.1", "0.2"]], "expected": "0.30"},
                {"args": [[]], "expected": "0.00"},
                {"args": [["100", "2.5", "0.25"]], "expected": "102.75"},
            ],
            "hint": 'total = sum((Decimal(p) for p in prices), Decimal("0")); str(total.quantize(Decimal("0.01"))).',
        },
        {
            "id": "fraction-sum",
            "mode": "func",
            "func": "fraction_sum",
            "title": "Сумма дробей",
            "statement": (
                "Напишите функцию fraction_sum(pairs): pairs — список пар "
                "[числитель, знаменатель]. Верните сумму дробей строкой в "
                "несократимом виде («1/2» или «3» для целого). Используйте "
                "Fraction."
            ),
            "starter": "from fractions import Fraction\n\n\ndef fraction_sum(pairs):\n    pass\n",
            "tests": [
                {"args": [[[1, 3], [1, 6]]], "expected": "1/2"},
                {"args": [[[1, 2], [1, 2]]], "expected": "1"},
                {"args": [[]], "expected": "0"},
                {"args": [[[2, 4], [3, 4]]], "expected": "5/4"},
            ],
            "hint": "str(sum((Fraction(a, b) for a, b in pairs), Fraction(0))) — Fraction сам сокращает и печатает целое без знаменателя.",
        },
        {
            "id": "roll-dice-seed",
            "mode": "stdout",
            "title": "Повторяемые кубики",
            "statement": (
                "Напишите функцию roll_dice(n, seed): список из n бросков "
                "кубика (числа 1–6). Одно и то же seed должно давать один и "
                "тот же результат: задайте зерно через random.seed."
            ),
            "starter": "import random\n\n\ndef roll_dice(n, seed):\n    pass\n",
            "driver": (
                "a = roll_dice(10, 5)\nb = roll_dice(10, 5)\nc = roll_dice(10, 6)\n"
                "print(a == b, len(a), all(1 <= x <= 6 for x in a))\nprint(roll_dice(0, 1))\n"
            ),
            "expected": ["True 10 True", "[]"],
            "hint": "random.seed(seed); return [random.randint(1, 6) for _ in range(n)].",
        },
        {
            "id": "stats-summary",
            "mode": "func",
            "func": "stats_summary",
            "title": "Сводка по данным",
            "statement": (
                "Напишите функцию stats_summary(data): кортеж (среднее, "
                "медиана, мода) списка чисел. Используйте модуль statistics."
            ),
            "starter": "import statistics\n\n\ndef stats_summary(data):\n    pass\n",
            "tests": [
                {"args": [[2, 4, 4, 4, 5, 5, 7, 9]], "expected": (5, 4.5, 4)},
                {"args": [[1, 2, 3]], "expected": (2, 2, 1)},
                {"args": [[10]], "expected": (10, 10, 10)},
            ],
            "hint": "return statistics.mean(data), statistics.median(data), statistics.mode(data).",
        },
        {
            "id": "random-password",
            "mode": "stdout",
            "title": "Безопасный пароль",
            "statement": (
                "Напишите функцию make_password(length): строка из length "
                "случайных символов — латинские буквы и цифры. Для "
                "безопасности используйте модуль secrets, а не random."
            ),
            "starter": "import secrets\nimport string\n\n\ndef make_password(length):\n    pass\n",
            "driver": (
                "import string\nok = set(string.ascii_letters + string.digits)\n"
                "p = make_password(16)\nprint(len(p), all(c in ok for c in p))\n"
                "print(make_password(16) != make_password(16), make_password(0) == '')\n"
            ),
            "expected": ["16 True", "True True"],
            "hint": '"".join(secrets.choice(alphabet) for _ in range(length)) — alphabet = string.ascii_letters + string.digits.',
        },
        {
            "id": "binary-info",
            "mode": "func",
            "func": "binary_info",
            "title": "Двоичная запись",
            "statement": (
                "Напишите функцию binary_info(n): кортеж (двоичная запись "
                "числа n БЕЗ префикса 0b, количество единиц в ней) для "
                "неотрицательного n."
            ),
            "starter": "def binary_info(n):\n    pass\n",
            "tests": [
                {"args": [10], "expected": ("1010", 2)},
                {"args": [0], "expected": ("0", 0)},
                {"args": [255], "expected": ("11111111", 8)},
                {"args": [1], "expected": ("1", 1)},
            ],
            "hint": 'b = f"{n:b}"; return b, b.count("1").',
        },
    ],
    26: [
        {
            "id": "days-between",
            "mode": "func",
            "func": "days_between",
            "title": "Дней между датами",
            "statement": (
                "Напишите функцию days_between(a, b): сколько дней от даты a "
                "до даты b (может быть отрицательным). Даты — строки "
                "«ГГГГ-ММ-ДД»."
            ),
            "starter": "from datetime import date\n\n\ndef days_between(a, b):\n    pass\n",
            "tests": [
                {"args": ["2024-12-25", "2025-01-01"], "expected": 7},
                {"args": ["2024-03-01", "2023-03-01"], "expected": -366},
                {"args": ["2024-05-05", "2024-05-05"], "expected": 0},
            ],
            "hint": "(date.fromisoformat(b) - date.fromisoformat(a)).days.",
        },
        {
            "id": "add-days",
            "mode": "func",
            "func": "add_days",
            "title": "Прибавить дни",
            "statement": (
                "Напишите функцию add_days(day, n): дата через n дней "
                "(n может быть отрицательным). Вход и результат — строки "
                "«ГГГГ-ММ-ДД»."
            ),
            "starter": "from datetime import date, timedelta\n\n\ndef add_days(day, n):\n    pass\n",
            "tests": [
                {"args": ["2024-02-28", 2], "expected": "2024-03-01"},
                {"args": ["2023-02-28", 2], "expected": "2023-03-02"},
                {"args": ["2024-01-01", -1], "expected": "2023-12-31"},
            ],
            "hint": "(date.fromisoformat(day) + timedelta(days=n)).isoformat().",
        },
        {
            "id": "format-date-ru",
            "mode": "func",
            "func": "format_ru",
            "title": "Дата по-русски",
            "statement": (
                "Напишите функцию format_ru(day): из «ГГГГ-ММ-ДД» получите "
                "«ДД.ММ.ГГГГ». Используйте datetime и strftime."
            ),
            "starter": "from datetime import date\n\n\ndef format_ru(day):\n    pass\n",
            "tests": [
                {"args": ["2024-03-05"], "expected": "05.03.2024"},
                {"args": ["1999-12-31"], "expected": "31.12.1999"},
            ],
            "hint": 'date.fromisoformat(day).strftime("%d.%m.%Y").',
        },
        {
            "id": "weekday-name",
            "mode": "func",
            "func": "weekday_name",
            "title": "День недели",
            "statement": (
                "Напишите функцию weekday_name(day): название дня недели "
                "по-русски («понедельник», «вторник», …) для даты "
                "«ГГГГ-ММ-ДД»."
            ),
            "starter": "from datetime import date\n\nNAMES = [\"понедельник\", \"вторник\", \"среда\", \"четверг\", \"пятница\", \"суббота\", \"воскресенье\"]\n\n\ndef weekday_name(day):\n    pass\n",
            "tests": [
                {"args": ["2000-01-01"], "expected": "суббота"},
                {"args": ["2024-02-29"], "expected": "четверг"},
                {"args": ["2024-03-04"], "expected": "понедельник"},
            ],
            "hint": "NAMES[date.fromisoformat(day).weekday()].",
        },
        {
            "id": "age-years",
            "mode": "func",
            "func": "age",
            "title": "Возраст",
            "statement": (
                "Напишите функцию age(born, today): полных лет между датой "
                "рождения и датой «сегодня» (строки «ГГГГ-ММ-ДД»). Если день "
                "рождения в этом году ещё не наступил, год не засчитывается."
            ),
            "starter": "from datetime import date\n\n\ndef age(born, today):\n    pass\n",
            "tests": [
                {"args": ["2000-06-15", "2024-06-14"], "expected": 23},
                {"args": ["2000-06-15", "2024-06-15"], "expected": 24},
                {"args": ["2000-02-29", "2024-02-28"], "expected": 23},
                {"args": ["2024-01-01", "2024-01-01"], "expected": 0},
            ],
            "hint": "years = today.year - born.year; если (today.month, today.day) < (born.month, born.day) — вычесть 1.",
        },
        {
            "id": "workdays-count",
            "mode": "func",
            "func": "workdays",
            "title": "Рабочие дни",
            "statement": (
                "Напишите функцию workdays(start, end): сколько будних дней "
                "(пн–пт) в промежутке от start до end включительно. Даты — "
                "строки «ГГГГ-ММ-ДД»."
            ),
            "starter": "from datetime import date, timedelta\n\n\ndef workdays(start, end):\n    pass\n",
            "tests": [
                {"args": ["2024-03-01", "2024-03-10"], "expected": 6},
                {"args": ["2024-03-02", "2024-03-03"], "expected": 0},
                {"args": ["2024-03-04", "2024-03-04"], "expected": 1},
            ],
            "hint": "Идите циклом от start до end и считайте дни, у которых weekday() < 5.",
        },
        {
            "id": "last-day-month",
            "mode": "func",
            "func": "last_day",
            "title": "Последний день месяца",
            "statement": (
                "Напишите функцию last_day(year, month): число дней в "
                "месяце. Используйте модуль calendar."
            ),
            "starter": "import calendar\n\n\ndef last_day(year, month):\n    pass\n",
            "tests": [
                {"args": [2024, 2], "expected": 29},
                {"args": [2023, 2], "expected": 28},
                {"args": [2024, 12], "expected": 31},
                {"args": [2024, 4], "expected": 30},
            ],
            "hint": "calendar.monthrange(year, month)[1].",
        },
        {
            "id": "utc-to-offset",
            "mode": "func",
            "func": "to_offset",
            "title": "Из UTC в местное",
            "statement": (
                "Напишите функцию to_offset(iso_utc, hours): время "
                "«ГГГГ-ММ-ДДTЧЧ:ММ», заданное в UTC, переведите в пояс со "
                "смещением hours часов и верните строкой «ГГГГ-ММ-ДД ЧЧ:ММ». "
                "Используйте timezone и timedelta."
            ),
            "starter": "from datetime import datetime, timedelta, timezone\n\n\ndef to_offset(iso_utc, hours):\n    pass\n",
            "tests": [
                {"args": ["2024-06-01T12:00", 3], "expected": "2024-06-01 15:00"},
                {"args": ["2024-06-01T23:30", 3], "expected": "2024-06-02 02:30"},
                {"args": ["2024-01-01T01:00", -5], "expected": "2023-12-31 20:00"},
            ],
            "hint": "dt = datetime.fromisoformat(s).replace(tzinfo=timezone.utc); dt.astimezone(timezone(timedelta(hours=hours))).strftime(...).",
        },
        {
            "id": "parse-log-line",
            "mode": "func",
            "func": "parse_log",
            "title": "Строка журнала",
            "statement": (
                "Напишите функцию parse_log(line): строка журнала вида "
                "«2024-03-05 09:07:03 ERROR сбой диска». Верните кортеж "
                "(время в формате ISO с буквой T, уровень)."
            ),
            "starter": "from datetime import datetime\n\n\ndef parse_log(line):\n    pass\n",
            "tests": [
                {"args": ["2024-03-05 09:07:03 ERROR сбой диска"], "expected": ("2024-03-05T09:07:03", "ERROR")},
                {"args": ["2023-12-31 23:59:59 INFO ok"], "expected": ("2023-12-31T23:59:59", "INFO")},
            ],
            "hint": "date_part, time_part, level, *_ = line.split(); datetime.fromisoformat(date_part + ' ' + time_part).isoformat().",
        },
    ],
    27: [
        {
            "id": "is-phone",
            "mode": "func",
            "func": "is_phone",
            "title": "Номер телефона",
            "statement": (
                "Напишите функцию is_phone(s): True, если вся строка — номер "
                "вида «+7-900-123-45-67» (после +7 четыре группы через дефис: "
                "3, 3, 2 и 2 цифры). Используйте re.fullmatch."
            ),
            "starter": "import re\n\n\ndef is_phone(s):\n    pass\n",
            "tests": [
                {"args": ["+7-900-123-45-67"], "expected": True},
                {"args": ["+7-900-123-45-6"], "expected": False},
                {"args": ["8-900-123-45-67"], "expected": False},
                {"args": ["тел +7-900-123-45-67"], "expected": False},
            ],
            "hint": r'bool(re.fullmatch(r"\+7-\d{3}-\d{3}-\d{2}-\d{2}", s)).',
        },
        {
            "id": "find-numbers",
            "mode": "func",
            "func": "find_numbers",
            "title": "Числа из текста",
            "statement": (
                "Напишите функцию find_numbers(text): список всех целых "
                "чисел в тексте, как int; перед числом может стоять минус."
            ),
            "starter": "import re\n\n\ndef find_numbers(text):\n    pass\n",
            "tests": [
                {"args": ["у меня 3 яблока и -12 груш, а 100 — много"], "expected": [3, -12, 100]},
                {"args": ["нет чисел"], "expected": []},
                {"args": ["a1b22c333"], "expected": [1, 22, 333]},
            ],
            "hint": r'[int(x) for x in re.findall(r"-?\d+", text)].',
        },
        {
            "id": "extract-emails",
            "mode": "func",
            "func": "extract_emails",
            "title": "Адреса почты",
            "statement": (
                "Напишите функцию extract_emails(text): список адресов "
                "вида имя@домен.зона (латиница, цифры, точки и подчёркивания "
                "в имени и домене) в порядке появления."
            ),
            "starter": "import re\n\n\ndef extract_emails(text):\n    pass\n",
            "tests": [
                {"args": ["пишите на ivan@mail.ru или olga_1@ya.ru!"], "expected": ["ivan@mail.ru", "olga_1@ya.ru"]},
                {"args": ["почты нет"], "expected": []},
                {"args": ["a.b@c.d.org, x"], "expected": ["a.b@c.d.org"]},
            ],
            "hint": r're.findall(r"[\w.]+@[\w.]+\w", text).',
        },
        {
            "id": "collapse-spaces",
            "mode": "func",
            "func": "collapse_spaces",
            "title": "Лишние пробелы",
            "statement": (
                "Напишите функцию collapse_spaces(text): подряд идущие "
                "пробельные символы (пробелы, табуляции, переводы строк) "
                "заменить одним пробелом и убрать пробелы по краям."
            ),
            "starter": "import re\n\n\ndef collapse_spaces(text):\n    pass\n",
            "tests": [
                {"args": ["много   пробелов\n тут"], "expected": "много пробелов тут"},
                {"args": ["   край   "], "expected": "край"},
                {"args": ["а\t\tб"], "expected": "а б"},
            ],
            "hint": r're.sub(r"\s+", " ", text).strip().',
        },
        {
            "id": "parse-date-groups",
            "mode": "func",
            "func": "parse_date",
            "title": "Разбор даты",
            "statement": (
                "Напишите функцию parse_date(s): из строки «ДД.ММ.ГГГГ» "
                "верните кортеж чисел (год, месяц, день). Если строка не "
                "соответствует формату целиком — None."
            ),
            "starter": "import re\n\n\ndef parse_date(s):\n    pass\n",
            "tests": [
                {"args": ["05.03.2024"], "expected": (2024, 3, 5)},
                {"args": ["31.12.1999"], "expected": (1999, 12, 31)},
                {"args": ["5.3.2024"], "expected": None},
                {"args": ["дата 05.03.2024"], "expected": None},
            ],
            "hint": r'm = re.fullmatch(r"(\d\d)\.(\d\d)\.(\d{4})", s); если m — int(m[3]), int(m[2]), int(m[1]).',
        },
        {
            "id": "hashtags",
            "mode": "func",
            "func": "hashtags",
            "title": "Хештеги",
            "statement": (
                "Напишите функцию hashtags(text): список хештегов (слово "
                "после #, буквы, цифры и подчёркивания) без символа #, в "
                "нижнем регистре."
            ),
            "starter": "import re\n\n\ndef hashtags(text):\n    pass\n",
            "tests": [
                {"args": ["Привет #Питон и #regex_101, не # тег"], "expected": ["питон", "regex_101"]},
                {"args": ["нет"], "expected": []},
                {"args": ["#А#Б"], "expected": ["а", "б"]},
            ],
            "hint": r'[t.lower() for t in re.findall(r"#(\w+)", text)].',
        },
        {
            "id": "split-words-re",
            "mode": "func",
            "func": "split_words",
            "title": "Слова без знаков",
            "statement": (
                "Напишите функцию split_words(text): список слов текста "
                "(буквы и цифры), без знаков препинания и пустых элементов. "
                "Используйте re.findall."
            ),
            "starter": "import re\n\n\ndef split_words(text):\n    pass\n",
            "tests": [
                {"args": ["Привет, мир! Как дела?"], "expected": ["Привет", "мир", "Как", "дела"]},
                {"args": ["...!!!"], "expected": []},
                {"args": ["a1-b2"], "expected": ["a1", "b2"]},
            ],
            "hint": r're.findall(r"\w+", text).',
        },
        {
            "id": "censor-words",
            "mode": "func",
            "func": "censor",
            "title": "Цензура",
            "statement": (
                "Напишите функцию censor(text, bad): замените каждое слово "
                "из списка bad (целиком, без учёта регистра) на «***». "
                "Части других слов не трогайте: «кот» не должно портить "
                "«котёл»."
            ),
            "starter": "import re\n\n\ndef censor(text, bad):\n    pass\n",
            "tests": [
                {"args": ["Кот и котёл, КОТ!", ["кот"]], "expected": "*** и котёл, ***!"},
                {"args": ["ничего", ["плохо"]], "expected": "ничего"},
                {"args": ["раз два три", ["два", "три"]], "expected": "раз *** ***"},
            ],
            "hint": r'Соберите шаблон r"\b(?:" + "|".join(map(re.escape, bad)) + r")\b" и вызовите re.sub с флагом re.I.',
        },
        {
            "id": "parse-log-dict",
            "mode": "func",
            "func": "parse_log",
            "title": "Журнал в словарь",
            "statement": (
                "Напишите функцию parse_log(line): строка «2024-03-05 "
                "09:07:03 ERROR сбой диска» → словарь с ключами «date», "
                "«time», «level», «msg». Если строка не подходит — None. "
                "Используйте именованные группы."
            ),
            "starter": "import re\n\n\ndef parse_log(line):\n    pass\n",
            "tests": [
                {"args": ["2024-03-05 09:07:03 ERROR сбой диска"], "expected": {"date": "2024-03-05", "time": "09:07:03", "level": "ERROR", "msg": "сбой диска"}},
                {"args": ["2023-12-31 23:59:59 INFO ok"], "expected": {"date": "2023-12-31", "time": "23:59:59", "level": "INFO", "msg": "ok"}},
                {"args": ["мусор"], "expected": None},
            ],
            "hint": r'(?P<date>\d{4}-\d\d-\d\d) (?P<time>[\d:]{8}) (?P<level>[A-Z]+) (?P<msg>.*); m.groupdict().',
        },
    ],
    28: [
        {
            "id": "parse-cli-args",
            "mode": "func",
            "func": "parse_cli",
            "title": "Разбор аргументов",
            "statement": (
                "Напишите функцию parse_cli(argv): с помощью argparse разберите "
                "список аргументов командной строки: позиционный text, "
                "необязательный --count (целое, по умолчанию 1) и флаг "
                "--upper. Верните кортеж (text, count, upper)."
            ),
            "starter": "import argparse\n\n\ndef parse_cli(argv):\n    pass\n",
            "tests": [
                {"args": [["привет", "--count", "3", "--upper"]], "expected": ("привет", 3, True)},
                {"args": [["мир"]], "expected": ("мир", 1, False)},
                {"args": [["--count", "2", "а"]], "expected": ("а", 2, False)},
            ],
            "hint": "p.add_argument('text'); p.add_argument('--count', type=int, default=1); p.add_argument('--upper', action='store_true').",
        },
        {
            "id": "sum-cli-main",
            "mode": "stdout",
            "title": "Утилита-сумматор",
            "statement": (
                "Напишите функцию main(argv): аргументы argv — числа "
                "(argparse, nargs='*', type=int). Если чисел нет — напечатайте "
                "в stderr «нет чисел» и верните 1; иначе напечатайте сумму и "
                "верните 0."
            ),
            "starter": "import argparse\nimport sys\n\n\ndef main(argv=None):\n    pass\n",
            "driver": (
                "print('код', main(['1', '2', '3']))\nprint('код', main([]))\n"
                "print('код', main(['-5', '5']))\n"
            ),
            "expected": ["6", "код 0", "код 1", "0", "код 0"],
            "hint": "p = argparse.ArgumentParser(); p.add_argument('nums', nargs='*', type=int); args = p.parse_args(argv).",
        },
        {
            "id": "env-or-default",
            "mode": "stdout",
            "title": "Настройка из окружения",
            "statement": (
                "Напишите функцию get_port(): значение переменной окружения "
                "PORT как целое число; если переменной нет — 8000."
            ),
            "starter": "import os\n\n\ndef get_port():\n    pass\n",
            "driver": (
                "import os\nos.environ.pop('PORT', None)\nprint(get_port())\n"
                "os.environ['PORT'] = '9090'\nprint(get_port(), type(get_port()).__name__)\n"
            ),
            "expected": ["8000", "9090 int"],
            "hint": "int(os.environ.get('PORT', 8000)).",
        },
        {
            "id": "make-logger",
            "mode": "stdout",
            "title": "Свой логгер",
            "statement": (
                "Напишите функцию make_logger(stream): логгер с именем "
                "«app», который пишет в переданный поток сообщения уровня INFO "
                "и выше в формате «УРОВЕНЬ: сообщение» (propagate выключите)."
            ),
            "starter": "import logging\n\n\ndef make_logger(stream):\n    pass\n",
            "driver": (
                "import io\nbuf = io.StringIO()\nlog = make_logger(buf)\n"
                "log.debug('скрыто')\nlog.info('старт')\nlog.warning('внимание')\nlog.error('сбой')\n"
                "print(buf.getvalue().splitlines())\n"
            ),
            "expected": ["['INFO: старт', 'WARNING: внимание', 'ERROR: сбой']"],
            "hint": "StreamHandler(stream) + Formatter('%(levelname)s: %(message)s'); logger.setLevel(logging.INFO); logger.propagate = False.",
        },
        {
            "id": "run-python-subprocess",
            "mode": "stdout",
            "title": "Запуск процесса",
            "statement": (
                "Напишите функцию run_python(code): запускает дочерний "
                "интерпретатор (sys.executable) с кодом code и возвращает "
                "кортеж (код возврата, вывод без пробелов по краям). "
                "Используйте subprocess.run, capture_output и text."
            ),
            "starter": "import subprocess\nimport sys\n\n\ndef run_python(code):\n    pass\n",
            "driver": (
                "print(run_python('print(2 + 2)'))\nprint(run_python('raise SystemExit(5)'))\n"
                "print(run_python('import sys; print(\"привет\"); sys.exit(1)'))\n"
            ),
            "expected": ["(0, '4')", "(5, '')", "(1, 'привет')"],
            "hint": "r = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True); return r.returncode, r.stdout.strip().",
        },
        {
            "id": "run-with-timeout",
            "mode": "stdout",
            "title": "Процесс с таймаутом",
            "statement": (
                "Напишите функцию run_limited(code, seconds): запускает код "
                "в дочернем интерпретаторе; если он не уложился в seconds "
                "секунд — верните строку «таймаут», иначе — его вывод без "
                "пробелов по краям."
            ),
            "starter": "import subprocess\nimport sys\n\n\ndef run_limited(code, seconds):\n    pass\n",
            "driver": (
                "print(run_limited('print(1)', 5))\nprint(run_limited('import time; time.sleep(10)', 0.3))\n"
            ),
            "expected": ["1", "таймаут"],
            "hint": "try: subprocess.run(..., timeout=seconds) / except subprocess.TimeoutExpired: return 'таймаут'.",
        },
        {
            "id": "count-nonempty-stream",
            "mode": "stdout",
            "title": "Строки из потока",
            "statement": (
                "Напишите функцию count_lines(stream): сколько непустых строк "
                "(после strip) в файловом объекте stream. Работайте с потоком "
                "так же, как со стандартным вводом: перебирайте его циклом."
            ),
            "starter": "def count_lines(stream):\n    pass\n",
            "driver": (
                "import io\nprint(count_lines(io.StringIO('а\\n\\nб\\n   \\nв\\n')))\n"
                "print(count_lines(io.StringIO('')))\nprint(count_lines(io.StringIO('одна')))\n"
            ),
            "expected": ["3", "0", "1"],
            "hint": "n = 0; for line in stream: if line.strip(): n += 1.",
        },
    ],
    29: [
        {
            "id": "point-dataclass",
            "mode": "stdout",
            "title": "Точка-датакласс",
            "statement": (
                "Опишите датакласс Point с полями x и y (числа, по умолчанию "
                "0) и методом distance_to(other) — расстояние до другой "
                "точки (math.hypot)."
            ),
            "starter": "from dataclasses import dataclass\nimport math\n\n\nclass Point:\n    pass\n",
            "driver": (
                "p = Point(3, 4)\nprint(p)\nprint(Point())\nprint(p == Point(3, 4), p == Point(4, 3))\n"
                "print(Point().distance_to(p))\n"
            ),
            "expected": ["Point(x=3, y=4)", "Point(x=0, y=0)", "True False", "5.0"],
            "hint": "@dataclass над class Point; x: float = 0; y: float = 0.",
        },
        {
            "id": "playlist-default-factory",
            "mode": "stdout",
            "title": "Плейлист без общего списка",
            "statement": (
                "Опишите датакласс Playlist с полями name (строка) и songs "
                "(список, по умолчанию пустой — но свой у каждого "
                "экземпляра) и методом add(song), который добавляет песню."
            ),
            "starter": "from dataclasses import dataclass, field\n\n\nclass Playlist:\n    pass\n",
            "driver": (
                "a = Playlist('а')\nb = Playlist('б')\na.add('песня 1')\na.add('песня 2')\n"
                "print(a)\nprint(b.songs)\nprint(a.songs is b.songs)\n"
            ),
            "expected": ["Playlist(name='а', songs=['песня 1', 'песня 2'])", "[]", "False"],
            "hint": "songs: list = field(default_factory=list).",
        },
        {
            "id": "money-frozen",
            "mode": "stdout",
            "title": "Неизменяемые деньги",
            "statement": (
                "Опишите неизменяемый (frozen) датакласс Money с полями "
                "amount (число) и currency (строка), сравниваемый по "
                "порядку полей (order=True)."
            ),
            "starter": "from dataclasses import dataclass\n\n\nclass Money:\n    pass\n",
            "driver": (
                "a, b = Money(5, 'RUB'), Money(3, 'RUB')\nprint(sorted([a, b]))\nprint({a: 'пять'}[Money(5, 'RUB')])\n"
                "try:\n    a.amount = 1\nexcept Exception as e:\n    print(type(e).__name__)\n"
            ),
            "expected": ["[Money(amount=3, currency='RUB'), Money(amount=5, currency='RUB')]", "пять", "FrozenInstanceError"],
            "hint": "@dataclass(frozen=True, order=True) — и заморозка, и сортировка, и хеш.",
        },
        {
            "id": "status-enum",
            "mode": "stdout",
            "title": "Статус заказа",
            "statement": (
                "Опишите перечисление Status с членами NEW = 'new', PAID = "
                "'paid', SHIPPED = 'shipped' и методом is_active() — True "
                "для NEW и PAID, False для SHIPPED."
            ),
            "starter": "from enum import Enum\n\n\nclass Status(Enum):\n    pass\n",
            "driver": (
                "print(Status('paid'), Status.NEW.value, Status['SHIPPED'].name)\n"
                "print([s.is_active() for s in Status])\n"
                "try:\n    Status('lost')\nexcept ValueError:\n    print('нет такого статуса')\n"
            ),
            "expected": ["Status.PAID new SHIPPED", "[True, True, False]", "нет такого статуса"],
            "hint": "NEW = 'new' и так далее; is_active: return self in (Status.NEW, Status.PAID).",
        },
        {
            "id": "perm-flag",
            "mode": "stdout",
            "title": "Права доступа",
            "statement": (
                "Опишите Flag-перечисление Perm с членами R, W, X (через "
                "auto) и функцию describe(p): строка из трёх символов, "
                "например «rw-» для R|W и «r-x» для R|X."
            ),
            "starter": "from enum import Flag, auto\n\n\nclass Perm(Flag):\n    pass\n\n\ndef describe(p):\n    pass\n",
            "driver": (
                "print(describe(Perm.R | Perm.W))\nprint(describe(Perm.R | Perm.X))\n"
                "print(describe(Perm.R | Perm.W | Perm.X))\nprint(describe(Perm(0)))\n"
            ),
            "expected": ["rw-", "r-x", "rwx", "---"],
            "hint": "('r' if Perm.R in p else '-') + ... для W и X.",
        },
        {
            "id": "annotated-average",
            "mode": "stdout",
            "title": "Функция с подсказками",
            "statement": (
                "Напишите функцию average(nums, default) с подсказками "
                "типов: nums — list[float], default — float (по умолчанию "
                "0.0), результат — float. Возвращает среднее, а для пустого "
                "списка — default."
            ),
            "starter": "def average(nums, default=0.0):\n    pass\n",
            "driver": (
                "print(average([1, 2, 3]), average([], 9.5))\n"
                "print(sorted(average.__annotations__))\nprint(average.__annotations__['return'].__name__)\n"
            ),
            "expected": ["2.0 9.5", "['default', 'nums', 'return']", "float"],
            "hint": "def average(nums: list[float], default: float = 0.0) -> float:",
        },
        {
            "id": "match-shape",
            "mode": "func",
            "func": "area",
            "title": "Площадь через match",
            "statement": (
                "Напишите функцию area(shape): shape — список ['circle', r], "
                "['rect', w, h] или ['square', a]. Верните площадь (для круга "
                "3 * r * r, чтобы не зависеть от π). Для остальных форм — "
                "None. Используйте match/case."
            ),
            "starter": "def area(shape):\n    pass\n",
            "tests": [
                {"args": [["circle", 2]], "expected": 12},
                {"args": [["rect", 3, 4]], "expected": 12},
                {"args": [["square", 5]], "expected": 25},
                {"args": [["triangle", 1, 2, 3]], "expected": None},
                {"args": [[]], "expected": None},
            ],
            "hint": 'case ["circle", r]: return 3 * r * r; case ["rect", w, h]: ...; case _: return None.',
        },
        {
            "id": "deepcopy-matrix",
            "mode": "stdout",
            "title": "Независимая копия",
            "statement": (
                "Напишите функцию clone_and_fill(matrix, value): возвращает "
                "копию списка списков, в которой ВСЕ числа заменены на "
                "value. Исходная таблица не должна измениться — используйте "
                "copy.deepcopy и вложенный цикл."
            ),
            "starter": "import copy\n\n\ndef clone_and_fill(matrix, value):\n    pass\n",
            "driver": (
                "m = [[1, 2], [3, 4]]\nr = clone_and_fill(m, 0)\nprint(m)\nprint(r)\nprint(r is m, r[0] is m[0])\n"
            ),
            "expected": ["[[1, 2], [3, 4]]", "[[0, 0], [0, 0]]", "False False"],
            "hint": "result = copy.deepcopy(matrix); for row in result: for j in range(len(row)): row[j] = value.",
        },
    ],
    30: [
        {
            "id": "tests-for-leap",
            "mode": "stdout",
            "title": "Тесты для високосного года",
            "statement": (
                "Допишите класс TestLeap (unittest): тесты функции "
                "is_leap(year). Проверка запустит ваши тесты против верной "
                "реализации (они должны ПРОЙТИ) и против трёх сломанных "
                "(они должны УПАСТЬ). Покройте типичный год, года-века и "
                "года, кратные 400."
            ),
            "starter": "import unittest\n\n\nclass TestLeap(unittest.TestCase):\n    def test_example(self):\n        pass  # вызывайте is_leap(год)\n",
            "driver": (
                "import io\n"
                "def run():\n"
                "    r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestLeap))\n"
                "    return r.wasSuccessful() and r.testsRun > 0\n"
                "def good(y): return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)\n"
                "def bad1(y): return y % 4 == 0\n"
                "def bad2(y): return y % 4 == 0 and y % 100 != 0\n"
                "def bad3(y): return y % 400 == 0\n"
                "for name, f in [('верная', good), ('ошибка 1', bad1), ('ошибка 2', bad2), ('ошибка 3', bad3)]:\n"
                "    is_leap = f\n"
                "    print(name, 'тесты прошли' if run() else 'тесты упали')\n"
            ),
            "expected": ["верная тесты прошли", "ошибка 1 тесты упали", "ошибка 2 тесты упали", "ошибка 3 тесты упали"],
            "hint": "assertTrue(is_leap(2024)), assertFalse(is_leap(2023)), assertFalse(is_leap(1900)), assertTrue(is_leap(2000)).",
        },
        {
            "id": "tests-for-clamp",
            "mode": "stdout",
            "title": "Тесты для clamp",
            "statement": (
                "Допишите класс TestClamp: тесты функции clamp(x, low, high) "
                "— ограничивает x диапазоном [low, high]. Ваши тесты должны "
                "пройти на верной реализации и упасть на каждой из трёх "
                "сломанных. Проверьте значения внутри, ниже, выше и на "
                "границах."
            ),
            "starter": "import unittest\n\n\nclass TestClamp(unittest.TestCase):\n    def test_example(self):\n        pass  # вызывайте clamp(x, low, high)\n",
            "driver": (
                "import io\n"
                "def run():\n"
                "    r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestClamp))\n"
                "    return r.wasSuccessful() and r.testsRun > 0\n"
                "def good(x, lo, hi): return min(max(x, lo), hi)\n"
                "def bad1(x, lo, hi): return max(x, lo)\n"
                "def bad2(x, lo, hi): return min(x, hi)\n"
                "def bad3(x, lo, hi):\n"
                "    if x < lo: return lo\n"
                "    if x > hi: return hi - 1\n"
                "    return x\n"
                "for name, f in [('верная', good), ('ошибка 1', bad1), ('ошибка 2', bad2), ('ошибка 3', bad3)]:\n"
                "    clamp = f\n"
                "    print(name, 'тесты прошли' if run() else 'тесты упали')\n"
            ),
            "expected": ["верная тесты прошли", "ошибка 1 тесты упали", "ошибка 2 тесты упали", "ошибка 3 тесты упали"],
            "hint": "clamp(5, 0, 10) == 5; clamp(-3, 0, 10) == 0; clamp(42, 0, 10) == 10; и сами границы.",
        },
        {
            "id": "tests-for-divide",
            "mode": "stdout",
            "title": "Тесты для divide",
            "statement": (
                "Допишите класс TestDivide: тесты функции divide(a, b) — "
                "обычное деление; при b == 0 она должна поднимать "
                "ValueError. Ваши тесты должны пройти на верной реализации "
                "и упасть на трёх сломанных. Не забудьте assertRaises."
            ),
            "starter": "import unittest\n\n\nclass TestDivide(unittest.TestCase):\n    def test_example(self):\n        pass  # вызывайте divide(a, b)\n",
            "driver": (
                "import io\n"
                "def run():\n"
                "    r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestDivide))\n"
                "    return r.wasSuccessful() and r.testsRun > 0\n"
                "def good(a, b):\n"
                "    if b == 0: raise ValueError('ноль')\n"
                "    return a / b\n"
                "def bad1(a, b):\n"
                "    if b == 0: return None\n"
                "    return a / b\n"
                "def bad2(a, b):\n"
                "    return a / b\n"
                "def bad3(a, b):\n"
                "    if b == 0: raise ValueError('ноль')\n"
                "    return a // b\n"
                "for name, f in [('верная', good), ('ошибка 1', bad1), ('ошибка 2', bad2), ('ошибка 3', bad3)]:\n"
                "    divide = f\n"
                "    print(name, 'тесты прошли' if run() else 'тесты упали')\n"
            ),
            "expected": ["верная тесты прошли", "ошибка 1 тесты упали", "ошибка 2 тесты упали", "ошибка 3 тесты упали"],
            "hint": "self.assertEqual(divide(7, 2), 3.5); with self.assertRaises(ValueError): divide(1, 0).",
        },
        {
            "id": "tests-for-fizzbuzz",
            "mode": "stdout",
            "title": "Тесты для fizzbuzz",
            "statement": (
                "Допишите класс TestFizz: тесты функции fizzbuzz(n): "
                "«FizzBuzz» для кратных 15, «Fizz» для кратных 3, «Buzz» для "
                "кратных 5, иначе число строкой. Ваши тесты должны пройти на "
                "верной реализации и упасть на трёх сломанных."
            ),
            "starter": "import unittest\n\n\nclass TestFizz(unittest.TestCase):\n    def test_example(self):\n        pass  # вызывайте fizzbuzz(n)\n",
            "driver": (
                "import io\n"
                "def run():\n"
                "    r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestFizz))\n"
                "    return r.wasSuccessful() and r.testsRun > 0\n"
                "def good(n):\n"
                "    if n % 15 == 0: return 'FizzBuzz'\n"
                "    if n % 3 == 0: return 'Fizz'\n"
                "    if n % 5 == 0: return 'Buzz'\n"
                "    return str(n)\n"
                "def bad1(n):\n"
                "    if n % 3 == 0: return 'Fizz'\n"
                "    if n % 5 == 0: return 'Buzz'\n"
                "    return str(n)\n"
                "def bad2(n):\n"
                "    if n % 15 == 0: return 'FizzBuzz'\n"
                "    if n % 3 == 0: return 'Fizz'\n"
                "    if n % 10 == 0: return 'Buzz'\n"
                "    return str(n)\n"
                "def bad3(n):\n"
                "    if n % 15 == 0: return 'FizzBuzz'\n"
                "    if n % 3 == 0: return 'Fizz'\n"
                "    if n % 5 == 0: return 'Buzz'\n"
                "    return n\n"
                "for name, f in [('верная', good), ('ошибка 1', bad1), ('ошибка 2', bad2), ('ошибка 3', bad3)]:\n"
                "    fizzbuzz = f\n"
                "    print(name, 'тесты прошли' if run() else 'тесты упали')\n"
            ),
            "expected": ["верная тесты прошли", "ошибка 1 тесты упали", "ошибка 2 тесты упали", "ошибка 3 тесты упали"],
            "hint": 'assertEqual(fizzbuzz(15), "FizzBuzz"), 9, 5, 10 (для Buzz — и нечётное, и чётное кратное), 7 → "7".',
        },
        {
            "id": "tests-for-stack",
            "mode": "stdout",
            "title": "Тесты для стека",
            "statement": (
                "Допишите класс TestStack: тесты класса Stack с методами "
                "push(x), pop() (снимает верхний; на пустом стеке — "
                "IndexError), peek() (верхний без снятия) и size(). Тесты "
                "должны пройти на верной реализации и упасть на трёх "
                "сломанных."
            ),
            "starter": "import unittest\n\n\nclass TestStack(unittest.TestCase):\n    def setUp(self):\n        self.s = Stack()\n\n    def test_example(self):\n        pass\n",
            "driver": (
                "import io\n"
                "def run():\n"
                "    r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestStack))\n"
                "    return r.wasSuccessful() and r.testsRun > 0\n"
                "class Good:\n"
                "    def __init__(self): self.a = []\n"
                "    def push(self, x): self.a.append(x)\n"
                "    def pop(self): return self.a.pop()\n"
                "    def peek(self): return self.a[-1]\n"
                "    def size(self): return len(self.a)\n"
                "class Bad1(Good):\n"
                "    def pop(self): return self.a.pop(0)\n"
                "class Bad2(Good):\n"
                "    def pop(self): return self.a.pop() if self.a else None\n"
                "class Bad3(Good):\n"
                "    def size(self): return len(self.a) + 1\n"
                "for name, c in [('верная', Good), ('ошибка 1', Bad1), ('ошибка 2', Bad2), ('ошибка 3', Bad3)]:\n"
                "    Stack = c\n"
                "    print(name, 'тесты прошли' if run() else 'тесты упали')\n"
            ),
            "expected": ["верная тесты прошли", "ошибка 1 тесты упали", "ошибка 2 тесты упали", "ошибка 3 тесты упали"],
            "hint": "Положите 1, 2, 3: pop() == 3, peek() == 2, size() == 2; на пустом: with self.assertRaises(IndexError): self.s.pop().",
        },
        {
            "id": "doctest-abs-diff",
            "mode": "stdout",
            "title": "Функция с doctest",
            "statement": (
                "Напишите функцию abs_diff(a, b) — модуль разности чисел — "
                "и снабдите её докстринг не менее чем тремя doctest-примерами "
                "(формат «>>> abs_diff(5, 8)» и ответ на следующей строке). "
                "Проверка выполнит ваши примеры."
            ),
            "starter": 'def abs_diff(a, b):\n    """Модуль разности.\n\n    Добавьте примеры в формате doctest.\n    """\n    pass\n',
            "driver": (
                "import doctest\n"
                "runner = doctest.DocTestRunner(verbose=False)\n"
                "for t in doctest.DocTestFinder().find(abs_diff, 'abs_diff', globs={'abs_diff': abs_diff}):\n"
                "    runner.run(t)\n"
                "res = runner.summarize(verbose=False)\n"
                "print(res.failed, res.attempted >= 3)\n"
                "print(abs_diff(5, 8), abs_diff(8, 5), abs_diff(2, 2))\n"
            ),
            "expected": ["0 True", "3 3 0"],
            "hint": '>>> abs_diff(5, 8)\\n    3 — каждый пример: строка с >>> и строка с ожидаемым результатом.',
        },
        {
            "id": "total-cost-mock",
            "mode": "stdout",
            "title": "Сумма через клиента",
            "statement": (
                "Напишите функцию total_cost(client, items): сумма цен всех "
                "товаров списка items; цену каждого возвращает "
                "client.get_price(item). Клиент передаётся параметром — так "
                "его можно подменить в тесте."
            ),
            "starter": "def total_cost(client, items):\n    pass\n",
            "driver": (
                "from unittest.mock import Mock, call\n"
                "m = Mock()\nm.get_price.side_effect = lambda item: {'а': 10, 'б': 25}[item]\n"
                "print(total_cost(m, ['а', 'б', 'а']))\n"
                "print(m.get_price.call_count, m.get_price.call_args_list == [call('а'), call('б'), call('а')])\n"
                "print(total_cost(Mock(), []))\n"
            ),
            "expected": ["45", "3 True", "0"],
            "hint": "sum(client.get_price(i) for i in items).",
        },
        {
            "id": "greeting-injected-time",
            "mode": "stdout",
            "title": "Время параметром",
            "statement": (
                "Напишите функцию greeting(now): now — объект datetime. До "
                "12 часов — «Доброе утро», с 12 до 18 — «Добрый день», "
                "позже — «Добрый вечер». Текущее время внутри не вызывайте."
            ),
            "starter": "def greeting(now):\n    pass\n",
            "driver": (
                "from datetime import datetime\n"
                "for h in (6, 11, 12, 17, 18, 23):\n    print(h, greeting(datetime(2024, 1, 1, h)))\n"
            ),
            "expected": ["6 Доброе утро", "11 Доброе утро", "12 Добрый день", "17 Добрый день", "18 Добрый вечер", "23 Добрый вечер"],
            "hint": "if now.hour < 12: ...; elif now.hour < 18: ...; else: ...",
        },
    ],
}
