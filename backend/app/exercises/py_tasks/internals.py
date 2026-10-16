"""Задачи «Python как первый язык»: Питон изнутри (главы 47–49) — память и слабые ссылки, байт-код и GIL, производительность.

Ключ — номер главы. Режим stdout со скрытым driver. В главе 49 заготовки — «наивные» решения: они верны, но не укладываются в лимит времени песочницы.
"""

TASKS: dict[int, list[dict]] = {
    47: [
        {
            "id": "mem-weak-cache",
            "mode": "stdout",
            "title": "Кэш без утечек",
            "statement": (
                'Напишите ObjectCache на WeakValueDictionary: метод get(key, factory) возвращает кэшированный объект, а если его нет (или он уже умер), создаёт через factory() и запоминает; __len__ — число живых записей. Кэш не должен продлевать жизнь объектов.'
            ),
            "starter": (
                'import weakref\n'
                '\n'
                '\n'
                'class ObjectCache:\n'
                '    pass\n'
            ),
            "driver": (
                'import gc\n'
                '\n'
                '\n'
                'class Thing:\n'
                '    pass\n'
                '\n'
                '\n'
                'c = ObjectCache()\n'
                'a = c.get("x", Thing)\n'
                'b = c.get("x", Thing)\n'
                'print(a is b, len(c))\n'
                'del a, b\n'
                'gc.collect()\n'
                'print(len(c))\n'
            ),
            "expected": ['True 1', '0'],
            "hint": (
                'self._data = weakref.WeakValueDictionary(); get: obj = self._data.get(key); если None — создать и положить.'
            ),
        },
        {
            "id": "mem-weak-callback",
            "mode": "stdout",
            "title": "Слабая ссылка с обратным вызовом",
            "statement": (
                'Напишите watch(obj, callback): возвращает слабую ссылку на obj, которая при смерти объекта вызывает callback(имя_типа), где имя_типа — type(obj).__name__, запомненное заранее.'
            ),
            "starter": (
                'import weakref\n'
                '\n'
                '\n'
                'def watch(obj, callback):\n'
                '    pass\n'
            ),
            "driver": (
                'class Thing:\n'
                '    pass\n'
                '\n'
                '\n'
                'log = []\n'
                't = Thing()\n'
                'r = watch(t, log.append)\n'
                'print(r() is t, log)\n'
                'del t\n'
                'print(log, r())\n'
            ),
            "expected": ['True []', "['Thing'] None"],
            "hint": "name = type(obj).__name__; return weakref.ref(obj, lambda _ref: callback(name)).",
        },
        {
            "id": "mem-finalize",
            "mode": "stdout",
            "title": "finalize вместо __del__",
            "statement": (
                'Напишите track(name, log): создаёт и возвращает объект Handle, а через weakref.finalize регистрирует запись «закрыт <name>» в список log при смерти объекта. Класс Handle без __del__.'
            ),
            "starter": (
                'import weakref\n'
                '\n'
                '\n'
                'class Handle:\n'
                '    pass\n'
                '\n'
                '\n'
                'def track(name, log):\n'
                '    pass\n'
            ),
            "driver": (
                'log = []\n'
                'h = track("a", log)\n'
                'print(log)\n'
                'del h\n'
                'print(log)\n'
                'h2 = track("b", log)\n'
                'print(log, type(h2).__name__, hasattr(Handle, "__del__"))\n'
            ),
            "expected": ['[]', "['закрыт a']", "['закрыт a'] Handle False"],
            "hint": 'h = Handle(); weakref.finalize(h, log.append, f"закрыт {name}"); return h.',
        },
        {
            "id": "mem-cycle-gc",
            "mode": "stdout",
            "title": "Цикл и сборщик мусора",
            "statement": (
                'Напишите cycle_demo(): отключите сборщик (gc.disable()), создайте два объекта Node, ссылающихся друг на друга, возьмите слабую ссылку на первый и удалите оба имени; верните кортеж (жив_до_сборки, жив_после_сборки), где «после» — после gc.collect(). В конце включите сборщик обратно.'
            ),
            "starter": (
                'import gc\n'
                'import weakref\n'
                '\n'
                '\n'
                'class Node:\n'
                '    pass\n'
                '\n'
                '\n'
                'def cycle_demo():\n'
                '    pass\n'
            ),
            "driver": (
                'print(cycle_demo())\n'
                'print(gc.isenabled())\n'
            ),
            "expected": ['(True, False)', 'True'],
            "hint": (
                'a.other = b; b.other = a; ref = weakref.ref(a); del a, b; before = ref() is not None; gc.collect(); after = ref() is not None; в finally — gc.enable().'
            ),
        },
        {
            "id": "mem-deepcopy-protocol",
            "mode": "stdout",
            "title": "Свой __deepcopy__",
            "statement": (
                'У Document есть текст, кэш (словарь) и список дочерних документов. Напишите __deepcopy__(self, memo): текст и дочерние документы копируются глубоко (передайте memo), а кэш в копии должен быть новым пустым словарём.'
            ),
            "starter": (
                'class Document:\n'
                '    def __init__(self, text, children=None):\n'
                '        self.text = text\n'
                '        self.children = children or []\n'
                '        self.cache = {}\n'
            ),
            "driver": (
                'import copy\n'
                '\n'
                'd = Document("root", [Document("child")])\n'
                'd.cache["k"] = 1\n'
                'd.children[0].cache["z"] = 2\n'
                'c = copy.deepcopy(d)\n'
                'print(c.text, c.children[0].text, c.cache, c.children[0].cache)\n'
                'print(c is not d, c.children[0] is not d.children[0], d.cache)\n'
            ),
            "expected": ['root child {} {}', "True True {'k': 1}"],
            "hint": (
                'new = type(self)(self.text, copy.deepcopy(self.children, memo)); return new (кэш создаётся пустым в __init__). Не забудьте import copy.'
            ),
        },
        {
            "id": "mem-peak-bytes",
            "mode": "stdout",
            "title": "Пик памяти через tracemalloc",
            "statement": (
                'Напишите peak_bytes(func): запустите tracemalloc, вызовите func(), верните пиковое число выделенных байт (get_traced_memory()[1]) и остановите tracemalloc.'
            ),
            "starter": (
                'import tracemalloc\n'
                '\n'
                '\n'
                'def peak_bytes(func):\n'
                '    pass\n'
            ),
            "driver": (
                'big = peak_bytes(lambda: [0] * 100000)\n'
                'small = peak_bytes(lambda: None)\n'
                'print(big > 700000, small < 5000)\n'
                'print(tracemalloc.is_tracing())\n'
            ),
            "expected": ['True True', 'False'],
            "hint": (
                'tracemalloc.start(); func(); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop(); return peak.'
            ),
        },
        {
            "id": "mem-lazy-sum",
            "mode": "stdout",
            "title": "Сумма квадратов без списка",
            "statement": (
                'Функция sum_squares(n) считает сумму квадратов 0..n-1, но строит для этого весь список. Перепишите её так, чтобы лишние данные в памяти не накапливались (генераторное выражение), результат не должен измениться.'
            ),
            "starter": (
                'def sum_squares(n):\n'
                '    squares = [i * i for i in range(n)]\n'
                '    return sum(squares)\n'
            ),
            "driver": (
                'import tracemalloc\n'
                '\n'
                'tracemalloc.start()\n'
                'result = sum_squares(100000)\n'
                'peak = tracemalloc.get_traced_memory()[1]\n'
                'tracemalloc.stop()\n'
                'print(result)\n'
                'print(peak < 50000)\n'
            ),
            "expected": ['333328333350000', 'True'],
            "hint": "return sum(i * i for i in range(n)).",
        },
        {
            "id": "mem-lru-bound",
            "mode": "stdout",
            "title": "Ограничить кэш",
            "statement": (
                'slow_square кэширует результаты без ограничения (maxsize=None), поэтому память растёт вечно. Ограничьте кэш 128 записями, чтобы последние вызовы по-прежнему попадали в кэш.'
            ),
            "starter": (
                'from functools import lru_cache\n'
                '\n'
                '\n'
                '@lru_cache(maxsize=None)\n'
                'def slow_square(n):\n'
                '    return n * n\n'
            ),
            "driver": (
                'for i in range(1000):\n'
                '    slow_square(i)\n'
                'info = slow_square.cache_info()\n'
                'print(info.currsize, info.maxsize)\n'
                'slow_square(999)\n'
                'print(slow_square.cache_info().hits)\n'
            ),
            "expected": ['128 128', '1'],
            "hint": "@lru_cache(maxsize=128).",
        },
        {
            "id": "mem-memoryview",
            "mode": "stdout",
            "title": "Срез без копирования",
            "statement": (
                'Напишите middle(data, start, stop): верните срез буфера data[start:stop] как memoryview (без копирования), чтобы изменения в исходном bytearray были видны через срез, а запись через срез меняла исходный буфер.'
            ),
            "starter": (
                'def middle(data, start, stop):\n'
                '    pass\n'
            ),
            "driver": (
                'data = bytearray(b"abcdef")\n'
                'v = middle(data, 1, 4)\n'
                'print(bytes(v))\n'
                'data[2] = ord("X")\n'
                'print(bytes(v))\n'
                'v[0] = ord("B")\n'
                'print(data)\n'
                'print(v.obj is data)\n'
            ),
            "expected": ["b'bcd'", "b'bXd'", "bytearray(b'aBXdef')", 'True'],
            "hint": "return memoryview(data)[start:stop].",
        },
    ],
    48: [
        {
            "id": "in-pyc-path",
            "mode": "stdout",
            "title": "Где лежит .pyc",
            "statement": (
                'Напишите pyc_path(source): путь к файлу кэша байт-кода для исходника (используйте importlib.util.cache_from_source). Для /app/mod.py это /app/__pycache__/mod.<метка-версии>.pyc.'
            ),
            "starter": (
                'import importlib.util\n'
                '\n'
                '\n'
                'def pyc_path(source):\n'
                '    pass\n'
            ),
            "driver": (
                'import sys\n'
                '\n'
                'p = pyc_path("/app/mod.py")\n'
                'print(p == f"/app/__pycache__/mod.{sys.implementation.cache_tag}.pyc")\n'
                'print(p.startswith("/app/__pycache__/"), p.endswith(".pyc"))\n'
            ),
            "expected": ['True', 'True True'],
            "hint": "importlib.util.cache_from_source(source).",
        },
        {
            "id": "in-switch-interval",
            "mode": "stdout",
            "title": "Временный интервал переключения",
            "statement": (
                'Напишите менеджер контекста switch_interval(value): внутри блока sys.getswitchinterval() равен value, а после выхода (даже при ошибке) возвращается прежнее значение. Реализуйте через @contextmanager и sys.setswitchinterval.'
            ),
            "starter": (
                'import sys\n'
                'from contextlib import contextmanager\n'
            ),
            "driver": (
                'before = sys.getswitchinterval()\n'
                'with switch_interval(0.001):\n'
                '    inside = sys.getswitchinterval()\n'
                'after = sys.getswitchinterval()\n'
                'print(inside, after == before)\n'
                'try:\n'
                '    with switch_interval(0.02):\n'
                '        raise RuntimeError\n'
                'except RuntimeError:\n'
                '    print(sys.getswitchinterval() == before)\n'
            ),
            "expected": ['0.001 True', 'True'],
            "hint": (
                'old = sys.getswitchinterval(); sys.setswitchinterval(value); try: yield; finally: sys.setswitchinterval(old).'
            ),
        },
        {
            "id": "in-locked-account",
            "mode": "stdout",
            "title": "Замок против гонки",
            "statement": (
                'В Account метод deposit читает баланс, «задумывается» (time.sleep(0) отдаёт управление другому потоку) и записывает результат — из-за этого параллельные вклады теряются. Исправьте класс замком threading.Lock, чтобы 4 потока по 100 вкладов дали ровно 400.'
            ),
            "starter": (
                'import threading\n'
                'import time\n'
                '\n'
                '\n'
                'class Account:\n'
                '    def __init__(self):\n'
                '        self.balance = 0\n'
                '\n'
                '    def deposit(self, amount):\n'
                '        current = self.balance\n'
                '        time.sleep(0)\n'
                '        self.balance = current + amount\n'
            ),
            "driver": (
                'acc = Account()\n'
                '\n'
                '\n'
                'def work():\n'
                '    for _ in range(100):\n'
                '        acc.deposit(1)\n'
                '\n'
                '\n'
                'threads = [threading.Thread(target=work) for _ in range(4)]\n'
                'for t in threads:\n'
                '    t.start()\n'
                'for t in threads:\n'
                '    t.join()\n'
                'print(acc.balance)\n'
            ),
            "expected": ['400'],
            "hint": "self._lock = threading.Lock() в __init__; в deposit: with self._lock: ...",
        },
        {
            "id": "in-parallel-map",
            "mode": "stdout",
            "title": "Параллельный map на потоках",
            "statement": (
                'Напишите parallel_map(func, items, workers=4): примените func к элементам в пуле потоков (ThreadPoolExecutor) и верните список результатов в порядке входа. Исключение из func должно пробрасываться вызывающему.'
            ),
            "starter": (
                'from concurrent.futures import ThreadPoolExecutor\n'
                '\n'
                '\n'
                'def parallel_map(func, items, workers=4):\n'
                '    pass\n'
            ),
            "driver": (
                'import time\n'
                '\n'
                '\n'
                'def slow(x):\n'
                '    time.sleep(0.01 * (5 - x))\n'
                '    return x * x\n'
                '\n'
                '\n'
                'print(parallel_map(slow, range(5)))\n'
                'print(parallel_map(str, []))\n'
                '\n'
                '\n'
                'def bad(x):\n'
                '    if x == 2:\n'
                '        raise ValueError("два")\n'
                '    return x\n'
                '\n'
                '\n'
                'try:\n'
                '    parallel_map(bad, range(4))\n'
                'except ValueError as e:\n'
                '    print("ValueError", e)\n'
            ),
            "expected": ['[0, 1, 4, 9, 16]', '[]', 'ValueError два'],
            "hint": "with ThreadPoolExecutor(workers) as pool: return list(pool.map(func, items)).",
        },
        {
            "id": "in-queue-pipeline",
            "mode": "stdout",
            "title": "Производитель и потребитель",
            "statement": (
                'Напишите consume_sum(items): поток-производитель кладёт числа в queue.Queue, а в конце — признак окончания None; поток-потребитель суммирует числа до None. Верните сумму. Общие данные передаются только через очередь.'
            ),
            "starter": (
                'import queue\n'
                'import threading\n'
                '\n'
                '\n'
                'def consume_sum(items):\n'
                '    pass\n'
            ),
            "driver": (
                'print(consume_sum(range(1, 101)))\n'
                'print(consume_sum([]))\n'
                'print(consume_sum([5]))\n'
            ),
            "expected": ['5050', '0', '5'],
            "hint": (
                'q = queue.Queue(); производитель: for x in items: q.put(x); q.put(None); потребитель: while (x := q.get()) is not None: total += x.'
            ),
        },
        {
            "id": "in-global-names",
            "mode": "stdout",
            "title": "Какие глобальные имена читает функция",
            "statement": (
                'Напишите global_names(func): отсортированный список имён, которые функция читает как глобальные (команды LOAD_GLOBAL из dis.get_instructions); параметры и локальные имена не считаются.'
            ),
            "starter": (
                'import dis\n'
                '\n'
                '\n'
                'def global_names(func):\n'
                '    pass\n'
            ),
            "driver": (
                'def helper(x):\n'
                '    return x\n'
                '\n'
                '\n'
                'def f(x, y):\n'
                '    z = len(x) + helper(y)\n'
                '    return z\n'
                '\n'
                '\n'
                'def g(a):\n'
                '    b = a + 1\n'
                '    return b\n'
                '\n'
                '\n'
                'print(global_names(f))\n'
                'print(global_names(g))\n'
            ),
            "expected": ["['helper', 'len']", '[]'],
            "hint": '{i.argval for i in dis.get_instructions(func) if i.opname == "LOAD_GLOBAL"}.',
        },
        {
            "id": "in-runtime-info",
            "mode": "stdout",
            "title": "Паспорт интерпретатора",
            "statement": (
                'Напишите runtime_info(): словарь с ключами gil_enabled (sys._is_gil_enabled(), а если функции нет — True), free_threaded_build (bool от sysconfig.get_config_var("Py_GIL_DISABLED")) и switch_interval (sys.getswitchinterval()).'
            ),
            "starter": (
                'import sys\n'
                'import sysconfig\n'
                '\n'
                '\n'
                'def runtime_info():\n'
                '    pass\n'
            ),
            "driver": (
                'info = runtime_info()\n'
                'print(sorted(info))\n'
                'print(info["gil_enabled"], info["free_threaded_build"], info["switch_interval"])\n'
            ),
            "expected": ["['free_threaded_build', 'gil_enabled', 'switch_interval']", 'True False 0.005'],
            "hint": (
                'check = getattr(sys, "_is_gil_enabled", lambda: True); bool(sysconfig.get_config_var("Py_GIL_DISABLED")).'
            ),
        },
        {
            "id": "in-compile-run",
            "mode": "stdout",
            "title": "Скомпилировать один раз, выполнить много",
            "statement": (
                'Напишите compile_expr(source): скомпилируйте выражение один раз (compile с режимом eval, имя файла «<expr>») и верните функцию evaluate(**names), которая вычисляет его при заданных значениях переменных, не разбирая текст заново.'
            ),
            "starter": (
                'def compile_expr(source):\n'
                '    pass\n'
            ),
            "driver": (
                'ev = compile_expr("x * 2 + y")\n'
                'print(ev(x=1, y=1), ev(x=5, y=0), ev(x=10, y=-3))\n'
                'try:\n'
                '    ev(x=1)\n'
                'except NameError:\n'
                '    print("NameError")\n'
                'try:\n'
                '    compile_expr("1 +")\n'
                'except SyntaxError:\n'
                '    print("SyntaxError")\n'
            ),
            "expected": ['3 10 17', 'NameError', 'SyntaxError'],
            "hint": (
                'code = compile(source, "<expr>", "eval"); def evaluate(**names): return eval(code, {"__builtins__": {}}, names).'
            ),
        },
        {
            "id": "in-thread-local",
            "mode": "stdout",
            "title": "Свои данные у каждого потока",
            "statement": (
                'Функция worker_values(n) запускает n потоков: каждый записывает в общий объект state своё число (индекс), ждёт и читает его обратно. Сейчас state общий, поэтому потоки перетирают друг друга. Замените state на threading.local(), чтобы у каждого потока были свои данные и результат совпал с индексами.'
            ),
            "starter": (
                'import threading\n'
                'import time\n'
                '\n'
                'state = type("Shared", (), {})()\n'
                '\n'
                '\n'
                'def worker_values(n):\n'
                '    results = [None] * n\n'
                '\n'
                '    def work(i):\n'
                '        state.value = i\n'
                '        time.sleep(0.02)\n'
                '        results[i] = state.value\n'
                '\n'
                '    threads = [threading.Thread(target=work, args=(i,)) for i in range(n)]\n'
                '    for t in threads:\n'
                '        t.start()\n'
                '    for t in threads:\n'
                '        t.join()\n'
                '    return results\n'
            ),
            "driver": (
                'print(worker_values(5))\n'
                'print(worker_values(1))\n'
                'print(isinstance(state, threading.local))\n'
            ),
            "expected": ['[0, 1, 2, 3, 4]', '[0]', 'True'],
            "hint": "state = threading.local() — атрибуты такого объекта у каждого потока свои.",
        },
    ],
    49: [
        {
            "id": "pf-dedupe",
            "mode": "stdout",
            "title": "Дубликаты за линейное время",
            "statement": (
                'Функция dedupe(items) убирает повторы, сохраняя порядок первых вхождений. Сейчас она работает квадратично и не укладывается во время на больших данных. Ускорьте её (используйте множество уже увиденных элементов).'
            ),
            "starter": (
                'def dedupe(items):\n'
                '    out = []\n'
                '    for x in items:\n'
                '        if x not in out:\n'
                '            out.append(x)\n'
                '    return out\n'
            ),
            "driver": (
                'data = list(range(150000)) + list(range(50000))\n'
                'result = dedupe(data)\n'
                'print(len(result), result[:3], result[-1])\n'
                'print(dedupe([3, 1, 3, 2, 1]))\n'
            ),
            "expected": ['150000 [0, 1, 2] 149999', '[3, 1, 2]'],
            "hint": "seen = set(); для каждого x: если x не в seen — добавить в seen и в результат.",
        },
        {
            "id": "pf-top-words",
            "mode": "stdout",
            "title": "Самые частые слова",
            "statement": (
                'top_words(words, k) возвращает k самых частых слов в виде пар (слово, число) — по убыванию числа, при равенстве по алфавиту. Текущая версия для каждого слова считает words.count и не укладывается во время на большом входе. Ускорьте её (collections.Counter).'
            ),
            "starter": (
                'def top_words(words, k):\n'
                '    counts = [(w, words.count(w)) for w in set(words)]\n'
                '    counts.sort(key=lambda p: (-p[1], p[0]))\n'
                '    return counts[:k]\n'
            ),
            "driver": (
                'words = [f"w{i % 50000}" for i in range(200000)] + ["w7"] * 5 + ["w3"] * 3\n'
                'print(top_words(words, 3))\n'
                'print(top_words(["b", "a", "b", "a", "c"], 2))\n'
                'print(top_words([], 5))\n'
            ),
            "expected": ["[('w7', 9), ('w3', 7), ('w0', 4)]", "[('a', 2), ('b', 2)]", '[]'],
            "hint": "Counter(words).items(), затем sorted с ключом (-число, слово) и срез [:k].",
        },
        {
            "id": "pf-fib-cache",
            "mode": "stdout",
            "title": "Фибоначчи с кэшем",
            "statement": (
                'Рекурсивная fib(n) пересчитывает одно и то же и не укладывается во время даже для n = 90. Добавьте кэширование (functools.cache), не меняя логику.'
            ),
            "starter": (
                'def fib(n):\n'
                '    if n < 2:\n'
                '        return n\n'
                '    return fib(n - 1) + fib(n - 2)\n'
            ),
            "driver": (
                'print(fib(90))\n'
                'print(fib(10), fib(1), fib(0))\n'
            ),
            "expected": ['2880067194370816120', '55 1 0'],
            "hint": "from functools import cache и @cache над def fib.",
        },
        {
            "id": "pf-bisect-count",
            "mode": "stdout",
            "title": "Сколько чисел в диапазонах",
            "statement": (
                'count_in_ranges(nums, queries): nums — отсортированный список, queries — пары (lo, hi); для каждой верните, сколько чисел nums лежит в [lo, hi]. Текущая версия сканирует список для каждого запроса и слишком медленна. Используйте модуль bisect.'
            ),
            "starter": (
                'def count_in_ranges(nums, queries):\n'
                '    return [sum(1 for x in nums if lo <= x <= hi) for lo, hi in queries]\n'
            ),
            "driver": (
                'nums = sorted((i * 7919) % 200003 for i in range(200000))\n'
                'queries = [((i * 37) % 100000, (i * 37) % 100000 + 50000) for i in range(5000)]\n'
                'res = count_in_ranges(nums, queries)\n'
                'print(len(res), sum(res))\n'
                'print(res[:3] == [sum(1 for x in nums if lo <= x <= hi) for lo, hi in queries[:3]])\n'
                'print(count_in_ranges([1, 2, 2, 3], [(2, 2), (0, 10), (5, 6)]))\n'
            ),
            "expected": ['5000 250005000', 'True', '[2, 4, 0]'],
            "hint": "bisect_right(nums, hi) - bisect_left(nums, lo).",
        },
        {
            "id": "pf-window-max",
            "mode": "stdout",
            "title": "Максимум в скользящем окне",
            "statement": (
                'window_max(nums, k) возвращает максимумы всех окон длины k. Текущая версия берёт max от среза для каждого окна и слишком медленна при большом k. Ускорьте (монотонная очередь collections.deque с индексами).'
            ),
            "starter": (
                'def window_max(nums, k):\n'
                '    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]\n'
            ),
            "driver": (
                'nums = [(i * 31337) % 1000003 for i in range(200000)]\n'
                'res = window_max(nums, 20000)\n'
                'print(len(res), res[0], res[-1])\n'
                'print(res[:3] == [max(nums[i:i + 20000]) for i in range(3)])\n'
                'print(window_max([1, 3, -1, -3, 5, 3, 6, 7], 3))\n'
            ),
            "expected": ['180001 999937 1000002', 'True', '[3, 3, 5, 5, 6, 7]'],
            "hint": (
                'deque хранит индексы по убыванию значений: убирайте с конца меньшие новому, с начала — выпавшие из окна.'
            ),
        },
        {
            "id": "pf-range-sum",
            "mode": "stdout",
            "title": "Суммы на отрезках",
            "statement": (
                'Класс RangeSum(data) отвечает на запросы query(l, r) — сумма data[l:r]. Сейчас каждый запрос считает сумму заново и слишком медленен при множестве запросов. Подготовьте префиксные суммы в __init__, чтобы запрос выполнялся за константу.'
            ),
            "starter": (
                'class RangeSum:\n'
                '    def __init__(self, data):\n'
                '        self.data = list(data)\n'
                '\n'
                '    def query(self, l, r):\n'
                '        return sum(self.data[l:r])\n'
            ),
            "driver": (
                'rs = RangeSum(range(200000))\n'
                'total = sum(rs.query(i % 1000, 100000 + i % 1000) for i in range(200000))\n'
                'print(total)\n'
                'print(rs.query(0, 5), rs.query(10, 10), rs.query(3, 4))\n'
            ),
            "expected": ['1009980000000000', '10 0 3'],
            "hint": (
                'prefix[i] = сумма первых i элементов; ответ prefix[r] - prefix[l]; itertools.accumulate с начальным 0.'
            ),
        },
        {
            "id": "pf-call-counts",
            "mode": "stdout",
            "title": "Число вызовов через cProfile",
            "statement": (
                'Напишите call_counts(func): запустите func() под cProfile и верните словарь «имя функции → число вызовов» только для функций, определённых в том же файле, что и func (сравнивайте func.__code__.co_filename с именем файла в статистике).'
            ),
            "starter": (
                'import cProfile\n'
                'import pstats\n'
                '\n'
                '\n'
                'def call_counts(func):\n'
                '    pass\n'
            ),
            "driver": (
                'def helper(x):\n'
                '    return x + 1\n'
                '\n'
                '\n'
                'def other():\n'
                '    pass\n'
                '\n'
                '\n'
                'def work():\n'
                '    for i in range(5):\n'
                '        helper(i)\n'
                '    other()\n'
                '    other()\n'
                '\n'
                '\n'
                'print(sorted(call_counts(work).items()))\n'
            ),
            "expected": ["[('helper', 5), ('other', 2), ('work', 1)]"],
            "hint": (
                'pr = cProfile.Profile(); pr.runcall(func); stats = pstats.Stats(pr).stats; ключи — (файл, строка, имя), значения — (cc, nc, tt, ct, callers).'
            ),
        },
        {
            "id": "pf-bench",
            "mode": "stdout",
            "title": "Свой замер времени",
            "statement": (
                'Напишите bench(func, repeat=5, number=20): с помощью timeit.repeat запустите func по number раз в каждой из repeat серий и верните минимальное время одного вызова (в секундах, число с плавающей точкой).'
            ),
            "starter": (
                'import timeit\n'
                '\n'
                '\n'
                'def bench(func, repeat=5, number=20):\n'
                '    pass\n'
            ),
            "driver": (
                'fast = bench(lambda: sum(range(10)))\n'
                'slow = bench(lambda: sum(range(100000)))\n'
                'print(isinstance(fast, float), fast > 0, slow > fast * 20)\n'
                'calls = []\n'
                'bench(lambda: calls.append(1), repeat=3, number=4)\n'
                'print(len(calls))\n'
            ),
            "expected": ['True True True', '12'],
            "hint": "min(timeit.repeat(func, repeat=repeat, number=number)) / number.",
        },
        {
            "id": "pf-two-sum",
            "mode": "stdout",
            "title": "Два числа с заданной суммой",
            "statement": (
                'two_sum(nums, target): индексы (i, j), i < j, двух чисел с суммой target, или None, если такой пары нет. Двойной цикл на больших данных не укладывается во время: используйте словарь «значение → индекс» и один проход.'
            ),
            "starter": (
                'def two_sum(nums, target):\n'
                '    for i in range(len(nums)):\n'
                '        for j in range(i + 1, len(nums)):\n'
                '            if nums[i] + nums[j] == target:\n'
                '                return (i, j)\n'
                '    return None\n'
            ),
            "driver": (
                'nums = list(range(0, 200000, 2))\n'
                'print(two_sum(nums, nums[-1] + nums[-2]))\n'
                'print(two_sum(nums, 1))\n'
                'print(two_sum([3, 2, 4], 6), two_sum([1], 2))\n'
            ),
            "expected": ['(99998, 99999)', 'None', '(1, 2) None'],
            "hint": (
                'seen = {}; для каждого i: need = target - nums[i]; если need в seen — вернуть (seen[need], i); иначе seen[nums[i]] = i.'
            ),
        },
    ],
}
