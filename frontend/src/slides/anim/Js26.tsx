import { scene } from "./alg.tsx";
import { Box, Tx, arrow, jc } from "./jv.tsx";

/* Глава 26 книги «Современный Frontend»: сборщики — webpack, Rollup, esbuild, Vite. */

const code = { w: 340, size: 9.5, lh: 14 };
const mod = (id: string, x: number, y: number, t: string, c = "b") => Box(id, x, y, 56, 26, t, c, { size: 9.5 });

// 1. Зачем сборщик
export const V01 = scene({
  labels: ["Сотни модулей", "Преобразования", "Результат"],
  caption: [
    "Тысячи модулей — сотни запросов; браузер так загружать неудобно",
    "TypeScript, JSX, стили, картинки, зависимости из node_modules",
    "Вход, обход импортов, преобразование, оптимизация — набор небольших файлов",
  ],
  frames: [
    [...Array.from({ length: 15 }, (_, i) => Box(`m${i}`, 40 + (i % 5) * 70, 50 + Math.floor(i / 5) * 36, 54, 24, `m${i + 1}`, "m", { size: 9 }))],
    [...["TS", "JSX", "CSS", "PNG", "npm"].map((t, i) => Box(`t${i}`, 50 + i * 65, 70, 56, 30, t, "y", { size: 10 })), Tx("n", 180, 120, "→ JavaScript, CSS, ресурсы", { size: 10 })],
    [Box("a", 70, 80, 100, 40, "сборщик", "g", { size: 12 }), arrow("e", 122, 80, 178, 80, "g"), Box("b", 250, 50, 90, 24, "app.a1b2.js", "b", { size: 9 }), Box("c", 250, 80, 90, 24, "vendor.c3d4.js", "b", { size: 9 }), Box("d", 250, 110, 90, 24, "app.e5f6.css", "b", { size: 9 })],
  ],
});

// 2. Граф модулей
export const V02 = scene({
  labels: ["Вход", "Обход импортов", "Разрешение путей"],
  caption: [
    "Точка входа — единственный файл, с которого начинается обход",
    "Каждый import ведёт к следующему файлу: получается граф зависимостей",
    "Относительные пути — от текущего файла, голые имена — в node_modules; расширения и index.js",
  ],
  frames: [
    [mod("e", 180, 40, "main", "g")],
    [mod("e", 180, 30, "main", "g"), mod("a", 100, 80, "app"), mod("b", 260, 80, "util"), mod("c", 60, 130, "ui"), mod("d", 160, 130, "api"), mod("f", 260, 130, "lodash", "y"), arrow("e1", 160, 42, 120, 68, "g"), arrow("e2", 200, 42, 240, 68, "g"), arrow("e3", 80, 92, 68, 118, "g"), arrow("e4", 120, 92, 152, 118, "g"), arrow("e5", 260, 94, 260, 118, "g")],
    [jc("c", 10, 20, ["import \"./util\";       // src/util.js", "import x from \"./ui\";   // src/ui/index.js", "import _ from \"lodash\";  // node_modules/lodash"], [0, 1, 2], { ...code, lh: 24, size: 9 })],
  ],
});

// 3. Бандлинг
export const V03 = scene({
  labels: ["Таблица модулей", "Загрузчик", "Один файл"],
  caption: [
    "Каждый модуль — функция в таблице под своим идентификатором",
    "require(id): вызвать модуль один раз, закэшировать exports",
    "Всё склеено в один файл; импорты стали вызовами require",
  ],
  frames: [
    [jc("c", 10, 20, ["const modules = {", "  1: function (module, exports, require) { … },", "  2: function (module, exports, require) { … },", "};"], [1, 2], { ...code, lh: 22, size: 9 })],
    [jc("c", 10, 20, ["function require(id) {", "  if (cache[id]) return cache[id].exports;", "  const m = (cache[id] = { exports: {} });", "  modules[id](m, m.exports, require);", "  return m.exports;", "}"], [1, 3], { ...code, lh: 17, size: 9 })],
    [Box("a", 70, 40, 90, 22, "main.js", "b", { size: 9.5 }), Box("b", 70, 70, 90, 22, "util.js", "b", { size: 9.5 }), Box("c", 70, 100, 90, 22, "ui.js", "b", { size: 9.5 }), arrow("e", 125, 70, 178, 70, "g"), Box("d", 270, 70, 130, 70, "bundle.js", "g", { size: 12 })],
  ],
});

