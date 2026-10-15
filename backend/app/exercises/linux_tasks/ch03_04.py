"""Задачи книги «Linux: от шелла до ядра»: главы 3–4."""

TASKS: dict[int, list[dict]] = {
    3: [
        {
            "id": "perm-symbolic",
            "mode": "func",
            "func": "mode_to_str",
            "title": "Права числом в права буквами",
            "statement": (
                "Напишите функцию mode_to_str(mode): mode — число (например, "
                "0o4755), результат — 9 символов как в ls -l, без типа файла: "
                "rwxr-xr-x. Особые биты: setuid (0o4000) заменяет x владельца на s "
                "(или S, если x нет), setgid (0o2000) — x группы на s/S, sticky "
                "(0o1000) — x прочих на t/T."
            ),
            "starter": "def mode_to_str(mode):\n    pass\n",
            "tests": [
                {"args": [493], "expected": "rwxr-xr-x"},
                {"args": [2541], "expected": "rwsr-xr-x"},
                {"args": [2468], "expected": "rwSr--r--"},
                {"args": [1517], "expected": "rwxr-sr-x"},
                {"args": [1023], "expected": "rwxrwxrwt"},
                {"args": [950], "expected": "rw-rw-rwT"},
                {"args": [0], "expected": "---------"},
                {"args": [416], "expected": "rw-r-----"},
                {"args": [4095], "expected": "rwsrwsrwt"},
            ],
            "hint": "Для каждой из трёх троек: биты 4/2/1 → r/w/x; если стоит спецбит — последний символ тройки заменяется на s/S или t/T.",
        },
        {
            "id": "perm-parse",
            "mode": "func",
            "func": "str_to_mode",
            "title": "Права буквами в права числом",
            "statement": (
                "Напишите функцию str_to_mode(text): text — 9 символов вида "
                "'rwsr-xr-t'. Верните число: обычные биты плюс специальные: s/S в "
                "позиции владельца — 0o4000, s/S у группы — 0o2000, t/T у прочих — "
                "0o1000; x установлен для 's', 't', 'x' (строчные), и не установлен "
                "для 'S', 'T', '-'."
            ),
            "starter": "def str_to_mode(text):\n    pass\n",
            "tests": [
                {"args": ["rwxr-xr-x"], "expected": 493},
                {"args": ["rwsr-xr-x"], "expected": 2541},
                {"args": ["rwSr--r--"], "expected": 2468},
                {"args": ["rwxr-sr-x"], "expected": 1517},
                {"args": ["rwxrwxrwt"], "expected": 1023},
                {"args": ["rw-rw-rwT"], "expected": 950},
                {"args": ["---------"], "expected": 0},
                {"args": ["rw-r-----"], "expected": 416},
            ],
            "hint": "Номер символа i: группа i // 3 (владелец, группа, прочие), позиция i % 3 (r, w, x/s/t).",
        },
        {
            "id": "perm-chmod",
            "mode": "func",
            "func": "chmod",
            "title": "chmod по-символьному",
            "statement": (
                "Напишите функцию chmod(mode, expr): expr — одна или несколько "
                "через запятую команд вида [кто][операция][права]. Кто: u, g, o, a "
                "(можно несколько букв, 'a' или пусто = ugo); операция: '+' "
                "(добавить), '-' (убрать), '=' (установить ровно); права: буквы r, "
                "w, x (могут отсутствовать — '=' без прав очищает). Особые биты не "
                "трогайте. Также expr может быть восьмеричным числом ('644') — "
                "тогда возвращайте его целиком. Результат — число (только обычные 9 "
                "бит)."
            ),
            "starter": "def chmod(mode, expr):\n    pass\n",
            "tests": [
                {"args": [420, "u+x"], "expected": 484},
                {"args": [493, "go-rx"], "expected": 448},
                {"args": [384, "a+r"], "expected": 420},
                {"args": [511, "o="], "expected": 504},
                {"args": [416, "u=rwx,g=rx,o="], "expected": 488},
                {"args": [420, "755"], "expected": 493},
                {"args": [0, "+x"], "expected": 73},
                {"args": [493, "g="], "expected": 453},
                {"args": [448, "go+rw,u-w"], "expected": 374},
                {"args": [292, "ug+w"], "expected": 436},
            ],
            "hint": "Разберите команду: who → сдвиги (u=6, g=3, o=0); права → число 0..7; затем |=, &= ~ или замена тройки.",
        },
        {
            "id": "perm-umask",
            "mode": "func",
            "func": "new_mode",
            "title": "Права нового файла и маска",
            "statement": (
                "Напишите функцию new_mode(umask, is_dir): права нового файла — это "
                "0o666 (для файла) или 0o777 (для каталога) без битов маски umask. "
                "Верните число."
            ),
            "starter": "def new_mode(umask, is_dir):\n    pass\n",
            "tests": [
                {"args": [18, False], "expected": 420},
                {"args": [18, True], "expected": 493},
                {"args": [63, False], "expected": 384},
                {"args": [63, True], "expected": 448},
                {"args": [0, False], "expected": 438},
                {"args": [2, True], "expected": 509},
                {"args": [511, False], "expected": 0},
                {"args": [23, True], "expected": 488},
            ],
            "hint": "Побитово: base & ~umask.",
        },
        {
            "id": "perm-can-access",
            "mode": "func",
            "func": "can_access",
            "title": "Кто может открыть файл",
            "statement": (
                "Напишите функцию can_access(file, user, groups, want): file — "
                "словарь {'owner': ..., 'group': ..., 'mode': число}; user — имя; "
                "groups — список групп пользователя; want — 'r', 'w' или 'x'. "
                "Правила: root (user == 'root') читает и пишет всегда, исполняет — "
                "если установлен любой x-бит. Остальные: если user — владелец, "
                "смотрим ТОЛЬКО биты владельца; иначе если группа файла входит в "
                "groups — биты группы; иначе — биты прочих."
            ),
            "starter": "def can_access(file, user, groups, want):\n    pass\n",
            "tests": [
                {"args": [{"owner": "ann", "group": "dev", "mode": 416}, "ann", ["ann"], "w"], "expected": True},
                {"args": [{"owner": "ann", "group": "dev", "mode": 416}, "bob", ["dev"], "r"], "expected": True},
                {"args": [{"owner": "ann", "group": "dev", "mode": 416}, "bob", ["dev"], "w"], "expected": False},
                {"args": [{"owner": "ann", "group": "dev", "mode": 416}, "eve", ["eve"], "r"], "expected": False},
                {"args": [{"owner": "ann", "group": "dev", "mode": 63}, "ann", ["ann", "dev"], "r"], "expected": False},
                {"args": [{"owner": "ann", "group": "dev", "mode": 4}, "bob", ["dev"], "r"], "expected": False},
                {"args": [{"owner": "ann", "group": "dev", "mode": 384}, "root", [], "w"], "expected": True},
                {"args": [{"owner": "ann", "group": "dev", "mode": 420}, "root", [], "x"], "expected": False},
                {"args": [{"owner": "ann", "group": "dev", "mode": 484}, "root", [], "x"], "expected": True},
            ],
            "hint": "Важно: если пользователь владелец, группа и прочие НЕ проверяются — даже если у них прав больше.",
        },
        {
            "id": "perm-acl",
            "mode": "func",
            "func": "acl_allows",
            "title": "Расширенные права (ACL) и маска",
            "statement": (
                "Напишите функцию acl_allows(acl, owner, group, user, user_groups, "
                "want): acl — список [тег, имя, права], где тег "
                "'user'/'group'/'other'/'mask', права — строка из трёх символов "
                "('r-x'); имя пустое у записей владельца ('user',''), "
                "группы-владельца ('group',''), 'other' и 'mask'. Если маски нет — "
                "она 'rwx'. Порядок проверки (POSIX): владелец — права владельца "
                "(маска не действует); иначе именованная запись user — права & "
                "маска; иначе если user_groups содержит группу файла или "
                "именованную группу из ACL — разрешено, если ХОТЬ ОДНА из "
                "подходящих записей (права & маска) даёт want, иначе отказ без "
                "проверки 'other'; иначе — права 'other'. want — 'r', 'w' или 'x'."
            ),
            "starter": "def acl_allows(acl, owner, group, user, user_groups, want):\n    pass\n",
            "tests": [
                {"args": [[["user", "", "rw-"], ["user", "bob", "rwx"], ["group", "", "r--"], ["mask", "", "r--"], ["other", "", "---"]], "ann", "dev", "bob", ["bob"], "w"], "expected": False},
                {"args": [[["user", "", "rw-"], ["user", "bob", "rwx"], ["group", "", "r--"], ["mask", "", "r--"], ["other", "", "---"]], "ann", "dev", "bob", ["bob"], "r"], "expected": True},
                {"args": [[["user", "", "rw-"], ["group", "", "r--"], ["group", "ops", "rw-"], ["mask", "", "rw-"], ["other", "", "r--"]], "ann", "dev", "cat", ["ops"], "w"], "expected": True},
                {"args": [[["user", "", "rw-"], ["group", "", "r--"], ["group", "ops", "rw-"], ["mask", "", "rw-"], ["other", "", "r--"]], "ann", "dev", "cat", ["dev", "ops"], "w"], "expected": True},
                {"args": [[["user", "", "rw-"], ["group", "", "r--"], ["other", "", "rwx"]], "ann", "dev", "dan", ["dev"], "w"], "expected": False},
                {"args": [[["user", "", "rw-"], ["group", "", "r--"], ["other", "", "rwx"]], "ann", "dev", "dan", ["staff"], "w"], "expected": True},
                {"args": [[["user", "", "r--"], ["group", "", "---"], ["mask", "", "---"], ["other", "", "---"]], "ann", "dev", "ann", ["ann"], "r"], "expected": True},
                {"args": [[["user", "", "rwx"], ["group", "", "---"], ["other", "", "---"]], "ann", "dev", "bob", [], "r"], "expected": False},
            ],
            "hint": "Соберите записи в словари; маска действует на именованных пользователей и все группы, но не на владельца и 'other'.",
        },
        {
            "id": "perm-risky",
            "mode": "func",
            "func": "risky_files",
            "title": "Опасные права в выводе ls -l",
            "statement": (
                "Напишите функцию risky_files(lines): lines — строки вывода ls -l "
                "(тип+права 10 символов, число ссылок, владелец, группа, размер, "
                "месяц, число, время, путь — путь может содержать пробелы). Верните "
                "отсортированный список путей, которые стоит проверить: обычные "
                "файлы ('-') с setuid или setgid (s/S в правах владельца или "
                "группы); любые файлы и каталоги, доступные всем на запись (w у "
                "прочих), кроме каталогов с sticky-битом (t/T) и символических "
                "ссылок ('l'), которые пропускайте целиком."
            ),
            "starter": "def risky_files(lines):\n    pass\n",
            "tests": [
                {"args": [["-rwsr-xr-x 1 root root 54096 Jan  1 12:00 /usr/bin/passwd", "-rwxr-xr-x 1 root root 100 Jan  1 12:00 /usr/bin/ls", "drwxrwxrwt 10 root root 4096 Jan  1 12:00 /tmp", "drwxrwxrwx 2 ann ann 4096 Jan  1 12:00 /srv/shared dir", "lrwxrwxrwx 1 root root 7 Jan  1 12:00 /bin"]], "expected": ["/srv/shared dir", "/usr/bin/passwd"]},
                {"args": [["-rw-rw-rw- 1 ann ann 5 Jan 2 10:00 /etc/x", "-rwxr-sr-x 1 root mail 5 Jan 2 10:00 /usr/bin/m", "-rw-r--r-- 1 root root 5 Jan 2 10:00 /etc/y", "-rwSr--r-- 1 root root 5 Jan 2 10:00 /opt/s"]], "expected": ["/etc/x", "/opt/s", "/usr/bin/m"]},
                {"args": [[]], "expected": []},
                {"args": [["drwxrwsr-x 2 root staff 4096 Jan 1 1:00 /var/local"]], "expected": []},
                {"args": [["drwxrwxrwT 2 root root 4096 Jan 1 1:00 /var/t"]], "expected": []},
            ],
            "hint": "line.split(None, 8) оставляет путь (с пробелами) последним полем; индексы строки прав: 3 — x владельца, 6 — x группы, 8 — w прочих, 9 — x прочих.",
        },
        {
            "id": "perm-sudoers",
            "mode": "func",
            "func": "sudo_allows",
            "title": "Разбор правил sudoers",
            "statement": (
                "Напишите функцию sudo_allows(rules, user, groups, command): rules "
                "— строки sudoers вида 'ann ALL=(ALL) ALL', '%wheel ALL=(ALL) "
                "NOPASSWD: /usr/bin/systemctl, /usr/bin/journalctl', 'bob "
                "ALL=(root) /usr/bin/apt update'. Субъект — имя пользователя или "
                "%группа (группа должна быть в groups). Команды через запятую: ALL "
                "— любая; спецификация без пробела — любая команда с такой "
                "программой (любые аргументы); спецификация с пробелами — только "
                "точное совпадение всей команды. Работает правило «последнее "
                "подходящее побеждает». Пустые строки и строки с '#' пропускайте. "
                "Верните ('allow', без_пароля) или ('deny',)."
            ),
            "starter": "def sudo_allows(rules, user, groups, command):\n    pass\n",
            "tests": [
                {"args": [["ann ALL=(ALL) ALL"], "ann", [], "/bin/ls -l"], "expected": ("allow", False)},
                {"args": [["%wheel ALL=(ALL) NOPASSWD: /usr/bin/systemctl, /usr/bin/journalctl"], "bob", ["wheel"], "/usr/bin/systemctl restart nginx"], "expected": ("allow", True)},
                {"args": [["%wheel ALL=(ALL) NOPASSWD: /usr/bin/systemctl, /usr/bin/journalctl"], "bob", ["wheel"], "/bin/rm -rf /"], "expected": ("deny",)},
                {"args": [["bob ALL=(root) /usr/bin/apt update"], "bob", [], "/usr/bin/apt update"], "expected": ("allow", False)},
                {"args": [["bob ALL=(root) /usr/bin/apt update"], "bob", [], "/usr/bin/apt install x"], "expected": ("deny",)},
                {"args": [["# comment", "", "ann ALL=(ALL) ALL"], "bob", ["ann"], "/bin/ls"], "expected": ("deny",)},
                {"args": [["ann ALL=(ALL) NOPASSWD: ALL", "ann ALL=(ALL) /bin/ls"], "ann", [], "/bin/ls"], "expected": ("allow", False)},
                {"args": [["ann ALL=(ALL) ALL", "%ops ALL=(ALL) NOPASSWD: /bin/ls"], "ann", ["ops"], "/bin/ls"], "expected": ("allow", True)},
            ],
            "hint": "Идите по правилам по порядку и обновляйте вердикт при каждом подходящем: последнее подходящее побеждает.",
        },
    ],
    4: [
        {
            "id": "proc-tree",
            "mode": "func",
            "func": "ps_tree",
            "title": "Дерево процессов",
            "statement": (
                "Напишите функцию ps_tree(procs): procs — список [pid, ppid, имя]. "
                "Верните список строк, как pstree: каждый процесс — строка 'имя "
                "(pid)' с отступом по 2 пробела на уровень вложенности; сначала "
                "родитель, потом дети по возрастанию pid. Корни — процессы, чей "
                "ppid отсутствует среди pid (по возрастанию pid)."
            ),
            "starter": "def ps_tree(procs):\n    pass\n",
            "tests": [
                {"args": [[[1, 0, "systemd"], [100, 1, "sshd"], [200, 100, "bash"], [201, 200, "vim"], [150, 1, "cron"]]], "expected": ["systemd (1)", "  sshd (100)", "    bash (200)", "      vim (201)", "  cron (150)"]},
                {"args": [[]], "expected": []},
                {"args": [[[5, 1, "orphan"], [6, 5, "child"]]], "expected": ["orphan (5)", "  child (6)"]},
                {"args": [[[2, 1, "b"], [1, 0, "a"], [3, 1, "c"], [4, 3, "d"], [5, 3, "e"]]], "expected": ["a (1)", "  b (2)", "  c (3)", "    d (4)", "    e (5)"]},
                {"args": [[[10, 99, "x"], [11, 98, "y"]]], "expected": ["x (10)", "y (11)"]},
            ],
            "hint": "Словарь «родитель → список детей» и рекурсивный обход; корни — те, у кого родителя нет в списке.",
        },
        {
            "id": "proc-reparent",
            "mode": "func",
            "func": "after_kills",
            "title": "Усыновление сирот",
            "statement": (
                "Напишите функцию after_kills(procs, dead): procs — список [pid, "
                "ppid]; dead — список pid, которые завершаются по очереди. Когда "
                "процесс завершается, он исчезает из списка, а все его дети "
                "переходят к процессу init (pid 1). Верните оставшиеся [pid, ppid], "
                "отсортированные по pid. init (pid 1) не завершается."
            ),
            "starter": "def after_kills(procs, dead):\n    pass\n",
            "tests": [
                {"args": [[[1, 0], [10, 1], [20, 10], [21, 10], [30, 20]], [10]], "expected": [[1, 0], [20, 1], [21, 1], [30, 20]]},
                {"args": [[[1, 0], [10, 1], [20, 10], [30, 20]], [10, 20]], "expected": [[1, 0], [30, 1]]},
                {"args": [[[1, 0], [10, 1]], []], "expected": [[1, 0], [10, 1]]},
                {"args": [[[1, 0], [10, 1], [20, 10], [30, 20]], [30, 20, 10]], "expected": [[1, 0]]},
                {"args": [[[1, 0], [5, 1]], [99]], "expected": [[1, 0], [5, 1]]},
            ],
            "hint": "Словарь pid → ppid; при смерти d всем, у кого ppid == d, ставим ppid = 1.",
        },
        {
            "id": "proc-wait-status",
            "mode": "func",
            "func": "decode_status",
            "title": "Статус завершения (wait)",
            "statement": (
                "Напишите функцию decode_status(status): статус, который возвращает "
                "wait(). Если младшие 7 бит равны 0 — процесс вышел сам: ('exited', "
                "код), где код = (status >> 8) & 255. Если младший байт равен 0x7f "
                "— остановлен: ('stopped', (status >> 8) & 255). Иначе убит "
                "сигналом: ('signaled', номер_сигнала, дамп_памяти), номер = status "
                "& 0x7f, дамп = True, если установлен бит 0x80."
            ),
            "starter": "def decode_status(status):\n    pass\n",
            "tests": [
                {"args": [0], "expected": ("exited", 0)},
                {"args": [256], "expected": ("exited", 1)},
                {"args": [10752], "expected": ("exited", 42)},
                {"args": [9], "expected": ("signaled", 9, False)},
                {"args": [15], "expected": ("signaled", 15, False)},
                {"args": [139], "expected": ("signaled", 11, True)},
                {"args": [4991], "expected": ("stopped", 19)},
                {"args": [32512], "expected": ("exited", 127)},
            ],
            "hint": "Сначала проверяйте «вышел сам», затем «остановлен» (младший байт 0x7f), потом «убит сигналом».",
        },
        {
            "id": "proc-signal-outcome",
            "mode": "func",
            "func": "signal_outcome",
            "title": "Что сделает процесс с сигналом",
            "statement": (
                "Напишите функцию signal_outcome(sig, handler): sig — имя сигнала "
                "('SIGTERM', 'SIGKILL', …), handler — 'default', 'ignore' или "
                "'catch' (процесс установил обработчик). SIGKILL и SIGSTOP нельзя "
                "поймать или игнорировать — всегда действует действие по умолчанию. "
                "Действия по умолчанию: SIGKILL, SIGTERM, SIGINT, SIGHUP, SIGUSR1, "
                "SIGUSR2, SIGSEGV, SIGPIPE, SIGALRM — 'terminated'; SIGSTOP, "
                "SIGTSTP — 'stopped'; SIGCONT — 'continued'; SIGCHLD — 'ignored'. "
                "Результат: при 'catch' — 'handled', при 'ignore' — 'ignored', при "
                "'default' — действие по умолчанию."
            ),
            "starter": "def signal_outcome(sig, handler):\n    pass\n",
            "tests": [
                {"args": ["SIGTERM", "default"], "expected": "terminated"},
                {"args": ["SIGTERM", "catch"], "expected": "handled"},
                {"args": ["SIGKILL", "catch"], "expected": "terminated"},
                {"args": ["SIGKILL", "ignore"], "expected": "terminated"},
                {"args": ["SIGSTOP", "catch"], "expected": "stopped"},
                {"args": ["SIGINT", "ignore"], "expected": "ignored"},
                {"args": ["SIGCHLD", "default"], "expected": "ignored"},
                {"args": ["SIGCONT", "default"], "expected": "continued"},
                {"args": ["SIGTSTP", "ignore"], "expected": "ignored"},
                {"args": ["SIGHUP", "catch"], "expected": "handled"},
            ],
            "hint": "Сначала примените правило про неперехватываемые сигналы, потом смотрите на обработчик.",
        },
        {
            "id": "proc-round-robin",
            "mode": "func",
            "func": "round_robin",
            "title": "Планировщик по кругу",
            "statement": (
                "Напишите функцию round_robin(jobs, quantum): jobs — список [имя, "
                "момент_появления, время_работы]. Круговой планировщик: очередь "
                "FIFO; берём первую задачу, исполняем min(quantum, остаток); затем "
                "в конец очереди сначала добавляются все задачи, появившиеся к "
                "этому моменту, а потом (если не закончилась) только что "
                "исполнявшаяся. Если очередь пуста — время прыгает к следующему "
                "появлению. Верните кортеж ([[имя, момент_завершения], …] в порядке "
                "завершения, среднее ожидание = завершение − появление − работа, "
                "округлено до 2 знаков)."
            ),
            "starter": "def round_robin(jobs, quantum):\n    pass\n",
            "tests": [
                {"args": [[["A", 0, 5], ["B", 1, 3], ["C", 2, 1]], 2], "expected": ([["C", 5], ["B", 8], ["A", 9]], 3.33)},
                {"args": [[["A", 0, 4]], 10], "expected": ([["A", 4]], 0.0)},
                {"args": [[], 3], "expected": ([], 0.0)},
                {"args": [[["A", 0, 2], ["B", 10, 2]], 5], "expected": ([["A", 2], ["B", 12]], 0.0)},
                {"args": [[["P1", 0, 24], ["P2", 0, 3], ["P3", 0, 3]], 4], "expected": ([["P2", 7], ["P3", 10], ["P1", 30]], 5.67)},
                {"args": [[["A", 0, 3], ["B", 0, 3]], 1], "expected": ([["A", 5], ["B", 6]], 2.5)},
                {"args": [[["A", 0, 6], ["B", 2, 4], ["C", 4, 2]], 3], "expected": ([["A", 9], ["C", 11], ["B", 12]], 4.67)},
            ],
            "hint": "Следите за порядком: новые задачи встают в очередь раньше, чем недоработавшая текущая.",
        },
        {
            "id": "proc-cfs",
            "mode": "func",
            "func": "cfs_runs",
            "title": "Справедливый планировщик (CFS)",
            "statement": (
                "Напишите функцию cfs_runs(nices, steps): у каждой задачи есть "
                "виртуальное время vruntime = 0 и приоритет nice (целое 0…10). "
                "Каждый из steps шагов: берём задачу с наименьшим vruntime (при "
                "равенстве — с меньшим номером), даём ей один квант и увеличиваем "
                "её vruntime на 1.25 ** nice. Верните список: сколько квантов "
                "получила каждая задача."
            ),
            "starter": "def cfs_runs(nices, steps):\n    pass\n",
            "tests": [
                {"args": [[0, 0], 10], "expected": [5, 5]},
                {"args": [[0, 4], 20], "expected": [14, 6]},
                {"args": [[0, 0, 0], 10], "expected": [4, 3, 3]},
                {"args": [[0, 2, 5], 50], "expected": [25, 16, 9]},
                {"args": [[10], 5], "expected": [5]},
                {"args": [[0, 10], 100], "expected": [90, 10]},
                {"args": [[3, 3, 3, 3], 12], "expected": [3, 3, 3, 3]},
            ],
            "hint": "Класс задач с равными nice делит время поровну; у большего nice vruntime растёт быстрее, поэтому кванты достаются реже.",
        },
        {
            "id": "proc-zombies",
            "mode": "func",
            "func": "zombies",
            "title": "Зомби и усыновление",
            "statement": (
                "Напишите функцию zombies(events): события жизни процессов. "
                "['fork', родитель, ребёнок] — новый процесс (ребёнок живой). "
                "['exit', pid] — процесс завершается: его живые дети переходят к "
                "init (pid 1), его дети-зомби немедленно подбираются init'ом "
                "(пропадают); сам процесс становится зомби, если его родитель — не "
                "init, иначе подбирается сразу. ['wait', родитель] — родитель "
                "подбирает одного ребёнка-зомби с наименьшим pid (если есть). "
                "Изначально существует только init (pid 1). Верните отсортированный "
                "список pid зомби в конце."
            ),
            "starter": "def zombies(events):\n    pass\n",
            "tests": [
                {"args": [[["fork", 1, 10], ["fork", 10, 20], ["fork", 10, 21], ["exit", 20], ["exit", 21]]], "expected": [20, 21]},
                {"args": [[["fork", 1, 10], ["fork", 10, 20], ["exit", 20], ["wait", 10]]], "expected": []},
                {"args": [[["fork", 1, 10], ["fork", 10, 20], ["fork", 10, 21], ["exit", 20], ["exit", 21], ["wait", 10]]], "expected": [21]},
                {"args": [[["fork", 1, 10], ["fork", 10, 20], ["exit", 20], ["exit", 10]]], "expected": []},
                {"args": [[["fork", 1, 10], ["fork", 10, 20], ["exit", 10], ["exit", 20]]], "expected": []},
                {"args": [[]], "expected": []},
                {"args": [[["fork", 1, 5], ["exit", 5]]], "expected": []},
            ],
            "hint": "Храните для каждого процесса родителя и состояние (alive/zombie); при exit перенаправьте живых детей к init и удалите детей-зомби.",
        },
        {
            "id": "proc-status-parse",
            "mode": "func",
            "func": "parse_status",
            "title": "Читаем /proc/PID/status",
            "statement": (
                "Напишите функцию parse_status(text): text — содержимое "
                "/proc/PID/status ('Ключ:\\tзначение' по строкам). Верните словарь с "
                "ключами 'name' (строка), 'state' (первая буква из 'State:'), "
                "'pid', 'ppid', 'threads' (числа) и 'rss_kb' (число из 'VmRSS:'; "
                "если строки нет — 0)."
            ),
            "starter": "def parse_status(text):\n    pass\n",
            "tests": [
                {"args": ["Name:\tbash\nState:\tS (sleeping)\nPid:\t1234\nPPid:\t1\nThreads:\t1\nVmRSS:\t   5120 kB\n"], "expected": {"name": "bash", "state": "S", "pid": 1234, "ppid": 1, "threads": 1, "rss_kb": 5120}},
                {"args": ["Name:\tkworker/0:1\nState:\tI (idle)\nPid:\t77\nPPid:\t2\nThreads:\t1\n"], "expected": {"name": "kworker/0:1", "state": "I", "pid": 77, "ppid": 2, "threads": 1, "rss_kb": 0}},
                {"args": ["Name:\tpython3\nState:\tR (running)\nPid:\t9\nPPid:\t8\nThreads:\t12\nVmRSS:\t100 kB\nVmSwap:\t0 kB\n"], "expected": {"name": "python3", "state": "R", "pid": 9, "ppid": 8, "threads": 12, "rss_kb": 100}},
                {"args": ["Name:\tx\nState:\tZ (zombie)\nPid:\t3\nPPid:\t2\nThreads:\t1\n"], "expected": {"name": "x", "state": "Z", "pid": 3, "ppid": 2, "threads": 1, "rss_kb": 0}},
            ],
            "hint": "Разбейте строки по первому ':' и обрежьте пробелы; из 'S (sleeping)' нужна первая буква.",
        },
    ],
}
