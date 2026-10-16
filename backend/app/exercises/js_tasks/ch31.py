"""Задачи книги «Современный Frontend»: глава 31."""

TASKS: dict[int, list[dict]] = {31: [{'id': 'j31-parse-env',
  'mode': 'js',
  'title': 'Разбор .env',
  'statement': 'Напишите parseEnv(text) → объект. Строки вида KEY=VALUE; пустые строки и строки, '
               'начинающиеся с «#», пропускаются; допустим префикс «export » перед ключом; ключ — '
               '/^[A-Za-z_][A-Za-z0-9_]*$/ после обрезки пробелов (иначе строка пропускается); '
               'пробелы вокруг «=» допустимы. Значение: если начинается с «"» или «\'» — до парной '
               'кавычки на этой же строке (для двойных кавычек «\\n» превращается в перевод '
               'строки; остаток после кавычки игнорируется); если закрывающей кавычки нет — '
               'значение берётся как есть без первой кавычки (обрезанное справа). Без кавычек '
               'значение обрезается по первому « #» (пробел и решётка — комментарий) и очищается '
               'от пробелов. Повторный ключ перезаписывает прежний.',
  'starter': 'function parseEnv(text) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const text = [\n'
            '  "# комментарий", "", "API_URL=/api", "export MODE = production ", "TITLE=\\"My '
            'App\\" # not a comment", "MULTI=\\"line1\\\\nline2\\"",\n'
            '  "SINGLE=\'a #b \\\\n\'", "PLAIN=value # trailing comment", "EMPTY=", "bad key=1", '
            '"1BAD=2", "DUP=1", "DUP=2", "UNCLOSED=\\"abc  ", "HASH=a#b",\n'
            '].join("\\n");\n'
            'console.log(JSON.stringify(parseEnv(text), null, 1));\n'
            'console.log(JSON.stringify(parseEnv("")), JSON.stringify(parseEnv("\\n# '
            'only\\n")));\n',
  'hint': 'Разбейте на строки; для значения проверьте первый символ; регулярное выражение для '
          'ключа.',
  'expected': ['{',
               ' "API_URL": "/api",',
               ' "MODE": "production",',
               ' "TITLE": "My App",',
               ' "MULTI": "line1\\nline2",',
               ' "SINGLE": "a #b \\\\n",',
               ' "PLAIN": "value",',
               ' "EMPTY": "",',
               ' "DUP": "2",',
               ' "UNCLOSED": "abc",',
               ' "HASH": "a#b"',
               '}',
               '{} {}']},
 {'id': 'j31-replace-env',
  'mode': 'js',
  'title': 'Подстановка import.meta.env',
  'statement': "Напишите replaceEnv(source, env, { prefix = 'VITE_', mode = 'development' } = {}): "
               'заменяет в тексте все выражения «import.meta.env.ИМЯ» (ИМЯ — [A-Za-z_]\\w*). '
               "Встроенные: MODE → JSON-строка режима, DEV → true, если mode !== 'production', "
               'PROD → противоположное. Имя с префиксом prefix и значением в env → '
               'JSON.stringify(значение). Всё остальное (нет префикса, нет в env, неизвестное) → '
               'undefined (слово undefined). Секреты не должны утекать: имя без префикса всегда '
               'даёт undefined, даже если оно есть в env.',
  'starter': 'function replaceEnv(source, env, opts = {}) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const env = { VITE_API: "/api", VITE_FLAG: "on", DB_PASSWORD: "secret", VITE_EMPTY: '
            '"" };\n'
            'const src = "const a = import.meta.env.VITE_API; const b = '
            'import.meta.env.DB_PASSWORD; const c = import.meta.env.VITE_MISSING;\\nif '
            '(import.meta.env.DEV) log(import.meta.env.MODE, import.meta.env.PROD, '
            'import.meta.env.VITE_EMPTY);";\n'
            'console.log(replaceEnv(src, env));\n'
            'console.log(replaceEnv(src, env, { mode: "production" }));\n'
            'console.log(replaceEnv("x = import.meta.env.APP_NAME", { APP_NAME: "z", VITE_A: "1" '
            '}, { prefix: "APP_" }));\n'
            'console.log(replaceEnv("import.meta.environment import.meta.env", env));\n',
  'hint': 'Одна replace с функцией; сначала встроенные имена, затем префикс.',
  'expected': ['const a = "/api"; const b = undefined; const c = undefined;',
               'if (true) log("development", false, "");',
               'const a = "/api"; const b = undefined; const c = undefined;',
               'if (false) log("production", true, "");',
               'x = "z"',
               'import.meta.environment import.meta.env']},
 {'id': 'j31-alias',
  'mode': 'js',
  'title': 'Алиасы путей',
  'statement': 'Напишите resolveAlias(aliases, spec): aliases — { псевдоним: цель }. Псевдоним '
               'подходит, если spec равен ему или начинается с псевдоним + «/». Побеждает самый '
               'длинный подходящий псевдоним (при равной длине невозможно — ключи уникальны). '
               'Результат — цель + остаток spec после псевдонима (цель без завершающего «/» '
               'склеивается с остатком, начинающимся с «/»). Если ничего не подошло — spec без '
               'изменений. Псевдонимы, оканчивающиеся на «$», требуют точного совпадения (сам «$» '
               'в сравнении не участвует: «react$» подходит только для «react»).',
  'starter': 'function resolveAlias(aliases, spec) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const aliases = { "@": "/src", "@ui": "/src/components/ui", "react$": '
            '"/vendor/react-lite.js", "utils/": "/lib/utils/", "~assets": "/static" };\n'
            'for (const s of ["@/store/index.js", "@ui/Button", "@ui", "@", "@uix/y", "react", '
            '"react/jsx-runtime", "utils/a", "utils", "~assets/logo.svg", "lodash"]) '
            'console.log(s, "→", resolveAlias(aliases, s));\n',
  'hint': 'Переберите ключи, отберите подходящие, возьмите самый длинный.',
  'expected': ['@/store/index.js → /src/store/index.js',
               '@ui/Button → /src/components/ui/Button',
               '@ui → /src/components/ui',
               '@ → /src',
               '@uix/y → @uix/y',
               'react → /vendor/react-lite.js',
               'react/jsx-runtime → react/jsx-runtime',
               'utils/a → /lib/utils/a',
               'utils → utils',
               '~assets/logo.svg → /static/logo.svg',
               'lodash → lodash']},
 {'id': 'j31-proxy',
  'mode': 'js',
  'title': 'Прокси dev-сервера',
  'statement': 'Напишите matchProxy(rules, path): rules — массив [ключ, { target, rewrite? }]. '
               'Ключ — префикс пути («/api» подходит для «/api» и «/api/...»; «/api/» — только для '
               'путей, начинающихся с «/api/») или регулярное выражение, если начинается с «^» '
               '(new RegExp(ключ).test(path)). Путь без query и hash для сопоставления, но в '
               'результат он попадает целиком (с query). Первое подошедшее правило побеждает. '
               'Результат — target без завершающего «/» + (rewrite ? rewrite(путь) : путь); '
               'rewrite получает полный путь с query. Нет правила — null.',
  'starter': 'function matchProxy(rules, path) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const rules = [\n'
            '  ["/api/v2/", { target: "http://localhost:9000/" }],\n'
            '  ["/api", { target: "http://localhost:8000", rewrite: (p) => p.replace(/^\\/api/, '
            '"") }],\n'
            '  ["^/ws(/|$)", { target: "ws://localhost:7000/" }],\n'
            '  ["/static", { target: "http://cdn.local" }],\n'
            '];\n'
            'for (const p of ["/api", "/api/users?id=1", "/api/v2/items", "/apix", "/ws", '
            '"/ws/chat#x", "/wsx", "/static/a.png", "/other", "/api/v2"]) console.log(p, "→", '
            'matchProxy(rules, p));\n',
  'hint': 'Отделите path от query/hash для сравнения; обрежьте слэш у target.',
  'expected': ['/api → http://localhost:8000',
               '/api/users?id=1 → http://localhost:8000/users?id=1',
               '/api/v2/items → http://localhost:9000/api/v2/items',
               '/apix → null',
               '/ws → ws://localhost:7000/ws',
               '/ws/chat#x → ws://localhost:7000/ws/chat#x',
               '/wsx → null',
               '/static/a.png → http://cdn.local/static/a.png',
               '/other → null',
               '/api/v2 → http://localhost:8000/v2']},
 {'id': 'j31-semver-range',
  'mode': 'js',
  'title': 'Диапазоны версий',
  'statement': 'Напишите satisfies(version, range). Версии — «M.m.p» без предрелизов. Диапазон: '
               'объединение через «||» (достаточно одного подходящего), в каждой части — условия '
               'через пробелы (все должны выполняться). Условия: «*» или пусто — любая версия; '
               '«=X.Y.Z» или «X.Y.Z» — равна; «>», «>=», «<», «<=» с версией; «^X.Y.Z» — от X.Y.Z '
               'до следующего «несовместимого»: при X>0 — <(X+1).0.0; при X=0, Y>0 — <0.(Y+1).0; '
               'при X=0,Y=0 — <0.0.(Z+1); «~X.Y.Z» — от X.Y.Z до <X.(Y+1).0. Недостающие части '
               '(«1.2», «1») считаются нулями.',
  'starter': 'function satisfies(version, range) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (v, r) => console.log(v, JSON.stringify(r), satisfies(v, r));\n'
            't("1.2.3", "^1.2.0"); t("1.9.9", "^1.2.0"); t("2.0.0", "^1.2.0"); t("1.1.9", '
            '"^1.2.0"); t("0.2.5", "^0.2.3"); t("0.3.0", "^0.2.3"); t("0.0.3", "^0.0.3"); '
            't("0.0.4", "^0.0.3");\n'
            't("1.2.9", "~1.2.3"); t("1.3.0", "~1.2.3"); t("1.2.2", "~1.2.3");\n'
            't("1.5.0", ">=1.2.0 <2.0.0"); t("2.0.0", ">=1.2.0 <2.0.0"); t("1.0.0", ">1.0.0"); '
            't("1.0.1", ">1.0.0"); t("1.0.0", "<=1.0.0");\n'
            't("3.1.0", "^1.0.0 || ^3.0.0"); t("2.1.0", "^1.0.0 || ^3.0.0"); t("5.5.5", "*"); '
            't("1.2.3", ""); t("1.2.3", "1.2.3"); t("1.2.3", "=1.2.4"); t("1.2.0", "1.2"); '
            't("1.0.0", "^1");\n',
  'hint': 'Функция cmp(a, b) по числам; каждое условие превратите в пару проверок.',
  'expected': ['1.2.3 "^1.2.0" true',
               '1.9.9 "^1.2.0" true',
               '2.0.0 "^1.2.0" false',
               '1.1.9 "^1.2.0" false',
               '0.2.5 "^0.2.3" true',
               '0.3.0 "^0.2.3" false',
               '0.0.3 "^0.0.3" true',
               '0.0.4 "^0.0.3" false',
               '1.2.9 "~1.2.3" true',
               '1.3.0 "~1.2.3" false',
               '1.2.2 "~1.2.3" false',
               '1.5.0 ">=1.2.0 <2.0.0" true',
               '2.0.0 ">=1.2.0 <2.0.0" false',
               '1.0.0 ">1.0.0" false',
               '1.0.1 ">1.0.0" true',
               '1.0.0 "<=1.0.0" true',
               '3.1.0 "^1.0.0 || ^3.0.0" true',
               '2.1.0 "^1.0.0 || ^3.0.0" false',
               '5.5.5 "*" true',
               '1.2.3 "" true',
               '1.2.3 "1.2.3" true',
               '1.2.3 "=1.2.4" false',
               '1.2.0 "1.2" true',
               '1.0.0 "^1" true']},
 {'id': 'j31-build-order',
  'mode': 'js',
  'title': 'Порядок модулей в бандле',
  'statement': 'Напишите buildOrder(graph): graph — { модуль: [зависимости] }. Верните массив всех '
               'модулей в порядке, где зависимости идут раньше зависимых. Порядок детерминирован: '
               'обход в глубину по ключам графа в порядке объявления, зависимости — в порядке '
               'списка. Модули, встречающиеся только как зависимости (нет среди ключей), — листья '
               "и тоже попадают в результат. Цикл — Error('Cycle: a -> b -> a') (путь от первого "
               'модуля цикла до его повторения).',
  'starter': 'function buildOrder(graph) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const g = { main: ["app", "utils"], app: ["store", "router"], store: ["utils"], '
            'router: ["utils", "history"], utils: [], extra: ["lib"] };\n'
            'console.log(buildOrder(g).join(" "));\n'
            'console.log(JSON.stringify(buildOrder({})), buildOrder({ a: ["b"], b: [] }).join(" '
            '"), buildOrder({ a: ["a_dep"] }).join(" "));\n'
            'const bad = (g) => { try { buildOrder(g); } catch (e) { console.log(e.message); } };\n'
            'bad({ a: ["b"], b: ["c"], c: ["a"] }); bad({ x: ["y"], y: ["z"], z: ["y"] }); bad({ '
            's: ["s"] });\n',
  'hint': 'DFS с состояниями visiting/done и стеком пути.',
  'expected': ['utils store history router app main lib extra',
               '[] b a a_dep a',
               'Cycle: a -> b -> c -> a',
               'Cycle: y -> z -> y',
               'Cycle: s -> s']},
 {'id': 'j31-tree-shake',
  'mode': 'js',
  'title': 'Tree shaking',
  'statement': 'Напишите shakeExports(modules, roots): modules — { файл: { экспорт: [ссылки] } }, '
               'где ссылка «файл#экспорт» — другой экспорт, который использует данный. roots — '
               'массив ссылок, нужных точке входа. Верните { kept, dropped }: kept — '
               'отсортированные по алфавиту ссылки всех достижимых экспортов (включая roots), '
               'dropped — отсортированные ссылки остальных экспортов всех модулей. Неизвестная '
               "ссылка (нет такого файла или экспорта) — Error('Unknown export: ссылка'). Ссылка "
               'на себя или циклы допустимы.',
  'starter': 'function shakeExports(modules, roots) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const modules = {\n'
            '  "ui.js": { Button: ["util.js#cls"], Modal: ["ui.js#Button", "util.js#cls", '
            '"dom.js#portal"], Tooltip: [] },\n'
            '  "util.js": { cls: [], debounce: [], unused: ["util.js#debounce"] },\n'
            '  "dom.js": { portal: [], query: ["util.js#cls"] },\n'
            '};\n'
            'const show = (r) => console.log(JSON.stringify(shakeExports(modules, r)));\n'
            'show(["ui.js#Button"]); show(["ui.js#Modal"]); show([]); show(["util.js#unused", '
            '"dom.js#query"]);\n'
            'for (const r of [["ui.js#Nope"], ["none.js#x"]]) { try { shakeExports(modules, r); } '
            'catch (e) { console.log(e.message); } }\n'
            'try { shakeExports({ "a.js": { x: ["a.js#y"] } }, ["a.js#x"]); } catch (e) { '
            'console.log(e.message); }\n'
            'console.log(JSON.stringify(shakeExports({ "a.js": { x: ["a.js#y"], y: ["a.js#x"] } }, '
            '["a.js#x"])));\n',
  'hint': 'Обход в глубину по ссылкам; множество всех ссылок строится из modules.',
  'expected': ['{"kept":["ui.js#Button","util.js#cls"],"dropped":["dom.js#portal","dom.js#query","ui.js#Modal","ui.js#Tooltip","util.js#debounce","util.js#unused"]}',
               '{"kept":["dom.js#portal","ui.js#Button","ui.js#Modal","util.js#cls"],"dropped":["dom.js#query","ui.js#Tooltip","util.js#debounce","util.js#unused"]}',
               '{"kept":[],"dropped":["dom.js#portal","dom.js#query","ui.js#Button","ui.js#Modal","ui.js#Tooltip","util.js#cls","util.js#debounce","util.js#unused"]}',
               '{"kept":["dom.js#query","util.js#cls","util.js#debounce","util.js#unused"],"dropped":["dom.js#portal","ui.js#Button","ui.js#Modal","ui.js#Tooltip"]}',
               'Unknown export: ui.js#Nope',
               'Unknown export: none.js#x',
               'Unknown export: a.js#y',
               '{"kept":["a.js#x","a.js#y"],"dropped":[]}']},
 {'id': 'j31-content-hash',
  'mode': 'js',
  'title': 'Хеши в именах файлов',
  'statement': 'Функция fnv1a(str) → 8 hex-символов уже есть. Напишите hashedName(name, content, '
               'len = 8): вставляет первые len символов fnv1a(content) перед последним '
               'расширением: «app.js» → «app.<хеш>.js», «a.min.js» → «a.min.<хеш>.js»; без '
               'расширения (нет точки после последнего «/», либо файл начинается с точки и точки '
               'больше нет) — «name.<хеш>». Каталоги сохраняются («assets/app.css» → '
               '«assets/app.<хеш>.css»). И напишите buildManifest(files): files — { имя: '
               'содержимое } → { имя: hashedName(...) } для всех, кроме index.html (он остаётся '
               'без хеша).',
  'starter': '// Готово: хеш FNV-1a (не изменяйте)\n'
             'function fnv1a(str) {\n'
             '  let h = 0x811c9dc5;\n'
             '  for (const b of new TextEncoder().encode(str)) { h ^= b; h = Math.imul(h, '
             '0x01000193) >>> 0; }\n'
             '  return h.toString(16).padStart(8, "0");\n'
             '}\n'
             'function hashedName(name, content, len = 8) {\n'
             '}\n'
             'function buildManifest(files) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(fnv1a(""), fnv1a("a"), fnv1a("hello"));\n'
            'console.log(hashedName("app.js", "console.log(1)"), hashedName("assets/app.css", '
            '"a{}"), hashedName("a.min.js", "x"), hashedName("LICENSE", "mit"), hashedName(".env", '
            '"x"), hashedName("dir.v2/file", "y"), hashedName("app.js", "console.log(1)", 4));\n'
            'console.log(hashedName("app.js", "A") === hashedName("lib.js", "A").replace("lib", '
            '"app"), hashedName("app.js", "A") === hashedName("app.js", "B"));\n'
            'console.log(JSON.stringify(buildManifest({ "index.html": "<html>", "main.js": "m", '
            '"assets/style.css": "s{}" }), null, 1));\n',
  'hint': "lastIndexOf('.') после последнего '/'; точка в позиции 0 имени — не расширение.",
  'expected': ['811c9dc5 e40c292c 4f9f2cab',
               'app.acd116d0.js assets/app.245dbf18.css a.min.fd0c5087.js LICENSE.d38f5515 '
               '.env.fd0c5087 dir.v2/file.fc0c4ef4 app.acd1.js',
               'true false',
               '{',
               ' "index.html": "index.html",',
               ' "main.js": "main.e80c2f78.js",',
               ' "assets/style.css": "assets/style.d152a4f2.css"',
               '}']},
 {'id': 'j31-chunks',
  'mode': 'js',
  'title': 'Разбиение на чанки',
  'statement': 'Напишите splitChunks(graph, entry): graph — { модуль: { static: [...], dynamic: '
               '[...] } } (поля могут отсутствовать). Корни чанков: entry и каждая цель '
               'динамического импорта, достижимая из entry любыми рёбрами (порядок обнаружения — '
               'обход в ширину, статические рёбра раньше динамических). Для каждого модуля найдите '
               'множество корней, из которых он достижим по статическим рёбрам. Если в множестве '
               'есть entry — модуль в чанке «entry»; иначе если корень один — в чанке с именем '
               'этого корня; иначе — в общем чанке «shared:» + корни через «+» (в порядке корней). '
               'Результат — массив { name, modules } (modules по алфавиту), сначала «entry», '
               'остальные по алфавиту имён. Недостижимые из entry модули игнорируются.',
  'starter': 'function splitChunks(graph, entry) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const g = {\n'
            '  main: { static: ["router", "ui"], dynamic: ["settings", "profile"] },\n'
            '  router: { static: ["util"] }, ui: {}, util: {},\n'
            '  settings: { static: ["form", "util", "chart"], dynamic: ["export"] },\n'
            '  profile: { static: ["form", "avatar"] },\n'
            '  form: { static: ["validate"] }, validate: {}, chart: {}, avatar: {},\n'
            '  export: { static: ["chart"] },\n'
            '  orphan: { static: ["util"] },\n'
            '};\n'
            'for (const c of splitChunks(g, "main")) console.log(c.name, c.modules.join(","));\n'
            'console.log(JSON.stringify(splitChunks({ a: { static: ["b"] }, b: {} }, "a")));\n'
            'console.log(JSON.stringify(splitChunks({ a: { dynamic: ["b", "c"] }, b: { static: '
            '["d"] }, c: { static: ["d"] }, d: {} }, "a")));\n',
  'hint': 'Сначала найдите все достижимые модули и корни, затем для каждого корня обход по static.',
  'expected': ['entry main,router,ui,util',
               'export export',
               'profile avatar,profile',
               'settings settings',
               'shared:settings+export chart',
               'shared:settings+profile form,validate',
               '[{"name":"entry","modules":["a","b"]}]',
               '[{"name":"entry","modules":["a"]},{"name":"b","modules":["b"]},{"name":"c","modules":["c"]},{"name":"shared:b+c","modules":["d"]}]']},
 {'id': 'j31-minify-css',
  'mode': 'js',
  'title': 'Минификация CSS',
  'statement': 'Напишите minifyCss(css): удалите комментарии /* … */ (в том числе многострочные); '
               'схлопните любые пробельные последовательности в один пробел; уберите пробелы '
               'вокруг «{», «}», «:», «;», «,», «>»; уберите «;» непосредственно перед «}»; '
               'обрежьте края. Содержимое строк в кавычках не меняется (кавычки одинарные или '
               'двойные, без экранирования внутри). Пробел после «:» внутри строки значения тоже '
               'убирается («margin: 0 auto» → «margin:0 auto»).',
  'starter': 'function minifyCss(css) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const css = `\n'
            '/* header */\n'
            '.nav > a,\n'
            '.nav   a:hover {\n'
            '  color : #fff ;\n'
            '  margin: 0  auto;   /* center\n'
            '  multi-line */\n'
            '  font-family: "Fira  Sans" , sans-serif;\n'
            '}\n'
            '\n'
            '@media (min-width: 600px) {\n'
            '  .x { content: ";  }  /* kept */" ; }\n'
            '}\n'
            '`;\n'
            'const out = minifyCss(css);\n'
            'console.log(out);\n'
            'console.log(out.length, minifyCss("a{}"), JSON.stringify(minifyCss("  \\n  ")), '
            'minifyCss("a { b : c ; }"));\n',
  'hint': 'Разбейте текст на строки в кавычках и всё остальное — минифицируйте только остальное.',
  'expected': ['.nav>a,.nav a:hover{color:#fff;margin:0 auto;font-family:"Fira  '
               'Sans",sans-serif}@media (min-width:600px){.x{content:";  }  /* kept */"}}',
               '137 a{} "" a{b:c}']},
 {'id': 'j31-vlq',
  'mode': 'js',
  'title': 'VLQ для карт исходников',
  'statement': 'Карты исходников хранят числа в Base64 VLQ. Напишите vlqEncode(n) → строка и '
               'vlqDecode(str) → массив чисел. Кодирование: знак уходит в младший бит (v = n < 0 ? '
               '((-n) << 1) | 1 : n << 1); затем по 5 бит, начиная с младших; если остались ещё '
               'биты — устанавливается бит продолжения (32); каждая 6-битная группа кодируется '
               'алфавитом «ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/». '
               'vlqDecode разбирает строку, содержащую подряд несколько закодированных чисел.',
  'starter': 'function vlqEncode(n) {\n}\nfunction vlqDecode(str) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'for (const n of [0, 1, -1, 2, 15, 16, -16, 123, -123, 1000, 65535, -100000]) '
            'console.log(n, vlqEncode(n), vlqDecode(vlqEncode(n))[0] === n);\n'
            'const nums = [0, 0, 16, 1, 0, 4, -2, 1000];\n'
            'const enc = nums.map(vlqEncode).join("");\n'
            'console.log(enc, JSON.stringify(vlqDecode(enc)), JSON.stringify(vlqDecode("")), '
            'JSON.stringify(vlqDecode("AAgBC")));\n',
  'hint': 'Цикл do/while: digit = v & 31; v >>>= 5; если v > 0 — digit |= 32.',
  'expected': ['0 A true',
               '1 C true',
               '-1 D true',
               '2 E true',
               '15 e true',
               '16 gB true',
               '-16 hB true',
               '123 2H true',
               '-123 3H true',
               '1000 w+B true',
               '65535 +//D true',
               '-100000 hqjG true',
               'AAgBCAIFw+B [0,0,16,1,0,4,-2,1000] [] [0,0,16,1]']},
 {'id': 'j31-test-runner',
  'mode': 'js',
  'title': 'Мини-раннер тестов',
  'statement': 'Напишите createRunner(): { describe, it, beforeEach, run }. describe(name, fn) '
               'вызывает fn сразу, создавая набор; наборы вкладываются. it(name, fn) регистрирует '
               'тест (fn может быть async); it.skip(name, fn) — пропущенный. beforeEach(fn) '
               'действует на тесты своего набора и вложенных (хуки родителей — раньше хуков детей, '
               'в порядке объявления). run() (async) выполняет тесты в порядке объявления: сначала '
               'beforeEach-хуки, затем тест; исключение/отклонение в хуке или тесте — status '
               "'failed' (тест после упавшего хука не запускается). Результат { passed, failed, "
               "skipped, results } — results: [{ name: 'набор > вложенный > тест', status: "
               "'passed'|'failed'|'skipped', error?: message }]. Тест вне describe имеет имя без "
               'префикса.',
  'starter': 'function createRunner() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const { describe, it, beforeEach, run } = createRunner();\n'
            'const log = [];\n'
            'beforeEach(() => log.push("root-hook"));\n'
            'it("top-level", () => log.push("t0"));\n'
            'describe("math", () => {\n'
            '  beforeEach(() => log.push("math-hook"));\n'
            '  it("adds", () => log.push("adds"));\n'
            '  it("fails", () => { throw new Error("boom"); });\n'
            '  describe("nested", () => {\n'
            '    beforeEach(async () => { await null; log.push("nested-hook"); });\n'
            '    it("async ok", async () => { await null; log.push("async"); });\n'
            '    it("async fails", async () => { await null; throw new Error("late"); });\n'
            '    it.skip("skipped", () => log.push("never"));\n'
            '  });\n'
            '  beforeEach(() => log.push("math-hook-2"));\n'
            '});\n'
            'describe("hooks", () => {\n'
            '  beforeEach(() => { throw new Error("hook broke"); });\n'
            '  it("not run", () => log.push("never2"));\n'
            '});\n'
            'const r = await run();\n'
            'console.log(r.passed, r.failed, r.skipped);\n'
            'for (const x of r.results) console.log(x.status, x.name, x.error ?? "");\n'
            'console.log(log.join(" "));\n',
  'hint': 'Храните стек наборов при регистрации и сразу собирайте для теста список хуков (снимок '
          'на момент регистрации не годится — хуки могут объявляться после it).',
  'expected': ['3 3 1',
               'passed top-level',
               'passed math > adds',
               'failed math > fails boom',
               'passed math > nested > async ok',
               'failed math > nested > async fails late',
               'skipped math > nested > skipped',
               'failed hooks > not run hook broke',
               'root-hook t0 root-hook math-hook math-hook-2 adds root-hook math-hook math-hook-2 '
               'root-hook math-hook math-hook-2 nested-hook async root-hook math-hook math-hook-2 '
               'nested-hook root-hook']},
 {'id': 'j31-expect',
  'mode': 'js',
  'title': 'expect и проверки',
  'statement': 'Напишите expect(actual) → объект проверок: toBe (Object.is), toEqual (глубокое '
               'равенство: примитивы, массивы, простые объекты по ключам; порядок ключей не '
               'важен), toContain (элемент массива по Object.is или подстрока строки), toBeTruthy, '
               'toBeNull, toThrow(подстрока?) (actual — функция; проходит, если она бросает, и '
               'сообщение содержит подстроку, если она задана). Свойство .not инвертирует проверку '
               '(expect(x).not.toBe(y)). При провале — Error с сообщением '
               '`expect(ФАКТ)[.not].метод(АРГУМЕНТЫ)`, где ФАКТ и АРГУМЕНТЫ — JSON.stringify '
               '(undefined и функции — слово undefined/[Function]), аргументы через «, ». Для '
               'toThrow ФАКТ выводится как [Function]. Успех — возвращает undefined.',
  'starter': 'function expect(actual) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (f) => { try { f(); console.log("ok"); } catch (e) { '
            'console.log(e.message); } };\n'
            't(() => expect(1).toBe(1)); t(() => expect(1).toBe(2)); t(() => '
            'expect(NaN).toBe(NaN)); t(() => expect({}).toBe({}));\n'
            't(() => expect({ a: [1, { b: 2 }], c: "x" }).toEqual({ c: "x", a: [1, { b: 2 }] })); '
            't(() => expect({ a: 1 }).toEqual({ a: 2 })); t(() => expect([1, 2]).toEqual([1, 2, '
            '3])); t(() => expect({ a: 1 }).toEqual({ a: 1, b: undefined }));\n'
            't(() => expect([1, 2, 3]).toContain(2)); t(() => expect("hello").toContain("ell")); '
            't(() => expect([1]).toContain(5));\n'
            't(() => expect(0).toBeTruthy()); t(() => expect("x").toBeTruthy()); t(() => '
            'expect(null).toBeNull()); t(() => expect(undefined).toBeNull());\n'
            't(() => expect(() => { throw new Error("bad input"); }).toThrow()); t(() => expect(() '
            '=> { throw new Error("bad input"); }).toThrow("input")); t(() => expect(() => { throw '
            'new Error("bad"); }).toThrow("good")); t(() => expect(() => 1).toThrow());\n'
            't(() => expect(1).not.toBe(2)); t(() => expect(1).not.toBe(1)); t(() => '
            'expect([1]).not.toContain(1)); t(() => expect(() => 1).not.toThrow()); t(() => '
            'expect(null).not.toBeNull());\n',
  'hint': 'Одна функция check(name, pass, args), а not инвертирует pass; deepEqual рекурсивно.',
  'expected': ['ok',
               'expect(1).toBe(2)',
               'ok',
               'expect({}).toBe({})',
               'ok',
               'expect({"a":1}).toEqual({"a":2})',
               'expect([1,2]).toEqual([1,2,3])',
               'expect({"a":1}).toEqual({"a":1})',
               'ok',
               'ok',
               'expect([1]).toContain(5)',
               'expect(0).toBeTruthy()',
               'ok',
               'ok',
               'expect(undefined).toBeNull()',
               'ok',
               'ok',
               'expect([Function]).toThrow("good")',
               'expect([Function]).toThrow()',
               'ok',
               'expect(1).not.toBe(1)',
               'expect([1]).not.toContain(1)',
               'ok',
               'expect(null).not.toBeNull()']},
 {'id': 'j31-mock-fn',
  'mode': 'js',
  'title': 'Функция-заглушка',
  'statement': 'Напишите mockFn(impl?): возвращает функцию f с полями: f.calls — массив массивов '
               "аргументов; f.results — массив { type: 'return'|'throw', value } для каждого "
               'вызова; методы (все возвращают f): mockReturnValue(v) — постоянное возвращаемое '
               'значение, mockImplementation(fn) — постоянная реализация, '
               'mockImplementationOnce(fn) — реализация на один следующий вызов (очередь), '
               'mockClear() — очистить calls и results, mockReset() — очистить calls, results, '
               'постоянные настройки и очередь. Порядок выбора: очередь Once → '
               'mockImplementation/mockReturnValue (последняя заданная) → impl из конструктора → '
               'undefined. Вызов, бросивший исключение, записывается как throw и исключение '
               'пробрасывается.',
  'starter': 'function mockFn(impl) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const f = mockFn((x) => x * 2);\n'
            'console.log(f(2), f(5), JSON.stringify(f.calls), JSON.stringify(f.results));\n'
            'f.mockReturnValue("const");\n'
            'console.log(f(1), f.mockImplementationOnce(() => "once-1").mockImplementationOnce(() '
            '=> { throw new Error("once-2"); }) === f);\n'
            'console.log(f(1));\n'
            'try { f(2); } catch (e) { console.log("thrown", e.message); }\n'
            'console.log(f(3), JSON.stringify(f.results.map((r) => r.type + ":" + (r.value '
            'instanceof Error ? r.value.message : r.value))));\n'
            'f.mockImplementation((a, b) => a + b);\n'
            'console.log(f(1, 2), f.mockClear() === f, f.calls.length, f.results.length, f(3, 4), '
            'f.calls.length);\n'
            'f.mockImplementationOnce(() => "queued");\n'
            'f.mockReset();\n'
            'console.log(f(1), f.calls.length);\n'
            'const g = mockFn(); console.log(g(), JSON.stringify(g.results));\n',
  'hint': 'Храните current (постоянная), once-очередь; обёртка записывает результат в '
          'finally/catch.',
  'expected': ['4 10 [[2],[5]] [{"type":"return","value":4},{"type":"return","value":10}]',
               'const true',
               'once-1',
               'thrown once-2',
               'const '
               '["return:4","return:10","return:const","return:once-1","throw:once-2","return:const"]',
               '3 true 0 0 7 1',
               'undefined 1',
               'undefined [{"type":"return"}]']},
 {'id': 'j31-fake-timers',
  'mode': 'js',
  'title': 'Управляемые часы',
  'statement': 'Напишите createClock(): { setTimeout, setInterval, clearTimeout, clearInterval, '
               'advance(ms), now(), pending() }. Время начинается с 0. setTimeout(fn, ms) и '
               'setInterval(fn, ms) возвращают числовой id, начиная с 1; ms < 1 считается за 1. '
               'advance(ms) двигает время вперёд, запуская таймеры в порядке времени срабатывания '
               '(при равенстве — в порядке создания); внутри callback now() равно времени '
               'срабатывания; таймеры, созданные в callback, учитываются, если срабатывают в '
               'пределах окна. Интервал после срабатывания перепланируется на +ms. clear* отменяет '
               'таймер любого типа (в том числе изнутри callback). pending() — число активных '
               'таймеров. После advance now() = прежнее + ms.',
  'starter': 'function createClock() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const c = createClock(); const log = [];\n'
            'const id1 = c.setTimeout(() => log.push(`A@${c.now()}`), 100);\n'
            'c.setInterval(() => log.push(`I@${c.now()}`), 30);\n'
            'c.setTimeout(() => { log.push(`B@${c.now()}`); c.setTimeout(() => '
            'log.push(`B2@${c.now()}`), 20); }, 50);\n'
            'c.setTimeout(() => log.push(`C@${c.now()}`), 100);\n'
            'console.log(c.pending(), c.now());\n'
            'c.advance(49); console.log(log.join(" "), c.now());\n'
            'c.advance(1); console.log(log.join(" "));\n'
            'c.advance(60); console.log(log.join(" "), c.now(), c.pending());\n'
            'const c2 = createClock(); const l2 = []; let n = 0;\n'
            'const iv = c2.setInterval(() => { l2.push(c2.now()); if (++n === 3) '
            'c2.clearInterval(iv); }, 10);\n'
            'c2.advance(100); console.log(l2.join(), c2.pending(), c2.now());\n'
            'const t = c2.setTimeout(() => l2.push("never"), 5); c2.clearTimeout(t); '
            'c2.advance(10); console.log(l2.length, id1, t);\n'
            'const c3 = createClock(); const l3 = []; c3.setTimeout(() => l3.push("zero"), 0); '
            'c3.advance(1); console.log(l3.join(), c3.now());\n',
  'hint': 'Цикл: найти ближайший таймер с time ≤ target, выставить now, выполнить; в конце now = '
          'target.',
  'expected': ['4 0',
               'I@30 49',
               'I@30 B@50',
               'I@30 B@50 I@60 B2@70 I@90 A@100 C@100 110 1',
               '10,20,30 0 100',
               '3 1 5',
               'zero 1']},
 {'id': 'j31-spy-on',
  'mode': 'js',
  'title': 'spyOn',
  'statement': 'Напишите spyOn(obj, method): подменяет obj[method] обёрткой, которая записывает '
               'вызовы и по умолчанию вызывает оригинал с тем же this и возвращает его результат. '
               'Возвращает объект шпиона: calls (массив массивов аргументов), mockReturnValue(v) — '
               'после этого обёртка возвращает v, не вызывая оригинал (метод возвращает шпиона), '
               'mockRestore() — вернуть оригинальный метод (повторный вызов безвреден; calls '
               'сохраняются). Если obj[method] не функция — Error(`Cannot spy on "метод": not a '
               'function`). Повторный spyOn поверх уже подменённого метода — Error(`"метод" is '
               'already spied on`) до восстановления.',
  'starter': 'function spyOn(obj, method) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const api = { base: 10, add(a, b) { return this.base + a + b; }, name: "x" };\n'
            'const spy = spyOn(api, "add");\n'
            'console.log(api.add(1, 2), JSON.stringify(spy.calls), api.add !== spy);\n'
            'spy.mockReturnValue(99);\n'
            'console.log(api.add(0, 0), spy.calls.length);\n'
            'spy.mockRestore(); spy.mockRestore();\n'
            'console.log(api.add(1, 1), spy.calls.length, api.add.name);\n'
            'for (const f of [() => spyOn(api, "name"), () => spyOn(api, "nope")]) { try { f(); } '
            'catch (e) { console.log(e.message); } }\n'
            'const s2 = spyOn(api, "add");\n'
            'try { spyOn(api, "add"); } catch (e) { console.log(e.message); }\n'
            's2.mockRestore(); const s3 = spyOn(api, "add"); console.log(typeof s3.calls, '
            'api.add(1, 1));\n',
  'hint': 'Сохраните оригинал и пометьте обёртку символом/свойством.',
  'expected': ['13 [[1,2]] true',
               '99 2',
               '12 2 add',
               'Cannot spy on "name": not a function',
               'Cannot spy on "nope": not a function',
               '"add" is already spied on',
               'object 12']},
 {'id': 'j31-by-role',
  'mode': 'js',
  'title': 'Поиск по роли',
  'statement': 'Модель DOM: { tag, text?, attrs?, children? }. Напишите queryAllByRole(root, role, '
               '{ name } = {}) и getByRole(root, role, opts). Роль элемента: attrs.role, если '
               'задан; иначе неявная: button → button, a с attrs.href → link, h1–h6 → heading, '
               "input с attrs.type === 'checkbox' → checkbox, прочие input → textbox, nav → "
               "navigation, ul/ol → list, li → listitem. Доступное имя: attrs['aria-label'], иначе "
               'собственный text вместе с текстом потомков (куски через пробел, пробелы схлопнуты '
               'и обрезаны). name — строка (точное совпадение имени) или RegExp (test). '
               'queryAllByRole — все совпадения в порядке обхода в глубину (корень первым). '
               "getByRole: ровно один — вернуть, ни одного — Error('Unable to find role "
               '"role"\'), больше — Error(\'Found multiple elements with role "role"\'). В '
               'сообщения добавьте ` and name "имя"` (для RegExp — её строковое представление в '
               'кавычках не берётся, просто String(regexp): `and name /re/`), если name задан.',
  'starter': 'function queryAllByRole(root, role, opts = {}) {\n'
             '}\n'
             'function getByRole(root, role, opts = {}) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const n = (tag, text, attrs, children) => ({ tag, text, attrs, children });\n'
            'const tree = n("div", undefined, {}, [\n'
            '  n("nav", undefined, { "aria-label": "main" }, [n("a", "Home", { href: "/" }), '
            'n("a", "Docs", { href: "/docs" }), n("a", "no href")]),\n'
            '  n("h1", "Title"), n("h2", "Sub  title "),\n'
            '  n("button", "Save", {}), n("button", undefined, { "aria-label": "Close" }, '
            '[n("span", "×")]),\n'
            '  n("div", "Click", { role: "button" }), n("input", undefined, { type: "checkbox", '
            '"aria-label": "Agree" }), n("input", undefined, { "aria-label": "Search" }),\n'
            '  n("ul", undefined, {}, [n("li", "one"), n("li", "two")]),\n'
            '  n("button", "Wrap", {}, [n("b", "ped  text")]),\n'
            ']);\n'
            'const names = (r, o) => queryAllByRole(tree, r, o).map((x) => x.text || '
            'x.attrs?.["aria-label"] || x.tag).join("|");\n'
            'console.log(names("link"), "/", names("button"), "/", names("heading"), "/", '
            'names("checkbox"), "/", names("textbox"), "/", names("listitem"), "/", '
            'names("navigation"), "/", names("list"), "/", JSON.stringify(names("dialog")));\n'
            'console.log(names("button", { name: "Save" }), names("button", { name: /^C/ }), '
            'names("button", { name: "Wrap ped text" }), names("link", { name: "Docs" }));\n'
            'const t = (f) => { try { console.log(f().text ?? f().attrs["aria-label"]); } catch '
            '(e) { console.log(e.message); } };\n'
            't(() => getByRole(tree, "navigation")); t(() => getByRole(tree, "link")); t(() => '
            'getByRole(tree, "dialog")); t(() => getByRole(tree, "link", { name: "Docs" })); t(() '
            '=> getByRole(tree, "button", { name: /zzz/ })); t(() => getByRole(tree, "button", { '
            'name: /e/ }));\n',
  'hint': 'Сначала функции roleOf(node) и nameOf(node), затем рекурсивный обход.',
  'expected': ['Home|Docs / Save|Close|Click|Wrap / Title|Sub  title  / Agree / Search / one|two / '
               'main / ul / ""',
               'Save Close|Click Wrap Docs',
               'main',
               'Found multiple elements with role "link"',
               'Unable to find role "dialog"',
               'Docs',
               'Unable to find role "button" and name /zzz/',
               'Found multiple elements with role "button" and name /e/']},
 {'id': 'j31-by-text',
  'mode': 'js',
  'title': 'Поиск по тексту',
  'statement': 'Модель: { tag, text?, children? }. Напишите getByText(root, text, { exact = true } '
               '= {}). Сравнивается собственный text узла (не потомков), нормализованный: пробелы '
               'схлопнуты, края обрезаны. exact: равенство строке; exact: false — вхождение '
               'подстроки без учёта регистра. Узлы с тегами script и style (и их потомки) '
               'пропускаются. Если text — RegExp, проверяется regexp.test(нормализованный текст). '
               "Ровно одно совпадение — вернуть узел; ни одного — Error('Unable to find text "
               '"text"\'); несколько — Error(\'Found multiple elements with text "text"\') (для '
               'RegExp в кавычках String(regexp) без кавычек).',
  'starter': 'function getByText(root, text, opts = {}) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const n = (tag, text, children) => ({ tag, text, children });\n'
            'const tree = n("div", "", [n("h1", "  Hello,   world "), n("p", "Hello again"), '
            'n("p", "hello"), n("script", "Hello, world", [n("i", "Hello")]), n("section", "Wrap", '
            '[n("span", "inner text")]), n("style", "x")]);\n'
            'const t = (...a) => { try { const r = getByText(tree, ...a); console.log(r.tag, '
            'JSON.stringify(r.text)); } catch (e) { console.log(e.message); } };\n'
            't("Hello, world"); t("Hello"); t("Hello", { exact: false }); t("hello", { exact: '
            'false }); t("hello"); t("inner text"); t("Wrap"); t("nothing"); t(/^Hello,/); '
            't(/hello/i); t("x"); t("inner", { exact: false });\n',
  'hint': 'Рекурсивный сбор совпадений, потом три исхода.',
  'expected': ['h1 "  Hello,   world "',
               'Unable to find text "Hello"',
               'Found multiple elements with text "Hello"',
               'Found multiple elements with text "hello"',
               'p "hello"',
               'span "inner text"',
               'section "Wrap"',
               'Unable to find text "nothing"',
               'h1 "  Hello,   world "',
               'Found multiple elements with text /hello/i',
               'Unable to find text "x"',
               'span "inner text"']},
 {'id': 'j31-wait-for',
  'mode': 'js',
  'title': 'waitFor',
  'statement': 'Напишите async waitFor(fn, { timeout = 1000, interval = 10 } = {}): вызывает fn '
               '(может быть async) и возвращает её результат, как только она не бросает '
               'исключение. Если бросает — ждёт interval мс и пробует снова. Когда прошло не '
               'меньше timeout мс (по Date.now()) с начала — бросает последнее пойманное '
               'исключение. Первый вызов — немедленно. Если fn не успевает завершиться (async), '
               'ожидание завершённого вызова всё равно дожидается результата; новый вызов не '
               'запускается, пока предыдущий не завершён.',
  'starter': 'async function waitFor(fn, opts = {}) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const sleep = (ms) => new Promise((r) => setTimeout(r, ms));\n'
            'let ready = false; setTimeout(() => (ready = true), 50);\n'
            'const t0 = Date.now();\n'
            'const v = await waitFor(() => { if (!ready) throw new Error("not ready"); return '
            '"done"; }, { timeout: 500, interval: 10 });\n'
            'const dt = Date.now() - t0;\n'
            'console.log(v, dt >= 45 && dt < 300);\n'
            'try { await waitFor(() => { throw new Error("always"); }, { timeout: 60, interval: 10 '
            '}); } catch (e) { console.log(e.message); }\n'
            'let calls = 0;\n'
            'console.log(await waitFor(() => { calls++; return 7; }), calls);\n'
            'let n = 0; let running = 0, maxRunning = 0;\n'
            'const r = await waitFor(async () => { running++; maxRunning = Math.max(maxRunning, '
            'running); await sleep(15); running--; if (++n < 3) throw new Error("try " + n); '
            'return n; }, { timeout: 1000, interval: 5 });\n'
            'console.log(r, maxRunning);\n'
            'let last; try { await waitFor(async () => { await sleep(5); throw new Error("e" + '
            '(last = (last ?? 0) + 1)); }, { timeout: 40, interval: 10 }); } catch (e) { '
            'console.log(/^e\\d+$/.test(e.message), Number(e.message.slice(1)) === last); }\n',
  'hint': 'Цикл с try/await; проверка времени после неудачной попытки.',
  'expected': ['done true', 'always', '7 1', '3 1', 'true true']},
 {'id': 'j31-snapshot',
  'mode': 'js',
  'title': 'Снимки (snapshot)',
  'statement': 'Напишите createSnapshots(): { check(name, value) }. Значение сериализуется в '
               'строку: JSON с отступом в 2 пробела, ключи объектов отсортированы по алфавиту на '
               'всех уровнях (undefined в объектах опускается как в JSON). Первый check для имени '
               "сохраняет снимок и возвращает { status: 'created' }. Следующие: совпало — { "
               "status: 'match' }; не совпало — { status: 'mismatch', diff }, где diff — "
               'построчная разница (массив строк): общие строки с префиксом «  » (два пробела), '
               'удалённые из снимка — «- », новые — «+ ». Используйте наибольшую общую '
               'подпоследовательность строк; при равноценном выборе удаление идёт раньше '
               'добавления. Снимок при mismatch НЕ перезаписывается.',
  'starter': 'function createSnapshots() {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const s = createSnapshots();\n'
            'const v1 = { title: "Hi", items: [1, 2, 3], meta: { b: 1, a: 2 } };\n'
            'console.log(JSON.stringify(s.check("card", v1)));\n'
            'console.log(JSON.stringify(s.check("card", { meta: { a: 2, b: 1 }, items: [1, 2, 3], '
            'title: "Hi" })));\n'
            'const r = s.check("card", { title: "Hello", items: [1, 3], meta: { a: 2, b: 1 }, '
            'extra: true });\n'
            'console.log(r.status); console.log(r.diff.join("\\n"));\n'
            'console.log(s.check("card", v1).status);\n'
            'console.log(JSON.stringify(s.check("other", [])), JSON.stringify(s.check("other", '
            '[])), JSON.stringify(s.check("n", null)), JSON.stringify(s.check("n", "x")));\n'
            'const r2 = s.check("list", ["a", "b"]); const r3 = s.check("list", ["b", "a"]); '
            'console.log(r3.diff.join("|"));\n',
  'hint': 'Сериализатор с сортировкой ключей; таблица LCS и проход с восстановлением.',
  'expected': ['{"status":"created"}',
               '{"status":"match"}',
               'mismatch',
               '  {',
               '+   "extra": true,',
               '    "items": [',
               '      1,',
               '-     2,',
               '      3',
               '    ],',
               '    "meta": {',
               '      "a": 2,',
               '      "b": 1',
               '    },',
               '-   "title": "Hi"',
               '+   "title": "Hello"',
               '  }',
               'match',
               '{"status":"created"} {"status":"match"} {"status":"created"} '
               '{"status":"mismatch","diff":["- null","+ \\"x\\""]}',
               '  [|-   "a",|-   "b"|+   "b",|+   "a"|  ]']},
 {'id': 'j31-coverage',
  'mode': 'js',
  'title': 'Покрытие строк',
  'statement': 'Напишите lineCoverage(source, hits, ignore = []): source — исходный текст; hits — '
               'массив номеров выполненных строк (с 1, возможны повторы и номера не-кодовых '
               'строк); ignore — номера строк, исключённые из подсчёта. Кодовая строка — не пустая '
               'после trim и не начинающаяся с «//». Верните { total, covered, percent, missing }: '
               'total — кодовых строк без ignore; covered — из них выполненных; percent — covered '
               '/ total * 100, округлённое до одного знака (если total = 0 — 100); missing — '
               'невыполненные кодовые строки одной строкой: подряд идущие номера (по кодовым '
               'строкам, пропуски пустых строк между ними разрывают диапазон НЕ нужно — диапазон '
               'по номерам строк) сворачиваются в «a-b», части через «, » (пустая строка, если всё '
               'покрыто). Диапазон = подряд идущие номера строк без разрыва.',
  'starter': 'function lineCoverage(source, hits, ignore = []) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const src = ["function f(x) {", "  // comment", "  if (x > 0) {", "    return 1;", "  '
            '}", "", "  if (x < 0) {", "    return -1;", "  }", "  return 0;", "}"].join("\\n");\n'
            'const show = (h, ig) => console.log(JSON.stringify(lineCoverage(src, h, ig)));\n'
            'show([1, 3, 4, 10, 11, 4, 4]); show([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]); show([]); '
            'show([1, 3, 4], [7, 8, 9, 10, 11]); show([1, 3, 4, 99, 0]);\n'
            'console.log(JSON.stringify(lineCoverage("", [])), JSON.stringify(lineCoverage("// '
            'only\\n\\n", [1])), JSON.stringify(lineCoverage("a\\nb\\nc\\nd\\ne", [1, 5])), '
            'JSON.stringify(lineCoverage("a\\nb\\nc", [], [1, 2, 3])));\n',
  'hint': 'Соберите массив непокрытых номеров и сверните подряд идущие.',
  'expected': ['{"total":9,"covered":5,"percent":55.6,"missing":"5, 7-9"}',
               '{"total":9,"covered":9,"percent":100,"missing":""}',
               '{"total":9,"covered":0,"percent":0,"missing":"1, 3-5, 7-11"}',
               '{"total":4,"covered":3,"percent":75,"missing":"5"}',
               '{"total":9,"covered":3,"percent":33.3,"missing":"5, 7-11"}',
               '{"total":0,"covered":0,"percent":100,"missing":""} '
               '{"total":0,"covered":0,"percent":100,"missing":""} '
               '{"total":5,"covered":2,"percent":40,"missing":"2-4"} '
               '{"total":0,"covered":0,"percent":100,"missing":""}']},
 {'id': 'j31-flaky',
  'mode': 'js',
  'title': 'Повтор нестабильных тестов',
  'statement': 'Напишите async runWithRetries(test, retries): test(attempt) — async-функция '
               '(attempt начинается с 0), выбрасывает при провале. Всего попыток 1 + retries. '
               "Результат: прошла с первой — { status: 'passed', attempts: 1 }; прошла после "
               "неудач — { status: 'flaky', attempts: k, errors: [сообщения прошлых неудач] }; все "
               "неудачны — { status: 'failed', attempts: 1 + retries, errors: [сообщения всех "
               'попыток] }. Успех прекращает дальнейшие попытки. Затем напишите '
               'summarize(results): results — { имя: результат } → { passed, flaky, failed, ok } '
               '(счётчики; ok — нет failed, flaky допустимы), а также flakyNames — имена '
               'нестабильных по алфавиту.',
  'starter': 'async function runWithRetries(test, retries) {\n'
             '}\n'
             'function summarize(results) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const mk = (failsBefore) => async (attempt) => { await null; if (attempt < '
            'failsBefore) throw new Error("fail#" + attempt); };\n'
            'console.log(JSON.stringify(await runWithRetries(mk(0), 2)));\n'
            'console.log(JSON.stringify(await runWithRetries(mk(2), 3)));\n'
            'console.log(JSON.stringify(await runWithRetries(mk(99), 2)));\n'
            'console.log(JSON.stringify(await runWithRetries(mk(1), 0)));\n'
            'let calls = 0; await runWithRetries(async () => { calls++; }, 5); '
            'console.log(calls);\n'
            'const res = { b: await runWithRetries(mk(1), 2), a: await runWithRetries(mk(1), 2), '
            'c: await runWithRetries(mk(0), 2), d: await runWithRetries(mk(5), 1) };\n'
            'console.log(JSON.stringify(summarize(res)), JSON.stringify(summarize({ x: res.c, y: '
            'res.a })), JSON.stringify(summarize({})));\n',
  'hint': 'Цикл по попыткам с try/catch; errors накапливайте массивом message.',
  'expected': ['{"status":"passed","attempts":1}',
               '{"status":"flaky","attempts":3,"errors":["fail#0","fail#1"]}',
               '{"status":"failed","attempts":3,"errors":["fail#0","fail#1","fail#2"]}',
               '{"status":"failed","attempts":1,"errors":["fail#0"]}',
               '1',
               '{"passed":1,"flaky":2,"failed":1,"ok":false,"flakyNames":["a","b"]} '
               '{"passed":1,"flaky":1,"failed":0,"ok":true,"flakyNames":["y"]} '
               '{"passed":0,"flaky":0,"failed":0,"ok":true,"flakyNames":[]}']},
 {'id': 'j31-unused-imports',
  'mode': 'js',
  'title': 'Неиспользуемые импорты',
  'statement': 'Напишите findUnusedImports(source) → массив локальных имён из import-строк, '
               'которые больше нигде не встречаются, в порядке объявления. Поддерживаются '
               'однострочные формы: `import X from "m";`, `import { a, b as c } from "m";`, '
               '`import X, { a } from "m";`, `import * as ns from "m";`; `import "m";` (без '
               'привязок) игнорируется. Для `b as c` локальное имя — c. Перед поиском удалите '
               'комментарии `//…` и `/* … */`; затем в тексте без import-строк ищется слово '
               'целиком (границы по символам идентификатора, включая «$»). Вхождения внутри строк '
               'считаются использованием.',
  'starter': 'function findUnusedImports(source) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const src = `\n'
            'import React from "react";\n'
            'import { useState, useEffect as useFx, memo } from "react";\n'
            'import * as utils from "./utils.js"; // utils\n'
            'import Button, { Icon, $dollar } from "./ui.js";\n'
            'import "./side-effect.css";\n'
            '/* import hidden from "x"; */\n'
            '// useState(0)\n'
            'export function App() {\n'
            '  const [a] = React.useState(1);\n'
            '  useFx(() => {}, []);\n'
            '  return <Button label="memo" />; // Icon\n'
            '}\n'
            '`;\n'
            'console.log(JSON.stringify(findUnusedImports(src)));\n'
            "console.log(JSON.stringify(findUnusedImports('import a from "
            '"a";\\nconsole.log(a);\')), JSON.stringify(findUnusedImports("")), '
            'JSON.stringify(findUnusedImports(\'import { x as y } from "m";\\nconst x = 1;\')), '
            'JSON.stringify(findUnusedImports(\'import { f } from "m";\\nconst s = "f";\\nconst g '
            "= fx + f_;')));\n",
  'hint': 'Разберите импорты регулярным выражением по строкам, остальной текст — в одну строку для '
          'поиска.',
  'expected': ['["utils","Icon","$dollar"]', '[] [] ["y"] []']},
 {'id': 'j31-conventional',
  'mode': 'js',
  'title': 'Conventional Commits: версия и changelog',
  'statement': 'Сообщение коммита: «тип(область)!: описание», область и «!» необязательны; тело — '
               'со второй строки. Напишите nextVersion(current, commits): commits — массив строк. '
               'Повышение: major — если у любого коммита есть «!» после типа/области или в теле '
               'строка, начинающаяся с «BREAKING CHANGE:»; иначе minor — если есть feat; иначе '
               'patch — если есть fix или perf; иначе bump = null и версия прежняя. Результат { '
               'version, bump }: при major — (M+1).0.0, minor — M.(m+1).0, patch — M.m.(p+1). '
               'Сообщения, не подходящие под формат, игнорируются. Также напишите '
               'changelog(commits) → строка Markdown: разделы в порядке «### Breaking Changes» '
               '(коммиты с «!»/BREAKING, текст — описание), «### Features» (feat), «### Fixes» '
               '(fix, perf); пустые разделы опускаются; пункты — «- описание» в порядке коммитов, '
               'а при области — «- **область:** описание»; разделы разделены пустой строкой; нет '
               'пунктов — пустая строка. Breaking-коммит попадает только в «Breaking Changes».',
  'starter': 'function nextVersion(current, commits) {\n}\nfunction changelog(commits) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (cur, cs) => console.log(cur, JSON.stringify(nextVersion(cur, cs)));\n'
            't("1.2.3", ["fix: typo"]); t("1.2.3", ["fix: a", "feat(ui): b"]); t("1.2.3", ["feat!: '
            'drop v1", "fix: x"]); t("1.2.3", ["chore: deps", "docs: readme"]); t("0.9.9", '
            '["fix(core): z\\n\\nBREAKING CHANGE: api changed"]);\n'
            't("2.0.0", ["perf: faster"]); t("2.0.0", ["random text", "Merge branch x"]); '
            't("1.0.0", ["refactor(api)!: rename"]); t("1.0.0", ["feat: x\\n\\nsome '
            'body\\nBREAKING CHANGE not at start"]);\n'
            'const cs = ["feat(ui): add dark mode", "fix: crash on empty list", "feat!: new config '
            'format", "chore: bump", "perf(core): cache routes", "fix(auth): refresh '
            'token\\n\\nBREAKING CHANGE: tokens renamed", "feat: export csv"];\n'
            'console.log(changelog(cs)); console.log(JSON.stringify(changelog(["chore: x"])), '
            'JSON.stringify(changelog([])), JSON.stringify(changelog(["fix: only"])));\n',
  'hint': 'Функция parseCommit возвращает { type, scope, desc, breaking } или null.',
  'expected': ['1.2.3 {"version":"1.2.4","bump":"patch"}',
               '1.2.3 {"version":"1.3.0","bump":"minor"}',
               '1.2.3 {"version":"2.0.0","bump":"major"}',
               '1.2.3 {"version":"1.2.3","bump":null}',
               '0.9.9 {"version":"1.0.0","bump":"major"}',
               '2.0.0 {"version":"2.0.1","bump":"patch"}',
               '2.0.0 {"version":"2.0.0","bump":null}',
               '1.0.0 {"version":"2.0.0","bump":"major"}',
               '1.0.0 {"version":"1.1.0","bump":"minor"}',
               '### Breaking Changes',
               '- new config format',
               '- **auth:** refresh token',
               '',
               '### Features',
               '- **ui:** add dark mode',
               '- export csv',
               '',
               '### Fixes',
               '- crash on empty list',
               '- **core:** cache routes',
               '"" "" "### Fixes\\n- only"']},
 {'id': 'j31-pipeline',
  'mode': 'js',
  'title': 'Конвейер CI',
  'statement': 'Напишите async runPipeline(steps, run): steps — [{ name, needs?: [имена], if?: '
               "'success' | 'always' | 'failure', run }] (if по умолчанию 'success'). Выполняйте "
               'последовательно. Порядок: повторяйте — берите первый по списку ещё не выполненный '
               "шаг, все needs которого уже обработаны. Неизвестное имя в needs — Error('Unknown "
               "step: имя') (до запуска чего-либо); невозможность продолжить (цикл) — "
               "Error('Cannot resolve needs'). Решение о запуске: 'success' — все needs "
               "завершились успешно (status 'passed'); 'always' — всегда; 'failure' — хотя бы один "
               "из needs failed (без needs — никогда). Иначе шаг 'skipped'. Запущенный шаг: await "
               "step.run(); исключение → 'failed' с error = message. Результат { ok, results } — "
               "results в порядке выполнения: [{ name, status: 'passed'|'failed'|'skipped', error? "
               '}]; ok — нет failed. Параметр run не используется (оставлен для совместимости) — '
               'вызывайте step.run.',
  'starter': 'async function runPipeline(steps) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const log = [];\n'
            'const ok = (n) => async () => { await null; log.push(n); };\n'
            'const bad = (n) => async () => { log.push(n); throw new Error(n + " broke"); };\n'
            'const show = (r) => console.log(r.ok, r.results.map((x) => '
            '`${x.name}:${x.status}${x.error ? "(" + x.error + ")" : ""}`).join(" "), "|", '
            'log.join(","));\n'
            'show(await runPipeline([{ name: "install", run: ok("install") }, { name: "lint", '
            'needs: ["install"], run: ok("lint") }, { name: "test", needs: ["install"], run: '
            'ok("test") }, { name: "build", needs: ["lint", "test"], run: ok("build") }]));\n'
            'log.length = 0;\n'
            'show(await runPipeline([{ name: "install", run: ok("install") }, { name: "test", '
            'needs: ["install"], run: bad("test") }, { name: "build", needs: ["test"], run: '
            'ok("build") }, { name: "notify", needs: ["build"], if: "always", run: ok("notify") }, '
            '{ name: "report", needs: ["test"], if: "failure", run: ok("report") }, { name: '
            '"cleanup", if: "failure", run: ok("cleanup") }]));\n'
            'log.length = 0;\n'
            'show(await runPipeline([{ name: "deploy", needs: ["build"], run: ok("deploy") }, { '
            'name: "build", run: ok("build") }]));\n'
            'for (const steps of [[{ name: "a", needs: ["zzz"], run: ok("a") }], [{ name: "a", '
            'needs: ["b"], run: ok("a") }, { name: "b", needs: ["a"], run: ok("b") }]]) { '
            'log.length = 0; try { await runPipeline(steps); } catch (e) { console.log(e.message, '
            'log.length); } }\n'
            'show(await runPipeline([]));\n',
  'hint': 'Map статусов; цикл while с поиском готового шага.',
  'expected': ['true install:passed lint:passed test:passed build:passed | install,lint,test,build',
               'false install:passed test:failed(test broke) build:skipped notify:passed '
               'report:passed cleanup:skipped | install,test,notify,report',
               'true build:passed deploy:passed | build,deploy',
               'Unknown step: zzz 0',
               'Cannot resolve needs 0',
               'true  |']},
 {'id': 'j31-matrix',
  'mode': 'js',
  'title': 'Матрица сборки',
  'statement': 'Напишите expandMatrix(matrix, { include = [], exclude = [] } = {}) → массив '
               'комбинаций (объектов). Базовые комбинации — декартово произведение значений: '
               'первый ключ меняется медленнее всего, порядок ключей — как в matrix. Затем '
               'exclude: убираются комбинации, у которых совпадают все ключи записи exclude '
               '(запись может быть частичной). Затем include: для записи считаются её «исходные» '
               'ключи (те, что есть в matrix); если исходных нет — запись добавляется ко всем '
               'комбинациям; иначе находятся комбинации, у которых эти ключи совпадают; в каждую '
               'найденную добавляются остальные ключи записи (не затирая существующие ключи); если '
               'подходящих нет — запись добавляется отдельной новой комбинацией как есть. Пустая '
               'matrix → [{}] плюс include по тем же правилам.',
  'starter': 'function expandMatrix(matrix, opts = {}) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (m, o) => console.log(JSON.stringify(expandMatrix(m, o)));\n'
            'const m = { os: ["linux", "mac"], node: [18, 20] };\n'
            'show(m); show(m, { exclude: [{ os: "mac", node: 18 }] }); show(m, { exclude: [{ os: '
            '"mac" }] });\n'
            'show(m, { include: [{ os: "linux", experimental: true }] }); show(m, { include: [{ '
            'os: "windows", node: 20 }] }); show(m, { include: [{ coverage: true }] }); show(m, { '
            'include: [{ node: 20, os: "linux", node: 20, tag: "x" }], exclude: [{ os: "linux", '
            'node: 18 }] });\n'
            'show({ a: [1, 2] }, { include: [{ a: 1, a2: "x" }, { a: 1, a2: "y" }] }); show({}); '
            'show({}, { include: [{ x: 1 }] }); show({ k: [] });\n',
  'hint': 'reduce по ключам для произведения; matches(combo, entry, keys).',
  'expected': ['[{"os":"linux","node":18},{"os":"linux","node":20},{"os":"mac","node":18},{"os":"mac","node":20}]',
               '[{"os":"linux","node":18},{"os":"linux","node":20},{"os":"mac","node":20}]',
               '[{"os":"linux","node":18},{"os":"linux","node":20}]',
               '[{"os":"linux","node":18,"experimental":true},{"os":"linux","node":20,"experimental":true},{"os":"mac","node":18},{"os":"mac","node":20}]',
               '[{"os":"linux","node":18},{"os":"linux","node":20},{"os":"mac","node":18},{"os":"mac","node":20},{"os":"windows","node":20}]',
               '[{"os":"linux","node":18,"coverage":true},{"os":"linux","node":20,"coverage":true},{"os":"mac","node":18,"coverage":true},{"os":"mac","node":20,"coverage":true}]',
               '[{"os":"linux","node":20,"tag":"x"},{"os":"mac","node":18},{"os":"mac","node":20}]',
               '[{"a":1,"a2":"x"},{"a":2}]',
               '[{}]',
               '[{"x":1}]',
               '[]']},
 {'id': 'j31-cache',
  'mode': 'js',
  'title': 'Кэш зависимостей в CI',
  'statement': 'Функция fnv1a(str) → 8 hex-символов уже есть. Напишите makeCacheKey(os, '
               "lockfileContent, prefix = 'npm') → `${os}-${prefix}-${fnv1a(lockfileContent)}`. И "
               'restoreCache(caches, key, restoreKeys = []): caches — массив { key } в порядке '
               "сохранения (последний — самый свежий). Точное совпадение key → { hit: 'exact', key "
               '}. Иначе для каждого префикса из restoreKeys по порядку: самый свежий кэш, чей '
               "ключ начинается с префикса → { hit: 'partial', key: найденный ключ }. Иначе { hit: "
               'null, key: null }.',
  'starter': '// Готово: хеш FNV-1a (не изменяйте)\n'
             'function fnv1a(str) {\n'
             '  let h = 0x811c9dc5;\n'
             '  for (const b of new TextEncoder().encode(str)) { h ^= b; h = Math.imul(h, '
             '0x01000193) >>> 0; }\n'
             '  return h.toString(16).padStart(8, "0");\n'
             '}\n'
             'function makeCacheKey(os, lockfileContent, prefix = "npm") {\n'
             '}\n'
             'function restoreCache(caches, key, restoreKeys = []) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const k1 = makeCacheKey("linux", "lock-v1"), k2 = makeCacheKey("linux", "lock-v2"), '
            'k3 = makeCacheKey("mac", "lock-v1", "pnpm");\n'
            'console.log(k1 === `linux-npm-${fnv1a("lock-v1")}`, k1 !== k2, '
            'k3.startsWith("mac-pnpm-"), k1.length);\n'
            'const caches = [{ key: k1 }, { key: "linux-npm-aaaaaaaa" }, { key: "mac-npm-bbbbbbbb" '
            '}, { key: "linux-npm-cccccccc" }, { key: "linux-yarn-dddddddd" }];\n'
            'console.log(JSON.stringify(restoreCache(caches, k1, ["linux-npm-"])));\n'
            'console.log(JSON.stringify(restoreCache(caches, k2, ["linux-npm-", "linux-"])));\n'
            'console.log(JSON.stringify(restoreCache(caches, k2, ["linux-pnpm-", "linux-yarn-", '
            '"linux-"])));\n'
            'console.log(JSON.stringify(restoreCache(caches, k2, ["windows-"])), '
            'JSON.stringify(restoreCache(caches, k2)), JSON.stringify(restoreCache([], "x", '
            '["a"])));\n'
            'console.log(JSON.stringify(restoreCache(caches, "mac-npm-bbbbbbbb", ["zzz"])));\n',
  'hint': 'Для точного совпадения достаточно some; для частичного — перебор с конца.',
  'expected': ['true true true 18',
               '{"hit":"exact","key":"linux-npm-ad04aee0"}',
               '{"hit":"partial","key":"linux-npm-cccccccc"}',
               '{"hit":"partial","key":"linux-yarn-dddddddd"}',
               '{"hit":null,"key":null} {"hit":null,"key":null} {"hit":null,"key":null}',
               '{"hit":"exact","key":"mac-npm-bbbbbbbb"}']},
 {'id': 'j31-cache-control',
  'mode': 'js',
  'title': 'Cache-Control для статики',
  'statement': 'Напишите cacheControl(path) → строка заголовка. Путь без query/hash. Правила по '
               'порядку: путь начинается с «/api/» → «no-store»; путь «/», оканчивается на '
               '«.html», либо последний сегмент без расширения (нет точки), либо это «/sw.js» или '
               '«/service-worker.js» → «no-cache»; имя файла содержит хеш — сегмент вида «.<8 и '
               'более hex-символов>.» перед расширением (например app.3f9a1c2d.js), — «public, '
               'max-age=31536000, immutable»; прочая статика — «public, max-age=3600». Регистр '
               'букв в hex не важен.',
  'starter': 'function cacheControl(path) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'for (const p of ["/", "/index.html", "/api/users", "/api/", "/users/42", '
            '"/assets/app.3f9a1c2d.js", "/assets/style.ABCDEF12.css", "/assets/app.12345.js", '
            '"/logo.png", "/sw.js", "/service-worker.js", "/docs/page.html?x=1", '
            '"/fonts/inter.8a7b6c5d4e.woff2", "/robots.txt", "/apix", '
            '"/assets/img.deadbeef.png#hash"]) console.log(p, "→", cacheControl(p));\n',
  'hint': 'Последний сегмент пути, регулярное выражение /\\.[0-9a-f]{8,}\\./i.',
  'expected': ['/ → no-cache',
               '/index.html → no-cache',
               '/api/users → no-store',
               '/api/ → no-store',
               '/users/42 → no-cache',
               '/assets/app.3f9a1c2d.js → public, max-age=31536000, immutable',
               '/assets/style.ABCDEF12.css → public, max-age=31536000, immutable',
               '/assets/app.12345.js → public, max-age=3600',
               '/logo.png → public, max-age=3600',
               '/sw.js → no-cache',
               '/service-worker.js → no-cache',
               '/docs/page.html?x=1 → no-cache',
               '/fonts/inter.8a7b6c5d4e.woff2 → public, max-age=31536000, immutable',
               '/robots.txt → public, max-age=3600',
               '/apix → no-cache',
               '/assets/img.deadbeef.png#hash → public, max-age=31536000, immutable']},
 {'id': 'j31-spa-fallback',
  'mode': 'js',
  'title': 'Сервер статики с SPA-фолбэком',
  'statement': 'Напишите resolveRequest(files, url): files — массив путей существующих файлов '
               '(«/index.html», «/assets/app.js», «/docs/index.html»…). url может содержать '
               'query/hash (отбрасываются) и процентное кодирование (decodeURIComponent; '
               'некорректное — статус 400). Путь с сегментом «..» (после декодирования) — { '
               'status: 400 }. Дальше: существующий файл → { status: 200, file }. Путь, '
               'оканчивающийся на «/», → индекс каталога (путь + «index.html»), если он есть → '
               '200, иначе — по общему правилу фолбэка. Нет файла: путь начинается с «/api/» → { '
               'status: 404 }; у последнего сегмента есть расширение (точка) → { status: 404 }; '
               "иначе (маршрут клиентского приложения) → { status: 200, file: '/index.html', "
               'fallback: true }, если «/index.html» есть, иначе 404.',
  'starter': 'function resolveRequest(files, url) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const files = ["/index.html", "/assets/app.3f9a1c2d.js", "/docs/index.html", '
            '"/logo.png", "/a b.txt"];\n'
            'for (const u of ["/", "/index.html", "/assets/app.3f9a1c2d.js?v=1", "/docs/", '
            '"/docs", "/users/42", "/users/42/", "/missing.png", "/api/users", "/api/", '
            '"/a%20b.txt", "/%E0%A4%A", "/../etc/passwd", "/a/%2e%2e/b", "/users/profile#top", '
            '"/assets/", "/v1.2/dashboard"]) console.log(u, "→", '
            'JSON.stringify(resolveRequest(files, u)));\n'
            'console.log(JSON.stringify(resolveRequest(["/logo.png"], "/users")), '
            'JSON.stringify(resolveRequest([], "/")));\n',
  'hint': 'Set путей; последовательность проверок как в условии.',
  'expected': ['/ → {"status":200,"file":"/index.html"}',
               '/index.html → {"status":200,"file":"/index.html"}',
               '/assets/app.3f9a1c2d.js?v=1 → {"status":200,"file":"/assets/app.3f9a1c2d.js"}',
               '/docs/ → {"status":200,"file":"/docs/index.html"}',
               '/docs → {"status":200,"file":"/index.html","fallback":true}',
               '/users/42 → {"status":200,"file":"/index.html","fallback":true}',
               '/users/42/ → {"status":200,"file":"/index.html","fallback":true}',
               '/missing.png → {"status":404}',
               '/api/users → {"status":404}',
               '/api/ → {"status":404}',
               '/a%20b.txt → {"status":200,"file":"/a b.txt"}',
               '/%E0%A4%A → {"status":400}',
               '/../etc/passwd → {"status":400}',
               '/a/%2e%2e/b → {"status":400}',
               '/users/profile#top → {"status":200,"file":"/index.html","fallback":true}',
               '/assets/ → {"status":200,"file":"/index.html","fallback":true}',
               '/v1.2/dashboard → {"status":200,"file":"/index.html","fallback":true}',
               '{"status":404} {"status":404}']},
 {'id': 'j31-releases',
  'mode': 'js',
  'title': 'Релизы и откат',
  'statement': 'Напишите createReleases({ keep = 3 } = {}): { deploy(id), activate(id), '
               'rollback(), active(), list() }. deploy(id) добавляет релиз и делает его активным; '
               "повторный id — Error('Release already exists: id'). После добавления, пока релизов "
               'больше keep, удаляется самый старый неактивный. activate(id) делает активным '
               "существующий релиз (иначе Error('Unknown release: id')); активация текущего ничего "
               'не меняет. rollback() возвращает к предыдущей активации: ведётся история активаций '
               '(стек); текущая снимается, берётся ближайшая предыдущая, чей релиз ещё существует; '
               "если такой нет — Error('No previous release'); возвращает id нового активного "
               'релиза. active() — id или null; list() — id по порядку развёртывания (старые '
               'первыми).',
  'starter': 'function createReleases(opts = {}) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const r = createReleases({ keep: 3 });\n'
            'console.log(r.active(), JSON.stringify(r.list()));\n'
            'try { r.rollback(); } catch (e) { console.log(e.message); }\n'
            'r.deploy("v1"); r.deploy("v2"); r.deploy("v3");\n'
            'console.log(r.active(), r.list().join());\n'
            'console.log(r.rollback(), r.active(), r.rollback(), r.active());\n'
            'try { r.rollback(); } catch (e) { console.log(e.message, r.active()); }\n'
            'r.activate("v3"); r.deploy("v4");\n'
            'console.log(r.list().join(), r.active());\n'
            'console.log(r.rollback());\n'
            'try { r.rollback(); } catch (e) { console.log(e.message); }\n'
            'for (const f of [() => r.deploy("v4"), () => r.activate("v1")]) { try { f(); } catch '
            '(e) { console.log(e.message); } }\n'
            'r.activate("v4"); r.activate("v4"); console.log(r.rollback(), r.active());\n'
            'const k = createReleases({ keep: 1 }); k.deploy("a"); k.deploy("b"); '
            'console.log(k.list().join(), k.active());\n'
            'const d = createReleases(); d.deploy("1"); d.deploy("2"); d.deploy("3"); '
            'd.deploy("4"); d.deploy("5"); console.log(d.list().join(), d.active(), d.rollback(), '
            'd.rollback());\n'
            'try { d.rollback(); } catch (e) { console.log(e.message, d.active()); }\n',
  'hint': 'Массив релизов и стек истории; при откате выкидывайте из стека удалённые id.',
  'expected': ['null []',
               'No previous release',
               'v3 v1,v2,v3',
               'v2 v2 v1 v1',
               'No previous release v1',
               'v2,v3,v4 v4',
               'v3',
               'No previous release',
               'Release already exists: v4',
               'Unknown release: v1',
               'v3 v3',
               'b b',
               '3,4,5 5 4 3',
               'No previous release 3']}]}
