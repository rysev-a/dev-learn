"""Задачи книги «Современный Frontend», глава 12 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {12: [{'id': 'j12-curry-placeholder',
       'mode': 'js',
       'title': 'Каррирование с заполнителем (как R.__)',
       'statement': 'Напишите функцию curryR(fn) и константу PH (заполнитель; любой уникальный объект). '
                    'Каррированная функция накапливает аргументы; место, занятое PH, считается «пропущенным» '
                    'и заполняется первым из следующих аргументов; fn вызывается, когда все fn.length '
                    'позиций заполнены. Например, curryR(sub)(PH, 10)(25) = sub(25, 10).',
       'starter': 'const PH = Symbol("placeholder");\nfunction curryR(fn) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sub = curryR((a, b) => a - b);\n'
                 'console.log(sub(10, 3), sub(10)(3), sub(PH, 3)(10), sub(PH)(3)(10), sub(PH, PH)(10, 3));\n'
                 'const f = curryR((a, b, c) => [a, b, c].join(""));\n'
                 'console.log(f("a")("b")("c"), f(PH, "b")("a")("c"), f(PH, PH, "c")("a", "b"), f(PH, "b", '
                 'PH)("a")("c"), f("a", PH, "c")("b"));\n'
                 'const half = curryR((a, b) => a / b)(PH, 2);\n'
                 'console.log(half(10), half(7));\n'
                 'console.log(typeof f(PH), typeof f("a", "b"));\n',
       'hint': 'Храните накопленные аргументы; при новом вызове сначала заполняйте дырки, затем добавляйте в '
               'конец.',
       'expected': ['7 7 7 -7 7', 'abc abc abc abc abc', '5 3.5', 'function function']},
      {'id': 'j12-assoc',
       'mode': 'js',
       'title': 'Ramda-подобные assoc, dissoc, path',
       'statement': 'Напишите неизменяемые функции в стиле Ramda (данные последними, без каррирования): '
                    'assoc(key, value, obj), assocPath(path, value, obj) (путь — массив; для числовых '
                    'ключей, если контейнера нет — создаётся массив, иначе объект), dissoc(key, obj), '
                    'dissocPath(path, obj), path(pathArr, obj), pathOr(def, pathArr, obj). Исходные данные '
                    'не меняются, нетронутые ветки не копируются.',
       'starter': 'function assoc(key, value, obj) {\n'
                  '}\n'
                  'function assocPath(path, value, obj) {\n'
                  '}\n'
                  'function dissoc(key, obj) {\n'
                  '}\n'
                  'function dissocPath(path, obj) {\n'
                  '}\n'
                  'function path(pathArr, obj) {\n'
                  '}\n'
                  'function pathOr(def, pathArr, obj) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const o = Object.freeze({ a: Object.freeze({ b: Object.freeze([1, Object.freeze({ c: 2 '
                 '})]) }), keep: Object.freeze({ k: 1 }) });\n'
                 'const s = (x) => console.log(JSON.stringify(x));\n'
                 's(assoc("x", 1, o).x); s(assoc(1, "z", ["a", "b"])); s(assoc("a", 5, { a: 1, b: 2 }));\n'
                 's(assocPath(["a", "b", 1, "c"], 99, o)); s(assocPath(["n", "m"], 1, {})); '
                 's(assocPath(["list", 0, "id"], 7, {}));\n'
                 'console.log(assocPath(["a", "b", 1, "c"], 99, o).keep === o.keep);\n'
                 's(dissoc("a", { a: 1, b: 2 })); s(dissoc(0, [1, 2, 3])); s(dissocPath(["a", "b", 1, "c"], '
                 'o)); s(dissocPath(["zzz", "q"], o) === o);\n'
                 's(path(["a", "b", 1, "c"], o)); s(path(["a", "x", "y"], o)); s(pathOr("нет", ["q"], o)); '
                 's(pathOr("нет", ["a", "b", 0], o));\n',
       'hint': 'Рекурсия по пути; для недостающего контейнера выбирайте массив, если следующий ключ — '
               'индекс.',
       'expected': ['1',
                    '["a","z"]',
                    '{"a":5,"b":2}',
                    '{"a":{"b":[1,{"c":99}]},"keep":{"k":1}}',
                    '{"n":{"m":1}}',
                    '{"list":[{"id":7}]}',
                    'true',
                    '{"b":2}',
                    '[2,3]',
                    '{"a":{"b":[1,{}]},"keep":{"k":1}}',
                    'true',
                    '2',
                    'undefined',
                    '"нет"',
                    '1']},
      {'id': 'j12-collections',
       'mode': 'js',
       'title': 'Утилиты коллекций (lodash-подобные)',
       'statement': 'Напишите функции: groupBy(f, xs) (объект ключ → массив), indexBy(f, xs) (ключ → '
                    'последний элемент), countBy(f, xs), partition(p, xs) → [подходящие, остальные], '
                    'uniqBy(f, xs) (первый по порядку), sortWith(comparators, xs) (новый массив; компараторы '
                    'по очереди), zipObj(keys, values), pickBy(p, obj) (p(value, key)), mapObj(f, obj) '
                    '(f(value, key)). Данные последними, исходные не меняются.',
       'starter': 'function groupBy(f, xs) {\n'
                  '}\n'
                  'function indexBy(f, xs) {\n'
                  '}\n'
                  'function countBy(f, xs) {\n'
                  '}\n'
                  'function partition(p, xs) {\n'
                  '}\n'
                  'function uniqBy(f, xs) {\n'
                  '}\n'
                  'function sortWith(comparators, xs) {\n'
                  '}\n'
                  'function zipObj(keys, values) {\n'
                  '}\n'
                  'function pickBy(p, obj) {\n'
                  '}\n'
                  'function mapObj(f, obj) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const people = Object.freeze([{ n: "Ада", age: 36, city: "Лондон" }, { n: "Борис", age: '
                 '25, city: "Москва" }, { n: "Вера", age: 36, city: "Лондон" }, { n: "Глеб", age: 25, city: '
                 '"Тверь" }]);\n'
                 'const s = (x) => console.log(JSON.stringify(x));\n'
                 's(groupBy((p) => p.city, people).Лондон.map((p) => p.n)); s(Object.keys(indexBy((p) => '
                 'p.age, people))); s(indexBy((p) => p.age, people)[36].n);\n'
                 's(countBy((p) => p.age, people)); s(partition((p) => p.age > 30, people).map((g) => '
                 'g.map((p) => p.n)));\n'
                 's(uniqBy((p) => p.age, people).map((p) => p.n));\n'
                 's(sortWith([(a, b) => b.age - a.age, (a, b) => a.n.localeCompare(b.n, "ru")], '
                 'people).map((p) => p.n));\n'
                 's(zipObj(["a", "b", "c"], [1, 2])); s(pickBy((v) => v > 1, { a: 1, b: 2, c: 3 })); '
                 's(mapObj((v, k) => k + v, { x: 1, y: 2 }));\n'
                 's(people.length);\n',
       'hint': 'Все функции — короткие свёртки; данные последним аргументом.',
       'expected': ['["Ада","Вера"]',
                    '["25","36"]',
                    '"Вера"',
                    '{"25":2,"36":2}',
                    '[["Ада","Вера"],["Борис","Глеб"]]',
                    '["Ада","Борис"]',
                    '["Ада","Вера","Борис","Глеб"]',
                    '{"a":1,"b":2}',
                    '{"b":2,"c":3}',
                    '{"x":"x1","y":"y2"}',
                    '4']},
      {'id': 'j12-lens-basic',
       'mode': 'js',
       'title': 'Линзы: lens, view, set, over',
       'statement': 'Напишите функции lens(getter, setter) (setter(value, whole) возвращает новую '
                    'структуру), view(l, whole), set(l, value, whole), over(l, fn, whole), а также '
                    'lensProp(key) и lensIndex(i) (неизменяемо: для массива возвращается копия). Линза — '
                    'объект { get, set }.',
       'starter': 'function lens(getter, setter) {\n'
                  '}\n'
                  'function view(l, whole) {\n'
                  '}\n'
                  'function set(l, value, whole) {\n'
                  '}\n'
                  'function over(l, fn, whole) {\n'
                  '}\n'
                  'function lensProp(key) {\n'
                  '}\n'
                  'function lensIndex(i) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const user = Object.freeze({ name: "Ада", age: 36, tags: Object.freeze(["a", "b", "c"]) '
                 '});\n'
                 'const age = lensProp("age"), tags = lensProp("tags"), second = lensIndex(1);\n'
                 'console.log(view(age, user), JSON.stringify(set(age, 40, user)), JSON.stringify(over(age, '
                 '(x) => x + 1, user)));\n'
                 'console.log(view(lens((u) => u.name.toUpperCase(), (v, u) => ({ ...u, name: v })), '
                 'user));\n'
                 'console.log(JSON.stringify(set(second, "Z", ["x", "y", "z"])), view(second, ["x", "y", '
                 '"z"]), view(lensIndex(9), ["x"]));\n'
                 'console.log(JSON.stringify(user), JSON.stringify(over(tags, (t) => t.map((x) => '
                 'x.toUpperCase()), user).tags));\n'
                 'console.log(set(age, 36, user) !== user, JSON.stringify(set(age, 36, user)) === '
                 'JSON.stringify(user));\n',
       'hint': 'lens(get, set) хранит две функции; over = set(fn(get(whole)), whole).',
       'expected': ['36 {"name":"Ада","age":40,"tags":["a","b","c"]} '
                    '{"name":"Ада","age":37,"tags":["a","b","c"]}',
                    'АДА',
                    '["x","Z","z"] y undefined',
                    '{"name":"Ада","age":36,"tags":["a","b","c"]} ["A","B","C"]',
                    'true true']},
      {'id': 'j12-lens-compose',
       'mode': 'js',
       'title': 'Композиция линз и lensPath',
       'statement': 'Напишите composeLenses(...lenses) (линзы слева направо: внешняя первой), lensPath(path) '
                    '(массив ключей/индексов; свойства создаются при записи; чтение недостающего — '
                    'undefined) и функцию modify(l, fn) → функция, применяющая over к структуре '
                    '(каррированная форма).',
       'starter': 'function composeLenses(...lenses) {\n'
                  '}\n'
                  'function lensPath(path) {\n'
                  '}\n'
                  'function modify(l, fn) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const s = Object.freeze({ user: Object.freeze({ address: Object.freeze({ city: "лондон" '
                 '}), tags: Object.freeze(["a", "b"]) }), other: Object.freeze({ x: 1 }) });\n'
                 'const city = lensPath(["user", "address", "city"]);\n'
                 'console.log(city.get(s), JSON.stringify(city.set("Париж", s)), city.set("Париж", s).other '
                 '=== s.other);\n'
                 'console.log(JSON.stringify(modify(city, (c) => c[0].toUpperCase() + '
                 'c.slice(1))(s).user.address));\n'
                 'const second = lensPath(["user", "tags", 1]);\n'
                 'console.log(second.get(s), JSON.stringify(second.set("B", s).user.tags), '
                 'Array.isArray(second.set("B", s).user.tags));\n'
                 'console.log(lensPath(["a", "b"]).get({}), JSON.stringify(lensPath(["a", "b"]).set(1, '
                 '{})));\n'
                 'const c2 = composeLenses(lensPath(["user"]), lensPath(["address"]), lensPath(["city"]));\n'
                 'console.log(c2.get(s), JSON.stringify(lensPath([]).set(5, s)), lensPath([]).get(s) === '
                 's);\n',
       'hint': 'Композиция: get идёт по цепочке, set — рекурсивно записывает внутренний результат во внешнюю '
               'часть.',
       'expected': ['лондон {"user":{"address":{"city":"Париж"},"tags":["a","b"]},"other":{"x":1}} true',
                    '{"city":"Лондон"}',
                    'b ["a","B"] true',
                    'undefined {"a":{"b":1}}',
                    'лондон 5 true']},
      {'id': 'j12-lens-laws',
       'mode': 'js',
       'title': 'Законы линз',
       'statement': 'Напишите функцию checkLensLaws(l, whole, value): возвращает { getSet, setGet, setSet }: '
                    'getSet — set(l, view(l, whole), whole) глубоко равно whole; setGet — view(l, set(l, '
                    'value, whole)) равно value; setSet — повторная запись второго значения поверх первой '
                    'даёт то же, что запись только второго (value1 = value, value2 = "второе" поверх value). '
                    'Линза — объект { get, set(value, whole) }. Сравнение через JSON.stringify.',
       'starter': 'function checkLensLaws(l, whole, value) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const prop = (k) => ({ get: (o) => o[k], set: (v, o) => ({ ...o, [k]: v }) });\n'
                 'const bad1 = { get: (o) => o.a, set: (v, o) => ({ ...o, a: v, touched: true }) };\n'
                 'const bad2 = { get: (o) => o.a, set: (v, o) => ({ ...o, a: String(v).toUpperCase() }) };\n'
                 'const nonEmpty = { get: (o) => o.a, set: (v, o) => ({ ...o, a: v, b: o.b + 1 }) };\n'
                 'for (const [name, l] of [["prop", prop("a")], ["bad1", bad1], ["bad2", bad2], ["counter", '
                 'nonEmpty]]) console.log(name, JSON.stringify(checkLensLaws(l, { a: "x", b: 0 }, '
                 '"значение")));\n',
       'hint': 'Три равенства, сравнение через JSON.stringify.',
       'expected': ['prop {"getSet":true,"setGet":true,"setSet":true}',
                    'bad1 {"getSet":false,"setGet":true,"setSet":true}',
                    'bad2 {"getSet":false,"setGet":false,"setSet":true}',
                    'counter {"getSet":false,"setGet":true,"setSet":false}']},
      {'id': 'j12-produce',
       'mode': 'js',
       'title': 'Мини-Immer: produce',
       'statement': 'Напишите функцию produce(base, recipe): recipe(draft) меняет черновик привычным '
                    'способом (присваивание свойств, delete, вложенные объекты, массивы: '
                    'push/pop/splice/индексы); produce возвращает новое значение: изменённые узлы '
                    'копируются, остальные остаются теми же ссылками; если изменений не было — возвращается '
                    'base. base не меняется (даже замороженный). Реализуйте через Proxy с копированием при '
                    'первой записи. Поддержите объекты и массивы.',
       'starter': 'function produce(base, recipe) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const base = Object.freeze({ user: Object.freeze({ name: "Ада", age: 36 }), items: '
                 'Object.freeze([Object.freeze({ id: 1 }), Object.freeze({ id: 2 })]), meta: Object.freeze({ '
                 'v: 1 }) });\n'
                 'const n1 = produce(base, (d) => { d.user.age++; d.items.push({ id: 3 }); });\n'
                 'console.log(JSON.stringify(n1), JSON.stringify(base));\n'
                 'console.log(n1.meta === base.meta, n1.items[0] === base.items[0], n1.user !== base.user, '
                 'n1 !== base);\n'
                 'console.log(produce(base, () => {}) === base, produce(base, (d) => { d.user.age = 36; }) '
                 '!== base);\n'
                 'const n2 = produce(base, (d) => { delete d.meta; d.items[1].id = 20; d.items.splice(0, 1); '
                 '});\n'
                 'console.log(JSON.stringify(n2));\n'
                 'const n3 = produce([1, 2, 3], (d) => { d[0] = 10; d.pop(); });\n'
                 'console.log(JSON.stringify(n3), Array.isArray(n3));\n'
                 'const n4 = produce({ a: { b: { c: 1 } }, x: { y: 1 } }, (d) => { d.a.b.c = 2; });\n'
                 'console.log(JSON.stringify(n4), n4.x === n4.x);\n'
                 'const n5 = produce({ list: [{ n: 1 }] }, (d) => { for (const it of d.list) it.n *= 10; '
                 'd.list.push({ n: 5 }); });\n'
                 'console.log(JSON.stringify(n5));\n',
       'hint': 'Proxy на каждый узел; при первой записи копируйте узел и всех его предков; в конце '
               'разверните черновики в обычные объекты.',
       'expected': ['{"user":{"name":"Ада","age":37},"items":[{"id":1},{"id":2},{"id":3}],"meta":{"v":1}} '
                    '{"user":{"name":"Ада","age":36},"items":[{"id":1},{"id":2}],"meta":{"v":1}}',
                    'true true true true',
                    'true false',
                    '{"user":{"name":"Ада","age":36},"items":[{"id":20}]}',
                    '[10,2] true',
                    '{"a":{"b":{"c":2}},"x":{"y":1}} true',
                    '{"list":[{"n":10},{"n":5}]}']},
      {'id': 'j12-patches',
       'mode': 'js',
       'title': 'Патчи: изменения и откат',
       'statement': 'Напишите функцию diffPatches(before, after) для JSON-подобных данных: возвращает массив '
                    'патчей { op: "add"|"replace"|"remove", path: [...], value? } (глубокое сравнение '
                    'объектов; массивы сравниваются поэлементно по индексам; порядок: по ключам по порядку '
                    'обхода before, затем добавленные ключи after) и applyPatches(base, patches) → новое '
                    'значение (неизменяемо). Должно выполняться applyPatches(a, diffPatches(a, b)) глубоко '
                    'равно b.',
       'starter': 'function diffPatches(before, after) {\n}\nfunction applyPatches(base, patches) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const a = Object.freeze({ name: "Ада", age: 36, tags: ["a", "b", "c"], addr: { city: '
                 '"Лондон", zip: 1 } });\n'
                 'const b = { name: "Ада", age: 37, tags: ["a", "x"], addr: { city: "Париж" }, role: "admin" '
                 '};\n'
                 'const patches = diffPatches(a, b);\n'
                 'for (const p of patches) console.log(JSON.stringify(p));\n'
                 'console.log(JSON.stringify(applyPatches(a, patches)) === JSON.stringify(b), '
                 'JSON.stringify(a.tags));\n'
                 'console.log(JSON.stringify(diffPatches({ x: 1 }, { x: 1 })), JSON.stringify(diffPatches(1, '
                 '2)), JSON.stringify(diffPatches([1], [1, 2])));\n'
                 'const back = applyPatches(b, diffPatches(b, a));\n'
                 'console.log(JSON.stringify(back) === JSON.stringify(a));\n',
       'hint': 'Сравнивайте рекурсивно; порядок удалений из массива — с конца, чтобы индексы не сдвигались.',
       'expected': ['{"op":"replace","path":["age"],"value":37}',
                    '{"op":"replace","path":["tags",1],"value":"x"}',
                    '{"op":"remove","path":["tags",2]}',
                    '{"op":"replace","path":["addr","city"],"value":"Париж"}',
                    '{"op":"remove","path":["addr","zip"]}',
                    '{"op":"add","path":["role"],"value":"admin"}',
                    'true ["a","b","c"]',
                    '[] [{"op":"replace","path":[],"value":2}] [{"op":"add","path":[1],"value":2}]',
                    'true']},
      {'id': 'j12-persistent-list',
       'mode': 'js',
       'title': 'Персистентный список',
       'statement': 'Напишите неизменяемый односвязный список: константа EMPTY и функции cons(head, tail), '
                    'head(list), tail(list), isEmpty(list), toArray(list), fromArray(arr), map(f, list), '
                    'concat(a, b) (общий хвост b: хвост результата === b), size(list). Операции не меняют '
                    'существующие списки; cons(x, list) делит list целиком.',
       'starter': 'const EMPTY = null;\nfunction cons(head, tail) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const a = fromArray([1, 2, 3]);\n'
                 'const b = cons(0, a);\n'
                 'console.log(JSON.stringify(toArray(a)), JSON.stringify(toArray(b)), tail(b) === a, '
                 'head(b), head(EMPTY), isEmpty(tail(tail(tail(a)))));\n'
                 'const c = concat(a, fromArray([4, 5]));\n'
                 'console.log(JSON.stringify(toArray(c)), JSON.stringify(toArray(a)), size(c), '
                 'size(EMPTY));\n'
                 'const tailB = fromArray([9]);\n'
                 'const joined = concat(a, tailB);\n'
                 'let last = joined; for (let i = 0; i < 3; i++) last = tail(last);\n'
                 'console.log(last === tailB, JSON.stringify(toArray(map((x) => x * 10, a))), '
                 'JSON.stringify(toArray(a)));\n'
                 'console.log(isEmpty(EMPTY), isEmpty(a), Object.isFrozen(a), '
                 'JSON.stringify(toArray(fromArray([]))));\n',
       'hint': 'Список — цепочка пар { head, tail } с общим концом EMPTY; concat пересобирает только первый '
               'список.',
       'expected': ['[1,2,3] [0,1,2,3] true 0 undefined true',
                    '[1,2,3,4,5] [1,2,3] 5 0',
                    'true [10,20,30] [1,2,3]',
                    'true false true []']},
      {'id': 'j12-persistent-map',
       'mode': 'js',
       'title': 'Персистентный словарь с общими частями',
       'statement': 'Напишите класс PMap — неизменяемый словарь на «корзинах»: фиксированное число корзин 8 '
                    '(индекс — хеш строки ключа по формуле сумма кодов символов % 8), в корзине — массив '
                    'пар. Методы set(k, v), delete(k) возвращают новый PMap, копируя только изменённую '
                    'корзину (остальные корзины — те же ссылки); get(k), has(k), size, toObject() (ключи по '
                    'алфавиту), buckets (массив корзин для проверки разделения). Исходный не меняется.',
       'starter': 'class PMap {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const m0 = new PMap();\n'
                 'const m1 = m0.set("a", 1).set("b", 2).set("c", 3);\n'
                 'const m2 = m1.set("b", 20);\n'
                 'console.log(m0.size, m1.size, m2.size, m1.get("b"), m2.get("b"), m1.get("zzz"), '
                 'm1.has("a"), m1.has("q"));\n'
                 'const changed = m1.buckets.map((b, i) => (b === m2.buckets[i] ? 0 : 1)).reduce((a, b) => a '
                 '+ b, 0);\n'
                 'console.log(changed, JSON.stringify(m2.toObject()), JSON.stringify(m1.toObject()));\n'
                 'const m3 = m2.delete("a");\n'
                 'console.log(m3.size, m3.has("a"), m2.has("a"), m3.delete("не было") === m3);\n'
                 'const keys = ["x", "yy", "zzz", "ключ", "k1", "k2", "k3", "k4"];\n'
                 'const big = keys.reduce((m, k, i) => m.set(k, i), new PMap());\n'
                 'console.log(big.size, JSON.stringify(big.toObject()));\n'
                 'console.log(m1.set("a", 1).buckets.filter((b, i) => b === m1.buckets[i]).length >= 7);\n',
       'hint': 'Копируется только корзина с изменённым ключом, остальные переиспользуются.',
       'expected': ['0 3 3 2 20 undefined true false',
                    '1 {"a":1,"b":20,"c":3} {"a":1,"b":2,"c":3}',
                    '2 false true true',
                    '8 {"k1":4,"k2":5,"k3":6,"k4":7,"x":0,"yy":1,"zzz":2,"ключ":3}',
                    'true']},
      {'id': 'j12-queue',
       'mode': 'js',
       'title': 'Персистентная очередь',
       'statement': 'Напишите неизменяемую очередь на двух списках (вход и выход): функции emptyQueue(), '
                    'enqueue(q, x), dequeue(q) → { value, queue } (для пустой — { value: undefined, queue: q '
                    '}), peek(q), sizeOf(q), toArray(q) (от головы к хвосту). Старые версии очереди остаются '
                    'рабочими; amortized O(1): переворот входа в выход — только когда выход пуст.',
       'starter': 'function emptyQueue() {\n'
                  '}\n'
                  'function enqueue(q, x) {\n'
                  '}\n'
                  'function dequeue(q) {\n'
                  '}\n'
                  'function peek(q) {\n'
                  '}\n'
                  'function sizeOf(q) {\n'
                  '}\n'
                  'function toArray(q) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let q0 = emptyQueue();\n'
                 'const q1 = enqueue(enqueue(enqueue(q0, "a"), "b"), "c");\n'
                 'console.log(sizeOf(q0), sizeOf(q1), JSON.stringify(toArray(q1)), peek(q1), peek(q0));\n'
                 'const d1 = dequeue(q1);\n'
                 'console.log(d1.value, JSON.stringify(toArray(d1.queue)), JSON.stringify(toArray(q1)));\n'
                 'const q2 = enqueue(d1.queue, "d");\n'
                 'const d2 = dequeue(d1.queue), d3 = dequeue(d2.queue), d4 = dequeue(d3.queue);\n'
                 'console.log(d2.value, d3.value, d4.value, sizeOf(d4.queue), JSON.stringify(toArray(q2)));\n'
                 'const e = dequeue(q0);\n'
                 'console.log(e.value, e.queue === q0, JSON.stringify(toArray(q1)));\n'
                 'let q = emptyQueue();\n'
                 'for (let i = 1; i <= 5; i++) q = enqueue(q, i);\n'
                 'const out = [];\n'
                 'for (let i = 0; i < 3; i++) { const r = dequeue(q); out.push(r.value); q = '
                 'enqueue(r.queue, i + 10); }\n'
                 'console.log(JSON.stringify(out), JSON.stringify(toArray(q)));\n',
       'hint': 'Два списка; dequeue берёт из выхода, а при пустом выходе разворачивает вход.',
       'expected': ['0 3 ["a","b","c"] a undefined',
                    'a ["b","c"] ["a","b","c"]',
                    'b c undefined 0 ["b","c","d"]',
                    'undefined true ["a","b","c"]',
                    '[1,2,3] [4,5,10,11,12]']},
      {'id': 'j12-task',
       'mode': 'js',
       'title': 'Task: ленивая асинхронность',
       'statement': 'Напишите функцию Task(computation) — computation(reject, resolve) вызывается только при '
                    'fork(onError, onSuccess). Методы: map(f), chain(f) (f возвращает Task), mapError(f), '
                    'fork. Статические Task.of(v), Task.rejected(e), Task.all(tasks) (параллельно, '
                    'результаты в порядке задач; первая ошибка — ошибка итога) и fromPromise(fn) (fn — '
                    'функция, возвращающая промис, вызывается при fork). Любой Task можно запускать повторно '
                    '— каждый раз заново.',
       'starter': 'function Task(computation) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const sleep = (ms, v) => new Promise((r) => setTimeout(() => r(v), ms));\n'
                 'let started = 0;\n'
                 'const t = Task((rej, res) => { started++; setTimeout(() => res(21), 5); });\n'
                 'const doubled = t.map((x) => x * 2);\n'
                 'console.log(started);\n'
                 'const run = (task) => new Promise((r) => task.fork((e) => r("ошибка " + e), (v) => '
                 'r("успех " + JSON.stringify(v))));\n'
                 'console.log(await run(doubled), started);\n'
                 'console.log(await run(doubled), started);\n'
                 'console.log(await run(Task.of(2).chain((x) => Task.of(x + 1)).map((x) => x * 10)));\n'
                 'console.log(await run(Task.of(1).chain(() => Task.rejected("сбой")).map((x) => x + 1)));\n'
                 'console.log(await run(Task.rejected("e").mapError((e) => e.toUpperCase())));\n'
                 'console.log(await run(Task.all([Task.fromPromise(() => sleep(20, "a")), Task.of("b"), '
                 'Task.fromPromise(() => sleep(5, "c"))])));\n'
                 'console.log(await run(Task.all([Task.fromPromise(() => sleep(20, "a")), '
                 'Task.rejected("упал")])), await run(Task.all([])));\n'
                 'let calls = 0;\n'
                 'const lazy = Task.fromPromise(() => { calls++; return Promise.resolve(1); });\n'
                 'console.log(calls);\n'
                 'await run(lazy); await run(lazy);\n'
                 'console.log(calls);\n',
       'hint': 'Task — обёртка над функцией; всё запускается только в fork.',
       'expected': ['0',
                    'успех 42 1',
                    'успех 42 2',
                    'успех 30',
                    'ошибка сбой',
                    'ошибка E',
                    'успех ["a","b","c"]',
                    'ошибка упал успех []',
                    '0',
                    '2']},
      {'id': 'j12-reader',
       'mode': 'js',
       'title': 'Reader: зависимости как параметр',
       'statement': 'Напишите функцию Reader(run) — run(env) возвращает значение; методы map(f), chain(f) (f '
                    'возвращает Reader), local(fn) (меняет окружение перед вызовом: '
                    'Reader.local(fn).run(env) = run(fn(env))), run(env). Статические Reader.of(v), '
                    'Reader.ask() (возвращает окружение). Обычная проверка: логика не знает, откуда берётся '
                    'конфиг.',
       'starter': 'function Reader(run) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const greeting = Reader((env) => env.greeting);\n'
                 'const greet = (name) => greeting.map((g) => `${g}, ${name}!`);\n'
                 'console.log(greet("Ада").run({ greeting: "Привет" }), greet("Б").run({ greeting: '
                 '"Здравствуйте" }));\n'
                 'const program = Reader.ask().chain((env) => Reader.of(env.items).map((xs) => xs.filter((x) '
                 '=> x > env.min)));\n'
                 'console.log(JSON.stringify(program.run({ items: [1, 5, 10], min: 3 })));\n'
                 'const logger = Reader((env) => (msg) => env.log.push(msg));\n'
                 'const work = logger.chain((log) => Reader.of(null).map(() => { log("старт"); log("конец"); '
                 'return "готово"; }));\n'
                 'const env = { log: [] };\n'
                 'console.log(work.run(env), env.log.join());\n'
                 'const nested = Reader((e) => e.db.url).local((e) => ({ db: { url: e.url + "/test" } }));\n'
                 'console.log(nested.run({ url: "pg://x" }));\n'
                 'console.log(Reader.of(5).map((x) => x * 2).run(), Reader.ask().run(42));\n',
       'hint': 'run(env) проходит окружение через всю цепочку.',
       'expected': ['Привет, Ада! Здравствуйте, Б!', '[5,10]', 'готово старт,конец', 'pg://x/test', '10 42']},
      {'id': 'j12-validation',
       'mode': 'js',
       'title': 'Validation: накопление ошибок',
       'statement': 'Напишите Success(value) и Failure(errors) (errors — массив) и функцию validate(form, '
                    'rules): rules — объект поле → массив проверок (value) → строка-ошибка или null; для '
                    'каждого поля все проверки выполняются (ошибки поля собираются), ошибки всех полей '
                    'объединяются в один массив в порядке полей, без повторов (по тексту). Возвращает '
                    'Success(form) если ошибок нет, иначе Failure(массив строк вида «поле: ошибка»). У '
                    'значений есть методы map(f) (для Success), fold(onFailure, onSuccess) и toString().',
       'starter': 'function Success(value) {\n'
                  '}\n'
                  'function Failure(errors) {\n'
                  '}\n'
                  'function validate(form, rules) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const required = (v) => (v === undefined || v === "" ? "обязательно" : null);\n'
                 'const minLen = (n) => (v) => (typeof v === "string" && v.length < n ? `минимум ${n} '
                 'символов` : null);\n'
                 'const isEmail = (v) => (typeof v === "string" && !/^[^@\\s]+@[^@\\s]+$/.test(v) ? '
                 '"неверный e-mail" : null);\n'
                 'const rules = { name: [required, minLen(3)], email: [required, isEmail], pass: [minLen(6), '
                 'minLen(6)] };\n'
                 'console.log(String(validate({ name: "Ада", email: "ada@x.ru", pass: "123456" }, rules)));\n'
                 'console.log(String(validate({ name: "", email: "bad", pass: "1" }, rules)));\n'
                 'console.log(String(validate({ name: "Борис", email: "", pass: "123456" }, rules)));\n'
                 'console.log(validate({ name: "Ок", email: "a@b", pass: "123456" }, rules).fold((e) => '
                 'e.length + " ошибок", () => "ок"));\n'
                 'console.log(String(validate({ name: "Вера", email: "v@x", pass: "abcdef" }, rules).map((f) '
                 '=> f.name.toUpperCase())));\n'
                 'console.log(String(validate({}, {})));\n',
       'hint': 'Проверки каждого поля — в массиве; ошибки добавляйте, если их ещё нет.',
       'expected': ['Success({"name":"Ада","email":"ada@x.ru","pass":"123456"})',
                    'Failure(["name: обязательно","name: минимум 3 символов","email: неверный e-mail","pass: '
                    'минимум 6 символов"])',
                    'Failure(["email: обязательно","email: неверный e-mail"])',
                    '1 ошибок',
                    'Success("ВЕРА")',
                    'Success({})']},
      {'id': 'j12-traverse',
       'mode': 'js',
       'title': 'sequence и traverse для Maybe и Either',
       'statement': 'Даны Maybe-значения как объекты { tag: "just", value } / { tag: "nothing" } и Either: { '
                    'tag: "right", value } / { tag: "left", error }. Напишите sequenceMaybe(list) (все Just '
                    '→ Just(массив значений), иначе Nothing), traverseMaybe(f, xs) (f возвращает Maybe), '
                    'sequenceEither(list) (первый Left или Right(массив)), traverseEither(f, xs). Фабрики '
                    'Just/Nothing/Right/Left определите сами.',
       'starter': 'const Just = null;\nconst Nothing = null;\nconst Right = null;\nconst Left = null;\n',
       'driver': '/*__DRIVER__*/\n'
                 'const s = (x) => console.log(JSON.stringify(x));\n'
                 's(sequenceMaybe([Just(1), Just(2)])); s(sequenceMaybe([Just(1), Nothing(), Just(3)])); '
                 's(sequenceMaybe([]));\n'
                 'const parse = (str) => (/^\\d+$/.test(str) ? Just(+str) : Nothing());\n'
                 's(traverseMaybe(parse, ["1", "22", "333"])); s(traverseMaybe(parse, ["1", "x"]));\n'
                 's(sequenceEither([Right("a"), Right("b")])); s(sequenceEither([Right("a"), Left("e1"), '
                 'Left("e2")])); s(sequenceEither([]));\n'
                 'let calls = 0;\n'
                 'const num = (str) => { calls++; return /^\\d+$/.test(str) ? Right(+str) : Left("не число: '
                 '" + str); };\n'
                 's(traverseEither(num, ["1", "2", "x", "4"])); s(calls);\n'
                 's(traverseEither(num, []));\n',
       'hint': 'Обход слева направо с остановкой на первом Nothing/Left.',
       'expected': ['{"tag":"just","value":[1,2]}',
                    '{"tag":"nothing"}',
                    '{"tag":"just","value":[]}',
                    '{"tag":"just","value":[1,22,333]}',
                    '{"tag":"nothing"}',
                    '{"tag":"right","value":["a","b"]}',
                    '{"tag":"left","error":"e1"}',
                    '{"tag":"right","value":[]}',
                    '{"tag":"left","error":"не число: x"}',
                    '3',
                    '{"tag":"right","value":[]}']},
      {'id': 'j12-transducers',
       'mode': 'js',
       'title': 'Трансдьюсеры: map, filter, take',
       'statement': 'Напишите трансдьюсеры mapT(f), filterT(p), takeT(n) (останавливает обход после n '
                    'элементов — нужен признак «завершено»: редьюсер может вернуть объект { reduced: value '
                    '}), и функции compose(...fns) (слева направо по преобразованию данных: первый '
                    'применяется первым), transduce(xf, step, init, coll) (останавливается, как только '
                    'получен reduced) и into(init, xf, coll) для массива-приёмника (push-подобный редьюсер, '
                    'копирует).',
       'starter': 'function mapT(f) {\n'
                  '}\n'
                  'function filterT(p) {\n'
                  '}\n'
                  'function takeT(n) {\n'
                  '}\n'
                  'function compose(...fns) {\n'
                  '}\n'
                  'function transduce(xf, step, init, coll) {\n'
                  '}\n'
                  'function into(init, xf, coll) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let seen = 0;\n'
                 'function* source() { for (let i = 1; i <= 100; i++) { seen++; yield i; } }\n'
                 'const xf = compose(mapT((x) => x * x), filterT((x) => x % 2 === 1), takeT(4));\n'
                 'console.log(JSON.stringify(into([], xf, source())), seen);\n'
                 'console.log(JSON.stringify(into([], compose(mapT((x) => x + 1)), [1, 2, 3])), '
                 'JSON.stringify(into(["start"], filterT((x) => x > 1), [1, 2, 3])));\n'
                 'console.log(transduce(compose(filterT((c) => c !== " "), mapT((c) => c.toUpperCase())), '
                 '(s, c) => s + c, "", "a b c"));\n'
                 'console.log(transduce(takeT(2), (a, b) => a + b, 0, [10, 20, 30]), JSON.stringify(into([], '
                 'takeT(0), [1, 2])), JSON.stringify(into([], takeT(10), [1, 2])));\n'
                 'console.log(transduce(compose(mapT((x) => x * 2)), (a, b) => a + b, 0, new Set([1, 2, '
                 '3])));\n',
       'hint': 'Трансдьюсер: (step) => (acc, x) => …; для take возвращайте { reduced } после n элементов.',
       'expected': ['[1,9,25,49] 7', '[2,3,4] ["start",2,3]', 'ABC', '30 [] [1,2]', '12']},
      {'id': 'j12-observable-basic',
       'mode': 'js',
       'title': 'Мини-RxJS: Observable, map, filter, take',
       'statement': 'Напишите класс Observable(subscribeFn): subscribeFn(observer) вызывает '
                    'observer.next/error/complete и возвращает функцию отписки (необязательно); метод '
                    'subscribe(observer | функция next) → { unsubscribe() } (после unsubscribe или '
                    'complete/error значения больше не приходят, а функция отписки из subscribeFn вызывается '
                    'один раз); pipe(...operators); статические of(...values), from(iterable); операторы '
                    'map, filter, take(n) (после n значений — complete и отписка от источника), '
                    'toArray(observable) → промис.',
       'starter': 'class Observable {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const log = [];\n'
                 'Observable.of(1, 2, 3).pipe(map((x) => x * 10)).subscribe({ next: (v) => log.push(v), '
                 'complete: () => log.push("конец") });\n'
                 'console.log(log.join());\n'
                 'console.log(JSON.stringify(await toArray(Observable.from([1, 2, 3, 4, 5, '
                 '6]).pipe(filter((x) => x % 2 === 0), map((x) => x * x), take(2)))));\n'
                 'let torn = 0, produced = 0;\n'
                 'const timer = new Observable((o) => { const id = setInterval(() => { produced++; '
                 'o.next(produced); }, 5); return () => { torn++; clearInterval(id); }; });\n'
                 'const got = await toArray(timer.pipe(take(3)));\n'
                 'await new Promise((r) => setTimeout(r, 40));\n'
                 'console.log(JSON.stringify(got), torn, produced);\n'
                 'const seen = [];\n'
                 'const sub = timer.subscribe((v) => seen.push(v));\n'
                 'await new Promise((r) => setTimeout(r, 22));\n'
                 'sub.unsubscribe(); sub.unsubscribe();\n'
                 'const n = seen.length;\n'
                 'await new Promise((r) => setTimeout(r, 30));\n'
                 'console.log(n >= 3, seen.length === n, torn);\n'
                 'const errs = [];\n'
                 'new Observable((o) => { o.next(1); o.error(new Error("упал")); o.next(2); }).subscribe({ '
                 'next: (v) => errs.push(v), error: (e) => errs.push(e.message) });\n'
                 'console.log(errs.join());\n',
       'hint': 'Оператор — функция Observable → Observable; отписка возвращается из subscribeFn и вызывается '
               'один раз.',
       'expected': ['10,20,30,конец', '[4,16]', '[1,2,3] 1 3', 'true true 2', '1,упал']},
      {'id': 'j12-rx-scan',
       'mode': 'js',
       'title': 'Операторы scan, distinctUntilChanged, startWith',
       'statement': 'Дан Observable из задачи про мини-RxJS (класс уже определён в тестовом окружении как '
                    'Observable; операторы пишутся функциями Observable → Observable через new Observable). '
                    'Напишите операторы scan(f, seed) (накопление), distinctUntilChanged(eq = (a, b) => a '
                    '=== b), startWith(...values), pairwise() (пары соседних значений), tap(fn). Ошибки и '
                    'завершение пробрасываются; отписка — вниз по цепочке.',
       'starter': 'const scan = null;\n'
                  'const distinctUntilChanged = null;\n'
                  'const startWith = null;\n'
                  'const pairwise = null;\n'
                  'const tap = null;\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'const collect = (obs) => { const out = []; let done = false; obs.subscribe({ next: (v) => '
                 'out.push(v), complete: () => { done = true; } }); return JSON.stringify(out) + (done ? " '
                 '✓" : ""); };\n'
                 'const src = (...v) => Observable.of(...v);\n'
                 'console.log(collect(src(1, 2, 3, 4).pipe(scan((a, b) => a + b, 0))));\n'
                 'console.log(collect(src(1, 1, 2, 2, 2, 3, 1).pipe(distinctUntilChanged())));\n'
                 'console.log(collect(src({ id: 1 }, { id: 1 }, { id: 2 }).pipe(distinctUntilChanged((a, b) '
                 '=> a.id === b.id))));\n'
                 'console.log(collect(src("a", "b").pipe(startWith("s0", "s1"))));\n'
                 'console.log(collect(src(1, 2, 3, 4).pipe(pairwise())), collect(src(1).pipe(pairwise())));\n'
                 'const seen = [];\n'
                 'console.log(collect(src(5, 6).pipe(tap((v) => seen.push("tap" + v)), scan((a, b) => a * b, '
                 '1))), seen.join());\n'
                 'console.log(collect(src().pipe(startWith(0), scan((a, b) => a + b, 100))));\n',
       'hint': 'Каждый оператор — new Observable, подписывающийся на источник и возвращающий его '
               'unsubscribe.',
       'expected': ['[1,3,6,10] ✓',
                    '[1,2,3,1] ✓',
                    '[{"id":1},{"id":2}] ✓',
                    '["s0","s1","a","b"] ✓',
                    '[[1,2],[2,3],[3,4]] ✓ [] ✓',
                    '[5,30] ✓ tap5,tap6',
                    '[100] ✓']},
      {'id': 'j12-debounce-time',
       'mode': 'js',
       'title': 'debounceTime на виртуальном времени',
       'statement': 'Время вынесено в планировщик: scheduler = { setTimeout(fn, ms) → id, clearTimeout(id) '
                    '}. Напишите функцию debounceTime(ms, scheduler) → оператор (Observable → Observable): '
                    'значение выдаётся, если за ms миллисекунд не пришло новое; при завершении источника '
                    'последнее ожидающее значение выдаётся сразу, затем complete; отписка отменяет таймер. '
                    'Класс Observable (как в предыдущих задачах) уже определён.',
       'starter': 'function debounceTime(ms, scheduler) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'function makeScheduler() {\n'
                 '  let now = 0, nextId = 1;\n'
                 '  const timers = new Map();\n'
                 '  return {\n'
                 '    setTimeout(fn, ms) { const id = nextId++; timers.set(id, { at: now + ms, fn }); return '
                 'id; },\n'
                 '    clearTimeout(id) { timers.delete(id); },\n'
                 '    advance(ms) {\n'
                 '      const end = now + ms;\n'
                 '      for (;;) {\n'
                 '        const due = [...timers].filter(([, t]) => t.at <= end).sort((a, b) => a[1].at - '
                 'b[1].at || a[0] - b[0])[0];\n'
                 '        if (!due) break;\n'
                 '        timers.delete(due[0]); now = due[1].at; due[1].fn();\n'
                 '      }\n'
                 '      now = end;\n'
                 '    },\n'
                 '    pending: () => timers.size,\n'
                 '  };\n'
                 '}\n'
                 'const sch = makeScheduler();\n'
                 'let emit, finish;\n'
                 'const source = new Observable((o) => { emit = (v) => o.next(v); finish = () => '
                 'o.complete(); });\n'
                 'const out = [];\n'
                 'const sub = source.pipe(debounceTime(100, sch)).subscribe({ next: (v) => out.push(v), '
                 'complete: () => out.push("конец") });\n'
                 'emit("п"); sch.advance(50); emit("по"); sch.advance(50); emit("пои"); sch.advance(99);\n'
                 'console.log(JSON.stringify(out), sch.pending());\n'
                 'sch.advance(1);\n'
                 'console.log(JSON.stringify(out));\n'
                 'emit("поис"); sch.advance(100); emit("поиск"); finish();\n'
                 'console.log(JSON.stringify(out), sch.pending());\n'
                 'const s2 = makeScheduler();\n'
                 'let e2;\n'
                 'const o2 = new Observable((o) => { e2 = (v) => o.next(v); });\n'
                 'const got = [];\n'
                 'const sb = o2.pipe(debounceTime(10, s2)).subscribe((v) => got.push(v));\n'
                 'e2(1); sb.unsubscribe(); s2.advance(100);\n'
                 'console.log(JSON.stringify(got), s2.pending());\n',
       'hint': 'Один отложенный таймер: при каждом значении отменяйте предыдущий и ставьте новый.',
       'expected': ['[] 1', '["пои"]', '["пои","поис","поиск","конец"] 0', '[] 0']},
      {'id': 'j12-switchmap',
       'mode': 'js',
       'title': 'switchMap и mergeMap',
       'statement': 'Напишите операторы switchMap(project) (новое внешнее значение отписывается от '
                    'предыдущего внутреннего потока и запускает новый; complete — когда внешний завершился и '
                    'внутренний тоже) и mergeMap(project) (все внутренние потоки параллельно; complete — '
                    'когда завершились внешний и все внутренние). project(v) возвращает Observable. Класс '
                    'Observable (как в предыдущих задачах) определён; ошибки пробрасываются.',
       'starter': 'const switchMap = null;\nconst mergeMap = null;\n',
       'driver': '/*__DRIVER__*/\n'
                 'const later = (v, ms) => new Observable((o) => { const id = setTimeout(() => { o.next(v); '
                 'o.complete(); }, ms); return () => clearTimeout(id); });\n'
                 'const manual = () => { let o; const obs = new Observable((x) => { o = x; }); return { obs, '
                 'next: (v) => o.next(v), complete: () => o.complete() }; };\n'
                 'const collect = (o) => { const out = []; return { out, sub: o.subscribe({ next: (v) => '
                 'out.push(v), complete: () => out.push("конец"), error: (e) => out.push("ошибка " + e) }) '
                 '}; };\n'
                 '{\n'
                 '  const outer = manual();\n'
                 '  const { out } = collect(outer.obs.pipe(switchMap((q) => later("результат " + q, q.length '
                 '=== 1 ? 30 : 10))));\n'
                 '  outer.next("a"); await new Promise((r) => setTimeout(r, 5)); outer.next("ab"); await new '
                 'Promise((r) => setTimeout(r, 60));\n'
                 '  outer.complete();\n'
                 '  console.log(out.join(" | "));\n'
                 '}\n'
                 '{\n'
                 '  const outer = manual();\n'
                 '  const { out } = collect(outer.obs.pipe(mergeMap((q) => later("результат " + q, q === "a" '
                 '? 30 : 10))));\n'
                 '  outer.next("a"); outer.next("b"); outer.complete();\n'
                 '  console.log(out.length);\n'
                 '  await new Promise((r) => setTimeout(r, 60));\n'
                 '  console.log(out.join(" | "));\n'
                 '}\n'
                 '{\n'
                 '  let torn = 0;\n'
                 '  const outer = manual();\n'
                 '  const never = new Observable(() => () => { torn++; });\n'
                 '  const { sub } = collect(outer.obs.pipe(switchMap(() => never)));\n'
                 '  outer.next(1); outer.next(2); outer.next(3);\n'
                 '  console.log(torn);\n'
                 '  sub.unsubscribe();\n'
                 '  console.log(torn);\n'
                 '}\n'
                 '{\n'
                 '  const { out } = collect(new Observable((o) => { o.next(1); o.complete(); '
                 '}).pipe(switchMap((x) => new Observable((o) => { o.next(x * 10); o.error("упал"); }))));\n'
                 '  console.log(out.join(" | "));\n'
                 '}\n',
       'hint': 'Следите за счётчиком активных внутренних потоков и флагом завершения внешнего; отписка '
               'закрывает всё.',
       'expected': ['результат ab | конец',
                    '0',
                    'результат b | результат a | конец',
                    '2',
                    '3',
                    '10 | ошибка упал']},
      {'id': 'j12-combine-latest',
       'mode': 'js',
       'title': 'combineLatest, merge и Subject',
       'statement': 'Напишите: Subject (наследник Observable: next(v), error(e), complete(); несколько '
                    'подписчиков получают значения; после complete новые подписчики сразу получают '
                    'complete), combineLatest(...observables) (выдаёт массив последних значений, когда у '
                    'каждого есть хотя бы одно; complete — когда завершились все), merge(...observables) '
                    '(значения по мере прихода; complete, когда все). Класс Observable определён.',
       'starter': 'class Subject {\n'
                  '}\n'
                  'function combineLatest(...observables) {\n'
                  '}\n'
                  'function merge(...observables) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'const rec = (o) => { const out = []; const sub = o.subscribe({ next: (v) => '
                 'out.push(JSON.stringify(v)), complete: () => out.push("✓") }); return { out, sub }; };\n'
                 'const s = new Subject();\n'
                 'const a = rec(s), b = rec(s);\n'
                 's.next(1); b.sub.unsubscribe(); s.next(2);\n'
                 'console.log(a.out.join(" "), "|", b.out.join(" "));\n'
                 's.complete();\n'
                 'console.log(a.out.join(" "), rec(s).out.join(" "));\n'
                 'const price = new Subject(), qty = new Subject();\n'
                 'const c = rec(combineLatest(price, qty));\n'
                 'price.next(10); price.next(20);\n'
                 'console.log(c.out.length);\n'
                 'qty.next(2); price.next(30); qty.next(3);\n'
                 'console.log(c.out.join(" "));\n'
                 'price.complete(); console.log(c.out.at(-1)); qty.complete(); console.log(c.out.at(-1));\n'
                 'const x = new Subject(), y = new Subject();\n'
                 'const m = rec(merge(x, y));\n'
                 'x.next("x1"); y.next("y1"); x.next("x2"); x.complete(); y.next("y2"); y.complete();\n'
                 'console.log(m.out.join(" "));\n'
                 'console.log(rec(merge()).out.join(" "));\n',
       'hint': 'Subject хранит множество подписчиков; combineLatest — массив последних значений и флаги '
               '«значение было».',
       'expected': ['1 2 | 1',
                    '1 2 ✓ ✓',
                    '0',
                    '[20,2] [30,2] [30,3]',
                    '[30,3]',
                    '✓',
                    '"x1" "y1" "x2" "y2" ✓',
                    '✓']},
      {'id': 'j12-from-event',
       'mode': 'js',
       'title': 'fromEvent, takeUntil и подписки',
       'statement': 'Напишите функции fromEvent(target, name) (Observable значений события: '
                    'target.addEventListener(name, handler) / removeEventListener при отписке), '
                    'takeUntil(notifier) (оператор: пока notifier не выдал значение — источник идёт; потом '
                    'complete и отписка от обоих) и функцию typeahead(input$, search, debounce): input$ — '
                    'Observable строк; результат — Observable результатов search(текст) (асинхронная, '
                    'возвращает промис), которые приходят только для последнего текста (устаревшие '
                    'игнорируются); пустые строки пропускаются. Debounce в мс реализуйте через setTimeout. '
                    'Класс Observable определён.',
       'starter': 'function fromEvent(target, name) {\n'
                  '}\n'
                  'function takeUntil(notifier) {\n'
                  '}\n'
                  'function typeahead(input$, search, debounce) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import { EventEmitter } from "node:events";\n'
                 'class Target { constructor() { this.e = new EventEmitter(); } addEventListener(n, h) { '
                 'this.e.on(n, h); } removeEventListener(n, h) { this.e.off(n, h); } dispatch(n, d) { '
                 'this.e.emit(n, d); } count(n) { return this.e.listenerCount(n); } }\n'
                 'const sleep = (ms) => new Promise((r) => setTimeout(r, ms));\n'
                 'const t = new Target();\n'
                 'const got = [];\n'
                 'const sub = fromEvent(t, "click").subscribe((e) => got.push(e));\n'
                 't.dispatch("click", 1); t.dispatch("click", 2);\n'
                 'console.log(JSON.stringify(got), t.count("click"));\n'
                 'sub.unsubscribe(); t.dispatch("click", 3);\n'
                 'console.log(JSON.stringify(got), t.count("click"));\n'
                 'const stop = new Target(); const out = []; let done = false;\n'
                 'fromEvent(t, "move").pipe(takeUntil(fromEvent(stop, "stop"))).subscribe({ next: (v) => '
                 'out.push(v), complete: () => { done = true; } });\n'
                 't.dispatch("move", "a"); t.dispatch("move", "b"); stop.dispatch("stop"); '
                 't.dispatch("move", "c");\n'
                 'console.log(JSON.stringify(out), done, t.count("move"), stop.count("stop"));\n'
                 'const typed = new Target();\n'
                 'const search = async (q) => { await sleep(q.length === 2 ? 40 : 5); return "найдено для " '
                 '+ q; };\n'
                 'const results = [];\n'
                 'const ta = typeahead(fromEvent(typed, "input"), search, 20).subscribe((r) => '
                 'results.push(r));\n'
                 'typed.dispatch("input", "п"); await sleep(5); typed.dispatch("input", "по");\n'
                 'await sleep(30);\n'
                 'typed.dispatch("input", "пои");\n'
                 'await sleep(10);\n'
                 'console.log(JSON.stringify(results));\n'
                 'await sleep(80);\n'
                 'console.log(JSON.stringify(results));\n'
                 'typed.dispatch("input", ""); await sleep(40);\n'
                 'console.log(results.length);\n'
                 'ta.unsubscribe();\n'
                 'console.log(typed.count("input"));\n',
       'hint': 'Подписка на событие и снятие слушателя в функции отписки; для typeahead — счётчик запросов и '
               'сравнение номера.',
       'expected': ['[1,2] 1', '[1,2] 0', '["a","b"] true 0 0', '[]', '["найдено для пои"]', '1', '0']},
      {'id': 'j12-lodash-paths',
       'mode': 'js',
       'title': 'get/set по строковому пути и orderBy',
       'statement': 'Напишите функции parsePath(str) («a[0].b.c» → ["a", 0, "b", "c"]; числа в скобках — '
                    'числа; кавычки в скобках — строки: «a[\\"x y\\"]»), get(obj, str, default), set(obj, '
                    'str, value) — неизменяемо, и orderBy(xs, keys, orders): keys — функции или имена полей, '
                    'orders — "asc"/"desc" на каждый ключ (по умолчанию asc); сортировка устойчива, '
                    'сравнение строк через localeCompare(‘ru’), чисел — разностью.',
       'starter': 'function parsePath(str) {\n'
                  '}\n'
                  'function get(obj, str, def) {\n'
                  '}\n'
                  'function set(obj, str, value) {\n'
                  '}\n'
                  'function orderBy(xs, keys, orders) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(JSON.stringify(parsePath("a[0].b.c")), JSON.stringify(parsePath(\'x["y '
                 'z"].w\')), JSON.stringify(parsePath("[1][2]")), JSON.stringify(parsePath("a")), '
                 'JSON.stringify(parsePath("")));\n'
                 'const o = Object.freeze({ a: Object.freeze([Object.freeze({ b: Object.freeze({ c: '
                 '"глубоко" }) })]), k: Object.freeze({ keep: 1 }) });\n'
                 'console.log(get(o, "a[0].b.c"), get(o, "a[1].b", "нет"), get(o, "a[0].zzz.q"), get(o, '
                 '"k.keep", 9));\n'
                 'const n = set(o, "a[0].b.c", "новое");\n'
                 'console.log(JSON.stringify(n), n.k === o.k, o.a[0].b.c);\n'
                 'console.log(JSON.stringify(set({}, "x.y[1].z", 5)), JSON.stringify(set({ a: 1 }, "b", 2)), '
                 'JSON.stringify(set(null, "a.b", 1)));\n'
                 'const people = [{ n: "Борис", age: 30 }, { n: "Ада", age: 25 }, { n: "Вера", age: 30 }, { '
                 'n: "Ёж", age: 25 }];\n'
                 'console.log(orderBy(people, ["age", "n"], ["desc", "asc"]).map((p) => p.n).join());\n'
                 'console.log(orderBy(people, [(p) => p.n.length, "n"]).map((p) => p.n).join(), '
                 'orderBy(people, ["n"], ["desc"]).map((p) => p.n).join());\n'
                 'console.log(people.map((p) => p.n).join());\n',
       'hint': 'parsePath — регулярное выражение с вариантами: имя, [число], ["строка"].',
       'expected': ['["a",0,"b","c"] ["x","y z","w"] [1,2] ["a"] []',
                    'глубоко нет undefined 1',
                    '{"a":[{"b":{"c":"новое"}}],"k":{"keep":1}} true глубоко',
                    '{"x":{"y":[null,{"z":5}]}} {"a":1,"b":2} {"a":{"b":1}}',
                    'Борис,Вера,Ада,Ёж',
                    'Ёж,Ада,Вера,Борис Ёж,Вера,Борис,Ада',
                    'Борис,Ада,Вера,Ёж']},
      {'id': 'j12-point-free',
       'mode': 'js',
       'title': 'Рефакторинг в конвейер',
       'statement': 'Перепишите функцию normalizeUsers(users) в виде конвейера из маленьких чистых функций, '
                    'собранных pipe (определите pipe сами): оставить пользователей со статусом «active», '
                    'привести имя к виду «Фамилия, И.» из строки «Имя Фамилия» (в нижнем регистре «ада '
                    'лавлейс» → «Лавлейс, А.»), удалить дубликаты по e-mail (без учёта регистра; оставить '
                    'первого), отсортировать по фамилии по правилам русского языка. Результат — массив { '
                    'name, email } (e-mail в нижнем регистре). Исходный массив не меняется.',
       'starter': 'function normalizeUsers(users) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const users = Object.freeze([\n'
                 '  { name: "ада лавлейс", email: "Ada@X.ru", status: "active" },\n'
                 '  { name: "ЛИНУС торвальдс", email: "linus@x.ru", status: "active" },\n'
                 '  { name: "Борис ёлкин", email: "ada@x.ru", status: "active" },\n'
                 '  { name: "Вера Яковлева", email: "vera@x.ru", status: "blocked" },\n'
                 '  { name: "анна  Берг", email: "anna@x.ru", status: "active" },\n'
                 ']);\n'
                 'for (const u of normalizeUsers(users)) console.log(JSON.stringify(u));\n'
                 'console.log(users.length, normalizeUsers([]).length);\n',
       'hint': 'Каждый шаг — маленькая функция; pipe склеивает их слева направо.',
       'expected': ['{"name":"Берг, А.","email":"anna@x.ru"}',
                    '{"name":"Лавлейс, А.","email":"ada@x.ru"}',
                    '{"name":"Торвальдс, Л.","email":"linus@x.ru"}',
                    '5 0']},
      {'id': 'j12-state-monad',
       'mode': 'js',
       'title': 'State: вычисления с состоянием',
       'statement': 'Напишите State-монаду: State(run) где run(s) возвращает [значение, новоеСостояние]; '
                    'методы map(f), chain(f) (f возвращает State), runState(s) → [значение, состояние], '
                    'evalState(s), execState(s); статические State.of(v), State.get() (значение = '
                    'состояние), State.put(s), State.modify(f). Затем с их помощью напишите counterDemo() — '
                    'три раза увеличить счётчик и вернуть список увиденных значений, и операции стека '
                    'push(x), pop() на состоянии-массиве.',
       'starter': 'function State(run) {\n'
                  '}\n'
                  'const counterDemo = null;\n'
                  'const push = null;\n'
                  'const pop = null;\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(JSON.stringify(counterDemo().runState(10)));\n'
                 'console.log(counterDemo().evalState(0).join(), counterDemo().execState(5));\n'
                 'const prog = push(1).chain(() => push(2)).chain(() => push(3)).chain(() => '
                 'pop()).chain((top) => pop().map((second) => [top, second]));\n'
                 'console.log(JSON.stringify(prog.runState([])));\n'
                 'console.log(JSON.stringify(pop().runState([])), '
                 'JSON.stringify(State.of("v").runState("s")));\n'
                 'console.log(JSON.stringify(State.modify((n) => n * 2).chain(() => '
                 'State.get()).evalState(21)));\n'
                 'const frozen = Object.freeze([9]);\n'
                 'console.log(JSON.stringify(push(1).execState(frozen)), JSON.stringify(frozen));\n',
       'hint': 'State — функция состояния; chain передаёт новое состояние в следующий шаг.',
       'expected': ['[[10,11,12],13]', '0,1,2 8', '[[3,2],[1]]', '[null,[]] ["v","s"]', '42', '[9,1] [9]']},
      {'id': 'j12-writer',
       'mode': 'js',
       'title': 'Writer: вычисление с журналом',
       'statement': 'Напишите Writer(value, log) (log — массив): методы map(f) (журнал тот же), chain(f) '
                    '(f(value) возвращает Writer; журналы склеиваются), Writer.of(v), функцию tell(msg) → '
                    'Writer(undefined, [msg]). И функции: factorialW(n) (журнал «база: 1», затем «умножаю на '
                    'k» для k от 2 до n; результат n!) и collatzW(n) (значение — число шагов до 1; журнал — '
                    '«n → следующее» на каждом шаге).',
       'starter': 'function Writer(value, log) {\n'
                  '}\n'
                  'const tell = null;\n'
                  'function factorialW(n) {\n'
                  '}\n'
                  'function collatzW(n) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const w = Writer.of(2).chain((x) => tell("прибавил 3").chain(() => Writer(x + 3, '
                 '[]))).chain((x) => Writer(x * 2, ["удвоил"]));\n'
                 'console.log(w.value, JSON.stringify(w.log));\n'
                 'console.log(JSON.stringify(Writer(1, ["a"]).map((x) => x + 1).log), Writer(1, '
                 '["a"]).map((x) => x + 1).value);\n'
                 'const f = factorialW(4);\n'
                 'console.log(f.value, JSON.stringify(f.log));\n'
                 'const c = collatzW(6);\n'
                 'console.log(c.value, c.log.join(", "));\n'
                 'console.log(collatzW(1).value, collatzW(1).log.length, factorialW(1).value);\n',
       'hint': 'chain склеивает журналы: [...log, ...w.log].',
       'expected': ['10 ["прибавил 3","удвоил"]',
                    '["a"] 2',
                    '24 ["база: 1","умножаю на 2","умножаю на 3","умножаю на 4"]',
                    '8 6 → 3, 3 → 10, 10 → 5, 5 → 16, 16 → 8, 8 → 4, 4 → 2, 2 → 1',
                    '0 0 1']},
      {'id': 'j12-prism',
       'mode': 'js',
       'title': 'Призмы (prism)',
       'statement': 'Напишите функции prism(preview, review) (preview(whole) → значение или undefined, '
                    'review(value, whole?) → whole), preview(p, whole), review(p, value, whole), over(p, fn, '
                    'whole) (если призма не подходит — вернуть whole без изменений), и готовые призмы: '
                    'tagged(tag) для объектов { tag, value } и prismIndex(i) для i-го элемента массива (если '
                    'он существует). Призмы работают с вариантами, у которых «части может не быть».',
       'starter': 'function prism(preview, review) {\n'
                  '}\n'
                  'function preview(p, whole) {\n'
                  '}\n'
                  'function review(p, value, whole) {\n'
                  '}\n'
                  'function over(p, fn, whole) {\n'
                  '}\n'
                  'function tagged(tag) {\n'
                  '}\n'
                  'function prismIndex(i) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const circle = tagged("circle"), rect = tagged("rect");\n'
                 'const shape = Object.freeze({ tag: "circle", value: 2 });\n'
                 'console.log(preview(circle, shape), preview(rect, shape), JSON.stringify(review(circle, '
                 '5)));\n'
                 'console.log(JSON.stringify(over(circle, (r) => r * 10, shape)), over(rect, (w) => w + 1, '
                 'shape) === shape);\n'
                 'const second = prismIndex(1);\n'
                 'const a = Object.freeze(["x", "y", "z"]);\n'
                 'console.log(preview(second, a), preview(prismIndex(9), a), JSON.stringify(over(second, (s) '
                 '=> s.toUpperCase(), a)), over(prismIndex(9), (s) => s, a) === a);\n'
                 'console.log(JSON.stringify([shape, { tag: "rect", value: 3 }, { tag: "circle", value: 1 '
                 '}].map((s) => over(circle, (r) => r + 100, s))));\n',
       'hint': 'preview возвращает undefined, если варианта нет; over в этом случае ничего не меняет.',
       'expected': ['2 undefined {"tag":"circle","value":5}',
                    '{"tag":"circle","value":20} true',
                    'y undefined ["x","Y","z"] true',
                    '[{"tag":"circle","value":102},{"tag":"rect","value":3},{"tag":"circle","value":101}]']},
      {'id': 'j12-traversal',
       'mode': 'js',
       'title': 'Траверсалы: сразу много частей',
       'statement': 'Траверсал — линза на несколько частей. Напишите функции traversed() (объект { '
                    'toList(whole), over(fn, whole) } для массива: все элементы), field(key) (траверсал '
                    'одного поля), composeT(t1, t2) (применить t2 внутри каждой части t1), toListOf(t, '
                    'whole), overT(t, fn, whole), setT(t, value, whole). Всё неизменяемо.',
       'starter': 'function traversed() {\n'
                  '}\n'
                  'function field(key) {\n'
                  '}\n'
                  'function composeT(t1, t2) {\n'
                  '}\n'
                  'function toListOf(t, whole) {\n'
                  '}\n'
                  'function overT(t, fn, whole) {\n'
                  '}\n'
                  'function setT(t, value, whole) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const shop = Object.freeze({ name: "ларёк", items: Object.freeze([Object.freeze({ title: '
                 '"хлеб", price: 40 }), Object.freeze({ title: "сыр", price: 300 })]) });\n'
                 'const prices = composeT(composeT(field("items"), traversed()), field("price"));\n'
                 'console.log(JSON.stringify(toListOf(prices, shop)));\n'
                 'const cheaper = overT(prices, (p) => p * 0.9, shop);\n'
                 'console.log(JSON.stringify(cheaper.items.map((i) => i.price)), '
                 'JSON.stringify(shop.items.map((i) => i.price)));\n'
                 'console.log(JSON.stringify(setT(prices, 1, shop).items), cheaper.name === shop.name);\n'
                 'console.log(JSON.stringify(toListOf(traversed(), [1, 2, 3])), '
                 'JSON.stringify(overT(traversed(), (x) => x * 2, [1, 2, 3])), '
                 'JSON.stringify(toListOf(prices, { items: [] })));\n'
                 'const nested = [[1, 2], [3], []];\n'
                 'console.log(JSON.stringify(toListOf(composeT(traversed(), traversed()), nested)), '
                 'JSON.stringify(overT(composeT(traversed(), traversed()), (x) => -x, nested)));\n',
       'hint': 'toList возвращает все части, over применяет функцию ко всем; композиция вкладывает второй '
               'траверсал в первый.',
       'expected': ['[40,300]',
                    '[36,270] [40,300]',
                    '[{"title":"хлеб","price":1},{"title":"сыр","price":1}] true',
                    '[1,2,3] [2,4,6] []',
                    '[1,2,3] [[-1,-2],[-3],[]]']},
      {'id': 'j12-memoize-weak',
       'mode': 'js',
       'title': 'Мемоизация по ссылке (WeakMap)',
       'statement': 'Напишите функцию memoizeByRef(fn): fn принимает один аргумент; для объектов и функций '
                    'результат кэшируется в WeakMap по ссылке (при сборке мусора ключей запись исчезает), '
                    'для примитивов (включая null) — в обычном Map. Возвращаемая функция имеет метод calls() '
                    '— сколько раз реально вызывалась fn. Один и тот же объект с изменённым содержимым '
                    'считается тем же ключом (кэш не сбрасывается).',
       'starter': 'function memoizeByRef(fn) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const total = memoizeByRef((cart) => cart.items.reduce((s, i) => s + i.price, 0));\n'
                 'const cart = { items: [{ price: 10 }, { price: 20 }] };\n'
                 'console.log(total(cart), total(cart), total.calls());\n'
                 'cart.items.push({ price: 100 });\n'
                 'console.log(total(cart), total.calls());\n'
                 'const copy = { items: [...cart.items] };\n'
                 'console.log(total(copy), total.calls());\n'
                 'const sq = memoizeByRef((n) => n * n);\n'
                 'console.log(sq(4), sq(4), sq("5"), sq("5"), sq(null), sq(null), sq.calls());\n'
                 'const wm = memoizeByRef(() => 1);\n'
                 'wm({}); wm({});\n'
                 'console.log(wm.calls());\n'
                 'const fnKey = () => 1;\n'
                 'const m2 = memoizeByRef((f) => f());\n'
                 'console.log(m2(fnKey), m2(fnKey), m2.calls());\n',
       'hint': 'WeakMap — для объектов и функций, Map — для всего остального.',
       'expected': ['30 30 1', '30 1', '130 2', '16 16 25 25 0 0 3', '2', '1 1 1']},
      {'id': 'j12-kleisli',
       'mode': 'js',
       'title': 'Композиция функций, возвращающих Result',
       'statement': 'Напишите функцию composeK(...fns) (слева направо): каждая функция принимает значение и '
                    'возвращает Result — { ok: true, value } или { ok: false, error }; композиция передаёт '
                    'value следующей и останавливается на первой ошибке (остальные функции не вызываются). '
                    'Без функций — ok(x). Функцию liftA(f) (обычная функция → «функция с результатом»: '
                    'ok(f(x)), исключение — ошибка с error = сообщение) и asyncComposeK(...fns) — то же для '
                    'асинхронных функций (возвращают промис результата).',
       'starter': 'function composeK(...fns) {\n'
                  '}\n'
                  'function liftA(f) {\n'
                  '}\n'
                  'function asyncComposeK(...fns) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const Ok = (value) => ({ ok: true, value }), Er = (error) => ({ ok: false, error });\n'
                 'const parse = (s) => (Number.isNaN(Number(s)) ? Er("не число: " + s) : Ok(Number(s)));\n'
                 'const positive = (n) => (n > 0 ? Ok(n) : Er("не положительное: " + n));\n'
                 'const half = (n) => (n % 2 === 0 ? Ok(n / 2) : Er("нечётное: " + n));\n'
                 'const calls = [];\n'
                 'const spy = (name, f) => (x) => { calls.push(name); return f(x); };\n'
                 'const pipeline = composeK(spy("parse", parse), spy("positive", positive), spy("half", '
                 'half));\n'
                 'const show = (r) => console.log(JSON.stringify(r));\n'
                 'show(pipeline("10")); show(pipeline("7")); show(pipeline("-4")); show(pipeline("x"));\n'
                 'console.log(calls.join());\n'
                 'show(composeK()(5));\n'
                 'const safeJson = liftA(JSON.parse);\n'
                 'show(safeJson(\'{"a":1}\')); show(safeJson("{").ok); show(composeK(liftA((x) => x.trim()), '
                 'liftA(JSON.parse), (o) => Ok(o.a))("  {\\"a\\": 7} "));\n'
                 'const later = (f) => async (x) => { await new Promise((r) => setTimeout(r, 3)); return '
                 'f(x); };\n'
                 'show(await asyncComposeK(later(parse), later(positive), later(half))("8"));\n'
                 'show(await asyncComposeK(later(parse), later(positive), later(half))("-8"));\n'
                 'show(await asyncComposeK()(1));\n',
       'hint': 'Цикл по функциям: на ошибке — немедленный возврат, иначе значение передаётся дальше.',
       'expected': ['{"ok":true,"value":5}',
                    '{"ok":false,"error":"нечётное: 7"}',
                    '{"ok":false,"error":"не положительное: -4"}',
                    '{"ok":false,"error":"не число: x"}',
                    'parse,positive,half,parse,positive,half,parse,positive,parse',
                    '{"ok":true,"value":5}',
                    '{"ok":true,"value":{"a":1}}',
                    'false',
                    '{"ok":true,"value":7}',
                    '{"ok":true,"value":4}',
                    '{"ok":false,"error":"не положительное: -8"}',
                    '{"ok":true,"value":1}']}]}