// 4. Загрузчики и плагины
export const V04 = scene({
  labels: ["Loader", "Plugin", "Хуки Rollup/Vite"],
  caption: [
    "Loader превращает файл в модуль: .ts → .js, .css → модуль, .png → URL",
    "Plugin вмешивается в любой этап: добавляет файлы, подставляет переменные, оптимизирует",
    "resolveId → load → transform → generateBundle: текст на входе, текст на выходе",
  ],
  frames: [
    [Box("a", 70, 70, 100, 36, "app.ts", "b", { size: 11 }), arrow("e", 122, 70, 148, 70, "g"), Box("l", 220, 70, 100, 36, "loader", "g", { size: 11 }), arrow("f", 272, 70, 288, 70, "g"), Box("b", 335, 70, 40, 36, "js", "b", { size: 11 })],
    [jc("c", 10, 20, ["plugins: [", "  define({ \"process.env.NODE_ENV\": '\"production\"' }),", "  minify(),", "]"], [1, 2], { ...code, lh: 22, size: 9 })],
    [...["resolveId", "load", "transform", "generate"].map((t, i) => Box(`h${i}`, 50 + i * 85, 80, 76, 32, t, "g", { size: 9 })), arrow("e1", 88, 80, 92, 80, "m"), arrow("e2", 173, 80, 177, 80, "m"), arrow("e3", 258, 80, 262, 80, "m")],
  ],
});

// 5. Tree shaking
export const V05 = scene({
  labels: ["Один из ста", "Побочные эффекты", "sideEffects: false"],
  caption: [
    "Импортировали одну функцию из библиотеки — остальные в бандл не попали",
    "Модуль, который при загрузке что-то делает, удалить нельзя",
    "Пакет обещает: его модули безопасно отбрасывать, если имена не нужны",
  ],
  frames: [
    [...Array.from({ length: 10 }, (_, i) => Box(`f${i}`, 40 + (i % 5) * 70, 56 + Math.floor(i / 5) * 40, 56, 26, `fn${i + 1}`, i === 2 ? "g" : "m", { size: 9.5 })), Tx("n", 180, 140, "import { fn3 } → в бандле только fn3", { size: 9.5 })],
    [jc("c", 10, 20, ["// polyfill.js", "window.fetch = window.fetch || myFetch;", "// импортирован без имён,", "// но удалить нельзя ✗"], [1], { ...code, lh: 22, size: 9.5, bad: [3] })],
    [jc("c", 10, 20, ["{", "  \"name\": \"my-lib\",", "  \"sideEffects\": false", "}"], [2], { ...code, lh: 24, size: 11 })],
  ],
});

// 6. Минификация
export const V06 = scene({
  labels: ["Короче", "Имена", "Source map"],
  caption: [
    "Убраны пробелы и комментарии, упрощены выражения, удалены мёртвые ветки",
    "Локальные переменные сокращены до одной-двух букв",
    "Карта соответствий: DevTools показывает ваши строки, а не минифицированную кашу",
  ],
  frames: [
    [jc("c", 10, 20, ["// до", "function add(first, second) {", "  return first + second;", "}", "// после: function a(b,c){return b+c}"], [4], { ...code, lh: 20, size: 9.5 })],
    [Box("a", 90, 70, 130, 36, "userAccountBalance", "b", { size: 9.5 }), arrow("e", 156, 70, 180, 70, "g"), Box("b", 270, 70, 90, 36, "a", "g", { size: 14 })],
    [Box("a", 90, 70, 130, 36, "app.min.js:1:4201", "y", { size: 9.5 }), arrow("e", 156, 70, 180, 70, "g"), Box("b", 270, 70, 130, 36, "src/cart.ts:42:7", "g", { size: 9.5 })],
  ],
});

