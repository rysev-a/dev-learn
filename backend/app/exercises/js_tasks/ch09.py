"""Задачи книги «Современный Frontend», глава 9 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {9: [{'id': 'j9-resolve-relative',
      'mode': 'js',
      'title': 'Разрешение относительных путей модулей',
      'statement': 'Напишите функцию resolveRelative(from, spec): from — путь файла-импортёра '
                   '(«src/app/main.js»), spec — относительный путь («./util.js», «../lib/x.js», '
                   '«./a/./b/../c.js»); верните нормализованный путь без «.» и «..» (например, '
                   '«src/app/util.js»). Если spec не начинается с «./» или «../» — бросьте TypeError("голое '
                   'имя"). Если путь уходит выше корня («../../../x.js» из «a/b.js») — Error("выше корня").',
      'starter': 'function resolveRelative(from, spec) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const f = "src/app/main.js";\n'
                'for (const s of ["./util.js", "../lib/x.js", "./a/./b/../c.js", "../../top.js", '
                '"./deep/er/f.js"]) console.log(resolveRelative(f, s));\n'
                'for (const [from, s] of [[f, "lodash"], ["a/b.js", "../../../x.js"], [f, "/abs.js"]]) { try '
                '{ console.log(resolveRelative(from, s)); } catch (e) { console.log(e.name, e.message); } }\n'
                'console.log(resolveRelative("main.js", "./x.js"));\n',
      'hint': 'Разбейте путь импортёра на папки, пройдите по сегментам spec: «..» убирает папку, «.» '
              'пропускается.',
      'expected': ['src/app/util.js',
                   'src/lib/x.js',
                   'src/app/a/c.js',
                   'top.js',
                   'src/app/deep/er/f.js',
                   'TypeError голое имя',
                   'Error выше корня',
                   'TypeError голое имя',
                   'x.js']},
     {'id': 'j9-resolve-bare',
      'mode': 'js',
      'title': 'Поиск пакета в node_modules',
      'statement': 'Файловая система задана множеством путей (массив строк-файлов). Напишите функцию '
                   'resolveBare(name, fromDir, files): ищет файл «<папка>/node_modules/<name>/index.js» (или '
                   '«<name>.js» прямо в node_modules), начиная с fromDir и поднимаясь к корню (пустая строка '
                   '— корень), и возвращает первый найденный путь; если не нашёл — бросьте Error("Cannot '
                   'find package \'<name>\'").',
      'starter': 'function resolveBare(name, fromDir, files) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const files = ["node_modules/lodash/index.js", "app/node_modules/react/index.js", '
                '"app/src/node_modules/local.js", "node_modules/@scope/pkg/index.js"];\n'
                'console.log(resolveBare("lodash", "app/src/ui", files));\n'
                'console.log(resolveBare("react", "app/src/ui", files));\n'
                'console.log(resolveBare("react", "app", files));\n'
                'console.log(resolveBare("local", "app/src", files));\n'
                'console.log(resolveBare("@scope/pkg", "app/src", files));\n'
                'for (const [n, d] of [["react", "other"], ["zzz", "app"], ["local", "app"]]) { try { '
                'console.log(resolveBare(n, d, files)); } catch (e) { console.log(e.message); } }\n',
      'hint': 'Цикл: проверьте <dir>/node_modules, затем поднимитесь на уровень выше; корень — пустая '
              'строка.',
      'expected': ['node_modules/lodash/index.js',
                   'app/node_modules/react/index.js',
                   'app/node_modules/react/index.js',
                   'app/src/node_modules/local.js',
                   'node_modules/@scope/pkg/index.js',
                   "Cannot find package 'react'",
                   "Cannot find package 'zzz'",
                   "Cannot find package 'local'"]},
     {'id': 'j9-exports-field',
      'mode': 'js',
      'title': 'Поле exports в package.json',
      'statement': 'Напишите функцию resolveExports(pkg, subpath, conditions): pkg — объект package.json, '
                   'subpath — «.» или «./utils» и т.п., conditions — массив активных условий, например '
                   '["import", "default"]. Поддержите: строку; объект условий (первое подходящее условие из '
                   'порядка ключей объекта; «default» подходит всегда); карту подпутей («.»: …, «./x»: …); '
                   'шаблоны «./features/*»: «./src/f/*.js» (звёздочка подставляется). Если подпути нет в '
                   'exports — Error("Package subpath \'<subpath>\' is not defined by \\"exports\\""). Если '
                   'exports нет — подпуть «.» даёт pkg.main ?? «./index.js».',
      'starter': 'function resolveExports(pkg, subpath, conditions) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const pkg = {\n'
                '  name: "lib",\n'
                '  exports: {\n'
                '    ".": { import: "./esm/index.js", require: "./cjs/index.cjs", default: "./index.js" },\n'
                '    "./utils": "./src/utils.js",\n'
                '    "./features/*": { browser: "./src/browser/*.js", default: "./src/f/*.js" },\n'
                '    "./internal": null,\n'
                '  },\n'
                '};\n'
                'const t = (sp, c) => { try { console.log(resolveExports(pkg, sp, c)); } catch (e) { '
                'console.log(e.message); } };\n'
                't(".", ["import"]); t(".", ["require"]); t(".", ["browser"]); t("./utils", ["import"]);\n'
                't("./features/chart", ["browser"]); t("./features/chart", ["node"]); t("./nope", '
                '["import"]); t("./internal", ["import"]);\n'
                'console.log(resolveExports({ exports: "./main.js" }, ".", []));\n'
                'console.log(resolveExports({ exports: { import: "./a.mjs", default: "./a.js" } }, ".", '
                '["require"]));\n'
                'console.log(resolveExports({ main: "./lib/m.js" }, ".", []), resolveExports({}, ".", '
                '[]));\n',
      'hint': 'Приведите exports к карте подпутей; для условий идите по ключам по порядку; для шаблонов '
              'замените * найденной серединой.',
      'expected': ['./esm/index.js',
                   './cjs/index.cjs',
                   './index.js',
                   './src/utils.js',
                   './src/browser/chart.js',
                   './src/f/chart.js',
                   'Package subpath \'./nope\' is not defined by "exports"',
                   'Package subpath \'./internal\' is not defined by "exports"',
                   './main.js',
                   './a.js',
                   './lib/m.js ./index.js']},
     {'id': 'j9-import-map',
      'mode': 'js',
      'title': 'Карта импортов браузера',
      'statement': 'Напишите функцию resolveImport(map, spec, referrer): map = { imports: {…}, scopes: { '
                   '"/admin/": {…} } }. Правила: если путь referrer начинается с ключа из scopes (выбирается '
                   'самый длинный подходящий), сначала смотрится эта область, затем imports. Точное '
                   'совпадение имени побеждает; ключ с «/» на конце — префикс: «vue/» + «dist/x.js» → '
                   'значение + «dist/x.js». Не найдено — spec без изменений, но голое имя (не начинается с '
                   '«/», «./», «../», «https://») — TypeError.',
      'starter': 'function resolveImport(map, spec, referrer) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const map = { imports: { lodash: "/vendor/lodash.js", "vue/": "/vendor/vue/", app: '
                '"/src/app.js" }, scopes: { "/admin/": { lodash: "/vendor/lodash-admin.js" }, '
                '"/admin/legacy/": { app: "/src/legacy-app.js" } } };\n'
                'for (const [s, r] of [["lodash", "/index.html"], ["lodash", "/admin/page.js"], '
                '["vue/dist/vue.js", "/x.js"], ["app", "/admin/legacy/a.js"], ["app", "/admin/b.js"], '
                '["./local.js", "/x.js"], ["https://cdn.x/y.js", "/x.js"]]) console.log(s, r, '
                'resolveImport(map, s, r));\n'
                'try { resolveImport(map, "react", "/x.js"); } catch (e) { console.log(e.name); }\n',
      'hint': 'Сначала самая длинная подходящая область, потом imports; для префиксов с «/» на конце — самый '
              'длинный ключ.',
      'expected': ['lodash /index.html /vendor/lodash.js',
                   'lodash /admin/page.js /vendor/lodash-admin.js',
                   'vue/dist/vue.js /x.js /vendor/vue/dist/vue.js',
                   'app /admin/legacy/a.js /src/legacy-app.js',
                   'app /admin/b.js /src/app.js',
                   './local.js /x.js ./local.js',
                   'https://cdn.x/y.js /x.js https://cdn.x/y.js',
                   'TypeError']},
     {'id': 'j9-live-binding',
      'mode': 'js',
      'title': 'Живые привязки: пространство имён модуля',
      'statement': 'Напишите функцию createNamespace(getters): getters — объект «имя → функция без '
                   'аргументов»; возвращает объект-пространство имён: чтение ns.имя вызывает функцию '
                   '(значение всегда свежее), ключи перечисляются в алфавитном порядке, запись, удаление и '
                   'добавление новых свойств бросают TypeError. Используйте Proxy или defineProperty.',
      'starter': 'function createNamespace(getters) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                '"use strict";\n'
                'let count = 0;\n'
                'const ns = createNamespace({ inc: () => () => ++count, count: () => count, a: () => "a" '
                '});\n'
                'console.log(ns.count);\n'
                'ns.inc();\n'
                'ns.inc();\n'
                'console.log(ns.count, count);\n'
                'console.log(JSON.stringify(Object.keys(ns)));\n'
                'for (const f of [() => { ns.count = 10; }, () => { ns.extra = 1; }, () => { delete ns.a; '
                '}]) { try { f(); console.log("ok"); } catch (e) { console.log(e.name); } }\n'
                'console.log(ns.count);\n',
      'hint': 'Object.defineProperty(ns, k, { get, enumerable: true }) + Object.freeze.',
      'expected': ['0', '2 2', '["a","count","inc"]', 'TypeError', 'TypeError', 'TypeError', '2']},
     {'id': 'j9-esm-order',
      'mode': 'js',
      'title': 'Порядок выполнения ES-модулей',
      'statement': 'Модули заданы так: { имя: { imports: [имена] } }. Напишите функцию '
                   'executionOrder(modules, entry): порядок выполнения как в ES-модулях — обход в глубину: '
                   'сначала импорты по порядку, затем сам модуль (post-order); каждый модуль один раз; при '
                   'циклах повторно не заходим. Для неизвестного модуля бросьте Error("нет модуля: <имя>").',
      'starter': 'function executionOrder(modules, entry) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const m = { main: { imports: ["a", "b"] }, a: { imports: ["c"] }, b: { imports: ["c", "a"] '
                '}, c: { imports: [] }, x: { imports: ["y"] }, y: { imports: ["x"] }, bad: { imports: '
                '["ghost"] } };\n'
                'console.log(executionOrder(m, "main").join(" "));\n'
                'console.log(executionOrder(m, "c").join(" "));\n'
                'console.log(executionOrder(m, "x").join(" "), "|", executionOrder(m, "y").join(" "));\n'
                'try { executionOrder(m, "bad"); } catch (e) { console.log(e.message); }\n',
      'hint': 'Пометьте модуль посещённым до рекурсии; добавляйте в результат после обхода импортов.',
      'expected': ['c a b main', 'c', 'y x | x y', 'нет модуля: ghost']},
     {'id': 'j9-dynamic-import',
      'mode': 'js',
      'title': 'Кэш динамического импорта',
      'statement': 'Напишите функцию createImporter(loaders): loaders — объект «имя → функция, возвращающая '
                   'промис модуля». Возвращает функцию load(name): для одного имени одновременно и повторно '
                   'возвращается один и тот же промис (загрузка выполняется один раз); если загрузка '
                   'завершилась ошибкой — запись из кэша удаляется, и следующий вызов пробует снова; '
                   'неизвестное имя — отклонённый промис с Error("нет модуля").',
      'starter': 'function createImporter(loaders) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'let calls = { ok: 0, flaky: 0 };\n'
                'const loaders = {\n'
                '  ok: () => { calls.ok++; return new Promise((r) => setTimeout(() => r({ v: 1 }), 10)); },\n'
                '  flaky: () => { calls.flaky++; return calls.flaky < 2 ? Promise.reject(new Error("сеть")) '
                ': Promise.resolve({ v: 2 }); },\n'
                '};\n'
                'const load = createImporter(loaders);\n'
                'const [a, b] = [load("ok"), load("ok")];\n'
                'console.log(a === b);\n'
                'console.log(JSON.stringify(await a), calls.ok);\n'
                'console.log(load("ok") === a, calls.ok);\n'
                'try { await load("flaky"); } catch (e) { console.log("1:", e.message); }\n'
                'console.log(JSON.stringify(await load("flaky")), calls.flaky);\n'
                'try { await load("zzz"); } catch (e) { console.log(e.message); }\n',
      'hint': 'Map имя → промис; при отклонении удаляйте запись в p.catch.',
      'expected': ['true', '{"v":1} 1', 'true 1', '1: сеть', '{"v":2} 2', 'нет модуля']},
     {'id': 'j9-barrel-cost',
      'mode': 'js',
      'title': 'Цена «бочки»',
      'statement': 'Файлы заданы так: { путь: исходник }, где в исходнике бывают строки «import … from '
                   "'./x.js'» и «export * from './x.js'». Напишите функцию pulledIn(files, entry): массив "
                   'всех файлов, которые будут загружены при подключении entry (включая его), '
                   'отсортированный; пути в импортах относительно корня, без папок (просто «./x.js» → '
                   '«x.js»). Несуществующие файлы пропускайте.',
      'starter': 'function pulledIn(files, entry) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const files = {\n'
                '  "index.js": "export * from \'./a.js\';\\nexport * from \'./b.js\';\\nexport * from '
                '\'./c.js\';",\n'
                '  "a.js": "import { h } from \'./helpers.js\';\\nexport const a = 1;",\n'
                '  "b.js": "export const b = 2;",\n'
                '  "c.js": "import \'./big.js\';\\nexport const c = 3;",\n'
                '  "helpers.js": "export const h = 0;",\n'
                '  "big.js": "import { x } from \'./huge.js\';",\n'
                '  "huge.js": "export const x = 1;",\n'
                '  "app.js": "import { a } from \'./a.js\';",\n'
                '};\n'
                'console.log(pulledIn(files, "app.js").join());\n'
                'console.log(pulledIn(files, "index.js").join());\n'
                'console.log(pulledIn(files, "b.js").join(), pulledIn(files, "ghost.js").length);\n',
      'hint': "Найдите в тексте все from './…' и обойдите граф; пометьте посещённые файлы.",
      'expected': ['a.js,app.js,helpers.js', 'a.js,b.js,c.js,helpers.js,index.js', 'b.js 0']},
     {'id': 'j9-find-cycles',
      'mode': 'js',
      'title': 'Поиск циклов зависимостей',
      'statement': 'Граф зависимостей задан объектом { модуль: [зависимости] }. Напишите функцию '
                   'findCycles(graph): массив найденных циклов — каждый цикл записан массивом имён, начиная '
                   'с лексикографически наименьшего, без повтора первого в конце (например, ["a","b","c"]); '
                   'один и тот же цикл не повторяется; массив циклов отсортирован. Рёбра в неизвестные узлы '
                   'игнорируйте.',
      'starter': 'function findCycles(graph) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(findCycles({ a: ["b"], b: ["c"], c: ["a"] })));\n'
                'console.log(JSON.stringify(findCycles({ a: ["b"], b: ["c"], c: [] })));\n'
                'console.log(JSON.stringify(findCycles({ x: ["x"], y: ["z"], z: ["y", "x"] })));\n'
                'console.log(JSON.stringify(findCycles({ b: ["a"], a: ["b"], c: ["ghost"] })));\n'
                'console.log(JSON.stringify(findCycles({})));\n',
      'hint': 'Обход в глубину со стеком текущего пути; встретив узел из стека, вырежьте цикл и нормализуйте '
              'поворотом.',
      'expected': ['[["a","b","c"]]', '[]', '[["x"],["y","z"]]', '[["a","b"]]', '[]']},
     {'id': 'j9-eval-cjs',
      'mode': 'js',
      'title': 'Загрузчик CommonJS из исходника',
      'statement': 'Напишите функцию runCommonJs(source, requireFn): выполняет исходный текст модуля в '
                   'функции с параметрами (exports, require, module) и возвращает итоговый module.exports '
                   '(то есть и записи в exports, и присваивание module.exports=… должны работать). Ошибки '
                   'выполнения не перехватывайте.',
      'starter': 'function runCommonJs(source, requireFn) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const req = (n) => ({ lodash: { id: (x) => x } })[n];\n'
                'console.log(JSON.stringify(runCommonJs("exports.a = 1; exports.b = '
                'require(\'lodash\').id(2);", req)));\n'
                'console.log(JSON.stringify(runCommonJs("module.exports = [1, 2, 3];", req)));\n'
                'console.log(JSON.stringify(runCommonJs("", req)));\n'
                'console.log(typeof runCommonJs("module.exports = function f() {};", req));\n'
                'try { runCommonJs("throw new Error(\'boom\');", req); } catch (e) { console.log(e.message); '
                '}\n'
                'console.log(JSON.stringify(runCommonJs("exports.me = this === module.exports ? \'same\' : '
                'typeof this;", req)));\n',
      'hint': "new Function('exports', 'require', 'module', source).call(…)",
      'expected': ['{"a":1,"b":2}', '[1,2,3]', '{}', 'function', 'boom', '{"me":"object"}']},
     {'id': 'j9-app-error',
      'mode': 'js',
      'title': 'Иерархия AppError',
      'statement': 'Напишите класс AppError extends Error: конструктор (message, { code = "E_APP", status = '
                   '500, details } = {}); поля name (по имени класса — this.constructor.name), code, status, '
                   'details; метод toJSON() → { name, code, message, status, details } (details — только '
                   'если задан). И подклассы NotFoundError (code E_NOT_FOUND, status 404, сообщение по '
                   'умолчанию «Не найдено») и ValidationError (E_VALIDATION, 422, details — массив ошибок '
                   'полей).',
      'starter': 'class AppError extends Error {\n'
                 '}\n'
                 'class NotFoundError extends AppError {\n'
                 '}\n'
                 'class ValidationError extends AppError {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'const e = new AppError("сбой");\n'
                'console.log(JSON.stringify(e), e.name, e instanceof Error);\n'
                'const nf = new NotFoundError();\n'
                'console.log(JSON.stringify(nf), nf instanceof AppError, nf.name);\n'
                'console.log(JSON.stringify(new NotFoundError("нет пользователя 5")));\n'
                'const v = new ValidationError([{ field: "age", msg: "мало" }]);\n'
                'console.log(JSON.stringify(v), v.status, v instanceof AppError);\n'
                'console.log(JSON.stringify({ error: v }));\n'
                'console.log(typeof v.stack, String(nf));\n',
      'hint': 'Имя класса: this.constructor.name; toJSON определяет, как ошибка попадёт в JSON.stringify.',
      'expected': ['{"name":"AppError","code":"E_APP","message":"сбой","status":500} AppError true',
                   '{"name":"NotFoundError","code":"E_NOT_FOUND","message":"Не найдено","status":404} true '
                   'NotFoundError',
                   '{"name":"NotFoundError","code":"E_NOT_FOUND","message":"нет пользователя '
                   '5","status":404}',
                   '{"name":"ValidationError","code":"E_VALIDATION","message":"Некорректные '
                   'данные","status":422,"details":[{"field":"age","msg":"мало"}]} 422 true',
                   '{"error":{"name":"ValidationError","code":"E_VALIDATION","message":"Некорректные '
                   'данные","status":422,"details":[{"field":"age","msg":"мало"}]}}',
                   'string NotFoundError: Не найдено']},
     {'id': 'j9-cause-chain',
      'mode': 'js',
      'title': 'Цепочка причин',
      'statement': 'Напишите функции wrap(message, cause) → new Error(message, { cause }), causeChain(err) → '
                   'массив сообщений от самой верхней ошибки к первопричине (cause может быть не ошибкой — '
                   'тогда String(cause) становится последним элементом цепочки) и rootCause(err) → '
                   'первопричина (последний объект в цепочке, у которого нет cause; для не-ошибки — она '
                   'сама).',
      'starter': 'function wrap(message, cause) {\n'
                 '}\n'
                 'function causeChain(err) {\n'
                 '}\n'
                 'function rootCause(err) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'const low = new TypeError("таймаут");\n'
                'const mid = wrap("обрыв соединения", low);\n'
                'const top = wrap("не удалось сохранить заказ", mid);\n'
                'console.log(causeChain(top).join(" ← "));\n'
                'console.log(rootCause(top) === low, rootCause(low) === low);\n'
                'console.log(top.cause === mid, top instanceof Error);\n'
                'console.log(causeChain(wrap("верх", "строка-причина")).join(" ← "));\n'
                'console.log(rootCause(wrap("верх", 42)));\n'
                'console.log(causeChain(new Error("одна")).length);\n',
      'hint': 'Идите по err.cause, пока значение остаётся Error с полем cause.',
      'expected': ['не удалось сохранить заказ ← обрыв соединения ← таймаут',
                   'true true',
                   'true true',
                   'верх ← строка-причина',
                   '42',
                   '1']},
     {'id': 'j9-aggregate',
      'mode': 'js',
      'title': 'Собрать все ошибки',
      'statement': 'Напишите функцию runAll(tasks): tasks — массив синхронных функций. Выполняет все (не '
                   'останавливаясь на первой ошибке); если все успешны — возвращает массив результатов; '
                   'иначе бросает AggregateError с массивом errors (в порядке задач) и сообщением «упало N '
                   'из M».',
      'starter': 'function runAll(tasks) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(runAll([() => 1, () => 2])));\n'
                'try { runAll([() => 1, () => { throw new Error("a"); }, () => 3, () => { throw new '
                'TypeError("b"); }]); } catch (e) {\n'
                '  console.log(e.name, e.message, e instanceof AggregateError, e.errors.map((x) => '
                'x.message).join());\n'
                '}\n'
                'console.log(JSON.stringify(runAll([])));\n'
                'let ran = 0;\n'
                'try { runAll([() => { ran++; throw 1; }, () => { ran++; }]); } catch (e) { console.log(ran, '
                'e.errors[0]); }\n',
      'hint': 'Собирайте ошибки в массив и в конце бросайте new AggregateError(errors, message).',
      'expected': ['[1,2]', 'AggregateError упало 2 из 4 true a,b', '[]', '2 1']},
     {'id': 'j9-with-cleanup',
      'mode': 'js',
      'title': 'Гарантированное освобождение',
      'statement': 'Напишите функцию withResource(open, use, close): open() возвращает ресурс; use(res) — '
                   'рабочая функция; close(res) — освобождение. Результат use возвращается, close вызывается '
                   'ровно один раз — и при успехе, и при исключении в use. Если упали и use, и close — '
                   'бросьте ошибку use (ошибку close потеряйте). Если упал только close — бросьте её. Если '
                   'упал open — close не вызывается.',
      'starter': 'function withResource(open, use, close) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const log = [];\n'
                'const open = () => { log.push("open"); return { id: 1 }; };\n'
                'const close = () => log.push("close");\n'
                'console.log(withResource(open, (r) => r.id + 1, close), log.join());\n'
                'log.length = 0;\n'
                'try { withResource(open, () => { throw new Error("use"); }, close); } catch (e) { '
                'console.log(e.message, log.join()); }\n'
                'log.length = 0;\n'
                'try { withResource(open, () => 1, () => { throw new Error("close"); }); } catch (e) { '
                'console.log(e.message); }\n'
                'try { withResource(open, () => { throw new Error("use2"); }, () => { throw new '
                'Error("close2"); }); } catch (e) { console.log(e.message); }\n'
                'log.length = 0;\n'
                'try { withResource(() => { throw new Error("open"); }, () => 1, close); } catch (e) { '
                'console.log(e.message, log.length); }\n',
      'hint': 'try/catch вокруг use с повторным throw и отдельный try вокруг close внутри catch.',
      'expected': ['2 open,close', 'use open,close', 'close', 'use2', 'open 0']},
     {'id': 'j9-result',
      'mode': 'js',
      'title': 'Тип «Результат»',
      'statement': 'Напишите ok(value), err(error) и функции над результатами: map(r, f) (применяет f к '
                   'значению успеха), mapErr(r, f), andThen(r, f) (f возвращает новый результат), '
                   'unwrapOr(r, default), tryCatch(fn) (вызывает fn: успех — ok(результат), исключение — '
                   'err(исключение)). Результат — объект { ok: true, value } или { ok: false, error }.',
      'starter': 'function ok(value) {\n'
                 '}\n'
                 'function err(error) {\n'
                 '}\n'
                 'function map(r, f) {\n'
                 '}\n'
                 'function mapErr(r, f) {\n'
                 '}\n'
                 'function andThen(r, f) {\n'
                 '}\n'
                 'function unwrapOr(r, d) {\n'
                 '}\n'
                 'function tryCatch(fn) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'const parse = (s) => (Number.isNaN(Number(s)) ? err("не число: " + s) : ok(Number(s)));\n'
                'const half = (n) => (n % 2 === 0 ? ok(n / 2) : err("нечётное: " + n));\n'
                'const show = (r) => console.log(JSON.stringify(r));\n'
                'show(andThen(parse("10"), half));\n'
                'show(andThen(parse("7"), half));\n'
                'show(andThen(parse("x"), half));\n'
                'show(map(ok(2), (x) => x * 5));\n'
                'show(map(err("e"), (x) => x * 5));\n'
                'show(mapErr(err("e"), (m) => m.toUpperCase()));\n'
                'console.log(unwrapOr(ok(1), 0), unwrapOr(err("e"), 0));\n'
                'show(tryCatch(() => JSON.parse(\'{"a":1}\')));\n'
                'console.log(tryCatch(() => JSON.parse("{")).error.name);\n'
                'show(tryCatch(() => 1 + 1));\n',
      'hint': 'Каждая функция проверяет r.ok и либо работает со значением, либо возвращает ошибку без '
              'изменений.',
      'expected': ['{"ok":true,"value":5}',
                   '{"ok":false,"error":"нечётное: 7"}',
                   '{"ok":false,"error":"не число: x"}',
                   '{"ok":true,"value":10}',
                   '{"ok":false,"error":"e"}',
                   '{"ok":false,"error":"E"}',
                   '1 0',
                   '{"ok":true,"value":{"a":1}}',
                   'SyntaxError',
                   '{"ok":true,"value":2}']},
     {'id': 'j9-parse-config',
      'mode': 'js',
      'title': 'Разбор настроек с накоплением ошибок',
      'statement': 'Напишите функцию parseConfig(text): text — JSON-строка. Возвращает { ok: true, value: { '
                   'port, host, debug } } или { ok: false, errors: [...] } (все найденные ошибки по '
                   'порядку). Правила: неверный JSON — одна ошибка «Неверный JSON»; port — целое 1–65535 '
                   '(«port: нужно целое 1–65535»); host — непустая строка, по умолчанию «localhost»; debug — '
                   'булево, по умолчанию false («debug: нужно true или false»). Неизвестные поля — ошибка '
                   '«Неизвестное поле: <имя>».',
      'starter': 'function parseConfig(text) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const t of [\'{"port":8080}\', \'{"port":80,"host":"x.ru","debug":true}\', "{oops", '
                '\'{"port":0,"debug":"yes"}\', \'{"port":1.5,"host":""}\', '
                '\'{"port":443,"extra":1,"more":2}\', "[]", "null"]) '
                'console.log(JSON.stringify(parseConfig(t)));\n',
      'hint': 'Сначала разбор JSON, потом независимые проверки полей — все сообщения копятся в массив.',
      'expected': ['{"ok":true,"value":{"port":8080,"host":"localhost","debug":false}}',
                   '{"ok":true,"value":{"port":80,"host":"x.ru","debug":true}}',
                   '{"ok":false,"errors":["Неверный JSON"]}',
                   '{"ok":false,"errors":["port: нужно целое 1–65535","debug: нужно true или false"]}',
                   '{"ok":false,"errors":["port: нужно целое 1–65535","host: нужна непустая строка"]}',
                   '{"ok":false,"errors":["Неизвестное поле: extra","Неизвестное поле: more"]}',
                   '{"ok":false,"errors":["Неверный JSON"]}',
                   '{"ok":false,"errors":["Неверный JSON"]}']},
     {'id': 'j9-backoff',
      'mode': 'js',
      'title': 'Расписание пауз с экспонентой',
      'statement': 'Напишите функцию backoffDelays(attempts, base, cap, random): возвращает массив пауз '
                   'между попытками (attempts - 1 штук, перед 2-й, 3-й … попытками): для i-й паузы (i с 0) '
                   'верхняя граница ceil = min(cap, base * 2 ** i); сама пауза — «полный jitter»: '
                   'Math.floor(random() * (ceil + 1)); random — функция, возвращающая число в [0, 1).',
      'starter': 'function backoffDelays(attempts, base, cap, random) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const max = () => 0.999999;\n'
                'const zero = () => 0;\n'
                'console.log(JSON.stringify(backoffDelays(6, 100, 1000, max)));\n'
                'console.log(JSON.stringify(backoffDelays(6, 100, 1000, zero)));\n'
                'console.log(JSON.stringify(backoffDelays(1, 100, 1000, max)), '
                'JSON.stringify(backoffDelays(0, 100, 1000, max)));\n'
                'let i = 0;\n'
                'const seq = () => [0.5, 0.25, 0.75][i++ % 3];\n'
                'console.log(JSON.stringify(backoffDelays(4, 200, 500, seq)));\n'
                'console.log(JSON.stringify(backoffDelays(5, 1, 3, max)));\n',
      'hint': 'ceil = min(cap, base * 2 ** i); пауза = floor(random() * (ceil + 1)).',
      'expected': ['[100,200,400,800,1000]', '[0,0,0,0,0]', '[] []', '[100,100,375]', '[1,2,3,3]']},
     {'id': 'j9-retry',
      'mode': 'js',
      'title': 'Повтор с паузой',
      'statement': 'Напишите функцию retry(fn, { attempts = 3, delays = [], sleep, shouldRetry = () => true '
                   '}): вызывает fn(номер попытки с 1); при исключении, если попытки остались и '
                   'shouldRetry(error) истинно, ждёт await sleep(delays[попытка - 1] ?? 0) и пробует снова; '
                   'после последней попытки (или при shouldRetry ложном) бросает последнюю ошибку. '
                   'Возвращает результат fn. fn и sleep могут быть асинхронными.',
      'starter': 'async function retry(fn, options) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const slept = [];\n'
                'const sleep = async (ms) => { slept.push(ms); };\n'
                'const flaky = (failTimes) => async (n) => { if (n <= failTimes) throw new Error("сбой " + '
                'n); return "успех на " + n; };\n'
                'console.log(await retry(flaky(0), { sleep }), slept.length);\n'
                'console.log(await retry(flaky(2), { attempts: 5, delays: [100, 200, 400], sleep }), '
                'JSON.stringify(slept));\n'
                'slept.length = 0;\n'
                'try { await retry(flaky(9), { attempts: 3, delays: [10, 20], sleep }); } catch (e) { '
                'console.log(e.message, JSON.stringify(slept)); }\n'
                'slept.length = 0;\n'
                'try { await retry(async () => { throw new TypeError("не повторять"); }, { attempts: 5, '
                'sleep, shouldRetry: (e) => !(e instanceof TypeError) }); } catch (e) { console.log(e.name, '
                'slept.length); }\n'
                'console.log(await retry((n) => n * 10, { attempts: 1, sleep }));\n',
      'hint': 'Цикл по номерам попыток: try/catch вокруг await fn(n); после последней попытки — throw.',
      'expected': ['успех на 1 0', 'успех на 3 [100,200]', 'сбой 3 [10,20]', 'TypeError 0', '10']},
     {'id': 'j9-timeout',
      'mode': 'js',
      'title': 'Таймаут для промиса',
      'statement': 'Напишите класс TimeoutError extends Error (name «TimeoutError») и функцию '
                   'withTimeout(promise, ms): возвращает промис, который выполнится значением promise, если '
                   'он успел за ms миллисекунд, иначе отклонится TimeoutError("Превышено время ожидания: '
                   '<ms> мс"). Таймер после завершения нужно очистить (иначе процесс не завершится вовремя).',
      'starter': 'class TimeoutError extends Error {\n}\nfunction withTimeout(promise, ms) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const later = (v, ms, fail) => new Promise((res, rej) => setTimeout(() => (fail ? rej(new '
                'Error(v)) : res(v)), ms));\n'
                'console.log(await withTimeout(later("быстро", 10), 100));\n'
                'try { await withTimeout(later("медленно", 150), 30); } catch (e) { console.log(e.name, '
                'e.message, e instanceof TimeoutError, e instanceof Error); }\n'
                'try { await withTimeout(later("своя ошибка", 10, true), 100); } catch (e) { '
                'console.log(e.message); }\n'
                'console.log(await withTimeout(42, 10));\n'
                'const t0 = Date.now();\n'
                'await withTimeout(later("ok", 5), 5000);\n'
                'console.log(Date.now() - t0 < 1000);\n',
      'hint': 'Promise.race между исходным промисом и промисом-таймером; clearTimeout в finally.',
      'expected': ['быстро',
                   'TimeoutError Превышено время ожидания: 30 мс true true',
                   'своя ошибка',
                   '42',
                   'true']},
     {'id': 'j9-assert',
      'mode': 'js',
      'title': 'Свои утверждения',
      'statement': 'Напишите класс AssertionError extends Error (name «AssertionError», поля actual, '
                   'expected) и функции assert(cond, message), assertEqual(actual, expected, message) '
                   '(строгое равенство; сообщение по умолчанию «Ожидалось <expected>, получено <actual>» '
                   'через JSON.stringify значений), assertThrows(fn, ErrorClass?) (бросает AssertionError '
                   '«Ожидалось исключение», если fn не бросила; если указан класс и ошибка не его экземпляр '
                   '— «Ожидалось исключение <ИмяКласса>, получено <name>»; возвращает пойманную ошибку).',
      'starter': 'class AssertionError extends Error {\n'
                 '}\n'
                 'function assert(cond, message) {\n'
                 '}\n'
                 'function assertEqual(actual, expected, message) {\n'
                 '}\n'
                 'function assertThrows(fn, ErrorClass) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'const t = (f) => { try { console.log("ok", f() ?? ""); } catch (e) { console.log(e.name + '
                '":", e.message); } };\n'
                't(() => assert(true));\n'
                't(() => assert(false));\n'
                't(() => assert(0, "ноль — ложь"));\n'
                't(() => assertEqual(2, 2));\n'
                't(() => assertEqual(2, 3));\n'
                't(() => assertEqual("a", "b", "строки разные"));\n'
                't(() => assertThrows(() => { throw new RangeError("r"); }, RangeError).message);\n'
                't(() => assertThrows(() => 1));\n'
                't(() => assertThrows(() => { throw new TypeError("t"); }, RangeError));\n'
                'const e = (() => { try { assertEqual(1, 2); } catch (x) { return x; } })();\n'
                'console.log(e.actual, e.expected, e instanceof Error);\n',
      'hint': 'Сообщение по умолчанию собирайте шаблоном с JSON.stringify; поймайте ошибку из fn в '
              'try/catch.',
      'expected': ['ok',
                   'AssertionError: Утверждение не выполнено',
                   'AssertionError: ноль — ложь',
                   'ok',
                   'AssertionError: Ожидалось 3, получено 2',
                   'AssertionError: строки разные',
                   'ok r',
                   'AssertionError: Ожидалось исключение',
                   'AssertionError: Ожидалось исключение RangeError, получено TypeError',
                   '1 2 true']},
     {'id': 'j9-serialize-error',
      'mode': 'js',
      'title': 'Передача ошибки между процессами',
      'statement': 'Напишите функции serializeError(err) и deserializeError(obj). serializeError возвращает '
                   '«простой» объект { name, message, stack, cause? (рекурсивно), extra? } — extra содержит '
                   'собственные перечисляемые поля ошибки (например, code, status), если они есть; для '
                   'не-ошибок — { name: "NonError", message: String(value) }. deserializeError '
                   'восстанавливает Error: класс по name из набора (Error, TypeError, RangeError, '
                   'SyntaxError), иначе Error с этим name; message, stack, cause и extra восстанавливаются.',
      'starter': 'function serializeError(err) {\n}\nfunction deserializeError(obj) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const inner = new TypeError("внутри");\n'
                'const e = Object.assign(new RangeError("снаружи", { cause: inner }), { code: "E_X", status: '
                '400 });\n'
                'const s = serializeError(e);\n'
                'console.log(s.name, s.message, s.cause.name, JSON.stringify(s.extra), typeof s.stack);\n'
                'const j = JSON.parse(JSON.stringify(s));\n'
                'const back = deserializeError(j);\n'
                'console.log(back instanceof RangeError, back.message, back.cause instanceof TypeError, '
                'back.code, back.status, back.stack === e.stack);\n'
                'console.log(JSON.stringify(serializeError("просто строка")));\n'
                'const custom = deserializeError({ name: "NotFound", message: "нет" });\n'
                'console.log(custom.name, custom instanceof Error, Object.keys(serializeError(new '
                'Error("x"))).sort().join());\n',
      'hint': 'Собственные поля: Object.keys(err); класс по имени — из словаря встроенных конструкторов.',
      'expected': ['RangeError снаружи TypeError {"code":"E_X","status":400} string',
                   'true снаружи true E_X 400 true',
                   '{"name":"NonError","message":"просто строка"}',
                   'NotFound true message,name,stack']},
     {'id': 'j9-parse-stack',
      'mode': 'js',
      'title': 'Разбор стека вызовов',
      'statement': 'Напишите функцию parseStack(stack): строка в формате V8: первая строка — сообщение, '
                   'дальше строки «    at имя (файл:строка:столбец)» или «    at файл:строка:столбец» '
                   '(анонимная функция). Верните массив { fn, file, line, col } (fn — null для анонимных; '
                   'line и col — числа); строки в другом формате пропускайте. Вложенные скобки в имени '
                   '«async Object.run» — fn берётся как есть.',
      'starter': 'function parseStack(stack) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const st = `Error: boom\n'
                '    at div (/app/math.js:2:9)\n'
                '    at async Object.run (/app/main.js:14:3)\n'
                '    at /app/index.js:30:1\n'
                '    at Module._compile (node:internal/modules/cjs/loader:1554:14)\n'
                '    какая-то посторонняя строка`;\n'
                'for (const f of parseStack(st)) console.log(JSON.stringify(f));\n'
                'console.log(parseStack("Error: x").length);\n',
      'hint': 'Регулярное выражение с необязательной группой «имя (» и разбором файл:строка:столбец.',
      'expected': ['{"fn":"div","file":"/app/math.js","line":2,"col":9}',
                   '{"fn":"async Object.run","file":"/app/main.js","line":14,"col":3}',
                   '{"fn":null,"file":"/app/index.js","line":30,"col":1}',
                   '{"fn":"Module._compile","file":"node:internal/modules/cjs/loader","line":1554,"col":14}',
                   '0']},
     {'id': 'j9-reporter',
      'mode': 'js',
      'title': 'Сборщик ошибок для мониторинга',
      'statement': 'Напишите функцию createReporter(now, limit): now() — текущее время (мс), limit — '
                   'максимум отправляемых отчётов за 1000 мс. Возвращает объект: report(err) → true, если '
                   'ошибка принята к отправке, и false, если отброшена (дубликат по паре name+message за '
                   'последние 1000 мс или превышен лимит за скользящие 1000 мс); sent() → массив принятых '
                   '«name: message» в порядке приёма.',
      'starter': 'function createReporter(now, limit) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'let t = 0;\n'
                'const r = createReporter(() => t, 3);\n'
                'const E = (m) => new Error(m);\n'
                'console.log(r.report(E("a")), r.report(E("a")), r.report(E("b")), r.report(new '
                'TypeError("a")));\n'
                'console.log(r.report(E("c")));\n'
                't = 500;\n'
                'console.log(r.report(E("d")));\n'
                't = 1001;\n'
                'console.log(r.report(E("a")), r.report(E("e")), r.report(E("f")), r.report(E("g")));\n'
                't = 3000;\n'
                'console.log(r.report(E("g")));\n'
                'console.log(r.sent().join(" | "));\n',
      'hint': 'Окно в 1000 мс: храните время последнего отчёта по ключу и список времён принятых отчётов.',
      'expected': ['true false true true',
                   'false',
                   'false',
                   'true true true false',
                   'true',
                   'Error: a | Error: b | TypeError: a | Error: a | Error: e | Error: f | Error: g']},
     {'id': 'j9-circuit-breaker',
      'mode': 'js',
      'title': 'Предохранитель (circuit breaker)',
      'statement': 'Напишите функцию createBreaker(fn, { threshold, cooldown, now }): после threshold подряд '
                   'идущих ошибок fn «размыкает» цепь: следующие вызовы сразу бросают Error("circuit open") '
                   'без вызова fn; по прошествии cooldown мс цепь «полуоткрыта»: один пробный вызов — успех '
                   'замыкает цепь (счётчик ошибок обнуляется), ошибка размыкает снова на cooldown. Успешный '
                   'вызов в обычном режиме тоже обнуляет счётчик. Возвращает функцию-обёртку call(...args). '
                   'Синхронные функции.',
      'starter': 'function createBreaker(fn, options) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'let t = 0;\n'
                'let broken = true;\n'
                'let calls = 0;\n'
                'const call = createBreaker(() => { calls++; if (broken) throw new Error("сбой"); return '
                '"ok"; }, { threshold: 3, cooldown: 100, now: () => t });\n'
                'const tryIt = () => { try { return call(); } catch (e) { return e.message; } };\n'
                'console.log([tryIt(), tryIt(), tryIt(), tryIt(), tryIt()].join(" | "), calls);\n'
                't = 99;\n'
                'console.log(tryIt(), calls);\n'
                't = 100;\n'
                'console.log(tryIt(), calls);\n'
                't = 150;\n'
                'console.log(tryIt(), calls);\n'
                't = 200;\n'
                'broken = false;\n'
                'console.log(tryIt(), tryIt(), calls);\n'
                'broken = true;\n'
                'console.log([tryIt(), tryIt(), tryIt(), tryIt()].join(" | "), calls);\n',
      'hint': 'Состояния: закрыта, открыта (до openedAt + cooldown), полуоткрыта (после — пробный вызов).',
      'expected': ['сбой | сбой | сбой | circuit open | circuit open 3',
                   'circuit open 3',
                   'сбой 4',
                   'circuit open 4',
                   'ok ok 6',
                   'сбой | сбой | сбой | circuit open 9']},
     {'id': 'j9-validate-all',
      'mode': 'js',
      'title': 'Валидация со всеми ошибками',
      'statement': 'Схема: { поле: { type: "string"|"number"|"boolean", required?: true, min?, max? } } '
                   '(min/max — для числа значение, для строки длина). Напишите функцию validate(schema, '
                   'obj): возвращает массив строк-ошибок «поле: причина» в порядке полей схемы, все сразу: '
                   '«обязательное поле», «ожидался тип <type>», «меньше минимума <min>», «больше максимума '
                   '<max>». Необязательное отсутствующее поле пропускается. Пустой массив — всё верно.',
      'starter': 'function validate(schema, obj) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const schema = { name: { type: "string", required: true, min: 2, max: 5 }, age: { type: '
                '"number", min: 0, max: 150 }, admin: { type: "boolean" } };\n'
                'for (const o of [{ name: "Ада", age: 36 }, {}, { name: "A", age: -1, admin: "yes" }, { '
                'name: "Длинноеимя", age: 200 }, { name: 5 }, { name: "Бо", admin: false }]) '
                'console.log(JSON.stringify(validate(schema, o)));\n',
      'hint': 'Для каждого поля схемы — несколько независимых проверок, ошибки копятся в массив.',
      'expected': ['[]',
                   '["name: обязательное поле"]',
                   '["name: меньше минимума 2","age: меньше минимума 0","admin: ожидался тип boolean"]',
                   '["name: больше максимума 5","age: больше максимума 150"]',
                   '["name: ожидался тип string"]',
                   '[]']},
     {'id': 'j9-fix-swallow',
      'mode': 'js',
      'title': 'Исправьте: проглоченная ошибка',
      'statement': 'Функция readJson(text, fallback) должна возвращать fallback только для некорректного '
                   'JSON (SyntaxError), а любые другие ошибки пробрасывать дальше. Сейчас пустой catch '
                   'скрывает всё — даже ошибку при обращении к text.trim, когда text не строка. Исправьте.',
      'starter': 'function readJson(text, fallback) {\n'
                 '  try {\n'
                 '    return JSON.parse(text.trim());\n'
                 '  } catch (e) {\n'
                 '    return fallback;\n'
                 '  }\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(readJson(\' {"a":1} \', null)));\n'
                'console.log(JSON.stringify(readJson("{oops", "запас")));\n'
                'try { readJson(42, "запас"); console.log("проглочено"); } catch (e) { console.log(e.name); '
                '}\n'
                'try { readJson(null, 1); console.log("проглочено"); } catch (e) { console.log(e.name); }\n'
                'console.log(readJson("", "пусто"));\n',
      'hint': 'В catch проверьте e instanceof SyntaxError; остальное — throw e.',
      'expected': ['{"a":1}', '"запас"', 'TypeError', 'TypeError', 'пусто']},
     {'id': 'j9-ensure-error',
      'mode': 'js',
      'title': 'Приведение брошенного значения к Error',
      'statement': 'В JavaScript можно бросить что угодно. Напишите функцию ensureError(x): если x — Error, '
                   'вернуть его; если строка — new Error(x); если объект с полем message (строкой) — Error с '
                   'этим сообщением и cause = x; иначе — Error(«Брошено не-значение ошибки: <JSON или '
                   'String(x)>») с cause = x. Для null и undefined — «Брошено не-значение ошибки: '
                   'null/undefined».',
      'starter': 'function ensureError(x) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const e = new TypeError("t");\n'
                'console.log(ensureError(e) === e);\n'
                'console.log(ensureError("строка").message);\n'
                'const o = { message: "из объекта", code: 7 };\n'
                'const r = ensureError(o);\n'
                'console.log(r.message, r.cause === o, r instanceof Error);\n'
                'console.log(ensureError(42).message);\n'
                'console.log(ensureError(null).message, "|", ensureError(undefined).message);\n'
                'console.log(ensureError({ a: 1 }).message);\n'
                'console.log(ensureError([1, 2]).message);\n'
                'const cyc = {}; cyc.self = cyc;\n'
                'console.log(ensureError(cyc).message);\n',
      'hint': 'Проверяйте типы по порядку; JSON.stringify может бросить на циклической ссылке — оберните в '
              'try.',
      'expected': ['true',
                   'строка',
                   'из объекта true true',
                   'Брошено не-значение ошибки: 42',
                   'Брошено не-значение ошибки: null | Брошено не-значение ошибки: undefined',
                   'Брошено не-значение ошибки: {"a":1}',
                   'Брошено не-значение ошибки: [1,2]',
                   'Брошено не-значение ошибки: [object Object]']},
     {'id': 'j9-with-resources',
      'mode': 'js',
      'title': 'Несколько ресурсов: закрытие в обратном порядке',
      'statement': 'Напишите функцию withResources(openers, use): openers — массив функций, каждая '
                   'возвращает ресурс { name, close() }; открываются по порядку; use(resources) вызывается с '
                   'массивом ресурсов; затем все открытые ресурсы закрываются в обратном порядке, даже если '
                   'use или открытие очередного ресурса упали. Если во время закрытия падает одна или '
                   'несколько ошибок вместе с ошибкой use — бросьте AggregateError([ошибка use, ошибки '
                   'закрытия…]); если только закрытия — AggregateError из них (при одной — сама эта ошибка); '
                   'если только use — его ошибка. Успех — результат use.',
      'starter': 'function withResources(openers, use) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const log = [];\n'
                'const res = (name, failClose) => () => { log.push("open " + name); return { name, close() { '
                'log.push("close " + name); if (failClose) throw new Error("close " + name); } }; };\n'
                'console.log(withResources([res("a"), res("b"), res("c")], (rs) => rs.map((r) => '
                'r.name).join("")), "|", log.join(", "));\n'
                'log.length = 0;\n'
                'try { withResources([res("a"), res("b")], () => { throw new Error("use"); }); } catch (e) { '
                'console.log(e.message, "|", log.join(", ")); }\n'
                'log.length = 0;\n'
                'try { withResources([res("a"), () => { throw new Error("open b"); }, res("c")], () => 1); } '
                'catch (e) { console.log(e.message, "|", log.join(", ")); }\n'
                'log.length = 0;\n'
                'try { withResources([res("a", true), res("b", true)], () => 1); } catch (e) { '
                'console.log(e.name, e.errors.map((x) => x.message).join()); }\n'
                'log.length = 0;\n'
                'try { withResources([res("a", true)], () => { throw new Error("use"); }); } catch (e) { '
                'console.log(e.name, e.errors.map((x) => x.message).join()); }\n'
                'log.length = 0;\n'
                'try { withResources([res("a", true)], () => 1); } catch (e) { console.log(e.name, '
                'e.message); }\n',
      'hint': 'Собирайте ошибки в массив, закрывайте ресурсы в цикле по перевёрнутому списку открытых.',
      'expected': ['abc | open a, open b, open c, close c, close b, close a',
                   'use | open a, open b, close b, close a',
                   'open b | open a, close a',
                   'AggregateError close b,close a',
                   'AggregateError use,close a',
                   'Error close a']},
     {'id': 'j9-fix-throw-string',
      'mode': 'js',
      'title': 'Исправьте: бросаются строки',
      'statement': 'Функция divideStrict(a, b) бросает строку при делении на ноль, из-за чего у «ошибки» нет '
                   'стека и её нельзя отличить по классу. Исправьте так, чтобы бросался RangeError с '
                   'сообщением «Деление на ноль»; при нечисловых аргументах — TypeError «Нужны числа».',
      'starter': 'function divideStrict(a, b) {\n'
                 '  if (typeof a !== "number" || typeof b !== "number") throw "Нужны числа";\n'
                 '  if (b === 0) throw "Деление на ноль";\n'
                 '  return a / b;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(divideStrict(9, 3));\n'
                'for (const args of [[1, 0], ["1", 2], [5, undefined]]) {\n'
                '  try { divideStrict(...args); } catch (e) { console.log(e instanceof Error, e.name, '
                'e.message, typeof e.stack); }\n'
                '}\n',
      'hint': 'throw new RangeError(...) и throw new TypeError(...)',
      'expected': ['3',
                   'true RangeError Деление на ноль string',
                   'true TypeError Нужны числа string',
                   'true TypeError Нужны числа string']},
     {'id': 'j9-fix-finally-return',
      'mode': 'js',
      'title': 'Исправьте: return в finally съедает исключение',
      'statement': 'Функция loadAll(loaders) должна вызвать все загрузчики по очереди, посчитать, сколько их '
                   'выполнено (поле done), и обязательно записать итог в журнал log.push("итог: N") — но '
                   'исключение первого упавшего загрузчика должно всплыть наружу. Сейчас return внутри '
                   'finally «съедает» исключение. Исправьте, не убирая запись в журнал.',
      'starter': 'function loadAll(loaders, log) {\n'
                 '  let done = 0;\n'
                 '  try {\n'
                 '    for (const l of loaders) {\n'
                 '      l();\n'
                 '      done++;\n'
                 '    }\n'
                 '    return done;\n'
                 '  } finally {\n'
                 '    log.push("итог: " + done);\n'
                 '    return done;\n'
                 '  }\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'const log = [];\n'
                'console.log(loadAll([() => 1, () => 2], log), log.join());\n'
                'log.length = 0;\n'
                'try { loadAll([() => 1, () => { throw new Error("упал второй"); }, () => 3], log); '
                'console.log("исключение проглочено"); } catch (e) { console.log(e.message, log.join()); }\n'
                'log.length = 0;\n'
                'console.log(loadAll([], log), log.join());\n',
      'hint': 'Уберите return из блока finally: тогда исключение продолжит всплывать.',
      'expected': ['2 итог: 2', 'упал второй итог: 1', '0 итог: 0']}]}
