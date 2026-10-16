"""Задачи «Python как первый язык»: глава 24 — send, throw, close, yield from, конвейеры корутин и планировщик.
"""

TASKS: dict[int, list[dict]] = {
    24: [
        {
            "id": "gx-averager",
            "mode": "stdout",
            "title": "Скользящее среднее",
            "statement": (
                'Напишите корутину averager(): она принимает числа через send и после каждого отдаёт текущее среднее всех присланных чисел. Первый next возвращает None (чисел ещё нет).'
            ),
            "starter": (
                'def averager():\n'
                '    pass\n'
            ),
            "driver": (
                'avg = averager()\n'
                'print(next(avg))\n'
                'print(avg.send(10), avg.send(20), avg.send(30))\n'
            ),
            "expected": ['None', '10.0 15.0 20.0'],
            "hint": (
                'Заведите total, count, average = None; в цикле: x = yield average; обновите total, count и average.'
            ),
        },
        {
            "id": "gx-primed",
            "mode": "stdout",
            "title": "Декоратор primed",
            "statement": (
                'Напишите декоратор primed: он оборачивает генераторную функцию так, что вызов возвращает уже «заведённый» генератор (первый next уже сделан), и можно сразу делать send.'
            ),
            "starter": (
                'def primed(func):\n'
                '    pass\n'
            ),
            "driver": (
                'import inspect\n'
                '\n'
                '\n'
                '@primed\n'
                'def collector():\n'
                '    items = []\n'
                '    while True:\n'
                '        item = yield items\n'
                '        items.append(item)\n'
                '\n'
                '\n'
                'c = collector()\n'
                'print(c.send("a"))\n'
                'print(c.send("b"))\n'
                'print(inspect.getgeneratorstate(c))\n'
            ),
            "expected": ["['a']", "['a', 'b']", 'GEN_SUSPENDED'],
            "hint": "Внутри обёртки: gen = func(*args, **kwargs); next(gen); return gen.",
        },
        {
            "id": "gx-throw-reset",
            "mode": "stdout",
            "title": "Счётчик со сбросом через throw",
            "statement": (
                'Напишите генератор counter(): отдаёт 0, 1, 2, … Если снаружи вбросили ValueError (gen.throw(ValueError)), счётчик сбрасывается в 0 и продолжает с нуля. Другие исключения не перехватывайте.'
            ),
            "starter": (
                'def counter():\n'
                '    pass\n'
            ),
            "driver": (
                'c = counter()\n'
                'print(next(c), next(c), next(c))\n'
                'print(c.throw(ValueError))\n'
                'print(next(c))\n'
                'try:\n'
                '    c.throw(KeyError)\n'
                'except KeyError:\n'
                '    print("KeyError пролетел")\n'
            ),
            "expected": ['0 1 2', '0', '1', 'KeyError пролетел'],
            "hint": "while True: try: yield n; n += 1; except ValueError: n = 0.",
        },
        {
            "id": "gx-close-cleanup",
            "mode": "stdout",
            "title": "Уборка при close",
            "statement": (
                'Напишите генератор lines(items): при первом запросе печатает «открыто», затем отдаёт элементы по одному, а при любом завершении — в том числе досрочном через close() — печатает «закрыто».'
            ),
            "starter": (
                'def lines(items):\n'
                '    pass\n'
            ),
            "driver": (
                'g = lines(["a", "b", "c"])\n'
                'print(next(g))\n'
                'g.close()\n'
                'print("после close")\n'
                'for x in lines(["z"]):\n'
                '    print(x)\n'
            ),
            "expected": ['открыто', 'a', 'закрыто', 'после close', 'открыто', 'z', 'закрыто'],
            "hint": 'print("открыто"); try: for item in items: yield item; finally: print("закрыто").',
        },
        {
            "id": "gx-return-value",
            "mode": "stdout",
            "title": "Генератор с итогом",
            "statement": (
                'Напишите генератор summing(items): он отдаёт каждый элемент как есть, а в конце возвращает (return) сумму всех элементов — она окажется в StopIteration.value.'
            ),
            "starter": (
                'def summing(items):\n'
                '    pass\n'
            ),
            "driver": (
                'g = summing([1, 2, 3])\n'
                'items = []\n'
                'try:\n'
                '    while True:\n'
                '        items.append(next(g))\n'
                'except StopIteration as e:\n'
                '    print(items, e.value)\n'
            ),
            "expected": ['[1, 2, 3] 6'],
            "hint": "total = 0; for x in items: total += x; yield x; в конце return total.",
        },
        {
            "id": "gx-chain-sum",
            "mode": "stdout",
            "title": "Делегирование через yield from",
            "statement": (
                'Генератор summing уже написан (отдаёт элементы и возвращает сумму). Напишите chain_sum(a, b): через yield from отдаёт элементы a, затем b, а возвращает общую сумму обоих списков.'
            ),
            "starter": (
                'def summing(items):\n'
                '    total = 0\n'
                '    for x in items:\n'
                '        total += x\n'
                '        yield x\n'
                '    return total\n'
                '\n'
                '\n'
                'def chain_sum(a, b):\n'
                '    pass\n'
            ),
            "driver": (
                'g = chain_sum([1, 2], [3, 4])\n'
                'items = []\n'
                'try:\n'
                '    while True:\n'
                '        items.append(next(g))\n'
                'except StopIteration as e:\n'
                '    print(items, e.value)\n'
            ),
            "expected": ['[1, 2, 3, 4] 10'],
            "hint": "first = yield from summing(a); second = yield from summing(b); return first + second.",
        },
        {
            "id": "gx-flatten",
            "mode": "stdout",
            "title": "Разворачиваем вложенные списки",
            "statement": (
                'Напишите генератор flatten(items): рекурсивно отдаёт все элементы вложенных списков и кортежей по порядку. Строки считайте листьями (не разбирайте на символы). Используйте yield from.'
            ),
            "starter": (
                'def flatten(items):\n'
                '    pass\n'
            ),
            "driver": (
                'print(list(flatten([1, [2, [3, 4]], "ab", [[5]], (6, 7)])))\n'
                'print(list(flatten([])))\n'
            ),
            "expected": ["[1, 2, 3, 4, 'ab', 5, 6, 7]", '[]'],
            "hint": "for x in items: if isinstance(x, (list, tuple)): yield from flatten(x); else: yield x.",
        },
        {
            "id": "gx-filter-stage",
            "mode": "stdout",
            "title": "Стадия конвейера",
            "statement": (
                'Напишите корутину keep(pred, target): она принимает значения через send и передаёт в target.send(...) только те, для которых pred(значение) истинно. Первый next (заведение корутины) сделает проверка.'
            ),
            "starter": (
                'def keep(pred, target):\n'
                '    pass\n'
            ),
            "driver": (
                'got = []\n'
                '\n'
                '\n'
                'def sink():\n'
                '    while True:\n'
                '        got.append((yield))\n'
                '\n'
                '\n'
                's = sink()\n'
                'next(s)\n'
                'f = keep(lambda x: x % 2 == 0, s)\n'
                'next(f)\n'
                'for i in range(7):\n'
                '    f.send(i)\n'
                'print(got)\n'
            ),
            "expected": ['[0, 2, 4, 6]'],
            "hint": "while True: item = yield; if pred(item): target.send(item).",
        },
        {
            "id": "gx-round-robin",
            "mode": "stdout",
            "title": "Планировщик по кругу",
            "statement": (
                'Напишите run(tasks): список генераторов-задач выполняется по кругу — на каждом шаге берётся первая задача, запрашивается одно значение (next), оно добавляется в результат, а незавершённая задача уходит в конец очереди. Завершившаяся (StopIteration) убирается. Верните список полученных значений.'
            ),
            "starter": (
                'from collections import deque\n'
                '\n'
                '\n'
                'def run(tasks):\n'
                '    pass\n'
            ),
            "driver": (
                'def worker(name, n):\n'
                '    for i in range(n):\n'
                '        yield f"{name}{i}"\n'
                '\n'
                '\n'
                'print(run([worker("a", 2), worker("b", 3), worker("c", 1)]))\n'
                'print(run([]))\n'
            ),
            "expected": ["['a0', 'b0', 'c0', 'a1', 'b1', 'b2']", '[]'],
            "hint": (
                'queue = deque(tasks); пока queue: task = queue.popleft(); try: out.append(next(task)); queue.append(task); except StopIteration: pass.'
            ),
        },
    ],
}
