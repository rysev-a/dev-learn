"""Задачи книги «Виртуализация»: глава 2 — Trap-and-emulate и проблема x86: двоичная трансляция и паравиртуализация."""

TASKS: dict[int, list[dict]] = {
    2: [
        {
            "id": "virt-trap-run",
            "mode": "func",
            "func": "run_guest",
            "title": "Монитор имитирует гостя",
            "statement": (
                "Напишите функцию run_guest(program): program — список команд гостевого ядра. Монитор "
                "ведёт виртуальные регистры: acc = 0, vif (виртуальный флаг прерываний) = 1, vcr3 = "
                "0. «ADD n» прибавляет n к acc и выполняется напрямую. Остальные команды — ловушки, "
                "каждая считается: «CLI» ставит vif = 0, «STI» — vif = 1, «WRCR3 v» ставит vcr3 = v, "
                "«RDCR3» записывает в acc значение vcr3, «HLT» (тоже ловушка) останавливает гостя, "
                "остальные команды не выполняются. Верните кортеж (acc, vif, vcr3, число ловушек)."
            ),
            "starter": "def run_guest(program):\n    pass\n",
            "tests": [
                {"args": [[]], "expected": (0, 1, 0, 0)},
                {"args": [["ADD 5", "ADD 7"]], "expected": (12, 1, 0, 0)},
                {"args": [["CLI", "ADD 1", "STI"]], "expected": (1, 1, 0, 2)},
                {"args": [["CLI", "HLT", "ADD 9"]], "expected": (0, 0, 0, 2)},
                {
                    "args": [["WRCR3 4096", "RDCR3", "ADD 1"]],
                    "expected": (4097, 1, 4096, 2),
                },
                {"args": [["ADD 3", "RDCR3"]], "expected": (0, 1, 0, 1)},
                {"args": [["CLI", "CLI", "ADD 2"]], "expected": (2, 0, 0, 2)},
            ],
            "hint": (
                "Разбирайте строку через split(); ADD не увеличивает счётчик ловушек, всё остальное "
                "увеличивает."
            ),
        },
        {
            "id": "virt-vif-queue",
            "mode": "func",
            "func": "deliver",
            "title": "Виртуальные прерывания",
            "statement": (
                "Напишите функцию deliver(events): events — события, приходящие монитору: «CLI» "
                "(гость запретил прерывания), «STI» (разрешил), «IRQ n» (пришло прерывание с номером "
                "n). Сначала виртуальный флаг разрешён. IRQ при разрешённом флаге доставляется гостю "
                "сразу; при запрещённом ждёт в очереди. «STI» разрешает флаг и доставляет всю очередь "
                "в порядке поступления. Верните кортеж (список доставленных номеров по порядку, "
                "список номеров, оставшихся в очереди)."
            ),
            "starter": "def deliver(events):\n    pass\n",
            "tests": [
                {"args": [[]], "expected": ([], [])},
                {"args": [["IRQ 1", "IRQ 2"]], "expected": ([1, 2], [])},
                {"args": [["CLI", "IRQ 3", "IRQ 4"]], "expected": ([], [3, 4])},
                {"args": [["CLI", "IRQ 3", "STI", "IRQ 4"]], "expected": ([3, 4], [])},
                {
                    "args": [["CLI", "IRQ 1", "STI", "CLI", "IRQ 2", "IRQ 3"]],
                    "expected": ([1], [2, 3]),
                },
                {"args": [["IRQ 7", "CLI", "STI", "CLI"]], "expected": ([7], [])},
                {"args": [["CLI", "STI", "STI", "IRQ 5"]], "expected": ([5], [])},
            ],
            "hint": (
                "Храните флаг и очередь; на STI перенесите очередь в список доставленных."
            ),
        },
        {
            "id": "virt-popf",
            "mode": "func",
            "func": "popf",
            "title": "POPF в разных кольцах",
            "statement": (
                "Напишите функцию popf(ring, flags, new): ring — кольцо защиты (0–3), flags — текущий "
                "регистр флагов, new — значение, снятое со стека командой POPF. В кольце 0 команда "
                "записывает все флаги: результат равен new. В кольцах 1–3 бит IF (значение 512, бит "
                "9) остаётся прежним, а остальные биты берутся из new — молча, без ошибки и ловушки. "
                "Верните новый регистр флагов."
            ),
            "starter": "def popf(ring, flags, new):\n    pass\n",
            "tests": [
                {"args": [0, 0, 514], "expected": 514},
                {"args": [1, 0, 514], "expected": 2},
                {"args": [1, 512, 2], "expected": 514},
                {"args": [3, 512, 0], "expected": 512},
                {"args": [0, 512, 0], "expected": 0},
                {"args": [2, 0, 1], "expected": 1},
                {"args": [1, 0, 0], "expected": 0},
                {"args": [0, 123, 5], "expected": 5},
            ],
            "hint": (
                "IF = 512. Результат вне кольца 0: (new без бита 512) | (flags & 512)."
            ),
        },
        {
            "id": "virt-ring-counts",
            "mode": "func",
            "func": "outcome_counts",
            "title": "Что случится с гостевым ядром",
            "statement": (
                "Гостевое ядро запущено в кольце ring (0–3). Напишите функцию outcome_counts(kinds, "
                "ring): kinds — список видов команд: «normal» (обычная), «privileged» "
                "(привилегированная), «sensitive» (чувствительная, но не привилегированная). Обычная "
                "команда выполняется напрямую всегда. Привилегированная выполняется напрямую только в "
                "кольце 0, иначе вызывает ловушку. Чувствительная в кольце 0 работает как надо, а в "
                "остальных кольцах выполняется «молча» — без ловушки, но неверно. Верните кортеж "
                "(напрямую, ловушек, молчаливых ошибок)."
            ),
            "starter": "def outcome_counts(kinds, ring):\n    pass\n",
            "tests": [
                {
                    "args": [["normal", "privileged", "sensitive"], 1],
                    "expected": (1, 1, 1),
                },
                {"args": [["normal", "normal", "normal"], 0], "expected": (3, 0, 0)},
                {"args": [[], 1], "expected": (0, 0, 0)},
                {
                    "args": [["privileged", "privileged", "sensitive"], 3],
                    "expected": (0, 2, 1),
                },
                {"args": [["sensitive", "sensitive"], 0], "expected": (2, 0, 0)},
                {
                    "args": [["sensitive", "normal", "privileged", "sensitive"], 1],
                    "expected": (1, 1, 2),
                },
            ],
            "hint": ("Заведите три счётчика и пройдите по kinds."),
        },
        {
            "id": "virt-translate",
            "mode": "func",
            "func": "translate",
            "title": "Двоичная трансляция блоков",
            "statement": (
                "Напишите функцию translate(code, unsafe): code — список команд гостевого ядра "
                "(строки вида «add eax, 2»; мнемоника — первое слово), unsafe — список опасных "
                "мнемоник. Транслятор режет код на базовые блоки: блок заканчивается командой "
                "перехода (мнемоники jmp, jz, jnz, call, ret), включая её; следующий блок начинается "
                "со следующей команды, остаток без перехода — тоже блок. Опасные команды заменяются "
                "на «call vmm_<мнемоника>», остальные остаются. Конец блока определяется по исходной "
                "команде. Верните список кортежей (индекс первой команды блока, список команд блока)."
            ),
            "starter": "def translate(code, unsafe):\n    pass\n",
            "tests": [
                {
                    "args": [
                        ["mov eax, 1", "popf", "add eax, 2", "jmp L1", "nop", "ret"],
                        ["popf"],
                    ],
                    "expected": [
                        (0, ["mov eax, 1", "call vmm_popf", "add eax, 2", "jmp L1"]),
                        (4, ["nop", "ret"]),
                    ],
                },
                {"args": [[], ["popf"]], "expected": []},
                {"args": [["nop", "nop"], []], "expected": [(0, ["nop", "nop"])]},
                {
                    "args": [
                        ["pushf", "jz L", "smsw ax", "call f", "sgdt [x]"],
                        ["pushf", "smsw", "sgdt"],
                    ],
                    "expected": [
                        (0, ["call vmm_pushf", "jz L"]),
                        (2, ["call vmm_smsw", "call f"]),
                        (4, ["call vmm_sgdt"]),
                    ],
                },
                {"args": [["ret"], ["ret"]], "expected": [(0, ["call vmm_ret"])]},
                {
                    "args": [["add eax, 1", "jmp A", "jmp B"], []],
                    "expected": [(0, ["add eax, 1", "jmp A"]), (2, ["jmp B"])],
                },
            ],
            "hint": (
                "Накапливайте текущий блок и закрывайте его, увидев переход; не забудьте последний "
                "блок."
            ),
        },
        {
            "id": "virt-hypercall",
            "mode": "func",
            "func": "hypercall",
            "title": "Диспетчер гипервызовов",
            "statement": (
                'Напишите функцию hypercall(vm, nr, args): vm — словарь {"frames": [номера машинных '
                'кадров, принадлежащих гостю], "timer": None или число, "console": строка, "p2m": '
                "словарь}, nr — номер вызова, args — список аргументов. Вызовы: 0 — yield, возвращает "
                "0; 1 — set_timer(ns): при ns >= 0 записывает timer = ns и возвращает 0, иначе "
                "возвращает -22; 2 — console_write(text): дописывает text в console и возвращает "
                "длину text; 3 — map_page(gfn, mfn): если mfn нет в frames, возвращает -1, иначе "
                "пишет p2m[str(gfn)] = mfn и возвращает 0; любой другой номер — -38. Не меняйте "
                "переданный vm: верните кортеж (код, новый vm)."
            ),
            "starter": "def hypercall(vm, nr, args):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {"frames": [10, 11], "timer": None, "console": "", "p2m": {}},
                        0,
                        [],
                    ],
                    "expected": (
                        0,
                        {"frames": [10, 11], "timer": None, "console": "", "p2m": {}},
                    ),
                },
                {
                    "args": [
                        {"frames": [10, 11], "timer": None, "console": "", "p2m": {}},
                        1,
                        [5000],
                    ],
                    "expected": (
                        0,
                        {"frames": [10, 11], "timer": 5000, "console": "", "p2m": {}},
                    ),
                },
                {
                    "args": [
                        {"frames": [10, 11], "timer": None, "console": "", "p2m": {}},
                        1,
                        [-1],
                    ],
                    "expected": (
                        -22,
                        {"frames": [10, 11], "timer": None, "console": "", "p2m": {}},
                    ),
                },
                {
                    "args": [
                        {"frames": [10, 11], "timer": None, "console": "", "p2m": {}},
                        2,
                        ["hi"],
                    ],
                    "expected": (
                        2,
                        {"frames": [10, 11], "timer": None, "console": "hi", "p2m": {}},
                    ),
                },
                {
                    "args": [
                        {"frames": [10, 11], "timer": None, "console": "ab", "p2m": {}},
                        2,
                        ["cd"],
                    ],
                    "expected": (
                        2,
                        {
                            "frames": [10, 11],
                            "timer": None,
                            "console": "abcd",
                            "p2m": {},
                        },
                    ),
                },
                {
                    "args": [
                        {"frames": [10, 11], "timer": None, "console": "", "p2m": {}},
                        3,
                        [7, 10],
                    ],
                    "expected": (
                        0,
                        {
                            "frames": [10, 11],
                            "timer": None,
                            "console": "",
                            "p2m": {"7": 10},
                        },
                    ),
                },
                {
                    "args": [
                        {"frames": [10, 11], "timer": None, "console": "", "p2m": {}},
                        3,
                        [7, 99],
                    ],
                    "expected": (
                        -1,
                        {"frames": [10, 11], "timer": None, "console": "", "p2m": {}},
                    ),
                },
                {
                    "args": [
                        {"frames": [10, 11], "timer": None, "console": "", "p2m": {}},
                        99,
                        [],
                    ],
                    "expected": (
                        -38,
                        {"frames": [10, 11], "timer": None, "console": "", "p2m": {}},
                    ),
                },
            ],
            "hint": ("Начните с copy.deepcopy(vm), изменения вносите в копию."),
        },
        {
            "id": "virt-multicall",
            "mode": "func",
            "func": "batch_cost",
            "title": "Пакетные гипервызовы",
            "statement": (
                "Паравиртуальное ядро может отправлять гипервызовы пачками. Напишите функцию "
                "batch_cost(n_calls, batch, trap, per_call): n_calls — сколько просьб надо выполнить, "
                "batch — максимум просьб в одном гипервызове, trap — цена одной ловушки в тактах, "
                "per_call — цена выполнения одной просьбы. Верните кортеж (число ловушек, суммарная "
                "цена в тактах). Для n_calls = 0 — (0, 0)."
            ),
            "starter": "def batch_cost(n_calls, batch, trap, per_call):\n    pass\n",
            "tests": [
                {"args": [0, 10, 1000, 50], "expected": (0, 0)},
                {"args": [10, 1, 1000, 50], "expected": (10, 10500)},
                {"args": [10, 10, 1000, 50], "expected": (1, 1500)},
                {"args": [10, 4, 1000, 50], "expected": (3, 3500)},
                {"args": [1, 8, 2000, 100], "expected": (1, 2100)},
                {"args": [100, 32, 1500, 20], "expected": (4, 8000)},
            ],
            "hint": (
                "Число ловушек — деление с округлением вверх: -(-n_calls // batch)."
            ),
        },
        {
            "id": "virt-cheapest",
            "mode": "func",
            "func": "cheapest",
            "title": "Какой способ дешевле",
            "statement": (
                "Напишите функцию cheapest(n_ops, strategies): strategies — список [имя, "
                "разовая_цена, цена_за_операцию] способов виртуализации (перехват, трансляция, "
                "паравиртуализация). Цена способа для n_ops операций — разовая_цена + "
                "цена_за_операцию * n_ops. Верните имя самого дешёвого способа; при равенстве — того, "
                "что раньше в списке."
            ),
            "starter": "def cheapest(n_ops, strategies):\n    pass\n",
            "tests": [
                {
                    "args": [
                        10,
                        [["trap", 0, 3000], ["bt", 100000, 100], ["pv", 0, 600]],
                    ],
                    "expected": "pv",
                },
                {
                    "args": [
                        100000,
                        [["trap", 0, 3000], ["bt", 100000, 100], ["pv", 50000000, 0]],
                    ],
                    "expected": "bt",
                },
                {"args": [0, [["a", 5, 1], ["b", 3, 9]]], "expected": "b"},
                {
                    "args": [5, [["a", 10, 0], ["b", 5, 1], ["c", 5, 1]]],
                    "expected": "a",
                },
                {"args": [1000, [["x", 0, 1]]], "expected": "x"},
                {"args": [3, [["slow", 0, 10], ["fast", 20, 1]]], "expected": "fast"},
            ],
            "hint": ("Подойдёт min с ключом: он возвращает первый из равных."),
        },
    ],
}
