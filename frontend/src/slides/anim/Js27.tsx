import { scene } from "./alg.tsx";
import { Box, Tx, arrow, jc } from "./jv.tsx";

/* Глава 27 книги «Современный Frontend»: TypeScript, линтеры и форматирование. */

const code = { w: 340, size: 9.5, lh: 14 };

// 1. Зачем типы
export const V01 = scene({
  labels: ["Ошибка в проде", "Типы до запуска", "Стираются"],
  caption: [
    "Опечатка в поле или неверный аргумент находятся только при запуске — иногда в продакшене",
    "TypeScript описывает типы и проверяет их до выполнения; это надмножество JavaScript",
    "При сборке типы стираются: скорость выполнения — как у обычного кода",
  ],
  frames: [
    [jc("c", 10, 30, ["user.nmae.toUpperCase();", "// TypeError: Cannot read properties", "//        of undefined (во время работы)"], [0], { ...code, lh: 24, size: 10, bad: [0] })],
    [jc("c", 10, 30, ["user.nmae.toUpperCase();", "// ✗ Property 'nmae' does not exist", "//   on type 'User'. Did you mean 'name'?"], [1, 2], { ...code, lh: 24, size: 9.5 })],
    [Box("a", 90, 70, 150, 36, "code.ts\nс типами", "b", { size: 10 }), arrow("e", 168, 70, 192, 70, "g"), Box("b", 280, 70, 150, 36, "code.js\nбез типов", "g", { size: 10 })],
  ],
});

// 2. Основы типов
export const V02 = scene({
  labels: ["Примитивы и массивы", "Union и литералы", "Вывод типов"],
  caption: [
    "string, number, boolean, null, undefined; number[] — массив; поля объекта",
    "string | number — одно из двух; \"up\" | \"down\" — только эти значения",
    "Локальные переменные выводятся сами; аннотации — на границах (параметры, API)",
  ],
  frames: [
    [jc("c", 10, 20, ["const n: number = 42;", "const names: string[] = [\"a\"];", "const p: { x: number; y: number } = { x: 1, y: 2 };"], [0, 1, 2], { ...code, lh: 24, size: 9 })],
    [jc("c", 10, 20, ["let id: string | number;", "type Dir = \"up\" | \"down\";", "const d: Dir = \"left\";   // ✗"], [0, 1], { ...code, lh: 24, size: 9.5, bad: [2] })],
    [jc("c", 10, 20, ["const n = 42;         // number", "const s = \"x\";        // string", "function f(a: number) { return a * 2; }  // → number"], [0, 1, 2], { ...code, lh: 24, size: 9 })],
  ],
});

// 3. Интерфейсы
export const V03 = scene({
  labels: ["interface", "Структурная типизация", "Свежий литерал"],
  caption: [
    "Поле может быть необязательным (?) или только для чтения (readonly)",
    "Подходит любое значение с нужными полями — неважно, откуда оно",
    "Лишнее поле в литерале объекта — ошибка; в готовой переменной — допустимо",
  ],
  frames: [
    [jc("c", 10, 20, ["interface User {", "  readonly id: number;", "  name: string;", "  email?: string;", "}"], [1, 3], { ...code, lh: 19, size: 10 })],
    [Box("a", 90, 70, 150, 40, "{ id, name, age }\n(есть лишнее поле)", "g", { size: 9.5 }), arrow("e", 168, 70, 192, 70, "g"), Box("b", 280, 70, 150, 40, "User\n{ id, name }", "b", { size: 10 })],
    [jc("c", 10, 20, ["const u: User = { id: 1, name: \"A\", age: 3 }; // ✗", "const raw = { id: 1, name: \"A\", age: 3 };", "const v: User = raw;                          // ✓"], [2], { ...code, lh: 24, size: 8.5, bad: [0] })],
  ],
});

// 4. Дженерики
export const V04 = scene({
  labels: ["T связывает типы", "Вывод T", "extends"],
  caption: [
    "function first<T>(xs: T[]): T — тип результата зависит от типа массива",
    "first([1, 2]) → number; first([\"a\"]) → string: T выводится по аргументам",
    "T extends { length: number } — допустимы только типы с полем length",
  ],
  frames: [
    [jc("c", 10, 30, ["function first<T>(xs: T[]): T {", "  return xs[0];", "}"], [0], { ...code, lh: 22, size: 10 })],
    [jc("c", 10, 30, ["first([1, 2, 3]);   // number", "first([\"a\", \"b\"]);   // string", "first<boolean>([]);   // явно"], [0, 1], { ...code, lh: 24, size: 10 })],
    [jc("c", 10, 30, ["function len<T extends { length: number }>(x: T) {", "  return x.length;", "}", "len(\"abc\"); len([1]); len(5); // ✗"], [0], { ...code, lh: 20, size: 9, bad: [3] })],
  ],
});

