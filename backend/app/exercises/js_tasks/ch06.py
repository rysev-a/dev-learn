"""Задачи книги «Современный Frontend», глава 6 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {6: [{'id': 'j6-compose',
      'mode': 'js',
      'title': 'Композиция двух функций',
      'statement': 'Напишите функцию compose(f, g): она возвращает новую функцию x => f(g(x)).',
      'starter': 'function compose(f, g) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const inc = (x) => x + 1;\n'
                'const dbl = (x) => x * 2;\n'
                'console.log(compose(inc, dbl)(5));\n'
                'console.log(compose(dbl, inc)(5));\n'
                'console.log(compose(String, inc)(1) === "2");\n'
                'console.log(typeof compose(inc, dbl));\n',
      'hint': 'return (x) => f(g(x));',
      'expected': ['11', '12', 'true', 'function']},
     {'id': 'j6-pipe',
      'mode': 'js',
      'title': 'pipe: конвейер функций',
      'statement': 'Напишите функцию pipe(...fns): она возвращает функцию, которая передаёт аргумент первой '
                   'функции, результат — второй и так далее; без функций возвращает аргумент как есть.',
      'starter': 'function pipe(...fns) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const inc = (x) => x + 1;\n'
                'const dbl = (x) => x * 2;\n'
                'console.log(pipe(inc, dbl, inc)(3));\n'
                'console.log(pipe()(7));\n'
                'console.log(pipe(dbl)(4));\n'
                'console.log(pipe((s) => s.trim(), (s) => s.toUpperCase())("  привет "));\n',
      'hint': 'fns.reduce((acc, f) => f(acc), x)',
      'expected': ['9', '7', '8', 'ПРИВЕТ']},
     {'id': 'j6-counter',
      'mode': 'js',
      'title': 'Счётчик в замыкании',
      'statement': 'Напишите функцию makeCounter(start = 0): она возвращает функцию, при каждом вызове '
                   'увеличивающую внутренний счётчик на 1 и возвращающую новое значение. Счётчики из разных '
                   'вызовов makeCounter независимы.',
      'starter': 'function makeCounter(start = 0) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const a = makeCounter();\n'
                'const b = makeCounter(10);\n'
                'console.log(a(), a(), a());\n'
                'console.log(b(), b());\n'
                'console.log(a());\n',
      'hint': 'let n = start; return () => ++n;',
      'expected': ['1 2 3', '11 12', '4']},
     {'id': 'j6-once',
      'mode': 'js',
      'title': 'once: вызвать только один раз',
      'statement': 'Напишите функцию once(fn): она возвращает функцию, которая при первом вызове вызывает fn '
                   'с переданными аргументами и запоминает результат, а при следующих — возвращает '
                   'запомненный результат, не вызывая fn.',
      'starter': 'function once(fn) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'let calls = 0;\n'
                'const f = once((x) => { calls++; return x * 2; });\n'
                'console.log(f(5), f(100), f(7));\n'
                'console.log(calls);\n'
                'const g = once(() => undefined);\n'
                'console.log(g(), g());\n',
      'hint': 'Запомните флаг и результат в замыкании.',
      'expected': ['10 10 10', '1', 'undefined undefined']},
     {'id': 'j6-memoize',
      'mode': 'js',
      'title': 'Мемоизация',
      'statement': 'Напишите функцию memoize(fn): она возвращает функцию, которая для одинаковых одиночных '
                   'аргументов вызывает fn только один раз (результаты хранятся в Map), включая случай, '
                   'когда результат равен undefined.',
      'starter': 'function memoize(fn) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'let calls = 0;\n'
                'const sq = memoize((x) => { calls++; return x * x; });\n'
                'console.log(sq(4), sq(4), sq(5), sq(4));\n'
                'console.log(calls);\n'
                'let n = 0;\n'
                'const u = memoize(() => { n++; });\n'
                'u(1); u(1); u(2);\n'
                'console.log(n);\n',
      'hint': 'cache.has(x), а не проверка значения: результат может быть undefined или 0.',
      'expected': ['16 16 25 16', '2', '2']},
     {'id': 'j6-curry',
      'mode': 'js',
      'title': 'Карринг для двух аргументов',
      'statement': 'Напишите функцию curry2(f): она превращает функцию двух аргументов в цепочку '
                   'curry2(f)(a)(b), результат которой равен f(a, b).',
      'starter': 'function curry2(f) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const add = (a, b) => a + b;\n'
                'console.log(curry2(add)(2)(3));\n'
                'const add10 = curry2(add)(10);\n'
                'console.log(add10(1), add10(5));\n'
                'console.log(curry2((a, b) => a + "-" + b)("x")("y"));\n',
      'hint': 'return (a) => (b) => f(a, b);',
      'expected': ['5', '11 15', 'x-y']},
     {'id': 'j6-partial',
      'mode': 'js',
      'title': 'Частичное применение',
      'statement': 'Напишите функцию partial(fn, ...bound): она возвращает функцию, которая вызывает fn, '
                   'сначала подставляя bound, а затем свои аргументы.',
      'starter': 'function partial(fn, ...bound) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const vol = (a, b, c) => a * b * c;\n'
                'console.log(partial(vol, 2)(3, 4));\n'
                'console.log(partial(vol, 2, 3)(4));\n'
                'console.log(partial(vol)(1, 2, 3));\n'
                'const greet = (g, name) => `${g}, ${name}!`;\n'
                'console.log(partial(greet, "Привет")("Ада"));\n',
      'hint': 'return (...rest) => fn(...bound, ...rest);',
      'expected': ['24', '24', '6', 'Привет, Ада!']},
     {'id': 'j6-sum-rest',
      'mode': 'js',
      'title': 'Сумма через rest',
      'statement': 'Напишите функцию sum(...nums): сумма всех аргументов (для пустого вызова — 0). Объект '
                   'arguments использовать нельзя.',
      'starter': 'function sum(...nums) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(sum(1, 2, 3));\n'
                'console.log(sum());\n'
                'console.log(sum(5));\n'
                'console.log(sum(...[1, 2, 3, 4]));\n'
                'console.log(__count("argu" + "ments"));\n',
      'hint': 'Остаточный параметр ...nums — настоящий массив.',
      'expected': ['6', '0', '5', '10', '0']},
     {'id': 'j6-defaults',
      'mode': 'js',
      'title': 'Параметры по умолчанию',
      'statement': 'Напишите функцию greet(name = "гость", greeting = "Привет"): она возвращает «<greeting>, '
                   '<name>!». Для null параметры умолчаний не получают.',
      'starter': 'function greet(name, greeting) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(greet());\n'
                'console.log(greet("Ада"));\n'
                'console.log(greet("Ада", "Здравствуйте"));\n'
                'console.log(greet(undefined, "Эй"));\n'
                'console.log(greet(null));\n',
      'hint': 'function greet(name = "гость", greeting = "Привет")',
      'expected': ['Привет, гость!', 'Привет, Ада!', 'Здравствуйте, Ада!', 'Эй, гость!', 'Привет, null!']},
     {'id': 'j6-box-options',
      'mode': 'js',
      'title': 'Объект настроек',
      'statement': 'Напишите функцию describeBox({ w, h = 10, color = "red" }): она возвращает строку '
                   '«<w>x<h> <color>». Параметры разберите прямо в заголовке.',
      'starter': 'function describeBox(opts) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(describeBox({ w: 5 }));\n'
                'console.log(describeBox({ w: 5, h: 2 }));\n'
                'console.log(describeBox({ color: "blue", w: 1, h: 1 }));\n'
                'console.log(describeBox({ w: 3, h: undefined, color: undefined }));\n',
      'hint': 'function describeBox({ w, h = 10, color = "red" })',
      'expected': ['5x10 red', '5x2 red', '1x1 blue', '3x10 red']},
     {'id': 'j6-max-of',
      'mode': 'js',
      'title': 'Максимум массива через spread',
      'statement': 'Напишите функцию maxOf(arr): наибольшее число массива, а для пустого массива — '
                   '-Infinity. Используйте Math.max и оператор ... в вызове; цикл не нужен.',
      'starter': 'function maxOf(arr) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(maxOf([3, 9, 4]));\n'
                'console.log(maxOf([]));\n'
                'console.log(maxOf([-5, -1, -9]));\n'
                'console.log(maxOf([7]));\n'
                'console.log(__count("for" + " (") + __count("for" + "("));\n',
      'hint': 'Math.max(...arr)',
      'expected': ['9', '-Infinity', '-1', '7', '0']},
     {'id': 'j6-fix-loop',
      'mode': 'js',
      'title': 'Исправьте: замыкания в цикле',
      'statement': 'Функция makeFns(n) должна вернуть массив из n функций, i-я из которых возвращает число i '
                   '(0, 1, …). Сейчас все функции возвращают одно и то же число. Исправьте.',
      'starter': 'function makeFns(n) {\n'
                 '  const fns = [];\n'
                 '  for (var i = 0; i < n; i++) {\n'
                 '    fns.push(() => i);\n'
                 '  }\n'
                 '  return fns;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(makeFns(4).map((f) => f())));\n'
                'console.log(JSON.stringify(makeFns(0).map((f) => f())));\n'
                'console.log(makeFns(3)[1]());\n',
      'hint': 'Замените var на let: на каждой итерации появится своя переменная.',
      'expected': ['[0,1,2,3]', '[]', '1']},
     {'id': 'j6-account',
      'mode': 'js',
      'title': 'Банковский счёт: приватное состояние',
      'statement': 'Напишите функцию createAccount(balance): она возвращает объект с методами deposit(x) '
                   '(добавляет), withdraw(x) (списывает; если денег не хватает — бросает RangeError и баланс '
                   'не меняется) и getBalance(). Сам баланс не должен быть полем объекта.',
      'starter': 'function createAccount(balance) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const acc = createAccount(100);\n'
                'acc.deposit(50);\n'
                'acc.withdraw(30);\n'
                'console.log(acc.getBalance());\n'
                'try { acc.withdraw(500); } catch (e) { console.log(e.name, acc.getBalance()); }\n'
                'console.log(JSON.stringify(Object.keys(acc).sort()));\n'
                'console.log(acc.balance);\n'
                'const other = createAccount(1);\n'
                'console.log(other.getBalance(), acc.getBalance());\n',
      'hint': 'Баланс — параметр функции, он живёт в замыкании методов.',
      'expected': ['120', 'RangeError 120', '["deposit","getBalance","withdraw"]', 'undefined', '1 120']},
     {'id': 'j6-id-gen',
      'mode': 'js',
      'title': 'Генератор идентификаторов',
      'statement': 'Напишите функцию makeIdGen(prefix): она возвращает функцию, которая при каждом вызове '
                   'выдаёт «<prefix>1», «<prefix>2», … Разные генераторы независимы.',
      'starter': 'function makeIdGen(prefix) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const u = makeIdGen("u");\n'
                'const t = makeIdGen("task-");\n'
                'console.log(u(), u(), t(), u(), t());\n',
      'hint': 'let n = 0; return () => `${prefix}${++n}`;',
      'expected': ['u1 u2 task-1 u3 task-2']},
     {'id': 'j6-my-map',
      'mode': 'js',
      'title': 'Своя map',
      'statement': 'Напишите функцию myMap(arr, fn): она возвращает новый массив из результатов fn(элемент, '
                   'индекс) для каждого элемента. Метод Array.prototype.map использовать нельзя.',
      'starter': 'function myMap(arr, fn) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(JSON.stringify(myMap([1, 2, 3], (x) => x * 2)));\n'
                'console.log(JSON.stringify(myMap(["a", "b"], (x, i) => x + i)));\n'
                'console.log(JSON.stringify(myMap([], (x) => x)));\n'
                'const src = [1];\n'
                'console.log(myMap(src, (x) => x) !== src);\n'
                'console.log(__count(".m" + "ap("));\n',
      'hint': 'Цикл по индексам и push результата fn(arr[i], i).',
      'expected': ['[2,4,6]', '["a0","b1"]', '[]', 'true', '0']},
     {'id': 'j6-my-filter',
      'mode': 'js',
      'title': 'Своя filter',
      'statement': 'Напишите функцию myFilter(arr, pred): возвращает новый массив из элементов, для которых '
                   'pred(элемент, индекс) истинно. Метод filter использовать нельзя.',
      'starter': 'function myFilter(arr, pred) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(JSON.stringify(myFilter([1, 2, 3, 4], (x) => x % 2 === 0)));\n'
                'console.log(JSON.stringify(myFilter(["a", "b", "c"], (x, i) => i !== 1)));\n'
                'console.log(JSON.stringify(myFilter([], () => true)));\n'
                'console.log(JSON.stringify(myFilter([0, "", null, 5], Boolean)));\n'
                'console.log(__count(".fil" + "ter("));\n',
      'hint': 'if (pred(arr[i], i)) out.push(arr[i]);',
      'expected': ['[2,4]', '["a","c"]', '[]', '[5]', '0']},
     {'id': 'j6-my-reduce',
      'mode': 'js',
      'title': 'Своя reduce',
      'statement': 'Напишите функцию myReduce(arr, fn, init): сворачивает массив слева направо: acc = init; '
                   'для каждого элемента acc = fn(acc, x, i). Если init не передан (аргументов меньше трёх), '
                   'начальным значением служит первый элемент, а обход идёт со второго; для пустого массива '
                   'без init бросьте TypeError.',
      'starter': 'function myReduce(arr, fn, init) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(myReduce([1, 2, 3, 4], (a, x) => a + x, 0));\n'
                'console.log(myReduce([1, 2, 3, 4], (a, x) => a + x));\n'
                'console.log(myReduce(["a", "b"], (a, x, i) => a + x + i, ""));\n'
                'console.log(myReduce([], (a, x) => a + x, 99));\n'
                'try { myReduce([], (a, x) => a + x); } catch (e) { console.log(e.name); }\n'
                'console.log(myReduce([5], (a, x) => a * x));\n'
                'console.log(myReduce([1, 2], (a, x) => a + x, undefined));\n',
      'hint': 'Чтобы отличить «init не передан» от «init равен undefined», посмотрите на arguments.length '
              'или на длину rest-массива.',
      'expected': ['10', '10', 'a0b1', '99', 'TypeError', '5', 'NaN']},
     {'id': 'j6-group-by',
      'mode': 'js',
      'title': 'Группировка',
      'statement': 'Напишите функцию groupBy(arr, keyFn): объект, где ключ — результат keyFn(элемент), а '
                   'значение — массив элементов с этим ключом в исходном порядке.',
      'starter': 'function groupBy(arr, keyFn) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(groupBy([1, 2, 3, 4, 5], (x) => (x % 2 ? "odd" : "even"))));\n'
                'console.log(JSON.stringify(groupBy(["apple", "avocado", "banana"], (s) => s[0])));\n'
                'console.log(JSON.stringify(groupBy([], (x) => x)));\n'
                'console.log(JSON.stringify(groupBy([{ t: "a", v: 1 }, { t: "a", v: 2 }], (o) => o.t)));\n',
      'hint': '(out[k] ??= []).push(x)',
      'expected': ['{"odd":[1,3,5],"even":[2,4]}',
                   '{"a":["apple","avocado"],"b":["banana"]}',
                   '{}',
                   '{"a":[{"t":"a","v":1},{"t":"a","v":2}]}']},
     {'id': 'j6-pluck',
      'mode': 'js',
      'title': 'pluck: поле из каждого объекта',
      'statement': 'Напишите функцию pluck(arr, key): возвращает массив значений поля key у каждого объекта '
                   '(для отсутствующего поля — undefined, которое JSON выведет как null).',
      'starter': 'function pluck(arr, key) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const users = [{ id: 1, n: "a" }, { id: 2, n: "b" }, { id: 3 }];\n'
                'console.log(JSON.stringify(pluck(users, "id")));\n'
                'console.log(JSON.stringify(pluck(users, "n")));\n'
                'console.log(JSON.stringify(pluck([], "x")));\n',
      'hint': 'arr.map((o) => o[key])',
      'expected': ['[1,2,3]', '["a","b",null]', '[]']},
     {'id': 'j6-apply-n',
      'mode': 'js',
      'title': 'Применить функцию n раз',
      'statement': 'Напишите функцию applyN(fn, n, x): применяет fn к x ровно n раз подряд (n ≥ 0) и '
                   'возвращает результат; при n = 0 возвращает x.',
      'starter': 'function applyN(fn, n, x) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(applyN((v) => v * 2, 5, 1));\n'
                'console.log(applyN((v) => v + "!", 3, "hi"));\n'
                'console.log(applyN((v) => v + 1, 0, 42));\n'
                'console.log(applyN((a) => [...a, a.length], 3, []).join());\n',
      'hint': 'Цикл от 0 до n: x = fn(x).',
      'expected': ['32', 'hi!!!', '42', '0,1,2']},
     {'id': 'j6-flip',
      'mode': 'js',
      'title': 'flip: поменять аргументы местами',
      'statement': 'Напишите функцию flip(fn): возвращает функцию, которая вызывает fn с теми же '
                   'аргументами, но в обратном порядке.',
      'starter': 'function flip(fn) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const sub = (a, b) => a - b;\n'
                'console.log(flip(sub)(10, 3));\n'
                'const join3 = (a, b, c) => [a, b, c].join("");\n'
                'console.log(flip(join3)("x", "y", "z"));\n'
                'const f = flip((...a) => a.length);\n'
                'console.log(f(), f(1, 2));\n',
      'hint': 'return (...args) => fn(...args.reverse());',
      'expected': ['-7', 'zyx', '0 2']},
     {'id': 'j6-fix-this',
      'mode': 'js',
      'title': 'Исправьте: потерянный this',
      'statement': 'Функция makeGreeter(user) должна вернуть функцию без аргументов, которая вызывает '
                   'user.greet() и возвращает его результат, даже если вызвана отдельно от объекта. Сейчас '
                   'она возвращает «голый» метод и теряет this. Исправьте.',
      'starter': 'function makeGreeter(user) {\n  return user.greet;\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const user = { name: "Ада", greet() { return "Привет, " + this.name; } };\n'
                'const g = makeGreeter(user);\n'
                'console.log(g());\n'
                'user.name = "Линус";\n'
                'console.log(g());\n'
                'const other = { name: "Б", greet: user.greet };\n'
                'console.log(makeGreeter(other)());\n',
      'hint': 'user.greet.bind(user) или () => user.greet()',
      'expected': ['Привет, Ада', 'Привет, Линус', 'Привет, Б']},
     {'id': 'j6-call-with',
      'mode': 'js',
      'title': 'Вызов с заданным this',
      'statement': 'Напишите функцию callWith(fn, thisArg, args): вызывает fn с this, равным thisArg, и '
                   'аргументами из массива args; возвращает результат. Используйте call или apply.',
      'starter': 'function callWith(fn, thisArg, args) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'function intro(city, year) { return this.name + " из " + city + ", " + year; }\n'
                'console.log(callWith(intro, { name: "Ада" }, ["Лондон", 1815]));\n'
                'console.log(callWith(function () { return this.v; }, { v: 7 }, []));\n'
                'console.log(callWith(Math.max, null, [1, 5, 2]));\n',
      'hint': 'fn.apply(thisArg, args)',
      'expected': ['Ада из Лондон, 1815', '7', '5']},
     {'id': 'j6-fix-arrow-method',
      'mode': 'js',
      'title': 'Исправьте: стрелка в роли метода',
      'statement': 'Функция createCounter() возвращает объект с полем count и методом inc(), увеличивающим '
                   'count на 1. Метод написан стрелкой, поэтому this в нём не объект и вызов падает. '
                   'Исправьте.',
      'starter': 'function createCounter() {\n'
                 '  return {\n'
                 '    count: 0,\n'
                 '    inc: () => {\n'
                 '      this.count++;\n'
                 '    },\n'
                 '  };\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'const c = createCounter();\n'
                'c.inc();\n'
                'c.inc();\n'
                'console.log(c.count);\n'
                'const d = createCounter();\n'
                'd.inc();\n'
                'console.log(d.count, c.count);\n',
      'hint': 'Метод объекта пишут обычной функцией: inc() { … }',
      'expected': ['2', '1 2']},
     {'id': 'j6-fib-memo',
      'mode': 'js',
      'title': 'Фибоначчи с мемоизацией',
      'statement': 'Напишите функцию fib(n): n-е число Фибоначчи (fib(0) = 0, fib(1) = 1) для n до 70. '
                   'Наивная двойная рекурсия не уложится в лимит времени — храните уже вычисленные значения '
                   'в замыкании.',
      'starter': 'function fib(n) {\n}\n',
      'driver': '/*__DRIVER__*/\nfor (const n of [0, 1, 2, 10, 30, 50, 70]) console.log(fib(n));\n',
      'hint': 'Map внутри замыкания (или внешняя переменная) + проверка перед рекурсивным вызовом.',
      'expected': ['0', '1', '1', '55', '832040', '12586269025', '190392490709135']},
     {'id': 'j6-flatten',
      'mode': 'js',
      'title': 'Глубокое выравнивание массива',
      'statement': 'Напишите рекурсивную функцию flatten(arr): возвращает плоский массив со всеми элементами '
                   'вложенных массивов любой глубины, в исходном порядке. Методы flat и flatMap использовать '
                   'нельзя.',
      'starter': 'function flatten(arr) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(JSON.stringify(flatten([1, [2, [3, [4]], 5]])));\n'
                'console.log(JSON.stringify(flatten([])));\n'
                'console.log(JSON.stringify(flatten([[], [[]], 1])));\n'
                'console.log(JSON.stringify(flatten(["a", ["b"]])));\n'
                'console.log(__count(".fl" + "at(") + __count(".fla" + "tMap("));\n',
      'hint': 'Для вложенного массива — рекурсивный вызов и spread результата.',
      'expected': ['[1,2,3,4,5]', '[]', '[1]', '["a","b"]', '0']},
     {'id': 'j6-sum-tree',
      'mode': 'js',
      'title': 'Сумма значений дерева',
      'statement': 'Дерево задано объектами { value, children: [...] }. Напишите функцию sumTree(node): '
                   'сумма value всех узлов дерева (рекурсивно).',
      'starter': 'function sumTree(node) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const t = { value: 1, children: [{ value: 2, children: [{ value: 4, children: [] }] }, { '
                'value: 3, children: [] }] };\n'
                'console.log(sumTree(t));\n'
                'console.log(sumTree({ value: 5, children: [] }));\n'
                'console.log(sumTree({ value: 0, children: [{ value: -1, children: [] }] }));\n',
      'hint': 'Значение узла плюс суммы поддеревьев детей.',
      'expected': ['10', '5', '-1']},
     {'id': 'j6-hanoi',
      'mode': 'js',
      'title': 'Ханойские башни',
      'statement': 'Напишите функцию hanoi(n): возвращает массив ходов ["A→C", …], которыми n дисков '
                   'переносятся со стержня A на стержень C через B по правилам игры (рекурсивно, за '
                   'минимальное число ходов).',
      'starter': 'function hanoi(n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(hanoi(1).join(" "));\n'
                'console.log(hanoi(2).join(" "));\n'
                'console.log(hanoi(3).join(" "));\n'
                'console.log(hanoi(10).length);\n',
      'hint': 'Перенести n-1 на B, диск на C, затем n-1 с B на C: значения from, to, via можно передавать '
              'параметрами по умолчанию.',
      'expected': ['A→C', 'A→B A→C B→C', 'A→C A→B C→B A→C B→A B→C A→C', '1023']},
     {'id': 'j6-stack',
      'mode': 'js',
      'title': 'Стек в замыкании',
      'statement': 'Напишите функцию createStack(): она возвращает объект с методами push(x), pop() (снимает '
                   'и возвращает вершину, для пустого стека — undefined), peek() (вершина без снятия) и '
                   'size(). Массив с данными не должен быть доступен снаружи.',
      'starter': 'function createStack() {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const s = createStack();\n'
                's.push(1); s.push(2); s.push(3);\n'
                'console.log(s.size(), s.peek(), s.pop(), s.pop(), s.size());\n'
                'console.log(s.pop(), s.pop(), s.size());\n'
                'console.log(JSON.stringify(Object.keys(s).sort()));\n'
                'console.log(Object.values(s).every((v) => typeof v === "function"));\n'
                'const t = createStack();\n'
                'console.log(t.size());\n',
      'hint': 'Массив items объявите внутри createStack — он живёт в замыкании методов.',
      'expected': ['3 3 3 2 1', '1 undefined 0', '["peek","pop","push","size"]', 'true', '0']},
     {'id': 'j6-fn-info',
      'mode': 'js',
      'title': 'Имя и число параметров функции',
      'statement': 'Напишите функцию fnInfo(fn): возвращает массив [fn.name, fn.length] — имя функции и '
                   'число её объявленных параметров (параметры по умолчанию и rest не считаются).',
      'starter': 'function fnInfo(fn) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'function add(a, b) { return a + b; }\n'
                'const dbl = (x) => x * 2;\n'
                'console.log(JSON.stringify(fnInfo(add)));\n'
                'console.log(JSON.stringify(fnInfo(dbl)));\n'
                'console.log(JSON.stringify(fnInfo((a, b = 1, ...c) => 0)));\n'
                'console.log(JSON.stringify(fnInfo(() => 0)));\n'
                'console.log(JSON.stringify(fnInfo(function () {})));\n',
      'hint': 'У функции есть поля name и length.',
      'expected': ['["add",2]', '["dbl",1]', '["",1]', '["",0]', '["",0]']}]}
