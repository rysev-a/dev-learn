import { scene } from "./alg.tsx";
import { Box, Tx, arrow, jc } from "./jv.tsx";

/* Глава 22 книги «Современный Frontend»: HTTP-сервер на Node.js. */

const code = { w: 340, size: 9.5, lh: 14 };

// 1. Сервер на Node.js
export const V01 = scene({
  labels: ["Клиент и сервер", "Модуль http", "План"],
  caption: [
    "Браузер шлёт запрос, сервер отвечает — и этот сервер можно написать на JavaScript",
    "Встроенный модуль http: слушать порт, разбирать запросы, отправлять ответы",
    "Маршрутизатор, цепочка обработчиков, тело запроса, JSON-ответы, ошибки; тесты на петле",
  ],
  frames: [
    [Box("c", 70, 80, 100, 40, "браузер", "b", { size: 11 }), arrow("e1", 122, 70, 238, 70, "g"), arrow("e2", 238, 90, 122, 90, "m"), Box("s", 290, 80, 100, 40, "Node.js", "g", { size: 11 }), Tx("a", 180, 56, "запрос", { size: 9 }), Tx("b", 180, 108, "ответ", { size: 9 })],
    [jc("c", 20, 40, ["import http from \"node:http\";", "", "http.createServer((req, res) => {", "  res.end(\"hi\");", "}).listen(3000);"], [2, 3], { ...code, lh: 18, size: 10 })],
    [Box("a", 65, 50, 110, 28, "маршруты", "g", { size: 10 }), Box("b", 180, 50, 110, 28, "middleware", "g", { size: 10 }), Box("c", 295, 50, 110, 28, "тело запроса", "g", { size: 10 }), Box("d", 120, 98, 110, 28, "JSON и ошибки", "g", { size: 10 }), Box("e", 240, 98, 110, 28, "тесты на 127.0.0.1", "g", { size: 8.5 })],
  ],
});

// 2. createServer
export const V02 = scene({
  labels: ["Обработчик", "req и res", "listen(0)"],
  caption: [
    "createServer(handler): обработчик вызывается на каждый запрос",
    "req — поток для чтения (метод, url, заголовки); res — поток для записи",
    "Порт 0 — система выберет свободный; server.address().port подскажет какой",
  ],
  frames: [
    [jc("c", 10, 20, ["const server = http.createServer((req, res) => {", "  // вызывается для КАЖДОГО запроса", "});"], [0, 1], { ...code, lh: 18, size: 9.5 })],
    [Box("r", 90, 60, 130, 36, "req\nmethod, url, headers", "b", { size: 8.5 }), Box("s", 270, 60, 130, 36, "res\nwriteHead, write, end", "g", { size: 8.5 }), jc("c", 10, 108, ["res.writeHead(200, { \"Content-Type\": \"text/plain\" });", "res.end(\"ok\");"], [0, 1], { ...code, size: 9 })],
    [jc("c", 10, 30, ["server.listen(0, () => {", "  const { port } = server.address();", "  console.log(port > 0);", "});"], [1], { ...code, lh: 18 })],
  ],
});

// 3. Маршрутизация
export const V03 = scene({
  labels: ["Метод + путь", "Параметры", "404 и 405"],
  caption: [
    "Маршрут — пара (метод, путь): GET /users — список, POST /users — создание",
    "Шаблон /users/:id: из /users/42 параметр id равен строке «42»",
    "Путь неизвестен — 404; путь есть, метод не тот — 405 и заголовок Allow",
  ],
  frames: [
    [Box("a", 90, 50, 150, 26, "GET   /users", "g", { size: 10 }), Box("b", 90, 86, 150, 26, "POST  /users", "g", { size: 10 }), Box("c", 90, 122, 150, 26, "GET   /users/:id", "g", { size: 10 }), Box("l", 280, 50, 100, 26, "список", "b", { size: 9.5 }), Box("m", 280, 86, 100, 26, "создать", "b", { size: 9.5 }), Box("n", 280, 122, 100, 26, "одна запись", "b", { size: 9.5 })],
    [Box("p", 100, 60, 150, 28, "/users/:id", "g", { size: 11 }), Box("u", 100, 110, 150, 28, "/users/42", "b", { size: 11 }), arrow("e", 175, 74, 175, 96, "g"), Box("r", 290, 85, 110, 40, "{ id: \"42\" }", "g", { size: 10 })],
    [jc("c", 10, 20, ["GET  /nope        → 404", "DELETE /users      → 405", "Allow: GET, POST"], [0, 1, 2], { ...code, lh: 22, size: 10.5 })],
  ],
});

