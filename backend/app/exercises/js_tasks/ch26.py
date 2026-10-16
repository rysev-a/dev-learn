"""Задачи книги «Современный Frontend»: глава 26."""

TASKS: dict[int, list[dict]] = {26: [{'id': 'j26-parse-imports',
  'mode': 'js',
  'title': 'Поиск импортов в исходнике',
  'statement': 'Напишите parseImports(src): массив { type, spec } в порядке появления в тексте. '
               "type 'static' — для «import … from 'x'», «import 'x'», «export … from 'x'» (любые "
               "формы списка имён, «* as ns», «default», «{ a as b }»); 'dynamic' — для "
               "«import('x')» с литеральной строкой в одинарных или двойных кавычках. Комментарии "
               '(// до конца строки и /* … */) игнорируются. Обычные объявления «export const …», '
               '«export default …» импортами не считаются. Нелитеральные динамические импорты '
               '(import(x)) — пропускаются.',
  'starter': 'function parseImports(src) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const src = `\n'
            'import a from "./a.js";\n'
            "import { b, c as d } from './b.js';\n"
            'import * as ns from "./ns.js";\n'
            'import "./side.js";\n'
            "export * from './re.js';\n"
            'export { x } from "./x.js";\n'
            'export const keep = 1;\n'
            'export default function () {}\n'
            '// import "./commented.js";\n'
            '/* import "./block.js"; */\n'
            "const lazy = () => import('./lazy.js');\n"
            'const dyn = (n) => import(n);\n'
            'import e, { f } from "lib";\n'
            '`;\n'
            'for (const i of parseImports(src)) console.log(i.type, i.spec);\n'
            'console.log(parseImports("const s = 1;").length);\n',
  'hint': 'Сначала вырежьте комментарии, затем одно регулярное выражение с флагом g и перебор '
          'exec.',
  'expected': ['static ./a.js',
               'static ./b.js',
               'static ./ns.js',
               'static ./side.js',
               'static ./re.js',
               'static ./x.js',
               'dynamic ./lazy.js',
               'static lib',
               '0']},
 {'id': 'j26-resolve',
  'mode': 'js',
  'title': 'Разрешение пути модуля',
  'statement': 'Напишите resolvePath(importer, spec, files): importer — путь файла-импортёра '
               '(POSIX, например «src/app/main.js»), spec — спецификатор, files — объект «путь → '
               'код». Голые спецификаторы (не начинаются с «.») — null. Относительные разрешаются '
               'от каталога импортёра (сегменты «.» и «..» учитываются). Затем проверяются '
               'кандидаты по порядку: точный путь, путь + «.js», путь + «/index.js» — возвращается '
               'первый существующий в files, иначе null. Выход выше корня «..» просто отбрасывает '
               'лишние сегменты.',
  'starter': 'function resolvePath(importer, spec, files) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const files = { "src/main.js": "", "src/util.js": "", "src/ui/index.js": "", '
            '"src/ui/button.js": "", "lib/x.js": "", "src/data.json": "" };\n'
            'const t = (imp, s) => console.log(imp, s, resolvePath(imp, s, files));\n'
            't("src/main.js", "./util"); t("src/main.js", "./util.js"); t("src/main.js", "./ui"); '
            't("src/ui/button.js", "../util"); t("src/ui/button.js", "./index");\n'
            't("src/main.js", "../lib/x"); t("src/main.js", "./data.json"); t("src/main.js", '
            '"./missing"); t("src/main.js", "react"); t("src/main.js", "/abs");\n'
            't("main.js", "./src/util"); t("src/ui/button.js", "../../../lib/x");\n',
  'hint': 'Соберите массив сегментов каталога, примените «.» и «..», затем перебор кандидатов.',
  'expected': ['src/main.js ./util src/util.js',
               'src/main.js ./util.js src/util.js',
               'src/main.js ./ui src/ui/index.js',
               'src/ui/button.js ../util src/util.js',
               'src/ui/button.js ./index src/ui/index.js',
               'src/main.js ../lib/x lib/x.js',
               'src/main.js ./data.json src/data.json',
               'src/main.js ./missing null',
               'src/main.js react null',
               'src/main.js /abs null',
               'main.js ./src/util src/util.js',
               'src/ui/button.js ../../../lib/x lib/x.js']},
 {'id': 'j26-graph',
  'mode': 'js',
  'title': 'Граф зависимостей',
  'statement': 'Напишите buildGraph(entry, files): files — { путь: код }. Вернуть { modules, order '
               '}. Обход в ширину от entry (очередь): для каждого модуля разберите импорты '
               '(parseImports) и разрешите относительные (resolvePath); голые спецификаторы '
               'пропускаются. modules[путь] = { deps, dynamic } — уникальные разрешённые пути '
               'статических и динамических импортов в порядке появления. order — порядок '
               'обнаружения модулей (в очереди). Относительный импорт, который не разрешился, — '
               "Error(`Cannot resolve '${spec}' from '${путь}'`). Циклы допустимы. parseImports и "
               'resolvePath уже есть.',
  'starter': '// Готово: найти импорты и разрешить относительный путь (не изменяйте)\n'
             'function parseImports(src) {\n'
             '  const out = [];\n'
             '  const re = '
             '/\\b(?:import|export)\\s+(?:[^\'"()]*?\\s+from\\s+)?([\'"])([^\'"]+)\\1|\\bimport\\(\\s*([\'"])([^\'"]+)\\3\\s*\\)/g;\n'
             '  let m;\n'
             '  while ((m = re.exec(src))) {\n'
             '    if (m[2] !== undefined) out.push({ type: "static", spec: m[2] });\n'
             '    else out.push({ type: "dynamic", spec: m[4] });\n'
             '  }\n'
             '  return out;\n'
             '}\n'
             'function resolvePath(importer, spec, files) {\n'
             '  if (!spec.startsWith(".")) return null;\n'
             '  const parts = importer.split("/").slice(0, -1);\n'
             '  for (const seg of spec.split("/")) {\n'
             '    if (seg === "." || seg === "") continue;\n'
             '    if (seg === "..") parts.pop();\n'
             '    else parts.push(seg);\n'
             '  }\n'
             '  const base = parts.join("/");\n'
             '  for (const cand of [base, base + ".js", base + "/index.js"]) if '
             '(Object.hasOwn(files, cand)) return cand;\n'
             '  return null;\n'
             '}\n'
             'function buildGraph(entry, files) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const files = {\n'
            '  "main.js": \'import a from "./a"; import "react"; const l = () => '
            'import("./lazy");\',\n'
            '  "a.js": \'import b from "./b"; import { x } from "./b";\',\n'
            '  "b.js": \'import a from "./a"; export const b = 1;\',\n'
            '  "lazy.js": \'import b from "./b"; import("./deep");\',\n'
            '  "deep.js": "export {}",\n'
            '  "orphan.js": "",\n'
            '};\n'
            'const g = buildGraph("main.js", files);\n'
            'console.log(JSON.stringify(g));\n'
            'try { buildGraph("main.js", { "main.js": \'import "./nope";\' }); } catch (e) { '
            'console.log(e.message); }\n'
            'console.log(JSON.stringify(buildGraph("x.js", { "x.js": "" })));\n',
  'hint': 'Очередь и множество seen; для каждого файла собираем два списка.',
  'expected': ['{"modules":{"main.js":{"deps":["a.js"],"dynamic":["lazy.js"]},"a.js":{"deps":["b.js"],"dynamic":[]},"lazy.js":{"deps":["b.js"],"dynamic":["deep.js"]},"b.js":{"deps":["a.js"],"dynamic":[]},"deep.js":{"deps":[],"dynamic":[]}},"order":["main.js","a.js","lazy.js","b.js","deep.js"]}',
               "Cannot resolve './nope' from 'main.js'",
               '{"modules":{"x.js":{"deps":[],"dynamic":[]}},"order":["x.js"]}']},
 {'id': 'j26-bundle-order',
  'mode': 'js',
  'title': 'Порядок модулей в бандле',
  'statement': 'Напишите bundleOrder(graph, entry): graph — { modules: { путь: { deps, dynamic } } '
               '} (как из buildGraph). Вернуть массив путей в порядке выполнения: обход в глубину '
               'по статическим deps, модуль добавляется после всех своих зависимостей '
               '(post-order), entry — последним. Каждый модуль один раз; на цикле повторный вход '
               'игнорируется. Динамические импорты не учитываются. Порядок обхода deps — как в '
               'массиве.',
  'starter': 'function bundleOrder(graph, entry) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const g = { modules: {\n'
            '  main: { deps: ["a", "b"], dynamic: ["lazy"] }, a: { deps: ["c"], dynamic: [] }, b: '
            '{ deps: ["c", "a"], dynamic: [] },\n'
            '  c: { deps: [], dynamic: [] }, lazy: { deps: ["c"], dynamic: [] },\n'
            '  p: { deps: ["q"], dynamic: [] }, q: { deps: ["p"], dynamic: [] },\n'
            '} };\n'
            'console.log(bundleOrder(g, "main").join(" "));\n'
            'console.log(bundleOrder(g, "p").join(" "));\n'
            'console.log(bundleOrder(g, "lazy").join(" "));\n'
            'console.log(bundleOrder(g, "c").join(" "));\n',
  'hint': 'Рекурсивный dfs с множеством visited; добавление в результат после обхода детей.',
  'expected': ['c a b main', 'q p', 'c lazy', 'c']},
 {'id': 'j26-esm-to-cjs',
  'mode': 'js',
  'title': 'ESM → CommonJS (подмножество)',
  'statement': 'Напишите transformEsm(src): превращает исходник эс-модуля в код CommonJS (для new '
               "Function('require','module','exports', код)). Каждая инструкция занимает свою "
               "строку. Правила: «import X from 'm';» → «const X = require('m').default;»; «import "
               "{ a, b as c } from 'm';» → «const { a, b: c } = require('m');»; «import * as ns "
               "from 'm';» → «const ns = require('m');»; «import 'm';» → «require('m');»; «export "
               'const|let|var name = …;» → та же строка без export, затем в той же строке « '
               'exports.name = name;» (добавьте перед концом строки после последней «;»); «export '
               'function name(» → «exports.name = name; function name(»; «export default '
               'выражение;» → «exports.default = выражение;»; «export { a, b as c };» → «exports.a '
               '= a; exports.c = b;». Остальные строки не меняются. Кавычки в import сохраняйте '
               'как есть.',
  'starter': 'function transformEsm(src) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const src = [\n'
            '  "import def from \'./d.js\';",\n'
            '  "import { a, b as c } from \\"./ab.js\\";",\n'
            '  "import * as ns from \'./ns.js\';",\n'
            '  "import \'./side.js\';",\n'
            '  "export const x = a + c;",\n'
            '  "export let y = 2;",\n'
            '  "export function f(n) { return n + x; }",\n'
            '  "export default { def, ns };",\n'
            '  "const z = 3;",\n'
            '  "export { z, z as zz };",\n'
            '].join("\\n");\n'
            'const out = transformEsm(src);\n'
            'console.log(out);\n'
            'const mods = { "./d.js": { default: "D" }, "./ab.js": { a: 1, b: 2 }, "./ns.js": { n: '
            '1 }, "./side.js": {} };\n'
            'const module = { exports: {} };\n'
            'new Function("require", "module", "exports", out)((p) => mods[p], module, '
            'module.exports);\n'
            'console.log(JSON.stringify(Object.keys(module.exports).sort()), module.exports.x, '
            'module.exports.f(1), module.exports.zz, JSON.stringify(module.exports.default));\n',
  'hint': 'Обработка построчно регулярными выражениями; для export const — найдите имя и допишите '
          'присваивание в конец строки.',
  'expected': ["const def = require('./d.js').default;",
               'const { a, b: c } = require("./ab.js");',
               "const ns = require('./ns.js');",
               "require('./side.js');",
               'const x = a + c; exports.x = x;',
               'let y = 2; exports.y = y;',
               'exports.f = f; function f(n) { return n + x; }',
               'exports.default = { def, ns };',
               'const z = 3;',
               'exports.z = z; exports.zz = z;',
               '["default","f","x","y","z","zz"] 3 4 3 {"def":"D","ns":{"n":1}}']},
 {'id': 'j26-make-bundle',
  'mode': 'js',
  'title': 'Сборка бандла из CommonJS-модулей',
  'statement': 'Напишите makeBundle(files, entry, externals = {}): files — { путь: код модуля '
               'CommonJS (module, exports, require) }. Результат — строка с кодом, которая при '
               'выполнении через new Function(код)() возвращает module.exports входного модуля. '
               "Относительные require('./x') разрешаются как resolvePath (расширение .js и "
               'index.js допустимы) и вызывают модуль из таблицы; каждый модуль выполняется один '
               'раз, результат кэшируется; при циклических require отдаётся уже созданный '
               "(возможно, неполный) exports. Голый require('имя') берёт значение из "
               'externals[имя], иначе при вызове бросает Error("Cannot find module \'имя\'"). '
               'Нужны только модули, достижимые из entry. resolvePath уже есть.',
  'starter': '// Готово: найти импорты и разрешить относительный путь (не изменяйте)\n'
             'function resolvePath(importer, spec, files) {\n'
             '  if (!spec.startsWith(".")) return null;\n'
             '  const parts = importer.split("/").slice(0, -1);\n'
             '  for (const seg of spec.split("/")) {\n'
             '    if (seg === "." || seg === "") continue;\n'
             '    if (seg === "..") parts.pop();\n'
             '    else parts.push(seg);\n'
             '  }\n'
             '  const base = parts.join("/");\n'
             '  for (const cand of [base, base + ".js", base + "/index.js"]) if '
             '(Object.hasOwn(files, cand)) return cand;\n'
             '  return null;\n'
             '}\n'
             'function makeBundle(files, entry, externals = {}) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const files = {\n'
            '  "main.js": \'const { add } = require("./math"); const _ = require("ext"); '
            'module.exports = { r: add(2, 3), ext: _.name, count: require("./counter").count() '
            "};',\n"
            '  "math.js": \'exports.add = (a, b) => a + b; require("./counter").count();\',\n'
            '  "counter.js": \'let n = 0; exports.count = () => ++n;\',\n'
            '  "a.js": \'exports.fromA = 1; const b = require("./b"); exports.seenB = '
            "b.partial;',\n"
            '  "b.js": \'const a = require("./a"); exports.partial = a.fromA; \',\n'
            '  "needs.js": \'require("missing-pkg");\',\n'
            '  "unused.js": \'throw new Error("must not run");\',\n'
            '};\n'
            'const run = (entry, ext) => new Function(makeBundle(files, entry, ext))();\n'
            'console.log(JSON.stringify(run("main.js", { ext: { name: "EXT" } })));\n'
            'console.log(JSON.stringify(run("a.js")));\n'
            'try { run("needs.js"); } catch (e) { console.log(e.message); }\n'
            'console.log(typeof makeBundle(files, "main.js", { ext: {} }));\n',
  'hint': 'Соберите таблицу {путь: function(module, exports, require){...}}, внутри каждой '
          'подставьте свой require, который сопоставляет спецификатор с путём из таблицы.',
  'expected': ['{"r":5,"ext":"EXT","count":2}',
               '{"fromA":1,"seenB":1}',
               "Cannot find module 'missing-pkg'",
               'string']},
 {'id': 'j26-tree-shake',
  'mode': 'js',
  'title': 'Tree shaking по графу',
  'statement': 'Напишите shake(modules, entry): modules — { путь: { imports: [{ from, names }], '
               "exports: [имена], sideEffects } }, names — массив имён, '*' (все) или [] (импорт "
               'ради эффекта). Правила: все экспорты entry считаются использованными, entry '
               'включён. Для включённого модуля обработайте каждый его импорт: именованные имена '
               "помечаются использованными у модуля from (внутри списка exports; '*' — все его "
               'экспорты); модуль from включается, если у него есть использованные экспорты, либо '
               'это импорт ради эффекта ([]) и sideEffects === true. Повторяйте до неизменности '
               '(импорты включённых модулей обрабатываются, исключённых — нет). Верните { путь: '
               'отсортированный массив использованных экспортов } для включённых модулей; ключи — '
               'по алфавиту.',
  'starter': 'function shake(modules, entry) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const m = {\n'
            '  main: { imports: [{ from: "lib", names: ["a", "b"] }, { from: "poly", names: [] }, '
            '{ from: "css", names: [] }, { from: "util", names: ["x"] }], exports: ["run"], '
            'sideEffects: true },\n'
            '  lib: { imports: [{ from: "deep", names: ["d1"] }], exports: ["a", "b", "c"], '
            'sideEffects: false },\n'
            '  deep: { imports: [{ from: "more", names: ["m1"] }], exports: ["d1", "d2"], '
            'sideEffects: false },\n'
            '  more: { imports: [], exports: ["m1", "m2"], sideEffects: false },\n'
            '  poly: { imports: [], exports: [], sideEffects: true },\n'
            '  css: { imports: [], exports: [], sideEffects: false },\n'
            '  util: { imports: [{ from: "lib", names: ["*"] }], exports: ["x", "y"], sideEffects: '
            'false },\n'
            '  dead: { imports: [{ from: "more", names: ["m2"] }], exports: ["z"], sideEffects: '
            'false },\n'
            '};\n'
            'console.log(JSON.stringify(shake(m, "main")));\n'
            'console.log(JSON.stringify(shake({ solo: { imports: [], exports: ["a", "b"], '
            'sideEffects: false } }, "solo")));\n',
  'hint': 'Фиксированная итерация: пока что-то меняется, пройдите по всем включённым модулям.',
  'expected': ['{"deep":["d1"],"lib":["a","b","c"],"main":["run"],"more":["m1"],"poly":[],"util":["x"]}',
               '{"solo":["a","b"]}']},
 {'id': 'j26-dce',
  'mode': 'js',
  'title': 'Удаление мёртвого кода',
  'statement': 'Напишите liveSet(decls, roots): decls — { имя: { refs: [имена, на которые '
               'ссылается объявление] } }, roots — массив корневых имён (то, что экспортируется '
               'или имеет побочные эффекты). Вернуть отсортированный массив всех имён, достижимых '
               'из roots по refs (включая сами корни, существующие в decls). Имена из refs, '
               'которых нет в decls, игнорируются (внешние). Циклы допустимы.',
  'starter': 'function liveSet(decls, roots) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const d = { main: { refs: ["a", "b", "fetch"] }, a: { refs: ["c"] }, b: { refs: [] }, '
            'c: { refs: ["a"] }, unused1: { refs: ["unused2"] }, unused2: { refs: [] }, helper: { '
            'refs: ["b"] } };\n'
            'console.log(liveSet(d, ["main"]).join(","));\n'
            'console.log(liveSet(d, ["helper", "ghost"]).join(","));\n'
            'console.log(liveSet(d, []).join(","), liveSet({}, ["x"]).length);\n'
            'console.log(liveSet(d, ["main", "unused1"]).join(","));\n',
  'hint': 'Обход в глубину или ширину с множеством посещённых.',
  'expected': ['a,b,c,main', 'b,helper', ' 0', 'a,b,c,main,unused1,unused2']},
 {'id': 'j26-short-names',
  'mode': 'js',
  'title': 'Короткие имена для минификатора',
  'statement': 'Напишите nameSequence(count, reserved = []): первые count допустимых коротких '
               'имён. Порядок: «a»…«z», «A»…«Z» (52 одно-символьных), затем двухсимвольные «aa», '
               '«ab», …, «aZ», «ba», … (первая буква меняется медленнее; алфавит a–z, A–Z, как у '
               'системы счисления, где после «Z» идёт перенос), затем трёхсимвольные и т.д. Имена '
               'из reserved пропускаются (в счёт не идут). Идентификаторы не начинаются с цифры '
               '(цифр в алфавите нет).',
  'starter': 'function nameSequence(count, reserved = []) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(nameSequence(5).join(","));\n'
            'const s = nameSequence(60);\n'
            'console.log(s.slice(24, 30).join(","), s.slice(50, 56).join(","), s[59]);\n'
            'console.log(nameSequence(4, ["b", "c"]).join(","));\n'
            'console.log(nameSequence(2 * 52 + 52 * 52 > 0 ? 52 + 52 * 52 + 2 : '
            '0).slice(-3).join(","));\n'
            'console.log(nameSequence(0).length, new Set(nameSequence(300)).size);\n'
            'console.log(nameSequence(54, ["aa", "do", "if", "in"]).slice(51, 54).join(","));\n',
  'hint': 'Перебор длин 1, 2, 3…: для каждой длины — все комбинации в лексикографическом порядке '
          'алфавита.',
  'expected': ['a,b,c,d,e',
               'y,z,A,B,C,D Y,Z,aa,ab,ac,ad ah',
               'a,d,e,f',
               'ZZ,aaa,aab',
               '0 300',
               'Z,ab,ac']},
 {'id': 'j26-minify-css',
  'mode': 'js',
  'title': 'Минификация CSS',
  'statement': 'Напишите minifyCss(css): уберите комментарии /* … */; схлопните любую '
               'последовательность пробельных символов в один пробел; удалите пробелы вокруг «{», '
               '«}», «:», «;», «,», «>» и по краям текста; удалите «;» перед «}». Строки в '
               'одинарных или двойных кавычках копируются без изменений (внутри них пробелы, '
               'комментарии и спецсимволы не трогаются). Пробел между значениями (например '
               '«margin: 0 auto») сохраняется. Селекторы с двоеточием (a:hover) остаются '
               'корректными: пробел после «:» убирается везде.',
  'starter': 'function minifyCss(css) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (s) => console.log(JSON.stringify(minifyCss(s)));\n'
            't("a { color: red; }");\n'
            't("/* header */\\nbody {\\n  margin : 0  auto ;\\n  padding: 0 ;\\n}\\n");\n'
            't("a:hover , b > c { color : #fff ; background : url( \'a b.png\' ) }");\n'
            't(\'p::before { content: "a  { /* not a comment */ ; }" ; }\');\n'
            't("  ");\n'
            't(".x{}");\n'
            't("a {\\n\\tfont-family: \'Open Sans\' , sans-serif;\\n}\\n\\n/* end */");\n',
  'hint': 'Посимвольный проход со состоянием «внутри строки»; либо токенизация строк и остального, '
          'и замены только вне строк.',
  'expected': ['"a{color:red}"',
               '"body{margin:0 auto;padding:0}"',
               '"a:hover,b>c{color:#fff;background:url( \'a b.png\' )}"',
               '"p::before{content:\\"a  { /* not a comment */ ; }\\"}"',
               '""',
               '".x{}"',
               '"a{font-family:\'Open Sans\',sans-serif}"']},
 {'id': 'j26-hash-name',
  'mode': 'js',
  'title': 'Имя файла с хешем содержимого',
  'statement': 'Напишите hashedName(filename, content, len = 8) (node:crypto): хеш — первые len '
               'символов sha256 (hex) от содержимого (строка, UTF-8). Хеш вставляется перед '
               'последним расширением: «app.js» → «app.<хеш>.js»; «a.b.css» → «a.b.<хеш>.css»; у '
               'файла без расширения (в последнем сегменте пути нет точки или точка только в '
               'начале, как у «.env») — хеш добавляется в конец через точку: «LICENSE» → '
               '«LICENSE.<хеш>». Каталоги в пути сохраняются.',
  'starter': 'import { createHash } from "node:crypto";\n'
             'function hashedName(filename, content, len = 8) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(hashedName("app.js", "console.log(1)"));\n'
            'console.log(hashedName("dist/a.b.css", "body{}", 6));\n'
            'console.log(hashedName("LICENSE", "MIT"));\n'
            'console.log(hashedName(".env", "X=1", 4));\n'
            'console.log(hashedName("dir.v2/file", "x"));\n'
            'console.log(hashedName("a.js", "console.log(1)") === hashedName("b/a.js", '
            '"console.log(1)").replace("b/", ""));\n'
            'console.log(hashedName("a.js", "1") === hashedName("a.js", "2"));\n',
  'hint': "Найдите последнюю точку в базовом имени; slice(0, i) + '.' + hash + slice(i).",
  'expected': ['app.0a286891.js',
               'dist/a.b.7c9804.css',
               'LICENSE.e5dcffe8',
               '.env.23a4',
               'dir.v2/file.2d711642',
               'true',
               'false']},
 {'id': 'j26-manifest',
  'mode': 'js',
  'title': 'Манифест сборки и HTML',
  'statement': 'Напишите buildManifest(files) и rewriteHtml(html, manifest) (node:crypto). files — '
               '{ имя: содержимое }; buildManifest возвращает { имя: хешированное имя } для всех '
               'файлов с расширением (по правилу «имя.<первые 8 hex sha256>.расширение»), ключи в '
               'порядке files. rewriteHtml заменяет значения атрибутов src и href (в двойных или '
               'одинарных кавычках), равные ключу манифеста, на хешированное имя; остальные '
               'атрибуты и ссылки не меняются.',
  'starter': 'import { createHash } from "node:crypto";\n'
             'function buildManifest(files) {\n'
             '}\n'
             'function rewriteHtml(html, manifest) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const files = { "app.js": "console.log(1)", "style.css": "body{}", "logo.svg": '
            '"<svg/>", "README": "x" };\n'
            'const m = buildManifest(files);\n'
            'console.log(JSON.stringify(m));\n'
            'const html = \'<link href="style.css" rel="stylesheet"><script '
            'src=\\\'app.js\\\'></script><img src="logo.svg" alt="app.js"><a '
            'href="other.html">x</a><script src="missing.js"></script>\';\n'
            'console.log(rewriteHtml(html, m));\n',
  'hint': 'Регулярка /\\b(src|href)=([\'"])([^\'"]*)\\2/g с функцией замены.',
  'expected': ['{"app.js":"app.0a286891.js","style.css":"style.7c98040a.css","logo.svg":"logo.d4dc5666.svg"}',
               '<link href="style.7c98040a.css" rel="stylesheet"><script '
               'src=\'app.0a286891.js\'></script><img src="logo.d4dc5666.svg" alt="app.js"><a '
               'href="other.html">x</a><script src="missing.js"></script>']},
 {'id': 'j26-split-shared',
  'mode': 'js',
  'title': 'Общий чанк для нескольких входов',
  'statement': 'Напишите splitChunks(graph, entries): graph — { modules: { путь: { deps } } }, '
               'entries — массив входных модулей. Для каждого входа найдите множество достижимых '
               'по deps модулей (включая сам вход). Модуль, достижимый из двух и более входов, '
               "попадает в чанк 'shared'; остальные — в чанк своего входа (имя чанка — путь "
               "входа). Результат — { имя чанка: отсортированный массив модулей }; чанк 'shared' "
               "включается только если он не пуст; ключи отсортированы, при этом 'shared' идёт "
               'первым. Входной модуль, достижимый из другого входа, тоже считается общим.',
  'starter': 'function splitChunks(graph, entries) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const g = { modules: {\n'
            '  "a.js": { deps: ["ui.js", "util.js"] }, "b.js": { deps: ["util.js", "api.js"] }, '
            '"c.js": { deps: ["a.js"] },\n'
            '  "ui.js": { deps: ["util.js"] }, "util.js": { deps: [] }, "api.js": { deps: [] },\n'
            '} };\n'
            'console.log(JSON.stringify(splitChunks(g, ["a.js", "b.js"])));\n'
            'console.log(JSON.stringify(splitChunks(g, ["b.js"])));\n'
            'console.log(JSON.stringify(splitChunks(g, ["c.js", "a.js"])));\n'
            'console.log(JSON.stringify(splitChunks(g, [])));\n',
  'hint': 'Посчитайте для каждого модуля, из скольких входов он достижим.',
  'expected': ['{"shared":["util.js"],"a.js":["a.js","ui.js"],"b.js":["api.js","b.js"]}',
               '{"b.js":["api.js","b.js","util.js"]}',
               '{"shared":["a.js","ui.js","util.js"],"c.js":["c.js"]}',
               '{}']},
 {'id': 'j26-async-chunks',
  'mode': 'js',
  'title': 'Асинхронные чанки',
  'statement': 'Напишите asyncChunks(graph, entry): graph — { modules: { путь: { deps, dynamic } } '
               '}. main — все модули, достижимые от entry по статическим deps (включая entry). '
               'Динамические цели (из dynamic любого модуля, попавшего в main или в уже найденный '
               'асинхронный чанк) начинают асинхронные чанки: чанк цели — модули, достижимые от '
               'неё по статическим deps и не входящие в main. Модуль, достижимый из нескольких '
               'асинхронных чанков, достаётся тому, чья цель раньше по алфавиту. Цель, уже '
               'входящая в main, чанка не создаёт. Результат { main, async } — main отсортирован, '
               'async — { цель: отсортированный массив } с ключами по алфавиту.',
  'starter': 'function asyncChunks(graph, entry) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const g = { modules: {\n'
            '  main: { deps: ["a", "shared"], dynamic: ["editor", "settings"] },\n'
            '  a: { deps: [], dynamic: [] }, shared: { deps: [], dynamic: [] },\n'
            '  editor: { deps: ["shared", "toolbar", "common"], dynamic: ["preview"] },\n'
            '  settings: { deps: ["common", "form"], dynamic: [] },\n'
            '  preview: { deps: ["common"], dynamic: ["main"] },\n'
            '  toolbar: { deps: [], dynamic: [] }, common: { deps: [], dynamic: [] }, form: { '
            'deps: [], dynamic: [] },\n'
            '} };\n'
            'console.log(JSON.stringify(asyncChunks(g, "main")));\n'
            'console.log(JSON.stringify(asyncChunks(g, "a")));\n',
  'hint': 'Сначала main; затем итерация: найти цели в main и в чанках, обрабатывать цели по '
          'алфавиту.',
  'expected': ['{"main":["a","main","shared"],"async":{"editor":["common","editor","toolbar"],"preview":["preview"],"settings":["form","settings"]}}',
               '{"main":["a"],"async":{}}']},
 {'id': 'j26-budgets',
  'mode': 'js',
  'title': 'Бюджеты размера',
  'statement': 'Напишите checkBudgets(sizes, budgets): sizes — { файл: байты }, budgets — { '
               'шаблон: максимум байт }. Шаблон — точное имя или маска «*.расширение» '
               '(оканчивается на указанное, например «*.css»). Для каждого файла применяется самый '
               'строгий (минимальный) из подходящих бюджетов. Нарушение — размер больше максимума '
               '(равный допустим): строка «файл: размер > максимум». Верните отсортированный '
               'массив строк.',
  'starter': 'function checkBudgets(sizes, budgets) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const sizes = { "main.js": 210000, "vendor.js": 450000, "app.css": 30000, '
            '"extra.css": 70000, "logo.png": 5000, "tiny.js": 100 };\n'
            'const budgets = { "*.js": 300000, "vendor.js": 400000, "*.css": 60000, "main.js": '
            '250000, "tiny.js": 100 };\n'
            'console.log(JSON.stringify(checkBudgets(sizes, budgets)));\n'
            'console.log(JSON.stringify(checkBudgets(sizes, {})), JSON.stringify(checkBudgets({}, '
            'budgets)));\n'
            'console.log(JSON.stringify(checkBudgets({ "a.js": 11 }, { "*.js": 10, "a.js": 20 '
            '})));\n',
  'hint': 'Для файла отфильтруйте подходящие шаблоны и возьмите min максимумов.',
  'expected': ['["extra.css: 70000 > 60000","vendor.js: 450000 > 300000"]',
               '[] []',
               '["a.js: 11 > 10"]']},
 {'id': 'j26-vlq',
  'mode': 'js',
  'title': 'VLQ для source map',
  'statement': 'Напишите encodeVlq(n) и decodeVlq(str). Кодирование — Base64 VLQ как в source map: '
               'знак переносится в младший бит (v = n < 0 ? ((-n) << 1) | 1 : n << 1), затем число '
               'разбивается на группы по 5 бит от младших; в каждой группе 5 бит данных и старший '
               '(шестой) бит продолжения; группы кодируются алфавитом A–Z a–z 0–9 + /. '
               'decodeVlq(str) разбирает строку в массив чисел (в строке может быть несколько '
               'значений подряд).',
  'starter': 'function encodeVlq(n) {\n}\nfunction decodeVlq(str) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'for (const n of [0, 1, -1, 15, 16, -16, 31, 32, 123, -123, 1000, 100000]) '
            'console.log(n, encodeVlq(n), JSON.stringify(decodeVlq(encodeVlq(n))));\n'
            'console.log(JSON.stringify(decodeVlq("AAgBC")));\n'
            'console.log(JSON.stringify(decodeVlq("")));\n'
            'console.log(encodeVlq(0) + encodeVlq(0) + encodeVlq(16) + encodeVlq(1));\n',
  'hint': 'Алфавит base64; бит продолжения — 32; при декодировании накапливайте сдвигами по 5.',
  'expected': ['0 A [0]',
               '1 C [1]',
               '-1 D [-1]',
               '15 e [15]',
               '16 gB [16]',
               '-16 hB [-16]',
               '31 +B [31]',
               '32 gC [32]',
               '123 2H [123]',
               '-123 3H [-123]',
               '1000 w+B [1000]',
               '100000 gqjG [100000]',
               '[0,0,16,1]',
               '[]',
               'AAgBC']},
 {'id': 'j26-decode-mappings',
  'mode': 'js',
  'title': 'Разбор mappings',
  'statement': 'Напишите decodeMappings(mappings): строка mappings из source map — строки '
               'результата разделены «;», сегменты в строке — «,», каждый сегмент — 1, 4 или 5 '
               'чисел в VLQ (уже есть decodeVlq). Значения относительные: колонка в '
               'сгенерированном файле накапливается внутри строки (на каждой новой строке '
               'сбрасывается в 0), индекс источника, строка и колонка в источнике, индекс имени '
               'накапливаются по всему тексту. Верните массив строк, каждая — массив сегментов; '
               'сегмент — массив абсолютных чисел той же длины, что в записи. Пустая строка между '
               '«;» — пустой массив.',
  'starter': 'const B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";\n'
             '// Готово: разбор строки VLQ в массив чисел (не изменяйте)\n'
             'function decodeVlq(str) {\n'
             '  const out = [];\n'
             '  let shift = 0, value = 0;\n'
             '  for (const ch of str) {\n'
             '    const d = B64.indexOf(ch);\n'
             '    value += (d & 31) << shift;\n'
             '    if (d & 32) shift += 5;\n'
             '    else {\n'
             '      out.push(value & 1 ? -(value >>> 1) : value >>> 1);\n'
             '      shift = 0;\n'
             '      value = 0;\n'
             '    }\n'
             '  }\n'
             '  return out;\n'
             '}\n'
             'function decodeMappings(mappings) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(JSON.stringify(decodeMappings("AAAA,SAASA,EAAE;AACX;;AAEA")));\n'
            'console.log(JSON.stringify(decodeMappings("")));\n'
            'console.log(JSON.stringify(decodeMappings("A;;;C")));\n'
            'console.log(JSON.stringify(decodeMappings("AAAA;AAAA,GACA")));\n',
  'hint': 'Состояние [src, line, col, name] вне цикла по строкам; genCol — внутри строки.',
  'expected': ['[[[0,0,0,0],[9,0,0,9,0],[11,0,0,11]],[[0,0,1,0]],[],[[0,0,3,0]]]',
               '[[]]',
               '[[[0]],[],[],[[1]]]',
               '[[[0,0,0,0]],[[0,0,0,0],[3,0,1,0]]]']},
 {'id': 'j26-alias',
  'mode': 'js',
  'title': 'Алиасы путей',
  'statement': 'Напишите resolveAlias(spec, aliases): aliases — { ключ: замена }. Ключ с «$» на '
               'конце («react$») совпадает только со спецификатором в точности «react». Обычный '
               'ключ совпадает со спецификатором, равным ключу, или начинающимся с ключ + «/» '
               '(тогда остаток после ключа сохраняется). Побеждает самый длинный подходящий ключ '
               '(без учёта «$»). Нет совпадения — спецификатор не меняется.',
  'starter': 'function resolveAlias(spec, aliases) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const al = { "@": "/src", "@/utils": "/src/lib/utils", react$: "preact/compat", '
            'lodash: "lodash-es", "~assets": "/static" };\n'
            'for (const s of ["@/components/Button", "@/utils/date", "@", "react", '
            '"react/jsx-runtime", "lodash", "lodash/fp", "~assets/logo.png", "@scope/pkg", '
            '"other", "@/utilsX"]) console.log(s, "→", resolveAlias(s, al));\n',
  'hint': 'Переберите ключи, вычислите совпадение и длину; запомните лучший.',
  'expected': ['@/components/Button → /src/components/Button',
               '@/utils/date → /src/lib/utils/date',
               '@ → /src',
               'react → preact/compat',
               'react/jsx-runtime → react/jsx-runtime',
               'lodash → lodash-es',
               'lodash/fp → lodash-es/fp',
               '~assets/logo.png → /static/logo.png',
               '@scope/pkg → @scope/pkg',
               'other → other',
               '@/utilsX → /src/utilsX']},
 {'id': 'j26-externals',
  'mode': 'js',
  'title': 'Внешние зависимости',
  'statement': 'Напишите splitImports(specs, externals): specs — массив спецификаторов; externals '
               '— массив строк и RegExp. Строка-внешняя совпадает со спецификатором, равным ей, '
               'или начинающимся с строка + «/» (подпути пакета); RegExp — если спецификатор '
               'проходит .test. Встроенные модули («node:…») всегда внешние. Относительные '
               '(начинаются с «.» или «/») всегда включаются в бандл. Результат { bundled, '
               'external } — уникальные спецификаторы в порядке первого появления.',
  'starter': 'function splitImports(specs, externals) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const specs = ["react", "react/jsx-runtime", "react-dom", "./local", "../up", '
            '"lodash", "node:fs", "date-fns/format", "react", "@scope/pkg", "/abs.js"];\n'
            'console.log(JSON.stringify(splitImports(specs, ["react", /^date-fns/, '
            '"@scope/pkg"])));\n'
            'console.log(JSON.stringify(splitImports(specs, [])));\n'
            'console.log(JSON.stringify(splitImports([], ["x"])));\n',
  'hint': 'Функция isExternal(spec); затем распределение с Set для уникальности.',
  'expected': ['{"bundled":["react-dom","./local","../up","lodash","/abs.js"],"external":["react","react/jsx-runtime","node:fs","date-fns/format","@scope/pkg"]}',
               '{"bundled":["react","react/jsx-runtime","react-dom","./local","../up","lodash","date-fns/format","@scope/pkg","/abs.js"],"external":["node:fs"]}',
               '{"bundled":[],"external":[]}']},
 {'id': 'j26-define',
  'mode': 'js',
  'title': 'Подстановка констант (define)',
  'statement': "Напишите applyDefines(code, defines): defines — { 'process.env.NODE_ENV': "
               "'production', 'import.meta.env.MODE': 'build', 'DEBUG': false, 'VERSION': "
               'undefined }. Каждое вхождение ключа в тексте заменяется на '
               'JSON.stringify(значение) (для undefined — слово undefined). Заменяется только '
               'целое выражение: перед ключом не должно стоять символ [A-Za-z0-9_$.], а после — '
               '[A-Za-z0-9_$]. Более длинные ключи имеют приоритет (чтобы «process.env» не '
               'перехватил «process.env.NODE_ENV»). Содержимое строк в кавычках не изменяется.',
  'starter': 'function applyDefines(code, defines) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const defs = { "process.env.NODE_ENV": "production", "process.env": { A: 1 }, '
            '"import.meta.env.MODE": "build", DEBUG: false, VERSION: undefined };\n'
            'const t = (c) => console.log(applyDefines(c, defs));\n'
            't(\'if (process.env.NODE_ENV !== "production") { DEBUG && log(VERSION); }\');\n'
            "t('const m = import.meta.env.MODE; const e = process.env;');\n"
            't(\'const s = "process.env.NODE_ENV and DEBUG"; x = DEBUG\');\n'
            "t('myprocess.env.NODE_ENV; process.env.NODE_ENVX; obj.DEBUG; DEBUGGER; _DEBUG');\n"
            't("");\n',
  'hint': 'Разберите код на строки-литералы и остальное; в остальном применяйте замены в порядке '
          'убывания длины ключа.',
  'expected': ['if ("production" !== "production") { false && log(undefined); }',
               'const m = "build"; const e = {"A":1};',
               'const s = "process.env.NODE_ENV and DEBUG"; x = false',
               'myprocess.env.NODE_ENV; {"A":1}.NODE_ENVX; obj.DEBUG; DEBUGGER; _DEBUG']},
 {'id': 'j26-hmr',
  'mode': 'js',
  'title': 'Границы горячей замены (HMR)',
  'statement': 'Напишите hmrUpdate(parents, accepts, changed): parents — { модуль: [импортёры] }, '
               'accepts — массив модулей, принимающих обновления (module.hot.accept), changed — '
               "изменившийся модуль. Если changed принимает обновление сам — { type: 'update', "
               'modules: [changed] }. Иначе поднимайтесь по импортёрам: для каждой цепочки вверх '
               'до первого принимающего — он попадает в границу. Если какая-то цепочка доходит до '
               "модуля без импортёров (корня), не встретив принимающего, — { type: 'reload' }. "
               "Если границы найдены по всем цепочкам — { type: 'update', modules } "
               '(отсортированные уникальные). Циклы: уже посещённые модули повторно не обходятся '
               '(не считаются корнем).',
  'starter': 'function hmrUpdate(parents, accepts, changed) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const parents = { util: ["page", "widget"], page: ["app"], widget: ["app"], app: [], '
            'style: ["page", "other"], other: [], loopA: ["loopB"], loopB: ["loopA", "root2"], '
            'root2: [] };\n'
            'const t = (ch, acc) => console.log(ch, JSON.stringify(hmrUpdate(parents, acc, ch)));\n'
            't("util", ["util"]); t("util", ["page", "widget"]); t("util", ["page"]); t("util", '
            '["app"]); t("util", []);\n'
            't("style", ["page", "other"]); t("style", ["page"]); t("loopA", ["loopB"]); '
            't("loopA", []); t("loopA", ["root2"]);\n'
            't("ghost", []); t("ghost", ["ghost"]);\n',
  'hint': 'Обход вверх с visited; корень — модуль, у которого нет импортёров (parents[m] пуст или '
          'отсутствует).',
  'expected': ['util {"type":"update","modules":["util"]}',
               'util {"type":"update","modules":["page","widget"]}',
               'util {"type":"reload"}',
               'util {"type":"update","modules":["app"]}',
               'util {"type":"reload"}',
               'style {"type":"update","modules":["other","page"]}',
               'style {"type":"reload"}',
               'loopA {"type":"update","modules":["loopB"]}',
               'loopA {"type":"reload"}',
               'loopA {"type":"update","modules":["root2"]}',
               'ghost {"type":"reload"}',
               'ghost {"type":"update","modules":["ghost"]}']},
 {'id': 'j26-targets',
  'mode': 'js',
  'title': 'Нужна ли транспиляция',
  'statement': 'Напишите needsTranspile(features, targets). Таблица минимальных версий задана '
               'константой MIN (в заготовке): feature → { браузер: версия }. targets — { браузер: '
               'версия } (например { chrome: 70, safari: 13 }). Возможность требует '
               'преобразования, если хотя бы для одного браузера из targets: браузера нет в '
               'MIN[feature] (не поддерживает) или версия цели меньше минимальной. Неизвестная '
               'возможность (нет в MIN) — требует преобразования. Верните отсортированный массив '
               'имён возможностей из features, которые требуют преобразования.',
  'starter': 'const MIN = {\n'
             '  "optional-chaining": { chrome: 80, firefox: 74, safari: 13.1 },\n'
             '  "nullish": { chrome: 80, firefox: 72, safari: 13.1 },\n'
             '  "class-fields": { chrome: 72, firefox: 69, safari: 14.1 },\n'
             '  "top-level-await": { chrome: 89, firefox: 89, safari: 15 },\n'
             '  "bigint": { chrome: 67, firefox: 68, safari: 14 },\n'
             '  "private-methods": { chrome: 84, firefox: 90, safari: 15 },\n'
             '};\n'
             'function needsTranspile(features, targets) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (f, tg) => console.log(JSON.stringify(tg), JSON.stringify(needsTranspile(f, '
            'tg)));\n'
            'const all = ["optional-chaining", "nullish", "class-fields", "top-level-await", '
            '"bigint", "private-methods"];\n'
            't(all, { chrome: 100, firefox: 100, safari: 16 });\n'
            't(all, { chrome: 70 });\n'
            't(all, { safari: 14 });\n'
            't(all, { chrome: 85, edge: 90 });\n'
            't(["unknown-feature", "bigint"], { chrome: 90 });\n'
            't(all, {});\n'
            't(["bigint"], { safari: 13.1, firefox: 68 });\n',
  'hint': 'every/some по браузерам цели; Object.hasOwn(MIN, feature).',
  'expected': ['{"chrome":100,"firefox":100,"safari":16} []',
               '{"chrome":70} '
               '["class-fields","nullish","optional-chaining","private-methods","top-level-await"]',
               '{"safari":14} ["class-fields","private-methods","top-level-await"]',
               '{"chrome":85,"edge":90} '
               '["bigint","class-fields","nullish","optional-chaining","private-methods","top-level-await"]',
               '{"chrome":90} ["unknown-feature"]',
               '{} []',
               '{"safari":13.1,"firefox":68} ["bigint"]']},
 {'id': 'j26-top-modules',
  'mode': 'js',
  'title': 'Самые тяжёлые модули',
  'statement': 'Напишите topModules(sizes, n): sizes — { путь: байты }. Верните массив { path, '
               'bytes, percent } для n самых больших модулей (по убыванию байт, при равенстве — по '
               'пути), percent — доля от общей суммы всех модулей с округлением до 1 знака. Если '
               "модулей больше n, добавьте в конец запись { path: '(others)', bytes: сумма "
               'остальных, percent } (процент тоже с округлением до 1 знака). Общая сумма 0 — '
               'percent у всех 0.',
  'starter': 'function topModules(sizes, n) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const s = { "a.js": 500, "b.js": 300, "c.js": 100, "d.js": 60, "e.js": 40, "f.js": 0 '
            '};\n'
            'console.log(JSON.stringify(topModules(s, 2)));\n'
            'console.log(JSON.stringify(topModules(s, 10)));\n'
            'console.log(JSON.stringify(topModules({ x: 1, y: 1 }, 1)));\n'
            'console.log(JSON.stringify(topModules({ z: 0 }, 1)));\n'
            'console.log(JSON.stringify(topModules({}, 3)));\n',
  'hint': 'Сортировка, slice, затем сумма хвоста; round1 = x => Math.round(x * 10) / 10.',
  'expected': ['[{"path":"a.js","bytes":500,"percent":50},{"path":"b.js","bytes":300,"percent":30},{"path":"(others)","bytes":200,"percent":20}]',
               '[{"path":"a.js","bytes":500,"percent":50},{"path":"b.js","bytes":300,"percent":30},{"path":"c.js","bytes":100,"percent":10},{"path":"d.js","bytes":60,"percent":6},{"path":"e.js","bytes":40,"percent":4},{"path":"f.js","bytes":0,"percent":0}]',
               '[{"path":"x","bytes":1,"percent":50},{"path":"(others)","bytes":1,"percent":50}]',
               '[{"path":"z","bytes":0,"percent":0}]',
               '[]']},
 {'id': 'j26-package-sizes',
  'mode': 'js',
  'title': 'Размер бандла по пакетам',
  'statement': 'Напишите sizeByPackage(sizes): sizes — { путь модуля: байты }. Пакет определяется '
               'по последнему «node_modules/» в пути: имя — следующий сегмент, а для области '
               '«@scope» — два сегмента («@scope/pkg»). Модули без node_modules относятся к '
               '«(app)». Суммируйте байты по пакетам. Результат — массив [имя, байты], по убыванию '
               'байт, при равенстве по имени.',
  'starter': 'function sizeByPackage(sizes) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const s = {\n'
            '  "src/main.js": 1000, "src/ui/button.js": 500,\n'
            '  "node_modules/react/index.js": 4000, "node_modules/react/jsx.js": 500,\n'
            '  "node_modules/@scope/pkg/lib/a.js": 700, "node_modules/@scope/pkg/lib/b.js": 300,\n'
            '  "node_modules/a/node_modules/react/index.js": 3000, "node_modules/lodash/fp.js": '
            '2500, "node_modules/ms/index.js": 5,\n'
            '};\n'
            'console.log(JSON.stringify(sizeByPackage(s)));\n'
            'console.log(JSON.stringify(sizeByPackage({})));\n',
  'hint': "lastIndexOf('node_modules/'), затем разберите сегменты после него.",
  'expected': ['[["react",7500],["lodash",2500],["(app)",1500],["@scope/pkg",1000],["ms",5]]',
               '[]']},
 {'id': 'j26-glob',
  'mode': 'js',
  'title': 'Шаблоны путей (glob)',
  'statement': 'Напишите globToRegExp(glob): RegExp, который целиком (с ^ и $) соответствует путям '
               'по маске. «*» — любые символы кроме «/» (включая пустую последовательность); «**» '
               '— любые символы, включая «/»; «**/» — ноль или больше каталогов (например '
               '«src/**/x.js» подходит и к «src/x.js», и к «src/a/b/x.js»); «?» — один символ '
               'кроме «/». Остальные символы — буквально (спецсимволы регулярных выражений '
               'экранируйте).',
  'starter': 'function globToRegExp(glob) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (g, p) => console.log(g, p, globToRegExp(g).test(p));\n'
            't("*.js", "a.js"); t("*.js", "src/a.js"); t("src/*.js", "src/a.js"); t("src/*.js", '
            '"src/x/a.js"); t("src/**/*.js", "src/a.js"); t("src/**/*.js", "src/x/y/a.js");\n'
            't("**/*.css", "a.css"); t("**/*.css", "d/e/a.css"); t("a?c", "abc"); t("a?c", "a/c"); '
            't("file.min.js", "file.min.js"); t("file.min.js", "fileXminXjs");\n'
            't("src/**", "src/a/b/c"); t("src/**", "src"); t("(x)+.js", "(x)+.js"); t("*", ""); '
            't("a*b", "a/b");\n',
  'hint': 'Идите по символам маски и собирайте строку регулярного выражения; для «**/» используйте '
          '(?:.*/)?',
  'expected': ['*.js a.js true',
               '*.js src/a.js false',
               'src/*.js src/a.js true',
               'src/*.js src/x/a.js false',
               'src/**/*.js src/a.js true',
               'src/**/*.js src/x/y/a.js true',
               '**/*.css a.css true',
               '**/*.css d/e/a.css true',
               'a?c abc true',
               'a?c a/c false',
               'file.min.js file.min.js true',
               'file.min.js fileXminXjs false',
               'src/** src/a/b/c true',
               'src/** src false',
               '(x)+.js (x)+.js true',
               '*  true',
               'a*b a/b false']},
 {'id': 'j26-side-effects',
  'mode': 'js',
  'title': 'Файлы с побочными эффектами',
  'statement': 'Напишите hasSideEffects(file, sideEffects). sideEffects — значение поля '
               'package.json: true или не задано — у любого файла есть эффекты; false — нет; '
               'массив шаблонов — эффекты только у файлов, подходящих хотя бы под один шаблон. '
               'Шаблон без «/» сравнивается с именем файла (последним сегментом пути) в любом '
               'каталоге; шаблон с «/» — с полным относительным путём (ведущее «./» у шаблона '
               'отбрасывается). Маски — как в globToRegExp (он уже есть в заготовке).',
  'starter': 'function globToRegExp(glob) {\n'
             '  let re = "";\n'
             '  for (let i = 0; i < glob.length; i++) {\n'
             '    const c = glob[i];\n'
             '    if (c === "*") {\n'
             '      if (glob[i + 1] === "*") {\n'
             '        i++;\n'
             '        if (glob[i + 1] === "/") { i++; re += "(?:.*/)?"; } else re += ".*";\n'
             '      } else re += "[^/]*";\n'
             '    } else if (c === "?") re += "[^/]";\n'
             '    else re += c.replace(/[.+^${}()|[\\]\\\\]/g, "\\\\$&");\n'
             '  }\n'
             '  return new RegExp("^" + re + "$");\n'
             '}\n'
             'function hasSideEffects(file, sideEffects) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (f, se) => console.log(f, JSON.stringify(se), hasSideEffects(f, se));\n'
            'const list = ["*.css", "./src/polyfills.js", "setup/**/*.js"];\n'
            't("a.js", true); t("a.js", undefined); t("a.js", false); t("src/ui/a.css", list); '
            't("a.css", list); t("src/polyfills.js", list); t("lib/polyfills.js", list);\n'
            't("setup/x/init.js", list); t("setup/init.js", list); t("src/main.js", list); '
            't("src/main.js", []);\n',
  'hint': 'Для массива: по каждому шаблону выберите, с чем сравнивать — basename или весь путь.',
  'expected': ['a.js true true',
               'a.js undefined true',
               'a.js false false',
               'src/ui/a.css ["*.css","./src/polyfills.js","setup/**/*.js"] true',
               'a.css ["*.css","./src/polyfills.js","setup/**/*.js"] true',
               'src/polyfills.js ["*.css","./src/polyfills.js","setup/**/*.js"] true',
               'lib/polyfills.js ["*.css","./src/polyfills.js","setup/**/*.js"] false',
               'setup/x/init.js ["*.css","./src/polyfills.js","setup/**/*.js"] true',
               'setup/init.js ["*.css","./src/polyfills.js","setup/**/*.js"] true',
               'src/main.js ["*.css","./src/polyfills.js","setup/**/*.js"] false',
               'src/main.js [] false']},
 {'id': 'j26-css-modules',
  'mode': 'js',
  'title': 'CSS Modules: локальные имена',
  'statement': 'Напишите scopeCss(css, file) (node:crypto). Каждый селектор-класс «.имя» (имя '
               'начинается с буквы или «_», затем буквы, цифры, «-», «_»; точка не должна быть '
               'частью числа, как в «1.5em», и не внутри url(…) или кавычек — в тестах таких '
               'случаев нет, кроме чисел) заменяется на «.имя_ХХХХХ», где ХХХХХ — первые 5 '
               'hex-символов sha1 от строки `${file}:${имя}`. Верните { css, map }: map — { '
               'исходное имя: новое имя (без точки) } в порядке первого появления. Числа вида '
               '«.5s» (после точки цифра) не трогайте.',
  'starter': 'import { createHash } from "node:crypto";\nfunction scopeCss(css, file) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const r = scopeCss(".btn { margin: 1.5em; transition: .5s }\\n.btn:hover, '
            '.btn-primary > .icon { color: red }\\n.icon_big { width: 10px }", "ui/button.css");\n'
            'console.log(r.css);\n'
            'console.log(JSON.stringify(r.map));\n'
            'const r2 = scopeCss(".btn {}", "other.css");\n'
            'console.log(r2.map.btn !== r.map.btn, r2.css);\n'
            'console.log(JSON.stringify(scopeCss("a { color: red }", "x.css")));\n',
  'hint': 'css.replace(/(?<![\\w])\\.([A-Za-z_][\\w-]*)/g, …) — не трогает «1.5em» и «.5s».',
  'expected': ['.btn_a814f { margin: 1.5em; transition: .5s }',
               '.btn_a814f:hover, .btn-primary_6925f > .icon_b2e11 { color: red }',
               '.icon_big_7a859 { width: 10px }',
               '{"btn":"btn_a814f","btn-primary":"btn-primary_6925f","icon":"icon_b2e11","icon_big":"icon_big_7a859"}',
               'true .btn_d5d19 {}',
               '{"css":"a { color: red }","map":{}}']},
 {'id': 'j26-inline-asset',
  'mode': 'js',
  'title': 'Встраивание ресурсов',
  'statement': 'Напишите inlineAsset(name, bytes, mime, limit) (node:crypto): bytes — Buffer. Если '
               'bytes.length ≤ limit — вернуть data-URL «data:MIME;base64,…» '
               "(Buffer.toString('base64')). Иначе — путь «/assets/ИМЯ.ХЕШ.РАСШИРЕНИЕ», где ИМЯ — "
               'имя файла без расширения и каталога, ХЕШ — первые 8 hex-символов sha256 от bytes, '
               'РАСШИРЕНИЕ — после последней точки (если расширения нет — путь «/assets/ИМЯ.ХЕШ»).',
  'starter': 'import { createHash } from "node:crypto";\n'
             'function inlineAsset(name, bytes, mime, limit) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const small = Buffer.from("hi");\n'
            'const big = Buffer.alloc(100, 7);\n'
            'console.log(inlineAsset("icons/a.svg", small, "image/svg+xml", 10));\n'
            'console.log(inlineAsset("icons/logo.big.png", big, "image/png", 10));\n'
            'console.log(inlineAsset("LICENSE", big, "text/plain", 99));\n'
            'console.log(inlineAsset("x.bin", Buffer.alloc(10), "application/octet-stream", '
            '10).slice(0, 30));\n'
            'console.log(inlineAsset("x.bin", Buffer.alloc(11), "application/octet-stream", '
            '10));\n',
  'hint': 'Базовое имя — после последнего «/»; расширение — после последней «.» в нём.',
  'expected': ['data:image/svg+xml;base64,aGk=',
               '/assets/logo.big.d876885b.png',
               '/assets/LICENSE.d876885b',
               'data:application/octet-stream;',
               '/assets/x.71b6c1d5.bin']},
 {'id': 'j26-polyfills',
  'mode': 'js',
  'title': 'Какие полифилы нужны',
  'statement': 'Напишите neededPolyfills(code, targets). В заготовке даны таблицы API: имя → { '
               'регулярное выражение обнаружения, минимальные версии браузеров }. Для каждого API, '
               'чьё выражение находит совпадение в code, проверьте targets ({ браузер: версия }): '
               'полифил нужен, если для какого-то браузера из targets его нет в таблице версий или '
               'версия цели меньше минимальной. Верните отсортированный массив имён нужных '
               'полифилов. Пустые targets — [].',
  'starter': 'const APIS = {\n'
             '  "Promise.allSettled": { re: /Promise\\.allSettled\\b/, min: { chrome: 76, firefox: '
             '71, safari: 13 } },\n'
             '  "Array.prototype.at": { re: /\\.at\\(/, min: { chrome: 92, firefox: 90, safari: '
             '15.4 } },\n'
             '  "structuredClone": { re: /\\bstructuredClone\\(/, min: { chrome: 98, firefox: 94, '
             'safari: 15.4 } },\n'
             '  "Object.hasOwn": { re: /Object\\.hasOwn\\(/, min: { chrome: 93, firefox: 92, '
             'safari: 15.4 } },\n'
             '  "String.prototype.replaceAll": { re: /\\.replaceAll\\(/, min: { chrome: 85, '
             'firefox: 77, safari: 13.1 } },\n'
             '};\n'
             'function neededPolyfills(code, targets) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const code = "const r = await Promise.allSettled(xs); const last = arr.at(-1); const '
            's = text.replaceAll(\'a\', \'b\'); Object.hasOwn(o, \'k\');";\n'
            'const t = (c, tg) => console.log(JSON.stringify(tg), '
            'JSON.stringify(neededPolyfills(c, tg)));\n'
            't(code, { chrome: 100, firefox: 100, safari: 16 });\n'
            't(code, { chrome: 80 });\n'
            't(code, { safari: 14, firefox: 78 });\n'
            't(code, { edge: 100 });\n'
            't(code, {});\n'
            't("structuredClone(x)", { chrome: 97 });\n'
            't("nothing here", { chrome: 1 });\n',
  'hint': 'Фильтр по re.test(code), затем some по браузерам цели.',
  'expected': ['{"chrome":100,"firefox":100,"safari":16} []',
               '{"chrome":80} ["Array.prototype.at","Object.hasOwn","String.prototype.replaceAll"]',
               '{"safari":14,"firefox":78} ["Array.prototype.at","Object.hasOwn"]',
               '{"edge":100} '
               '["Array.prototype.at","Object.hasOwn","Promise.allSettled","String.prototype.replaceAll"]',
               '{} []',
               '{"chrome":97} ["structuredClone"]',
               '{"chrome":1} []']},
 {'id': 'j26-compare-builds',
  'mode': 'js',
  'title': 'Сравнение двух сборок',
  'statement': 'Напишите compareBuilds(before, after, threshold = 0.05): before и after — { чанк: '
               'байты }. Верните { added, removed, changed, regressions, total }. added — чанки '
               'только в after, removed — только в before (отсортированы); changed — для чанков в '
               'обеих сборках с различным размером объекты { name, before, after, delta, percent } '
               '(delta = after − before, percent = delta / before × 100 с округлением до 1 знака; '
               'before = 0 — percent 0), отсортированы по имени; regressions — имена из changed, у '
               'которых delta / before > threshold (before > 0), отсортированы; total — { before, '
               'after, delta } по суммам всех чанков.',
  'starter': 'function compareBuilds(before, after, threshold = 0.05) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const b = { "main.js": 100000, "vendor.js": 300000, "old.js": 5000, "same.js": 1000, '
            '"zero.js": 0 };\n'
            'const a = { "main.js": 112000, "vendor.js": 290000, "new.js": 85000, "same.js": 1000, '
            '"zero.js": 10 };\n'
            'console.log(JSON.stringify(compareBuilds(b, a)));\n'
            'console.log(JSON.stringify(compareBuilds(b, a, 0.2).regressions));\n'
            'console.log(JSON.stringify(compareBuilds({}, {})));\n',
  'hint': 'Объедините ключи; для общих сравните размеры; суммы считайте по всем чанкам.',
  'expected': ['{"added":["new.js"],"removed":["old.js"],"changed":[{"name":"main.js","before":100000,"after":112000,"delta":12000,"percent":12},{"name":"vendor.js","before":300000,"after":290000,"delta":-10000,"percent":-3.3},{"name":"zero.js","before":0,"after":10,"delta":10,"percent":0}],"regressions":["main.js"],"total":{"before":406000,"after":488010,"delta":82010}}',
               '[]',
               '{"added":[],"removed":[],"changed":[],"regressions":[],"total":{"before":0,"after":0,"delta":0}}']}]}
