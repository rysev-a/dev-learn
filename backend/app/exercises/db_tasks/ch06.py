"""Задачи книги «Базы данных»: глава 6."""

TASKS: dict[int, list[dict]] = {6: [{'id': 's06-01',
  'mode': 'sql',
  'title': 'Заказ и клиент',
  'statement': 'Выведите id заказа и имя клиента (JOIN customers по customer_id): столбцы order_id, name; по '
               'id заказа.',
  'starter': 'SELECT o.id AS order_id, c.name\nFROM orders o\nJOIN customers c ON ...\nORDER BY o.id;\n',
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
  'expected': [[1, 'Анна Петрова'],
               [2, 'Анна Петрова'],
               [3, 'Борис Иванов'],
               [4, 'Борис Иванов'],
               [5, 'Вера Смирнова'],
               [6, 'Глеб Орлов'],
               [7, 'Дарья Лебедева'],
               [8, 'Дарья Лебедева'],
               [9, 'Дарья Лебедева'],
               [10, 'Егор Козлов'],
               [11, 'Игорь Соколов'],
               [12, 'Игорь Соколов'],
               [13, 'Лев Новиков'],
               [14, 'Лев Новиков'],
               [15, 'Мария Фёдорова'],
               [16, 'Никита Белов'],
               [17, 'Анна Петрова'],
               [18, 'Борис Иванов'],
               [19, 'Вера Смирнова'],
               [20, 'Дарья Лебедева']],
  'expected_cols': ['order_id', 'name'],
  'hint': 'ON c.id = o.customer_id',
  'ordered': True},
 {'id': 's06-02',
  'mode': 'sql',
  'title': 'С суммой',
  'statement': 'Выведите name, id заказа и total для всех заказов (JOIN), по id заказа.',
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
  'expected': [['Анна Петрова', 1, 79500],
               ['Анна Петрова', 2, 5200],
               ['Борис Иванов', 3, 55400],
               ['Борис Иванов', 4, 3900],
               ['Вера Смирнова', 5, 3040],
               ['Глеб Орлов', 6, 2550],
               ['Дарья Лебедева', 7, 45000],
               ['Дарья Лебедева', 8, 8200],
               ['Дарья Лебедева', 9, 2500],
               ['Егор Козлов', 10, 1740],
               ['Игорь Соколов', 11, 78000],
               ['Игорь Соколов', 12, 890],
               ['Лев Новиков', 13, 46500],
               ['Лев Новиков', 14, 2400],
               ['Мария Фёдорова', 15, 3200],
               ['Никита Белов', 16, 9100],
               ['Анна Петрова', 17, 2550],
               ['Борис Иванов', 18, 1800],
               ['Вера Смирнова', 19, 2100],
               ['Дарья Лебедева', 20, 3670]],
  'expected_cols': ['name', 'order_id', 'total'],
  'hint': '',
  'ordered': True},
 {'id': 's06-03',
  'mode': 'sql',
  'title': 'Фильтр после JOIN',
  'statement': "Выведите name клиентов и id их оплаченных заказов (status = 'paid'), по id заказа.",
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
  'expected': [['Борис Иванов', 3],
               ['Дарья Лебедева', 8],
               ['Егор Козлов', 10],
               ['Лев Новиков', 13],
               ['Никита Белов', 16],
               ['Вера Смирнова', 19]],
  'expected_cols': ['name', 'order_id'],
  'hint': '',
  'ordered': True},
 {'id': 's06-04',
  'mode': 'sql',
  'title': 'Позиции и товары',
  'statement': 'Для заказа №1 выведите title и qty каждой позиции (order_items JOIN products), по title.',
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
  'expected': [['Мышь Click', 1], ['Ноутбук Air 13', 1]],
  'expected_cols': ['title', 'qty'],
  'hint': '',
  'ordered': True},
 {'id': 's06-05',
  'mode': 'sql',
  'title': 'Три таблицы',
  'statement': 'Выведите order_id, created и title товара для каждой позиции (order_items, orders, '
               'products), по order_id, затем по title.',
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
  'expected': [[1, '2024-02-01', 'Мышь Click'],
               [1, '2024-02-01', 'Ноутбук Air 13'],
               [2, '2024-03-15', 'Наушники Beat'],
               [3, '2024-03-02', 'Наушники Beat'],
               [3, '2024-03-02', 'Смартфон S5'],
               [4, '2024-04-10', 'Клавиатура Type'],
               [5, '2024-03-05', 'Кофе зерновой'],
               [5, '2024-03-05', 'Чай зелёный'],
               [6, '2024-03-20', 'Книга Python'],
               [6, '2024-03-20', 'Книга SQL'],
               [7, '2024-04-02', 'Смартфон S5'],
               [8, '2024-04-18', 'Мышь Click'],
               [8, '2024-04-18', 'Наушники Beat'],
               [9, '2024-05-07', 'Блокнот A5'],
               [10, '2024-05-01', 'Чай зелёный'],
               [10, '2024-05-01', 'Шоколад тёмный'],
               [11, '2024-05-15', 'Ноутбук Air 13'],
               [12, '2024-06-03', 'Кофе зерновой'],
               [13, '2024-06-10', 'Мышь Click'],
               [13, '2024-06-10', 'Смартфон S5'],
               [14, '2024-06-25', 'Книга SQL'],
               [15, '2024-07-01', 'Рюкзак City'],
               [16, '2024-07-08', 'Клавиатура Type'],
               [16, '2024-07-08', 'Наушники Beat'],
               [17, '2024-07-12', 'Книга Python'],
               [17, '2024-07-12', 'Книга SQL'],
               [18, '2024-07-20', 'Шоколад тёмный'],
               [19, '2024-07-22', 'Чай зелёный'],
               [20, '2024-07-30', 'Блокнот A5'],
               [20, '2024-07-30', 'Кофе зерновой']],
  'expected_cols': ['order_id', 'created', 'title'],
  'hint': '',
  'ordered': True},
 {'id': 's06-06',
  'mode': 'sql',
  'title': 'Четыре таблицы',
  'statement': 'Выведите name клиента, id заказа, title товара и qty для каждой позиции: по заказу, затем по '
               'title.',
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
  'expected': [['Анна Петрова', 1, 'Мышь Click', 1],
               ['Анна Петрова', 1, 'Ноутбук Air 13', 1],
               ['Анна Петрова', 2, 'Наушники Beat', 1],
               ['Борис Иванов', 3, 'Наушники Beat', 2],
               ['Борис Иванов', 3, 'Смартфон S5', 1],
               ['Борис Иванов', 4, 'Клавиатура Type', 1],
               ['Вера Смирнова', 5, 'Кофе зерновой', 2],
               ['Вера Смирнова', 5, 'Чай зелёный', 3],
               ['Глеб Орлов', 6, 'Книга Python', 1],
               ['Глеб Орлов', 6, 'Книга SQL', 1],
               ['Дарья Лебедева', 7, 'Смартфон S5', 1],
               ['Дарья Лебедева', 8, 'Мышь Click', 2],
               ['Дарья Лебедева', 8, 'Наушники Beat', 1],
               ['Дарья Лебедева', 9, 'Блокнот A5', 10],
               ['Егор Козлов', 10, 'Чай зелёный', 2],
               ['Егор Козлов', 10, 'Шоколад тёмный', 5],
               ['Игорь Соколов', 11, 'Ноутбук Air 13', 1],
               ['Игорь Соколов', 12, 'Кофе зерновой', 1],
               ['Лев Новиков', 13, 'Мышь Click', 1],
               ['Лев Новиков', 13, 'Смартфон S5', 1],
               ['Лев Новиков', 14, 'Книга SQL', 2],
               ['Мария Фёдорова', 15, 'Рюкзак City', 1],
               ['Никита Белов', 16, 'Клавиатура Type', 1],
               ['Никита Белов', 16, 'Наушники Beat', 1],
               ['Анна Петрова', 17, 'Книга Python', 1],
               ['Анна Петрова', 17, 'Книга SQL', 1],
               ['Борис Иванов', 18, 'Шоколад тёмный', 10],
               ['Вера Смирнова', 19, 'Чай зелёный', 5],
               ['Дарья Лебедева', 20, 'Блокнот A5', 4],
               ['Дарья Лебедева', 20, 'Кофе зерновой', 3]],
  'expected_cols': ['name', 'order_id', 'title', 'qty'],
  'hint': '',
  'ordered': True},
 {'id': 's06-07',
  'mode': 'sql',
  'title': 'USING',
  'statement': 'В базе есть справочник cities(city, country). Когда столбец называется одинаково в обеих '
               'таблицах, соединение можно записать через USING (city). Выведите name клиента и country; '
               'клиенты без города в результат не попадают. По name.',
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
           'orders.id);\n'
           'CREATE TABLE cities (city TEXT PRIMARY KEY, country TEXT NOT NULL);\n'
           "INSERT INTO cities VALUES ('Москва', 'Россия'), ('Казань', 'Россия'), ('Тверь', 'Россия'), "
           "('Санкт-Петербург', 'Россия'), ('Омск', 'Россия');\n",
  'expected': [['Анна Петрова', 'Россия'],
               ['Борис Иванов', 'Россия'],
               ['Вера Смирнова', 'Россия'],
               ['Глеб Орлов', 'Россия'],
               ['Дарья Лебедева', 'Россия'],
               ['Егор Козлов', 'Россия'],
               ['Игорь Соколов', 'Россия'],
               ['Ксения Волкова', 'Россия'],
               ['Лев Новиков', 'Россия'],
               ['Мария Фёдорова', 'Россия'],
               ['Никита Белов', 'Россия']],
  'expected_cols': ['name', 'country'],
  'hint': 'JOIN cities ct USING (city) вместо ON c.city = ct.city.',
  'ordered': True},
 {'id': 's06-08',
  'mode': 'sql',
  'title': 'Клиенты и заказы (LEFT)',
  'statement': 'Выведите name клиента и id заказа; клиенты без заказов тоже должны быть в результате (LEFT '
               'JOIN, order_id будет NULL). По name, затем по order_id.',
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
  'expected': [['Анна Петрова', 1],
               ['Анна Петрова', 2],
               ['Анна Петрова', 17],
               ['Борис Иванов', 3],
               ['Борис Иванов', 4],
               ['Борис Иванов', 18],
               ['Вера Смирнова', 5],
               ['Вера Смирнова', 19],
               ['Глеб Орлов', 6],
               ['Дарья Лебедева', 7],
               ['Дарья Лебедева', 8],
               ['Дарья Лебедева', 9],
               ['Дарья Лебедева', 20],
               ['Егор Козлов', 10],
               ['Жанна Морозова', None],
               ['Игорь Соколов', 11],
               ['Игорь Соколов', 12],
               ['Ксения Волкова', None],
               ['Лев Новиков', 13],
               ['Лев Новиков', 14],
               ['Мария Фёдорова', 15],
               ['Никита Белов', 16]],
  'expected_cols': ['name', 'order_id'],
  'hint': 'LEFT JOIN сохраняет все строки левой таблицы.',
  'ordered': True},
 {'id': 's06-09',
  'mode': 'sql',
  'title': 'Клиенты без заказов',
  'statement': 'Выведите name клиентов, у которых нет ни одного заказа: LEFT JOIN и условие o.id IS NULL. По '
               'name.',
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
  'expected': [['Жанна Морозова'], ['Ксения Волкова']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's06-10',
  'mode': 'sql',
  'title': 'Непроданные товары',
  'statement': 'Выведите title товаров, которые ни разу не продавались (нет строк в order_items), по title.',
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
  'expected': [['Подарочная карта']],
  'expected_cols': ['title'],
  'hint': '',
  'ordered': True},
 {'id': 's06-11',
  'mode': 'sql',
  'title': 'Сколько без заказов',
  'statement': 'Сколько клиентов не сделали ни одного заказа? Столбец n.',
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
  'expected': [[2]],
  'expected_cols': ['n'],
  'hint': ''},
 {'id': 's06-12',
  'mode': 'sql',
  'title': 'Условие в ON',
  'statement': 'Выведите name клиента и id его оплаченных заказов; клиенты без оплаченных заказов должны '
               "остаться (order_id NULL). Условие status = 'paid' поставьте в ON, не в WHERE. По name, "
               'order_id.',
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
  'expected': [['Анна Петрова', None],
               ['Борис Иванов', 3],
               ['Вера Смирнова', 19],
               ['Глеб Орлов', None],
               ['Дарья Лебедева', 8],
               ['Егор Козлов', 10],
               ['Жанна Морозова', None],
               ['Игорь Соколов', None],
               ['Ксения Волкова', None],
               ['Лев Новиков', 13],
               ['Мария Фёдорова', None],
               ['Никита Белов', 16]],
  'expected_cols': ['name', 'order_id'],
  'hint': 'Условие в WHERE превратило бы LEFT JOIN во внутреннее.',
  'ordered': True},
 {'id': 's06-13',
  'mode': 'sql',
  'title': 'Нет оплаченных',
  'statement': 'Выведите name клиентов, у которых нет ни одного оплаченного заказа; по name.',
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
  'expected': [['Анна Петрова'],
               ['Глеб Орлов'],
               ['Жанна Морозова'],
               ['Игорь Соколов'],
               ['Ксения Волкова'],
               ['Мария Фёдорова']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's06-14',
  'mode': 'sql',
  'title': 'RIGHT JOIN',
  'statement': 'RIGHT JOIN сохраняет строки правой таблицы. Выведите title товара и order_id из order_items '
               'RIGHT JOIN products; непроданные дадут NULL. По title, order_id.',
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
  'expected': [['Блокнот A5', 9],
               ['Блокнот A5', 20],
               ['Клавиатура Type', 4],
               ['Клавиатура Type', 16],
               ['Книга Python', 6],
               ['Книга Python', 17],
               ['Книга SQL', 6],
               ['Книга SQL', 14],
               ['Книга SQL', 17],
               ['Кофе зерновой', 5],
               ['Кофе зерновой', 12],
               ['Кофе зерновой', 20],
               ['Мышь Click', 1],
               ['Мышь Click', 8],
               ['Мышь Click', 13],
               ['Наушники Beat', 2],
               ['Наушники Beat', 3],
               ['Наушники Beat', 8],
               ['Наушники Beat', 16],
               ['Ноутбук Air 13', 1],
               ['Ноутбук Air 13', 11],
               ['Подарочная карта', None],
               ['Рюкзак City', 15],
               ['Смартфон S5', 3],
               ['Смартфон S5', 7],
               ['Смартфон S5', 13],
               ['Чай зелёный', 5],
               ['Чай зелёный', 10],
               ['Чай зелёный', 19],
               ['Шоколад тёмный', 10],
               ['Шоколад тёмный', 18]],
  'expected_cols': ['title', 'order_id'],
  'hint': '',
  'ordered': True},
 {'id': 's06-15',
  'mode': 'sql',
  'title': 'Сотрудники и отделы',
  'statement': 'База HR. Выведите name сотрудника и название отдела (JOIN departments); сотрудники без '
               'отдела не попадут в результат. По id сотрудника.',
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
  'expected': [['Ольга Громова', 'Разработка'],
               ['Игорь Беляев', 'Разработка'],
               ['Мария Орлова', 'Разработка'],
               ['Пётр Зуев', 'Разработка'],
               ['Нина Белова', 'Продажи'],
               ['Олег Савин', 'Продажи'],
               ['Анна Крылова', 'Продажи'],
               ['Сергей Ким', 'Продажи'],
               ['Лидия Фомина', 'Бухгалтерия'],
               ['Роман Дьяков', 'Бухгалтерия'],
               ['Ева Миронова', 'Поддержка'],
               ['Артём Исаев', 'Поддержка'],
               ['Вера Жукова', 'Поддержка'],
               ['Юлия Седова', 'Продажи']],
  'expected_cols': ['name', 'dept'],
  'hint': '',
  'ordered': True},
 {'id': 's06-16',
  'mode': 'sql',
  'title': 'Все сотрудники',
  'statement': 'База HR. Выведите name и название отдела для всех сотрудников, включая без отдела (LEFT '
               'JOIN). По id.',
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
  'expected': [['Ольга Громова', 'Разработка'],
               ['Игорь Беляев', 'Разработка'],
               ['Мария Орлова', 'Разработка'],
               ['Пётр Зуев', 'Разработка'],
               ['Нина Белова', 'Продажи'],
               ['Олег Савин', 'Продажи'],
               ['Анна Крылова', 'Продажи'],
               ['Сергей Ким', 'Продажи'],
               ['Лидия Фомина', 'Бухгалтерия'],
               ['Роман Дьяков', 'Бухгалтерия'],
               ['Ева Миронова', 'Поддержка'],
               ['Артём Исаев', 'Поддержка'],
               ['Вера Жукова', 'Поддержка'],
               ['Тимур Рахимов', None],
               ['Юлия Седова', 'Продажи']],
  'expected_cols': ['name', 'dept'],
  'hint': '',
  'ordered': True},
 {'id': 's06-17',
  'mode': 'sql',
  'title': 'Пустые отделы',
  'statement': 'База HR. Выведите названия отделов, в которых нет сотрудников.',
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
  'expected': [['Исследования']],
  'expected_cols': ['name'],
  'hint': ''},
 {'id': 's06-18',
  'mode': 'sql',
  'title': 'FULL JOIN',
  'statement': 'База HR. FULL OUTER JOIN сохраняет строки обеих таблиц. Выведите e.name и d.name для всех '
               'пар, включая сотрудников без отдела и отделы без сотрудников; по e.name, d.name (NULL идут '
               'первыми).',
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
  'expected': [[None, 'Исследования'],
               ['Анна Крылова', 'Продажи'],
               ['Артём Исаев', 'Поддержка'],
               ['Вера Жукова', 'Поддержка'],
               ['Ева Миронова', 'Поддержка'],
               ['Игорь Беляев', 'Разработка'],
               ['Лидия Фомина', 'Бухгалтерия'],
               ['Мария Орлова', 'Разработка'],
               ['Нина Белова', 'Продажи'],
               ['Олег Савин', 'Продажи'],
               ['Ольга Громова', 'Разработка'],
               ['Пётр Зуев', 'Разработка'],
               ['Роман Дьяков', 'Бухгалтерия'],
               ['Сергей Ким', 'Продажи'],
               ['Тимур Рахимов', None],
               ['Юлия Седова', 'Продажи']],
  'expected_cols': ['employee', 'dept'],
  'hint': '',
  'ordered': True},
 {'id': 's06-19',
  'mode': 'sql',
  'title': 'Сотрудник и начальник',
  'statement': 'База HR. Самосоединение: выведите name сотрудника и name его начальника (boss) для тех, у '
               'кого начальник есть; по id сотрудника.',
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
  'expected': [['Игорь Беляев', 'Ольга Громова'],
               ['Мария Орлова', 'Ольга Громова'],
               ['Пётр Зуев', 'Игорь Беляев'],
               ['Олег Савин', 'Нина Белова'],
               ['Анна Крылова', 'Нина Белова'],
               ['Сергей Ким', 'Нина Белова'],
               ['Роман Дьяков', 'Лидия Фомина'],
               ['Артём Исаев', 'Ева Миронова'],
               ['Вера Жукова', 'Ева Миронова'],
               ['Юлия Седова', 'Нина Белова']],
  'expected_cols': ['employee', 'boss'],
  'hint': 'Одна и та же таблица берётся дважды под разными псевдонимами.',
  'ordered': True},
 {'id': 's06-20',
  'mode': 'sql',
  'title': 'Без начальника тоже',
  'statement': 'База HR. Выведите name сотрудника и начальника; у кого начальника нет — NULL. По id.',
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
  'expected': [['Ольга Громова', None],
               ['Игорь Беляев', 'Ольга Громова'],
               ['Мария Орлова', 'Ольга Громова'],
               ['Пётр Зуев', 'Игорь Беляев'],
               ['Нина Белова', None],
               ['Олег Савин', 'Нина Белова'],
               ['Анна Крылова', 'Нина Белова'],
               ['Сергей Ким', 'Нина Белова'],
               ['Лидия Фомина', None],
               ['Роман Дьяков', 'Лидия Фомина'],
               ['Ева Миронова', None],
               ['Артём Исаев', 'Ева Миронова'],
               ['Вера Жукова', 'Ева Миронова'],
               ['Тимур Рахимов', None],
               ['Юлия Седова', 'Нина Белова']],
  'expected_cols': ['employee', 'boss'],
  'hint': '',
  'ordered': True},
 {'id': 's06-21',
  'mode': 'sql',
  'title': 'Пары с одинаковой зарплатой',
  'statement': 'База HR. Найдите пары сотрудников одного отдела с равной зарплатой: a.name, b.name, a.id < '
               'b.id, чтобы пара не повторялась.',
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
  'expected': [['Олег Савин', 'Анна Крылова']],
  'expected_cols': ['first', 'second'],
  'hint': ''},
 {'id': 's06-22',
  'mode': 'sql',
  'title': 'Подчинённые Нины',
  'statement': 'База HR. Выведите name подчинённых Нины Беловой (boss — по имени), по id.',
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
  'expected': [['Олег Савин'], ['Анна Крылова'], ['Сергей Ким'], ['Юлия Седова']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's06-23',
  'mode': 'sql',
  'title': 'CROSS JOIN',
  'statement': 'Сколько строк даёт перекрёстное соединение customers CROSS JOIN products? Столбец n.',
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
  'expected': [[156]],
  'expected_cols': ['n'],
  'hint': 'Каждая строка слева с каждой строкой справа: 12 × 13.'},
 {'id': 's06-24',
  'mode': 'sql',
  'title': 'Все сочетания',
  'statement': 'Выведите все сочетания «категория товара» и «статус заказа» без повторов: DISTINCT '
               'p.category, o.status из products p CROSS JOIN orders o; по category, status.',
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
  'expected': [['Аксессуары', 'cancelled'],
               ['Аксессуары', 'new'],
               ['Аксессуары', 'paid'],
               ['Аксессуары', 'shipped'],
               ['Канцелярия', 'cancelled'],
               ['Канцелярия', 'new'],
               ['Канцелярия', 'paid'],
               ['Канцелярия', 'shipped'],
               ['Книги', 'cancelled'],
               ['Книги', 'new'],
               ['Книги', 'paid'],
               ['Книги', 'shipped'],
               ['Продукты', 'cancelled'],
               ['Продукты', 'new'],
               ['Продукты', 'paid'],
               ['Продукты', 'shipped'],
               ['Прочее', 'cancelled'],
               ['Прочее', 'new'],
               ['Прочее', 'paid'],
               ['Прочее', 'shipped'],
               ['Электроника', 'cancelled'],
               ['Электроника', 'new'],
               ['Электроника', 'paid'],
               ['Электроника', 'shipped']],
  'expected_cols': ['category', 'status'],
  'hint': '',
  'ordered': True},
 {'id': 's06-25',
  'mode': 'sql',
  'title': 'Размножение строк',
  'statement': 'Сколько строк в результате orders JOIN order_items? Столбец n. Соединение размножает строки: '
               'на каждый заказ приходится по строке на позицию.',
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
  'expected': [[30]],
  'expected_cols': ['n'],
  'hint': ''},
 {'id': 's06-26',
  'mode': 'sql',
  'title': 'Покупали электронику',
  'statement': "Выведите без повторов name клиентов, купивших хотя бы один товар категории 'Электроника'; по "
               'name.',
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
  'expected': [['Анна Петрова'],
               ['Борис Иванов'],
               ['Дарья Лебедева'],
               ['Игорь Соколов'],
               ['Лев Новиков'],
               ['Никита Белов']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's06-27',
  'mode': 'sql',
  'title': 'Покупали книгу SQL',
  'statement': "Выведите name клиентов, купивших 'Книга SQL'; по name без повторов.",
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
  'expected': [['Анна Петрова'], ['Глеб Орлов'], ['Лев Новиков']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's06-28',
  'mode': 'sql',
  'title': 'Сумма строк',
  'statement': 'Выведите order_id, title и стоимость позиции qty * price как line_total для заказа №5; по '
               'title.',
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
  'expected': [[5, 'Кофе зерновой', 1780], [5, 'Чай зелёный', 1260]],
  'expected_cols': ['order_id', 'title', 'line_total'],
  'hint': '',
  'ordered': True},
 {'id': 's06-29',
  'mode': 'sql',
  'title': 'Топ-3 заказа с клиентом',
  'statement': 'Выведите name и total трёх самых крупных заказов (суммы различны).',
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
  'expected': [['Анна Петрова', 79500], ['Игорь Соколов', 78000], ['Борис Иванов', 55400]],
  'expected_cols': ['name', 'total'],
  'hint': '',
  'ordered': True},
 {'id': 's06-30',
  'mode': 'sql',
  'title': 'Выручка москвичей',
  'statement': 'Какова сумма всех заказов клиентов из Москвы? Столбец revenue.',
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
  'expected': [[180380]],
  'expected_cols': ['revenue'],
  'hint': ''},
 {'id': 's06-31',
  'mode': 'sql',
  'title': 'Соединение по неравенству',
  'statement': 'Таблица tiers задаёт уровни цен (low–high). Выведите title и название уровня (tiers.name) '
               'для каждого товара; соединение по p.price BETWEEN t.low AND t.high. По id товара.',
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
           'orders.id);\n'
           'CREATE TABLE tiers (name TEXT PRIMARY KEY, low INTEGER NOT NULL, high INTEGER NOT NULL);\n'
           "INSERT INTO tiers VALUES ('бюджет', 0, 999), ('средний', 1000, 9999), ('премиум', 10000, "
           '999999);\n',
  'expected': [['Ноутбук Air 13', 'премиум'],
               ['Смартфон S5', 'премиум'],
               ['Наушники Beat', 'средний'],
               ['Мышь Click', 'средний'],
               ['Клавиатура Type', 'средний'],
               ['Рюкзак City', 'средний'],
               ['Кофе зерновой', 'бюджет'],
               ['Чай зелёный', 'бюджет'],
               ['Шоколад тёмный', 'бюджет'],
               ['Книга SQL', 'средний'],
               ['Книга Python', 'средний'],
               ['Блокнот A5', 'бюджет'],
               ['Подарочная карта', 'средний']],
  'expected_cols': ['title', 'tier'],
  'hint': '',
  'ordered': True},
 {'id': 's06-32',
  'mode': 'sql',
  'title': 'Товары премиум-уровня',
  'statement': "Выведите title товаров, попадающих в уровень 'премиум' по таблице tiers; по title.",
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
           'orders.id);\n'
           'CREATE TABLE tiers (name TEXT PRIMARY KEY, low INTEGER NOT NULL, high INTEGER NOT NULL);\n'
           "INSERT INTO tiers VALUES ('бюджет', 0, 999), ('средний', 1000, 9999), ('премиум', 10000, "
           '999999);\n',
  'expected': [['Ноутбук Air 13'], ['Смартфон S5']],
  'expected_cols': ['title'],
  'hint': '',
  'ordered': True},
 {'id': 's06-33',
  'mode': 'sql',
  'title': 'Ученики и курсы',
  'statement': 'Школьная база. Выведите name ученика, title курса и score за 2024 год; по name, title.',
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
  'expected': [['Алёна Громова', 'Информатика', 5],
               ['Алёна Громова', 'Литература', 4],
               ['Алёна Громова', 'Математика', 5],
               ['Богдан Сидоров', 'Информатика', None],
               ['Богдан Сидоров', 'Математика', 3],
               ['Богдан Сидоров', 'Физика', 4],
               ['Варвара Кузнецова', 'История', 3],
               ['Варвара Кузнецова', 'Литература', 5],
               ['Варвара Кузнецова', 'Математика', 4],
               ['Галина Соколова', 'Информатика', 5],
               ['Галина Соколова', 'Математика', 4],
               ['Галина Соколова', 'Физика', 3],
               ['Давид Попов', 'Информатика', 5],
               ['Давид Попов', 'Математика', 4],
               ['Давид Попов', 'Физика', 5],
               ['Ева Васильева', 'История', None],
               ['Ева Васильева', 'Математика', 5],
               ['Ева Васильева', 'Физика', 4],
               ['Игнат Павлов', 'История', 4],
               ['Игнат Павлов', 'Литература', 5],
               ['Тимофей Орлов', 'Литература', 4],
               ['Тимофей Орлов', 'Физика', None],
               ['Фёдор Михайлов', 'Информатика', 3],
               ['Фёдор Михайлов', 'Литература', 3],
               ['Яна Тихонова', 'Информатика', 4],
               ['Яна Тихонова', 'Математика', 5]],
  'expected_cols': ['name', 'title', 'score'],
  'hint': '',
  'ordered': True},
 {'id': 's06-34',
  'mode': 'sql',
  'title': 'Пятёрки по математике',
  'statement': "Школьная база. Выведите name учеников, получивших 5 по курсу 'Математика' (год любой); по "
               'name без повторов.',
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
  'expected': [['Алёна Громова'], ['Ева Васильева'], ['Яна Тихонова']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's06-35',
  'mode': 'sql',
  'title': 'Курсы без записей',
  'statement': 'Школьная база. Выведите title курсов, на которые никто не записан (нет строк в enrollments).',
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
  'expected': [['Химия']],
  'expected_cols': ['title'],
  'hint': ''},
 {'id': 's06-36',
  'mode': 'sql',
  'title': 'Фильм и режиссёр',
  'statement': 'База фильмов. Выведите title фильма и name режиссёра; фильмы без режиссёра не показывайте; '
               'по title.',
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
  'expected': [['Барби', 'Грета Гервиг'],
               ['Ветер крепчает', 'Хаяо Миядзаки'],
               ['Дюна', 'Дени Вильнёв'],
               ['Интерстеллар', 'Кристофер Нолан'],
               ['Левиафан', 'Андрей Звягинцев'],
               ['Маленькие женщины', 'Грета Гервиг'],
               ['Начало', 'Кристофер Нолан'],
               ['Нелюбовь', 'Андрей Звягинцев'],
               ['Прибытие', 'Дени Вильнёв'],
               ['Тёмный рыцарь', 'Кристофер Нолан'],
               ['Унесённые призраками', 'Хаяо Миядзаки'],
               ['Ходячий замок', 'Хаяо Миядзаки']],
  'expected_cols': ['title', 'director'],
  'hint': '',
  'ordered': True},
 {'id': 's06-37',
  'mode': 'sql',
  'title': 'Фильм без режиссёра',
  'statement': 'База фильмов. Выведите title и name режиссёра для всех фильмов (LEFT JOIN); у кого режиссёра '
               'нет — NULL; по title.',
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
  'expected': [['Барби', 'Грета Гервиг'],
               ['Ветер крепчает', 'Хаяо Миядзаки'],
               ['Дюна', 'Дени Вильнёв'],
               ['Интерстеллар', 'Кристофер Нолан'],
               ['Левиафан', 'Андрей Звягинцев'],
               ['Маленькие женщины', 'Грета Гервиг'],
               ['Начало', 'Кристофер Нолан'],
               ['Неизвестный фильм', None],
               ['Нелюбовь', 'Андрей Звягинцев'],
               ['Прибытие', 'Дени Вильнёв'],
               ['Тёмный рыцарь', 'Кристофер Нолан'],
               ['Унесённые призраками', 'Хаяо Миядзаки'],
               ['Ходячий замок', 'Хаяо Миядзаки']],
  'expected_cols': ['title', 'director'],
  'hint': '',
  'ordered': True},
 {'id': 's06-38',
  'mode': 'sql',
  'title': 'Режиссёры из США и Японии',
  'statement': 'База фильмов. Выведите title фильмов режиссёров из Японии или США; по title.',
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
  'expected': [['Барби'],
               ['Ветер крепчает'],
               ['Маленькие женщины'],
               ['Унесённые призраками'],
               ['Ходячий замок']],
  'expected_cols': ['title'],
  'hint': '',
  'ordered': True}]}
