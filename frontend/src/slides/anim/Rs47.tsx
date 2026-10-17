import { scene } from "./alg.tsx";
import { Box, arrow, note, rs } from "./rs.tsx";

/* Глава 47 книги «Изучаем Rust»: PostgreSQL и sqlx — данные чата. */

const code = { w: 340, size: 9.5, lh: 14 };

// 1. Данные чата
export const V01 = scene({
  labels: ["Память", "Данные", "Связь миров"],
  caption: [
    "Комнаты в памяти пропадают при перезапуске; чату нужна надёжная память",
    "Пользователи, комнаты, участники, история сообщений — в PostgreSQL",
    "Строки → структуры, ошибки базы → ошибки приложения, изменения → транзакции",
  ],
  frames: [
    [Box("a", 90, 70, 130, 36, "HashMap в памяти", "y", { size: 10 }), arrow("e", 156, 70, 214, 70, "r"), Box("b", 290, 70, 130, 36, "перезапуск: пусто", "r", { size: 10 })],
    [Box("a", 70, 50, 100, 26, "users", "b", { size: 10.5 }), Box("b", 180, 50, 100, 26, "rooms", "b", { size: 10.5 }), Box("c", 290, 50, 100, 26, "members", "b", { size: 10.5 }), Box("d", 180, 110, 160, 26, "messages", "g", { size: 10.5 })],
    [Box("a", 70, 70, 100, 30, "строки", "b", { size: 10.5 }), arrow("e1", 120, 70, 134, 70, "g"), Box("b", 180, 70, 100, 30, "структуры", "g", { size: 10.5 }), arrow("e2", 230, 70, 244, 70, "g"), Box("c", 300, 70, 100, 30, "AppError", "g", { size: 10.5 })],
  ],
});

// 2. Почему PostgreSQL
export const V02 = scene({
  labels: ["Транзакции", "Ограничения", "Параллельность"],
  caption: [
    "Либо все изменения, либо ни одного; изоляция между одновременными транзакциями",
    "UNIQUE, FOREIGN KEY, CHECK: некорректное состояние нельзя записать",
    "Читатели не мешают писателям; много процессов сервера работают с одной базой",
  ],
  frames: [
    [Box("a", 90, 70, 100, 30, "BEGIN", "g", { size: 11 }), Box("b", 220, 70, 80, 30, "ещё", "b", { size: 10.5 }), Box("c", 320, 70, 80, 30, "COMMIT", "g", { size: 10.5 }), arrow("e1", 140, 70, 180, 70, "m"), arrow("e2", 260, 70, 280, 70, "m")],
    [Box("a", 90, 40, 130, 24, "UNIQUE (name)", "b", { size: 10 }), Box("b", 90, 80, 130, 24, "FOREIGN KEY room_id", "b", { size: 9 }), Box("c", 90, 120, 130, 24, "CHECK (text <> '')", "b", { size: 9.5 }), note("n", 280, 80, "ловят ошибки\nна уровне базы", "m")],
    [Box("a", 70, 40, 70, 22, "сервер 1", "b", { size: 9.5 }), Box("b", 70, 80, 70, 22, "сервер 2", "b", { size: 9.5 }), Box("c", 70, 120, 70, 22, "сервер 3", "b", { size: 9.5 }), arrow("e1", 106, 40, 186, 72, "m"), arrow("e2", 106, 80, 186, 80, "m"), arrow("e3", 106, 120, 186, 88, "m"), Box("d", 250, 80, 110, 36, "PostgreSQL", "g", { size: 11 })],
  ],
});

