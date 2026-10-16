"""Задачи книги «Базы данных»: глава 18."""

TASKS: dict[int, list[dict]] = {18: [{'id': 'd2-transfer',
  'mode': 'sql',
  'title': 'Перевод в одной транзакции',
  'statement': 'Переведите 30 рублей со счёта 1 на счёт 2 в одной транзакции (BEGIN … COMMIT). Итог '
               'проверяется по балансам.',
  'starter': '-- перевод 30 со счёта 1 на счёт 2\nBEGIN;\n',
  'setup': 'CREATE TABLE acc (id INTEGER PRIMARY KEY, owner TEXT NOT NULL, bal INTEGER NOT NULL CHECK (bal '
           '>= 0));\n'
           "INSERT INTO acc VALUES (1,'Анна',100),(2,'Борис',50),(3,'Вера',0);\n",
  'expected': [[1, 70], [2, 80], [3, 0]],
  'expected_cols': ['id', 'bal'],
  'hint': 'BEGIN; два UPDATE; COMMIT; — обе операции фиксируются разом.',
  'ordered': True,
  'check': 'SELECT id, bal FROM acc ORDER BY id'},
 {'id': 'd2-conditional-debit',
  'mode': 'sql',
  'title': 'Списание, только если хватает',
  'statement': 'Сначала попытайтесь списать 150 со счёта 1 (там 100) — списание не должно произойти и не '
               'должно вызывать ошибку CHECK: защитите UPDATE условием. Затем спишите 80 с того же счёта. '
               'Итог проверяется по балансам.',
  'starter': '-- списать 150 (не хватает) и затем 80\n',
  'setup': 'CREATE TABLE acc (id INTEGER PRIMARY KEY, owner TEXT NOT NULL, bal INTEGER NOT NULL CHECK (bal '
           '>= 0));\n'
           "INSERT INTO acc VALUES (1,'Анна',100),(2,'Борис',50),(3,'Вера',0);\n",
  'expected': [[1, 20], [2, 50], [3, 0]],
  'expected_cols': ['id', 'bal'],
  'hint': 'Условие bal >= сумма в WHERE: недостаточный остаток — 0 затронутых строк, а не ошибка.',
  'ordered': True,
  'check': 'SELECT id, bal FROM acc ORDER BY id'},
 {'id': 'd2-atomic-update',
  'mode': 'sql',
  'title': 'Атомарное обновление вместо чтения',
  'statement': 'Начислите счёту 2 два бонуса по 10 и 15 рублей двумя UPDATE, в каждом — арифметика прямо в '
               'базе (bal = bal + …), без предварительных SELECT.',
  'starter': '-- два начисления арифметикой в базе\n',
  'setup': 'CREATE TABLE acc (id INTEGER PRIMARY KEY, owner TEXT NOT NULL, bal INTEGER NOT NULL CHECK (bal '
           '>= 0));\n'
           "INSERT INTO acc VALUES (1,'Анна',100),(2,'Борис',50),(3,'Вера',0);\n",
  'expected': [[75]],
  'expected_cols': ['bal'],
  'hint': 'UPDATE acc SET bal = bal + 10 WHERE id = 2; — чтение и запись в одном запросе.',
  'check': 'SELECT bal FROM acc WHERE id = 2'},
 {'id': 'd2-savepoint',
  'mode': 'sql',
  'title': 'SAVEPOINT и частичный откат',
  'statement': "В одной транзакции: вставьте запись 'start', поставьте точку сохранения s1, вставьте 'oops', "
               "откатитесь к s1, вставьте 'finish' и зафиксируйте. В итоге в log должны остаться 'start' и "
               "'finish'.",
  'starter': '-- start, savepoint, oops, rollback to, finish\nBEGIN;\n',
  'setup': 'CREATE TABLE log (id INTEGER PRIMARY KEY, msg TEXT NOT NULL);\n',
  'expected': [['start'], ['finish']],
  'expected_cols': ['msg'],
  'hint': 'SAVEPOINT s1; … ROLLBACK TO s1; откат не закрывает транзакцию — дальше можно продолжать и делать '
          'COMMIT.',
  'ordered': True,
  'check': 'SELECT msg FROM log ORDER BY id'},
 {'id': 'd2-optimistic',
  'mode': 'sql',
  'title': 'Оптимистичная проверка версии',
  'statement': "Два редактора прочитали документ 7 при ver = 1. Первый сохраняет текст 'первый', второй — "
               "'второй': оба обновляют с условием ver = 1 и увеличивают ver. Выполните оба UPDATE подряд: "
               'второй не должен ничего изменить. Итог проверяется по таблице.',
  'starter': '-- два UPDATE с проверкой версии\n',
  'setup': 'CREATE TABLE doc (id INTEGER PRIMARY KEY, body TEXT NOT NULL, ver INTEGER NOT NULL);\n'
           "INSERT INTO doc VALUES (7,'v1',1);\n",
  'expected': [['первый', 2]],
  'expected_cols': ['body', 'ver'],
  'hint': 'В WHERE: id = 7 AND ver = 1; после первого обновления ver = 2, поэтому второе условие ложно.',
  'check': 'SELECT body, ver FROM doc'},
 {'id': 'd2-idempotent',
  'mode': 'sql',
  'title': 'Идемпотентная обработка платежа',
  'statement': 'Платёж p-100 на 500 рублей пришёл дважды (повтор после таймаута). Вставьте его двумя '
               'командами INSERT так, чтобы повтор был проигнорирован, а не вызвал ошибку: в таблице должна '
               'остаться одна строка.',
  'starter': '-- платёж p-100 дважды, но обработан один раз\n',
  'setup': 'CREATE TABLE payments (payment_id TEXT PRIMARY KEY, amount INTEGER NOT NULL);\n',
  'expected': [['p-100', 500]],
  'expected_cols': ['payment_id', 'amount'],
  'hint': 'Уникальный ключ + INSERT OR IGNORE (или ON CONFLICT DO NOTHING) делают повтор безвредным.',
  'check': 'SELECT payment_id, amount FROM payments'},
 {'id': 'd2-write-skew',
  'mode': 'sql',
  'title': 'Перекос записи: дежурные врачи',
  'statement': 'Правило: на дежурстве всегда хотя бы один врач. Снимите с дежурства Анну, а затем Бориса — '
               'каждым UPDATE, в условии которого проверяется, что после снятия останется кто-то ещё '
               '(проверка и изменение в одном запросе). Второе снятие не должно сработать.',
  'starter': '-- снять Анну, затем Бориса с сохранением инварианта\n',
  'setup': 'CREATE TABLE doctors (name TEXT PRIMARY KEY, on_call INTEGER NOT NULL);\n'
           "INSERT INTO doctors VALUES ('Анна',1),('Борис',1);\n",
  'expected': [['Анна', 0], ['Борис', 1]],
  'expected_cols': ['name', 'on_call'],
  'hint': 'Условие (SELECT COUNT(*) … WHERE on_call = 1) > 1 внутри самого UPDATE: проверка и запись '
          'неделимы.',
  'ordered': True,
  'check': 'SELECT name, on_call FROM doctors ORDER BY name'},
 {'id': 'd2-queue-claim',
  'mode': 'sql',
  'title': 'Захват задачи из очереди',
  'statement': 'Два воркера по очереди забирают задачи. Каждый выполняет один UPDATE: переводит самую раннюю '
               "задачу со статусом 'new' в 'taken' и возвращает её id (RETURNING). Выполните две такие "
               'команды подряд; итог проверяется по таблице.',
  'starter': '-- два захвата самой ранней задачи new\n',
  'setup': 'CREATE TABLE jobs (id INTEGER PRIMARY KEY, status TEXT NOT NULL);\n'
           "INSERT INTO jobs VALUES (1,'new'),(2,'new'),(3,'new');\n",
  'expected': [[1, 'taken'], [2, 'taken'], [3, 'new']],
  'expected_cols': ['id', 'status'],
  'hint': 'Выбор и захват — один UPDATE с подзапросом MIN(id): задача не достанется двум воркерам.',
  'ordered': True,
  'check': 'SELECT id, status FROM jobs ORDER BY id'},
 {'id': 'd2-ledger',
  'mode': 'sql',
  'title': 'Двойная запись: сумма равна нулю',
  'statement': 'Журнал проводок ledger(tx, account, amount): каждая транзакция должна давать в сумме 0. '
               'Найдите номера «битых» транзакций, у которых сумма не равна нулю, и саму сумму (колонки: tx, '
               'total).',
  'starter': '-- битые транзакции: сумма amount ≠ 0\nSELECT\n',
  'setup': 'CREATE TABLE ledger (id INTEGER PRIMARY KEY, tx INTEGER NOT NULL, account TEXT NOT NULL, amount '
           'INTEGER NOT NULL);\n'
           'INSERT INTO ledger VALUES '
           "(1,1,'cash',100),(2,1,'sales',-100),(3,2,'cash',-30),(4,2,'rent',30),(5,3,'cash',50),(6,3,'sales',-40);\n",
  'expected': [[3, 10]],
  'expected_cols': ['tx', 'total'],
  'hint': 'GROUP BY tx HAVING SUM(amount) <> 0 — инвариант проверяется запросом.'},
 {'id': 'd2-conflict-graph',
  'mode': 'func',
  'func': 'conflict_edges',
  'title': 'Граф конфликтов расписания',
  'statement': "Расписание — список операций [транзакция, 'r' или 'w', объект] в порядке выполнения. Две "
               'операции конфликтуют, если они над одним объектом, из разных транзакций и хотя бы одна — '
               'запись. Напишите conflict_edges(schedule): отсортированный список уникальных рёбер [Ti, Tj] '
               '— ребро ставится, когда конфликтующая операция Ti идёт раньше операции Tj.',
  'starter': 'def conflict_edges(schedule):\n    pass\n',
  'tests': [{'args': [[[1, 'r', 'x'], [2, 'w', 'x'], [1, 'w', 'y']]], 'expected': [[1, 2]]},
            {'args': [[[1, 'w', 'x'], [2, 'r', 'x'], [2, 'w', 'y'], [3, 'r', 'y']]],
             'expected': [[1, 2], [2, 3]]},
            {'args': [[[1, 'r', 'x'], [2, 'r', 'x']]], 'expected': []},
            {'args': [[[1, 'w', 'x'], [2, 'w', 'x'], [1, 'w', 'y'], [2, 'w', 'y']]], 'expected': [[1, 2]]},
            {'args': [[]], 'expected': []}],
  'hint': 'Для каждой пары операций i < j: разные транзакции, один объект и хотя бы одна запись — ребро (Ti, '
          'Tj).'},
 {'id': 'd2-serializable',
  'mode': 'func',
  'func': 'is_serializable',
  'title': 'Сериализуемо ли расписание',
  'statement': "Расписание — список [транзакция, 'r'/'w', объект]. Расписание сериализуемо по конфликтам, "
               'если граф конфликтов (ребро Ti → Tj, когда конфликтующая операция Ti идёт раньше) не '
               'содержит циклов. Напишите is_serializable(schedule) → True/False.',
  'starter': 'def is_serializable(schedule):\n    pass\n',
  'tests': [{'args': [[[1, 'r', 'x'], [2, 'w', 'x'], [1, 'w', 'x']]], 'expected': False},
            {'args': [[[1, 'r', 'x'], [1, 'w', 'x'], [2, 'r', 'x'], [2, 'w', 'x']]], 'expected': True},
            {'args': [[[1, 'w', 'x'], [2, 'w', 'y'], [1, 'w', 'y'], [2, 'w', 'x']]], 'expected': False},
            {'args': [[[1, 'r', 'x'], [2, 'r', 'x'], [3, 'r', 'x']]], 'expected': True},
            {'args': [[]], 'expected': True},
            {'args': [[[1, 'w', 'x'], [2, 'r', 'x'], [3, 'w', 'x'], [2, 'w', 'y'], [3, 'r', 'y']]],
             'expected': True}],
  'hint': 'Постройте рёбра так же, как в предыдущей задаче, и поищите цикл поиском в глубину (состояния: не '
          'посещена, в стеке, закончена).'},
 {'id': 'd2-lock-compat',
  'mode': 'func',
  'func': 'can_grant',
  'title': 'Совместимость блокировок',
  'statement': 'Менеджер блокировок на один объект. held — список уже выданных блокировок [транзакция, '
               "режим], режим 'S' (разделяемая) или 'X' (исключительная). Напишите can_grant(held, tx, "
               'mode): можно ли выдать блокировку транзакции tx в режиме mode. Правила: S совместима с S; X '
               'несовместима ни с чем; блокировки самой tx не мешают ей же.',
  'starter': 'def can_grant(held, tx, mode):\n    pass\n',
  'tests': [{'args': [[], 1, 'X'], 'expected': True},
            {'args': [[[1, 'S'], [2, 'S']], 3, 'S'], 'expected': True},
            {'args': [[[1, 'S']], 2, 'X'], 'expected': False},
            {'args': [[[1, 'X']], 2, 'S'], 'expected': False},
            {'args': [[[1, 'S']], 1, 'X'], 'expected': True},
            {'args': [[[1, 'S'], [2, 'S']], 1, 'X'], 'expected': False},
            {'args': [[[1, 'X']], 1, 'S'], 'expected': True}],
  'hint': 'Проверяйте только чужие блокировки: если режим запроса X или чужая блокировка X — отказ.'},
 {'id': 'd2-deadlock',
  'mode': 'func',
  'func': 'find_deadlock',
  'title': 'Поиск взаимоблокировки',
  'statement': 'Граф ожиданий: словарь «транзакция → транзакция, которую она ждёт» (ключи — строки, например '
               '{"1": "2", "2": "1"}). Напишите find_deadlock(waits): отсортированный список транзакций, '
               'входящих в цикл ожидания, или [] если цикла нет (каждая транзакция ждёт не больше одной).',
  'starter': 'def find_deadlock(waits):\n    pass\n',
  'tests': [{'args': [{'1': '2', '2': '1'}], 'expected': ['1', '2']},
            {'args': [{'1': '2', '2': '3', '3': '1'}], 'expected': ['1', '2', '3']},
            {'args': [{'1': '2', '2': '3'}], 'expected': []},
            {'args': [{}], 'expected': []},
            {'args': [{'1': '2', '2': '3', '3': '2', '4': '1'}], 'expected': ['2', '3']},
            {'args': [{'5': '5'}], 'expected': ['5']}],
  'hint': 'Идите по цепочке ожиданий, запоминая посещённые; если вернулись в уже виденную транзакцию — это '
          'цикл.'},
 {'id': 'd2-mvcc-visible',
  'mode': 'func',
  'func': 'visible',
  'title': 'Видимость версий строки (MVCC)',
  'statement': 'Версия строки — [xmin, xmax, значение], xmax = 0, если версия не удалена. Снимок: committed '
               '— список номеров зафиксировавшихся транзакций, me — номер текущей. Версия видна, если '
               'создана зафиксированной транзакцией или самой me, и не удалена зафиксированной транзакцией '
               'или самой me. Напишите visible(versions, committed, me): список значений видимых версий в '
               'исходном порядке.',
  'starter': 'def visible(versions, committed, me):\n    pass\n',
  'tests': [{'args': [[[10, 25, 100], [25, 0, 70]], [10, 25], 30], 'expected': [70]},
            {'args': [[[10, 25, 100], [25, 0, 70]], [10], 30], 'expected': [100]},
            {'args': [[[10, 0, 5]], [], 10], 'expected': [5]},
            {'args': [[[10, 25, 100], [25, 0, 70]], [10, 25], 25], 'expected': [70]},
            {'args': [[[1, 0, 'a'], [2, 3, 'b'], [3, 0, 'c']], [1, 2], 9], 'expected': ['a', 'b']},
            {'args': [[], [1], 1], 'expected': []}],
  'hint': 'Два независимых условия: создана видимой транзакцией и не удалена видимой транзакцией.'},
 {'id': 'd2-dirty-reads',
  'mode': 'func',
  'func': 'dirty_reads',
  'title': 'Поиск грязных чтений',
  'statement': "История одного объекта: события [тип, транзакция]: ['w', t] — запись, ['r', t] — чтение, "
               "['c', t] — фиксация, ['a', t] — откат. Грязное чтение — когда транзакция читает объект, "
               'последнюю запись которого сделала другая, ещё не зафиксированная и не откатанная транзакция. '
               'Напишите dirty_reads(history): отсортированный список уникальных пар [читатель, писатель].',
  'starter': 'def dirty_reads(history):\n    pass\n',
  'tests': [{'args': [[['w', 2], ['r', 1], ['a', 2]]], 'expected': [[1, 2]]},
            {'args': [[['w', 2], ['c', 2], ['r', 1]]], 'expected': []},
            {'args': [[['w', 1], ['r', 1]]], 'expected': []},
            {'args': [[['w', 1], ['r', 2], ['r', 3], ['c', 1]]], 'expected': [[2, 1], [3, 1]]},
            {'args': [[]], 'expected': []},
            {'args': [[['w', 1], ['w', 2], ['r', 3], ['c', 2], ['c', 1]]], 'expected': [[3, 2]]}],
  'hint': 'Храните автора последней записи и множество незавершённых транзакций; чтение чужой незавершённой '
          'записи — находка.'},
 {'id': 'd2-lost-update',
  'mode': 'func',
  'func': 'final_balance',
  'title': 'Симуляция потерянного обновления',
  'statement': "Два клиента делают «прочитать, прибавить, записать». Шаги — список ['r', клиент] (прочитать "
               "текущее значение в локальную переменную) и ['w', клиент, дельта] (записать локальное "
               'значение + дельта). Напишите final_balance(start, steps): значение после всех шагов. Клиент '
               'читает один раз перед записью.',
  'starter': 'def final_balance(start, steps):\n    pass\n',
  'tests': [{'args': [100, [['r', 'a'], ['w', 'a', 10], ['r', 'b'], ['w', 'b', 10]]], 'expected': 120},
            {'args': [100, [['r', 'a'], ['r', 'b'], ['w', 'a', 10], ['w', 'b', 10]]], 'expected': 110},
            {'args': [0, [['r', 'a'], ['r', 'b'], ['r', 'c'], ['w', 'c', 5], ['w', 'b', 5], ['w', 'a', 5]]],
             'expected': 5},
            {'args': [50, []], 'expected': 50},
            {'args': [10, [['r', 'x'], ['w', 'x', -4]]], 'expected': 6}],
  'hint': 'Каждый клиент хранит своё прочитанное значение; запись затирает общее значение, не учитывая чужие '
          'изменения.'},
 {'id': 'd2-apply-atomic',
  'mode': 'func',
  'func': 'apply_atomic',
  'title': 'Атомарное применение переводов',
  'statement': 'Остатки — словарь «счёт → сумма» (строковые ключи). Переводы — список [откуда, куда, сумма]. '
               'Примените все переводы по порядку как одну транзакцию: если какой-то перевод сделал бы '
               'остаток отрицательным, откатите всё и верните исходные остатки; иначе верните новые. '
               'Напишите apply_atomic(balances, transfers).',
  'starter': 'def apply_atomic(balances, transfers):\n    pass\n',
  'tests': [{'args': [{'a': 100, 'b': 0}, [['a', 'b', 30], ['b', 'a', 10]]], 'expected': {'a': 80, 'b': 20}},
            {'args': [{'a': 100, 'b': 0}, [['a', 'b', 30], ['b', 'a', 50]]], 'expected': {'a': 100, 'b': 0}},
            {'args': [{'a': 10, 'b': 10}, []], 'expected': {'a': 10, 'b': 10}},
            {'args': [{'a': 5, 'b': 5, 'c': 0}, [['a', 'b', 5], ['b', 'c', 10], ['c', 'a', 10]]],
             'expected': {'a': 10, 'b': 0, 'c': 0}}],
  'hint': 'Работайте с копией словаря; при первом отрицательном остатке верните исходный словарь.'},
 {'id': 'd2-version-check',
  'mode': 'func',
  'func': 'optimistic_apply',
  'title': 'Оптимистичные обновления',
  'statement': 'Строки — словарь «id → [версия, значение]» (ключи строковые). Обновления — список [id, '
               'ожидаемая_версия, новое_значение]. Каждое обновление срабатывает, только если версия строки '
               'равна ожидаемой: тогда значение заменяется, а версия растёт на 1. Напишите '
               'optimistic_apply(rows, updates): пару [итоговые_строки, число_конфликтов].',
  'starter': 'def optimistic_apply(rows, updates):\n    pass\n',
  'tests': [{'args': [{'7': [1, 'a']}, [['7', 1, 'b'], ['7', 1, 'c']]], 'expected': [{'7': [2, 'b']}, 1]},
            {'args': [{'7': [1, 'a']}, [['7', 1, 'b'], ['7', 2, 'c']]], 'expected': [{'7': [3, 'c']}, 0]},
            {'args': [{'1': [3, 'x'], '2': [1, 'y']}, [['1', 3, 'z'], ['2', 2, 'q'], ['9', 1, 'n']]],
             'expected': [{'1': [4, 'z'], '2': [1, 'y']}, 2]},
            {'args': [{}, []], 'expected': [{}, 0]}],
  'hint': 'Сравнивайте версию с ожидаемой; несовпадение (или отсутствие строки) — конфликт, строка не '
          'меняется.'},
 {'id': 'd2-backoff',
  'mode': 'func',
  'func': 'backoff',
  'title': 'Задержки между повторами',
  'statement': 'После ошибки сериализации транзакцию повторяют с экспоненциальной задержкой. Напишите '
               'backoff(tries, base, cap): список задержек для tries повторов — base, 2·base, 4·base, … но '
               'не больше cap.',
  'starter': 'def backoff(tries, base, cap):\n    pass\n',
  'tests': [{'args': [5, 10, 100], 'expected': [10, 20, 40, 80, 100]},
            {'args': [0, 10, 100], 'expected': []},
            {'args': [3, 1, 1000], 'expected': [1, 2, 4]},
            {'args': [6, 50, 400], 'expected': [50, 100, 200, 400, 400, 400]},
            {'args': [1, 500, 100], 'expected': [100]}],
  'hint': 'Задержка номер i равна base * 2**i, ограниченная сверху значением cap.'},
 {'id': 'd2-isolation-levels',
  'mode': 'func',
  'func': 'allowed_anomalies',
  'title': 'Аномалии по уровням изоляции',
  'statement': 'Для уровня изоляции (строка) верните отсортированный список аномалий, которые он допускает '
               "по стандарту SQL, из набора: 'dirty', 'non_repeatable', 'phantom'. Уровни: 'READ "
               "UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ', 'SERIALIZABLE'. Напишите "
               'allowed_anomalies(level).',
  'starter': 'def allowed_anomalies(level):\n    pass\n',
  'tests': [{'args': ['READ UNCOMMITTED'], 'expected': ['dirty', 'non_repeatable', 'phantom']},
            {'args': ['READ COMMITTED'], 'expected': ['non_repeatable', 'phantom']},
            {'args': ['REPEATABLE READ'], 'expected': ['phantom']},
            {'args': ['SERIALIZABLE'], 'expected': []}],
  'hint': 'Чем выше уровень, тем меньше аномалий: заведите словарь «уровень → список».'},
 {'id': 'd2-lock-order',
  'mode': 'func',
  'func': 'lock_order',
  'title': 'Единый порядок блокировок',
  'statement': 'Чтобы избежать дедлоков, все транзакции берут блокировки в одном порядке — по возрастанию '
               'номера строки. Напишите lock_order(requests): для каждого запроса (списка номеров строк, '
               'которые нужно заблокировать) верните отсортированный список без повторов; результат — список '
               'таких списков.',
  'starter': 'def lock_order(requests):\n    pass\n',
  'tests': [{'args': [[[3, 1, 2], [2, 1]]], 'expected': [[1, 2, 3], [1, 2]]},
            {'args': [[[5, 5, 5]]], 'expected': [[5]]},
            {'args': [[]], 'expected': []},
            {'args': [[[10, 2], [7], []]], 'expected': [[2, 10], [7], []]}],
  'hint': 'sorted(set(r)) даёт строки по возрастанию без повторов.'}]}
