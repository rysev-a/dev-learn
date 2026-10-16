"""Задачи книги «Алгоритмы и структуры данных»: глава 15."""

TASKS: dict[int, list[dict]] = {
    15: [
        {
            "id": "graph-bfs-distances",
            "mode": "func",
            "func": "bfs_distances",
            "title": "Расстояния обходом в ширину",
            "statement": (
                "Напишите функцию bfs_distances(graph, start): graph — словарь "
                "«вершина → список соседей» (имена вершин — строки). Верните "
                "словарь «вершина → минимальное число рёбер от start» для "
                "всех достижимых вершин."
            ),
            "starter": "from collections import deque\n\n\ndef bfs_distances(graph, start):\n    pass\n",
            "tests": [
                {"args": [{"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}, "a"], "expected": {"a": 0, "b": 1, "c": 1, "d": 2}},
                {"args": [{"x": []}, "x"], "expected": {"x": 0}},
                {"args": [{"a": ["b"], "b": ["a"], "c": ["a"]}, "a"], "expected": {"a": 0, "b": 1}},
                {"args": [{"1": ["2"], "2": ["3"], "3": ["1"]}, "2"], "expected": {"2": 0, "3": 1, "1": 2}},
            ],
            "hint": "Очередь и словарь расстояний (он же «посещённые»): сосед получает dist[v] + 1, если ещё не посещён.",
        },
        {
            "id": "graph-components",
            "mode": "stdout",
            "title": "Компоненты связности",
            "statement": (
                "Напишите функцию count_components(graph): число компонент "
                "связности неориентированного графа (словарь «вершина → список "
                "соседей», каждое ребро записано в обе стороны). Проверка "
                "подаёт цепочку из 200 000 вершин, поэтому обход должен быть "
                "итеративным (рекурсия упадёт)."
            ),
            "starter": "def count_components(graph):\n    pass\n",
            "driver": (
                "print(count_components({'a': ['b'], 'b': ['a'], 'c': []}), count_components({}), count_components({'x': []}))\n"
                "n = 200000\ng = {i: [] for i in range(n)}\nfor i in range(n - 1):\n    g[i].append(i + 1)\n    g[i + 1].append(i)\nprint(count_components(g))\n"
                "g2 = {i: [] for i in range(n)}\nprint(count_components(g2))\n"
            ),
            "expected": ["2 0 1", "1", "200000"],
            "hint": "Для каждой непосещённой вершины запустите обход со стеком/очередью и увеличьте счётчик компонент.",
        },
        {
            "id": "graph-undirected-cycle",
            "mode": "func",
            "func": "has_cycle",
            "title": "Цикл в неориентированном графе",
            "statement": (
                "Напишите функцию has_cycle(graph): True, если в "
                "неориентированном графе (каждое ребро записано в обе "
                "стороны, петель и кратных рёбер нет) есть цикл. При обходе "
                "помните «родителя» вершины: возврат к нему циклом не "
                "считается."
            ),
            "starter": "def has_cycle(graph):\n    pass\n",
            "tests": [
                {"args": [{"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}], "expected": True},
                {"args": [{"a": ["b"], "b": ["a", "c"], "c": ["b"]}], "expected": False},
                {"args": [{}], "expected": False},
                {"args": [{"a": [], "b": ["c"], "c": ["b", "d", "e"], "d": ["c", "e"], "e": ["c", "d"]}], "expected": True},
            ],
            "hint": "DFS/BFS с (вершина, родитель): если сосед уже посещён и это не родитель — найден цикл.",
        },
        {
            "id": "graph-topological",
            "mode": "func",
            "func": "topo_order",
            "title": "Топологическая сортировка",
            "statement": (
                "Напишите функцию topo_order(graph): graph — ориентированный "
                "граф без циклов, «вершина → список тех, на кого указывает». "
                "Верните порядок вершин, в котором каждая идёт раньше всех "
                "своих потомков; из нескольких допустимых берите "
                "лексикографически наименьший (в алгоритме Кана выбирайте "
                "наименьшую готовую вершину — куча). Если есть цикл — верните "
                "пустой список."
            ),
            "starter": "import heapq\n\n\ndef topo_order(graph):\n    pass\n",
            "tests": [
                {"args": [{"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}], "expected": ["a", "b", "c", "d"]},
                {"args": [{"c": ["a"], "b": ["a"], "a": []}], "expected": ["b", "c", "a"]},
                {"args": [{"a": ["b"], "b": ["a"]}], "expected": []},
                {"args": [{}], "expected": []},
                {"args": [{"x": []}], "expected": ["x"]},
            ],
            "hint": "indegree каждой вершины; в куче — вершины с нулём; вынимайте, уменьшайте indegree соседей. Если выдали не все вершины — цикл.",
        },
        {
            "id": "graph-bipartite",
            "mode": "func",
            "func": "is_bipartite",
            "title": "Двудольный граф",
            "statement": (
                "Напишите функцию is_bipartite(graph): True, если вершины "
                "неориентированного графа можно раскрасить в два цвета так, "
                "чтобы концы каждого ребра были разного цвета. Граф может быть "
                "несвязным."
            ),
            "starter": "def is_bipartite(graph):\n    pass\n",
            "tests": [
                {"args": [{"a": ["b", "d"], "b": ["a", "c"], "c": ["b", "d"], "d": ["a", "c"]}], "expected": True},
                {"args": [{"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}], "expected": False},
                {"args": [{}], "expected": True},
                {"args": [{"a": [], "b": ["c"], "c": ["b"]}], "expected": True},
            ],
            "hint": "Обход с раскраской: сосед получает противоположный цвет; если у уже покрашенного соседа тот же цвет — граф не двудольный.",
        },
        {
            "id": "grid-islands",
            "mode": "stdout",
            "title": "Количество островов",
            "statement": (
                "Напишите функцию count_islands(grid): grid — список строк "
                "из '1' (суша) и '0' (вода). Остров — группа клеток суши, "
                "соединённых по горизонтали и вертикали. Верните число "
                "островов. Проверка подаёт поле 1000×1000, поэтому без "
                "рекурсии."
            ),
            "starter": "def count_islands(grid):\n    pass\n",
            "driver": (
                "print(count_islands(['11000', '11000', '00100', '00011']), count_islands([]), count_islands(['0']), count_islands(['1']))\n"
                "print(count_islands(['101', '010', '101']))\n"
                "big = ['1' * 1000 for _ in range(1000)]\nprint(count_islands(big))\n"
                "chess = [''.join('1' if (i + j) % 2 == 0 else '0' for j in range(1000)) for i in range(1000)]\nprint(count_islands(chess))\n"
            ),
            "expected": ["3 0 0 1", "5", "1", "500000"],
            "hint": "Для каждой клетки '1', которую ещё не видели, запустите обход (стек) по четырём направлениям и увеличьте счётчик.",
        },
        {
            "id": "grid-shortest-path",
            "mode": "stdout",
            "title": "Кратчайший путь в лабиринте",
            "statement": (
                "Напишите функцию maze_steps(grid): grid — список строк из "
                "'.' (проход) и '#' (стена). Минимальное число шагов из "
                "левого верхнего угла в правый нижний (шаг — на соседнюю "
                "клетку по горизонтали или вертикали) либо -1. Поле до "
                "501×501: нужен обход в ширину."
            ),
            "starter": "from collections import deque\n\n\ndef maze_steps(grid):\n    pass\n",
            "driver": (
                "print(maze_steps(['..#', '#..', '#..']), maze_steps(['.#', '#.']), maze_steps(['.']), maze_steps(['#.']), maze_steps([]))\n"
                "n = 500\nopen_field = ['.' * n for _ in range(n)]\nprint(maze_steps(open_field))\n"
                "n = 501\nsnake = []\nfor i in range(n):\n    row = ['.'] * n\n    if i % 2 == 1:\n        row = ['#'] * n\n        row[0 if i % 4 == 3 else n - 1] = '.'\n    snake.append(''.join(row))\nprint(maze_steps(snake))\n"
            ),
            "expected": ["4 -1 0 -1 -1", "998", "126000"],
            "hint": "Очередь клеток с расстоянием, список посещённых; соседей — только внутри поля и без стен.",
        },
        {
            "id": "union-find-class",
            "mode": "stdout",
            "title": "Система непересекающихся множеств",
            "statement": (
                "Опишите класс UnionFind(n): элементы 0..n-1, поначалу каждый "
                "в своём множестве. Методы: find(x) — представитель "
                "множества, union(a, b) — объединить, connected(a, b) и "
                "атрибут count — число множеств. Нужны сжатие путей и "
                "объединение по размеру: проверка делает миллион операций."
            ),
            "starter": "class UnionFind:\n    def __init__(self, n):\n        pass\n",
            "driver": (
                "u = UnionFind(6)\nu.union(0, 1)\nu.union(1, 2)\nu.union(4, 5)\nprint(u.connected(0, 2), u.connected(0, 4), u.count)\nu.union(2, 5)\nprint(u.connected(0, 4), u.count)\n"
                "n = 1000000\nbig = UnionFind(n)\nfor i in range(n - 1):\n    big.union(i, i + 1)\nprint(big.count, big.connected(0, n - 1))\n"
            ),
            "expected": ["True False 3", "True 2", "1 True"],
            "hint": "parent[i] = i; find с сжатием путей (итеративно!); union по размеру; при слиянии count -= 1.",
        },
    ],
}
