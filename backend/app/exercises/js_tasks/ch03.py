"""Задачи книги «Современный Frontend», глава 3 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {3: [{'id': 'j3-arrow-to-function',
      'mode': 'js',
      'title': 'Мини-Babel: стрелка → function',
      'statement': 'Напишите функцию arrowToFunction(src): превращает одну строку вида «(a, b) => '
                   'выражение», «x => выражение» или «() => выражение» в «function (a, b) { return '
                   'выражение; }». Скобки вокруг единственного параметра необязательны; пробелы вокруг '
                   'стрелки не важны; результат должен совпадать с примерами.',
      'starter': 'function arrowToFunction(src) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const s of ["(a, b) => a + b", "x => x * 2", "() => 42", "(x) => x.length;", "n   =>   '
                'n > 0 ? \'да\' : \'нет\'", "( a ,b ) => [a, b]"]) console.log(arrowToFunction(s));\n',
      'hint': 'Регулярное выражение с двумя вариантами параметров: в скобках или одиночный идентификатор.',
      'expected': ['function (a, b) { return a + b; }',
                   'function (x) { return x * 2; }',
                   'function () { return 42; }',
                   'function (x) { return x.length; }',
                   "function (n) { return n > 0 ? 'да' : 'нет'; }",
                   'function (a ,b) { return [a, b]; }']},
     {'id': 'j3-let-to-var',
      'mode': 'js',
      'title': 'Мини-Babel: let/const → var',
      'statement': 'Напишите функцию letToVar(src): заменяет ключевые слова let и const на var во всём '
                   'исходнике, но не внутри строк в одинарных или двойных кавычках (и не в частях слов вроде '
                   '«outlet» или «constant»).',
      'starter': 'function letToVar(src) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(letToVar("let a = 1; const b = 2;"));\n'
                'console.log(letToVar("const s = \'let me in\'; let t = \\"const\\";"));\n'
                'console.log(letToVar("outlet = constant + letter; // let"));\n'
                'console.log(letToVar("for (let i = 0; i < n; i++) {}"));\n'
                'console.log(letToVar("const q = \'it\\\\\'s let\'; const z = 1;"));\n'
                'console.log(letToVar(""));\n',
      'hint': 'Пройдите по тексту: строки копируйте целиком, а в остальных местах ищите слова с границами.',
      'expected': ['var a = 1; var b = 2;',
                   'var s = \'let me in\'; var t = "const";',
                   'outlet = constant + letter; // var',
                   'for (var i = 0; i < n; i++) {}',
                   "var q = 'it\\'s let'; var z = 1;"]},
     {'id': 'j3-template-to-concat',
      'mode': 'js',
      'title': 'Мини-Babel: шаблон → конкатенация',
      'statement': 'Напишите функцию templateToConcat(tpl): принимает содержимое шаблонной строки (без '
                   'обратных кавычек) вроде «Привет, ${name}! Тебе ${age + 1}.» и возвращает код '
                   'конкатенации «"Привет, " + name + "! Тебе " + (age + 1) + "."». Выражения в ${…} '
                   'оборачиваются в скобки, если в них есть пробел; пустые литеральные части пропускаются; '
                   'для строки без подстановок — один литерал. Кавычки и обратные слэши в литералах '
                   'экранируйте через JSON.stringify.',
      'starter': 'function templateToConcat(tpl) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(templateToConcat("Привет, ${name}! Тебе ${age + 1}."));\n'
                'console.log(templateToConcat("${a}${b}"));\n'
                'console.log(templateToConcat("без подстановок"));\n'
                'console.log(templateToConcat(""));\n'
                'console.log(templateToConcat(\'он сказал "да" ${x}\'));\n'
                'console.log(templateToConcat("${ user.name }"));\n',
      'hint': 'matchAll по /\\$\\{([^}]*)\\}/g; между подстановками — литералы через JSON.stringify.',
      'expected': ['"Привет, " + name + "! Тебе " + (age + 1) + "."',
                   'a + b',
                   '"без подстановок"',
                   '""',
                   '"он сказал \\"да\\" " + x',
                   'user.name']},
     {'id': 'j3-array-from',
      'mode': 'js',
      'title': 'Полифил Array.from',
      'statement': 'Напишите функцию arrayFrom(src, mapFn): принимает итерируемый объект (массив, строку, '
                   'Set, Map, генератор) или «массивоподобный» объект { length, 0:…, 1:… }; возвращает '
                   'массив, применяя mapFn(значение, индекс), если она передана. Метод Array.from '
                   'использовать нельзя.',
      'starter': 'function arrayFrom(src, mapFn) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(JSON.stringify(arrayFrom("абв")));\n'
                'console.log(JSON.stringify(arrayFrom(new Set([1, 2, 2, 3]))));\n'
                'console.log(JSON.stringify(arrayFrom(new Map([["a", 1]]))));\n'
                'console.log(JSON.stringify(arrayFrom({ length: 3, 0: "x", 2: "z" })));\n'
                'console.log(JSON.stringify(arrayFrom({ length: 3 }, (_, i) => i * i)));\n'
                'console.log(JSON.stringify(arrayFrom((function* () { yield 1; yield 2; })(), (x) => x + '
                '10)));\n'
                'console.log(JSON.stringify(arrayFrom({})), JSON.stringify(arrayFrom([1, 2], (x, i) => x * '
                'i)));\n'
                'console.log(__count("Array" + ".from"));\n',
      'hint': 'Если у объекта есть Symbol.iterator — обходите for…of, иначе — по length.',
      'expected': ['["а","б","в"]',
                   '[1,2,3]',
                   '[["a",1]]',
                   '["x",null,"z"]',
                   '[0,1,4]',
                   '[11,12]',
                   '[] [0,2]',
                   '0']},
     {'id': 'j3-object-assign',
      'mode': 'js',
      'title': 'Полифил Object.assign',
      'statement': 'Напишите функцию assign(target, ...sources): копирует собственные перечисляемые свойства '
                   '(включая символьные ключи) из источников в target слева направо и возвращает target; '
                   'null и undefined в источниках пропускаются; если target равен null или undefined — '
                   'TypeError. Object.assign использовать нельзя.',
      'starter': 'function assign(target, ...sources) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'const s = Symbol("s");\n'
                'const t = { a: 1 };\n'
                'const r = assign(t, { b: 2, a: 9 }, null, undefined, { [s]: 3, c: 4 }, "xy");\n'
                'console.log(r === t, JSON.stringify(r), r[s]);\n'
                'try { assign(null, {}); } catch (e) { console.log(e.name); }\n'
                'console.log(JSON.stringify(assign({}, [7, 8])));\n'
                'console.log(typeof assign(5, { a: 1 }), assign(5, { a: 1 }).a);\n'
                'console.log(__count("Object" + ".assign"));\n',
      'hint': 'Ключи: Object.keys + перечисляемые символы из Object.getOwnPropertySymbols.',
      'expected': ['true {"0":"x","1":"y","a":9,"b":2,"c":4} 3',
                   'TypeError',
                   '{"0":7,"1":8}',
                   'object 1',
                   '0']},
     {'id': 'j3-includes',
      'mode': 'js',
      'title': 'Полифил Array.prototype.includes',
      'statement': 'Напишите функцию includesPoly(arr, x, from = 0): true, если x есть в массиве начиная с '
                   'индекса from (отрицательный from считается от конца); сравнение SameValueZero: NaN '
                   'находится, +0 и -0 равны. Методы includes и indexOf использовать нельзя.',
      'starter': 'function includesPoly(arr, x, from = 0) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(includesPoly([1, 2, 3], 2), includesPoly([1, 2, 3], 4));\n'
                'console.log(includesPoly([NaN], NaN), includesPoly([0], -0), includesPoly([-0], 0));\n'
                'console.log(includesPoly([1, 2, 3], 1, 1), includesPoly([1, 2, 3], 3, -1), includesPoly([1, '
                '2, 3], 1, -1));\n'
                'console.log(includesPoly(["1"], 1), includesPoly([], undefined), includesPoly([undefined], '
                'undefined));\n'
                'console.log(__count(".incl" + "udes(") + __count(".ind" + "exOf("));\n',
      'hint': 'Сравнение: v === x || (v !== v && x !== x).',
      'expected': ['true false', 'true true true', 'false true false', 'false false true', '0']},
     {'id': 'j3-pad-start',
      'mode': 'js',
      'title': 'Полифил padStart',
      'statement': 'Напишите функцию padStartPoly(s, n, pad = " "): дополняет строку s в начале повторениями '
                   'pad до длины n (последнее повторение обрезается); если s уже не короче n или pad пустая '
                   '— возвращает s. Методы padStart и repeat использовать нельзя.',
      'starter': 'function padStartPoly(s, n, pad = " ") {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(padStartPoly("5", 3, "0"), padStartPoly("abc", 2), padStartPoly("7", 5), '
                'padStartPoly("1", 6, "ab"));\n'
                'console.log("[" + padStartPoly("x", 4) + "]", padStartPoly(42, 5, "*"), padStartPoly("a", '
                '3, ""));\n'
                'console.log(padStartPoly("", 3, "xy"));\n'
                'console.log(__count(".padS" + "tart(") + __count(".rep" + "eat("));\n',
      'hint': 'Накопите заполнитель циклом и обрежьте до нужной длины.',
      'expected': ['005 abc     7 ababa1', '[   x] ***42 a', 'xyx', '0']},
     {'id': 'j3-entries',
      'mode': 'js',
      'title': 'Полифилы Object.entries и Object.fromEntries',
      'statement': 'Напишите функции entriesPoly(obj) (массив пар [ключ, значение] собственных перечисляемых '
                   'строковых ключей в порядке перебора) и fromEntriesPoly(iterable) (объект из пар; поздний '
                   'ключ перезаписывает ранний). Object.entries и Object.fromEntries использовать нельзя.',
      'starter': 'function entriesPoly(obj) {\n}\nfunction fromEntriesPoly(iterable) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(JSON.stringify(entriesPoly({ b: 1, a: 2, 1: "x" })));\n'
                'console.log(JSON.stringify(entriesPoly({})));\n'
                'function P() { this.own = 1; }\n'
                'P.prototype.inh = 2;\n'
                'console.log(JSON.stringify(entriesPoly(new P())));\n'
                'console.log(JSON.stringify(fromEntriesPoly([["a", 1], ["b", 2], ["a", 3]])));\n'
                'console.log(JSON.stringify(fromEntriesPoly(new Map([["x", 1]]))));\n'
                'console.log(JSON.stringify(fromEntriesPoly(entriesPoly({ k: [1, 2] }))));\n'
                'console.log(__count("Object." + "entries") + __count("Object.fr" + "omEntries"));\n',
      'hint': 'for…in + hasOwn; fromEntries — цикл по парам с деструктурированием.',
      'expected': ['[["1","x"],["b",1],["a",2]]',
                   '[]',
                   '[["own",1]]',
                   '{"a":3,"b":2}',
                   '{"x":1}',
                   '{"k":[1,2]}',
                   '0']},
     {'id': 'j3-my-promise',
      'mode': 'js',
      'title': 'Полифил Promise',
      'statement': 'Напишите класс MyPromise: конструктор (executor(resolve, reject)); методы '
                   'then(onFulfilled, onRejected) (возвращает новый MyPromise; обработчики вызываются '
                   'асинхронно — через queueMicrotask; значение-«thenable» разворачивается), '
                   'catch(onRejected). Исключение внутри executor или обработчика отклоняет промис. '
                   'Статические resolve(v) и reject(e). Встроенный Promise использовать нельзя.',
      'starter': 'class MyPromise {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'const logs = { chain: [], nested: [], late: [], rej: [], exec: [], pass: [], thenable: [] '
                '};\n'
                'const p = new MyPromise((res) => { logs.chain.push("executor"); res(1); });\n'
                'p.then((v) => { logs.chain.push("then " + v); return v + 1; })\n'
                ' .then((v) => { logs.chain.push("then " + v); throw new Error("упало"); })\n'
                ' .then(() => logs.chain.push("не должно"))\n'
                ' .catch((e) => { logs.chain.push("catch " + e.message); return "восстановились"; })\n'
                ' .then((v) => logs.chain.push(v));\n'
                'logs.chain.push("sync конец");\n'
                'MyPromise.resolve(MyPromise.resolve(7)).then((v) => logs.nested.push("вложенный " + v));\n'
                'new MyPromise((_, rej) => setTimeout(() => rej("поздно"), 10)).catch((e) => '
                'logs.late.push("поздно: " + e));\n'
                'MyPromise.reject("r").then(undefined, (e) => logs.rej.push("onRejected " + e));\n'
                'new MyPromise(() => { throw new Error("в executor"); }).catch((e) => '
                'logs.exec.push(e.message));\n'
                'MyPromise.resolve(5).then().then((v) => logs.pass.push("прозрачно " + v));\n'
                'MyPromise.resolve({ then(res) { res("thenable"); } }).then((v) => logs.thenable.push(v));\n'
                'console.log("sync:", logs.chain.join(" / "));\n'
                'setTimeout(() => { for (const k of Object.keys(logs)) console.log(k + ":", logs[k].join(" / '
                '")); }, 60);\n'
                'console.log(__count("new Pr" + "omise("));\n',
      'hint': 'Состояние (pending/fulfilled/rejected), очередь обработчиков и queueMicrotask для их запуска; '
              'then возвращает новый MyPromise.',
      'expected': ['sync: executor / sync конец',
                   '0',
                   'chain: executor / sync конец / then 1 / then 2 / catch упало / восстановились',
                   'nested: вложенный 7',
                   'late: поздно: поздно',
                   'rej: onRejected r',
                   'exec: в executor',
                   'pass: прозрачно 5',
                   'thenable: thenable']},
     {'id': 'j3-promise-all',
      'mode': 'js',
      'title': 'Promise.all своими руками',
      'statement': 'Напишите функцию all(list): принимает массив значений и промисов; возвращает промис с '
                   'массивом результатов в исходном порядке; при первом отклонении отклоняется с той же '
                   'причиной; для пустого массива выполняется сразу. Promise.all, Promise.allSettled и '
                   'async/await использовать нельзя (конструктор Promise и then — можно).',
      'starter': 'function all(list) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'const later = (v, ms) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                'all([later("a", 30), "b", later("c", 5), 4]).then((r) => console.log(JSON.stringify(r)));\n'
                'all([]).then((r) => console.log(JSON.stringify(r)));\n'
                'all([later(1, 20), Promise.reject(new Error("плохо")), later(3, 5)]).then(() => '
                'console.log("не должно"), (e) => console.log("отклонён:", e.message));\n'
                'console.log(__count("Promis" + "e.all(") + __count("allSe" + "ttled") + __count("asy" + "nc '
                '") + __count("awa" + "it "));\n',
      'hint': 'Счётчик оставшихся; результаты кладите по индексу, а не в порядке завершения.',
      'expected': ['0', '[]', 'отклонён: плохо', '["a","b","c",4]']},
     {'id': 'j3-detect-features',
      'mode': 'js',
      'title': 'Какие возможности ES6+ использует код',
      'statement': 'Напишите функцию detectFeatures(src): возвращает отсортированный массив имён '
                   'возможностей, найденных в исходнике (вне строк в кавычках не учитывайте — для простоты '
                   'ищите по всему тексту): «arrow» (=>), «class» (слово class), «template» (обратная '
                   'кавычка), «letconst» (let или const как слова), «spread» (...), «async» (слова '
                   'async/await), «destructuring» (const/let/var { или [ слева от =), «optional» (?.), '
                   '«nullish» (??).',
      'starter': 'function detectFeatures(src) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(detectFeatures("var a = 1; function f(x) { return x; }")));\n'
                'console.log(JSON.stringify(detectFeatures("const f = (x) => x * 2;")));\n'
                'console.log(JSON.stringify(detectFeatures("class A { m() { return `hi ${this.x}`; } }")));\n'
                'console.log(JSON.stringify(detectFeatures("async function g() { const { a, b } = await '
                'load(); return [...a, b ?? 0, a?.c]; }")));\n'
                'console.log(JSON.stringify(detectFeatures("let [x, y] = pair; var { z } = obj;")));\n'
                'console.log(JSON.stringify(detectFeatures("")));\n',
      'hint': 'Таблица регулярных выражений; результат — отсортированные ключи сработавших.',
      'expected': ['[]',
                   '["arrow","letconst"]',
                   '["class","template"]',
                   '["async","destructuring","letconst","nullish","optional","spread"]',
                   '["destructuring","letconst"]',
                   '[]']},
     {'id': 'j3-browserslist',
      'mode': 'js',
      'title': 'Запрос browserslist',
      'statement': 'Напишите функцию matchBrowsers(query, data): query — строка вида «chrome >= 80, firefox '
                   '>= 78, not firefox 79, ie 11»; data — массив { name, version } (версия — число). Запросы '
                   'через запятую объединяются; «name >= N», «name > N», «name <= N», «name < N», «name N» '
                   'задают набор, «not …» вычитает из накопленного (применяется по порядку слева направо). '
                   'Результат — отсортированный массив строк «name version» (сортировка по имени, затем по '
                   'версии).',
      'starter': 'function matchBrowsers(query, data) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const data = [];\n'
                'for (const v of [78, 79, 80, 81, 100]) data.push({ name: "chrome", version: v });\n'
                'for (const v of [77, 78, 79, 80]) data.push({ name: "firefox", version: v });\n'
                'for (const v of [10, 11]) data.push({ name: "ie", version: v });\n'
                'console.log(matchBrowsers("chrome >= 80, firefox >= 78, not firefox 79, ie 11", '
                'data).join(" | "));\n'
                'console.log(matchBrowsers("chrome < 80", data).join(" | "));\n'
                'console.log(matchBrowsers("chrome > 79, not chrome >= 100", data).join(" | "));\n'
                'console.log(matchBrowsers("safari 15", data).length);\n'
                'console.log(matchBrowsers("ie <= 11, not ie 10", data).join(" | "));\n'
                'console.log(matchBrowsers("", data).length);\n',
      'hint': 'Разберите каждый запрос регулярным выражением, накапливайте набор в Map по строковому ключу '
              '«name version».',
      'expected': ['chrome 80 | chrome 81 | chrome 100 | firefox 78 | firefox 80 | ie 11',
                   'chrome 78 | chrome 79',
                   'chrome 80 | chrome 81',
                   '0',
                   'ie 11',
                   '0']},
     {'id': 'j3-support-table',
      'mode': 'js',
      'title': 'Поддержка возможности браузерами',
      'statement': 'Таблица минимальных версий: { arrow: { chrome: 45, firefox: 22, ie: null }, … } (null — '
                   'не поддерживается никогда). Напишите функцию unsupported(table, features, browsers): '
                   'browsers — массив { name, version }; верните отсортированный массив строк «feature → '
                   'name version» для каждой пары (возможность, браузер), где браузер не поддерживает '
                   'возможность. Браузер, которого нет в таблице возможности, считается не поддерживающим.',
      'starter': 'function unsupported(table, features, browsers) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const table = { arrow: { chrome: 45, firefox: 22, ie: null }, class: { chrome: 49, firefox: '
                '45 }, optional: { chrome: 80, firefox: 74 } };\n'
                'const br = [{ name: "chrome", version: 70 }, { name: "firefox", version: 80 }, { name: '
                '"ie", version: 11 }, { name: "safari", version: 15 }];\n'
                'console.log(unsupported(table, ["arrow", "class", "optional"], br).join("\\n"));\n'
                'console.log(unsupported(table, [], br).length);\n'
                'console.log(unsupported(table, ["arrow"], [{ name: "chrome", version: 45 }]).length);\n',
      'hint': 'Минимум для пары — table[feature]?.[browser]; null/undefined = не поддерживается.',
      'expected': ['arrow → ie 11',
                   'arrow → safari 15',
                   'class → ie 11',
                   'class → safari 15',
                   'optional → chrome 70',
                   'optional → ie 11',
                   'optional → safari 15',
                   '0',
                   '0']},
     {'id': 'j3-find-imports',
      'mode': 'js',
      'title': 'Поиск зависимостей в файле',
      'statement': 'Напишите функцию findImports(src): возвращает массив строк-путей, подключаемых в '
                   'исходнике: require(\'x\'), require("x"), import x from \'y\', import { a } from \'y\', '
                   "import 'y' и динамический import('y'); без повторов, в порядке появления. Строки внутри "
                   'комментариев игнорируйте (// … и /* … */).',
      'starter': 'function findImports(src) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                "console.log(JSON.stringify(findImports(`const a = require('./a');\\nconst b = "
                'require("b");\\nimport c from \'c\';\\nimport { d, e } from "./d.js";\\nimport * as f from '
                "'f';\\nimport 'side-effect';\\nconst g = await import('g');\\nrequire('./a');`)));\n"
                "console.log(JSON.stringify(findImports(`// import x from 'nope'\\n/* require('no') "
                "*/\\nimport y from 'yes'; // import z from 'no2'`)));\n"
                'console.log(JSON.stringify(findImports("const x = 1;")));\n'
                "console.log(JSON.stringify(findImports(`import def, { n } from 'm';`)));\n",
      'hint': 'Сначала удалите комментарии, затем одна регулярка с тремя вариантами: require, динамический '
              'import, статический import.',
      'expected': ['["./a","b","c","./d.js","f","side-effect","g"]', '["yes"]', '[]', '["m"]']},
     {'id': 'j3-build-graph',
      'mode': 'js',
      'title': 'Граф модулей для бандла',
      'statement': 'Напишите функцию buildOrder(files, entry): files — объект «путь → исходник», где '
                   "зависимости подключены через require('./x') (путь относительно корня без расширения: "
                   '«./a» → ключ «a.js»); верните массив путей в порядке для склейки: зависимости раньше '
                   'зависящих, каждый модуль один раз, обход от entry. Циклы допустимы (тогда модуль уже в '
                   'обработке — пропускается). Для отсутствующего модуля бросьте Error("нет модуля: '
                   '<путь>").',
      'starter': 'function buildOrder(files, entry) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const files = {\n'
                '  "main.js": "const a = require(\'./a\'); const u = require(\'./util\');",\n'
                '  "a.js": "const u = require(\'./util\'); const b = require(\\"./b\\");",\n'
                '  "b.js": "const a = require(\'./a\');",\n'
                '  "util.js": "module.exports = 1;",\n'
                '  "unused.js": "require(\'./util\');",\n'
                '};\n'
                'console.log(buildOrder(files, "main.js").join(" "));\n'
                'console.log(buildOrder(files, "util.js").join(" "));\n'
                'try { buildOrder({ "m.js": "require(\'./zzz\')" }, "m.js"); } catch (e) { '
                'console.log(e.message); }\n'
                'console.log(buildOrder({ "solo.js": "" }, "solo.js").join());\n',
      'hint': 'Поиск в глубину: сначала посетите все require, потом добавьте сам файл; помечайте посещённые '
              'заранее.',
      'expected': ['util.js b.js a.js main.js', 'util.js', 'нет модуля: zzz.js', 'solo.js']},
     {'id': 'j3-tree-shake',
      'mode': 'js',
      'title': 'Tree shaking',
      'statement': 'Модули описаны так: { имя: { exports: [имена], uses: { другойМодуль: [использованные '
                   'имена] } } }. Напишите функцию unusedExports(modules, entry): считается, что entry '
                   'использует все свои экспорты; верните объект «модуль → массив неиспользуемых экспортов» '
                   'только для достижимых от entry модулей, где они есть (имена в порядке объявления, модули '
                   '— в порядке имён). Экспорты модуля, который использован целиком (в uses стоит "*"), '
                   'используются все. Использование считается транзитивным: модуль участвует, только если на '
                   'него ссылается достижимый модуль.',
      'starter': 'function unusedExports(modules, entry) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const mods = {\n'
                '  main: { exports: ["run"], uses: { lib: ["map"], all: ["*"] } },\n'
                '  lib: { exports: ["map", "filter", "reduce"], uses: { deep: ["helper"] } },\n'
                '  deep: { exports: ["helper", "spare"], uses: {} },\n'
                '  all: { exports: ["a", "b"], uses: {} },\n'
                '  dead: { exports: ["x"], uses: { lib: ["filter"] } },\n'
                '};\n'
                'console.log(JSON.stringify(unusedExports(mods, "main")));\n'
                'console.log(JSON.stringify(unusedExports(mods, "dead")));\n'
                'console.log(JSON.stringify(unusedExports({ e: { exports: [], uses: {} } }, "e")));\n',
      'hint': 'Обход от entry: накапливайте множество использованных имён для каждого модуля, «*» означает '
              'все экспорты.',
      'expected': ['{"deep":["spare"],"lib":["filter","reduce"]}',
                   '{"deep":["spare"],"lib":["map","reduce"]}',
                   '{}']},
     {'id': 'j3-minify-js',
      'mode': 'js',
      'title': 'Минификатор комментариев',
      'statement': 'Напишите функцию stripComments(src): удаляет комментарии «// …» до конца строки и «/* … '
                   '*/» из исходника, не трогая такие же последовательности внутри строк в одинарных, '
                   'двойных и обратных кавычках; затем удаляет пустые (из одних пробелов) строки и пробелы в '
                   'конце строк. Остальной текст не менять.',
      'starter': 'function stripComments(src) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(stripComments("var a = 1; // один\\n/* блок\\nна строки */\\nvar b = '
                '\'http://x.ru\'; /* c */\\n\\n   \\nvar s = \\"a // b /* c */\\";"));\n'
                'console.log(JSON.stringify(stripComments("// только комментарий")));\n'
                'console.log(stripComments("let t = `шаблон // не комментарий`;"));\n'
                'console.log(stripComments("x = 1;/* a */y = 2;"));\n'
                'console.log(JSON.stringify(stripComments("")));\n',
      'hint': 'Проходите по символам: строки копируйте целиком, комментарии пропускайте.',
      'expected': ['var a = 1;',
                   "var b = 'http://x.ru';",
                   'var s = "a // b /* c */";',
                   '""',
                   'let t = `шаблон // не комментарий`;',
                   'x = 1;y = 2;',
                   '""']},
     {'id': 'j3-concat-map',
      'mode': 'js',
      'title': 'Склейка файлов с картой строк',
      'statement': 'Напишите функцию concatFiles(files): files — массив { name, code }; верните { code, map '
                   '}: code — все файлы подряд, между файлами одна пустая строка-разделитель «// ----» (не '
                   'входит ни в один файл); map — массив для каждой строки итогового кода: [имя файла, номер '
                   'строки в файле с 1] или null для строк-разделителей. Это упрощённая source map.',
      'starter': 'function concatFiles(files) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const r = concatFiles([{ name: "a.js", code: "var a = 1;\\nvar b = 2;" }, { name: "b.js", '
                'code: "run();" }, { name: "c.js", code: "x;\\ny;" }]);\n'
                'console.log(r.code);\n'
                'console.log(JSON.stringify(r.map));\n'
                'const e = concatFiles([]);\n'
                'console.log(JSON.stringify(e));\n',
      'hint': 'Обходите файлы и строки; перед каждым файлом, кроме первого, вставляйте разделитель.',
      'expected': ['var a = 1;',
                   'var b = 2;',
                   '// ----',
                   'run();',
                   '// ----',
                   'x;',
                   'y;',
                   '[["a.js",1],["a.js",2],null,["b.js",1],null,["c.js",1],["c.js",2]]',
                   '{"code":"","map":[]}']},
     {'id': 'j3-hash-name',
      'mode': 'js',
      'title': 'Имя файла с хешем содержимого',
      'statement': 'Для сброса кэша имя файла получают из хеша содержимого. Напишите функцию '
                   'hashedName(name, content): считает 32-битный хеш FNV-1a по символам строки (кодовые '
                   'единицы UTF-16: h = 2166136261; для каждой: h ^= код; h = (h * 16777619) >>> 0 через '
                   'Math.imul), берёт 8 шестнадцатеричных цифр в нижнем регистре и вставляет перед последней '
                   'точкой имени: («app.js», …) → «app.1a2b3c4d.js»; без точки — добавляет в конец через '
                   'точку.',
      'starter': 'function hashedName(name, content) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(hashedName("app.js", ""));\n'
                'console.log(hashedName("app.js", "a"));\n'
                'console.log(hashedName("main.min.css", "body{}"));\n'
                'console.log(hashedName("LICENSE", "MIT"));\n'
                'console.log(hashedName("app.js", "var x = 1;") === hashedName("app.js", "var x = 1;"), '
                'hashedName("a.js", "x") === hashedName("a.js", "y"));\n'
                'console.log(hashedName("p.js", "привет"));\n',
      'hint': 'h ^= code; h = Math.imul(h, 16777619) >>> 0; затем toString(16) с дополнением нулями до 8 '
              'цифр.',
      'expected': ['app.811c9dc5.js',
                   'app.e40c292c.js',
                   'main.min.c9b8fe55.css',
                   'LICENSE.18460475',
                   'true false',
                   'p.9015dafb.js']},
     {'id': 'j3-gulp-stream',
      'mode': 'js',
      'title': 'Мини-Gulp: конвейер преобразований файлов',
      'statement': 'Напишите класс Stream(files): files — массив { name, content }. Метод pipe(transform) — '
                   'транспонирует каждый файл: transform(file) возвращает новый файл (или null — тогда файл '
                   'отбрасывается); возвращает новый Stream, исходный не меняется. Метод run() возвращает '
                   'массив файлов. Вычисления откладываются до run().',
      'starter': 'class Stream {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'let calls = 0;\n'
                'const src = new Stream([{ name: "a.js", content: "x" }, { name: "b.css", content: "y" }, { '
                'name: "c.js", content: "z" }]);\n'
                'const onlyJs = (f) => { calls++; return f.name.endsWith(".js") ? f : null; };\n'
                'const upper = (f) => ({ ...f, content: f.content.toUpperCase() });\n'
                'const rename = (f) => ({ ...f, name: f.name.replace(".js", ".min.js") });\n'
                'const p = src.pipe(onlyJs).pipe(upper);\n'
                'console.log(calls);\n'
                'console.log(JSON.stringify(p.run()));\n'
                'console.log(calls);\n'
                'console.log(JSON.stringify(p.pipe(rename).run().map((f) => f.name)));\n'
                'console.log(JSON.stringify(src.run().length));\n',
      'hint': 'Храните список шагов; run применяет их по очереди к копиям файлов и отбрасывает null.',
      'expected': ['0',
                   '[{"name":"a.js","content":"X"},{"name":"c.js","content":"Z"}]',
                   '3',
                   '["a.min.js","c.min.js"]',
                   '3']},
     {'id': 'j3-task-runner',
      'mode': 'js',
      'title': 'Мини-Grunt: запуск задач с зависимостями',
      'statement': 'Напишите класс Runner: task(name, deps, fn) регистрирует задачу (deps — массив имён, fn '
                   '— функция без аргументов); run(name) выполняет задачу после зависимостей — каждую задачу '
                   'не более одного раза за вызов run, в порядке перечисления зависимостей; возвращает '
                   'массив имён в порядке выполнения. Неизвестная задача — Error("нет задачи: <имя>"), цикл '
                   '— Error("цикл: <a> → <b> …") с цепочкой имён.',
      'starter': 'class Runner {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const log = [];\n'
                'const r = new Runner()\n'
                '  .task("clean", [], () => log.push("clean"))\n'
                '  .task("sass", ["clean"], () => log.push("sass"))\n'
                '  .task("js", ["clean"], () => log.push("js"))\n'
                '  .task("build", ["sass", "js"], () => log.push("build"))\n'
                '  .task("a", ["b"], () => {})\n'
                '  .task("b", ["c"], () => {})\n'
                '  .task("c", ["a"], () => {});\n'
                'console.log(r.run("build").join(" "));\n'
                'console.log(log.join(" "));\n'
                'console.log(r.run("sass").join(" "));\n'
                'for (const n of ["a", "zzz"]) { try { r.run(n); } catch (e) { console.log(e.message); } }\n',
      'hint': 'Обход в глубину со стеком для обнаружения цикла и множеством выполненных задач.',
      'expected': ['clean sass js build',
                   'clean sass js build',
                   'clean sass',
                   'цикл: a → b → c → a',
                   'нет задачи: zzz']},
     {'id': 'j3-scss-vars',
      'mode': 'js',
      'title': 'Sass: переменные',
      'statement': 'Напишите функцию compileVars(scss): строки вида «$имя: значение;» объявляют переменные '
                   '(значение может содержать другие переменные); в остальном тексте $имя заменяется '
                   'значением; сами объявления из результата удаляются (вместе со строкой). Переопределение '
                   '— позднее значение действует для последующих строк. Необъявленная переменная остаётся '
                   'как есть.',
      'starter': 'function compileVars(scss) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(compileVars("$main: #36c;\\n$gap: 8px;\\n.a { color: $main; margin: $gap; '
                '}\\n.b { padding: $gap $gap; border-color: $main }"));\n'
                'console.log("---");\n'
                'console.log(compileVars("$a: 1px;\\n$b: $a solid;\\n.x { border: $b; }\\n$a: 5px;\\n.y { '
                'top: $a; }"));\n'
                'console.log("---");\n'
                'console.log(compileVars(".z { color: $nope; }"));\n',
      'hint': 'Разбирайте построчно: объявление сохраняет значение (с подстановкой), остальные строки '
              'подставляют.',
      'expected': ['.a { color: #36c; margin: 8px; }',
                   '.b { padding: 8px 8px; border-color: #36c }',
                   '---',
                   '.x { border: 1px solid; }',
                   '.y { top: 5px; }',
                   '---',
                   '.z { color: $nope; }']},
     {'id': 'j3-scss-nesting',
      'mode': 'js',
      'title': 'Мини-Sass: вложенные правила',
      'statement': 'Напишите функцию flattenScss(scss): вход — упрощённый SCSS без переменных, где правила '
                   'вложены: «.nav { color: red; a { color: blue; &:hover { color: green; } } }»; на выходе '
                   '— плоский CSS, где у вложенных селекторов склеены родительские: «.nav a», «&» заменяется '
                   'родителем («.nav a:hover»). Выводите правила в порядке появления (родитель — до детей, '
                   'если у него есть свои объявления), формат каждого: «селектор { объявление; объявление; '
                   '}» в одной строке, правила разделены переводом строки. Селекторы через запятую не '
                   'используйте.',
      'starter': 'function flattenScss(scss) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(flattenScss(".nav { color: red; a { color: blue; &:hover { color: green; } } '
                '}"));\n'
                'console.log("---");\n'
                'console.log(flattenScss(".a { .b { .c { x: 1; } } }"));\n'
                'console.log("---");\n'
                'console.log(flattenScss(".card { padding: 4px; margin: 0; .title { font-size: 20px; } &.big '
                '{ padding: 8px; } }\\n.footer { color: gray; }"));\n'
                'console.log("---");\n'
                'console.log(flattenScss(""));\n',
      'hint': 'Рекурсивный разбор: текст до «{» — селектор вложенного правила; «&» заменяйте на родительский '
              'селектор.',
      'expected': ['.nav { color: red; }',
                   '.nav a { color: blue; }',
                   '.nav a:hover { color: green; }',
                   '---',
                   '.a .b .c { x: 1; }',
                   '---',
                   '.card { padding: 4px; margin: 0; }',
                   '.card .title { font-size: 20px; }',
                   '.card.big { padding: 8px; }',
                   '.footer { color: gray; }',
                   '---']},
     {'id': 'j3-autoprefix',
      'mode': 'js',
      'title': 'Autoprefixer',
      'statement': 'Напишите функцию autoprefix(css, table): css — плоский CSS из одной или нескольких строк '
                   '«селектор { свойство: значение; … }» (каждое объявление на одной строке в фигурных '
                   'скобках), table — { свойство: [префиксы] } (например, { "user-select": ["-webkit-", '
                   '"-moz-"] }); для каждого объявления, свойство которого есть в таблице, перед ним '
                   'добавляются копии с префиксами (в порядке таблицы), затем оригинал. Значение копируйте '
                   'без изменений.',
      'starter': 'function autoprefix(css, table) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const table = { "user-select": ["-webkit-", "-moz-"], transform: ["-webkit-"] };\n'
                'console.log(autoprefix(".a { user-select: none; color: red; }", table));\n'
                'console.log(autoprefix(".b { transform: rotate(5deg); }\\n.c { margin: 0 }", table));\n'
                'console.log(autoprefix("", table));\n'
                'console.log(autoprefix(".d { color: red; }", {}));\n',
      'hint': 'Для каждого объявления внутри { … } вставьте варианты с префиксами перед оригиналом.',
      'expected': ['.a { -webkit-user-select: none; -moz-user-select: none; user-select: none; color: red; }',
                   '.b { -webkit-transform: rotate(5deg); transform: rotate(5deg); }',
                   '.c { margin: 0; }',
                   '',
                   '.d { color: red; }']},
     {'id': 'j3-minify-css',
      'mode': 'js',
      'title': 'Минификатор CSS',
      'statement': 'Напишите функцию minifyCss(css): удаляет комментарии /* … */, лишние пробелы и переводы '
                   'строк; пробелы вокруг «{ } : ; ,» убираются (кроме пробелов внутри значений между '
                   'словами: «margin: 0 auto» → «margin:0 auto»); последняя «;» перед «}» удаляется. Строки '
                   'в кавычках не трогайте.',
      'starter': 'function minifyCss(css) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(minifyCss(".a {\\n  color : red;\\n  margin: 0   auto;\\n}\\n\\n/* комментарий '
                '*/\\n.b,\\n.c { padding: 0 }"));\n'
                'console.log(minifyCss(\'.q::before { content: "a  b ; c"; }\'));\n'
                'console.log(JSON.stringify(minifyCss("")));\n'
                'console.log(minifyCss("a{b:c;d:e;}"));\n',
      'hint': 'Удалите комментарии, затем сожмите пробелы вне строк и уберите их вокруг знаков { } : ; ,',
      'expected': ['.a{color:red;margin:0 auto}.b,.c{padding:0}',
                   '.q::before{content:"a  b ; c"}',
                   '""',
                   'a{b:c;d:e}']},
     {'id': 'j3-left-pad',
      'mode': 'js',
      'title': 'left-pad: те самые 11 строк',
      'statement': 'Напишите функцию leftPad(str, len, ch = " "): добавляет ch слева, пока длина строки '
                   'меньше len (str приводится к строке; ch — один символ или строка; пустая ch считается '
                   'пробелом; если len не число или не больше длины строки — вернуть строку как есть). '
                   'padStart использовать нельзя.',
      'starter': 'function leftPad(str, len, ch = " ") {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(leftPad("5", 3, "0"), leftPad("abc", 2), leftPad(7, 4, "*"), leftPad("x", 4, '
                '""), leftPad("a", NaN, "-"));\n'
                'console.log("[" + leftPad("x", 4) + "]", leftPad("1", 6, "ab"), leftPad("", 2, "z"), '
                'leftPad("long", 2, "0"));\n'
                'console.log(__count(".padS" + "tart("));\n',
      'hint': 'Цикл накопления: pad += ch, пока pad.length + str.length < len.',
      'expected': ['005 abc ***7    x a', '[   x] ababa1 zz long', '0']},
     {'id': 'j3-dependents',
      'mode': 'js',
      'title': 'Кто сломается, если удалить пакет',
      'statement': 'Зависимости заданы графом { пакет: [его зависимости] }. Напишите функцию brokenBy(graph, '
                   'removed): отсортированный массив всех пакетов, которые прямо или косвенно зависят от '
                   'removed (сам removed не включается). Пример: после удаления left-pad ломаются все, кто '
                   'его подключил, и все, кто подключил их.',
      'starter': 'function brokenBy(graph, removed) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const g = { app: ["react", "webpack"], react: ["object-assign"], webpack: ["babel-core", '
                '"left-pad"], "babel-core": ["left-pad", "lodash"], lodash: [], "left-pad": [], '
                '"object-assign": [], tool: ["lodash"] };\n'
                'console.log(JSON.stringify(brokenBy(g, "left-pad")));\n'
                'console.log(JSON.stringify(brokenBy(g, "lodash")));\n'
                'console.log(JSON.stringify(brokenBy(g, "app")));\n'
                'console.log(JSON.stringify(brokenBy({ a: ["b"], b: ["a"] }, "a")));\n'
                'console.log(JSON.stringify(brokenBy(g, "нет-такого")));\n',
      'hint': 'Постройте обратный граф и обойдите его от удаляемого пакета.',
      'expected': ['["app","babel-core","webpack"]',
                   '["app","babel-core","tool","webpack"]',
                   '[]',
                   '["b"]',
                   '[]']},
     {'id': 'j3-module-format',
      'mode': 'js',
      'title': 'Формат модуля по исходнику',
      'statement': 'Напишите функцию moduleFormat(src): «esm» — если есть import … from или export на уровне '
                   'строки; «amd» — если есть вызов define([…], function…) или define(function…); «umd» — '
                   'если одновременно встречаются «module.exports» (или exports) и «define.amd»; «cjs» — '
                   'если есть require( или module.exports/exports.; «iife» — если код начинается с '
                   '«(function» или «!function»; иначе «script». Проверяйте в порядке: umd, amd, esm, cjs, '
                   'iife.',
      'starter': 'function moduleFormat(src) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const t = [\n'
                '  "import a from \'./a\';\\nexport default a;",\n'
                '  "export const x = 1;",\n'
                '  "const a = require(\'a\');\\nmodule.exports = a;",\n'
                '  "exports.f = function () {};",\n'
                '  "define([\'jquery\'], function ($) { return {}; });",\n'
                '  "define(function (require) {});",\n'
                '  "(function (root, factory) { if (typeof define === \'function\' && define.amd) { '
                "define([], factory); } else if (typeof module === 'object') { module.exports = factory(); } "
                '})(this, function () {});",\n'
                '  "(function () { var a = 1; })();",\n'
                '  "!function () {}();",\n'
                '  "var x = 1;",\n'
                '];\n'
                'for (const s of t) console.log(moduleFormat(s));\n',
      'hint': 'Порядок проверок важен: UMD содержит и define, и module.exports.',
      'expected': ['esm', 'esm', 'cjs', 'cjs', 'amd', 'amd', 'umd', 'iife', 'iife', 'script']},
     {'id': 'j3-coffee',
      'mode': 'js',
      'title': 'Мини-CoffeeScript',
      'statement': 'Напишите функцию coffeeToJs(src): переводит строки вида «имя = (a, b) -> выражение» и '
                   '«имя = (a) -> выражение» и «имя = -> выражение» в «var имя = function (a, b) { return '
                   'выражение; };», а строки «имя = значение» (без стрелки) — в «var имя = значение;». '
                   'Пустые строки сохраняются; остальные строки оставляйте без изменения. Результат — '
                   'строки, склеенные через перевод строки.',
      'starter': 'function coffeeToJs(src) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(coffeeToJs("square = (x) -> x * x\\nadd = (a, b) -> a + b\\nnow = -> '
                'Date.now()\\nanswer = 42\\n\\nname = \'Ада\'\\nconsole.log square 5"));\n'
                'console.log(JSON.stringify(coffeeToJs("")));\n',
      'hint': 'Две регулярки: сначала со стрелкой, затем простое присваивание.',
      'expected': ['var square = function (x) { return x * x; };',
                   'var add = function (a, b) { return a + b; };',
                   'var now = function () { return Date.now(); };',
                   'var answer = 42;',
                   '',
                   "var name = 'Ада';",
                   'console.log square 5',
                   '""']},
     {'id': 'j3-vlq',
      'mode': 'js',
      'title': 'Source map: VLQ Base64',
      'statement': 'Карты кода хранят числа в формате Base64 VLQ. Напишите функции vlqEncode(n) и '
                   'vlqDecode(str): число переводится в знаково-беззнаковое (n < 0 → ((-n) << 1) | 1, иначе '
                   'n << 1), затем выдаётся группами по 5 бит от младших к старшим; в каждой группе бит 5 '
                   '(значение 32) — «продолжение»; группы кодируются алфавитом Base64 «A–Za–z0–9+/». '
                   'vlqDecode(str) возвращает массив чисел из строки, закодированной подряд.',
      'starter': 'function vlqEncode(n) {\n}\nfunction vlqDecode(str) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const n of [0, 1, -1, 2, 15, 16, -16, 123, -123, 1000, 100000]) console.log(n, '
                'vlqEncode(n), JSON.stringify(vlqDecode(vlqEncode(n))));\n'
                'console.log(JSON.stringify(vlqDecode("AAAA")), JSON.stringify(vlqDecode("AACA")), '
                'JSON.stringify(vlqDecode("2HAAA")));\n'
                'console.log(JSON.stringify(vlqDecode("")));\n',
      'hint': '5 бит на цифру: младшие 5 бит значения + бит продолжения 32, если остались старшие биты.',
      'expected': ['0 A [0]',
                   '1 C [1]',
                   '-1 D [-1]',
                   '2 E [2]',
                   '15 e [15]',
                   '16 gB [16]',
                   '-16 hB [-16]',
                   '123 2H [123]',
                   '-123 3H [-123]',
                   '1000 w+B [1000]',
                   '100000 gqjG [100000]',
                   '[0,0,0,0] [0,0,1,0] [123,0,0,0]',
                   '[]']}]}