// 3. sqlx
export const V03 = scene({
  labels: ["Без ORM", "Чистый Rust", "Что написано — то выполняется"],
  caption: [
    "Запросы пишете на настоящем SQL; библиотека ведёт соединения и разбор строк",
    "Асинхронный драйвер протокола PostgreSQL поверх tokio",
    "Прозрачно: план запроса и производительность остаются под вашим контролем",
  ],
  frames: [
    [rs("c", 10, 20, ["sqlx::query_as::<_, Room>(", "    \"SELECT id, name FROM rooms WHERE id = $1\"", ")", ".bind(id).fetch_one(&pool).await?"], [1, 3], { ...code, lh: 24, size: 9 })],
    [Box("a", 70, 40, 100, 24, "ваш код", "y", { size: 10 }), Box("b", 70, 80, 100, 24, "sqlx", "g", { size: 10.5 }), Box("c", 70, 120, 100, 24, "tokio + TCP", "b", { size: 10 }), arrow("e1", 70, 52, 70, 68, "m"), arrow("e2", 70, 92, 70, 108, "m"), Box("d", 270, 80, 130, 30, "протокол Postgres", "b", { size: 9.5 })],
    [Box("a", 90, 60, 130, 26, "SQL как есть", "g", { size: 10.5 }), Box("b", 90, 110, 130, 26, "EXPLAIN, индексы", "g", { size: 10 }), note("n", 280, 85, "контроль у вас", "m")],
  ],
});

// 4. Пул
export const V04 = scene({
  labels: ["Пул соединений", "Предел", "Не держать долго"],
  caption: [
    "Пул держит несколько соединений и выдаёт свободное по требованию",
    "Размер ограничен: у базы свой предел подключений; нет свободных — запрос ждёт",
    "Соединение нельзя держать на время посторонних долгих операций",
  ],
  frames: [
    [Box("p", 180, 40, 150, 26, "PgPool (клонируется)", "g", { size: 10 }), Box("a", 70, 110, 60, 22, "conn 1", "b", { size: 9.5 }), Box("b", 150, 110, 60, 22, "conn 2", "b", { size: 9.5 }), Box("c", 230, 110, 60, 22, "conn 3", "b", { size: 9.5 }), Box("d", 310, 110, 60, 22, "conn 4", "b", { size: 9.5 }), arrow("e1", 150, 54, 82, 98, "m"), arrow("e2", 170, 54, 150, 98, "m"), arrow("e3", 190, 54, 224, 98, "m"), arrow("e4", 210, 54, 296, 98, "m")],
    [Box("a", 70, 40, 90, 22, "занято", "r", { size: 9.5 }), Box("b", 160, 40, 90, 22, "занято", "r", { size: 9.5 }), Box("c", 250, 40, 90, 22, "запрос ждёт", "y", { size: 9.5 }), rs("n", 10, 80, ["PgPoolOptions::new()", "    .max_connections(5)", "    .acquire_timeout(Duration::from_secs(3))"], [1, 2], { ...code, lh: 20, size: 9 })],
    [rs("c", 10, 20, ["let mut conn = pool.acquire().await?;", "http_client.get(url).await;   // долго!", "// соединение занято всё это время"], [1, 2], { ...code, lh: 28, size: 9, bad: [1, 2] })],
  ],
});

// 5. Запросы
export const V05 = scene({
  labels: ["Три функции", "bind", "Результаты"],
  caption: [
    "query — сырые строки, query_as — структуры, query_scalar — одно значение",
    "Параметры $1, $2 уходят отдельно от текста: никакой подстановки строк",
    "fetch_one, fetch_optional, fetch_all, fetch (поток); нет строки — RowNotFound",
  ],
  frames: [
    [Box("a", 70, 50, 100, 26, "query", "b", { size: 11 }), note("n1", 220, 50, "сырые строки", "m"), Box("b", 70, 90, 100, 26, "query_as", "b", { size: 11 }), note("n2", 220, 90, "структуры", "m"), Box("c", 70, 130, 100, 26, "query_scalar", "b", { size: 10.5 }), note("n3", 220, 130, "одно значение", "m")],
    [rs("c", 10, 20, ["// плохо: внедрение чужого кода", "format!(\"... WHERE name = '{}'\", name)", "// хорошо: параметр отдельно", "query(\"... WHERE name = $1\").bind(name)"], [1, 3], { ...code, lh: 26, size: 9, bad: [1] })],
    [Box("a", 70, 40, 110, 24, "fetch_one", "g", { size: 10 }), note("n1", 240, 40, "ровно одна, иначе Err", "m"), Box("b", 70, 80, 110, 24, "fetch_optional", "g", { size: 10 }), note("n2", 240, 80, "Option", "m"), Box("c", 70, 120, 110, 24, "fetch_all", "g", { size: 10 }), note("n3", 240, 120, "Vec / поток fetch", "m")],
  ],
});

