"""Задачи книги «Архитектура компьютера»: главы 6–8."""

TASKS: dict[int, list[dict]] = {
    6: [
        {
            "id": "split-address",
            "mode": "func",
            "func": "split_address",
            "title": "Разбор адреса для кэша",
            "statement": (
                "Напишите функцию split_address(addr, offset_bits, "
                "index_bits): верните кортеж (tag, index, offset). "
                "Смещение — младшие offset_bits бит, индекс — следующие "
                "index_bits бит, тег — всё остальное. Число бит индекса "
                "может быть нулевым."
            ),
            "starter": "def split_address(addr, offset_bits, index_bits):\n    pass\n",
            "tests": [
                {"args": [0x12345, 6, 4], "expected": (72, 13, 5)},
                {"args": [0, 6, 4], "expected": (0, 0, 0)},
                {"args": [0xFFFF, 4, 4], "expected": (255, 15, 15)},
                {"args": [1000, 5, 3], "expected": (3, 7, 8)},
                {"args": [64, 6, 0], "expected": (1, 0, 0)},
            ],
            "hint": "offset = addr & ((1 << offset_bits) - 1); index = (addr >> offset_bits) & ((1 << index_bits) - 1); tag = addr >> (offset_bits + index_bits).",
        },
        {
            "id": "direct-mapped-cache",
            "mode": "func",
            "func": "direct_cache",
            "title": "Кэш с прямым отображением",
            "statement": (
                "Напишите функцию direct_cache(trace, lines, line_size): "
                "trace — список адресов, кэш на lines строк по line_size "
                "байт, изначально пустой. Блок = адрес // line_size; "
                "строка = блок % lines; тег = блок // lines. Верните "
                "кортеж (попадания, промахи). При промахе блок загружается "
                "в строку."
            ),
            "starter": "def direct_cache(trace, lines, line_size):\n    pass\n",
            "tests": [
                {"args": [[0, 4, 8, 16, 0, 64, 0], 4, 16], "expected": (3, 4)},
                {"args": [[], 4, 16], "expected": (0, 0)},
                {"args": [[0, 0, 0], 4, 16], "expected": (2, 1)},
                {"args": [[0, 64, 0, 64], 4, 16], "expected": (0, 4)},
                {"args": [list(range(0, 256, 4)), 4, 16], "expected": (48, 16)},
                {"args": [[0, 16, 32, 48, 0, 16, 32, 48], 4, 16], "expected": (4, 4)},
                {"args": [[0, 16, 32, 48, 64, 0], 4, 16], "expected": (0, 6)},
            ],
            "hint": "tags = [None] * lines; для адреса сравните tags[index] с tag: совпало — попадание, нет — промах и запись нового тега.",
        },
        {
            "id": "set-associative-lru",
            "mode": "func",
            "func": "set_assoc",
            "title": "Наборно-ассоциативный кэш с LRU",
            "statement": (
                "Напишите функцию set_assoc(trace, sets, ways, line_size): "
                "кэш из sets наборов по ways строк, политика LRU "
                "внутри набора. Блок = адрес // line_size, набор = блок % "
                "sets. Верните число попаданий. Для ways = 1 это кэш с "
                "прямым отображением, для sets = 1 — полностью ассоциативный."
            ),
            "starter": "def set_assoc(trace, sets, ways, line_size):\n    pass\n",
            "tests": [
                {"args": [[0, 64, 0, 64, 0, 64], 4, 1, 16], "expected": 0},
                {"args": [[0, 64, 0, 64, 0, 64], 2, 2, 16], "expected": 4},
                {"args": [[0, 64, 0, 64, 0, 64], 1, 4, 16], "expected": 4},
                {"args": [[0, 16, 32, 0, 48, 0, 16, 64, 0], 1, 3, 16], "expected": 3},
                {"args": [[], 2, 2, 16], "expected": 0},
                {"args": [[0, 32, 64, 0, 32, 64], 1, 2, 16], "expected": 0},
                {"args": [[0, 32, 64, 0, 32, 64], 1, 3, 16], "expected": 3},
            ],
            "hint": "На каждый набор — упорядоченный словарь (collections.OrderedDict) или список: попадание переносит блок в конец, при нехватке места удаляется первый.",
        },
        {
            "id": "replacement-policies",
            "mode": "func",
            "func": "cache_hits",
            "title": "LRU, FIFO и идеальная политика",
            "statement": (
                "Напишите функцию cache_hits(trace, capacity, policy): "
                "полностью ассоциативный кэш на capacity блоков, trace — "
                "список номеров блоков. policy: 'LRU' — вытеснять давно "
                "не использованный; 'FIFO' — вытеснять загруженный раньше "
                "всех (попадание порядок не меняет); 'OPT' — вытеснять тот, "
                "чьё следующее использование самое далёкое (или никогда). "
                "Верните число попаданий. Обратите внимание на «аномалию "
                "Биледи» у FIFO."
            ),
            "starter": "def cache_hits(trace, capacity, policy):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3, 1, 4, 1, 5, 1, 6, 1], 3, "LRU"], "expected": 4},
                {"args": [[1, 2, 3, 1, 4, 1, 5, 1, 6, 1], 3, "FIFO"], "expected": 3},
                {"args": [[1, 2, 3, 1, 4, 1, 5, 1, 6, 1], 3, "OPT"], "expected": 4},
                {"args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3, "FIFO"], "expected": 3},
                {"args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 4, "FIFO"], "expected": 2},
                {"args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3, "LRU"], "expected": 2},
                {"args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3, "OPT"], "expected": 5},
                {"args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 4, "OPT"], "expected": 6},
                {"args": [[], 2, "LRU"], "expected": 0},
                {"args": [[1, 1, 1], 1, "OPT"], "expected": 2},
            ],
            "hint": "OPT: для каждого блока в кэше найдите trace.index(x, i + 1) — позицию следующего использования (нет — бесконечность) и вытесните максимальный.",
        },
        {
            "id": "amat-levels",
            "mode": "func",
            "func": "amat",
            "title": "Среднее время доступа",
            "statement": (
                "Напишите функцию amat(levels, memory_time): levels — "
                "список пар [время_попадания, доля_промахов] от L1 вглубь, "
                "memory_time — время доступа к основной памяти. Верните "
                "среднее время доступа, округлённое до двух знаков. "
                "Для пустого списка уровней — memory_time."
            ),
            "starter": "def amat(levels, memory_time):\n    pass\n",
            "tests": [
                {"args": [[[1, 0.05], [10, 0.2]], 200], "expected": 3.5},
                {"args": [[], 100], "expected": 100},
                {"args": [[[4, 0.1]], 100], "expected": 14.0},
                {"args": [[[1, 0.1], [10, 0.2], [40, 0.5]], 300], "expected": 5.8},
                {"args": [[[2, 0.0]], 500], "expected": 2.0},
            ],
            "hint": "Идите от последнего уровня к первому: t = memory_time; для (hit, miss) в обратном порядке: t = hit + miss * t.",
        },
        {
            "id": "write-policy-count",
            "mode": "func",
            "func": "memory_writes",
            "title": "Сколько записей дойдёт до памяти",
            "statement": (
                "Напишите функцию memory_writes(trace, lines, line_size, "
                "policy): кэш с прямым отображением (как в задаче про "
                "direct_cache), размещение при записи (промах на запись "
                "загружает строку). trace — список пар ['R' или 'W', "
                "адрес]. policy 'WT' (сквозная запись): каждая запись "
                "('W') отправляет одну запись в память. policy 'WB' "
                "(отложенная): память пишется один раз при вытеснении "
                "«грязной» строки, а в конце работы все оставшиеся "
                "грязные строки сбрасываются. Верните число записей в память."
            ),
            "starter": "def memory_writes(trace, lines, line_size, policy):\n    pass\n",
            "tests": [
                {"args": [[["W", 0], ["W", 0], ["W", 4], ["R", 64], ["W", 64], ["W", 128], ["R", 0], ["W", 16]], 4, 16, "WT"], "expected": 6},
                {"args": [[["W", 0], ["W", 0], ["W", 4], ["R", 64], ["W", 64], ["W", 128], ["R", 0], ["W", 16]], 4, 16, "WB"], "expected": 4},
                {"args": [[], 4, 16, "WB"], "expected": 0},
                {"args": [[["R", 0], ["R", 16]], 4, 16, "WB"], "expected": 0},
                {"args": [[["W", 0], ["W", 64], ["W", 0], ["W", 64]], 4, 16, "WB"], "expected": 4},
                {"args": [[["W", 0], ["W", 64], ["W", 0], ["W", 64]], 4, 16, "WT"], "expected": 4},
            ],
            "hint": "Заведите массивы tags и dirty. При вытеснении (смена тега) в режиме WB грязная строка даёт одну запись; в конце прибавьте число грязных.",
        },
        {
            "id": "lru-cache-class",
            "mode": "stdout",
            "title": "Свой LRU-кэш",
            "statement": (
                "Напишите класс LRUCache(capacity) с методами get(key) "
                "(значение или -1; обращение делает ключ «свежим») и "
                "put(key, value) (запись; при переполнении удаляется "
                "самый давно использованный ключ). Обе операции должны "
                "работать за O(1): проверка подаёт 300 000 операций."
            ),
            "starter": "class LRUCache:\n    def __init__(self, capacity):\n        pass\n\n    def get(self, key):\n        pass\n\n    def put(self, key, value):\n        pass\n",
            "driver": (
                "c = LRUCache(2)\nc.put(1, 1)\nc.put(2, 2)\nprint(c.get(1))\nc.put(3, 3)\nprint(c.get(2), c.get(3))\nc.put(4, 4)\nprint(c.get(1), c.get(3), c.get(4))\n"
                "c = LRUCache(1)\nc.put(1, 10)\nc.put(1, 11)\nprint(c.get(1))\nc.put(2, 20)\nprint(c.get(1), c.get(2))\n"
                "import random\nrandom.seed(3)\nc = LRUCache(1000)\nhits = 0\n"
                "for _ in range(300000):\n    k = random.randint(0, 1500)\n    if c.get(k) != -1:\n        hits += 1\n    else:\n        c.put(k, k)\nprint(hits)\n"
            ),
            "expected": ["1", "-1 3", "-1 3 4", "11", "-1 20", "199025"],
            "hint": "collections.OrderedDict: move_to_end(key) при обращении, popitem(last=False) при переполнении.",
        },
        {
            "id": "traversal-misses",
            "mode": "func",
            "func": "traversal_misses",
            "title": "Промахи при обходе матрицы",
            "statement": (
                "Матрица n×n лежит в памяти по строкам: элемент (i, j) "
                "по адресу (i·n + j)·elem. Напишите функцию "
                "traversal_misses(n, order, lines, line_size, elem): "
                "обход построчно ('row': внешний цикл по i) или "
                "постолбцово ('col': внешний по j); кэш с прямым "
                "отображением на lines строк по line_size байт, "
                "изначально пустой. Верните число промахов."
            ),
            "starter": "def traversal_misses(n, order, lines, line_size, elem):\n    pass\n",
            "tests": [
                {"args": [64, "row", 64, 64, 4], "expected": 256},
                {"args": [64, "col", 64, 64, 4], "expected": 4096},
                {"args": [32, "row", 16, 64, 4], "expected": 64},
                {"args": [32, "col", 16, 64, 4], "expected": 1024},
                {"args": [16, "col", 256, 64, 4], "expected": 16},
                {"args": [8, "row", 4, 16, 4], "expected": 16},
                {"args": [8, "col", 4, 16, 4], "expected": 64},
            ],
            "hint": "Перебирайте пары (a, b); (i, j) = (a, b) для 'row' и (b, a) для 'col'; дальше — обычный кэш с прямым отображением.",
        },
        {
            "id": "working-set",
            "mode": "stdout",
            "title": "Рабочее множество",
            "statement": (
                "Напишите функцию max_working_set(trace, window): trace — "
                "список номеров блоков, window — размер скользящего окна "
                "подряд идущих обращений. Верните наибольшее число "
                "различных блоков в одном окне (если trace короче окна — "
                "по всему списку). Решение за O(n): проверка подаёт "
                "300 000 обращений и окно 1000."
            ),
            "starter": "def max_working_set(trace, window):\n    pass\n",
            "driver": (
                "print(max_working_set([1, 2, 1, 3, 4], 3), max_working_set([5, 5, 5], 2), max_working_set([], 3), max_working_set([1, 2, 3], 10))\n"
                "import random\nrandom.seed(2)\ntrace = [random.randint(0, 5000) for _ in range(300000)]\nprint(max_working_set(trace, 1000), max_working_set(trace, 50))\n"
            ),
            "expected": ["3 1 0 3", "936 50"],
            "hint": "Счётчик Counter внутри окна: добавляйте новый блок, удаляйте вышедший (когда счётчик стал нулём — удаляйте ключ); размер словаря — число различных блоков.",
        },
    ],
    7: [
        {
            "id": "pipeline-cycles",
            "mode": "func",
            "func": "pipeline_cycles",
            "title": "Такты конвейера",
            "statement": (
                "Напишите функцию pipeline_cycles(n, stages, stalls): n "
                "команд проходят конвейер из stages стадий, а stalls — "
                "число пузырей (пустых тактов). Верните кортеж "
                "(с_конвейером, без_конвейера, ускорение): с конвейером — "
                "stages + n − 1 + stalls; без — stages · n; ускорение — "
                "отношение, округлённое до двух знаков. Для n = 0 — "
                "(0, 0, 0.0)."
            ),
            "starter": "def pipeline_cycles(n, stages, stalls):\n    pass\n",
            "tests": [
                {"args": [1, 5, 0], "expected": (5, 5, 1.0)},
                {"args": [5, 5, 0], "expected": (9, 25, 2.78)},
                {"args": [100, 5, 0], "expected": (104, 500, 4.81)},
                {"args": [10, 5, 3], "expected": (17, 50, 2.94)},
                {"args": [0, 5, 0], "expected": (0, 0, 0.0)},
                {"args": [8, 4, 2], "expected": (13, 32, 2.46)},
            ],
            "hint": "Не забудьте частный случай n = 0 — деления на ноль быть не должно.",
        },
        {
            "id": "pipeline-diagram",
            "mode": "func",
            "func": "pipeline_diagram",
            "title": "Диаграмма конвейера",
            "statement": (
                "Напишите функцию pipeline_diagram(n, stages): stages — "
                "список названий стадий. Верните список из n строк (по "
                "одной на команду): общее число тактов stages + n − 1; "
                "в каждой строке названия стадий в нужных тактах, "
                "остальные клетки — '.', всё соединено одним пробелом. "
                "Команда i стартует в такте i."
            ),
            "starter": "def pipeline_diagram(n, stages):\n    pass\n",
            "tests": [
                {"args": [2, ["IF", "ID", "EX"]], "expected": ["IF ID EX .", ". IF ID EX"]},
                {"args": [1, ["IF", "ID"]], "expected": ["IF ID"]},
                {"args": [3, ["F", "D"]], "expected": ["F D . .", ". F D .", ". . F D"]},
                {"args": [0, ["IF", "ID"]], "expected": []},
            ],
            "hint": "total = len(stages) + n - 1; строка i: cells = ['.'] * total; cells[i + k] = stages[k].",
        },
        {
            "id": "find-raw",
            "mode": "func",
            "func": "find_raw",
            "title": "Зависимости «чтение после записи»",
            "statement": (
                "Напишите функцию find_raw(prog): prog — список команд "
                "[операция, приёмник, источники…] (приёмник может быть "
                "None — команда ничего не пишет в регистр). Верните "
                "отсортированный список пар [i, j]: команда j читает "
                "регистр, последний раз записанный командой i (ближайшей "
                "предыдущей, пишущей в этот регистр). Одинаковые пары "
                "не повторяются."
            ),
            "starter": "def find_raw(prog):\n    pass\n",
            "tests": [
                {"args": [[["ADD", "R1", "R2", "R3"], ["SUB", "R4", "R1", "R5"], ["AND", "R6", "R7", "R8"], ["OR", "R9", "R1", "R4"]]], "expected": [[0, 1], [0, 3], [1, 3]]},
                {"args": [[["LW", "R1", "R2"], ["ADD", "R1", "R1", "R1"], ["SW", None, "R1", "R2"], ["ADD", "R3", "R1", "R1"]]], "expected": [[0, 1], [1, 2], [1, 3]]},
                {"args": [[]], "expected": []},
                {"args": [[["ADD", "R1", "R2", "R3"], ["ADD", "R4", "R5", "R6"]]], "expected": []},
            ],
            "hint": "Для каждой команды j и каждого её источника идите назад, пока не найдёте команду с таким же приёмником: это ближайший производитель.",
        },
        {
            "id": "pipeline-stalls",
            "mode": "func",
            "func": "pipeline_stalls",
            "title": "Пузыри в конвейере",
            "statement": (
                "Напишите функцию pipeline_stalls(prog, forwarding): "
                "число пузырей в пятистадийном конвейере (IF ID EX MEM "
                "WB). Команды [операция, приёмник, источники…]. Команда "
                "входит в стадию ID в такте t: не раньше, чем "
                "предыдущая плюс 1, и не раньше, чем готовы её источники. "
                "Результат команды, вошедшей в ID в такте t, готов для "
                "чтения: без обходов — в t + 3; с обходами — в t + 1 "
                "для обычных команд и в t + 2 для 'LW'. Число пузырей = "
                "сумма задержек сверх «по одной команде за такт»."
            ),
            "starter": "def pipeline_stalls(prog, forwarding):\n    pass\n",
            "tests": [
                {"args": [[["ADD", "R1", "R2", "R3"], ["SUB", "R4", "R1", "R5"], ["AND", "R6", "R7", "R8"], ["OR", "R9", "R1", "R4"]], False], "expected": 3},
                {"args": [[["ADD", "R1", "R2", "R3"], ["SUB", "R4", "R1", "R5"], ["AND", "R6", "R7", "R8"], ["OR", "R9", "R1", "R4"]], True], "expected": 0},
                {"args": [[["LW", "R1", "R2"], ["ADD", "R1", "R1", "R1"], ["SW", None, "R1", "R2"], ["ADD", "R3", "R1", "R1"]], False], "expected": 4},
                {"args": [[["LW", "R1", "R2"], ["ADD", "R1", "R1", "R1"], ["SW", None, "R1", "R2"], ["ADD", "R3", "R1", "R1"]], True], "expected": 1},
                {"args": [[["LW", "R1", "R2"], ["ADD", "R3", "R1", "R4"], ["SUB", "R5", "R3", "R1"]], True], "expected": 1},
                {"args": [[["ADD", "R1", "R2", "R3"], ["SUB", "R4", "R1", "R5"], ["AND", "R6", "R4", "R1"]], False], "expected": 4},
                {"args": [[["ADD", "R1", "R2", "R3"], ["ADD", "R4", "R5", "R6"], ["ADD", "R7", "R1", "R4"]], False], "expected": 2},
                {"args": [[], True], "expected": 0},
            ],
            "hint": "Храните для каждого регистра такт, начиная с которого его можно читать (ready); t = max(t_prev + 1, ready всех источников).",
        },
        {
            "id": "compare-cpus",
            "mode": "func",
            "func": "compare_cpus",
            "title": "Какой процессор быстрее",
            "statement": (
                "Напишите функцию compare_cpus(a, b): a и b — тройки "
                "[число_команд, CPI, частота_ГГц] — одна и та же задача на "
                "двух процессорах (время = IC · CPI / f). Верните кортеж "
                "(кто_быстрее, ускорение): 'A' или 'B', ускорение — "
                "отношение времён, округлённое до двух знаков; при равных "
                "временах — ('equal', 1.0)."
            ),
            "starter": "def compare_cpus(a, b):\n    pass\n",
            "tests": [
                {"args": [[1000000000, 1.5, 3], [1000000000, 1.0, 2]], "expected": ("equal", 1.0)},
                {"args": [[1000000000, 2.0, 3], [1000000000, 1.0, 3]], "expected": ("B", 2.0)},
                {"args": [[500000000, 1.0, 2], [1000000000, 1.0, 2]], "expected": ("A", 2.0)},
                {"args": [[1000000000, 1.2, 4], [1000000000, 1.5, 4]], "expected": ("A", 1.25)},
            ],
            "hint": "Сравнивайте времена ta = IC · CPI / f; ускорение — большее время, делённое на меньшее.",
        },
        {
            "id": "effective-cpi",
            "mode": "func",
            "func": "effective_cpi",
            "title": "CPI с учётом переходов",
            "statement": (
                "Напишите функцию effective_cpi(base, branch_share, "
                "miss_rate, penalty): base — CPI без потерь, branch_share "
                "— доля переходов среди команд, miss_rate — доля "
                "неверных предсказаний среди переходов, penalty — штраф "
                "в тактах. Верните CPI, округлённый до трёх знаков."
            ),
            "starter": "def effective_cpi(base, branch_share, miss_rate, penalty):\n    pass\n",
            "tests": [
                {"args": [1, 0.2, 0.1, 3], "expected": 1.06},
                {"args": [1.2, 0.25, 0.05, 20], "expected": 1.45},
                {"args": [1, 0, 0.5, 10], "expected": 1.0},
                {"args": [1.5, 0.15, 0.08, 14], "expected": 1.668},
            ],
            "hint": "CPI = base + branch_share · miss_rate · penalty.",
        },
        {
            "id": "predictor-accuracy",
            "mode": "func",
            "func": "predictor_accuracy",
            "title": "Предсказатель переходов",
            "statement": (
                "Напишите функцию predictor_accuracy(history, bits): "
                "history — список исходов переходов (True — взят). bits = 1: "
                "однобитный предсказатель, прогноз = последний исход, "
                "в начале «не взят». bits = 2: двухбитный насыщающийся "
                "счётчик 0..3, начало 0, прогноз «взят» при значении ≥ 2; "
                "после исхода «взят» счётчик увеличивается (не выше 3), "
                "иначе уменьшается (не ниже 0). Верните число верных "
                "прогнозов."
            ),
            "starter": "def predictor_accuracy(history, bits):\n    pass\n",
            "tests": [
                {"args": [([True] * 9 + [False]) * 10, 1], "expected": 80},
                {"args": [([True] * 9 + [False]) * 10, 2], "expected": 88},
                {"args": [[True, False] * 5, 1], "expected": 0},
                {"args": [[True, False] * 5, 2], "expected": 5},
                {"args": [[], 2], "expected": 0},
                {"args": [[True] * 5, 1], "expected": 4},
                {"args": [[True] * 5, 2], "expected": 3},
                {"args": [[False] * 4, 2], "expected": 4},
            ],
            "hint": "Сначала прогноз и сравнение с исходом, потом обновление состояния.",
        },
        {
            "id": "required-fraction",
            "mode": "func",
            "func": "required_fraction",
            "title": "Какая доля должна ускоряться",
            "statement": (
                "По закону Амдала ускорение = 1 / ((1 − p) + p / s). "
                "Напишите функцию required_fraction(target, s): какая "
                "доля p программы должна ускоряться в s раз, чтобы общее "
                "ускорение равнялось target. Округлите до четырёх знаков. "
                "Если target <= 1 — 0.0; если цель недостижима (target > s) — None."
            ),
            "starter": "def required_fraction(target, s):\n    pass\n",
            "tests": [
                {"args": [5, 10], "expected": 0.8889},
                {"args": [2, 2], "expected": 1.0},
                {"args": [3, 2], "expected": None},
                {"args": [1, 10], "expected": 0.0},
                {"args": [1.5, 4], "expected": 0.4444},
                {"args": [0.5, 3], "expected": 0.0},
                {"args": [8, 16], "expected": 0.9333},
            ],
            "hint": "Из формулы: p = (1 − 1/target) / (1 − 1/s).",
        },
        {
            "id": "schedule-width",
            "mode": "func",
            "func": "schedule_cycles",
            "title": "Планировщик суперскалярного процессора",
            "statement": (
                "Напишите функцию schedule_cycles(deps, width): deps — "
                "словарь «номер команды → список номеров команд, от "
                "которых она зависит», у каждой команды задержка 1 такт; "
                "(в JSON ключи — строки, берите int(k)); width — сколько "
                "команд запускается за такт. Каждый такт запускаются "
                "готовые команды (все зависимости выполнены в "
                "предыдущих тактах), по возрастанию номера, не больше "
                "width штук. Верните число тактов."
            ),
            "starter": "def schedule_cycles(deps, width):\n    pass\n",
            "tests": [
                {"args": [{"0": [], "1": [], "2": [0, 1], "3": [2], "4": [], "5": [3, 4]}, 2], "expected": 4},
                {"args": [{str(i): [] for i in range(10)}, 4], "expected": 3},
                {"args": [{str(i): ([i - 1] if i else []) for i in range(100)}, 4], "expected": 100},
                {"args": [{"0": [], "1": [0], "2": [0], "3": [1, 2]}, 2], "expected": 3},
                {"args": [{"0": [], "1": [0], "2": [0], "3": [1, 2]}, 1], "expected": 4},
                {"args": [{}, 3], "expected": 0},
            ],
            "hint": "Пока не выполнены все: ready = [i для невыполненных, у которых все зависимости done]; отметьте первые width из них выполненными (по состоянию на начало такта).",
        },
    ],
    8: [
        {
            "id": "translate-address",
            "mode": "func",
            "func": "translate",
            "title": "Перевод виртуального адреса",
            "statement": (
                "Напишите функцию translate(table, vaddr, page_bits): "
                "table — список, где индекс — номер виртуальной страницы, "
                "значение — номер кадра или None (страницы нет); "
                "page_bits — число бит смещения. Верните физический адрес "
                "либо None при страничном прерывании (страницы нет или "
                "номер за пределами таблицы)."
            ),
            "starter": "def translate(table, vaddr, page_bits):\n    pass\n",
            "tests": [
                {"args": [[7, None, 3], 66, 12], "expected": 28738},
                {"args": [[7, None, 3], 4096, 12], "expected": None},
                {"args": [[7, None, 3], 10940, 12], "expected": 15036},
                {"args": [[7, None, 3], 36864, 12], "expected": None},
                {"args": [[7, None, 3], 4095, 12], "expected": 32767},
                {"args": [[], 0, 12], "expected": None},
                {"args": [[5, 6], 19, 4], "expected": 99},
                {"args": [[5, 6], 31, 4], "expected": 111},
            ],
            "hint": "vpn = vaddr >> page_bits; offset = vaddr & ((1 << page_bits) - 1); результат (frame << page_bits) | offset.",
        },
        {
            "id": "translate-protect",
            "mode": "func",
            "func": "access",
            "title": "Перевод с проверкой защиты",
            "statement": (
                "Страница 4 КиБ (12 бит смещения). Напишите функцию "
                "access(table, vaddr, write, user): table[vpn] — None или "
                "[кадр, можно_писать, доступна_пользователю] (0/1). write — "
                "обращение на запись, user — из пользовательского режима. "
                "Верните ('ok', физический_адрес), ('page fault',) если "
                "страницы нет (или номер за пределами таблицы), либо "
                "('protection fault',): запись в страницу без права записи "
                "или обращение пользователя к странице ядра."
            ),
            "starter": "def access(table, vaddr, write, user):\n    pass\n",
            "tests": [
                {"args": [[[7, 1, 1], None, [3, 0, 1], [9, 1, 0]], 66, False, True], "expected": ("ok", 28738)},
                {"args": [[[7, 1, 1], None, [3, 0, 1], [9, 1, 0]], 4096, False, True], "expected": ("page fault",)},
                {"args": [[[7, 1, 1], None, [3, 0, 1], [9, 1, 0]], 10940, False, True], "expected": ("ok", 15036)},
                {"args": [[[7, 1, 1], None, [3, 0, 1], [9, 1, 0]], 10940, True, True], "expected": ("protection fault",)},
                {"args": [[[7, 1, 1], None, [3, 0, 1], [9, 1, 0]], 12288, False, True], "expected": ("protection fault",)},
                {"args": [[[7, 1, 1], None, [3, 0, 1], [9, 1, 0]], 12288, False, False], "expected": ("ok", 36864)},
                {"args": [[[7, 1, 1], None, [3, 0, 1], [9, 1, 0]], 12292, True, False], "expected": ("ok", 36868)},
                {"args": [[[7, 1, 1], None, [3, 0, 1], [9, 1, 0]], 36864, False, False], "expected": ("page fault",)},
            ],
            "hint": "Сначала проверьте существование страницы, потом права: нарушение прав — если write и нет записи, либо user и страница не пользовательская.",
        },
        {
            "id": "pte-decode",
            "mode": "func",
            "func": "pte_decode",
            "title": "Запись таблицы страниц",
            "statement": (
                "Напишите функцию pte_decode(pte): в записи таблицы "
                "страниц биты: 0 — present, 1 — writable, 2 — user, 5 — "
                "accessed, 6 — dirty; номер кадра — биты 12 и выше. "
                "Верните кортеж (кадр, список_имён_установленных_флагов): "
                "имена в порядке present, writable, user, accessed, dirty."
            ),
            "starter": "def pte_decode(pte):\n    pass\n",
            "tests": [
                {"args": [0x5043], "expected": (5, ["present", "writable", "dirty"])},
                {"args": [0], "expected": (0, [])},
                {"args": [0xABCDE067], "expected": (703710, ["present", "writable", "user", "accessed", "dirty"])},
                {"args": [0x1005], "expected": (1, ["present", "user"])},
            ],
            "hint": "frame = pte >> 12; для каждой пары (маска, имя): если pte & маска — добавьте имя.",
        },
        {
            "id": "multilevel-translate",
            "mode": "func",
            "func": "translate_multi",
            "title": "Многоуровневая таблица страниц",
            "statement": (
                "Напишите функцию translate_multi(root, vaddr, level_bits, "
                "page_bits): root — вложенные списки (по числу уровней), "
                "в листьях — номера кадров, None — отсутствующая запись. "
                "level_bits — список ширин индексов уровней от старшего "
                "к младшему, page_bits — ширина смещения. Верните "
                "физический адрес либо None, если на любом уровне записи "
                "нет или адрес не помещается в сумму ширин."
            ),
            "starter": "def translate_multi(root, vaddr, level_bits, page_bits):\n    pass\n",
            "tests": [
                {"args": [[[10, 11, None, 13], None, [20, None, None, None], [None, None, None, 33]], 5, [2, 2], 4], "expected": 165},
                {"args": [[[10, 11, None, 13], None, [20, None, None, None], [None, None, None, 33]], 21, [2, 2], 4], "expected": 181},
                {"args": [[[10, 11, None, 13], None, [20, None, None, None], [None, None, None, 33]], 37, [2, 2], 4], "expected": None},
                {"args": [[[10, 11, None, 13], None, [20, None, None, None], [None, None, None, 33]], 53, [2, 2], 4], "expected": 213},
                {"args": [[[10, 11, None, 13], None, [20, None, None, None], [None, None, None, 33]], 64, [2, 2], 4], "expected": None},
                {"args": [[[10, 11, None, 13], None, [20, None, None, None], [None, None, None, 33]], 133, [2, 2], 4], "expected": 325},
                {"args": [[[10, 11, None, 13], None, [20, None, None, None], [None, None, None, 33]], 181, [2, 2], 4], "expected": None},
                {"args": [[[10, 11, None, 13], None, [20, None, None, None], [None, None, None, 33]], 245, [2, 2], 4], "expected": 533},
                {"args": [[[10, 11, None, 13], None, [20, None, None, None], [None, None, None, 33]], 256, [2, 2], 4], "expected": None},
                {"args": [[5, None, 7, 9], 29, [2], 3], "expected": 77},
                {"args": [[5, None, 7, 9], 45, [2], 3], "expected": None},
            ],
            "hint": "Отбросьте смещение, затем от старших битов к младшим берите индексы уровней: node = node[idx]; на любом шаге None — возвращайте None.",
        },
        {
            "id": "page-table-levels",
            "mode": "func",
            "func": "table_levels",
            "title": "Сколько уровней у таблицы страниц",
            "statement": (
                "Напишите функцию table_levels(va_bits, page_bits, "
                "pte_bytes): верните кортеж (размер_плоской_таблицы_в_байтах, "
                "число_уровней). Плоская таблица: 2^(va_bits − page_bits) "
                "записей по pte_bytes. Многоуровневая: каждая таблица "
                "занимает ровно одну страницу, то есть содержит "
                "2^page_bits / pte_bytes записей (степень двойки); "
                "уровней столько, чтобы индексы покрыли va_bits − page_bits."
            ),
            "starter": "def table_levels(va_bits, page_bits, pte_bytes):\n    pass\n",
            "tests": [
                {"args": [48, 12, 8], "expected": (549755813888, 4)},
                {"args": [32, 12, 4], "expected": (4194304, 2)},
                {"args": [39, 12, 8], "expected": (1073741824, 3)},
                {"args": [57, 12, 8], "expected": (281474976710656, 5)},
                {"args": [16, 8, 2], "expected": (512, 2)},
                {"args": [64, 12, 8], "expected": (36028797018963968, 6)},
            ],
            "hint": "Бит на уровень = log2(2**page_bits // pte_bytes); уровней = ceil((va_bits − page_bits) / бит_на_уровень).",
        },
        {
            "id": "tlb-lru",
            "mode": "stdout",
            "title": "TLB с вытеснением LRU",
            "statement": (
                "Напишите функцию tlb_hits(pages, size): TLB на size "
                "записей, политика LRU; pages — последовательность номеров "
                "страниц. Верните число попаданий. Проверка подаёт "
                "300 000 обращений: операции должны быть за O(1)."
            ),
            "starter": "def tlb_hits(pages, size):\n    pass\n",
            "driver": (
                "print(tlb_hits([1, 2, 3] * 100, 4), tlb_hits([1, 2, 3] * 100, 2), tlb_hits([], 4), tlb_hits([1, 1, 1], 1))\n"
                "import random\nrandom.seed(7)\nbig = [random.randint(0, 600) for _ in range(300000)]\nprint(tlb_hits(big, 64), tlb_hits(big, 512))\n"
            ),
            "expected": ["297 0 0 2", "32185 255082"],
            "hint": "OrderedDict: move_to_end при попадании, popitem(last=False) при переполнении; список с remove() на 300 000 обращений не уложится.",
        },
        {
            "id": "page-replacement",
            "mode": "func",
            "func": "page_faults",
            "title": "Алгоритмы замещения страниц",
            "statement": (
                "Напишите функцию page_faults(trace, frames, policy): "
                "число страничных прерываний для frames кадров. policy: "
                "'FIFO', 'LRU', 'OPT' (вытеснять страницу, которая "
                "понадобится позже всех или никогда) и 'CLOCK' (второй "
                "шанс): кадры по кругу, у каждого бит обращения; "
                "попадание ставит бит в 1; при промахе стрелка (в начале "
                "на кадре 0) идёт по кругу, пропуская кадры с битом 1 "
                "(сбрасывая его) и свободные места берёт сразу; на найденное "
                "место загружается страница с битом 1, стрелка уходит на "
                "следующий кадр."
            ),
            "starter": "def page_faults(trace, frames, policy):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3, "FIFO"], "expected": 9},
                {"args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 4, "FIFO"], "expected": 10},
                {"args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3, "LRU"], "expected": 10},
                {"args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 4, "LRU"], "expected": 8},
                {"args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3, "OPT"], "expected": 7},
                {"args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 4, "OPT"], "expected": 6},
                {"args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 3, "CLOCK"], "expected": 9},
                {"args": [[1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5], 4, "CLOCK"], "expected": 10},
                {"args": [[0, 1, 2, 3, 4] * 10, 4, "LRU"], "expected": 50},
                {"args": [[0, 1, 2, 3, 4] * 10, 4, "OPT"], "expected": 16},
                {"args": [[0, 1, 2, 3, 4] * 10, 5, "FIFO"], "expected": 5},
                {"args": [[1, 2, 1, 3, 1, 4, 1, 5], 2, "LRU"], "expected": 5},
                {"args": [[1, 2, 1, 3, 1, 4, 1, 5], 2, "FIFO"], "expected": 6},
                {"args": [[], 3, "CLOCK"], "expected": 0},
            ],
            "hint": "FIFO и LRU — список порядка вытеснения; OPT — вытесняйте страницу с наибольшим индексом следующего использования; CLOCK — массивы pages, ref и позиция hand.",
        },
        {
            "id": "effective-access-time",
            "mode": "func",
            "func": "effective_access_time",
            "title": "Среднее время обращения",
            "statement": (
                "Напишите функцию effective_access_time(tlb_hit, tlb_ns, "
                "mem_ns, levels, fault_rate, fault_ns): время = tlb_ns + "
                "(1 − tlb_hit) · levels · mem_ns (обход таблиц при промахе "
                "TLB) + mem_ns (само обращение к данным) + fault_rate · "
                "fault_ns (страничные прерывания). Результат округлите "
                "до двух знаков."
            ),
            "starter": "def effective_access_time(tlb_hit, tlb_ns, mem_ns, levels, fault_rate, fault_ns):\n    pass\n",
            "tests": [
                {"args": [0.99, 1, 100, 4, 0, 0], "expected": 105.0},
                {"args": [0.9, 2, 80, 4, 0.0001, 8000000], "expected": 914.0},
                {"args": [1.0, 1, 100, 4, 0, 0], "expected": 101.0},
                {"args": [0.0, 0, 100, 2, 0, 0], "expected": 300.0},
                {"args": [0.98, 1, 60, 3, 0.000001, 5000000], "expected": 69.6},
            ],
            "hint": "Просто подставьте числа в формулу; обратите внимание: при попадании в TLB обход не нужен.",
        },
        {
            "id": "cow-frames",
            "mode": "func",
            "func": "cow_frames",
            "title": "Копирование при записи",
            "statement": (
                "Напишите функцию cow_frames(pages, ops): процесс 'p0' "
                "владеет pages страницами в pages разных кадрах. ops — "
                "список операций: ['fork', родитель, потомок] — потомок "
                "получает копию таблицы страниц с общими кадрами; "
                "['write', процесс, номер_страницы] — запись: если кадр "
                "общий (им владеет больше одного процесса), процесс "
                "получает новый собственный кадр, иначе кадр меняется на "
                "месте; ['exit', процесс] — процесс завершается и "
                "освобождает свои ссылки. Верните число занятых физических "
                "кадров (на которые кто-то ссылается) в конце."
            ),
            "starter": "def cow_frames(pages, ops):\n    pass\n",
            "tests": [
                {"args": [3, []], "expected": 3},
                {"args": [3, [["fork", "p0", "p1"]]], "expected": 3},
                {"args": [3, [["fork", "p0", "p1"], ["write", "p1", 0]]], "expected": 4},
                {"args": [3, [["fork", "p0", "p1"], ["write", "p1", 0], ["write", "p1", 0], ["write", "p0", 0]]], "expected": 4},
                {"args": [2, [["fork", "p0", "p1"], ["fork", "p1", "p2"], ["write", "p2", 1], ["write", "p2", 1], ["exit", "p1"]]], "expected": 3},
                {"args": [4, [["fork", "p0", "p1"], ["exit", "p0"], ["write", "p1", 2]]], "expected": 4},
                {"args": [4, [["fork", "p0", "p1"], ["write", "p0", 0], ["write", "p0", 1], ["write", "p1", 0], ["exit", "p1"]]], "expected": 4},
            ],
            "hint": "Счётчик ссылок на кадр: fork увеличивает, write на общем кадре уменьшает старый и заводит новый, exit уменьшает все ссылки процесса.",
        },
    ],
}
