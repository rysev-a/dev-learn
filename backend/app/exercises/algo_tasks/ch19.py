"""Задачи книги «Алгоритмы и структуры данных»: глава 19."""

TASKS: dict[int, list[dict]] = {
    19: [
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
