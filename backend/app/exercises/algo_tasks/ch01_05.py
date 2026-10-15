"""Задачи книги «Алгоритмы»: ch01_05."""

TASKS: dict[int, list[dict]] = {
    1: [
        {
            "id": "has-duplicates",
            "mode": "stdout",
            "title": "Есть ли повторы за O(n)",
            "statement": (
                "Напишите функцию has_duplicates(nums): True, если в списке "
                "есть повторяющиеся числа. Решение должно работать за O(n) "
                "или O(n log n): проверка подаёт списки из 300 000 элементов, "
                "с вложенными циклами O(n²) вы в лимит времени не уложитесь."
            ),
            "starter": "def has_duplicates(nums):\n    pass\n",
            "driver": (
                "print(has_duplicates([1, 2, 3, 1]), has_duplicates([]), has_duplicates([5]), has_duplicates([1, 2, 3]))\n"
                "big = list(range(300000))\nprint(has_duplicates(big), has_duplicates(big + [7]))\n"
            ),
            "expected": ["True False False False", "False True"],
            "hint": "Заведите словарь или множество увиденных чисел: проверка «уже было» — O(1).",
        },
        {
            "id": "fast-power",
            "mode": "stdout",
            "title": "Быстрое возведение в степень",
            "statement": (
                "Напишите функцию fast_power(base, exp): base в степени exp "
                "(exp — целое, 0 и больше), используя только умножение *. "
                "Алгоритм должен делать O(log exp) умножений: проверка "
                "считает, сколько раз вы умножали, и для exp = 1000 допускает "
                "не более 30. Для exp = 0 результат — 1."
            ),
            "starter": "def fast_power(base, exp):\n    pass\n",
            "driver": (
                "class M:\n    count = 0\n    def __init__(self, v):\n        self.v = v\n"
                "    def __mul__(self, o):\n        M.count += 1\n        return M(self.v * (o.v if isinstance(o, M) else o))\n"
                "    __rmul__ = __mul__\n"
                "r = fast_power(M(3), 20)\nprint(r.v == 3 ** 20, M.count <= 10)\n"
                "M.count = 0\nr = fast_power(M(2), 1000)\nprint(r.v == 2 ** 1000, M.count <= 30)\n"
                "print(fast_power(5, 0), fast_power(2, 10), fast_power(7, 1))\n"
            ),
            "expected": ["True True", "True True", "1 1024 7"],
            "hint": "Двоичная запись показателя: на каждом шаге возводите base в квадрат, а если очередной бит единица — домножайте результат (или рекурсия: x^n = (x^(n/2))² и ещё один множитель при нечётном n).",
        },
        {
            "id": "count-pairs-hash",
            "mode": "stdout",
            "title": "Пары с заданной суммой",
            "statement": (
                "Напишите функцию count_pairs(nums, target): сколько пар "
                "индексов i < j даёт nums[i] + nums[j] == target. Числа могут "
                "повторяться. Нужен линейный алгоритм: проверка подаёт "
                "100 000 чисел."
            ),
            "starter": "def count_pairs(nums, target):\n    pass\n",
            "driver": (
                "print(count_pairs([1, 2, 3, 4], 5), count_pairs([2, 2, 2], 4), count_pairs([], 1), count_pairs([5], 10))\n"
                "print(count_pairs([1, 5, 1, 5], 6))\n"
                "big = list(range(100000))\nprint(count_pairs(big, 100000), count_pairs(big, 1000000))\n"
            ),
            "expected": ["2 3 0 0", "4", "49999 0"],
            "hint": "Идите слева направо и храните в словаре, сколько раз уже встретилось каждое число; для x прибавляйте count[target - x].",
        },
        {
            "id": "max-subarray-kadane",
            "mode": "stdout",
            "title": "Лучший подотрезок",
            "statement": (
                "Напишите функцию max_subarray(nums): наибольшая сумма "
                "непрерывного непустого подотрезка списка. Список не пустой. "
                "Решение за один проход (алгоритм Кадане): проверка подаёт "
                "миллион чисел."
            ),
            "starter": "def max_subarray(nums):\n    pass\n",
            "driver": (
                "print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), max_subarray([-3, -1, -2]), max_subarray([5]))\n"
                "print(max_subarray([1] * 1000000), max_subarray([3, -1] * 500000))\n"
            ),
            "expected": ["6 -1 5", "1000000 1000001"],
            "hint": "current = max(x, current + x); best = max(best, current) — «обрываем» отрезок, если хвост только мешает.",
        },
        {
            "id": "power-of-two",
            "mode": "func",
            "func": "is_power_of_two",
            "title": "Степень двойки за O(1)",
            "statement": (
                "Напишите функцию is_power_of_two(n): True, если n — степень "
                "двойки (1, 2, 4, 8, …). Для n <= 0 — False. Без циклов: "
                "достаточно одной побитовой проверки."
            ),
            "starter": "def is_power_of_two(n):\n    pass\n",
            "tests": [
                {"args": [1], "expected": True},
                {"args": [64], "expected": True},
                {"args": [6], "expected": False},
                {"args": [0], "expected": False},
                {"args": [-8], "expected": False},
                {"args": [2 ** 100], "expected": True},
            ],
            "hint": "У степени двойки ровно один единичный бит: n & (n - 1) == 0.",
        },
        {
            "id": "fib-linear",
            "mode": "stdout",
            "title": "Фибоначчи без экспоненты",
            "statement": (
                "Напишите функцию fib(n): n-е число Фибоначчи (fib(0) = 0, "
                "fib(1) = 1). Наивная рекурсия делает экспоненциально много "
                "вызовов, а проверка просит fib(300): нужен линейный "
                "алгоритм (цикл или запоминание)."
            ),
            "starter": "def fib(n):\n    pass\n",
            "driver": "print(fib(0), fib(1), fib(10))\nprint(fib(90))\nprint(fib(300))\n",
            "expected": ["0 1 55", "2880067194370816120", "222232244629420445529739893461909967206666939096499764990979600"],
            "hint": "Держите две последние величины: a, b = b, a + b — и n шагов.",
        },
        {
            "id": "binary-search-steps",
            "mode": "func",
            "func": "worst_case_steps",
            "title": "Сколько шагов у двоичного поиска",
            "statement": (
                "Напишите функцию worst_case_steps(n): сколько сравнений "
                "понадобится двоичному поиску в худшем случае на "
                "отсортированном списке из n элементов (n >= 1). Делите n "
                "пополам (с отбрасыванием остатка), пока не останется 0, и "
                "считайте шаги: для 1 → 1, для 7 → 3, для 8 → 4."
            ),
            "starter": "def worst_case_steps(n):\n    pass\n",
            "tests": [
                {"args": [1], "expected": 1},
                {"args": [7], "expected": 3},
                {"args": [8], "expected": 4},
                {"args": [1000000], "expected": 20},
                {"args": [10 ** 18], "expected": 60},
            ],
            "hint": "steps = 0; while n > 0: n //= 2; steps += 1 — это ровно длина двоичной записи числа.",
        },
    ],
    2: [
        {
            "id": "reverse-in-place",
            "mode": "stdout",
            "title": "Развернуть на месте",
            "statement": (
                "Напишите функцию reverse_in_place(arr): разворачивает "
                "список НА МЕСТЕ двумя указателями (один с начала, другой с "
                "конца, обмениваем и сближаем). Ничего не возвращает и не "
                "создаёт копий."
            ),
            "starter": "def reverse_in_place(arr):\n    pass\n",
            "driver": (
                "a = [1, 2, 3, 4, 5]\nr = reverse_in_place(a)\nprint(a, r)\nb = []\nreverse_in_place(b)\nprint(b)\n"
                "c = ['а', 'б']\nsame = c\nreverse_in_place(c)\nprint(same)\n"
                "big = list(range(1000000))\nreverse_in_place(big)\nprint(big[0], big[-1])\n"
            ),
            "expected": ["[5, 4, 3, 2, 1] None", "[]", "['б', 'а']", "999999 0"],
            "hint": "i, j = 0, len(arr) - 1; while i < j: arr[i], arr[j] = arr[j], arr[i]; i += 1; j -= 1.",
        },
        {
            "id": "rotate-right",
            "mode": "stdout",
            "title": "Циклический сдвиг",
            "statement": (
                "Напишите функцию rotate_right(arr, k): сдвигает список "
                "вправо на k позиций по кругу НА МЕСТЕ (k может быть больше "
                "длины). Решение за O(n): проверка подаёт миллион элементов."
            ),
            "starter": "def rotate_right(arr, k):\n    pass\n",
            "driver": (
                "a = [1, 2, 3, 4, 5, 6, 7]\nrotate_right(a, 3)\nprint(a)\n"
                "b = [1, 2, 3]\nrotate_right(b, 7)\nprint(b)\nc = []\nrotate_right(c, 2)\nprint(c)\n"
                "big = list(range(1000000))\nrotate_right(big, 100000)\nprint(big[0], big[100000], big[-1])\n"
            ),
            "expected": ["[5, 6, 7, 1, 2, 3, 4]", "[3, 1, 2]", "[]", "900000 0 899999"],
            "hint": "k %= n; затем три разворота: весь список, первые k, остальные — либо срез arr[:] = arr[-k:] + arr[:-k].",
        },
        {
            "id": "reverse-linked-list",
            "mode": "stdout",
            "title": "Развернуть связный список",
            "statement": (
                "Дан класс ListNode (val, next). Напишите функцию "
                "reverse_list(head): разворачивает односвязный список, "
                "переставляя ссылки next, и возвращает новую голову. Без "
                "создания новых узлов и без рекурсии (в списке бывает 100 000 "
                "узлов)."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef reverse_list(head):\n    pass\n",
            "driver": (
                "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n"
                "def to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\n"
                "print(to_list(reverse_list(build([1, 2, 3, 4]))), to_list(reverse_list(build([7]))), to_list(reverse_list(None)))\n"
                "r = reverse_list(build(list(range(100000))))\nprint(r.val, to_list(r)[-1])\n"
            ),
            "expected": ["[4, 3, 2, 1] [7] []", "99999 0"],
            "hint": "prev = None; пока head: nxt = head.next; head.next = prev; prev = head; head = nxt; вернуть prev.",
        },
        {
            "id": "middle-node",
            "mode": "stdout",
            "title": "Середина списка",
            "statement": (
                "Дан класс ListNode. Напишите функцию middle(head): значение "
                "среднего узла за ОДИН проход (медленный и быстрый указатели). "
                "Для списка чётной длины — второй из двух средних."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef middle(head):\n    pass\n",
            "driver": (
                "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n"
                "print(middle(build([1, 2, 3, 4, 5])), middle(build([1, 2, 3, 4])), middle(build([9])))\n"
                "print(middle(build(list(range(1000001)))))\n"
            ),
            "expected": ["3 3 9", "500000"],
            "hint": "slow = fast = head; while fast and fast.next: slow = slow.next; fast = fast.next.next.",
        },
        {
            "id": "has-cycle",
            "mode": "stdout",
            "title": "Есть ли цикл",
            "statement": (
                "Дан класс ListNode. Напишите функцию has_cycle(head): True, "
                "если по ссылкам next можно ходить бесконечно (в списке есть "
                "цикл). Алгоритм Флойда: два указателя с разной скоростью, O(1) "
                "памяти."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef has_cycle(head):\n    pass\n",
            "driver": (
                "def build(n):\n    nodes = [ListNode(i) for i in range(n)]\n    for a, b in zip(nodes, nodes[1:]):\n        a.next = b\n    return nodes\n"
                "print(has_cycle(None), has_cycle(ListNode(1)))\n"
                "ns = build(5)\nprint(has_cycle(ns[0]))\nns[4].next = ns[2]\nprint(has_cycle(ns[0]))\n"
                "one = ListNode(1)\none.next = one\nprint(has_cycle(one))\n"
                "big = build(200000)\nprint(has_cycle(big[0]))\nbig[-1].next = big[0]\nprint(has_cycle(big[0]))\n"
            ),
            "expected": ["False False", "False", "True", "True", "False", "True"],
            "hint": "slow сдвигайте на 1, fast на 2; если они встретились — цикл есть, если fast упёрся в None — нет.",
        },
        {
            "id": "merge-sorted-lists",
            "mode": "stdout",
            "title": "Слить два отсортированных списка",
            "statement": (
                "Дан класс ListNode. Напишите функцию merge_lists(a, b): "
                "сливает два отсортированных по возрастанию связных списка в "
                "один отсортированный, переиспользуя узлы, и возвращает "
                "голову. Время O(n + m), без рекурсии."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef merge_lists(a, b):\n    pass\n",
            "driver": (
                "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n"
                "def to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\n"
                "print(to_list(merge_lists(build([1, 3, 5]), build([2, 4, 6]))))\n"
                "print(to_list(merge_lists(build([]), build([1, 2]))), to_list(merge_lists(build([1]), build([]))))\n"
                "print(to_list(merge_lists(build([1, 1, 2]), build([1, 3]))))\n"
                "m = to_list(merge_lists(build(list(range(0, 200000, 2))), build(list(range(1, 200000, 2)))))\nprint(m == list(range(200000)))\n"
            ),
            "expected": ["[1, 2, 3, 4, 5, 6]", "[1, 2] [1]", "[1, 1, 1, 2, 3]", "True"],
            "hint": "Фиктивный узел dummy и указатель tail: на каждом шаге присоединяйте меньший из двух текущих узлов.",
        },
        {
            "id": "is-palindrome-two-pointers",
            "mode": "func",
            "func": "is_palindrome",
            "title": "Палиндром",
            "statement": (
                "Напишите функцию is_palindrome(s): True, если строка читается "
                "одинаково в обе стороны, если не обращать внимания на "
                "регистр и на все символы, кроме букв и цифр. Идите двумя "
                "указателями с концов."
            ),
            "starter": "def is_palindrome(s):\n    pass\n",
            "tests": [
                {"args": ["А роза упала на лапу Азора"], "expected": True},
                {"args": ["Was it a car or a cat I saw?"], "expected": True},
                {"args": ["привет"], "expected": False},
                {"args": [""], "expected": True},
                {"args": [".,"], "expected": True},
                {"args": ["ab"], "expected": False},
            ],
            "hint": "i, j = 0, len(s) - 1; пропускайте символы, у которых not ch.isalnum(); сравнивайте через lower().",
        },
        {
            "id": "longest-common-prefix",
            "mode": "func",
            "func": "common_prefix",
            "title": "Общий префикс",
            "statement": (
                "Напишите функцию common_prefix(words): самая длинная общая "
                "начальная часть всех слов списка (пустая строка, если её нет "
                "или список пуст)."
            ),
            "starter": "def common_prefix(words):\n    pass\n",
            "tests": [
                {"args": [["цветок", "цвет", "цветной"]], "expected": "цвет"},
                {"args": [["собака", "гоночная", "машина"]], "expected": ""},
                {"args": [["одно"]], "expected": "одно"},
                {"args": [[]], "expected": ""},
                {"args": [["аб", "аб", "аб"]], "expected": "аб"},
            ],
            "hint": "Берите первое слово как кандидата и укорачивайте, пока каждое слово не начнётся с него (startswith).",
        },
    ],
    3: [
        {
            "id": "binary-search-count",
            "mode": "stdout",
            "title": "Двоичный поиск",
            "statement": (
                "Напишите функцию binary_search(arr, target): индекс target в "
                "отсортированном по возрастанию списке или -1. Проверка "
                "считает обращения к элементам: на списке из миллиона "
                "элементов вы вправе сделать не больше 25 обращений — "
                "линейный перебор не пройдёт."
            ),
            "starter": "def binary_search(arr, target):\n    pass\n",
            "driver": (
                "class CL(list):\n    reads = 0\n    def __getitem__(self, i):\n        CL.reads += 1\n        return list.__getitem__(self, i)\n"
                "print(binary_search([1, 3, 5, 7, 9], 7), binary_search([1, 3, 5], 4), binary_search([], 1), binary_search([2], 2))\n"
                "arr = CL(range(0, 2000000, 2))\nCL.reads = 0\nx = binary_search(arr, 1234568)\nr1 = CL.reads\nCL.reads = 0\ny = binary_search(arr, 7)\nr2 = CL.reads\nprint(x, y, r1 <= 25 and r2 <= 25)\n"
            ),
            "expected": ["3 -1 -1 0", "617284 -1 True"],
            "hint": "lo, hi = 0, len(arr) - 1; mid = (lo + hi) // 2; сравните arr[mid] один раз за шаг (положите в переменную!) и отбросьте половину.",
        },
        {
            "id": "lower-bound",
            "mode": "stdout",
            "title": "Первая позиция не меньше x",
            "statement": (
                "Напишите функцию lower_bound(arr, x): индекс первого "
                "элемента отсортированного списка, который больше или равен "
                "x (len(arr), если такого нет). За O(log n): проверка "
                "считает обращения (не больше 25 на миллионе)."
            ),
            "starter": "def lower_bound(arr, x):\n    pass\n",
            "driver": (
                "class CL(list):\n    reads = 0\n    def __getitem__(self, i):\n        CL.reads += 1\n        return list.__getitem__(self, i)\n"
                "print(lower_bound([1, 2, 2, 2, 5], 2), lower_bound([1, 2, 5], 3), lower_bound([1, 2, 5], 9), lower_bound([1, 2, 5], 0), lower_bound([], 1))\n"
                "arr = CL(range(1000000))\nprint(lower_bound(arr, 777777), CL.reads <= 25)\n"
            ),
            "expected": ["1 2 3 0 0", "777777 True"],
            "hint": "lo, hi = 0, len(arr); пока lo < hi: mid = (lo + hi) // 2; если arr[mid] < x: lo = mid + 1, иначе hi = mid.",
        },
        {
            "id": "search-rotated",
            "mode": "stdout",
            "title": "Поиск в повёрнутом массиве",
            "statement": (
                "Отсортированный список без повторов циклически сдвинули: "
                "[4, 5, 6, 7, 0, 1, 2]. Напишите функцию search_rotated(arr, "
                "target): индекс target или -1 за O(log n) (проверка допускает "
                "не более 60 обращений на миллионе элементов)."
            ),
            "starter": "def search_rotated(arr, target):\n    pass\n",
            "driver": (
                "class CL(list):\n    reads = 0\n    def __getitem__(self, i):\n        CL.reads += 1\n        return list.__getitem__(self, i)\n"
                "a = [4, 5, 6, 7, 0, 1, 2]\nprint([search_rotated(a, x) for x in (0, 4, 7, 2, 3)], search_rotated([], 1), search_rotated([1], 1))\n"
                "n = 1000000\nbig = CL(list(range(300000, n)) + list(range(300000)))\nCL.reads = 0\nx = search_rotated(big, 5)\nr1 = CL.reads\nCL.reads = 0\ny = search_rotated(big, 999999)\nr2 = CL.reads\nprint(x, y, r1 <= 60 and r2 <= 60)\n"
            ),
            "expected": ["[4, 0, 3, 6, -1] -1 0", "700005 699999 True"],
            "hint": "На каждом шаге одна из половин [lo, mid] или [mid, hi] обязательно отсортирована: определите её и решите, лежит ли target внутри.",
        },
        {
            "id": "merge-sort-impl",
            "mode": "stdout",
            "title": "Сортировка слиянием",
            "statement": (
                "Напишите функцию merge_sort(arr): возвращает НОВЫЙ "
                "отсортированный список (исходный не меняйте), сортировка "
                "слиянием за O(n log n), устойчивая. Встроенные sorted и "
                "sort использовать нельзя: проверка подаёт 100 000 чисел и "
                "пары (число, метка) для проверки устойчивости."
            ),
            "starter": "def merge_sort(arr):\n    pass\n",
            "driver": (
                "import random\nrandom.seed(3)\n"
                "print(merge_sort([5, 2, 9, 1, 5, 6]), merge_sort([]), merge_sort([1]))\n"
                "a = [(2, 'а'), (1, 'б'), (2, 'в'), (1, 'г')]\nprint(merge_sort(a))\nprint(a)\n"
                "big = [random.randint(0, 10 ** 6) for _ in range(100000)]\nr = merge_sort(big)\nprint(r == sorted(big), len(r))\n"
            ),
            "expected": ["[1, 2, 5, 5, 6, 9] [] [1]", "[(1, 'б'), (1, 'г'), (2, 'а'), (2, 'в')]", "[(2, 'а'), (1, 'б'), (2, 'в'), (1, 'г')]", "True 100000"],
            "hint": "Разделите пополам, отсортируйте половины рекурсивно, слейте двумя указателями (при равных берите из ЛЕВОЙ половины — так сортировка устойчива).",
        },
        {
            "id": "quick-sort-impl",
            "mode": "stdout",
            "title": "Быстрая сортировка",
            "statement": (
                "Напишите функцию quick_sort(arr): сортирует список НА МЕСТЕ "
                "быстрой сортировкой. Проверка подаёт случайные данные, уже "
                "отсортированный список и 100 000 одинаковых элементов — "
                "наивный выбор опорного (первый/последний) и деление без "
                "учёта равных дадут O(n²) и не уложатся по времени."
            ),
            "starter": "def quick_sort(arr):\n    pass\n",
            "driver": (
                "import random, sys\nsys.setrecursionlimit(10000)\nrandom.seed(5)\n"
                "a = [3, 6, 1, 8, 2, 9, 2]\nquick_sort(a)\nprint(a)\nb = []\nquick_sort(b)\nprint(b)\n"
                "r = [random.randint(0, 10 ** 6) for _ in range(100000)]\nexp = sorted(r)\nquick_sort(r)\nprint(r == exp)\n"
                "s = list(range(100000))\nquick_sort(s)\nprint(s == list(range(100000)))\n"
                "e = [7] * 100000\nquick_sort(e)\nprint(e == [7] * 100000)\n"
            ),
            "expected": ["[1, 2, 2, 3, 6, 8, 9]", "[]", "True", "True", "True"],
            "hint": "Случайный опорный; разделение на три части: меньше, равные, больше (трёхстороннее) — тогда одинаковые элементы не вызывают деградации.",
        },
        {
            "id": "counting-sort-impl",
            "mode": "stdout",
            "title": "Сортировка подсчётом",
            "statement": (
                "Напишите функцию counting_sort(nums, max_value): сортирует "
                "целые числа от 0 до max_value за O(n + k), где k = "
                "max_value + 1. Возвращает новый список. Проверка подаёт "
                "миллион чисел с max_value = 100."
            ),
            "starter": "def counting_sort(nums, max_value):\n    pass\n",
            "driver": (
                "import random\nrandom.seed(1)\n"
                "print(counting_sort([3, 0, 2, 3, 1, 0], 3), counting_sort([], 5), counting_sort([4], 4))\n"
                "big = [random.randint(0, 100) for _ in range(1000000)]\nr = counting_sort(big, 100)\nprint(r == sorted(big), len(r))\n"
            ),
            "expected": ["[0, 0, 1, 2, 3, 3] [] [4]", "True 1000000"],
            "hint": "counts = [0] * (max_value + 1); посчитайте вхождения; затем выпишите каждое значение v ровно counts[v] раз.",
        },
        {
            "id": "kth-largest",
            "mode": "func",
            "func": "kth_largest",
            "title": "k-й по величине",
            "statement": (
                "Напишите функцию kth_largest(nums, k): k-й по величине "
                "элемент списка (k = 1 — наибольший); одинаковые значения "
                "считаются отдельными элементами. 1 <= k <= len(nums). "
                "Подойдёт куча (heapq) или быстрый выбор."
            ),
            "starter": "import heapq\n\n\ndef kth_largest(nums, k):\n    pass\n",
            "tests": [
                {"args": [[3, 2, 1, 5, 6, 4], 2], "expected": 5},
                {"args": [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], "expected": 4},
                {"args": [[7], 1], "expected": 7},
                {"args": [[1, 1, 1], 3], "expected": 1},
            ],
            "hint": "heapq.nlargest(k, nums)[-1], либо куча размера k: храните k наибольших, наименьший из них — ответ.",
        },
        {
            "id": "sort-stable-two-keys",
            "mode": "func",
            "func": "sort_students",
            "title": "Устойчивая сортировка по двум ключам",
            "statement": (
                "Напишите функцию sort_students(students): students — список "
                "пар [имя, оценка]. Верните их по убыванию оценки; у равных "
                "оценок порядок остаётся таким, как во входном списке "
                "(устойчивость). Важно: ключ ровно один — оценка."
            ),
            "starter": "def sort_students(students):\n    pass\n",
            "tests": [
                {"args": [[["Аня", 4], ["Боря", 5], ["Вера", 4], ["Гоша", 5]]], "expected": [["Боря", 5], ["Гоша", 5], ["Аня", 4], ["Вера", 4]]},
                {"args": [[]], "expected": []},
                {"args": [[["Я", 3]]], "expected": [["Я", 3]]},
                {"args": [[["б", 1], ["а", 1]]], "expected": [["б", 1], ["а", 1]]},
            ],
            "hint": "sorted(students, key=lambda s: s[1], reverse=True) — устойчивость сохраняется и с reverse.",
        },
    ],
    4: [
        {
            "id": "two-sum-hash",
            "mode": "stdout",
            "title": "Два числа с суммой",
            "statement": (
                "Напишите функцию two_sum(nums, target): индексы двух разных "
                "элементов с суммой target — кортеж (i, j), i < j. Ответ в "
                "тестах единственный. Нужно O(n): проверка подаёт 200 000 "
                "чисел."
            ),
            "starter": "def two_sum(nums, target):\n    pass\n",
            "driver": (
                "print(two_sum([2, 7, 11, 15], 9), two_sum([3, 2, 4], 6), two_sum([3, 3], 6))\n"
                "big = list(range(200000))\nprint(two_sum(big, 399997))\n"
            ),
            "expected": ["(0, 1) (1, 2) (0, 1)", "(199998, 199999)"],
            "hint": "Идите слева направо, храните в словаре «значение → индекс»; для x ищите target - x среди уже просмотренных.",
        },
        {
            "id": "group-anagrams-hash",
            "mode": "func",
            "func": "group_anagrams",
            "title": "Группы анаграмм",
            "statement": (
                "Напишите функцию group_anagrams(words): список групп слов, "
                "состоящих из одних и тех же букв. Внутри группы слова по "
                "алфавиту, сами группы — по первому слову. Ключ словаря — "
                "отсортированные буквы слова."
            ),
            "starter": "def group_anagrams(words):\n    pass\n",
            "tests": [
                {"args": [["кот", "ток", "рот", "тор", "кто", "лес"]], "expected": [["кот", "кто", "ток"], ["лес"], ["рот", "тор"]]},
                {"args": [[]], "expected": []},
                {"args": [["а", "а"]], "expected": [["а", "а"]]},
            ],
            "hint": "groups[''.join(sorted(w))].append(w); в конце отсортируйте слова в группах и сами группы.",
        },
        {
            "id": "first-unique-char",
            "mode": "func",
            "func": "first_unique",
            "title": "Первый неповторяющийся символ",
            "statement": (
                "Напишите функцию first_unique(s): индекс первого символа, "
                "который встречается в строке ровно один раз, или -1."
            ),
            "starter": "def first_unique(s):\n    pass\n",
            "tests": [
                {"args": ["левел"], "expected": 2},
                {"args": ["аабб"], "expected": -1},
                {"args": [""], "expected": -1},
                {"args": ["ж"], "expected": 0},
                {"args": ["аббвга"], "expected": 3},
            ],
            "hint": "Первый проход — посчитать символы (Counter), второй — найти первый со счётом 1.",
        },
        {
            "id": "longest-consecutive",
            "mode": "stdout",
            "title": "Самая длинная цепочка подряд",
            "statement": (
                "Напишите функцию longest_run(nums): длина самой длинной "
                "последовательности последовательных чисел (по значению, не "
                "по позиции): для [100, 4, 200, 1, 3, 2] это 1-2-3-4, длина 4. "
                "Нужно O(n): проверка подаёт 300 000 перемешанных чисел."
            ),
            "starter": "def longest_run(nums):\n    pass\n",
            "driver": (
                "import random\nrandom.seed(2)\n"
                "print(longest_run([100, 4, 200, 1, 3, 2]), longest_run([]), longest_run([5]), longest_run([1, 1, 1]))\n"
                "big = list(range(300000))\nrandom.shuffle(big)\nprint(longest_run(big))\n"
            ),
            "expected": ["4 0 1 1", "300000"],
            "hint": "Положите числа в множество/словарь; цепочку начинайте только с числа, у которого нет x - 1, и растите вправо.",
        },
        {
            "id": "subarray-sum-k",
            "mode": "stdout",
            "title": "Подотрезки с суммой k",
            "statement": (
                "Напишите функцию count_subarrays(nums, k): сколько "
                "непрерывных подотрезков имеют сумму ровно k. Числа могут "
                "быть отрицательными. Префиксные суммы и словарь, O(n): "
                "проверка подаёт 200 000 чисел."
            ),
            "starter": "def count_subarrays(nums, k):\n    pass\n",
            "driver": (
                "print(count_subarrays([1, 1, 1], 2), count_subarrays([1, 2, 3], 3), count_subarrays([1, -1, 0], 0), count_subarrays([], 0))\n"
                "print(count_subarrays([0] * 200000, 0) == 200000 * 200001 // 2)\nprint(count_subarrays([1] * 200000, 100000))\n"
            ),
            "expected": ["2 2 3 0", "True", "100001"],
            "hint": "seen = {0: 1}; на каждом шаге prefix += x; ответ += seen.get(prefix - k, 0); seen[prefix] += 1.",
        },
        {
            "id": "top-k-frequent",
            "mode": "func",
            "func": "top_k",
            "title": "k самых частых",
            "statement": (
                "Напишите функцию top_k(nums, k): k самых частых чисел; при "
                "равной частоте — меньшее число раньше. Результат — список "
                "по убыванию частоты."
            ),
            "starter": "from collections import Counter\n\n\ndef top_k(nums, k):\n    pass\n",
            "tests": [
                {"args": [[1, 1, 1, 2, 2, 3], 2], "expected": [1, 2]},
                {"args": [[4, 4, 5, 5, 6], 2], "expected": [4, 5]},
                {"args": [[1], 1], "expected": [1]},
                {"args": [[3, 1, 2], 3], "expected": [1, 2, 3]},
            ],
            "hint": "sorted(counter, key=lambda x: (-counter[x], x))[:k].",
        },
        {
            "id": "lru-cache-class",
            "mode": "stdout",
            "title": "LRU-кеш",
            "statement": (
                "Опишите класс LRUCache(capacity): get(key) возвращает "
                "значение или -1 и помечает ключ «недавно использованным»; "
                "put(key, value) добавляет или обновляет и, если мест нет, "
                "выбрасывает давно неиспользованный. Обе операции — O(1) "
                "(OrderedDict). Проверка делает миллион операций."
            ),
            "starter": "from collections import OrderedDict\n\n\nclass LRUCache:\n    def __init__(self, capacity):\n        pass\n",
            "driver": (
                "c = LRUCache(2)\nc.put(1, 1)\nc.put(2, 2)\nprint(c.get(1))\nc.put(3, 3)\nprint(c.get(2))\nc.put(4, 4)\nprint(c.get(1), c.get(3), c.get(4))\n"
                "d = LRUCache(1)\nd.put(1, 10)\nd.put(1, 20)\nprint(d.get(1))\n"
                "big = LRUCache(1000)\nfor i in range(1000000):\n    big.put(i, i)\nprint(big.get(999999), big.get(0))\n"
            ),
            "expected": ["1", "-1", "-1 3 4", "20", "999999 -1"],
            "hint": "OrderedDict: move_to_end(key) при чтении и записи; popitem(last=False) удаляет самый старый.",
        },
        {
            "id": "word-pattern-bijection",
            "mode": "func",
            "func": "word_pattern",
            "title": "Шаблон слов",
            "statement": (
                "Напишите функцию word_pattern(pattern, words): True, если "
                "слова повторяются так же, как буквы шаблона (соответствие "
                "взаимно однозначное): pattern 'абба' и слова ['кот', "
                "'пёс', 'пёс', 'кот'] — True; 'абба' и ['кот', 'кот', 'кот', "
                "'кот'] — False."
            ),
            "starter": "def word_pattern(pattern, words):\n    pass\n",
            "tests": [
                {"args": ["абба", ["кот", "пёс", "пёс", "кот"]], "expected": True},
                {"args": ["абба", ["кот", "кот", "кот", "кот"]], "expected": False},
                {"args": ["аааа", ["кот", "пёс", "пёс", "кот"]], "expected": False},
                {"args": ["аб", ["кот"]], "expected": False},
                {"args": ["", []], "expected": True},
            ],
            "hint": "Два словаря: буква → слово и слово → буква; любое несовпадение — False; длины должны совпадать.",
        },
    ],
    5: [
        {
            "id": "two-sum-sorted-pointers",
            "mode": "stdout",
            "title": "Два указателя в отсортированном",
            "statement": (
                "Напишите функцию pair_with_sum(arr, target): в "
                "отсортированном по возрастанию списке найдите два разных "
                "элемента с суммой target и верните их индексы (i, j), i < "
                "j, либо None. Два указателя, O(n) времени и O(1) памяти: "
                "проверка подаёт миллион элементов."
            ),
            "starter": "def pair_with_sum(arr, target):\n    pass\n",
            "driver": (
                "print(pair_with_sum([1, 2, 4, 7, 11], 9), pair_with_sum([1, 2, 3], 10), pair_with_sum([], 1), pair_with_sum([5], 5))\n"
                "big = list(range(1000000))\nprint(pair_with_sum(big, 1999997), pair_with_sum(big, 3000000))\n"
            ),
            "expected": ["(1, 3) None None None", "(999998, 999999) None"],
            "hint": "i = 0, j = len - 1; сумма мала — i += 1, велика — j -= 1; пока i < j.",
        },
        {
            "id": "remove-duplicates-sorted",
            "mode": "stdout",
            "title": "Убрать повторы на месте",
            "statement": (
                "Напишите функцию dedupe(arr): в отсортированном списке "
                "оставьте по одному экземпляру каждого значения НА МЕСТЕ "
                "(два указателя: читающий и пишущий), не создавая второго "
                "списка. Функция возвращает новую длину k, а первые k "
                "элементов arr — уникальные значения."
            ),
            "starter": "def dedupe(arr):\n    pass\n",
            "driver": (
                "a = [1, 1, 2, 3, 3, 3, 4]\nk = dedupe(a)\nprint(k, a[:k])\nb = []\nprint(dedupe(b))\nc = [5, 5, 5]\nk = dedupe(c)\nprint(k, c[:k])\n"
                "big = sorted([i // 3 for i in range(900000)])\nk = dedupe(big)\nprint(k, big[:3], big[k - 1])\n"
            ),
            "expected": ["4 [1, 2, 3, 4]", "0", "1 [5]", "300000 [0, 1, 2] 299999"],
            "hint": "w = 1; для r в 1..n-1: если arr[r] != arr[w - 1]: arr[w] = arr[r]; w += 1. Вернуть w (для пустого — 0).",
        },
        {
            "id": "longest-unique-window",
            "mode": "stdout",
            "title": "Самая длинная подстрока без повторов",
            "statement": (
                "Напишите функцию longest_unique(s): длина самой длинной "
                "подстроки без повторяющихся символов. Скользящее окно, O(n): "
                "проверка подаёт строку из 500 000 символов."
            ),
            "starter": "def longest_unique(s):\n    pass\n",
            "driver": (
                "print(longest_unique('abcabcbb'), longest_unique('bbbbb'), longest_unique('pwwkew'), longest_unique(''), longest_unique('привет'))\n"
                "import string\nbig = (string.ascii_lowercase * 20000)[:500000]\nprint(longest_unique(big))\nprint(longest_unique('a' * 500000))\n"
            ),
            "expected": ["3 1 3 0 6", "26", "1"],
            "hint": "Словарь «символ → последний индекс» и левая граница окна: при повторе сдвиньте её на last[ch] + 1.",
        },
        {
            "id": "max-sum-window",
            "mode": "stdout",
            "title": "Окно фиксированной длины",
            "statement": (
                "Напишите функцию best_window(nums, k): наибольшая сумма k "
                "подряд идущих элементов (k <= len(nums), k >= 1). Не "
                "пересчитывайте сумму окна заново: сдвигайте её за O(1). "
                "Проверка — миллион элементов и окно в 100 000."
            ),
            "starter": "def best_window(nums, k):\n    pass\n",
            "driver": (
                "print(best_window([1, 4, 2, 10, 23, 3, 1, 0, 20], 4), best_window([5], 1), best_window([-1, -2, -3], 2))\n"
                "big = list(range(1000000))\nprint(best_window(big, 100000))\n"
            ),
            "expected": ["39 5 -3", "94999950000"],
            "hint": "Сумма первого окна, затем window += nums[i] - nums[i - k] и обновление максимума.",
        },
        {
            "id": "container-most-water",
            "mode": "stdout",
            "title": "Больше всего воды",
            "statement": (
                "Дан список высот вертикальных линий. Напишите функцию "
                "most_water(heights): наибольшая площадь прямоугольника "
                "между двумя линиями — ширина (разница индексов) на меньшую "
                "из высот. Два указателя, O(n): проверка подаёт 200 000 "
                "линий."
            ),
            "starter": "def most_water(heights):\n    pass\n",
            "driver": (
                "print(most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]), most_water([1, 1]), most_water([4, 3, 2, 1, 4]), most_water([5]))\n"
                "big = [min(i, 200000 - i) for i in range(200001)]\nprint(most_water(big))\n"
            ),
            "expected": ["49 1 16 0", "5000000000"],
            "hint": "Идите с обоих концов; всегда сдвигайте указатель у МЕНЬШЕЙ линии — большая её ширину не улучшит.",
        },
        {
            "id": "count-inversions",
            "mode": "stdout",
            "title": "Число инверсий",
            "statement": (
                "Напишите функцию count_inversions(arr): сколько пар (i, j) "
                "с i < j и arr[i] > arr[j]. Разделяй и властвуй (модификация "
                "сортировки слиянием), O(n log n): проверка подаёт 100 000 "
                "элементов в обратном порядке."
            ),
            "starter": "def count_inversions(arr):\n    pass\n",
            "driver": (
                "print(count_inversions([2, 4, 1, 3, 5]), count_inversions([1, 2, 3]), count_inversions([3, 2, 1]), count_inversions([]))\n"
                "n = 100000\nprint(count_inversions(list(range(n, 0, -1))) == n * (n - 1) // 2)\n"
            ),
            "expected": ["3 0 3 0", "True"],
            "hint": "При слиянии, если берём элемент ПРАВОЙ половины, он «перепрыгивает» все оставшиеся в левой: прибавляйте len(left) - i.",
        },
        {
            "id": "max-subarray-divide",
            "mode": "stdout",
            "title": "Лучший подотрезок: разделяй и властвуй",
            "statement": (
                "Напишите функцию best_sum(nums): наибольшая сумма "
                "непрерывного непустого подотрезка (список не пустой), но "
                "рекурсивно: лучший отрезок либо целиком слева, либо целиком "
                "справа, либо пересекает середину (тогда его можно найти "
                "за линейное время). Глубина рекурсии должна быть O(log n)."
            ),
            "starter": "def best_sum(nums):\n    pass\n",
            "driver": (
                "import sys\nsys.setrecursionlimit(200)\n"
                "print(best_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]), best_sum([-5]), best_sum([2, 3, -10, 4, 5]), best_sum([-3, -1, -2]))\n"
                "print(best_sum([1, -1] * 100000 + [5]))\n"
            ),
            "expected": ["6 -5 9 -1", "5"],
            "hint": "Разделите пополам; ответ = max(лучший слева, лучший справа, лучший суффикс слева + лучший префикс справа).",
        },
        {
            "id": "min-window-substring",
            "mode": "func",
            "func": "min_window_len",
            "title": "Минимальное окно",
            "statement": (
                "Напишите функцию min_window_len(s, t): длина самой короткой "
                "подстроки s, содержащей все символы t (с учётом кратности), "
                "либо 0, если такой нет. Скользящее окно с двумя "
                "указателями."
            ),
            "starter": "def min_window_len(s, t):\n    pass\n",
            "tests": [
                {"args": ["ADOBECODEBANC", "ABC"], "expected": 4},
                {"args": ["a", "a"], "expected": 1},
                {"args": ["a", "aa"], "expected": 0},
                {"args": ["abc", ""], "expected": 0},
                {"args": ["aaflslflsldkalskaaa", "aaa"], "expected": 3},
            ],
            "hint": "need = Counter(t); расширяйте правую границу, пока окно не покрывает need, затем сжимайте левую, обновляя минимум.",
        },
    ],
}
