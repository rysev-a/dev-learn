import { scene } from "./alg.tsx";
import { Box, arrow, note, rs } from "./rs.tsx";

/* Глава 45 книги «Изучаем Rust»: состояние приложения и слои tower. */

const code = { w: 340, size: 9.5, lh: 14 };

// 1. Общее состояние
export const V01 = scene({
  labels: ["Общее", "Сквозное", "Два инструмента"],
  caption: [
    "Настройки, пул базы, список подключений, счётчики — нужны всем обработчикам",
    "Авторизация, время, лимиты, номер запроса — относятся ко всем маршрутам сразу",
    "Первое решает состояние приложения, второе — слои",
  ],
  frames: [
    [Box("s", 180, 40, 150, 28, "общее состояние", "g", { size: 10.5 }), Box("a", 70, 110, 80, 26, "обработчик", "b", { size: 9 }), Box("b", 180, 110, 80, 26, "обработчик", "b", { size: 9 }), Box("c", 290, 110, 80, 26, "обработчик", "b", { size: 9 }), arrow("e1", 150, 54, 90, 98, "m"), arrow("e2", 180, 54, 180, 98, "m"), arrow("e3", 210, 54, 270, 98, "m")],
    [Box("a", 60, 70, 76, 28, "авторизация", "y", { size: 9 }), Box("b", 150, 70, 76, 28, "время", "y", { size: 9.5 }), Box("c", 240, 70, 76, 28, "лимиты", "y", { size: 9.5 }), Box("d", 320, 70, 56, 28, "id", "y", { size: 10 }), note("n", 180, 120, "для всех маршрутов", "m")],
    [Box("a", 100, 70, 130, 36, "State\n(данные)", "g", { size: 10 }), Box("b", 260, 70, 130, 36, "Layer\n(логика вокруг)", "g", { size: 10 })],
  ],
});

// 2. State
export const V02 = scene({
  labels: ["with_state", "Клон на запрос", "Тип проверяется"],
  caption: [
    "Роутеру передают значение, обработчик запрашивает State<T>",
    "Клонируется Arc — счётчик ссылок; данные остаются общими",
    "Не тот тип состояния — программа не соберётся",
  ],
  frames: [
    [rs("c", 10, 20, ["#[derive(Clone)]", "struct App { rooms: Arc<RwLock<Vec<Room>>> }", "", "Router::new().route(\"/rooms\", get(list)).with_state(app)", "async fn list(State(app): State<App>) -> ..."], [3, 4], { ...code, lh: 22, size: 8.5 })],
    [Box("a", 70, 40, 80, 24, "запрос 1", "b", { size: 9.5 }), Box("b", 70, 80, 80, 24, "запрос 2", "b", { size: 9.5 }), Box("c", 70, 120, 80, 24, "запрос 3", "b", { size: 9.5 }), Box("d", 270, 80, 100, 30, "Arc: данные", "g", { size: 10 }), arrow("e1", 110, 40, 220, 72, "m"), arrow("e2", 110, 80, 220, 80, "m"), arrow("e3", 110, 120, 220, 88, "m")],
    [Box("a", 90, 60, 140, 26, "with_state(Db)", "b", { size: 10 }), Box("b", 90, 110, 140, 26, "State<Config>", "b", { size: 10 }), arrow("e", 160, 60, 160, 98, "r"), Box("c", 290, 85, 110, 36, "ошибка\nкомпиляции", "r", { size: 9.5 })],
  ],
});

// 3. Что хранить
export const V03 = scene({
  labels: ["Атомики", "RwLock и Mutex", "До await"],
  caption: [
    "Счётчикам хватает AtomicUsize: блокировок нет",
    "Читают часто — RwLock; меняют коротко — Mutex",
    "std::sync::Mutex через .await не держим: берём в блоке и отпускаем",
  ],
  frames: [
    [rs("c", 10, 20, ["hits: Arc<AtomicUsize>", "hits.fetch_add(1, Ordering::Relaxed);"], [1], { ...code, lh: 30, size: 10 })],
    [Box("a", 90, 60, 140, 28, "RwLock<Config>", "b", { size: 10.5 }), note("n", 270, 60, "читают часто,\nменяют редко", "m"), Box("b", 90, 110, 140, 28, "Mutex<Vec<Msg>>", "b", { size: 10.5 }), note("m", 270, 110, "короткие\nизменения", "m")],
    [rs("c", 10, 20, ["let n = {", "    let mut g = state.count.lock().unwrap();", "    *g += 1; *g", "};                       // блокировка отпущена", "sleep(..).await;"], [3, 4], { ...code, lh: 22, size: 9 })],
  ],
});

