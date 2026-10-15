"""Задачи книги «Алгоритмы и структуры данных»: глава 6."""

from app.exercises.algo_tasks._kept import KEPT

_NEW: dict[int, list[dict]] = {
    6: [
        {
            "id": "pair-with-difference",
            "mode": "func",
            "func": "has_pair_diff",
            "title": "Пара с заданной разностью",
            "statement": (
                "Дан отсортированный по возрастанию список a и число k ≥ 0. "
                "Напишите функцию has_pair_diff(a, k): True, если есть два РАЗНЫХ "
                "индекса i ≠ j, для которых a[j] − a[i] == k. Два указателя идут в "
                "одну сторону. Проверка подаёт 300 000 чисел."
            ),
            "starter": "def has_pair_diff(a, k):\n    pass\n",
            "tests": [
                {"args": [[1, 3, 5, 8, 12], 4], "expected": True},
                {"args": [[1, 3, 5, 8, 12], 6], "expected": False},
                {"args": [[1, 2, 3], 0], "expected": False},
                {"args": [[2, 2, 3], 0], "expected": True},
                {"args": [[], 1], "expected": False},
                {"args": [[5], 0], "expected": False},
                {"args": [[1, 5], 4], "expected": True},
                {"args": [[1, 2, 4, 7, 11], 10], "expected": True},
            ],
            "hint": "Идём указателем j вправо, а i подтягиваем, пока разность больше k. Не забывайте про i == j: пара из элемента с самим собой не считается (важно при k = 0).",
        },
        {
            "id": "valid-palindrome-one-deletion",
            "mode": "func",
            "func": "valid_palindrome",
            "title": "Палиндром с одним удалением",
            "statement": (
                "Напишите функцию valid_palindrome(s): True, если строка становится "
                "палиндромом после удаления не более одного символа. Идите "
                "указателями навстречу; на первом несовпадении проверьте два "
                "варианта: пропустить левый или правый символ. Проверка подаёт "
                "строки по 200 000 символов."
            ),
            "starter": "def valid_palindrome(s):\n    pass\n",
            "tests": [
                {"args": ["aba"], "expected": True},
                {"args": ["abca"], "expected": True},
                {"args": ["abc"], "expected": False},
                {"args": [""], "expected": True},
                {"args": ["a"], "expected": True},
                {"args": ["deeee"], "expected": True},
                {"args": ["eedede"], "expected": True},
                {"args": ["abbca"], "expected": True},
                {"args": ["cbbcc"], "expected": True},
            ],
            "hint": "Внутренняя функция ok(i, j) проверяет палиндромность среза; при первом несовпадении ответ — ok(i + 1, j) or ok(i, j − 1).",
        },
        {
            "id": "remove-duplicates-at-most-two",
            "mode": "stdout",
            "title": "Не больше двух копий",
            "statement": (
                "Отсортированный список a. Напишите функцию remove_dups_two(a): "
                "оставьте каждое значение не более чем в двух экземплярах, на "
                "месте, сохранив порядок; верните новую длину k (первые k элементов "
                "— результат, хвост неважен). Проверка подаёт 500 000 элементов: "
                "сдвиги через pop и del не успеют."
            ),
            "starter": "def remove_dups_two(a):\n    pass\n",
            "driver": (
                "a = [1, 1, 1, 2, 2, 3]\n"
                "k = remove_dups_two(a)\n"
                "print(k, a[:k])\n"
                "a = [0, 0, 1, 1, 1, 1, 2, 3, 3]\n"
                "k = remove_dups_two(a)\n"
                "print(k, a[:k])\n"
                "b = []\n"
                "print(remove_dups_two(b))\n"
                "c = [5]\n"
                "k = remove_dups_two(c)\n"
                "print(k, c[:k])\n"
                "big = [i // 4 for i in range(500000)]\n"
                "k = remove_dups_two(big)\n"
                "print(k, big[:7], big[k - 3:k])\n"
            ),
            "expected": ["5 [1, 1, 2, 2, 3]", "7 [0, 0, 1, 1, 2, 3, 3]", "0", "1 [5]", "250000 [0, 0, 1, 1, 2, 2, 3] [124998, 124999, 124999]"],
            "hint": "Условие записи: либо в результате меньше двух элементов, либо x отличается от a[k − 2] — предпоследнего записанного.",
        },
        {
            "id": "sorted-squares",
            "mode": "func",
            "func": "sorted_squares",
            "title": "Отсортированные квадраты",
            "statement": (
                "Дан отсортированный по возрастанию список целых a (есть "
                "отрицательные). Напишите функцию sorted_squares(a): квадраты "
                "элементов по возрастанию за O(n): два указателя с концов, большие "
                "по модулю идут в результат с конца."
            ),
            "starter": "def sorted_squares(a):\n    pass\n",
            "tests": [
                {"args": [[-4, -1, 0, 3, 10]], "expected": [0, 1, 9, 16, 100]},
                {"args": [[-7, -3, 2, 3, 11]], "expected": [4, 9, 9, 49, 121]},
                {"args": [[1, 2, 3]], "expected": [1, 4, 9]},
                {"args": [[-3, -2, -1]], "expected": [1, 4, 9]},
                {"args": [[]], "expected": []},
                {"args": [[0]], "expected": [0]},
                {"args": [[-5, 5]], "expected": [25, 25]},
            ],
            "hint": "Самый большой квадрат — у одного из концов. Сравните |a[lo]| и |a[hi]|, запишите больший в результат с конца и сдвиньте соответствующий указатель.",
        },
        {
            "id": "intersect-sorted",
            "mode": "stdout",
            "title": "Пересечение отсортированных",
            "statement": (
                "Два отсортированных по возрастанию списка. Напишите функцию "
                "intersect(a, b): их пересечение с учётом кратности (общие значения "
                "столько раз, сколько они есть в обоих списках), по возрастанию. "
                "Проверка подаёт по 500 000 элементов: поиск через x in b не "
                "успеет."
            ),
            "starter": "def intersect(a, b):\n    pass\n",
            "driver": (
                "print(intersect([1, 2, 2, 3, 5], [2, 2, 4, 5]), intersect([], [1]), intersect([1, 2], [3, 4]), intersect([1, 1, 1], [1, 1]))\n"
                "a = list(range(0, 1000000, 2))\n"
                "b = list(range(0, 1000000, 3))\n"
                "r = intersect(a, b)\n"
                "print(len(r), r[:4], r[-2:])\n"
            ),
            "expected": ["[2, 2, 5] [] [] [1, 1]", "166667 [0, 6, 12, 18] [999990, 999996]"],
            "hint": "Два указателя: равны — в ответ и оба вперёд; меньший — вперёд. Цикл while i < len(a) and j < len(b).",
        },
        {
            "id": "is-subsequence",
            "mode": "stdout",
            "title": "Подпоследовательность",
            "statement": (
                "Напишите функцию is_subsequence(s, t): True, если все символы s "
                "встречаются в t в том же порядке (не обязательно подряд). Пустая s "
                "— всегда подпоследовательность. Проверка подаёт t длиной 2 000 "
                "000."
            ),
            "starter": "def is_subsequence(s, t):\n    pass\n",
            "driver": (
                "print(is_subsequence(\"ace\", \"abcde\"), is_subsequence(\"aec\", \"abcde\"), is_subsequence(\"\", \"abc\"), is_subsequence(\"a\", \"\"), is_subsequence(\"abc\", \"abc\"))\n"
                "t = \"ab\" * 1000000\n"
                "print(is_subsequence(\"a\" * 1000000, t), is_subsequence(\"a\" * 1000001, t), is_subsequence(\"ba\" * 999999, t))\n"
            ),
            "expected": ["True False True False True", "True False True"],
            "hint": "i — позиция в s. Идём по t; если текущий символ равен s[i], сдвигаем i. В конце i == len(s).",
        },
        {
            "id": "interval-intersections",
            "mode": "func",
            "func": "interval_intersection",
            "title": "Пересечения интервалов",
            "statement": (
                "Даны два списка замкнутых интервалов [начало, конец]: внутри "
                "каждого списка интервалы не пересекаются и отсортированы. Напишите "
                "функцию interval_intersection(A, B): список всех непустых "
                "пересечений интервалов (в виде списков [начало, конец]) в порядке "
                "возрастания. Касание в одной точке — пересечение."
            ),
            "starter": "def interval_intersection(A, B):\n    pass\n",
            "tests": [
                {"args": [[[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]], "expected": [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]},
                {"args": [[], [[1, 3]]], "expected": []},
                {"args": [[[1, 3], [5, 9]], []], "expected": []},
                {"args": [[[1, 7]], [[3, 10]]], "expected": [[3, 7]]},
                {"args": [[[1, 3]], [[3, 5]]], "expected": [[3, 3]]},
                {"args": [[[1, 2]], [[3, 4]]], "expected": []},
            ],
            "hint": "Пересечение двух интервалов: [max(начал), min(концов)] — если max ≤ min. Двигайте указатель того интервала, который закончился раньше.",
        },
        {
            "id": "trap-rain-water",
            "mode": "stdout",
            "title": "Дождевая вода",
            "statement": (
                "Дана высота столбиков h. После дождя между ними застаивается вода. "
                "Напишите функцию trap(h): общий объём воды (каждый столбик шириной "
                "1). Два указателя с концов и два максимума: двигайте сторону с "
                "меньшим максимумом. Проверка подаёт 500 000 столбиков."
            ),
            "starter": "def trap(h):\n    pass\n",
            "driver": (
                "print(trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), trap([4, 2, 0, 3, 2, 5]), trap([]), trap([3]), trap([1, 2, 3]), trap([3, 0, 3]))\n"
                "h = [(i * 37) % 101 for i in range(500000)]\n"
                "print(trap(h))\n"
            ),
            "expected": ["6 9 0 0 0 3", "24999535"],
            "hint": "Вода над столбиком = (меньший из максимумов слева и справа) − высота. Если h[lo] < h[hi], граница слева — максимум слева; считаем воду на lo и сдвигаем его.",
        },
        {
            "id": "sort-colors",
            "mode": "stdout",
            "title": "Сортировка цветов",
            "statement": (
                "В списке a лежат только 0, 1 и 2. Напишите функцию sort_colors(a): "
                "отсортируйте на месте за один проход и O(1) памяти (голландский "
                "флаг); ничего не возвращайте. Встроенный sort и счёт количеств "
                "запрещены по смыслу задачи, но проверка видит только результат. "
                "Проверка подаёт 1 000 000 элементов."
            ),
            "starter": "def sort_colors(a):\n    pass\n",
            "driver": (
                "a = [2, 0, 2, 1, 1, 0]\n"
                "sort_colors(a)\n"
                "print(a)\n"
                "for t in ([0], [], [1, 0], [2, 2, 2], [1, 2, 0, 1]):\n"
                "    t = list(t)\n"
                "    sort_colors(t)\n"
                "    print(t)\n"
                "n = 1000000\n"
                "big = [(i * 7919) % 3 for i in range(n)]\n"
                "sort_colors(big)\n"
                "print(big[0], big[n // 2], big[-1], big == sorted(big))\n"
            ),
            "expected": ["[0, 0, 1, 1, 2, 2]", "[0]", "[]", "[0, 1]", "[2, 2, 2]", "[0, 1, 1, 2]", "0 1 2 True"],
            "hint": "lo — граница нулей, hi — граница двойки, mid идёт вперёд. Ноль меняем с lo (и lo, mid вперёд), двойку — с hi (только hi назад), единицу — пропускаем.",
        },
        {
            "id": "sort-by-parity",
            "mode": "stdout",
            "title": "Чётные вперёд",
            "statement": (
                "Напишите функцию sort_by_parity(a): переставьте элементы списка на "
                "месте так, чтобы все чётные числа стояли раньше всех нечётных "
                "(порядок внутри групп не важен); ничего не возвращайте. Два "
                "указателя навстречу: левый ищет нечётное, правый — чётное, и они "
                "меняются. Проверка подаёт 1 000 000 элементов."
            ),
            "starter": "def sort_by_parity(a):\n    pass\n",
            "driver": (
                "def check(src):\n"
                "    a = list(src)\n"
                "    sort_by_parity(a)\n"
                "    k = sum(1 for x in a if x % 2 == 0)\n"
                "    return sorted(a) == sorted(src) and all(x % 2 == 0 for x in a[:k]) and all(x % 2 == 1 for x in a[k:])\n"
                "\n"
                "\n"
                "print(check([3, 1, 2, 4]), check([]), check([1]), check([2, 4]), check([1, 3, 5]), check([2, 1, 4, 3, 6, 5]))\n"
                "print(check([(i * 7919) % 1009 for i in range(1000000)]))\n"
            ),
            "expected": ["True True True True True True", "True"],
            "hint": "Пока i < j: чётное слева — шагаем вправо; нечётное справа — шагаем влево; иначе (слева нечётное, справа чётное) меняем и сдвигаем оба.",
        },
        {
            "id": "three-sum",
            "mode": "stdout",
            "title": "Тройки с нулевой суммой",
            "statement": (
                "Напишите функцию three_sum(a): все различные тройки значений "
                "(a[i], a[j], a[k]) с i < j < k и нулевой суммой. Каждая тройка — "
                "список по возрастанию; тройки — по возрастанию. Одинаковые тройки "
                "не повторяются. Время O(n²): сортировка и два указателя. Проверка "
                "подаёт 2 500 элементов — куб не успеет."
            ),
            "starter": "def three_sum(a):\n    pass\n",
            "driver": (
                "print(three_sum([-1, 0, 1, 2, -1, -4]), three_sum([0, 0, 0, 0]), three_sum([1, 2, 3]), three_sum([]), three_sum([-2, 0, 1, 1, 2]))\n"
                "a = [(i * 7919) % 2001 - 1000 for i in range(2500)]\n"
                "r = three_sum(a)\n"
                "print(len(r), r[:3], all(sum(t) == 0 for t in r))\n"
            ),
            "expected": ["[[-1, -1, 2], [-1, 0, 1]] [[0, 0, 0]] [] [] [[-2, 0, 2], [-2, 1, 1]]", "500246 [[-1000, 0, 1000], [-1000, 1, 999], [-1000, 2, 998]] True"],
            "hint": "Сортировка; для каждого i (кроме повторяющихся значений) указатели lo = i + 1 и hi = n − 1. После найденной тройки сдвиньте оба и пропустите повторы lo.",
        },
        {
            "id": "three-sum-closest",
            "mode": "stdout",
            "title": "Ближайшая сумма трёх",
            "statement": (
                "Напишите функцию three_sum_closest(a, target): сумму трёх "
                "элементов (на трёх разных позициях), наиболее близкую к target. "
                "Гарантируется ровно один ответ. Проверка подаёт 2 000 элементов."
            ),
            "starter": "def three_sum_closest(a, target):\n    pass\n",
            "driver": (
                "print(three_sum_closest([-1, 2, 1, -4], 1), three_sum_closest([0, 0, 0], 1), three_sum_closest([1, 1, 1, 0], -100), three_sum_closest([1, 2, 5, 10, 11], 12))\n"
                "a = [(i * 104729) % 100003 for i in range(2000)]\n"
                "print(three_sum_closest(a, 150000), three_sum_closest(a, 5))\n"
            ),
            "expected": ["2 0 2 13", "150002 263"],
            "hint": "Как three_sum, но запоминайте сумму, ближайшую к target. Если s < target — lo вправо, если больше — hi влево.",
        },
        {
            "id": "count-pairs-sum-at-most",
            "mode": "stdout",
            "title": "Пары с суммой не больше k",
            "statement": (
                "Напишите функцию count_pairs_le(a, k): число пар индексов i < j с "
                "a[i] + a[j] ≤ k. Список неотсортирован. Отсортируйте копию и "
                "посчитайте двумя указателями. Проверка подаёт 200 000 элементов: "
                "перебор пар не успеет."
            ),
            "starter": "def count_pairs_le(a, k):\n    pass\n",
            "driver": (
                "print(count_pairs_le([1, 2, 3, 4, 5, 6], 7), count_pairs_le([5, 1, 4], 5), count_pairs_le([], 3), count_pairs_le([2], 5), count_pairs_le([3, 3, 3], 6), count_pairs_le([3, 3, 3], 5))\n"
                "a = [(i * 7919) % 10007 for i in range(200000)]\n"
                "print(count_pairs_le(a, 10000), count_pairs_le(a, 20000))\n"
            ),
            "expected": ["9 1 0 0 3 0", "9988845001 19999884460"],
            "hint": "Если b[lo] + b[hi] ≤ k, то b[lo] подходит со всеми элементами от lo + 1 до hi — прибавьте hi − lo и сдвиньте lo; иначе hi − 1.",
        },
        {
            "id": "find-duplicate-floyd",
            "mode": "stdout",
            "title": "Дубликат без изменения массива",
            "statement": (
                "В списке a из n + 1 чисел значения лежат в диапазоне 1…n, и ровно "
                "одно число повторяется (возможно, несколько раз). Напишите функцию "
                "find_duplicate(a): повторяющееся число. Список менять нельзя, "
                "дополнительной памяти — O(1): смотрите на список как на связный "
                "(позиция i ведёт в позицию a[i]) и ищите вход в цикл по Флойду. "
                "Проверка подаёт 500 001 число."
            ),
            "starter": "def find_duplicate(a):\n    pass\n",
            "driver": (
                "for a in ([1, 3, 4, 2, 2], [3, 1, 3, 4, 2], [1, 1], [2, 2, 2, 2, 2], [1, 4, 4, 2, 4]):\n"
                "    b = list(a)\n"
                "    print(find_duplicate(a), a == b)\n"
                "n = 500000\n"
                "big = list(range(1, n + 1)) + [123457]\n"
                "x = 17\n"
                "for i in range(n):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    j = x % (n + 1)\n"
                "    big[i], big[j] = big[j], big[i]\n"
                "save = list(big)\n"
                "print(find_duplicate(big), big == save)\n"
            ),
            "expected": ["2 True", "3 True", "1 True", "2 True", "4 True", "123457 True"],
            "hint": "Старт с индекса 0 (в него никто не ведёт). Первый заход: slow = a[slow], fast = a[a[fast]] до встречи. Второй: slow с нуля, оба по одному шагу — встретятся во входе в цикл.",
        },
        {
            "id": "backspace-compare",
            "mode": "stdout",
            "title": "Сравнение с возвратом каретки",
            "statement": (
                "Символ '#' означает «удалить предыдущий символ» (в пустой строке "
                "ничего не происходит). Напишите функцию backspace_compare(s, t): "
                "равны ли строки после применения всех '#'. Решение за O(1) "
                "дополнительной памяти: идите по обеим строкам справа налево с "
                "двумя указателями. Проверка подаёт строки по 1 000 000 символов."
            ),
            "starter": "def backspace_compare(s, t):\n    pass\n",
            "driver": (
                "print(backspace_compare(\"ab#c\", \"ad#c\"), backspace_compare(\"ab##\", \"c#d#\"), backspace_compare(\"a#c\", \"b\"), backspace_compare(\"\", \"a#\"), backspace_compare(\"a##c\", \"#a#c\"), backspace_compare(\"xywrrmp\", \"xywrrmu#p\"))\n"
                "s = \"ab#\" * 333333 + \"c\"\n"
                "t = \"a\" * 0 + \"ab#\" * 333333 + \"c\"\n"
                "print(backspace_compare(s, t), backspace_compare(s, t[:-1] + \"d\"))\n"
            ),
            "expected": ["True True False True True True", "True False"],
            "hint": "Функция next_valid(x, i) идёт влево, считая '#' и пропуская столько обычных символов; возвращает позицию следующего «живого» символа или −1.",
        },
        {
            "id": "boats",
            "mode": "stdout",
            "title": "Лодки",
            "statement": (
                "Люди с весами w, каждая лодка выдерживает не более limit и несёт "
                "не более двух человек (вес каждого не больше limit). Напишите "
                "функцию num_boats(w, limit): наименьшее число лодок. Сортировка и "
                "два указателя: самый тяжёлый садится в лодку, к нему берём самого "
                "лёгкого, если вместе проходят. Проверка подаёт 300 000 человек."
            ),
            "starter": "def num_boats(w, limit):\n    pass\n",
            "driver": (
                "print(num_boats([1, 2], 3), num_boats([3, 2, 2, 1], 3), num_boats([3, 5, 3, 4], 5), num_boats([], 5), num_boats([4], 5), num_boats([2, 2, 2], 4))\n"
                "w = [(i * 7919) % 5000 + 1 for i in range(300000)]\n"
                "print(num_boats(w, 5000), num_boats(w, 6000), num_boats(w, 2600))\n"
            ),
            "expected": ["1 3 4 0 1 2", "150030 150000 222030"],
            "hint": "После сортировки самого тяжёлого посадим в любом случае (hi − 1); самого лёгкого берём с ним, если сумма не больше limit (lo + 1). Каждый шаг — одна лодка.",
        },
    ],
}

_BY_ID = {t["id"]: t for t in _NEW[6]} | KEPT

TASKS: dict[int, list[dict]] = {
    6: [_BY_ID[i] for i in (
        "two-sum-sorted-pointers",
        "pair-with-difference",
        "is-palindrome-two-pointers",
        "valid-palindrome-one-deletion",
        "remove-duplicates-sorted",
        "remove-duplicates-at-most-two",
        "sorted-squares",
        "intersect-sorted",
        "is-subsequence",
        "interval-intersections",
        "container-most-water",
        "trap-rain-water",
        "sort-colors",
        "sort-by-parity",
        "three-sum",
        "three-sum-closest",
        "count-pairs-sum-at-most",
        "find-duplicate-floyd",
        "backspace-compare",
        "boats",
    )],
}
