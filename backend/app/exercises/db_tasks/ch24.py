"""Задачи книги «Базы данных»: глава 24."""

TASKS: dict[int, list[dict]] = {24: [{'id': 'd8-orphans',
  'mode': 'sql',
  'title': 'Осиротевшие строки',
  'statement': 'Внешних ключей нет, и данные могли разойтись. Найдите заказы, ссылающиеся на несуществующих '
               'клиентов: колонка id, по возрастанию.',
  'starter': '-- заказы без клиента\nSELECT\n',
  'setup': 'CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, total INTEGER NOT '
           'NULL);\n'
           "INSERT INTO customers VALUES (1,'Анна'),(2,'Борис');\n"
           'INSERT INTO orders VALUES (1,1,100),(2,2,50),(3,3,70),(4,9,10),(5,1,5);\n',
  'expected': [[3], [4]],
  'expected_cols': ['id'],
  'hint': 'LEFT JOIN и условие c.id IS NULL, либо NOT EXISTS.',
  'ordered': True},
 {'id': 'd8-duplicates',
  'mode': 'sql',
  'title': 'Дубликаты после повторной доставки',
  'statement': 'Сообщения доставлялись «хотя бы раз». Выведите op_id, пришедшие больше одного раза, и '
               'сколько раз (колонки: op_id, n), по op_id.',
  'starter': '-- дубли по op_id\nSELECT\n',
  'setup': 'CREATE TABLE events (id INTEGER PRIMARY KEY, op_id TEXT NOT NULL, amount INTEGER NOT NULL);\n'
           'INSERT INTO events VALUES '
           "(1,'a',100),(2,'b',50),(3,'a',100),(4,'c',70),(5,'b',50),(6,'a',100);\n",
  'expected': [['a', 3], ['b', 2]],
  'expected_cols': ['op_id', 'n'],
  'hint': 'GROUP BY op_id HAVING COUNT(*) > 1.',
  'ordered': True},
 {'id': 'd8-dedupe-delete',
  'mode': 'sql',
  'title': 'Очистка дублей',
  'statement': 'Оставьте для каждого op_id только самое раннее событие (с наименьшим id) и удалите '
               'остальные. Итог проверяется по таблице.',
  'starter': '-- удалить дубли, оставив самую раннюю строку на op_id\nDELETE\n',
  'setup': 'CREATE TABLE events (id INTEGER PRIMARY KEY, op_id TEXT NOT NULL, amount INTEGER NOT NULL);\n'
           'INSERT INTO events VALUES '
           "(1,'a',100),(2,'b',50),(3,'a',100),(4,'c',70),(5,'b',50),(6,'a',100);\n",
  'expected': [[1, 'a'], [2, 'b'], [4, 'c']],
  'expected_cols': ['id', 'op_id'],
  'hint': 'DELETE … WHERE id NOT IN (SELECT MIN(id) … GROUP BY op_id).',
  'ordered': True,
  'check': 'SELECT id, op_id FROM events ORDER BY id'},
 {'id': 'd8-outbox',
  'mode': 'sql',
  'title': 'Outbox в одной транзакции',
  'statement': 'В одной транзакции создайте заказ (id 1, total 500) и добавьте в outbox событие: topic = '
               '\'order.created\', payload = \'{"id":1}\'. Итог проверяется по обеим таблицам: заказ и одно '
               'неотправленное событие.',
  'starter': '-- заказ и событие — в одной транзакции\nBEGIN;\n',
  'setup': 'CREATE TABLE orders (id INTEGER PRIMARY KEY, total INTEGER NOT NULL);\n'
           'CREATE TABLE outbox (id INTEGER PRIMARY KEY AUTOINCREMENT, topic TEXT NOT NULL, payload TEXT NOT '
           'NULL, sent INTEGER NOT NULL DEFAULT 0);\n',
  'expected': [[1, 1]],
  'expected_cols': ['(SELECT COUNT(*) FROM orders)', '(SELECT COUNT(*) FROM outbox WHERE sent = 0)'],
  'hint': 'BEGIN; INSERT в orders; INSERT в outbox; COMMIT; — событие не потеряется, если заказ записан.',
  'check': 'SELECT (SELECT COUNT(*) FROM orders), (SELECT COUNT(*) FROM outbox WHERE sent = 0)'},
 {'id': 'd8-latest-per-key',
  'mode': 'sql',
  'title': 'Последнее значение по ключу',
  'statement': 'Реплика получила версии значений в произвольном порядке. Для каждого ключа выведите значение '
               'с наибольшим ts (last write wins): колонки key, value; по ключу.',
  'starter': '-- последняя версия каждого ключа\nSELECT\n',
  'setup': 'CREATE TABLE versions (key TEXT NOT NULL, ts INTEGER NOT NULL, value TEXT NOT NULL);\n'
           'INSERT INTO versions VALUES '
           "('a',1,'x'),('a',5,'y'),('b',2,'p'),('a',3,'z'),('b',9,'q'),('c',4,'only');\n",
  'expected': [['a', 'y'], ['b', 'q'], ['c', 'only']],
  'expected_cols': ['key', 'value'],
  'hint': 'Коррелированный подзапрос на MAX(ts) по ключу — или оконная функция ROW_NUMBER().',
  'ordered': True},
 {'id': 'd8-lamport',
  'mode': 'func',
  'func': 'lamport_run',
  'title': 'Часы Лампорта',
  'statement': "События: ['local', узел], ['send', узел, id] — отправка (счётчик +1, сообщение с id "
               "запоминает текущее значение) и ['recv', узел, id] — получение (счётчик = max(свой, значение "
               'сообщения) + 1). Счётчики узлов стартуют с 0. Напишите lamport_run(events): список значений '
               'счётчика после каждого события.',
  'starter': 'def lamport_run(events):\n    pass\n',
  'tests': [{'args': [[['local', 'A'], ['send', 'A', 'm1'], ['recv', 'B', 'm1'], ['local', 'B']]],
             'expected': [1, 2, 3, 4]},
            {'args': [[['send', 'A', 'x'], ['send', 'A', 'y'], ['recv', 'B', 'y'], ['recv', 'B', 'x']]],
             'expected': [1, 2, 3, 4]},
            {'args': [[]], 'expected': []},
            {'args': [[['local', 'A'], ['local', 'A'], ['local', 'B']]], 'expected': [1, 2, 1]}],
  'hint': 'Для recv берётся максимум из своего счётчика и записанного при отправке, затем +1.'},
 {'id': 'd8-vector-step',
  'mode': 'func',
  'func': 'vc_events',
  'title': 'Векторные часы событий',
  'statement': "События: ['local', узел], ['send', узел, id], ['recv', узел, id]. Вектор — словарь «узел → "
               'счётчик». Событие увеличивает счётчик своего узла на 1; при send вектор копируется в '
               'сообщение id (после увеличения); при recv сначала берутся покомпонентные максимумы с '
               'вектором сообщения, потом счётчик своего узла +1. Напишите vc_events(events): список '
               'векторов (словарей) после каждого события.',
  'starter': 'def vc_events(events):\n    pass\n',
  'tests': [{'args': [[['local', 'A'], ['send', 'A', 'm'], ['recv', 'B', 'm']]],
             'expected': [{'A': 1}, {'A': 2}, {'A': 2, 'B': 1}]},
            {'args': [[['send', 'A', 'x'], ['send', 'B', 'y'], ['recv', 'A', 'y'], ['recv', 'B', 'x']]],
             'expected': [{'A': 1}, {'B': 1}, {'A': 2, 'B': 1}, {'B': 2, 'A': 1}]},
            {'args': [[]], 'expected': []}],
  'hint': 'Копируйте словари; при получении объединяйте максимумами, затем увеличивайте свой компонент.'},
 {'id': 'd8-linearizable',
  'mode': 'func',
  'func': 'is_linearizable',
  'title': 'Линеаризуем ли регистр',
  'statement': "Операции над одним регистром (изначально 0): ['w', старт, конец, значение] и ['r', старт, "
               'конец, прочитанное]. Операция возможна в любой момент между стартом и концом. История '
               'линеаризуема, если существует порядок операций, при котором каждое чтение видит последнюю '
               'запись перед ним, а если конец одной операции раньше старта другой (a.конец < b.старт), то a '
               'идёт раньше b. Напишите is_linearizable(ops): True/False (операций не больше шести — '
               'допустим перебор).',
  'starter': 'def is_linearizable(ops):\n    pass\n',
  'tests': [{'args': [[['w', 0, 1, 5], ['r', 2, 3, 5]]], 'expected': True},
            {'args': [[['w', 0, 1, 5], ['r', 2, 3, 0]]], 'expected': False},
            {'args': [[['w', 0, 5, 5], ['r', 1, 2, 0], ['r', 3, 4, 5]]], 'expected': True},
            {'args': [[['w', 0, 1, 1], ['w', 2, 3, 2], ['r', 4, 5, 1]]], 'expected': False},
            {'args': [[]], 'expected': True},
            {'args': [[['w', 0, 10, 1], ['r', 1, 2, 1], ['r', 3, 4, 0]]], 'expected': False}],
  'hint': 'Переберите перестановки: порядок должен уважать реальное время, а чтения — совпадать с последним '
          'записанным значением.'},
 {'id': 'd8-majority',
  'mode': 'func',
  'func': 'majority_info',
  'title': 'Большинство и отказы',
  'statement': 'Напишите majority_info(n): пару [размер большинства (n // 2 + 1), сколько отказов переживает '
               'кластер (n − большинство)].',
  'starter': 'def majority_info(n):\n    pass\n',
  'tests': [{'args': [3], 'expected': [2, 1]},
            {'args': [5], 'expected': [3, 2]},
            {'args': [4], 'expected': [3, 1]},
            {'args': [1], 'expected': [1, 0]},
            {'args': [7], 'expected': [4, 3]}],
  'hint': 'Большинство — n // 2 + 1; остальные узлы могут отказать.'},
 {'id': 'd8-available',
  'mode': 'func',
  'func': 'can_serve',
  'title': 'Доступность при разделении',
  'statement': "Сеть разделилась; в «моей» части up узлов из n. Режим 'cp' обслуживает запрос, только если в "
               "этой части большинство узлов; режим 'ap' обслуживает, если в части есть хотя бы один узел. "
               'Напишите can_serve(mode, n, up): True/False.',
  'starter': 'def can_serve(mode, n, up):\n    pass\n',
  'tests': [{'args': ['cp', 5, 3], 'expected': True},
            {'args': ['cp', 5, 2], 'expected': False},
            {'args': ['ap', 5, 2], 'expected': True},
            {'args': ['ap', 5, 0], 'expected': False},
            {'args': ['cp', 4, 2], 'expected': False},
            {'args': ['cp', 1, 1], 'expected': True}],
  'hint': 'CP — нужно строгое большинство; AP — достаточно одного живого узла.'},
 {'id': 'd8-raft-vote',
  'mode': 'func',
  'func': 'grant_vote',
  'title': 'Раф: отдать ли голос',
  'statement': 'Узел отдаёт голос кандидату, если срок кандидата не меньше собственного, в этом сроке он ещё '
               'ни за кого не голосовал (или голосовал за этого же кандидата), и журнал кандидата не '
               'отстаёт: последний срок в журнале кандидата больше, либо равен при длине журнала не меньшей. '
               'Напишите grant_vote(my_term, my_voted_for, my_last, cand_id, cand_term, cand_last): '
               'True/False, где *_last — пара [срок последней записи, длина журнала], my_voted_for — '
               'идентификатор или None.',
  'starter': 'def grant_vote(my_term, my_voted_for, my_last, cand_id, cand_term, cand_last):\n    pass\n',
  'tests': [{'args': [3, None, [2, 5], 'B', 4, [2, 5]], 'expected': True},
            {'args': [3, 'A', [2, 5], 'B', 3, [2, 9]], 'expected': False},
            {'args': [3, 'B', [2, 5], 'B', 3, [2, 5]], 'expected': True},
            {'args': [3, None, [2, 5], 'B', 4, [1, 99]], 'expected': False},
            {'args': [5, None, [2, 5], 'B', 4, [2, 5]], 'expected': False},
            {'args': [3, None, [2, 5], 'B', 4, [3, 1]], 'expected': True},
            {'args': [3, None, [2, 5], 'B', 4, [2, 4]], 'expected': False}],
  'hint': 'Три проверки: срок, повторное голосование и актуальность журнала (сначала срок последней записи, '
          'потом длина).'},
 {'id': 'd8-raft-commit',
  'mode': 'func',
  'func': 'commit_index',
  'title': 'Индекс фиксации',
  'statement': 'Лидер знает, до какой записи журнала реплицировался каждый узел (список match, включая '
               'лидера). Запись зафиксирована, если она есть у большинства. Напишите commit_index(match): '
               'наибольший индекс, который есть как минимум у большинства узлов (0, если никакой).',
  'starter': 'def commit_index(match):\n    pass\n',
  'tests': [{'args': [[7, 7, 5]], 'expected': 7},
            {'args': [[7, 4, 3]], 'expected': 4},
            {'args': [[9, 9, 9, 1, 1]], 'expected': 9},
            {'args': [[0, 0, 0]], 'expected': 0},
            {'args': [[5]], 'expected': 5},
            {'args': [[6, 5, 4, 3]], 'expected': 4}],
  'hint': 'Отсортируйте по убыванию: нужный индекс — элемент с номером len // 2.'},
 {'id': 'd8-idempotent',
  'mode': 'func',
  'func': 'process_events',
  'title': 'Идемпотентная обработка',
  'statement': 'События — список [op_id, счёт, сумма] (может содержать повторы op_id из-за повторной '
               'доставки). Каждый op_id обрабатывается только один раз (первое появление). Напишите '
               'process_events(events): словарь «счёт → итоговая сумма».',
  'starter': 'def process_events(events):\n    pass\n',
  'tests': [{'args': [[['a', 'x', 100], ['b', 'x', 50], ['a', 'x', 100], ['c', 'y', 7]]],
             'expected': {'x': 150, 'y': 7}},
            {'args': [[]], 'expected': {}},
            {'args': [[['z', 'q', 1], ['z', 'q', 1], ['z', 'q', 1]]], 'expected': {'q': 1}}],
  'hint': 'Множество уже виденных op_id: повторы пропускаем.'},
 {'id': 'd8-causal-delivery',
  'mode': 'func',
  'func': 'causal_order',
  'title': 'Причинная доставка',
  'statement': 'Сообщения — список [id, зависит_от или None] в порядке прихода. Сообщение можно показать, '
               'только если сообщение, от которого оно зависит, уже показано. Напишите causal_order(msgs): '
               'список id в порядке показа; сообщение, чья причина ещё не пришла, ждёт и показывается сразу '
               'после неё (в порядке прихода, если несколько ждут одну причину).',
  'starter': 'def causal_order(msgs):\n    pass\n',
  'tests': [{'args': [[['a', None], ['c', 'b'], ['b', 'a']]], 'expected': ['a', 'b', 'c']},
            {'args': [[['x', None], ['y', 'x'], ['z', 'y']]], 'expected': ['x', 'y', 'z']},
            {'args': [[['z', 'y'], ['y', 'x'], ['x', None]]], 'expected': ['x', 'y', 'z']},
            {'args': [[]], 'expected': []},
            {'args': [[['q', 'nope']]], 'expected': []}],
  'hint': 'Держите список ожидающих и после показа каждого сообщения освобождайте тех, кто ждал именно его.'},
 {'id': 'd8-sloppy',
  'mode': 'func',
  'func': 'write_targets',
  'title': 'Нестрогий кворум',
  'statement': 'Для записи выбирается W живых узлов: сначала «домашние» (в порядке списка home), а если '
               'домашних живых меньше W — добираются живые соседи (список neighbors) по порядку. Напишите '
               'write_targets(home, neighbors, alive, w): список выбранных узлов (может быть короче w, если '
               'живых не хватает).',
  'starter': 'def write_targets(home, neighbors, alive, w):\n    pass\n',
  'tests': [{'args': [['a', 'b', 'c'], ['d', 'e'], ['a', 'b', 'c', 'd'], 2], 'expected': ['a', 'b']},
            {'args': [['a', 'b', 'c'], ['d', 'e'], ['a', 'd', 'e'], 3], 'expected': ['a', 'd', 'e']},
            {'args': [['a', 'b'], ['c'], [], 2], 'expected': []},
            {'args': [['a'], ['b'], ['a', 'b'], 2], 'expected': ['a', 'b']}],
  'hint': 'Сначала домашние живые узлы, затем живые соседи, пока не наберётся w.'},
 {'id': 'd8-lww-convergence',
  'mode': 'func',
  'func': 'converge',
  'title': 'Сходимость реплик',
  'statement': 'Три реплики получили набор записей [ключ, значение, время] в разном порядке. Правило: '
               'побеждает запись с большим временем (при равенстве — большее значение как строка). Напишите '
               'converge(replica_logs): словарь «ключ → значение», к которому придут все реплики после '
               'обмена, если объединить записи всех реплик.',
  'starter': 'def converge(replica_logs):\n    pass\n',
  'tests': [{'args': [[[['a', '1', 1], ['b', 'x', 5]], [['a', '2', 3]], [['b', 'y', 5], ['c', 'z', 1]]]],
             'expected': {'a': '2', 'b': 'y', 'c': 'z'}},
            {'args': [[[], []]], 'expected': {}},
            {'args': [[[['k', 'v', 1]], [['k', 'v', 1]]]], 'expected': {'k': 'v'}}],
  'hint': 'Для каждого ключа сохраняйте лучшую запись по паре (время, значение).'},
 {'id': 'd8-clock-skew',
  'mode': 'func',
  'func': 'safe_after',
  'title': 'Ожидание погрешности часов',
  'statement': 'Часы узла показывают now с погрешностью ±eps. Чтобы утверждать, что событие в момент ts '
               'точно произошло в прошлом, нужно подождать, пока now − eps > ts. Напишите safe_after(ts, '
               'now, eps): сколько ещё ждать (в тех же единицах, не меньше нуля).',
  'starter': 'def safe_after(ts, now, eps):\n    pass\n',
  'tests': [{'args': [100, 105, 3], 'expected': 0},
            {'args': [100, 101, 3], 'expected': 2},
            {'args': [100, 200, 3], 'expected': 0},
            {'args': [0, 0, 0], 'expected': 0},
            {'args': [50, 50, 7], 'expected': 7}],
  'hint': 'Нужно now − eps > ts, то есть ждать, пока now не дойдёт до ts + eps.'},
 {'id': 'd8-pacelc',
  'mode': 'func',
  'func': 'choose_mode',
  'title': 'PACELC: что выбрать',
  'statement': 'Напишите choose_mode(partitioned, prefer): partitioned — разделена ли сеть (True/False), '
               "prefer — 'consistency' или 'availability' (для неразделённой сети — 'consistency' или "
               "'latency'). Верните строку: при разделении 'CP' или 'AP', без разделения 'EC' "
               "(согласованность) или 'EL' (задержка).",
  'starter': 'def choose_mode(partitioned, prefer):\n    pass\n',
  'tests': [{'args': [True, 'consistency'], 'expected': 'CP'},
            {'args': [True, 'availability'], 'expected': 'AP'},
            {'args': [False, 'consistency'], 'expected': 'EC'},
            {'args': [False, 'latency'], 'expected': 'EL'}],
  'hint': 'Четыре комбинации — по двум условиям.'}]}
