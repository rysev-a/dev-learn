import { scene } from "./alg.tsx";
import { Box, arrow, note, rs } from "./rs.tsx";

/* Глава 44 книги «Изучаем Rust»: axum — маршруты, обработчики и экстракторы. */

const code = { w: 340, size: 9.5, lh: 14 };

// 1. Чат на Rust
export const V01 = scene({
  labels: ["Что строим", "Стек", "Слой за слоем"],
  caption: [
    "Чат: пользователи, комнаты, история сообщений и живая доставка по веб-сокетам",
    "tokio — рантайм, axum — каркас, sqlx — база, serde — формат данных",
    "Главы 44–51 добавляют по слою; в конце — запускаемый сервис с тестами",
  ],
  frames: [
    [Box("a", 70, 50, 100, 28, "пользователи", "b", { size: 10 }), Box("b", 180, 50, 100, 28, "комнаты", "b", { size: 10 }), Box("c", 290, 50, 100, 28, "сообщения", "b", { size: 10 }), Box("d", 180, 110, 140, 28, "веб-сокеты", "g", { size: 10.5 }), arrow("e1", 120, 64, 150, 98, "m"), arrow("e2", 180, 64, 180, 96, "m"), arrow("e3", 240, 64, 212, 98, "m")],
    [Box("a", 70, 40, 100, 26, "tokio", "g", { size: 10.5 }), Box("b", 180, 40, 100, 26, "axum", "g", { size: 10.5 }), Box("c", 290, 40, 100, 26, "sqlx", "g", { size: 10.5 }), Box("d", 125, 110, 100, 26, "serde", "b", { size: 10.5 }), Box("e", 235, 110, 100, 26, "tower", "b", { size: 10.5 })],
    [Box("a", 50, 70, 70, 30, "каркас", "g", { size: 10 }), arrow("e1", 86, 70, 110, 70, "m"), Box("b", 140, 70, 62, 30, "слои", "g", { size: 10 }), arrow("e2", 172, 70, 196, 70, "m"), Box("c", 222, 70, 50, 30, "база", "g", { size: 10 }), arrow("e3", 248, 70, 256, 70, "m"), Box("d", 288, 70, 60, 30, "сокеты", "g", { size: 9.5 }), Box("e", 341, 70, 34, 30, "✓", "y", { size: 11 })],
  ],
});

// 2. Устройство axum
export const V02 = scene({
  labels: ["Тонкий слой", "Service", "Всё из tower"],
  caption: [
    "hyper разбирает протокол, tower задаёт интерфейс службы, axum даёт удобную обёртку",
    "Service: запрос → асинхронный ответ; Router сам реализует этот интерфейс",
    "Слои, таймауты и ограничения нагрузки подходят и роутеру, и обработчику",
  ],
  frames: [
    [Box("a", 180, 140, 140, 24, "hyper — HTTP", "b", { size: 10 }), Box("b", 180, 100, 140, 24, "tower — Service", "b", { size: 10 }), Box("c", 180, 60, 140, 24, "axum — Router", "g", { size: 10 }), Box("d", 180, 20, 140, 22, "ваш код", "y", { size: 10 })],
    [rs("c", 10, 20, ["trait Service<Request> {", "    type Response;", "    fn call(&mut self, req: Request)", "        -> Future<Output = Response>;", "}"], [2, 3], { ...code, lh: 22, size: 9.5 })],
    [Box("a", 60, 70, 80, 28, "Router", "g", { size: 10 }), arrow("e1", 100, 70, 130, 70, "m"), Box("b", 180, 70, 80, 28, "слой", "b", { size: 10 }), arrow("e2", 220, 70, 250, 70, "m"), Box("c", 300, 70, 80, 28, "таймаут", "b", { size: 10 }), note("n", 180, 120, "один и тот же интерфейс на всех уровнях", "m")],
  ],
});

