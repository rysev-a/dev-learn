"""Задачи книги «Алгоритмы»: ch06_08."""

TASKS: dict[int, list[dict]] = {
    6: [
        {
            "id": "tree-inorder-iter",
            "mode": "stdout",
            "title": "Симметричный обход без рекурсии",
            "statement": (
                "Дан класс TreeNode (val, left, right). Напишите функцию "
                "inorder(root): список значений в симметричном порядке "
                "(левое поддерево, узел, правое), НЕ используя рекурсию — "
                "стек вручную. Проверка подаёт вырожденное дерево глубиной "
                "100 000, на котором рекурсия падает."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef inorder(root):\n    pass\n",
            "driver": (
                "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n"
                "print(inorder(build([4, 2, 6, 1, 3, 5, 7])), inorder(None), inorder(TreeNode(9)))\n"
                "print(inorder(build([1, None, 2, 3])))\n"
                "root = cur = TreeNode(0)\nfor i in range(1, 100000):\n    cur.left = TreeNode(i)\n    cur = cur.left\nres = inorder(root)\nprint(len(res), res[0], res[-1])\n"
            ),
            "expected": ["[1, 2, 3, 4, 5, 6, 7] [] [9]", "[1, 3, 2]", "100000 99999 0"],
            "hint": "stack = []; cur = root; while cur or stack: спускайтесь влево, кладя узлы в стек; затем pop, запись значения, переход вправо.",
        },
        {
            "id": "tree-max-depth",
            "mode": "stdout",
            "title": "Высота дерева",
            "statement": (
                "Дан класс TreeNode. Напишите функцию max_depth(root): "
                "количество узлов на самом длинном пути от корня до листа "
                "(у пустого дерева — 0). Обход в ширину по уровням: проверка "
                "подаёт цепочку из 100 000 узлов."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef max_depth(root):\n    pass\n",
            "driver": (
                "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n"
                "print(max_depth(build([3, 9, 20, None, None, 15, 7])), max_depth(None), max_depth(TreeNode(1)))\n"
                "root = cur = TreeNode(0)\nfor i in range(1, 100000):\n    cur.right = TreeNode(i)\n    cur = cur.right\nprint(max_depth(root))\n"
            ),
            "expected": ["3 0 1", "100000"],
            "hint": "Очередь (deque) с уровнями: обработайте все узлы текущего уровня, соберите детей, depth += 1.",
        },
        {
            "id": "tree-level-order",
            "mode": "stdout",
            "title": "Обход по уровням",
            "statement": (
                "Дан класс TreeNode. Напишите функцию level_order(root): "
                "список списков значений — по одному списку на каждый "
                "уровень, слева направо. Для пустого дерева — []."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef level_order(root):\n    pass\n",
            "driver": (
                "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n"
                "print(level_order(build([3, 9, 20, None, None, 15, 7])))\nprint(level_order(None), level_order(TreeNode(1)))\n"
                "print(level_order(build([1, 2, 3, 4, None, None, 5])))\n"
            ),
            "expected": ["[[3], [9, 20], [15, 7]]", "[] [[1]]", "[[1], [2, 3], [4, 5]]"],
            "hint": "На каждом шаге цикла возьмите ровно len(queue) узлов — это один уровень.",
        },
        {
            "id": "tree-valid-bst",
            "mode": "stdout",
            "title": "Это двоичное дерево поиска?",
            "statement": (
                "Дан класс TreeNode. Напишите функцию is_bst(root): True, "
                "если дерево — корректное двоичное дерево поиска: у каждого "
                "узла ВСЕ значения слева строго меньше, а справа строго "
                "больше. Недостаточно сравнить узел только с детьми: передавайте "
                "допустимые границы вниз."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef is_bst(root):\n    pass\n",
            "driver": (
                "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n"
                "print(is_bst(build([2, 1, 3])), is_bst(build([5, 1, 4, None, None, 3, 6])), is_bst(None))\n"
                "print(is_bst(build([5, 4, 6, None, None, 3, 7])), is_bst(build([2, 2, 2])))\n"
            ),
            "expected": ["True False True", "False False"],
            "hint": "check(node, low, high): None → True; low < val < high; левое — (low, val), правое — (val, high).",
        },
        {
            "id": "tree-lca",
            "mode": "stdout",
            "title": "Общий предок",
            "statement": (
                "Дан класс TreeNode (значения уникальны). Напишите функцию "
                "lca(root, p, q): значение самого глубокого узла, являющегося "
                "предком и для узла со значением p, и для узла со значением "
                "q (узел считается предком самого себя)."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef lca(root, p, q):\n    pass\n",
            "driver": (
                "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n"
                "t = build([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])\n"
                "print(lca(t, 5, 1), lca(t, 5, 4), lca(t, 6, 4), lca(t, 7, 8), lca(t, 3, 3))\n"
            ),
            "expected": ["3 5 5 3 3"],
            "hint": "Рекурсивно: если узел None или равен p или q — вернуть его; если нашлось и слева, и справа — это узел-ответ; иначе то, что нашлось.",
        },
        {
            "id": "tree-diameter",
            "mode": "stdout",
            "title": "Диаметр дерева",
            "statement": (
                "Дан класс TreeNode. Напишите функцию diameter(root): "
                "длина (в рёбрах) самого длинного пути между любыми двумя "
                "узлами; путь может не проходить через корень. Один обход: "
                "высоту поддеревьев считайте тем же проходом."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef diameter(root):\n    pass\n",
            "driver": (
                "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n"
                "print(diameter(build([1, 2, 3, 4, 5])), diameter(None), diameter(TreeNode(1)), diameter(build([1, 2])))\n"
                "print(diameter(build([1, 2, None, 3, None, 4])))\n"
            ),
            "expected": ["3 0 0 1", "3"],
            "hint": "dfs(node) возвращает высоту; по дороге обновляйте best = max(best, h_left + h_right).",
        },
        {
            "id": "tree-path-sum",
            "mode": "stdout",
            "title": "Путь с заданной суммой",
            "statement": (
                "Дан класс TreeNode. Напишите функцию has_path_sum(root, "
                "target): True, если есть путь от корня до ЛИСТА, сумма "
                "значений на котором равна target. Пустое дерево — False."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef has_path_sum(root, target):\n    pass\n",
            "driver": (
                "def build(vals):\n    if not vals or vals[0] is None:\n        return None\n    nodes = [TreeNode(v) if v is not None else None for v in vals]\n    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n        if n:\n            if kids:\n                n.left = kids.pop()\n            if kids:\n                n.right = kids.pop()\n    return nodes[0]\n"
                "t = build([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])\n"
                "print(has_path_sum(t, 22), has_path_sum(t, 26), has_path_sum(t, 5), has_path_sum(None, 0), has_path_sum(TreeNode(7), 7))\n"
            ),
            "expected": ["True True False False True"],
            "hint": "Уменьшайте target на val; в листе (нет детей) проверьте, что остаток равен нулю.",
        },
        {
            "id": "bst-insert",
            "mode": "stdout",
            "title": "Вставка в дерево поиска",
            "statement": (
                "Дан класс TreeNode. Напишите функцию insert(root, val): "
                "вставляет значение в двоичное дерево поиска (меньшие — "
                "влево, остальные — вправо) и возвращает корень. Для пустого "
                "дерева создайте узел. Итеративно: дерево бывает глубоким."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef insert(root, val):\n    pass\n",
            "driver": (
                "def inorder(n):\n    out, st = [], []\n    while n or st:\n        while n:\n            st.append(n)\n            n = n.left\n        n = st.pop()\n        out.append(n.val)\n        n = n.right\n    return out\n"
                "root = None\nfor v in [5, 3, 8, 1, 4, 7, 9, 3]:\n    root = insert(root, v)\nprint(inorder(root), root.val, root.left.val, root.right.val)\n"
                "chain = None\nfor v in range(20000):\n    chain = insert(chain, v)\nprint(len(inorder(chain)))\n"
            ),
            "expected": ["[1, 3, 3, 4, 5, 7, 8, 9] 5 3 8", "20000"],
            "hint": "cur = root; в цикле идите влево при val < cur.val, иначе вправо, пока не найдёте пустое место.",
        },
    ],
    7: [
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
    8: [
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
