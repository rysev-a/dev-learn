"""Задачи книги «Linux: от шелла до ядра»: главы 7–8."""

TASKS: dict[int, list[dict]] = {
    7: [
        {
            "id": "disk-partition-plan",
            "mode": "func",
            "func": "partition_plan",
            "title": "Разметка диска",
            "statement": (
                "Напишите функцию partition_plan(disk_mib, sizes): диск на disk_mib "
                "МиБ. Первый МиБ занят таблицей разделов (разделы начинаются с "
                "отметки 1). sizes — размеры разделов по порядку в МиБ; значение "
                "'rest' означает «всё оставшееся» и бывает только последним. "
                "Верните список [начало, конец) каждого раздела (конец не "
                "включается) либо строку 'no space', если разделы не помещаются или "
                "для 'rest' не осталось места."
            ),
            "starter": "def partition_plan(disk_mib, sizes):\n    pass\n",
            "tests": [
                {"args": [1024, [512, 256]], "expected": [[1, 513], [513, 769]]},
                {"args": [1024, [512, "rest"]], "expected": [[1, 513], [513, 1024]]},
                {"args": [1024, [1024]], "expected": "no space"},
                {"args": [1024, [1023]], "expected": [[1, 1024]]},
                {"args": [1024, [1023, "rest"]], "expected": "no space"},
                {"args": [10, []], "expected": []},
                {"args": [100, [10, 20, 30, "rest"]], "expected": [[1, 11], [11, 31], [31, 61], [61, 100]]},
                {"args": [2048, ["rest"]], "expected": [[1, 2048]]},
                {"args": [1, ["rest"]], "expected": "no space"},
            ],
            "hint": "Текущая позиция pos начинается с 1; 'rest' = disk_mib − pos; проверяйте выход за конец диска.",
        },
        {
            "id": "disk-lvm-plan",
            "mode": "func",
            "func": "lvm_plan",
            "title": "Тома LVM: экстенты",
            "statement": (
                "Напишите функцию lvm_plan(pe_mib, pvs_mib, lvs): группа томов "
                "собирается из физических дисков pvs_mib (МиБ); каждый диск вносит "
                "целое число экстентов размера pe_mib (остаток пропадает). lvs — "
                "список [имя, размер_МиБ]: размер округляется вверх до целого числа "
                "экстентов. Верните кортеж ([[имя, экстентов], …], "
                "свободных_экстентов) или строку 'insufficient space', если "
                "экстентов не хватает."
            ),
            "starter": "def lvm_plan(pe_mib, pvs_mib, lvs):\n    pass\n",
            "tests": [
                {"args": [4, [100, 50], [["root", 60], ["home", 41]]], "expected": ([["root", 15], ["home", 11]], 11)},
                {"args": [4, [100, 50], [["root", 150]]], "expected": "insufficient space"},
                {"args": [4, [10], [["a", 1]]], "expected": ([["a", 1]], 1)},
                {"args": [4, [3], [["a", 1]]], "expected": "insufficient space"},
                {"args": [32, [1000, 1000], [["data", 1500], ["log", 400]]], "expected": ([["data", 47], ["log", 13]], 2)},
                {"args": [4, [], []], "expected": ([], 0)},
                {"args": [4, [100], []], "expected": ([], 25)},
            ],
            "hint": "Экстентов в диске — pv // pe; в томе — потолок размер / pe.",
        },
        {
            "id": "disk-raid-info",
            "mode": "func",
            "func": "raid_info",
            "title": "Ёмкость и надёжность RAID",
            "statement": (
                "Напишите функцию raid_info(level, disks, size_gb): level — "
                "'raid0', 'raid1', 'raid5', 'raid6' или 'raid10'; disks — число "
                "дисков одинакового размера size_gb. Верните кортеж "
                "(полезная_ёмкость_ГБ, гарантированно_переживаемых_отказов). raid0: "
                "диски·размер, 0; raid1 (все диски — зеркала): размер, disks − 1; "
                "raid5: (disks − 1)·размер, 1; raid6: (disks − 2)·размер, 2; raid10 "
                "(зеркала в полосе): disks / 2 · размер, 1. Минимумы дисков: raid0 "
                "— 2, raid1 — 2, raid5 — 3, raid6 — 4, raid10 — 4 и чётное число; "
                "иначе верните None."
            ),
            "starter": "def raid_info(level, disks, size_gb):\n    pass\n",
            "tests": [
                {"args": ["raid0", 4, 1000], "expected": (4000, 0)},
                {"args": ["raid1", 2, 2000], "expected": (2000, 1)},
                {"args": ["raid1", 3, 2000], "expected": (2000, 2)},
                {"args": ["raid5", 4, 1000], "expected": (3000, 1)},
                {"args": ["raid5", 2, 1000], "expected": None},
                {"args": ["raid6", 6, 4000], "expected": (16000, 2)},
                {"args": ["raid6", 3, 4000], "expected": None},
                {"args": ["raid10", 6, 1000], "expected": (3000, 1)},
                {"args": ["raid10", 5, 1000], "expected": None},
                {"args": ["raid10", 2, 1000], "expected": None},
                {"args": ["raid0", 1, 500], "expected": None},
            ],
            "hint": "Проверка условий — отдельным if на каждый уровень; в остальных случаях None.",
        },
        {
            "id": "disk-raid5-layout",
            "mode": "func",
            "func": "raid5_layout",
            "title": "Раскладка RAID-5",
            "statement": (
                "Напишите функцию raid5_layout(disks, stripes): раскладка "
                "«слева-симметричная». В полосе i блок чётности 'P' лежит на диске "
                "(disks − 1 − i) mod disks; блоки данных полосы идут по кругу, "
                "начиная со следующего за чётностью диска: j-й блок полосы (j от 0 "
                "до disks − 2) — на диске (p + 1 + j) mod disks, подпись 'D' + "
                "номер, где номер = i·(disks − 1) + j. Верните список строк (по "
                "полосам) из disks подписей."
            ),
            "starter": "def raid5_layout(disks, stripes):\n    pass\n",
            "tests": [
                {"args": [3, 3], "expected": [["D0", "D1", "P"], ["D3", "P", "D2"], ["P", "D4", "D5"]]},
                {"args": [4, 5], "expected": [["D0", "D1", "D2", "P"], ["D4", "D5", "P", "D3"], ["D8", "P", "D6", "D7"], ["P", "D9", "D10", "D11"], ["D12", "D13", "D14", "P"]]},
                {"args": [3, 0], "expected": []},
                {"args": [5, 2], "expected": [["D0", "D1", "D2", "D3", "P"], ["D5", "D6", "D7", "P", "D4"]]},
                {"args": [3, 6], "expected": [["D0", "D1", "P"], ["D3", "P", "D2"], ["P", "D4", "D5"], ["D6", "D7", "P"], ["D9", "P", "D8"], ["P", "D10", "D11"]]},
            ],
            "hint": "Четность «ходит» влево по дискам с каждой полосой; данные заполняют остальные места по кругу.",
        },
        {
            "id": "disk-rsync-plan",
            "mode": "func",
            "func": "rsync_plan",
            "title": "Что скопирует rsync",
            "statement": (
                "Напишите функцию rsync_plan(src, dst, delete): src и dst — словари "
                "«путь → [размер, время_изменения]». rsync копирует файл, если его "
                "нет в dst или различается размер или время. Верните словарь "
                "{'copy': отсортированные пути, 'delete': отсортированные пути}: в "
                "'delete' — файлы, которых нет в src (только если delete=True, "
                "иначе пустой список)."
            ),
            "starter": "def rsync_plan(src, dst, delete):\n    pass\n",
            "tests": [
                {"args": [{"a": [10, 100], "b": [20, 100]}, {"a": [10, 100], "c": [5, 1]}, True], "expected": {"copy": ["b"], "delete": ["c"]}},
                {"args": [{"a": [10, 100], "b": [20, 100]}, {"a": [10, 100], "c": [5, 1]}, False], "expected": {"copy": ["b"], "delete": []}},
                {"args": [{"a": [10, 101]}, {"a": [10, 100]}, False], "expected": {"copy": ["a"], "delete": []}},
                {"args": [{}, {}, True], "expected": {"copy": [], "delete": []}},
                {"args": [{"x": [1, 1]}, {}, True], "expected": {"copy": ["x"], "delete": []}},
                {"args": [{}, {"old": [1, 1]}, True], "expected": {"copy": [], "delete": ["old"]}},
            ],
            "hint": "Сравните списки значений [размер, mtime] — они равны, только если оба числа совпали.",
        },
        {
            "id": "disk-backup-retention",
            "mode": "func",
            "func": "keep_backups",
            "title": "Хранение бэкапов",
            "statement": (
                "Напишите функцию keep_backups(days, daily, weekly, monthly): days "
                "— номера дней, в которые есть бэкапы (по возрастанию). Оставьте: "
                "daily самых новых бэкапов; по одному (самому новому) бэкапу из "
                "каждой из weekly последних недель, где неделя = день // 7; по "
                "одному из каждого из monthly последних месяцев, где месяц = день "
                "// 30. «Последние» считаются среди недель/месяцев, в которых есть "
                "бэкапы. Верните отсортированный список дней, которые нужно "
                "сохранить."
            ),
            "starter": "def keep_backups(days, daily, weekly, monthly):\n    pass\n",
            "tests": [
                {"args": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59], 3, 2, 1], "expected": [55, 57, 58, 59]},
                {"args": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 0, 0], "expected": []},
                {"args": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 20, 0, 0], "expected": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]},
                {"args": [[0, 7, 14, 21, 28, 35], 1, 3, 0], "expected": [21, 28, 35]},
                {"args": [[1, 2, 3, 40, 41, 80], 1, 0, 3], "expected": [3, 41, 80]},
                {"args": [[], 3, 3, 3], "expected": []},
                {"args": [[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95], 2, 4, 2], "expected": [75, 80, 85, 90, 95]},
            ],
            "hint": "Для недель и месяцев: словарь «номер периода → самый новый день»; затем возьмите последние count периодов.",
        },
        {
            "id": "disk-backup-321",
            "mode": "func",
            "func": "check_321",
            "title": "Правило 3-2-1",
            "statement": (
                "Напишите функцию check_321(copies): copies — список копий данных, "
                "каждая {'medium': 'disk'|'tape'|'cloud'|…, 'offsite': True/False}. "
                "Правило 3-2-1: минимум 3 копии; минимум 2 разных типа носителей; "
                "минимум 1 копия вне площадки. Верните список нарушенных правил "
                "среди 'copies', 'media', 'offsite' (в этом порядке); пустой — всё "
                "в порядке."
            ),
            "starter": "def check_321(copies):\n    pass\n",
            "tests": [
                {"args": [[{"medium": "disk", "offsite": False}, {"medium": "tape", "offsite": False}, {"medium": "cloud", "offsite": True}]], "expected": []},
                {"args": [[{"medium": "disk", "offsite": False}, {"medium": "disk", "offsite": False}]], "expected": ["copies", "media", "offsite"]},
                {"args": [[]], "expected": ["copies", "media", "offsite"]},
                {"args": [[{"medium": "disk", "offsite": True}, {"medium": "disk", "offsite": True}, {"medium": "disk", "offsite": True}]], "expected": ["media"]},
                {"args": [[{"medium": "disk", "offsite": False}, {"medium": "cloud", "offsite": False}, {"medium": "tape", "offsite": False}]], "expected": ["offsite"]},
            ],
            "hint": "Три независимых проверки: len(copies), число различных media и any(offsite).",
        },
        {
            "id": "disk-smart",
            "mode": "func",
            "func": "smart_health",
            "title": "Здоровье диска по SMART",
            "statement": (
                "Напишите функцию smart_health(attrs): attrs — список [имя, "
                "нормализованное_значение, порог, сырое_значение]. Диск 'FAIL', "
                "если у какого-то атрибута значение не больше порога (и порог > 0); "
                "иначе 'WARN', если сырое число в одном из атрибутов "
                "'Reallocated_Sector_Ct', 'Current_Pending_Sector' или "
                "'Offline_Uncorrectable' больше нуля; иначе 'OK'."
            ),
            "starter": "def smart_health(attrs):\n    pass\n",
            "tests": [
                {"args": [[["Reallocated_Sector_Ct", 100, 10, 0], ["Power_On_Hours", 95, 0, 12000]]], "expected": "OK"},
                {"args": [[["Reallocated_Sector_Ct", 100, 10, 8]]], "expected": "WARN"},
                {"args": [[["Reallocated_Sector_Ct", 10, 10, 800]]], "expected": "FAIL"},
                {"args": [[["Current_Pending_Sector", 200, 0, 3]]], "expected": "WARN"},
                {"args": [[]], "expected": "OK"},
                {"args": [[["Spin_Retry_Count", 90, 97, 0]]], "expected": "FAIL"},
                {"args": [[["Temperature_Celsius", 30, 0, 30], ["Offline_Uncorrectable", 100, 0, 1]]], "expected": "WARN"},
            ],
            "hint": "Сначала ищем критические атрибуты (FAIL), потом предупреждения (WARN).",
        },
    ],
    8: [
        {
            "id": "pkg-compare-versions",
            "mode": "func",
            "func": "cmp_versions",
            "title": "Сравнение версий",
            "statement": (
                "Напишите функцию cmp_versions(a, b): -1, 0 или 1. Версия — числа "
                "через точку ('1.2.10') и, возможно, предрелизный суффикс после '-' "
                "('2.0-rc1'). Числовые части сравниваются как числа (1.10 > 1.9), "
                "недостающие считаются нулём (1.0 == 1.0.0). При равных числах "
                "предрелиз меньше релиза; два предрелиза сравниваются как строки."
            ),
            "starter": "def cmp_versions(a, b):\n    pass\n",
            "tests": [
                {"args": ["1.2.10", "1.2.9"], "expected": 1},
                {"args": ["1.0", "1.0.0"], "expected": 0},
                {"args": ["2.0-rc1", "2.0"], "expected": -1},
                {"args": ["2.0-rc2", "2.0-rc1"], "expected": 1},
                {"args": ["1.10", "1.9"], "expected": 1},
                {"args": ["3", "3.0.1"], "expected": -1},
                {"args": ["2.0", "2.0-beta"], "expected": 1},
                {"args": ["1.0-alpha", "1.0-beta"], "expected": -1},
                {"args": ["0.9.9", "1.0"], "expected": -1},
            ],
            "hint": "Разберите версию на (список чисел, предрелиз); дополните числа нулями до равной длины.",
        },
        {
            "id": "pkg-satisfies",
            "mode": "func",
            "func": "satisfies",
            "title": "Ограничения версий",
            "statement": (
                "Напишите функцию satisfies(version, constraint): constraint — "
                "условия через запятую: '>=1.2', '<2.0', '==1.5', '!=1.3', '>1', "
                "'<=3.1'; либо '^1.2.3' (≥1.2.3 и <2.0.0), либо '~1.2.3' (≥1.2.3 и "
                "<1.3.0). Предрелизных суффиксов в тестах нет. Верните True/False."
            ),
            "starter": "def satisfies(version, constraint):\n    pass\n",
            "tests": [
                {"args": ["1.5", ">=1.2,<2.0"], "expected": True},
                {"args": ["2.0", ">=1.2,<2.0"], "expected": False},
                {"args": ["1.2", ">=1.2"], "expected": True},
                {"args": ["1.1.9", ">=1.2"], "expected": False},
                {"args": ["1.5", "==1.5.0"], "expected": True},
                {"args": ["1.3", "!=1.3"], "expected": False},
                {"args": ["1.9.9", "^1.2.3"], "expected": True},
                {"args": ["2.0.0", "^1.2.3"], "expected": False},
                {"args": ["1.2.2", "^1.2.3"], "expected": False},
                {"args": ["1.2.9", "~1.2.3"], "expected": True},
                {"args": ["1.3.0", "~1.2.3"], "expected": False},
                {"args": ["3.1", "<=3.1,>2"], "expected": True},
            ],
            "hint": "Каждое условие — пара (операция, версия); сравнение версий — по спискам чисел с дополнением нулями.",
        },
        {
            "id": "pkg-install-order",
            "mode": "func",
            "func": "install_order",
            "title": "Порядок установки",
            "statement": (
                "Напишите функцию install_order(repo, want): repo — словарь «пакет "
                "→ список зависимостей», want — список пакетов, которые просит "
                "пользователь. Верните список пакетов в порядке установки (сначала "
                "зависимости; если несколько пакетов можно ставить, берите по "
                "алфавиту), включая все транзитивные зависимости. Если пакета или "
                "зависимости нет в repo — строка 'missing: имя' (первое по алфавиту "
                "отсутствующее); если есть цикл — 'cycle'."
            ),
            "starter": "import heapq\n\n\ndef install_order(repo, want):\n    pass\n",
            "tests": [
                {"args": [{"app": ["lib", "db"], "lib": ["libc"], "db": ["libc"], "libc": []}, ["app"]], "expected": ["libc", "db", "lib", "app"]},
                {"args": [{"a": [], "b": ["a"]}, ["b", "a"]], "expected": ["a", "b"]},
                {"args": [{"a": ["ghost"]}, ["a"]], "expected": "missing: ghost"},
                {"args": [{"a": ["b"], "b": ["a"]}, ["a"]], "expected": "cycle"},
                {"args": [{}, []], "expected": []},
                {"args": [{"x": []}, ["y"]], "expected": "missing: y"},
                {"args": [{"z": [], "y": [], "app": ["z", "y"]}, ["app"]], "expected": ["y", "z", "app"]},
            ],
            "hint": "Сначала соберите замыкание зависимостей, затем топологическая сортировка с кучей (алфавит среди готовых).",
        },
        {
            "id": "pkg-autoremove",
            "mode": "func",
            "func": "autoremove",
            "title": "autoremove: осиротевшие пакеты",
            "statement": (
                "Напишите функцию autoremove(installed, manual): installed — "
                "словарь «пакет → список зависимостей» для всех установленных; "
                "manual — список пакетов, поставленных вручную. Пакет нужен, если "
                "он в manual или от него транзитивно зависит какой-то нужный пакет. "
                "Верните отсортированный список ненужных (их можно удалить)."
            ),
            "starter": "def autoremove(installed, manual):\n    pass\n",
            "tests": [
                {"args": [{"app": ["lib"], "lib": [], "oldlib": [], "tool": ["oldlib"]}, ["app"]], "expected": ["oldlib", "tool"]},
                {"args": [{"a": [], "b": []}, []], "expected": ["a", "b"]},
                {"args": [{"a": ["b"], "b": ["a"]}, []], "expected": ["a", "b"]},
                {"args": [{"a": ["b"], "b": ["a"], "c": []}, ["a"]], "expected": ["c"]},
                {"args": [{}, ["x"]], "expected": []},
                {"args": [{"x": ["y"], "y": ["z"], "z": []}, ["x", "z"]], "expected": []},
            ],
            "hint": "Обход в глубину от вручную установленных; всё, что не достигнуто, можно удалять.",
        },
        {
            "id": "pkg-resolve-versions",
            "mode": "func",
            "func": "resolve",
            "title": "Подбор версий (resolver)",
            "statement": (
                "Напишите функцию resolve(available, requires): available — словарь "
                "«пакет → список версий»; версия — {'version': '1.2', 'deps': "
                "{'пакет': 'ограничение'}} (ограничения: '>=1.0', '<2.0', '==1.5', "
                "через запятую). requires — {'пакет': 'ограничение'} от "
                "пользователя. Подберите для каждого нужного пакета версию так, "
                "чтобы все ограничения выполнялись, предпочитая более новые версии "
                "(с откатом назад при неудаче). Верните словарь «пакет → версия» "
                "(только нужные пакеты) или None, если решения нет."
            ),
            "starter": "def resolve(available, requires):\n    pass\n",
            "tests": [
                {"args": [{"app": [{"version": "2.0", "deps": {"lib": ">=2.0"}}, {"version": "1.0", "deps": {"lib": ">=1.0,<2.0"}}], "lib": [{"version": "2.1", "deps": {}}, {"version": "1.5", "deps": {}}]}, {"app": ">=1.0"}], "expected": {"app": "2.0", "lib": "2.1"}},
                {"args": [{"app": [{"version": "2.0", "deps": {"lib": ">=2.0"}}, {"version": "1.0", "deps": {"lib": "<2.0"}}], "lib": [{"version": "1.5", "deps": {}}]}, {"app": ">=1.0"}], "expected": {"app": "1.0", "lib": "1.5"}},
                {"args": [{"a": [{"version": "1", "deps": {"b": "==1"}}], "b": [{"version": "2", "deps": {}}]}, {"a": ">=1"}], "expected": None},
                {"args": [{"a": [{"version": "1", "deps": {}}]}, {"a": ">=2"}], "expected": None},
                {"args": [{}, {}], "expected": {}},
                {"args": [{"a": [{"version": "1", "deps": {}}]}, {"ghost": ">=1"}], "expected": None},
                {"args": [{"x": [{"version": "3", "deps": {"y": "<2"}}, {"version": "2", "deps": {"y": "<3"}}], "y": [{"version": "2", "deps": {}}, {"version": "1", "deps": {}}]}, {"x": ">=2", "y": ">=2"}], "expected": {"x": "2", "y": "2"}},
            ],
            "hint": "Рекурсивный поиск с откатом: выбираем версию пакета (новые первыми), добавляем её ограничения, идём дальше; если тупик — пробуем следующую версию.",
        },
        {
            "id": "pkg-parse-control",
            "mode": "func",
            "func": "parse_control",
            "title": "Файл control пакета",
            "statement": (
                "Напишите функцию parse_control(text): текст из абзацев (разделены "
                "пустой строкой), каждый — поля 'Ключ: значение'. Строка, "
                "начинающаяся с пробела, — продолжение значения предыдущего поля (в "
                "значение добавляется '\\n' и строка без начальных пробелов). "
                "Верните список словарей по абзацам."
            ),
            "starter": "def parse_control(text):\n    pass\n",
            "tests": [
                {"args": ["Package: nginx\nVersion: 1.24\nDepends: libc6 (>= 2.34), libssl3\nDescription: web server\n small and fast\n high load\n\nPackage: curl\nVersion: 8.0\n"], "expected": [{"Package": "nginx", "Version": "1.24", "Depends": "libc6 (>= 2.34), libssl3", "Description": "web server\nsmall and fast\nhigh load"}, {"Package": "curl", "Version": "8.0"}]},
                {"args": [""], "expected": []},
                {"args": ["A: 1\n\n\n\nB: 2\n"], "expected": [{"A": "1"}, {"B": "2"}]},
                {"args": ["Package: x\nDescription: one\n two\n"], "expected": [{"Package": "x", "Description": "one\ntwo"}]},
                {"args": ["Key: value: with colon\n"], "expected": [{"Key": "value: with colon"}]},
            ],
            "hint": "Накапливайте поля текущего абзаца; пустая строка закрывает абзац; продолжение приклеивается к последнему ключу.",
        },
        {
            "id": "pkg-upgrade-plan",
            "mode": "func",
            "func": "upgrade_plan",
            "title": "Что обновит upgrade",
            "statement": (
                "Напишите функцию upgrade_plan(installed, repo): словари «пакет → "
                "версия». Версии — числа через точку (1.10 > 1.9; недостающие числа "
                "— нули). Верните отсортированный по имени список [пакет, "
                "установленная, новая] для установленных пакетов, у которых в "
                "репозитории версия новее. Пакеты, которых нет в репозитории, "
                "пропускайте."
            ),
            "starter": "def upgrade_plan(installed, repo):\n    pass\n",
            "tests": [
                {"args": [{"a": "1.9", "b": "2.0", "c": "1.0"}, {"a": "1.10", "b": "2.0.0", "d": "9"}], "expected": [["a", "1.9", "1.10"]]},
                {"args": [{}, {"a": "1"}], "expected": []},
                {"args": [{"a": "1"}, {}], "expected": []},
                {"args": [{"z": "0.9.9", "y": "1.0"}, {"z": "1.0", "y": "0.9"}], "expected": [["z", "0.9.9", "1.0"]]},
                {"args": [{"x": "1.0"}, {"x": "1.0.1"}], "expected": [["x", "1.0", "1.0.1"]]},
            ],
            "hint": "Сравнивайте версии как списки чисел (а не как строки).",
        },
        {
            "id": "pkg-missing-libs",
            "mode": "func",
            "func": "find_libs",
            "title": "Поиск разделяемых библиотек",
            "statement": (
                "Напишите функцию find_libs(needed, env_paths, default_paths, "
                "files): для каждой библиотеки из needed загрузчик ищет файл "
                "'каталог/имя' сначала в env_paths (LD_LIBRARY_PATH), потом в "
                "default_paths, по порядку; files — множество (список) существующих "
                "полных путей. Верните словарь {'found': {имя: путь}, 'missing': "
                "отсортированные имена}."
            ),
            "starter": "def find_libs(needed, env_paths, default_paths, files):\n    pass\n",
            "tests": [
                {"args": [["libc.so.6", "libssl.so.3", "libz.so.1"], ["/opt/lib"], ["/lib", "/usr/lib"], ["/lib/libc.so.6", "/usr/lib/libssl.so.3", "/opt/lib/libssl.so.3"]], "expected": {"found": {"libc.so.6": "/lib/libc.so.6", "libssl.so.3": "/opt/lib/libssl.so.3"}, "missing": ["libz.so.1"]}},
                {"args": [[], [], ["/lib"], []], "expected": {"found": {}, "missing": []}},
                {"args": [["libx.so"], [], ["/lib"], []], "expected": {"found": {}, "missing": ["libx.so"]}},
                {"args": [["libx.so"], ["/a", "/b"], ["/lib"], ["/b/libx.so", "/lib/libx.so"]], "expected": {"found": {"libx.so": "/b/libx.so"}, "missing": []}},
                {"args": [["liby.so"], [], ["/lib/", "/usr/lib"], ["/lib/liby.so"]], "expected": {"found": {"liby.so": "/lib/liby.so"}, "missing": []}},
            ],
            "hint": "Для каждой библиотеки перебирайте каталоги в порядке приоритета; for/else удобен для «не нашли».",
        },
    ],
}
