"""Задачи книги «Базы данных»: глава 25."""

TASKS: dict[int, list[dict]] = {25: [{'id': 'd9-hit-ratio',
  'mode': 'sql',
  'title': 'Доля попаданий',
  'statement': 'По журналу обращений access_log(key, hit, ms): hit = 1 — попадание, 0 — промах. Выведите '
               'долю попаданий в процентах, округлённую до целого (одна колонка pct).',
  'starter': '-- hit ratio в процентах\nSELECT\n',
  'setup': 'CREATE TABLE access_log (id INTEGER PRIMARY KEY, key TEXT NOT NULL, hit INTEGER NOT NULL, ms '
           'INTEGER NOT NULL);\n'
           'INSERT INTO access_log VALUES '
           "(1,'user:1',1,2),(2,'user:2',0,40),(3,'user:1',1,2),(4,'page:/',1,1),(5,'user:3',0,55),(6,'user:1',1,3),(7,'page:/',1,1),(8,'user:2',1,2),(9,'page:/',0,30),(10,'user:4',0,45);\n",
  'expected': [[60.0]],
  'expected_cols': ['pct'],
  'hint': 'SUM(hit) — число попаданий, COUNT(*) — всего; умножьте на 100.0, чтобы не было целочисленного '
          'деления.'},
 {'id': 'd9-hot-keys',
  'mode': 'sql',
  'title': 'Самые горячие ключи',
  'statement': 'Выведите три самых частых ключа и число обращений к каждому (колонки key, n); при равенстве '
               '— по ключу.',
  'starter': '-- топ-3 горячих ключа\nSELECT\n',
  'setup': 'CREATE TABLE access_log (id INTEGER PRIMARY KEY, key TEXT NOT NULL, hit INTEGER NOT NULL, ms '
           'INTEGER NOT NULL);\n'
           'INSERT INTO access_log VALUES '
           "(1,'user:1',1,2),(2,'user:2',0,40),(3,'user:1',1,2),(4,'page:/',1,1),(5,'user:3',0,55),(6,'user:1',1,3),(7,'page:/',1,1),(8,'user:2',1,2),(9,'page:/',0,30),(10,'user:4',0,45);\n",
  'expected': [['page:/', 3], ['user:1', 3], ['user:2', 2]],
  'expected_cols': ['key', 'n'],
  'hint': 'GROUP BY key, сортировка по убыванию числа, LIMIT 3.',
  'ordered': True},
 {'id': 'd9-avg-latency',
  'mode': 'sql',
  'title': 'Средняя задержка с кэшем и без',
  'statement': 'Выведите среднюю задержку (колонка ms) отдельно для попаданий и промахов: колонки hit, '
               'avg_ms (целое, округлённое), по hit.',
  'starter': '-- средняя задержка по hit\nSELECT\n',
  'setup': 'CREATE TABLE access_log (id INTEGER PRIMARY KEY, key TEXT NOT NULL, hit INTEGER NOT NULL, ms '
           'INTEGER NOT NULL);\n'
           'INSERT INTO access_log VALUES '
           "(1,'user:1',1,2),(2,'user:2',0,40),(3,'user:1',1,2),(4,'page:/',1,1),(5,'user:3',0,55),(6,'user:1',1,3),(7,'page:/',1,1),(8,'user:2',1,2),(9,'page:/',0,30),(10,'user:4',0,45);\n",
  'expected': [[0, 43.0], [1, 2.0]],
  'expected_cols': ['hit', 'avg_ms'],
  'hint': 'GROUP BY hit и AVG(ms).',
  'ordered': True},
 {'id': 'd9-stale-entries',
  'mode': 'sql',
  'title': 'Устаревшие записи в кэше',
  'statement': 'В cache лежат копии строк source. Выведите id записей, которые нужно инвалидировать: версия '
               'в кэше меньше версии источника, а также записи, которых уже нет в источнике. Колонка id, по '
               'возрастанию.',
  'starter': '-- что инвалидировать\nSELECT\n',
  'setup': 'CREATE TABLE source (id INTEGER PRIMARY KEY, version INTEGER NOT NULL, body TEXT NOT NULL);\n'
           'CREATE TABLE cache (id INTEGER PRIMARY KEY, version INTEGER NOT NULL, body TEXT NOT NULL);\n'
           "INSERT INTO source VALUES (1,3,'a3'),(2,1,'b1'),(3,5,'c5'),(4,2,'d2');\n"
           "INSERT INTO cache VALUES (1,3,'a3'),(2,0,'b0'),(3,4,'c4'),(9,1,'ghost');\n",
  'expected': [[2], [3], [9]],
  'expected_cols': ['id'],
  'hint': 'LEFT JOIN cache → source: нет пары (IS NULL) или версия меньше.',
  'ordered': True},
 {'id': 'd9-refresh-upsert',
  'mode': 'sql',
  'title': 'Обновление кэш-таблицы',
  'statement': 'Обновите cache из source одним INSERT … SELECT … ON CONFLICT: новые id вставить, у '
               'существующих обновить version и body, но только если версия в source больше. Итог '
               'проверяется по таблице cache.',
  'starter': '-- синхронизировать cache из source\nINSERT INTO cache\n',
  'setup': 'CREATE TABLE source (id INTEGER PRIMARY KEY, version INTEGER NOT NULL, body TEXT NOT NULL);\n'
           'CREATE TABLE cache (id INTEGER PRIMARY KEY, version INTEGER NOT NULL, body TEXT NOT NULL);\n'
           "INSERT INTO source VALUES (1,3,'a3'),(2,1,'b1'),(3,5,'c5');\n"
           "INSERT INTO cache VALUES (1,3,'a3'),(2,0,'b0');\n",
  'expected': [[1, 3, 'a3'], [2, 1, 'b1'], [3, 5, 'c5']],
  'expected_cols': ['id', 'version', 'body'],
  'hint': 'ON CONFLICT (id) DO UPDATE SET … WHERE excluded.version > cache.version; WHERE true нужен, чтобы '
          'SQLite разобрал ON CONFLICT после SELECT.',
  'ordered': True,
  'check': 'SELECT id, version, body FROM cache ORDER BY id'},
 {'id': 'd9-lru-cache',
  'mode': 'func',
  'func': 'lru_run',
  'title': 'LRU-кэш: get и put',
  'statement': "Кэш ёмкостью cap. Операции: ['put', ключ, значение] и ['get', ключ]. put добавляет или "
               'обновляет (запись становится самой свежей); при переполнении вытесняется самая давняя. get '
               'возвращает значение и делает запись самой свежей. Напишите lru_run(cap, ops): пару [список '
               'результатов get (None при промахе), ключи в кэше от самого давнего к самому свежему].',
  'starter': 'def lru_run(cap, ops):\n    pass\n',
  'tests': [{'args': [2,
                      [['put', 'a', 1],
                       ['put', 'b', 2],
                       ['get', 'a'],
                       ['put', 'c', 3],
                       ['get', 'b'],
                       ['get', 'c']]],
             'expected': [[1, None, 3], ['a', 'c']]},
            {'args': [1, [['put', 'x', 1], ['put', 'y', 2], ['get', 'x']]], 'expected': [[None], ['y']]},
            {'args': [3, []], 'expected': [[], []]},
            {'args': [2, [['put', 'a', 1], ['put', 'a', 2], ['get', 'a']]], 'expected': [[2], ['a']]}],
  'hint': 'Список порядка + словарь значений; get и put переносят ключ в конец списка.'},
 {'id': 'd9-lfu',
  'mode': 'func',
  'func': 'lfu_evict',
  'title': 'LFU: кого вытеснить',
  'statement': 'Счётчики обращений — словарь «ключ → число», порядок вставки — список keys (от старых к '
               'новым). Вытесняется ключ с наименьшим числом обращений; при равенстве — тот, что вставлен '
               'раньше. Напишите lfu_evict(keys, counts): ключ для вытеснения (None, если кэш пуст).',
  'starter': 'def lfu_evict(keys, counts):\n    pass\n',
  'tests': [{'args': [['a', 'b', 'c'], {'a': 5, 'b': 2, 'c': 2}], 'expected': 'b'},
            {'args': [[], {}], 'expected': None},
            {'args': [['x'], {'x': 1}], 'expected': 'x'},
            {'args': [['a', 'b'], {'a': 0}], 'expected': 'a'},
            {'args': [['p', 'q', 'r'], {'p': 1, 'q': 1, 'r': 1}], 'expected': 'p'}],
  'hint': 'min по паре (число обращений, позиция в списке вставки).'},
 {'id': 'd9-ttl-cache',
  'mode': 'func',
  'func': 'ttl_run',
  'title': 'Кэш с временем жизни',
  'statement': "Операции: ['put', t, ключ, значение, ttl] и ['get', t, ключ]. Запись живёт, пока t < t_put + "
               'ttl. Напишите ttl_run(ops): список результатов get (значение или None). Повторный put '
               'перезаписывает значение и срок.',
  'starter': 'def ttl_run(ops):\n    pass\n',
  'tests': [{'args': [[['put', 0, 'a', 1, 10], ['get', 9, 'a'], ['get', 10, 'a']]], 'expected': [1, None]},
            {'args': [[['put', 0, 'a', 1, 10], ['put', 8, 'a', 2, 10], ['get', 15, 'a']]], 'expected': [2]},
            {'args': [[['get', 0, 'z']]], 'expected': [None]},
            {'args': [[]], 'expected': []}],
  'hint': 'Храните значение и момент истечения; get сравнивает t с моментом истечения.'},
 {'id': 'd9-cache-aside',
  'mode': 'func',
  'func': 'cache_aside',
  'title': 'Cache-aside: сколько раз ходили в базу',
  'statement': 'Запросы — список ключей на чтение. Кэш изначально пуст и без ограничений. При промахе читаем '
               'базу и кладём значение в кэш. Напишите cache_aside(reads): пару [число попаданий, число '
               'обращений к базе].',
  'starter': 'def cache_aside(reads):\n    pass\n',
  'tests': [{'args': [['a', 'b', 'a', 'a', 'c', 'b']], 'expected': [3, 3]},
            {'args': [[]], 'expected': [0, 0]},
            {'args': [['x', 'x', 'x']], 'expected': [2, 1]},
            {'args': [['a', 'b', 'c']], 'expected': [0, 3]}],
  'hint': 'Множество ключей в кэше: уже есть — попадание, нет — обращение к базе и добавление.'},
 {'id': 'd9-write-back',
  'mode': 'func',
  'func': 'write_back_flush',
  'title': 'Отложенная запись',
  'statement': 'Записи — список [ключ, значение] по порядку. Кэш write-back копит изменения и сбрасывает их '
               'в базу, когда накопилось batch различных ключей, а в конце сбрасывает остаток. Напишите '
               'write_back_flush(writes, batch): список сбросов, каждый — словарь «ключ → последнее '
               'значение» на момент сброса (для пустого списка — пустой список).',
  'starter': 'def write_back_flush(writes, batch):\n    pass\n',
  'tests': [{'args': [[['a', 1], ['b', 2], ['a', 3], ['c', 4], ['d', 5]], 3],
             'expected': [{'a': 3, 'b': 2, 'c': 4}, {'d': 5}]},
            {'args': [[], 2], 'expected': []},
            {'args': [[['x', 1], ['x', 2], ['x', 3]], 2], 'expected': [{'x': 3}]},
            {'args': [[['a', 1], ['b', 2]], 1], 'expected': [{'a': 1}, {'b': 2}]}],
  'hint': 'Словарь «грязных» ключей; при достижении batch различных ключей отправьте его в результат и '
          'начните новый.'},
 {'id': 'd9-stampede',
  'mode': 'func',
  'func': 'db_hits_on_expiry',
  'title': 'Сколько запросов дойдёт до базы',
  'statement': 'В момент истечения записи одновременно приходят n запросов. Без защиты каждый идёт в базу. С '
               'одним пересчётом (single-flight) в базу идёт один запрос, остальные ждут. Напишите '
               'db_hits_on_expiry(n, single_flight): число обращений к базе (0, если запросов нет).',
  'starter': 'def db_hits_on_expiry(n, single_flight):\n    pass\n',
  'tests': [{'args': [1000, False], 'expected': 1000},
            {'args': [1000, True], 'expected': 1},
            {'args': [0, True], 'expected': 0},
            {'args': [1, True], 'expected': 1},
            {'args': [5, False], 'expected': 5}],
  'hint': 'Два варианта: n или 1; ноль запросов — ноль обращений.'},
 {'id': 'd9-jitter',
  'mode': 'func',
  'func': 'ttl_with_jitter',
  'title': 'Джиттер TTL',
  'statement': 'Чтобы записи не истекали пачкой, к базовому сроку base добавляют разброс. Детерминированная '
               'версия: для записи номер i (с нуля) срок = base + (i · step) % spread. Напишите '
               'ttl_with_jitter(base, spread, step, count): список сроков для count записей (spread > 0).',
  'starter': 'def ttl_with_jitter(base, spread, step, count):\n    pass\n',
  'tests': [{'args': [300, 30, 7, 6], 'expected': [300, 307, 314, 321, 328, 305]},
            {'args': [60, 10, 3, 0], 'expected': []},
            {'args': [100, 1, 5, 3], 'expected': [100, 100, 100]},
            {'args': [10, 5, 5, 4], 'expected': [10, 10, 10, 10]}],
  'hint': 'Список по формуле base + (i * step) % spread.'},
 {'id': 'd9-negative-cache',
  'mode': 'func',
  'func': 'negative_cache',
  'title': 'Отрицательное кэширование',
  'statement': 'База — словарь «ключ → значение», отсутствующий ключ даёт None. Кэш запоминает и значения, и '
               '«нет» (отрицательный результат). Обращения к базе считаются только при промахе кэша. '
               'Напишите negative_cache(db, reads): пару [список ответов, число обращений к базе].',
  'starter': 'def negative_cache(db, reads):\n    pass\n',
  'tests': [{'args': [{'a': 1}, ['a', 'z', 'z', 'a', 'q']], 'expected': [[1, None, None, 1, None], 3]},
            {'args': [{}, ['x', 'x', 'x']], 'expected': [[None, None, None], 1]},
            {'args': [{'k': 5}, []], 'expected': [[], 0]}],
  'hint': 'Кэш хранит и None; проверять нужно наличие ключа в кэше, а не истинность значения.'},
 {'id': 'd9-cache-key',
  'mode': 'func',
  'func': 'cache_key',
  'title': 'Ключ кэша',
  'statement': "Ключ собирается из пути и параметров: путь + '?' + параметры «имя=значение» через '&', "
               'отсортированные по имени. Пустые параметры (значение None) пропускаются; без параметров знак '
               "'?' не нужен. Напишите cache_key(path, params): строку.",
  'starter': 'def cache_key(path, params):\n    pass\n',
  'tests': [{'args': ['/cart', {'user': 42, 'lang': 'ru'}], 'expected': '/cart?lang=ru&user=42'},
            {'args': ['/cart', {}], 'expected': '/cart'},
            {'args': ['/p', {'b': 2, 'a': None}], 'expected': '/p?b=2'},
            {'args': ['/x', {'z': '1', 'a': '2', 'm': 3}], 'expected': '/x?a=2&m=3&z=1'}],
  'hint': 'Сортируйте пары по имени; формат f"{k}={v}".'},
 {'id': 'd9-versioned-key',
  'mode': 'func',
  'func': 'versioned_keys',
  'title': 'Версии ключей',
  'statement': 'Версия сущности хранится отдельно: словарь «сущность → версия». Ключ кэша — '
               '«сущность:версия». Напишите versioned_keys(versions, bumps, entities): сначала примените '
               'bumps (список сущностей, чья версия растёт на 1; новой сущности версия 0 → 1), затем верните '
               'список ключей для entities в том же порядке (неизвестная сущность — версия 0).',
  'starter': 'def versioned_keys(versions, bumps, entities):\n    pass\n',
  'tests': [{'args': [{'p7': 3}, ['p7'], ['p7', 'p8']], 'expected': ['p7:4', 'p8:0']},
            {'args': [{}, ['a', 'a'], ['a']], 'expected': ['a:2']},
            {'args': [{'x': 1}, [], ['x', 'y']], 'expected': ['x:1', 'y:0']},
            {'args': [{}, [], []], 'expected': []}],
  'hint': 'Копия словаря версий; увеличение в цикле; затем формирование ключей.'},
 {'id': 'd9-double-delete',
  'mode': 'func',
  'func': 'stale_after',
  'title': 'Гонка кэша и базы',
  'statement': "Три события в порядке времени: 'read_db' (читатель взял v1 из базы), 'write' (писатель "
               "обновил базу до v2 и удалил запись в кэше), 'set_cache' (читатель положил свою версию в "
               'кэш). Напишите stale_after(events): True, если после всех событий кэш содержит устаревшее '
               "значение — то есть 'set_cache' произошёл после 'write', а 'read_db' — до 'write'.",
  'starter': 'def stale_after(events):\n    pass\n',
  'tests': [{'args': [['read_db', 'write', 'set_cache']], 'expected': True},
            {'args': [['read_db', 'set_cache', 'write']], 'expected': False},
            {'args': [['write', 'read_db', 'set_cache']], 'expected': False},
            {'args': [['read_db', 'write']], 'expected': False},
            {'args': [[]], 'expected': False}],
  'hint': 'Устаревание — только порядок read_db < write < set_cache.'},
 {'id': 'd9-expected-latency',
  'mode': 'func',
  'func': 'expected_latency',
  'title': 'Ожидаемая задержка',
  'statement': 'Напишите expected_latency(hit, t_cache, t_db): hit·t_cache + (1 − hit)·t_db, округлённое до '
               'двух знаков; и вторую величину — во сколько раз упала нагрузка на базу (1 / (1 − hit); при '
               'hit = 1 вернуть None). Верните пару.',
  'starter': 'def expected_latency(hit, t_cache, t_db):\n    pass\n',
  'tests': [{'args': [0.9, 1, 20], 'expected': [2.9, 10.0]},
            {'args': [0.5, 2, 40], 'expected': [21.0, 2.0]},
            {'args': [1, 1, 20], 'expected': [1, None]},
            {'args': [0, 1, 20], 'expected': [20, 1.0]},
            {'args': [0.99, 1, 50], 'expected': [1.49, 100.0]}],
  'hint': 'Две формулы; осторожно с делением на ноль при hit = 1.'},
 {'id': 'd9-two-level',
  'mode': 'func',
  'func': 'two_level',
  'title': 'Двухуровневый кэш',
  'statement': 'L1 (в процессе) и L2 (общий) — множества ключей без ограничений. Чтение: если ключ в L1 — '
               "ответ 'L1'; иначе если в L2 — ответ 'L2' и ключ попадает в L1; иначе 'DB', и ключ попадает в "
               'L1 и L2. Напишите two_level(reads): список ответов.',
  'starter': 'def two_level(reads):\n    pass\n',
  'tests': [{'args': [['a', 'a', 'b', 'a', 'b']], 'expected': ['DB', 'L1', 'DB', 'L1', 'L1']},
            {'args': [[]], 'expected': []},
            {'args': [['x']], 'expected': ['DB']}],
  'hint': 'Две множества; порядок проверок L1 → L2 → база.'},
 {'id': 'd9-hot-key-detect',
  'mode': 'func',
  'func': 'hot_keys',
  'title': 'Поиск горячих ключей',
  'statement': 'Журнал обращений — список ключей. Ключ горячий, если на него приходится не менее share (доля '
               'от 0 до 1) всех обращений. Напишите hot_keys(log, share): отсортированный список горячих '
               'ключей.',
  'starter': 'def hot_keys(log, share):\n    pass\n',
  'tests': [{'args': [['a', 'a', 'a', 'b', 'c', 'a'], 0.5], 'expected': ['a']},
            {'args': [['a', 'b', 'c', 'd'], 0.25], 'expected': ['a', 'b', 'c', 'd']},
            {'args': [[], 0.1], 'expected': []},
            {'args': [['x', 'x'], 1.0], 'expected': ['x']}],
  'hint': 'Подсчитайте частоты и сравните c / n с share.'}]}
