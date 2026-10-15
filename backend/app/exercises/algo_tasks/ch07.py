"""Задачи книги «Алгоритмы и структуры данных»: глава 7."""

from app.exercises.algo_tasks._kept import KEPT

_NEW: dict[int, list[dict]] = {
    7: [
        {
            "id": "find-anagrams",
            "mode": "stdout",
            "title": "Анаграммы в строке",
            "statement": (
                "Напишите функцию find_anagrams(s, p): список всех индексов i, где "
                "подстрока s[i:i+len(p)] — анаграмма строки p (по возрастанию). "
                "Окно шириной len(p) и счётчики символов; пересчёт при сдвиге за "
                "O(1). Проверка подаёт s длиной 300 000."
            ),
            "starter": "def find_anagrams(s, p):\n    pass\n",
            "driver": (
                "print(find_anagrams(\"cbaebabacd\", \"abc\"), find_anagrams(\"abab\", \"ab\"), find_anagrams(\"a\", \"ab\"), find_anagrams(\"aaa\", \"aa\"), find_anagrams(\"\", \"a\"))\n"
                "s = \"abc\" * 100000\n"
                "print(len(find_anagrams(s, \"cab\")), find_anagrams(s, \"abcc\")[:2])\n"
            ),
            "expected": ["[0, 6] [0, 1, 2] [] [0, 1] []", "299998 [2, 5]"],
            "hint": "Хранить два словаря счётчиков и в каждом сдвиге сравнивать их целиком — O(k) на шаг. Лучше держать matched — число букв, чьи счётчики сейчас совпадают с образцом, и обновлять его при добавлении и удалении буквы.",
        },
        {
            "id": "max-in-windows",
            "mode": "stdout",
            "title": "Максимум в каждом окне",
            "statement": (
                "Напишите функцию max_sliding(a, k): список максимумов всех окон "
                "длины k (слева направо). Монотонная очередь индексов "
                "(collections.deque) даёт O(n). Проверка: 400 000 элементов и окно "
                "20 000 — max(a[i:i+k]) в цикле не успеет."
            ),
            "starter": "from collections import deque\n\n\ndef max_sliding(a, k):\n    pass\n",
            "driver": (
                "print(max_sliding([1, 3, -1, -3, 5, 3, 6, 7], 3), max_sliding([1], 1), max_sliding([9, 11], 2), max_sliding([4, 3, 2, 1], 2), max_sliding([1, 2, 3, 4], 4))\n"
                "a = [(i * 7919) % 100003 for i in range(400000)]\n"
                "r = max_sliding(a, 20000)\n"
                "print(len(r), r[0], r[-1], sum(r) % 1000003)\n"
            ),
            "expected": ["[3, 3, 5, 5, 6, 7] [1] [11] [4, 3, 2] [4]", "380001 100001 99990 40951"],
            "hint": "В очереди — индексы, значения по убыванию. Новый x выталкивает с конца всех, кто ≤ x. С головы убирайте индекс, вышедший из окна (dq[0] ≤ i − k). Ответ окна — a[dq[0]].",
        },
        {
            "id": "longest-ones-flip-k",
            "mode": "stdout",
            "title": "Единицы с заменами",
            "statement": (
                "Дан список из 0 и 1 и число k. Напишите функцию longest_ones(a, "
                "k): длина самого длинного подряд идущего куска, в котором после "
                "замены не более k нулей на единицы остаются одни единицы (то есть "
                "в куске не больше k нулей). Проверка подаёт 500 000 элементов."
            ),
            "starter": "def longest_ones(a, k):\n    pass\n",
            "driver": (
                "print(longest_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2), longest_ones([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3), longest_ones([], 1), longest_ones([0, 0], 0), longest_ones([1], 0))\n"
                "a = [0 if (i * 7919) % 11 == 0 else 1 for i in range(500000)]\n"
                "print(longest_ones(a, 0), longest_ones(a, 5), longest_ones(a, 1000))\n"
            ),
            "expected": ["6 10 0 0 1", "10 65 11010"],
            "hint": "Окно с числом нулей не больше k. Расширяем правую границу; если нулей стало больше k, сжимаем левую, пока не станет допустимо. Ответ — максимальная ширина окна.",
        },
        {
            "id": "min-subarray-len",
            "mode": "stdout",
            "title": "Самый короткий подмассив с суммой",
            "statement": (
                "Напишите функцию min_subarray_len(target, a): наименьшая длина "
                "подряд идущего куска натуральных чисел a с суммой не меньше "
                "target, или 0, если такого нет. Окно переменной длины. Проверка "
                "подаёт 500 000 чисел."
            ),
            "starter": "def min_subarray_len(target, a):\n    pass\n",
            "driver": (
                "print(min_subarray_len(7, [2, 3, 1, 2, 4, 3]), min_subarray_len(4, [1, 4, 4]), min_subarray_len(11, [1, 1, 1, 1, 1, 1, 1, 1]), min_subarray_len(5, [5]), min_subarray_len(3, []))\n"
                "a = [(i * 7919) % 100 + 1 for i in range(500000)]\n"
                "print(min_subarray_len(1000, a), min_subarray_len(10 ** 9, a), min_subarray_len(5000000, a))\n"
            ),
            "expected": ["2 1 0 1 0", "18 0 99008"],
            "hint": "Расширяйте правую границу, накапливая сумму. Пока сумма ≥ target — фиксируйте длину и сжимайте левую (вычитая её элемент).",
        },
        {
            "id": "char-replacement",
            "mode": "stdout",
            "title": "Замена символов",
            "statement": (
                "Дана строка s из заглавных латинских букв и число k. Напишите "
                "функцию char_replacement(s, k): длина самой длинной подстроки, "
                "которую можно превратить в строку из одинаковых букв не более чем "
                "k заменами. Окно, в котором «длина окна − частота самой частой "
                "буквы ≤ k». Проверка подаёт 300 000 символов."
            ),
            "starter": "def char_replacement(s, k):\n    pass\n",
            "driver": (
                "print(char_replacement(\"ABAB\", 2), char_replacement(\"AABABBA\", 1), char_replacement(\"\", 3), char_replacement(\"A\", 0), char_replacement(\"ABC\", 0))\n"
                "s = \"\".join(\"ABCD\"[(i * i) % 4 + (i // 7) % 2] if (i * 31) % 5 else \"A\" for i in range(300000))\n"
                "print(char_replacement(s, 0), char_replacement(s, 10), char_replacement(s, 1000))\n"
            ),
            "expected": ["4 4 0 1 1", "3 21 1753"],
            "hint": "Достаточно хранить максимальную частоту в окне (её можно не уменьшать при сжатии — ответ от этого не портится). Окно допустимо, пока длина − максимальная частота ≤ k.",
        },
        {
            "id": "product-less-than-k",
            "mode": "stdout",
            "title": "Подмассивы с малым произведением",
            "statement": (
                "Дан список натуральных чисел a и число k. Напишите функцию "
                "count_product_less(a, k): число подряд идущих непустых "
                "подмассивов, произведение элементов которых строго меньше k. Окно: "
                "для каждого правого конца считайте, сколько левых начал допустимо. "
                "Проверка подаёт 300 000 чисел."
            ),
            "starter": "def count_product_less(a, k):\n    pass\n",
            "driver": (
                "print(count_product_less([10, 5, 2, 6], 100), count_product_less([1, 2, 3], 0), count_product_less([1, 1, 1], 2), count_product_less([], 5), count_product_less([5], 5), count_product_less([5], 6))\n"
                "a = [(i * 7919) % 5 + 1 for i in range(300000)]\n"
                "print(count_product_less(a, 1000), count_product_less(a, 10 ** 6))\n"
            ),
            "expected": ["8 0 6 0 0 1", "2039979 4139911"],
            "hint": "Правый конец r; пока произведение окна ≥ k — сжимаем левую границу. Допустимых подмассивов, заканчивающихся в r, ровно r − l + 1.",
        },
        {
            "id": "fruit-baskets",
            "mode": "stdout",
            "title": "Фрукты в двух корзинах",
            "statement": (
                "Вдоль ряда деревьев растут фрукты разных видов (список f). Вы "
                "идёте слева направо и можете собирать фрукты лишь двух разных "
                "видов. Напишите функцию total_fruit(f): длина самого длинного "
                "подряд идущего куска ряда, в котором не больше двух различных "
                "видов. Проверка подаёт 500 000 деревьев."
            ),
            "starter": "def total_fruit(f):\n    pass\n",
            "driver": (
                "print(total_fruit([1, 2, 1]), total_fruit([0, 1, 2, 2]), total_fruit([1, 2, 3, 2, 2]), total_fruit([3, 3, 3, 1, 2, 1, 1, 2, 3, 3, 4]), total_fruit([]), total_fruit([5]))\n"
                "f = [(i // 50) % 7 if i % 3 else (i // 70) % 5 for i in range(500000)]\n"
                "print(total_fruit(f), total_fruit([i % 2 for i in range(500000)]))\n"
            ),
            "expected": ["3 3 4 5 0 1", "101 500000"],
            "hint": "Окно и словарь видов → количество. Когда видов стало больше двух, сжимайте слева, удаляя вид из словаря при нуле.",
        },
        {
            "id": "hanoi-moves",
            "mode": "stdout",
            "title": "Ханойские башни",
            "statement": (
                "Напишите функцию hanoi(n): список ходов (из, в) для перекладывания "
                "n дисков со стержня 'A' на 'C' через 'B' (можно класть меньший "
                "диск на больший, а не наоборот). Ходы — кортежи ('A', 'C'). "
                "Разделяй и властвуй: n−1 дисков на запасной, самый большой на "
                "цель, n−1 дисков на цель. Для n = 0 — пустой список."
            ),
            "starter": "def hanoi(n):\n    pass\n",
            "driver": (
                "print(hanoi(0), hanoi(1), hanoi(2), hanoi(3))\n"
                "m = hanoi(18)\n"
                "print(len(m), m[0], m[-1], m[len(m) // 2])\n"
                "pegs = {\"A\": list(range(10, 0, -1)), \"B\": [], \"C\": []}\n"
                "ok = True\n"
                "for a, c in hanoi(10):\n"
                "    d = pegs[a].pop()\n"
                "    if pegs[c] and pegs[c][-1] < d:\n"
                "        ok = False\n"
                "    pegs[c].append(d)\n"
                "print(ok, pegs[\"C\"] == list(range(10, 0, -1)), len(pegs[\"A\"]), len(pegs[\"B\"]))\n"
            ),
            "expected": ["[] [('A', 'C')] [('A', 'B'), ('A', 'C'), ('B', 'C')] [('A', 'C'), ('A', 'B'), ('C', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('A', 'C')]", "262143 ('A', 'B') ('B', 'C') ('A', 'C')", "True True 0 0"],
            "hint": "Внутренняя рекурсивная функция go(k, откуда, через, куда): k − 1 дисков откуда→через, ход откуда→куда, k − 1 дисков через→куда.",
        },
        {
            "id": "segment-tree-class",
            "mode": "stdout",
            "title": "Дерево отрезков",
            "statement": (
                "Реализуйте класс SegmentTree(a): построение по списку чисел и два "
                "метода: query(l, r) — сумма a[l..r] включительно, update(i, v) — "
                "присвоить a[i] = v. Обе операции — O(log n). Проверка подаёт 100 "
                "000 элементов и по 100 000 запросов и обновлений: сумма срезом на "
                "каждый запрос не успеет."
            ),
            "starter": "class SegmentTree:\n    def __init__(self, a):\n        self.n = len(a)\n        self.t = [0] * (2 * self.n)\n        # построить дерево\n\n    def update(self, i, v):\n        pass\n\n    def query(self, l, r):\n        pass\n",
            "driver": (
                "st = SegmentTree([5, 3, 7, 1, 4, 6, 2, 8])\n"
                "print(st.query(0, 7), st.query(1, 6), st.query(3, 3), st.query(2, 4))\n"
                "st.update(3, 5)\n"
                "print(st.query(0, 7), st.query(2, 4), st.query(3, 3))\n"
                "one = SegmentTree([9])\n"
                "print(one.query(0, 0))\n"
                "one.update(0, 4)\n"
                "print(one.query(0, 0))\n"
                "n = 100000\n"
                "a = [(i * 7919) % 1000 for i in range(n)]\n"
                "st = SegmentTree(a)\n"
                "x = 5\n"
                "total = 0\n"
                "for i in range(100000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    l = x % n\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    r = l + x % (n - l)\n"
                "    if i % 2:\n"
                "        st.update(l, x % 1000)\n"
                "    else:\n"
                "        total += st.query(l, r)\n"
                "print(total, st.query(0, n - 1))\n"
            ),
            "expected": ["36 23 1 12", "40 16 5", "9", "4", "622797724702 50004502"],
            "hint": "Нижний уровень массива t — сами значения (позиции n…2n−1), родитель узла i — i // 2, t[i] = t[2i] + t[2i+1]. В query идите l и r вверх: нечётный левый край берём и сдвигаем, нечётный правый — отступаем и берём.",
        },
    ],
}

_BY_ID = {t["id"]: t for t in _NEW[7]} | KEPT

TASKS: dict[int, list[dict]] = {
    7: [_BY_ID[i] for i in (
        "longest-unique-window",
        "max-sum-window",
        "find-anagrams",
        "min-subarray-len",
        "longest-ones-flip-k",
        "fruit-baskets",
        "char-replacement",
        "product-less-than-k",
        "min-window-substring",
        "max-in-windows",
        "hanoi-moves",
        "count-inversions",
        "max-subarray-divide",
        "segment-tree-class",
    )],
}
