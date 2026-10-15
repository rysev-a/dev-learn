"""Задачи книги «Алгоритмы и структуры данных»: глава 13."""

TASKS: dict[int, list[dict]] = {
    13: [
        {
            "id": "dijkstra-dist",
            "mode": "stdout",
            "title": "Алгоритм Дейкстры",
            "statement": (
                "Напишите функцию dijkstra(graph, start): graph — словарь "
                "«вершина → {сосед: вес}» (веса неотрицательные), вершины — "
                "числа. Верните словарь «вершина → кратчайшее расстояние» "
                "для достижимых вершин. Нужна куча (heapq): проверка подаёт "
                "граф из 100 000 вершин и 300 000 рёбер."
            ),
            "starter": "import heapq\n\n\ndef dijkstra(graph, start):\n    pass\n",
            "driver": (
                "g = {1: {2: 7, 3: 9, 6: 14}, 2: {1: 7, 3: 10, 4: 15}, 3: {1: 9, 2: 10, 4: 11, 6: 2}, 4: {2: 15, 3: 11, 5: 6}, 5: {4: 6, 6: 9}, 6: {1: 14, 3: 2, 5: 9}}\n"
                "print(sorted(dijkstra(g, 1).items()))\nprint(dijkstra({1: {}}, 1), dijkstra({1: {2: 5}, 2: {}, 3: {}}, 1))\n"
                "import random\nrandom.seed(4)\nn = 100000\nbig = {i: {} for i in range(n)}\nfor i in range(n - 1):\n    big[i][i + 1] = 1\nfor _ in range(200000):\n    a, b = random.randrange(n), random.randrange(n)\n    if a != b:\n        big[a][b] = random.randint(1, 50)\n"
                "d = dijkstra(big, 0)\nprint(len(d), d[n - 1] <= n - 1, d[0])\n"
            ),
            "expected": ["[(1, 0), (2, 7), (3, 9), (4, 20), (5, 20), (6, 11)]", "{1: 0} {1: 0, 2: 5}", "100000 True 0"],
            "hint": "Куча пар (расстояние, вершина); при извлечении устаревшую запись (d > dist[v]) пропускайте; релаксация: dist[u] = dist[v] + w.",
        },
        {
            "id": "shortest-path-route",
            "mode": "func",
            "func": "shortest_route",
            "title": "Сам маршрут",
            "statement": (
                "Напишите функцию shortest_route(graph, start, goal): "
                "graph — словарь «вершина → {сосед: вес}» (строковые "
                "вершины, веса положительные). Верните кортеж (длина, "
                "список вершин пути от start до goal) либо None, если пути "
                "нет. Кратчайший путь в тестах единственный."
            ),
            "starter": "import heapq\n\n\ndef shortest_route(graph, start, goal):\n    pass\n",
            "tests": [
                {"args": [{"a": {"b": 1, "c": 4}, "b": {"c": 2, "d": 6}, "c": {"d": 3}, "d": {}}, "a", "d"], "expected": (6, ["a", "b", "c", "d"])},
                {"args": [{"a": {"b": 1}, "b": {}, "c": {}}, "a", "c"], "expected": None},
                {"args": [{"a": {}}, "a", "a"], "expected": (0, ["a"])},
                {"args": [{"a": {"b": 10, "c": 1}, "c": {"b": 1}, "b": {}}, "a", "b"], "expected": (2, ["a", "c", "b"])},
            ],
            "hint": "В Дейкстре храните prev[u] = v при каждом улучшении расстояния; путь восстанавливайте от goal по prev.",
        },
        {
            "id": "bellman-ford-neg",
            "mode": "func",
            "func": "bellman_ford",
            "title": "Беллман — Форд",
            "statement": (
                "Напишите функцию bellman_ford(n, edges, src): вершины "
                "0..n-1, edges — список троек [u, v, вес] (веса могут быть "
                "отрицательными). Верните список расстояний от src "
                "(None для недостижимых вершин) либо строку «цикл», если из "
                "src достижим цикл отрицательного веса."
            ),
            "starter": "def bellman_ford(n, edges, src):\n    pass\n",
            "tests": [
                {"args": [5, [[0, 1, 6], [0, 2, 7], [1, 2, 8], [1, 3, 5], [1, 4, -4], [2, 3, -3], [2, 4, 9], [3, 1, -2], [4, 3, 7]], 0], "expected": [0, 2, 7, 4, -2]},
                {"args": [3, [[0, 1, 1], [1, 2, -1], [2, 1, -1]], 0], "expected": "цикл"},
                {"args": [3, [[1, 2, 5]], 0], "expected": [0, None, None]},
                {"args": [1, [], 0], "expected": [0]},
            ],
            "hint": "n - 1 раз релаксируйте все рёбра; ещё один проход, который что-то улучшил, означает отрицательный цикл.",
        },
        {
            "id": "floyd-warshall-matrix",
            "mode": "func",
            "func": "all_pairs",
            "title": "Все пары вершин",
            "statement": (
                "Напишите функцию all_pairs(n, edges): вершины 0..n-1, "
                "edges — тройки [u, v, вес] ориентированного графа "
                "(неотрицательные веса). Верните матрицу n×n кратчайших "
                "расстояний (алгоритм Флойда — Уоршелла); недостижимо — None, "
                "расстояние до себя — 0."
            ),
            "starter": "def all_pairs(n, edges):\n    pass\n",
            "tests": [
                {"args": [3, [[0, 1, 4], [1, 2, 1], [0, 2, 7]]], "expected": [[0, 4, 5], [None, 0, 1], [None, None, 0]]},
                {"args": [1, []], "expected": [[0]]},
                {"args": [2, []], "expected": [[0, None], [None, 0]]},
                {"args": [3, [[0, 1, 1], [1, 0, 1], [1, 2, 2]]], "expected": [[0, 1, 3], [1, 0, 2], [None, None, 0]]},
            ],
            "hint": "dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) для k, i, j в тройном цикле; бесконечность — float('inf'), в конце заменить на None.",
        },
        {
            "id": "kruskal-mst",
            "mode": "stdout",
            "title": "Минимальный остов: Краскал",
            "statement": (
                "Напишите функцию mst_weight(n, edges): вершины 0..n-1, "
                "edges — тройки (u, v, вес) неориентированного графа. "
                "Верните вес минимального остовного дерева, либо None, если "
                "граф несвязен. Алгоритм Краскала: сортировка рёбер и "
                "система непересекающихся множеств. Проверка — 200 000 "
                "рёбер."
            ),
            "starter": "def mst_weight(n, edges):\n    pass\n",
            "driver": (
                "print(mst_weight(4, [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 4), (1, 3, 5)]), mst_weight(3, [(0, 1, 5)]), mst_weight(1, []), mst_weight(2, [(0, 1, 7), (0, 1, 3)]))\n"
                "import random\nrandom.seed(8)\nn = 50000\nedges = [(i, i + 1, 1) for i in range(n - 1)] + [(random.randrange(n), random.randrange(n), random.randint(2, 100)) for _ in range(200000)]\n"
                "print(mst_weight(n, edges))\n"
            ),
            "expected": ["7 None 0 3", "49999"],
            "hint": "Отсортируйте рёбра по весу; берите ребро, если его концы в разных множествах (union), и прибавляйте вес; в конце проверьте, что взято n - 1 ребро.",
        },
        {
            "id": "prim-mst",
            "mode": "func",
            "func": "prim_weight",
            "title": "Минимальный остов: Прим",
            "statement": (
                "Напишите функцию prim_weight(graph): graph — словарь "
                "«вершина → {сосед: вес}» связного неориентированного графа "
                "(рёбра записаны в обе стороны, вершины — строки). Верните "
                "вес минимального остова алгоритмом Прима с кучей. Пустой "
                "граф — 0."
            ),
            "starter": "import heapq\n\n\ndef prim_weight(graph):\n    pass\n",
            "tests": [
                {"args": [{"a": {"b": 1, "c": 3}, "b": {"a": 1, "c": 2, "d": 5}, "c": {"a": 3, "b": 2, "d": 4}, "d": {"b": 5, "c": 4}}], "expected": 7},
                {"args": [{}], "expected": 0},
                {"args": [{"x": {}}], "expected": 0},
                {"args": [{"a": {"b": 10}, "b": {"a": 10}}], "expected": 10},
            ],
            "hint": "Начните с любой вершины; в куче — рёбра, ведущие из дерева наружу; вынимайте минимальное, и если конец ещё не в дереве — добавляйте.",
        },
        {
            "id": "network-delay",
            "mode": "func",
            "func": "network_delay",
            "title": "Время распространения сигнала",
            "statement": (
                "Сеть из узлов 1..n. times — список троек [u, v, w]: сигнал "
                "идёт от u к v за w. Сигнал отправляют из узла k. Напишите "
                "функцию network_delay(times, n, k): через сколько "
                "времени сигнал дойдёт до ВСЕХ узлов, либо -1, если дойдёт не "
                "до всех."
            ),
            "starter": "import heapq\n\n\ndef network_delay(times, n, k):\n    pass\n",
            "tests": [
                {"args": [[[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2], "expected": 2},
                {"args": [[[1, 2, 1]], 2, 1], "expected": 1},
                {"args": [[[1, 2, 1]], 2, 2], "expected": -1},
                {"args": [[], 1, 1], "expected": 0},
                {"args": [[[1, 2, 5], [1, 3, 1], [3, 2, 1]], 3, 1], "expected": 2},
            ],
            "hint": "Дейкстра от k; ответ — максимальное расстояние, если достигнуты все n узлов.",
        },
        {
            "id": "cheapest-flight-k-stops",
            "mode": "func",
            "func": "cheapest_flight",
            "title": "Дешёвый перелёт с ограничением пересадок",
            "statement": (
                "Напишите функцию cheapest_flight(n, flights, src, dst, k): "
                "города 0..n-1, flights — тройки [откуда, куда, цена]. "
                "Минимальная цена перелёта из src в dst с не более чем k "
                "пересадками (то есть не более k + 1 перелётов) либо -1. "
                "Подсказка: Беллман — Форд ровно на k + 1 итераций с копией "
                "расстояний на каждом шаге."
            ),
            "starter": "def cheapest_flight(n, flights, src, dst, k):\n    pass\n",
            "tests": [
                {"args": [4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1], "expected": 700},
                {"args": [3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1], "expected": 200},
                {"args": [3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0], "expected": 500},
                {"args": [2, [], 0, 1, 5], "expected": -1},
            ],
            "hint": "dist = [inf] * n; dist[src] = 0; k + 1 раз: new = dist[:]; для каждого перелёта улучшайте new[v] по dist[u] + цена; dist = new.",
        },
    ],
}
