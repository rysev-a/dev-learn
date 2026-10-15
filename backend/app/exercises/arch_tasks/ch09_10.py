"""Задачи книги «Архитектура компьютера»: главы 9–10."""

TASKS: dict[int, list[dict]] = {
    9: [
        {
            "id": "bus-bandwidth",
            "mode": "func",
            "func": "bus_bandwidth",
            "title": "Пропускная способность шины",
            "statement": (
                "Напишите функцию bus_bandwidth(width_bits, mega_transfers): "
                "ширина шины в битах и число мегапередач в секунду. Верните "
                "пропускную способность в ГБ/с (1 ГБ = 1000 МБ), округлённую "
                "до трёх знаков."
            ),
            "starter": "def bus_bandwidth(width_bits, mega_transfers):\n    pass\n",
            "tests": [
                {"args": [64, 3200], "expected": 25.6},
                {"args": [32, 33], "expected": 0.132},
                {"args": [128, 2400], "expected": 38.4},
                {"args": [8, 1000], "expected": 1.0},
                {"args": [16, 0], "expected": 0.0},
            ],
            "hint": "байт за передачу = width_bits / 8; в секунду — умножить на mega_transfers МБ; ГБ — разделить на 1000.",
        },
        {
            "id": "memory-mapped-bus",
            "mode": "stdout",
            "title": "Шина с отображённым вводом-выводом",
            "statement": (
                "Напишите класс MemoryBus с методами map(start, end, "
                "device), read(addr) и write(addr, value). Устройство "
                "занимает адреса [start, end); обращение по адресу "
                "перенаправляется методам device.read(offset) и "
                "device.write(offset, value), где offset = addr − start. "
                "Если по адресу нет устройства, бросьте ValueError."
            ),
            "starter": "class MemoryBus:\n    def __init__(self):\n        pass\n\n    def map(self, start, end, device):\n        pass\n\n    def read(self, addr):\n        pass\n\n    def write(self, addr, value):\n        pass\n",
            "driver": (
                "class Ram:\n    def __init__(self):\n        self.d = {}\n    def read(self, off):\n        return self.d.get(off, 0)\n    def write(self, off, v):\n        self.d[off] = v\n"
                "class Console:\n    def __init__(self):\n        self.out = []\n    def read(self, off):\n        return len(self.out)\n    def write(self, off, v):\n        self.out.append(chr(v))\n"
                "ram, con = Ram(), Console()\nbus = MemoryBus()\nbus.map(0x0000, 0x1000, ram)\nbus.map(0x8000, 0x8010, con)\n"
                "bus.write(0x10, 7)\nbus.write(0x8000, ord('H'))\nbus.write(0x8005, ord('i'))\n"
                "print(bus.read(0x10), bus.read(0x8000), ''.join(con.out), ram.d)\n"
                "for addr in (0x4000, 0x1000, 0x8010):\n    try:\n        bus.read(addr)\n    except ValueError:\n        print('нет устройства')\n"
            ),
            "expected": ["7 2 Hi {16: 7}", "нет устройства", "нет устройства", "нет устройства"],
            "hint": "Храните список (start, end, device); для адреса найдите запись, где start <= addr < end.",
        },
        {
            "id": "interrupt-order",
            "mode": "func",
            "func": "handle_interrupts",
            "title": "Контроллер прерываний",
            "statement": (
                "Напишите функцию handle_interrupts(batches, masked): "
                "batches — список «пачек»: в каждой номера линий "
                "прерываний, пришедших одновременно (одна и та же линия "
                "в пачке считается один раз); masked — список "
                "замаскированных линий. Внутри пачки прерывания "
                "обрабатываются по возрастанию номера (меньше номер — "
                "выше приоритет), замаскированные пропускаются. "
                "Верните список обработанных линий в порядке обработки."
            ),
            "starter": "def handle_interrupts(batches, masked):\n    pass\n",
            "tests": [
                {"args": [[[3, 1], [2, 2, 0], [], [5, 4]], []], "expected": [1, 3, 0, 2, 4, 5]},
                {"args": [[[3, 1], [2, 2, 0], [], [5, 4]], [0, 4]], "expected": [1, 3, 2, 5]},
                {"args": [[], [1]], "expected": []},
                {"args": [[[1, 1, 1]], []], "expected": [1]},
            ],
            "hint": "Для каждой пачки: sorted(set(batch)) и фильтр по masked.",
        },
        {
            "id": "cheaper-mode",
            "mode": "func",
            "func": "cheaper_mode",
            "title": "Опрос или прерывания",
            "statement": (
                "Напишите функцию cheaper_mode(rate, irq_cost, poll_hz, "
                "poll_cost): rate — событий в секунду, irq_cost — тактов "
                "на одно прерывание, poll_hz — сколько раз в секунду "
                "опрашиваем устройство, poll_cost — тактов на один опрос. "
                "Верните кортеж (режим, тактов_в_секунду): 'interrupts' "
                "(rate · irq_cost) или 'polling' (poll_hz · poll_cost), "
                "в зависимости от того, что дешевле; при равенстве — "
                "'interrupts'."
            ),
            "starter": "def cheaper_mode(rate, irq_cost, poll_hz, poll_cost):\n    pass\n",
            "tests": [
                {"args": [10, 2000, 1000, 50], "expected": ("interrupts", 20000)},
                {"args": [1000, 2000, 1000, 50], "expected": ("polling", 50000)},
                {"args": [25, 2000, 1000, 50], "expected": ("interrupts", 50000)},
                {"args": [26, 2000, 1000, 50], "expected": ("polling", 50000)},
                {"args": [0, 500, 100, 10], "expected": ("interrupts", 0)},
            ],
            "hint": "Посчитайте обе стоимости и сравните.",
        },
        {
            "id": "hdd-access",
            "mode": "func",
            "func": "hdd_access_ms",
            "title": "Время обращения к жёсткому диску",
            "statement": (
                "Напишите функцию hdd_access_ms(rpm, seek_ms, size_bytes, "
                "mb_per_s): время случайного обращения в миллисекундах = "
                "поиск + половина оборота + передача size_bytes при "
                "скорости mb_per_s МБ/с (1 МБ = 10⁶ байт). Округлите до "
                "двух знаков."
            ),
            "starter": "def hdd_access_ms(rpm, seek_ms, size_bytes, mb_per_s):\n    pass\n",
            "tests": [
                {"args": [7200, 8, 4096, 150], "expected": 12.19},
                {"args": [5400, 12, 1048576, 100], "expected": 28.04},
                {"args": [15000, 3.5, 512, 200], "expected": 5.5},
                {"args": [7200, 0, 0, 100], "expected": 4.17},
            ],
            "hint": "Пол-оборота: 60000 / rpm / 2 мс; передача: size_bytes / (mb_per_s · 10⁶) · 1000 мс.",
        },
        {
            "id": "disk-scheduling",
            "mode": "func",
            "func": "head_movement",
            "title": "Планировщик диска",
            "statement": (
                "Напишите функцию head_movement(start, reqs, policy, "
                "cylinders): суммарный путь головки по цилиндрам. policy: "
                "'FCFS' — по порядку поступления; 'SSTF' — каждый раз "
                "ближайший запрос; 'SCAN' — головка идёт вверх до "
                "последнего цилиндра (cylinders − 1), затем вниз до "
                "наименьшего запроса ниже start (если такие есть); "
                "'CSCAN' — вверх до последнего цилиндра, возврат на "
                "цилиндр 0 (путь cylinders − 1 считается) и вверх до "
                "наибольшего запроса ниже start. Запросы с номером ≥ start "
                "обслуживаются по пути вверх. Для SCAN/CSCAN без запросов "
                "— 0."
            ),
            "starter": "def head_movement(start, reqs, policy, cylinders):\n    pass\n",
            "tests": [
                {"args": [53, [98, 183, 37, 122, 14, 124, 65, 67], "FCFS", 200], "expected": 640},
                {"args": [53, [98, 183, 37, 122, 14, 124, 65, 67], "SSTF", 200], "expected": 236},
                {"args": [53, [98, 183, 37, 122, 14, 124, 65, 67], "SCAN", 200], "expected": 331},
                {"args": [53, [98, 183, 37, 122, 14, 124, 65, 67], "CSCAN", 200], "expected": 382},
                {"args": [50, [10, 20], "FCFS", 100], "expected": 50},
                {"args": [50, [10, 20], "SSTF", 100], "expected": 40},
                {"args": [50, [10, 20], "SCAN", 100], "expected": 138},
                {"args": [50, [10, 20], "CSCAN", 100], "expected": 168},
                {"args": [0, [30, 60], "SCAN", 100], "expected": 99},
                {"args": [99, [5], "CSCAN", 100], "expected": 104},
                {"args": [10, [], "SCAN", 100], "expected": 0},
                {"args": [20, [10, 30, 20], "SCAN", 100], "expected": 168},
            ],
            "hint": "SCAN/CSCAN: ниже = [r for r in reqs if r < start]; путь вверх (cylinders − 1) − start, потом по условиям политики.",
        },
        {
            "id": "raid-recover",
            "mode": "func",
            "func": "raid_recover",
            "title": "Восстановление диска в RAID-5",
            "statement": (
                "Напишите функцию raid_recover(disks, failed): disks — "
                "список дисков (включая диск с чётностью), каждый — список "
                "байтов одной длины; failed — номер вышедшего из строя "
                "диска (его содержимое неизвестно, значение в списке "
                "игнорируется). Верните восстановленное содержимое "
                "этого диска — XOR всех остальных."
            ),
            "starter": "def raid_recover(disks, failed):\n    pass\n",
            "tests": [
                {"args": [[[0, 0, 0], [4, 5, 6], [2, 7, 4]], 0], "expected": [6, 2, 2]},
                {"args": [[[1, 2, 3], [4, 5, 6], [0, 0, 0]], 2], "expected": [5, 7, 5]},
                {"args": [[[10], [0], [30]], 1], "expected": [20]},
                {"args": [[[255, 0], [0, 255], [1, 2], [3, 4]], 3], "expected": [254, 253]},
            ],
            "hint": "Для каждой позиции — XOR значений всех дисков, кроме failed.",
        },
        {
            "id": "buffered-writes",
            "mode": "func",
            "func": "count_syscalls",
            "title": "Системные вызовы при буферизации",
            "statement": (
                "Напишите функцию count_syscalls(chunks, buf_size): "
                "chunks — размеры последовательных записей, buf_size — "
                "размер буфера. Правила: запись не меньше буфера сначала "
                "сбрасывает накопленное (если оно есть — один вызов), "
                "потом уходит напрямую одним вызовом; иначе, если запись "
                "не помещается в остаток буфера, буфер сбрасывается "
                "(один вызов) и запись начинает новый буфер; в конце "
                "непустой буфер сбрасывается. Верните число вызовов."
            ),
            "starter": "def count_syscalls(chunks, buf_size):\n    pass\n",
            "tests": [
                {"args": [[1] * 10000, 4096], "expected": 3},
                {"args": [[], 4096], "expected": 0},
                {"args": [[5000], 4096], "expected": 1},
                {"args": [[100, 4000, 100], 4096], "expected": 3},
                {"args": [[4096, 1, 4096], 4096], "expected": 3},
                {"args": [[10, 20, 30], 100], "expected": 1},
                {"args": [[2000, 2000, 2000], 4096], "expected": 2},
            ],
            "hint": "used — сколько байт в буфере; следите за тремя случаями: большая запись, переполнение буфера, обычное накопление.",
        },
        {
            "id": "merge-requests",
            "mode": "func",
            "func": "merge_requests",
            "title": "Слияние запросов к диску",
            "statement": (
                "Планировщик ввода-вывода склеивает соседние запросы. "
                "Напишите функцию merge_requests(reqs): reqs — список "
                "пар [начальный_блок, длина]. Объедините перекрывающиеся "
                "и соприкасающиеся диапазоны (конец одного = начало "
                "другого) и верните список [начало, длина] по возрастанию."
            ),
            "starter": "def merge_requests(reqs):\n    pass\n",
            "tests": [
                {"args": [[[10, 5], [0, 3], [15, 2], [3, 2]]], "expected": [[0, 5], [10, 7]]},
                {"args": [[]], "expected": []},
                {"args": [[[5, 1], [5, 3]]], "expected": [[5, 3]]},
                {"args": [[[0, 10], [2, 3]]], "expected": [[0, 10]]},
                {"args": [[[0, 1], [2, 1]]], "expected": [[0, 1], [2, 1]]},
            ],
            "hint": "Отсортируйте; если начало следующего ≤ концу текущего — продлите текущий (конец = максимум из двух).",
        },
    ],
    10: [
        {
            "id": "power-wall",
            "mode": "func",
            "func": "best_cores",
            "title": "Стена мощности",
            "statement": (
                "Относительные единицы: ядро на частоте f = 1 потребляет "
                "мощность 1 и даёт производительность 1; мощность ядра "
                "растёт как f³, производительность — как f (задача "
                "идеально параллелится). Напишите функцию best_cores(budget, "
                "max_cores): при бюджете мощности budget выберите число "
                "ядер n от 1 до max_cores; частота — наибольшая из "
                "допустимых: min(1.0, (budget / n) ** (1/3)). Верните "
                "кортеж (n, суммарная_производительность), округлив "
                "производительность до трёх знаков; при равенстве "
                "выбирайте меньшее n."
            ),
            "starter": "def best_cores(budget, max_cores):\n    pass\n",
            "tests": [
                {"args": [1, 8], "expected": (8, 4.0)},
                {"args": [4, 8], "expected": (8, 6.35)},
                {"args": [4, 2], "expected": (2, 2.0)},
                {"args": [2, 16], "expected": (16, 8.0)},
                {"args": [0.5, 4], "expected": (4, 2.0)},
                {"args": [8, 4], "expected": (4, 4.0)},
            ],
            "hint": "Для каждого n: f = min(1, (budget / n) ** (1 / 3)); perf = n · f; запоминайте строго лучший результат.",
        },
        {
            "id": "amdahl-gustafson",
            "mode": "func",
            "func": "speedups",
            "title": "Амдал и Густафсон",
            "statement": (
                "Напишите функцию speedups(p, n): p — доля параллельной "
                "части, n — число ядер. Верните кортеж (Амдал, Густафсон): "
                "Амдал = 1 / ((1 − p) + p / n) (размер задачи фиксирован), "
                "Густафсон = n − (1 − p)(n − 1) (задача растёт вместе с "
                "числом ядер). Оба значения округлите до двух знаков."
            ),
            "starter": "def speedups(p, n):\n    pass\n",
            "tests": [
                {"args": [0.95, 8], "expected": (5.93, 7.65)},
                {"args": [0.95, 64], "expected": (15.42, 60.85)},
                {"args": [0.5, 4], "expected": (1.6, 2.5)},
                {"args": [1.0, 16], "expected": (16.0, 16.0)},
                {"args": [0.0, 10], "expected": (1.0, 1.0)},
            ],
            "hint": "Подставьте числа в обе формулы и округлите.",
        },
        {
            "id": "mesi-simulate",
            "mode": "func",
            "func": "mesi_simulate",
            "title": "Протокол MESI",
            "statement": (
                "Напишите функцию mesi_simulate(ops, cores): одна кэш-строка "
                "на cores ядер, у каждого состояние 'M', 'E', 'S' или 'I' "
                "(в начале все 'I'). ops — список пар [ядро, 'R' или 'W']. "
                "Чтение при 'I': если у кого-то есть копия — у держателей "
                "'M' и 'E' состояние становится 'S' (запись в память "
                "игнорируем), читающий получает 'S'; если ни у кого нет — "
                "читающий получает 'E'. Чтение при M/E/S состояние не "
                "меняет. Запись: у остальных 'I', у пишущего 'M'. После "
                "каждой операции запишите состояния всех ядер одной строкой "
                "(например, 'SSI'). Верните список строк."
            ),
            "starter": "def mesi_simulate(ops, cores):\n    pass\n",
            "tests": [
                {"args": [[[0, "R"], [1, "R"], [0, "W"], [1, "R"]], 2], "expected": ["EI", "SS", "MI", "SS"]},
                {"args": [[[0, "W"], [0, "R"], [1, "W"]], 3], "expected": ["MII", "MII", "IMI"]},
                {"args": [[[2, "R"], [0, "R"], [1, "R"], [1, "W"]], 3], "expected": ["IIE", "SIS", "SSS", "IMI"]},
                {"args": [[], 2], "expected": []},
                {"args": [[[0, "W"], [1, "R"], [0, "R"]], 2], "expected": ["MI", "SS", "SS"]},
            ],
            "hint": "Одна функция шага с двумя ветками (R/W); состояния держите в списке символов.",
        },
        {
            "id": "false-sharing",
            "mode": "stdout",
            "title": "Пинг-понг кэш-строки",
            "statement": (
                "Напишите функцию ping_pong(writes, line): writes — список "
                "пар [ядро, адрес] — последовательные записи; line — "
                "размер кэш-строки. Верните, сколько раз строка «переезжала» "
                "от одного ядра к другому: запись в строку, которую "
                "последним писало другое ядро. Первая запись в строку "
                "переезда не считается. Проверка подаёт 400 000 записей."
            ),
            "starter": "def ping_pong(writes, line):\n    pass\n",
            "driver": (
                "print(ping_pong([(0, 0), (1, 8)] * 5, 64), ping_pong([(0, 0), (1, 64)] * 5, 64), ping_pong([(0, 0), (0, 8), (0, 16)], 64), ping_pong([(0, 0), (1, 4), (2, 8), (0, 12)], 64), ping_pong([], 64))\n"
                "big = [(i % 4, (i % 4) * 8) for i in range(400000)]\nprint(ping_pong(big, 64), ping_pong(big, 8))\n"
            ),
            "expected": ["9 0 0 3 0", "399999 0"],
            "hint": "Словарь «строка → последнее ядро»: block = addr // line; если ядро другое — счётчик +1.",
        },
        {
            "id": "counter-outcomes",
            "mode": "func",
            "func": "counter_outcomes",
            "title": "Какие значения может дать гонка",
            "statement": (
                "Несколько потоков (threads) увеличивают общий счётчик "
                "(начальное значение 0), каждый делает increments "
                "инкрементов. Один инкремент — две атомарные "
                "операции: load (прочитать счётчик в свой регистр) и "
                "store (записать регистр + 1). Шаги потоков "
                "чередуются в любом порядке. Напишите функцию "
                "counter_outcomes(threads, increments): отсортированный "
                "список всех возможных итоговых значений счётчика."
            ),
            "starter": "def counter_outcomes(threads, increments):\n    pass\n",
            "tests": [
                {"args": [1, 1], "expected": [1]},
                {"args": [2, 1], "expected": [1, 2]},
                {"args": [3, 1], "expected": [1, 2, 3]},
                {"args": [2, 2], "expected": [2, 3, 4]},
                {"args": [1, 3], "expected": [3]},
                {"args": [3, 2], "expected": [2, 3, 4, 5, 6]},
                {"args": [0, 5], "expected": [0]},
            ],
            "hint": "Поиск в глубину по состояниям (счётчик, у каждого потока: сколько осталось инкрементов и что лежит в регистре); множество посещённых состояний не даёт перебору взорваться.",
        },
        {
            "id": "cas-increment",
            "mode": "stdout",
            "title": "Счётчик на CAS",
            "statement": (
                "Напишите функцию increment(cell), которая атомарно "
                "увеличивает cell.v на 1 с помощью метода "
                "cell.cas(expected, new) (возвращает True, если значение "
                "совпало и заменено). Не используйте блокировки и "
                "присваивание cell.v напрямую: проверка запускает 8 "
                "потоков по 2000 увеличений и специально провоцирует "
                "гонки при чтении cell.v."
            ),
            "starter": "def increment(cell):\n    pass\n",
            "driver": (
                "import threading, time\n"
                "class Cell:\n    def __init__(self, v):\n        self._v = v\n        self._lock = threading.Lock()\n"
                "    @property\n    def v(self):\n        val = self._v\n        time.sleep(0)\n        return val\n"
                "    @v.setter\n    def v(self, value):\n        self._v = value\n"
                "    def cas(self, expected, new):\n        with self._lock:\n            if self._v == expected:\n                self._v = new\n                return True\n            return False\n"
                "cell = Cell(0)\n"
                "def worker():\n    for _ in range(2000):\n        increment(cell)\n"
                "threads = [threading.Thread(target=worker) for _ in range(8)]\n"
                "for t in threads:\n    t.start()\nfor t in threads:\n    t.join()\nprint(cell._v)\n"
            ),
            "expected": ["16000"],
            "hint": "while True: old = cell.v; if cell.cas(old, old + 1): return — повтор при неудаче.",
        },
        {
            "id": "simd-dot",
            "mode": "func",
            "func": "simd_dot",
            "title": "Скалярное произведение на векторах",
            "statement": (
                "Напишите функцию simd_dot(a, b, width): скалярное "
                "произведение списков одинаковой длины. Обработка "
                "кусками по width элементов — каждый полный кусок это "
                "одна векторная команда; «хвост», не заполняющий вектор, "
                "считается по одному элементу (скалярные команды). Верните "
                "кортеж (результат, векторных_команд, скалярных_команд)."
            ),
            "starter": "def simd_dot(a, b, width):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3, 4, 5, 6, 7, 8], [1, 1, 1, 1, 1, 1, 1, 1], 4], "expected": (36, 2, 0)},
                {"args": [[1, 2, 3, 4, 5], [2, 2, 2, 2, 2], 4], "expected": (30, 1, 1)},
                {"args": [[], [], 8], "expected": (0, 0, 0)},
                {"args": [[3], [4], 8], "expected": (12, 0, 1)},
                {"args": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 4], "expected": (285, 2, 2)},
            ],
            "hint": "full = n - n % width; цикл по кускам до full, потом хвост.",
        },
        {
            "id": "warp-divergence",
            "mode": "func",
            "func": "warp_cost",
            "title": "Расхождение потоков в варпе",
            "statement": (
                "Напишите функцию warp_cost(conditions, then_cost, "
                "else_cost, warp_size): потоки разбиты на варпы по "
                "warp_size подряд идущих (последний может быть короче). "
                "У каждого потока условие True/False. Варп выполняет ветку "
                "«then» (then_cost тактов), если хоть у одного потока "
                "True, и ветку «else» (else_cost), если хоть у одного "
                "False. Верните суммарное число тактов по всем варпам."
            ),
            "starter": "def warp_cost(conditions, then_cost, else_cost, warp_size):\n    pass\n",
            "tests": [
                {"args": [[True] * 32, 10, 10, 32], "expected": 10},
                {"args": [[True] * 31 + [False], 10, 10, 32], "expected": 20},
                {"args": [[False] * 64, 10, 5, 32], "expected": 10},
                {"args": [[True, False] * 32, 10, 5, 32], "expected": 30},
                {"args": [[], 10, 10, 32], "expected": 0},
                {"args": [[True] * 5, 3, 1, 4], "expected": 6},
            ],
            "hint": "Для каждого среза w: if any(w): += then_cost; if not all(w): += else_cost.",
        },
        {
            "id": "optimal-threads",
            "mode": "func",
            "func": "optimal_threads",
            "title": "Сколько потоков запускать",
            "statement": (
                "Время работы с n потоками: T(n) = serial + parallel / n "
                "+ overhead · n (накладные расходы на синхронизацию растут "
                "с числом потоков). Напишите функцию optimal_threads(serial, "
                "parallel, overhead, max_n): верните кортеж (n, T(n)) "
                "для n от 1 до max_n, дающего наименьшее время; при "
                "равенстве — меньшее n. T округлите до трёх знаков."
            ),
            "starter": "def optimal_threads(serial, parallel, overhead, max_n):\n    pass\n",
            "tests": [
                {"args": [10, 100, 0.5, 64], "expected": (14, 24.143)},
                {"args": [0, 100, 0, 16], "expected": (16, 6.25)},
                {"args": [5, 50, 2, 8], "expected": (5, 25.0)},
                {"args": [1, 1, 10, 4], "expected": (1, 12.0)},
            ],
            "hint": "Переберите n от 1 до max_n и запомните строго лучшее время.",
        },
    ],
}