// 6. Типы и FromRow
export const V06 = scene({
  labels: ["FromRow", "Соответствие типов", "NULL и переименование"],
  caption: [
    "Структура собирается из строки по именам столбцов",
    "BIGINT↔i64, TEXT↔String, TIMESTAMPTZ↔DateTime<Utc>, UUID↔Uuid, JSONB↔Json",
    "Столбец с NULL — Option<T>; #[sqlx(rename)] задаёт имя столбца",
  ],
  frames: [
    [rs("c", 10, 20, ["#[derive(FromRow)]", "struct Msg { id: i64, room_id: i64, text: String }", "", "query_as::<_, Msg>(\"SELECT * FROM messages\")"], [0, 3], { ...code, lh: 24, size: 9 })],
    [Box("a", 80, 40, 100, 22, "BIGINT", "b", { size: 10 }), Box("b", 80, 70, 100, 22, "TEXT", "b", { size: 10 }), Box("c", 80, 100, 100, 22, "TIMESTAMPTZ", "b", { size: 9.5 }), Box("d", 80, 130, 100, 22, "UUID / JSONB", "b", { size: 9.5 }), Box("e", 270, 40, 130, 22, "i64", "g", { size: 10 }), Box("f", 270, 70, 130, 22, "String", "g", { size: 10 }), Box("g", 270, 100, 130, 22, "DateTime<Utc>", "g", { size: 10 }), Box("h", 270, 130, 130, 22, "Uuid / Json<T>", "g", { size: 10 })],
    [rs("c", 10, 20, ["struct User {", "    id: i64,", "    bio: Option<String>,          // NULL → None", "    #[sqlx(rename = \"room_name\")] room: String,", "}"], [2, 3], { ...code, lh: 22, size: 9 })],
  ],
});

// 7. RETURNING
export const V07 = scene({
  labels: ["RETURNING", "ON CONFLICT", "rows_affected"],
  caption: [
    "Вставка сразу возвращает созданную строку: без гонки между INSERT и SELECT",
    "DO NOTHING — повтор безвреден; DO UPDATE — атомарное «вставить или обновить»",
    "Выполнение сообщает, сколько строк затронуто на самом деле",
  ],
  frames: [
    [rs("c", 10, 20, ["let id: i64 = query_scalar(", "    \"INSERT INTO rooms(name) VALUES ($1) RETURNING id\")", "    .bind(name).fetch_one(&pool).await?;"], [1], { ...code, lh: 26, size: 9 })],
    [rs("c", 10, 20, ["INSERT INTO hits(path, n) VALUES ($1, 1)", "ON CONFLICT (path) DO UPDATE SET n = hits.n + 1", "-- один атомарный запрос вместо «прочитать и записать»"], [1], { ...code, lh: 28, size: 8.5 })],
    [Box("a", 90, 60, 130, 26, "1 строка вставлена", "g", { size: 10 }), Box("b", 90, 110, 130, 26, "0 — уже была", "y", { size: 10.5 }), note("n", 280, 85, "res.rows_affected()", "m")],
  ],
});