// 7. Разбиение на части
export const V07 = scene({
  labels: ["Один бандл", "Динамический import", "Общий чанк"],
  caption: [
    "Гигантский бандл: пользователь качает всё, даже ненужное",
    "import() создаёт отдельный файл: страница настроек или редактор грузятся по требованию",
    "Код, нужный нескольким частям, выносится в общий чанк и не дублируется",
  ],
  frames: [
    [Box("a", 180, 80, 280, 50, "bundle.js — 2 МБ", "r", { size: 13 })],
    [Box("m", 90, 60, 100, 36, "main.js\n(первый экран)", "g", { size: 9 }), Box("e", 270, 40, 100, 26, "editor.js", "b", { size: 9.5 }), Box("s", 270, 80, 100, 26, "settings.js", "b", { size: 9.5 }), arrow("a1", 140, 56, 218, 42, "m", { dash: true }), arrow("a2", 140, 64, 218, 78, "m", { dash: true }), Tx("n", 180, 130, "import() — по требованию", { size: 9.5 })],
    [Box("a", 80, 50, 100, 26, "page-a.js", "b", { size: 9.5 }), Box("b", 80, 110, 100, 26, "page-b.js", "b", { size: 9.5 }), Box("s", 280, 80, 110, 36, "shared.js", "g", { size: 10 }), arrow("e1", 132, 56, 224, 72, "g"), arrow("e2", 132, 104, 224, 88, "g")],
  ],
});

// 8. Хеши и кэш
export const V08 = scene({
  labels: ["Долгий кэш", "Меняется код", "Манифест"],
  caption: [
    "app.a1b2c3.js: имя содержит хеш содержимого — кэшируем на год",
    "Изменили код — хеш и имя новые: браузер скачает только изменившееся",
    "Манифест сопоставляет app.js → app.a1b2c3.js; страница получает свежие адреса",
  ],
  frames: [
    [Box("a", 90, 70, 150, 36, "app.a1b2c3.js", "g", { size: 11 }), Box("b", 270, 70, 150, 36, "Cache-Control:\nmax-age=1 год", "b", { size: 9.5 })],
    [Box("a", 90, 70, 150, 36, "app.a1b2c3.js → из кэша", "g", { size: 9 }), Box("b", 270, 70, 150, 36, "app.9f8e7d.js → скачать", "y", { size: 9.5 })],
    [jc("c", 10, 30, ["{", "  \"app.js\":    \"app.9f8e7d.js\",", "  \"vendor.js\": \"vendor.4b3a21.js\"", "}"], [1, 2], { ...code, lh: 22, size: 10 })],
  ],
});

// 9. Инструменты
export const V09 = scene({
  labels: ["webpack и Rollup", "esbuild", "Vite"],
  caption: [
    "webpack — гибкость и плагины; Rollup — библиотеки и чистый ESM-вывод",
    "esbuild на Go собирает за доли секунды, плагинов меньше",
    "Vite: esbuild для зависимостей, Rollup для сборки и готовые настройки",
  ],
  frames: [
    [Box("a", 90, 70, 150, 40, "webpack\nгибкость, плагины", "b", { size: 10 }), Box("b", 270, 70, 150, 40, "Rollup\nбиблиотеки, ESM", "b", { size: 10 })],
    [Box("a", 180, 70, 200, 44, "esbuild (Go)\nмиллисекунды", "g", { size: 12 })],
    [Box("a", 90, 70, 150, 40, "dev: нативные ESM\n+ esbuild", "g", { size: 10 }), Box("b", 270, 70, 150, 40, "build: Rollup\n(или Rolldown)", "b", { size: 10 })],
  ],
});