// 5. Сужение типов
export const V05 = scene({
  labels: ["typeof", "Дискриминант", "never"],
  caption: [
    "После проверки typeof тип в ветке сужается до string",
    "Поле-метка kind определяет вариант целиком",
    "Все варианты разобраны — остаток never; новый вариант подсветит забытое место",
  ],
  frames: [
    [jc("c", 10, 20, ["function f(x: string | number) {", "  if (typeof x === \"string\") {", "    return x.toUpperCase();   // string", "  }", "  return x.toFixed(2);        // number", "}"], [1, 2, 4], { ...code, lh: 17, size: 9 })],
    [jc("c", 10, 20, ["type Shape =", "  | { kind: \"circle\"; r: number }", "  | { kind: \"rect\"; w: number; h: number };", "if (s.kind === \"circle\") s.r;   // ✓"], [1, 2, 3], { ...code, lh: 20, size: 9 })],
    [jc("c", 10, 20, ["switch (s.kind) {", "  case \"circle\": …", "  case \"rect\": …", "  default: const _: never = s;   // ✓ полно", "}"], [3], { ...code, lh: 20, size: 9.5 })],
  ],
});

// 6. Утилитные типы
export const V06 = scene({
  labels: ["Partial и Pick", "Omit и Record", "Из одного источника"],
  caption: [
    "Partial<User> — все поля необязательные; Pick<User, \"id\"> — выбранные",
    "Omit<User, \"email\"> — без поля; Record<string, number> — словарь",
    "ReturnType<typeof f> и Parameters<typeof f> выводятся из функции — не копируем описания",
  ],
  frames: [
    [jc("c", 10, 20, ["type A = Partial<User>;", "type B = Pick<User, \"id\" | \"name\">;"], [0, 1], { ...code, lh: 30, size: 10 })],
    [jc("c", 10, 20, ["type C = Omit<User, \"email\">;", "type D = Record<string, number>;"], [0, 1], { ...code, lh: 30, size: 10 })],
    [jc("c", 10, 20, ["function make() { return { id: 1, ok: true }; }", "type Made = ReturnType<typeof make>;"], [1], { ...code, lh: 30, size: 9.5 })],
  ],
});

// 7. tsconfig
export const V07 = scene({
  labels: ["strict", "target и module", "extends"],
  caption: [
    "strict включает набор: noImplicitAny, strictNullChecks, strictFunctionTypes…",
    "target — версия языка вывода; module/moduleResolution — правила подключения; noEmit — только проверка",
    "extends: общая база, а в проекте — только отличия",
  ],
  frames: [
    [jc("c", 10, 20, ["{ \"compilerOptions\": {", "    \"strict\": true", "} }"], [1], { ...code, lh: 26, size: 11 })],
    [jc("c", 10, 20, ["\"target\": \"ES2022\",", "\"module\": \"ESNext\",", "\"moduleResolution\": \"bundler\",", "\"noEmit\": true"], [0, 1, 2, 3], { ...code, lh: 20, size: 10 })],
    [jc("c", 10, 30, ["{ \"extends\": \"../../tsconfig.base.json\",", "  \"include\": [\"src\"] }"], [0], { ...code, lh: 26, size: 10 })],
  ],
});

// 8. tsc и сборка
export const V08 = scene({
  labels: ["Вырезать типы", "Проверка отдельно", "d.ts"],
  caption: [
    "esbuild и SWC убирают типы за миллисекунды, но не проверяют корректность",
    "tsc --noEmit — шаг в редакторе и CI",
    "index.d.ts описывает типы библиотеки; @types/… — от сообщества (DefinitelyTyped)",
  ],
  frames: [
    [Box("a", 70, 70, 100, 36, "app.ts", "b", { size: 11 }), arrow("e", 122, 70, 148, 70, "g"), Box("b", 220, 70, 100, 36, "esbuild", "g", { size: 11 }), arrow("f", 272, 70, 288, 70, "g"), Box("c", 335, 70, 40, 36, "js", "b", { size: 11 })],
    [jc("c", 10, 30, ["$ tsc --noEmit", "src/app.ts(5,3): error TS2322:", "  Type 'string' is not assignable to type 'number'."], [1, 2], { ...code, lh: 24, size: 9.5, bad: [1] })],
    [jc("c", 10, 30, ["// index.d.ts", "export declare function add(a: number, b: number): number;", "// npm i -D @types/lodash"], [1, 2], { ...code, lh: 24, size: 9 })],
  ],
});

// 9. Типы и рантайм
export const V09 = scene({
  labels: ["Типы не проверяют", "unknown + проверка", "Не as"],
  caption: [
    "Ответ сервера приходит во время работы; тип «в голове компилятора» его не проверит",
    "На границе принимаем unknown и проверяем type guard-ом или zod",
    "as и any отключают проверки — редкое исключение, а не способ заставить замолчать",
  ],
  frames: [
    [Box("a", 90, 70, 150, 36, "fetch → JSON\n(что внутри?)", "y", { size: 9.5 }), arrow("e", 168, 70, 192, 70, "g"), Box("b", 280, 70, 150, 36, "тип User\nтолько на бумаге", "r", { size: 9.5 })],
    [jc("c", 10, 20, ["const data: unknown = await res.json();", "const user = UserSchema.parse(data);   // zod", "user.name.toUpperCase();   // ✓ проверено"], [1], { ...code, lh: 24, size: 9 })],
    [jc("c", 10, 20, ["const user = data as User;   // обещание без проверки", "const x: any = data;          // отключили типы"], undefined, { ...code, lh: 30, size: 9.5, bad: [0, 1] })],
  ],
});

