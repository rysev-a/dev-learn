"""Задачи книги «Базы данных»: глава 17."""

TASKS: dict[int, list[dict]] = {17: [{'id': 'd1-projection',
  'mode': 'sql',
  'title': 'Проекция: нужные столбцы',
  'statement': 'Таблица customers(id, name, city). Выведите имя и город всех клиентов по возрастанию id '
               '(колонки: name, city).',
  'starter': '-- имя и город всех клиентов\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['Анна', 'Москва'],
               ['Борис', 'Казань'],
               ['Вера', 'Москва'],
               ['Глеб', 'Тверь'],
               ['Дарья', 'Казань'],
               ['Егор', 'Москва']],
  'expected_cols': ['name', 'city'],
  'hint': 'Перечислите нужные столбцы после SELECT, таблицу — после FROM; порядок задаёт ORDER BY.',
  'ordered': True},
 {'id': 'd1-filter-sort',
  'mode': 'sql',
  'title': 'Выборка: WHERE и ORDER BY',
  'statement': 'Таблица products(id, title, category, price). Выведите название и цену товаров дороже 1000 '
               'рублей, самые дорогие — первыми (колонки: title, price).',
  'starter': '-- товары дороже 1000, по убыванию цены\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['Ноутбук', 70000], ['Наушники', 5000], ['Мышь', 1500]],
  'expected_cols': ['title', 'price'],
  'hint': 'WHERE price > 1000 ORDER BY price DESC.',
  'ordered': True},
 {'id': 'd1-between-like',
  'mode': 'sql',
  'title': 'Диапазон и шаблон',
  'statement': 'Выведите названия товаров, цена которых от 500 до 5000 включительно и в названии которых '
               'есть буква «о» (строчная). Колонка title, порядок по возрастанию id.',
  'starter': '-- цена от 500 до 5000 и «о» в названии\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['Кофе']],
  'expected_cols': ['title'],
  'hint': "BETWEEN включает обе границы; LIKE '%о%' — «о» в любом месте. Учтите: в SQLite LIKE не различает "
          'регистр только для латиницы.',
  'ordered': True},
 {'id': 'd1-distinct',
  'mode': 'sql',
  'title': 'Без повторов',
  'statement': 'Выведите список городов, в которых живут клиенты, без повторов, по алфавиту. Колонка city.',
  'starter': '-- города без повторов\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['Казань'], ['Москва'], ['Тверь']],
  'expected_cols': ['city'],
  'hint': 'SELECT DISTINCT city … ORDER BY city.',
  'ordered': True},
 {'id': 'd1-limit-offset',
  'mode': 'sql',
  'title': 'Вторая по цене позиция',
  'statement': 'Выведите название самого дорогого товара без учёта первого места, то есть вторую по цене '
               'позицию (ровно одна строка, колонка title).',
  'starter': '-- второй по цене товар\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['Наушники']],
  'expected_cols': ['title'],
  'hint': 'ORDER BY price DESC, затем LIMIT 1 OFFSET 1: пропустить одну строку и взять следующую.',
  'ordered': True},
 {'id': 'd1-is-null',
  'mode': 'sql',
  'title': 'Нет начальника',
  'statement': 'Таблица employees(id, name, dept, manager_id, bonus, salary). У кого нет начальника '
               '(manager_id не задан)? Выведите name.',
  'starter': '-- сотрудники без начальника\nSELECT\n',
  'setup': 'CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept TEXT NOT NULL, '
           'manager_id INTEGER REFERENCES employees(id), bonus INTEGER, salary INTEGER NOT NULL);\n'
           'INSERT INTO employees VALUES '
           "(1,'Игорь','mgmt',NULL,NULL,300),(2,'Ольга','dev',1,50,200),(3,'Павел','dev',2,NULL,150),(4,'Рита','dev',2,30,160),(5,'Семён','ops',1,NULL,140),(6,'Тая','ops',5,10,130);\n",
  'expected': [['Игорь']],
  'expected_cols': ['name'],
  'hint': 'Сравнение manager_id = NULL никогда не сработает: нужен IS NULL.'},
 {'id': 'd1-coalesce',
  'mode': 'sql',
  'title': 'COALESCE: пропуски в премии',
  'statement': 'Выведите имя и премию каждого сотрудника, а пропуск (NULL) в премии заменяйте нулём. '
               'Колонки: name, bonus; порядок по id.',
  'starter': '-- имя и премия (NULL → 0)\nSELECT\n',
  'setup': 'CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept TEXT NOT NULL, '
           'manager_id INTEGER REFERENCES employees(id), bonus INTEGER, salary INTEGER NOT NULL);\n'
           'INSERT INTO employees VALUES '
           "(1,'Игорь','mgmt',NULL,NULL,300),(2,'Ольга','dev',1,50,200),(3,'Павел','dev',2,NULL,150),(4,'Рита','dev',2,30,160),(5,'Семён','ops',1,NULL,140),(6,'Тая','ops',5,10,130);\n",
  'expected': [['Игорь', 0], ['Ольга', 50], ['Павел', 0], ['Рита', 30], ['Семён', 0], ['Тая', 10]],
  'expected_cols': ['name', 'bonus'],
  'hint': 'COALESCE(bonus, 0) возвращает первое значение, не равное NULL.',
  'ordered': True},
 {'id': 'd1-count-null',
  'mode': 'sql',
  'title': 'COUNT(*) и COUNT(столбец)',
  'statement': 'Одним запросом выведите две колонки: сколько всего сотрудников (total) и у скольких задана '
               'премия (with_bonus).',
  'starter': '-- total и with_bonus\nSELECT\n',
  'setup': 'CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept TEXT NOT NULL, '
           'manager_id INTEGER REFERENCES employees(id), bonus INTEGER, salary INTEGER NOT NULL);\n'
           'INSERT INTO employees VALUES '
           "(1,'Игорь','mgmt',NULL,NULL,300),(2,'Ольга','dev',1,50,200),(3,'Павел','dev',2,NULL,150),(4,'Рита','dev',2,30,160),(5,'Семён','ops',1,NULL,140),(6,'Тая','ops',5,10,130);\n",
  'expected': [[6, 3]],
  'expected_cols': ['total', 'with_bonus'],
  'hint': 'COUNT(*) считает все строки, а COUNT(bonus) пропускает NULL.'},
 {'id': 'd1-not-in-trap',
  'mode': 'sql',
  'title': 'NOT IN и NULL',
  'statement': 'В таблице a числа 1, 2, 3, 4, в таблице b — 2, NULL и 4. Выведите те x из a, которых нет в b '
               '(колонка x). Запрос с NOT IN вернёт пусто из-за NULL — подберите корректный.',
  'starter': '-- x из a, которых нет в b (с учётом NULL в b)\nSELECT\n',
  'setup': 'CREATE TABLE a (x INTEGER);\n'
           'CREATE TABLE b (y INTEGER);\n'
           'INSERT INTO a VALUES (1),(2),(3),(4);\n'
           'INSERT INTO b VALUES (2),(NULL),(4);\n',
  'expected': [[1], [3]],
  'expected_cols': ['x'],
  'hint': 'NOT EXISTS с коррелированным подзапросом не страдает от NULL в b; можно и NOT IN (SELECT y FROM b '
          'WHERE y IS NOT NULL).'},
 {'id': 'd1-create-constraints',
  'mode': 'sql',
  'title': 'Ограничения в таблице',
  'statement': 'Создайте таблицу accounts: id — целочисленный первичный ключ; owner — текст, обязателен; '
               'balance — целое, обязательно, не меньше нуля (CHECK). Таблица должна называться accounts, '
               'столбцы — в этом порядке.',
  'starter': '-- создайте таблицу accounts\nCREATE TABLE accounts (\n\n);\n',
  'setup': '',
  'expected': [['id', 'INTEGER', 0, 1], ['owner', 'TEXT', 1, 0], ['balance', 'INTEGER', 1, 0]],
  'expected_cols': ['name', 'type', 'notnull', 'pk'],
  'hint': 'id INTEGER PRIMARY KEY, owner TEXT NOT NULL, balance INTEGER NOT NULL CHECK (balance >= 0).',
  'check': 'SELECT name, type, "notnull", pk FROM pragma_table_info(\'accounts\') ORDER BY cid'},
 {'id': 'd1-foreign-key',
  'mode': 'sql',
  'title': 'Внешний ключ',
  'statement': 'Создайте таблицу invoices: id — первичный ключ, customer_id — целое, обязательное и '
               'ссылается на customers(id), amount — целое. Столбцы — в этом порядке.',
  'starter': '-- таблица invoices с внешним ключом на customers\nCREATE TABLE invoices (\n\n);\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL);\n',
  'expected': [['customers', 'customer_id', 'id']],
  'expected_cols': ['table', 'from', 'to'],
  'hint': 'customer_id INTEGER NOT NULL REFERENCES customers(id) — внешний ключ в описании столбца.',
  'check': 'SELECT "table", "from", "to" FROM pragma_foreign_key_list(\'invoices\')'},
 {'id': 'd1-inner-join',
  'mode': 'sql',
  'title': 'Соединение: клиент и заказ',
  'statement': "Выведите имя клиента и дату заказа для всех оплаченных заказов (status = 'paid') по "
               'возрастанию даты, при равенстве — по имени. Колонки: name, created.',
  'starter': '-- имя клиента и дата оплаченных заказов\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['Анна', '2024-01-05'],
               ['Анна', '2024-02-10'],
               ['Вера', '2024-03-01'],
               ['Вера', '2024-03-15'],
               ['Дарья', '2024-04-03'],
               ['Борис', '2024-04-20']],
  'expected_cols': ['name', 'created'],
  'hint': 'orders JOIN customers ON customers.id = orders.customer_id.',
  'ordered': True},
 {'id': 'd1-three-way-join',
  'mode': 'sql',
  'title': 'Три таблицы: что купил клиент',
  'statement': 'Выведите имена клиентов и названия товаров, которые они купили в оплаченных заказах, без '
               'повторов пар «клиент — товар». Колонки: name, title; порядок по имени, затем по названию.',
  'starter': '-- клиент и товар в оплаченных заказах\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['Анна', 'Книга SQL'],
               ['Анна', 'Кофе'],
               ['Анна', 'Мышь'],
               ['Анна', 'Ноутбук'],
               ['Борис', 'Мышь'],
               ['Борис', 'Наушники'],
               ['Вера', 'Книга SQL'],
               ['Вера', 'Кофе'],
               ['Вера', 'Наушники'],
               ['Вера', 'Ноутбук'],
               ['Дарья', 'Кофе'],
               ['Дарья', 'Чай']],
  'expected_cols': ['name', 'title'],
  'hint': 'Цепочка: customers → orders → order_items → products; DISTINCT уберёт повторы пар.',
  'ordered': True},
 {'id': 'd1-join-multiply',
  'mode': 'sql',
  'title': 'Соединение размножает строки',
  'statement': 'Сколько строк получится, если соединить orders с order_items по order_id и ничего не '
               'отфильтровать? Выведите одно число в колонке n.',
  'starter': '-- число строк после соединения orders и order_items\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [[14]],
  'expected_cols': ['n'],
  'hint': 'Каждый заказ повторяется столько раз, сколько у него позиций: COUNT(*) после JOIN.'},
 {'id': 'd1-left-anti',
  'mode': 'sql',
  'title': 'Клиенты без заказов',
  'statement': 'Найдите клиентов, у которых нет ни одного заказа, через LEFT JOIN. Выведите одну колонку '
               'name.',
  'starter': '-- клиенты без заказов\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['Глеб'], ['Егор']],
  'expected_cols': ['name'],
  'hint': 'После LEFT JOIN у клиентов без заказов столбцы orders равны NULL: WHERE o.id IS NULL.'},
 {'id': 'd1-left-on-vs-where',
  'mode': 'sql',
  'title': 'LEFT JOIN: условие в ON',
  'statement': "Для каждого клиента выведите число его оплаченных заказов (status = 'paid'), включая "
               'клиентов, у которых их нет (тогда 0). Колонки: name, paid; порядок по id клиента. Условие по '
               'заказам нужно в ON, а не в WHERE.',
  'starter': '-- клиенты и число оплаченных заказов (в том числе 0)\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['Анна', 2], ['Борис', 1], ['Вера', 2], ['Глеб', 0], ['Дарья', 1], ['Егор', 0]],
  'expected_cols': ['name', 'paid'],
  'hint': "COUNT(o.id) не считает NULL; условие o.status = 'paid' в ON сохраняет клиентов без оплаченных "
          'заказов.',
  'ordered': True},
 {'id': 'd1-group-having',
  'mode': 'sql',
  'title': 'HAVING: активные клиенты',
  'statement': 'Выведите id клиентов, у которых не меньше двух заказов, и число заказов (колонки: '
               'customer_id, n).',
  'starter': '-- клиенты с двумя и более заказами\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [[1, 2], [2, 2], [3, 3]],
  'expected_cols': ['customer_id', 'n'],
  'hint': 'GROUP BY customer_id HAVING COUNT(*) >= 2.'},
 {'id': 'd1-revenue-by-category',
  'mode': 'sql',
  'title': 'Выручка по категориям',
  'statement': 'Посчитайте выручку по категориям товаров — сумму qty × price — только по оплаченным заказам. '
               'Колонки: category, revenue; порядок по убыванию выручки.',
  'starter': '-- выручка по категориям (paid)\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['tech', 159500], ['food', 5600], ['books', 2700]],
  'expected_cols': ['category', 'revenue'],
  'hint': "Соедините order_items, orders и products; WHERE o.status = 'paid'; GROUP BY p.category.",
  'ordered': True},
 {'id': 'd1-above-average',
  'mode': 'sql',
  'title': 'Скалярный подзапрос',
  'statement': 'Выведите названия товаров, цена которых выше средней цены всех товаров. Колонка title, '
               'порядок по id.',
  'starter': '-- товары дороже средней цены\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['Ноутбук']],
  'expected_cols': ['title'],
  'hint': 'Средняя цена — подзапрос в скобках: price > (SELECT AVG(price) FROM products).',
  'ordered': True},
 {'id': 'd1-exists',
  'mode': 'sql',
  'title': 'EXISTS: есть оплаченный заказ',
  'statement': 'Выведите имена клиентов, у которых есть хотя бы один оплаченный заказ, через EXISTS. Колонка '
               'name, порядок по id.',
  'starter': '-- клиенты с оплаченным заказом\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['Анна'], ['Борис'], ['Вера'], ['Дарья']],
  'expected_cols': ['name'],
  'hint': "Коррелированный подзапрос: WHERE o.customer_id = c.id AND o.status = 'paid'.",
  'ordered': True},
 {'id': 'd1-cte-no-multiply',
  'mode': 'sql',
  'title': 'Свернуть до соединения',
  'statement': 'Для каждого оплаченного заказа выведите число позиций (items = сумма qty) и сумму платежей '
               '(paid_sum). Если соединить обе таблицы напрямую, суммы удвоятся: сначала сверните каждую '
               'ветку отдельно (WITH или подзапросы). Колонки: id, items, paid_sum; только заказы, по '
               'которым есть и позиции, и платежи; порядок по id.',
  'starter': '-- по оплаченным заказам: items и paid_sum без размножения строк\nWITH\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n'
           'CREATE TABLE payments (order_id INTEGER NOT NULL REFERENCES orders(id), amount INTEGER NOT '
           'NULL);\n'
           'INSERT INTO payments VALUES (1,50),(1,20),(2,30),(4,100),(4,100),(4,5),(5,40);\n',
  'expected': [[1, 3, 70], [2, 4, 30], [4, 2, 205], [5, 3, 40]],
  'expected_cols': ['id', 'items', 'paid_sum'],
  'hint': 'Каждый CTE даёт одну строку на заказ; JOIN сворачивающих запросов уже не размножает строки.',
  'ordered': True},
 {'id': 'd1-update-returning',
  'mode': 'sql',
  'title': 'UPDATE … RETURNING',
  'statement': "Поднимите цену всех товаров категории 'tech' на 10 % (в целых рублях: price = price * 11 / "
               '10) и верните изменённые строки: id и новую цену (колонки: id, price), по возрастанию id.',
  'starter': '-- поднять цену tech на 10 % и вернуть id, price\nUPDATE\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [[1, 77000], [2, 1650], [6, 5500]],
  'expected_cols': ['id', 'price'],
  'hint': 'RETURNING id, price в конце UPDATE возвращает изменённые строки. Не забудьте WHERE category = '
          "'tech'."},
 {'id': 'd1-upsert',
  'mode': 'sql',
  'title': 'UPSERT: ON CONFLICT',
  'statement': 'Склад stock(id, qty). Придёт поставка: товару 2 — ещё 7 штук, товару 3 — 4 штуки (его на '
               'складе пока нет). Одним INSERT … ON CONFLICT выполните обе вставки так, чтобы для '
               'существующего товара количество увеличилось. Итог проверяется по таблице.',
  'starter': '-- поставка: (2, 7) и (3, 4) через INSERT ... ON CONFLICT\n'
             'INSERT INTO stock (id, qty) VALUES\n',
  'setup': 'CREATE TABLE stock (id INTEGER PRIMARY KEY, qty INTEGER NOT NULL);\n'
           'INSERT INTO stock VALUES (1,10),(2,5);\n',
  'expected': [[1, 10], [2, 12], [3, 4]],
  'expected_cols': ['id', 'qty'],
  'hint': 'ON CONFLICT (id) DO UPDATE SET qty = qty + excluded.qty; excluded — вставляемая строка.',
  'ordered': True,
  'check': 'SELECT id, qty FROM stock ORDER BY id'},
 {'id': 'd1-delete-check',
  'mode': 'sql',
  'title': 'Безопасное удаление',
  'statement': "Удалите отменённые заказы (status = 'cancelled') вместе с их позициями: сначала позиции, "
               'потом сами заказы. Итог проверяется по числу строк в orders и order_items.',
  'starter': '-- удалить cancelled-заказы и их позиции\nDELETE\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [[7, 13]],
  'expected_cols': ['(SELECT COUNT(*) FROM orders)', '(SELECT COUNT(*) FROM order_items)'],
  'hint': 'Порядок важен из-за внешнего ключа: сначала order_items с подзапросом по orders, затем orders.',
  'check': 'SELECT (SELECT COUNT(*) FROM orders), (SELECT COUNT(*) FROM order_items)'},
 {'id': 'd1-case-when',
  'mode': 'sql',
  'title': 'CASE: ценовые категории',
  'statement': "Для каждого товара выведите название и ценовую категорию: 'дорого' при цене от 5000, "
               "'средне' от 1000 до 4999, иначе 'дёшево'. Колонки: title, tier; порядок по id.",
  'starter': '-- название и категория цены\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE products (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, '
           'price INTEGER NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES '
           'customers(id), created TEXT NOT NULL, status TEXT NOT NULL);\n'
           'CREATE TABLE order_items (order_id INTEGER NOT NULL REFERENCES orders(id), product_id INTEGER '
           'NOT NULL REFERENCES products(id), qty INTEGER NOT NULL, PRIMARY KEY (order_id, product_id));\n'
           'INSERT INTO customers VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь'),(5,'Дарья','Казань'),(6,'Егор','Москва');\n"
           "INSERT INTO products VALUES (1,'Ноутбук','tech',70000),(2,'Мышь','tech',1500),(3,'Книга "
           "SQL','books',900),(4,'Кофе','food',600),(5,'Чай','food',400),(6,'Наушники','tech',5000);\n"
           'INSERT INTO orders VALUES '
           "(1,1,'2024-01-05','paid'),(2,1,'2024-02-10','paid'),(3,2,'2024-02-11','cancelled'),(4,3,'2024-03-01','paid'),(5,3,'2024-03-15','paid'),(6,3,'2024-04-02','new'),(7,5,'2024-04-03','paid'),(8,2,'2024-04-20','paid');\n"
           'INSERT INTO order_items VALUES '
           '(1,1,1),(1,2,2),(2,3,1),(2,4,3),(3,5,2),(4,1,1),(4,6,1),(5,3,2),(5,4,1),(6,2,1),(7,5,5),(7,4,2),(8,6,2),(8,2,1);\n',
  'expected': [['Ноутбук', 'дорого'],
               ['Мышь', 'средне'],
               ['Книга SQL', 'дёшево'],
               ['Кофе', 'дёшево'],
               ['Чай', 'дёшево'],
               ['Наушники', 'дорого']],
  'expected_cols': ['title', 'tier'],
  'hint': 'CASE WHEN … THEN … WHEN … THEN … ELSE … END; ветви проверяются сверху вниз.',
  'ordered': True}]}
