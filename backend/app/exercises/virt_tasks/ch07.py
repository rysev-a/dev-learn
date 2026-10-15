"""Задачи книги «Виртуализация»: глава 7 — Проброс устройств: IOMMU, VFIO и SR-IOV."""

TASKS: dict[int, list[dict]] = {
    7: [
        {
            "id": "virt-iommu-check",
            "mode": "func",
            "func": "iommu_check",
            "title": "Проверка DMA в IOMMU",
            "statement": (
                "Напишите функцию iommu_check(domains, bdf, iova, write): domains — словарь "
                "«идентификатор устройства → список отображений» [начало_iova, размер, начало_hpa, "
                'права], права — "r" или "rw". Обращение устройства bdf по адресу iova (write — '
                "запись или чтение). Верните хозяйский адрес (начало_hpa + iova - начало_iova); "
                '"fault:no-domain", если у устройства нет домена; "fault:unmapped", если iova не '
                'попадает ни в одно отображение; "fault:write", если отображение только для чтения, а '
                "обращение — запись."
            ),
            "starter": "def iommu_check(domains, bdf, iova, write):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {"03:00.0": [[4096, 8192, 1048576, "rw"]]},
                        "03:00.0",
                        4100,
                        True,
                    ],
                    "expected": 1048580,
                },
                {
                    "args": [
                        {"03:00.0": [[4096, 8192, 1048576, "rw"]]},
                        "03:00.0",
                        12288,
                        False,
                    ],
                    "expected": "fault:unmapped",
                },
                {
                    "args": [{"03:00.0": [[0, 4096, 65536, "r"]]}, "03:00.0", 10, True],
                    "expected": "fault:write",
                },
                {
                    "args": [
                        {"03:00.0": [[0, 4096, 65536, "r"]]},
                        "03:00.0",
                        10,
                        False,
                    ],
                    "expected": 65546,
                },
                {
                    "args": [
                        {"03:00.0": [[0, 4096, 65536, "r"]]},
                        "04:00.0",
                        10,
                        False,
                    ],
                    "expected": "fault:no-domain",
                },
                {"args": [{}, "03:00.0", 0, False], "expected": "fault:no-domain"},
                {
                    "args": [
                        {"03:00.0": [[0, 4096, 0, "rw"], [8192, 4096, 40960, "rw"]]},
                        "03:00.0",
                        9000,
                        True,
                    ],
                    "expected": 41768,
                },
            ],
            "hint": (
                "Отображение покрывает iova от начала до начала + размер, не включая конец."
            ),
        },
        {
            "id": "virt-iommu-groups",
            "mode": "func",
            "func": "iommu_groups",
            "title": "Группы IOMMU",
            "statement": (
                "Напишите функцию iommu_groups(devices, acs): devices — список [идентификатор "
                "устройства, мост, к которому оно подключено], acs — список мостов, у которых "
                "включена изоляция (ACS). Устройства под одним мостом без ACS IOMMU различить не "
                "может, и они образуют одну группу. Каждое устройство под мостом с ACS образует свою "
                "группу. Верните список групп (каждая — отсортированный список идентификаторов), "
                "отсортированный по первому элементу группы."
            ),
            "starter": "def iommu_groups(devices, acs):\n    pass\n",
            "tests": [
                {
                    "args": [
                        [["03:00.0", "br1"], ["03:00.1", "br1"], ["04:00.0", "br2"]],
                        [],
                    ],
                    "expected": [["03:00.0", "03:00.1"], ["04:00.0"]],
                },
                {
                    "args": [
                        [["03:00.0", "br1"], ["03:00.1", "br1"], ["04:00.0", "br2"]],
                        ["br1"],
                    ],
                    "expected": [["03:00.0"], ["03:00.1"], ["04:00.0"]],
                },
                {"args": [[], []], "expected": []},
                {"args": [[["05:00.0", "br3"]], []], "expected": [["05:00.0"]]},
                {
                    "args": [
                        [["06:00.2", "b"], ["06:00.0", "b"], ["06:00.1", "b"]],
                        [],
                    ],
                    "expected": [["06:00.0", "06:00.1", "06:00.2"]],
                },
                {
                    "args": [[["a", "x"], ["b", "x"], ["c", "y"], ["d", "y"]], ["y"]],
                    "expected": [["a", "b"], ["c"], ["d"]],
                },
            ],
            "hint": (
                "Для моста без ACS собирайте устройства в общий список, для моста с ACS — по одному."
            ),
        },
        {
            "id": "virt-vfio-ready",
            "mode": "func",
            "func": "vfio_ready",
            "title": "Готовность групп к пробросу",
            "statement": (
                "Напишите функцию vfio_ready(groups, drivers): groups — список групп IOMMU (каждая — "
                "список идентификаторов устройств), drivers — словарь «устройство → имя драйвера или "
                'None». Устройства с драйвером "pcieport" (мосты) не учитываются. Группа готова к '
                "пробросу, если после этого в ней остался хотя бы один учитываемый, и у всех "
                'учитываемых драйвер "vfio-pci". Верните отсортированный список номеров готовых групп '
                "(с нуля)."
            ),
            "starter": "def vfio_ready(groups, drivers):\n    pass\n",
            "tests": [
                {
                    "args": [
                        [["a", "b"], ["c"]],
                        {"a": "vfio-pci", "b": "vfio-pci", "c": "nvme"},
                    ],
                    "expected": [0],
                },
                {
                    "args": [[["a", "b"]], {"a": "vfio-pci", "b": "nvme"}],
                    "expected": [],
                },
                {
                    "args": [[["a", "br"]], {"a": "vfio-pci", "br": "pcieport"}],
                    "expected": [0],
                },
                {"args": [[["br"]], {"br": "pcieport"}], "expected": []},
                {"args": [[], {}], "expected": []},
                {
                    "args": [[["a"], ["b"]], {"a": None, "b": "vfio-pci"}],
                    "expected": [1],
                },
                {
                    "args": [
                        [["x", "y"], ["z"]],
                        {"x": "vfio-pci", "y": "vfio-pci", "z": "vfio-pci"},
                    ],
                    "expected": [0, 1],
                },
            ],
            "hint": (
                "Отфильтруйте мосты и проверьте, что все оставшиеся привязаны к vfio-pci."
            ),
        },
        {
            "id": "virt-vf-assign",
            "mode": "func",
            "func": "assign_vfs",
            "title": "Раздача виртуальных функций",
            "statement": (
                "Напишите функцию assign_vfs(total_vfs, vms): у карты total_vfs виртуальных функций с "
                "номерами от 1. vms — список [имя ВМ, сколько функций нужно]. Выдавайте машинам "
                "функции подряд по порядку списка, но каждой — всё нужное сразу или ничего: если "
                "свободных функций меньше, чем нужно, машина получает None, а следующие машины могут "
                "получить оставшиеся. Верните словарь «имя → список номеров функций или None»."
            ),
            "starter": "def assign_vfs(total_vfs, vms):\n    pass\n",
            "tests": [
                {
                    "args": [4, [["a", 2], ["b", 2]]],
                    "expected": {"a": [1, 2], "b": [3, 4]},
                },
                {
                    "args": [4, [["a", 3], ["b", 2], ["c", 1]]],
                    "expected": {"a": [1, 2, 3], "b": None, "c": [4]},
                },
                {"args": [0, [["a", 1]]], "expected": {"a": None}},
                {"args": [8, []], "expected": {}},
                {
                    "args": [3, [["a", 0], ["b", 3]]],
                    "expected": {"a": [], "b": [1, 2, 3]},
                },
                {
                    "args": [5, [["x", 2], ["y", 4], ["z", 3]]],
                    "expected": {"x": [1, 2], "y": None, "z": [3, 4, 5]},
                },
            ],
            "hint": ("Храните номер следующей свободной функции."),
        },
        {
            "id": "virt-irq-exits",
            "mode": "func",
            "func": "irq_exits",
            "title": "Доставка прерываний гостю",
            "statement": (
                'Напишите функцию irq_exits(events, posted): events — список событий "irq" (пришло '
                'прерывание гостю), "halt" (виртуальный процессор уснул) и "run" (проснулся и '
                "работает). Вначале процессор работает. Прерывание работающему процессору при posted "
                "(отправленные прерывания) доставляется без выхода, а без posted вызывает один выход. "
                "Прерывание спящему процессору всегда вызывает один выход (его нужно разбудить), "
                "после чего процессор работает. Верните число выходов."
            ),
            "starter": "def irq_exits(events, posted):\n    pass\n",
            "tests": [
                {"args": [["irq", "irq", "irq"], True], "expected": 0},
                {"args": [["irq", "irq", "irq"], False], "expected": 3},
                {"args": [["halt", "irq", "irq"], True], "expected": 1},
                {"args": [["halt", "irq", "halt", "irq"], True], "expected": 2},
                {"args": [[], False], "expected": 0},
                {"args": [["halt", "run", "irq"], True], "expected": 0},
                {"args": [["halt", "run", "irq"], False], "expected": 1},
            ],
            "hint": ("Следите за состоянием процессора: работает или спит."),
        },
        {
            "id": "virt-pinned",
            "mode": "func",
            "func": "free_for_overcommit",
            "title": "Закреплённая память",
            "statement": (
                "Напишите функцию free_for_overcommit(host_mb, reserve_mb, vms): host_mb — память "
                "хоста, reserve_mb — резерв для самого хозяина, vms — список [имя, память ВМ, проброс "
                "ли устройства]. Память машин с пробросом закреплена и не переподписывается. Верните "
                "кортеж (закреплено всего, сколько памяти остаётся остальным машинам: хост минус "
                "резерв минус закреплённое). Если остаток отрицателен, верните None вместо кортежа."
            ),
            "starter": "def free_for_overcommit(host_mb, reserve_mb, vms):\n    pass\n",
            "tests": [
                {
                    "args": [65536, 4096, [["a", 16384, True], ["b", 8192, False]]],
                    "expected": (16384, 45056),
                },
                {"args": [65536, 4096, []], "expected": (0, 61440)},
                {"args": [16384, 2048, [["a", 16384, True]]], "expected": None},
                {
                    "args": [
                        32768,
                        2048,
                        [["a", 8192, True], ["b", 8192, True], ["c", 4096, False]],
                    ],
                    "expected": (16384, 14336),
                },
                {"args": [8192, 0, [["a", 8192, True]]], "expected": (8192, 0)},
                {"args": [8192, 1, [["a", 8192, True]]], "expected": None},
            ],
            "hint": ("Просуммируйте память машин, у которых третье поле истинно."),
        },
        {
            "id": "virt-migration-blockers",
            "mode": "func",
            "func": "migration_blockers",
            "title": "Что мешает живой миграции",
            "statement": (
                "Напишите функцию migration_blockers(devices): devices — список видов устройств "
                'машины: "emulated", "virtio", "vdpa", "vfio" (проброс), "vf" (виртуальная функция '
                'SR-IOV), "mdev" (посредник). Живой миграции мешают устройства видов vfio, vf и mdev. '
                "Верните кортеж (можно ли мигрировать, отсортированный список мешающих видов без "
                "повторов)."
            ),
            "starter": "def migration_blockers(devices):\n    pass\n",
            "tests": [
                {"args": [["virtio", "virtio"]], "expected": (True, [])},
                {"args": [["virtio", "vfio"]], "expected": (False, ["vfio"])},
                {
                    "args": [["vf", "vf", "mdev", "vdpa"]],
                    "expected": (False, ["mdev", "vf"]),
                },
                {"args": [[]], "expected": (True, [])},
                {"args": [["emulated", "vdpa"]], "expected": (True, [])},
                {
                    "args": [["mdev", "vfio", "vf", "vf"]],
                    "expected": (False, ["mdev", "vf", "vfio"]),
                },
            ],
            "hint": ("Мигрировать можно, когда список мешающих видов пуст."),
        },
        {
            "id": "virt-choose-io",
            "mode": "func",
            "func": "choose_io",
            "title": "Выбор способа ввода-вывода",
            "statement": (
                'Напишите функцию choose_io(req): req — словарь с логическими полями "legacy_guest" '
                '(старый гость без драйверов virtio), "line_rate" (нужна скорость железа) и '
                '"migration" (нужна живая миграция). Правила по порядку: старый гость — "emulated"; '
                'нужна скорость железа и миграция — "vdpa"; нужна скорость железа — "sriov"; иначе — '
                '"virtio".'
            ),
            "starter": "def choose_io(req):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {"legacy_guest": True, "line_rate": True, "migration": True}
                    ],
                    "expected": "emulated",
                },
                {
                    "args": [
                        {"legacy_guest": False, "line_rate": True, "migration": True}
                    ],
                    "expected": "vdpa",
                },
                {
                    "args": [
                        {"legacy_guest": False, "line_rate": True, "migration": False}
                    ],
                    "expected": "sriov",
                },
                {
                    "args": [
                        {"legacy_guest": False, "line_rate": False, "migration": True}
                    ],
                    "expected": "virtio",
                },
                {
                    "args": [
                        {"legacy_guest": False, "line_rate": False, "migration": False}
                    ],
                    "expected": "virtio",
                },
                {
                    "args": [
                        {"legacy_guest": True, "line_rate": False, "migration": False}
                    ],
                    "expected": "emulated",
                },
            ],
            "hint": ("Проверяйте условия строго в указанном порядке."),
        },
    ],
}
