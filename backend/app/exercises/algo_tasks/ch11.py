"""Задачи книги «Алгоритмы и структуры данных»: глава 11."""

TASKS: dict[int, list[dict]] = {
    11: [
        {
            "id": "rotations",
            "mode": "stdout",
            "title": "Вращения",
            "statement": (
                "Дан класс TreeNode. Напишите функции rotate_left(x) и "
                "rotate_right(x): левое и правое вращение поддерева с корнем x; "
                "верните новый корень поддерева (у x должен быть правый — для "
                "левого, левый — для правого вращения ребёнок; иначе верните x без "
                "изменений). Порядок ключей при этом не должен нарушаться."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef rotate_left(x):\n    pass\n\n\ndef rotate_right(x):\n    pass\n",
            "driver": (
                "def tup(n):\n"
                "    return None if n is None else (n.val, tup(n.left), tup(n.right))\n"
                "\n"
                "\n"
                "def inorder_list(root):\n"
                "    out, st, cur = [], [], root\n"
                "    while cur or st:\n"
                "        while cur:\n"
                "            st.append(cur)\n"
                "            cur = cur.left\n"
                "        cur = st.pop()\n"
                "        out.append(cur.val)\n"
                "        cur = cur.right\n"
                "    return out\n"
                "\n"
                "\n"
                "t = TreeNode(2, TreeNode(1), TreeNode(5, TreeNode(3), TreeNode(6)))\n"
                "r = rotate_left(t)\n"
                "print(tup(r), inorder_list(r))\n"
                "r = rotate_right(r)\n"
                "print(tup(r), inorder_list(r))\n"
                "print(tup(rotate_left(TreeNode(1))), tup(rotate_right(TreeNode(1, None, TreeNode(2)))))\n"
                "n = 50000\n"
                "chain = cur = TreeNode(0)\n"
                "for i in range(1, n):\n"
                "    cur.right = TreeNode(i)\n"
                "    cur = cur.right\n"
                "r = rotate_left(chain)\n"
                "print(r.val, r.left.val, r.right.val, inorder_list(r)[:4])\n"
            ),
            "expected": ["(5, (2, (1, None, None), (3, None, None)), (6, None, None)) [1, 2, 3, 5, 6]", "(2, (1, None, None), (5, (3, None, None), (6, None, None))) [1, 2, 3, 5, 6]", "(1, None, None) (1, None, (2, None, None))", "1 0 2 [0, 1, 2, 3]"],
            "hint": "Левое: y = x.right; x.right = y.left; y.left = x; вернуть y. Правое — зеркально. Три присваивания ссылок.",
        },
        {
            "id": "avl-balance",
            "mode": "stdout",
            "title": "Баланс АВЛ-дерева",
            "statement": (
                "Дан класс TreeNode. Напишите функцию avl_check(root): кортеж "
                "(высота дерева, является ли оно АВЛ-деревом) — то есть для каждого "
                "узла высоты поддеревьев отличаются не больше чем на 1. Высота "
                "пустого дерева — 0, одного узла — 1. Один обход снизу вверх: "
                "проверка подаёт дерево из 100 000 узлов, поэтому пишите итеративно "
                "или с большим запасом рекурсии (sys.setrecursionlimit)."
            ),
            "starter": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right\n\n\ndef avl_check(root):\n    pass\n",
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
                "print(avl_check(build([4, 2, 6, 1, 3, 5, 7])), avl_check(build([1, None, 2, None, 3])), avl_check(None), avl_check(TreeNode(1)), avl_check(build([1, 2, 3, 4, None, None, None])))\n"
                "root = cur = TreeNode(0)\n"
                "for i in range(1, 100000):\n"
                "    cur.left = TreeNode(i)\n"
                "    cur = cur.left\n"
                "print(avl_check(root))\n"
                "def perfect(d):\n"
                "    return None if d == 0 else TreeNode(d, perfect(d - 1), perfect(d - 1))\n"
                "print(avl_check(perfect(16)))\n"
            ),
            "expected": ["(3, True) (3, False) (0, True) (1, True) (3, True)", "(100000, False)", "(16, True)"],
            "hint": "Нужно знать высоты поддеревьев раньше, чем высоту узла — обход снизу вверх (обратный порядок). Храните высоты в словаре по узлам и проверяйте |hl − hr| ≤ 1 в каждом.",
        },
        {
            "id": "avl-rebalance",
            "mode": "stdout",
            "title": "Один шаг балансировки АВЛ",
            "statement": (
                "Дан класс TreeNode, в котором высоты хранятся в поле h. Напишите "
                "функцию rebalance(node): если баланс узла (высота левого − высота "
                "правого) равен +2 или −2, выполните нужные вращения (случаи LL, "
                "RR, LR, RL) и верните новый корень поддерева, обновив поля h; "
                "иначе только обновите h узла и верните его. Баланс детей считается "
                "допустимым. Высота пустого поддерева — 0."
            ),
            "starter": "class Node:\n    def __init__(self, key, left=None, right=None):\n        self.key = key\n        self.left = left\n        self.right = right\n        self.h = 1\n\n\ndef h(n):\n    return n.h if n else 0\n\n\ndef update(n):\n    n.h = 1 + max(h(n.left), h(n.right))\n\n\ndef rebalance(node):\n    pass\n",
            "driver": (
                "def mk(k, l=None, r=None):\n"
                "    n = Node(k, l, r)\n"
                "    update(n)\n"
                "    return n\n"
                "\n"
                "\n"
                "def tup(n):\n"
                "    return None if n is None else (n.key, tup(n.left), tup(n.right))\n"
                "\n"
                "\n"
                "ll = mk(3, mk(2, mk(1)))\n"
                "r = rebalance(ll)\n"
                "print(tup(r), r.h)\n"
                "rr = mk(1, None, mk(2, None, mk(3)))\n"
                "r = rebalance(rr)\n"
                "print(tup(r), r.h)\n"
                "lr = mk(3, mk(1, None, mk(2)))\n"
                "r = rebalance(lr)\n"
                "print(tup(r), r.h)\n"
                "rl = mk(1, None, mk(3, mk(2)))\n"
                "r = rebalance(rl)\n"
                "print(tup(r), r.h)\n"
                "ok = mk(2, mk(1), mk(3))\n"
                "print(tup(rebalance(ok)), ok.h)\n"
                "big = mk(5, mk(3, mk(2, mk(1)), mk(4)), mk(6))\n"
                "r = rebalance(big)\n"
                "print(tup(r), r.h)\n"
            ),
            "expected": ["(2, (1, None, None), (3, None, None)) 2", "(2, (1, None, None), (3, None, None)) 2", "(2, (1, None, None), (3, None, None)) 2", "(2, (1, None, None), (3, None, None)) 2", "(2, (1, None, None), (3, None, None)) 2", "(3, (2, (1, None, None), None), (5, (4, None, None), (6, None, None))) 3"],
            "hint": "Если баланс +2: когда у левого ребёнка перевешивает правое поддерево (случай LR) — сначала левое вращение ребёнка; затем правое вращение узла. Зеркально для −2. После каждого вращения обновляйте h у опущенного узла, затем у поднятого.",
        },
        {
            "id": "avl-tree-class",
            "mode": "stdout",
            "title": "АВЛ-дерево",
            "statement": (
                "Реализуйте класс AVLTree: insert(x) (повтор игнорируется), "
                "contains(x), inorder(), height() (пустое — 0) и len(t). После "
                "каждой вставки дерево должно оставаться АВЛ-деревом (вращения LL, "
                "RR, LR, RL). Проверка вставляет 100 000 упорядоченных ключей — "
                "обычное дерево поиска вырождается, а ваше должно держать высоту ≤ "
                "1,45 log₂ n + 2. Рекурсия допустима: глубина — логарифм."
            ),
            "starter": "class Node:\n    def __init__(self, key):\n        self.key = key\n        self.left = None\n        self.right = None\n        self.h = 1\n\n\nclass AVLTree:\n    def __init__(self):\n        self.root = None\n        self._n = 0\n\n    def __len__(self):\n        return self._n\n\n    # insert, contains, inorder, height\n",
            "driver": (
                "import math\n"
                "\n"
                "t = AVLTree()\n"
                "for x in (3, 2, 1, 4, 5, 6, 7, 16, 15, 14):\n"
                "    t.insert(x)\n"
                "print(t.inorder(), len(t), t.height(), t.contains(6), t.contains(8))\n"
                "t.insert(5)\n"
                "print(len(t), AVLTree().height())\n"
                "seq = AVLTree()\n"
                "n = 100000\n"
                "for i in range(n):\n"
                "    seq.insert(i)\n"
                "print(len(seq), seq.height() <= 1.45 * math.log2(n) + 2, seq.inorder() == list(range(n)))\n"
                "rev = AVLTree()\n"
                "for i in range(n, 0, -1):\n"
                "    rev.insert(i)\n"
                "print(rev.height() <= 1.45 * math.log2(n) + 2, rev.contains(1), rev.contains(n))\n"
            ),
            "expected": ["[1, 2, 3, 4, 5, 6, 7, 14, 15, 16] 10 4 True False", "10 0", "100000 True True", "True True True"],
            "hint": "Рекурсивная вставка возвращает новый корень поддерева; после вставки в ребёнка вызывайте balance(n): обновить высоту, посчитать баланс, при ±2 сделать один из четырёх случаев вращений.",
        },
        {
            "id": "rb-validate",
            "mode": "stdout",
            "title": "Проверка красно-чёрных правил",
            "statement": (
                "Дан класс RBNode (key, color, left, right), где color — строка 'R' "
                "или 'B'; пустая ссылка — None (чёрный лист). Напишите функцию "
                "black_height(root): чёрная высота дерева (число чёрных узлов на "
                "любом пути от корня до пустой ссылки, пустая ссылка не считается), "
                "если дерево удовлетворяет правилам красно-чёрного дерева (корень "
                "чёрный; у красного узла чёрные дети; чёрная высота всех путей "
                "одинакова; ключи упорядочены), иначе −1. Для пустого дерева — 0."
            ),
            "starter": "class RBNode:\n    def __init__(self, key, color, left=None, right=None):\n        self.key = key\n        self.color = color\n        self.left = left\n        self.right = right\n\n\ndef black_height(root):\n    pass\n",
            "driver": (
                "B, R = \"B\", \"R\"\n"
                "good = RBNode(8, B, RBNode(4, R, RBNode(2, B), RBNode(6, B)), RBNode(12, B, RBNode(10, R), RBNode(14, R)))\n"
                "print(black_height(good), black_height(None), black_height(RBNode(5, B)), black_height(RBNode(5, R)))\n"
                "red_red = RBNode(8, B, RBNode(4, R, RBNode(2, R), RBNode(6, B)), RBNode(12, B))\n"
                "print(black_height(red_red))\n"
                "uneven = RBNode(8, B, RBNode(4, B, RBNode(2, B), RBNode(6, B)), RBNode(12, B))\n"
                "print(black_height(uneven))\n"
                "order = RBNode(8, B, RBNode(9, R), RBNode(12, R))\n"
                "print(black_height(order))\n"
                "def perfect(d, lo, hi):\n"
                "    if d == 0:\n"
                "        return None\n"
                "    m = (lo + hi) // 2\n"
                "    return RBNode(m, B, perfect(d - 1, lo, m - 1), perfect(d - 1, m + 1, hi))\n"
                "print(black_height(perfect(15, 1, 2 ** 15 - 1)))\n"
            ),
            "expected": ["2 0 1 -1", "-1", "-1", "-1", "15"],
            "hint": "Рекурсивная функция возвращает чёрную высоту поддерева или −1 при нарушении. Передавайте вниз допустимые границы ключей и «родитель красный»; у узла высоты детей должны совпасть, чёрный добавляет единицу.",
        },
        {
            "id": "rb-bounds",
            "mode": "func",
            "func": "rb_bounds",
            "title": "Оценки красно-чёрного дерева",
            "statement": (
                "Напишите функцию rb_bounds(b, n): кортеж из двух чисел. Первое — "
                "наименьшее число узлов в красно-чёрном дереве с чёрной высотой b "
                "(b чёрных узлов на каждом пути до пустой ссылки): 2**b − 1. Второе "
                "— наибольшая возможная высота красно-чёрного дерева из n узлов (в "
                "узлах, пустое дерево — 0): целая часть от 2·log₂(n + 1)."
            ),
            "starter": "import math\n\n\ndef rb_bounds(b, n):\n    pass\n",
            "tests": [
                {"args": [1, 1], "expected": (1, 2)},
                {"args": [3, 7], "expected": (7, 6)},
                {"args": [4, 100], "expected": (15, 13)},
                {"args": [10, 1000], "expected": (1023, 19)},
                {"args": [0, 0], "expected": (0, 0)},
                {"args": [5, 31], "expected": (31, 10)},
                {"args": [2, 3], "expected": (3, 4)},
                {"args": [20, 1000000], "expected": (1048575, 39)},
            ],
            "hint": "Минимум узлов достигается, когда все узлы чёрные и дерево полное: 2^b − 1. Максимальная высота — из неравенства h ≤ 2·log₂(n + 1), берите целую часть.",
        },
        {
            "id": "rb-insert-case",
            "mode": "func",
            "func": "insert_case",
            "title": "Случай вставки",
            "statement": (
                "После вставки красного узла родитель оказался красным. Напишите "
                "функцию insert_case(parent_color, uncle_color, node_side, "
                "parent_side): строка с нужным действием. Цвета — 'R' или 'B' "
                "(пустой дядя — 'B'); стороны — 'L' или 'R': node_side — какой "
                "ребёнок родителя наш узел, parent_side — каким ребёнком деда "
                "является родитель. Результат: 'done' — родитель чёрный, ничего "
                "делать не нужно; 'recolor' — дядя красный (перекраска и подъём); "
                "'kink' — дядя чёрный и узел «в изломе» (стороны разные: вращение "
                "родителя, затем деда); 'line' — дядя чёрный и узел на одной линии "
                "(стороны совпадают: вращение деда с перекраской)."
            ),
            "starter": "def insert_case(parent_color, uncle_color, node_side, parent_side):\n    pass\n",
            "tests": [
                {"args": ["B", "R", "L", "L"], "expected": "done"},
                {"args": ["R", "R", "L", "R"], "expected": "recolor"},
                {"args": ["R", "B", "R", "L"], "expected": "kink"},
                {"args": ["R", "B", "L", "L"], "expected": "line"},
                {"args": ["R", "B", "R", "R"], "expected": "line"},
                {"args": ["R", "B", "L", "R"], "expected": "kink"},
                {"args": ["B", "B", "R", "R"], "expected": "done"},
                {"args": ["R", "R", "R", "R"], "expected": "recolor"},
            ],
            "hint": "Четыре ветки подряд: чёрный родитель → done; красный дядя → recolor; иначе по сторонам: разные → kink, одинаковые → line.",
        },
        {
            "id": "llrb-insert",
            "mode": "stdout",
            "title": "Левонаклонное красно-чёрное дерево",
            "statement": (
                "Реализуйте класс LLRB (левонаклонное красно-чёрное дерево "
                "Седжвика): insert(x) (повтор игнорируется), contains(x), "
                "inorder(), height() и black_height_ok() — выполняются ли правила "
                "(корень чёрный, красных подряд нет, красных правых ссылок нет, "
                "чёрные высоты равны). Вставка рекурсивная: вставить как в дереве "
                "поиска красным узлом, затем на пути вверх: правая красная и левая "
                "чёрная → левое вращение; левая красная с красной левой внучкой → "
                "правое вращение; обе ссылки красные → перекрасить (flip_colors). "
                "Корень после вставки чёрный."
            ),
            "starter": "RED, BLACK = True, False\n\n\nclass Node:\n    def __init__(self, key, color=RED):\n        self.key = key\n        self.color = color\n        self.left = None\n        self.right = None\n\n\nclass LLRB:\n    def __init__(self):\n        self.root = None\n\n    # insert, contains, inorder, height, black_height_ok\n",
            "driver": (
                "import math\n"
                "\n"
                "t = LLRB()\n"
                "for x in (5, 3, 8, 1, 4, 7, 9, 2, 6):\n"
                "    t.insert(x)\n"
                "    assert t.black_height_ok()\n"
                "print(t.inorder(), t.height(), t.black_height_ok(), t.contains(6), t.contains(10))\n"
                "t.insert(5)\n"
                "print(len(t.inorder()))\n"
                "n = 20000\n"
                "a = LLRB()\n"
                "for i in range(n):\n"
                "    a.insert(i)\n"
                "print(a.inorder() == list(range(n)), a.black_height_ok(), a.height() <= 2 * math.log2(n + 1) + 1)\n"
                "b = LLRB()\n"
                "x = 7\n"
                "vals = []\n"
                "for _ in range(20000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    vals.append(x % 100000)\n"
                "for i, v in enumerate(vals):\n"
                "    b.insert(v)\n"
                "    if i % 2000 == 0:\n"
                "        assert b.black_height_ok()\n"
                "print(b.inorder() == sorted(set(vals)), b.black_height_ok(), b.height() <= 2 * math.log2(len(set(vals)) + 1) + 1)\n"
            ),
            "expected": ["[1, 2, 3, 4, 5, 6, 7, 8, 9] 4 True True False", "9", "True True True", "True True True"],
            "hint": "Три шага в конце рекурсии (в таком порядке): если правая ссылка красная, а левая нет — rotate_left; если левая и её левая красные — rotate_right; если обе красные — flip_colors. rotate_* переносит цвет корня на поднявшийся узел, а опустившийся делает красным.",
        },
        {
            "id": "rb-tree-class",
            "mode": "stdout",
            "title": "Красно-чёрное дерево",
            "statement": (
                "Реализуйте класс RBTree по правилам CLRS: узлы с родителем и общим "
                "листом-дозорным NIL (чёрным), методы insert(x) (повтор "
                "игнорируется), contains(x), inorder(), height() и valid() — "
                "выполнены ли все правила (корень чёрный, красных подряд нет, "
                "чёрные высоты равны, порядок ключей). Вставка: красный узел, затем "
                "исправление: красный дядя — перекраска и подъём; чёрный дядя — "
                "вращение излома, затем вращение деда с перекраской. Проверка "
                "вставляет 100 000 упорядоченных и случайных ключей."
            ),
            "starter": "BLACK, RED = 0, 1\n\n\nclass Node:\n    def __init__(self, key=None, color=BLACK):\n        self.key = key\n        self.color = color\n        self.left = None\n        self.right = None\n        self.parent = None\n\n\nclass RBTree:\n    def __init__(self):\n        self.NIL = Node()\n        self.root = self.NIL\n\n    # insert, contains, inorder, height, valid\n",
            "driver": (
                "import math\n"
                "\n"
                "t = RBTree()\n"
                "for x in (41, 38, 31, 12, 19, 8):\n"
                "    t.insert(x)\n"
                "    assert t.valid()\n"
                "print(t.inorder(), t.height(), t.valid(), t.contains(19), t.contains(20), t.root.color)\n"
                "t.insert(19)\n"
                "print(len(t.inorder()))\n"
                "n = 100000\n"
                "a = RBTree()\n"
                "for i in range(n):\n"
                "    a.insert(i)\n"
                "print(a.inorder() == list(range(n)), a.valid(), a.height() <= 2 * math.log2(n + 1))\n"
                "b = RBTree()\n"
                "x = 9\n"
                "vals = []\n"
                "for _ in range(100000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    vals.append(x % 10**6)\n"
                "for i, v in enumerate(vals):\n"
                "    b.insert(v)\n"
                "    if i % 10000 == 0:\n"
                "        assert b.valid()\n"
                "u = len(set(vals))\n"
                "print(b.inorder() == sorted(set(vals)), b.valid(), b.height() <= 2 * math.log2(u + 1))\n"
            ),
            "expected": ["[8, 12, 19, 31, 38, 41] 4 True True False 0", "6", "True True True", "True True True"],
            "hint": "Вставка: как в дереве поиска, узел красный с детьми NIL. Исправление пока родитель красный: дядя красный — перекрасить родителя, дядю и деда, подняться к деду; дядя чёрный — если излом, повернуть родителя; затем перекрасить родителя в чёрный, деда в красный и повернуть деда. В конце корень чёрный.",
        },
    ],
}
