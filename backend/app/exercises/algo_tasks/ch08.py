"""Задачи книги «Алгоритмы и структуры данных»: глава 8."""

TASKS: dict[int, list[dict]] = {
    8: [
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
}
