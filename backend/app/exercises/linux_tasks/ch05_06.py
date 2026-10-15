"""Задачи книги «Linux: от шелла до ядра»: главы 5–6."""

TASKS: dict[int, list[dict]] = {
    5: [
        {
            "id": "svc-parse-unit",
            "mode": "func",
            "func": "parse_unit",
            "title": "Разбор юнит-файла",
            "statement": (
                "Напишите функцию parse_unit(text): разберите юнит-файл systemd. "
                "Секции — '[Unit]', '[Service]' и т. д.; строки 'Ключ=значение'; "
                "строки с '#' или ';' в начале и пустые игнорируются. Верните "
                "словарь «секция → словарь «ключ → список значений в порядке "
                "появления»» (ключ может повторяться: несколько After=, "
                "ExecStartPre=)."
            ),
            "starter": "def parse_unit(text):\n    pass\n",
            "tests": [
                {"args": ["[Unit]\nDescription=Web\nAfter=network.target\nAfter=postgresql.service\n\n[Service]\nExecStart=/usr/bin/web --port=80\nRestart=on-failure\n\n[Install]\nWantedBy=multi-user.target\n"], "expected": {"Unit": {"Description": ["Web"], "After": ["network.target", "postgresql.service"]}, "Service": {"ExecStart": ["/usr/bin/web --port=80"], "Restart": ["on-failure"]}, "Install": {"WantedBy": ["multi-user.target"]}}},
                {"args": ["# комментарий\n[Service]\n; ещё\nType=simple\nEnvironment=A=1\nEnvironment=B=2\n"], "expected": {"Service": {"Type": ["simple"], "Environment": ["A=1", "B=2"]}}},
                {"args": [""], "expected": {}},
                {"args": ["[Unit]\n"], "expected": {"Unit": {}}},
                {"args": ["[Service]\nExecStart = /bin/true\n"], "expected": {"Service": {"ExecStart": ["/bin/true"]}}},
            ],
            "hint": "Текущая секция — переменная; значения копите списком через setdefault; split('=', 1) сохраняет '=' внутри значения.",
        },
        {
            "id": "svc-start-order",
            "mode": "func",
            "func": "start_order",
            "title": "Порядок запуска юнитов",
            "statement": (
                "Напишите функцию start_order(units): units — словарь «имя → список "
                "имён юнитов, после которых он стартует» (After=; имена, которых "
                "нет среди ключей, игнорируются). Верните порядок запуска: юнит "
                "стартует после всех своих зависимостей; из готовых к старту берите "
                "первым наименьшее имя по алфавиту. Если есть цикл — строку "
                "'cycle'."
            ),
            "starter": "import heapq\n\n\ndef start_order(units):\n    pass\n",
            "tests": [
                {"args": [{"web": ["db", "net"], "db": ["net"], "net": []}], "expected": ["net", "db", "web"]},
                {"args": [{"a": [], "b": [], "c": ["a", "b"]}], "expected": ["a", "b", "c"]},
                {"args": [{"a": ["b"], "b": ["a"]}], "expected": "cycle"},
                {"args": [{"x": ["missing"]}], "expected": ["x"]},
                {"args": [{}], "expected": []},
                {"args": [{"a": ["a"]}], "expected": "cycle"},
                {"args": [{"z": [], "m": ["z"], "b": ["z"], "a": ["m", "b"]}], "expected": ["z", "b", "m", "a"]},
            ],
            "hint": "Алгоритм Кана с кучей: пока есть юниты без неудовлетворённых зависимостей — берём наименьший; если в конце остались юниты — цикл.",
        },
        {
            "id": "svc-activation",
            "mode": "func",
            "func": "activation",
            "title": "Что запустит цель",
            "statement": (
                "Напишите функцию activation(units, target): units — словарь «имя → "
                "{'requires': [...], 'wants': [...]}» (ключи могут отсутствовать). "
                "Запуск цели тянет за собой все юниты, достижимые по requires и "
                "wants. Отсутствующий в units юнит из wants игнорируется, а "
                "отсутствующий из requires (или сама цель) — ошибка. Если ошибок "
                "нет — отсортированный список всех запускаемых юнитов (с целью), "
                "иначе строка 'failed: ' + отсортированные через ', ' имена "
                "отсутствующих."
            ),
            "starter": "def activation(units, target):\n    pass\n",
            "tests": [
                {"args": [{"multi": {"requires": ["net"], "wants": ["web"]}, "net": {}, "web": {"requires": ["db"]}, "db": {}}, "multi"], "expected": ["db", "multi", "net", "web"]},
                {"args": [{"a": {"wants": ["ghost"]}}, "a"], "expected": ["a"]},
                {"args": [{"a": {"requires": ["ghost", "phantom"]}}, "a"], "expected": "failed: ghost, phantom"},
                {"args": [{"a": {"requires": ["b"]}, "b": {"requires": ["a"]}}, "a"], "expected": ["a", "b"]},
                {"args": [{}, "nothing"], "expected": "failed: nothing"},
                {"args": [{"t": {"wants": ["x"]}, "x": {"requires": ["y"]}}, "t"], "expected": "failed: y"},
            ],
            "hint": "Обход в глубину с признаком «обязательна ли зависимость»; отсутствующие обязательные накапливайте и в конце верните ошибку.",
        },
        {
            "id": "svc-restart-policy",
            "mode": "func",
            "func": "should_restart",
            "title": "Политика перезапуска",
            "statement": (
                "Напишите функцию should_restart(policy, kind): policy — значение "
                "Restart= ('no', 'always', 'on-success', 'on-failure', "
                "'on-abnormal', 'on-abort'); kind — как завершилась служба: 'exit0' "
                "(код 0), 'exit-nonzero' (ненулевой код), 'clean-signal' (SIGTERM, "
                "SIGHUP, SIGINT, SIGPIPE), 'unclean-signal' (любой другой сигнал, "
                "например SIGSEGV), 'timeout', 'watchdog'. Правила: no — никогда; "
                "always — всегда; on-success — exit0 и clean-signal; on-failure — "
                "всё кроме exit0 и clean-signal; on-abnormal — unclean-signal, "
                "timeout, watchdog; on-abort — только unclean-signal. Верните "
                "True/False."
            ),
            "starter": "def should_restart(policy, kind):\n    pass\n",
            "tests": [
                {"args": ["no", "exit0"], "expected": False},
                {"args": ["no", "exit-nonzero"], "expected": False},
                {"args": ["no", "clean-signal"], "expected": False},
                {"args": ["no", "unclean-signal"], "expected": False},
                {"args": ["no", "timeout"], "expected": False},
                {"args": ["no", "watchdog"], "expected": False},
                {"args": ["always", "exit0"], "expected": True},
                {"args": ["always", "exit-nonzero"], "expected": True},
                {"args": ["always", "clean-signal"], "expected": True},
                {"args": ["always", "unclean-signal"], "expected": True},
                {"args": ["always", "timeout"], "expected": True},
                {"args": ["always", "watchdog"], "expected": True},
                {"args": ["on-success", "exit0"], "expected": True},
                {"args": ["on-success", "exit-nonzero"], "expected": False},
                {"args": ["on-success", "clean-signal"], "expected": True},
                {"args": ["on-success", "unclean-signal"], "expected": False},
                {"args": ["on-success", "timeout"], "expected": False},
                {"args": ["on-success", "watchdog"], "expected": False},
                {"args": ["on-failure", "exit0"], "expected": False},
                {"args": ["on-failure", "exit-nonzero"], "expected": True},
                {"args": ["on-failure", "clean-signal"], "expected": False},
                {"args": ["on-failure", "unclean-signal"], "expected": True},
                {"args": ["on-failure", "timeout"], "expected": True},
                {"args": ["on-failure", "watchdog"], "expected": True},
                {"args": ["on-abnormal", "exit0"], "expected": False},
                {"args": ["on-abnormal", "exit-nonzero"], "expected": False},
                {"args": ["on-abnormal", "clean-signal"], "expected": False},
                {"args": ["on-abnormal", "unclean-signal"], "expected": True},
                {"args": ["on-abnormal", "timeout"], "expected": True},
                {"args": ["on-abnormal", "watchdog"], "expected": True},
                {"args": ["on-abort", "exit0"], "expected": False},
                {"args": ["on-abort", "exit-nonzero"], "expected": False},
                {"args": ["on-abort", "clean-signal"], "expected": False},
                {"args": ["on-abort", "unclean-signal"], "expected": True},
                {"args": ["on-abort", "timeout"], "expected": False},
                {"args": ["on-abort", "watchdog"], "expected": False},
            ],
            "hint": "Задайте множество «чистых» завершений и выразите каждую политику через принадлежность к множествам.",
        },
        {
            "id": "svc-start-limit",
            "mode": "func",
            "func": "start_limit_time",
            "title": "Защита от бесконечных перезапусков",
            "statement": (
                "Напишите функцию start_limit_time(starts, interval, burst): starts "
                "— моменты (секунды, по возрастанию), в которые служба пытается "
                "запуститься. Запуск запрещён, если за последние interval секунд "
                "уже было burst запусков (то есть предыдущие запуски с t_prev > t − "
                "interval). Верните момент первого запрещённого запуска или None."
            ),
            "starter": "def start_limit_time(starts, interval, burst):\n    pass\n",
            "tests": [
                {"args": [[0, 1, 2, 3, 4, 5], 10, 5], "expected": 5},
                {"args": [[0, 10, 20, 30], 10, 1], "expected": None},
                {"args": [[0, 5, 10, 15, 20, 25], 10, 3], "expected": None},
                {"args": [[], 10, 5], "expected": None},
                {"args": [[0, 1, 2], 60, 5], "expected": None},
                {"args": [[0, 100, 200, 300, 400, 500, 600], 100, 2], "expected": None},
                {"args": [[5], 1, 1], "expected": None},
            ],
            "hint": "Скользящее окно: оставляйте только запуски, которые моложе interval, и сравнивайте их число с burst до добавления нового.",
        },
        {
            "id": "svc-timer-next",
            "mode": "func",
            "func": "next_timer",
            "title": "Следующее срабатывание таймера",
            "statement": (
                "Напишите функцию next_timer(spec, now): now — 'ГГГГ-ММ-ДД ЧЧ:ММ'; "
                "spec — 'daily ЧЧ:ММ', 'hourly ММ' (минута каждого часа) или "
                "'weekly день ЧЧ:ММ' (день: mon, tue, wed, thu, fri, sat, sun). "
                "Верните ближайший момент строго после now в том же формате."
            ),
            "starter": "from datetime import datetime, timedelta\n\n\ndef next_timer(spec, now):\n    pass\n",
            "tests": [
                {"args": ["daily 03:30", "2024-05-10 01:00"], "expected": "2024-05-10 03:30"},
                {"args": ["daily 03:30", "2024-05-10 03:30"], "expected": "2024-05-11 03:30"},
                {"args": ["daily 03:30", "2024-05-10 12:00"], "expected": "2024-05-11 03:30"},
                {"args": ["hourly 15", "2024-05-10 10:14"], "expected": "2024-05-10 10:15"},
                {"args": ["hourly 15", "2024-05-10 10:15"], "expected": "2024-05-10 11:15"},
                {"args": ["hourly 15", "2024-05-10 23:59"], "expected": "2024-05-11 00:15"},
                {"args": ["weekly mon 02:00", "2024-05-10 12:00"], "expected": "2024-05-13 02:00"},
                {"args": ["weekly fri 12:00", "2024-05-10 12:00"], "expected": "2024-05-17 12:00"},
                {"args": ["weekly fri 12:00", "2024-05-10 11:59"], "expected": "2024-05-10 12:00"},
                {"args": ["daily 00:00", "2024-12-31 23:59"], "expected": "2025-01-01 00:00"},
            ],
            "hint": "Подставьте время в сегодняшнюю дату; если получилось не позже now — сдвиньте на период (день, час, неделю); день недели — через weekday().",
        },
        {
            "id": "svc-journal-filter",
            "mode": "func",
            "func": "journal_filter",
            "title": "Фильтр журнала",
            "statement": (
                "Напишите функцию journal_filter(lines, level, unit): строки "
                "журнала вида '2024-05-01 12:00:01 nginx err Connection refused' "
                "(дата, время, юнит, уровень, сообщение до конца строки). Уровни по "
                "убыванию важности: emerg, alert, crit, err, warning, notice, info, "
                "debug. Верните сообщения (по порядку) записей, у которых уровень "
                "не менее важен, чем level, и (если unit не None) юнит совпадает."
            ),
            "starter": "def journal_filter(lines, level, unit):\n    pass\n",
            "tests": [
                {"args": [["2024-05-01 12:00:01 nginx err Connection refused", "2024-05-01 12:00:02 nginx info started", "2024-05-01 12:00:03 sshd crit Disk full here"], "err", None], "expected": ["Connection refused", "Disk full here"]},
                {"args": [["2024-05-01 12:00:01 nginx err a b c", "2024-05-01 12:00:02 sshd err x"], "debug", "nginx"], "expected": ["a b c"]},
                {"args": [[], "err", None], "expected": []},
                {"args": [["2024-05-01 12:00:01 app warning slow query"], "err", None], "expected": []},
                {"args": [["2024-05-01 12:00:01 app emerg boom", "bad line"], "emerg", "app"], "expected": ["boom"]},
            ],
            "hint": "Уровень — индекс в списке LEVELS; «не менее важен» значит индекс не больше.",
        },
        {
            "id": "svc-env-file",
            "mode": "func",
            "func": "parse_env_file",
            "title": "EnvironmentFile",
            "statement": (
                "Напишите функцию parse_env_file(text): файл окружения службы. "
                "Строки 'КЛЮЧ=значение'; пустые, без '=' и начинающиеся с '#' или "
                "';' игнорируйте. Значение в одинарных или двойных кавычках — "
                "снимите внешние кавычки. Пробелы вокруг ключа и значения обрежьте. "
                "При повторе побеждает последняя строка. Верните словарь."
            ),
            "starter": "def parse_env_file(text):\n    pass\n",
            "tests": [
                {"args": ["PORT=8080\nHOST=\"0.0.0.0\"\nNAME='my app'\n"], "expected": {"PORT": "8080", "HOST": "0.0.0.0", "NAME": "my app"}},
                {"args": ["# c\n; d\n\nA=1\nA=2\nB = x y \n"], "expected": {"A": "2", "B": "x y"}},
                {"args": [""], "expected": {}},
                {"args": ["NOEQ\nX=1=2\n"], "expected": {"X": "1=2"}},
                {"args": ["Q=\"unterminated\nE=\"\"\n"], "expected": {"Q": "\"unterminated", "E": ""}},
            ],
            "hint": "split('=', 1); кавычки снимаются только если первый и последний символ значения одинаковые кавычки.",
        },
    ],
    6: [
        {
            "id": "net-ip-convert",
            "mode": "func",
            "func": "ip_convert",
            "title": "IP-адрес и число",
            "statement": (
                "Напишите функцию ip_convert(value): если value — строка вида "
                "'192.168.1.10', верните целое число (32 бита); если целое — "
                "верните строку адреса. Без модуля ipaddress."
            ),
            "starter": "def ip_convert(value):\n    pass\n",
            "tests": [
                {"args": ["192.168.1.10"], "expected": 3232235786},
                {"args": ["0.0.0.0"], "expected": 0},
                {"args": ["255.255.255.255"], "expected": 4294967295},
                {"args": [3232235786], "expected": "192.168.1.10"},
                {"args": [0], "expected": "0.0.0.0"},
                {"args": [4294967295], "expected": "255.255.255.255"},
                {"args": ["10.0.0.1"], "expected": 167772161},
                {"args": [167772161], "expected": "10.0.0.1"},
            ],
            "hint": "Четыре октета — это четыре байта числа: сдвиги на 24, 16, 8 и 0.",
        },
        {
            "id": "net-cidr-info",
            "mode": "func",
            "func": "cidr_info",
            "title": "Калькулятор подсетей",
            "statement": (
                "Напишите функцию cidr_info(cidr): 'a.b.c.d/p'. Верните кортеж из 6 "
                "элементов: (адрес_сети, широковещательный, первый_хост, "
                "последний_хост, число_хостов, маска) — адреса строками, число — "
                "целое. Для p ≤ 30: первый = сеть + 1, последний = "
                "широковещательный − 1, хостов 2^(32−p) − 2. Для /31 хостов 2 "
                "(первый и последний — сами адреса сети), для /32 — один (сам "
                "адрес). Адрес в записи может быть любым адресом сети."
            ),
            "starter": "def cidr_info(cidr):\n    pass\n",
            "tests": [
                {"args": ["192.168.1.77/24"], "expected": ("192.168.1.0", "192.168.1.255", "192.168.1.1", "192.168.1.254", 254, "255.255.255.0")},
                {"args": ["10.0.0.0/8"], "expected": ("10.0.0.0", "10.255.255.255", "10.0.0.1", "10.255.255.254", 16777214, "255.0.0.0")},
                {"args": ["172.16.5.130/26"], "expected": ("172.16.5.128", "172.16.5.191", "172.16.5.129", "172.16.5.190", 62, "255.255.255.192")},
                {"args": ["192.168.0.1/30"], "expected": ("192.168.0.0", "192.168.0.3", "192.168.0.1", "192.168.0.2", 2, "255.255.255.252")},
                {"args": ["10.1.1.1/31"], "expected": ("10.1.1.0", "10.1.1.1", "10.1.1.0", "10.1.1.1", 2, "255.255.255.254")},
                {"args": ["10.1.1.1/32"], "expected": ("10.1.1.1", "10.1.1.1", "10.1.1.1", "10.1.1.1", 1, "255.255.255.255")},
                {"args": ["0.0.0.0/0"], "expected": ("0.0.0.0", "255.255.255.255", "0.0.0.1", "255.255.255.254", 4294967294, "0.0.0.0")},
                {"args": ["203.0.113.200/25"], "expected": ("203.0.113.128", "203.0.113.255", "203.0.113.129", "203.0.113.254", 126, "255.255.255.128")},
            ],
            "hint": "mask = (0xFFFFFFFF << (32 − p)) & 0xFFFFFFFF; сеть = ip & mask; широковещательный = сеть | ~mask.",
        },
        {
            "id": "net-same-subnet",
            "mode": "func",
            "func": "same_subnet",
            "title": "В одной ли подсети",
            "statement": (
                "Напишите функцию same_subnet(a, b, prefix): True, если два "
                "IPv4-адреса (строки) находятся в одной подсети с длиной префикса "
                "prefix (0…32)."
            ),
            "starter": "def same_subnet(a, b, prefix):\n    pass\n",
            "tests": [
                {"args": ["192.168.1.10", "192.168.1.200", 24], "expected": True},
                {"args": ["192.168.1.10", "192.168.2.10", 24], "expected": False},
                {"args": ["192.168.1.10", "192.168.2.10", 16], "expected": True},
                {"args": ["10.0.0.1", "10.0.0.2", 32], "expected": False},
                {"args": ["10.0.0.1", "11.0.0.1", 0], "expected": True},
                {"args": ["172.16.0.1", "172.31.255.254", 12], "expected": True},
                {"args": ["172.16.0.1", "172.32.0.1", 12], "expected": False},
            ],
            "hint": "Сравните a & mask и b & mask.",
        },
        {
            "id": "net-route-lookup",
            "mode": "func",
            "func": "route_lookup",
            "title": "Выбор маршрута",
            "statement": (
                "Напишите функцию route_lookup(table, dest): table — список "
                "[сеть_cidr, шлюз]; dest — IPv4-адрес. Выберите запись с наибольшей "
                "длиной префикса, содержащую dest, и верните её шлюз (маршрут по "
                "умолчанию — '0.0.0.0/0'). Если подходящих нет — 'unreachable'. При "
                "равной длине — первая в списке."
            ),
            "starter": "def route_lookup(table, dest):\n    pass\n",
            "tests": [
                {"args": [[["10.0.0.0/8", "gw1"], ["10.1.0.0/16", "gw2"], ["0.0.0.0/0", "gw0"]], "10.1.2.3"], "expected": "gw2"},
                {"args": [[["10.0.0.0/8", "gw1"], ["10.1.0.0/16", "gw2"], ["0.0.0.0/0", "gw0"]], "10.2.2.2"], "expected": "gw1"},
                {"args": [[["10.0.0.0/8", "gw1"], ["10.1.0.0/16", "gw2"], ["0.0.0.0/0", "gw0"]], "8.8.8.8"], "expected": "gw0"},
                {"args": [[["10.0.0.0/8", "gw1"]], "8.8.8.8"], "expected": "unreachable"},
                {"args": [[], "1.1.1.1"], "expected": "unreachable"},
                {"args": [[["192.168.1.0/24", "eth0"], ["192.168.1.128/25", "eth1"]], "192.168.1.200"], "expected": "eth1"},
                {"args": [[["192.168.1.0/24", "eth0"], ["192.168.1.128/25", "eth1"]], "192.168.1.100"], "expected": "eth0"},
                {"args": [[["1.2.3.4/32", "host"], ["0.0.0.0/0", "def"]], "1.2.3.4"], "expected": "host"},
            ],
            "hint": "Для каждой записи проверьте принадлежность адреса сети и запомните запись с самым длинным префиксом.",
        },
        {
            "id": "net-split-subnet",
            "mode": "func",
            "func": "split_subnet",
            "title": "Нарезка сети на подсети",
            "statement": (
                "Напишите функцию split_subnet(cidr, new_prefix): разбейте сеть "
                "cidr ('a.b.c.d/p', адрес — начало сети) на подсети с длиной "
                "префикса new_prefix ≥ p. Верните список строк 'адрес/new_prefix' "
                "по возрастанию."
            ),
            "starter": "def split_subnet(cidr, new_prefix):\n    pass\n",
            "tests": [
                {"args": ["192.168.1.0/24", 26], "expected": ["192.168.1.0/26", "192.168.1.64/26", "192.168.1.128/26", "192.168.1.192/26"]},
                {"args": ["10.0.0.0/8", 10], "expected": ["10.0.0.0/10", "10.64.0.0/10", "10.128.0.0/10", "10.192.0.0/10"]},
                {"args": ["192.168.1.0/24", 24], "expected": ["192.168.1.0/24"]},
                {"args": ["172.16.0.0/22", 24], "expected": ["172.16.0.0/24", "172.16.1.0/24", "172.16.2.0/24", "172.16.3.0/24"]},
                {"args": ["10.0.0.0/30", 32], "expected": ["10.0.0.0/32", "10.0.0.1/32", "10.0.0.2/32", "10.0.0.3/32"]},
            ],
            "hint": "Шаг между подсетями — 2^(32 − new_prefix); подсетей 2^(new_prefix − p).",
        },
        {
            "id": "net-firewall",
            "mode": "func",
            "func": "firewall",
            "title": "Правила фильтра пакетов",
            "statement": (
                "Напишите функцию firewall(rules, packet, policy): rules — список "
                "[действие, протокол, источник, порт], где действие 'ACCEPT' или "
                "'DROP'; протокол — 'tcp', 'udp' или 'any'; источник — IPv4-подсеть "
                "'a.b.c.d/p' или 'any'; порт — число или 'any' (порт назначения). "
                "packet — [протокол, адрес_источника, порт_назначения]. Правила "
                "проверяются по порядку, срабатывает первое подходящее; если "
                "подходящих нет — действие policy. Верните 'ACCEPT' или 'DROP'."
            ),
            "starter": "def firewall(rules, packet, policy):\n    pass\n",
            "tests": [
                {"args": [[["ACCEPT", "tcp", "any", 22], ["ACCEPT", "tcp", "any", 80]], ["tcp", "1.2.3.4", 22], "DROP"], "expected": "ACCEPT"},
                {"args": [[["ACCEPT", "tcp", "any", 22], ["ACCEPT", "tcp", "any", 80]], ["tcp", "1.2.3.4", 25], "DROP"], "expected": "DROP"},
                {"args": [[["DROP", "any", "10.0.0.0/8", "any"], ["ACCEPT", "tcp", "any", 22]], ["tcp", "10.1.1.1", 22], "DROP"], "expected": "DROP"},
                {"args": [[["ACCEPT", "tcp", "10.0.0.0/8", 22], ["DROP", "any", "any", "any"]], ["tcp", "10.9.9.9", 22], "ACCEPT"], "expected": "ACCEPT"},
                {"args": [[["ACCEPT", "tcp", "10.0.0.0/8", 22], ["DROP", "any", "any", "any"]], ["tcp", "8.8.8.8", 22], "ACCEPT"], "expected": "DROP"},
                {"args": [[["ACCEPT", "udp", "any", 53]], ["tcp", "1.1.1.1", 53], "ACCEPT"], "expected": "ACCEPT"},
                {"args": [[], ["udp", "1.1.1.1", 53], "DROP"], "expected": "DROP"},
                {"args": [[["ACCEPT", "udp", "any", 53]], ["udp", "1.1.1.1", 53], "DROP"], "expected": "ACCEPT"},
            ],
            "hint": "Для правила проверьте три условия (протокол, источник, порт); первое подошедшее возвращает своё действие.",
        },
        {
            "id": "net-parse-ss",
            "mode": "func",
            "func": "listening",
            "title": "Читаем вывод ss -tln",
            "statement": (
                "Напишите функцию listening(text): text — вывод 'ss -tlnp' (первая "
                "строка — заголовок). Для каждой строки состояния LISTEN возьмите "
                "4-е поле 'адрес:порт' (адрес может быть '0.0.0.0', '127.0.0.1', "
                "'[::]'; порт после последнего ':') и имя процесса из "
                "'users:((\"имя\",…))' (если нет — пустая строка). Верните список "
                "[порт, адрес, процесс], отсортированный по порту, затем по адресу."
            ),
            "starter": "import re\n\n\ndef listening(text):\n    pass\n",
            "tests": [
                {"args": ["State  Recv-Q Send-Q Local Address:Port Peer Address:Port Process\nLISTEN 0 128 0.0.0.0:22 0.0.0.0:* users:((\"sshd\",pid=812,fd=3))\nLISTEN 0 511 [::]:80 [::]:* users:((\"nginx\",pid=900,fd=6))\nESTAB 0 0 10.0.0.5:22 10.0.0.9:50000\nLISTEN 0 4096 127.0.0.1:5432 0.0.0.0:*\n"], "expected": [[22, "0.0.0.0", "sshd"], [80, "[::]", "nginx"], [5432, "127.0.0.1", ""]]},
                {"args": ["State Recv-Q Send-Q Local Address:Port Peer Address:Port Process\n"], "expected": []},
                {"args": ["State Recv-Q Send-Q Local Address:Port Peer Address:Port Process\nLISTEN 0 1 127.0.0.1:8080 0.0.0.0:* users:((\"python3\",pid=1,fd=3))\nLISTEN 0 1 0.0.0.0:8080 0.0.0.0:*\n"], "expected": [[8080, "0.0.0.0", ""], [8080, "127.0.0.1", "python3"]]},
            ],
            "hint": "Адрес и порт делятся по последнему ':' (в IPv6 двоеточий много); имя процесса — регулярным выражением.",
        },
        {
            "id": "net-dns-resolve",
            "mode": "func",
            "func": "dns_resolve",
            "title": "Разрешение имён через CNAME",
            "statement": (
                "Напишите функцию dns_resolve(records, name): records — список "
                "[имя, тип, значение], тип 'A' или 'CNAME'. Для name идите по "
                "цепочке CNAME до имени с записями A и верните список их значений "
                "(в порядке записей). Если A-записей нет — 'NXDOMAIN'. Если цепочка "
                "CNAME зацикливается или длиннее 8 переходов — 'CNAME loop'."
            ),
            "starter": "def dns_resolve(records, name):\n    pass\n",
            "tests": [
                {"args": [[["www.example.com", "CNAME", "web.example.com"], ["web.example.com", "A", "1.2.3.4"], ["web.example.com", "A", "1.2.3.5"]], "www.example.com"], "expected": ["1.2.3.4", "1.2.3.5"]},
                {"args": [[["a", "CNAME", "b"], ["b", "CNAME", "a"]], "a"], "expected": "CNAME loop"},
                {"args": [[], "nothing"], "expected": "NXDOMAIN"},
                {"args": [[["x", "A", "9.9.9.9"]], "x"], "expected": ["9.9.9.9"]},
                {"args": [[["a", "CNAME", "b"]], "a"], "expected": "NXDOMAIN"},
                {"args": [[["a", "CNAME", "b"], ["b", "CNAME", "c"], ["c", "A", "7.7.7.7"]], "a"], "expected": ["7.7.7.7"]},
                {"args": [[["n0", "CNAME", "n1"], ["n1", "CNAME", "n2"], ["n2", "CNAME", "n3"], ["n3", "CNAME", "n4"], ["n4", "CNAME", "n5"], ["n5", "CNAME", "n6"], ["n6", "CNAME", "n7"], ["n7", "CNAME", "n8"], ["n8", "CNAME", "n9"], ["n9", "CNAME", "n10"], ["n10", "A", "1.1.1.1"]], "n0"], "expected": "CNAME loop"},
            ],
            "hint": "Идите по словарю CNAME, храня посещённые имена; на каждом шаге сначала проверяйте A-записи.",
        },
        {
            "id": "net-fragments",
            "mode": "func",
            "func": "fragments",
            "title": "Фрагментация пакета",
            "statement": (
                "Напишите функцию fragments(total_len, mtu): IP-пакет длиной "
                "total_len байт (включая заголовок 20 байт) надо передать по каналу "
                "с MTU mtu. Если он помещается — верните [total_len − 20] (размер "
                "данных). Иначе разбейте данные на фрагменты: в каждом (кроме "
                "последнего) данных ((mtu − 20) // 8) · 8 байт; верните список "
                "размеров данных фрагментов."
            ),
            "starter": "def fragments(total_len, mtu):\n    pass\n",
            "tests": [
                {"args": [1500, 1500], "expected": [1480]},
                {"args": [4000, 1500], "expected": [1480, 1480, 1020]},
                {"args": [3000, 1500], "expected": [1480, 1480, 20]},
                {"args": [1521, 1500], "expected": [1480, 21]},
                {"args": [100, 576], "expected": [80]},
                {"args": [65535, 1500], "expected": [1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 1480, 395]},
                {"args": [1500, 1280], "expected": [1256, 224]},
            ],
            "hint": "Данных в одном фрагменте — наибольшее кратное 8, не превышающее mtu − 20.",
        },
    ],
}