// 10. ESLint
export const V10 = scene({
  labels: ["Правило", "Уровни", "Автофикс"],
  caption: [
    "ESLint разбирает код в AST и проверяет его правилами: eqeqeq, no-unused-vars, require-await",
    "Каждое правило: off, warn или error; плагины добавляют правила для TS и React",
    "--fix исправляет безопасные замечания сам",
  ],
  frames: [
    [jc("c", 10, 20, ["if (x == 1) { … }", "// ✗ eqeqeq: Expected '===' and instead saw '=='", "const unused = 5;", "// ✗ no-unused-vars"], [1, 3], { ...code, lh: 24, size: 9.5, bad: [0, 2] })],
    [jc("c", 10, 20, ["rules: {", "  eqeqeq: \"error\",", "  \"no-console\": \"warn\",", "  \"no-var\": \"off\"", "}"], [1, 2, 3], { ...code, lh: 20, size: 10 })],
    [jc("c", 10, 30, ["$ eslint --fix src", "  var a = 1;   →   let a = 1;", "  x == 1       →   x === 1"], [1, 2], { ...code, lh: 24, size: 10 })],
  ],
});

// 11. Prettier
export const V11 = scene({
  labels: ["Один формат", "Не спорим", "EditorConfig"],
  caption: [
    "Prettier печатает код заново по одним правилам: ширина, кавычки, запятые",
    "eslint-config-prettier отключает стилевые правила ESLint, чтобы они не конфликтовали",
    "Отступы и переводы строк для всех редакторов — .editorconfig",
  ],
  frames: [
    [Box("a", 90, 70, 150, 40, "const a={b:1,\n c:[1,2]}", "y", { size: 9.5 }), arrow("e", 168, 70, 192, 70, "g"), Box("b", 280, 70, 150, 40, "const a = {\n  b: 1, c: [1, 2],\n};", "g", { size: 9 })],
    [Box("a", 90, 70, 130, 36, "ESLint:\nошибки", "b", { size: 10 }), Box("b", 270, 70, 130, 36, "Prettier:\nстиль", "g", { size: 10 }), Tx("n", 180, 70, "+", { size: 14 })],
    [jc("c", 10, 30, ["[*]", "indent_style = space", "indent_size = 2", "end_of_line = lf"], [1, 2, 3], { ...code, lh: 22, size: 10 })],
  ],
});

// 12. Автоматизация
export const V12 = scene({
  labels: ["pre-commit", "CI", "Редактор"],
  caption: [
    "husky + lint-staged: линтер и форматировщик только на изменённых файлах",
    "В CI всё целиком: tsc --noEmit, eslint, prettier --check, тесты",
    "Редактор подсказывает те же ошибки при наборе — до коммита их почти не остаётся",
  ],
  frames: [
    [Box("a", 70, 70, 100, 36, "git commit", "b", { size: 10 }), arrow("e1", 122, 70, 148, 70, "g"), Box("b", 220, 70, 100, 36, "lint-staged", "g", { size: 10 }), arrow("e2", 272, 70, 288, 70, "g"), Box("c", 335, 70, 40, 36, "✓", "g", { size: 14 })],
    [jc("c", 10, 20, ["- run: npx tsc --noEmit", "- run: npx eslint .", "- run: npx prettier --check .", "- run: npm test"], [0, 1, 2, 3], { ...code, lh: 22, size: 10 })],
    [Box("a", 90, 70, 150, 36, "красное подчёркивание\nпри наборе", "g", { size: 9.5 }), Box("b", 270, 70, 150, 36, "формат при\nсохранении", "g", { size: 9.5 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Типы", "Качество", "Дальше"],
  caption: [
    "Типы до запуска и стираются при сборке; структурная совместимость; дженерики; сужение",
    "ESLint — плохие практики; Prettier — стиль; автоматизация в pre-commit и CI",
    "Следующая тема — свой мини-фреймворк: начинаем с реактивности",
  ],
  frames: [
    [Box("a", 65, 60, 110, 28, "типы", "g", { size: 11 }), Box("b", 180, 60, 110, 28, "дженерики", "g", { size: 10 }), Box("c", 295, 60, 110, 28, "сужение", "g", { size: 10 })],
    [Box("a", 65, 60, 110, 28, "ESLint", "b", { size: 11 }), Box("b", 180, 60, 110, 28, "Prettier", "b", { size: 11 }), Box("c", 295, 60, 110, 28, "CI", "b", { size: 11 })],
    [jc("c", 20, 40, ["const count = signal(0);", "effect(() => log(count()));", "count.set(1);"], [0, 1, 2], { ...code, lh: 22, size: 11 })],
  ],
});
