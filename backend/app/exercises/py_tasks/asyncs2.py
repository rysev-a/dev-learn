"""Задачи «Python как первый язык»: глава 46 — асинхронные итераторы, генераторы и менеджеры контекста.

Режим stdout со скрытым driver; asyncio.run запускает драйвер.
"""

TASKS: dict[int, list[dict]] = {
    46: [
        {
            "id": "aio-countdown",
            "mode": "stdout",
            "title": "Асинхронный итератор-класс",
            "statement": (
                'Напишите класс AsyncCountdown(n): асинхронный итератор, который отдаёт n, n-1, …, 1 (перед каждым значением делает await asyncio.sleep(0)) и затем поднимает StopAsyncIteration. Используйте __aiter__ и __anext__.'
            ),
            "starter": (
                'import asyncio\n'
                '\n'
                '\n'
                'class AsyncCountdown:\n'
                '    def __init__(self, n):\n'
                '        self.n = n\n'
            ),
            "driver": (
                'async def main():\n'
                '    out = []\n'
                '    async for x in AsyncCountdown(3):\n'
                '        out.append(x)\n'
                '    print(out)\n'
                '    it = aiter(AsyncCountdown(2))\n'
                '    print(await anext(it), await anext(it))\n'
                '    try:\n'
                '        await anext(it)\n'
                '    except StopAsyncIteration:\n'
                '        print("конец")\n'
                '\n'
                '\n'
                'asyncio.run(main())\n'
            ),
            "expected": ['[3, 2, 1]', '2 1', 'конец'],
            "hint": (
                '__aiter__ возвращает self; async def __anext__: если n <= 0 — raise StopAsyncIteration; иначе await asyncio.sleep(0), уменьшить n и вернуть значение.'
            ),
        },
        {
            "id": "aio-agen-pages",
            "mode": "stdout",
            "title": "Постраничный генератор",
            "statement": (
                'Напишите асинхронный генератор items(fetch): fetch(page) — корутина, возвращающая список элементов страницы (страницы нумеруются с 1); пустой список означает конец. Генератор отдаёт элементы по одному и не запрашивает лишних страниц.'
            ),
            "starter": (
                'import asyncio\n'
                '\n'
                '\n'
                'async def items(fetch):\n'
                '    pass\n'
            ),
            "driver": (
                'calls = []\n'
                '\n'
                '\n'
                'async def fetch(page):\n'
                '    calls.append(page)\n'
                '    await asyncio.sleep(0)\n'
                '    data = {1: ["a", "b"], 2: ["c"], 3: []}\n'
                '    return data.get(page, [])\n'
                '\n'
                '\n'
                'async def main():\n'
                '    out = []\n'
                '    async for x in items(fetch):\n'
                '        out.append(x)\n'
                '    print(out, calls)\n'
                '    calls.clear()\n'
                '    async for x in items(fetch):\n'
                '        break\n'
                '    print(calls)\n'
                '\n'
                '\n'
                'asyncio.run(main())\n'
            ),
            "expected": ["['a', 'b', 'c'] [1, 2, 3]", '[1]'],
            "hint": (
                'page = 1; while True: batch = await fetch(page); if not batch: return; for x in batch: yield x; page += 1.'
            ),
        },
        {
            "id": "aio-filter-comp",
            "mode": "stdout",
            "title": "Асинхронное включение",
            "statement": (
                'Напишите async-функцию evens_squared(source): верните список квадратов чётных значений асинхронного источника, используя асинхронное включение списка.'
            ),
            "starter": (
                'import asyncio\n'
                '\n'
                '\n'
                'async def evens_squared(source):\n'
                '    pass\n'
            ),
            "driver": (
                'async def numbers(n):\n'
                '    for i in range(n):\n'
                '        await asyncio.sleep(0)\n'
                '        yield i\n'
                '\n'
                '\n'
                'async def main():\n'
                '    print(await evens_squared(numbers(7)))\n'
                '    print(await evens_squared(numbers(1)))\n'
                '\n'
                '\n'
                'asyncio.run(main())\n'
            ),
            "expected": ['[0, 4, 16, 36]', '[0]'],
            "hint": "return [x * x async for x in source if x % 2 == 0].",
        },
        {
            "id": "aio-async-with",
            "mode": "stdout",
            "title": "Класс-менеджер async with",
            "statement": (
                'Напишите класс Resource: __aenter__ печатает «открыт» и возвращает self (после await asyncio.sleep(0)), __aexit__ печатает «закрыт» и подавляет только KeyError (возвращает True), остальные исключения пропускает.'
            ),
            "starter": (
                'import asyncio\n'
                '\n'
                '\n'
                'class Resource:\n'
                '    pass\n'
            ),
            "driver": (
                'async def main():\n'
                '    async with Resource() as r:\n'
                '        print(type(r).__name__)\n'
                '    async with Resource():\n'
                '        raise KeyError("x")\n'
                '    print("KeyError подавлен")\n'
                '    try:\n'
                '        async with Resource():\n'
                '            raise ValueError("y")\n'
                '    except ValueError:\n'
                '        print("ValueError прошёл")\n'
                '\n'
                '\n'
                'asyncio.run(main())\n'
            ),
            "expected": ['открыт', 'Resource', 'закрыт', 'открыт', 'закрыт', 'KeyError подавлен', 'открыт', 'закрыт', 'ValueError прошёл'],
            "hint": (
                'async def __aexit__(self, et, ev, tb): print("закрыт"); return et is not None and issubclass(et, KeyError).'
            ),
        },
        {
            "id": "aio-asynccontextmanager",
            "mode": "stdout",
            "title": "@asynccontextmanager",
            "statement": (
                'Напишите менеджер connection(name) через @asynccontextmanager: при входе печатает «открыто <name>» и отдаёт словарь {"name": name}, при выходе — в том числе при ошибке в блоке — печатает «закрыто <name>».'
            ),
            "starter": (
                'import asyncio\n'
                'from contextlib import asynccontextmanager\n'
            ),
            "driver": (
                'async def main():\n'
                '    async with connection("db") as c:\n'
                '        print(c)\n'
                '    try:\n'
                '        async with connection("cache"):\n'
                '            raise RuntimeError("сбой")\n'
                '    except RuntimeError as e:\n'
                '        print("ошибка:", e)\n'
                '\n'
                '\n'
                'asyncio.run(main())\n'
            ),
            "expected": ['открыто db', "{'name': 'db'}", 'закрыто db', 'открыто cache', 'закрыто cache', 'ошибка: сбой'],
            "hint": "print вход; try: yield {...}; finally: print выход.",
        },
        {
            "id": "aio-take-aclosing",
            "mode": "stdout",
            "title": "Взять первые n и закрыть генератор",
            "statement": (
                'Напишите async-функцию take(agen, n): верните список первых n элементов асинхронного генератора и гарантируйте, что генератор закрыт к моменту возврата (его блок finally уже выполнен) — используйте contextlib.aclosing.'
            ),
            "starter": (
                'import asyncio\n'
                'from contextlib import aclosing\n'
                '\n'
                '\n'
                'async def take(agen, n):\n'
                '    pass\n'
            ),
            "driver": (
                'async def numbers():\n'
                '    try:\n'
                '        i = 0\n'
                '        while True:\n'
                '            await asyncio.sleep(0)\n'
                '            yield i\n'
                '            i += 1\n'
                '    finally:\n'
                '        print("очистка")\n'
                '\n'
                '\n'
                'async def main():\n'
                '    first = await take(numbers(), 2)\n'
                '    print(first)\n'
                '    print(await take(numbers(), 0))\n'
                '\n'
                '\n'
                'asyncio.run(main())\n'
            ),
            "expected": ['очистка', '[0, 1]', 'очистка', '[]'],
            "hint": (
                'async with aclosing(agen) as g: out = []; async for x in g: if len(out) == n: break; out.append(x). Длину out проверяйте до добавления элемента.'
            ),
        },
        {
            "id": "aio-interleave",
            "mode": "stdout",
            "title": "Чередование потоков",
            "statement": (
                'Напишите асинхронный генератор interleave(*sources): по кругу берёт по одному элементу из каждого непустого асинхронного источника (через anext) и отдаёт их; источники, исчерпавшие элементы, пропускаются; работа заканчивается, когда исчерпаны все.'
            ),
            "starter": (
                'import asyncio\n'
                '\n'
                '\n'
                'async def interleave(*sources):\n'
                '    pass\n'
            ),
            "driver": (
                'async def gen(name, n):\n'
                '    for i in range(n):\n'
                '        await asyncio.sleep(0)\n'
                '        yield f"{name}{i}"\n'
                '\n'
                '\n'
                'async def main():\n'
                '    print([x async for x in interleave(gen("a", 2), gen("b", 3), gen("c", 1))])\n'
                '    print([x async for x in interleave()])\n'
                '\n'
                '\n'
                'asyncio.run(main())\n'
            ),
            "expected": ["['a0', 'b0', 'c0', 'a1', 'b1', 'b2']", '[]'],
            "hint": (
                'active = list(sources); пока active: для каждого источника попробуйте await anext(src); при StopAsyncIteration уберите его из списка.'
            ),
        },
        {
            "id": "aio-batched",
            "mode": "stdout",
            "title": "Пачки из асинхронного потока",
            "statement": (
                'Напишите асинхронный генератор batched(source, n): собирает элементы источника в списки по n штук и отдаёт их; последняя пачка может быть короче. n ≥ 1.'
            ),
            "starter": (
                'import asyncio\n'
                '\n'
                '\n'
                'async def batched(source, n):\n'
                '    pass\n'
                '    yield\n'
            ),
            "driver": (
                'async def numbers(k):\n'
                '    for i in range(k):\n'
                '        await asyncio.sleep(0)\n'
                '        yield i\n'
                '\n'
                '\n'
                'async def main():\n'
                '    print([b async for b in batched(numbers(7), 3)])\n'
                '    print([b async for b in batched(numbers(4), 2)])\n'
                '    print([b async for b in batched(numbers(0), 5)])\n'
                '\n'
                '\n'
                'asyncio.run(main())\n'
            ),
            "expected": ['[[0, 1, 2], [3, 4, 5], [6]]', '[[0, 1], [2, 3]]', '[]'],
            "hint": (
                'batch = []; async for x in source: batch.append(x); если len == n — yield batch; batch = []; в конце, если batch не пуст — yield batch.'
            ),
        },
        {
            "id": "aio-limiter",
            "mode": "stdout",
            "title": "Ограничитель параллелизма",
            "statement": (
                'Напишите класс Limiter(n) — асинхронный менеджер контекста, который пускает внутрь блока не больше n корутин одновременно (на основе asyncio.Semaphore). __aenter__ захватывает место, __aexit__ освобождает.'
            ),
            "starter": (
                'import asyncio\n'
                '\n'
                '\n'
                'class Limiter:\n'
                '    def __init__(self, n):\n'
                '        pass\n'
            ),
            "driver": (
                'active = 0\n'
                'peak = 0\n'
                '\n'
                '\n'
                'async def job(limiter, i):\n'
                '    global active, peak\n'
                '    async with limiter:\n'
                '        active += 1\n'
                '        peak = max(peak, active)\n'
                '        await asyncio.sleep(0)\n'
                '        await asyncio.sleep(0)\n'
                '        active -= 1\n'
                '    return i\n'
                '\n'
                '\n'
                'async def main():\n'
                '    limiter = Limiter(2)\n'
                '    results = await asyncio.gather(*(job(limiter, i) for i in range(5)))\n'
                '    print(results, peak)\n'
                '\n'
                '\n'
                'asyncio.run(main())\n'
            ),
            "expected": ['[0, 1, 2, 3, 4] 2'],
            "hint": (
                'self._sem = asyncio.Semaphore(n); async def __aenter__(self): await self._sem.acquire(); async def __aexit__(...): self._sem.release().'
            ),
        },
    ],
}
