"""Задачи книги «Алгоритмы и структуры данных»: глава 8."""

from app.exercises.algo_tasks._kept import KEPT

_NEW: dict[int, list[dict]] = {
    8: [
        {
            "id": "tree-preorder-iter",
            "mode": "stdout",
            "title": "Прямой обход без рекурсии",
            "statement": (
                "Дан класс TreeNode (val, left, right). Напишите функцию "
                "preorder(root): список значений в прямом порядке (узел, левое, "
                "правое) без рекурсии — со своим стеком. Проверка подаёт цепочку из "
                "100 000 узлов."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef preorder(root):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    if not vals or vals[0] is None:\n"
                "        return None\n"
                "    nodes = [TreeNode(v) if v is not None else None for v in vals]\n"
                "    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n"
                "        if n:\n"
                "            if kids:\n"
                "                n.left = kids.pop()\n"
                "            if kids:\n"
                "                n.right = kids.pop()\n"
                "    return nodes[0]\n"
                "\n"
                "\n"
                "def levels(root):\n"
                "    out, cur = [], [root] if root else []\n"
                "    while cur:\n"
                "        out.append([n.val for n in cur])\n"
                "        cur = [c for n in cur for c in (n.left, n.right) if c]\n"
                "    return out\n"
                "\n"
                "\n"
                "def chain(n, side=\"left\"):\n"
                "    root = cur = TreeNode(0)\n"
                "    for i in range(1, n):\n"
                "        nxt = TreeNode(i)\n"
                "        setattr(cur, side, nxt)\n"
                "        cur = nxt\n"
                "    return root\n"
                "\n"
                "\n"
                "print(preorder(build([4, 2, 6, 1, 3, 5, 7])), preorder(None), preorder(TreeNode(9)), preorder(build([1, None, 2, 3])))\n"
                "r = preorder(chain(100000))\n"
                "print(len(r), r[0], r[-1])\n"
            ),
            "expected": ["[4, 2, 1, 3, 6, 5, 7] [] [9] [1, 2, 3]", "100000 0 99999"],
            "hint": "Стек с корнем. Снимаем узел, записываем значение, кладём правого ребёнка, затем левого — чтобы левый вышел раньше.",
        },
        {
            "id": "tree-postorder-iter",
            "mode": "stdout",
            "title": "Обратный обход без рекурсии",
            "statement": (
                "Дан класс TreeNode. Напишите функцию postorder(root): значения в "
                "обратном порядке (левое, правое, узел) без рекурсии. Подсказка: "
                "обратный порядок — это «узел, правое, левое», развёрнутый. "
                "Проверка подаёт цепочку из 100 000 узлов."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef postorder(root):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    if not vals or vals[0] is None:\n"
                "        return None\n"
                "    nodes = [TreeNode(v) if v is not None else None for v in vals]\n"
                "    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n"
                "        if n:\n"
                "            if kids:\n"
                "                n.left = kids.pop()\n"
                "            if kids:\n"
                "                n.right = kids.pop()\n"
                "    return nodes[0]\n"
                "\n"
                "\n"
                "def levels(root):\n"
                "    out, cur = [], [root] if root else []\n"
                "    while cur:\n"
                "        out.append([n.val for n in cur])\n"
                "        cur = [c for n in cur for c in (n.left, n.right) if c]\n"
                "    return out\n"
                "\n"
                "\n"
                "def chain(n, side=\"left\"):\n"
                "    root = cur = TreeNode(0)\n"
                "    for i in range(1, n):\n"
                "        nxt = TreeNode(i)\n"
                "        setattr(cur, side, nxt)\n"
                "        cur = nxt\n"
                "    return root\n"
                "\n"
                "\n"
                "print(postorder(build([4, 2, 6, 1, 3, 5, 7])), postorder(None), postorder(TreeNode(9)), postorder(build([1, None, 2, 3])))\n"
                "r = postorder(chain(100000, \"right\"))\n"
                "print(len(r), r[0], r[-1])\n"
            ),
            "expected": ["[1, 3, 2, 5, 7, 6, 4] [] [9] [3, 2, 1]", "100000 99999 0"],
            "hint": "Тот же стек, что и для прямого, но детей кладём в обратном порядке (сначала левого), а итоговый список разворачиваем.",
        },
        {
            "id": "tree-zigzag",
            "mode": "stdout",
            "title": "Обход зигзагом",
            "statement": (
                "Дан класс TreeNode. Напишите функцию zigzag(root): список уровней, "
                "где первый уровень идёт слева направо, второй — справа налево, "
                "третий снова слева направо и так далее. Пустое дерево — []."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef zigzag(root):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    if not vals or vals[0] is None:\n"
                "        return None\n"
                "    nodes = [TreeNode(v) if v is not None else None for v in vals]\n"
                "    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n"
                "        if n:\n"
                "            if kids:\n"
                "                n.left = kids.pop()\n"
                "            if kids:\n"
                "                n.right = kids.pop()\n"
                "    return nodes[0]\n"
                "\n"
                "\n"
                "def levels(root):\n"
                "    out, cur = [], [root] if root else []\n"
                "    while cur:\n"
                "        out.append([n.val for n in cur])\n"
                "        cur = [c for n in cur for c in (n.left, n.right) if c]\n"
                "    return out\n"
                "\n"
                "\n"
                "def chain(n, side=\"left\"):\n"
                "    root = cur = TreeNode(0)\n"
                "    for i in range(1, n):\n"
                "        nxt = TreeNode(i)\n"
                "        setattr(cur, side, nxt)\n"
                "        cur = nxt\n"
                "    return root\n"
                "\n"
                "\n"
                "print(zigzag(build([3, 9, 20, None, None, 15, 7])), zigzag(None), zigzag(TreeNode(1)), zigzag(build([1, 2, 3, 4, None, None, 5])))\n"
            ),
            "expected": ["[[3], [20, 9], [15, 7]] [] [[1]] [[1], [3, 2], [4, 5]]"],
            "hint": "Обычный обход по уровням, а у каждого второго уровня список значений разворачивается.",
        },
        {
            "id": "tree-right-view",
            "mode": "stdout",
            "title": "Вид справа",
            "statement": (
                "Дан класс TreeNode. Напишите функцию right_view(root): значения "
                "узлов, которые видны, если смотреть на дерево справа, — по одному "
                "на каждый уровень (самый правый узел уровня), сверху вниз. Пустое "
                "дерево — []."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef right_view(root):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    if not vals or vals[0] is None:\n"
                "        return None\n"
                "    nodes = [TreeNode(v) if v is not None else None for v in vals]\n"
                "    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n"
                "        if n:\n"
                "            if kids:\n"
                "                n.left = kids.pop()\n"
                "            if kids:\n"
                "                n.right = kids.pop()\n"
                "    return nodes[0]\n"
                "\n"
                "\n"
                "def levels(root):\n"
                "    out, cur = [], [root] if root else []\n"
                "    while cur:\n"
                "        out.append([n.val for n in cur])\n"
                "        cur = [c for n in cur for c in (n.left, n.right) if c]\n"
                "    return out\n"
                "\n"
                "\n"
                "def chain(n, side=\"left\"):\n"
                "    root = cur = TreeNode(0)\n"
                "    for i in range(1, n):\n"
                "        nxt = TreeNode(i)\n"
                "        setattr(cur, side, nxt)\n"
                "        cur = nxt\n"
                "    return root\n"
                "\n"
                "\n"
                "print(right_view(build([1, 2, 3, None, 5, None, 4])), right_view(None), right_view(build([1, None, 3])), right_view(build([1, 2])), right_view(build([1, 2, 3, 4])))\n"
            ),
            "expected": ["[1, 3, 4] [] [1, 3] [1, 2] [1, 3, 4]"],
            "hint": "Обход по уровням слева направо: последний узел списка текущего уровня — тот, что виден справа.",
        },
        {
            "id": "tree-symmetric",
            "mode": "stdout",
            "title": "Симметричное дерево",
            "statement": (
                "Дан класс TreeNode. Напишите функцию is_symmetric(root): True, "
                "если дерево — зеркальное отражение самого себя относительно корня "
                "(левое поддерево — отражение правого). Пустое дерево симметрично. "
                "Решите итеративно, очередью пар узлов: проверка подаёт "
                "симметричное дерево из цепочек по 50 000 узлов."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef is_symmetric(root):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    if not vals or vals[0] is None:\n"
                "        return None\n"
                "    nodes = [TreeNode(v) if v is not None else None for v in vals]\n"
                "    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n"
                "        if n:\n"
                "            if kids:\n"
                "                n.left = kids.pop()\n"
                "            if kids:\n"
                "                n.right = kids.pop()\n"
                "    return nodes[0]\n"
                "\n"
                "\n"
                "def levels(root):\n"
                "    out, cur = [], [root] if root else []\n"
                "    while cur:\n"
                "        out.append([n.val for n in cur])\n"
                "        cur = [c for n in cur for c in (n.left, n.right) if c]\n"
                "    return out\n"
                "\n"
                "\n"
                "def chain(n, side=\"left\"):\n"
                "    root = cur = TreeNode(0)\n"
                "    for i in range(1, n):\n"
                "        nxt = TreeNode(i)\n"
                "        setattr(cur, side, nxt)\n"
                "        cur = nxt\n"
                "    return root\n"
                "\n"
                "\n"
                "print(is_symmetric(build([1, 2, 2, 3, 4, 4, 3])), is_symmetric(build([1, 2, 2, None, 3, None, 3])), is_symmetric(None), is_symmetric(TreeNode(1)), is_symmetric(build([1, 2, 3])))\n"
                "root = TreeNode(0)\n"
                "a = root.left = TreeNode(1)\n"
                "b = root.right = TreeNode(1)\n"
                "for i in range(2, 50000):\n"
                "    a.left = TreeNode(i)\n"
                "    b.right = TreeNode(i)\n"
                "    a, b = a.left, b.right\n"
                "print(is_symmetric(root))\n"
                "b.val = -1\n"
                "print(is_symmetric(root))\n"
            ),
            "expected": ["True False True True False", "True", "False"],
            "hint": "Кладите в очередь или стек пары (левый, правый), которые должны быть зеркальны: у них равны значения, а их дети кладутся перекрёстно — (a.left, b.right) и (a.right, b.left).",
        },
        {
            "id": "tree-invert",
            "mode": "stdout",
            "title": "Отразить дерево",
            "statement": (
                "Дан класс TreeNode. Напишите функцию invert(root): поменяйте "
                "местами левого и правого ребёнка у каждого узла и верните корень. "
                "Решите без рекурсии — проверка подаёт цепочку из 100 000 узлов."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef invert(root):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    if not vals or vals[0] is None:\n"
                "        return None\n"
                "    nodes = [TreeNode(v) if v is not None else None for v in vals]\n"
                "    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n"
                "        if n:\n"
                "            if kids:\n"
                "                n.left = kids.pop()\n"
                "            if kids:\n"
                "                n.right = kids.pop()\n"
                "    return nodes[0]\n"
                "\n"
                "\n"
                "def levels(root):\n"
                "    out, cur = [], [root] if root else []\n"
                "    while cur:\n"
                "        out.append([n.val for n in cur])\n"
                "        cur = [c for n in cur for c in (n.left, n.right) if c]\n"
                "    return out\n"
                "\n"
                "\n"
                "def chain(n, side=\"left\"):\n"
                "    root = cur = TreeNode(0)\n"
                "    for i in range(1, n):\n"
                "        nxt = TreeNode(i)\n"
                "        setattr(cur, side, nxt)\n"
                "        cur = nxt\n"
                "    return root\n"
                "\n"
                "\n"
                "print(levels(invert(build([4, 2, 7, 1, 3, 6, 9]))), levels(invert(None)), levels(invert(build([1, 2]))))\n"
                "r = invert(chain(100000))\n"
                "d = 0\n"
                "while r.right:\n"
                "    r = r.right\n"
                "    d += 1\n"
                "print(d, r.val)\n"
            ),
            "expected": ["[[4], [7, 2], [9, 6, 3, 1]] [] [[1], [2]]", "99999 99999"],
            "hint": "Обойдите дерево любым способом со своим стеком и у каждого узла поменяйте left и right местами.",
        },
        {
            "id": "tree-build-pre-in",
            "mode": "stdout",
            "title": "Дерево по двум обходам",
            "statement": (
                "Даны прямой (preorder) и центрированный (inorder) обходы бинарного "
                "дерева с различными значениями. Напишите функцию build_tree(pre, "
                "ino): восстановите дерево и верните корень. Поиск корня в inorder "
                "должен быть O(1) — заведите словарь значение → позиция. Проверка "
                "подаёт 100 000 узлов."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef build_tree(pre, ino):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    if not vals or vals[0] is None:\n"
                "        return None\n"
                "    nodes = [TreeNode(v) if v is not None else None for v in vals]\n"
                "    kids = nodes[1:][::-1]\n"
                "    for n in nodes:\n"
                "        if n:\n"
                "            if kids:\n"
                "                n.left = kids.pop()\n"
                "            if kids:\n"
                "                n.right = kids.pop()\n"
                "    return nodes[0]\n"
                "\n"
                "\n"
                "def levels(root):\n"
                "    out, cur = [], [root] if root else []\n"
                "    while cur:\n"
                "        out.append([n.val for n in cur])\n"
                "        cur = [c for n in cur for c in (n.left, n.right) if c]\n"
                "    return out\n"
                "\n"
                "\n"
                "def chain(n, side=\"left\"):\n"
                "    root = cur = TreeNode(0)\n"
                "    for i in range(1, n):\n"
                "        nxt = TreeNode(i)\n"
                "        setattr(cur, side, nxt)\n"
                "        cur = nxt\n"
                "    return root\n"
                "\n"
                "\n"
                "print(levels(build_tree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])), levels(build_tree([], [])), levels(build_tree([1], [1])), levels(build_tree([1, 2], [2, 1])))\n"
                "n = 100000\n"
                "vals = [(i * 7919) % n for i in range(n)]\n"
                "root = None\n"
                "nodes = []\n"
                "def ins(r, v):\n"
                "    if r is None:\n"
                "        return TreeNode(v)\n"
                "    cur = r\n"
                "    while True:\n"
                "        if v < cur.val:\n"
                "            if cur.left is None:\n"
                "                cur.left = TreeNode(v)\n"
                "                return r\n"
                "            cur = cur.left\n"
                "        else:\n"
                "            if cur.right is None:\n"
                "                cur.right = TreeNode(v)\n"
                "                return r\n"
                "            cur = cur.right\n"
                "for v in vals:\n"
                "    root = ins(root, v)\n"
                "def pre(r):\n"
                "    out, st = [], [r]\n"
                "    while st:\n"
                "        x = st.pop()\n"
                "        out.append(x.val)\n"
                "        if x.right: st.append(x.right)\n"
                "        if x.left: st.append(x.left)\n"
                "    return out\n"
                "def ino_(r):\n"
                "    out, st, cur = [], [], r\n"
                "    while cur or st:\n"
                "        while cur:\n"
                "            st.append(cur)\n"
                "            cur = cur.left\n"
                "        cur = st.pop()\n"
                "        out.append(cur.val)\n"
                "        cur = cur.right\n"
                "    return out\n"
                "p, i = pre(root), ino_(root)\n"
                "t = build_tree(p, i)\n"
                "print(pre(t) == p, ino_(t) == i)\n"
            ),
            "expected": ["[[3], [9, 20], [15, 7]] [] [[1]] [[1], [2]]", "True True"],
            "hint": "Первый элемент pre — корень. Его позиция m в ino делит ино-обход: слева левое поддерево (m − lo узлов), справа правое. Прямой порядок ведите одним итератором: сначала строится левое поддерево, потом правое.",
        },
        {
            "id": "trie-class",
            "mode": "stdout",
            "title": "Префиксное дерево",
            "statement": (
                "Реализуйте класс Trie: insert(word), search(word) — есть ли слово "
                "целиком, starts_with(prefix) — есть ли слово с таким началом, "
                "count_prefix(prefix) — сколько вставленных слов (с учётом "
                "повторных вставок) начинаются с prefix. Узел — словарь детей и "
                "счётчик. Все операции — O(длина слова). Проверка подаёт 100 000 "
                "слов."
            ),
            "starter": "class Trie:\n    def __init__(self):\n        self.root = {}\n\n    # insert, search, starts_with, count_prefix\n",
            "driver": (
                "t = Trie()\n"
                "for w in (\"apple\", \"app\", \"apple\", \"apt\", \"bat\", \"bath\"):\n"
                "    t.insert(w)\n"
                "print(t.search(\"apple\"), t.search(\"app\"), t.search(\"ap\"), t.search(\"bath\"), t.search(\"bad\"))\n"
                "print(t.starts_with(\"ap\"), t.starts_with(\"ba\"), t.starts_with(\"c\"), t.starts_with(\"bathe\"))\n"
                "print(t.count_prefix(\"app\"), t.count_prefix(\"ap\"), t.count_prefix(\"b\"), t.count_prefix(\"z\"), t.count_prefix(\"bath\"))\n"
                "words = [\"\".join(chr(97 + (i * j) % 26) for j in range(1, 9)) for i in range(1, 100001)]\n"
                "big = Trie()\n"
                "for w in words:\n"
                "    big.insert(w)\n"
                "print(all(big.search(w) for w in words[:2000]), big.search(\"zzzzzzzz\"), big.count_prefix(words[7][:3]), big.count_prefix(words[999][:5]))\n"
            ),
            "expected": ["True True False True False", "True True False False", "3 4 2 0 1", "True False 3846 3846"],
            "hint": "Узел хранит словарь детей, счётчик слов, прошедших через узел, и счётчик слов, закончившихся здесь. count_prefix — счётчик «прошло» у узла, до которого спустились по префиксу.",
        },
    ],
}

_BY_ID = {t["id"]: t for t in _NEW[8]} | KEPT

TASKS: dict[int, list[dict]] = {
    8: [_BY_ID[i] for i in (
        "tree-max-depth",
        "tree-path-sum",
        "tree-preorder-iter",
        "tree-inorder-iter",
        "tree-postorder-iter",
        "tree-level-order",
        "tree-zigzag",
        "tree-right-view",
        "tree-symmetric",
        "tree-invert",
        "tree-diameter",
        "tree-lca",
        "tree-build-pre-in",
        "trie-class",
    )],
}
