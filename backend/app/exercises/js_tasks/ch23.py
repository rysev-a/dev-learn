"""Задачи книги «Современный Frontend»: глава 23."""

TASKS: dict[int, list[dict]] = {23: [{'id': 'j23-permissions',
  'mode': 'js',
  'title': 'Модель прав доступа',
  'statement': 'Напишите isAllowed(perms, kind, target). perms = { allow: { read, write, net, env '
               '}, deny: { … } }, значение — true (всё) или массив записей. Если target подпадает '
               'под deny[kind] — false. Иначе true, если allow[kind] === true или подпадает под '
               'запись из allow[kind]; иначе false. Правила подпадания: read/write — запись '
               '«/data» подходит к «/data» и к «/data/…» (но не к «/database»), завершающий «/» в '
               'записи игнорируется; net — запись «host» подходит к «host» и «host:порт», запись '
               '«host:порт» — только к точному «host:порт»; env — точное совпадение имени.',
  'starter': 'function isAllowed(perms, kind, target) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const perms = {\n'
            '  allow: { read: ["/data/", "/etc/app"], net: ["api.example.com", "localhost:8080"], '
            'env: ["HOME"], write: true },\n'
            '  deny: { read: ["/data/secret"], net: ["api.example.com:25"] },\n'
            '};\n'
            'const t = (k, x) => console.log(k, x, isAllowed(perms, k, x));\n'
            't("read", "/data/a.txt"); t("read", "/data"); t("read", "/database"); t("read", '
            '"/data/secret"); t("read", "/data/secret/k"); t("read", "/etc/app/cfg"); t("read", '
            '"/etc/passwd");\n'
            't("net", "api.example.com"); t("net", "api.example.com:443"); t("net", '
            '"api.example.com:25"); t("net", "localhost:8080"); t("net", "localhost:9"); t("net", '
            '"evil.com");\n'
            't("env", "HOME"); t("env", "PATH"); t("write", "/anything"); t("run", "ls");\n',
  'hint': 'Функция matches(kind, entry, target) и порядок проверок: deny, затем allow.',
  'expected': ['read /data/a.txt true',
               'read /data true',
               'read /database false',
               'read /data/secret false',
               'read /data/secret/k false',
               'read /etc/app/cfg true',
               'read /etc/passwd false',
               'net api.example.com true',
               'net api.example.com:443 true',
               'net api.example.com:25 false',
               'net localhost:8080 true',
               'net localhost:9 false',
               'net evil.com false',
               'env HOME true',
               'env PATH false',
               'write /anything true',
               'run ls false']},
 {'id': 'j23-perm-flags',
  'mode': 'js',
  'title': 'Разбор флагов прав',
  'statement': 'Напишите parsePermissionFlags(args): args — массив строк командной строки. '
               'Распознаются флаги --allow-KIND и --deny-KIND (KIND: read, write, net, env, run), '
               'с необязательным значением «=a,b» (список через запятую). Без значения — true '
               '(всё). Результат: { allowAll, allow: {…}, deny: {…} }: allowAll — true, если '
               'встретился --allow-all или -A; в allow/deny попадают только упомянутые виды (в '
               'порядке первого упоминания). Повторы объединяются в один массив; если хотя бы раз '
               'флаг был без значения — true. Остальные аргументы игнорируются.',
  'starter': 'function parsePermissionFlags(args) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (a) => console.log(JSON.stringify(parsePermissionFlags(a)));\n'
            'show(["--allow-read=/a,/b", "app.ts"]);\n'
            'show(["--allow-net", "--deny-net=evil.com", "--allow-env=HOME"]);\n'
            'show(["--allow-read=/a", "--allow-read=/b", "--allow-read=/a"]);\n'
            'show(["--allow-read=/a", "--allow-read"]);\n'
            'show(["--allow-read", "--allow-read=/x"]);\n'
            'show(["-A", "--deny-write=/etc"]);\n'
            'show(["--allow-all"]);\n'
            'show(["--foo", "--allow-gpu", "x.js"]);\n'
            'show([]);\n',
  'hint': 'Регулярка /^--(allow|deny)-(read|write|net|env|run)(?:=(.*))?$/; для объединения '
          'учитывайте true.',
  'expected': ['{"allowAll":false,"allow":{"read":["/a","/b"]},"deny":{}}',
               '{"allowAll":false,"allow":{"net":true,"env":["HOME"]},"deny":{"net":["evil.com"]}}',
               '{"allowAll":false,"allow":{"read":["/a","/b"]},"deny":{}}',
               '{"allowAll":false,"allow":{"read":true},"deny":{}}',
               '{"allowAll":false,"allow":{"read":true},"deny":{}}',
               '{"allowAll":true,"allow":{},"deny":{"write":["/etc"]}}',
               '{"allowAll":true,"allow":{},"deny":{}}',
               '{"allowAll":false,"allow":{},"deny":{}}',
               '{"allowAll":false,"allow":{},"deny":{}}']},
 {'id': 'j23-runner',
  'mode': 'js',
  'title': 'Мини-раннер тестов',
  'statement': 'Напишите createRunner(): возвращает { test, beforeEach, afterEach, run }. '
               'test(name, fn, { timeout = 100 } = {}) регистрирует тест; beforeEach/afterEach(fn) '
               '— хуки для всех тестов. run() (async) выполняет тесты строго по очереди в порядке '
               'регистрации и возвращает массив { name, status, error? }: перед тестом вызываются '
               "хуки beforeEach, после — afterEach (даже если тест упал). status — 'pass', 'fail' "
               "(fn или хук бросили исключение/отклонили промис; error — сообщение) или 'timeout' "
               "(fn не завершилась за timeout мс; error — 'timeout').",
  'starter': 'function createRunner() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const r = createRunner();\n'
            'const log = [];\n'
            'r.beforeEach(() => log.push("before"));\n'
            'r.afterEach(() => log.push("after"));\n'
            'r.test("ok", () => { log.push("ok"); });\n'
            'r.test("async ok", async () => { await new Promise((x) => setTimeout(x, 5)); '
            'log.push("async"); });\n'
            'r.test("fails", () => { throw new Error("boom"); });\n'
            'r.test("rejects", async () => { throw new Error("late boom"); });\n'
            'r.test("slow", () => new Promise((x) => setTimeout(x, 200)), { timeout: 30 });\n'
            'r.test("after slow", () => { log.push("last"); });\n'
            'const res = await r.run();\n'
            'console.log(JSON.stringify(res));\n'
            'console.log(log.join(" "));\n',
  'hint': 'Promise.race между вызовом fn и таймером; не забудьте очистить таймер.',
  'expected': ['[{"name":"ok","status":"pass"},{"name":"async '
               'ok","status":"pass"},{"name":"fails","status":"fail","error":"boom"},{"name":"rejects","status":"fail","error":"late '
               'boom"},{"name":"slow","status":"timeout","error":"timeout"},{"name":"after '
               'slow","status":"pass"}]',
               'before ok after before async after before after before after before after before '
               'last after']},
 {'id': 'j23-describe',
  'mode': 'js',
  'title': 'describe и it',
  'statement': 'Напишите collectTests(build): build — функция (describe, it) => …, которая '
               'описывает тесты. describe(name, fn) вызывает fn сразу и вкладывает имена; it(name, '
               'fn) регистрирует тест. collectTests возвращает массив полных имён в порядке '
               'регистрации, части соединены « › » (пробел, стрелка, пробел). Тест вне describe '
               'имеет просто своё имя.',
  'starter': 'function collectTests(build) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const names = collectTests((describe, it) => {\n'
            '  it("top", () => {});\n'
            '  describe("cart", () => {\n'
            '    it("empty", () => {});\n'
            '    describe("with items", () => {\n'
            '      it("sums", () => {});\n'
            '      it("counts", () => {});\n'
            '    });\n'
            '    it("clears", () => {});\n'
            '  });\n'
            '  describe("empty group", () => {});\n'
            '  describe("b", () => { it("x", () => {}); });\n'
            '});\n'
            'console.log(JSON.stringify(names));\n'
            'console.log(JSON.stringify(collectTests(() => {})));\n',
  'hint': 'Стек имён: describe кладёт имя, вызывает fn, снимает имя.',
  'expected': ['["top","cart › empty","cart › with items › sums","cart › with items › '
               'counts","cart › clears","b › x"]',
               '[]']},
 {'id': 'j23-deep-equal',
  'mode': 'js',
  'title': 'Глубокое сравнение',
  'statement': 'Напишите deepEqual(a, b). Примитивы сравниваются как Object.is (NaN равен NaN, +0 '
               'не равен -0). Массивы — по длине и поэлементно. Объекты — по набору собственных '
               'перечислимых ключей (порядок не важен) и значениям. Date — по getTime(), RegExp — '
               'по toString(), Map — по размеру и парам (ключи сравниваются Object.is, значения '
               'глубоко), Set — по размеру и вхождению каждого элемента-примитива (для объектов в '
               'Set можно искать глубоким равным). Значения разных видов (массив и объект, Date и '
               'объект и т.д.) не равны.',
  'starter': 'function deepEqual(a, b) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const c = (a, b) => console.log(deepEqual(a, b));\n'
            'c(1, 1); c(NaN, NaN); c(0, -0); c("a", "a"); c(null, undefined);\n'
            'c([1, [2, 3]], [1, [2, 3]]); c([1, 2], [1, 2, 3]); c([1, 2], { 0: 1, 1: 2 });\n'
            'c({ a: 1, b: { c: 2 } }, { b: { c: 2 }, a: 1 }); c({ a: 1 }, { a: 1, b: undefined }); '
            'c({ a: 1 }, { a: 2 });\n'
            'c(new Date(5), new Date(5)); c(new Date(5), new Date(6)); c(/a/g, /a/g); c(/a/g, '
            '/a/i);\n'
            'c(new Map([[1, { x: 1 }]]), new Map([[1, { x: 1 }]])); c(new Map([[1, 1]]), new '
            'Map([[1, 2]]));\n'
            'c(new Set([1, 2, 3]), new Set([3, 2, 1])); c(new Set([1]), new Set([2])); c(new '
            'Set([{ a: 1 }]), new Set([{ a: 1 }]));\n'
            'c(new Date(5), {}); c([], {});\n',
  'hint': 'Сначала Object.is, затем разбор по Array.isArray, instanceof Date/RegExp/Map/Set и '
          'объектам.',
  'expected': ['true',
               'true',
               'false',
               'true',
               'false',
               'true',
               'false',
               'false',
               'true',
               'false',
               'false',
               'true',
               'false',
               'true',
               'false',
               'true',
               'false',
               'true',
               'false',
               'true',
               'false',
               'false']},
 {'id': 'j23-assert-throws',
  'mode': 'js',
  'title': 'assertThrows и assertRejects',
  'statement': 'Напишите assertThrows(fn, expected) и async assertRejects(promiseOrFn, expected). '
               'Они проверяют, что fn бросила исключение (rejects — что промис, или результат '
               'вызова функции, отклонён). expected: класс ошибки (проверка instanceof), RegExp '
               '(проверка message), строка (message включает её) или не задан (подходит любое). '
               "Успех — вернуть true. Если исключения не было — бросить Error('Missing expected "
               "exception'); если ошибка не подошла под expected — бросить Error('Unexpected "
               "error: ' + message ошибки).",
  'starter': 'function assertThrows(fn, expected) {\n'
             '}\n'
             'async function assertRejects(promiseOrFn, expected) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'class MyErr extends Error {}\n'
            'const t = async (f) => { try { console.log(await f()); } catch (e) { console.log("!" '
            '+ e.message); } };\n'
            'await t(() => assertThrows(() => { throw new Error("boom"); }));\n'
            'await t(() => assertThrows(() => { throw new MyErr("x"); }, MyErr));\n'
            'await t(() => assertThrows(() => { throw new Error("x"); }, MyErr));\n'
            'await t(() => assertThrows(() => { throw new Error("hello world"); }, /wor/));\n'
            'await t(() => assertThrows(() => { throw new Error("hello world"); }, "world"));\n'
            'await t(() => assertThrows(() => { throw new Error("hello"); }, "bye"));\n'
            'await t(() => assertThrows(() => 1));\n'
            'await t(() => assertRejects(Promise.reject(new TypeError("t")), TypeError));\n'
            'await t(() => assertRejects(async () => { throw new Error("late"); }, /late/));\n'
            'await t(() => assertRejects(Promise.resolve(1)));\n'
            'await t(() => assertRejects(() => Promise.reject(new Error("a")), "b"));\n',
  'hint': 'Общий matcher(err, expected); для rejects: await, затем try/catch.',
  'expected': ['true',
               'true',
               '!Unexpected error: x',
               'true',
               'true',
               '!Unexpected error: hello',
               '!Missing expected exception',
               'true',
               'true',
               '!Missing expected exception',
               '!Unexpected error: a']},
 {'id': 'j23-mock-fn',
  'mode': 'js',
  'title': 'Функция-заглушка',
  'statement': 'Напишите mockFn(impl). Возвращаемая функция f вызывает impl (если он задан) и '
               'возвращает его результат; иначе undefined. У f есть: f.calls — массив массивов '
               "аргументов; f.results — массив { type: 'return', value } или { type: 'throw', "
               'value } (исключение перебрасывается дальше); f.returnOnce(v) — очередной вызов '
               'вернёт v вместо вызова impl (несколько вызовов returnOnce образуют очередь); '
               'f.reset() — очищает calls, results и очередь.',
  'starter': 'function mockFn(impl) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const f = mockFn((a, b) => a + b);\n'
            'console.log(f(1, 2), f(3, 4));\n'
            'console.log(JSON.stringify(f.calls), JSON.stringify(f.results));\n'
            'f.returnOnce(100); f.returnOnce(200);\n'
            'console.log(f(1, 1), f(1, 1), f(1, 1));\n'
            'const g = mockFn(() => { throw new Error("bad"); });\n'
            'try { g(5); } catch (e) { console.log("caught", e.message); }\n'
            'console.log(JSON.stringify(g.calls), g.results[0].type, g.results[0].value.message);\n'
            'const h = mockFn();\n'
            'console.log(h(1), h.results.length);\n'
            'f.reset();\n'
            'console.log(f.calls.length, f.results.length, f(5, 5));\n',
  'hint': 'Храните очередь onceValues; в f проверяйте её перед вызовом impl.',
  'expected': ['3 7',
               '[[1,2],[3,4]] [{"type":"return","value":3},{"type":"return","value":7}]',
               '100 200 2',
               'caught bad',
               '[[5]] throw bad',
               'undefined 1',
               '0 0 10']},
 {'id': 'j23-spy-on',
  'mode': 'js',
  'title': 'spyOn и restore',
  'statement': 'Напишите spyOn(obj, method): подменяет obj[method] обёрткой, которая вызывает '
               'оригинал (с тем же this и аргументами), возвращает его результат и записывает '
               'вызовы. Возвращает объект шпиона: spy.calls — массив { args, result } (для '
               'бросившего исключение вызова — { args, error }, исключение пробрасывается), '
               'spy.restore() — возвращает оригинальный метод. Обёртка доступна как obj[method].',
  'starter': 'function spyOn(obj, method) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const counter = { n: 0, inc(by) { this.n += by; return this.n; }, fail() { throw new '
            'Error("nope"); } };\n'
            'const spy = spyOn(counter, "inc");\n'
            'console.log(counter.inc(2), counter.inc(3), counter.n);\n'
            'console.log(JSON.stringify(spy.calls));\n'
            'const spy2 = spyOn(counter, "fail");\n'
            'try { counter.fail(1); } catch (e) { console.log("caught", e.message); }\n'
            'console.log(spy2.calls.length, spy2.calls[0].error.message, '
            'JSON.stringify(spy2.calls[0].args));\n'
            'const wrapped = counter.inc;\n'
            'spy.restore();\n'
            'console.log(counter.inc !== wrapped, counter.inc(1), spy.calls.length);\n',
  'hint': 'const orig = obj[method]; obj[method] = function (...args) { … orig.apply(this, args) … '
          '}.',
  'expected': ['2 5 5',
               '[{"args":[2],"result":2},{"args":[3],"result":5}]',
               'caught nope',
               '1 nope [1]',
               'true 6 2']},
 {'id': 'j23-fake-clock',
  'mode': 'js',
  'title': 'Поддельные таймеры',
  'statement': 'Напишите createFakeClock(): { now, setTimeout, setInterval, clear, advance }. '
               'now() — текущее поддельное время (сначала 0). setTimeout(fn, ms) и setInterval(fn, '
               'ms) возвращают числовой id (1, 2, 3…) и планируют fn на now + ms; clear(id) '
               'отменяет. advance(ms) двигает время вперёд до now + ms, запуская все подошедшие '
               'таймеры по порядку времени (при равном времени — по id); на момент запуска now() '
               'равен времени срабатывания таймера. Таймеры, поставленные во время advance, тоже '
               'срабатывают, если успевают; интервал с ms ≤ 0 считайте ms = 1.',
  'starter': 'function createFakeClock() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const c = createFakeClock();\n'
            'const log = [];\n'
            'c.setTimeout(() => log.push("t100@" + c.now()), 100);\n'
            'const iv = c.setInterval(() => log.push("i30@" + c.now()), 30);\n'
            'c.setTimeout(() => { log.push("t50@" + c.now()); c.setTimeout(() => '
            'log.push("nested@" + c.now()), 20); }, 50);\n'
            'c.advance(60);\n'
            'console.log(log.join(" "), c.now());\n'
            'c.advance(60);\n'
            'console.log(log.join(" "), c.now());\n'
            'c.clear(iv);\n'
            'c.advance(100);\n'
            'console.log(log.length, c.now());\n'
            'const id = c.setTimeout(() => log.push("never"), 10);\n'
            'c.clear(id);\n'
            'c.advance(50);\n'
            'console.log(log.includes("never"), id);\n',
  'hint': 'Список таймеров; в цикле выбирайте ближайший с time ≤ target; после срабатывания '
          'интервала переносите его на time + ms.',
  'expected': ['i30@30 t50@50 i30@60 60',
               'i30@30 t50@50 i30@60 nested@70 i30@90 t100@100 i30@120 120',
               '7 220',
               'false 5']},
 {'id': 'j23-case-names',
  'mode': 'js',
  'title': 'Имена тестов из таблицы',
  'statement': 'Напишите caseNames(name, cases): cases — массив случаев { args, expected }. '
               'Верните массив имён вида `${name} #${номер с 1}: ${args через «, »} → '
               '${expected}`; строки в аргументах и результате берите в двойные кавычки '
               '(JSON.stringify), остальные значения приводите String(); для undefined и null — '
               'слова undefined и null. Массив-аргумент выводите через JSON.stringify.',
  'starter': 'function caseNames(name, cases) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(JSON.stringify(caseNames("parse", [\n'
            '  { args: ["1"], expected: 1 },\n'
            '  { args: ["", 10], expected: NaN },\n'
            '  { args: [[1, 2]], expected: "x" },\n'
            '  { args: [null, undefined], expected: null },\n'
            '  { args: [true, 0.5], expected: false },\n'
            '  { args: [], expected: undefined },\n'
            '])));\n'
            'console.log(JSON.stringify(caseNames("f", [])));\n',
  'hint': "Функция show(v): typeof v === 'string' ? JSON.stringify(v) : Array.isArray(v) || (v && "
          "typeof v === 'object') ? JSON.stringify(v) : String(v).",
  'expected': ['["parse #1: \\"1\\" → 1","parse #2: \\"\\", 10 → NaN","parse #3: [1,2] → '
               '\\"x\\"","parse #4: null, undefined → null","parse #5: true, 0.5 → false","parse '
               '#6:  → undefined"]',
               '[]']},
 {'id': 'j23-snapshot',
  'mode': 'js',
  'title': 'Сериализация для снимков',
  'statement': 'Напишите serialize(value): стабильное текстовое представление для снимков. Строки '
               '— JSON.stringify; числа, логические, null, undefined — как есть (NaN, -0 → «-0», '
               'Infinity); bigint — число с суффиксом n; Date — «Date(ISO)»; функции — «[Function '
               'имя]» («anonymous» для безымянных); массив — «[» элементы «]» с отступом 2 пробела '
               'на уровень, каждый элемент на своей строке; объект — «{» строки «ключ: значение» '
               '(ключи по алфавиту) «}»; пустой массив — «[]», пустой объект — «{}»; Map — «Map '
               '{…}» с записями «ключ => значение» в порядке вставки, Set — «Set […]». После '
               'элементов запятых нет.',
  'starter': 'function serialize(value, indent = 0) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(serialize({ b: 1, a: "x", c: [1, { z: null, y: undefined }], d: {} , e: '
            '[] }));\n'
            'console.log(serialize([NaN, -0, 0, Infinity, 10n, true]));\n'
            'console.log(serialize({ f() {}, g: () => 1, h: function named() {}, d: new Date(0) '
            '}));\n'
            'console.log(serialize(new Map([["k", { a: 1 }], [2, [3]]])));\n'
            'console.log(serialize(new Set([1, "a"])));\n'
            'console.log(serialize("текст"));\n',
  'hint': 'Рекурсия с уровнем отступа; единый helper pad(n).',
  'expected': ['{',
               '  a: "x"',
               '  b: 1',
               '  c: [',
               '    1',
               '    {',
               '      y: undefined',
               '      z: null',
               '    }',
               '  ]',
               '  d: {}',
               '  e: []',
               '}',
               '[',
               '  NaN',
               '  -0',
               '  0',
               '  Infinity',
               '  10n',
               '  true',
               ']',
               '{',
               '  d: Date(1970-01-01T00:00:00.000Z)',
               '  f: [Function f]',
               '  g: [Function g]',
               '  h: [Function named]',
               '}',
               'Map {',
               '  "k" => {',
               '    a: 1',
               '  }',
               '  2 => [',
               '    3',
               '  ]',
               '}',
               'Set [',
               '  1',
               '  "a"',
               ']',
               '"текст"']},
 {'id': 'j23-coverage',
  'mode': 'js',
  'title': 'Покрытие по строкам',
  'statement': 'Напишите coverage(files, executed): files — { путь: [номера исполняемых строк] }, '
               'executed — { путь: [номера выполненных строк] } (может содержать лишние номера и '
               'не содержать файла). Результат: { files: { путь: { covered, total, pct } }, total: '
               '{ covered, total, pct } }. covered — число исполняемых строк, попавших в executed '
               '(без дублей); pct — процент с округлением до 2 знаков (для total = 0 — 100). В '
               'total — суммы по файлам. Затем напишите meetsThreshold(result, min): вернуть { ok, '
               'failing } — ok, если total.pct ≥ min и каждый файл ≥ min; failing — '
               'отсортированные пути файлов ниже min.',
  'starter': 'function coverage(files, executed) {\n}\nfunction meetsThreshold(result, min) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const files = { "a.js": [1, 2, 3, 4], "b.js": [1, 2], "c.js": [] };\n'
            'const res = coverage(files, { "a.js": [1, 2, 2, 9], "b.js": [1, 2] });\n'
            'console.log(JSON.stringify(res));\n'
            'console.log(JSON.stringify(meetsThreshold(res, 50)));\n'
            'console.log(JSON.stringify(meetsThreshold(res, 80)));\n'
            'console.log(JSON.stringify(meetsThreshold(coverage({ x: [1] }, {}), 1)));\n'
            'console.log(JSON.stringify(coverage({}, {})));\n',
  'hint': 'Set из executed[path]; pct = Math.round(covered / total * 10000) / 100.',
  'expected': ['{"files":{"a.js":{"covered":2,"total":4,"pct":50},"b.js":{"covered":2,"total":2,"pct":100},"c.js":{"covered":0,"total":0,"pct":100}},"total":{"covered":4,"total":6,"pct":66.67}}',
               '{"ok":true,"failing":[]}',
               '{"ok":false,"failing":["a.js"]}',
               '{"ok":false,"failing":["x"]}',
               '{"files":{},"total":{"covered":0,"total":0,"pct":100}}']},
 {'id': 'j23-bench-stats',
  'mode': 'js',
  'title': 'Статистика замеров',
  'statement': 'Напишите stats(samples): samples — массив чисел (мс). Результат { n, min, max, '
               'mean, median, p95, stddev }; пустой массив — null. Все дробные числа округляются '
               'до 3 знаков. median — для чётного n среднее двух средних. p95 — метод ближайшего '
               'ранга: элемент отсортированного массива с рангом ceil(0.95 × n) (ранг считается с '
               '1). stddev — стандартное отклонение генеральной совокупности (деление на n). Не '
               'изменяйте входной массив.',
  'starter': 'function stats(samples) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (a) => console.log(JSON.stringify(stats(a)));\n'
            'show([5, 1, 3, 2, 4]);\n'
            'show([10, 20, 30, 40]);\n'
            'show([1.5, 2.5]);\n'
            'show([7]);\n'
            'show([]);\n'
            'show(Array.from({ length: 20 }, (_, i) => i + 1));\n'
            'const arr = [3, 1, 2]; stats(arr); console.log(arr.join(","));\n',
  'hint': 'Скопируйте и отсортируйте; round3 = x => Math.round(x * 1000) / 1000.',
  'expected': ['{"n":5,"min":1,"max":5,"mean":3,"median":3,"p95":5,"stddev":1.414}',
               '{"n":4,"min":10,"max":40,"mean":25,"median":25,"p95":40,"stddev":11.18}',
               '{"n":2,"min":1.5,"max":2.5,"mean":2,"median":2,"p95":2.5,"stddev":0.5}',
               '{"n":1,"min":7,"max":7,"mean":7,"median":7,"p95":7,"stddev":0}',
               'null',
               '{"n":20,"min":1,"max":20,"mean":10.5,"median":10.5,"p95":19,"stddev":5.766}',
               '3,1,2']},
 {'id': 'j23-bench-run',
  'mode': 'js',
  'title': 'Запуск бенчмарка с прогревом',
  'statement': 'Напишите bench(fn, { warmup, iterations }, now): now — функция текущего времени в '
               'мс (внедряется для детерминированности). Сначала warmup вызовов fn без замеров, '
               'затем iterations замеренных: для каждого сэмпл = now() после − now() до. '
               'Результат: { samples, median } (median — медиана сэмплов, для чётного числа — '
               'среднее двух средних, для пустого — null). Поддержка async не нужна.',
  'starter': 'function bench(fn, opts, now) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'let t = 0;\n'
            'const durations = [9, 5, 2, 1, 1, 1, 1, 1];\n'
            'let call = 0;\n'
            'const fn = () => { t += durations[Math.min(call++, durations.length - 1)]; };\n'
            'const now = () => t;\n'
            'console.log(JSON.stringify(bench(fn, { warmup: 3, iterations: 5 }, now)));\n'
            'call = 0; t = 0;\n'
            'console.log(JSON.stringify(bench(fn, { warmup: 0, iterations: 4 }, now)));\n'
            'console.log(JSON.stringify(bench(fn, { warmup: 2, iterations: 0 }, now)));\n',
  'hint': 'Два цикла: прогрев и замеры; медиану считайте по отсортированной копии.',
  'expected': ['{"samples":[1,1,1,1,1],"median":1}',
               '{"samples":[9,5,2,1],"median":3.5}',
               '{"samples":[],"median":null}']},
 {'id': 'j23-tap',
  'mode': 'js',
  'title': 'Отчёт в формате TAP',
  'statement': 'Напишите formatTap(results): results — массив { name, status, error? }, status — '
               "'pass', 'fail', 'skip'. Возвращает массив строк. Первая — «1..N». Затем для "
               'каждого теста с номером i (с 1): «ok i - name» для pass, «not ok i - name» для '
               'fail, «ok i - name # SKIP» для skip. После «not ok» с error добавьте три строки: '
               '«  ---», «  message: error», «  ...». Последняя строка: «# pass P», затем «# fail '
               'F» (пропущенные в P не входят). Пустой список даёт «1..0», «# pass 0», «# fail 0».',
  'starter': 'function formatTap(results) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(formatTap([\n'
            '  { name: "adds", status: "pass" },\n'
            '  { name: "divides", status: "fail", error: "division by zero" },\n'
            '  { name: "later", status: "skip" },\n'
            '  { name: "bare fail", status: "fail" },\n'
            ']).join("\\n"));\n'
            'console.log(formatTap([]).join("|"));\n',
  'hint': 'Соберите массив lines и push по порядку; счётчики pass/fail считайте в цикле.',
  'expected': ['1..4',
               'ok 1 - adds',
               'not ok 2 - divides',
               '  ---',
               '  message: division by zero',
               '  ...',
               'ok 3 - later # SKIP',
               'not ok 4 - bare fail',
               '# pass 1',
               '# fail 2',
               '1..0|# pass 0|# fail 0']},
 {'id': 'j23-filter-tests',
  'mode': 'js',
  'title': 'Фильтр тестов по имени',
  'statement': 'Напишите filterTests(tests, { pattern, only }): tests — массив { name, only? }. '
               'Если среди тестов есть хотя бы один с only: true и опция only включена (opts.only '
               '=== true), оставьте только такие тесты. Затем, если задан pattern (строка — тело '
               'регулярного выражения), оставьте тесты, имя которых подходит под RegExp(pattern, '
               "'i'). Порядок сохраняется. Возвращает массив имён.",
  'starter': 'function filterTests(tests, opts) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const tests = [\n'
            '  { name: "parse number" }, { name: "Parse string", only: true }, { name: "format '
            'date" }, { name: "parse date", only: true }, { name: "misc" },\n'
            '];\n'
            'const f = (o) => console.log(JSON.stringify(filterTests(tests, o)));\n'
            'f({}); f({ only: true }); f({ pattern: "parse" }); f({ pattern: "^parse", only: true '
            '}); f({ pattern: "DATE" }); f({ pattern: "nothing" }); f({ pattern: "" });\n'
            'console.log(JSON.stringify(filterTests([{ name: "a" }, { name: "b" }], { only: true '
            '})));\n',
  'hint': 'Сначала фильтр по only, потом по регулярному выражению; пустой pattern считать '
          'незаданным.',
  'expected': ['["parse number","Parse string","format date","parse date","misc"]',
               '["Parse string","parse date"]',
               '["parse number","Parse string","parse date"]',
               '["Parse string","parse date"]',
               '["format date","parse date"]',
               '[]',
               '["parse number","Parse string","format date","parse date","misc"]',
               '["a","b"]']},
 {'id': 'j23-with-timeout',
  'mode': 'js',
  'title': 'Промис с таймаутом',
  'statement': 'Напишите withTimeout(promise, ms): возвращает промис с результатом promise, если '
               "он успел за ms миллисекунд; иначе отклоняется с Error('timeout after Nms') (N — "
               'ms). Если promise отклонился раньше — пробросить его ошибку. Таймер должен быть '
               'очищен, как только результат известен (процесс не должен висеть).',
  'starter': 'function withTimeout(promise, ms) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const sleep = (ms, v, fail) => new Promise((res, rej) => setTimeout(() => (fail ? '
            'rej(new Error(v)) : res(v)), ms));\n'
            'const t = async (p) => { try { console.log(await p); } catch (e) { console.log("!" + '
            'e.message); } };\n'
            'await t(withTimeout(sleep(10, "fast"), 100));\n'
            'await t(withTimeout(sleep(100, "slow"), 20));\n'
            'await t(withTimeout(sleep(5, "oops", true), 100));\n'
            'await t(withTimeout(Promise.resolve(7), 50));\n'
            'await t(withTimeout(sleep(50, "x"), 0));\n'
            'console.log("end");\n',
  'hint': 'new Promise + setTimeout + promise.then(resolve, reject); clearTimeout в обоих случаях.',
  'expected': ['fast', '!timeout after 20ms', '!oops', '7', '!timeout after 0ms', 'end']},
 {'id': 'j23-map-limit',
  'mode': 'js',
  'title': 'Параллельность с пределом',
  'statement': 'Напишите async mapLimit(items, limit, fn): применяет асинхронную fn(item, index) '
               'ко всем элементам, одновременно выполняя не более limit вызовов; результаты '
               'возвращаются в порядке исходного массива. Если какой-то вызов отклонился — промис '
               'mapLimit отклоняется с его ошибкой (новые вызовы можно не запускать). limit меньше '
               '1 считайте равным 1.',
  'starter': 'async function mapLimit(items, limit, fn) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'let running = 0, peak = 0;\n'
            'const fn = async (x) => { running++; peak = Math.max(peak, running); await new '
            'Promise((r) => setTimeout(r, 10 * (x % 3 + 1))); running--; return x * 2; };\n'
            'const out = await mapLimit([1, 2, 3, 4, 5, 6, 7], 3, fn);\n'
            'console.log(out.join(","), peak);\n'
            'running = peak = 0;\n'
            'console.log((await mapLimit([1, 2, 3], 1, fn)).join(","), peak);\n'
            'console.log((await mapLimit([1, 2], 10, fn)).join(","), (await mapLimit([], 2, '
            'fn)).length, (await mapLimit([5], 0, fn)).join(","));\n'
            'try { await mapLimit([1, 2, 3], 2, async (x) => { if (x === 2) throw new Error("bad " '
            '+ x); return x; }); } catch (e) { console.log(e.message); }\n',
  'hint': 'Пул «рабочих»: каждый берёт следующий индекс, пока они не закончатся; Promise.all по '
          'рабочим.',
  'expected': ['2,4,6,8,10,12,14 3', '2,4,6 1', '2,4 0 10', 'bad 2']},
 {'id': 'j23-detect-runtime',
  'mode': 'js',
  'title': 'Определение среды выполнения',
  'statement': 'Напишите detectRuntime(g): g — объект «глобального пространства». Проверки по '
               "порядку: если g.Deno?.version — 'deno'; иначе g.Bun?.version — 'bun'; иначе "
               "g.process?.versions?.node — 'node'; иначе есть g.window и g.document — 'browser'; "
               "иначе 'unknown'. Затем featureReport(g): объект с булевыми значениями для имён "
               'fetch, Request, Response, URL, AbortController, ReadableStream, structuredClone, '
               "EventTarget — true, если typeof g[имя] !== 'undefined'.",
  'starter': 'function detectRuntime(g) {\n}\nfunction featureReport(g) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const d = (g) => console.log(detectRuntime(g));\n'
            'd({ Deno: { version: { deno: "2" } }, process: { versions: { node: "22" } } });\n'
            'd({ Bun: { version: "1.1" }, process: { versions: { node: "22" } } });\n'
            'd({ process: { versions: { node: "22.1" } } });\n'
            'd({ window: {}, document: {} });\n'
            'd({ window: {} }); d({}); d({ Deno: {} });\n'
            'console.log(JSON.stringify(featureReport({ fetch() {}, URL: class {}, '
            'structuredClone() {} })));\n'
            'console.log(JSON.stringify(featureReport(globalThis)));\n',
  'hint': 'Опциональная цепочка ?. и список имён для featureReport.',
  'expected': ['deno',
               'bun',
               'node',
               'browser',
               'unknown',
               'unknown',
               'unknown',
               '{"fetch":true,"Request":false,"Response":false,"URL":true,"AbortController":false,"ReadableStream":false,"structuredClone":true,"EventTarget":false}',
               '{"fetch":true,"Request":true,"Response":true,"URL":true,"AbortController":true,"ReadableStream":true,"structuredClone":true,"EventTarget":true}']},
 {'id': 'j23-engines',
  'mode': 'js',
  'title': 'Проверка engines',
  'statement': 'Напишите satisfies(range, version) и checkEngines(engines, versions). Версии — '
               '«x», «x.y» или «x.y.z» (недостающие части — 0). range — один или несколько наборов '
               'через «||»; набор — компараторы через пробел (И); компаратор — оператор >=, >, <=, '
               '<, = (или без оператора — то же, что =) и версия. satisfies — true, если подходит '
               'хотя бы один набор. checkEngines(engines, versions): engines — { имя: range }, '
               'versions — { имя: версия }; вернуть отсортированный массив имён, для которых '
               'версия не подходит или версии нет в versions.',
  'starter': 'function satisfies(range, version) {\n'
             '}\n'
             'function checkEngines(engines, versions) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const s = (r, v) => console.log(JSON.stringify(r), v, satisfies(r, v));\n'
            's(">=18", "18.0.0"); s(">=18", "17.9.9"); s(">=18 <21", "20.5"); s(">=18 <21", "21"); '
            's("<2", "1.99.99");\n'
            's(">18", "18.0.0"); s(">18", "18.0.1"); s("22", "22.0.0"); s("=22.1", "22.1.0"); '
            's("<=1.5", "1.5.0"); s("<=1.5", "1.5.1");\n'
            's(">=18 <20 || >=22", "21"); s(">=18 <20 || >=22", "22.1"); s(">=18 <20 || >=22", '
            '"19");\n'
            'console.log(JSON.stringify(checkEngines({ node: ">=18", bun: ">=1.1", deno: "^2" , '
            'npm: ">=9 <11"}, { node: "20.1.0", bun: "1.0.30", npm: "10.2.0" })));\n'
            'console.log(JSON.stringify(checkEngines({}, { node: "20" })));\n',
  'hint': 'parseVersion → [x, y, z]; cmp сравнивает по частям; длинные операторы (>=, <=) '
          'проверяйте раньше коротких.',
  'expected': ['">=18" 18.0.0 true',
               '">=18" 17.9.9 false',
               '">=18 <21" 20.5 true',
               '">=18 <21" 21 false',
               '"<2" 1.99.99 true',
               '">18" 18.0.0 false',
               '">18" 18.0.1 true',
               '"22" 22.0.0 true',
               '"=22.1" 22.1.0 true',
               '"<=1.5" 1.5.0 true',
               '"<=1.5" 1.5.1 false',
               '">=18 <20 || >=22" 21 false',
               '">=18 <20 || >=22" 22.1 true',
               '">=18 <20 || >=22" 19 true',
               '["bun","deno"]',
               '[]']},
 {'id': 'j23-import-map',
  'mode': 'js',
  'title': 'Import map',
  'statement': 'Напишите resolveImport(specifier, importMap, base): importMap = { imports: { ключ: '
               'значение } }. Алгоритм: если specifier — абсолютный URL (есть схема вида «xxx:») — '
               'вернуть как есть; если начинается с «./», «../» или «/» — разрешить относительно '
               'base через new URL(...).href; иначе (голый) — искать в imports: точное совпадение '
               'ключа; иначе самый длинный ключ, оканчивающийся на «/» и являющийся префиксом '
               'specifier — заменить префикс значением. Результат отображения, начинающийся с '
               '«./», «../», «/», разрешается относительно base. Нет совпадения — бросить '
               'TypeError(\'Unmapped bare specifier "\' + specifier + \'"\').',
  'starter': 'function resolveImport(specifier, importMap, base) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const map = { imports: {\n'
            '  "lodash": "https://cdn.example/lodash@4/index.js",\n'
            '  "app/": "./src/",\n'
            '  "app/utils/": "./src/lib/utils/",\n'
            '  "react": "npm:react@18",\n'
            '} };\n'
            'const base = "https://site.example/app/main.js";\n'
            'const r = (s) => { try { console.log(s, "→", resolveImport(s, map, base)); } catch '
            '(e) { console.log(s, "!", e.message); } };\n'
            'r("lodash"); r("app/x.js"); r("app/utils/a.js"); r("react"); r("./local.js"); '
            'r("../up.js"); r("/abs.js");\n'
            'r("https://other.example/x.js"); r("npm:zod@3"); r("unknown"); r("lodash/fp");\n',
  'hint': 'Сначала проверьте схему регулярным выражением /^[a-z][a-z0-9+.-]*:/i; затем '
          'относительные пути; затем карту.',
  'expected': ['lodash → https://cdn.example/lodash@4/index.js',
               'app/x.js → https://site.example/app/src/x.js',
               'app/utils/a.js → https://site.example/app/src/lib/utils/a.js',
               'react → npm:react@18',
               './local.js → https://site.example/app/local.js',
               '../up.js → https://site.example/up.js',
               '/abs.js → https://site.example/abs.js',
               'https://other.example/x.js → https://other.example/x.js',
               'npm:zod@3 → npm:zod@3',
               'unknown ! Unmapped bare specifier "unknown"',
               'lodash/fp ! Unmapped bare specifier "lodash/fp"']},
 {'id': 'j23-classify-specifier',
  'mode': 'js',
  'title': 'Классификация спецификатора',
  'statement': 'Напишите classifySpecifier(spec). Результат — объект: для «npm:» и «jsr:» — { '
               'scheme, name, version, subpath }: после схемы идёт имя (для «@scope/pkg» — два '
               'сегмента), затем необязательное «@версия» (до «/» или конца), затем необязательный '
               'подпуть (начинается с «/»); отсутствующие части — null. Для «node:» — { scheme: '
               "'node', name } (имя — всё после «node:»). Для «http:» и «https:» — { scheme: 'url' "
               "}. Начинается с «./» или «../» — { scheme: 'relative' }; с «/» — { scheme: "
               "'absolute' }. Иначе — { scheme: 'bare', name: spec }.",
  'starter': 'function classifySpecifier(spec) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'for (const s of ["npm:lodash", "npm:lodash@4.17.21", "npm:lodash@4.17.21/fp", '
            '"npm:@scope/pkg", "npm:@scope/pkg@^1.2/sub/path", "jsr:@std/path@1", '
            '"jsr:@std/assert/equals", "node:fs", "node:fs/promises", "https://x.example/a.js", '
            '"http://y", "./a.js", "../b.js", "/abs/c.js", "lodash", "@scope/pkg/x"])\n'
            '  console.log(s, JSON.stringify(classifySpecifier(s)));\n',
  'hint': 'Регулярка для npm/jsr: ^(npm|jsr):((?:@[^/@]+/)?[^/@]+)(?:@([^/]+))?(/.*)?$',
  'expected': ['npm:lodash {"scheme":"npm","name":"lodash","version":null,"subpath":null}',
               'npm:lodash@4.17.21 '
               '{"scheme":"npm","name":"lodash","version":"4.17.21","subpath":null}',
               'npm:lodash@4.17.21/fp '
               '{"scheme":"npm","name":"lodash","version":"4.17.21","subpath":"/fp"}',
               'npm:@scope/pkg {"scheme":"npm","name":"@scope/pkg","version":null,"subpath":null}',
               'npm:@scope/pkg@^1.2/sub/path '
               '{"scheme":"npm","name":"@scope/pkg","version":"^1.2","subpath":"/sub/path"}',
               'jsr:@std/path@1 {"scheme":"jsr","name":"@std/path","version":"1","subpath":null}',
               'jsr:@std/assert/equals '
               '{"scheme":"jsr","name":"@std/assert","version":null,"subpath":"/equals"}',
               'node:fs {"scheme":"node","name":"fs"}',
               'node:fs/promises {"scheme":"node","name":"fs/promises"}',
               'https://x.example/a.js {"scheme":"url"}',
               'http://y {"scheme":"url"}',
               './a.js {"scheme":"relative"}',
               '../b.js {"scheme":"relative"}',
               '/abs/c.js {"scheme":"absolute"}',
               'lodash {"scheme":"bare","name":"lodash"}',
               '@scope/pkg/x {"scheme":"bare","name":"@scope/pkg/x"}']},
 {'id': 'j23-integrity',
  'mode': 'js',
  'title': 'Проверка целостности (SRI)',
  'statement': "Напишите makeIntegrity(content, alg = 'sha256') и verifyIntegrity(content, "
               'integrity) (node:crypto). makeIntegrity возвращает строку «алгоритм-base64 хеша '
               'UTF-8 содержимого», например «sha256-…». verifyIntegrity: integrity — один или '
               'несколько хешей через пробел; true, если содержимое подходит хотя бы под один '
               'известный (sha256, sha384, sha512) хеш; хеши неизвестных алгоритмов и некорректные '
               'записи игнорируются; пустая строка или отсутствие подходящих — false.',
  'starter': 'import { createHash } from "node:crypto";\n'
             'function makeIntegrity(content, alg = "sha256") {\n'
             '}\n'
             'function verifyIntegrity(content, integrity) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const a = makeIntegrity("hello");\n'
            'console.log(a);\n'
            'console.log(makeIntegrity("hello", "sha512").slice(0, 20));\n'
            'console.log(makeIntegrity("", "sha384"));\n'
            'console.log(verifyIntegrity("hello", a), verifyIntegrity("hellO", a), '
            'verifyIntegrity("hello", ""), verifyIntegrity("hello", "md5-xxx"));\n'
            'console.log(verifyIntegrity("hello", "sha256-AAAA " + a), verifyIntegrity("hello", '
            '"garbage " + makeIntegrity("hello", "sha512")), verifyIntegrity("x", "sha1-abc"));\n',
  'hint': "createHash(alg).update(content).digest('base64'); для verify — split(/\\s+/) и "
          'сравнение строк.',
  'expected': ['sha256-LPJNul+wow4m6DsqxbninhsWHlwfp0JecwQzYpOLmCQ=',
               'sha512-m3HSJL1i83hdl',
               'sha384-OLBgp1GsljhM2TJ+sbHjaiH9txEUvgdDTAzHv2P24donTt6/529l+9Ua0vFImLlb',
               'true false false false',
               'true true false']},
 {'id': 'j23-fetch-handler',
  'mode': 'js',
  'title': 'Переносимый обработчик Request → Response',
  'statement': 'Напишите async handle(request) на веб-стандартах (Request, Response, URL). GET '
               '/hello — текст «Hello, NAME» (NAME — параметр query name, по умолчанию «world»), '
               'Content-Type text/plain;charset=UTF-8 (по умолчанию для строки). GET /json — '
               'Response.json({ ok: true, path }) с путём запроса. Любой другой метод или путь — '
               'Response со статусом 404 и телом «Not Found». HEAD и прочие методы к /hello и '
               '/json тоже дают 404.',
  'starter': 'async function handle(request) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const r = async (m, u) => {\n'
            '  const res = await handle(new Request("http://x.test" + u, { method: m }));\n'
            '  console.log(m, u, res.status, res.headers.get("content-type"), await res.text());\n'
            '};\n'
            'await r("GET", "/hello"); await r("GET", "/hello?name=Аня"); await r("GET", "/json"); '
            'await r("GET", "/nope"); await r("POST", "/hello"); await r("HEAD", "/json");\n',
  'hint': 'const url = new URL(request.url); new Response(text) сам выставляет '
          'text/plain;charset=UTF-8.',
  'expected': ['GET /hello 200 text/plain;charset=UTF-8 Hello, world',
               'GET /hello?name=Аня 200 text/plain;charset=UTF-8 Hello, Аня',
               'GET /json 200 application/json {"ok":true,"path":"/json"}',
               'GET /nope 404 text/plain;charset=UTF-8 Not Found',
               'POST /hello 404 text/plain;charset=UTF-8 Not Found',
               'HEAD /json 404 text/plain;charset=UTF-8 Not Found']},
 {'id': 'j23-abort-timeout',
  'mode': 'js',
  'title': 'Отмена по таймауту (AbortController)',
  'statement': 'Напишите fetchWithTimeout(task, ms): task(signal) — async-функция, принимающая '
               'AbortSignal. Создайте AbortController, через ms миллисекунд вызовите abort() и '
               'передайте signal в task. Если task успела — вернуть её результат (и очистить '
               "таймер). Если сигнал сработал раньше — отклонить Error('aborted'), даже если task "
               'сама ничего не бросила позже (то есть результат не нужен). task, бросившая своё '
               'исключение до таймаута, пробрасывает его.',
  'starter': 'function fetchWithTimeout(task, ms) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const wait = (signal, ms, v) => new Promise((res, rej) => {\n'
            '  const t = setTimeout(() => res(v), ms);\n'
            '  signal.addEventListener("abort", () => { clearTimeout(t); rej(new Error("task saw '
            'abort")); });\n'
            '});\n'
            'const t = async (p) => { try { console.log(await p); } catch (e) { console.log("!" + '
            'e.message); } };\n'
            'await t(fetchWithTimeout((s) => wait(s, 10, "ok"), 100));\n'
            'await t(fetchWithTimeout((s) => wait(s, 100, "late"), 20));\n'
            'let seen;\n'
            'await t(fetchWithTimeout(async (s) => { seen = s; return new Promise(() => {}); }, '
            '20));\n'
            'console.log(seen.aborted);\n'
            'await t(fetchWithTimeout(async () => { throw new Error("own"); }, 100));\n',
  'hint': 'Promise.race между task(signal) и промисом, который отклоняется на событии abort '
          'сигнала.',
  'expected': ['ok', '!aborted', '!aborted', 'true', '!own']},
 {'id': 'j23-web-streams',
  'mode': 'js',
  'title': 'Web Streams: преобразование',
  'statement': 'Напишите async transformChunks(chunks, fn): chunks — массив значений; создайте '
               'ReadableStream из этих значений, пропустите через TransformStream, применяющий fn '
               'к каждому значению (fn может быть async), и прочитайте результат в массив через '
               'reader. Верните массив результатов в том же порядке. Исключение из fn должно '
               'отклонить итоговый промис.',
  'starter': 'async function transformChunks(chunks, fn) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(JSON.stringify(await transformChunks(["a", "b", "c"], (s) => '
            's.toUpperCase())));\n'
            'console.log(JSON.stringify(await transformChunks([1, 2, 3], async (x) => { await '
            'null; return x * x; })));\n'
            'console.log(JSON.stringify(await transformChunks([], (x) => x)));\n'
            'try { await transformChunks([1, 2, 3], (x) => { if (x === 2) throw new Error("bad " + '
            'x); return x; }); } catch (e) { console.log("!" + e.message); }\n',
  'hint': 'new ReadableStream({ start(c) { chunks.forEach(x => c.enqueue(x)); c.close(); } '
          '}).pipeThrough(new TransformStream({ async transform(ch, c) { c.enqueue(await fn(ch)); '
          '} })).',
  'expected': ['["A","B","C"]', '[1,4,9]', '[]', '!bad 2']},
 {'id': 'j23-event-bus',
  'mode': 'js',
  'title': 'Шина событий на EventTarget',
  'statement': 'Напишите createBus() на EventTarget и CustomEvent: возвращает { on, once, emit }. '
               'on(name, fn) подписывает fn(detail) и возвращает функцию отписки; once(name, fn) — '
               'подписка на одно срабатывание; emit(name, detail) рассылает событие синхронно и '
               'возвращает число подписчиков, получивших его (для once — только если сработал). '
               'События разных имён независимы.',
  'starter': 'function createBus() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const bus = createBus();\n'
            'const log = [];\n'
            'const off = bus.on("a", (d) => log.push("a1:" + d));\n'
            'bus.on("a", (d) => log.push("a2:" + d));\n'
            'bus.once("a", (d) => log.push("once:" + d));\n'
            'bus.on("b", (d) => log.push("b:" + d));\n'
            'console.log(bus.emit("a", 1));\n'
            'console.log(bus.emit("a", 2));\n'
            'off();\n'
            'console.log(bus.emit("a", 3));\n'
            'console.log(bus.emit("b", "x"), bus.emit("none", 0));\n'
            'console.log(log.join(" "));\n',
  'hint': 'Храните Map имя → число подписчиков либо считайте через собственные обёртки; '
          'CustomEvent(name, { detail }).',
  'expected': ['3', '2', '1', '1 0', 'a1:1 a2:1 once:1 a1:2 a2:2 a2:3 b:x']},
 {'id': 'j23-retry-test',
  'mode': 'js',
  'title': 'Повтор нестабильного теста',
  'statement': 'Напишите async runWithRetries(testFn, retries): запускает testFn(attempt) (attempt '
               'с 1), при исключении или отклонении повторяет, всего не более retries + 1 попыток. '
               'Возвращает { passed, attempts, error? }: passed — true при первой успешной попытке '
               '(attempts — её номер); если все провалились — passed: false, attempts = retries + '
               '1, error — сообщение последней ошибки. retries < 0 считайте нулём.',
  'starter': 'async function runWithRetries(testFn, retries) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const flaky = (okAt) => async (n) => { if (n < okAt) throw new Error("fail " + n); '
            '};\n'
            'console.log(JSON.stringify(await runWithRetries(flaky(1), 2)));\n'
            'console.log(JSON.stringify(await runWithRetries(flaky(3), 2)));\n'
            'console.log(JSON.stringify(await runWithRetries(flaky(4), 2)));\n'
            'console.log(JSON.stringify(await runWithRetries(flaky(2), 0)));\n'
            'console.log(JSON.stringify(await runWithRetries(() => { throw new Error("sync"); }, '
            '-5)));\n',
  'hint': 'Цикл по попыткам с try/catch и await; запомните сообщение последней ошибки.',
  'expected': ['{"passed":true,"attempts":1}',
               '{"passed":true,"attempts":3}',
               '{"passed":false,"attempts":3,"error":"fail 3"}',
               '{"passed":false,"attempts":1,"error":"fail 1"}',
               '{"passed":false,"attempts":1,"error":"sync"}']},
 {'id': 'j23-summary',
  'mode': 'js',
  'title': 'Сводка результатов тестов',
  'statement': 'Напишите summarize(results): results — массив { name, status, ms }, status — '
               "'pass', 'fail', 'skip'. Результат: { total, passed, failed, skipped, durationMs, "
               'failures } — durationMs — сумма ms (отсутствующее — 0), failures — имена упавших в '
               'порядке следования. Затем formatSummary(s): массив строк «tests N», «pass P», '
               '«fail F», «skipped S», «duration D ms»; если есть падения — после них «FAILED: '
               'имя1, имя2», иначе «OK».',
  'starter': 'function summarize(results) {\n}\nfunction formatSummary(s) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const res = [\n'
            '  { name: "a", status: "pass", ms: 12 }, { name: "b", status: "fail", ms: 30 }, { '
            'name: "c", status: "skip" },\n'
            '  { name: "d", status: "pass", ms: 8 }, { name: "e", status: "fail", ms: 1 },\n'
            '];\n'
            'const s = summarize(res);\n'
            'console.log(JSON.stringify(s));\n'
            'console.log(formatSummary(s).join(" | "));\n'
            'console.log(formatSummary(summarize([{ name: "x", status: "pass", ms: 5 }])).join(" | '
            '"));\n'
            'console.log(JSON.stringify(summarize([])));\n',
  'hint': 'Один проход reduce или цикл со счётчиками.',
  'expected': ['{"total":5,"passed":2,"failed":2,"skipped":1,"durationMs":51,"failures":["b","e"]}',
               'tests 5 | pass 2 | fail 2 | skipped 1 | duration 51 ms | FAILED: b, e',
               'tests 1 | pass 1 | fail 0 | skipped 0 | duration 5 ms | OK',
               '{"total":0,"passed":0,"failed":0,"skipped":0,"durationMs":0,"failures":[]}']},
 {'id': 'j23-diff-lines',
  'mode': 'js',
  'title': 'Различие снимков построчно',
  'statement': 'Напишите diffLines(a, b): a и b — многострочные строки (разделитель «\\n»). '
               'Верните массив строк-различий: «  » + строка для общих, «- » + строка для '
               'удалённых из a, «+ » + строка для добавленных в b. Используйте наибольшую общую '
               'подпоследовательность строк (LCS). Порядок обхода: пока обе строки есть — если '
               'a[i] === b[j], общая строка; иначе, если LCS без a[i] не меньше, чем LCS без b[j], '
               'выводится удаление a[i], иначе добавление b[j]; остатки — удаления a, затем '
               'добавления b.',
  'starter': 'function diffLines(a, b) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (a, b) => console.log(diffLines(a, b).join("|"));\n'
            'show("a\\nb\\nc", "a\\nb\\nc");\n'
            'show("a\\nb\\nc", "a\\nx\\nc");\n'
            'show("a\\nb", "a\\nb\\nc");\n'
            'show("a\\nb\\nc", "b");\n'
            'show("", "x");\n'
            'show("one\\ntwo\\nthree\\nfour", "one\\nthree\\nfour\\nfive");\n'
            'show("x\\ny", "y\\nx");\n',
  'hint': 'Таблица lcs[i][j] для суффиксов; затем проход по двум указателям по правилам из '
          'условия.',
  'expected': ['  a|  b|  c',
               '  a|- b|+ x|  c',
               '  a|  b|+ c',
               '- a|  b|- c',
               '- |+ x',
               '  one|- two|  three|  four|+ five',
               '- x|  y|+ x']}]}
