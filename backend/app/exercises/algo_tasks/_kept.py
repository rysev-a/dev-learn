"""Задачи старых глав 2, 4, 5, переехавшие в новые главы (массивы, списки, хеш-таблицы, два указателя)."""

KEPT: dict[str, dict] = {
    "reverse-in-place": {
            "id": "reverse-in-place",
            "mode": "stdout",
            "title": "Развернуть на месте",
            "statement": (
                "Напишите функцию reverse_in_place(arr): разворачивает "
                "список НА МЕСТЕ двумя указателями (один с начала, другой с "
                "конца, обмениваем и сближаем). Ничего не возвращает и не "
                "создаёт копий."
            ),
            "starter": "def reverse_in_place(arr):\n    pass\n",
            "driver": (
                "a = [1, 2, 3, 4, 5]\nr = reverse_in_place(a)\nprint(a, r)\nb = []\nreverse_in_place(b)\nprint(b)\n"
                "c = ['а', 'б']\nsame = c\nreverse_in_place(c)\nprint(same)\n"
                "big = list(range(1000000))\nreverse_in_place(big)\nprint(big[0], big[-1])\n"
            ),
            "expected": ["[5, 4, 3, 2, 1] None", "[]", "['б', 'а']", "999999 0"],
            "hint": "i, j = 0, len(arr) - 1; while i < j: arr[i], arr[j] = arr[j], arr[i]; i += 1; j -= 1.",
        },
    "rotate-right": {
            "id": "rotate-right",
            "mode": "stdout",
            "title": "Циклический сдвиг",
            "statement": (
                "Напишите функцию rotate_right(arr, k): сдвигает список "
                "вправо на k позиций по кругу НА МЕСТЕ (k может быть больше "
                "длины). Решение за O(n): проверка подаёт миллион элементов."
            ),
            "starter": "def rotate_right(arr, k):\n    pass\n",
            "driver": (
                "a = [1, 2, 3, 4, 5, 6, 7]\nrotate_right(a, 3)\nprint(a)\n"
                "b = [1, 2, 3]\nrotate_right(b, 7)\nprint(b)\nc = []\nrotate_right(c, 2)\nprint(c)\n"
                "big = list(range(1000000))\nrotate_right(big, 100000)\nprint(big[0], big[100000], big[-1])\n"
            ),
            "expected": ["[5, 6, 7, 1, 2, 3, 4]", "[3, 1, 2]", "[]", "900000 0 899999"],
            "hint": "k %= n; затем три разворота: весь список, первые k, остальные — либо срез arr[:] = arr[-k:] + arr[:-k].",
        },
    "reverse-linked-list": {
            "id": "reverse-linked-list",
            "mode": "stdout",
            "title": "Развернуть связный список",
            "statement": (
                "Дан класс ListNode (val, next). Напишите функцию "
                "reverse_list(head): разворачивает односвязный список, "
                "переставляя ссылки next, и возвращает новую голову. Без "
                "создания новых узлов и без рекурсии (в списке бывает 100 000 "
                "узлов)."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef reverse_list(head):\n    pass\n",
            "driver": (
                "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n"
                "def to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\n"
                "print(to_list(reverse_list(build([1, 2, 3, 4]))), to_list(reverse_list(build([7]))), to_list(reverse_list(None)))\n"
                "r = reverse_list(build(list(range(100000))))\nprint(r.val, to_list(r)[-1])\n"
            ),
            "expected": ["[4, 3, 2, 1] [7] []", "99999 0"],
            "hint": "prev = None; пока head: nxt = head.next; head.next = prev; prev = head; head = nxt; вернуть prev.",
        },
    "middle-node": {
            "id": "middle-node",
            "mode": "stdout",
            "title": "Середина списка",
            "statement": (
                "Дан класс ListNode. Напишите функцию middle(head): значение "
                "среднего узла за ОДИН проход (медленный и быстрый указатели). "
                "Для списка чётной длины — второй из двух средних."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef middle(head):\n    pass\n",
            "driver": (
                "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n"
                "print(middle(build([1, 2, 3, 4, 5])), middle(build([1, 2, 3, 4])), middle(build([9])))\n"
                "print(middle(build(list(range(1000001)))))\n"
            ),
            "expected": ["3 3 9", "500000"],
            "hint": "slow = fast = head; while fast and fast.next: slow = slow.next; fast = fast.next.next.",
        },
    "has-cycle": {
            "id": "has-cycle",
            "mode": "stdout",
            "title": "Есть ли цикл",
            "statement": (
                "Дан класс ListNode. Напишите функцию has_cycle(head): True, "
                "если по ссылкам next можно ходить бесконечно (в списке есть "
                "цикл). Алгоритм Флойда: два указателя с разной скоростью, O(1) "
                "памяти."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef has_cycle(head):\n    pass\n",
            "driver": (
                "def build(n):\n    nodes = [ListNode(i) for i in range(n)]\n    for a, b in zip(nodes, nodes[1:]):\n        a.next = b\n    return nodes\n"
                "print(has_cycle(None), has_cycle(ListNode(1)))\n"
                "ns = build(5)\nprint(has_cycle(ns[0]))\nns[4].next = ns[2]\nprint(has_cycle(ns[0]))\n"
                "one = ListNode(1)\none.next = one\nprint(has_cycle(one))\n"
                "big = build(200000)\nprint(has_cycle(big[0]))\nbig[-1].next = big[0]\nprint(has_cycle(big[0]))\n"
            ),
            "expected": ["False False", "False", "True", "True", "False", "True"],
            "hint": "slow сдвигайте на 1, fast на 2; если они встретились — цикл есть, если fast упёрся в None — нет.",
        },
    "merge-sorted-lists": {
            "id": "merge-sorted-lists",
            "mode": "stdout",
            "title": "Слить два отсортированных списка",
            "statement": (
                "Дан класс ListNode. Напишите функцию merge_lists(a, b): "
                "сливает два отсортированных по возрастанию связных списка в "
                "один отсортированный, переиспользуя узлы, и возвращает "
                "голову. Время O(n + m), без рекурсии."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef merge_lists(a, b):\n    pass\n",
            "driver": (
                "def build(vals):\n    head = None\n    for v in reversed(vals):\n        head = ListNode(v, head)\n    return head\n"
                "def to_list(h):\n    out = []\n    while h:\n        out.append(h.val)\n        h = h.next\n    return out\n"
                "print(to_list(merge_lists(build([1, 3, 5]), build([2, 4, 6]))))\n"
                "print(to_list(merge_lists(build([]), build([1, 2]))), to_list(merge_lists(build([1]), build([]))))\n"
                "print(to_list(merge_lists(build([1, 1, 2]), build([1, 3]))))\n"
                "m = to_list(merge_lists(build(list(range(0, 200000, 2))), build(list(range(1, 200000, 2)))))\nprint(m == list(range(200000)))\n"
            ),
            "expected": ["[1, 2, 3, 4, 5, 6]", "[1, 2] [1]", "[1, 1, 1, 2, 3]", "True"],
            "hint": "Фиктивный узел dummy и указатель tail: на каждом шаге присоединяйте меньший из двух текущих узлов.",
        },
    "is-palindrome-two-pointers": {
            "id": "is-palindrome-two-pointers",
            "mode": "func",
            "func": "is_palindrome",
            "title": "Палиндром",
            "statement": (
                "Напишите функцию is_palindrome(s): True, если строка читается "
                "одинаково в обе стороны, если не обращать внимания на "
                "регистр и на все символы, кроме букв и цифр. Идите двумя "
                "указателями с концов."
            ),
            "starter": "def is_palindrome(s):\n    pass\n",
            "tests": [
                {"args": ["А роза упала на лапу Азора"], "expected": True},
                {"args": ["Was it a car or a cat I saw?"], "expected": True},
                {"args": ["привет"], "expected": False},
                {"args": [""], "expected": True},
                {"args": [".,"], "expected": True},
                {"args": ["ab"], "expected": False},
            ],
            "hint": "i, j = 0, len(s) - 1; пропускайте символы, у которых not ch.isalnum(); сравнивайте через lower().",
        },
    "longest-common-prefix": {
            "id": "longest-common-prefix",
            "mode": "func",
            "func": "common_prefix",
            "title": "Общий префикс",
            "statement": (
                "Напишите функцию common_prefix(words): самая длинная общая "
                "начальная часть всех слов списка (пустая строка, если её нет "
                "или список пуст)."
            ),
            "starter": "def common_prefix(words):\n    pass\n",
            "tests": [
                {"args": [["цветок", "цвет", "цветной"]], "expected": "цвет"},
                {"args": [["собака", "гоночная", "машина"]], "expected": ""},
                {"args": [["одно"]], "expected": "одно"},
                {"args": [[]], "expected": ""},
                {"args": [["аб", "аб", "аб"]], "expected": "аб"},
            ],
            "hint": "Берите первое слово как кандидата и укорачивайте, пока каждое слово не начнётся с него (startswith).",
        },
    "two-sum-sorted-pointers": {
            "id": "two-sum-sorted-pointers",
            "mode": "stdout",
            "title": "Два указателя в отсортированном",
            "statement": (
                "Напишите функцию pair_with_sum(arr, target): в "
                "отсортированном по возрастанию списке найдите два разных "
                "элемента с суммой target и верните их индексы (i, j), i < "
                "j, либо None. Два указателя, O(n) времени и O(1) памяти: "
                "проверка подаёт миллион элементов."
            ),
            "starter": "def pair_with_sum(arr, target):\n    pass\n",
            "driver": (
                "print(pair_with_sum([1, 2, 4, 7, 11], 9), pair_with_sum([1, 2, 3], 10), pair_with_sum([], 1), pair_with_sum([5], 5))\n"
                "big = list(range(1000000))\nprint(pair_with_sum(big, 1999997), pair_with_sum(big, 3000000))\n"
            ),
            "expected": ["(1, 3) None None None", "(999998, 999999) None"],
            "hint": "i = 0, j = len - 1; сумма мала — i += 1, велика — j -= 1; пока i < j.",
        },
    "remove-duplicates-sorted": {
            "id": "remove-duplicates-sorted",
            "mode": "stdout",
            "title": "Убрать повторы на месте",
            "statement": (
                "Напишите функцию dedupe(arr): в отсортированном списке "
                "оставьте по одному экземпляру каждого значения НА МЕСТЕ "
                "(два указателя: читающий и пишущий), не создавая второго "
                "списка. Функция возвращает новую длину k, а первые k "
                "элементов arr — уникальные значения."
            ),
            "starter": "def dedupe(arr):\n    pass\n",
            "driver": (
                "a = [1, 1, 2, 3, 3, 3, 4]\nk = dedupe(a)\nprint(k, a[:k])\nb = []\nprint(dedupe(b))\nc = [5, 5, 5]\nk = dedupe(c)\nprint(k, c[:k])\n"
                "big = sorted([i // 3 for i in range(900000)])\nk = dedupe(big)\nprint(k, big[:3], big[k - 1])\n"
            ),
            "expected": ["4 [1, 2, 3, 4]", "0", "1 [5]", "300000 [0, 1, 2] 299999"],
            "hint": "w = 1; для r в 1..n-1: если arr[r] != arr[w - 1]: arr[w] = arr[r]; w += 1. Вернуть w (для пустого — 0).",
        },
    "longest-unique-window": {
            "id": "longest-unique-window",
            "mode": "stdout",
            "title": "Самая длинная подстрока без повторов",
            "statement": (
                "Напишите функцию longest_unique(s): длина самой длинной "
                "подстроки без повторяющихся символов. Скользящее окно, O(n): "
                "проверка подаёт строку из 500 000 символов."
            ),
            "starter": "def longest_unique(s):\n    pass\n",
            "driver": (
                "print(longest_unique('abcabcbb'), longest_unique('bbbbb'), longest_unique('pwwkew'), longest_unique(''), longest_unique('привет'))\n"
                "import string\nbig = (string.ascii_lowercase * 20000)[:500000]\nprint(longest_unique(big))\nprint(longest_unique('a' * 500000))\n"
            ),
            "expected": ["3 1 3 0 6", "26", "1"],
            "hint": "Словарь «символ → последний индекс» и левая граница окна: при повторе сдвиньте её на last[ch] + 1.",
        },
    "max-sum-window": {
            "id": "max-sum-window",
            "mode": "stdout",
            "title": "Окно фиксированной длины",
            "statement": (
                "Напишите функцию best_window(nums, k): наибольшая сумма k "
                "подряд идущих элементов (k <= len(nums), k >= 1). Не "
                "пересчитывайте сумму окна заново: сдвигайте её за O(1). "
                "Проверка — миллион элементов и окно в 100 000."
            ),
            "starter": "def best_window(nums, k):\n    pass\n",
            "driver": (
                "print(best_window([1, 4, 2, 10, 23, 3, 1, 0, 20], 4), best_window([5], 1), best_window([-1, -2, -3], 2))\n"
                "big = list(range(1000000))\nprint(best_window(big, 100000))\n"
            ),
            "expected": ["39 5 -3", "94999950000"],
            "hint": "Сумма первого окна, затем window += nums[i] - nums[i - k] и обновление максимума.",
        },
    "container-most-water": {
            "id": "container-most-water",
            "mode": "stdout",
            "title": "Больше всего воды",
            "statement": (
                "Дан список высот вертикальных линий. Напишите функцию "
                "most_water(heights): наибольшая площадь прямоугольника "
                "между двумя линиями — ширина (разница индексов) на меньшую "
                "из высот. Два указателя, O(n): проверка подаёт 200 000 "
                "линий."
            ),
            "starter": "def most_water(heights):\n    pass\n",
            "driver": (
                "print(most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]), most_water([1, 1]), most_water([4, 3, 2, 1, 4]), most_water([5]))\n"
                "big = [min(i, 200000 - i) for i in range(200001)]\nprint(most_water(big))\n"
            ),
            "expected": ["49 1 16 0", "5000000000"],
            "hint": "Идите с обоих концов; всегда сдвигайте указатель у МЕНЬШЕЙ линии — большая её ширину не улучшит.",
        },
    "count-inversions": {
            "id": "count-inversions",
            "mode": "stdout",
            "title": "Число инверсий",
            "statement": (
                "Напишите функцию count_inversions(arr): сколько пар (i, j) "
                "с i < j и arr[i] > arr[j]. Разделяй и властвуй (модификация "
                "сортировки слиянием), O(n log n): проверка подаёт 100 000 "
                "элементов в обратном порядке."
            ),
            "starter": "def count_inversions(arr):\n    pass\n",
            "driver": (
                "print(count_inversions([2, 4, 1, 3, 5]), count_inversions([1, 2, 3]), count_inversions([3, 2, 1]), count_inversions([]))\n"
                "n = 100000\nprint(count_inversions(list(range(n, 0, -1))) == n * (n - 1) // 2)\n"
            ),
            "expected": ["3 0 3 0", "True"],
            "hint": "При слиянии, если берём элемент ПРАВОЙ половины, он «перепрыгивает» все оставшиеся в левой: прибавляйте len(left) - i.",
        },
    "max-subarray-divide": {
            "id": "max-subarray-divide",
            "mode": "stdout",
            "title": "Лучший подотрезок: разделяй и властвуй",
            "statement": (
                "Напишите функцию best_sum(nums): наибольшая сумма "
                "непрерывного непустого подотрезка (список не пустой), но "
                "рекурсивно: лучший отрезок либо целиком слева, либо целиком "
                "справа, либо пересекает середину (тогда его можно найти "
                "за линейное время). Глубина рекурсии должна быть O(log n)."
            ),
            "starter": "def best_sum(nums):\n    pass\n",
            "driver": (
                "import sys\nsys.setrecursionlimit(200)\n"
                "print(best_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]), best_sum([-5]), best_sum([2, 3, -10, 4, 5]), best_sum([-3, -1, -2]))\n"
                "print(best_sum([1, -1] * 100000 + [5]))\n"
            ),
            "expected": ["6 -5 9 -1", "5"],
            "hint": "Разделите пополам; ответ = max(лучший слева, лучший справа, лучший суффикс слева + лучший префикс справа).",
        },
    "min-window-substring": {
            "id": "min-window-substring",
            "mode": "func",
            "func": "min_window_len",
            "title": "Минимальное окно",
            "statement": (
                "Напишите функцию min_window_len(s, t): длина самой короткой "
                "подстроки s, содержащей все символы t (с учётом кратности), "
                "либо 0, если такой нет. Скользящее окно с двумя "
                "указателями."
            ),
            "starter": "def min_window_len(s, t):\n    pass\n",
            "tests": [
                {"args": ["ADOBECODEBANC", "ABC"], "expected": 4},
                {"args": ["a", "a"], "expected": 1},
                {"args": ["a", "aa"], "expected": 0},
                {"args": ["abc", ""], "expected": 0},
                {"args": ["aaflslflsldkalskaaa", "aaa"], "expected": 3},
            ],
            "hint": "need = Counter(t); расширяйте правую границу, пока окно не покрывает need, затем сжимайте левую, обновляя минимум.",
        },
    "tree-inorder-iter": {
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
    "tree-max-depth": {
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
    "tree-level-order": {
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
    "tree-valid-bst": {
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
    "tree-lca": {
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
    "tree-diameter": {
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
    "tree-path-sum": {
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
    "bst-insert": {
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
}
