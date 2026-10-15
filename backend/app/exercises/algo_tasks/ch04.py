"""Задачи книги «Алгоритмы и структуры данных»: глава 4."""

TASKS: dict[int, list[dict]] = {
    4: [
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
}
