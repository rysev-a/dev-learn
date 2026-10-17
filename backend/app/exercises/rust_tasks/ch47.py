"""Задачи книги «Изучаем Rust»: глава 47 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {47: [{'id': 'r47-select-one',
  'mode': 'rust',
  'title': 'Первое подключение',
  'statement': 'Подключитесь к базе (функция pool() уже есть) и напечатайте: результат запроса '
               'SELECT 20 + 22 через query_scalar::<_, i32>, а затем «версия сервера >= 14: '
               'true/false» (SHOW server_version_num возвращает строку с числом).\n'
               '\n'
               'Ожидаемый вывод:\n'
               '42\n'
               'версия сервера >= 14: true',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'sqlx::query_scalar::<_, i32>("SELECT 20 + 22").fetch_one(&pool).await.unwrap().',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['42', 'версия сервера >= 14: true'],
  'postgres': True},
 {'id': 'r47-users-table',
  'mode': 'rust',
  'title': 'Таблица и FromRow',
  'statement': 'Создайте таблицу users (id BIGSERIAL PRIMARY KEY, name TEXT NOT NULL, bio TEXT), '
               'вставьте «аня» (без bio) и «боря» (bio «привет»), прочитайте обе строки структурой '
               'User (derive FromRow) в порядке id и напечатайте их Debug.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'User { id: 1, name: "аня", bio: None }\n'
               'User { id: 2, name: "боря", bio: Some("привет") }',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[derive(FromRow, Debug)]\n'
             'struct User {\n'
             '    id: i64,\n'
             '    name: String,\n'
             '    bio: Option<String>,\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'query("CREATE TABLE ...").execute(&pool); query_as::<_, User>("SELECT * FROM users '
          'ORDER BY id").fetch_all.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['User { id: 1, name: "аня", bio: None }',
               'User { id: 2, name: "боря", bio: Some("привет") }'],
  'postgres': True},
 {'id': 'r47-bind-safe',
  'mode': 'rust',
  'title': 'Параметры вместо подстановки',
  'statement': "Вставьте в таблицу notes(text TEXT) строку «x'); DROP TABLE notes;--» через bind, "
               'затем прочитайте её обратно и напечатайте, а также число строк в таблице (таблица '
               'должна уцелеть).\n'
               '\n'
               'Ожидаемый вывод:\n'
               "x'); DROP TABLE notes;--\n"
               'строк: 1',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'bind передаёт значение отдельно от текста запроса — оно не исполняется как SQL.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ["x'); DROP TABLE notes;--", 'строк: 1'],
  'postgres': True},
 {'id': 'r47-optional',
  'mode': 'rust',
  'title': 'Нет строки: Option и ошибка',
  'statement': 'В таблице rooms(id BIGSERIAL, name TEXT) одна строка «общая». Найдите комнату с id '
               '= 1 (fetch_optional → Some), с id = 99 (None) и покажите, что fetch_one для id = '
               '99 возвращает ошибку sqlx::Error::RowNotFound (напечатайте true).\n'
               '\n'
               'Ожидаемый вывод:\n'
               '1: Some("общая")\n'
               '99: None\n'
               'true',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'fetch_optional даёт Option; matches!(err, sqlx::Error::RowNotFound).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['1: Some("общая")', '99: None', 'true'],
  'postgres': True},
 {'id': 'r47-returning',
  'mode': 'rust',
  'title': 'INSERT … RETURNING',
  'statement': 'Создайте rooms(id BIGSERIAL PRIMARY KEY, name TEXT UNIQUE NOT NULL) и функцию '
               'create_room(&PgPool, &str) -> i64, которая вставляет комнату и возвращает её id '
               'одним запросом (RETURNING id). Создайте три комнаты и напечатайте их id.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '1\n'
               '2\n'
               '3',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             'async fn create_room(pool: &PgPool, name: &str) -> i64 {\n'
             '    todo!()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE rooms (id BIGSERIAL PRIMARY KEY, name TEXT UNIQUE NOT '
             'NULL)").execute(&pool).await.unwrap();\n'
             '    for n in ["общая", "dev", "random"] {\n'
             '        println!("{}", create_room(&pool, n).await);\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'query_scalar("INSERT ... RETURNING id").bind(name).fetch_one(pool).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['1', '2', '3'],
  'postgres': True},
 {'id': 'r47-on-conflict-nothing',
  'mode': 'rust',
  'title': 'Идемпотентное создание',
  'statement': 'Таблица rooms(name TEXT PRIMARY KEY). Функция ensure_room(&PgPool, &str) -> bool '
               'вставляет комнату с ON CONFLICT DO NOTHING и возвращает true, если комната создана '
               'сейчас (rows_affected() == 1). Вызовите её для «a», «b», «a», «b», «c».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'a: true\n'
               'b: true\n'
               'a: false\n'
               'b: false\n'
               'c: true',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             'async fn ensure_room(pool: &PgPool, name: &str) -> bool {\n'
             '    todo!()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE rooms (name TEXT PRIMARY '
             'KEY)").execute(&pool).await.unwrap();\n'
             '    for n in ["a", "b", "a", "b", "c"] {\n'
             '        println!("{n}: {}", ensure_room(&pool, n).await);\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'INSERT ... ON CONFLICT (name) DO NOTHING; res.rows_affected() == 1.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['a: true', 'b: true', 'a: false', 'b: false', 'c: true'],
  'postgres': True},
 {'id': 'r47-on-conflict-update',
  'mode': 'rust',
  'title': 'Счётчик одним запросом',
  'statement': 'Таблица hits(path TEXT PRIMARY KEY, n BIGINT NOT NULL). Функция hit(&PgPool, &str) '
               '-> i64 увеличивает счётчик пути одним запросом (INSERT … ON CONFLICT DO UPDATE … '
               'RETURNING n) и возвращает новое значение. Вызовите hit для /a, /a, /b, /a, /b.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '/a: 1\n'
               '/a: 2\n'
               '/b: 1\n'
               '/a: 3\n'
               '/b: 2',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             'async fn hit(pool: &PgPool, path: &str) -> i64 {\n'
             '    todo!()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE hits (path TEXT PRIMARY KEY, n BIGINT NOT '
             'NULL)").execute(&pool).await.unwrap();\n'
             '    for p in ["/a", "/a", "/b", "/a", "/b"] {\n'
             '        println!("{p}: {}", hit(&pool, p).await);\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'ON CONFLICT (path) DO UPDATE SET n = hits.n + 1 RETURNING n.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['/a: 1', '/a: 2', '/b: 1', '/a: 3', '/b: 2'],
  'postgres': True},
 {'id': 'r47-null',
  'mode': 'rust',
  'title': 'NULL и Option',
  'statement': 'Таблица profiles(user_name TEXT, city TEXT) со строками («аня», NULL) и («боря», '
               '«Тверь»). Прочитайте обе строки кортежем (String, Option<String>) через query_as и '
               'напечатайте «аня: ?» / «боря: Тверь» (неизвестный город — «?»).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'аня: ?\n'
               'боря: Тверь',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'query_as::<_, (String, Option<String>)>; unwrap_or("?".into()).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['аня: ?', 'боря: Тверь'],
  'postgres': True},
 {'id': 'r47-timestamptz',
  'mode': 'rust',
  'title': 'Время создания',
  'statement': 'Таблица events(id BIGSERIAL, at TIMESTAMPTZ NOT NULL DEFAULT now()). Вставьте два '
               'события с паузой 20 мс между ними, прочитайте at как chrono::DateTime<Utc> и '
               'напечатайте: «второе позже первого: true», «разница не меньше 20 мс: true», «время '
               'не из будущего: true» (сравнение с Utc::now()).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'второе позже первого: true\n'
               'разница не меньше 20 мс: true\n'
               'время не из будущего: true',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'Столбец TIMESTAMPTZ ↔ chrono::DateTime<chrono::Utc>.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['второе позже первого: true',
               'разница не меньше 20 мс: true',
               'время не из будущего: true'],
  'postgres': True},
 {'id': 'r47-uuid',
  'mode': 'rust',
  'title': 'UUID как ключ',
  'statement': 'Таблица tokens(id UUID PRIMARY KEY DEFAULT gen_random_uuid(), owner TEXT). '
               'Вставьте две строки с RETURNING id (тип uuid::Uuid). Напечатайте: идентификаторы '
               'различны, версия каждого равна 4 (get_version_num()), и выбор по id возвращает '
               'владельца.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'различны: true\n'
               'версия 4: true\n'
               'боря',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'query_scalar::<_, uuid::Uuid>("INSERT ... RETURNING id").',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['различны: true', 'версия 4: true', 'боря'],
  'postgres': True},
 {'id': 'r47-jsonb',
  'mode': 'rust',
  'title': 'JSONB-столбец',
  'statement': 'Таблица settings(user_name TEXT, prefs JSONB). Вставьте prefs как '
               'sqlx::types::Json<Prefs> (структура Prefs { theme: String, sound: bool } с '
               'Serialize/Deserialize), затем прочитайте обратно Json<Prefs> и достаньте theme '
               'прямо в SQL оператором ->> (query_scalar). Напечатайте оба результата.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Prefs { theme: "тёмная", sound: true }\n'
               'тёмная',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             'use serde::{Deserialize, Serialize};\n'
             '\n'
             '#[derive(Serialize, Deserialize, Debug)]\n'
             'struct Prefs {\n'
             '    theme: String,\n'
             '    sound: bool,\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': "sqlx::types::Json(prefs) в bind; Json<Prefs> при чтении; SELECT prefs->>'theme'.",
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Prefs { theme: "тёмная", sound: true }', 'тёмная'],
  'postgres': True},
 {'id': 'r47-tx-commit',
  'mode': 'rust',
  'title': 'Транзакция: комната и участник',
  'statement': 'Таблицы rooms(id BIGSERIAL PK, name TEXT) и members(room_id BIGINT, user_name '
               'TEXT). Функция create_with_owner(&PgPool, room, owner) -> i64 в одной транзакции '
               'вставляет комнату (RETURNING id) и участника-владельца, затем фиксирует. Создайте '
               'две комнаты и напечатайте число строк в обеих таблицах.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'rooms: 2\n'
               'members: 2',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             'async fn create_with_owner(pool: &PgPool, room: &str, owner: &str) -> i64 {\n'
             '    todo!()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE rooms (id BIGSERIAL PRIMARY KEY, name '
             'TEXT)").execute(&pool).await.unwrap();\n'
             '    sqlx::query("CREATE TABLE members (room_id BIGINT, user_name '
             'TEXT)").execute(&pool).await.unwrap();\n'
             '    create_with_owner(&pool, "общая", "аня").await;\n'
             '    create_with_owner(&pool, "dev", "боря").await;\n'
             '    let r: i64 = sqlx::query_scalar("SELECT COUNT(*) FROM '
             'rooms").fetch_one(&pool).await.unwrap();\n'
             '    let m: i64 = sqlx::query_scalar("SELECT COUNT(*) FROM '
             'members").fetch_one(&pool).await.unwrap();\n'
             '    println!("rooms: {r}\\nmembers: {m}");\n'
             '}\n',
  'driver': '',
  'hint': 'let mut tx = pool.begin().await?; ... .execute(&mut *tx) ... tx.commit().',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['rooms: 2', 'members: 2'],
  'postgres': True},
 {'id': 'r47-tx-drop',
  'mode': 'rust',
  'title': 'Откат при уничтожении',
  'statement': 'Таблица log(msg TEXT). Откройте транзакцию, вставьте строку «в транзакции», '
               'напечатайте число строк внутри транзакции, затем уничтожьте транзакцию без commit '
               '(drop) и напечатайте число строк снаружи (должно быть 0). Затем повторите с commit '
               '— число снаружи 1.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'внутри: 1\n'
               'снаружи после drop: 0\n'
               'снаружи после commit: 1',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'tx.commit() фиксирует; drop(tx) откатывает.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['внутри: 1', 'снаружи после drop: 0', 'снаружи после commit: 1'],
  'postgres': True},
 {'id': 'r47-transfer',
  'mode': 'rust',
  'title': 'Перевод между счетами',
  'statement': 'Таблица accounts(name TEXT PK, balance BIGINT CHECK (balance >= 0)) со счетами '
               '«аня» 100 и «боря» 50. Функция transfer(&PgPool, from, to, amount) -> Result<(), '
               'sqlx::Error> в транзакции списывает и зачисляет. Переведите 30 от ани к боре '
               '(успех), затем 500 от ани к боре (ограничение CHECK нарушено — вся транзакция '
               'откатывается). Напечатайте результаты и итоговые балансы.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'true\n'
               'false\n'
               '[("аня", 70), ("боря", 80)]',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             'async fn transfer(pool: &PgPool, from: &str, to: &str, amount: i64) -> Result<(), '
             'sqlx::Error> {\n'
             '    todo!()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE accounts (name TEXT PRIMARY KEY, balance BIGINT CHECK '
             '(balance >= 0))").execute(&pool).await.unwrap();\n'
             '    sqlx::query("INSERT INTO accounts VALUES (\'аня\', 100), (\'боря\', '
             '50)").execute(&pool).await.unwrap();\n'
             '    println!("{:?}", transfer(&pool, "аня", "боря", 30).await.is_ok());\n'
             '    println!("{:?}", transfer(&pool, "аня", "боря", 500).await.is_ok());\n'
             '    let rows: Vec<(String, i64)> = sqlx::query_as("SELECT name, balance FROM '
             'accounts ORDER BY name").fetch_all(&pool).await.unwrap();\n'
             '    println!("{rows:?}");\n'
             '}\n',
  'driver': '',
  'hint': 'Два UPDATE в одной транзакции; Err на первом — ранний возврат через ? и откат при drop.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['true', 'false', '[("аня", 70), ("боря", 80)]'],
  'postgres': True},
 {'id': 'r47-unique-violation',
  'mode': 'rust',
  'title': 'Нарушение уникальности',
  'statement': 'Таблица users(name TEXT UNIQUE). Функция add_user(&PgPool, &str) -> Result<(), '
               'String>: успех — Ok, нарушение уникальности (SQLSTATE 23505) — Err("имя занято"), '
               'любая другая ошибка — Err(текст ошибки). Добавьте «аня», «боря», «аня» и '
               'напечатайте результаты.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'аня: Ok(())\n'
               'боря: Ok(())\n'
               'аня: Err("имя занято")',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             'async fn add_user(pool: &PgPool, name: &str) -> Result<(), String> {\n'
             '    todo!()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE users (name TEXT '
             'UNIQUE)").execute(&pool).await.unwrap();\n'
             '    for n in ["аня", "боря", "аня"] {\n'
             '        println!("{n}: {:?}", add_user(&pool, n).await);\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'e.as_database_error().and_then(|d| d.code()) — сравните с "23505" (или '
          'd.is_unique_violation()).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['аня: Ok(())', 'боря: Ok(())', 'аня: Err("имя занято")'],
  'postgres': True},
 {'id': 'r47-fk-violation',
  'mode': 'rust',
  'title': 'Нарушение внешнего ключа',
  'statement': 'Таблицы rooms(id BIGSERIAL PK, name TEXT) и messages(id BIGSERIAL PK, room_id '
               'BIGINT REFERENCES rooms(id), text TEXT). Функция post(&PgPool, room_id, text) -> '
               "&'static str возвращает «ок», если вставка прошла, «нет комнаты» при нарушении "
               'внешнего ключа (SQLSTATE 23503) и «сбой» иначе. Опубликуйте в комнату 1 (создана), '
               'и в комнату 2 (нет).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'ок\n'
               'нет комнаты',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             "async fn post(pool: &PgPool, room_id: i64, text: &str) -> &'static str {\n"
             '    todo!()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE rooms (id BIGSERIAL PRIMARY KEY, name '
             'TEXT)").execute(&pool).await.unwrap();\n'
             '    sqlx::query("CREATE TABLE messages (id BIGSERIAL PRIMARY KEY, room_id BIGINT '
             'REFERENCES rooms(id), text TEXT)").execute(&pool).await.unwrap();\n'
             '    sqlx::query("INSERT INTO rooms (name) VALUES '
             '(\'общая\')").execute(&pool).await.unwrap();\n'
             '    println!("{}", post(&pool, 1, "привет").await);\n'
             '    println!("{}", post(&pool, 2, "эй").await);\n'
             '}\n',
  'driver': '',
  'hint': 'Код 23503 — foreign_key_violation.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['ок', 'нет комнаты'],
  'postgres': True},
 {'id': 'r47-check-violation',
  'mode': 'rust',
  'title': 'Ограничение CHECK',
  'statement': 'Таблица messages(text TEXT NOT NULL CHECK (length(trim(text)) > 0)). Напечатайте '
               'SQLSTATE кода ошибки при вставке «   » (пробелы) и при вставке NULL, а также «ок» '
               'для нормального текста.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '23514\n'
               '23502\n'
               'ок',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'Пустой текст — 23514 (check_violation), NULL — 23502 (not_null_violation).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['23514', '23502', 'ок'],
  'postgres': True},
 {'id': 'r47-rename',
  'mode': 'rust',
  'title': 'Переименование столбца',
  'statement': 'Запрос SELECT id, name AS room_name FROM rooms должен собираться в структуру Room '
               '{ id: i64, title: String } — свяжите поле title со столбцом room_name атрибутом '
               '#[sqlx(rename = ...)]. Выведите комнаты в порядке id.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Room { id: 1, title: "общая" }\n'
               'Room { id: 2, title: "dev" }',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[derive(FromRow, Debug)]\n'
             'struct Room {\n'
             '    id: i64,\n'
             '    title: String,\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE rooms (id BIGSERIAL PRIMARY KEY, name '
             'TEXT)").execute(&pool).await.unwrap();\n'
             '    sqlx::query("INSERT INTO rooms (name) VALUES (\'общая\'), '
             '(\'dev\')").execute(&pool).await.unwrap();\n'
             '    let rooms: Vec<Room> = sqlx::query_as("SELECT id, name AS room_name FROM rooms '
             'ORDER BY id").fetch_all(&pool).await.unwrap();\n'
             '    for r in rooms {\n'
             '        println!("{r:?}");\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': '#[sqlx(rename = "room_name")] на поле title.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Room { id: 1, title: "общая" }', 'Room { id: 2, title: "dev" }'],
  'postgres': True},
 {'id': 'r47-keyset',
  'mode': 'rust',
  'title': 'Пагинация по ключу',
  'statement': 'В таблице messages(id BIGSERIAL PK, text TEXT) двенадцать сообщений «m1»…«m12». '
               'Напишите функцию page(&PgPool, before: Option<i64>, limit: i64) -> Vec<(i64, '
               'String)>: сообщения с id меньше before (или все, если None) от новых к старым, не '
               'больше limit. Напечатайте id страниц по 5 сообщений, пока страницы не закончатся.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '[12, 11, 10, 9, 8]\n'
               '[7, 6, 5, 4, 3]\n'
               '[2, 1]',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             'async fn page(pool: &PgPool, before: Option<i64>, limit: i64) -> Vec<(i64, String)> '
             '{\n'
             '    todo!()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE messages (id BIGSERIAL PRIMARY KEY, text '
             'TEXT)").execute(&pool).await.unwrap();\n'
             '    for i in 1..=12 {\n'
             '        sqlx::query("INSERT INTO messages (text) VALUES '
             '($1)").bind(format!("m{i}")).execute(&pool).await.unwrap();\n'
             '    }\n'
             '    let mut before = None;\n'
             '    loop {\n'
             '        let p = page(&pool, before, 5).await;\n'
             '        if p.is_empty() {\n'
             '            break;\n'
             '        }\n'
             '        println!("{:?}", p.iter().map(|(id, _)| *id).collect::<Vec<_>>());\n'
             '        before = p.last().map(|(id, _)| *id);\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'WHERE ($1::bigint IS NULL OR id < $1) ORDER BY id DESC LIMIT $2.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['[12, 11, 10, 9, 8]', '[7, 6, 5, 4, 3]', '[2, 1]'],
  'postgres': True},
 {'id': 'r47-stream',
  'mode': 'rust',
  'title': 'Потоковое чтение',
  'statement': 'Таблица nums(n INT) со значениями 1…10. Прочитайте её потоком (fetch и '
               'TryStreamExt::try_next) и накапливайте сумму, останавливаясь, как только сумма '
               'превысит 20. Напечатайте, сколько строк прочитано и итоговую сумму.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'прочитано 6, сумма 21',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'use futures::TryStreamExt; let mut s = query_scalar::<_, i32>(..).fetch(&pool); while '
          'let Some(n) = s.try_next().await.unwrap() { .. }',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['прочитано 6, сумма 21'],
  'postgres': True},
 {'id': 'r47-unnest',
  'mode': 'rust',
  'title': 'Массовая вставка',
  'statement': 'Таблица users(name TEXT UNIQUE). Функция add_many(&PgPool, &[String]) -> u64 '
               'вставляет все имена ОДНИМ запросом через UNNEST($1::text[]) с ON CONFLICT DO '
               'NOTHING и возвращает число реально добавленных. Вызовите для ["a","b","c"], затем '
               'для ["b","c","d","e"] и напечатайте результаты и итоговое число строк.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '3\n'
               '2\n'
               'итого 5',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             'async fn add_many(pool: &PgPool, names: &[String]) -> u64 {\n'
             '    todo!()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE users (name TEXT '
             'UNIQUE)").execute(&pool).await.unwrap();\n'
             '    let a: Vec<String> = ["a", "b", "c"].iter().map(|s| s.to_string()).collect();\n'
             '    let b: Vec<String> = ["b", "c", "d", "e"].iter().map(|s| '
             's.to_string()).collect();\n'
             '    println!("{}", add_many(&pool, &a).await);\n'
             '    println!("{}", add_many(&pool, &b).await);\n'
             '    let n: i64 = sqlx::query_scalar("SELECT COUNT(*) FROM '
             'users").fetch_one(&pool).await.unwrap();\n'
             '    println!("итого {n}");\n'
             '}\n',
  'driver': '',
  'hint': 'INSERT INTO users (name) SELECT * FROM UNNEST($1::text[]) ON CONFLICT DO NOTHING; '
          'bind(&[String]).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['3', '2', 'итого 5'],
  'postgres': True},
 {'id': 'r47-any-array',
  'mode': 'rust',
  'title': 'Выбор по массиву идентификаторов',
  'statement': 'Таблица users(id BIGSERIAL PK, name TEXT) с шестью пользователями u1…u6. Функция '
               'names_of(&PgPool, &[i64]) -> Vec<String> одним запросом возвращает имена для '
               'заданных id (WHERE id = ANY($1)) в порядке возрастания id. Проверьте для [5, 2, '
               '99, 2].\n'
               '\n'
               'Ожидаемый вывод:\n'
               '["u2", "u5"]\n'
               '[]',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             'async fn names_of(pool: &PgPool, ids: &[i64]) -> Vec<String> {\n'
             '    todo!()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE users (id BIGSERIAL PRIMARY KEY, name '
             'TEXT)").execute(&pool).await.unwrap();\n'
             '    for i in 1..=6 {\n'
             '        sqlx::query("INSERT INTO users (name) VALUES '
             '($1)").bind(format!("u{i}")).execute(&pool).await.unwrap();\n'
             '    }\n'
             '    println!("{:?}", names_of(&pool, &[5, 2, 99, 2]).await);\n'
             '    println!("{:?}", names_of(&pool, &[]).await);\n'
             '}\n',
  'driver': '',
  'hint': 'bind(ids) для &[i64]; id = ANY($1) ORDER BY id.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['["u2", "u5"]', '[]'],
  'postgres': True},
 {'id': 'r47-join-group',
  'mode': 'rust',
  'title': 'Один запрос вместо цикла',
  'statement': 'Таблицы rooms(id BIGSERIAL PK, name TEXT) и members(room_id BIGINT, user_name '
               'TEXT): комнаты «a», «b», «c»; в a два участника, в b ни одного, в c три. Одним '
               'запросом (LEFT JOIN + GROUP BY) получите (название, число участников) для всех '
               'комнат по названию.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '[("a", 2), ("b", 0), ("c", 3)]',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'SELECT r.name, COUNT(m.user_name) FROM rooms r LEFT JOIN members m ON m.room_id = r.id '
          'GROUP BY r.name ORDER BY r.name.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['[("a", 2), ("b", 0), ("c", 3)]'],
  'postgres': True},
 {'id': 'r47-migrator',
  'mode': 'rust',
  'title': 'Свой исполнитель миграций',
  'statement': 'Напишите функцию migrate(&PgPool, &[(i32, &str)]) -> Vec<i32>: создаёт служебную '
               'таблицу _migrations(version INT PRIMARY KEY), затем для каждой миграции в порядке '
               'версий применяет SQL (в sqlx 0.9 текст запроса, не являющийся литералом, '
               'оборачивают в sqlx::AssertSqlSafe(String) — мы сами отвечаем за его безопасность) '
               'в транзакции вместе с записью версии, пропуская уже применённые; возвращает '
               'версии, применённые в этом вызове. Вызовите дважды: сначала с миграциями 1 и 2, '
               'затем с 1, 2, 3 — второй вызов должен применить только 3. Напечатайте результаты и '
               'список столбцов таблицы users.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '[1, 2]\n'
               '[3]\n'
               '[]\n'
               '["id", "name", "bio", "city"]',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             'async fn migrate(pool: &PgPool, migrations: &[(i32, &str)]) -> Vec<i32> {\n'
             '    todo!()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    let m1 = [(1, "CREATE TABLE users (id BIGSERIAL PRIMARY KEY, name TEXT)"), (2, '
             '"ALTER TABLE users ADD COLUMN bio TEXT")];\n'
             '    println!("{:?}", migrate(&pool, &m1).await);\n'
             '    let m2 = [(1, "CREATE TABLE users (id BIGSERIAL PRIMARY KEY, name TEXT)"), (2, '
             '"ALTER TABLE users ADD COLUMN bio TEXT"), (3, "ALTER TABLE users ADD COLUMN city '
             'TEXT")];\n'
             '    println!("{:?}", migrate(&pool, &m2).await);\n'
             '    println!("{:?}", migrate(&pool, &m2).await);\n'
             '    let cols: Vec<String> = sqlx::query_scalar("SELECT column_name::text FROM '
             "information_schema.columns WHERE table_name = 'users' ORDER BY "
             'ordinal_position").fetch_all(&pool).await.unwrap();\n'
             '    println!("{cols:?}");\n'
             '}\n',
  'driver': '',
  'hint': 'Сначала SELECT version FROM _migrations; для новых — begin, execute(sql), INSERT '
          'версию, commit.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['[1, 2]', '[3]', '[]', '["id", "name", "bio", "city"]'],
  'postgres': True},
 {'id': 'r47-pool-timeout',
  'mode': 'rust',
  'title': 'Исчерпание пула',
  'statement': 'Создайте пул на одно соединение с acquire_timeout 100 мс '
               '(PgPoolOptions::new().max_connections(1).acquire_timeout(...).connect(...)). '
               'Захватите соединение (acquire) и держите, пока второй acquire не завершится '
               'ошибкой: напечатайте «пул исчерпан: true» (sqlx::Error::PoolTimedOut). Освободите '
               'первое соединение и убедитесь, что запрос SELECT 1 снова работает.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'пул исчерпан: true\n'
               'после освобождения: 1',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'matches!(err, sqlx::Error::PoolTimedOut); drop(conn) возвращает соединение в пул.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['пул исчерпан: true', 'после освобождения: 1'],
  'postgres': True},
 {'id': 'r47-parallel',
  'mode': 'rust',
  'title': 'Параллельные вставки',
  'statement': 'Таблица counters(id INT PRIMARY KEY, n BIGINT). В одной строке (id = 1, n = 0) '
               'пятьдесят задач (tokio::spawn) параллельно выполняют UPDATE counters SET n = n + 1 '
               'WHERE id = 1 через пул из 5 соединений. После всех напечатайте итоговое значение n '
               '(должно быть 50 — база сериализует обновления строки).\n'
               '\n'
               'Ожидаемый вывод:\n'
               '50',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'Клонируйте пул в каждую задачу; дождитесь JoinHandle.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['50'],
  'postgres': True},
 {'id': 'r47-skip-locked',
  'mode': 'rust',
  'title': 'Очередь заданий: SKIP LOCKED',
  'statement': 'Таблица jobs(id SERIAL PK, done BOOLEAN DEFAULT false) с шестью заданиями. Функция '
               'claim(&PgPool) -> Option<i32> в транзакции выбирает свободное задание с FOR UPDATE '
               'SKIP LOCKED, помечает его выполненным и возвращает id; None, если свободных нет. '
               'Четыре исполнителя (spawn) по два раза вызывают claim — все полученные id должны '
               'быть различны. Напечатайте отсортированный список полученных id и число '
               'оставшихся.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '[1, 2, 3, 4, 5, 6]\n'
               'осталось 0',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             'async fn claim(pool: &PgPool) -> Option<i32> {\n'
             '    todo!()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE jobs (id SERIAL PRIMARY KEY, done BOOLEAN NOT NULL '
             'DEFAULT false)").execute(&pool).await.unwrap();\n'
             '    sqlx::query("INSERT INTO jobs SELECT FROM generate_series(1, '
             '6)").execute(&pool).await.unwrap();\n'
             '    let handles: Vec<_> = (0..4)\n'
             '        .map(|_| {\n'
             '            let pool = pool.clone();\n'
             '            tokio::spawn(async move {\n'
             '                let mut got = Vec::new();\n'
             '                for _ in 0..2 {\n'
             '                    if let Some(id) = claim(&pool).await {\n'
             '                        got.push(id);\n'
             '                    }\n'
             '                }\n'
             '                got\n'
             '            })\n'
             '        })\n'
             '        .collect();\n'
             '    let mut all = Vec::new();\n'
             '    for h in handles {\n'
             '        all.extend(h.await.unwrap());\n'
             '    }\n'
             '    all.sort();\n'
             '    println!("{all:?}");\n'
             '    let left: i64 = sqlx::query_scalar("SELECT COUNT(*) FROM jobs WHERE NOT '
             'done").fetch_one(&pool).await.unwrap();\n'
             '    println!("осталось {left}");\n'
             '}\n',
  'driver': '',
  'hint': 'SELECT id FROM jobs WHERE NOT done ORDER BY id LIMIT 1 FOR UPDATE SKIP LOCKED; затем '
          'UPDATE; commit.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['[1, 2, 3, 4, 5, 6]', 'осталось 0'],
  'postgres': True},
 {'id': 'r47-listen-notify',
  'mode': 'rust',
  'title': 'LISTEN / NOTIFY',
  'statement': 'Подпишитесь на канал «chat» через sqlx::postgres::PgListener '
               '(listener.listen("chat")), затем из пула выполните SELECT pg_notify(\'chat\', $1) '
               'с полезной нагрузкой «привет из базы» и ещё одной «второе». Напечатайте канал и '
               'нагрузку двух полученных уведомлений (listener.recv()).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'chat: привет из базы\n'
               'chat: второе',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    // ваш код\n'
             '    let _ = pool;\n'
             '}\n',
  'driver': '',
  'hint': 'PgListener::connect_with(&pool).await?; listener.listen("chat"); n.channel(), '
          'n.payload().',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['chat: привет из базы', 'chat: второе'],
  'postgres': True},
 {'id': 'r47-fix-placeholder',
  'mode': 'rust',
  'title': 'Исправьте: плейсхолдеры',
  'statement': 'Программа падает при выполнении: в запросах использованы «?» вместо параметров '
               'PostgreSQL. Исправьте запросы ($1, $2), чтобы программа печатала «добавлена аня» и '
               '«найдена: аня».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'добавлена аня\n'
               'найдена: аня',
  'starter': 'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE users (id BIGSERIAL PRIMARY KEY, name '
             'TEXT)").execute(&pool).await.unwrap();\n'
             '    sqlx::query("INSERT INTO users (name) VALUES '
             '(?)").bind("аня").execute(&pool).await.unwrap();\n'
             '    println!("добавлена аня");\n'
             '    let n: String = sqlx::query_scalar("SELECT name FROM users WHERE id = '
             '?").bind(1i64).fetch_one(&pool).await.unwrap();\n'
             '    println!("найдена: {n}");\n'
             '}\n',
  'driver': '',
  'hint': 'В PostgreSQL параметры нумеруются: $1, $2, …',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['добавлена аня', 'найдена: аня'],
  'postgres': True},
 {'id': 'r47-http-rooms',
  'mode': 'rust',
  'title': 'Комнаты по HTTP из базы',
  'statement': 'Состояние приложения — PgPool (таблица rooms(id BIGSERIAL PK, name TEXT UNIQUE NOT '
               'NULL) создаётся в main до запросов). POST /rooms/{name} создаёт комнату и отвечает '
               '201 и JSON {"id":N,"name":".."} (RETURNING); повтор — 409 и текст «имя занято» '
               '(нарушение уникальности 23505). GET /rooms отвечает JSON-массивом комнат по id. '
               'Заготовка содержит пустой app(pool). Напечатайте ответы на три POST (общая, dev, '
               'общая) и GET.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '(201, "{\\"id\\":1,\\"name\\":\\"общая\\"}")\n'
               '(201, "{\\"id\\":2,\\"name\\":\\"dev\\"}")\n'
               '(409, "имя занято")\n'
               '(200, "[{\\"id\\":1,\\"name\\":\\"общая\\"},{\\"id\\":2,\\"name\\":\\"dev\\"}]")',
  'starter': 'use axum::body::{to_bytes, Body};\n'
             'use axum::http::{Request, StatusCode};\n'
             'use axum::Router;\n'
             'use tower::ServiceExt;\n'
             '\n'
             '// Готово: отправляет запрос в роутер без сети и возвращает (статус, тело)\n'
             'async fn call(app: &Router, method: &str, uri: &str, body: &str) -> (StatusCode, '
             'String) {\n'
             '    let req = Request::builder()\n'
             '        .method(method)\n'
             '        .uri(uri)\n'
             '        .header("content-type", "application/json")\n'
             '        .body(Body::from(body.to_string()))\n'
             '        .unwrap();\n'
             '    let res = app.clone().oneshot(req).await.unwrap();\n'
             '    let status = res.status();\n'
             '    let bytes = to_bytes(res.into_body(), 1 << 20).await.unwrap();\n'
             '    (status, String::from_utf8_lossy(&bytes).into_owned())\n'
             '}\n'
             '\n'
             'use sqlx::postgres::PgPoolOptions;\n'
             'use sqlx::{FromRow, PgPool, Row};\n'
             '\n'
             '// Готово: PostgreSQL уже запущен в песочнице (пользователь postgres без пароля, '
             'база chat), каждая проверка — чистая база\n'
             'async fn pool() -> PgPool {\n'
             '    PgPoolOptions::new()\n'
             '        .max_connections(5)\n'
             '        .connect("postgres://postgres@127.0.0.1/chat")\n'
             '        .await\n'
             '        .unwrap()\n'
             '}\n'
             '\n'
             'use axum::Router;\n'
             '\n'
             'fn app(pool: PgPool) -> Router {\n'
             '    let _ = pool;\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let pool = pool().await;\n'
             '    sqlx::query("CREATE TABLE rooms (id BIGSERIAL PRIMARY KEY, name TEXT UNIQUE NOT '
             'NULL)").execute(&pool).await.unwrap();\n'
             '    let app = app(pool);\n'
             '    for n in ["общая", "dev", "общая"] {\n'
             '        println!("{:?}", call(&app, "POST", &format!("/rooms/{n}"), "").await);\n'
             '    }\n'
             '    println!("{:?}", call(&app, "GET", "/rooms", "").await);\n'
             '}\n',
  'driver': '',
  'hint': "Handler с State<PgPool>, Result<(StatusCode, Json<Room>), (StatusCode, &'static str)>; "
          'query_as::<_, Room> с #[derive(FromRow, Serialize)].',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['(201, "{\\"id\\":1,\\"name\\":\\"общая\\"}")',
               '(201, "{\\"id\\":2,\\"name\\":\\"dev\\"}")',
               '(409, "имя занято")',
               '(200, "[{\\"id\\":1,\\"name\\":\\"общая\\"},{\\"id\\":2,\\"name\\":\\"dev\\"}]")'],
  'postgres': True}]}
