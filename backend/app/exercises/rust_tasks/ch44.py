"""Задачи книги «Изучаем Rust»: глава 44 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {44: [{'id': 'r44-hello',
  'mode': 'rust',
  'title': 'Первый обработчик',
  'statement': 'Напишите роутер с одним маршрутом: GET / отвечает текстом «привет». Функция main '
               '(готова) отправляет два запроса: на «/» и на несуществующий путь «/nope».\n'
               '\n'
               'Ожидаемый вывод:\n'
               '(200, "привет")\n'
               '(404, "")',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{:?}", call(&app, "GET", "/", "").await);\n'
             '    println!("{:?}", call(&app, "GET", "/nope", "").await);\n'
             '}\n',
  'driver': '',
  'hint': 'Router::new().route("/", get(hello)); обработчик — async fn hello() -> &\'static str.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['(200, "привет")', '(404, "")']},
 {'id': 'r44-path',
  'mode': 'rust',
  'title': 'Параметр пути',
  'statement': 'Маршрут GET /rooms/{id} отвечает «комната N», где N — число из пути (u32). Для '
               '/rooms/abc axum сам вернёт отказ.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '"комната 7"\n'
               '400',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{:?}", call(&app, "GET", "/rooms/7", "").await.1);\n'
             '    println!("{:?}", call(&app, "GET", "/rooms/abc", "").await.0);\n'
             '}\n',
  'driver': '',
  'hint': 'Path(id): Path<u32>; формат — format!.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['"комната 7"', '400']},
 {'id': 'r44-two-params',
  'mode': 'rust',
  'title': 'Два параметра пути',
  'statement': 'Маршрут GET /rooms/{room}/msgs/{n} отвечает «room=R n=N» (оба u32). Используйте '
               'кортеж Path<(u32, u32)>.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'room=3 n=15\n'
               '404',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{}", call(&app, "GET", "/rooms/3/msgs/15", "").await.1);\n'
             '    println!("{:?}", call(&app, "GET", "/rooms/3/msgs", "").await.0);\n'
             '}\n',
  'driver': '',
  'hint': 'Path((room, n)): Path<(u32, u32)>.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['room=3 n=15', '404']},
 {'id': 'r44-wildcard',
  'mode': 'rust',
  'title': 'Остаток пути',
  'statement': 'Маршрут GET /files/{*rest} отвечает «файл: REST», где REST — весь остаток пути (в '
               'том числе со слэшами).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'файл: a.txt\n'
               'файл: docs/2026/report.pdf',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{}", call(&app, "GET", "/files/a.txt", "").await.1);\n'
             '    println!("{}", call(&app, "GET", "/files/docs/2026/report.pdf", "").await.1);\n'
             '}\n',
  'driver': '',
  'hint': 'В пути пишется {*rest}, в обработчике — Path<String>.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['файл: a.txt', 'файл: docs/2026/report.pdf']},
 {'id': 'r44-query-defaults',
  'mode': 'rust',
  'title': 'Query со значениями по умолчанию',
  'statement': 'GET /msgs принимает строку запроса: limit (u32, по умолчанию 10) и before '
               '(необязательное u64). Обработчик отвечает «limit=L before=B», где отсутствующее '
               'before печатается как «none».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'limit=10 before=none\n'
               'limit=5 before=none\n'
               'limit=10 before=100\n'
               'limit=3 before=7',
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
             'use serde::Deserialize;\n'
             '\n'
             '#[derive(Deserialize)]\n'
             'struct Page {\n'
             '    limit: u32,\n'
             '    before: Option<u64>,\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for uri in ["/msgs", "/msgs?limit=5", "/msgs?before=100", '
             '"/msgs?limit=3&before=7"] {\n'
             '        println!("{}", call(&app, "GET", uri, "").await.1);\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'Структура с #[derive(Deserialize)], #[serde(default = "fn")] и Option<u64>; экстрактор '
          'Query<Page>.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['limit=10 before=none',
               'limit=5 before=none',
               'limit=10 before=100',
               'limit=3 before=7']},
 {'id': 'r44-bad-query',
  'mode': 'rust',
  'title': 'Некорректная строка запроса',
  'statement': 'Маршрут GET /page принимает ?n=число (u32, обязательное) и отвечает «n=N». '
               'Напечатайте статусы для /page?n=5, /page?n=x и /page (без параметра).\n'
               '\n'
               'Ожидаемый вывод:\n'
               '/page?n=5 -> 200 OK n=5\n'
               '/page?n=x -> 400 Bad Request\n'
               '/page -> 400 Bad Request',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for uri in ["/page?n=5", "/page?n=x", "/page"] {\n'
             '        let (s, b) = call(&app, "GET", uri, "").await;\n'
             '        println!("{uri} -> {s} {}", if s.is_success() { b } else { String::new() '
             '});\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'Query<Params> с полем n: u32; отказ экстрактора — 400.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['/page?n=5 -> 200 OK n=5',
               '/page?n=x -> 400 Bad Request',
               '/page -> 400 Bad Request']},
 {'id': 'r44-405',
  'mode': 'rust',
  'title': 'Метод не разрешён',
  'statement': 'Маршрут /rooms принимает только GET (ответ «список») и POST (ответ «создано»). '
               'Напечатайте статусы для GET, POST, PUT и DELETE по /rooms и по /other.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'GET /rooms -> 200 OK\n'
               'POST /rooms -> 200 OK\n'
               'PUT /rooms -> 405 Method Not Allowed\n'
               'DELETE /rooms -> 405 Method Not Allowed\n'
               'GET /other -> 404 Not Found',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for m in ["GET", "POST", "PUT", "DELETE"] {\n'
             '        println!("{m} /rooms -> {}", call(&app, m, "/rooms", "").await.0);\n'
             '    }\n'
             '    println!("GET /other -> {}", call(&app, "GET", "/other", "").await.0);\n'
             '}\n',
  'driver': '',
  'hint': 'get(list).post(create); неподходящий метод даёт 405 сам.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['GET /rooms -> 200 OK',
               'POST /rooms -> 200 OK',
               'PUT /rooms -> 405 Method Not Allowed',
               'DELETE /rooms -> 405 Method Not Allowed',
               'GET /other -> 404 Not Found']},
 {'id': 'r44-fallback',
  'mode': 'rust',
  'title': 'Свой ответ 404',
  'statement': 'Добавьте к роутеру запасной обработчик: для любого неизвестного пути статус 404 и '
               'тело {"error":"not found"} (строкой). Маршрут GET /health отвечает «ok».\n'
               '\n'
               'Ожидаемый вывод:\n'
               '(200, "ok")\n'
               '(404, "{\\"error\\":\\"not found\\"}")',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{:?}", call(&app, "GET", "/health", "").await);\n'
             '    println!("{:?}", call(&app, "GET", "/nowhere", "").await);\n'
             '}\n',
  'driver': '',
  'hint': 'Router::fallback(handler); кортеж (StatusCode::NOT_FOUND, текст).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['(200, "ok")', '(404, "{\\"error\\":\\"not found\\"}")']},
 {'id': 'r44-created',
  'mode': 'rust',
  'title': '201 и заголовок Location',
  'statement': 'POST /rooms отвечает статусом 201 и заголовком Location: /rooms/42, тело — '
               '«создано». main печатает статус, заголовок Location и тело.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '201 Created Some("/rooms/42") создано',
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
             'async fn call_full(app: &Router, uri: &str) -> (StatusCode, Option<String>, String) '
             '{\n'
             '    let req = '
             'Request::builder().method("POST").uri(uri).body(Body::empty()).unwrap();\n'
             '    let res = app.clone().oneshot(req).await.unwrap();\n'
             '    let status = res.status();\n'
             '    let loc = res.headers().get("location").map(|v| '
             'v.to_str().unwrap().to_string());\n'
             '    let body = to_bytes(res.into_body(), 1 << 20).await.unwrap();\n'
             '    (status, loc, String::from_utf8_lossy(&body).into_owned())\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    let (s, loc, body) = call_full(&app, "/rooms").await;\n'
             '    println!("{s} {loc:?} {body}");\n'
             '}\n',
  'driver': '',
  'hint': 'Кортеж (StatusCode::CREATED, [(header::LOCATION, "/rooms/42")], "создано").',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['201 Created Some("/rooms/42") создано']},
 {'id': 'r44-204',
  'mode': 'rust',
  'title': '204 без тела',
  'statement': 'DELETE /rooms/{id} отвечает статусом 204 No Content и пустым телом, если id — '
               'число; иначе (для нечислового id) ответ формирует сам axum. Напечатайте статус и '
               'длину тела.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '/rooms/5 204 No Content длина тела 0\n'
               '/rooms/x 400 Bad Request длина тела 40',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for uri in ["/rooms/5", "/rooms/x"] {\n'
             '        let (s, b) = call(&app, "DELETE", uri, "").await;\n'
             '        println!("{uri} {s} длина тела {}", b.len());\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'Возвращайте StatusCode::NO_CONTENT.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['/rooms/5 204 No Content длина тела 0', '/rooms/x 400 Bad Request длина тела 40']},
 {'id': 'r44-json-out',
  'mode': 'rust',
  'title': 'Ответ в формате JSON',
  'statement': 'GET /rooms/{id} возвращает JSON {"id":N,"name":"room-N"} (структура Room с '
               'Serialize). Напечатайте тело ответа для /rooms/3.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '{"id":3,"name":"room-3"}',
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
             'use serde::Serialize;\n'
             '\n'
             '#[derive(Serialize)]\n'
             'struct Room {\n'
             '    id: u32,\n'
             '    name: String,\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{}", call(&app, "GET", "/rooms/3", "").await.1);\n'
             '}\n',
  'driver': '',
  'hint': 'Json(Room { id, name }) с #[derive(Serialize)].',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['{"id":3,"name":"room-3"}']},
 {'id': 'r44-json-in',
  'mode': 'rust',
  'title': 'Тело запроса в формате JSON',
  'statement': 'POST /echo принимает JSON {"user":"имя","text":"текст"} (структура Msg с '
               'Deserialize) и отвечает «имя: текст (N символов)», где N — число символов (chars) '
               'в тексте.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'аня: привет (6 символов)',
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
             'use serde::Deserialize;\n'
             '\n'
             '#[derive(Deserialize)]\n'
             'struct Msg {\n'
             '    user: String,\n'
             '    text: String,\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{}", call(&app, "POST", "/echo", '
             'r#"{"user":"аня","text":"привет"}"#).await.1);\n'
             '}\n',
  'driver': '',
  'hint': 'Json(m): Json<Msg>; число символов — m.text.chars().count().',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['аня: привет (6 символов)']},
 {'id': 'r44-json-errors',
  'mode': 'rust',
  'title': 'Ошибки разбора JSON',
  'statement': 'POST /echo принимает JSON {"n":число}. Напечатайте статусы ответа axum на три '
               'тела: корректное, синтаксически неверное (не JSON) и с неверным типом поля (n — '
               'строка).\n'
               '\n'
               'Ожидаемый вывод:\n'
               '200 OK\n'
               '400 Bad Request\n'
               '422 Unprocessable Entity',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for body in [r#"{"n": 5}"#, "not json", r#"{"n": "five"}"#] {\n'
             '        println!("{}", call(&app, "POST", "/echo", body).await.0);\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'Json<Num> с полем n: i64; отказы: синтаксис — 400, данные не подходят — 422.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['200 OK', '400 Bad Request', '422 Unprocessable Entity']},
 {'id': 'r44-into-response',
  'mode': 'rust',
  'title': 'Свой тип ответа',
  'statement': 'Реализуйте IntoResponse для перечисления Reply: Ok(String) → 200 и текст; '
               'Created(String) → 201 и текст; Gone → 410 с телом «удалено». Маршрут GET /r/{kind} '
               'возвращает Reply по kind: «ok», «created» или «gone» (другое — 404).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'ok: 200 OK хорошо\n'
               'created: 201 Created создано\n'
               'gone: 410 Gone удалено\n'
               'zzz: 404 Not Found',
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
             'use axum::response::{IntoResponse, Response};\n'
             '\n'
             'enum Reply {\n'
             '    Ok(String),\n'
             '    Created(String),\n'
             '    Gone,\n'
             '}\n'
             '\n'
             'impl IntoResponse for Reply {\n'
             '    fn into_response(self) -> Response {\n'
             '        todo!()\n'
             '    }\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for k in ["ok", "created", "gone", "zzz"] {\n'
             '        let (s, b) = call(&app, "GET", &format!("/r/{k}"), "").await;\n'
             '        println!("{k}: {s} {b}");\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'impl IntoResponse for Reply { fn into_response(self) -> Response { ... } }.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['ok: 200 OK хорошо',
               'created: 201 Created создано',
               'gone: 410 Gone удалено',
               'zzz: 404 Not Found']},
 {'id': 'r44-result',
  'mode': 'rust',
  'title': 'Result как ответ',
  'statement': 'GET /rooms/{id}: комнаты 1 и 2 существуют (ответ «комната-1», «комната-2»), '
               'остальные — 404 с текстом «нет такой комнаты». Обработчик возвращает '
               "Result<String, (StatusCode, &'static str)>.\n"
               '\n'
               'Ожидаемый вывод:\n'
               '(200, "комната-1")\n'
               '(200, "комната-2")\n'
               '(404, "нет такой комнаты")',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for id in [1, 2, 3] {\n'
             '        println!("{:?}", call(&app, "GET", &format!("/rooms/{id}"), "").await);\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'Err((StatusCode::NOT_FOUND, "нет такой комнаты")) — кортеж умеет превращаться в ответ.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['(200, "комната-1")', '(200, "комната-2")', '(404, "нет такой комнаты")']},
 {'id': 'r44-nest',
  'mode': 'rust',
  'title': 'Вложенный роутер',
  'statement': 'Функция rooms() возвращает Router с маршрутами GET / («все комнаты») и GET /{id} '
               '(«комната ID»). Смонтируйте его под префиксом /api/rooms (nest). Напечатайте тела '
               'для /api/rooms, /api/rooms/9 и статус для /rooms.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'все комнаты\n'
               'комната 9\n'
               '404 Not Found',
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
             'use axum::routing::get;\n'
             '\n'
             'fn rooms() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{}", call(&app, "GET", "/api/rooms", "").await.1);\n'
             '    println!("{}", call(&app, "GET", "/api/rooms/9", "").await.1);\n'
             '    println!("{}", call(&app, "GET", "/rooms", "").await.0);\n'
             '}\n',
  'driver': '',
  'hint': 'Router::new().nest("/api/rooms", rooms()).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['все комнаты', 'комната 9', '404 Not Found']},
 {'id': 'r44-merge',
  'mode': 'rust',
  'title': 'Объединение роутеров',
  'statement': 'Есть два роутера: users() с GET /users («пользователи») и rooms() с GET /rooms '
               '(«комнаты»). Объедините их в app() методом merge, добавив ещё GET /health («ok»). '
               'Напечатайте тела трёх путей.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '/users: пользователи\n'
               '/rooms: комнаты\n'
               '/health: ok',
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
             'use axum::routing::get;\n'
             '\n'
             'fn users() -> Router {\n'
             '    Router::new().route("/users", get(|| async { "пользователи" }))\n'
             '}\n'
             'fn rooms() -> Router {\n'
             '    Router::new().route("/rooms", get(|| async { "комнаты" }))\n'
             '}\n'
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for p in ["/users", "/rooms", "/health"] {\n'
             '        println!("{p}: {}", call(&app, "GET", p, "").await.1);\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'Router::new().merge(users()).merge(rooms()).route(...).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['/users: пользователи', '/rooms: комнаты', '/health: ok']},
 {'id': 'r44-nested-fallback',
  'mode': 'rust',
  'title': 'Запасной ответ вложенного роутера',
  'statement': 'API под /api отвечает на неизвестные пути своим 404 с текстом «api: нет»; всё '
               'приложение вне /api — текстом «app: нет». Маршрут GET /api/ping отвечает «pong». '
               'Напечатайте ответы для /api/ping, /api/zzz, /zzz.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '/api/ping: (200, "pong")\n'
               '/api/zzz: (404, "api: нет")\n'
               '/zzz: (404, "app: нет")',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for p in ["/api/ping", "/api/zzz", "/zzz"] {\n'
             '        println!("{p}: {:?}", call(&app, "GET", p, "").await);\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'У вложенного роутера свой .fallback(..), у внешнего — свой.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['/api/ping: (200, "pong")',
               '/api/zzz: (404, "api: нет")',
               '/zzz: (404, "app: нет")']},
 {'id': 'r44-head',
  'mode': 'rust',
  'title': 'HEAD через GET',
  'statement': 'Маршрут GET /info отвечает «информация». Напечатайте статус и длину тела для '
               'запроса GET и для запроса HEAD по /info (axum обрабатывает HEAD сам).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'GET: 200 OK, тело есть\n'
               'HEAD: 200 OK, тело пустое',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for m in ["GET", "HEAD"] {\n'
             '        let (s, b) = call(&app, m, "/info", "").await;\n'
             '        println!("{m}: {s}, тело {}", if b.is_empty() { "пустое" } else { "есть" '
             '});\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'Отдельный обработчик HEAD писать не нужно.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['GET: 200 OK, тело есть', 'HEAD: 200 OK, тело пустое']},
 {'id': 'r44-headers-out',
  'mode': 'rust',
  'title': 'Свой заголовок в ответе',
  'statement': 'GET /ver отвечает телом «v1» и заголовком X-Api-Version: 1. main читает заголовок '
               'из ответа.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'Some("1")\n'
               'None',
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
             'async fn header_of(app: &Router, uri: &str, name: &str) -> Option<String> {\n'
             '    let res = '
             'app.clone().oneshot(Request::get(uri).body(Body::empty()).unwrap()).await.unwrap();\n'
             '    res.headers().get(name).map(|v| v.to_str().unwrap().to_string())\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{:?}", header_of(&app, "/ver", "x-api-version").await);\n'
             '    println!("{:?}", header_of(&app, "/ver", "x-other").await);\n'
             '}\n',
  'driver': '',
  'hint': 'Кортеж ([("x-api-version", "1")], "v1").',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['Some("1")', 'None']},
 {'id': 'r44-header-in',
  'mode': 'rust',
  'title': 'Заголовок запроса',
  'statement': 'GET /agent отвечает «agent: ...» с значением заголовка User-Agent или «agent: '
               'неизвестен», если заголовка нет. Используйте экстрактор HeaderMap.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'agent: curl/8\n'
               'agent: неизвестен',
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
             'async fn with_agent(app: &Router, agent: Option<&str>) -> String {\n'
             '    let mut b = Request::get("/agent");\n'
             '    if let Some(a) = agent {\n'
             '        b = b.header("user-agent", a);\n'
             '    }\n'
             '    let res = app.clone().oneshot(b.body(Body::empty()).unwrap()).await.unwrap();\n'
             '    String::from_utf8_lossy(&to_bytes(res.into_body(), 1 << '
             '20).await.unwrap()).into_owned()\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{}", with_agent(&app, Some("curl/8")).await);\n'
             '    println!("{}", with_agent(&app, None).await);\n'
             '}\n',
  'driver': '',
  'hint': 'headers.get("user-agent").and_then(|v| v.to_str().ok()).',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['agent: curl/8', 'agent: неизвестен']},
 {'id': 'r44-raw-request',
  'mode': 'rust',
  'title': 'Запрос целиком',
  'statement': 'Обработчик any-метода для пути /whoami принимает весь Request<Body> и отвечает '
               '«МЕТОД ПУТЬ», например «POST /whoami?x=1». main шлёт GET и POST.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'GET /whoami\n'
               'POST /whoami?x=1',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{}", call(&app, "GET", "/whoami", "").await.1);\n'
             '    println!("{}", call(&app, "POST", "/whoami?x=1", "").await.1);\n'
             '}\n',
  'driver': '',
  'hint': 'axum::routing::any; req.method(), req.uri().',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['GET /whoami', 'POST /whoami?x=1']},
 {'id': 'r44-conflict',
  'mode': 'rust',
  'title': '409 при конфликте',
  'statement': 'POST /rooms/{name}: имя «general» уже занято — ответ 409 и текст «занято», любое '
               'другое — 201 и текст «создана». Проверьте общий и произвольный случаи.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'general: (409, "занято")\n'
               'random: (201, "создана")',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for n in ["general", "random"] {\n'
             '        println!("{n}: {:?}", call(&app, "POST", &format!("/rooms/{n}"), '
             '"").await);\n'
             '    }\n'
             '}\n',
  'driver': '',
  'hint': 'Возвращайте кортеж (StatusCode, &str) в обеих ветках.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['general: (409, "занято")', 'random: (201, "создана")']},
 {'id': 'r44-async-handler',
  'mode': 'rust',
  'title': 'Обработчик с ожиданием',
  'statement': 'GET /slow/{ms} ждёт ms миллисекунд (tokio::time::sleep) и отвечает «ждал ms мс». '
               'Три запроса отправляются одновременно (tokio::join!) с ожиданиями 60, 20 и 40; '
               'main печатает ответы в порядке запросов и «всё за < 110 мс: true/false» '
               '(параллельно должно быть быстрее суммы 120 мс).\n'
               '\n'
               'Ожидаемый вывод:\n'
               'ждал 60 мс\n'
               'ждал 20 мс\n'
               'ждал 40 мс\n'
               'всё за < 110 мс: true',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    let t = std::time::Instant::now();\n'
             '    let (a, b, c) = tokio::join!(\n'
             '        call(&app, "GET", "/slow/60", ""),\n'
             '        call(&app, "GET", "/slow/20", ""),\n'
             '        call(&app, "GET", "/slow/40", "")\n'
             '    );\n'
             '    println!("{}\\n{}\\n{}", a.1, b.1, c.1);\n'
             '    println!("всё за < 110 мс: {}", t.elapsed().as_millis() < 110);\n'
             '}\n',
  'driver': '',
  'hint': 'async-обработчик с sleep(Duration::from_millis(ms)).await.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['ждал 60 мс', 'ждал 20 мс', 'ждал 40 мс', 'всё за < 110 мс: true']},
 {'id': 'r44-static-first',
  'mode': 'rust',
  'title': 'Статический путь против параметра',
  'statement': 'Маршруты: GET /rooms/new («форма») и GET /rooms/{id} («комната ID»). Порядок их '
               'регистрации не должен влиять на результат: статический путь выигрывает. '
               'Зарегистрируйте сначала параметрический, затем статический и напечатайте ответы '
               'для /rooms/new и /rooms/5.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'форма\n'
               'комната 5',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{}", call(&app, "GET", "/rooms/new", "").await.1);\n'
             '    println!("{}", call(&app, "GET", "/rooms/5", "").await.1);\n'
             '}\n',
  'driver': '',
  'hint': 'matchit выбирает самое конкретное совпадение независимо от порядка.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['форма', 'комната 5']},
 {'id': 'r44-redirect',
  'mode': 'rust',
  'title': 'Перенаправление',
  'statement': 'GET /old отвечает перенаправлением на /new (Redirect::to — статус 303 и заголовок '
               'Location), GET /new — «новая». main печатает статус и Location для /old.\n'
               '\n'
               'Ожидаемый вывод:\n'
               '(303, Some("/new"))\n'
               '(200, None)',
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
             'async fn location(app: &Router, uri: &str) -> (StatusCode, Option<String>) {\n'
             '    let res = '
             'app.clone().oneshot(Request::get(uri).body(Body::empty()).unwrap()).await.unwrap();\n'
             '    let loc = res.headers().get("location").map(|v| '
             'v.to_str().unwrap().to_string());\n'
             '    (res.status(), loc)\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{:?}", location(&app, "/old").await);\n'
             '    println!("{:?}", location(&app, "/new").await);\n'
             '}\n',
  'driver': '',
  'hint': 'axum::response::Redirect::to("/new").',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['(303, Some("/new"))', '(200, None)']},
 {'id': 'r44-method-router',
  'mode': 'rust',
  'title': 'Все методы ресурса',
  'statement': 'Ресурс /rooms/{id} поддерживает четыре метода: GET («читаем ID»), PUT («меняем '
               'ID»), PATCH («правим ID»), DELETE («удаляем ID»). Один вызов .route с цепочкой '
               'get().put().patch().delete(). Напечатайте ответы для всех четырёх методов по '
               '/rooms/8 и статус POST.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'GET: читаем 8\n'
               'PUT: меняем 8\n'
               'PATCH: правим 8\n'
               'DELETE: удаляем 8\n'
               'POST: 405 Method Not Allowed',
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
             'fn app() -> Router {\n'
             '    Router::new()\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    for m in ["GET", "PUT", "PATCH", "DELETE"] {\n'
             '        println!("{m}: {}", call(&app, m, "/rooms/8", "").await.1);\n'
             '    }\n'
             '    println!("POST: {}", call(&app, "POST", "/rooms/8", "").await.0);\n'
             '}\n',
  'driver': '',
  'hint': 'get(h1).put(h2).patch(h3).delete(h4); обработчики можно писать замыканиями.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['GET: читаем 8',
               'PUT: меняем 8',
               'PATCH: правим 8',
               'DELETE: удаляем 8',
               'POST: 405 Method Not Allowed']},
 {'id': 'r44-real-server',
  'mode': 'rust',
  'title': 'Настоящий сервер на порту 0',
  'statement': 'Запустите сервер на 127.0.0.1:0 (TcpListener + axum::serve в задаче tokio), '
               'узнайте порт и отправьте обычный HTTP/1.1-запрос «GET /hi» по TcpStream с '
               'Connection: close. Обработчик отвечает «привет из axum». Напечатайте первую строку '
               'ответа (статус) и последнюю строку тела.\n'
               '\n'
               'Ожидаемый вывод:\n'
               'HTTP/1.1 200 OK\n'
               'привет из axum',
  'starter': 'use tokio::io::{AsyncReadExt, AsyncWriteExt};\n'
             'use tokio::net::{TcpListener, TcpStream};\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    // ваш код\n'
             '}\n',
  'driver': '',
  'hint': 'tokio::spawn(async move { axum::serve(listener, app).await.unwrap() }); читайте ответ '
          'read_to_string.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['HTTP/1.1 200 OK', 'привет из axum']},
 {'id': 'r44-fix-body-order',
  'mode': 'rust',
  'title': 'Исправьте: тело не последним',
  'statement': 'Код не компилируется: Json читает тело и должен быть последним аргументом '
               'обработчика. Исправьте порядок аргументов, чтобы POST /rooms/5/say с телом '
               '{"text":"hi"} отвечал «5: hi».\n'
               '\n'
               'Ожидаемый вывод:\n'
               '5: hi',
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
             'use axum::extract::Path;\n'
             'use axum::routing::post;\n'
             'use axum::Json;\n'
             'use serde::Deserialize;\n'
             '\n'
             '#[derive(Deserialize)]\n'
             'struct Say {\n'
             '    text: String,\n'
             '}\n'
             '\n'
             'async fn say(Json(m): Json<Say>, Path(id): Path<u32>) -> String {\n'
             '    format!("{id}: {}", m.text)\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new().route("/rooms/{id}/say", post(say))\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{}", call(&app, "POST", "/rooms/5/say", r#"{"text":"hi"}"#).await.1);\n'
             '}\n',
  'driver': '',
  'hint': 'Path — первым, Json — последним.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['5: hi']},
 {'id': 'r44-fix-not-send',
  'mode': 'rust',
  'title': 'Исправьте: значение не Send через await',
  'statement': 'Код не компилируется: std::sync::MutexGuard удерживается через .await, а будущее '
               'обработчика обязано быть Send. Исправьте так, чтобы блокировка отпускалась до '
               'await (ограничьте её область блоком); ответ — «счётчик: 1», затем «счётчик: 2».\n'
               '\n'
               'Ожидаемый вывод:\n'
               'счётчик: 1\n'
               'счётчик: 2',
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
             'use axum::extract::State;\n'
             'use axum::routing::get;\n'
             'use std::sync::{Arc, Mutex};\n'
             'use std::time::Duration;\n'
             '\n'
             'async fn bump(State(c): State<Arc<Mutex<u32>>>) -> String {\n'
             '    let mut g = c.lock().unwrap();\n'
             '    *g += 1;\n'
             '    tokio::time::sleep(Duration::from_millis(1)).await;\n'
             '    format!("счётчик: {}", *g)\n'
             '}\n'
             '\n'
             'fn app() -> Router {\n'
             '    Router::new().route("/bump", get(bump)).with_state(Arc::new(Mutex::new(0)))\n'
             '}\n'
             '\n'
             '#[tokio::main]\n'
             'async fn main() {\n'
             '    let app = app();\n'
             '    println!("{}", call(&app, "GET", "/bump", "").await.1);\n'
             '    println!("{}", call(&app, "GET", "/bump", "").await.1);\n'
             '}\n',
  'driver': '',
  'hint': 'Возьмите значение в отдельном блоке { let mut g = ...; *g += 1; *g } до sleep.',
  'standalone': True,
  'crates': ['tokio'],
  'expected': ['счётчик: 1', 'счётчик: 2']}]}