// 8. Транзакции
export const V08 = scene({
  labels: ["begin / commit", "Откат при drop", "Блокировка строк"],
  caption: [
    "Запросы идут через объект транзакции; commit фиксирует результат",
    "Ранний выход по ошибке или drop без commit — изменения откатываются сами",
    "FOR UPDATE SKIP LOCKED: исполнители берут разные задания и не мешают друг другу",
  ],
  frames: [
    [rs("c", 10, 14, ["let mut tx = pool.begin().await?;", "query(\"INSERT INTO rooms ..\").execute(&mut *tx).await?;", "query(\"INSERT INTO members ..\").execute(&mut *tx).await?;", "tx.commit().await?;"], [0, 3], { ...code, lh: 22, size: 8.5 })],
    [rs("c", 10, 20, ["let mut tx = pool.begin().await?;", "do_work(&mut tx).await?;     // Err → return", "// tx уничтожен без commit → ROLLBACK"], [1, 2], { ...code, lh: 28, size: 9 })],
    [rs("c", 10, 20, ["SELECT id FROM jobs", "WHERE done = false", "ORDER BY id LIMIT 1", "FOR UPDATE SKIP LOCKED"], [3], { ...code, lh: 24, size: 9.5 })],
  ],
});

// 9. Миграции
export const V09 = scene({
  labels: ["Файлы", "Таблица версий", "Не править"],
  caption: [
    "Пронумерованные SQL-файлы: 0001_users.sql, 0002_rooms.sql …",
    "Служебная таблица помнит применённые; запуск доводит базу до последней",
    "Применённую миграцию не меняют: правка схемы — новая миграция",
  ],
  frames: [
    [rs("c", 10, 20, ["migrations/", "  0001_users.sql", "  0002_rooms.sql", "  0003_messages.sql"], [1, 2, 3], { ...code, lh: 26, size: 10.5 })],
    [Box("a", 90, 50, 140, 24, "_migrations", "b", { size: 10.5 }), note("n", 270, 50, "1, 2 применены", "m"), Box("b", 90, 100, 140, 24, "0003_…sql", "y", { size: 10 }), arrow("e", 156, 100, 220, 100, "g"), Box("c", 290, 100, 100, 24, "применить", "g", { size: 10 })],
    [Box("a", 90, 60, 150, 26, "0002 изменён задним числом", "r", { size: 9 }), note("n1", 290, 60, "базы расходятся", "r"), Box("b", 90, 110, 150, 26, "0004_alter.sql — новая", "g", { size: 9.5 }), note("n2", 290, 110, "так правильно", "g")],
  ],
});

// 10. Схема чата
export const V10 = scene({
  labels: ["Таблицы", "Ограничения", "Индекс"],
  caption: [
    "users, rooms, members и messages — минимальная схема чата",
    "UNIQUE на именах, внешние ключи на комнату и автора, CHECK на текст",
    "Индекс (room_id, id DESC) делает быстрой выборку последних сообщений комнаты",
  ],
  frames: [
    [Box("u", 70, 50, 90, 26, "users", "b", { size: 10.5 }), Box("r", 180, 50, 90, 26, "rooms", "b", { size: 10.5 }), Box("m", 290, 50, 90, 26, "members", "b", { size: 10.5 }), Box("g", 180, 115, 110, 26, "messages", "g", { size: 10.5 }), arrow("e1", 116, 62, 270, 56, "m"), arrow("e2", 180, 64, 180, 102, "m"), arrow("e3", 250, 62, 214, 104, "m")],
    [rs("c", 10, 14, ["name TEXT NOT NULL UNIQUE,", "room_id BIGINT NOT NULL REFERENCES rooms(id),", "author_id BIGINT NOT NULL REFERENCES users(id),", "text TEXT NOT NULL CHECK (text <> '')"], [0, 1, 2, 3], { ...code, lh: 24, size: 8.5 })],
    [rs("c", 10, 20, ["CREATE INDEX messages_room_id", "    ON messages (room_id, id DESC);", "-- WHERE room_id = $1 ORDER BY id DESC LIMIT 50"], [0, 1], { ...code, lh: 28, size: 9.5 })],
  ],
});