// 3. Маршруты
export const V03 = scene({
  labels: ["route + метод", "Параметры", "405 и 404"],
  caption: [
    "route связывает путь с методами; несколько методов цепляются друг за другом",
    "{id} — один сегмент, {*rest} — остаток пути",
    "Путь есть, метода нет — 405; пути нет — 404 или свой fallback",
  ],
  frames: [
    [rs("c", 10, 20, ["let app = Router::new()", "    .route(\"/rooms\", get(list).post(create))", "    .route(\"/rooms/{id}\", get(show).delete(remove));"], [1, 2], { ...code, lh: 26, size: 8.5 })],
    [rs("c", 10, 20, ["\"/rooms/{id}\"        → id = \"7\"", "\"/files/{*rest}\"      → rest = \"a/b/c.txt\"", "\"/rooms/{room}/msgs/{n}\" → два параметра"], [0, 1, 2], { ...code, lh: 28, size: 9 })],
    [Box("a", 70, 40, 110, 26, "PUT /rooms → 405", "y", { size: 9.5 }), Box("b", 70, 80, 110, 26, "GET /nope → 404", "r", { size: 9.5 }), Box("c", 70, 120, 110, 26, "GET /rooms → 200", "g", { size: 9.5 }), note("n", 270, 80, "заголовок Allow:\nGET, POST", "m")],
  ],
});

// 4. Обработчики
export const V04 = scene({
  labels: ["async fn", "Что проверяет компилятор", "Ответ"],
  caption: [
    "Аргументы — экстракторы, результат — всё, что умеет превращаться в ответ",
    "Аргументы — экстракторы; Future — Send; результат — IntoResponse",
    "Нарушено любое условие — ошибка «Handler не реализован»",
  ],
  frames: [
    [rs("c", 10, 20, ["async fn show(Path(id): Path<u32>) -> String {", "    format!(\"комната {id}\")", "}"], [0, 1], { ...code, lh: 28, size: 9 })],
    [Box("a", 70, 40, 110, 26, "экстракторы", "b", { size: 10 }), Box("b", 70, 80, 110, 26, "Future: Send", "b", { size: 10 }), Box("c", 70, 120, 110, 26, "IntoResponse", "b", { size: 10 }), arrow("e1", 126, 40, 214, 76, "m"), arrow("e2", 126, 80, 214, 80, "m"), arrow("e3", 126, 120, 214, 84, "m"), Box("d", 280, 80, 90, 30, "Handler ✓", "g", { size: 10 })],
    [Box("a", 90, 80, 130, 30, "что-то не так", "y", { size: 10 }), arrow("e", 156, 80, 208, 80, "m"), Box("b", 290, 80, 130, 40, "the trait Handler\nis not implemented", "r", { size: 9 })],
  ],
});

// 5. Экстракторы
export const V05 = scene({
  labels: ["Каталог", "Два вида", "Отказ"],
  caption: [
    "Path, Query, Json, State, HeaderMap, Extension, Request",
    "Читают только заголовки и адрес — в любом порядке; читают тело — только последним",
    "Экстрактор не справился — обработчик не вызывается, клиент получает 4xx",
  ],
  frames: [
    [Box("a", 70, 40, 100, 24, "Path<T>", "b", { size: 10 }), Box("b", 180, 40, 100, 24, "Query<T>", "b", { size: 10 }), Box("c", 290, 40, 100, 24, "Json<T>", "b", { size: 10 }), Box("d", 70, 90, 100, 24, "State<S>", "b", { size: 10 }), Box("e", 180, 90, 100, 24, "HeaderMap", "b", { size: 10 }), Box("f", 290, 90, 100, 24, "Request", "b", { size: 10 }), note("n", 180, 140, "FromRequestParts и FromRequest", "m")],
    [rs("c", 10, 20, ["async fn h(", "    Path(id): Path<u32>,     // не трогает тело", "    State(s): State<App>,    // не трогает тело", "    Json(m): Json<Msg>,      // тело — последним", ") -> StatusCode", ], [3], { ...code, lh: 22, size: 9 })],
    [Box("a", 70, 70, 100, 28, "запрос", "b", { size: 10 }), arrow("e1", 120, 70, 144, 70, "m"), Box("b", 180, 70, 70, 28, "Json", "y", { size: 10.5 }), arrow("e2", 216, 70, 242, 70, "r"), Box("c", 300, 70, 100, 28, "400 / 422", "r", { size: 10 }), note("n", 180, 120, "обработчик не вызван", "r")],
  ],
});

