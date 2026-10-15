"""Задачи книги «Базы данных: под капотом»: главы 1–3."""

TASKS: dict[int, list[dict]] = {
    1: [
        {
            "id": "sql-filter-sort",
            "mode": "sql",
            "title": "Фильтр и сортировка",
            "statement": (
                "Таблица products(id, title, category, price). Выведите название и "
                "цену товаров дороже 1000 рублей, самые дорогие — первыми (колонки: "
                "title, price)."
            ),
            "starter": "-- название и цена товаров дороже 1000, по убыванию цены\nSELECT\n",
            "setup": (
                "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n"
                "CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, price INTEGER NOT NULL);\n"
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n"
                "CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n"
                "INSERT INTO customers VALUES (1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
                "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
                "INSERT INTO orders VALUES (1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
                "INSERT INTO order_items VALUES (1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n"
            ),
            "expected": [["Ноутбук", 70000], ["Наушники", 5000], ["Мышь", 1500]],
            "ordered": True,
            "hint": "WHERE price > 1000 ORDER BY price DESC.",
        },
        {
            "id": "sql-join-paid",
            "mode": "sql",
            "title": "Соединение таблиц",
            "statement": (
                "Выведите имя клиента и дату заказа для всех оплаченных заказов "
                "(status = 'paid') по возрастанию даты, при равенстве — по имени. "
                "Колонки: name, created."
            ),
            "starter": "-- имя клиента и дата оплаченных заказов\nSELECT\n",
            "setup": (
                "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n"
                "CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, price INTEGER NOT NULL);\n"
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n"
                "CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n"
                "INSERT INTO customers VALUES (1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
                "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
                "INSERT INTO orders VALUES (1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
                "INSERT INTO order_items VALUES (1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n"
            ),
            "expected": [["Анна", "2024-01-05"], ["Анна", "2024-02-10"], ["Вера", "2024-03-01"], ["Вера", "2024-03-15"], ["Дарья", "2024-04-03"], ["Борис", "2024-04-20"]],
            "ordered": True,
            "hint": "orders JOIN customers ON customers.id = orders.customer_id.",
        },
        {
            "id": "sql-left-join",
            "mode": "sql",
            "title": "Клиенты без заказов",
            "statement": (
                "Найдите клиентов, у которых нет ни одного заказа. Выведите одну "
                "колонку name."
            ),
            "starter": "-- клиенты без заказов\nSELECT\n",
            "setup": (
                "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n"
                "CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, price INTEGER NOT NULL);\n"
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n"
                "CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n"
                "INSERT INTO customers VALUES (1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
                "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
                "INSERT INTO orders VALUES (1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
                "INSERT INTO order_items VALUES (1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n"
            ),
            "expected": [["Глеб"], ["Егор"]],
            "ordered": False,
            "hint": "LEFT JOIN и условие IS NULL на колонку правой таблицы (или NOT EXISTS).",
        },
        {
            "id": "sql-group-having",
            "mode": "sql",
            "title": "Группировка и HAVING",
            "statement": (
                "Для каждого клиента посчитайте число оплаченных заказов (status = "
                "'paid') и оставьте тех, у кого их не меньше двух. Колонки: name, "
                "paid_orders."
            ),
            "starter": "-- клиенты с двумя и более оплаченными заказами\nSELECT\n",
            "setup": (
                "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n"
                "CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, price INTEGER NOT NULL);\n"
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n"
                "CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n"
                "INSERT INTO customers VALUES (1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
                "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
                "INSERT INTO orders VALUES (1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
                "INSERT INTO order_items VALUES (1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n"
            ),
            "expected": [["Анна", 2], ["Вера", 2]],
            "ordered": False,
            "hint": "Условие по строкам — в WHERE, по группам — в HAVING.",
        },
        {
            "id": "sql-revenue-category",
            "mode": "sql",
            "title": "Выручка по категориям",
            "statement": (
                "Посчитайте выручку (сумма qty · price) по категориям товаров "
                "только по оплаченным заказам. Колонки: category, revenue; самая "
                "большая выручка — первой."
            ),
            "starter": "-- выручка по категориям\nSELECT\n",
            "setup": (
                "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n"
                "CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, price INTEGER NOT NULL);\n"
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n"
                "CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n"
                "INSERT INTO customers VALUES (1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
                "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
                "INSERT INTO orders VALUES (1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
                "INSERT INTO order_items VALUES (1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n"
            ),
            "expected": [["tech", 159500], ["food", 5600], ["books", 2700]],
            "ordered": True,
            "hint": "Три таблицы через JOIN, затем GROUP BY category и SUM(i.qty * p.price).",
        },
        {
            "id": "sql-subquery-avg",
            "mode": "sql",
            "title": "Подзапрос",
            "statement": (
                "Выведите названия товаров, цена которых выше средней цены всех "
                "товаров (колонка title)."
            ),
            "starter": "-- товары дороже средней цены\nSELECT\n",
            "setup": (
                "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n"
                "CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, price INTEGER NOT NULL);\n"
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n"
                "CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n"
                "INSERT INTO customers VALUES (1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
                "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
                "INSERT INTO orders VALUES (1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
                "INSERT INTO order_items VALUES (1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n"
            ),
            "expected": [["Ноутбук"]],
            "ordered": False,
            "hint": "Скалярный подзапрос (SELECT AVG(price) FROM products) можно использовать в WHERE.",
        },
        {
            "id": "sql-window-top",
            "mode": "sql",
            "title": "Оконная функция: лучший в категории",
            "statement": (
                "Для каждой категории выведите самый дорогой товар: колонки "
                "category, title, price. Используйте оконную функцию RANK() или "
                "ROW_NUMBER() с PARTITION BY."
            ),
            "starter": "-- самый дорогой товар в каждой категории\nSELECT\n",
            "setup": (
                "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n"
                "CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, price INTEGER NOT NULL);\n"
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n"
                "CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n"
                "INSERT INTO customers VALUES (1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
                "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
                "INSERT INTO orders VALUES (1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
                "INSERT INTO order_items VALUES (1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n"
            ),
            "expected": [["books", "Книга SQL", 900], ["food", "Кофе", 600], ["tech", "Ноутбук", 70000]],
            "ordered": False,
            "hint": "Во внутреннем запросе пронумеруйте товары внутри категории (RANK() OVER (PARTITION BY category ORDER BY price DESC)), во внешнем оставьте первых.",
        },
        {
            "id": "sql-case-label",
            "mode": "sql",
            "title": "CASE: размер заказа",
            "statement": (
                "Для каждого оплаченного заказа посчитайте сумму (qty · price) и "
                "подпишите: 'big' при сумме не меньше 10000, иначе 'small'. "
                "Колонки: order_id, total, size; по возрастанию order_id."
            ),
            "starter": "-- сумма и размер оплаченных заказов\nSELECT\n",
            "setup": (
                "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n"
                "CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, price INTEGER NOT NULL);\n"
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n"
                "CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n"
                "INSERT INTO customers VALUES (1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
                "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
                "INSERT INTO orders VALUES (1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
                "INSERT INTO order_items VALUES (1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n"
            ),
            "expected": [[1, 73000, "big"], [2, 2700, "small"], [4, 75000, "big"], [5, 2400, "small"], [7, 3200, "small"], [8, 11500, "big"]],
            "ordered": True,
            "hint": "CASE WHEN SUM(...) >= 10000 THEN 'big' ELSE 'small' END прямо в SELECT.",
        },
        {
            "id": "sql-create-reviews",
            "mode": "sql",
            "title": "Схема с ключами",
            "statement": (
                "Создайте таблицу reviews: id — первичный ключ; customer_id — "
                "внешний ключ на customers(id), не NULL; product_id — внешний ключ "
                "на products(id), не NULL; rating — целое от 1 до 5 (CHECK); text — "
                "текст. Проверка смотрит определение таблицы."
            ),
            "starter": "-- CREATE TABLE reviews (...)\n",
            "setup": (
                "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n"
                "CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, price INTEGER NOT NULL);\n"
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n"
                "CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n"
                "INSERT INTO customers VALUES (1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
                "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
                "INSERT INTO orders VALUES (1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
                "INSERT INTO order_items VALUES (1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n"
            ),
            "check": "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'reviews'",
            "contains": ["PRIMARY KEY", "REFERENCES customers", "REFERENCES products", "CHECK", "NOT NULL"],
            "hint": "customer_id INTEGER NOT NULL REFERENCES customers(id); rating INTEGER CHECK (rating BETWEEN 1 AND 5).",
        },
    ],
    2: [
        {
            "id": "tx-transfer",
            "mode": "sql",
            "title": "Перевод в транзакции",
            "statement": (
                "Переведите 300 рублей со счёта 1 на счёт 2 одной транзакцией: "
                "BEGIN, два UPDATE, COMMIT. Проверка читает балансы после "
                "выполнения."
            ),
            "starter": "BEGIN;\n-- списание\n-- зачисление\nCOMMIT;\n",
            "setup": (
                "CREATE TABLE accounts (id INTEGER PRIMARY KEY, owner TEXT NOT NULL, balance INTEGER NOT NULL CHECK (balance >= 0));\n"
                "INSERT INTO accounts VALUES (1,'Анна',1000),(2,'Борис',200),(3,'Вера',50);\n"
            ),
            "check": "SELECT id, balance FROM accounts ORDER BY id",
            "expected": [[1, 700], [2, 500], [3, 50]],
            "ordered": True,
            "hint": "Оба UPDATE между BEGIN и COMMIT: либо оба применятся, либо ни один.",
        },
        {
            "id": "tx-safe-transfer",
            "mode": "sql",
            "title": "Переводы с проверкой остатка",
            "statement": (
                "В одной транзакции выполните два перевода: 500 рублей со счёта 3 "
                "(там 50) на счёт 2 и 100 рублей со счёта 1 на счёт 2. Каждый "
                "перевод должен срабатывать только при достаточном остатке: "
                "списывайте с условием balance >= сумма, а зачисляйте только если "
                "списание сработало (функция changes() возвращает число строк, "
                "затронутых последним запросом). Первый перевод не пройдёт, второй "
                "— пройдёт."
            ),
            "starter": "BEGIN;\n-- перевод 3 → 2 на 500: списание и зачисление\n-- перевод 1 → 2 на 100: списание и зачисление\nCOMMIT;\n",
            "setup": (
                "CREATE TABLE accounts (id INTEGER PRIMARY KEY, owner TEXT NOT NULL, balance INTEGER NOT NULL CHECK (balance >= 0));\n"
                "INSERT INTO accounts VALUES (1,'Анна',1000),(2,'Борис',200),(3,'Вера',50);\n"
            ),
            "check": "SELECT id, balance FROM accounts ORDER BY id",
            "expected": [[1, 900], [2, 300], [3, 50]],
            "ordered": True,
            "hint": "Зачисление: UPDATE ... WHERE id = 2 AND changes() = 1 — оно видит число строк предыдущего UPDATE.",
        },
        {
            "id": "tx-savepoint",
            "mode": "sql",
            "title": "Точка сохранения",
            "statement": (
                "В одной транзакции: спишите 100 со счёта 1; поставьте SAVEPOINT "
                "s1; спишите ещё 900 со счёта 1; откатитесь к s1 (ROLLBACK TO s1); "
                "зафиксируйте транзакцию. Итог: со счёта 1 списано только 100."
            ),
            "starter": "BEGIN;\n-- UPDATE ...\nSAVEPOINT s1;\n-- UPDATE ...\n-- откат к s1\nCOMMIT;\n",
            "setup": (
                "CREATE TABLE accounts (id INTEGER PRIMARY KEY, owner TEXT NOT NULL, balance INTEGER NOT NULL CHECK (balance >= 0));\n"
                "INSERT INTO accounts VALUES (1,'Анна',1000),(2,'Борис',200),(3,'Вера',50);\n"
            ),
            "check": "SELECT id, balance FROM accounts ORDER BY id",
            "expected": [[1, 900], [2, 200], [3, 50]],
            "ordered": True,
            "hint": "ROLLBACK TO s1 отменяет только то, что было после SAVEPOINT s1; транзакция остаётся открытой.",
        },
        {
            "id": "tx-upsert",
            "mode": "sql",
            "title": "Upsert: вставить или увеличить",
            "statement": (
                "Учтите три просмотра: страница 'home' (уже есть) и две новые — "
                "'about' и 'blog'. Для каждой напишите один INSERT ... ON "
                "CONFLICT(page) DO UPDATE SET views = views + 1 (для новых будет "
                "views = 1). Всего три оператора."
            ),
            "starter": "-- три INSERT ... ON CONFLICT ...\n",
            "setup": (
                "CREATE TABLE page_views (page TEXT PRIMARY KEY, views INTEGER NOT NULL);\n"
                "INSERT INTO page_views VALUES ('home', 10);\n"
            ),
            "check": "SELECT page, views FROM page_views ORDER BY page",
            "expected": [["about", 1], ["blog", 1], ["home", 11]],
            "ordered": True,
            "hint": "INSERT INTO page_views VALUES ('home', 1) ON CONFLICT(page) DO UPDATE SET views = views + 1;",
        },
        {
            "id": "tx-serializable",
            "mode": "func",
            "func": "serializable",
            "title": "Конфликтная сериализуемость",
            "statement": (
                "Расписание — список операций [транзакция, 'R' или 'W', объект] в "
                "порядке выполнения. Две операции конфликтуют, если они из разных "
                "транзакций, над одним объектом и хотя бы одна — запись. Напишите "
                "функцию serializable(schedule): постройте граф «раньше → позже» по "
                "конфликтам (Ti → Tj, если конфликтующая операция Ti стоит раньше). "
                "Если цикла нет — верните список транзакций в порядке "
                "топологической сортировки (при выборе — по алфавиту), иначе None."
            ),
            "starter": "import heapq\n\n\ndef serializable(schedule):\n    pass\n",
            "tests": [
                {"args": [[["T1", "R", "x"], ["T2", "W", "x"], ["T1", "W", "y"], ["T2", "R", "y"]]], "expected": ["T1", "T2"]},
                {"args": [[["T1", "R", "x"], ["T2", "W", "x"], ["T2", "W", "y"], ["T1", "W", "y"]]], "expected": None},
                {"args": [[["T1", "R", "x"], ["T2", "R", "x"]]], "expected": ["T1", "T2"]},
                {"args": [[]], "expected": []},
                {"args": [[["T1", "W", "x"], ["T2", "W", "x"], ["T3", "R", "x"]]], "expected": ["T1", "T2", "T3"]},
                {"args": [[["T2", "W", "a"], ["T1", "R", "a"], ["T3", "W", "b"], ["T1", "W", "b"]]], "expected": ["T2", "T3", "T1"]},
            ],
            "hint": "Для каждой пары операций (i < j) с конфликтом добавьте ребро; затем алгоритм Кана — если выбрались не все вершины, есть цикл.",
        },
        {
            "id": "tx-anomalies",
            "mode": "func",
            "func": "anomalies",
            "title": "Аномалии параллельного доступа",
            "statement": (
                "Расписание — список операций [транзакция, операция, объект], "
                "операция 'R', 'W', 'C' (фиксация) или 'A' (откат); у 'C' и 'A' "
                "объект — None. Напишите функцию anomalies(schedule): верните "
                "отсортированный список имён найденных аномалий: 'dirty_read' — "
                "транзакция читает объект, изменённый другой транзакцией, которая к "
                "этому моменту ещё не зафиксирована; 'non_repeatable_read' — "
                "транзакция дважды читает объект, и между чтениями другая "
                "транзакция записала его и зафиксировалась; 'lost_update' — две "
                "транзакции прочитали объект, затем обе записали его (до фиксации "
                "первой записи)."
            ),
            "starter": "def anomalies(schedule):\n    pass\n",
            "tests": [
                {"args": [[["T1", "W", "x"], ["T2", "R", "x"], ["T1", "A", None], ["T2", "C", None]]], "expected": ["dirty_read"]},
                {"args": [[["T1", "R", "x"], ["T2", "W", "x"], ["T2", "C", None], ["T1", "R", "x"], ["T1", "C", None]]], "expected": ["non_repeatable_read"]},
                {"args": [[["T1", "R", "x"], ["T2", "R", "x"], ["T1", "W", "x"], ["T2", "W", "x"], ["T1", "C", None], ["T2", "C", None]]], "expected": ["lost_update"]},
                {"args": [[["T1", "R", "x"], ["T1", "W", "x"], ["T1", "C", None], ["T2", "R", "x"], ["T2", "C", None]]], "expected": []},
                {"args": [[]], "expected": []},
                {"args": [[["T1", "W", "x"], ["T1", "C", None], ["T2", "R", "x"]]], "expected": []},
                {"args": [[["T1", "R", "x"], ["T2", "W", "x"], ["T1", "R", "x"], ["T2", "C", None]]], "expected": ["dirty_read"]},
            ],
            "hint": "Каждую аномалию ищите отдельным проходом по расписанию; фиксации ('C') определяют, «грязное» ли чтение.",
        },
        {
            "id": "tx-deadlock",
            "mode": "func",
            "func": "deadlocked",
            "title": "Поиск взаимной блокировки",
            "statement": (
                "События — список [транзакция, 'lock' или 'unlock', объект]. "
                "Эксклюзивные блокировки: 'lock' занимает объект, если он свободен; "
                "если занят другой транзакцией — транзакция ждёт (запрос ждёт, пока "
                "объект освободят, и дальше этого объекта не продвигается; новые "
                "события этой же транзакции пока игнорируются). 'unlock' "
                "освобождает объект, и первая ждущая транзакция (по порядку "
                "появления) его получает. Напишите функцию deadlocked(events): "
                "после обработки всех событий верните отсортированный список "
                "транзакций, участвующих в цикле ожидания (T1 ждёт объект T2, T2 "
                "ждёт объект T1…)."
            ),
            "starter": "def deadlocked(events):\n    pass\n",
            "tests": [
                {"args": [[["T1", "lock", "a"], ["T2", "lock", "b"], ["T1", "lock", "b"], ["T2", "lock", "a"]]], "expected": ["T1", "T2"]},
                {"args": [[["T1", "lock", "a"], ["T2", "lock", "a"], ["T1", "unlock", "a"]]], "expected": []},
                {"args": [[["T1", "lock", "a"], ["T2", "lock", "b"], ["T3", "lock", "c"], ["T1", "lock", "b"], ["T2", "lock", "c"], ["T3", "lock", "a"]]], "expected": ["T1", "T2", "T3"]},
                {"args": [[]], "expected": []},
                {"args": [[["T1", "lock", "a"], ["T2", "lock", "a"], ["T3", "lock", "a"]]], "expected": []},
                {"args": [[["T1", "lock", "a"], ["T2", "lock", "b"], ["T3", "lock", "c"], ["T1", "lock", "b"], ["T2", "lock", "a"], ["T3", "lock", "a"]]], "expected": ["T1", "T2"]},
            ],
            "hint": "Граф «кто кого ждёт»: транзакция → владелец объекта, который она запросила; цикл в таком графе — и есть deadlock.",
        },
        {
            "id": "tx-mvcc-visible",
            "mode": "func",
            "func": "visible",
            "title": "MVCC: какие версии видны",
            "statement": (
                "Версия строки — [id, xmin, xmax]: xmin — транзакция, создавшая "
                "версию; xmax — транзакция, удалившая её (None — не удалена). "
                "Моментальный снимок: snapshot — наибольший номер транзакции, "
                "видимый читателю; committed — список зафиксированных транзакций. "
                "Версия видна, если xmin зафиксирована и xmin ≤ snapshot, и при "
                "этом (xmax is None, или xmax не зафиксирована, или xmax > "
                "snapshot). Напишите функцию visible(versions, snapshot, "
                "committed): список id видимых версий в исходном порядке."
            ),
            "starter": "def visible(versions, snapshot, committed):\n    pass\n",
            "tests": [
                {"args": [[["a", 1, None], ["b", 2, 3], ["c", 3, None]], 3, [1, 2, 3]], "expected": ["a", "c"]},
                {"args": [[["a", 1, None], ["b", 2, 3], ["c", 3, None]], 2, [1, 2, 3]], "expected": ["a", "b"]},
                {"args": [[["a", 1, 2]], 5, [1]], "expected": ["a"]},
                {"args": [[["a", 1, 2]], 5, [1, 2]], "expected": []},
                {"args": [[["a", 4, None]], 3, [4]], "expected": []},
                {"args": [[], 10, []], "expected": []},
                {"args": [[["a", 1, None], ["a2", 5, None]], 4, [1, 5]], "expected": ["a"]},
            ],
            "hint": "Проверьте по очереди: xmin виден читателю? затем: не удалена ли версия для этого снимка.",
        },
        {
            "id": "tx-two-phase-commit",
            "mode": "func",
            "func": "two_phase_commit",
            "title": "Двухфазная фиксация",
            "statement": (
                "Координатор 2PC опрашивает участников. Напишите функцию "
                "two_phase_commit(votes): votes — ответы участников на фазе "
                "подготовки: 'yes', 'no' или 'timeout'. Решение: 'commit', если все "
                "ответили 'yes' (и участников хотя бы один), иначе 'abort'. Верните "
                "кортеж (решение, состояния_участников): при commit все участники — "
                "'committed'; при abort — те, кто ответил 'yes', 'aborted' (они "
                "откатываются по команде), ответившие 'no' — 'aborted' (уже "
                "откатились сами), ответившие 'timeout' — 'unknown'."
            ),
            "starter": "def two_phase_commit(votes):\n    pass\n",
            "tests": [
                {"args": [["yes", "yes", "yes"]], "expected": ("commit", ["committed", "committed", "committed"])},
                {"args": [["yes", "no", "yes"]], "expected": ("abort", ["aborted", "aborted", "aborted"])},
                {"args": [["yes", "timeout"]], "expected": ("abort", ["aborted", "unknown"])},
                {"args": [[]], "expected": ("abort", [])},
                {"args": [["no"]], "expected": ("abort", ["aborted"])},
                {"args": [["timeout", "timeout"]], "expected": ("abort", ["unknown", "unknown"])},
            ],
            "hint": "Единственный путь к commit — единогласное 'yes' всех участников.",
        },
    ],
    3: [
        {
            "id": "idx-basic",
            "mode": "sql",
            "title": "Индекс по внешнему ключу",
            "statement": (
                "Запрос SELECT * FROM orders WHERE customer_id = 42 сейчас читает "
                "всю таблицу. Создайте индекс idx_orders_customer так, чтобы план "
                "запроса использовал индекс. Проверка выполняет EXPLAIN QUERY PLAN "
                "этого запроса."
            ),
            "starter": "-- CREATE INDEX idx_orders_customer ON ...\n",
            "setup": (
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, status TEXT NOT NULL, created TEXT NOT NULL, total INTEGER NOT NULL);\n"
                "CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, name TEXT NOT NULL);\n"
                "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 2000)\n"
                "INSERT INTO orders SELECT i, i % 100, CASE WHEN i % 10 = 0 THEN 'new' ELSE 'paid' END, '2024-' || printf('%02d', 1 + i % 12) || '-' || printf('%02d', 1 + i % 28), i % 500 FROM n;\n"
                "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 500)\n"
                "INSERT INTO users SELECT i, 'user' || i || '@Example.com', 'name' || i FROM n;\n"
            ),
            "check": "EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 42",
            "contains": ["USING INDEX idx_orders_customer"],
            "hint": "CREATE INDEX имя ON таблица(колонка);",
        },
        {
            "id": "idx-composite",
            "mode": "sql",
            "title": "Составной индекс и порядок колонок",
            "statement": (
                "Запрос SELECT id FROM orders WHERE status = 'new' ORDER BY created "
                "требует сортировки. Создайте индекс idx_orders_status_created, "
                "который отдаёт строки уже в нужном порядке (в плане не должно быть "
                "'USE TEMP B-TREE')."
            ),
            "starter": "-- составной индекс: сначала равенство, потом сортировка\n",
            "setup": (
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, status TEXT NOT NULL, created TEXT NOT NULL, total INTEGER NOT NULL);\n"
                "CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, name TEXT NOT NULL);\n"
                "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 2000)\n"
                "INSERT INTO orders SELECT i, i % 100, CASE WHEN i % 10 = 0 THEN 'new' ELSE 'paid' END, '2024-' || printf('%02d', 1 + i % 12) || '-' || printf('%02d', 1 + i % 28), i % 500 FROM n;\n"
                "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 500)\n"
                "INSERT INTO users SELECT i, 'user' || i || '@Example.com', 'name' || i FROM n;\n"
            ),
            "check": "EXPLAIN QUERY PLAN SELECT id FROM orders WHERE status = 'new' ORDER BY created",
            "contains": ["USING"],
            "forbid": ["TEMP B-TREE"],
            "hint": "Колонка с равенством — первой, колонка сортировки — второй: (status, created).",
        },
        {
            "id": "idx-covering",
            "mode": "sql",
            "title": "Покрывающий индекс",
            "statement": (
                "Запрос SELECT created, total FROM orders WHERE customer_id = 7 "
                "читает только две колонки. Создайте индекс idx_orders_cover так, "
                "чтобы таблицу вообще не читали: в плане должно быть 'COVERING "
                "INDEX'."
            ),
            "starter": "-- индекс, содержащий все нужные колонки\n",
            "setup": (
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, status TEXT NOT NULL, created TEXT NOT NULL, total INTEGER NOT NULL);\n"
                "CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, name TEXT NOT NULL);\n"
                "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 2000)\n"
                "INSERT INTO orders SELECT i, i % 100, CASE WHEN i % 10 = 0 THEN 'new' ELSE 'paid' END, '2024-' || printf('%02d', 1 + i % 12) || '-' || printf('%02d', 1 + i % 28), i % 500 FROM n;\n"
                "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 500)\n"
                "INSERT INTO users SELECT i, 'user' || i || '@Example.com', 'name' || i FROM n;\n"
            ),
            "check": "EXPLAIN QUERY PLAN SELECT created, total FROM orders WHERE customer_id = 7",
            "contains": ["COVERING INDEX idx_orders_cover"],
            "hint": "Индекс на (customer_id, created, total): по первой колонке ищем, остальные — «пассажиры».",
        },
        {
            "id": "idx-partial",
            "mode": "sql",
            "title": "Частичный индекс",
            "statement": (
                "Активные заказы (status = 'new') составляют малую долю таблицы, а "
                "запросы SELECT id FROM orders WHERE status = 'new' AND customer_id "
                "= 5 частые. Создайте частичный индекс idx_orders_new по "
                "customer_id только для строк со status = 'new' и убедитесь, что "
                "запрос его использует."
            ),
            "starter": "-- CREATE INDEX idx_orders_new ON orders(...) WHERE ...\n",
            "setup": (
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, status TEXT NOT NULL, created TEXT NOT NULL, total INTEGER NOT NULL);\n"
                "CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, name TEXT NOT NULL);\n"
                "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 2000)\n"
                "INSERT INTO orders SELECT i, i % 100, CASE WHEN i % 10 = 0 THEN 'new' ELSE 'paid' END, '2024-' || printf('%02d', 1 + i % 12) || '-' || printf('%02d', 1 + i % 28), i % 500 FROM n;\n"
                "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 500)\n"
                "INSERT INTO users SELECT i, 'user' || i || '@Example.com', 'name' || i FROM n;\n"
            ),
            "check": "EXPLAIN QUERY PLAN SELECT id FROM orders WHERE status = 'new' AND customer_id = 5",
            "contains": ["idx_orders_new"],
            "hint": "В конце CREATE INDEX добавьте WHERE status = 'new'.",
        },
        {
            "id": "idx-expression",
            "mode": "sql",
            "title": "Функциональный индекс",
            "statement": (
                "Поиск по почте без учёта регистра: SELECT id FROM users WHERE "
                "lower(email) = 'user7@example.com'. Создайте индекс "
                "idx_users_email_lower по выражению lower(email), который "
                "использует этот запрос."
            ),
            "starter": "-- индекс по выражению\n",
            "setup": (
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, status TEXT NOT NULL, created TEXT NOT NULL, total INTEGER NOT NULL);\n"
                "CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, name TEXT NOT NULL);\n"
                "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 2000)\n"
                "INSERT INTO orders SELECT i, i % 100, CASE WHEN i % 10 = 0 THEN 'new' ELSE 'paid' END, '2024-' || printf('%02d', 1 + i % 12) || '-' || printf('%02d', 1 + i % 28), i % 500 FROM n;\n"
                "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 500)\n"
                "INSERT INTO users SELECT i, 'user' || i || '@Example.com', 'name' || i FROM n;\n"
            ),
            "check": "EXPLAIN QUERY PLAN SELECT id FROM users WHERE lower(email) = 'user7@example.com'",
            "contains": ["idx_users_email_lower"],
            "hint": "Индекс можно построить по выражению: ON users(lower(email)).",
        },
        {
            "id": "idx-unique",
            "mode": "sql",
            "title": "Уникальный индекс",
            "statement": (
                "Почта пользователя должна быть уникальной без учёта регистра. "
                "Создайте уникальный индекс uq_users_email по lower(email). "
                "Проверка смотрит определение индекса."
            ),
            "starter": "-- CREATE UNIQUE INDEX ...\n",
            "setup": (
                "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, status TEXT NOT NULL, created TEXT NOT NULL, total INTEGER NOT NULL);\n"
                "CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL, name TEXT NOT NULL);\n"
                "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 2000)\n"
                "INSERT INTO orders SELECT i, i % 100, CASE WHEN i % 10 = 0 THEN 'new' ELSE 'paid' END, '2024-' || printf('%02d', 1 + i % 12) || '-' || printf('%02d', 1 + i % 28), i % 500 FROM n;\n"
                "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n WHERE i < 500)\n"
                "INSERT INTO users SELECT i, 'user' || i || '@Example.com', 'name' || i FROM n;\n"
            ),
            "check": "SELECT sql FROM sqlite_master WHERE type = 'index' AND name = 'uq_users_email'",
            "contains": ["UNIQUE", "lower(email)"],
            "hint": "CREATE UNIQUE INDEX uq_users_email ON users(lower(email));",
        },
        {
            "id": "idx-btree-levels",
            "mode": "func",
            "func": "btree_levels",
            "title": "Высота B+-дерева",
            "statement": (
                "Напишите функцию btree_levels(rows, leaf_capacity, fanout): в "
                "листьях страниц помещается leaf_capacity строк, во внутреннем узле "
                "— fanout ссылок на дочерние страницы. Верните список числа страниц "
                "по уровням снизу вверх (листья, затем следующий уровень и т. д., "
                "до корня — уровня из одной страницы). Для rows = 0 — [1] (пустой "
                "корень-лист)."
            ),
            "starter": "def btree_levels(rows, leaf_capacity, fanout):\n    pass\n",
            "tests": [
                {"args": [1000000, 100, 200], "expected": [10000, 50, 1]},
                {"args": [0, 100, 200], "expected": [1]},
                {"args": [50, 100, 200], "expected": [1]},
                {"args": [100, 100, 200], "expected": [1]},
                {"args": [101, 100, 200], "expected": [2, 1]},
                {"args": [1000000000, 50, 500], "expected": [20000000, 40000, 80, 1]},
                {"args": [20000, 100, 100], "expected": [200, 2, 1]},
            ],
            "hint": "Число листьев — потолок rows / leaf_capacity; на каждом следующем уровне — потолок предыдущего / fanout.",
        },
        {
            "id": "idx-leftmost-prefix",
            "mode": "func",
            "func": "usable_prefix",
            "title": "Правило левого префикса",
            "statement": (
                "Напишите функцию usable_prefix(index_cols, conds): index_cols — "
                "колонки составного индекса по порядку; conds — словарь «колонка → "
                "'=' или 'range'» условий запроса. Индекс используется по префиксу: "
                "идём по колонкам индекса слева направо — каждое условие '=' "
                "продолжает префикс; первое условие 'range' включается и обрывает "
                "префикс; колонка без условия обрывает без включения. Верните число "
                "использованных колонок."
            ),
            "starter": "def usable_prefix(index_cols, conds):\n    pass\n",
            "tests": [
                {"args": [["a", "b", "c"], {"a": "=", "b": "=", "c": "="}], "expected": 3},
                {"args": [["a", "b", "c"], {"a": "=", "c": "="}], "expected": 1},
                {"args": [["a", "b", "c"], {"b": "=", "c": "="}], "expected": 0},
                {"args": [["a", "b", "c"], {"a": "=", "b": "range", "c": "="}], "expected": 2},
                {"args": [["a", "b"], {}], "expected": 0},
                {"args": [["a"], {"a": "range"}], "expected": 1},
                {"args": [[], {"a": "="}], "expected": 0},
                {"args": [["status", "created"], {"status": "=", "created": "range"}], "expected": 2},
            ],
            "hint": "Идите по index_cols; '=' — n += 1, 'range' — вернуть n + 1, всё остальное — выход из цикла.",
        },
        {
            "id": "idx-choose-plan",
            "mode": "func",
            "func": "choose_plan",
            "title": "Индекс или полное чтение",
            "statement": (
                "Напишите функцию choose_plan(table_rows, rows_per_page, matches, "
                "height, random_cost): стоимость полного чтения = число страниц "
                "таблицы (потолок table_rows / rows_per_page); стоимость доступа по "
                "индексу = height + matches · random_cost (каждая подходящая строка "
                "— случайное чтение страницы). Верните 'index', если индекс строго "
                "дешевле, иначе 'seq'."
            ),
            "starter": "def choose_plan(table_rows, rows_per_page, matches, height, random_cost):\n    pass\n",
            "tests": [
                {"args": [1000000, 100, 10, 3, 4], "expected": "index"},
                {"args": [1000000, 100, 5000, 3, 4], "expected": "seq"},
                {"args": [1000000, 100, 2500, 3, 4], "expected": "seq"},
                {"args": [100, 100, 1, 1, 4], "expected": "seq"},
                {"args": [0, 100, 0, 1, 4], "expected": "seq"},
                {"args": [10000, 50, 40, 2, 4], "expected": "index"},
                {"args": [10000, 50, 49, 2, 4], "expected": "index"},
            ],
            "hint": "Сравните два числа: страницы таблицы и height + matches · random_cost.",
        },
    ],
}
