"""Задачи книги «Базы данных»: глава 29."""

TASKS: dict[int, list[dict]] = {29: [{'id': 'd13-analyze-stats',
  'mode': 'sql',
  'title': 'Статистика после ANALYZE',
  'statement': 'Соберите статистику командой ANALYZE. Итог проверяется по таблице sqlite_stat1: в ней должны '
               'появиться строки статистики индексов.',
  'starter': '-- собрать статистику\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n"
           'CREATE INDEX idx_orders_user ON orders(user_id);\n'
           'CREATE INDEX idx_orders_status ON orders(status);\n',
  'expected': [['orders', 'idx_orders_status', '3000 1500'],
               ['orders', 'idx_orders_user', '3000 10'],
               ['users', None, '300']],
  'expected_cols': ['tbl', 'idx', 'stat'],
  'hint': 'Достаточно команды ANALYZE; — SQLite запишет число строк и среднее число строк на значение '
          'индекса в sqlite_stat1.',
  'ordered': True,
  'check': 'SELECT tbl, idx, stat FROM sqlite_stat1 ORDER BY tbl, idx'},
 {'id': 'd13-index-filter',
  'mode': 'sql',
  'title': 'Индекс под фильтр',
  'statement': 'Запрос SELECT * FROM orders WHERE user_id = 7 просматривает таблицу. Создайте индекс так, '
               'чтобы план стал поиском по индексу.',
  'starter': '-- индекс под WHERE user_id = ?\nCREATE INDEX\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n",
  'expected': [[3, 0, 61, 'SEARCH orders USING INDEX idx_orders_user (user_id=?)']],
  'hint': 'CREATE INDEX имя ON orders (user_id);',
  'check': 'EXPLAIN QUERY PLAN SELECT * FROM orders WHERE user_id = 7',
  'contains': ['SEARCH orders USING INDEX'],
  'forbid': ['SCAN']},
 {'id': 'd13-index-expression',
  'mode': 'sql',
  'title': 'Индекс на выражении',
  'statement': "Запрос SELECT * FROM users WHERE lower(email) = 'user5@mail.ru' не использует индекс по "
               'email. Создайте индекс на выражении lower(email), чтобы план стал поиском.',
  'starter': '-- индекс на выражении\nCREATE INDEX\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n",
  'expected': [[3, 0, 61, 'SEARCH users USING INDEX idx_users_lower_email (<expr>=?)']],
  'hint': 'CREATE INDEX … ON users (lower(email));',
  'check': "EXPLAIN QUERY PLAN SELECT * FROM users WHERE lower(email) = 'user5@mail.ru'",
  'contains': ['SEARCH users USING INDEX'],
  'forbid': ['SCAN']},
 {'id': 'd13-covering',
  'mode': 'sql',
  'title': 'Покрывающий индекс',
  'statement': 'Запрос SELECT created, total FROM orders WHERE user_id = 7 читает таблицу. Создайте один '
               'индекс, который покрывает запрос полностью (план должен содержать COVERING INDEX).',
  'starter': '-- покрывающий индекс\nCREATE INDEX\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n",
  'expected': [[2, 0, 54, 'SEARCH orders USING COVERING INDEX idx_cover (user_id=?)']],
  'hint': 'Добавьте в индекс после user_id и оба нужных столбца: created и total.',
  'check': 'EXPLAIN QUERY PLAN SELECT created, total FROM orders WHERE user_id = 7',
  'contains': ['USING COVERING INDEX']},
 {'id': 'd13-composite-order',
  'mode': 'sql',
  'title': 'Порядок столбцов в индексе',
  'statement': "Запрос: WHERE status = 'new' AND user_id = 5. Создайте составной индекс (в любом порядке "
               'столбцов), чтобы в плане условие использовало оба столбца: в тексте плана должно быть '
               '«status=? AND user_id=?» либо «user_id=? AND status=?».',
  'starter': '-- составной индекс\nCREATE INDEX\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n",
  'expected': [[3, 0, 62, 'SEARCH orders USING INDEX idx_su (user_id=? AND status=?)']],
  'hint': 'Индекс (user_id, status): оба условия — равенства, оба столбца войдут в поиск.',
  'check': "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE status = 'new' AND user_id = 5",
  'contains': ['(user_id=? AND status=?)']},
 {'id': 'd13-join-index',
  'mode': 'sql',
  'title': 'Индекс под соединение',
  'statement': 'Запрос SELECT u.email, o.total FROM users u JOIN orders o ON o.user_id = u.id WHERE u.id = 5 '
               'соединяет таблицы. Создайте индекс, чтобы доступ к orders шёл поиском по индексу.',
  'starter': '-- индекс на внешнем ключе\nCREATE INDEX\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n",
  'expected': [[4, 0, 45, 'SEARCH u USING INTEGER PRIMARY KEY (rowid=?)'],
               [7, 0, 61, 'SEARCH o USING INDEX idx_orders_user (user_id=?)']],
  'hint': 'Индексируйте столбец соединения в той таблице, где идёт поиск: orders.user_id.',
  'check': 'EXPLAIN QUERY PLAN SELECT u.email, o.total FROM users u JOIN orders o ON o.user_id = u.id WHERE '
           'u.id = 5',
  'contains': ['SEARCH o USING INDEX']},
 {'id': 'd13-selectivity',
  'mode': 'sql',
  'title': 'Селективность условия',
  'statement': "Выведите долю заказов со статусом 'new' в процентах с одним знаком после запятой: колонка "
               'pct (ROUND до 1 знака).',
  'starter': '-- доля строк\nSELECT\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n",
  'expected': [[2.0]],
  'expected_cols': ['pct'],
  'hint': "SUM(status = 'new') считает подходящие строки, COUNT(*) — все."},
 {'id': 'd13-n-distinct',
  'mode': 'sql',
  'title': 'Число различных значений',
  'statement': 'Для столбцов city и status таблицы users выведите число различных значений: колонки cities, '
               'statuses.',
  'starter': '-- кардинальность\nSELECT\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n",
  'expected': [[4, 2]],
  'expected_cols': ['cities', 'statuses'],
  'hint': 'COUNT(DISTINCT …) для каждого столбца.'},
 {'id': 'd13-mcv',
  'mode': 'sql',
  'title': 'Самые частые значения',
  'statement': 'Выведите самые частые значения city и долю каждого в процентах (целое): колонки city, pct; '
               'по убыванию доли, затем по городу.',
  'starter': '-- как собирает статистику ANALYZE\nSELECT\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n",
  'expected': [['Казань', 25.0], ['Москва', 25.0], ['Омск', 25.0], ['Тверь', 25.0]],
  'expected_cols': ['city', 'pct'],
  'hint': 'GROUP BY city, COUNT(*) и доля от общего числа строк.',
  'ordered': True},
 {'id': 'd13-histogram',
  'mode': 'sql',
  'title': 'Границы корзин гистограммы',
  'statement': 'Разбейте заказы на 4 корзины равной численности по total (NTILE) и выведите наибольшее '
               'значение total в каждой корзине: колонки bucket, upper; по корзине.',
  'starter': '-- NTILE\nSELECT\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n",
  'expected': [[1, 134], [2, 259], [3, 384], [4, 509]],
  'expected_cols': ['bucket', 'upper'],
  'hint': 'NTILE(4) OVER (ORDER BY total), затем MAX(total) по корзине.',
  'ordered': True},
 {'id': 'd13-independence',
  'mode': 'sql',
  'title': 'Оценка и факт',
  'statement': "Оценка по независимости: доля city='Москва' умноженная на долю status='blocked' и на число "
               'строк. Выведите одну строку: est — оценка числа строк (ROUND до целого) и actual — реальное '
               'число строк, где оба условия выполнены.',
  'starter': '-- оценка против факта\nSELECT\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n",
  'expected': [[8.0, 15]],
  'expected_cols': ['est', 'actual'],
  'hint': 'est = n_city * n_status / n; actual — COUNT(*) с обоими условиями.'},
 {'id': 'd13-notin-null',
  'mode': 'sql',
  'title': 'Ловушка NOT IN',
  'statement': 'Выведите id из a, которых нет в b, так, чтобы NULL в b не ломал результат (NOT EXISTS): '
               'колонка id; по возрастанию.',
  'starter': '-- anti-join\nSELECT\n',
  'setup': 'CREATE TABLE a (id INTEGER);\n'
           'CREATE TABLE b (id INTEGER);\n'
           'INSERT INTO a VALUES (1),(2),(3),(4);\n'
           'INSERT INTO b VALUES (2),(NULL);\n',
  'expected': [[1], [3], [4]],
  'expected_cols': ['id'],
  'hint': 'NOT EXISTS (SELECT 1 FROM b WHERE b.id = a.id).',
  'ordered': True},
 {'id': 'd13-keyset',
  'mode': 'sql',
  'title': 'Страницы без OFFSET',
  'statement': 'Выведите следующую страницу из 5 заказов после заказа с id 100 в порядке возрастания id (без '
               'OFFSET): колонки id, total.',
  'starter': '-- keyset-пагинация\nSELECT\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n",
  'expected': [[101, 323], [102, 336], [103, 349], [104, 362], [105, 375]],
  'expected_cols': ['id', 'total'],
  'hint': 'WHERE id > 100 ORDER BY id LIMIT 5.',
  'ordered': True},
 {'id': 'd13-semijoin',
  'mode': 'sql',
  'title': 'IN вместо соединения с размножением',
  'statement': "Выведите пользователей (id, email), у которых есть хотя бы один заказ со статусом 'new', без "
               'повторов. Используйте EXISTS. По id.',
  'starter': '-- semi-join\nSELECT\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n",
  'expected': [[1, 'user1@Mail.ru'],
               [51, 'user51@Mail.ru'],
               [101, 'user101@Mail.ru'],
               [151, 'user151@Mail.ru'],
               [201, 'user201@Mail.ru'],
               [251, 'user251@Mail.ru']],
  'expected_cols': ['id', 'email'],
  'hint': 'EXISTS не размножает строки, в отличие от JOIN.',
  'ordered': True},
 {'id': 'd13-join-card',
  'mode': 'sql',
  'title': 'Размер соединения',
  'statement': 'Выведите число строк в результате соединения users и orders по user_id: колонка n.',
  'starter': '-- размер результата\nSELECT\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, city TEXT NOT NULL, status TEXT '
           'NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, created INTEGER NOT NULL, '
           'total INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 300) INSERT INTO users '
           "SELECT i, 'user' || i || '@Mail.ru', CASE i % 4 WHEN 0 THEN 'Москва' WHEN 1 THEN 'Казань' WHEN 2 "
           "THEN 'Тверь' ELSE 'Омск' END, CASE WHEN i % 10 = 0 THEN 'blocked' ELSE 'active' END FROM n;\n"
           'WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 3000) INSERT INTO '
           'orders SELECT i, 1 + (i * 7) % 300, 1000 + i, 10 + (i * 13) % 500, CASE WHEN i % 50 = 0 THEN '
           "'new' ELSE 'done' END FROM n;\n",
  'expected': [[3000]],
  'expected_cols': ['n'],
  'hint': 'Каждый заказ найдёт своего пользователя — результат равен числу заказов.'},
 {'id': 'd13-cost-seq',
  'mode': 'func',
  'func': 'seq_scan_cost',
  'title': 'Стоимость просмотра',
  'statement': 'Стоимость последовательного просмотра = страниц · 1.0 + строк · 0.01. Напишите '
               'seq_scan_cost(pages, rows): число, округлённое до двух знаков.',
  'starter': 'def seq_scan_cost(pages, rows):\n    pass\n',
  'tests': [{'args': [100, 10000], 'expected': 200.0},
            {'args': [0, 0], 'expected': 0.0},
            {'args': [1, 1], 'expected': 1.01},
            {'args': [5000, 400000], 'expected': 9000.0}],
  'hint': 'Подставьте в формулу и округлите.'},
 {'id': 'd13-cost-index',
  'mode': 'func',
  'func': 'index_scan_cost',
  'title': 'Стоимость индексного поиска',
  'statement': 'Индексный поиск: на каждую подходящую строку случайное чтение страницы (4.0) плюс 0.01 за '
               'строку, плюс подъём по дереву (height · 4.0). Напишите index_scan_cost(matching_rows, '
               'height): число, округлённое до двух знаков.',
  'starter': 'def index_scan_cost(matching_rows, height):\n    pass\n',
  'tests': [{'args': [10, 3], 'expected': 52.1},
            {'args': [0, 3], 'expected': 12.0},
            {'args': [1000, 4], 'expected': 4026.0},
            {'args': [1, 1], 'expected': 8.01}],
  'hint': 'height·4 + строки·(4 + 0.01).'},
 {'id': 'd13-choose-access',
  'mode': 'func',
  'func': 'choose_access',
  'title': 'Просмотр или индекс?',
  'statement': 'Просмотр стоит pages + rows·0.01, индекс — height·4 + matching·4.01. Напишите '
               "choose_access(pages, rows, matching, height): 'seq', если просмотр строго дешевле, иначе "
               "'index'.",
  'starter': 'def choose_access(pages, rows, matching, height):\n    pass\n',
  'tests': [{'args': [1000, 100000, 10, 3], 'expected': 'index'},
            {'args': [1000, 100000, 5000, 3], 'expected': 'seq'},
            {'args': [10, 100, 5, 2], 'expected': 'seq'},
            {'args': [100, 1000, 25, 1], 'expected': 'index'}],
  'hint': 'Сравните две стоимости; при равенстве выбираем индекс.'},
 {'id': 'd13-breakeven',
  'mode': 'func',
  'func': 'breakeven_rows',
  'title': 'Точка безубыточности',
  'statement': 'Для просмотра за pages + rows·0.01 и индекса за height·4 + m·4.01 найдите наибольшее целое '
               'число подходящих строк m, при котором индекс ещё не дороже просмотра. Напишите '
               'breakeven_rows(pages, rows, height); если даже при m = 0 индекс дороже — вернуть −1.',
  'starter': 'def breakeven_rows(pages, rows, height):\n    pass\n',
  'tests': [{'args': [1000, 100000, 3], 'expected': 495},
            {'args': [10, 100, 2], 'expected': 0},
            {'args': [1, 0, 1], 'expected': -1},
            {'args': [500, 20000, 4], 'expected': 170}],
  'hint': 'm = (seq − height·4) / 4.01, округлите вниз и проверьте границу.'},
 {'id': 'd13-nested-loop-cost',
  'mode': 'func',
  'func': 'nested_loop_cost',
  'title': 'Вложенные циклы',
  'statement': 'Внешняя таблица возвращает outer_rows строк. Для каждой делается поиск во внутренней: '
               'index_probe_cost, если индекс есть, иначе просмотр inner_pages. Напишите '
               'nested_loop_cost(outer_rows, inner_pages, has_index, index_probe_cost): outer_rows · '
               '(index_probe_cost, если has_index, иначе inner_pages).',
  'starter': 'def nested_loop_cost(outer_rows, inner_pages, has_index, index_probe_cost):\n    pass\n',
  'tests': [{'args': [10, 1000, True, 4], 'expected': 40},
            {'args': [10, 1000, False, 4], 'expected': 10000},
            {'args': [0, 100, True, 3], 'expected': 0},
            {'args': [1000, 50, False, 5], 'expected': 50000}],
  'hint': 'Умножьте число строк внешней таблицы на цену одного поиска.'},
 {'id': 'd13-hash-join-cost',
  'mode': 'func',
  'func': 'hash_join_cost',
  'title': 'Хеш-соединение',
  'statement': 'Хеш-соединение читает обе таблицы один раз и строит хеш-таблицу по меньшей: стоимость = '
               'pages_a + pages_b + 0.02·(rows_a + rows_b). Напишите hash_join_cost(pages_a, rows_a, '
               'pages_b, rows_b): число, округлённое до двух знаков.',
  'starter': 'def hash_join_cost(pages_a, rows_a, pages_b, rows_b):\n    pass\n',
  'tests': [{'args': [100, 10000, 1000, 100000], 'expected': 3300.0},
            {'args': [0, 0, 0, 0], 'expected': 0.0},
            {'args': [1, 10, 1, 10], 'expected': 2.4}],
  'hint': 'Сложите страницы и 0.02 от суммы строк.'},
 {'id': 'd13-merge-join-cost',
  'mode': 'func',
  'func': 'merge_join_cost',
  'title': 'Соединение слиянием',
  'statement': 'Слияние требует сортировки по каждой несортированной стороне: n·log₂(n)·0.01 (округлите итог '
               'до двух знаков; для n ≤ 1 сортировка стоит 0), затем проход 0.01·(rows_a + rows_b). Напишите '
               'merge_join_cost(rows_a, sorted_a, rows_b, sorted_b): sorted_* = True означает, что '
               'сортировка не нужна.',
  'starter': 'def merge_join_cost(rows_a, sorted_a, rows_b, sorted_b):\n    pass\n',
  'tests': [{'args': [1000, True, 2000, True], 'expected': 30.0},
            {'args': [1000, False, 2000, True], 'expected': 129.66},
            {'args': [1024, False, 1024, False], 'expected': 225.28},
            {'args': [1, False, 0, False], 'expected': 0.01}],
  'hint': 'Функция сортировки по сторонам + линейный проход.'},
 {'id': 'd13-pick-join',
  'mode': 'func',
  'func': 'pick_join',
  'title': 'Выбор алгоритма соединения',
  'statement': 'Напишите pick_join(outer_rows, inner_has_index, equality, both_sorted): если соединение не '
               "по равенству — 'nested'; иначе если обе стороны отсортированы — 'merge'; иначе если "
               "внутренняя таблица с индексом и outer_rows ≤ 100 — 'nested'; иначе 'hash'.",
  'starter': 'def pick_join(outer_rows, inner_has_index, equality, both_sorted):\n    pass\n',
  'tests': [{'args': [10, True, True, False], 'expected': 'nested'},
            {'args': [10000, True, True, False], 'expected': 'hash'},
            {'args': [10, False, False, False], 'expected': 'nested'},
            {'args': [5000, False, True, True], 'expected': 'merge'},
            {'args': [50, False, True, False], 'expected': 'hash'}],
  'hint': 'Проверяйте условия в указанном порядке.'},
 {'id': 'd13-eq-selectivity',
  'mode': 'func',
  'func': 'eq_selectivity',
  'title': 'Селективность равенства',
  'statement': 'Статистика столбца: mcv — словарь «значение → доля» (самые частые), n_distinct — число '
               'различных значений. Для значения из mcv селективность — его доля; иначе оставшаяся доля (1 − '
               'сумма долей mcv) делится поровну между остальными различными значениями: (1 − Σ) / '
               '(n_distinct − len(mcv)). Напишите eq_selectivity(mcv, n_distinct, value): число, округлённое '
               'до 4 знаков.',
  'starter': 'def eq_selectivity(mcv, n_distinct, value):\n    pass\n',
  'tests': [{'args': [{'Москва': 0.4, 'Казань': 0.3}, 10, 'Москва'], 'expected': 0.4},
            {'args': [{'Москва': 0.4, 'Казань': 0.3}, 10, 'Омск'], 'expected': 0.0375},
            {'args': [{}, 5, 'x'], 'expected': 0.2},
            {'args': [{'a': 1.0}, 1, 'b'], 'expected': 0.0}],
  'hint': 'Два случая: значение из частых или из «хвоста».'},
 {'id': 'd13-range-selectivity',
  'mode': 'func',
  'func': 'range_selectivity',
  'title': 'Селективность диапазона',
  'statement': 'Гистограмма — список границ корзин bounds (возрастает), в каждой корзине поровну строк. Доля '
               'строк в диапазоне [lo, hi] — число корзин, целиком лежащих внутри, плюс части крайних '
               '(линейная интерполяция), делённое на число корзин. Напишите range_selectivity(bounds, lo, '
               'hi): число, округлённое до 4 знаков; диапазон вне границ обрезается.',
  'starter': 'def range_selectivity(bounds, lo, hi):\n    pass\n',
  'tests': [{'args': [[0, 10, 20, 30, 40], 10, 30], 'expected': 0.5},
            {'args': [[0, 10, 20, 30, 40], 5, 15], 'expected': 0.25},
            {'args': [[0, 100], -50, 50], 'expected': 0.5},
            {'args': [[0, 10, 20], 30, 40], 'expected': 0.0},
            {'args': [[0, 10, 20, 30, 40], 0, 40], 'expected': 1.0}],
  'hint': 'Для каждой корзины возьмите долю её длины, попавшую в диапазон; сложите и разделите на число '
          'корзин.'},
 {'id': 'd13-combine-sel',
  'mode': 'func',
  'func': 'combined_rows',
  'title': 'Оценка числа строк',
  'statement': 'Таблица из rows строк, список селективностей условий sels, условия независимы. Напишите '
               'combined_rows(rows, sels): оценку числа строк — rows · произведение долей — округлённую до '
               'целого, но не меньше 1.',
  'starter': 'def combined_rows(rows, sels):\n    pass\n',
  'tests': [{'args': [1000000, [0.1, 0.05]], 'expected': 5000},
            {'args': [100, [0.001]], 'expected': 1},
            {'args': [100, []], 'expected': 100},
            {'args': [1000, [0.5, 0.5, 0.5]], 'expected': 125}],
  'hint': 'Перемножьте доли и умножьте на число строк; минимум 1.'},
 {'id': 'd13-join-card-est',
  'mode': 'func',
  'func': 'join_cardinality',
  'title': 'Размер соединения',
  'statement': 'Оценка размера соединения по равенству: |A|·|B| / max(d_a, d_b), где d_* — число различных '
               'значений ключа в таблице. Напишите join_cardinality(rows_a, rows_b, d_a, d_b): оценку, '
               'округлённую до целого (минимум 0).',
  'starter': 'def join_cardinality(rows_a, rows_b, d_a, d_b):\n    pass\n',
  'tests': [{'args': [1000, 100, 100, 100], 'expected': 1000},
            {'args': [1000, 5000, 1000, 50], 'expected': 5000},
            {'args': [0, 10, 1, 1], 'expected': 0},
            {'args': [10, 10, 10, 10], 'expected': 10}],
  'hint': 'Формулу — в код; деление на максимум из различных значений.'},
 {'id': 'd13-qerror',
  'mode': 'func',
  'func': 'q_error',
  'title': 'Ошибка оценки',
  'statement': 'Q-ошибка — во сколько раз оценка отличается от факта: max(est/actual, actual/est), '
               'округлённое до двух знаков. Напишите q_error(est, actual); если любое значение 0, заменить '
               'его на 1.',
  'starter': 'def q_error(est, actual):\n    pass\n',
  'tests': [{'args': [10, 1000], 'expected': 100.0},
            {'args': [1000, 10], 'expected': 100.0},
            {'args': [50, 50], 'expected': 1.0},
            {'args': [0, 7], 'expected': 7.0}],
  'hint': 'Заменить нули на 1, затем максимум из двух отношений.'},
 {'id': 'd13-count-orders',
  'mode': 'func',
  'func': 'join_orders',
  'title': 'Сколько порядков соединения',
  'statement': 'Для n таблиц число порядков левоглубокого соединения — n!, число всех порядков с учётом форм '
               'дерева (bushy) — (2n−2)! / (n−1)!. Напишите join_orders(n): пару [левоглубокие, все]. Для n '
               '= 1 — [1, 1].',
  'starter': 'def join_orders(n):\n    pass\n',
  'tests': [{'args': [1], 'expected': [1, 1]},
            {'args': [2], 'expected': [2, 2]},
            {'args': [3], 'expected': [6, 12]},
            {'args': [5], 'expected': [120, 1680]},
            {'args': [8], 'expected': [40320, 17297280]}],
  'hint': 'math.factorial; для n = 1 вернуть единицы.'},
 {'id': 'd13-best-order',
  'mode': 'func',
  'func': 'best_order_cost',
  'title': 'Лучший порядок соединения',
  'statement': 'Даны размеры таблиц sizes и общая селективность соединения sel (одна для всех пар): размер '
               'соединения подмножества размера k — произведение размеров · sel^(k−1). Левоглубокий порядок '
               'стоит сумме размеров всех промежуточных результатов (после каждого соединения). Напишите '
               'best_order_cost(sizes, sel): минимальную стоимость, округлённую до двух знаков (для одной '
               'таблицы — 0).',
  'starter': 'def best_order_cost(sizes, sel):\n    pass\n',
  'tests': [{'args': [[1000, 10, 100], 0.01], 'expected': 110.0},
            {'args': [[100], 0.5], 'expected': 0.0},
            {'args': [[5, 5], 0.2], 'expected': 5.0},
            {'args': [[1000, 1000, 10, 10], 0.001], 'expected': 0.3}],
  'hint': 'Переберите перестановки и посчитайте сумму промежуточных результатов; возьмите минимум.'},
 {'id': 'd13-plan-self-cost',
  'mode': 'func',
  'func': 'hottest_node',
  'title': 'Самый дорогой узел',
  'statement': 'План — список узлов [глубина, название, общая стоимость] в порядке вывода (родитель идёт '
               'перед детьми; глубина корня 0). Собственная стоимость узла = его общая − сумма общих '
               'стоимостей прямых детей. Напишите hottest_node(plan): название узла с наибольшей собственной '
               'стоимостью (при равенстве — первого по порядку).',
  'starter': 'def hottest_node(plan):\n    pass\n',
  'tests': [{'args': [[[0, 'Sort', 1000],
                       [1, 'Hash Join', 900],
                       [2, 'Seq Scan a', 600],
                       [2, 'Seq Scan b', 100]]],
             'expected': 'Seq Scan a'},
            {'args': [[[0, 'Scan', 50]]], 'expected': 'Scan'},
            {'args': [[[0, 'A', 10], [1, 'B', 8], [1, 'C', 1]]], 'expected': 'B'}],
  'hint': 'Для каждого узла вычтите общие стоимости прямых детей — это следующие узлы с глубиной на единицу '
          'больше до возвращения на ту же или меньшую.'},
 {'id': 'd13-slow-queries',
  'mode': 'func',
  'func': 'top_total_time',
  'title': 'Самые тяжёлые запросы',
  'statement': 'Статистика — список [запрос, вызовов, среднее время мс]. Суммарное время = вызовов · '
               'среднее. Напишите top_total_time(stats, k): список названий запросов k самых тяжёлых по '
               'суммарному времени (по убыванию; при равенстве — по названию).',
  'starter': 'def top_total_time(stats, k):\n    pass\n',
  'tests': [{'args': [[['q1', 10000, 2], ['q2', 50, 4000], ['q3', 1000000, 0.1]], 2],
             'expected': ['q2', 'q3']},
            {'args': [[], 3], 'expected': []},
            {'args': [[['a', 1, 1], ['b', 1, 1]], 5], 'expected': ['a', 'b']}],
  'hint': 'Сортировка по убыванию вызовов·среднее и по названию.'},
 {'id': 'd13-generic-plan',
  'mode': 'func',
  'func': 'use_generic_plan',
  'title': 'Общий или индивидуальный план',
  'statement': 'Стоимости индивидуальных планов первых вызовов — список custom. Общий план стоит generic. '
               'Правило: использовать общий план, если generic ≤ среднего индивидуальных · 1.1 и вызовов '
               'было не меньше 5; иначе индивидуальный. Напишите use_generic_plan(custom, generic): True, '
               'если выбираем общий.',
  'starter': 'def use_generic_plan(custom, generic):\n    pass\n',
  'tests': [{'args': [[10, 11, 9, 10, 10], 10.5], 'expected': True},
            {'args': [[10, 11, 9, 10, 10], 12], 'expected': False},
            {'args': [[10, 10], 5], 'expected': False},
            {'args': [[], 1], 'expected': False}],
  'hint': 'Сначала проверка числа вызовов, потом сравнение со средним.'}]}
