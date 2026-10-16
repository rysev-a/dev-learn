"""Задачи книги «Базы данных»: глава 30."""

TASKS: dict[int, list[dict]] = {30: [{'id': 'd14-add-column',
  'mode': 'sql',
  'title': 'Добавить столбец',
  'statement': 'Добавьте в users столбец active INTEGER NOT NULL DEFAULT 1. Итог проверяется по содержимому '
               'таблицы.',
  'starter': '-- миграция: новый столбец\nALTER TABLE users\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT, city TEXT);\n'
           'INSERT INTO users VALUES '
           "(1,'Анна','a@x.ru','Москва'),(2,'Борис','b@x.ru','Казань'),(3,'Вера',NULL,'Москва'),(4,'Глеб','g@x.ru',NULL),(5,'Дарья','a@x.ru','Тверь');\n",
  'expected': [[1, 'Анна', 1], [2, 'Борис', 1], [3, 'Вера', 1], [4, 'Глеб', 1], [5, 'Дарья', 1]],
  'expected_cols': ['id', 'name', 'active'],
  'hint': 'ALTER TABLE users ADD COLUMN active INTEGER NOT NULL DEFAULT 1;',
  'ordered': True,
  'check': 'SELECT id, name, active FROM users ORDER BY id'},
 {'id': 'd14-rename-column',
  'mode': 'sql',
  'title': 'Переименовать столбец',
  'statement': 'Переименуйте столбец name в full_name (RENAME COLUMN). Итог проверяется выборкой по новому '
               'имени.',
  'starter': '-- переименование\nALTER TABLE users\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT, city TEXT);\n'
           'INSERT INTO users VALUES '
           "(1,'Анна','a@x.ru','Москва'),(2,'Борис','b@x.ru','Казань'),(3,'Вера',NULL,'Москва'),(4,'Глеб','g@x.ru',NULL),(5,'Дарья','a@x.ru','Тверь');\n",
  'expected': [[1, 'Анна'], [2, 'Борис'], [3, 'Вера'], [4, 'Глеб'], [5, 'Дарья']],
  'expected_cols': ['id', 'full_name'],
  'hint': 'ALTER TABLE users RENAME COLUMN name TO full_name;',
  'ordered': True,
  'check': 'SELECT id, full_name FROM users ORDER BY id'},
 {'id': 'd14-expand-backfill',
  'mode': 'sql',
  'title': 'Расширить и заполнить',
  'statement': 'Расширьте схему: добавьте столбец email_norm TEXT и заполните его почтой в нижнем регистре '
               '(NULL остаётся NULL). Итог проверяется выборкой id, email_norm.',
  'starter': '-- expand + backfill\nALTER TABLE users\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT, city TEXT);\n'
           'INSERT INTO users VALUES '
           "(1,'Анна','a@x.ru','Москва'),(2,'Борис','b@x.ru','Казань'),(3,'Вера',NULL,'Москва'),(4,'Глеб','g@x.ru',NULL),(5,'Дарья','a@x.ru','Тверь');\n",
  'expected': [[1, 'a@x.ru'], [2, 'b@x.ru'], [3, None], [4, 'g@x.ru'], [5, 'a@x.ru']],
  'expected_cols': ['id', 'email_norm'],
  'hint': 'Сначала ADD COLUMN, затем UPDATE … SET email_norm = lower(email).',
  'ordered': True,
  'check': 'SELECT id, email_norm FROM users ORDER BY id'},
 {'id': 'd14-batch-update',
  'mode': 'sql',
  'title': 'Обновление порцией',
  'statement': 'Перенесите данные порциями: пометьте migrated = 1 только у строк с id от 1 до 4 включительно '
               '(первая порция по ключу). Итог проверяется по таблице.',
  'starter': '-- первая порция\nUPDATE t\n',
  'setup': 'CREATE TABLE t (id INTEGER PRIMARY KEY, v INTEGER, migrated INTEGER NOT NULL DEFAULT 0);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 10) INSERT INTO t (id, '
           'v) SELECT i, i * 10 FROM n;\n',
  'expected': [[1, 1], [2, 1], [3, 1], [4, 1], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0]],
  'expected_cols': ['id', 'migrated'],
  'hint': 'UPDATE … WHERE id BETWEEN 1 AND 4.',
  'ordered': True,
  'check': 'SELECT id, migrated FROM t ORDER BY id'},
 {'id': 'd14-resume-batch',
  'mode': 'sql',
  'title': 'Продолжить с места остановки',
  'statement': 'Перенос остановился: строки до id 4 уже мигрированы. Мигрируйте следующую порцию из 3 строк, '
               'не трогая уже сделанные (без жёсткого указания границ, через подзапрос по MIN(id) среди '
               'немигрированных). Итог — по таблице.',
  'starter': '-- продолжение с последнего ключа\nUPDATE t\n',
  'setup': 'CREATE TABLE t (id INTEGER PRIMARY KEY, v INTEGER, migrated INTEGER NOT NULL DEFAULT 0);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 10) INSERT INTO t (id, '
           'v) SELECT i, i * 10 FROM n;\n'
           'UPDATE t SET migrated = 1 WHERE id <= 4;\n',
  'expected': [[1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 0], [9, 0], [10, 0]],
  'expected_cols': ['id', 'migrated'],
  'hint': 'Выберите id из немигрированных с ORDER BY id LIMIT 3 и обновите по IN.',
  'ordered': True,
  'check': 'SELECT id, migrated FROM t ORDER BY id'},
 {'id': 'd14-dedupe-before-unique',
  'mode': 'sql',
  'title': 'Дубли перед уникальным индексом',
  'statement': 'Прежде чем создать уникальный индекс по email, удалите дубликаты почты, оставив строку с '
               'наименьшим id (NULL-почты не трогать). Затем создайте индекс uq_users_email. Итог '
               'проверяется по таблице.',
  'starter': '-- чистим дубликаты и создаём индекс\nDELETE FROM users\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT, city TEXT);\n'
           'INSERT INTO users VALUES '
           "(1,'Анна','a@x.ru','Москва'),(2,'Борис','b@x.ru','Казань'),(3,'Вера',NULL,'Москва'),(4,'Глеб','g@x.ru',NULL),(5,'Дарья','a@x.ru','Тверь');\n",
  'expected': [[1, 'a@x.ru'], [2, 'b@x.ru'], [3, None], [4, 'g@x.ru']],
  'expected_cols': ['id', 'email'],
  'hint': 'DELETE строк, у которых id не минимальный в группе по email; затем CREATE UNIQUE INDEX.',
  'ordered': True,
  'check': 'SELECT id, email FROM users ORDER BY id'},
 {'id': 'd14-find-duplicates',
  'mode': 'sql',
  'title': 'Найти дубликаты',
  'statement': 'Выведите почты, которые встречаются более одного раза, и число повторов: колонки email, n; '
               'по почте.',
  'starter': '-- дубли\nSELECT\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT, city TEXT);\n'
           'INSERT INTO users VALUES '
           "(1,'Анна','a@x.ru','Москва'),(2,'Борис','b@x.ru','Казань'),(3,'Вера',NULL,'Москва'),(4,'Глеб','g@x.ru',NULL),(5,'Дарья','a@x.ru','Тверь');\n",
  'expected': [['a@x.ru', 2]],
  'expected_cols': ['email', 'n'],
  'hint': 'GROUP BY email HAVING COUNT(*) > 1; NULL исключите.',
  'ordered': True},
 {'id': 'd14-rebuild-table',
  'mode': 'sql',
  'title': 'Пересборка таблицы',
  'statement': 'В SQLite тип столбца меняют пересборкой. Создайте items_new(id INTEGER PRIMARY KEY, title '
               'TEXT NOT NULL, price INTEGER NOT NULL), перенесите данные с CAST, удалите items и '
               'переименуйте items_new в items. Итог проверяется по items и по типам столбцов.',
  'starter': '-- таблица пересобирается\nCREATE TABLE items_new\n',
  'setup': 'CREATE TABLE items (id INTEGER PRIMARY KEY, title TEXT, price TEXT);\n'
           "INSERT INTO items VALUES (1,'Чай','120'),(2,'Кофе','300'),(3,'Сыр','350');\n",
  'expected': [[1, 'Чай', 120, 'integer'], [2, 'Кофе', 300, 'integer'], [3, 'Сыр', 350, 'integer']],
  'expected_cols': ['id', 'title', 'price', 't'],
  'hint': 'Создать новую, INSERT … SELECT с CAST, DROP старой, RENAME новой.',
  'ordered': True,
  'check': 'SELECT id, title, price, typeof(price) AS t FROM items ORDER BY id'},
 {'id': 'd14-migrations-table',
  'mode': 'sql',
  'title': 'Таблица версий миграций',
  'statement': 'Создайте служебную таблицу schema_migrations(version TEXT PRIMARY KEY, applied_at TEXT NOT '
               "NULL) и запишите в неё две применённые версии: '001' (applied_at '2026-01-10') и '002' "
               "(applied_at '2026-02-01'). Итог проверяется по таблице.",
  'starter': '-- служебная таблица\nCREATE TABLE schema_migrations\n',
  'setup': '',
  'expected': [['001', '2026-01-10'], ['002', '2026-02-01']],
  'expected_cols': ['version', 'applied_at'],
  'hint': 'CREATE TABLE с первичным ключом по version и INSERT двух строк.',
  'ordered': True,
  'check': 'SELECT version, applied_at FROM schema_migrations ORDER BY version'},
 {'id': 'd14-pending',
  'mode': 'sql',
  'title': 'Какие миграции осталось применить',
  'statement': 'Выведите версии и названия миграций из available, которых ещё нет в schema_migrations: '
               'колонки version, name; по версии.',
  'starter': '-- ожидающие миграции\nSELECT\n',
  'setup': 'CREATE TABLE available (version TEXT PRIMARY KEY, name TEXT);\n'
           'CREATE TABLE schema_migrations (version TEXT PRIMARY KEY, applied_at TEXT);\n'
           "INSERT INTO available VALUES ('001','users'),('002','orders'),('003','index'),('004','audit');\n"
           "INSERT INTO schema_migrations VALUES ('001','d1'),('002','d2');\n",
  'expected': [['003', 'index'], ['004', 'audit']],
  'expected_cols': ['version', 'name'],
  'hint': 'LEFT JOIN и фильтр m.version IS NULL, или NOT EXISTS.',
  'ordered': True},
 {'id': 'd14-consistency-check',
  'mode': 'sql',
  'title': 'Сверка после переноса',
  'statement': 'Сравните old_t и new_t по id: выведите расхождения — колонки id, issue, где issue — '
               "'missing' (есть в old_t, нет в new_t), 'extra' (есть в new_t, нет в old_t) или 'diff' "
               '(значения v различаются); по id.',
  'starter': '-- сверка таблиц\nSELECT\n',
  'setup': 'CREATE TABLE old_t (id INTEGER PRIMARY KEY, v INTEGER);\n'
           'CREATE TABLE new_t (id INTEGER PRIMARY KEY, v INTEGER);\n'
           'INSERT INTO old_t VALUES (1,10),(2,20),(3,30),(4,40);\n'
           'INSERT INTO new_t VALUES (1,10),(2,21),(4,40),(5,50);\n',
  'expected': [[2, 'diff'], [3, 'missing'], [5, 'extra']],
  'expected_cols': ['id', 'issue'],
  'hint': 'Три выборки через UNION ALL: left-anti, right-anti и различие значений.',
  'ordered': True},
 {'id': 'd14-checksum',
  'mode': 'sql',
  'title': 'Контрольная сумма таблицы',
  'statement': 'Выведите «контрольную сумму» таблицы: n — число строк и s — сумма id·v (колонки n, s).',
  'starter': '-- контрольная сумма\nSELECT\n',
  'setup': 'CREATE TABLE t (id INTEGER PRIMARY KEY, v INTEGER);\n'
           'INSERT INTO t VALUES (1,10),(2,20),(3,30);\n',
  'expected': [[3, 140]],
  'expected_cols': ['n', 's'],
  'hint': 'COUNT(*) и SUM(id * v).'},
 {'id': 'd14-dump-inserts',
  'mode': 'sql',
  'title': 'Логическая копия',
  'statement': "Постройте дамп: выведите по одной строке INSERT INTO t VALUES (id, 'name'); для каждой "
               'строки (колонка stmt, по id). Строки экранируйте функцией quote(); NULL должен выводиться '
               'как NULL.',
  'starter': '-- INSERT-ы из данных\nSELECT\n',
  'setup': 'CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT);\n'
           "INSERT INTO t VALUES (1,'Анна'),(2,'О''Брайен'),(3,NULL);\n",
  'expected': [["INSERT INTO t VALUES (1, 'Анна');"],
               ["INSERT INTO t VALUES (2, 'О''Брайен');"],
               ['INSERT INTO t VALUES (3, NULL);']],
  'expected_cols': ['stmt'],
  'hint': 'quote(name) сам добавляет кавычки и экранирует апострофы; для NULL даёт слово NULL.',
  'ordered': True},
 {'id': 'd14-soft-archive',
  'mode': 'sql',
  'title': 'Архивирование перед удалением',
  'statement': 'Перенесите заказы старше created = 250 в orders_archive и удалите их из orders. Итог '
               'проверяется по обеим таблицам.',
  'starter': '-- архивирование\nINSERT INTO orders_archive\n',
  'setup': 'CREATE TABLE orders (id INTEGER PRIMARY KEY, created INTEGER, total INTEGER);\n'
           'CREATE TABLE orders_archive (id INTEGER PRIMARY KEY, created INTEGER, total INTEGER);\n'
           'INSERT INTO orders VALUES (1,100,10),(2,200,20),(3,300,30),(4,400,40);\n',
  'expected': [['archive', 1], ['archive', 2], ['orders', 3], ['orders', 4]],
  'expected_cols': ['t', 'id'],
  'hint': 'INSERT … SELECT с условием, затем DELETE с тем же условием.',
  'ordered': True,
  'check': "SELECT 'orders' AS t, id FROM orders UNION ALL SELECT 'archive', id FROM orders_archive ORDER BY "
           '1, 2'},
 {'id': 'd14-add-not-null',
  'mode': 'sql',
  'title': 'NOT NULL в два шага',
  'statement': "Столбец city в users пока допускает NULL. Сначала заполните пропуски значением 'unknown' "
               '(UPDATE), затем проверьте результат: итог проверяется выборкой city по id. (В SQLite NOT '
               'NULL задним числом добавляют пересборкой — здесь достаточно первого шага.)',
  'starter': '-- шаг 1: заполнить пропуски\nUPDATE users\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT, city TEXT);\n'
           'INSERT INTO users VALUES '
           "(1,'Анна','a@x.ru','Москва'),(2,'Борис','b@x.ru','Казань'),(3,'Вера',NULL,'Москва'),(4,'Глеб','g@x.ru',NULL),(5,'Дарья','a@x.ru','Тверь');\n",
  'expected': [[1, 'Москва'], [2, 'Казань'], [3, 'Москва'], [4, 'unknown'], [5, 'Тверь']],
  'expected_cols': ['id', 'city'],
  'hint': "UPDATE users SET city = 'unknown' WHERE city IS NULL;",
  'ordered': True,
  'check': 'SELECT id, city FROM users ORDER BY id'},
 {'id': 'd14-runner',
  'mode': 'func',
  'func': 'pending_migrations',
  'title': 'Что применить',
  'statement': 'Доступные миграции — список версий (строки) в произвольном порядке, применённые — список '
               'версий. Напишите pending_migrations(available, applied): отсортированный список версий, '
               'которые ещё не применены. Если среди применённых есть версия, которой нет в available, '
               "вернуть строку 'error: unknown <версия>' (самую меньшую).",
  'starter': 'def pending_migrations(available, applied):\n    pass\n',
  'tests': [{'args': [['003', '001', '002'], ['001']], 'expected': ['002', '003']},
            {'args': [['001'], ['001']], 'expected': []},
            {'args': [['001', '002'], ['003']], 'expected': 'error: unknown 003'},
            {'args': [[], []], 'expected': []}],
  'hint': 'Разность множеств; проверка на неизвестные применённые версии.'},
 {'id': 'd14-checksum-edit',
  'mode': 'func',
  'func': 'edited_migrations',
  'title': 'Правка применённой миграции',
  'statement': 'applied — словарь «версия → контрольная сумма при применении», files — словарь «версия → '
               'текущая сумма файла». Напишите edited_migrations(applied, files): отсортированный список '
               'версий, у которых сумма изменилась (файл правили после применения), а также версий, чей файл '
               'пропал.',
  'starter': 'def edited_migrations(applied, files):\n    pass\n',
  'tests': [{'args': [{'001': 'a', '002': 'b'}, {'001': 'a', '002': 'x'}], 'expected': ['002']},
            {'args': [{'001': 'a'}, {}], 'expected': ['001']},
            {'args': [{}, {'001': 'a'}], 'expected': []},
            {'args': [{'001': 'a'}, {'001': 'a', '002': 'b'}], 'expected': []}],
  'hint': 'Сравните files.get(версия) с суммой при применении.'},
 {'id': 'd14-topo-migrations',
  'mode': 'func',
  'func': 'order_migrations',
  'title': 'Порядок миграций по зависимостям',
  'statement': 'Миграции — словарь «имя → список имён, от которых зависит». Напишите order_migrations(deps): '
               'порядок применения (зависимости раньше), при выборе из готовых — по алфавиту. Если есть цикл '
               '— вернуть None.',
  'starter': 'def order_migrations(deps):\n    pass\n',
  'tests': [{'args': [{'c': ['a', 'b'], 'b': ['a'], 'a': []}], 'expected': ['a', 'b', 'c']},
            {'args': [{'a': ['b'], 'b': ['a']}], 'expected': None},
            {'args': [{'x': [], 'y': []}], 'expected': ['x', 'y']},
            {'args': [{}], 'expected': []}],
  'hint': 'Топологическая сортировка: берите готовые (без зависимостей) по алфавиту; нет готовых — цикл.'},
 {'id': 'd14-lint-migration',
  'mode': 'func',
  'func': 'lint_migration',
  'title': 'Линтер опасных операций',
  'statement': 'Миграция — список строк SQL. Напишите lint_migration(statements): отсортированный список '
               "предупреждений без повторов: 'drop-column' для ALTER … DROP COLUMN, 'create-index-blocking' "
               "для CREATE INDEX без слова CONCURRENTLY, 'update-no-where' для UPDATE без WHERE, "
               "'drop-table' для DROP TABLE. Регистр не важен.",
  'starter': 'def lint_migration(statements):\n    pass\n',
  'tests': [{'args': [['ALTER TABLE t DROP COLUMN x;', 'create index i on t(a);', 'UPDATE t SET a = 1;']],
             'expected': ['create-index-blocking', 'drop-column', 'update-no-where']},
            {'args': [['CREATE INDEX CONCURRENTLY i ON t(a);', 'UPDATE t SET a=1 WHERE id=1;']],
             'expected': []},
            {'args': [['drop table x;', 'DROP TABLE y;']], 'expected': ['drop-table']},
            {'args': [[]], 'expected': []}],
  'hint': 'Приведите строку к верхнему регистру и ищите ключевые слова.'},
 {'id': 'd14-backfill-batches',
  'mode': 'func',
  'func': 'batch_ranges',
  'title': 'Диапазоны порций',
  'statement': 'Нужно обработать идентификаторы от first до last включительно порциями по size. Напишите '
               'batch_ranges(first, last, size): список пар [начало, конец] включительно; последняя порция '
               'может быть короче; если first > last — пустой список.',
  'starter': 'def batch_ranges(first, last, size):\n    pass\n',
  'tests': [{'args': [1, 10, 4], 'expected': [[1, 4], [5, 8], [9, 10]]},
            {'args': [5, 5, 3], 'expected': [[5, 5]]},
            {'args': [10, 1, 5], 'expected': []},
            {'args': [1, 9, 3], 'expected': [[1, 3], [4, 6], [7, 9]]}],
  'hint': 'Цикл: конец порции = min(начало + size − 1, last).'},
 {'id': 'd14-resume',
  'mode': 'func',
  'func': 'resume_point',
  'title': 'Откуда продолжить',
  'statement': "Журнал порций — список [начало, конец, статус], статус 'ok' или 'fail'. Напишите "
               'resume_point(log, first): с какого идентификатора продолжить — конец последней подряд '
               'успешной порции от начала плюс 1; если первая порция не успешна или журнал пуст — first. '
               'Порции идут по порядку без пропусков.',
  'starter': 'def resume_point(log, first):\n    pass\n',
  'tests': [{'args': [[[1, 4, 'ok'], [5, 8, 'ok'], [9, 12, 'fail']], 1], 'expected': 9},
            {'args': [[], 1], 'expected': 1},
            {'args': [[[1, 4, 'fail']], 1], 'expected': 1},
            {'args': [[[10, 19, 'ok']], 10], 'expected': 20}],
  'hint': 'Идите по журналу, пока статус ok, и запоминайте конец + 1.'},
 {'id': 'd14-expand-contract',
  'mode': 'func',
  'func': 'expand_contract_ok',
  'title': 'Совместимость шагов',
  'statement': "Релиз — словарь {'writes': множество столбцов, куда пишет код, 'reads': множество столбцов, "
               'откуда читает}. Схема — множество существующих столбцов. Релиз совместим со схемой, если все '
               'писанные и читаемые столбцы существуют. Напишите expand_contract_ok(schema, releases): '
               "список True/False для каждого релиза в порядке (ключи 'writes' и 'reads' — списки).",
  'starter': 'def expand_contract_ok(schema, releases):\n    pass\n',
  'tests': [{'args': [['name', 'full_name'],
                      [{'writes': ['name'], 'reads': ['name']},
                       {'writes': ['name', 'full_name'], 'reads': ['name']},
                       {'writes': ['full_name'], 'reads': ['full_name']}]],
             'expected': [True, True, True]},
            {'args': [['name'], [{'writes': ['full_name'], 'reads': ['name']}]], 'expected': [False]},
            {'args': [[], []], 'expected': []}],
  'hint': 'Подмножество: set(writes) <= schema и set(reads) <= schema.'},
 {'id': 'd14-pitr',
  'mode': 'func',
  'func': 'restore_to',
  'title': 'Восстановление на момент',
  'statement': 'База — словарь «ключ → значение». Копия snapshot сделана в момент 0. Журнал — список записей '
               "[время, операция, ключ, значение] по возрастанию времени, операция 'set' или 'del'. Напишите "
               'restore_to(snapshot, wal, t): состояние на момент t (записи со временем ≤ t применяются). '
               'Исходный snapshot не менять.',
  'starter': 'def restore_to(snapshot, wal, t):\n    pass\n',
  'tests': [{'args': [{'a': 1}, [[1, 'set', 'b', 2], [2, 'del', 'a', None], [3, 'set', 'a', 9]], 2],
             'expected': {'b': 2}},
            {'args': [{'a': 1}, [[5, 'set', 'b', 2]], 0], 'expected': {'a': 1}},
            {'args': [{}, [], 10], 'expected': {}},
            {'args': [{'x': 1}, [[1, 'del', 'x', None], [2, 'set', 'x', 5]], 1], 'expected': {}}],
  'hint': 'Копия словаря и применение записей журнала, пока время ≤ t.'},
 {'id': 'd14-find-bad-moment',
  'mode': 'func',
  'func': 'last_good_time',
  'title': 'Момент перед ошибкой',
  'statement': 'Журнал — список [время, текст команды]. Напишите last_good_time(wal, bad): время последней '
               'записи строго перед первой командой, текст которой содержит подстроку bad (регистр важен); '
               'если плохой команды нет — время последней записи журнала; если журнал пуст — 0; если плохая '
               'команда первая — 0.',
  'starter': 'def last_good_time(wal, bad):\n    pass\n',
  'tests': [{'args': [[[1, 'INSERT a'], [2, 'UPDATE b'], [3, 'DROP TABLE t'], [4, 'INSERT c']], 'DROP'],
             'expected': 2},
            {'args': [[[1, 'INSERT a']], 'DROP'], 'expected': 1},
            {'args': [[], 'DROP'], 'expected': 0},
            {'args': [[[1, 'DROP TABLE x']], 'DROP'], 'expected': 0}],
  'hint': 'Идите по журналу, помните время предыдущей записи.'},
 {'id': 'd14-rpo-loss',
  'mode': 'func',
  'func': 'data_loss_seconds',
  'title': 'Сколько данных потеряем',
  'statement': 'Сбой на сервере в момент crash. Журнал архивируется каждые interval секунд (архив уходит в '
               'хранилище в моменты, кратные interval: 0, interval, 2·interval, …). Всё, что записано после '
               'последнего архива, теряется. Напишите data_loss_seconds(crash, interval): сколько секунд '
               'данных потеряно (crash % interval).',
  'starter': 'def data_loss_seconds(crash, interval):\n    pass\n',
  'tests': [{'args': [125, 60], 'expected': 5},
            {'args': [60, 60], 'expected': 0},
            {'args': [59, 60], 'expected': 59},
            {'args': [0, 30], 'expected': 0}],
  'hint': 'Остаток от деления.'},
 {'id': 'd14-rto',
  'mode': 'func',
  'func': 'restore_time',
  'title': 'Время восстановления',
  'statement': 'Восстановление = загрузка копии (size_gb / read_speed_gbps секунд) + проигрыш журнала '
               '(wal_gb / replay_speed_gbps секунд). Напишите restore_time(size_gb, read_speed_gbps, wal_gb, '
               'replay_speed_gbps): секунд, округлённо до целого (всё положительное).',
  'starter': 'def restore_time(size_gb, read_speed_gbps, wal_gb, replay_speed_gbps):\n    pass\n',
  'tests': [{'args': [500, 0.5, 20, 0.05], 'expected': 1400},
            {'args': [100, 1, 0, 1], 'expected': 100},
            {'args': [1000, 2, 50, 0.1], 'expected': 1000}],
  'hint': 'Две дроби и сумма.'},
 {'id': 'd14-retention',
  'mode': 'func',
  'func': 'keep_backups',
  'title': 'Политика хранения',
  'statement': 'Копии — список номеров дней (целые, 0 — сегодня, 1 — вчера, …). Политика: держать все копии '
               'за последние 7 дней (дни 0–6), из старших — по одной в неделю (день, кратный 7, и не младше '
               '7) до 28 дней включительно, остальные удалить. Напишите keep_backups(days): отсортированный '
               'список дней, которые остаются.',
  'starter': 'def keep_backups(days):\n    pass\n',
  'tests': [{'args': [[0,
                       1,
                       2,
                       3,
                       4,
                       5,
                       6,
                       7,
                       8,
                       9,
                       10,
                       11,
                       12,
                       13,
                       14,
                       15,
                       16,
                       17,
                       18,
                       19,
                       20,
                       21,
                       22,
                       23,
                       24,
                       25,
                       26,
                       27,
                       28,
                       29,
                       30]],
             'expected': [0, 1, 2, 3, 4, 5, 6, 7, 14, 21, 28]},
            {'args': [[3, 8, 14, 29]], 'expected': [3, 14]},
            {'args': [[]], 'expected': []},
            {'args': [[0, 7, 28, 35]], 'expected': [0, 7, 28]}],
  'hint': 'Условие: d < 7 или (d ≤ 28 и d кратно 7).'},
 {'id': 'd14-lock-wait',
  'mode': 'func',
  'func': 'blocked_requests',
  'title': 'Запросы в очереди на блокировку',
  'statement': 'Миграция берёт эксклюзивную блокировку на interval = [начало, конец) (в секундах). Запросы '
               'приходят в моменты arrivals. Запрос, пришедший внутри интервала, ждёт до конца блокировки; '
               'если ожидание больше timeout, запрос получает ошибку. Напишите blocked_requests(start, end, '
               'arrivals, timeout): пару [число ждавших, число упавших по таймауту]. Ждавшими считаются и '
               'упавшие.',
  'starter': 'def blocked_requests(start, end, arrivals, timeout):\n    pass\n',
  'tests': [{'args': [10, 20, [5, 10, 15, 19, 25], 3], 'expected': [3, 2]},
            {'args': [10, 20, [1, 2], 5], 'expected': [0, 0]},
            {'args': [0, 100, [10, 50, 99], 60], 'expected': [3, 1]},
            {'args': [5, 5, [5], 1], 'expected': [0, 0]}],
  'hint': 'Для пришедших внутри интервала ожидание = end − t; сравните с timeout.'},
 {'id': 'd14-verify-restore',
  'mode': 'func',
  'func': 'restore_ok',
  'title': 'Проверка восстановленной копии',
  'statement': "Эталон — словарь метрик {'rows': n, 'sum': s}. Восстановленная копия даёт такой же словарь "
               'или None, если база не поднялась. Напишите restore_ok(expected, restored, seconds, rto): '
               'True, если restored не None, оба значения совпадают и seconds ≤ rto.',
  'starter': 'def restore_ok(expected, restored, seconds, rto):\n    pass\n',
  'tests': [{'args': [{'rows': 10, 'sum': 5}, {'rows': 10, 'sum': 5}, 100, 200], 'expected': True},
            {'args': [{'rows': 10, 'sum': 5}, {'rows': 9, 'sum': 5}, 100, 200], 'expected': False},
            {'args': [{'rows': 10, 'sum': 5}, None, 1, 1], 'expected': False},
            {'args': [{'rows': 1, 'sum': 1}, {'rows': 1, 'sum': 1}, 300, 200], 'expected': False}],
  'hint': 'Три условия вместе.'}]}