// 4. Тело запроса
export const V04 = scene({
  labels: ["Чанки", "Предел", "JSON.parse"],
  caption: [
    "Тело приходит кусками: подписка на data или for await (const chunk of req)",
    "Размер ограничен: больше предела — 413 и остановка чтения",
    "Склеили, разобрали; некорректный JSON — 400, а не исключение",
  ],
  frames: [
    [...["{\"na", "me\":", "\"Аня\"}"].map((t, i) => Box(`k${i}`, 70 + i * 100, 60, 90, 28, t, "b", { size: 10 })), Tx("n", 180, 110, "чанки склеиваются в тело", { size: 9.5 })],
    [Box("l", 90, 60, 140, 28, "лимит 1 МБ", "g", { size: 10 }), Box("b", 270, 60, 140, 28, "пришло 5 ГБ ✗", "r", { size: 10 }), Tx("n", 180, 110, "ответ 413, чтение прервано", { size: 9.5, c: "r" })],
    [jc("c", 10, 14, ["let body;", "try { body = JSON.parse(text); }", "catch { return send(res, 400, { error: \"bad json\" }); }"], [2], { ...code, lh: 18, size: 9 })],
  ],
});

// 5. JSON-ответы
export const V05 = scene({
  labels: ["Заголовок и тело", "Коды успеха", "Коды ошибок"],
  caption: [
    "Content-Type: application/json и JSON.stringify для тела",
    "200 OK, 201 Created, 204 No Content",
    "400 плохой запрос, 404 не найдено, 422 не прошло проверку, 500 сбой сервера",
  ],
  frames: [
    [jc("c", 10, 20, ["res.writeHead(200, {", "  \"Content-Type\": \"application/json\" });", "res.end(JSON.stringify({ ok: true }));"], [0, 1, 2], { ...code, lh: 18, size: 9.5 })],
    [Box("a", 70, 70, 100, 40, "200\nOK", "g", { size: 11 }), Box("b", 180, 70, 100, 40, "201\nCreated", "g", { size: 11 }), Box("c", 290, 70, 100, 40, "204\nNo Content", "g", { size: 10 })],
    [Box("a", 65, 50, 100, 30, "400 запрос", "y", { size: 10 }), Box("b", 180, 50, 100, 30, "404 нет", "y", { size: 10 }), Box("c", 295, 50, 100, 30, "422 проверка", "y", { size: 10 }), Box("d", 180, 100, 120, 30, "500 сбой", "r", { size: 10 })],
  ],
});

// 6. Middleware
export const V06 = scene({
  labels: ["Цепочка", "next()", "Остановка"],
  caption: [
    "Журнал → проверка доступа → разбор тела → маршрут",
    "Каждый делает своё и вызывает next(), передавая запрос дальше",
    "Не вызвал next — цепочка остановлена: например, 401 без токена",
  ],
  frames: [
    [Box("a", 50, 80, 70, 40, "журнал", "b", { size: 9.5 }), Box("b", 128, 80, 70, 40, "доступ", "b", { size: 9.5 }), Box("c", 206, 80, 70, 40, "тело", "b", { size: 9.5 }), Box("d", 300, 80, 90, 40, "маршрут", "g", { size: 10 }), arrow("e1", 86, 80, 92, 80, "m"), arrow("e2", 164, 80, 170, 80, "m"), arrow("e3", 242, 80, 252, 80, "m")],
    [jc("c", 10, 20, ["const log = (req, res, next) => {", "  console.log(req.method, req.url);", "  next();", "};"], [2], { ...code, lh: 18, size: 9.5 })],
    [Box("a", 50, 80, 70, 40, "журнал", "g", { size: 9.5 }), Box("b", 128, 80, 70, 40, "доступ\n401 ✗", "r", { size: 9 }), Box("c", 206, 80, 70, 40, "тело", "m", { size: 9.5 }), Box("d", 300, 80, 90, 40, "маршрут", "m", { size: 10 }), Tx("n", 180, 130, "дальше запрос не идёт", { size: 9.5, c: "r" })],
  ],
});

