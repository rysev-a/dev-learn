"""Задачи книги «Современный Frontend»: глава 21."""

TASKS: dict[int, list[dict]] = {21: [{'id': 'j21-emitter',
  'mode': 'js',
  'title': 'Свой EventEmitter',
  'statement': 'Напишите класс Emitter с методами: on(name, fn) и once(name, fn) (возвращают '
               'this), off(name, fn) (снимает первое совпадение; для once-обёртки сравнивается '
               'исходная функция), prependListener(name, fn), emit(name, ...args) → true, если '
               'были обработчики, иначе false; listenerCount(name); listeners(name) — копия '
               'массива исходных функций. emit работает со снимком списка на момент вызова '
               '(подписки/отписки внутри обработчиков действуют со следующего emit); '
               "once-обработчик снимается до вызова. Событие 'error' без обработчиков: если "
               'аргумент — Error, он бросается; иначе бросается Error(`Unhandled error: ${arg}`).',
  'starter': 'class Emitter {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const e = new Emitter(); const log = [];\n'
            'const a = (x) => log.push("a" + x), b = (x) => log.push("b" + x);\n'
            'console.log(e.on("x", a) === e, e.once("x", b) === e, e.listenerCount("x"), '
            'e.listeners("x").length, e.listeners("x")[1] === b);\n'
            'console.log(e.emit("x", 1), e.emit("x", 2), e.emit("none"), log.join());\n'
            'e.prependListener("x", () => log.push("first"));\n'
            'log.length = 0; e.emit("x", 3); console.log(log.join());\n'
            'e.off("x", a); log.length = 0; e.emit("x", 4); console.log(log.join(), '
            'e.listenerCount("x"));\n'
            'log.length = 0;\n'
            'const c = new Emitter();\n'
            'const self = () => { log.push("self"); c.off("y", self); c.on("y", () => '
            'log.push("added")); };\n'
            'c.on("y", self); c.on("y", () => log.push("tail"));\n'
            'c.emit("y"); c.emit("y"); console.log(log.join());\n'
            'const once2 = () => log.push("o"); c.once("z", once2); c.off("z", once2); '
            'console.log(c.emit("z"));\n'
            'const err = new Emitter();\n'
            'try { err.emit("error", new TypeError("bad")); } catch (x) { console.log(x.name, '
            'x.message); }\n'
            'try { err.emit("error", "oops"); } catch (x) { console.log(x.message); }\n'
            'err.on("error", (x) => console.log("handled", x)); console.log(err.emit("error", '
            '5));\n',
  'hint': 'Храните Map имя → массив записей { fn, once }; для emit копируйте массив.',
  'expected': ['true true 2 2 true',
               'true true false a1,b1,a2',
               'first,a3',
               'first 1',
               'self,tail,tail,added',
               'false',
               'TypeError bad',
               'Unhandled error: oops',
               'handled 5',
               'true']},
 {'id': 'j21-promisify',
  'mode': 'js',
  'title': 'promisify',
  'statement': 'Напишите promisify(fn): функцию, которая принимает те же аргументы, что fn без '
               'последнего callback, и возвращает промис. fn вызывается с this вызывающей стороны '
               'и callback (err, value) последним аргументом: err (истинное значение) → '
               'reject(err), иначе resolve(value) (остальные аргументы callback игнорируются). '
               'Синхронное исключение fn превращается в отклонённый промис. Повторные вызовы '
               'callback игнорируются.',
  'starter': 'function promisify(fn) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const read = promisify(function (name, cb) { setTimeout(() => (name === "bad" ? '
            'cb(new Error("ENOENT " + name)) : cb(null, name.toUpperCase(), "ignored")), 1); });\n'
            'console.log(await read("abc"));\n'
            'try { await read("bad"); } catch (e) { console.log(e.message); }\n'
            'const obj = { prefix: "p:", get: promisify(function (x, cb) { cb(null, this.prefix + '
            'x); }) };\n'
            'console.log(await obj.get("v"));\n'
            'const sync = promisify(() => { throw new RangeError("sync boom"); });\n'
            'try { await sync(); } catch (e) { console.log(e.name, e.message); }\n'
            'const twice = promisify((cb) => { cb(null, 1); cb(null, 2); cb(new Error("late")); '
            '});\n'
            'console.log(await twice());\n'
            'console.log(await promisify((a, b, cb) => cb(0, a + b))(2, 3), await promisify((cb) '
            '=> cb(null))());\n',
  'hint': 'return function (...args) { return new Promise(...) } — обычная функция, чтобы '
          'сохранить this.',
  'expected': ['ABC', 'ENOENT bad', 'p:v', 'RangeError sync boom', '1', '5 undefined']},
 {'id': 'j21-callbackify',
  'mode': 'js',
  'title': 'callbackify',
  'statement': 'Напишите callbackify(fn) для async-функции: возвращает функцию (...args, cb). Она '
               'вызывает fn(...args) (this сохраняется); при успехе вызывает cb(null, значение), '
               "при отказе — cb(err). Если отказ с ложным значением (null, 0, '' и т. п.), cb "
               "получает Error('Promise was rejected with a falsy value') с полем reason = "
               'исходное значение. cb вызывается асинхронно — после завершения текущего '
               'синхронного кода (через process.nextTick). Если последний аргумент не функция — '
               "TypeError('The last argument must be of type function').",
  'starter': 'function callbackify(fn) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const log = [];\n'
            'const f = callbackify(async function (a, b) { return a + b + (this?.k ?? 0); });\n'
            'f(1, 2, (err, v) => log.push(["f", err, v]));\n'
            'log.push("sync-end");\n'
            'await new Promise((r) => setTimeout(r, 5));\n'
            'console.log(JSON.stringify(log));\n'
            'const g = callbackify(async () => { throw new Error("nope"); });\n'
            'g((err, v) => console.log(err.message, v));\n'
            'const h = callbackify(async () => Promise.reject(0));\n'
            'h((err) => console.log(err.message, err.reason, err instanceof Error));\n'
            'const o = { k: 10, f }; o.f(1, 2, (e, v) => console.log("this", v));\n'
            'try { f(1); } catch (e) { console.log(e.name, e.message); }\n'
            'await new Promise((r) => setTimeout(r, 5));\n',
  'hint': 'Promise.then(ok => nextTick(cb, null, ok), err => ...).',
  'expected': ['["sync-end",["f",null,3]]',
               'TypeError The last argument must be of type function',
               'nope undefined',
               'this 13',
               'Promise was rejected with a falsy value 0 true']},
 {'id': 'j21-run-loop',
  'mode': 'js',
  'title': 'Модель цикла событий',
  'statement': 'Напишите runLoop(main) → массив строк журнала. Программа — массив операций: { log: '
               "'A' } (записать), { timeout: ms, cb: [операции] }, { immediate: [операции] }, { "
               'io: [операции] } (обратный вызов завершённого ввода-вывода: выполняется в фазе '
               'опроса), { tick: [операции] } (process.nextTick), { micro: [операции] } '
               '(микрозадача промиса). Правила. Сначала выполняется main, затем «опустошение»: '
               'пока есть тики или микрозадачи — сначала все тики (включая новые), затем все '
               'микрозадачи (включая новые), и снова; такое опустошение происходит после каждого '
               'обратного вызова. Время now = 0; задержка меньше 1 считается за 1; срок таймера = '
               'now (на момент создания) + задержка. Итерация цикла: если нет ни immediate, ни io '
               '— now прыгает к ближайшему сроку (не назад), иначе now += 1. Фазы: таймеры (все со '
               'сроком ≤ now по возрастанию срока, при равенстве — по порядку создания; созданные '
               'в этой фазе не входят), опрос (io, поставленные до начала фазы), проверка '
               '(immediate, поставленные до начала фазы). Цикл идёт, пока есть таймеры, immediate '
               'или io.',
  'starter': 'function runLoop(main) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const L = (s) => ({ log: s });\n'
            'const run = (name, p) => console.log(name + ":", runLoop(p).join(" "));\n'
            'run("classic", [L("A"), { timeout: 0, cb: [L("T")] }, { immediate: [L("I")] }, { '
            'tick: [L("N")] }, { micro: [L("M")] }, L("B")]);\n'
            'run("io", [{ io: [{ timeout: 0, cb: [L("T")] }, { immediate: [L("I")] }, L("io")] '
            '}]);\n'
            'run("order", [{ timeout: 10, cb: [L("X")] }, { timeout: 5, cb: [L("Y")] }, { timeout: '
            '5, cb: [L("Z")] }, { timeout: 0, cb: [L("W")] }]);\n'
            'run("queues", [{ micro: [L("m1"), { tick: [L("t-in-m")] }, { micro: [L("m2")] }] }, { '
            'tick: [L("t1"), { micro: [L("m-in-t")] }, { tick: [L("t2")] }] }, L("main")]);\n'
            'run("timer-cb", [{ timeout: 1, cb: [L("T1"), { timeout: 0, cb: [L("T2")] }, { '
            'immediate: [L("I")] }, { tick: [L("tick")] }] }]);\n'
            'run("two-timers-drain", [{ timeout: 1, cb: [L("a"), { micro: [L("a-micro")] }] }, { '
            'timeout: 1, cb: [L("b"), { tick: [L("b-tick")] }] }]);\n'
            'run("immediate-chain", [{ immediate: [L("i1"), { immediate: [L("i2")] }] }, { '
            'immediate: [L("i1b")] }, { timeout: 0, cb: [L("T")] }]);\n'
            'run("late-timer", [{ io: [{ timeout: 100, cb: [L("late")] }] }, { timeout: 50, cb: '
            '[L("mid")] }, L("start")]);\n'
            'console.log(JSON.stringify(runLoop([])));\n',
  'hint': 'Очереди timers, ios, immediates, ticks, micros; exec(ops) разбирает операции; drain() '
          'после каждого обратного вызова.',
  'expected': ['classic: A B N M T I',
               'io: io I T',
               'order: W Y Z X',
               'queues: main t1 t2 m1 m-in-t m2 t-in-m',
               'timer-cb: T1 tick I T2',
               'two-timers-drain: a a-micro b b-tick',
               'immediate-chain: T i1 i1b i2',
               'late-timer: start mid late',
               '[]']},
 {'id': 'j21-timer-list',
  'mode': 'js',
  'title': 'Таймеры и unref',
  'statement': 'Напишите createTimers() → { setTimeout(name, delay, opts?), clear(id), run() }. '
               'setTimeout возвращает числовой id (с 1); opts.unref === true делает таймер '
               '«неудерживающим» цикл. Время виртуальное, начинается с 0; delay < 1 считается за '
               '1; срок = delay (все таймеры создаются до run). run() выполняет таймеры в порядке '
               '(срок, порядок создания) и возвращает { order, now }: order — имена выполненных '
               'таймеров, now — срок последнего выполненного (0, если ничего не выполнено). Цикл '
               'завершается, как только не осталось ни одного неотменённого таймера без unref '
               '(оставшиеся unref-таймеры не выполняются). clear(id) отменяет таймер любого вида.',
  'starter': 'function createTimers() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = createTimers();\n'
            't.setTimeout("a", 30); t.setTimeout("heartbeat", 10, { unref: true }); '
            't.setTimeout("b", 20);\n'
            't.setTimeout("tail-unref", 100, { unref: true }); t.setTimeout("zero", 0); '
            't.setTimeout("a2", 30);\n'
            'console.log(JSON.stringify(t.run()));\n'
            'const u = createTimers(); u.setTimeout("only-unref", 5, { unref: true }); '
            'console.log(JSON.stringify(u.run()));\n'
            'const c = createTimers(); const x = c.setTimeout("x", 5); const y = c.setTimeout("y", '
            '7, { unref: true }); c.setTimeout("z", 9); c.clear(x); c.clear(y);\n'
            'console.log(x, y, JSON.stringify(c.run()));\n'
            'const e = createTimers(); console.log(JSON.stringify(e.run()));\n'
            'const m = createTimers(); m.setTimeout("late-ref", 50); m.setTimeout("early-unref", '
            '1, { unref: true }); m.setTimeout("mid-unref", 49, { unref: true }); '
            'console.log(JSON.stringify(m.run()));\n',
  'hint': 'Сортируйте по (due, seq); перед каждым шагом проверяйте, остался ли хоть один '
          'ref-таймер.',
  'expected': ['{"order":["zero","heartbeat","b","a","a2"],"now":30}',
               '{"order":[],"now":0}',
               '1 2 {"order":["z"],"now":9}',
               '{"order":[],"now":0}',
               '{"order":["early-unref","mid-unref","late-ref"],"now":50}']},
 {'id': 'j21-threadpool',
  'mode': 'js',
  'title': 'Пул потоков libuv',
  'statement': 'Напишите simulatePool(size, jobs): jobs — [{ name, duration }], все поставлены в '
               'очередь в момент 0 в указанном порядке. Каждое задание берёт поток, который '
               'освобождается раньше всех (при равенстве — с меньшим номером, потоки нумеруются с '
               '0). Верните { schedule, makespan }: schedule — для каждого задания в исходном '
               'порядке { name, worker, start, end }, makespan — момент завершения последнего (0 '
               "для пустого списка). size меньше 1 — Error('Pool size must be >= 1').",
  'starter': 'function simulatePool(size, jobs) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const jobs = [["fs.read", 30], ["dns", 10], ["zlib", 50], ["crypto", 20], '
            '["fs.write", 10], ["dns2", 5]].map(([name, duration]) => ({ name, duration }));\n'
            'for (const n of [1, 2, 4, 8]) { const r = simulatePool(n, jobs); console.log(n, '
            'r.makespan, r.schedule.map((s) => '
            '`${s.name}@${s.worker}[${s.start}-${s.end}]`).join(" ")); }\n'
            'console.log(JSON.stringify(simulatePool(3, [])));\n'
            'try { simulatePool(0, jobs); } catch (e) { console.log(e.message); }\n',
  'hint': 'Массив free[i] — время освобождения потока; для каждого задания найдите минимум.',
  'expected': ['1 125 fs.read@0[0-30] dns@0[30-40] zlib@0[40-90] crypto@0[90-110] '
               'fs.write@0[110-120] dns2@0[120-125]',
               '2 65 fs.read@0[0-30] dns@1[0-10] zlib@1[10-60] crypto@0[30-50] fs.write@0[50-60] '
               'dns2@0[60-65]',
               '4 50 fs.read@0[0-30] dns@1[0-10] zlib@2[0-50] crypto@3[0-20] fs.write@1[10-20] '
               'dns2@1[20-25]',
               '8 50 fs.read@0[0-30] dns@1[0-10] zlib@2[0-50] crypto@3[0-20] fs.write@4[0-10] '
               'dns2@5[0-5]',
               '{"schedule":[],"makespan":0}',
               'Pool size must be >= 1']},
 {'id': 'j21-cjs-resolve',
  'mode': 'js',
  'title': 'Разрешение require()',
  'statement': 'Функция normalize(path), dirname(path) уже есть. Напишите resolve(request, '
               'fromDir, files): files — объект { абсолютный путь: содержимое }. Правила CommonJS. '
               "1) Встроенные: имя из ['fs','path','http','os','events','util'] или начинающееся с "
               '«node:» → вернуть «node:» + имя (без повторного префикса). 2) Начинается с «./», '
               "«../» или «/» — путь = normalize(fromDir + '/' + request) (для «/…» — "
               'normalize(request)); 3) иначе (голое имя, возможно с подпутём «pkg/sub») — перебор '
               "каталогов от fromDir вверх до корня: кандидат = каталог + '/node_modules/' + "
               "request. Для кандидата: точный файл → иначе кандидат + '.js', '.json' → иначе как "
               'каталог: если есть кандидат/package.json (JSON с полем main) — попробовать main '
               'как файл (точный, .js, .json), затем main/index.js; иначе (или если не нашлось) '
               'кандидат/index.js, кандидат/index.json. Первое найденное возвращается. Не найдено '
               "— Error(`Cannot find module '${request}'`).",
  'starter': '// Готово: нормализация пути (не изменяйте)\n'
             'function normalize(p) {\n'
             '  const out = [];\n'
             '  for (const s of p.split("/")) {\n'
             '    if (s === "" || s === ".") continue;\n'
             '    if (s === "..") out.pop(); else out.push(s);\n'
             '  }\n'
             '  return "/" + out.join("/");\n'
             '}\n'
             'const dirname = (p) => normalize(p.slice(0, p.lastIndexOf("/")) || "/");\n'
             'function resolve(request, fromDir, files) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const files = {\n'
            '  "/app/main.js": "", "/app/util.js": "", "/app/data.json": "{}", '
            '"/app/lib/index.js": "", "/app/lib/extra.js": "",\n'
            '  "/app/pkg/package.json": \'{"main":"./dist/entry"}\', "/app/pkg/dist/entry.js": "", '
            '"/app/pkg/index.js": "",\n'
            '  "/app/broken/package.json": \'{"main":"missing.js"}\', "/app/broken/index.js": "",\n'
            '  "/app/node_modules/left/package.json": \'{"main":"lib/main.js"}\', '
            '"/app/node_modules/left/lib/main.js": "", "/app/node_modules/left/sub.js": "",\n'
            '  "/node_modules/top/index.js": "", "/app/src/node_modules/inner/index.js": "", '
            '"/app/src/page.js": "",\n'
            '};\n'
            'const t = (r, d = "/app") => { try { console.log(r, "→", resolve(r, d, files)); } '
            'catch (e) { console.log(r, "!", e.message); } };\n'
            't("./util"); t("./util.js"); t("./data"); t("./lib"); t("./lib/extra"); t("./pkg"); '
            't("./broken"); t("../app/util", "/app/lib"); t("/app/main"); t("./nope");\n'
            't("left"); t("left/sub"); t("left/lib/main"); t("top"); t("top", "/app/src/deep"); '
            't("inner", "/app/src"); t("inner", "/app"); t("fs"); t("node:test"); t("node:fs"); '
            't("missing-pkg");\n',
  'hint': 'tryFile(p) и tryDir(p); для голых имён — цикл по цепочке предков fromDir.',
  'expected': ['./util → /app/util.js',
               './util.js → /app/util.js',
               './data → /app/data.json',
               './lib → /app/lib/index.js',
               './lib/extra → /app/lib/extra.js',
               './pkg → /app/pkg/dist/entry.js',
               './broken → /app/broken/index.js',
               "../app/util ! Cannot find module '../app/util'",
               '/app/main → /app/main.js',
               "./nope ! Cannot find module './nope'",
               'left → /app/node_modules/left/lib/main.js',
               'left/sub → /app/node_modules/left/sub.js',
               'left/lib/main → /app/node_modules/left/lib/main.js',
               'top → /node_modules/top/index.js',
               'top → /node_modules/top/index.js',
               'inner → /app/src/node_modules/inner/index.js',
               "inner ! Cannot find module 'inner'",
               'fs → node:fs',
               'node:test → node:test',
               'node:fs → node:fs',
               "missing-pkg ! Cannot find module 'missing-pkg'"]},
 {'id': 'j21-require-cache',
  'mode': 'js',
  'title': 'require с кэшем и циклами',
  'statement': 'Функции normalize/dirname уже есть. Напишите createRequire(modules): modules — { '
               'абсолютный путь: функция(exports, require, module) }. Верните функцию '
               'require(path), которая вызывается с абсолютным путём. Внутри модуля require '
               "получает: «./x» или «../x» → путь = normalize(dirname(текущий) + '/' + x), если "
               "ключа нет — добавляется «.js»; иное — Error(`Cannot find module '${spec}'`) также "
               'если ключа нет. Модуль выполняется один раз: объект module = { exports: {}, '
               'loaded: false, id: path }; результат кэшируется в момент начала выполнения '
               '(поэтому циклическая зависимость получает частично заполненный exports); после '
               'завершения loaded = true. Возвращается module.exports (в том числе после '
               'переприсвоения). Если модуль бросил исключение — запись удаляется из кэша '
               '(следующий require выполнит его заново), исключение пробрасывается. Функцию '
               'require можно вызвать у возвращённого require как require.cache (объект путь → '
               'module).',
  'starter': '// Готово: нормализация пути (не изменяйте)\n'
             'function normalize(p) {\n'
             '  const out = [];\n'
             '  for (const s of p.split("/")) {\n'
             '    if (s === "" || s === ".") continue;\n'
             '    if (s === "..") out.pop(); else out.push(s);\n'
             '  }\n'
             '  return "/" + out.join("/");\n'
             '}\n'
             'const dirname = (p) => normalize(p.slice(0, p.lastIndexOf("/")) || "/");\n'
             'function createRequire(modules) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const log = [];\n'
            'const modules = {\n'
            '  "/app/a.js": (exports, require, module) => { log.push("a start"); exports.early = '
            '1; const b = require("./b"); log.push("a sees b.done=" + b.done); exports.late = 2; '
            'log.push("a end"); },\n'
            '  "/app/b.js": (exports, require, module) => { log.push("b start"); const a = '
            'require("./a"); log.push("b sees a=" + JSON.stringify(a)); exports.done = true; },\n'
            '  "/app/counter.js": (exports, require, module) => { log.push("counter run"); let n = '
            '0; module.exports = { inc: () => ++n }; },\n'
            '  "/app/use1.js": (exports, require, module) => { exports.v = '
            'require("./counter").inc(); },\n'
            '  "/app/use2.js": (exports, require, module) => { exports.v = '
            'require("./counter").inc(); },\n'
            '  "/app/lib/flaky.js": (exports, require, module) => { log.push("flaky run"); if '
            '(!globalThis.__ok) throw new Error("not ready"); exports.ok = 1; },\n'
            '  "/app/lib/rel.js": (exports, require, module) => { exports.c = '
            'require("../counter") === require("/app/counter.js"); },\n'
            '  "/app/bad.js": (exports, require) => { require("./ghost"); },\n'
            '};\n'
            'const require = createRequire(modules);\n'
            'const a = require("/app/a.js"); console.log(JSON.stringify(a), log.join(" | "));\n'
            'log.length = 0;\n'
            'console.log(require("/app/use1.js").v, require("/app/use2.js").v, log.join());\n'
            'try { require("/app/lib/flaky.js"); } catch (e) { console.log(e.message); }\n'
            'try { require("/app/lib/flaky.js"); } catch (e) { console.log(e.message); }\n'
            'globalThis.__ok = true; console.log(JSON.stringify(require("/app/lib/flaky.js")), '
            'log.filter((x) => x === "flaky run").length);\n'
            'console.log(require("/app/lib/rel.js").c);\n'
            'try { require("/app/bad.js"); } catch (e) { console.log(e.message); }\n'
            'try { require("/app/none.js"); } catch (e) { console.log(e.message); }\n'
            'console.log(Object.keys(require.cache).sort().join(), '
            'require.cache["/app/a.js"].loaded, require.cache["/app/counter.js"].id);\n',
  'hint': 'Фабрика makeRequire(parentPath); кэш — общий объект cache.',
  'expected': ['{"early":1,"late":2} a start | b start | b sees a={"early":1} | a sees b.done=true '
               '| a end',
               '1 2 counter run',
               'not ready',
               'not ready',
               '{"ok":1} 3',
               'true',
               "Cannot find module './ghost'",
               "Cannot find module '/app/none.js'",
               '/app/a.js,/app/b.js,/app/counter.js,/app/lib/flaky.js,/app/lib/rel.js,/app/use1.js,/app/use2.js '
               'true /app/counter.js']},
 {'id': 'j21-exports-map',
  'mode': 'js',
  'title': 'Поле exports пакета',
  'statement': 'Напишите resolveExports(exportsField, subpath, conditions). exportsField — строка '
               "(сокращение для { '.': строка }), объект «подпути» (ключи начинаются с «.»), либо "
               "объект «условий» (ключи не начинаются с «.»; равносилен { '.': объект }). subpath "
               '— «.» или «./что-то». conditions — массив активных условий (например '
               "['node','import']); условие 'default' активно всегда. Цель — строка, объект "
               'условий (берётся первое по порядку ключей условие, которое активно; результат '
               'разрешается рекурсивно), массив (первая цель, которая разрешилась не в null) или '
               'null (закрыто). Шаблоны: ключ с одной «*» («./features/*») подходит подпутям с '
               'этим префиксом и суффиксом, «*» в цели заменяется на найденный фрагмент (во всех '
               'местах); при нескольких шаблонах побеждает с самым длинным префиксом; точный ключ '
               'приоритетнее шаблона. Не найдено или цель null — Error(`Package subpath '
               '\'${subpath}\' is not defined by "exports"`).',
  'starter': 'function resolveExports(exportsField, subpath, conditions) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (f, s, c = ["node", "import"]) => { try { console.log(JSON.stringify(s), '
            '"→", resolveExports(f, s, c)); } catch (e) { console.log(JSON.stringify(s), "!", '
            'e.message); } };\n'
            't("./main.js", "."); t("./main.js", "./other");\n'
            'const cond = { import: "./esm.mjs", require: "./cjs.cjs", default: "./fallback.js" '
            '};\n'
            't(cond, "."); t(cond, ".", ["require"]); t(cond, ".", ["browser"]);\n'
            'const map = {\n'
            '  ".": { node: { import: "./node/index.mjs", require: "./node/index.cjs" }, default: '
            '"./browser.js" },\n'
            '  "./utils": "./src/utils.js", "./features/*": "./src/features/*.js", '
            '"./features/internal/*": null, "./features/beta/*": ["./nope", "./src/beta/*.js"],\n'
            '  "./data/*.json": "./json/*.json", "./package.json": "./package.json", "./private": '
            'null, "./multi/*": "./src/*/x/*.js",\n'
            '};\n'
            't(map, "."); t(map, ".", ["browser"]); t(map, ".", ["node", "require"]); t(map, '
            '"./utils"); t(map, "./features/a"); t(map, "./features/a/b"); t(map, '
            '"./features/internal/secret");\n'
            't(map, "./features/beta/z"); t(map, "./data/users.json"); t(map, "./data/users.txt"); '
            't(map, "./private"); t(map, "./missing"); t(map, "./package.json"); t(map, '
            '"./multi/q");\n'
            't({ "./x": "./x.js" }, "."); t({ ".": ["./a.js", "./b.js"] }, "."); t({ ".": [null, '
            '"./b.js"] }, ".");\n',
  'hint': 'Функция target(t, star) возвращает строку или null; подпути ищите точным ключом, затем '
          'шаблоном.',
  'expected': ['"." → ./main.js',
               '"./other" ! Package subpath \'./other\' is not defined by "exports"',
               '"." → ./esm.mjs',
               '"." → ./cjs.cjs',
               '"." → ./fallback.js',
               '"." → ./node/index.mjs',
               '"." → ./browser.js',
               '"." → ./node/index.cjs',
               '"./utils" → ./src/utils.js',
               '"./features/a" → ./src/features/a.js',
               '"./features/a/b" → ./src/features/a/b.js',
               '"./features/internal/secret" ! Package subpath \'./features/internal/secret\' is '
               'not defined by "exports"',
               '"./features/beta/z" → ./nope',
               '"./data/users.json" → ./json/users.json',
               '"./data/users.txt" ! Package subpath \'./data/users.txt\' is not defined by '
               '"exports"',
               '"./private" ! Package subpath \'./private\' is not defined by "exports"',
               '"./missing" ! Package subpath \'./missing\' is not defined by "exports"',
               '"./package.json" → ./package.json',
               '"./multi/q" → ./src/q/x/q.js',
               '"." ! Package subpath \'.\' is not defined by "exports"',
               '"." → ./a.js',
               '"." → ./b.js']},
 {'id': 'j21-imports-map',
  'mode': 'js',
  'title': 'Поле imports пакета',
  'statement': 'Функция resolveTarget(target, conditions, star) → строка | null уже есть (строка / '
               'объект условий / массив / null, замена «*»). Напишите resolveImports(imports, '
               'specifier, conditions). specifier обязан начинаться с «#» и не быть «#» или «#/…» '
               "— иначе Error(`Invalid package import specifier '${specifier}'`). Сначала точный "
               'ключ, затем шаблон с одной «*» (побеждает самый длинный префикс; сам префикс — '
               'включая «#»). Цель, разрешившаяся в null, или отсутствие совпадения — '
               "Error(`Package import specifier '${specifier}' is not defined`). Если цель — голое "
               "имя пакета (не начинается с «./», «../» или «/»), результат — { type: 'package', "
               "name: цель }, иначе { type: 'file', path: цель }.",
  'starter': '// Готово: разрешение цели (не изменяйте)\n'
             'function resolveTarget(t, conditions, star) {\n'
             '  if (t === null || t === undefined) return null;\n'
             '  if (typeof t === "string") return star === undefined ? t : '
             't.split("*").join(star);\n'
             '  if (Array.isArray(t)) { for (const x of t) { const r = resolveTarget(x, '
             'conditions, star); if (r !== null) return r; } return null; }\n'
             '  for (const [k, v] of Object.entries(t)) if (k === "default" || '
             'conditions.includes(k)) return resolveTarget(v, conditions, star);\n'
             '  return null;\n'
             '}\n'
             'function resolveImports(imports, specifier, conditions) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const imports = { "#config": { node: "./src/config.node.js", default: '
            '"./src/config.js" }, "#utils/*": "./src/utils/*.js", "#utils/internal/*": null, '
            '"#dep": { node: "lodash", default: "./vendor/lodash.js" }, "#db/*": ["./nope", '
            '"./db/*.mjs"] };\n'
            'const t = (s, c = ["node"]) => { try { console.log(s, "→", '
            'JSON.stringify(resolveImports(imports, s, c))); } catch (e) { console.log(s, "!", '
            'e.message); } };\n'
            't("#config"); t("#config", ["browser"]); t("#utils/format"); t("#utils/a/b"); '
            't("#utils/internal/x"); t("#dep"); t("#dep", []); t("#db/main"); t("#missing"); '
            't("lodash"); t("#"); t("#/x"); t("");\n',
  'hint': 'Используйте resolveTarget; шаблон ищите перебором ключей с «*».',
  'expected': ['#config → {"type":"file","path":"./src/config.node.js"}',
               '#config → {"type":"file","path":"./src/config.js"}',
               '#utils/format → {"type":"file","path":"./src/utils/format.js"}',
               '#utils/a/b → {"type":"file","path":"./src/utils/a/b.js"}',
               "#utils/internal/x ! Package import specifier '#utils/internal/x' is not defined",
               '#dep → {"type":"package","name":"lodash"}',
               '#dep → {"type":"file","path":"./vendor/lodash.js"}',
               '#db/main → {"type":"file","path":"./nope"}',
               "#missing ! Package import specifier '#missing' is not defined",
               "lodash ! Invalid package import specifier 'lodash'",
               "# ! Invalid package import specifier '#'",
               "#/x ! Invalid package import specifier '#/x'",
               " ! Invalid package import specifier ''"]},
 {'id': 'j21-exit-code',
  'mode': 'js',
  'title': 'Коды завершения процесса',
  'statement': 'Таблица SIGNALS (имя → номер) уже есть. Напишите exitCode(event) → число и '
               "describeExit(code) → строка. Событие: { type: 'normal' } → 0; { type: 'exit', code "
               "} → code & 255; { type: 'signal', name } → 128 + номер (неизвестное имя — "
               "Error(`Unknown signal: ${name}`)); { type: 'uncaught' } → 1; { type: 'rejection', "
               "mode } — mode 'warn' → 0, иначе ('throw' по умолчанию и 'strict') → 1; { type: "
               "'internal-handler-error' } → 7; { type: 'invalid-argument' } → 9; другой тип — "
               "Error(`Unknown event: ${type}`). describeExit(code): 0 → 'success'; 1 → 'uncaught "
               "exception'; 7 → 'internal exception handler failure'; 9 → 'invalid argument'; "
               'число в диапазоне 129…159, соответствующее 128 + известный сигнал, → `terminated '
               'by ${имя сигнала}`; остальное → `exit code ${code}`.',
  'starter': '// Готово: номера сигналов Linux (не изменяйте)\n'
             'const SIGNALS = { SIGHUP: 1, SIGINT: 2, SIGQUIT: 3, SIGABRT: 6, SIGKILL: 9, SIGUSR1: '
             '10, SIGSEGV: 11, SIGUSR2: 12, SIGPIPE: 13, SIGALRM: 14, SIGTERM: 15 };\n'
             'function exitCode(event) {\n'
             '}\n'
             'function describeExit(code) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const evs = [{ type: "normal" }, { type: "exit", code: 3 }, { type: "exit", code: 256 '
            '}, { type: "exit", code: -1 }, { type: "signal", name: "SIGINT" }, { type: "signal", '
            'name: "SIGTERM" }, { type: "signal", name: "SIGKILL" }, { type: "signal", name: '
            '"SIGSEGV" }, { type: "uncaught" }, { type: "rejection" }, { type: "rejection", mode: '
            '"warn" }, { type: "rejection", mode: "strict" }, { type: "internal-handler-error" }, '
            '{ type: "invalid-argument" }, { type: "signal", name: "SIGFOO" }, { type: "weird" '
            '}];\n'
            'for (const e of evs) { try { const c = exitCode(e); console.log(JSON.stringify(e), c, '
            'describeExit(c)); } catch (x) { console.log(JSON.stringify(e), "!", x.message); } }\n'
            'console.log([0, 1, 2, 7, 9, 130, 137, 143, 128, 129, 160, 255, '
            '42].map(describeExit).join(" | "));\n',
  'hint': 'Обратная таблица номер → имя для describeExit.',
  'expected': ['{"type":"normal"} 0 success',
               '{"type":"exit","code":3} 3 exit code 3',
               '{"type":"exit","code":256} 0 success',
               '{"type":"exit","code":-1} 255 exit code 255',
               '{"type":"signal","name":"SIGINT"} 130 terminated by SIGINT',
               '{"type":"signal","name":"SIGTERM"} 143 terminated by SIGTERM',
               '{"type":"signal","name":"SIGKILL"} 137 terminated by SIGKILL',
               '{"type":"signal","name":"SIGSEGV"} 139 terminated by SIGSEGV',
               '{"type":"uncaught"} 1 uncaught exception',
               '{"type":"rejection"} 1 uncaught exception',
               '{"type":"rejection","mode":"warn"} 0 success',
               '{"type":"rejection","mode":"strict"} 1 uncaught exception',
               '{"type":"internal-handler-error"} 7 internal exception handler failure',
               '{"type":"invalid-argument"} 9 invalid argument',
               '{"type":"signal","name":"SIGFOO"} ! Unknown signal: SIGFOO',
               '{"type":"weird"} ! Unknown event: weird',
               'success | uncaught exception | exit code 2 | internal exception handler failure | '
               'invalid argument | terminated by SIGINT | terminated by SIGKILL | terminated by '
               'SIGTERM | exit code 128 | terminated by SIGHUP | exit code 160 | exit code 255 | '
               'exit code 42']},
 {'id': 'j21-parse-args',
  'mode': 'js',
  'title': 'Разбор аргументов командной строки',
  'statement': 'Напишите parseArgs(argv, options) → { values, positionals }. options — { имя: { '
               "type: 'boolean' | 'string', short?: 'x', multiple?: bool, default? } }. Формы: "
               '«--имя», «--имя=значение», «--имя значение» (для string следующий элемент — '
               'значение, даже если начинается с «-»? нет: если следующий элемент отсутствует — '
               'ошибка; если начинается с «-» — тоже ошибка), «-x», «-x значение» (string), '
               'склейка булевых «-abc» (каждая буква — опция с short; последняя может быть string '
               'и взять следующий аргумент), «--» завершает опции (остальное — позиционные), всё '
               'без «-» — позиционные. Неизвестная опция — Error(`Unknown option '
               "'${как_написано}'`) (например '--zzz' или '-q'); string без значения — "
               "Error(`Option '--${имя} <value>' argument missing`); boolean с «=значение» — "
               "Error(`Option '--${имя}' does not take an argument`). multiple: значения копятся в "
               'массив; без multiple повтор перезаписывает. В values попадают только заданные '
               'опции и опции с default (boolean по умолчанию — без записи).',
  'starter': 'function parseArgs(argv, options) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const opts = { verbose: { type: "boolean", short: "v" }, quiet: { type: "boolean", '
            'short: "q" }, out: { type: "string", short: "o" }, tag: { type: "string", short: "t", '
            'multiple: true }, level: { type: "string", default: "info" } };\n'
            'const t = (...argv) => { try { console.log(JSON.stringify(argv), "→", '
            'JSON.stringify(parseArgs(argv, opts))); } catch (e) { '
            'console.log(JSON.stringify(argv), "!", e.message); } };\n'
            't(); t("a", "b"); t("--verbose", "file"); t("--out=x.txt", "--level", "debug"); '
            't("--out", "y"); t("-o", "z"); t("-vq"); t("-vo", "w"); t("--tag", "a", "--tag=b", '
            '"-t", "c"); t("--out", "1", "--out", "2");\n'
            't("--", "--verbose", "x"); t("a", "--", "-v"); t("--zzz"); t("-x"); t("--out"); '
            't("-o"); t("--out", "-v"); t("--verbose=yes"); t("-vx"); t("-"); t("--level=");\n',
  'hint': 'Карта short → имя; цикл с индексом; отдельная функция set(name, value).',
  'expected': ['[] → {"values":{"level":"info"},"positionals":[]}',
               '["a","b"] → {"values":{"level":"info"},"positionals":["a","b"]}',
               '["--verbose","file"] → '
               '{"values":{"level":"info","verbose":true},"positionals":["file"]}',
               '["--out=x.txt","--level","debug"] → '
               '{"values":{"level":"debug","out":"x.txt"},"positionals":[]}',
               '["--out","y"] → {"values":{"level":"info","out":"y"},"positionals":[]}',
               '["-o","z"] → {"values":{"level":"info","out":"z"},"positionals":[]}',
               '["-vq"] → {"values":{"level":"info","verbose":true,"quiet":true},"positionals":[]}',
               '["-vo","w"] → '
               '{"values":{"level":"info","verbose":true,"out":"w"},"positionals":[]}',
               '["--tag","a","--tag=b","-t","c"] → '
               '{"values":{"level":"info","tag":["a","b","c"]},"positionals":[]}',
               '["--out","1","--out","2"] → {"values":{"level":"info","out":"2"},"positionals":[]}',
               '["--","--verbose","x"] → '
               '{"values":{"level":"info"},"positionals":["--verbose","x"]}',
               '["a","--","-v"] → {"values":{"level":"info"},"positionals":["a","-v"]}',
               '["--zzz"] ! Unknown option \'--zzz\'',
               '["-x"] ! Unknown option \'-x\'',
               '["--out"] ! Option \'--out <value>\' argument missing',
               '["-o"] ! Option \'--out <value>\' argument missing',
               '["--out","-v"] ! Option \'--out <value>\' argument missing',
               '["--verbose=yes"] ! Option \'--verbose\' does not take an argument',
               '["-vx"] ! Unknown option \'-x\'',
               '["-"] → {"values":{"level":"info"},"positionals":["-"]}',
               '["--level="] → {"values":{"level":""},"positionals":[]}']},
 {'id': 'j21-graceful',
  'mode': 'js',
  'title': 'Корректное завершение сервиса',
  'statement': 'Напишите async gracefulShutdown({ stopAccepting, pending, closers, timeoutMs, '
               "pollMs = 5 }) → { code, forced, log }. Порядок: log.push('stop'); вызвать "
               'stopAccepting() (может быть async); затем опрашивать pending() (число '
               'обрабатываемых запросов) каждые pollMs мс, пока не станет 0 или не пройдёт '
               "timeoutMs мс (Date.now) — при таймауте forced = true и log.push('timeout'), иначе "
               "log.push('drained'). Затем по порядку await closers: [{ name, close }]: "
               "log.push('close:' + name); исключение закрывателя — log.push('error:' + name), и "
               'работа продолжается. Результат: forced или были ошибки → code 1, иначе 0. Опрос не '
               'должен ждать после того, как pending() уже 0.',
  'starter': 'async function gracefulShutdown(opts) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const sleep = (ms) => new Promise((r) => setTimeout(r, ms));\n'
            'let busy = 3; const t0 = Date.now();\n'
            'const drain = setInterval(() => { busy = Math.max(0, busy - 1); }, 10);\n'
            'const r1 = await gracefulShutdown({ stopAccepting: async () => { await sleep(1); }, '
            'pending: () => busy, closers: [{ name: "db", close: async () => { await sleep(1); } '
            '}, { name: "cache", close() {} }], timeoutMs: 500 });\n'
            'clearInterval(drain);\n'
            'console.log(JSON.stringify(r1), Date.now() - t0 < 300);\n'
            'const r2 = await gracefulShutdown({ stopAccepting() {}, pending: () => 5, closers: [{ '
            'name: "db", close() {} }], timeoutMs: 40, pollMs: 5 });\n'
            'console.log(JSON.stringify(r2));\n'
            'const r3 = await gracefulShutdown({ stopAccepting() {}, pending: () => 0, closers: [{ '
            'name: "a", close() { throw new Error("x"); } }, { name: "b", close() {} }], '
            'timeoutMs: 10 });\n'
            'console.log(JSON.stringify(r3));\n'
            'const start = Date.now(); const r4 = await gracefulShutdown({ stopAccepting() {}, '
            'pending: () => 0, closers: [], timeoutMs: 1000, pollMs: 200 }); '
            'console.log(JSON.stringify(r4), Date.now() - start < 100);\n',
  'hint': 'Цикл: while (pending() > 0) { if (прошло ≥ timeout) {...; break;} await sleep(pollMs) '
          '}.',
  'expected': ['{"code":0,"forced":false,"log":["stop","drained","close:db","close:cache"]} true',
               '{"code":1,"forced":true,"log":["stop","timeout","close:db"]}',
               '{"code":1,"forced":false,"log":["stop","drained","close:a","error:a","close:b"]}',
               '{"code":0,"forced":false,"log":["stop","drained"]} true']},
 {'id': 'j21-backoff',
  'mode': 'js',
  'title': 'Перезапуск процесса с задержкой',
  'statement': 'Напишите createBackoff({ base = 100, factor = 2, max = 5000, resetAfter = 10000, '
               'maxAttempts = Infinity } = {}) → { onStart(now), onExit(now) }. onStart запоминает '
               'время запуска. onExit(now) вызывается при падении процесса: если процесс '
               'проработал не меньше resetAfter мс (now − время последнего запуска), счётчик '
               'попыток сбрасывается в 0. Затем, если попыток уже maxAttempts — вернуть null '
               '(сдаёмся); иначе вернуть задержку min(max, base · factor^попытки) и увеличить '
               'счётчик. Если onStart не вызывали, время запуска считается равным 0.',
  'starter': 'function createBackoff(opts = {}) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const b = createBackoff();\n'
            'let t = 0; const out = [];\n'
            'for (let i = 0; i < 9; i++) { b.onStart(t); t += 50; out.push(b.onExit(t)); }\n'
            'console.log(out.join(" "));\n'
            'b.onStart(t); t += 20000; console.log(b.onExit(t));\n'
            'b.onStart(t); t += 10; console.log(b.onExit(t), b.onExit(t));\n'
            'const c = createBackoff({ base: 10, factor: 3, max: 100, maxAttempts: 4, resetAfter: '
            '1000 });\n'
            'const r = []; for (let i = 0; i < 6; i++) { c.onStart(i * 10); r.push(c.onExit(i * 10 '
            '+ 1)); } console.log(JSON.stringify(r));\n'
            'c.onStart(100); console.log(c.onExit(5000), c.onExit(5001));\n'
            'const d = createBackoff({ resetAfter: 100 }); console.log(d.onExit(99), '
            'd.onExit(100), d.onExit(150));\n',
  'hint': 'Состояние: attempts, startedAt.',
  'expected': ['100 200 400 800 1600 3200 5000 5000 5000',
               '100',
               '200 400',
               '[10,30,90,100,null,null]',
               '10 10',
               '100 100 100']},
 {'id': 'j21-als',
  'mode': 'js',
  'title': 'Контекст запроса через AsyncLocalStorage',
  'statement': 'Напишите createRequestContext() → { run(id, fn), log(message), current() } на '
               'основе AsyncLocalStorage из node:async_hooks. run(id, fn) выполняет fn (может быть '
               'async) в контексте с идентификатором запроса и возвращает её результат. '
               'log(message) возвращает строку `[${id}] ${message}` внутри контекста и `[-] '
               '${message}` вне его. current() — id или undefined. Контекст должен сохраняться '
               'через await, setTimeout и промисы; вложенный run перекрывает id только внутри '
               'себя.',
  'starter': 'import { AsyncLocalStorage } from "node:async_hooks";\n'
             'function createRequestContext() {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const ctx = createRequestContext();\n'
            'const sleep = (ms) => new Promise((r) => setTimeout(r, ms));\n'
            'const out = [];\n'
            'async function handler(id, delay) {\n'
            '  out.push(ctx.log("start"));\n'
            '  await sleep(delay);\n'
            '  out.push(ctx.log("after sleep"));\n'
            '  await new Promise((r) => setTimeout(r, 1)); await null;\n'
            '  out.push(ctx.log("end"));\n'
            '  return id + ":" + ctx.current();\n'
            '}\n'
            'const results = await Promise.all([ctx.run("A", () => handler("A", 12)), ctx.run("B", '
            '() => handler("B", 3)), ctx.run("C", () => handler("C", 7))]);\n'
            'console.log(results.join(" "));\n'
            'console.log(out.sort().join(" | "));\n'
            'console.log(ctx.log("outside"), ctx.current());\n'
            'await ctx.run("outer", async () => { console.log(ctx.log("x")); await '
            'ctx.run("inner", async () => { await sleep(1); console.log(ctx.log("y")); }); '
            'console.log(ctx.log("z"), ctx.current()); });\n'
            'console.log(ctx.run("sync", () => ctx.current()), ctx.current());\n',
  'hint': 'const als = new AsyncLocalStorage(); run → als.run(id, fn); current → als.getStore().',
  'expected': ['A:A B:B C:C',
               '[A] after sleep | [A] end | [A] start | [B] after sleep | [B] end | [B] start | '
               '[C] after sleep | [C] end | [C] start',
               '[-] outside undefined',
               '[outer] x',
               '[inner] y',
               '[outer] z outer',
               'sync undefined']},
 {'id': 'j21-parse-stack',
  'mode': 'js',
  'title': 'Разбор стека ошибки',
  'statement': 'Напишите parseStack(stack) → массив кадров { fn, file, line, col, async, isNew }. '
               'Строки кадров начинаются (после пробелов) с «at »; остальные строки (сообщение, '
               'пустые) пропускаются. Форматы: «at имя (файл:строка:столбец)», «at '
               'файл:строка:столбец» (fn = null), «at async имя (…)» (async = true), «at new Класс '
               "(…)» (isNew = true, fn = 'Класс'; префиксы «async» и «new» не входят в fn). Для "
               'имени вида «Class.method [as alias]» fn берётся целиком. Файл — всё до последних '
               'двух «:число» (в нём могут быть «file:///…», «node:internal/x», Windows-диск '
               '«C:\\…»); line и col — числа. Кадр, не подходящий под формат (например «at '
               '<anonymous>»), пропускается.',
  'starter': 'function parseStack(stack) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const stack = `Error: boom: with at word\n'
            '    at readConfig (file:///app/src/config.mjs:12:9)\n'
            '    at async Server.start (file:///app/src/server.mjs:40:5)\n'
            '    at new Router (/app/src/router.js:7:3)\n'
            '    at Object.<anonymous> (/app/index.js:3:1)\n'
            '    at file:///app/src/anon.mjs:99:12\n'
            '    at Array.map (<anonymous>)\n'
            '    at <anonymous>\n'
            '    at Class.method [as alias] (C:\\\\proj\\\\a.js:5:7)\n'
            '    at process.processTicksAndRejections (node:internal/process/task_queues:95:5)\n'
            '    at async file:///app/async-anon.mjs:1:2\n'
            '\n'
            'garbage line`;\n'
            'for (const f of parseStack(stack)) console.log(JSON.stringify(f));\n'
            'console.log(parseStack("").length, parseStack("Error: x\\n    at bad '
            '(no-position)").length);\n',
  'hint': 'Регулярное выражение /^\\s*at (?:(async|new) )?(?:(.+?) \\()?(.+):(\\d+):(\\d+)\\)?$/.',
  'expected': ['{"fn":"readConfig","file":"file:///app/src/config.mjs","line":12,"col":9,"async":false,"isNew":false}',
               '{"fn":"Server.start","file":"file:///app/src/server.mjs","line":40,"col":5,"async":true,"isNew":false}',
               '{"fn":"Router","file":"/app/src/router.js","line":7,"col":3,"async":false,"isNew":true}',
               '{"fn":"Object.<anonymous>","file":"/app/index.js","line":3,"col":1,"async":false,"isNew":false}',
               '{"fn":null,"file":"file:///app/src/anon.mjs","line":99,"col":12,"async":false,"isNew":false}',
               '{"fn":"Class.method [as '
               'alias]","file":"C:\\\\proj\\\\a.js","line":5,"col":7,"async":false,"isNew":false}',
               '{"fn":"process.processTicksAndRejections","file":"node:internal/process/task_queues","line":95,"col":5,"async":false,"isNew":false}',
               '{"fn":null,"file":"file:///app/async-anon.mjs","line":1,"col":2,"async":true,"isNew":false}',
               '0 0']},
 {'id': 'j21-line-splitter',
  'mode': 'js',
  'title': 'Построчный Transform-поток',
  'statement': 'Напишите createLineSplitter() → Transform (из node:stream), который принимает '
               'строки/буферы (decodeStrings отключать не нужно: на входе строки) и выдаёт в '
               'readable-сторону (objectMode) отдельные строки без символов конца строки. '
               'Разделители — «\\n» и «\\r\\n». Неполная последняя строка копится до следующего '
               'чанка; при завершении потока (flush) выдаётся остаток, если он непустой. Пустые '
               'строки между разделителями сохраняются (как пустые строки). Строка, разбитая между '
               'чанками (в том числе «\\r» и «\\n» в разных чанках), собирается правильно.',
  'starter': 'import { Transform } from "node:stream";\nfunction createLineSplitter() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'import { Readable } from "node:stream";\n'
            'import { pipeline } from "node:stream/promises";\n'
            'async function lines(chunks) { const out = []; await pipeline(Readable.from(chunks), '
            'createLineSplitter(), async (src) => { for await (const l of src) out.push(l); }); '
            'return out; }\n'
            'console.log(JSON.stringify(await lines(["ab\\ncd\\n"])));\n'
            'console.log(JSON.stringify(await lines(["a", "b\\nc", "d\\ne"])));\n'
            'console.log(JSON.stringify(await lines(["x\\r\\ny\\r", "\\nz\\r\\n\\r\\nw"])));\n'
            'console.log(JSON.stringify(await lines(["\\n\\n", "tail"])));\n'
            'console.log(JSON.stringify(await lines([])), JSON.stringify(await lines(["only"])), '
            'JSON.stringify(await lines(["end\\n"])));\n'
            'console.log(JSON.stringify(await lines(["héllo\\nwörld", "\\nпривет"])));\n'
            'const s = createLineSplitter(); console.log(s.readableObjectMode, typeof s.pipe);\n',
  'hint': 'Transform({ readableObjectMode: true, transform(chunk, enc, cb) {...}, flush(cb) {...} '
          '}); буфер строкой.',
  'expected': ['["ab","cd"]',
               '["ab","cd","e"]',
               '["x","y","z","","w"]',
               '["","","tail"]',
               '[] ["only"] ["end"]',
               '["héllo","wörld","привет"]',
               'true function']},
 {'id': 'j21-writable',
  'mode': 'js',
  'title': 'Обратное давление',
  'statement': 'Напишите createWritable({ highWaterMark, sink }) → { write(chunk), end(), '
               'on(event, fn) }. sink(chunk, cb) — асинхронная запись одного куска, по завершении '
               'вызывает cb(). Размер куска — chunk.length. Состояние: length — суммарный размер '
               'ещё не записанных кусков (включая тот, что пишется сейчас). write(chunk): length '
               '+= размер; затем, если ни один кусок не пишется, сразу запустить sink для него, '
               'иначе поставить в очередь; результат write — length < highWaterMark, он '
               'определяется сразу после добавления, ещё до запуска sink; если получилось false — '
               'запомнить needDrain (до запуска sink). Когда sink вызвал cb: length −= размер; '
               'если очередь не пуста — запустить следующий; иначе, если needDrain, сбросить его и '
               "вызвать обработчики 'drain'. end(): после записи всего вызвать 'finish' (если всё "
               "уже записано — вызвать сразу, синхронно); write после end — Error('write after "
               "end'). on(event, fn) поддерживает 'drain' и 'finish'.",
  'starter': 'function createWritable({ highWaterMark, sink }) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const log = [];\n'
            'const w = createWritable({ highWaterMark: 5, sink: (chunk, cb) => setTimeout(() => { '
            'log.push("wrote:" + chunk); cb(); }, 2) });\n'
            'w.on("drain", () => log.push("drain")); w.on("finish", () => log.push("finish"));\n'
            'console.log(w.write("ab"), w.write("cd"), w.write("ef"), w.write("g"));\n'
            'await new Promise((r) => setTimeout(r, 30));\n'
            'console.log(log.join(" "));\n'
            'log.length = 0;\n'
            'console.log(w.write("12345"));\n'
            'w.end();\n'
            'try { w.write("late"); } catch (e) { console.log(e.message); }\n'
            'await new Promise((r) => setTimeout(r, 30));\n'
            'console.log(log.join(" "));\n'
            'const fast = createWritable({ highWaterMark: 3, sink: (c, cb) => cb() }); const l2 = '
            '[]; fast.on("drain", () => l2.push("d")); fast.on("finish", () => l2.push("f"));\n'
            'console.log(fast.write("abcd"), l2.join(), fast.write("x"), l2.join()); fast.end(); '
            'console.log(l2.join());\n',
  'hint': 'Очередь queue, флаг writing, needDrain, ended; функция next().',
  'expected': ['true true false false',
               'wrote:ab wrote:cd wrote:ef wrote:g drain',
               'false',
               'write after end',
               'wrote:12345 finish',
               'false d true d',
               'd,f']},
 {'id': 'j21-limit-pool',
  'mode': 'js',
  'title': 'Пул с ограничением параллелизма',
  'statement': 'Напишите createPool(limit) → { run(task), idle() }. run(task) принимает функцию '
               '(sync или async), ставит её в очередь и возвращает промис с её результатом (или '
               'отказом). Одновременно выполняется не более limit задач; запуск — строго в порядке '
               'очереди (FIFO); отказ одной задачи не мешает остальным. idle() возвращает промис, '
               'который выполнится, когда нет ни выполняющихся, ни ожидающих задач (если пул уже '
               "простаивает — сразу). limit меньше 1 — Error('limit must be >= 1').",
  'starter': 'function createPool(limit) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const sleep = (ms) => new Promise((r) => setTimeout(r, ms));\n'
            'const pool = createPool(2); let active = 0, maxActive = 0; const started = [];\n'
            'const job = (name, ms, fail) => () => { started.push(name); active++; maxActive = '
            'Math.max(maxActive, active); return sleep(ms).then(() => { active--; if (fail) throw '
            'new Error(name + " failed"); return name.toUpperCase(); }); };\n'
            'const ps = [pool.run(job("a", 20)), pool.run(job("b", 5)), pool.run(job("c", 5, '
            'true)), pool.run(job("d", 5)), pool.run(job("e", 1)), pool.run(() => "sync")];\n'
            'const res = await Promise.allSettled(ps);\n'
            'console.log(res.map((r) => (r.status === "fulfilled" ? r.value : "ERR:" + '
            'r.reason.message)).join(" "));\n'
            'console.log(started.join(""), maxActive);\n'
            'await pool.idle(); console.log("idle ok");\n'
            'const p2 = createPool(1); const order = []; p2.run(async () => { await sleep(5); '
            'order.push(1); }); p2.run(() => order.push(2)); p2.run(async () => { order.push(3); '
            '});\n'
            'await p2.idle(); console.log(order.join(""));\n'
            'const t0 = Date.now(); await createPool(3).idle(); console.log(Date.now() - t0 < '
            '20);\n'
            'try { createPool(0); } catch (e) { console.log(e.message); }\n'
            'const p3 = createPool(2); const r = await Promise.all([p3.run(() => 1), p3.run(async '
            '() => 2)]); console.log(r.join());\n',
  'hint': 'Счётчик active, очередь; после завершения запускайте следующую; idle — список ожидающих '
          'resolve.',
  'expected': ['A B ERR:c failed D E sync',
               'abcde 2',
               'idle ok',
               '123',
               'true',
               'limit must be >= 1',
               '1,2']},
 {'id': 'j21-cluster',
  'mode': 'js',
  'title': 'Кластер: круговая раздача',
  'statement': 'Напишите createCluster(n) → { dispatch(), kill(id), fork(), alive() }. Рабочие '
               'нумеруются с 1; порядок обхода — по возрастанию номера (новые, созданные fork, '
               'получают следующий номер и встают в конец). dispatch() возвращает id следующего '
               'живого рабочего после последнего выбранного (по кругу; перед первым вызовом '
               "«последний» — предшествующий первому); если живых нет — Error('No workers'). "
               'kill(id) помечает рабочего мёртвым (неизвестный или уже мёртвый id — Error(`No '
               'such worker: ${id}`)). fork() создаёт нового живого рабочего и возвращает его id. '
               'alive() — массив id живых по возрастанию.',
  'starter': 'function createCluster(n) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const c = createCluster(3);\n'
            'const d = (k) => Array.from({ length: k }, () => c.dispatch()).join("");\n'
            'console.log(d(7));\n'
            'c.kill(2); console.log(d(4), c.alive().join());\n'
            'console.log(c.fork(), c.alive().join(), d(6));\n'
            'c.kill(1); c.kill(3); console.log(d(3), c.alive().join());\n'
            'try { c.kill(3); } catch (e) { console.log(e.message); }\n'
            'try { c.kill(99); } catch (e) { console.log(e.message); }\n'
            'c.kill(4);\n'
            'try { c.dispatch(); } catch (e) { console.log(e.message); }\n'
            'console.log(c.fork(), d(3), c.alive().join());\n'
            'const solo = createCluster(1); console.log(solo.dispatch(), solo.dispatch());\n',
  'hint': 'Массив рабочих {id, alive}, указатель last (id); поиск следующего по кругу.',
  'expected': ['1231231',
               '3131 1,3',
               '4 1,3,4 341341',
               '444 4',
               'No such worker: 3',
               'No such worker: 99',
               'No workers',
               '5 555 5',
               '1 1']},
 {'id': 'j21-shapes',
  'mode': 'js',
  'title': 'Скрытые классы V8',
  'statement': 'Напишите createShapes() → { shapeOf(obj), count(), sameShape(a, b) }. Форма '
               '(hidden class) объекта определяется последовательностью его собственных строковых '
               'ключей в порядке Object.keys (значения не важны). Формы образуют дерево переходов: '
               'пустой объект — форма 0 (корень); для каждого нового (родитель, ключ) создаётся '
               'форма со следующим порядковым номером при первом обращении. shapeOf(obj) '
               'возвращает номер формы, проходя ключи по порядку и создавая переходы по мере '
               'необходимости; count() — общее число форм (с корнем); sameShape(a, b) — совпадают '
               'ли формы (создаёт переходы, если нужно).',
  'starter': 'function createShapes() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const s = createShapes();\n'
            'const p1 = { x: 1, y: 2 }, p2 = { x: 10, y: 20 }, p3 = { y: 1, x: 2 }, p4 = { x: 1 }, '
            'p5 = { x: 1, y: 2, z: 3 };\n'
            'console.log([p1, p2, p3, p4, p5, {}].map((o) => s.shapeOf(o)).join(), s.count());\n'
            'console.log(s.sameShape(p1, p2), s.sameShape(p1, p3), s.sameShape({}, {}), '
            's.sameShape(p4, { x: "str" }), s.count());\n'
            'const o = {}; o.a = 1; const a1 = s.shapeOf(o); o.b = 2; const a2 = s.shapeOf(o); '
            'delete o.a; console.log(a1, a2, s.shapeOf(o), s.count());\n'
            'const q = { x: 1 }; q.y = 2; console.log(s.shapeOf(q) === s.shapeOf(p1));\n'
            'const fresh = createShapes(); console.log(fresh.count(), fresh.shapeOf({ k: 1 }), '
            'fresh.count(), fresh.shapeOf({ "": 1 }), fresh.shapeOf({ k: 1, "": 2 }));\n',
  'hint': 'Дерево: Map от «id родителя + ключ» к id; шаги по ключам.',
  'expected': ['2,2,4,1,5,0 6', 'true false true true 6', '6 7 8 9', 'true', '1 1 2 2 3']},
 {'id': 'j21-inline-cache',
  'mode': 'js',
  'title': 'Inline cache',
  'statement': 'Напишите createCallSite() → { observe(shapeId) }. Место доступа к свойству '
               "запоминает формы объектов. Состояния: 'uninitialized' (форм не видели), "
               "'monomorphic' (1 форма), 'polymorphic' (2–4 разные формы), 'megamorphic' (5 и "
               'более; состояние необратимо, кэш больше не используется). observe(shapeId) '
               'вызывается при каждом обращении и возвращает { state, hit }: state — состояние '
               'после обращения; hit — true, если форма уже была в кэше на момент обращения и '
               'состояние до обращения не было megamorphic (megamorphic всегда hit = false; первое '
               'обращение — hit = false).',
  'starter': 'function createCallSite() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const cs = createCallSite();\n'
            'const seq = [1, 1, 2, 1, 2, 3, 4, 4, 5, 1, 2, 6];\n'
            'console.log(seq.map((s) => { const r = cs.observe(s); return '
            '`${s}:${r.state[0]}${r.state.startsWith("mega") ? "M" : ""}${r.hit ? "+" : "-"}`; '
            '}).join(" "));\n'
            'const mono = createCallSite(); console.log([7, 7, 7].map((s) => '
            'JSON.stringify(mono.observe(s))).join(" "));\n'
            'const p = createCallSite(); for (const s of [1, 2, 3, 4]) p.observe(s); '
            'console.log(JSON.stringify(p.observe(4)), JSON.stringify(p.observe(5)), '
            'JSON.stringify(p.observe(1)));\n',
  'hint': 'Set форм и флаг mega; hit вычисляется до добавления формы.',
  'expected': ['1:m- 1:m+ 2:p- 1:p+ 2:p+ 3:p- 4:p- 4:p+ 5:mM- 1:mM- 2:mM- 6:mM-',
               '{"state":"monomorphic","hit":false} {"state":"monomorphic","hit":true} '
               '{"state":"monomorphic","hit":true}',
               '{"state":"polymorphic","hit":true} {"state":"megamorphic","hit":false} '
               '{"state":"megamorphic","hit":false}']},
 {'id': 'j21-tiering',
  'mode': 'js',
  'title': 'Уровни компиляции и деоптимизация',
  'statement': 'Напишите createTiering({ baseline = 8, optimize = 40 } = {}) → { call(name, sig), '
               'stats(name) }. Функция имеет счётчик calls и множество feedback (типы аргументов, '
               "виденные в вызовах: строка sig, например 'int,int'). call(name, sig) → { tier, "
               'deopt }. Уровень для этого вызова определяется числом вызовов ДО него: меньше '
               "baseline — 'ignition'; меньше optimize — 'baseline'; иначе 'optimized'. До "
               'перехода в optimized каждый вызов добавляет sig в feedback. В optimized: если sig '
               "уже в feedback — вызов идёт на 'optimized'; иначе происходит деоптимизация: этот "
               "вызов возвращает { tier: 'ignition', deopt: true }, sig добавляется в feedback, "
               'calls сбрасывается в 0 и затем этот вызов считается (calls = 1), счётчик deopts '
               'растёт. После деоптимизации функция снова проходит уровни с начала. stats(name) → '
               '{ calls, deopts, feedback: отсортированный массив }; для незнакомой функции — { '
               'calls: 0, deopts: 0, feedback: [] }.',
  'starter': 'function createTiering(opts = {}) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const jit = createTiering({ baseline: 3, optimize: 6 });\n'
            'const out = []; for (let i = 0; i < 9; i++) { const r = jit.call("add", "int,int"); '
            'out.push(r.tier[0] + (r.deopt ? "!" : "")); }\n'
            'console.log(out.join(" "), JSON.stringify(jit.stats("add")));\n'
            'const r = jit.call("add", "str,str"); console.log(JSON.stringify(r), '
            'JSON.stringify(jit.stats("add")));\n'
            'const out2 = []; for (let i = 0; i < 8; i++) { const x = jit.call("add", i % 2 ? '
            '"str,str" : "int,int"); out2.push(x.tier[0] + (x.deopt ? "!" : "")); } '
            'console.log(out2.join(" "), JSON.stringify(jit.stats("add")));\n'
            'console.log(JSON.stringify(jit.stats("none")), JSON.stringify(jit.call("other", '
            '"x")));\n'
            'const d = createTiering(); const o3 = []; for (let i = 0; i < 45; i++) '
            'o3.push(d.call("f", "a").tier[0]); console.log(o3.join("").replace(/(.)\\1+/g, (m, c) '
            '=> c + m.length));\n'
            'const m = createTiering({ baseline: 1, optimize: 2 }); console.log(["a", "a", "a", '
            '"b", "b", "b", "a"].map((s) => { const x = m.call("g", s); return x.tier[0] + '
            '(x.deopt ? "!" : ""); }).join(" "), JSON.stringify(m.stats("g")));\n',
  'hint': 'Объект на функцию: calls, deopts, feedback (Set); сначала tier по calls, потом '
          'обновление.',
  'expected': ['i i i b b b o o o {"calls":9,"deopts":0,"feedback":["int,int"]}',
               '{"tier":"ignition","deopt":true} '
               '{"calls":1,"deopts":1,"feedback":["int,int","str,str"]}',
               'i i b b b o o o {"calls":9,"deopts":1,"feedback":["int,int","str,str"]}',
               '{"calls":0,"deopts":0,"feedback":[]} {"tier":"ignition","deopt":false}',
               'i8b32o5',
               'i b o i! b o o {"calls":4,"deopts":1,"feedback":["a","b"]}']},
 {'id': 'j21-loop-lag',
  'mode': 'js',
  'title': 'Задержка цикла событий',
  'statement': 'Напишите loopLag(ticks, intervalMs, thresholdMs = 0): ticks — моменты (мс) '
               'срабатывания таймера, который должен срабатывать каждые intervalMs мс начиная с 0. '
               'Лаг i-го срабатывания = max(0, ticks[i] − ticks[i−1] − intervalMs), для первого '
               'предыдущее равно 0. Верните { count, min, max, mean, p50, p99, blocked }: mean — '
               'среднее, округлённое до 2 знаков; p50 и p99 — перцентили методом ближайшего ранга '
               '(отсортировать по возрастанию, индекс = ceil(p/100 · n) − 1); blocked — число '
               'срабатываний с лагом строго больше thresholdMs. Для пустого массива — все поля 0.',
  'starter': 'function loopLag(ticks, intervalMs, thresholdMs = 0) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(JSON.stringify(loopLag([100, 200, 300, 400], 100)));\n'
            'console.log(JSON.stringify(loopLag([105, 200, 340, 400, 520, 600, 610], 100, 10)));\n'
            'const ticks = []; let t = 0; for (let i = 0; i < 100; i++) { t += 100 + (i === 50 ? '
            '480 : i % 10 === 0 ? 7 : 0); ticks.push(t); }\n'
            'console.log(JSON.stringify(loopLag(ticks, 100, 5)));\n'
            'console.log(JSON.stringify(loopLag([], 100)), JSON.stringify(loopLag([97], 100)), '
            'JSON.stringify(loopLag([130], 100, 29)));\n'
            'console.log(JSON.stringify(loopLag([10, 10, 50], 10)));\n',
  'hint': 'Сначала массив лагов, затем статистика.',
  'expected': ['{"count":4,"min":0,"max":0,"mean":0,"p50":0,"p99":0,"blocked":0}',
               '{"count":7,"min":0,"max":40,"mean":9.29,"p50":0,"p99":40,"blocked":2}',
               '{"count":100,"min":0,"max":480,"mean":5.43,"p50":0,"p99":7,"blocked":10}',
               '{"count":0,"min":0,"max":0,"mean":0,"p50":0,"p99":0,"blocked":0} '
               '{"count":1,"min":0,"max":0,"mean":0,"p50":0,"p99":0,"blocked":0} '
               '{"count":1,"min":30,"max":30,"mean":30,"p50":30,"p99":30,"blocked":1}',
               '{"count":3,"min":0,"max":30,"mean":10,"p50":0,"p99":30,"blocked":1}']},
 {'id': 'j21-config',
  'mode': 'js',
  'title': 'Конфигурация из переменных окружения',
  'statement': 'Напишите loadConfig(env, schema) → { config, errors }. schema — { ИМЯ: { type, '
               "required?, default?, enum?, min?, max? } }, type: 'string' | 'number' | 'boolean' "
               "| 'port'. Пустая строка и отсутствие переменной — «не задано». Не задано: есть "
               'default — берётся как есть (без проверок); required — ошибка `ИМЯ: is required`; '
               'иначе ключа нет в config. Задано: string — как есть; number — Number(значение), '
               'нечисло/NaN — `ИМЯ: must be a number`; boolean — без учёта регистра true/1/yes/on '
               '→ true, false/0/no/off → false, иначе `ИМЯ: must be a boolean`; port — целое от 1 '
               'до 65535, иначе `ИМЯ: must be a port (1-65535)`. Затем enum (значение после '
               'преобразования должно входить): `ИМЯ: must be one of a, b`; min/max для number: '
               '`ИМЯ: must be >= N` / `ИМЯ: must be <= N`. Собираются все ошибки (по порядку '
               'схемы); при ошибке значение в config не попадает.',
  'starter': 'function loadConfig(env, schema) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const schema = {\n'
            '  NODE_ENV: { type: "string", enum: ["development", "production", "test"], default: '
            '"development" },\n'
            '  PORT: { type: "port", default: 3000 }, WORKERS: { type: "number", min: 1, max: 16, '
            'default: 2 },\n'
            '  DEBUG: { type: "boolean", default: false }, DATABASE_URL: { type: "string", '
            'required: true }, TIMEOUT: { type: "number" }, REGION: { type: "string", enum: ["eu", '
            '"us"] },\n'
            '};\n'
            'const show = (env) => { const r = loadConfig(env, schema); '
            'console.log(JSON.stringify(r)); };\n'
            'show({ DATABASE_URL: "pg://x" });\n'
            'show({ DATABASE_URL: "pg://x", NODE_ENV: "production", PORT: "8080", WORKERS: "8", '
            'DEBUG: "YES", TIMEOUT: "1.5", REGION: "eu" });\n'
            'show({});\n'
            'show({ DATABASE_URL: "", PORT: "0", WORKERS: "abc", DEBUG: "maybe", NODE_ENV: '
            '"staging", REGION: "asia", TIMEOUT: "x" });\n'
            'show({ DATABASE_URL: "u", PORT: "65536", WORKERS: "20" }); show({ DATABASE_URL: "u", '
            'PORT: "80.5", WORKERS: "0", DEBUG: "0", TIMEOUT: "" }); show({ DATABASE_URL: "u", '
            'PORT: " 80", DEBUG: "Off", WORKERS: "16" });\n',
  'hint': 'Для каждого имени: raw, parse → value|error, затем enum и границы.',
  'expected': ['{"config":{"NODE_ENV":"development","PORT":3000,"WORKERS":2,"DEBUG":false,"DATABASE_URL":"pg://x"},"errors":[]}',
               '{"config":{"NODE_ENV":"production","PORT":8080,"WORKERS":8,"DEBUG":true,"DATABASE_URL":"pg://x","TIMEOUT":1.5,"REGION":"eu"},"errors":[]}',
               '{"config":{"NODE_ENV":"development","PORT":3000,"WORKERS":2,"DEBUG":false},"errors":["DATABASE_URL: '
               'is required"]}',
               '{"config":{},"errors":["NODE_ENV: must be one of development, production, '
               'test","PORT: must be a port (1-65535)","WORKERS: must be a number","DEBUG: must be '
               'a boolean","DATABASE_URL: is required","TIMEOUT: must be a number","REGION: must '
               'be one of eu, us"]}',
               '{"config":{"NODE_ENV":"development","DEBUG":false,"DATABASE_URL":"u"},"errors":["PORT: '
               'must be a port (1-65535)","WORKERS: must be <= 16"]}',
               '{"config":{"NODE_ENV":"development","DEBUG":false,"DATABASE_URL":"u"},"errors":["PORT: '
               'must be a port (1-65535)","WORKERS: must be >= 1"]}',
               '{"config":{"NODE_ENV":"development","PORT":80,"WORKERS":16,"DEBUG":false,"DATABASE_URL":"u"},"errors":[]}']},
 {'id': 'j21-signals',
  'mode': 'js',
  'title': 'Обработка сигналов',
  'statement': 'Таблица SIGNALS уже есть. Напишите createSignalHandler({ onGraceful, onReload }) → '
               '{ handle(sig), finish() }. handle(sig) возвращает { action, exit? }. SIGINT и '
               "SIGTERM: первый — action 'graceful' (вызвать onGraceful(sig) один раз; запомнить "
               'первый сигнал); пока завершение не закончено, любой следующий SIGINT/SIGTERM — { '
               "action: 'force', exit: 128 + номер этого сигнала }. SIGHUP — { action: 'reload' } "
               "(вызывает onReload; если идёт завершение — игнорируется: { action: 'ignore' }). "
               "SIGUSR2 и прочие известные сигналы — { action: 'ignore' }; неизвестное имя — "
               'Error(`Unknown signal: ${sig}`). finish() — вызывается, когда мягкое завершение '
               "закончено: { action: 'exit', exit: 128 + номер первого сигнала } (если graceful не "
               "начинался — Error('Not shutting down')); после finish или force любой handle — "
               "Error('Already exited').",
  'starter': '// Готово: номера сигналов Linux (не изменяйте)\n'
             'const SIGNALS = { SIGHUP: 1, SIGINT: 2, SIGQUIT: 3, SIGABRT: 6, SIGKILL: 9, SIGUSR1: '
             '10, SIGSEGV: 11, SIGUSR2: 12, SIGPIPE: 13, SIGALRM: 14, SIGTERM: 15 };\n'
             'function createSignalHandler({ onGraceful, onReload }) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const log = [];\n'
            'const h = createSignalHandler({ onGraceful: (s) => log.push("graceful:" + s), '
            'onReload: () => log.push("reload") });\n'
            'const t = (s) => { try { console.log(s, JSON.stringify(h.handle(s))); } catch (e) { '
            'console.log(s, "!", e.message); } };\n'
            't("SIGHUP"); t("SIGUSR2"); t("SIGTERM"); t("SIGHUP"); t("SIGUSR1"); t("SIGFOO");\n'
            'try { console.log(JSON.stringify(h.finish())); } catch (e) { console.log(e.message); '
            '}\n'
            't("SIGINT");\n'
            'console.log(log.join());\n'
            'const h2 = createSignalHandler({ onGraceful: () => log.push("g2"), onReload() {} });\n'
            'try { h2.finish(); } catch (e) { console.log(e.message); }\n'
            'console.log(JSON.stringify(h2.handle("SIGINT")), '
            'JSON.stringify(h2.handle("SIGINT")));\n'
            'try { h2.handle("SIGTERM"); } catch (e) { console.log(e.message); }\n'
            'const h3 = createSignalHandler({ onGraceful: () => log.push("g3"), onReload() {} }); '
            'h3.handle("SIGINT"); console.log(JSON.stringify(h3.handle("SIGTERM")), log.filter((x) '
            '=> x.startsWith("g")).join());\n',
  'hint': 'Состояние: first (имя сигнала), exited.',
  'expected': ['SIGHUP {"action":"reload"}',
               'SIGUSR2 {"action":"ignore"}',
               'SIGTERM {"action":"graceful"}',
               'SIGHUP {"action":"ignore"}',
               'SIGUSR1 {"action":"ignore"}',
               'SIGFOO ! Unknown signal: SIGFOO',
               '{"action":"exit","exit":143}',
               'SIGINT ! Already exited',
               'reload,graceful:SIGTERM',
               'Not shutting down',
               '{"action":"graceful"} {"action":"force","exit":130}',
               'Already exited',
               '{"action":"force","exit":143} graceful:SIGTERM,g2,g3']},
 {'id': 'j21-cjs-exports',
  'mode': 'js',
  'title': 'Именованные экспорты CommonJS',
  'statement': 'Напишите detectNamedExports(source) → отсортированный по алфавиту массив имён без '
               'повторов — упрощённый аналог cjs-module-lexer, который Node использует при import '
               'из CommonJS. Сначала удалите комментарии (// и /* */). Находятся: `exports.имя =`, '
               '`module.exports.имя =` (имя — идентификатор; «==» не считается присваиванием), '
               '`Object.defineProperty(exports, "имя"` и `Object.defineProperty(module.exports, '
               "'имя'` (кавычки любые), а также литерал `module.exports = { a, b: 1, 'c': 2, d() "
               '{} }`: ключи верхнего уровня — идентификаторы (в том числе шорткат «a»), строки в '
               'кавычках и методы; вложенные объекты и значения игнорируются (учтите запятые '
               'внутри скобок/фигурных/квадратных скобок и строк). Имя «default» не включается. '
               'Если после `module.exports =` стоит не «{» — это не литерал (ничего не '
               'добавляется).',
  'starter': 'function detectNamedExports(source) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (src) => console.log(JSON.stringify(detectNamedExports(src)));\n'
            't("exports.a = 1;\\nmodule.exports.b = function () {};\\nexports.a = 2;");\n'
            't("// exports.hidden = 1\\n/* module.exports.x = 1 */\\nexports.shown = 1;");\n'
            't("Object.defineProperty(exports, \'x\', { value: 1 '
            '});\\nObject.defineProperty(module.exports, \\"y\\", { get() {} });");\n'
            't("module.exports = { a, b: 1, \'c-d\': 2, e() {}, f: { g: 1, h: 2 }, i: [1, 2, 3], '
            'j: (x, y) => x, k: \\"a,b\\" };");\n'
            't("module.exports = function main() {};\\nexports.extra = 1;");\n'
            't("if (exports.flag == 1) {}\\nexports.ok = 1;\\nconst x = exports.read;");\n'
            't("exports.default = 1;\\nmodule.exports = { default: 2, real: 3 };");\n'
            't("module.exports = {\\n  async run() {},\\n  get value() { return 1; },\\n  '
            '[computed]: 1,\\n  ...rest,\\n  last,\\n};");\n'
            't("");\n',
  'hint': 'Регулярные выражения для первых форм; для литерала — ручной разбор верхнего уровня с '
          'глубиной скобок.',
  'expected': ['["a","b"]',
               '["shown"]',
               '["x","y"]',
               '["a","b","c-d","e","f","i","j","k"]',
               '["extra"]',
               '["ok"]',
               '["real"]',
               '["last","run","value"]',
               '[]']},
 {'id': 'j21-heap-diff',
  'mode': 'js',
  'title': 'Снимки кучи и утечки',
  'statement': 'Снимок кучи — { Конструктор: { count, size } }. Напишите diffHeap(before, after, { '
               'top = 3 } = {}) и findLeaks(snapshots). diffHeap → массив до top элементов { name, '
               'dCount, dSize } — для конструкторов, у которых размер вырос (dSize > 0; '
               'отсутствующий в before считается { count: 0, size: 0 }), по убыванию dSize, при '
               'равенстве — по имени. findLeaks(snapshots) (массив ≥ 2 снимков в порядке времени) '
               '→ массив { name, growth } для конструкторов, размер которых строго возрастал на '
               'каждом шаге между соседними снимками (конструктор должен присутствовать во всех '
               'снимках), growth = размер в последнем − размер в первом; по убыванию growth, при '
               'равенстве — по имени.',
  'starter': 'function diffHeap(before, after, opts = {}) {\n'
             '}\n'
             'function findLeaks(snapshots) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const s1 = { Array: { count: 100, size: 4000 }, Buffer: { count: 10, size: 10000 }, '
            'Session: { count: 5, size: 500 }, Closure: { count: 50, size: 2000 } };\n'
            'const s2 = { Array: { count: 120, size: 4800 }, Buffer: { count: 10, size: 10000 }, '
            'Session: { count: 25, size: 2500 }, Closure: { count: 40, size: 1600 }, Cache: { '
            'count: 3, size: 3000 } };\n'
            'const s3 = { Array: { count: 110, size: 4400 }, Buffer: { count: 10, size: 9000 }, '
            'Session: { count: 60, size: 6000 }, Cache: { count: 6, size: 6000 }, Closure: { '
            'count: 45, size: 1800 } };\n'
            'console.log(JSON.stringify(diffHeap(s1, s2))); '
            'console.log(JSON.stringify(diffHeap(s1, s2, { top: 1 }))); '
            'console.log(JSON.stringify(diffHeap(s2, s1)), JSON.stringify(diffHeap({}, {})));\n'
            'console.log(JSON.stringify(findLeaks([s1, s2, s3])), JSON.stringify(findLeaks([s2, '
            's3])), JSON.stringify(findLeaks([s1])), JSON.stringify(findLeaks([s1, s1])));\n'
            'console.log(JSON.stringify(findLeaks([{ A: { count: 1, size: 1 }, B: { count: 1, '
            'size: 1 } }, { A: { count: 2, size: 2 }, B: { count: 2, size: 2 } }, { A: { count: 3, '
            'size: 3 }, B: { count: 3, size: 3 } }])));\n',
  'hint': 'Объединение имён из before и after; для findLeaks — проверка каждой пары.',
  'expected': ['[{"name":"Cache","dCount":3,"dSize":3000},{"name":"Session","dCount":20,"dSize":2000},{"name":"Array","dCount":20,"dSize":800}]',
               '[{"name":"Cache","dCount":3,"dSize":3000}]',
               '[{"name":"Closure","dCount":10,"dSize":400}] []',
               '[{"name":"Session","growth":5500}] '
               '[{"name":"Session","growth":3500},{"name":"Cache","growth":3000},{"name":"Closure","growth":200}] '
               '[] []',
               '[{"name":"A","growth":2},{"name":"B","growth":2}]']},
 {'id': 'j21-error-chain',
  'mode': 'js',
  'title': 'Вывод цепочки ошибок',
  'statement': 'Напишите formatError(err, depth = 0) → строка (строки через «\\n»). pad = 2·depth '
               'пробелов. Первая строка: pad + имя + (если есть err.code — ` [код]`) + «: » + '
               'сообщение. Если у ошибки есть cause (не undefined): строка `${pad}  [cause]:` и '
               'далее — formatError(cause, depth + 2), а если cause не Error — pad + 4 пробела + '
               'String(cause). Если err — AggregateError (err.errors — массив): строка `${pad}  '
               '[errors]:` и затем для каждого элемента — formatError(e, depth + 2) (не-Error — '
               'pad + 4 пробела + String(e)). Порядок: сначала cause, потом errors. Ссылка на уже '
               'встречавшуюся в цепочке ошибку (цикл через cause или errors) выводится строкой pad '
               "+ '[Circular]'.",
  'starter': 'function formatError(err, depth = 0) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const e1 = new Error("connect failed"); e1.code = "ECONNREFUSED";\n'
            'const e2 = new Error("query failed", { cause: e1 });\n'
            'const e3 = new TypeError("request failed", { cause: e2 });\n'
            'console.log(formatError(e3));\n'
            'console.log(formatError(new Error("plain")));\n'
            'console.log(formatError(new Error("with string cause", { cause: "just text" })));\n'
            'console.log(formatError(new Error("zero cause", { cause: 0 })));\n'
            'const agg = new AggregateError([new Error("one"), Object.assign(new '
            'RangeError("two"), { code: "E2" }), "str", new Error("three", { cause: new '
            'Error("deep") })], "all failed");\n'
            'console.log(formatError(agg));\n'
            'const loop = new Error("loop"); loop.cause = new Error("inner"); loop.cause.cause = '
            'loop; console.log(formatError(loop));\n'
            'const shared = new Error("shared"); console.log(formatError(new '
            'AggregateError([shared, shared], "twice")));\n'
            'console.log(formatError(new Error("x"), 2));\n',
  'hint': 'Рекурсивная функция с Set посещённых в текущей ветви.',
  'expected': ['TypeError: request failed',
               '  [cause]:',
               '    Error: query failed',
               '      [cause]:',
               '        Error [ECONNREFUSED]: connect failed',
               'Error: plain',
               'Error: with string cause',
               '  [cause]:',
               '    just text',
               'Error: zero cause',
               '  [cause]:',
               '    0',
               'AggregateError: all failed',
               '  [errors]:',
               '    Error: one',
               '    RangeError [E2]: two',
               '    str',
               '    Error: three',
               '      [cause]:',
               '        Error: deep',
               'Error: loop',
               '  [cause]:',
               '    Error: inner',
               '      [cause]:',
               '        [Circular]',
               'AggregateError: twice',
               '  [errors]:',
               '    Error: shared',
               '    Error: shared',
               '    Error: x']},
 {'id': 'j21-esm-order',
  'mode': 'js',
  'title': 'Порядок выполнения ES-модулей',
  'statement': 'Напишите esmOrder(graph, entry) → массив имён модулей в порядке выполнения. graph '
               '— { модуль: { imports: [имена] } } (ключ imports может отсутствовать). Правила как '
               'у ES-модулей: обход в глубину от entry, импорты — по порядку объявления; модуль '
               'выполняется после всех своих зависимостей (пост-порядок); каждый модуль '
               'выполняется один раз; при циклическом импорте уже посещаемый модуль пропускается '
               '(ошибки нет, зависимость цикла выполняется раньше, а модуль, замкнувший цикл, — '
               "после неё). Модуль, которого нет в graph, — Error(`Cannot find module '${имя}'`).",
  'starter': 'function esmOrder(graph, entry) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const g = { main: { imports: ["a", "b", "log"] }, a: { imports: ["c", "log"] }, b: { '
            'imports: ["c", "a"] }, c: { imports: [] }, log: {}, x: { imports: ["y"] }, y: { '
            'imports: ["x", "z"] }, z: { imports: ["x"] }, bad: { imports: ["ghost"] } };\n'
            'const t = (e) => { try { console.log(e, esmOrder(g, e).join(" ")); } catch (err) { '
            'console.log(e, "!", err.message); } };\n'
            't("main"); t("x"); t("y"); t("c"); t("bad"); t("nope");\n'
            'console.log(esmOrder({ a: { imports: ["a"] } }, "a").join());\n',
  'hint': 'DFS с множеством seen: добавлять в seen при входе, в результат — при выходе.',
  'expected': ['main c log a b main',
               'x z y x',
               'y x z y',
               'c c',
               "bad ! Cannot find module 'ghost'",
               "nope ! Cannot find module 'nope'",
               'a']}]}
