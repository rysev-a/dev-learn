"""Задачи книги «Виртуализация»: глава 15 — Вложенная виртуализация: гипервизор внутри виртуальной машины."""

TASKS: dict[int, list[dict]] = {
    15: [
        {
            "id": "virt-l0-exits",
            "mode": "func",
            "func": "l0_exits",
            "title": "Выходы в L0 при вложенности",
            "statement": (
                "Напишите функцию l0_exits(kinds, accesses, shadowing): kinds — список выходов машины "
                'L2, каждый — "l0" (его целиком обрабатывает гипервизор L0) или "l1" (он адресован '
                "гипервизору L1). accesses — сколько полей управляющей структуры читает и пишет L1 "
                "при обработке одного такого выхода, shadowing — включена ли теневая структура "
                '(обращения L1 к полям без выхода). Выход "l0" стоит один выход в L0. Выход "l1" '
                "стоит 2 выхода в L0 (сам выход L2 и возобновление L1) плюс accesses, если shadowing "
                "выключен. Верните суммарное число выходов в L0."
            ),
            "starter": "def l0_exits(kinds, accesses, shadowing):\n    pass\n",
            "tests": [
                {"args": [["l0", "l0", "l1"], 10, False], "expected": 14},
                {"args": [["l0", "l0", "l1"], 10, True], "expected": 4},
                {"args": [[], 10, False], "expected": 0},
                {"args": [["l1", "l1"], 30, False], "expected": 64},
                {"args": [["l1", "l1"], 30, True], "expected": 4},
                {"args": [["l0"], 5, False], "expected": 1},
            ],
            "hint": ("Сложите стоимость каждого выхода по его виду."),
        },
        {
            "id": "virt-merge-vmcs",
            "mode": "func",
            "func": "merge_vmcs",
            "title": "Слияние VMCS",
            "statement": (
                "Напишите функцию merge_vmcs(v12, v01): v12 — описание машины L2, которое подготовил "
                "гипервизор L1, и v01 — структура самого L1 у гипервизора L0. Каждая — словарь "
                '{"guest": {поле: значение}, "host": {поле: значение}, "controls": [имена включённых '
                "перехватов]}. Настоящая структура VMCS 0-2: состояние гостя берётся из v12, "
                "состояние хозяина — из v01 (возвращаться нужно в L0), перехваты — объединение "
                "перехватов обеих структур. Верните словарь того же вида; список перехватов "
                "отсортируйте."
            ),
            "starter": "def merge_vmcs(v12, v01):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {
                            "guest": {"rip": 1, "rsp": 2},
                            "host": {"rip": 100},
                            "controls": ["hlt", "io"],
                        },
                        {
                            "guest": {"rip": 50},
                            "host": {"rip": 900, "rsp": 800},
                            "controls": ["io", "msr"],
                        },
                    ],
                    "expected": {
                        "guest": {"rip": 1, "rsp": 2},
                        "host": {"rip": 900, "rsp": 800},
                        "controls": ["hlt", "io", "msr"],
                    },
                },
                {
                    "args": [
                        {"guest": {}, "host": {}, "controls": []},
                        {"guest": {}, "host": {}, "controls": []},
                    ],
                    "expected": {"guest": {}, "host": {}, "controls": []},
                },
                {
                    "args": [
                        {"guest": {"cr3": 7}, "host": {}, "controls": ["cpuid"]},
                        {
                            "guest": {"cr3": 1},
                            "host": {"cr3": 9},
                            "controls": ["cpuid"],
                        },
                    ],
                    "expected": {
                        "guest": {"cr3": 7},
                        "host": {"cr3": 9},
                        "controls": ["cpuid"],
                    },
                },
                {
                    "args": [
                        {"guest": {"a": 1}, "host": {"b": 2}, "controls": ["z", "a"]},
                        {"guest": {"c": 3}, "host": {"d": 4}, "controls": ["m"]},
                    ],
                    "expected": {
                        "guest": {"a": 1},
                        "host": {"d": 4},
                        "controls": ["a", "m", "z"],
                    },
                },
            ],
            "hint": ("Объедините перехваты через множества и отсортируйте."),
        },
        {
            "id": "virt-build-ept02",
            "mode": "func",
            "func": "build_ept02",
            "title": "Склейка вложенных таблиц",
            "statement": (
                "Напишите функцию build_ept02(ept12, ept01): ept12 — таблица L1 для L2 (словарь "
                "«страница L2 (строка) → страница L1»), ept01 — таблица L0 для L1 (словарь «страница "
                "L1 (строка) → хозяйская страница»). Постройте таблицу, которую L0 даст процессору: "
                "«страница L2 (строка) → хозяйская страница». В неё входят только те страницы L2, для "
                "которых есть отображение в обеих таблицах."
            ),
            "starter": "def build_ept02(ept12, ept01):\n    pass\n",
            "tests": [
                {
                    "args": [{"0": 5, "1": 6}, {"5": 100, "6": 101}],
                    "expected": {"0": 100, "1": 101},
                },
                {"args": [{"0": 5, "1": 6}, {"5": 100}], "expected": {"0": 100}},
                {"args": [{}, {"1": 2}], "expected": {}},
                {"args": [{"3": 9}, {}], "expected": {}},
                {"args": [{"0": 1, "1": 1}, {"1": 42}], "expected": {"0": 42, "1": 42}},
            ],
            "hint": ("Ключи таблиц — строки: используйте str() для номеров страниц."),
        },
        {
            "id": "virt-route-nested",
            "mode": "func",
            "func": "route_nested_exits",
            "title": "Чей выход",
            "statement": (
                "Напишите функцию route_nested_exits(reasons, l1_intercepts): reasons — причины "
                "выходов машины L2 по порядку, l1_intercepts — причины, которые гипервизор L1 "
                "попросил перехватывать у своей машины. Гипервизор L0 всегда обрабатывает сам "
                "EXTERNAL_INTERRUPT и EPT_VIOLATION_01 (ошибки собственной таблицы L0). Остальные "
                'причины L0 передаёт L1 ("l1"), если L1 их перехватывает, иначе обрабатывает сам '
                '("l0"). Верните список "l0"/"l1" по каждому выходу.'
            ),
            "starter": "def route_nested_exits(reasons, l1_intercepts):\n    pass\n",
            "tests": [
                {
                    "args": [
                        ["CPUID", "HLT", "EXTERNAL_INTERRUPT", "IO"],
                        ["CPUID", "IO"],
                    ],
                    "expected": ["l1", "l0", "l0", "l1"],
                },
                {"args": [[], ["CPUID"]], "expected": []},
                {
                    "args": [["EXTERNAL_INTERRUPT"], ["EXTERNAL_INTERRUPT"]],
                    "expected": ["l0"],
                },
                {
                    "args": [["EPT_VIOLATION_01", "MSR"], ["EPT_VIOLATION_01", "MSR"]],
                    "expected": ["l0", "l1"],
                },
                {"args": [["HLT", "HLT"], []], "expected": ["l0", "l0"]},
                {"args": [["CPUID", "CPUID"], ["CPUID"]], "expected": ["l1", "l1"]},
            ],
            "hint": ("Проверяйте сначала причины, которые всегда остаются у L0."),
        },
        {
            "id": "virt-can-nest",
            "mode": "func",
            "func": "can_nest",
            "title": "Можно ли запустить гипервизор",
            "statement": (
                "Напишите функцию can_nest(flags_line, nested): flags_line — строка flags из "
                "/proc/cpuinfo гостя (имя поля, двоеточие и список признаков через пробел), nested — "
                'значение параметра nested модуля KVM ("Y", "1", "N", "0" или другое). Признак vmx '
                'означает Intel, svm — AMD. Верните кортеж (вендор: "intel", "amd" или None, можно ли '
                'запустить вложенный гипервизор — вендор определён и nested равен "Y", "y" или "1").'
            ),
            "starter": "def can_nest(flags_line, nested):\n    pass\n",
            "tests": [
                {
                    "args": ["flags\t\t: fpu vme vmx ept vpid", "Y"],
                    "expected": ("intel", True),
                },
                {
                    "args": ["flags\t\t: fpu vme svm npt", "1"],
                    "expected": ("amd", True),
                },
                {"args": ["flags\t\t: fpu vme sse2", "Y"], "expected": (None, False)},
                {"args": ["flags : fpu vmx", "N"], "expected": ("intel", False)},
                {"args": ["flags : fpu vmxfoo avx", "Y"], "expected": (None, False)},
                {"args": ["flags : svm", "0"], "expected": ("amd", False)},
                {"args": ["flags : vmx hypervisor", "y"], "expected": ("intel", True)},
            ],
            "hint": ("Разберите признаки как отдельные слова после двоеточия."),
        },
        {
            "id": "virt-nested-slowdown",
            "mode": "func",
            "func": "nested_slowdown",
            "title": "Замедление из-за выходов",
            "statement": (
                "Напишите функцию nested_slowdown(exits_per_s, cost_cycles, hz, factor): сколько "
                "процентов процессорного времени съедают выходы. Для обычной машины это exits_per_s * "
                "cost_cycles * 100 // hz (целое, не больше 100). Для вложенной цена выхода умножается "
                "на factor. Верните кортеж (проценты для обычной машины, проценты для вложенной), "
                "каждое не больше 100."
            ),
            "starter": "def nested_slowdown(exits_per_s, cost_cycles, hz, factor):\n    pass\n",
            "tests": [
                {"args": [10000, 2000, 3000000000, 10], "expected": (0, 6)},
                {"args": [100000, 2000, 3000000000, 10], "expected": (6, 66)},
                {"args": [100000, 2000, 3000000000, 2], "expected": (6, 13)},
                {"args": [0, 2000, 3000000000, 10], "expected": (0, 0)},
                {"args": [1000000, 3000, 3000000000, 5], "expected": (100, 100)},
                {"args": [5000, 1500, 2000000000, 4], "expected": (0, 1)},
            ],
            "hint": (
                "Считайте целыми числами: сначала умножайте, потом делите; ограничьте результат "
                "сотней."
            ),
        },
        {
            "id": "virt-pick-nesting",
            "mode": "func",
            "func": "pick_nesting",
            "title": "Чем заменить вложенность",
            "statement": (
                'Напишите функцию pick_nesting(env): env — словарь с логическими полями "bare_metal" '
                '(доступна машина без гипервизора), "cloud_allows" (облако разрешает вложенную '
                'виртуализацию), "tcg_ok" (допустима программная трансляция, медленно). Правила по '
                'порядку: есть bare-metal — "bare-metal"; облако разрешает — "nested-kvm"; допустима '
                'трансляция — "tcg"; иначе — "none".'
            ),
            "starter": "def pick_nesting(env):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {"bare_metal": True, "cloud_allows": True, "tcg_ok": True}
                    ],
                    "expected": "bare-metal",
                },
                {
                    "args": [
                        {"bare_metal": False, "cloud_allows": True, "tcg_ok": True}
                    ],
                    "expected": "nested-kvm",
                },
                {
                    "args": [
                        {"bare_metal": False, "cloud_allows": False, "tcg_ok": True}
                    ],
                    "expected": "tcg",
                },
                {
                    "args": [
                        {"bare_metal": False, "cloud_allows": False, "tcg_ok": False}
                    ],
                    "expected": "none",
                },
                {
                    "args": [
                        {"bare_metal": True, "cloud_allows": False, "tcg_ok": False}
                    ],
                    "expected": "bare-metal",
                },
            ],
            "hint": ("Проверяйте условия строго в указанном порядке."),
        },
        {
            "id": "virt-vmcs-shadow",
            "mode": "func",
            "func": "vmcs_exits",
            "title": "Какие обращения к VMCS вызывают выход",
            "statement": (
                "Напишите функцию vmcs_exits(accesses, shadowed): accesses — поля управляющей "
                "структуры, к которым по очереди обращается гипервизор L1, shadowed — список полей, "
                "разрешённых без выхода (VMCS shadowing). Обращение к такому полю идёт напрямую, к "
                "остальным — выход в L0. Верните кортеж (число выходов, число прямых обращений)."
            ),
            "starter": "def vmcs_exits(accesses, shadowed):\n    pass\n",
            "tests": [
                {
                    "args": [
                        ["guest_rip", "guest_rsp", "exit_reason", "ept_pointer"],
                        ["guest_rip", "guest_rsp", "exit_reason"],
                    ],
                    "expected": (1, 3),
                },
                {"args": [[], ["a"]], "expected": (0, 0)},
                {"args": [["a", "a", "b"], []], "expected": (3, 0)},
                {"args": [["a", "b"], ["a", "b", "c"]], "expected": (0, 2)},
                {"args": [["x", "x", "x", "x", "x"], ["x"]], "expected": (0, 5)},
            ],
            "hint": ("Сравнивайте каждое поле со множеством разрешённых."),
        },
    ],
}
