import { scene } from "./alg.tsx";
import { Box, arrow, note, rs } from "./rs.tsx";

/* Глава 46 книги «Изучаем Rust»: JSON, serde и единый тип ошибки. */

const code = { w: 340, size: 9.5, lh: 14 };

// 1. Данные и ошибки
export const V01 = scene({
  labels: ["Граница", "Точные типы", "Единый формат"],
  caption: [
    "Клиент говорит JSON-ом: запрос превращается в типы, ответ — обратно в JSON",
    "Неверное отсекается на входе, внутрь попадают только ожидаемые формы",
    "Любая ошибка выглядит одинаково: клиент разбирает её одним кодом",
  ],
  frames: [
    [Box("a", 60, 70, 80, 30, "JSON", "b", { size: 11 }), arrow("e1", 100, 70, 134, 70, "g"), Box("b", 180, 70, 80, 30, "типы Rust", "g", { size: 10 }), arrow("e2", 220, 70, 254, 70, "g"), Box("c", 300, 70, 80, 30, "JSON", "b", { size: 11 })],
    [Box("a", 90, 60, 130, 26, "{\"name\": 5}", "r", { size: 10 }), arrow("e", 156, 60, 210, 60, "r"), Box("b", 290, 60, 110, 26, "422 на входе", "y", { size: 10 }), Box("c", 90, 110, 130, 26, "{\"name\": \"аня\"}", "g", { size: 10 }), arrow("e2", 156, 110, 210, 110, "g"), Box("d", 290, 110, 110, 26, "struct User", "g", { size: 10 })],
    [Box("a", 70, 40, 100, 24, "не найдено", "y", { size: 10 }), Box("b", 180, 40, 100, 24, "конфликт", "y", { size: 10 }), Box("c", 290, 40, 100, 24, "сбой базы", "y", { size: 10 }), arrow("e1", 70, 54, 160, 96, "m"), arrow("e2", 180, 54, 180, 96, "m"), arrow("e3", 290, 54, 200, 96, "m"), Box("d", 180, 110, 150, 26, "{\"error\": { .. }}", "g", { size: 10 })],
  ],
});

// 2. serde
export const V02 = scene({
  labels: ["Структура ↔ формат", "derive", "Строгий разбор"],
  caption: [
    "serde отделяет данные от формата: JSON, YAML или двоичный",
    "Два производных признака — и структура умеет превращаться и собираться",
    "Неверный тип или пропущенное поле — ошибка с позицией",
  ],
  frames: [
    [Box("a", 70, 70, 100, 36, "Room {\nid, name }", "g", { size: 9.5 }), arrow("e1", 120, 62, 160, 62, "m"), arrow("e2", 160, 78, 120, 78, "m"), Box("b", 220, 40, 90, 22, "JSON", "b", { size: 10 }), Box("c", 220, 70, 90, 22, "YAML", "b", { size: 10 }), Box("d", 220, 100, 90, 22, "бинарный", "b", { size: 10 })],
    [rs("c", 10, 20, ["#[derive(Serialize, Deserialize)]", "struct Room { id: u32, name: String }", "", "let s = serde_json::to_string(&room)?;", "let r: Room = serde_json::from_str(&s)?;"], [0, 3, 4], { ...code, lh: 22, size: 9 })],
    [rs("c", 10, 20, ["from_str::<Room>(\"{\\\"id\\\": \\\"x\\\"}\")", "// Err: invalid type: string \"x\", expected u32", "//      at line 1 column 10"], [1, 2], { ...code, lh: 28, size: 9, bad: [1, 2] })],
  ],
});

// 3. Атрибуты
export const V03 = scene({
  labels: ["Имена", "default и skip", "Строго и гибко"],
  caption: [
    "rename_all превращает snake_case в camelCase для клиентов на JavaScript",
    "default позволяет не присылать поле; skip_serializing_if убирает пустые",
    "deny_unknown_fields ловит опечатки; alias принимает старые имена; flatten сплющивает",
  ],
  frames: [
    [rs("c", 10, 20, ["#[serde(rename_all = \"camelCase\")]", "struct Msg { room_id: u32, sent_at: u64 }", "// {\"roomId\": 1, \"sentAt\": 1700000000}"], [0, 2], { ...code, lh: 28, size: 9 })],
    [rs("c", 10, 20, ["#[serde(default)]", "limit: u32,", "#[serde(skip_serializing_if = \"Option::is_none\")]", "reply_to: Option<u64>,"], [0, 2], { ...code, lh: 24, size: 9.5 })],
    [Box("a", 70, 40, 110, 24, "deny_unknown_fields", "y", { size: 9 }), Box("b", 70, 80, 110, 24, "alias = \"old\"", "y", { size: 9.5 }), Box("c", 70, 120, 110, 24, "flatten", "y", { size: 10 }), note("n1", 270, 40, "опечатка → ошибка", "m"), note("n2", 270, 80, "старое имя принимаем", "m"), note("n3", 270, 120, "поля на одном уровне", "m")],
  ],
});