// 7. Обработка ошибок
export const V07 = scene({
  labels: ["try/catch", "Обработчик ошибок", "Не светить детали"],
  caption: [
    "async-обработчик: ждём результат и ловим отказ промиса — иначе процесс упадёт",
    "Известные ошибки превращаются в свои коды, остальные — в 500",
    "Подробности — в журнал, клиенту — общее сообщение",
  ],
  frames: [
    [jc("c", 10, 14, ["async function handle(req, res) {", "  try { await route(req, res); }", "  catch (e) { onError(e, res); }", "}"], [1, 2], { ...code, lh: 18, size: 9.5 })],
    [Box("a", 70, 60, 110, 28, "NotFound → 404", "y", { size: 9.5 }), Box("b", 180, 60, 110, 28, "Invalid → 422", "y", { size: 9.5 }), Box("c", 295, 60, 110, 28, "другое → 500", "r", { size: 9.5 })],
    [Box("a", 90, 70, 150, 36, "журнал: стек,\nпараметры, id запроса", "b", { size: 9 }), Box("b", 270, 70, 150, 36, "клиент:\n{ error: \"internal\" }", "g", { size: 9 })],
  ],
});

// 8. Query-параметры
export const V08 = scene({
  labels: ["URLSearchParams", "Границы", "Метаданные"],
  caption: [
    "Строка запроса разбирается URLSearchParams: повторяющиеся ключи, проценты",
    "Всё — строки: приведите к числу и ограничьте: page ≥ 1, per_page ≤ 100",
    "Ответ списком: данные, всего записей, ссылки next и prev",
  ],
  frames: [
    [jc("c", 10, 14, ["const u = new URL(req.url, \"http://x\");", "u.searchParams.get(\"page\");     // \"2\"", "u.searchParams.getAll(\"tag\");  // [\"a\", \"b\"]"], [1, 2], { ...code, lh: 18, size: 9 })],
    [jc("c", 10, 20, ["const page = Math.max(1, Number(q.page) || 1);", "const per = Math.min(100, Number(q.per_page) || 20);"], [0, 1], { ...code, lh: 22, size: 9 })],
    [jc("c", 10, 14, ["{ \"data\": [ … ],", "  \"meta\": { \"total\": 95, \"page\": 2 },", "  \"links\": { \"next\": \"?page=3\", \"prev\": \"?page=1\" } }"], [1, 2], { ...code, lh: 18, size: 9 })],
  ],
});

// 9. CORS и заголовки
export const V09 = scene({
  labels: ["Чужой origin", "Preflight", "Allowlist"],
  caption: [
    "Страница с одного origin не прочитает ответ с другого, пока сервер не разрешит",
    "OPTIONS-запрос заранее спрашивает, какие методы и заголовки допустимы",
    "Разрешаем конкретные origin из списка, а не звёздочку — особенно с куками",
  ],
  frames: [
    [Box("p", 70, 70, 110, 36, "app.example.com", "b", { size: 9 }), arrow("e", 128, 70, 232, 70, "g"), Box("s", 300, 70, 110, 36, "api.example.com", "b", { size: 9 }), Tx("n", 180, 110, "Access-Control-Allow-Origin ?", { size: 9.5, c: "y" })],
    [Box("p", 70, 60, 100, 30, "OPTIONS", "y", { size: 10 }), arrow("e", 122, 60, 238, 60, "g"), Box("s", 300, 60, 100, 30, "204 + Allow-*", "g", { size: 9 }), Box("q", 70, 110, 100, 30, "POST", "b", { size: 10 }), arrow("f", 122, 110, 238, 110, "m")],
    [jc("c", 10, 20, ["const ALLOW = [\"https://app.example.com\"];", "if (ALLOW.includes(origin))", "  res.setHeader(\"Access-Control-Allow-Origin\", origin);"], [1, 2], { ...code, lh: 18, size: 9 })],
  ],
});

