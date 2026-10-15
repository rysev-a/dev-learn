"""Задачи книги «Виртуализация»: глава 3 — Аппаратная поддержка: VT-x, AMD-V, VM exit, ARM EL2 и RISC-V H."""

TASKS: dict[int, list[dict]] = {
    3: [
        {
            "id": "virt-exits",
            "mode": "func",
            "func": "exits",
            "title": "Какие команды вызовут выход",
            "statement": (
                "Напишите функцию exits(program, controls): program — список мнемоник команд гостя, "
                "controls — список включённых битов перехвата в VMCS. Выход вызывают всегда: CPUID, "
                "VMCALL, VMXON, VMLAUNCH. Остальное зависит от битов: HLT — «hlt_exiting», IN и OUT — "
                "«io_exiting», MOV_CR3 — «cr3_load_exiting», RDMSR и WRMSR — «msr_exiting». Прочие "
                "команды (ADD, MOV и т. д.) не вызывают выхода никогда. Верните список индексов "
                "команд, на которых гость выйдет в монитор."
            ),
            "starter": "def exits(program, controls):\n    pass\n",
            "tests": [
                {"args": [["ADD", "CPUID", "MOV"], []], "expected": [1]},
                {"args": [["HLT", "HLT"], []], "expected": []},
                {"args": [["HLT", "HLT"], ["hlt_exiting"]], "expected": [0, 1]},
                {"args": [["IN", "OUT", "ADD"], ["io_exiting"]], "expected": [0, 1]},
                {
                    "args": [["MOV_CR3", "RDMSR", "WRMSR"], ["cr3_load_exiting"]],
                    "expected": [0],
                },
                {
                    "args": [
                        ["RDMSR", "WRMSR", "VMCALL", "VMXON", "VMLAUNCH"],
                        ["msr_exiting"],
                    ],
                    "expected": [0, 1, 2, 3, 4],
                },
                {
                    "args": [["MOV_CR3"], ["hlt_exiting", "io_exiting", "msr_exiting"]],
                    "expected": [],
                },
                {"args": [[], ["hlt_exiting"]], "expected": []},
            ],
            "hint": (
                "Заведите словарь «мнемоника → бит» и множество безусловных выходов."
            ),
        },
        {
            "id": "virt-vmcs-cycle",
            "mode": "func",
            "func": "vm_cycle",
            "title": "Вход и выход через VMCS",
            "statement": (
                "Напишите функцию vm_cycle(host, guest, events): host и guest — словари регистров "
                '(например {"rip": 100, "rsp": 200}), events — список событий. Вначале cpu — копия '
                'host, vmcs_host — копия host, vmcs_guest — копия guest. События: ["enter"] (VM '
                'entry) — сохраняет cpu в vmcs_host и загружает в cpu копию vmcs_guest; ["run", поля] '
                'и ["monitor", поля] — обновляют регистры cpu (выполняет гость или монитор); ["exit", '
                "причина] (VM exit) — сохраняет cpu в vmcs_guest, загружает в cpu копию vmcs_host и "
                'добавляет причину в журнал; ["vmwrite", поля] — обновляет vmcs_guest. Верните кортеж '
                "(cpu, vmcs_host, vmcs_guest, журнал причин)."
            ),
            "starter": "def vm_cycle(host, guest, events):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {"rip": 100, "rsp": 200, "cr3": 1},
                        {"rip": 0, "rsp": 50, "cr3": 7},
                        [["enter"], ["run", {"rip": 4}], ["exit", "CPUID"]],
                    ],
                    "expected": (
                        {"rip": 100, "rsp": 200, "cr3": 1},
                        {"rip": 100, "rsp": 200, "cr3": 1},
                        {"rip": 4, "rsp": 50, "cr3": 7},
                        ["CPUID"],
                    ),
                },
                {
                    "args": [
                        {"rip": 100, "rsp": 200, "cr3": 1},
                        {"rip": 0, "rsp": 50, "cr3": 7},
                        [],
                    ],
                    "expected": (
                        {"rip": 100, "rsp": 200, "cr3": 1},
                        {"rip": 100, "rsp": 200, "cr3": 1},
                        {"rip": 0, "rsp": 50, "cr3": 7},
                        [],
                    ),
                },
                {
                    "args": [
                        {"rip": 100, "rsp": 200, "cr3": 1},
                        {"rip": 0, "rsp": 50, "cr3": 7},
                        [
                            ["enter"],
                            ["run", {"rip": 8}],
                            ["exit", "HLT"],
                            ["vmwrite", {"rip": 12}],
                            ["enter"],
                            ["run", {"rsp": 60}],
                            ["exit", "IO"],
                        ],
                    ],
                    "expected": (
                        {"rip": 100, "rsp": 200, "cr3": 1},
                        {"rip": 100, "rsp": 200, "cr3": 1},
                        {"rip": 12, "rsp": 60, "cr3": 7},
                        ["HLT", "IO"],
                    ),
                },
                {
                    "args": [
                        {"rip": 100, "rsp": 200, "cr3": 1},
                        {"rip": 0, "rsp": 50, "cr3": 7},
                        [
                            ["enter"],
                            ["exit", "MSR"],
                            ["monitor", {"rip": 101}],
                            ["enter"],
                            ["run", {"cr3": 9}],
                        ],
                    ],
                    "expected": (
                        {"rip": 0, "rsp": 50, "cr3": 9},
                        {"rip": 101, "rsp": 200, "cr3": 1},
                        {"rip": 0, "rsp": 50, "cr3": 7},
                        ["MSR"],
                    ),
                },
                {
                    "args": [
                        {"rip": 1, "rsp": 2},
                        {"rip": 3, "rsp": 4},
                        [
                            ["enter"],
                            ["run", {"rip": 5}],
                            ["exit", "A"],
                            ["enter"],
                            ["exit", "B"],
                        ],
                    ],
                    "expected": (
                        {"rip": 1, "rsp": 2},
                        {"rip": 1, "rsp": 2},
                        {"rip": 5, "rsp": 4},
                        ["A", "B"],
                    ),
                },
            ],
            "hint": ("Копируйте словари через dict(...), чтобы не менять исходные."),
        },
        {
            "id": "virt-exit-profile",
            "mode": "func",
            "func": "exit_profile",
            "title": "Профиль выходов",
            "statement": (
                "Напишите функцию exit_profile(log, costs): log — список причин выходов из гостя, "
                "costs — словарь «причина → цена одного выхода в тактах». Если причины в costs нет, "
                "цена равна 1500. Верните список кортежей (причина, сколько раз, суммарные такты), "
                "отсортированный по убыванию суммарных тактов, а при равенстве — по названию причины."
            ),
            "starter": "def exit_profile(log, costs):\n    pass\n",
            "tests": [
                {"args": [[], {}], "expected": []},
                {
                    "args": [["CPUID", "CPUID", "HLT"], {"CPUID": 1000, "HLT": 3000}],
                    "expected": [("HLT", 1, 3000), ("CPUID", 2, 2000)],
                },
                {
                    "args": [
                        ["IO", "IO", "IO", "MSR", "MSR"],
                        {"IO": 1000, "MSR": 1500},
                    ],
                    "expected": [("IO", 3, 3000), ("MSR", 2, 3000)],
                },
                {"args": [["EPT"], {}], "expected": [("EPT", 1, 1500)]},
                {
                    "args": [
                        ["A", "B", "A", "C", "B", "A"],
                        {"A": 100, "B": 400, "C": 1000},
                    ],
                    "expected": [("C", 1, 1000), ("B", 2, 800), ("A", 3, 300)],
                },
            ],
            "hint": (
                "Посчитайте выходы словарём, потом отсортируйте с ключом (-такты, причина)."
            ),
        },
        {
            "id": "virt-exit-budget",
            "mode": "func",
            "func": "max_exits",
            "title": "Бюджет выходов",
            "statement": (
                "Напишите функцию max_exits(hz, exit_cost, overhead_percent): hz — частота процессора "
                "в герцах, exit_cost — цена одного выхода в тактах, overhead_percent — какую целую "
                "долю процессорного времени в процентах можно потратить на выходы. Верните целое "
                "число выходов в секунду, не превышающее бюджет (округление вниз; считайте целыми "
                "числами)."
            ),
            "starter": "def max_exits(hz, exit_cost, overhead_percent):\n    pass\n",
            "tests": [
                {"args": [3000000000, 2000, 5], "expected": 75000},
                {"args": [3000000000, 1500, 10], "expected": 200000},
                {"args": [2000000000, 3000, 1], "expected": 6666},
                {"args": [1000, 5000, 50], "expected": 0},
                {"args": [3500000000, 1000, 100], "expected": 3500000},
                {"args": [3000000000, 2000, 0], "expected": 0},
            ],
            "hint": (
                "Бюджет тактов в секунду: hz * процент // 100. Разделите его на цену выхода."
            ),
        },
        {
            "id": "virt-arm-el",
            "mode": "func",
            "func": "target_el",
            "title": "Куда уходит исключение на ARM",
            "statement": (
                "Напишите функцию target_el(instr, el, tsc=False): instr — команда («SVC», «HVC» или "
                "«SMC»), el — текущий уровень исключений (0, 1 или 2), tsc — включён ли перехват SMC "
                "(бит HCR_EL2.TSC). Верните уровень, на который попадёт исключение, или строку "
                '"undef", если команда на этом уровне не определена. SVC уходит на тот же уровень, но '
                "не ниже 1. HVC из EL0 не определена, из EL1 и EL2 уходит на EL2. SMC из EL0 не "
                "определена; из EL1 при tsc уходит на EL2; во всех остальных случаях — на EL3."
            ),
            "starter": "def target_el(instr, el, tsc=False):\n    pass\n",
            "tests": [
                {"args": ["SVC", 0], "expected": 1},
                {"args": ["SVC", 1], "expected": 1},
                {"args": ["SVC", 2], "expected": 2},
                {"args": ["HVC", 0], "expected": "undef"},
                {"args": ["HVC", 1], "expected": 2},
                {"args": ["HVC", 2], "expected": 2},
                {"args": ["SMC", 0], "expected": "undef"},
                {"args": ["SMC", 1], "expected": 3},
                {"args": ["SMC", 1, True], "expected": 2},
                {"args": ["SMC", 2, True], "expected": 3},
            ],
            "hint": ("Разберите три команды отдельными ветками."),
        },
        {
            "id": "virt-riscv-csr",
            "mode": "func",
            "func": "csr_access",
            "title": "Доступ к CSR в RISC-V с расширением H",
            "statement": (
                "Напишите функцию csr_access(mode, csr): mode — режим («M», «HS», «U», «VS», «VU»), "
                "csr — имя регистра («mstatus», «satp», «sstatus», «vsatp», «vsstatus», «hgatp», "
                "«hstatus»). Верните имя регистра, к которому реально получит доступ команда, либо "
                "название исключения. M: любой регистр доступен под своим именем. HS: доступно всё, "
                "кроме mstatus — «illegal-instruction». VS: satp и sstatus подменяются на vsatp и "
                "vsstatus; mstatus — «illegal-instruction»; остальные (vsatp, vsstatus, hgatp, "
                "hstatus) — «virtual-instruction». U: любой регистр — «illegal-instruction». VU: "
                "любой — «virtual-instruction»."
            ),
            "starter": "def csr_access(mode, csr):\n    pass\n",
            "tests": [
                {"args": ["M", "mstatus"], "expected": "mstatus"},
                {"args": ["HS", "hgatp"], "expected": "hgatp"},
                {"args": ["HS", "satp"], "expected": "satp"},
                {"args": ["HS", "mstatus"], "expected": "illegal-instruction"},
                {"args": ["VS", "satp"], "expected": "vssatp"},
                {"args": ["VS", "sstatus"], "expected": "vssstatus"},
                {"args": ["VS", "hgatp"], "expected": "virtual-instruction"},
                {"args": ["VS", "vsatp"], "expected": "virtual-instruction"},
                {"args": ["VS", "mstatus"], "expected": "illegal-instruction"},
                {"args": ["U", "satp"], "expected": "illegal-instruction"},
                {"args": ["VU", "satp"], "expected": "virtual-instruction"},
            ],
            "hint": ("Начните с режимов U, VU и M, затем разберите HS и VS."),
        },
        {
            "id": "virt-vmx-lifecycle",
            "mode": "func",
            "func": "vmx_run",
            "title": "Жизненный цикл VMX",
            "statement": (
                'Напишите функцию vmx_run(ops): ops — список операций над VMX вида ["VMXON"], '
                '["VMPTRLD", id], ["VMLAUNCH"], ["VMRESUME"], ["VMCLEAR", id], ["VMXOFF"]. Для каждой '
                'верните "ok" или "fail". До VMXON и после VMXOFF любая операция, кроме VMXON, — '
                "fail; повторный VMXON — fail. VMPTRLD делает VMCS с данным id текущей. VMLAUNCH — "
                "ok, если есть текущая VMCS и она ещё не запускалась (после этого она «запущена»). "
                "VMRESUME — ok, если есть текущая VMCS и она запущена. VMCLEAR сбрасывает состояние "
                "«запущена» у VMCS с данным id, а если она текущая — снимает «текущую». VMXOFF "
                "выключает режим и снимает текущую. Состояние «запущена» хранится у VMCS и переживает "
                "VMPTRLD другой VMCS и обратно."
            ),
            "starter": "def vmx_run(ops):\n    pass\n",
            "tests": [
                {"args": [[]], "expected": []},
                {"args": [[["VMLAUNCH"]]], "expected": ["fail"]},
                {
                    "args": [
                        [
                            ["VMXON"],
                            ["VMPTRLD", 1],
                            ["VMLAUNCH"],
                            ["VMRESUME"],
                            ["VMRESUME"],
                        ]
                    ],
                    "expected": ["ok", "ok", "ok", "ok", "ok"],
                },
                {"args": [[["VMXON"], ["VMLAUNCH"]]], "expected": ["ok", "fail"]},
                {
                    "args": [[["VMXON"], ["VMPTRLD", 1], ["VMRESUME"]]],
                    "expected": ["ok", "ok", "fail"],
                },
                {"args": [[["VMXON"], ["VMXON"]]], "expected": ["ok", "fail"]},
                {
                    "args": [[["VMXON"], ["VMPTRLD", 1], ["VMLAUNCH"], ["VMLAUNCH"]]],
                    "expected": ["ok", "ok", "ok", "fail"],
                },
                {
                    "args": [
                        [
                            ["VMXON"],
                            ["VMPTRLD", 1],
                            ["VMLAUNCH"],
                            ["VMCLEAR", 1],
                            ["VMRESUME"],
                        ]
                    ],
                    "expected": ["ok", "ok", "ok", "ok", "fail"],
                },
                {
                    "args": [
                        [
                            ["VMXON"],
                            ["VMPTRLD", 1],
                            ["VMLAUNCH"],
                            ["VMPTRLD", 2],
                            ["VMLAUNCH"],
                            ["VMPTRLD", 1],
                            ["VMRESUME"],
                        ]
                    ],
                    "expected": ["ok", "ok", "ok", "ok", "ok", "ok", "ok"],
                },
                {
                    "args": [[["VMXON"], ["VMXOFF"], ["VMPTRLD", 1]]],
                    "expected": ["ok", "ok", "fail"],
                },
                {
                    "args": [
                        [
                            ["VMXON"],
                            ["VMPTRLD", 1],
                            ["VMLAUNCH"],
                            ["VMCLEAR", 1],
                            ["VMPTRLD", 1],
                            ["VMLAUNCH"],
                        ]
                    ],
                    "expected": ["ok", "ok", "ok", "ok", "ok", "ok"],
                },
            ],
            "hint": ("Храните on, id текущей VMCS и словарь «id → запущена ли»."),
        },
        {
            "id": "virt-kvm-run",
            "mode": "func",
            "func": "kvm_run",
            "title": "Цикл KVM_RUN",
            "statement": (
                "Напишите функцию kvm_run(exits): exits — список причин выходов гостя, по порядку. "
                "Ядро Linux обрабатывает само: EXTERNAL_INTERRUPT, HLT, CPUID, EPT_VIOLATION, MSR. "
                "Всё остальное (IO, MMIO, SHUTDOWN и неизвестные причины) ядро возвращает "
                "пользовательскому процессу — вызов KVM_RUN завершается. После SHUTDOWN гость "
                "останавливается, дальнейшие выходы не рассматриваются. Верните кортеж (сколько "
                "выходов обработало ядро, сколько вернулось в пользовательский процесс)."
            ),
            "starter": "def kvm_run(exits):\n    pass\n",
            "tests": [
                {"args": [[]], "expected": (0, 0)},
                {"args": [["HLT", "EXTERNAL_INTERRUPT", "CPUID"]], "expected": (3, 0)},
                {"args": [["IO", "MMIO"]], "expected": (0, 2)},
                {"args": [["EPT_VIOLATION", "MMIO", "MSR", "IO"]], "expected": (2, 2)},
                {"args": [["HLT", "SHUTDOWN", "IO"]], "expected": (1, 1)},
                {"args": [["XYZ"]], "expected": (0, 1)},
                {"args": [["SHUTDOWN"]], "expected": (0, 1)},
            ],
            "hint": ("Идите по списку и остановитесь после первого SHUTDOWN."),
        },
    ],
}
