"""Задачи главы 3"""

from app.exercises.algo_tasks._kept import KEPT

_NEW: dict[int, list[dict]] = {
    3: [
        {
            "id": "ll-length-sum",
            "mode": "stdout",
            "title": "Длина и сумма",
            "statement": (
                "Дан класс ListNode (val, next). Напишите функцию "
                "length_and_sum(head): кортеж (количество узлов, сумма значений). "
                "Для пустого списка (head — None) — (0, 0)."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef length_and_sum(head):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    head = None\n"
                "    for v in reversed(vals):\n"
                "        head = ListNode(v, head)\n"
                "    return head\n"
                "\n"
                "\n"
                "def to_list(h):\n"
                "    out = []\n"
                "    while h:\n"
                "        out.append(h.val)\n"
                "        h = h.next\n"
                "    return out\n"
                "\n"
                "\n"
                "print(length_and_sum(build([3, 1, 4])), length_and_sum(None), length_and_sum(build(list(range(100000)))))\n"
            ),
            "expected": ["(3, 8) (0, 0) (100000, 4999950000)"],
            "hint": "Один цикл: while head: счётчики и head = head.next.",
        },
        {
            "id": "ll-singly-class",
            "mode": "stdout",
            "title": "Свой односвязный список",
            "statement": (
                "Реализуйте класс SinglyLinkedList на узлах Node (val, next): поля "
                "head и tail, методы push_front(x), push_back(x) за O(1) (нужен "
                "указатель на хвост), pop_front() (значение первого узла; "
                "IndexError, если пусто), find(x) (индекс первого вхождения или "
                "−1), remove(x) (удалить первое вхождение; True/False) и to_list(); "
                "len(s) — число узлов. Следите за tail при удалении последнего узла "
                "и при опустошении списка. Проверка кладёт в хвост 200 000 "
                "элементов — без tail не успеть."
            ),
            "starter": "class Node:\n    def __init__(self, val, next=None):\n        self.val = val\n        self.next = next\n\n\nclass SinglyLinkedList:\n    def __init__(self):\n        self.head = None\n        self.tail = None\n        self._n = 0\n\n    def __len__(self):\n        return self._n\n\n    # push_front, push_back, pop_front, find, remove, to_list\n",
            "driver": (
                "s = SinglyLinkedList()\n"
                "s.push_back(1)\n"
                "s.push_back(2)\n"
                "s.push_front(0)\n"
                "s.push_back(3)\n"
                "print(s.to_list(), len(s), s.find(2), s.find(9))\n"
                "print(s.remove(0), s.remove(3), s.remove(7), s.to_list())\n"
                "s.push_back(5)\n"
                "print(s.to_list(), s.pop_front(), s.pop_front(), s.pop_front(), len(s))\n"
                "try:\n"
                "    s.pop_front()\n"
                "except IndexError:\n"
                "    print(\"IndexError\")\n"
                "s.push_back(8)\n"
                "print(s.to_list())\n"
                "big = SinglyLinkedList()\n"
                "for i in range(200000):\n"
                "    big.push_back(i)\n"
                "print(len(big), big.find(199999), big.pop_front())\n"
            ),
            "expected": ["[0, 1, 2, 3] 4 2 -1", "True True False [1, 2]", "[1, 2, 5] 1 2 5 0", "IndexError", "[8]", "200000 199999 0"],
            "hint": "push_back: если tail None — голова и хвост это новый узел, иначе tail.next = node; tail = node. В remove хранимый prev нужен и для обычного удаления, и для обновления tail.",
        },
        {
            "id": "cycle-start",
            "mode": "stdout",
            "title": "Где начинается цикл",
            "statement": (
                "Дан класс ListNode. Напишите функцию detect_cycle(head): узел, с "
                "которого начинается цикл, или None, если цикла нет. Память — O(1), "
                "алгоритм Флойда в два этапа (встреча, затем один указатель — в "
                "голову)."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef detect_cycle(head):\n    pass\n",
            "driver": (
                "def make(n, pos):\n"
                "    nodes = [ListNode(i) for i in range(n)]\n"
                "    for a, b in zip(nodes, nodes[1:]):\n"
                "        a.next = b\n"
                "    if pos >= 0:\n"
                "        nodes[-1].next = nodes[pos]\n"
                "    return nodes[0] if nodes else None\n"
                "\n"
                "\n"
                "print(detect_cycle(make(5, 2)).val)\n"
                "print(detect_cycle(make(5, -1)), detect_cycle(None))\n"
                "print(detect_cycle(make(1, 0)).val)\n"
                "print(detect_cycle(make(300000, 1234)).val)\n"
            ),
            "expected": ["2", "None None", "0", "1234"],
            "hint": "Первый цикл — как в has_cycle; при slow is fast поставьте slow = head и двигайте оба по одному шагу, пока не совпадут.",
        },
        {
            "id": "remove-nth-from-end",
            "mode": "stdout",
            "title": "Удалить n-й с конца",
            "statement": (
                "Дан класс ListNode. Напишите функцию remove_nth_from_end(head, n): "
                "удалите n-й узел с конца (n = 1 — последний) и верните голову. За "
                "один проход: два указателя на расстоянии n друг от друга. Удалять "
                "можно и саму голову — поможет дозорный узел."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef remove_nth_from_end(head, n):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    head = None\n"
                "    for v in reversed(vals):\n"
                "        head = ListNode(v, head)\n"
                "    return head\n"
                "\n"
                "\n"
                "def to_list(h):\n"
                "    out = []\n"
                "    while h:\n"
                "        out.append(h.val)\n"
                "        h = h.next\n"
                "    return out\n"
                "\n"
                "\n"
                "print(to_list(remove_nth_from_end(build([1, 2, 3, 4, 5]), 2)))\n"
                "print(to_list(remove_nth_from_end(build([1]), 1)))\n"
                "print(to_list(remove_nth_from_end(build([1, 2]), 2)), to_list(remove_nth_from_end(build([1, 2]), 1)))\n"
                "r = to_list(remove_nth_from_end(build(list(range(500000))), 250000))\n"
                "print(len(r), r[249999], r[250000])\n"
            ),
            "expected": ["[1, 2, 3, 5]", "[]", "[2] [1]", "499999 249999 250001"],
            "hint": "dummy → head. fast уходит на n шагов вперёд, затем fast и slow идут вместе до конца; slow.next = slow.next.next.",
        },
        {
            "id": "delete-duplicates-sorted",
            "mode": "stdout",
            "title": "Дубликаты в отсортированном списке",
            "statement": (
                "Дан класс ListNode. Список отсортирован. Напишите функцию "
                "delete_duplicates(head): оставьте в списке по одному узлу каждого "
                "значения (первый), верните голову. Новых узлов не создавайте."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef delete_duplicates(head):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    head = None\n"
                "    for v in reversed(vals):\n"
                "        head = ListNode(v, head)\n"
                "    return head\n"
                "\n"
                "\n"
                "def to_list(h):\n"
                "    out = []\n"
                "    while h:\n"
                "        out.append(h.val)\n"
                "        h = h.next\n"
                "    return out\n"
                "\n"
                "\n"
                "print(to_list(delete_duplicates(build([1, 1, 2, 3, 3]))), to_list(delete_duplicates(None)), to_list(delete_duplicates(build([1, 1, 1]))))\n"
                "r = to_list(delete_duplicates(build([i // 3 for i in range(300000)])))\n"
                "print(len(r), r[-1])\n"
            ),
            "expected": ["[1, 2, 3] [] [1]", "100000 99999"],
            "hint": "Пока есть cur.next: если значения равны — перепрыгните лишний узел (cur.next = cur.next.next), иначе шагните вперёд.",
        },
        {
            "id": "remove-all-value",
            "mode": "stdout",
            "title": "Удалить все значения",
            "statement": (
                "Дан класс ListNode. Напишите функцию remove_value(head, val): "
                "удалите из списка все узлы со значением val и верните новую "
                "голову. Голова тоже может подлежать удалению — используйте "
                "дозорный узел."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef remove_value(head, val):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    head = None\n"
                "    for v in reversed(vals):\n"
                "        head = ListNode(v, head)\n"
                "    return head\n"
                "\n"
                "\n"
                "def to_list(h):\n"
                "    out = []\n"
                "    while h:\n"
                "        out.append(h.val)\n"
                "        h = h.next\n"
                "    return out\n"
                "\n"
                "\n"
                "print(to_list(remove_value(build([1, 2, 6, 3, 4, 5, 6]), 6)), to_list(remove_value(build([7, 7, 7]), 7)))\n"
                "print(to_list(remove_value(build([1, 2]), 3)), to_list(remove_value(build([6, 1]), 6)), to_list(remove_value(None, 1)))\n"
                "print(to_list(remove_value(build([1] * 200000), 1)))\n"
            ),
            "expected": ["[1, 2, 3, 4, 5] []", "[1, 2] [1] []", "[]"],
            "hint": "prev = dummy; пока prev.next: если prev.next.val == val — prev.next = prev.next.next (prev стоит), иначе prev = prev.next.",
        },
        {
            "id": "palindrome-list",
            "mode": "stdout",
            "title": "Палиндром в списке",
            "statement": (
                "Дан класс ListNode. Напишите функцию is_palindrome_list(head): "
                "True, если значения читаются одинаково в обе стороны. Пустой "
                "список и список из одного узла — палиндромы. Лучшее решение — O(1) "
                "дополнительной памяти: найдите середину, разверните вторую "
                "половину и сравните половины."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef is_palindrome_list(head):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    head = None\n"
                "    for v in reversed(vals):\n"
                "        head = ListNode(v, head)\n"
                "    return head\n"
                "\n"
                "\n"
                "def to_list(h):\n"
                "    out = []\n"
                "    while h:\n"
                "        out.append(h.val)\n"
                "        h = h.next\n"
                "    return out\n"
                "\n"
                "\n"
                "print(is_palindrome_list(build([1, 2, 2, 1])), is_palindrome_list(build([1, 2, 3, 2, 1])), is_palindrome_list(build([1, 2])))\n"
                "print(is_palindrome_list(build([1])), is_palindrome_list(None))\n"
                "half = list(range(400000))\n"
                "print(is_palindrome_list(build(half + [5] + half[::-1])), is_palindrome_list(build(half + [5, 6] + half[::-1])))\n"
            ),
            "expected": ["True True False", "True True", "True False"],
            "hint": "Быстрый и медленный указатели находят середину; разверните вторую половину (как в reverse_list) и идите двумя указателями с краёв.",
        },
        {
            "id": "add-two-numbers",
            "mode": "stdout",
            "title": "Сложение чисел в списках",
            "statement": (
                "Дан класс ListNode. Два неотрицательных числа записаны списками "
                "цифр в обратном порядке (младшая цифра — в голове). Напишите "
                "функцию add_two_numbers(a, b): список с суммой в том же виде. "
                "Сложение в столбик: цифры и перенос. Цифры в каждом числе — без "
                "ведущих нулей, кроме самого числа 0."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef add_two_numbers(a, b):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    head = None\n"
                "    for v in reversed(vals):\n"
                "        head = ListNode(v, head)\n"
                "    return head\n"
                "\n"
                "\n"
                "def to_list(h):\n"
                "    out = []\n"
                "    while h:\n"
                "        out.append(h.val)\n"
                "        h = h.next\n"
                "    return out\n"
                "\n"
                "\n"
                "print(to_list(add_two_numbers(build([2, 4, 3]), build([5, 6, 4]))))\n"
                "print(to_list(add_two_numbers(build([0]), build([0]))), to_list(add_two_numbers(build([5]), build([5]))))\n"
                "print(to_list(add_two_numbers(build([9, 9, 9, 9]), build([1]))))\n"
                "r = to_list(add_two_numbers(build([9] * 100000), build([1])))\n"
                "print(len(r), r[0], r[-1])\n"
            ),
            "expected": ["[7, 0, 8]", "[0] [0, 1]", "[0, 0, 0, 0, 1]", "100001 0 1"],
            "hint": "Цикл идёт, пока есть хотя бы одно из: узел в a, узел в b, перенос. Цифра суммы — s % 10, новый перенос — s // 10.",
        },
        {
            "id": "partition-list",
            "mode": "stdout",
            "title": "Разбиение списка",
            "statement": (
                "Дан класс ListNode и число x. Напишите функцию partition(head, x): "
                "переставьте узлы так, чтобы сначала шли все узлы со значением "
                "меньше x, потом все остальные; порядок внутри каждой группы "
                "сохраняется. Верните голову. Две цепочки с дозорными и их склейка."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef partition(head, x):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    head = None\n"
                "    for v in reversed(vals):\n"
                "        head = ListNode(v, head)\n"
                "    return head\n"
                "\n"
                "\n"
                "def to_list(h):\n"
                "    out = []\n"
                "    while h:\n"
                "        out.append(h.val)\n"
                "        h = h.next\n"
                "    return out\n"
                "\n"
                "\n"
                "print(to_list(partition(build([1, 4, 3, 2, 5, 2]), 3)), to_list(partition(build([2, 1]), 2)), to_list(partition(None, 1)))\n"
                "print(to_list(partition(build([3, 3]), 3)), to_list(partition(build([1, 2, 3]), 5)))\n"
                "r = to_list(partition(build([i % 7 for i in range(300000)]), 3))\n"
                "print(len(r), r[:5], r[-3:], sum(1 for v in r if v < 3))\n"
            ),
            "expected": ["[1, 2, 2, 4, 3, 5] [1, 2] []", "[3, 3] [1, 2, 3]", "300000 [0, 1, 2, 0, 1] [4, 5, 6] 128572"],
            "hint": "Две цепочки (меньшие и остальные), у каждой свой дозорный. Не забудьте обнулить хвост второй цепочки: b.next = None.",
        },
        {
            "id": "reorder-list",
            "mode": "stdout",
            "title": "Переупорядочить список",
            "statement": (
                "Дан класс ListNode. Напишите функцию reorder(head): перестройте "
                "список L0 → L1 → … → Ln в порядок L0 → Ln → L1 → Ln−1 → L2 → … на "
                "месте, без изменения значений узлов. Возвращать ничего не нужно. "
                "Середина, разворот второй половины, чередующееся слияние."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef reorder(head):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    head = None\n"
                "    for v in reversed(vals):\n"
                "        head = ListNode(v, head)\n"
                "    return head\n"
                "\n"
                "\n"
                "def to_list(h):\n"
                "    out = []\n"
                "    while h:\n"
                "        out.append(h.val)\n"
                "        h = h.next\n"
                "    return out\n"
                "\n"
                "\n"
                "for vals in ([1, 2, 3, 4], [1, 2, 3, 4, 5], [1], [], [1, 2]):\n"
                "    h = build(vals)\n"
                "    reorder(h)\n"
                "    print(to_list(h))\n"
                "h = build(list(range(200000)))\n"
                "reorder(h)\n"
                "r = to_list(h)\n"
                "print(len(r), r[:6], sum(r))\n"
            ),
            "expected": ["[1, 4, 2, 3]", "[1, 5, 2, 4, 3]", "[1]", "[]", "[1, 2]", "200000 [0, 199999, 1, 199998, 2, 199997] 19999900000"],
            "hint": "Три шага: найти середину и отрезать вторую половину; развернуть её; затем по очереди брать узел из первой и из второй половины.",
        },
        {
            "id": "sort-list",
            "mode": "stdout",
            "title": "Сортировка списка слиянием",
            "statement": (
                "Дан класс ListNode. Напишите функцию sort_list(head): отсортируйте "
                "список по возрастанию и верните голову — сортировкой слиянием, "
                "перестановкой ссылок: значения в узлах менять нельзя (проверка "
                "следит, что у каждого узла осталось его значение). Время O(n log "
                "n); проверка подаёт 100 000 узлов."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef sort_list(head):\n    pass\n",
            "driver": (
                "def build(vals):\n"
                "    head = None\n"
                "    for v in reversed(vals):\n"
                "        head = ListNode(v, head)\n"
                "    return head\n"
                "\n"
                "\n"
                "def to_list(h):\n"
                "    out = []\n"
                "    while h:\n"
                "        out.append(h.val)\n"
                "        h = h.next\n"
                "    return out\n"
                "\n"
                "\n"
                "print(to_list(sort_list(build([4, 2, 1, 3]))), to_list(sort_list(build([-1, 5, 3, 4, 0]))), to_list(sort_list(None)), to_list(sort_list(build([2, 2, 1]))))\n"
                "x = 7\n"
                "vals = []\n"
                "for _ in range(100000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    vals.append(x % 1000)\n"
                "h = build(vals)\n"
                "nodes = []\n"
                "c = h\n"
                "while c:\n"
                "    nodes.append((id(c), c.val))\n"
                "    c = c.next\n"
                "r = sort_list(h)\n"
                "out, after = [], []\n"
                "while r:\n"
                "    out.append(r.val)\n"
                "    after.append((id(r), r.val))\n"
                "    r = r.next\n"
                "print(out == sorted(vals), set(after) == set(nodes))\n"
            ),
            "expected": ["[1, 2, 3, 4] [-1, 0, 3, 4, 5] [] [1, 2, 2]", "True True"],
            "hint": "Середина быстрым и медленным указателями, slow.next = None разрезает список; рекурсивно сортируем половины и сливаем (как merge_two_lists).",
        },
        {
            "id": "list-intersection",
            "mode": "stdout",
            "title": "Пересечение списков",
            "statement": (
                "Дан класс ListNode. Два списка могут сходиться в общий хвост (это "
                "один и тот же узел, а не узлы с равными значениями). Напишите "
                "функцию get_intersection(a, b): первый общий узел или None. O(n + "
                "m) времени и O(1) памяти. Проверка: списки по сотням тысяч узлов, "
                "вложенные циклы не успеют."
            ),
            "starter": "class ListNode:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next\n\n\ndef get_intersection(a, b):\n    pass\n",
            "driver": (
                "def chain(vals, tail=None):\n"
                "    head = tail\n"
                "    for v in reversed(vals):\n"
                "        head = ListNode(v, head)\n"
                "    return head\n"
                "\n"
                "\n"
                "common = chain([8, 4, 5])\n"
                "a = chain([4, 1], common)\n"
                "b = chain([5, 6, 1], common)\n"
                "print(get_intersection(a, b).val)\n"
                "print(get_intersection(chain([1, 2]), chain([3])), get_intersection(None, a), get_intersection(a, a).val)\n"
                "common = chain(list(range(400000)))\n"
                "a = chain(list(range(100000)), common)\n"
                "b = chain([7], common)\n"
                "r = get_intersection(a, b)\n"
                "print(r is common, r.val)\n"
            ),
            "expected": ["8", "None None 4", "True 0"],
            "hint": "Хитрость: каждый указатель, дойдя до конца, перескакивает на голову другого списка. Через n + m шагов они либо встретятся в общем узле, либо оба станут None.",
        },
        {
            "id": "doubly-linked-class",
            "mode": "stdout",
            "title": "Свой двусвязный список",
            "statement": (
                "Реализуйте класс DoublyLinkedList на узлах DNode (val, prev, next) "
                "с двумя дозорными head и tail: push_front(x) и push_back(x) "
                "(возвращают созданный узел-«ручку»), pop_front() и pop_back() "
                "(значение; IndexError, если пусто), remove(node) — удалить узел по "
                "ручке за O(1), move_to_front(node), len(d), обход for v in d (от "
                "головы к хвосту) и reversed_values() (список значений от хвоста к "
                "голове). Проверка удаляет 100 000 узлов по ручкам: поиск по "
                "значению не успеет."
            ),
            "starter": "class DNode:\n    def __init__(self, val=None):\n        self.val = val\n        self.prev = None\n        self.next = None\n\n\nclass DoublyLinkedList:\n    def __init__(self):\n        self.head = DNode()\n        self.tail = DNode()\n        self.head.next = self.tail\n        self.tail.prev = self.head\n        self._n = 0\n\n    def __len__(self):\n        return self._n\n\n    # push_front, push_back, pop_front, pop_back, remove, move_to_front, __iter__, reversed_values\n",
            "driver": (
                "d = DoublyLinkedList()\n"
                "a = d.push_back(1)\n"
                "b = d.push_back(2)\n"
                "c = d.push_back(3)\n"
                "z = d.push_front(0)\n"
                "print(list(d), d.reversed_values(), len(d))\n"
                "d.remove(b)\n"
                "print(list(d), d.reversed_values())\n"
                "d.move_to_front(c)\n"
                "print(list(d), len(d))\n"
                "print(d.pop_front(), d.pop_back(), list(d), len(d))\n"
                "print(d.pop_front(), len(d))\n"
                "try:\n"
                "    d.pop_back()\n"
                "except IndexError:\n"
                "    print(\"IndexError\")\n"
                "d.push_back(5)\n"
                "print(list(d), d.reversed_values())\n"
                "big = DoublyLinkedList()\n"
                "hs = [big.push_back(i) for i in range(200000)]\n"
                "for h in hs[::2]:\n"
                "    big.remove(h)\n"
                "print(len(big), next(iter(big)), big.reversed_values()[0], sum(big))\n"
            ),
            "expected": ["[0, 1, 2, 3] [3, 2, 1, 0] 4", "[0, 1, 3] [3, 1, 0]", "[3, 0, 1] 3", "3 1 [0] 1", "0 0", "IndexError", "[5] [5]", "100000 1 199999 10000000000"],
            "hint": "С дозорными вставка и удаление одинаковы для всех узлов: _insert_after(left, node) и remove(node) — по четыре присваивания. move_to_front = вырезать узел и вставить после head.",
        },
        {
            "id": "circular-queue",
            "mode": "stdout",
            "title": "Циклическая очередь",
            "statement": (
                "Реализуйте класс CircularQueue(k) — очередь фиксированной ёмкости "
                "k на массиве (кольцевой буфер): enqueue(x) — True, если место "
                "было, иначе False; dequeue() — True, если было что снять, иначе "
                "False; front() и rear() — первый и последний элемент или −1, если "
                "очередь пуста; is_empty() и is_full(). Хранилище — список длины k, "
                "который не растёт; индексы идут по кругу."
            ),
            "starter": "class CircularQueue:\n    def __init__(self, k):\n        self.a = [None] * k\n        self.head = 0\n        self.size = 0\n\n    # enqueue, dequeue, front, rear, is_empty, is_full\n",
            "driver": (
                "q = CircularQueue(3)\n"
                "print(q.enqueue(1), q.enqueue(2), q.enqueue(3), q.enqueue(4))\n"
                "print(q.rear(), q.is_full(), q.dequeue(), q.enqueue(4), q.rear(), q.front())\n"
                "print(q.dequeue(), q.dequeue(), q.dequeue(), q.dequeue(), q.is_empty(), q.front(), q.rear())\n"
                "q = CircularQueue(5)\n"
                "total = 0\n"
                "for i in range(300000):\n"
                "    q.enqueue(i)\n"
                "    if i % 3 != 0:\n"
                "        total += q.front()\n"
                "        q.dequeue()\n"
                "print(total, q.front(), q.rear(), q.is_full(), len(q.a))\n"
            ),
            "expected": ["True True True False", "3 True True True 4 2", "True True True False True -1 -1", "29998700036 299994 299999 False 5"],
            "hint": "head — индекс первого элемента, size — сколько занято. Место для записи: (head + size) % k. Счётчик size отличает пустую очередь от полной.",
        },
        {
            "id": "queue-two-stacks",
            "mode": "stdout",
            "title": "Очередь из двух стопок",
            "statement": (
                "Реализуйте класс MyQueue на двух списках-стопках (разрешены только "
                "append и pop() с конца): push(x), pop() (первый элемент, "
                "IndexError на пустой), peek() (посмотреть первый, IndexError на "
                "пустой) и empty(). Снятие должно стоить амортизированную "
                "константу: переливайте из входной стопки в выходную только когда "
                "выходная пуста."
            ),
            "starter": "class MyQueue:\n    def __init__(self):\n        self.inp = []\n        self.out = []\n\n    # push, pop, peek, empty\n",
            "driver": (
                "q = MyQueue()\n"
                "q.push(1)\n"
                "q.push(2)\n"
                "print(q.peek(), q.pop(), q.empty())\n"
                "q.push(3)\n"
                "print(q.pop(), q.pop(), q.empty())\n"
                "try:\n"
                "    q.pop()\n"
                "except IndexError:\n"
                "    print(\"IndexError\")\n"
                "q = MyQueue()\n"
                "total = 0\n"
                "for i in range(300000):\n"
                "    q.push(i)\n"
                "    if i % 2:\n"
                "        total += q.pop()\n"
                "while not q.empty():\n"
                "    total += q.pop()\n"
                "print(total)\n"
            ),
            "expected": ["1 1 False", "2 3 True", "IndexError", "44999850000"],
            "hint": "Входная стопка принимает push. Когда нужно снять, а выходная пуста — переложите всё из входной в выходную: порядок перевернётся, самый старый окажется сверху.",
        },
        {
            "id": "min-stack",
            "mode": "stdout",
            "title": "Стек с минимумом",
            "statement": (
                "Реализуйте класс MinStack: push(x), pop() (значение; IndexError на "
                "пустом), top() и get_min() — минимальный элемент стека за O(1) "
                "(IndexError на пустом). Подумайте, что хранить рядом с каждым "
                "элементом."
            ),
            "starter": "class MinStack:\n    def __init__(self):\n        self.items = []\n\n    # push, pop, top, get_min\n",
            "driver": (
                "s = MinStack()\n"
                "for v in (5, 3, 7, 3, 8):\n"
                "    s.push(v)\n"
                "print(s.get_min(), s.top())\n"
                "print(s.pop(), s.get_min(), s.pop(), s.get_min(), s.pop(), s.get_min(), s.pop(), s.get_min())\n"
                "try:\n"
                "    MinStack().get_min()\n"
                "except IndexError:\n"
                "    print(\"IndexError\")\n"
                "s = MinStack()\n"
                "acc = 0\n"
                "for i in range(300000):\n"
                "    s.push((i * 7919) % 10007)\n"
                "    acc += s.get_min()\n"
                "for _ in range(300000):\n"
                "    acc -= s.get_min()\n"
                "    s.pop()\n"
                "print(acc)\n"
            ),
            "expected": ["3 8", "8 3 3 3 7 3 3 5", "IndexError", "0"],
            "hint": "Вместе со значением кладите в стопку минимум «на этот момент»: m = min(x, предыдущий минимум). get_min — минимум на вершине.",
        },
    ],
}

_BY_ID = {t["id"]: t for t in _NEW[3]} | KEPT

TASKS: dict[int, list[dict]] = {
    3: [_BY_ID[i] for i in (
        "ll-length-sum",
        "ll-singly-class",
        "reverse-linked-list",
        "middle-node",
        "has-cycle",
        "cycle-start",
        "remove-nth-from-end",
        "merge-sorted-lists",
        "delete-duplicates-sorted",
        "remove-all-value",
        "palindrome-list",
        "add-two-numbers",
        "partition-list",
        "reorder-list",
        "sort-list",
        "list-intersection",
        "doubly-linked-class",
        "circular-queue",
        "queue-two-stacks",
        "min-stack",
    )],
}
