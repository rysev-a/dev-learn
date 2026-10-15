"""Задачи книги «Linux: от шелла до ядра»: главы 1–2."""

TASKS: dict[int, list[dict]] = {
    1: [
        {
            "id": "fs-normalize-path",
            "mode": "func",
            "func": "normalize",
            "title": "Канонический путь",
            "statement": (
                "Напишите функцию normalize(path): path — абсолютный путь. Уберите "
                "повторные слэши, точки '.', обработайте '..' (выше корня подняться "
                "нельзя), уберите хвостовой слэш. Результат всегда начинается с "
                "'/'; корень — '/'."
            ),
            "starter": "def normalize(path):\n    pass\n",
            "tests": [
                {"args": ["/usr/./bin/../lib//x/"], "expected": "/usr/lib/x"},
                {"args": ["/"], "expected": "/"},
                {"args": ["/../.."], "expected": "/"},
                {"args": ["/a/b/../../c"], "expected": "/c"},
                {"args": ["/a//b///c"], "expected": "/a/b/c"},
                {"args": ["/home/user/./"], "expected": "/home/user"},
                {"args": ["/a/b/c/../../../.."], "expected": "/"},
                {"args": ["//"], "expected": "/"},
                {"args": ["/.hidden/..x/."], "expected": "/.hidden/..x"},
            ],
            "hint": "Разбейте по '/' и ведите стек компонентов: '..' снимает вершину (если она есть), '' и '.' пропускаются.",
        },
        {
            "id": "fs-resolve-symlinks",
            "mode": "func",
            "func": "resolve",
            "title": "Цепочка символических ссылок",
            "statement": (
                "Напишите функцию resolve(links, path): links — словарь «путь "
                "ссылки → цель». Цель может быть абсолютной ('/etc/x') или "
                "относительной (разбирается относительно каталога, где лежит "
                "ссылка). Идите по цепочке, пока текущий путь является ссылкой; "
                "пути приводите к каноническому виду (как в normalize: '.', '..', "
                "'//'). Если цепочка длиннее 40 переходов — верните строку 'ELOOP'. "
                "Иначе — конечный путь."
            ),
            "starter": "def resolve(links, path):\n    pass\n",
            "tests": [
                {"args": [{"/bin/sh": "dash", "/bin/dash": "/usr/bin/dash"}, "/bin/sh"], "expected": "/usr/bin/dash"},
                {"args": [{"/a": "b", "/b": "c"}, "/a"], "expected": "/c"},
                {"args": [{"/a": "/b", "/b": "/a"}, "/a"], "expected": "ELOOP"},
                {"args": [{}, "/etc/../etc/passwd"], "expected": "/etc/passwd"},
                {"args": [{"/usr/lib/libx.so": "libx.so.1", "/usr/lib/libx.so.1": "../lib64/libx.so.1.2"}, "/usr/lib/libx.so"], "expected": "/usr/lib64/libx.so.1.2"},
                {"args": [{"/loop": "loop"}, "/loop"], "expected": "ELOOP"},
                {"args": [{"/x": "./y/../z"}, "/x"], "expected": "/z"},
            ],
            "hint": "Относительная цель = каталог ссылки + '/' + цель; перед каждым шагом нормализуйте путь; счётчик переходов защищает от циклов.",
        },
        {
            "id": "fs-inode-usage",
            "mode": "func",
            "func": "disk_usage",
            "title": "Куда делось место: иноды и ссылки",
            "statement": (
                "Напишите функцию disk_usage(ops): ops — операции над файловой "
                "системой. ['create', имя, размер] — новый файл (инод со счётчиком "
                "ссылок 1); ['link', новое_имя, имя] — жёсткая ссылка; ['unlink', "
                "имя] — удалить имя; ['open', дескриптор, имя] и ['close', "
                "дескриптор] — открыть и закрыть файл. Данные инода занимают место, "
                "пока у него есть хотя бы одно имя или хотя бы один открытый "
                "дескриптор. Верните число занятых байт после всех операций."
            ),
            "starter": "def disk_usage(ops):\n    pass\n",
            "tests": [
                {"args": [[["create", "a", 100]]], "expected": 100},
                {"args": [[["create", "a", 100], ["unlink", "a"]]], "expected": 0},
                {"args": [[["create", "log", 500], ["open", "h", "log"], ["unlink", "log"]]], "expected": 500},
                {"args": [[["create", "log", 500], ["open", "h", "log"], ["unlink", "log"], ["close", "h"]]], "expected": 0},
                {"args": [[["create", "a", 50], ["link", "b", "a"], ["unlink", "a"]]], "expected": 50},
                {"args": [[["create", "a", 50], ["link", "b", "a"], ["unlink", "a"], ["unlink", "b"]]], "expected": 0},
                {"args": [[["create", "a", 10], ["create", "b", 20], ["link", "c", "b"], ["unlink", "b"], ["open", "h1", "c"], ["open", "h2", "c"], ["unlink", "c"], ["close", "h1"]]], "expected": 30},
                {"args": [[]], "expected": 0},
            ],
            "hint": "Для каждого инода храните число имён (links) и открытых дескрипторов (open); инод исчезает, когда оба нуля.",
        },
        {
            "id": "fs-mount-lookup",
            "mode": "func",
            "func": "mount_device",
            "title": "Какой диск обслуживает путь",
            "statement": (
                "Напишите функцию mount_device(mounts, path): mounts — список пар "
                "[точка_монтирования, устройство], path — нормализованный "
                "абсолютный путь. Верните устройство той точки монтирования, "
                "которая является наибольшим по длине префиксом пути по границам "
                "компонентов ('/home' подходит для '/home/ann', но не для "
                "'/homework')."
            ),
            "starter": "def mount_device(mounts, path):\n    pass\n",
            "tests": [
                {"args": [[["/", "sda1"], ["/home", "sdb1"], ["/home/ann/backup", "sdc1"]], "/home/ann/backup/x"], "expected": "sdc1"},
                {"args": [[["/", "sda1"], ["/home", "sdb1"]], "/homework/a"], "expected": "sda1"},
                {"args": [[["/", "sda1"], ["/home", "sdb1"]], "/home"], "expected": "sdb1"},
                {"args": [[["/", "sda1"], ["/var", "sdb2"], ["/var/log", "sdb3"]], "/var/lib/db"], "expected": "sdb2"},
                {"args": [[["/", "sda1"]], "/"], "expected": "sda1"},
                {"args": [[["/", "sda1"], ["/mnt/usb", "sdd1"]], "/mnt"], "expected": "sda1"},
            ],
            "hint": "Подходит точка, если path равен ей или начинается с точка + '/'; корень '/' подходит всегда; выберите самую длинную.",
        },
        {
            "id": "fs-block-slack",
            "mode": "func",
            "func": "blocks_used",
            "title": "Блоки и потерянные хвосты",
            "statement": (
                "Файлы занимают целое число блоков. Напишите функцию "
                "blocks_used(sizes, block): sizes — размеры файлов в байтах, block "
                "— размер блока. Верните кортеж (всего_блоков, потеряно_байт): "
                "сколько блоков занято (пустой файл не занимает блоков) и сколько "
                "байт выделенного места не использовано (внутренняя фрагментация)."
            ),
            "starter": "def blocks_used(sizes, block):\n    pass\n",
            "tests": [
                {"args": [[0, 1, 4096, 4097], 4096], "expected": (4, 8190)},
                {"args": [[], 4096], "expected": (0, 0)},
                {"args": [[10, 10, 10], 512], "expected": (3, 1506)},
                {"args": [[8192], 4096], "expected": (2, 0)},
                {"args": [[1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000], 4096], "expected": (100, 309600)},
                {"args": [[5], 1], "expected": (5, 0)},
            ],
            "hint": "Блоков на файл — потолок размер / block; потери = блоки · block − размер.",
        },
        {
            "id": "fs-mount-options",
            "mode": "func",
            "func": "parse_options",
            "title": "Опции монтирования",
            "statement": (
                "Напишите функцию parse_options(opts): строка опций mount вида "
                "'rw,noexec,size=100m,uid=1000'. Верните словарь: опция без '=' — "
                "имя → True, с '=' — имя → значение-строка. Пустая строка — пустой "
                "словарь. Пробелов по краям нет."
            ),
            "starter": "def parse_options(opts):\n    pass\n",
            "tests": [
                {"args": ["rw,noexec,size=100m,uid=1000"], "expected": {"rw": True, "noexec": True, "size": "100m", "uid": "1000"}},
                {"args": [""], "expected": {}},
                {"args": ["ro"], "expected": {"ro": True}},
                {"args": ["defaults,x-systemd.automount"], "expected": {"defaults": True, "x-systemd.automount": True}},
                {"args": ["errors=remount-ro,data=ordered"], "expected": {"errors": "remount-ro", "data": "ordered"}},
                {"args": ["opt=a=b"], "expected": {"opt": "a=b"}},
            ],
            "hint": "Разбейте по запятым; каждый элемент — split('=', 1) (значение может само содержать '=').",
        },
        {
            "id": "fs-du-tree",
            "mode": "func",
            "func": "dir_sizes",
            "title": "Размеры каталогов (du)",
            "statement": (
                "Напишите функцию dir_sizes(tree): tree — вложенные словари; "
                "каталог — словарь «имя → содержимое», файл — пара [инод, размер]. "
                "Верните словарь «путь каталога → суммарный размер» для корня '/' и "
                "всех вложенных каталогов. Как и du, считайте каждый инод один раз "
                "за весь обход: обходите имена в алфавитном порядке, байты "
                "зачисляются каталогу, где инод встретился первым (и всем его "
                "родителям)."
            ),
            "starter": "def dir_sizes(tree):\n    pass\n",
            "tests": [
                {"args": [{"etc": {"hosts": [1, 100], "passwd": [2, 200]}, "var": {"log": {"a": [3, 1000]}}}], "expected": {"/etc": 300, "/var/log": 1000, "/var": 1000, "/": 1300}},
                {"args": [{"a": [1, 10], "b": [1, 10]}], "expected": {"/": 10}},
                {"args": [{"bin": {"ls": [1, 50]}, "usr": {"bin": {"ls2": [1, 50], "cat": [2, 30]}}}], "expected": {"/bin": 50, "/usr/bin": 30, "/usr": 30, "/": 80}},
                {"args": [{}], "expected": {"/": 0}},
                {"args": [{"d": {"e": {"f": {}}}}], "expected": {"/d/e/f": 0, "/d/e": 0, "/d": 0, "/": 0}},
            ],
            "hint": "Рекурсия по словарю: сумма размеров непосещённых инодов + суммы вложенных каталогов; множество seen общее на весь обход.",
        },
        {
            "id": "fs-meminfo",
            "mode": "func",
            "func": "used_percent",
            "title": "Читаем /proc/meminfo",
            "statement": (
                "Напишите функцию used_percent(text): text — содержимое "
                "/proc/meminfo (строки вида 'MemTotal:       16384000 kB'). Верните "
                "процент используемой памяти (MemTotal − MemAvailable) / MemTotal · "
                "100, округлённый до одного знака."
            ),
            "starter": "def used_percent(text):\n    pass\n",
            "tests": [
                {"args": ["MemTotal:       16384000 kB\nMemFree:         1000000 kB\nMemAvailable:    8192000 kB\nBuffers:          500 kB\n"], "expected": 50.0},
                {"args": ["MemTotal: 1000 kB\nMemAvailable: 1000 kB\n"], "expected": 0.0},
                {"args": ["MemFree: 5 kB\nMemTotal: 2000 kB\nMemAvailable: 500 kB\nSwapTotal: 0 kB\n"], "expected": 75.0},
                {"args": ["MemTotal:  3 kB\nMemAvailable:   1 kB\n"], "expected": 66.7},
            ],
            "hint": "Разберите строки в словарь «ключ → число»; единицы (kB) сокращаются в отношении.",
        },
    ],
    2: [
        {
            "id": "sh-split-words",
            "mode": "func",
            "func": "split_words",
            "title": "Разбор командной строки",
            "statement": (
                "Напишите функцию split_words(line): разбейте строку на слова как "
                "шелл. Слова разделены пробелами; внутри одинарных кавычек всё "
                "буквально; внутри двойных — тоже, но \\\" и \\\\ дают кавычку и "
                "обратный слэш; вне кавычек обратный слэш делает следующий символ "
                "обычным. Соседние куски без пробелов склеиваются (a\"b c\"d → 'ab "
                "cd'). Кавычки в результат не попадают. Незакрытых кавычек в тестах "
                "нет."
            ),
            "starter": "def split_words(line):\n    pass\n",
            "tests": [
                {"args": ["ls -la /tmp"], "expected": ["ls", "-la", "/tmp"]},
                {"args": ["echo 'hello   world' x"], "expected": ["echo", "hello   world", "x"]},
                {"args": ["echo \"a b\" c\\ d"], "expected": ["echo", "a b", "c d"]},
                {"args": ["say \"he said \\\"hi\\\"\""], "expected": ["say", "he said \"hi\""]},
                {"args": ["a\"b c\"d"], "expected": ["ab cd"]},
                {"args": [""], "expected": []},
                {"args": ["   "], "expected": []},
                {"args": ["''"], "expected": [""]},
                {"args": ["echo \\$HOME '$HOME'"], "expected": ["echo", "$HOME", "$HOME"]},
            ],
            "hint": "Одно движение по строке с индексом и признаком «слово начато» (пустые кавычки '' тоже создают пустое слово).",
        },
        {
            "id": "sh-pipeline",
            "mode": "func",
            "func": "run_pipeline",
            "title": "Свой конвейер из команд",
            "statement": (
                "Напишите функцию run_pipeline(stages, text): text — входной текст, "
                "stages — список команд (каждая — список слов), выход одной "
                "подаётся на вход следующей. Команды: ['grep', шаблон] и ['grep', "
                "'-v', шаблон] (строки, содержащие / не содержащие подстроку); "
                "['sort'], ['sort', '-r'], ['sort', '-n'] (по числу в начале "
                "строки, нечисловое = 0; при равенстве — по строке), ['uniq'] "
                "(склеить подряд идущие одинаковые), ['uniq', '-c'] (с числом: "
                "счётчик, выровненный вправо в 7 символов, пробел, строка); "
                "['head', '-n', N], ['tail', '-n', N]; ['wc', '-l'] (число строк "
                "одной строкой); ['cut', '-d', разделитель, '-f', номер] (поле с "
                "1). Вход и выход — строки, разделённые '\\n', без завершающего "
                "'\\n'. Пустой вход — пустой список строк."
            ),
            "starter": "import re\n\n\ndef run_pipeline(stages, text):\n    pass\n",
            "tests": [
                {"args": [[["grep", "err"], ["wc", "-l"]], "ok\nerr 1\nok\nerr 2"], "expected": "2"},
                {"args": [[["sort"], ["uniq", "-c"]], "b\na\nb\nc\na\nb"], "expected": "      2 a\n      3 b\n      1 c"},
                {"args": [[["sort"], ["uniq", "-c"], ["sort", "-n"], ["tail", "-n", "1"]], "x\ny\nx\nz\nx\ny"], "expected": "      3 x"},
                {"args": [[["cut", "-d", ":", "-f", "1"], ["sort", "-r"], ["head", "-n", "2"]], "root:x:0\nann:x:1000\nbob:x:1001"], "expected": "root\nbob"},
                {"args": [[["grep", "-v", "#"]], "# comment\nkey=1\n# x\nkey=2"], "expected": "key=1\nkey=2"},
                {"args": [[["sort", "-n"]], "10 b\n9 a\n100 c\nzzz\n-5 d"], "expected": "-5 d\nzzz\n9 a\n10 b\n100 c"},
                {"args": [[["uniq"]], "a\na\nb\na\na"], "expected": "a\nb\na"},
                {"args": [[["wc", "-l"]], ""], "expected": "0"},
                {"args": [[["cut", "-d", ",", "-f", "3"]], "a,b,c\nx,y\n1,2,3"], "expected": "c\n\n3"},
            ],
            "hint": "Преобразуйте входной текст в список строк и пропускайте его через команды по очереди; для sort -n используйте ключ (число, строка).",
        },
        {
            "id": "sh-glob",
            "mode": "func",
            "func": "glob_match",
            "title": "Шаблоны имён (glob)",
            "statement": (
                "Напишите функцию glob_match(pattern, name) без fnmatch и re: '*' — "
                "любая последовательность (в том числе пустая), '?' — один любой "
                "символ, '[abc]' и '[a-z]' — один символ из набора/диапазона, "
                "'[!abc]' — один символ не из набора. Остальные символы совпадают "
                "буквально. Весь name должен соответствовать шаблону."
            ),
            "starter": "def glob_match(pattern, name):\n    pass\n",
            "tests": [
                {"args": ["*.txt", "notes.txt"], "expected": True},
                {"args": ["*.txt", "notes.txt.bak"], "expected": False},
                {"args": ["file?.log", "file1.log"], "expected": True},
                {"args": ["file?.log", "file12.log"], "expected": False},
                {"args": ["[abc]*", "banana"], "expected": True},
                {"args": ["[!abc]*", "banana"], "expected": False},
                {"args": ["[a-c]x", "bx"], "expected": True},
                {"args": ["[0-9][0-9]", "42"], "expected": True},
                {"args": ["*", ""], "expected": True},
                {"args": ["a*b*c", "aXXbYYc"], "expected": True},
                {"args": ["a*b*c", "aXXbYY"], "expected": False},
                {"args": ["", ""], "expected": True},
                {"args": ["?", ""], "expected": False},
            ],
            "hint": "Рекурсия по позициям (pattern, name): '*' пробует все варианты сколько символов съесть; для набора найдите ']' и проверьте диапазоны a-z.",
        },
        {
            "id": "sh-sed-subst",
            "mode": "func",
            "func": "sed_s",
            "title": "sed s/старое/новое/",
            "statement": (
                "Напишите функцию sed_s(text, expr): expr — 's/старое/новое/' или "
                "'s/старое/новое/g' (разделитель всегда '/', 'старое' и 'новое' — "
                "обычные строки без спецсимволов; 'старое' непустое). Для каждой "
                "строки текста замените первое вхождение (без g) или все (с g). "
                "Строки в тексте разделены '\\n'."
            ),
            "starter": "def sed_s(text, expr):\n    pass\n",
            "tests": [
                {"args": ["foo foo\nbar foo", "s/foo/X/"], "expected": "X foo\nbar X"},
                {"args": ["foo foo\nbar foo", "s/foo/X/g"], "expected": "X X\nbar X"},
                {"args": ["a.b.c", "s/./-/g"], "expected": "a-b-c"},
                {"args": ["none", "s/x/y/g"], "expected": "none"},
                {"args": ["aaa", "s/aa/b/g"], "expected": "ba"},
                {"args": ["", "s/a/b/"], "expected": ""},
                {"args": ["path/to", "s/o//g"], "expected": "path/t"},
            ],
            "hint": "expr.split('/') даёт ['s', старое, новое, флаги]; str.replace с ограничением числа замен.",
        },
        {
            "id": "sh-awk-sum",
            "mode": "func",
            "func": "column_sum",
            "title": "Сумма столбца (awk)",
            "statement": (
                "Напишите функцию column_sum(text, col): text — строки с полями "
                "через пробелы/табуляции, col — номер столбца с 1. Просуммируйте "
                "числа (целые или дробные) этого столбца; строки, где такого "
                "столбца нет или в нём не число, пропускайте. Верните сумму, "
                "округлённую до двух знаков (float)."
            ),
            "starter": "def column_sum(text, col):\n    pass\n",
            "tests": [
                {"args": ["a 1\nb 2\nc 3.5", 2], "expected": 6.5},
                {"args": ["x 10\ny\nz abc\nw 5", 2], "expected": 15.0},
                {"args": ["1 2 3\n4 5 6", 3], "expected": 9.0},
                {"args": ["", 1], "expected": 0.0},
                {"args": ["a\tb\t7", 3], "expected": 7.0},
                {"args": ["  5   6  ", 1], "expected": 5.0},
                {"args": ["n 0.1\nn 0.2", 2], "expected": 0.3},
            ],
            "hint": "split() без аргументов делит по любым пробельным символам; float() + except ValueError для нечисловых.",
        },
        {
            "id": "sh-pipeline-status",
            "mode": "func",
            "func": "pipeline_status",
            "title": "Код возврата конвейера",
            "statement": (
                "Напишите функцию pipeline_status(codes, pipefail): codes — коды "
                "выхода команд конвейера слева направо. Без pipefail результат — "
                "код последней команды; с pipefail — код самой правой команды, "
                "завершившейся с ненулевым кодом (или 0, если все нули). Пустой "
                "конвейер — 0."
            ),
            "starter": "def pipeline_status(codes, pipefail):\n    pass\n",
            "tests": [
                {"args": [[0, 0, 0], False], "expected": 0},
                {"args": [[1, 0], False], "expected": 0},
                {"args": [[1, 0], True], "expected": 1},
                {"args": [[2, 3, 0], True], "expected": 3},
                {"args": [[0, 5, 0, 7, 0], True], "expected": 7},
                {"args": [[], True], "expected": 0},
                {"args": [[127], False], "expected": 127},
                {"args": [[0, 0], True], "expected": 0},
            ],
            "hint": "Проход справа налево до первого ненулевого кода.",
        },
        {
            "id": "sh-expand-vars",
            "mode": "func",
            "func": "expand",
            "title": "Подстановка переменных",
            "statement": (
                "Напишите функцию expand(template, env): env — словарь переменных. "
                "Подставьте $NAME, ${NAME} и ${NAME:-запасное} (запасное "
                "используется, если переменной нет или она пустая). Имя — буквы, "
                "цифры и '_', не начинается с цифры. Неизвестная переменная "
                "превращается в пустую строку. Остальной текст не меняется."
            ),
            "starter": "import re\n\n\ndef expand(template, env):\n    pass\n",
            "tests": [
                {"args": ["Hello, $USER!", {"USER": "ann"}], "expected": "Hello, ann!"},
                {"args": ["${A}_${B}", {"A": "x", "B": "y"}], "expected": "x_y"},
                {"args": ["${HOME:-/tmp}/f", {}], "expected": "/tmp/f"},
                {"args": ["${HOME:-/tmp}/f", {"HOME": ""}], "expected": "/tmp/f"},
                {"args": ["${HOME:-/tmp}/f", {"HOME": "/root"}], "expected": "/root/f"},
                {"args": ["$X$Y", {"X": "1"}], "expected": "1"},
                {"args": ["price: $5", {}], "expected": "price: $5"},
                {"args": ["no vars", {"A": "1"}], "expected": "no vars"},
                {"args": ["$A_B", {"A": "1", "A_B": "2"}], "expected": "2"},
            ],
            "hint": "Один re.sub с шаблоном для $имя и ${имя[:-запасное]}.",
        },
        {
            "id": "sh-top-commands",
            "mode": "func",
            "func": "top_commands",
            "title": "Топ команд из истории",
            "statement": (
                "Напишите функцию top_commands(history, n): history — строки вида ' "
                "101  git status' (номер, затем команда). Определите первое слово "
                "команды, посчитайте и верните список [команда, число] из n самых "
                "частых: по убыванию числа, при равенстве — по алфавиту. Пустые "
                "строки пропускайте."
            ),
            "starter": "from collections import Counter\n\n\ndef top_commands(history, n):\n    pass\n",
            "tests": [
                {"args": [["  1  git status", "  2  ls -la", "  3  git diff", "  4  git add .", "  5  ls"], 2], "expected": [["git", 3], ["ls", 2]]},
                {"args": [["1 a", "2 b", "3 b", "4 a", "5 c"], 3], "expected": [["a", 2], ["b", 2], ["c", 1]]},
                {"args": [[], 5], "expected": []},
                {"args": [["", "  ", "1 x"], 1], "expected": [["x", 1]]},
                {"args": [["1 ls", "2 ls", "3 cd"], 10], "expected": [["ls", 2], ["cd", 1]]},
            ],
            "hint": "Номер пропускаем (parts[1] — команда); sorted по ключу (−число, имя).",
        },
    ],
}
