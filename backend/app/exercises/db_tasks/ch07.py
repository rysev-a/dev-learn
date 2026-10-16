"""Задачи книги «Базы данных»: глава 7."""

TASKS: dict[int, list[dict]] = {7: [{'id': 's07-01',
  'mode': 'sql',
  'title': 'Выше среднего',
  'statement': 'Выведите title и price товаров дороже средней цены. Среднюю цену получите подзапросом '
               '(SELECT AVG(price) FROM products).',
  'starter': 'SELECT title, price\nFROM products\nWHERE price > (SELECT ...);\n',
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
  'expected': [['Ноутбук Air 13', 78000], ['Смартфон S5', 45000]],
  'expected_cols': ['title', 'price'],
  'hint': 'Подзапрос в скобках возвращает одно число.'},
 {'id': 's07-02',
  'mode': 'sql',
  'title': 'Ниже среднего',
  'statement': 'Выведите title товаров дешевле среднего; по title.',
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
  'expected': [['Блокнот A5'],
               ['Клавиатура Type'],
               ['Книга Python'],
               ['Книга SQL'],
               ['Кофе зерновой'],
               ['Мышь Click'],
               ['Наушники Beat'],
               ['Подарочная карта'],
               ['Рюкзак City'],
               ['Чай зелёный'],
               ['Шоколад тёмный']],
  'expected_cols': ['title'],
  'hint': '',
  'ordered': True},
 {'id': 's07-03',
  'mode': 'sql',
  'title': 'Самый дорогой',
  'statement': 'Выведите title самого дорогого товара: price = (SELECT MAX(price) FROM products).',
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
  'expected': [['Ноутбук Air 13']],
  'expected_cols': ['title'],
  'hint': ''},
 {'id': 's07-04',
  'mode': 'sql',
  'title': 'Крупнее среднего заказа',
  'statement': 'Выведите id и total заказов, сумма которых больше средней суммы заказа; по id.',
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
  'expected': [[1, 79500], [3, 55400], [7, 45000], [11, 78000], [13, 46500]],
  'expected_cols': ['id', 'total'],
  'hint': '',
  'ordered': True},
 {'id': 's07-05',
  'mode': 'sql',
  'title': 'Подзапрос в списке столбцов',
  'statement': 'Выведите title, price и разницу с средней ценой diff = price − (SELECT AVG(price) FROM '
               'products), округлённую ROUND до целого; по id товара.',
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
  'expected': [['Ноутбук Air 13', 78000, 67070.0],
               ['Смартфон S5', 45000, 34070.0],
               ['Наушники Beat', 5200, -5730.0],
               ['Мышь Click', 1500, -9430.0],
               ['Клавиатура Type', 3900, -7030.0],
               ['Рюкзак City', 3200, -7730.0],
               ['Кофе зерновой', 890, -10040.0],
               ['Чай зелёный', 420, -10510.0],
               ['Шоколад тёмный', 180, -10750.0],
               ['Книга SQL', 1200, -9730.0],
               ['Книга Python', 1350, -9580.0],
               ['Блокнот A5', 250, -10680.0],
               ['Подарочная карта', 1000, -9930.0]],
  'expected_cols': ['title', 'price', 'diff'],
  'hint': '',
  'ordered': True},
 {'id': 's07-06',
  'mode': 'sql',
  'title': 'IN: у кого есть заказы',
  'statement': 'Выведите name клиентов, у которых есть заказы: id IN (SELECT customer_id FROM orders); по '
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
               ['Вера Смирнова'],
               ['Глеб Орлов'],
               ['Дарья Лебедева'],
               ['Егор Козлов'],
               ['Игорь Соколов'],
               ['Лев Новиков'],
               ['Мария Фёдорова'],
               ['Никита Белов']],
  'expected_cols': ['name'],
  'hint': 'Подзапрос возвращает столбец значений для IN.',
  'ordered': True},
 {'id': 's07-07',
  'mode': 'sql',
  'title': 'NOT IN: без заказов',
  'statement': 'Выведите name клиентов без заказов (NOT IN); по name.',
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
 {'id': 's07-08',
  'mode': 'sql',
  'title': 'Ловушка NOT IN с NULL',
  'statement': "Бренд category 'Канцелярия' неизвестен (NULL), и NOT IN с таким списком не вернёт ничего. "
               'Выведите title товаров, бренд которых не совпадает ни с одним известным брендом категории '
               "'Канцелярия' (добавьте в подзапрос WHERE brand IS NOT NULL); товары с неизвестным брендом в "
               'ответ не входят. По title.',
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
  'expected': [['Блокнот A5'],
               ['Клавиатура Type'],
               ['Книга Python'],
               ['Книга SQL'],
               ['Кофе зерновой'],
               ['Мышь Click'],
               ['Наушники Beat'],
               ['Ноутбук Air 13'],
               ['Подарочная карта'],
               ['Рюкзак City'],
               ['Смартфон S5'],
               ['Чай зелёный'],
               ['Шоколад тёмный']],
  'expected_cols': ['title'],
  'hint': 'Если в списке IN/NOT IN есть NULL, результат для NOT IN становится неопределённым.',
  'ordered': True},
 {'id': 's07-09',
  'mode': 'sql',
  'title': 'EXISTS',
  'statement': 'Выведите name клиентов, у которых есть отменённый заказ (EXISTS с подзапросом по '
               "orders.customer_id = c.id и status = 'cancelled'); по name.",
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
  'expected': [['Борис Иванов'], ['Мария Фёдорова']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's07-10',
  'mode': 'sql',
  'title': 'NOT EXISTS',
  'statement': 'Выведите name клиентов, у которых нет оплаченных заказов (NOT EXISTS); по name.',
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
 {'id': 's07-11',
  'mode': 'sql',
  'title': 'Коррелированный подзапрос',
  'statement': 'Для каждого клиента выведите name и число его заказов n: (SELECT COUNT(*) FROM orders o '
               'WHERE o.customer_id = c.id); по id клиента.',
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
  'expected': [['Анна Петрова', 3],
               ['Борис Иванов', 3],
               ['Вера Смирнова', 2],
               ['Глеб Орлов', 1],
               ['Дарья Лебедева', 4],
               ['Егор Козлов', 1],
               ['Жанна Морозова', 0],
               ['Игорь Соколов', 2],
               ['Ксения Волкова', 0],
               ['Лев Новиков', 2],
               ['Мария Фёдорова', 1],
               ['Никита Белов', 1]],
  'expected_cols': ['name', 'n'],
  'hint': 'Подзапрос ссылается на внешнюю строку c.',
  'ordered': True},
 {'id': 's07-12',
  'mode': 'sql',
  'title': 'Максимальный заказ клиента',
  'statement': 'Для каждого клиента выведите name и наибольшую сумму его заказов best (NULL, если заказов '
               'нет); по id.',
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
  'expected': [['Анна Петрова', 79500],
               ['Борис Иванов', 55400],
               ['Вера Смирнова', 3040],
               ['Глеб Орлов', 2550],
               ['Дарья Лебедева', 45000],
               ['Егор Козлов', 1740],
               ['Жанна Морозова', None],
               ['Игорь Соколов', 78000],
               ['Ксения Волкова', None],
               ['Лев Новиков', 46500],
               ['Мария Фёдорова', 3200],
               ['Никита Белов', 9100]],
  'expected_cols': ['name', 'best'],
  'hint': '',
  'ordered': True},
 {'id': 's07-13',
  'mode': 'sql',
  'title': 'Подзапрос во FROM',
  'statement': 'Выведите title и value (price * stock) только для товаров, у которых value больше 100000. '
               'Сначала вычислите value в подзапросе во FROM; по value по убыванию.',
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
               ['Мышь Click', 120000]],
  'expected_cols': ['title', 'value'],
  'hint': 'Подзапрос во FROM работает как временная таблица.',
  'ordered': True},
 {'id': 's07-14',
  'mode': 'sql',
  'title': 'Дважды отфильтровать',
  'statement': 'Из подзапроса «оплаченные заказы» выберите три крупнейших: id и total. Подзапрос: SELECT id, '
               "total FROM orders WHERE status = 'paid'.",
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
  'expected': [[3, 55400], [13, 46500], [16, 9100]],
  'expected_cols': ['id', 'total'],
  'hint': '',
  'ordered': True},
 {'id': 's07-15',
  'mode': 'sql',
  'title': 'Дороже любого продукта',
  'statement': "Выведите title товаров, которые дороже самого дорогого товара категории 'Продукты' (price > "
               'MAX); по title.',
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
  'expected': [['Клавиатура Type'],
               ['Книга Python'],
               ['Книга SQL'],
               ['Мышь Click'],
               ['Наушники Beat'],
               ['Ноутбук Air 13'],
               ['Подарочная карта'],
               ['Рюкзак City'],
               ['Смартфон S5']],
  'expected_cols': ['title'],
  'hint': '',
  'ordered': True},
 {'id': 's07-16',
  'mode': 'sql',
  'title': 'Дешевле любой книги',
  'statement': "Выведите title товаров, которые дешевле самой дешёвой книги (категория 'Книги'); по title.",
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
  'expected': [['Блокнот A5'], ['Кофе зерновой'], ['Подарочная карта'], ['Чай зелёный'], ['Шоколад тёмный']],
  'expected_cols': ['title'],
  'hint': '',
  'ordered': True},
 {'id': 's07-17',
  'mode': 'sql',
  'title': 'Вложенность в два уровня',
  'statement': "Выведите id заказов, в которых есть 'Ноутбук Air 13': order_id IN (SELECT order_id FROM "
               "order_items WHERE product_id = (SELECT id FROM products WHERE title = 'Ноутбук Air 13')); по "
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
  'expected': [[1], [11]],
  'expected_cols': ['id'],
  'hint': '',
  'ordered': True},
 {'id': 's07-18',
  'mode': 'sql',
  'title': 'Земляки Анны',
  'statement': "Выведите name клиентов из того же города, что и 'Анна Петрова', кроме неё самой; по name.",
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
  'expected': [['Вера Смирнова'], ['Игорь Соколов'], ['Никита Белов']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's07-19',
  'mode': 'sql',
  'title': 'Позже Бориса',
  'statement': "Выведите name клиентов, зарегистрировавшихся позже 'Борис Иванов'; по registered.",
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
  'expected': [['Вера Смирнова'],
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
 {'id': 's07-20',
  'mode': 'sql',
  'title': 'Соседи по категории',
  'statement': "Выведите title товаров той же категории, что и 'Мышь Click', кроме неё самой; по title.",
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
  'expected': [['Клавиатура Type'], ['Рюкзак City']],
  'expected_cols': ['title'],
  'hint': '',
  'ordered': True},
 {'id': 's07-21',
  'mode': 'sql',
  'title': 'Самый крупный заказ',
  'statement': 'Выведите id, total самого крупного заказа (подзапрос с MAX).',
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
  'expected': [[1, 79500]],
  'expected_cols': ['id', 'total'],
  'hint': ''},
 {'id': 's07-22',
  'mode': 'sql',
  'title': 'Вторая по величине цена',
  'statement': 'Выведите вторую по величине цену товара second: MAX(price) среди товаров, цена которых '
               'меньше максимальной.',
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
  'expected': [[45000]],
  'expected_cols': ['second'],
  'hint': ''},
 {'id': 's07-23',
  'mode': 'sql',
  'title': 'Заказы с электроникой',
  'statement': 'Выведите id заказов, содержащих хотя бы одну позицию-электронику (EXISTS и JOIN в '
               'подзапросе); по id.',
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
  'expected': [[1], [2], [3], [7], [8], [11], [13], [16]],
  'expected_cols': ['id'],
  'hint': '',
  'ordered': True},
 {'id': 's07-24',
  'mode': 'sql',
  'title': 'Скалярные подзапросы',
  'statement': 'Одной строкой выведите число клиентов customers_n и число товаров products_n двумя '
               'скалярными подзапросами.',
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
  'expected': [[12, 13]],
  'expected_cols': ['customers_n', 'products_n'],
  'hint': ''},
 {'id': 's07-25',
  'mode': 'sql',
  'title': 'HR: сотрудники московских отделов',
  'statement': 'База HR. Выведите name сотрудников отделов, расположенных в Москве (dept_id IN (SELECT id '
               "FROM departments WHERE city = 'Москва')); по id.",
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
  'expected': [['Ольга Громова'],
               ['Игорь Беляев'],
               ['Мария Орлова'],
               ['Пётр Зуев'],
               ['Лидия Фомина'],
               ['Роман Дьяков']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's07-26',
  'mode': 'sql',
  'title': 'HR: отделы без сотрудников',
  'statement': 'База HR. Выведите name отделов, где нет сотрудников (NOT EXISTS).',
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
 {'id': 's07-27',
  'mode': 'sql',
  'title': 'HR: выше средней по отделу',
  'statement': 'База HR. Выведите name и salary сотрудников, получающих больше средней зарплаты своего '
               'отдела (коррелированный подзапрос по dept_id); по name.',
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
  'expected': [['Ева Миронова', 170000],
               ['Лидия Фомина', 200000],
               ['Нина Белова', 280000],
               ['Ольга Громова', 320000],
               ['Юлия Седова', 175000]],
  'expected_cols': ['name', 'salary'],
  'hint': '',
  'ordered': True},
 {'id': 's07-28',
  'mode': 'sql',
  'title': 'HR: лучшие в отделе',
  'statement': 'База HR. Выведите name, dept_id и salary сотрудников с самой высокой зарплатой в своём '
               'отделе (сотрудников без отдела не учитывайте); по dept_id.',
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
  'expected': [['Ольга Громова', 1, 320000],
               ['Нина Белова', 2, 280000],
               ['Лидия Фомина', 3, 200000],
               ['Ева Миронова', 4, 170000]],
  'expected_cols': ['name', 'dept_id', 'salary'],
  'hint': '',
  'ordered': True},
 {'id': 's07-29',
  'mode': 'sql',
  'title': 'HR: кто руководит',
  'statement': 'База HR. Выведите name сотрудников, которые являются чьими-то руководителями (id IN (SELECT '
               'boss_id …)); по id.',
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
  'expected': [['Ольга Громова'], ['Игорь Беляев'], ['Нина Белова'], ['Лидия Фомина'], ['Ева Миронова']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's07-30',
  'mode': 'sql',
  'title': 'HR: рядовые',
  'statement': 'База HR. Выведите name сотрудников, у которых нет подчинённых (NOT EXISTS); по id.',
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
  'expected': [['Мария Орлова'],
               ['Пётр Зуев'],
               ['Олег Савин'],
               ['Анна Крылова'],
               ['Сергей Ким'],
               ['Роман Дьяков'],
               ['Артём Исаев'],
               ['Вера Жукова'],
               ['Тимур Рахимов'],
               ['Юлия Седова']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's07-31',
  'mode': 'sql',
  'title': 'HR: выше общей средней',
  'statement': 'База HR. Выведите name и salary сотрудников с зарплатой выше средней по компании; по salary '
               'по убыванию.',
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
               ['Мария Орлова', 190000],
               ['Юлия Седова', 175000],
               ['Ева Миронова', 170000]],
  'expected_cols': ['name', 'salary'],
  'hint': '',
  'ordered': True},
 {'id': 's07-32',
  'mode': 'sql',
  'title': 'Школа: записанные на математику',
  'statement': "Школьная база. Выведите name учеников, у которых есть запись по курсу 'Математика' (id IN "
               'подзапрос с двумя уровнями); по name.',
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
  'expected': [['Алёна Громова'],
               ['Богдан Сидоров'],
               ['Варвара Кузнецова'],
               ['Галина Соколова'],
               ['Давид Попов'],
               ['Ева Васильева'],
               ['Яна Тихонова']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's07-33',
  'mode': 'sql',
  'title': 'Школа: самый длинный курс',
  'statement': 'Школьная база. Выведите title курсов с наибольшим числом часов; по title.',
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
  'expected': [['Математика']],
  'expected_cols': ['title'],
  'hint': '',
  'ordered': True},
 {'id': 's07-34',
  'mode': 'sql',
  'title': 'Школа: выше среднего',
  'statement': 'Школьная база. Выведите name учеников, у которых есть оценка выше средней по школе (EXISTS); '
               'по name.',
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
  'expected': [['Алёна Громова'],
               ['Варвара Кузнецова'],
               ['Галина Соколова'],
               ['Давид Попов'],
               ['Ева Васильева'],
               ['Игнат Павлов'],
               ['Яна Тихонова']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's07-35',
  'mode': 'sql',
  'title': 'Фильмы выше среднего рейтинга',
  'statement': 'База фильмов. Выведите title и rating фильмов с рейтингом выше среднего; по рейтингу по '
               'убыванию, затем по title.',
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
 {'id': 's07-36',
  'mode': 'sql',
  'title': 'Режиссёры недавних фильмов',
  'statement': 'База фильмов. Выведите name режиссёров, у которых есть фильм, вышедший после 2015 года '
               '(EXISTS); по name.',
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
  'expected': [['Андрей Звягинцев'], ['Грета Гервиг'], ['Дени Вильнёв']],
  'expected_cols': ['name'],
  'hint': '',
  'ordered': True},
 {'id': 's07-37',
  'mode': 'sql',
  'title': 'Коллеги Нолана',
  'statement': "База фильмов. Выведите title всех фильмов режиссёра фильма 'Начало', кроме самого 'Начало'; "
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
  'expected': [['Интерстеллар'], ['Тёмный рыцарь']],
  'expected_cols': ['title'],
  'hint': '',
  'ordered': True}]}
