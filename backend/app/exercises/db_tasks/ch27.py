"""Задачи книги «Базы данных»: глава 27."""

TASKS: dict[int, list[dict]] = {27: [{'id': 'd11-fd-violations',
  'mode': 'sql',
  'title': 'Нарушения зависимости',
  'statement': 'В таблице flat должно выполняться «клиент → город»: у одного клиента один город. Выведите '
               'клиентов, у которых нарушено: колонки client, n — число разных городов; по клиенту.',
  'starter': '-- клиенты с несколькими городами\nSELECT\n',
  'setup': 'CREATE TABLE flat (order_id INTEGER, client TEXT, city TEXT, product TEXT, price INTEGER);\n'
           'INSERT INTO flat VALUES '
           "(1,'Анна','Москва','Чай',120),(2,'Анна','Казань','Кофе',300),(3,'Борис','Казань','Чай',130),(4,'Вера','Москва','Сыр',350),(5,'Анна','Москва','Чай',120);\n",
  'expected': [['Анна', 2]],
  'expected_cols': ['client', 'n'],
  'hint': 'GROUP BY client и HAVING COUNT(DISTINCT city) > 1.',
  'ordered': True},
 {'id': 'd11-fd-product-price',
  'mode': 'sql',
  'title': 'Цена определяется товаром?',
  'statement': 'Проверьте зависимость «товар → цена»: выведите товары, у которых в таблице больше одного '
               'значения цены. Колонки product, prices (число разных цен); по товару.',
  'starter': '-- товар → цена\nSELECT\n',
  'setup': 'CREATE TABLE flat (order_id INTEGER, client TEXT, city TEXT, product TEXT, price INTEGER);\n'
           'INSERT INTO flat VALUES '
           "(1,'Анна','Москва','Чай',120),(2,'Анна','Казань','Кофе',300),(3,'Борис','Казань','Чай',130),(4,'Вера','Москва','Сыр',350),(5,'Анна','Москва','Чай',120);\n",
  'expected': [['Чай', 2]],
  'expected_cols': ['product', 'prices'],
  'hint': 'COUNT(DISTINCT price) по товару.',
  'ordered': True},
 {'id': 'd11-extract-clients',
  'mode': 'sql',
  'title': 'Выносим клиентов',
  'statement': 'Создайте таблицу clients(client, city) — по одной строке на клиента (CREATE TABLE … AS '
               'SELECT DISTINCT). Итог проверяется по её содержимому.',
  'starter': '-- таблица клиентов\nCREATE TABLE clients AS\n',
  'setup': 'CREATE TABLE flat (order_id INTEGER, client TEXT, city TEXT, product TEXT, price INTEGER, qty '
           'INTEGER);\n'
           'INSERT INTO flat VALUES '
           "(1,'Анна','Москва','Чай',120,2),(2,'Анна','Москва','Кофе',300,1),(3,'Борис','Казань','Чай',120,3),(4,'Вера','Москва','Сыр',350,1),(5,'Борис','Казань','Кофе',300,2),(6,'Глеб','Тверь','Чай',120,1);\n",
  'expected': [['Анна', 'Москва'], ['Борис', 'Казань'], ['Вера', 'Москва'], ['Глеб', 'Тверь']],
  'expected_cols': ['client', 'city'],
  'hint': 'SELECT DISTINCT client, city FROM flat.',
  'ordered': True,
  'check': 'SELECT client, city FROM clients ORDER BY client'},
 {'id': 'd11-extract-products',
  'mode': 'sql',
  'title': 'Выносим товары',
  'statement': 'Создайте таблицу products(product, price) — по одной строке на товар. Итог проверяется по её '
               'содержимому.',
  'starter': '-- таблица товаров\nCREATE TABLE products AS\n',
  'setup': 'CREATE TABLE flat (order_id INTEGER, client TEXT, city TEXT, product TEXT, price INTEGER, qty '
           'INTEGER);\n'
           'INSERT INTO flat VALUES '
           "(1,'Анна','Москва','Чай',120,2),(2,'Анна','Москва','Кофе',300,1),(3,'Борис','Казань','Чай',120,3),(4,'Вера','Москва','Сыр',350,1),(5,'Борис','Казань','Кофе',300,2),(6,'Глеб','Тверь','Чай',120,1);\n",
  'expected': [['Кофе', 300], ['Сыр', 350], ['Чай', 120]],
  'expected_cols': ['product', 'price'],
  'hint': 'SELECT DISTINCT product, price FROM flat.',
  'ordered': True,
  'check': 'SELECT product, price FROM products ORDER BY product'},
 {'id': 'd11-lossless-check',
  'mode': 'sql',
  'title': 'Разложение без потерь?',
  'statement': 'Исходную таблицу flat разложили на orders(order_id, client, product, qty), clients(client, '
               'city) и products(product, price) (создайте их сами в запросе через WITH). Выведите одну '
               'строку и одну колонку lost — число строк flat, которых нет в соединении этих трёх таблиц (0, '
               'если разложение без потерь).',
  'starter': '-- проверяем, что соединение возвращает исходное\nWITH\n',
  'setup': 'CREATE TABLE flat (order_id INTEGER, client TEXT, city TEXT, product TEXT, price INTEGER, qty '
           'INTEGER);\n'
           'INSERT INTO flat VALUES '
           "(1,'Анна','Москва','Чай',120,2),(2,'Анна','Москва','Кофе',300,1),(3,'Борис','Казань','Чай',120,3),(4,'Вера','Москва','Сыр',350,1),(5,'Борис','Казань','Кофе',300,2),(6,'Глеб','Тверь','Чай',120,1);\n",
  'expected': [[0]],
  'expected_cols': ['lost'],
  'hint': 'Соберите соединение и вычтите его из flat оператором EXCEPT; сравнивайте строки целиком.'},
 {'id': 'd11-spurious-rows',
  'mode': 'sql',
  'title': 'Лишние строки при плохом разложении',
  'statement': 'Таблицу r(a, b, c) разложили на r1(a, b) и r2(b, c) — общий столбец b не ключ. Выведите '
               'число строк соединения r1 ⋈ r2 минус число строк r: колонка extra.',
  'starter': '-- сколько лишних строк\nSELECT\n',
  'setup': 'CREATE TABLE r (a INTEGER, b TEXT, c TEXT);\n'
           "INSERT INTO r VALUES (1,'x','p'),(2,'x','q'),(3,'y','r');\n",
  'expected': [[2]],
  'expected_cols': ['extra'],
  'hint': 'Соедините DISTINCT-проекции по b и вычтите COUNT(*) из r.'},
 {'id': 'd11-tree-path',
  'mode': 'sql',
  'title': 'Поддерево по пути',
  'statement': 'Выведите все потомки категории «Напитки» (id 2), но не её саму: колонки id, name; по id. '
               'Используйте столбец path.',
  'starter': '-- поддерево\nSELECT\n',
  'setup': 'CREATE TABLE cat (id INTEGER PRIMARY KEY, name TEXT NOT NULL, path TEXT NOT NULL);\n'
           'INSERT INTO cat VALUES '
           "(1,'Каталог','/1/'),(2,'Напитки','/1/2/'),(3,'Чай','/1/2/3/'),(4,'Кофе','/1/2/4/'),(5,'Еда','/1/5/'),(6,'Сыр','/1/5/6/');\n",
  'expected': [[3, 'Чай'], [4, 'Кофе']],
  'expected_cols': ['id', 'name'],
  'hint': "path LIKE '/1/2/%' и исключите саму строку.",
  'ordered': True},
 {'id': 'd11-adjacency-recursive',
  'mode': 'sql',
  'title': 'Предки по списку смежности',
  'statement': 'Выведите всех предков категории «Чай» (id 3) от ближнего к корню: колонки id, name, depth (1 '
               '— родитель). Порядок по depth.',
  'starter': '-- рекурсивный подъём\nWITH RECURSIVE\n',
  'setup': 'CREATE TABLE cat (id INTEGER PRIMARY KEY, parent_id INTEGER REFERENCES cat(id), name TEXT NOT '
           'NULL);\n'
           'INSERT INTO cat VALUES '
           "(1,NULL,'Каталог'),(2,1,'Напитки'),(3,2,'Чай'),(4,2,'Кофе'),(5,1,'Еда'),(6,5,'Сыр');\n",
  'expected': [[2, 'Напитки', 1], [1, 'Каталог', 2]],
  'expected_cols': ['id', 'name', 'depth'],
  'hint': 'WITH RECURSIVE: начните с родителя узла 3, затем поднимайтесь по parent_id, увеличивая depth.',
  'ordered': True},
 {'id': 'd11-closure-build',
  'mode': 'sql',
  'title': 'Таблица замыканий',
  'statement': 'Постройте таблицу closure(ancestor, descendant, depth), где каждая пара «предок — потомок» '
               '(включая пару узла с самим собой, depth = 0) присутствует ровно один раз. Итог проверяется '
               'по closure.',
  'starter': '-- замыкание дерева\nCREATE TABLE closure AS\nWITH RECURSIVE\n',
  'setup': 'CREATE TABLE cat (id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT NOT NULL);\n'
           "INSERT INTO cat VALUES (1,NULL,'Каталог'),(2,1,'Напитки'),(3,2,'Чай'),(4,1,'Еда');\n",
  'expected': [[1, 1, 0], [1, 2, 1], [1, 3, 2], [1, 4, 1], [2, 2, 0], [2, 3, 1], [3, 3, 0], [4, 4, 0]],
  'expected_cols': ['ancestor', 'descendant', 'depth'],
  'hint': 'Рекурсия: стартовые пары (id, id, 0), затем потомки потомков с depth + 1.',
  'ordered': True,
  'check': 'SELECT ancestor, descendant, depth FROM closure ORDER BY ancestor, descendant'},
 {'id': 'd11-soft-delete',
  'mode': 'sql',
  'title': 'Мягкое удаление и уникальность',
  'statement': 'Создайте уникальный индекс uq_users_email так, чтобы почта была уникальна только среди '
               'неудалённых пользователей (частичный индекс по deleted_at IS NULL). Затем вставьте '
               "пользователя с почтой 'b@x.ru' (раньше он был удалён). Итог проверяется по таблице users.",
  'starter': '-- частичный уникальный индекс\nCREATE UNIQUE INDEX uq_users_email\n',
  'setup': 'CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, deleted_at TEXT);\n'
           "INSERT INTO users VALUES (1,'a@x.ru',NULL),(2,'b@x.ru','2026-01-01'),(3,'c@x.ru',NULL);\n",
  'expected': [[1, 'a@x.ru', None], [2, 'b@x.ru', '2026-01-01'], [3, 'c@x.ru', None], [4, 'b@x.ru', None]],
  'expected_cols': ['id', 'email', 'deleted_at'],
  'hint': 'CREATE UNIQUE INDEX … ON users(email) WHERE deleted_at IS NULL; затем обычный INSERT.',
  'ordered': True,
  'check': 'SELECT id, email, deleted_at FROM users ORDER BY id'},
 {'id': 'd11-check-constraint',
  'mode': 'sql',
  'title': 'Ограничения в схеме',
  'statement': 'Создайте таблицу orders(id INTEGER PRIMARY KEY, total INTEGER NOT NULL, status TEXT NOT '
               "NULL) с проверками: total >= 0 и status только 'new', 'paid' или 'cancelled'. Затем вставьте "
               "корректную строку (1, 100, 'new'). Итог проверяется по таблице orders и по sql в "
               'sqlite_master (в нём должны быть оба условия).',
  'starter': '-- таблица с CHECK\nCREATE TABLE orders (\n',
  'setup': '',
  'expected': [[1, 100, 'new', 1]],
  'expected_cols': ['id', 'total', 'status', 'has_checks'],
  'hint': "CHECK (total >= 0) и CHECK (status IN ('new','paid','cancelled')); sqlite_master хранит исходный "
          'текст.',
  'ordered': True,
  'check': "SELECT id, total, status, (SELECT sql LIKE '%total >= 0%' AND sql LIKE '%IN (%' FROM "
           "sqlite_master WHERE name = 'orders') AS has_checks FROM orders"},
 {'id': 'd11-fk-cascade',
  'mode': 'sql',
  'title': 'Каскадное удаление',
  'statement': 'Удалите клиента Анна (id 1). Благодаря внешнему ключу ON DELETE CASCADE её заказы должны '
               'исчезнуть сами. Итог проверяется по таблице orders.',
  'starter': '-- удалить клиента\nDELETE FROM\n',
  'setup': 'PRAGMA foreign_keys = ON;\n'
           'CREATE TABLE clients (id INTEGER PRIMARY KEY, name TEXT);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL REFERENCES clients(id) '
           'ON DELETE CASCADE, total INTEGER);\n'
           "INSERT INTO clients VALUES (1,'Анна'),(2,'Борис');\n"
           'INSERT INTO orders VALUES (1,1,10),(2,1,20),(3,2,30);\n',
  'expected': [[3, 2, 30]],
  'expected_cols': ['id', 'client_id', 'total'],
  'hint': 'Внешние ключи в SQLite включает PRAGMA foreign_keys = ON; после этого достаточно DELETE клиента.',
  'ordered': True,
  'check': 'SELECT id, client_id, total FROM orders ORDER BY id'},
 {'id': 'd11-snapshot-price',
  'mode': 'sql',
  'title': 'Цена на момент покупки',
  'statement': 'Добавьте в order_items столбец price_at_purchase, заполните его текущей ценой товара '
               '(UPDATE) и затем поднимите цену чая до 150. Итог проверяется по запросу: сумма '
               'price_at_purchase * qty по заказам (order_id, total) — она не должна измениться из-за новой '
               'цены.',
  'starter': '-- копия цены в позиции\nALTER TABLE order_items\n',
  'setup': 'CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER);\n'
           'CREATE TABLE order_items (order_id INTEGER, product_id INTEGER, qty INTEGER);\n'
           "INSERT INTO products VALUES (1,'Чай',120),(2,'Кофе',300);\n"
           'INSERT INTO order_items VALUES (1,1,2),(1,2,1),(2,1,3);\n',
  'expected': [[1, 540], [2, 360]],
  'expected_cols': ['order_id', 'total'],
  'hint': 'ADD COLUMN, затем UPDATE с подзапросом цены и только потом смена цены в products.',
  'ordered': True,
  'check': 'SELECT order_id, SUM(price_at_purchase * qty) AS total FROM order_items GROUP BY order_id ORDER '
           'BY order_id'},
 {'id': 'd11-money-cents',
  'mode': 'sql',
  'title': 'Деньги целыми',
  'statement': 'Суммы хранились дробными числами. Выведите итог в копейках — целое число: колонка cents = '
               'сумма amount·100, округлённая функцией ROUND до целого и приведённая к целому типу (CAST … '
               'AS INTEGER). Суммируйте округлённые по строкам значения, а не округляйте итог.',
  'starter': '-- итог в копейках\nSELECT\n',
  'setup': 'CREATE TABLE pay (id INTEGER PRIMARY KEY, amount REAL);\n'
           'INSERT INTO pay VALUES (1,0.1),(2,0.1),(3,0.1),(4,19.99),(5,0.05);\n',
  'expected': [[2034]],
  'expected_cols': ['cents'],
  'hint': 'Округляйте каждую строку: CAST(ROUND(amount * 100) AS INTEGER), затем SUM.'},
 {'id': 'd11-attr-closure',
  'mode': 'func',
  'func': 'attr_closure',
  'title': 'Замыкание набора атрибутов',
  'statement': 'Функциональные зависимости — список пар [левая часть, правая часть] (каждая — список '
               'атрибутов). Напишите attr_closure(attrs, fds): отсортированный список всех атрибутов, '
               'функционально определяемых набором attrs (включая сам attrs). Пример: fds = '
               '[[["a"],["b"]],[["b"],["c"]]], attrs = ["a"] → ["a","b","c"].',
  'starter': 'def attr_closure(attrs, fds):\n    pass\n',
  'tests': [{'args': [['a'], [[['a'], ['b']], [['b'], ['c']]]], 'expected': ['a', 'b', 'c']},
            {'args': [['c'], [[['a'], ['b']], [['b'], ['c']]]], 'expected': ['c']},
            {'args': [['a', 'b'], [[['a', 'b'], ['c']], [['c'], ['d']]]], 'expected': ['a', 'b', 'c', 'd']},
            {'args': [['x'], []], 'expected': ['x']}],
  'hint': 'Повторяйте: если левая часть зависимости уже в результате, добавьте правую; пока что-то '
          'добавляется.'},
 {'id': 'd11-candidate-keys',
  'mode': 'func',
  'func': 'candidate_keys',
  'title': 'Потенциальные ключи',
  'statement': 'Даны атрибуты relation и функциональные зависимости fds (как в предыдущей задаче). Напишите '
               'candidate_keys(relation, fds): список всех потенциальных (минимальных по включению) ключей — '
               'каждый ключ отсортированный список, список ключей отсортирован. Ключ — набор, замыкание '
               'которого равно всем атрибутам.',
  'starter': 'def candidate_keys(relation, fds):\n    pass\n',
  'tests': [{'args': [['a', 'b', 'c'], [[['a'], ['b']], [['b'], ['c']]]], 'expected': [['a']]},
            {'args': [['a', 'b', 'c', 'd'], [[['a', 'b'], ['c']], [['c'], ['d']]]], 'expected': [['a', 'b']]},
            {'args': [['a', 'b'], []], 'expected': [['a', 'b']]},
            {'args': [['a', 'b', 'c'], [[['a'], ['b', 'c']], [['b'], ['a']]]], 'expected': [['a'], ['b']]}],
  'hint': 'Переберите наборы по возрастанию размера; пропускайте надмножества уже найденных ключей.'},
 {'id': 'd11-check-3nf',
  'mode': 'func',
  'func': 'is_3nf',
  'title': 'Третья нормальная форма',
  'statement': 'Отношение — набор атрибутов, дано множество зависимостей (по одному атрибуту справа) и '
               'множество ключевых атрибутов (входят в какой-нибудь потенциальный ключ) prime. Напишите '
               'is_3nf(fds, prime, keys): True, если для каждой зависимости X → A либо A входит в X, либо X '
               '— суперключ (содержит какой-либо ключ из keys), либо A — ключевой атрибут (в prime).',
  'starter': 'def is_3nf(fds, prime, keys):\n    pass\n',
  'tests': [{'args': [[[['a'], ['b']], [['b'], ['c']]], ['a'], [['a']]], 'expected': False},
            {'args': [[[['a'], ['b']], [['a'], ['c']]], ['a'], [['a']]], 'expected': True},
            {'args': [[[['a', 'b'], ['c']], [['c'], ['b']]], ['a', 'b', 'c'], [['a', 'b'], ['a', 'c']]],
             'expected': True},
            {'args': [[], [], []], 'expected': True}],
  'hint': 'Для каждой зависимости проверьте три разрешающих условия; если ни одно не выполнено — не 3НФ.'},
 {'id': 'd11-lossless-join',
  'mode': 'func',
  'func': 'lossless_binary',
  'title': 'Разложение без потерь',
  'statement': 'Отношение с атрибутами relation разложили на две части r1 и r2 (наборы атрибутов, вместе '
               'покрывающие relation). Известны ФЗ fds. Напишите lossless_binary(relation, fds, r1, r2): '
               'True, если общие атрибуты r1 ∩ r2 функционально определяют r1 целиком или r2 целиком '
               '(замыкание общих атрибутов содержит r1 или r2).',
  'starter': 'def lossless_binary(relation, fds, r1, r2):\n    pass\n',
  'tests': [{'args': [['a', 'b', 'c'], [[['a'], ['b']]], ['a', 'b'], ['a', 'c']], 'expected': True},
            {'args': [['a', 'b', 'c'], [], ['a', 'b'], ['b', 'c']], 'expected': False},
            {'args': [['a', 'b', 'c'], [[['b'], ['c']]], ['a', 'b'], ['b', 'c']], 'expected': True},
            {'args': [['a', 'b'], [], ['a'], ['b']], 'expected': False}],
  'hint': 'Замыкание общих атрибутов должно покрыть одну из частей.'},
 {'id': 'd11-normalize-rows',
  'mode': 'func',
  'func': 'split_table',
  'title': 'Разложение плоской таблицы',
  'statement': 'Плоская таблица — список строк [заказ, клиент, город, товар, цена]. Напишите '
               'split_table(rows): тройку списков [заказы [заказ, клиент, товар], клиенты [клиент, город], '
               'товары [товар, цена]] — клиенты и товары без повторов, отсортированы; заказы в исходном '
               'порядке. Если у клиента или товара встречаются разные значения города или цены — оставляйте '
               'первое.',
  'starter': 'def split_table(rows):\n    pass\n',
  'tests': [{'args': [[[1, 'Анна', 'Москва', 'Чай', 120],
                       [2, 'Анна', 'Москва', 'Кофе', 300],
                       [3, 'Борис', 'Казань', 'Чай', 120]]],
             'expected': [[[1, 'Анна', 'Чай'], [2, 'Анна', 'Кофе'], [3, 'Борис', 'Чай']],
                          [['Анна', 'Москва'], ['Борис', 'Казань']],
                          [['Кофе', 300], ['Чай', 120]]]},
            {'args': [[]], 'expected': [[], [], []]},
            {'args': [[[1, 'Анна', 'Москва', 'Чай', 120], [2, 'Анна', 'Казань', 'Чай', 130]]],
             'expected': [[[1, 'Анна', 'Чай'], [2, 'Анна', 'Чай']], [['Анна', 'Москва']], [['Чай', 120]]]}],
  'hint': 'Словари setdefault для клиентов и товаров; заказы — в порядке строк.'},
 {'id': 'd11-gen-ids',
  'mode': 'func',
  'func': 'ordered_ids',
  'title': 'Упорядоченные идентификаторы',
  'statement': 'Идентификатор — пара [время в миллисекундах, счётчик внутри миллисекунды]. Напишите '
               'ordered_ids(times): для списка моментов вставки (возрастают нестрого) вернуть '
               'идентификаторы: счётчик равен числу предыдущих вставок в ту же миллисекунду. Затем результат '
               'должен быть строго возрастающим как пары.',
  'starter': 'def ordered_ids(times):\n    pass\n',
  'tests': [{'args': [[1, 1, 1, 2, 5, 5]], 'expected': [[1, 0], [1, 1], [1, 2], [2, 0], [5, 0], [5, 1]]},
            {'args': [[]], 'expected': []},
            {'args': [[7]], 'expected': [[7, 0]]}],
  'hint': 'Сбрасывайте счётчик при смене миллисекунды.'},
 {'id': 'd11-tenant-keys',
  'mode': 'func',
  'func': 'scope_by_tenant',
  'title': 'Изоляция арендаторов',
  'statement': 'Строки — списки [арендатор, id, значение]. Первичный ключ — пара (арендатор, id). Напишите '
               'scope_by_tenant(rows, tenant): словарь «id → значение» только для строк этого арендатора; '
               'если пара встречается несколько раз — побеждает последняя строка. Ключи словаря — id '
               'строкой.',
  'starter': 'def scope_by_tenant(rows, tenant):\n    pass\n',
  'tests': [{'args': [[['A', 1, 'x'], ['B', 1, 'y'], ['A', 2, 'z'], ['A', 1, 'w']], 'A'],
             'expected': {'1': 'w', '2': 'z'}},
            {'args': [[['A', 1, 'x']], 'B'], 'expected': {}},
            {'args': [[], 'A'], 'expected': {}}],
  'hint': 'Словарь по строкам только нужного арендатора; последняя запись перезаписывает предыдущую.'}]}
