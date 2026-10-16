"""Задачи книги «Современный Frontend»: глава 22."""

TASKS: dict[int, list[dict]] = {22: [{'id': 'j22-parse-query',
  'mode': 'js',
  'title': 'Разбор строки запроса',
  'statement': 'Напишите parseQuery(qs): qs — строка запроса без «?». Пары разделены «&», внутри '
               'пары «ключ=значение»; значения декодируются (%XX и «+» как пробел). Повторяющиеся '
               'ключи собираются в массив в порядке появления; ключ без «=» даёт пустую строку; '
               'пустые части («&&») пропускаются. Результат — обычный объект.',
  'starter': 'function parseQuery(qs) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (x) => console.log(JSON.stringify(x));\n'
            'show(parseQuery("a=1&b=2"));\n'
            'show(parseQuery("tag=x&tag=y&tag=z"));\n'
            'show(parseQuery("q=hello+world&r=%D0%B0%D0%B1"));\n'
            'show(parseQuery("flag&x=&&y=1"));\n'
            'show(parseQuery(""));\n'
            'show(parseQuery("k=1&k=2&k=3&z=0"));\n',
  'hint': 'URLSearchParams умеет декодирование; повторы собирайте вручную: если ключ уже есть — '
          'превратите в массив.',
  'expected': ['{"a":"1","b":"2"}',
               '{"tag":["x","y","z"]}',
               '{"q":"hello world","r":"аб"}',
               '{"flag":"","x":"","y":"1"}',
               '{}',
               '{"k":["1","2","3"],"z":"0"}']},
 {'id': 'j22-match-route',
  'mode': 'js',
  'title': 'Шаблон пути с параметрами',
  'statement': 'Напишите matchRoute(pattern, path): шаблон из сегментов через «/», сегмент вида '
               '«:name» захватывает значение (декодируйте decodeURIComponent). Число сегментов '
               'должно совпадать; завершающий «/» игнорируется, пустые сегменты по краям тоже. '
               'Результат — объект параметров или null. Если последний сегмент шаблона «*», он '
               'захватывает весь непустой остаток пути (в виде строки с «/») под ключом «*»; если '
               'остатка нет — null.',
  'starter': 'function matchRoute(pattern, path) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (x) => console.log(JSON.stringify(x));\n'
            'show(matchRoute("/users/:id", "/users/42"));\n'
            'show(matchRoute("/users/:id", "/users/42/"));\n'
            'show(matchRoute("/users/:id", "/users"));\n'
            'show(matchRoute("/users/:id/posts/:pid", "/users/7/posts/a%20b"));\n'
            'show(matchRoute("/a/b", "/a/b"));\n'
            'show(matchRoute("/a/b", "/a/c"));\n'
            'show(matchRoute("/files/*", "/files/x/y/z.txt"));\n'
            'show(matchRoute("/files/*", "/files"));\n'
            'show(matchRoute("/", "/"));\n',
  'hint': 'Разбейте оба пути на сегменты (filter(Boolean)); сравнивайте по очереди; «*» забирает '
          'остаток.',
  'expected': ['{"id":"42"}',
               '{"id":"42"}',
               'null',
               '{"id":"7","pid":"a b"}',
               '{}',
               'null',
               '{"*":"x/y/z.txt"}',
               'null',
               '{}']},
 {'id': 'j22-router',
  'mode': 'js',
  'title': 'Маршрутизатор: найти обработчик',
  'statement': 'Напишите createRouter() с методами add(method, pattern, handler) и find(method, '
               'path). Шаблоны — как в «:id» (число сегментов равно, завершающий «/» '
               'игнорируется). find возвращает { handler, params } для первого подходящего '
               'маршрута (в порядке добавления; метод сравнивается без учёта регистра). Если ни '
               'один путь не подошёл — { status: 404 }. Если путь подошёл, но не для этого метода '
               '— { status: 405, allow } (allow — отсортированный массив уникальных методов в '
               'верхнем регистре).',
  'starter': 'function createRouter() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const r = createRouter();\n'
            'const h = (n) => () => n;\n'
            'r.add("GET", "/users", h("list"));\n'
            'r.add("post", "/users", h("create"));\n'
            'r.add("GET", "/users/:id", h("get"));\n'
            'r.add("DELETE", "/users/:id", h("del"));\n'
            'const show = (m, p) => { const x = r.find(m, p); console.log(m, p, x.handler ? '
            'x.handler() + " " + JSON.stringify(x.params) : JSON.stringify(x)); };\n'
            'show("GET", "/users"); show("POST", "/users/"); show("get", "/users/5"); '
            'show("DELETE", "/users/5");\n'
            'show("PUT", "/users"); show("PATCH", "/users/9"); show("GET", "/nope"); show("GET", '
            '"/users/1/x");\n',
  'hint': 'Храните маршруты массивом; для 405 соберите методы всех маршрутов с совпавшим путём.',
  'expected': ['GET /users list {}',
               'POST /users/ create {}',
               'get /users/5 get {"id":"5"}',
               'DELETE /users/5 del {"id":"5"}',
               'PUT /users {"status":405,"allow":["GET","POST"]}',
               'PATCH /users/9 {"status":405,"allow":["DELETE","GET"]}',
               'GET /nope {"status":404}',
               'GET /users/1/x {"status":404}']},
 {'id': 'j22-compose',
  'mode': 'js',
  'title': 'compose для middleware',
  'statement': 'Напишите compose(middlewares): возвращает async-функцию run(ctx). Каждый '
               'middleware вызывается как mw(ctx, next); next() запускает следующий и возвращает '
               'промис его завершения; после последнего middleware next() просто завершается. Если '
               "middleware вызвал next() дважды, второй вызов должен отклониться с Error('next() "
               "called multiple times'). run возвращает промис, который завершается после всей "
               'цепочки (в порядке «луковицы»).',
  'starter': 'function compose(middlewares) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const log = [];\n'
            'const a = async (ctx, next) => { log.push("a1"); await next(); log.push("a2"); };\n'
            'const b = async (ctx, next) => { log.push("b1"); await next(); log.push("b2"); };\n'
            'const c = async (ctx) => { log.push("c"); ctx.done = true; };\n'
            'const ctx = {};\n'
            'await compose([a, b, c])(ctx);\n'
            'console.log(log.join(" "), ctx.done);\n'
            'const stop = async () => { log.push("stop"); };\n'
            'log.length = 0;\n'
            'await compose([a, stop, b, c])({});\n'
            'console.log(log.join(" "));\n'
            'const twice = async (ctx, next) => { await next(); await next(); };\n'
            'try { await compose([twice, c])({}); } catch (e) { console.log(e.message); }\n'
            'console.log(await compose([])({}));\n',
  'hint': 'Рекурсивная функция dispatch(i): запоминайте максимальный i, чтобы поймать повторный '
          'вызов.',
  'expected': ['a1 b1 c b2 a2 true', 'a1 stop a2', 'next() called multiple times', 'undefined']},
 {'id': 'j22-safe-handler',
  'mode': 'js',
  'title': 'Безопасный обработчик',
  'statement': 'Напишите safeHandler(handler, onError): возвращает async-функцию (...args). Она '
               'вызывает handler(...args) и возвращает его результат (если результат — промис, '
               'дожидается). Если handler бросил исключение синхронно или вернул отклонённый '
               'промис, вызывается onError(err, ...args), и результат onError становится '
               'результатом.',
  'starter': 'function safeHandler(handler, onError) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const onError = (e, x) => "err:" + e.message + ":" + x;\n'
            'const ok = safeHandler((x) => x * 2, onError);\n'
            'const sync = safeHandler((x) => { throw new Error("boom"); }, onError);\n'
            'const asy = safeHandler(async (x) => { await null; throw new Error("late"); }, '
            'onError);\n'
            'const asyOk = safeHandler(async (x) => { await null; return x + 1; }, onError);\n'
            'console.log(await ok(4), await sync(1), await asy(2), await asyOk(3));\n'
            'console.log(ok(1) instanceof Promise);\n',
  'hint': 'async-функция с try/catch и await вокруг вызова handler ловит и синхронные, и '
          'асинхронные ошибки.',
  'expected': ['8 err:boom:1 err:late:2 4', 'true']},
 {'id': 'j22-read-body',
  'mode': 'js',
  'title': 'Чтение тела с пределом',
  'statement': 'Напишите readBody(chunks, limit): chunks — массив строк или Buffer-ов (куски '
               'тела), limit — максимум байт (UTF-8). Читайте куски по порядку и суммируйте байты. '
               'Если сумма стала больше limit — немедленно остановитесь и верните { ok: false, '
               'status: 413, consumed } (consumed — число прочитанных кусков, включая тот, на '
               'котором превысили). Иначе — { ok: true, text, bytes }, где text — склеенная строка '
               'UTF-8.',
  'starter': 'function readBody(chunks, limit) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (x) => console.log(JSON.stringify(x));\n'
            'show(readBody(["{\\"a\\":", "1}"], 100));\n'
            'show(readBody([Buffer.from("абв"), "г"], 100));\n'
            'show(readBody(["12345", "678", "9"], 8));\n'
            'show(readBody(["12345", "678", "9"], 9));\n'
            'show(readBody(["1234567890"], 5));\n'
            'show(readBody([], 0));\n'
            'show(readBody(["я"], 1));\n',
  'hint': 'Приведите всё к Buffer (Buffer.from(chunk)); накапливайте массив и счётчик байт.',
  'expected': ['{"ok":true,"text":"{\\"a\\":1}","bytes":7}',
               '{"ok":true,"text":"абвг","bytes":8}',
               '{"ok":false,"status":413,"consumed":3}',
               '{"ok":true,"text":"123456789","bytes":9}',
               '{"ok":false,"status":413,"consumed":1}',
               '{"ok":true,"text":"","bytes":0}',
               '{"ok":false,"status":413,"consumed":1}']},
 {'id': 'j22-parse-json',
  'mode': 'js',
  'title': 'Разбор JSON-тела',
  'statement': 'Напишите parseJsonBody(text, contentType). Если contentType не начинается с '
               'application/json (без учёта регистра; допустимы параметры после «;»), верните { '
               'ok: false, status: 415 }. Пустое тело (или только пробелы) — { ok: false, status: '
               "400, message: 'empty' }. Некорректный JSON — { ok: false, status: 400, message: "
               "'invalid json' }. Иначе — { ok: true, value }.",
  'starter': 'function parseJsonBody(text, contentType) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (x) => console.log(JSON.stringify(x));\n'
            'show(parseJsonBody(\'{"a":1}\', "application/json"));\n'
            'show(parseJsonBody(\'[1,2]\', "Application/JSON; charset=utf-8"));\n'
            'show(parseJsonBody(\'{"a":1}\', "text/plain"));\n'
            'show(parseJsonBody(\'{"a":1}\', undefined));\n'
            'show(parseJsonBody("   ", "application/json"));\n'
            'show(parseJsonBody("", "application/json"));\n'
            'show(parseJsonBody("{oops", "application/json"));\n'
            'show(parseJsonBody("null", "application/json"));\n',
  'hint': 'Сначала проверьте тип, затем пустоту, затем try/catch вокруг JSON.parse.',
  'expected': ['{"ok":true,"value":{"a":1}}',
               '{"ok":true,"value":[1,2]}',
               '{"ok":false,"status":415}',
               '{"ok":false,"status":415}',
               '{"ok":false,"status":400,"message":"empty"}',
               '{"ok":false,"status":400,"message":"empty"}',
               '{"ok":false,"status":400,"message":"invalid json"}',
               '{"ok":true,"value":null}']},
 {'id': 'j22-status-text',
  'mode': 'js',
  'title': 'Текст кода состояния',
  'statement': 'Напишите statusText(code): 200 OK, 201 Created, 204 No Content, 301 Moved '
               'Permanently, 302 Found, 304 Not Modified, 400 Bad Request, 401 Unauthorized, 403 '
               'Forbidden, 404 Not Found, 405 Method Not Allowed, 409 Conflict, 413 Payload Too '
               'Large, 415 Unsupported Media Type, 422 Unprocessable Content, 429 Too Many '
               'Requests, 500 Internal Server Error, 503 Service Unavailable. Для других кодов — '
               'по классу: 1xx «Informational», 2xx «Success», 3xx «Redirection», 4xx «Client '
               'Error», 5xx «Server Error»; вне 100–599 или не целое — «Unknown».',
  'starter': 'function statusText(code) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log([200, 201, 204, 304, 404, 405, 413, 422, 429, '
            '503].map(statusText).join("|"));\n'
            'console.log([226, 307, 418, 599, 102, 99, 600, 200.5, NaN, '
            '"200"].map(statusText).join("|"));\n',
  'hint': 'Объект-таблица для известных кодов и запасной вариант по Math.floor(code / 100).',
  'expected': ['OK|Created|No Content|Not Modified|Not Found|Method Not Allowed|Payload Too '
               'Large|Unprocessable Content|Too Many Requests|Service Unavailable',
               'Success|Redirection|Client Error|Server '
               'Error|Informational|Unknown|Unknown|Unknown|Unknown|Unknown']},
 {'id': 'j22-paginate',
  'mode': 'js',
  'title': 'Пагинация списка',
  'statement': 'Напишите paginate(items, { page, perPage }, base). По умолчанию page = 1, perPage '
               '= 10; page приводится к целому ≥ 1, perPage — к целому в диапазоне 1…100 (нечисла '
               '— значения по умолчанию). Результат: { data, meta: { total, page, perPage, pages '
               '}, links: { next, prev } }. pages = max(1, ceil(total / perPage)). Если page '
               'больше pages — data пустой массив, page остаётся как есть. links.next/prev — '
               'строки `${base}?page=N&per_page=P` либо null, если страницы нет (prev — при page > '
               '1; next — при page < pages).',
  'starter': 'function paginate(items, opts, base) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const items = Array.from({ length: 25 }, (_, i) => i + 1);\n'
            'const show = (x) => console.log(JSON.stringify(x));\n'
            'show(paginate(items, {}, "/n"));\n'
            'show(paginate(items, { page: 3, perPage: 10 }, "/n"));\n'
            'show(paginate(items, { page: 2, perPage: 10 }, "/n"));\n'
            'show(paginate(items, { page: 9, perPage: 10 }, "/n"));\n'
            'show(paginate(items, { page: "x", perPage: 1000 }, "/n"));\n'
            'show(paginate(items, { page: 0, perPage: 0 }, "/n"));\n'
            'show(paginate([], { page: 1 }, "/e"));\n',
  'hint': 'Сначала нормализуйте page и perPage, затем slice((page - 1) * perPage, page * perPage).',
  'expected': ['{"data":[1,2,3,4,5,6,7,8,9,10],"meta":{"total":25,"page":1,"perPage":10,"pages":3},"links":{"next":"/n?page=2&per_page=10","prev":null}}',
               '{"data":[21,22,23,24,25],"meta":{"total":25,"page":3,"perPage":10,"pages":3},"links":{"next":null,"prev":"/n?page=2&per_page=10"}}',
               '{"data":[11,12,13,14,15,16,17,18,19,20],"meta":{"total":25,"page":2,"perPage":10,"pages":3},"links":{"next":"/n?page=3&per_page=10","prev":"/n?page=1&per_page=10"}}',
               '{"data":[],"meta":{"total":25,"page":9,"perPage":10,"pages":3},"links":{"next":null,"prev":"/n?page=8&per_page=10"}}',
               '{"data":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],"meta":{"total":25,"page":1,"perPage":100,"pages":1},"links":{"next":null,"prev":null}}',
               '{"data":[1],"meta":{"total":25,"page":1,"perPage":1,"pages":25},"links":{"next":"/n?page=2&per_page=1","prev":null}}',
               '{"data":[],"meta":{"total":0,"page":1,"perPage":10,"pages":1},"links":{"next":null,"prev":null}}']},
 {'id': 'j22-cookies',
  'mode': 'js',
  'title': 'Cookie: разбор и запись',
  'statement': 'Напишите parseCookies(header) и serializeCookie(name, value, opts). parseCookies: '
               'пары «имя=значение» через «; », значение декодируется decodeURIComponent; пары без '
               '«=» и с пустым именем пропускаются; при повторе имени побеждает первое; пустой или '
               'отсутствующий заголовок → {}. serializeCookie: «name=encodeURIComponent(value)», '
               'затем в порядке: «; Max-Age=N» (если задан opts.maxAge), «; Path=P», «; HttpOnly», '
               '«; Secure», «; SameSite=S» — только для заданных опций.',
  'starter': 'function parseCookies(header) {\n'
             '}\n'
             'function serializeCookie(name, value, opts = {}) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (x) => console.log(JSON.stringify(x));\n'
            'show(parseCookies("a=1; b=%D0%B0; c"));\n'
            'show(parseCookies("a=1; a=2"));\n'
            'show(parseCookies(""));\n'
            'show(parseCookies(undefined));\n'
            'show(parseCookies("=x; y=z"));\n'
            'console.log(serializeCookie("sid", "a b", {}));\n'
            'console.log(serializeCookie("sid", "x", { maxAge: 3600, path: "/", httpOnly: true, '
            'secure: true, sameSite: "Lax" }));\n'
            'console.log(serializeCookie("t", "1", { sameSite: "Strict", path: "/api" }));\n'
            'console.log(serializeCookie("k", "я", { maxAge: 0 }));\n',
  'hint': "split(';'), trim, indexOf('='); при сборке добавляйте части по порядку.",
  'expected': ['{"a":"1","b":"а"}',
               '{"a":"1"}',
               '{}',
               '{}',
               '{"y":"z"}',
               'sid=a%20b',
               'sid=x; Max-Age=3600; Path=/; HttpOnly; Secure; SameSite=Lax',
               't=1; Path=/api; SameSite=Strict',
               'k=%D1%8F; Max-Age=0']},
 {'id': 'j22-cors',
  'mode': 'js',
  'title': 'Заголовки CORS',
  'statement': 'Напишите corsHeaders({ origin, method, requestHeaders }, allow). allow — массив '
               'разрешённых origin. Если origin не указан или не в списке — {}. Иначе: { '
               "'Access-Control-Allow-Origin': origin, 'Vary': 'Origin' }. Для method = 'OPTIONS' "
               "(preflight) добавьте ещё 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE', "
               "'Access-Control-Allow-Headers': значение requestHeaders, если оно есть, иначе "
               "'Content-Type', и 'Access-Control-Max-Age': '600'.",
  'starter': 'function corsHeaders(req, allow) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const allow = ["https://a.example", "https://b.example"];\n'
            'const show = (x) => console.log(JSON.stringify(x));\n'
            'show(corsHeaders({ origin: "https://a.example", method: "GET" }, allow));\n'
            'show(corsHeaders({ origin: "https://evil.example", method: "GET" }, allow));\n'
            'show(corsHeaders({ method: "GET" }, allow));\n'
            'show(corsHeaders({ origin: "https://b.example", method: "OPTIONS", requestHeaders: '
            '"x-token, content-type" }, allow));\n'
            'show(corsHeaders({ origin: "https://b.example", method: "OPTIONS" }, allow));\n'
            'show(corsHeaders({ origin: "https://b.example", method: "OPTIONS" }, []));\n',
  'hint': 'Соберите объект поэтапно; ключи сохраняйте в указанном порядке.',
  'expected': ['{"Access-Control-Allow-Origin":"https://a.example","Vary":"Origin"}',
               '{}',
               '{}',
               '{"Access-Control-Allow-Origin":"https://b.example","Vary":"Origin","Access-Control-Allow-Methods":"GET, '
               'POST, PUT, DELETE","Access-Control-Allow-Headers":"x-token, '
               'content-type","Access-Control-Max-Age":"600"}',
               '{"Access-Control-Allow-Origin":"https://b.example","Vary":"Origin","Access-Control-Allow-Methods":"GET, '
               'POST, PUT, '
               'DELETE","Access-Control-Allow-Headers":"Content-Type","Access-Control-Max-Age":"600"}',
               '{}']},
 {'id': 'j22-etag',
  'mode': 'js',
  'title': 'ETag по содержимому',
  'statement': 'Напишите makeEtag(body): тело — строка. Вычислите 32-битный хеш FNV-1a по байтам '
               'UTF-8 (начальное значение 0x811c9dc5, на каждый байт: h ^= byte, затем h = '
               'Math.imul(h, 0x01000193) >>> 0). Результат — строка в двойных кавычках: «"» + хеш '
               'из 8 hex-цифр (строчные, с ведущими нулями) + «-» + длина тела в байтах в hex + '
               '«"».',
  'starter': 'function makeEtag(body) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(makeEtag(""));\n'
            'console.log(makeEtag("a"));\n'
            'console.log(makeEtag("hello world"));\n'
            'console.log(makeEtag("Привет"));\n'
            'console.log(makeEtag("x".repeat(300)));\n'
            'console.log(makeEtag("a") === makeEtag("a"), makeEtag("a") === makeEtag("b"));\n',
  'hint': "Buffer.from(body) даёт байты UTF-8; padStart(8, '0') для хеша.",
  'expected': ['"811c9dc5-0"',
               '"e40c292c-1"',
               '"d58b3fa7-b"',
               '"33db115f-c"',
               '"970138f5-12c"',
               'true false']},
 {'id': 'j22-not-modified',
  'mode': 'js',
  'title': 'Условные запросы: 304',
  'statement': 'Напишите notModified(etag, ifNoneMatch): вернёт true, если сервер должен ответить '
               '304. ifNoneMatch — значение заголовка If-None-Match (или undefined): список etag '
               'через запятую (с пробелами или без), «*» совпадает с любым etag. Префикс слабого '
               'сравнения «W/» перед etag игнорируется с обеих сторон. Нет заголовка или пустой — '
               'false.',
  'starter': 'function notModified(etag, ifNoneMatch) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const e = \'"abc"\';\n'
            'console.log([\n'
            '  notModified(e, \'"abc"\'), notModified(e, \'W/"abc"\'), notModified(\'W/"abc"\', '
            '\'"abc"\'),\n'
            '  notModified(e, \'"x", "abc"\'), notModified(e, \'"x","y"\'), notModified(e, "*"),\n'
            '  notModified(e, undefined), notModified(e, ""), notModified(e, \'  "abc"  \'),\n'
            '].join(" "));\n',
  'hint': 'Разбейте по запятым, обрежьте пробелы, уберите ведущий W/ и сравните.',
  'expected': ['true true true true false true false false true']},
 {'id': 'j22-rate-limit',
  'mode': 'js',
  'title': 'Ограничение частоты (фиксированное окно)',
  'statement': 'Напишите createLimiter(max, windowMs): функцию-проверку allow(key, now). Окно '
               'ключа начинается с первого запроса и длится windowMs мс ([start, start + '
               'windowMs)). Внутри окна первые max запросов разрешены. Результат — { allowed, '
               'remaining, resetMs }: remaining — сколько запросов ещё можно (после этого), '
               'resetMs — сколько мс осталось до конца окна. Когда окно закончилось (now ≥ start + '
               'windowMs), следующий запрос открывает новое окно. Ключи независимы.',
  'starter': 'function createLimiter(max, windowMs) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const allow = createLimiter(2, 1000);\n'
            'const show = (r) => console.log(JSON.stringify(r));\n'
            'show(allow("a", 0)); show(allow("a", 100)); show(allow("a", 200)); show(allow("b", '
            '300));\n'
            'show(allow("a", 999)); show(allow("a", 1000)); show(allow("a", 1500)); '
            'show(allow("a", 2100));\n',
  'hint': 'Map: key → { start, count }; при now - start >= windowMs начинайте новое окно.',
  'expected': ['{"allowed":true,"remaining":1,"resetMs":1000}',
               '{"allowed":true,"remaining":0,"resetMs":900}',
               '{"allowed":false,"remaining":0,"resetMs":800}',
               '{"allowed":true,"remaining":1,"resetMs":1000}',
               '{"allowed":false,"remaining":0,"resetMs":1}',
               '{"allowed":true,"remaining":1,"resetMs":1000}',
               '{"allowed":true,"remaining":0,"resetMs":500}',
               '{"allowed":true,"remaining":1,"resetMs":1000}']},
 {'id': 'j22-bearer',
  'mode': 'js',
  'title': 'Проверка Bearer-токена',
  'statement': 'Напишите bearerAuth(header, tokens): tokens — объект «токен → пользователь». Нет '
               "заголовка — { ok: false, status: 401, reason: 'missing' }. Схема не Bearer (без "
               "учёта регистра) или после неё нет ровно одного токена — reason 'malformed'. Токена "
               "нет в tokens — reason 'invalid'. Иначе — { ok: true, user }.",
  'starter': 'function bearerAuth(header, tokens) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const tokens = { t1: "ann", t2: "bob" };\n'
            'const show = (h) => console.log(JSON.stringify(bearerAuth(h, tokens)));\n'
            'show("Bearer t1"); show("bearer t2"); show(undefined); show("");\n'
            'show("Basic t1"); show("Bearer"); show("Bearer t1 t2"); show("Bearer nope"); '
            'show("Bearer toString");\n',
  'hint': 'split(/\\s+/), сравните схему в нижнем регистре, затем Object.hasOwn(tokens, token).',
  'expected': ['{"ok":true,"user":"ann"}',
               '{"ok":true,"user":"bob"}',
               '{"ok":false,"status":401,"reason":"missing"}',
               '{"ok":false,"status":401,"reason":"missing"}',
               '{"ok":false,"status":401,"reason":"malformed"}',
               '{"ok":false,"status":401,"reason":"malformed"}',
               '{"ok":false,"status":401,"reason":"malformed"}',
               '{"ok":false,"status":401,"reason":"invalid"}',
               '{"ok":false,"status":401,"reason":"invalid"}']},
 {'id': 'j22-validate',
  'mode': 'js',
  'title': 'Проверка входных данных',
  'statement': 'Напишите validate(schema, obj): schema — объект «поле → правила» ({ type: '
               "'string'|'number'|'boolean', required, min, max, integer }). Верните массив "
               'строк-ошибок, отсортированный по имени поля (для одного поля — не больше одной '
               'ошибки, проверяются по порядку): «поле: required» (поля нет или null/undefined, а '
               'required: true); если поля нет и не required — пропуск; «поле: must be тип»; для '
               'number при integer: true — «поле: must be integer»; min/max для string — длина, '
               'для number — значение: «поле: too small» (меньше min) / «поле: too large» (больше '
               'max). Лишние поля игнорируются.',
  'starter': 'function validate(schema, obj) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const schema = {\n'
            '  name: { type: "string", required: true, min: 2, max: 5 },\n'
            '  age: { type: "number", integer: true, min: 0, max: 150 },\n'
            '  vip: { type: "boolean" },\n'
            '};\n'
            'const show = (o) => console.log(JSON.stringify(validate(schema, o)));\n'
            'show({ name: "Ann", age: 30, vip: true }); show({}); show({ name: "A" }); show({ '
            'name: "Alexander" });\n'
            'show({ name: 5, age: "x", vip: "yes" }); show({ name: "Bob", age: 3.5 }); show({ '
            'name: "Bob", age: -1 }); show({ name: "Bob", age: 200 });\n'
            'show({ name: "Bob", age: null, extra: 1 });\n',
  'hint': 'Пройдите по отсортированным ключам schema; для string min/max сравнивайте length.',
  'expected': ['[]',
               '["name: required"]',
               '["name: too small"]',
               '["name: too large"]',
               '["age: must be number","name: must be string","vip: must be boolean"]',
               '["age: must be integer"]',
               '["age: too small"]',
               '["age: too large"]',
               '[]']},
 {'id': 'j22-safe-join',
  'mode': 'js',
  'title': 'Защита от выхода из каталога',
  'statement': 'Напишите safeJoin(root, urlPath) (используйте node:path/posix): urlPath — путь из '
               'адреса запроса, возможно с %XX. Декодируйте его (decodeURIComponent; при ошибке '
               'декодирования — null), отвергайте нулевой байт (null), склейте с root и '
               'нормализуйте. Результат — абсолютный путь внутри root (равный root или '
               'начинающийся с root + «/»), иначе null. root — абсолютный путь без завершающего '
               '«/».',
  'starter': 'import path from "node:path/posix";\nfunction safeJoin(root, urlPath) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const root = "/srv/public";\n'
            'for (const p of ["/index.html", "/a/b.txt", "/", "/../etc/passwd", "/a/../../x", '
            '"/%2e%2e/secret", "/a/%2e%2e/b", "/ok/..", "/x%00y", "/%E0%A4%A", "/a//b", '
            '"/../public-evil/x"])\n'
            '  console.log(JSON.stringify(p), safeJoin(root, p));\n',
  'hint': "path.resolve(root, '.' + p) и проверка full === root || full.startsWith(root + '/').",
  'expected': ['"/index.html" /srv/public/index.html',
               '"/a/b.txt" /srv/public/a/b.txt',
               '"/" /srv/public',
               '"/../etc/passwd" null',
               '"/a/../../x" null',
               '"/%2e%2e/secret" null',
               '"/a/%2e%2e/b" /srv/public/b',
               '"/ok/.." /srv/public',
               '"/x%00y" null',
               '"/%E0%A4%A" null',
               '"/a//b" /srv/public/a/b',
               '"/../public-evil/x" null']},
 {'id': 'j22-mime',
  'mode': 'js',
  'title': 'Тип содержимого по расширению',
  'statement': 'Напишите mimeType(filename): расширение — после последней точки в последнем '
               'сегменте имени, без учёта регистра. Таблица: html → text/html, css → text/css, js '
               'и mjs → text/javascript, json → application/json, txt → text/plain, png → '
               'image/png, jpg и jpeg → image/jpeg, svg → image/svg+xml. Для text/* и '
               'application/json добавьте «; charset=utf-8». Нет расширения или оно неизвестно — '
               'application/octet-stream. Имя, начинающееся с точки и без других точек (.env), '
               'расширения не имеет.',
  'starter': 'function mimeType(filename) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'for (const f of ["index.html", "a/b/style.CSS", "app.mjs", "data.json", "readme.txt", '
            '"pic.PNG", "p.jpeg", "x.jpg", "logo.svg", "archive.tar.gz", "noext", ".env", '
            '"dir.v2/file", "a.b/c.html", "end."])\n'
            '  console.log(f, mimeType(f));\n',
  'hint': "Возьмите basename, найдите lastIndexOf('.'); индекс 0 или -1 — нет расширения.",
  'expected': ['index.html text/html; charset=utf-8',
               'a/b/style.CSS text/css; charset=utf-8',
               'app.mjs text/javascript; charset=utf-8',
               'data.json application/json; charset=utf-8',
               'readme.txt text/plain; charset=utf-8',
               'pic.PNG image/png',
               'p.jpeg image/jpeg',
               'x.jpg image/jpeg',
               'logo.svg image/svg+xml',
               'archive.tar.gz application/octet-stream',
               'noext application/octet-stream',
               '.env application/octet-stream',
               'dir.v2/file application/octet-stream',
               'a.b/c.html text/html; charset=utf-8',
               'end. application/octet-stream']},
 {'id': 'j22-range',
  'mode': 'js',
  'title': 'Заголовок Range',
  'statement': 'Напишите parseRange(header, size): поддерживается один диапазон вида «bytes=a-b», '
               '«bytes=a-» или «bytes=-n» (последние n байт). Результат — { start, end } '
               '(включительно, end не больше size − 1). Заголовок отсутствует, не начинается с '
               '«bytes=» или содержит несколько диапазонов (запятую) — null (игнорировать). '
               'Диапазон разобран, но не может быть удовлетворён (start ≥ size, start > end, n = '
               '0, size = 0) — { status: 416 }.',
  'starter': 'function parseRange(header, size) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (h, s = 1000) => console.log(h, JSON.stringify(parseRange(h, s)));\n'
            'show("bytes=0-499"); show("bytes=500-"); show("bytes=-200"); show("bytes=0-0"); '
            'show("bytes=900-5000");\n'
            'show("bytes=1000-"); show("bytes=-0"); show("bytes=-5000"); show("bytes=5-2"); '
            'show("bytes=0-1,5-9");\n'
            'show(undefined); show("items=0-5"); show("bytes=abc"); show("bytes=0-10", 0);\n',
  'hint': 'Разберите регулярным выражением /^bytes=(\\d*)-(\\d*)$/; суффикс -n: start = max(0, '
          'size - n).',
  'expected': ['bytes=0-499 {"start":0,"end":499}',
               'bytes=500- {"start":500,"end":999}',
               'bytes=-200 {"start":800,"end":999}',
               'bytes=0-0 {"start":0,"end":0}',
               'bytes=900-5000 {"start":900,"end":999}',
               'bytes=1000- {"status":416}',
               'bytes=-0 {"status":416}',
               'bytes=-5000 {"start":0,"end":999}',
               'bytes=5-2 {"status":416}',
               'bytes=0-1,5-9 null',
               'undefined null',
               'items=0-5 null',
               'bytes=abc null',
               'bytes=0-10 {"status":416}']},
 {'id': 'j22-encoding',
  'mode': 'js',
  'title': 'Выбор сжатия',
  'statement': "Напишите chooseEncoding(acceptEncoding, supported = ['br', 'gzip']). Разберите "
               'заголовок: элементы через запятую, у каждого необязательный «;q=число» (по '
               'умолчанию 1), имя без учёта регистра, «*» — любое. Кодировки с q = 0 запрещены. '
               'Выберите поддерживаемую кодировку с наибольшим q (при равенстве — раньше в '
               'supported); «*» даёт q остальным поддерживаемым, не упомянутым явно. Если '
               "подходящей нет — 'identity'. Нет заголовка — 'identity'.",
  'starter': 'function chooseEncoding(acceptEncoding, supported = ["br", "gzip"]) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const c = (h, s) => console.log(JSON.stringify(h), chooseEncoding(h, s));\n'
            'c("gzip, br"); c("gzip;q=0.5, br;q=0.8"); c("gzip;q=1.0, br;q=0.5"); c("*"); '
            'c("identity"); c("br;q=0, gzip"); c("GZIP"); c(undefined); c("");\n'
            'c("deflate"); c("*;q=0, gzip;q=0.1"); c("gzip;q=0.5, *;q=0.9"); c("br, gzip", '
            '["gzip"]); c("gzip;q=0.7, br;q=0.7");\n',
  'hint': 'Соберите Map имя → q; для каждой поддерживаемой кодировки возьмите её q или q от «*».',
  'expected': ['"gzip, br" br',
               '"gzip;q=0.5, br;q=0.8" br',
               '"gzip;q=1.0, br;q=0.5" gzip',
               '"*" br',
               '"identity" identity',
               '"br;q=0, gzip" gzip',
               '"GZIP" gzip',
               'undefined identity',
               '"" identity',
               '"deflate" identity',
               '"*;q=0, gzip;q=0.1" gzip',
               '"gzip;q=0.5, *;q=0.9" br',
               '"br, gzip" gzip',
               '"gzip;q=0.7, br;q=0.7" br']},
 {'id': 'j22-request-id',
  'mode': 'js',
  'title': 'Идентификатор запроса',
  'statement': 'Напишите createRequestId(): возвращает функцию nextId(incoming). Если incoming — '
               'строка, целиком состоящая из латинских букв, цифр, «_» и «-» длиной 1…64, вернуть '
               'её как есть. Иначе — сгенерировать «req-» и порядковый номер (1, 2, 3…) из 6 цифр '
               'с ведущими нулями; номер растёт только при генерации.',
  'starter': 'function createRequestId() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const next = createRequestId();\n'
            'console.log([next(), next("abc-123"), next(), next("bad id"), next("x".repeat(65)), '
            'next(""), next(undefined), next("A_b-9"), next(123)].join(" "));\n'
            'const other = createRequestId();\n'
            'console.log(other());\n',
  'hint': 'Замыкание со счётчиком; проверка регулярным выражением /^[\\w-]{1,64}$/.',
  'expected': ['req-000001 abc-123 req-000002 req-000003 req-000004 req-000005 req-000006 A_b-9 '
               'req-000007',
               'req-000001']},
 {'id': 'j22-idempotent',
  'mode': 'js',
  'title': 'Идемпотентные запросы',
  'statement': 'Напишите createIdempotent(handler): возвращает async-функцию (key, body). '
               'handler(body) — async-функция, возвращающая ответ { status, body }. Без key '
               '(undefined или пустой) — просто вызвать handler. С key: первый вызов выполняет '
               'handler и запоминает результат вместе с телом запроса (сравнивайте через '
               'JSON.stringify); повтор с тем же key и тем же телом возвращает запомненный ответ '
               "без вызова handler; тот же key с другим телом — { status: 422, body: { error: 'key "
               "reused' } }. Параллельные вызовы с одним key и одинаковым телом должны вызвать "
               'handler один раз (запоминайте промис).',
  'starter': 'function createIdempotent(handler) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'let calls = 0;\n'
            'const run = createIdempotent(async (body) => { calls++; await null; return { status: '
            '201, body: { id: calls, ...body } }; });\n'
            'const show = (x) => console.log(JSON.stringify(x));\n'
            'show(await run("k1", { a: 1 }));\n'
            'show(await run("k1", { a: 1 }));\n'
            'show(await run("k1", { a: 2 }));\n'
            'show(await run(undefined, { a: 3 }));\n'
            'show(await run("", { a: 3 }));\n'
            'const [x, y] = await Promise.all([run("k2", { b: 1 }), run("k2", { b: 1 })]);\n'
            'show([x, y]);\n'
            'console.log("calls", calls);\n',
  'hint': 'Map: key → { bodyJson, promise }; сохраняйте промис сразу, до завершения handler.',
  'expected': ['{"status":201,"body":{"id":1,"a":1}}',
               '{"status":201,"body":{"id":1,"a":1}}',
               '{"status":422,"body":{"error":"key reused"}}',
               '{"status":201,"body":{"id":2,"a":3}}',
               '{"status":201,"body":{"id":3,"a":3}}',
               '[{"status":201,"body":{"id":4,"b":1}},{"status":201,"body":{"id":4,"b":1}}]',
               'calls 4']},
 {'id': 'j22-sort-routes',
  'mode': 'js',
  'title': 'Специфичность маршрутов',
  'statement': 'Напишите sortRoutes(patterns): вернуть новый массив шаблонов, упорядоченный по '
               'специфичности. Сравнение по сегментам слева направо: статический сегмент (например '
               'users) специфичнее параметра (:id), параметр специфичнее «*». При равенстве всех '
               'общих сегментов более длинный шаблон идёт позже; полностью равные по структуре — в '
               'исходном порядке.',
  'starter': 'function sortRoutes(patterns) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (a) => console.log(sortRoutes(a).join(" "));\n'
            'show(["/users/:id", "/users/me", "/users"]);\n'
            'show(["/*", "/a/*", "/a/b", "/:x/b", "/a/:y"]);\n'
            'show(["/a/:id/b", "/a/me/b", "/a/me/:c", "/a/me"]);\n'
            'show(["/b", "/a", "/:z", "/c"]);\n'
            'show([]);\n',
  'hint': 'Присвойте сегментам ранги 0, 1, 2 и сравните массивы рангов лексикографически; sort в '
          'Node устойчив.',
  'expected': ['/users /users/me /users/:id',
               '/a/b /a/:y /a/* /:x/b /*',
               '/a/me /a/me/b /a/me/:c /a/:id/b',
               '/b /a /c /:z']},
 {'id': 'j22-build-query',
  'mode': 'js',
  'title': 'Сборка строки запроса',
  'statement': 'Напишите buildQuery(obj): ключи сортируются по алфавиту; значение-массив даёт '
               'повторяющийся ключ (элементы в исходном порядке); значения undefined и null '
               'пропускаются (в том числе внутри массива); числа и логические приводятся к строке; '
               'ключи и значения кодируются encodeURIComponent. Результат — «a=1&b=2» без «?»; '
               'пустой объект — пустая строка.',
  'starter': 'function buildQuery(obj) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const q = (o) => console.log(JSON.stringify(buildQuery(o)));\n'
            'q({ b: 2, a: 1 }); q({ tag: ["x", "y"], page: 2 }); q({ a: undefined, b: null, c: 0, '
            'd: false });\n'
            'q({ q: "hello world", r: "а&б=в" }); q({}); q({ "k y": 1 }); q({ a: [1, null, 2, '
            'undefined] });\n',
  'hint': 'Object.keys().sort(), flatMap по значениям, encodeURIComponent(String(v)).',
  'expected': ['"a=1&b=2"',
               '"page=2&tag=x&tag=y"',
               '"c=0&d=false"',
               '"q=hello%20world&r=%D0%B0%26%D0%B1%3D%D0%B2"',
               '""',
               '"k%20y=1"',
               '"a=1&a=2"']},
 {'id': 'j22-cache-control',
  'mode': 'js',
  'title': 'Cache-Control',
  'statement': 'Напишите parseCacheControl(header) и isFresh(cc, ageSeconds). parseCacheControl: '
               'директивы через запятую (пробелы вокруг игнорируются, имена в нижнем регистре); '
               '«имя=число» → числовое значение, «имя» без значения → true; кавычки у значения '
               'снимаются, нечисловые значения остаются строками; пустой/отсутствующий → {}. '
               'isFresh: false, если есть no-store или no-cache; иначе true, если задан max-age и '
               'ageSeconds < max-age; иначе false.',
  'starter': 'function parseCacheControl(header) {\n}\nfunction isFresh(cc, ageSeconds) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (h) => console.log(JSON.stringify(parseCacheControl(h)));\n'
            'show("max-age=60, public"); show("No-Store"); show(" private ,max-age=0 "); '
            'show(\'x="abc", y=5\'); show(""); show(undefined);\n'
            'const f = (h, age) => console.log(isFresh(parseCacheControl(h), age));\n'
            'f("max-age=60", 10); f("max-age=60", 60); f("max-age=60, no-cache", 1); f("no-store, '
            'max-age=100", 1); f("public", 0); f("max-age=0", 0);\n',
  'hint': "split(','), затем разделите по первому '='; Number(...) для чисел.",
  'expected': ['{"max-age":60,"public":true}',
               '{"no-store":true}',
               '{"private":true,"max-age":0}',
               '{"x":"abc","y":5}',
               '{}',
               '{}',
               'true',
               'false',
               'false',
               'false',
               'false',
               'false']},
 {'id': 'j22-hello-server',
  'mode': 'js',
  'title': 'Первый сервер',
  'statement': 'Напишите createApp(): возвращает http.Server (не запущенный). На GET / ответьте '
               '200, тело «hello», Content-Type text/plain. На любой другой запрос — 404 и JSON '
               '{"error":"not found"} с Content-Type application/json.',
  'starter': 'import http from "node:http";\nfunction createApp() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const server = createApp();\n'
            'await new Promise((r) => server.listen(0, "127.0.0.1", r));\n'
            'const base = `http://127.0.0.1:${server.address().port}`;\n'
            'for (const [m, p] of [["GET", "/"], ["GET", "/x"], ["POST", "/"]]) {\n'
            '  const res = await fetch(base + p, { method: m });\n'
            '  console.log(m, p, res.status, res.headers.get("content-type"), JSON.stringify(await '
            'res.text()));\n'
            '}\n'
            'server.close();\n',
  'hint': 'http.createServer((req, res) => { res.writeHead(...); res.end(...); }).',
  'expected': ['GET / 200 text/plain "hello"',
               'GET /x 404 application/json "{\\"error\\":\\"not found\\"}"',
               'POST / 404 application/json "{\\"error\\":\\"not found\\"}"']},
 {'id': 'j22-echo-server',
  'mode': 'js',
  'title': 'Сервер с JSON-телом',
  'statement': 'Напишите createApp(): http.Server. POST /echo читает тело запроса (поток), '
               'разбирает JSON и отвечает 201 с JSON {"received": значение}; при некорректном JSON '
               '— 400 и {"error":"bad json"}. На /echo другим методом — 405 и заголовок Allow: '
               'POST. Другие пути — 404 (тело любое). Ответы — Content-Type application/json.',
  'starter': 'import http from "node:http";\nfunction createApp() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const server = createApp();\n'
            'await new Promise((r) => server.listen(0, "127.0.0.1", r));\n'
            'const base = `http://127.0.0.1:${server.address().port}`;\n'
            'const show = async (res) => console.log(res.status, res.headers.get("allow"), '
            'res.headers.get("content-type"), await res.text());\n'
            'await show(await fetch(base + "/echo", { method: "POST", body: JSON.stringify({ a: '
            '[1, 2] }), headers: { "content-type": "application/json" } }));\n'
            'await show(await fetch(base + "/echo", { method: "POST", body: "{oops" }));\n'
            'await show(await fetch(base + "/echo"));\n'
            'await show(await fetch(base + "/other", { method: "POST", body: "{}" }));\n'
            'server.close();\n',
  'hint': 'for await (const chunk of req) собирает тело; try/catch вокруг JSON.parse.',
  'expected': ['201 null application/json {"received":{"a":[1,2]}}',
               '400 null application/json {"error":"bad json"}',
               '405 POST application/json {"error":"method not allowed"}',
               '404 null application/json {"error":"not found"}']},
 {'id': 'j22-users-server',
  'mode': 'js',
  'title': 'Сервер с параметрами пути',
  'statement': 'Напишите createApp(users): users — объект «id → имя». GET /users — 200 и '
               'JSON-массив [{id, name}, …] в порядке ключей. GET /users/:id — 200 и {id, name}, '
               'либо 404 и {"error":"not found"}, если пользователя нет. Любой другой метод на '
               'этих путях — 405 с заголовком Allow: GET. Остальные пути — 404 с таким же JSON. '
               'Ответы — application/json.',
  'starter': 'import http from "node:http";\nfunction createApp(users) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const server = createApp({ 1: "Аня", 2: "Борис" });\n'
            'await new Promise((r) => server.listen(0, "127.0.0.1", r));\n'
            'const base = `http://127.0.0.1:${server.address().port}`;\n'
            'for (const [m, p] of [["GET", "/users"], ["GET", "/users/2"], ["GET", "/users/9"], '
            '["DELETE", "/users/1"], ["POST", "/users"], ["GET", "/nope"]]) {\n'
            '  const res = await fetch(base + p, { method: m });\n'
            '  console.log(m, p, res.status, res.headers.get("allow"), await res.text());\n'
            '}\n'
            'server.close();\n',
  'hint': "Разберите путь через new URL(req.url, 'http://x'); сегменты — split('/').",
  'expected': ['GET /users 200 null [{"id":"1","name":"Аня"},{"id":"2","name":"Борис"}]',
               'GET /users/2 200 null {"id":"2","name":"Борис"}',
               'GET /users/9 404 null {"error":"not found"}',
               'DELETE /users/1 405 GET {"error":"method not allowed"}',
               'POST /users 405 GET {"error":"method not allowed"}',
               'GET /nope 404 null {"error":"not found"}']},
 {'id': 'j22-middleware-server',
  'mode': 'js',
  'title': 'Сервер с цепочкой middleware',
  'statement': 'Напишите createApp(middlewares): http.Server, который для каждого запроса '
               'последовательно вызывает middleware вида (req, res, next). next() передаёт '
               'управление следующему; если дошли до конца цепочки и ответ ещё не отправлен — 404 '
               'с телом «not found». Если middleware бросил исключение (синхронно) или вызвал '
               'next(err) — ответить 500 с телом «error: » + сообщение ошибки. После отправки '
               'ответа цепочку продолжать не нужно.',
  'starter': 'import http from "node:http";\nfunction createApp(middlewares) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const log = [];\n'
            'const mws = [\n'
            '  (req, res, next) => { log.push("log " + req.url); next(); },\n'
            '  (req, res, next) => { if (req.url === "/secret") { res.writeHead(401); return '
            'res.end("no"); } next(); },\n'
            '  (req, res, next) => { if (req.url === "/boom") throw new Error("bang"); if (req.url '
            '=== "/err") return next(new Error("custom")); next(); },\n'
            '  (req, res, next) => { if (req.url === "/hi") { res.end("hi"); return; } next(); },\n'
            '];\n'
            'const server = createApp(mws);\n'
            'await new Promise((r) => server.listen(0, "127.0.0.1", r));\n'
            'const base = `http://127.0.0.1:${server.address().port}`;\n'
            'for (const p of ["/hi", "/secret", "/boom", "/err", "/other"]) {\n'
            '  const res = await fetch(base + p);\n'
            '  console.log(p, res.status, await res.text());\n'
            '}\n'
            'console.log(log.join(" | "));\n'
            'server.close();\n',
  'hint': 'Функция step(i, err): при err → 500; при i === length → 404; иначе mw(req, res, e => '
          'step(i + 1, e)) в try/catch.',
  'expected': ['/hi 200 hi',
               '/secret 401 no',
               '/boom 500 error: bang',
               '/err 500 error: custom',
               '/other 404 not found',
               'log /hi | log /secret | log /boom | log /err | log /other']},
 {'id': 'j22-graceful-stop',
  'mode': 'js',
  'title': 'Корректная остановка сервера',
  'statement': 'Напишите stopServer(server): возвращает промис, который завершается, когда сервер '
               'перестал принимать соединения и все запросы в обработке завершены. Новые '
               'соединения при этом принимать нельзя. Простаивающие keep-alive-соединения нужно '
               'закрыть, чтобы не ждать их таймаута. Если во время остановки возникла ошибка '
               'закрытия — отклонить промис.',
  'starter': 'function stopServer(server) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'import http from "node:http";\n'
            'const server = http.createServer(async (req, res) => {\n'
            '  await new Promise((r) => setTimeout(r, 100));\n'
            '  res.end("done");\n'
            '});\n'
            'await new Promise((r) => server.listen(0, "127.0.0.1", r));\n'
            'const port = server.address().port;\n'
            'const slow = fetch(`http://127.0.0.1:${port}/`).then((r) => r.text()).then((t) => '
            'console.log("response", t));\n'
            'await new Promise((r) => setTimeout(r, 30));\n'
            'const t0 = Date.now();\n'
            'await stopServer(server);\n'
            'console.log("stopped", Date.now() - t0 >= 40);\n'
            'await slow;\n'
            'try { await fetch(`http://127.0.0.1:${port}/`); console.log("still open"); } catch { '
            'console.log("refused"); }\n',
  'hint': 'server.close(cb) + server.closeIdleConnections(); медленный запрос завершится сам.',
  'expected': ['response done', 'stopped true', 'refused']}]}
