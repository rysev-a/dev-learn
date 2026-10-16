"""Задачи книги «Базы данных»: глава 31."""

TASKS: dict[int, list[dict]] = {31: [{'id': 'd15-rbac-direct',
  'mode': 'sql',
  'title': 'Прямые привилегии роли',
  'statement': 'Выведите прямые привилегии роли app_rw: колонки object, priv; по объекту и привилегии.',
  'starter': '-- GRANT-ы роли\nSELECT\n',
  'setup': 'CREATE TABLE roles (name TEXT PRIMARY KEY);\n'
           'CREATE TABLE role_member (member TEXT NOT NULL, parent TEXT NOT NULL);\n'
           'CREATE TABLE grants (role TEXT NOT NULL, object TEXT NOT NULL, priv TEXT NOT NULL);\n'
           "INSERT INTO roles VALUES ('anna'),('boris'),('app_rw'),('report_ro'),('owner'),('dev');\n"
           'INSERT INTO role_member VALUES '
           "('anna','dev'),('dev','app_rw'),('boris','report_ro'),('app_rw','report_ro');\n"
           'INSERT INTO grants VALUES '
           "('report_ro','orders','SELECT'),('app_rw','orders','INSERT'),('app_rw','orders','UPDATE'),('app_rw','users','SELECT'),('owner','orders','DELETE'),('owner','orders','DROP'),('dev','users','UPDATE');\n",
  'expected': [['orders', 'INSERT'], ['orders', 'UPDATE'], ['users', 'SELECT']],
  'expected_cols': ['object', 'priv'],
  'hint': 'Выборка из grants по role.',
  'ordered': True},
 {'id': 'd15-rbac-effective',
  'mode': 'sql',
  'title': 'Эффективные привилегии с наследованием',
  'statement': 'Роль anna входит в dev, dev — в app_rw, app_rw — в report_ro. Выведите все привилегии anna с '
               'учётом наследования (без повторов): object, priv; по объекту и привилегии.',
  'starter': '-- рекурсивно по role_member\nWITH RECURSIVE\n',
  'setup': 'CREATE TABLE roles (name TEXT PRIMARY KEY);\n'
           'CREATE TABLE role_member (member TEXT NOT NULL, parent TEXT NOT NULL);\n'
           'CREATE TABLE grants (role TEXT NOT NULL, object TEXT NOT NULL, priv TEXT NOT NULL);\n'
           "INSERT INTO roles VALUES ('anna'),('boris'),('app_rw'),('report_ro'),('owner'),('dev');\n"
           'INSERT INTO role_member VALUES '
           "('anna','dev'),('dev','app_rw'),('boris','report_ro'),('app_rw','report_ro');\n"
           'INSERT INTO grants VALUES '
           "('report_ro','orders','SELECT'),('app_rw','orders','INSERT'),('app_rw','orders','UPDATE'),('app_rw','users','SELECT'),('owner','orders','DELETE'),('owner','orders','DROP'),('dev','users','UPDATE');\n",
  'expected': [['orders', 'INSERT'],
               ['orders', 'SELECT'],
               ['orders', 'UPDATE'],
               ['users', 'SELECT'],
               ['users', 'UPDATE']],
  'expected_cols': ['object', 'priv'],
  'hint': 'Рекурсивно соберите роли: сама anna и все её предки, затем выберите привилегии для этих ролей.',
  'ordered': True},
 {'id': 'd15-who-can-delete',
  'mode': 'sql',
  'title': 'Кто может удалять',
  'statement': 'Выведите роли (name), которые с учётом наследования могут выполнять DELETE над orders; по '
               'имени. Подсказка: проверьте и самих владельцев привилегии, и тех, кто входит в такие роли.',
  'starter': '-- кто может DELETE на orders\nWITH RECURSIVE\n',
  'setup': 'CREATE TABLE roles (name TEXT PRIMARY KEY);\n'
           'CREATE TABLE role_member (member TEXT NOT NULL, parent TEXT NOT NULL);\n'
           'CREATE TABLE grants (role TEXT NOT NULL, object TEXT NOT NULL, priv TEXT NOT NULL);\n'
           "INSERT INTO roles VALUES ('anna'),('boris'),('app_rw'),('report_ro'),('owner'),('dev');\n"
           'INSERT INTO role_member VALUES '
           "('anna','dev'),('dev','app_rw'),('boris','report_ro'),('app_rw','report_ro');\n"
           'INSERT INTO grants VALUES '
           "('report_ro','orders','SELECT'),('app_rw','orders','INSERT'),('app_rw','orders','UPDATE'),('app_rw','users','SELECT'),('owner','orders','DELETE'),('owner','orders','DROP'),('dev','users','UPDATE');\n",
  'expected': [['owner']],
  'expected_cols': ['name'],
  'hint': 'Спускайтесь вниз по наследованию: члены ролей-держателей тоже получают право.',
  'ordered': True},
 {'id': 'd15-excessive-ddl',
  'mode': 'sql',
  'title': 'Лишние права',
  'statement': 'Выведите роли, у которых есть привилегия DROP на любой объект, хотя они не owner: колонка '
               'role; по имени. Включайте и унаследованные права через членство.',
  'starter': '-- роли с DROP, кроме owner\nWITH RECURSIVE\n',
  'setup': 'CREATE TABLE roles (name TEXT PRIMARY KEY);\n'
           'CREATE TABLE role_member (member TEXT NOT NULL, parent TEXT NOT NULL);\n'
           'CREATE TABLE grants (role TEXT NOT NULL, object TEXT NOT NULL, priv TEXT NOT NULL);\n'
           "INSERT INTO roles VALUES ('anna'),('boris'),('app_rw'),('report_ro'),('owner'),('dev');\n"
           'INSERT INTO role_member VALUES '
           "('anna','dev'),('dev','app_rw'),('boris','report_ro'),('app_rw','report_ro');\n"
           'INSERT INTO grants VALUES '
           "('report_ro','orders','SELECT'),('app_rw','orders','INSERT'),('app_rw','orders','UPDATE'),('app_rw','users','SELECT'),('owner','orders','DELETE'),('owner','orders','DROP'),('dev','users','UPDATE');\n"
           "INSERT INTO grants VALUES ('app_rw','users','DROP');\n",
  'expected': [['anna'], ['app_rw'], ['dev']],
  'expected_cols': ['role'],
  'hint': 'Рекурсивно соберите роли с DROP и тех, кто в них входит; owner исключите.',
  'ordered': True},
 {'id': 'd15-grant-sim',
  'mode': 'sql',
  'title': 'GRANT как INSERT',
  'statement': 'Моделью GRANT служит вставка в grants. Выдайте роли report_ro право SELECT на users и '
               'отберите у app_rw право UPDATE на orders (DELETE из grants). Итог проверяется по таблице '
               'grants.',
  'starter': '-- GRANT / REVOKE\nINSERT INTO grants\n',
  'setup': 'CREATE TABLE roles (name TEXT PRIMARY KEY);\n'
           'CREATE TABLE role_member (member TEXT NOT NULL, parent TEXT NOT NULL);\n'
           'CREATE TABLE grants (role TEXT NOT NULL, object TEXT NOT NULL, priv TEXT NOT NULL);\n'
           "INSERT INTO roles VALUES ('anna'),('boris'),('app_rw'),('report_ro'),('owner'),('dev');\n"
           'INSERT INTO role_member VALUES '
           "('anna','dev'),('dev','app_rw'),('boris','report_ro'),('app_rw','report_ro');\n"
           'INSERT INTO grants VALUES '
           "('report_ro','orders','SELECT'),('app_rw','orders','INSERT'),('app_rw','orders','UPDATE'),('app_rw','users','SELECT'),('owner','orders','DELETE'),('owner','orders','DROP'),('dev','users','UPDATE');\n",
  'expected': [['app_rw', 'orders', 'INSERT'],
               ['app_rw', 'users', 'SELECT'],
               ['dev', 'users', 'UPDATE'],
               ['owner', 'orders', 'DELETE'],
               ['owner', 'orders', 'DROP'],
               ['report_ro', 'orders', 'SELECT'],
               ['report_ro', 'users', 'SELECT']],
  'expected_cols': ['role', 'object', 'priv'],
  'hint': 'INSERT одной строки и DELETE по трём условиям.',
  'ordered': True,
  'check': 'SELECT role, object, priv FROM grants ORDER BY role, object, priv'},
 {'id': 'd15-view-rls',
  'mode': 'sql',
  'title': 'Защита строк через представление',
  'statement': "Создайте представление people_a, которое показывает только людей арендатора 'A' (все "
               'столбцы). Итог проверяется выборкой из представления по id.',
  'starter': '-- RLS через view\nCREATE VIEW people_a AS\n',
  'setup': 'CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, phone '
           'TEXT, city TEXT NOT NULL, tenant TEXT NOT NULL);\n'
           "INSERT INTO people VALUES (1,'Анна','anna@mail.ru','+7 900 "
           "123-45-67','Москва','A'),(2,'Борис','boris@corp.com','+7 911 "
           "222-33-44','Казань','A'),(3,'Вера','vera@mail.ru',NULL,'Москва','B'),(4,'Глеб','gleb@gmail.com','+7 "
           "922 555-66-77','Тверь','B'),(5,'Дарья','dasha@mail.ru','+7 933 000-11-22','Москва','A');\n",
  'expected': [[1, 'Анна', 'A'], [2, 'Борис', 'A'], [5, 'Дарья', 'A']],
  'expected_cols': ['id', 'name', 'tenant'],
  'hint': "CREATE VIEW … AS SELECT * FROM people WHERE tenant = 'A'.",
  'ordered': True,
  'check': 'SELECT id, name, tenant FROM people_a ORDER BY id'},
 {'id': 'd15-view-columns',
  'mode': 'sql',
  'title': 'Только безопасные столбцы',
  'statement': 'Создайте представление people_public(id, name, city) — без почты и телефона. Итог '
               'проверяется выборкой, а также списком столбцов представления.',
  'starter': '-- безопасное представление\nCREATE VIEW people_public AS\n',
  'setup': 'CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, phone '
           'TEXT, city TEXT NOT NULL, tenant TEXT NOT NULL);\n'
           "INSERT INTO people VALUES (1,'Анна','anna@mail.ru','+7 900 "
           "123-45-67','Москва','A'),(2,'Борис','boris@corp.com','+7 911 "
           "222-33-44','Казань','A'),(3,'Вера','vera@mail.ru',NULL,'Москва','B'),(4,'Глеб','gleb@gmail.com','+7 "
           "922 555-66-77','Тверь','B'),(5,'Дарья','dasha@mail.ru','+7 933 000-11-22','Москва','A');\n",
  'expected': [[1, 'Анна', 'Москва'],
               [2, 'Борис', 'Казань'],
               [3, 'Вера', 'Москва'],
               [4, 'Глеб', 'Тверь'],
               [5, 'Дарья', 'Москва']],
  'expected_cols': ['id', 'name', 'city'],
  'hint': 'Перечислите только допустимые столбцы.',
  'ordered': True,
  'check': 'SELECT id, name, city FROM people_public ORDER BY id'},
 {'id': 'd15-mask-email',
  'mode': 'sql',
  'title': 'Маскирование почты',
  'statement': "Выведите маскированную почту: первая буква + '***' + всё начиная с символа '@'. Колонки id, "
               'masked; по id. Пример: anna@mail.ru → a***@mail.ru.',
  'starter': '-- маскирование\nSELECT\n',
  'setup': 'CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, phone '
           'TEXT, city TEXT NOT NULL, tenant TEXT NOT NULL);\n'
           "INSERT INTO people VALUES (1,'Анна','anna@mail.ru','+7 900 "
           "123-45-67','Москва','A'),(2,'Борис','boris@corp.com','+7 911 "
           "222-33-44','Казань','A'),(3,'Вера','vera@mail.ru',NULL,'Москва','B'),(4,'Глеб','gleb@gmail.com','+7 "
           "922 555-66-77','Тверь','B'),(5,'Дарья','dasha@mail.ru','+7 933 000-11-22','Москва','A');\n",
  'expected': [[1, 'a***@mail.ru'],
               [2, 'b***@corp.com'],
               [3, 'v***@mail.ru'],
               [4, 'g***@gmail.com'],
               [5, 'd***@mail.ru']],
  'expected_cols': ['id', 'masked'],
  'hint': "substr(email, 1, 1) и substr(email, instr(email, '@')).",
  'ordered': True},
 {'id': 'd15-mask-phone',
  'mode': 'sql',
  'title': 'Маскирование телефона',
  'statement': "Выведите последние 4 символа телефона, остальное заменив звёздочками одной группой: '***' || "
               'последние 4. Для NULL — NULL. Колонки id, masked; по id.',
  'starter': '-- маскирование телефона\nSELECT\n',
  'setup': 'CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, phone '
           'TEXT, city TEXT NOT NULL, tenant TEXT NOT NULL);\n'
           "INSERT INTO people VALUES (1,'Анна','anna@mail.ru','+7 900 "
           "123-45-67','Москва','A'),(2,'Борис','boris@corp.com','+7 911 "
           "222-33-44','Казань','A'),(3,'Вера','vera@mail.ru',NULL,'Москва','B'),(4,'Глеб','gleb@gmail.com','+7 "
           "922 555-66-77','Тверь','B'),(5,'Дарья','dasha@mail.ru','+7 933 000-11-22','Москва','A');\n",
  'expected': [[1, '***5-67'], [2, '***3-44'], [3, None], [4, '***6-77'], [5, '***1-22']],
  'expected_cols': ['id', 'masked'],
  'hint': 'substr(phone, -4) берёт последние 4 символа; CASE для NULL.',
  'ordered': True},
 {'id': 'd15-pseudonymize',
  'mode': 'sql',
  'title': 'Обезличивание для тестов',
  'statement': "Обезличьте таблицу: name = 'User' || id, email = 'user' || id || '@example.com', phone = "
               'NULL. Итог проверяется по таблице.',
  'starter': '-- UPDATE для тестовой среды\nUPDATE people\n',
  'setup': 'CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, phone '
           'TEXT, city TEXT NOT NULL, tenant TEXT NOT NULL);\n'
           "INSERT INTO people VALUES (1,'Анна','anna@mail.ru','+7 900 "
           "123-45-67','Москва','A'),(2,'Борис','boris@corp.com','+7 911 "
           "222-33-44','Казань','A'),(3,'Вера','vera@mail.ru',NULL,'Москва','B'),(4,'Глеб','gleb@gmail.com','+7 "
           "922 555-66-77','Тверь','B'),(5,'Дарья','dasha@mail.ru','+7 933 000-11-22','Москва','A');\n",
  'expected': [[1, 'User1', 'user1@example.com', None, 'Москва', 'A'],
               [2, 'User2', 'user2@example.com', None, 'Казань', 'A'],
               [3, 'User3', 'user3@example.com', None, 'Москва', 'B'],
               [4, 'User4', 'user4@example.com', None, 'Тверь', 'B'],
               [5, 'User5', 'user5@example.com', None, 'Москва', 'A']],
  'expected_cols': ['id', 'name', 'email', 'phone', 'city', 'tenant'],
  'hint': 'Один UPDATE с тремя присваиваниями.',
  'ordered': True,
  'check': 'SELECT id, name, email, phone, city, tenant FROM people ORDER BY id'},
 {'id': 'd15-k-anonymity',
  'mode': 'sql',
  'title': 'k-анонимность',
  'statement': 'Группы по городу с числом людей меньше 2 позволяют опознать человека. Выведите такие города '
               'и число людей: колонки city, n; по городу.',
  'starter': '-- мелкие группы\nSELECT\n',
  'setup': 'CREATE TABLE people (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL, phone '
           'TEXT, city TEXT NOT NULL, tenant TEXT NOT NULL);\n'
           "INSERT INTO people VALUES (1,'Анна','anna@mail.ru','+7 900 "
           "123-45-67','Москва','A'),(2,'Борис','boris@corp.com','+7 911 "
           "222-33-44','Казань','A'),(3,'Вера','vera@mail.ru',NULL,'Москва','B'),(4,'Глеб','gleb@gmail.com','+7 "
           "922 555-66-77','Тверь','B'),(5,'Дарья','dasha@mail.ru','+7 933 000-11-22','Москва','A');\n",
  'expected': [['Казань', 1], ['Тверь', 1]],
  'expected_cols': ['city', 'n'],
  'hint': 'GROUP BY city HAVING COUNT(*) < 2.',
  'ordered': True},
 {'id': 'd15-find-pii',
  'mode': 'sql',
  'title': 'Поиск персональных данных',
  'statement': "Найдите заметки, в которых встречается адрес почты (есть символ '@'): колонка id; по "
               'возрастанию.',
  'starter': '-- поиск e-mail\nSELECT\n',
  'setup': 'CREATE TABLE notes (id INTEGER PRIMARY KEY, body TEXT NOT NULL);\n'
           "INSERT INTO notes VALUES (1,'созвон в пятницу'),(2,'почта клиента: vera@mail.ru'),(3,'телефон +7 "
           "900 111-22-33'),(4,'без данных'),(5,'пишите на a.b@corp.com срочно');\n",
  'expected': [[2], [5]],
  'expected_cols': ['id'],
  'hint': "LIKE '%@%'.",
  'ordered': True},
 {'id': 'd15-delete-subject',
  'mode': 'sql',
  'title': 'Право на удаление',
  'statement': "По запросу субъекта удалите все данные пользователя с email 'a@x.ru' из всех таблиц одной "
               'командой DELETE (каскад сделает остальное). Итог проверяется по трём таблицам.',
  'starter': '-- удалить субъекта\nDELETE FROM\n',
  'setup': 'PRAGMA foreign_keys = ON;\n'
           'CREATE TABLE subjects (id INTEGER PRIMARY KEY, email TEXT UNIQUE);\n'
           'CREATE TABLE orders (id INTEGER PRIMARY KEY, subject_id INTEGER REFERENCES subjects(id) ON '
           'DELETE CASCADE, total INTEGER);\n'
           'CREATE TABLE messages (id INTEGER PRIMARY KEY, subject_id INTEGER REFERENCES subjects(id) ON '
           'DELETE CASCADE, body TEXT);\n'
           "INSERT INTO subjects VALUES (1,'a@x.ru'),(2,'b@x.ru');\n"
           'INSERT INTO orders VALUES (1,1,10),(2,2,20),(3,1,30);\n'
           "INSERT INTO messages VALUES (1,1,'hi'),(2,2,'yo');\n",
  'expected': [['m', 2], ['o', 2], ['s', 2]],
  'expected_cols': ['t', 'id'],
  'hint': 'Каскадные внешние ключи удалят зависимые строки сами.',
  'ordered': True,
  'check': "SELECT 's' AS t, id FROM subjects UNION ALL SELECT 'o', id FROM orders UNION ALL SELECT 'm', id "
           'FROM messages ORDER BY 1, 2'},
 {'id': 'd15-audit-trigger',
  'mode': 'sql',
  'title': 'Триггер аудита',
  'statement': 'Создайте триггер trg_audit AFTER UPDATE OF balance ON accounts: он записывает в audit строку '
               '(acc_id, old_balance, new_balance). Затем выполните UPDATE accounts SET balance = balance + '
               '25 WHERE id = 1. Итог проверяется по audit.',
  'starter': '-- аудит изменений\nCREATE TRIGGER trg_audit\n',
  'setup': 'CREATE TABLE accounts (id INTEGER PRIMARY KEY, owner TEXT, balance INTEGER NOT NULL);\n'
           'CREATE TABLE audit (id INTEGER PRIMARY KEY AUTOINCREMENT, acc_id INTEGER, old_balance INTEGER, '
           'new_balance INTEGER);\n'
           "INSERT INTO accounts VALUES (1,'Анна',100),(2,'Борис',50);\n",
  'expected': [[1, 100, 125]],
  'expected_cols': ['acc_id', 'old_balance', 'new_balance'],
  'hint': 'CREATE TRIGGER … AFTER UPDATE OF balance ON accounts BEGIN INSERT … VALUES (OLD.id, OLD.balance, '
          'NEW.balance); END;',
  'ordered': True,
  'check': 'SELECT acc_id, old_balance, new_balance FROM audit ORDER BY id'},
 {'id': 'd15-audit-who',
  'mode': 'sql',
  'title': 'Кто чаще всего менял',
  'statement': 'Выведите для каждого пользователя число действий DELETE: колонки who, deletes; по убыванию '
               'числа, затем по имени. Только тех, у кого они были.',
  'starter': '-- аудит удалений\nSELECT\n',
  'setup': 'CREATE TABLE audit (id INTEGER PRIMARY KEY, who TEXT, table_name TEXT, action TEXT);\n'
           'INSERT INTO audit VALUES '
           "(1,'anna','orders','UPDATE'),(2,'boris','users','DELETE'),(3,'anna','orders','DELETE'),(4,'anna','users','UPDATE'),(5,'boris','orders','UPDATE'),(6,'root','users','DELETE');\n",
  'expected': [['anna', 1], ['boris', 1], ['root', 1]],
  'expected_cols': ['who', 'deletes'],
  'hint': "WHERE action = 'DELETE' и GROUP BY who.",
  'ordered': True},
 {'id': 'd15-brute-force',
  'mode': 'sql',
  'title': 'Подбор паролей',
  'statement': 'Выведите IP-адреса, с которых было 3 и более неудачных входов (ok = 0): колонки ip, '
               'failures; по убыванию числа, затем по адресу.',
  'starter': '-- brute force\nSELECT\n',
  'setup': 'CREATE TABLE logins (id INTEGER PRIMARY KEY, ts INTEGER NOT NULL, user TEXT NOT NULL, ip TEXT '
           'NOT NULL, ok INTEGER NOT NULL);\n'
           'INSERT INTO logins VALUES '
           "(1,100,'anna','1.1.1.1',1),(2,101,'root','9.9.9.9',0),(3,102,'root','9.9.9.9',0),(4,103,'admin','9.9.9.9',0),(5,104,'root','9.9.9.9',0),(6,105,'boris','2.2.2.2',0),(7,106,'boris','2.2.2.2',1),(8,200,'root','8.8.8.8',0),(9,201,'root','8.8.8.8',0);\n",
  'expected': [['9.9.9.9', 4]],
  'expected_cols': ['ip', 'failures'],
  'hint': 'WHERE ok = 0, GROUP BY ip, HAVING COUNT(*) >= 3.',
  'ordered': True},
 {'id': 'd15-lockout',
  'mode': 'sql',
  'title': 'Блокировка после неудач',
  'statement': 'Выведите пользователей, у которых по журналу не меньше двух неудачных входов и ни одного '
               'успешного: колонка user; по имени.',
  'starter': '-- кандидаты на блокировку\nSELECT\n',
  'setup': 'CREATE TABLE logins (id INTEGER PRIMARY KEY, ts INTEGER NOT NULL, user TEXT NOT NULL, ip TEXT '
           'NOT NULL, ok INTEGER NOT NULL);\n'
           'INSERT INTO logins VALUES '
           "(1,100,'anna','1.1.1.1',1),(2,101,'root','9.9.9.9',0),(3,102,'root','9.9.9.9',0),(4,103,'admin','9.9.9.9',0),(5,104,'root','9.9.9.9',0),(6,105,'boris','2.2.2.2',0),(7,106,'boris','2.2.2.2',1),(8,200,'root','8.8.8.8',0),(9,201,'root','8.8.8.8',0);\n",
  'expected': [['root']],
  'expected_cols': ['user'],
  'hint': 'GROUP BY user HAVING SUM(ok = 0) >= 2 AND SUM(ok = 1) = 0.',
  'ordered': True},
 {'id': 'd15-sqli-log',
  'mode': 'sql',
  'title': 'Подозрительные запросы в журнале',
  'statement': "Найдите записи, содержащие признаки инъекции: подстроки ' OR 1=1' или '; DROP' (регистр "
               'учитывать не нужно, достаточно LIKE). Колонка id; по возрастанию.',
  'starter': '-- поиск следов инъекций\nSELECT\n',
  'setup': 'CREATE TABLE qlog (id INTEGER PRIMARY KEY, q TEXT NOT NULL);\n'
           "INSERT INTO qlog VALUES (1,'SELECT * FROM u WHERE id = 5'),(2,'SELECT * FROM u WHERE name = "
           "''x'' OR 1=1 --'),(3,'SELECT 1'),(4,'SELECT * FROM u; DROP TABLE u'),(5,'SELECT * FROM o WHERE a "
           "= ''b''');\n",
  'expected': [[2], [4]],
  'expected_cols': ['id'],
  'hint': 'Два LIKE через OR.',
  'ordered': True},
 {'id': 'd15-hash-password',
  'mode': 'func',
  'func': 'hash_password',
  'title': 'Хеш пароля с солью',
  'statement': "Напишите hash_password(password, salt): результат hashlib.pbkdf2_hmac('sha256', "
               'password.encode(), salt.encode(), 1000).hex() — строка из шестнадцатеричных цифр. (Для сдачи '
               'точное значение важно: параметры заданы.)',
  'starter': 'import hashlib\n\ndef hash_password(password, salt):\n    pass\n',
  'tests': [{'args': ['qwerty', 'a91'],
             'expected': '71ecfbf1e10e7b25aaee6c22c141bce187e0c930449447f8cbdbf5dfe2173b4c'},
            {'args': ['qwerty', 'k02'],
             'expected': '3359f8615331361e63a0401905cb1e51952713c263cccf3f754fabb74431df68'},
            {'args': ['', 's'],
             'expected': '1d1ffa57cc2050dd643d375e9f497e5eb9af1e1ec69748d7220e566ff4e9f396'},
            {'args': ['пароль', 'соль'],
             'expected': '0746286eb900e3c447fee13b65c735667682e19125526e7931d14e92c775428b'}],
  'hint': "hashlib.pbkdf2_hmac('sha256', …, 1000).hex()."},
 {'id': 'd15-verify-password',
  'mode': 'func',
  'func': 'verify_password',
  'title': 'Проверка пароля',
  'statement': "Напишите verify_password(password, salt, stored): True, если hashlib.pbkdf2_hmac('sha256', "
               'password.encode(), salt.encode(), 1000).hex() совпадает с stored. Сравнивайте за постоянное '
               'время (hmac.compare_digest).',
  'starter': 'import hashlib\nimport hmac\n\ndef verify_password(password, salt, stored):\n    pass\n',
  'tests': [{'args': ['qwerty', 'a91', '71ecfbf1e10e7b25aaee6c22c141bce187e0c930449447f8cbdbf5dfe2173b4c'],
             'expected': True},
            {'args': ['qwerty', 'a91', '00'], 'expected': False},
            {'args': ['x', 'y', 'x'], 'expected': False}],
  'hint': 'hmac.compare_digest(h, stored).'},
 {'id': 'd15-password-policy',
  'mode': 'func',
  'func': 'password_violations',
  'title': 'Политика паролей',
  'statement': "Правила: длина не меньше 8 ('short'), есть цифра ('no-digit'), есть заглавная буква "
               "('no-upper'), нет подряд идущих трёх одинаковых символов ('repeat'). Напишите "
               'password_violations(pw): отсортированный список нарушенных правил.',
  'starter': 'def password_violations(pw):\n    pass\n',
  'tests': [{'args': ['abc'], 'expected': ['no-digit', 'no-upper', 'short']},
            {'args': ['Abcdefg1'], 'expected': []},
            {'args': ['aaaa1111'], 'expected': ['no-upper', 'repeat']},
            {'args': ['Strong#Pass9'], 'expected': []},
            {'args': [''], 'expected': ['no-digit', 'no-upper', 'short']}],
  'hint': 'Четыре независимые проверки; результат отсортируйте.'},
 {'id': 'd15-param-query',
  'mode': 'func',
  'func': 'build_query',
  'title': 'Параметризованный запрос',
  'statement': 'Таблицы разрешены только users и orders, столбцы фильтра — id, name, city, status. Напишите '
               "build_query(table, filters): пару [sql, params], где sql = 'SELECT * FROM <table> WHERE a = "
               "? AND b = ?' (условия в порядке ключей словаря filters; без фильтров — 'SELECT * FROM "
               "<table>'), params — значения в том же порядке. Если таблица или столбец не разрешены — "
               'вернуть None.',
  'starter': 'def build_query(table, filters):\n    pass\n',
  'tests': [{'args': ['users', {'city': 'Москва', 'id': 5}],
             'expected': ['SELECT * FROM users WHERE city = ? AND id = ?', ['Москва', 5]]},
            {'args': ['orders', {}], 'expected': ['SELECT * FROM orders', []]},
            {'args': ['secret', {}], 'expected': None},
            {'args': ['users', {'1=1; --': 1}], 'expected': None}],
  'hint': 'Белые списки для таблицы и столбцов; значения — только в params.'},
 {'id': 'd15-order-by',
  'mode': 'func',
  'func': 'safe_order_by',
  'title': 'Безопасная сортировка',
  'statement': 'Пользователь передаёт столбец и направление. Разрешены столбцы из allowed и направления '
               "'asc'/'desc' (без учёта регистра). Напишите safe_order_by(column, direction, allowed): "
               "строку 'ORDER BY col DIR' (направление заглавными) или 'ORDER BY id ASC', если ввод "
               'недопустим.',
  'starter': 'def safe_order_by(column, direction, allowed):\n    pass\n',
  'tests': [{'args': ['price', 'DESC', ['price', 'name']], 'expected': 'ORDER BY price DESC'},
            {'args': ['price; DROP', 'asc', ['price']], 'expected': 'ORDER BY id ASC'},
            {'args': ['name', 'sideways', ['name']], 'expected': 'ORDER BY id ASC'},
            {'args': ['name', 'Asc', ['name']], 'expected': 'ORDER BY name ASC'}],
  'hint': 'Оба параметра сверьте с белыми списками.'},
 {'id': 'd15-detect-sqli',
  'mode': 'func',
  'func': 'looks_like_injection',
  'title': 'Подозрительный ввод',
  'statement': 'Напишите looks_like_injection(s): True, если в нижнем регистре в строке встречается один из '
               'признаков: "\' or ", "--", ";", "union select", "/*". Иначе False. Это эвристика для '
               'журнала, а не защита.',
  'starter': 'def looks_like_injection(s):\n    pass\n',
  'tests': [{'args': ['Иван'], 'expected': False},
            {'args': ["x' OR 1=1 --"], 'expected': True},
            {'args': ['a; drop table t'], 'expected': True},
            {'args': ['1 UNION SELECT password'], 'expected': True},
            {'args': ["O'Brien"], 'expected': False}],
  'hint': 'Приведите к нижнему регистру и проверьте каждую подстроку.'},
 {'id': 'd15-effective-privs',
  'mode': 'func',
  'func': 'effective_privs',
  'title': 'Наследование ролей',
  'statement': 'Роли заданы словарём «роль → список ролей-родителей», привилегии — словарём «роль → список '
               'привилегий». Напишите effective_privs(role, parents, privs): отсортированный список '
               'привилегий роли с учётом наследования (циклы допустимы). Неизвестные роли — без привилегий.',
  'starter': 'def effective_privs(role, parents, privs):\n    pass\n',
  'tests': [{'args': ['a', {'a': ['b'], 'b': ['c']}, {'a': ['x'], 'b': ['y'], 'c': ['x', 'z']}],
             'expected': ['x', 'y', 'z']},
            {'args': ['q', {}, {}], 'expected': []},
            {'args': ['a', {'a': ['b'], 'b': ['a']}, {'a': ['r'], 'b': ['w']}], 'expected': ['r', 'w']}],
  'hint': 'Обход графа ролей с множеством посещённых.'},
 {'id': 'd15-rls-filter',
  'mode': 'func',
  'func': 'rls_filter',
  'title': 'Политика строк',
  'statement': "Строки — словари с ключом 'tenant'. Напишите rls_filter(rows, tenant, is_owner): если "
               'is_owner — все строки (владелец обходит политику), иначе только строки арендатора.',
  'starter': 'def rls_filter(rows, tenant, is_owner):\n    pass\n',
  'tests': [{'args': [[{'tenant': 'A', 'id': 1}, {'tenant': 'B', 'id': 2}], 'A', False],
             'expected': [{'tenant': 'A', 'id': 1}]},
            {'args': [[{'tenant': 'A', 'id': 1}, {'tenant': 'B', 'id': 2}], 'A', True],
             'expected': [{'tenant': 'A', 'id': 1}, {'tenant': 'B', 'id': 2}]},
            {'args': [[], 'A', False], 'expected': []}],
  'hint': 'Список с фильтром по tenant или без него для владельца.'},
 {'id': 'd15-mask-card',
  'mode': 'func',
  'func': 'mask_card',
  'title': 'Маскирование карты',
  'statement': "Напишите mask_card(number): оставить последние 4 цифры, остальные цифры заменить '•', "
               'пробелы и дефисы сохранить как есть. Если цифр меньше 4 — все цифры оставить.',
  'starter': 'def mask_card(number):\n    pass\n',
  'tests': [{'args': ['4242 4242 4242 4242'], 'expected': '•••• •••• •••• 4242'},
            {'args': ['1234-5678'], 'expected': '••••-5678'},
            {'args': ['12'], 'expected': '12'},
            {'args': [''], 'expected': ''}],
  'hint': 'Найдите позиции цифр; последние 4 оставьте.'},
 {'id': 'd15-k-anon-py',
  'mode': 'func',
  'func': 'small_groups',
  'title': 'Мелкие группы',
  'statement': 'Записи — списки значений квазиидентификаторов (например, [город, возраст]). Напишите '
               'small_groups(rows, k): отсортированный список групп (как списки), которые встречаются меньше '
               'k раз.',
  'starter': 'def small_groups(rows, k):\n    pass\n',
  'tests': [{'args': [[['Москва', 30], ['Москва', 30], ['Тверь', 25]], 2], 'expected': [['Тверь', 25]]},
            {'args': [[], 2], 'expected': []},
            {'args': [[['a'], ['b'], ['a']], 3], 'expected': [['a'], ['b']]}],
  'hint': 'Подсчёт кортежей и отбор групп с n < k.'},
 {'id': 'd15-audit-diff',
  'mode': 'func',
  'func': 'audit_diff',
  'title': 'Что изменилось',
  'statement': 'Строки до и после — словари. Напишите audit_diff(before, after): отсортированный по полю '
               'список записей [поле, было, стало] для полей, значения которых различаются (поле есть только '
               'в одном из словарей — отсутствующее значение None).',
  'starter': 'def audit_diff(before, after):\n    pass\n',
  'tests': [{'args': [{'a': 1, 'b': 2}, {'a': 1, 'b': 3, 'c': 4}], 'expected': [['b', 2, 3], ['c', None, 4]]},
            {'args': [{}, {}], 'expected': []},
            {'args': [{'x': None}, {'x': 5}], 'expected': [['x', None, 5]]}],
  'hint': 'Объедините ключи, сравните значения через get.'},
 {'id': 'd15-rate-limit',
  'mode': 'func',
  'func': 'allowed_attempts',
  'title': 'Ограничение частоты',
  'statement': 'Попытки входа — возрастающий список секунд. Лимит: не более limit попыток за любые window '
               'секунд (окно [t − window + 1, t]). Напишите allowed_attempts(times, limit, window): список '
               'True/False для каждой попытки — разрешена ли она (отклонённые попытки тоже считаются в окне '
               'как попытки).',
  'starter': 'def allowed_attempts(times, limit, window):\n    pass\n',
  'tests': [{'args': [[1, 2, 3, 4, 5, 70], 3, 10], 'expected': [True, True, True, False, False, True]},
            {'args': [[], 3, 10], 'expected': []},
            {'args': [[1, 1, 1, 1], 2, 5], 'expected': [True, True, False, False]}],
  'hint': 'Для каждой попытки сосчитайте попытки в окне, включая её саму.'},
 {'id': 'd15-hba',
  'mode': 'func',
  'func': 'match_rule',
  'title': 'Правила доступа',
  'statement': "Правила — список [тип, база, роль, сеть, решение]; 'all' означает любое значение, сеть — "
               'CIDR. Побеждает первое подходящее правило. Напишите match_rule(rules, db, role, ip, ssl): '
               "решение ('allow' или 'reject') первого подходящего; тип 'hostssl' подходит только при "
               "ssl=True, 'host' — при любом; если ничего не подошло — 'reject'. Используйте ipaddress.",
  'starter': 'import ipaddress\n\ndef match_rule(rules, db, role, ip, ssl):\n    pass\n',
  'tests': [{'args': [[['hostssl', 'app', 'app_rw', '10.0.1.0/24', 'allow'],
                       ['host', 'all', 'all', '0.0.0.0/0', 'reject']],
                      'app',
                      'app_rw',
                      '10.0.1.5',
                      True],
             'expected': 'allow'},
            {'args': [[['hostssl', 'app', 'app_rw', '10.0.1.0/24', 'allow'],
                       ['host', 'all', 'all', '0.0.0.0/0', 'reject']],
                      'app',
                      'app_rw',
                      '10.0.1.5',
                      False],
             'expected': 'reject'},
            {'args': [[], 'x', 'y', '1.1.1.1', True], 'expected': 'reject'},
            {'args': [[['host', 'all', 'all', '10.0.0.0/8', 'allow']], 'any', 'any', '11.0.0.1', False],
             'expected': 'reject'}],
  'hint': 'Идите по правилам по порядку, пропуская неподходящие.'}]}
