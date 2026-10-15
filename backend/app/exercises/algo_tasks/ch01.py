"""Задачи книги «Алгоритмы и структуры данных»: глава 1."""

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
}
