"""Задачи книги «Базы данных»: глава 22."""

TASKS: dict[int, list[dict]] = {22: [{'id': 'd6-lag',
  'mode': 'sql',
  'title': 'Отставание реплик',
  'statement': 'Таблица replicas(name, role, applied_lsn, alive). Номер последней записи лидера — '
               "applied_lsn строки с role = 'leader'. Выведите живые реплики (role = 'replica', alive = 1) и "
               'их отставание в записях (колонки: name, lag), по убыванию отставания, при равенстве — по '
               'имени.',
  'starter': '-- живые реплики и их отставание\nSELECT\n',
  'setup': 'CREATE TABLE replicas (name TEXT PRIMARY KEY, role TEXT NOT NULL, applied_lsn INTEGER NOT NULL, '
           'alive INTEGER NOT NULL);\n'
           'INSERT INTO replicas VALUES '
           "('db1','leader',1200,1),('db2','replica',1198,1),('db3','replica',1150,1),('db4','replica',1200,0),('db5','replica',1199,1);\n",
  'expected': [['db3', 50], ['db2', 2], ['db5', 1]],
  'expected_cols': ['name', 'lag'],
  'hint': 'Номер лидера берём подзапросом; для каждой реплики lag = lsn лидера − её applied_lsn.',
  'ordered': True},
 {'id': 'd6-failover-candidate',
  'mode': 'sql',
  'title': 'Кого назначить лидером',
  'statement': 'Лидер db1 упал. Выберите нового: среди живых реплик самую свежую (наибольший applied_lsn); '
               'при равенстве — с меньшим именем. Выведите одну строку: name.',
  'starter': '-- кандидат в новые лидеры\nSELECT\n',
  'setup': 'CREATE TABLE replicas (name TEXT PRIMARY KEY, role TEXT NOT NULL, applied_lsn INTEGER NOT NULL, '
           'alive INTEGER NOT NULL);\n'
           'INSERT INTO replicas VALUES '
           "('db1','leader',1200,1),('db2','replica',1198,1),('db3','replica',1150,1),('db4','replica',1200,0),('db5','replica',1199,1);\n",
  'expected': [['db5']],
  'expected_cols': ['name'],
  'hint': "Фильтр: role = 'replica' AND alive = 1; сортировка по applied_lsn по убыванию, LIMIT 1.",
  'ordered': True},
 {'id': 'd6-read-eligible',
  'mode': 'sql',
  'title': 'Реплики для чтения своих записей',
  'statement': 'Клиент только что записал данные, получив LSN 1199. Выведите живые реплики (не лидера), '
               'которые уже применили этот LSN (applied_lsn ≥ 1199), по имени: колонка name.',
  'starter': '-- реплики, на которых можно читать свои записи\nSELECT\n',
  'setup': 'CREATE TABLE replicas (name TEXT PRIMARY KEY, role TEXT NOT NULL, applied_lsn INTEGER NOT NULL, '
           'alive INTEGER NOT NULL);\n'
           'INSERT INTO replicas VALUES '
           "('db1','leader',1200,1),('db2','replica',1198,1),('db3','replica',1150,1),('db4','replica',1200,0),('db5','replica',1199,1);\n",
  'expected': [['db5']],
  'expected_cols': ['name'],
  'hint': 'Условие applied_lsn >= 1199 плюс фильтры по роли и живости.',
  'ordered': True},
 {'id': 'd6-apply-log',
  'mode': 'func',
  'func': 'apply_log',
  'title': 'Реплика применяет журнал',
  'statement': "Журнал репликации — список записей [lsn, операция, ключ, значение]: операция 'set' или 'del' "
               '(у del значение None). Реплика применяет их строго по возрастанию lsn, пропуская записи с '
               'lsn не больше уже применённого. Напишите apply_log(state, applied_lsn, log): пара [новое '
               'состояние (словарь), новый applied_lsn]; исходное состояние не меняйте.',
  'starter': 'def apply_log(state, applied_lsn, log):\n    pass\n',
  'tests': [{'args': [{'a': 1}, 10, [[11, 'set', 'b', 2], [12, 'del', 'a', None]]],
             'expected': [{'b': 2}, 12]},
            {'args': [{'a': 1}, 10, [[9, 'set', 'a', 5], [10, 'set', 'a', 6]]], 'expected': [{'a': 1}, 10]},
            {'args': [{}, 0, [[3, 'set', 'x', 1], [1, 'set', 'x', 0]]], 'expected': [{'x': 1}, 3]},
            {'args': [{'k': 1}, 5, []], 'expected': [{'k': 1}, 5]}],
  'hint': 'Отсортируйте журнал, пропускайте записи с lsn ≤ уже применённого, обновляйте счётчик после '
          'применения.'},
 {'id': 'd6-ack-time',
  'mode': 'func',
  'func': 'commit_ack_time',
  'title': 'Когда подтвердится запись',
  'statement': 'Лидер записывает локально за local мс, ответы реплик приходят через acks мс после начала '
               "записи (список). Режимы: 'async' — подтверждение сразу после локальной записи; 'sync' — "
               "после ответов всех реплик; 'quorum' с числом k — после k самых быстрых ответов (но не раньше "
               'локальной записи). Напишите commit_ack_time(mode, k, local, acks): время подтверждения '
               'клиенту в мс.',
  'starter': 'def commit_ack_time(mode, k, local, acks):\n    pass\n',
  'tests': [{'args': ['async', 0, 2, [10, 30]], 'expected': 2},
            {'args': ['sync', 0, 2, [10, 30]], 'expected': 30},
            {'args': ['quorum', 1, 2, [10, 30]], 'expected': 10},
            {'args': ['quorum', 2, 2, [10, 30, 5]], 'expected': 10},
            {'args': ['sync', 0, 50, [10, 30]], 'expected': 50},
            {'args': ['quorum', 1, 2, []], 'expected': 2}],
  'hint': 'Отсортируйте времена ответов: sync ждёт последнего, quorum k — k-го; результат не меньше local.'},
 {'id': 'd6-read-your-writes',
  'mode': 'func',
  'func': 'eligible_replicas',
  'title': 'Реплики, свежие для клиента',
  'statement': 'Реплики — словарь «имя → applied_lsn». Клиент знает LSN своей последней записи. Напишите '
               'eligible_replicas(replicas, client_lsn): отсортированный список имён реплик, у которых '
               'applied_lsn ≥ client_lsn.',
  'starter': 'def eligible_replicas(replicas, client_lsn):\n    pass\n',
  'tests': [{'args': [{'a': 100, 'b': 98, 'c': 105}, 100], 'expected': ['a', 'c']},
            {'args': [{'a': 1}, 2], 'expected': []},
            {'args': [{}, 5], 'expected': []},
            {'args': [{'x': 7, 'y': 7}, 7], 'expected': ['x', 'y']}],
  'hint': 'Простой фильтр по словарю с последующей сортировкой имён.'},
 {'id': 'd6-monotonic',
  'mode': 'func',
  'func': 'monotonic_violations',
  'title': 'Нарушения монотонности чтений',
  'statement': 'Лог чтений одного клиента — список [момент, версия, реплика]. Чтения монотонны, если версия '
               'никогда не уменьшается. Напишите monotonic_violations(reads): список номеров (с нуля) '
               'чтений, версия которых меньше максимальной из ранее выполненных чтений (читайте в порядке '
               'списка).',
  'starter': 'def monotonic_violations(reads):\n    pass\n',
  'tests': [{'args': [[[1, 5, 'a'], [2, 3, 'b'], [3, 5, 'a'], [4, 4, 'b']]], 'expected': [1, 3]},
            {'args': [[[1, 1, 'a'], [2, 2, 'a']]], 'expected': []},
            {'args': [[]], 'expected': []},
            {'args': [[[1, 9, 'x'], [2, 2, 'y'], [3, 1, 'z']]], 'expected': [1, 2]}],
  'hint': 'Храните максимальную увиденную версию; чтение с меньшей версией — нарушение.'},
 {'id': 'd6-pick-leader',
  'mode': 'func',
  'func': 'pick_leader',
  'title': 'Выбор нового лидера',
  'statement': 'Реплики — список [имя, applied_lsn, жива ли (True/False)]. Новый лидер — живая реплика с '
               'наибольшим applied_lsn; при равенстве — меньшее имя. Напишите pick_leader(replicas): имя или '
               'None, если живых нет.',
  'starter': 'def pick_leader(replicas):\n    pass\n',
  'tests': [{'args': [[['a', 10, True], ['b', 12, True], ['c', 12, False]]], 'expected': 'b'},
            {'args': [[['a', 5, False]]], 'expected': None},
            {'args': [[]], 'expected': None},
            {'args': [[['z', 7, True], ['m', 7, True]]], 'expected': 'm'}],
  'hint': 'min по паре (−lsn, имя) среди живых реплик даёт нужный порядок.'},
 {'id': 'd6-lost-writes',
  'mode': 'func',
  'func': 'lost_writes',
  'title': 'Что потеряется при фейловере',
  'statement': 'Подтверждённые клиентам записи лидера имеют номера 1..leader_lsn. Новый лидер применил '
               'только записи до new_lsn. Напишите lost_writes(leader_lsn, new_lsn, acked): список номеров '
               'записей, которые были подтверждены клиентам (список acked), но больше new_lsn — то есть '
               'потеряны, по возрастанию.',
  'starter': 'def lost_writes(leader_lsn, new_lsn, acked):\n    pass\n',
  'tests': [{'args': [10, 7, [5, 8, 9, 10]], 'expected': [8, 9, 10]},
            {'args': [10, 10, [1, 10]], 'expected': []},
            {'args': [5, 0, []], 'expected': []},
            {'args': [8, 6, [7, 8, 6]], 'expected': [7, 8]},
            {'args': [8, 3, [9]], 'expected': []}],
  'hint': 'Потеряны подтверждённые записи с номерами от new_lsn + 1 до leader_lsn.'},
 {'id': 'd6-fencing',
  'mode': 'func',
  'func': 'accept_writes',
  'title': 'Ограждение по эпохам',
  'statement': 'Хранилище запоминает наибольшую увиденную эпоху. Запись [эпоха, ключ, значение] принимается, '
               'если её эпоха не меньше наибольшей уже увиденной (и тогда запоминается), иначе отвергается. '
               'Напишите accept_writes(writes): пара [словарь принятых значений, список номеров (с нуля) '
               'отвергнутых записей].',
  'starter': 'def accept_writes(writes):\n    pass\n',
  'tests': [{'args': [[[3, 'a', 1], [4, 'a', 2], [3, 'a', 99], [4, 'b', 5]]],
             'expected': [{'a': 2, 'b': 5}, [2]]},
            {'args': [[[1, 'x', 1]]], 'expected': [{'x': 1}, []]},
            {'args': [[]], 'expected': [{}, []]},
            {'args': [[[2, 'k', 'n'], [1, 'k', 'old'], [2, 'k', 'm']]], 'expected': [{'k': 'm'}, [1]]}],
  'hint': 'Запоминайте максимальную эпоху; запись с меньшей эпохой отвергайте и фиксируйте её номер.'},
 {'id': 'd6-lww',
  'mode': 'func',
  'func': 'lww_merge',
  'title': 'Last write wins',
  'statement': 'Две реплики хранят словари «ключ → [время, значение, узел]». Напишите lww_merge(a, b): '
               'словарь, где для каждого ключа выбрана запись с большим временем; при равенстве времён — с '
               'большим именем узла (строки сравниваются лексикографически).',
  'starter': 'def lww_merge(a, b):\n    pass\n',
  'tests': [{'args': [{'x': [5, 'A', 'n1']}, {'x': [7, 'B', 'n2'], 'y': [1, 'Y', 'n2']}],
             'expected': {'x': [7, 'B', 'n2'], 'y': [1, 'Y', 'n2']}},
            {'args': [{'x': [5, 'A', 'n1']}, {'x': [5, 'B', 'n2']}], 'expected': {'x': [5, 'B', 'n2']}},
            {'args': [{}, {}], 'expected': {}},
            {'args': [{'k': [1, 'v', 'z']}, {}], 'expected': {'k': [1, 'v', 'z']}}],
  'hint': 'max по ключу (время, узел) среди записей этого ключа из обеих реплик.'},
 {'id': 'd6-quorum',
  'mode': 'func',
  'func': 'quorum_info',
  'title': 'Кворумы: что гарантируется',
  'statement': 'Напишите quorum_info(n, w, r): пару [читает ли свежее значение (w + r > n), нет ли '
               'конфликтов записи (w > n // 2, то есть записи пересекаются)].',
  'starter': 'def quorum_info(n, w, r):\n    pass\n',
  'tests': [{'args': [3, 2, 2], 'expected': [True, True]},
            {'args': [3, 1, 1], 'expected': [False, False]},
            {'args': [5, 3, 3], 'expected': [True, True]},
            {'args': [5, 5, 1], 'expected': [True, True]},
            {'args': [4, 2, 3], 'expected': [True, False]},
            {'args': [1, 1, 1], 'expected': [True, True]}],
  'hint': 'Две проверки: w + r > n и w > n // 2.'},
 {'id': 'd6-quorum-read',
  'mode': 'func',
  'func': 'quorum_read',
  'title': 'Чтение с кворумом',
  'statement': 'Реплики — список [версия, значение] (версия — число). Клиент опрашивает реплики с номерами '
               'из queried и берёт значение с наибольшей версией. Напишите quorum_read(replicas, queried): '
               'пару [значение, версия]. Если несколько с одной версией — берите любое (значения у них '
               'равны).',
  'starter': 'def quorum_read(replicas, queried):\n    pass\n',
  'tests': [{'args': [[[7, 'new'], [7, 'new'], [6, 'old']], [1, 2]], 'expected': ['new', 7]},
            {'args': [[[7, 'new'], [7, 'new'], [6, 'old']], [2]], 'expected': ['old', 6]},
            {'args': [[[1, 'a'], [3, 'c'], [2, 'b']], [0, 1, 2]], 'expected': ['c', 3]},
            {'args': [[[5, 'z']], [0]], 'expected': ['z', 5]}],
  'hint': 'Из опрошенных реплик выберите ту, у которой версия максимальна.'},
 {'id': 'd6-read-repair',
  'mode': 'func',
  'func': 'read_repair',
  'title': 'Read repair',
  'statement': 'Реплики — список [версия, значение]. После чтения клиент находит самую свежую версию среди '
               'опрошенных реплик (номера queried) и записывает её во все опрошенные реплики, у которых '
               'версия меньше. Напишите read_repair(replicas, queried): новый список реплик (неопрошенные не '
               'меняются).',
  'starter': 'def read_repair(replicas, queried):\n    pass\n',
  'tests': [{'args': [[[7, 'n'], [6, 'o'], [5, 'x']], [0, 1]], 'expected': [[7, 'n'], [7, 'n'], [5, 'x']]},
            {'args': [[[7, 'n'], [6, 'o'], [5, 'x']], [1, 2]], 'expected': [[7, 'n'], [6, 'o'], [6, 'o']]},
            {'args': [[[1, 'a'], [1, 'a']], [0, 1]], 'expected': [[1, 'a'], [1, 'a']]},
            {'args': [[[2, 'b']], [0]], 'expected': [[2, 'b']]}],
  'hint': 'Найдите лучшую копию среди опрошенных и перепишите ею отставшие опрошенные реплики.'},
 {'id': 'd6-vector-clock',
  'mode': 'func',
  'func': 'compare_vc',
  'title': 'Сравнение векторных часов',
  'statement': 'Вектор — словарь «узел → счётчик» (отсутствующий узел — 0). Напишите compare_vc(a, b): '
               "'equal', если векторы равны; 'before', если a предшествует b (все ≤ и хотя бы один <); "
               "'after', если b предшествует a; иначе 'concurrent'.",
  'starter': 'def compare_vc(a, b):\n    pass\n',
  'tests': [{'args': [{'A': 2, 'B': 1}, {'A': 2, 'B': 2}], 'expected': 'before'},
            {'args': [{'A': 3, 'B': 1}, {'A': 2, 'B': 2}], 'expected': 'concurrent'},
            {'args': [{'A': 1}, {'A': 1}], 'expected': 'equal'},
            {'args': [{'A': 2}, {'A': 1}], 'expected': 'after'},
            {'args': [{}, {'A': 1}], 'expected': 'before'},
            {'args': [{'A': 1, 'B': 0}, {'A': 1}], 'expected': 'equal'}],
  'hint': 'Проверьте, все ли компоненты a ≤ b и все ли ≥; комбинация ответов даёт один из четырёх '
          'результатов.'},
 {'id': 'd6-gcounter',
  'mode': 'func',
  'func': 'merge_counters',
  'title': 'CRDT: счётчик, который сливается',
  'statement': 'Растущий счётчик на нескольких узлах: у каждой реплики словарь «узел → сколько увеличил этот '
               'узел». Слияние — по каждому узлу берётся максимум. Напишите merge_counters(a, b): словарь '
               'слияния, и значением счётчика считается сумма по узлам; верните пару [слитый словарь, '
               'сумма].',
  'starter': 'def merge_counters(a, b):\n    pass\n',
  'tests': [{'args': [{'A': 3, 'B': 1}, {'A': 2, 'B': 4, 'C': 1}], 'expected': [{'C': 1, 'B': 4, 'A': 3}, 8]},
            {'args': [{}, {}], 'expected': [{}, 0]},
            {'args': [{'A': 5}, {'A': 5}], 'expected': [{'A': 5}, 5]},
            {'args': [{'X': 1}, {'Y': 2}], 'expected': [{'X': 1, 'Y': 2}, 3]}],
  'hint': 'Максимум по каждому узлу не теряет приращений и делает слияние идемпотентным.'},
 {'id': 'd6-heartbeat',
  'mode': 'func',
  'func': 'suspected',
  'title': 'Обнаружение отказов по heartbeat',
  'statement': 'Узлы — словарь «имя → время последнего сигнала». Узел считается подозрительным, если now − '
               'last > timeout. Напишите suspected(last_seen, now, timeout): отсортированный список '
               'подозрительных узлов.',
  'starter': 'def suspected(last_seen, now, timeout):\n    pass\n',
  'tests': [{'args': [{'a': 95, 'b': 80, 'c': 99}, 100, 10], 'expected': ['b']},
            {'args': [{}, 100, 10], 'expected': []},
            {'args': [{'a': 90}, 100, 10], 'expected': []},
            {'args': [{'a': 89}, 100, 10], 'expected': ['a']}],
  'hint': 'Подозрительны узлы, у которых now − last строго больше timeout.'},
 {'id': 'd6-replica-placement',
  'mode': 'func',
  'func': 'replicas_for',
  'title': 'Куда положить копии',
  'statement': 'Узлы стоят на кольце в порядке списка ring (уже отсортирован по позиции). Ключ попадает на '
               'первый узел с позицией ≥ hash (позиции — второй элемент пары [имя, позиция]), а если таких '
               'нет — на первый узел кольца; копии кладут на n последовательных узлов по кольцу. Напишите '
               'replicas_for(ring, hash_value, n): список имён.',
  'starter': 'def replicas_for(ring, hash_value, n):\n    pass\n',
  'tests': [{'args': [[['a', 10], ['b', 20], ['c', 30]], 15, 2], 'expected': ['b', 'c']},
            {'args': [[['a', 10], ['b', 20], ['c', 30]], 35, 2], 'expected': ['a', 'b']},
            {'args': [[['a', 10], ['b', 20], ['c', 30]], 30, 3], 'expected': ['c', 'a', 'b']},
            {'args': [[['a', 10]], 5, 3], 'expected': ['a']},
            {'args': [[], 5, 2], 'expected': []}],
  'hint': 'Найдите стартовый индекс, затем берите узлы по кругу через % len(ring).'},
 {'id': 'd6-log-gap',
  'mode': 'func',
  'func': 'missing_lsns',
  'title': 'Пропуски в журнале',
  'statement': 'Реплика получила записи журнала с номерами received (в произвольном порядке, возможны '
               'повторы). Напишите missing_lsns(received, upto): отсортированный список номеров от 1 до '
               'upto, которых нет и которые нужно запросить повторно.',
  'starter': 'def missing_lsns(received, upto):\n    pass\n',
  'tests': [{'args': [[1, 2, 4, 6], 6], 'expected': [3, 5]},
            {'args': [[], 3], 'expected': [1, 2, 3]},
            {'args': [[3, 1, 2, 2], 3], 'expected': []},
            {'args': [[1, 2, 3], 2], 'expected': []},
            {'args': [[5], 0], 'expected': []}],
  'hint': 'Множество полученных номеров и перебор 1..upto.'}]}