// 4. Каналы
export const V04 = scene({
  labels: ["broadcast", "mpsc", "Слабая связь"],
  caption: [
    "Обработчик публикует событие, подписчики получают его все",
    "Обработчик отдаёт работу фоновой задаче через очередь",
    "Обработчик не знает, кто и как обработает: он только публикует",
  ],
  frames: [
    [Box("h", 70, 70, 90, 30, "обработчик", "b", { size: 10 }), arrow("e0", 116, 70, 160, 70, "g"), Box("c", 180, 70, 50, 30, "bcast", "g", { size: 9.5 }), arrow("e1", 206, 62, 256, 40, "m"), arrow("e2", 206, 70, 256, 70, "m"), arrow("e3", 206, 78, 256, 100, "m"), Box("a", 300, 40, 70, 22, "клиент 1", "b", { size: 9 }), Box("b", 300, 70, 70, 22, "клиент 2", "b", { size: 9 }), Box("d", 300, 100, 70, 22, "клиент 3", "b", { size: 9 })],
    [Box("h", 70, 70, 90, 30, "обработчик", "b", { size: 10 }), arrow("e0", 116, 70, 170, 70, "g"), Box("q", 200, 70, 70, 30, "очередь", "g", { size: 9.5 }), arrow("e1", 236, 70, 276, 70, "g"), Box("w", 320, 70, 80, 30, "фоновая\nзадача", "b", { size: 9 })],
    [rs("c", 10, 20, ["state.events.send(Event::Message(msg));", "// кто подписан — не наша забота"], [0], { ...code, lh: 30, size: 10 })],
  ],
});

// 5. FromRef
export const V05 = scene({
  labels: ["Узкое окно", "FromRef", "Тесты проще"],
  caption: [
    "Обработчику нужен конфиг, а не всё приложение",
    "FromRef достаёт клон нужного поля из состояния",
    "В тесте подставляется только нужная часть",
  ],
  frames: [
    [Box("a", 90, 70, 130, 70, "AppState\nconfig\npool\nhub", "g", { size: 9.5 }), arrow("e", 156, 70, 218, 70, "m"), Box("b", 290, 70, 110, 30, "State<Config>", "b", { size: 10 })],
    [rs("c", 10, 20, ["impl FromRef<AppState> for Config {", "    fn from_ref(s: &AppState) -> Config {", "        s.config.clone()", "    }", "}"], [1, 2], { ...code, lh: 22, size: 9 })],
    [Box("a", 90, 60, 130, 26, "handler(State<Config>)", "g", { size: 9 }), Box("b", 90, 110, 130, 26, "тест: Config::test()", "b", { size: 9.5 }), arrow("e", 160, 98, 160, 74, "g"), note("n", 290, 85, "без пула\nи без хаба", "m")],
  ],
});

// 6. State и Extension
export const V06 = scene({
  labels: ["State", "Extension", "Что куда"],
  caption: [
    "Известно при сборке роутера; проверяется компилятором",
    "Кладётся в запрос на лету; достаётся экстрактором Extension<T>",
    "Постоянное — в State, данные запроса — в Extension",
  ],
  frames: [
    [Box("a", 90, 70, 130, 30, "with_state(app)", "g", { size: 10 }), arrow("e", 156, 70, 214, 70, "g"), Box("b", 290, 70, 130, 30, "проверка при сборке", "b", { size: 9.5 })],
    [Box("a", 70, 40, 100, 26, "слой auth", "b", { size: 10 }), arrow("e1", 120, 40, 164, 40, "g"), Box("b", 210, 40, 100, 26, "req.extensions", "g", { size: 9.5 }), arrow("e2", 260, 54, 260, 96, "g"), Box("c", 260, 110, 130, 26, "Extension<UserId>", "b", { size: 9.5 }), note("n", 80, 110, "нет слоя → 500", "r")],
    [Box("a", 90, 50, 130, 26, "пул, конфиг, hub", "g", { size: 9.5 }), Box("b", 270, 50, 110, 26, "State", "b", { size: 10.5 }), arrow("e1", 156, 50, 214, 50, "m"), Box("c", 90, 110, 130, 26, "кто пришёл, id запроса", "y", { size: 9 }), Box("d", 270, 110, 110, 26, "Extension", "b", { size: 10.5 }), arrow("e2", 156, 110, 214, 110, "m")],
  ],
});

