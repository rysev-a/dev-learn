"""Задачи книги «Linux: от шелла до ядра»: главы 9–10."""

TASKS: dict[int, list[dict]] = {
    9: [
        {
            "id": "ct-cgroup-oom",
            "mode": "func",
            "func": "cgroup_oom",
            "title": "Лимит памяти контрольной группы",
            "statement": (
                "Напишите функцию cgroup_oom(events, limit): группа ограничена "
                "limit МБ. События: ['alloc', процесс, МБ] — процесс получает "
                "память; ['free', процесс, МБ] — освобождает (но не ниже нуля). "
                "Если после 'alloc' сумма превысила limit, ядро убивает процессы с "
                "наибольшим расходом (при равенстве — с меньшим именем по "
                "алфавиту), пока сумма не станет ≤ limit; убитый процесс исчезает "
                "из учёта. Верните кортеж (убитые_по_порядку, словарь «процесс → "
                "МБ» оставшихся)."
            ),
            "starter": "def cgroup_oom(events, limit):\n    pass\n",
            "tests": [
                {"args": [[["alloc", "web", 300], ["alloc", "db", 500], ["alloc", "cache", 300]], 1000], "expected": (["db"], {"web": 300, "cache": 300})},
                {"args": [[["alloc", "a", 600], ["alloc", "b", 600]], 1000], "expected": (["a"], {"b": 600})},
                {"args": [[["alloc", "a", 1500]], 1000], "expected": (["a"], {})},
                {"args": [[["alloc", "a", 400], ["free", "a", 100], ["alloc", "b", 700]], 1000], "expected": ([], {"a": 300, "b": 700})},
                {"args": [[["alloc", "x", 500], ["alloc", "y", 500], ["alloc", "z", 1]], 1000], "expected": (["x"], {"y": 500, "z": 1})},
                {"args": [[], 100], "expected": ([], {})},
                {"args": [[["alloc", "a", 100], ["free", "a", 500], ["alloc", "a", 50]], 1000], "expected": ([], {"a": 50})},
                {"args": [[["alloc", "m", 700], ["alloc", "n", 700], ["alloc", "o", 700]], 1000], "expected": (["m", "n"], {"o": 700})},
            ],
            "hint": "После каждого alloc, пока сумма > limit, выбирайте жертву по ключу (−расход, имя) и удаляйте её из словаря.",
        },
        {
            "id": "ct-cpu-quota",
            "mode": "func",
            "func": "cpu_quota",
            "title": "Квота процессора (CFS bandwidth)",
            "statement": (
                "Напишите функцию cpu_quota(quota_ms, period_ms, work_ms): "
                "контейнеру разрешено quota_ms миллисекунд процессорного времени в "
                "каждом периоде длиной period_ms (quota_ms ≤ period_ms), остаток "
                "периода он «заморожен». Ему нужно выполнить work_ms миллисекунд "
                "работы. Верните кортеж (число_периодов, момент_окончания_в_мс); "
                "при work_ms = 0 — (0, 0)."
            ),
            "starter": "def cpu_quota(quota_ms, period_ms, work_ms):\n    pass\n",
            "tests": [
                {"args": [50, 100, 120], "expected": (3, 220)},
                {"args": [50, 100, 100], "expected": (2, 150)},
                {"args": [100, 100, 30], "expected": (1, 30)},
                {"args": [25, 100, 0], "expected": (0, 0)},
                {"args": [10, 100, 5], "expected": (1, 5)},
                {"args": [20, 50, 100], "expected": (5, 220)},
                {"args": [1, 10, 7], "expected": (7, 61)},
            ],
            "hint": "Целых периодов с полной квотой — (work − 1) // quota; последний период — остаток работы.",
        },
        {
            "id": "ct-cpu-allocation",
            "mode": "func",
            "func": "cpu_allocation",
            "title": "Доли процессора контейнеров",
            "statement": (
                "Напишите функцию cpu_allocation(shares, caps): shares — словарь "
                "«контейнер → вес» (cpu.shares), caps — словарь «контейнер → "
                "максимальная доля процессора» (0…1; есть не у всех). Все "
                "контейнеры загружены. Весь процессор = 1.0 делится пропорционально "
                "весам, но никто не получает больше своего предела; освободившееся "
                "делится между остальными пропорционально весам (повторяйте, пока "
                "кто-то превышает предел). Верните словарь «контейнер → доля», "
                "округлённую до 3 знаков."
            ),
            "starter": "def cpu_allocation(shares, caps):\n    pass\n",
            "tests": [
                {"args": [{"a": 1024, "b": 1024}, {}], "expected": {"a": 0.5, "b": 0.5}},
                {"args": [{"a": 1024, "b": 512, "c": 512}, {}], "expected": {"a": 0.5, "b": 0.25, "c": 0.25}},
                {"args": [{"a": 1024, "b": 1024}, {"a": 0.25}], "expected": {"a": 0.25, "b": 0.75}},
                {"args": [{"a": 1, "b": 1, "c": 2}, {"c": 0.3, "a": 0.1}], "expected": {"a": 0.1, "c": 0.3, "b": 0.6}},
                {"args": [{"only": 100}, {"only": 0.5}], "expected": {"only": 0.5}},
                {"args": [{}, {}], "expected": {}},
                {"args": [{"a": 1, "b": 1, "c": 1}, {"a": 0.2, "b": 0.2}], "expected": {"a": 0.2, "b": 0.2, "c": 0.6}},
            ],
            "hint": "Прогрессивное заполнение: считаем доли, превысившим предел назначаем предел и пересчитываем остальных на оставшееся.",
        },
        {
            "id": "ct-overlay",
            "mode": "func",
            "func": "overlay",
            "title": "Слои образа (overlayfs)",
            "statement": (
                "Напишите функцию overlay(layers): layers — слои образа снизу "
                "вверх; слой — словарь «путь → содержимое». Верхний слой "
                "перекрывает нижние. Значение None — «белое поле» (whiteout): файл "
                "с этим путём удалён; если путь оканчивается на '/', удаляются все "
                "файлы, путь которых начинается с него. Верните итоговый вид — "
                "словарь «путь → содержимое» без удалённых."
            ),
            "starter": "def overlay(layers):\n    pass\n",
            "tests": [
                {"args": [[{"/etc/a": "1", "/bin/x": "x"}, {"/etc/a": "2", "/etc/b": "b"}]], "expected": {"/etc/a": "2", "/bin/x": "x", "/etc/b": "b"}},
                {"args": [[{"/a": "1", "/b": "2"}, {"/a": None}]], "expected": {"/b": "2"}},
                {"args": [[{"/data/x": "1", "/data/y": "2", "/keep": "k"}, {"/data/": None}]], "expected": {"/keep": "k"}},
                {"args": [[{"/a": "1"}, {"/a": None}, {"/a": "again"}]], "expected": {"/a": "again"}},
                {"args": [[]], "expected": {}},
                {"args": [[{"/x": None}]], "expected": {}},
                {"args": [[{"/d/1": "1"}, {"/d/": None}, {"/d/2": "2"}]], "expected": {"/d/2": "2"}},
            ],
            "hint": "Идите по слоям снизу вверх, обновляя общий словарь; None — удаление (для каталогов — по префиксу).",
        },
        {
            "id": "ct-layer-cache",
            "mode": "func",
            "func": "build_cache",
            "title": "Кэш слоёв при сборке",
            "statement": (
                "Напишите функцию build_cache(old, new): old и new — списки "
                "инструкций Dockerfile (строки; у COPY в строке уже учтён хеш "
                "файла). Слой берётся из кэша, пока инструкции совпадают с прошлой "
                "сборкой с самого начала; после первого отличия пересобирается всё "
                "остальное. Верните кортеж (взято_из_кэша, пересобрано)."
            ),
            "starter": "def build_cache(old, new):\n    pass\n",
            "tests": [
                {"args": [["FROM py", "COPY req #1", "RUN pip install", "COPY src #1", "CMD run"], ["FROM py", "COPY req #1", "RUN pip install", "COPY src #2", "CMD run"]], "expected": (3, 2)},
                {"args": [["FROM py", "COPY . #1", "RUN pip install"], ["FROM py", "COPY . #2", "RUN pip install"]], "expected": (1, 2)},
                {"args": [[], ["FROM py"]], "expected": (0, 1)},
                {"args": [["FROM a"], ["FROM a"]], "expected": (1, 0)},
                {"args": [["FROM a", "RUN x"], ["FROM b", "RUN x"]], "expected": (0, 2)},
                {"args": [["A", "B", "C"], ["A", "B"]], "expected": (2, 0)},
            ],
            "hint": "Длина общего префикса двух списков.",
        },
        {
            "id": "ct-image-disk",
            "mode": "func",
            "func": "image_disk",
            "title": "Диск под образы",
            "statement": (
                "Напишите функцию image_disk(images): images — список образов; "
                "образ — список слоёв [идентификатор, размер_МБ] (от нижнего к "
                "верхнему). Слои с одинаковым идентификатором хранятся один раз. "
                "Верните кортеж (реально_занято_МБ, "
                "список_размеров_образов_по_отдельности_если_бы_слои_не_делились)."
            ),
            "starter": "def image_disk(images):\n    pass\n",
            "tests": [
                {"args": [[[["base", 100], ["app1", 20]], [["base", 100], ["app2", 30]]]], "expected": (150, [120, 130])},
                {"args": [[]], "expected": (0, [])},
                {"args": [[[["a", 5]]]], "expected": (5, [5])},
                {"args": [[[["base", 100], ["x", 1]], [["base", 100], ["x", 1]]]], "expected": (101, [101, 101])},
                {"args": [[[["a", 10], ["b", 20]], [["b", 20], ["c", 30]], [["a", 10]]]], "expected": (60, [30, 50, 10])},
            ],
            "hint": "Словарь «идентификатор слоя → размер» даёт реальное место; сумма по образам — «виртуальный» размер.",
        },
        {
            "id": "ct-port-mappings",
            "mode": "func",
            "func": "parse_ports",
            "title": "Опция -p в docker run",
            "statement": (
                "Напишите функцию parse_ports(specs): specs — список строк опции "
                "-p: '8080:80', '127.0.0.1:5432:5432', '9000:9000/udp'. Формат: "
                "[адрес:]порт_хоста:порт_контейнера[/протокол]; адрес по умолчанию "
                "'0.0.0.0', протокол — 'tcp'. Верните список [адрес, порт_хоста "
                "(число), порт_контейнера (число), протокол]."
            ),
            "starter": "def parse_ports(specs):\n    pass\n",
            "tests": [
                {"args": [["8080:80", "127.0.0.1:5432:5432", "9000:9000/udp"]], "expected": [["0.0.0.0", 8080, 80, "tcp"], ["127.0.0.1", 5432, 5432, "tcp"], ["0.0.0.0", 9000, 9000, "udp"]]},
                {"args": [[]], "expected": []},
                {"args": [["443:8443/tcp"]], "expected": [["0.0.0.0", 443, 8443, "tcp"]]},
                {"args": [["10.0.0.5:53:53/udp"]], "expected": [["10.0.0.5", 53, 53, "udp"]]},
            ],
            "hint": "Сначала отделите протокол по '/', затем разбейте по ':' — два или три поля.",
        },
        {
            "id": "ct-pick-tag",
            "mode": "func",
            "func": "pick_tag",
            "title": "Плавающие теги образов",
            "statement": (
                "Напишите функцию pick_tag(tags, wanted): tags — теги образа в "
                "реестре. Если wanted есть среди тегов — вернуть его. 'latest' "
                "(если такого тега нет) — самый большой по версии из тегов вида "
                "x.y.z (числа через точку). Если wanted — «короткая» версия ('1' "
                "или '1.2'), верните самую большую версию среди тегов, начинающихся "
                "с 'wanted.'. Иначе — None."
            ),
            "starter": "def pick_tag(tags, wanted):\n    pass\n",
            "tests": [
                {"args": [["1.2.0", "1.2.3", "1.10.1", "1.9.9", "alpine"], "1.2"], "expected": "1.2.3"},
                {"args": [["1.2.0", "1.2.3", "1.10.1", "1.9.9", "alpine"], "1"], "expected": "1.10.1"},
                {"args": [["1.2.0", "1.2.3", "1.10.1", "1.9.9", "alpine"], "latest"], "expected": "1.10.1"},
                {"args": [["1.2.0", "latest"], "latest"], "expected": "latest"},
                {"args": [["1.2.0"], "2"], "expected": None},
                {"args": [[], "latest"], "expected": None},
                {"args": [["alpine", "slim"], "latest"], "expected": None},
                {"args": [["3.11", "3.11.4", "3.12.0"], "3.11"], "expected": "3.11"},
            ],
            "hint": "Версии сравнивайте списками чисел; префикс проверяйте с точкой, чтобы '1' не совпал с '10.0.0'.",
        },
        {
            "id": "ct-health",
            "mode": "func",
            "func": "health_status",
            "title": "Статус здоровья контейнера",
            "statement": (
                "Напишите функцию health_status(results, retries, start_checks): "
                "results — результаты проверок (True — успех). Статус сначала "
                "'starting'; успех → 'healthy' (и счётчик подряд идущих неудач "
                "сбрасывается); неудачи считаются подряд, но первые start_checks "
                "проверок в состоянии 'starting' в счёт не идут; когда подряд "
                "неудач набралось retries — 'unhealthy'. Верните статус после "
                "каждой проверки."
            ),
            "starter": "def health_status(results, retries, start_checks):\n    pass\n",
            "tests": [
                {"args": [[False, False, True, True], 3, 2], "expected": ["starting", "starting", "healthy", "healthy"]},
                {"args": [[True, False, False, False], 3, 0], "expected": ["healthy", "healthy", "healthy", "unhealthy"]},
                {"args": [[False, False, False], 2, 0], "expected": ["starting", "unhealthy", "unhealthy"]},
                {"args": [[False, False, False, False], 2, 2], "expected": ["starting", "starting", "starting", "unhealthy"]},
                {"args": [[], 3, 0], "expected": []},
                {"args": [[True, False, True, False, False], 2, 0], "expected": ["healthy", "healthy", "healthy", "healthy", "unhealthy"]},
                {"args": [[False, True, False, False, False], 3, 1], "expected": ["starting", "healthy", "healthy", "healthy", "unhealthy"]},
            ],
            "hint": "Заведите счётчик подряд идущих неудач и статус; в начальный период неудачи пропускайте.",
        },
    ],
    10: [
        {
            "id": "k-loadavg",
            "mode": "func",
            "func": "load_average",
            "title": "Средняя нагрузка (load average)",
            "statement": (
                "Напишите функцию load_average(samples): samples — число работающих "
                "и ожидающих процессов каждые 5 секунд. Ядро считает три "
                "экспоненциальных средних (1, 5 и 15 минут): load = load · e + n · "
                "(1 − e), где e = exp(−5 / (60 · минут)), начальное значение 0. "
                "Верните список [l1, l5, l15] после всех замеров, округлённый до "
                "двух знаков."
            ),
            "starter": "import math\n\n\ndef load_average(samples):\n    pass\n",
            "tests": [
                {"args": [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]], "expected": [2.53, 0.73, 0.26]},
                {"args": [[0, 0, 0, 0, 0]], "expected": [0.0, 0.0, 0.0]},
                {"args": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]], "expected": [8.0, 7.6, 5.06]},
                {"args": [[1, 2, 3, 4, 5, 6]], "expected": [1.47, 0.34, 0.12]},
                {"args": [[]], "expected": [0.0, 0.0, 0.0]},
                {"args": [[10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], "expected": [2.33, 1.48, 0.6]},
            ],
            "hint": "Три независимых экспоненциальных среднего с разными e; округление в самом конце.",
        },
        {
            "id": "k-sysctl-parse",
            "mode": "func",
            "func": "parse_sysctl",
            "title": "Файл sysctl.conf",
            "statement": (
                "Напишите функцию parse_sysctl(text): строки 'ключ = значение', "
                "ключ с точками ('net.ipv4.ip_forward'). Пустые строки, строки без "
                "'=' и с '#' или ';' в начале пропускайте. Верните вложенные "
                "словари по частям ключа; значения — строки без пробелов по краям; "
                "при повторе побеждает последняя строка. Конфликтов вида «a и a.b» "
                "в тестах нет."
            ),
            "starter": "def parse_sysctl(text):\n    pass\n",
            "tests": [
                {"args": ["net.ipv4.ip_forward = 1\nnet.ipv4.tcp_syncookies=1\nvm.swappiness = 10\n"], "expected": {"net": {"ipv4": {"ip_forward": "1", "tcp_syncookies": "1"}}, "vm": {"swappiness": "10"}}},
                {"args": ["# c\n\nkernel.hostname = box\nkernel.hostname = other\n"], "expected": {"kernel": {"hostname": "other"}}},
                {"args": [""], "expected": {}},
                {"args": ["fs.file-max = 2097152\nfs.inotify.max_user_watches = 524288\n"], "expected": {"fs": {"file-max": "2097152", "inotify": {"max_user_watches": "524288"}}}},
                {"args": ["a.b.c = x = y\n"], "expected": {"a": {"b": {"c": "x = y"}}}},
            ],
            "hint": "Делите ключ по точкам, а для вложенности используйте setdefault.",
        },
        {
            "id": "k-strace-summary",
            "mode": "func",
            "func": "strace_summary",
            "title": "Сводка strace",
            "statement": (
                "Напишите функцию strace_summary(lines): строки вывода strace вида "
                "'openat(AT_FDCWD, \"/etc/x\", O_RDONLY) = 3' или 'read(3, ..., 4096) "
                "= -1 EAGAIN (Resource temporarily unavailable)'. Для строк, "
                "начинающихся с имени вызова и '(': посчитайте вызовы по именам и "
                "ошибки по кодам (= -1 КОД). Остальные строки (например '+++ exited "
                "with 0 +++') пропустите. Верните {'counts': {...}, 'errors': "
                "{...}}."
            ),
            "starter": "import re\n\n\ndef strace_summary(lines):\n    pass\n",
            "tests": [
                {"args": [["openat(AT_FDCWD, \"/etc/ld.so.cache\", O_RDONLY) = 3", "read(3, \"abc\", 4096) = 3", "openat(AT_FDCWD, \"/nope\", O_RDONLY) = -1 ENOENT (No such file or directory)", "openat(AT_FDCWD, \"/root\", O_RDONLY) = -1 EACCES (Permission denied)", "close(3) = 0", "+++ exited with 1 +++"]], "expected": {"counts": {"openat": 3, "read": 1, "close": 1}, "errors": {"ENOENT": 1, "EACCES": 1}}},
                {"args": [[]], "expected": {"counts": {}, "errors": {}}},
                {"args": [["read(0, 0x7ffd, 100) = -1 EAGAIN (Resource temporarily unavailable)", "read(0, 0x7ffd, 100) = -1 EAGAIN (Resource temporarily unavailable)", "write(1, \"x\", 1) = 1"]], "expected": {"counts": {"read": 2, "write": 1}, "errors": {"EAGAIN": 2}}},
                {"args": [["--- SIGCHLD {si_signo=SIGCHLD} ---", "wait4(-1, NULL, 0, NULL) = 123"]], "expected": {"counts": {"wait4": 1}, "errors": {}}},
            ],
            "hint": "Имя вызова — регулярным выражением в начале строки; код ошибки ищите после '= -1 '.",
        },
        {
            "id": "k-fd-table",
            "mode": "func",
            "func": "fd_table",
            "title": "Таблица дескрипторов",
            "statement": (
                "Напишите функцию fd_table(ops, limit): процесс начинает с "
                "открытыми 0, 1, 2; limit — наибольшее число одновременно "
                "допустимых номеров (fd < limit). Операции: ['open'] и ['dup', fd] "
                "получают наименьший свободный номер; ['close', fd] закрывает. "
                "Результаты: для open/dup — номер, либо 'EMFILE' (нет свободных), "
                "для dup несуществующего — 'EBADF'; для close — 0 или 'EBADF'. "
                "Верните список результатов."
            ),
            "starter": "def fd_table(ops, limit):\n    pass\n",
            "tests": [
                {"args": [[["open"], ["open"], ["close", 3], ["open"]], 10], "expected": [3, 4, 0, 3]},
                {"args": [[["open"], ["open"]], 4], "expected": [3, "EMFILE"]},
                {"args": [[["close", 1], ["open"]], 5], "expected": [0, 1]},
                {"args": [[["dup", 1], ["dup", 9]], 8], "expected": [3, "EBADF"]},
                {"args": [[["close", 7]], 8], "expected": ["EBADF"]},
                {"args": [[], 8], "expected": []},
                {"args": [[["open"], ["open"], ["open"]], 5], "expected": [3, 4, "EMFILE"]},
                {"args": [[["open"], ["close", 0], ["close", 0], ["open"]], 6], "expected": [3, 0, "EBADF", 0]},
            ],
            "hint": "Множество занятых номеров; новый номер — наименьший свободный в диапазоне [0, limit).",
        },
        {
            "id": "k-oom-victim",
            "mode": "func",
            "func": "oom_victim",
            "title": "Кого убьёт OOM-killer",
            "statement": (
                "Напишите функцию oom_victim(procs, total_kb): procs — список [pid, "
                "rss_kb, oom_score_adj]. Оценка = rss_kb · 1000 // total_kb + "
                "oom_score_adj, ограниченная диапазоном 0…1000. Процесс с adj = "
                "−1000 не убивают никогда. Верните pid процесса с наибольшей "
                "оценкой (при равных — с меньшим pid) или None, если убивать "
                "некого."
            ),
            "starter": "def oom_victim(procs, total_kb):\n    pass\n",
            "tests": [
                {"args": [[[1, 1000, 0], [2, 5000, 0], [3, 3000, 0]], 10000], "expected": 2},
                {"args": [[[1, 5000, -1000], [2, 100, 0]], 10000], "expected": 2},
                {"args": [[[1, 5000, -1000]], 10000], "expected": None},
                {"args": [[[5, 100, 900], [6, 9000, 0]], 10000], "expected": 5},
                {"args": [[[7, 9000, 500], [8, 9500, 500]], 10000], "expected": 7},
                {"args": [[], 1000], "expected": None},
                {"args": [[[3, 0, 0], [2, 0, 0]], 1000], "expected": 2},
            ],
            "hint": "Оценка обрезается до [0, 1000]; при равенстве оценок выбирайте меньший pid.",
        },
        {
            "id": "k-unload-order",
            "mode": "func",
            "func": "unload_order",
            "title": "Выгрузка модулей ядра",
            "statement": (
                "Напишите функцию unload_order(deps, target): deps — словарь "
                "«модуль → список модулей, которые он использует». Чтобы выгрузить "
                "target, сначала надо выгрузить все модули, которые (прямо или "
                "косвенно) используют его. Верните порядок выгрузки (target — "
                "последний): модуль можно выгрузить, когда не осталось "
                "невыгруженных модулей, использующих его; среди готовых берите "
                "первым наименьшее имя. Если target нет в deps — [target]."
            ),
            "starter": "import heapq\n\n\ndef unload_order(deps, target):\n    pass\n",
            "tests": [
                {"args": [{"nvidia_drm": ["nvidia_modeset", "drm"], "nvidia_modeset": ["nvidia"], "nvidia": [], "drm": []}, "nvidia"], "expected": ["nvidia_drm", "nvidia_modeset", "nvidia"]},
                {"args": [{"a": ["b"], "b": ["c"], "c": []}, "c"], "expected": ["a", "b", "c"]},
                {"args": [{"a": ["b"], "b": []}, "a"], "expected": ["a"]},
                {"args": [{"x": []}, "x"], "expected": ["x"]},
                {"args": [{}, "ghost"], "expected": ["ghost"]},
                {"args": [{"a": ["t"], "b": ["t"], "c": ["a", "b"], "t": []}, "t"], "expected": ["c", "a", "b", "t"]},
            ],
            "hint": "Найдите всех, кто зависит от target (транзитивно), и выгружайте их в обратном порядке зависимостей с кучей для алфавита.",
        },
        {
            "id": "k-vmstat",
            "mode": "func",
            "func": "vmstat_avg",
            "title": "Среднее по vmstat",
            "statement": (
                "Напишите функцию vmstat_avg(text): вывод 'vmstat 1 N' — две строки "
                "заголовка (вторая с именами столбцов: r b swpd free … st) и строки "
                "чисел. Первая строка данных — среднее с момента загрузки, её "
                "исключите; если строк данных всего одна — используйте её. Верните "
                "словарь «столбец → среднее по остальным строкам», округлённое до "
                "одного знака."
            ),
            "starter": "def vmstat_avg(text):\n    pass\n",
            "tests": [
                {"args": ["procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----\n r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st\n 1  0      0 800000  50000 300000    0    0    10    20  100  200  5  2 93  0  0\n 3  0      0 790000  50000 301000    0    0     0    40  300  500 20  5 75  0  0\n 5  1      0 780000  50000 302000    0    0     0    60  500  700 40 10 50  0  0\n"], "expected": {"r": 4.0, "b": 0.5, "swpd": 0.0, "free": 785000.0, "buff": 50000.0, "cache": 301500.0, "si": 0.0, "so": 0.0, "bi": 0.0, "bo": 50.0, "in": 400.0, "cs": 600.0, "us": 30.0, "sy": 7.5, "id": 62.5, "wa": 0.0, "st": 0.0}},
                {"args": ["procs\n r b swpd free buff cache si so bi bo in cs us sy id wa st\n 2 0 0 1000 10 20 0 0 1 2 3 4 5 6 7 8 9\n"], "expected": {"r": 2.0, "b": 0.0, "swpd": 0.0, "free": 1000.0, "buff": 10.0, "cache": 20.0, "si": 0.0, "so": 0.0, "bi": 1.0, "bo": 2.0, "in": 3.0, "cs": 4.0, "us": 5.0, "sy": 6.0, "id": 7.0, "wa": 8.0, "st": 9.0}},
                {"args": ["h1\n r b swpd free buff cache si so bi bo in cs us sy id wa st\n 1 0 0 100 10 20 0 0 0 0 10 10 1 1 98 0 0\n 2 0 0 200 10 20 0 0 0 0 10 10 1 1 98 0 0\n"], "expected": {"r": 2.0, "b": 0.0, "swpd": 0.0, "free": 200.0, "buff": 10.0, "cache": 20.0, "si": 0.0, "so": 0.0, "bi": 0.0, "bo": 0.0, "in": 10.0, "cs": 10.0, "us": 1.0, "sy": 1.0, "id": 98.0, "wa": 0.0, "st": 0.0}},
            ],
            "hint": "Найдите строку заголовка (начинается с 'r'), затем собирайте только строки из чисел; отбросьте первую.",
        },
        {
            "id": "k-perf-report",
            "mode": "func",
            "func": "perf_report",
            "title": "Отчёт профилировщика",
            "statement": (
                "Напишите функцию perf_report(samples): samples — стеки вызовов в "
                "моменты снимков, функции через ';' от внешней к внутренней "
                "('main;parse;read'). Для каждой функции посчитайте self% (доля "
                "снимков, где она на вершине стека — последняя) и total% (доля "
                "снимков, где она есть в стеке хотя бы раз), округлите до 1 знака. "
                "Верните список [имя, self%, total%], отсортированный по self% "
                "(убывание), затем total% (убывание), затем имени. Пустой список "
                "снимков — пустой список."
            ),
            "starter": "def perf_report(samples):\n    pass\n",
            "tests": [
                {"args": [["main;parse;read", "main;parse;read", "main;parse;tokenize", "main;render", "main;render;draw", "main"]], "expected": [["read", 33.3, 33.3], ["main", 16.7, 100.0], ["render", 16.7, 33.3], ["draw", 16.7, 16.7], ["tokenize", 16.7, 16.7], ["parse", 0.0, 50.0]]},
                {"args": [[]], "expected": []},
                {"args": [["a"]], "expected": [["a", 100.0, 100.0]]},
                {"args": [["a;b;a", "a;b", "c"]], "expected": [["a", 33.3, 66.7], ["b", 33.3, 66.7], ["c", 33.3, 33.3]]},
                {"args": [["x;y", "x;y", "x;y"]], "expected": [["y", 100.0, 100.0], ["x", 0.0, 100.0]]},
            ],
            "hint": "Два счётчика: self — по последнему элементу стека, total — по множеству функций стека (чтобы рекурсия не считалась дважды).",
        },
        {
            "id": "k-dmesg-filter",
            "mode": "func",
            "func": "dmesg_filter",
            "title": "Фильтр dmesg",
            "statement": (
                "Напишите функцию dmesg_filter(lines, since, word): строки 'dmesg' "
                "вида '[   12.345678] usb 1-1: new high-speed device'. Верните "
                "список [время (float), сообщение] для строк, где время ≥ since и "
                "слово word встречается в сообщении без учёта регистра. Строки без "
                "метки времени пропустите."
            ),
            "starter": "import re\n\n\ndef dmesg_filter(lines, since, word):\n    pass\n",
            "tests": [
                {"args": [["[    0.000000] Linux version 6.1", "[   12.345678] usb 1-1: new high-speed device", "[   30.5] USB disconnect", "garbage"], 10.0, "usb"], "expected": [[12.345678, "usb 1-1: new high-speed device"], [30.5, "USB disconnect"]]},
                {"args": [[], 0.0, "x"], "expected": []},
                {"args": [["[1.0] a", "[ 2.0] b"], 1.5, ""], "expected": [[2.0, "b"]]},
                {"args": [["[100.25] Out of memory: Killed process 42"], 0.0, "KILLED"], "expected": [[100.25, "Out of memory: Killed process 42"]]},
                {"args": [["[5.5] nothing here"], 6.0, "nothing"], "expected": []},
            ],
            "hint": "Регулярное выражение вытаскивает время и текст; сравнивайте слово в нижнем регистре.",
        },
    ],
}
