"""Задачи книги «Алгоритмы и структуры данных»: глава 12."""

TASKS: dict[int, list[dict]] = {
    12: [
        {
            "id": "heap-indices",
            "mode": "stdout",
            "title": "Индексы и проверка кучи",
            "statement": (
                "Куча лежит в списке: корень — a[0]. Напишите функции parent(i), "
                "left(i), right(i) (индексы родителя и детей) и first_violation(a): "
                "для минимальной кучи верните кортеж (индекс родителя, индекс "
                "ребёнка) первой пары, где родитель БОЛЬШЕ ребёнка (перебор детей "
                "по возрастанию индекса), или None, если свойство кучи выполнено."
            ),
            "starter": "def parent(i):\n    pass\n\n\ndef left(i):\n    pass\n\n\ndef right(i):\n    pass\n\n\ndef first_violation(a):\n    pass\n",
            "driver": (
                "print([parent(i) for i in range(1, 8)], [left(i) for i in range(4)], [right(i) for i in range(4)])\n"
                "print(first_violation([1, 3, 2, 7, 4, 5, 6]), first_violation([1, 3, 2, 7, 0]), first_violation([2, 1]), first_violation([]), first_violation([5]))\n"
                "print(first_violation(list(range(200000))), first_violation([0] + list(range(1, 100000)) + [-1]))\n"
            ),
            "expected": ["[0, 0, 1, 1, 2, 2, 3] [1, 3, 5, 7] [2, 4, 6, 8]", "None (1, 4) (0, 1) None None", "None (49999, 100000)"],
            "hint": "parent(i) = (i − 1) // 2; left(i) = 2i + 1; right(i) = 2i + 2. Свойство кучи достаточно проверить для каждого i ≥ 1: a[parent(i)] ≤ a[i].",
        },
        {
            "id": "heap-sift-up",
            "mode": "stdout",
            "title": "Просеивание вверх",
            "statement": (
                "Напишите функцию sift_up(a, i): элемент a[i] поднимается вверх по "
                "минимальной куче, пока он МЕНЬШЕ родителя (обмен с родителем). "
                "Список меняется на месте; верните число сделанных обменов."
            ),
            "starter": "def sift_up(a, i):\n    pass\n",
            "driver": (
                "a = [1, 3, 2, 7, 4, 5, 6, 0]\n"
                "print(sift_up(a, 7), a)\n"
                "b = [1, 3, 2, 7, 4, 5, 6, 8]\n"
                "print(sift_up(b, 7), b)\n"
                "c = [5, 6, 7, 1]\n"
                "print(sift_up(c, 3), c)\n"
                "d = [4]\n"
                "print(sift_up(d, 0), d)\n"
                "e = [2, 2, 2, 2]\n"
                "print(sift_up(e, 3), e)\n"
                "n = 131071\n"
                "big = list(range(1, n)) + [0]\n"
                "print(sift_up(big, n - 1), big[0], big[1], big[2])\n"
            ),
            "expected": ["3 [0, 1, 2, 3, 4, 5, 6, 7]", "0 [1, 3, 2, 7, 4, 5, 6, 8]", "2 [1, 5, 7, 6]", "0 [4]", "0 [2, 2, 2, 2]", "16 0 2 1"],
            "hint": "Пока i > 0: p = (i − 1) // 2; если a[i] < a[p] — меняем местами и i = p; иначе стоп. Равные не обмениваются (строго меньше).",
        },
        {
            "id": "heap-sift-down",
            "mode": "stdout",
            "title": "Просеивание вниз",
            "statement": (
                "Напишите функцию sift_down(a, i, n): элемент a[i] опускается по "
                "минимальной куче из первых n элементов списка (a[n:] не трогать). "
                "Выбор: c = левый ребёнок; если правый существует (< n) и СТРОГО "
                "меньше левого — c = правый; если a[c] < a[i] — обмен и продолжаем "
                "с c, иначе стоп. Список меняется на месте; верните число обменов."
            ),
            "starter": "def sift_down(a, i, n):\n    pass\n",
            "driver": (
                "a = [7, 1, 2, 3, 4, 5, 6]\n"
                "print(sift_down(a, 0, 7), a)\n"
                "b = [9, 2, 2, 5, 6, 3, 4]\n"
                "print(sift_down(b, 0, 7), b)\n"
                "c = [0, 5, 6]\n"
                "print(sift_down(c, 0, 3), c)\n"
                "d = [8, 1, 2, 0]\n"
                "print(sift_down(d, 0, 3), d)\n"
                "e = [3]\n"
                "print(sift_down(e, 0, 1), e)\n"
                "n = 131071\n"
                "big = [10**9] + list(range(1, n))\n"
                "print(sift_down(big, 0, n), big[0], big[1], big[2], big[n - 1])\n"
            ),
            "expected": ["2 [1, 3, 2, 7, 4, 5, 6]", "2 [2, 5, 2, 9, 6, 3, 4]", "0 [0, 5, 6]", "1 [1, 8, 2, 0]", "0 [3]", "16 1 3 2 131070"],
            "hint": "Выбор ребёнка: c = 2i + 1; если c + 1 < n и a[c + 1] < a[c] — c += 1. Если a[c] < a[i] — меняем и идём вниз, иначе выходим. При n граница кучи — a[n:] не смотрим.",
        },
        {
            "id": "heap-push",
            "mode": "stdout",
            "title": "Вставка в кучу",
            "statement": (
                "Напишите функцию heap_push(a, x): добавьте x в минимальную кучу a "
                "(список меняется на месте): в конец и просеивание вверх. Проверка "
                "добавляет 200 000 чисел."
            ),
            "starter": "def heap_push(a, x):\n    pass\n",
            "driver": (
                "def ok(a):\n"
                "    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))\n"
                "\n"
                "\n"
                "def rnd(n, seed, mod=10**9):\n"
                "    x = seed\n"
                "    out = []\n"
                "    for _ in range(n):\n"
                "        x = (x * 1103515245 + 12345) % 2147483648\n"
                "        out.append(x % mod)\n"
                "    return out\n"
                "\n"
                "\n"
                "h = []\n"
                "for x in (5, 3, 8, 1, 9, 2):\n"
                "    heap_push(h, x)\n"
                "    print(h)\n"
                "big = []\n"
                "for v in rnd(200000, 3):\n"
                "    heap_push(big, v)\n"
                "print(ok(big), big[0] == min(big), len(big))\n"
                "desc = []\n"
                "for v in range(100000, 0, -1):\n"
                "    heap_push(desc, v)\n"
                "print(ok(desc), desc[0])\n"
            ),
            "expected": ["[5]", "[3, 5]", "[3, 5, 8]", "[1, 3, 8, 5]", "[1, 3, 8, 5, 9]", "[1, 3, 2, 5, 9, 8]", "True True 200000", "True 1"],
            "hint": "a.append(x), затем i = len(a) − 1 и цикл просеивания вверх (как в sift_up).",
        },
        {
            "id": "heap-pop",
            "mode": "stdout",
            "title": "Извлечение минимума",
            "statement": (
                "Напишите функцию heap_pop(a): удалите и верните наименьший элемент "
                "минимальной кучи a (на месте): последний элемент перемещается в "
                "корень и просеивается вниз (выбор ребёнка — как в sift_down: "
                "левый, правый если строго меньше). Для пустой кучи — IndexError. "
                "Проверка извлекает 100 000 чисел."
            ),
            "starter": "def heap_pop(a):\n    pass\n",
            "driver": (
                "def ok(a):\n"
                "    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))\n"
                "\n"
                "\n"
                "def rnd(n, seed, mod=10**9):\n"
                "    x = seed\n"
                "    out = []\n"
                "    for _ in range(n):\n"
                "        x = (x * 1103515245 + 12345) % 2147483648\n"
                "        out.append(x % mod)\n"
                "    return out\n"
                "\n"
                "\n"
                "h = [1, 3, 2, 7, 4, 5, 6]\n"
                "print(heap_pop(h), h)\n"
                "print(heap_pop(h), h)\n"
                "print(heap_pop(h), h)\n"
                "one = [4]\n"
                "print(heap_pop(one), one)\n"
                "try:\n"
                "    heap_pop([])\n"
                "except IndexError:\n"
                "    print(\"IndexError\")\n"
                "vals = rnd(100000, 8)\n"
                "big = sorted(vals)\n"
                "big = big[::-1]\n"
                "import heapq\n"
                "heapq.heapify(big)\n"
                "out = [heap_pop(big) for _ in range(len(vals))]\n"
                "print(out == sorted(vals), len(big))\n"
            ),
            "expected": ["1 [2, 3, 5, 7, 4, 6]", "2 [3, 4, 5, 7, 6]", "3 [4, 6, 5, 7]", "4 []", "IndexError", "True 0"],
            "hint": "top = a[0]; last = a.pop(); если куча не пуста — a[0] = last и просеивание вниз (n = len(a)). Не забудьте вернуть top.",
        },
        {
            "id": "heapify-linear",
            "mode": "stdout",
            "title": "Построение кучи за O(n)",
            "statement": (
                "Напишите функцию heapify(a): превратите список в минимальную кучу "
                "на месте, просеивая вниз от последнего родителя к корню. Проверка "
                "считает сравнения элементов на 100 000 числах по убыванию (худший "
                "случай): не более 3n — построение вставками не пройдёт."
            ),
            "starter": "def heapify(a):\n    pass\n",
            "driver": (
                "class C:\n"
                "    cnt = 0\n"
                "\n"
                "    def __init__(self, v):\n"
                "        self.v = v\n"
                "\n"
                "    def __lt__(self, o):\n"
                "        C.cnt += 1\n"
                "        return self.v < o.v\n"
                "\n"
                "    def __gt__(self, o):\n"
                "        C.cnt += 1\n"
                "        return self.v > o.v\n"
                "\n"
                "    def __le__(self, o):\n"
                "        C.cnt += 1\n"
                "        return self.v <= o.v\n"
                "\n"
                "    def __ge__(self, o):\n"
                "        C.cnt += 1\n"
                "        return self.v >= o.v\n"
                "\n"
                "    def __eq__(self, o):\n"
                "        return self.v == o.v\n"
                "\n"
                "    def __repr__(self):\n"
                "        return str(self.v)\n"
                "\n"
                "\n"
                "def ok(a):\n"
                "    return all(a[(i - 1) // 2].v <= a[i].v for i in range(1, len(a)))\n"
                "\n"
                "\n"
                "a = [9, 4, 7, 1, 3, 8, 2]\n"
                "heapify(a)\n"
                "print(a)\n"
                "print(heapify([]), heapify([5]))\n"
                "n = 100000\n"
                "arr = [C(v) for v in range(n, 0, -1)]\n"
                "heapify(arr)\n"
                "print(ok(arr), arr[0].v, C.cnt <= 3 * n)\n"
                "arr = [C(v) for v in range(0, 100000)]\n"
                "rnd = arr[:]\n"
                "heapify(rnd)\n"
                "print(ok(rnd))\n"
            ),
            "expected": ["[1, 3, 2, 4, 9, 8, 7]", "None None", "True 1 True", "True"],
            "hint": "for start in range(n // 2 − 1, −1, −1): просеивание вниз элемента start (sift_down). Листья (индексы от n // 2) уже кучи.",
        },
        {
            "id": "heap-sort",
            "mode": "stdout",
            "title": "Пирамидальная сортировка",
            "statement": (
                "Напишите функцию heap_sort(a): отсортируйте список по возрастанию "
                "на месте пирамидальной сортировкой: постройте максимальную кучу, "
                "затем N раз меняйте корень с последним элементом неотсортированной "
                "части и просеивайте новый корень вниз. Встроенные "
                "sort/sorted/heapq запрещены по смыслу. Проверка сортирует 100 000 "
                "чисел."
            ),
            "starter": "def heap_sort(a):\n    pass\n",
            "driver": (
                "for src in ([5, 2, 9, 1, 5, 6], [], [1], [2, 1], [3, 3, 3], list(range(10, 0, -1))):\n"
                "    a = list(src)\n"
                "    heap_sort(a)\n"
                "    print(a)\n"
                "src = [(i * 7919) % 100003 for i in range(100000)]\n"
                "a = list(src)\n"
                "heap_sort(a)\n"
                "print(a == sorted(src), a[:3], a[-3:])\n"
            ),
            "expected": ["[1, 2, 5, 5, 6, 9]", "[]", "[1]", "[1, 2]", "[3, 3, 3]", "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]", "True [0, 1, 2] [100000, 100001, 100002]"],
            "hint": "Максимальная куча: просеивание вниз с условием «ребёнок БОЛЬШЕ». Обмен корня с a[end], затем просеивание корня в куче размером end.",
        },
        {
            "id": "heap-pushpop-replace",
            "mode": "stdout",
            "title": "pushpop и replace",
            "statement": (
                "Напишите две функции для минимальной кучи a (список, на месте): "
                "heap_pushpop(a, x) — «положить x, затем достать минимум»: если "
                "куча пуста или x не больше a[0], вернуть x, не трогая кучу; иначе "
                "вернуть старый корень, поставив на его место x и просеяв вниз. "
                "heap_replace(a, x) — «достать минимум, затем положить x»: всегда "
                "возвращает старый корень, ставит x на его место и просеивает вниз; "
                "для пустой кучи — IndexError."
            ),
            "starter": "def heap_pushpop(a, x):\n    pass\n\n\ndef heap_replace(a, x):\n    pass\n",
            "driver": (
                "import heapq\n"
                "\n"
                "\n"
                "def ok(a):\n"
                "    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))\n"
                "\n"
                "\n"
                "h = [1, 3, 2, 7, 4, 5, 6]\n"
                "print(heap_pushpop(h, 0), h)\n"
                "print(heap_pushpop(h, 9), h, ok(h))\n"
                "print(heap_replace(h, 0), h, ok(h))\n"
                "print(heap_pushpop([], 5), heap_pushpop([2], 2))\n"
                "try:\n"
                "    heap_replace([], 1)\n"
                "except IndexError:\n"
                "    print(\"IndexError\")\n"
                "x = 3\n"
                "mine, ref = [], []\n"
                "good = True\n"
                "for i in range(20000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    v = x % 1000\n"
                "    if i % 3 == 0 or not mine:\n"
                "        mine.append(v)\n"
                "        ref.append(v)\n"
                "        heapq.heapify(mine)\n"
                "        heapq.heapify(ref)\n"
                "    elif i % 3 == 1:\n"
                "        good = good and heap_pushpop(mine, v) == heapq.heappushpop(ref, v)\n"
                "    else:\n"
                "        good = good and heap_replace(mine, v) == heapq.heapreplace(ref, v)\n"
                "    good = good and ok(mine) and sorted(mine) == sorted(ref)\n"
                "print(good)\n"
            ),
            "expected": ["0 [1, 3, 2, 7, 4, 5, 6]", "1 [2, 3, 5, 7, 4, 9, 6] True", "2 [0, 3, 5, 7, 4, 9, 6] True", "5 2", "IndexError", "True"],
            "hint": "pushpop: если x не больше корня — он и есть минимум, куча не меняется. Иначе корень уходит, x встаёт на его место и опускается. replace отличается тем, что корень отдаётся всегда.",
        },
        {
            "id": "max-heap-class",
            "mode": "stdout",
            "title": "Максимальная куча",
            "statement": (
                "Реализуйте класс MaxHeap(key=None) — максимальная куча на списке: "
                "push(x), pop() — элемент с наибольшим key(x) (IndexError на "
                "пустой), peek(), len(h). Без key элементы сравниваются сами. "
                "Просеивание пишите сами, модуль heapq не используйте. Проверка "
                "кладёт 100 000 элементов."
            ),
            "starter": "class MaxHeap:\n    def __init__(self, key=None):\n        self.key = key or (lambda x: x)\n        self.a = []\n\n    def __len__(self):\n        return len(self.a)\n\n    # push, pop, peek\n",
            "driver": (
                "h = MaxHeap()\n"
                "for x in (3, 9, 1, 7, 5):\n"
                "    h.push(x)\n"
                "print(len(h), h.peek(), [h.pop() for _ in range(5)], len(h))\n"
                "w = MaxHeap(key=len)\n"
                "for s in (\"aa\", \"b\", \"cccc\", \"ddd\"):\n"
                "    w.push(s)\n"
                "print([w.pop() for _ in range(4)])\n"
                "try:\n"
                "    MaxHeap().pop()\n"
                "except IndexError:\n"
                "    print(\"IndexError\")\n"
                "vals = [(i * 7919) % 100003 for i in range(100000)]\n"
                "big = MaxHeap()\n"
                "for v in vals:\n"
                "    big.push(v)\n"
                "out = [big.pop() for _ in range(len(vals))]\n"
                "print(out == sorted(vals, reverse=True))\n"
            ),
            "expected": ["5 9 [9, 7, 5, 3, 1] 0", "['cccc', 'ddd', 'aa', 'b']", "IndexError", "True"],
            "hint": "То же, что heap_push/heap_pop, но сравнение инвертировано и идёт по key(x): куча хранит сами элементы, а упорядочивает по ключу.",
        },
        {
            "id": "stable-priority-queue",
            "mode": "stdout",
            "title": "Приоритетная очередь с порядком",
            "statement": (
                "Реализуйте класс PriorityQueue: push(priority, item), pop() — "
                "элемент с наименьшим приоритетом; при равных приоритетах — в "
                "порядке добавления (FIFO). Элементы могут быть несравнимыми "
                "(словари, объекты): вторым полем хранимой записи ставьте "
                "возрастающий счётчик. Просеивание — своё, без heapq. pop на пустой "
                "— IndexError. Проверка кладёт 100 000 записей."
            ),
            "starter": "class PriorityQueue:\n    def __init__(self):\n        self.a = []\n        self.n = 0\n\n    def __len__(self):\n        return len(self.a)\n\n    # push(priority, item), pop()\n",
            "driver": (
                "q = PriorityQueue()\n"
                "q.push(2, {\"name\": \"b\"})\n"
                "q.push(1, {\"name\": \"a\"})\n"
                "q.push(2, {\"name\": \"c\"})\n"
                "q.push(1, {\"name\": \"d\"})\n"
                "q.push(3, {\"name\": \"e\"})\n"
                "print([q.pop()[\"name\"] for _ in range(5)], len(q))\n"
                "try:\n"
                "    q.pop()\n"
                "except IndexError:\n"
                "    print(\"IndexError\")\n"
                "big = PriorityQueue()\n"
                "for i in range(100000):\n"
                "    big.push((i * 7919) % 10, i)\n"
                "out = [big.pop() for _ in range(100000)]\n"
                "exp = sorted(range(100000), key=lambda i: ((i * 7919) % 10, i))\n"
                "print(out == exp)\n"
            ),
            "expected": ["['a', 'd', 'b', 'c', 'e'] 0", "IndexError", "True"],
            "hint": "Храните в куче кортежи (приоритет, счётчик, элемент). Сравнивайте только первые два поля (приоритет и счётчик): счётчик уникален, поэтому до самих элементов сравнение не дойдёт.",
        },
        {
            "id": "my-heapq",
            "mode": "stdout",
            "title": "Свой модуль heapq",
            "statement": (
                "Реализуйте функции модуля heapq для минимальной кучи на списке: "
                "heappush(h, x), heappop(h), heapify(h), heappushpop(h, x), "
                "heapreplace(h, x), nsmallest(n, it, key=None), nlargest(n, it, "
                "key=None) и merge(*iterables, key=None) (возвращает итератор по "
                "слитой отсортированной последовательности). Модуль heapq и sorted "
                "не используйте внутри. Проверка сравнивает ваши результаты с "
                "настоящим heapq на сотнях тысяч операций."
            ),
            "starter": "def heappush(h, x):\n    pass\n\n\ndef heappop(h):\n    pass\n\n\ndef heapify(h):\n    pass\n\n\ndef heappushpop(h, x):\n    pass\n\n\ndef heapreplace(h, x):\n    pass\n\n\ndef nsmallest(n, it, key=None):\n    pass\n\n\ndef nlargest(n, it, key=None):\n    pass\n\n\ndef merge(*iterables, key=None):\n    pass\n",
            "driver": (
                "import heapq\n"
                "\n"
                "\n"
                "def ok(a):\n"
                "    return all(a[(i - 1) // 2] <= a[i] for i in range(1, len(a)))\n"
                "\n"
                "\n"
                "h = []\n"
                "for x in (5, 3, 8, 1, 9, 2):\n"
                "    heappush(h, x)\n"
                "print(h[0], ok(h), [heappop(h) for _ in range(6)])\n"
                "a = [9, 4, 7, 1, 3, 8, 2]\n"
                "heapify(a)\n"
                "print(ok(a), a[0])\n"
                "h = [1, 3, 2]\n"
                "print(heappushpop(h, 0), heappushpop(h, 5), ok(h), heapreplace(h, 0), ok(h))\n"
                "x = 11\n"
                "good = True\n"
                "mine, ref = [], []\n"
                "for i in range(200000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    v = x % 5000\n"
                "    r = x % 5\n"
                "    if r < 3 or not mine:\n"
                "        heappush(mine, v)\n"
                "        heapq.heappush(ref, v)\n"
                "    elif r == 3:\n"
                "        good = good and heappop(mine) == heapq.heappop(ref)\n"
                "    else:\n"
                "        good = good and heappushpop(mine, v) == heapq.heappushpop(ref, v)\n"
                "    if i % 20000 == 0:\n"
                "        good = good and ok(mine) and sorted(mine) == sorted(ref)\n"
                "print(good, ok(mine), len(mine) == len(ref))\n"
                "data = [(i * 7919) % 10007 for i in range(50000)]\n"
                "print(nsmallest(5, data) == heapq.nsmallest(5, data), nlargest(5, data) == heapq.nlargest(5, data), nsmallest(3, []), nlargest(0, data))\n"
                "words = [\"pear\", \"fig\", \"banana\", \"kiwi\", \"apple\", \"plum\", \"date\"]\n"
                "print(nsmallest(3, words, key=len) == heapq.nsmallest(3, words, key=len), nlargest(2, words, key=len) == heapq.nlargest(2, words, key=len))\n"
                "lists = [sorted(rnd) for rnd in ([(i * 31 + j * 17) % 1000 for j in range(2000)] for i in range(50))]\n"
                "print(list(merge(*lists)) == list(heapq.merge(*lists)), list(merge([], [1, 2], [])) == [1, 2], list(merge()) == [])\n"
                "print(list(merge([5, 3, 1], [4, 2], key=lambda v: -v)) == list(heapq.merge([5, 3, 1], [4, 2], key=lambda v: -v)))\n"
            ),
            "expected": ["1 True [1, 2, 3, 5, 8, 9]", "True 1", "0 1 True 2 True", "True True True", "True True [] []", "True True", "True True True", "True"],
            "hint": "Основа — две функции: _up (просеивание вверх) и _down (вниз). heappush = append + _up, heappop = последний в корень + _down, heapify — _down от n // 2 − 1 до 0. nsmallest можно через кучу из n лучших; merge — куча из «голов» с номером последовательности.",
        },
        {
            "id": "kth-largest-stream",
            "mode": "stdout",
            "title": "k-й по величине в потоке",
            "statement": (
                "Реализуйте класс KthLargest(k, nums): конструктор принимает k и "
                "начальный список чисел, метод add(val) добавляет число и "
                "возвращает k-й по величине элемент среди всех добавленных. "
                "Гарантируется, что после первого add элементов хватает. "
                "Используйте минимальную кучу размера k (модуль heapq разрешён). "
                "Проверка: 300 000 добавлений."
            ),
            "starter": "import heapq\n\n\nclass KthLargest:\n    def __init__(self, k, nums):\n        pass\n\n    def add(self, val):\n        pass\n",
            "driver": (
                "t = KthLargest(3, [4, 5, 8, 2])\n"
                "print([t.add(v) for v in (3, 5, 10, 9, 4)])\n"
                "u = KthLargest(1, [])\n"
                "print([u.add(v) for v in (-3, -2, -4, 0, 4)])\n"
                "big = KthLargest(100, [])\n"
                "x = 5\n"
                "last = 0\n"
                "total = 0\n"
                "for i in range(300000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    last = big.add(x % 1000000)\n"
                "    if i >= 100:\n"
                "        total += last\n"
                "print(last, total)\n"
            ),
            "expected": ["[4, 5, 5, 8, 8]", "[-3, -2, -2, 0, 4]", "999570 299117860381"],
            "hint": "Куча размера k: в корне k-й по величине. Пока размер меньше k — heappush; иначе, если val больше корня, — heapreplace.",
        },
        {
            "id": "merge-k-sorted",
            "mode": "stdout",
            "title": "Слияние k отсортированных",
            "statement": (
                "Напишите функцию merge_k_lists(lists): слейте k отсортированных "
                "списков в один отсортированный список. Используйте кучу из «голов» "
                "(heapq): время O(N log k). Проверка: 200 списков по 2000 чисел."
            ),
            "starter": "import heapq\n\n\ndef merge_k_lists(lists):\n    pass\n",
            "driver": (
                "print(merge_k_lists([[1, 4, 5], [1, 3, 4], [2, 6]]), merge_k_lists([]), merge_k_lists([[], []]), merge_k_lists([[3], [], [1, 2]]))\n"
                "lists = [sorted((i * 7919 + j * 104729) % 100003 for j in range(2000)) for i in range(200)]\n"
                "r = merge_k_lists(lists)\n"
                "print(len(r), r[:5], r == sorted(v for l in lists for v in l))\n"
            ),
            "expected": ["[1, 1, 2, 3, 4, 4, 5, 6] [] [] [1, 2, 3]", "400000 [0, 0, 0, 0, 0] True"],
            "hint": "В куче — тройки (значение, номер списка, позиция). Достаём минимум, записываем и кладём следующий элемент того же списка (heapreplace); если список кончился — heappop.",
        },
        {
            "id": "median-stream",
            "mode": "stdout",
            "title": "Медиана потока",
            "statement": (
                "Реализуйте класс MedianFinder: add_num(x) и find_median() — "
                "медиана всех добавленных чисел (для чётного количества — среднее "
                "двух средних, вещественное число). Две кучи (heapq): нижняя "
                "половина в максимальной, верхняя — в минимальной. Проверка: 300 "
                "000 добавлений — вставка в отсортированный список не успеет."
            ),
            "starter": "import heapq\n\n\nclass MedianFinder:\n    def __init__(self):\n        pass\n\n    def add_num(self, x):\n        pass\n\n    def find_median(self):\n        pass\n",
            "driver": (
                "m = MedianFinder()\n"
                "out = []\n"
                "for v in (5, 2, 8, 1, 9):\n"
                "    m.add_num(v)\n"
                "    out.append(m.find_median())\n"
                "print(out)\n"
                "m = MedianFinder()\n"
                "m.add_num(-1)\n"
                "m.add_num(-2)\n"
                "print(m.find_median())\n"
                "m = MedianFinder()\n"
                "x = 13\n"
                "acc = 0.0\n"
                "for i in range(300000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    m.add_num(x % 1000000)\n"
                "    if i % 1000 == 0:\n"
                "        acc += m.find_median()\n"
                "print(acc)\n"
            ),
            "expected": ["[5.0, 3.5, 5.0, 3.5, 5.0]", "-1.5", "149821698.0"],
            "hint": "Нижняя половина — max-куча (числа со знаком минус), верхняя — min-куча. После каждой вставки размеры отличаются не больше чем на 1, нижняя не меньше верхней.",
        },
        {
            "id": "min-meeting-rooms",
            "mode": "stdout",
            "title": "Сколько нужно переговорных",
            "statement": (
                "Дан список встреч — пары [начало, конец) (конец не включается: "
                "встреча, закончившаяся в момент t, не мешает встрече, начавшейся в "
                "t). Напишите функцию min_rooms(intervals): наименьшее число "
                "переговорных комнат. Сортировка по началу и куча моментов "
                "окончания (heapq). Проверка: 300 000 встреч."
            ),
            "starter": "import heapq\n\n\ndef min_rooms(intervals):\n    pass\n",
            "driver": (
                "print(min_rooms([[0, 30], [5, 10], [15, 20]]), min_rooms([[7, 10], [2, 4]]), min_rooms([]), min_rooms([[1, 5], [5, 9]]), min_rooms([[1, 4], [2, 5], [3, 6]]))\n"
                "x = 21\n"
                "iv = []\n"
                "for _ in range(300000):\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    s = x % 1000000\n"
                "    x = (x * 1103515245 + 12345) % 2147483648\n"
                "    iv.append([s, s + 1 + x % 500])\n"
                "print(min_rooms(iv))\n"
            ),
            "expected": ["2 1 0 1 3", "111"],
            "hint": "Идём по встречам в порядке начала. В куче — моменты окончания занятых комнат. Освободившиеся (end ≤ start) убираем, новую встречу кладём; максимальный размер кучи — ответ.",
        },
    ],
}
