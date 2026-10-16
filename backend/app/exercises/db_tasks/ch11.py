"""Задачи книги «Базы данных»: глава 11."""

TASKS: dict[int, list[dict]] = {11: [{'id': 's11-01',
  'mode': 'sql',
  'title': 'Длина строки',
  'statement': 'Выведите title и length(title) как len для товаров; по id.',
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
  'expected': [['Ноутбук Air 13', 14],
               ['Смартфон S5', 11],
               ['Наушники Beat', 13],
               ['Мышь Click', 10],
               ['Клавиатура Type', 15],
               ['Рюкзак City', 11],
               ['Кофе зерновой', 13],
               ['Чай зелёный', 11],
               ['Шоколад тёмный', 14],
               ['Книга SQL', 9],
               ['Книга Python', 12],
               ['Блокнот A5', 10],
               ['Подарочная карта', 16]],
  'expected_cols': ['title', 'len'],
  'hint': '',
  'ordered': True},
 {'id': 's11-02',
  'mode': 'sql',
  'title': 'Регистр',
  'statement': 'Выведите email клиентов в верхнем (upper) и нижнем (lower) регистре: up и low; только '
               'непустые, по id.',
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
  'expected': [['ANNA@MAIL.RU', 'anna@mail.ru'],
               ['BORIS@GMAIL.COM', 'boris@gmail.com'],
               ['GLEB@YANDEX.RU', 'gleb@yandex.ru'],
               ['DASHA@MAIL.RU', 'dasha@mail.ru'],
               ['EGOR@GMAIL.COM', 'egor@gmail.com'],
               ['ZHANNA@YANDEX.RU', 'zhanna@yandex.ru'],
               ['IGOR@MAIL.RU', 'igor@mail.ru'],
               ['LEV@GMAIL.COM', 'lev@gmail.com'],
               ['MARIA@MAIL.RU', 'maria@mail.ru'],
               ['NIKITA@YANDEX.RU', 'nikita@yandex.ru']],
  'expected_cols': ['up', 'low'],
  'hint': 'upper и lower работают для латиницы.',
  'ordered': True},
 {'id': 's11-03',
  'mode': 'sql',
  'title': 'Подстрока',
  'statement': 'Выведите title и первые 5 символов substr(title, 1, 5) как head для товаров; по id.',
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
  'expected': [['Ноутбук Air 13', 'Ноутб'],
               ['Смартфон S5', 'Смарт'],
               ['Наушники Beat', 'Наушн'],
               ['Мышь Click', 'Мышь '],
               ['Клавиатура Type', 'Клави'],
               ['Рюкзак City', 'Рюкза'],
               ['Кофе зерновой', 'Кофе '],
               ['Чай зелёный', 'Чай з'],
               ['Шоколад тёмный', 'Шокол'],
               ['Книга SQL', 'Книга'],
               ['Книга Python', 'Книга'],
               ['Блокнот A5', 'Блокн'],
               ['Подарочная карта', 'Подар']],
  'expected_cols': ['title', 'head'],
  'hint': 'substr(строка, начало, длина); нумерация с 1.',
  'ordered': True},
 {'id': 's11-04',
  'mode': 'sql',
  'title': 'Подстрока до конца',
  'statement': 'Выведите title и часть названия начиная с 6-го символа: substr(title, 6) как tail; по id.',
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
  'expected': [['Ноутбук Air 13', 'ук Air 13'],
               ['Смартфон S5', 'фон S5'],
               ['Наушники Beat', 'ики Beat'],
               ['Мышь Click', 'Click'],
               ['Клавиатура Type', 'атура Type'],
               ['Рюкзак City', 'к City'],
               ['Кофе зерновой', 'зерновой'],
               ['Чай зелёный', 'елёный'],
               ['Шоколад тёмный', 'ад тёмный'],
               ['Книга SQL', ' SQL'],
               ['Книга Python', ' Python'],
               ['Блокнот A5', 'от A5'],
               ['Подарочная карта', 'очная карта']],
  'expected_cols': ['title', 'tail'],
  'hint': '',
  'ordered': True},
 {'id': 's11-05',
  'mode': 'sql',
  'title': 'Последние символы',
  'statement': 'Выведите последние 2 символа каждого email: substr(email, -2) как tail для клиентов с '
               'почтой; по id.',
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
  'expected': [['ru'], ['om'], ['ru'], ['ru'], ['om'], ['ru'], ['ru'], ['om'], ['ru'], ['ru']],
  'expected_cols': ['tail'],
  'hint': 'Отрицательное начало отсчитывается с конца.',
  'ordered': True},
 {'id': 's11-06',
  'mode': 'sql',
  'title': 'Позиция символа',
  'statement': "Выведите name и позицию первого пробела instr(name, ' ') как pos для клиентов; по id.",
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
  'expected': [['Анна Петрова', 5],
               ['Борис Иванов', 6],
               ['Вера Смирнова', 5],
               ['Глеб Орлов', 5],
               ['Дарья Лебедева', 6],
               ['Егор Козлов', 5],
               ['Жанна Морозова', 6],
               ['Игорь Соколов', 6],
               ['Ксения Волкова', 7],
               ['Лев Новиков', 4],
               ['Мария Фёдорова', 6],
               ['Никита Белов', 7]],
  'expected_cols': ['name', 'pos'],
  'hint': '',
  'ordered': True},
 {'id': 's11-07',
  'mode': 'sql',
  'title': 'Имя клиента',
  'statement': "Выведите имя (до пробела) как first_name: substr(name, 1, instr(name, ' ') - 1); по id.",
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
  'expected': [['Анна'],
               ['Борис'],
               ['Вера'],
               ['Глеб'],
               ['Дарья'],
               ['Егор'],
               ['Жанна'],
               ['Игорь'],
               ['Ксения'],
               ['Лев'],
               ['Мария'],
               ['Никита']],
  'expected_cols': ['first_name'],
  'hint': '',
  'ordered': True},
 {'id': 's11-08',
  'mode': 'sql',
  'title': 'Фамилия клиента',
  'statement': "Выведите фамилию (после пробела) как last_name: substr(name, instr(name, ' ') + 1); по id.",
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
  'expected': [['Петрова'],
               ['Иванов'],
               ['Смирнова'],
               ['Орлов'],
               ['Лебедева'],
               ['Козлов'],
               ['Морозова'],
               ['Соколов'],
               ['Волкова'],
               ['Новиков'],
               ['Фёдорова'],
               ['Белов']],
  'expected_cols': ['last_name'],
  'hint': '',
  'ordered': True},
 {'id': 's11-09',
  'mode': 'sql',
  'title': 'Инициалы',
  'statement': 'Выведите инициалы вида «А.П.» — первая буква имени, точка, первая буква фамилии, точка — как '
               'initials; по id.',
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
  'expected': [['А.П.'],
               ['Б.И.'],
               ['В.С.'],
               ['Г.О.'],
               ['Д.Л.'],
               ['Е.К.'],
               ['Ж.М.'],
               ['И.С.'],
               ['К.В.'],
               ['Л.Н.'],
               ['М.Ф.'],
               ['Н.Б.']],
  'expected_cols': ['initials'],
  'hint': '',
  'ordered': True},
 {'id': 's11-10',
  'mode': 'sql',
  'title': 'Слаг из названия',
  'statement': 'Выведите slug — название товара строчными буквами с дефисами вместо пробелов: '
               "lower(replace(title, ' ', '-')) — для товаров, в названии которых есть «Air» или «Click»; по "
               'id.',
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
  'expected': [['Ноутбук-air-13'], ['Мышь-click']],
  'expected_cols': ['slug'],
  'hint': 'replace(строка, что, на_что)',
  'ordered': True},
 {'id': 's11-11',
  'mode': 'sql',
  'title': 'Обрезка пробелов',
  'statement': "Выведите trim('  ab  ') как a, ltrim('  ab  ') как b, rtrim('  ab  ') как c.",
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
  'expected': [['ab', 'ab  ', '  ab']],
  'expected_cols': ['a', 'b', 'c'],
  'hint': ''},
 {'id': 's11-12',
  'mode': 'sql',
  'title': 'Обрезка символов',
  'statement': "trim(строка, символы) убирает перечисленные символы по краям. Выведите trim('--abc--', '-') "
               "как a и rtrim('xxabcxx', 'x') как b.",
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
  'expected': [['abc', 'xxabc']],
  'expected_cols': ['a', 'b'],
  'hint': ''},
 {'id': 's11-13',
  'mode': 'sql',
  'title': 'Выравнивание',
  'statement': "printf форматирует числа и строки. Выведите printf('%05d', id) как code и printf('%-8s|', "
               'brand) как brand_col для товаров с брендом; по id.',
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
  'expected': [['00001', 'Nova    |'],
               ['00002', 'Nova    |'],
               ['00003', 'Sonic   |'],
               ['00004', 'Sonic   |'],
               ['00005', 'Keyra   |'],
               ['00006', 'Urbo    |'],
               ['00007', 'Bean    |'],
               ['00008', 'Leaf    |'],
               ['00009', 'Cacao   |'],
               ['00010', 'Prime   |'],
               ['00011', 'Prime   |']],
  'expected_cols': ['code', 'brand_col'],
  'hint': '',
  'ordered': True},
 {'id': 's11-14',
  'mode': 'sql',
  'title': 'Склейка concat_ws',
  'statement': "concat_ws(разделитель, a, b, …) склеивает значения и пропускает NULL. Выведите concat_ws(', "
               "', name, city, email) как card для клиентов; по id.",
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
  'expected': [['Анна Петрова, Москва, anna@mail.ru'],
               ['Борис Иванов, Казань, boris@gmail.com'],
               ['Вера Смирнова, Москва'],
               ['Глеб Орлов, Тверь, gleb@yandex.ru'],
               ['Дарья Лебедева, Санкт-Петербург, dasha@mail.ru'],
               ['Егор Козлов, Казань, egor@gmail.com'],
               ['Жанна Морозова, zhanna@yandex.ru'],
               ['Игорь Соколов, Москва, igor@mail.ru'],
               ['Ксения Волкова, Омск'],
               ['Лев Новиков, Санкт-Петербург, lev@gmail.com'],
               ['Мария Фёдорова, Тверь, maria@mail.ru'],
               ['Никита Белов, Москва, nikita@yandex.ru']],
  'expected_cols': ['card'],
  'hint': '',
  'ordered': True},
 {'id': 's11-15',
  'mode': 'sql',
  'title': 'Столбчатая диаграмма',
  'statement': "Нарисуйте столбики из звёздочек: replace(hex(zeroblob(qty)), '00', '*') для позиций заказа 5 "
               'и 10 (order_id IN (5, 10)); столбцы order_id, product_id, bar; по order_id, product_id.',
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
  'expected': [[5, 7, '**'], [5, 8, '***'], [10, 8, '**'], [10, 9, '*****']],
  'expected_cols': ['order_id', 'product_id', 'bar'],
  'hint': 'hex(zeroblob(n)) даёт строку из 2n нулей; пары нулей меняем на звёздочки.',
  'ordered': True},
 {'id': 's11-16',
  'mode': 'sql',
  'title': 'Код символа',
  'statement': "Выведите unicode('A') как code, char(66, 67) как letters.",
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
  'expected': [[65, 'BC']],
  'expected_cols': ['code', 'letters'],
  'hint': ''},
 {'id': 's11-17',
  'mode': 'sql',
  'title': 'Символы и байты',
  'statement': "Для кириллицы символ занимает 2 байта. Выведите length('Анна') как chars и "
               "octet_length('Анна') как bytes.",
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
  'expected': [[4, 8]],
  'expected_cols': ['chars', 'bytes'],
  'hint': ''},
 {'id': 's11-18',
  'mode': 'sql',
  'title': 'Модуль числа',
  'statement': 'Выведите id заказа и abs(total - 10000) как dist (расстояние до 10000); по dist, затем по '
               'id; первые 5.',
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
  'expected': [[16, 900], [8, 1800], [2, 4800], [4, 6100], [20, 6330]],
  'expected_cols': ['id', 'dist'],
  'hint': '',
  'ordered': True},
 {'id': 's11-19',
  'mode': 'sql',
  'title': 'Округление',
  'statement': 'Выведите title и price / 3.0 с округлением до сотых (round(…, 2)) как third для товаров '
               'дешевле 1500; по id.',
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
  'expected': [['Кофе зерновой', 296.67],
               ['Чай зелёный', 140.0],
               ['Шоколад тёмный', 60.0],
               ['Книга SQL', 400.0],
               ['Книга Python', 450.0],
               ['Блокнот A5', 83.33],
               ['Подарочная карта', 333.33]],
  'expected_cols': ['title', 'third'],
  'hint': '',
  'ordered': True},
 {'id': 's11-20',
  'mode': 'sql',
  'title': 'Цена в тысячах',
  'statement': 'Выведите title и цену в тысячах рублей с одним знаком: round(price / 1000.0, 1) как k; по '
               'id.',
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
  'expected': [['Ноутбук Air 13', 78.0],
               ['Смартфон S5', 45.0],
               ['Наушники Beat', 5.2],
               ['Мышь Click', 1.5],
               ['Клавиатура Type', 3.9],
               ['Рюкзак City', 3.2],
               ['Кофе зерновой', 0.9],
               ['Чай зелёный', 0.4],
               ['Шоколад тёмный', 0.2],
               ['Книга SQL', 1.2],
               ['Книга Python', 1.4],
               ['Блокнот A5', 0.3],
               ['Подарочная карта', 1.0]],
  'expected_cols': ['title', 'k'],
  'hint': '',
  'ordered': True},
 {'id': 's11-21',
  'mode': 'sql',
  'title': 'Вниз и вверх',
  'statement': 'Выведите price / 1000.0 как x, floor(price / 1000.0) как fl, ceil(price / 1000.0) как ce для '
               'товаров с id ≤ 3; по id.',
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
  'expected': [[78.0, 78.0, 78.0], [45.0, 45.0, 45.0], [5.2, 5.0, 6.0]],
  'expected_cols': ['x', 'fl', 'ce'],
  'hint': '',
  'ordered': True},
 {'id': 's11-22',
  'mode': 'sql',
  'title': 'Остаток от деления',
  'statement': 'Выведите id и номер «смены» id % 3 как shift для клиентов; по id.',
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
  'expected': [[1, 1],
               [2, 2],
               [3, 0],
               [4, 1],
               [5, 2],
               [6, 0],
               [7, 1],
               [8, 2],
               [9, 0],
               [10, 1],
               [11, 2],
               [12, 0]],
  'expected_cols': ['id', 'shift'],
  'hint': '',
  'ordered': True},
 {'id': 's11-23',
  'mode': 'sql',
  'title': 'Максимум из двух',
  'statement': 'Скалярные max и min принимают несколько значений. Выведите title и max(price, 1000) как '
               'at_least, min(price, 5000) как at_most; по id.',
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
  'expected': [['Ноутбук Air 13', 78000, 5000],
               ['Смартфон S5', 45000, 5000],
               ['Наушники Beat', 5200, 5000],
               ['Мышь Click', 1500, 1500],
               ['Клавиатура Type', 3900, 3900],
               ['Рюкзак City', 3200, 3200],
               ['Кофе зерновой', 1000, 890],
               ['Чай зелёный', 1000, 420],
               ['Шоколад тёмный', 1000, 180],
               ['Книга SQL', 1200, 1200],
               ['Книга Python', 1350, 1350],
               ['Блокнот A5', 1000, 250],
               ['Подарочная карта', 1000, 1000]],
  'expected_cols': ['title', 'at_least', 'at_most'],
  'hint': 'Не путайте с агрегатными MAX/MIN: у скалярных несколько аргументов.',
  'ordered': True},
 {'id': 's11-24',
  'mode': 'sql',
  'title': 'Корень и степень',
  'statement': 'Выведите sqrt(144) как r и power(2, 10) как p.',
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
  'expected': [[12.0, 1024.0]],
  'expected_cols': ['r', 'p'],
  'hint': ''},
 {'id': 's11-25',
  'mode': 'sql',
  'title': 'Знак числа',
  'statement': 'Выведите id заказа и sign(total - 10000) как s (−1, 0 или 1); по id.',
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
  'expected': [[1, 1],
               [2, -1],
               [3, 1],
               [4, -1],
               [5, -1],
               [6, -1],
               [7, 1],
               [8, -1],
               [9, -1],
               [10, -1],
               [11, 1],
               [12, -1],
               [13, 1],
               [14, -1],
               [15, -1],
               [16, -1],
               [17, -1],
               [18, -1],
               [19, -1],
               [20, -1]],
  'expected_cols': ['id', 's'],
  'hint': '',
  'ordered': True},
 {'id': 's11-26',
  'mode': 'sql',
  'title': 'Приведение типов',
  'statement': "Выведите CAST('12abc' AS INTEGER) как a, CAST(7 AS TEXT) || '!' как b, CAST('3.9' AS REAL) "
               'как c.',
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
  'expected': [[12, '7!', 3.9]],
  'expected_cols': ['a', 'b', 'c'],
  'hint': ''},
 {'id': 's11-27',
  'mode': 'sql',
  'title': 'Части даты',
  'statement': "Выведите id заказа, год, месяц и день created как y, m, d через strftime('%Y', …), '%m', "
               "'%d'; по id, первые 4.",
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
  'expected': [[1, '2024', '02', '01'],
               [2, '2024', '03', '15'],
               [3, '2024', '03', '02'],
               [4, '2024', '04', '10']],
  'expected_cols': ['id', 'y', 'm', 'd'],
  'hint': '',
  'ordered': True},
 {'id': 's11-28',
  'mode': 'sql',
  'title': 'Плюс неделя',
  'statement': "Выведите id и дату через 7 дней после created: date(created, '+7 days') как due; по id, "
               'первые 4.',
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
  'expected': [[1, '2024-02-08'], [2, '2024-03-22'], [3, '2024-03-09'], [4, '2024-04-17']],
  'expected_cols': ['id', 'due'],
  'hint': 'date(дата, модификатор) сдвигает дату.',
  'ordered': True},
 {'id': 's11-29',
  'mode': 'sql',
  'title': 'Начало месяца',
  'statement': "Выведите id и начало месяца заказа date(created, 'start of month') как month_start; по id, "
               'первые 4.',
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
  'expected': [[1, '2024-02-01'], [2, '2024-03-01'], [3, '2024-03-01'], [4, '2024-04-01']],
  'expected_cols': ['id', 'month_start'],
  'hint': '',
  'ordered': True},
 {'id': 's11-30',
  'mode': 'sql',
  'title': 'Конец месяца',
  'statement': "Выведите id и последний день месяца заказа: date(created, 'start of month', '+1 month', '-1 "
               "day') как month_end; по id, первые 4.",
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
  'expected': [[1, '2024-02-29'], [2, '2024-03-31'], [3, '2024-03-31'], [4, '2024-04-30']],
  'expected_cols': ['id', 'month_end'],
  'hint': '',
  'ordered': True},
 {'id': 's11-31',
  'mode': 'sql',
  'title': 'Дней между датами',
  'statement': "Выведите id и число дней от created до '2024-08-01': julianday('2024-08-01') - "
               'julianday(created), приведённое к целому (CAST AS INTEGER) как days_ago; по id, первые 5.',
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
  'expected': [[1, 182], [2, 139], [3, 152], [4, 113], [5, 149]],
  'expected_cols': ['id', 'days_ago'],
  'hint': '',
  'ordered': True},
 {'id': 's11-32',
  'mode': 'sql',
  'title': 'Заказы июля',
  'statement': "Выведите id и created заказов июля 2024 с помощью strftime('%Y-%m', created) = '2024-07'; по "
               'id.',
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
  'expected': [[15, '2024-07-01'],
               [16, '2024-07-08'],
               [17, '2024-07-12'],
               [18, '2024-07-20'],
               [19, '2024-07-22'],
               [20, '2024-07-30']],
  'expected_cols': ['id', 'created'],
  'hint': '',
  'ordered': True},
 {'id': 's11-33',
  'mode': 'sql',
  'title': 'День недели',
  'statement': "Выведите id и номер дня недели strftime('%w', created) (0 — воскресенье) как wd для заказов "
               '1–4; по id.',
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
  'expected': [[1, '4'], [2, '5'], [3, '6'], [4, '3']],
  'expected_cols': ['id', 'wd'],
  'hint': '',
  'ordered': True},
 {'id': 's11-34',
  'mode': 'sql',
  'title': 'Квартал',
  'statement': "Выведите id и квартал заказа: (CAST(strftime('%m', created) AS INTEGER) + 2) / 3 как "
               'quarter; по id, первые 6.',
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
  'expected': [[1, 1], [2, 1], [3, 1], [4, 2], [5, 1], [6, 1]],
  'expected_cols': ['id', 'quarter'],
  'hint': '',
  'ordered': True},
 {'id': 's11-35',
  'mode': 'sql',
  'title': 'Дата по-русски',
  'statement': "Выведите id и дату в формате ДД.ММ.ГГГГ: strftime('%d.%m.%Y', created) как d; по id, первые "
               '3.',
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
  'expected': [[1, '01.02.2024'], [2, '15.03.2024'], [3, '02.03.2024']],
  'expected_cols': ['id', 'd'],
  'hint': '',
  'ordered': True},
 {'id': 's11-36',
  'mode': 'sql',
  'title': 'Давность клиента',
  'statement': "Выведите name и сколько целых месяцев прошло от registered до '2024-08-01': (год2−год1)·12 + "
               '(месяц2−месяц1) как months; по id.',
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
  'expected': [['Анна Петрова', 7],
               ['Борис Иванов', 6],
               ['Вера Смирнова', 6],
               ['Глеб Орлов', 5],
               ['Дарья Лебедева', 5],
               ['Егор Козлов', 4],
               ['Жанна Морозова', 4],
               ['Игорь Соколов', 3],
               ['Ксения Волкова', 3],
               ['Лев Новиков', 2],
               ['Мария Фёдорова', 2],
               ['Никита Белов', 1]],
  'expected_cols': ['name', 'months'],
  'hint': '',
  'ordered': True},
 {'id': 's11-37',
  'mode': 'sql',
  'title': 'Дата и время',
  'statement': "Выведите datetime('2024-03-15 10:00', '+1 day', '-2 hours') как dt и time('12:30', '+90 "
               "minutes') как t.",
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
  'expected': [['2024-03-16 08:00:00', '14:00:00']],
  'expected_cols': ['dt', 't'],
  'hint': ''},
 {'id': 's11-38',
  'mode': 'sql',
  'title': 'HR: стаж в годах',
  'statement': "База HR. Выведите name и стаж на '2024-08-01' в целых годах: CAST((julianday('2024-08-01') - "
               'julianday(hired)) / 365.25 AS INTEGER) как years; по id.',
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
  'expected': [['Ольга Громова', 5],
               ['Игорь Беляев', 4],
               ['Мария Орлова', 3],
               ['Пётр Зуев', 0],
               ['Нина Белова', 5],
               ['Олег Савин', 2],
               ['Анна Крылова', 2],
               ['Сергей Ким', 0],
               ['Лидия Фомина', 7],
               ['Роман Дьяков', 1],
               ['Ева Миронова', 2],
               ['Артём Исаев', 0],
               ['Вера Жукова', 0],
               ['Тимур Рахимов', 0],
               ['Юлия Седова', 3]],
  'expected_cols': ['name', 'years'],
  'hint': '',
  'ordered': True},
 {'id': 's11-39',
  'mode': 'sql',
  'title': 'HR: домен почты',
  'statement': "База HR. Выведите name и логин почты (до @) как login: substr(email, 1, instr(email, '@') - "
               '1); по id.',
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
  'expected': [['Ольга Громова', 'olga'],
               ['Игорь Беляев', 'igor.b'],
               ['Мария Орлова', 'maria'],
               ['Пётр Зуев', 'petr'],
               ['Нина Белова', 'nina'],
               ['Олег Савин', 'oleg'],
               ['Анна Крылова', 'anna.k'],
               ['Сергей Ким', 'sergey'],
               ['Лидия Фомина', 'lidia'],
               ['Роман Дьяков', 'roman'],
               ['Ева Миронова', 'eva'],
               ['Артём Исаев', 'artem'],
               ['Вера Жукова', 'vera.z'],
               ['Тимур Рахимов', 'timur'],
               ['Юлия Седова', 'yulia']],
  'expected_cols': ['name', 'login'],
  'hint': '',
  'ordered': True},
 {'id': 's11-40',
  'mode': 'sql',
  'title': 'HR: телефон без пробелов',
  'statement': "База HR. Выведите name и телефон без пробелов и дефисов: replace(replace(phone, ' ', ''), "
               "'-', '') как digits, только для тех, у кого телефон есть; по id.",
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
  'expected': [['Ольга Громова', '+74951111111'],
               ['Игорь Беляев', '+74951111112'],
               ['Пётр Зуев', '+74951111114'],
               ['Нина Белова', '+78432222221'],
               ['Олег Савин', '+78432222222'],
               ['Сергей Ким', '+78432222224'],
               ['Лидия Фомина', '+74953333331'],
               ['Роман Дьяков', '+74953333332'],
               ['Ева Миронова', '+74824444441'],
               ['Вера Жукова', '+74824444443'],
               ['Юлия Седова', '+78432222225']],
  'expected_cols': ['name', 'digits'],
  'hint': '',
  'ordered': True},
 {'id': 's11-41',
  'mode': 'sql',
  'title': 'HR: зарплата в тысячах',
  'statement': 'База HR. Выведите name и salary в тысячах с округлением вниз: salary / 1000 как k; по id.',
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
  'expected': [['Ольга Громова', 320],
               ['Игорь Беляев', 210],
               ['Мария Орлова', 190],
               ['Пётр Зуев', 120],
               ['Нина Белова', 280],
               ['Олег Савин', 150],
               ['Анна Крылова', 150],
               ['Сергей Ким', 95],
               ['Лидия Фомина', 200],
               ['Роман Дьяков', 110],
               ['Ева Миронова', 170],
               ['Артём Исаев', 80],
               ['Вера Жукова', 85],
               ['Тимур Рахимов', 130],
               ['Юлия Седова', 175]],
  'expected_cols': ['name', 'k'],
  'hint': '',
  'ordered': True},
 {'id': 's11-42',
  'mode': 'sql',
  'title': 'Школа: возраст',
  'statement': "Школьная база. Выведите name и возраст на '2024-09-01' в целых годах: "
               "CAST((julianday('2024-09-01') - julianday(birth)) / 365.25 AS INTEGER) как age; по id.",
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
  'expected': [['Алёна Громова', 15],
               ['Богдан Сидоров', 14],
               ['Варвара Кузнецова', 15],
               ['Давид Попов', 16],
               ['Ева Васильева', 15],
               ['Фёдор Михайлов', 16],
               ['Галина Соколова', 17],
               ['Игнат Павлов', 16],
               ['Яна Тихонова', 17],
               ['Тимофей Орлов', 15]],
  'expected_cols': ['name', 'age'],
  'hint': '',
  'ordered': True},
 {'id': 's11-43',
  'mode': 'sql',
  'title': 'Школа: номер класса',
  'statement': 'Школьная база. Выведите name и номер параллели (число в class) как grade: CAST(class AS '
               'INTEGER) — приведение берёт число из начала строки; по id.',
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
  'expected': [['Алёна Громова', 9],
               ['Богдан Сидоров', 9],
               ['Варвара Кузнецова', 9],
               ['Давид Попов', 10],
               ['Ева Васильева', 10],
               ['Фёдор Михайлов', 10],
               ['Галина Соколова', 11],
               ['Игнат Павлов', 11],
               ['Яна Тихонова', 11],
               ['Тимофей Орлов', 9]],
  'expected_cols': ['name', 'grade'],
  'hint': '',
  'ordered': True},
 {'id': 's11-44',
  'mode': 'sql',
  'title': 'Фильмы: десятилетие',
  'statement': 'База фильмов. Выведите title и десятилетие выхода: year / 10 * 10 как decade; по id.',
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
  'expected': [['Начало', 2010],
               ['Интерстеллар', 2010],
               ['Тёмный рыцарь', 2000],
               ['Унесённые призраками', 2000],
               ['Ходячий замок', 2000],
               ['Ветер крепчает', 2010],
               ['Левиафан', 2010],
               ['Нелюбовь', 2010],
               ['Барби', 2020],
               ['Маленькие женщины', 2010],
               ['Дюна', 2020],
               ['Прибытие', 2010],
               ['Неизвестный фильм', 2020]],
  'expected_cols': ['title', 'decade'],
  'hint': '',
  'ordered': True},
 {'id': 's11-45',
  'mode': 'sql',
  'title': 'Фильмы: длинные названия',
  'statement': 'База фильмов. Выведите длину названия фильма length(title) как len для фильмов, у которых '
               'она больше 12; по len, title.',
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
  'expected': [['Тёмный рыцарь', 13],
               ['Ходячий замок', 13],
               ['Ветер крепчает', 14],
               ['Маленькие женщины', 17],
               ['Неизвестный фильм', 17],
               ['Унесённые призраками', 20]],
  'expected_cols': ['title', 'len'],
  'hint': '',
  'ordered': True}]}
