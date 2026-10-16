"""Задачи книги «Современный Frontend», глава 2 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {2: [{'id': 'j2-semver-parse',
      'mode': 'js',
      'title': 'Разбор версии semver',
      'statement': 'Напишите функцию parseSemver(s): «1.2.3», «v1.2.3», «1.2.3-beta.1», «1.2.3+build5» → { '
                   'major, minor, patch, pre } (pre — массив частей пререлиза, числовые части — числами, без '
                   'пререлиза — []; build-метаданные отбрасываются). Для неверной строки верните null.',
      'starter': 'function parseSemver(s) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const s of ["1.2.3", "v10.0.1", "1.2.3-beta.1", "1.2.3-rc.1+build5", "1.2", "x.y.z", '
                '"1.2.3.4", "", "0.0.0-alpha"]) console.log(JSON.stringify(parseSemver(s)));\n',
      'hint': 'Регулярное выражение с группами для major, minor, patch, пререлиза и build.',
      'expected': ['{"major":1,"minor":2,"patch":3,"pre":[]}',
                   '{"major":10,"minor":0,"patch":1,"pre":[]}',
                   '{"major":1,"minor":2,"patch":3,"pre":["beta",1]}',
                   '{"major":1,"minor":2,"patch":3,"pre":["rc",1]}',
                   'null',
                   'null',
                   'null',
                   'null',
                   '{"major":0,"minor":0,"patch":0,"pre":["alpha"]}']},
     {'id': 'j2-semver-compare',
      'mode': 'js',
      'title': 'Сравнение версий semver',
      'statement': 'Напишите функцию compareSemver(a, b) (строки версий): -1, 0 или 1. Сравниваются major, '
                   'minor, patch как числа. Версия с пререлизом младше такой же без него; пререлизы '
                   'сравниваются по частям: числовые — как числа, строковые — по алфавиту, числовая часть '
                   'младше строковой, более короткий набор частей младше, если все его части совпали. '
                   'Build-метаданные не учитываются.',
      'starter': 'function compareSemver(a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const pairs = [["1.0.0", "2.0.0"], ["1.10.0", "1.9.0"], ["1.2.3", "1.2.3"], ["1.0.0-alpha", '
                '"1.0.0"], ["1.0.0-alpha", "1.0.0-alpha.1"], ["1.0.0-alpha.1", "1.0.0-alpha.beta"], '
                '["1.0.0-beta.2", "1.0.0-beta.11"], ["1.0.0-rc.1", "1.0.0-beta.11"], ["1.0.0+a", "1.0.0+b"], '
                '["v4.0.0", "0.12.7"]];\n'
                'for (const [a, b] of pairs) console.log(a, b, compareSemver(a, b), compareSemver(b, a));\n',
      'hint': 'Сначала числа major/minor/patch, затем пререлизы по частям: число < строка; без пререлиза — '
              'старше.',
      'expected': ['1.0.0 2.0.0 -1 1',
                   '1.10.0 1.9.0 1 -1',
                   '1.2.3 1.2.3 0 0',
                   '1.0.0-alpha 1.0.0 -1 1',
                   '1.0.0-alpha 1.0.0-alpha.1 -1 1',
                   '1.0.0-alpha.1 1.0.0-alpha.beta -1 1',
                   '1.0.0-beta.2 1.0.0-beta.11 -1 1',
                   '1.0.0-rc.1 1.0.0-beta.11 1 -1',
                   '1.0.0+a 1.0.0+b 0 0',
                   'v4.0.0 0.12.7 1 -1']},
     {'id': 'j2-semver-satisfies',
      'mode': 'js',
      'title': 'Диапазоны версий: ^, ~, >=',
      'statement': 'Напишите функцию satisfies(version, range) для версий без пререлизов: range — «1.2.3» '
                   '(точно), «^1.2.3» (≥1.2.3 и <2.0.0; для «^0.2.3» — <0.3.0; для «^0.0.3» — только 0.0.3), '
                   '«~1.2.3» (≥1.2.3 и <1.3.0), «>=1.2.3», «>1.2.3», «<=1.2.3», «<1.2.3», «*» (любая).',
      'starter': 'function satisfies(version, range) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const t = [["1.2.3", "^1.2.3"], ["1.9.9", "^1.2.3"], ["2.0.0", "^1.2.3"], ["1.2.2", '
                '"^1.2.3"], ["0.2.9", "^0.2.3"], ["0.3.0", "^0.2.3"], ["0.0.3", "^0.0.3"], ["0.0.4", '
                '"^0.0.3"], ["1.2.9", "~1.2.3"], ["1.3.0", "~1.2.3"], ["1.2.3", "1.2.3"], ["1.2.4", '
                '"1.2.3"], ["4.0.0", ">=4.0.0"], ["3.9.9", ">=4.0.0"], ["4.0.0", ">4.0.0"], ["3.0.0", '
                '"<4.0.0"], ["4.0.0", "<=4.0.0"], ["9.9.9", "*"], ["10.0.0", "^9.5.0"]];\n'
                'for (const [v, r] of t) console.log(v, r, satisfies(v, r));\n',
      'hint': 'Для ^ верхняя граница — следующий «значимый» разряд: major, если он > 0, иначе minor, иначе '
              'patch.',
      'expected': ['1.2.3 ^1.2.3 true',
                   '1.9.9 ^1.2.3 true',
                   '2.0.0 ^1.2.3 false',
                   '1.2.2 ^1.2.3 false',
                   '0.2.9 ^0.2.3 true',
                   '0.3.0 ^0.2.3 false',
                   '0.0.3 ^0.0.3 true',
                   '0.0.4 ^0.0.3 false',
                   '1.2.9 ~1.2.3 true',
                   '1.3.0 ~1.2.3 false',
                   '1.2.3 1.2.3 true',
                   '1.2.4 1.2.3 false',
                   '4.0.0 >=4.0.0 true',
                   '3.9.9 >=4.0.0 false',
                   '4.0.0 >4.0.0 false',
                   '3.0.0 <4.0.0 true',
                   '4.0.0 <=4.0.0 true',
                   '9.9.9 * true',
                   '10.0.0 ^9.5.0 false']},
     {'id': 'j2-semver-bump',
      'mode': 'js',
      'title': 'Повышение версии',
      'statement': 'Напишите функцию bump(version, kind): kind — «major», «minor» или «patch»; возвращает '
                   'новую строку версии (при повышении старшего разряда младшие сбрасываются в 0); пререлиз '
                   'и build отбрасываются. Для неизвестного kind бросьте Error.',
      'starter': 'function bump(version, kind) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(bump("1.2.3", "patch"), bump("1.2.3", "minor"), bump("1.2.3", "major"));\n'
                'console.log(bump("v0.12.7", "major"), bump("4.0.0-rc.1", "patch"), bump("1.9.9+b5", '
                '"minor"));\n'
                'try { bump("1.0.0", "huge"); } catch (e) { console.log(e.message); }\n',
      'hint': 'Деструктурирующее присваивание сбрасывает младшие разряды: [minor, patch] = [minor + 1, 0].',
      'expected': ['1.2.4 1.3.0 2.0.0', '1.0.0 4.0.1 1.10.0', 'неизвестный kind: huge']},
     {'id': 'j2-require',
      'mode': 'js',
      'title': 'Загрузчик CommonJS-модулей',
      'statement': 'Напишите функцию makeRequire(files): files — объект «имя → функция (module, exports, '
                   'require)»; makeRequire возвращает функцию require(name). Модуль выполняется один раз '
                   '(результат кэшируется), require возвращает module.exports; присваивание module.exports = '
                   '… должно работать так же, как запись в exports. Для неизвестного имени бросьте '
                   'Error("Cannot find module \'<name>\'").',
      'starter': 'function makeRequire(files) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'let runs = 0;\n'
                'const files = {\n'
                '  math: (module, exports) => { runs++; exports.add = (a, b) => a + b; },\n'
                '  pi: (module) => { runs++; module.exports = 3.14; },\n'
                '  app: (module, exports, require) => { module.exports = { sum: require("math").add(1, 2), '
                'pi: require("pi") }; },\n'
                '};\n'
                'const require = makeRequire(files);\n'
                'console.log(JSON.stringify(require("app")));\n'
                'console.log(require("math") === require("math"), require("pi"));\n'
                'console.log(runs);\n'
                'try { require("zzz"); } catch (e) { console.log(e.message); }\n',
      'hint': 'Кэш по имени: сначала запишите module в кэш, затем выполняйте файл.',
      'expected': ['{"sum":3,"pi":3.14}', 'true 3.14', '2', "Cannot find module 'zzz'"]},
     {'id': 'j2-require-cycle',
      'mode': 'js',
      'title': 'Циклические зависимости в require',
      'statement': 'Модули могут требовать друг друга по кругу. Напишите функцию makeRequire(files) как '
                   'загрузчик CommonJS (кэш + module.exports), который при цикле отдаёт «недостроенный» '
                   'экспорт модуля, как Node.js: модуль кладётся в кэш до выполнения.',
      'starter': 'function makeRequire(files) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const log = [];\n'
                'const files = {\n'
                '  a: (m, e, require) => { e.early = 1; log.push("a: подключаю b"); const b = require("b"); '
                'log.push("a: b.sawA = " + JSON.stringify(b.sawA)); e.late = 2; },\n'
                '  b: (m, e, require) => { log.push("b: подключаю a"); const a = require("a"); e.sawA = '
                'JSON.stringify(a); },\n'
                '};\n'
                'const require = makeRequire(files);\n'
                'const a = require("a");\n'
                'console.log(log.join(" | "));\n'
                'console.log(JSON.stringify(a), JSON.stringify(require("b")));\n',
      'hint': 'Кладите module в кэш до вызова функции модуля.',
      'expected': ['a: подключаю b | b: подключаю a | a: b.sawA = "{\\"early\\":1}"',
                   '{"early":1,"late":2} {"sawA":"{\\"early\\":1}"}']},
     {'id': 'j2-path',
      'mode': 'js',
      'title': 'Модуль path: basename, dirname, extname',
      'statement': 'Напишите функции basename(p, ext?) (последняя часть пути; если передано ext и имя '
                   'оканчивается им — без него), dirname(p) (всё до последнего «/»; «.» если слэша нет; «/» '
                   'для корня) и extname(p) (расширение с точкой из последней части; «» если точки нет или '
                   'она первая в имени). Завершающие «/» игнорируйте. Модуль path использовать нельзя.',
      'starter': 'function basename(p, ext) {\n}\nfunction dirname(p) {\n}\nfunction extname(p) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'for (const p of ["/a/b/c.txt", "c.txt", "/a/b/", "/", ".bashrc", "/x/archive.tar.gz", '
                '"dir/file", "a/b/.hidden.js"]) {\n'
                '  console.log(JSON.stringify([basename(p), dirname(p), extname(p)]));\n'
                '}\n'
                'console.log(basename("/a/b/c.txt", ".txt"), basename("c.txt", "c.txt"), '
                'basename("/a/b/c.js", ".txt"));\n'
                'console.log(__count("node:" + "path") + __count("req" + "uire("));\n',
      'hint': 'lastIndexOf("/") и lastIndexOf("."); не забудьте особые случаи: корень, пустая часть, скрытые '
              'файлы.',
      'expected': ['["c.txt","/a/b",".txt"]',
                   '["c.txt",".",".txt"]',
                   '["b","/a",""]',
                   '["","/",""]',
                   '[".bashrc",".",""]',
                   '["archive.tar.gz","/x",".gz"]',
                   '["file","dir",""]',
                   '[".hidden.js","a/b",".js"]',
                   'c c.txt c.js',
                   '0']},
     {'id': 'j2-emitter',
      'mode': 'js',
      'title': 'EventEmitter как в Node.js',
      'statement': 'Напишите класс EventEmitter с методами on(event, fn), once(event, fn), off(event, fn), '
                   'emit(event, ...args) (возвращает true, если у события были обработчики), '
                   'listenerCount(event). Обработчики вызываются в порядке подписки; once срабатывает один '
                   "раз; emit('error') без обработчиков бросает переданную ошибку. Методы on/once/off "
                   'возвращают this.',
      'starter': 'class EventEmitter {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const e = new EventEmitter();\n'
                'const log = [];\n'
                'const a = (x) => log.push("a" + x);\n'
                'e.on("m", a).on("m", (x) => log.push("b" + x)).once("m", (x) => log.push("o" + x));\n'
                'console.log(e.listenerCount("m"));\n'
                'console.log(e.emit("m", 1), e.emit("m", 2), e.emit("zzz"));\n'
                'console.log(log.join(","), e.listenerCount("m"));\n'
                'e.off("m", a);\n'
                'e.emit("m", 3);\n'
                'console.log(log.join(","));\n'
                'try { e.emit("error", new Error("упало")); } catch (err) { console.log("поймано", '
                'err.message); }\n'
                'e.on("error", (x) => log.push("err:" + x.message));\n'
                'console.log(e.emit("error", new Error("ещё")), log.at(-1));\n',
      'hint': 'Храните обработчики с флагом once; при emit обходите копию массива.',
      'expected': ['3',
                   'true true false',
                   'a1,b1,o1,a2,b2 2',
                   'a1,b1,o1,a2,b2,b3',
                   'поймано упало',
                   'true err:ещё']},
     {'id': 'j2-fake-clock',
      'mode': 'js',
      'title': 'Фальшивые таймеры',
      'statement': 'Напишите класс FakeClock: метод setTimeout(fn, ms) → id (с 1), clearTimeout(id), now() '
                   '(виртуальное время, 0 в начале) и advance(ms): продвигает время и выполняет все таймеры, '
                   'срок которых наступил, в порядке срока (при равенстве — в порядке создания); внутри '
                   'колбэка now() равно времени срабатывания; таймеры, созданные во время выполнения '
                   'колбэков, тоже срабатывают, если успевают в advance.',
      'starter': 'class FakeClock {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const c = new FakeClock();\n'
                'const log = [];\n'
                'c.setTimeout(() => log.push("a@" + c.now()), 100);\n'
                'const b = c.setTimeout(() => log.push("b@" + c.now()), 50);\n'
                'c.setTimeout(() => { log.push("c@" + c.now()); c.setTimeout(() => log.push("c2@" + '
                'c.now()), 30); }, 50);\n'
                'c.setTimeout(() => log.push("d@" + c.now()), 100);\n'
                'c.advance(40);\n'
                'console.log(log.join(), c.now());\n'
                'c.advance(20);\n'
                'console.log(log.join(), c.now());\n'
                'c.advance(100);\n'
                'console.log(log.join(), c.now());\n'
                'const x = c.setTimeout(() => log.push("x"), 10);\n'
                'c.clearTimeout(x);\n'
                'c.advance(50);\n'
                'console.log(log.length);\n',
      'hint': 'Каждый раз выбирайте ближайший таймер с at <= end, сдвигайте now на его срок и вызывайте.',
      'expected': [' 40', 'b@50,c@50 60', 'b@50,c@50,c2@80,a@100,d@100 160', '5']},
     {'id': 'j2-order-tick',
      'mode': 'js',
      'title': 'Порядок: nextTick и таймер',
      'statement': 'Напишите функцию run(), которая через console.log выводит строки в таком порядке: «1: '
                   'синхронно», «2: nextTick», «3: таймер». Используйте process.nextTick и setTimeout (с '
                   'нулевой задержкой), код вывода «синхронно» должен идти в конце функции.',
      'starter': 'function run() {\n}\n',
      'driver': '/*__DRIVER__*/\nrun();\nconsole.log("конец скрипта");\n',
      'hint': 'nextTick выполняется после текущей операции, но раньше таймеров.',
      'expected': ['1: синхронно', 'конец скрипта', '2: nextTick', '3: таймер']},
     {'id': 'j2-order-timers',
      'mode': 'js',
      'title': 'Порядок таймеров',
      'statement': 'Напишите функцию run(): три setTimeout с задержками 30, 10 и 20 мс выводят «C», «A» и '
                   '«B» соответственно (то есть по времени — A, B, C, но вызывать вы их будете в порядке C, '
                   'A, B). После вывода всех трёх выведите «готово» — через четвёртый таймер, который '
                   'сработает после остальных.',
      'starter': 'function run() {\n}\n',
      'driver': '/*__DRIVER__*/\nrun();\nconsole.log("начало");\n',
      'hint': 'Порядок срабатывания определяется сроком, а не порядком вызова setTimeout.',
      'expected': ['начало', 'A', 'B', 'C', 'готово']},
     {'id': 'j2-order-microtask',
      'mode': 'js',
      'title': 'Порядок: микрозадача и таймер',
      'statement': 'Напишите функцию run(): выведите «sync», затем «micro» (queueMicrotask), затем «timer» '
                   '(setTimeout с нулевой задержкой). Запланируйте всё в произвольном порядке, но так, чтобы '
                   'вывод получился именно таким; «sync» — в конце тела функции.',
      'starter': 'function run() {\n}\n',
      'driver': '/*__DRIVER__*/\nrun();\nconsole.log("конец скрипта");\n',
      'hint': 'Микрозадачи выполняются сразу после текущего синхронного кода, раньше любых таймеров.',
      'expected': ['sync', 'конец скрипта', 'micro', 'timer']},
     {'id': 'j2-worker-pool',
      'mode': 'js',
      'title': 'Блокирующая модель: пул потоков',
      'statement': 'Напишите функцию totalTime(durations, workers): задачи (длительности в мс) раздаются по '
                   'порядку свободным потокам; поток, освободившись, берёт следующую задачу; верните время '
                   'завершения последней. Так считается, сколько тратит сервер «поток на соединение», когда '
                   'потоков мало.',
      'starter': 'function totalTime(durations, workers) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(totalTime([100, 100, 100, 100], 4));\n'
                'console.log(totalTime([100, 100, 100, 100], 2));\n'
                'console.log(totalTime([100, 100, 100, 100], 1));\n'
                'console.log(totalTime([30, 10, 20, 40], 2));\n'
                'console.log(totalTime([], 3), totalTime([5], 10));\n'
                'console.log(totalTime(Array(1000).fill(10), 10));\n',
      'hint': 'Следите за временем освобождения каждого потока; следующая задача идёт самому раннему '
              'свободному.',
      'expected': ['100', '200', '400', '70', '0 5', '1000']},
     {'id': 'j2-max-concurrent',
      'mode': 'js',
      'title': 'Сколько одновременных соединений',
      'statement': 'Напишите функцию maxConcurrent(requests): requests — массив [start, end) (миллисекунды, '
                   'конец не включается); верните наибольшее число одновременно открытых соединений.',
      'starter': 'function maxConcurrent(requests) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(maxConcurrent([[0, 10], [5, 15], [10, 20]]));\n'
                'console.log(maxConcurrent([[0, 5], [5, 10]]));\n'
                'console.log(maxConcurrent([]));\n'
                'console.log(maxConcurrent([[1, 100], [2, 99], [3, 98], [50, 51]]));\n'
                'console.log(maxConcurrent(Array.from({ length: 100000 }, (_, i) => [i, i + 3])));\n',
      'hint': 'События «начало» (+1) и «конец» (−1), при равных моментах конец раньше начала.',
      'expected': ['2', '1', '0', '4', '3']},
     {'id': 'j2-parse-request',
      'mode': 'js',
      'title': 'Разбор HTTP-запроса',
      'statement': 'Напишите функцию parseRequest(text): сырой запрос «GET /path?a=1&b=2 HTTP/1.1\\r\\nHost: '
                   'x\\r\\nContent-Type: text/plain\\r\\n\\r\\nтело» → { method, path, query (объект строк), '
                   'headers (ключи в нижнем регистре), body }. Заголовки — до первой пустой строки; query '
                   'может отсутствовать.',
      'starter': 'function parseRequest(text) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const r = parseRequest("GET /users?id=7&name=%D0%90%D0%B4%D0%B0 HTTP/1.1\\r\\nHost: '
                'example.com\\r\\nContent-Type: text/plain\\r\\n\\r\\n");\n'
                'console.log(JSON.stringify(r));\n'
                'console.log(JSON.stringify(parseRequest("POST /api HTTP/1.1\\r\\nHost: '
                'x\\r\\nContent-Length: 11\\r\\n\\r\\nhello\\r\\n\\r\\nworld")));\n'
                'console.log(JSON.stringify(parseRequest("GET / HTTP/1.1\\r\\n\\r\\n")));\n',
      'hint': 'Разделите по «\\r\\n\\r\\n» на голову и тело; затем по строкам, а заголовки — по первому «:».',
      'expected': ['{"method":"GET","path":"/users","query":{"id":"7","name":"Ада"},"headers":{"host":"example.com","content-type":"text/plain"},"body":""}',
                   '{"method":"POST","path":"/api","query":{},"headers":{"host":"x","content-length":"11"},"body":"hello\\r\\n\\r\\nworld"}',
                   '{"method":"GET","path":"/","query":{},"headers":{},"body":""}']},
     {'id': 'j2-router',
      'mode': 'js',
      'title': 'Маршрутизатор с параметрами',
      'statement': 'Напишите функцию createRouter(routes): routes — массив [шаблон, обработчик], шаблон '
                   'вроде «/users/:id/posts/:post»; возвращает функцию route(path), которая находит первый '
                   'подходящий шаблон (сегменты считаются по «/», «:имя» — параметр, совпадает с непустым '
                   'сегментом) и возвращает обработчик(params); если ничего не подошло — null. Конечный «/» '
                   'игнорируется.',
      'starter': 'function createRouter(routes) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const route = createRouter([\n'
                '  ["/", () => "главная"],\n'
                '  ["/users/:id", (p) => "пользователь " + p.id],\n'
                '  ["/users/:id/posts/:post", (p) => `пост ${p.post} у ${p.id}`],\n'
                '  ["/about", () => "о нас"],\n'
                ']);\n'
                'for (const p of ["/", "/users/7", "/users/7/", "/users/7/posts/3", "/about", "/nope", '
                '"/users", "/users/%D0%90"]) console.log(p, route(p));\n',
      'hint': 'Сравнивайте сегменты попарно; сегмент шаблона на «:» записывает параметр.',
      'expected': ['/ главная',
                   '/users/7 пользователь 7',
                   '/users/7/ пользователь 7',
                   '/users/7/posts/3 пост 3 у 7',
                   '/about о нас',
                   '/nope null',
                   '/users null',
                   '/users/%D0%90 пользователь А']},
     {'id': 'j2-middleware',
      'mode': 'js',
      'title': 'Цепочка middleware',
      'statement': 'Напишите функцию createApp(): возвращает объект с методами use(fn) (fn(ctx, next)) и '
                   'run(ctx) → вызывает цепочку по порядку; next() запускает следующий обработчик (после '
                   'последнего — ничего); вызов next() дважды из одного обработчика бросает Error("next() '
                   'вызван дважды"). run возвращает ctx.',
      'starter': 'function createApp() {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const app = createApp();\n'
                'app.use((ctx, next) => { ctx.log.push("1 до"); next(); ctx.log.push("1 после"); })\n'
                '   .use((ctx, next) => { ctx.log.push("2"); if (ctx.stop) return; next(); })\n'
                '   .use((ctx) => { ctx.log.push("3"); });\n'
                'console.log(app.run({ log: [] }).log.join(" > "));\n'
                'console.log(app.run({ log: [], stop: true }).log.join(" > "));\n'
                'const bad = createApp().use((ctx, next) => { next(); next(); });\n'
                'try { bad.run({}); } catch (e) { console.log(e.message); }\n'
                'console.log(JSON.stringify(createApp().run({ a: 1 })));\n',
      'hint': 'dispatch(i) вызывает stack[i](ctx, () => dispatch(i + 1)); запоминайте индекс последнего '
              'вызова.',
      'expected': ['1 до > 2 > 3 > 1 после', '1 до > 2 > 1 после', 'next() вызван дважды', '{"a":1}']},
     {'id': 'j2-json-api',
      'mode': 'js',
      'title': 'Мини-API: обработчик запросов',
      'statement': 'Напишите функцию handle(req, db): req = { method, path, body }, db — массив объектов { '
                   'id, text }. Маршруты: GET /items → 200 и список; GET /items/<id> → 200 и элемент или '
                   '404; POST /items (body — объект с text) → 201 и созданный элемент { id: следующий номер, '
                   'text } (добавьте в db; без text — 400); остальное — 404 «не найдено». Верните { status, '
                   'body }.',
      'starter': 'function handle(req, db) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const db = [{ id: 1, text: "a" }];\n'
                'const show = (r) => console.log(r.status, JSON.stringify(r.body));\n'
                'show(handle({ method: "GET", path: "/items" }, db));\n'
                'show(handle({ method: "GET", path: "/items/1" }, db));\n'
                'show(handle({ method: "GET", path: "/items/9" }, db));\n'
                'show(handle({ method: "POST", path: "/items", body: { text: "b" } }, db));\n'
                'show(handle({ method: "POST", path: "/items", body: {} }, db));\n'
                'show(handle({ method: "POST", path: "/items", body: { text: "c" } }, db));\n'
                'show(handle({ method: "DELETE", path: "/items/1" }, db));\n'
                'show(handle({ method: "GET", path: "/zzz" }, db));\n'
                'console.log(db.length);\n',
      'hint': 'Один маршрутный шаблон /items(/id)? и затем ветвление по методу.',
      'expected': ['200 [{"id":1,"text":"a"}]',
                   '200 {"id":1,"text":"a"}',
                   '404 "не найдено"',
                   '201 {"id":2,"text":"b"}',
                   '400 "нужен text"',
                   '201 {"id":3,"text":"c"}',
                   '404 "не найдено"',
                   '404 "не найдено"',
                   '3']},
     {'id': 'j2-line-splitter',
      'mode': 'js',
      'title': 'Потоковый разбор строк',
      'statement': 'Данные приходят кусками (chunk), границы кусков произвольны. Напишите функцию '
                   'createLineParser(onLine): возвращает объект с методами write(chunk) (для каждой '
                   'завершённой строки вызывает onLine(строка) без «\\n»; «\\r\\n» тоже считается концом) и '
                   'end() (отдаёт последнюю незавершённую строку, если она не пуста).',
      'starter': 'function createLineParser(onLine) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const out = [];\n'
                'const p = createLineParser((l) => out.push(l));\n'
                'for (const c of ["ab", "c\\nde", "f\\r\\ng", "\\n\\nh", "i"]) p.write(c);\n'
                'console.log(JSON.stringify(out));\n'
                'p.end();\n'
                'console.log(JSON.stringify(out));\n'
                'p.end();\n'
                'console.log(out.length);\n'
                'const q = [];\n'
                'const p2 = createLineParser((l) => q.push(l));\n'
                'p2.write("только\\n"); p2.end();\n'
                'console.log(JSON.stringify(q));\n',
      'hint': 'Держите буфер необработанного остатка и ищите в нём перевод строки.',
      'expected': ['["abc","def","g",""]', '["abc","def","g","","hi"]', '5', '["только"]']},
     {'id': 'j2-utf8',
      'mode': 'js',
      'title': 'UTF-8 вручную',
      'statement': 'Напишите функции utf8Encode(str) → массив байтов и utf8Decode(bytes) → строка (по '
                   'правилам UTF-8: 1–4 байта на символ; кодовые точки получайте через codePointAt и '
                   'String.fromCodePoint). TextEncoder, TextDecoder и Buffer использовать нельзя.',
      'starter': 'function utf8Encode(str) {\n}\nfunction utf8Decode(bytes) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'for (const s of ["", "a", "Привет", "€", "😀x", "Aя€😀"]) {\n'
                '  const b = utf8Encode(s);\n'
                '  console.log(JSON.stringify(b), utf8Decode(b) === s, b.length === Buffer.byteLength(s));\n'
                '}\n'
                'console.log(__count("TextE" + "ncoder") + __count("TextD" + "ecoder") + __count("Buf" + '
                '"fer"));\n',
      'hint': 'Число байт определяет первый байт: 0xxxxxxx, 110xxxxx, 1110xxxx, 11110xxx.',
      'expected': ['[] true true',
                   '[97] true true',
                   '[208,159,209,128,208,184,208,178,208,181,209,130] true true',
                   '[226,130,172] true true',
                   '[240,159,152,128,120] true true',
                   '[65,209,143,226,130,172,240,159,152,128] true true',
                   '0']},
     {'id': 'j2-base64',
      'mode': 'js',
      'title': 'Base64 вручную',
      'statement': 'Напишите функции base64Encode(bytes) (массив байтов 0–255 → строка с «=» дополнением) и '
                   'base64Decode(str) → массив байтов. btoa, atob и Buffer использовать нельзя.',
      'starter': 'function base64Encode(bytes) {\n}\nfunction base64Decode(str) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'const enc = (s) => [...Buffer.from(s)];\n'
                'for (const s of ["", "f", "fo", "foo", "foob", "Man", "привет"]) {\n'
                '  const e = base64Encode(enc(s));\n'
                '  console.log(JSON.stringify(e), e === Buffer.from(s).toString("base64"), '
                'JSON.stringify(base64Decode(e)) === JSON.stringify(enc(s)));\n'
                '}\n'
                'console.log(__count("bt" + "oa(") + __count("at" + "ob("));\n',
      'hint': 'Три байта = 24 бита = четыре группы по 6 бит; неполную тройку дополняют «=».',
      'expected': ['"" true true',
                   '"Zg==" true true',
                   '"Zm8=" true true',
                   '"Zm9v" true true',
                   '"Zm9vYg==" true true',
                   '"TWFu" true true',
                   '"0L/RgNC40LLQtdGC" true true',
                   '0']},
     {'id': 'j2-pipeline',
      'mode': 'js',
      'title': 'Конвейер преобразований (как stream.pipeline)',
      'statement': 'Напишите функцию pipeline(source, ...transforms): source — итерируемый объект, каждый '
                   'transform — генератор-функция, принимающая итерируемый объект и возвращающая '
                   'итерируемый; pipeline возвращает итератор-результат цепочки source → t1 → t2 → … '
                   '(ленивый: пока не потребуются значения, ничего не вычисляется).',
      'starter': 'function pipeline(source, ...transforms) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'let pulled = 0;\n'
                'function* nums() { for (let i = 1; i <= 1000000; i++) { pulled++; yield i; } }\n'
                'const map = (f) => function* (it) { for (const x of it) yield f(x); };\n'
                'const filter = (p) => function* (it) { for (const x of it) if (p(x)) yield x; };\n'
                'const take = (n) => function* (it) { if (n <= 0) return; let i = 0; for (const x of it) { '
                'yield x; if (++i >= n) return; } };\n'
                'const r = pipeline(nums(), map((x) => x * x), filter((x) => x % 2 === 1), take(4));\n'
                'console.log(pulled);\n'
                'console.log([...r].join());\n'
                'console.log(pulled);\n'
                'console.log([...pipeline([1, 2, 3])].join());\n'
                'console.log([...pipeline("abc", map((c) => c.toUpperCase()))].join(""));\n',
      'hint': 'Каждая стадия принимает результат предыдущей: cur = t(cur).',
      'expected': ['0', '1,9,25,49', '7', '1,2,3', 'ABC']},
     {'id': 'j2-parse-args',
      'mode': 'js',
      'title': 'Разбор аргументов командной строки',
      'statement': 'Напишите функцию parseArgs(argv): argv — массив строк (как process.argv.slice(2)). '
                   'Результат { _: [позиционные], …опции }. «--name=value» и «--name value» задают значение '
                   '(строка), «--flag» без значения — true, «--no-flag» — false, «-abc» — три флага a, b, c '
                   'со значением true; «--» — всё после неё позиционное. Значение «--name value» берётся '
                   'только если следующий элемент не начинается с «-».',
      'starter': 'function parseArgs(argv) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(parseArgs(["build", "--out=dist", "--minify", "-vq", "src"])));\n'
                'console.log(JSON.stringify(parseArgs(["--port", "8080", "--no-color", "file.js"])));\n'
                'console.log(JSON.stringify(parseArgs(["--name", "--flag"])));\n'
                'console.log(JSON.stringify(parseArgs(["a", "--", "--not-an-option", "-x"])));\n'
                'console.log(JSON.stringify(parseArgs([])));\n',
      'hint': 'Обходите argv по индексу: значение «--name value» съедает следующий элемент.',
      'expected': ['{"_":["build","src"],"out":"dist","minify":true,"v":true,"q":true}',
                   '{"_":["file.js"],"port":"8080","color":false}',
                   '{"_":[],"name":true,"flag":true}',
                   '{"_":["a","--not-an-option","-x"]}',
                   '{"_":[]}']},
     {'id': 'j2-load-env',
      'mode': 'js',
      'title': 'Разбор .env',
      'statement': 'Напишите функцию loadEnv(text): строки «KEY=VALUE»; пустые строки и строки, начинающиеся '
                   'с «#», пропускаются; пробелы вокруг ключа и значения обрезаются; значение в одинарных '
                   'или двойных кавычках — без кавычек (внутри кавычек «#» не комментарий); у значения без '
                   'кавычек комментарий после « #» отбрасывается; в двойных кавычках «\\n» превращается в '
                   'перевод строки. Повторный ключ — последнее значение.',
      'starter': 'function loadEnv(text) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const t = String.raw`# конфиг\n'
                'PORT=8080\n'
                'HOST = localhost   # хост\n'
                'NAME="Ада # Лавлейс"\n'
                'MSG="строка1\\nстрока2"\n'
                "RAW='без \\n замены'\n"
                '\n'
                'EMPTY=\n'
                'PORT=9090\n'
                'bad line`;\n'
                'console.log(JSON.stringify(loadEnv(t)));\n',
      'hint': 'Сначала проверьте кавычки, и только если их нет — отбрасывайте комментарий.',
      'expected': ['{"PORT":"9090","HOST":"localhost","NAME":"Ада # '
                   'Лавлейс","MSG":"строка1\\nстрока2","RAW":"без \\\\n замены","EMPTY":""}']},
     {'id': 'j2-three-way-merge',
      'mode': 'js',
      'title': 'Трёхстороннее слияние JSON',
      'statement': 'Форки сливаются так же, как правки: напишите функцию merge3(base, a, b) для плоских '
                   'объектов: для каждого ключа, если a и b равны — берётся общее значение; если изменила '
                   '(или удалила) только одна сторона — берётся её значение; если обе изменили по-разному — '
                   'конфликт. Верните { merged, conflicts } (conflicts — отсортированный массив ключей; в '
                   'merged конфликтный ключ получает значение из a). Удаление — отсутствие ключа.',
      'starter': 'function merge3(base, a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const base = { name: "node", v: 1, lic: "MIT", old: true };\n'
                'console.log(JSON.stringify(merge3(base, { ...base, v: 2 }, { ...base, lic: "ISC" })));\n'
                'console.log(JSON.stringify(merge3(base, { ...base, v: 2 }, { ...base, v: 3 })));\n'
                'console.log(JSON.stringify(merge3(base, { name: "node", v: 1, lic: "MIT" }, { ...base, v: 5 '
                '})));\n'
                'console.log(JSON.stringify(merge3({}, { x: 1 }, { y: 2 })));\n'
                'console.log(JSON.stringify(merge3({}, { x: 1 }, { x: 1 })));\n'
                'console.log(JSON.stringify(merge3({ k: 1 }, {}, {})));\n'
                'console.log(JSON.stringify(merge3({ k: 1 }, {}, { k: 2 })));\n',
      'hint': 'Для каждого ключа сравните a с base и b с base: изменила ли сторона значение.',
      'expected': ['{"merged":{"name":"node","v":2,"lic":"ISC","old":true},"conflicts":[]}',
                   '{"merged":{"name":"node","v":2,"lic":"MIT","old":true},"conflicts":["v"]}',
                   '{"merged":{"name":"node","v":5,"lic":"MIT"},"conflicts":[]}',
                   '{"merged":{"x":1,"y":2},"conflicts":[]}',
                   '{"merged":{"x":1},"conflicts":[]}',
                   '{"merged":{},"conflicts":[]}',
                   '{"merged":{},"conflicts":["k"]}']},
     {'id': 'j2-common-ancestor',
      'mode': 'js',
      'title': 'Общий предок коммитов',
      'statement': 'История проекта — граф коммитов: { id: [родители] }. Напишите функцию '
                   'commonAncestor(graph, x, y): ближайший общий предок двух коммитов (сам коммит считается '
                   'своим предком): среди общих предков — тот, из которого нельзя дойти до другого общего '
                   'предка; если таких несколько — лексикографически наименьший id; если общих нет — null. '
                   'Это та точка, от которой разошлись Node.js и io.js.',
      'starter': 'function commonAncestor(graph, x, y) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const g = { m3: ["m2"], m2: ["m1"], m1: [], n1: ["m2"], n2: ["n1"], i1: ["m2"], i2: ["i1"], '
                'merge: ["n2", "i2"], solo: [] };\n'
                'console.log(commonAncestor(g, "n2", "i2"));\n'
                'console.log(commonAncestor(g, "m3", "n2"));\n'
                'console.log(commonAncestor(g, "merge", "i1"));\n'
                'console.log(commonAncestor(g, "n1", "n1"));\n'
                'console.log(commonAncestor(g, "solo", "m1"));\n'
                'console.log(commonAncestor({ a: [], b: ["a"], c: ["a"], d: ["b", "c"], e: ["b", "c"] }, '
                '"d", "e"));\n',
      'hint': 'Предки каждого коммита — обход графа; «ближайший» — общий предок, не являющийся предком '
              'другого общего.',
      'expected': ['m2', 'm2', 'i1', 'n1', 'null', 'b']},
     {'id': 'j2-next-version',
      'mode': 'js',
      'title': 'Следующая версия по сообщениям коммитов',
      'statement': 'Напишите функцию nextVersion(current, commits): commits — массив строк-сообщений '
                   '(Conventional Commits). Если есть сообщение с «!» после типа («feat!: …») или строка '
                   '«BREAKING CHANGE» — повышается major; иначе если есть «feat» — minor; иначе если есть '
                   '«fix» (или «perf») — patch; иначе версия не меняется. Для версий 0.x «major» '
                   'превращается в minor, а «minor» — в patch (так принято до версии 1.0).',
      'starter': 'function nextVersion(current, commits) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(nextVersion("1.2.3", ["fix: опечатка", "docs: readme"]));\n'
                'console.log(nextVersion("1.2.3", ["fix: a", "feat(api): b"]));\n'
                'console.log(nextVersion("1.2.3", ["feat!: удалён старый API"]));\n'
                'console.log(nextVersion("1.2.3", ["chore: x", "feat: y\\n\\nBREAKING CHANGE: z"]));\n'
                'console.log(nextVersion("1.2.3", ["docs: x", "style: y"]));\n'
                'console.log(nextVersion("0.4.1", ["feat: новая", "fix: старая"]));\n'
                'console.log(nextVersion("0.4.1", ["feat!: ломаем"]));\n'
                'console.log(nextVersion("0.4.1", ["perf: быстрее"]));\n',
      'hint': 'Найдите наивысший уровень среди коммитов, затем примените его с поправкой для 0.x.',
      'expected': ['1.2.4', '1.3.0', '2.0.0', '2.0.0', '1.2.3', '0.4.2', '0.5.0', '0.4.2']},
     {'id': 'j2-install-plan',
      'mode': 'js',
      'title': 'Что поставит npm',
      'statement': 'Реестр задан так: { имя: { версия: { dependencies: { имя: диапазон } } } } (версии вида '
                   '«1.2.3»). Напишите функцию installPlan(registry, deps): deps — { имя: диапазон }; для '
                   'каждой зависимости (рекурсивно) выбирается наибольшая версия, подходящая под диапазон '
                   '(«1.2.3», «^1.2.3», «~1.2.3», «*»). Верните объект «имя → версия» (если одно имя нужно в '
                   'двух версиях, берите версию, подходящую под все диапазоны, а при невозможности — '
                   'Error("конфликт: <имя>")); если подходящей версии нет — Error("нет версии: '
                   '<имя>@<диапазон>").',
      'starter': 'function installPlan(registry, deps) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const reg = {\n'
                '  express: { "4.17.1": { dependencies: { qs: "^6.5.0", cookie: "0.4.0" } }, "4.18.2": { '
                'dependencies: { qs: "^6.11.0", cookie: "~0.5.0" } } },\n'
                '  qs: { "6.5.2": {}, "6.9.0": {}, "6.11.2": {}, "7.0.0": {} },\n'
                '  cookie: { "0.4.0": {}, "0.5.0": {}, "0.5.1": {}, "0.6.0": {} },\n'
                '  lodash: { "4.17.20": {}, "4.17.21": {} },\n'
                '};\n'
                'console.log(JSON.stringify(installPlan(reg, { express: "^4.17.1" })));\n'
                'console.log(JSON.stringify(installPlan(reg, { express: "4.17.1", lodash: "*" })));\n'
                'console.log(JSON.stringify(installPlan(reg, { express: "~4.18.0", qs: "^6.5.0" })));\n'
                'try { installPlan(reg, { express: "^5.0.0" }); } catch (e) { console.log(e.message); }\n'
                'try { installPlan(reg, { express: "4.18.2", cookie: "0.4.0" }); } catch (e) { '
                'console.log(e.message); }\n'
                'try { installPlan(reg, { react: "*" }); } catch (e) { console.log(e.message); }\n',
      'hint': 'Накапливайте диапазоны по имени и выбирайте наибольшую версию, подходящую под все; затем '
              'обходите её зависимости.',
      'expected': ['{"cookie":"0.5.1","express":"4.18.2","qs":"6.11.2"}',
                   '{"cookie":"0.4.0","express":"4.17.1","lodash":"4.17.21","qs":"6.11.2"}',
                   '{"cookie":"0.5.1","express":"4.18.2","qs":"6.11.2"}',
                   'нет версии: express@^5.0.0',
                   'конфликт: cookie',
                   'нет версии: react@*']},
     {'id': 'j2-diff-deps',
      'mode': 'js',
      'title': 'Различие двух package.json',
      'statement': 'Напишите функцию diffDeps(oldDeps, newDeps): объекты «имя → диапазон». Верните { added: '
                   '[имена], removed: [имена], changed: [[имя, было, стало]] } — все списки отсортированы по '
                   'имени; неизменённые зависимости не включаются.',
      'starter': 'function diffDeps(oldDeps, newDeps) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(diffDeps({ express: "^4.17.1", lodash: "4.17.20", qs: "^6.5.0" '
                '}, { express: "^4.18.2", qs: "^6.5.0", cors: "^2.8.5", zod: "^3.0.0" })));\n'
                'console.log(JSON.stringify(diffDeps({}, {})));\n'
                'console.log(JSON.stringify(diffDeps({ a: "1" }, { a: "1" })));\n'
                'console.log(JSON.stringify(diffDeps({ a: "1" }, {})));\n',
      'hint': 'Три прохода: что есть только в новом, только в старом, и у общих — различие значений.',
      'expected': ['{"added":["cors","zod"],"removed":["lodash"],"changed":[["express","^4.17.1","^4.18.2"]]}',
                   '{"added":[],"removed":[],"changed":[]}',
                   '{"added":[],"removed":[],"changed":[]}',
                   '{"added":[],"removed":["a"],"changed":[]}']},
     {'id': 'j2-event-loop-sim',
      'mode': 'js',
      'title': 'Модель цикла событий',
      'statement': 'Напишите функцию simulate(ops): ops — массив операций программы по порядку: { type: '
                   '"sync" | "nextTick" | "microtask" | "timeout" | "immediate", label, delay? }. Верните '
                   'массив label в порядке выполнения по правилам Node.js: сначала все sync (в порядке '
                   'следования); затем очередь nextTick; затем очередь microtask (после каждой из них снова '
                   'сначала nextTick, но для простоты считайте очереди независимыми: все nextTick, затем все '
                   'microtask); затем таймеры по возрастанию delay (при равенстве — по порядку создания; '
                   'delay по умолчанию 0); затем все immediate.',
      'starter': 'function simulate(ops) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const t = (type, label, delay) => ({ type, label, delay });\n'
                'console.log(simulate([t("timeout", "T0", 0), t("immediate", "I"), t("microtask", "M"), '
                't("nextTick", "N"), t("sync", "S1"), t("sync", "S2")]).join(" "));\n'
                'console.log(simulate([t("timeout", "T50", 50), t("timeout", "T10", 10), t("timeout", '
                '"T10b", 10), t("timeout", "T0")]).join(" "));\n'
                'console.log(simulate([t("microtask", "M1"), t("nextTick", "N1"), t("microtask", "M2"), '
                't("nextTick", "N2")]).join(" "));\n'
                'console.log(JSON.stringify(simulate([])));\n',
      'hint': 'Вывод — конкатенация очередей: sync, nextTick, microtask, timeout (отсортированные), '
              'immediate.',
      'expected': ['S1 S2 N M T0 I', 'T0 T10 T10b T50', 'N1 N2 M1 M2', '[]']}]}
