-- Упражнения книги 7 «algo — Алгоритмы и структуры данных». Файл строит export_tasks.py — руками не правьте.

INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 1, 'has-duplicates', 0, 'stdout', 'Есть ли повторы за O(n)', 'Напишите функцию has_duplicates(nums): True, если в списке есть повторяющиеся числа. Решение должно работать за O(n) или O(n log n): проверка подаёт списки из 300 000 элементов, с вложенными циклами O(n²) вы в лимит времени не уложитесь.', 'def has_duplicates(nums):
    pass
', 'Заведите словарь или множество увиденных чисел: проверка «уже было» — O(1).', '{"driver": "print(has_duplicates([1, 2, 3, 1]), has_duplicates([]), has_duplicates([5]), has_duplicates([1, 2, 3]))\nbig = list(range(300000))\nprint(has_duplicates(big), has_duplicates(big + [7]))\n", "expected": ["True False False False", "False True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 1, 'fast-power', 1, 'stdout', 'Быстрое возведение в степень', 'Напишите функцию fast_power(base, exp): base в степени exp (exp — целое, 0 и больше), используя только умножение *. Алгоритм должен делать O(log exp) умножений: проверка считает, сколько раз вы умножали, и для exp = 1000 допускает не более 30. Для exp = 0 результат — 1.', 'def fast_power(base, exp):
    pass
', 'Двоичная запись показателя: на каждом шаге возводите base в квадрат, а если очередной бит единица — домножайте результат (или рекурсия: x^n = (x^(n/2))² и ещё один множитель при нечётном n).', '{"driver": "class M:\n    count = 0\n    def __init__(self, v):\n        self.v = v\n    def __mul__(self, o):\n        M.count += 1\n        return M(self.v * (o.v if isinstance(o, M) else o))\n    __rmul__ = __mul__\nr = fast_power(M(3), 20)\nprint(r.v == 3 ** 20, M.count <= 10)\nM.count = 0\nr = fast_power(M(2), 1000)\nprint(r.v == 2 ** 1000, M.count <= 30)\nprint(fast_power(5, 0), fast_power(2, 10), fast_power(7, 1))\n", "expected": ["True True", "True True", "1 1024 7"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 1, 'count-pairs-hash', 2, 'stdout', 'Пары с заданной суммой', 'Напишите функцию count_pairs(nums, target): сколько пар индексов i < j даёт nums[i] + nums[j] == target. Числа могут повторяться. Нужен линейный алгоритм: проверка подаёт 100 000 чисел.', 'def count_pairs(nums, target):
    pass
', 'Идите слева направо и храните в словаре, сколько раз уже встретилось каждое число; для x прибавляйте count[target - x].', '{"driver": "print(count_pairs([1, 2, 3, 4], 5), count_pairs([2, 2, 2], 4), count_pairs([], 1), count_pairs([5], 10))\nprint(count_pairs([1, 5, 1, 5], 6))\nbig = list(range(100000))\nprint(count_pairs(big, 100000), count_pairs(big, 1000000))\n", "expected": ["2 3 0 0", "4", "49999 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 1, 'max-subarray-kadane', 3, 'stdout', 'Лучший подотрезок', 'Напишите функцию max_subarray(nums): наибольшая сумма непрерывного непустого подотрезка списка. Список не пустой. Решение за один проход (алгоритм Кадане): проверка подаёт миллион чисел.', 'def max_subarray(nums):
    pass
', 'current = max(x, current + x); best = max(best, current) — «обрываем» отрезок, если хвост только мешает.', '{"driver": "print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), max_subarray([-3, -1, -2]), max_subarray([5]))\nprint(max_subarray([1] * 1000000), max_subarray([3, -1] * 500000))\n", "expected": ["6 -1 5", "1000000 1000001"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 1, 'power-of-two', 4, 'func', 'Степень двойки за O(1)', 'Напишите функцию is_power_of_two(n): True, если n — степень двойки (1, 2, 4, 8, …). Для n <= 0 — False. Без циклов: достаточно одной побитовой проверки.', 'def is_power_of_two(n):
    pass
', 'У степени двойки ровно один единичный бит: n & (n - 1) == 0.', '{"func": "is_power_of_two", "tests": [{"args": [1], "expected": true}, {"args": [64], "expected": true}, {"args": [6], "expected": false}, {"args": [0], "expected": false}, {"args": [-8], "expected": false}, {"args": [1267650600228229401496703205376], "expected": true}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 1, 'fib-linear', 5, 'stdout', 'Фибоначчи без экспоненты', 'Напишите функцию fib(n): n-е число Фибоначчи (fib(0) = 0, fib(1) = 1). Наивная рекурсия делает экспоненциально много вызовов, а проверка просит fib(300): нужен линейный алгоритм (цикл или запоминание).', 'def fib(n):
    pass
', 'Держите две последние величины: a, b = b, a + b — и n шагов.', '{"driver": "print(fib(0), fib(1), fib(10))\nprint(fib(90))\nprint(fib(300))\n", "expected": ["0 1 55", "2880067194370816120", "222232244629420445529739893461909967206666939096499764990979600"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 1, 'binary-search-steps', 6, 'func', 'Сколько шагов у двоичного поиска', 'Напишите функцию worst_case_steps(n): сколько сравнений понадобится двоичному поиску в худшем случае на отсортированном списке из n элементов (n >= 1). Делите n пополам (с отбрасыванием остатка), пока не останется 0, и считайте шаги: для 1 → 1, для 7 → 3, для 8 → 4.', 'def worst_case_steps(n):
    pass
', 'steps = 0; while n > 0: n //= 2; steps += 1 — это ровно длина двоичной записи числа.', '{"func": "worst_case_steps", "tests": [{"args": [1], "expected": 1}, {"args": [7], "expected": 3}, {"args": [8], "expected": 4}, {"args": [1000000], "expected": 20}, {"args": [1000000000000000000], "expected": 60}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'second-largest', 0, 'func', 'Второй по величине', 'Напишите функцию second_largest(a): второе по величине РАЗЛИЧНОЕ значение списка. Если различных значений меньше двух, верните None. Достаточно одного прохода и двух переменных.', 'def second_largest(a):
    pass
', 'Держите first и second. Новый элемент больше first — старый first становится second; иначе он может претендовать только на second (и не равен first).', '{"func": "second_largest", "tests": [{"args": [[4, 9, 2, 7, 5]], "expected": 7}, {"args": [[5, 5, 5]], "expected": null}, {"args": [[1, 2]], "expected": 1}, {"args": [[-3, -1, -2]], "expected": -2}, {"args": [[9, 9, 8]], "expected": 8}, {"args": [[]], "expected": null}, {"args": [[10]], "expected": null}, {"args": [[3, 3, 2, 2, 1]], "expected": 2}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'reverse-in-place', 1, 'stdout', 'Развернуть на месте', 'Напишите функцию reverse_in_place(arr): разворачивает список НА МЕСТЕ двумя указателями (один с начала, другой с конца, обмениваем и сближаем). Ничего не возвращает и не создаёт копий.', 'def reverse_in_place(arr):
    pass
', 'i, j = 0, len(arr) - 1; while i < j: arr[i], arr[j] = arr[j], arr[i]; i += 1; j -= 1.', '{"driver": "a = [1, 2, 3, 4, 5]\nr = reverse_in_place(a)\nprint(a, r)\nb = []\nreverse_in_place(b)\nprint(b)\nc = [''а'', ''б'']\nsame = c\nreverse_in_place(c)\nprint(same)\nbig = list(range(1000000))\nreverse_in_place(big)\nprint(big[0], big[-1])\n", "expected": ["[5, 4, 3, 2, 1] None", "[]", "[''б'', ''а'']", "999999 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'rotate-right', 2, 'stdout', 'Циклический сдвиг', 'Напишите функцию rotate_right(arr, k): сдвигает список вправо на k позиций по кругу НА МЕСТЕ (k может быть больше длины). Решение за O(n): проверка подаёт миллион элементов.', 'def rotate_right(arr, k):
    pass
', 'k %= n; затем три разворота: весь список, первые k, остальные — либо срез arr[:] = arr[-k:] + arr[:-k].', '{"driver": "a = [1, 2, 3, 4, 5, 6, 7]\nrotate_right(a, 3)\nprint(a)\nb = [1, 2, 3]\nrotate_right(b, 7)\nprint(b)\nc = []\nrotate_right(c, 2)\nprint(c)\nbig = list(range(1000000))\nrotate_right(big, 100000)\nprint(big[0], big[100000], big[-1])\n", "expected": ["[5, 6, 7, 1, 2, 3, 4]", "[3, 1, 2]", "[]", "900000 0 899999"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'dyn-array-class', 3, 'stdout', 'Свой динамический массив', 'Реализуйте класс DynArray — динамический массив поверх списка ФИКСИРОВАННОЙ длины. Хранилище — список self._data, его длина равна ёмкости (свойство capacity), начальная ёмкость 1. append(x) пишет в свободную клетку, а когда места нет — создаёт новый список вдвое длиннее и копирует элементы. Также нужны: len(a), a[i] и a[i] = x (IndexError при индексе вне 0 … len−1), pop() (последний элемент, IndexError на пустом) и insert(i, x) для 0 ≤ i ≤ len со сдвигом вправо. Встроенные append/insert/pop списка для хранилища не используйте.', 'class DynArray:
    def __init__(self):
        self._data = [None]
        self._len = 0

    @property
    def capacity(self):
        return len(self._data)

    def __len__(self):
        return self._len

    # __getitem__, __setitem__, append, pop, insert
', 'append: if self._len == len(self._data): создайте new = [None] * (2 * len(self._data)), скопируйте циклом, подмените self._data. insert: append(None), затем сдвиг справа налево до позиции i.', '{"driver": "a = DynArray()\ncaps = []\nfor i in range(1, 1001):\n    a.append(i * i)\n    if not caps or caps[-1] != a.capacity:\n        caps.append(a.capacity)\nprint(len(a), caps)\nprint(a[0], a[999], a[500])\na[3] = -1\nprint(a[3])\na.insert(0, \"x\")\na.insert(len(a), \"y\")\na.insert(5, \"z\")\nprint(len(a), a[0], a[5], a[len(a) - 1])\nprint([a.pop() for _ in range(3)], len(a))\nfor bad in (lambda: a[len(a)], lambda: a.insert(len(a) + 1, 0), lambda: DynArray().pop()):\n    try:\n        bad()\n        print(\"нет ошибки\")\n    except IndexError:\n        print(\"IndexError\")\nprint(isinstance(a._data, list), len(a._data) == a.capacity)\n", "expected": ["1000 [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]", "1 1000000 251001", "-1", "1003 x z y", "[''y'', 1000000, 998001] 1000", "IndexError", "IndexError", "IndexError", "True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'remove-element', 4, 'stdout', 'Удалить значение на месте', 'Напишите функцию remove_element(a, x): уберите из списка a все вхождения x на месте, сохранив порядок остальных, и верните новую длину k — первые k элементов a после вызова должны быть оставшимися значениями (хвост неважен). Проверка подаёт 400 000 элементов, половина из которых равна x: многократный a.remove не успеет.', 'def remove_element(a, x):
    pass
', 'Два индекса: читающий идёт по всем элементам, пишущий k — по оставшимся. Если a[i] != x: a[k] = a[i]; k += 1.', '{"driver": "a = [3, 2, 2, 3, 4, 3, 5]\nk = remove_element(a, 3)\nprint(k, a[:k])\nb = [1, 1, 1]\nk = remove_element(b, 1)\nprint(k, b[:k])\nprint(remove_element([], 5))\nbig = [i % 2 for i in range(400000)]\nk = remove_element(big, 1)\nprint(k, sum(big[:k]), big[:3])\nprint(remove_element([7] * 400000, 7))\n", "expected": ["4 [2, 2, 4, 5]", "0 []", "0", "200000 0 [0, 0, 0]", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'move-zeroes', 5, 'stdout', 'Нули в конец', 'Напишите функцию move_zeroes(a): переставьте на месте все нули в конец списка, сохранив порядок остальных элементов. Возвращать ничего не нужно. Проверка подаёт миллион элементов, из них половина нулей в начале: pop и append в цикле не успеют.', 'def move_zeroes(a):
    pass
', 'Индекс k — «следующее место для ненулевого». Идите по списку; встретили ненулевой — поменяйте его с a[k] и сдвиньте k.', '{"driver": "a = [0, 1, 0, 3, 12]\nmove_zeroes(a)\nprint(a)\nb = [0, 0, 0]\nmove_zeroes(b)\nprint(b)\nc = [4, 5]\nmove_zeroes(c)\nprint(c)\nbig = [0] * 500000 + [i + 1 for i in range(500000)]\nmove_zeroes(big)\nprint(big[:4], big[-3:], big.count(0), sum(big))\n", "expected": ["[1, 3, 12, 0, 0]", "[0, 0, 0]", "[4, 5]", "[1, 2, 3, 4] [0, 0, 0] 500000 125000250000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'merge-into-first', 6, 'stdout', 'Слияние в первый массив', 'Список a содержит m отсортированных элементов, а за ними — n свободных мест (нули). Список b — n отсортированных элементов. Напишите merge(a, m, b, n): влейте b в a так, чтобы a целиком стал отсортированным; ничего не возвращайте. Лишних списков не заводите, а вставки со сдвигом на 300 000 элементах не успеют.', 'def merge(a, m, b, n):
    pass
', 'Пишите с конца: так большие значения встают на свои места, не затирая ещё не прочитанное. Три индекса: i в a, j в b, k — позиция записи.', '{"driver": "a = [1, 3, 5, 0, 0, 0]\nmerge(a, 3, [2, 4, 6], 3)\nprint(a)\na = [0, 0]\nmerge(a, 0, [1, 2], 2)\nprint(a)\na = [4, 5, 6, 0, 0, 0]\nmerge(a, 3, [1, 2, 3], 3)\nprint(a)\na = [1, 2]\nmerge(a, 2, [], 0)\nprint(a)\nn = 300000\na = list(range(0, 2 * n, 2)) + [0] * n\nb = list(range(1, 2 * n, 2))\nmerge(a, n, b, n)\nprint(a[:6], a[-3:], a == list(range(2 * n)))\n", "expected": ["[1, 2, 3, 4, 5, 6]", "[1, 2]", "[1, 2, 3, 4, 5, 6]", "[1, 2]", "[0, 1, 2, 3, 4, 5] [599997, 599998, 599999] True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'range-sums-prefix', 7, 'stdout', 'Суммы на отрезках', 'Напишите функцию range_sums(a, queries): queries — список пар (l, r), для каждой верните сумму a[l..r] включительно; результат — список сумм в порядке запросов. Проверка: 300 000 элементов и 300 000 запросов, цикл по отрезку на каждый запрос не успеет — нужны префиксные суммы.', 'def range_sums(a, queries):
    pass
', 'p[i] — сумма первых i элементов (p[0] = 0). Сумма a[l..r] = p[r + 1] − p[l].', '{"driver": "print(range_sums([3, 1, 4, 1, 5, 9], [(0, 5), (2, 4), (3, 3), (1, 2)]))\nprint(range_sums([-2, 5, -1], [(0, 0), (0, 2), (1, 2)]))\nn = 300000\nx = 12345\na = []\nfor i in range(n):\n    x = (x * 1103515245 + 12345) % 2147483648\n    a.append(x % 2001 - 1000)\nqs = []\nfor i in range(300000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    l = x % n\n    x = (x * 1103515245 + 12345) % 2147483648\n    r = l + x % (n - l)\n    qs.append((l, r))\nres = range_sums(a, qs)\nprint(len(res), sum(res), res[0], res[-1])\n", "expected": ["[23, 10, 1, 5]", "[-2, 2, 4]", "300000 -14865874907 -141894 -125331"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'pivot-index', 8, 'stdout', 'Точка равновесия', 'Напишите функцию pivot_index(a): наименьший индекс i, при котором сумма элементов левее i равна сумме элементов правее i (сам a[i] не считается). Если такого нет — −1. Для пустого списка — −1. Проверка подаёт 300 000 элементов: пересчёт сумм срезами на каждом шаге не успеет.', 'def pivot_index(a):
    pass
', 'Посчитайте total один раз. Идя слева, держите left; правая сумма = total − left − a[i].', '{"driver": "print(pivot_index([1, 7, 3, 6, 5, 6]), pivot_index([1, 2, 3]), pivot_index([2, 1, -1]), pivot_index([]), pivot_index([5]))\nbig = [1] * 200000 + [7] + [2] * 100000\nprint(pivot_index(big))\n", "expected": ["3 -1 0 -1 0", "200000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'product-except-self', 9, 'func', 'Произведение остальных', 'Напишите функцию product_except_self(a): список, где i-й элемент — произведение всех элементов a, кроме a[i]. Деление использовать нельзя (в данных бывают нули), нужно линейное время.', 'def product_except_self(a):
    pass
', 'Два прохода: слева направо res[i] — произведение всего левее i; справа налево умножайте res[i] на произведение всего правее.', '{"func": "product_except_self", "tests": [{"args": [[1, 2, 3, 4]], "expected": [24, 12, 8, 6]}, {"args": [[0, 1, 2]], "expected": [2, 0, 0]}, {"args": [[0, 0, 3]], "expected": [0, 0, 0]}, {"args": [[5]], "expected": [1]}, {"args": [[-1, 1, 0, -3, 3]], "expected": [0, 0, 9, 0, 0]}, {"args": [[2, 3]], "expected": [3, 2]}, {"args": [[]], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'apply-range-updates', 10, 'stdout', 'Прибавления на отрезках', 'Напишите функцию apply_updates(n, updates): список из n нулей, к которому применены все команды (l, r, v) — «прибавить v ко всем элементам с l по r включительно». Проверка: 500 000 элементов и 100 000 команд на длинных отрезках — цикл по отрезку не успеет, нужен разностный массив.', 'def apply_updates(n, updates):
    pass
', 'd[l] += v; d[r + 1] −= v (d длины n + 1). В конце накопление: cur += d[i], result[i] = cur.', '{"driver": "print(apply_updates(5, [(0, 1, 3), (1, 3, 2), (4, 4, 7)]))\nprint(apply_updates(3, []))\nn = 500000\nx = 99\nups = []\nfor i in range(100000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    l = x % n\n    x = (x * 1103515245 + 12345) % 2147483648\n    r = l + x % (n - l)\n    ups.append((l, r, x % 21 - 10))\nres = apply_updates(n, ups)\nprint(len(res), sum(res), res[0], res[-1], max(res), min(res))\n", "expected": ["[3, 5, 2, 2, 7]", "[0, 0, 0]", "500000 199536968 0 24 2516 -1190"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'matrix-transpose', 11, 'func', 'Транспонирование', 'Напишите функцию transpose(m): новая матрица, в которой строки и столбцы поменялись местами (m — прямоугольная, список списков; пустая матрица даёт пустую).', 'def transpose(m):
    pass
', 'Элемент (i, j) новой матрицы — это m[j][i]. Размеры меняются местами: было h × w, стало w × h.', '{"func": "transpose", "tests": [{"args": [[[1, 2, 3], [4, 5, 6]]], "expected": [[1, 4], [2, 5], [3, 6]]}, {"args": [[[1]]], "expected": [[1]]}, {"args": [[[1, 2]]], "expected": [[1], [2]]}, {"args": [[]], "expected": []}, {"args": [[[1], [2], [3]]], "expected": [[1, 2, 3]]}, {"args": [[[1, 2], [3, 4]]], "expected": [[1, 3], [2, 4]]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'rotate-matrix', 12, 'func', 'Поворот матрицы', 'Напишите функцию rotate_clockwise(m): новая матрица — исходная, повёрнутая на 90 градусов по часовой стрелке. Пустая матрица даёт пустую. Подсказка: поворот — это транспонирование и разворот строк.', 'def rotate_clockwise(m):
    pass
', 'Первая строка повёрнутой матрицы — это первый столбец исходной, прочитанный снизу вверх: m[h−1−i][j].', '{"func": "rotate_clockwise", "tests": [{"args": [[[1, 2, 3], [4, 5, 6]]], "expected": [[4, 1], [5, 2], [6, 3]]}, {"args": [[[1, 2], [3, 4]]], "expected": [[3, 1], [4, 2]]}, {"args": [[[1]]], "expected": [[1]]}, {"args": [[[1, 2, 3]]], "expected": [[1], [2], [3]]}, {"args": [[]], "expected": []}, {"args": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], "expected": [[7, 4, 1], [8, 5, 2], [9, 6, 3]]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'spiral-order', 13, 'func', 'Обход по спирали', 'Напишите функцию spiral(m): элементы матрицы в порядке обхода по спирали по часовой стрелке, начиная с левого верхнего угла. Матрица прямоугольная и может быть пустой.', 'def spiral(m):
    pass
', 'Четыре границы top, bottom, left, right сужаются после каждого витка. Следите за случаями одной строки и одного столбца — иначе повторите элементы.', '{"func": "spiral", "tests": [{"args": [[[1, 2, 3], [4, 5, 6], [7, 8, 9]]], "expected": [1, 2, 3, 6, 9, 8, 7, 4, 5]}, {"args": [[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]], "expected": [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]}, {"args": [[[1]]], "expected": [1]}, {"args": [[[1, 2], [3, 4], [5, 6]]], "expected": [1, 2, 4, 6, 5, 3]}, {"args": [[[1, 2, 3]]], "expected": [1, 2, 3]}, {"args": [[[1], [2], [3]]], "expected": [1, 2, 3]}, {"args": [[]], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'zero-rows-cols', 14, 'func', 'Обнулить строки и столбцы', 'Напишите функцию zero_rows_cols(m): новая матрица, в которой каждая строка и каждый столбец, содержавшие в исходной матрице ноль, целиком заменены нулями. Нули, которые вы сами поставили, на другие строки не влияют.', 'def zero_rows_cols(m):
    pass
', 'Сначала один обход — запомнить номера строк и столбцов с нулями; потом второй — построить результат.', '{"func": "zero_rows_cols", "tests": [{"args": [[[1, 2, 3], [4, 0, 6], [7, 8, 9]]], "expected": [[1, 0, 3], [0, 0, 0], [7, 0, 9]]}, {"args": [[[0, 1], [2, 3]]], "expected": [[0, 0], [0, 3]]}, {"args": [[[1, 2], [3, 4]]], "expected": [[1, 2], [3, 4]]}, {"args": [[[0]]], "expected": [[0]]}, {"args": [[[1, 1, 1, 1], [1, 1, 0, 1]]], "expected": [[1, 1, 0, 1], [0, 0, 0, 0]]}, {"args": [[]], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'is-anagram', 15, 'func', 'Анаграммы', 'Напишите функцию is_anagram(a, b): True, если строки состоят из одних и тех же символов в одинаковых количествах (регистр различается). Без сортировки: подсчитайте частоты за линейное время.', 'def is_anagram(a, b):
    pass
', 'Словарь счётчиков: по a прибавляем, по b вычитаем (и сразу сдаёмся, если счётчик ушёл в минус).', '{"func": "is_anagram", "tests": [{"args": ["listen", "silent"], "expected": true}, {"args": ["rat", "car"], "expected": false}, {"args": ["a", "ab"], "expected": false}, {"args": ["", ""], "expected": true}, {"args": ["aab", "aba"], "expected": true}, {"args": ["aab", "abb"], "expected": false}, {"args": ["Привет", "тривеП"], "expected": true}, {"args": ["Aa", "aa"], "expected": false}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'longest-common-prefix', 16, 'func', 'Общий префикс', 'Напишите функцию common_prefix(words): самая длинная общая начальная часть всех слов списка (пустая строка, если её нет или список пуст).', 'def common_prefix(words):
    pass
', 'Берите первое слово как кандидата и укорачивайте, пока каждое слово не начнётся с него (startswith).', '{"func": "common_prefix", "tests": [{"args": [["цветок", "цвет", "цветной"]], "expected": "цвет"}, {"args": [["собака", "гоночная", "машина"]], "expected": ""}, {"args": [["одно"]], "expected": "одно"}, {"args": [[]], "expected": ""}, {"args": [["аб", "аб", "аб"]], "expected": "аб"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'run-length-encode', 17, 'func', 'Сжатие повторов', 'Напишите функцию rle(s): каждая группа одинаковых символов подряд заменяется символом и длиной группы, например ''aaabcc'' → ''a3b1c2''. Пустая строка даёт пустую. Собирайте результат одним join, а не склеиванием в цикле.', 'def rle(s):
    pass
', 'Два индекса: i — начало группы, j бежит, пока символы совпадают. Куски кладите в список, в конце ''''.join(...).', '{"func": "rle", "tests": [{"args": ["aaabcc"], "expected": "a3b1c2"}, {"args": [""], "expected": ""}, {"args": ["z"], "expected": "z1"}, {"args": ["aabbbbaa"], "expected": "a2b4a2"}, {"args": ["abc"], "expected": "a1b1c1"}, {"args": ["xxxxxxxxxxxx"], "expected": "x12"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'reverse-words', 18, 'func', 'Слова наоборот', 'Напишите функцию reverse_words(s): слова строки в обратном порядке, разделённые одним пробелом, без пробелов по краям. Лишние пробелы между словами в исходной строке схлопываются; строка из одних пробелов даёт пустую.', 'def reverse_words(s):
    pass
', 's.split() без аргументов сам убирает пустые куски; потом разворот списка и join через один пробел.', '{"func": "reverse_words", "tests": [{"args": ["the sky is blue"], "expected": "blue is sky the"}, {"args": ["  hello   world  "], "expected": "world hello"}, {"args": ["one"], "expected": "one"}, {"args": [""], "expected": ""}, {"args": ["a b"], "expected": "b a"}, {"args": ["   "], "expected": ""}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 2, 'first-missing-positive', 19, 'func', 'Первое пропущенное положительное', 'Напишите функцию first_missing_positive(a): наименьшее целое положительное число, которого нет в списке a. Нужно линейное время и константная дополнительная память — можно переставлять элементы самого списка (его не нужно сохранять).', 'def first_missing_positive(a):
    pass
', 'Ответ лежит в диапазоне 1…n+1. Положите каждое значение v из 1…n на место v−1 обменами, затем найдите первую позицию, где a[i] != i+1.', '{"func": "first_missing_positive", "tests": [{"args": [[1, 2, 0]], "expected": 3}, {"args": [[3, 4, -1, 1]], "expected": 2}, {"args": [[7, 8, 9, 11, 12]], "expected": 1}, {"args": [[1]], "expected": 2}, {"args": [[]], "expected": 1}, {"args": [[2, 1]], "expected": 3}, {"args": [[1, 1, 2, 2]], "expected": 3}, {"args": [[-5, 0]], "expected": 1}, {"args": [[2, 2]], "expected": 1}, {"args": [[4, 3, 2, 1]], "expected": 5}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'll-length-sum', 0, 'stdout', 'Длина и сумма', 'Дан класс ListNode (val, next). Напишите функцию length_and_sum(head): кортеж (количество узлов, сумма значений). Для пустого списка (head — None) — (0, 0).', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def length_and_sum(head):
    pass
', 'Один цикл: while head: счётчики и head = head.next.', '{"driver": "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n\n\ndef to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\n\n\nprint(length_and_sum(build([3, 1, 4])), length_and_sum(None), length_and_sum(build(list(range(100000)))))\n", "expected": ["(3, 8) (0, 0) (100000, 4999950000)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'll-singly-class', 1, 'stdout', 'Свой односвязный список', 'Реализуйте класс SinglyLinkedList на узлах Node (val, next): поля head и tail, методы push_front(x), push_back(x) за O(1) (нужен указатель на хвост), pop_front() (значение первого узла; IndexError, если пусто), find(x) (индекс первого вхождения или −1), remove(x) (удалить первое вхождение; True/False) и to_list(); len(s) — число узлов. Следите за tail при удалении последнего узла и при опустошении списка. Проверка кладёт в хвост 200 000 элементов — без tail не успеть.', 'class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._n = 0

    def __len__(self):
        return self._n

    # push_front, push_back, pop_front, find, remove, to_list
', 'push_back: если tail None — голова и хвост это новый узел, иначе tail.next = node; tail = node. В remove хранимый prev нужен и для обычного удаления, и для обновления tail.', '{"driver": "s = SinglyLinkedList()\ns.push_back(1)\ns.push_back(2)\ns.push_front(0)\ns.push_back(3)\nprint(s.to_list(), len(s), s.find(2), s.find(9))\nprint(s.remove(0), s.remove(3), s.remove(7), s.to_list())\ns.push_back(5)\nprint(s.to_list(), s.pop_front(), s.pop_front(), s.pop_front(), len(s))\ntry:\n    s.pop_front()\nexcept IndexError:\n    print(\"IndexError\")\ns.push_back(8)\nprint(s.to_list())\nbig = SinglyLinkedList()\nfor i in range(200000):\n    big.push_back(i)\nprint(len(big), big.find(199999), big.pop_front())\n", "expected": ["[0, 1, 2, 3] 4 2 -1", "True True False [1, 2]", "[1, 2, 5] 1 2 5 0", "IndexError", "[8]", "200000 199999 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'reverse-linked-list', 2, 'stdout', 'Развернуть связный список', 'Дан класс ListNode (val, next). Напишите функцию reverse_list(head): разворачивает односвязный список, переставляя ссылки next, и возвращает новую голову. Без создания новых узлов и без рекурсии (в списке бывает 100 000 узлов).', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_list(head):
    pass
', 'prev = None; пока head: nxt = head.next; head.next = prev; prev = head; head = nxt; вернуть prev.', '{"driver": "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\ndef to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\nprint(to_list(reverse_list(build([1, 2, 3, 4]))), to_list(reverse_list(build([7]))), to_list(reverse_list(None)))\nr = reverse_list(build(list(range(100000))))\nprint(r.val, to_list(r)[-1])\n", "expected": ["[4, 3, 2, 1] [7] []", "99999 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'middle-node', 3, 'stdout', 'Середина списка', 'Дан класс ListNode. Напишите функцию middle(head): значение среднего узла за ОДИН проход (медленный и быстрый указатели). Для списка чётной длины — второй из двух средних.', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def middle(head):
    pass
', 'slow = fast = head; while fast and fast.next: slow = slow.next; fast = fast.next.next.', '{"driver": "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\nprint(middle(build([1, 2, 3, 4, 5])), middle(build([1, 2, 3, 4])), middle(build([9])))\nprint(middle(build(list(range(1000001)))))\n", "expected": ["3 3 9", "500000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'has-cycle', 4, 'stdout', 'Есть ли цикл', 'Дан класс ListNode. Напишите функцию has_cycle(head): True, если по ссылкам next можно ходить бесконечно (в списке есть цикл). Алгоритм Флойда: два указателя с разной скоростью, O(1) памяти.', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def has_cycle(head):
    pass
', 'slow сдвигайте на 1, fast на 2; если они встретились — цикл есть, если fast упёрся в None — нет.', '{"driver": "def build(n):\n    nodes = [ListNode(i) for i in range(n)]\n    for a, b in zip(nodes, nodes[1:]):\n        a.next = b\n    return nodes\nprint(has_cycle(None), has_cycle(ListNode(1)))\nns = build(5)\nprint(has_cycle(ns[0]))\nns[4].next = ns[2]\nprint(has_cycle(ns[0]))\none = ListNode(1)\none.next = one\nprint(has_cycle(one))\nbig = build(200000)\nprint(has_cycle(big[0]))\nbig[-1].next = big[0]\nprint(has_cycle(big[0]))\n", "expected": ["False False", "False", "True", "True", "False", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'cycle-start', 5, 'stdout', 'Где начинается цикл', 'Дан класс ListNode. Напишите функцию detect_cycle(head): узел, с которого начинается цикл, или None, если цикла нет. Память — O(1), алгоритм Флойда в два этапа (встреча, затем один указатель — в голову).', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def detect_cycle(head):
    pass
', 'Первый цикл — как в has_cycle; при slow is fast поставьте slow = head и двигайте оба по одному шагу, пока не совпадут.', '{"driver": "def make(n, pos):\n    nodes = [ListNode(i) for i in range(n)]\n    for a, b in zip(nodes, nodes[1:]):\n        a.next = b\n    if pos >= 0:\n        nodes[-1].next = nodes[pos]\n    return nodes[0] if nodes else None\n\n\nprint(detect_cycle(make(5, 2)).val)\nprint(detect_cycle(make(5, -1)), detect_cycle(None))\nprint(detect_cycle(make(1, 0)).val)\nprint(detect_cycle(make(300000, 1234)).val)\n", "expected": ["2", "None None", "0", "1234"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'remove-nth-from-end', 6, 'stdout', 'Удалить n-й с конца', 'Дан класс ListNode. Напишите функцию remove_nth_from_end(head, n): удалите n-й узел с конца (n = 1 — последний) и верните голову. За один проход: два указателя на расстоянии n друг от друга. Удалять можно и саму голову — поможет дозорный узел.', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def remove_nth_from_end(head, n):
    pass
', 'dummy → head. fast уходит на n шагов вперёд, затем fast и slow идут вместе до конца; slow.next = slow.next.next.', '{"driver": "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n\n\ndef to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\n\n\nprint(to_list(remove_nth_from_end(build([1, 2, 3, 4, 5]), 2)))\nprint(to_list(remove_nth_from_end(build([1]), 1)))\nprint(to_list(remove_nth_from_end(build([1, 2]), 2)), to_list(remove_nth_from_end(build([1, 2]), 1)))\nr = to_list(remove_nth_from_end(build(list(range(500000))), 250000))\nprint(len(r), r[249999], r[250000])\n", "expected": ["[1, 2, 3, 5]", "[]", "[2] [1]", "499999 249999 250001"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'merge-sorted-lists', 7, 'stdout', 'Слить два отсортированных списка', 'Дан класс ListNode. Напишите функцию merge_lists(a, b): сливает два отсортированных по возрастанию связных списка в один отсортированный, переиспользуя узлы, и возвращает голову. Время O(n + m), без рекурсии.', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_lists(a, b):
    pass
', 'Фиктивный узел dummy и указатель tail: на каждом шаге присоединяйте меньший из двух текущих узлов.', '{"driver": "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\ndef to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\nprint(to_list(merge_lists(build([1, 3, 5]), build([2, 4, 6]))))\nprint(to_list(merge_lists(build([]), build([1, 2]))), to_list(merge_lists(build([1]), build([]))))\nprint(to_list(merge_lists(build([1, 1, 2]), build([1, 3]))))\nm = to_list(merge_lists(build(list(range(0, 200000, 2))), build(list(range(1, 200000, 2)))))\nprint(m == list(range(200000)))\n", "expected": ["[1, 2, 3, 4, 5, 6]", "[1, 2] [1]", "[1, 1, 1, 2, 3]", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'delete-duplicates-sorted', 8, 'stdout', 'Дубликаты в отсортированном списке', 'Дан класс ListNode. Список отсортирован. Напишите функцию delete_duplicates(head): оставьте в списке по одному узлу каждого значения (первый), верните голову. Новых узлов не создавайте.', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def delete_duplicates(head):
    pass
', 'Пока есть cur.next: если значения равны — перепрыгните лишний узел (cur.next = cur.next.next), иначе шагните вперёд.', '{"driver": "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n\n\ndef to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\n\n\nprint(to_list(delete_duplicates(build([1, 1, 2, 3, 3]))), to_list(delete_duplicates(None)), to_list(delete_duplicates(build([1, 1, 1]))))\nr = to_list(delete_duplicates(build([i // 3 for i in range(300000)])))\nprint(len(r), r[-1])\n", "expected": ["[1, 2, 3] [] [1]", "100000 99999"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'remove-all-value', 9, 'stdout', 'Удалить все значения', 'Дан класс ListNode. Напишите функцию remove_value(head, val): удалите из списка все узлы со значением val и верните новую голову. Голова тоже может подлежать удалению — используйте дозорный узел.', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def remove_value(head, val):
    pass
', 'prev = dummy; пока prev.next: если prev.next.val == val — prev.next = prev.next.next (prev стоит), иначе prev = prev.next.', '{"driver": "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n\n\ndef to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\n\n\nprint(to_list(remove_value(build([1, 2, 6, 3, 4, 5, 6]), 6)), to_list(remove_value(build([7, 7, 7]), 7)))\nprint(to_list(remove_value(build([1, 2]), 3)), to_list(remove_value(build([6, 1]), 6)), to_list(remove_value(None, 1)))\nprint(to_list(remove_value(build([1] * 200000), 1)))\n", "expected": ["[1, 2, 3, 4, 5] []", "[1, 2] [1] []", "[]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'palindrome-list', 10, 'stdout', 'Палиндром в списке', 'Дан класс ListNode. Напишите функцию is_palindrome_list(head): True, если значения читаются одинаково в обе стороны. Пустой список и список из одного узла — палиндромы. Лучшее решение — O(1) дополнительной памяти: найдите середину, разверните вторую половину и сравните половины.', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def is_palindrome_list(head):
    pass
', 'Быстрый и медленный указатели находят середину; разверните вторую половину (как в reverse_list) и идите двумя указателями с краёв.', '{"driver": "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n\n\ndef to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\n\n\nprint(is_palindrome_list(build([1, 2, 2, 1])), is_palindrome_list(build([1, 2, 3, 2, 1])), is_palindrome_list(build([1, 2])))\nprint(is_palindrome_list(build([1])), is_palindrome_list(None))\nhalf = list(range(400000))\nprint(is_palindrome_list(build(half + [5] + half[::-1])), is_palindrome_list(build(half + [5, 6] + half[::-1])))\n", "expected": ["True True False", "True True", "True False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'add-two-numbers', 11, 'stdout', 'Сложение чисел в списках', 'Дан класс ListNode. Два неотрицательных числа записаны списками цифр в обратном порядке (младшая цифра — в голове). Напишите функцию add_two_numbers(a, b): список с суммой в том же виде. Сложение в столбик: цифры и перенос. Цифры в каждом числе — без ведущих нулей, кроме самого числа 0.', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def add_two_numbers(a, b):
    pass
', 'Цикл идёт, пока есть хотя бы одно из: узел в a, узел в b, перенос. Цифра суммы — s % 10, новый перенос — s // 10.', '{"driver": "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n\n\ndef to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\n\n\nprint(to_list(add_two_numbers(build([2, 4, 3]), build([5, 6, 4]))))\nprint(to_list(add_two_numbers(build([0]), build([0]))), to_list(add_two_numbers(build([5]), build([5]))))\nprint(to_list(add_two_numbers(build([9, 9, 9, 9]), build([1]))))\nr = to_list(add_two_numbers(build([9] * 100000), build([1])))\nprint(len(r), r[0], r[-1])\n", "expected": ["[7, 0, 8]", "[0] [0, 1]", "[0, 0, 0, 0, 1]", "100001 0 1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'partition-list', 12, 'stdout', 'Разбиение списка', 'Дан класс ListNode и число x. Напишите функцию partition(head, x): переставьте узлы так, чтобы сначала шли все узлы со значением меньше x, потом все остальные; порядок внутри каждой группы сохраняется. Верните голову. Две цепочки с дозорными и их склейка.', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def partition(head, x):
    pass
', 'Две цепочки (меньшие и остальные), у каждой свой дозорный. Не забудьте обнулить хвост второй цепочки: b.next = None.', '{"driver": "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n\n\ndef to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\n\n\nprint(to_list(partition(build([1, 4, 3, 2, 5, 2]), 3)), to_list(partition(build([2, 1]), 2)), to_list(partition(None, 1)))\nprint(to_list(partition(build([3, 3]), 3)), to_list(partition(build([1, 2, 3]), 5)))\nr = to_list(partition(build([i % 7 for i in range(300000)]), 3))\nprint(len(r), r[:5], r[-3:], sum(1 for v in r if v < 3))\n", "expected": ["[1, 2, 2, 4, 3, 5] [1, 2] []", "[3, 3] [1, 2, 3]", "300000 [0, 1, 2, 0, 1] [4, 5, 6] 128572"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'reorder-list', 13, 'stdout', 'Переупорядочить список', 'Дан класс ListNode. Напишите функцию reorder(head): перестройте список L0 → L1 → … → Ln в порядок L0 → Ln → L1 → Ln−1 → L2 → … на месте, без изменения значений узлов. Возвращать ничего не нужно. Середина, разворот второй половины, чередующееся слияние.', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reorder(head):
    pass
', 'Три шага: найти середину и отрезать вторую половину; развернуть её; затем по очереди брать узел из первой и из второй половины.', '{"driver": "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n\n\ndef to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\n\n\nfor vals in ([1, 2, 3, 4], [1, 2, 3, 4, 5], [1], [], [1, 2]):\n    h = build(vals)\n    reorder(h)\n    print(to_list(h))\nh = build(list(range(200000)))\nreorder(h)\nr = to_list(h)\nprint(len(r), r[:6], sum(r))\n", "expected": ["[1, 4, 2, 3]", "[1, 5, 2, 4, 3]", "[1]", "[]", "[1, 2]", "200000 [0, 199999, 1, 199998, 2, 199997] 19999900000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'sort-list', 14, 'stdout', 'Сортировка списка слиянием', 'Дан класс ListNode. Напишите функцию sort_list(head): отсортируйте список по возрастанию и верните голову — сортировкой слиянием, перестановкой ссылок: значения в узлах менять нельзя (проверка следит, что у каждого узла осталось его значение). Время O(n log n); проверка подаёт 100 000 узлов.', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def sort_list(head):
    pass
', 'Середина быстрым и медленным указателями, slow.next = None разрезает список; рекурсивно сортируем половины и сливаем (как merge_two_lists).', '{"driver": "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n\n\ndef to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\n\n\nprint(to_list(sort_list(build([4, 2, 1, 3]))), to_list(sort_list(build([-1, 5, 3, 4, 0]))), to_list(sort_list(None)), to_list(sort_list(build([2, 2, 1]))))\nx = 7\nvals = []\nfor _ in range(100000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    vals.append(x % 1000)\nh = build(vals)\nnodes = []\nc = h\nwhile c:\n    nodes.append((id(c), c.val))\n    c = c.next\nr = sort_list(h)\nout, after = [], []\nwhile r:\n    out.append(r.val)\n    after.append((id(r), r.val))\n    r = r.next\nprint(out == sorted(vals), set(after) == set(nodes))\n", "expected": ["[1, 2, 3, 4] [-1, 0, 3, 4, 5] [] [1, 2, 2]", "True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'list-intersection', 15, 'stdout', 'Пересечение списков', 'Дан класс ListNode. Два списка могут сходиться в общий хвост (это один и тот же узел, а не узлы с равными значениями). Напишите функцию get_intersection(a, b): первый общий узел или None. O(n + m) времени и O(1) памяти. Проверка: списки по сотням тысяч узлов, вложенные циклы не успеют.', 'class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def get_intersection(a, b):
    pass
', 'Хитрость: каждый указатель, дойдя до конца, перескакивает на голову другого списка. Через n + m шагов они либо встретятся в общем узле, либо оба станут None.', '{"driver": "def chain(vals, tail=None):\n    head = tail\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n\n\ncommon = chain([8, 4, 5])\na = chain([4, 1], common)\nb = chain([5, 6, 1], common)\nprint(get_intersection(a, b).val)\nprint(get_intersection(chain([1, 2]), chain([3])), get_intersection(None, a), get_intersection(a, a).val)\ncommon = chain(list(range(400000)))\na = chain(list(range(100000)), common)\nb = chain([7], common)\nr = get_intersection(a, b)\nprint(r is common, r.val)\n", "expected": ["8", "None None 4", "True 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'doubly-linked-class', 16, 'stdout', 'Свой двусвязный список', 'Реализуйте класс DoublyLinkedList на узлах DNode (val, prev, next) с двумя дозорными head и tail: push_front(x) и push_back(x) (возвращают созданный узел-«ручку»), pop_front() и pop_back() (значение; IndexError, если пусто), remove(node) — удалить узел по ручке за O(1), move_to_front(node), len(d), обход for v in d (от головы к хвосту) и reversed_values() (список значений от хвоста к голове). Проверка удаляет 100 000 узлов по ручкам: поиск по значению не успеет.', 'class DNode:
    def __init__(self, val=None):
        self.val = val
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = DNode()
        self.tail = DNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self._n = 0

    def __len__(self):
        return self._n

    # push_front, push_back, pop_front, pop_back, remove, move_to_front, __iter__, reversed_values
', 'С дозорными вставка и удаление одинаковы для всех узлов: _insert_after(left, node) и remove(node) — по четыре присваивания. move_to_front = вырезать узел и вставить после head.', '{"driver": "d = DoublyLinkedList()\na = d.push_back(1)\nb = d.push_back(2)\nc = d.push_back(3)\nz = d.push_front(0)\nprint(list(d), d.reversed_values(), len(d))\nd.remove(b)\nprint(list(d), d.reversed_values())\nd.move_to_front(c)\nprint(list(d), len(d))\nprint(d.pop_front(), d.pop_back(), list(d), len(d))\nprint(d.pop_front(), len(d))\ntry:\n    d.pop_back()\nexcept IndexError:\n    print(\"IndexError\")\nd.push_back(5)\nprint(list(d), d.reversed_values())\nbig = DoublyLinkedList()\nhs = [big.push_back(i) for i in range(200000)]\nfor h in hs[::2]:\n    big.remove(h)\nprint(len(big), next(iter(big)), big.reversed_values()[0], sum(big))\n", "expected": ["[0, 1, 2, 3] [3, 2, 1, 0] 4", "[0, 1, 3] [3, 1, 0]", "[3, 0, 1] 3", "3 1 [0] 1", "0 0", "IndexError", "[5] [5]", "100000 1 199999 10000000000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'circular-queue', 17, 'stdout', 'Циклическая очередь', 'Реализуйте класс CircularQueue(k) — очередь фиксированной ёмкости k на массиве (кольцевой буфер): enqueue(x) — True, если место было, иначе False; dequeue() — True, если было что снять, иначе False; front() и rear() — первый и последний элемент или −1, если очередь пуста; is_empty() и is_full(). Хранилище — список длины k, который не растёт; индексы идут по кругу.', 'class CircularQueue:
    def __init__(self, k):
        self.a = [None] * k
        self.head = 0
        self.size = 0

    # enqueue, dequeue, front, rear, is_empty, is_full
', 'head — индекс первого элемента, size — сколько занято. Место для записи: (head + size) % k. Счётчик size отличает пустую очередь от полной.', '{"driver": "q = CircularQueue(3)\nprint(q.enqueue(1), q.enqueue(2), q.enqueue(3), q.enqueue(4))\nprint(q.rear(), q.is_full(), q.dequeue(), q.enqueue(4), q.rear(), q.front())\nprint(q.dequeue(), q.dequeue(), q.dequeue(), q.dequeue(), q.is_empty(), q.front(), q.rear())\nq = CircularQueue(5)\ntotal = 0\nfor i in range(300000):\n    q.enqueue(i)\n    if i % 3 != 0:\n        total += q.front()\n        q.dequeue()\nprint(total, q.front(), q.rear(), q.is_full(), len(q.a))\n", "expected": ["True True True False", "3 True True True 4 2", "True True True False True -1 -1", "29998700036 299994 299999 False 5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'queue-two-stacks', 18, 'stdout', 'Очередь из двух стопок', 'Реализуйте класс MyQueue на двух списках-стопках (разрешены только append и pop() с конца): push(x), pop() (первый элемент, IndexError на пустой), peek() (посмотреть первый, IndexError на пустой) и empty(). Снятие должно стоить амортизированную константу: переливайте из входной стопки в выходную только когда выходная пуста.', 'class MyQueue:
    def __init__(self):
        self.inp = []
        self.out = []

    # push, pop, peek, empty
', 'Входная стопка принимает push. Когда нужно снять, а выходная пуста — переложите всё из входной в выходную: порядок перевернётся, самый старый окажется сверху.', '{"driver": "q = MyQueue()\nq.push(1)\nq.push(2)\nprint(q.peek(), q.pop(), q.empty())\nq.push(3)\nprint(q.pop(), q.pop(), q.empty())\ntry:\n    q.pop()\nexcept IndexError:\n    print(\"IndexError\")\nq = MyQueue()\ntotal = 0\nfor i in range(300000):\n    q.push(i)\n    if i % 2:\n        total += q.pop()\nwhile not q.empty():\n    total += q.pop()\nprint(total)\n", "expected": ["1 1 False", "2 3 True", "IndexError", "44999850000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 3, 'min-stack', 19, 'stdout', 'Стек с минимумом', 'Реализуйте класс MinStack: push(x), pop() (значение; IndexError на пустом), top() и get_min() — минимальный элемент стека за O(1) (IndexError на пустом). Подумайте, что хранить рядом с каждым элементом.', 'class MinStack:
    def __init__(self):
        self.items = []

    # push, pop, top, get_min
', 'Вместе со значением кладите в стопку минимум «на этот момент»: m = min(x, предыдущий минимум). get_min — минимум на вершине.', '{"driver": "s = MinStack()\nfor v in (5, 3, 7, 3, 8):\n    s.push(v)\nprint(s.get_min(), s.top())\nprint(s.pop(), s.get_min(), s.pop(), s.get_min(), s.pop(), s.get_min(), s.pop(), s.get_min())\ntry:\n    MinStack().get_min()\nexcept IndexError:\n    print(\"IndexError\")\ns = MinStack()\nacc = 0\nfor i in range(300000):\n    s.push((i * 7919) % 10007)\n    acc += s.get_min()\nfor _ in range(300000):\n    acc -= s.get_min()\n    s.pop()\nprint(acc)\n", "expected": ["3 8", "8 3 3 3 7 3 3 5", "IndexError", "0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 4, 'binary-search-count', 0, 'stdout', 'Двоичный поиск', 'Напишите функцию binary_search(arr, target): индекс target в отсортированном по возрастанию списке или -1. Проверка считает обращения к элементам: на списке из миллиона элементов вы вправе сделать не больше 25 обращений — линейный перебор не пройдёт.', 'def binary_search(arr, target):
    pass
', 'lo, hi = 0, len(arr) - 1; mid = (lo + hi) // 2; сравните arr[mid] один раз за шаг (положите в переменную!) и отбросьте половину.', '{"driver": "class CL(list):\n    reads = 0\n    def __getitem__(self, i):\n        CL.reads += 1\n        return list.__getitem__(self, i)\nprint(binary_search([1, 3, 5, 7, 9], 7), binary_search([1, 3, 5], 4), binary_search([], 1), binary_search([2], 2))\narr = CL(range(0, 2000000, 2))\nCL.reads = 0\nx = binary_search(arr, 1234568)\nr1 = CL.reads\nCL.reads = 0\ny = binary_search(arr, 7)\nr2 = CL.reads\nprint(x, y, r1 <= 25 and r2 <= 25)\n", "expected": ["3 -1 -1 0", "617284 -1 True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 4, 'lower-bound', 1, 'stdout', 'Первая позиция не меньше x', 'Напишите функцию lower_bound(arr, x): индекс первого элемента отсортированного списка, который больше или равен x (len(arr), если такого нет). За O(log n): проверка считает обращения (не больше 25 на миллионе).', 'def lower_bound(arr, x):
    pass
', 'lo, hi = 0, len(arr); пока lo < hi: mid = (lo + hi) // 2; если arr[mid] < x: lo = mid + 1, иначе hi = mid.', '{"driver": "class CL(list):\n    reads = 0\n    def __getitem__(self, i):\n        CL.reads += 1\n        return list.__getitem__(self, i)\nprint(lower_bound([1, 2, 2, 2, 5], 2), lower_bound([1, 2, 5], 3), lower_bound([1, 2, 5], 9), lower_bound([1, 2, 5], 0), lower_bound([], 1))\narr = CL(range(1000000))\nprint(lower_bound(arr, 777777), CL.reads <= 25)\n", "expected": ["1 2 3 0 0", "777777 True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 4, 'search-rotated', 2, 'stdout', 'Поиск в повёрнутом массиве', 'Отсортированный список без повторов циклически сдвинули: [4, 5, 6, 7, 0, 1, 2]. Напишите функцию search_rotated(arr, target): индекс target или -1 за O(log n) (проверка допускает не более 60 обращений на миллионе элементов).', 'def search_rotated(arr, target):
    pass
', 'На каждом шаге одна из половин [lo, mid] или [mid, hi] обязательно отсортирована: определите её и решите, лежит ли target внутри.', '{"driver": "class CL(list):\n    reads = 0\n    def __getitem__(self, i):\n        CL.reads += 1\n        return list.__getitem__(self, i)\na = [4, 5, 6, 7, 0, 1, 2]\nprint([search_rotated(a, x) for x in (0, 4, 7, 2, 3)], search_rotated([], 1), search_rotated([1], 1))\nn = 1000000\nbig = CL(list(range(300000, n)) + list(range(300000)))\nCL.reads = 0\nx = search_rotated(big, 5)\nr1 = CL.reads\nCL.reads = 0\ny = search_rotated(big, 999999)\nr2 = CL.reads\nprint(x, y, r1 <= 60 and r2 <= 60)\n", "expected": ["[4, 0, 3, 6, -1] -1 0", "700005 699999 True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 4, 'merge-sort-impl', 3, 'stdout', 'Сортировка слиянием', 'Напишите функцию merge_sort(arr): возвращает НОВЫЙ отсортированный список (исходный не меняйте), сортировка слиянием за O(n log n), устойчивая. Встроенные sorted и sort использовать нельзя: проверка подаёт 100 000 чисел и пары (число, метка) для проверки устойчивости.', 'def merge_sort(arr):
    pass
', 'Разделите пополам, отсортируйте половины рекурсивно, слейте двумя указателями (при равных берите из ЛЕВОЙ половины — так сортировка устойчива).', '{"driver": "import random\nrandom.seed(3)\nprint(merge_sort([5, 2, 9, 1, 5, 6]), merge_sort([]), merge_sort([1]))\na = [(2, ''а''), (1, ''б''), (2, ''в''), (1, ''г'')]\nprint(merge_sort(a))\nprint(a)\nbig = [random.randint(0, 10 ** 6) for _ in range(100000)]\nr = merge_sort(big)\nprint(r == sorted(big), len(r))\n", "expected": ["[1, 2, 5, 5, 6, 9] [] [1]", "[(1, ''б''), (1, ''г''), (2, ''а''), (2, ''в'')]", "[(2, ''а''), (1, ''б''), (2, ''в''), (1, ''г'')]", "True 100000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 4, 'quick-sort-impl', 4, 'stdout', 'Быстрая сортировка', 'Напишите функцию quick_sort(arr): сортирует список НА МЕСТЕ быстрой сортировкой. Проверка подаёт случайные данные, уже отсортированный список и 100 000 одинаковых элементов — наивный выбор опорного (первый/последний) и деление без учёта равных дадут O(n²) и не уложатся по времени.', 'def quick_sort(arr):
    pass
', 'Случайный опорный; разделение на три части: меньше, равные, больше (трёхстороннее) — тогда одинаковые элементы не вызывают деградации.', '{"driver": "import random, sys\nsys.setrecursionlimit(10000)\nrandom.seed(5)\na = [3, 6, 1, 8, 2, 9, 2]\nquick_sort(a)\nprint(a)\nb = []\nquick_sort(b)\nprint(b)\nr = [random.randint(0, 10 ** 6) for _ in range(100000)]\nexp = sorted(r)\nquick_sort(r)\nprint(r == exp)\ns = list(range(100000))\nquick_sort(s)\nprint(s == list(range(100000)))\ne = [7] * 100000\nquick_sort(e)\nprint(e == [7] * 100000)\n", "expected": ["[1, 2, 2, 3, 6, 8, 9]", "[]", "True", "True", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 4, 'counting-sort-impl', 5, 'stdout', 'Сортировка подсчётом', 'Напишите функцию counting_sort(nums, max_value): сортирует целые числа от 0 до max_value за O(n + k), где k = max_value + 1. Возвращает новый список. Проверка подаёт миллион чисел с max_value = 100.', 'def counting_sort(nums, max_value):
    pass
', 'counts = [0] * (max_value + 1); посчитайте вхождения; затем выпишите каждое значение v ровно counts[v] раз.', '{"driver": "import random\nrandom.seed(1)\nprint(counting_sort([3, 0, 2, 3, 1, 0], 3), counting_sort([], 5), counting_sort([4], 4))\nbig = [random.randint(0, 100) for _ in range(1000000)]\nr = counting_sort(big, 100)\nprint(r == sorted(big), len(r))\n", "expected": ["[0, 0, 1, 2, 3, 3] [] [4]", "True 1000000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 4, 'kth-largest', 6, 'func', 'k-й по величине', 'Напишите функцию kth_largest(nums, k): k-й по величине элемент списка (k = 1 — наибольший); одинаковые значения считаются отдельными элементами. 1 <= k <= len(nums). Подойдёт куча (heapq) или быстрый выбор.', 'import heapq


def kth_largest(nums, k):
    pass
', 'heapq.nlargest(k, nums)[-1], либо куча размера k: храните k наибольших, наименьший из них — ответ.', '{"func": "kth_largest", "tests": [{"args": [[3, 2, 1, 5, 6, 4], 2], "expected": 5}, {"args": [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], "expected": 4}, {"args": [[7], 1], "expected": 7}, {"args": [[1, 1, 1], 3], "expected": 1}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 4, 'sort-stable-two-keys', 7, 'func', 'Устойчивая сортировка по двум ключам', 'Напишите функцию sort_students(students): students — список пар [имя, оценка]. Верните их по убыванию оценки; у равных оценок порядок остаётся таким, как во входном списке (устойчивость). Важно: ключ ровно один — оценка.', 'def sort_students(students):
    pass
', 'sorted(students, key=lambda s: s[1], reverse=True) — устойчивость сохраняется и с reverse.', '{"func": "sort_students", "tests": [{"args": [[["Аня", 4], ["Боря", 5], ["Вера", 4], ["Гоша", 5]]], "expected": [["Боря", 5], ["Гоша", 5], ["Аня", 4], ["Вера", 4]]}, {"args": [[]], "expected": []}, {"args": [[["Я", 3]]], "expected": [["Я", 3]]}, {"args": [[["б", 1], ["а", 1]]], "expected": [["б", 1], ["а", 1]]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'poly-string-hash', 0, 'func', 'Полиномиальный хеш строки', 'Напишите функцию poly_hash(s, base, mod): хеш строки по схеме h = 0; для каждого символа h = (h * base + ord(символ)) % mod. Пустая строка даёт 0.', 'def poly_hash(s, base, mod):
    pass
', 'Один цикл по символам; остаток берите на каждом шаге — число остаётся небольшим.', '{"func": "poly_hash", "tests": [{"args": ["abc", 31, 1000000007], "expected": 96354}, {"args": ["", 31, 997], "expected": 0}, {"args": ["a", 31, 2], "expected": 1}, {"args": ["hello", 31, 1000000007], "expected": 99162322}, {"args": ["abc", 31, 100], "expected": 54}, {"args": ["яблоко", 257, 1000003], "expected": 286210}, {"args": ["ba", 31, 1000000007], "expected": 3135}, {"args": ["ab", 31, 1000000007], "expected": 3105}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'window-hashes', 1, 'stdout', 'Хеши всех окон', 'Напишите функцию window_hashes(s, k, base, mod): список полиномиальных хешей (h = h * base + ord(символ), по модулю mod) всех подстрок длины k слева направо. Для k больше длины строки — пустой список. Хеш следующего окна считайте из предыдущего за O(1) (скользящий хеш): проверка подаёт 500 000 символов и окно из 1000.', 'def window_hashes(s, k, base, mod):
    pass
', 'Хеш окна — многочлен: вычитаем вклад ушедшего символа ord(s[i-k]) * base**(k-1), умножаем на base и прибавляем код нового. Степень посчитайте один раз: pow(base, k-1, mod).', '{"driver": "print(window_hashes(\"abcab\", 2, 31, 1000000007))\nprint(window_hashes(\"abc\", 5, 31, 1000000007), window_hashes(\"abc\", 3, 31, 1000000007))\ntext = \"\".join(chr(97 + (i * i + 3 * i) % 26) for i in range(500000))\nhs = window_hashes(text, 1000, 257, 1000000007)\nprint(len(hs), hs[0], hs[-1], sum(hs) % 1000000007)\n", "expected": ["[3105, 3137, 3166, 3105]", "[] [96354]", "499001 792260583 281438055 700002660"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'int-hash-spread', 2, 'func', 'Деление или умножение', 'Напишите функцию max_bucket(keys, m, method): разложите целые ключи по m ячейкам и верните размер самой заполненной. method = ''division'' — номер ключа key % m; method = ''multiplication'' — ((key * 2654435769) % 4294967296) * m // 4294967296 (константа — 2³² / золотое сечение).', 'def max_bucket(keys, m, method):
    pass
', 'Заведите список счётчиков длины m; для каждого ключа вычислите номер выбранным способом и прибавьте единицу. Ответ — max(счётчики).', '{"func": "max_bucket", "tests": [{"args": [[0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120], 8, "division"], "expected": 16}, {"args": [[0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120], 8, "multiplication"], "expected": 3}, {"args": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99], 10, "division"], "expected": 10}, {"args": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99], 10, "multiplication"], "expected": 11}, {"args": [[0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000, 101000, 102000, 103000, 104000, 105000, 106000, 107000, 108000, 109000, 110000, 111000, 112000, 113000, 114000, 115000, 116000, 117000, 118000, 119000, 120000, 121000, 122000, 123000, 124000, 125000, 126000, 127000, 128000, 129000, 130000, 131000, 132000, 133000, 134000, 135000, 136000, 137000, 138000, 139000, 140000, 141000, 142000, 143000, 144000, 145000, 146000, 147000, 148000, 149000, 150000, 151000, 152000, 153000, 154000, 155000, 156000, 157000, 158000, 159000, 160000, 161000, 162000, 163000, 164000, 165000, 166000, 167000, 168000, 169000, 170000, 171000, 172000, 173000, 174000, 175000, 176000, 177000, 178000, 179000, 180000, 181000, 182000, 183000, 184000, 185000, 186000, 187000, 188000, 189000, 190000, 191000, 192000, 193000, 194000, 195000, 196000, 197000, 198000, 199000, 200000, 201000, 202000, 203000, 204000, 205000, 206000, 207000, 208000, 209000, 210000, 211000, 212000, 213000, 214000, 215000, 216000, 217000, 218000, 219000, 220000, 221000, 222000, 223000, 224000, 225000, 226000, 227000, 228000, 229000, 230000, 231000, 232000, 233000, 234000, 235000, 236000, 237000, 238000, 239000, 240000, 241000, 242000, 243000, 244000, 245000, 246000, 247000, 248000, 249000, 250000, 251000, 252000, 253000, 254000, 255000, 256000, 257000, 258000, 259000, 260000, 261000, 262000, 263000, 264000, 265000, 266000, 267000, 268000, 269000, 270000, 271000, 272000, 273000, 274000, 275000, 276000, 277000, 278000, 279000, 280000, 281000, 282000, 283000, 284000, 285000, 286000, 287000, 288000, 289000, 290000, 291000, 292000, 293000, 294000, 295000, 296000, 297000, 298000, 299000, 300000, 301000, 302000, 303000, 304000, 305000, 306000, 307000, 308000, 309000, 310000, 311000, 312000, 313000, 314000, 315000, 316000, 317000, 318000, 319000, 320000, 321000, 322000, 323000, 324000, 325000, 326000, 327000, 328000, 329000, 330000, 331000, 332000, 333000, 334000, 335000, 336000, 337000, 338000, 339000, 340000, 341000, 342000, 343000, 344000, 345000, 346000, 347000, 348000, 349000, 350000, 351000, 352000, 353000, 354000, 355000, 356000, 357000, 358000, 359000, 360000, 361000, 362000, 363000, 364000, 365000, 366000, 367000, 368000, 369000, 370000, 371000, 372000, 373000, 374000, 375000, 376000, 377000, 378000, 379000, 380000, 381000, 382000, 383000, 384000, 385000, 386000, 387000, 388000, 389000, 390000, 391000, 392000, 393000, 394000, 395000, 396000, 397000, 398000, 399000, 400000, 401000, 402000, 403000, 404000, 405000, 406000, 407000, 408000, 409000, 410000, 411000, 412000, 413000, 414000, 415000, 416000, 417000, 418000, 419000, 420000, 421000, 422000, 423000, 424000, 425000, 426000, 427000, 428000, 429000, 430000, 431000, 432000, 433000, 434000, 435000, 436000, 437000, 438000, 439000, 440000, 441000, 442000, 443000, 444000, 445000, 446000, 447000, 448000, 449000, 450000, 451000, 452000, 453000, 454000, 455000, 456000, 457000, 458000, 459000, 460000, 461000, 462000, 463000, 464000, 465000, 466000, 467000, 468000, 469000, 470000, 471000, 472000, 473000, 474000, 475000, 476000, 477000, 478000, 479000, 480000, 481000, 482000, 483000, 484000, 485000, 486000, 487000, 488000, 489000, 490000, 491000, 492000, 493000, 494000, 495000, 496000, 497000, 498000, 499000], 1000, "division"], "expected": 500}, {"args": [[0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000, 40000, 41000, 42000, 43000, 44000, 45000, 46000, 47000, 48000, 49000, 50000, 51000, 52000, 53000, 54000, 55000, 56000, 57000, 58000, 59000, 60000, 61000, 62000, 63000, 64000, 65000, 66000, 67000, 68000, 69000, 70000, 71000, 72000, 73000, 74000, 75000, 76000, 77000, 78000, 79000, 80000, 81000, 82000, 83000, 84000, 85000, 86000, 87000, 88000, 89000, 90000, 91000, 92000, 93000, 94000, 95000, 96000, 97000, 98000, 99000, 100000, 101000, 102000, 103000, 104000, 105000, 106000, 107000, 108000, 109000, 110000, 111000, 112000, 113000, 114000, 115000, 116000, 117000, 118000, 119000, 120000, 121000, 122000, 123000, 124000, 125000, 126000, 127000, 128000, 129000, 130000, 131000, 132000, 133000, 134000, 135000, 136000, 137000, 138000, 139000, 140000, 141000, 142000, 143000, 144000, 145000, 146000, 147000, 148000, 149000, 150000, 151000, 152000, 153000, 154000, 155000, 156000, 157000, 158000, 159000, 160000, 161000, 162000, 163000, 164000, 165000, 166000, 167000, 168000, 169000, 170000, 171000, 172000, 173000, 174000, 175000, 176000, 177000, 178000, 179000, 180000, 181000, 182000, 183000, 184000, 185000, 186000, 187000, 188000, 189000, 190000, 191000, 192000, 193000, 194000, 195000, 196000, 197000, 198000, 199000, 200000, 201000, 202000, 203000, 204000, 205000, 206000, 207000, 208000, 209000, 210000, 211000, 212000, 213000, 214000, 215000, 216000, 217000, 218000, 219000, 220000, 221000, 222000, 223000, 224000, 225000, 226000, 227000, 228000, 229000, 230000, 231000, 232000, 233000, 234000, 235000, 236000, 237000, 238000, 239000, 240000, 241000, 242000, 243000, 244000, 245000, 246000, 247000, 248000, 249000, 250000, 251000, 252000, 253000, 254000, 255000, 256000, 257000, 258000, 259000, 260000, 261000, 262000, 263000, 264000, 265000, 266000, 267000, 268000, 269000, 270000, 271000, 272000, 273000, 274000, 275000, 276000, 277000, 278000, 279000, 280000, 281000, 282000, 283000, 284000, 285000, 286000, 287000, 288000, 289000, 290000, 291000, 292000, 293000, 294000, 295000, 296000, 297000, 298000, 299000, 300000, 301000, 302000, 303000, 304000, 305000, 306000, 307000, 308000, 309000, 310000, 311000, 312000, 313000, 314000, 315000, 316000, 317000, 318000, 319000, 320000, 321000, 322000, 323000, 324000, 325000, 326000, 327000, 328000, 329000, 330000, 331000, 332000, 333000, 334000, 335000, 336000, 337000, 338000, 339000, 340000, 341000, 342000, 343000, 344000, 345000, 346000, 347000, 348000, 349000, 350000, 351000, 352000, 353000, 354000, 355000, 356000, 357000, 358000, 359000, 360000, 361000, 362000, 363000, 364000, 365000, 366000, 367000, 368000, 369000, 370000, 371000, 372000, 373000, 374000, 375000, 376000, 377000, 378000, 379000, 380000, 381000, 382000, 383000, 384000, 385000, 386000, 387000, 388000, 389000, 390000, 391000, 392000, 393000, 394000, 395000, 396000, 397000, 398000, 399000, 400000, 401000, 402000, 403000, 404000, 405000, 406000, 407000, 408000, 409000, 410000, 411000, 412000, 413000, 414000, 415000, 416000, 417000, 418000, 419000, 420000, 421000, 422000, 423000, 424000, 425000, 426000, 427000, 428000, 429000, 430000, 431000, 432000, 433000, 434000, 435000, 436000, 437000, 438000, 439000, 440000, 441000, 442000, 443000, 444000, 445000, 446000, 447000, 448000, 449000, 450000, 451000, 452000, 453000, 454000, 455000, 456000, 457000, 458000, 459000, 460000, 461000, 462000, 463000, 464000, 465000, 466000, 467000, 468000, 469000, 470000, 471000, 472000, 473000, 474000, 475000, 476000, 477000, 478000, 479000, 480000, 481000, 482000, 483000, 484000, 485000, 486000, 487000, 488000, 489000, 490000, 491000, 492000, 493000, 494000, 495000, 496000, 497000, 498000, 499000], 1000, "multiplication"], "expected": 1}, {"args": [[], 4, "division"], "expected": 0}, {"args": [[5], 4, "multiplication"], "expected": 1}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'chained-hashmap', 3, 'stdout', 'Хеш-таблица с цепочками', 'Реализуйте класс ChainedHashMap(capacity=8, hash_fn=None) — таблицу с цепочками. Корзины — список списков пар [ключ, значение]; номер корзины hash_fn(key) % capacity (по умолчанию hash). Методы: put(key, value) (новый ключ — в конец цепочки, существующий — обновить), get(key, default=None), remove(key) → True/False, key in m, len(m), keys(), свойство capacity и max_chain() — длина самой длинной цепочки. Рост: после вставки НОВОГО ключа, если len(m) > 0.75 * capacity, вдвое увеличьте число корзин и вставьте все пары заново (перебирая старые корзины по порядку, цепочки — слева направо).', 'class ChainedHashMap:
    def __init__(self, capacity=8, hash_fn=None):
        self.hash_fn = hash_fn or hash
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0

    @property
    def capacity(self):
        return len(self.buckets)

    def __len__(self):
        return self.size

    # put, get, remove, __contains__, keys, max_chain
', 'Рост: соберите все пары, создайте вдвое больше пустых корзин и вставьте пары заново (без повторной проверки роста), иначе порядок и размер разойдутся с эталоном.', '{"driver": "m = ChainedHashMap(4, hash_fn=lambda k: k)\nfor k in (1, 5, 9, 2):\n    m.put(k, k * 10)\nprint(m.capacity, len(m), m.max_chain(), m.keys())\nm.put(5, 55)\nprint(m.get(5), m.get(7), m.get(7, \"нет\"), 9 in m, 3 in m)\nprint(m.remove(9), m.remove(9), len(m), m.keys())\nm.put(3, 30)\nprint(m.capacity, m.keys())\ncaps = []\nbig = ChainedHashMap()\nfor i in range(2000):\n    big.put((\"k\", i), i)\n    if not caps or caps[-1] != big.capacity:\n        caps.append(big.capacity)\nprint(caps, len(big), big.get((\"k\", 1999)), big.max_chain() < 12)\nbad = ChainedHashMap(8, hash_fn=lambda k: 0)\nfor i in range(300):\n    bad.put(i, i)\nprint(bad.max_chain(), all(bad.get(i) == i for i in range(300)))\n", "expected": ["8 4 2 [1, 9, 2, 5]", "55 None нет True False", "True False 3 [1, 2, 5]", "8 [1, 2, 3, 5]", "[8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096] 2000 1999 True", "300 True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'linear-probing-map', 4, 'stdout', 'Линейное пробирование', 'Реализуйте класс LinearProbingMap(capacity=8, hash_fn=None) — открытая адресация с линейным пробированием: ячейки start, start+1, start+2, … по кругу, где start = hash_fn(key) % capacity. Ячейки — список self.slots: None (пусто), TOMB (надгробие) или кортеж (ключ, значение). Поля: size — живые ключи, used — живые ключи плюс надгробия, probes — счётчик осмотренных ячеек. Каждый осмотр ячейки в get / put / remove увеличивает probes на 1 (от стартовой до найденного ключа или до первой пустой ячейки включительно). get идёт мимо надгробий и останавливается на None. put сначала убеждается, что ключа нет (доходит до None), и вставляет в первое встретившееся надгробие, а если его не было — в пустую ячейку (тогда used += 1); существующий ключ обновляется. remove ставит надгробие (size -= 1). Рост: после вставки НОВОГО ключа в пустую ячейку (не в надгробие), если used * 2 > capacity, перестройте таблицу вдвое большего размера: пройдите по старым ячейкам по возрастанию индекса и вставьте живые пары (надгробия выбрасываются; probes при перестройке не меняется).', 'TOMB = object()


class LinearProbingMap:
    def __init__(self, capacity=8, hash_fn=None):
        self.hash_fn = hash_fn or hash
        self.slots = [None] * capacity
        self.size = 0
        self.used = 0
        self.probes = 0

    def __len__(self):
        return self.size

    # put, get, remove, __contains__
', 'Один метод поиска _find(key), который возвращает индекс ключа, первого надгробия и пустой ячейки, избавит от дублирования в get/put/remove. Не забывайте считать probes при каждом осмотре ячейки.', '{"driver": "def layout(m):\n    return [(\"T\" if s is TOMB else None if s is None else s[0]) for s in m.slots]\n\n\nm = LinearProbingMap(8, hash_fn=lambda k: k)\nfor k in (5, 13, 21):\n    m.put(k, k * 10)\nprint(layout(m), m.probes, len(m))\nm.probes = 0\nprint(m.get(21), m.probes)\nm.probes = 0\nprint(m.get(29), m.probes)\nm.probes = 0\nprint(m.remove(13), m.probes, layout(m))\nm.probes = 0\nprint(m.get(21), m.probes)\nm.probes = 0\nm.put(29, 290)\nprint(m.probes, layout(m), len(m), m.used)\nm.put(6, 60)\nprint(layout(m), len(m), m.used)\nm = LinearProbingMap(4, hash_fn=lambda k: k)\ncaps = []\nfor k in range(10):\n    m.put(k, k)\n    caps.append(len(m.slots))\nprint(caps)\nfor k in range(10):\n    m.remove(k)\nprint(len(m), len(m.slots), 3 in m)\nbig = LinearProbingMap()\nx = 1\nfor i in range(100000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    k = x % 5000\n    if x % 3 == 0:\n        big.remove(k)\n    else:\n        big.put(k, i)\nprint(len(big), len(big.slots), sum(1 for k in range(5000) if k in big))\n", "expected": ["[None, None, None, None, None, 5, 13, 21] 6 3", "210 3", "None 4", "True 2 [None, None, None, None, None, 5, ''T'', 21]", "210 3", "4 [None, None, None, None, None, 5, 29, 21] 3 3", "[6, None, None, None, None, 5, 29, 21] 4 4", "[4, 4, 8, 8, 16, 16, 16, 16, 32, 32]", "0 32 False", "3283 16384 3283"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'quadratic-probing-map', 5, 'stdout', 'Квадратичное пробирование', 'Реализуйте класс QuadraticProbingMap(capacity=8, hash_fn=None) — как LinearProbingMap, но на шаге i (i = 0, 1, 2, …) проверяется ячейка (start + i·(i+1)//2) % capacity — треугольные смещения 0, 1, 3, 6, 10…; для размера, равного степени двойки, они обходят все ячейки. Ячейки — список self.slots: None (пусто), TOMB (надгробие) или кортеж (ключ, значение). Поля: size — живые ключи, used — живые ключи плюс надгробия, probes — счётчик осмотренных ячеек. Каждый осмотр ячейки в get / put / remove увеличивает probes на 1 (от стартовой до найденного ключа или до первой пустой ячейки включительно). get идёт мимо надгробий и останавливается на None. put сначала убеждается, что ключа нет (доходит до None), и вставляет в первое встретившееся надгробие, а если его не было — в пустую ячейку (тогда used += 1); существующий ключ обновляется. remove ставит надгробие (size -= 1). Рост: после вставки НОВОГО ключа в пустую ячейку, если used * 2 > capacity, перестройте таблицу вдвое большего размера (старые ячейки по возрастанию индекса, надгробия выбрасываются, probes не меняется).', 'TOMB = object()


class QuadraticProbingMap:
    def __init__(self, capacity=8, hash_fn=None):
        self.hash_fn = hash_fn or hash
        self.slots = [None] * capacity
        self.size = 0
        self.used = 0
        self.probes = 0

    def __len__(self):
        return self.size

    # put, get, remove, __contains__
', 'Тот же каркас, что и у линейного пробирования, меняется только формула индекса на шаге i: (start + i * (i + 1) // 2) % capacity.', '{"driver": "def layout(m):\n    return [(\"T\" if s is TOMB else None if s is None else s[0]) for s in m.slots]\n\n\nm = QuadraticProbingMap(16, hash_fn=lambda k: k)\nfor k in (3, 19, 35, 51, 4):\n    m.put(k, k)\nprint(layout(m), m.probes)\nm.probes = 0\nprint(m.get(51), m.probes)\nm.probes = 0\nprint(m.get(67), m.probes)\nm.probes = 0\nprint(m.remove(19), layout(m))\nm.probes = 0\nprint(m.get(35), m.probes, m.get(51), m.probes)\nm.put(67, 1)\nprint(layout(m), len(m), m.used)\nm = QuadraticProbingMap(4, hash_fn=lambda k: k)\ncaps = []\nfor k in range(0, 40, 4):\n    m.put(k, k)\n    caps.append(len(m.slots))\nprint(caps, len(m))\nbig = QuadraticProbingMap()\nx = 7\nfor i in range(100000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    k = x % 8000\n    if x % 4 == 0:\n        big.remove(k)\n    else:\n        big.put(k, i)\nprint(len(big), len(big.slots), sum(1 for k in range(8000) if k in big))\n", "expected": ["[None, None, None, 3, 19, 4, 35, None, None, 51, None, None, None, None, None, None] 12", "51 4", "None 5", "True [None, None, None, 3, ''T'', 4, 35, None, None, 51, None, None, None, None, None, None]", "35 3 51 7", "[None, None, None, 3, 67, 4, 35, None, None, 51, None, None, None, None, None, None] 5 5", "[4, 4, 8, 8, 16, 16, 16, 16, 32, 32] 10", "6000 16384 6000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'double-hashing-map', 6, 'stdout', 'Двойное хеширование', 'Реализуйте класс DoubleHashMap(capacity=11, hash_fn=None) фиксированного простого размера: на шаге i (i = 0, 1, 2, …) проверяется ячейка (h + i·step) % capacity, где h = hash_fn(key), step = 1 + h % (capacity − 1) — второй хеш. Ячейки — список self.slots: None (пусто), TOMB (надгробие) или кортеж (ключ, значение). Поля: size — живые ключи, used — живые ключи плюс надгробия, probes — счётчик осмотренных ячеек. Каждый осмотр ячейки в get / put / remove увеличивает probes на 1 (от стартовой до найденного ключа или до первой пустой ячейки включительно). get идёт мимо надгробий и останавливается на None. put сначала убеждается, что ключа нет (доходит до None), и вставляет в первое встретившееся надгробие, а если его не было — в пустую ячейку (тогда used += 1); существующий ключ обновляется. remove ставит надгробие (size -= 1). Рост не предусмотрен: если свободной ячейки (пустой или надгробия) не нашлось и ключа нет — поднимите OverflowError.', 'TOMB = object()


class DoubleHashMap:
    def __init__(self, capacity=11, hash_fn=None):
        self.hash_fn = hash_fn or hash
        self.slots = [None] * capacity
        self.size = 0
        self.used = 0
        self.probes = 0

    def __len__(self):
        return self.size

    # put, get, remove, __contains__
', 'Шаг второй функции не нулевой и взаимно прост с простым размером, поэтому за capacity проб обходятся все ячейки.', '{"driver": "def layout(m):\n    return [(\"T\" if s is TOMB else None if s is None else s[0]) for s in m.slots]\n\n\nm = DoubleHashMap(11, hash_fn=lambda k: k)\nfor k in (3, 14, 25, 36):\n    m.put(k, k)\nprint(layout(m), m.probes)\nm.probes = 0\nprint(m.get(36), m.probes, m.get(47), m.probes)\nm.probes = 0\nprint(m.remove(14), layout(m))\nm.probes = 0\nprint(m.get(25), m.probes)\nm.put(47, 0)\nprint(layout(m), len(m))\nfor k in range(100, 110):\n    try:\n        m.put(k, k)\n    except OverflowError:\n        print(\"полна на\", k)\n        break\nprint(len(m), sum(1 for s in m.slots if s is None))\n", "expected": ["[None, None, None, 3, None, None, None, None, 14, 25, 36] 7", "36 2 None 4", "True [None, None, None, 3, None, None, None, None, ''T'', 25, 36]", "25 2", "[47, None, None, 3, None, None, None, None, ''T'', 25, 36] 4", "полна на 107", "11 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'robin-hood-map', 7, 'stdout', 'Хеш-таблица Робин Гуда', 'Реализуйте класс RobinHoodMap(capacity=8, hash_fn=None) для целых ключей: фиксированный размер, линейное пробирование от start = hash_fn(key) % capacity. Ячейка — None или список [ключ, значение, d], где d — расстояние до родной ячейки. put: идём по ячейкам с d = 0, 1, 2, …; пустая — кладём; тот же ключ — обновляем значение; если d у хозяина ячейки МЕНЬШЕ нашего — меняемся местами и продолжаем вставлять вытесненного (его d в следующей ячейке — на 1 больше). get: останавливаемся на пустой ячейке или когда d хозяина меньше нашего (ключа нет). remove: найдя ключ, сдвиньте назад следующие ячейки, пока не встретится пустая или ячейка с d = 0. Каждый осмотр ячейки в put и get прибавляет 1 к probes. При put нового ключа в полную таблицу — OverflowError (таблица не меняется).', 'class RobinHoodMap:
    def __init__(self, capacity=8, hash_fn=None):
        self.hash_fn = hash_fn or hash
        self.slots = [None] * capacity
        self.size = 0
        self.probes = 0

    def __len__(self):
        return self.size

    # put, get, remove, __contains__
', 'В put у вытесненного хозяина d относится к ячейке, откуда его выбросили; в следующей ячейке он будет на d + 1. В remove после нахождения ключа тяните назад следующие ячейки, уменьшая их d на 1.', '{"driver": "def layout(m):\n    return [None if s is None else (s[0], s[2]) for s in m.slots]\n\n\nm = RobinHoodMap(8, hash_fn=lambda k: k)\nfor k in (8, 16, 2, 10, 24):\n    m.put(k, k)\nprint(layout(m), m.probes, len(m))\nm.probes = 0\nprint(m.get(24), m.probes, m.get(18), m.probes)\nm.probes = 0\nprint(m.get(3), m.probes)\nprint(m.remove(16), layout(m), len(m))\nprint(m.remove(99), m.remove(8), layout(m))\nm.put(24, \"x\")\nprint(m.get(24), len(m))\nf = RobinHoodMap(4, hash_fn=lambda k: k)\nfor k in (0, 4, 8, 12):\n    f.put(k, k)\nprint(layout(f))\ntry:\n    f.put(16, 1)\nexcept OverflowError:\n    print(\"полна\")\nf.put(8, \"обновили\")\nprint(f.get(8), len(f))\nbig = RobinHoodMap(1024, hash_fn=lambda k: k * 7)\nx = 5\nfor i in range(700):\n    x = (x * 1103515245 + 12345) % 2147483648\n    big.put(x % 100000, i)\nmx = max(s[2] for s in big.slots if s is not None)\nprint(len(big), mx, sum(1 for s in big.slots if s is not None))\nfor k in range(0, 100000, 3):\n    big.remove(k)\nprint(len(big), all(s is None or (s[0] % 3 != 0) for s in big.slots))\n", "expected": ["[(8, 0), (16, 1), (24, 2), (10, 1), (2, 2), None, None, None] 11 5", "24 3 None 7", "None 3", "True [(8, 0), (24, 1), (10, 0), (2, 1), None, None, None, None] 4", "False True [(24, 0), None, (10, 0), (2, 1), None, None, None, None]", "x 3", "[(0, 0), (4, 1), (8, 2), (12, 3)]", "полна", "обновили 4", "698 7 698", "484 True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'cuckoo-hash', 8, 'stdout', 'Кукушкино хеширование', 'Реализуйте класс CuckooHash(capacity=8) для неотрицательных целых ключей: две таблицы t1 и t2 (списки длины capacity из None или пар [ключ, значение]); h1(k) = k % capacity, h2(k) = (k // capacity) % capacity. put: если ключ уже есть — обновить; иначе класть в t1[h1], выселяя жильца в его t2[h2], выселенного оттуда — обратно в t1 и так далее, не более 32 выселений; если не получилось — удвойте capacity и вставьте всё заново (включая оставшегося без дома). get(key, default=None) проверяет t1[h1], затем t2[h2]; каждая проверка ячейки увеличивает self.probes, так что поиск стоит не больше двух проб. Нужны также remove(key) → True/False, key in m и len(m).', 'class CuckooHash:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.t1 = [None] * capacity
        self.t2 = [None] * capacity
        self.size = 0
        self.probes = 0

    def __len__(self):
        return self.size

    # put, get, remove, __contains__
', 'Цикл выселений: item, t1[i] = t1[i], item; если item стал None — готово; иначе то же с t2 по h2(item). После 32 кругов — удвойте capacity и вставьте всё заново, не забыв item.', '{"driver": "m = CuckooHash(8)\nn = 3000\nfor k in range(0, n * 7, 7):\n    m.put(k, k + 1)\nprint(len(m))\nprint(all(m.get(k) == k + 1 for k in range(0, n * 7, 7)))\nprint(all(m.get(k) is None for k in range(1, 2000, 7)))\nmx = 0\nfor k in list(range(0, 600, 7)) + list(range(1, 600, 7)):\n    m.probes = 0\n    m.get(k)\n    mx = max(mx, m.probes)\nprint(mx <= 2)\nm.put(0, \"x\")\nprint(m.get(0), len(m), 7 in m, 8 in m)\nprint(m.remove(7), m.remove(7), 7 in m, len(m))\nw = CuckooHash(4)\nfor k in (0, 16, 32, 48, 64, 80, 96, 112, 128):\n    w.put(k, k)\nprint(len(w), all(w.get(k) == k for k in (0, 16, 32, 48, 64, 80, 96, 112, 128)))\n", "expected": ["3000", "True", "True", "True", "x 3000 True False", "True False False 2999", "9 True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'hashset-on-map', 9, 'stdout', 'Множество на своей таблице', 'Хеш-таблица HashMap уже лежит в заготовке (она из предыдущих упражнений). Постройте на ней класс HashSet: add(x), remove(x) → True/False, x in s, len(s), union(other), intersection(other), difference(other) (каждая возвращает НОВЫЙ HashSet) и to_sorted_list(). Встроенные set, dict и импорты запрещены.', 'class HashMap:
    """Хеш-таблица с цепочками: put / get / remove / in / len / keys / items."""

    def __init__(self, capacity=8):
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > 0.75 * len(self._buckets):
            self._grow()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key):
        for k, _ in self._bucket(key):
            if k == key:
                return True
        return False

    def __len__(self):
        return self._size

    def keys(self):
        return [k for b in self._buckets for k, _ in b]

    def items(self):
        return [(k, v) for b in self._buckets for k, v in b]

    def _grow(self):
        old = self.items()
        self._buckets = [[] for _ in range(2 * len(self._buckets))]
        self._size = 0
        for k, v in old:
            self.put(k, v)


class HashSet:
    def __init__(self):
        self._map = HashMap()

    # add, remove, __contains__, __len__, union, intersection, difference, to_sorted_list
', 'Множество — это таблица, где значение не важно: add кладёт пару (x, True), остальное делегируется таблице. Новые множества стройте, перебирая keys().', '{"driver": "import ast as _ast\ntry:\n    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\nexcept OSError:\n    _src = \"\"\n_bad = set()\nfor _top in _ast.parse(_src).body:\n    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n        continue\n    for _n in _ast.walk(_top):\n        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n            _bad.add(\"литерал словаря или множества\")\n        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n            _bad.add(_n.func.id + \"()\")\n        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n            _bad.add(\"import\")\nprint(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\na = HashSet()\nb = HashSet()\nfor x in [1, 2, 3, 4, 2, 2]:\n    a.add(x)\nfor x in [3, 4, 5, 6]:\n    b.add(x)\nprint(len(a), a.to_sorted_list(), 2 in a, 9 in a)\nprint(a.union(b).to_sorted_list(), a.intersection(b).to_sorted_list(), a.difference(b).to_sorted_list(), b.difference(a).to_sorted_list())\nprint(a.remove(1), a.remove(1), a.to_sorted_list())\nbig = HashSet()\nfor i in range(100000):\n    big.add(i * 3 % 100003)\nprint(len(big), big.intersection(a).to_sorted_list())\n", "expected": ["словари и множества не использованы", "4 [1, 2, 3, 4] True False", "[1, 2, 3, 4, 5, 6] [3, 4] [1, 2] [5, 6]", "True False [2, 3, 4]", "100000 [2, 3, 4]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'word-frequencies', 10, 'stdout', 'Частоты слов', 'Напишите функцию word_frequencies(text): частота каждого слова текста (слова разделены пробелами и переводами строк, регистр различается) — список пар (слово, число), отсортированный по убыванию числа, а при равенстве — по слову. Готовая таблица HashMap лежит в заготовке — используйте только её put / get / remove / in / len / keys / items. Литералы словарей и множеств, dict(), set() и импорты запрещены.', 'class HashMap:
    """Хеш-таблица с цепочками: put / get / remove / in / len / keys / items."""

    def __init__(self, capacity=8):
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > 0.75 * len(self._buckets):
            self._grow()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key):
        for k, _ in self._bucket(key):
            if k == key:
                return True
        return False

    def __len__(self):
        return self._size

    def keys(self):
        return [k for b in self._buckets for k, _ in b]

    def items(self):
        return [(k, v) for b in self._buckets for k, v in b]

    def _grow(self):
        old = self.items()
        self._buckets = [[] for _ in range(2 * len(self._buckets))]
        self._size = 0
        for k, v in old:
            self.put(k, v)


def word_frequencies(text):
    pass
', 'm.put(w, m.get(w, 0) + 1) — вся суть. Затем sorted(m.items(), key=lambda kv: (-kv[1], kv[0])).', '{"driver": "import ast as _ast\ntry:\n    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\nexcept OSError:\n    _src = \"\"\n_bad = set()\nfor _top in _ast.parse(_src).body:\n    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n        continue\n    for _n in _ast.walk(_top):\n        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n            _bad.add(\"литерал словаря или множества\")\n        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n            _bad.add(_n.func.id + \"()\")\n        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n            _bad.add(\"import\")\nprint(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\nprint(word_frequencies(\"a b a c b a\"))\nprint(word_frequencies(\"\"), word_frequencies(\"x\"))\ntext = \" \".join(\"w\" + str(i % 1000) for i in range(300000))\nr = word_frequencies(text)\nprint(len(r), r[0], r[-1])\n", "expected": ["словари и множества не использованы", "[(''a'', 3), (''b'', 2), (''c'', 1)]", "[] [(''x'', 1)]", "1000 (''w0'', 300) (''w999'', 300)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'two-sum-own-map', 11, 'stdout', 'Два числа с суммой (на своей таблице)', 'Напишите функцию two_sum(nums, target): пару индексов (i, j), i < j, где nums[i] + nums[j] == target. Если пар несколько — берите ту, у которой наименьший j, а при равенстве — наименьший i. Если пары нет — None. Проверка подаёт 200 000 чисел: вложенные циклы не успеют. Готовая таблица HashMap лежит в заготовке — используйте только её put / get / remove / in / len / keys / items. Литералы словарей и множеств, dict(), set() и импорты запрещены.', 'class HashMap:
    """Хеш-таблица с цепочками: put / get / remove / in / len / keys / items."""

    def __init__(self, capacity=8):
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > 0.75 * len(self._buckets):
            self._grow()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key):
        for k, _ in self._bucket(key):
            if k == key:
                return True
        return False

    def __len__(self):
        return self._size

    def keys(self):
        return [k for b in self._buckets for k, _ in b]

    def items(self):
        return [(k, v) for b in self._buckets for k, v in b]

    def _grow(self):
        old = self.items()
        self._buckets = [[] for _ in range(2 * len(self._buckets))]
        self._size = 0
        for k, v in old:
            self.put(k, v)


def two_sum(nums, target):
    pass
', 'Идём слева направо: нужное «target − x» уже встречалось? Тогда пара найдена. Иначе запоминаем x → индекс (только первое вхождение).', '{"driver": "import ast as _ast\ntry:\n    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\nexcept OSError:\n    _src = \"\"\n_bad = set()\nfor _top in _ast.parse(_src).body:\n    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n        continue\n    for _n in _ast.walk(_top):\n        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n            _bad.add(\"литерал словаря или множества\")\n        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n            _bad.add(_n.func.id + \"()\")\n        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n            _bad.add(\"import\")\nprint(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\nprint(two_sum([2, 7, 11, 15], 9), two_sum([3, 2, 4], 6), two_sum([3, 3], 6), two_sum([5, 5, 1], 6), two_sum([1, 2], 10), two_sum([], 1))\nbig = list(range(200000))\nprint(two_sum(big, 399997), two_sum(big, 500000))\n", "expected": ["словари и множества не использованы", "(0, 1) (1, 2) (0, 1) (0, 2) None None", "(199998, 199999) None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'first-unique-own-map', 12, 'stdout', 'Первая уникальная буква', 'Напишите функцию first_unique(s): индекс первого символа, который встречается в строке ровно один раз, или −1. Проверка подаёт 500 000 символов. Готовая таблица HashMap лежит в заготовке — используйте только её put / get / remove / in / len / keys / items. Литералы словарей и множеств, dict(), set() и импорты запрещены.', 'class HashMap:
    """Хеш-таблица с цепочками: put / get / remove / in / len / keys / items."""

    def __init__(self, capacity=8):
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > 0.75 * len(self._buckets):
            self._grow()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key):
        for k, _ in self._bucket(key):
            if k == key:
                return True
        return False

    def __len__(self):
        return self._size

    def keys(self):
        return [k for b in self._buckets for k, _ in b]

    def items(self):
        return [(k, v) for b in self._buckets for k, v in b]

    def _grow(self):
        old = self.items()
        self._buckets = [[] for _ in range(2 * len(self._buckets))]
        self._size = 0
        for k, v in old:
            self.put(k, v)


def first_unique(s):
    pass
', 'Два прохода: первый считает частоты, второй возвращает индекс первого символа с частотой 1.', '{"driver": "import ast as _ast\ntry:\n    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\nexcept OSError:\n    _src = \"\"\n_bad = set()\nfor _top in _ast.parse(_src).body:\n    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n        continue\n    for _n in _ast.walk(_top):\n        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n            _bad.add(\"литерал словаря или множества\")\n        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n            _bad.add(_n.func.id + \"()\")\n        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n            _bad.add(\"import\")\nprint(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\nprint(first_unique(\"leetcode\"), first_unique(\"loveleetcode\"), first_unique(\"aabb\"), first_unique(\"\"), first_unique(\"z\"))\ns = \"\".join(chr(97 + i % 20) for i in range(250000)) * 2 + \"Z\"\nprint(first_unique(s))\n", "expected": ["словари и множества не использованы", "0 2 -1 -1 0", "500000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'group-anagrams-own-map', 13, 'stdout', 'Группы анаграмм', 'Напишите функцию group_anagrams(words): разбейте слова на группы анаграмм. Результат — список групп; внутри группы слова отсортированы, группы отсортированы между собой (как списки). Готовая таблица HashMap лежит в заготовке — используйте только её put / get / remove / in / len / keys / items. Литералы словарей и множеств, dict(), set() и импорты запрещены.', 'class HashMap:
    """Хеш-таблица с цепочками: put / get / remove / in / len / keys / items."""

    def __init__(self, capacity=8):
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > 0.75 * len(self._buckets):
            self._grow()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key):
        for k, _ in self._bucket(key):
            if k == key:
                return True
        return False

    def __len__(self):
        return self._size

    def keys(self):
        return [k for b in self._buckets for k, _ in b]

    def items(self):
        return [(k, v) for b in self._buckets for k, v in b]

    def _grow(self):
        old = self.items()
        self._buckets = [[] for _ in range(2 * len(self._buckets))]
        self._size = 0
        for k, v in old:
            self.put(k, v)


def group_anagrams(words):
    pass
', 'Ключ группы — отсортированные буквы слова: «eat» и «tea» дают «aet». Значение — список слов; список можно положить в таблицу и дописывать.', '{"driver": "import ast as _ast\ntry:\n    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\nexcept OSError:\n    _src = \"\"\n_bad = set()\nfor _top in _ast.parse(_src).body:\n    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n        continue\n    for _n in _ast.walk(_top):\n        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n            _bad.add(\"литерал словаря или множества\")\n        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n            _bad.add(_n.func.id + \"()\")\n        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n            _bad.add(\"import\")\nprint(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\nprint(group_anagrams([\"eat\", \"tea\", \"tan\", \"ate\", \"nat\", \"bat\"]))\nprint(group_anagrams([\"\"]), group_anagrams([\"a\"]), group_anagrams([]))\nwords = [\"\".join(sorted(str(i))) + \"x\" if False else str(i) for i in range(30000)]\nr = group_anagrams(words)\nprint(len(r), max(len(g) for g in r))\n", "expected": ["словари и множества не использованы", "[[''ate'', ''eat'', ''tea''], [''bat''], [''nat'', ''tan'']]", "[['''']] [[''a'']] []", "2207 48"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'subarray-sum-k-own-map', 14, 'stdout', 'Подмассивы с суммой k', 'Напишите функцию count_subarrays(nums, k): сколько непустых подряд идущих подмассивов имеют сумму k (числа могут быть отрицательными). Проверка подаёт 200 000 чисел. Готовая таблица HashMap лежит в заготовке — используйте только её put / get / remove / in / len / keys / items. Литералы словарей и множеств, dict(), set() и импорты запрещены.', 'class HashMap:
    """Хеш-таблица с цепочками: put / get / remove / in / len / keys / items."""

    def __init__(self, capacity=8):
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > 0.75 * len(self._buckets):
            self._grow()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key):
        for k, _ in self._bucket(key):
            if k == key:
                return True
        return False

    def __len__(self):
        return self._size

    def keys(self):
        return [k for b in self._buckets for k, _ in b]

    def items(self):
        return [(k, v) for b in self._buckets for k, v in b]

    def _grow(self):
        old = self.items()
        self._buckets = [[] for _ in range(2 * len(self._buckets))]
        self._size = 0
        for k, v in old:
            self.put(k, v)


def count_subarrays(nums, k):
    pass
', 'Префиксная сумма total; нужный подмассив заканчивается здесь, если раньше встречалась префиксная сумма total − k. Таблица хранит, сколько раз встречалась каждая префиксная сумма (сначала 0 встречалась один раз).', '{"driver": "import ast as _ast\ntry:\n    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\nexcept OSError:\n    _src = \"\"\n_bad = set()\nfor _top in _ast.parse(_src).body:\n    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n        continue\n    for _n in _ast.walk(_top):\n        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n            _bad.add(\"литерал словаря или множества\")\n        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n            _bad.add(_n.func.id + \"()\")\n        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n            _bad.add(\"import\")\nprint(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\nprint(count_subarrays([1, 1, 1], 2), count_subarrays([1, 2, 3], 3), count_subarrays([1, -1, 0], 0), count_subarrays([], 0), count_subarrays([5], 5))\nx = 3\nnums = []\nfor _ in range(200000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    nums.append(x % 5 - 2)\nprint(count_subarrays(nums, 3), count_subarrays(nums, 0))\n", "expected": ["словари и множества не использованы", "2 2 3 0 1", "30030654 30462315"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'longest-consecutive-own-map', 15, 'stdout', 'Самая длинная серия подряд', 'Напишите функцию longest_consecutive(nums): длина самой длинной серии подряд идущих целых (например, 100, 4, 200, 1, 3, 2 → серия 1, 2, 3, 4 длиной 4). Порядок в массиве не важен, дубликаты возможны. Нужно линейное время: сортировкой не обойдётся — проверка подаёт 300 000 чисел, а сама серия строится от каждого начала ровно один раз. Готовая таблица HashMap лежит в заготовке — используйте только её put / get / remove / in / len / keys / items. Литералы словарей и множеств, dict(), set() и импорты запрещены.', 'class HashMap:
    """Хеш-таблица с цепочками: put / get / remove / in / len / keys / items."""

    def __init__(self, capacity=8):
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > 0.75 * len(self._buckets):
            self._grow()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key):
        for k, _ in self._bucket(key):
            if k == key:
                return True
        return False

    def __len__(self):
        return self._size

    def keys(self):
        return [k for b in self._buckets for k, _ in b]

    def items(self):
        return [(k, v) for b in self._buckets for k, v in b]

    def _grow(self):
        old = self.items()
        self._buckets = [[] for _ in range(2 * len(self._buckets))]
        self._size = 0
        for k, v in old:
            self.put(k, v)


def longest_consecutive(nums):
    pass
', 'Положите все числа в таблицу. Серию начинайте только с числа, у которого нет x − 1: тогда каждое число посещается не больше двух раз.', '{"driver": "import ast as _ast\ntry:\n    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\nexcept OSError:\n    _src = \"\"\n_bad = set()\nfor _top in _ast.parse(_src).body:\n    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n        continue\n    for _n in _ast.walk(_top):\n        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n            _bad.add(\"литерал словаря или множества\")\n        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n            _bad.add(_n.func.id + \"()\")\n        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n            _bad.add(\"import\")\nprint(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\nprint(longest_consecutive([100, 4, 200, 1, 3, 2]), longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]), longest_consecutive([]), longest_consecutive([5]), longest_consecutive([1, 1, 1]))\nnums = [(i * 7919) % 300007 for i in range(300000)]\nprint(longest_consecutive(nums))\n", "expected": ["словари и множества не использованы", "4 9 0 1 1", "244574"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'isomorphic-own-map', 16, 'stdout', 'Изоморфные строки', 'Напишите функцию is_isomorphic(s, t): True, если буквы строки s можно заменить так, чтобы получилась t, причём каждая буква заменяется одной и той же буквой, а разные буквы — разными (взаимно однозначно). Строки одной длины. Нужны две таблицы: s→t и t→s. Готовая таблица HashMap лежит в заготовке — используйте только её put / get / remove / in / len / keys / items. Литералы словарей и множеств, dict(), set() и импорты запрещены.', 'class HashMap:
    """Хеш-таблица с цепочками: put / get / remove / in / len / keys / items."""

    def __init__(self, capacity=8):
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > 0.75 * len(self._buckets):
            self._grow()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key):
        for k, _ in self._bucket(key):
            if k == key:
                return True
        return False

    def __len__(self):
        return self._size

    def keys(self):
        return [k for b in self._buckets for k, _ in b]

    def items(self):
        return [(k, v) for b in self._buckets for k, v in b]

    def _grow(self):
        old = self.items()
        self._buckets = [[] for _ in range(2 * len(self._buckets))]
        self._size = 0
        for k, v in old:
            self.put(k, v)


def is_isomorphic(s, t):
    pass
', 'Достаточно двух таблиц: что стоит на месте буквы x в t (a) и что стоит на месте буквы y в s (b); любое противоречие — False.', '{"driver": "import ast as _ast\ntry:\n    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\nexcept OSError:\n    _src = \"\"\n_bad = set()\nfor _top in _ast.parse(_src).body:\n    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n        continue\n    for _n in _ast.walk(_top):\n        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n            _bad.add(\"литерал словаря или множества\")\n        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n            _bad.add(_n.func.id + \"()\")\n        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n            _bad.add(\"import\")\nprint(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\nprint(is_isomorphic(\"egg\", \"add\"), is_isomorphic(\"foo\", \"bar\"), is_isomorphic(\"paper\", \"title\"), is_isomorphic(\"ab\", \"aa\"), is_isomorphic(\"\", \"\"), is_isomorphic(\"a\", \"ab\"))\ns = \"\".join(chr(97 + i % 26) for i in range(300000))\nt = \"\".join(chr(65 + i % 26) for i in range(300000))\nprint(is_isomorphic(s, t), is_isomorphic(s, t[:-1] + \"a\"))\n", "expected": ["словари и множества не использованы", "True False True False True False", "True False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'lru-own-map', 17, 'stdout', 'LRU-кэш на своей таблице', 'Реализуйте класс LRUCache(capacity): get(key) → значение или −1 (обращение делает ключ самым свежим); put(key, value) — добавить или обновить (тоже освежает); при превышении capacity вытесняется самый давний ключ. Обе операции за O(1): таблица HashMap хранит узлы двусвязного списка DNode, список упорядочивает ключи по свежести (дозорные в начале и в конце помогут). Готовая таблица HashMap лежит в заготовке — используйте только её put / get / remove / in / len / keys / items. Литералы словарей и множеств, dict(), set() и импорты запрещены.', 'class HashMap:
    """Хеш-таблица с цепочками: put / get / remove / in / len / keys / items."""

    def __init__(self, capacity=8):
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > 0.75 * len(self._buckets):
            self._grow()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key):
        for k, _ in self._bucket(key):
            if k == key:
                return True
        return False

    def __len__(self):
        return self._size

    def keys(self):
        return [k for b in self._buckets for k, _ in b]

    def items(self):
        return [(k, v) for b in self._buckets for k, v in b]

    def _grow(self):
        old = self.items()
        self._buckets = [[] for _ in range(2 * len(self._buckets))]
        self._size = 0
        for k, v in old:
            self.put(k, v)


class DNode:
    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.table = HashMap()
        self.head = DNode()
        self.tail = DNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    # get, put (и вспомогательные методы работы со списком)
', 'get: найти узел в таблице, вырезать из списка, вставить после head. put: если ключ есть — обновить и освежить; иначе при переполнении удалить tail.prev (и из списка, и из таблицы), затем вставить новый узел.', '{"driver": "import ast as _ast\ntry:\n    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\nexcept OSError:\n    _src = \"\"\n_bad = set()\nfor _top in _ast.parse(_src).body:\n    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n        continue\n    for _n in _ast.walk(_top):\n        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n            _bad.add(\"литерал словаря или множества\")\n        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n            _bad.add(_n.func.id + \"()\")\n        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n            _bad.add(\"import\")\nprint(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\nc = LRUCache(2)\nc.put(1, 1)\nc.put(2, 2)\nprint(c.get(1))\nc.put(3, 3)\nprint(c.get(2))\nc.put(4, 4)\nprint(c.get(1), c.get(3), c.get(4))\nc.put(4, 40)\nprint(c.get(4), len(c.table))\nbig = LRUCache(1000)\nx = 11\ntotal = 0\nfor i in range(200000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    k = x % 1500\n    if x % 2:\n        big.put(k, i)\n    else:\n        total += big.get(k)\nprint(total, len(big.table))\n", "expected": ["словари и множества не использованы", "1", "-1", "-1 3 4", "40 2", "-100000 750"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'top-k-own-map', 18, 'stdout', 'k самых частых', 'Напишите функцию top_k(nums, k): k самых частых значений массива в порядке убывания частоты, при равенстве частот — по возрастанию значения. Гарантируется, что k не больше числа различных значений. Считайте частоты в таблице. Проверка подаёт 300 000 чисел. Готовая таблица HashMap лежит в заготовке — используйте только её put / get / remove / in / len / keys / items. Литералы словарей и множеств, dict(), set() и импорты запрещены.', 'class HashMap:
    """Хеш-таблица с цепочками: put / get / remove / in / len / keys / items."""

    def __init__(self, capacity=8):
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > 0.75 * len(self._buckets):
            self._grow()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key):
        for k, _ in self._bucket(key):
            if k == key:
                return True
        return False

    def __len__(self):
        return self._size

    def keys(self):
        return [k for b in self._buckets for k, _ in b]

    def items(self):
        return [(k, v) for b in self._buckets for k, v in b]

    def _grow(self):
        old = self.items()
        self._buckets = [[] for _ in range(2 * len(self._buckets))]
        self._size = 0
        for k, v in old:
            self.put(k, v)


def top_k(nums, k):
    pass
', 'Частоты — в таблице; затем отсортируйте items() по (−частота, значение) и возьмите первые k значений.', '{"driver": "import ast as _ast\ntry:\n    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\nexcept OSError:\n    _src = \"\"\n_bad = set()\nfor _top in _ast.parse(_src).body:\n    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n        continue\n    for _n in _ast.walk(_top):\n        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n            _bad.add(\"литерал словаря или множества\")\n        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n            _bad.add(_n.func.id + \"()\")\n        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n            _bad.add(\"import\")\nprint(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\nprint(top_k([1, 1, 1, 2, 2, 3], 2), top_k([4], 1), top_k([5, 5, 6, 6, 7], 3))\nnums = [(i * i) % 997 for i in range(300000)]\nprint(top_k(nums, 5))\n", "expected": ["словари и множества не использованы", "[1, 2] [4] [5, 6, 7]", "[3, 10, 12, 13, 14]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 5, 'nearby-duplicate-own-map', 19, 'stdout', 'Близкие дубликаты', 'Напишите функцию contains_nearby_duplicate(nums, k): True, если есть два разных индекса i и j с nums[i] == nums[j] и |i − j| ≤ k. Таблица хранит последний индекс каждого значения. Проверка подаёт 400 000 чисел. Готовая таблица HashMap лежит в заготовке — используйте только её put / get / remove / in / len / keys / items. Литералы словарей и множеств, dict(), set() и импорты запрещены.', 'class HashMap:
    """Хеш-таблица с цепочками: put / get / remove / in / len / keys / items."""

    def __init__(self, capacity=8):
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return
        bucket.append([key, value])
        self._size += 1
        if self._size > 0.75 * len(self._buckets):
            self._grow()

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, pair in enumerate(bucket):
            if pair[0] == key:
                del bucket[i]
                self._size -= 1
                return True
        return False

    def __contains__(self, key):
        for k, _ in self._bucket(key):
            if k == key:
                return True
        return False

    def __len__(self):
        return self._size

    def keys(self):
        return [k for b in self._buckets for k, _ in b]

    def items(self):
        return [(k, v) for b in self._buckets for k, v in b]

    def _grow(self):
        old = self.items()
        self._buckets = [[] for _ in range(2 * len(self._buckets))]
        self._size = 0
        for k, v in old:
            self.put(k, v)


def contains_nearby_duplicate(nums, k):
    pass
', 'Идём по массиву и помним последний индекс каждого значения. Нашли значение, виденное не дальше k шагов назад — ответ True.', '{"driver": "import ast as _ast\ntry:\n    _src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\nexcept OSError:\n    _src = \"\"\n_bad = set()\nfor _top in _ast.parse(_src).body:\n    if isinstance(_top, _ast.ClassDef) and _top.name == \"HashMap\":\n        continue\n    for _n in _ast.walk(_top):\n        if isinstance(_n, (_ast.Dict, _ast.Set, _ast.DictComp, _ast.SetComp)):\n            _bad.add(\"литерал словаря или множества\")\n        elif isinstance(_n, _ast.Call) and isinstance(_n.func, _ast.Name) and _n.func.id in (\"dict\", \"set\", \"frozenset\"):\n            _bad.add(_n.func.id + \"()\")\n        elif isinstance(_n, (_ast.Import, _ast.ImportFrom)):\n            _bad.add(\"import\")\nprint(\"словари и множества не использованы\" if not _bad else \"ЗАПРЕЩЕНО: \" + \", \".join(sorted(_bad)))\nprint(contains_nearby_duplicate([1, 2, 3, 1], 3), contains_nearby_duplicate([1, 0, 1, 1], 1), contains_nearby_duplicate([1, 2, 3, 1, 2, 3], 2), contains_nearby_duplicate([], 5), contains_nearby_duplicate([7], 0))\nnums = list(range(400000))\nprint(contains_nearby_duplicate(nums, 100000), contains_nearby_duplicate(nums + [0], 399999), contains_nearby_duplicate(nums + [0], 400000))\n", "expected": ["словари и множества не использованы", "True True False False False", "False False True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'two-sum-sorted-pointers', 0, 'stdout', 'Два указателя в отсортированном', 'Напишите функцию pair_with_sum(arr, target): в отсортированном по возрастанию списке найдите два разных элемента с суммой target и верните их индексы (i, j), i < j, либо None. Два указателя, O(n) времени и O(1) памяти: проверка подаёт миллион элементов.', 'def pair_with_sum(arr, target):
    pass
', 'i = 0, j = len - 1; сумма мала — i += 1, велика — j -= 1; пока i < j.', '{"driver": "print(pair_with_sum([1, 2, 4, 7, 11], 9), pair_with_sum([1, 2, 3], 10), pair_with_sum([], 1), pair_with_sum([5], 5))\nbig = list(range(1000000))\nprint(pair_with_sum(big, 1999997), pair_with_sum(big, 3000000))\n", "expected": ["(1, 3) None None None", "(999998, 999999) None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'pair-with-difference', 1, 'func', 'Пара с заданной разностью', 'Дан отсортированный по возрастанию список a и число k ≥ 0. Напишите функцию has_pair_diff(a, k): True, если есть два РАЗНЫХ индекса i ≠ j, для которых a[j] − a[i] == k. Два указателя идут в одну сторону. Проверка подаёт 300 000 чисел.', 'def has_pair_diff(a, k):
    pass
', 'Идём указателем j вправо, а i подтягиваем, пока разность больше k. Не забывайте про i == j: пара из элемента с самим собой не считается (важно при k = 0).', '{"func": "has_pair_diff", "tests": [{"args": [[1, 3, 5, 8, 12], 4], "expected": true}, {"args": [[1, 3, 5, 8, 12], 6], "expected": false}, {"args": [[1, 2, 3], 0], "expected": false}, {"args": [[2, 2, 3], 0], "expected": true}, {"args": [[], 1], "expected": false}, {"args": [[5], 0], "expected": false}, {"args": [[1, 5], 4], "expected": true}, {"args": [[1, 2, 4, 7, 11], 10], "expected": true}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'is-palindrome-two-pointers', 2, 'func', 'Палиндром', 'Напишите функцию is_palindrome(s): True, если строка читается одинаково в обе стороны, если не обращать внимания на регистр и на все символы, кроме букв и цифр. Идите двумя указателями с концов.', 'def is_palindrome(s):
    pass
', 'i, j = 0, len(s) - 1; пропускайте символы, у которых not ch.isalnum(); сравнивайте через lower().', '{"func": "is_palindrome", "tests": [{"args": ["А роза упала на лапу Азора"], "expected": true}, {"args": ["Was it a car or a cat I saw?"], "expected": true}, {"args": ["привет"], "expected": false}, {"args": [""], "expected": true}, {"args": [".,"], "expected": true}, {"args": ["ab"], "expected": false}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'valid-palindrome-one-deletion', 3, 'func', 'Палиндром с одним удалением', 'Напишите функцию valid_palindrome(s): True, если строка становится палиндромом после удаления не более одного символа. Идите указателями навстречу; на первом несовпадении проверьте два варианта: пропустить левый или правый символ. Проверка подаёт строки по 200 000 символов.', 'def valid_palindrome(s):
    pass
', 'Внутренняя функция ok(i, j) проверяет палиндромность среза; при первом несовпадении ответ — ok(i + 1, j) or ok(i, j − 1).', '{"func": "valid_palindrome", "tests": [{"args": ["aba"], "expected": true}, {"args": ["abca"], "expected": true}, {"args": ["abc"], "expected": false}, {"args": [""], "expected": true}, {"args": ["a"], "expected": true}, {"args": ["deeee"], "expected": true}, {"args": ["eedede"], "expected": true}, {"args": ["abbca"], "expected": true}, {"args": ["cbbcc"], "expected": true}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'remove-duplicates-sorted', 4, 'stdout', 'Убрать повторы на месте', 'Напишите функцию dedupe(arr): в отсортированном списке оставьте по одному экземпляру каждого значения НА МЕСТЕ (два указателя: читающий и пишущий), не создавая второго списка. Функция возвращает новую длину k, а первые k элементов arr — уникальные значения.', 'def dedupe(arr):
    pass
', 'w = 1; для r в 1..n-1: если arr[r] != arr[w - 1]: arr[w] = arr[r]; w += 1. Вернуть w (для пустого — 0).', '{"driver": "a = [1, 1, 2, 3, 3, 3, 4]\nk = dedupe(a)\nprint(k, a[:k])\nb = []\nprint(dedupe(b))\nc = [5, 5, 5]\nk = dedupe(c)\nprint(k, c[:k])\nbig = sorted([i // 3 for i in range(900000)])\nk = dedupe(big)\nprint(k, big[:3], big[k - 1])\n", "expected": ["4 [1, 2, 3, 4]", "0", "1 [5]", "300000 [0, 1, 2] 299999"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'remove-duplicates-at-most-two', 5, 'stdout', 'Не больше двух копий', 'Отсортированный список a. Напишите функцию remove_dups_two(a): оставьте каждое значение не более чем в двух экземплярах, на месте, сохранив порядок; верните новую длину k (первые k элементов — результат, хвост неважен). Проверка подаёт 500 000 элементов: сдвиги через pop и del не успеют.', 'def remove_dups_two(a):
    pass
', 'Условие записи: либо в результате меньше двух элементов, либо x отличается от a[k − 2] — предпоследнего записанного.', '{"driver": "a = [1, 1, 1, 2, 2, 3]\nk = remove_dups_two(a)\nprint(k, a[:k])\na = [0, 0, 1, 1, 1, 1, 2, 3, 3]\nk = remove_dups_two(a)\nprint(k, a[:k])\nb = []\nprint(remove_dups_two(b))\nc = [5]\nk = remove_dups_two(c)\nprint(k, c[:k])\nbig = [i // 4 for i in range(500000)]\nk = remove_dups_two(big)\nprint(k, big[:7], big[k - 3:k])\n", "expected": ["5 [1, 1, 2, 2, 3]", "7 [0, 0, 1, 1, 2, 3, 3]", "0", "1 [5]", "250000 [0, 0, 1, 1, 2, 2, 3] [124998, 124999, 124999]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'sorted-squares', 6, 'func', 'Отсортированные квадраты', 'Дан отсортированный по возрастанию список целых a (есть отрицательные). Напишите функцию sorted_squares(a): квадраты элементов по возрастанию за O(n): два указателя с концов, большие по модулю идут в результат с конца.', 'def sorted_squares(a):
    pass
', 'Самый большой квадрат — у одного из концов. Сравните |a[lo]| и |a[hi]|, запишите больший в результат с конца и сдвиньте соответствующий указатель.', '{"func": "sorted_squares", "tests": [{"args": [[-4, -1, 0, 3, 10]], "expected": [0, 1, 9, 16, 100]}, {"args": [[-7, -3, 2, 3, 11]], "expected": [4, 9, 9, 49, 121]}, {"args": [[1, 2, 3]], "expected": [1, 4, 9]}, {"args": [[-3, -2, -1]], "expected": [1, 4, 9]}, {"args": [[]], "expected": []}, {"args": [[0]], "expected": [0]}, {"args": [[-5, 5]], "expected": [25, 25]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'intersect-sorted', 7, 'stdout', 'Пересечение отсортированных', 'Два отсортированных по возрастанию списка. Напишите функцию intersect(a, b): их пересечение с учётом кратности (общие значения столько раз, сколько они есть в обоих списках), по возрастанию. Проверка подаёт по 500 000 элементов: поиск через x in b не успеет.', 'def intersect(a, b):
    pass
', 'Два указателя: равны — в ответ и оба вперёд; меньший — вперёд. Цикл while i < len(a) and j < len(b).', '{"driver": "print(intersect([1, 2, 2, 3, 5], [2, 2, 4, 5]), intersect([], [1]), intersect([1, 2], [3, 4]), intersect([1, 1, 1], [1, 1]))\na = list(range(0, 1000000, 2))\nb = list(range(0, 1000000, 3))\nr = intersect(a, b)\nprint(len(r), r[:4], r[-2:])\n", "expected": ["[2, 2, 5] [] [] [1, 1]", "166667 [0, 6, 12, 18] [999990, 999996]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'is-subsequence', 8, 'stdout', 'Подпоследовательность', 'Напишите функцию is_subsequence(s, t): True, если все символы s встречаются в t в том же порядке (не обязательно подряд). Пустая s — всегда подпоследовательность. Проверка подаёт t длиной 2 000 000.', 'def is_subsequence(s, t):
    pass
', 'i — позиция в s. Идём по t; если текущий символ равен s[i], сдвигаем i. В конце i == len(s).', '{"driver": "print(is_subsequence(\"ace\", \"abcde\"), is_subsequence(\"aec\", \"abcde\"), is_subsequence(\"\", \"abc\"), is_subsequence(\"a\", \"\"), is_subsequence(\"abc\", \"abc\"))\nt = \"ab\" * 1000000\nprint(is_subsequence(\"a\" * 1000000, t), is_subsequence(\"a\" * 1000001, t), is_subsequence(\"ba\" * 999999, t))\n", "expected": ["True False True False True", "True False True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'interval-intersections', 9, 'func', 'Пересечения интервалов', 'Даны два списка замкнутых интервалов [начало, конец]: внутри каждого списка интервалы не пересекаются и отсортированы. Напишите функцию interval_intersection(A, B): список всех непустых пересечений интервалов (в виде списков [начало, конец]) в порядке возрастания. Касание в одной точке — пересечение.', 'def interval_intersection(A, B):
    pass
', 'Пересечение двух интервалов: [max(начал), min(концов)] — если max ≤ min. Двигайте указатель того интервала, который закончился раньше.', '{"func": "interval_intersection", "tests": [{"args": [[[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]], "expected": [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]}, {"args": [[], [[1, 3]]], "expected": []}, {"args": [[[1, 3], [5, 9]], []], "expected": []}, {"args": [[[1, 7]], [[3, 10]]], "expected": [[3, 7]]}, {"args": [[[1, 3]], [[3, 5]]], "expected": [[3, 3]]}, {"args": [[[1, 2]], [[3, 4]]], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'container-most-water', 10, 'stdout', 'Больше всего воды', 'Дан список высот вертикальных линий. Напишите функцию most_water(heights): наибольшая площадь прямоугольника между двумя линиями — ширина (разница индексов) на меньшую из высот. Два указателя, O(n): проверка подаёт 200 000 линий.', 'def most_water(heights):
    pass
', 'Идите с обоих концов; всегда сдвигайте указатель у МЕНЬШЕЙ линии — большая её ширину не улучшит.', '{"driver": "print(most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]), most_water([1, 1]), most_water([4, 3, 2, 1, 4]), most_water([5]))\nbig = [min(i, 200000 - i) for i in range(200001)]\nprint(most_water(big))\n", "expected": ["49 1 16 0", "5000000000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'trap-rain-water', 11, 'stdout', 'Дождевая вода', 'Дана высота столбиков h. После дождя между ними застаивается вода. Напишите функцию trap(h): общий объём воды (каждый столбик шириной 1). Два указателя с концов и два максимума: двигайте сторону с меньшим максимумом. Проверка подаёт 500 000 столбиков.', 'def trap(h):
    pass
', 'Вода над столбиком = (меньший из максимумов слева и справа) − высота. Если h[lo] < h[hi], граница слева — максимум слева; считаем воду на lo и сдвигаем его.', '{"driver": "print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), trap([4, 2, 0, 3, 2, 5]), trap([]), trap([3]), trap([1, 2, 3]), trap([3, 0, 3]))\nh = [(i * 37) % 101 for i in range(500000)]\nprint(trap(h))\n", "expected": ["6 9 0 0 0 3", "24999535"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'sort-colors', 12, 'stdout', 'Сортировка цветов', 'В списке a лежат только 0, 1 и 2. Напишите функцию sort_colors(a): отсортируйте на месте за один проход и O(1) памяти (голландский флаг); ничего не возвращайте. Встроенный sort и счёт количеств запрещены по смыслу задачи, но проверка видит только результат. Проверка подаёт 1 000 000 элементов.', 'def sort_colors(a):
    pass
', 'lo — граница нулей, hi — граница двойки, mid идёт вперёд. Ноль меняем с lo (и lo, mid вперёд), двойку — с hi (только hi назад), единицу — пропускаем.', '{"driver": "a = [2, 0, 2, 1, 1, 0]\nsort_colors(a)\nprint(a)\nfor t in ([0], [], [1, 0], [2, 2, 2], [1, 2, 0, 1]):\n    t = list(t)\n    sort_colors(t)\n    print(t)\nn = 1000000\nbig = [(i * 7919) % 3 for i in range(n)]\nsort_colors(big)\nprint(big[0], big[n // 2], big[-1], big == sorted(big))\n", "expected": ["[0, 0, 1, 1, 2, 2]", "[0]", "[]", "[0, 1]", "[2, 2, 2]", "[0, 1, 1, 2]", "0 1 2 True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'sort-by-parity', 13, 'stdout', 'Чётные вперёд', 'Напишите функцию sort_by_parity(a): переставьте элементы списка на месте так, чтобы все чётные числа стояли раньше всех нечётных (порядок внутри групп не важен); ничего не возвращайте. Два указателя навстречу: левый ищет нечётное, правый — чётное, и они меняются. Проверка подаёт 1 000 000 элементов.', 'def sort_by_parity(a):
    pass
', 'Пока i < j: чётное слева — шагаем вправо; нечётное справа — шагаем влево; иначе (слева нечётное, справа чётное) меняем и сдвигаем оба.', '{"driver": "def check(src):\n    a = list(src)\n    sort_by_parity(a)\n    k = sum(1 for x in a if x % 2 == 0)\n    return sorted(a) == sorted(src) and all(x % 2 == 0 for x in a[:k]) and all(x % 2 == 1 for x in a[k:])\n\n\nprint(check([3, 1, 2, 4]), check([]), check([1]), check([2, 4]), check([1, 3, 5]), check([2, 1, 4, 3, 6, 5]))\nprint(check([(i * 7919) % 1009 for i in range(1000000)]))\n", "expected": ["True True True True True True", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'three-sum', 14, 'stdout', 'Тройки с нулевой суммой', 'Напишите функцию three_sum(a): все различные тройки значений (a[i], a[j], a[k]) с i < j < k и нулевой суммой. Каждая тройка — список по возрастанию; тройки — по возрастанию. Одинаковые тройки не повторяются. Время O(n²): сортировка и два указателя. Проверка подаёт 2 500 элементов — куб не успеет.', 'def three_sum(a):
    pass
', 'Сортировка; для каждого i (кроме повторяющихся значений) указатели lo = i + 1 и hi = n − 1. После найденной тройки сдвиньте оба и пропустите повторы lo.', '{"driver": "print(three_sum([-1, 0, 1, 2, -1, -4]), three_sum([0, 0, 0, 0]), three_sum([1, 2, 3]), three_sum([]), three_sum([-2, 0, 1, 1, 2]))\na = [(i * 7919) % 2001 - 1000 for i in range(2500)]\nr = three_sum(a)\nprint(len(r), r[:3], all(sum(t) == 0 for t in r))\n", "expected": ["[[-1, -1, 2], [-1, 0, 1]] [[0, 0, 0]] [] [] [[-2, 0, 2], [-2, 1, 1]]", "500246 [[-1000, 0, 1000], [-1000, 1, 999], [-1000, 2, 998]] True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'three-sum-closest', 15, 'stdout', 'Ближайшая сумма трёх', 'Напишите функцию three_sum_closest(a, target): сумму трёх элементов (на трёх разных позициях), наиболее близкую к target. Гарантируется ровно один ответ. Проверка подаёт 2 000 элементов.', 'def three_sum_closest(a, target):
    pass
', 'Как three_sum, но запоминайте сумму, ближайшую к target. Если s < target — lo вправо, если больше — hi влево.', '{"driver": "print(three_sum_closest([-1, 2, 1, -4], 1), three_sum_closest([0, 0, 0], 1), three_sum_closest([1, 1, 1, 0], -100), three_sum_closest([1, 2, 5, 10, 11], 12))\na = [(i * 104729) % 100003 for i in range(2000)]\nprint(three_sum_closest(a, 150000), three_sum_closest(a, 5))\n", "expected": ["2 0 2 13", "150002 263"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'count-pairs-sum-at-most', 16, 'stdout', 'Пары с суммой не больше k', 'Напишите функцию count_pairs_le(a, k): число пар индексов i < j с a[i] + a[j] ≤ k. Список неотсортирован. Отсортируйте копию и посчитайте двумя указателями. Проверка подаёт 200 000 элементов: перебор пар не успеет.', 'def count_pairs_le(a, k):
    pass
', 'Если b[lo] + b[hi] ≤ k, то b[lo] подходит со всеми элементами от lo + 1 до hi — прибавьте hi − lo и сдвиньте lo; иначе hi − 1.', '{"driver": "print(count_pairs_le([1, 2, 3, 4, 5, 6], 7), count_pairs_le([5, 1, 4], 5), count_pairs_le([], 3), count_pairs_le([2], 5), count_pairs_le([3, 3, 3], 6), count_pairs_le([3, 3, 3], 5))\na = [(i * 7919) % 10007 for i in range(200000)]\nprint(count_pairs_le(a, 10000), count_pairs_le(a, 20000))\n", "expected": ["9 1 0 0 3 0", "9988845001 19999884460"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'find-duplicate-floyd', 17, 'stdout', 'Дубликат без изменения массива', 'В списке a из n + 1 чисел значения лежат в диапазоне 1…n, и ровно одно число повторяется (возможно, несколько раз). Напишите функцию find_duplicate(a): повторяющееся число. Список менять нельзя, дополнительной памяти — O(1): смотрите на список как на связный (позиция i ведёт в позицию a[i]) и ищите вход в цикл по Флойду. Проверка подаёт 500 001 число.', 'def find_duplicate(a):
    pass
', 'Старт с индекса 0 (в него никто не ведёт). Первый заход: slow = a[slow], fast = a[a[fast]] до встречи. Второй: slow с нуля, оба по одному шагу — встретятся во входе в цикл.', '{"driver": "for a in ([1, 3, 4, 2, 2], [3, 1, 3, 4, 2], [1, 1], [2, 2, 2, 2, 2], [1, 4, 4, 2, 4]):\n    b = list(a)\n    print(find_duplicate(a), a == b)\nn = 500000\nbig = list(range(1, n + 1)) + [123457]\nx = 17\nfor i in range(n):\n    x = (x * 1103515245 + 12345) % 2147483648\n    j = x % (n + 1)\n    big[i], big[j] = big[j], big[i]\nsave = list(big)\nprint(find_duplicate(big), big == save)\n", "expected": ["2 True", "3 True", "1 True", "2 True", "4 True", "123457 True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'backspace-compare', 18, 'stdout', 'Сравнение с возвратом каретки', 'Символ ''#'' означает «удалить предыдущий символ» (в пустой строке ничего не происходит). Напишите функцию backspace_compare(s, t): равны ли строки после применения всех ''#''. Решение за O(1) дополнительной памяти: идите по обеим строкам справа налево с двумя указателями. Проверка подаёт строки по 1 000 000 символов.', 'def backspace_compare(s, t):
    pass
', 'Функция next_valid(x, i) идёт влево, считая ''#'' и пропуская столько обычных символов; возвращает позицию следующего «живого» символа или −1.', '{"driver": "print(backspace_compare(\"ab#c\", \"ad#c\"), backspace_compare(\"ab##\", \"c#d#\"), backspace_compare(\"a#c\", \"b\"), backspace_compare(\"\", \"a#\"), backspace_compare(\"a##c\", \"#a#c\"), backspace_compare(\"xywrrmp\", \"xywrrmu#p\"))\ns = \"ab#\" * 333333 + \"c\"\nt = \"a\" * 0 + \"ab#\" * 333333 + \"c\"\nprint(backspace_compare(s, t), backspace_compare(s, t[:-1] + \"d\"))\n", "expected": ["True True False True True True", "True False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 6, 'boats', 19, 'stdout', 'Лодки', 'Люди с весами w, каждая лодка выдерживает не более limit и несёт не более двух человек (вес каждого не больше limit). Напишите функцию num_boats(w, limit): наименьшее число лодок. Сортировка и два указателя: самый тяжёлый садится в лодку, к нему берём самого лёгкого, если вместе проходят. Проверка подаёт 300 000 человек.', 'def num_boats(w, limit):
    pass
', 'После сортировки самого тяжёлого посадим в любом случае (hi − 1); самого лёгкого берём с ним, если сумма не больше limit (lo + 1). Каждый шаг — одна лодка.', '{"driver": "print(num_boats([1, 2], 3), num_boats([3, 2, 2, 1], 3), num_boats([3, 5, 3, 4], 5), num_boats([], 5), num_boats([4], 5), num_boats([2, 2, 2], 4))\nw = [(i * 7919) % 5000 + 1 for i in range(300000)]\nprint(num_boats(w, 5000), num_boats(w, 6000), num_boats(w, 2600))\n", "expected": ["1 3 4 0 1 2", "150030 150000 222030"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'longest-unique-window', 0, 'stdout', 'Самая длинная подстрока без повторов', 'Напишите функцию longest_unique(s): длина самой длинной подстроки без повторяющихся символов. Скользящее окно, O(n): проверка подаёт строку из 500 000 символов.', 'def longest_unique(s):
    pass
', 'Словарь «символ → последний индекс» и левая граница окна: при повторе сдвиньте её на last[ch] + 1.', '{"driver": "print(longest_unique(''abcabcbb''), longest_unique(''bbbbb''), longest_unique(''pwwkew''), longest_unique(''''), longest_unique(''привет''))\nimport string\nbig = (string.ascii_lowercase * 20000)[:500000]\nprint(longest_unique(big))\nprint(longest_unique(''a'' * 500000))\n", "expected": ["3 1 3 0 6", "26", "1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'max-sum-window', 1, 'stdout', 'Окно фиксированной длины', 'Напишите функцию best_window(nums, k): наибольшая сумма k подряд идущих элементов (k <= len(nums), k >= 1). Не пересчитывайте сумму окна заново: сдвигайте её за O(1). Проверка — миллион элементов и окно в 100 000.', 'def best_window(nums, k):
    pass
', 'Сумма первого окна, затем window += nums[i] - nums[i - k] и обновление максимума.', '{"driver": "print(best_window([1, 4, 2, 10, 23, 3, 1, 0, 20], 4), best_window([5], 1), best_window([-1, -2, -3], 2))\nbig = list(range(1000000))\nprint(best_window(big, 100000))\n", "expected": ["39 5 -3", "94999950000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'find-anagrams', 2, 'stdout', 'Анаграммы в строке', 'Напишите функцию find_anagrams(s, p): список всех индексов i, где подстрока s[i:i+len(p)] — анаграмма строки p (по возрастанию). Окно шириной len(p) и счётчики символов; пересчёт при сдвиге за O(1). Проверка подаёт s длиной 300 000.', 'def find_anagrams(s, p):
    pass
', 'Хранить два словаря счётчиков и в каждом сдвиге сравнивать их целиком — O(k) на шаг. Лучше держать matched — число букв, чьи счётчики сейчас совпадают с образцом, и обновлять его при добавлении и удалении буквы.', '{"driver": "print(find_anagrams(\"cbaebabacd\", \"abc\"), find_anagrams(\"abab\", \"ab\"), find_anagrams(\"a\", \"ab\"), find_anagrams(\"aaa\", \"aa\"), find_anagrams(\"\", \"a\"))\ns = \"abc\" * 100000\nprint(len(find_anagrams(s, \"cab\")), find_anagrams(s, \"abcc\")[:2])\n", "expected": ["[0, 6] [0, 1, 2] [] [0, 1] []", "299998 [2, 5]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'min-subarray-len', 3, 'stdout', 'Самый короткий подмассив с суммой', 'Напишите функцию min_subarray_len(target, a): наименьшая длина подряд идущего куска натуральных чисел a с суммой не меньше target, или 0, если такого нет. Окно переменной длины. Проверка подаёт 500 000 чисел.', 'def min_subarray_len(target, a):
    pass
', 'Расширяйте правую границу, накапливая сумму. Пока сумма ≥ target — фиксируйте длину и сжимайте левую (вычитая её элемент).', '{"driver": "print(min_subarray_len(7, [2, 3, 1, 2, 4, 3]), min_subarray_len(4, [1, 4, 4]), min_subarray_len(11, [1, 1, 1, 1, 1, 1, 1, 1]), min_subarray_len(5, [5]), min_subarray_len(3, []))\na = [(i * 7919) % 100 + 1 for i in range(500000)]\nprint(min_subarray_len(1000, a), min_subarray_len(10 ** 9, a), min_subarray_len(5000000, a))\n", "expected": ["2 1 0 1 0", "18 0 99008"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'longest-ones-flip-k', 4, 'stdout', 'Единицы с заменами', 'Дан список из 0 и 1 и число k. Напишите функцию longest_ones(a, k): длина самого длинного подряд идущего куска, в котором после замены не более k нулей на единицы остаются одни единицы (то есть в куске не больше k нулей). Проверка подаёт 500 000 элементов.', 'def longest_ones(a, k):
    pass
', 'Окно с числом нулей не больше k. Расширяем правую границу; если нулей стало больше k, сжимаем левую, пока не станет допустимо. Ответ — максимальная ширина окна.', '{"driver": "print(longest_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2), longest_ones([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3), longest_ones([], 1), longest_ones([0, 0], 0), longest_ones([1], 0))\na = [0 if (i * 7919) % 11 == 0 else 1 for i in range(500000)]\nprint(longest_ones(a, 0), longest_ones(a, 5), longest_ones(a, 1000))\n", "expected": ["6 10 0 0 1", "10 65 11010"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'fruit-baskets', 5, 'stdout', 'Фрукты в двух корзинах', 'Вдоль ряда деревьев растут фрукты разных видов (список f). Вы идёте слева направо и можете собирать фрукты лишь двух разных видов. Напишите функцию total_fruit(f): длина самого длинного подряд идущего куска ряда, в котором не больше двух различных видов. Проверка подаёт 500 000 деревьев.', 'def total_fruit(f):
    pass
', 'Окно и словарь видов → количество. Когда видов стало больше двух, сжимайте слева, удаляя вид из словаря при нуле.', '{"driver": "print(total_fruit([1, 2, 1]), total_fruit([0, 1, 2, 2]), total_fruit([1, 2, 3, 2, 2]), total_fruit([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4]), total_fruit([]), total_fruit([5]))\nf = [(i // 50) % 7 if i % 3 else (i // 70) % 5 for i in range(500000)]\nprint(total_fruit(f), total_fruit([i % 2 for i in range(500000)]))\n", "expected": ["3 3 4 5 0 1", "101 500000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'char-replacement', 6, 'stdout', 'Замена символов', 'Дана строка s из заглавных латинских букв и число k. Напишите функцию char_replacement(s, k): длина самой длинной подстроки, которую можно превратить в строку из одинаковых букв не более чем k заменами. Окно, в котором «длина окна − частота самой частой буквы ≤ k». Проверка подаёт 300 000 символов.', 'def char_replacement(s, k):
    pass
', 'Достаточно хранить максимальную частоту в окне (её можно не уменьшать при сжатии — ответ от этого не портится). Окно допустимо, пока длина − максимальная частота ≤ k.', '{"driver": "print(char_replacement(\"ABAB\", 2), char_replacement(\"AABABBA\", 1), char_replacement(\"\", 3), char_replacement(\"A\", 0), char_replacement(\"ABC\", 0))\ns = \"\".join(\"ABCD\"[(i * i) % 4 + (i // 7) % 2] if (i * 31) % 5 else \"A\" for i in range(300000))\nprint(char_replacement(s, 0), char_replacement(s, 10), char_replacement(s, 1000))\n", "expected": ["4 4 0 1 1", "3 21 1753"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'product-less-than-k', 7, 'stdout', 'Подмассивы с малым произведением', 'Дан список натуральных чисел a и число k. Напишите функцию count_product_less(a, k): число подряд идущих непустых подмассивов, произведение элементов которых строго меньше k. Окно: для каждого правого конца считайте, сколько левых начал допустимо. Проверка подаёт 300 000 чисел.', 'def count_product_less(a, k):
    pass
', 'Правый конец r; пока произведение окна ≥ k — сжимаем левую границу. Допустимых подмассивов, заканчивающихся в r, ровно r − l + 1.', '{"driver": "print(count_product_less([10, 5, 2, 6], 100), count_product_less([1, 2, 3], 0), count_product_less([1, 1, 1], 2), count_product_less([], 5), count_product_less([5], 5), count_product_less([5], 6))\na = [(i * 7919) % 5 + 1 for i in range(300000)]\nprint(count_product_less(a, 1000), count_product_less(a, 10 ** 6))\n", "expected": ["8 0 6 0 0 1", "2039979 4139911"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'min-window-substring', 8, 'func', 'Минимальное окно', 'Напишите функцию min_window_len(s, t): длина самой короткой подстроки s, содержащей все символы t (с учётом кратности), либо 0, если такой нет. Скользящее окно с двумя указателями.', 'def min_window_len(s, t):
    pass
', 'need = Counter(t); расширяйте правую границу, пока окно не покрывает need, затем сжимайте левую, обновляя минимум.', '{"func": "min_window_len", "tests": [{"args": ["ADOBECODEBANC", "ABC"], "expected": 4}, {"args": ["a", "a"], "expected": 1}, {"args": ["a", "aa"], "expected": 0}, {"args": ["abc", ""], "expected": 0}, {"args": ["aaflslflsldkalskaaa", "aaa"], "expected": 3}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'max-in-windows', 9, 'stdout', 'Максимум в каждом окне', 'Напишите функцию max_sliding(a, k): список максимумов всех окон длины k (слева направо). Монотонная очередь индексов (collections.deque) даёт O(n). Проверка: 400 000 элементов и окно 20 000 — max(a[i:i+k]) в цикле не успеет.', 'from collections import deque


def max_sliding(a, k):
    pass
', 'В очереди — индексы, значения по убыванию. Новый x выталкивает с конца всех, кто ≤ x. С головы убирайте индекс, вышедший из окна (dq[0] ≤ i − k). Ответ окна — a[dq[0]].', '{"driver": "print(max_sliding([1, 3, -1, -3, 5, 3, 6, 7], 3), max_sliding([1], 1), max_sliding([9, 11], 2), max_sliding([4, 3, 2, 1], 2), max_sliding([1, 2, 3, 4], 4))\na = [(i * 7919) % 100003 for i in range(400000)]\nr = max_sliding(a, 20000)\nprint(len(r), r[0], r[-1], sum(r) % 1000003)\n", "expected": ["[3, 3, 5, 5, 6, 7] [1] [11] [4, 3, 2] [4]", "380001 100001 99990 40951"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'hanoi-moves', 10, 'stdout', 'Ханойские башни', 'Напишите функцию hanoi(n): список ходов (из, в) для перекладывания n дисков со стержня ''A'' на ''C'' через ''B'' (можно класть меньший диск на больший, а не наоборот). Ходы — кортежи (''A'', ''C''). Разделяй и властвуй: n−1 дисков на запасной, самый большой на цель, n−1 дисков на цель. Для n = 0 — пустой список.', 'def hanoi(n):
    pass
', 'Внутренняя рекурсивная функция go(k, откуда, через, куда): k − 1 дисков откуда→через, ход откуда→куда, k − 1 дисков через→куда.', '{"driver": "print(hanoi(0), hanoi(1), hanoi(2), hanoi(3))\nm = hanoi(18)\nprint(len(m), m[0], m[-1], m[len(m) // 2])\npegs = {\"A\": list(range(10, 0, -1)), \"B\": [], \"C\": []}\nok = True\nfor a, c in hanoi(10):\n    d = pegs[a].pop()\n    if pegs[c] and pegs[c][-1] < d:\n        ok = False\n    pegs[c].append(d)\nprint(ok, pegs[\"C\"] == list(range(10, 0, -1)), len(pegs[\"A\"]), len(pegs[\"B\"]))\n", "expected": ["[] [(''A'', ''C'')] [(''A'', ''B''), (''A'', ''C''), (''B'', ''C'')] [(''A'', ''C''), (''A'', ''B''), (''C'', ''B''), (''A'', ''C''), (''B'', ''A''), (''B'', ''C''), (''A'', ''C'')]", "262143 (''A'', ''B'') (''B'', ''C'') (''A'', ''C'')", "True True 0 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'count-inversions', 11, 'stdout', 'Число инверсий', 'Напишите функцию count_inversions(arr): сколько пар (i, j) с i < j и arr[i] > arr[j]. Разделяй и властвуй (модификация сортировки слиянием), O(n log n): проверка подаёт 100 000 элементов в обратном порядке.', 'def count_inversions(arr):
    pass
', 'При слиянии, если берём элемент ПРАВОЙ половины, он «перепрыгивает» все оставшиеся в левой: прибавляйте len(left) - i.', '{"driver": "print(count_inversions([2, 4, 1, 3, 5]), count_inversions([1, 2, 3]), count_inversions([3, 2, 1]), count_inversions([]))\nn = 100000\nprint(count_inversions(list(range(n, 0, -1))) == n * (n - 1) // 2)\n", "expected": ["3 0 3 0", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'max-subarray-divide', 12, 'stdout', 'Лучший подотрезок: разделяй и властвуй', 'Напишите функцию best_sum(nums): наибольшая сумма непрерывного непустого подотрезка (список не пустой), но рекурсивно: лучший отрезок либо целиком слева, либо целиком справа, либо пересекает середину (тогда его можно найти за линейное время). Глубина рекурсии должна быть O(log n).', 'def best_sum(nums):
    pass
', 'Разделите пополам; ответ = max(лучший слева, лучший справа, лучший суффикс слева + лучший префикс справа).', '{"driver": "import sys\nsys.setrecursionlimit(200)\nprint(best_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]), best_sum([-5]), best_sum([2, 3, -10, 4, 5]), best_sum([-3, -1, -2]))\nprint(best_sum([1, -1] * 100000 + [5]))\n", "expected": ["6 -5 9 -1", "5"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 7, 'segment-tree-class', 13, 'stdout', 'Дерево отрезков', 'Реализуйте класс SegmentTree(a): построение по списку чисел и два метода: query(l, r) — сумма a[l..r] включительно, update(i, v) — присвоить a[i] = v. Обе операции — O(log n). Проверка подаёт 100 000 элементов и по 100 000 запросов и обновлений: сумма срезом на каждый запрос не успеет.', 'class SegmentTree:
    def __init__(self, a):
        self.n = len(a)
        self.t = [0] * (2 * self.n)
        # построить дерево

    def update(self, i, v):
        pass

    def query(self, l, r):
        pass
', 'Нижний уровень массива t — сами значения (позиции n…2n−1), родитель узла i — i // 2, t[i] = t[2i] + t[2i+1]. В query идите l и r вверх: нечётный левый край берём и сдвигаем, нечётный правый — отступаем и берём.', '{"driver": "st = SegmentTree([5, 3, 7, 1, 4, 6, 2, 8])\nprint(st.query(0, 7), st.query(1, 6), st.query(3, 3), st.query(2, 4))\nst.update(3, 5)\nprint(st.query(0, 7), st.query(2, 4), st.query(3, 3))\none = SegmentTree([9])\nprint(one.query(0, 0))\none.update(0, 4)\nprint(one.query(0, 0))\nn = 100000\na = [(i * 7919) % 1000 for i in range(n)]\nst = SegmentTree(a)\nx = 5\ntotal = 0\nfor i in range(100000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    l = x % n\n    x = (x * 1103515245 + 12345) % 2147483648\n    r = l + x % (n - l)\n    if i % 2:\n        st.update(l, x % 1000)\n    else:\n        total += st.query(l, r)\nprint(total, st.query(0, n - 1))\n", "expected": ["36 23 1 12", "40 16 5", "9", "4", "622797724702 50004502"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-find-first', 0, 'func', 'Первое вхождение: наивный поиск', 'Напишите функцию find_first(text, pat): индекс первого вхождения образца pat в строку text или -1, если его нет. Пустой образец встречается в позиции 0. Решите двумя вложенными циклами: сдвиг и посимвольное сравнение, без find, index и in.', 'def find_first(text, pat):
    pass
', 'Для каждого сдвига i сравнивайте text[i + j] и pat[j], пока символы равны; дошли до длины образца — нашли.', '{"func": "find_first", "tests": [{"args": ["hello world", "o w"], "expected": 4}, {"args": ["aaa", "aaaa"], "expected": -1}, {"args": ["abc", ""], "expected": 0}, {"args": ["", "a"], "expected": -1}, {"args": ["abcabcd", "abcd"], "expected": 3}, {"args": ["aaaaab", "aab"], "expected": 3}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-common-prefix', 1, 'func', 'Общее начало слов', 'Напишите функцию common_prefix(words): наибольшее общее начало всех слов списка. Для пустого списка или если общего начала нет — пустая строка.', 'def common_prefix(words):
    pass
', 'Возьмите первое слово как образец и укорачивайте длину общего начала по каждому следующему слову.', '{"func": "common_prefix", "tests": [{"args": [["flower", "flow", "flight"]], "expected": "fl"}, {"args": [["dog", "racecar"]], "expected": ""}, {"args": [[]], "expected": ""}, {"args": [["same", "same"]], "expected": "same"}, {"args": [["a"]], "expected": "a"}, {"args": [["ab", "abc", "a"]], "expected": "a"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-count-overlap', 2, 'func', 'Сколько раз встречается, включая перекрытия', 'Напишите функцию count_overlapping(text, pat): число вхождений образца pat (он непустой) в text, при этом вхождения могут перекрываться: в «aaaa» образец «aa» встречается три раза.', 'def count_overlapping(text, pat):
    pass
', 'После каждого найденного вхождения сдвигайтесь всего на одну позицию, а не на длину образца.', '{"func": "count_overlapping", "tests": [{"args": ["aaaa", "aa"], "expected": 3}, {"args": ["abababa", "aba"], "expected": 3}, {"args": ["abc", "d"], "expected": 0}, {"args": ["a", "a"], "expected": 1}, {"args": ["mississippi", "issi"], "expected": 2}, {"args": ["xyz", "xyzxyz"], "expected": 0}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-prefix-function', 3, 'func', 'Префикс-функция', 'Напишите функцию prefix_function(s): список p той же длины, где p[i] — длина наибольшего собственного префикса подстроки s[0..i], совпадающего с её суффиксом. Для «abacaba» ответ [0, 0, 1, 0, 1, 2, 3]. Время — линейное.', 'def prefix_function(s):
    pass
', 'Держите k — текущую длину совпадения; при несовпадении откатывайтесь: k = p[k - 1].', '{"func": "prefix_function", "tests": [{"args": ["abacaba"], "expected": [0, 0, 1, 0, 1, 2, 3]}, {"args": ["aaaa"], "expected": [0, 1, 2, 3]}, {"args": ["abcd"], "expected": [0, 0, 0, 0]}, {"args": ["abababab"], "expected": [0, 0, 1, 2, 3, 4, 5, 6]}, {"args": [""], "expected": []}, {"args": ["a"], "expected": [0]}, {"args": ["aabaaab"], "expected": [0, 1, 0, 1, 2, 2, 3]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-longest-border', 4, 'func', 'Самая длинная граница', 'Граница строки — собственный префикс, равный суффиксу. Напишите функцию longest_border(s): самая длинная граница в виде строки (пустая, если границ нет). Для «abacaba» это «aba».', 'def longest_border(s):
    pass
', 'Последнее значение префикс-функции — длина самой длинной границы.', '{"func": "longest_border", "tests": [{"args": ["abacaba"], "expected": "aba"}, {"args": ["abcd"], "expected": ""}, {"args": ["aaaa"], "expected": "aaa"}, {"args": ["abab"], "expected": "ab"}, {"args": [""], "expected": ""}, {"args": ["xyxyxyx"], "expected": "xyxyx"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-min-period', 5, 'func', 'Наименьший период', 'Напишите функцию min_period(s): наименьшая длина p, при которой строка целиком состоит из повторений своих первых p символов (p делит длину). Если такого p меньше длины нет, ответ — длина строки; для пустой строки — 0. Например, для «abcabcabc» ответ 3, для «abcab» — 5.', 'def min_period(s):
    pass
', 'Кандидат в периоды — длина минус последнее значение префикс-функции; проверьте, что он делит длину.', '{"func": "min_period", "tests": [{"args": ["abcabcabc"], "expected": 3}, {"args": ["abcab"], "expected": 5}, {"args": ["aaaa"], "expected": 1}, {"args": ["abab"], "expected": 2}, {"args": ["a"], "expected": 1}, {"args": [""], "expected": 0}, {"args": ["abaaba"], "expected": 3}, {"args": ["abaab"], "expected": 5}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-kmp-search', 6, 'stdout', 'Поиск Кнута — Морриса — Пратта', 'Напишите функцию find_all(text, pat): список начал всех вхождений образца в текст (с перекрытиями) по возрастанию. Пустой образец встречается в каждой позиции от 0 до len(text). Время — порядка n + m: проверка подаёт текст в миллион символов и образец в триста тысяч. Запрещены find, index, count, startswith, split, replace, in и re.', 'def find_all(text, pat):
    pass
', 'Постройте префикс-функцию образца, затем идите по тексту: указатель по тексту не возвращается, k откатывается по таблице.', '{"driver": "import ast as _ast\n_src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n_bad = set()\nfor _n in _ast.walk(_ast.parse(_src)):\n    if isinstance(_n, _ast.Attribute) and _n.attr in {''endswith'', ''find'', ''replace'', ''rfind'', ''split'', ''rindex'', ''partition'', ''startswith'', ''index'', ''count''}:\n        _bad.add(\".\" + _n.attr + \"()\")\n    elif True and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, _ast.NotIn)) for _o in _n.ops):\n        _bad.add(\"in\")\n    elif False and isinstance(_n, _ast.Slice):\n        _bad.add(\"срезы\")\n    elif isinstance(_n, _ast.Import) and any(_a.name.split(\".\")[0] in {''re''} for _a in _n.names):\n        _bad.add(\"import\")\n    elif isinstance(_n, _ast.ImportFrom) and (_n.module or \"\").split(\".\")[0] in {''re''}:\n        _bad.add(\"import\")\nif _bad:\n    print(\"запрещённые приёмы:\", \", \".join(sorted(_bad)))\nelse:\n    print(find_all(\"abracadabra\", \"abra\"), find_all(\"aaaa\", \"aa\"), find_all(\"abc\", \"d\"), find_all(\"abc\", \"\"))\n    big = \"a\" * 1000000\n    print(len(find_all(big, \"a\" * 300000 + \"b\")))\n    r = find_all(big, \"a\" * 300000)\n    print(len(r), r[0], r[-1])\n    r = find_all(\"ab\" * 400000, \"abab\")\n    print(len(r), r[1], r[-1])\n", "expected": ["[0, 7] [0, 1, 2] [] [0, 1, 2, 3]", "0", "700001 0 700000", "399999 2 799996"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-prefix-occurrences', 7, 'func', 'Сколько раз встречается каждый префикс', 'Напишите функцию prefix_occurrences(s): список ans, где ans[l - 1] — сколько раз префикс длины l встречается в s как подстрока (с перекрытиями). Для «abab» ответ [2, 2, 1, 1]. Время — линейное.', 'def prefix_occurrences(s):
    pass
', 'Каждое значение префикс-функции — вхождение префикса этой длины; затем «протолкните» счётчики по цепочке p[l - 1].', '{"func": "prefix_occurrences", "tests": [{"args": ["abab"], "expected": [2, 2, 1, 1]}, {"args": ["aaa"], "expected": [3, 2, 1]}, {"args": ["abc"], "expected": [1, 1, 1]}, {"args": ["abacaba"], "expected": [4, 2, 2, 1, 1, 1, 1]}, {"args": [""], "expected": []}, {"args": ["a"], "expected": [1]}, {"args": ["aabaab"], "expected": [4, 2, 2, 1, 1, 1]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-is-rotation', 8, 'stdout', 'Циклический сдвиг', 'Напишите функцию is_rotation(a, b): можно ли получить b циклическим сдвигом a. Время — линейное: проверка подаёт строки по пятьсот тысяч символов. Запрещены срезы, find, index, count, startswith, split, replace, in и re.', 'def is_rotation(a, b):
    pass
', 'b — сдвиг a, если b встречается в склейке a + a; ищите её префикс-функцией, не создавая лишних копий.', '{"driver": "import ast as _ast\n_src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n_bad = set()\nfor _n in _ast.walk(_ast.parse(_src)):\n    if isinstance(_n, _ast.Attribute) and _n.attr in {''endswith'', ''find'', ''replace'', ''rfind'', ''split'', ''rindex'', ''partition'', ''startswith'', ''index'', ''count''}:\n        _bad.add(\".\" + _n.attr + \"()\")\n    elif True and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, _ast.NotIn)) for _o in _n.ops):\n        _bad.add(\"in\")\n    elif True and isinstance(_n, _ast.Slice):\n        _bad.add(\"срезы\")\n    elif isinstance(_n, _ast.Import) and any(_a.name.split(\".\")[0] in {''re''} for _a in _n.names):\n        _bad.add(\"import\")\n    elif isinstance(_n, _ast.ImportFrom) and (_n.module or \"\").split(\".\")[0] in {''re''}:\n        _bad.add(\"import\")\nif _bad:\n    print(\"запрещённые приёмы:\", \", \".join(sorted(_bad)))\nelse:\n    print(is_rotation(\"abcde\", \"cdeab\"), is_rotation(\"abcde\", \"abced\"), is_rotation(\"\", \"\"), is_rotation(\"a\", \"ab\"))\n    a = \"a\" * 500000 + \"b\"\n    print(is_rotation(a, \"a\" * 300000 + \"b\" + \"a\" * 200000))\n    print(is_rotation(a, \"a\" * 500000 + \"c\"))\n    print(is_rotation(\"ab\" * 250000, \"ba\" * 250000))\n", "expected": ["True False True False", "True", "False", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-shortest-palindrome', 9, 'stdout', 'Кратчайший палиндром приписыванием', 'Напишите функцию shortest_palindrome(s): припишите к s слева минимальное число символов так, чтобы получился палиндром, и верните результат. Для «abcd» ответ «dcbabcd». Время — линейное: проверка подаёт строку в четыреста тысяч символов. Запрещены find, index, count, startswith, split, replace, in и re.', 'def shortest_palindrome(s):
    pass
', 'Найдите самый длинный палиндромный префикс: префикс-функция строки s + разделитель + развёрнутая s.', '{"driver": "import ast as _ast\n_src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n_bad = set()\nfor _n in _ast.walk(_ast.parse(_src)):\n    if isinstance(_n, _ast.Attribute) and _n.attr in {''endswith'', ''find'', ''replace'', ''rfind'', ''split'', ''rindex'', ''partition'', ''startswith'', ''index'', ''count''}:\n        _bad.add(\".\" + _n.attr + \"()\")\n    elif True and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, _ast.NotIn)) for _o in _n.ops):\n        _bad.add(\"in\")\n    elif False and isinstance(_n, _ast.Slice):\n        _bad.add(\"срезы\")\n    elif isinstance(_n, _ast.Import) and any(_a.name.split(\".\")[0] in {''re''} for _a in _n.names):\n        _bad.add(\"import\")\n    elif isinstance(_n, _ast.ImportFrom) and (_n.module or \"\").split(\".\")[0] in {''re''}:\n        _bad.add(\"import\")\nif _bad:\n    print(\"запрещённые приёмы:\", \", \".join(sorted(_bad)))\nelse:\n    print(shortest_palindrome(\"aacecaaa\"), shortest_palindrome(\"abcd\"), repr(shortest_palindrome(\"\")), shortest_palindrome(\"a\"))\n    r = shortest_palindrome(\"abcd\" * 100000)\n    print(len(r), r[:6], r[-6:])\n    r = shortest_palindrome(\"a\" * 200000 + \"b\")\n    print(len(r), r[:3], r[-3:])\n", "expected": ["aaacecaaa dcbabcd '''' a", "799999 dcbadc cdabcd", "200002 baa aab"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-z-function', 10, 'func', 'Зет-функция', 'Напишите функцию z_function(s): список z, где z[i] — длина наибольшего общего начала строки s и её суффикса, начинающегося в позиции i. Значение z[0] считаем равным 0. Для «aabxaab» ответ [0, 1, 0, 0, 3, 1, 0]. Время — линейное.', 'def z_function(s):
    pass
', 'Храните зет-блок [l, r): внутри него начинайте с min(r − i, z[i − l]), затем расширяйте посимвольно.', '{"func": "z_function", "tests": [{"args": ["aabxaab"], "expected": [0, 1, 0, 0, 3, 1, 0]}, {"args": ["aaaa"], "expected": [0, 3, 2, 1]}, {"args": ["abc"], "expected": [0, 0, 0]}, {"args": [""], "expected": []}, {"args": ["a"], "expected": [0]}, {"args": ["abababab"], "expected": [0, 0, 6, 0, 4, 0, 2, 0]}, {"args": ["aabaaab"], "expected": [0, 1, 0, 2, 3, 1, 0]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-z-search', 11, 'stdout', 'Поиск через зет-функцию', 'Напишите функцию z_count(text, pat): число вхождений непустого образца в текст (с перекрытиями) через зет-функцию склейки pat + разделитель + text. Время — линейное: проверка подаёт текст в миллион символов. Запрещены find, index, count, startswith, split, replace, in и re.', 'def z_count(text, pat):
    pass
', 'z[i] == len(pat) на позиции i > len(pat) означает вхождение; разделитель не даёт z вырасти больше длины образца.', '{"driver": "import ast as _ast\n_src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n_bad = set()\nfor _n in _ast.walk(_ast.parse(_src)):\n    if isinstance(_n, _ast.Attribute) and _n.attr in {''endswith'', ''find'', ''replace'', ''rfind'', ''split'', ''rindex'', ''partition'', ''startswith'', ''index'', ''count''}:\n        _bad.add(\".\" + _n.attr + \"()\")\n    elif True and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, _ast.NotIn)) for _o in _n.ops):\n        _bad.add(\"in\")\n    elif False and isinstance(_n, _ast.Slice):\n        _bad.add(\"срезы\")\n    elif isinstance(_n, _ast.Import) and any(_a.name.split(\".\")[0] in {''re''} for _a in _n.names):\n        _bad.add(\"import\")\n    elif isinstance(_n, _ast.ImportFrom) and (_n.module or \"\").split(\".\")[0] in {''re''}:\n        _bad.add(\"import\")\nif _bad:\n    print(\"запрещённые приёмы:\", \", \".join(sorted(_bad)))\nelse:\n    print(z_count(\"abracadabra\", \"abra\"), z_count(\"aaaa\", \"aa\"), z_count(\"abc\", \"d\"))\n    big = \"a\" * 1000000\n    print(z_count(big, \"a\" * 300000), z_count(big, \"a\" * 300000 + \"b\"))\n    print(z_count(\"ab\" * 500000, \"abab\"))\n", "expected": ["2 3 0", "700001 0", "499999"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-hash-substring', 12, 'stdout', 'Хеш подстроки за константу', 'Напишите класс SubHash: конструктор SubHash(s) считает хеши префиксов; метод get(l, r) возвращает хеш подстроки s[l:r] за O(1), метод same(l1, l2, length) — True, если подстроки s[l1:l1+length] и s[l2:l2+length] равны (сравнение по хешам, без срезов). Используйте большой модуль, например 2^61 − 1. Проверка: строка в девятьсот тысяч символов и двести тысяч запросов. Запрещены срезы, find, index, count, startswith, split, replace, in и re.', 'class SubHash:
    def __init__(self, s):
        pass

    def get(self, l, r):
        pass

    def same(self, l1, l2, length):
        pass
', 'H[i + 1] = (H[i] · B + код символа) mod M; хеш [l, r) = H[r] − H[l] · B^(r − l) mod M.', '{"driver": "import ast as _ast\n_src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n_bad = set()\nfor _n in _ast.walk(_ast.parse(_src)):\n    if isinstance(_n, _ast.Attribute) and _n.attr in {''endswith'', ''find'', ''replace'', ''rfind'', ''split'', ''rindex'', ''partition'', ''startswith'', ''index'', ''count''}:\n        _bad.add(\".\" + _n.attr + \"()\")\n    elif True and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, _ast.NotIn)) for _o in _n.ops):\n        _bad.add(\"in\")\n    elif True and isinstance(_n, _ast.Slice):\n        _bad.add(\"срезы\")\n    elif isinstance(_n, _ast.Import) and any(_a.name.split(\".\")[0] in {''re''} for _a in _n.names):\n        _bad.add(\"import\")\n    elif isinstance(_n, _ast.ImportFrom) and (_n.module or \"\").split(\".\")[0] in {''re''}:\n        _bad.add(\"import\")\nif _bad:\n    print(\"запрещённые приёмы:\", \", \".join(sorted(_bad)))\nelse:\n    t = SubHash(\"abracadabra\")\n    print(t.same(0, 7, 4), t.same(1, 8, 3), t.same(0, 3, 2), t.same(2, 9, 0))\n    def nxt(x):\n        x ^= (x << 13) & 0xFFFFFFFF\n        x ^= x >> 17\n        x ^= (x << 5) & 0xFFFFFFFF\n        return x\n    s = \"abc\" * 300000\n    h = SubHash(s)\n    n = len(s)\n    x = 12345\n    total = 0\n    for _ in range(200000):\n        x = nxt(x)\n        l1 = x % n\n        x = nxt(x)\n        l2 = x % n\n        x = nxt(x)\n        length = x % (n - max(l1, l2) + 1)\n        if h.same(l1, l2, length):\n            total += 1\n    print(total)\n", "expected": ["True True False True", "66636"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-rabin-karp', 13, 'stdout', 'Алгоритм Рабина — Карпа', 'Напишите функцию rabin_karp(text, pat): индекс первого вхождения pat в text или -1; пустой образец — 0. Считайте хеш образца и скользящий хеш окна (модуль большой, например 2^61 − 1), а при равенстве хешей сверяйте строки. Проверка: текст в миллион символов и образец в триста тысяч. Запрещены срезы, find, index, count, startswith, split, replace, in и re.', 'def rabin_karp(text, pat):
    pass
', 'Окно: ht = ((ht − код ушедшего · B^(m−1)) · B + код нового) mod M; не забывайте брать остаток после вычитания.', '{"driver": "import ast as _ast\n_src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n_bad = set()\nfor _n in _ast.walk(_ast.parse(_src)):\n    if isinstance(_n, _ast.Attribute) and _n.attr in {''endswith'', ''find'', ''replace'', ''rfind'', ''split'', ''rindex'', ''partition'', ''startswith'', ''index'', ''count''}:\n        _bad.add(\".\" + _n.attr + \"()\")\n    elif True and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, _ast.NotIn)) for _o in _n.ops):\n        _bad.add(\"in\")\n    elif True and isinstance(_n, _ast.Slice):\n        _bad.add(\"срезы\")\n    elif isinstance(_n, _ast.Import) and any(_a.name.split(\".\")[0] in {''re''} for _a in _n.names):\n        _bad.add(\"import\")\n    elif isinstance(_n, _ast.ImportFrom) and (_n.module or \"\").split(\".\")[0] in {''re''}:\n        _bad.add(\"import\")\nif _bad:\n    print(\"запрещённые приёмы:\", \", \".join(sorted(_bad)))\nelse:\n    print(rabin_karp(\"hello world\", \"o w\"), rabin_karp(\"abc\", \"abcd\"), rabin_karp(\"abc\", \"\"), rabin_karp(\"abcabc\", \"cab\"))\n    big = \"a\" * 1000000\n    print(rabin_karp(big, \"a\" * 300000 + \"b\"))\n    print(rabin_karp(big + \"b\", \"a\" * 300000 + \"b\"))\n    print(rabin_karp(\"ab\" * 400000 + \"c\", \"abababc\"))\n", "expected": ["4 -1 0 2", "-1", "700000", "799994"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-trie', 14, 'stdout', 'Префиксное дерево', 'Напишите класс Trie с методами insert(word), contains(word) → bool и count_prefix(prefix) → сколько различных вставленных слов начинается с prefix (пустая приставка — все слова). Повторная вставка слова ничего не меняет. Проверка: сто тысяч слов и сто тысяч запросов — перебор списка не уложится.', 'class Trie:
    def __init__(self):
        pass

    def insert(self, word):
        pass

    def contains(self, word):
        pass

    def count_prefix(self, prefix):
        pass
', 'В узле храните словарь детей, признак конца слова и сколько слов проходит через узел.', '{"driver": "t = Trie()\nfor w in [\"to\", \"tea\", \"ten\", \"in\", \"to\"]:\n    t.insert(w)\nprint(t.contains(\"te\"), t.contains(\"ten\"), t.count_prefix(\"te\"), t.count_prefix(\"\"), t.count_prefix(\"x\"))\ndef nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nx = 777\ndef rnd():\n    global x\n    x = nxt(x)\n    return x\nwords = []\nbig = Trie()\nfor _ in range(100000):\n    w = \"\".join(\"abcdefgh\"[rnd() % 8] for _ in range(1 + rnd() % 12))\n    words.append(w)\n    big.insert(w)\nprint(sum(big.contains(words[rnd() % 100000]) for _ in range(20000)))\ntotal = 0\nfor _ in range(100000):\n    w = words[rnd() % 100000]\n    total += big.count_prefix(w[: 1 + rnd() % 6])\nprint(total, big.count_prefix(\"\"))\n", "expected": ["False True 2 4 0", "20000", "229381066 69785"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-autocomplete', 15, 'func', 'Автодополнение', 'Напишите функцию autocomplete(words, prefix, k): первые k слов (без повторов) из списка words, которые начинаются с prefix, в алфавитном порядке. Если таких слов меньше k — вернуть сколько есть.', 'def autocomplete(words, prefix, k):
    pass
', 'Спуститесь в бор по приставке и обойдите поддерево, посещая детей по алфавиту, пока не наберёте k слов.', '{"func": "autocomplete", "tests": [{"args": [["tea", "ten", "to", "in", "tea"], "te", 5], "expected": ["tea", "ten"]}, {"args": [["tea", "ten", "to", "in"], "t", 2], "expected": ["tea", "ten"]}, {"args": [["a", "b"], "c", 3], "expected": []}, {"args": [["b", "ab", "a"], "", 2], "expected": ["a", "ab"]}, {"args": [[], "x", 1], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-edit-distance', 16, 'func', 'Расстояние Левенштейна', 'Напишите функцию edit_distance(a, b): минимальное число вставок, удалений и замен символа, которое превращает a в b. Для «kitten» и «sitting» ответ 3. Время — порядка len(a) · len(b).', 'def edit_distance(a, b):
    pass
', 'd[i][j] = d[i − 1][j − 1], если символы равны; иначе 1 + min из трёх соседей. Хватит двух строк таблицы.', '{"func": "edit_distance", "tests": [{"args": ["kitten", "sitting"], "expected": 3}, {"args": ["", "abc"], "expected": 3}, {"args": ["abc", "abc"], "expected": 0}, {"args": ["flaw", "lawn"], "expected": 2}, {"args": ["intention", "execution"], "expected": 5}, {"args": ["abc", ""], "expected": 3}, {"args": ["a", "b"], "expected": 1}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-one-edit', 17, 'func', 'Одна правка', 'Напишите функцию one_edit_away(a, b): True, если a можно превратить в b не более чем одной вставкой, удалением или заменой символа (строки равны — тоже True). Время — линейное, без таблицы.', 'def one_edit_away(a, b):
    pass
', 'Найдите первую позицию, где строки расходятся, и проверьте оставшиеся хвосты для трёх случаев длины.', '{"func": "one_edit_away", "tests": [{"args": ["pale", "ple"], "expected": true}, {"args": ["pales", "pale"], "expected": true}, {"args": ["pale", "bale"], "expected": true}, {"args": ["pale", "bake"], "expected": false}, {"args": ["same", "same"], "expected": true}, {"args": ["", "a"], "expected": true}, {"args": ["", "ab"], "expected": false}, {"args": ["abc", "ab"], "expected": true}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-lcs', 18, 'func', 'Наибольшая общая подпоследовательность', 'Напишите функцию lcs_length(a, b): длина наибольшей общей подпоследовательности двух строк — символы идут в том же порядке, но не обязательно подряд. Для «abcde» и «ace» ответ 3.', 'def lcs_length(a, b):
    pass
', 'Совпали последние символы — длина на единицу больше, чем у префиксов; иначе максимум из «без последнего в a» и «без последнего в b».', '{"func": "lcs_length", "tests": [{"args": ["abcde", "ace"], "expected": 3}, {"args": ["abc", "def"], "expected": 0}, {"args": ["", "a"], "expected": 0}, {"args": ["AGGTAB", "GXTXAYB"], "expected": 4}, {"args": ["aaaa", "aa"], "expected": 2}, {"args": ["abc", "abc"], "expected": 3}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 8, 'str-distinct-substrings', 19, 'stdout', 'Сколько различных подстрок', 'Напишите функцию count_distinct(s): число различных непустых подстрок строки s. Для «aaa» ответ 3, для «abab» — 7. Хранить все подстроки нельзя: проверка подаёт строки в две тысячи символов, а память песочницы ограничена. Идея: при дописывании символа к префиксу длины i появляются новые подстроки — суффиксы, которых раньше не было. Их число равно i минус наибольшее значение префикс-функции развёрнутого префикса.', 'def count_distinct(s):
    pass
', 'Новые подстроки при дописывании символа — это суффиксы, ещё не встречавшиеся раньше; их длина — i минус максимум π развёрнутого префикса.', '{"driver": "print(count_distinct(\"aaa\"), count_distinct(\"abab\"), count_distinct(\"abc\"), count_distinct(\"\"))\nprint(count_distinct(\"a\" * 2000), count_distinct(\"ab\" * 1000))\ndef nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nx = 99\ns = []\nfor _ in range(1500):\n    x = nxt(x)\n    s.append(\"abc\"[(x >> 10) % 3])\nprint(count_distinct(\"\".join(s)))\n", "expected": ["3 7 6 0", "2000 3999", "1117153"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-gcd', 0, 'func', 'Наибольший общий делитель', 'Напишите функцию gcd(a, b): наибольший общий делитель неотрицательных чисел алгоритмом Евклида. gcd(a, 0) = a. Числа в проверках достигают 10^30 — перебор делителей не уложится.', 'def gcd(a, b):
    pass
', 'Пока b не ноль, заменяйте пару (a, b) на (b, a % b).', '{"func": "gcd", "tests": [{"args": [48, 18], "expected": 6}, {"args": [0, 5], "expected": 5}, {"args": [17, 0], "expected": 17}, {"args": [0, 0], "expected": 0}, {"args": [7, 13], "expected": 1}, {"args": [1267650600228229401496703205376, 808281277464764060643139600456536293376], "expected": 1125899906842624}, {"args": [498454011879264, 308061521170129], "expected": 1}, {"args": [1000000000000000000000000000001, 1000000000000000], "expected": 1}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-lcm', 1, 'func', 'Наименьшее общее кратное списка', 'Напишите функцию lcm_list(nums): наименьшее общее кратное всех положительных чисел списка. Для пустого списка — 1. Подсказка: lcm(a, b) = a / gcd(a, b) · b.', 'def lcm_list(nums):
    pass
', 'Накапливайте результат: res = res // gcd(res, v) * v.', '{"func": "lcm_list", "tests": [{"args": [[4, 6]], "expected": 12}, {"args": [[]], "expected": 1}, {"args": [[7]], "expected": 7}, {"args": [[2, 3, 5, 7, 11, 13]], "expected": 30030}, {"args": [[12, 18, 24]], "expected": 72}, {"args": [[1000000007, 1000000009]], "expected": 1000000016000000063}, {"args": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]], "expected": 232792560}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-ext-gcd', 2, 'stdout', 'Расширенный алгоритм Евклида', 'Напишите функцию ext_gcd(a, b): кортеж (g, x, y), где g — наибольший общий делитель неотрицательных a и b, а целые x и y удовлетворяют a·x + b·y = g. Подойдёт любая пара (x, y), проверка подставляет её в равенство.', 'def ext_gcd(a, b):
    pass
', 'Рекурсивно: (g, x, y) = ext_gcd(b, a % b), затем x'' = y, y'' = x − (a // b)·y.', '{"driver": "import math\npairs = [(30, 18), (18, 30), (7, 0), (0, 7), (240, 46), (10 ** 18 + 9, 10 ** 9 + 7), (2 ** 89 - 1, 3 ** 40), (1, 1), (0, 0), (35, 15)]\nbad = []\nfor a, b in pairs:\n    r = ext_gcd(a, b)\n    if not (isinstance(r, tuple) and len(r) == 3):\n        bad.append((a, b, \"не кортеж из трёх чисел\"))\n        continue\n    g, x, y = r\n    if g != math.gcd(a, b) or a * x + b * y != g:\n        bad.append((a, b))\nprint(\"ошибки:\", bad)\n", "expected": ["ошибки: []"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-mod-inverse', 3, 'func', 'Обратный по модулю', 'Напишите функцию mod_inverse(a, m): такое x от 0 до m − 1, что a·x ≡ 1 (mod m), или -1, если обратного нет (a и m не взаимно просты). Модуль m ≥ 2, не обязательно простой.', 'def mod_inverse(a, m):
    pass
', 'Ведите коэффициенты при a вместе с остатками — это итеративный расширенный Евклид.', '{"func": "mod_inverse", "tests": [{"args": [3, 7], "expected": 5}, {"args": [10, 17], "expected": 12}, {"args": [2, 4], "expected": -1}, {"args": [1, 2], "expected": 1}, {"args": [123456789, 1000000007], "expected": 18633540}, {"args": [6, 9], "expected": -1}, {"args": [-3, 7], "expected": 2}, {"args": [14, 15], "expected": 14}, {"args": [999999999999, 1000000000039], "expected": 975000000038}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-pow-mod', 4, 'func', 'Быстрое возведение в степень по модулю', 'Напишите функцию power_mod(b, e, m): b в степени e по модулю m (m ≥ 1, e ≥ 0). Показатель может быть порядка 10^18 — нужно порядка log e умножений. Без встроенного pow с тремя аргументами.', 'def power_mod(b, e, m):
    pass
', 'Идите по двоичным разрядам e: если разряд единица — умножайте результат на текущую степень b; затем возводите b в квадрат.', '{"func": "power_mod", "tests": [{"args": [2, 10, 1000], "expected": 24}, {"args": [3, 13, 1000000007], "expected": 1594323}, {"args": [5, 0, 7], "expected": 1}, {"args": [7, 1, 1], "expected": 0}, {"args": [2, 1000000000000000000, 1000000007], "expected": 719476260}, {"args": [123456789, 987654321987654321, 998244353], "expected": 89607075}, {"args": [0, 0, 5], "expected": 1}, {"args": [10, 1000000000000000001, 1000000000039], "expected": 906917793724}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-fib-mod', 5, 'func', 'Число Фибоначчи за логарифм', 'Напишите функцию fib_mod(n, m): n-е число Фибоначчи по модулю m (F(0) = 0, F(1) = 1). n бывает порядка 10^18, поэтому нужна быстрая степень матрицы или формулы удвоения.', 'def fib_mod(n, m):
    pass
', 'Возведите матрицу [[1, 1], [1, 0]] в степень n по модулю m; число Фибоначчи — элемент в углу.', '{"func": "fib_mod", "tests": [{"args": [0, 10], "expected": 0}, {"args": [1, 10], "expected": 1}, {"args": [10, 1000], "expected": 55}, {"args": [50, 1000000007], "expected": 586268941}, {"args": [1000000000000000000, 1000000007], "expected": 209783453}, {"args": [1000000000000000000, 1000], "expected": 875}, {"args": [90, 1000000000000000000000000000000], "expected": 2880067194370816120}, {"args": [2, 1], "expected": 0}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-is-prime', 6, 'func', 'Проверка на простоту', 'Напишите функцию is_prime(n): True, если n простое (n ≥ 0; 0 и 1 — не простые). Числа в проверках достигают 10^12, поэтому делители ищите только до корня из n.', 'def is_prime(n):
    pass
', 'Проверьте двойку отдельно, затем делители 3, 5, 7, … пока d · d ≤ n.', '{"func": "is_prime", "tests": [{"args": [0], "expected": false}, {"args": [1], "expected": false}, {"args": [2], "expected": true}, {"args": [3], "expected": true}, {"args": [4], "expected": false}, {"args": [91], "expected": false}, {"args": [97], "expected": true}, {"args": [999999999989], "expected": true}, {"args": [1000000000039], "expected": true}, {"args": [1000000000037], "expected": false}, {"args": [2147483647], "expected": true}, {"args": [999985999949], "expected": false}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-sieve', 7, 'stdout', 'Решето Эратосфена', 'Напишите функцию primes_upto(n): список всех простых чисел от 2 до n включительно. Проверка просит все простые до пяти миллионов — пробное деление не уложится в лимит времени.', 'def primes_upto(n):
    pass
', 'Заведите массив отметок; для каждого неотмеченного i с i·i ≤ n отметьте i·i, i·i + i, … (срезом это быстрее).', '{"driver": "print(primes_upto(30), primes_upto(1), primes_upto(2))\np = primes_upto(5000000)\nprint(len(p), p[-1], sum(p[:100]))\n", "expected": ["[2, 3, 5, 7, 11, 13, 17, 19, 23, 29] [] [2]", "348513 4999999 24133"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-goldbach', 8, 'func', 'Разбиение Гольдбаха', 'Напишите функцию goldbach(n): для чётного n ≥ 4 верните наименьшее простое p, при котором n − p тоже простое (например, для 28 это 5, потому что 23 простое). Проверки доходят до 10^6.', 'def goldbach(n):
    pass
', 'Постройте решето до n и найдите первое простое p, для которого n − p тоже отмечено простым.', '{"func": "goldbach", "tests": [{"args": [4], "expected": 2}, {"args": [6], "expected": 3}, {"args": [28], "expected": 5}, {"args": [100], "expected": 3}, {"args": [1000], "expected": 3}, {"args": [1000000], "expected": 17}, {"args": [999998], "expected": 19}, {"args": [98], "expected": 19}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-factorize', 9, 'func', 'Разложение на простые множители', 'Напишите функцию factorize(n): разложение n ≥ 1 на простые множители — список кортежей (простое, степень) по возрастанию простых. Для 1 — пустой список; например, factorize(12) = [(2, 2), (3, 1)]. Числа достигают 10^12: делите пробно до корня.', 'def factorize(n):
    pass
', 'Делите на d, пока делится, записывая степень; после цикла остаток больше 1 — это простой множитель.', '{"func": "factorize", "tests": [{"args": [1], "expected": []}, {"args": [12], "expected": [{"__tuple__": [2, 2]}, {"__tuple__": [3, 1]}]}, {"args": [97], "expected": [{"__tuple__": [97, 1]}]}, {"args": [600851475143], "expected": [{"__tuple__": [71, 1]}, {"__tuple__": [839, 1]}, {"__tuple__": [1471, 1]}, {"__tuple__": [6857, 1]}]}, {"args": [1000000000000], "expected": [{"__tuple__": [2, 12]}, {"__tuple__": [5, 12]}]}, {"args": [999999999989], "expected": [{"__tuple__": [999999999989, 1]}]}, {"args": [2147483647], "expected": [{"__tuple__": [2147483647, 1]}]}, {"args": [8633], "expected": [{"__tuple__": [89, 1]}, {"__tuple__": [97, 1]}]}, {"args": [720720], "expected": [{"__tuple__": [2, 4]}, {"__tuple__": [3, 2]}, {"__tuple__": [5, 1]}, {"__tuple__": [7, 1]}, {"__tuple__": [11, 1]}, {"__tuple__": [13, 1]}]}, {"args": [1099511627776], "expected": [{"__tuple__": [2, 40]}]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-spf', 10, 'stdout', 'Разложение через таблицу делителей', 'Напишите класс Factorizer: конструктор Factorizer(limit) строит таблицу наименьших простых делителей до limit, метод factor(n) (2 ≤ n ≤ limit) возвращает список кортежей (простое, степень) по возрастанию. Проверка: таблица до трёх миллионов и триста тысяч запросов — пробное деление не успеет.', 'class Factorizer:
    def __init__(self, limit):
        pass

    def factor(self, n):
        pass
', 'Решето: spf[j] = i для составных j, которые ещё не получили делитель; factor делит n на spf[n], пока n > 1.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nf = Factorizer(3000000)\nprint(f.factor(84), f.factor(97), f.factor(2 ** 20), f.factor(2999999))\nN = 3000000\ns = bytearray([1]) * (N + 1)\ns[0] = s[1] = 0\nfor i in range(2, 1733):\n    if s[i]:\n        s[i * i :: i] = bytearray(len(range(i * i, N + 1, i)))\nprimes = [i for i in range(2000000, N + 1) if s[i]]\nx = 2024\ntotal = 0\ndistinct = 0\nfor q in range(300000):\n    x = nxt(x)\n    n = primes[x % len(primes)] if q % 2 else 2 + x % 2999999\n    r = f.factor(n)\n    distinct += len(r)\n    total += sum(e for _, e in r)\nprint(distinct, total)\n", "expected": ["[(2, 2), (3, 1), (7, 1)] [(97, 1)] [(2, 20)] [(2999999, 1)]", "590231 705430"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-divisor-count', 11, 'func', 'Количество делителей', 'Напишите функцию divisor_count(n): сколько натуральных делителей у n ≥ 1 (включая 1 и n). Числа достигают 10^12: раскладывайте на простые и перемножайте (степень + 1).', 'def divisor_count(n):
    pass
', 'Разложите n: ответ — произведение (e + 1) по всем простым множителям.', '{"func": "divisor_count", "tests": [{"args": [1], "expected": 1}, {"args": [36], "expected": 9}, {"args": [97], "expected": 2}, {"args": [1000000000000], "expected": 169}, {"args": [963761198400], "expected": 6720}, {"args": [1099511627776], "expected": 41}, {"args": [999999999989], "expected": 2}, {"args": [720720], "expected": 240}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-euler-phi', 12, 'func', 'Функция Эйлера', 'Напишите функцию euler_phi(n): сколько чисел от 1 до n взаимно просты с n (φ(1) = 1). Для n = p₁ᵉ¹ · … ответ равен n · ∏(1 − 1/p). Числа достигают 10^12.', 'def euler_phi(n):
    pass
', 'Для каждого простого делителя p выполните result -= result // p, после чего выделите p из n целиком.', '{"func": "euler_phi", "tests": [{"args": [1], "expected": 1}, {"args": [2], "expected": 1}, {"args": [9], "expected": 6}, {"args": [10], "expected": 4}, {"args": [36], "expected": 12}, {"args": [97], "expected": 96}, {"args": [1000000000000], "expected": 400000000000}, {"args": [999999999989], "expected": 999999999988}, {"args": [720720], "expected": 138240}, {"args": [1099511627776], "expected": 549755813888}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-binom', 13, 'stdout', 'Биномиальные коэффициенты по модулю', 'Напишите класс Binom: конструктор Binom(limit, p) (p простое, p > limit) готовит факториалы и обратные факториалы по модулю p; метод c(n, k) возвращает C(n, k) mod p за O(1) (0, если k < 0 или k > n). Проверка: limit = 10^6 и триста тысяч запросов.', 'class Binom:
    def __init__(self, limit, p):
        pass

    def c(self, n, k):
        pass
', 'f[n] = n! mod p; обратный к f[limit] — степень p − 2, остальные: inv[i − 1] = inv[i] · i.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nP = 10 ** 9 + 7\nb = Binom(1000000, P)\nprint(b.c(5, 2), b.c(10, 0), b.c(10, 11), b.c(10, 10), b.c(1000000, 500000))\nx = 31337\ntotal = 0\nfor _ in range(300000):\n    x = nxt(x)\n    n = x % 1000001\n    x = nxt(x)\n    k = x % (n + 1)\n    total = (total + b.c(n, k)) % P\nprint(total)\n", "expected": ["10 1 0 1 996692777", "960654159"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-pow2', 14, 'func', 'Степень двойки', 'Напишите функцию is_power_of_two(x): True, если x — степень двойки (1, 2, 4, 8, …). Нуль и отрицательные числа — False. Без циклов и без логарифмов: одним битовым выражением.', 'def is_power_of_two(x):
    pass
', 'У степени двойки единственная единица в двоичной записи: x & (x − 1) сбрасывает её и даёт 0.', '{"func": "is_power_of_two", "tests": [{"args": [1], "expected": true}, {"args": [2], "expected": true}, {"args": [3], "expected": false}, {"args": [0], "expected": false}, {"args": [-4], "expected": false}, {"args": [1024], "expected": true}, {"args": [1267650600228229401496703205376], "expected": true}, {"args": [1267650600228229401496703205377], "expected": false}, {"args": [6], "expected": false}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-popcount', 15, 'func', 'Число единиц в двоичной записи', 'Напишите функцию popcount(x): сколько единиц в двоичной записи неотрицательного x. Цикл должен выполняться столько раз, сколько в числе единиц: используйте x & (x − 1). Без bin(), count и bit_count.', 'def popcount(x):
    pass
', 'Пока x не ноль, сбрасывайте младшую единицу и увеличивайте счётчик.', '{"func": "popcount", "tests": [{"args": [0], "expected": 0}, {"args": [1], "expected": 1}, {"args": [44], "expected": 3}, {"args": [255], "expected": 8}, {"args": [1606938044258990275541962092341162602522202993782792835301375], "expected": 200}, {"args": [10715086071862673209484250490600018105614048117055336074437503883703510511249361224931983788156958581275946729175531468251871452856923140435984577574698574803934567774824230985421074605062371141877954182153046474983581941267398767559165543946077062914571196477686542167660429831652624386837205668069376], "expected": 1}, {"args": [18446744078004518913], "expected": 3}, {"args": [12345678901234567890], "expected": 32}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-gray', 16, 'func', 'Код Грея', 'Напишите функцию gray_code(n): список из 2ⁿ чисел — кодов Грея длины n в порядке номеров, где соседние коды отличаются ровно одним битом. Формула: i ^ (i >> 1). Для n = 0 — [0].', 'def gray_code(n):
    pass
', 'Код с номером i равен i XOR (i >> 1).', '{"func": "gray_code", "tests": [{"args": [0], "expected": [0]}, {"args": [1], "expected": [0, 1]}, {"args": [2], "expected": [0, 1, 3, 2]}, {"args": [3], "expected": [0, 1, 3, 2, 6, 7, 5, 4]}, {"args": [4], "expected": [0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8]}, {"args": [10], "expected": [0, 1, 3, 2, 6, 7, 5, 4, 12, 13, 15, 14, 10, 11, 9, 8, 24, 25, 27, 26, 30, 31, 29, 28, 20, 21, 23, 22, 18, 19, 17, 16, 48, 49, 51, 50, 54, 55, 53, 52, 60, 61, 63, 62, 58, 59, 57, 56, 40, 41, 43, 42, 46, 47, 45, 44, 36, 37, 39, 38, 34, 35, 33, 32, 96, 97, 99, 98, 102, 103, 101, 100, 108, 109, 111, 110, 106, 107, 105, 104, 120, 121, 123, 122, 126, 127, 125, 124, 116, 117, 119, 118, 114, 115, 113, 112, 80, 81, 83, 82, 86, 87, 85, 84, 92, 93, 95, 94, 90, 91, 89, 88, 72, 73, 75, 74, 78, 79, 77, 76, 68, 69, 71, 70, 66, 67, 65, 64, 192, 193, 195, 194, 198, 199, 197, 196, 204, 205, 207, 206, 202, 203, 201, 200, 216, 217, 219, 218, 222, 223, 221, 220, 212, 213, 215, 214, 210, 211, 209, 208, 240, 241, 243, 242, 246, 247, 245, 244, 252, 253, 255, 254, 250, 251, 249, 248, 232, 233, 235, 234, 238, 239, 237, 236, 228, 229, 231, 230, 226, 227, 225, 224, 160, 161, 163, 162, 166, 167, 165, 164, 172, 173, 175, 174, 170, 171, 169, 168, 184, 185, 187, 186, 190, 191, 189, 188, 180, 181, 183, 182, 178, 179, 177, 176, 144, 145, 147, 146, 150, 151, 149, 148, 156, 157, 159, 158, 154, 155, 153, 152, 136, 137, 139, 138, 142, 143, 141, 140, 132, 133, 135, 134, 130, 131, 129, 128, 384, 385, 387, 386, 390, 391, 389, 388, 396, 397, 399, 398, 394, 395, 393, 392, 408, 409, 411, 410, 414, 415, 413, 412, 404, 405, 407, 406, 402, 403, 401, 400, 432, 433, 435, 434, 438, 439, 437, 436, 444, 445, 447, 446, 442, 443, 441, 440, 424, 425, 427, 426, 430, 431, 429, 428, 420, 421, 423, 422, 418, 419, 417, 416, 480, 481, 483, 482, 486, 487, 485, 484, 492, 493, 495, 494, 490, 491, 489, 488, 504, 505, 507, 506, 510, 511, 509, 508, 500, 501, 503, 502, 498, 499, 497, 496, 464, 465, 467, 466, 470, 471, 469, 468, 476, 477, 479, 478, 474, 475, 473, 472, 456, 457, 459, 458, 462, 463, 461, 460, 452, 453, 455, 454, 450, 451, 449, 448, 320, 321, 323, 322, 326, 327, 325, 324, 332, 333, 335, 334, 330, 331, 329, 328, 344, 345, 347, 346, 350, 351, 349, 348, 340, 341, 343, 342, 338, 339, 337, 336, 368, 369, 371, 370, 374, 375, 373, 372, 380, 381, 383, 382, 378, 379, 377, 376, 360, 361, 363, 362, 366, 367, 365, 364, 356, 357, 359, 358, 354, 355, 353, 352, 288, 289, 291, 290, 294, 295, 293, 292, 300, 301, 303, 302, 298, 299, 297, 296, 312, 313, 315, 314, 318, 319, 317, 316, 308, 309, 311, 310, 306, 307, 305, 304, 272, 273, 275, 274, 278, 279, 277, 276, 284, 285, 287, 286, 282, 283, 281, 280, 264, 265, 267, 266, 270, 271, 269, 268, 260, 261, 263, 262, 258, 259, 257, 256, 768, 769, 771, 770, 774, 775, 773, 772, 780, 781, 783, 782, 778, 779, 777, 776, 792, 793, 795, 794, 798, 799, 797, 796, 788, 789, 791, 790, 786, 787, 785, 784, 816, 817, 819, 818, 822, 823, 821, 820, 828, 829, 831, 830, 826, 827, 825, 824, 808, 809, 811, 810, 814, 815, 813, 812, 804, 805, 807, 806, 802, 803, 801, 800, 864, 865, 867, 866, 870, 871, 869, 868, 876, 877, 879, 878, 874, 875, 873, 872, 888, 889, 891, 890, 894, 895, 893, 892, 884, 885, 887, 886, 882, 883, 881, 880, 848, 849, 851, 850, 854, 855, 853, 852, 860, 861, 863, 862, 858, 859, 857, 856, 840, 841, 843, 842, 846, 847, 845, 844, 836, 837, 839, 838, 834, 835, 833, 832, 960, 961, 963, 962, 966, 967, 965, 964, 972, 973, 975, 974, 970, 971, 969, 968, 984, 985, 987, 986, 990, 991, 989, 988, 980, 981, 983, 982, 978, 979, 977, 976, 1008, 1009, 1011, 1010, 1014, 1015, 1013, 1012, 1020, 1021, 1023, 1022, 1018, 1019, 1017, 1016, 1000, 1001, 1003, 1002, 1006, 1007, 1005, 1004, 996, 997, 999, 998, 994, 995, 993, 992, 928, 929, 931, 930, 934, 935, 933, 932, 940, 941, 943, 942, 938, 939, 937, 936, 952, 953, 955, 954, 958, 959, 957, 956, 948, 949, 951, 950, 946, 947, 945, 944, 912, 913, 915, 914, 918, 919, 917, 916, 924, 925, 927, 926, 922, 923, 921, 920, 904, 905, 907, 906, 910, 911, 909, 908, 900, 901, 903, 902, 898, 899, 897, 896, 640, 641, 643, 642, 646, 647, 645, 644, 652, 653, 655, 654, 650, 651, 649, 648, 664, 665, 667, 666, 670, 671, 669, 668, 660, 661, 663, 662, 658, 659, 657, 656, 688, 689, 691, 690, 694, 695, 693, 692, 700, 701, 703, 702, 698, 699, 697, 696, 680, 681, 683, 682, 686, 687, 685, 684, 676, 677, 679, 678, 674, 675, 673, 672, 736, 737, 739, 738, 742, 743, 741, 740, 748, 749, 751, 750, 746, 747, 745, 744, 760, 761, 763, 762, 766, 767, 765, 764, 756, 757, 759, 758, 754, 755, 753, 752, 720, 721, 723, 722, 726, 727, 725, 724, 732, 733, 735, 734, 730, 731, 729, 728, 712, 713, 715, 714, 718, 719, 717, 716, 708, 709, 711, 710, 706, 707, 705, 704, 576, 577, 579, 578, 582, 583, 581, 580, 588, 589, 591, 590, 586, 587, 585, 584, 600, 601, 603, 602, 606, 607, 605, 604, 596, 597, 599, 598, 594, 595, 593, 592, 624, 625, 627, 626, 630, 631, 629, 628, 636, 637, 639, 638, 634, 635, 633, 632, 616, 617, 619, 618, 622, 623, 621, 620, 612, 613, 615, 614, 610, 611, 609, 608, 544, 545, 547, 546, 550, 551, 549, 548, 556, 557, 559, 558, 554, 555, 553, 552, 568, 569, 571, 570, 574, 575, 573, 572, 564, 565, 567, 566, 562, 563, 561, 560, 528, 529, 531, 530, 534, 535, 533, 532, 540, 541, 543, 542, 538, 539, 537, 536, 520, 521, 523, 522, 526, 527, 525, 524, 516, 517, 519, 518, 514, 515, 513, 512]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-subsets', 17, 'func', 'Все подмножества масками', 'Напишите функцию all_subsets(items): список всех подмножеств списка (каждое — список) в порядке масок 0, 1, …, 2ⁿ − 1; бит с номером i маски означает, что в подмножество входит items[i]; элементы внутри подмножества идут в порядке индексов. Для [1, 2] — [[], [1], [2], [1, 2]].', 'def all_subsets(items):
    pass
', 'Для каждой маски от 0 до 2ⁿ − 1 соберите элементы, чьи биты включены.', '{"func": "all_subsets", "tests": [{"args": [[1, 2]], "expected": [[], [1], [2], [1, 2]]}, {"args": [[]], "expected": [[]]}, {"args": [["a", "b", "c"]], "expected": [[], ["a"], ["b"], ["a", "b"], ["c"], ["a", "c"], ["b", "c"], ["a", "b", "c"]]}, {"args": [[5]], "expected": [[], [5]]}, {"args": [[3, 1, 2, 4]], "expected": [[], [3], [1], [3, 1], [2], [3, 2], [1, 2], [3, 1, 2], [4], [3, 4], [1, 4], [3, 1, 4], [2, 4], [3, 2, 4], [1, 2, 4], [3, 1, 2, 4]]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-single-number', 18, 'stdout', 'Единственное непарное число', 'Напишите функцию single_number(nums): в списке каждое число встречается дважды, кроме одного; верните это число. Время — линейное, память — константа. Словари, множества, sorted, count и index запрещены: проверка подаёт два миллиона чисел.', 'def single_number(nums):
    pass
', 'Исключающее или: a ^ a = 0, a ^ 0 = a — пары сократятся, останется одно число.', '{"driver": "import ast as _ast\n_src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n_bad = set()\nfor _n in _ast.walk(_ast.parse(_src)):\n    if isinstance(_n, _ast.Attribute) and _n.attr in {''count'', ''index''}:\n        _bad.add(\".\" + _n.attr + \"()\")\n    elif True and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, _ast.NotIn)) for _o in _n.ops):\n        _bad.add(\"in\")\n    elif False and isinstance(_n, _ast.Slice):\n        _bad.add(\"срезы\")\n    elif isinstance(_n, _ast.Name) and _n.id in {''set'', ''sorted'', ''dict'', ''Counter'', ''defaultdict'', ''frozenset''}:\n        _bad.add(_n.id)\n    elif type(_n).__name__ in {''Set'', ''DictComp'', ''SetComp'', ''Dict''}:\n        _bad.add(\"словари и множества\")\n    elif isinstance(_n, _ast.Import) and any(_a.name.split(\".\")[0] in {''re''} for _a in _n.names):\n        _bad.add(\"import\")\n    elif isinstance(_n, _ast.ImportFrom) and (_n.module or \"\").split(\".\")[0] in {''re''}:\n        _bad.add(\"import\")\nif _bad:\n    print(\"запрещённые приёмы:\", \", \".join(sorted(_bad)))\nelse:\n    print(single_number([4, 1, 2, 1, 2]), single_number([7]), single_number([-3, 5, 5]))\n    x = 7\n    a = []\n    def nxt(x):\n        x ^= (x << 13) & 0xFFFFFFFF\n        x ^= x >> 17\n        x ^= (x << 5) & 0xFFFFFFFF\n        return x\n    for i in range(1000000):\n        x = nxt(x)\n        a.append(x)\n    a.append(123456789012)\n    a = a + a[:-1]\n    a = a[1:] + a[:1]\n    print(single_number(a))\n", "expected": ["4 7 -3", "123456789012"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 9, 'num-tsp', 19, 'func', 'Коммивояжёр динамикой по маскам', 'Напишите функцию tsp(dist): dist — квадратная матрица расстояний между n городами (dist[i][j] — путь из i в j, может быть несимметричной). Верните длину кратчайшего цикла, который начинается и заканчивается в городе 0 и посещает каждый город ровно один раз; для одного города — 0. Городов до 13: перебор всех перестановок не уложится, нужна динамика dp[маска][последний город].', 'def tsp(dist):
    pass
', 'dp[mask][v] — длина кратчайшего пути из 0 через города маски, заканчивающегося в v; переходы — в ещё не посещённый город.', '{"func": "tsp", "tests": [{"args": [[[0]]], "expected": 0}, {"args": [[[0, 5], [7, 0]]], "expected": 12}, {"args": [[[0, 2, 9, 10, 7], [1, 0, 6, 4, 3], [15, 7, 0, 8, 3], [6, 3, 12, 0, 11], [9, 7, 5, 6, 0]]], "expected": 22}, {"args": [[[0, 1, 9], [9, 0, 1], [1, 9, 0]]], "expected": 3}, {"args": [[[0, 80, 33, 95, 46, 89, 95, 84, 68, 4, 60, 32, 84], [7, 0, 21, 15, 48, 61, 32, 49, 70, 14, 74, 32, 2], [94, 28, 0, 53, 36, 24, 99, 50, 21, 98, 10, 18, 80], [80, 57, 17, 0, 17, 1, 1, 27, 28, 22, 22, 38, 41], [26, 70, 87, 81, 0, 27, 24, 89, 26, 50, 39, 3, 47], [54, 22, 19, 34, 9, 0, 43, 39, 78, 76, 1, 77, 87], [91, 44, 9, 40, 46, 40, 0, 62, 90, 41, 24, 62, 61], [91, 23, 8, 33, 3, 96, 46, 0, 52, 3, 71, 54, 47], [49, 75, 2, 58, 6, 91, 24, 80, 0, 26, 16, 97, 32], [60, 45, 66, 46, 68, 33, 60, 14, 76, 0, 96, 48, 38], [5, 56, 12, 27, 44, 66, 79, 47, 19, 44, 0, 36, 90], [70, 12, 40, 88, 41, 40, 23, 11, 81, 20, 93, 0, 89], [40, 62, 21, 93, 7, 11, 77, 69, 52, 5, 31, 95, 0]]], "expected": 122}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'tree-max-depth', 0, 'stdout', 'Высота дерева', 'Дан класс TreeNode. Напишите функцию max_depth(root): количество узлов на самом длинном пути от корня до листа (у пустого дерева — 0). Обход в ширину по уровням: проверка подаёт цепочку из 100 000 узлов.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root):
    pass
', 'Очередь (deque) с уровнями: обработайте все узлы текущего уровня, соберите детей, depth += 1.', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\nprint(max_depth(build([3, 9, 20, None, None, 15, 7])), max_depth(None), max_depth(TreeNode(1)))\nroot = cur = TreeNode(0)\nfor i in range(1, 100000):\n    cur.right = TreeNode(i)\n    cur = cur.right\nprint(max_depth(root))\n", "expected": ["3 0 1", "100000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'tree-path-sum', 1, 'stdout', 'Путь с заданной суммой', 'Дан класс TreeNode. Напишите функцию has_path_sum(root, target): True, если есть путь от корня до ЛИСТА, сумма значений на котором равна target. Пустое дерево — False.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def has_path_sum(root, target):
    pass
', 'Уменьшайте target на val; в листе (нет детей) проверьте, что остаток равен нулю.', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\nt = build([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])\nprint(has_path_sum(t, 22), has_path_sum(t, 26), has_path_sum(t, 5), has_path_sum(None, 0), has_path_sum(TreeNode(7), 7))\n", "expected": ["True True False False True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'tree-preorder-iter', 2, 'stdout', 'Прямой обход без рекурсии', 'Дан класс TreeNode (val, left, right). Напишите функцию preorder(root): список значений в прямом порядке (узел, левое, правое) без рекурсии — со своим стеком. Проверка подаёт цепочку из 100 000 узлов.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def preorder(root):
    pass
', 'Стек с корнем. Снимаем узел, записываем значение, кладём правого ребёнка, затем левого — чтобы левый вышел раньше.', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n\n\ndef levels(root):\n    out, cur = [], [root] if root else []\n    while cur:\n        out.append([n.val for n in cur])\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return out\n\n\ndef chain(n, side=\"left\"):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        nxt = TreeNode(i)\n        setattr(cur, side, nxt)\n        cur = nxt\n    return root\n\n\nprint(preorder(build([4, 2, 6, 1, 3, 5, 7])), preorder(None), preorder(TreeNode(9)), preorder(build([1, None, 2, 3])))\nr = preorder(chain(100000))\nprint(len(r), r[0], r[-1])\n", "expected": ["[4, 2, 1, 3, 6, 5, 7] [] [9] [1, 2, 3]", "100000 0 99999"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'tree-inorder-iter', 3, 'stdout', 'Симметричный обход без рекурсии', 'Дан класс TreeNode (val, left, right). Напишите функцию inorder(root): список значений в симметричном порядке (левое поддерево, узел, правое), НЕ используя рекурсию — стек вручную. Проверка подаёт вырожденное дерево глубиной 100 000, на котором рекурсия падает.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def inorder(root):
    pass
', 'stack = []; cur = root; while cur or stack: спускайтесь влево, кладя узлы в стек; затем pop, запись значения, переход вправо.', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\nprint(inorder(build([4, 2, 6, 1, 3, 5, 7])), inorder(None), inorder(TreeNode(9)))\nprint(inorder(build([1, None, 2, 3])))\nroot = cur = TreeNode(0)\nfor i in range(1, 100000):\n    cur.left = TreeNode(i)\n    cur = cur.left\nres = inorder(root)\nprint(len(res), res[0], res[-1])\n", "expected": ["[1, 2, 3, 4, 5, 6, 7] [] [9]", "[1, 3, 2]", "100000 99999 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'tree-postorder-iter', 4, 'stdout', 'Обратный обход без рекурсии', 'Дан класс TreeNode. Напишите функцию postorder(root): значения в обратном порядке (левое, правое, узел) без рекурсии. Подсказка: обратный порядок — это «узел, правое, левое», развёрнутый. Проверка подаёт цепочку из 100 000 узлов.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def postorder(root):
    pass
', 'Тот же стек, что и для прямого, но детей кладём в обратном порядке (сначала левого), а итоговый список разворачиваем.', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n\n\ndef levels(root):\n    out, cur = [], [root] if root else []\n    while cur:\n        out.append([n.val for n in cur])\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return out\n\n\ndef chain(n, side=\"left\"):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        nxt = TreeNode(i)\n        setattr(cur, side, nxt)\n        cur = nxt\n    return root\n\n\nprint(postorder(build([4, 2, 6, 1, 3, 5, 7])), postorder(None), postorder(TreeNode(9)), postorder(build([1, None, 2, 3])))\nr = postorder(chain(100000, \"right\"))\nprint(len(r), r[0], r[-1])\n", "expected": ["[1, 3, 2, 5, 7, 6, 4] [] [9] [3, 2, 1]", "100000 99999 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'tree-level-order', 5, 'stdout', 'Обход по уровням', 'Дан класс TreeNode. Напишите функцию level_order(root): список списков значений — по одному списку на каждый уровень, слева направо. Для пустого дерева — [].', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def level_order(root):
    pass
', 'На каждом шаге цикла возьмите ровно len(queue) узлов — это один уровень.', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\nprint(level_order(build([3, 9, 20, None, None, 15, 7])))\nprint(level_order(None), level_order(TreeNode(1)))\nprint(level_order(build([1, 2, 3, 4, None, None, 5])))\n", "expected": ["[[3], [9, 20], [15, 7]]", "[] [[1]]", "[[1], [2, 3], [4, 5]]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'tree-zigzag', 6, 'stdout', 'Обход зигзагом', 'Дан класс TreeNode. Напишите функцию zigzag(root): список уровней, где первый уровень идёт слева направо, второй — справа налево, третий снова слева направо и так далее. Пустое дерево — [].', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def zigzag(root):
    pass
', 'Обычный обход по уровням, а у каждого второго уровня список значений разворачивается.', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n\n\ndef levels(root):\n    out, cur = [], [root] if root else []\n    while cur:\n        out.append([n.val for n in cur])\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return out\n\n\ndef chain(n, side=\"left\"):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        nxt = TreeNode(i)\n        setattr(cur, side, nxt)\n        cur = nxt\n    return root\n\n\nprint(zigzag(build([3, 9, 20, None, None, 15, 7])), zigzag(None), zigzag(TreeNode(1)), zigzag(build([1, 2, 3, 4, None, None, 5])))\n", "expected": ["[[3], [20, 9], [15, 7]] [] [[1]] [[1], [3, 2], [4, 5]]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'tree-right-view', 7, 'stdout', 'Вид справа', 'Дан класс TreeNode. Напишите функцию right_view(root): значения узлов, которые видны, если смотреть на дерево справа, — по одному на каждый уровень (самый правый узел уровня), сверху вниз. Пустое дерево — [].', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def right_view(root):
    pass
', 'Обход по уровням слева направо: последний узел списка текущего уровня — тот, что виден справа.', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n\n\ndef levels(root):\n    out, cur = [], [root] if root else []\n    while cur:\n        out.append([n.val for n in cur])\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return out\n\n\ndef chain(n, side=\"left\"):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        nxt = TreeNode(i)\n        setattr(cur, side, nxt)\n        cur = nxt\n    return root\n\n\nprint(right_view(build([1, 2, 3, None, 5, None, 4])), right_view(None), right_view(build([1, None, 3])), right_view(build([1, 2])), right_view(build([1, 2, 3, 4])))\n", "expected": ["[1, 3, 4] [] [1, 3] [1, 2] [1, 3, 4]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'tree-symmetric', 8, 'stdout', 'Симметричное дерево', 'Дан класс TreeNode. Напишите функцию is_symmetric(root): True, если дерево — зеркальное отражение самого себя относительно корня (левое поддерево — отражение правого). Пустое дерево симметрично. Решите итеративно, очередью пар узлов: проверка подаёт симметричное дерево из цепочек по 50 000 узлов.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_symmetric(root):
    pass
', 'Кладите в очередь или стек пары (левый, правый), которые должны быть зеркальны: у них равны значения, а их дети кладутся перекрёстно — (a.left, b.right) и (a.right, b.left).', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n\n\ndef levels(root):\n    out, cur = [], [root] if root else []\n    while cur:\n        out.append([n.val for n in cur])\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return out\n\n\ndef chain(n, side=\"left\"):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        nxt = TreeNode(i)\n        setattr(cur, side, nxt)\n        cur = nxt\n    return root\n\n\nprint(is_symmetric(build([1, 2, 2, 3, 4, 4, 3])), is_symmetric(build([1, 2, 2, None, 3, None, 3])), is_symmetric(None), is_symmetric(TreeNode(1)), is_symmetric(build([1, 2, 3])))\nroot = TreeNode(0)\na = root.left = TreeNode(1)\nb = root.right = TreeNode(1)\nfor i in range(2, 50000):\n    a.left = TreeNode(i)\n    b.right = TreeNode(i)\n    a, b = a.left, b.right\nprint(is_symmetric(root))\nb.val = -1\nprint(is_symmetric(root))\n", "expected": ["True False True True False", "True", "False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'tree-invert', 9, 'stdout', 'Отразить дерево', 'Дан класс TreeNode. Напишите функцию invert(root): поменяйте местами левого и правого ребёнка у каждого узла и верните корень. Решите без рекурсии — проверка подаёт цепочку из 100 000 узлов.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def invert(root):
    pass
', 'Обойдите дерево любым способом со своим стеком и у каждого узла поменяйте left и right местами.', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n\n\ndef levels(root):\n    out, cur = [], [root] if root else []\n    while cur:\n        out.append([n.val for n in cur])\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return out\n\n\ndef chain(n, side=\"left\"):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        nxt = TreeNode(i)\n        setattr(cur, side, nxt)\n        cur = nxt\n    return root\n\n\nprint(levels(invert(build([4, 2, 7, 1, 3, 6, 9]))), levels(invert(None)), levels(invert(build([1, 2]))))\nr = invert(chain(100000))\nd = 0\nwhile r.right:\n    r = r.right\n    d += 1\nprint(d, r.val)\n", "expected": ["[[4], [7, 2], [9, 6, 3, 1]] [] [[1], [2]]", "99999 99999"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'tree-diameter', 10, 'stdout', 'Диаметр дерева', 'Дан класс TreeNode. Напишите функцию diameter(root): длина (в рёбрах) самого длинного пути между любыми двумя узлами; путь может не проходить через корень. Один обход: высоту поддеревьев считайте тем же проходом.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def diameter(root):
    pass
', 'dfs(node) возвращает высоту; по дороге обновляйте best = max(best, h_left + h_right).', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\nprint(diameter(build([1, 2, 3, 4, 5])), diameter(None), diameter(TreeNode(1)), diameter(build([1, 2])))\nprint(diameter(build([1, 2, None, 3, None, 4])))\n", "expected": ["3 0 0 1", "3"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'tree-lca', 11, 'stdout', 'Общий предок', 'Дан класс TreeNode (значения уникальны). Напишите функцию lca(root, p, q): значение самого глубокого узла, являющегося предком и для узла со значением p, и для узла со значением q (узел считается предком самого себя).', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lca(root, p, q):
    pass
', 'Рекурсивно: если узел None или равен p или q — вернуть его; если нашлось и слева, и справа — это узел-ответ; иначе то, что нашлось.', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\nt = build([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])\nprint(lca(t, 5, 1), lca(t, 5, 4), lca(t, 6, 4), lca(t, 7, 8), lca(t, 3, 3))\n", "expected": ["3 5 5 3 3"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'tree-build-pre-in', 12, 'stdout', 'Дерево по двум обходам', 'Даны прямой (preorder) и центрированный (inorder) обходы бинарного дерева с различными значениями. Напишите функцию build_tree(pre, ino): восстановите дерево и верните корень. Поиск корня в inorder должен быть O(1) — заведите словарь значение → позиция. Проверка подаёт 100 000 узлов.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def build_tree(pre, ino):
    pass
', 'Первый элемент pre — корень. Его позиция m в ino делит ино-обход: слева левое поддерево (m − lo узлов), справа правое. Прямой порядок ведите одним итератором: сначала строится левое поддерево, потом правое.', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n\n\ndef levels(root):\n    out, cur = [], [root] if root else []\n    while cur:\n        out.append([n.val for n in cur])\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return out\n\n\ndef chain(n, side=\"left\"):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        nxt = TreeNode(i)\n        setattr(cur, side, nxt)\n        cur = nxt\n    return root\n\n\nprint(levels(build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])), levels(build_tree([], [])), levels(build_tree([1], [1])), levels(build_tree([1, 2], [2, 1])))\nn = 100000\nvals = [(i * 7919) % n for i in range(n)]\nroot = None\nnodes = []\ndef ins(r, v):\n    if r is None:\n        return TreeNode(v)\n    cur = r\n    while True:\n        if v < cur.val:\n            if cur.left is None:\n                cur.left = TreeNode(v)\n                return r\n            cur = cur.left\n        else:\n            if cur.right is None:\n                cur.right = TreeNode(v)\n                return r\n            cur = cur.right\nfor v in vals:\n    root = ins(root, v)\ndef pre(r):\n    out, st = [], [r]\n    while st:\n        x = st.pop()\n        out.append(x.val)\n        if x.right: st.append(x.right)\n        if x.left: st.append(x.left)\n    return out\ndef ino_(r):\n    out, st, cur = [], [], r\n    while cur or st:\n        while cur:\n            st.append(cur)\n            cur = cur.left\n        cur = st.pop()\n        out.append(cur.val)\n        cur = cur.right\n    return out\np, i = pre(root), ino_(root)\nt = build_tree(p, i)\nprint(pre(t) == p, ino_(t) == i)\n", "expected": ["[[3], [9, 20], [15, 7]] [] [[1]] [[1], [2]]", "True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 10, 'trie-class', 13, 'stdout', 'Префиксное дерево', 'Реализуйте класс Trie: insert(word), search(word) — есть ли слово целиком, starts_with(prefix) — есть ли слово с таким началом, count_prefix(prefix) — сколько вставленных слов (с учётом повторных вставок) начинаются с prefix. Узел — словарь детей и счётчик. Все операции — O(длина слова). Проверка подаёт 100 000 слов.', 'class Trie:
    def __init__(self):
        self.root = {}

    # insert, search, starts_with, count_prefix
', 'Узел хранит словарь детей, счётчик слов, прошедших через узел, и счётчик слов, закончившихся здесь. count_prefix — счётчик «прошло» у узла, до которого спустились по префиксу.', '{"driver": "t = Trie()\nfor w in (\"apple\", \"app\", \"apple\", \"apt\", \"bat\", \"bath\"):\n    t.insert(w)\nprint(t.search(\"apple\"), t.search(\"app\"), t.search(\"ap\"), t.search(\"bath\"), t.search(\"bad\"))\nprint(t.starts_with(\"ap\"), t.starts_with(\"ba\"), t.starts_with(\"c\"), t.starts_with(\"bathe\"))\nprint(t.count_prefix(\"app\"), t.count_prefix(\"ap\"), t.count_prefix(\"b\"), t.count_prefix(\"z\"), t.count_prefix(\"bath\"))\nwords = [\"\".join(chr(97 + (i * j) % 26) for j in range(1, 9)) for i in range(1, 100001)]\nbig = Trie()\nfor w in words:\n    big.insert(w)\nprint(all(big.search(w) for w in words[:2000]), big.search(\"zzzzzzzz\"), big.count_prefix(words[7][:3]), big.count_prefix(words[999][:5]))\n", "expected": ["True True False True False", "True True False False", "3 4 2 0 1", "True False 3846 3846"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'bst-search', 0, 'stdout', 'Поиск в дереве поиска', 'Дан класс TreeNode и дерево поиска (слева меньшие, справа большие, ключи различны). Напишите функцию search(root, val): True, если ключ есть. Итеративно: проверка подаёт цепочку из 100 000 узлов.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def search(root, val):
    pass
', 'Пока root не пуст: равны — True; меньше — идём налево, больше — направо. Рекурсия не нужна.', '{"driver": "def bst_from(vals):\n    root = None\n    for v in vals:\n        n = TreeNode(v)\n        if root is None:\n            root = n\n            continue\n        cur = root\n        while True:\n            if v < cur.val:\n                if cur.left is None:\n                    cur.left = n\n                    break\n                cur = cur.left\n            else:\n                if cur.right is None:\n                    cur.right = n\n                    break\n                cur = cur.right\n    return root\n\n\ndef inorder_list(root):\n    out, st, cur = [], [], root\n    while cur or st:\n        while cur:\n            st.append(cur)\n            cur = cur.left\n        cur = st.pop()\n        out.append(cur.val)\n        cur = cur.right\n    return out\n\n\ndef height(root):\n    h, cur = 0, [root] if root else []\n    while cur:\n        h += 1\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return h\n\n\ndef chain_bst(n):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        cur.right = TreeNode(i)\n        cur = cur.right\n    return root\n\n\ndef shuffled(n, seed):\n    a = list(range(n))\n    x = seed\n    for i in range(n - 1, 0, -1):\n        x = (x * 1103515245 + 12345) % 2147483648\n        j = x % (i + 1)\n        a[i], a[j] = a[j], a[i]\n    return a\n\n\ndef rnd(n, seed, mod=10**9):\n    x = seed\n    out = []\n    for _ in range(n):\n        x = (x * 1103515245 + 12345) % 2147483648\n        out.append(x % mod)\n    return out\n\n\nt = bst_from([5, 3, 8, 1, 4, 7, 9])\nprint(search(t, 4), search(t, 9), search(t, 6), search(None, 1), search(t, 5))\nchain = chain_bst(100000)\nprint(search(chain, 99999), search(chain, 100000), search(chain, 0))\n", "expected": ["True True False False True", "True False True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'tree-valid-bst', 1, 'stdout', 'Это двоичное дерево поиска?', 'Дан класс TreeNode. Напишите функцию is_bst(root): True, если дерево — корректное двоичное дерево поиска: у каждого узла ВСЕ значения слева строго меньше, а справа строго больше. Недостаточно сравнить узел только с детьми: передавайте допустимые границы вниз.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def is_bst(root):
    pass
', 'check(node, low, high): None → True; low < val < high; левое — (low, val), правое — (val, high).', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\nprint(is_bst(build([2, 1, 3])), is_bst(build([5, 1, 4, None, None, 3, 6])), is_bst(None))\nprint(is_bst(build([5, 4, 6, None, None, 3, 7])), is_bst(build([2, 2, 2])))\n", "expected": ["True False True", "False False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'bst-insert', 2, 'stdout', 'Вставка в дерево поиска', 'Дан класс TreeNode. Напишите функцию insert(root, val): вставляет значение в двоичное дерево поиска (меньшие — влево, остальные — вправо) и возвращает корень. Для пустого дерева создайте узел. Итеративно: дерево бывает глубоким.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def insert(root, val):
    pass
', 'cur = root; в цикле идите влево при val < cur.val, иначе вправо, пока не найдёте пустое место.', '{"driver": "def inorder(n):\n    out, st = [], []\n    while n or st:\n        while n:\n            st.append(n)\n            n = n.left\n        n = st.pop()\n        out.append(n.val)\n        n = n.right\n    return out\nroot = None\nfor v in [5, 3, 8, 1, 4, 7, 9, 3]:\n    root = insert(root, v)\nprint(inorder(root), root.val, root.left.val, root.right.val)\nchain = None\nfor v in range(20000):\n    chain = insert(chain, v)\nprint(len(inorder(chain)))\n", "expected": ["[1, 3, 3, 4, 5, 7, 8, 9] 5 3 8", "20000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'bst-min-max', 3, 'stdout', 'Наименьший и наибольший', 'Напишите функцию min_max(root): кортеж (наименьший ключ, наибольший ключ) дерева поиска или None для пустого дерева. Достаточно двух спусков: влево до конца и вправо до конца.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def min_max(root):
    pass
', 'Минимум — самый левый узел, максимум — самый правый.', '{"driver": "def bst_from(vals):\n    root = None\n    for v in vals:\n        n = TreeNode(v)\n        if root is None:\n            root = n\n            continue\n        cur = root\n        while True:\n            if v < cur.val:\n                if cur.left is None:\n                    cur.left = n\n                    break\n                cur = cur.left\n            else:\n                if cur.right is None:\n                    cur.right = n\n                    break\n                cur = cur.right\n    return root\n\n\ndef inorder_list(root):\n    out, st, cur = [], [], root\n    while cur or st:\n        while cur:\n            st.append(cur)\n            cur = cur.left\n        cur = st.pop()\n        out.append(cur.val)\n        cur = cur.right\n    return out\n\n\ndef height(root):\n    h, cur = 0, [root] if root else []\n    while cur:\n        h += 1\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return h\n\n\ndef chain_bst(n):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        cur.right = TreeNode(i)\n        cur = cur.right\n    return root\n\n\ndef shuffled(n, seed):\n    a = list(range(n))\n    x = seed\n    for i in range(n - 1, 0, -1):\n        x = (x * 1103515245 + 12345) % 2147483648\n        j = x % (i + 1)\n        a[i], a[j] = a[j], a[i]\n    return a\n\n\ndef rnd(n, seed, mod=10**9):\n    x = seed\n    out = []\n    for _ in range(n):\n        x = (x * 1103515245 + 12345) % 2147483648\n        out.append(x % mod)\n    return out\n\n\nprint(min_max(bst_from([5, 3, 8, 1, 4, 7, 9])), min_max(None), min_max(TreeNode(4)), min_max(bst_from([3, 2, 1])))\nprint(min_max(bst_from(rnd(100000, 3))))\n", "expected": ["(1, 9) None (4, 4) (1, 3)", "(8749, 999992346)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'bst-successor', 4, 'stdout', 'Следующий по величине', 'Напишите функцию successor(root, val): наименьший ключ дерева поиска, строго больший val (val может быть и не в дереве), или None. Один спуск от корня: при повороте налево запоминайте узел как кандидата.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def successor(root, val):
    pass
', 'best = None; пока есть узел: если val < узел.val — он кандидат, идём налево; иначе — направо.', '{"driver": "def bst_from(vals):\n    root = None\n    for v in vals:\n        n = TreeNode(v)\n        if root is None:\n            root = n\n            continue\n        cur = root\n        while True:\n            if v < cur.val:\n                if cur.left is None:\n                    cur.left = n\n                    break\n                cur = cur.left\n            else:\n                if cur.right is None:\n                    cur.right = n\n                    break\n                cur = cur.right\n    return root\n\n\ndef inorder_list(root):\n    out, st, cur = [], [], root\n    while cur or st:\n        while cur:\n            st.append(cur)\n            cur = cur.left\n        cur = st.pop()\n        out.append(cur.val)\n        cur = cur.right\n    return out\n\n\ndef height(root):\n    h, cur = 0, [root] if root else []\n    while cur:\n        h += 1\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return h\n\n\ndef chain_bst(n):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        cur.right = TreeNode(i)\n        cur = cur.right\n    return root\n\n\ndef shuffled(n, seed):\n    a = list(range(n))\n    x = seed\n    for i in range(n - 1, 0, -1):\n        x = (x * 1103515245 + 12345) % 2147483648\n        j = x % (i + 1)\n        a[i], a[j] = a[j], a[i]\n    return a\n\n\ndef rnd(n, seed, mod=10**9):\n    x = seed\n    out = []\n    for _ in range(n):\n        x = (x * 1103515245 + 12345) % 2147483648\n        out.append(x % mod)\n    return out\n\n\nt = bst_from([8, 3, 10, 1, 6, 14, 4, 7, 13])\nprint([successor(t, v) for v in (1, 4, 7, 8, 13, 14, 0, 5, 20)], successor(None, 1))\nbig = bst_from(rnd(100000, 9, 10**6))\ns = inorder_list(big)\nprint(successor(big, s[50000]) == s[50001], successor(big, s[-1]), successor(big, -1) == s[0])\n", "expected": ["[3, 6, 8, 10, 14, None, 1, 6, None] None", "True None True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'bst-kth', 5, 'stdout', 'k-й по величине', 'Напишите функцию kth_smallest(root, k): k-й по возрастанию ключ дерева поиска (k считается с 1; гарантируется 1 ≤ k ≤ число узлов). Итеративный центрированный обход с остановкой на k-м узле.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def kth_smallest(root, k):
    pass
', 'Центрированный обход со стеком; уменьшайте k при каждом снятии узла, и когда k стал 0 — это ответ.', '{"driver": "def bst_from(vals):\n    root = None\n    for v in vals:\n        n = TreeNode(v)\n        if root is None:\n            root = n\n            continue\n        cur = root\n        while True:\n            if v < cur.val:\n                if cur.left is None:\n                    cur.left = n\n                    break\n                cur = cur.left\n            else:\n                if cur.right is None:\n                    cur.right = n\n                    break\n                cur = cur.right\n    return root\n\n\ndef inorder_list(root):\n    out, st, cur = [], [], root\n    while cur or st:\n        while cur:\n            st.append(cur)\n            cur = cur.left\n        cur = st.pop()\n        out.append(cur.val)\n        cur = cur.right\n    return out\n\n\ndef height(root):\n    h, cur = 0, [root] if root else []\n    while cur:\n        h += 1\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return h\n\n\ndef chain_bst(n):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        cur.right = TreeNode(i)\n        cur = cur.right\n    return root\n\n\ndef shuffled(n, seed):\n    a = list(range(n))\n    x = seed\n    for i in range(n - 1, 0, -1):\n        x = (x * 1103515245 + 12345) % 2147483648\n        j = x % (i + 1)\n        a[i], a[j] = a[j], a[i]\n    return a\n\n\ndef rnd(n, seed, mod=10**9):\n    x = seed\n    out = []\n    for _ in range(n):\n        x = (x * 1103515245 + 12345) % 2147483648\n        out.append(x % mod)\n    return out\n\n\nt = bst_from([5, 3, 6, 2, 4, 1])\nprint([kth_smallest(t, k) for k in range(1, 7)], kth_smallest(TreeNode(7), 1))\nchain = chain_bst(100000)\nprint(kth_smallest(chain, 100000), kth_smallest(chain, 1))\n", "expected": ["[1, 2, 3, 4, 5, 6] 7", "99999 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'bst-floor-ceiling', 6, 'stdout', 'Пол и потолок', 'Напишите функцию floor_ceiling(root, x): кортеж (floor, ceil), где floor — наибольший ключ ≤ x, ceil — наименьший ключ ≥ x; если такого нет — None на его месте. Один спуск от корня.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def floor_ceiling(root, x):
    pass
', 'Если ключ узла < x — он кандидат на floor, идём направо; если > x — кандидат на ceil, идём налево; равный — оба равны x.', '{"driver": "def bst_from(vals):\n    root = None\n    for v in vals:\n        n = TreeNode(v)\n        if root is None:\n            root = n\n            continue\n        cur = root\n        while True:\n            if v < cur.val:\n                if cur.left is None:\n                    cur.left = n\n                    break\n                cur = cur.left\n            else:\n                if cur.right is None:\n                    cur.right = n\n                    break\n                cur = cur.right\n    return root\n\n\ndef inorder_list(root):\n    out, st, cur = [], [], root\n    while cur or st:\n        while cur:\n            st.append(cur)\n            cur = cur.left\n        cur = st.pop()\n        out.append(cur.val)\n        cur = cur.right\n    return out\n\n\ndef height(root):\n    h, cur = 0, [root] if root else []\n    while cur:\n        h += 1\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return h\n\n\ndef chain_bst(n):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        cur.right = TreeNode(i)\n        cur = cur.right\n    return root\n\n\ndef shuffled(n, seed):\n    a = list(range(n))\n    x = seed\n    for i in range(n - 1, 0, -1):\n        x = (x * 1103515245 + 12345) % 2147483648\n        j = x % (i + 1)\n        a[i], a[j] = a[j], a[i]\n    return a\n\n\ndef rnd(n, seed, mod=10**9):\n    x = seed\n    out = []\n    for _ in range(n):\n        x = (x * 1103515245 + 12345) % 2147483648\n        out.append(x % mod)\n    return out\n\n\nt = bst_from([8, 3, 10, 1, 6, 14, 4, 7, 13])\nprint([floor_ceiling(t, x) for x in (0, 1, 5, 8, 9, 14, 15)], floor_ceiling(None, 3))\nbig = bst_from(rnd(100000, 4, 10**7))\ns = inorder_list(big)\nprint(floor_ceiling(big, s[777] + 1)[0] >= s[777], floor_ceiling(big, -5), floor_ceiling(big, 10**8))\n", "expected": ["[(None, 1), (1, 1), (4, 6), (8, 8), (8, 10), (14, 14), (14, None)] (None, None)", "True (None, 22) (9999977, None)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'bst-range-sum', 7, 'stdout', 'Сумма в диапазоне', 'Напишите функцию range_sum(root, lo, hi): сумма ключей дерева поиска, попадающих в отрезок [lo, hi]. Отсекайте поддеревья, которые заведомо вне диапазона: проверка считает обращения к ключам и требует не больше нескольких сотен на дереве из 100 000 узлов.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def range_sum(root, lo, hi):
    pass
', 'Левое поддерево имеет смысл только если ключ узла > lo, правое — если ключ < hi. Остальное пропускайте целиком.', '{"driver": "def bst_from(vals):\n    root = None\n    for v in vals:\n        n = TreeNode(v)\n        if root is None:\n            root = n\n            continue\n        cur = root\n        while True:\n            if v < cur.val:\n                if cur.left is None:\n                    cur.left = n\n                    break\n                cur = cur.left\n            else:\n                if cur.right is None:\n                    cur.right = n\n                    break\n                cur = cur.right\n    return root\n\n\ndef inorder_list(root):\n    out, st, cur = [], [], root\n    while cur or st:\n        while cur:\n            st.append(cur)\n            cur = cur.left\n        cur = st.pop()\n        out.append(cur.val)\n        cur = cur.right\n    return out\n\n\ndef height(root):\n    h, cur = 0, [root] if root else []\n    while cur:\n        h += 1\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return h\n\n\ndef chain_bst(n):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        cur.right = TreeNode(i)\n        cur = cur.right\n    return root\n\n\ndef shuffled(n, seed):\n    a = list(range(n))\n    x = seed\n    for i in range(n - 1, 0, -1):\n        x = (x * 1103515245 + 12345) % 2147483648\n        j = x % (i + 1)\n        a[i], a[j] = a[j], a[i]\n    return a\n\n\ndef rnd(n, seed, mod=10**9):\n    x = seed\n    out = []\n    for _ in range(n):\n        x = (x * 1103515245 + 12345) % 2147483648\n        out.append(x % mod)\n    return out\n\n\nclass Spy(TreeNode):\n    reads = 0\n\n    @property\n    def val(self):\n        Spy.reads += 1\n        return self._v\n\n    @val.setter\n    def val(self, v):\n        self._v = v\n\n\ndef spy_balanced(a):\n    def go(lo, hi):\n        if lo > hi:\n            return None\n        m = (lo + hi) // 2\n        n = Spy(a[m])\n        n.left = go(lo, m - 1)\n        n.right = go(m + 1, hi)\n        return n\n    return go(0, len(a) - 1)\n\n\nt = bst_from([8, 3, 10, 1, 6, 14, 4, 7, 13])\nprint(range_sum(t, 4, 10), range_sum(t, 0, 100), range_sum(t, 15, 20), range_sum(None, 1, 2), range_sum(t, 6, 6))\na = list(range(0, 200000, 2))\nbig = spy_balanced(a)\nSpy.reads = 0\ns = range_sum(big, 50000, 50040)\nprint(s, Spy.reads < 400)\n", "expected": ["35 66 0 0 6", "1050420 True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'bst-lca', 8, 'stdout', 'Общий предок в дереве поиска', 'Напишите функцию lca_bst(root, p, q): ключ наименьшего общего предка узлов с ключами p и q в дереве поиска (оба ключа есть в дереве; узел — предок самого себя). Не нужен полный обход: спускайтесь, пока p и q с одной стороны от узла.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lca_bst(root, p, q):
    pass
', 'Если оба ключа меньше узла — идём налево, оба больше — направо. Иначе узел разделяет их (или равен одному) — это ответ.', '{"driver": "def bst_from(vals):\n    root = None\n    for v in vals:\n        n = TreeNode(v)\n        if root is None:\n            root = n\n            continue\n        cur = root\n        while True:\n            if v < cur.val:\n                if cur.left is None:\n                    cur.left = n\n                    break\n                cur = cur.left\n            else:\n                if cur.right is None:\n                    cur.right = n\n                    break\n                cur = cur.right\n    return root\n\n\ndef inorder_list(root):\n    out, st, cur = [], [], root\n    while cur or st:\n        while cur:\n            st.append(cur)\n            cur = cur.left\n        cur = st.pop()\n        out.append(cur.val)\n        cur = cur.right\n    return out\n\n\ndef height(root):\n    h, cur = 0, [root] if root else []\n    while cur:\n        h += 1\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return h\n\n\ndef chain_bst(n):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        cur.right = TreeNode(i)\n        cur = cur.right\n    return root\n\n\ndef shuffled(n, seed):\n    a = list(range(n))\n    x = seed\n    for i in range(n - 1, 0, -1):\n        x = (x * 1103515245 + 12345) % 2147483648\n        j = x % (i + 1)\n        a[i], a[j] = a[j], a[i]\n    return a\n\n\ndef rnd(n, seed, mod=10**9):\n    x = seed\n    out = []\n    for _ in range(n):\n        x = (x * 1103515245 + 12345) % 2147483648\n        out.append(x % mod)\n    return out\n\n\nt = bst_from([6, 2, 8, 0, 4, 7, 9, 3, 5])\nprint(lca_bst(t, 2, 8), lca_bst(t, 2, 4), lca_bst(t, 3, 5), lca_bst(t, 0, 5), lca_bst(t, 7, 9), lca_bst(t, 6, 6))\nbig = chain_bst(100000)\nprint(lca_bst(big, 5, 99999), lca_bst(big, 70000, 70001))\n", "expected": ["6 2 4 2 8 6", "5 70000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'sorted-to-bst', 9, 'stdout', 'Сбалансированное дерево из массива', 'Напишите функцию sorted_to_bst(a): из отсортированного списка различных чисел постройте дерево поиска минимальной высоты и верните корень. Корнем берите средний элемент, левое и правое поддерево строятся из половин. Проверка подаёт 200 000 чисел и смотрит высоту.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def sorted_to_bst(a):
    pass
', 'Рекурсивная функция go(lo, hi): если lo > hi — None; иначе m = (lo + hi) // 2, корень a[m], левое поддерево go(lo, m − 1), правое go(m + 1, hi).', '{"driver": "def bst_from(vals):\n    root = None\n    for v in vals:\n        n = TreeNode(v)\n        if root is None:\n            root = n\n            continue\n        cur = root\n        while True:\n            if v < cur.val:\n                if cur.left is None:\n                    cur.left = n\n                    break\n                cur = cur.left\n            else:\n                if cur.right is None:\n                    cur.right = n\n                    break\n                cur = cur.right\n    return root\n\n\ndef inorder_list(root):\n    out, st, cur = [], [], root\n    while cur or st:\n        while cur:\n            st.append(cur)\n            cur = cur.left\n        cur = st.pop()\n        out.append(cur.val)\n        cur = cur.right\n    return out\n\n\ndef height(root):\n    h, cur = 0, [root] if root else []\n    while cur:\n        h += 1\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return h\n\n\ndef chain_bst(n):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        cur.right = TreeNode(i)\n        cur = cur.right\n    return root\n\n\ndef shuffled(n, seed):\n    a = list(range(n))\n    x = seed\n    for i in range(n - 1, 0, -1):\n        x = (x * 1103515245 + 12345) % 2147483648\n        j = x % (i + 1)\n        a[i], a[j] = a[j], a[i]\n    return a\n\n\ndef rnd(n, seed, mod=10**9):\n    x = seed\n    out = []\n    for _ in range(n):\n        x = (x * 1103515245 + 12345) % 2147483648\n        out.append(x % mod)\n    return out\n\n\nprint(inorder_list(sorted_to_bst([1, 2, 3, 4, 5, 6, 7])), height(sorted_to_bst([1, 2, 3, 4, 5, 6, 7])), sorted_to_bst([]), height(sorted_to_bst([1])))\na = list(range(200000))\nt = sorted_to_bst(a)\nprint(inorder_list(t) == a, height(t))\n", "expected": ["[1, 2, 3, 4, 5, 6, 7] 3 None 1", "True 18"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'bst-trim', 10, 'stdout', 'Обрезка дерева поиска', 'Напишите функцию trim(root, lo, hi): оставьте в дереве поиска только ключи из отрезка [lo, hi], сохранив относительную структуру оставшихся узлов, и верните новый корень. Если узел меньше lo — берём только его правое поддерево, больше hi — левое.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def trim(root, lo, hi):
    pass
', 'Рекурсия: узел вне диапазона заменяется результатом для нужного поддерева; узел внутри — оставляем и обрезаем оба ребёнка.', '{"driver": "def bst_from(vals):\n    root = None\n    for v in vals:\n        n = TreeNode(v)\n        if root is None:\n            root = n\n            continue\n        cur = root\n        while True:\n            if v < cur.val:\n                if cur.left is None:\n                    cur.left = n\n                    break\n                cur = cur.left\n            else:\n                if cur.right is None:\n                    cur.right = n\n                    break\n                cur = cur.right\n    return root\n\n\ndef inorder_list(root):\n    out, st, cur = [], [], root\n    while cur or st:\n        while cur:\n            st.append(cur)\n            cur = cur.left\n        cur = st.pop()\n        out.append(cur.val)\n        cur = cur.right\n    return out\n\n\ndef height(root):\n    h, cur = 0, [root] if root else []\n    while cur:\n        h += 1\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return h\n\n\ndef chain_bst(n):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        cur.right = TreeNode(i)\n        cur = cur.right\n    return root\n\n\ndef shuffled(n, seed):\n    a = list(range(n))\n    x = seed\n    for i in range(n - 1, 0, -1):\n        x = (x * 1103515245 + 12345) % 2147483648\n        j = x % (i + 1)\n        a[i], a[j] = a[j], a[i]\n    return a\n\n\ndef rnd(n, seed, mod=10**9):\n    x = seed\n    out = []\n    for _ in range(n):\n        x = (x * 1103515245 + 12345) % 2147483648\n        out.append(x % mod)\n    return out\n\n\nt = bst_from([3, 0, 4, 2, 1])\nprint(inorder_list(trim(t, 1, 3)))\nt = bst_from([3, 0, 4, 2, 1])\nr = trim(t, 1, 3)\nprint(r.val, r.left.val, r.left.right.val if r.left.right else None)\nprint(trim(bst_from([5, 3, 8]), 9, 10), inorder_list(trim(bst_from([1, 2, 3]), 0, 100)), trim(None, 1, 2))\nbig = bst_from(rnd(100000, 12, 10**6))\nr = trim(big, 200000, 700000)\nv = inorder_list(r)\nprint(len(v) > 0, v[0] >= 200000, v[-1] <= 700000, v == sorted(v))\n", "expected": ["[1, 2, 3]", "3 2 None", "None [1, 2, 3] None", "True True True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'bst-iterator', 11, 'stdout', 'Итератор по дереву', 'Реализуйте класс BSTIterator(root): методы next() — следующий по возрастанию ключ и has_next() — есть ли ещё. Память — O(высота): держите стек пути, как в итеративном центрированном обходе. next() вызывается только при has_next().', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class BSTIterator:
    def __init__(self, root):
        pass

    def next(self):
        pass

    def has_next(self):
        pass
', 'В конструкторе спуститесь от корня налево, складывая узлы в стек. next(): снять узел, спуститься влево от его правого ребёнка, вернуть значение.', '{"driver": "def bst_from(vals):\n    root = None\n    for v in vals:\n        n = TreeNode(v)\n        if root is None:\n            root = n\n            continue\n        cur = root\n        while True:\n            if v < cur.val:\n                if cur.left is None:\n                    cur.left = n\n                    break\n                cur = cur.left\n            else:\n                if cur.right is None:\n                    cur.right = n\n                    break\n                cur = cur.right\n    return root\n\n\ndef inorder_list(root):\n    out, st, cur = [], [], root\n    while cur or st:\n        while cur:\n            st.append(cur)\n            cur = cur.left\n        cur = st.pop()\n        out.append(cur.val)\n        cur = cur.right\n    return out\n\n\ndef height(root):\n    h, cur = 0, [root] if root else []\n    while cur:\n        h += 1\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return h\n\n\ndef chain_bst(n):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        cur.right = TreeNode(i)\n        cur = cur.right\n    return root\n\n\ndef shuffled(n, seed):\n    a = list(range(n))\n    x = seed\n    for i in range(n - 1, 0, -1):\n        x = (x * 1103515245 + 12345) % 2147483648\n        j = x % (i + 1)\n        a[i], a[j] = a[j], a[i]\n    return a\n\n\ndef rnd(n, seed, mod=10**9):\n    x = seed\n    out = []\n    for _ in range(n):\n        x = (x * 1103515245 + 12345) % 2147483648\n        out.append(x % mod)\n    return out\n\n\nt = bst_from([7, 3, 15, 9, 20])\nit = BSTIterator(t)\nout = []\nwhile it.has_next():\n    out.append(it.next())\nprint(out, BSTIterator(None).has_next())\nbig = bst_from(rnd(100000, 21, 10**7))\nit = BSTIterator(big)\nvals = []\nwhile it.has_next():\n    vals.append(it.next())\nprint(vals == inorder_list(big), len(vals))\n", "expected": ["[3, 7, 9, 15, 20] False", "True 100000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'bst-two-sum', 12, 'stdout', 'Пара с суммой в дереве', 'Напишите функцию find_target(root, k): есть ли в дереве поиска два РАЗНЫХ узла, сумма ключей которых равна k. Решите двумя итераторами навстречу (по возрастанию и по убыванию), как в задаче с двумя указателями; память — O(высота). Проверка подаёт 100 000 узлов.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def find_target(root, k):
    pass
', 'Два стека-итератора: левый идёт по возрастанию, правый — по убыванию. Сумма мала — двигаем левый, велика — правый; остановка, когда они сошлись на одном узле.', '{"driver": "def bst_from(vals):\n    root = None\n    for v in vals:\n        n = TreeNode(v)\n        if root is None:\n            root = n\n            continue\n        cur = root\n        while True:\n            if v < cur.val:\n                if cur.left is None:\n                    cur.left = n\n                    break\n                cur = cur.left\n            else:\n                if cur.right is None:\n                    cur.right = n\n                    break\n                cur = cur.right\n    return root\n\n\ndef inorder_list(root):\n    out, st, cur = [], [], root\n    while cur or st:\n        while cur:\n            st.append(cur)\n            cur = cur.left\n        cur = st.pop()\n        out.append(cur.val)\n        cur = cur.right\n    return out\n\n\ndef height(root):\n    h, cur = 0, [root] if root else []\n    while cur:\n        h += 1\n        cur = [c for n in cur for c in (n.left, n.right) if c]\n    return h\n\n\ndef chain_bst(n):\n    root = cur = TreeNode(0)\n    for i in range(1, n):\n        cur.right = TreeNode(i)\n        cur = cur.right\n    return root\n\n\ndef shuffled(n, seed):\n    a = list(range(n))\n    x = seed\n    for i in range(n - 1, 0, -1):\n        x = (x * 1103515245 + 12345) % 2147483648\n        j = x % (i + 1)\n        a[i], a[j] = a[j], a[i]\n    return a\n\n\ndef rnd(n, seed, mod=10**9):\n    x = seed\n    out = []\n    for _ in range(n):\n        x = (x * 1103515245 + 12345) % 2147483648\n        out.append(x % mod)\n    return out\n\n\nt = bst_from([5, 3, 6, 2, 4, 7])\nprint(find_target(t, 9), find_target(t, 28), find_target(TreeNode(2), 4), find_target(None, 0), find_target(t, 8))\nvals = list(range(0, 200000, 2))\nbig = bst_from([vals[j] for j in shuffled(len(vals), 5)])\nprint(find_target(big, 199998), find_target(big, 199999), find_target(big, 4), find_target(big, 2))\n", "expected": ["True False False False True", "True False True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 11, 'bst-class', 13, 'stdout', 'Своё дерево поиска', 'Реализуйте класс BST: insert(x) (повтор игнорируется), contains(x), delete(x) → True/False (все три случая: лист, один ребёнок, два ребёнка через преемника), inorder() — список ключей, height() — высота (пустое дерево — 0), len(t). Все операции кроме inorder — итеративно. Проверка кладёт и удаляет по 100 000 ключей.', 'class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self._n = 0

    def __len__(self):
        return self._n

    # insert, contains, delete, inorder, height
', 'В delete спуститесь к узлу, запомнив родителя. Два ребёнка: найдите преемника (минимум правого поддерева) с его родителем, скопируйте ключ и удаляйте преемника как узел максимум с одним ребёнком.', '{"driver": "t = BST()\nfor x in (8, 3, 10, 1, 6, 14, 4, 7, 13, 6):\n    t.insert(x)\nprint(t.inorder(), len(t), t.height(), t.contains(7), t.contains(5))\nprint(t.delete(7), t.delete(3), t.delete(8), t.delete(99), t.inorder(), len(t))\nprint(t.contains(3), t.contains(4), t.height())\nwhile len(t):\n    t.delete(t.root.key)\nprint(t.inorder(), t.height(), t.delete(1))\nx = 17\nkeys = []\nfor _ in range(100000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    keys.append(x % 10**6)\nbig = BST()\nfor k in keys:\n    big.insert(k)\ns = sorted(set(keys))\nprint(len(big) == len(s), big.inorder() == s, big.height() < 60)\nfor k in keys[::2]:\n    big.delete(k)\nleft = sorted(set(keys) - set(keys[::2]))\nprint(len(big) == len(left), big.inorder() == left)\n", "expected": ["[1, 3, 4, 6, 7, 8, 10, 13, 14] 9 4 True False", "True True True False [1, 4, 6, 10, 13, 14] 6", "False True 3", "[] 0 False", "True True True", "True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'heap-indices', 0, 'stdout', 'Индексы и проверка кучи', 'Куча лежит в списке: корень — a[0]. Напишите функции parent(i), left(i), right(i) (индексы родителя и детей) и first_violation(a): для минимальной кучи верните кортеж (индекс родителя, индекс ребёнка) первой пары, где родитель БОЛЬШЕ ребёнка (перебор детей по возрастанию индекса), или None, если свойство кучи выполнено.', 'def parent(i):
    pass


def left(i):
    pass


def right(i):
    pass


def first_violation(a):
    pass
', 'parent(i) = (i − 1) // 2; left(i) = 2i + 1; right(i) = 2i + 2. Свойство кучи достаточно проверить для каждого i ≥ 1: a[parent(i)] ≤ a[i].', '{"driver": "print([parent(i) for i in range(1, 8)], [left(i) for i in range(4)], [right(i) for i in range(4)])\nprint(first_violation([1, 3, 2, 7, 4, 5, 6]), first_violation([1, 3, 2, 7, 0]), first_violation([2, 1]), first_violation([]), first_violation([5]))\nprint(first_violation(list(range(200000))), first_violation([0] + list(range(1, 100000)) + [-1]))\n", "expected": ["[0, 0, 1, 1, 2, 2, 3] [1, 3, 5, 7] [2, 4, 6, 8]", "None (1, 4) (0, 1) None None", "None (49999, 100000)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'heap-sift-up', 1, 'stdout', 'Просеивание вверх', 'Напишите функцию sift_up(a, i): элемент a[i] поднимается вверх по минимальной куче, пока он МЕНЬШЕ родителя (обмен с родителем). Список меняется на месте; верните число сделанных обменов.', 'def sift_up(a, i):
    pass
', 'Пока i > 0: p = (i − 1) // 2; если a[i] < a[p] — меняем местами и i = p; иначе стоп. Равные не обмениваются (строго меньше).', '{"driver": "a = [1, 3, 2, 7, 4, 5, 6, 0]\nprint(sift_up(a, 7), a)\nb = [1, 3, 2, 7, 4, 5, 6, 8]\nprint(sift_up(b, 7), b)\nc = [5, 6, 7, 1]\nprint(sift_up(c, 3), c)\nd = [4]\nprint(sift_up(d, 0), d)\ne = [2, 2, 2, 2]\nprint(sift_up(e, 3), e)\nn = 131071\nbig = list(range(1, n)) + [0]\nprint(sift_up(big, n - 1), big[0], big[1], big[2])\n", "expected": ["3 [0, 1, 2, 3, 4, 5, 6, 7]", "0 [1, 3, 2, 7, 4, 5, 6, 8]", "2 [1, 5, 7, 6]", "0 [4]", "0 [2, 2, 2, 2]", "16 0 2 1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'heap-sift-down', 2, 'stdout', 'Просеивание вниз', 'Напишите функцию sift_down(a, i, n): элемент a[i] опускается по минимальной куче из первых n элементов списка (a[n:] не трогать). Выбор: c = левый ребёнок; если правый существует (< n) и СТРОГО меньше левого — c = правый; если a[c] < a[i] — обмен и продолжаем с c, иначе стоп. Список меняется на месте; верните число обменов.', 'def sift_down(a, i, n):
    pass
', 'Выбор ребёнка: c = 2i + 1; если c + 1 < n и a[c + 1] < a[c] — c += 1. Если a[c] < a[i] — меняем и идём вниз, иначе выходим. При n граница кучи — a[n:] не смотрим.', '{"driver": "a = [7, 1, 2, 3, 4, 5, 6]\nprint(sift_down(a, 0, 7), a)\nb = [9, 2, 2, 5, 6, 3, 4]\nprint(sift_down(b, 0, 7), b)\nc = [0, 5, 6]\nprint(sift_down(c, 0, 3), c)\nd = [8, 1, 2, 0]\nprint(sift_down(d, 0, 3), d)\ne = [3]\nprint(sift_down(e, 0, 1), e)\nn = 131071\nbig = [10**9] + list(range(1, n))\nprint(sift_down(big, 0, n), big[0], big[1], big[2], big[n - 1])\n", "expected": ["2 [1, 3, 2, 7, 4, 5, 6]", "2 [2, 5, 2, 9, 6, 3, 4]", "0 [0, 5, 6]", "1 [1, 8, 2, 0]", "0 [3]", "16 1 3 2 131070"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'heap-push', 3, 'stdout', 'Вставка в кучу', 'Напишите функцию heap_push(a, x): добавьте x в минимальную кучу a (список меняется на месте): в конец и просеивание вверх. Проверка добавляет 200 000 чисел.', 'def heap_push(a, x):
    pass
', 'a.append(x), затем i = len(a) − 1 и цикл просеивания вверх (как в sift_up).', '{"driver": "def ok(a):\n    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))\n\n\ndef rnd(n, seed, mod=10**9):\n    x = seed\n    out = []\n    for _ in range(n):\n        x = (x * 1103515245 + 12345) % 2147483648\n        out.append(x % mod)\n    return out\n\n\nh = []\nfor x in (5, 3, 8, 1, 9, 2):\n    heap_push(h, x)\n    print(h)\nbig = []\nfor v in rnd(200000, 3):\n    heap_push(big, v)\nprint(ok(big), big[0] == min(big), len(big))\ndesc = []\nfor v in range(100000, 0, -1):\n    heap_push(desc, v)\nprint(ok(desc), desc[0])\n", "expected": ["[5]", "[3, 5]", "[3, 5, 8]", "[1, 3, 8, 5]", "[1, 3, 8, 5, 9]", "[1, 3, 2, 5, 9, 8]", "True True 200000", "True 1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'heap-pop', 4, 'stdout', 'Извлечение минимума', 'Напишите функцию heap_pop(a): удалите и верните наименьший элемент минимальной кучи a (на месте): последний элемент перемещается в корень и просеивается вниз (выбор ребёнка — как в sift_down: левый, правый если строго меньше). Для пустой кучи — IndexError. Проверка извлекает 100 000 чисел.', 'def heap_pop(a):
    pass
', 'top = a[0]; last = a.pop(); если куча не пуста — a[0] = last и просеивание вниз (n = len(a)). Не забудьте вернуть top.', '{"driver": "def ok(a):\n    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))\n\n\ndef rnd(n, seed, mod=10**9):\n    x = seed\n    out = []\n    for _ in range(n):\n        x = (x * 1103515245 + 12345) % 2147483648\n        out.append(x % mod)\n    return out\n\n\nh = [1, 3, 2, 7, 4, 5, 6]\nprint(heap_pop(h), h)\nprint(heap_pop(h), h)\nprint(heap_pop(h), h)\none = [4]\nprint(heap_pop(one), one)\ntry:\n    heap_pop([])\nexcept IndexError:\n    print(\"IndexError\")\nvals = rnd(100000, 8)\nbig = sorted(vals)\nbig = big[::-1]\nimport heapq\nheapq.heapify(big)\nout = [heap_pop(big) for _ in range(len(vals))]\nprint(out == sorted(vals), len(big))\n", "expected": ["1 [2, 3, 5, 7, 4, 6]", "2 [3, 4, 5, 7, 6]", "3 [4, 6, 5, 7]", "4 []", "IndexError", "True 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'heapify-linear', 5, 'stdout', 'Построение кучи за O(n)', 'Напишите функцию heapify(a): превратите список в минимальную кучу на месте, просеивая вниз от последнего родителя к корню. Проверка считает сравнения элементов на 100 000 числах по убыванию (худший случай): не более 3n — построение вставками не пройдёт.', 'def heapify(a):
    pass
', 'for start in range(n // 2 − 1, −1, −1): просеивание вниз элемента start (sift_down). Листья (индексы от n // 2) уже кучи.', '{"driver": "class C:\n    cnt = 0\n\n    def __init__(self, v):\n        self.v = v\n\n    def __lt__(self, o):\n        C.cnt += 1\n        return self.v < o.v\n\n    def __gt__(self, o):\n        C.cnt += 1\n        return self.v > o.v\n\n    def __le__(self, o):\n        C.cnt += 1\n        return self.v <= o.v\n\n    def __ge__(self, o):\n        C.cnt += 1\n        return self.v >= o.v\n\n    def __eq__(self, o):\n        return self.v == o.v\n\n    def __repr__(self):\n        return str(self.v)\n\n\ndef ok(a):\n    return all(a[(i - 1) // 2].v <= a[i].v for i in range(1, len(a)))\n\n\na = [9, 4, 7, 1, 3, 8, 2]\nheapify(a)\nprint(a)\nprint(heapify([]), heapify([5]))\nn = 100000\narr = [C(v) for v in range(n, 0, -1)]\nheapify(arr)\nprint(ok(arr), arr[0].v, C.cnt <= 3 * n)\narr = [C(v) for v in range(0, 100000)]\nrnd = arr[:]\nheapify(rnd)\nprint(ok(rnd))\n", "expected": ["[1, 3, 2, 4, 9, 8, 7]", "None None", "True 1 True", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'heap-sort', 6, 'stdout', 'Пирамидальная сортировка', 'Напишите функцию heap_sort(a): отсортируйте список по возрастанию на месте пирамидальной сортировкой: постройте максимальную кучу, затем N раз меняйте корень с последним элементом неотсортированной части и просеивайте новый корень вниз. Встроенные sort/sorted/heapq запрещены по смыслу. Проверка сортирует 100 000 чисел.', 'def heap_sort(a):
    pass
', 'Максимальная куча: просеивание вниз с условием «ребёнок БОЛЬШЕ». Обмен корня с a[end], затем просеивание корня в куче размером end.', '{"driver": "for src in ([5, 2, 9, 1, 5, 6], [], [1], [2, 1], [3, 3, 3], list(range(10, 0, -1))):\n    a = list(src)\n    heap_sort(a)\n    print(a)\nsrc = [(i * 7919) % 100003 for i in range(100000)]\na = list(src)\nheap_sort(a)\nprint(a == sorted(src), a[:3], a[-3:])\n", "expected": ["[1, 2, 5, 5, 6, 9]", "[]", "[1]", "[1, 2]", "[3, 3, 3]", "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]", "True [0, 1, 2] [100000, 100001, 100002]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'heap-pushpop-replace', 7, 'stdout', 'pushpop и replace', 'Напишите две функции для минимальной кучи a (список, на месте): heap_pushpop(a, x) — «положить x, затем достать минимум»: если куча пуста или x не больше a[0], вернуть x, не трогая кучу; иначе вернуть старый корень, поставив на его место x и просеяв вниз. heap_replace(a, x) — «достать минимум, затем положить x»: всегда возвращает старый корень, ставит x на его место и просеивает вниз; для пустой кучи — IndexError.', 'def heap_pushpop(a, x):
    pass


def heap_replace(a, x):
    pass
', 'pushpop: если x не больше корня — он и есть минимум, куча не меняется. Иначе корень уходит, x встаёт на его место и опускается. replace отличается тем, что корень отдаётся всегда.', '{"driver": "import heapq\n\n\ndef ok(a):\n    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))\n\n\nh = [1, 3, 2, 7, 4, 5, 6]\nprint(heap_pushpop(h, 0), h)\nprint(heap_pushpop(h, 9), h, ok(h))\nprint(heap_replace(h, 0), h, ok(h))\nprint(heap_pushpop([], 5), heap_pushpop([2], 2))\ntry:\n    heap_replace([], 1)\nexcept IndexError:\n    print(\"IndexError\")\nx = 3\nmine, ref = [], []\ngood = True\nfor i in range(20000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    v = x % 1000\n    if i % 3 == 0 or not mine:\n        mine.append(v)\n        ref.append(v)\n        heapq.heapify(mine)\n        heapq.heapify(ref)\n    elif i % 3 == 1:\n        good = good and heap_pushpop(mine, v) == heapq.heappushpop(ref, v)\n    else:\n        good = good and heap_replace(mine, v) == heapq.heapreplace(ref, v)\n    good = good and ok(mine) and sorted(mine) == sorted(ref)\nprint(good)\n", "expected": ["0 [1, 3, 2, 7, 4, 5, 6]", "1 [2, 3, 5, 7, 4, 9, 6] True", "2 [0, 3, 5, 7, 4, 9, 6] True", "5 2", "IndexError", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'max-heap-class', 8, 'stdout', 'Максимальная куча', 'Реализуйте класс MaxHeap(key=None) — максимальная куча на списке: push(x), pop() — элемент с наибольшим key(x) (IndexError на пустой), peek(), len(h). Без key элементы сравниваются сами. Просеивание пишите сами, модуль heapq не используйте. Проверка кладёт 100 000 элементов.', 'class MaxHeap:
    def __init__(self, key=None):
        self.key = key or (lambda x: x)
        self.a = []

    def __len__(self):
        return len(self.a)

    # push, pop, peek
', 'То же, что heap_push/heap_pop, но сравнение инвертировано и идёт по key(x): куча хранит сами элементы, а упорядочивает по ключу.', '{"driver": "h = MaxHeap()\nfor x in (3, 9, 1, 7, 5):\n    h.push(x)\nprint(len(h), h.peek(), [h.pop() for _ in range(5)], len(h))\nw = MaxHeap(key=len)\nfor s in (\"aa\", \"b\", \"cccc\", \"ddd\"):\n    w.push(s)\nprint([w.pop() for _ in range(4)])\ntry:\n    MaxHeap().pop()\nexcept IndexError:\n    print(\"IndexError\")\nvals = [(i * 7919) % 100003 for i in range(100000)]\nbig = MaxHeap()\nfor v in vals:\n    big.push(v)\nout = [big.pop() for _ in range(len(vals))]\nprint(out == sorted(vals, reverse=True))\n", "expected": ["5 9 [9, 7, 5, 3, 1] 0", "[''cccc'', ''ddd'', ''aa'', ''b'']", "IndexError", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'stable-priority-queue', 9, 'stdout', 'Приоритетная очередь с порядком', 'Реализуйте класс PriorityQueue: push(priority, item), pop() — элемент с наименьшим приоритетом; при равных приоритетах — в порядке добавления (FIFO). Элементы могут быть несравнимыми (словари, объекты): вторым полем хранимой записи ставьте возрастающий счётчик. Просеивание — своё, без heapq. pop на пустой — IndexError. Проверка кладёт 100 000 записей.', 'class PriorityQueue:
    def __init__(self):
        self.a = []
        self.n = 0

    def __len__(self):
        return len(self.a)

    # push(priority, item), pop()
', 'Храните в куче кортежи (приоритет, счётчик, элемент). Сравнивайте только первые два поля (приоритет и счётчик): счётчик уникален, поэтому до самих элементов сравнение не дойдёт.', '{"driver": "q = PriorityQueue()\nq.push(2, {\"name\": \"b\"})\nq.push(1, {\"name\": \"a\"})\nq.push(2, {\"name\": \"c\"})\nq.push(1, {\"name\": \"d\"})\nq.push(3, {\"name\": \"e\"})\nprint([q.pop()[\"name\"] for _ in range(5)], len(q))\ntry:\n    q.pop()\nexcept IndexError:\n    print(\"IndexError\")\nbig = PriorityQueue()\nfor i in range(100000):\n    big.push((i * 7919) % 10, i)\nout = [big.pop() for _ in range(100000)]\nexp = sorted(range(100000), key=lambda i: ((i * 7919) % 10, i))\nprint(out == exp)\n", "expected": ["[''a'', ''d'', ''b'', ''c'', ''e''] 0", "IndexError", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'my-heapq', 10, 'stdout', 'Свой модуль heapq', 'Реализуйте функции модуля heapq для минимальной кучи на списке: heappush(h, x), heappop(h), heapify(h), heappushpop(h, x), heapreplace(h, x), nsmallest(n, it, key=None), nlargest(n, it, key=None) и merge(*iterables, key=None) (возвращает итератор по слитой отсортированной последовательности). Модуль heapq и sorted не используйте внутри. Проверка сравнивает ваши результаты с настоящим heapq на сотнях тысяч операций.', 'def heappush(h, x):
    pass


def heappop(h):
    pass


def heapify(h):
    pass


def heappushpop(h, x):
    pass


def heapreplace(h, x):
    pass


def nsmallest(n, it, key=None):
    pass


def nlargest(n, it, key=None):
    pass


def merge(*iterables, key=None):
    pass
', 'Основа — две функции: _up (просеивание вверх) и _down (вниз). heappush = append + _up, heappop = последний в корень + _down, heapify — _down от n // 2 − 1 до 0. nsmallest можно через кучу из n лучших; merge — куча из «голов» с номером последовательности.', '{"driver": "import heapq\n\n\ndef ok(a):\n    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))\n\n\nh = []\nfor x in (5, 3, 8, 1, 9, 2):\n    heappush(h, x)\nprint(h[0], ok(h), [heappop(h) for _ in range(6)])\na = [9, 4, 7, 1, 3, 8, 2]\nheapify(a)\nprint(ok(a), a[0])\nh = [1, 3, 2]\nprint(heappushpop(h, 0), heappushpop(h, 5), ok(h), heapreplace(h, 0), ok(h))\nx = 11\ngood = True\nmine, ref = [], []\nfor i in range(200000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    v = x % 5000\n    r = x % 5\n    if r < 3 or not mine:\n        heappush(mine, v)\n        heapq.heappush(ref, v)\n    elif r == 3:\n        good = good and heappop(mine) == heapq.heappop(ref)\n    else:\n        good = good and heappushpop(mine, v) == heapq.heappushpop(ref, v)\n    if i % 20000 == 0:\n        good = good and ok(mine) and sorted(mine) == sorted(ref)\nprint(good, ok(mine), len(mine) == len(ref))\ndata = [(i * 7919) % 10007 for i in range(50000)]\nprint(nsmallest(5, data) == heapq.nsmallest(5, data), nlargest(5, data) == heapq.nlargest(5, data), nsmallest(3, []), nlargest(0, data))\nwords = [\"pear\", \"fig\", \"banana\", \"kiwi\", \"apple\", \"plum\", \"date\"]\nprint(nsmallest(3, words, key=len) == heapq.nsmallest(3, words, key=len), nlargest(2, words, key=len) == heapq.nlargest(2, words, key=len))\nlists = [sorted(rnd) for rnd in ([(i * 31 + j * 17) % 1000 for j in range(2000)] for i in range(50))]\nprint(list(merge(*lists)) == list(heapq.merge(*lists)), list(merge([], [1, 2], [])) == [1, 2], list(merge()) == [])\nprint(list(merge([5, 3, 1], [4, 2], key=lambda v: -v)) == list(heapq.merge([5, 3, 1], [4, 2], key=lambda v: -v)))\n", "expected": ["1 True [1, 2, 3, 5, 8, 9]", "True 1", "0 1 True 2 True", "True True True", "True True [] []", "True True", "True True True", "True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'kth-largest-stream', 11, 'stdout', 'k-й по величине в потоке', 'Реализуйте класс KthLargest(k, nums): конструктор принимает k и начальный список чисел, метод add(val) добавляет число и возвращает k-й по величине элемент среди всех добавленных. Гарантируется, что после первого add элементов хватает. Используйте минимальную кучу размера k (модуль heapq разрешён). Проверка: 300 000 добавлений.', 'import heapq


class KthLargest:
    def __init__(self, k, nums):
        pass

    def add(self, val):
        pass
', 'Куча размера k: в корне k-й по величине. Пока размер меньше k — heappush; иначе, если val больше корня, — heapreplace.', '{"driver": "t = KthLargest(3, [4, 5, 8, 2])\nprint([t.add(v) for v in (3, 5, 10, 9, 4)])\nu = KthLargest(1, [])\nprint([u.add(v) for v in (-3, -2, -4, 0, 4)])\nbig = KthLargest(100, [])\nx = 5\nlast = 0\ntotal = 0\nfor i in range(300000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    last = big.add(x % 1000000)\n    if i >= 100:\n        total += last\nprint(last, total)\n", "expected": ["[4, 5, 5, 8, 8]", "[-3, -2, -2, 0, 4]", "999570 299117860381"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'merge-k-sorted', 12, 'stdout', 'Слияние k отсортированных', 'Напишите функцию merge_k_lists(lists): слейте k отсортированных списков в один отсортированный список. Используйте кучу из «голов» (heapq): время O(N log k). Проверка: 200 списков по 2000 чисел.', 'import heapq


def merge_k_lists(lists):
    pass
', 'В куче — тройки (значение, номер списка, позиция). Достаём минимум, записываем и кладём следующий элемент того же списка (heapreplace); если список кончился — heappop.', '{"driver": "print(merge_k_lists([[1, 4, 5], [1, 3, 4], [2, 6]]), merge_k_lists([]), merge_k_lists([[], []]), merge_k_lists([[3], [], [1, 2]]))\nlists = [sorted((i * 7919 + j * 104729) % 100003 for j in range(2000)) for i in range(200)]\nr = merge_k_lists(lists)\nprint(len(r), r[:5], r == sorted(v for l in lists for v in l))\n", "expected": ["[1, 1, 2, 3, 4, 4, 5, 6] [] [] [1, 2, 3]", "400000 [0, 0, 0, 0, 0] True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'median-stream', 13, 'stdout', 'Медиана потока', 'Реализуйте класс MedianFinder: add_num(x) и find_median() — медиана всех добавленных чисел (для чётного количества — среднее двух средних, вещественное число). Две кучи (heapq): нижняя половина в максимальной, верхняя — в минимальной. Проверка: 300 000 добавлений — вставка в отсортированный список не успеет.', 'import heapq


class MedianFinder:
    def __init__(self):
        pass

    def add_num(self, x):
        pass

    def find_median(self):
        pass
', 'Нижняя половина — max-куча (числа со знаком минус), верхняя — min-куча. После каждой вставки размеры отличаются не больше чем на 1, нижняя не меньше верхней.', '{"driver": "m = MedianFinder()\nout = []\nfor v in (5, 2, 8, 1, 9):\n    m.add_num(v)\n    out.append(m.find_median())\nprint(out)\nm = MedianFinder()\nm.add_num(-1)\nm.add_num(-2)\nprint(m.find_median())\nm = MedianFinder()\nx = 13\nacc = 0.0\nfor i in range(300000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    m.add_num(x % 1000000)\n    if i % 1000 == 0:\n        acc += m.find_median()\nprint(acc)\n", "expected": ["[5.0, 3.5, 5.0, 3.5, 5.0]", "-1.5", "149821698.0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 12, 'min-meeting-rooms', 14, 'stdout', 'Сколько нужно переговорных', 'Дан список встреч — пары [начало, конец) (конец не включается: встреча, закончившаяся в момент t, не мешает встрече, начавшейся в t). Напишите функцию min_rooms(intervals): наименьшее число переговорных комнат. Сортировка по началу и куча моментов окончания (heapq). Проверка: 300 000 встреч.', 'import heapq


def min_rooms(intervals):
    pass
', 'Идём по встречам в порядке начала. В куче — моменты окончания занятых комнат. Освободившиеся (end ≤ start) убираем, новую встречу кладём; максимальный размер кучи — ответ.', '{"driver": "print(min_rooms([[0, 30], [5, 10], [15, 20]]), min_rooms([[7, 10], [2, 4]]), min_rooms([]), min_rooms([[1, 5], [5, 9]]), min_rooms([[1, 4], [2, 5], [3, 6]]))\nx = 21\niv = []\nfor _ in range(300000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    s = x % 1000000\n    x = (x * 1103515245 + 12345) % 2147483648\n    iv.append([s, s + 1 + x % 500])\nprint(min_rooms(iv))\n", "expected": ["2 1 0 1 3", "111"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 13, 'rotations', 0, 'stdout', 'Вращения', 'Дан класс TreeNode. Напишите функции rotate_left(x) и rotate_right(x): левое и правое вращение поддерева с корнем x; верните новый корень поддерева (у x должен быть правый — для левого, левый — для правого вращения ребёнок; иначе верните x без изменений). Порядок ключей при этом не должен нарушаться.', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def rotate_left(x):
    pass


def rotate_right(x):
    pass
', 'Левое: y = x.right; x.right = y.left; y.left = x; вернуть y. Правое — зеркально. Три присваивания ссылок.', '{"driver": "def tup(n):\n    return None if n is None else (n.val, tup(n.left), tup(n.right))\n\n\ndef inorder_list(root):\n    out, st, cur = [], [], root\n    while cur or st:\n        while cur:\n            st.append(cur)\n            cur = cur.left\n        cur = st.pop()\n        out.append(cur.val)\n        cur = cur.right\n    return out\n\n\nt = TreeNode(2, TreeNode(1), TreeNode(5, TreeNode(3), TreeNode(6)))\nr = rotate_left(t)\nprint(tup(r), inorder_list(r))\nr = rotate_right(r)\nprint(tup(r), inorder_list(r))\nprint(tup(rotate_left(TreeNode(1))), tup(rotate_right(TreeNode(1, None, TreeNode(2)))))\nn = 50000\nchain = cur = TreeNode(0)\nfor i in range(1, n):\n    cur.right = TreeNode(i)\n    cur = cur.right\nr = rotate_left(chain)\nprint(r.val, r.left.val, r.right.val, inorder_list(r)[:4])\n", "expected": ["(5, (2, (1, None, None), (3, None, None)), (6, None, None)) [1, 2, 3, 5, 6]", "(2, (1, None, None), (5, (3, None, None), (6, None, None))) [1, 2, 3, 5, 6]", "(1, None, None) (1, None, (2, None, None))", "1 0 2 [0, 1, 2, 3]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 13, 'avl-balance', 1, 'stdout', 'Баланс АВЛ-дерева', 'Дан класс TreeNode. Напишите функцию avl_check(root): кортеж (высота дерева, является ли оно АВЛ-деревом) — то есть для каждого узла высоты поддеревьев отличаются не больше чем на 1. Высота пустого дерева — 0, одного узла — 1. Один обход снизу вверх: проверка подаёт дерево из 100 000 узлов, поэтому пишите итеративно или с большим запасом рекурсии (sys.setrecursionlimit).', 'class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def avl_check(root):
    pass
', 'Нужно знать высоты поддеревьев раньше, чем высоту узла — обход снизу вверх (обратный порядок). Храните высоты в словаре по узлам и проверяйте |hl − hr| ≤ 1 в каждом.', '{"driver": "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n\n\nprint(avl_check(build([4, 2, 6, 1, 3, 5, 7])), avl_check(build([1, None, 2, None, 3])), avl_check(None), avl_check(TreeNode(1)), avl_check(build([1, 2, 3, 4, None, None, None])))\nroot = cur = TreeNode(0)\nfor i in range(1, 100000):\n    cur.left = TreeNode(i)\n    cur = cur.left\nprint(avl_check(root))\ndef perfect(d):\n    return None if d == 0 else TreeNode(d, perfect(d - 1), perfect(d - 1))\nprint(avl_check(perfect(16)))\n", "expected": ["(3, True) (3, False) (0, True) (1, True) (3, True)", "(100000, False)", "(16, True)"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 13, 'avl-rebalance', 2, 'stdout', 'Один шаг балансировки АВЛ', 'Дан класс TreeNode, в котором высоты хранятся в поле h. Напишите функцию rebalance(node): если баланс узла (высота левого − высота правого) равен +2 или −2, выполните нужные вращения (случаи LL, RR, LR, RL) и верните новый корень поддерева, обновив поля h; иначе только обновите h узла и верните его. Баланс детей считается допустимым. Высота пустого поддерева — 0.', 'class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.h = 1


def h(n):
    return n.h if n else 0


def update(n):
    n.h = 1 + max(h(n.left), h(n.right))


def rebalance(node):
    pass
', 'Если баланс +2: когда у левого ребёнка перевешивает правое поддерево (случай LR) — сначала левое вращение ребёнка; затем правое вращение узла. Зеркально для −2. После каждого вращения обновляйте h у опущенного узла, затем у поднятого.', '{"driver": "def mk(k, l=None, r=None):\n    n = Node(k, l, r)\n    update(n)\n    return n\n\n\ndef tup(n):\n    return None if n is None else (n.key, tup(n.left), tup(n.right))\n\n\nll = mk(3, mk(2, mk(1)))\nr = rebalance(ll)\nprint(tup(r), r.h)\nrr = mk(1, None, mk(2, None, mk(3)))\nr = rebalance(rr)\nprint(tup(r), r.h)\nlr = mk(3, mk(1, None, mk(2)))\nr = rebalance(lr)\nprint(tup(r), r.h)\nrl = mk(1, None, mk(3, mk(2)))\nr = rebalance(rl)\nprint(tup(r), r.h)\nok = mk(2, mk(1), mk(3))\nprint(tup(rebalance(ok)), ok.h)\nbig = mk(5, mk(3, mk(2, mk(1)), mk(4)), mk(6))\nr = rebalance(big)\nprint(tup(r), r.h)\n", "expected": ["(2, (1, None, None), (3, None, None)) 2", "(2, (1, None, None), (3, None, None)) 2", "(2, (1, None, None), (3, None, None)) 2", "(2, (1, None, None), (3, None, None)) 2", "(2, (1, None, None), (3, None, None)) 2", "(3, (2, (1, None, None), None), (5, (4, None, None), (6, None, None))) 3"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 13, 'avl-tree-class', 3, 'stdout', 'АВЛ-дерево', 'Реализуйте класс AVLTree: insert(x) (повтор игнорируется), contains(x), inorder(), height() (пустое — 0) и len(t). После каждой вставки дерево должно оставаться АВЛ-деревом (вращения LL, RR, LR, RL). Проверка вставляет 100 000 упорядоченных ключей — обычное дерево поиска вырождается, а ваше должно держать высоту ≤ 1,45 log₂ n + 2. Рекурсия допустима: глубина — логарифм.', 'class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.h = 1


class AVLTree:
    def __init__(self):
        self.root = None
        self._n = 0

    def __len__(self):
        return self._n

    # insert, contains, inorder, height
', 'Рекурсивная вставка возвращает новый корень поддерева; после вставки в ребёнка вызывайте balance(n): обновить высоту, посчитать баланс, при ±2 сделать один из четырёх случаев вращений.', '{"driver": "import math\n\nt = AVLTree()\nfor x in (3, 2, 1, 4, 5, 6, 7, 16, 15, 14):\n    t.insert(x)\nprint(t.inorder(), len(t), t.height(), t.contains(6), t.contains(8))\nt.insert(5)\nprint(len(t), AVLTree().height())\nseq = AVLTree()\nn = 100000\nfor i in range(n):\n    seq.insert(i)\nprint(len(seq), seq.height() <= 1.45 * math.log2(n) + 2, seq.inorder() == list(range(n)))\nrev = AVLTree()\nfor i in range(n, 0, -1):\n    rev.insert(i)\nprint(rev.height() <= 1.45 * math.log2(n) + 2, rev.contains(1), rev.contains(n))\n", "expected": ["[1, 2, 3, 4, 5, 6, 7, 14, 15, 16] 10 4 True False", "10 0", "100000 True True", "True True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 13, 'rb-validate', 4, 'stdout', 'Проверка красно-чёрных правил', 'Дан класс RBNode (key, color, left, right), где color — строка ''R'' или ''B''; пустая ссылка — None (чёрный лист). Напишите функцию black_height(root): чёрная высота дерева (число чёрных узлов на любом пути от корня до пустой ссылки, пустая ссылка не считается), если дерево удовлетворяет правилам красно-чёрного дерева (корень чёрный; у красного узла чёрные дети; чёрная высота всех путей одинакова; ключи упорядочены), иначе −1. Для пустого дерева — 0.', 'class RBNode:
    def __init__(self, key, color, left=None, right=None):
        self.key = key
        self.color = color
        self.left = left
        self.right = right


def black_height(root):
    pass
', 'Рекурсивная функция возвращает чёрную высоту поддерева или −1 при нарушении. Передавайте вниз допустимые границы ключей и «родитель красный»; у узла высоты детей должны совпасть, чёрный добавляет единицу.', '{"driver": "B, R = \"B\", \"R\"\ngood = RBNode(8, B, RBNode(4, R, RBNode(2, B), RBNode(6, B)), RBNode(12, B, RBNode(10, R), RBNode(14, R)))\nprint(black_height(good), black_height(None), black_height(RBNode(5, B)), black_height(RBNode(5, R)))\nred_red = RBNode(8, B, RBNode(4, R, RBNode(2, R), RBNode(6, B)), RBNode(12, B))\nprint(black_height(red_red))\nuneven = RBNode(8, B, RBNode(4, B, RBNode(2, B), RBNode(6, B)), RBNode(12, B))\nprint(black_height(uneven))\norder = RBNode(8, B, RBNode(9, R), RBNode(12, R))\nprint(black_height(order))\ndef perfect(d, lo, hi):\n    if d == 0:\n        return None\n    m = (lo + hi) // 2\n    return RBNode(m, B, perfect(d - 1, lo, m - 1), perfect(d - 1, m + 1, hi))\nprint(black_height(perfect(15, 1, 2 ** 15 - 1)))\n", "expected": ["2 0 1 -1", "-1", "-1", "-1", "15"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 13, 'rb-bounds', 5, 'func', 'Оценки красно-чёрного дерева', 'Напишите функцию rb_bounds(b, n): кортеж из двух чисел. Первое — наименьшее число узлов в красно-чёрном дереве с чёрной высотой b (b чёрных узлов на каждом пути до пустой ссылки): 2**b − 1. Второе — наибольшая возможная высота красно-чёрного дерева из n узлов (в узлах, пустое дерево — 0): целая часть от 2·log₂(n + 1).', 'import math


def rb_bounds(b, n):
    pass
', 'Минимум узлов достигается, когда все узлы чёрные и дерево полное: 2^b − 1. Максимальная высота — из неравенства h ≤ 2·log₂(n + 1), берите целую часть.', '{"func": "rb_bounds", "tests": [{"args": [1, 1], "expected": {"__tuple__": [1, 2]}}, {"args": [3, 7], "expected": {"__tuple__": [7, 6]}}, {"args": [4, 100], "expected": {"__tuple__": [15, 13]}}, {"args": [10, 1000], "expected": {"__tuple__": [1023, 19]}}, {"args": [0, 0], "expected": {"__tuple__": [0, 0]}}, {"args": [5, 31], "expected": {"__tuple__": [31, 10]}}, {"args": [2, 3], "expected": {"__tuple__": [3, 4]}}, {"args": [20, 1000000], "expected": {"__tuple__": [1048575, 39]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 13, 'rb-insert-case', 6, 'func', 'Случай вставки', 'После вставки красного узла родитель оказался красным. Напишите функцию insert_case(parent_color, uncle_color, node_side, parent_side): строка с нужным действием. Цвета — ''R'' или ''B'' (пустой дядя — ''B''); стороны — ''L'' или ''R'': node_side — какой ребёнок родителя наш узел, parent_side — каким ребёнком деда является родитель. Результат: ''done'' — родитель чёрный, ничего делать не нужно; ''recolor'' — дядя красный (перекраска и подъём); ''kink'' — дядя чёрный и узел «в изломе» (стороны разные: вращение родителя, затем деда); ''line'' — дядя чёрный и узел на одной линии (стороны совпадают: вращение деда с перекраской).', 'def insert_case(parent_color, uncle_color, node_side, parent_side):
    pass
', 'Четыре ветки подряд: чёрный родитель → done; красный дядя → recolor; иначе по сторонам: разные → kink, одинаковые → line.', '{"func": "insert_case", "tests": [{"args": ["B", "R", "L", "L"], "expected": "done"}, {"args": ["R", "R", "L", "R"], "expected": "recolor"}, {"args": ["R", "B", "R", "L"], "expected": "kink"}, {"args": ["R", "B", "L", "L"], "expected": "line"}, {"args": ["R", "B", "R", "R"], "expected": "line"}, {"args": ["R", "B", "L", "R"], "expected": "kink"}, {"args": ["B", "B", "R", "R"], "expected": "done"}, {"args": ["R", "R", "R", "R"], "expected": "recolor"}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 13, 'llrb-insert', 7, 'stdout', 'Левонаклонное красно-чёрное дерево', 'Реализуйте класс LLRB (левонаклонное красно-чёрное дерево Седжвика): insert(x) (повтор игнорируется), contains(x), inorder(), height() и black_height_ok() — выполняются ли правила (корень чёрный, красных подряд нет, красных правых ссылок нет, чёрные высоты равны). Вставка рекурсивная: вставить как в дереве поиска красным узлом, затем на пути вверх: правая красная и левая чёрная → левое вращение; левая красная с красной левой внучкой → правое вращение; обе ссылки красные → перекрасить (flip_colors). Корень после вставки чёрный.', 'RED, BLACK = True, False


class Node:
    def __init__(self, key, color=RED):
        self.key = key
        self.color = color
        self.left = None
        self.right = None


class LLRB:
    def __init__(self):
        self.root = None

    # insert, contains, inorder, height, black_height_ok
', 'Три шага в конце рекурсии (в таком порядке): если правая ссылка красная, а левая нет — rotate_left; если левая и её левая красные — rotate_right; если обе красные — flip_colors. rotate_* переносит цвет корня на поднявшийся узел, а опустившийся делает красным.', '{"driver": "import math\n\nt = LLRB()\nfor x in (5, 3, 8, 1, 4, 7, 9, 2, 6):\n    t.insert(x)\n    assert t.black_height_ok()\nprint(t.inorder(), t.height(), t.black_height_ok(), t.contains(6), t.contains(10))\nt.insert(5)\nprint(len(t.inorder()))\nn = 20000\na = LLRB()\nfor i in range(n):\n    a.insert(i)\nprint(a.inorder() == list(range(n)), a.black_height_ok(), a.height() <= 2 * math.log2(n + 1) + 1)\nb = LLRB()\nx = 7\nvals = []\nfor _ in range(20000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    vals.append(x % 100000)\nfor i, v in enumerate(vals):\n    b.insert(v)\n    if i % 2000 == 0:\n        assert b.black_height_ok()\nprint(b.inorder() == sorted(set(vals)), b.black_height_ok(), b.height() <= 2 * math.log2(len(set(vals)) + 1) + 1)\n", "expected": ["[1, 2, 3, 4, 5, 6, 7, 8, 9] 4 True True False", "9", "True True True", "True True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 13, 'rb-tree-class', 8, 'stdout', 'Красно-чёрное дерево', 'Реализуйте класс RBTree по правилам CLRS: узлы с родителем и общим листом-дозорным NIL (чёрным), методы insert(x) (повтор игнорируется), contains(x), inorder(), height() и valid() — выполнены ли все правила (корень чёрный, красных подряд нет, чёрные высоты равны, порядок ключей). Вставка: красный узел, затем исправление: красный дядя — перекраска и подъём; чёрный дядя — вращение излома, затем вращение деда с перекраской. Проверка вставляет 100 000 упорядоченных и случайных ключей.', 'BLACK, RED = 0, 1


class Node:
    def __init__(self, key=None, color=BLACK):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RBTree:
    def __init__(self):
        self.NIL = Node()
        self.root = self.NIL

    # insert, contains, inorder, height, valid
', 'Вставка: как в дереве поиска, узел красный с детьми NIL. Исправление пока родитель красный: дядя красный — перекрасить родителя, дядю и деда, подняться к деду; дядя чёрный — если излом, повернуть родителя; затем перекрасить родителя в чёрный, деда в красный и повернуть деда. В конце корень чёрный.', '{"driver": "import math\n\nt = RBTree()\nfor x in (41, 38, 31, 12, 19, 8):\n    t.insert(x)\n    assert t.valid()\nprint(t.inorder(), t.height(), t.valid(), t.contains(19), t.contains(20), t.root.color)\nt.insert(19)\nprint(len(t.inorder()))\nn = 100000\na = RBTree()\nfor i in range(n):\n    a.insert(i)\nprint(a.inorder() == list(range(n)), a.valid(), a.height() <= 2 * math.log2(n + 1))\nb = RBTree()\nx = 9\nvals = []\nfor _ in range(100000):\n    x = (x * 1103515245 + 12345) % 2147483648\n    vals.append(x % 10**6)\nfor i, v in enumerate(vals):\n    b.insert(v)\n    if i % 10000 == 0:\n        assert b.valid()\nu = len(set(vals))\nprint(b.inorder() == sorted(set(vals)), b.valid(), b.height() <= 2 * math.log2(u + 1))\n", "expected": ["[8, 12, 19, 31, 38, 41] 4 True True False 0", "6", "True True True", "True True True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-range-sums', 0, 'func', 'Суммы на отрезках: префиксные суммы', 'Напишите функцию range_sums(a, queries): queries — список пар [l, r] (индексы с нуля, обе границы включены); верните список сумм a[l] + … + a[r]. Постройте префиксные суммы один раз, каждый запрос — за константу.', 'def range_sums(a, queries):
    pass
', 'p[i + 1] = p[i] + a[i]; сумма на [l, r] равна p[r + 1] − p[l].', '{"func": "range_sums", "tests": [{"args": [[3, 1, 4, 1, 5, 9, 2, 6], [[2, 5], [0, 7], [3, 3]]], "expected": [19, 31, 1]}, {"args": [[-2, 5, -1], [[0, 2], [1, 1]]], "expected": [2, 5]}, {"args": [[7], [[0, 0]]], "expected": [7]}, {"args": [[1, 2, 3], []], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-fenwick-range', 1, 'func', 'Какой отрезок хранит ячейка Фенвика', 'В дереве Фенвика элементы нумеруются с единицы, а ячейка i хранит сумму отрезка длины i & −i, заканчивающегося в i. Напишите функцию fenwick_range(i): кортеж (l, r) — границы этого отрезка. Например, fenwick_range(12) = (9, 12).', 'def fenwick_range(i):
    pass
', 'Длина отрезка — i & −i; он заканчивается в i.', '{"func": "fenwick_range", "tests": [{"args": [12], "expected": {"__tuple__": [9, 12]}}, {"args": [8], "expected": {"__tuple__": [1, 8]}}, {"args": [7], "expected": {"__tuple__": [7, 7]}}, {"args": [6], "expected": {"__tuple__": [5, 6]}}, {"args": [1], "expected": {"__tuple__": [1, 1]}}, {"args": [10], "expected": {"__tuple__": [9, 10]}}, {"args": [1024], "expected": {"__tuple__": [1, 1024]}}, {"args": [1000], "expected": {"__tuple__": [993, 1000]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-prefix-path', 2, 'func', 'Путь запроса префикса', 'Напишите функцию prefix_path(i): список ячеек дерева Фенвика, которые складываются при запросе суммы первых i элементов, в порядке посещения. Начните с i и на каждом шаге убирайте младший бит; для 11 — [11, 10, 8], для 0 — пустой список.', 'def prefix_path(i):
    pass
', 'Цикл: пока i > 0, записываем i и вычитаем i & −i.', '{"func": "prefix_path", "tests": [{"args": [11], "expected": [11, 10, 8]}, {"args": [7], "expected": [7, 6, 4]}, {"args": [8], "expected": [8]}, {"args": [0], "expected": []}, {"args": [1], "expected": [1]}, {"args": [1023], "expected": [1023, 1022, 1020, 1016, 1008, 992, 960, 896, 768, 512]}, {"args": [12], "expected": [12, 8]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-update-path', 3, 'func', 'Путь изменения', 'Напишите функцию update_path(i, n): список ячеек дерева Фенвика размера n, которые меняются при изменении элемента i, в порядке посещения. Начните с i и прибавляйте младший бит, пока не выйдете за n; update_path(3, 8) = [3, 4, 8].', 'def update_path(i, n):
    pass
', 'Цикл: пока i ≤ n, записываем i и прибавляем i & −i.', '{"func": "update_path", "tests": [{"args": [3, 8], "expected": [3, 4, 8]}, {"args": [8, 8], "expected": [8]}, {"args": [5, 12], "expected": [5, 6, 8]}, {"args": [1, 16], "expected": [1, 2, 4, 8, 16]}, {"args": [7, 7], "expected": [7]}, {"args": [6, 100], "expected": [6, 8, 16, 32, 64]}, {"args": [9, 8], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-fenwick', 4, 'stdout', 'Дерево Фенвика', 'Напишите класс Fenwick: конструктор Fenwick(n) создаёт нулевой массив из n элементов (индексы с 1); add(i, delta) прибавляет delta к элементу i; prefix(i) — сумма первых i элементов (prefix(0) = 0); range_sum(l, r) — сумма элементов с l по r включительно. Всё за O(log n): проверка выполняет двести тысяч операций над массивом из двухсот тысяч элементов.', 'class Fenwick:
    def __init__(self, n):
        pass

    def add(self, i, delta):
        pass

    def prefix(self, i):
        pass

    def range_sum(self, l, r):
        pass
', 'Ячейка i хранит сумму отрезка длины i & −i: add идёт вверх (i += i & −i), prefix — вниз (i −= i & −i).', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nf = Fenwick(8)\nfor i, v in enumerate([2, 5, 1, 4, 3, 6, 2, 7], 1):\n    f.add(i, v)\nprint(f.prefix(7), f.range_sum(3, 6), f.prefix(0), f.range_sum(1, 8))\nf.add(3, 5)\nprint(f.prefix(3), f.range_sum(3, 3))\nn = 200000\nf = Fenwick(n)\nx = 5\ntotal = 0\nfor q in range(200000):\n    x = nxt(x)\n    i = 1 + x % n\n    x = nxt(x)\n    if q % 3 == 0:\n        f.add(i, x % 1000 - 500)\n    elif q % 3 == 1:\n        total += f.prefix(i)\n    else:\n        j = 1 + x % n\n        total += f.range_sum(min(i, j), max(i, j))\nprint(total, f.prefix(n))\n", "expected": ["23 14 0 30", "13 6", "-1754336517 -55366"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-fenwick-build', 5, 'stdout', 'Построение Фенвика за линейное время', 'Напишите функцию build_fenwick(a): список tree длины n + 1 (tree[0] = 0), в котором tree[i] — сумма a[i − (i & −i)] … a[i − 1] (то есть отрезка длины i & −i, заканчивающегося на i-м элементе при нумерации с единицы). Время — O(n): n последовательных вызовов add дали бы n log n; проверка использует два с половиной миллиона чисел.', 'def build_fenwick(a):
    pass
', 'Положите a в tree[1..n], затем для каждого i прибавьте tree[i] к родителю i + (i & −i), если он не вышел за n.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nprint(build_fenwick([2, 5, 1, 4, 3, 6, 2, 7]))\ndef brute(a):\n    t = [0] * (len(a) + 1)\n    for i in range(1, len(a) + 1):\n        t[i] = sum(a[i - (i & -i): i])\n    return t\ny = 3\nb = []\nfor _ in range(1000):\n    y = nxt(y)\n    b.append(y % 100 - 50)\nprint(build_fenwick(b) == brute(b), build_fenwick([]) == [0])\nN = 2500000\nbig = []\nfor _ in range(N):\n    y = nxt(y)\n    big.append(y & 1023)\nt = build_fenwick(big)\nprint(len(t), t[N], t[2 ** 21], sum(t) % 1000003)\n", "expected": ["[0, 2, 7, 1, 12, 3, 9, 2, 30]", "True True", "2500001 17168 1072520550 158394"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-inversions', 6, 'stdout', 'Подсчёт инверсий', 'Напишите функцию count_inversions(a): число пар i < j, для которых a[i] > a[j]. Проверка подаёт двести тысяч чисел — квадратичный перебор не успеет. Подумайте о дереве Фенвика по сжатым значениям или о сортировке слиянием.', 'def count_inversions(a):
    pass
', 'Идите слева направо: сколько уже встречённых элементов больше текущего — это (число встреченных) − (число ≤ текущего).', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nprint(count_inversions([2, 4, 1, 3, 5]), count_inversions([]), count_inversions([3, 2, 1]), count_inversions([1, 1, 1]))\nn = 200000\nx = 3\na = []\nfor _ in range(n):\n    x = nxt(x)\n    a.append(x % 1000000)\nprint(count_inversions(a))\nprint(count_inversions(list(range(n, 0, -1))))\n", "expected": ["3 0 3 0", "10012382156", "19999900000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-range-add', 7, 'stdout', 'Прибавление на отрезке, значение в точке', 'Напишите класс RangeAdd: RangeAdd(n) — массив из n нулей (индексы с нуля); add(l, r, v) прибавляет v ко всем элементам с l по r включительно; get(i) возвращает значение i-го элемента. Оба — за O(log n): храните разности в дереве Фенвика. Проверка — двести тысяч операций.', 'class RangeAdd:
    def __init__(self, n):
        pass

    def add(self, l, r, v):
        pass

    def get(self, i):
        pass
', 'add(l, r, v) — это два точечных изменения разностей: +v в позиции l и −v в позиции r + 1; get — префиксная сумма разностей.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nt = RangeAdd(6)\nt.add(1, 3, 5)\nt.add(0, 5, 1)\nprint([t.get(i) for i in range(6)])\nn = 200000\nt = RangeAdd(n)\nx = 9\ntotal = 0\nfor q in range(200000):\n    x = nxt(x)\n    l = x % n\n    x = nxt(x)\n    r = l + x % (n - l)\n    x = nxt(x)\n    if q % 2:\n        t.add(l, r, x % 100 - 50)\n    else:\n        total += t.get(l) + t.get(r)\nprint(total, t.get(0), t.get(n - 1))\n", "expected": ["[1, 6, 6, 6, 1, 1]", "-1353428639 0 33"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-order-set', 8, 'stdout', 'k-е по величине через спуск по Фенвику', 'Напишите класс OrderSet: OrderSet(maxv) — пустой набор значений от 1 до maxv (повторы допустимы); add(x) добавляет x; discard(x) удаляет одно вхождение x (оно точно есть); kth(k) — k-е по возрастанию значение (k с единицы). Всё за O(log maxv): храните счётчики в дереве Фенвика и спускайтесь по битам. Запрещены bisect, heapq, sorted и методы insert, remove, pop, sort, index, count.', 'class OrderSet:
    def __init__(self, maxv):
        pass

    def add(self, x):
        pass

    def discard(self, x):
        pass

    def kth(self, k):
        pass
', 'В узле Фенвика лежит число элементов отрезка: спускайтесь от старшего бита, прибавляя шаг, пока накопленное меньше k.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nimport ast as _ast\n_src = open(\"/sandbox/solution.py\", encoding=\"utf-8\").read()\n_bad = set()\nfor _n in _ast.walk(_ast.parse(_src)):\n    if isinstance(_n, _ast.Attribute) and _n.attr in {''sort'', ''index'', ''pop'', ''remove'', ''count'', ''insert''}:\n        _bad.add(\".\" + _n.attr + \"()\")\n    elif False and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, _ast.NotIn)) for _o in _n.ops):\n        _bad.add(\"in\")\n    elif False and isinstance(_n, _ast.Slice):\n        _bad.add(\"срезы\")\n    elif isinstance(_n, _ast.Name) and _n.id in {''sorted''}:\n        _bad.add(_n.id)\n    elif type(_n).__name__ in set():\n        _bad.add(\"словари и множества\")\n    elif isinstance(_n, _ast.Import) and any(_a.name.split(\".\")[0] in {''bisect'', ''re'', ''heapq''} for _a in _n.names):\n        _bad.add(\"import\")\n    elif isinstance(_n, _ast.ImportFrom) and (_n.module or \"\").split(\".\")[0] in {''bisect'', ''re'', ''heapq''}:\n        _bad.add(\"import\")\nif _bad:\n    print(\"запрещённые приёмы:\", \", \".join(sorted(_bad)))\nelse:\n    s = OrderSet(10)\n    for v in [5, 3, 8, 3, 10]:\n        s.add(v)\n    print([s.kth(k) for k in range(1, 6)])\n    s.discard(3)\n    print([s.kth(k) for k in range(1, 5)])\n    M = 1000000\n    s = OrderSet(M)\n    x = 17\n    size = 0\n    total = 0\n    for q in range(200000):\n        x = nxt(x)\n        if size < 1000 or q % 3:\n            s.add(1 + x % M)\n            size += 1\n        else:\n            v = s.kth(1 + x % size)\n            s.discard(v)\n            size -= 1\n            total += v\n    print(size, total, s.kth(1), s.kth(size))\n", "expected": ["[3, 3, 5, 8, 10]", "[3, 5, 8, 10]", "67334 33223511952 6 999986"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-smaller-before', 9, 'stdout', 'Сколько меньших слева', 'Напишите функцию smaller_before(a): список res, где res[i] — сколько элементов слева от i-го строго меньше a[i]. Проверка — двести тысяч чисел: квадратичный перебор не успеет.', 'def smaller_before(a):
    pass
', 'Сожмите значения в ранги; считайте в дереве Фенвика, сколько встретилось рангов меньше текущего.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nprint(smaller_before([3, 1, 4, 1, 5, 9, 2, 6]), smaller_before([]), smaller_before([5, 5, 5]))\nn = 200000\nx = 1\na = []\nfor _ in range(n):\n    x = nxt(x)\n    a.append(x % 100000)\nr = smaller_before(a)\nprint(sum(r), r[-1], max(r))\n", "expected": ["[0, 0, 2, 0, 4, 5, 2, 6] [] [0, 0, 0]", "10016927167 86989 199517"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-distinct-ranges', 10, 'stdout', 'Различные числа на отрезках', 'Напишите функцию distinct_in_ranges(a, queries): для каждого запроса [l, r] (с нуля, обе границы включены) — сколько различных значений среди a[l..r]. Ответы — в порядке запросов. Проверка — двести тысяч элементов и запросов. Идея: обработайте запросы офлайн по правому краю и храните в дереве Фенвика единицы на последних вхождениях значений.', 'def distinct_in_ranges(a, queries):
    pass
', 'Идите по r слева направо: на последнем вхождении значения держите единицу, на предыдущем — снимайте; ответ — сумма на [l, r].', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nprint(distinct_in_ranges([1, 2, 1, 3, 2], [[0, 4], [1, 2], [2, 2], [0, 0], [2, 4]]))\nn = 200000\nx = 21\na = []\nfor _ in range(n):\n    x = nxt(x)\n    a.append(x % 50000)\nqs = []\nfor _ in range(200000):\n    x = nxt(x)\n    l = x % n\n    x = nxt(x)\n    qs.append([l, l + x % (n - l)])\nr = distinct_in_ranges(a, qs)\nprint(sum(r), r[:3], r[-3:])\n", "expected": ["[3, 2, 1, 1, 3]", "5074342404 [43270, 40408, 20537] [18764, 27112, 9643]"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-tree-sum', 11, 'stdout', 'Дерево отрезков: сумма', 'Напишите класс SegTree: SegTree(a) строит дерево по списку a; update(i, v) присваивает a[i] = v; query(l, r) возвращает сумму a[l] + … + a[r − 1] (правая граница не включена). Операции — за O(log n): проверка выполняет двести тысяч операций над массивом из двухсот тысяч чисел.', 'class SegTree:
    def __init__(self, a):
        pass

    def update(self, i, v):
        pass

    def query(self, l, r):
        pass
', 'Листья — во второй половине массива из 2n элементов; родитель i — сумма детей 2i и 2i + 1. Запрос идёт двумя указателями l и r и поднимается к корню.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nt = SegTree([5, 3, 7, 1, 4, 2, 6, 8])\nprint(t.query(0, 8), t.query(2, 7), t.query(3, 4), t.query(5, 5))\nt.update(3, 6)\nprint(t.query(0, 8), t.query(2, 4))\nn = 200000\nx = 33\na = []\nfor _ in range(n):\n    x = nxt(x)\n    a.append(x % 1000)\nt = SegTree(a)\ntotal = 0\nfor q in range(200000):\n    x = nxt(x)\n    i = x % n\n    x = nxt(x)\n    if q % 2:\n        t.update(i, x % 1000)\n    else:\n        total += t.query(i, i + 1 + x % (n - i))\nprint(total, t.query(0, n))\n", "expected": ["36 20 1 0", "41 13", "2497352033162 99847686"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-tree-generic', 12, 'stdout', 'Дерево отрезков для любой операции', 'Напишите класс GenericTree: GenericTree(a, op, neutral) — дерево для ассоциативной операции op с нейтральным элементом neutral (op не обязательно коммутативна: склейка строк, умножение матриц); update(i, v) присваивает a[i] = v; query(l, r) — результат op по элементам a[l..r − 1] слева направо (для пустого отрезка — neutral). Порядок аргументов op важен.', 'class GenericTree:
    def __init__(self, a, op, neutral):
        pass

    def update(self, i, v):
        pass

    def query(self, l, r):
        pass
', 'Накапливайте левую и правую части отдельно: left = op(left, t[l]), right = op(t[r], right) — тогда порядок сохраняется.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nimport math\nt = GenericTree([4, 8, 6, 9, 12, 15], math.gcd, 0)\nprint(t.query(0, 3), t.query(3, 6), t.query(1, 2), t.query(2, 2))\nt.update(1, 3)\nprint(t.query(0, 3))\ns = GenericTree(list(\"hello\"), lambda p, q: p + q, \"\")\nprint(s.query(0, 5), s.query(1, 4), repr(s.query(2, 2)))\ns.update(0, \"J\")\nprint(s.query(0, 5))\nn = 100000\nx = 41\na = []\nfor _ in range(n):\n    x = nxt(x)\n    a.append(x % 1000003)\nm = GenericTree(a, min, 10 ** 9)\ntotal = 0\nfor q in range(100000):\n    x = nxt(x)\n    i = x % n\n    x = nxt(x)\n    if q % 2:\n        m.update(i, x % 1000003)\n    else:\n        total += m.query(i, i + 1 + x % (n - i))\nprint(total)\n", "expected": ["2 3 8 0", "1", "hello ell ''''", "Jello", "33015139"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-first-at-least', 13, 'stdout', 'Первый элемент не меньше x', 'Напишите класс MaxTree: MaxTree(a) строит дерево максимумов; update(i, v) присваивает a[i] = v; first_at_least(x) возвращает наименьший индекс i с a[i] ≥ x или -1. Ответ — за один спуск от корня, O(log n): проверка размещает сто тысяч заявок в гостинице на 131072 номера.', 'class MaxTree:
    def __init__(self, a):
        pass

    def update(self, i, v):
        pass

    def first_at_least(self, x):
        pass
', 'В узле хранится максимум: если левый ребёнок содержит значение ≥ x — идите влево, иначе вправо.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nt = MaxTree([3, 9, 4, 12, 7])\nprint(t.first_at_least(10), t.first_at_least(4), t.first_at_least(13), t.first_at_least(1))\nt.update(3, 2)\nprint(t.first_at_least(10), t.first_at_least(8))\nn = 131072\nt = MaxTree([1000] * n)\nx = 77\nplaced = 0\nlast = 0\nfor _ in range(100000):\n    x = nxt(x)\n    need = 500 + x % 501\n    room = t.first_at_least(need)\n    if room >= 0:\n        placed += 1\n        last = room\n        t.update(room, t.t[t.n + room] - need)\nprint(placed, last)\n", "expected": ["3 1 -1 0", "-1 1", "100000 99908"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-max-subarray', 14, 'stdout', 'Максимальная подотрезочная сумма с изменениями', 'Напишите класс MaxSub: MaxSub(a) строит структуру; update(i, v) присваивает a[i] = v; query(l, r) — наибольшая сумма непустого подотрезка внутри a[l..r − 1] (l < r). В узле храните четвёрку: сумма всего отрезка, лучший префикс, лучший суффикс и лучший подотрезок. Проверка — сто тысяч операций.', 'class MaxSub:
    def __init__(self, a):
        pass

    def update(self, i, v):
        pass

    def query(self, l, r):
        pass
', 'Склейка (s₁, p₁, u₁, b₁) и (s₂, p₂, u₂, b₂): сумма s₁ + s₂, префикс max(p₁, s₁ + p₂), суффикс max(u₂, s₂ + u₁), лучший max(b₁, b₂, u₁ + p₂).', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nt = MaxSub([-2, 1, -3, 4, -1, 2, 1, -5, 4])\nprint(t.query(0, 9), t.query(0, 3), t.query(7, 8), t.query(3, 7))\nt.update(7, 10)\nprint(t.query(0, 9), t.query(6, 9))\nn = 50000\nx = 55\na = []\nfor _ in range(n):\n    x = nxt(x)\n    a.append(x % 201 - 100)\nt = MaxSub(a)\ntotal = 0\nfor q in range(50000):\n    x = nxt(x)\n    i = x % n\n    x = nxt(x)\n    if q % 2:\n        t.update(i, x % 201 - 100)\n    else:\n        total += t.query(i, i + 1 + x % (n - i))\nprint(total, t.query(0, n))\n", "expected": ["6 1 -5 6", "20 15", "143525107 10739"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-lazy-add', 15, 'stdout', 'Ленивые метки: прибавление и сумма', 'Напишите класс LazyTree: LazyTree(a); add(l, r, x) прибавляет x ко всем элементам a[l..r − 1]; sum(l, r) — сумма a[l..r − 1]. Обе операции — за O(log n) с ленивыми метками. Проверка — пятьдесят тысяч операций над массивом из пятидесяти тысяч чисел.', 'class LazyTree:
    def __init__(self, a):
        pass

    def add(self, l, r, x):
        pass

    def sum(self, l, r):
        pass
', 'Узел, целиком накрытый операцией, обновляется сразу и получает метку; перед спуском метку передают детям (push).', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nt = LazyTree([1, 2, 3, 4, 5])\nt.add(1, 4, 10)\nprint(t.sum(0, 5), t.sum(1, 2), t.sum(2, 4))\nt.add(0, 5, -1)\nprint(t.sum(0, 5), t.sum(4, 5))\nn = 50000\nx = 91\na = []\nfor _ in range(n):\n    x = nxt(x)\n    a.append(x % 100)\nt = LazyTree(a)\ntotal = 0\nfor q in range(50000):\n    x = nxt(x)\n    l = x % n\n    x = nxt(x)\n    r = l + 1 + x % (n - l)\n    x = nxt(x)\n    if q % 2:\n        t.add(l, r, x % 21 - 10)\n    else:\n        total += t.sum(l, r)\nprint(total, t.sum(0, n))\n", "expected": ["45 12 27", "40 4", "40251771747 7042763"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-lazy-assign', 16, 'stdout', 'Ленивые метки: присваивание и сумма', 'Напишите класс AssignTree: AssignTree(a); assign(l, r, x) присваивает x всем элементам a[l..r − 1]; sum(l, r) — сумма a[l..r − 1]. Метка — «присвоить x» (None, если метки нет): новая метка заменяет старую, а ответ узла равен x умножить на длину отрезка. Проверка — сто тысяч элементов и шестьдесят тысяч операций.', 'class AssignTree:
    def __init__(self, a):
        pass

    def assign(self, l, r, x):
        pass

    def sum(self, l, r):
        pass
', 'Метка None означает «ничего не откладывали»; при push обновите ответы детей как x · длина и передайте им метку.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nt = AssignTree([1, 2, 3, 4, 5])\nt.assign(1, 4, 7)\nprint(t.sum(0, 5), t.sum(1, 2), t.sum(3, 5))\nt.assign(0, 5, 0)\nprint(t.sum(0, 5))\nn = 100000\nx = 5\na = []\nfor _ in range(n):\n    x = nxt(x)\n    a.append(x % 100)\nt = AssignTree(a)\ntotal = 0\nfor q in range(60000):\n    x = nxt(x)\n    l = x % n\n    x = nxt(x)\n    r = l + 1 + x % (n - l)\n    x = nxt(x)\n    if q % 2 == 0:\n        t.assign(l, r, x % 50)\n    else:\n        total += t.sum(l, r)\nprint(total, t.sum(0, n))\n", "expected": ["27 7 12", "0", "18336188223 1509608"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-sparse-table', 17, 'stdout', 'Разреженная таблица', 'Напишите класс SparseTable: SparseTable(a) строит таблицу за O(n log n); query(l, r) возвращает минимум a[l..r − 1] (l < r) за O(1) — через две перекрывающиеся степени двойки. Проверка — триста тысяч элементов и пятьсот тысяч запросов.', 'class SparseTable:
    def __init__(self, a):
        pass

    def query(self, l, r):
        pass
', 'Строка k хранит минимумы на отрезках длины 2ᵏ: t[k][i] = min(t[k − 1][i], t[k − 1][i + 2^(k−1)]). Для запроса возьмите k = floor(log₂(r − l)).', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nt = SparseTable([5, 2, 4, 7, 1, 3, 6, 8])\nprint(t.query(1, 6), t.query(0, 8), t.query(3, 4), t.query(5, 8))\nn = 300000\nx = 61\na = []\nfor _ in range(n):\n    x = nxt(x)\n    a.append(x % 1000000)\nt = SparseTable(a)\ntotal = 0\nfor _ in range(500000):\n    x = nxt(x)\n    l = x % n\n    x = nxt(x)\n    total += t.query(l, l + 1 + x % (n - l))\nprint(total, t.query(0, n))\n", "expected": ["1 1 7 3", "141215170 3"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-fenwick-2d', 18, 'stdout', 'Двумерное дерево Фенвика', 'Напишите класс Fenwick2D: Fenwick2D(n, m) — нулевая матрица n × m (индексы с нуля); add(x, y, v) прибавляет v к клетке (x, y); sum(x1, y1, x2, y2) — сумма по прямоугольнику с углами (x1, y1) и (x2, y2), включая границы. Каждая операция — O(log n · log m): проверка — матрица 1000 × 1000 и сто тысяч операций.', 'class Fenwick2D:
    def __init__(self, n, m):
        pass

    def add(self, x, y, v):
        pass

    def sum(self, x1, y1, x2, y2):
        pass
', 'Вложенный цикл: внешний по x (i += i & −i), внутренний по y. Прямоугольник — четыре префикса, как в двумерных суммах.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nt = Fenwick2D(3, 4)\nt.add(0, 0, 5)\nt.add(1, 2, 3)\nt.add(2, 3, 7)\nprint(t.sum(0, 0, 2, 3), t.sum(1, 1, 2, 3), t.sum(0, 0, 0, 0), t.sum(1, 0, 1, 1))\nn = m = 1000\nt = Fenwick2D(n, m)\nx = 13\ntotal = 0\nfor q in range(100000):\n    x = nxt(x)\n    a = x % n\n    x = nxt(x)\n    b = x % m\n    x = nxt(x)\n    if q % 2:\n        t.add(a, b, x % 100)\n    else:\n        c = a + x % (n - a)\n        x = nxt(x)\n        d = b + x % (m - b)\n        total += t.sum(a, b, c, d)\nprint(total, t.sum(0, 0, n - 1, m - 1))\n", "expected": ["15 10 5 0", "3804190072 2471190"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 14, 'seg-lis', 19, 'stdout', 'Длиннейшая возрастающая подпоследовательность', 'Напишите функцию lis_length(a): длина наибольшей строго возрастающей подпоследовательности списка (не обязательно из соседних элементов). Проверка — сто тысяч чисел, поэтому нужно O(n log n): дерево Фенвика по максимуму (в позиции значения хранится лучшая длина) или метод «хвостов» с двоичным поиском.', 'def lis_length(a):
    pass
', 'Дерево Фенвика по максимуму: dp[значение] = 1 + максимум по меньшим значениям; ответ — максимум всех dp.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nprint(lis_length([10, 9, 2, 5, 3, 7, 101, 18]), lis_length([0, 1, 0, 3, 2, 3]), lis_length([7, 7, 7]), lis_length([]))\nn = 100000\nx = 8\na = []\nfor _ in range(n):\n    x = nxt(x)\n    a.append(x % 1000000)\nprint(lis_length(a), lis_length(list(range(n))), lis_length(list(range(n, 0, -1))))\n", "expected": ["4 4 1 0", "630 100000 1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 15, 'graph-bfs-distances', 0, 'func', 'Расстояния обходом в ширину', 'Напишите функцию bfs_distances(graph, start): graph — словарь «вершина → список соседей» (имена вершин — строки). Верните словарь «вершина → минимальное число рёбер от start» для всех достижимых вершин.', 'from collections import deque


def bfs_distances(graph, start):
    pass
', 'Очередь и словарь расстояний (он же «посещённые»): сосед получает dist[v] + 1, если ещё не посещён.', '{"func": "bfs_distances", "tests": [{"args": [{"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}, "a"], "expected": {"a": 0, "b": 1, "c": 1, "d": 2}}, {"args": [{"x": []}, "x"], "expected": {"x": 0}}, {"args": [{"a": ["b"], "b": ["a"], "c": ["a"]}, "a"], "expected": {"a": 0, "b": 1}}, {"args": [{"1": ["2"], "2": ["3"], "3": ["1"]}, "2"], "expected": {"1": 2, "2": 0, "3": 1}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 15, 'graph-components', 1, 'stdout', 'Компоненты связности', 'Напишите функцию count_components(graph): число компонент связности неориентированного графа (словарь «вершина → список соседей», каждое ребро записано в обе стороны). Проверка подаёт цепочку из 200 000 вершин, поэтому обход должен быть итеративным (рекурсия упадёт).', 'def count_components(graph):
    pass
', 'Для каждой непосещённой вершины запустите обход со стеком/очередью и увеличьте счётчик компонент.', '{"driver": "print(count_components({''a'': [''b''], ''b'': [''a''], ''c'': []}), count_components({}), count_components({''x'': []}))\nn = 200000\ng = {i: [] for i in range(n)}\nfor i in range(n - 1):\n    g[i].append(i + 1)\n    g[i + 1].append(i)\nprint(count_components(g))\ng2 = {i: [] for i in range(n)}\nprint(count_components(g2))\n", "expected": ["2 0 1", "1", "200000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 15, 'graph-undirected-cycle', 2, 'func', 'Цикл в неориентированном графе', 'Напишите функцию has_cycle(graph): True, если в неориентированном графе (каждое ребро записано в обе стороны, петель и кратных рёбер нет) есть цикл. При обходе помните «родителя» вершины: возврат к нему циклом не считается.', 'def has_cycle(graph):
    pass
', 'DFS/BFS с (вершина, родитель): если сосед уже посещён и это не родитель — найден цикл.', '{"func": "has_cycle", "tests": [{"args": [{"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}], "expected": true}, {"args": [{"a": ["b"], "b": ["a", "c"], "c": ["b"]}], "expected": false}, {"args": [{}], "expected": false}, {"args": [{"a": [], "b": ["c"], "c": ["b", "d", "e"], "d": ["c", "e"], "e": ["c", "d"]}], "expected": true}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 15, 'graph-topological', 3, 'func', 'Топологическая сортировка', 'Напишите функцию topo_order(graph): graph — ориентированный граф без циклов, «вершина → список тех, на кого указывает». Верните порядок вершин, в котором каждая идёт раньше всех своих потомков; из нескольких допустимых берите лексикографически наименьший (в алгоритме Кана выбирайте наименьшую готовую вершину — куча). Если есть цикл — верните пустой список.', 'import heapq


def topo_order(graph):
    pass
', 'indegree каждой вершины; в куче — вершины с нулём; вынимайте, уменьшайте indegree соседей. Если выдали не все вершины — цикл.', '{"func": "topo_order", "tests": [{"args": [{"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}], "expected": ["a", "b", "c", "d"]}, {"args": [{"a": [], "b": ["a"], "c": ["a"]}], "expected": ["b", "c", "a"]}, {"args": [{"a": ["b"], "b": ["a"]}], "expected": []}, {"args": [{}], "expected": []}, {"args": [{"x": []}], "expected": ["x"]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 15, 'graph-bipartite', 4, 'func', 'Двудольный граф', 'Напишите функцию is_bipartite(graph): True, если вершины неориентированного графа можно раскрасить в два цвета так, чтобы концы каждого ребра были разного цвета. Граф может быть несвязным.', 'def is_bipartite(graph):
    pass
', 'Обход с раскраской: сосед получает противоположный цвет; если у уже покрашенного соседа тот же цвет — граф не двудольный.', '{"func": "is_bipartite", "tests": [{"args": [{"a": ["b", "d"], "b": ["a", "c"], "c": ["b", "d"], "d": ["a", "c"]}], "expected": true}, {"args": [{"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}], "expected": false}, {"args": [{}], "expected": true}, {"args": [{"a": [], "b": ["c"], "c": ["b"]}], "expected": true}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 15, 'grid-islands', 5, 'stdout', 'Количество островов', 'Напишите функцию count_islands(grid): grid — список строк из ''1'' (суша) и ''0'' (вода). Остров — группа клеток суши, соединённых по горизонтали и вертикали. Верните число островов. Проверка подаёт поле 1000×1000, поэтому без рекурсии.', 'def count_islands(grid):
    pass
', 'Для каждой клетки ''1'', которую ещё не видели, запустите обход (стек) по четырём направлениям и увеличьте счётчик.', '{"driver": "print(count_islands([''11000'', ''11000'', ''00100'', ''00011'']), count_islands([]), count_islands([''0'']), count_islands([''1'']))\nprint(count_islands([''101'', ''010'', ''101'']))\nbig = [''1'' * 1000 for _ in range(1000)]\nprint(count_islands(big))\nchess = [''''.join(''1'' if (i + j) % 2 == 0 else ''0'' for j in range(1000)) for i in range(1000)]\nprint(count_islands(chess))\n", "expected": ["3 0 0 1", "5", "1", "500000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 15, 'grid-shortest-path', 6, 'stdout', 'Кратчайший путь в лабиринте', 'Напишите функцию maze_steps(grid): grid — список строк из ''.'' (проход) и ''#'' (стена). Минимальное число шагов из левого верхнего угла в правый нижний (шаг — на соседнюю клетку по горизонтали или вертикали) либо -1. Поле до 501×501: нужен обход в ширину.', 'from collections import deque


def maze_steps(grid):
    pass
', 'Очередь клеток с расстоянием, список посещённых; соседей — только внутри поля и без стен.', '{"driver": "print(maze_steps([''..#'', ''#..'', ''#..'']), maze_steps([''.#'', ''#.'']), maze_steps([''.'']), maze_steps([''#.'']), maze_steps([]))\nn = 500\nopen_field = [''.'' * n for _ in range(n)]\nprint(maze_steps(open_field))\nn = 501\nsnake = []\nfor i in range(n):\n    row = [''.''] * n\n    if i % 2 == 1:\n        row = [''#''] * n\n        row[0 if i % 4 == 3 else n - 1] = ''.''\n    snake.append(''''.join(row))\nprint(maze_steps(snake))\n", "expected": ["4 -1 0 -1 -1", "998", "126000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 15, 'union-find-class', 7, 'stdout', 'Система непересекающихся множеств', 'Опишите класс UnionFind(n): элементы 0..n-1, поначалу каждый в своём множестве. Методы: find(x) — представитель множества, union(a, b) — объединить, connected(a, b) и атрибут count — число множеств. Нужны сжатие путей и объединение по размеру: проверка делает миллион операций.', 'class UnionFind:
    def __init__(self, n):
        pass
', 'parent[i] = i; find с сжатием путей (итеративно!); union по размеру; при слиянии count -= 1.', '{"driver": "u = UnionFind(6)\nu.union(0, 1)\nu.union(1, 2)\nu.union(4, 5)\nprint(u.connected(0, 2), u.connected(0, 4), u.count)\nu.union(2, 5)\nprint(u.connected(0, 4), u.count)\nn = 1000000\nbig = UnionFind(n)\nfor i in range(n - 1):\n    big.union(i, i + 1)\nprint(big.count, big.connected(0, n - 1))\n", "expected": ["True False 3", "True 2", "1 True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 16, 'dijkstra-dist', 0, 'stdout', 'Алгоритм Дейкстры', 'Напишите функцию dijkstra(graph, start): graph — словарь «вершина → {сосед: вес}» (веса неотрицательные), вершины — числа. Верните словарь «вершина → кратчайшее расстояние» для достижимых вершин. Нужна куча (heapq): проверка подаёт граф из 100 000 вершин и 300 000 рёбер.', 'import heapq


def dijkstra(graph, start):
    pass
', 'Куча пар (расстояние, вершина); при извлечении устаревшую запись (d > dist[v]) пропускайте; релаксация: dist[u] = dist[v] + w.', '{"driver": "g = {1: {2: 7, 3: 9, 6: 14}, 2: {1: 7, 3: 10, 4: 15}, 3: {1: 9, 2: 10, 4: 11, 6: 2}, 4: {2: 15, 3: 11, 5: 6}, 5: {4: 6, 6: 9}, 6: {1: 14, 3: 2, 5: 9}}\nprint(sorted(dijkstra(g, 1).items()))\nprint(dijkstra({1: {}}, 1), dijkstra({1: {2: 5}, 2: {}, 3: {}}, 1))\nimport random\nrandom.seed(4)\nn = 100000\nbig = {i: {} for i in range(n)}\nfor i in range(n - 1):\n    big[i][i + 1] = 1\nfor _ in range(200000):\n    a, b = random.randrange(n), random.randrange(n)\n    if a != b:\n        big[a][b] = random.randint(1, 50)\nd = dijkstra(big, 0)\nprint(len(d), d[n - 1] <= n - 1, d[0])\n", "expected": ["[(1, 0), (2, 7), (3, 9), (4, 20), (5, 20), (6, 11)]", "{1: 0} {1: 0, 2: 5}", "100000 True 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 16, 'shortest-path-route', 1, 'func', 'Сам маршрут', 'Напишите функцию shortest_route(graph, start, goal): graph — словарь «вершина → {сосед: вес}» (строковые вершины, веса положительные). Верните кортеж (длина, список вершин пути от start до goal) либо None, если пути нет. Кратчайший путь в тестах единственный.', 'import heapq


def shortest_route(graph, start, goal):
    pass
', 'В Дейкстре храните prev[u] = v при каждом улучшении расстояния; путь восстанавливайте от goal по prev.', '{"func": "shortest_route", "tests": [{"args": [{"a": {"b": 1, "c": 4}, "b": {"c": 2, "d": 6}, "c": {"d": 3}, "d": {}}, "a", "d"], "expected": {"__tuple__": [6, ["a", "b", "c", "d"]]}}, {"args": [{"a": {"b": 1}, "b": {}, "c": {}}, "a", "c"], "expected": null}, {"args": [{"a": {}}, "a", "a"], "expected": {"__tuple__": [0, ["a"]]}}, {"args": [{"a": {"b": 10, "c": 1}, "b": {}, "c": {"b": 1}}, "a", "b"], "expected": {"__tuple__": [2, ["a", "c", "b"]]}}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 16, 'bellman-ford-neg', 2, 'func', 'Беллман — Форд', 'Напишите функцию bellman_ford(n, edges, src): вершины 0..n-1, edges — список троек [u, v, вес] (веса могут быть отрицательными). Верните список расстояний от src (None для недостижимых вершин) либо строку «цикл», если из src достижим цикл отрицательного веса.', 'def bellman_ford(n, edges, src):
    pass
', 'n - 1 раз релаксируйте все рёбра; ещё один проход, который что-то улучшил, означает отрицательный цикл.', '{"func": "bellman_ford", "tests": [{"args": [5, [[0, 1, 6], [0, 2, 7], [1, 2, 8], [1, 3, 5], [1, 4, -4], [2, 3, -3], [2, 4, 9], [3, 1, -2], [4, 3, 7]], 0], "expected": [0, 2, 7, 4, -2]}, {"args": [3, [[0, 1, 1], [1, 2, -1], [2, 1, -1]], 0], "expected": "цикл"}, {"args": [3, [[1, 2, 5]], 0], "expected": [0, null, null]}, {"args": [1, [], 0], "expected": [0]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 16, 'floyd-warshall-matrix', 3, 'func', 'Все пары вершин', 'Напишите функцию all_pairs(n, edges): вершины 0..n-1, edges — тройки [u, v, вес] ориентированного графа (неотрицательные веса). Верните матрицу n×n кратчайших расстояний (алгоритм Флойда — Уоршелла); недостижимо — None, расстояние до себя — 0.', 'def all_pairs(n, edges):
    pass
', 'dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) для k, i, j в тройном цикле; бесконечность — float(''inf''), в конце заменить на None.', '{"func": "all_pairs", "tests": [{"args": [3, [[0, 1, 4], [1, 2, 1], [0, 2, 7]]], "expected": [[0, 4, 5], [null, 0, 1], [null, null, 0]]}, {"args": [1, []], "expected": [[0]]}, {"args": [2, []], "expected": [[0, null], [null, 0]]}, {"args": [3, [[0, 1, 1], [1, 0, 1], [1, 2, 2]]], "expected": [[0, 1, 3], [1, 0, 2], [null, null, 0]]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 16, 'kruskal-mst', 4, 'stdout', 'Минимальный остов: Краскал', 'Напишите функцию mst_weight(n, edges): вершины 0..n-1, edges — тройки (u, v, вес) неориентированного графа. Верните вес минимального остовного дерева, либо None, если граф несвязен. Алгоритм Краскала: сортировка рёбер и система непересекающихся множеств. Проверка — 200 000 рёбер.', 'def mst_weight(n, edges):
    pass
', 'Отсортируйте рёбра по весу; берите ребро, если его концы в разных множествах (union), и прибавляйте вес; в конце проверьте, что взято n - 1 ребро.', '{"driver": "print(mst_weight(4, [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 4), (1, 3, 5)]), mst_weight(3, [(0, 1, 5)]), mst_weight(1, []), mst_weight(2, [(0, 1, 7), (0, 1, 3)]))\nimport random\nrandom.seed(8)\nn = 50000\nedges = [(i, i + 1, 1) for i in range(n - 1)] + [(random.randrange(n), random.randrange(n), random.randint(2, 100)) for _ in range(200000)]\nprint(mst_weight(n, edges))\n", "expected": ["7 None 0 3", "49999"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 16, 'prim-mst', 5, 'func', 'Минимальный остов: Прим', 'Напишите функцию prim_weight(graph): graph — словарь «вершина → {сосед: вес}» связного неориентированного графа (рёбра записаны в обе стороны, вершины — строки). Верните вес минимального остова алгоритмом Прима с кучей. Пустой граф — 0.', 'import heapq


def prim_weight(graph):
    pass
', 'Начните с любой вершины; в куче — рёбра, ведущие из дерева наружу; вынимайте минимальное, и если конец ещё не в дереве — добавляйте.', '{"func": "prim_weight", "tests": [{"args": [{"a": {"b": 1, "c": 3}, "b": {"a": 1, "c": 2, "d": 5}, "c": {"a": 3, "b": 2, "d": 4}, "d": {"b": 5, "c": 4}}], "expected": 7}, {"args": [{}], "expected": 0}, {"args": [{"x": {}}], "expected": 0}, {"args": [{"a": {"b": 10}, "b": {"a": 10}}], "expected": 10}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 16, 'network-delay', 6, 'func', 'Время распространения сигнала', 'Сеть из узлов 1..n. times — список троек [u, v, w]: сигнал идёт от u к v за w. Сигнал отправляют из узла k. Напишите функцию network_delay(times, n, k): через сколько времени сигнал дойдёт до ВСЕХ узлов, либо -1, если дойдёт не до всех.', 'import heapq


def network_delay(times, n, k):
    pass
', 'Дейкстра от k; ответ — максимальное расстояние, если достигнуты все n узлов.', '{"func": "network_delay", "tests": [{"args": [[[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2], "expected": 2}, {"args": [[[1, 2, 1]], 2, 1], "expected": 1}, {"args": [[[1, 2, 1]], 2, 2], "expected": -1}, {"args": [[], 1, 1], "expected": 0}, {"args": [[[1, 2, 5], [1, 3, 1], [3, 2, 1]], 3, 1], "expected": 2}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 16, 'cheapest-flight-k-stops', 7, 'func', 'Дешёвый перелёт с ограничением пересадок', 'Напишите функцию cheapest_flight(n, flights, src, dst, k): города 0..n-1, flights — тройки [откуда, куда, цена]. Минимальная цена перелёта из src в dst с не более чем k пересадками (то есть не более k + 1 перелётов) либо -1. Подсказка: Беллман — Форд ровно на k + 1 итераций с копией расстояний на каждом шаге.', 'def cheapest_flight(n, flights, src, dst, k):
    pass
', 'dist = [inf] * n; dist[src] = 0; k + 1 раз: new = dist[:]; для каждого перелёта улучшайте new[v] по dist[u] + цена; dist = new.', '{"func": "cheapest_flight", "tests": [{"args": [4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1], "expected": 700}, {"args": [3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1], "expected": 200}, {"args": [3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0], "expected": 500}, {"args": [2, [], 0, 1, 5], "expected": -1}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'dsu-basic', 0, 'stdout', 'Система непересекающихся множеств', 'Напишите класс DSU: DSU(n) — n элементов, каждый в своей группе; find(x) — представитель группы; union(a, b) объединяет группы и возвращает True, если они были разными, иначе False; connected(a, b) — в одной ли группе; size(x) — размер группы x; count() — число групп. Используйте сжатие путей и объединение по размеру. Проверка подаёт цепочку union(i, i + 1) из двухсот тысяч элементов и двести тысяч запросов connected: без оптимизаций это квадрат.', 'class DSU:
    def __init__(self, n):
        pass

    def find(self, x):
        pass

    def union(self, a, b):
        pass

    def connected(self, a, b):
        pass

    def size(self, x):
        pass

    def count(self):
        pass
', 'p[x] — родитель; find поднимается до корня и перевешивает пройденных на корень; union подвешивает меньшее дерево под большее.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nd = DSU(6)\nprint(d.union(0, 1), d.union(1, 2), d.union(0, 2), d.connected(0, 2), d.connected(0, 5), d.size(1), d.count())\nn = 200000\nd = DSU(n)\nfor i in range(n - 1):\n    d.union(i, i + 1)\nprint(d.count(), d.size(0), d.connected(0, n - 1))\nok = 0\nfor _ in range(n):\n    ok += d.connected(0, n - 1)\nprint(ok)\nm = 1000000\nd = DSU(m)\nx = 12345\nfor _ in range(500000):\n    x = nxt(x)\n    a = x % m\n    x = nxt(x)\n    d.union(a, x % m)\nprint(d.count(), d.size(0) > 0)\n", "expected": ["True True False True False 3 4", "1 200000 True", "200000", "500001 True"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'dsu-components', 1, 'func', 'Число компонент связности', 'Напишите функцию count_components(n, edges): число компонент связности неориентированного графа из n вершин (0…n−1) и списка рёбер [a, b]. Каждое успешное объединение уменьшает число групп на один.', 'def count_components(n, edges):
    pass
', 'Начните с n групп; на каждом ребре, которое объединило разные группы, вычитайте единицу.', '{"func": "count_components", "tests": [{"args": [5, [[0, 1], [1, 2], [3, 4]]], "expected": 2}, {"args": [4, []], "expected": 4}, {"args": [1, []], "expected": 1}, {"args": [6, [[0, 1], [1, 0], [2, 3], [3, 4], [4, 2]]], "expected": 3}, {"args": [3, [[0, 1], [1, 2], [0, 2]]], "expected": 1}, {"args": [0, []], "expected": 0}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'dsu-cycle', 2, 'func', 'Есть ли цикл', 'Напишите функцию has_cycle(n, edges): True, если в неориентированном графе есть цикл (параллельные рёбра между одной парой вершин — тоже цикл; петля [a, a] — цикл).', 'def has_cycle(n, edges):
    pass
', 'Ребро, концы которого уже в одной группе, замыкает цикл.', '{"func": "has_cycle", "tests": [{"args": [4, [[0, 1], [1, 2], [2, 3]]], "expected": false}, {"args": [3, [[0, 1], [1, 2], [2, 0]]], "expected": true}, {"args": [2, [[0, 1], [1, 0]]], "expected": true}, {"args": [3, [[1, 1]]], "expected": true}, {"args": [5, []], "expected": false}, {"args": [6, [[0, 1], [2, 3], [4, 5], [1, 2], [3, 4]]], "expected": false}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'dsu-redundant', 3, 'func', 'Лишнее ребро', 'Напишите функцию redundant_edge(n, edges): первое по порядку ребро (в виде списка [a, b]), которое замыкает цикл — на момент его добавления концы уже в одной группе. Если циклов нет — пустой список.', 'def redundant_edge(n, edges):
    pass
', 'Обрабатывайте рёбра по порядку и верните первое, для которого union вернул False.', '{"func": "redundant_edge", "tests": [{"args": [4, [[0, 1], [1, 2], [2, 3], [3, 1]]], "expected": [3, 1]}, {"args": [3, [[0, 1], [1, 2]]], "expected": []}, {"args": [3, [[0, 1], [1, 2], [2, 0], [0, 1]]], "expected": [2, 0]}, {"args": [2, [[1, 0], [0, 1]]], "expected": [0, 1]}, {"args": [0, []], "expected": []}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'dsu-islands', 4, 'stdout', 'Количество островов', 'Напишите функцию count_islands(grid): grid — список строк из «1» (суша) и «0» (вода) одинаковой длины; остров — группа клеток суши, соседних по стороне (по горизонтали или вертикали). Верните число островов. Проверка подаёт карту, где один остров вьётся змейкой на сотни тысяч клеток: рекурсивный обход упрётся в лимит глубины — используйте систему непересекающихся множеств или обход со стеком.', 'def count_islands(grid):
    pass
', 'Для каждой клетки суши объедините её с правым и нижним соседом; в конце посчитайте различные корни.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nprint(count_islands([\"11000\", \"11000\", \"00100\", \"00011\"]), count_islands([]), count_islands([\"0\"]), count_islands([\"1\"]))\nw, h = 700, 700\ng = []\nx = 7\nfor r in range(h):\n    row = []\n    for c in range(w):\n        x = nxt(x)\n        row.append(\"1\" if x % 100 < 45 else \"0\")\n    g.append(\"\".join(row))\nprint(count_islands(g))\nw, h = 501, 501\nsnake = []\nfor r in range(h):\n    if r % 2 == 0:\n        snake.append(\"1\" * w)\n    elif r % 4 == 1:\n        snake.append(\"0\" * (w - 1) + \"1\")\n    else:\n        snake.append(\"1\" + \"0\" * (w - 1))\nprint(count_islands(snake))\n", "expected": ["3 0 0 1", "43116", "1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'dsu-kruskal', 5, 'func', 'Минимальный остов (Краскал)', 'Напишите функцию mst_weight(n, edges): вес минимального остовного дерева связного неориентированного графа; edges — список троек [a, b, вес]. Если граф несвязный — верните -1. Алгоритм Краскала: рёбра по возрастанию веса, берём те, что соединяют разные группы.', 'def mst_weight(n, edges):
    pass
', 'Отсортируйте рёбра по весу; каждое, для которого union вернул True, добавьте к сумме; в остове n − 1 ребро.', '{"func": "mst_weight", "tests": [{"args": [4, [[0, 1, 1], [1, 2, 2], [2, 3, 3], [0, 3, 10], [0, 2, 4]]], "expected": 6}, {"args": [3, [[0, 1, 5]]], "expected": -1}, {"args": [1, []], "expected": 0}, {"args": [4, [[0, 1, 2], [1, 2, 3], [2, 3, 1], [3, 0, 4], [0, 2, 5], [1, 3, 6]]], "expected": 6}, {"args": [2, [[0, 1, 7], [0, 1, 3]]], "expected": 3}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'dsu-equations', 6, 'func', 'Равенства и неравенства', 'Напишите функцию equations_possible(eqs): eqs — список строк вида «a==b» или «a!=b» (однобуквенные переменные). Верните True, если переменным можно подобрать значения, при которых выполняются все условия.', 'def equations_possible(eqs):
    pass
', 'Сначала объедините все равенства, затем проверьте, что ни одно неравенство не попало в одну группу.', '{"func": "equations_possible", "tests": [{"args": [["a==b", "b!=a"]], "expected": false}, {"args": [["a==b", "b==c", "a==c"]], "expected": true}, {"args": [["a==b", "b!=c", "c==a"]], "expected": false}, {"args": [["c==c", "b==d", "x!=z"]], "expected": true}, {"args": [["a!=a"]], "expected": false}, {"args": [[]], "expected": true}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'dsu-weighted', 7, 'stdout', 'Непересекающиеся множества с разностями', 'Напишите класс WeightedDSU: WeightedDSU(n) — n неизвестных; union(a, b, d) сообщает условие x[a] − x[b] = d и возвращает False, если оно противоречит уже известным (иначе True и запоминает); diff(a, b) возвращает x[a] − x[b], если эта разность выводится из условий, иначе None. Храните в каждом элементе смещение относительно родителя. Проверка — триста тысяч условий на двухстах тысячах неизвестных.', 'class WeightedDSU:
    def __init__(self, n):
        pass

    def union(self, a, b, d):
        pass

    def diff(self, a, b):
        pass
', 'Если корни совпали, сравните смещения; иначе подвесьте один корень под другой, подобрав смещение из условия.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nw = WeightedDSU(5)\nprint(w.union(0, 1, 3), w.union(1, 2, 4), w.diff(0, 2), w.diff(2, 0), w.diff(0, 3), w.union(0, 2, 7), w.union(0, 2, 8), w.union(3, 4, -1), w.union(4, 0, 2), w.diff(3, 1))\nn = 200000\nx = 5\nval = []\nfor _ in range(n):\n    x = nxt(x)\n    val.append(x % 1000)\nw = WeightedDSU(n)\nok = bad = 0\nfor q in range(300000):\n    x = nxt(x)\n    a = x % n\n    x = nxt(x)\n    b = x % n\n    if q % 7 == 6:\n        d = val[a] - val[b] + 1\n    else:\n        d = val[a] - val[b]\n    if w.union(a, b, d):\n        ok += 1\n    else:\n        bad += 1\nprint(ok, bad)\nx = 99\ntotal = 0\nknown = 0\nfor _ in range(100000):\n    x = nxt(x)\n    a = x % n\n    x = nxt(x)\n    r = w.diff(a, x % n)\n    if r is not None:\n        known += 1\n        total += r\nprint(known, total)\n", "expected": ["True True 7 -7 None True False True True 4", "202506 97494", "88578 -41710"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'dsu-offline', 8, 'stdout', 'Удаление рёбер: идём с конца', 'Напишите функцию components_after_removals(n, edges, order): из графа по очереди удаляют рёбра с номерами order[0], order[1], … (номера в списке edges, без повторов). Верните список res, где res[k] — число компонент связности после k + 1 удалений. Система непересекающихся множеств не умеет разделять, поэтому обрабатывайте удаления в обратном порядке как добавления. Проверка — двести тысяч рёбер и сто тысяч удалений.', 'def components_after_removals(n, edges, order):
    pass
', 'Постройте систему из рёбер, которые не удаляют; затем идите по order с конца: запишите число компонент и верните ребро в граф.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nprint(components_after_removals(4, [[0, 1], [1, 2], [2, 3], [0, 3]], [0, 3, 1]), components_after_removals(3, [], []))\nn = 200000\nx = 321\nedges = []\nfor _ in range(200000):\n    x = nxt(x)\n    a = x % n\n    x = nxt(x)\n    edges.append([a, x % n])\nidx = list(range(len(edges)))\nfor i in range(100000):\n    x = nxt(x)\n    j = i + x % (len(idx) - i)\n    idx[i], idx[j] = idx[j], idx[i]\nres = components_after_removals(n, edges, idx[:100000])\nprint(sum(res) % 1000003, res[0], res[-1])\n", "expected": ["[1, 2, 3] []", "100061 32334 100002"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'dsu-accounts', 9, 'func', 'Слияние аккаунтов', 'Напишите функцию merge_accounts(accounts): accounts — список [имя, почта1, почта2, …]. Два аккаунта — один человек, если у них есть общая почта (имена могут совпадать у разных людей). Верните список объединённых аккаунтов в виде [имя, почты по возрастанию…], отсортированный по самому списку.', 'def merge_accounts(accounts):
    pass
', 'Для каждой почты запомните первый аккаунт с ней; встретили снова — объедините аккаунты. Затем соберите почты по корням.', '{"func": "merge_accounts", "tests": [{"args": [[["Иван", "a@x", "b@x"], ["Иван", "c@x"], ["Иван", "b@x", "d@x"], ["Пётр", "a@x"]]], "expected": [["Иван", "a@x", "b@x", "d@x"], ["Иван", "c@x"]]}, {"args": [[["А", "1@m"]]], "expected": [["А", "1@m"]]}, {"args": [[]], "expected": []}, {"args": [[["А", "x@y", "z@y"], ["Б", "z@y"], ["А", "w@y"]]], "expected": [["А", "w@y"], ["Б", "x@y", "z@y"]]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'bt-subsets', 10, 'stdout', 'Все подмножества', 'Напишите функцию subsets(nums): список всех подмножеств списка различных чисел (каждое — список, элементы в порядке входа; порядок самих подмножеств не важен). Используйте шаблон «выбрать, исследовать, отменить» и не забывайте копировать текущий путь.', 'def subsets(nums):
    pass
', 'На каждом элементе два ветвления: не брать и взять; после возврата удалите взятый элемент (pop).', '{"driver": "print(sorted(sorted(s) for s in subsets([1, 2, 3])), subsets([]))\nbig = subsets(list(range(16)))\nprint(len(big), len({tuple(s) for s in big}), sum(len(s) for s in big))\n", "expected": ["[[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]] [[]]", "65536 65536 524288"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'bt-subsets-dups', 11, 'stdout', 'Подмножества с повторами', 'Напишите функцию subsets_unique(nums): все различные подмножества списка, в котором есть повторяющиеся числа (каждое подмножество — отсортированный список; порядок подмножеств не важен). Одинаковые подмножества в ответе повторяться не должны. Подсказка: отсортируйте вход и пропускайте число, равное предыдущему на этом уровне.', 'def subsets_unique(nums):
    pass
', 'Отсортируйте nums; в цикле по start: если i > start и nums[i] == nums[i − 1], пропустите.', '{"driver": "print(sorted(subsets_unique([2, 1, 2])), subsets_unique([]))\nr = subsets_unique([1] * 8 + [2] * 8 + [3] * 4)\nprint(len(r), len({tuple(sorted(s)) for s in r}))\n", "expected": ["[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]] [[]]", "405 405"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'bt-permutations', 12, 'stdout', 'Все перестановки', 'Напишите функцию permutations(nums): все перестановки списка различных чисел (список списков; порядок не важен). Помечайте использованные элементы массивом used и снимайте пометку при откате. Без itertools.', 'def permutations(nums):
    pass
', 'На каждом шаге цикл по индексам: если used[i], пропустите; иначе выберите, спуститесь, отмените.', '{"driver": "print(sorted(permutations([1, 2, 3])), permutations([]))\nr = permutations(list(range(8)))\nprint(len(r), len({tuple(p) for p in r}), sum(p[0] for p in r))\n", "expected": ["[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]] [[]]", "40320 40320 141120"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'bt-perm-dups', 13, 'stdout', 'Перестановки с повторами', 'Напишите функцию permutations_unique(nums): все различные перестановки списка с повторяющимися числами (порядок не важен, одинаковые перестановки не повторяются). Не генерируйте лишнее: проверка подаёт список из девяти чисел с повторами — 9! перестановок слишком много, различных намного меньше.', 'def permutations_unique(nums):
    pass
', 'Отсортируйте и пропускайте элемент, равный предыдущему, если предыдущий ещё не использован.', '{"driver": "print(sorted(permutations_unique([1, 1, 2])), permutations_unique([]))\nr = permutations_unique([1, 1, 2, 2, 3, 3, 4, 4, 5])\nprint(len(r), len({tuple(p) for p in r}))\nr = permutations_unique([1] * 7 + [2] * 6)\nprint(len(r))\n", "expected": ["[[1, 1, 2], [1, 2, 1], [2, 1, 1]] [[]]", "22680 22680", "1716"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'bt-combinations', 14, 'stdout', 'Сочетания', 'Напишите функцию combine(n, k): все сочетания по k чисел из 1…n (каждое — возрастающий список; порядок не важен). Отсекайте ветки, где оставшихся чисел не хватит на нужное количество.', 'def combine(n, k):
    pass
', 'go(start): берите v от start; если чисел от v до n не хватает до k — выходите из цикла досрочно.', '{"driver": "print(sorted(combine(4, 2)), combine(3, 0), combine(2, 3))\nr = combine(22, 11)\nprint(len(r), r[0], sum(c[0] for c in r))\n", "expected": ["[[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]] [[]] []", "705432 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11] 1352078"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'bt-combination-sum', 15, 'stdout', 'Сумма сочетаний с повторами', 'Напишите функцию combination_sum(candidates, target): все различные наборы чисел из candidates (различные положительные), в сумме дающие target; одно число можно брать сколько угодно раз. Каждый набор — неубывающий список; порядок наборов не важен. Отсортируйте числа и прерывайте цикл, когда число больше остатка.', 'def combination_sum(candidates, target):
    pass
', 'go(i, rest): для j от i: если nums[j] > rest — break; иначе берите число, вызывайте go(j, rest − nums[j]).', '{"driver": "print(sorted(combination_sum([2, 3, 6, 7], 7)), sorted(combination_sum([2, 3, 5], 8)), combination_sum([5], 3), combination_sum([1], 0))\nr = combination_sum([2, 3, 5, 7, 11, 13, 17, 19, 23, 29], 120)\nprint(len(r), max(len(c) for c in r), len({tuple(c) for c in r}))\n", "expected": ["[[2, 2, 3], [7]] [[2, 2, 2, 2], [2, 3, 3], [3, 5]] [] [[]]", "84685 60 84685"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'bt-n-queens', 16, 'stdout', 'Расстановка ферзей', 'Напишите функцию n_queens(n): сколько способов расставить n ферзей на доске n × n так, чтобы они не били друг друга. Ставьте по ферзю в каждую строку и проверяйте занятость столбцов и двух диагоналей за константу (множества или битовые маски). Проверка доходит до n = 11.', 'def n_queens(n):
    pass
', 'Диагонали: r − c и r + c постоянны на каждой; храните занятые в множествах и снимайте при откате.', '{"driver": "print([n_queens(n) for n in range(1, 10)])\nprint(n_queens(10), n_queens(11))\n", "expected": ["[1, 0, 0, 2, 10, 4, 40, 92, 352]", "724 2680"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'bt-sudoku', 17, 'stdout', 'Судоку', 'Напишите функцию solve_sudoku(rows): rows — девять строк по девять символов, цифры «1»–«9» и «.» для пустой клетки; решение единственное. Верните девять строк решённой доски или None, если решить нельзя. Проверка включает головоломку, на которой перебор клеток подряд работает минуты: выбирайте клетку с наименьшим числом вариантов и храните занятые цифры в строках, столбцах и блоках масками.', 'def solve_sudoku(rows):
    pass
', 'Выбирайте клетку с минимумом кандидатов (ноль — тупик, откат); кандидаты — это ~(строка | столбец | блок) & 0b1111111110.', '{"driver": "def rows(s):\n    return [s[i * 9:(i + 1) * 9] for i in range(9)]\nfor puzzle in (''53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79'', ''..............3.85..1.2.......5.7.....4...1...9.......5......73..2.1........4...9''):\n    ans = solve_sudoku(rows(puzzle))\n    ok = all(sorted(r) == list(\"123456789\") for r in ans) and all(sorted(ans[r][c] for r in range(9)) == list(\"123456789\") for c in range(9))\n    ok = ok and all(sorted(ans[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)) == list(\"123456789\") for br in (0, 3, 6) for bc in (0, 3, 6))\n    ok = ok and all(p == \".\" or p == ans[i // 9][i % 9] for i, p in enumerate(puzzle))\n    print(ok, ans[0], ans[8])\nprint(solve_sudoku(rows(\"12345678.\" + \"........9\" + \".\" * 63)))\n", "expected": ["True 534678912 345286179", "True 987654321 863745219", "None"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'bt-word-search', 18, 'func', 'Слово на сетке', 'Напишите функцию exist(board, word): board — список строк-рядов; можно ли составить слово word, идя по соседним по стороне клеткам, не используя одну клетку дважды? Пустое слово — True. Отмечайте клетку посещённой перед спуском и снимайте отметку при возврате.', 'def exist(board, word):
    pass
', 'go(r, c, i): клетка должна совпасть с word[i]; пометьте её, попробуйте четыре соседа, снимите пометку.', '{"func": "exist", "tests": [{"args": [["ABCE", "SFCS", "ADEE"], "ABCCED"], "expected": true}, {"args": [["ABCE", "SFCS", "ADEE"], "SEE"], "expected": true}, {"args": [["ABCE", "SFCS", "ADEE"], "ABCB"], "expected": false}, {"args": [["a"], "a"], "expected": true}, {"args": [["a"], "b"], "expected": false}, {"args": [["aa"], "aaa"], "expected": false}, {"args": [["ab", "cd"], "acdb"], "expected": true}, {"args": [["ABCE", "SFCS", "ADEE"], ""], "expected": true}, {"args": [["ABCD", "EFGH"], "AFGD"], "expected": false}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 17, 'bt-meet-in-middle', 19, 'stdout', 'Встреча посередине', 'Напишите функцию count_subsets_sum(nums, target): сколько подмножеств (по позициям, то есть одинаковые числа на разных местах — разные подмножества, пустое тоже считается) списка nums имеют сумму target. В списке до 36 чисел: перебор 2³⁶ подмножеств не уложится. Разделите список пополам, переберите суммы каждой половины (2¹⁸ штук) и соедините их через словарь счётчиков.', 'def count_subsets_sum(nums, target):
    pass
', 'Суммы половины строят удвоением: sums += [s + v for s in sums]; затем для каждой суммы левой половины ищите target − s в словаре правой.', '{"driver": "def nxt(x):\n    x ^= (x << 13) & 0xFFFFFFFF\n    x ^= x >> 17\n    x ^= (x << 5) & 0xFFFFFFFF\n    return x\nprint(count_subsets_sum([1, 2, 3], 3), count_subsets_sum([], 0), count_subsets_sum([0, 0], 0), count_subsets_sum([5], 3))\nx = 202\nnums = []\nfor _ in range(36):\n    x = nxt(x)\n    nums.append(x % 1000)\nprint(count_subsets_sum(nums, sum(nums) // 2), count_subsets_sum(nums, 1234), count_subsets_sum(nums, -1))\nnums = [1] * 20 + [2] * 16\nprint(count_subsets_sum(nums, 18))\n", "expected": ["2 1 4 0", "13046942 16 0", "1330038610"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 18, 'dp-climb-stairs', 0, 'stdout', 'Лестница', 'Напишите функцию climb(n): сколькими способами можно подняться на n-ю ступень, делая шаги по 1 или по 2 ступени. Наивная рекурсия делает экспоненциально много вызовов: проверка подаёт n = 5000 (ответ огромный, Python справится).', 'def climb(n):
    pass
', 'ways[i] = ways[i - 1] + ways[i - 2] — это числа Фибоначчи; храните только две последние.', '{"driver": "print(climb(1), climb(2), climb(5), climb(45))\nprint(climb(5000) % 1000000007)\n", "expected": ["1 2 8 1836311903", "419609281"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 18, 'dp-coin-change', 1, 'stdout', 'Размен монет', 'Напишите функцию min_coins(coins, amount): наименьшее число монет номиналов coins (каждого номинала — сколько угодно), дающих сумму amount; если набрать нельзя — -1; для суммы 0 — 0. Динамическое программирование по сумме: проверка подаёт сумму 100 000.', 'def min_coins(coins, amount):
    pass
', 'best[0] = 0; best[a] = min(best[a - c] + 1 для монет c <= a); бесконечность — «набрать нельзя».', '{"driver": "print(min_coins([1, 2, 5], 11), min_coins([2], 3), min_coins([1], 0), min_coins([186, 419, 83, 408], 6249), min_coins([], 5))\nprint(min_coins([1, 5, 10, 25], 100000), min_coins([7, 13], 100000))\n", "expected": ["3 -1 0 20 -1", "4000 7696"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 18, 'dp-knapsack-01', 2, 'stdout', 'Рюкзак 0/1', 'Напишите функцию knapsack(weights, values, capacity): наибольшая суммарная ценность предметов, которые влезают в рюкзак (каждый предмет — один раз). Таблица по вместимости, O(n · capacity) времени и O(capacity) памяти: проверка подаёт 100 предметов и вместимость 10 000.', 'def knapsack(weights, values, capacity):
    pass
', 'dp = [0] * (capacity + 1); для каждого предмета идите по вместимости ОТ БОЛЬШЕЙ К МЕНЬШЕЙ: dp[c] = max(dp[c], dp[c - w] + v).', '{"driver": "print(knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7), knapsack([], [], 10), knapsack([5], [10], 4), knapsack([2, 2], [3, 4], 4))\nimport random\nrandom.seed(9)\nw = [random.randint(10, 400) for _ in range(100)]\nv = [random.randint(1, 1000) for _ in range(100)]\nprint(knapsack(w, v, 10000), knapsack(w, v, 1000))\n", "expected": ["9 0 0 7", "41394 13942"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 18, 'dp-lcs', 3, 'stdout', 'Наибольшая общая подпоследовательность', 'Напишите функцию lcs_length(a, b): длина наибольшей общей подпоследовательности двух строк (символы идут в том же порядке, но не обязательно подряд). Таблица динамического программирования: проверка подаёт строки по 2000 символов.', 'def lcs_length(a, b):
    pass
', 'dp[i][j]: если a[i-1] == b[j-1] — dp[i-1][j-1] + 1, иначе max(dp[i-1][j], dp[i][j-1]); хватит двух строк таблицы.', '{"driver": "print(lcs_length(''abcde'', ''ace''), lcs_length(''abc'', ''def''), lcs_length('''', ''x''), lcs_length(''привет'', ''превет''))\nimport random\nrandom.seed(6)\nx = ''''.join(random.choice(''abcd'') for _ in range(2000))\ny = ''''.join(random.choice(''abcd'') for _ in range(2000))\nprint(lcs_length(x, x), lcs_length(x, y))\n", "expected": ["3 0 0 5", "2000 1301"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 18, 'dp-edit-distance', 4, 'stdout', 'Расстояние редактирования', 'Напишите функцию edit_distance(a, b): минимальное число операций (вставка, удаление или замена одного символа), превращающих строку a в b (расстояние Левенштейна). Проверка подаёт строки по 1500 символов.', 'def edit_distance(a, b):
    pass
', 'dp[i][j] = min(удаление: dp[i-1][j] + 1, вставка: dp[i][j-1] + 1, замена: dp[i-1][j-1] + (a[i-1] != b[j-1])).', '{"driver": "print(edit_distance(''kitten'', ''sitting''), edit_distance('''', ''abc''), edit_distance(''abc'', ''''), edit_distance(''abc'', ''abc''), edit_distance(''кот'', ''код''))\nimport random\nrandom.seed(2)\nx = ''''.join(random.choice(''abc'') for _ in range(1500))\ny = x[:700] + ''zz'' + x[702:]\nprint(edit_distance(x, y), edit_distance(x, x))\n", "expected": ["3 3 3 0 1", "2 0"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 18, 'dp-lis-nlogn', 5, 'stdout', 'Самая длинная возрастающая подпоследовательность', 'Напишите функцию lis_length(nums): длина самой длинной строго возрастающей подпоследовательности. Решение за O(n log n) (список «хвостов» и бинарный поиск bisect): проверка подаёт 100 000 чисел, а O(n²) не успеет.', 'import bisect


def lis_length(nums):
    pass
', 'tails[k] — наименьший возможный хвост возрастающей подпоследовательности длины k + 1; для x найдите bisect_left(tails, x) и замените или допишите.', '{"driver": "print(lis_length([10, 9, 2, 5, 3, 7, 101, 18]), lis_length([]), lis_length([7, 7, 7]), lis_length([1, 2, 3, 4]))\nimport random\nrandom.seed(1)\nbig = [random.randint(0, 10 ** 9) for _ in range(100000)]\nprint(lis_length(big))\nprint(lis_length(list(range(100000))), lis_length(list(range(100000, 0, -1))))\n", "expected": ["4 0 1 4", "627", "100000 1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 18, 'dp-house-robber', 6, 'stdout', 'Грабитель домов', 'Напишите функцию rob(money): наибольшая сумма, которую можно собрать из домов на улице, не заходя в два соседних (money[i] — деньги в i-м доме, все неотрицательные). Достаточно двух переменных: проверка подаёт миллион домов.', 'def rob(money):
    pass
', 'take, skip = 0, 0; для x: take, skip = skip + x, max(take, skip).', '{"driver": "print(rob([1, 2, 3, 1]), rob([2, 7, 9, 3, 1]), rob([]), rob([5]), rob([2, 1, 1, 2]))\nprint(rob([3] * 1000000), rob(list(range(1000000))))\n", "expected": ["4 12 0 5 4", "1500000 250000000000"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 18, 'dp-partition-subset', 7, 'stdout', 'Разбиение на две равные суммы', 'Напишите функцию can_split(nums): True, если числа списка (натуральные) можно разделить на две группы с равной суммой. Задача о подмножестве с суммой total/2: множество достижимых сумм. Проверка: 200 чисел, суммы до 20 000.', 'def can_split(nums):
    pass
', 'total нечётное → False; иначе reachable = {0}; для каждого x: добавляйте s + x, не превышая total // 2 — или битовая маска bits |= bits << x.', '{"driver": "print(can_split([1, 5, 11, 5]), can_split([1, 2, 3, 5]), can_split([]), can_split([2, 2]), can_split([7]))\nimport random\nrandom.seed(12)\nnums = [random.randint(1, 200) for _ in range(200)]\nif sum(nums) % 2:\n    nums[0] += 1\nprint(can_split(nums))\nprint(can_split([1000] * 19 + [999]))\n", "expected": ["True False True True False", "True", "False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 19, 'greedy-interval-scheduling', 0, 'func', 'Выбор максимума непересекающихся встреч', 'Напишите функцию max_meetings(intervals): intervals — список пар [начало, конец]. Верните наибольшее число встреч, которые можно провести, если две встречи не должны пересекаться (встреча, заканчивающаяся в момент t, не мешает той, что начинается в t). Жадный выбор: по самому раннему окончанию.', 'def max_meetings(intervals):
    pass
', 'Отсортируйте по концу; берите встречу, если её начало >= конца последней выбранной.', '{"func": "max_meetings", "tests": [{"args": [[[1, 3], [2, 4], [3, 5], [0, 6], [5, 7], [8, 9], [5, 9]]], "expected": 4}, {"args": [[]], "expected": 0}, {"args": [[[1, 2], [1, 2], [1, 2]]], "expected": 1}, {"args": [[[1, 10], [2, 3], [4, 5], [6, 7]]], "expected": 3}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 19, 'greedy-merge-intervals', 1, 'func', 'Слияние отрезков', 'Напишите функцию merge_intervals(intervals): объедините пересекающиеся и касающиеся отрезки [начало, конец] и верните результат, отсортированный по началу.', 'def merge_intervals(intervals):
    pass
', 'Сортировка по началу; текущий отрезок продлевайте, пока следующий начинается не позже его конца.', '{"func": "merge_intervals", "tests": [{"args": [[[1, 3], [2, 6], [8, 10], [15, 18]]], "expected": [[1, 6], [8, 10], [15, 18]]}, {"args": [[[1, 4], [4, 5]]], "expected": [[1, 5]]}, {"args": [[]], "expected": []}, {"args": [[[5, 6], [1, 10], [2, 3]]], "expected": [[1, 10]]}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 19, 'greedy-jump-game', 2, 'stdout', 'Прыжки по массиву', 'Напишите функцию can_reach(jumps): на i-й позиции можно прыгнуть вперёд на любое число клеток от 0 до jumps[i]. Можно ли добраться из первой клетки до последней? Жадно: следите за самой дальней достижимой клеткой. Проверка — миллион клеток.', 'def can_reach(jumps):
    pass
', 'far = 0; для i: если i > far — тупик (False); far = max(far, i + jumps[i]); достигли last — True.', '{"driver": "print(can_reach([2, 3, 1, 1, 4]), can_reach([3, 2, 1, 0, 4]), can_reach([0]), can_reach([1, 0]), can_reach([0, 1]))\nprint(can_reach([1] * 1000000), can_reach([1] * 999999 + [0]), can_reach([1] * 500000 + [0] + [1] * 499999))\n", "expected": ["True False True True False", "True True False"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 19, 'greedy-min-jumps', 3, 'stdout', 'Минимум прыжков', 'Напишите функцию min_jumps(jumps): наименьшее число прыжков из первой клетки в последнюю (на i-й клетке — прыжок на 0..jumps[i]); до конца гарантированно можно добраться. Жадно, за один проход: проверка подаёт миллион клеток.', 'def min_jumps(jumps):
    pass
', 'Границы «текущего прыжка»: end — предел текущего шага, far — самая дальняя достижимая; дошли до end — делаем прыжок, end = far.', '{"driver": "print(min_jumps([2, 3, 1, 1, 4]), min_jumps([2, 3, 0, 1, 4]), min_jumps([0]), min_jumps([1, 1, 1, 1]))\nprint(min_jumps([1000] * 1000), min_jumps([1] * 1000000), min_jumps([5] + [1] * 5))\n", "expected": ["2 2 0 3", "1 999999 1"]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 19, 'greedy-gas-station', 4, 'func', 'Заправки по кругу', 'По кольцевой дороге стоят заправки: gas[i] — сколько топлива на i-й, cost[i] — сколько его тратится на переезд до следующей. Напишите функцию start_station(gas, cost): индекс заправки, с которой можно начать (с пустым баком) и объехать круг, либо -1. Такой индекс единственный. Один проход.', 'def start_station(gas, cost):
    pass
', 'Если суммарно топлива меньше расхода — -1. Иначе идите по кругу: когда баланс стал отрицательным, начало — со следующей заправки.', '{"func": "start_station", "tests": [{"args": [[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]], "expected": 3}, {"args": [[2, 3, 4], [3, 4, 3]], "expected": -1}, {"args": [[5], [4]], "expected": 0}, {"args": [[5, 1, 2, 3, 4], [4, 4, 1, 5, 1]], "expected": 4}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 19, 'greedy-fractional-knapsack', 5, 'func', 'Непрерывный рюкзак', 'Предметы можно дробить. Напишите функцию fractional_knapsack(items, capacity): items — пары [вес, ценность]. Верните наибольшую ценность, округлённую до двух знаков (round). Жадно: сначала предметы с наибольшей ценностью на единицу веса.', 'def fractional_knapsack(items, capacity):
    pass
', 'Отсортируйте по ценность/вес по убыванию; берите целиком, пока влезает, последний — долей.', '{"func": "fractional_knapsack", "tests": [{"args": [[[10, 60], [20, 100], [30, 120]], 50], "expected": 240.0}, {"args": [[[5, 50]], 2], "expected": 20.0}, {"args": [[], 10], "expected": 0.0}, {"args": [[[1, 1], [2, 5]], 10], "expected": 6.0}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 19, 'greedy-huffman-cost', 6, 'func', 'Стоимость кода Хаффмана', 'Напишите функцию huffman_cost(freqs): freqs — частоты символов. Верните суммарную стоимость оптимального префиксного кода: сумму длин кодов, взвешенную частотами (равна сумме всех слияний в алгоритме Хаффмана). Каждый шаг: берём две наименьшие частоты (куча), заменяем их суммой. Для одного символа — 0.', 'import heapq


def huffman_cost(freqs):
    pass
', 'heap = freqs; пока в куче больше одного: a, b = два наименьших; cost += a + b; вернуть a + b.', '{"func": "huffman_cost", "tests": [{"args": [[5, 9, 12, 13, 16, 45]], "expected": 224}, {"args": [[1, 1]], "expected": 2}, {"args": [[7]], "expected": 0}, {"args": [[]], "expected": 0}, {"args": [[1, 2, 3, 4]], "expected": 19}]}');
INSERT INTO tasks (book_id, chapter, id, ord, mode, title, statement, starter, hint, spec) VALUES (7, 19, 'greedy-min-platforms', 7, 'stdout', 'Минимум платформ', 'Напишите функцию min_platforms(arrivals, departures): сколько платформ нужно вокзалу, чтобы ни один поезд не ждал. Поезд i стоит с arrivals[i] до departures[i] (если один уезжает, когда другой приезжает, платформа освобождается). Отсортируйте события и идите двумя указателями. Проверка — 200 000 поездов.', 'def min_platforms(arrivals, departures):
    pass
', 'Отсортируйте обе последовательности; i, j: если arrivals[i] < departures[j] — нужна новая платформа (i += 1), иначе поезд уехал (j += 1); следите за максимумом.', '{"driver": "print(min_platforms([900, 940, 950, 1100, 1500, 1800], [910, 1200, 1120, 1130, 1900, 2000]), min_platforms([], []), min_platforms([1], [2]), min_platforms([1, 2], [2, 3]))\nn = 200000\nprint(min_platforms(list(range(n)), [i + 5 for i in range(n)]), min_platforms(list(range(n)), [i + 1 for i in range(n)]))\n", "expected": ["3 0 1 1", "5 1"]}');
