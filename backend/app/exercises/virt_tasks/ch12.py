"""Задачи книги «Виртуализация»: глава 12 — Контейнеры против виртуальных машин: namespaces, cgroups, gVisor и Kata."""

TASKS: dict[int, list[dict]] = {
    12: [
        {
            "id": "virt-pid-ns",
            "mode": "func",
            "func": "pid_namespaces",
            "title": "Нумерация в пространстве процессов",
            "statement": (
                "Напишите функцию pid_namespaces(procs): procs — список процессов [номер на хозяине, "
                'пространство]. Пространство "host" — обычное: номер внутри равен номеру на хозяине. '
                "В остальных пространствах процессы нумеруются заново с 1 в порядке возрастания "
                "номеров на хозяине. Верните словарь «номер на хозяине (строкой) → номер внутри "
                "пространства»."
            ),
            "starter": "def pid_namespaces(procs):\n    pass\n",
            "tests": [
                {
                    "args": [[[100, "c1"], [101, "c1"], [200, "c2"]]],
                    "expected": {"100": 1, "101": 2, "200": 1},
                },
                {"args": [[[5, "host"], [6, "c1"]]], "expected": {"5": 5, "6": 1}},
                {"args": [[]], "expected": {}},
                {
                    "args": [[[300, "c1"], [100, "c1"], [200, "c1"]]],
                    "expected": {"100": 1, "200": 2, "300": 3},
                },
                {
                    "args": [[[7, "a"], [8, "b"], [9, "a"], [10, "b"]]],
                    "expected": {"7": 1, "8": 1, "9": 2, "10": 2},
                },
            ],
            "hint": (
                "Отсортируйте процессы и ведите счётчик для каждого пространства."
            ),
        },
        {
            "id": "virt-cgroup-limit",
            "mode": "func",
            "func": "effective_limit",
            "title": "Лимит с учётом иерархии",
            "statement": (
                "В группах управления второй версии лимит родителя ограничивает потомков. Напишите "
                "функцию effective_limit(parents, limits, node): parents — словарь «группа → "
                "родитель» (у корня записи нет), limits — словарь «группа → лимит» (есть не у всех), "
                "node — группа. Верните наименьший лимит среди самой группы и всех её предков, а если "
                "лимитов нет нигде — None."
            ),
            "starter": "def effective_limit(parents, limits, node):\n    pass\n",
            "tests": [
                {
                    "args": [{"a": "root", "b": "a"}, {"root": 8, "a": 4}, "b"],
                    "expected": 4,
                },
                {
                    "args": [{"a": "root", "b": "a"}, {"b": 2, "a": 4}, "b"],
                    "expected": 2,
                },
                {"args": [{"a": "root"}, {}, "a"], "expected": None},
                {"args": [{"a": "root", "b": "a"}, {"root": 8}, "root"], "expected": 8},
                {
                    "args": [
                        {"a": "root", "b": "a", "c": "b"},
                        {"root": 10, "b": 3, "c": 5},
                        "c",
                    ],
                    "expected": 3,
                },
                {"args": [{}, {"x": 1}, "x"], "expected": 1},
            ],
            "hint": (
                "Поднимайтесь вверх по parents до корня и собирайте найденные лимиты."
            ),
        },
        {
            "id": "virt-overlay-run",
            "mode": "func",
            "func": "overlay_run",
            "title": "Файловая система overlayfs",
            "statement": (
                "Напишите функцию overlay_run(lowers, ops): lowers — нижние слои образа от верхнего к "
                "нижнему (словари «путь → содержимое»). Сверху лежит пустой слой контейнера. "
                'Операции: ["write", путь, данные] (запись в верхний слой), ["delete", путь] (если '
                "путь есть в нижних слоях, в верхнем ставится метка whiteout, иначе путь просто "
                'убирается из верхнего слоя) и ["read", путь] (сначала верхний слой; метка whiteout '
                "скрывает файл; затем нижние слои сверху вниз; нет нигде — None). Не меняйте входные "
                "данные. Верните список результатов всех чтений."
            ),
            "starter": "def overlay_run(lowers, ops):\n    pass\n",
            "tests": [
                {
                    "args": [
                        [{"/a": "1"}, {"/a": "0", "/b": "2"}],
                        [["read", "/a"], ["read", "/b"], ["read", "/c"]],
                    ],
                    "expected": ["1", "2", None],
                },
                {
                    "args": [[{"/a": "1"}], [["write", "/a", "new"], ["read", "/a"]]],
                    "expected": ["new"],
                },
                {
                    "args": [[{"/a": "1"}], [["delete", "/a"], ["read", "/a"]]],
                    "expected": [None],
                },
                {
                    "args": [
                        [{"/a": "1"}],
                        [["delete", "/a"], ["write", "/a", "again"], ["read", "/a"]],
                    ],
                    "expected": ["again"],
                },
                {
                    "args": [
                        [],
                        [["write", "/x", "1"], ["delete", "/x"], ["read", "/x"]],
                    ],
                    "expected": [None],
                },
                {
                    "args": [
                        [{"/a": "1"}, {"/a": "0"}],
                        [
                            ["delete", "/a"],
                            ["read", "/a"],
                            ["delete", "/zzz"],
                            ["read", "/zzz"],
                        ],
                    ],
                    "expected": [None, None],
                },
            ],
            "hint": ("В верхнем слое храните специальное значение-метку для whiteout."),
        },
        {
            "id": "virt-seccomp",
            "mode": "func",
            "func": "seccomp_run",
            "title": "Фильтр системных вызовов",
            "statement": (
                "Напишите функцию seccomp_run(allowed, trace, action): allowed — список разрешённых "
                "системных вызовов, trace — вызовы процесса по порядку, action — действие для "
                'запрещённых: "errno" (вызов возвращает ошибку, процесс продолжает) или "kill" '
                "(процесс убивается на первом запрещённом вызове). Верните кортеж (сколько вызовов "
                "выполнено, список запрещённых вызовов по порядку — при kill в нём не больше одного)."
            ),
            "starter": "def seccomp_run(allowed, trace, action):\n    pass\n",
            "tests": [
                {
                    "args": [
                        ["read", "write", "exit"],
                        ["read", "write", "ptrace", "exit"],
                        "errno",
                    ],
                    "expected": (3, ["ptrace"]),
                },
                {
                    "args": [
                        ["read", "write", "exit"],
                        ["read", "write", "ptrace", "exit"],
                        "kill",
                    ],
                    "expected": (2, ["ptrace"]),
                },
                {"args": [["read"], [], "kill"], "expected": (0, [])},
                {
                    "args": [["read"], ["mount", "mount", "read"], "errno"],
                    "expected": (1, ["mount", "mount"]),
                },
                {
                    "args": [["read"], ["mount", "mount", "read"], "kill"],
                    "expected": (0, ["mount"]),
                },
                {"args": [[], ["read"], "errno"], "expected": (0, ["read"])},
            ],
            "hint": ("Идите по trace; при kill остановитесь на первом запрещённом."),
        },
        {
            "id": "virt-fit-instances",
            "mode": "func",
            "func": "fit_instances",
            "title": "Плотность размещения",
            "statement": (
                "Напишите функцию fit_instances(host_mb, reserve_mb, workload_mb, overhead_mb): "
                "сколько одинаковых экземпляров поместится на хосте. Каждый занимает workload_mb на "
                "нагрузку и overhead_mb накладных расходов (у контейнера они малы, у виртуальной "
                "машины включают ядро гостя), на хозяина оставляют reserve_mb. Верните целое число "
                "экземпляров (не меньше нуля)."
            ),
            "starter": "def fit_instances(host_mb, reserve_mb, workload_mb, overhead_mb):\n    pass\n",
            "tests": [
                {"args": [65536, 4096, 512, 5], "expected": 118},
                {"args": [65536, 4096, 512, 300], "expected": 75},
                {"args": [1024, 2048, 100, 10], "expected": 0},
                {"args": [8192, 0, 1024, 0], "expected": 8},
                {"args": [1000, 100, 300, 50], "expected": 2},
                {"args": [4096, 4096, 1, 1], "expected": 0},
            ],
            "hint": ("(host - reserve) // (workload + overhead), но не меньше 0."),
        },
        {
            "id": "virt-choose-runtime",
            "mode": "func",
            "func": "choose_runtime",
            "title": "Выбор среды запуска",
            "statement": (
                'Напишите функцию choose_runtime(req): req — словарь с логическими полями "trusted" '
                '(свой доверенный код), "needs_other_os" (нужна не Linux-система), "kernel_modules" '
                '(нужны свои модули ядра) и "multi_tenant" (на сервере чужие арендаторы). Правила по '
                'порядку: нужна другая ОС или модули ядра — "vm"; код доверенный — "container"; чужие '
                'арендаторы — "kata"; иначе — "gvisor".'
            ),
            "starter": "def choose_runtime(req):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {
                            "trusted": True,
                            "needs_other_os": False,
                            "kernel_modules": False,
                            "multi_tenant": False,
                        }
                    ],
                    "expected": "container",
                },
                {
                    "args": [
                        {
                            "trusted": True,
                            "needs_other_os": True,
                            "kernel_modules": False,
                            "multi_tenant": False,
                        }
                    ],
                    "expected": "vm",
                },
                {
                    "args": [
                        {
                            "trusted": False,
                            "needs_other_os": False,
                            "kernel_modules": False,
                            "multi_tenant": True,
                        }
                    ],
                    "expected": "kata",
                },
                {
                    "args": [
                        {
                            "trusted": False,
                            "needs_other_os": False,
                            "kernel_modules": False,
                            "multi_tenant": False,
                        }
                    ],
                    "expected": "gvisor",
                },
                {
                    "args": [
                        {
                            "trusted": False,
                            "needs_other_os": False,
                            "kernel_modules": True,
                            "multi_tenant": True,
                        }
                    ],
                    "expected": "vm",
                },
            ],
            "hint": ("Проверяйте условия строго в указанном порядке."),
        },
        {
            "id": "virt-userns",
            "mode": "func",
            "func": "map_uid",
            "title": "Отображение пользователей",
            "statement": (
                "Напишите функцию map_uid(uid_map, inner): uid_map — таблица пространства "
                "пользователей, список строк [начало_внутри, начало_снаружи, сколько], inner — номер "
                "пользователя внутри контейнера. Верните соответствующий номер на хозяине: если inner "
                "попадает в диапазон [начало_внутри, начало_внутри + сколько), результат равен "
                "начало_снаружи + inner - начало_внутри. Если номер не отображён ни в одну строку, "
                "верните None."
            ),
            "starter": "def map_uid(uid_map, inner):\n    pass\n",
            "tests": [
                {"args": [[[0, 100000, 65536]], 0], "expected": 100000},
                {"args": [[[0, 100000, 65536]], 1000], "expected": 101000},
                {"args": [[[0, 100000, 65536]], 65536], "expected": None},
                {"args": [[[0, 1000, 1], [1, 100000, 65535]], 0], "expected": 1000},
                {"args": [[[0, 1000, 1], [1, 100000, 65535]], 5], "expected": 100004},
                {"args": [[], 0], "expected": None},
                {"args": [[[10, 500, 5]], 9], "expected": None},
            ],
            "hint": (
                "Просмотрите строки таблицы и найдите ту, чей диапазон содержит inner."
            ),
        },
        {
            "id": "virt-sentry",
            "mode": "func",
            "func": "sentry_split",
            "title": "Поверхность атаки gVisor",
            "statement": (
                "Напишите функцию sentry_split(calls, host_set): calls — системные вызовы приложения, "
                "host_set — список вызовов, которые Sentry вынужден передавать настоящему ядру "
                "хозяина; остальные он обрабатывает сам. Верните кортеж (сколько вызовов обработал "
                "Sentry, сколько ушло хозяину, доля обработанных Sentry в целых процентах — "
                "округление вниз; для пустого списка — 100)."
            ),
            "starter": "def sentry_split(calls, host_set):\n    pass\n",
            "tests": [
                {
                    "args": [["read", "write", "open", "futex"], ["read", "open"]],
                    "expected": (2, 2, 50),
                },
                {"args": [[], ["read"]], "expected": (0, 0, 100)},
                {"args": [["futex", "futex", "futex"], []], "expected": (3, 0, 100)},
                {"args": [["read", "read"], ["read"]], "expected": (0, 2, 0)},
                {"args": [["a", "b", "c"], ["a"]], "expected": (2, 1, 66)},
                {
                    "args": [["a", "b", "c", "d", "e", "f", "g"], ["a"]],
                    "expected": (6, 1, 85),
                },
            ],
            "hint": ("Посчитайте вызовы из host_set и вычтите их из общего числа."),
        },
    ],
}
