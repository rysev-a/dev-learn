"""Задачи книги «Виртуализация»: глава 13 — MicroVM и облако: Firecracker, Xen, ESXi и libvirt."""

TASKS: dict[int, list[dict]] = {
    13: [
        {
            "id": "virt-snap-restore",
            "mode": "func",
            "func": "snapshot_restore",
            "title": "Восстановление из снимка",
            "statement": (
                "Напишите функцию snapshot_restore(touched, base_us, fault_us): микро-машина "
                "восстановлена из снимка, память отображена лениво. touched — страницы, к которым "
                "обращался гость, по порядку (с повторами), base_us — фиксированное время "
                "восстановления, fault_us — цена подгрузки одной страницы при первом обращении. "
                "Верните кортеж (число подгрузок, суммарное время в микросекундах)."
            ),
            "starter": "def snapshot_restore(touched, base_us, fault_us):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 1, 3, 2], 500, 20], "expected": (3, 560)},
                {"args": [[], 500, 20], "expected": (0, 500)},
                {"args": [[7, 7, 7], 1000, 50], "expected": (1, 1050)},
                {"args": [[0, 1, 2, 3], 0, 10], "expected": (4, 40)},
                {"args": [[5], 300, 0], "expected": (1, 300)},
                {"args": [[9, 8, 9, 8, 7], 250, 25], "expected": (3, 325)},
            ],
            "hint": ("Подгрузка — один раз на каждую различную страницу."),
        },
        {
            "id": "virt-device-surface",
            "mode": "func",
            "func": "device_surface",
            "title": "Поверхность атаки по устройствам",
            "statement": (
                "Напишите функцию device_surface(devices): devices — список имён устройств машины. "
                "Вес устройства в условных единицах поверхности атаки: serial — 1, balloon — 2, vsock "
                "— 3, virtio-block — 5, virtio-net — 6, usb — 25, vga — 20, pci-nic — 30; любое "
                "другое имя — 10. Верните суммарный вес."
            ),
            "starter": "def device_surface(devices):\n    pass\n",
            "tests": [
                {
                    "args": [["virtio-net", "virtio-block", "vsock", "serial"]],
                    "expected": 15,
                },
                {"args": [[]], "expected": 0},
                {"args": [["usb", "vga", "pci-nic", "serial"]], "expected": 76},
                {"args": [["floppy"]], "expected": 10},
                {"args": [["balloon", "balloon", "mystery"]], "expected": 14},
                {"args": [["virtio-net", "pci-nic"]], "expected": 36},
            ],
            "hint": (
                "Заведите словарь весов и используйте get со значением по умолчанию 10."
            ),
        },
        {
            "id": "virt-jailer",
            "mode": "func",
            "func": "jailer_steps",
            "title": "Слои защиты монитора",
            "statement": (
                'Напишите функцию jailer_steps(cfg): cfg — словарь с логическими полями "cgroup", '
                '"namespaces", "chroot", "drop_privileges", "seccomp". Джейлер применяет включённые '
                "меры в фиксированном порядке: cgroup, namespaces, chroot, drop-privileges, seccomp. "
                "Верните кортеж (список применённых мер по порядку, оценка надёжности — число мер, а "
                "если seccomp выключен, то на 1 меньше)."
            ),
            "starter": "def jailer_steps(cfg):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {
                            "cgroup": True,
                            "namespaces": True,
                            "chroot": True,
                            "drop_privileges": True,
                            "seccomp": True,
                        }
                    ],
                    "expected": (
                        [
                            "cgroup",
                            "namespaces",
                            "chroot",
                            "drop-privileges",
                            "seccomp",
                        ],
                        5,
                    ),
                },
                {
                    "args": [
                        {
                            "cgroup": False,
                            "namespaces": False,
                            "chroot": False,
                            "drop_privileges": False,
                            "seccomp": False,
                        }
                    ],
                    "expected": ([], 0),
                },
                {
                    "args": [
                        {
                            "cgroup": True,
                            "namespaces": True,
                            "chroot": True,
                            "drop_privileges": True,
                            "seccomp": False,
                        }
                    ],
                    "expected": (
                        ["cgroup", "namespaces", "chroot", "drop-privileges"],
                        3,
                    ),
                },
                {"args": [{"seccomp": True}], "expected": (["seccomp"], 1)},
                {
                    "args": [{"chroot": True, "seccomp": True}],
                    "expected": (["chroot", "seccomp"], 2),
                },
                {"args": [{"cgroup": True}], "expected": (["cgroup"], 0)},
            ],
            "hint": (
                "Пройдите по именам в нужном порядке и оставьте те, что включены."
            ),
        },
        {
            "id": "virt-cold-start",
            "mode": "func",
            "func": "cold_starts",
            "title": "Холодные старты функций",
            "statement": (
                "Напишите функцию cold_starts(calls, ttl): calls — вызовы функции по порядку [время "
                "начала, длительность] (в секундах), ttl — сколько секунд микро-машина живёт после "
                "завершения вызова. Машина одна. Вызов «тёплый», если машина уже существует и с конца "
                "предыдущего вызова прошло не больше ttl секунд (время начала минус конец "
                "предыдущего); иначе «холодный». Верните кортеж (число холодных стартов, список "
                '"cold"/"warm" по вызовам).'
            ),
            "starter": "def cold_starts(calls, ttl):\n    pass\n",
            "tests": [
                {
                    "args": [[[0, 1], [5, 1], [100, 1]], 10],
                    "expected": (2, ["cold", "warm", "cold"]),
                },
                {"args": [[], 10], "expected": (0, [])},
                {"args": [[[0, 5], [5, 1]], 0], "expected": (1, ["cold", "warm"])},
                {"args": [[[0, 1], [11, 1]], 10], "expected": (1, ["cold", "warm"])},
                {"args": [[[0, 1], [12, 1]], 10], "expected": (2, ["cold", "cold"])},
                {
                    "args": [[[0, 2], [3, 2], [8, 2], [30, 1]], 5],
                    "expected": (2, ["cold", "warm", "warm", "cold"]),
                },
            ],
            "hint": (
                "Запоминайте конец предыдущего вызова; для первого вызова машины ещё нет."
            ),
        },
        {
            "id": "virt-spread-pods",
            "mode": "func",
            "func": "spread_pods",
            "title": "Распределение подов по серверам",
            "statement": (
                "Напишите функцию spread_pods(pods, nodes): pods — список [имя, ядра, память], nodes "
                "— список [имя, свободных ядер, свободной памяти]. Каждый под по порядку ставят на "
                "тот из подходящих узлов (хватает и ядер, и памяти), где сейчас больше всего "
                "свободных ядер; при равенстве — на узел с меньшим именем. Ресурсы узла уменьшаются. "
                "Верните словарь «под → узел или None, если не поместился»."
            ),
            "starter": "def spread_pods(pods, nodes):\n    pass\n",
            "tests": [
                {
                    "args": [
                        [["a", 2, 4], ["b", 2, 4], ["c", 2, 4]],
                        [["n1", 4, 16], ["n2", 4, 16]],
                    ],
                    "expected": {"a": "n1", "b": "n2", "c": "n1"},
                },
                {"args": [[["a", 8, 1]], [["n1", 4, 16]]], "expected": {"a": None}},
                {"args": [[], [["n1", 1, 1]]], "expected": {}},
                {
                    "args": [
                        [["a", 1, 1], ["b", 1, 1], ["c", 1, 1]],
                        [["n2", 2, 8], ["n1", 2, 8]],
                    ],
                    "expected": {"a": "n1", "b": "n2", "c": "n1"},
                },
                {
                    "args": [
                        [["a", 2, 20], ["b", 1, 1]],
                        [["n1", 4, 16], ["n2", 2, 32]],
                    ],
                    "expected": {"a": "n2", "b": "n1"},
                },
            ],
            "hint": (
                "Из подходящих узлов выберите максимум по (свободные ядра, -имя) — удобно "
                "использовать сортировку."
            ),
        },
        {
            "id": "virt-overlay-mtu",
            "mode": "func",
            "func": "overlay_mtu",
            "title": "MTU внутри туннеля",
            "statement": (
                "Напишите функцию overlay_mtu(outer_mtu, kind, opts=0): outer_mtu — MTU физической "
                'сети, kind — тип туннеля. Накладные расходы: "vxlan" — 50 байт, "geneve" — 50 байт '
                'плюс opts байт опций, "gre" — 24, "ipip" — 20. Верните MTU, который можно выдать '
                "гостю: outer_mtu минус накладные расходы."
            ),
            "starter": "def overlay_mtu(outer_mtu, kind, opts=0):\n    pass\n",
            "tests": [
                {"args": [1500, "vxlan"], "expected": 1450},
                {"args": [9000, "vxlan"], "expected": 8950},
                {"args": [1500, "geneve", 8], "expected": 1442},
                {"args": [1500, "gre"], "expected": 1476},
                {"args": [1500, "ipip"], "expected": 1480},
                {"args": [1600, "geneve"], "expected": 1550},
            ],
            "hint": ("Заведите таблицу накладных расходов; у geneve добавьте opts."),
        },
        {
            "id": "virt-pick-virt",
            "mode": "func",
            "func": "pick_virt",
            "title": "Выбор платформы виртуализации",
            "statement": (
                'Напишите функцию pick_virt(req): req — словарь с полями "min_boot_ms" (допустимое '
                'время старта), "open_source" (нужен открытый код) и "live_migration" (нужна живая '
                "миграция). Правила по порядку: если допустимое время старта не больше 300 мс — "
                '"microvm"; иначе если нужен открытый код и живая миграция — "kvm"; иначе если нужен '
                'открытый код — "xen"; иначе — "esxi".'
            ),
            "starter": "def pick_virt(req):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {
                            "min_boot_ms": 100,
                            "open_source": False,
                            "live_migration": False,
                        }
                    ],
                    "expected": "microvm",
                },
                {
                    "args": [
                        {
                            "min_boot_ms": 300,
                            "open_source": True,
                            "live_migration": True,
                        }
                    ],
                    "expected": "microvm",
                },
                {
                    "args": [
                        {
                            "min_boot_ms": 5000,
                            "open_source": True,
                            "live_migration": True,
                        }
                    ],
                    "expected": "kvm",
                },
                {
                    "args": [
                        {
                            "min_boot_ms": 5000,
                            "open_source": True,
                            "live_migration": False,
                        }
                    ],
                    "expected": "xen",
                },
                {
                    "args": [
                        {
                            "min_boot_ms": 5000,
                            "open_source": False,
                            "live_migration": True,
                        }
                    ],
                    "expected": "esxi",
                },
                {
                    "args": [
                        {
                            "min_boot_ms": 301,
                            "open_source": False,
                            "live_migration": False,
                        }
                    ],
                    "expected": "esxi",
                },
            ],
            "hint": ("Проверяйте правила в указанном порядке."),
        },
        {
            "id": "virt-microvm-density",
            "mode": "func",
            "func": "microvm_density",
            "title": "Плотность микро-машин",
            "statement": (
                "Напишите функцию microvm_density(host_mb, vm_mb, overhead_mb, reserve_mb): сколько "
                "микро-машин поместится на хосте, если каждая занимает vm_mb плюс overhead_mb "
                "накладных расходов монитора, а reserve_mb нужно хозяину. Верните целое число (не "
                "меньше нуля)."
            ),
            "starter": "def microvm_density(host_mb, vm_mb, overhead_mb, reserve_mb):\n    pass\n",
            "tests": [
                {"args": [65536, 128, 5, 4096], "expected": 461},
                {"args": [65536, 128, 300, 4096], "expected": 143},
                {"args": [1024, 128, 5, 2048], "expected": 0},
                {"args": [8192, 64, 5, 0], "expected": 118},
                {"args": [10000, 100, 0, 0], "expected": 100},
                {"args": [500, 128, 5, 100], "expected": 3},
            ],
            "hint": ("(host - reserve) // (vm + overhead), не меньше нуля."),
        },
    ],
}
