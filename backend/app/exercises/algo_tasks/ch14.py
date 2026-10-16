"""Задачи книги «Алгоритмы и структуры данных»: глава 14."""

TASKS: dict[int, list[dict]] = {
    14: [
        {'id': 'seg-range-sums',
         'mode': 'func',
         'func': 'range_sums',
         'title': 'Суммы на отрезках: префиксные суммы',
         'statement': 'Напишите функцию range_sums(a, queries): queries — список пар [l, r] (индексы с '
                      'нуля, обе границы включены); верните список сумм a[l] + … + a[r]. Постройте '
                      'префиксные суммы один раз, каждый запрос — за константу.',
         'starter': 'def range_sums(a, queries):\n    pass\n',
         'tests': [{'args': [[3, 1, 4, 1, 5, 9, 2, 6], [[2, 5], [0, 7], [3, 3]]], 'expected': [19, 31, 1]},
                   {'args': [[-2, 5, -1], [[0, 2], [1, 1]]], 'expected': [2, 5]},
                   {'args': [[7], [[0, 0]]], 'expected': [7]},
                   {'args': [[1, 2, 3], []], 'expected': []}],
         'hint': 'p[i + 1] = p[i] + a[i]; сумма на [l, r] равна p[r + 1] − p[l].'},
        {'id': 'seg-fenwick-range',
         'mode': 'func',
         'func': 'fenwick_range',
         'title': 'Какой отрезок хранит ячейка Фенвика',
         'statement': 'В дереве Фенвика элементы нумеруются с единицы, а ячейка i хранит сумму отрезка '
                      'длины i & −i, заканчивающегося в i. Напишите функцию fenwick_range(i): кортеж (l, '
                      'r) — границы этого отрезка. Например, fenwick_range(12) = (9, 12).',
         'starter': 'def fenwick_range(i):\n    pass\n',
         'tests': [{'args': [12], 'expected': (9, 12)},
                   {'args': [8], 'expected': (1, 8)},
                   {'args': [7], 'expected': (7, 7)},
                   {'args': [6], 'expected': (5, 6)},
                   {'args': [1], 'expected': (1, 1)},
                   {'args': [10], 'expected': (9, 10)},
                   {'args': [1024], 'expected': (1, 1024)},
                   {'args': [1000], 'expected': (993, 1000)}],
         'hint': 'Длина отрезка — i & −i; он заканчивается в i.'},
        {'id': 'seg-prefix-path',
         'mode': 'func',
         'func': 'prefix_path',
         'title': 'Путь запроса префикса',
         'statement': 'Напишите функцию prefix_path(i): список ячеек дерева Фенвика, которые складываются '
                      'при запросе суммы первых i элементов, в порядке посещения. Начните с i и на каждом '
                      'шаге убирайте младший бит; для 11 — [11, 10, 8], для 0 — пустой список.',
         'starter': 'def prefix_path(i):\n    pass\n',
         'tests': [{'args': [11], 'expected': [11, 10, 8]},
                   {'args': [7], 'expected': [7, 6, 4]},
                   {'args': [8], 'expected': [8]},
                   {'args': [0], 'expected': []},
                   {'args': [1], 'expected': [1]},
                   {'args': [1023], 'expected': [1023, 1022, 1020, 1016, 1008, 992, 960, 896, 768, 512]},
                   {'args': [12], 'expected': [12, 8]}],
         'hint': 'Цикл: пока i > 0, записываем i и вычитаем i & −i.'},
        {'id': 'seg-update-path',
         'mode': 'func',
         'func': 'update_path',
         'title': 'Путь изменения',
         'statement': 'Напишите функцию update_path(i, n): список ячеек дерева Фенвика размера n, которые '
                      'меняются при изменении элемента i, в порядке посещения. Начните с i и прибавляйте '
                      'младший бит, пока не выйдете за n; update_path(3, 8) = [3, 4, 8].',
         'starter': 'def update_path(i, n):\n    pass\n',
         'tests': [{'args': [3, 8], 'expected': [3, 4, 8]},
                   {'args': [8, 8], 'expected': [8]},
                   {'args': [5, 12], 'expected': [5, 6, 8]},
                   {'args': [1, 16], 'expected': [1, 2, 4, 8, 16]},
                   {'args': [7, 7], 'expected': [7]},
                   {'args': [6, 100], 'expected': [6, 8, 16, 32, 64]},
                   {'args': [9, 8], 'expected': []}],
         'hint': 'Цикл: пока i ≤ n, записываем i и прибавляем i & −i.'},
        {'id': 'seg-fenwick',
         'mode': 'stdout',
         'title': 'Дерево Фенвика',
         'statement': 'Напишите класс Fenwick: конструктор Fenwick(n) создаёт нулевой массив из n '
                      'элементов (индексы с 1); add(i, delta) прибавляет delta к элементу i; prefix(i) — '
                      'сумма первых i элементов (prefix(0) = 0); range_sum(l, r) — сумма элементов с l по '
                      'r включительно. Всё за O(log n): проверка выполняет двести тысяч операций над '
                      'массивом из двухсот тысяч элементов.',
         'starter': 'class Fenwick:\n'
                    '    def __init__(self, n):\n'
                    '        pass\n'
                    '\n'
                    '    def add(self, i, delta):\n'
                    '        pass\n'
                    '\n'
                    '    def prefix(self, i):\n'
                    '        pass\n'
                    '\n'
                    '    def range_sum(self, l, r):\n'
                    '        pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'f = Fenwick(8)\n'
                   'for i, v in enumerate([2, 5, 1, 4, 3, 6, 2, 7], 1):\n'
                   '    f.add(i, v)\n'
                   'print(f.prefix(7), f.range_sum(3, 6), f.prefix(0), f.range_sum(1, 8))\n'
                   'f.add(3, 5)\n'
                   'print(f.prefix(3), f.range_sum(3, 3))\n'
                   'n = 200000\n'
                   'f = Fenwick(n)\n'
                   'x = 5\n'
                   'total = 0\n'
                   'for q in range(200000):\n'
                   '    x = nxt(x)\n'
                   '    i = 1 + x % n\n'
                   '    x = nxt(x)\n'
                   '    if q % 3 == 0:\n'
                   '        f.add(i, x % 1000 - 500)\n'
                   '    elif q % 3 == 1:\n'
                   '        total += f.prefix(i)\n'
                   '    else:\n'
                   '        j = 1 + x % n\n'
                   '        total += f.range_sum(min(i, j), max(i, j))\n'
                   'print(total, f.prefix(n))\n',
         'expected': ['23 14 0 30', '13 6', '-1754336517 -55366'],
         'hint': 'Ячейка i хранит сумму отрезка длины i & −i: add идёт вверх (i += i & −i), prefix — вниз '
                 '(i −= i & −i).'},
        {'id': 'seg-fenwick-build',
         'mode': 'stdout',
         'title': 'Построение Фенвика за линейное время',
         'statement': 'Напишите функцию build_fenwick(a): список tree длины n + 1 (tree[0] = 0), в котором '
                      'tree[i] — сумма a[i − (i & −i)] … a[i − 1] (то есть отрезка длины i & −i, '
                      'заканчивающегося на i-м элементе при нумерации с единицы). Время — O(n): n '
                      'последовательных вызовов add дали бы n log n; проверка использует два с половиной '
                      'миллиона чисел.',
         'starter': 'def build_fenwick(a):\n    pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'print(build_fenwick([2, 5, 1, 4, 3, 6, 2, 7]))\n'
                   'def brute(a):\n'
                   '    t = [0] * (len(a) + 1)\n'
                   '    for i in range(1, len(a) + 1):\n'
                   '        t[i] = sum(a[i - (i & -i): i])\n'
                   '    return t\n'
                   'y = 3\n'
                   'b = []\n'
                   'for _ in range(1000):\n'
                   '    y = nxt(y)\n'
                   '    b.append(y % 100 - 50)\n'
                   'print(build_fenwick(b) == brute(b), build_fenwick([]) == [0])\n'
                   'N = 2500000\n'
                   'big = []\n'
                   'for _ in range(N):\n'
                   '    y = nxt(y)\n'
                   '    big.append(y & 1023)\n'
                   't = build_fenwick(big)\n'
                   'print(len(t), t[N], t[2 ** 21], sum(t) % 1000003)\n',
         'expected': ['[0, 2, 7, 1, 12, 3, 9, 2, 30]', 'True True', '2500001 17168 1072520550 158394'],
         'hint': 'Положите a в tree[1..n], затем для каждого i прибавьте tree[i] к родителю i + (i & −i), '
                 'если он не вышел за n.'},
        {'id': 'seg-inversions',
         'mode': 'stdout',
         'title': 'Подсчёт инверсий',
         'statement': 'Напишите функцию count_inversions(a): число пар i < j, для которых a[i] > a[j]. '
                      'Проверка подаёт двести тысяч чисел — квадратичный перебор не успеет. Подумайте о '
                      'дереве Фенвика по сжатым значениям или о сортировке слиянием.',
         'starter': 'def count_inversions(a):\n    pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'print(count_inversions([2, 4, 1, 3, 5]), count_inversions([]), count_inversions([3, 2, '
                   '1]), count_inversions([1, 1, 1]))\n'
                   'n = 200000\n'
                   'x = 3\n'
                   'a = []\n'
                   'for _ in range(n):\n'
                   '    x = nxt(x)\n'
                   '    a.append(x % 1000000)\n'
                   'print(count_inversions(a))\n'
                   'print(count_inversions(list(range(n, 0, -1))))\n',
         'expected': ['3 0 3 0', '10012382156', '19999900000'],
         'hint': 'Идите слева направо: сколько уже встречённых элементов больше текущего — это (число '
                 'встреченных) − (число ≤ текущего).'},
        {'id': 'seg-range-add',
         'mode': 'stdout',
         'title': 'Прибавление на отрезке, значение в точке',
         'statement': 'Напишите класс RangeAdd: RangeAdd(n) — массив из n нулей (индексы с нуля); add(l, '
                      'r, v) прибавляет v ко всем элементам с l по r включительно; get(i) возвращает '
                      'значение i-го элемента. Оба — за O(log n): храните разности в дереве Фенвика. '
                      'Проверка — двести тысяч операций.',
         'starter': 'class RangeAdd:\n'
                    '    def __init__(self, n):\n'
                    '        pass\n'
                    '\n'
                    '    def add(self, l, r, v):\n'
                    '        pass\n'
                    '\n'
                    '    def get(self, i):\n'
                    '        pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   't = RangeAdd(6)\n'
                   't.add(1, 3, 5)\n'
                   't.add(0, 5, 1)\n'
                   'print([t.get(i) for i in range(6)])\n'
                   'n = 200000\n'
                   't = RangeAdd(n)\n'
                   'x = 9\n'
                   'total = 0\n'
                   'for q in range(200000):\n'
                   '    x = nxt(x)\n'
                   '    l = x % n\n'
                   '    x = nxt(x)\n'
                   '    r = l + x % (n - l)\n'
                   '    x = nxt(x)\n'
                   '    if q % 2:\n'
                   '        t.add(l, r, x % 100 - 50)\n'
                   '    else:\n'
                   '        total += t.get(l) + t.get(r)\n'
                   'print(total, t.get(0), t.get(n - 1))\n',
         'expected': ['[1, 6, 6, 6, 1, 1]', '-1353428639 0 33'],
         'hint': 'add(l, r, v) — это два точечных изменения разностей: +v в позиции l и −v в позиции r + '
                 '1; get — префиксная сумма разностей.'},
        {'id': 'seg-order-set',
         'mode': 'stdout',
         'title': 'k-е по величине через спуск по Фенвику',
         'statement': 'Напишите класс OrderSet: OrderSet(maxv) — пустой набор значений от 1 до maxv '
                      '(повторы допустимы); add(x) добавляет x; discard(x) удаляет одно вхождение x (оно '
                      'точно есть); kth(k) — k-е по возрастанию значение (k с единицы). Всё за O(log '
                      'maxv): храните счётчики в дереве Фенвика и спускайтесь по битам. Запрещены bisect, '
                      'heapq, sorted и методы insert, remove, pop, sort, index, count.',
         'starter': 'class OrderSet:\n'
                    '    def __init__(self, maxv):\n'
                    '        pass\n'
                    '\n'
                    '    def add(self, x):\n'
                    '        pass\n'
                    '\n'
                    '    def discard(self, x):\n'
                    '        pass\n'
                    '\n'
                    '    def kth(self, k):\n'
                    '        pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'import ast as _ast\n'
                   '_src = open("/sandbox/solution.py", encoding="utf-8").read()\n'
                   '_bad = set()\n'
                   'for _n in _ast.walk(_ast.parse(_src)):\n'
                   "    if isinstance(_n, _ast.Attribute) and _n.attr in {'sort', 'index', 'pop', "
                   "'remove', 'count', 'insert'}:\n"
                   '        _bad.add("." + _n.attr + "()")\n'
                   '    elif False and isinstance(_n, _ast.Compare) and any(isinstance(_o, (_ast.In, '
                   '_ast.NotIn)) for _o in _n.ops):\n'
                   '        _bad.add("in")\n'
                   '    elif False and isinstance(_n, _ast.Slice):\n'
                   '        _bad.add("срезы")\n'
                   "    elif isinstance(_n, _ast.Name) and _n.id in {'sorted'}:\n"
                   '        _bad.add(_n.id)\n'
                   '    elif type(_n).__name__ in set():\n'
                   '        _bad.add("словари и множества")\n'
                   '    elif isinstance(_n, _ast.Import) and any(_a.name.split(".")[0] in {\'bisect\', '
                   "'re', 'heapq'} for _a in _n.names):\n"
                   '        _bad.add("import")\n'
                   '    elif isinstance(_n, _ast.ImportFrom) and (_n.module or "").split(".")[0] in '
                   "{'bisect', 're', 'heapq'}:\n"
                   '        _bad.add("import")\n'
                   'if _bad:\n'
                   '    print("запрещённые приёмы:", ", ".join(sorted(_bad)))\n'
                   'else:\n'
                   '    s = OrderSet(10)\n'
                   '    for v in [5, 3, 8, 3, 10]:\n'
                   '        s.add(v)\n'
                   '    print([s.kth(k) for k in range(1, 6)])\n'
                   '    s.discard(3)\n'
                   '    print([s.kth(k) for k in range(1, 5)])\n'
                   '    M = 1000000\n'
                   '    s = OrderSet(M)\n'
                   '    x = 17\n'
                   '    size = 0\n'
                   '    total = 0\n'
                   '    for q in range(200000):\n'
                   '        x = nxt(x)\n'
                   '        if size < 1000 or q % 3:\n'
                   '            s.add(1 + x % M)\n'
                   '            size += 1\n'
                   '        else:\n'
                   '            v = s.kth(1 + x % size)\n'
                   '            s.discard(v)\n'
                   '            size -= 1\n'
                   '            total += v\n'
                   '    print(size, total, s.kth(1), s.kth(size))\n',
         'expected': ['[3, 3, 5, 8, 10]', '[3, 5, 8, 10]', '67334 33223511952 6 999986'],
         'hint': 'В узле Фенвика лежит число элементов отрезка: спускайтесь от старшего бита, прибавляя '
                 'шаг, пока накопленное меньше k.'},
        {'id': 'seg-smaller-before',
         'mode': 'stdout',
         'title': 'Сколько меньших слева',
         'statement': 'Напишите функцию smaller_before(a): список res, где res[i] — сколько элементов '
                      'слева от i-го строго меньше a[i]. Проверка — двести тысяч чисел: квадратичный '
                      'перебор не успеет.',
         'starter': 'def smaller_before(a):\n    pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'print(smaller_before([3, 1, 4, 1, 5, 9, 2, 6]), smaller_before([]), smaller_before([5, '
                   '5, 5]))\n'
                   'n = 200000\n'
                   'x = 1\n'
                   'a = []\n'
                   'for _ in range(n):\n'
                   '    x = nxt(x)\n'
                   '    a.append(x % 100000)\n'
                   'r = smaller_before(a)\n'
                   'print(sum(r), r[-1], max(r))\n',
         'expected': ['[0, 0, 2, 0, 4, 5, 2, 6] [] [0, 0, 0]', '10016927167 86989 199517'],
         'hint': 'Сожмите значения в ранги; считайте в дереве Фенвика, сколько встретилось рангов меньше '
                 'текущего.'},
        {'id': 'seg-distinct-ranges',
         'mode': 'stdout',
         'title': 'Различные числа на отрезках',
         'statement': 'Напишите функцию distinct_in_ranges(a, queries): для каждого запроса [l, r] (с '
                      'нуля, обе границы включены) — сколько различных значений среди a[l..r]. Ответы — в '
                      'порядке запросов. Проверка — двести тысяч элементов и запросов. Идея: обработайте '
                      'запросы офлайн по правому краю и храните в дереве Фенвика единицы на последних '
                      'вхождениях значений.',
         'starter': 'def distinct_in_ranges(a, queries):\n    pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'print(distinct_in_ranges([1, 2, 1, 3, 2], [[0, 4], [1, 2], [2, 2], [0, 0], [2, 4]]))\n'
                   'n = 200000\n'
                   'x = 21\n'
                   'a = []\n'
                   'for _ in range(n):\n'
                   '    x = nxt(x)\n'
                   '    a.append(x % 50000)\n'
                   'qs = []\n'
                   'for _ in range(200000):\n'
                   '    x = nxt(x)\n'
                   '    l = x % n\n'
                   '    x = nxt(x)\n'
                   '    qs.append([l, l + x % (n - l)])\n'
                   'r = distinct_in_ranges(a, qs)\n'
                   'print(sum(r), r[:3], r[-3:])\n',
         'expected': ['[3, 2, 1, 1, 3]', '5074342404 [43270, 40408, 20537] [18764, 27112, 9643]'],
         'hint': 'Идите по r слева направо: на последнем вхождении значения держите единицу, на предыдущем '
                 '— снимайте; ответ — сумма на [l, r].'},
        {'id': 'seg-tree-sum',
         'mode': 'stdout',
         'title': 'Дерево отрезков: сумма',
         'statement': 'Напишите класс SegTree: SegTree(a) строит дерево по списку a; update(i, v) '
                      'присваивает a[i] = v; query(l, r) возвращает сумму a[l] + … + a[r − 1] (правая '
                      'граница не включена). Операции — за O(log n): проверка выполняет двести тысяч '
                      'операций над массивом из двухсот тысяч чисел.',
         'starter': 'class SegTree:\n'
                    '    def __init__(self, a):\n'
                    '        pass\n'
                    '\n'
                    '    def update(self, i, v):\n'
                    '        pass\n'
                    '\n'
                    '    def query(self, l, r):\n'
                    '        pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   't = SegTree([5, 3, 7, 1, 4, 2, 6, 8])\n'
                   'print(t.query(0, 8), t.query(2, 7), t.query(3, 4), t.query(5, 5))\n'
                   't.update(3, 6)\n'
                   'print(t.query(0, 8), t.query(2, 4))\n'
                   'n = 200000\n'
                   'x = 33\n'
                   'a = []\n'
                   'for _ in range(n):\n'
                   '    x = nxt(x)\n'
                   '    a.append(x % 1000)\n'
                   't = SegTree(a)\n'
                   'total = 0\n'
                   'for q in range(200000):\n'
                   '    x = nxt(x)\n'
                   '    i = x % n\n'
                   '    x = nxt(x)\n'
                   '    if q % 2:\n'
                   '        t.update(i, x % 1000)\n'
                   '    else:\n'
                   '        total += t.query(i, i + 1 + x % (n - i))\n'
                   'print(total, t.query(0, n))\n',
         'expected': ['36 20 1 0', '41 13', '2497352033162 99847686'],
         'hint': 'Листья — во второй половине массива из 2n элементов; родитель i — сумма детей 2i и 2i + '
                 '1. Запрос идёт двумя указателями l и r и поднимается к корню.'},
        {'id': 'seg-tree-generic',
         'mode': 'stdout',
         'title': 'Дерево отрезков для любой операции',
         'statement': 'Напишите класс GenericTree: GenericTree(a, op, neutral) — дерево для ассоциативной '
                      'операции op с нейтральным элементом neutral (op не обязательно коммутативна: '
                      'склейка строк, умножение матриц); update(i, v) присваивает a[i] = v; query(l, r) — '
                      'результат op по элементам a[l..r − 1] слева направо (для пустого отрезка — '
                      'neutral). Порядок аргументов op важен.',
         'starter': 'class GenericTree:\n'
                    '    def __init__(self, a, op, neutral):\n'
                    '        pass\n'
                    '\n'
                    '    def update(self, i, v):\n'
                    '        pass\n'
                    '\n'
                    '    def query(self, l, r):\n'
                    '        pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'import math\n'
                   't = GenericTree([4, 8, 6, 9, 12, 15], math.gcd, 0)\n'
                   'print(t.query(0, 3), t.query(3, 6), t.query(1, 2), t.query(2, 2))\n'
                   't.update(1, 3)\n'
                   'print(t.query(0, 3))\n'
                   's = GenericTree(list("hello"), lambda p, q: p + q, "")\n'
                   'print(s.query(0, 5), s.query(1, 4), repr(s.query(2, 2)))\n'
                   's.update(0, "J")\n'
                   'print(s.query(0, 5))\n'
                   'n = 100000\n'
                   'x = 41\n'
                   'a = []\n'
                   'for _ in range(n):\n'
                   '    x = nxt(x)\n'
                   '    a.append(x % 1000003)\n'
                   'm = GenericTree(a, min, 10 ** 9)\n'
                   'total = 0\n'
                   'for q in range(100000):\n'
                   '    x = nxt(x)\n'
                   '    i = x % n\n'
                   '    x = nxt(x)\n'
                   '    if q % 2:\n'
                   '        m.update(i, x % 1000003)\n'
                   '    else:\n'
                   '        total += m.query(i, i + 1 + x % (n - i))\n'
                   'print(total)\n',
         'expected': ['2 3 8 0', '1', "hello ell ''", 'Jello', '33015139'],
         'hint': 'Накапливайте левую и правую части отдельно: left = op(left, t[l]), right = op(t[r], '
                 'right) — тогда порядок сохраняется.'},
        {'id': 'seg-first-at-least',
         'mode': 'stdout',
         'title': 'Первый элемент не меньше x',
         'statement': 'Напишите класс MaxTree: MaxTree(a) строит дерево максимумов; update(i, v) '
                      'присваивает a[i] = v; first_at_least(x) возвращает наименьший индекс i с a[i] ≥ x '
                      'или -1. Ответ — за один спуск от корня, O(log n): проверка размещает сто тысяч '
                      'заявок в гостинице на 131072 номера.',
         'starter': 'class MaxTree:\n'
                    '    def __init__(self, a):\n'
                    '        pass\n'
                    '\n'
                    '    def update(self, i, v):\n'
                    '        pass\n'
                    '\n'
                    '    def first_at_least(self, x):\n'
                    '        pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   't = MaxTree([3, 9, 4, 12, 7])\n'
                   'print(t.first_at_least(10), t.first_at_least(4), t.first_at_least(13), '
                   't.first_at_least(1))\n'
                   't.update(3, 2)\n'
                   'print(t.first_at_least(10), t.first_at_least(8))\n'
                   'n = 131072\n'
                   't = MaxTree([1000] * n)\n'
                   'x = 77\n'
                   'placed = 0\n'
                   'last = 0\n'
                   'for _ in range(100000):\n'
                   '    x = nxt(x)\n'
                   '    need = 500 + x % 501\n'
                   '    room = t.first_at_least(need)\n'
                   '    if room >= 0:\n'
                   '        placed += 1\n'
                   '        last = room\n'
                   '        t.update(room, t.t[t.n + room] - need)\n'
                   'print(placed, last)\n',
         'expected': ['3 1 -1 0', '-1 1', '100000 99908'],
         'hint': 'В узле хранится максимум: если левый ребёнок содержит значение ≥ x — идите влево, иначе '
                 'вправо.'},
        {'id': 'seg-max-subarray',
         'mode': 'stdout',
         'title': 'Максимальная подотрезочная сумма с изменениями',
         'statement': 'Напишите класс MaxSub: MaxSub(a) строит структуру; update(i, v) присваивает a[i] = '
                      'v; query(l, r) — наибольшая сумма непустого подотрезка внутри a[l..r − 1] (l < r). '
                      'В узле храните четвёрку: сумма всего отрезка, лучший префикс, лучший суффикс и '
                      'лучший подотрезок. Проверка — сто тысяч операций.',
         'starter': 'class MaxSub:\n'
                    '    def __init__(self, a):\n'
                    '        pass\n'
                    '\n'
                    '    def update(self, i, v):\n'
                    '        pass\n'
                    '\n'
                    '    def query(self, l, r):\n'
                    '        pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   't = MaxSub([-2, 1, -3, 4, -1, 2, 1, -5, 4])\n'
                   'print(t.query(0, 9), t.query(0, 3), t.query(7, 8), t.query(3, 7))\n'
                   't.update(7, 10)\n'
                   'print(t.query(0, 9), t.query(6, 9))\n'
                   'n = 50000\n'
                   'x = 55\n'
                   'a = []\n'
                   'for _ in range(n):\n'
                   '    x = nxt(x)\n'
                   '    a.append(x % 201 - 100)\n'
                   't = MaxSub(a)\n'
                   'total = 0\n'
                   'for q in range(50000):\n'
                   '    x = nxt(x)\n'
                   '    i = x % n\n'
                   '    x = nxt(x)\n'
                   '    if q % 2:\n'
                   '        t.update(i, x % 201 - 100)\n'
                   '    else:\n'
                   '        total += t.query(i, i + 1 + x % (n - i))\n'
                   'print(total, t.query(0, n))\n',
         'expected': ['6 1 -5 6', '20 15', '143525107 10739'],
         'hint': 'Склейка (s₁, p₁, u₁, b₁) и (s₂, p₂, u₂, b₂): сумма s₁ + s₂, префикс max(p₁, s₁ + p₂), '
                 'суффикс max(u₂, s₂ + u₁), лучший max(b₁, b₂, u₁ + p₂).'},
        {'id': 'seg-lazy-add',
         'mode': 'stdout',
         'title': 'Ленивые метки: прибавление и сумма',
         'statement': 'Напишите класс LazyTree: LazyTree(a); add(l, r, x) прибавляет x ко всем элементам '
                      'a[l..r − 1]; sum(l, r) — сумма a[l..r − 1]. Обе операции — за O(log n) с ленивыми '
                      'метками. Проверка — пятьдесят тысяч операций над массивом из пятидесяти тысяч '
                      'чисел.',
         'starter': 'class LazyTree:\n'
                    '    def __init__(self, a):\n'
                    '        pass\n'
                    '\n'
                    '    def add(self, l, r, x):\n'
                    '        pass\n'
                    '\n'
                    '    def sum(self, l, r):\n'
                    '        pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   't = LazyTree([1, 2, 3, 4, 5])\n'
                   't.add(1, 4, 10)\n'
                   'print(t.sum(0, 5), t.sum(1, 2), t.sum(2, 4))\n'
                   't.add(0, 5, -1)\n'
                   'print(t.sum(0, 5), t.sum(4, 5))\n'
                   'n = 50000\n'
                   'x = 91\n'
                   'a = []\n'
                   'for _ in range(n):\n'
                   '    x = nxt(x)\n'
                   '    a.append(x % 100)\n'
                   't = LazyTree(a)\n'
                   'total = 0\n'
                   'for q in range(50000):\n'
                   '    x = nxt(x)\n'
                   '    l = x % n\n'
                   '    x = nxt(x)\n'
                   '    r = l + 1 + x % (n - l)\n'
                   '    x = nxt(x)\n'
                   '    if q % 2:\n'
                   '        t.add(l, r, x % 21 - 10)\n'
                   '    else:\n'
                   '        total += t.sum(l, r)\n'
                   'print(total, t.sum(0, n))\n',
         'expected': ['45 12 27', '40 4', '40251771747 7042763'],
         'hint': 'Узел, целиком накрытый операцией, обновляется сразу и получает метку; перед спуском '
                 'метку передают детям (push).'},
        {'id': 'seg-lazy-assign',
         'mode': 'stdout',
         'title': 'Ленивые метки: присваивание и сумма',
         'statement': 'Напишите класс AssignTree: AssignTree(a); assign(l, r, x) присваивает x всем '
                      'элементам a[l..r − 1]; sum(l, r) — сумма a[l..r − 1]. Метка — «присвоить x» (None, '
                      'если метки нет): новая метка заменяет старую, а ответ узла равен x умножить на '
                      'длину отрезка. Проверка — сто тысяч элементов и шестьдесят тысяч операций.',
         'starter': 'class AssignTree:\n'
                    '    def __init__(self, a):\n'
                    '        pass\n'
                    '\n'
                    '    def assign(self, l, r, x):\n'
                    '        pass\n'
                    '\n'
                    '    def sum(self, l, r):\n'
                    '        pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   't = AssignTree([1, 2, 3, 4, 5])\n'
                   't.assign(1, 4, 7)\n'
                   'print(t.sum(0, 5), t.sum(1, 2), t.sum(3, 5))\n'
                   't.assign(0, 5, 0)\n'
                   'print(t.sum(0, 5))\n'
                   'n = 100000\n'
                   'x = 5\n'
                   'a = []\n'
                   'for _ in range(n):\n'
                   '    x = nxt(x)\n'
                   '    a.append(x % 100)\n'
                   't = AssignTree(a)\n'
                   'total = 0\n'
                   'for q in range(60000):\n'
                   '    x = nxt(x)\n'
                   '    l = x % n\n'
                   '    x = nxt(x)\n'
                   '    r = l + 1 + x % (n - l)\n'
                   '    x = nxt(x)\n'
                   '    if q % 2 == 0:\n'
                   '        t.assign(l, r, x % 50)\n'
                   '    else:\n'
                   '        total += t.sum(l, r)\n'
                   'print(total, t.sum(0, n))\n',
         'expected': ['27 7 12', '0', '18336188223 1509608'],
         'hint': 'Метка None означает «ничего не откладывали»; при push обновите ответы детей как x · '
                 'длина и передайте им метку.'},
        {'id': 'seg-sparse-table',
         'mode': 'stdout',
         'title': 'Разреженная таблица',
         'statement': 'Напишите класс SparseTable: SparseTable(a) строит таблицу за O(n log n); query(l, '
                      'r) возвращает минимум a[l..r − 1] (l < r) за O(1) — через две перекрывающиеся '
                      'степени двойки. Проверка — триста тысяч элементов и пятьсот тысяч запросов.',
         'starter': 'class SparseTable:\n'
                    '    def __init__(self, a):\n'
                    '        pass\n'
                    '\n'
                    '    def query(self, l, r):\n'
                    '        pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   't = SparseTable([5, 2, 4, 7, 1, 3, 6, 8])\n'
                   'print(t.query(1, 6), t.query(0, 8), t.query(3, 4), t.query(5, 8))\n'
                   'n = 300000\n'
                   'x = 61\n'
                   'a = []\n'
                   'for _ in range(n):\n'
                   '    x = nxt(x)\n'
                   '    a.append(x % 1000000)\n'
                   't = SparseTable(a)\n'
                   'total = 0\n'
                   'for _ in range(500000):\n'
                   '    x = nxt(x)\n'
                   '    l = x % n\n'
                   '    x = nxt(x)\n'
                   '    total += t.query(l, l + 1 + x % (n - l))\n'
                   'print(total, t.query(0, n))\n',
         'expected': ['1 1 7 3', '141215170 3'],
         'hint': 'Строка k хранит минимумы на отрезках длины 2ᵏ: t[k][i] = min(t[k − 1][i], t[k − 1][i + '
                 '2^(k−1)]). Для запроса возьмите k = floor(log₂(r − l)).'},
        {'id': 'seg-fenwick-2d',
         'mode': 'stdout',
         'title': 'Двумерное дерево Фенвика',
         'statement': 'Напишите класс Fenwick2D: Fenwick2D(n, m) — нулевая матрица n × m (индексы с нуля); '
                      'add(x, y, v) прибавляет v к клетке (x, y); sum(x1, y1, x2, y2) — сумма по '
                      'прямоугольнику с углами (x1, y1) и (x2, y2), включая границы. Каждая операция — '
                      'O(log n · log m): проверка — матрица 1000 × 1000 и сто тысяч операций.',
         'starter': 'class Fenwick2D:\n'
                    '    def __init__(self, n, m):\n'
                    '        pass\n'
                    '\n'
                    '    def add(self, x, y, v):\n'
                    '        pass\n'
                    '\n'
                    '    def sum(self, x1, y1, x2, y2):\n'
                    '        pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   't = Fenwick2D(3, 4)\n'
                   't.add(0, 0, 5)\n'
                   't.add(1, 2, 3)\n'
                   't.add(2, 3, 7)\n'
                   'print(t.sum(0, 0, 2, 3), t.sum(1, 1, 2, 3), t.sum(0, 0, 0, 0), t.sum(1, 0, 1, 1))\n'
                   'n = m = 1000\n'
                   't = Fenwick2D(n, m)\n'
                   'x = 13\n'
                   'total = 0\n'
                   'for q in range(100000):\n'
                   '    x = nxt(x)\n'
                   '    a = x % n\n'
                   '    x = nxt(x)\n'
                   '    b = x % m\n'
                   '    x = nxt(x)\n'
                   '    if q % 2:\n'
                   '        t.add(a, b, x % 100)\n'
                   '    else:\n'
                   '        c = a + x % (n - a)\n'
                   '        x = nxt(x)\n'
                   '        d = b + x % (m - b)\n'
                   '        total += t.sum(a, b, c, d)\n'
                   'print(total, t.sum(0, 0, n - 1, m - 1))\n',
         'expected': ['15 10 5 0', '3804190072 2471190'],
         'hint': 'Вложенный цикл: внешний по x (i += i & −i), внутренний по y. Прямоугольник — четыре '
                 'префикса, как в двумерных суммах.'},
        {'id': 'seg-lis',
         'mode': 'stdout',
         'title': 'Длиннейшая возрастающая подпоследовательность',
         'statement': 'Напишите функцию lis_length(a): длина наибольшей строго возрастающей '
                      'подпоследовательности списка (не обязательно из соседних элементов). Проверка — сто '
                      'тысяч чисел, поэтому нужно O(n log n): дерево Фенвика по максимуму (в позиции '
                      'значения хранится лучшая длина) или метод «хвостов» с двоичным поиском.',
         'starter': 'def lis_length(a):\n    pass\n',
         'driver': 'def nxt(x):\n'
                   '    x ^= (x << 13) & 0xFFFFFFFF\n'
                   '    x ^= x >> 17\n'
                   '    x ^= (x << 5) & 0xFFFFFFFF\n'
                   '    return x\n'
                   'print(lis_length([10, 9, 2, 5, 3, 7, 101, 18]), lis_length([0, 1, 0, 3, 2, 3]), '
                   'lis_length([7, 7, 7]), lis_length([]))\n'
                   'n = 100000\n'
                   'x = 8\n'
                   'a = []\n'
                   'for _ in range(n):\n'
                   '    x = nxt(x)\n'
                   '    a.append(x % 1000000)\n'
                   'print(lis_length(a), lis_length(list(range(n))), lis_length(list(range(n, 0, -1))))\n',
         'expected': ['4 4 1 0', '630 100000 1'],
         'hint': 'Дерево Фенвика по максимуму: dp[значение] = 1 + максимум по меньшим значениям; ответ — '
                 'максимум всех dp.'},
    ],
}