// 4. Перечисления
export const V04 = scene({
  labels: ["По умолчанию", "tag = \"type\"", "Событие чата"],
  caption: [
    "Вариант — объект с единственным ключом: имя варианта",
    "Внутренний тег: поле type и остальные поля рядом",
    "Клиент смотрит на type и выбирает обработчик",
  ],
  frames: [
    [rs("c", 10, 20, ["enum Event { Join(String), Leave(String) }", "// {\"Join\": \"аня\"}"], [1], { ...code, lh: 30, size: 9.5 })],
    [rs("c", 10, 14, ["#[serde(tag = \"type\", rename_all = \"snake_case\")]", "enum Event {", "    Message { room: u32, text: String },", "    Join { user: String },", "}"], [0], { ...code, lh: 18, size: 9 })],
    [rs("c", 10, 20, ["{\"type\": \"message\", \"room\": 3, \"text\": \"привет\"}", "{\"type\": \"join\", \"user\": \"аня\"}", "{\"type\": \"leave\", \"user\": \"аня\"}"], [0, 1, 2], { ...code, lh: 28, size: 8.5 })],
  ],
});

// 5. Валидация
export const V05 = scene({
  labels: ["Проверка повсюду", "Тип-гарантия", "TryFrom + serde"],
  caption: [
    "Строка с именем: длину придётся проверять в каждом месте",
    "Новый тип создаётся только из допустимой строки — недопустимого значения не существует",
    "try_from в атрибуте serde отвергает плохое имя прямо при разборе тела",
  ],
  frames: [
    [Box("a", 70, 40, 100, 24, "String", "y", { size: 10.5 }), Box("b", 70, 80, 100, 24, "if len < 3 ..", "r", { size: 10 }), Box("c", 70, 120, 100, 24, "if len > 16 ..", "r", { size: 10 }), note("n", 270, 80, "проверки повсюду,\nлегко забыть", "m")],
    [rs("c", 10, 20, ["struct Username(String);", "impl Username {", "    fn parse(s: &str) -> Result<Username, Bad> { .. }", "}", "// чужого значения не создать"], [2], { ...code, lh: 22, size: 8.5 })],
    [rs("c", 10, 20, ["#[derive(Deserialize)]", "#[serde(try_from = \"String\")]", "struct Username(String);", "// JSON {\"user\": \"x\"} → ошибка при разборе"], [1, 3], { ...code, lh: 26, size: 9 })],
  ],
});

// 6. Json и отказы
export const V06 = scene({
  labels: ["Три кода", "Свой экстрактор", "Единый формат"],
  caption: [
    "400 — синтаксис, 415 — Content-Type, 422 — данные не подходят",
    "Обёртка вызывает Json<T> и превращает JsonRejection в AppError",
    "После этого отказы разбора выглядят как остальные ошибки API",
  ],
  frames: [
    [Box("a", 70, 40, 100, 24, "400", "y", { size: 11 }), note("n1", 220, 40, "не JSON", "m"), Box("b", 70, 80, 100, 24, "415", "y", { size: 11 }), note("n2", 220, 80, "нет content-type", "m"), Box("c", 70, 120, 100, 24, "422", "y", { size: 11 }), note("n3", 220, 120, "поля не подходят", "m")],
    [rs("c", 10, 20, ["struct ApiJson<T>(T);", "impl<T, S> FromRequest<S> for ApiJson<T> {", "    type Rejection = AppError;", "    // Json::<T>::from_request(..).map_err(AppError::from)", "}"], [2, 3], { ...code, lh: 22, size: 8.5 })],
    [Box("a", 70, 70, 110, 28, "тело не JSON", "r", { size: 10 }), arrow("e", 126, 70, 168, 70, "m"), Box("b", 240, 70, 150, 40, "400\n{\"error\":{\"code\":\n\"bad_json\"}}", "g", { size: 8.5 })],
  ],
});

