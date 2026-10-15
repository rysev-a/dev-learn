"""Задачи книги «Алгоритмы»: ch09_10."""

TASKS: dict[int, list[dict]] = {
    9: [
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
    10: [
        {
            "id": "greedy-interval-scheduling",
            "mode": "func",
            "func": "max_meetings",
            "title": "Выбор максимума непересекающихся встреч",
            "statement": (
                "Напишите функцию max_meetings(intervals): intervals — список "
                "пар [начало, конец]. Верните наибольшее число встреч, "
                "которые можно провести, если две встречи не должны "
                "пересекаться (встреча, заканчивающаяся в момент t, не "
                "мешает той, что начинается в t). Жадный выбор: по самому "
                "раннему окончанию."
            ),
            "starter": "def max_meetings(intervals):\n    pass\n",
            "tests": [
                {"args": [[[1, 3], [2, 4], [3, 5], [0, 6], [5, 7], [8, 9], [5, 9]]], "expected": 4},
                {"args": [[]], "expected": 0},
                {"args": [[[1, 2], [1, 2], [1, 2]]], "expected": 1},
                {"args": [[[1, 10], [2, 3], [4, 5], [6, 7]]], "expected": 3},
            ],
            "hint": "Отсортируйте по концу; берите встречу, если её начало >= конца последней выбранной.",
        },
        {
            "id": "greedy-merge-intervals",
            "mode": "func",
            "func": "merge_intervals",
            "title": "Слияние отрезков",
            "statement": (
                "Напишите функцию merge_intervals(intervals): объедините "
                "пересекающиеся и касающиеся отрезки [начало, конец] и верните "
                "результат, отсортированный по началу."
            ),
            "starter": "def merge_intervals(intervals):\n    pass\n",
            "tests": [
                {"args": [[[1, 3], [2, 6], [8, 10], [15, 18]]], "expected": [[1, 6], [8, 10], [15, 18]]},
                {"args": [[[1, 4], [4, 5]]], "expected": [[1, 5]]},
                {"args": [[]], "expected": []},
                {"args": [[[5, 6], [1, 10], [2, 3]]], "expected": [[1, 10]]},
            ],
            "hint": "Сортировка по началу; текущий отрезок продлевайте, пока следующий начинается не позже его конца.",
        },
        {
            "id": "greedy-jump-game",
            "mode": "stdout",
            "title": "Прыжки по массиву",
            "statement": (
                "Напишите функцию can_reach(jumps): на i-й позиции можно "
                "прыгнуть вперёд на любое число клеток от 0 до jumps[i]. "
                "Можно ли добраться из первой клетки до последней? Жадно: "
                "следите за самой дальней достижимой клеткой. Проверка — "
                "миллион клеток."
            ),
            "starter": "def can_reach(jumps):\n    pass\n",
            "driver": (
                "print(can_reach([2, 3, 1, 1, 4]), can_reach([3, 2, 1, 0, 4]), can_reach([0]), can_reach([1, 0]), can_reach([0, 1]))\n"
                "print(can_reach([1] * 1000000), can_reach([1] * 999999 + [0]), can_reach([1] * 500000 + [0] + [1] * 499999))\n"
            ),
            "expected": ["True False True True False", "True True False"],
            "hint": "far = 0; для i: если i > far — тупик (False); far = max(far, i + jumps[i]); достигли last — True.",
        },
        {
            "id": "greedy-min-jumps",
            "mode": "stdout",
            "title": "Минимум прыжков",
            "statement": (
                "Напишите функцию min_jumps(jumps): наименьшее число "
                "прыжков из первой клетки в последнюю (на i-й клетке — "
                "прыжок на 0..jumps[i]); до конца гарантированно можно "
                "добраться. Жадно, за один проход: проверка подаёт миллион "
                "клеток."
            ),
            "starter": "def min_jumps(jumps):\n    pass\n",
            "driver": (
                "print(min_jumps([2, 3, 1, 1, 4]), min_jumps([2, 3, 0, 1, 4]), min_jumps([0]), min_jumps([1, 1, 1, 1]))\n"
                "print(min_jumps([1000] * 1000), min_jumps([1] * 1000000), min_jumps([5] + [1] * 5))\n"
            ),
            "expected": ["2 2 0 3", "1 999999 1"],
            "hint": "Границы «текущего прыжка»: end — предел текущего шага, far — самая дальняя достижимая; дошли до end — делаем прыжок, end = far.",
        },
        {
            "id": "greedy-gas-station",
            "mode": "func",
            "func": "start_station",
            "title": "Заправки по кругу",
            "statement": (
                "По кольцевой дороге стоят заправки: gas[i] — сколько топлива "
                "на i-й, cost[i] — сколько его тратится на переезд до "
                "следующей. Напишите функцию start_station(gas, cost): "
                "индекс заправки, с которой можно начать (с пустым баком) и "
                "объехать круг, либо -1. Такой индекс единственный. "
                "Один проход."
            ),
            "starter": "def start_station(gas, cost):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3, 4, 5], [3, 4, 5, 1, 2]], "expected": 3},
                {"args": [[2, 3, 4], [3, 4, 3]], "expected": -1},
                {"args": [[5], [4]], "expected": 0},
                {"args": [[5, 1, 2, 3, 4], [4, 4, 1, 5, 1]], "expected": 4},
            ],
            "hint": "Если суммарно топлива меньше расхода — -1. Иначе идите по кругу: когда баланс стал отрицательным, начало — со следующей заправки.",
        },
        {
            "id": "greedy-fractional-knapsack",
            "mode": "func",
            "func": "fractional_knapsack",
            "title": "Непрерывный рюкзак",
            "statement": (
                "Предметы можно дробить. Напишите функцию "
                "fractional_knapsack(items, capacity): items — пары "
                "[вес, ценность]. Верните наибольшую ценность, округлённую "
                "до двух знаков (round). Жадно: сначала предметы с наибольшей "
                "ценностью на единицу веса."
            ),
            "starter": "def fractional_knapsack(items, capacity):\n    pass\n",
            "tests": [
                {"args": [[[10, 60], [20, 100], [30, 120]], 50], "expected": 240.0},
                {"args": [[[5, 50]], 2], "expected": 20.0},
                {"args": [[], 10], "expected": 0.0},
                {"args": [[[1, 1], [2, 5]], 10], "expected": 6.0},
            ],
            "hint": "Отсортируйте по ценность/вес по убыванию; берите целиком, пока влезает, последний — долей.",
        },
        {
            "id": "greedy-huffman-cost",
            "mode": "func",
            "func": "huffman_cost",
            "title": "Стоимость кода Хаффмана",
            "statement": (
                "Напишите функцию huffman_cost(freqs): freqs — частоты "
                "символов. Верните суммарную стоимость оптимального "
                "префиксного кода: сумму длин кодов, взвешенную частотами "
                "(равна сумме всех слияний в алгоритме Хаффмана). Каждый "
                "шаг: берём две наименьшие частоты (куча), заменяем их "
                "суммой. Для одного символа — 0."
            ),
            "starter": "import heapq\n\n\ndef huffman_cost(freqs):\n    pass\n",
            "tests": [
                {"args": [[5, 9, 12, 13, 16, 45]], "expected": 224},
                {"args": [[1, 1]], "expected": 2},
                {"args": [[7]], "expected": 0},
                {"args": [[]], "expected": 0},
                {"args": [[1, 2, 3, 4]], "expected": 19},
            ],
            "hint": "heap = freqs; пока в куче больше одного: a, b = два наименьших; cost += a + b; вернуть a + b.",
        },
        {
            "id": "greedy-min-platforms",
            "mode": "stdout",
            "title": "Минимум платформ",
            "statement": (
                "Напишите функцию min_platforms(arrivals, departures): "
                "сколько платформ нужно вокзалу, чтобы ни один поезд не "
                "ждал. Поезд i стоит с arrivals[i] до departures[i] "
                "(если один уезжает, когда другой приезжает, платформа "
                "освобождается). Отсортируйте события и идите двумя "
                "указателями. Проверка — 200 000 поездов."
            ),
            "starter": "def min_platforms(arrivals, departures):\n    pass\n",
            "driver": (
                "print(min_platforms([900, 940, 950, 1100, 1500, 1800], [910, 1200, 1120, 1130, 1900, 2000]), min_platforms([], []), min_platforms([1], [2]), min_platforms([1, 2], [2, 3]))\n"
                "n = 200000\nprint(min_platforms(list(range(n)), [i + 5 for i in range(n)]), min_platforms(list(range(n)), [i + 1 for i in range(n)]))\n"
            ),
            "expected": ["3 0 1 1", "5 1"],
            "hint": "Отсортируйте обе последовательности; i, j: если arrivals[i] < departures[j] — нужна новая платформа (i += 1), иначе поезд уехал (j += 1); следите за максимумом.",
        },
    ],
}