// 7. Слои tower
export const V07 = scene({
  labels: ["Layer", "Матрёшка", "ServiceBuilder"],
  caption: [
    "Layer берёт службу и возвращает новую — с логикой вокруг вызова",
    "Внешний видит запрос первым, а ответ получает последним",
    "ServiceBuilder перечисляет слои сверху вниз — в порядке выполнения",
  ],
  frames: [
    [rs("c", 10, 20, ["trait Layer<S> {", "    type Service;", "    fn layer(&self, inner: S) -> Self::Service;", "}"], [2], { ...code, lh: 24, size: 9.5 })],
    [Box("a", 180, 85, 170, 130, "", "b"), Box("b", 180, 85, 120, 90, "", "g"), Box("c", 180, 85, 70, 40, "handler", "y", { size: 9 }), note("n1", 180, 30, "слой 1", "m"), note("n2", 180, 52, "слой 2", "m"), arrow("e", 60, 85, 120, 85, "g")],
    [rs("c", 10, 20, ["ServiceBuilder::new()", "    .layer(TraceLayer::new_for_http())   // снаружи", "    .layer(TimeoutLayer::new(secs))      // внутри", "    .service(handler)"], [1, 2], { ...code, lh: 24, size: 8.5 })],
  ],
});

// 8. from_fn
export const V08 = scene({
  labels: ["Функция-слой", "До и после", "С состоянием"],
  caption: [
    "async fn(req, next) -> Response вместо ручной реализации Service",
    "До next меняем запрос или отвечаем сами, после — меняем ответ",
    "from_fn_with_state даёт доступ к общему состоянию",
  ],
  frames: [
    [rs("c", 10, 20, ["async fn mw(req: Request, next: Next) -> Response {", "    let res = next.run(req).await;", "    res", "}", "app.layer(middleware::from_fn(mw))"], [0, 4], { ...code, lh: 22, size: 9 })],
    [rs("c", 10, 14, ["async fn auth(req: Request, next: Next) -> Response {", "    if req.headers().get(AUTHORIZATION).is_none() {", "        return StatusCode::UNAUTHORIZED.into_response();", "    }", "    let mut res = next.run(req).await;", "    res.headers_mut().insert(\"x-done\", \"1\".parse().unwrap());", "    res", "}"], [1, 2, 5], { ...code, lh: 16, size: 8 })],
    [rs("c", 10, 20, ["app.layer(middleware::from_fn_with_state(", "    state.clone(), count));", "", "async fn count(State(s): State<App>,", "               req: Request, next: Next) -> Response"], [0, 1, 3], { ...code, lh: 22, size: 9 })],
  ],
});

// 9. Порядок слоёв
export const V09 = scene({
  labels: ["layer — последний снаружи", "route_layer", "ServiceBuilder — наоборот"],
  caption: [
    "Router::layer оборачивает всё добавленное до него: последний видит запрос первым",
    "route_layer не затрагивает запросы к несуществующим путям — они идут мимо слоя",
    "В ServiceBuilder первым перечисленный слой — самый внешний",
  ],
  frames: [
    [rs("c", 10, 20, ["Router::new()", "    .route(\"/x\", get(h))", "    .layer(A)      // внутри", "    .layer(B)      // снаружи: B → A → h"], [2, 3], { ...code, lh: 26, size: 9.5 })],
    [Box("a", 80, 40, 120, 26, "GET /x  → слой → h", "g", { size: 9 }), Box("b", 80, 90, 120, 26, "GET /zzz → 404", "y", { size: 9.5 }), note("n", 270, 40, "с route_layer —\nсо слоем", "m"), note("m", 270, 90, "layer — со слоем,\nroute_layer — без", "m")],
    [rs("c", 10, 20, ["ServiceBuilder::new()", "    .layer(A)      // снаружи: A → B → h", "    .layer(B)", "    .service(h)"], [1, 2], { ...code, lh: 26, size: 9.5 })],
  ],
});