// 7. Тип ошибки
export const V07 = scene({
  labels: ["Варианты", "Статус и код", "Один тип"],
  caption: [
    "Не найдено, конфликт, неверные данные, не авторизован, запрещено, внутренняя",
    "Каждый вариант знает HTTP-статус и короткий машинный код",
    "Обработчики возвращают Result<_, AppError> и используют ?",
  ],
  frames: [
    [rs("c", 10, 14, ["enum AppError {", "    NotFound,", "    Conflict(String),", "    Invalid(Vec<FieldError>),", "    Unauthorized,", "    Internal(String),", "}"], [1, 2, 3, 4, 5], { ...code, lh: 17, size: 9 })],
    [Box("a", 80, 40, 110, 22, "NotFound → 404", "b", { size: 9 }), Box("b", 80, 70, 110, 22, "Conflict → 409", "b", { size: 9 }), Box("c", 80, 100, 110, 22, "Invalid → 422", "b", { size: 9 }), Box("d", 80, 130, 110, 22, "Internal → 500", "b", { size: 9 }), note("n", 270, 85, "код: not_found,\nconflict,\ninvalid, internal", "m")],
    [rs("c", 10, 20, ["async fn show(..) -> Result<Json<Room>, AppError> {", "    let room = find(id).await?;", "    Ok(Json(room))", "}"], [0, 1], { ...code, lh: 24, size: 8.5 })],
  ],
});

// 8. В ответ
export const V08 = scene({
  labels: ["IntoResponse", "Безопасность", "Один разбор"],
  caption: [
    "Статус по варианту, тело одинакового формата: код, сообщение, поля",
    "Внутренние детали — в журнал; клиенту — общее сообщение",
    "Клиент разбирает все ошибки одним кодом",
  ],
  frames: [
    [rs("c", 10, 14, ["impl IntoResponse for AppError {", "    fn into_response(self) -> Response {", "        let (status, code) = self.parts();", "        (status, Json(body(code, &self))).into_response()", "    }", "}"], [2, 3], { ...code, lh: 17, size: 8.5 })],
    [Box("a", 90, 55, 130, 26, "sqlx: UNIQUE failed...", "r", { size: 9 }), arrow("e1", 156, 55, 214, 55, "m"), Box("b", 290, 55, 110, 26, "журнал", "b", { size: 10 }), Box("c", 90, 105, 130, 26, "клиенту: internal", "g", { size: 9.5 }), arrow("e2", 156, 105, 214, 105, "m"), Box("d", 290, 105, 110, 26, "общее сообщение", "g", { size: 9 })],
    [rs("c", 10, 20, ["{ \"error\": {", "    \"code\": \"invalid\",", "    \"message\": \"данные не годятся\",", "    \"fields\": [{\"name\": \"user\", \"why\": \"короткое\"}]", "} }"], [1, 3], { ...code, lh: 22, size: 8.5 })],
  ],
});

// 9. Оператор ?
export const V09 = scene({
  labels: ["From", "База → ошибка", "Линейный код"],
  caption: [
    "Оператор ? вызывает From: ошибка библиотеки становится AppError",
    "Нет строки — не найдено, нарушена уникальность — конфликт, остальное — внутренняя",
    "Запросили, получили, вернули: без вложенных проверок",
  ],
  frames: [
    [rs("c", 10, 20, ["impl From<sqlx::Error> for AppError {", "    fn from(e: sqlx::Error) -> Self { .. }", "}", "let row = query.fetch_one(&pool).await?;"], [3], { ...code, lh: 24, size: 9 })],
    [Box("a", 80, 40, 130, 24, "RowNotFound", "b", { size: 10 }), arrow("e1", 146, 40, 194, 40, "m"), Box("b", 280, 40, 120, 24, "NotFound", "g", { size: 10 }), Box("c", 80, 80, 130, 24, "UNIQUE violation", "b", { size: 10 }), arrow("e2", 146, 80, 194, 80, "m"), Box("d", 280, 80, 120, 24, "Conflict", "g", { size: 10 }), Box("e", 80, 120, 130, 24, "всё остальное", "b", { size: 10 }), arrow("e3", 146, 120, 194, 120, "m"), Box("f", 280, 120, 120, 24, "Internal", "g", { size: 10 })],
    [rs("c", 10, 20, ["let room = find(&pool, id).await?;", "let user = load_user(&pool, uid).await?;", "Ok(Json(Out::from((room, user))))"], [0, 1, 2], { ...code, lh: 28, size: 9 })],
  ],
});

