"""Задачи книги «Базы данных»: глава 9."""

TASKS: dict[int, list[dict]] = {9: [{'id': 's09-01',
  'mode': 'sql',
  'title': 'Первая таблица',
  'statement': 'Создайте таблицу tags: id (целое, первичный ключ) и name (текст). Итог проверяется по '
               'структуре таблицы.',
  'starter': 'CREATE TABLE tags (\n  id ...,\n  name ...\n);\n',
  'setup': '\n',
  'expected': [['id', 'INTEGER', 0, None, 1], ['name', 'TEXT', 0, None, 0]],
  'expected_cols': ['name', 'type', 'notnull', 'dflt_value', 'pk'],
  'hint': 'CREATE TABLE имя (столбец тип, столбец тип, …);',
  'ordered': True,
  'check': 'SELECT name, type, "notnull", dflt_value, pk FROM pragma_table_info(\'tags\') ORDER BY cid'},
 {'id': 's09-02',
  'mode': 'sql',
  'title': 'Типы столбцов',
  'statement': 'Создайте таблицу items: id INTEGER PRIMARY KEY, title TEXT, price REAL, stock INTEGER.',
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [['id', 'INTEGER', 0, None, 1],
               ['title', 'TEXT', 0, None, 0],
               ['price', 'REAL', 0, None, 0],
               ['stock', 'INTEGER', 0, None, 0]],
  'expected_cols': ['name', 'type', 'notnull', 'dflt_value', 'pk'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT name, type, "notnull", dflt_value, pk FROM pragma_table_info(\'items\') ORDER BY cid'},
 {'id': 's09-03',
  'mode': 'sql',
  'title': 'NOT NULL',
  'statement': 'Создайте таблицу users: id INTEGER PRIMARY KEY, email TEXT NOT NULL, nickname TEXT '
               '(необязательный).',
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [['id', 'INTEGER', 0, None, 1],
               ['email', 'TEXT', 1, None, 0],
               ['nickname', 'TEXT', 0, None, 0]],
  'expected_cols': ['name', 'type', 'notnull', 'dflt_value', 'pk'],
  'hint': 'NOT NULL запрещает пустые значения.',
  'ordered': True,
  'check': 'SELECT name, type, "notnull", dflt_value, pk FROM pragma_table_info(\'users\') ORDER BY cid'},
 {'id': 's09-04',
  'mode': 'sql',
  'title': 'DEFAULT',
  'statement': 'Создайте таблицу tasks: id INTEGER PRIMARY KEY, title TEXT NOT NULL, status TEXT NOT NULL '
               "DEFAULT 'new', priority INTEGER DEFAULT 3.",
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [['id', 'INTEGER', 0, None, 1],
               ['title', 'TEXT', 1, None, 0],
               ['status', 'TEXT', 1, "'new'", 0],
               ['priority', 'INTEGER', 0, '3', 0]],
  'expected_cols': ['name', 'type', 'notnull', 'dflt_value', 'pk'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT name, type, "notnull", dflt_value, pk FROM pragma_table_info(\'tasks\') ORDER BY cid'},
 {'id': 's09-05',
  'mode': 'sql',
  'title': 'DEFAULT в действии',
  'statement': "Создайте таблицу tasks (как в предыдущем задании), добавьте строку (title = 'написать "
               "отчёт') без status и priority и убедитесь, что подставились значения по умолчанию.",
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [[1, 'написать отчёт', 'new', 3]],
  'expected_cols': ['id', 'title', 'status', 'priority'],
  'hint': '',
  'check': 'SELECT id, title, status, priority FROM tasks'},
 {'id': 's09-06',
  'mode': 'sql',
  'title': 'Текстовый ключ',
  'statement': "Создайте таблицу countries: code TEXT PRIMARY KEY (например, 'RU'), name TEXT NOT NULL.",
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [['code', 'TEXT', 0, None, 1], ['name', 'TEXT', 1, None, 0]],
  'expected_cols': ['name', 'type', 'notnull', 'dflt_value', 'pk'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT name, type, "notnull", dflt_value, pk FROM pragma_table_info(\'countries\') ORDER BY cid'},
 {'id': 's09-07',
  'mode': 'sql',
  'title': 'Составной ключ',
  'statement': 'Создайте таблицу wishlist: customer_id INTEGER, product_id INTEGER, PRIMARY KEY '
               '(customer_id, product_id). Составной ключ запрещает повторы пары.',
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [['customer_id', 'INTEGER', 0, None, 1], ['product_id', 'INTEGER', 0, None, 2]],
  'expected_cols': ['name', 'type', 'notnull', 'dflt_value', 'pk'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT name, type, "notnull", dflt_value, pk FROM pragma_table_info(\'wishlist\') ORDER BY cid'},
 {'id': 's09-08',
  'mode': 'sql',
  'title': 'UNIQUE',
  'statement': 'Создайте таблицу accounts: id INTEGER PRIMARY KEY, login TEXT NOT NULL UNIQUE. Затем INSERT '
               "OR IGNORE двух строк с одинаковым login 'anna' — вторая будет пропущена.",
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [[1, 'anna']],
  'expected_cols': ['id', 'login'],
  'hint': 'OR IGNORE молча пропускает строку, нарушающую ограничение.',
  'check': 'SELECT id, login FROM accounts'},
 {'id': 's09-09',
  'mode': 'sql',
  'title': 'CHECK',
  'statement': 'Создайте таблицу goods: id INTEGER PRIMARY KEY, title TEXT, price INTEGER CHECK (price >= '
               "0). Вставьте через INSERT OR IGNORE строки ('a', 100) и ('b', -5); вторая нарушит CHECK.",
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [[1, 'a', 100]],
  'expected_cols': ['id', 'title', 'price'],
  'hint': '',
  'check': 'SELECT id, title, price FROM goods'},
 {'id': 's09-10',
  'mode': 'sql',
  'title': 'CHECK со списком',
  'statement': 'Создайте таблицу orders2: id INTEGER PRIMARY KEY, status TEXT NOT NULL CHECK (status IN '
               "('new', 'paid', 'shipped')). Вставьте через INSERT OR IGNORE статусы 'paid' и 'lost' — "
               'последний будет отвергнут.',
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [[1, 'paid']],
  'expected_cols': ['id', 'status'],
  'hint': '',
  'check': 'SELECT id, status FROM orders2'},
 {'id': 's09-11',
  'mode': 'sql',
  'title': 'NOT NULL в действии',
  'statement': 'Создайте таблицу people: id INTEGER PRIMARY KEY, name TEXT NOT NULL. INSERT OR IGNORE двух '
               "строк: ('Анна') и (NULL). Останется одна.",
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [[1, 'Анна']],
  'expected_cols': ['id', 'name'],
  'hint': '',
  'check': 'SELECT id, name FROM people'},
 {'id': 's09-12',
  'mode': 'sql',
  'title': 'Составной UNIQUE',
  'statement': 'Создайте таблицу slots: room TEXT, hour INTEGER, UNIQUE (room, hour). Вставьте через INSERT '
               "OR IGNORE ('A', 9), ('A', 10), ('A', 9), ('B', 9) — повтор пары будет отвергнут.",
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [['A', 9], ['A', 10], ['B', 9]],
  'expected_cols': ['room', 'hour'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT room, hour FROM slots ORDER BY room, hour'},
 {'id': 's09-13',
  'mode': 'sql',
  'title': 'Внешний ключ',
  'statement': 'Создайте таблицу reviews: id INTEGER PRIMARY KEY, product_id INTEGER NOT NULL REFERENCES '
               'products(id), stars INTEGER NOT NULL CHECK (stars BETWEEN 1 AND 5), body TEXT. Итог '
               'проверяется по внешним ключам таблицы.',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [['products', 'product_id', 'id']],
  'expected_cols': ['table', 'from', 'to'],
  'hint': 'REFERENCES таблица(столбец) объявляет внешний ключ.',
  'check': 'SELECT "table", "from", "to" FROM pragma_foreign_key_list(\'reviews\')'},
 {'id': 's09-14',
  'mode': 'sql',
  'title': 'Два внешних ключа',
  'statement': 'Создайте таблицу favorites: customer_id INTEGER NOT NULL REFERENCES customers(id), '
               'product_id INTEGER NOT NULL REFERENCES products(id), PRIMARY KEY (customer_id, product_id).',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [['customer_id', 'customers', 'id'], ['product_id', 'products', 'id']],
  'expected_cols': ['from', 'table', 'to'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT "from", "table", "to" FROM pragma_foreign_key_list(\'favorites\') ORDER BY "from"'},
 {'id': 's09-15',
  'mode': 'sql',
  'title': 'ON DELETE CASCADE',
  'statement': 'Создайте таблицу comments: id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES '
               'orders(id) ON DELETE CASCADE, body TEXT. Проверяется правило on_delete внешнего ключа.',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [['orders', 'order_id', 'CASCADE']],
  'expected_cols': ['table', 'from', 'on_delete'],
  'hint': '',
  'check': 'SELECT "table", "from", on_delete FROM pragma_foreign_key_list(\'comments\')'},
 {'id': 's09-16',
  'mode': 'sql',
  'title': 'AUTOINCREMENT',
  'statement': 'Создайте таблицу log: id INTEGER PRIMARY KEY AUTOINCREMENT, msg TEXT. Вставьте три сообщения '
               "'a','b','c', удалите последнее и вставьте 'd' — AUTOINCREMENT не использует освободившийся "
               'номер.',
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [[1, 'a'], [2, 'b'], [4, 'd']],
  'expected_cols': ['id', 'msg'],
  'hint': "Номер 3 уже использован, поэтому 'd' получит 4.",
  'ordered': True,
  'check': 'SELECT id, msg FROM log ORDER BY id'},
 {'id': 's09-17',
  'mode': 'sql',
  'title': 'Новый столбец',
  'statement': 'В таблицу customers добавьте столбец phone TEXT (ALTER TABLE … ADD COLUMN).',
  'starter': 'ALTER TABLE customers\n...;\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [['id', 'INTEGER'],
               ['name', 'TEXT'],
               ['city', 'TEXT'],
               ['email', 'TEXT'],
               ['registered', 'TEXT'],
               ['vip', 'INTEGER'],
               ['phone', 'TEXT']],
  'expected_cols': ['name', 'type'],
  'hint': '',
  'ordered': True,
  'check': "SELECT name, type FROM pragma_table_info('customers') ORDER BY cid"},
 {'id': 's09-18',
  'mode': 'sql',
  'title': 'Столбец с DEFAULT',
  'statement': 'Добавьте в products столбец archived INTEGER NOT NULL DEFAULT 0. Существующие строки получат '
               '0.',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [[1, 'Ноутбук Air 13', 0],
               [2, 'Смартфон S5', 0],
               [3, 'Наушники Beat', 0],
               [4, 'Мышь Click', 0],
               [5, 'Клавиатура Type', 0],
               [6, 'Рюкзак City', 0],
               [7, 'Кофе зерновой', 0],
               [8, 'Чай зелёный', 0],
               [9, 'Шоколад тёмный', 0],
               [10, 'Книга SQL', 0],
               [11, 'Книга Python', 0],
               [12, 'Блокнот A5', 0],
               [13, 'Подарочная карта', 0]],
  'expected_cols': ['id', 'title', 'archived'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT id, title, archived FROM products ORDER BY id'},
 {'id': 's09-19',
  'mode': 'sql',
  'title': 'Новый столбец и данные',
  'statement': "Добавьте в orders столбец note TEXT и заполните его для заказа 1 значением 'подарок'.",
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [[1, 'подарок'], [2, None], [3, None]],
  'expected_cols': ['id', 'note'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT id, note FROM orders WHERE id <= 3 ORDER BY id'},
 {'id': 's09-20',
  'mode': 'sql',
  'title': 'Переименовать таблицу',
  'statement': 'Переименуйте таблицу products в goods (ALTER TABLE … RENAME TO …). Проверяется число строк в '
               'goods.',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [[13]],
  'expected_cols': ['n'],
  'hint': '',
  'check': 'SELECT COUNT(*) AS n FROM goods'},
 {'id': 's09-21',
  'mode': 'sql',
  'title': 'Переименовать столбец',
  'statement': 'Переименуйте столбец title таблицы products в name (RENAME COLUMN).',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [[1, 'Ноутбук Air 13'], [2, 'Смартфон S5'], [3, 'Наушники Beat']],
  'expected_cols': ['id', 'name'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT id, name FROM products ORDER BY id LIMIT 3'},
 {'id': 's09-22',
  'mode': 'sql',
  'title': 'Удалить столбец',
  'statement': 'Удалите столбец brand из таблицы products (ALTER TABLE … DROP COLUMN …).',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [['id'], ['title'], ['category'], ['price'], ['stock']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True,
  'check': "SELECT name FROM pragma_table_info('products') ORDER BY cid"},
 {'id': 's09-23',
  'mode': 'sql',
  'title': 'DROP TABLE',
  'statement': 'Удалите таблицу order_items (DROP TABLE). Проверяется список оставшихся таблиц.',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [['customers'], ['orders'], ['products']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True,
  'check': "SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name"},
 {'id': 's09-24',
  'mode': 'sql',
  'title': 'IF EXISTS',
  'statement': 'Удалите таблицу temp_report, если она есть (DROP TABLE IF EXISTS …), и ещё раз — ошибки быть '
               'не должно. Затем создайте temp_report(id INTEGER). Итог — по структуре.',
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [['id', 'INTEGER', 0, None, 0]],
  'expected_cols': ['name', 'type', 'notnull', 'dflt_value', 'pk'],
  'hint': 'IF EXISTS делает команду безопасной для повторного запуска.',
  'ordered': True,
  'check': 'SELECT name, type, "notnull", dflt_value, pk FROM pragma_table_info(\'temp_report\') ORDER BY '
           'cid'},
 {'id': 's09-25',
  'mode': 'sql',
  'title': 'IF NOT EXISTS',
  'statement': 'Создайте таблицу cache(k TEXT PRIMARY KEY, v TEXT) командой CREATE TABLE IF NOT EXISTS — '
               "дважды подряд, без ошибки. Затем вставьте одну строку ('a','1').",
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [['a', '1']],
  'expected_cols': ['k', 'v'],
  'hint': '',
  'check': 'SELECT k, v FROM cache'},
 {'id': 's09-26',
  'mode': 'sql',
  'title': 'Таблица из запроса',
  'statement': 'Создайте таблицу vip_report из запроса: id, name, city VIP-клиентов (CREATE TABLE … AS '
               'SELECT …).',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [[1, 'Анна Петрова', 'Москва'],
               [5, 'Дарья Лебедева', 'Санкт-Петербург'],
               [10, 'Лев Новиков', 'Санкт-Петербург']],
  'expected_cols': ['id', 'name', 'city'],
  'hint': 'Ограничения и ключи при этом не копируются.',
  'ordered': True,
  'check': 'SELECT id, name, city FROM vip_report ORDER BY id'},
 {'id': 's09-27',
  'mode': 'sql',
  'title': 'Сводная таблица',
  'statement': 'Создайте таблицу sales_by_status(status, n, revenue) из запроса: число заказов и сумма по '
               'статусам (используйте GROUP BY status).',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [['cancelled', 2, 7100], ['new', 4, 86770], ['paid', 6, 123040], ['shipped', 8, 140330]],
  'expected_cols': ['status', 'n', 'revenue'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT status, n, revenue FROM sales_by_status ORDER BY status'},
 {'id': 's09-28',
  'mode': 'sql',
  'title': 'Временная таблица',
  'statement': 'Создайте временную таблицу top_products (CREATE TEMP TABLE … AS SELECT …) с тремя самыми '
               'дорогими товарами: title, price.',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [['Ноутбук Air 13', 78000], ['Смартфон S5', 45000], ['Наушники Beat', 5200]],
  'expected_cols': ['title', 'price'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT title, price FROM top_products ORDER BY price DESC'},
 {'id': 's09-29',
  'mode': 'sql',
  'title': 'Вычисляемый столбец',
  'statement': 'Создайте таблицу lines: qty INTEGER, price INTEGER, total INTEGER GENERATED ALWAYS AS (qty * '
               'price) STORED. Вставьте (2, 150) и (3, 40); total посчитается сам.',
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [[2, 150, 300], [3, 40, 120]],
  'expected_cols': ['qty', 'price', 'total'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT qty, price, total FROM lines ORDER BY qty'},
 {'id': 's09-30',
  'mode': 'sql',
  'title': 'Аффинность типов',
  'statement': 'SQLite приводит значения к типу столбца (аффинность). Создайте таблицу t(a INTEGER), '
               "вставьте '123' (строкой) и 'abc'. Выведите typeof(a) для обеих строк по возрастанию rowid.",
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [[123, 'integer'], ['abc', 'text']],
  'expected_cols': ['a', 't'],
  'hint': "'123' превратится в число, а 'abc' останется текстом.",
  'ordered': True,
  'check': 'SELECT a, typeof(a) AS t FROM t ORDER BY rowid'},
 {'id': 's09-31',
  'mode': 'sql',
  'title': 'Подробный каталог',
  'statement': 'Выведите названия таблиц и число столбцов в каждой: sqlite_master JOIN '
               'pragma_table_info(name); столбцы name, cols; по name.',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [['customers', 6], ['order_items', 4], ['orders', 5], ['products', 6]],
  'expected_cols': ['name', 'cols'],
  'hint': '',
  'ordered': True},
 {'id': 's09-32',
  'mode': 'sql',
  'title': 'Пересоздать с новым ограничением',
  'statement': 'В SQLite ограничение нельзя добавить командой ALTER — таблицу пересоздают. Создайте '
               'goods_new(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price INTEGER NOT NULL CHECK (price > '
               '0)), перенесите в неё id, title, price из products, удалите products и переименуйте '
               'goods_new в products.',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE customers (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT,\n'
           '  email TEXT,\n'
           '  registered TEXT NOT NULL,\n'
           '  vip INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE products (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  category TEXT NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  stock INTEGER NOT NULL,\n'
           '  brand TEXT\n'
           ');\n'
           'CREATE TABLE orders (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  customer_id INTEGER NOT NULL REFERENCES customers(id),\n'
           '  created TEXT NOT NULL,\n'
           '  status TEXT NOT NULL,\n'
           '  total INTEGER NOT NULL DEFAULT 0\n'
           ');\n'
           'CREATE TABLE order_items (\n'
           '  order_id INTEGER NOT NULL REFERENCES orders(id),\n'
           '  product_id INTEGER NOT NULL REFERENCES products(id),\n'
           '  qty INTEGER NOT NULL,\n'
           '  price INTEGER NOT NULL,\n'
           '  PRIMARY KEY (order_id, product_id)\n'
           ');\n'
           'INSERT INTO customers VALUES\n'
           " (1,'Анна Петрова','Москва','anna@mail.ru','2024-01-15',1),\n"
           " (2,'Борис Иванов','Казань','boris@gmail.com','2024-02-03',0),\n"
           " (3,'Вера Смирнова','Москва',NULL,'2024-02-20',0),\n"
           " (4,'Глеб Орлов','Тверь','gleb@yandex.ru','2024-03-11',0),\n"
           " (5,'Дарья Лебедева','Санкт-Петербург','dasha@mail.ru','2024-03-30',1),\n"
           " (6,'Егор Козлов','Казань','egor@gmail.com','2024-04-08',0),\n"
           " (7,'Жанна Морозова',NULL,'zhanna@yandex.ru','2024-04-25',0),\n"
           " (8,'Игорь Соколов','Москва','igor@mail.ru','2024-05-02',0),\n"
           " (9,'Ксения Волкова','Омск',NULL,'2024-05-19',0),\n"
           " (10,'Лев Новиков','Санкт-Петербург','lev@gmail.com','2024-06-07',1),\n"
           " (11,'Мария Фёдорова','Тверь','maria@mail.ru','2024-06-21',0),\n"
           " (12,'Никита Белов','Москва','nikita@yandex.ru','2024-07-04',0);\n"
           'INSERT INTO products VALUES\n'
           " (1,'Ноутбук Air 13','Электроника',78000,5,'Nova'),\n"
           " (2,'Смартфон S5','Электроника',45000,12,'Nova'),\n"
           " (3,'Наушники Beat','Электроника',5200,40,'Sonic'),\n"
           " (4,'Мышь Click','Аксессуары',1500,80,'Sonic'),\n"
           " (5,'Клавиатура Type','Аксессуары',3900,25,'Keyra'),\n"
           " (6,'Рюкзак City','Аксессуары',3200,0,'Urbo'),\n"
           " (7,'Кофе зерновой','Продукты',890,150,'Bean'),\n"
           " (8,'Чай зелёный','Продукты',420,200,'Leaf'),\n"
           " (9,'Шоколад тёмный','Продукты',180,300,'Cacao'),\n"
           " (10,'Книга SQL','Книги',1200,30,'Prime'),\n"
           " (11,'Книга Python','Книги',1350,18,'Prime'),\n"
           " (12,'Блокнот A5','Канцелярия',250,500,NULL),\n"
           " (13,'Подарочная карта','Прочее',1000,999,NULL);\n"
           'INSERT INTO orders (id, customer_id, created, status) VALUES\n'
           " (1,1,'2024-02-01','shipped'),(2,1,'2024-03-15','shipped'),(3,2,'2024-03-02','paid'),\n"
           " (4,2,'2024-04-10','cancelled'),(5,3,'2024-03-05','shipped'),(6,4,'2024-03-20','new'),\n"
           " (7,5,'2024-04-02','shipped'),(8,5,'2024-04-18','paid'),(9,5,'2024-05-07','shipped'),\n"
           " (10,6,'2024-05-01','paid'),(11,8,'2024-05-15','new'),(12,8,'2024-06-03','shipped'),\n"
           " (13,10,'2024-06-10','paid'),(14,10,'2024-06-25','shipped'),(15,11,'2024-07-01','cancelled'),\n"
           " (16,12,'2024-07-08','paid'),(17,1,'2024-07-12','new'),(18,2,'2024-07-20','shipped'),\n"
           " (19,3,'2024-07-22','paid'),(20,5,'2024-07-30','new');\n"
           'INSERT INTO order_items VALUES\n'
           ' (1,1,1,78000),(1,4,1,1500),(2,3,1,5200),(3,2,1,45000),(3,3,2,5200),(4,5,1,3900),\n'
           ' (5,7,2,890),(5,8,3,420),(6,10,1,1200),(6,11,1,1350),(7,2,1,45000),(8,3,1,5200),\n'
           ' (8,4,2,1500),(9,12,10,250),(10,9,5,180),(10,8,2,420),(11,1,1,78000),(12,7,1,890),\n'
           ' (13,2,1,45000),(13,4,1,1500),(14,10,2,1200),(15,6,1,3200),(16,5,1,3900),(16,3,1,5200),\n'
           ' (17,11,1,1350),(17,10,1,1200),(18,9,10,180),(19,8,5,420),(20,7,3,890),(20,12,4,250);\n'
           'UPDATE orders SET total = (SELECT SUM(qty * price) FROM order_items WHERE order_id = '
           'orders.id);\n',
  'expected': [[13, 1]],
  'expected_cols': ['n', 'has_check'],
  'hint': '',
  'check': "SELECT COUNT(*) AS n, (SELECT sql LIKE '%CHECK%' FROM sqlite_master WHERE name = 'products') AS "
           'has_check FROM products'},
 {'id': 's09-33',
  'mode': 'sql',
  'title': 'Разделить таблицу',
  'statement': 'В таблице flat(order_id, customer, city, product, price) данные дублируются. Создайте '
               'таблицу cust(customer, city) без повторов и prod(product, price) без повторов (CREATE TABLE '
               '… AS SELECT DISTINCT …).',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE flat (order_id INTEGER, customer TEXT, city TEXT, product TEXT, price INTEGER);\n'
           'INSERT INTO flat VALUES '
           "(1,'Анна','Москва','Чай',100),(2,'Анна','Москва','Кофе',300),(3,'Борис','Казань','Чай',100),(4,'Борис','Казань','Сыр',350);\n",
  'expected': [['cust', 'Анна', 'Москва'],
               ['cust', 'Борис', 'Казань'],
               ['prod', 'Кофе', 300],
               ['prod', 'Сыр', 350],
               ['prod', 'Чай', 100]],
  'expected_cols': ['t', 'a', 'b'],
  'hint': '',
  'ordered': True,
  'check': "SELECT 'cust' AS t, customer AS a, city AS b FROM cust UNION ALL SELECT 'prod', product, price "
           'FROM prod ORDER BY 1, 2'},
 {'id': 's09-34',
  'mode': 'sql',
  'title': 'Структура таблицы',
  'statement': 'База HR. Выведите для таблицы employees имя, тип и признак notnull каждого столбца в порядке '
               'объявления: SELECT name, type, "notnull" FROM pragma_table_info(\'employees\').',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE departments (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  city TEXT NOT NULL\n'
           ');\n'
           'CREATE TABLE employees (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  dept_id INTEGER REFERENCES departments(id),\n'
           '  boss_id INTEGER REFERENCES employees(id),\n'
           '  salary INTEGER NOT NULL,\n'
           '  hired TEXT NOT NULL,\n'
           '  email TEXT NOT NULL,\n'
           '  phone TEXT,\n'
           '  grade TEXT NOT NULL\n'
           ');\n'
           'INSERT INTO departments VALUES\n'
           " (1,'Разработка','Москва'),(2,'Продажи','Казань'),(3,'Бухгалтерия','Москва'),\n"
           " (4,'Поддержка','Тверь'),(5,'Исследования','Омск');\n"
           'INSERT INTO employees VALUES\n'
           " (1,'Ольга Громова',1,NULL,320000,'2019-03-01','olga@corp.ru','+7 495 111-11-11','lead'),\n"
           " (2,'Игорь Беляев',1,1,210000,'2020-06-15','igor.b@corp.ru','+7 495 111-11-12','senior'),\n"
           " (3,'Мария Орлова',1,1,190000,'2021-01-11','maria@corp.ru',NULL,'middle'),\n"
           " (4,'Пётр Зуев',1,2,120000,'2023-09-04','petr@corp.ru','+7 495 111-11-14','junior'),\n"
           " (5,'Нина Белова',2,NULL,280000,'2018-11-20','nina@corp.ru','+7 843 222-22-21','lead'),\n"
           " (6,'Олег Савин',2,5,150000,'2022-02-14','oleg@corp.ru','+7 843 222-22-22','middle'),\n"
           " (7,'Анна Крылова',2,5,150000,'2022-08-01','anna.k@corp.ru',NULL,'middle'),\n"
           " (8,'Сергей Ким',2,5,95000,'2024-01-09','sergey@corp.ru','+7 843 222-22-24','junior'),\n"
           " (9,'Лидия Фомина',3,NULL,200000,'2017-05-25','lidia@corp.ru','+7 495 333-33-31','lead'),\n"
           " (10,'Роман Дьяков',3,9,110000,'2023-03-13','roman@corp.ru','+7 495 333-33-32','middle'),\n"
           " (11,'Ева Миронова',4,NULL,170000,'2021-10-01','eva@corp.ru','+7 482 444-44-41','lead'),\n"
           " (12,'Артём Исаев',4,11,80000,'2024-03-18','artem@corp.ru',NULL,'junior'),\n"
           " (13,'Вера Жукова',4,11,85000,'2023-12-04','vera.z@corp.ru','+7 482 444-44-43','junior'),\n"
           " (14,'Тимур Рахимов',NULL,NULL,130000,'2024-05-06','timur@corp.ru',NULL,'middle'),\n"
           " (15,'Юлия Седова',2,5,175000,'2020-09-21','yulia@corp.ru','+7 843 222-22-25','senior');\n",
  'expected': [['id', 'INTEGER', 0],
               ['name', 'TEXT', 1],
               ['dept_id', 'INTEGER', 0],
               ['boss_id', 'INTEGER', 0],
               ['salary', 'INTEGER', 1],
               ['hired', 'TEXT', 1],
               ['email', 'TEXT', 1],
               ['phone', 'TEXT', 0],
               ['grade', 'TEXT', 1]],
  'expected_cols': ['name', 'type', 'notnull'],
  'hint': '',
  'ordered': True},
 {'id': 's09-35',
  'mode': 'sql',
  'title': 'Индексы таблицы',
  'statement': 'Создайте таблицу u(id INTEGER PRIMARY KEY, email TEXT UNIQUE, code TEXT UNIQUE) и выведите '
               'число её индексов (pragma_index_list) как n — каждое UNIQUE создаёт индекс.',
  'starter': '-- Напишите запрос\n',
  'setup': '\n',
  'expected': [[2]],
  'expected_cols': ['n'],
  'hint': ''},
 {'id': 's09-36',
  'mode': 'sql',
  'title': 'Школа: новая таблица',
  'statement': 'Школьная база. Создайте таблицу teachers(id INTEGER PRIMARY KEY, name TEXT NOT NULL, subject '
               "TEXT) и добавьте двух преподавателей: 'Н. Крылова' (Математика) и 'А. Беляев' (Физика).",
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE students (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  class TEXT NOT NULL,\n'
           '  birth TEXT NOT NULL,\n'
           '  city TEXT NOT NULL\n'
           ');\n'
           'CREATE TABLE courses (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  teacher TEXT NOT NULL,\n'
           '  hours INTEGER NOT NULL\n'
           ');\n'
           'CREATE TABLE enrollments (\n'
           '  student_id INTEGER NOT NULL REFERENCES students(id),\n'
           '  course_id INTEGER NOT NULL REFERENCES courses(id),\n'
           '  score INTEGER,\n'
           '  year INTEGER NOT NULL,\n'
           '  PRIMARY KEY (student_id, course_id, year)\n'
           ');\n'
           'INSERT INTO students VALUES\n'
           " (1,'Алёна Громова','9А','2009-04-12','Москва'),\n"
           " (2,'Богдан Сидоров','9А','2009-09-30','Казань'),\n"
           " (3,'Варвара Кузнецова','9Б','2009-01-25','Москва'),\n"
           " (4,'Давид Попов','10А','2008-06-18','Тверь'),\n"
           " (5,'Ева Васильева','10А','2008-11-03','Москва'),\n"
           " (6,'Фёдор Михайлов','10Б','2008-02-14','Омск'),\n"
           " (7,'Галина Соколова','11А','2007-07-07','Казань'),\n"
           " (8,'Игнат Павлов','11А','2007-12-21','Москва'),\n"
           " (9,'Яна Тихонова','11Б','2007-03-09','Тверь'),\n"
           " (10,'Тимофей Орлов','9Б','2009-08-15','Москва');\n"
           'INSERT INTO courses VALUES\n'
           " (1,'Математика','Н. Крылова',140),(2,'Физика','А. Беляев',102),(3,'Информатика','М. "
           "Лебедев',68),\n"
           " (4,'Литература','О. Миронова',102),(5,'История','В. Жуков',68),(6,'Химия','Е. Седова',68);\n"
           'INSERT INTO enrollments VALUES\n'
           ' (1,1,5,2024),(1,3,5,2024),(1,4,4,2024),(2,1,3,2024),(2,2,4,2024),(2,3,NULL,2024),\n'
           ' (3,1,4,2024),(3,4,5,2024),(3,5,3,2024),(4,2,5,2024),(4,3,5,2024),(4,1,4,2024),\n'
           ' (5,1,5,2024),(5,2,4,2024),(5,5,NULL,2024),(6,3,3,2024),(6,4,3,2024),(7,1,4,2024),\n'
           ' (7,2,3,2024),(7,3,5,2024),(8,5,4,2024),(8,4,5,2024),(9,1,5,2024),(9,3,4,2024),\n'
           ' (10,2,NULL,2024),(10,4,4,2024),(1,1,4,2023),(2,1,3,2023),(3,3,5,2023);\n',
  'expected': [[1, 'Н. Крылова', 'Математика'], [2, 'А. Беляев', 'Физика']],
  'expected_cols': ['id', 'name', 'subject'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT id, name, subject FROM teachers ORDER BY id'},
 {'id': 's09-37',
  'mode': 'sql',
  'title': 'Фильмы: жанры',
  'statement': 'База фильмов. Создайте справочник genres(name TEXT PRIMARY KEY) и заполните его различными '
               'жанрами из movies (INSERT … SELECT DISTINCT genre …).',
  'starter': '-- Напишите запрос\n',
  'setup': 'CREATE TABLE directors (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  name TEXT NOT NULL,\n'
           '  country TEXT NOT NULL\n'
           ');\n'
           'CREATE TABLE movies (\n'
           '  id INTEGER PRIMARY KEY,\n'
           '  title TEXT NOT NULL,\n'
           '  year INTEGER NOT NULL,\n'
           '  genre TEXT NOT NULL,\n'
           '  rating REAL,\n'
           '  budget INTEGER,\n'
           '  director_id INTEGER REFERENCES directors(id)\n'
           ');\n'
           'INSERT INTO directors VALUES\n'
           " (1,'Кристофер Нолан','Великобритания'),(2,'Хаяо Миядзаки','Япония'),(3,'Андрей "
           "Звягинцев','Россия'),\n"
           " (4,'Грета Гервиг','США'),(5,'Дени Вильнёв','Канада');\n"
           'INSERT INTO movies VALUES\n'
           " (1,'Начало',2010,'фантастика',8.8,160,1),(2,'Интерстеллар',2014,'фантастика',8.7,165,1),\n"
           " (3,'Тёмный рыцарь',2008,'боевик',9.0,185,1),(4,'Унесённые "
           "призраками',2001,'анимация',8.6,19,2),\n"
           " (5,'Ходячий замок',2004,'анимация',8.2,24,2),(6,'Ветер крепчает',2013,'анимация',7.8,30,2),\n"
           " (7,'Левиафан',2014,'драма',7.6,4,3),(8,'Нелюбовь',2017,'драма',7.7,5,3),\n"
           " (9,'Барби',2023,'комедия',6.9,145,4),(10,'Маленькие женщины',2019,'драма',7.8,40,4),\n"
           " (11,'Дюна',2021,'фантастика',8.0,165,5),(12,'Прибытие',2016,'фантастика',7.9,47,5),\n"
           " (13,'Неизвестный фильм',2022,'драма',NULL,NULL,NULL);\n",
  'expected': [['анимация'], ['боевик'], ['драма'], ['комедия'], ['фантастика']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True,
  'check': 'SELECT name FROM genres ORDER BY name'}]}
