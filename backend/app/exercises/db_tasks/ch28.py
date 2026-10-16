"""Задачи книги «Базы данных»: глава 28."""

TASKS: dict[int, list[dict]] = {28: [{'id': 'd12-cte-top-clients',
  'mode': 'sql',
  'title': 'Лучшие через CTE',
  'statement': 'Через WITH найдите отделы со средней зарплатой выше общей средней: колонки dept, avg_sal '
               '(целое, ROUND), по названию отдела.',
  'starter': '-- WITH + сравнение со средним\nWITH\n',
  'setup': 'CREATE TABLE emp (id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept TEXT NOT NULL, boss_id '
           'INTEGER, salary INTEGER NOT NULL);\n'
           'INSERT INTO emp VALUES '
           "(1,'Ольга','IT',NULL,500),(2,'Игорь','IT',1,300),(3,'Мария','IT',1,300),(4,'Пётр','IT',2,200),(5,'Нина','HR',1,250),(6,'Олег','HR',5,150),(7,'Сергей','Sales',1,280),(8,'Аня','Sales',7,180),(9,'Лев','Sales',7,180),(10,'Ира','Sales',8,120);\n",
  'expected': [['IT', 325.0]],
  'expected_cols': ['dept', 'avg_sal'],
  'hint': 'Общее выражение со средним по отделам и подзапрос со средним по всем.',
  'ordered': True},
 {'id': 'd12-window-share',
  'mode': 'sql',
  'title': 'Доля в отделе',
  'statement': 'Для каждого сотрудника выведите его долю зарплаты в отделе в процентах (округлить до '
               'целого): колонки name, dept, pct; по dept, затем по name.',
  'starter': '-- SUM() OVER\nSELECT\n',
  'setup': 'CREATE TABLE emp (id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept TEXT NOT NULL, boss_id '
           'INTEGER, salary INTEGER NOT NULL);\n'
           'INSERT INTO emp VALUES '
           "(1,'Ольга','IT',NULL,500),(2,'Игорь','IT',1,300),(3,'Мария','IT',1,300),(4,'Пётр','IT',2,200),(5,'Нина','HR',1,250),(6,'Олег','HR',5,150),(7,'Сергей','Sales',1,280),(8,'Аня','Sales',7,180),(9,'Лев','Sales',7,180),(10,'Ира','Sales',8,120);\n",
  'expected': [['Нина', 'HR', 63.0],
               ['Олег', 'HR', 38.0],
               ['Игорь', 'IT', 23.0],
               ['Мария', 'IT', 23.0],
               ['Ольга', 'IT', 38.0],
               ['Пётр', 'IT', 15.0],
               ['Аня', 'Sales', 24.0],
               ['Ира', 'Sales', 16.0],
               ['Лев', 'Sales', 24.0],
               ['Сергей', 'Sales', 37.0]],
  'expected_cols': ['name', 'dept', 'pct'],
  'hint': 'SUM(salary) OVER (PARTITION BY dept) в знаменателе.',
  'ordered': True},
 {'id': 'd12-row-number-top',
  'mode': 'sql',
  'title': 'Топ-2 в отделе',
  'statement': 'Для каждого отдела выведите двух самых высокооплачиваемых; при равной зарплате первым идёт '
               'меньший id. Колонки dept, name, salary; по dept, затем по убыванию зарплаты и id.',
  'starter': '-- ROW_NUMBER по отделу\nSELECT\n',
  'setup': 'CREATE TABLE emp (id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept TEXT NOT NULL, boss_id '
           'INTEGER, salary INTEGER NOT NULL);\n'
           'INSERT INTO emp VALUES '
           "(1,'Ольга','IT',NULL,500),(2,'Игорь','IT',1,300),(3,'Мария','IT',1,300),(4,'Пётр','IT',2,200),(5,'Нина','HR',1,250),(6,'Олег','HR',5,150),(7,'Сергей','Sales',1,280),(8,'Аня','Sales',7,180),(9,'Лев','Sales',7,180),(10,'Ира','Sales',8,120);\n",
  'expected': [['HR', 'Нина', 250],
               ['HR', 'Олег', 150],
               ['IT', 'Ольга', 500],
               ['IT', 'Игорь', 300],
               ['Sales', 'Сергей', 280],
               ['Sales', 'Аня', 180]],
  'expected_cols': ['dept', 'name', 'salary'],
  'hint': 'ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC, id) и фильтр rn <= 2 снаружи.',
  'ordered': True},
 {'id': 'd12-rank-ties',
  'mode': 'sql',
  'title': 'RANK и DENSE_RANK',
  'statement': 'Выведите сотрудников с их рангом по зарплате внутри отдела без пропусков при равенстве '
               '(DENSE_RANK, по убыванию зарплаты): колонки name, dept, r; по dept, r, name.',
  'starter': '-- DENSE_RANK\nSELECT\n',
  'setup': 'CREATE TABLE emp (id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept TEXT NOT NULL, boss_id '
           'INTEGER, salary INTEGER NOT NULL);\n'
           'INSERT INTO emp VALUES '
           "(1,'Ольга','IT',NULL,500),(2,'Игорь','IT',1,300),(3,'Мария','IT',1,300),(4,'Пётр','IT',2,200),(5,'Нина','HR',1,250),(6,'Олег','HR',5,150),(7,'Сергей','Sales',1,280),(8,'Аня','Sales',7,180),(9,'Лев','Sales',7,180),(10,'Ира','Sales',8,120);\n",
  'expected': [['Нина', 'HR', 1],
               ['Олег', 'HR', 2],
               ['Ольга', 'IT', 1],
               ['Игорь', 'IT', 2],
               ['Мария', 'IT', 2],
               ['Пётр', 'IT', 3],
               ['Сергей', 'Sales', 1],
               ['Аня', 'Sales', 2],
               ['Лев', 'Sales', 2],
               ['Ира', 'Sales', 3]],
  'expected_cols': ['name', 'dept', 'r'],
  'hint': 'DENSE_RANK() OVER (PARTITION BY dept ORDER BY salary DESC).',
  'ordered': True},
 {'id': 'd12-lag-growth',
  'mode': 'sql',
  'title': 'Рост по дням',
  'statement': 'Для региона N выведите изменение выручки по сравнению с предыдущим днём: колонки day, '
               'amount, delta (NULL у первого дня); по дням.',
  'starter': '-- LAG\nSELECT\n',
  'setup': 'CREATE TABLE sales (id INTEGER PRIMARY KEY, day INTEGER NOT NULL, region TEXT NOT NULL, amount '
           'INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'INSERT INTO sales VALUES '
           "(1,1,'N',100,'ok'),(2,2,'N',150,'ok'),(3,3,'N',120,'cancelled'),(4,4,'N',200,'ok'),(5,1,'S',80,'ok'),(6,2,'S',90,'cancelled'),(7,3,'S',110,'ok'),(8,5,'S',60,'ok');\n",
  'expected': [[1, 100, None], [2, 150, 50], [3, 120, -30], [4, 200, 80]],
  'expected_cols': ['day', 'amount', 'delta'],
  'hint': "LAG(amount) OVER (ORDER BY day); фильтр region = 'N' в WHERE.",
  'ordered': True},
 {'id': 'd12-running-total',
  'mode': 'sql',
  'title': 'Накопительная сумма по регионам',
  'statement': 'Выведите накопительную выручку по дням внутри каждого региона: колонки region, day, total; '
               'по региону и дню.',
  'starter': '-- накопительная сумма\nSELECT\n',
  'setup': 'CREATE TABLE sales (id INTEGER PRIMARY KEY, day INTEGER NOT NULL, region TEXT NOT NULL, amount '
           'INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'INSERT INTO sales VALUES '
           "(1,1,'N',100,'ok'),(2,2,'N',150,'ok'),(3,3,'N',120,'cancelled'),(4,4,'N',200,'ok'),(5,1,'S',80,'ok'),(6,2,'S',90,'cancelled'),(7,3,'S',110,'ok'),(8,5,'S',60,'ok');\n",
  'expected': [['N', 1, 100],
               ['N', 2, 250],
               ['N', 3, 370],
               ['N', 4, 570],
               ['S', 1, 80],
               ['S', 2, 170],
               ['S', 3, 280],
               ['S', 5, 340]],
  'expected_cols': ['region', 'day', 'total'],
  'hint': 'SUM(amount) OVER (PARTITION BY region ORDER BY day).',
  'ordered': True},
 {'id': 'd12-moving-avg',
  'mode': 'sql',
  'title': 'Скользящее среднее',
  'statement': 'Для региона N выведите скользящее среднее суммы за текущий и два предыдущих дня (ROUND до '
               'целого): колонки day, avg3; по дням.',
  'starter': '-- рамка ROWS\nSELECT\n',
  'setup': 'CREATE TABLE sales (id INTEGER PRIMARY KEY, day INTEGER NOT NULL, region TEXT NOT NULL, amount '
           'INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'INSERT INTO sales VALUES '
           "(1,1,'N',100,'ok'),(2,2,'N',150,'ok'),(3,3,'N',120,'cancelled'),(4,4,'N',200,'ok'),(5,1,'S',80,'ok'),(6,2,'S',90,'cancelled'),(7,3,'S',110,'ok'),(8,5,'S',60,'ok');\n",
  'expected': [[1, 100.0], [2, 125.0], [3, 123.0], [4, 157.0]],
  'expected_cols': ['day', 'avg3'],
  'hint': 'AVG(amount) OVER (ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW).',
  'ordered': True},
 {'id': 'd12-pivot',
  'mode': 'sql',
  'title': 'Сводная таблица',
  'statement': 'Одной строкой выведите выручку регионов N и S по неотменённым продажам: колонки n_total, '
               's_total. Используйте условную агрегацию.',
  'starter': '-- SUM(CASE ...)\nSELECT\n',
  'setup': 'CREATE TABLE sales (id INTEGER PRIMARY KEY, day INTEGER NOT NULL, region TEXT NOT NULL, amount '
           'INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'INSERT INTO sales VALUES '
           "(1,1,'N',100,'ok'),(2,2,'N',150,'ok'),(3,3,'N',120,'cancelled'),(4,4,'N',200,'ok'),(5,1,'S',80,'ok'),(6,2,'S',90,'cancelled'),(7,3,'S',110,'ok'),(8,5,'S',60,'ok');\n",
  'expected': [[450, 250]],
  'expected_cols': ['n_total', 's_total'],
  'hint': 'Два SUM(CASE WHEN … THEN amount ELSE 0 END).'},
 {'id': 'd12-filter',
  'mode': 'sql',
  'title': 'FILTER',
  'statement': 'Для каждого региона выведите число продаж (n) и число отменённых (cancelled) с помощью '
               'COUNT(*) FILTER (WHERE …): колонки region, n, cancelled; по региону.',
  'starter': '-- COUNT(*) FILTER\nSELECT\n',
  'setup': 'CREATE TABLE sales (id INTEGER PRIMARY KEY, day INTEGER NOT NULL, region TEXT NOT NULL, amount '
           'INTEGER NOT NULL, status TEXT NOT NULL);\n'
           'INSERT INTO sales VALUES '
           "(1,1,'N',100,'ok'),(2,2,'N',150,'ok'),(3,3,'N',120,'cancelled'),(4,4,'N',200,'ok'),(5,1,'S',80,'ok'),(6,2,'S',90,'cancelled'),(7,3,'S',110,'ok'),(8,5,'S',60,'ok');\n",
  'expected': [['N', 4, 1], ['S', 4, 1]],
  'expected_cols': ['region', 'n', 'cancelled'],
  'hint': "COUNT(*) FILTER (WHERE status = 'cancelled').",
  'ordered': True},
 {'id': 'd12-recursive-subordinates',
  'mode': 'sql',
  'title': 'Все подчинённые',
  'statement': 'Выведите всех подчинённых Сергея (id 7) на всех уровнях: колонки id, name, level (1 — '
               'прямые); по level, затем по id.',
  'starter': '-- рекурсия вниз\nWITH RECURSIVE\n',
  'setup': 'CREATE TABLE emp (id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept TEXT NOT NULL, boss_id '
           'INTEGER, salary INTEGER NOT NULL);\n'
           'INSERT INTO emp VALUES '
           "(1,'Ольга','IT',NULL,500),(2,'Игорь','IT',1,300),(3,'Мария','IT',1,300),(4,'Пётр','IT',2,200),(5,'Нина','HR',1,250),(6,'Олег','HR',5,150),(7,'Сергей','Sales',1,280),(8,'Аня','Sales',7,180),(9,'Лев','Sales',7,180),(10,'Ира','Sales',8,120);\n",
  'expected': [[8, 'Аня', 1], [9, 'Лев', 1], [10, 'Ира', 2]],
  'expected_cols': ['id', 'name', 'level'],
  'hint': 'Якорь — прямые подчинённые id 7; шаг — присоединяем тех, чей boss_id равен id из предыдущего '
          'шага.',
  'ordered': True},
 {'id': 'd12-recursive-depth',
  'mode': 'sql',
  'title': 'Глубина дерева',
  'statement': 'Выведите максимальную глубину иерархии (директор — уровень 0): колонка depth.',
  'starter': '-- глубина\nWITH RECURSIVE\n',
  'setup': 'CREATE TABLE emp (id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept TEXT NOT NULL, boss_id '
           'INTEGER, salary INTEGER NOT NULL);\n'
           'INSERT INTO emp VALUES '
           "(1,'Ольга','IT',NULL,500),(2,'Игорь','IT',1,300),(3,'Мария','IT',1,300),(4,'Пётр','IT',2,200),(5,'Нина','HR',1,250),(6,'Олег','HR',5,150),(7,'Сергей','Sales',1,280),(8,'Аня','Sales',7,180),(9,'Лев','Sales',7,180),(10,'Ира','Sales',8,120);\n",
  'expected': [[3]],
  'expected_cols': ['depth'],
  'hint': 'Рекурсия считает глубину; снаружи MAX.'},
 {'id': 'd12-recursive-dates',
  'mode': 'sql',
  'title': 'Ряд дат',
  'statement': 'Сгенерируйте ряд из последовательных чисел от 1 до 7 рекурсивным выражением и выведите их '
               'сумму квадратов: колонка s (должно получиться 140).',
  'starter': '-- ряд чисел\nWITH RECURSIVE\n',
  'setup': '',
  'expected': [[140]],
  'expected_cols': ['s'],
  'hint': 'Якорь SELECT 1, шаг i + 1 с условием i < 7.'},
 {'id': 'd12-not-exists',
  'mode': 'sql',
  'title': 'Отделы без руководителей-продавцов',
  'statement': 'Выведите сотрудников, у которых нет подчинённых: колонки id, name; по id. Используйте NOT '
               'EXISTS.',
  'starter': '-- NOT EXISTS\nSELECT\n',
  'setup': 'CREATE TABLE emp (id INTEGER PRIMARY KEY, name TEXT NOT NULL, dept TEXT NOT NULL, boss_id '
           'INTEGER, salary INTEGER NOT NULL);\n'
           'INSERT INTO emp VALUES '
           "(1,'Ольга','IT',NULL,500),(2,'Игорь','IT',1,300),(3,'Мария','IT',1,300),(4,'Пётр','IT',2,200),(5,'Нина','HR',1,250),(6,'Олег','HR',5,150),(7,'Сергей','Sales',1,280),(8,'Аня','Sales',7,180),(9,'Лев','Sales',7,180),(10,'Ира','Sales',8,120);\n",
  'expected': [[3, 'Мария'], [4, 'Пётр'], [6, 'Олег'], [9, 'Лев'], [10, 'Ира']],
  'expected_cols': ['id', 'name'],
  'hint': 'NOT EXISTS (SELECT 1 FROM emp s WHERE s.boss_id = e.id).',
  'ordered': True},
 {'id': 'd12-except',
  'mode': 'sql',
  'title': 'Разность множеств',
  'statement': 'Выведите значения, которые есть в a, но нет в b (без повторов): колонка x; по возрастанию.',
  'starter': '-- EXCEPT\nSELECT\n',
  'setup': 'CREATE TABLE a (x INTEGER);\n'
           'CREATE TABLE b (x INTEGER);\n'
           'INSERT INTO a VALUES (1),(2),(3),(3),(4);\n'
           'INSERT INTO b VALUES (3),(4),(5);\n',
  'expected': [[1], [2]],
  'expected_cols': ['x'],
  'hint': 'EXCEPT убирает повторы сам.',
  'ordered': True},
 {'id': 'd12-intersect-union',
  'mode': 'sql',
  'title': 'Пересечение и объединение',
  'statement': 'Выведите одну строку: сколько значений в пересечении a и b (k_int) и сколько всего различных '
               'значений в объединении (k_union). Колонки k_int, k_union.',
  'starter': '-- INTERSECT и UNION\nSELECT\n',
  'setup': 'CREATE TABLE a (x INTEGER);\n'
           'CREATE TABLE b (x INTEGER);\n'
           'INSERT INTO a VALUES (1),(2),(3),(3),(4);\n'
           'INSERT INTO b VALUES (3),(4),(5);\n',
  'expected': [[2, 5]],
  'expected_cols': ['k_int', 'k_union'],
  'hint': 'Две скалярные подвыборки с COUNT(*) над INTERSECT и UNION.'},
 {'id': 'd12-json-extract',
  'mode': 'sql',
  'title': 'Значения из JSON',
  'statement': 'Выведите города и средний возраст пользователей по событиям: колонки city, avg_age (ROUND до '
               'целого); по городу. Используйте json_extract.',
  'starter': '-- json_extract\nSELECT\n',
  'setup': 'CREATE TABLE events (id INTEGER PRIMARY KEY, doc TEXT NOT NULL);\n'
           'INSERT INTO events VALUES '
           '(1,\'{"user":{"city":"Москва","age":30},"tags":["a","b"]}\'),(2,\'{"user":{"city":"Казань","age":25},"tags":[]}\'),(3,\'{"user":{"city":"Москва","age":41},"tags":["c"]}\');\n',
  'expected': [['Казань', 25.0], ['Москва', 36.0]],
  'expected_cols': ['city', 'avg_age'],
  'hint': "Пути '$.user.city' и '$.user.age'; группировка по первому.",
  'ordered': True},
 {'id': 'd12-json-each',
  'mode': 'sql',
  'title': 'Развернуть массив из JSON',
  'statement': 'Выведите число событий для каждого тега из массива tags: колонки tag, n; по убыванию n, '
               'затем по тегу. Используйте json_each.',
  'starter': '-- json_each\nSELECT\n',
  'setup': 'CREATE TABLE events (id INTEGER PRIMARY KEY, doc TEXT NOT NULL);\n'
           'INSERT INTO events VALUES '
           '(1,\'{"tags":["a","b"]}\'),(2,\'{"tags":[]}\'),(3,\'{"tags":["b","c"]}\');\n',
  'expected': [['b', 2], ['a', 1], ['c', 1]],
  'expected_cols': ['tag', 'n'],
  'hint': "json_each(doc, '$.tags') возвращает строки с value; соедините с events через запятую.",
  'ordered': True},
 {'id': 'd12-upsert-returning',
  'mode': 'sql',
  'title': 'UPSERT с RETURNING',
  'statement': "Увеличьте счётчик 'a' на 2, а счётчика 'b' ещё нет — создайте со значением 1. Сделайте это "
               'двумя INSERT … ON CONFLICT (name) DO UPDATE SET n = n + excluded.n. Итог проверяется по '
               'таблице.',
  'starter': '-- два upsert\nINSERT INTO counters\n',
  'setup': 'CREATE TABLE counters (name TEXT PRIMARY KEY, n INTEGER NOT NULL);\n'
           "INSERT INTO counters VALUES ('a', 5);\n",
  'expected': [['a', 7], ['b', 1]],
  'expected_cols': ['name', 'n'],
  'hint': 'ON CONFLICT (name) DO UPDATE SET n = n + excluded.n.',
  'ordered': True,
  'check': 'SELECT name, n FROM counters ORDER BY name'},
 {'id': 'd12-delete-returning',
  'mode': 'sql',
  'title': 'DELETE RETURNING',
  'statement': 'Удалите из q строки с отрицательным v и одновременно верните их запросом DELETE … RETURNING '
               'id, v. Итог проверяется по оставшимся строкам таблицы q.',
  'starter': '-- DELETE ... RETURNING\nDELETE FROM q\n',
  'setup': 'CREATE TABLE q (id INTEGER PRIMARY KEY, v INTEGER);\n'
           'INSERT INTO q VALUES (1,5),(2,-3),(3,0),(4,-8);\n',
  'expected': [[1, 5], [3, 0]],
  'expected_cols': ['id', 'v'],
  'hint': 'DELETE FROM q WHERE v < 0 RETURNING id, v;',
  'ordered': True,
  'check': 'SELECT id, v FROM q ORDER BY id'},
 {'id': 'd12-gaps-islands',
  'mode': 'sql',
  'title': 'Пропуски и острова',
  'statement': 'Для каждого пользователя выведите непрерывные серии дней (острова): колонки user_id, '
               'first_day, last_day, length; по user_id и first_day. Подсказка: day − ROW_NUMBER() даёт '
               'постоянное значение внутри серии.',
  'starter': '-- серии подряд\nSELECT\n',
  'setup': 'CREATE TABLE logins (user_id INTEGER, day INTEGER);\n'
           'INSERT INTO logins VALUES (1,1),(1,2),(1,3),(1,5),(1,6),(2,10),(2,12),(2,13);\n',
  'expected': [[1, 1, 3, 3], [1, 5, 6, 2], [2, 10, 10, 1], [2, 12, 13, 2]],
  'expected_cols': ['user_id', 'first_day', 'last_day', 'length'],
  'hint': 'Группа = day − ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day); затем GROUP BY user_id, '
          'grp.',
  'ordered': True},
 {'id': 'd12-first-value',
  'mode': 'sql',
  'title': 'Первая покупка клиента',
  'statement': 'Для каждого заказа выведите сумму первой покупки клиента (по минимальному дню): колонки id, '
               'first_amount; по id. Используйте FIRST_VALUE.',
  'starter': '-- FIRST_VALUE\nSELECT\n',
  'setup': 'CREATE TABLE o (id INTEGER PRIMARY KEY, client TEXT, day INTEGER, amount INTEGER);\n'
           "INSERT INTO o VALUES (1,'A',5,100),(2,'A',9,70),(3,'B',3,40),(4,'B',4,90),(5,'A',2,30);\n",
  'expected': [[1, 30], [2, 30], [3, 40], [4, 40], [5, 30]],
  'expected_cols': ['id', 'first_amount'],
  'hint': 'FIRST_VALUE(amount) OVER (PARTITION BY client ORDER BY day).',
  'ordered': True},
 {'id': 'd12-py-window-rank',
  'mode': 'func',
  'func': 'dense_rank_by_group',
  'title': 'DENSE_RANK вручную',
  'statement': 'Строки — списки [группа, значение]. Напишите dense_rank_by_group(rows): список рангов в том '
               'же порядке строк — по убыванию значения внутри группы, равные значения получают один ранг, '
               'ранги идут без пропусков с 1.',
  'starter': 'def dense_rank_by_group(rows):\n    pass\n',
  'tests': [{'args': [[['a', 5], ['a', 7], ['b', 1], ['a', 5], ['b', 3]]], 'expected': [2, 1, 2, 2, 1]},
            {'args': [[]], 'expected': []},
            {'args': [[['x', 1]]], 'expected': [1]}],
  'hint': 'Для каждой группы отсортируйте различные значения по убыванию и пронумеруйте.'},
 {'id': 'd12-py-lag',
  'mode': 'func',
  'func': 'deltas',
  'title': 'LAG своими руками',
  'statement': 'Напишите deltas(values): список разностей между соседними значениями; первая позиция — None '
               '(предыдущего нет). Для пустого списка — пустой список.',
  'starter': 'def deltas(values):\n    pass\n',
  'tests': [{'args': [[10, 13, 9]], 'expected': [None, 3, -4]},
            {'args': [[]], 'expected': []},
            {'args': [[5]], 'expected': [None]}],
  'hint': 'Первый элемент None, остальные — v[i] − v[i−1].'},
 {'id': 'd12-py-frame',
  'mode': 'func',
  'func': 'moving_avg',
  'title': 'Скользящее среднее',
  'statement': 'Напишите moving_avg(values, k): для каждой позиции среднее значений в окне из текущего и k−1 '
               'предыдущих (в начале окно короче), округлённое до двух знаков.',
  'starter': 'def moving_avg(values, k):\n    pass\n',
  'tests': [{'args': [[10, 20, 30, 40], 3], 'expected': [10.0, 15.0, 20.0, 30.0]},
            {'args': [[], 2], 'expected': []},
            {'args': [[7], 5], 'expected': [7.0]},
            {'args': [[1, 2, 3, 4, 5], 2], 'expected': [1.0, 1.5, 2.5, 3.5, 4.5]}],
  'hint': 'Срез values[max(0, i-k+1):i+1] и среднее.'},
 {'id': 'd12-py-pivot',
  'mode': 'func',
  'func': 'pivot_sum',
  'title': 'Сводная таблица',
  'statement': 'Записи — списки [строка, столбец, значение]. Напишите pivot_sum(records): словарь «строка → '
               'словарь «столбец → сумма значений»». Ключи — строки.',
  'starter': 'def pivot_sum(records):\n    pass\n',
  'tests': [{'args': [[['a', 'x', 1], ['a', 'y', 2], ['b', 'x', 3], ['a', 'x', 4]]],
             'expected': {'a': {'x': 5, 'y': 2}, 'b': {'x': 3}}},
            {'args': [[]], 'expected': {}}],
  'hint': 'Вложенный словарь: setdefault на строку и get на столбец.'},
 {'id': 'd12-py-recursive',
  'mode': 'func',
  'func': 'descendants',
  'title': 'Обход иерархии',
  'statement': 'Связи — список пар [начальник, подчинённый]. Напишите descendants(pairs, root): '
               'отсортированный список всех (прямых и косвенных) подчинённых root; в данных может быть цикл '
               '— каждый узел учитывается один раз, сам root в ответ не входит.',
  'starter': 'def descendants(pairs, root):\n    pass\n',
  'tests': [{'args': [[[1, 2], [1, 3], [2, 4], [4, 5]], 1], 'expected': [2, 3, 4, 5]},
            {'args': [[[1, 2], [2, 3], [3, 1]], 1], 'expected': [2, 3]},
            {'args': [[], 7], 'expected': []}],
  'hint': 'Обход в глубину с множеством посещённых узлов — так цикл не страшен.'},
 {'id': 'd12-py-upsert',
  'mode': 'func',
  'func': 'upsert_all',
  'title': 'UPSERT по ключу',
  'statement': 'Таблица — словарь «ключ → значение». Изменения — список [ключ, дельта]. Напишите '
               'upsert_all(table, changes): новый словарь, где к существующему ключу значение прибавляется, '
               'а новому ключу присваивается дельта (как INSERT … ON CONFLICT DO UPDATE n = n + excluded.n). '
               'Исходный не менять.',
  'starter': 'def upsert_all(table, changes):\n    pass\n',
  'tests': [{'args': [{'a': 5}, [['a', 2], ['b', 1], ['b', 3]]], 'expected': {'a': 7, 'b': 4}},
            {'args': [{}, []], 'expected': {}},
            {'args': [{'x': 1}, [['y', 2]]], 'expected': {'x': 1, 'y': 2}}],
  'hint': 'Копия словаря и сложение через get(k, 0).'},
 {'id': 'd12-py-set-ops',
  'mode': 'func',
  'func': 'set_ops',
  'title': 'Операции над множествами',
  'statement': 'Даны два списка a и b. Напишите set_ops(a, b): список из четырёх отсортированных списков '
               '[объединение без повторов, пересечение, a минус b, число строк UNION ALL (одно число)].',
  'starter': 'def set_ops(a, b):\n    pass\n',
  'tests': [{'args': [[1, 2, 3, 3, 4], [3, 4, 5]], 'expected': [[1, 2, 3, 4, 5], [3, 4], [1, 2], 8]},
            {'args': [[], []], 'expected': [[], [], [], 0]},
            {'args': [[1], [1]], 'expected': [[1], [1], [], 2]}],
  'hint': 'Множества Python: |, &, −; для UNION ALL просто сложите длины.'}]}