// 10. Формат ошибки
export const V10 = scene({
  labels: ["Контракт", "Машинный код", "Везде одинаково"],
  caption: [
    "Формат ошибок — такая же часть API, как формат успешных ответов",
    "Код стабилен — по нему выбирают поведение; сообщение можно менять и переводить",
    "Даже ошибки каркаса — неизвестный путь, метод, большое тело — в том же формате",
  ],
  frames: [
    [Box("a", 90, 70, 130, 36, "успешный ответ", "g", { size: 10 }), Box("b", 270, 70, 130, 36, "ошибка", "g", { size: 10 }), note("n", 180, 125, "оба — контракт", "m")],
    [Box("a", 90, 60, 130, 26, "\"code\": \"conflict\"", "g", { size: 9.5 }), note("n1", 270, 60, "для программы", "m"), Box("b", 90, 110, 130, 26, "\"message\": \"имя занято\"", "b", { size: 9 }), note("n2", 270, 110, "для человека", "m")],
    [Box("a", 70, 40, 100, 24, "404 путь", "y", { size: 10 }), Box("b", 180, 40, 100, 24, "405 метод", "y", { size: 10 }), Box("c", 290, 40, 100, 24, "413 тело", "y", { size: 10 }), arrow("e1", 70, 54, 160, 96, "m"), arrow("e2", 180, 54, 180, 96, "m"), arrow("e3", 290, 54, 200, 96, "m"), Box("d", 180, 110, 150, 26, "{\"error\": { .. }}", "g", { size: 10 })],
  ],
});

// 11. DTO
export const V11 = scene({
  labels: ["Три структуры", "Не показывать лишнее", "Преобразования"],
  caption: [
    "Запрос, ответ и строка базы — разные типы с разным составом полей",
    "Хеш пароля есть в строке, но в ответ он попасть не может",
    "Преобразования между слоями — From или простая функция",
  ],
  frames: [
    [Box("a", 70, 70, 90, 36, "CreateRoom\n{ name }", "b", { size: 9 }), Box("b", 180, 70, 90, 36, "RoomRow\n{ id, name,\ncreated }", "g", { size: 8.5 }), Box("c", 290, 70, 90, 36, "RoomOut\n{ id, name }", "b", { size: 9 })],
    [Box("a", 90, 60, 150, 26, "UserRow: pass_hash", "r", { size: 9.5 }), arrow("e", 166, 60, 214, 60, "r"), Box("b", 290, 60, 110, 26, "UserOut: нет", "g", { size: 9.5 }), note("n", 180, 110, "лишнего поля нет в типе ответа", "m")],
    [rs("c", 10, 20, ["impl From<RoomRow> for RoomOut {", "    fn from(r: RoomRow) -> Self {", "        RoomOut { id: r.id, name: r.name }", "    }", "}"], [2], { ...code, lh: 22, size: 9 })],
  ],
});

// 12. Эволюция API
export const V12 = scene({
  labels: ["Добавлять можно", "Переименовать", "Присутствие поля"],
  caption: [
    "Новые поля в ответах — свободно; в запросах — необязательные",
    "alias: принимаем старое и новое имя, отдаём новое; потом убираем старое",
    "PATCH: поля нет, null и значение — три разных намерения",
  ],
  frames: [
    [Box("a", 90, 60, 130, 26, "ответ + новое поле", "g", { size: 9.5 }), note("n1", 270, 60, "клиенты игнорируют", "m"), Box("b", 90, 110, 130, 26, "запрос + Option", "g", { size: 9.5 }), note("n2", 270, 110, "старые не ломаются", "m")],
    [rs("c", 10, 20, ["#[serde(alias = \"room\")]", "room_id: u32,", "// принимает {\"room\": 1} и {\"room_id\": 1}"], [0, 2], { ...code, lh: 28, size: 9 })],
    [Box("a", 70, 40, 110, 24, "{}", "b", { size: 10.5 }), note("n1", 240, 40, "не трогать", "m"), Box("b", 70, 80, 110, 24, "{\"x\": null}", "y", { size: 10 }), note("n2", 240, 80, "очистить", "m"), Box("c", 70, 120, 110, 24, "{\"x\": 5}", "g", { size: 10 }), note("n3", 240, 120, "записать 5", "m")],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Типы на границе", "Единая ошибка", "Дальше"],
  caption: [
    "serde и атрибуты задают контракт; валидация один раз — в типы с гарантиями",
    "AppError → IntoResponse, From для ошибок, один формат, подробности — в журнал",
    "Следующая глава: подключаем PostgreSQL через sqlx",
  ],
  frames: [
    [Box("a", 70, 70, 100, 30, "serde", "g", { size: 11 }), Box("b", 180, 70, 100, 30, "атрибуты", "g", { size: 10.5 }), Box("c", 290, 70, 100, 30, "типы-гарантии", "g", { size: 9.5 })],
    [Box("a", 70, 70, 100, 30, "AppError", "g", { size: 11 }), Box("b", 180, 70, 100, 30, "IntoResponse", "g", { size: 10 }), Box("c", 290, 70, 100, 30, "From + ?", "g", { size: 11 })],
    [Box("a", 90, 70, 130, 30, "sqlx", "b", { size: 11 }), Box("b", 250, 70, 130, 30, "пул и запросы", "b", { size: 10 }), Box("c", 340, 70, 40, 30, "→", "y", { size: 12 })],
  ],
});