// 11. Ошибки базы
export const V11 = scene({
  labels: ["Нет строки", "Коды SQLSTATE", "В AppError"],
  caption: [
    "RowNotFound — не сбой, а вариант «не найдено»",
    "23505 — повтор уникального значения, 23503 — внешний ключ, 23514 — проверка",
    "Уникальность → Conflict, внешний ключ → NotFound/Invalid, остальное → Internal + журнал",
  ],
  frames: [
    [Box("a", 90, 70, 130, 30, "RowNotFound", "y", { size: 10.5 }), arrow("e", 156, 70, 214, 70, "m"), Box("b", 290, 70, 130, 30, "404 Not Found", "g", { size: 10.5 })],
    [Box("a", 80, 40, 100, 24, "23505", "y", { size: 11 }), note("n1", 240, 40, "unique_violation", "m"), Box("b", 80, 80, 100, 24, "23503", "y", { size: 11 }), note("n2", 240, 80, "foreign_key_violation", "m"), Box("c", 80, 120, 100, 24, "23514", "y", { size: 11 }), note("n3", 240, 120, "check_violation", "m")],
    [rs("c", 10, 14, ["match e.as_database_error().and_then(|d| d.code()).as_deref() {", "    Some(\"23505\") => AppError::Conflict(..),", "    Some(\"23503\") => AppError::NotFound,", "    _ => AppError::Internal(e.to_string()),", "}"], [1, 2, 3], { ...code, lh: 20, size: 8 })],
  ],
});

// 12. Эффективность
export const V12 = scene({
  labels: ["Индекс", "N+1", "Ключевая пагинация"],
  caption: [
    "Индекс под частую выборку ускоряет её на порядки; EXPLAIN показывает план",
    "Запрос в цикле — беда: заменяем одним запросом с JOIN или = ANY($1)",
    "«До id N» использует индекс; OFFSET вынужден пропускать строки",
  ],
  frames: [
    [Box("a", 90, 50, 130, 26, "Seq Scan: 12 000 мс", "r", { size: 9.5 }), arrow("e", 156, 50, 214, 50, "g"), Box("b", 290, 50, 130, 26, "Index Scan: 2 мс", "g", { size: 10 }), note("n", 180, 110, "EXPLAIN ANALYZE", "m")],
    [rs("c", 10, 20, ["for room in rooms {            // N запросов", "    members_of(room.id).await?;", "}", "WHERE room_id = ANY($1)       // один запрос"], [0, 1, 3], { ...code, lh: 24, size: 9 })],
    [rs("c", 10, 20, ["... WHERE room_id = $1 AND id < $2", "    ORDER BY id DESC LIMIT 50          -- быстро", "... OFFSET 100000 LIMIT 50             -- медленно"], [0, 1, 2], { ...code, lh: 28, size: 8.5 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запросы и типы", "Целостность", "Дальше"],
  caption: [
    "PgPool в состоянии; параметры через bind; FromRow; RETURNING и ON CONFLICT",
    "Транзакции откатываются сами; миграции ведут схему; ошибки по кодам SQLSTATE",
    "Следующая глава: пользователи — регистрация, хеши паролей и вход по токену",
  ],
  frames: [
    [Box("a", 70, 70, 100, 30, "PgPool", "g", { size: 11 }), Box("b", 180, 70, 100, 30, "bind", "g", { size: 11 }), Box("c", 290, 70, 100, 30, "FromRow", "g", { size: 11 })],
    [Box("a", 70, 70, 100, 30, "транзакции", "g", { size: 10 }), Box("b", 180, 70, 100, 30, "миграции", "g", { size: 10.5 }), Box("c", 290, 70, 100, 30, "SQLSTATE", "g", { size: 10.5 })],
    [Box("a", 90, 70, 130, 30, "argon2", "b", { size: 11 }), Box("b", 250, 70, 130, 30, "токены сессий", "b", { size: 10 }), Box("c", 340, 70, 40, 30, "→", "y", { size: 12 })],
  ],
});
