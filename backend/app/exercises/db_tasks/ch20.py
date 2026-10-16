"""Задачи книги «Базы данных»: глава 20."""

TASKS: dict[int, list[dict]] = {20: [{'id': 'd4-without-rowid',
  'mode': 'sql',
  'title': 'Кластеризованная таблица',
  'statement': 'Создайте таблицу kv(k TEXT PRIMARY KEY, v TEXT) так, чтобы сама таблица была B-деревом по '
               'ключу k (в SQLite — WITHOUT ROWID).',
  'starter': '-- таблица kv, кластеризованная по k\nCREATE TABLE kv (\n\n)\n',
  'setup': '',
  'expected': [[1]],
  'expected_cols': ['wr'],
  'hint': 'После скобок со столбцами допишите WITHOUT ROWID.',
  'check': "SELECT wr FROM pragma_table_list('kv')"},
 {'id': 'd4-pk-plan',
  'mode': 'sql',
  'title': 'Поиск по первичному ключу в кластеризованной таблице',
  'statement': 'Создайте таблицу cfg(name TEXT PRIMARY KEY, value TEXT), чтобы запрос по name шёл напрямую '
               'по первичному ключу (в плане — USING PRIMARY KEY), а не через отдельный служебный индекс.',
  'starter': '-- таблица cfg\nCREATE TABLE cfg (\n\n)\n',
  'setup': '',
  'expected': [[2, 0, 39, 'SEARCH cfg USING PRIMARY KEY (name=?)']],
  'hint': 'WITHOUT ROWID делает первичный ключ самой структурой таблицы.',
  'check': "EXPLAIN QUERY PLAN SELECT value FROM cfg WHERE name = 'a'",
  'contains': ['USING PRIMARY KEY']},
 {'id': 'd4-pages-sql',
  'mode': 'sql',
  'title': 'Сколько страниц займёт таблица',
  'statement': 'Страница — 8192 байта, из них 192 заняты заголовком; на каждую строку уходит ещё 4 байта '
               'слота. Для каждой таблицы из tables_info выведите name и число страниц (целое, округление '
               'вверх): rows_per_page = (8192 − 192) / (row_bytes + 4) с отбрасыванием дробной части; pages '
               '= ceil(rows / rows_per_page). Колонки: name, pages; порядок по name.',
  'starter': '-- name и число страниц\nSELECT\n',
  'setup': 'CREATE TABLE tables_info (name TEXT PRIMARY KEY, rows INTEGER NOT NULL, row_bytes INTEGER NOT '
           'NULL);\n'
           "INSERT INTO tables_info VALUES ('orders', 1000000, 120),('users', 50000, 300),('logs', 20000000, "
           '80);\n',
  'expected': [['logs', 210527], ['orders', 15625], ['users', 1924]],
  'expected_cols': ['name', 'pages'],
  'hint': 'Целочисленное деление в SQLite: 8000 / (row_bytes + 4); потолок: (a + b − 1) / b.',
  'ordered': True},
 {'id': 'd4-slotted-page',
  'mode': 'func',
  'func': 'page_layout',
  'title': 'Раскладка страницы со слотами',
  'statement': 'Страница размером page_size байт: заголовок header байт, затем массив слотов по 4 байта на '
               'строку, а строки укладываются с конца страницы подряд (первая строка — самая последняя). '
               'Напишите page_layout(page_size, header, rows): список смещений начала каждой строки от '
               'начала страницы; если строки вместе со слотами и заголовком не помещаются — пустой список.',
  'starter': 'def page_layout(page_size, header, rows):\n    pass\n',
  'tests': [{'args': [100, 10, [20, 30]], 'expected': [80, 50]},
            {'args': [100, 10, [40, 40]], 'expected': [60, 20]},
            {'args': [100, 10, [40, 41]], 'expected': [60, 19]},
            {'args': [64, 8, []], 'expected': []},
            {'args': [50, 10, [10, 10, 10]], 'expected': []}],
  'hint': 'Проверьте сумму: заголовок + 4 на слот + длины строк; затем идите с конца страницы, вычитая '
          'длины.'},
 {'id': 'd4-rows-per-page',
  'mode': 'func',
  'func': 'pages_needed',
  'title': 'Страницы под таблицу',
  'statement': 'Напишите pages_needed(rows, row_bytes, page_size, header): сколько страниц нужно под '
               'таблицу. На строку тратится row_bytes + 4 байта (слот), на странице доступно page_size − '
               'header байт; строки не делятся между страницами; для 0 строк — 0 страниц.',
  'starter': 'def pages_needed(rows, row_bytes, page_size, header):\n    pass\n',
  'tests': [{'args': [1000, 96, 8192, 192], 'expected': 13},
            {'args': [0, 100, 8192, 192], 'expected': 0},
            {'args': [1, 100, 8192, 192], 'expected': 1},
            {'args': [80, 96, 8192, 192], 'expected': 1},
            {'args': [81, 96, 8192, 192], 'expected': 2},
            {'args': [1000000, 120, 8192, 192], 'expected': 15625}],
  'hint': 'rows_per_page = (page_size − header) // (row_bytes + 4); потолок деления: -(-a // b).'},
 {'id': 'd4-lru',
  'mode': 'func',
  'func': 'lru_sim',
  'title': 'Буферный пул: LRU',
  'statement': 'Буферный пул на capacity страниц вытесняет давно не использовавшуюся (LRU). Напишите '
               'lru_sim(capacity, accesses): тройка [попаданий, промахов, страницы в пуле от самой давней к '
               'самой свежей].',
  'starter': 'def lru_sim(capacity, accesses):\n    pass\n',
  'tests': [{'args': [3, [1, 2, 3, 1, 4, 2]], 'expected': [1, 5, [1, 4, 2]]},
            {'args': [2, [1, 2, 1, 2, 1, 2]], 'expected': [4, 2, [1, 2]]},
            {'args': [1, [1, 1, 2, 2]], 'expected': [2, 2, [2]]},
            {'args': [3, []], 'expected': [0, 0, []]},
            {'args': [3, [1, 2, 3, 4, 5, 6, 1]], 'expected': [0, 7, [5, 6, 1]]},
            {'args': [4, [7, 7, 7, 8, 9, 7]], 'expected': [3, 3, [8, 9, 7]]}],
  'hint': 'Список пула: попадание — переложить страницу в конец; промах при полном пуле — убрать первую.'},
 {'id': 'd4-wal-redo',
  'mode': 'func',
  'func': 'redo',
  'title': 'Redo по LSN',
  'statement': 'Страницы — словарь «имя → [lsn, значение]». Журнал — список записей [lsn, страница, '
               'новое_значение] по порядку. Проигрывание применяет запись, только если её lsn больше lsn '
               'страницы; тогда у страницы меняются и lsn, и значение. Напишите redo(pages, log): страницы '
               'после проигрывания (исходный словарь не меняйте).',
  'starter': 'def redo(pages, log):\n    pass\n',
  'tests': [{'args': [{'p1': [100, 'a']}, [[101, 'p1', 'b'], [102, 'p1', 'c']]],
             'expected': {'p1': [102, 'c']}},
            {'args': [{'p1': [102, 'c']}, [[101, 'p1', 'b'], [102, 'p1', 'c']]],
             'expected': {'p1': [102, 'c']}},
            {'args': [{'p1': [5, 'x'], 'p2': [9, 'y']}, [[6, 'p1', 'x2'], [7, 'p2', 'y2'], [10, 'p2', 'y3']]],
             'expected': {'p1': [6, 'x2'], 'p2': [10, 'y3']}},
            {'args': [{'p1': [1, 'a']}, []], 'expected': {'p1': [1, 'a']}}],
  'hint': 'Повторное проигрывание безвредно именно из-за сравнения lsn > lsn страницы.'},
 {'id': 'd4-checkpoint',
  'mode': 'func',
  'func': 'keep_log',
  'title': 'Какой журнал можно удалить',
  'statement': 'Журнал хранит записи с номерами LSN. После контрольной точки на checkpoint_lsn журнал нужен, '
               'начиная с самой старой записи, которая ещё нужна: это min(checkpoint_lsn, минимальный '
               'первый_lsn среди активных транзакций). Напишите keep_log(lsns, checkpoint_lsn, '
               'active_first_lsns): список LSN, которые нужно сохранить (в исходном порядке).',
  'starter': 'def keep_log(lsns, checkpoint_lsn, active_first_lsns):\n    pass\n',
  'tests': [{'args': [[1, 2, 3, 4, 5, 6], 4, []], 'expected': [4, 5, 6]},
            {'args': [[1, 2, 3, 4, 5, 6], 4, [2]], 'expected': [2, 3, 4, 5, 6]},
            {'args': [[1, 2, 3, 4, 5, 6], 4, [5]], 'expected': [4, 5, 6]},
            {'args': [[], 10, [3]], 'expected': []},
            {'args': [[10, 11], 3, []], 'expected': [10, 11]}],
  'hint': 'Старейшая нужная запись — минимум из контрольной точки и первых записей активных транзакций.'},
 {'id': 'd4-memtable-flush',
  'mode': 'func',
  'func': 'lsm_flush',
  'title': 'Memtable и сброс на диск',
  'statement': 'Операции — ["put", ключ, значение] и ["del", ключ]. Memtable — словарь; удаление записывает '
               'надгробие (значение None). После каждой операции, если в memtable стало не меньше limit '
               'ключей, она сбрасывается в новую SSTable — список пар [ключ, значение] по возрастанию ключа '
               '— и очищается. Напишите lsm_flush(ops, limit): пара [список SSTable в порядке создания, '
               'оставшийся memtable в виде отсортированного списка пар].',
  'starter': 'def lsm_flush(ops, limit):\n    pass\n',
  'tests': [{'args': [[['put', 'b', 1], ['put', 'a', 2], ['put', 'c', 3], ['put', 'd', 4]], 3],
             'expected': [[[['a', 2], ['b', 1], ['c', 3]]], [['d', 4]]]},
            {'args': [[['put', 'a', 1], ['put', 'a', 2], ['del', 'a']], 2], 'expected': [[], [['a', None]]]},
            {'args': [[], 2], 'expected': [[], []]},
            {'args': [[['put', 'x', 1], ['del', 'y'], ['put', 'z', 9]], 2],
             'expected': [[[['x', 1], ['y', None]]], [['z', 9]]]}],
  'hint': 'Ключ, записанный повторно, не увеличивает размер memtable; удаление — это запись None.'},
 {'id': 'd4-lsm-get',
  'mode': 'func',
  'func': 'lsm_get',
  'title': 'Чтение из LSM-дерева',
  'statement': 'Чтение смотрит сначала memtable (словарь), затем SSTable от новой к старой (список '
               'словарей); значение None — надгробие. Напишите lsm_get(memtable, sstables, key): пара '
               '[значение или None, сколько структур проверено]. Если ключ найден (даже как надгробие), '
               'поиск прекращается; проверенной считается и та, где ключ нашёлся.',
  'starter': 'def lsm_get(memtable, sstables, key):\n    pass\n',
  'tests': [{'args': [{'a': 1}, [{'b': 2}, {'a': 0, 'c': 3}], 'a'], 'expected': [1, 1]},
            {'args': [{'a': 1}, [{'b': 2}, {'a': 0, 'c': 3}], 'c'], 'expected': [3, 3]},
            {'args': [{}, [{'a': None}, {'a': 5}], 'a'], 'expected': [None, 2]},
            {'args': [{}, [{'b': 2}], 'z'], 'expected': [None, 2]},
            {'args': [{'k': 7}, [], 'k'], 'expected': [7, 1]}],
  'hint': 'Идите по структурам от новых к старым; на первом найденном ключе остановитесь — даже если там '
          'None.'},
 {'id': 'd4-compaction',
  'mode': 'func',
  'func': 'merge_runs',
  'title': 'Компакция: слияние двух файлов',
  'statement': 'Два отсортированных по ключу файла — списки пар [ключ, значение]; значение None — надгробие. '
               'Напишите merge_runs(newer, older, drop_tombstones): слитый отсортированный список, в котором '
               'для общего ключа берётся значение из newer; если drop_tombstones истинно, пары со значением '
               'None убираются.',
  'starter': 'def merge_runs(newer, older, drop_tombstones):\n    pass\n',
  'tests': [{'args': [[['a', 9], ['b', 2]], [['a', 1], ['c', 3]], False],
             'expected': [['a', 9], ['b', 2], ['c', 3]]},
            {'args': [[['a', None]], [['a', 1], ['b', 2]], False], 'expected': [['a', None], ['b', 2]]},
            {'args': [[['a', None]], [['a', 1], ['b', 2]], True], 'expected': [['b', 2]]},
            {'args': [[], [['x', 1]], True], 'expected': [['x', 1]]},
            {'args': [[], [], False], 'expected': []}],
  'hint': 'Сначала положите в словарь старые значения, затем поверх — новые; надгробия убирайте только если '
          'разрешено.'},
 {'id': 'd4-bloom',
  'mode': 'func',
  'func': 'bloom_check',
  'title': 'Фильтр Блума',
  'statement': 'Фильтр Блума из m бит и k хеш-функций: h_i(s) = (сумма кодов символов s · (i + 1) + i) % m '
               'для i = 0..k−1. В фильтр добавляют items (устанавливают биты), затем для каждого запроса из '
               "queries отвечают 'maybe', если все k бит установлены, иначе 'no'. Напишите bloom_check(m, k, "
               'items, queries): список ответов.',
  'starter': 'def bloom_check(m, k, items, queries):\n    pass\n',
  'tests': [{'args': [16, 2, ['ab', 'cd'], ['ab', 'cd', 'zz', 'ba']],
             'expected': ['maybe', 'maybe', 'no', 'maybe']},
            {'args': [8, 1, ['a'], ['a', 'b', 'i']], 'expected': ['maybe', 'no', 'maybe']},
            {'args': [32, 3, [], ['x']], 'expected': ['no']},
            {'args': [10, 2, ['key1', 'key2', 'key3'], ['key1', 'key4', 'key5', 'keyA']],
             'expected': ['maybe', 'no', 'no', 'no']}],
  'hint': 'Одна функция хеширования с параметром i; запрос «maybe» только если все k её значений уже '
          'установлены.'},
 {'id': 'd4-write-amp',
  'mode': 'func',
  'func': 'write_amplification',
  'title': 'Усиление записи',
  'statement': 'Упрощённые модели. B-дерево: на изменение row_bytes байт записывается страница page_size '
               'плюс журнал row_bytes. LSM с уровнями: журнал и сброс дают 2 записи, а каждый из levels '
               'уровней переписывает данные ratio раз: 2 + levels · ratio. Напишите '
               "write_amplification(kind, a, b): для 'btree' (a — page_size, b — row_bytes) верните (a + b) "
               "/ b, для 'lsm' (a — levels, b — ratio) верните 2 + a · b; результат округлите до двух "
               'знаков.',
  'starter': 'def write_amplification(kind, a, b):\n    pass\n',
  'tests': [{'args': ['btree', 8192, 100], 'expected': 82.92},
            {'args': ['btree', 4096, 4096], 'expected': 2.0},
            {'args': ['lsm', 4, 10], 'expected': 42},
            {'args': ['lsm', 3, 8], 'expected': 26},
            {'args': ['lsm', 0, 10], 'expected': 2}],
  'hint': 'Две формулы — по одной на каждый вид; не забудьте round(…, 2).'},
 {'id': 'd4-lookup-cost',
  'mode': 'func',
  'func': 'lookup_cost',
  'title': 'Стоимость поиска строки',
  'statement': 'Считаем чтения страниц. Куча: поиск по индексу — index_height страниц плюс 1 страница кучи. '
               'Кластеризованная таблица: поиск по первичному ключу — table_height. Кластеризованная, поиск '
               'по вторичному индексу: index_height + table_height. Напишите lookup_cost(kind, index_height, '
               "table_height): kind — 'heap', 'clustered_pk' или 'clustered_secondary'.",
  'starter': 'def lookup_cost(kind, index_height, table_height):\n    pass\n',
  'tests': [{'args': ['heap', 3, 4], 'expected': 4},
            {'args': ['clustered_pk', 3, 4], 'expected': 4},
            {'args': ['clustered_secondary', 3, 4], 'expected': 7},
            {'args': ['heap', 1, 1], 'expected': 2},
            {'args': ['clustered_secondary', 2, 3], 'expected': 5}],
  'hint': 'Три случая — три формулы из условия.'},
 {'id': 'd4-torn-page',
  'mode': 'func',
  'func': 'is_torn',
  'title': 'Разорванная страница',
  'statement': 'Страница состоит из секторов; в каждом хранится номер версии записи страницы. Если после '
               'сбоя версии секторов не совпадают, страница «разорвана». Напишите is_torn(sector_versions): '
               'True, если не все версии одинаковы; пустую страницу считайте целой.',
  'starter': 'def is_torn(sector_versions):\n    pass\n',
  'tests': [{'args': [[5, 5, 5, 5]], 'expected': False},
            {'args': [[5, 5, 4, 4]], 'expected': True},
            {'args': [[]], 'expected': False},
            {'args': [[7]], 'expected': False},
            {'args': [[1, 2, 1, 1]], 'expected': True}],
  'hint': 'Достаточно проверить, сколько различных версий в списке.'},
 {'id': 'd4-columnar-bytes',
  'mode': 'func',
  'func': 'bytes_read',
  'title': 'Сколько байтов читает запрос',
  'statement': 'Таблица из rows строк, размеры столбцов в байтах — col_sizes. В строковом хранилище запрос '
               'читает все столбцы каждой строки, в колоночном — только нужные. Напишите bytes_read(layout, '
               "rows, col_sizes, wanted): layout — 'row' или 'column', wanted — индексы нужных столбцов; "
               'верните число байт.',
  'starter': 'def bytes_read(layout, rows, col_sizes, wanted):\n    pass\n',
  'tests': [{'args': ['row', 1000, [8, 40, 4, 8], [3]], 'expected': 60000},
            {'args': ['column', 1000, [8, 40, 4, 8], [3]], 'expected': 8000},
            {'args': ['column', 1000, [8, 40, 4, 8], [0, 3]], 'expected': 16000},
            {'args': ['column', 10, [8], []], 'expected': 0},
            {'args': ['row', 0, [8, 8], [0]], 'expected': 0}],
  'hint': 'Строковое хранение читает строки целиком, колоночное — только суммирует размеры выбранных '
          'столбцов.'},
 {'id': 'd4-rle',
  'mode': 'func',
  'func': 'rle',
  'title': 'Run-length кодирование',
  'statement': 'Напишите rle(values): список пар [значение, сколько раз подряд встретилось] для подряд '
               'идущих одинаковых значений. Пустой список даёт пустой результат.',
  'starter': 'def rle(values):\n    pass\n',
  'tests': [{'args': [['A', 'A', 'A', 'B', 'B', 'A']], 'expected': [['A', 3], ['B', 2], ['A', 1]]},
            {'args': [[]], 'expected': []},
            {'args': [[1, 1, 1, 1]], 'expected': [[1, 4]]},
            {'args': [['x', 'y', 'z']], 'expected': [['x', 1], ['y', 1], ['z', 1]]},
            {'args': [[0, 0, 1, 1, 0, 0]], 'expected': [[0, 2], [1, 2], [0, 2]]}],
  'hint': 'Сравнивайте текущее значение с последним в результате: совпало — увеличьте счётчик, иначе начните '
          'новую пару.'},
 {'id': 'd4-dict-encode',
  'mode': 'func',
  'func': 'dict_encode',
  'title': 'Словарное кодирование столбца',
  'statement': 'Строки столбца заменяют числами. Напишите dict_encode(values): пару [словарь — список '
               'уникальных значений в порядке первого появления, коды — для каждого значения его номер в '
               'словаре].',
  'starter': 'def dict_encode(values):\n    pass\n',
  'tests': [{'args': [['Москва', 'Казань', 'Москва', 'Тверь', 'Казань']],
             'expected': [['Москва', 'Казань', 'Тверь'], [0, 1, 0, 2, 1]]},
            {'args': [[]], 'expected': [[], []]},
            {'args': [['a', 'a', 'a']], 'expected': [['a'], [0, 0, 0]]},
            {'args': [['x', 'y', 'z']], 'expected': [['x', 'y', 'z'], [0, 1, 2]]}],
  'hint': 'Словарь «значение → номер» заполняется по мере появления; порядок вставки словаря сохраняется.'},
 {'id': 'd4-group-commit',
  'mode': 'func',
  'func': 'group_commit',
  'title': 'Групповой коммит',
  'statement': 'fsync выполняется по тикам: в моменты 0, interval, 2·interval, … Коммит, пришедший в момент '
               't, ждёт ближайшего тика, не раньше t. Напишите group_commit(arrivals, interval): пара '
               '[сколько различных тиков (fsync) понадобилось, наибольшее ожидание в мс].',
  'starter': 'def group_commit(arrivals, interval):\n    pass\n',
  'tests': [{'args': [[1, 2, 3, 12, 19], 10], 'expected': [2, 9]},
            {'args': [[0, 10, 20], 10], 'expected': [3, 0]},
            {'args': [[], 10], 'expected': [0, 0]},
            {'args': [[5, 5, 5, 5], 8], 'expected': [1, 3]},
            {'args': [[9, 11], 10], 'expected': [2, 9]}],
  'hint': 'Ближайший тик не раньше t: ceil(t / interval) * interval; тики собираются во множество.'}]}