// 10. Статика и потоки
export const V10 = scene({
  labels: ["pipe", "Обход каталога", "Проверка корня"],
  caption: [
    "createReadStream(file).pipe(res): читаем кусками, не загружая файл в память",
    "/../../etc/passwd выйдет за пределы каталога, если подставить путь как есть",
    "resolve(root, path) и проверка префикса: результат должен остаться внутри root",
  ],
  frames: [
    [Box("f", 70, 70, 100, 36, "файл", "b", { size: 11 }), arrow("e1", 122, 70, 148, 70, "g"), Box("p", 180, 70, 70, 36, "pipe", "g", { size: 10 }), arrow("e2", 216, 70, 242, 70, "g"), Box("r", 300, 70, 100, 36, "res", "b", { size: 11 })],
    [jc("c", 10, 30, ["join(\"/srv/public\", \"/../../etc/passwd\")", "// → /etc/passwd   ✗"], [1], { ...code, lh: 22, bad: [1], size: 9.5 })],
    [jc("c", 10, 14, ["const full = resolve(root, \".\" + urlPath);", "if (!full.startsWith(root + sep)) {", "  return send(res, 403);", "}"], [1, 2], { ...code, lh: 18, size: 9.5 })],
  ],
});

// 11. Соединения и пределы
export const V11 = scene({
  labels: ["Медленный клиент", "Пределы", "keep-alive"],
  caption: [
    "Медленный клиент часами держит соединение, огромное тело съедает память",
    "Таймауты, размер тела, частота запросов, число соединений",
    "keep-alive переиспользует соединение, но с таймаутом простоя",
  ],
  frames: [
    [Box("a", 90, 60, 130, 30, "клиент: 1 байт/мин", "r", { size: 9.5 }), Box("b", 270, 60, 130, 30, "тело 5 ГБ", "r", { size: 10 }), Box("c", 180, 110, 160, 30, "поток запросов с IP", "y", { size: 10 })],
    [Box("a", 65, 50, 110, 28, "headersTimeout", "g", { size: 9.5 }), Box("b", 180, 50, 110, 28, "лимит тела", "g", { size: 10 }), Box("c", 295, 50, 110, 28, "rate limit", "g", { size: 10 }), Box("d", 180, 100, 160, 28, "maxConnections", "g", { size: 10 })],
    [jc("c", 10, 20, ["server.keepAliveTimeout = 5000;", "server.headersTimeout  = 10000;", "server.requestTimeout  = 30000;"], [0, 1, 2], { ...code, lh: 20, size: 10 })],
  ],
});

// 12. Тесты API
export const V12 = scene({
  labels: ["Свой сервер", "fetch", "Чистые функции"],
  caption: [
    "Каждый тест запускает сервер на порту 0 и закрывает его в конце",
    "Обычный fetch проверяет настоящие коды, заголовки и тело",
    "Логику без сети — разбор путей, проверку данных — проверяют чистыми функциями",
  ],
  frames: [
    [jc("c", 10, 14, ["const server = createApp().listen(0);", "const { port } = server.address();", "// … тест …", "server.close();"], [0, 3], { ...code, lh: 18, size: 9.5 })],
    [jc("c", 10, 20, ["const res = await fetch(`http://127.0.0.1:${port}/users/1`);", "console.log(res.status, await res.json());"], [0, 1], { ...code, lh: 22, size: 9 })],
    [Box("a", 90, 70, 150, 36, "matchRoute(шаблон, путь)", "b", { size: 8.5 }), Box("b", 270, 70, 150, 36, "без сокетов: быстро и точно", "g", { size: 9 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Основа", "Надёжность", "Дальше"],
  caption: [
    "Обработчик, маршрутизатор, middleware, единый формат ответов и ошибок",
    "Пределы, таймауты, защита пути, тесты на порту 0; для фронтенда сервер — контракт",
    "Следующая тема — другие среды выполнения: Deno и Bun",
  ],
  frames: [
    [Box("a", 65, 60, 110, 28, "маршруты", "g", { size: 10 }), Box("b", 180, 60, 110, 28, "middleware", "g", { size: 10 }), Box("c", 295, 60, 110, 28, "JSON + коды", "g", { size: 10 })],
    [Box("a", 65, 60, 110, 28, "лимиты", "b", { size: 10 }), Box("b", 180, 60, 110, 28, "защита пути", "b", { size: 10 }), Box("c", 295, 60, 110, 28, "тесты", "b", { size: 10 })],
    [Box("a", 90, 70, 110, 36, "Node", "b", { size: 12 }), Box("b", 220, 70, 80, 36, "Deno", "g", { size: 12 }), Box("c", 320, 70, 70, 36, "Bun", "g", { size: 12 })],
  ],
});
