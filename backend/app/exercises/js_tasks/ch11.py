"""Задачи книги «Современный Frontend», глава 11 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {11: [{'id': 'j11-is-pure',
       'mode': 'js',
       'title': 'Проверка на чистоту',
       'statement': 'Напишите функцию checkPurity(fn, args): args — массив аргументов (JSON-подобных '
                    'данных). Вызовите fn дважды на глубоких копиях аргументов (структурно клонированных) и '
                    'верните { deterministic, mutatesArgs }: deterministic — результаты двух вызовов глубоко '
                    'равны (сравнивайте через JSON.stringify), mutatesArgs — после вызова аргументы '
                    'отличаются от исходных (по JSON.stringify).',
       'starter': 'function checkPurity(fn, args) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let counter = 0;\n'
                 'const cases = [\n'
                 '  ["pure", (a, b) => a + b, [1, 2]],\n'
                 '  ["random", () => Math.random(), []],\n'
                 '  ["push", (arr) => arr.push(1), [[1, 2]]],\n'
                 '  ["sort", (arr) => arr.sort(), [[3, 1, 2]]],\n'
                 '  ["toSorted", (arr) => arr.toSorted(), [[3, 1, 2]]],\n'
                 '  ["counter", () => ++counter, []],\n'
                 '  ["setField", (o) => { o.x = 1; return o; }, [{ x: 0 }]],\n'
                 '  ["spread", (o) => ({ ...o, x: 1 }), [{ x: 0 }]],\n'
                 '];\n'
                 'for (const [name, fn, args] of cases) console.log(name, JSON.stringify(checkPurity(fn, '
                 'args)));\n',
       'hint': 'Копии аргументов: structuredClone; сравнение — через JSON.stringify до и после.',
       'expected': ['pure {"deterministic":true,"mutatesArgs":false}',
                    'random {"deterministic":false,"mutatesArgs":false}',
                    'push {"deterministic":true,"mutatesArgs":true}',
                    'sort {"deterministic":true,"mutatesArgs":true}',
                    'toSorted {"deterministic":true,"mutatesArgs":false}',
                    'counter {"deterministic":false,"mutatesArgs":false}',
                    'setField {"deterministic":true,"mutatesArgs":true}',
                    'spread {"deterministic":true,"mutatesArgs":false}']},
      {'id': 'j11-immutable-arrays',
       'mode': 'js',
       'title': 'Неизменяемые операции над массивами',
       'statement': 'Напишите функции (ни одна не меняет исходный массив): insertAt(arr, i, x), '
                    'removeAt(arr, i), replaceAt(arr, i, x), move(arr, from, to) (переставить элемент с '
                    'позиции from на позицию to), swap(arr, i, j). Индексы корректны (0 ≤ i ≤ длина для '
                    'insertAt, иначе внутри массива).',
       'starter': 'function insertAt(arr, i, x) {\n'
                  '}\n'
                  'function removeAt(arr, i) {\n'
                  '}\n'
                  'function replaceAt(arr, i, x) {\n'
                  '}\n'
                  'function move(arr, from, to) {\n'
                  '}\n'
                  'function swap(arr, i, j) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const a = Object.freeze(["a", "b", "c", "d"]);\n'
                 'const show = (x) => console.log(JSON.stringify(x));\n'
                 'show(insertAt(a, 2, "X")); show(insertAt(a, 4, "Y")); show(insertAt(a, 0, "Z"));\n'
                 'show(removeAt(a, 0)); show(removeAt(a, 3));\n'
                 'show(replaceAt(a, 1, "B"));\n'
                 'show(move(a, 0, 2)); show(move(a, 3, 0)); show(move(a, 1, 1));\n'
                 'show(swap(a, 0, 3)); show(swap(a, 1, 1));\n'
                 'show(a);\n',
       'hint': 'Срезы и spread: [...arr.slice(0, i), x, ...arr.slice(i)].',
       'expected': ['["a","b","X","c","d"]',
                    '["a","b","c","d","Y"]',
                    '["Z","a","b","c","d"]',
                    '["b","c","d"]',
                    '["a","b","c"]',
                    '["a","B","c","d"]',
                    '["b","c","a","d"]',
                    '["d","a","b","c"]',
                    '["a","b","c","d"]',
                    '["d","b","c","a"]',
                    '["a","b","c","d"]',
                    '["a","b","c","d"]']},
      {'id': 'j11-update-in',
       'mode': 'js',
       'title': 'updateIn, removeKey, mergeDeep',
       'statement': 'Напишите неизменяемые функции для объектов: updateIn(obj, path, fn) — применяет fn к '
                    'значению по пути (массив ключей; путь может содержать индексы массивов; недостающие '
                    'объекты создаются как {}); removeKey(obj, key) — копия без ключа; mergeDeep(a, b) — '
                    'глубокое слияние обычных объектов (значения b побеждают; массивы заменяются целиком). '
                    'Ветви, не затронутые изменением, должны остаться теми же ссылками.',
       'starter': 'function updateIn(obj, path, fn) {\n'
                  '}\n'
                  'function removeKey(obj, key) {\n'
                  '}\n'
                  'function mergeDeep(a, b) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const s = Object.freeze({ user: Object.freeze({ name: "Ада", tags: Object.freeze(["a", '
                 '"b"]) }), items: Object.freeze([1, 2]) });\n'
                 'const t = updateIn(s, ["user", "name"], (n) => n.toUpperCase());\n'
                 'console.log(JSON.stringify(t), t.items === s.items, t.user.tags === s.user.tags);\n'
                 'console.log(JSON.stringify(updateIn(s, ["user", "tags", 1], (x) => x + "!")));\n'
                 'console.log(JSON.stringify(updateIn({}, ["a", "b", "count"], (n = 0) => n + 1)));\n'
                 'console.log(JSON.stringify(removeKey({ a: 1, b: 2 }, "a")), JSON.stringify(removeKey({ a: '
                 '1 }, "zzz")));\n'
                 'console.log(JSON.stringify(mergeDeep({ a: { x: 1, y: 2 }, l: [1] }, { a: { y: 9, z: 3 }, '
                 'l: [2, 3], n: 5 })));\n'
                 'const base = { p: { q: 1 }, r: { s: 2 } };\n'
                 'const m = mergeDeep(base, { p: { q: 5 } });\n'
                 'console.log(m.r === base.r, JSON.stringify(base));\n',
       'hint': 'Рекурсия по пути: копируйте только узлы вдоль пути (объект — spread, массив — копия).',
       'expected': ['{"user":{"name":"АДА","tags":["a","b"]},"items":[1,2]} true true',
                    '{"user":{"name":"Ада","tags":["a","b!"]},"items":[1,2]}',
                    '{"a":{"b":{"count":"[object Object]1"}}}',
                    '{"b":2} {"a":1}',
                    '{"a":{"x":1,"y":9,"z":3},"l":[2,3],"n":5}',
                    'true {"p":{"q":1},"r":{"s":2}}']},
      {'id': 'j11-curry',
       'mode': 'js',
       'title': 'Автокаррирование',
       'statement': 'Напишите функцию curry(fn): возвращает каррированную версию: вызывать можно с любым '
                    'числом аргументов за раз, пока не накоплено fn.length — тогда вызывается fn. '
                    'Каррированная функция должна принимать и сразу все аргументы. Для функций без '
                    'обязательных параметров (length 0) — вызов при первом обращении.',
       'starter': 'function curry(fn) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const vol = curry((a, b, c) => a * b * c);\n'
                 'console.log(vol(2)(3)(4), vol(2, 3)(4), vol(2)(3, 4), vol(2, 3, 4));\n'
                 'const double = vol(2, 1);\n'
                 'console.log(double(5), double(7));\n'
                 'const greet = curry((greeting, name) => `${greeting}, ${name}!`);\n'
                 'console.log(["Ада", "Линус"].map(greet("Привет")).join(" "));\n'
                 'console.log(curry(() => "ноль")());\n'
                 'console.log(typeof vol(1), typeof vol(1)(2));\n'
                 'const sum4 = curry((a, b, c, d) => a + b + c + d);\n'
                 'console.log(sum4(1)(2)(3)(4), sum4(1, 2)(3, 4), sum4(1)(2, 3, 4));\n',
       'hint': 'Накапливайте аргументы; когда их не меньше fn.length — вызывайте fn.',
       'expected': ['24 24 24 24',
                    '10 14',
                    'Привет, Ада! Привет, Линус!',
                    'ноль',
                    'function function',
                    '10 10 10']},
      {'id': 'j11-partial-flip',
       'mode': 'js',
       'title': 'partial, partialRight, flip',
       'statement': 'Напишите функции partial(fn, ...left) (фиксирует первые аргументы), partialRight(fn, '
                    '...right) (фиксирует последние: вызов fn(...новые, ...right)) и flip(fn) (меняет '
                    'местами первые два аргумента: flip(f)(a, b, ...rest) = f(b, a, ...rest)).',
       'starter': 'function partial(fn, ...left) {\n'
                  '}\n'
                  'function partialRight(fn, ...right) {\n'
                  '}\n'
                  'function flip(fn) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sub = (a, b, c = 0) => a - b - c;\n'
                 'console.log(partial(sub, 10)(3), partial(sub, 10, 3)(), partial(sub, 10, 3)(1));\n'
                 'console.log(partialRight(sub, 3)(10), partialRight(sub, 3, 1)(10), partialRight((a, b) => '
                 '`${a}/${b}`, "z")("y"));\n'
                 'console.log(flip(sub)(3, 10), flip(sub)(3, 10, 1), flip((a, b) => [a, b])("x", '
                 '"y").join());\n'
                 'console.log(partial(Math.max, 5)(1, 9), partialRight(Math.pow, 2)(7));\n',
       'hint': 'Каждая — стрелка, возвращающая стрелку, склеивающая аргументы через spread.',
       'expected': ['7 7 6', '7 6 y/z', '7 6 y,x', '9 49']},
      {'id': 'j11-compose-pipe',
       'mode': 'js',
       'title': 'compose, pipe и tap',
       'statement': 'Напишите функции compose(...fns) (справа налево) и pipe(...fns) (слева направо); первая '
                    'применяемая функция может принимать несколько аргументов, остальные — по одному; без '
                    'функций — тождественная (возвращает первый аргумент). И tap(fn) → функция, которая '
                    'вызывает fn(x) ради побочного эффекта и возвращает x.',
       'starter': 'function compose(...fns) {\n}\nfunction pipe(...fns) {\n}\nfunction tap(fn) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const inc = (x) => x + 1, dbl = (x) => x * 2, add = (a, b) => a + b;\n'
                 'console.log(pipe(inc, dbl)(3), compose(inc, dbl)(3));\n'
                 'console.log(pipe(add, dbl)(2, 3), compose(dbl, add)(2, 3));\n'
                 'console.log(pipe()(7), compose()(8), pipe(inc)(1));\n'
                 'const log = [];\n'
                 'console.log(pipe(inc, tap((x) => log.push("после inc: " + x)), dbl, tap((x) => '
                 'log.push("итог: " + x)))(4), log.join(" | "));\n'
                 'console.log(pipe((s) => s.trim(), (s) => s.split(" "), (a) => a.length)("  раз два три '
                 '"));\n',
       'hint': 'pipe через reduce; compose — pipe от перевёрнутого списка.',
       'expected': ['8 7', '10 10', '7 8 2', '10 после inc: 5 | итог: 10', '3']},
      {'id': 'j11-data-last',
       'mode': 'js',
       'title': 'Каррированные map, filter, reduce, prop',
       'statement': 'Напишите набор каррированных функций «данные последними»: map(f)(xs), filter(p)(xs), '
                    'reduce(f, init)(xs), prop(key)(obj), sortBy(f)(xs) (по возрастанию значения f, '
                    'сортировка устойчива, исходный массив не меняется), uniq(xs), sum(xs), take(n)(xs). '
                    'Затем композицией: topPrices — «взять цены, отфильтровать дороже 10, отсортировать, '
                    'взять 3».',
       'starter': 'const map = null;\n'
                  'const filter = null;\n'
                  'const reduce = null;\n'
                  'const prop = null;\n'
                  'const sortBy = null;\n'
                  'const uniq = null;\n'
                  'const sum = null;\n'
                  'const take = null;\n'
                  'const topPrices = null;\n',
       'driver': '/*__DRIVER__*/\n'
                 'const items = [{ n: "a", price: 30 }, { n: "b", price: 5 }, { n: "c", price: 12 }, { n: '
                 '"d", price: 20 }, { n: "e", price: 11 }];\n'
                 'console.log(JSON.stringify(map((x) => x * 2)([1, 2, 3])), JSON.stringify(filter((x) => x % '
                 '2)([1, 2, 3])), reduce((a, b) => a + b, 10)([1, 2]));\n'
                 'console.log(prop("n")(items[0]), sum([1, 2, 3]), JSON.stringify(uniq([1, 2, 1, 3, 2])), '
                 'JSON.stringify(take(2)([5, 6, 7])), JSON.stringify(take(9)([1])));\n'
                 'console.log(JSON.stringify(sortBy((x) => x.price)(items).map((x) => x.n)), items[0].n);\n'
                 'console.log(JSON.stringify(sortBy((s) => s.length)(["ccc", "a", "bb", "d"])));\n'
                 'console.log(JSON.stringify(topPrices(items)));\n',
       'hint': 'Каждая функция сначала принимает настройки, затем данные.',
       'expected': ['[2,4,6] [1,3] 13',
                    'a 6 [1,2,3] [5,6] [1]',
                    '["b","e","c","d","a"] a',
                    '["a","d","bb","ccc"]',
                    '[11,12,20]']},
      {'id': 'j11-memoize-key',
       'mode': 'js',
       'title': 'Мемоизация с функцией ключа',
       'statement': 'Напишите функцию memoize(fn, keyFn = (...args) => JSON.stringify(args)): кэширует '
                    'результаты по ключу; повторный вызов с тем же ключом не вызывает fn; у результата есть '
                    'метод stats() → { hits, misses } и clear(). Исключения не кэшируются.',
       'starter': 'function memoize(fn, keyFn) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let calls = 0;\n'
                 'const slow = memoize((a, b) => { calls++; return a + b; });\n'
                 'console.log(slow(1, 2), slow(1, 2), slow(2, 1), slow(1, 2), calls, '
                 'JSON.stringify(slow.stats()));\n'
                 'const byId = memoize((obj) => { calls++; return obj.id * 10; }, (obj) => obj.id);\n'
                 'console.log(byId({ id: 1, x: "a" }), byId({ id: 1, x: "b" }), byId({ id: 2 }), calls);\n'
                 'let boom = 0;\n'
                 'const flaky = memoize((x) => { if (++boom < 2) throw new Error("первый раз"); return x; '
                 '});\n'
                 'try { flaky(1); } catch (e) { console.log(e.message); }\n'
                 'console.log(flaky(1), flaky(1), boom);\n'
                 'slow.clear();\n'
                 'slow(1, 2);\n'
                 'console.log(JSON.stringify(slow.stats()), calls);\n'
                 'const fib = memoize((n) => (n < 2 ? n : fib(n - 1) + fib(n - 2)));\n'
                 'console.log(fib(80));\n',
       'hint': 'Map ключ → результат; исключение вылетает до записи в кэш.',
       'expected': ['3 3 3 3 2 {"hits":2,"misses":2}',
                    '10 10 20 4',
                    'первый раз',
                    '1 1 2',
                    '{"hits":2,"misses":3} 5',
                    '23416728348467684']},
      {'id': 'j11-before-after',
       'mode': 'js',
       'title': 'before, after, once, unary',
       'statement': 'Напишите функции-обёртки: once(fn) (вызывает fn только первый раз, дальше возвращает '
                    'прежний результат), before(n, fn) (вызывает fn первые n - 1 раз, после — возвращает '
                    'результат последнего вызова), after(n, fn) (fn начинает вызываться с n-го обращения), '
                    'unary(fn) (передаёт в fn только первый аргумент — полезно для map(parseInt)).',
       'starter': 'function once(fn) {\n'
                  '}\n'
                  'function before(n, fn) {\n'
                  '}\n'
                  'function after(n, fn) {\n'
                  '}\n'
                  'function unary(fn) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let c = 0;\n'
                 'const inc = () => ++c;\n'
                 'const o = once(inc); console.log(o(), o(), o(), c);\n'
                 'c = 0;\n'
                 'const b = before(3, inc); console.log(b(), b(), b(), b(), c);\n'
                 'c = 0;\n'
                 'const a = after(3, inc); console.log(a(), a(), a(), a(), c);\n'
                 'console.log(JSON.stringify(["1", "2", "3"].map(parseInt)), JSON.stringify(["1", "2", '
                 '"3"].map(unary(parseInt))));\n'
                 'console.log(once((x) => x * 2)(21), unary(Math.max)(1, 9));\n',
       'hint': 'Счётчик вызовов в замыкании; before запоминает последний результат.',
       'expected': ['1 1 1 1', '1 2 2 2 2', 'undefined undefined 1 2 2', '[1,null,null] [1,2,3]', '42 1']},
      {'id': 'j11-trampoline',
       'mode': 'js',
       'title': 'Батут',
       'statement': 'Напишите функцию trampoline(fn): возвращает функцию, которая вызывает fn и, пока '
                    'результат — функция, вызывает её, возвращая итог; стек не растёт. Примените: sumTo(n) '
                    '(сумма 1..n) и isEven(n)/isOdd(n) через взаимную рекурсию на батуте работают для n = 1 '
                    '000 000. Определите sumTo, isEven, isOdd самостоятельно (isEven/isOdd вызывают друг '
                    'друга через возвращаемые шаги).',
       'starter': 'function trampoline(fn) {\n'
                  '}\n'
                  'const sumTo = null;\n'
                  'const isEven = null;\n'
                  'const isOdd = null;\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(sumTo(10), sumTo(0), sumTo(1000000));\n'
                 'console.log(isEven(10), isEven(7), isOdd(7), isOdd(0), isEven(1000000), isOdd(999999));\n'
                 'const naive = (n) => (n === 0 ? 0 : n + naive(n - 1));\n'
                 'try { naive(1000000); console.log("без ошибки?"); } catch (e) { console.log(e.name); }\n'
                 'const t = trampoline((n) => (n > 3 ? "готово " + n : () => t2(n + 1)));\n'
                 'const t2 = (n) => (n > 3 ? "готово " + n : () => t2(n + 1));\n'
                 'console.log(t(0));\n',
       'hint': 'Шаг возвращает либо значение, либо стрелку без аргументов — следующий шаг.',
       'expected': ['55 0 500000500000', 'true false true false true true', 'RangeError', 'готово 4']},
      {'id': 'j11-recursion',
       'mode': 'js',
       'title': 'Рекурсия: перестановки и подмножества',
       'statement': 'Напишите чистые рекурсивные функции: permutations(arr) (все перестановки в '
                    'лексикографическом порядке индексов: сначала с первым элементом на месте и т.д.), '
                    'subsets(arr) (все подмножества: сначала без первого элемента, затем с ним: для [1,2] — '
                    '[], [2], [1], [1,2]… порядок задан примером в драйвере) и flattenDeep(arr).',
       'starter': 'function permutations(arr) {\n'
                  '}\n'
                  'function subsets(arr) {\n'
                  '}\n'
                  'function flattenDeep(arr) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(JSON.stringify(permutations([1, 2, 3])));\n'
                 'console.log(JSON.stringify(permutations([])), JSON.stringify(permutations(["a"])));\n'
                 'console.log(JSON.stringify(subsets([1, 2])), JSON.stringify(subsets([])), subsets([1, 2, '
                 '3, 4]).length);\n'
                 'console.log(JSON.stringify(flattenDeep([1, [2, [3, [4, [5]]]], [], 6])));\n'
                 'const a = [3, 1, 2];\n'
                 'permutations(a);\n'
                 'console.log(JSON.stringify(a));\n',
       'hint': 'permutations: для каждого элемента — перестановки остальных; subsets: подмножества хвоста '
               'без головы и с головой.',
       'expected': ['[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]',
                    '[[]] [["a"]]',
                    '[[],[2],[1],[1,2]] [[]] 16',
                    '[1,2,3,4,5,6]',
                    '[3,1,2]']},
      {'id': 'j11-reduce-all',
       'mode': 'js',
       'title': 'Всё через reduce',
       'statement': 'Напишите функции, реализованные только через reduce (без '
                    'map/filter/for/while/цикла/Set/flatMap): mapR(xs, f), filterR(xs, p), groupByR(xs, f) '
                    '(объект ключ → массив), countByR(xs, f), uniqR(xs) (по порядку первого появления), '
                    'maxByR(xs, f) (элемент с наибольшим f(x); при равенстве — первый; для пустого массива — '
                    'undefined).',
       'starter': 'function mapR(xs, f) {\n'
                  '}\n'
                  'function filterR(xs, p) {\n'
                  '}\n'
                  'function groupByR(xs, f) {\n'
                  '}\n'
                  'function countByR(xs, f) {\n'
                  '}\n'
                  'function uniqR(xs) {\n'
                  '}\n'
                  'function maxByR(xs, f) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'const nums = [1, 2, 3, 4, 5, 6];\n'
                 'console.log(JSON.stringify(mapR(nums, (x, i) => x * i)), JSON.stringify(filterR(nums, (x) '
                 '=> x % 2 === 0)));\n'
                 'console.log(JSON.stringify(groupByR(nums, (x) => (x % 3 === 0 ? "три" : "прочие"))), '
                 'JSON.stringify(countByR(["a", "bb", "cc", "d"], (s) => s.length)));\n'
                 'console.log(JSON.stringify(uniqR([3, 1, 3, 2, 1])), JSON.stringify(maxByR(["aa", "b", '
                 '"cccc", "dddd"], (s) => s.length)), maxByR([], (x) => x));\n'
                 'const src = [...nums];\n'
                 'mapR(src, (x) => x); console.log(JSON.stringify(src));\n'
                 'const banned = [".ma" + "p(", ".fil" + "ter(", "for" + " (", "wh" + "ile", "new Se" + "t", '
                 '".flatM" + "ap(", "for" + "Each"];\n'
                 'console.log(banned.reduce((n, p) => n + __count(p), 0));\n',
       'hint': 'Накопитель — массив или объект; на каждом шаге возвращайте новое значение.',
       'expected': ['[0,2,6,12,20,30] [2,4,6]',
                    '{"прочие":[1,2,4,5],"три":[3,6]} {"1":2,"2":2}',
                    '[3,1,2] "cccc" undefined',
                    '[1,2,3,4,5,6]',
                    '0']},
      {'id': 'j11-zip-transpose',
       'mode': 'js',
       'title': 'zipWith, unzip, transpose',
       'statement': 'Напишите чистые функции: zipWith(f, a, b) (до длины короткого), unzip(pairs) → [первые, '
                    'вторые] (из массива пар), transpose(matrix) (матрица как массив строк; строки разной '
                    'длины — транспонируются до самой длинной, недостающие ячейки пропускаются), и '
                    'pairwise(xs) → соседние пары [x0,x1],[x1,x2]….',
       'starter': 'function zipWith(f, a, b) {\n'
                  '}\n'
                  'function unzip(pairs) {\n'
                  '}\n'
                  'function transpose(matrix) {\n'
                  '}\n'
                  'function pairwise(xs) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(JSON.stringify(zipWith((a, b) => a + b, [1, 2, 3], [10, 20])));\n'
                 'console.log(JSON.stringify(unzip([[1, "a"], [2, "b"], [3, "c"]])), '
                 'JSON.stringify(unzip([])));\n'
                 'console.log(JSON.stringify(transpose([[1, 2, 3], [4, 5, 6]])), '
                 'JSON.stringify(transpose([[1, 2], [3], [4, 5, 6]])), JSON.stringify(transpose([])));\n'
                 'console.log(JSON.stringify(pairwise([1, 2, 3, 4])), JSON.stringify(pairwise([1])), '
                 'JSON.stringify(pairwise([])));\n',
       'hint': 'Array.from({ length }, (_, i) => …) строит результат по индексам.',
       'expected': ['[11,22]',
                    '[[1,2,3],["a","b","c"]] [[],[]]',
                    '[[1,4],[2,5],[3,6]] [[1,3,4],[2,5],[6]] []',
                    '[[1,2],[2,3],[3,4]] [] []']},
      {'id': 'j11-scan-unfold',
       'mode': 'js',
       'title': 'scan и unfold',
       'statement': 'Напишите функции scan(f, init, xs) → массив промежуточных накоплений (без начального '
                    'значения: для [1,2,3] и сложения — [1,3,6]), unfold(f, seed) → массив: f(seed) '
                    'возвращает [значение, следующееСемя] или null для остановки (например, unfold(n => n > '
                    '5 ? null : [n * n, n + 1], 1)), и windowed(xs, size) — скользящие окна.',
       'starter': 'function scan(f, init, xs) {\n'
                  '}\n'
                  'function unfold(f, seed) {\n'
                  '}\n'
                  'function windowed(xs, size) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(JSON.stringify(scan((a, b) => a + b, 0, [1, 2, 3, 4])), '
                 'JSON.stringify(scan((a, b) => a * b, 1, [])), JSON.stringify(scan((a, x) => a + x, "", '
                 '["a", "b", "c"])));\n'
                 'console.log(JSON.stringify(unfold((n) => (n > 5 ? null : [n * n, n + 1]), 1)), '
                 'JSON.stringify(unfold(() => null, 0)));\n'
                 'console.log(JSON.stringify(unfold(([a, b]) => (a > 50 ? null : [a, [b, a + b]]), [0, '
                 '1])));\n'
                 'console.log(JSON.stringify(windowed([1, 2, 3, 4, 5], 3)), JSON.stringify(windowed([1, 2], '
                 '3)), JSON.stringify(windowed([1, 2, 3], 1)), JSON.stringify(windowed([1, 2], 0)));\n',
       'hint': 'scan — как reduce, но сохраняет каждый шаг; unfold — «обратный reduce».',
       'expected': ['[1,3,6,10] [] ["a","ab","abc"]',
                    '[1,4,9,16,25] []',
                    '[0,1,1,2,3,5,8,13,21,34]',
                    '[[1,2,3],[2,3,4],[3,4,5]] [] [[1],[2],[3]] []']},
      {'id': 'j11-maybe',
       'mode': 'js',
       'title': 'Maybe',
       'statement': 'Напишите фабрики Just(value) и Nothing() и методы объектов: map(f) (для Nothing — '
                    'Nothing), chain(f) (f возвращает Maybe), getOrElse(d), isNothing(), toString() '
                    '(«Just(5)» / «Nothing»). Функция fromNullable(x) → Nothing для null/undefined, иначе '
                    'Just(x). Значения 0, пустая строка и false — это Just.',
       'starter': 'function Just(value) {\n}\nfunction Nothing() {\n}\nfunction fromNullable(x) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const show = (m) => console.log(String(m));\n'
                 'show(Just(5).map((x) => x + 1));\n'
                 'show(Nothing().map((x) => x + 1));\n'
                 'show(fromNullable(null)); show(fromNullable(undefined)); show(fromNullable(0)); '
                 'show(fromNullable(""));\n'
                 'const safeDiv = (a, b) => (b === 0 ? Nothing() : Just(a / b));\n'
                 'show(Just(10).chain((x) => safeDiv(x, 2)).chain((x) => safeDiv(x, 0)).map((x) => x * '
                 '100));\n'
                 'console.log(Just(3).getOrElse(0), Nothing().getOrElse(0), Just(1).isNothing(), '
                 'Nothing().isNothing());\n'
                 'const user = { profile: { name: "Ада" } };\n'
                 'console.log(fromNullable(user).map((u) => u.profile).chain((p) => '
                 'fromNullable(p.name)).map((n) => n.toUpperCase()).getOrElse("аноним"));\n'
                 'console.log(fromNullable({}).map((u) => u.profile).chain((p) => fromNullable(p && '
                 'p.name)).getOrElse("аноним"));\n',
       'hint': 'Nothing — общий объект, методы которого возвращают его самого.',
       'expected': ['Just(6)',
                    'Nothing',
                    'Nothing',
                    'Nothing',
                    'Just(0)',
                    'Just("")',
                    'Nothing',
                    '3 0 false true',
                    'АДА',
                    'аноним']},
      {'id': 'j11-either',
       'mode': 'js',
       'title': 'Either',
       'statement': 'Напишите Right(value) и Left(error) с методами map(f) (для Left — без изменений), '
                    'mapLeft(f), chain(f), fold(onLeft, onRight), toString() («Right(1)» / «Left("e")»). И '
                    'функции tryCatch(fn) → Right(результат) или Left(исключение), sequence(eithers) → '
                    'Right(массив значений) если все Right, иначе первый Left.',
       'starter': 'function Right(value) {\n'
                  '}\n'
                  'function Left(error) {\n'
                  '}\n'
                  'function tryCatch(fn) {\n'
                  '}\n'
                  'function sequence(eithers) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const parse = (s) => (Number.isNaN(Number(s)) ? Left("не число: " + s) : '
                 'Right(Number(s)));\n'
                 'const pos = (n) => (n > 0 ? Right(n) : Left("не положительное: " + n));\n'
                 'console.log(String(parse("5").chain(pos).map((x) => x * 2)));\n'
                 'console.log(String(parse("-5").chain(pos).map((x) => x * 2)));\n'
                 'console.log(String(parse("x").chain(pos)));\n'
                 'console.log(String(parse("x").mapLeft((m) => m.toUpperCase())), '
                 'String(Right(1).mapLeft((m) => m + "!")));\n'
                 'console.log(parse("7").fold((e) => "ошибка " + e, (v) => "значение " + v), '
                 'parse("z").fold((e) => "ошибка " + e, (v) => "значение " + v));\n'
                 'console.log(tryCatch(() => JSON.parse(\'{"a":1}\')).fold(() => "плохо", (o) => o.a), '
                 'tryCatch(() => JSON.parse("{")).fold((e) => e.name, () => "ок"));\n'
                 'console.log(String(sequence([parse("1"), parse("2"), parse("3")])), '
                 'String(sequence([parse("1"), parse("a"), parse("b")])), String(sequence([])));\n',
       'hint': 'Left и Right — объекты с одним и тем же набором методов, но разным поведением.',
       'expected': ['Right(10)',
                    'Left("не положительное: -5")',
                    'Left("не число: x")',
                    'Left("НЕ ЧИСЛО: X") Right(1)',
                    'значение 7 ошибка не число: z',
                    '1 SyntaxError',
                    'Right([1,2,3]) Left("не число: a") Right([])']},
      {'id': 'j11-safe-path',
       'mode': 'js',
       'title': 'Безопасный доступ через Maybe-подход',
       'statement': 'Напишите функции get(path, obj) → значение по пути (массив ключей) или undefined, если '
                    'на пути null/undefined (без исключений); getOr(def, path, obj); и pluckAll(path, list) '
                    '→ массив значений по пути только из тех элементов, где значение существует (не '
                    'null/undefined), в порядке списка. Функции каррированные: get(path)(obj), getOr(def, '
                    'path)(obj), pluckAll(path)(list).',
       'starter': 'function get(path) {\n}\nfunction getOr(def, path) {\n}\nfunction pluckAll(path) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const u = { a: { b: [10, { c: "глубоко" }] }, z: null, f: 0 };\n'
                 'console.log(get(["a", "b", 1, "c"])(u), get(["a", "x", "y"])(u), get(["z", "q"])(u), '
                 'get([])(u) === u, get(["f"])(u));\n'
                 'console.log(getOr("нет", ["a", "b", 1, "c"])(u), getOr("нет", ["z"])(u), getOr("нет", '
                 '["f"])(u), getOr(0, ["q", "w"])(null));\n'
                 'const users = [{ p: { age: 30 } }, {}, { p: null }, { p: { age: 0 } }, { p: { age: 25 } '
                 '}];\n'
                 'console.log(JSON.stringify(pluckAll(["p", "age"])(users)));\n',
       'hint': 'reduce по ключам с проверкой на null/undefined на каждом шаге.',
       'expected': ['глубоко undefined undefined true 0', 'глубоко нет 0 0', '[30,0,25]']},
      {'id': 'j11-functor-laws',
       'mode': 'js',
       'title': 'Проверка законов функтора',
       'statement': 'Напишите функцию checkFunctorLaws(make, value, f, g): make(v) создаёт контейнер с '
                    'методом map и методом unwrap() (достать значение для сравнения); верните { identity, '
                    'composition } — выполняются ли законы: container.map(x => x) равен container (сравнение '
                    'через JSON.stringify(unwrap())) и container.map(x => f(g(x))) равен '
                    'container.map(g).map(f).',
       'starter': 'function checkFunctorLaws(make, value, f, g) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const Box = (v) => ({ map: (f) => Box(f(v)), unwrap: () => v });\n'
                 'const BadBox = (v) => ({ map: (f) => BadBox(f(f(v))), unwrap: () => v });\n'
                 'const Counter = (v, n = 0) => ({ map: (f) => Counter(f(v), n + 1), unwrap: () => [v, n] '
                 '});\n'
                 'const List = (xs) => ({ map: (f) => List(xs.map(f)), unwrap: () => xs });\n'
                 'const f = (x) => x + 1, g = (x) => x * 2;\n'
                 'console.log(JSON.stringify(checkFunctorLaws(Box, 3, f, g)));\n'
                 'console.log(JSON.stringify(checkFunctorLaws(BadBox, 3, f, g)));\n'
                 'console.log(JSON.stringify(checkFunctorLaws(Counter, 3, f, g)));\n'
                 'console.log(JSON.stringify(checkFunctorLaws(List, [1, 2, 3], f, g)));\n',
       'hint': 'Создайте контейнер, примените оба варианта и сравните распакованные значения.',
       'expected': ['{"identity":true,"composition":true}',
                    '{"identity":true,"composition":false}',
                    '{"identity":false,"composition":false}',
                    '{"identity":true,"composition":true}']},
      {'id': 'j11-reducer',
       'mode': 'js',
       'title': 'Редьюсер списка дел',
       'statement': 'Напишите чистый редьюсер todos(state = [], action): действия { type: "add", id, text }, '
                    '{ type: "toggle", id }, { type: "remove", id }, { type: "clearDone" }, { type: '
                    '"rename", id, text }. Задача: { id, text, done: false }. Неизвестное действие или '
                    'несуществующий id — вернуть то же состояние (ту же ссылку). Состояние не мутировать, у '
                    'нетронутых задач ссылки остаются прежними.',
       'starter': 'function todos(state = [], action) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const actions = [{ type: "add", id: 1, text: "молоко" }, { type: "add", id: 2, text: '
                 '"хлеб" }, { type: "add", id: 3, text: "сыр" }, { type: "toggle", id: 2 }, { type: '
                 '"rename", id: 1, text: "кефир" }, { type: "toggle", id: 9 }, { type: "nope" }, { type: '
                 '"clearDone" }, { type: "remove", id: 3 }];\n'
                 'let s = [];\n'
                 'for (const a of actions) { const next = todos(Object.freeze(s), a); console.log(a.type, '
                 'next === s ? "=" : "≠", JSON.stringify(next)); s = next; }\n'
                 'const st = Object.freeze([Object.freeze({ id: 1, text: "a", done: false }), '
                 'Object.freeze({ id: 2, text: "b", done: false })]);\n'
                 'const t = todos(st, { type: "toggle", id: 1 });\n'
                 'console.log(t[1] === st[1], t[0] !== st[0], JSON.stringify(todos(undefined, { type: "init" '
                 '})));\n',
       'hint': 'Каждая ветка возвращает новый массив; для «ничего не изменилось» — тот же state.',
       'expected': ['add ≠ [{"id":1,"text":"молоко","done":false}]',
                    'add ≠ [{"id":1,"text":"молоко","done":false},{"id":2,"text":"хлеб","done":false}]',
                    'add ≠ '
                    '[{"id":1,"text":"молоко","done":false},{"id":2,"text":"хлеб","done":false},{"id":3,"text":"сыр","done":false}]',
                    'toggle ≠ '
                    '[{"id":1,"text":"молоко","done":false},{"id":2,"text":"хлеб","done":true},{"id":3,"text":"сыр","done":false}]',
                    'rename ≠ '
                    '[{"id":1,"text":"кефир","done":false},{"id":2,"text":"хлеб","done":true},{"id":3,"text":"сыр","done":false}]',
                    'toggle = '
                    '[{"id":1,"text":"кефир","done":false},{"id":2,"text":"хлеб","done":true},{"id":3,"text":"сыр","done":false}]',
                    'nope = '
                    '[{"id":1,"text":"кефир","done":false},{"id":2,"text":"хлеб","done":true},{"id":3,"text":"сыр","done":false}]',
                    'clearDone ≠ [{"id":1,"text":"кефир","done":false},{"id":3,"text":"сыр","done":false}]',
                    'remove ≠ [{"id":1,"text":"кефир","done":false}]',
                    'true true []']},
      {'id': 'j11-history',
       'mode': 'js',
       'title': 'История состояний: undo и redo',
       'statement': 'Напишите функцию createHistory(initial): возвращает объект с методами push(state) '
                    '(новое текущее; всё «будущее» отбрасывается), undo(), redo(), и геттеры present, '
                    'canUndo, canRedo. undo/redo на границе ничего не делают. Все состояния — неизменяемые '
                    'значения; повторный push того же значения (===) не создаёт новую запись.',
       'starter': 'function createHistory(initial) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const h = createHistory("a");\n'
                 'console.log(h.present, h.canUndo, h.canRedo);\n'
                 'h.push("b"); h.push("c"); h.push("c");\n'
                 'console.log(h.present, h.canUndo, h.canRedo);\n'
                 'h.undo(); console.log(h.present, h.canRedo);\n'
                 'h.undo(); h.undo(); console.log(h.present, h.canUndo);\n'
                 'h.redo(); h.redo(); console.log(h.present, h.canRedo);\n'
                 'h.undo(); h.push("x");\n'
                 'console.log(h.present, h.canRedo);\n'
                 'h.redo(); console.log(h.present);\n'
                 'h.undo(); h.undo(); h.undo(); console.log(h.present);\n',
       'hint': 'Три списка: прошлое, настоящее, будущее.',
       'expected': ['a false false', 'c true false', 'b true', 'a false', 'c false', 'x false', 'x', 'a']},
      {'id': 'j11-selector',
       'mode': 'js',
       'title': 'Мемоизированный селектор',
       'statement': 'Напишите функцию createSelector(inputSelectors, combiner) как в reselect: возвращает '
                    'селектор (state) → результат; combiner вызывается только если хотя бы одно из значений '
                    'inputSelectors(state) изменилось (по ===) с прошлого вызова; иначе возвращается прежний '
                    'результат. У селектора есть поле recomputations() — сколько раз вызывался combiner.',
       'starter': 'function createSelector(inputSelectors, combiner) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const items = (s) => s.items;\n'
                 'const filter = (s) => s.filter;\n'
                 'const visible = createSelector([items, filter], (it, f) => it.filter((x) => '
                 'x.includes(f)));\n'
                 'const s1 = { items: ["яблоко", "груша", "ананас"], filter: "я", other: 1 };\n'
                 'const r1 = visible(s1);\n'
                 'console.log(JSON.stringify(r1), visible.recomputations());\n'
                 'const s2 = { ...s1, other: 2 };\n'
                 'console.log(visible(s2) === r1, visible.recomputations());\n'
                 'const s3 = { ...s2, filter: "а" };\n'
                 'console.log(JSON.stringify(visible(s3)), visible.recomputations());\n'
                 'const s4 = { ...s3, items: [...s3.items, "арбуз"] };\n'
                 'console.log(JSON.stringify(visible(s4)), visible.recomputations());\n'
                 'console.log(visible(s4) === visible(s4), visible.recomputations());\n'
                 'const total = createSelector([(s) => s.price, (s) => s.qty], (p, q) => p * q);\n'
                 'console.log(total({ price: 5, qty: 3 }), total({ price: 5, qty: 3 }), '
                 'total.recomputations());\n',
       'hint': 'Запомните входные значения прошлого вызова и результат; сравните покомпонентно через ===.',
       'expected': ['["яблоко"] 1',
                    'true 1',
                    '["груша","ананас"] 2',
                    '["груша","ананас","арбуз"] 3',
                    'true 3',
                    '15 15 1']},
      {'id': 'j11-lazy-seq',
       'mode': 'js',
       'title': 'Ленивая последовательность',
       'statement': 'Напишите класс Seq: статические Seq.from(iterable), Seq.range(start, end?) (без end — '
                    'бесконечная), методы map(f), filter(p), take(n), takeWhile(p), drop(n), toArray(), '
                    'first(), reduce(f, init). Все преобразования ленивы: ничего не вычисляется до '
                    'toArray/first/reduce; каждый элемент проходит всю цепочку целиком (без промежуточных '
                    'массивов). Seq итерируем (Symbol.iterator).',
       'starter': 'class Seq {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let evaluated = 0;\n'
                 'const s = Seq.range(1).map((x) => { evaluated++; return x * x; }).filter((x) => x % 2 === '
                 '1);\n'
                 'console.log(evaluated);\n'
                 'console.log(JSON.stringify(s.take(4).toArray()), evaluated);\n'
                 'console.log(s.first(), JSON.stringify(Seq.range(0, 10).drop(7).toArray()), '
                 'JSON.stringify(Seq.range(1).takeWhile((x) => x < 5).toArray()));\n'
                 'console.log(Seq.from([1, 2, 3]).map((x) => x * 10).reduce((a, b) => a + b, 0), '
                 'JSON.stringify([...Seq.from("abc")]), Seq.range(5, 5).first());\n'
                 'console.log(JSON.stringify(Seq.range(1).drop(2).filter((x) => x % 3 === 0).map((x) => x + '
                 '0.5).take(3).toArray()));\n'
                 'console.log(JSON.stringify(Seq.range(0).take(0).toArray()));\n',
       'hint': 'Каждый метод возвращает новый Seq с генератором поверх предыдущего.',
       'expected': ['0',
                    '[1,9,25,49] 7',
                    '1 [7,8,9] [1,2,3,4]',
                    '60 ["a","b","c"] undefined',
                    '[3.5,6.5,9.5]',
                    '[]']},
      {'id': 'j11-iter-tools',
       'mode': 'js',
       'title': 'Инструменты для итераторов',
       'statement': 'Напишите генераторы: takeWhile(it, p), dropWhile(it, p), enumerate(it, start = 0) → '
                    'пары [индекс, значение], cycle(it) (бесконечно по кругу; пустой — пусто), range(start, '
                    'end, step = 1) (шаг может быть отрицательным), zip(...its) (до самого короткого).',
       'starter': 'function* takeWhile(it, p) {\n'
                  '}\n'
                  'function* dropWhile(it, p) {\n'
                  '}\n'
                  'function* enumerate(it, start = 0) {\n'
                  '}\n'
                  'function* cycle(it) {\n'
                  '}\n'
                  'function* range(start, end, step = 1) {\n'
                  '}\n'
                  'function* zip(...its) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const take = (n, it) => { const out = []; for (const x of it) { if (out.length >= n) '
                 'break; out.push(x); } return JSON.stringify(out); };\n'
                 'console.log(take(99, takeWhile([1, 2, 3, 1], (x) => x < 3)), take(99, dropWhile([1, 2, 3, '
                 '1], (x) => x < 3)));\n'
                 'console.log(take(99, enumerate("ab")), take(99, enumerate(["x"], 10)));\n'
                 'console.log(take(7, cycle([1, 2, 3])), take(5, cycle([])), take(5, cycle("ab")));\n'
                 'console.log(take(99, range(0, 10, 3)), take(99, range(5, 0, -2)), take(99, range(3, 3)), '
                 'take(3, range(0, Infinity)));\n'
                 'console.log(take(99, zip([1, 2, 3], "ab", [true, false, true])), take(99, zip()), take(99, '
                 'zip([1, 2])));\n'
                 'function* inf() { let i = 0; while (true) yield i++; }\n'
                 'console.log(take(3, zip(inf(), cycle(["a", "b"]))));\n',
       'hint': 'Генераторы с yield и yield*; zip берёт итераторы вручную через next().',
       'expected': ['[1,2] [3,1]',
                    '[[0,"a"],[1,"b"]] [[10,"x"]]',
                    '[1,2,3,1,2,3,1] [] ["a","b","a","b","a"]',
                    '[0,3,6,9] [5,3,1] [] [0,1,2]',
                    '[[1,"a",true],[2,"b",false]] [] [[1],[2]]',
                    '[[0,"a"],[1,"b"],[2,"a"]]']},
      {'id': 'j11-evolve',
       'mode': 'js',
       'title': 'evolve: преобразование полей объекта',
       'statement': 'Напишите функцию evolve(spec, obj): spec — объект «поле → функция» (или вложенный spec '
                    'для вложенных объектов); возвращает новый объект: у полей, которые есть в spec, '
                    'значение заменено результатом функции; остальные поля копируются как есть; поля из '
                    'spec, которых нет в obj, игнорируются. Исходный объект не меняется.',
       'starter': 'function evolve(spec, obj) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const user = Object.freeze({ name: " Ада ", age: 36, address: Object.freeze({ city: '
                 '"лондон", zip: 12345 }), tags: Object.freeze(["a"]) });\n'
                 'const r = evolve({ name: (s) => s.trim(), age: (n) => n + 1, address: { city: (s) => '
                 's[0].toUpperCase() + s.slice(1) }, missing: () => 1 }, user);\n'
                 'console.log(JSON.stringify(r));\n'
                 'console.log(r.tags === user.tags, r.address.zip, JSON.stringify(user.address));\n'
                 'console.log(JSON.stringify(evolve({}, { a: 1 })), JSON.stringify(evolve({ a: (x) => x * 2 '
                 '}, {})));\n',
       'hint': 'Для функции — применить; для объекта-спецификации — рекурсивный вызов evolve.',
       'expected': ['{"name":"Ада","age":37,"address":{"city":"Лондон","zip":12345},"tags":["a"]}',
                    'true 12345 {"city":"лондон","zip":12345}',
                    '{"a":1} {}']},
      {'id': 'j11-report',
       'mode': 'js',
       'title': 'Отчёт по заказам через конвейер',
       'statement': 'Заказы: { id, customer, items: [{ sku, price, qty }], status }. Напишите функцию '
                    'report(orders) → массив { customer, total, orders } по клиентам, где учитываются только '
                    'заказы со статусом «paid»; total — сумма price*qty по всем позициям; сортировка: по '
                    'убыванию total, при равенстве — по имени клиента; округлите total до копеек (два знака, '
                    'Math.round(x * 100) / 100). Используйте цепочку map/filter/reduce без изменения '
                    'исходных данных.',
       'starter': 'function report(orders) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const orders = Object.freeze([\n'
                 '  { id: 1, customer: "Борис", status: "paid", items: [{ sku: "a", price: 10.5, qty: 2 }, { '
                 'sku: "b", price: 0.1, qty: 3 }] },\n'
                 '  { id: 2, customer: "Анна", status: "paid", items: [{ sku: "c", price: 21.3, qty: 1 }] '
                 '},\n'
                 '  { id: 3, customer: "Борис", status: "cancelled", items: [{ sku: "a", price: 1000, qty: 1 '
                 '}] },\n'
                 '  { id: 4, customer: "Анна", status: "paid", items: [{ sku: "d", price: 0.2, qty: 1 }, { '
                 'sku: "e", price: 0.1, qty: 1 }] },\n'
                 '  { id: 5, customer: "Вера", status: "paid", items: [{ sku: "f", price: 21.6, qty: 1 }] '
                 '},\n'
                 '  { id: 6, customer: "Ёлка", status: "new", items: [] },\n'
                 ']);\n'
                 'for (const r of report(orders)) console.log(JSON.stringify(r));\n'
                 'console.log(JSON.stringify(report([])), orders.length);\n',
       'hint': 'Группировка в Map по клиенту, затем преобразование значений и сортировка.',
       'expected': ['{"customer":"Анна","total":21.6,"orders":2}',
                    '{"customer":"Вера","total":21.6,"orders":1}',
                    '{"customer":"Борис","total":21.3,"orders":1}',
                    '[] 6']},
      {'id': 'j11-match',
       'mode': 'js',
       'title': 'Сопоставление с образцом',
       'statement': 'Напишите функцию match(value, cases): cases — массив пар [образец, функция]; образец — '
                    'функция-предикат, примитивное значение (сравнивается через ===), объект-шаблон '
                    '(значение подходит, если у него есть все поля шаблона и они соответствуют вложенным '
                    'образцам) или match.any (всегда подходит). Возвращает результат функции первой '
                    'подошедшей пары, вызванной с value; если ничего не подошло — бросает Error("нет '
                    'подходящего образца").',
       'starter': 'function match(value, cases) {\n}\nmatch.any = Symbol("any");\n',
       'driver': '/*__DRIVER__*/\n'
                 'const area = (s) => match(s, [\n'
                 '  [{ type: "circle" }, (c) => +(Math.PI * c.r ** 2).toFixed(2)],\n'
                 '  [{ type: "rect", w: (w) => w > 0, h: (h) => h > 0 }, (r) => r.w * r.h],\n'
                 '  [{ type: "rect" }, () => 0],\n'
                 '  [match.any, () => "неизвестно"],\n'
                 ']);\n'
                 'console.log(area({ type: "circle", r: 2 }), area({ type: "rect", w: 3, h: 4 }), area({ '
                 'type: "rect", w: -1, h: 4 }), area({ type: "tri" }), area(5));\n'
                 'const fizz = (n) => match(n, [[(x) => x % 15 === 0, () => "FizzBuzz"], [(x) => x % 3 === '
                 '0, () => "Fizz"], [(x) => x % 5 === 0, () => "Buzz"], [match.any, String]]);\n'
                 'console.log([1, 3, 5, 15, 7].map(fizz).join());\n'
                 'console.log(match(0, [[0, () => "ноль"], [match.any, () => "иное"]]), match("a", [["a", '
                 '(v) => v + "!"]]), match({ a: { b: 1 } }, [[{ a: { b: 1 } }, () => "вложенный"]]));\n'
                 'try { match(42, [["x", () => 1]]); } catch (e) { console.log(e.message); }\n'
                 'console.log(match(null, [[{ a: 1 }, () => "объект"], [null, () => "null"]]));\n',
       'hint': 'Рекурсивная функция matches(pattern, value): предикат, объект-шаблон, примитив.',
       'expected': ['12.57 12 0 неизвестно неизвестно',
                    '1,Fizz,Buzz,FizzBuzz,7',
                    'ноль a! вложенный',
                    'нет подходящего образца',
                    'null']},
      {'id': 'j11-fix-mutation',
       'mode': 'js',
       'title': 'Исправьте: функция портит аргумент',
       'statement': 'Функция addItem(cart, item) должна вернуть новую корзину { items: [...], total } с '
                    'добавленным товаром и пересчитанной суммой, не меняя переданную cart. Сейчас она '
                    'изменяет cart на месте. Исправьте так, чтобы cart (даже замороженная) не менялась, а '
                    'нетронутые товары остались теми же объектами.',
       'starter': 'function addItem(cart, item) {\n'
                  '  cart.items.push(item);\n'
                  '  cart.total += item.price;\n'
                  '  return cart;\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 '"use strict";\n'
                 'const cart = Object.freeze({ items: Object.freeze([Object.freeze({ name: "хлеб", price: 40 '
                 '})]), total: 40, owner: "Ада" });\n'
                 'try {\n'
                 '  const c2 = addItem(cart, { name: "сыр", price: 300 });\n'
                 '  console.log(c2.items.length, c2.total, c2.owner, cart.items.length, cart.total, c2 !== '
                 'cart, c2.items[0] === cart.items[0]);\n'
                 '} catch (e) { console.log("ошибка:", e.name); }\n',
       'hint': 'Создайте новый объект: spread для полей, [...items, item] для массива.',
       'expected': ['2 340 Ада 1 40 true true']},
      {'id': 'j11-fix-impure',
       'mode': 'js',
       'title': 'Исправьте: нечистая функция',
       'statement': 'Функция makeTicket(user) использует Date.now() и Math.random() и поэтому '
                    'непредсказуема; а sortByAge(users) сортирует массив на месте. Перепишите: '
                    'makeTicket(user, now, random) → { id: `${user}-${now}-${Math.floor(random() * 1000)}`, '
                    'user }, sortByAge(users) → новый отсортированный по возрасту массив без изменения '
                    'исходного.',
       'starter': 'function makeTicket(user) {\n'
                  '  return { id: `${user}-${Date.now()}-${Math.floor(Math.random() * 1000)}`, user };\n'
                  '}\n'
                  'function sortByAge(users) {\n'
                  '  return users.sort((a, b) => a.age - b.age);\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(JSON.stringify(makeTicket("ада", 1700000000000, () => 0.5)));\n'
                 'console.log(JSON.stringify(makeTicket("ада", 1700000000000, () => 0.5)) === '
                 'JSON.stringify(makeTicket("ада", 1700000000000, () => 0.5)));\n'
                 'const users = Object.freeze([{ n: "b", age: 30 }, { n: "a", age: 20 }, { n: "c", age: 25 '
                 '}]);\n'
                 'console.log(JSON.stringify(sortByAge(users).map((u) => u.n)), JSON.stringify(users.map((u) '
                 '=> u.n)));\n',
       'hint': 'Время и случайность — параметрами; sort применяйте к копии.',
       'expected': ['{"id":"ада-1700000000000-500","user":"ада"}', 'true', '["a","c","b"] ["b","a","c"]']},
      {'id': 'j11-pipeline-text',
       'mode': 'js',
       'title': 'Конвейер обработки текста',
       'statement': 'Напишите функцию wordFrequency(text, n): чистый конвейер: привести к нижнему регистру, '
                    'разбить на слова (последовательности букв и цифр Юникода — /[\\p{L}\\p{N}]+/gu), убрать '
                    'стоп-слова из набора STOP = ["и", "в", "на", "не"], посчитать частоты, отсортировать по '
                    'убыванию частоты (при равенстве — по слову по алфавиту) и вернуть первые n пар [слово, '
                    'число].',
       'starter': 'function wordFrequency(text, n) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const t = "Кот и пёс. Кот на крыше, кот не спит! Пёс спит в будке; а КОТ — нет, пёс не '
                 'кот. Кошка и кот.";\n'
                 'console.log(JSON.stringify(wordFrequency(t, 3)));\n'
                 'console.log(JSON.stringify(wordFrequency(t, 100).slice(0, 8)));\n'
                 'console.log(JSON.stringify(wordFrequency("", 5)), JSON.stringify(wordFrequency("и в на '
                 'не", 5)), JSON.stringify(wordFrequency("a b a 1 1 1", 2)));\n',
       'hint': 'match → filter → reduce в Map → sort → slice.',
       'expected': ['[["кот",6],["пёс",3],["спит",2]]',
                    '[["кот",6],["пёс",3],["спит",2],["а",1],["будке",1],["кошка",1],["крыше",1],["нет",1]]',
                    '[] [] [["1",3],["a",2]]']},
      {'id': 'j11-stats',
       'mode': 'js',
       'title': 'Статистика без мутаций',
       'statement': 'Напишите чистую функцию stats(xs) для непустого массива чисел: { min, max, mean '
                    '(среднее, округлённое до 2 знаков), median (для чётного количества — среднее двух '
                    'средних), mode (наименьшее из самых частых значений) }. Для пустого массива верните '
                    'null. Исходный массив менять нельзя (в том числе сортировкой на месте).',
       'starter': 'function stats(xs) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const a = Object.freeze([5, 3, 9, 3, 1, 9, 7]);\n'
                 'console.log(JSON.stringify(stats(a)));\n'
                 'console.log(JSON.stringify(stats([4, 1, 3, 2])), JSON.stringify(stats([7])), '
                 'JSON.stringify(stats([])));\n'
                 'console.log(JSON.stringify(stats([1, 1, 2, 2, 3])), JSON.stringify(stats([-5, 0, 5, 10])), '
                 'JSON.stringify(stats([0.1, 0.2, 0.4])));\n'
                 'console.log(JSON.stringify(a));\n',
       'hint': 'Работайте с копией: [...xs].sort((a, b) => a - b); частоты — в Map.',
       'expected': ['{"min":1,"max":9,"mean":5.29,"median":5,"mode":3}',
                    '{"min":1,"max":4,"mean":2.5,"median":2.5,"mode":1} '
                    '{"min":7,"max":7,"mean":7,"median":7,"mode":7} null',
                    '{"min":1,"max":3,"mean":1.8,"median":2,"mode":1} '
                    '{"min":-5,"max":10,"mean":2.5,"median":2.5,"mode":-5} '
                    '{"min":0.1,"max":0.4,"mean":0.23,"median":0.2,"mode":0.1}',
                    '[5,3,9,3,1,9,7]']}]}
