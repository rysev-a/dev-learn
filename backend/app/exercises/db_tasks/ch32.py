"""Задачи книги «Базы данных»: глава 32."""

TASKS: dict[int, list[dict]] = {32: [{'id': 'd16-nplus1-join',
  'mode': 'sql',
  'title': 'Вместо запросов в цикле',
  'statement': 'Вместо запроса клиента для каждого заказа выведите заказы вместе с именем клиента одним '
               'запросом: колонки id, name, total; по id заказа.',
  'starter': '-- один запрос вместо N+1\nSELECT\n',
  'setup': 'CREATE TABLE clients (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL REFERENCES clients(id), '
           'total INTEGER NOT NULL, status TEXT NOT NULL, ver INTEGER NOT NULL DEFAULT 1);\n'
           'INSERT INTO clients VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб',NULL);\n"
           'INSERT INTO orders VALUES '
           "(1,1,100,'new',1),(2,1,250,'paid',1),(3,2,80,'new',1),(4,3,400,'paid',1),(5,3,60,'cancelled',1),(6,1,90,'new',1);\n",
  'expected': [[1, 'Анна', 100],
               [2, 'Анна', 250],
               [3, 'Борис', 80],
               [4, 'Вера', 400],
               [5, 'Вера', 60],
               [6, 'Анна', 90]],
  'expected_cols': ['id', 'name', 'total'],
  'hint': 'JOIN orders и clients по client_id.',
  'ordered': True},
 {'id': 'd16-batch-in',
  'mode': 'sql',
  'title': 'Пакет по списку идентификаторов',
  'statement': 'Загрузите клиентов с id 1, 3 и 4 одним запросом: колонки id, name; по id.',
  'starter': '-- IN вместо трёх запросов\nSELECT\n',
  'setup': 'CREATE TABLE clients (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL REFERENCES clients(id), '
           'total INTEGER NOT NULL, status TEXT NOT NULL, ver INTEGER NOT NULL DEFAULT 1);\n'
           'INSERT INTO clients VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб',NULL);\n"
           'INSERT INTO orders VALUES '
           "(1,1,100,'new',1),(2,1,250,'paid',1),(3,2,80,'new',1),(4,3,400,'paid',1),(5,3,60,'cancelled',1),(6,1,90,'new',1);\n",
  'expected': [[1, 'Анна'], [3, 'Вера'], [4, 'Глеб']],
  'expected_cols': ['id', 'name'],
  'hint': 'WHERE id IN (…).',
  'ordered': True},
 {'id': 'd16-detect-nplus1',
  'mode': 'sql',
  'title': 'Найти запросы в цикле',
  'statement': 'По журналу qlog найдите пары «запрос (req) — шаблон», в которых один и тот же шаблон '
               'выполнился 3 и более раз: колонки req, tpl, n; по req, затем tpl.',
  'starter': '-- детектор N+1\nSELECT\n',
  'setup': 'CREATE TABLE qlog (id INTEGER PRIMARY KEY, ts INTEGER NOT NULL, tpl TEXT NOT NULL, ms INTEGER '
           'NOT NULL, req TEXT NOT NULL);\n'
           "INSERT INTO qlog VALUES (1,1,'SELECT * FROM orders',12,'r1'),(2,2,'SELECT * FROM clients WHERE "
           "id = ?',1,'r1'),(3,3,'SELECT * FROM clients WHERE id = ?',1,'r1'),(4,4,'SELECT * FROM clients "
           "WHERE id = ?',2,'r1'),(5,5,'SELECT * FROM orders',10,'r2'),(6,6,'SELECT * FROM clients WHERE id "
           "IN (?)',3,'r2'),(7,7,'SELECT * FROM clients WHERE id = ?',1,'r3'),(8,8,'SELECT * FROM clients "
           "WHERE id = ?',1,'r3'),(9,9,'SELECT * FROM clients WHERE id = ?',1,'r3'),(10,10,'SELECT * FROM "
           "clients WHERE id = ?',1,'r3'),(11,11,'SELECT * FROM clients WHERE id = ?',2,'r3');\n",
  'expected': [['r1', 'SELECT * FROM clients WHERE id = ?', 3],
               ['r3', 'SELECT * FROM clients WHERE id = ?', 5]],
  'expected_cols': ['req', 'tpl', 'n'],
  'hint': 'GROUP BY req, tpl HAVING COUNT(*) >= 3.',
  'ordered': True},
 {'id': 'd16-time-by-req',
  'mode': 'sql',
  'title': 'Время запросов по обращению',
  'statement': 'Для каждого обращения (req) выведите число запросов к базе и суммарное время: колонки req, '
               'n, total_ms; по req.',
  'starter': '-- нагрузка по запросам пользователя\nSELECT\n',
  'setup': 'CREATE TABLE qlog (id INTEGER PRIMARY KEY, ts INTEGER NOT NULL, tpl TEXT NOT NULL, ms INTEGER '
           'NOT NULL, req TEXT NOT NULL);\n'
           "INSERT INTO qlog VALUES (1,1,'SELECT * FROM orders',12,'r1'),(2,2,'SELECT * FROM clients WHERE "
           "id = ?',1,'r1'),(3,3,'SELECT * FROM clients WHERE id = ?',1,'r1'),(4,4,'SELECT * FROM clients "
           "WHERE id = ?',2,'r1'),(5,5,'SELECT * FROM orders',10,'r2'),(6,6,'SELECT * FROM clients WHERE id "
           "IN (?)',3,'r2'),(7,7,'SELECT * FROM clients WHERE id = ?',1,'r3'),(8,8,'SELECT * FROM clients "
           "WHERE id = ?',1,'r3'),(9,9,'SELECT * FROM clients WHERE id = ?',1,'r3'),(10,10,'SELECT * FROM "
           "clients WHERE id = ?',1,'r3'),(11,11,'SELECT * FROM clients WHERE id = ?',2,'r3');\n",
  'expected': [['r1', 4, 16], ['r2', 2, 13], ['r3', 5, 6]],
  'expected_cols': ['req', 'n', 'total_ms'],
  'hint': 'GROUP BY req с COUNT(*) и SUM(ms).',
  'ordered': True},
 {'id': 'd16-slowest-tpl',
  'mode': 'sql',
  'title': 'Самые тяжёлые шаблоны',
  'statement': 'Выведите два шаблона с наибольшим суммарным временем: колонки tpl, total_ms; по убыванию '
               'времени, затем по шаблону.',
  'starter': '-- топ шаблонов\nSELECT\n',
  'setup': 'CREATE TABLE qlog (id INTEGER PRIMARY KEY, ts INTEGER NOT NULL, tpl TEXT NOT NULL, ms INTEGER '
           'NOT NULL, req TEXT NOT NULL);\n'
           "INSERT INTO qlog VALUES (1,1,'SELECT * FROM orders',12,'r1'),(2,2,'SELECT * FROM clients WHERE "
           "id = ?',1,'r1'),(3,3,'SELECT * FROM clients WHERE id = ?',1,'r1'),(4,4,'SELECT * FROM clients "
           "WHERE id = ?',2,'r1'),(5,5,'SELECT * FROM orders',10,'r2'),(6,6,'SELECT * FROM clients WHERE id "
           "IN (?)',3,'r2'),(7,7,'SELECT * FROM clients WHERE id = ?',1,'r3'),(8,8,'SELECT * FROM clients "
           "WHERE id = ?',1,'r3'),(9,9,'SELECT * FROM clients WHERE id = ?',1,'r3'),(10,10,'SELECT * FROM "
           "clients WHERE id = ?',1,'r3'),(11,11,'SELECT * FROM clients WHERE id = ?',2,'r3');\n",
  'expected': [['SELECT * FROM orders', 22], ['SELECT * FROM clients WHERE id = ?', 10]],
  'expected_cols': ['tpl', 'total_ms'],
  'hint': 'GROUP BY tpl, сортировка по сумме, LIMIT 2.',
  'ordered': True},
 {'id': 'd16-select-needed',
  'mode': 'sql',
  'title': 'Только нужные столбцы',
  'statement': 'Для списка заказов нужны только id, status и total, причём только для оплаченных, самые '
               'крупные первыми (LIMIT 2). Колонки id, status, total.',
  'starter': '-- не SELECT *\nSELECT\n',
  'setup': 'CREATE TABLE clients (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL REFERENCES clients(id), '
           'total INTEGER NOT NULL, status TEXT NOT NULL, ver INTEGER NOT NULL DEFAULT 1);\n'
           'INSERT INTO clients VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб',NULL);\n"
           'INSERT INTO orders VALUES '
           "(1,1,100,'new',1),(2,1,250,'paid',1),(3,2,80,'new',1),(4,3,400,'paid',1),(5,3,60,'cancelled',1),(6,1,90,'new',1);\n",
  'expected': [[4, 'paid', 400], [2, 'paid', 250]],
  'expected_cols': ['id', 'status', 'total'],
  'hint': 'Перечислите нужные столбцы; ORDER BY total DESC LIMIT 2.',
  'ordered': True},
 {'id': 'd16-keyset',
  'mode': 'sql',
  'title': 'Следующая страница',
  'statement': 'Выведите следующую страницу заказов по 2 после заказа с id 2 (без OFFSET), по возрастанию '
               'id: колонки id, total.',
  'starter': '-- keyset\nSELECT\n',
  'setup': 'CREATE TABLE clients (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL REFERENCES clients(id), '
           'total INTEGER NOT NULL, status TEXT NOT NULL, ver INTEGER NOT NULL DEFAULT 1);\n'
           'INSERT INTO clients VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб',NULL);\n"
           'INSERT INTO orders VALUES '
           "(1,1,100,'new',1),(2,1,250,'paid',1),(3,2,80,'new',1),(4,3,400,'paid',1),(5,3,60,'cancelled',1),(6,1,90,'new',1);\n",
  'expected': [[3, 80], [4, 400]],
  'expected_cols': ['id', 'total'],
  'hint': 'WHERE id > 2 ORDER BY id LIMIT 2.',
  'ordered': True},
 {'id': 'd16-bulk-insert',
  'mode': 'sql',
  'title': 'Пакетная вставка',
  'statement': "Вставьте одним оператором INSERT три строки: (1,'view',10), (2,'click',3), (3,'buy',1). Итог "
               'проверяется по таблице.',
  'starter': '-- одна команда, три строки\nINSERT INTO events\n',
  'setup': 'CREATE TABLE events (id INTEGER PRIMARY KEY, kind TEXT NOT NULL, n INTEGER NOT NULL);\n',
  'expected': [[1, 'view', 10], [2, 'click', 3], [3, 'buy', 1]],
  'expected_cols': ['id', 'kind', 'n'],
  'hint': 'INSERT INTO events VALUES (…), (…), (…);',
  'ordered': True,
  'check': 'SELECT id, kind, n FROM events ORDER BY id'},
 {'id': 'd16-bulk-update',
  'mode': 'sql',
  'title': 'Массовое обновление',
  'statement': "Одним UPDATE отметьте все новые заказы клиента 1 как 'paid'. Итог проверяется по таблице "
               'orders.',
  'starter': '-- один запрос вместо цикла\nUPDATE orders\n',
  'setup': 'CREATE TABLE clients (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL REFERENCES clients(id), '
           'total INTEGER NOT NULL, status TEXT NOT NULL, ver INTEGER NOT NULL DEFAULT 1);\n'
           'INSERT INTO clients VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб',NULL);\n"
           'INSERT INTO orders VALUES '
           "(1,1,100,'new',1),(2,1,250,'paid',1),(3,2,80,'new',1),(4,3,400,'paid',1),(5,3,60,'cancelled',1),(6,1,90,'new',1);\n",
  'expected': [[1, 'paid'], [2, 'paid'], [3, 'new'], [4, 'paid'], [5, 'cancelled'], [6, 'paid']],
  'expected_cols': ['id', 'status'],
  'hint': "UPDATE orders SET status = 'paid' WHERE client_id = 1 AND status = 'new';",
  'ordered': True,
  'check': 'SELECT id, status FROM orders ORDER BY id'},
 {'id': 'd16-optimistic',
  'mode': 'sql',
  'title': 'Оптимистичная блокировка',
  'statement': "Приложение прочитало заказ 1 с ver = 1 и хочет поставить status = 'paid'. Обновите так, "
               'чтобы изменение сработало только при прежней версии, и увеличьте ver. Затем повторите ту же '
               'команду (имитация конкурента, который опоздал): второй раз строка не должна измениться. Итог '
               'проверяется по orders.',
  'starter': '-- UPDATE ... WHERE ver = ?\nUPDATE orders\n',
  'setup': 'CREATE TABLE clients (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL REFERENCES clients(id), '
           'total INTEGER NOT NULL, status TEXT NOT NULL, ver INTEGER NOT NULL DEFAULT 1);\n'
           'INSERT INTO clients VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб',NULL);\n"
           'INSERT INTO orders VALUES '
           "(1,1,100,'new',1),(2,1,250,'paid',1),(3,2,80,'new',1),(4,3,400,'paid',1),(5,3,60,'cancelled',1),(6,1,90,'new',1);\n",
  'expected': [[1, 'paid', 2]],
  'expected_cols': ['id', 'status', 'ver'],
  'hint': 'WHERE id = 1 AND ver = 1 и ver = ver + 1; второй запуск не найдёт строку с ver = 1.',
  'ordered': True,
  'check': 'SELECT id, status, ver FROM orders WHERE id = 1'},
 {'id': 'd16-idempotency-key',
  'mode': 'sql',
  'title': 'Ключ идемпотентности',
  'statement': "Выполните платёж идемпотентно: вставьте ('k-91a', 500, 'ok') командой INSERT OR IGNORE, а "
               'затем ещё раз ту же команду (повтор клиента). В таблице должна остаться одна строка. Итог — '
               'по таблице.',
  'starter': '-- повтор безопасен\nINSERT OR IGNORE INTO payments\n',
  'setup': 'CREATE TABLE payments (key TEXT PRIMARY KEY, amount INTEGER NOT NULL, result TEXT);\n',
  'expected': [['k-91a', 500, 'ok']],
  'expected_cols': ['key', 'amount', 'result'],
  'hint': 'INSERT OR IGNORE при конфликте по первичному ключу молча пропускает вставку.',
  'ordered': True,
  'check': 'SELECT key, amount, result FROM payments'},
 {'id': 'd16-outbox',
  'mode': 'sql',
  'title': 'Исходящие сообщения',
  'statement': 'В одной транзакции создайте заказ (id 1, total 300) и событие в outbox: topic '
               "'order.created', payload — id заказа как строка '1'. Используйте BEGIN … COMMIT. Итог "
               'проверяется по обеим таблицам.',
  'starter': '-- заказ и событие вместе\nBEGIN;\n',
  'setup': 'CREATE TABLE orders (id INTEGER PRIMARY KEY, total INTEGER NOT NULL);\n'
           'CREATE TABLE outbox (id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT NOT NULL, payload TEXT NOT '
           'NULL, sent INTEGER NOT NULL DEFAULT 0);\n',
  'expected': [['o', 1, 300], ['x', 1, 0]],
  'expected_cols': ['t', 'id', 'total'],
  'hint': 'Две вставки между BEGIN и COMMIT.',
  'ordered': True,
  'check': "SELECT 'o' AS t, id, total FROM orders UNION ALL SELECT 'x', id, sent FROM outbox ORDER BY 1, 2"},
 {'id': 'd16-queue-claim',
  'mode': 'sql',
  'title': 'Взять задачу из очереди',
  'statement': "Обработчик w1 берёт одну необработанную задачу (status = 'new') с наименьшим id: одним "
               "UPDATE установите status = 'running', worker = 'w1'. Итог проверяется по таблице jobs.",
  'starter': '-- взять задачу\nUPDATE jobs\n',
  'setup': "CREATE TABLE jobs (id INTEGER PRIMARY KEY, payload TEXT, status TEXT NOT NULL DEFAULT 'new', "
           'worker TEXT);\n'
           "INSERT INTO jobs (id, payload) VALUES (1,'a'),(2,'b'),(3,'c');\n"
           "UPDATE jobs SET status = 'done' WHERE id = 1;\n",
  'expected': [[1, 'done', None], [2, 'running', 'w1'], [3, 'new', None]],
  'expected_cols': ['id', 'status', 'worker'],
  'hint': "Подзапрос SELECT MIN(id) … WHERE status = 'new' в условии UPDATE.",
  'ordered': True,
  'check': 'SELECT id, status, worker FROM jobs ORDER BY id'},
 {'id': 'd16-requeue-stuck',
  'mode': 'sql',
  'title': 'Вернуть зависшие задачи',
  'statement': 'Сейчас момент 500. Задачи в статусе running, начатые 300 и более секунд назад, считаются '
               'зависшими: верните их в new, обнулив started и worker. Итог — по таблице jobs.',
  'starter': '-- по таймауту\nUPDATE jobs\n',
  'setup': 'CREATE TABLE jobs (id INTEGER PRIMARY KEY, status TEXT NOT NULL, started INTEGER, worker TEXT);\n'
           'INSERT INTO jobs VALUES '
           "(1,'running',100,'w1'),(2,'running',450,'w2'),(3,'done',50,'w1'),(4,'new',NULL,NULL),(5,'running',90,'w3');\n",
  'expected': [[1, 'new', None, None],
               [2, 'running', 450, 'w2'],
               [3, 'done', 50, 'w1'],
               [4, 'new', None, None],
               [5, 'new', None, None]],
  'expected_cols': ['id', 'status', 'started', 'worker'],
  'hint': "WHERE status = 'running' AND 500 - started >= 300.",
  'ordered': True,
  'check': 'SELECT id, status, started, worker FROM jobs ORDER BY id'},
 {'id': 'd16-upsert-counter',
  'mode': 'sql',
  'title': 'Счётчик через upsert',
  'statement': "Зафиксируйте три посещения: '/home' (+1), '/cart' (+1), '/home' (+1) тремя командами INSERT "
               '… ON CONFLICT (page) DO UPDATE SET n = n + 1. Итог — по таблице hits.',
  'starter': '-- upsert\nINSERT INTO hits\n',
  'setup': 'CREATE TABLE hits (page TEXT PRIMARY KEY, n INTEGER NOT NULL);\n'
           "INSERT INTO hits VALUES ('/home', 5);\n",
  'expected': [['/cart', 1], ['/home', 7]],
  'expected_cols': ['page', 'n'],
  'hint': 'ON CONFLICT (page) DO UPDATE SET n = n + 1.',
  'ordered': True,
  'check': 'SELECT page, n FROM hits ORDER BY page'},
 {'id': 'd16-percentile',
  'mode': 'sql',
  'title': 'Медленные запросы',
  'statement': 'Найдите значение ms, ниже которого лежат не менее 90% запросов (через сортировку по ms и '
               'подсчёт: наименьшее ms, для которого доля записей с ms ≤ него не меньше 0.9). Колонка p90.',
  'starter': '-- p90\nSELECT\n',
  'setup': 'CREATE TABLE qlog (id INTEGER PRIMARY KEY, ts INTEGER NOT NULL, tpl TEXT NOT NULL, ms INTEGER '
           'NOT NULL, req TEXT NOT NULL);\n'
           "INSERT INTO qlog VALUES (1,1,'SELECT * FROM orders',12,'r1'),(2,2,'SELECT * FROM clients WHERE "
           "id = ?',1,'r1'),(3,3,'SELECT * FROM clients WHERE id = ?',1,'r1'),(4,4,'SELECT * FROM clients "
           "WHERE id = ?',2,'r1'),(5,5,'SELECT * FROM orders',10,'r2'),(6,6,'SELECT * FROM clients WHERE id "
           "IN (?)',3,'r2'),(7,7,'SELECT * FROM clients WHERE id = ?',1,'r3'),(8,8,'SELECT * FROM clients "
           "WHERE id = ?',1,'r3'),(9,9,'SELECT * FROM clients WHERE id = ?',1,'r3'),(10,10,'SELECT * FROM "
           "clients WHERE id = ?',1,'r3'),(11,11,'SELECT * FROM clients WHERE id = ?',2,'r3');\n",
  'expected': [[10]],
  'expected_cols': ['p90'],
  'hint': 'Для каждого значения посчитайте долю записей не больше него и выберите наименьшее с долей ≥ 0.9.'},
 {'id': 'd16-pool-sim',
  'mode': 'func',
  'func': 'pool_wait',
  'title': 'Очередь на пул',
  'statement': 'Пул из size соединений. Запросы — списки [момент прихода, длительность] по возрастанию '
               'момента. Свободное соединение берётся сразу, иначе запрос ждёт самого раннего освобождения '
               '(FIFO). Напишите pool_wait(size, requests): список времён ожидания каждого запроса.',
  'starter': 'def pool_wait(size, requests):\n    pass\n',
  'tests': [{'args': [2, [[0, 10], [1, 10], [2, 10], [3, 10]]], 'expected': [0, 0, 8, 8]},
            {'args': [1, [[0, 5], [1, 5]]], 'expected': [0, 4]},
            {'args': [3, []], 'expected': []},
            {'args': [2, [[0, 1], [5, 1]]], 'expected': [0, 0]}],
  'hint': 'Куча моментов освобождения соединений; старт = max(приход, освобождение).'},
 {'id': 'd16-littles-law',
  'mode': 'func',
  'func': 'pool_needed',
  'title': 'Закон Литтла',
  'statement': 'Среднее число занятых соединений = интенсивность (запросов/с) × среднее время (мс) / 1000. '
               'Напишите pool_needed(rps, avg_ms, headroom): целое число соединений — округлить вверх '
               'произведение с запасом headroom (множитель), минимум 1.',
  'starter': 'import math\n\ndef pool_needed(rps, avg_ms, headroom):\n    pass\n',
  'tests': [{'args': [100, 20, 2], 'expected': 4},
            {'args': [1000, 5, 1.5], 'expected': 8},
            {'args': [1, 1, 1], 'expected': 1},
            {'args': [0, 10, 2], 'expected': 1}],
  'hint': 'math.ceil(rps * avg_ms / 1000 * headroom), не меньше 1.'},
 {'id': 'd16-nplus1-count',
  'mode': 'func',
  'func': 'query_count',
  'title': 'Сколько запросов',
  'statement': 'Страница показывает orders заказов, у каждого — клиент, а у клиента — страна. Стратегии: '
               "'lazy' — 1 + orders + orders (клиент и страна по запросу на заказ), 'join' — 1, 'batch' — 3 "
               '(заказы, клиенты списком, страны списком). Напишите query_count(orders, strategy): число '
               "запросов; при orders = 0 для 'lazy' — 1.",
  'starter': 'def query_count(orders, strategy):\n    pass\n',
  'tests': [{'args': [100, 'lazy'], 'expected': 201},
            {'args': [100, 'join'], 'expected': 1},
            {'args': [100, 'batch'], 'expected': 3},
            {'args': [0, 'lazy'], 'expected': 1}],
  'hint': 'Три формулы по стратегии.'},
 {'id': 'd16-latency',
  'mode': 'func',
  'func': 'page_latency',
  'title': 'Задержка страницы',
  'statement': 'Каждый запрос стоит rtt (сетевая задержка) + exec_ms (выполнение), запросы идут '
               'последовательно. Напишите page_latency(queries, rtt, exec_ms): суммарное время в мс.',
  'starter': 'def page_latency(queries, rtt, exec_ms):\n    pass\n',
  'tests': [{'args': [101, 1, 0.5], 'expected': 151.5},
            {'args': [1, 1, 20], 'expected': 21},
            {'args': [0, 5, 5], 'expected': 0}],
  'hint': 'queries · (rtt + exec).'},
 {'id': 'd16-retry-backoff',
  'mode': 'func',
  'func': 'backoff_schedule',
  'title': 'Повторы с задержкой',
  'statement': 'Экспоненциальная задержка: base · 2^k для k = 0, 1, …; но не больше cap. Напишите '
               'backoff_schedule(base, cap, attempts): список задержек для attempts повторов.',
  'starter': 'def backoff_schedule(base, cap, attempts):\n    pass\n',
  'tests': [{'args': [100, 1000, 6], 'expected': [100, 200, 400, 800, 1000, 1000]},
            {'args': [1, 100, 0], 'expected': []},
            {'args': [50, 50, 3], 'expected': [50, 50, 50]}],
  'hint': 'min(cap, base * 2 ** k).'},
 {'id': 'd16-chunks',
  'mode': 'func',
  'func': 'chunked',
  'title': 'Пакеты',
  'statement': 'Напишите chunked(items, size): список пакетов по size элементов (последний может быть '
               'короче). Для пустого списка — пустой список.',
  'starter': 'def chunked(items, size):\n    pass\n',
  'tests': [{'args': [[1, 2, 3, 4, 5], 2], 'expected': [[1, 2], [3, 4], [5]]},
            {'args': [[], 3], 'expected': []},
            {'args': [[1], 5], 'expected': [[1]]},
            {'args': [[1, 2, 3], 3], 'expected': [[1, 2, 3]]}],
  'hint': 'Срезы с шагом size.'},
 {'id': 'd16-idempotent',
  'mode': 'func',
  'func': 'process_requests',
  'title': 'Обработка с ключом',
  'statement': 'Запросы — списки [ключ, сумма]. Первый запрос с ключом выполняется (баланс уменьшается на '
               'сумму), повторный с тем же ключом возвращает прежний результат и баланс не меняет. Начальный '
               'баланс balance. Напишите process_requests(balance, requests): пару [итоговый баланс, список '
               "результатов 'ok' / 'duplicate' / 'insufficient'] — недостаточно средств 'insufficient' "
               '(баланс не меняется, ключ запоминается как выполненный с этим результатом).',
  'starter': 'def process_requests(balance, requests):\n    pass\n',
  'tests': [{'args': [100, [['a', 30], ['a', 30], ['b', 80], ['c', 70]]],
             'expected': [0, ['ok', 'duplicate', 'insufficient', 'ok']]},
            {'args': [0, []], 'expected': [0, []]},
            {'args': [10, [['x', 11], ['x', 11]]], 'expected': [10, ['insufficient', 'duplicate']]}],
  'hint': 'Словарь выполненных ключей; повтор — duplicate без изменений.'},
 {'id': 'd16-optimistic-py',
  'mode': 'func',
  'func': 'apply_with_version',
  'title': 'Оптимистичные версии',
  'statement': "Запись — словарь {'v': значение, 'ver': номер}. Попытки — списки [ожидаемая версия, новое "
               'значение]. Попытка срабатывает, только если ожидаемая версия равна текущей; тогда значение '
               'меняется и версия растёт на 1. Напишите apply_with_version(rec, attempts): пару [итоговая '
               'запись, список True/False по попыткам]. Исходную запись не менять.',
  'starter': 'def apply_with_version(rec, attempts):\n    pass\n',
  'tests': [{'args': [{'v': 'a', 'ver': 1}, [[1, 'b'], [1, 'c'], [2, 'd']]],
             'expected': [{'v': 'd', 'ver': 3}, [True, False, True]]},
            {'args': [{'v': 0, 'ver': 5}, []], 'expected': [{'v': 0, 'ver': 5}, []]},
            {'args': [{'v': 'x', 'ver': 1}, [[0, 'y']]], 'expected': [{'v': 'x', 'ver': 1}, [False]]}],
  'hint': 'Сравнивайте ожидаемую версию с текущей; при успехе увеличивайте версию.'},
 {'id': 'd16-outbox-py',
  'mode': 'func',
  'func': 'publish_outbox',
  'title': 'Публикация исходящих',
  'statement': "Таблица outbox — список словарей {'id', 'sent'}. Публикатор берёт неотправленные по "
               'возрастанию id не более limit штук и помечает sent. Публикация может упасть на сообщении с '
               'id из fail: оно остаётся неотправленным, и публикатор останавливается (порядок сохраняется). '
               'Напишите publish_outbox(outbox, limit, fail): список id, отправленных за этот проход.',
  'starter': 'def publish_outbox(outbox, limit, fail):\n    pass\n',
  'tests': [{'args': [[{'id': 1, 'sent': False}, {'id': 2, 'sent': False}, {'id': 3, 'sent': False}], 2, []],
             'expected': [1, 2]},
            {'args': [[{'id': 1, 'sent': False}, {'id': 2, 'sent': False}], 5, [2]], 'expected': [1]},
            {'args': [[{'id': 1, 'sent': True}, {'id': 2, 'sent': False}], 5, []], 'expected': [2]},
            {'args': [[], 3, []], 'expected': []}],
  'hint': 'Идите по неотправленным в порядке id; остановитесь по лимиту или на ошибке.'},
 {'id': 'd16-replica-route',
  'mode': 'func',
  'func': 'route_read',
  'title': 'Куда читать',
  'statement': 'Пользователь сделал запись в момент last_write (None — не писал). Реплика отстаёт на lag '
               'секунд. Читаем с основной, если пользователь писал и с момента записи прошло меньше lag + 1 '
               'секунды (now − last_write < lag + 1), иначе с реплики. Напишите route_read(now, last_write, '
               "lag): 'primary' или 'replica'.",
  'starter': 'def route_read(now, last_write, lag):\n    pass\n',
  'tests': [{'args': [100, 99, 2], 'expected': 'primary'},
            {'args': [100, 90, 2], 'expected': 'replica'},
            {'args': [100, None, 2], 'expected': 'replica'},
            {'args': [10, 10, 0], 'expected': 'primary'}],
  'hint': 'Два условия: была запись и прошло недостаточно времени.'},
 {'id': 'd16-normalize-sql',
  'mode': 'func',
  'func': 'normalize_query',
  'title': 'Шаблон запроса',
  'statement': 'Чтобы группировать запросы в журнале, значения заменяют на ?. Напишите normalize_query(sql): '
               'строка, в которой каждое целое или дробное число и каждый строковый литерал в одинарных '
               "кавычках заменены на '?', а последовательности пробелов сжаты до одного (концы обрезаются); "
               'регистр не менять. Числа внутри идентификаторов (t1) не трогать.',
  'starter': 'import re\n\ndef normalize_query(sql):\n    pass\n',
  'tests': [{'args': ["SELECT * FROM t1 WHERE id = 42 AND name = 'Анна'"],
             'expected': 'SELECT * FROM t1 WHERE id = ? AND name = ?'},
            {'args': ['  SELECT  1,   2.5  FROM x  '], 'expected': 'SELECT ?, ? FROM x'},
            {'args': ["WHERE a = 'O''Brien' OR b IN (1, 2, 3)"], 'expected': 'WHERE a = ? OR b IN (?, ?, ?)'},
            {'args': [''], 'expected': ''}],
  'hint': "Два re.sub: литералы в кавычках и отдельно стоящие числа; затем ' '.join(s.split())."},
 {'id': 'd16-detect-nplus1-py',
  'mode': 'func',
  'func': 'repeated_templates',
  'title': 'Детектор N+1',
  'statement': 'Журнал — список [обращение, шаблон]. Напишите repeated_templates(log, threshold): '
               'отсортированный список пар [обращение, шаблон], в которых шаблон повторился не менее '
               'threshold раз.',
  'starter': 'def repeated_templates(log, threshold):\n    pass\n',
  'tests': [{'args': [[['r1', 'a'], ['r1', 'b'], ['r1', 'b'], ['r1', 'b'], ['r2', 'b']], 3],
             'expected': [['r1', 'b']]},
            {'args': [[], 2], 'expected': []},
            {'args': [[['x', 'y']], 1], 'expected': [['x', 'y']]}],
  'hint': 'Счётчик по парам (обращение, шаблон).'},
 {'id': 'd16-unit-of-work',
  'mode': 'func',
  'func': 'pending_updates',
  'title': 'Единица работы',
  'statement': 'ORM помнит исходное состояние объектов. Исходные — словарь «id → словарь полей», текущие — '
               'такой же. Напишите pending_updates(original, current): отсортированный по id список записей '
               '[id, словарь изменённых полей и их новых значений] только для объектов, у которых что-то '
               'изменилось (поля сравниваются по ключам текущего объекта).',
  'starter': 'def pending_updates(original, current):\n    pass\n',
  'tests': [{'args': [{'1': {'a': 1, 'b': 2}, '2': {'a': 5}}, {'1': {'a': 1, 'b': 3}, '2': {'a': 5}}],
             'expected': [['1', {'b': 3}]]},
            {'args': [{}, {}], 'expected': []},
            {'args': [{'1': {'a': 1}}, {'1': {'a': 2, 'c': 3}}], 'expected': [['1', {'a': 2, 'c': 3}]]}],
  'hint': 'Для каждого объекта сравните текущие поля с исходными.'}]}