// 6. Path и Query
export const V06 = scene({
  labels: ["Path", "Query", "Ошибки"],
  caption: [
    "Один тип, кортеж или структура: serde разбирает сегменты по именам",
    "Структура с Option и значениями по умолчанию описывает допустимые поля",
    "Не число там, где ждали число — 400 с текстом причины",
  ],
  frames: [
    [rs("c", 10, 20, ["Path(id): Path<u32>", "Path((room, n)): Path<(u32, u32)>", "Path(p): Path<Params>  // struct { room, n }"], [0, 1, 2], { ...code, lh: 28, size: 9 })],
    [rs("c", 10, 14, ["#[derive(Deserialize)]", "struct Page {", "    #[serde(default = \"ten\")] limit: u32,", "    before: Option<u64>,", "}", "// GET /msgs?limit=5&before=100"], [2, 3], { ...code, lh: 16, size: 9 })],
    [Box("a", 80, 50, 130, 26, "/rooms/abc", "y", { size: 10 }), arrow("e1", 146, 50, 214, 50, "m"), Box("b", 290, 50, 120, 26, "400 Bad Request", "r", { size: 10 }), Box("c", 80, 110, 130, 26, "/msgs?limit=x", "y", { size: 10 }), arrow("e2", 146, 110, 214, 110, "m"), Box("d", 290, 110, 120, 26, "400 Bad Request", "r", { size: 10 })],
  ],
});

// 7. Ответы
export const V07 = scene({
  labels: ["IntoResponse", "Кортежи", "Result"],
  caption: [
    "Строки, байты, StatusCode, Json, Html, Redirect — всё превращается в Response",
    "(StatusCode, T) и (StatusCode, заголовки, T) собирают ответ целиком",
    "Result<T, E>: и Ok, и Err должны уметь стать ответом — основа обработки ошибок",
  ],
  frames: [
    [rs("c", 10, 20, ["\"ok\"                       // 200, text/plain", "Json(room)                // 200, application/json", "StatusCode::NO_CONTENT    // 204, пустое тело", "Redirect::to(\"/rooms\")     // 303"], [0, 1, 2, 3], { ...code, lh: 24, size: 8.5 })],
    [rs("c", 10, 20, ["(StatusCode::CREATED, Json(room))", "(StatusCode::CREATED,", " [(LOCATION, \"/rooms/7\")],", " Json(room))"], [0, 1, 2, 3], { ...code, lh: 24, size: 9.5 })],
    [rs("c", 10, 20, ["async fn show(..) -> Result<Json<Room>, AppError> {", "    let room = find(id).ok_or(AppError::NotFound)?;", "    Ok(Json(room))", "}"], [0, 1], { ...code, lh: 24, size: 8.5 })],
  ],
});

