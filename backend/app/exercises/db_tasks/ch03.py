"""Задачи книги «Базы данных»: глава 3."""

TASKS: dict[int, list[dict]] = {3: [{'id': 's03-01',
  'mode': 'sql',
  'title': 'Сортировка по возрастанию',
  'statement': 'Выведите title и price товаров от дешёвых к дорогим (ORDER BY price).',
  'starter': 'SELECT title, price\nFROM products\nORDER BY ...;\n',
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
  'expected': [['Шоколад тёмный', 180],
               ['Блокнот A5', 250],
               ['Чай зелёный', 420],
               ['Кофе зерновой', 890],
               ['Подарочная карта', 1000],
               ['Книга SQL', 1200],
               ['Книга Python', 1350],
               ['Мышь Click', 1500],
               ['Рюкзак City', 3200],
               ['Клавиатура Type', 3900],
               ['Наушники Beat', 5200],
               ['Смартфон S5', 45000],
               ['Ноутбук Air 13', 78000]],
  'expected_cols': ['title', 'price'],
  'hint': 'ORDER BY price сортирует по возрастанию.',
  'ordered': True},
 {'id': 's03-02',
  'mode': 'sql',
  'title': 'Сортировка по убыванию',
  'statement': 'Выведите title и price товаров от дорогих к дешёвым (DESC). Цены у товаров разные.',
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
  'expected': [['Ноутбук Air 13', 78000],
               ['Смартфон S5', 45000],
               ['Наушники Beat', 5200],
               ['Клавиатура Type', 3900],
               ['Рюкзак City', 3200],
               ['Мышь Click', 1500],
               ['Книга Python', 1350],
               ['Книга SQL', 1200],
               ['Подарочная карта', 1000],
               ['Кофе зерновой', 890],
               ['Чай зелёный', 420],
               ['Блокнот A5', 250],
               ['Шоколад тёмный', 180]],
  'expected_cols': ['title', 'price'],
  'hint': 'ORDER BY price DESC',
  'ordered': True},
 {'id': 's03-03',
  'mode': 'sql',
  'title': 'Сортировка текста',
  'statement': 'Выведите name клиентов в алфавитном порядке.',
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
               ['Вера Смирнова'],
               ['Глеб Орлов'],
               ['Дарья Лебедева'],
               ['Егор Козлов'],
               ['Жанна Морозова'],
               ['Игорь Соколов'],
               ['Ксения Волкова'],
               ['Лев Новиков'],
               ['Мария Фёдорова'],
               ['Никита Белов']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's03-04',
  'mode': 'sql',
  'title': 'Обратный алфавит',
  'statement': 'Выведите name клиентов в обратном алфавитном порядке.',
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
  'expected': [['Никита Белов'],
               ['Мария Фёдорова'],
               ['Лев Новиков'],
               ['Ксения Волкова'],
               ['Игорь Соколов'],
               ['Жанна Морозова'],
               ['Егор Козлов'],
               ['Дарья Лебедева'],
               ['Глеб Орлов'],
               ['Вера Смирнова'],
               ['Борис Иванов'],
               ['Анна Петрова']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's03-05',
  'mode': 'sql',
  'title': 'Сортировка по дате',
  'statement': 'Выведите id и created заказов от самых новых к самым старым.',
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
  'expected': [[20, '2024-07-30'],
               [19, '2024-07-22'],
               [18, '2024-07-20'],
               [17, '2024-07-12'],
               [16, '2024-07-08'],
               [15, '2024-07-01'],
               [14, '2024-06-25'],
               [13, '2024-06-10'],
               [12, '2024-06-03'],
               [11, '2024-05-15'],
               [9, '2024-05-07'],
               [10, '2024-05-01'],
               [8, '2024-04-18'],
               [4, '2024-04-10'],
               [7, '2024-04-02'],
               [6, '2024-03-20'],
               [2, '2024-03-15'],
               [5, '2024-03-05'],
               [3, '2024-03-02'],
               [1, '2024-02-01']],
  'expected_cols': ['id', 'created'],
  'hint': 'Даты в формате ГГГГ-ММ-ДД сортируются как строки правильно. Для одинаковых дат добавьте id DESC.',
  'ordered': True},
 {'id': 's03-06',
  'mode': 'sql',
  'title': 'Сортировка по двум столбцам',
  'statement': 'Выведите city и name клиентов: сначала по городу, внутри города — по имени (ORDER BY city, '
               'name).',
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
  'expected': [[None, 'Жанна Морозова'],
               ['Казань', 'Борис Иванов'],
               ['Казань', 'Егор Козлов'],
               ['Москва', 'Анна Петрова'],
               ['Москва', 'Вера Смирнова'],
               ['Москва', 'Игорь Соколов'],
               ['Москва', 'Никита Белов'],
               ['Омск', 'Ксения Волкова'],
               ['Санкт-Петербург', 'Дарья Лебедева'],
               ['Санкт-Петербург', 'Лев Новиков'],
               ['Тверь', 'Глеб Орлов'],
               ['Тверь', 'Мария Фёдорова']],
  'expected_cols': ['city', 'name'],
  'hint': 'Второй столбец работает при равенстве первого.',
  'ordered': True},
 {'id': 's03-07',
  'mode': 'sql',
  'title': 'Разные направления',
  'statement': 'Выведите category, title, price: категории по алфавиту, внутри категории — дорогие первыми.',
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
  'expected': [['Аксессуары', 'Клавиатура Type', 3900],
               ['Аксессуары', 'Рюкзак City', 3200],
               ['Аксессуары', 'Мышь Click', 1500],
               ['Канцелярия', 'Блокнот A5', 250],
               ['Книги', 'Книга Python', 1350],
               ['Книги', 'Книга SQL', 1200],
               ['Продукты', 'Кофе зерновой', 890],
               ['Продукты', 'Чай зелёный', 420],
               ['Продукты', 'Шоколад тёмный', 180],
               ['Прочее', 'Подарочная карта', 1000],
               ['Электроника', 'Ноутбук Air 13', 78000],
               ['Электроника', 'Смартфон S5', 45000],
               ['Электроника', 'Наушники Beat', 5200]],
  'expected_cols': ['category', 'title', 'price'],
  'hint': 'ORDER BY category, price DESC — направление задаётся для каждого столбца.',
  'ordered': True},
 {'id': 's03-08',
  'mode': 'sql',
  'title': 'По выражению',
  'statement': 'Выведите title и стоимость остатка (price * stock) как stock_value; самые дорогие остатки '
               'первыми.',
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
  'expected': [['Подарочная карта', 999000],
               ['Смартфон S5', 540000],
               ['Ноутбук Air 13', 390000],
               ['Наушники Beat', 208000],
               ['Кофе зерновой', 133500],
               ['Блокнот A5', 125000],
               ['Мышь Click', 120000],
               ['Клавиатура Type', 97500],
               ['Чай зелёный', 84000],
               ['Шоколад тёмный', 54000],
               ['Книга SQL', 36000],
               ['Книга Python', 24300],
               ['Рюкзак City', 0]],
  'expected_cols': ['title', 'stock_value'],
  'hint': 'Можно сортировать по псевдониму.',
  'ordered': True},
 {'id': 's03-09',
  'mode': 'sql',
  'title': 'По номеру столбца',
  'statement': 'Выведите title, price, отсортировав по второму столбцу списка (ORDER BY 2) по убыванию; цены '
               'различны.',
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
  'expected': [['Ноутбук Air 13', 78000],
               ['Смартфон S5', 45000],
               ['Наушники Beat', 5200],
               ['Клавиатура Type', 3900],
               ['Рюкзак City', 3200],
               ['Мышь Click', 1500],
               ['Книга Python', 1350],
               ['Книга SQL', 1200],
               ['Подарочная карта', 1000],
               ['Кофе зерновой', 890],
               ['Чай зелёный', 420],
               ['Блокнот A5', 250],
               ['Шоколад тёмный', 180]],
  'expected_cols': ['title', 'price'],
  'hint': 'ORDER BY 2 — по второму столбцу результата.',
  'ordered': True},
 {'id': 's03-10',
  'mode': 'sql',
  'title': 'Сортировка не по выводимому',
  'statement': 'Выведите только title товаров, отсортировав их по цене (price) по возрастанию. Сортировать '
               'можно по столбцу, которого нет в результате.',
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
  'expected': [['Шоколад тёмный'],
               ['Блокнот A5'],
               ['Чай зелёный'],
               ['Кофе зерновой'],
               ['Подарочная карта'],
               ['Книга SQL'],
               ['Книга Python'],
               ['Мышь Click'],
               ['Рюкзак City'],
               ['Клавиатура Type'],
               ['Наушники Beat'],
               ['Смартфон S5'],
               ['Ноутбук Air 13']],
  'expected_cols': ['title'],
  'hint': '',
  'ordered': True},
 {'id': 's03-11',
  'mode': 'sql',
  'title': 'NULL при сортировке',
  'statement': 'Выведите name и city клиентов, отсортировав по city по возрастанию, затем по name. В SQLite '
               'NULL считается самым малым значением и идёт первым.',
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
  'expected': [['Жанна Морозова', None],
               ['Борис Иванов', 'Казань'],
               ['Егор Козлов', 'Казань'],
               ['Анна Петрова', 'Москва'],
               ['Вера Смирнова', 'Москва'],
               ['Игорь Соколов', 'Москва'],
               ['Никита Белов', 'Москва'],
               ['Ксения Волкова', 'Омск'],
               ['Дарья Лебедева', 'Санкт-Петербург'],
               ['Лев Новиков', 'Санкт-Петербург'],
               ['Глеб Орлов', 'Тверь'],
               ['Мария Фёдорова', 'Тверь']],
  'expected_cols': ['name', 'city'],
  'hint': '',
  'ordered': True},
 {'id': 's03-12',
  'mode': 'sql',
  'title': 'NULL в конце',
  'statement': 'Выведите name и city клиентов по city, но NULL-города — в конце: сначала ORDER BY city IS '
               'NULL, затем city, name.',
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
  'expected': [['Борис Иванов', 'Казань'],
               ['Егор Козлов', 'Казань'],
               ['Анна Петрова', 'Москва'],
               ['Вера Смирнова', 'Москва'],
               ['Игорь Соколов', 'Москва'],
               ['Никита Белов', 'Москва'],
               ['Ксения Волкова', 'Омск'],
               ['Дарья Лебедева', 'Санкт-Петербург'],
               ['Лев Новиков', 'Санкт-Петербург'],
               ['Глеб Орлов', 'Тверь'],
               ['Мария Фёдорова', 'Тверь'],
               ['Жанна Морозова', None]],
  'expected_cols': ['name', 'city'],
  'hint': 'city IS NULL равно 0 для заполненных и 1 для пустых.',
  'ordered': True},
 {'id': 's03-13',
  'mode': 'sql',
  'title': 'Фильтр и сортировка',
  'statement': 'Выведите title и price товаров дешевле 5000, самые дорогие первыми (сначала WHERE, потом '
               'ORDER BY).',
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
  'expected': [['Клавиатура Type', 3900],
               ['Рюкзак City', 3200],
               ['Мышь Click', 1500],
               ['Книга Python', 1350],
               ['Книга SQL', 1200],
               ['Подарочная карта', 1000],
               ['Кофе зерновой', 890],
               ['Чай зелёный', 420],
               ['Блокнот A5', 250],
               ['Шоколад тёмный', 180]],
  'expected_cols': ['title', 'price'],
  'hint': 'Порядок слов: SELECT … FROM … WHERE … ORDER BY …',
  'ordered': True},
 {'id': 's03-14',
  'mode': 'sql',
  'title': 'Первые три',
  'statement': 'Выведите три самых дорогих товара: title и price (ORDER BY price DESC LIMIT 3).',
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
  'hint': 'LIMIT ограничивает число строк.',
  'ordered': True},
 {'id': 's03-15',
  'mode': 'sql',
  'title': 'Самый дешёвый',
  'statement': 'Выведите самый дешёвый товар (title, price).',
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
  'expected': [['Шоколад тёмный', 180]],
  'expected_cols': ['title', 'price'],
  'hint': '',
  'ordered': True},
 {'id': 's03-16',
  'mode': 'sql',
  'title': 'Самый новый заказ',
  'statement': 'Выведите id и created самого свежего заказа (при равных датах — с большим id).',
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
  'expected': [[20, '2024-07-30']],
  'expected_cols': ['id', 'created'],
  'hint': '',
  'ordered': True},
 {'id': 's03-17',
  'mode': 'sql',
  'title': 'Самый ранний клиент',
  'statement': 'Выведите name и registered самого раннего клиента по дате регистрации.',
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
  'expected': [['Анна Петрова', '2024-01-15']],
  'expected_cols': ['name', 'registered'],
  'hint': '',
  'ordered': True},
 {'id': 's03-18',
  'mode': 'sql',
  'title': 'Пять крупнейших заказов',
  'statement': 'Выведите id и total пяти самых крупных заказов (суммы различны).',
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
  'expected': [[1, 79500], [11, 78000], [3, 55400], [13, 46500], [7, 45000]],
  'expected_cols': ['id', 'total'],
  'hint': '',
  'ordered': True},
 {'id': 's03-19',
  'mode': 'sql',
  'title': 'Пропустить строки',
  'statement': 'OFFSET пропускает строки. Выведите id, name клиентов по возрастанию id, пропустив первых '
               'трёх и взяв следующих четырёх.',
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
  'expected': [[4, 'Глеб Орлов'], [5, 'Дарья Лебедева'], [6, 'Егор Козлов'], [7, 'Жанна Морозова']],
  'expected_cols': ['id', 'name'],
  'hint': 'LIMIT 4 OFFSET 3',
  'ordered': True},
 {'id': 's03-20',
  'mode': 'sql',
  'title': 'Страница 1',
  'statement': 'Постраничный вывод по 5 товаров, отсортированных по id. Выведите страницу 1: id и title.',
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
  'expected': [[1, 'Ноутбук Air 13'],
               [2, 'Смартфон S5'],
               [3, 'Наушники Beat'],
               [4, 'Мышь Click'],
               [5, 'Клавиатура Type']],
  'expected_cols': ['id', 'title'],
  'hint': '',
  'ordered': True},
 {'id': 's03-21',
  'mode': 'sql',
  'title': 'Страница 2',
  'statement': 'Выведите страницу 2 (по 5 товаров, сортировка по id): id и title.',
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
  'expected': [[6, 'Рюкзак City'],
               [7, 'Кофе зерновой'],
               [8, 'Чай зелёный'],
               [9, 'Шоколад тёмный'],
               [10, 'Книга SQL']],
  'expected_cols': ['id', 'title'],
  'hint': 'OFFSET = (номер страницы − 1) × размер страницы.',
  'ordered': True},
 {'id': 's03-22',
  'mode': 'sql',
  'title': 'Страница 3',
  'statement': 'Выведите страницу 3 (по 5 товаров, сортировка по id): id и title. Страница неполная.',
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
  'expected': [[11, 'Книга Python'], [12, 'Блокнот A5'], [13, 'Подарочная карта']],
  'expected_cols': ['id', 'title'],
  'hint': '',
  'ordered': True},
 {'id': 's03-23',
  'mode': 'sql',
  'title': 'Второй по цене',
  'statement': 'Выведите второй по цене товар (title, price): ORDER BY price DESC, пропустить одну строку, '
               'взять одну.',
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
  'expected': [['Смартфон S5', 45000]],
  'expected_cols': ['title', 'price'],
  'hint': '',
  'ordered': True},
 {'id': 's03-24',
  'mode': 'sql',
  'title': 'Три самых дешёвых в категории',
  'statement': "Выведите title, price трёх самых дешёвых товаров категории 'Продукты' (по возрастанию цены).",
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
  'expected': [['Шоколад тёмный', 180], ['Чай зелёный', 420], ['Кофе зерновой', 890]],
  'expected_cols': ['title', 'price'],
  'hint': '',
  'ordered': True},
 {'id': 's03-25',
  'mode': 'sql',
  'title': 'Последние регистрации',
  'statement': 'Выведите name и registered трёх клиентов, зарегистрировавшихся последними (новые первыми).',
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
  'expected': [['Никита Белов', '2024-07-04'],
               ['Мария Фёдорова', '2024-06-21'],
               ['Лев Новиков', '2024-06-07']],
  'expected_cols': ['name', 'registered'],
  'hint': '',
  'ordered': True},
 {'id': 's03-26',
  'mode': 'sql',
  'title': 'Различные и по порядку',
  'statement': 'Выведите различные категории товаров по алфавиту (DISTINCT и ORDER BY вместе).',
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
  'expected': [['Аксессуары'], ['Канцелярия'], ['Книги'], ['Продукты'], ['Прочее'], ['Электроника']],
  'expected_cols': ['category'],
  'hint': '',
  'ordered': True},
 {'id': 's03-27',
  'mode': 'sql',
  'title': 'Города по убыванию',
  'statement': 'Выведите различные непустые города клиентов в обратном алфавитном порядке.',
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
  'expected': [['Тверь'], ['Санкт-Петербург'], ['Омск'], ['Москва'], ['Казань']],
  'expected_cols': ['city'],
  'hint': 'IS NOT NULL отсекает пропущенные значения.',
  'ordered': True},
 {'id': 's03-28',
  'mode': 'sql',
  'title': 'Склад: меньше всего',
  'statement': 'Выведите title и stock пяти товаров с наименьшим остатком; при равенстве — по title.',
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
  'expected': [['Рюкзак City', 0],
               ['Ноутбук Air 13', 5],
               ['Смартфон S5', 12],
               ['Книга Python', 18],
               ['Клавиатура Type', 25]],
  'expected_cols': ['title', 'stock'],
  'hint': '',
  'ordered': True},
 {'id': 's03-29',
  'mode': 'sql',
  'title': 'Две ключевые сортировки',
  'statement': 'Выведите status и total заказов: по статусу по алфавиту, внутри статуса — крупные заказы '
               'первыми; id в конце для стабильности.',
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
  'expected': [['cancelled', 3900, 4],
               ['cancelled', 3200, 15],
               ['new', 78000, 11],
               ['new', 3670, 20],
               ['new', 2550, 6],
               ['new', 2550, 17],
               ['paid', 55400, 3],
               ['paid', 46500, 13],
               ['paid', 9100, 16],
               ['paid', 8200, 8],
               ['paid', 2100, 19],
               ['paid', 1740, 10],
               ['shipped', 79500, 1],
               ['shipped', 45000, 7],
               ['shipped', 5200, 2],
               ['shipped', 3040, 5],
               ['shipped', 2500, 9],
               ['shipped', 2400, 14],
               ['shipped', 1800, 18],
               ['shipped', 890, 12]],
  'expected_cols': ['status', 'total', 'id'],
  'hint': 'Третий ключ id делает порядок однозначным.',
  'ordered': True},
 {'id': 's03-30',
  'mode': 'sql',
  'title': 'Топ по длине названия',
  'statement': 'Выведите title и length(title) как len для трёх самых длинных названий товаров (по убыванию '
               'длины, затем по title).',
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
  'expected': [['Подарочная карта', 16], ['Клавиатура Type', 15], ['Ноутбук Air 13', 14]],
  'expected_cols': ['title', 'len'],
  'hint': 'length(строка) — число символов.',
  'ordered': True},
 {'id': 's03-31',
  'mode': 'sql',
  'title': 'Позиции заказов',
  'statement': 'Таблица order_items. Выведите order_id, product_id, qty, price по убыванию qty, затем по '
               'order_id, product_id; первые 5 строк.',
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
  'expected': [[9, 12, 10, 250], [18, 9, 10, 180], [10, 9, 5, 180], [19, 8, 5, 420], [20, 12, 4, 250]],
  'expected_cols': ['order_id', 'product_id', 'qty', 'price'],
  'hint': '',
  'ordered': True},
 {'id': 's03-32',
  'mode': 'sql',
  'title': 'Зарплаты по убыванию',
  'statement': 'База HR. Выведите name и salary пяти самых высокооплачиваемых сотрудников (зарплаты разные).',
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
  'expected': [['Ольга Громова', 320000],
               ['Нина Белова', 280000],
               ['Игорь Беляев', 210000],
               ['Лидия Фомина', 200000],
               ['Мария Орлова', 190000]],
  'expected_cols': ['name', 'salary'],
  'hint': '',
  'ordered': True},
 {'id': 's03-33',
  'mode': 'sql',
  'title': 'Старожилы',
  'statement': 'База HR. Выведите name и hired трёх сотрудников, давно работающих в компании.',
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
  'expected': [['Лидия Фомина', '2017-05-25'],
               ['Нина Белова', '2018-11-20'],
               ['Ольга Громова', '2019-03-01']],
  'expected_cols': ['name', 'hired'],
  'hint': '',
  'ordered': True},
 {'id': 's03-34',
  'mode': 'sql',
  'title': 'Сотрудники по отделам',
  'statement': 'База HR. Выведите dept_id, name, salary: по отделу, внутри отдела — по убыванию зарплаты, '
               'затем по name. NULL-отдел идёт первым.',
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
  'expected': [[None, 'Тимур Рахимов', 130000],
               [1, 'Ольга Громова', 320000],
               [1, 'Игорь Беляев', 210000],
               [1, 'Мария Орлова', 190000],
               [1, 'Пётр Зуев', 120000],
               [2, 'Нина Белова', 280000],
               [2, 'Юлия Седова', 175000],
               [2, 'Анна Крылова', 150000],
               [2, 'Олег Савин', 150000],
               [2, 'Сергей Ким', 95000],
               [3, 'Лидия Фомина', 200000],
               [3, 'Роман Дьяков', 110000],
               [4, 'Ева Миронова', 170000],
               [4, 'Вера Жукова', 85000],
               [4, 'Артём Исаев', 80000]],
  'expected_cols': ['dept_id', 'name', 'salary'],
  'hint': '',
  'ordered': True},
 {'id': 's03-35',
  'mode': 'sql',
  'title': 'Лучшие оценки',
  'statement': 'Школьная база. Выведите student_id, course_id, score для 2024 года: по убыванию score (NULL '
               '— в конце), затем по student_id, course_id; первые 6 строк.',
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
  'expected': [[1, 1, 5], [1, 3, 5], [3, 4, 5], [4, 2, 5], [4, 3, 5], [5, 1, 5]],
  'expected_cols': ['student_id', 'course_id', 'score'],
  'hint': '',
  'ordered': True},
 {'id': 's03-36',
  'mode': 'sql',
  'title': 'Младшие ученики',
  'statement': 'Школьная база. Выведите name и birth трёх самых младших учеников (самые поздние даты '
               'рождения).',
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
  'expected': [['Богдан Сидоров', '2009-09-30'],
               ['Тимофей Орлов', '2009-08-15'],
               ['Алёна Громова', '2009-04-12']],
  'expected_cols': ['name', 'birth'],
  'hint': '',
  'ordered': True},
 {'id': 's03-37',
  'mode': 'sql',
  'title': 'Фильмы по рейтингу',
  'statement': 'База фильмов. Выведите title и rating фильмов по убыванию рейтинга; фильмы без рейтинга — в '
               'конце. Первые 5.',
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
  'expected': [['Тёмный рыцарь', 9.0],
               ['Начало', 8.8],
               ['Интерстеллар', 8.7],
               ['Унесённые призраками', 8.6],
               ['Ходячий замок', 8.2]],
  'expected_cols': ['title', 'rating'],
  'hint': '',
  'ordered': True},
 {'id': 's03-38',
  'mode': 'sql',
  'title': 'Самые длинные бюджеты',
  'statement': 'База фильмов. Выведите title и budget трёх фильмов с самым большим бюджетом.',
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
  'expected': [['Тёмный рыцарь', 185], ['Интерстеллар', 165], ['Дюна', 165]],
  'expected_cols': ['title', 'budget'],
  'hint': '',
  'ordered': True},
 {'id': 's03-39',
  'mode': 'sql',
  'title': 'Хронология',
  'statement': 'База фильмов. Выведите title и year по возрастанию года, при равенстве — по title.',
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
  'expected': [['Унесённые призраками', 2001],
               ['Ходячий замок', 2004],
               ['Тёмный рыцарь', 2008],
               ['Начало', 2010],
               ['Ветер крепчает', 2013],
               ['Интерстеллар', 2014],
               ['Левиафан', 2014],
               ['Прибытие', 2016],
               ['Нелюбовь', 2017],
               ['Маленькие женщины', 2019],
               ['Дюна', 2021],
               ['Неизвестный фильм', 2022],
               ['Барби', 2023]],
  'expected_cols': ['title', 'year'],
  'hint': '',
  'ordered': True}]}
