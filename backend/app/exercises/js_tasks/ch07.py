"""Задачи книги «Современный Frontend», глава 7 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {7: [{'id': 'j7-invert',
      'mode': 'js',
      'title': 'Инвертировать объект',
      'statement': 'Напишите функцию invert(obj): возвращает объект, в котором ключи и значения поменялись '
                   'местами (значения — строки или числа). Если значения повторяются, побеждает последний '
                   'ключ.',
      'starter': 'function invert(obj) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(invert({ a: "x", b: "y" })));\n'
                'console.log(JSON.stringify(invert({ a: 1, b: 1 })));\n'
                'console.log(JSON.stringify(invert({})));\n',
      'hint': 'Object.fromEntries(Object.entries(obj).map(([k, v]) => [v, k]))',
      'expected': ['{"x":"a","y":"b"}', '{"1":"b"}', '{}']},
     {'id': 'j7-pick',
      'mode': 'js',
      'title': 'pick: выбрать поля',
      'statement': 'Напишите функцию pick(obj, keys): возвращает новый объект только с теми полями из keys, '
                   'которые есть в obj (в порядке keys); исходный объект не меняется.',
      'starter': 'function pick(obj, keys) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const u = { id: 1, name: "Ада", pass: "x", n: undefined };\n'
                'console.log(JSON.stringify(pick(u, ["name", "id"])));\n'
                'console.log(JSON.stringify(pick(u, ["zzz"])));\n'
                'console.log(Object.keys(pick(u, ["n"])).length);\n'
                'console.log(Object.keys(u).length);\n',
      'hint': 'Проверяйте наличие поля через Object.hasOwn — значение может быть undefined.',
      'expected': ['{"name":"Ада","id":1}', '{}', '1', '4']},
     {'id': 'j7-omit',
      'mode': 'js',
      'title': 'omit: убрать поля',
      'statement': 'Напишите функцию omit(obj, keys): возвращает копию объекта без полей из keys; исходный '
                   'объект не меняется.',
      'starter': 'function omit(obj, keys) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const u = { id: 1, name: "Ада", pass: "x" };\n'
                'console.log(JSON.stringify(omit(u, ["pass"])));\n'
                'console.log(JSON.stringify(omit(u, ["id", "name", "pass"])));\n'
                'console.log(JSON.stringify(omit(u, ["zzz"])));\n'
                'console.log(JSON.stringify(u));\n',
      'hint': 'Скопируйте объект расширением и удалите ключи оператором delete.',
      'expected': ['{"id":1,"name":"Ада"}',
                   '{}',
                   '{"id":1,"name":"Ада","pass":"x"}',
                   '{"id":1,"name":"Ада","pass":"x"}']},
     {'id': 'j7-map-values',
      'mode': 'js',
      'title': 'mapValues',
      'statement': 'Напишите функцию mapValues(obj, fn): возвращает новый объект с теми же ключами, значения '
                   'которого — результат fn(значение, ключ).',
      'starter': 'function mapValues(obj, fn) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(mapValues({ a: 1, b: 2 }, (v) => v * 10)));\n'
                'console.log(JSON.stringify(mapValues({ a: 1, b: 2 }, (v, k) => k + v)));\n'
                'console.log(JSON.stringify(mapValues({}, (v) => v)));\n',
      'hint': 'Object.entries → map → Object.fromEntries',
      'expected': ['{"a":10,"b":20}', '{"a":"a1","b":"b2"}', '{}']},
     {'id': 'j7-defaults',
      'mode': 'js',
      'title': 'Объединить с умолчаниями',
      'statement': 'Напишите функцию withDefaults(opts, defaults): возвращает новый объект: поля defaults, '
                   'поверх которых записаны поля opts, кроме тех, где в opts стоит undefined (там остаётся '
                   'умолчание). Исходные объекты не меняются.',
      'starter': 'function withDefaults(opts, defaults) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const d = { size: 10, color: "red", on: true };\n'
                'console.log(JSON.stringify(withDefaults({ size: 5 }, d)));\n'
                'console.log(JSON.stringify(withDefaults({ size: undefined, on: false }, d)));\n'
                'console.log(JSON.stringify(withDefaults({ extra: 1 }, d)));\n'
                'console.log(JSON.stringify(d));\n',
      'hint': 'Обычное { ...defaults, ...opts } затрёт умолчания значением undefined — отфильтруйте их.',
      'expected': ['{"size":5,"color":"red","on":true}',
                   '{"size":10,"color":"red","on":false}',
                   '{"size":10,"color":"red","on":true,"extra":1}',
                   '{"size":10,"color":"red","on":true}']},
     {'id': 'j7-deep-clone',
      'mode': 'js',
      'title': 'Глубокая копия вручную',
      'statement': 'Напишите функцию deepClone(v) для JSON-подобных данных (числа, строки, булевы, null, '
                   'массивы и обычные объекты любой вложенности): возвращает полностью независимую копию. '
                   'structuredClone и JSON.parse использовать нельзя.',
      'starter': 'function deepClone(v) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'const src = { a: 1, b: [1, { c: 2 }], d: { e: null } };\n'
                'const c = deepClone(src);\n'
                'c.b[1].c = 99;\n'
                'c.d.e = "x";\n'
                'c.b.push(3);\n'
                'console.log(JSON.stringify(src));\n'
                'console.log(JSON.stringify(c));\n'
                'console.log(c !== src && c.b !== src.b && c.d !== src.d);\n'
                'console.log(deepClone(5), deepClone(null), JSON.stringify(deepClone([])));\n'
                'console.log(__count("structu" + "redClone") + __count("JSON." + "parse"));\n',
      'hint': 'Массив → map(deepClone); объект → рекурсия по Object.entries; остальное вернуть как есть.',
      'expected': ['{"a":1,"b":[1,{"c":2}],"d":{"e":null}}',
                   '{"a":1,"b":[1,{"c":99},3],"d":{"e":"x"}}',
                   'true',
                   '5 null []',
                   '0']},
     {'id': 'j7-deep-equal',
      'mode': 'js',
      'title': 'Глубокое сравнение',
      'statement': 'Напишите функцию deepEqual(a, b) для JSON-подобных данных: примитивы сравниваются через '
                   '===, массивы — поэлементно, объекты — по набору ключей и значений (порядок ключей '
                   'неважен).',
      'starter': 'function deepEqual(a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(deepEqual({ a: 1, b: [1, 2] }, { b: [1, 2], a: 1 }));\n'
                'console.log(deepEqual([1, [2]], [1, [2]]));\n'
                'console.log(deepEqual([1, 2], [1, 3]));\n'
                'console.log(deepEqual({ a: 1 }, { a: 1, b: undefined }));\n'
                'console.log(deepEqual([], {}));\n'
                'console.log(deepEqual(null, {}));\n'
                'console.log(deepEqual(1, 1), deepEqual("a", "b"));\n'
                'console.log(deepEqual({ a: { b: { c: 1 } } }, { a: { b: { c: 1 } } }));\n',
      'hint': 'Сначала ===, затем проверка типов, число ключей и рекурсия по ключам.',
      'expected': ['true', 'true', 'false', 'false', 'false', 'false', 'true false', 'true']},
     {'id': 'j7-get-path',
      'mode': 'js',
      'title': 'Значение по пути',
      'statement': 'Напишите функцию getPath(obj, path, def): path — строка вида «a.b.0.c»; возвращает '
                   'значение по этому пути, а если на пути встретилось null/undefined или поля нет (значение '
                   'undefined) — def. Найденное значение null или 0 возвращается как есть.',
      'starter': 'function getPath(obj, path, def) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const o = { a: { b: [{ c: 5 }, { c: 0 }] }, n: null };\n'
                'console.log(getPath(o, "a.b.0.c", "нет"));\n'
                'console.log(getPath(o, "a.b.1.c", "нет"));\n'
                'console.log(getPath(o, "a.x.y", "нет"));\n'
                'console.log(getPath(o, "n.z", "нет"));\n'
                'console.log(getPath(o, "a.b.5.c", "нет"));\n'
                'console.log(getPath(o, "n", "нет"));\n',
      'hint': 'Идите по ключам; при null/undefined на пути возвращайте def. Значение 0 — не «пусто».',
      'expected': ['5', '0', 'нет', 'нет', 'нет', 'null']},
     {'id': 'j7-set-in',
      'mode': 'js',
      'title': 'Неизменяемая запись по пути',
      'statement': 'Напишите функцию setIn(obj, path, value): path — массив ключей; возвращает новый объект, '
                   'в котором по этому пути лежит value. Исходный объект не меняется, а ветки, не затронутые '
                   'изменением, остаются теми же ссылками (не копируются). Недостающие объекты создавайте.',
      'starter': 'function setIn(obj, path, value) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const s = { user: { name: "Ада", age: 36 }, items: [1, 2] };\n'
                'const t = setIn(s, ["user", "age"], 37);\n'
                'console.log(JSON.stringify(s));\n'
                'console.log(JSON.stringify(t));\n'
                'console.log(t.items === s.items, t.user === s.user, t !== s);\n'
                'console.log(JSON.stringify(setIn({}, ["a", "b", "c"], 1)));\n'
                'console.log(JSON.stringify(setIn({ a: 1 }, ["b"], 2)));\n',
      'hint': 'Рекурсия: { ...obj, [k]: setIn(obj?.[k] ?? {}, rest, value) }',
      'expected': ['{"user":{"name":"Ада","age":36},"items":[1,2]}',
                   '{"user":{"name":"Ада","age":37},"items":[1,2]}',
                   'true false true',
                   '{"a":{"b":{"c":1}}}',
                   '{"a":1,"b":2}']},
     {'id': 'j7-swap-pairs',
      'mode': 'js',
      'title': 'Поменять соседние элементы',
      'statement': 'Напишите функцию swapPairs(arr): возвращает новый массив, в котором соседние пары (0-й и '
                   '1-й, 2-й и 3-й …) поменялись местами; последний непарный элемент остаётся на месте. Для '
                   'обмена используйте деструктурирование.',
      'starter': 'function swapPairs(arr) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(swapPairs([1, 2, 3, 4])));\n'
                'console.log(JSON.stringify(swapPairs([1, 2, 3])));\n'
                'console.log(JSON.stringify(swapPairs([])));\n'
                'console.log(JSON.stringify(swapPairs([7])));\n'
                'const a = [1, 2];\n'
                'swapPairs(a);\n'
                'console.log(JSON.stringify(a));\n',
      'hint': '[out[i], out[i + 1]] = [out[i + 1], out[i]];',
      'expected': ['[2,1,4,3]', '[2,1,3]', '[]', '[7]', '[1,2]']},
     {'id': 'j7-describe-user',
      'mode': 'js',
      'title': 'Деструктурирование вложенного объекта',
      'statement': 'Напишите функцию describeUser(user): с помощью деструктурирования в параметре достаньте '
                   'name, address.city (по умолчанию «неизвестно») и tags (по умолчанию []); верните «<name> '
                   'из <city>, тегов: <n>».',
      'starter': 'function describeUser(user) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(describeUser({ name: "Ада", address: { city: "Лондон" }, tags: ["a", "b"] }));\n'
                'console.log(describeUser({ name: "Линус" }));\n'
                'console.log(describeUser({ name: "Б", address: {} }));\n'
                'console.log(describeUser({ name: "В", address: { city: "Тверь" }, tags: [] }));\n',
      'hint': 'function describeUser({ name, address: { city = "неизвестно" } = {}, tags = [] })',
      'expected': ['Ада из Лондон, тегов: 2',
                   'Линус из неизвестно, тегов: 0',
                   'Б из неизвестно, тегов: 0',
                   'В из Тверь, тегов: 0']},
     {'id': 'j7-chunk',
      'mode': 'js',
      'title': 'Разбить на части',
      'statement': 'Напишите функцию chunk(arr, n): разбивает массив на части по n элементов; последняя '
                   'часть может быть короче; исходный массив не меняется.',
      'starter': 'function chunk(arr, n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(chunk([1, 2, 3, 4, 5], 2)));\n'
                'console.log(JSON.stringify(chunk([1, 2, 3, 4], 2)));\n'
                'console.log(JSON.stringify(chunk([], 3)));\n'
                'console.log(JSON.stringify(chunk([1, 2], 5)));\n'
                'console.log(JSON.stringify(chunk([1, 2, 3], 1)));\n',
      'hint': 'Цикл с шагом n и arr.slice(i, i + n).',
      'expected': ['[[1,2],[3,4],[5]]', '[[1,2],[3,4]]', '[]', '[[1,2]]', '[[1],[2],[3]]']},
     {'id': 'j7-unique',
      'mode': 'js',
      'title': 'Уникальные элементы по порядку',
      'statement': 'Напишите функцию unique(arr): возвращает массив без повторов в порядке первого '
                   'появления; NaN считается равным NaN. Используйте Set.',
      'starter': 'function unique(arr) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(unique([3, 1, 3, 2, 1])));\n'
                'console.log(JSON.stringify(unique(["a", "a", "b"])));\n'
                'console.log(unique([NaN, NaN, 1]).length);\n'
                'console.log(JSON.stringify(unique([])));\n'
                'console.log(unique([1, "1", 1]).length);\n',
      'hint': '[...new Set(arr)]',
      'expected': ['[3,1,2]', '["a","b"]', '2', '[]', '2']},
     {'id': 'j7-zip',
      'mode': 'js',
      'title': 'zip: объединить два массива',
      'statement': 'Напишите функцию zip(a, b): возвращает массив пар [a[i], b[i]] до длины более короткого '
                   'массива.',
      'starter': 'function zip(a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(zip([1, 2, 3], ["a", "b", "c"])));\n'
                'console.log(JSON.stringify(zip([1, 2, 3], ["a"])));\n'
                'console.log(JSON.stringify(zip([], [1])));\n'
                'console.log(JSON.stringify(zip(["x"], ["y", "z"])));\n',
      'hint': 'Array.from({ length: n }, (_, i) => [a[i], b[i]])',
      'expected': ['[[1,"a"],[2,"b"],[3,"c"]]', '[[1,"a"]]', '[]', '[["x","y"]]']},
     {'id': 'j7-rotate',
      'mode': 'js',
      'title': 'Циклический сдвиг',
      'statement': 'Напишите функцию rotate(arr, k): возвращает новый массив, сдвинутый влево на k позиций '
                   '(k может быть отрицательным — тогда вправо, и больше длины массива). Исходный не '
                   'меняется.',
      'starter': 'function rotate(arr, k) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(rotate([1, 2, 3, 4, 5], 2)));\n'
                'console.log(JSON.stringify(rotate([1, 2, 3, 4, 5], -1)));\n'
                'console.log(JSON.stringify(rotate([1, 2, 3], 7)));\n'
                'console.log(JSON.stringify(rotate([], 3)));\n'
                'console.log(JSON.stringify(rotate([1, 2, 3], 0)));\n'
                'console.log(JSON.stringify(rotate([1, 2, 3], -4)));\n',
      'hint': 'Нормализуйте k: ((k % n) + n) % n; затем slice(s) и slice(0, s).',
      'expected': ['[3,4,5,1,2]', '[5,1,2,3,4]', '[2,3,1]', '[]', '[1,2,3]', '[3,1,2]']},
     {'id': 'j7-set-ops',
      'mode': 'js',
      'title': 'Операции над множествами',
      'statement': 'Напишите функцию setOps(a, b): a и b — массивы; верните объект { both, onlyA, either } — '
                   'массивы уникальных элементов: общие, только из a, и из любого из них (в порядке первого '
                   'появления). Используйте Set.',
      'starter': 'function setOps(a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(setOps([1, 2, 3, 3], [3, 4, 2])));\n'
                'console.log(JSON.stringify(setOps([], [1])));\n'
                'console.log(JSON.stringify(setOps(["a"], ["a"])));\n'
                'console.log(JSON.stringify(setOps([1, 2], [3, 4])));\n',
      'hint': 'Set + filter(has) для пересечения и разности, new Set([...a, ...b]) для объединения.',
      'expected': ['{"both":[2,3],"onlyA":[1],"either":[1,2,3,4]}',
                   '{"both":[],"onlyA":[],"either":[1]}',
                   '{"both":["a"],"onlyA":[],"either":["a"]}',
                   '{"both":[],"onlyA":[1,2],"either":[1,2,3,4]}']},
     {'id': 'j7-count-by',
      'mode': 'js',
      'title': 'Частота элементов',
      'statement': 'Напишите функцию countItems(arr): возвращает массив пар [элемент, сколько раз '
                   'встретился], отсортированный по убыванию количества; при равенстве — в порядке первого '
                   'появления. Используйте Map.',
      'starter': 'function countItems(arr) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(countItems(["b", "a", "b", "c", "a", "b"])));\n'
                'console.log(JSON.stringify(countItems([1, 2, 3])));\n'
                'console.log(JSON.stringify(countItems([])));\n'
                'console.log(JSON.stringify(countItems([1, "1", 1, "1", "1"])));\n',
      'hint': 'Устойчивая сортировка сохранит порядок вставки Map для равных счётчиков.',
      'expected': ['[["b",3],["a",2],["c",1]]', '[[1,1],[2,1],[3,1]]', '[]', '[["1",3],[1,2]]']},
     {'id': 'j7-partition',
      'mode': 'js',
      'title': 'Разделить на две группы',
      'statement': 'Напишите функцию partition(arr, pred): возвращает [подходящие, остальные] — два массива '
                   'в исходном порядке; pred получает (элемент, индекс).',
      'starter': 'function partition(arr, pred) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(partition([1, 2, 3, 4, 5], (x) => x % 2 === 0)));\n'
                'console.log(JSON.stringify(partition([], () => true)));\n'
                'console.log(JSON.stringify(partition(["a", "b", "c"], (x, i) => i === 1)));\n'
                'console.log(JSON.stringify(partition([1, 2], () => false)));\n',
      'hint': '(pred(x, i) ? yes : no).push(x)',
      'expected': ['[[2,4],[1,3,5]]', '[[],[]]', '[["b"],["a","c"]]', '[[],[1,2]]']},
     {'id': 'j7-sort-by',
      'mode': 'js',
      'title': 'Сортировка объектов по ключу',
      'statement': 'Напишите функцию sortBy(arr, key): возвращает новый массив объектов, отсортированный по '
                   'полю key по возрастанию (числа — как числа, строки — по правилам русского алфавита, '
                   'localeCompare с локалью «ru»); сортировка устойчива, исходный массив не меняется.',
      'starter': 'function sortBy(arr, key) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const people = [{ n: "Яна", a: 30 }, { n: "Ёлка", a: 25 }, { n: "Егор", a: 30 }, { n: '
                '"Аня", a: 25 }];\n'
                'console.log(JSON.stringify(sortBy(people, "n").map((p) => p.n)));\n'
                'console.log(JSON.stringify(sortBy(people, "a").map((p) => p.n)));\n'
                'console.log(JSON.stringify(people.map((p) => p.n)));\n'
                'console.log(JSON.stringify(sortBy([], "a")));\n',
      'hint': 'Сравнивайте строки через localeCompare, числа — вычитанием; сортируйте копию.',
      'expected': ['["Аня","Егор","Ёлка","Яна"]',
                   '["Ёлка","Аня","Яна","Егор"]',
                   '["Яна","Ёлка","Егор","Аня"]',
                   '[]']},
     {'id': 'j7-sort-multi',
      'mode': 'js',
      'title': 'Сортировка по нескольким полям',
      'statement': 'Напишите функцию sortUsers(users): возвращает новый массив, отсортированный по возрасту '
                   'age по убыванию, а при равном возрасте — по имени name по возрастанию (localeCompare с '
                   'локалью «ru»).',
      'starter': 'function sortUsers(users) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const u = [{ name: "Борис", age: 30 }, { name: "Анна", age: 25 }, { name: "Алла", age: 30 '
                '}, { name: "Вера", age: 25 }, { name: "Ёж", age: 30 }];\n'
                'console.log(JSON.stringify(sortUsers(u).map((x) => x.name)));\n'
                'console.log(JSON.stringify(u.map((x) => x.name)));\n'
                'console.log(JSON.stringify(sortUsers([])));\n',
      'hint': 'b.age - a.age || a.name.localeCompare(b.name, "ru")',
      'expected': ['["Алла","Борис","Ёж","Анна","Вера"]', '["Борис","Анна","Алла","Вера","Ёж"]', '[]']},
     {'id': 'j7-matrix',
      'mode': 'js',
      'title': 'Матрица с независимыми строками',
      'statement': 'Напишите функцию createMatrix(rows, cols, value): возвращает массив из rows массивов по '
                   'cols элементов value; строки должны быть независимыми массивами (изменение одной не '
                   'влияет на другие).',
      'starter': 'function createMatrix(rows, cols, value) {\n'
                 '  return new Array(rows).fill(new Array(cols).fill(value));\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'const m = createMatrix(2, 3, 0);\n'
                'm[0][1] = 5;\n'
                'console.log(JSON.stringify(m));\n'
                'console.log(m[0] !== m[1]);\n'
                'console.log(JSON.stringify(createMatrix(0, 3, 1)));\n'
                'console.log(JSON.stringify(createMatrix(2, 0, 1)));\n',
      'hint': 'fill(array) раздаёт ссылку на один и тот же массив. Создавайте строку в колбэке Array.from.',
      'expected': ['[[0,5,0],[0,0,0]]', 'true', '[]', '[[],[]]']},
     {'id': 'j7-flatten-keys',
      'mode': 'js',
      'title': 'Плоские ключи',
      'statement': 'Напишите функцию flattenKeys(obj): превращает вложенный объект в плоский с ключами через '
                   'точку: { a: { b: 1 }, c: 2 } → { "a.b": 1, c: 2 }. Массивы и примитивы считаются '
                   'листьями.',
      'starter': 'function flattenKeys(obj) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(flattenKeys({ a: { b: 1, c: { d: 2 } }, e: 3 })));\n'
                'console.log(JSON.stringify(flattenKeys({})));\n'
                'console.log(JSON.stringify(flattenKeys({ a: [1, 2], b: null, c: { d: [3] } })));\n',
      'hint': 'Рекурсия с префиксом; для вложенного объекта — Object.assign(out, flattenKeys(v, key)).',
      'expected': ['{"a.b":1,"a.c.d":2,"e":3}', '{}', '{"a":[1,2],"b":null,"c.d":[3]}']},
     {'id': 'j7-lru',
      'mode': 'js',
      'title': 'Кэш LRU на Map',
      'statement': 'Напишите функцию createLru(capacity): возвращает объект с методами get(k) (значение или '
                   'undefined; обращение делает ключ «свежим») и set(k, v) (при переполнении удаляет самый '
                   'давно использованный ключ). Подсказка: Map помнит порядок вставки.',
      'starter': 'function createLru(capacity) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const c = createLru(2);\n'
                'c.set("a", 1); c.set("b", 2);\n'
                'console.log(c.get("a"));\n'
                'c.set("c", 3);\n'
                'console.log(c.get("b"), c.get("a"), c.get("c"));\n'
                'c.set("a", 10);\n'
                'c.set("d", 4);\n'
                'console.log(c.get("c"), c.get("a"), c.get("d"));\n',
      'hint': 'get: delete и set заново; set: если size > capacity — удалить первый ключ '
              'm.keys().next().value.',
      'expected': ['1', 'undefined 1 3', 'undefined 10 4']},
     {'id': 'j7-stable-stringify',
      'mode': 'js',
      'title': 'Стабильный JSON',
      'statement': 'Напишите функцию stableStringify(v): как JSON.stringify, но ключи объектов на всех '
                   'уровнях идут в алфавитном порядке (по умолчанию sort()). Достаточно поддержать '
                   'JSON-подобные данные.',
      'starter': 'function stableStringify(v) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(stableStringify({ b: 1, a: { d: [1, { z: 1, y: 2 }], c: "x" } }));\n'
                'console.log(stableStringify([]));\n'
                'console.log(stableStringify({}));\n'
                'console.log(stableStringify(null));\n'
                'console.log(stableStringify("a\\"b"));\n',
      'hint': 'Рекурсия: массивы — по элементам, объекты — по отсортированным ключам, остальное — '
              'JSON.stringify.',
      'expected': ['{"a":{"c":"x","d":[1,{"y":2,"z":1}]},"b":1}', '[]', '{}', 'null', '"a\\"b"']},
     {'id': 'j7-revive-dates',
      'mode': 'js',
      'title': 'JSON с датами',
      'statement': 'Напишите функцию parseWithDates(text): разбирает JSON и превращает все строковые '
                   'значения полей, имена которых оканчиваются на «At» (createdAt), в числа — миллисекунды '
                   'Date.parse. Используйте reviver — второй аргумент JSON.parse.',
      'starter': 'function parseWithDates(text) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const t = '
                '\'{"id":1,"createdAt":"2024-01-02T03:04:05.000Z","meta":{"updatedAt":"1970-01-01T00:00:00.000Z","note":"At"},"list":[{"doneAt":"2000-01-01T00:00:00.000Z"}]}\';\n'
                'console.log(JSON.stringify(parseWithDates(t)));\n'
                'console.log(JSON.stringify(parseWithDates(\'{"a":"b"}\')));\n'
                'console.log(typeof '
                'parseWithDates(\'{"x":{"startAt":"2020-02-02T00:00:00Z"}}\').x.startAt);\n',
      'hint': 'JSON.parse(text, (key, value) => …)',
      'expected': ['{"id":1,"createdAt":1704164645000,"meta":{"updatedAt":0,"note":"At"},"list":[{"doneAt":946684800000}]}',
                   '{"a":"b"}',
                   'number']},
     {'id': 'j7-toggle-todo',
      'mode': 'js',
      'title': 'Неизменяемое обновление списка',
      'statement': 'Напишите функцию toggleTodo(list, id): возвращает новый массив, в котором у задачи с '
                   'данным id поле done инвертировано. Остальные задачи остаются теми же объектами (не '
                   'копируются), исходный массив и исходная задача не меняются.',
      'starter': 'function toggleTodo(list, id) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const list = [{ id: 1, done: false }, { id: 2, done: true }, { id: 3, done: false }];\n'
                'const next = toggleTodo(list, 2);\n'
                'console.log(JSON.stringify(next));\n'
                'console.log(JSON.stringify(list));\n'
                'console.log(next !== list, next[0] === list[0], next[1] !== list[1], next[2] === list[2]);\n'
                'console.log(JSON.stringify(toggleTodo(list, 99)) === JSON.stringify(list));\n',
      'hint': 'list.map((t) => (t.id === id ? { ...t, done: !t.done } : t))',
      'expected': ['[{"id":1,"done":false},{"id":2,"done":false},{"id":3,"done":false}]',
                   '[{"id":1,"done":false},{"id":2,"done":true},{"id":3,"done":false}]',
                   'true true true true',
                   'true']},
     {'id': 'j7-update-nested',
      'mode': 'js',
      'title': 'Вложенное неизменяемое обновление',
      'statement': 'Состояние: { user: { name, address: { city, zip } }, items: [...] }. Напишите функцию '
                   'moveTo(state, city): возвращает новое состояние с изменённым user.address.city; '
                   'user.address, user и state — новые объекты, а user.name, address.zip и items остаются '
                   'прежними (те же ссылки). Исходное состояние не меняется.',
      'starter': 'function moveTo(state, city) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const s = { user: { name: "Ада", address: { city: "Лондон", zip: "N1" } }, items: [1, 2] '
                '};\n'
                'const t = moveTo(s, "Париж");\n'
                'console.log(JSON.stringify(s.user.address));\n'
                'console.log(JSON.stringify(t.user.address));\n'
                'console.log(t !== s, t.user !== s.user, t.user.address !== s.user.address);\n'
                'console.log(t.items === s.items, t.user.name === s.user.name);\n',
      'hint': 'Копируйте каждый уровень по цепочке: state → user → address.',
      'expected': ['{"city":"Лондон","zip":"N1"}',
                   '{"city":"Париж","zip":"N1"}',
                   'true true true',
                   'true true']},
     {'id': 'j7-fix-sort-mutation',
      'mode': 'js',
      'title': 'Исправьте: сортировка портит исходный массив',
      'statement': 'Функция topThree(scores) должна вернуть три наибольших числа по убыванию, не изменяя '
                   'переданный массив. Сейчас она сортирует его на месте и сравнивает как строки. Исправьте.',
      'starter': 'function topThree(scores) {\n  return scores.sort().reverse().slice(0, 3);\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const a = [5, 100, 25, 9, 1];\n'
                'console.log(JSON.stringify(topThree(a)));\n'
                'console.log(JSON.stringify(a));\n'
                'console.log(JSON.stringify(topThree([2, 1])));\n'
                'console.log(JSON.stringify(topThree([])));\n',
      'hint': 'Сортируйте копию с функцией сравнения (a, b) => b - a.',
      'expected': ['[100,25,9]', '[5,100,25,9,1]', '[2,1]', '[]']},
     {'id': 'j7-fix-shallow',
      'mode': 'js',
      'title': 'Исправьте: копия настроек не независима',
      'statement': 'Функция withTheme(config, theme) должна вернуть копию config с новым config.ui.theme, не '
                   'затрагивая оригинал. Сейчас она делает поверхностную копию и меняет вложенный объект '
                   'оригинала. Исправьте (подойдёт structuredClone).',
      'starter': 'function withTheme(config, theme) {\n'
                 '  const copy = { ...config };\n'
                 '  copy.ui.theme = theme;\n'
                 '  return copy;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'const cfg = { lang: "ru", ui: { theme: "light", size: 12 } };\n'
                'const next = withTheme(cfg, "dark");\n'
                'console.log(JSON.stringify(cfg));\n'
                'console.log(JSON.stringify(next));\n'
                'console.log(next !== cfg && next.ui !== cfg.ui);\n',
      'hint': 'structuredClone(config) создаёт независимую копию вложенных объектов.',
      'expected': ['{"lang":"ru","ui":{"theme":"light","size":12}}',
                   '{"lang":"ru","ui":{"theme":"dark","size":12}}',
                   'true']},
     {'id': 'j7-json-lines',
      'mode': 'js',
      'title': 'Разбор JSON Lines',
      'statement': 'Напишите функцию parseLines(text): каждая непустая строка текста — отдельный '
                   'JSON-документ. Верните { values, errors }: values — массив разобранных значений по '
                   'порядку, errors — число строк, которые не удалось разобрать (пустые и строки из пробелов '
                   'пропускайте, не считая ошибками).',
      'starter': 'function parseLines(text) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(parseLines(\'{"a":1}\\n[2,3]\\n"s"\\n\')));\n'
                'console.log(JSON.stringify(parseLines(\'{"a":1}\\n{oops}\\n\\n   \\nnull\\n{\')));\n'
                'console.log(JSON.stringify(parseLines("")));\n'
                'console.log(JSON.stringify(parseLines("1\\n2\\nx")));\n',
      'hint': 'Разбейте по переводу строки; try { JSON.parse } catch { errors++ }.',
      'expected': ['{"values":[{"a":1},[2,3],"s"],"errors":0}',
                   '{"values":[{"a":1},null],"errors":2}',
                   '{"values":[],"errors":0}',
                   '{"values":[1,2],"errors":1}']}]}