// 8. Статусы и заголовки
export const V08 = scene({
  labels: ["2xx", "4xx", "Автоматика"],
  caption: [
    "200 — с телом, 201 — создано (Location), 204 — успех без тела",
    "404 — нет ресурса, 409 — конфликт, 422 — данные не годятся",
    "HEAD обрабатывается через GET без тела; неподходящий метод — 405",
  ],
  frames: [
    [Box("a", 70, 40, 100, 24, "200 OK", "g", { size: 10 }), Box("b", 180, 40, 100, 24, "201 Created", "g", { size: 10 }), Box("c", 290, 40, 100, 24, "204 No Content", "g", { size: 9.5 }), note("n", 180, 100, "201 + Location: /rooms/7", "m"), note("m", 290, 100, "после удаления", "m")],
    [Box("a", 70, 40, 100, 24, "404 нет", "y", { size: 10 }), Box("b", 180, 40, 100, 24, "409 конфликт", "y", { size: 10 }), Box("c", 290, 40, 100, 24, "422 не годится", "y", { size: 9.5 }), note("n", 70, 90, "комнаты нет", "m"), note("m", 180, 90, "имя занято", "m"), note("k", 290, 90, "пароль слишком короткий", "m")],
    [Box("a", 90, 50, 130, 26, "HEAD /rooms", "b", { size: 10 }), arrow("e1", 156, 50, 214, 50, "m"), Box("b", 290, 50, 120, 26, "как GET, без тела", "g", { size: 9.5 }), Box("c", 90, 110, 130, 26, "PATCH /rooms", "b", { size: 10 }), arrow("e2", 156, 110, 214, 110, "m"), Box("d", 290, 110, 120, 26, "405 + Allow", "y", { size: 10 })],
  ],
});

// 9. nest и merge
export const V09 = scene({
  labels: ["Модули", "nest", "merge и fallback"],
  caption: [
    "Каждый модуль возвращает свой Router: пользователи, комнаты, сообщения",
    "nest монтирует под префикс; внутри пути пишутся от корня модуля",
    "merge склеивает роутеры на одном уровне; fallback отвечает на неизвестное",
  ],
  frames: [
    [Box("r", 180, 30, 120, 26, "app()", "g", { size: 10.5 }), Box("a", 70, 100, 100, 26, "users()", "b", { size: 10 }), Box("b", 180, 100, 100, 26, "rooms()", "b", { size: 10 }), Box("c", 290, 100, 100, 26, "messages()", "b", { size: 10 }), arrow("e1", 150, 44, 100, 88, "m"), arrow("e2", 180, 44, 180, 88, "m"), arrow("e3", 210, 44, 260, 88, "m")],
    [rs("c", 10, 20, ["Router::new()", "    .nest(\"/api/rooms\", rooms())", "    .nest(\"/api/users\", users())", "// внутри rooms(): route(\"/{id}\", ..) → /api/rooms/{id}"], [1, 2], { ...code, lh: 24, size: 8.5 })],
    [rs("c", 10, 20, ["Router::new()", "    .merge(health())", "    .nest(\"/api\", api())", "    .fallback(not_found)"], [1, 3], { ...code, lh: 26, size: 10 })],
  ],
});

// 10. Запуск сервера
export const V10 = scene({
  labels: ["Три строки", "Порт 0", "Сервер — задача"],
  caption: [
    "Привязать сокет, передать в serve вместе с роутером, ждать",
    "Порт 0 — система выбирает свободный; адрес спрашиваем у сокета",
    "Каждое соединение обслуживает своя задача tokio",
  ],
  frames: [
    [rs("c", 10, 20, ["let listener = TcpListener::bind(\"0.0.0.0:3000\")", "    .await?;", "axum::serve(listener, app).await?;"], [0, 2], { ...code, lh: 28, size: 9 })],
    [rs("c", 10, 20, ["let l = TcpListener::bind(\"127.0.0.1:0\").await?;", "let addr = l.local_addr()?;  // 127.0.0.1:54321", "tokio::spawn(axum::serve(l, app).into_future());"], [1], { ...code, lh: 28, size: 8.5 })],
    [Box("s", 70, 70, 80, 28, "serve", "g", { size: 10.5 }), arrow("e1", 110, 62, 150, 40, "m"), arrow("e2", 110, 70, 150, 70, "m"), arrow("e3", 110, 78, 150, 100, "m"), Box("a", 190, 40, 80, 22, "соед. 1", "b", { size: 9.5 }), Box("b", 190, 70, 80, 22, "соед. 2", "b", { size: 9.5 }), Box("c", 190, 100, 80, 22, "соед. 3", "b", { size: 9.5 }), note("n", 300, 70, "по задаче\nна соединение", "m")],
  ],
});

