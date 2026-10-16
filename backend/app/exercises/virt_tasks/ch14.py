"""Задачи книги «Виртуализация»: глава 14 — Безопасность: побег из гостя, побочные каналы и confidential computing."""

TASKS: dict[int, list[dict]] = {
    14: [
        {
            "id": "virt-recover-key",
            "mode": "func",
            "func": "recover_key",
            "title": "Ключ по следам в кэше",
            "statement": (
                "Жертва возводит число в степень методом «возведи в квадрат и умножь»: в каждом "
                'раунде она обращается к строке кэша "sqr", а умножение (строка "mul") делает только '
                "если очередной бит ключа равен 1. Атакующий через Flush+Reload узнал, какие строки "
                "кэша были затронуты в каждом раунде. Напишите функцию recover_key(rounds): rounds — "
                "список раундов, каждый — список затронутых строк. Верните строку из нулей и единиц — "
                "восстановленный ключ."
            ),
            "starter": "def recover_key(rounds):\n    pass\n",
            "tests": [
                {
                    "args": [[["sqr", "mul"], ["sqr"], ["sqr", "mul"], ["sqr", "mul"]]],
                    "expected": "1011",
                },
                {"args": [[]], "expected": ""},
                {"args": [[["sqr"], ["sqr"]]], "expected": "00"},
                {"args": [[["mul", "sqr"]]], "expected": "1"},
                {
                    "args": [
                        [["sqr"], ["sqr", "mul"], ["sqr"], ["sqr"], ["sqr", "mul"]]
                    ],
                    "expected": "01001",
                },
            ],
            "hint": ('Бит раунда — 1, если в нём встречается "mul".'),
        },
        {
            "id": "virt-prime-probe",
            "mode": "func",
            "func": "prime_probe",
            "title": "Prime+Probe",
            "statement": (
                "Напишите функцию prime_probe(num_sets, ways, victim_addrs, line_size): атакующий "
                "заполнил каждый набор кэша (num_sets наборов по ways линий). Жертва обращается к "
                "адресам victim_addrs. Адрес относится к линии адрес // line_size, линия — к набору "
                "линия % num_sets. Каждая различная линия жертвы вытесняет одну линию атакующего в "
                "своём наборе, но не больше ways на набор. Верните список длины num_sets: сколько "
                "линий атакующего вытеснено в каждом наборе (так он узнаёт, какими наборами "
                "пользовалась жертва)."
            ),
            "starter": "def prime_probe(num_sets, ways, victim_addrs, line_size):\n    pass\n",
            "tests": [
                {
                    "args": [8, 4, [0, 64, 128], 64],
                    "expected": [1, 1, 1, 0, 0, 0, 0, 0],
                },
                {"args": [4, 2, [0, 1, 2, 3], 64], "expected": [1, 0, 0, 0]},
                {"args": [4, 2, [0, 256, 512, 768], 64], "expected": [2, 0, 0, 0]},
                {"args": [4, 2, [], 64], "expected": [0, 0, 0, 0]},
                {"args": [4, 1, [0, 256], 64], "expected": [1, 0, 0, 0]},
                {
                    "args": [8, 4, [10, 70, 130, 200, 10], 64],
                    "expected": [1, 1, 1, 1, 0, 0, 0, 0],
                },
            ],
            "hint": (
                "Посчитайте различные линии жертвы по наборам и ограничьте значения числом ways."
            ),
        },
        {
            "id": "virt-ksm-timing",
            "mode": "func",
            "func": "merged_pages",
            "title": "Тайминг записи в слитые страницы",
            "statement": (
                "Атакующий меряет время записи в свои страницы с предполагаемым содержимым. Запись в "
                "слитую страницу дольше обычной: нужна копия при записи. Напишите функцию "
                "merged_pages(times, threshold): times — время записи в каждую страницу (мкс), "
                "threshold — порог. Верните список индексов страниц, время записи в которые строго "
                "больше порога (они, вероятно, слиты, то есть у соседа такое же содержимое)."
            ),
            "starter": "def merged_pages(times, threshold):\n    pass\n",
            "tests": [
                {"args": [[2, 3, 50, 2, 61], 10], "expected": [2, 4]},
                {"args": [[], 10], "expected": []},
                {"args": [[1, 1, 1], 10], "expected": []},
                {"args": [[10, 11], 10], "expected": [1]},
                {"args": [[100, 200], 5], "expected": [0, 1]},
                {"args": [[5, 9, 12, 8], 8], "expected": [1, 2]},
            ],
            "hint": ("Пройдите по индексам и оставьте те, где время превышает порог."),
        },
        {
            "id": "virt-harden",
            "mode": "func",
            "func": "harden_report",
            "title": "Рекомендации по защите хоста",
            "statement": (
                'Напишите функцию harden_report(cfg): cfg — словарь с логическими полями "smt", '
                '"l1d_flush", "ksm", "multi_tenant", "qemu_root", "passthrough", "iommu". Верните '
                'отсортированный список рекомендаций: "disable-smt", если SMT включён и на сервере '
                'чужие арендаторы; "enable-l1d-flush", если сброс L1D выключен; "disable-ksm", если '
                'KSM включён и арендаторы чужие; "drop-root", если QEMU работает от root; '
                '"enable-iommu", если есть проброс устройств, а IOMMU выключен.'
            ),
            "starter": "def harden_report(cfg):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {
                            "smt": True,
                            "l1d_flush": False,
                            "ksm": True,
                            "multi_tenant": True,
                            "qemu_root": True,
                            "passthrough": True,
                            "iommu": False,
                        }
                    ],
                    "expected": [
                        "disable-ksm",
                        "disable-smt",
                        "drop-root",
                        "enable-iommu",
                        "enable-l1d-flush",
                    ],
                },
                {
                    "args": [
                        {
                            "smt": False,
                            "l1d_flush": True,
                            "ksm": False,
                            "multi_tenant": False,
                            "qemu_root": False,
                            "passthrough": False,
                            "iommu": False,
                        }
                    ],
                    "expected": [],
                },
                {
                    "args": [
                        {
                            "smt": True,
                            "l1d_flush": True,
                            "ksm": True,
                            "multi_tenant": False,
                            "qemu_root": False,
                            "passthrough": False,
                            "iommu": False,
                        }
                    ],
                    "expected": [],
                },
                {
                    "args": [
                        {
                            "smt": True,
                            "l1d_flush": True,
                            "ksm": False,
                            "multi_tenant": True,
                            "qemu_root": False,
                            "passthrough": True,
                            "iommu": True,
                        }
                    ],
                    "expected": ["disable-smt"],
                },
                {
                    "args": [
                        {
                            "smt": False,
                            "l1d_flush": False,
                            "ksm": True,
                            "multi_tenant": True,
                            "qemu_root": True,
                            "passthrough": False,
                            "iommu": False,
                        }
                    ],
                    "expected": ["disable-ksm", "drop-root", "enable-l1d-flush"],
                },
            ],
            "hint": ("Проверьте условия по очереди и отсортируйте результат."),
        },
        {
            "id": "virt-rmp",
            "mode": "func",
            "func": "rmp_check",
            "title": "Таблица владельцев страниц (RMP)",
            "statement": (
                "Напишите функцию rmp_check(owners, accesses): owners — словарь «страница (строка) → "
                'владелец», где владелец — имя машины, "hv" (гипервизор) или "shared" (общая '
                'страница). accesses — обращения [кто, страница, вид], вид — "r", "w" или "remap" '
                '(переотображение). Для каждого обращения верните "ok", если страница общая или '
                'обращается её владелец, иначе "blocked". Страницы, которых нет в owners, считаются '
                'принадлежащими "hv". Верните список результатов.'
            ),
            "starter": "def rmp_check(owners, accesses):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {"1": "vm1", "2": "shared", "3": "hv"},
                        [
                            ["hv", 1, "r"],
                            ["vm1", 1, "w"],
                            ["hv", 2, "w"],
                            ["vm2", 2, "r"],
                            ["vm1", 3, "r"],
                            ["hv", 3, "remap"],
                        ],
                    ],
                    "expected": ["blocked", "ok", "ok", "ok", "blocked", "ok"],
                },
                {
                    "args": [{}, [["hv", 9, "r"], ["vm1", 9, "r"]]],
                    "expected": ["ok", "blocked"],
                },
                {"args": [{"5": "vm1"}, [["hv", 5, "remap"]]], "expected": ["blocked"]},
                {"args": [{"5": "vm1"}, []], "expected": []},
                {
                    "args": [{"7": "shared"}, [["vm1", 7, "w"], ["hv", 7, "w"]]],
                    "expected": ["ok", "ok"],
                },
            ],
            "hint": (
                "Найдите владельца страницы (по умолчанию hv) и сравните с тем, кто обращается."
            ),
        },
        {
            "id": "virt-attest",
            "mode": "func",
            "func": "verify_report",
            "title": "Проверка отчёта аттестации",
            "statement": (
                "Напишите функцию verify_report(report, expected, nonce): report — отчёт "
                '{"measurement": хеш образа, "nonce": число-метка свежести, "signature_ok": верна ли '
                "подпись процессора}, expected — хеш, который клиент ожидает, nonce — метка, которую "
                'клиент отправил. Причины недоверия: "bad-signature" (подпись неверна), '
                '"wrong-measurement" (хеш не совпал), "stale-nonce" (метка не совпала). Верните '
                'кортеж ("trusted", []), если причин нет, иначе ("untrusted", отсортированный список '
                "причин)."
            ),
            "starter": "def verify_report(report, expected, nonce):\n    pass\n",
            "tests": [
                {
                    "args": [
                        {"measurement": "aa", "nonce": 7, "signature_ok": True},
                        "aa",
                        7,
                    ],
                    "expected": ("trusted", []),
                },
                {
                    "args": [
                        {"measurement": "bb", "nonce": 7, "signature_ok": True},
                        "aa",
                        7,
                    ],
                    "expected": ("untrusted", ["wrong-measurement"]),
                },
                {
                    "args": [
                        {"measurement": "aa", "nonce": 6, "signature_ok": True},
                        "aa",
                        7,
                    ],
                    "expected": ("untrusted", ["stale-nonce"]),
                },
                {
                    "args": [
                        {"measurement": "aa", "nonce": 7, "signature_ok": False},
                        "aa",
                        7,
                    ],
                    "expected": ("untrusted", ["bad-signature"]),
                },
                {
                    "args": [
                        {"measurement": "x", "nonce": 1, "signature_ok": False},
                        "y",
                        2,
                    ],
                    "expected": (
                        "untrusted",
                        ["bad-signature", "stale-nonce", "wrong-measurement"],
                    ),
                },
            ],
            "hint": ("Соберите причины в список и отсортируйте."),
        },
        {
            "id": "virt-measure",
            "mode": "func",
            "func": "measure_chain",
            "title": "Цепочка измерений загрузки",
            "statement": (
                "Напишите функцию measure_chain(components): components — список строк (прошивка, "
                "загрузчик, ядро, …). Измерение начинается со значения из 32 нулевых байт. Для каждой "
                "строки по порядку новое значение — SHA-256 от склейки (прежнее значение, SHA-256 от "
                "строки в кодировке UTF-8) — как расширение регистра PCR. Верните итоговое значение в "
                "виде строки из шестнадцатеричных цифр."
            ),
            "starter": "def measure_chain(components):\n    pass\n",
            "tests": [
                {
                    "args": [[]],
                    "expected": "0000000000000000000000000000000000000000000000000000000000000000",
                },
                {
                    "args": [["firmware"]],
                    "expected": "3e287e57770de15677579228044a2abe6ca7c39d61de4b8a47fd6b7209dd0bab",
                },
                {
                    "args": [["firmware", "bootloader", "kernel"]],
                    "expected": "0748b1c8ca7fabd3533749e2c02d5b097e0723b4bd2f722f6152bf4f2d90d674",
                },
                {
                    "args": [["kernel", "bootloader", "firmware"]],
                    "expected": "61fc74a3b694cc267b533e996a8e210bacb48802381a4103410661a340e1d8d0",
                },
                {
                    "args": [["a", "a"]],
                    "expected": "df7397cce34036cf7527f2669f014bd6a2356de274e09930a08d369414f34bd9",
                },
                {
                    "args": [["прошивка"]],
                    "expected": "dafc0fe4bed79bee3a40e01c906ecf6b2cab570173704090d5d83e6a14650626",
                },
            ],
            "hint": (
                "Используйте hashlib.sha256(...).digest() для промежуточных значений и hexdigest() "
                "для итога."
            ),
        },
        {
            "id": "virt-triage",
            "mode": "func",
            "func": "triage",
            "title": "Разбор находок безопасности",
            "statement": (
                "Напишите функцию triage(findings): findings — список текстовых описаний находок. "
                "Категория выбирается по первому подходящему правилу (регистр букв не важен): "
                'содержит "qemu" или "device" — "escape"; содержит "cache" или "timing" — '
                '"side-channel"; содержит "dma" — "dma"; содержит "storm" или "hog" — "dos"; иначе — '
                '"other". Верните словарь «категория → сколько находок», только для категорий, где их '
                "больше нуля."
            ),
            "starter": "def triage(findings):\n    pass\n",
            "tests": [
                {
                    "args": [
                        [
                            "QEMU heap overflow",
                            "L1 cache timing leak",
                            "interrupt storm",
                            "weak password",
                        ]
                    ],
                    "expected": {"escape": 1, "side-channel": 1, "dos": 1, "other": 1},
                },
                {"args": [[]], "expected": {}},
                {
                    "args": [
                        [
                            "device emulation bug",
                            "Device reset bug",
                            "DMA to host memory",
                        ]
                    ],
                    "expected": {"escape": 2, "dma": 1},
                },
                {
                    "args": [
                        [
                            "CPU hog in guest",
                            "timing difference on write",
                            "Cache probe",
                        ]
                    ],
                    "expected": {"dos": 1, "side-channel": 2},
                },
                {"args": [["unknown", "other thing"]], "expected": {"other": 2}},
            ],
            "hint": (
                "Для каждой находки проверьте правила по порядку и увеличьте счётчик."
            ),
        },
    ],
}
