"""Задачи книги «Базы данных»: глава 26."""

TASKS: dict[int, list[dict]] = {26: [{'id': 'd10-month-totals',
  'mode': 'sql',
  'title': 'Выручка по месяцам',
  'statement': 'Выведите выручку (сумма amount) по месяцам: колонки month (формат ГГГГ-ММ) и total, по '
               'месяцам.',
  'starter': '-- выручка по месяцам\nSELECT\n',
  'setup': 'CREATE TABLE dim_product (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);\n'
           'CREATE TABLE dim_client (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE fact_sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, product_id INTEGER NOT NULL '
           'REFERENCES dim_product(id), client_id INTEGER NOT NULL REFERENCES dim_client(id), qty INTEGER '
           'NOT NULL, amount INTEGER NOT NULL);\n'
           'INSERT INTO dim_product VALUES '
           "(1,'Кофе','Напитки'),(2,'Чай','Напитки'),(3,'Печенье','Еда'),(4,'Сыр','Еда'),(5,'Кружка','Посуда');\n"
           'INSERT INTO dim_client VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь');\n"
           'INSERT INTO fact_sales VALUES '
           "(1,'2026-01-05',1,1,2,300),(2,'2026-01-05',3,2,1,80),(3,'2026-01-20',2,1,1,120),(4,'2026-02-02',1,3,3,450),(5,'2026-02-02',5,1,1,500),(6,'2026-02-14',4,2,1,350),(7,'2026-02-14',1,1,1,150),(8,'2026-03-01',3,3,2,160),(9,'2026-03-01',2,4,1,120),(10,'2026-03-09',1,2,2,300),(11,'2026-03-09',5,3,1,500),(12,'2026-03-20',4,1,2,700);\n",
  'expected': [['2026-01', 500], ['2026-02', 1450], ['2026-03', 1780]],
  'expected_cols': ['month', 'total'],
  'hint': 'substr(day, 1, 7) даёт «ГГГГ-ММ»; GROUP BY по этому выражению.',
  'ordered': True},
 {'id': 'd10-star-join',
  'mode': 'sql',
  'title': 'Соединяем звезду',
  'statement': 'Выведите выручку по сочетаниям «категория товара — город клиента»: колонки category, city, '
               'total; по категории, затем по городу.',
  'starter': '-- факты + измерения\nSELECT\n',
  'setup': 'CREATE TABLE dim_product (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);\n'
           'CREATE TABLE dim_client (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE fact_sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, product_id INTEGER NOT NULL '
           'REFERENCES dim_product(id), client_id INTEGER NOT NULL REFERENCES dim_client(id), qty INTEGER '
           'NOT NULL, amount INTEGER NOT NULL);\n'
           'INSERT INTO dim_product VALUES '
           "(1,'Кофе','Напитки'),(2,'Чай','Напитки'),(3,'Печенье','Еда'),(4,'Сыр','Еда'),(5,'Кружка','Посуда');\n"
           'INSERT INTO dim_client VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь');\n"
           'INSERT INTO fact_sales VALUES '
           "(1,'2026-01-05',1,1,2,300),(2,'2026-01-05',3,2,1,80),(3,'2026-01-20',2,1,1,120),(4,'2026-02-02',1,3,3,450),(5,'2026-02-02',5,1,1,500),(6,'2026-02-14',4,2,1,350),(7,'2026-02-14',1,1,1,150),(8,'2026-03-01',3,3,2,160),(9,'2026-03-01',2,4,1,120),(10,'2026-03-09',1,2,2,300),(11,'2026-03-09',5,3,1,500),(12,'2026-03-20',4,1,2,700);\n",
  'expected': [['Еда', 'Казань', 430],
               ['Еда', 'Москва', 860],
               ['Напитки', 'Казань', 300],
               ['Напитки', 'Москва', 1020],
               ['Напитки', 'Тверь', 120],
               ['Посуда', 'Москва', 1000]],
  'expected_cols': ['category', 'city', 'total'],
  'hint': 'Две связи INNER JOIN: к dim_product и к dim_client; группировка по двум столбцам измерений.',
  'ordered': True},
 {'id': 'd10-category-share',
  'mode': 'sql',
  'title': 'Доля категории',
  'statement': 'Для каждой категории выведите долю в общей выручке в процентах, округлённую до целого: '
               'колонки category, pct; по убыванию доли, при равенстве — по названию.',
  'starter': '-- доля категорий\nSELECT\n',
  'setup': 'CREATE TABLE dim_product (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);\n'
           'CREATE TABLE dim_client (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE fact_sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, product_id INTEGER NOT NULL '
           'REFERENCES dim_product(id), client_id INTEGER NOT NULL REFERENCES dim_client(id), qty INTEGER '
           'NOT NULL, amount INTEGER NOT NULL);\n'
           'INSERT INTO dim_product VALUES '
           "(1,'Кофе','Напитки'),(2,'Чай','Напитки'),(3,'Печенье','Еда'),(4,'Сыр','Еда'),(5,'Кружка','Посуда');\n"
           'INSERT INTO dim_client VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь');\n"
           'INSERT INTO fact_sales VALUES '
           "(1,'2026-01-05',1,1,2,300),(2,'2026-01-05',3,2,1,80),(3,'2026-01-20',2,1,1,120),(4,'2026-02-02',1,3,3,450),(5,'2026-02-02',5,1,1,500),(6,'2026-02-14',4,2,1,350),(7,'2026-02-14',1,1,1,150),(8,'2026-03-01',3,3,2,160),(9,'2026-03-01',2,4,1,120),(10,'2026-03-09',1,2,2,300),(11,'2026-03-09',5,3,1,500),(12,'2026-03-20',4,1,2,700);\n",
  'expected': [['Напитки', 39.0], ['Еда', 35.0], ['Посуда', 27.0]],
  'expected_cols': ['category', 'pct'],
  'hint': 'Общую сумму берите скалярным подзапросом, умножайте на 100.0.',
  'ordered': True},
 {'id': 'd10-running-total',
  'mode': 'sql',
  'title': 'Накопительная выручка',
  'statement': 'Выведите по дням выручку за день и накопительный итог: колонки day, daily, running; по дням. '
               'Используйте оконную функцию.',
  'starter': '-- нарастающий итог по дням\nSELECT\n',
  'setup': 'CREATE TABLE dim_product (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);\n'
           'CREATE TABLE dim_client (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE fact_sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, product_id INTEGER NOT NULL '
           'REFERENCES dim_product(id), client_id INTEGER NOT NULL REFERENCES dim_client(id), qty INTEGER '
           'NOT NULL, amount INTEGER NOT NULL);\n'
           'INSERT INTO dim_product VALUES '
           "(1,'Кофе','Напитки'),(2,'Чай','Напитки'),(3,'Печенье','Еда'),(4,'Сыр','Еда'),(5,'Кружка','Посуда');\n"
           'INSERT INTO dim_client VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь');\n"
           'INSERT INTO fact_sales VALUES '
           "(1,'2026-01-05',1,1,2,300),(2,'2026-01-05',3,2,1,80),(3,'2026-01-20',2,1,1,120),(4,'2026-02-02',1,3,3,450),(5,'2026-02-02',5,1,1,500),(6,'2026-02-14',4,2,1,350),(7,'2026-02-14',1,1,1,150),(8,'2026-03-01',3,3,2,160),(9,'2026-03-01',2,4,1,120),(10,'2026-03-09',1,2,2,300),(11,'2026-03-09',5,3,1,500),(12,'2026-03-20',4,1,2,700);\n",
  'expected': [['2026-01-05', 380, 380],
               ['2026-01-20', 120, 500],
               ['2026-02-02', 950, 1450],
               ['2026-02-14', 500, 1950],
               ['2026-03-01', 280, 2230],
               ['2026-03-09', 800, 3030],
               ['2026-03-20', 700, 3730]],
  'expected_cols': ['day', 'daily', 'running'],
  'hint': 'Сначала сверните факты до дня (подзапрос), затем SUM(...) OVER (ORDER BY day).',
  'ordered': True},
 {'id': 'd10-day-diff',
  'mode': 'sql',
  'title': 'Разница с предыдущим днём',
  'statement': 'Для каждого дня, у которого есть предыдущий день с продажами, выведите изменение выручки: '
               'колонки day, delta (выручка дня минус выручка предыдущего дня); по дням.',
  'starter': '-- LAG по дням\nSELECT\n',
  'setup': 'CREATE TABLE dim_product (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);\n'
           'CREATE TABLE dim_client (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE fact_sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, product_id INTEGER NOT NULL '
           'REFERENCES dim_product(id), client_id INTEGER NOT NULL REFERENCES dim_client(id), qty INTEGER '
           'NOT NULL, amount INTEGER NOT NULL);\n'
           'INSERT INTO dim_product VALUES '
           "(1,'Кофе','Напитки'),(2,'Чай','Напитки'),(3,'Печенье','Еда'),(4,'Сыр','Еда'),(5,'Кружка','Посуда');\n"
           'INSERT INTO dim_client VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь');\n"
           'INSERT INTO fact_sales VALUES '
           "(1,'2026-01-05',1,1,2,300),(2,'2026-01-05',3,2,1,80),(3,'2026-01-20',2,1,1,120),(4,'2026-02-02',1,3,3,450),(5,'2026-02-02',5,1,1,500),(6,'2026-02-14',4,2,1,350),(7,'2026-02-14',1,1,1,150),(8,'2026-03-01',3,3,2,160),(9,'2026-03-01',2,4,1,120),(10,'2026-03-09',1,2,2,300),(11,'2026-03-09',5,3,1,500),(12,'2026-03-20',4,1,2,700);\n",
  'expected': [['2026-01-20', -260],
               ['2026-02-02', 830],
               ['2026-02-14', -450],
               ['2026-03-01', -220],
               ['2026-03-09', 520],
               ['2026-03-20', -100]],
  'expected_cols': ['day', 'delta'],
  'hint': 'LAG(daily) OVER (ORDER BY day) даёт предыдущее значение; у первого дня оно NULL — его уберите.',
  'ordered': True},
 {'id': 'd10-top-per-category',
  'mode': 'sql',
  'title': 'Лучший товар категории',
  'statement': 'Для каждой категории выведите товар с наибольшей выручкой: колонки category, name, total; по '
               'категории.',
  'starter': '-- ранг в категории\nSELECT\n',
  'setup': 'CREATE TABLE dim_product (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);\n'
           'CREATE TABLE dim_client (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE fact_sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, product_id INTEGER NOT NULL '
           'REFERENCES dim_product(id), client_id INTEGER NOT NULL REFERENCES dim_client(id), qty INTEGER '
           'NOT NULL, amount INTEGER NOT NULL);\n'
           'INSERT INTO dim_product VALUES '
           "(1,'Кофе','Напитки'),(2,'Чай','Напитки'),(3,'Печенье','Еда'),(4,'Сыр','Еда'),(5,'Кружка','Посуда');\n"
           'INSERT INTO dim_client VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь');\n"
           'INSERT INTO fact_sales VALUES '
           "(1,'2026-01-05',1,1,2,300),(2,'2026-01-05',3,2,1,80),(3,'2026-01-20',2,1,1,120),(4,'2026-02-02',1,3,3,450),(5,'2026-02-02',5,1,1,500),(6,'2026-02-14',4,2,1,350),(7,'2026-02-14',1,1,1,150),(8,'2026-03-01',3,3,2,160),(9,'2026-03-01',2,4,1,120),(10,'2026-03-09',1,2,2,300),(11,'2026-03-09',5,3,1,500),(12,'2026-03-20',4,1,2,700);\n",
  'expected': [['Еда', 'Сыр', 1050], ['Напитки', 'Кофе', 1200], ['Посуда', 'Кружка', 1000]],
  'expected_cols': ['category', 'name', 'total'],
  'hint': 'ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(amount) DESC) поверх группировки по товару.',
  'ordered': True},
 {'id': 'd10-rollup-emulation',
  'mode': 'sql',
  'title': 'Итоги как в ROLLUP',
  'statement': 'В SQLite нет ROLLUP. Выведите выручку по категориям и общий итог одной выборкой: колонки '
               "category, total; последняя строка — category = 'ИТОГО'. Порядок: категории по алфавиту, итог "
               'последним.',
  'starter': '-- итоги по категориям и общий\nSELECT\n',
  'setup': 'CREATE TABLE dim_product (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);\n'
           'CREATE TABLE dim_client (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE fact_sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, product_id INTEGER NOT NULL '
           'REFERENCES dim_product(id), client_id INTEGER NOT NULL REFERENCES dim_client(id), qty INTEGER '
           'NOT NULL, amount INTEGER NOT NULL);\n'
           'INSERT INTO dim_product VALUES '
           "(1,'Кофе','Напитки'),(2,'Чай','Напитки'),(3,'Печенье','Еда'),(4,'Сыр','Еда'),(5,'Кружка','Посуда');\n"
           'INSERT INTO dim_client VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь');\n"
           'INSERT INTO fact_sales VALUES '
           "(1,'2026-01-05',1,1,2,300),(2,'2026-01-05',3,2,1,80),(3,'2026-01-20',2,1,1,120),(4,'2026-02-02',1,3,3,450),(5,'2026-02-02',5,1,1,500),(6,'2026-02-14',4,2,1,350),(7,'2026-02-14',1,1,1,150),(8,'2026-03-01',3,3,2,160),(9,'2026-03-01',2,4,1,120),(10,'2026-03-09',1,2,2,300),(11,'2026-03-09',5,3,1,500),(12,'2026-03-20',4,1,2,700);\n",
  'expected': [['Еда', 1290], ['Напитки', 1440], ['Посуда', 1000], ['ИТОГО', 3730]],
  'expected_cols': ['category', 'total'],
  'hint': 'UNION ALL группировки и общего итога; для порядка добавьте служебный столбец.',
  'ordered': True},
 {'id': 'd10-cohort',
  'mode': 'sql',
  'title': 'Когорты по месяцу первой покупки',
  'statement': 'Для каждого месяца первой покупки (cohort, формат ГГГГ-ММ) выведите число клиентов (clients) '
               'и сколько из них купили ещё и в следующем календарном месяце (returned). Колонки cohort, '
               'clients, returned; по когорте. Месяцы в данных идут подряд (янв, фев, мар).',
  'starter': '-- когорты\nSELECT\n',
  'setup': 'CREATE TABLE dim_product (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);\n'
           'CREATE TABLE dim_client (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE fact_sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, product_id INTEGER NOT NULL '
           'REFERENCES dim_product(id), client_id INTEGER NOT NULL REFERENCES dim_client(id), qty INTEGER '
           'NOT NULL, amount INTEGER NOT NULL);\n'
           'INSERT INTO dim_product VALUES '
           "(1,'Кофе','Напитки'),(2,'Чай','Напитки'),(3,'Печенье','Еда'),(4,'Сыр','Еда'),(5,'Кружка','Посуда');\n"
           'INSERT INTO dim_client VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь');\n"
           'INSERT INTO fact_sales VALUES '
           "(1,'2026-01-05',1,1,2,300),(2,'2026-01-05',3,2,1,80),(3,'2026-01-20',2,1,1,120),(4,'2026-02-02',1,3,3,450),(5,'2026-02-02',5,1,1,500),(6,'2026-02-14',4,2,1,350),(7,'2026-02-14',1,1,1,150),(8,'2026-03-01',3,3,2,160),(9,'2026-03-01',2,4,1,120),(10,'2026-03-09',1,2,2,300),(11,'2026-03-09',5,3,1,500),(12,'2026-03-20',4,1,2,700);\n",
  'expected': [['2026-01', 2, 2], ['2026-02', 1, 1], ['2026-03', 1, 0]],
  'expected_cols': ['cohort', 'clients', 'returned'],
  'hint': 'Сначала месяц первой покупки каждого клиента, затем EXISTS: есть ли у него покупка в месяце '
          "«когорта + 1 месяц» (strftime(..., '+1 month')).",
  'ordered': True},
 {'id': 'd10-funnel',
  'mode': 'sql',
  'title': 'Воронка',
  'statement': "Таблица events(user_id, step, ts): шаги 'view', 'cart', 'pay'. Выведите воронку: число "
               'различных пользователей на каждом шаге — колонки step, users; порядок view, cart, pay.',
  'starter': '-- воронка\nSELECT\n',
  'setup': 'CREATE TABLE events (user_id INTEGER NOT NULL, step TEXT NOT NULL, ts INTEGER NOT NULL);\n'
           'INSERT INTO events VALUES '
           "(1,'view',1),(1,'cart',2),(1,'pay',3),(2,'view',1),(2,'cart',2),(3,'view',1),(4,'view',1),(4,'cart',3),(4,'pay',5),(5,'view',2),(5,'view',3),(6,'cart',1);\n",
  'expected': [['view', 5], ['cart', 4], ['pay', 2]],
  'expected_cols': ['step', 'users'],
  'hint': 'COUNT(DISTINCT user_id) по шагу; порядок задаёт CASE в ORDER BY.',
  'ordered': True},
 {'id': 'd10-scd2-asof',
  'mode': 'sql',
  'title': 'Версия измерения на дату',
  'statement': 'Для каждого заказа выведите город клиента на день заказа (версия, у которой valid_from <= '
               'day < valid_to, а valid_to = NULL означает «действует сейчас»): колонки id, city; по id.',
  'starter': '-- город на дату заказа\nSELECT\n',
  'setup': 'CREATE TABLE dim_client_hist (client_id INTEGER NOT NULL, city TEXT NOT NULL, valid_from TEXT '
           'NOT NULL, valid_to TEXT);\n'
           'INSERT INTO dim_client_hist VALUES '
           "(7,'Казань','2023-01-01','2026-02-01'),(7,'Москва','2026-02-01',NULL),(8,'Тверь','2024-05-01',NULL);\n"
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, client_id INTEGER NOT NULL, day TEXT NOT NULL, '
           'amount INTEGER NOT NULL);\n'
           'INSERT INTO orders VALUES '
           "(1,7,'2026-01-10',100),(2,7,'2026-03-05',200),(3,8,'2026-02-01',50),(4,7,'2026-02-01',70);\n",
  'expected': [[1, 'Казань'], [2, 'Москва'], [3, 'Тверь'], [4, 'Москва']],
  'expected_cols': ['id', 'city'],
  'hint': 'Условие периода в ON: valid_from <= day и (valid_to IS NULL OR day < valid_to).',
  'ordered': True},
 {'id': 'd10-scd2-update',
  'mode': 'sql',
  'title': 'Закрыть версию и добавить новую',
  'statement': "Клиент 7 переехал в Москву 2026-04-01. Закройте текущую версию (valid_to = '2026-04-01') и "
               "добавьте новую с city = 'Москва', valid_from = '2026-04-01', valid_to = NULL. Клиента 8 не "
               'трогайте. Итог проверяется по таблице.',
  'starter': '-- SCD2: закрыть и добавить\n',
  'setup': 'CREATE TABLE dim_client_hist (client_id INTEGER NOT NULL, city TEXT NOT NULL, valid_from TEXT '
           'NOT NULL, valid_to TEXT);\n'
           'INSERT INTO dim_client_hist VALUES '
           "(7,'Казань','2023-01-01',NULL),(8,'Тверь','2024-05-01',NULL);\n",
  'expected': [[7, 'Казань', '2023-01-01', '2026-04-01'],
               [7, 'Москва', '2026-04-01', None],
               [8, 'Тверь', '2024-05-01', None]],
  'expected_cols': ['client_id', 'city', 'valid_from', 'valid_to'],
  'hint': 'Сначала UPDATE только открытой версии клиента 7 (valid_to IS NULL), затем INSERT.',
  'ordered': True,
  'check': 'SELECT client_id, city, valid_from, valid_to FROM dim_client_hist ORDER BY client_id, '
           'valid_from'},
 {'id': 'd10-mv',
  'mode': 'sql',
  'title': 'Материализованная таблица',
  'statement': 'Создайте таблицу mv_daily(day, total) — выручка по дням — командой CREATE TABLE … AS SELECT. '
               'Итог проверяется по её содержимому.',
  'starter': '-- предагрегат по дням\nCREATE TABLE mv_daily AS\n',
  'setup': 'CREATE TABLE dim_product (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);\n'
           'CREATE TABLE dim_client (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE fact_sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, product_id INTEGER NOT NULL '
           'REFERENCES dim_product(id), client_id INTEGER NOT NULL REFERENCES dim_client(id), qty INTEGER '
           'NOT NULL, amount INTEGER NOT NULL);\n'
           'INSERT INTO dim_product VALUES '
           "(1,'Кофе','Напитки'),(2,'Чай','Напитки'),(3,'Печенье','Еда'),(4,'Сыр','Еда'),(5,'Кружка','Посуда');\n"
           'INSERT INTO dim_client VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь');\n"
           'INSERT INTO fact_sales VALUES '
           "(1,'2026-01-05',1,1,2,300),(2,'2026-01-05',3,2,1,80),(3,'2026-01-20',2,1,1,120),(4,'2026-02-02',1,3,3,450),(5,'2026-02-02',5,1,1,500),(6,'2026-02-14',4,2,1,350),(7,'2026-02-14',1,1,1,150),(8,'2026-03-01',3,3,2,160),(9,'2026-03-01',2,4,1,120),(10,'2026-03-09',1,2,2,300),(11,'2026-03-09',5,3,1,500),(12,'2026-03-20',4,1,2,700);\n",
  'expected': [['2026-01-05', 380],
               ['2026-01-20', 120],
               ['2026-02-02', 950],
               ['2026-02-14', 500],
               ['2026-03-01', 280],
               ['2026-03-09', 800],
               ['2026-03-20', 700]],
  'expected_cols': ['day', 'total'],
  'hint': 'CREATE TABLE mv_daily AS SELECT day, SUM(amount) AS total … GROUP BY day.',
  'ordered': True,
  'check': 'SELECT day, total FROM mv_daily ORDER BY day'},
 {'id': 'd10-mv-refresh',
  'mode': 'sql',
  'title': 'Дозагрузка предагрегата',
  'statement': 'В mv лежат суммы по дням, но день d2 пополнился (в fact его сумма 10), а день d3 ещё не '
               'попал. Одним INSERT … ON CONFLICT обновите mv целиком из fact (новые дни вставить, у '
               'существующих обновить total). Итог проверяется по mv.',
  'starter': '-- пересчёт предагрегата\nINSERT INTO mv\n',
  'setup': 'CREATE TABLE fact (id INTEGER PRIMARY KEY, day TEXT NOT NULL, amount INTEGER NOT NULL);\n'
           'CREATE TABLE mv (day TEXT PRIMARY KEY, total INTEGER NOT NULL);\n'
           "INSERT INTO fact VALUES (1,'d1',10),(2,'d1',5),(3,'d2',7),(4,'d2',3),(5,'d3',9);\n"
           "INSERT INTO mv VALUES ('d1',15),('d2',7);\n",
  'expected': [['d1', 15], ['d2', 10], ['d3', 9]],
  'expected_cols': ['day', 'total'],
  'hint': 'INSERT … SELECT … GROUP BY day … ON CONFLICT (day) DO UPDATE SET total = excluded.total; WHERE '
          'true нужен для разбора ON CONFLICT.',
  'ordered': True,
  'check': 'SELECT day, total FROM mv ORDER BY day'},
 {'id': 'd10-dedupe',
  'mode': 'sql',
  'title': 'Дубли в загрузке',
  'statement': 'В stage события по id приходят многократно с разными version. Выведите по одной последней '
               '(наибольшая version) записи на id: колонки id, version, payload; по id.',
  'starter': '-- последняя версия на id\nSELECT\n',
  'setup': 'CREATE TABLE stage (id INTEGER NOT NULL, version INTEGER NOT NULL, payload TEXT NOT NULL);\n'
           "INSERT INTO stage VALUES (1,1,'a'),(1,2,'a2'),(2,1,'b'),(3,1,'c'),(3,3,'c3'),(3,2,'c2');\n",
  'expected': [[1, 2, 'a2'], [2, 1, 'b'], [3, 3, 'c3']],
  'expected_cols': ['id', 'version', 'payload'],
  'hint': 'ROW_NUMBER() OVER (PARTITION BY id ORDER BY version DESC) и фильтр rn = 1.',
  'ordered': True},
 {'id': 'd10-idempotent-load',
  'mode': 'sql',
  'title': 'Идемпотентная загрузка',
  'statement': 'Загрузите stage в sales так, чтобы запуск можно было повторять: новые id вставить, у '
               'существующих обновить day и amount. Итог проверяется по sales.',
  'starter': '-- upsert из stage\nINSERT INTO sales\n',
  'setup': 'CREATE TABLE sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, amount INTEGER NOT NULL);\n'
           'CREATE TABLE stage (id INTEGER PRIMARY KEY, day TEXT NOT NULL, amount INTEGER NOT NULL);\n'
           "INSERT INTO sales VALUES (1,'d1',10),(2,'d1',20),(3,'d2',30);\n"
           "INSERT INTO stage VALUES (2,'d1',25),(3,'d2',30),(4,'d2',40);\n",
  'expected': [[1, 'd1', 10], [2, 'd1', 25], [3, 'd2', 30], [4, 'd2', 40]],
  'expected_cols': ['id', 'day', 'amount'],
  'hint': 'ON CONFLICT (id) DO UPDATE SET … = excluded.…',
  'ordered': True,
  'check': 'SELECT id, day, amount FROM sales ORDER BY id'},
 {'id': 'd10-quality',
  'mode': 'sql',
  'title': 'Проверки качества данных',
  'statement': 'В fact_sales попали плохие строки. Выведите id строк, у которых нет товара в dim_product ИЛИ '
               'qty <= 0 ИЛИ amount < 0. Колонка id, по возрастанию.',
  'starter': '-- плохие строки\nSELECT\n',
  'setup': 'CREATE TABLE dim_product (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);\n'
           'CREATE TABLE dim_client (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE fact_sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, product_id INTEGER NOT NULL '
           'REFERENCES dim_product(id), client_id INTEGER NOT NULL REFERENCES dim_client(id), qty INTEGER '
           'NOT NULL, amount INTEGER NOT NULL);\n'
           'INSERT INTO dim_product VALUES '
           "(1,'Кофе','Напитки'),(2,'Чай','Напитки'),(3,'Печенье','Еда'),(4,'Сыр','Еда'),(5,'Кружка','Посуда');\n"
           'INSERT INTO dim_client VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь');\n"
           'INSERT INTO fact_sales VALUES '
           "(1,'2026-01-05',1,1,2,300),(2,'2026-01-05',3,2,1,80),(3,'2026-01-20',2,1,1,120),(4,'2026-02-02',1,3,3,450),(5,'2026-02-02',5,1,1,500),(6,'2026-02-14',4,2,1,350),(7,'2026-02-14',1,1,1,150),(8,'2026-03-01',3,3,2,160),(9,'2026-03-01',2,4,1,120),(10,'2026-03-09',1,2,2,300),(11,'2026-03-09',5,3,1,500),(12,'2026-03-20',4,1,2,700);\n"
           "INSERT INTO fact_sales VALUES (13,'2026-03-25',99,1,1,100),(14,'2026-03-26',1,1,0,-50);\n",
  'expected': [[13], [14]],
  'expected_cols': ['id'],
  'hint': 'LEFT JOIN к dim_product и проверка p.id IS NULL; плюс условия по qty и amount.',
  'ordered': True},
 {'id': 'd10-top-clients',
  'mode': 'sql',
  'title': 'Лучшие клиенты по городам',
  'statement': 'Для каждого города выведите клиента с наибольшей выручкой: колонки city, name, total; по '
               'городу.',
  'starter': '-- лучший клиент в городе\nSELECT\n',
  'setup': 'CREATE TABLE dim_product (id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL);\n'
           'CREATE TABLE dim_client (id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT NOT NULL);\n'
           'CREATE TABLE fact_sales (id INTEGER PRIMARY KEY, day TEXT NOT NULL, product_id INTEGER NOT NULL '
           'REFERENCES dim_product(id), client_id INTEGER NOT NULL REFERENCES dim_client(id), qty INTEGER '
           'NOT NULL, amount INTEGER NOT NULL);\n'
           'INSERT INTO dim_product VALUES '
           "(1,'Кофе','Напитки'),(2,'Чай','Напитки'),(3,'Печенье','Еда'),(4,'Сыр','Еда'),(5,'Кружка','Посуда');\n"
           'INSERT INTO dim_client VALUES '
           "(1,'Анна','Москва'),(2,'Борис','Казань'),(3,'Вера','Москва'),(4,'Глеб','Тверь');\n"
           'INSERT INTO fact_sales VALUES '
           "(1,'2026-01-05',1,1,2,300),(2,'2026-01-05',3,2,1,80),(3,'2026-01-20',2,1,1,120),(4,'2026-02-02',1,3,3,450),(5,'2026-02-02',5,1,1,500),(6,'2026-02-14',4,2,1,350),(7,'2026-02-14',1,1,1,150),(8,'2026-03-01',3,3,2,160),(9,'2026-03-01',2,4,1,120),(10,'2026-03-09',1,2,2,300),(11,'2026-03-09',5,3,1,500),(12,'2026-03-20',4,1,2,700);\n",
  'expected': [['Казань', 'Борис', 730], ['Москва', 'Анна', 1770], ['Тверь', 'Глеб', 120]],
  'expected_cols': ['city', 'name', 'total'],
  'hint': 'RANK() OVER (PARTITION BY city ORDER BY SUM(amount) DESC) поверх группировки по клиенту.',
  'ordered': True},
 {'id': 'd10-rollup-py',
  'mode': 'func',
  'func': 'rollup_rows',
  'title': 'ROLLUP своими руками',
  'statement': 'Строки — списки [регион, город, сумма]. Напишите rollup_rows(rows): список строк [регион, '
               'город, сумма] в порядке: для каждого региона (по алфавиту) его города (по алфавиту), затем '
               'промежуточный итог [регион, None, сумма региона]; в конце общий итог [None, None, сумма '
               'всех]. Пустой вход — [[None, None, 0]].',
  'starter': 'def rollup_rows(rows):\n    pass\n',
  'tests': [{'args': [[['север', 'Мурманск', 5],
                       ['юг', 'Сочи', 7],
                       ['север', 'Архангельск', 3],
                       ['юг', 'Сочи', 1]]],
             'expected': [['север', 'Архангельск', 3],
                          ['север', 'Мурманск', 5],
                          ['север', None, 8],
                          ['юг', 'Сочи', 8],
                          ['юг', None, 8],
                          [None, None, 16]]},
            {'args': [[]], 'expected': [[None, None, 0]]},
            {'args': [[['a', 'x', 2]]], 'expected': [['a', 'x', 2], ['a', None, 2], [None, None, 2]]}],
  'hint': 'Сначала словарь «регион → город → сумма», затем обход в отсортированном порядке.'},
 {'id': 'd10-rle',
  'mode': 'func',
  'func': 'rle_encode',
  'title': 'Сжатие длинами серий',
  'statement': 'Столбец значений хранится кодированием длин серий. Напишите rle_encode(values): список пар '
               '[значение, длина серии] подряд идущих одинаковых значений; пустой список даёт пустой список.',
  'starter': 'def rle_encode(values):\n    pass\n',
  'tests': [{'args': [['a', 'a', 'b', 'b', 'b', 'a']], 'expected': [['a', 2], ['b', 3], ['a', 1]]},
            {'args': [[]], 'expected': []},
            {'args': [[1, 1, 1, 1]], 'expected': [[1, 4]]},
            {'args': [['x', 'y', 'z']], 'expected': [['x', 1], ['y', 1], ['z', 1]]}],
  'hint': 'Следите за последней парой: то же значение — увеличиваем длину, иначе начинаем новую пару.'},
 {'id': 'd10-rows-to-cols',
  'mode': 'func',
  'func': 'rows_to_cols',
  'title': 'Из строк в столбцы',
  'statement': 'Таблица — список словарей-строк, columns — порядок столбцов. Напишите rows_to_cols(rows, '
               'columns): словарь «столбец → список значений по порядку строк» (отсутствующее значение — '
               'None). Для пустого списка строк — пустые списки.',
  'starter': 'def rows_to_cols(rows, columns):\n    pass\n',
  'tests': [{'args': [[{'id': 1, 'p': 10}, {'id': 2}], ['id', 'p']],
             'expected': {'id': [1, 2], 'p': [10, None]}},
            {'args': [[], ['a']], 'expected': {'a': []}},
            {'args': [[{'x': 1, 'y': 2}], ['y']], 'expected': {'y': [2]}}],
  'hint': 'Для каждого столбца — список значений r.get(c) по строкам.'},
 {'id': 'd10-column-scan',
  'mode': 'func',
  'func': 'scan_cost',
  'title': 'Сколько читаем',
  'statement': 'Таблица: rows строк, width байт в строке всего; запрос читает столбцы общим размером need '
               'байт на строку. Напишите scan_cost(rows, width, need): пару [байт при строчном хранении, '
               'байт при колоночном] (в колоночном без сжатия читаются только нужные столбцы).',
  'starter': 'def scan_cost(rows, width, need):\n    pass\n',
  'tests': [{'args': [1000, 200, 8], 'expected': [200000, 8000]},
            {'args': [0, 100, 4], 'expected': [0, 0]},
            {'args': [10, 50, 50], 'expected': [500, 500]}],
  'hint': 'Строчное хранилище читает всю строку, колоночное — только нужные столбцы.'},
 {'id': 'd10-etl-clean',
  'mode': 'func',
  'func': 'clean_rows',
  'title': 'Очистка перед загрузкой',
  'statement': 'Строки — списки [id, имя, сумма-строкой]. Напишите clean_rows(rows): оставьте строки, у '
               'которых сумма — целое число (допустим знак минус не допускается), имя очищается от пробелов '
               'по краям и приводится к нижнему регистру, сумма — int; повторяющиеся id оставляют только '
               'первую строку. Результат — список [id, имя, сумма] в исходном порядке.',
  'starter': 'def clean_rows(rows):\n    pass\n',
  'tests': [{'args': [[[1, ' Анна ', '100'],
                       [2, 'БОРИС', 'x'],
                       [1, 'Анна', '5'],
                       [3, 'Вера', '-4'],
                       [4, ' Глеб', '0']]],
             'expected': [[1, 'анна', 100], [4, 'глеб', 0]]},
            {'args': [[]], 'expected': []}],
  'hint': 'Проверка str.isdigit(); множество уже виденных id.'},
 {'id': 'd10-partition-replace',
  'mode': 'func',
  'func': 'load_partitions',
  'title': 'Загрузка заменой партиции',
  'statement': 'Склад — словарь «день → список сумм». Новая порция — список пар [день, сумма]. Загрузка '
               'заменой партиций: для каждого дня, который есть в порции, старые данные дня удаляются и '
               'заменяются суммами порции (в порядке порции). Напишите load_partitions(store, batch): новый '
               'словарь; исходный не менять. Повтор той же порции даёт тот же результат.',
  'starter': 'def load_partitions(store, batch):\n    pass\n',
  'tests': [{'args': [{'d1': [1, 2], 'd2': [5]}, [['d2', 7], ['d3', 1], ['d2', 8]]],
             'expected': {'d1': [1, 2], 'd2': [7, 8], 'd3': [1]}},
            {'args': [{}, [['d1', 3]]], 'expected': {'d1': [3]}},
            {'args': [{'d1': [4]}, []], 'expected': {'d1': [4]}}],
  'hint': 'Соберите новые партиции из порции и обновите ими копию склада.'},
 {'id': 'd10-cdc-apply',
  'mode': 'func',
  'func': 'apply_changes',
  'title': 'Применение потока изменений',
  'statement': "События — списки [номер, операция, ключ, значение], операция 'put' или 'del'. Применяйте по "
               'возрастанию номера (даже если пришли вразнобой); событие с уже виденным номером пропускается '
               '(повторная доставка). Напишите apply_changes(events): итоговый словарь «ключ → значение».',
  'starter': 'def apply_changes(events):\n    pass\n',
  'tests': [{'args': [[[2, 'put', 'a', 2],
                       [1, 'put', 'a', 1],
                       [2, 'put', 'a', 2],
                       [3, 'put', 'b', 9],
                       [4, 'del', 'a', None]]],
             'expected': {'b': 9}},
            {'args': [[]], 'expected': {}},
            {'args': [[[1, 'del', 'x', None], [2, 'put', 'x', 5]]], 'expected': {'x': 5}}],
  'hint': 'Сортировка по номеру, множество увиденных номеров; put пишет, del убирает ключ.'},
 {'id': 'd10-scd2-py',
  'mode': 'func',
  'func': 'scd2_apply',
  'title': 'Версии измерения',
  'statement': 'История клиента — список версий [город, с, по] (по = None у текущей), изменения — список '
               '[дата, город] по возрастанию даты. Напишите scd2_apply(history, changes): новую историю — '
               'для каждого изменения с другим городом, чем у текущей версии, текущая закрывается этой '
               'датой, добавляется новая [город, дата, None]; изменение с тем же городом игнорируется. '
               'Исходный список не менять. Даты — строки ГГГГ-ММ-ДД.',
  'starter': 'def scd2_apply(history, changes):\n    pass\n',
  'tests': [{'args': [[['Казань', '2023-01-01', None]],
                      [['2026-04-01', 'Москва'], ['2026-05-01', 'Москва'], ['2026-06-01', 'Тверь']]],
             'expected': [['Казань', '2023-01-01', '2026-04-01'],
                          ['Москва', '2026-04-01', '2026-06-01'],
                          ['Тверь', '2026-06-01', None]]},
            {'args': [[], [['2026-01-01', 'Омск']]], 'expected': [['Омск', '2026-01-01', None]]},
            {'args': [[['Тверь', '2024-01-01', None]], []], 'expected': [['Тверь', '2024-01-01', None]]}],
  'hint': 'Копия истории; у текущей версии закройте «по», затем добавьте новую; одинаковый город '
          'пропустите.'},
 {'id': 'd10-funnel-py',
  'mode': 'func',
  'func': 'funnel',
  'title': 'Воронка конверсии',
  'statement': 'События — списки [пользователь, шаг]. steps — порядок шагов воронки. Пользователь '
               'засчитывается на шаге k, только если он прошёл все шаги до k включительно (в любом порядке '
               'событий). Напишите funnel(events, steps): список числа пользователей на каждом шаге.',
  'starter': 'def funnel(events, steps):\n    pass\n',
  'tests': [{'args': [[[1, 'view'],
                       [1, 'cart'],
                       [1, 'pay'],
                       [2, 'view'],
                       [2, 'cart'],
                       [3, 'view'],
                       [4, 'cart'],
                       [5, 'pay']],
                      ['view', 'cart', 'pay']],
             'expected': [3, 2, 1]},
            {'args': [[], ['a', 'b']], 'expected': [0, 0]}],
  'hint': 'Множество шагов каждого пользователя; на шаге k нужно содержать steps[:k+1].'},
 {'id': 'd10-cohort-py',
  'mode': 'func',
  'func': 'cohort_retention',
  'title': 'Удержание когорты',
  'statement': 'Покупки — списки [клиент, месяц], месяц — целое число 1, 2, 3… Для клиента когорта — его '
               'первый месяц. Напишите cohort_retention(purchases): словарь «когорта (строкой) → список '
               '[клиентов в когорте, из них купивших ещё и в следующем месяце]».',
  'starter': 'def cohort_retention(purchases):\n    pass\n',
  'tests': [{'args': [[['a', 1], ['b', 1], ['a', 2], ['c', 2], ['c', 4], ['b', 3]]],
             'expected': {'1': [2, 1], '2': [1, 0]}},
            {'args': [[]], 'expected': {}}],
  'hint': 'Множество месяцев каждого клиента; когорта — минимум; удержание — наличие минимума + 1.'},
 {'id': 'd10-pick-store',
  'mode': 'func',
  'func': 'pick_store',
  'title': 'Куда класть нагрузку',
  'statement': "Напишите pick_store(qps, rows_per_query, point_lookup): 'OLTP', если запросов много (qps >= "
               "100) и они точечные (point_lookup True) и читают не более 100 строк; 'OLAP', если запросов "
               "мало (qps < 100) и каждый читает не менее 100000 строк; иначе 'reduce' (пересмотреть "
               'нагрузку).',
  'starter': 'def pick_store(qps, rows_per_query, point_lookup):\n    pass\n',
  'tests': [{'args': [500, 3, True], 'expected': 'OLTP'},
            {'args': [2, 5000000, False], 'expected': 'OLAP'},
            {'args': [50, 10, True], 'expected': 'reduce'},
            {'args': [500, 100000, False], 'expected': 'reduce'},
            {'args': [99, 100000, False], 'expected': 'OLAP'}],
  'hint': 'Два условия и ветка по умолчанию.'}]}