// 11. Тест без сети
export const V11 = scene({
  labels: ["oneshot", "Запрос и тело", "Без портов"],
  caption: [
    "ServiceExt::oneshot отправляет запрос в роутер в памяти",
    "Request::builder собирает запрос, to_bytes читает тело ответа",
    "Быстро и стабильно, а запрос проходит те же маршруты, экстракторы и слои",
  ],
  frames: [
    [rs("c", 10, 20, ["use tower::ServiceExt;", "let res = app.clone().oneshot(req).await.unwrap();", "assert_eq!(res.status(), StatusCode::OK);"], [1, 2], { ...code, lh: 28, size: 8.5 })],
    [rs("c", 10, 20, ["let req = Request::get(\"/health\").body(Body::empty())?;", "let bytes = to_bytes(res.into_body(), 1 << 20).await?;", "assert_eq!(&bytes[..], b\"ok\");"], [0, 1, 2], { ...code, lh: 28, size: 8 })],
    [Box("a", 70, 70, 100, 30, "тест", "b", { size: 10 }), arrow("e", 120, 70, 156, 70, "g"), Box("b", 220, 70, 110, 30, "Router (память)", "g", { size: 9.5 }), note("n", 180, 120, "ни сокета, ни порта, ни гонок", "m")],
  ],
});

// 12. Типичные ошибки
export const V12 = scene({
  labels: ["Handler не реализован", "Причины", "debug_handler"],
  caption: [
    "Самая длинная ошибка axum: функция не подходит под Handler",
    "Не Send, тело не последним, нет with_state, экстрактор не подходит",
    "#[debug_handler] называет проблемный аргумент",
  ],
  frames: [
    [rs("c", 10, 14, ["error[E0277]: the trait bound", "  `fn(State<Pool>) -> .. {list}: Handler<_, _>`", "  is not satisfied"], [0, 1, 2], { ...code, lh: 24, size: 9, bad: [0, 1, 2] })],
    [Box("a", 93, 30, 156, 22, "значение не Send через .await", "y", { size: 9 }), Box("b", 90, 62, 150, 22, "Json не последним", "y", { size: 9 }), Box("c", 90, 94, 150, 22, "забыли .with_state(..)", "y", { size: 9 }), Box("d", 90, 126, 150, 22, "тип не FromRequest", "y", { size: 9 }), note("n", 280, 80, "четыре\nпричины", "m")],
    [rs("c", 10, 20, ["#[axum::debug_handler]", "async fn create(Json(m): Json<Msg>, State(s): State<App>) {", "    // ошибка: Json должен быть последним", "}"], [0, 2], { ...code, lh: 26, size: 8.5 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Роутер и обработчик", "Ответы и тесты", "Дальше"],
  caption: [
    "Router — Service; обработчик — async fn с экстракторами; тело читается один раз",
    "Ответ — IntoResponse; модули собираются nest и merge; проверка — oneshot",
    "Следующая глава: общее состояние приложения и слои tower",
  ],
  frames: [
    [Box("a", 90, 70, 130, 30, "Router = Service", "g", { size: 10.5 }), Box("b", 270, 70, 130, 30, "handler + экстракторы", "g", { size: 9.5 })],
    [Box("a", 70, 70, 100, 30, "IntoResponse", "g", { size: 10 }), Box("b", 180, 70, 100, 30, "nest / merge", "g", { size: 10 }), Box("c", 290, 70, 100, 30, "oneshot", "g", { size: 10.5 })],
    [Box("a", 80, 70, 110, 30, "State", "b", { size: 11 }), Box("b", 200, 70, 110, 30, "tower layers", "b", { size: 10.5 }), arrow("e1", 134, 70, 146, 70, "m"), Box("c", 320, 70, 80, 30, "глава 45", "y", { size: 10 })],
  ],
});
