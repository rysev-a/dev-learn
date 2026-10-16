"""Задачи книги «Виртуализация»: глава 9 — Диски и образы: qcow2, снимки и copy-on-write."""

TASKS: dict[int, list[dict]] = {
    9: [
        {
            "id": "virt-qcow2-split",
            "mode": "func",
            "func": "qcow2_split",
            "title": "Поиск кластера в qcow2",
            "statement": (
                "Напишите функцию qcow2_split(addr, cluster_size): addr — гостевое смещение в байтах, "
                "cluster_size — размер кластера в байтах. Таблица второго уровня (L2) занимает один "
                "кластер, запись — 8 байт. Верните кортеж (индекс в L1, индекс в L2, смещение внутри "
                "кластера)."
            ),
            "starter": "def qcow2_split(addr, cluster_size):\n    pass\n",
            "tests": [
                {"args": [0, 65536], "expected": (0, 0, 0)},
                {"args": [65536, 65536], "expected": (0, 1, 0)},
                {"args": [65535, 65536], "expected": (0, 0, 65535)},
                {"args": [536870912, 65536], "expected": (1, 0, 0)},
                {"args": [536940912, 65536], "expected": (1, 1, 4464)},
                {"args": [5000, 4096], "expected": (0, 1, 904)},
                {"args": [6320137, 4096], "expected": (3, 7, 9)},
            ],
            "hint": (
                "Номер кластера = addr // cluster_size; записей в L2 — cluster_size // 8."
            ),
        },
        {
            "id": "virt-overlay-read",
            "mode": "func",
            "func": "overlay_read",
            "title": "Чтение через цепочку слоёв",
            "statement": (
                "Напишите функцию overlay_read(chain, cluster): chain — цепочка слоёв образа, от "
                "верхнего (текущего) к базовому; каждый слой — словарь «номер кластера (строка) → "
                "данные». cluster — номер кластера. Верните данные из самого верхнего слоя, где "
                "кластер есть; если его нет ни в одном слое, верните None (кластер читается нулями)."
            ),
            "starter": "def overlay_read(chain, cluster):\n    pass\n",
            "tests": [
                {"args": [[{"2": "x"}, {"1": "a", "2": "b"}], 2], "expected": "x"},
                {"args": [[{"2": "x"}, {"1": "a", "2": "b"}], 1], "expected": "a"},
                {"args": [[{"2": "x"}, {"1": "a", "2": "b"}], 3], "expected": None},
                {"args": [[], 0], "expected": None},
                {"args": [[{}, {}, {"7": "deep"}], 7], "expected": "deep"},
                {
                    "args": [[{"0": "top"}, {"0": "mid"}, {"0": "base"}], 0],
                    "expected": "top",
                },
            ],
            "hint": ("Идите по слоям сверху вниз и берите первое найденное."),
        },
        {
            "id": "virt-layer-run",
            "mode": "func",
            "func": "layer_run",
            "title": "Запись, чтение и снимки",
            "statement": (
                "Напишите функцию layer_run(layers, ops): layers — цепочка слоёв (словари «номер "
                "кластера (строка) → данные»), от верхнего к базовому; не меняйте входные данные. ops "
                '— операции: ["w", кластер, данные] (запись попадает только в верхний слой), ["r", '
                'кластер] (чтение из самого верхнего слоя, где кластер есть, иначе None) и ["snap"] '
                "(снимок: сверху добавляется новый пустой слой). Верните кортеж (список результатов "
                "всех чтений по порядку, список размеров слоёв — числа кластеров в каждом, сверху "
                "вниз)."
            ),
            "starter": "def layer_run(layers, ops):\n    pass\n",
            "tests": [
                {
                    "args": [[{}], [["w", 1, "a"], ["r", 1], ["r", 2]]],
                    "expected": (["a", None], [1]),
                },
                {
                    "args": [
                        [{"1": "base"}],
                        [["snap"], ["r", 1], ["w", 1, "new"], ["r", 1]],
                    ],
                    "expected": (["base", "new"], [1, 1]),
                },
                {
                    "args": [
                        [{"1": "x"}, {"2": "y"}],
                        [
                            ["w", 3, "z"],
                            ["snap"],
                            ["snap"],
                            ["r", 2],
                            ["w", 2, "q"],
                            ["r", 2],
                        ],
                    ],
                    "expected": (["y", "q"], [1, 0, 2, 1]),
                },
                {"args": [[{}], []], "expected": ([], [0])},
                {
                    "args": [
                        [{"0": "a", "1": "b"}],
                        [["snap"], ["w", 0, "c"], ["snap"], ["r", 0], ["r", 1]],
                    ],
                    "expected": (["c", "b"], [0, 1, 2]),
                },
            ],
            "hint": (
                "Верхний слой — первый элемент списка; снимок вставляет пустой словарь в начало."
            ),
        },
        {
            "id": "virt-chain-lookups",
            "mode": "func",
            "func": "chain_lookups",
            "title": "Цена чтения по цепочке",
            "statement": (
                "Напишите функцию chain_lookups(chain, clusters): chain — цепочка слоёв (словари "
                "«номер кластера (строка) → данные»), от верхнего к базовому; clusters — номера "
                "читаемых кластеров. Чтение кластера из слоя на глубине d (верхний слой — глубина 0) "
                "стоит d + 1 обращение к таблицам; если кластера нет нигде, проверяются все слои. "
                "Верните суммарное число обращений."
            ),
            "starter": "def chain_lookups(chain, clusters):\n    pass\n",
            "tests": [
                {
                    "args": [[{"1": "a"}, {"2": "b"}, {"3": "c"}], [1, 2, 3]],
                    "expected": 6,
                },
                {"args": [[{"1": "a"}, {"2": "b"}, {"3": "c"}], [9]], "expected": 3},
                {"args": [[], [1, 2]], "expected": 0},
                {"args": [[{"1": "a"}], []], "expected": 0},
                {"args": [[{}, {}, {"5": "x"}], [5, 5, 5]], "expected": 9},
                {"args": [[{"0": "a", "1": "b"}], [0, 1, 2]], "expected": 3},
            ],
            "hint": ("Для каждого кластера найдите индекс первого слоя, где он есть."),
        },
        {
            "id": "virt-commit-layer",
            "mode": "func",
            "func": "commit_layer",
            "title": "Слияние слоя вниз",
            "statement": (
                "Напишите функцию commit_layer(top, base): top и base — слои (словари «номер кластера "
                "(строка) → данные»). Слияние переносит все кластеры верхнего слоя в нижний, при "
                "совпадении побеждает верхний. Не меняйте входные словари. Верните кортеж (новый "
                "нижний слой, сколько кластеров перенесено — размер top)."
            ),
            "starter": "def commit_layer(top, base):\n    pass\n",
            "tests": [
                {
                    "args": [{"1": "x"}, {"1": "a", "2": "b"}],
                    "expected": ({"1": "x", "2": "b"}, 1),
                },
                {"args": [{}, {"1": "a"}], "expected": ({"1": "a"}, 0)},
                {"args": [{"3": "n"}, {}], "expected": ({"3": "n"}, 1)},
                {
                    "args": [{"1": "x", "2": "y"}, {"2": "b", "3": "c"}],
                    "expected": ({"2": "y", "3": "c", "1": "x"}, 2),
                },
                {"args": [{}, {}], "expected": ({}, 0)},
            ],
            "hint": ("Скопируйте base и обновите его содержимым top."),
        },
        {
            "id": "virt-thin-size",
            "mode": "func",
            "func": "thin_size",
            "title": "Размер разреженного qcow2",
            "statement": (
                "Модель размера файла qcow2. Напишите функцию thin_size(written, cluster_size): "
                "written — список номеров кластеров, в которые гость писал (номера могут "
                "повторяться), cluster_size — размер кластера. Размер файла = (число различных "
                "записанных кластеров + число различных таблиц L2, которые нужны для них, + 1 кластер "
                "на заголовок и таблицу L1) * cluster_size. Таблица L2 вмещает cluster_size // 8 "
                "записей, номер её — кластер // (cluster_size // 8)."
            ),
            "starter": "def thin_size(written, cluster_size):\n    pass\n",
            "tests": [
                {"args": [[], 65536], "expected": 65536},
                {"args": [[0], 65536], "expected": 196608},
                {"args": [[0, 0, 0], 65536], "expected": 196608},
                {"args": [[0, 1, 2, 3], 65536], "expected": 393216},
                {"args": [[0, 8192], 65536], "expected": 327680},
                {"args": [[0, 511, 512], 4096], "expected": 24576},
                {"args": [[5, 6, 7, 1000], 4096], "expected": 28672},
            ],
            "hint": ("Различные таблицы L2 — множество значений cluster // per_l2."),
        },
        {
            "id": "virt-discard",
            "mode": "func",
            "func": "allocated_after",
            "title": "Возврат места командой discard",
            "statement": (
                'Напишите функцию allocated_after(ops, discard): ops — список операций ["w", кластер] '
                '(запись выделяет кластер) и ["d", кластер] (гость отбрасывает кластер командой '
                "TRIM). Если discard истинно, команда d освобождает кластер; если ложно — "
                "игнорируется (устройство не передаёт discard). Верните отсортированный список "
                "выделенных кластеров в конце."
            ),
            "starter": "def allocated_after(ops, discard):\n    pass\n",
            "tests": [
                {"args": [[["w", 1], ["w", 2], ["d", 1]], True], "expected": [2]},
                {"args": [[["w", 1], ["w", 2], ["d", 1]], False], "expected": [1, 2]},
                {"args": [[], True], "expected": []},
                {"args": [[["d", 5]], True], "expected": []},
                {"args": [[["w", 3], ["d", 3], ["w", 3]], True], "expected": [3]},
                {
                    "args": [[["w", 9], ["w", 1], ["w", 5], ["d", 5]], True],
                    "expected": [1, 9],
                },
            ],
            "hint": ("Храните множество выделенных кластеров."),
        },
        {
            "id": "virt-fsfreeze",
            "mode": "func",
            "func": "snapshot_states",
            "title": "Согласованность снимка",
            "statement": (
                'Напишите функцию snapshot_states(events): events — события "write" (запись гостя), '
                '"flush" (гость сбросил кэш на диск), "freeze" (агент: сбросить кэш и заморозить '
                'запись), "thaw" (разморозить) и "snapshot". У гостя есть счётчик «грязных» данных в '
                "кэше (вначале 0). Запись при незамороженной записи увеличивает его на 1, при "
                "замороженной — ставится в очередь. flush обнуляет счётчик. freeze обнуляет счётчик и "
                "замораживает запись. thaw размораживает и переносит очередь в счётчик. Для каждого "
                'snapshot верните "consistent", если счётчик равен 0, иначе "crash-consistent".'
            ),
            "starter": "def snapshot_states(events):\n    pass\n",
            "tests": [
                {"args": [["write", "snapshot"]], "expected": ["crash-consistent"]},
                {
                    "args": [["write", "freeze", "snapshot", "thaw"]],
                    "expected": ["consistent"],
                },
                {
                    "args": [
                        [
                            "write",
                            "write",
                            "freeze",
                            "write",
                            "snapshot",
                            "thaw",
                            "snapshot",
                        ]
                    ],
                    "expected": ["consistent", "crash-consistent"],
                },
                {"args": [[]], "expected": []},
                {"args": [["snapshot"]], "expected": ["consistent"]},
                {"args": [["write", "flush", "snapshot"]], "expected": ["consistent"]},
                {
                    "args": [["freeze", "thaw", "write", "snapshot"]],
                    "expected": ["crash-consistent"],
                },
            ],
            "hint": ("Заведите счётчик, очередь и флаг заморозки."),
        },
    ],
}