// 10. Сервер разработки
export const V10 = scene({
  labels: ["По запросу", "HMR", "Подъём до родителя"],
  caption: [
    "Браузер просит модуль — dev-сервер преобразует его на лету: старт мгновенный",
    "HMR заменяет изменённый модуль в работающей странице, сохраняя состояние",
    "Не принял обновление — оно поднимается к родителю; в худшем случае — перезагрузка",
  ],
  frames: [
    [Box("b", 70, 80, 100, 36, "браузер", "b", { size: 10 }), arrow("e1", 122, 70, 148, 70, "g"), Box("s", 220, 80, 100, 36, "dev-сервер", "g", { size: 10 }), arrow("e2", 148, 90, 122, 90, "m"), Tx("n", 330, 80, "ESM\nпо запросу", { size: 9 })],
    [mod("a", 90, 60, "app"), mod("b", 90, 110, "cart", "y"), mod("c", 270, 60, "ui"), arrow("e1", 90, 74, 90, 98, "m"), Tx("n", 270, 110, "cart заменён,\nсостояние цело", { size: 9.5, c: "g" })],
    [mod("a", 180, 40, "main", "g"), mod("b", 120, 90, "page", "y"), mod("c", 120, 140, "util", "r"), arrow("e1", 150, 52, 130, 78, "m"), arrow("e2", 120, 102, 120, 128, "m"), Tx("n", 280, 100, "util не принимает →\nвверх до page", { size: 9.5 })],
  ],
});

// 11. Конфигурация
export const V11 = scene({
  labels: ["Подстановка env", "Alias", "external"],
  caption: [
    "process.env.NODE_ENV заменяется константой при сборке; секреты в браузер не кладут",
    "@/ вместо длинных относительных путей",
    "external: пакет не включается в бандл — типично для библиотек",
  ],
  frames: [
    [jc("c", 10, 20, ["if (process.env.NODE_ENV !== \"production\") {", "  console.debug(state);", "}", "// сборка: ложное условие → ветка вырезана"], [0, 3], { ...code, lh: 22, size: 9 })],
    [jc("c", 10, 30, ["alias: { \"@\": \"/src\" }", "", "import { api } from \"@/lib/api\";"], [0, 2], { ...code, lh: 22, size: 10 })],
    [jc("c", 10, 30, ["external: [\"react\", \"react-dom\"]", "// бандл библиотеки без React —", "// его даст приложение"], [0], { ...code, lh: 22, size: 10 })],
  ],
});

// 12. Анализ бандла
export const V12 = scene({
  labels: ["Состав", "Бюджет", "Сравнение"],
  caption: [
    "Визуализатор показывает, какие пакеты занимают место и где дубликаты",
    "Бюджет размера на чанк: превышение роняет CI",
    "Сравнение с прошлой сборкой: какое изменение добавило сколько байт",
  ],
  frames: [
    [Box("a", 90, 80, 120, 80, "moment 290 КБ", "r", { size: 10 }), Box("b", 220, 60, 80, 40, "react 45 КБ", "b", { size: 9.5 }), Box("c", 220, 110, 80, 40, "lodash 70 КБ", "y", { size: 9 }), Box("d", 310, 80, 50, 80, "app", "g", { size: 10 })],
    [jc("c", 10, 30, ["main.js     180 КБ / 200 КБ  ✓", "vendor.js   410 КБ / 300 КБ  ✗", "→ CI красный"], [1, 2], { ...code, lh: 24, size: 9, bad: [1] })],
    [jc("c", 10, 30, ["main.js    +12 КБ (+7%)", "vendor.js   −3 КБ", "new: chart.js +85 КБ ⚠"], [0, 2], { ...code, lh: 24, size: 10 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Конвейер", "Решения", "Дальше"],
  caption: [
    "Граф → бандл → tree shaking → минификация → чанки → хеши",
    "webpack, Rollup, esbuild и Vite решают одну задачу по-разному; анализ и бюджеты",
    "Следующая тема — TypeScript, линтеры и форматирование",
  ],
  frames: [
    [...["граф", "бандл", "shake", "min", "чанки", "hash"].map((t, i) => Box(`s${i}`, 36 + i * 58, 80, 52, 34, t, "g", { size: 9 }))],
    [Box("a", 65, 60, 110, 28, "webpack", "b", { size: 10 }), Box("b", 180, 60, 110, 28, "Rollup", "b", { size: 10 }), Box("c", 295, 60, 110, 28, "esbuild", "b", { size: 10 }), Box("d", 180, 104, 110, 28, "Vite", "g", { size: 11 })],
    [jc("c", 20, 40, ["interface User {", "  id: number;", "  name: string;", "}"], [0], { ...code, lh: 20, size: 11 }), arrow("a", 180, 130, 180, 144, "g")],
  ],
});
