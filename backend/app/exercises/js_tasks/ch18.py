"""Задачи книги «Современный Frontend», глава 18 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {18: [{'id': 'j18-parse-headers',
       'mode': 'js',
       'title': 'Разбор сырых заголовков',
       'statement': 'Напишите функцию parseHeaders(raw): raw — блок заголовков, строки разделены «\\r\\n» '
                    'или «\\n»; строка «Имя: значение». Правила: имя приводится к нижнему регистру, значение '
                    'обрезается по краям; повтор имени склеивается через «, » в порядке появления, кроме '
                    'set-cookie — для него всегда массив значений (даже одно); строка, начинающаяся с '
                    'пробела или табуляции, продолжает предыдущее значение (склейка через один пробел после '
                    'обрезки); строки без двоеточия и пустые строки игнорируются; результат — обычный '
                    'объект.',
       'starter': 'function parseHeaders(raw) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'console.log(JSON.stringify(canon(parseHeaders("Content-Type: application/json\\r\\nX-Id:  '
                 '42  \\r\\nx-id: 43\\r\\nAccept: a,\\r\\n  b\\r\\n\\tc\\r\\n\\r\\nбез '
                 'двоеточия\\r\\nSet-Cookie: a=1\\r\\nSet-Cookie: b=2; Path=/\\r\\n"))));\n'
                 'console.log(JSON.stringify(parseHeaders("")), JSON.stringify(parseHeaders("set-cookie: '
                 'one")), JSON.stringify(parseHeaders("A: 1\\nA: 2\\nA: 3\\n:пусто\\n")));\n'
                 'console.log(JSON.stringify(parseHeaders("Link: <a>; rel=next, <b>; rel=prev\\nDate: Tue, '
                 '15 Nov 1994 08:12:31 GMT")));\n',
       'hint': 'Сначала склейте строки-продолжения, потом разбирайте «имя: значение»; set-cookie копите в '
               'массив.',
       'expected': ['{"accept":"a, b c","content-type":"application/json","set-cookie":["a=1","b=2; '
                    'Path=/"],"x-id":"42, 43"}',
                    '{} {"set-cookie":["one"]} {"a":"1, 2, 3"}',
                    '{"link":"<a>; rel=next, <b>; rel=prev","date":"Tue, 15 Nov 1994 08:12:31 GMT"}']},
      {'id': 'j18-headers-class',
       'mode': 'js',
       'title': 'Свой Headers',
       'statement': 'Напишите класс MyHeaders(init): init — объект, массив пар или другой MyHeaders '
                    '(необязателен). Методы: append(name, value) (повторы склеиваются через «, »; set-cookie '
                    'хранится отдельными значениями), set(name, value) (заменяет), get(name) → строка или '
                    'null, has, delete, getSetCookie() → массив, entries() → итератор пар [имя, значение] в '
                    'порядке сортировки имён по возрастанию (имена в нижнем регистре; каждое значение '
                    'set-cookie — отдельной парой), keys(), values(), forEach(cb) (cb(value, name)), '
                    '[Symbol.iterator]. Имя регистронезависимо; значения обрезаются по краям; пустое имя или '
                    'имя с пробелом — TypeError.',
       'starter': 'class MyHeaders {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const h = new MyHeaders({ "Content-Type": "text/html", "X-A": " 1 " });\n'
                 'h.append("x-a", "2"); h.append("Set-Cookie", "a=1"); h.append("set-cookie", "b=2"); '
                 'h.append("Accept", "*/*");\n'
                 'console.log(JSON.stringify([...h]), h.get("X-A"), h.get("nope"), h.get("SET-COOKIE"), '
                 'JSON.stringify(h.getSetCookie()));\n'
                 'h.set("x-a", "только"); h.set("set-cookie", "c=3"); console.log(h.get("x-a"), '
                 'JSON.stringify(h.getSetCookie()), h.has("ACCEPT"), h.has("zzz"), h.has("set-cookie"));\n'
                 'h.delete("accept"); h.delete("set-cookie"); console.log(JSON.stringify([...h.keys()]), '
                 'JSON.stringify([...h.values()]), h.has("set-cookie"));\n'
                 'const log = []; h.forEach((v, k) => log.push(`${k}=${v}`)); console.log(log.join(";"));\n'
                 'const c = new MyHeaders(h); c.append("x-a", "ещё"); console.log(c.get("x-a"), '
                 'h.get("x-a"), JSON.stringify([...new MyHeaders([["b", "2"], ["a", "1"], ["B", "3"]])]));\n'
                 'for (const bad of ["", "a b", "  "]) { try { h.get(bad); console.log("нет ошибки"); } '
                 'catch (e) { console.log(e.name); } }\n',
       'hint': 'Map имя → строка плюс отдельный массив для set-cookie; entries сортируйте по имени.',
       'expected': ['[["accept","*/*"],["content-type","text/html"],["set-cookie","a=1"],["set-cookie","b=2"],["x-a","1, '
                    '2"]] 1, 2 null a=1, b=2 ["a=1","b=2"]',
                    'только ["c=3"] true false true',
                    '["content-type","x-a"] ["text/html","только"] false',
                    'content-type=text/html;x-a=только',
                    'только, ещё только [["a","1"],["b","2, 3"]]',
                    'TypeError',
                    'TypeError',
                    'TypeError']},
      {'id': 'j18-build-url',
       'mode': 'js',
       'title': 'Сборка адреса запроса',
       'statement': 'Напишите функцию buildUrl(base, path, params): base — адрес вида «https://api.ru/v1/» '
                    '(с косой чертой или без), path — строка «/users» (с косой чертой или без) или массив '
                    'сегментов [«users», «a/b», 42] (каждый сегмент кодируется целиком, косая внутри '
                    'сегмента превращается в %2F); они соединяются ровно одной «/». params — объект: '
                    'значения null и undefined пропускаются, массив даёт повтор ключа, булевы и числа — '
                    'строки, Date — в ISO, вложенный простой объект — JSON-строкой; ключи и значения '
                    'кодируются encodeURIComponent, но пробел в значении — «%20». Если параметров нет — без '
                    '«?». Порядок параметров — как в объекте.',
       'starter': 'function buildUrl(base, path, params) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(buildUrl("https://api.ru/v1/", "/users"));\n'
                 'console.log(buildUrl("https://api.ru/v1", "users", { page: 2, q: "тест поиск", done: '
                 'false, none: null, un: undefined }));\n'
                 'console.log(buildUrl("https://api.ru", ["files", "a/b", 42, "ж"], { tag: ["x", "y z"], at: '
                 'new Date(Date.UTC(2024, 0, 2, 3, 4, 5)), f: { a: 1 } }));\n'
                 'console.log(buildUrl("https://api.ru/", "/", {}), buildUrl("http://x.ru//", "//a"), '
                 'buildUrl("http://x.ru", [], { z: 0 }));\n',
       'hint': 'Сначала соедините базу и путь одной косой чертой, затем соберите строку запроса из пар.',
       'expected': ['https://api.ru/v1/users',
                    'https://api.ru/v1/users?page=2&q=%D1%82%D0%B5%D1%81%D1%82%20%D0%BF%D0%BE%D0%B8%D1%81%D0%BA&done=false',
                    'https://api.ru/files/a%2Fb/42/%D0%B6?tag=x&tag=y%20z&at=2024-01-02T03%3A04%3A05.000Z&f=%7B%22a%22%3A1%7D',
                    'https://api.ru/ http://x.ru/a http://x.ru/?z=0']},
      {'id': 'j18-content-type',
       'mode': 'js',
       'title': 'Content-Type и вид тела',
       'statement': 'Напишите функции parseContentType(header) и bodyKind(header). parseContentType → { '
                    'type, subtype, suffix, params } или null, если значение не вида «тип/подтип»: type и '
                    'subtype в нижнем регистре, suffix — часть подтипа после последнего «+» (или null), '
                    'params — объект параметров (имена в нижнем регистре, значения без кавычек, «\\"» внутри '
                    'кавычек раскрывается; значение может содержать «;» внутри кавычек). bodyKind → «json» '
                    '(subtype json или suffix json), «form» (application/x-www-form-urlencoded), «multipart» '
                    '(type multipart), «text» (type text, subtype xml, suffix xml, javascript), «binary» '
                    '(всё остальное, в том числе некорректный заголовок и пустая строка).',
       'starter': 'function parseContentType(header) {\n}\nfunction bodyKind(header) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'for (const h of ["application/json", "Application/JSON; charset=UTF-8", '
                 '"application/vnd.api+json", "text/html;charset=utf-8", "multipart/form-data; '
                 'boundary=\\"a;b\\"; x=1", "image/svg+xml", "application/x-www-form-urlencoded", '
                 '"application/javascript", "text/plain; name=\\"a\\\\\\"b\\"", "ерунда", "", '
                 '"application/octet-stream", "application/xml"]) {\n'
                 '  console.log(JSON.stringify(h), JSON.stringify(canon(parseContentType(h))), '
                 'bodyKind(h));\n'
                 '}\n'
                 'console.log(parseContentType(undefined), bodyKind(undefined));\n',
       'hint': 'Регулярное выражение для «тип/подтип» плюс цикл по параметрам с кавычками.',
       'expected': ['"application/json" {"params":{},"subtype":"json","suffix":null,"type":"application"} '
                    'json',
                    '"Application/JSON; charset=UTF-8" '
                    '{"params":{"charset":"UTF-8"},"subtype":"json","suffix":null,"type":"application"} json',
                    '"application/vnd.api+json" '
                    '{"params":{},"subtype":"vnd.api+json","suffix":"json","type":"application"} json',
                    '"text/html;charset=utf-8" '
                    '{"params":{"charset":"utf-8"},"subtype":"html","suffix":null,"type":"text"} text',
                    '"multipart/form-data; boundary=\\"a;b\\"; x=1" '
                    '{"params":{"boundary":"a;b","x":"1"},"subtype":"form-data","suffix":null,"type":"multipart"} '
                    'multipart',
                    '"image/svg+xml" {"params":{},"subtype":"svg+xml","suffix":"xml","type":"image"} text',
                    '"application/x-www-form-urlencoded" '
                    '{"params":{},"subtype":"x-www-form-urlencoded","suffix":null,"type":"application"} form',
                    '"application/javascript" '
                    '{"params":{},"subtype":"javascript","suffix":null,"type":"application"} text',
                    '"text/plain; name=\\"a\\\\\\"b\\"" '
                    '{"params":{"name":"a\\"b"},"subtype":"plain","suffix":null,"type":"text"} text',
                    '"ерунда" null binary',
                    '"" null binary',
                    '"application/octet-stream" '
                    '{"params":{},"subtype":"octet-stream","suffix":null,"type":"application"} binary',
                    '"application/xml" {"params":{},"subtype":"xml","suffix":null,"type":"application"} text',
                    'null binary']},
      {'id': 'j18-response',
       'mode': 'js',
       'title': 'Свой Response',
       'statement': 'Напишите класс MyResponse(body, init): body — строка или null; init = { status = 200, '
                    'statusText = "", headers = {} }. Свойства: status, statusText, ok (200–299), headers '
                    '(объект с именами в нижнем регистре), bodyUsed (false, пока тело не прочитано). Методы '
                    '(все возвращают промис): text() → строка (null → ""), json() → JSON.parse(text) (ошибка '
                    'разбора — SyntaxError, промис отклоняется), clone() → копия (синхронно; если тело уже '
                    'прочитано — TypeError; копия и оригинал читаются независимо). Повторное чтение тела — '
                    'отклонение с TypeError. Статические: MyResponse.json(data, init) — тело JSON.stringify '
                    'и заголовок content-type: application/json (если не задан), и MyResponse.error() → '
                    'ответ со status 0, type "error", ok false.',
       'starter': 'class MyResponse {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const r = new MyResponse(\'{"a":1}\', { status: 201, statusText: "Created", headers: { '
                 '"Content-Type": "application/json" } });\n'
                 'console.log(r.ok, r.status, r.statusText, JSON.stringify(r.headers), r.bodyUsed);\n'
                 'const c = r.clone(); console.log(JSON.stringify(await r.json()), r.bodyUsed, c.bodyUsed, '
                 'await c.text());\n'
                 'for (const f of [() => r.text(), () => r.json(), () => c.json()]) { try { await f(); '
                 'console.log("нет ошибки"); } catch (e) { console.log(e.name); } }\n'
                 'try { r.clone(); } catch (e) { console.log("clone", e.name); }\n'
                 'try { await new MyResponse("не json").json(); } catch (e) { console.log(e.name); }\n'
                 'console.log(JSON.stringify(await new MyResponse(null).text()), new MyResponse("", { '
                 'status: 404 }).ok, new MyResponse("", { status: 299 }).ok, new MyResponse("", { status: '
                 '300 }).ok, new MyResponse().status);\n'
                 'const j = MyResponse.json({ x: [1, 2] }, { status: 202 }); console.log(j.status, '
                 'JSON.stringify(j.headers), await j.text());\n'
                 'console.log(JSON.stringify(MyResponse.json(1, { headers: { "Content-type": "text/x" } '
                 '}).headers));\n'
                 'const e = MyResponse.error(); console.log(e.status, e.type, e.ok);\n',
       'hint': 'Флаг «тело прочитано» и приватное поле с телом; clone создаёт новый объект до чтения.',
       'expected': ['true 201 Created {"content-type":"application/json"} false',
                    '{"a":1} true false {"a":1}',
                    'TypeError',
                    'TypeError',
                    'TypeError',
                    'clone TypeError',
                    'SyntaxError',
                    '"" false true false 200',
                    '202 {"content-type":"application/json"} {"x":[1,2]}',
                    '{"content-type":"text/x"}',
                    '0 error false']},
      {'id': 'j18-fetch-json',
       'mode': 'js',
       'title': 'Обёртка fetchJson',
       'statement': 'Напишите функцию fetchJson(fetchFn, url, options = {}), и класс HttpError (extends '
                    'Error; name «HttpError», поля status, statusText, body; message «HTTP <status>»). '
                    'options: { method = "GET", body, headers = {} }. Если body — объект или массив, он '
                    'отправляется JSON.stringify с заголовком "content-type": "application/json". Всегда '
                    'добавляется заголовок accept: "application/json". Заголовки из options.headers '
                    'добавляются последними и перекрывают общие (ключи регистронезависимы — используйте '
                    'нижний регистр). Вызов: fetchFn(url, { method, headers, body }) (body только если '
                    'задан). Ответ res имеет ok, status, statusText, headers.get(name), json(), text(). Если '
                    '!res.ok — бросить HttpError с body: разобранный json, если content-type содержит '
                    '«json», иначе текст. Статус 204 → null (тело не читать). Иначе → await res.json().',
       'starter': 'class HttpError extends Error {\n'
                  '}\n'
                  'async function fetchJson(fetchFn, url, options) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const mk = (status, body, ct, statusText = "") => ({ ok: status >= 200 && status < 300, '
                 'status, statusText, headers: { get: (n) => (n.toLowerCase() === "content-type" ? ct : '
                 'null) }, json: async () => JSON.parse(body), text: async () => body });\n'
                 'const calls = [];\n'
                 'const fakeFetch = async (url, init) => {\n'
                 '  calls.push([url, canon(init)]);\n'
                 '  if (url.endsWith("/ok")) return mk(200, \'{"v":1}\', "application/json");\n'
                 '  if (url.endsWith("/empty")) return mk(204, "", null);\n'
                 '  if (url.endsWith("/bad")) return mk(422, \'{"error":"поле"}\', "application/json; '
                 'charset=utf-8", "Unprocessable");\n'
                 '  if (url.endsWith("/html")) return mk(502, "<h1>плохой шлюз</h1>", "text/html", "Bad '
                 'Gateway");\n'
                 '  throw new TypeError("сеть");\n'
                 '};\n'
                 'console.log(JSON.stringify(await fetchJson(fakeFetch, "/ok")), JSON.stringify(await '
                 'fetchJson(fakeFetch, "/ok", { method: "POST", body: { a: [1] }, headers: { "X-Token": "t", '
                 'Accept: "text/plain" } })));\n'
                 'console.log(JSON.stringify(await fetchJson(fakeFetch, "/ok", { method: "PUT", body: "raw" '
                 '})), await fetchJson(fakeFetch, "/empty", { method: "DELETE" }));\n'
                 'for (const u of ["/bad", "/html", "/net"]) { try { await fetchJson(fakeFetch, u); } catch '
                 '(e) { console.log(u, e.name, e instanceof Error, e.message, e.status, e.statusText, '
                 'JSON.stringify(e.body)); } }\n'
                 'for (const c of calls) console.log(JSON.stringify(c));\n',
       'hint': 'Соберите заголовки, затем сначала проверьте ok, потом 204, потом разбирайте JSON.',
       'expected': ['{"v":1} {"v":1}',
                    '{"v":1} null',
                    '/bad HttpError true HTTP 422 422 Unprocessable {"error":"поле"}',
                    '/html HttpError true HTTP 502 502 Bad Gateway "<h1>плохой шлюз</h1>"',
                    '/net TypeError true сеть undefined undefined undefined',
                    '["/ok",{"headers":{"accept":"application/json"},"method":"GET"}]',
                    '["/ok",{"body":"{\\"a\\":[1]}","headers":{"accept":"text/plain","content-type":"application/json","x-token":"t"},"method":"POST"}]',
                    '["/ok",{"body":"raw","headers":{"accept":"application/json"},"method":"PUT"}]',
                    '["/empty",{"headers":{"accept":"application/json"},"method":"DELETE"}]',
                    '["/bad",{"headers":{"accept":"application/json"},"method":"GET"}]',
                    '["/html",{"headers":{"accept":"application/json"},"method":"GET"}]',
                    '["/net",{"headers":{"accept":"application/json"},"method":"GET"}]']},
      {'id': 'j18-stream-text',
       'mode': 'js',
       'title': 'Чтение потока с прогрессом',
       'statement': 'Напишите функцию readText(stream, onProgress, total): stream — ReadableStream, выдающий '
                    'Uint8Array; читайте через getReader(). Результат — полная строка, декодированная '
                    'TextDecoder в потоковом режиме (символ UTF-8 может быть разрезан между кусками). После '
                    'каждого куска вызывается onProgress({ loaded, total, percent }): loaded — накопленные '
                    'байты, total — переданное число или null, percent — целая часть процентов (0–100, но не '
                    'больше 100) или null, если total не задан или равен 0. Если onProgress не передан — '
                    'молча читайте. В конце вызовите reader.releaseLock().',
       'starter': 'async function readText(stream, onProgress, total) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const bytes = new TextEncoder().encode("Привет, мир! 😀 конец");\n'
                 'const streamOf = (sizes) => { let i = 0, k = 0; return new ReadableStream({ pull(c) { if '
                 '(i >= bytes.length) return c.close(); const n = sizes[k++ % sizes.length]; '
                 'c.enqueue(bytes.slice(i, i + n)); i += n; } }); };\n'
                 'for (const sizes of [[1], [3, 5], [7], [1000]]) {\n'
                 '  const log = [];\n'
                 '  const text = await readText(streamOf(sizes), (p) => '
                 'log.push(`${p.loaded}/${p.percent}`), bytes.length);\n'
                 '  console.log(text === "Привет, мир! 😀 конец", log.length, log.slice(-2).join(" "));\n'
                 '}\n'
                 'const l2 = []; await readText(streamOf([10]), (p) => l2.push(JSON.stringify(p))); '
                 'console.log(l2.slice(0, 2).join(" "));\n'
                 'const l3 = []; await readText(streamOf([40]), (p) => l3.push(p.percent), 10); '
                 'console.log(l3.join());\n'
                 'console.log(await readText(streamOf([4])), JSON.stringify(await readText(new '
                 'ReadableStream({ start(c) { c.close(); } }), () => {}, 0)));\n',
       'hint': 'Накапливайте текст через decode(value, {stream: true}) и в конце вызовите decode() без '
               'аргументов.',
       'expected': ['true 37 36/97 37/100',
                    'true 10 35/94 37/100',
                    'true 6 35/94 37/100',
                    'true 1 37/100',
                    '{"loaded":10,"total":null,"percent":null} {"loaded":20,"total":null,"percent":null}',
                    '100',
                    'Привет, мир! 😀 конец ""']},
      {'id': 'j18-ndjson',
       'mode': 'js',
       'title': 'Поток JSON-строк (NDJSON)',
       'statement': 'Напишите асинхронный генератор ndjson(stream): stream — ReadableStream из Uint8Array. '
                    'Он декодирует поток (UTF-8 может быть разрезан между кусками), делит на строки по «\\n» '
                    '(допустим «\\r\\n») — строки могут быть разрезаны между кусками — и для каждой непустой '
                    'строки отдаёт JSON.parse. Последняя строка без перевода строки тоже обрабатывается. '
                    'Пустые строки пропускаются (но считаются при нумерации). Если строка не JSON — '
                    'выбросьте Error с сообщением «Строка N: невалидный JSON», где N — номер строки с 1; уже '
                    'отданные объекты остаются отданными.',
       'starter': 'async function* ndjson(stream) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const streamOf = (text, size) => { const b = new TextEncoder().encode(text); let i = 0; '
                 'return new ReadableStream({ pull(c) { if (i >= b.length) return c.close(); '
                 'c.enqueue(b.slice(i, i + size)); i += size; } }); };\n'
                 'const collect = async (text, size) => { const out = []; try { for await (const x of '
                 'ndjson(streamOf(text, size))) out.push(x); } catch (e) { out.push("ERR:" + e.message); } '
                 'return JSON.stringify(out); };\n'
                 'const data = \'{"a":1}\\n{"имя":"Ада"}\\r\\n\\n[1,2]\\n{"last":true}\';\n'
                 'for (const s of [1, 2, 5, 100]) console.log(s, await collect(data, s));\n'
                 'console.log(await collect(\'{"a":1}\\n{плохо}\\n{"b":2}\\n\', 3));\n'
                 'console.log(await collect("", 3), await collect("\\n\\n", 3), await '
                 'collect(\'{"x":"😀"}\\n\', 1), await collect("не json", 4));\n',
       'hint': 'Копите буфер; пока в нём есть «\\n» — отрезайте строку и разбирайте; хвост обработайте после '
               'конца потока.',
       'expected': ['1 [{"a":1},{"имя":"Ада"},[1,2],{"last":true}]',
                    '2 [{"a":1},{"имя":"Ада"},[1,2],{"last":true}]',
                    '5 [{"a":1},{"имя":"Ада"},[1,2],{"last":true}]',
                    '100 [{"a":1},{"имя":"Ада"},[1,2],{"last":true}]',
                    '[{"a":1},"ERR:Строка 2: невалидный JSON"]',
                    '[] [] [{"x":"😀"}] ["ERR:Строка 1: невалидный JSON"]']},
      {'id': 'j18-progress',
       'mode': 'js',
       'title': 'Трекер прогресса загрузки',
       'statement': 'Напишите функцию createProgress(total, now): now — функция «время в миллисекундах»; '
                    'момент создания считается стартом. Возвращает { update(loaded), snapshot() }. update '
                    'запоминает число загруженных байт (не больше total, если total задан; не меньше '
                    'предыдущего значения). snapshot → { loaded, total, percent, rate, eta, done }: percent '
                    '— целая часть процентов или null, если total не задан (null/0); rate — байт в секунду '
                    'за всё время с старта (loaded / секунды; 0, если прошло 0 мс); eta — оставшиеся '
                    'секунды, округлённые вверх (null, если total не задан или rate = 0; 0, если загрузка '
                    'завершена); done — loaded ≥ total (false, если total не задан).',
       'starter': 'function createProgress(total, now) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let t = 1000;\n'
                 'const p = createProgress(1000, () => t);\n'
                 'console.log(JSON.stringify(p.snapshot()));\n'
                 't = 3000; p.update(250); console.log(JSON.stringify(p.snapshot()));\n'
                 'p.update(100); console.log(p.snapshot().loaded);\n'
                 't = 4000; p.update(700); console.log(JSON.stringify(p.snapshot()));\n'
                 't = 5000; p.update(5000); console.log(JSON.stringify(p.snapshot()));\n'
                 'const q = createProgress(null, () => t); t = 6000; q.update(500); '
                 'console.log(JSON.stringify(q.snapshot()));\n'
                 'const z = createProgress(0, () => t); z.update(3); '
                 'console.log(JSON.stringify(z.snapshot()));\n'
                 'const w = createProgress(10, () => t); t += 1; w.update(3); '
                 'console.log(JSON.stringify(w.snapshot()));\n',
       'hint': 'Храните start и loaded; всё остальное считайте в snapshot.',
       'expected': ['{"loaded":0,"total":1000,"percent":0,"rate":0,"eta":null,"done":false}',
                    '{"loaded":250,"total":1000,"percent":25,"rate":125,"eta":6,"done":false}',
                    '250',
                    '{"loaded":700,"total":1000,"percent":70,"rate":233.33333333333334,"eta":2,"done":false}',
                    '{"loaded":1000,"total":1000,"percent":100,"rate":250,"eta":0,"done":true}',
                    '{"loaded":500,"total":null,"percent":null,"rate":500,"eta":null,"done":false}',
                    '{"loaded":3,"total":null,"percent":null,"rate":0,"eta":null,"done":false}',
                    '{"loaded":3,"total":10,"percent":30,"rate":3000,"eta":1,"done":false}']},
      {'id': 'j18-abort-controller',
       'mode': 'js',
       'title': 'Свой AbortController',
       'statement': 'Напишите классы MyAbortSignal и MyAbortController. Контроллер: свойство signal, метод '
                    'abort(reason) (повторный вызов ничего не делает; reason по умолчанию — Error с name '
                    '«AbortError» и message «This operation was aborted»). Сигнал: aborted, reason '
                    '(undefined, пока не отменён), addEventListener("abort", fn, { once }), '
                    'removeEventListener, onabort (свойство-обработчик, вызывается первым, затем слушатели в '
                    'порядке добавления; слушатель получает объект { type: "abort", target }), '
                    'throwIfAborted() (бросает reason), статические MyAbortSignal.abort(reason) → уже '
                    'отменённый сигнал и MyAbortSignal.any(signals) → сигнал, отменяющийся с причиной '
                    'первого отменённого (если среди них уже есть отменённый — сразу отменён). Слушатель, '
                    'добавленный уже после отмены, не вызывается.',
       'starter': 'class MyAbortSignal {\n}\nclass MyAbortController {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const c = new MyAbortController(); const s = c.signal; const log = [];\n'
                 's.onabort = () => log.push("onabort"); const f1 = () => log.push("f1"); '
                 's.addEventListener("abort", f1); s.addEventListener("abort", () => log.push("once"), { '
                 'once: true }); s.addEventListener("abort", (e) => log.push("f3:" + e.type + ":" + '
                 '(e.target === s)));\n'
                 'const f4 = () => log.push("f4"); s.addEventListener("abort", f4); '
                 's.removeEventListener("abort", f4);\n'
                 'console.log(s.aborted, s.reason);\n'
                 'c.abort(); console.log(s.aborted, s.reason.name, s.reason.message, log.join());\n'
                 'c.abort(new Error("другая")); console.log(s.reason.name, log.length);\n'
                 's.addEventListener("abort", () => log.push("late")); console.log(log.length);\n'
                 'try { s.throwIfAborted(); } catch (e) { console.log("бросил", e.name); }\n'
                 'const ok = new MyAbortController(); ok.signal.throwIfAborted(); console.log("не бросил");\n'
                 'const a = MyAbortSignal.abort("причина"); console.log(a.aborted, a.reason, '
                 'MyAbortSignal.abort().reason.name);\n'
                 'const c1 = new MyAbortController(), c2 = new MyAbortController(); const any = '
                 'MyAbortSignal.any([c1.signal, c2.signal]); const l2 = []; any.addEventListener("abort", () '
                 '=> l2.push(any.reason));\n'
                 'console.log(any.aborted); c2.abort("вторая"); c1.abort("первая"); console.log(any.aborted, '
                 'any.reason, l2.join());\n'
                 'console.log(MyAbortSignal.any([new MyAbortController().signal, a]).reason, '
                 'MyAbortSignal.any([]).aborted);\n',
       'hint': 'Состояние (aborted, reason, слушатели) живёт в сигнале; контроллер только вызывает '
               'внутренний метод отмены.',
       'expected': ['false undefined',
                    'true AbortError This operation was aborted onabort,f1,once,f3:abort:true',
                    'AbortError 4',
                    '4',
                    'бросил AbortError',
                    'не бросил',
                    'true причина AbortError',
                    'false',
                    'true вторая вторая',
                    'причина false']},
      {'id': 'j18-abortable',
       'mode': 'js',
       'title': 'Отменяемая операция',
       'statement': 'Напишите функцию abortable(fn, signal): fn(signal) возвращает промис. abortable '
                    'возвращает промис, который: если сигнал уже отменён — отклоняется signal.reason, не '
                    'вызывая fn; иначе вызывает fn(signal) и при отмене сигнала немедленно отклоняется '
                    'причиной signal.reason (не дожидаясь fn); если fn завершилась раньше — её результат или '
                    'ошибка; завершение fn после отмены игнорируется (без необработанных ошибок). Слушатель '
                    'отмены нужно снять после завершения.',
       'starter': 'function abortable(fn, signal) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const later = (ms, v, fail) => new Promise((res, rej) => setTimeout(() => (fail ? rej(new '
                 'Error(v)) : res(v)), ms));\n'
                 'const show = async (label, p) => { try { console.log(label, "ok", await p); } catch (e) { '
                 'console.log(label, "err", e?.message ?? e); } };\n'
                 'await show("быстро", abortable(() => later(5, "готово"), new AbortController().signal));\n'
                 'await show("ошибка fn", abortable(() => later(5, "сбой", true), new '
                 'AbortController().signal));\n'
                 'const c = new AbortController(); let called = 0;\n'
                 'const p = abortable(() => { called++; return later(40, "поздно"); }, c.signal); '
                 'setTimeout(() => c.abort(new Error("отмена")), 10);\n'
                 'await show("отмена", p); console.log(called);\n'
                 'const c2 = new AbortController(); c2.abort(new Error("заранее")); let called2 = 0;\n'
                 'await show("заранее", abortable(() => { called2++; return later(1, "x"); }, c2.signal)); '
                 'console.log(called2);\n'
                 'const c3 = new AbortController(); const p3 = abortable(() => later(30, "boom", true), '
                 'c3.signal); c3.abort(new Error("раньше сбоя")); await show("после fn", p3);\n'
                 'await later(60);\n'
                 'console.log("без необработанных ошибок");\n',
       'hint': 'Оберните в new Promise; отмену и завершение fn направьте в resolve/reject — первое '
               'сработавшее побеждает.',
       'expected': ['быстро ok готово',
                    'ошибка fn err сбой',
                    'отмена err отмена',
                    '1',
                    'заранее err заранее',
                    '0',
                    'после fn err раньше сбоя',
                    'без необработанных ошибок']},
      {'id': 'j18-latest-only',
       'mode': 'js',
       'title': 'Только последний запрос',
       'statement': 'Напишите функцию createLatest(fetcher): fetcher(arg, signal) → промис. Возвращает '
                    'функцию run(arg) → промис. Каждый новый вызов отменяет предыдущий (вызывает abort() у '
                    'его AbortController) и вызывает fetcher(arg, signal) с новым сигналом. Результат: { '
                    'stale: false, value } — если это всё ещё последний вызов к моменту завершения; { stale: '
                    'true } — если вызов уже вытеснен более новым (и тогда его ошибка не пробрасывается, а '
                    'просто { stale: true }). Ошибка последнего вызова пробрасывается как есть.',
       'starter': 'function createLatest(fetcher) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const later = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const seen = [];\n'
                 'const run = createLatest(async (q, signal) => { signal.addEventListener("abort", () => '
                 'seen.push("abort:" + q)); if (q === "boom") { await later(5); throw new Error("сбой"); } '
                 'await later(q === "slow" ? 40 : 10); return q.toUpperCase(); });\n'
                 'const a = run("slow"); await later(5); const b = run("fast");\n'
                 'console.log(JSON.stringify(await a), JSON.stringify(await b), seen.join());\n'
                 'console.log(JSON.stringify(await run("one")), JSON.stringify(await run("two")));\n'
                 'const c = run("boom"); const d = run("last"); console.log(JSON.stringify(await c), '
                 'JSON.stringify(await d));\n'
                 'try { await run("boom"); } catch (e) { console.log("ошибка", e.message); }\n'
                 'const e1 = run("slow"); const e2 = run("boom"); e2.catch(() => {}); '
                 'console.log(JSON.stringify(await e1)); try { await e2; } catch (e) { console.log("ошибка", '
                 'e.message); }\n',
       'hint': 'Счётчик вызовов и общий AbortController; сравнивайте номер вызова с текущим после await.',
       'expected': ['{"stale":true} {"stale":false,"value":"FAST"} abort:slow',
                    '{"stale":false,"value":"ONE"} {"stale":false,"value":"TWO"}',
                    '{"stale":true} {"stale":false,"value":"LAST"}',
                    'ошибка сбой',
                    '{"stale":true}',
                    'ошибка сбой']},
      {'id': 'j18-timeout',
       'mode': 'js',
       'title': 'Таймаут запроса',
       'statement': 'Напишите функцию withTimeout(fn, ms, timers): timers = { setTimeout, clearTimeout } '
                    '(виртуальные часы). fn(signal) → промис. Создайте AbortController, запустите fn(signal) '
                    'и таймер на ms. Если fn завершилась раньше — вернуть её результат (или пробросить '
                    'ошибку) и снять таймер. Если таймер сработал раньше — вызвать abort(reason), где reason '
                    '— Error с name «TimeoutError» и message «Превышено время ожидания: <ms> мс», и '
                    'отклонить промис этой же ошибкой; позднее завершение fn игнорируется. После любого '
                    'исхода активных таймеров не остаётся.',
       'starter': 'function withTimeout(fn, ms, timers) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const FAKE = () => { let t = 0; const timers = new Map(); let id = 1; return { now: () => '
                 't, setTimeout(fn, ms) { const i = id++; timers.set(i, { at: t + ms, fn }); return i; }, '
                 'clearTimeout(i) { timers.delete(i); }, advance(ms) { const end = t + ms; for (;;) { const '
                 'due = [...timers].filter(([, x]) => x.at <= end).sort((a, b) => a[1].at - b[1].at || a[0] '
                 '- b[0])[0]; if (!due) break; timers.delete(due[0]); t = due[1].at; due[1].fn(); } t = end; '
                 '}, pending: () => timers.size }; };\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'const clock = FAKE();\n'
                 'const slow = (ms, fail) => (signal) => new Promise((res, rej) => { const id = '
                 'clock.setTimeout(() => (fail ? rej(new Error("сбой")) : res("готово")), ms); '
                 'signal.addEventListener("abort", () => clock.clearTimeout(id)); });\n'
                 'const run = async (label, fn, ms, advance) => {\n'
                 '  const p = withTimeout(fn, ms, clock); let out = "ожидание"; p.then((v) => (out = "ok " + '
                 'v), (e) => (out = `${e.name}: ${e.message}`));\n'
                 '  await tick(); clock.advance(advance); await tick(); await tick(); console.log(label, '
                 'out, "таймеров:", clock.pending());\n'
                 '};\n'
                 'await run("успел", slow(50), 100, 60);\n'
                 'await run("не успел", slow(500), 100, 100);\n'
                 'await run("ошибка до таймаута", slow(20, true), 100, 20);\n'
                 'await run("точно в срок?", slow(100), 100, 100);\n'
                 'let aborted = ""; const p2 = withTimeout((s) => { s.addEventListener("abort", () => '
                 '(aborted = s.reason.name)); return new Promise(() => {}); }, 30, clock); p2.catch(() => '
                 '{}); await tick(); clock.advance(30); await tick(); console.log(aborted, '
                 'clock.pending());\n',
       'hint': 'Таймер → abort(reason) + reject; завершение fn → resolve/reject; в обоих случаях снимайте '
               'таймер.',
       'expected': ['успел ok готово таймеров: 0',
                    'не успел TimeoutError: Превышено время ожидания: 100 мс таймеров: 0',
                    'ошибка до таймаута Error: сбой таймеров: 0',
                    'точно в срок? TimeoutError: Превышено время ожидания: 100 мс таймеров: 0',
                    'TimeoutError 0']},
      {'id': 'j18-retry',
       'mode': 'js',
       'title': 'Повтор с экспоненциальной задержкой',
       'statement': 'Напишите асинхронную функцию retry(fn, options): fn(attempt) → промис (attempt от 0). '
                    'options: { retries = 3, base = 100, factor = 2, max = 2000, jitter = "none", rand = '
                    'Math.random, sleep, shouldRetry = () => true, onRetry }. Всего попыток retries + 1. '
                    'После неудачной попытки n (с 0), если попытки остались и shouldRetry(error, n) истинно: '
                    'delay = min(max, base × factor^n); при jitter "full" delay = floor(rand() × delay); при '
                    '"equal" delay = floor(delay / 2) + floor(rand() × (delay / 2)) (деление — вещественное, '
                    'как есть); вызвать onRetry?.({ attempt: n, delay, error }), затем await sleep(delay) и '
                    'следующая попытка. Если shouldRetry вернул false или попытки кончились — пробросить '
                    'последнюю ошибку. Успех — вернуть значение.',
       'starter': 'async function retry(fn, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const flaky = (fails, label = "сбой") => { let c = 0; return async (a) => { c++; if (c <= '
                 'fails) throw new Error(`${label}${c}`); return `ok на попытке ${a}`; }; };\n'
                 'const run = async (name, fn, opts) => { const delays = []; const log = []; try { const v = '
                 'await retry(fn, { sleep: async (d) => { delays.push(d); }, onRetry: (i) => '
                 'log.push(`${i.attempt}:${i.delay}:${i.error.message}`), ...opts }); console.log(name, v, '
                 'delays.join(), log.join("|")); } catch (e) { console.log(name, "ошибка", e.message, '
                 'delays.join()); } };\n'
                 'await run("сразу", flaky(0), {});\n'
                 'await run("две неудачи", flaky(2), {});\n'
                 'await run("исчерпали", flaky(10), {});\n'
                 'await run("max", flaky(10), { retries: 6, base: 500, max: 1500 });\n'
                 'await run("factor 3", flaky(3), { base: 10, factor: 3 });\n'
                 'await run("retries 0", flaky(1), { retries: 0 });\n'
                 'await run("full jitter", flaky(3), { jitter: "full", rand: () => 0.5 });\n'
                 'await run("equal jitter", flaky(3), { jitter: "equal", rand: () => 0.999 });\n'
                 'await run("shouldRetry", flaky(5), { shouldRetry: (e, n) => n < 1 });\n'
                 'await run("только на \'сбой1\'", flaky(5), { shouldRetry: (e) => e.message === "сбой1" '
                 '});\n',
       'hint': 'Цикл по попыткам с try/catch; расчёт задержки по формуле до sleep.',
       'expected': ['сразу ok на попытке 0',
                    'две неудачи ok на попытке 2 100,200 0:100:сбой1|1:200:сбой2',
                    'исчерпали ошибка сбой4 100,200,400',
                    'max ошибка сбой7 500,1000,1500,1500,1500,1500',
                    'factor 3 ok на попытке 3 10,30,90 0:10:сбой1|1:30:сбой2|2:90:сбой3',
                    'retries 0 ошибка сбой1',
                    'full jitter ok на попытке 3 50,100,200 0:50:сбой1|1:100:сбой2|2:200:сбой3',
                    'equal jitter ok на попытке 3 99,199,399 0:99:сбой1|1:199:сбой2|2:399:сбой3',
                    'shouldRetry ошибка сбой2 100',
                    "только на 'сбой1' ошибка сбой2 100"]},
      {'id': 'j18-retry-after',
       'mode': 'js',
       'title': 'Заголовок Retry-After',
       'statement': 'Напишите функцию parseRetryAfter(value, nowMs) → число миллисекунд ожидания или null. '
                    'value — значение заголовка: целое число секунд («120»; пробелы по краям допустимы; '
                    'дробные, отрицательные и значения с буквами — null) или дата в формате HTTP («Wed, 21 '
                    'Oct 2026 07:28:00 GMT»; дата в прошлом даёт 0). Прочее (пусто, не строка, неразборчивая '
                    'дата) — null. Результат не больше 24 часов: более длинное ожидание ограничивается 86 '
                    '400 000.',
       'starter': 'function parseRetryAfter(value, nowMs) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const now = Date.UTC(2026, 9, 21, 7, 0, 0);\n'
                 'for (const v of ["120", " 5 ", "0", "1.5", "-3", "10s", "", "   ", "Wed, 21 Oct 2026 '
                 '07:28:00 GMT", "Wed, 21 Oct 2026 06:00:00 GMT", "Wed, 21 Oct 2026 07:00:00 GMT", "Fri, 30 '
                 'Dec 2027 00:00:00 GMT", "когда-нибудь", "99999999", undefined, 5, null]) '
                 'console.log(JSON.stringify(v), parseRetryAfter(v, now));\n',
       'hint': 'Две ветки: только цифры → секунды; иначе — разбор даты и вычитание текущего времени.',
       'expected': ['"120" 120000',
                    '" 5 " 5000',
                    '"0" 0',
                    '"1.5" null',
                    '"-3" null',
                    '"10s" null',
                    '"" null',
                    '"   " null',
                    '"Wed, 21 Oct 2026 07:28:00 GMT" 1680000',
                    '"Wed, 21 Oct 2026 06:00:00 GMT" 0',
                    '"Wed, 21 Oct 2026 07:00:00 GMT" 0',
                    '"Fri, 30 Dec 2027 00:00:00 GMT" 86400000',
                    '"когда-нибудь" null',
                    '"99999999" 86400000',
                    'undefined null',
                    '5 null',
                    'null null']},
      {'id': 'j18-retry-rules',
       'mode': 'js',
       'title': 'Когда можно повторять запрос',
       'statement': 'Напишите функцию shouldRetry({ method, status, attempt, retries = 3, hasIdempotencyKey '
                    '= false }) → boolean. status не задан (undefined) — сетевая ошибка. attempt — сколько '
                    'повторов уже сделано; если attempt ≥ retries — false. Метод идемпотентный: GET, HEAD, '
                    'OPTIONS, PUT, DELETE (регистр не важен); POST и PATCH — только с hasIdempotencyKey. '
                    'Правила: сетевая ошибка → повторять, если метод идемпотентный или есть ключ; статусы '
                    '408, 425, 500, 502, 503, 504 → так же; статус 429 → повторять для любого метода (сервер '
                    'запрос не выполнял); остальные статусы (в том числе 2xx, 3xx, 4xx, 501) — false.',
       'starter': 'function shouldRetry(info) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const rows = [];\n'
                 'for (const method of ["get", "PUT", "post", "PATCH", "DELETE"]) {\n'
                 '  rows.push(method + ": " + [undefined, 200, 301, 400, 404, 408, 425, 429, 500, 501, 502, '
                 '503, 504].map((s) => (shouldRetry({ method, status: s, attempt: 0 }) ? 1 : 0)).join(""));\n'
                 '}\n'
                 'console.log(rows.join("\\n"));\n'
                 'console.log(shouldRetry({ method: "POST", status: 503, attempt: 0, hasIdempotencyKey: true '
                 '}), shouldRetry({ method: "POST", status: undefined, attempt: 1, hasIdempotencyKey: true '
                 '}), shouldRetry({ method: "GET", status: 500, attempt: 3 }), shouldRetry({ method: "GET", '
                 'status: 500, attempt: 2, retries: 2 }), shouldRetry({ method: "GET", status: 500, attempt: '
                 '1, retries: 2 }), shouldRetry({ method: "POST", status: 429, attempt: 0 }));\n',
       'hint': 'Сначала проверка лимита попыток, затем «безопасен ли метод», затем таблица статусов.',
       'expected': ['get: 1000011110111',
                    'PUT: 1000011110111',
                    'post: 0000000100000',
                    'PATCH: 0000000100000',
                    'DELETE: 1000011110111',
                    'true true false false true true']},
      {'id': 'j18-origin',
       'mode': 'js',
       'title': 'Источник (origin) адреса',
       'statement': 'Напишите функции originOf(url) и sameOrigin(a, b). originOf → строка '
                    '«схема://хост[:порт]» в нижнем регистре; порт по умолчанию (80 для http, 443 для https) '
                    'не пишется; для адресов с вложенным источником (blob:https://x.ru/uuid) — источник '
                    'вложенного адреса; для остальных схем (file:, data:, about:, javascript:) и '
                    'некорректных строк — «null». sameOrigin(a, b) — true, если источники одинаковы и ни '
                    'один не «null». Нестандартные порты различают источники; «example.com» и '
                    '«www.example.com» — разные.',
       'starter': 'function originOf(url) {\n}\nfunction sameOrigin(a, b) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'for (const u of ["https://Example.COM/path?q=1#h", "http://example.com:80/", '
                 '"http://example.com:8080/x", "https://example.com:443", "https://example.com:444", '
                 '"blob:https://x.ru/3e1f-uuid", "blob:null/uuid", "file:///etc/hosts", '
                 '"data:text/plain,hi", "about:blank", "javascript:void(0)", "не адрес", "", "ws://x.ru/"]) '
                 'console.log(JSON.stringify(u), originOf(u));\n'
                 'console.log(sameOrigin("https://a.ru/x", "https://A.ru:443/y"), sameOrigin("https://a.ru", '
                 '"http://a.ru"), sameOrigin("https://a.ru", "https://www.a.ru"), sameOrigin("file:///a", '
                 '"file:///a"), sameOrigin("https://a.ru:8080", "https://a.ru"), sameOrigin("data:,1", '
                 '"data:,1"));\n',
       'hint': 'Класс URL даёт protocol и host (порт по умолчанию он уже убирает).',
       'expected': ['"https://Example.COM/path?q=1#h" https://example.com',
                    '"http://example.com:80/" http://example.com',
                    '"http://example.com:8080/x" http://example.com:8080',
                    '"https://example.com:443" https://example.com',
                    '"https://example.com:444" https://example.com:444',
                    '"blob:https://x.ru/3e1f-uuid" https://x.ru',
                    '"blob:null/uuid" null',
                    '"file:///etc/hosts" null',
                    '"data:text/plain,hi" null',
                    '"about:blank" null',
                    '"javascript:void(0)" null',
                    '"не адрес" null',
                    '"" null',
                    '"ws://x.ru/" null',
                    'true false false false false false']},
      {'id': 'j18-simple-request',
       'mode': 'js',
       'title': 'Простой ли CORS-запрос',
       'statement': 'Напишите функцию needsPreflight({ method, headers = {}, streamBody = false }) → true, '
                    'если браузер сначала отправит предварительный запрос OPTIONS. Простой запрос (preflight '
                    'не нужен): метод GET, HEAD или POST (регистр не важен); все заголовки (имена без учёта '
                    'регистра) из списка: accept, accept-language, content-language, content-type, range '
                    '(range — только вида «bytes=число-», «bytes=число-число»); content-type — только '
                    'application/x-www-form-urlencoded, multipart/form-data или text/plain (параметры после '
                    '«;» не учитываются, регистр не важен); значение любого заголовка не длиннее 128 '
                    'символов; тело-поток (streamBody) делает запрос непростым. Любое нарушение — true.',
       'starter': 'function needsPreflight(req) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const cases = [\n'
                 '  ["GET без заголовков", { method: "GET" }], ["get + accept", { method: "get", headers: { '
                 'Accept: "application/json" } }], ["POST форма", { method: "POST", headers: { '
                 '"Content-Type": "application/x-www-form-urlencoded; charset=utf-8" } }],\n'
                 '  ["POST JSON", { method: "POST", headers: { "Content-Type": "application/json" } }], '
                 '["PUT", { method: "PUT" }], ["DELETE", { method: "DELETE" }], ["PATCH", { method: "PATCH" '
                 '}], ["HEAD", { method: "HEAD" }],\n'
                 '  ["свой заголовок", { method: "GET", headers: { "X-Token": "1" } }], ["Authorization", { '
                 'method: "GET", headers: { Authorization: "Bearer x" } }], ["multipart", { method: "POST", '
                 'headers: { "content-type": "Multipart/Form-Data; boundary=x" } }],\n'
                 '  ["text/plain", { method: "POST", headers: { "Content-Type": "text/plain" } }], '
                 '["text/html", { method: "POST", headers: { "Content-Type": "text/html" } }], ["range ok", '
                 '{ method: "GET", headers: { Range: "bytes=0-99" } }], ["range open", { method: "GET", '
                 'headers: { Range: "bytes=100-" } }],\n'
                 '  ["range bad", { method: "GET", headers: { Range: "bytes=0-5,10-15" } }], ["длинное '
                 'значение", { method: "GET", headers: { Accept: "a".repeat(129) } }], ["128 ок", { method: '
                 '"GET", headers: { Accept: "a".repeat(128) } }], ["поток", { method: "POST", streamBody: '
                 'true }],\n'
                 '  ["accept-language", { method: "GET", headers: { "Accept-Language": "ru", '
                 '"Content-Language": "ru" } }],\n'
                 '];\n'
                 'for (const [n, r] of cases) console.log(n.padEnd(20), needsPreflight(r));\n',
       'hint': 'Метод, потом каждый заголовок по таблице допустимых; любое нарушение — true.',
       'expected': ['GET без заголовков   false',
                    'get + accept         false',
                    'POST форма           false',
                    'POST JSON            true',
                    'PUT                  true',
                    'DELETE               true',
                    'PATCH                true',
                    'HEAD                 false',
                    'свой заголовок       true',
                    'Authorization        true',
                    'multipart            false',
                    'text/plain           false',
                    'text/html            true',
                    'range ok             false',
                    'range open           false',
                    'range bad            true',
                    'длинное значение     true',
                    '128 ок               false',
                    'поток                true',
                    'accept-language      false']},
      {'id': 'j18-cors-server',
       'mode': 'js',
       'title': 'Сервер, который разрешает CORS',
       'statement': 'Напишите функцию createCors(config) → handle(req) → { status, headers, next }. config: '
                    '{ origins ("*" | массив строк и RegExp), credentials = false, methods = '
                    '["GET","HEAD","POST"], allowedHeaders (массив; если не задан — отражать '
                    'access-control-request-headers), exposedHeaders = [], maxAge }. req = { method, headers '
                    '} (ключи headers — в нижнем регистре). Правила: нет заголовка origin → { status: null, '
                    'headers: {}, next: true }. Источник не разрешён: предзапрос (OPTIONS с '
                    'access-control-request-method) → { status: 403, headers: {}, next: false }, обычный '
                    'запрос → { status: null, headers: {}, next: true } (браузер сам заблокирует). '
                    'Предзапрос разрешённого источника: если метод запроса не в methods — { status: 405, '
                    'headers: {}, next: false }; иначе { status: 204, next: false } и заголовки: '
                    'access-control-allow-origin (сам источник; «*» только если origins === "*" и нет '
                    'credentials), access-control-allow-methods (methods через «, »), '
                    'access-control-allow-headers (allowedHeaders через «, » либо отражённые; если пусто — '
                    'не добавлять), access-control-allow-credentials: "true" (если credentials), '
                    'access-control-max-age (строка, если задан), vary (значение «Origin», а при отражении '
                    'заголовков — «Origin, Access-Control-Request-Headers»; не добавлять при ответе «*»). '
                    'Обычный запрос разрешённого источника → { status: null, next: true } и заголовки '
                    'allow-origin, allow-credentials, access-control-expose-headers (если есть), vary: '
                    'Origin (если не «*»).',
       'starter': 'function createCors(config) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const show = (label, r) => console.log(label.padEnd(18), JSON.stringify(canon(r)));\n'
                 'const pre = (origin, method, hdrs) => ({ method: "OPTIONS", headers: { origin, '
                 '"access-control-request-method": method, ...(hdrs ? { "access-control-request-headers": '
                 'hdrs } : {}) } });\n'
                 'const a = createCors({ origins: ["https://app.ru", /^https:\\/\\/.*\\.example\\.com$/], '
                 'credentials: true, methods: ["GET", "POST", "PUT"], maxAge: 600, exposedHeaders: '
                 '["x-total", "etag"] });\n'
                 'show("нет origin", a({ method: "GET", headers: {} }));\n'
                 'show("предзапрос ок", a(pre("https://app.ru", "PUT", "content-type, x-token")));\n'
                 'show("предзапрос regexp", a(pre("https://a.example.com", "get")));\n'
                 'show("метод запрещён", a(pre("https://app.ru", "DELETE")));\n'
                 'show("чужой предзапрос", a(pre("https://evil.com", "GET")));\n'
                 'show("чужой обычный", a({ method: "GET", headers: { origin: "https://evil.com" } }));\n'
                 'show("обычный", a({ method: "GET", headers: { origin: "https://app.ru" } }));\n'
                 'const b = createCors({ origins: "*", allowedHeaders: ["content-type"], exposedHeaders: [] '
                 '});\n'
                 'show("* предзапрос", b(pre("https://x.ru", "POST", "authorization")));\n'
                 'show("* обычный", b({ method: "POST", headers: { origin: "https://x.ru" } }));\n'
                 'const c = createCors({ origins: "*", credentials: true });\n'
                 'show("* + cred", c({ method: "GET", headers: { origin: "https://x.ru" } }));\n'
                 'show("без запрошенных", c(pre("https://x.ru", "GET")));\n'
                 'show("OPTIONS без acrm", a({ method: "OPTIONS", headers: { origin: "https://app.ru" } '
                 '}));\n',
       'hint': 'Разделите предзапрос и обычный запрос; собирайте заголовки по таблице правил, vary — '
               'отдельным списком.',
       'expected': ['нет origin         {"headers":{},"next":true,"status":null}',
                    'предзапрос ок      '
                    '{"headers":{"access-control-allow-credentials":"true","access-control-allow-headers":"content-type, '
                    'x-token","access-control-allow-methods":"GET, POST, '
                    'PUT","access-control-allow-origin":"https://app.ru","access-control-max-age":"600","vary":"Origin, '
                    'Access-Control-Request-Headers"},"next":false,"status":204}',
                    'предзапрос regexp  '
                    '{"headers":{"access-control-allow-credentials":"true","access-control-allow-methods":"GET, '
                    'POST, '
                    'PUT","access-control-allow-origin":"https://a.example.com","access-control-max-age":"600","vary":"Origin, '
                    'Access-Control-Request-Headers"},"next":false,"status":204}',
                    'метод запрещён     {"headers":{},"next":false,"status":405}',
                    'чужой предзапрос   {"headers":{},"next":false,"status":403}',
                    'чужой обычный      {"headers":{},"next":true,"status":null}',
                    'обычный            '
                    '{"headers":{"access-control-allow-credentials":"true","access-control-allow-origin":"https://app.ru","access-control-expose-headers":"x-total, '
                    'etag","vary":"Origin"},"next":true,"status":null}',
                    '* предзапрос       '
                    '{"headers":{"access-control-allow-headers":"content-type","access-control-allow-methods":"GET, '
                    'HEAD, POST","access-control-allow-origin":"*"},"next":false,"status":204}',
                    '* обычный          '
                    '{"headers":{"access-control-allow-origin":"*"},"next":true,"status":null}',
                    '* + cred           '
                    '{"headers":{"access-control-allow-credentials":"true","access-control-allow-origin":"https://x.ru","vary":"Origin"},"next":true,"status":null}',
                    'без запрошенных    '
                    '{"headers":{"access-control-allow-credentials":"true","access-control-allow-methods":"GET, '
                    'HEAD, POST","access-control-allow-origin":"https://x.ru","vary":"Origin, '
                    'Access-Control-Request-Headers"},"next":false,"status":204}',
                    'OPTIONS без acrm   '
                    '{"headers":{"access-control-allow-credentials":"true","access-control-allow-origin":"https://app.ru","access-control-expose-headers":"x-total, '
                    'etag","vary":"Origin"},"next":true,"status":null}']},
      {'id': 'j18-cors-check',
       'mode': 'js',
       'title': 'Разрешит ли браузер прочитать ответ',
       'statement': 'Напишите функцию checkCors({ pageOrigin, requestUrl, credentials, responseHeaders }) → '
                    '{ allowed, reason }. credentials — «omit», «same-origin» или «include»; responseHeaders '
                    '— объект с ключами в нижнем регистре. Если источник requestUrl совпадает с pageOrigin '
                    '(схема, хост, порт) — { allowed: true, reason: "same-origin" }. Иначе смотрим '
                    'access-control-allow-origin: нет заголовка → { false, "нет Access-Control-Allow-Origin" '
                    '}; значение «*»: при credentials «include» — { false, "звёздочка недопустима с '
                    'credentials" }, иначе { true, "ok" }; значение равно pageOrigin: при credentials '
                    '«include» нужен access-control-allow-credentials ровно «true», иначе { false, "нет '
                    'Access-Control-Allow-Credentials" }; когда всё в порядке — { true, "ok" }; любое другое '
                    'значение — { false, "источник не совпадает" }.',
       'starter': 'function checkCors(info) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const page = "https://app.ru";\n'
                 'const t = (url, credentials, h) => console.log(url.padEnd(26), credentials.padEnd(12), '
                 'JSON.stringify(canon(h)), JSON.stringify(canon(checkCors({ pageOrigin: page, requestUrl: '
                 'url, credentials, responseHeaders: h }))));\n'
                 't("https://app.ru/api", "include", {});\n'
                 't("https://app.ru:8443/api", "omit", {});\n'
                 't("https://api.ru/x", "omit", {});\n'
                 't("https://api.ru/x", "omit", { "access-control-allow-origin": "*" });\n'
                 't("https://api.ru/x", "include", { "access-control-allow-origin": "*", '
                 '"access-control-allow-credentials": "true" });\n'
                 't("https://api.ru/x", "same-origin", { "access-control-allow-origin": "https://app.ru" '
                 '});\n'
                 't("https://api.ru/x", "include", { "access-control-allow-origin": "https://app.ru" });\n'
                 't("https://api.ru/x", "include", { "access-control-allow-origin": "https://app.ru", '
                 '"access-control-allow-credentials": "true" });\n'
                 't("https://api.ru/x", "include", { "access-control-allow-origin": "https://app.ru", '
                 '"access-control-allow-credentials": "True" });\n'
                 't("https://api.ru/x", "omit", { "access-control-allow-origin": "https://other.ru" });\n'
                 't("http://app.ru/x", "omit", { "access-control-allow-origin": "https://app.ru" });\n',
       'hint': 'Сначала same-origin, затем значение Allow-Origin: отсутствует, «*», совпадает или нет.',
       'expected': ['https://app.ru/api         include      {} {"allowed":true,"reason":"same-origin"}',
                    'https://app.ru:8443/api    omit         {} {"allowed":false,"reason":"нет '
                    'Access-Control-Allow-Origin"}',
                    'https://api.ru/x           omit         {} {"allowed":false,"reason":"нет '
                    'Access-Control-Allow-Origin"}',
                    'https://api.ru/x           omit         {"access-control-allow-origin":"*"} '
                    '{"allowed":true,"reason":"ok"}',
                    'https://api.ru/x           include      '
                    '{"access-control-allow-credentials":"true","access-control-allow-origin":"*"} '
                    '{"allowed":false,"reason":"звёздочка недопустима с credentials"}',
                    'https://api.ru/x           same-origin  '
                    '{"access-control-allow-origin":"https://app.ru"} {"allowed":true,"reason":"ok"}',
                    'https://api.ru/x           include      '
                    '{"access-control-allow-origin":"https://app.ru"} {"allowed":false,"reason":"нет '
                    'Access-Control-Allow-Credentials"}',
                    'https://api.ru/x           include      '
                    '{"access-control-allow-credentials":"true","access-control-allow-origin":"https://app.ru"} '
                    '{"allowed":true,"reason":"ok"}',
                    'https://api.ru/x           include      '
                    '{"access-control-allow-credentials":"True","access-control-allow-origin":"https://app.ru"} '
                    '{"allowed":false,"reason":"нет Access-Control-Allow-Credentials"}',
                    'https://api.ru/x           omit         '
                    '{"access-control-allow-origin":"https://other.ru"} {"allowed":false,"reason":"источник '
                    'не совпадает"}',
                    'http://app.ru/x            omit         '
                    '{"access-control-allow-origin":"https://app.ru"} {"allowed":true,"reason":"ok"}']},
      {'id': 'j18-freshness',
       'mode': 'js',
       'title': 'Свежесть ответа в HTTP-кеше',
       'statement': 'Напишите функции parseCacheControl(header) и freshness(res, now). parseCacheControl → '
                    'объект: директивы без значения становятся true (имена в нижнем регистре: «no-store» → '
                    '"no-store": true), числовые — числами («max-age=60» → "max-age": 60), прочие — строками '
                    'без кавычек; пустой или не строка — {}. freshness(res, now): res = { headers (ключи в '
                    'нижнем регистре; могут быть cache-control, age (секунды), date, expires, '
                    'last-modified), storedAt (мс) } → { state, ttl, canServeStale }. state: «no-store» — '
                    'если no-store; «revalidate» — если no-cache; иначе считаем возраст age = now − storedAt '
                    '+ (заголовок age в секундах) × 1000 и срок жизни lifetime: max-age × 1000; иначе '
                    '(expires − date) в мс (если оба заданы, не меньше 0); иначе эвристика — 10% от (date − '
                    'last-modified), если оба заданы; иначе 0. age < lifetime → «fresh» (ttl = lifetime − '
                    'age); иначе «stale» (ttl = 0), а при must-revalidate — «revalidate». canServeStale — '
                    'true, только если state «stale» и задан stale-while-revalidate (секунды) и age − '
                    'lifetime < swr × 1000. Во всех остальных случаях ttl = 0 и canServeStale = false.',
       'starter': 'function parseCacheControl(header) {\n}\nfunction freshness(res, now) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'for (const h of ["max-age=60, public", "No-Cache, no-store", \'private, community="UCI", '
                 'max-age=0\', "", undefined, "stale-while-revalidate=30,must-revalidate", " max-age = 5 ,, '
                 'immutable"]) console.log(JSON.stringify(h), JSON.stringify(canon(parseCacheControl(h))));\n'
                 'const base = 1_000_000;\n'
                 'const f = (headers, now, extra = {}) => console.log(JSON.stringify(headers), now - base, '
                 'JSON.stringify(canon(freshness({ headers, storedAt: base, ...extra }, now))));\n'
                 'f({ "cache-control": "max-age=60" }, base + 10_000); f({ "cache-control": "max-age=60" }, '
                 'base + 60_000); f({ "cache-control": "max-age=60" }, base + 90_000);\n'
                 'f({ "cache-control": "max-age=60", age: "20" }, base + 30_000); f({ "cache-control": '
                 '"max-age=60", age: "20" }, base + 40_000);\n'
                 'f({ "cache-control": "no-store, max-age=60" }, base); f({ "cache-control": "no-cache, '
                 'max-age=60" }, base);\n'
                 'f({ "cache-control": "max-age=60, stale-while-revalidate=30" }, base + 80_000); f({ '
                 '"cache-control": "max-age=60, stale-while-revalidate=30" }, base + 95_000);\n'
                 'f({ "cache-control": "max-age=60, must-revalidate, stale-while-revalidate=30" }, base + '
                 '80_000);\n'
                 'f({ expires: "Wed, 21 Oct 2026 07:30:00 GMT", date: "Wed, 21 Oct 2026 07:28:00 GMT" }, '
                 'base + 100_000); f({ expires: "Wed, 21 Oct 2026 07:30:00 GMT", date: "Wed, 21 Oct 2026 '
                 '07:28:00 GMT" }, base + 130_000);\n'
                 'f({ expires: "Wed, 21 Oct 2026 07:00:00 GMT", date: "Wed, 21 Oct 2026 07:28:00 GMT" }, '
                 'base);\n'
                 'f({ "last-modified": "Wed, 21 Oct 2026 04:28:00 GMT", date: "Wed, 21 Oct 2026 07:28:00 '
                 'GMT" }, base + 1_000_000); f({ "last-modified": "Wed, 21 Oct 2026 04:28:00 GMT", date: '
                 '"Wed, 21 Oct 2026 07:28:00 GMT" }, base + 1_100_000);\n'
                 'f({}, base); f({ "cache-control": "max-age=60, expires-ignored" , expires: "x"}, base + '
                 '1);\n',
       'hint': 'Приоритет: no-store, no-cache, затем срок из max-age / expires / эвристики; сравните возраст '
               'со сроком.',
       'expected': ['"max-age=60, public" {"max-age":60,"public":true}',
                    '"No-Cache, no-store" {"no-cache":true,"no-store":true}',
                    '"private, community=\\"UCI\\", max-age=0" '
                    '{"community":"UCI","max-age":0,"private":true}',
                    '"" {}',
                    'undefined {}',
                    '"stale-while-revalidate=30,must-revalidate" '
                    '{"must-revalidate":true,"stale-while-revalidate":30}',
                    '" max-age = 5 ,, immutable" {"immutable":true,"max-age":5}',
                    '{"cache-control":"max-age=60"} 10000 '
                    '{"canServeStale":false,"state":"fresh","ttl":50000}',
                    '{"cache-control":"max-age=60"} 60000 {"canServeStale":false,"state":"stale","ttl":0}',
                    '{"cache-control":"max-age=60"} 90000 {"canServeStale":false,"state":"stale","ttl":0}',
                    '{"cache-control":"max-age=60","age":"20"} 30000 '
                    '{"canServeStale":false,"state":"fresh","ttl":10000}',
                    '{"cache-control":"max-age=60","age":"20"} 40000 '
                    '{"canServeStale":false,"state":"stale","ttl":0}',
                    '{"cache-control":"no-store, max-age=60"} 0 '
                    '{"canServeStale":false,"state":"no-store","ttl":0}',
                    '{"cache-control":"no-cache, max-age=60"} 0 '
                    '{"canServeStale":false,"state":"revalidate","ttl":0}',
                    '{"cache-control":"max-age=60, stale-while-revalidate=30"} 80000 '
                    '{"canServeStale":true,"state":"stale","ttl":0}',
                    '{"cache-control":"max-age=60, stale-while-revalidate=30"} 95000 '
                    '{"canServeStale":false,"state":"stale","ttl":0}',
                    '{"cache-control":"max-age=60, must-revalidate, stale-while-revalidate=30"} 80000 '
                    '{"canServeStale":false,"state":"revalidate","ttl":0}',
                    '{"expires":"Wed, 21 Oct 2026 07:30:00 GMT","date":"Wed, 21 Oct 2026 07:28:00 GMT"} '
                    '100000 {"canServeStale":false,"state":"fresh","ttl":20000}',
                    '{"expires":"Wed, 21 Oct 2026 07:30:00 GMT","date":"Wed, 21 Oct 2026 07:28:00 GMT"} '
                    '130000 {"canServeStale":false,"state":"stale","ttl":0}',
                    '{"expires":"Wed, 21 Oct 2026 07:00:00 GMT","date":"Wed, 21 Oct 2026 07:28:00 GMT"} 0 '
                    '{"canServeStale":false,"state":"stale","ttl":0}',
                    '{"last-modified":"Wed, 21 Oct 2026 04:28:00 GMT","date":"Wed, 21 Oct 2026 07:28:00 '
                    'GMT"} 1000000 {"canServeStale":false,"state":"fresh","ttl":80000}',
                    '{"last-modified":"Wed, 21 Oct 2026 04:28:00 GMT","date":"Wed, 21 Oct 2026 07:28:00 '
                    'GMT"} 1100000 {"canServeStale":false,"state":"stale","ttl":0}',
                    '{} 0 {"canServeStale":false,"state":"stale","ttl":0}',
                    '{"cache-control":"max-age=60, expires-ignored","expires":"x"} 1 '
                    '{"canServeStale":false,"state":"fresh","ttl":59999}']},
      {'id': 'j18-http-cache',
       'mode': 'js',
       'title': 'HTTP-кеш с условными запросами',
       'statement': 'Напишите функцию createHttpCache(origin, now): origin(url, headers) → промис { status, '
                    'headers (нижний регистр), body }; now() — время в мс. Возвращает { get(url) → промис { '
                    'body, from } }, где from — «network», «cache» или «revalidated». Алгоритм: нет записи → '
                    'запрос к origin без заголовков; ответ 200 сохраняется (storedAt = now()), если в '
                    'cache-control нет no-store (иначе не сохраняется; результат «network»). Запись есть: '
                    'если cache-control записи содержит max-age и age = now − storedAt < max-age × 1000 (без '
                    'no-cache) — вернуть из кеша без обращения к origin («cache»). Иначе — условный запрос: '
                    'заголовки if-none-match (если у записи есть etag) и if-modified-since (если есть '
                    'last-modified); ответ 304 — запись остаётся, storedAt = now(), заголовки '
                    'cache-control/etag/last-modified обновляются из ответа, если они там есть, возвращается '
                    'тело записи («revalidated»); ответ 200 — запись заменяется («network»); любой другой '
                    'статус — вернуть его как есть («network»), запись не менять; ошибка origin — '
                    'пробросить.',
       'starter': 'function createHttpCache(origin, now) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let t = 0; const log = [];\n'
                 'let version = 1;\n'
                 'const origin = async (url, headers) => {\n'
                 '  log.push(`${url} ${JSON.stringify(headers)}`);\n'
                 '  if (url === "/boom") throw new Error("сеть");\n'
                 '  if (url === "/gone") return { status: 404, headers: {}, body: "нет" };\n'
                 '  if (url === "/secret") return { status: 200, headers: { "cache-control": "no-store" }, '
                 'body: "секрет" };\n'
                 '  if (url === "/nocache") return headers["if-none-match"] === `"v${version}"` ? { status: '
                 '304, headers: {}, body: "" } : { status: 200, headers: { "cache-control": "no-cache", '
                 'etag: `"v${version}"` }, body: `данные v${version}` };\n'
                 '  if (headers["if-none-match"] === `"v${version}"` || (headers["if-modified-since"] && '
                 'version === 1)) return { status: 304, headers: { "cache-control": "max-age=10" }, body: "" '
                 '};\n'
                 '  return { status: 200, headers: { "cache-control": "max-age=10", etag: `"v${version}"`, '
                 '"last-modified": "Mon, 01 Jan 2024 00:00:00 GMT" }, body: `данные v${version}` };\n'
                 '};\n'
                 'const cache = createHttpCache(origin, () => t);\n'
                 'const g = async (url) => { const r = await cache.get(url); console.log(t, url, r.from, '
                 'r.body, r.status); };\n'
                 'await g("/a"); t = 5000; await g("/a"); t = 10000; await g("/a"); t = 19000; await '
                 'g("/a");\n'
                 'version = 2; t = 21000; await g("/a"); t = 22000; await g("/a");\n'
                 'await g("/secret"); await g("/secret"); await g("/gone"); await g("/gone");\n'
                 'await g("/nocache"); await g("/nocache"); version = 3; await g("/nocache"); await '
                 'g("/nocache");\n'
                 'try { await cache.get("/boom"); } catch (e) { console.log("ошибка", e.message); }\n'
                 'console.log(log.join("\\n"));\n',
       'hint': 'Map url → запись; при устаревании шлите условный запрос и обновляйте storedAt при 304.',
       'expected': ['0 /a network данные v1 200',
                    '5000 /a cache данные v1 200',
                    '10000 /a revalidated данные v1 200',
                    '19000 /a cache данные v1 200',
                    '21000 /a network данные v2 200',
                    '22000 /a cache данные v2 200',
                    '22000 /secret network секрет 200',
                    '22000 /secret network секрет 200',
                    '22000 /gone network нет 404',
                    '22000 /gone network нет 404',
                    '22000 /nocache network данные v2 200',
                    '22000 /nocache revalidated данные v2 200',
                    '22000 /nocache network данные v3 200',
                    '22000 /nocache revalidated данные v3 200',
                    'ошибка сеть',
                    '/a {}',
                    '/a {"if-none-match":"\\"v1\\"","if-modified-since":"Mon, 01 Jan 2024 00:00:00 GMT"}',
                    '/a {"if-none-match":"\\"v1\\"","if-modified-since":"Mon, 01 Jan 2024 00:00:00 GMT"}',
                    '/secret {}',
                    '/secret {}',
                    '/gone {}',
                    '/gone {}',
                    '/nocache {}',
                    '/nocache {"if-none-match":"\\"v2\\""}',
                    '/nocache {"if-none-match":"\\"v2\\""}',
                    '/nocache {"if-none-match":"\\"v3\\""}',
                    '/boom {}']},
      {'id': 'j18-swr',
       'mode': 'js',
       'title': 'Stale-while-revalidate на клиенте',
       'statement': 'Напишите функцию createSWR({ fetcher, now, ttl, staleTtl, onUpdate }): fetcher(key) → '
                    'промис; now() — мс. Возвращает { get(key), mutate(key, data), inflight() }. get(key) → '
                    'промис { data, state }: нет записи или возраст ≥ ttl + staleTtl → ждём fetcher («miss»; '
                    'ошибка отклоняет промис, запись не меняется); возраст < ttl → { data, state: "fresh" } '
                    'без запросов; ttl ≤ возраст < ttl + staleTtl → сразу { data, state: "stale" } и запуск '
                    'фонового обновления: по успеху запись обновляется (время = now()) и вызывается '
                    'onUpdate(key, data); ошибка фона молча игнорируется (старые данные остаются). '
                    'Одновременные запросы к одному ключу (и miss, и фон) используют один вызов fetcher; '
                    'если фоновое обновление уже идёт, новый get его не запускает и onUpdate не вызывает — '
                    'onUpdate срабатывает ровно один раз на обновление, которое запустил get. mutate '
                    'записывает данные вручную (время = now()). inflight() — число активных запросов.',
       'starter': 'function createSWR(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'let t = 0, calls = 0; const pend = []; const updates = [];\n'
                 'const fetcher = (key) => { calls++; return new Promise((res, rej) => pend.push({ key, res, '
                 'rej })); };\n'
                 'const swr = createSWR({ fetcher, now: () => t, ttl: 1000, staleTtl: 5000, onUpdate: (k, d) '
                 '=> updates.push(`${k}=${d}`) });\n'
                 'const p1 = swr.get("a"), p2 = swr.get("a"); await tick(); console.log(calls, '
                 'swr.inflight());\n'
                 'pend[0].res("v1"); console.log(JSON.stringify(await p1), JSON.stringify(await p2), '
                 'swr.inflight());\n'
                 't = 500; console.log(JSON.stringify(await swr.get("a")), calls);\n'
                 't = 2000; console.log(JSON.stringify(await swr.get("a")), JSON.stringify(await '
                 'swr.get("a"))); await tick(); console.log(calls, swr.inflight());\n'
                 'pend[1].res("v2"); await tick(); console.log(updates.join(), JSON.stringify(await '
                 'swr.get("a")), calls);\n'
                 't = 3500; const s = await swr.get("a"); await tick(); pend[2].rej(new Error("сбой")); '
                 'await tick(); console.log(JSON.stringify(s), updates.length, swr.inflight(), '
                 'JSON.stringify(await swr.get("a")));\n'
                 't = 3600; swr.mutate("a", "ручное"); console.log(JSON.stringify(await swr.get("a")));\n'
                 't = 20000; const m = swr.get("a"); await tick(); pend[pend.length - 1].rej(new '
                 'Error("сеть")); try { await m; } catch (e) { console.log("miss-ошибка", e.message); }\n'
                 'const m2 = swr.get("a"); await tick(); pend[pend.length - 1].res("новое"); '
                 'console.log(JSON.stringify(await m2), calls);\n'
                 'const n = swr.get("b"); await tick(); console.log(swr.inflight()); pend[pend.length - '
                 '1].res("B"); await n; t = 20000 + 7000; const last = swr.get("b"); await tick(); '
                 'pend[pend.length - 1].res("B2"); console.log(JSON.stringify(await '
                 'last).includes("miss"));\n',
       'hint': 'Кеш {data, at} и таблица «ключ → промис в полёте»; фон — без await и с проглатыванием '
               'ошибки.',
       'expected': ['1 1',
                    '{"data":"v1","state":"miss"} {"data":"v1","state":"miss"} 0',
                    '{"data":"v1","state":"fresh"} 1',
                    '{"data":"v1","state":"stale"} {"data":"v1","state":"stale"}',
                    '2 1',
                    'a=v2 {"data":"v2","state":"fresh"} 2',
                    '{"data":"v2","state":"stale"} 1 0 {"data":"v2","state":"stale"}',
                    '{"data":"ручное","state":"fresh"}',
                    'miss-ошибка сеть',
                    '{"data":"новое","state":"miss"} 5',
                    '1',
                    'true']},
      {'id': 'j18-dedupe',
       'mode': 'js',
       'title': 'Объединение одинаковых запросов',
       'statement': 'Напишите функцию dedupe(fn, keyFn = (...args) => JSON.stringify(args)): возвращает '
                    'функцию wrapped(...args) → промис. Пока вызов fn с данным ключом ещё не завершён, '
                    'повторные вызовы с тем же ключом возвращают тот же промис (fn не вызывается снова). '
                    'После завершения (успешного или нет) ключ освобождается, и следующий вызов запускает fn '
                    'заново. Разные ключи не мешают друг другу. wrapped.pending() — число незавершённых '
                    'ключей. Синхронные исключения fn превращаются в отклонённый промис.',
       'starter': 'function dedupe(fn, keyFn) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'let calls = 0; const gates = [];\n'
                 'const load = (id, fail) => { calls++; return new Promise((res, rej) => gates.push(() => '
                 '(fail ? rej(new Error("сбой " + id)) : res("данные " + id)))); };\n'
                 'const d = dedupe(load);\n'
                 'const a = d(1), b = d(1), c = d(2), e = d(1);\n'
                 'console.log(a === b, a === e, a === c, calls, d.pending());\n'
                 'gates[0](); console.log(await a, await b, d.pending()); gates[1](); await c; '
                 'console.log(d.pending());\n'
                 'const again = d(1); console.log(again === a, calls); gates[2]();  await again;\n'
                 'const f1 = d(9, true), f2 = d(9, true); f1.catch(() => {}); console.log(f1 === f2, '
                 'd.pending()); gates[3](); try { await f1; } catch (x) { console.log(x.message, '
                 'd.pending()); }\n'
                 'const f3 = d(9, true); f3.catch(() => {}); console.log(calls);\n'
                 'gates[4]();\n'
                 'const throwing = dedupe(() => { throw new Error("синхронно"); }); const tp = throwing(); '
                 'try { await tp; } catch (x) { console.log(x.message, throwing.pending()); }\n'
                 'const byUser = dedupe((u, n) => Promise.resolve(u + n), (u) => u); const x1 = '
                 'byUser("ann", 1), x2 = byUser("ann", 2); console.log(x1 === x2, await x1, await x2);\n'
                 'await tick(); console.log(byUser.pending());\n',
       'hint': 'Map ключ → промис; в finally удаляйте ключ.',
       'expected': ['true true false 2 2',
                    'данные 1 данные 1 1',
                    '0',
                    'false 3',
                    'true 1',
                    'сбой 9 0',
                    '5',
                    'синхронно 0',
                    'true ann1 ann1',
                    '0']},
      {'id': 'j18-auth-refresh',
       'mode': 'js',
       'title': 'Обновление токена при 401',
       'statement': 'Напишите функцию createAuthClient({ token, request, refresh, onLogout }): request(req, '
                    'token) → промис { status, body }; refresh() → промис нового токена; onLogout() '
                    'вызывается при окончательной потере доступа. Возвращает { call(req) → промис { status, '
                    'body }, token() → текущий токен }. Алгоритм: call выполняет request(req, текущий '
                    'токен). Если ответ не 401 — вернуть его. Если 401 и токен с момента отправки уже '
                    'сменился (другой параллельный вызов обновил) — просто повторить с текущим токеном. '
                    'Иначе запустить refresh() — при параллельных 401 обновление запускается один раз и '
                    'делится между ожидающими; новый токен сохраняется. Затем повторить запрос один раз с '
                    'новым токеном: если и он дал 401 — вызвать onLogout() (один раз на всех) и отклонить '
                    'Error("unauthorized"). Если refresh отклонился — тоже onLogout() (один раз) и '
                    'Error("unauthorized"). Повторный запрос после успешного обновления не вызывает ещё '
                    'одного обновления.',
       'starter': 'function createAuthClient(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'const mk = (valid, refreshImpl) => {\n'
                 '  const log = { requests: [], refreshes: 0, logouts: 0 };\n'
                 '  const client = createAuthClient({ token: "t0", request: async (req, tok) => { '
                 'log.requests.push(`${req}:${tok}`); await tick(); return valid.has(tok) ? { status: 200, '
                 'body: `${req} ок` } : { status: 401, body: "" }; }, refresh: async () => { '
                 'log.refreshes++; await tick(); return refreshImpl(log.refreshes); }, onLogout: () => '
                 'log.logouts++ });\n'
                 '  return { client, log };\n'
                 '};\n'
                 'const show = async (label, p) => { try { const r = await p; console.log(label, r.status, '
                 'r.body); } catch (e) { console.log(label, "ошибка", e.message); } };\n'
                 '{ const { client, log } = mk(new Set(["t0"]), () => "t1"); await show("валидный", '
                 'client.call("a")); console.log(log.requests.join(), log.refreshes, client.token()); }\n'
                 '{ const { client, log } = mk(new Set(["t1"]), () => "t1"); await show("одиночный 401", '
                 'client.call("a")); console.log(log.requests.join(), log.refreshes, log.logouts, '
                 'client.token()); }\n'
                 '{ const { client, log } = mk(new Set(["t1"]), () => "t1"); await Promise.all([show("p1", '
                 'client.call("a")), show("p2", client.call("b")), show("p3", client.call("c"))]); '
                 'console.log(log.requests.join(), log.refreshes, log.logouts); await show("после", '
                 'client.call("d")); console.log(log.refreshes); }\n'
                 '{ const { client, log } = mk(new Set(), () => "t1"); await Promise.all([show("q1", '
                 'client.call("a")), show("q2", client.call("b"))]); console.log(log.requests.join(), '
                 'log.refreshes, log.logouts); }\n'
                 '{ const { client, log } = mk(new Set(["t1"]), () => { throw new Error("refresh упал"); }); '
                 'await Promise.all([show("r1", client.call("a")), show("r2", client.call("b"))]); '
                 'console.log(log.requests.join(), log.refreshes, log.logouts, client.token()); }\n',
       'hint': 'Один общий промис обновления; запоминайте токен, с которым ушёл запрос, чтобы понять, что '
               'его уже сменили.',
       'expected': ['валидный 200 a ок',
                    'a:t0 0 t0',
                    'одиночный 401 200 a ок',
                    'a:t0,a:t1 1 0 t1',
                    'p1 200 a ок',
                    'p2 200 b ок',
                    'p3 200 c ок',
                    'a:t0,b:t0,c:t0,a:t1,b:t1,c:t1 1 0',
                    'после 200 d ок',
                    '1',
                    'q1 ошибка unauthorized',
                    'q2 ошибка unauthorized',
                    'a:t0,b:t0,a:t1,b:t1 1 1',
                    'r1 ошибка unauthorized',
                    'r2 ошибка unauthorized',
                    'a:t0,b:t0 1 1 t0']},
      {'id': 'j18-ws-frame',
       'mode': 'js',
       'title': 'Кадры WebSocket',
       'statement': 'Напишите функции encodeFrame({ fin = true, opcode, payload, maskKey = null }) → '
                    'Uint8Array и decodeFrame(bytes) по RFC 6455. payload — строка (кодируется UTF-8) или '
                    'Uint8Array; opcode — число (1 текст, 2 бинарный, 8 закрытие, 9 пинг, 10 понг). Формат: '
                    'байт 0 = (fin ? 0x80 : 0) | opcode; байт 1 = (маска ? 0x80 : 0) | длина, где длина < '
                    '126 — сама длина; от 126 до 65535 — значение 126 и затем 2 байта длины (big-endian); '
                    'больше — значение 127 и 8 байт; затем, если есть маска (maskKey — 4 байта), сам ключ, '
                    'затем данные (при маске каждый байт данных xor ключ[i % 4]). decodeFrame возвращает '
                    'null, если байт не хватает для полного кадра, иначе { fin, opcode, masked, payload '
                    '(Uint8Array, уже без маски), length (сколько байт кадра прочитано), text } — text есть '
                    'только у opcode 1 (строка UTF-8). После кадра в буфере могут идти другие данные — их не '
                    'трогать.',
       'starter': 'function encodeFrame(frame) {\n}\nfunction decodeFrame(bytes) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const hex = (u) => [...u].map((b) => b.toString(16).padStart(2, "0")).join(" ");\n'
                 'console.log(hex(encodeFrame({ opcode: 1, payload: "Hello" })));\n'
                 'console.log(hex(encodeFrame({ opcode: 1, payload: "Hello", maskKey: new Uint8Array([0x37, '
                 '0xfa, 0x21, 0x3d]) })));\n'
                 'console.log(hex(encodeFrame({ opcode: 9, payload: "" })), "|", hex(encodeFrame({ fin: '
                 'false, opcode: 2, payload: new Uint8Array([1, 2, 3]) })), "|", hex(encodeFrame({ opcode: '
                 '8, payload: new Uint8Array([3, 232]) })));\n'
                 'for (const n of [125, 126, 65535, 65536]) { const f = encodeFrame({ opcode: 2, payload: '
                 'new Uint8Array(n).fill(7) }); console.log(n, hex(f.slice(0, 11)), f.length); }\n'
                 'const d1 = decodeFrame(encodeFrame({ opcode: 1, payload: "Привет 😀", maskKey: new '
                 'Uint8Array([1, 2, 3, 4]) }));\n'
                 'console.log(d1.fin, d1.opcode, d1.masked, d1.text, d1.length, d1.payload.length);\n'
                 'const two = new Uint8Array([...encodeFrame({ opcode: 1, payload: "a" }), ...encodeFrame({ '
                 'opcode: 10, payload: "p" })]);\n'
                 'const f1 = decodeFrame(two); const f2 = decodeFrame(two.slice(f1.length)); '
                 'console.log(f1.text, f1.length, f2.opcode, f2.text, f2.length, f2.payload[0]);\n'
                 'const full = encodeFrame({ opcode: 1, payload: "x".repeat(300), maskKey: new '
                 'Uint8Array([9, 9, 9, 9]) });\n'
                 'console.log([0, 1, 2, 3, 4, 7, 100, full.length - 1].map((n) => decodeFrame(full.slice(0, '
                 'n))).map((r) => (r ? "кадр" : "ждать")).join(), decodeFrame(full).text.length, '
                 'decodeFrame(full).length === full.length);\n'
                 'const big = decodeFrame(encodeFrame({ opcode: 2, payload: new Uint8Array(70000).fill(5) '
                 '})); console.log(big.payload.length, big.length, big.text);\n'
                 'console.log(decodeFrame(new Uint8Array([0x01, 0x00])).fin, decodeFrame(new '
                 'Uint8Array([0x01, 0x00])).opcode, decodeFrame(new Uint8Array([0x01, '
                 '0x00])).payload.length);\n',
       'hint': 'Первые два байта — флаги и длина; расширенная длина и маска идут дальше; сначала проверяйте, '
               'хватает ли байт.',
       'expected': ['81 05 48 65 6c 6c 6f',
                    '81 85 37 fa 21 3d 7f 9f 4d 51 58',
                    '89 00 | 02 03 01 02 03 | 88 02 03 e8',
                    '125 82 7d 07 07 07 07 07 07 07 07 07 127',
                    '126 82 7e 00 7e 07 07 07 07 07 07 07 130',
                    '65535 82 7e ff ff 07 07 07 07 07 07 07 65539',
                    '65536 82 7f 00 00 00 00 00 01 00 00 07 65546',
                    'true 1 true Привет 😀 23 17',
                    'a 3 10 undefined 3 112',
                    'ждать,ждать,ждать,ждать,ждать,ждать,ждать,ждать 300 true',
                    '70000 70010 undefined',
                    'false 1 0']},
      {'id': 'j18-ws-accept',
       'mode': 'js',
       'title': 'Рукопожатие WebSocket на сервере',
       'statement': 'Напишите функции computeAccept(key) (async) и validateHandshake(req) (async). '
                    'computeAccept: base64 от SHA-1 строки key + «258EAFA5-E914-47DA-95CA-C5AB0DC85B11» '
                    '(используйте crypto.subtle.digest и btoa). validateHandshake({ method, headers }) '
                    '(ключи headers в нижнем регистре) → { ok, status, headers, accept? }. Проверки по '
                    'порядку: метод GET (иначе 405); upgrade без учёта регистра равен «websocket» (иначе '
                    '400); connection содержит токен «upgrade» (токены через запятую, регистр не важен; '
                    'иначе 400); sec-websocket-version равна «13» (иначе 426 и headers { '
                    '"sec-websocket-version": "13" }); sec-websocket-key — base64 ровно от 16 байт (22 '
                    'символа и «==»; иначе 400). Успех: { ok: true, status: 101, headers: { upgrade: '
                    '"websocket", connection: "Upgrade", "sec-websocket-accept": <accept> } }. Для ошибок '
                    'headers — {} (кроме 426), ok: false.',
       'starter': 'async function computeAccept(key) {\n}\nasync function validateHandshake(req) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'console.log(await computeAccept("dGhlIHNhbXBsZSBub25jZQ=="), await '
                 'computeAccept("x3JJHMbDL1EzLkh9GBhXDw=="));\n'
                 'const good = { upgrade: "WebSocket", connection: "keep-alive, Upgrade", '
                 '"sec-websocket-version": "13", "sec-websocket-key": "dGhlIHNhbXBsZSBub25jZQ==" };\n'
                 'const show = async (label, req) => console.log(label.padEnd(14), '
                 'JSON.stringify(canon(await validateHandshake(req))));\n'
                 'await show("ok", { method: "GET", headers: good });\n'
                 'await show("post", { method: "POST", headers: good });\n'
                 'await show("без upgrade", { method: "GET", headers: { ...good, upgrade: undefined } });\n'
                 'await show("другой upgrade", { method: "GET", headers: { ...good, upgrade: "h2c" } });\n'
                 'await show("connection", { method: "GET", headers: { ...good, connection: "close" } });\n'
                 'await show("версия 8", { method: "GET", headers: { ...good, "sec-websocket-version": "8" } '
                 '});\n'
                 'await show("ключ короткий", { method: "GET", headers: { ...good, "sec-websocket-key": '
                 '"abc==" } });\n'
                 'await show("нет ключа", { method: "GET", headers: { ...good, "sec-websocket-key": '
                 'undefined } });\n'
                 'await show("get в нижнем", { method: "get", headers: { ...good, connection: "UPGRADE" } '
                 '});\n',
       'hint': 'Проверяйте по порядку: метод, upgrade, connection, версия, ключ; sha-1 считает '
               'crypto.subtle.',
       'expected': ['s3pPLMBiTxaQ9kYGzzhZRbK+xOo= HSmrc0sMlYUkAGmm5OPpG2HaGWk=',
                    'ok             '
                    '{"headers":{"connection":"Upgrade","sec-websocket-accept":"s3pPLMBiTxaQ9kYGzzhZRbK+xOo=","upgrade":"websocket"},"ok":true,"status":101}',
                    'post           {"headers":{},"ok":false,"status":405}',
                    'без upgrade    {"headers":{},"ok":false,"status":400}',
                    'другой upgrade {"headers":{},"ok":false,"status":400}',
                    'connection     {"headers":{},"ok":false,"status":400}',
                    'версия 8       {"headers":{"sec-websocket-version":"13"},"ok":false,"status":426}',
                    'ключ короткий  {"headers":{},"ok":false,"status":400}',
                    'нет ключа      {"headers":{},"ok":false,"status":400}',
                    'get в нижнем   '
                    '{"headers":{"connection":"Upgrade","sec-websocket-accept":"s3pPLMBiTxaQ9kYGzzhZRbK+xOo=","upgrade":"websocket"},"ok":true,"status":101}']},
      {'id': 'j18-ws-client',
       'mode': 'js',
       'title': 'Клиент WebSocket с переподключением',
       'statement': 'Напишите функцию createSocketClient({ WS, url, timers, baseDelay = 1000, maxDelay = '
                    '8000, pingInterval = 5000, pongTimeout = 2000 }): WS — конструктор сокета (new WS(url) '
                    'с полями onopen, onmessage(e) (e.data), onclose(e) (e.code) и методами send(data), '
                    'close(code)); timers = { setTimeout, clearTimeout }. Клиент подключается сразу. API: '
                    'send(msg) (в состоянии «open» — ws.send, иначе сообщение копится в очереди и уходит по '
                    'порядку при открытии; в состоянии «closed» — бросить Error("Сокет закрыт")), on(event, '
                    'fn) для событий «open», «message» (fn(data)), «reconnect» (fn({ attempt, delay })), '
                    'close(), и state: «connecting» → «open»; при обрыве «reconnecting»; после close() — '
                    '«closed». Пока соединение открыто, каждые pingInterval отправляется «ping»; если за '
                    'pongTimeout не пришёл «pong» (такое сообщение не передаётся подписчикам) — вызвать '
                    'ws.close(4000). При обрыве (событие close, если не close() клиента) попытка n (с 0) '
                    'переподключается через min(maxDelay, baseDelay × 2ⁿ); счётчик попыток сбрасывается при '
                    'успешном открытии. События старых сокетов игнорируются. close() клиента: '
                    'ws.close(1000), снимает все таймеры, переподключений больше нет.',
       'starter': 'function createSocketClient(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const FAKE = () => { let t = 0; const timers = new Map(); let id = 1; return { now: () => '
                 't, setTimeout(fn, ms) { const i = id++; timers.set(i, { at: t + ms, fn }); return i; }, '
                 'clearTimeout(i) { timers.delete(i); }, advance(ms) { const end = t + ms; for (;;) { const '
                 'due = [...timers].filter(([, x]) => x.at <= end).sort((a, b) => a[1].at - b[1].at || a[0] '
                 '- b[0])[0]; if (!due) break; timers.delete(due[0]); t = due[1].at; due[1].fn(); } t = end; '
                 '}, pending: () => timers.size }; };\n'
                 'class FakeWS { static all = []; constructor(url) { this.url = url; this.sent = []; '
                 'this.closed = null; FakeWS.all.push(this); } send(d) { this.sent.push(d); } close(code) { '
                 'this.closed = code; this.onclose?.({ code }); } open() { this.onopen?.(); } msg(d) { '
                 'this.onmessage?.({ data: d }); } drop(code = 1006) { this.onclose?.({ code }); } }\n'
                 'const clock = FAKE(); const log = [];\n'
                 'const c = createSocketClient({ WS: FakeWS, url: "wss://x.ru/ws", timers: clock, baseDelay: '
                 '100, maxDelay: 400, pingInterval: 1000, pongTimeout: 200 });\n'
                 'c.on("open", () => log.push("open")); c.on("message", (d) => log.push("msg:" + d)); '
                 'c.on("reconnect", (r) => log.push(`reconnect:${r.attempt}:${r.delay}`));\n'
                 'const s = () => `${c.state} сокетов=${FakeWS.all.length} таймеров=${clock.pending()}`;\n'
                 'console.log(s(), FakeWS.all[0].url); c.send("a"); c.send("b"); '
                 'console.log(JSON.stringify(FakeWS.all[0].sent));\n'
                 'FakeWS.all[0].open(); console.log(s(), JSON.stringify(FakeWS.all[0].sent)); c.send("c"); '
                 'console.log(JSON.stringify(FakeWS.all[0].sent));\n'
                 'FakeWS.all[0].msg("hello"); FakeWS.all[0].msg("pong"); console.log(log.join());\n'
                 'clock.advance(1000); console.log(JSON.stringify(FakeWS.all[0].sent.slice(-1)), s()); '
                 'FakeWS.all[0].msg("pong"); clock.advance(200); console.log(FakeWS.all[0].closed, '
                 'c.state);\n'
                 'clock.advance(800); console.log(JSON.stringify(FakeWS.all[0].sent.slice(-1)), '
                 'FakeWS.all[0].closed, c.state); clock.advance(200); console.log(FakeWS.all[0].closed, '
                 'c.state, FakeWS.all.length, log.slice(-1).join());\n'
                 'c.send("d"); clock.advance(100); console.log(s(), JSON.stringify(FakeWS.all[1].sent)); '
                 'FakeWS.all[1].open(); console.log(c.state, JSON.stringify(FakeWS.all[1].sent));\n'
                 'FakeWS.all[1].drop(); console.log(c.state, log.slice(-1).join()); clock.advance(100); '
                 'FakeWS.all[2].drop(); clock.advance(200); FakeWS.all[3].drop(); clock.advance(400); '
                 'FakeWS.all[4].drop(); clock.advance(400);\n'
                 'console.log(log.filter((x) => x.startsWith("reconnect")).join(), FakeWS.all.length, '
                 'c.state);\n'
                 'FakeWS.all[5].open(); FakeWS.all[5].drop(); console.log(log.slice(-1).join()); '
                 'FakeWS.all[1].drop(); FakeWS.all[1].msg("старый"); console.log(log.includes("msg:старый"), '
                 'FakeWS.all.length);\n'
                 'clock.advance(100); FakeWS.all[6].open(); c.close(); console.log(c.state, '
                 'FakeWS.all[6].closed, clock.pending()); clock.advance(100000); '
                 'console.log(FakeWS.all.length, JSON.stringify(FakeWS.all[6].sent));\n'
                 'try { c.send("x"); } catch (e) { console.log(e.message); }\n',
       'hint': 'Таймеры ping, pong и reconnect храните отдельно; в обработчиках сравнивайте сокет с текущим.',
       'expected': ['connecting сокетов=1 таймеров=0 wss://x.ru/ws',
                    '[]',
                    'open сокетов=1 таймеров=1 ["a","b"]',
                    '["a","b","c"]',
                    'open,msg:hello',
                    '["ping"] open сокетов=1 таймеров=2',
                    'null open',
                    '["ping"] null open',
                    '4000 reconnecting 1 reconnect:1:100',
                    'reconnecting сокетов=2 таймеров=0 []',
                    'open ["d"]',
                    'reconnecting reconnect:1:100',
                    'reconnect:1:100,reconnect:1:100,reconnect:2:200,reconnect:3:400,reconnect:4:400 6 '
                    'reconnecting',
                    'reconnect:1:100',
                    'false 6',
                    'closed 1000 0',
                    '7 []',
                    'Сокет закрыт']},
      {'id': 'j18-sse-parser',
       'mode': 'js',
       'title': 'Парсер потока Server-Sent Events',
       'statement': 'Напишите функцию createSSEParser() → { feed(chunk) → массив событий, lastEventId() }. '
                    'chunk — строка (кусок потока, может резать строку и даже пару «\\r\\n» посередине). '
                    'Окончание строки — «\\n», «\\r» или «\\r\\n». Правила: пустая строка — конец события; '
                    'строка с «:» в начале — комментарий; иначе «поле: значение» (один пробел после '
                    'двоеточия отбрасывается; строка без двоеточия — поле целиком и пустое значение). Поля: '
                    'data (повторы объединяются через «\\n»), event (тип; по умолчанию «message»), id '
                    '(запоминается как lastEventId, если не содержит символ \\u0000; сохраняется между '
                    'событиями), retry (только цифры → число, иначе игнор). Событие создаётся только если '
                    'было хотя бы одно поле data: { type, data, lastEventId, retry? } (retry — только если '
                    'поле было в этом блоке). Блок без data сбрасывается. Начальный BOM (\ufeff) в потоке '
                    'отбрасывается. Незавершённый блок в конце потока теряется.',
       'starter': 'function createSSEParser() {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const all = (chunks) => { const p = createSSEParser(); const out = []; for (const c of '
                 'chunks) out.push(...p.feed(c)); return JSON.stringify(out.map(canon)) + " id=" + '
                 'p.lastEventId(); };\n'
                 'const text = "id: 1\\nevent: price\\ndata: 93\\n\\n: комментарий\\ndata: строка1\\ndata: '
                 'строка2\\n\\nretry: 5000\\ndata\\n\\nretry: abc\\nid: 7\\ndata:   пробелы\\n\\nevent: '
                 'нет-data\\n\\ndata: после\\n\\n";\n'
                 'console.log(all([text]));\n'
                 'for (const n of [1, 2, 3, 7]) console.log(n, all(text.match(new RegExp(`[^]{1,${n}}`, '
                 '"g"))) === all([text]));\n'
                 'console.log(all(["data: a\\r\\n\\r\\ndata: b\\r\\rdata: c\\n\\n"]), all(["data: a\\r", '
                 '"\\n\\r", "\\ndata: b\\r", "\\r"]));\n'
                 'console.log(all(["\ufeffdata: bom\\n\\n"]), all(["data: нет конца\\n"]), all(["data: '
                 'x\\n\\nid: 5\\n\\ndata: y\\n\\n"]), all(["id: a\\u0000b\\ndata: z\\n\\n"]));\n'
                 'console.log(all(["data:нет пробела\\n\\n", "data:  два\\n\\n", "event\\ndata: тип '
                 'пустой\\n\\n", "ev: игнор\\ndata: q\\n\\n"]));\n'
                 'const p = createSSEParser(); console.log(JSON.stringify(p.feed("data: 1\\n")), '
                 'JSON.stringify(p.feed("\\n")), JSON.stringify(p.feed("")), p.lastEventId() === "");\n',
       'hint': 'Накапливайте буфер; строку, оканчивающуюся на одиночный «\\r» в самом конце буфера, не '
               'разбирайте — дождитесь следующего куска.',
       'expected': ['[{"data":"93","lastEventId":"1","type":"price"},{"data":"строка1\\nстрока2","lastEventId":"1","type":"message"},{"data":"","lastEventId":"1","retry":5000,"type":"message"},{"data":"  '
                    'пробелы","lastEventId":"7","type":"message"},{"data":"после","lastEventId":"7","type":"message"}] '
                    'id=7',
                    '1 true',
                    '2 true',
                    '3 true',
                    '7 true',
                    '[{"data":"a","lastEventId":"","type":"message"},{"data":"b","lastEventId":"","type":"message"},{"data":"c","lastEventId":"","type":"message"}] '
                    'id= [{"data":"a","lastEventId":"","type":"message"}] id=',
                    '[{"data":"bom","lastEventId":"","type":"message"}] id= [] id= '
                    '[{"data":"x","lastEventId":"","type":"message"},{"data":"y","lastEventId":"5","type":"message"}] '
                    'id=5 [{"data":"z","lastEventId":"","type":"message"}] id=',
                    '[{"data":"нет пробела","lastEventId":"","type":"message"},{"data":" '
                    'два","lastEventId":"","type":"message"},{"data":"тип '
                    'пустой","lastEventId":"","type":"message"},{"data":"q","lastEventId":"","type":"message"}] '
                    'id=',
                    '[] [{"type":"message","data":"1","lastEventId":""}] [] true']},
      {'id': 'j18-sse-client',
       'mode': 'js',
       'title': 'Клиент EventSource с переподключением',
       'statement': 'Напишите функцию createSSEClient({ connect, createParser, timers, onEvent }): '
                    'connect(headers) → промис { status, chunks } (chunks — асинхронный итерируемый поток '
                    'строк); createParser() — как в предыдущем разборе: parser.feed(chunk) → события { type, '
                    'data, lastEventId, retry? }; timers = { setTimeout, clearTimeout }. Возвращает { '
                    'start(), stop(), delay() }. Цикл: connect({ accept: "text/event-stream", '
                    '"cache-control": "no-cache" }) плюс заголовок "last-event-id" с последним полученным '
                    'id, если он непустой. Статус 204 — остановиться навсегда; статус не 200 или ошибка '
                    'подключения — ждать delay и повторить; для 200 читать chunks, для каждого события: если '
                    'есть retry — запомнить как новую задержку, затем вызвать onEvent(event). Парсер '
                    'создаётся заново на каждое соединение, id запоминается между соединениями. Когда поток '
                    'закончился или оборвался (в том числе ошибкой) — ждать delay (по умолчанию 3000) и '
                    'подключаться снова. stop() останавливает всё немедленно, в том числе ожидание. delay() '
                    '— текущая задержка.',
       'starter': 'function createSSEClient(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const FAKE = () => { let t = 0; const timers = new Map(); let id = 1; return { now: () => '
                 't, setTimeout(fn, ms) { const i = id++; timers.set(i, { at: t + ms, fn }); return i; }, '
                 'clearTimeout(i) { timers.delete(i); }, advance(ms) { const end = t + ms; for (;;) { const '
                 'due = [...timers].filter(([, x]) => x.at <= end).sort((a, b) => a[1].at - b[1].at || a[0] '
                 '- b[0])[0]; if (!due) break; timers.delete(due[0]); t = due[1].at; due[1].fn(); } t = end; '
                 '}, pending: () => timers.size }; };\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'const parserFactory = () => { let buf = ""; let id = ""; return { feed(chunk) { buf += '
                 'chunk; const out = []; let i; while ((i = buf.indexOf("\\n\\n")) !== -1) { const block = '
                 'buf.slice(0, i); buf = buf.slice(i + 2); const ev = { type: "message", data: "", '
                 'lastEventId: id }; for (const l of block.split("\\n")) { const [k, ...v] = l.split(":"); '
                 'const val = v.join(":").trim(); if (k === "data") ev.data = val; else if (k === "id") { id '
                 '= val; ev.lastEventId = val; } else if (k === "retry") ev.retry = Number(val); else if (k '
                 '=== "event") ev.type = val; } out.push(ev); } return out; } }; };\n'
                 'const clock = FAKE(); const script = []; const reqs = []; const got = [];\n'
                 'async function* gen(parts, fail) { for (const p of parts) { await tick(); yield p; } if '
                 '(fail) throw new Error("обрыв"); }\n'
                 'const connect = async (headers) => { reqs.push(JSON.stringify(headers)); const next = '
                 'script.shift(); if (!next) return { status: 200, chunks: gen([], false) }; if '
                 '(next.throws) throw new Error("нет сети"); return { status: next.status, chunks: '
                 'next.parts ? gen(next.parts, next.fail) : null }; };\n'
                 'const c = createSSEClient({ connect, createParser: parserFactory, timers: clock, onEvent: '
                 '(e) => got.push(`${e.type}:${e.data}:${e.lastEventId}`) });\n'
                 'script.push({ status: 200, parts: ["id: 1\\ndata: ", "a\\n\\nid: 2\\ndata: b\\n\\n"], '
                 'fail: true });\n'
                 'script.push({ status: 500 });\n'
                 'script.push({ status: 200, parts: ["retry: 500\\ndata: c\\n\\n"], fail: false });\n'
                 'script.push({ throws: true });\n'
                 'script.push({ status: 200, parts: ["event: ping\\ndata: d\\n\\nid: 9\\ndata: e\\n\\n"] '
                 '});\n'
                 'c.start(); c.start(); await tick(); await tick(); await tick(); await tick(); await '
                 'tick();\n'
                 'console.log(got.join("|"), reqs.length, c.delay(), clock.pending());\n'
                 'clock.advance(3000); await tick(); console.log(reqs.length, reqs[1]); await tick(); '
                 'console.log(clock.pending());\n'
                 'clock.advance(3000); for (let i = 0; i < 6; i++) await tick(); console.log(reqs.length, '
                 'reqs[2], c.delay(), got.slice(-1).join(), clock.pending());\n'
                 'clock.advance(499); await tick(); console.log(reqs.length); clock.advance(1); for (let i = '
                 '0; i < 4; i++) await tick(); console.log(reqs.length, clock.pending());\n'
                 'clock.advance(500); for (let i = 0; i < 8; i++) await tick(); console.log(reqs.length, '
                 'reqs[reqs.length - 1], got.slice(-3).join("|"));\n'
                 'c.stop(); console.log(clock.pending()); clock.advance(100000); for (let i = 0; i < 4; i++) '
                 'await tick(); console.log(reqs.length);\n'
                 'const c2 = createSSEClient({ connect, createParser: parserFactory, timers: clock, onEvent: '
                 '() => {} }); script.push({ status: 204 }); c2.start(); await tick(); await tick(); '
                 'clock.advance(100000); await tick(); console.log(reqs.length, clock.pending());\n',
       'hint': 'Асинхронный цикл: подключение → чтение чанков → ожидание → снова; в ожидании должен работать '
               'stop().',
       'expected': ['message:a:1|message:b:2 1 3000 1',
                    '2 {"accept":"text/event-stream","cache-control":"no-cache","last-event-id":"2"}',
                    '1',
                    '3 {"accept":"text/event-stream","cache-control":"no-cache","last-event-id":"2"} 500 '
                    'message:c: 1',
                    '3',
                    '4 1',
                    '5 {"accept":"text/event-stream","cache-control":"no-cache","last-event-id":"2"} '
                    'message:c:|ping:d:|message:e:9',
                    '0',
                    '5',
                    '6 0']}]}
