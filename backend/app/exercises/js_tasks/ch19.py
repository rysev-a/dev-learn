"""Задачи книги «Современный Frontend», глава 19 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {19: [{'id': 'j19-deep-clone',
       'mode': 'js',
       'title': 'Структурное клонирование',
       'statement': 'Напишите функцию deepClone(value) — упрощённый structuredClone (самим structuredClone '
                    'пользоваться нельзя). Поддержка: примитивы (включая undefined, NaN, BigInt, null), Date '
                    '(новый объект с тем же временем), RegExp (source и flags, lastIndex = 0), Map, Set, '
                    'массивы, простые объекты (только собственные перечисляемые строковые ключи; прототип '
                    'теряется — экземпляры классов становятся обычными объектами), ArrayBuffer и '
                    'типизированные массивы (копия данных). Общие ссылки сохраняются: если один объект '
                    'встречается дважды, в копии это тоже один объект; циклические ссылки поддерживаются. '
                    'Функции и символы (в любом месте, в том числе внутри структур) — Error с name '
                    '«DataCloneError» и message «Невозможно клонировать: function» / «symbol».',
       'starter': 'function deepClone(value) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'const e = (f) => { try { f(); return "ok"; } catch (x) { return x.name + ": " + x.message; '
                 '} };\n'
                 'const shared = { n: 1 };\n'
                 'const src = { d: new Date(86400000), r: /a+b/gi, m: new Map([["k", { v: 1 }], [shared, '
                 '"ключ-объект"]]), s: new Set([1, [2], "x"]), arr: [1, , 3], big: 10n, u: undefined, nul: '
                 'null, nan: NaN, buf: new Uint8Array([1, 2, 3]), a: shared, b: shared, text: "т" };\n'
                 'src.self = src;\n'
                 'const c = deepClone(src);\n'
                 'console.log(c !== src, c.d !== src.d, c.d.getTime(), c.r !== src.r, c.r.source, c.r.flags, '
                 'c.r.lastIndex, c.m.get("k").v, c.m.get("k") !== src.m.get("k"), [...c.m.keys()][1] === '
                 'c.a, c.m.get(c.a));\n'
                 'console.log([...c.s].length, c.s.has("x"), c.arr.length, 1 in c.arr, c.big, "u" in c, c.u, '
                 'c.nul, Number.isNaN(c.nan), c.buf instanceof Uint8Array, c.buf !== src.buf, c.buf.buffer '
                 '!== src.buf.buffer, [...c.buf].join());\n'
                 'console.log(c.a === c.b, c.a !== shared, c.self === c, c.self !== src);\n'
                 'class P { constructor() { this.x = 1; } get y() { return 2; } } const p = deepClone(new '
                 'P()); console.log(Object.getPrototypeOf(p) === Object.prototype, p.x, "y" in p);\n'
                 'console.log(e(() => deepClone(() => 1)), e(() => deepClone({ a: [{ f() {} }] })), e(() => '
                 'deepClone({ s: Symbol("x") })), e(() => deepClone(new Map([[1, () => 2]]))));\n'
                 'const ab = new ArrayBuffer(4); new Uint8Array(ab).set([9, 8, 7, 6]); const abc = '
                 'deepClone(ab); new Uint8Array(ab)[0] = 0; console.log([...new Uint8Array(abc)].join());\n'
                 'console.log(__count("structu" + "redClone"));\n',
       'hint': 'Таблица «исходный объект → копия» решает и общие ссылки, и циклы: кладите копию в неё до '
               'обхода потомков.',
       'expected': ['true true 86400000 true a+b gi 0 1 true true ключ-объект',
                    '3 true 3 false 10n true undefined null true true true true 1,2,3',
                    'true true true true',
                    'true 1 false',
                    'DataCloneError: Невозможно клонировать: function DataCloneError: Невозможно '
                    'клонировать: function DataCloneError: Невозможно клонировать: symbol DataCloneError: '
                    'Невозможно клонировать: function',
                    '9,8,7,6',
                    '0']},
      {'id': 'j19-message-channel',
       'mode': 'js',
       'title': 'Свой MessageChannel',
       'statement': 'Напишите класс MyMessageChannel с портами port1 и port2. Порт: postMessage(data, '
                    'transfer = []) — данные копируются structuredClone(data, { transfer }) (можно '
                    'использовать) и доставляются парному порту асинхронно (после текущего кода, в порядке '
                    'отправки) событием { data, target: порт-получатель }; свойство onmessage — обработчик '
                    '(присваивание сразу «запускает» порт); addEventListener("message", fn) и '
                    'removeEventListener; метод start() запускает порт. Пока порт не запущен, сообщения '
                    'копятся и доставляются при start() (в порядке отправки, до новых). close() закрывает '
                    'оба порта: ожидающие доставки сообщения не доставляются, а postMessage после закрытия '
                    'молча ничего не делает. Ошибки клонирования (DataCloneError) бросаются синхронно из '
                    'postMessage.',
       'starter': 'class MyMessageChannel {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'const ch = new MyMessageChannel(); const log = [];\n'
                 'ch.port2.onmessage = (e) => log.push(`2<-${JSON.stringify(e.data)}:${e.target === '
                 'ch.port2}`);\n'
                 'ch.port1.postMessage({ a: 1 }); ch.port1.postMessage("два"); log.push("после отправки"); '
                 'await tick(); console.log(log.join(" | "));\n'
                 'const src = { x: [1] }; ch.port1.postMessage(src); src.x.push(2); await tick(); '
                 'console.log(log.at(-1));\n'
                 'const buf = new ArrayBuffer(8); ch.port1.postMessage(buf, [buf]); '
                 'console.log(buf.byteLength); await tick();\n'
                 'try { ch.port1.postMessage(() => 1); } catch (e) { console.log(e.name); }\n'
                 'const log2 = []; const c2 = new MyMessageChannel();\n'
                 'c2.port2.addEventListener("message", (e) => log2.push(e.data)); c2.port1.postMessage(1); '
                 'await tick(); console.log("до start", log2.length); c2.port1.postMessage(2); '
                 'c2.port2.start(); console.log("сразу после start", log2.join()); await tick(); '
                 'console.log(log2.join());\n'
                 'const f = (e) => log2.push("f" + e.data); c2.port2.addEventListener("message", f); '
                 'c2.port1.postMessage(3); await tick(); c2.port2.removeEventListener("message", f); '
                 'c2.port1.postMessage(4); await tick(); console.log(log2.join());\n'
                 'const c3 = new MyMessageChannel(); const log3 = []; c3.port1.onmessage = (e) => '
                 'log3.push("p1:" + e.data); c3.port2.onmessage = (e) => { log3.push("p2:" + e.data); '
                 'c3.port2.postMessage("эхо:" + e.data); };\n'
                 'c3.port1.postMessage("ping"); await tick(); console.log(log3.join());\n'
                 'c3.port1.postMessage("поздно"); c3.port2.close(); await tick(); '
                 'c3.port1.postMessage("мёртвый"); c3.port2.postMessage("x"); await tick(); '
                 'console.log(log3.join());\n',
       'hint': 'Очередь входящих и флаг «запущен» на каждом порту; доставка — через микрозадачу.',
       'expected': ['после отправки | 2<-{"a":1}:true | 2<-"два":true',
                    '2<-{"x":[1]}:true',
                    '0',
                    'DataCloneError',
                    'до start 0',
                    'сразу после start 1',
                    '1,2',
                    '1,2,3,f3,4',
                    'p2:ping,p1:эхо:ping',
                    'p2:ping,p1:эхо:ping']},
      {'id': 'j19-rpc',
       'mode': 'js',
       'title': 'RPC поверх postMessage',
       'statement': 'Напишите функции expose(api, port) и wrap(port). port — объект { postMessage(msg), '
                    'onmessage }: входящее событие приходит как onmessage({ data }). wrap возвращает прокси: '
                    'rpc.method(...args) → промис. Протокол: клиент шлёт { id, method, args }; сервер '
                    'вызывает api[method](...args) и отвечает { id, result } либо { id, error: { name, '
                    'message } } (если метод бросил/отклонился; для неизвестного метода — { name: '
                    '"NoSuchMethod", message: "Нет метода: <method>" }). Клиент сопоставляет ответы по id '
                    '(ответы могут приходить не по порядку), успех → result, ошибка → отклонение Error с '
                    'теми же name и message. id — возрастающие числа с 1. Обращение к «then» у прокси должно '
                    'возвращать undefined (чтобы await rpc не завис). Метод api может быть синхронным или '
                    'возвращать промис.',
       'starter': 'function expose(api, port) {\n}\nfunction wrap(port) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'const later = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'const pair = (delayFor = () => 0) => { const a = { onmessage: null, sent: [] }, b = { '
                 'onmessage: null, sent: [] }; const link = (from, to) => { from.postMessage = (m) => { '
                 'from.sent.push(m); const copy = structuredClone(m); setTimeout(() => to.onmessage?.({ '
                 'data: copy }), delayFor(m)); }; }; link(a, b); link(b, a); return [a, b]; };\n'
                 'const [client, server] = pair((m) => (m.id === 1 ? 20 : m.result === "медленно" ? 20 : '
                 '0));\n'
                 'expose({ add: (a, b) => a + b, slow: async () => { await later(5); return "медленно"; }, '
                 'fast: () => "быстро", boom() { const e = new RangeError("вне диапазона"); throw e; }, '
                 'async reject() { throw new TypeError("отказ"); }, echo: (o) => ({ ...o, seen: true }) }, '
                 'server);\n'
                 'const rpc = wrap(client);\n'
                 'console.log(await rpc.add(2, 3), JSON.stringify(await rpc.echo({ a: 1 })));\n'
                 'const order = []; await Promise.all([rpc.slow().then((v) => order.push("slow:" + v)), '
                 'rpc.fast().then((v) => order.push("fast:" + v))]); console.log(order.join());\n'
                 'for (const m of ["boom", "reject", "nope"]) { try { await rpc[m](); } catch (e) { '
                 'console.log(m, e instanceof Error, e.name, e.message); } }\n'
                 'console.log(JSON.stringify(client.sent.map((m) => m.id)), JSON.stringify(client.sent[0]), '
                 'typeof rpc.then, (await rpc) === rpc);\n',
       'hint': 'Таблица ожидающих вызовов по id; Proxy возвращает функцию, которая отправляет сообщение.',
       'expected': ['5 {"a":1,"seen":true}',
                    'fast:быстро,slow:медленно',
                    'boom true RangeError вне диапазона',
                    'reject true TypeError отказ',
                    'nope true NoSuchMethod Нет метода: nope',
                    '[1,2,3,4,5,6,7] {"id":1,"method":"add","args":[2,3]} undefined true']},
      {'id': 'j19-worker-pool',
       'mode': 'js',
       'title': 'Пул воркеров',
       'statement': 'Напишите функцию createPool(size, spawn): spawn() создаёт воркера { run(task) → промис, '
                    'terminate() }. Возвращает { exec(task) → промис, stats(), terminate() }. Воркеры '
                    'создаются лениво: новый создаётся только если нет свободного и их меньше size; '
                    'свободный воркер берётся раньше создания нового (первый по порядку создания). Задачи, '
                    'для которых нет воркера, ждут в очереди FIFO. exec возвращает результат task у воркера; '
                    'если run отклонился — exec отклоняется той же ошибкой, воркер остаётся в пуле. stats() '
                    '→ { workers (создано), busy, queued }. terminate(): очередные задачи отклоняются '
                    'Error("Pool terminated"), у всех воркеров вызывается terminate(), а последующие exec '
                    'сразу отклоняются тем же Error. Выполняющиеся задачи завершаются как обычно.',
       'starter': 'function createPool(size, spawn) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'let spawned = 0; const gates = {}; const terminated = [];\n'
                 'const spawn = () => { const id = ++spawned; return { run: (t) => new Promise((res, rej) => '
                 '{ (gates[t] = () => res(`${t}@w${id}`)); gates[t + "!"] = () => rej(new Error("сбой " + '
                 't)); }), terminate: () => terminated.push(id) }; };\n'
                 'const pool = createPool(2, spawn); const out = [];\n'
                 'const go = (t) => pool.exec(t).then((v) => out.push(v), (e) => out.push("ERR:" + '
                 'e.message));\n'
                 'go("a"); await tick(); console.log(JSON.stringify(pool.stats()), spawned);\n'
                 'go("b"); go("c"); go("d"); await tick(); console.log(JSON.stringify(pool.stats()), '
                 'spawned);\n'
                 'gates.a(); await tick(); await tick(); console.log(JSON.stringify(pool.stats()), '
                 'out.join(), spawned);\n'
                 'gates["c!"](); await tick(); await tick(); console.log(JSON.stringify(pool.stats()), '
                 'out.join());\n'
                 'gates.b(); gates.d(); await tick(); await tick(); '
                 'console.log(JSON.stringify(pool.stats()), out.join());\n'
                 'go("e"); await tick(); console.log(out.at(-1), JSON.stringify(pool.stats()), spawned); '
                 'gates.e(); await tick(); await tick(); console.log(out.at(-1));\n'
                 'go("x"); go("y"); go("z"); await tick(); pool.terminate(); await tick(); '
                 'console.log(out.slice(-2).join(), JSON.stringify(pool.stats()), terminated.join());\n'
                 'gates.x(); gates.y(); await tick(); await tick(); console.log(out.slice(-2).join());\n'
                 'try { await pool.exec("late"); } catch (e) { console.log(e.message); }\n',
       'hint': 'Список воркеров с флагом busy и очередь; после завершения задачи запускайте следующую из '
               'очереди.',
       'expected': ['{"workers":1,"busy":1,"queued":0} 1',
                    '{"workers":2,"busy":2,"queued":2} 2',
                    '{"workers":2,"busy":2,"queued":1} a@w1 2',
                    '{"workers":2,"busy":2,"queued":0} a@w1,ERR:сбой c',
                    '{"workers":2,"busy":0,"queued":0} a@w1,ERR:сбой c,b@w2,d@w1',
                    'd@w1 {"workers":2,"busy":1,"queued":0} 2',
                    'e@w1',
                    'e@w1,ERR:Pool terminated {"workers":2,"busy":2,"queued":0} 1,2',
                    'x@w1,y@w2',
                    'Pool terminated']},
      {'id': 'j19-ranges',
       'mode': 'js',
       'title': 'Разбиение работы между воркерами',
       'statement': 'Напишите функции splitRanges(n, parts) и parallelMap(items, parts, run). splitRanges → '
                    'массив диапазонов [start, end) для индексов 0..n−1, максимально равных: первые n % '
                    'parts диапазонов на один элемент длиннее; пустые диапазоны не возвращаются (если parts '
                    '> n — по одному элементу); n = 0 → []. parts < 1 — RangeError. parallelMap делит items '
                    'этим разбиением, запускает run(chunk, index) для всех кусков сразу (параллельно) и '
                    'возвращает промис с плоским массивом результатов в порядке исходных данных (run '
                    'возвращает промис массива результатов куска); если любой кусок отклонился — отклониться '
                    'его ошибкой.',
       'starter': 'function splitRanges(n, parts) {\n}\nasync function parallelMap(items, parts, run) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'for (const [n, p] of [[10, 3], [9, 3], [3, 5], [0, 4], [1, 1], [7, 7], [100, 8]]) '
                 'console.log(n, p, JSON.stringify(splitRanges(n, p)));\n'
                 'try { splitRanges(5, 0); } catch (e) { console.log(e.name); }\n'
                 'const later = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms)); const started = '
                 '[];\n'
                 'const out = await parallelMap([1, 2, 3, 4, 5, 6, 7], 3, async (chunk, i) => { '
                 'started.push(i); await later(30 - i * 10); return chunk.map((x) => x * x); });\n'
                 'console.log(JSON.stringify(out), started.join());\n'
                 'console.log(JSON.stringify(await parallelMap([], 4, async () => [1])), '
                 'JSON.stringify(await parallelMap(["a", "b"], 5, async (c) => c.map((x) => x + "!"))));\n'
                 'try { await parallelMap([1, 2, 3], 3, async (c, i) => { if (i === 1) throw new Error("куск '
                 '1"); return c; }); } catch (e) { console.log(e.message); }\n',
       'hint': 'Первые n % parts кусков получают по лишнему элементу; Promise.all сохраняет порядок.',
       'expected': ['10 3 [[0,4],[4,7],[7,10]]',
                    '9 3 [[0,3],[3,6],[6,9]]',
                    '3 5 [[0,1],[1,2],[2,3]]',
                    '0 4 []',
                    '1 1 [[0,1]]',
                    '7 7 [[0,1],[1,2],[2,3],[3,4],[4,5],[5,6],[6,7]]',
                    '100 8 [[0,13],[13,26],[26,39],[39,52],[52,64],[64,76],[76,88],[88,100]]',
                    'RangeError',
                    '[1,4,9,16,25,36,49] 0,1,2',
                    '[] ["a!","b!"]',
                    'куск 1']},
      {'id': 'j19-sw-lifecycle',
       'mode': 'js',
       'title': 'Жизненный цикл сервис-воркера',
       'statement': 'Напишите функцию createSwModel() → { register(version, opts), openPage(id), '
                    'closePage(id), skipWaiting(), state(), log }. Модель одной регистрации. register(v, { '
                    'skipWaiting = false, claim = false }): если v уже active или waiting — ничего; иначе '
                    'лог «install:v»; если активной версии нет — сразу activate(v); если есть и skipWaiting '
                    '— activate(v) сразу; иначе v становится waiting (прежняя waiting уходит в redundant). '
                    'activate(v): лог «activate:v»; прежняя active (если была) → redundant; waiting = null '
                    '(если v была waiting); active = v; если у версии claim — все открытые страницы '
                    'переходят под v. openPage(id): страница управляется текущей active (или null, если её '
                    'нет). closePage(id): страница закрывается; если есть waiting и ни одна страница больше '
                    'не управляется текущей active — waiting активируется. skipWaiting() — если есть '
                    'waiting, активировать её сейчас. state() → { active, waiting, redundant: [версии в '
                    'порядке ухода], pages: { id: версия|null } }. log — массив строк.',
       'starter': 'function createSwModel() {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const sw = createSwModel(); const show = (l) => console.log(l.padEnd(18), '
                 'JSON.stringify(canon(sw.state())), "|", sw.log.slice(-2).join());\n'
                 'sw.openPage("p0"); sw.register("v1"); show("v1 первый"); sw.openPage("p1"); show("страница '
                 'p1");\n'
                 'sw.register("v1"); show("v1 повтор"); sw.register("v2"); show("v2 ждёт"); '
                 'sw.register("v3"); show("v3 вместо v2");\n'
                 'sw.closePage("p0"); show("закрыли p0"); sw.openPage("p2"); sw.closePage("p1"); '
                 'show("закрыли p1"); sw.closePage("p2"); show("закрыли p2");\n'
                 'sw.openPage("p3"); sw.register("v4", { claim: true }); show("v4 ждёт"); sw.skipWaiting(); '
                 'show("skipWaiting"); sw.skipWaiting(); show("ещё раз");\n'
                 'sw.register("v5", { skipWaiting: true }); show("v5 skip"); sw.openPage("p4"); show("p4"); '
                 'sw.register("v6", { skipWaiting: true, claim: true }); show("v6 claim");\n'
                 'console.log(sw.log.join(" "));\n'
                 'const empty = createSwModel(); empty.closePage("x"); empty.skipWaiting(); '
                 'console.log(JSON.stringify(canon(empty.state())));\n',
       'hint': 'Две функции-переходы: register решает, ждать или активировать; activate переносит active и '
               'redundant.',
       'expected': ['v1 первый          {"active":"v1","pages":{"p0":null},"redundant":[],"waiting":null} | '
                    'install:v1,activate:v1',
                    'страница p1        '
                    '{"active":"v1","pages":{"p0":null,"p1":"v1"},"redundant":[],"waiting":null} | '
                    'install:v1,activate:v1',
                    'v1 повтор          '
                    '{"active":"v1","pages":{"p0":null,"p1":"v1"},"redundant":[],"waiting":null} | '
                    'install:v1,activate:v1',
                    'v2 ждёт            '
                    '{"active":"v1","pages":{"p0":null,"p1":"v1"},"redundant":[],"waiting":"v2"} | '
                    'activate:v1,install:v2',
                    'v3 вместо v2       '
                    '{"active":"v1","pages":{"p0":null,"p1":"v1"},"redundant":["v2"],"waiting":"v3"} | '
                    'install:v2,install:v3',
                    'закрыли p0         '
                    '{"active":"v1","pages":{"p1":"v1"},"redundant":["v2"],"waiting":"v3"} | '
                    'install:v2,install:v3',
                    'закрыли p1         '
                    '{"active":"v1","pages":{"p2":"v1"},"redundant":["v2"],"waiting":"v3"} | '
                    'install:v2,install:v3',
                    'закрыли p2         {"active":"v3","pages":{},"redundant":["v2","v1"],"waiting":null} | '
                    'install:v3,activate:v3',
                    'v4 ждёт            '
                    '{"active":"v3","pages":{"p3":"v3"},"redundant":["v2","v1"],"waiting":"v4"} | '
                    'activate:v3,install:v4',
                    'skipWaiting        '
                    '{"active":"v4","pages":{"p3":"v4"},"redundant":["v2","v1","v3"],"waiting":null} | '
                    'install:v4,activate:v4',
                    'ещё раз            '
                    '{"active":"v4","pages":{"p3":"v4"},"redundant":["v2","v1","v3"],"waiting":null} | '
                    'install:v4,activate:v4',
                    'v5 skip            '
                    '{"active":"v5","pages":{"p3":"v4"},"redundant":["v2","v1","v3","v4"],"waiting":null} | '
                    'install:v5,activate:v5',
                    'p4                 '
                    '{"active":"v5","pages":{"p3":"v4","p4":"v5"},"redundant":["v2","v1","v3","v4"],"waiting":null} '
                    '| install:v5,activate:v5',
                    'v6 claim           '
                    '{"active":"v6","pages":{"p3":"v6","p4":"v6"},"redundant":["v2","v1","v3","v4","v5"],"waiting":null} '
                    '| install:v6,activate:v6',
                    'install:v1 activate:v1 install:v2 install:v3 activate:v3 install:v4 activate:v4 '
                    'install:v5 activate:v5 install:v6 activate:v6',
                    '{"active":null,"pages":{},"redundant":[],"waiting":null}']},
      {'id': 'j19-update-check',
       'mode': 'js',
       'title': 'Проверка обновления скрипта воркера',
       'statement': 'Напишите функции compareWorkerScripts(oldScript, newScript) и needsCheck(lastCheck, '
                    'now, trigger). Скрипт — { main: строка, imports: { url: строка } } (импортированные '
                    'через importScripts скрипты тоже проверяются). compareWorkerScripts → { changed, reason '
                    '}: если main отличается — { true, "main" }; иначе первый (по возрастанию url среди '
                    'объединения адресов обоих скриптов) импорт, который отличается, добавлен или удалён — { '
                    'true, "import:<url>" }; иначе { false, "none" }. needsCheck: проверка обновления '
                    'выполняется при каждой навигации в области воркера, но не чаще чем раз в 24 часа для '
                    'функциональных событий (push, sync); trigger — «navigation» | «push» | «sync» | '
                    '«register». Для «navigation» и «register» — всегда true; для «push» и «sync» — true, '
                    'если lastCheck = null или now − lastCheck ≥ 24 часа (86 400 000 мс).',
       'starter': 'function compareWorkerScripts(oldScript, newScript) {\n'
                  '}\n'
                  'function needsCheck(lastCheck, now, trigger) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const base = { main: "a", imports: { "/x.js": "1", "/y.js": "2" } };\n'
                 'const cmp = (n) => console.log(JSON.stringify(canon(compareWorkerScripts(base, n))));\n'
                 'cmp({ main: "a", imports: { "/y.js": "2", "/x.js": "1" } }); cmp({ main: "b", imports: '
                 'base.imports }); cmp({ main: "a", imports: { "/x.js": "1", "/y.js": "3" } });\n'
                 'cmp({ main: "a", imports: { "/x.js": "1" } }); cmp({ main: "a", imports: { "/x.js": "1", '
                 '"/y.js": "2", "/a.js": "new" } }); cmp({ main: "a", imports: { "/x.js": "9", "/y.js": "9" '
                 '} }); cmp({ main: "a" });\n'
                 'console.log(JSON.stringify(canon(compareWorkerScripts({ main: "a" }, { main: "a", imports: '
                 '{} }))));\n'
                 'const H = 3600000; for (const [l, n, t] of [[0, 1, "navigation"], [null, 1, "register"], '
                 '[0, 23 * H, "push"], [0, 24 * H, "sync"], [0, 24 * H - 1, "sync"], [null, 5, "push"], '
                 '[100, 100, "navigation"], [0, 100 * H, "push"]]) console.log(l, n, t, needsCheck(l, n, '
                 't));\n',
       'hint': 'Объедините адреса импортов обоих скриптов, отсортируйте и найдите первое расхождение.',
       'expected': ['{"changed":false,"reason":"none"}',
                    '{"changed":true,"reason":"main"}',
                    '{"changed":true,"reason":"import:/y.js"}',
                    '{"changed":true,"reason":"import:/y.js"}',
                    '{"changed":true,"reason":"import:/a.js"}',
                    '{"changed":true,"reason":"import:/x.js"}',
                    '{"changed":true,"reason":"import:/x.js"}',
                    '{"changed":false,"reason":"none"}',
                    '0 1 navigation true',
                    'null 1 register true',
                    '0 82800000 push false',
                    '0 86400000 sync true',
                    '0 86399999 sync false',
                    'null 5 push true',
                    '100 100 navigation true',
                    '0 360000000 push true']},
      {'id': 'j19-scope',
       'mode': 'js',
       'title': 'Область (scope) сервис-воркера',
       'statement': 'Напишите функции defaultScope(scriptUrl), isScopeAllowed(scriptUrl, scope, '
                    'allowedHeader) и findRegistration(pageUrl, registrations). defaultScope → адрес папки '
                    'скрипта («https://x.ru/app/sw.js» → «https://x.ru/app/»). isScopeAllowed: область '
                    'должна быть того же источника, что скрипт, и её путь должен начинаться с пути папки '
                    'скрипта; если сервер прислал заголовок Service-Worker-Allowed (allowedHeader — путь или '
                    'абсолютный адрес, либо null), допустима также любая область, чей путь начинается с него '
                    '(путь заголовка относительно источника скрипта). findRegistration: registrations — '
                    'массив { scope: абсолютный адрес области }; выбирается регистрация с самым длинным '
                    'совпадающим scope по префиксу строки адреса (того же источника); совпадение — pageUrl '
                    '(без фрагмента и параметров запроса) начинается с scope; нет совпадения — null.',
       'starter': 'function defaultScope(scriptUrl) {\n'
                  '}\n'
                  'function isScopeAllowed(scriptUrl, scope, allowedHeader) {\n'
                  '}\n'
                  'function findRegistration(pageUrl, registrations) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'for (const u of ["https://x.ru/app/sw.js", "https://x.ru/sw.js", '
                 '"https://x.ru/a/b/c/worker.js?v=2#h"]) console.log(defaultScope(u));\n'
                 'const S = "https://x.ru/app/sw.js";\n'
                 'for (const [sc, h] of [["/app/", null], ["/app/inner/", null], ["/", null], '
                 '["/application/", null], ["/other/", "/"], ["/other/", "/other/"], ["/other/a/", '
                 '"/other/"], ["/zzz/", "/other/"], ["https://evil.ru/app/", null], ["https://evil.ru/", '
                 '"https://evil.ru/"], ["./sub/", null], ["../up/", null], ["../up/", "/"]]) '
                 'console.log(sc.padEnd(24), String(h).padEnd(12), isScopeAllowed(S, sc, h));\n'
                 'const regs = [{ scope: "https://x.ru/" }, { scope: "https://x.ru/app/" }, { scope: '
                 '"https://x.ru/app/admin/" }, { scope: "https://other.ru/app/" }, { scope: '
                 '"https://x.ru/ap" }];\n'
                 'for (const p of ["https://x.ru/", "https://x.ru/app", "https://x.ru/app/", '
                 '"https://x.ru/app/page?x=1#h", "https://x.ru/app/admin/users", "https://x.ru/application", '
                 '"https://other.ru/app/x", "https://other.ru/", "http://x.ru/app/"]) '
                 'console.log(p.padEnd(32), findRegistration(p, regs)?.scope ?? null);\n'
                 'console.log(findRegistration("https://x.ru/a", []));\n',
       'hint': 'Работайте с классом URL: сравнивайте origin и pathname; самое длинное совпадение выигрывает.',
       'expected': ['https://x.ru/app/',
                    'https://x.ru/',
                    'https://x.ru/a/b/c/',
                    '/app/                    null         true',
                    '/app/inner/              null         true',
                    '/                        null         false',
                    '/application/            null         false',
                    '/other/                  /            true',
                    '/other/                  /other/      true',
                    '/other/a/                /other/      true',
                    '/zzz/                    /other/      false',
                    'https://evil.ru/app/     null         false',
                    'https://evil.ru/         https://evil.ru/ false',
                    './sub/                   null         true',
                    '../up/                   null         false',
                    '../up/                   /            true',
                    'https://x.ru/                    https://x.ru/',
                    'https://x.ru/app                 https://x.ru/ap',
                    'https://x.ru/app/                https://x.ru/app/',
                    'https://x.ru/app/page?x=1#h      https://x.ru/app/',
                    'https://x.ru/app/admin/users     https://x.ru/app/admin/',
                    'https://x.ru/application         https://x.ru/ap',
                    'https://other.ru/app/x           https://other.ru/app/',
                    'https://other.ru/                null',
                    'http://x.ru/app/                 null',
                    'null']},
      {'id': 'j19-sw-router',
       'mode': 'js',
       'title': 'Маршрутизатор запросов сервис-воркера',
       'statement': 'Напишите функцию createRouter() → { register(matcher, handler, method = "GET"), '
                    'setDefaultHandler(h), setCatchHandler(h), handle(request) }. request — { url '
                    '(абсолютный), method, headers, destination }; страница — https://app.ru. matcher: '
                    'строка — если начинается с «/», сравнивается с pathname запроса (только того же '
                    'источника, https://app.ru); иначе — с полным адресом (без параметров запроса и '
                    'фрагмента); RegExp — проверяется (test) по полному адресу; функция — matcher({ url '
                    '(объект URL), request }) → истина/ложь или объект (параметры), который становится '
                    'params. handle(request) → промис: перебирает маршруты по порядку регистрации, метод '
                    'запроса должен совпадать (без учёта регистра); у первого подошедшего вызывается '
                    'handler({ request, url, params }) и результат возвращается; если handler бросил или '
                    'отклонился — и есть catch-обработчик — вернуть его результат (catch({ request, url, '
                    'error })), иначе пробросить; нет подходящего маршрута — вернуть результат '
                    'default-обработчика (с { request, url }), если он есть, иначе undefined.',
       'starter': 'function createRouter() {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const R = (url, method = "GET") => ({ url, method, headers: {}, destination: "" });\n'
                 'const r = createRouter(); const calls = [];\n'
                 'r.register("/api/ping", ({ url }) => "ping " + url.search);\n'
                 'r.register("https://cdn.ru/lib.js", () => "cdn lib");\n'
                 'r.register(/\\.(png|jpg)$/, ({ url }) => "image " + url.pathname);\n'
                 'r.register(({ url }) => url.pathname.startsWith("/users/") && { id: '
                 'url.pathname.split("/")[2] }, ({ params }) => "user " + params.id);\n'
                 'r.register(({ request }) => request.destination === "script", () => "script", "GET");\n'
                 'r.register("/form", () => "form post", "post");\n'
                 'r.register("/boom", () => { throw new Error("взрыв"); });\n'
                 'r.register("/boom-async", async () => { throw new Error("async взрыв"); });\n'
                 'r.register(({ url }) => url.pathname === "/first", () => "первый"); r.register("/first", '
                 '() => "второй");\n'
                 'const run = async (u, m, extra) => { try { console.log(m ?? "GET", u.padEnd(34), '
                 'JSON.stringify(await r.handle({ ...R(u, m), ...extra }))); } catch (e) { console.log(m ?? '
                 '"GET", u.padEnd(34), "ERR", e.message); } };\n'
                 'await run("https://app.ru/api/ping?x=1"); await run("https://other.ru/api/ping"); await '
                 'run("https://cdn.ru/lib.js?v=3#h"); await run("https://cdn.ru/lib.js", "POST");\n'
                 'await run("https://cdn.ru/pic.png"); await run("https://app.ru/users/42"); await '
                 'run("https://app.ru/users/"); await run("https://app.ru/app.js", "get", { destination: '
                 '"script" });\n'
                 'await run("https://app.ru/form"); await run("https://app.ru/form", "POST"); await '
                 'run("https://app.ru/first"); await run("https://app.ru/nothing");\n'
                 'await run("https://app.ru/boom"); await run("https://app.ru/boom-async");\n'
                 'r.setDefaultHandler(({ url }) => "по умолчанию " + url.pathname); r.setCatchHandler(({ '
                 'error, url }) => `поймали ${error.message} на ${url.pathname}`);\n'
                 'await run("https://app.ru/nothing"); await run("https://app.ru/boom"); await '
                 'run("https://app.ru/boom-async");\n',
       'hint': 'Перебор маршрутов по порядку; разные виды matcher разбирайте по типу.',
       'expected': ['GET https://app.ru/api/ping?x=1        "ping ?x=1"',
                    'GET https://other.ru/api/ping          undefined',
                    'GET https://cdn.ru/lib.js?v=3#h        "cdn lib"',
                    'POST https://cdn.ru/lib.js              undefined',
                    'GET https://cdn.ru/pic.png             "image /pic.png"',
                    'GET https://app.ru/users/42            "user 42"',
                    'GET https://app.ru/users/              "user "',
                    'get https://app.ru/app.js              "script"',
                    'GET https://app.ru/form                undefined',
                    'POST https://app.ru/form                "form post"',
                    'GET https://app.ru/first               "первый"',
                    'GET https://app.ru/nothing             undefined',
                    'GET https://app.ru/boom                ERR взрыв',
                    'GET https://app.ru/boom-async          ERR async взрыв',
                    'GET https://app.ru/nothing             "по умолчанию /nothing"',
                    'GET https://app.ru/boom                "поймали взрыв на /boom"',
                    'GET https://app.ru/boom-async          "поймали async взрыв на /boom-async"']},
      {'id': 'j19-cache-api',
       'mode': 'js',
       'title': 'Свой Cache и CacheStorage',
       'statement': 'Напишите классы MyCache и MyCacheStorage (упрощённый Cache API). Запрос — { url, '
                    'method, headers }, ответ — { status, headers (нижний регистр), body, clone() }. '
                    'MyCacheStorage(fetchFn) — fetchFn(request) → промис ответа; методы: open(name) → '
                    'MyCache (создаёт, если нет; тот же объект при повторном open), has(name), delete(name) '
                    '→ boolean, keys() → имена в порядке создания, match(request, options) → первый '
                    'найденный ответ по всем кешам в порядке создания. MyCache: put(request, response) — '
                    'только GET (иначе TypeError), нельзя статус 206 (TypeError), нельзя заголовок vary со '
                    'значением «*» (TypeError); хранит копию (clone) ответа и запрос; повторный put по тому '
                    'же ключу заменяет (позиция в keys() сохраняется); ключ — url (метод GET). '
                    'match(request, { ignoreSearch = false, ignoreVary = false }) → копию ответа или '
                    'undefined: сравнение по url (с ignoreSearch — без параметров запроса и фрагмента); если '
                    'у сохранённого ответа есть vary, значения перечисленных заголовков у сохранённого и '
                    'искомого запросов должны совпадать (регистр имён не важен, отсутствие = пустая строка), '
                    'если не ignoreVary. add(request) = fetch + put; addAll(requests) — атомарно: запросы '
                    'выполняются, и если любой ответ не ok (status вне 200–299) или fetch отклонился — не '
                    'добавляется ничего (отклоняется TypeError / исходной ошибкой); delete(request) → '
                    'boolean; keys() → список сохранённых запросов.',
       'starter': 'class MyCache {\n}\nclass MyCacheStorage {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const res = (body = "", status = 200, headers = {}) => ({ status, ok: status >= 200 && '
                 'status < 300, headers: Object.fromEntries(Object.entries(headers).map(([k, v]) => '
                 '[k.toLowerCase(), v])), body, clone() { return res(this.body, this.status, this.headers); '
                 '} });\n'
                 'const req = (url, extra = {}) => ({ url: new URL(url, "https://app.ru").href, method: '
                 '"GET", mode: "cors", destination: "", headers: {}, ...extra });\n'
                 'const net = []; const files = { "/a.css": res("css", 200, { "Content-Type": "text/css" }), '
                 '"/b.js": res("js"), "/bad.js": res("нет", 404), "/lang": res("язык", 200, { Vary: '
                 '"Accept-Language" }), "/star": res("x", 200, { Vary: "*" }), "/part": res("p", 206) };\n'
                 'const fetchFn = async (r) => { net.push(new URL(r.url).pathname); const f = files[new '
                 'URL(r.url).pathname]; if (!f) throw new Error("сеть"); return f.clone(); };\n'
                 'const cs = new MyCacheStorage(fetchFn); const text = async (p) => (await p)?.body;\n'
                 'const c = await cs.open("v1"); console.log(c === (await cs.open("v1")), await '
                 'cs.has("v1"), await cs.has("v2"));\n'
                 'await c.put(req("/a.css"), res("a1")); console.log(await text(c.match(req("/a.css"))), '
                 'await text(c.match(req("/a.css?x=1"))), await text(c.match(req("/a.css?x=1"), { '
                 'ignoreSearch: true })), await text(c.match(req("/a.css#frag"))));\n'
                 'await c.put(req("/a.css"), res("a2")); await c.put(req("/b.js"), res("b")); '
                 'console.log(await text(c.match(req("/a.css"))), (await c.keys()).map((r) => new '
                 'URL(r.url).pathname).join());\n'
                 'for (const [label, r, resp] of [["POST", req("/x", { method: "POST" }), res("x")], ["206", '
                 'req("/p"), res("p", 206)], ["vary *", req("/s"), res("s", 200, { vary: "*" })]]) { try { '
                 'await c.put(r, resp); console.log(label, "принят"); } catch (e) { console.log(label, '
                 'e.name); } }\n'
                 'const orig = res("тело", 200, { "X-A": "1" }); await c.put(req("/clone"), orig); orig.body '
                 '= "изменено"; const got = await c.match(req("/clone")); got.body = "снаружи"; '
                 'console.log((await c.match(req("/clone"))).body);\n'
                 'await c.put(req("/lang", { headers: { "accept-language": "ru" } }), res("рус", 200, { '
                 'vary: "Accept-Language" })); await c.put(req("/lang", { headers: { "accept-language": "en" '
                 '} }), res("eng", 200, { vary: "accept-language" }));\n'
                 'console.log(await text(c.match(req("/lang", { headers: { "accept-language": "ru" } }))), '
                 'await text(c.match(req("/lang", { headers: { "accept-language": "en" } }))), await '
                 'text(c.match(req("/lang", { headers: { "accept-language": "de" } }))), await '
                 'text(c.match(req("/lang", { headers: { "accept-language": "de" } }), { ignoreVary: true '
                 '})), await text(c.match(req("/lang"))));\n'
                 'console.log(await c.delete(req("/b.js")), await c.delete(req("/b.js")), (await '
                 'c.keys()).length);\n'
                 'await c.add(req("/a.css")); console.log(await text(c.match(req("/a.css"))), net.join());\n'
                 'const c2 = await cs.open("v2"); try { await c2.addAll([req("/a.css"), req("/bad.js"), '
                 'req("/b.js")]); } catch (e) { console.log("addAll", e.name, (await c2.keys()).length); }\n'
                 'try { await c2.addAll([req("/a.css"), req("/zzz")]); } catch (e) { console.log("addAll", '
                 'e.message, (await c2.keys()).length); }\n'
                 'await c2.addAll([req("/a.css"), req("/b.js")]); console.log((await c2.keys()).length, '
                 'await cs.keys(), await text(cs.match(req("/b.js"))), await '
                 'text(cs.match(req("/nothing"))));\n'
                 'await c2.put(req("/only-v2"), res("v2")); console.log(await '
                 'text(cs.match(req("/only-v2"))), await cs.delete("v2"), await cs.delete("v2"), await '
                 'text(cs.match(req("/only-v2"))), await cs.keys());\n',
       'hint': 'Массив записей {request, response}; match с учётом ignoreSearch и vary; addAll сначала '
               'получает всё, потом кладёт.',
       'expected': ['true true false',
                    'a1 undefined a1 a1',
                    'a2 /a.css,/b.js',
                    'POST TypeError',
                    '206 TypeError',
                    'vary * TypeError',
                    'тело',
                    'рус eng undefined рус undefined',
                    'true false 4',
                    'css /a.css',
                    'addAll TypeError 0',
                    'addAll сеть 0',
                    "2 [ 'v1', 'v2' ] js undefined",
                    "v2 true false undefined [ 'v1' ]"]},
      {'id': 'j19-cache-first',
       'mode': 'js',
       'title': 'Стратегия Cache First',
       'statement': 'Напишите функцию cacheFirst({ caches, cacheName, fetchFn, waitUntil }) → '
                    'handler(request) → промис ответа. caches.open(name) → промис кеша с match(request) → '
                    'ответ|undefined и put(request, response). Алгоритм: открыть кеш cacheName; если ответ '
                    'найден — вернуть его (в сеть не ходить); иначе fetchFn(request); если ответ успешный '
                    '(status 200) и метод запроса GET — положить в кеш копию (response.clone()) через '
                    'waitUntil(промис) (кладётся не дожидаясь), и вернуть оригинальный ответ; неуспешные '
                    'ответы (404, 500, …) возвращаются как есть и в кеш не кладутся; ошибка сети '
                    'пробрасывается.',
       'starter': 'function cacheFirst(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const res = (body = "", status = 200, headers = {}) => ({ status, ok: status >= 200 && '
                 'status < 300, headers: Object.fromEntries(Object.entries(headers).map(([k, v]) => '
                 '[k.toLowerCase(), v])), body, clone() { return res(this.body, this.status, this.headers); '
                 '} });\n'
                 'const req = (url, extra = {}) => ({ url: new URL(url, "https://app.ru").href, method: '
                 '"GET", mode: "cors", destination: "", headers: {}, ...extra });\n'
                 'const store = new Map(); const log = []; const waits = [];\n'
                 'const caches = { open: async (name) => { log.push("open " + name); return { match: async '
                 '(r) => store.get(name + r.url)?.clone(), put: async (r, resp) => { log.push("put " + new '
                 'URL(r.url).pathname); store.set(name + r.url, resp); } }; } };\n'
                 'const net = { "/app.js": res("код"), "/missing": res("нет", 404), "/err": res("ошибка", '
                 '500) };\n'
                 'const fetchFn = async (r) => { log.push("fetch " + new URL(r.url).pathname); const x = '
                 'net[new URL(r.url).pathname]; if (!x) throw new Error("сеть"); return x.clone(); };\n'
                 'const h = cacheFirst({ caches, cacheName: "static-v1", fetchFn, waitUntil: (p) => '
                 'waits.push(p) });\n'
                 'const go = async (r) => { try { const x = await h(r); console.log(r.method, new '
                 'URL(r.url).pathname, x.status, x.body, "|", log.splice(0).join(", "), "| waitUntil:", '
                 'waits.length); } catch (e) { console.log(r.method, new URL(r.url).pathname, "ERR", '
                 'e.message, "|", log.splice(0).join(", ")); } await Promise.all(waits.splice(0)); };\n'
                 'await go(req("/app.js")); await go(req("/app.js")); await go(req("/missing")); await '
                 'go(req("/missing")); await go(req("/err")); await go(req("/offline")); await '
                 'go(req("/app.js", { method: "POST" })); await go(req("/app.js?v=2"));\n',
       'hint': 'Сначала кеш; сеть — только при промахе; запись в кеш отдавайте в waitUntil, не дожидаясь.',
       'expected': ['GET /app.js 200 код | open static-v1, fetch /app.js, put /app.js | waitUntil: 1',
                    'GET /app.js 200 код | open static-v1 | waitUntil: 0',
                    'GET /missing 404 нет | open static-v1, fetch /missing | waitUntil: 0',
                    'GET /missing 404 нет | open static-v1, fetch /missing | waitUntil: 0',
                    'GET /err 500 ошибка | open static-v1, fetch /err | waitUntil: 0',
                    'GET /offline ERR сеть | open static-v1, fetch /offline',
                    'POST /app.js 200 код | open static-v1 | waitUntil: 0',
                    'GET /app.js 200 код | open static-v1, fetch /app.js, put /app.js | waitUntil: 1']},
      {'id': 'j19-network-first',
       'mode': 'js',
       'title': 'Стратегия Network First с таймаутом',
       'statement': 'Напишите функцию networkFirst({ caches, cacheName, fetchFn, timers, timeoutMs, '
                    'waitUntil }) → handler(request) → промис ответа. Запускает fetchFn(request) и таймер '
                    'timeoutMs. Если сеть ответила раньше таймера: успешный (status 200) ответ кладётся в '
                    'кеш (копия, через waitUntil) и возвращается; неуспешный (не 200) возвращается как есть '
                    'без записи в кеш. Если сеть упала до таймера — вернуть ответ из кеша, а если его нет — '
                    'пробросить ошибку. Если сработал таймер раньше сети — вернуть ответ из кеша (если он '
                    'есть; сеть при этом продолжает работать и по завершении обновляет кеш, если ответ '
                    'успешный); если в кеше пусто — продолжить ждать сеть (таймаут тогда не действует; '
                    'ошибка сети пробрасывается). Таймер должен быть снят, когда он больше не нужен.',
       'starter': 'function networkFirst(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const FAKE = () => { let t = 0; const timers = new Map(); let id = 1; return { now: () => '
                 't, setTimeout(fn, ms) { const i = id++; timers.set(i, { at: t + ms, fn }); return i; }, '
                 'clearTimeout(i) { timers.delete(i); }, advance(ms) { const end = t + ms; for (;;) { const '
                 'due = [...timers].filter(([, x]) => x.at <= end).sort((a, b) => a[1].at - b[1].at || a[0] '
                 '- b[0])[0]; if (!due) break; timers.delete(due[0]); t = due[1].at; due[1].fn(); } t = end; '
                 '}, pending: () => timers.size }; };\n'
                 '\n'
                 'const res = (body = "", status = 200, headers = {}) => ({ status, ok: status >= 200 && '
                 'status < 300, headers: Object.fromEntries(Object.entries(headers).map(([k, v]) => '
                 '[k.toLowerCase(), v])), body, clone() { return res(this.body, this.status, this.headers); '
                 '} });\n'
                 'const req = (url, extra = {}) => ({ url: new URL(url, "https://app.ru").href, method: '
                 '"GET", mode: "cors", destination: "", headers: {}, ...extra });\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'const clock = FAKE(); const store = new Map(); const waits = [];\n'
                 'const caches = { open: async () => ({ match: async (r) => store.get(r.url)?.clone(), put: '
                 'async (r, resp) => { store.set(r.url, resp); } }) };\n'
                 'let behaviour = {};\n'
                 'const fetchFn = (r) => new Promise((resolve, reject) => { const b = behaviour[new '
                 'URL(r.url).pathname]; clock.setTimeout(() => (b.fail ? reject(new Error("сеть")) : '
                 'resolve(res(b.body, b.status ?? 200))), b.after); });\n'
                 'const h = networkFirst({ caches, cacheName: "data", fetchFn, timers: clock, timeoutMs: '
                 '100, waitUntil: (p) => waits.push(p) });\n'
                 'const run = async (label, path, b, advance) => { behaviour[path] = b; let out = "…"; '
                 'h(req(path)).then((x) => (out = `${x.status}:${x.body}`), (e) => (out = "ERR:" + '
                 'e.message)); await tick(); clock.advance(advance); await tick(); await tick(); await '
                 'Promise.all(waits.splice(0)); console.log(label.padEnd(26), out.padEnd(16), "кеш:", '
                 'store.get(new URL(path, "https://app.ru").href)?.body ?? "-", "таймеров:", '
                 'clock.pending()); };\n'
                 'await run("быстрая сеть", "/a", { body: "свежее", after: 50 }, 60);\n'
                 'await run("медленная, кеш есть", "/a", { body: "ещё свежее", after: 300 }, 100); '
                 'clock.advance(300); await tick(); await tick(); await Promise.all(waits.splice(0)); '
                 'console.log("кеш после фона:", store.get("https://app.ru/a").body, clock.pending());\n'
                 'await run("упала, кеш есть", "/a", { fail: true, after: 20 }, 30);\n'
                 'await run("упала, кеша нет", "/b", { fail: true, after: 20 }, 30);\n'
                 'await run("медленная, кеша нет", "/c", { body: "ждали", after: 500 }, 100); '
                 'clock.advance(400); await tick(); await tick(); await Promise.all(waits.splice(0)); '
                 'console.log("кеш /c:", store.get("https://app.ru/c")?.body, clock.pending());\n'
                 'await run("404 быстро", "/d", { body: "нет", status: 404, after: 10 }, 20);\n'
                 'await run("медленная 500, кеш есть", "/a", { body: "ошибка", status: 500, after: 300 }, '
                 '100); clock.advance(300); await tick(); await tick(); await Promise.all(waits.splice(0)); '
                 'console.log("кеш /a:", store.get("https://app.ru/a").body);\n'
                 'await run("падает после таймаута", "/a", { fail: true, after: 400 }, 100); '
                 'clock.advance(400); await tick(); await tick(); console.log("без необработанных ошибок", '
                 'clock.pending());\n',
       'hint': 'Promise.race между сетью и таймером; при таймауте сеть остаётся в работе и обновляет кеш '
               'позже.',
       'expected': ['быстрая сеть               200:свежее       кеш: свежее таймеров: 0',
                    'медленная, кеш есть        200:свежее       кеш: свежее таймеров: 1',
                    'кеш после фона: ещё свежее 0',
                    'упала, кеш есть            200:ещё свежее   кеш: ещё свежее таймеров: 0',
                    'упала, кеша нет            ERR:сеть         кеш: - таймеров: 0',
                    'медленная, кеша нет        …                кеш: - таймеров: 1',
                    'кеш /c: ждали 0',
                    '404 быстро                 404:нет          кеш: - таймеров: 0',
                    'медленная 500, кеш есть    200:ещё свежее   кеш: ещё свежее таймеров: 1',
                    'кеш /a: ещё свежее',
                    'падает после таймаута      200:ещё свежее   кеш: ещё свежее таймеров: 1',
                    'без необработанных ошибок 0']},
      {'id': 'j19-swr-strategy',
       'mode': 'js',
       'title': 'Стратегия Stale-While-Revalidate',
       'statement': 'Напишите функцию staleWhileRevalidate({ caches, cacheName, fetchFn, waitUntil, onUpdate '
                    '}) → handler(request). Есть ответ в кеше — вернуть его сразу, а в фоне запросить сеть '
                    '(waitUntil(промис фонового обновления)); успешный (status 200) сетевой ответ кладётся в '
                    'кеш, и вызывается onUpdate({ url, response }) (копия), а ошибка и неуспешный ответ '
                    'молча игнорируются (кеш не меняется). Если в кеше пусто — дождаться сети, положить '
                    'успешный ответ в кеш (копию) и вернуть ответ; неуспешный ответ вернуть как есть без '
                    'записи; ошибка сети пробрасывается. Если обновление этого адреса уже идёт, повторный '
                    'запрос новое не запускает (но кеш возвращает).',
       'starter': 'function staleWhileRevalidate(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const res = (body = "", status = 200, headers = {}) => ({ status, ok: status >= 200 && '
                 'status < 300, headers: Object.fromEntries(Object.entries(headers).map(([k, v]) => '
                 '[k.toLowerCase(), v])), body, clone() { return res(this.body, this.status, this.headers); '
                 '} });\n'
                 'const req = (url, extra = {}) => ({ url: new URL(url, "https://app.ru").href, method: '
                 '"GET", mode: "cors", destination: "", headers: {}, ...extra });\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'const store = new Map(); const waits = []; const updates = []; let version = 1; let '
                 'netCalls = 0; let mode = "ok";\n'
                 'const caches = { open: async () => ({ match: async (r) => store.get(r.url)?.clone(), put: '
                 'async (r, resp) => { store.set(r.url, resp); } }) };\n'
                 'const fetchFn = async (r) => { netCalls++; await tick(); if (mode === "fail") throw new '
                 'Error("сеть"); if (mode === "500") return res("сбой", 500); return res("v" + version); };\n'
                 'const h = staleWhileRevalidate({ caches, cacheName: "img", fetchFn, waitUntil: (p) => '
                 'waits.push(p), onUpdate: (u) => updates.push(`${new '
                 'URL(u.url).pathname}=${u.response.body}`) });\n'
                 'const go = async (label, path) => { let out; try { const r = await h(req(path)); out = '
                 '`${r.status}:${r.body}`; } catch (e) { out = "ERR:" + e.message; } const before = '
                 'waits.length; await Promise.all(waits.splice(0)); console.log(label.padEnd(22), '
                 'out.padEnd(10), "фон:", before, "кеш:", store.get("https://app.ru" + path)?.body ?? "-", '
                 '"сеть:", netCalls, "upd:", updates.join()); };\n'
                 'await go("пусто → сеть", "/a"); version = 2; await go("есть → фон v2", "/a"); await '
                 'go("снова", "/a");\n'
                 'version = 3; mode = "fail"; await go("сеть упала", "/a"); mode = "500"; await go("сеть '
                 '500", "/a"); mode = "ok"; await go("снова ok", "/a");\n'
                 'mode = "fail"; await go("пусто и сеть упала", "/b"); mode = "500"; await go("пусто и 500", '
                 '"/b"); mode = "ok";\n'
                 'version = 4; const p1 = h(req("/a")), p2 = h(req("/a")); await p1; await p2; '
                 'console.log("дубль:", waits.length, netCalls); await Promise.all(waits.splice(0)); '
                 'console.log(store.get("https://app.ru/a").body, updates.at(-1));\n',
       'hint': 'Запоминайте адреса, для которых фон уже идёт; фоновое обновление заворачивайте в catch.',
       'expected': ['пусто → сеть           200:v1     фон: 0 кеш: v1 сеть: 1 upd: /a=v1',
                    'есть → фон v2          200:v1     фон: 1 кеш: v2 сеть: 2 upd: /a=v1,/a=v2',
                    'снова                  200:v2     фон: 1 кеш: v2 сеть: 3 upd: /a=v1,/a=v2,/a=v2',
                    'сеть упала             200:v2     фон: 1 кеш: v2 сеть: 4 upd: /a=v1,/a=v2,/a=v2',
                    'сеть 500               200:v2     фон: 1 кеш: v2 сеть: 5 upd: /a=v1,/a=v2,/a=v2',
                    'снова ok               200:v2     фон: 1 кеш: v3 сеть: 6 upd: /a=v1,/a=v2,/a=v2,/a=v3',
                    'пусто и сеть упала     ERR:сеть   фон: 0 кеш: - сеть: 7 upd: /a=v1,/a=v2,/a=v2,/a=v3',
                    'пусто и 500            500:сбой   фон: 0 кеш: - сеть: 8 upd: /a=v1,/a=v2,/a=v2,/a=v3',
                    'дубль: 1 9',
                    'v4 /a=v4']},
      {'id': 'j19-cacheable',
       'mode': 'js',
       'title': 'Что можно класть в кеш',
       'statement': 'Напишите функцию isCacheable(request, response, options = {}) → { ok, reason }. '
                    'options: { maxBytes = Infinity, allowOpaque = false }. Проверки по порядку, первая '
                    'сработавшая даёт ok: false и reason: метод не GET → «method»; response.type «opaque» '
                    '(или status 0): allowOpaque ? ok : «opaque»; статус 206 → «partial»; статус не 200 '
                    '(после opaque) → «status»; заголовок cache-control (ключи в нижнем регистре) содержит '
                    'директиву no-store → «no-store»; vary равен «*» (с учётом пробелов) → «vary»; '
                    'content-length больше maxBytes → «too-large»; запрос с заголовком authorization (в '
                    'нижнем регистре) и cache-control ответа без директивы public → «private». Иначе { ok: '
                    'true, reason: "ok" }.',
       'starter': 'function isCacheable(request, response, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const rq = (method = "GET", headers = {}) => ({ method, headers });\n'
                 'const rs = (status = 200, headers = {}, type = "basic") => ({ status, headers, type });\n'
                 'const cases = [\n'
                 '  ["обычный", rq(), rs()], ["POST", rq("POST"), rs()], ["opaque", rq(), rs(0, {}, '
                 '"opaque")], ["opaque разрешён", rq(), rs(0, {}, "opaque"), { allowOpaque: true }], ["206", '
                 'rq(), rs(206)], ["404", rq(), rs(404)], ["301", rq(), rs(301)],\n'
                 '  ["no-store", rq(), rs(200, { "cache-control": "private, No-Store" })], ["max-age", rq(), '
                 'rs(200, { "cache-control": "max-age=60" })], ["vary *", rq(), rs(200, { vary: " * " })], '
                 '["vary accept", rq(), rs(200, { vary: "accept" })],\n'
                 '  ["большой", rq(), rs(200, { "content-length": "1001" }), { maxBytes: 1000 }], ["ровно", '
                 'rq(), rs(200, { "content-length": "1000" }), { maxBytes: 1000 }], ["без длины", rq(), '
                 'rs(200), { maxBytes: 10 }],\n'
                 '  ["authorization", rq("GET", { authorization: "Bearer x" }), rs()], ["auth + public", '
                 'rq("GET", { authorization: "Bearer x" }), rs(200, { "cache-control": "public, max-age=1" '
                 '})], ["post+opaque", rq("POST"), rs(0, {}, "opaque"), { allowOpaque: true }],\n'
                 '];\n'
                 'for (const [n, r, p, o] of cases) console.log(n.padEnd(16), JSON.stringify(isCacheable(r, '
                 'p, o)));\n',
       'hint': 'Проверки по порядку, как в условии; заголовки в нижнем регистре.',
       'expected': ['обычный          {"ok":true,"reason":"ok"}',
                    'POST             {"ok":false,"reason":"method"}',
                    'opaque           {"ok":false,"reason":"opaque"}',
                    'opaque разрешён  {"ok":true,"reason":"ok"}',
                    '206              {"ok":false,"reason":"partial"}',
                    '404              {"ok":false,"reason":"status"}',
                    '301              {"ok":false,"reason":"status"}',
                    'no-store         {"ok":false,"reason":"no-store"}',
                    'max-age          {"ok":true,"reason":"ok"}',
                    'vary *           {"ok":false,"reason":"vary"}',
                    'vary accept      {"ok":true,"reason":"ok"}',
                    'большой          {"ok":false,"reason":"too-large"}',
                    'ровно            {"ok":true,"reason":"ok"}',
                    'без длины        {"ok":true,"reason":"ok"}',
                    'authorization    {"ok":false,"reason":"private"}',
                    'auth + public    {"ok":true,"reason":"ok"}',
                    'post+opaque      {"ok":false,"reason":"method"}']},
      {'id': 'j19-precache-plan',
       'mode': 'js',
       'title': 'План предзагрузки (precache)',
       'statement': 'Напишите функцию planPrecache(oldManifest, newManifest) → { toFetch, toDelete, '
                    'unchanged }. Манифест — массив записей { url, revision } (revision — строка или null, '
                    'если версия зашита в имя файла). Идентичность записи — нормализованный url (без '
                    'фрагмента #…, без параметров, начинающихся с «__WB_REVISION__»; относительные адреса '
                    'считаются относительно https://app.ru/). Запись считается той же, если её '
                    'нормализованный url совпал и revision одинакова; изменилась ревизия — файл нужно '
                    'скачать заново (в toFetch). toFetch — нормализованные адреса новых и изменившихся '
                    'записей, toDelete — адреса, которых нет в новом манифесте, unchanged — совпавшие; все '
                    'три отсортированы по адресу. Если в новом манифесте один и тот же url встречается с '
                    'разными revision — Error с message «Конфликт ревизий: <url>» (url нормализованный); '
                    'точные дубликаты схлопываются в один. Адреса в результате — без origin, только путь с '
                    'параметрами запроса (например «/app.js?v=2»).',
       'starter': 'function planPrecache(oldManifest, newManifest) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const old = [{ url: "/index.html", revision: "r1" }, { url: "/main.a1f3.js", revision: '
                 'null }, { url: "/style.9c2e.css", revision: null }, { url: "/old.js", revision: null }, { '
                 'url: "/logo.svg", revision: "x" }];\n'
                 'const show = (n) => console.log(JSON.stringify(canon(planPrecache(old, n))));\n'
                 'show(old);\n'
                 'show([{ url: "/index.html", revision: "r2" }, { url: "/main.a1f3.js", revision: null }, { '
                 'url: "/style.1111.css", revision: null }, { url: "/logo.svg", revision: "x" }, { url: '
                 '"/new.js", revision: null }]);\n'
                 'show([{ url: "https://app.ru/index.html#top", revision: "r1" }, { url: '
                 '"/main.a1f3.js?__WB_REVISION__=abc", revision: null }, { url: "style.9c2e.css", revision: '
                 'null }, { url: "/old.js", revision: null }, { url: "/logo.svg", revision: "x" }, { url: '
                 '"/logo.svg", revision: "x" }]);\n'
                 'show([]); console.log(JSON.stringify(planPrecache([], [{ url: "/b.js?v=2", revision: null '
                 '}, { url: "/a.js", revision: null }])));\n'
                 'try { show([{ url: "/a.js", revision: "1" }, { url: "/a.js#x", revision: "2" }]); } catch '
                 '(e) { console.log(e.message); }\n'
                 'console.log(JSON.stringify(planPrecache([{ url: "/a.js", revision: "1" }, { url: "/a.js", '
                 'revision: "2" }], [{ url: "/a.js", revision: "2" }])));\n',
       'hint': 'Нормализуйте адрес через URL; сравните две карты «адрес → revision».',
       'expected': ['{"toDelete":[],"toFetch":[],"unchanged":["/index.html","/logo.svg","/main.a1f3.js","/old.js","/style.9c2e.css"]}',
                    '{"toDelete":["/old.js","/style.9c2e.css"],"toFetch":["/index.html","/new.js","/style.1111.css"],"unchanged":["/logo.svg","/main.a1f3.js"]}',
                    '{"toDelete":[],"toFetch":[],"unchanged":["/index.html","/logo.svg","/main.a1f3.js","/old.js","/style.9c2e.css"]}',
                    '{"toDelete":["/index.html","/logo.svg","/main.a1f3.js","/old.js","/style.9c2e.css"],"toFetch":[],"unchanged":[]}',
                    '{"toFetch":["/a.js","/b.js?v=2"],"toDelete":[],"unchanged":[]}',
                    'Конфликт ревизий: /a.js',
                    '{"toFetch":[],"toDelete":[],"unchanged":["/a.js"]}']},
      {'id': 'j19-cache-names',
       'mode': 'js',
       'title': 'Версионные имена кешей',
       'statement': 'Напишите функции cacheName(prefix, version), parseCacheName(name) и '
                    'cachesToDelete(names, prefix, currentVersion). cacheName → «prefix-v<version>». '
                    'parseCacheName → { prefix, version (число) } или null, если имя не вида '
                    '«что-то-v<цифры>» (префикс может содержать дефисы; версия — последняя группа после '
                    '«-v»; имена вроде «app-v1.2», «app-v», «v3», «app-vx» — null). cachesToDelete: из names '
                    'выбрать подлежащие удалению при активации: кеши с тем же префиксом и версией, не равной '
                    'currentVersion (старые и более новые тоже — чужая версия), а также кеши с этим '
                    'префиксом, у которых имя не разбирается как версионное (например «app-tmp»); кеши с '
                    'другим префиксом (в том числе «app-extra-v1» при префиксе «app») не трогать. Порядок '
                    'результата — как в names.',
       'starter': 'function cacheName(prefix, version) {\n'
                  '}\n'
                  'function parseCacheName(name) {\n'
                  '}\n'
                  'function cachesToDelete(names, prefix, currentVersion) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'console.log(cacheName("app", 3), cacheName("static-assets", "12"));\n'
                 'for (const n of ["app-v1", "static-assets-v12", "app-v1.2", "app-v", "v3", "app-vx", '
                 '"app-v007", "a-b-c-v9", "app", "app-v1-v2"]) console.log(n.padEnd(18), '
                 'JSON.stringify(parseCacheName(n)));\n'
                 'const names = ["app-v1", "app-v2", "app-v3", "app-tmp", "app", "app-extra-v1", "other-v1", '
                 '"application-v1", "workbox-precache-v2", "app-v2-runtime", "app-v10"];\n'
                 'console.log(JSON.stringify(cachesToDelete(names, "app", 2)), '
                 'JSON.stringify(cachesToDelete(names, "app", 10)), JSON.stringify(cachesToDelete(names, '
                 '"app-extra", 1)), JSON.stringify(cachesToDelete([], "app", 1)), '
                 'JSON.stringify(cachesToDelete(["app-v2"], "app", 2)));\n',
       'hint': 'Регулярное выражение для имени; затем фильтр: тот же префикс и другая версия либо '
               'неразобранное имя с префиксом.',
       'expected': ['app-v3 static-assets-v12',
                    'app-v1             {"prefix":"app","version":1}',
                    'static-assets-v12  {"prefix":"static-assets","version":12}',
                    'app-v1.2           null',
                    'app-v              null',
                    'v3                 null',
                    'app-vx             null',
                    'app-v007           {"prefix":"app","version":7}',
                    'a-b-c-v9           {"prefix":"a-b-c","version":9}',
                    'app                null',
                    'app-v1-v2          {"prefix":"app-v1","version":2}',
                    '["app-v1","app-v3","app-tmp","app","app-v2-runtime","app-v10"] '
                    '["app-v1","app-v2","app-v3","app-tmp","app","app-v2-runtime"] [] [] []']},
      {'id': 'j19-offline-fallback',
       'mode': 'js',
       'title': 'Запасной ответ без сети',
       'statement': 'Напишите функцию withFallback(handler, options): options = { cache (с методом '
                    'match(url) → ответ|undefined), pages: { document: "/offline.html", image: '
                    '"/placeholder.svg" } }. Возвращает handler2(request) → промис. Вызвать '
                    'handler(request); если он вернул ответ — вернуть его, если отклонился или вернул ответ '
                    'со статусом ≥ 500 — выбрать запасной по request.destination: ключ из pages → '
                    'cache.match(адрес); если запасной не найден в кеше (или для destination нет записи) — '
                    'вернуть { status: 503, body: "Offline", headers: {}, fallback: false }. Найденный '
                    'запасной ответ вернуть, пометив fallback: true (копию с полем). Ответы 4xx возвращаются '
                    'как есть (это настоящий ответ сервера). Если handler отклонился, а для destination в '
                    'pages нет записи — вернуть тот самый 503.',
       'starter': 'function withFallback(handler, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const cache = { match: async (u) => ({ "/offline.html": { status: 200, body: "Нет связи", '
                 'headers: {} }, "/placeholder.svg": { status: 200, body: "<svg/>", headers: {} } })[u] };\n'
                 'const pages = { document: "/offline.html", image: "/placeholder.svg" };\n'
                 'const mk = (behavior) => withFallback(async () => { if (behavior === "throw") throw new '
                 'Error("сеть"); return { status: behavior, body: "оригинал " + behavior, headers: {} }; }, '
                 '{ cache, pages });\n'
                 'for (const behavior of [200, 404, 500, 503, "throw"]) for (const destination of '
                 '["document", "image", "script", ""]) { const r = await mk(behavior)({ url: "/x", '
                 'destination }); console.log(String(behavior).padEnd(6), destination.padEnd(9), r.status, '
                 'r.body, r.fallback); }\n'
                 'const noCache = withFallback(async () => { throw new Error("x"); }, { cache: { match: '
                 'async () => undefined }, pages }); console.log(JSON.stringify(await noCache({ destination: '
                 '"document" })));\n',
       'hint': 'try/catch вокруг handler; фоллбэк по destination; запасной берите из кеша по адресу.',
       'expected': ['200    document  200 оригинал 200 undefined',
                    '200    image     200 оригинал 200 undefined',
                    '200    script    200 оригинал 200 undefined',
                    '200              200 оригинал 200 undefined',
                    '404    document  404 оригинал 404 undefined',
                    '404    image     404 оригинал 404 undefined',
                    '404    script    404 оригинал 404 undefined',
                    '404              404 оригинал 404 undefined',
                    '500    document  200 Нет связи true',
                    '500    image     200 <svg/> true',
                    '500    script    503 Offline false',
                    '500              503 Offline false',
                    '503    document  200 Нет связи true',
                    '503    image     200 <svg/> true',
                    '503    script    503 Offline false',
                    '503              503 Offline false',
                    'throw  document  200 Нет связи true',
                    'throw  image     200 <svg/> true',
                    'throw  script    503 Offline false',
                    'throw            503 Offline false',
                    '{"status":503,"body":"Offline","headers":{},"fallback":false}']},
      {'id': 'j19-navigation',
       'mode': 'js',
       'title': 'Навигация и оболочка приложения',
       'statement': 'Напишите функцию createNavigationHandler({ allowlist = [], denylist = [] }) → '
                    'decide(request) → { serve, reason }. request = { url, method, mode, headers: { accept } '
                    '}. Считать навигацией: метод GET и (mode «navigate» или accept содержит «text/html»); '
                    'иначе { serve: "network", reason: "not-navigation" }. Для навигации проверяется путь '
                    '(pathname): совпал с любым из denylist (RegExp) → { "network", "denylist" }; если '
                    'allowlist не пуст и путь не совпал ни с одним из allowlist → { "network", "not-allowed" '
                    '}; путь, оканчивающийся именем файла с расширением (последний сегмент содержит «.» — '
                    'например /file.pdf), → { "network", "file-extension" } (эта проверка идёт после '
                    'denylist, но до allowlist); иначе { serve: "shell", reason: "navigation" }. Параметры '
                    'запроса при проверке пути игнорируются.',
       'starter': 'function createNavigationHandler(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const q = (url, extra = {}) => ({ url, method: "GET", mode: "navigate", headers: {}, '
                 '...extra });\n'
                 'const d = createNavigationHandler({ denylist: [/^\\/api\\//, /^\\/admin/] });\n'
                 'for (const r of [q("/"), q("/profile?tab=1"), q("/api/users"), q("/admin"), '
                 'q("/administrator"), q("/docs/file.pdf"), q("/docs.v2/page"), q("/img/a.png", { mode: '
                 '"no-cors", headers: { accept: "image/png" } }), q("/x", { mode: "cors", headers: { accept: '
                 '"text/html,*/*" } }), q("/x", { mode: "cors", headers: { accept: "application/json" } }), '
                 'q("/post", { method: "POST" }), q("/a.b/"), q("/page.html")]) console.log(r.method, '
                 'r.url.padEnd(18), JSON.stringify(d(r)));\n'
                 'const w = createNavigationHandler({ allowlist: [/^\\/app\\//], denylist: [/^\\/app\\/raw/] '
                 '});\n'
                 'for (const u of ["/app/home", "/other", "/app/raw/x", "/app/file.js", "/app/"]) '
                 'console.log(u.padEnd(14), JSON.stringify(w(q(u))));\n'
                 'console.log(JSON.stringify(createNavigationHandler()(q("/"))));\n',
       'hint': 'Сначала «навигация ли это», затем denylist, расширение файла и allowlist — в указанном '
               'порядке.',
       'expected': ['GET /                  {"serve":"shell","reason":"navigation"}',
                    'GET /profile?tab=1     {"serve":"shell","reason":"navigation"}',
                    'GET /api/users         {"serve":"network","reason":"denylist"}',
                    'GET /admin             {"serve":"network","reason":"denylist"}',
                    'GET /administrator     {"serve":"network","reason":"denylist"}',
                    'GET /docs/file.pdf     {"serve":"network","reason":"file-extension"}',
                    'GET /docs.v2/page      {"serve":"shell","reason":"navigation"}',
                    'GET /img/a.png         {"serve":"network","reason":"not-navigation"}',
                    'GET /x                 {"serve":"shell","reason":"navigation"}',
                    'GET /x                 {"serve":"network","reason":"not-navigation"}',
                    'POST /post              {"serve":"network","reason":"not-navigation"}',
                    'GET /a.b/              {"serve":"shell","reason":"navigation"}',
                    'GET /page.html         {"serve":"network","reason":"file-extension"}',
                    '/app/home      {"serve":"shell","reason":"navigation"}',
                    '/other         {"serve":"network","reason":"not-allowed"}',
                    '/app/raw/x     {"serve":"network","reason":"denylist"}',
                    '/app/file.js   {"serve":"network","reason":"file-extension"}',
                    '/app/          {"serve":"shell","reason":"navigation"}',
                    '{"serve":"shell","reason":"navigation"}']},
      {'id': 'j19-update-manager',
       'mode': 'js',
       'title': 'Поток «доступна новая версия»',
       'statement': 'Напишите функцию createUpdateManager({ postMessage, reload, hasController }) → manager. '
                    'hasController — функция: управляется ли страница сервис-воркером на момент вызова. '
                    'Состояние manager.state: «idle» → «available» → «applying» → «reloading». Методы: '
                    'onWaiting() — появился ожидающий воркер: если есть state «idle» и hasController() — '
                    'state «available» (и сохраняется для UI: manager.available = true); если страница не '
                    'управляется (первая установка) — игнорировать; accept() — только из «available»: state '
                    '«applying», postMessage({ type: "SKIP_WAITING" }) один раз (повторные accept — ничего); '
                    'dismiss() — только из «available»: state «idle» (available = false) и до следующего '
                    'onWaiting новых предложений нет; onControllerChange(): если state «applying» — state '
                    '«reloading» и reload() ровно один раз; в остальных случаях (первая установка, чужое '
                    'обновление из другой вкладки при state не «applying», повторные события) reload не '
                    'вызывается. Также если onControllerChange пришёл во время «idle»/«available» — ничего.',
       'starter': 'function createUpdateManager(deps) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const mk = (controlled = true) => { const log = []; const m = createUpdateManager({ '
                 'postMessage: (x) => log.push(JSON.stringify(x)), reload: () => log.push("reload"), '
                 'hasController: () => controlled }); return { m, log }; };\n'
                 'const show = (label, { m, log }) => console.log(label.padEnd(24), m.state, m.available, '
                 'log.join());\n'
                 '{ const t = mk(); t.m.onWaiting(); show("ожидание", t); t.m.accept(); show("accept", t); '
                 't.m.accept(); show("accept ещё", t); t.m.onControllerChange(); show("controllerchange", '
                 't); t.m.onControllerChange(); t.m.onWaiting(); show("после перезагрузки", t); }\n'
                 '{ const t = mk(false); t.m.onWaiting(); show("первая установка", t); t.m.accept(); '
                 't.m.onControllerChange(); show("controllerchange", t); }\n'
                 '{ const t = mk(); t.m.onControllerChange(); show("чужое обновление", t); t.m.onWaiting(); '
                 't.m.dismiss(); show("отказ", t); t.m.accept(); show("accept после отказа", t); '
                 't.m.onWaiting(); show("снова waiting", t); t.m.onWaiting(); t.m.onWaiting(); '
                 'show("повторные waiting", t); t.m.onControllerChange(); show("controllerchange без '
                 'accept", t); }\n'
                 '{ const t = mk(); t.m.onWaiting(); t.m.dismiss(); t.m.dismiss(); show("двойной отказ", t); '
                 't.m.onWaiting(); t.m.accept(); t.m.onWaiting(); t.m.dismiss(); show("accept → dismiss", '
                 't); }\n',
       'hint': 'Небольшой автомат: каждый метод проверяет текущее состояние и меняет его только из '
               'допустимого.',
       'expected': ['ожидание                 available true',
                    'accept                   applying false {"type":"SKIP_WAITING"}',
                    'accept ещё               applying false {"type":"SKIP_WAITING"}',
                    'controllerchange         reloading false {"type":"SKIP_WAITING"},reload',
                    'после перезагрузки       reloading false {"type":"SKIP_WAITING"},reload',
                    'первая установка         idle false',
                    'controllerchange         idle false',
                    'чужое обновление         idle false',
                    'отказ                    idle false',
                    'accept после отказа      idle false',
                    'снова waiting            available true',
                    'повторные waiting        available true',
                    'controllerchange без accept available true',
                    'двойной отказ            idle false',
                    'accept → dismiss         applying false {"type":"SKIP_WAITING"}']},
      {'id': 'j19-broadcast',
       'mode': 'js',
       'title': 'Свой BroadcastChannel',
       'statement': 'Напишите класс MyBroadcastChannel(name). Все каналы с одинаковым name (в пределах '
                    'программы) общаются: postMessage(data) отправляет копию (structuredClone допустим) всем '
                    'остальным открытым каналам с тем же именем, но не отправителю; доставка асинхронна '
                    '(после текущего кода), в порядке отправки, событием { data, target } в onmessage и в '
                    'слушатели addEventListener("message"). removeEventListener снимает слушатель. close(): '
                    'канал больше не принимает сообщения (в том числе уже отправленные, но ещё не '
                    'доставленные) и не отправляет; postMessage на закрытом канале бросает Error с name '
                    '«InvalidStateError». name — свойство. Ошибки клонирования бросаются синхронно.',
       'starter': 'class MyBroadcastChannel {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'const a = new MyBroadcastChannel("news"), b = new MyBroadcastChannel("news"), c = new '
                 'MyBroadcastChannel("news"), other = new MyBroadcastChannel("другой"); const log = [];\n'
                 'a.onmessage = (e) => log.push("a:" + JSON.stringify(e.data)); b.onmessage = (e) => '
                 'log.push("b:" + JSON.stringify(e.data) + (e.target === b)); c.addEventListener("message", '
                 '(e) => log.push("c:" + JSON.stringify(e.data))); other.onmessage = () => '
                 'log.push("other!");\n'
                 'a.postMessage({ n: 1 }); a.postMessage("два"); log.push("sync"); await tick(); '
                 'console.log(log.splice(0).join(" | "));\n'
                 'const obj = { x: [1] }; b.postMessage(obj); obj.x.push(2); await tick(); '
                 'console.log(log.splice(0).join(" | "));\n'
                 'c.postMessage("от c"); c.close(); await tick(); console.log(log.splice(0).join(" | "));\n'
                 'try { c.postMessage("мёртвый"); } catch (e) { console.log(e.name); }\n'
                 'a.postMessage("перед закрытием b"); b.close(); await tick(); '
                 'console.log(log.splice(0).join(" | "));\n'
                 'a.postMessage("никому"); await tick(); console.log(log.length, a.name, other.name);\n'
                 'try { a.postMessage(() => 1); } catch (e) { console.log(e.name); }\n'
                 'const d = new MyBroadcastChannel("news"); const f = (e) => log.push("d:" + e.data); '
                 'd.addEventListener("message", f); a.postMessage(1); await tick(); '
                 'd.removeEventListener("message", f); a.postMessage(2); await tick(); '
                 'console.log(log.join());\n',
       'hint': 'Общий реестр «имя → множество каналов»; доставка через микрозадачу с проверкой, что '
               'получатель ещё открыт.',
       'expected': ['sync | b:{"n":1}true | c:{"n":1} | b:"два"true | c:"два"',
                    'a:{"x":[1]} | c:{"x":[1]}',
                    'a:"от c" | b:"от c"true',
                    'InvalidStateError',
                    '',
                    '0 news другой',
                    'd:1']},
      {'id': 'j19-push',
       'mode': 'js',
       'title': 'Уведомление из push-сообщения',
       'statement': 'Напишите функции buildNotification(raw, defaults) и clickTarget(action, data, clients). '
                    'buildNotification: raw — тело push-сообщения (строка или null). defaults = { title, '
                    'icon, url }. Если raw — JSON-объект (строка, начинающаяся с «{», которая разбирается), '
                    'берутся поля title, body, icon, tag, url, actions, requireInteraction, silent; если '
                    'JSON не разобрался или raw — обычный текст, то title = defaults.title, body = raw; '
                    'null/пусто — только title по умолчанию. Результат { title, options }: options = { body '
                    '(если есть), icon (из сообщения или defaults.icon; если нигде нет — не добавлять), tag '
                    '(если есть), actions (не более 2 первых, каждое { action, title }; если нет — не '
                    'добавлять), requireInteraction (true только если был true), silent (true только если '
                    'был true), data: { url } } где url — из сообщения, иначе defaults.url, иначе «/». '
                    'clickTarget(action, data, clients): clients — [{ url, focused }]; action «dismiss» → { '
                    'type: "none" }; иначе ищем клиента, чей pathname совпадает с pathname data.url '
                    '(параметры и фрагмент не важны): если нашли — { type: "focus", index } (предпочитая '
                    'сфокусированного, иначе первого); иначе { type: "open", url: data.url }.',
       'starter': 'function buildNotification(raw, defaults) {\n'
                  '}\n'
                  'function clickTarget(action, data, clients) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const def = { title: "Заметки", icon: "/icon.png", url: "/inbox" };\n'
                 'for (const raw of '
                 '[\'{"title":"Новое","body":"Письмо","tag":"m1","url":"/mail/1","actions":[{"action":"open","title":"Открыть","icon":"x"},{"action":"dismiss","title":"Скрыть"},{"action":"third","title":"Третье"}],"requireInteraction":true,"silent":false}\', '
                 '"Просто текст", "", null, "{сломано", \'{"body":"без '
                 'заголовка","icon":"/own.png","silent":true}\', \'{"title":"T","url":"/x","actions":[]}\', '
                 '"[1,2]", \'{"requireInteraction":"yes"}\']) '
                 'console.log(JSON.stringify(canon(buildNotification(raw, def))));\n'
                 'console.log(JSON.stringify(canon(buildNotification("текст", { title: "Без иконки" }))));\n'
                 'const cl = [{ url: "https://app.ru/inbox?x=1#a", focused: false }, { url: '
                 '"https://app.ru/mail/1", focused: false }, { url: "https://app.ru/mail/1?tab=2", focused: '
                 'true }];\n'
                 'for (const [a, u] of [["open", "/mail/1"], ["open", "/inbox"], ["open", "/nope"], '
                 '["dismiss", "/mail/1"], ["", "https://app.ru/mail/1#x"], ["", "/mail/1/"]]) '
                 'console.log(a.padEnd(8), u.padEnd(26), JSON.stringify(clickTarget(a, { url: u }, cl)));\n'
                 'console.log(JSON.stringify(clickTarget("open", { url: "/a" }, [])));\n',
       'hint': 'Сначала разберите JSON безопасно; затем соберите options по таблице правил; клиент ищите по '
               'pathname.',
       'expected': ['{"options":{"actions":[{"action":"open","title":"Открыть"},{"action":"dismiss","title":"Скрыть"}],"body":"Письмо","data":{"url":"/mail/1"},"icon":"/icon.png","requireInteraction":true,"tag":"m1"},"title":"Новое"}',
                    '{"options":{"body":"Просто '
                    'текст","data":{"url":"/inbox"},"icon":"/icon.png"},"title":"Заметки"}',
                    '{"options":{"data":{"url":"/inbox"},"icon":"/icon.png"},"title":"Заметки"}',
                    '{"options":{"data":{"url":"/inbox"},"icon":"/icon.png"},"title":"Заметки"}',
                    '{"options":{"body":"{сломано","data":{"url":"/inbox"},"icon":"/icon.png"},"title":"Заметки"}',
                    '{"options":{"body":"без '
                    'заголовка","data":{"url":"/inbox"},"icon":"/own.png","silent":true},"title":"Заметки"}',
                    '{"options":{"data":{"url":"/x"},"icon":"/icon.png"},"title":"T"}',
                    '{"options":{"body":"[1,2]","data":{"url":"/inbox"},"icon":"/icon.png"},"title":"Заметки"}',
                    '{"options":{"data":{"url":"/inbox"},"icon":"/icon.png"},"title":"Заметки"}',
                    '{"options":{"body":"текст","data":{"url":"/"}},"title":"Без иконки"}',
                    'open     /mail/1                    {"type":"focus","index":2}',
                    'open     /inbox                     {"type":"focus","index":0}',
                    'open     /nope                      {"type":"open","url":"/nope"}',
                    'dismiss  /mail/1                    {"type":"none"}',
                    '         https://app.ru/mail/1#x    {"type":"focus","index":2}',
                    '         /mail/1/                   {"type":"open","url":"/mail/1/"}',
                    '{"type":"open","url":"/a"}']},
      {'id': 'j19-vapid-helpers',
       'mode': 'js',
       'title': 'Base64url и заготовка VAPID',
       'statement': 'Напишите функции base64urlEncode(bytes) → строка (Uint8Array → base64 с заменой '
                    '«+»→«-», «/»→«_» и без «=»), base64urlDecode(str) → Uint8Array (принимает и «-_» и '
                    '«+/», с «=» и без), urlBase64ToUint8Array — псевдоним decode, vapidClaims({ endpoint, '
                    'subject, nowMs, ttlSec = 43200 }) → { aud (origin адреса endpoint), exp (целые секунды: '
                    'floor(nowMs/1000) + ttl, но не более 24 часов от now: ttl ограничивается 86400), sub '
                    '(subject) } и signingInput(header, claims) → base64url(JSON.stringify(header)) + «.» + '
                    'base64url(JSON.stringify(claims)) (JSON кодируется как UTF-8). Некорректные символы в '
                    'base64urlDecode — Error с message «Некорректный base64url». Использовать '
                    'btoa/atob/Buffer можно.',
       'starter': 'function base64urlEncode(bytes) {\n'
                  '}\n'
                  'function base64urlDecode(str) {\n'
                  '}\n'
                  'function vapidClaims(options) {\n'
                  '}\n'
                  'function signingInput(header, claims) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const hex = (u) => [...u].map((b) => b.toString(16).padStart(2, "0")).join("");\n'
                 'for (const bytes of [[], [0], [251, 255, 191], [255, 254, 253, 252], [1, 2, 3, 4, 5], '
                 '[248, 62, 190]]) { const e = base64urlEncode(Uint8Array.from(bytes)); '
                 'console.log(JSON.stringify(e), hex(base64urlDecode(e)) === hex(Uint8Array.from(bytes))); '
                 '}\n'
                 'console.log(hex(base64urlDecode("-_-_")), hex(base64urlDecode("+/+/")), '
                 'hex(base64urlDecode("AQID")), hex(base64urlDecode("AQI=")), hex(base64urlDecode("AQI")), '
                 'hex(urlBase64ToUint8Array("_-8")));\n'
                 'for (const bad of ["a$b", "A", "ab cd", "AQ=I"]) { try { base64urlDecode(bad); '
                 'console.log("нет ошибки", bad); } catch (e) { console.log(e.message); } }\n'
                 'console.log(JSON.stringify(canon(vapidClaims({ endpoint: '
                 '"https://fcm.googleapis.com/fcm/send/abc", subject: "mailto:a@x.ru", nowMs: '
                 '1_700_000_000_999 }))));\n'
                 'console.log(JSON.stringify(canon(vapidClaims({ endpoint: '
                 '"https://updates.push.services.mozilla.com:8443/wpush/v2/x", subject: "https://x.ru", '
                 'nowMs: 1000, ttlSec: 999999 }))), vapidClaims({ endpoint: "https://a.ru/x", subject: "s", '
                 'nowMs: 5000, ttlSec: 60 }).exp);\n'
                 'const si = signingInput({ typ: "JWT", alg: "ES256" }, { aud: "https://a.ru", sub: "ж" }); '
                 'console.log(si); console.log(new '
                 'TextDecoder().decode(base64urlDecode(si.split(".")[1])));\n',
       'hint': 'btoa/atob работают с «бинарными» строками; приведите алфавит к стандартному и допишите «=».',
       'expected': ['"" true',
                    '"AA" true',
                    '"-_-_" true',
                    '"__79_A" true',
                    '"AQIDBAU" true',
                    '"-D6-" true',
                    'fbffbf fbffbf 010203 0102 0102 ffef',
                    'Некорректный base64url',
                    'Некорректный base64url',
                    'Некорректный base64url',
                    'Некорректный base64url',
                    '{"aud":"https://fcm.googleapis.com","exp":1700043200,"sub":"mailto:a@x.ru"}',
                    '{"aud":"https://updates.push.services.mozilla.com:8443","exp":86401,"sub":"https://x.ru"} '
                    '65',
                    'eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJhdWQiOiJodHRwczovL2EucnUiLCJzdWIiOiLQtiJ9',
                    '{"aud":"https://a.ru","sub":"ж"}']},
      {'id': 'j19-sync-queue',
       'mode': 'js',
       'title': 'Очередь фоновой синхронизации',
       'statement': 'Напишите функцию createSyncQueue({ storage, key = "sync-queue", send, now, '
                    'maxRetentionMs = 86400000, maxAttempts = 3 }): storage — { getItem, setItem } (строки). '
                    'Возвращает { add(request), process(), size(), items() }. Очередь хранится в storage '
                    'JSON-массивом { request, addedAt, attempts } и должна восстанавливаться при создании '
                    '(новый экземпляр с тем же storage видит прежние записи). add — добавить в конец '
                    '(addedAt = now(), attempts = 0), сохранить. process() → промис { sent, dropped, '
                    'remaining }: обходит очередь по порядку: запись, старше maxRetentionMs (now − addedAt > '
                    'maxRetentionMs), удаляется и считается dropped; иначе вызывается send(request): успех — '
                    'запись удаляется, sent++; ошибка (исключение или отклонённый промис) — attempts++ и '
                    'сохранить; если attempts достиг maxAttempts — запись удаляется (dropped++) и обход '
                    'продолжается, иначе обход прекращается (остальные записи остаются нетронутыми, чтобы '
                    'порядок не нарушался). В конце сохранить очередь. remaining — длина очереди. size() — '
                    'длина, items() — копии записей.',
       'starter': 'function createSyncQueue(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'let t = 0; const store = new Map(); const storage = { getItem: (k) => store.get(k) ?? '
                 'null, setItem: (k, v) => store.set(k, v) };\n'
                 'const sentLog = []; let failing = new Set();\n'
                 'const send = async (r) => { sentLog.push(r); if (failing.has(r)) throw new Error("нет '
                 'сети"); };\n'
                 'const q = createSyncQueue({ storage, send, now: () => t, maxRetentionMs: 1000, '
                 'maxAttempts: 2 });\n'
                 'const show = async (label) => { const r = await q.process(); console.log(label.padEnd(18), '
                 'JSON.stringify(canon(r)), "отправки:", sentLog.splice(0).join(), "| в очереди:", '
                 'q.items().map((x) => `${x.request}#${x.attempts}`).join(",")); };\n'
                 'q.add("a"); q.add("b"); q.add("c"); console.log(q.size(), '
                 'JSON.parse(store.get("sync-queue")).length);\n'
                 'failing = new Set(["b"]); await show("b падает"); await show("b падает снова"); await '
                 'show("после"); \n'
                 'failing = new Set(); q.add("d"); t = 500; q.add("e"); t = 1200; await show("d устарела"); '
                 't = 2000; await show("e устарела");\n'
                 'failing = new Set(["x", "y"]); q.add("x"); q.add("y"); const q2 = createSyncQueue({ '
                 'storage, send, now: () => t, maxRetentionMs: 1000, maxAttempts: 2 }); '
                 'console.log(q2.size(), q2.items().map((i) => i.request).join());\n'
                 'console.log(JSON.stringify(canon(await q2.process())), sentLog.splice(0).join(), '
                 'q2.items().map((i) => i.attempts).join()); failing = new Set(["y"]); '
                 'console.log(JSON.stringify(canon(await q2.process())), sentLog.splice(0).join(), '
                 'q2.items().map((i) => `${i.request}#${i.attempts}`).join());\n'
                 'console.log(JSON.stringify(canon(await q2.process())), q2.size(), '
                 'JSON.parse(store.get("sync-queue")).length, JSON.stringify(canon(await createSyncQueue({ '
                 'storage, send, now: () => t }).process())));\n'
                 'const asyncFail = createSyncQueue({ storage: { getItem: () => null, setItem() {} }, send: '
                 '() => Promise.reject(new Error("отказ")), now: () => 0, maxAttempts: 1 }); '
                 'asyncFail.add(1); console.log(JSON.stringify(canon(await asyncFail.process())));\n',
       'hint': 'Очередь — массив; в process идите по голове: успех/устарела — shift; сбой — attempts++ и '
               'break (или drop).',
       'expected': ['3 3',
                    'b падает           {"dropped":0,"remaining":2,"sent":1} отправки: a,b | в очереди: '
                    'b#1,c#0',
                    'b падает снова     {"dropped":1,"remaining":0,"sent":1} отправки: b,c | в очереди:',
                    'после              {"dropped":0,"remaining":0,"sent":0} отправки:  | в очереди:',
                    'd устарела         {"dropped":1,"remaining":0,"sent":1} отправки: e | в очереди:',
                    'e устарела         {"dropped":0,"remaining":0,"sent":0} отправки:  | в очереди:',
                    '2 x,y',
                    '{"dropped":0,"remaining":2,"sent":0} x 1,0',
                    '{"dropped":0,"remaining":1,"sent":1} x,y y#1',
                    '{"dropped":1,"remaining":0,"sent":0} 0 0 {"dropped":0,"remaining":0,"sent":0}',
                    '{"dropped":1,"remaining":0,"sent":0}']},
      {'id': 'j19-manifest-validate',
       'mode': 'js',
       'title': 'Проверка манифеста приложения',
       'statement': 'Напишите функции validateManifest(m) → массив кодов проблем (в порядке проверок) и '
                    'isInstallable(m) → boolean. Проверки по порядку: «name-missing» — нет ни name, ни '
                    'short_name; «short-name-long» — short_name длиннее 12 символов; «start-url-missing» — '
                    'нет start_url; «start-url-out-of-scope» — заданы start_url и scope, и start_url '
                    '(относительно https://app.ru/) не лежит внутри scope (путь scope — префикс пути '
                    'start_url; если scope не задан, считается папкой start_url — проверка проходит); '
                    '«display-invalid» — display задан, но не из fullscreen, standalone, minimal-ui, '
                    'browser; «icon-192-missing» и «icon-512-missing» — нет иконки подходящего размера '
                    '(sizes — строка размеров через пробел вида «192x192»; подходит размер ровно 192x192 / '
                    '512x512 или «any»; для 512 подходит и размер больше 512); «icon-maskable-missing» — ни '
                    'у одной иконки purpose не содержит «maskable»; «theme-color-invalid» — theme_color '
                    'задан и не вида #rgb/#rrggbb. isInstallable: нет проблем кодов name-missing, '
                    'start-url-missing, display-invalid, icon-192-missing, icon-512-missing и display (если '
                    'задан) не «browser» (по умолчанию display считается «browser» — не устанавливаемый '
                    'режим, поэтому нужно явно standalone, fullscreen или minimal-ui).',
       'starter': 'function validateManifest(m) {\n}\nfunction isInstallable(m) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const good = { name: "Заметки", short_name: "Notes", start_url: "/app/", scope: "/app/", '
                 'display: "standalone", theme_color: "#1a73e8", icons: [{ src: "a.png", sizes: "192x192", '
                 'purpose: "any" }, { src: "b.png", sizes: "512x512", purpose: "any maskable" }] };\n'
                 'const cases = [["хороший", good], ["пустой", {}], ["только short", { short_name: "Очень '
                 'длинное имя" }], ["вне scope", { ...good, start_url: "/other/" }], ["scope без start", { '
                 '...good, start_url: undefined }], ["start без scope", { ...good, scope: undefined, '
                 'start_url: "/x/y.html" }], ["display", { ...good, display: "tv" }], ["browser", { ...good, '
                 'display: "browser" }], ["без display", { ...good, display: undefined }],\n'
                 '  ["иконка any", { ...good, icons: [{ src: "x.svg", sizes: "any" }] }], ["большая иконка", '
                 '{ ...good, icons: [{ sizes: "192x192" }, { sizes: "1024x1024", purpose: "maskable" }] }], '
                 '["несколько размеров", { ...good, icons: [{ sizes: "48x48 192x192 512x512", purpose: '
                 '"monochrome" }] }], ["маленькие", { ...good, icons: [{ sizes: "48x48 96x96" }] }], ["без '
                 'иконок", { ...good, icons: undefined }],\n'
                 '  ["цвет", { ...good, theme_color: "red" }], ["цвет rgb", { ...good, theme_color: "#FFF" '
                 '}], ["fullscreen", { ...good, display: "fullscreen" }], ["minimal", { ...good, display: '
                 '"minimal-ui" }], ["имя 12", { ...good, short_name: "123456789012" }], ["имя 13", { '
                 '...good, short_name: "1234567890123" }]];\n'
                 'for (const [n, m] of cases) console.log(n.padEnd(18), JSON.stringify(validateManifest(m)), '
                 'isInstallable(m));\n',
       'hint': 'Список проверок по порядку; для иконок соберите все размеры в один массив.',
       'expected': ['хороший            [] true',
                    'пустой             '
                    '["name-missing","start-url-missing","icon-192-missing","icon-512-missing","icon-maskable-missing"] '
                    'false',
                    'только short       '
                    '["short-name-long","start-url-missing","icon-192-missing","icon-512-missing","icon-maskable-missing"] '
                    'false',
                    'вне scope          ["start-url-out-of-scope"] true',
                    'scope без start    ["start-url-missing"] false',
                    'start без scope    [] true',
                    'display            ["display-invalid"] false',
                    'browser            [] false',
                    'без display        [] false',
                    'иконка any         ["icon-maskable-missing"] true',
                    'большая иконка     [] true',
                    'несколько размеров ["icon-maskable-missing"] true',
                    'маленькие          ["icon-192-missing","icon-512-missing","icon-maskable-missing"] '
                    'false',
                    'без иконок         ["icon-192-missing","icon-512-missing","icon-maskable-missing"] '
                    'false',
                    'цвет               ["theme-color-invalid"] true',
                    'цвет rgb           [] true',
                    'fullscreen         [] true',
                    'minimal            [] true',
                    'имя 12             [] true',
                    'имя 13             ["short-name-long"] true']},
      {'id': 'j19-manifest-resolve',
       'mode': 'js',
       'title': 'Разбор адресов манифеста',
       'statement': 'Напишите функции resolveManifest(manifest, manifestUrl) и inScope(resolved, url). '
                    'resolveManifest → { startUrl, scope, id, icons } со всеми абсолютными адресами '
                    'относительно manifestUrl: startUrl — абсолютный start_url (если нет — сам адрес '
                    'документа... для простоты — manifestUrl без имени файла, т.е. папка манифеста); scope — '
                    'абсолютный scope, а если не задан — папка startUrl (путь до последнего «/»); id — '
                    'абсолютный id (если id задан — origin + путь id, без фрагмента), иначе startUrl без '
                    'фрагмента #; icons — для каждой иконки { src (абсолютный), sizes (массив чисел — ширина '
                    'из «NxN»; «any» → строка «any»), purpose (массив слов, по умолчанию [«any»]) }; иконки '
                    'с пустым src пропускаются. Если startUrl не лежит внутри scope (по префиксу адреса) или '
                    'другого источника — scope заменяется на папку startUrl. inScope(resolved, url) → true, '
                    'если адрес url начинается с resolved.scope (сравнение префикса полного адреса без '
                    'фрагмента).',
       'starter': 'function resolveManifest(manifest, manifestUrl) {\n'
                  '}\n'
                  'function inScope(resolved, url) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const mu = "https://app.ru/static/manifest.webmanifest";\n'
                 'const show = (m) => console.log(JSON.stringify(canon(resolveManifest(m, mu))));\n'
                 'show({});\n'
                 'show({ start_url: "/app/index.html?src=pwa#top", scope: "/app/", id: "/app/?id=1#x", '
                 'icons: [{ src: "/icons/a.png", sizes: "192x192", purpose: "maskable any" }, { src: '
                 '"b.svg", sizes: "any" }, { src: "", sizes: "10x10" }, { src: "https://cdn.ru/c.png" }] '
                 '});\n'
                 'show({ start_url: "page.html", scope: "/other/" });\n'
                 'show({ start_url: "https://other.ru/x/y", scope: "/" });\n'
                 'show({ start_url: "/a/b/c", id: "myapp" });\n'
                 'const r = resolveManifest({ start_url: "/app/", scope: "/app/" }, mu);\n'
                 'for (const u of ["https://app.ru/app/", "https://app.ru/app/page#x", "https://app.ru/app", '
                 '"https://app.ru/application", "https://other.ru/app/", "http://app.ru/app/"]) '
                 'console.log(u.padEnd(30), inScope(r, u));\n',
       'hint': 'URL с базой делает абсолютные адреса; «папка» — путь до последней косой черты.',
       'expected': ['{"icons":[],"id":"https://app.ru/static/","scope":"https://app.ru/static/","startUrl":"https://app.ru/static/"}',
                    '{"icons":[{"purpose":["maskable","any"],"sizes":[192],"src":"https://app.ru/icons/a.png"},{"purpose":["any"],"sizes":["any"],"src":"https://app.ru/static/b.svg"},{"purpose":["any"],"sizes":[],"src":"https://cdn.ru/c.png"}],"id":"https://app.ru/app/","scope":"https://app.ru/app/","startUrl":"https://app.ru/app/index.html?src=pwa#top"}',
                    '{"icons":[],"id":"https://app.ru/static/page.html","scope":"https://app.ru/static/","startUrl":"https://app.ru/static/page.html"}',
                    '{"icons":[],"id":"https://other.ru/x/y","scope":"https://other.ru/x/","startUrl":"https://other.ru/x/y"}',
                    '{"icons":[],"id":"https://app.ru/myapp","scope":"https://app.ru/a/b/","startUrl":"https://app.ru/a/b/c"}',
                    'https://app.ru/app/            true',
                    'https://app.ru/app/page#x      true',
                    'https://app.ru/app             false',
                    'https://app.ru/application     false',
                    'https://other.ru/app/          false',
                    'http://app.ru/app/             false']},
      {'id': 'j19-install-prompt',
       'mode': 'js',
       'title': 'Собственная кнопка установки',
       'statement': 'Напишите функцию createInstallPrompt({ storage, now, snoozeDays = 7, key = '
                    '"install-snooze" }) → controller. Методы: onBeforeInstallPrompt(event) — запоминает '
                    'событие (event.prompt() → промис { outcome: "accepted" | "dismissed" }); canShow() → '
                    'true, если есть сохранённое событие, приложение не установлено и «отсрочка» не '
                    'действует (отсрочка хранится в storage по ключу key как строка с временем окончания в '
                    'мс и переживает создание нового controller); show() → промис outcome или null, если '
                    'показывать нельзя: вызывает event.prompt() один раз (событие после показа сбрасывается '
                    '— повторно показать можно только после нового onBeforeInstallPrompt); «accepted» → '
                    'установлено (installed = true); «dismissed» → отсрочка до now() + snoozeDays суток '
                    '(запись в storage); onAppInstalled() — installed = true и событие сбрасывается; '
                    'свойство installed. Если show() вызван, пока предыдущий вызов ещё идёт, вернуть null '
                    '(одновременно один показ).',
       'starter': 'function createInstallPrompt(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const tick = () => new Promise((r) => setImmediate(r));\n'
                 'let t = 1000; const store = new Map(); const storage = { getItem: (k) => store.get(k) ?? '
                 'null, setItem: (k, v) => store.set(k, v) };\n'
                 'const ev = (outcome, log) => ({ prompt: () => { log.push("prompt"); return new Promise((r) '
                 '=> setTimeout(() => r({ outcome }), 5)); } });\n'
                 'const log = []; const c = createInstallPrompt({ storage, now: () => t, snoozeDays: 2 });\n'
                 'console.log(c.canShow(), await c.show(), c.installed);\n'
                 'c.onBeforeInstallPrompt(ev("dismissed", log)); console.log(c.canShow());\n'
                 'const p1 = c.show(); console.log(c.canShow(), await c.show()); console.log(await p1, '
                 'log.length, c.canShow(), store.get("install-snooze"));\n'
                 'c.onBeforeInstallPrompt(ev("accepted", log)); console.log(c.canShow(), await c.show()); t '
                 '+= 2 * 86400000 - 1; console.log(c.canShow()); t += 1; console.log(c.canShow());\n'
                 'const c2 = createInstallPrompt({ storage, now: () => t, snoozeDays: 2 }); '
                 'c2.onBeforeInstallPrompt(ev("accepted", log)); console.log(c2.canShow(), c2.installed);\n'
                 'console.log(await c2.show(), c2.installed, c2.canShow(), await c2.show()); '
                 'c2.onBeforeInstallPrompt(ev("accepted", log)); console.log(c2.canShow(), log.length);\n'
                 'const c3 = createInstallPrompt({ storage: { getItem: () => null, setItem() {} }, now: () '
                 '=> 0 }); c3.onBeforeInstallPrompt(ev("dismissed", [])); c3.onAppInstalled(); '
                 'console.log(c3.installed, c3.canShow(), await c3.show());\n'
                 'const c4 = createInstallPrompt({ storage: { getItem: () => null, setItem() {} }, now: () '
                 '=> 0 }); c4.onBeforeInstallPrompt(ev("dismissed", [])); await c4.show(); '
                 'console.log(c4.canShow()); c4.onBeforeInstallPrompt(ev("dismissed", [])); '
                 'console.log(c4.canShow());\n',
       'hint': 'Событие запоминается и «расходуется» при показе; отсрочку храните как время окончания в '
               'storage.',
       'expected': ['false null false',
                    'true',
                    'false null',
                    'dismissed 1 false 172801000',
                    'false null',
                    'false',
                    'true',
                    'true false',
                    'accepted true false null',
                    'false 2',
                    'true false null',
                    'false',
                    'true']},
      {'id': 'j19-eviction',
       'mode': 'js',
       'title': 'Вытеснение источников при нехватке квоты',
       'statement': 'Напишите функцию planEviction(origins, quota) → { evicted, remaining, overQuota }. '
                    'origins — массив { name, usage, lastUsed, persisted }; quota — общий лимит. Если '
                    'суммарное usage ≤ quota — ничего не вытесняется. Иначе вытесняются целые источники: '
                    'сначала непостоянные (persisted false) в порядке самого давнего lastUsed (при равенстве '
                    '— по имени по возрастанию), пока суммарное usage не станет ≤ quota; постоянные '
                    '(persisted true) не вытесняются никогда. evicted — имена в порядке вытеснения, '
                    'remaining — имена оставшихся источников (в исходном порядке), overQuota — true, если '
                    'даже после вытеснения всех непостоянных сумма больше quota. Вытеснение прекращается '
                    'ровно тогда, когда квота соблюдена (не вытеснять лишнего). Исходный массив не изменять.',
       'starter': 'function planEviction(origins, quota) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const O = (name, usage, lastUsed, persisted = false) => ({ name, usage, lastUsed, '
                 'persisted });\n'
                 'const list = [O("a.ru", 40, 5), O("b.ru", 30, 1), O("c.ru", 20, 3, true), O("d.ru", 25, '
                 '1), O("e.ru", 10, 9)];\n'
                 'const frozen = Object.freeze(list.map(Object.freeze));\n'
                 'for (const q of [200, 125, 120, 100, 60, 30, 20, 0]) console.log(q, '
                 'JSON.stringify(canon(planEviction(frozen, q))));\n'
                 'console.log(JSON.stringify(canon(planEviction([], 10))), '
                 'JSON.stringify(canon(planEviction([O("p", 100, 1, true)], 10))), '
                 'JSON.stringify(canon(planEviction([O("p", 100, 1, true), O("q", 5, 1)], 10))));\n',
       'hint': 'Отсортируйте непостоянных по давности и убирайте по одному, пока сумма не уложится в квоту.',
       'expected': ['200 {"evicted":[],"overQuota":false,"remaining":["a.ru","b.ru","c.ru","d.ru","e.ru"]}',
                    '125 {"evicted":[],"overQuota":false,"remaining":["a.ru","b.ru","c.ru","d.ru","e.ru"]}',
                    '120 {"evicted":["b.ru"],"overQuota":false,"remaining":["a.ru","c.ru","d.ru","e.ru"]}',
                    '100 {"evicted":["b.ru"],"overQuota":false,"remaining":["a.ru","c.ru","d.ru","e.ru"]}',
                    '60 {"evicted":["b.ru","d.ru","a.ru"],"overQuota":false,"remaining":["c.ru","e.ru"]}',
                    '30 {"evicted":["b.ru","d.ru","a.ru"],"overQuota":false,"remaining":["c.ru","e.ru"]}',
                    '20 {"evicted":["b.ru","d.ru","a.ru","e.ru"],"overQuota":false,"remaining":["c.ru"]}',
                    '0 {"evicted":["b.ru","d.ru","a.ru","e.ru"],"overQuota":true,"remaining":["c.ru"]}',
                    '{"evicted":[],"overQuota":false,"remaining":[]} '
                    '{"evicted":[],"overQuota":true,"remaining":["p"]} '
                    '{"evicted":["q"],"overQuota":true,"remaining":["p"]}']},
      {'id': 'j19-leader-election',
       'mode': 'js',
       'title': 'Выбор главной вкладки',
       'statement': 'Напишите функцию createElection({ id, channel, timers, heartbeat = 1000, timeout = '
                    '3000, now }): channel = { postMessage(msg), onmessage }: входящее событие onmessage({ '
                    'data }); timers = { setTimeout, clearTimeout }, now() — время в мс. Возвращает { '
                    'start(), stop(), isLeader(), onChange(fn) }. Протокол: сообщения { type: '
                    '"hello"|"alive"|"bye", id }. start(): сразу отправить hello, затем каждые heartbeat мс '
                    'отправлять alive (цепочкой setTimeout). При получении hello/alive от другого id '
                    'запомнить lastSeen[id] = now(); на hello дополнительно сразу ответить alive (чтобы '
                    'новичок узнал о нас); на bye — сразу забыть id. Лидер — вкладка с наименьшим id '
                    '(строковое сравнение) среди себя и «живых» (lastSeen не старше timeout; устаревших '
                    'вычёркиваем при каждой проверке). Лидерство пересчитывается после start, при каждом '
                    'входящем сообщении и при каждом тике heartbeat; когда оно меняется — вызываются '
                    'подписчики onChange(isLeader) (только при изменении, включая первое определение: после '
                    'start вкладка без соседей становится лидером). stop(): отправить bye, остановить '
                    'таймеры, больше не реагировать на сообщения; isLeader() после stop — false.',
       'starter': 'function createElection(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const FAKE = () => { let t = 0; const timers = new Map(); let id = 1; return { now: () => '
                 't, setTimeout(fn, ms) { const i = id++; timers.set(i, { at: t + ms, fn }); return i; }, '
                 'clearTimeout(i) { timers.delete(i); }, advance(ms) { const end = t + ms; for (;;) { const '
                 'due = [...timers].filter(([, x]) => x.at <= end).sort((a, b) => a[1].at - b[1].at || a[0] '
                 '- b[0])[0]; if (!due) break; timers.delete(due[0]); t = due[1].at; due[1].fn(); } t = end; '
                 '}, pending: () => timers.size }; };\n'
                 'const clock = FAKE(); const bus = []; const mkChannel = () => { const ch = { onmessage: '
                 'null, __id: null }; ch.postMessage = (m) => { for (const o of bus) if (o !== ch) '
                 'o.onmessage?.({ data: structuredClone(m) }); }; bus.push(ch); return ch; };\n'
                 'const tabs = {}; const events = [];\n'
                 'const open = (id) => { const chn = mkChannel(); chn.__id = id; const e = createElection({ '
                 'id, channel: chn, timers: clock, now: clock.now }); e.onChange((l) => '
                 'events.push(`${id}:${l}`)); tabs[id] = e; e.start(); return e; };\n'
                 'const status = (label) => console.log(label.padEnd(16), Object.entries(tabs).map(([k, e]) '
                 '=> `${k}=${e.isLeader() ? "L" : "-"}`).join(" "), "|", events.splice(0).join(" "));\n'
                 'open("tab-b"); status("b один"); open("tab-c"); status("+c"); open("tab-a"); status("+a '
                 '(меньший id)");\n'
                 'clock.advance(1000); status("heartbeat"); clock.advance(5000); status("5 секунд");\n'
                 'tabs["tab-a"].stop(); status("a закрыта"); console.log(tabs["tab-a"].isLeader());\n'
                 'clock.advance(2000); status("ещё"); tabs["tab-b"].stop(); status("b закрыта"); '
                 'clock.advance(10000); status("ещё 10 с");\n'
                 'open("tab-d"); status("+d"); console.log(clock.pending());\n'
                 'const crash = (id) => { const ch = bus.find((c) => c.__id === id); ch.postMessage = () => '
                 '{}; bus.splice(bus.indexOf(ch), 1); };\n'
                 'tabs["tab-d"].stop(); delete tabs["tab-d"]; clock.advance(100); status("d закрыта");\n'
                 'open("tab-0"); status("+0"); clock.advance(500); status("+500"); crash("tab-0"); '
                 'clock.advance(1000); status("0 упала +1с"); clock.advance(1000); status("+2с"); '
                 'clock.advance(1000); status("+3с"); clock.advance(1000); status("+4с"); '
                 'clock.advance(1000); status("+5с");\n',
       'hint': 'lastSeen для соседей; лидер — минимальный id среди живых; пересчёт при сообщениях и на '
               'каждом тике.',
       'expected': ['b один           tab-b=L | tab-b:true',
                    '+c               tab-b=L tab-c=- |',
                    '+a (меньший id)  tab-b=- tab-c=- tab-a=L | tab-a:true tab-b:false',
                    'heartbeat        tab-b=- tab-c=- tab-a=L |',
                    '5 секунд         tab-b=- tab-c=- tab-a=L |',
                    'a закрыта        tab-b=L tab-c=- tab-a=- | tab-b:true tab-a:false',
                    'false',
                    'ещё              tab-b=L tab-c=- tab-a=- |',
                    'b закрыта        tab-b=- tab-c=L tab-a=- | tab-c:true tab-b:false',
                    'ещё 10 с         tab-b=- tab-c=L tab-a=- |',
                    '+d               tab-b=- tab-c=L tab-a=- tab-d=- |',
                    '2',
                    'd закрыта        tab-b=- tab-c=L tab-a=- |',
                    '+0               tab-b=- tab-c=- tab-a=- tab-0=L | tab-0:true tab-c:false',
                    '+500             tab-b=- tab-c=- tab-a=- tab-0=L |',
                    '0 упала +1с      tab-b=- tab-c=- tab-a=- tab-0=L |',
                    '+2с              tab-b=- tab-c=- tab-a=- tab-0=L |',
                    '+3с              tab-b=- tab-c=- tab-a=- tab-0=L |',
                    '+4с              tab-b=- tab-c=L tab-a=- tab-0=L | tab-c:true',
                    '+5с              tab-b=- tab-c=L tab-a=- tab-0=L |']},
      {'id': 'j19-cache-expiration',
       'mode': 'js',
       'title': 'Срок жизни записей кеша',
       'statement': 'Напишите функцию createExpiration({ maxEntries, maxAgeMs, now }) → { add(url), '
                    'has(url), remove(url), entries() }. add(url) — запомнить (или обновить) время '
                    'добавления url = now() и считать его самым свежим; затем вычислить вытеснение и вернуть '
                    'массив адресов, которые нужно удалить из кеша: сначала все просроченные записи (now() − '
                    'addedAt > maxAgeMs; сам url свежей добавленной записи не просрочен), в порядке '
                    'добавления; затем, если записей больше maxEntries, — самые давно использованные (то '
                    'есть добавленные/обновлённые раньше всех), пока не останется maxEntries. Эти адреса из '
                    'внутреннего учёта удаляются. has(url) — есть ли запись и не просрочена ли она '
                    '(просроченная — false, но не удаляется сама до следующего add). remove(url) — убрать из '
                    'учёта. entries() → адреса от самого давнего к самому свежему (включая просроченные, ещё '
                    'не вытесненные).',
       'starter': 'function createExpiration(options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let t = 0; const e = createExpiration({ maxEntries: 3, maxAgeMs: 1000, now: () => t });\n'
                 'const add = (u) => console.log(t, "add", u, JSON.stringify(e.add(u)), '
                 'e.entries().join());\n'
                 'add("a"); t = 100; add("b"); t = 200; add("c"); t = 300; add("d"); t = 400; add("b"); t = '
                 '500; add("e");\n'
                 'console.log(e.has("b"), e.has("a"), e.has("zzz")); t = 1450; console.log(e.has("e"), '
                 'e.has("b"), e.entries().join()); add("f"); t = 1500; add("g");\n'
                 'e.remove("g"); e.remove("nope"); console.log(e.entries().join(), e.has("g")); t = 5000; '
                 'add("h"); console.log(e.entries().join());\n'
                 'const one = createExpiration({ maxEntries: 1, maxAgeMs: 10, now: () => t }); '
                 'console.log(JSON.stringify(one.add("x")), JSON.stringify(one.add("y")), '
                 'JSON.stringify(one.add("y")), one.entries().join());\n'
                 'const zero = createExpiration({ maxEntries: 5, maxAgeMs: 0, now: () => t }); '
                 'console.log(JSON.stringify(zero.add("p")), zero.has("p")); t += 1; '
                 'console.log(zero.has("p"), JSON.stringify(zero.add("q")), zero.entries().join());\n',
       'hint': 'Map сохраняет порядок вставки: чтобы «освежить» запись, удалите и вставьте её заново.',
       'expected': ['0 add a [] a',
                    '100 add b [] a,b',
                    '200 add c [] a,b,c',
                    '300 add d ["a"] b,c,d',
                    '400 add b [] c,d,b',
                    '500 add e ["c"] d,b,e',
                    'true false false',
                    'true false d,b,e',
                    '1450 add f ["d","b"] e,f',
                    '1500 add g [] e,f,g',
                    'e,f false',
                    '5000 add h ["e","f"] h',
                    'h',
                    '[] ["x"] [] y',
                    '[] true',
                    'false ["p"] q']},
      {'id': 'j19-range-request',
       'mode': 'js',
       'title': 'Запросы с Range (частичные ответы)',
       'statement': 'Напишите функции parseRange(header, size) и rangeResponse(body, rangeHeader, '
                    'contentType). parseRange → { start, end } (включительно) для одного диапазона вида '
                    '«bytes=0-99», «bytes=500-» (до конца), «bytes=-100» (последние 100 байт); end сверху '
                    'ограничивается size − 1; если start ≥ size (или суффикс 0) — «unsatisfiable»; для '
                    'некорректных заголовков, нескольких диапазонов («bytes=0-1,5-6»), другой единицы или '
                    'start > end — null (игнорировать Range). rangeResponse(body, rangeHeader, contentType): '
                    'body — Uint8Array. Без Range (null/undefined) или при null из parseRange → { status: '
                    '200, headers: { "content-type", "content-length": размер, "accept-ranges": "bytes" }, '
                    'body }. При корректном диапазоне → { status: 206, headers: { content-type, '
                    'content-length: длина части, accept-ranges, "content-range": "bytes start-end/size" }, '
                    'body: срез }. При «unsatisfiable» → { status: 416, headers: { "content-range": "bytes '
                    '*/size" }, body: пустой Uint8Array }. Значения заголовков — строки.',
       'starter': 'function parseRange(header, size) {\n'
                  '}\n'
                  'function rangeResponse(body, rangeHeader, contentType) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'for (const h of ["bytes=0-99", "bytes=0-0", "bytes=500-", "bytes=-100", "bytes=-2000", '
                 '"bytes=900-2000", "bytes=1000-", "bytes=1000-1010", "bytes=-0", "bytes=5-2", '
                 '"bytes=0-1,5-6", "items=0-1", "bytes=", "bytes=-", "bytes=a-b", "", undefined, " '
                 'bytes=10-20 ", "bytes=999-999"]) console.log(JSON.stringify(h), '
                 'JSON.stringify(parseRange(h, 1000)));\n'
                 'const body = Uint8Array.from({ length: 10 }, (_, i) => i * 10);\n'
                 'const show = (h) => { const r = rangeResponse(body, h, "video/mp4"); '
                 'console.log(JSON.stringify(h), r.status, JSON.stringify(canon(r.headers)), '
                 '[...r.body].join()); };\n'
                 'show(undefined); show(null); show("bytes=2-4"); show("bytes=7-"); show("bytes=-3"); '
                 'show("bytes=0-100"); show("bytes=10-"); show("bytes=-0"); show("мусор"); '
                 'show("bytes=0-1,3-4");\n'
                 'console.log(rangeResponse(new Uint8Array(0), "bytes=0-0", "a/b").status, rangeResponse(new '
                 'Uint8Array(0), null, "a/b").headers["content-length"]);\n',
       'hint': 'Регулярное выражение с двумя необязательными числами; три формы: «a-b», «a-», «-n».',
       'expected': ['"bytes=0-99" {"start":0,"end":99}',
                    '"bytes=0-0" {"start":0,"end":0}',
                    '"bytes=500-" {"start":500,"end":999}',
                    '"bytes=-100" {"start":900,"end":999}',
                    '"bytes=-2000" {"start":0,"end":999}',
                    '"bytes=900-2000" {"start":900,"end":999}',
                    '"bytes=1000-" "unsatisfiable"',
                    '"bytes=1000-1010" "unsatisfiable"',
                    '"bytes=-0" "unsatisfiable"',
                    '"bytes=5-2" null',
                    '"bytes=0-1,5-6" null',
                    '"items=0-1" null',
                    '"bytes=" null',
                    '"bytes=-" null',
                    '"bytes=a-b" null',
                    '"" null',
                    'undefined null',
                    '" bytes=10-20 " {"start":10,"end":20}',
                    '"bytes=999-999" {"start":999,"end":999}',
                    'undefined 200 '
                    '{"accept-ranges":"bytes","content-length":"10","content-type":"video/mp4"} '
                    '0,10,20,30,40,50,60,70,80,90',
                    'null 200 {"accept-ranges":"bytes","content-length":"10","content-type":"video/mp4"} '
                    '0,10,20,30,40,50,60,70,80,90',
                    '"bytes=2-4" 206 {"accept-ranges":"bytes","content-length":"3","content-range":"bytes '
                    '2-4/10","content-type":"video/mp4"} 20,30,40',
                    '"bytes=7-" 206 {"accept-ranges":"bytes","content-length":"3","content-range":"bytes '
                    '7-9/10","content-type":"video/mp4"} 70,80,90',
                    '"bytes=-3" 206 {"accept-ranges":"bytes","content-length":"3","content-range":"bytes '
                    '7-9/10","content-type":"video/mp4"} 70,80,90',
                    '"bytes=0-100" 206 {"accept-ranges":"bytes","content-length":"10","content-range":"bytes '
                    '0-9/10","content-type":"video/mp4"} 0,10,20,30,40,50,60,70,80,90',
                    '"bytes=10-" 416 {"content-range":"bytes */10"}',
                    '"bytes=-0" 416 {"content-range":"bytes */10"}',
                    '"мусор" 200 {"accept-ranges":"bytes","content-length":"10","content-type":"video/mp4"} '
                    '0,10,20,30,40,50,60,70,80,90',
                    '"bytes=0-1,3-4" 200 '
                    '{"accept-ranges":"bytes","content-length":"10","content-type":"video/mp4"} '
                    '0,10,20,30,40,50,60,70,80,90',
                    '416 0']}]}