// 10. Готовые слои
export const V10 = scene({
  labels: ["tower-http", "tower", "Свои слои"],
  caption: [
    "Трассировка, CORS, таймаут, лимит тела, сжатие, статические файлы",
    "Ограничение параллелизма и простое ограничение частоты",
    "Свои — для специфичного: авторизация, учёт, корреляция",
  ],
  frames: [
    [Box("a", 70, 40, 100, 24, "TraceLayer", "b", { size: 10 }), Box("b", 180, 40, 100, 24, "CorsLayer", "b", { size: 10 }), Box("c", 290, 40, 100, 24, "TimeoutLayer", "b", { size: 10 }), Box("d", 125, 90, 130, 24, "RequestBodyLimit", "b", { size: 9.5 }), Box("e", 265, 90, 120, 24, "CompressionLayer", "b", { size: 9 })],
    [Box("a", 100, 70, 160, 28, "ConcurrencyLimitLayer", "g", { size: 10 }), Box("b", 290, 70, 100, 28, "RateLimitLayer", "g", { size: 10 })],
    [Box("a", 90, 60, 130, 26, "общее → готовое", "g", { size: 10 }), Box("b", 90, 110, 130, 26, "своё → from_fn", "y", { size: 10 }), note("n", 270, 85, "меньше кода,\nменьше ошибок", "m")],
  ],
});

// 11. Идентификатор запроса
export const V11 = scene({
  labels: ["Присвоить", "В журнал", "Время"],
  caption: [
    "Берём из заголовка или создаём; кладём в расширения и в ответ",
    "Каждая запись журнала содержит идентификатор: запрос находится по одной строке",
    "Засекли начало, дождались ответа, записали длительность",
  ],
  frames: [
    [rs("c", 10, 20, ["let id = req.headers().get(\"x-request-id\")", "    .map(|v| v.to_owned())", "    .unwrap_or_else(new_id);", "req.extensions_mut().insert(RequestId(id));"], [3], { ...code, lh: 24, size: 8.5 })],
    [rs("c", 10, 20, ["[req-17] POST /rooms/3/msgs", "[req-17] insert message", "[req-17] 201 in 4 ms"], [0, 1, 2], { ...code, lh: 30, size: 10 })],
    [rs("c", 10, 20, ["let t = Instant::now();", "let res = next.run(req).await;", "log(\"{} in {:?}\", res.status(), t.elapsed());"], [0, 2], { ...code, lh: 28, size: 9.5 })],
  ],
});

// 12. Защита от перегрузки
export const V12 = scene({
  labels: ["413 и 408", "Параллелизм", "Ведро жетонов"],
  caption: [
    "Тело больше лимита — 413; обработчик слишком долгий — 408",
    "Не больше N запросов одновременно, остальные ждут очереди",
    "Каждый запрос тратит жетон; жетоны пополняются со временем",
  ],
  frames: [
    [Box("a", 90, 50, 130, 26, "тело 10 МБ → 413", "y", { size: 9.5 }), Box("b", 90, 100, 130, 26, "ответа нет 5 с → 408", "y", { size: 9.5 }), note("n", 270, 75, "лимит и время\nпо измерениям", "m")],
    [Box("a", 70, 40, 60, 22, "запрос", "g", { size: 9.5 }), Box("b", 130, 40, 60, 22, "запрос", "g", { size: 9.5 }), Box("c", 190, 40, 60, 22, "запрос", "g", { size: 9.5 }), Box("d", 250, 40, 60, 22, "ждёт", "y", { size: 9.5 }), Box("e", 310, 40, 60, 22, "ждёт", "y", { size: 9.5 }), note("n", 180, 100, "limit = 3", "m")],
    [Box("b", 180, 50, 160, 30, "● ● ● ○ ○   жетоны", "b", { size: 10 }), arrow("e1", 100, 90, 140, 66, "r"), arrow("e2", 260, 66, 280, 90, "g"), note("n1", 100, 105, "запрос: −1", "r"), note("n2", 280, 105, "время: +1", "g")],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Состояние", "Слои", "Дальше"],
  caption: [
    "State: Arc, атомики, блокировки не через await; FromRef и Extension — под задачу",
    "Слой оборачивает службу; from_fn для своих, tower-http для общих; порядок проверяем тестом",
    "Следующая глава: serde, JSON и единый тип ошибки приложения",
  ],
  frames: [
    [Box("a", 70, 70, 100, 30, "State + Arc", "g", { size: 10.5 }), Box("b", 180, 70, 100, 30, "FromRef", "g", { size: 10.5 }), Box("c", 290, 70, 100, 30, "Extension", "g", { size: 10.5 })],
    [Box("a", 70, 70, 100, 30, "Layer", "g", { size: 11 }), Box("b", 180, 70, 100, 30, "from_fn", "g", { size: 11 }), Box("c", 290, 70, 100, 30, "tower-http", "g", { size: 10.5 })],
    [Box("a", 90, 70, 130, 30, "serde + JSON", "b", { size: 10.5 }), Box("b", 250, 70, 130, 30, "AppError", "b", { size: 10.5 }), Box("c", 340, 70, 40, 30, "→", "y", { size: 12 })],
  ],
});
