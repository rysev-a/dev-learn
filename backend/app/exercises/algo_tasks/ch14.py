"""Задачи книги «Алгоритмы и структуры данных»: глава 14."""

TASKS: dict[int, list[dict]] = {
    14: [
        {
            "id": "dp-climb-stairs",
            "mode": "stdout",
            "title": "Лестница",
            "statement": (
                "Напишите функцию climb(n): сколькими способами можно "
                "подняться на n-ю ступень, делая шаги по 1 или по 2 ступени. "
                "Наивная рекурсия делает экспоненциально много вызовов: "
                "проверка подаёт n = 5000 (ответ огромный, Python справится)."
            ),
            "starter": "def climb(n):\n    pass\n",
            "driver": "print(climb(1), climb(2), climb(5), climb(45))\nprint(climb(5000) % 1000000007)\n",
            "expected": ["1 2 8 1836311903", "419609281"],
            "hint": "ways[i] = ways[i - 1] + ways[i - 2] — это числа Фибоначчи; храните только две последние.",
        },
        {
            "id": "dp-coin-change",
            "mode": "stdout",
            "title": "Размен монет",
            "statement": (
                "Напишите функцию min_coins(coins, amount): наименьшее число "
                "монет номиналов coins (каждого номинала — сколько угодно), "
                "дающих сумму amount; если набрать нельзя — -1; для суммы 0 — "
                "0. Динамическое программирование по сумме: проверка подаёт "
                "сумму 100 000."
            ),
            "starter": "def min_coins(coins, amount):\n    pass\n",
            "driver": (
                "print(min_coins([1, 2, 5], 11), min_coins([2], 3), min_coins([1], 0), min_coins([186, 419, 83, 408], 6249), min_coins([], 5))\n"
                "print(min_coins([1, 5, 10, 25], 100000), min_coins([7, 13], 100000))\n"
            ),
            "expected": ["3 -1 0 20 -1", "4000 7696"],
            "hint": "best[0] = 0; best[a] = min(best[a - c] + 1 для монет c <= a); бесконечность — «набрать нельзя».",
        },
        {
            "id": "dp-knapsack-01",
            "mode": "stdout",
            "title": "Рюкзак 0/1",
            "statement": (
                "Напишите функцию knapsack(weights, values, capacity): "
                "наибольшая суммарная ценность предметов, которые влезают в "
                "рюкзак (каждый предмет — один раз). Таблица по вместимости, "
                "O(n · capacity) времени и O(capacity) памяти: проверка "
                "подаёт 100 предметов и вместимость 10 000."
            ),
            "starter": "def knapsack(weights, values, capacity):\n    pass\n",
            "driver": (
                "print(knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7), knapsack([], [], 10), knapsack([5], [10], 4), knapsack([2, 2], [3, 4], 4))\n"
                "import random\nrandom.seed(9)\nw = [random.randint(10, 400) for _ in range(100)]\nv = [random.randint(1, 1000) for _ in range(100)]\nprint(knapsack(w, v, 10000), knapsack(w, v, 1000))\n"
            ),
            "expected": ["9 0 0 7", "41394 13942"],
            "hint": "dp = [0] * (capacity + 1); для каждого предмета идите по вместимости ОТ БОЛЬШЕЙ К МЕНЬШЕЙ: dp[c] = max(dp[c], dp[c - w] + v).",
        },
        {
            "id": "dp-lcs",
            "mode": "stdout",
            "title": "Наибольшая общая подпоследовательность",
            "statement": (
                "Напишите функцию lcs_length(a, b): длина наибольшей общей "
                "подпоследовательности двух строк (символы идут в том же "
                "порядке, но не обязательно подряд). Таблица динамического "
                "программирования: проверка подаёт строки по 2000 символов."
            ),
            "starter": "def lcs_length(a, b):\n    pass\n",
            "driver": (
                "print(lcs_length('abcde', 'ace'), lcs_length('abc', 'def'), lcs_length('', 'x'), lcs_length('привет', 'превет'))\n"
                "import random\nrandom.seed(6)\nx = ''.join(random.choice('abcd') for _ in range(2000))\ny = ''.join(random.choice('abcd') for _ in range(2000))\nprint(lcs_length(x, x), lcs_length(x, y))\n"
            ),
            "expected": ["3 0 0 5", "2000 1301"],
            "hint": "dp[i][j]: если a[i-1] == b[j-1] — dp[i-1][j-1] + 1, иначе max(dp[i-1][j], dp[i][j-1]); хватит двух строк таблицы.",
        },
        {
            "id": "dp-edit-distance",
            "mode": "stdout",
            "title": "Расстояние редактирования",
            "statement": (
                "Напишите функцию edit_distance(a, b): минимальное число "
                "операций (вставка, удаление или замена одного символа), "
                "превращающих строку a в b (расстояние Левенштейна). "
                "Проверка подаёт строки по 1500 символов."
            ),
            "starter": "def edit_distance(a, b):\n    pass\n",
            "driver": (
                "print(edit_distance('kitten', 'sitting'), edit_distance('', 'abc'), edit_distance('abc', ''), edit_distance('abc', 'abc'), edit_distance('кот', 'код'))\n"
                "import random\nrandom.seed(2)\nx = ''.join(random.choice('abc') for _ in range(1500))\ny = x[:700] + 'zz' + x[702:]\nprint(edit_distance(x, y), edit_distance(x, x))\n"
            ),
            "expected": ["3 3 3 0 1", "2 0"],
            "hint": "dp[i][j] = min(удаление: dp[i-1][j] + 1, вставка: dp[i][j-1] + 1, замена: dp[i-1][j-1] + (a[i-1] != b[j-1])).",
        },
        {
            "id": "dp-lis-nlogn",
            "mode": "stdout",
            "title": "Самая длинная возрастающая подпоследовательность",
            "statement": (
                "Напишите функцию lis_length(nums): длина самой длинной "
                "строго возрастающей подпоследовательности. Решение за "
                "O(n log n) (список «хвостов» и бинарный поиск bisect): "
                "проверка подаёт 100 000 чисел, а O(n²) не успеет."
            ),
            "starter": "import bisect\n\n\ndef lis_length(nums):\n    pass\n",
            "driver": (
                "print(lis_length([10, 9, 2, 5, 3, 7, 101, 18]), lis_length([]), lis_length([7, 7, 7]), lis_length([1, 2, 3, 4]))\n"
                "import random\nrandom.seed(1)\nbig = [random.randint(0, 10 ** 9) for _ in range(100000)]\nprint(lis_length(big))\nprint(lis_length(list(range(100000))), lis_length(list(range(100000, 0, -1))))\n"
            ),
            "expected": ["4 0 1 4", "627", "100000 1"],
            "hint": "tails[k] — наименьший возможный хвост возрастающей подпоследовательности длины k + 1; для x найдите bisect_left(tails, x) и замените или допишите.",
        },
        {
            "id": "dp-house-robber",
            "mode": "stdout",
            "title": "Грабитель домов",
            "statement": (
                "Напишите функцию rob(money): наибольшая сумма, которую "
                "можно собрать из домов на улице, не заходя в два соседних "
                "(money[i] — деньги в i-м доме, все неотрицательные). "
                "Достаточно двух переменных: проверка подаёт миллион домов."
            ),
            "starter": "def rob(money):\n    pass\n",
            "driver": (
                "print(rob([1, 2, 3, 1]), rob([2, 7, 9, 3, 1]), rob([]), rob([5]), rob([2, 1, 1, 2]))\n"
                "print(rob([3] * 1000000), rob(list(range(1000000))))\n"
            ),
            "expected": ["4 12 0 5 4", "1500000 250000000000"],
            "hint": "take, skip = 0, 0; для x: take, skip = skip + x, max(take, skip).",
        },
        {
            "id": "dp-partition-subset",
            "mode": "stdout",
            "title": "Разбиение на две равные суммы",
            "statement": (
                "Напишите функцию can_split(nums): True, если числа списка "
                "(натуральные) можно разделить на две группы с равной "
                "суммой. Задача о подмножестве с суммой total/2: множество "
                "достижимых сумм. Проверка: 200 чисел, суммы до 20 000."
            ),
            "starter": "def can_split(nums):\n    pass\n",
            "driver": (
                "print(can_split([1, 5, 11, 5]), can_split([1, 2, 3, 5]), can_split([]), can_split([2, 2]), can_split([7]))\n"
                "import random\nrandom.seed(12)\nnums = [random.randint(1, 200) for _ in range(200)]\nif sum(nums) % 2:\n    nums[0] += 1\nprint(can_split(nums))\nprint(can_split([1000] * 19 + [999]))\n"
            ),
            "expected": ["True False True True False", "True", "False"],
            "hint": "total нечётное → False; иначе reachable = {0}; для каждого x: добавляйте s + x, не превышая total // 2 — или битовая маска bits |= bits << x.",
        },
    ],
}
