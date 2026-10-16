"""Задачи книги «Современный Frontend», глава 1 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {1: [{'id': 'j1-iife-counter',
      'mode': 'js',
      'title': 'Модуль на замыкании (IIFE)',
      'statement': 'Создайте переменную counter — результат немедленно вызываемой функции: объект с методами '
                   'inc() (увеличивает счётчик и возвращает его), reset() и value(). Сам счётчик снаружи '
                   'недоступен. Пишите в стиле ES3: только var и function — без стрелок, let/const, классов, '
                   'шаблонных строк и spread.',
      'starter': 'var counter;\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'counter.inc(); counter.inc();\n'
                'console.log(counter.value());\n'
                'console.log(counter.inc());\n'
                'counter.reset();\n'
                'console.log(counter.value());\n'
                'console.log(JSON.stringify(Object.keys(counter).sort()));\n'
                'console.log(counter.n);\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'var counter = (function () { var n = 0; return { … }; })();',
      'expected': ['2', '3', '0', '["inc","reset","value"]', 'undefined', 'стиль ES3: ок']},
     {'id': 'j1-bind',
      'mode': 'js',
      'title': 'Полифил Function.prototype.bind',
      'statement': 'Напишите функцию bindFn(fn, ctx) (дополнительные аргументы запоминаются): возвращает '
                   'функцию, вызывающую fn с this = ctx, сначала с запомненными аргументами, затем с '
                   'переданными позже. Метод bind использовать нельзя. Пишите в стиле ES3: только var и '
                   'function — без стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function bindFn(fn, ctx) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'function hi(greet, punct) { return greet + ", " + this.name + punct; }\n'
                'var f = bindFn(hi, { name: "Ада" }, "Привет");\n'
                'console.log(f("!"));\n'
                'console.log(bindFn(hi, { name: "Б" })("Здравствуй", "?"));\n'
                'console.log(bindFn(function () { return arguments.length; }, null, 1, 2)(3));\n'
                'console.log(__count(".bi" + "nd("));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Array.prototype.slice.call(arguments, 2) и fn.apply(ctx, …)',
      'expected': ['Привет, Ада!', 'Здравствуй, Б?', '3', '0', 'стиль ES3: ок']},
     {'id': 'j1-object-create',
      'mode': 'js',
      'title': 'Полифил Object.create (по Крокфорду)',
      'statement': 'Напишите функцию objectFrom(proto): возвращает новый пустой объект, прототип которого — '
                   'proto. Object.create использовать нельзя: сделайте временный конструктор. Пишите в стиле '
                   'ES3: только var и function — без стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function objectFrom(proto) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var base = { kind: "base", hi: function () { return "hi " + this.name; } };\n'
                'var o = objectFrom(base);\n'
                'o.name = "Ада";\n'
                'console.log(o.hi(), o.kind, Object.hasOwn(o, "kind"));\n'
                'console.log(Object.getPrototypeOf(o) === base);\n'
                'console.log(base.isPrototypeOf(o));\n'
                'console.log(__count("Object" + ".create"));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'function F() {} F.prototype = proto; return new F();',
      'expected': ['hi Ада base false', 'true', 'true', '0', 'стиль ES3: ок']},
     {'id': 'j1-map-es3',
      'mode': 'js',
      'title': 'map в стиле ES3',
      'statement': 'Напишите функцию mapES3(arr, fn, thisArg): возвращает новый массив результатов '
                   'fn.call(thisArg, элемент, индекс, массив) для каждого элемента; дыры в разреженном '
                   'массиве пропускаются (в результате тоже остаются дырами). Метод map использовать нельзя. '
                   'Пишите в стиле ES3: только var и function — без стрелок, let/const, классов, шаблонных '
                   'строк и spread.',
      'starter': 'function mapES3(arr, fn, thisArg) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(JSON.stringify(mapES3([1, 2, 3], function (x) { return x * 2; })));\n'
                'console.log(JSON.stringify(mapES3(["a", "b"], function (x, i) { return x + i; })));\n'
                'console.log(JSON.stringify(mapES3([1, 2], function (x) { return x * this.k; }, { k: 10 '
                '})));\n'
                'var sparse = [1, , 3];\n'
                'var r = mapES3(sparse, function (x) { return x + 1; });\n'
                'console.log(r.length, 1 in r, JSON.stringify(r));\n'
                'console.log(__count(".m" + "ap("));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Проверяйте i in arr — так пропускаются дыры.',
      'expected': ['[2,4,6]', '["a0","b1"]', '[10,20]', '3 false [2,null,4]', '0', 'стиль ES3: ок']},
     {'id': 'j1-filter-es3',
      'mode': 'js',
      'title': 'filter в стиле ES3',
      'statement': 'Напишите функцию filterES3(arr, pred, thisArg): возвращает новый массив элементов, для '
                   'которых pred.call(thisArg, элемент, индекс, массив) истинно; дыры пропускаются. Метод '
                   'filter использовать нельзя. Пишите в стиле ES3: только var и function — без стрелок, '
                   'let/const, классов, шаблонных строк и spread.',
      'starter': 'function filterES3(arr, pred, thisArg) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(JSON.stringify(filterES3([1, 2, 3, 4], function (x) { return x % 2 === 0; '
                '})));\n'
                'console.log(JSON.stringify(filterES3(["a", "b", "c"], function (x, i) { return i !== 1; '
                '})));\n'
                'console.log(JSON.stringify(filterES3([5, 6, 7], function (x) { return x > this.min; }, { '
                'min: 5 })));\n'
                'console.log(JSON.stringify(filterES3([1, , 3], function () { return true; })));\n'
                'console.log(__count(".fil" + "ter("));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'i in arr && pred.call(thisArg, arr[i], i, arr)',
      'expected': ['[2,4]', '["a","c"]', '[6,7]', '[1,3]', '0', 'стиль ES3: ок']},
     {'id': 'j1-reduce-es3',
      'mode': 'js',
      'title': 'reduce в стиле ES3',
      'statement': 'Напишите функцию reduceES3(arr, fn, init): сворачивает массив слева направо; если init '
                   'не передан (arguments.length < 3), первый элемент служит начальным значением; для '
                   'пустого массива без init бросьте TypeError. Метод reduce использовать нельзя. Пишите в '
                   'стиле ES3: только var и function — без стрелок, let/const, классов, шаблонных строк и '
                   'spread.',
      'starter': 'function reduceES3(arr, fn, init) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var add = function (a, b) { return a + b; };\n'
                'console.log(reduceES3([1, 2, 3, 4], add, 0));\n'
                'console.log(reduceES3([1, 2, 3, 4], add));\n'
                'console.log(reduceES3([], add, 7));\n'
                'try { reduceES3([], add); } catch (e) { console.log(e.name); }\n'
                'console.log(reduceES3(["a", "b"], function (a, x, i) { return a + x + i; }, ""));\n'
                'console.log(reduceES3([5], add));\n'
                'console.log(__count(".red" + "uce("));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'arguments.length отличает «init не передан» от «init равен undefined».',
      'expected': ['10', '10', '7', 'TypeError', 'a0b1', '5', '0', 'стиль ES3: ок']},
     {'id': 'j1-indexof',
      'mode': 'js',
      'title': 'Полифил indexOf',
      'statement': 'Напишите функцию indexOfES3(arr, x, from): индекс первого элемента, строго равного x, '
                   'начиная с позиции from (по умолчанию 0); отрицательное from отсчитывается от конца; если '
                   'не найден — -1. Метод indexOf использовать нельзя. Пишите в стиле ES3: только var и '
                   'function — без стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function indexOfES3(arr, x, from) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var a = [1, 2, 3, 2, 1];\n'
                'console.log(indexOfES3(a, 2), indexOfES3(a, 2, 2), indexOfES3(a, 2, 4), indexOfES3(a, 9));\n'
                'console.log(indexOfES3(a, 1, -1), indexOfES3(a, 1, -10), indexOfES3(a, 3, -3));\n'
                'console.log(indexOfES3([NaN], NaN), indexOfES3([], 1), indexOfES3(["1"], 1));\n'
                'console.log(__count(".ind" + "exOf("));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Нормализуйте from: при отрицательном — max(0, n + from).',
      'expected': ['1 3 -1 -1', '4 0 2', '-1 -1 -1', '0', 'стиль ES3: ок']},
     {'id': 'j1-trim',
      'mode': 'js',
      'title': 'Полифил trim',
      'statement': 'Напишите функцию trimES3(s): убирает пробельные символы (пробелы, табуляции, переводы '
                   'строк) в начале и в конце строки регулярным выражением. Метод trim использовать нельзя. '
                   'Пишите в стиле ES3: только var и function — без стрелок, let/const, классов, шаблонных '
                   'строк и spread.',
      'starter': 'function trimES3(s) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log("[" + trimES3("  привет  ") + "]");\n'
                'console.log("[" + trimES3("\\t\\n x y \\n") + "]");\n'
                'console.log("[" + trimES3("") + "]");\n'
                'console.log("[" + trimES3("   ") + "]");\n'
                'console.log("[" + trimES3("a b") + "]");\n'
                'console.log(__count(".tr" + "im("));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 's.replace(/^\\s+|\\s+$/g, "")',
      'expected': ['[привет]', '[x y]', '[]', '[]', '[a b]', '0', 'стиль ES3: ок']},
     {'id': 'j1-keys',
      'mode': 'js',
      'title': 'Полифил Object.keys',
      'statement': 'Напишите функцию keysES3(obj): массив собственных перечисляемых ключей объекта в порядке '
                   'перебора for…in; унаследованные ключи пропускайте (hasOwnProperty). Object.keys '
                   'использовать нельзя. Пишите в стиле ES3: только var и function — без стрелок, let/const, '
                   'классов, шаблонных строк и spread.',
      'starter': 'function keysES3(obj) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'function P() { this.own = 1; }\n'
                'P.prototype.inherited = 2;\n'
                'var p = new P();\n'
                'p.extra = 3;\n'
                'console.log(JSON.stringify(keysES3(p)));\n'
                'console.log(JSON.stringify(keysES3({})));\n'
                'console.log(JSON.stringify(keysES3({ b: 1, a: 2, 10: 3, 2: 4 })));\n'
                'console.log(__count("Object" + ".keys("));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Проверка Object.prototype.hasOwnProperty.call(obj, k) внутри for (var k in obj).',
      'expected': ['["own","extra"]', '[]', '["2","10","b","a"]', '0', 'стиль ES3: ок']},
     {'id': 'j1-call',
      'mode': 'js',
      'title': 'Свой call через временное свойство',
      'statement': 'Напишите функцию callFn(fn, ctx) (остальные аргументы передаются fn): вызывает fn так, '
                   'чтобы внутри this был ctx, без call, apply и bind. Подсказка: положите fn во временное '
                   'свойство ctx и вызовите как метод, затем удалите. Пишите в стиле ES3: только var и '
                   'function — без стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function callFn(fn, ctx) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'function intro(a, b) { return this.name + ":" + a + b; }\n'
                'var o = { name: "Ада" };\n'
                'console.log(callFn(intro, o, 1, 2));\n'
                'console.log(callFn(function () { return arguments.length; }, o));\n'
                'console.log(JSON.stringify(Object.keys(o)));\n'
                'console.log(__count(".ca" + "ll(") + __count(".ap" + "ply(") + __count(".bi" + "nd("));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'ctx[key] = fn; ctx[key](…); delete ctx[key]. Передачу произвольного числа аргументов в ES3 '
              'решали через eval — или подставьте нужное число вариантов вручную.',
      'expected': ['Ада:12', '0', '["name"]', '0', 'стиль ES3: ок']},
     {'id': 'j1-query-string',
      'mode': 'js',
      'title': 'Строка запроса: разбор и сборка',
      'statement': 'Напишите функции parseQuery(s) («a=1&b=%D0%B0&c», начальный «?» допустим) → объект со '
                   'значениями-строками (отсутствие «=» даёт пустую строку; повторяющийся ключ — последнее '
                   'значение) и buildQuery(obj) → строка «k=v&k2=v2» с кодированием encodeURIComponent. '
                   'Пишите в стиле ES3: только var и function — без стрелок, let/const, классов, шаблонных '
                   'строк и spread.',
      'starter': 'function parseQuery(s) {\n}\nfunction buildQuery(obj) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(JSON.stringify(parseQuery("?a=1&b=%D0%B0%D0%B1&c")));\n'
                'console.log(JSON.stringify(parseQuery("x=1&x=2")));\n'
                'console.log(JSON.stringify(parseQuery("")));\n'
                'console.log(JSON.stringify(parseQuery("k=a=b")));\n'
                'console.log(buildQuery({ q: "привет мир", n: 5 }));\n'
                'console.log(buildQuery({}));\n'
                'console.log(JSON.stringify(parseQuery(buildQuery({ "a&b": "c=d" }))));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'split("&"), затем split("="); не забудьте decodeURIComponent и encodeURIComponent.',
      'expected': ['{"a":"1","b":"аб","c":""}',
                   '{"x":"2"}',
                   '{}',
                   '{"k":"a=b"}',
                   'q=%D0%BF%D1%80%D0%B8%D0%B2%D0%B5%D1%82%20%D0%BC%D0%B8%D1%80&n=5',
                   '',
                   '{"a&b":"c=d"}',
                   'стиль ES3: ок']},
     {'id': 'j1-cookies',
      'mode': 'js',
      'title': 'Разбор document.cookie',
      'statement': 'Напишите функцию parseCookies(str): строка вида «a=1; b=hello%20world; c=» → объект; '
                   'пробелы вокруг пар отбрасываются, значения декодируются decodeURIComponent, пары без «=» '
                   'пропускаются. Пишите в стиле ES3: только var и function — без стрелок, let/const, '
                   'классов, шаблонных строк и spread.',
      'starter': 'function parseCookies(str) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(JSON.stringify(parseCookies("a=1; b=hello%20world; c=")));\n'
                'console.log(JSON.stringify(parseCookies("")));\n'
                'console.log(JSON.stringify(parseCookies("flag; x=%D0%B0")));\n'
                'console.log(JSON.stringify(parseCookies("t=a=b;u=2")));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'split(";"), затем indexOf("=") — значение может содержать «=».',
      'expected': ['{"a":"1","b":"hello world","c":""}',
                   '{}',
                   '{"x":"а"}',
                   '{"t":"a=b","u":"2"}',
                   'стиль ES3: ок']},
     {'id': 'j1-mini-jquery',
      'mode': 'js',
      'title': 'Мини-jQuery на списке узлов',
      'statement': 'Узлы страницы моделируются объектами { tag, classes: [...], text }. Напишите функцию '
                   '$(nodes, selector): возвращает объект-обёртку с методами length (число — геттер не '
                   'нужен, просто поле), each(fn(node, i)), addClass(c), removeClass(c), text() (тексты '
                   'найденных узлов через пробел) и text(value) (записать). Все изменяющие методы возвращают '
                   'обёртку (цепочки). Селекторы: «tag», «.class», «tag.class», «*». Пишите в стиле ES3: '
                   'только var и function — без стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function $(nodes, selector) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var page = [\n'
                '  { tag: "li", classes: ["item", "a"], text: "один" },\n'
                '  { tag: "li", classes: ["item"], text: "два" },\n'
                '  { tag: "p", classes: ["item"], text: "абзац" },\n'
                '  { tag: "li", classes: [], text: "три" },\n'
                '];\n'
                'console.log($(page, "li").length, $(page, ".item").length, $(page, "li.item").length, '
                '$(page, "*").length, $(page, "div").length);\n'
                'console.log($(page, "li.item").text());\n'
                '$(page, "li").addClass("open").removeClass("a");\n'
                'console.log(JSON.stringify(page.map(function (n) { return n.classes; })));\n'
                '$(page, "p").text("новый").addClass("x");\n'
                'console.log(page[2].text, page[2].classes.join());\n'
                'var seen = [];\n'
                '$(page, ".item").each(function (n, i) { seen.push(i + ":" + n.tag); });\n'
                'console.log(seen.join());\n'
                'console.log(typeof $(page, "li").addClass("q").removeClass("q").each);\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Разберите селектор по «.», отфильтруйте узлы и верните объект, чьи методы возвращают его же.',
      'expected': ['3 3 2 4 0',
                   'один два',
                   '[["item","open"],["item","open"],["item"],["open"]]',
                   'новый item,x',
                   '0:li,1:li,2:p',
                   'function',
                   'стиль ES3: ок']},
     {'id': 'j1-fake-xhr',
      'mode': 'js',
      'title': 'Модель XMLHttpRequest',
      'statement': 'Напишите конструктор FakeXHR(server): server — объект «адрес → {status, body}». Методы '
                   'open(method, url) (readyState = 1), send() (синхронно проходит состояния 2, 3, 4; после '
                   'каждого меняет readyState и вызывает onreadystatechange, если он задан; на 4 заполняются '
                   'status и responseText; неизвестный адрес — status 404 и пустой responseText). Начальное '
                   'readyState = 0. Пишите в стиле ES3: только var и function — без стрелок, let/const, '
                   'классов, шаблонных строк и spread.',
      'starter': 'function FakeXHR(server) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var srv = { "/a": { status: 200, body: "OK!" }, "/b": { status: 500, body: "boom" } };\n'
                'var x = new FakeXHR(srv);\n'
                'console.log(x.readyState);\n'
                'var log = [];\n'
                'x.onreadystatechange = function () { log.push(x.readyState); };\n'
                'x.open("GET", "/a");\n'
                'x.send();\n'
                'console.log(log.join(), x.status, x.responseText);\n'
                'var y = new FakeXHR(srv);\n'
                'y.open("GET", "/zzz");\n'
                'y.send();\n'
                'console.log(y.readyState, y.status, JSON.stringify(y.responseText));\n'
                'var z = new FakeXHR(srv);\n'
                'z.open("POST", "/b");\n'
                'z.send();\n'
                'console.log(z.status, z.responseText);\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Метод _set(state) один раз описывает «смена состояния + колбэк».',
      'expected': ['0', '1,2,3,4 200 OK!', '4 404 ""', '500 boom', 'стиль ES3: ок']},
     {'id': 'j1-error-first',
      'mode': 'js',
      'title': 'Колбэки «ошибка первой»',
      'statement': 'Напишите функцию getJson(http, url, cb): http.get(url, function (err, text)) — запрос '
                   '(асинхронный); getJson вызывает cb(err) при ошибке запроса, cb(null, объект) при '
                   'успешном разборе JSON и cb(err) с ошибкой SyntaxError при неверном JSON. cb нужно '
                   'вызвать ровно один раз, даже если сам cb бросит исключение. Пишите в стиле ES3: только '
                   'var и function — без стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function getJson(http, url, cb) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var pages = { "/ok": \'{"a":[1,2]}\', "/bad": "{oops", "/net": null };\n'
                'var http = {\n'
                '  get: function (url, cb) {\n'
                '    setTimeout(function () {\n'
                '      if (pages[url] === null || pages[url] === undefined) cb(new Error("нет сети"));\n'
                '      else cb(null, pages[url]);\n'
                '    }, 5);\n'
                '  },\n'
                '};\n'
                'var calls = 0;\n'
                'function done(label) {\n'
                '  return function (err, data) {\n'
                '    calls++;\n'
                '    console.log(label, err ? err.name + ":" + err.message.slice(0, 7) : "-", '
                'JSON.stringify(data));\n'
                '  };\n'
                '}\n'
                'getJson(http, "/ok", done("ok"));\n'
                'getJson(http, "/bad", done("bad"));\n'
                'getJson(http, "/net", done("net"));\n'
                'setTimeout(function () { console.log("вызовов", calls); }, 50);\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Исключение из JSON.parse ловите отдельно, чтобы cb не вызвался дважды (try вокруг самого cb — '
              'ошибка).',
      'expected': ['стиль ES3: ок',
                   'ok - {"a":[1,2]}',
                   'bad SyntaxError:Expecte undefined',
                   'net Error:нет сет undefined',
                   'вызовов 3']},
     {'id': 'j1-series',
      'mode': 'js',
      'title': 'series: задачи по очереди',
      'statement': 'Напишите функцию series(tasks, done): tasks — функции вида function (cb) { … cb(err, '
                   'result) }; запускайте их строго по очереди (следующую — после вызова cb предыдущей); '
                   'done(err, results) вызывается один раз: после последней задачи с массивом результатов '
                   'или сразу при первой ошибке с этой ошибкой. Пишите в стиле ES3: только var и function — '
                   'без стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function series(tasks, done) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var order = [];\n'
                'function task(name, ms, fail) {\n'
                '  return function (cb) {\n'
                '    order.push("start " + name);\n'
                '    setTimeout(function () {\n'
                '      order.push("end " + name);\n'
                '      cb(fail ? new Error(name) : null, name.toUpperCase());\n'
                '    }, ms);\n'
                '  };\n'
                '}\n'
                'series([task("a", 20), task("b", 5), task("c", 10)], function (err, res) {\n'
                '  console.log(err, JSON.stringify(res));\n'
                '  console.log(order.join(" | "));\n'
                '  order.length = 0;\n'
                '  series([task("x", 5), task("y", 5, true), task("z", 5)], function (err2, res2) {\n'
                '    console.log(err2.message, res2);\n'
                '    console.log(order.join(" | "));\n'
                '    series([], function (e3, r3) { console.log(e3, JSON.stringify(r3)); });\n'
                '  });\n'
                '});\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Рекурсивная функция next(), которая берёт следующую задачу и передаёт ей колбэк, вызывающий '
              'next().',
      'expected': ['стиль ES3: ок',
                   'null ["A","B","C"]',
                   'start a | end a | start b | end b | start c | end c',
                   'y undefined',
                   'start x | end x | start y | end y',
                   'null []']},
     {'id': 'j1-parallel',
      'mode': 'js',
      'title': 'parallel: задачи одновременно',
      'statement': 'Напишите функцию parallel(tasks, done): запускает все задачи (function (cb) { … cb(err, '
                   'result) }) сразу; done(err, results) вызывается один раз: когда завершились все — с '
                   'результатами в порядке задач (а не в порядке завершения), либо при первой ошибке. Пустой '
                   'массив — done(null, []) сразу. Пишите в стиле ES3: только var и function — без стрелок, '
                   'let/const, классов, шаблонных строк и spread.',
      'starter': 'function parallel(tasks, done) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'function t(name, ms, fail) {\n'
                '  return function (cb) { setTimeout(function () { cb(fail ? new Error(name) : null, name); '
                '}, ms); };\n'
                '}\n'
                'var t0 = Date.now();\n'
                'parallel([t("a", 40), t("b", 10), t("c", 25)], function (err, res) {\n'
                '  console.log(err, JSON.stringify(res), Date.now() - t0 < 90);\n'
                '  parallel([t("x", 30), t("y", 5, true), t("z", 10, true)], function (err2, res2) {\n'
                '    console.log(err2.message, res2);\n'
                '    parallel([], function (e3, r3) { console.log(e3, JSON.stringify(r3)); });\n'
                '  });\n'
                '});\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Счётчик оставшихся задач и замыкание с индексом; флаг finished защищает от повторного done.',
      'expected': ['стиль ES3: ок', 'null ["a","b","c"] true', 'y undefined', 'null []']},
     {'id': 'j1-detect-browser',
      'mode': 'js',
      'title': 'Определение браузера по User-Agent',
      'statement': 'Напишите функцию detectBrowser(ua): возвращает «ie» (есть «MSIE» или «Trident/»), «edge» '
                   '(«Edg/» или «Edge/»), «opera» («OPR/» или «Opera»), «chrome» («Chrome/» — в строке '
                   'Chrome есть и «Safari/»), «firefox» («Firefox/»), «safari» («Safari/» без «Chrome/») или '
                   '«unknown». Порядок проверок важен. Пишите в стиле ES3: только var и function — без '
                   'стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function detectBrowser(ua) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var uas = [\n'
                '  "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1)",\n'
                '  "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",\n'
                '  "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 Chrome/120.0 Safari/537.36 Edg/120.0",\n'
                '  "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 Chrome/120.0 Safari/537.36 OPR/105.0",\n'
                '  "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",\n'
                '  "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",\n'
                '  "Mozilla/5.0 (Macintosh) AppleWebKit/605.1.15 Version/17.0 Safari/605.1.15",\n'
                '  "curl/8.0",\n'
                '];\n'
                'uas.forEach(function (u) { console.log(detectBrowser(u)); });\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Chrome, Edge и Opera содержат «Chrome/» и «Safari/» — проверяйте их раньше обычных.',
      'expected': ['ie', 'ie', 'edge', 'opera', 'chrome', 'firefox', 'safari', 'unknown', 'стиль ES3: ок']},
     {'id': 'j1-script-order',
      'mode': 'js',
      'title': 'Порядок подключения скриптов',
      'statement': 'Скрипты зависят друг от друга: [{ name: "app.js", needs: ["plugin.js", "jquery.js"] }, '
                   '…]. Напишите функцию scriptOrder(scripts): возвращает массив имён в таком порядке, чтобы '
                   'каждый скрипт шёл после своих зависимостей (при выборе из готовых — в порядке исходного '
                   'списка); при цикле зависимостей бросает Error("цикл"), при зависимости от неизвестного '
                   'скрипта — Error("нет скрипта: <имя>"). Пишите в стиле ES3: только var и function — без '
                   'стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function scriptOrder(scripts) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(scriptOrder([{ name: "app.js", needs: ["plugin.js", "jquery.js"] }, { name: '
                '"plugin.js", needs: ["jquery.js"] }, { name: "jquery.js" }]).join());\n'
                'console.log(scriptOrder([{ name: "a" }, { name: "b" }]).join());\n'
                'console.log(scriptOrder([{ name: "b", needs: ["a"] }, { name: "a" }, { name: "c", needs: '
                '["b"] }]).join());\n'
                'try { scriptOrder([{ name: "a", needs: ["b"] }, { name: "b", needs: ["a"] }]); } catch (e) '
                '{ console.log(e.message); }\n'
                'try { scriptOrder([{ name: "a", needs: ["zzz"] }]); } catch (e) { console.log(e.message); '
                '}\n'
                'console.log(scriptOrder([]).length);\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Обход в глубину с тремя состояниями узла: не посещён, в обработке, готов.',
      'expected': ['jquery.js,plugin.js,app.js',
                   'a,b',
                   'a,b,c',
                   'цикл',
                   'нет скрипта: zzz',
                   '0',
                   'стиль ES3: ок']},
     {'id': 'j1-namespace',
      'mode': 'js',
      'title': 'Пространства имён (YUI-стиль)',
      'statement': 'Напишите функцию namespace(root, path): path — строка вида «app.ui.menu»; создаёт в '
                   'объекте root вложенные пустые объекты по частям пути (существующие не затирает) и '
                   'возвращает самый глубокий. Пишите в стиле ES3: только var и function — без стрелок, '
                   'let/const, классов, шаблонных строк и spread.',
      'starter': 'function namespace(root, path) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var app = {};\n'
                'var menu = namespace(app, "ui.menu");\n'
                'menu.open = true;\n'
                'console.log(JSON.stringify(app));\n'
                'var same = namespace(app, "ui.menu");\n'
                'console.log(same === menu);\n'
                'app.ui.keep = 1;\n'
                'namespace(app, "ui.panel");\n'
                'console.log(JSON.stringify(app));\n'
                'console.log(namespace(app, "x") === app.x);\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Идите по частям пути, создавая объект там, где поля ещё нет.',
      'expected': ['{"ui":{"menu":{"open":true}}}',
                   'true',
                   '{"ui":{"menu":{"open":true},"keep":1,"panel":{}}}',
                   'true',
                   'стиль ES3: ок']},
     {'id': 'j1-inherit',
      'mode': 'js',
      'title': 'Наследование через прототип (ES3)',
      'statement': 'Напишите функцию inherit(Child, Parent): настраивает цепочку прототипов так, чтобы '
                   'экземпляры Child наследовали методы Parent.prototype, не вызывая Parent и сохранив '
                   'Child.prototype.constructor === Child. Если у Child.prototype уже есть методы, их '
                   'затирать не нужно — вызывается до объявления методов. Пишите в стиле ES3: только var и '
                   'function — без стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function inherit(Child, Parent) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var calls = 0;\n'
                'function Animal(name) { calls++; this.name = name; }\n'
                'Animal.prototype.speak = function () { return this.name + " издаёт звук"; };\n'
                'function Dog(name) { Animal.call(this, name); }\n'
                'inherit(Dog, Animal);\n'
                'Dog.prototype.speak = function () { return Animal.prototype.speak.call(this) + ": гав"; };\n'
                'var d = new Dog("Бобик");\n'
                'console.log(d.speak());\n'
                'console.log(d instanceof Dog, d instanceof Animal, d.constructor === Dog);\n'
                'console.log(calls);\n'
                'console.log(Object.getPrototypeOf(Dog.prototype) !== Animal.prototype ? "через F" : '
                '"напрямую");\n'
                'console.log(Animal.prototype.hasOwnProperty("bark"));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Временный конструктор F с F.prototype = Parent.prototype; Child.prototype = new F().',
      'expected': ['Бобик издаёт звук: гав', 'true true true', '1', 'напрямую', 'false', 'стиль ES3: ок']},
     {'id': 'j1-extend',
      'mode': 'js',
      'title': 'extend в духе jQuery',
      'statement': 'Напишите функцию extend(target, …sources) и вариант с глубоким слиянием: если первым '
                   'аргументом передано true — extend(true, target, a, b) рекурсивно сливает вложенные '
                   'обычные объекты (массивы и прочее заменяются целиком). Возвращает target. Значения '
                   'undefined пропускаются. Пишите в стиле ES3: только var и function — без стрелок, '
                   'let/const, классов, шаблонных строк и spread.',
      'starter': 'function extend() {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var a = { x: 1, nested: { p: 1, q: 2 }, list: [1] };\n'
                'var b = { y: 2, nested: { q: 9, r: 3 }, list: [2, 3], skip: undefined };\n'
                'console.log(JSON.stringify(extend({}, a, b)));\n'
                'console.log(JSON.stringify(extend(true, {}, a, b)));\n'
                'var t = { n: { keep: 1 } };\n'
                'extend(true, t, { n: { add: 2 } });\n'
                'console.log(JSON.stringify(t));\n'
                'var shallow = extend({ n: { keep: 1 } }, { n: { add: 2 } });\n'
                'console.log(JSON.stringify(shallow));\n'
                'console.log(extend(a) === a);\n'
                'var copy = extend(true, {}, a);\n'
                'copy.nested.p = 99;\n'
                'console.log(a.nested.p);\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'arguments[0] может быть булевым флагом; для вложенных объектов в deep-режиме вызывайте extend '
              'рекурсивно.',
      'expected': ['{"x":1,"nested":{"q":9,"r":3},"list":[2,3],"y":2}',
                   '{"x":1,"nested":{"p":1,"q":9,"r":3},"list":[2,3],"y":2}',
                   '{"n":{"keep":1,"add":2}}',
                   '{"n":{"add":2}}',
                   'true',
                   '1',
                   'стиль ES3: ок']},
     {'id': 'j1-pubsub',
      'mode': 'js',
      'title': 'PubSub в духе jQuery-плагинов',
      'statement': 'Напишите функцию createPubSub(): возвращает объект с методами subscribe(topic, fn) → '
                   'токен (число, растёт с 1), publish(topic, data) → число вызванных подписчиков '
                   '(подписчики вызываются в порядке подписки, fn(data, topic)) и unsubscribe(token) → '
                   'true/false (был ли такой токен). Пишите в стиле ES3: только var и function — без '
                   'стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function createPubSub() {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var bus = createPubSub();\n'
                'var log = [];\n'
                'var t1 = bus.subscribe("msg", function (d, t) { log.push("a:" + d + ":" + t); });\n'
                'var t2 = bus.subscribe("msg", function (d) { log.push("b:" + d); });\n'
                'var t3 = bus.subscribe("other", function (d) { log.push("c:" + d); });\n'
                'console.log(t1, t2, t3);\n'
                'console.log(bus.publish("msg", 1));\n'
                'console.log(bus.unsubscribe(t1), bus.unsubscribe(t1), bus.unsubscribe(99));\n'
                'console.log(bus.publish("msg", 2), bus.publish("other", 3), bus.publish("none", 4));\n'
                'console.log(log.join(" "));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Токен — уникальный id; unsubscribe ищет его по всем темам.',
      'expected': ['1 2 3', '2', 'true false false', '1 1 0', 'a:1:msg b:1 b:2 c:3', 'стиль ES3: ок']},
     {'id': 'j1-ecma-info',
      'mode': 'js',
      'title': 'Редакции ECMAScript',
      'statement': 'Напишите функцию ecmaInfo(name): принимает «ES3», «ES5», «ES6», «ES2015», «ES2020», … и '
                   'возвращает объект { edition, year }. Правила: ES1 — 1997, ES2 — 1998, ES3 — 1999, ES5 — '
                   '2009 (ES4 отменили — для него бросьте Error("ES4 не вышел")); начиная с ES6 редакция n '
                   'выходит в 2009 + n году (ES6 = ES2015, ES7 = ES2016, …); «ES<год>» (год ≥ 2015) даёт '
                   'edition = год - 2009. Некорректные имена — Error("неизвестная редакция"). Пишите в стиле '
                   'ES3: только var и function — без стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function ecmaInfo(name) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                '["ES1", "ES3", "ES5", "ES6", "ES2015", "ES2020", "ES11", "ES2024"].forEach(function (n) { '
                'console.log(n, JSON.stringify(ecmaInfo(n))); });\n'
                '["ES4", "ES0", "ES", "ECMA", "ES2010", "es6", "ES99"].forEach(function (n) {\n'
                '  try { ecmaInfo(n); console.log(n, "ok?"); } catch (e) { console.log(n, e.message); }\n'
                '});\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Регулярное выражение /^ES(\\d+)$/ и таблица ранних редакций {1: 1997, 2: 1998, 3: 1999, 5: '
              '2009}.',
      'expected': ['ES1 {"edition":1,"year":1997}',
                   'ES3 {"edition":3,"year":1999}',
                   'ES5 {"edition":5,"year":2009}',
                   'ES6 {"edition":6,"year":2015}',
                   'ES2015 {"edition":6,"year":2015}',
                   'ES2020 {"edition":11,"year":2020}',
                   'ES11 {"edition":11,"year":2020}',
                   'ES2024 {"edition":15,"year":2024}',
                   'ES4 ES4 не вышел',
                   'ES0 неизвестная редакция',
                   'ES неизвестная редакция',
                   'ECMA неизвестная редакция',
                   'ES2010 неизвестная редакция',
                   'es6 неизвестная редакция',
                   'ES99 неизвестная редакция',
                   'стиль ES3: ок']},
     {'id': 'j1-xml-json',
      'mode': 'js',
      'title': 'XML против JSON',
      'statement': 'Напишите функцию toXml(name, obj): плоский объект превращается в XML: toXml("user", {id: '
                   '1, name: "Ада"}) → «<user><id>1</id><name>Ада</name></user>». Символы &, <, > в '
                   'значениях экранируйте как &amp; &lt; &gt;. И функцию compareSize(obj) → { json, xml } — '
                   'длины двух записей (JSON.stringify и toXml("o", obj)). Пишите в стиле ES3: только var и '
                   'function — без стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function toXml(name, obj) {\n}\nfunction compareSize(obj) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(toXml("user", { id: 1, name: "Ада" }));\n'
                'console.log(toXml("m", { text: "a < b && c > d" }));\n'
                'console.log(toXml("e", {}));\n'
                'console.log(JSON.stringify(compareSize({ id: 1, name: "Ада" })));\n'
                'var c = compareSize({ a: 1, b: 2, c: 3 });\n'
                'console.log(c.json < c.xml);\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Порядок замен: сначала & (иначе экранируете собственные амперсанды), затем < и >.',
      'expected': ['<user><id>1</id><name>Ада</name></user>',
                   '<m><text>a &lt; b &amp;&amp; c &gt; d</text></m>',
                   '<e></e>',
                   '{"json":21,"xml":33}',
                   'true',
                   'стиль ES3: ок']},
     {'id': 'j1-debounce',
      'mode': 'js',
      'title': 'debounce для события resize',
      'statement': 'Напишите функцию debounce(fn, ms): возвращает функцию, которая откладывает вызов fn на '
                   'ms миллисекунд после последнего обращения (каждое новое обращение сбрасывает таймер); fn '
                   'вызывается с аргументами и this последнего обращения. Пишите в стиле ES3: только var и '
                   'function — без стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function debounce(fn, ms) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var calls = [];\n'
                'var obj = { name: "o", handler: debounce(function (x) { calls.push(this.name + ":" + x); }, '
                '60) };\n'
                'var t0 = Date.now();\n'
                'obj.handler(1);\n'
                'setTimeout(function () { obj.handler(2); }, 20);\n'
                'setTimeout(function () { obj.handler(3); }, 40);\n'
                'setTimeout(function () { console.log("в процессе:", calls.length); }, 80);\n'
                'setTimeout(function () { console.log(calls.join()); }, 200);\n'
                'setTimeout(function () { obj.handler(4); }, 220);\n'
                'setTimeout(function () { console.log(calls.length); }, 400);\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'clearTimeout(timer) перед новым setTimeout; this и arguments сохраните в локальные '
              'переменные.',
      'expected': ['стиль ES3: ок', 'в процессе: 0', 'o:3', '2']},
     {'id': 'j1-type-of',
      'mode': 'js',
      'title': 'typeOf по Крокфорду',
      'statement': 'Напишите функцию typeOf(v): возвращает «null», «array», «date», «regexp», «function», '
                   '«error», «object» (для остальных объектов) или результат typeof для примитивов; '
                   'используйте Object.prototype.toString. Пишите в стиле ES3: только var и function — без '
                   'стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function typeOf(v) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var vals = [null, undefined, 1, "s", true, [], {}, new Date(0), /x/, function () {}, new '
                'Error("e"), new Number(1), Object.create(null)];\n'
                'console.log(vals.map(typeOf).join());\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Object.prototype.toString.call(v).slice(8, -1)',
      'expected': ['null,undefined,number,string,boolean,array,object,date,regexp,function,error,object,object',
                   'стиль ES3: ок']},
     {'id': 'j1-memoize-es3',
      'mode': 'js',
      'title': 'Мемоизация в стиле ES3',
      'statement': 'Напишите функцию memoizeES3(fn): возвращает функцию, которая кэширует результат по ключу '
                   '— аргументы, склеенные JSON.stringify(Array.prototype.slice.call(arguments)). Повторный '
                   'вызов с теми же аргументами не вызывает fn. Пишите в стиле ES3: только var и function — '
                   'без стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function memoizeES3(fn) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'var calls = 0;\n'
                'var add = memoizeES3(function (a, b) { calls++; return a + b; });\n'
                'console.log(add(1, 2), add(1, 2), add(2, 1), add(1, 2));\n'
                'console.log(calls);\n'
                'var cnt = 0;\n'
                'var u = memoizeES3(function () { cnt++; });\n'
                'u(); u(); u(undefined);\n'
                'console.log(cnt);\n'
                'console.log(add("1", 2), calls);\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'hasOwnProperty надёжнее, чем проверка значения: результат может быть 0 или undefined.',
      'expected': ['3 3 3 3', '2', '2', '12 3', 'стиль ES3: ок']},
     {'id': 'j1-compose-es3',
      'mode': 'js',
      'title': 'compose и pipe в стиле ES3',
      'statement': 'Напишите функцию composeES3(f, g, h, …): возвращает функцию, применяющую переданные '
                   'функции справа налево (как математическая композиция); без аргументов — тождественная '
                   'функция. Пишите в стиле ES3: только var и function — без стрелок, let/const, классов, '
                   'шаблонных строк и spread.',
      'starter': 'function composeES3() {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'function inc(x) { return x + 1; }\n'
                'function dbl(x) { return x * 2; }\n'
                'function neg(x) { return -x; }\n'
                'console.log(composeES3(inc, dbl)(5));\n'
                'console.log(composeES3(dbl, inc)(5));\n'
                'console.log(composeES3(neg, inc, dbl)(3));\n'
                'console.log(composeES3()(42));\n'
                'console.log(composeES3(dbl)(4));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Перебирайте сохранённый массив функций с конца.',
      'expected': ['11', '12', '-7', '42', '8', 'стиль ES3: ок']},
     {'id': 'j1-curry-es3',
      'mode': 'js',
      'title': 'Карринг в стиле ES3',
      'statement': 'Напишите функцию curryN(fn, n): возвращает функцию, которую можно вызывать частями '
                   '(curryN(f, 3)(1)(2)(3), curryN(f, 3)(1, 2)(3) и т.п.); когда накоплено n аргументов, '
                   'вызывает fn с ними и возвращает результат. Пишите в стиле ES3: только var и function — '
                   'без стрелок, let/const, классов, шаблонных строк и spread.',
      'starter': 'function curryN(fn, n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'function vol(a, b, c) { return a * b * c; }\n'
                'var c = curryN(vol, 3);\n'
                'console.log(c(2)(3)(4), c(2, 3)(4), c(2)(3, 4), c(2, 3, 4));\n'
                'var part = c(10);\n'
                'console.log(part(1, 1), part(2)(2));\n'
                'console.log(typeof c(1), typeof c(1)(2));\n'
                'console.log(curryN(function () { return "zero"; }, 0)());\n'
                'console.log(curryN(function (a, b) { return a + b; }, 2)("x")("y"));\n'
                'var __bad = ["=>", "(^|[^\\\\w$.])const\\\\s", "(^|[^\\\\w$.])let\\\\s", '
                '"(^|[^\\\\w$.])class\\\\s", "`", "\\\\.\\\\.\\\\."].reduce(function (n, r) { return n + '
                '(__src.match(new RegExp(r, "g")) || []).length; }, 0);\n'
                'console.log(__bad === 0 ? "стиль ES3: ок" : "использованы возможности ES6+");\n',
      'hint': 'Накапливайте аргументы в массиве, пока их не станет n.',
      'expected': ['24 24 24 24', '10 40', 'function function', 'zero', 'xy', 'стиль ES3: ок']}]}
