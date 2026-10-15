"""Задачи «Python как первый язык»: асинхронность (главы 31–33).

Потоки и asyncio проверяются скрытым драйвером; времена в проверках
осторожные (допуск в разы), порядок событий — детерминированный.
"""

TASKS: dict[int, list[dict]] = {
    31: [
        {
            "id": "parallel-map-threads",
            "mode": "stdout",
            "title": "Параллельный map на потоках",
            "statement": (
                "Напишите функцию parallel_map(func, items, workers): "
                "применяет func к каждому элементу в пуле из workers потоков "
                "и возвращает список результатов В ИСХОДНОМ порядке. "
                "Используйте ThreadPoolExecutor."
            ),
            "starter": "from concurrent.futures import ThreadPoolExecutor\n\n\ndef parallel_map(func, items, workers):\n    pass\n",
            "driver": (
                "import time\n"
                "def slow_square(x):\n    time.sleep(0.1)\n    return x * x\n"
                "t0 = time.perf_counter()\nres = parallel_map(slow_square, list(range(8)), 8)\nel = time.perf_counter() - t0\n"
                "print(res)\nprint(el < 0.5)\nprint(parallel_map(str, [], 3))\n"
            ),
            "expected": ["[0, 1, 4, 9, 16, 25, 36, 49]", "True", "[]"],
            "hint": "with ThreadPoolExecutor(max_workers=workers) as pool: return list(pool.map(func, items)).",
        },
        {
            "id": "locked-counter",
            "mode": "stdout",
            "title": "Счётчик под замком",
            "statement": (
                "Напишите функцию count_in_threads(threads, per_thread): "
                "запускает threads потоков, каждый из которых увеличивает "
                "общий счётчик на 1 ровно per_thread раз, и возвращает "
                "итоговое значение. Защитите счётчик замком Lock."
            ),
            "starter": "import threading\n\n\ndef count_in_threads(threads, per_thread):\n    pass\n",
            "driver": "print(count_in_threads(4, 25000))\nprint(count_in_threads(1, 10))\nprint(count_in_threads(8, 0))\n",
            "expected": ["100000", "10", "0"],
            "hint": "Общий счётчик — в списке или через nonlocal; внутри цикла: with lock: counter += 1; в конце join всех потоков.",
        },
        {
            "id": "queue-worker",
            "mode": "stdout",
            "title": "Производитель и потребитель",
            "statement": (
                "Напишите функцию process_with_queue(items): главный поток "
                "кладёт элементы в queue.Queue, один рабочий поток берёт их и "
                "складывает в результат квадраты. Верните список квадратов в "
                "порядке поступления. Для остановки рабочего используйте "
                "сигнальное значение None."
            ),
            "starter": "import queue\nimport threading\n\n\ndef process_with_queue(items):\n    pass\n",
            "driver": "print(process_with_queue([1, 2, 3, 4]))\nprint(process_with_queue([]))\nprint(process_with_queue(range(5)))\n",
            "expected": ["[1, 4, 9, 16]", "[]", "[0, 1, 4, 9, 16]"],
            "hint": "while True: item = q.get(); if item is None: break; results.append(item * item) — после всех элементов положите None и сделайте join.",
        },
        {
            "id": "first-completed",
            "mode": "stdout",
            "title": "Кто быстрее",
            "statement": (
                "Напишите функцию first_done(funcs): запускает все функции "
                "(без аргументов) в пуле потоков и возвращает результат той, "
                "что завершилась ПЕРВОЙ. Используйте as_completed."
            ),
            "starter": "from concurrent.futures import ThreadPoolExecutor, as_completed\n\n\ndef first_done(funcs):\n    pass\n",
            "driver": (
                "import time\n"
                "def make(label, delay):\n    def f():\n        time.sleep(delay)\n        return label\n    return f\n"
                "print(first_done([make('медленная', 0.3), make('быстрая', 0.05), make('средняя', 0.15)]))\n"
                "print(first_done([make('одна', 0.01)]))\n"
            ),
            "expected": ["быстрая", "одна"],
            "hint": "with ThreadPoolExecutor(len(funcs)) as pool: futures = [pool.submit(f) for f in funcs]; for fut in as_completed(futures): return fut.result().",
        },
        {
            "id": "stoppable-ticker",
            "mode": "stdout",
            "title": "Останавливаемый фоновый поток",
            "statement": (
                "Опишите класс Ticker: start() запускает фоновый поток, "
                "который каждые 0.02 секунды увеличивает атрибут ticks на 1; "
                "stop() останавливает его (через threading.Event) и дожидается "
                "завершения. После stop() тики больше не растут."
            ),
            "starter": "import threading\n\n\nclass Ticker:\n    def __init__(self):\n        self.ticks = 0\n",
            "driver": (
                "import time\nt = Ticker()\nt.start()\ntime.sleep(0.25)\nt.stop()\nn = t.ticks\ntime.sleep(0.1)\n"
                "print(n >= 3, t.ticks == n)\nprint(Ticker().ticks)\n"
            ),
            "expected": ["True True", "0"],
            "hint": "self._stop = threading.Event(); в потоке: while not self._stop.is_set(): self.ticks += 1; self._stop.wait(0.02).",
        },
        {
            "id": "limited-parallel",
            "mode": "stdout",
            "title": "Не больше N одновременно",
            "statement": (
                "Напишите функцию run_limited(tasks, limit): запускает все "
                "функции из tasks в потоках, но не позволяет работать "
                "одновременно более limit из них (Semaphore). Дождитесь "
                "завершения всех."
            ),
            "starter": "import threading\n\n\ndef run_limited(tasks, limit):\n    pass\n",
            "driver": (
                "import threading, time\nlock = threading.Lock()\nstate = {'now': 0, 'max': 0, 'done': 0}\n"
                "def task():\n    with lock:\n        state['now'] += 1\n        state['max'] = max(state['max'], state['now'])\n"
                "    time.sleep(0.05)\n    with lock:\n        state['now'] -= 1\n        state['done'] += 1\n"
                "run_limited([task] * 10, 3)\nprint(state['done'], state['max'])\n"
            ),
            "expected": ["10 3"],
            "hint": "sem = threading.Semaphore(limit); обёртка: with sem: task(); на каждую задачу — свой поток, затем join.",
        },
        {
            "id": "collect-with-errors",
            "mode": "stdout",
            "title": "Результаты и ошибки",
            "statement": (
                "Напишите функцию run_all(funcs): запускает функции в пуле "
                "потоков и возвращает список в исходном порядке: для "
                "успешной — ('ok', значение), для упавшей — ('error', "
                "текст исключения)."
            ),
            "starter": "from concurrent.futures import ThreadPoolExecutor\n\n\ndef run_all(funcs):\n    pass\n",
            "driver": (
                "def good():\n    return 42\n"
                "def bad():\n    raise ValueError('сбой')\n"
                "def zero():\n    return 1 / 0\n"
                "print(run_all([good, bad, zero]))\nprint(run_all([]))\n"
            ),
            "expected": ["[('ok', 42), ('error', 'сбой'), ('error', 'division by zero')]", "[]"],
            "hint": "futures = [pool.submit(f) for f in funcs]; затем try: ('ok', fut.result()) / except Exception as e: ('error', str(e)).",
        },
    ],
    32: [
        {
            "id": "async-add-later",
            "mode": "stdout",
            "title": "Первая корутина",
            "statement": (
                "Напишите корутину add_later(a, b, delay=0.01): ждёт delay "
                "секунд (asyncio.sleep) и возвращает a + b."
            ),
            "starter": "import asyncio\n\n\nasync def add_later(a, b, delay=0.01):\n    pass\n",
            "driver": (
                "import asyncio\nprint(asyncio.run(add_later(2, 3)))\n"
                "print(asyncio.run(add_later('а', 'б', delay=0)))\nprint(type(add_later(1, 1)).__name__)\n"
                "async def main():\n    return await add_later(10, 5)\nprint(asyncio.run(main()))\n"
            ),
            "expected": ["5", "аб", "coroutine", "15"],
            "hint": "await asyncio.sleep(delay); return a + b.",
        },
        {
            "id": "async-fetch-all",
            "mode": "stdout",
            "title": "Все сразу",
            "statement": (
                "Напишите корутину fetch_all(delays): для каждой задержки "
                "из списка запускает корутину, которая ждёт столько секунд и "
                "возвращает строку «готово <i>» (i — номер с нуля). Все "
                "ожидания должны идти одновременно (gather); результаты — в "
                "порядке списка."
            ),
            "starter": "import asyncio\n\n\nasync def fetch_all(delays):\n    pass\n",
            "driver": (
                "import asyncio, time\nt0 = time.perf_counter()\nres = asyncio.run(fetch_all([0.3, 0.1, 0.2]))\nel = time.perf_counter() - t0\n"
                "print(res)\nprint(el < 0.5)\nprint(asyncio.run(fetch_all([])))\n"
            ),
            "expected": ["['готово 0', 'готово 1', 'готово 2']", "True", "[]"],
            "hint": "Опишите вложенную async def one(i, d): await asyncio.sleep(d); return f'готово {i}' и верните await asyncio.gather(*(one(i, d) for i, d in enumerate(delays))).",
        },
        {
            "id": "async-with-timeout",
            "mode": "stdout",
            "title": "Ограничение по времени",
            "statement": (
                "Напишите корутину with_timeout(coro, seconds): ждёт "
                "результат корутины coro не дольше seconds секунд; если не "
                "уложилась — возвращает строку «таймаут»."
            ),
            "starter": "import asyncio\n\n\nasync def with_timeout(coro, seconds):\n    pass\n",
            "driver": (
                "import asyncio\nasync def job(delay, value):\n    await asyncio.sleep(delay)\n    return value\n"
                "print(asyncio.run(with_timeout(job(0.05, 'успел'), 1)))\n"
                "print(asyncio.run(with_timeout(job(5, 'не успел'), 0.1)))\n"
            ),
            "expected": ["успел", "таймаут"],
            "hint": "try: return await asyncio.wait_for(coro, seconds) / except TimeoutError: return 'таймаут'.",
        },
        {
            "id": "async-safe-all",
            "mode": "stdout",
            "title": "Результаты и ошибки",
            "statement": (
                "Напишите корутину run_safely(coros): запускает корутины "
                "конкурентно и возвращает список в исходном порядке: "
                "('ok', значение) для успешных и ('error', текст) для "
                "упавших. Используйте gather с return_exceptions=True."
            ),
            "starter": "import asyncio\n\n\nasync def run_safely(coros):\n    pass\n",
            "driver": (
                "import asyncio\nasync def good(x):\n    await asyncio.sleep(0.01)\n    return x\n"
                "async def bad():\n    raise ValueError('сбой')\n"
                "print(asyncio.run(run_safely([good(1), bad(), good(3)])))\nprint(asyncio.run(run_safely([])))\n"
            ),
            "expected": ["[('ok', 1), ('error', 'сбой'), ('ok', 3)]", "[]"],
            "hint": "results = await asyncio.gather(*coros, return_exceptions=True); исключения — экземпляры BaseException.",
        },
        {
            "id": "async-bounded-gather",
            "mode": "stdout",
            "title": "Не больше N сразу",
            "statement": (
                "Напишите корутину bounded_gather(funcs, limit): funcs — "
                "список функций без аргументов, каждая возвращает корутину. "
                "Запустите их конкурентно, но так, чтобы одновременно "
                "выполнялось не больше limit (asyncio.Semaphore). Верните "
                "результаты в исходном порядке."
            ),
            "starter": "import asyncio\n\n\nasync def bounded_gather(funcs, limit):\n    pass\n",
            "driver": (
                "import asyncio\nstate = {'now': 0, 'peak': 0}\n"
                "def make(i):\n    async def job():\n        state['now'] += 1\n        state['peak'] = max(state['peak'], state['now'])\n"
                "        await asyncio.sleep(0.02)\n        state['now'] -= 1\n        return i * i\n    return job\n"
                "res = asyncio.run(bounded_gather([make(i) for i in range(10)], 3))\nprint(res)\nprint(state['peak'])\n"
            ),
            "expected": ["[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]", "3"],
            "hint": "sem = asyncio.Semaphore(limit); async def run(f): async with sem: return await f(); затем gather(*(run(f) for f in funcs)).",
        },
        {
            "id": "async-generator-range",
            "mode": "stdout",
            "title": "Асинхронный генератор",
            "statement": (
                "Напишите асинхронный генератор async_range(n, delay): "
                "отдаёт числа от 0 до n - 1, ожидая delay секунд "
                "(asyncio.sleep) перед каждым."
            ),
            "starter": "import asyncio\n\n\nasync def async_range(n, delay=0.01):\n    pass\n",
            "driver": (
                "import asyncio\nasync def main():\n    out = []\n    async for x in async_range(4):\n        out.append(x)\n"
                "    print(out)\n    print([x async for x in async_range(0)])\n    print(sum([x async for x in async_range(5, 0)]))\n"
                "asyncio.run(main())\n"
            ),
            "expected": ["[0, 1, 2, 3]", "[]", "10"],
            "hint": "async def с yield внутри: for i in range(n): await asyncio.sleep(delay); yield i.",
        },
        {
            "id": "async-queue-workers",
            "mode": "stdout",
            "title": "Пул воркеров",
            "statement": (
                "Напишите корутину process_all(items, workers): положите "
                "items в asyncio.Queue и обработайте их workers корутинами-"
                "воркерами (каждый берёт задание, ждёт 0.01 с и кладёт в "
                "результат квадрат). Верните отсортированный список "
                "квадратов. Воркеров после работы остановите."
            ),
            "starter": "import asyncio\n\n\nasync def process_all(items, workers):\n    pass\n",
            "driver": (
                "import asyncio, time\nt0 = time.perf_counter()\nprint(asyncio.run(process_all(list(range(10)), 5)))\n"
                "print(time.perf_counter() - t0 < 0.5)\nprint(asyncio.run(process_all([], 2)))\n"
            ),
            "expected": ["[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]", "True", "[]"],
            "hint": "workers = [asyncio.create_task(worker()) ...]; await q.join(); затем cancel() у воркеров.",
        },
        {
            "id": "async-retry",
            "mode": "stdout",
            "title": "Повторные попытки",
            "statement": (
                "Напишите корутину retry(make_coro, attempts, delay=0.01): "
                "вызывает make_coro() (возвращает корутину), и если она "
                "падает с исключением — ждёт delay и пробует снова, всего "
                "attempts раз. Если все попытки неудачны — поднимает "
                "последнее исключение."
            ),
            "starter": "import asyncio\n\n\nasync def retry(make_coro, attempts, delay=0.01):\n    pass\n",
            "driver": (
                "import asyncio\ncalls = {'n': 0}\n"
                "async def flaky():\n    calls['n'] += 1\n    if calls['n'] < 3:\n        raise ConnectionError('нет связи')\n    return 'успех'\n"
                "print(asyncio.run(retry(flaky, 5)), calls['n'])\n"
                "async def always_bad():\n    raise ValueError('вечный сбой')\n"
                "try:\n    asyncio.run(retry(always_bad, 3))\nexcept ValueError as e:\n    print('сдались:', e)\n"
            ),
            "expected": ["успех 3", "сдались: вечный сбой"],
            "hint": "for i in range(attempts): try: return await make_coro() / except Exception as e: last = e; await asyncio.sleep(delay); после цикла raise last.",
        },
    ],
    33: [
        {
            "id": "tcp-roundtrip",
            "mode": "stdout",
            "title": "Свой TCP-сервер",
            "statement": (
                "Напишите корутину shout(text): поднимите asyncio-сервер на "
                "127.0.0.1 (порт 0), который читает строку, отвечает ею же "
                "заглавными буквами; подключитесь клиентом, отправьте "
                "text + перевод строки и верните ответ сервера (без "
                "перевода строки)."
            ),
            "starter": "import asyncio\n\n\nasync def shout(text):\n    pass\n",
            "driver": (
                "import asyncio\nprint(asyncio.run(shout('привет')))\nprint(asyncio.run(shout('abc def')))\n"
            ),
            "expected": ["ПРИВЕТ", "ABC DEF"],
            "hint": "start_server(handle, '127.0.0.1', 0); порт — server.sockets[0].getsockname()[1]; не забудьте drain и закрытие writer.",
        },
        {
            "id": "async-run-commands",
            "mode": "stdout",
            "title": "Команды одновременно",
            "statement": (
                "Напишите корутину run_codes(codes): для каждой строки кода "
                "запускает дочерний интерпретатор (sys.executable, '-c', "
                "код) через asyncio.create_subprocess_exec, и возвращает "
                "список выводов (stdout без пробелов по краям) в исходном "
                "порядке. Все процессы должны идти одновременно."
            ),
            "starter": "import asyncio\nimport sys\n\n\nasync def run_codes(codes):\n    pass\n",
            "driver": (
                "import asyncio\nprint(asyncio.run(run_codes(['print(1 + 1)', 'print(\"привет\")', 'print(sum(range(5)))'])))\n"
                "print(asyncio.run(run_codes([])))\n"
            ),
            "expected": ["['2', 'привет', '10']", "[]"],
            "hint": "async def one(code): proc = await asyncio.create_subprocess_exec(sys.executable, '-c', code, stdout=asyncio.subprocess.PIPE); out, _ = await proc.communicate(); return out.decode().strip().",
        },
        {
            "id": "async-first-success",
            "mode": "stdout",
            "title": "Кто первый",
            "statement": (
                "Напишите корутину first_of(coros): запускает корутины "
                "конкурентно, возвращает результат ПЕРВОЙ завершившейся и "
                "отменяет остальные (asyncio.wait, FIRST_COMPLETED)."
            ),
            "starter": "import asyncio\n\n\nasync def first_of(coros):\n    pass\n",
            "driver": (
                "import asyncio\nfinished = []\n"
                "async def src(name, delay):\n    try:\n        await asyncio.sleep(delay)\n        finished.append(name)\n        return name\n    except asyncio.CancelledError:\n        finished.append('отменён ' + name)\n        raise\n"
                "print(asyncio.run(first_of([src('медленный', 0.4), src('быстрый', 0.05), src('средний', 0.2)])))\n"
                "print(sorted(finished))\n"
            ),
            "expected": ["быстрый", "['быстрый', 'отменён медленный', 'отменён средний']"],
            "hint": "tasks = [asyncio.create_task(c) for c in coros]; done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED); отмените pending и дождитесь их (gather с return_exceptions).",
        },
        {
            "id": "backoff-delays",
            "mode": "stdout",
            "title": "Растущая задержка",
            "statement": (
                "Напишите корутину retry_backoff(func, tries, base): "
                "вызывает корутинную функцию func(); при исключении "
                "ConnectionError ждёт base * 2 ** i секунд (i — номер "
                "неудачной попытки с нуля) через asyncio.sleep и пробует "
                "снова; на последней неудаче поднимает исключение."
            ),
            "starter": "import asyncio\n\n\nasync def retry_backoff(func, tries, base):\n    pass\n",
            "driver": (
                "import asyncio\ndelays = []\n_real = asyncio.sleep\n"
                "async def fake_sleep(d, *a, **k):\n    delays.append(d)\n"
                "asyncio.sleep = fake_sleep\n"
                "calls = {'n': 0}\n"
                "async def flaky():\n    calls['n'] += 1\n    if calls['n'] < 4:\n        raise ConnectionError('нет')\n    return 'ок'\n"
                "print(asyncio.run(retry_backoff(flaky, 6, 0.5)), calls['n'], delays)\n"
                "delays.clear()\nasync def bad():\n    raise ConnectionError('вечно')\n"
                "try:\n    asyncio.run(retry_backoff(bad, 3, 1))\nexcept ConnectionError as e:\n    print('сдались', e, delays)\n"
                "asyncio.sleep = _real\n"
            ),
            "expected": ["ок 4 [0.5, 1.0, 2.0]", "сдались вечно [1, 2]"],
            "hint": "for i in range(tries): try: return await func() / except ConnectionError: if i == tries - 1: raise; await asyncio.sleep(base * 2 ** i).",
        },
        {
            "id": "graceful-workers",
            "mode": "stdout",
            "title": "Аккуратная остановка",
            "statement": (
                "Напишите корутину run_workers(names, duration): запустите по "
                "корутине-воркеру на каждое имя; воркер в цикле делает "
                "await asyncio.sleep(0.01), пока не поставлено событие "
                "остановки, а при завершении (в finally) добавляет своё имя "
                "в список. Через duration секунд поставьте событие и верните "
                "отсортированный список имён остановившихся воркеров."
            ),
            "starter": "import asyncio\n\n\nasync def run_workers(names, duration):\n    pass\n",
            "driver": (
                "import asyncio\nprint(asyncio.run(run_workers(['в', 'а', 'б'], 0.1)))\nprint(asyncio.run(run_workers([], 0.05)))\n"
            ),
            "expected": ["['а', 'б', 'в']", "[]"],
            "hint": "stop = asyncio.Event(); async with asyncio.TaskGroup() as tg: создать задачи; await asyncio.sleep(duration); stop.set().",
        },
        {
            "id": "ctxvar-request-id",
            "mode": "stdout",
            "title": "Номер запроса в контексте",
            "statement": (
                "Опишите переменную request_id = contextvars.ContextVar(…, "
                "default='-') и корутину handle(rid): сохраняет rid в "
                "request_id, ждёт 0.01 с и возвращает строку «<rid>:<значение "
                "request_id>». Параллельные обработчики не должны мешать "
                "друг другу."
            ),
            "starter": "import asyncio\nimport contextvars\n\nrequest_id = None\n\n\nasync def handle(rid):\n    pass\n",
            "driver": (
                "import asyncio\nasync def main():\n    r = await asyncio.gather(handle('a'), handle('b'), handle('c'))\n    print(r)\n    print(request_id.get())\nasyncio.run(main())\n"
            ),
            "expected": ["['a:a', 'b:b', 'c:c']", "-"],
            "hint": 'request_id = contextvars.ContextVar("request_id", default="-"); gather оборачивает каждую корутину в задачу с копией контекста.',
        },
        {
            "id": "async-tests-for-total",
            "mode": "stdout",
            "title": "Тесты для асинхронной функции",
            "statement": (
                "Допишите класс TestTotal (unittest.IsolatedAsyncioTestCase): "
                "тесты корутины total(prices) — сумма чисел списка (для "
                "пустого — 0). Тесты должны пройти на верной реализации и "
                "упасть на каждой из трёх сломанных. Корутину вызывайте "
                "через await."
            ),
            "starter": "import unittest\n\n\nclass TestTotal(unittest.IsolatedAsyncioTestCase):\n    async def test_example(self):\n        pass  # await total([...])\n",
            "driver": (
                "import io\nimport asyncio\n"
                "def run():\n    r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(TestTotal))\n    return r.wasSuccessful() and r.testsRun > 0\n"
                "async def good(p):\n    await asyncio.sleep(0)\n    return sum(p)\n"
                "async def bad1(p):\n    return sum(p[1:])\n"
                "async def bad2(p):\n    return sum(p) if p else None\n"
                "async def bad3(p):\n    return sum(abs(x) for x in p)\n"
                "for name, f in [('верная', good), ('ошибка 1', bad1), ('ошибка 2', bad2), ('ошибка 3', bad3)]:\n"
                "    total = f\n    print(name, 'тесты прошли' if run() else 'тесты упали')\n"
            ),
            "expected": ["верная тесты прошли", "ошибка 1 тесты упали", "ошибка 2 тесты упали", "ошибка 3 тесты упали"],
            "hint": "assertEqual(await total([1, 2, 3]), 6); пустой список → 0; отрицательные числа: await total([5, -3]) == 2; ещё один элемент в начале.",
        },
    ],
}
