"""Задачи главы 2"""

from app.exercises.algo_tasks._kept import KEPT

_NEW: dict[int, list[dict]] = {
    2: [
        {
            "id": "second-largest",
            "mode": "func",
            "func": "second_largest",
            "title": "Второй по величине",
            "statement": (
                "Напишите функцию second_largest(a): второе по величине РАЗЛИЧНОЕ "
                "значение списка. Если различных значений меньше двух, верните "
                "None. Достаточно одного прохода и двух переменных."
            ),
            "starter": "def second_largest(a):\n    pass\n",
            "tests": [
                {"args": [[4, 9, 2, 7, 5]], "expected": 7},
                {"args": [[5, 5, 5]], "expected": None},
                {"args": [[1, 2]], "expected": 1},
                {"args": [[-3, -1, -2]], "expected": -2},
                {"args": [[9, 9, 8]], "expected": 8},
                {"args": [[]], "expected": None},
                {"args": [[10]], "expected": None},
                {"args": [[3, 3, 2, 2, 1]], "expected": 2},
            ],
            "hint": "Держите first и second. Новый элемент больше first — старый first становится second; иначе он может претендовать только на second (и не равен first).",
        },
        {
            "id": "dyn-array-class",
            "mode": "stdout",
            "title": "Свой динамический массив",
            "statement": (
                "Реализуйте класс DynArray — динамический массив поверх списка "
                "ФИКСИРОВАННОЙ длины. Хранилище — список self._data, его длина "
                "равна ёмкости (свойство capacity), начальная ёмкость 1. append(x) "
                "пишет в свободную клетку, а когда места нет — создаёт новый список "
                "вдвое длиннее и копирует элементы. Также нужны: len(a), a[i] и "
                "a[i] = x (IndexError при индексе вне 0 … len−1), pop() (последний "
                "элемент, IndexError на пустом) и insert(i, x) для 0 ≤ i ≤ len со "
                "сдвигом вправо. Встроенные append/insert/pop списка для хранилища "
                "не используйте."
            ),
            "starter": "class DynArray:\n    def __init__(self):\n        self._data = [None]\n        self._len = 0\n\n    @property\n    def capacity(self):\n        return len(self._data)\n\n    def __len__(self):\n        return self._len\n\n    # __getitem__, __setitem__, append, pop, insert\n",
            "driver": (
                "a = DynArray()\n"
                "caps = []\n"
                "for i in range(1, 1001):\n"
                "    a.append(i * i)\n"
                "    if not caps or caps[-1] != a.capacity:\n"
                "        caps.append(a.capacity)\n"
                "print(len(a), caps)\n"
                "print(a[0], a[999], a[500])\n"
                "a[3] = -1\n"
                "print(a[3])\n"
                "a.insert(0, \"x\")\n"
                "a.insert(len(a), \"y\")\n"
                "a.insert(5, \"z\")\n"
                "print(len(a), a[0], a[5], a[len(a) - 1])\n"
                "print([a.pop() for _ in range(3)], len(a))\n"
                "for bad in (lambda: a[len(a)], lambda: a.insert(len(a) + 1, 0), lambda: DynArray().pop()):\n"
                "    try:\n"
                "        bad()\n"
                "        print(\"нет ошибки\")\n"
                "    except IndexError:\n"
                "        print(\"IndexError\")\n"
                "print(isinstance(a._data, list), len(a._data) == a.capacity)\n"
            ),
            "expected": ["1000 [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]", "1 1000000 251001", "-1", "1003 x z y", "['y', 1000000, 998001] 1000", "IndexError", "IndexError", "IndexError", "True True"],
            "hint": "append: if self._len == len(self._data): создайте new = [None] * (2 * len(self._data)), скопируйте циклом, подмените self._data. insert: append(None), затем сдвиг справа налево до позиции i.",
        },
        {
            "id": "remove-element",
            "mode": "stdout",
            "title": "Удалить значение на месте",
            "statement": (
                "Напишите функцию remove_element(a, x): уберите из списка a все "
                "вхождения x на месте, сохранив порядок остальных, и верните новую "
                "длину k — первые k элементов a после вызова должны быть "
                "оставшимися значениями (хвост неважен). Проверка подаёт 400 000 "
                "элементов, половина из которых равна x: многократный a.remove не "
                "успеет."
            ),
            "starter": "def remove_element(a, x):\n    pass\n",
            "driver": (
                "a = [3, 2, 2, 3, 4, 3, 5]\n"
                "k = remove_element(a, 3)\n"
                "print(k, a[:k])\n"
                "b = [1, 1, 1]\n"
                "k = remove_element(b, 1)\n"
                "print(k, b[:k])\n"
                "print(remove_element([], 5))\n"
                "big = [i % 2 for i in range(400000)]\n"
                "k = remove_element(big, 1)\n"
                "print(k, sum(big[:k]), big[:3])\n"
                "print(remove_element([7] * 400000, 7))\n"
            ),
            "expected": ["4 [2, 2, 4, 5]", "0 []", "0", "200000 0 [0, 0, 0]", "0"],
            "hint": "Два индекса: читающий идёт по всем элементам, пишущий k — по оставшимся. Если a[i] != x: a[k] = a[i]; k += 1.",
        },
        {
            "id": "move-zeroes",
            "mode": "stdout",
            "title": "Нули в конец",
            "statement": (
                "Напишите функцию move_zeroes(a): переставьте на месте все нули в "
                "конец списка, сохранив порядок остальных элементов. Возвращать "
                "ничего не нужно. Проверка подаёт миллион элементов, из них "
                "половина нулей в начале: pop и append в цикле не успеют."
            ),
            "starter": "def move_zeroes(a):\n    pass\n",
            "driver": (
                "a = [0, 1, 0, 3, 12]\n"
                "move_zeroes(a)\n"
                "print(a)\n"
                "b = [0, 0, 0]\n"
                "move_zeroes(b)\n"
                "print(b)\n"
                "c = [4, 5]\n"
                "move_zeroes(c)\n"
                "print(c)\n"
                "big = [0] * 500000 + [i + 1 for i in range(500000)]\n"
                "move_zeroes(big)\n"
                "print(big[:4], big[-3:], big.count(0), sum(big))\n"
            ),
            "expected": ["[1, 3, 12, 0, 0]", "[0, 0, 0]", "[4, 5]", "[1, 2, 3, 4] [0, 0, 0] 500000 125000250000"],
            "hint": "Индекс k — «следующее место для ненулевого». Идите по списку; встретили ненулевой — поменяйте его с a[k] и сдвиньте k.",
        },
        {
            "id": "merge-into-first",
            "mode": "stdout",
            "title": "Слияние в первый массив",
            "statement": (
                "Список a содержит m отсортированных элементов, а за ними — n "
                "свободных мест (нули). Список b — n отсортированных элементов. "
                "Напишите merge(a, m, b, n): влейте b в a так, чтобы a целиком стал "
                "отсортированным; ничего не возвращайте. Лишних списков не "
                "заводите, а вставки со сдвигом на 300 000 элементах не успеют."
            ),
            "starter": "def merge(a, m, b, n):\n    pass\n",
            "driver": (
                "a = [1, 3, 5, 0, 0, 0]\n"
                "merge(a, 3, [2, 4, 6], 3)\n"
                "print(a)\n"
                "a = [0, 0]\n"
                "merge(a, 0, [1, 2], 2)\n"
                "print(a)\n"
                "a = [4, 5, 6, 0, 0, 0]\n"
                "merge(a, 3, [1, 2, 3], 3)\n"
                "print(a)\n"
                "a = [1, 2]\n"
                "merge(a, 2, [], 0)\n"
                "print(a)\n"
                "n = 300000\n"
                "a = list(range(0, 2 * n, 2)) + [0] * n\n"
                "b = list(range(1, 2 * n, 2))\n"
                "merge(a, n, b, n)\n"
                "print(a[:6], a[-3:], a == list(range(2 * n)))\n"
            ),
            "expected": ["[1, 2, 3, 4, 5, 6]", "[1, 2]", "[1, 2, 3, 4, 5, 6]", "[1, 2]", "[0, 1, 2, 3, 4, 5] [599997, 599998, 599999] True"],
            "hint": "Пишите с конца: так большие значения встают на свои места, не затирая ещё не прочитанное. Три индекса: i в a, j в b, k — позиция записи.",
        },
        {
            "id": "range-sums-prefix",
            "mode": "stdout",
            "title": "Суммы на отрезках",
            "statement": (
                "Напишите функцию range_sums(a, queries): queries — список пар (l, "
                "r), для каждой верните сумму a[l..r] включительно; результат — "
                "список сумм в порядке запросов. Проверка: 300 000 элементов и 300 "
                "000 запросов, цикл по отрезку на каждый запрос не успеет — нужны "
                "префиксные суммы."
            ),
            "starter": "def range_sums(a, queries):\n    pass\n",
            "driver": (
                "print(range_sums([3, 1, 4, 1, 5, 9], [(0, 5), (2, 4), (3, 3), (1, 2)]))\n"
                "print(range_sums([-2, 5, -1], [(0, 0), (0, 2), (1, 2)]))\n"
                "n = 300000\n"
                "x = 12345\n"
                "a = []\n"
                "for i in range(n):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    a.append(x % 2001 - 1000)\n"
                "qs = []\n"
                "for i in range(300000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    l = x % n\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    r = l + x % (n - l)\n"
                "    qs.append((l, r))\n"
                "res = range_sums(a, qs)\n"
                "print(len(res), sum(res), res[0], res[-1])\n"
            ),
            "expected": ["[23, 10, 1, 5]", "[-2, 2, 4]", "300000 -14865874907 -141894 -125331"],
            "hint": "p[i] — сумма первых i элементов (p[0] = 0). Сумма a[l..r] = p[r + 1] − p[l].",
        },
        {
            "id": "pivot-index",
            "mode": "stdout",
            "title": "Точка равновесия",
            "statement": (
                "Напишите функцию pivot_index(a): наименьший индекс i, при котором "
                "сумма элементов левее i равна сумме элементов правее i (сам a[i] "
                "не считается). Если такого нет — −1. Для пустого списка — −1. "
                "Проверка подаёт 300 000 элементов: пересчёт сумм срезами на каждом "
                "шаге не успеет."
            ),
            "starter": "def pivot_index(a):\n    pass\n",
            "driver": (
                "print(pivot_index([1, 7, 3, 6, 5, 6]), pivot_index([1, 2, 3]), pivot_index([2, 1, -1]), pivot_index([]), pivot_index([5]))\n"
                "big = [1] * 200000 + [7] + [2] * 100000\n"
                "print(pivot_index(big))\n"
            ),
            "expected": ["3 -1 0 -1 0", "200000"],
            "hint": "Посчитайте total один раз. Идя слева, держите left; правая сумма = total − left − a[i].",
        },
        {
            "id": "product-except-self",
            "mode": "func",
            "func": "product_except_self",
            "title": "Произведение остальных",
            "statement": (
                "Напишите функцию product_except_self(a): список, где i-й элемент — "
                "произведение всех элементов a, кроме a[i]. Деление использовать "
                "нельзя (в данных бывают нули), нужно линейное время."
            ),
            "starter": "def product_except_self(a):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3, 4]], "expected": [24, 12, 8, 6]},
                {"args": [[0, 1, 2]], "expected": [2, 0, 0]},
                {"args": [[0, 0, 3]], "expected": [0, 0, 0]},
                {"args": [[5]], "expected": [1]},
                {"args": [[-1, 1, 0, -3, 3]], "expected": [0, 0, 9, 0, 0]},
                {"args": [[2, 3]], "expected": [3, 2]},
                {"args": [[]], "expected": []},
            ],
            "hint": "Два прохода: слева направо res[i] — произведение всего левее i; справа налево умножайте res[i] на произведение всего правее.",
        },
        {
            "id": "apply-range-updates",
            "mode": "stdout",
            "title": "Прибавления на отрезках",
            "statement": (
                "Напишите функцию apply_updates(n, updates): список из n нулей, к "
                "которому применены все команды (l, r, v) — «прибавить v ко всем "
                "элементам с l по r включительно». Проверка: 500 000 элементов и "
                "100 000 команд на длинных отрезках — цикл по отрезку не успеет, "
                "нужен разностный массив."
            ),
            "starter": "def apply_updates(n, updates):\n    pass\n",
            "driver": (
                "print(apply_updates(5, [(0, 1, 3), (1, 3, 2), (4, 4, 7)]))\n"
                "print(apply_updates(3, []))\n"
                "n = 500000\n"
                "x = 99\n"
                "ups = []\n"
                "for i in range(100000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    l = x % n\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    r = l + x % (n - l)\n"
                "    ups.append((l, r, x % 21 - 10))\n"
                "res = apply_updates(n, ups)\n"
                "print(len(res), sum(res), res[0], res[-1], max(res), min(res))\n"
            ),
            "expected": ["[3, 5, 2, 2, 7]", "[0, 0, 0]", "500000 199536968 0 24 2516 -1190"],
            "hint": "d[l] += v; d[r + 1] −= v (d длины n + 1). В конце накопление: cur += d[i], result[i] = cur.",
        },
        {
            "id": "matrix-transpose",
            "mode": "func",
            "func": "transpose",
            "title": "Транспонирование",
            "statement": (
                "Напишите функцию transpose(m): новая матрица, в которой строки и "
                "столбцы поменялись местами (m — прямоугольная, список списков; "
                "пустая матрица даёт пустую)."
            ),
            "starter": "def transpose(m):\n    pass\n",
            "tests": [
                {"args": [[[1, 2, 3], [4, 5, 6]]], "expected": [[1, 4], [2, 5], [3, 6]]},
                {"args": [[[1]]], "expected": [[1]]},
                {"args": [[[1, 2]]], "expected": [[1], [2]]},
                {"args": [[]], "expected": []},
                {"args": [[[1], [2], [3]]], "expected": [[1, 2, 3]]},
                {"args": [[[1, 2], [3, 4]]], "expected": [[1, 3], [2, 4]]},
            ],
            "hint": "Элемент (i, j) новой матрицы — это m[j][i]. Размеры меняются местами: было h × w, стало w × h.",
        },
        {
            "id": "rotate-matrix",
            "mode": "func",
            "func": "rotate_clockwise",
            "title": "Поворот матрицы",
            "statement": (
                "Напишите функцию rotate_clockwise(m): новая матрица — исходная, "
                "повёрнутая на 90 градусов по часовой стрелке. Пустая матрица даёт "
                "пустую. Подсказка: поворот — это транспонирование и разворот "
                "строк."
            ),
            "starter": "def rotate_clockwise(m):\n    pass\n",
            "tests": [
                {"args": [[[1, 2, 3], [4, 5, 6]]], "expected": [[4, 1], [5, 2], [6, 3]]},
                {"args": [[[1, 2], [3, 4]]], "expected": [[3, 1], [4, 2]]},
                {"args": [[[1]]], "expected": [[1]]},
                {"args": [[[1, 2, 3]]], "expected": [[1], [2], [3]]},
                {"args": [[]], "expected": []},
                {"args": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], "expected": [[7, 4, 1], [8, 5, 2], [9, 6, 3]]},
            ],
            "hint": "Первая строка повёрнутой матрицы — это первый столбец исходной, прочитанный снизу вверх: m[h−1−i][j].",
        },
        {
            "id": "spiral-order",
            "mode": "func",
            "func": "spiral",
            "title": "Обход по спирали",
            "statement": (
                "Напишите функцию spiral(m): элементы матрицы в порядке обхода по "
                "спирали по часовой стрелке, начиная с левого верхнего угла. "
                "Матрица прямоугольная и может быть пустой."
            ),
            "starter": "def spiral(m):\n    pass\n",
            "tests": [
                {"args": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], "expected": [1, 2, 3, 6, 9, 8, 7, 4, 5]},
                {"args": [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]], "expected": [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]},
                {"args": [[[1]]], "expected": [1]},
                {"args": [[[1, 2], [3, 4], [5, 6]]], "expected": [1, 2, 4, 6, 5, 3]},
                {"args": [[[1, 2, 3]]], "expected": [1, 2, 3]},
                {"args": [[[1], [2], [3]]], "expected": [1, 2, 3]},
                {"args": [[]], "expected": []},
            ],
            "hint": "Четыре границы top, bottom, left, right сужаются после каждого витка. Следите за случаями одной строки и одного столбца — иначе повторите элементы.",
        },
        {
            "id": "zero-rows-cols",
            "mode": "func",
            "func": "zero_rows_cols",
            "title": "Обнулить строки и столбцы",
            "statement": (
                "Напишите функцию zero_rows_cols(m): новая матрица, в которой "
                "каждая строка и каждый столбец, содержавшие в исходной матрице "
                "ноль, целиком заменены нулями. Нули, которые вы сами поставили, на "
                "другие строки не влияют."
            ),
            "starter": "def zero_rows_cols(m):\n    pass\n",
            "tests": [
                {"args": [[[1, 2, 3], [4, 0, 6], [7, 8, 9]]], "expected": [[1, 0, 3], [0, 0, 0], [7, 0, 9]]},
                {"args": [[[0, 1], [2, 3]]], "expected": [[0, 0], [0, 3]]},
                {"args": [[[1, 2], [3, 4]]], "expected": [[1, 2], [3, 4]]},
                {"args": [[[0]]], "expected": [[0]]},
                {"args": [[[1, 1, 1, 1], [1, 1, 0, 1]]], "expected": [[1, 1, 0, 1], [0, 0, 0, 0]]},
                {"args": [[]], "expected": []},
            ],
            "hint": "Сначала один обход — запомнить номера строк и столбцов с нулями; потом второй — построить результат.",
        },
        {
            "id": "is-anagram",
            "mode": "func",
            "func": "is_anagram",
            "title": "Анаграммы",
            "statement": (
                "Напишите функцию is_anagram(a, b): True, если строки состоят из "
                "одних и тех же символов в одинаковых количествах (регистр "
                "различается). Без сортировки: подсчитайте частоты за линейное "
                "время."
            ),
            "starter": "def is_anagram(a, b):\n    pass\n",
            "tests": [
                {"args": ["listen", "silent"], "expected": True},
                {"args": ["rat", "car"], "expected": False},
                {"args": ["a", "ab"], "expected": False},
                {"args": ["", ""], "expected": True},
                {"args": ["aab", "aba"], "expected": True},
                {"args": ["aab", "abb"], "expected": False},
                {"args": ["Привет", "тривеП"], "expected": True},
                {"args": ["Aa", "aa"], "expected": False},
            ],
            "hint": "Словарь счётчиков: по a прибавляем, по b вычитаем (и сразу сдаёмся, если счётчик ушёл в минус).",
        },
        {
            "id": "run-length-encode",
            "mode": "func",
            "func": "rle",
            "title": "Сжатие повторов",
            "statement": (
                "Напишите функцию rle(s): каждая группа одинаковых символов подряд "
                "заменяется символом и длиной группы, например 'aaabcc' → 'a3b1c2'. "
                "Пустая строка даёт пустую. Собирайте результат одним join, а не "
                "склеиванием в цикле."
            ),
            "starter": "def rle(s):\n    pass\n",
            "tests": [
                {"args": ["aaabcc"], "expected": "a3b1c2"},
                {"args": [""], "expected": ""},
                {"args": ["z"], "expected": "z1"},
                {"args": ["aabbbbaa"], "expected": "a2b4a2"},
                {"args": ["abc"], "expected": "a1b1c1"},
                {"args": ["xxxxxxxxxxxx"], "expected": "x12"},
            ],
            "hint": "Два индекса: i — начало группы, j бежит, пока символы совпадают. Куски кладите в список, в конце ''.join(...).",
        },
        {
            "id": "reverse-words",
            "mode": "func",
            "func": "reverse_words",
            "title": "Слова наоборот",
            "statement": (
                "Напишите функцию reverse_words(s): слова строки в обратном "
                "порядке, разделённые одним пробелом, без пробелов по краям. Лишние "
                "пробелы между словами в исходной строке схлопываются; строка из "
                "одних пробелов даёт пустую."
            ),
            "starter": "def reverse_words(s):\n    pass\n",
            "tests": [
                {"args": ["the sky is blue"], "expected": "blue is sky the"},
                {"args": ["  hello   world  "], "expected": "world hello"},
                {"args": ["one"], "expected": "one"},
                {"args": [""], "expected": ""},
                {"args": ["a b"], "expected": "b a"},
                {"args": ["   "], "expected": ""},
            ],
            "hint": "s.split() без аргументов сам убирает пустые куски; потом разворот списка и join через один пробел.",
        },
        {
            "id": "first-missing-positive",
            "mode": "func",
            "func": "first_missing_positive",
            "title": "Первое пропущенное положительное",
            "statement": (
                "Напишите функцию first_missing_positive(a): наименьшее целое "
                "положительное число, которого нет в списке a. Нужно линейное время "
                "и константная дополнительная память — можно переставлять элементы "
                "самого списка (его не нужно сохранять)."
            ),
            "starter": "def first_missing_positive(a):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 0]], "expected": 3},
                {"args": [[3, 4, -1, 1]], "expected": 2},
                {"args": [[7, 8, 9, 11, 12]], "expected": 1},
                {"args": [[1]], "expected": 2},
                {"args": [[]], "expected": 1},
                {"args": [[2, 1]], "expected": 3},
                {"args": [[1, 1, 2, 2]], "expected": 3},
                {"args": [[-5, 0]], "expected": 1},
                {"args": [[2, 2]], "expected": 1},
                {"args": [[4, 3, 2, 1]], "expected": 5},
            ],
            "hint": "Ответ лежит в диапазоне 1…n+1. Положите каждое значение v из 1…n на место v−1 обменами, затем найдите первую позицию, где a[i] != i+1.",
        },
    ],
}

_BY_ID = {t["id"]: t for t in _NEW[2]} | KEPT

TASKS: dict[int, list[dict]] = {
    2: [_BY_ID[i] for i in (
        "second-largest",
        "reverse-in-place",
        "rotate-right",
        "dyn-array-class",
        "remove-element",
        "move-zeroes",
        "merge-into-first",
        "range-sums-prefix",
        "pivot-index",
        "product-except-self",
        "apply-range-updates",
        "matrix-transpose",
        "rotate-matrix",
        "spiral-order",
        "zero-rows-cols",
        "is-anagram",
        "longest-common-prefix",
        "run-length-encode",
        "reverse-words",
        "first-missing-positive",
    )],
}
