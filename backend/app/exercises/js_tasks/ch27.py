"""Задачи книги «Современный Frontend»: глава 27."""

TASKS: dict[int, list[dict]] = {27: [{'id': 'j27-tokenize',
  'mode': 'js',
  'title': 'Лексер JavaScript',
  'statement': 'Напишите tokenize(src) → массив { type, value }. Пробелы и комментарии (// до '
               "конца строки, /* … */) пропускаются. Типы: 'ident' — [A-Za-z_$][A-Za-z0-9_$]*; "
               "'number' — десятичные (с дробной частью и экспонентой) и 0x…; 'string' — строка в "
               '\'…\', "…" или `…` целиком с кавычками (экранирование «\\\\» учитывается; value — '
               "исходный текст литерала); 'punct' — операторы: === !== == != <= >= => && || ?? ?. "
               '... ** ++ -- (самые длинные первыми), иначе один символ из '
               '«{}()[];,.:?<>=+-*/%!&|^~@#». Любой другой символ — Error(`Unexpected character '
               "'${c}' at ${позиция}`). Незакрытая строка — Error('Unterminated string').",
  'starter': 'function tokenize(src) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const show = (s) => { try { console.log(tokenize(s).map((t) => t.type[0] + ":" + '
            't.value).join(" ")); } catch (e) { console.log("!" + e.message); } };\n'
            'show("const x = 42;");\n'
            'show("a === b !== c ?? d?.e ... f ** 2 => g && h || i");\n'
            'show("let s = \'it\\\\\'s\'; // comment\\nlet t = \\"q\\"; /* block */ let u = `tpl '
            '${1}`;");\n'
            'show("0x1F + 1.5e3 + .5 + 7.");\n'
            'show("x++ + --y");\n'
            'show("a # b");\n'
            'show("\'open");\n'
            'show("");\n'
            'show("foo$bar _baz");\n',
  'hint': 'Цикл по позиции; на каждом шаге попробуйте комментарий, пробел, строку, число, '
          'идентификатор, оператор.',
  'expected': ['i:const i:x p:= n:42 p:;',
               'i:a p:=== i:b p:!== i:c p:?? i:d p:?. i:e p:... i:f p:** n:2 p:=> i:g p:&& i:h '
               'p:|| i:i',
               'i:let i:s p:= s:\'it\\\'s\' p:; i:let i:t p:= s:"q" p:; i:let i:u p:= s:`tpl ${1}` '
               'p:;',
               'n:0x1F p:+ n:1.5e3 p:+ n:.5 p:+ n:7.',
               'i:x p:++ p:+ p:-- i:y',
               'i:a p:# i:b',
               '!Unterminated string',
               '',
               'i:foo$bar i:_baz']},
 {'id': 'j27-strip-types',
  'mode': 'js',
  'title': 'Удаление типов (подмножество)',
  'statement': 'Напишите stripTypes(src): превращает TypeScript в JavaScript для следующего '
               'подмножества. 1) Строки, начинающиеся с «interface » или «type » (однострочные '
               'объявления), удаляются целиком. 2) Аннотации «: ТИП» после имени переменной или '
               'параметра (в «const x: number =», «let y: string;», «(a: number, b?: string)») '
               'удаляются; у необязательного параметра «?» тоже убирается. 3) Тип результата '
               'функции «): ТИП {» → «) {». 4) « as ТИП» удаляется. ТИП — слово из букв, цифр, '
               '«_», «.», с необязательным «<…>» (без вложенных <>), необязательными «[]» и '
               'объединениями через « | » (например «number | null», «Array<string>[]»). Остальной '
               'текст не меняется.',
  'starter': 'function stripTypes(src) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const src = [\n'
            '  "interface User { id: number; name: string }",\n'
            '  "type Id = string | number;",\n'
            '  "const x: number = 1;",\n'
            '  "let name: string | null;",\n'
            '  "const list: Array<string>[] = [];",\n'
            '  "function f(a: number, b?: string): boolean { return (a as number) > 0; }",\n'
            '  "const g = (u: User): void => { console.log(u.name as string); };",\n'
            '  "const ok = cond ? a : b;",\n'
            '  "const o = { k: 1 };",\n'
            '].join("\\n");\n'
            'console.log(stripTypes(src));\n',
  'hint': 'Регулярные выражения по порядку: удалить строки, затем аннотации, возвращаемые типы и '
          'as.',
  'expected': ['const x = 1;',
               'let name;',
               'const list = [];',
               'function f(a, b) { return (a) > 0; }',
               'const g = (u) => { console.log(u.name); };',
               'const ok = cond ? a : b;',
               'const o = { k: 1 };']},
 {'id': 'j27-type-of',
  'mode': 'js',
  'title': 'Тип значения в записи TypeScript',
  'statement': 'Напишите typeOf(v) → строка, как показал бы TypeScript для литерала: null → '
               "'null', undefined → 'undefined', 'string', 'number', 'boolean', 'bigint'; функция "
               "→ 'function'; Date → 'Date'. Массив: пустой — 'never[]'; иначе типы элементов "
               '(рекурсивно), уникальные, отсортированные по строке и соединённые « | »; если '
               "вариантов больше одного — в скобках: '(number | string)[]', иначе 'number[]'. "
               "Обычный объект: '{ ключ: тип; … }' с ключами по алфавиту; пустой — '{}'.",
  'starter': 'function typeOf(v) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'for (const v of [1, "a", true, null, undefined, 10n, () => 1, new Date(0), [], [1, '
            '2], [1, "a", 2], [[1], ["x"]], { b: 1, a: "s" }, {}, { n: { z: [true, false] } }, [{ '
            'a: 1 }, { a: 2 }], [null, 1]]) console.log(typeOf(v));\n',
  'hint': 'Рекурсивная функция с разбором по typeof и Array.isArray.',
  'expected': ['number',
               'string',
               'boolean',
               'null',
               'undefined',
               'bigint',
               'function',
               'Date',
               'never[]',
               'number[]',
               '(number | string)[]',
               '(number[] | string[])[]',
               '{ a: string; b: number }',
               '{}',
               '{ n: { z: boolean[] } }',
               '{ a: number }[]',
               '(null | number)[]']},
 {'id': 'j27-assignable',
  'mode': 'js',
  'title': 'Совместимость типов',
  'statement': 'Напишите isAssignable(from, to) для типов-строк: примитивы string, number, '
               'boolean, null, undefined; специальные any, unknown, never; литералы ("abc" в '
               'двойных кавычках, числа вроде 42, true, false); объединения «A | B» (без скобок); '
               'массивы «T[]». Правила: from === to — true; never присваивается чему угодно; всё '
               'присваивается any и unknown; any присваивается любому типу, кроме never; unknown — '
               'только в any/unknown; литерал присваивается своему базовому примитиву (строка → '
               'string, число → number, true/false → boolean) и самому себе; union в from — все '
               'члены должны подходить; union в to — подходит, если from присваивается хотя бы '
               'одному члену; массив присваивается массиву, если типы элементов совместимы; иначе '
               'false.',
  'starter': 'function isAssignable(from, to) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (a, b) => console.log(a, "→", b, isAssignable(a, b));\n'
            't("string", "string"); t("number", "string"); t(\'"a"\', "string"); t("string", '
            '\'"a"\'); t(\'"a"\', \'"a"\'); t(\'"a"\', \'"b"\'); t("42", "number"); t("true", '
            '"boolean"); t("boolean", "true");\n'
            't("never", "string"); t("string", "never"); t("any", "string"); t("string", "any"); '
            't("any", "never"); t("unknown", "string"); t("string", "unknown"); t("unknown", '
            '"any");\n'
            't("string | number", "string"); t("string", "string | number"); t(\'"a" | "b"\', '
            '"string"); t("string | null", "string | null | undefined"); t("number | string", '
            '"string | number");\n'
            't("string[]", "unknown[]"); t(\'"a"[]\', "string[]"); t("string[]", "number[]"); '
            't("(string)[]", "string[]"); t("null", "undefined"); t("undefined", "string | '
            'undefined");\n',
  'hint': 'Разберите объединения по « | » и действуйте от общего к частному: сначала from-union, '
          'затем to-union.',
  'expected': ['string → string true',
               'number → string false',
               '"a" → string true',
               'string → "a" false',
               '"a" → "a" true',
               '"a" → "b" false',
               '42 → number true',
               'true → boolean true',
               'boolean → true false',
               'never → string true',
               'string → never false',
               'any → string true',
               'string → any true',
               'any → never false',
               'unknown → string false',
               'string → unknown true',
               'unknown → any true',
               'string | number → string false',
               'string → string | number true',
               '"a" | "b" → string true',
               'string | null → string | null | undefined true',
               'number | string → string | number true',
               'string[] → unknown[] true',
               '"a"[] → string[] true',
               'string[] → number[] false',
               '(string)[] → string[] true',
               'null → undefined false',
               'undefined → string | undefined true']},
 {'id': 'j27-narrowing',
  'mode': 'js',
  'title': 'Различаемые объединения',
  'statement': 'Напишите narrowByKind(variants, kind) и missingCases(variants, handled). variants '
               '— массив описаний вариантов { kind, … } (объединение с полем-меткой). narrowByKind '
               'возвращает массив вариантов с указанным kind (в исходном порядке; пустой массив '
               'означает тип never). missingCases — отсортированный массив kind вариантов '
               '(уникальных), которых нет в массиве handled (проверка полноты разбора). Если '
               'handled содержит неизвестные kind — они игнорируются.',
  'starter': 'function narrowByKind(variants, kind) {\n'
             '}\n'
             'function missingCases(variants, handled) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const shapes = [{ kind: "circle", r: 1 }, { kind: "rect", w: 1, h: 2 }, { kind: '
            '"tri", a: 1 }, { kind: "rect", w: 3, h: 4 }];\n'
            'console.log(JSON.stringify(narrowByKind(shapes, "rect")));\n'
            'console.log(JSON.stringify(narrowByKind(shapes, "circle")), '
            'JSON.stringify(narrowByKind(shapes, "poly")));\n'
            'console.log(JSON.stringify(missingCases(shapes, ["circle"])));\n'
            'console.log(JSON.stringify(missingCases(shapes, ["circle", "rect", "tri", '
            '"other"])));\n'
            'console.log(JSON.stringify(missingCases(shapes, [])), JSON.stringify(missingCases([], '
            '["x"])));\n',
  'hint': 'filter по kind; Set для уникальных меток.',
  'expected': ['[{"kind":"rect","w":1,"h":2},{"kind":"rect","w":3,"h":4}]',
               '[{"kind":"circle","r":1}] []',
               '["rect","tri"]',
               '[]',
               '["circle","rect","tri"] []']},
 {'id': 'j27-infer-decl',
  'mode': 'js',
  'title': 'Вывод типа объявления',
  'statement': 'Напишите inferDecl(keyword, value, asConst = false) → строка типа. keyword — '
               '\'const\' или \'let\'. Примитивы: у const — литеральный тип (строка → «"abc"», '
               'число → «42», boolean → «true»), у let — расширенный (string, number, boolean). '
               'Массив: тип элементов расширяется всегда (как в typeOf: уникальные, по алфавиту, '
               "через « | »; несколько вариантов — в скобках; пустой — never[]): 'string[]', "
               "'(number | string)[]'. Объект: «{ k: тип; … }», ключи по алфавиту, значения "
               'расширены. При asConst === true (как «as const»): всё остаётся литеральным и '
               'неизменяемым: примитив → литерал; массив → «readonly [литерал, …]» (в порядке '
               'элементов); объект → «{ readonly k: литерал; … }» (ключи по алфавиту), рекурсивно.',
  'starter': 'function inferDecl(keyword, value, asConst = false) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (k, v, c) => console.log(k, JSON.stringify(v), c ?? false, inferDecl(k, v, '
            'c));\n'
            't("const", "abc"); t("let", "abc"); t("const", 42); t("let", 42); t("const", true); '
            't("let", false);\n'
            't("const", [1, 2]); t("let", [1, "a"]); t("const", []); t("const", { b: 1, a: "x" '
            '});\n'
            't("const", "up", true); t("const", [1, "a"], true); t("const", { b: [1, 2], a: "x" }, '
            'true); t("let", { k: "v" }, true);\n',
  'hint': 'Две функции: widen(value) и literal(value, constMode); asConst рекурсивно использует '
          'literal.',
  'expected': ['const "abc" false "abc"',
               'let "abc" false string',
               'const 42 false 42',
               'let 42 false number',
               'const true false true',
               'let false false boolean',
               'const [1,2] false number[]',
               'let [1,"a"] false (number | string)[]',
               'const [] false never[]',
               'const {"b":1,"a":"x"} false { a: string; b: number }',
               'const "up" true "up"',
               'const [1,"a"] true readonly [1, "a"]',
               'const {"b":[1,2],"a":"x"} true { readonly a: "x"; readonly b: readonly [1, 2] }',
               'let {"k":"v"} true { readonly k: "v" }']},
 {'id': 'j27-utility-types',
  'mode': 'js',
  'title': 'Утилитные типы над схемой',
  'statement': 'Схема объекта — { ключ: { type, optional?, readonly? } }. Напишите partial(s) (у '
               'всех optional: true), required(s) (optional убирается — ключ не должен '
               'присутствовать), pick(s, keys) (только указанные существующие ключи), omit(s, '
               'keys) (все, кроме указанных), record(keys, type) (каждый ключ → { type }) и '
               'keyOf(s) → строка «"a" | "b"» с ключами по алфавиту (пустая схема — \'never\'). '
               'Функции не изменяют входные объекты, ключи результата сохраняют порядок исходной '
               'схемы (для record — порядок keys; keyOf — алфавитный).',
  'starter': 'function partial(s) {\n'
             '}\n'
             'function required(s) {\n'
             '}\n'
             'function pick(s, keys) {\n'
             '}\n'
             'function omit(s, keys) {\n'
             '}\n'
             'function record(keys, type) {\n'
             '}\n'
             'function keyOf(s) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const User = { id: { type: "number", readonly: true }, name: { type: "string" }, '
            'email: { type: "string", optional: true } };\n'
            'const show = (x) => console.log(JSON.stringify(x));\n'
            'show(partial(User)); show(required(User)); show(pick(User, ["name", "id", "zzz"])); '
            'show(omit(User, ["email", "nope"]));\n'
            'show(record(["a", "b"], "number")); console.log(keyOf(User), keyOf({}));\n'
            'console.log(User.name.optional, User.email.optional);\n',
  'hint': 'Object.entries + fromEntries; spread для копирования полей.',
  'expected': ['{"id":{"type":"number","readonly":true,"optional":true},"name":{"type":"string","optional":true},"email":{"type":"string","optional":true}}',
               '{"id":{"type":"number","readonly":true},"name":{"type":"string"},"email":{"type":"string"}}',
               '{"id":{"type":"number","readonly":true},"name":{"type":"string"}}',
               '{"id":{"type":"number","readonly":true},"name":{"type":"string"}}',
               '{"a":{"type":"number"},"b":{"type":"number"}}',
               '"email" | "id" | "name" never',
               'undefined true']},
 {'id': 'j27-intersect',
  'mode': 'js',
  'title': 'Пересечение типов',
  'statement': 'Напишите intersect(a, b): схемы — { ключ: { type, optional? } }. Результат — схема '
               'с объединением ключей (порядок: сначала ключи a, затем новые ключи b). Для общего '
               "ключа: типы равны — тип сохраняется, иначе type: 'never'; optional: true только "
               'если поле необязательно в обеих схемах (иначе поля optional нет). Для ключа только '
               'в одной схеме поле копируется как есть.',
  'starter': 'function intersect(a, b) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const A = { id: { type: "number" }, name: { type: "string", optional: true }, tag: { '
            'type: "string", optional: true } };\n'
            'const B = { id: { type: "number" }, name: { type: "string" }, tag: { type: "number", '
            'optional: true }, extra: { type: "boolean", optional: true } };\n'
            'console.log(JSON.stringify(intersect(A, B)));\n'
            'console.log(JSON.stringify(intersect({}, B)));\n'
            'console.log(JSON.stringify(intersect(A, {})));\n',
  'hint': 'Сначала пройдите ключи a и объедините с b, затем добавьте оставшиеся ключи b.',
  'expected': ['{"id":{"type":"number"},"name":{"type":"string"},"tag":{"type":"never","optional":true},"extra":{"type":"boolean","optional":true}}',
               '{"id":{"type":"number"},"name":{"type":"string"},"tag":{"type":"number","optional":true},"extra":{"type":"boolean","optional":true}}',
               '{"id":{"type":"number"},"name":{"type":"string","optional":true},"tag":{"type":"string","optional":true}}']},
 {'id': 'j27-check-object',
  'mode': 'js',
  'title': 'Структурная проверка объекта',
  'statement': 'Напишите checkObject(value, schema, fresh = false): schema — { ключ: { type, '
               "optional? } } (type — 'string', 'number', 'boolean'). Верните массив ошибок, "
               'отсортированный по ключу, затем в порядке «отсутствие, тип, лишнее»: для '
               "обязательного отсутствующего (undefined) поля — «Property 'k' is missing»; для "
               "присутствующего с неверным типом — «Type 'ФАКТ' is not assignable to type "
               "'ОЖИДАЕМЫЙ' (property 'k')»; если fresh === true (свежий литерал), то для каждого "
               'ключа value, которого нет в схеме, — «Object literal may only specify known '
               "properties, and 'k' does not exist». Необязательное поле допускает отсутствие и "
               "undefined. ФАКТ — typeof значения (null → 'null').",
  'starter': 'function checkObject(value, schema, fresh = false) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const schema = { id: { type: "number" }, name: { type: "string" }, email: { type: '
            '"string", optional: true } };\n'
            'const t = (v, f) => console.log(JSON.stringify(checkObject(v, schema, f)));\n'
            't({ id: 1, name: "a" }); t({ id: 1, name: "a", email: "e" }); t({ id: "1", name: 5 '
            '}); t({}); t({ id: 1, name: "a", email: 5 });\n'
            't({ id: 1, name: "a", age: 3 }); t({ id: 1, name: "a", age: 3 }, true); t({ id: 1, '
            'zz: 1, aa: 2 }, true); t({ id: null, name: "a", email: undefined });\n',
  'hint': 'Объедините ключи схемы и value, отсортируйте; для каждого ключа вычислите ошибки.',
  'expected': ['[]',
               '[]',
               '["Type \'string\' is not assignable to type \'number\' (property \'id\')","Type '
               '\'number\' is not assignable to type \'string\' (property \'name\')"]',
               '["Property \'id\' is missing","Property \'name\' is missing"]',
               '["Type \'number\' is not assignable to type \'string\' (property \'email\')"]',
               '[]',
               '["Object literal may only specify known properties, and \'age\' does not exist"]',
               '["Object literal may only specify known properties, and \'aa\' does not '
               'exist","Property \'name\' is missing","Object literal may only specify known '
               'properties, and \'zz\' does not exist"]',
               '["Type \'null\' is not assignable to type \'number\' (property \'id\')"]']},
 {'id': 'j27-unify',
  'mode': 'js',
  'title': 'Вывод параметров дженерика',
  'statement': 'Напишите unify(pattern, type): сопоставляет образец с конкретным типом и '
               'возвращает связи параметров типа или null. Синтаксис (только эти формы): имя '
               'типа-параметра — одна заглавная буква (T, K, V…) или любой конкретный '
               'тип-идентификатор (number, string, User); массив «X[]»; обобщённый «Имя<X, Y, …>» '
               '(аргументы через запятую, вложенность допустима, например «Map<K, Array<V>>»); '
               'объект «{ поле: X; … }» (поля в одном порядке). Однобуквенная заглавная — '
               'переменная: связывается с соответствующей частью. Одна переменная должна получить '
               'одинаковые значения во всех местах, иначе null. Несовпадение структуры — null. '
               "Результат — объект { T: 'number', … }.",
  'starter': 'function unify(pattern, type) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (p, x) => console.log(p, "~", x, JSON.stringify(unify(p, x)));\n'
            't("T", "number"); t("T[]", "string[]"); t("T[]", "string"); t("Array<T>", '
            '"Array<number>"); t("Promise<T>", "Promise<User>");\n'
            't("Map<K, V>", "Map<string, number>"); t("Map<K, Array<V>>", "Map<string, '
            'Array<number>>"); t("Map<K, V>", "Set<string>");\n'
            't("{ id: T }", "{ id: number }"); t("{ a: T; b: T }", "{ a: string; b: string }"); '
            't("{ a: T; b: T }", "{ a: string; b: number }");\n'
            't("number", "number"); t("number", "string"); t("T[][]", "number[][]"); t("Pair<T, '
            'T>", "Pair<a, b>"); t("T[]", "Array<number>");\n',
  'hint': 'Разберите обе строки в деревья (рекурсивный парсер) и сопоставьте рекурсивно.',
  'expected': ['T ~ number {"T":"number"}',
               'T[] ~ string[] {"T":"string"}',
               'T[] ~ string null',
               'Array<T> ~ Array<number> {"T":"number"}',
               'Promise<T> ~ Promise<User> {"T":"User"}',
               'Map<K, V> ~ Map<string, number> {"K":"string","V":"number"}',
               'Map<K, Array<V>> ~ Map<string, Array<number>> {"K":"string","V":"number"}',
               'Map<K, V> ~ Set<string> null',
               '{ id: T } ~ { id: number } {"T":"number"}',
               '{ a: T; b: T } ~ { a: string; b: string } {"T":"string"}',
               '{ a: T; b: T } ~ { a: string; b: number } null',
               'number ~ number {}',
               'number ~ string null',
               'T[][] ~ number[][] {"T":"number"}',
               'Pair<T, T> ~ Pair<a, b> null',
               'T[] ~ Array<number> null']},
 {'id': 'j27-tsconfig-extends',
  'mode': 'js',
  'title': 'Наследование tsconfig',
  'statement': 'Напишите resolveTsconfig(name, configs): configs — { имя: { extends?, '
               'compilerOptions?, include?, exclude?, … } }, extends — имя или массив имён '
               '(применяются по порядку, поздние перекрывают ранние), затем сам конфиг. Слияние: '
               'compilerOptions объединяются по ключам (дочерний перекрывает), остальные поля '
               '(include, exclude, files и др.) заменяются целиком, если заданы. В результате нет '
               "поля extends. Нет конфига — Error('Cannot find config ИМЯ'); цикл — "
               "Error('Circular extends: a -> b -> a') (цепочка имён от начала до повтора).",
  'starter': 'function resolveTsconfig(name, configs) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const configs = {\n'
            '  base: { compilerOptions: { strict: true, target: "ES2020", module: "ESNext" }, '
            'include: ["src"], exclude: ["dist"] },\n'
            '  web: { extends: "base", compilerOptions: { lib: ["dom"], target: "ES2022" } },\n'
            '  node: { extends: "base", compilerOptions: { module: "NodeNext" }, include: '
            '["server"] },\n'
            '  both: { extends: ["web", "node"], compilerOptions: { noEmit: true } },\n'
            '  a: { extends: "b" }, b: { extends: "c" }, c: { extends: "a" },\n'
            '  ghost: { extends: "missing" },\n'
            '};\n'
            'const t = (n) => { try { console.log(n, JSON.stringify(resolveTsconfig(n, configs))); '
            '} catch (e) { console.log(n, "!" + e.message); } };\n'
            't("base"); t("web"); t("node"); t("both"); t("a"); t("ghost"); t("nothing");\n',
  'hint': 'Рекурсия со стеком посещённых имён; merge(parent, child).',
  'expected': ['base '
               '{"compilerOptions":{"strict":true,"target":"ES2020","module":"ESNext"},"include":["src"],"exclude":["dist"]}',
               'web '
               '{"compilerOptions":{"strict":true,"target":"ES2022","module":"ESNext","lib":["dom"]},"include":["src"],"exclude":["dist"]}',
               'node '
               '{"compilerOptions":{"strict":true,"target":"ES2020","module":"NodeNext"},"include":["server"],"exclude":["dist"]}',
               'both '
               '{"compilerOptions":{"strict":true,"target":"ES2020","module":"NodeNext","lib":["dom"],"noEmit":true},"include":["server"],"exclude":["dist"]}',
               'a !Circular extends: a -> b -> c -> a',
               'ghost !Cannot find config missing',
               'nothing !Cannot find config nothing']},
 {'id': 'j27-strict-flags',
  'mode': 'js',
  'title': 'Что включает strict',
  'statement': 'Напишите enabledStrictFlags(options): options — compilerOptions. Флаги семейства '
               'strict: alwaysStrict, noImplicitAny, noImplicitThis, strictBindCallApply, '
               'strictFunctionTypes, strictNullChecks, strictPropertyInitialization, '
               'useUnknownInCatchVariables. Если strict === true, все они включены, кроме явно '
               'заданных как false; если strict не true — включены только явно заданные true. '
               'Верните отсортированный массив включённых флагов. Дополнительно: '
               'strictPropertyInitialization работает только при включённом strictNullChecks — '
               'если он выключен, исключите strictPropertyInitialization из результата.',
  'starter': 'function enabledStrictFlags(options) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (o) => console.log(JSON.stringify(o), enabledStrictFlags(o).join(","));\n'
            't({ strict: true }); t({}); t({ strict: true, noImplicitAny: false }); t({ strict: '
            'false, noImplicitAny: true, strictNullChecks: true });\n'
            't({ strict: true, strictNullChecks: false }); t({ strictPropertyInitialization: true '
            '}); t({ strictNullChecks: true, strictPropertyInitialization: true });\n'
            't({ strict: true, noEmit: true, target: "ES2022" });\n',
  'hint': 'Список флагов; для каждого вычислите effective = options[f] ?? options.strict === true.',
  'expected': ['{"strict":true} '
               'alwaysStrict,noImplicitAny,noImplicitThis,strictBindCallApply,strictFunctionTypes,strictNullChecks,strictPropertyInitialization,useUnknownInCatchVariables',
               '{}',
               '{"strict":true,"noImplicitAny":false} '
               'alwaysStrict,noImplicitThis,strictBindCallApply,strictFunctionTypes,strictNullChecks,strictPropertyInitialization,useUnknownInCatchVariables',
               '{"strict":false,"noImplicitAny":true,"strictNullChecks":true} '
               'noImplicitAny,strictNullChecks',
               '{"strict":true,"strictNullChecks":false} '
               'alwaysStrict,noImplicitAny,noImplicitThis,strictBindCallApply,strictFunctionTypes,useUnknownInCatchVariables',
               '{"strictPropertyInitialization":true}',
               '{"strictNullChecks":true,"strictPropertyInitialization":true} '
               'strictNullChecks,strictPropertyInitialization',
               '{"strict":true,"noEmit":true,"target":"ES2022"} '
               'alwaysStrict,noImplicitAny,noImplicitThis,strictBindCallApply,strictFunctionTypes,strictNullChecks,strictPropertyInitialization,useUnknownInCatchVariables']},
 {'id': 'j27-gen-dts',
  'mode': 'js',
  'title': 'Генерация .d.ts',
  'statement': "Напишите genDts(items): items — описания { kind: 'function' | 'const' | "
               "'interface' | 'type', … }. Каждый элемент даёт блок текста, блоки разделяются "
               'пустой строкой. function { name, params: [{ name, type, optional? }], returns, '
               'generics? } → «export declare function имя<ГЕНЕРИКИ>(a: T, b?: U): R;» (generics — '
               'массив строк, соединяются «, », угловые скобки только если непусто); const { name, '
               'type } → «export declare const имя: тип;»; type { name, type } → «export type Имя '
               '= тип;»; interface { name, fields: [{ name, type, optional?, readonly? }] } → '
               '«export interface Имя {» + по строке на поле с отступом 2 пробела «  readonly '
               'имя?: тип;» (readonly — если задан, «?» — если optional) + «}». Пустой список — '
               'пустая строка.',
  'starter': 'function genDts(items) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const out = genDts([\n'
            '  { kind: "function", name: "add", params: [{ name: "a", type: "number" }, { name: '
            '"b", type: "number", optional: true }], returns: "number" },\n'
            '  { kind: "function", name: "first", generics: ["T"], params: [{ name: "xs", type: '
            '"T[]" }], returns: "T | undefined" },\n'
            '  { kind: "const", name: "VERSION", type: "string" },\n'
            '  { kind: "type", name: "Id", type: "string | number" },\n'
            '  { kind: "interface", name: "User", fields: [{ name: "id", type: "number", readonly: '
            'true }, { name: "email", type: "string", optional: true }, { name: "name", type: '
            '"string" }] },\n'
            '  { kind: "interface", name: "Empty", fields: [] },\n'
            ']);\n'
            'console.log(out);\n'
            'console.log(JSON.stringify(genDts([])));\n',
  'hint': "map по видам, join('\\n\\n').",
  'expected': ['export declare function add(a: number, b?: number): number;',
               '',
               'export declare function first<T>(xs: T[]): T | undefined;',
               '',
               'export declare const VERSION: string;',
               '',
               'export type Id = string | number;',
               '',
               'export interface User {',
               '  readonly id: number;',
               '  email?: string;',
               '  name: string;',
               '}',
               '',
               'export interface Empty {',
               '}',
               '""']},
 {'id': 'j27-types-version',
  'mode': 'js',
  'title': 'Выбор версии @types',
  'statement': 'Напишите pickTypesVersion(libVersion, typesVersions): libVersion — версия '
               'библиотеки «M.m.p», typesVersions — массив версий пакета @types/…. По правилам '
               'DefinitelyTyped версия типов M.m.* соответствует библиотеке M.m. Верните '
               'наибольшую версию из typesVersions с тем же M.m; если такой нет — наибольшую '
               'версию из тех, что ниже M.m (по major, затем minor); если и таких нет — null. '
               'Версии сравниваются по числам, не по строкам. Некорректные строки игнорируются.',
  'starter': 'function pickTypesVersion(libVersion, typesVersions) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const tv = ["18.0.0", "18.2.5", "18.2.10", "18.3.1", "17.0.80", "16.9.0", "bad", '
            '"19.0.0"];\n'
            'const t = (v) => console.log(v, pickTypesVersion(v, tv));\n'
            't("18.2.0"); t("18.3.9"); t("18.1.0"); t("17.5.0"); t("15.0.0"); t("19.0.4"); '
            't("20.0.0"); t("16.9.99");\n'
            'console.log(pickTypesVersion("1.0.0", []));\n',
  'hint': 'Разберите версии в тройки чисел; отфильтруйте по (major, minor) и выберите максимум.',
  'expected': ['18.2.0 18.2.10',
               '18.3.9 18.3.1',
               '18.1.0 18.0.0',
               '17.5.0 17.0.80',
               '15.0.0 null',
               '19.0.4 19.0.0',
               '20.0.0 19.0.0',
               '16.9.99 16.9.0',
               'null']},
 {'id': 'j27-validate',
  'mode': 'js',
  'title': 'Валидатор данных (как zod)',
  'statement': "Напишите validate(schema, data, path = 'value') → массив строк-ошибок (пустой — "
               "данные верны). Схема: строки 'string', 'number', 'boolean'; { array: схема }; { "
               'object: { ключ: схема } } (лишние ключи допустимы); { optional: схема } (undefined '
               'допустим); { oneOf: [значения] }. Сообщения: «ПУТЬ: expected number, got string» '
               "(got — typeof, для null 'null', для массива 'array'); для oneOf — «ПУТЬ: expected "
               'one of [a, b], got x» (значения через «, » без кавычек); для отсутствующего '
               'обязательного поля объекта путь «ПУТЬ.ключ» и «got undefined». Путь элементов '
               'массива — «ПУТЬ[0]», полей — «ПУТЬ.ключ». Ошибки идут в порядке обхода (ключи — в '
               'порядке схемы).',
  'starter': 'function validate(schema, data, path = "value") {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const schema = { object: { name: "string", age: { optional: "number" }, tags: { '
            'array: "string" }, role: { oneOf: ["admin", "user"] }, address: { object: { city: '
            '"string" } } } };\n'
            'const t = (d) => console.log(JSON.stringify(validate(schema, d, "user")));\n'
            't({ name: "A", tags: ["x"], role: "admin", address: { city: "M" } });\n'
            't({ name: 5, age: "x", tags: ["a", 2, null], role: "root", address: {} });\n'
            't({});\n'
            't(null);\n'
            't({ name: "A", tags: "no", role: "user", address: 5, extra: true });\n'
            'console.log(JSON.stringify(validate("number", 5)), JSON.stringify(validate("boolean", '
            '[])), JSON.stringify(validate({ array: "number" }, [1, "2"])));\n',
  'hint': 'Рекурсия по схеме; функция kind(data) для имён типов.',
  'expected': ['[]',
               '["user.name: expected string, got number","user.age: expected number, got '
               'string","user.tags[1]: expected string, got number","user.tags[2]: expected '
               'string, got null","user.role: expected one of [admin, user], got '
               'root","user.address.city: expected string, got undefined"]',
               '["user.name: expected string, got undefined","user.tags: expected array, got '
               'undefined","user.role: expected one of [admin, user], got '
               'undefined","user.address: expected object, got undefined"]',
               '["user: expected object, got null"]',
               '["user.tags: expected array, got string","user.address: expected object, got '
               'number"]',
               '[] ["value: expected boolean, got array"] ["value[1]: expected number, got '
               'string"]']},
 {'id': 'j27-guard',
  'mode': 'js',
  'title': 'Type guard по описанию',
  'statement': "Напишите createGuard(shape): shape — { ключ: 'string' | 'number' | 'boolean' | "
               "'string?' | 'number?' | 'boolean?' } (суффикс «?» — необязательное поле, "
               'допускающее undefined). Верните функцию-предикат (x) → boolean: true, если x — '
               'обычный объект (не null, не массив), у которого каждое поле из shape имеет нужный '
               'тип (typeof; NaN для number считается ошибкой). Лишние поля допустимы.',
  'starter': 'function createGuard(shape) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const isUser = createGuard({ id: "number", name: "string", admin: "boolean?" });\n'
            'for (const x of [{ id: 1, name: "a" }, { id: 1, name: "a", admin: true }, { id: 1, '
            'name: "a", admin: "yes" }, { id: "1", name: "a" }, { id: NaN, name: "a" }, { name: '
            '"a" }, null, [], "str", { id: 1, name: "a", extra: 1 }, { id: 1, name: "a", admin: '
            'undefined }])\n'
            '  console.log(JSON.stringify(x), isUser(x));\n'
            'console.log(createGuard({})({}), createGuard({})(null));\n',
  'hint': 'Проверка typeof и обработка суффикса «?».',
  'expected': ['{"id":1,"name":"a"} true',
               '{"id":1,"name":"a","admin":true} true',
               '{"id":1,"name":"a","admin":"yes"} false',
               '{"id":"1","name":"a"} false',
               '{"id":null,"name":"a"} false',
               '{"name":"a"} false',
               'null false',
               '[] false',
               '"str" false',
               '{"id":1,"name":"a","extra":1} true',
               '{"id":1,"name":"a"} true',
               'true false']},
 {'id': 'j27-unused-vars',
  'mode': 'js',
  'title': 'Неиспользуемые переменные',
  'statement': 'Напишите findUnused(src): имена, объявленные через const, let или var (по одному в '
               'объявлении: «const a = 1», «let b;», «var c = 2, d» — учитывайте только первое имя '
               'до «=»/«;»/«,») и функции function имя(, которые встречаются в коде как целое '
               'слово ровно один раз (только своё объявление). Строки в кавычках и комментарии (// '
               'и /* */) при подсчёте не учитываются. Результат — отсортированный массив '
               'уникальных имён.',
  'starter': 'function findUnused(src) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const src = `\n'
            'const used = 1;\n'
            'const unused = 2; // unused\n'
            'let counter = 0;\n'
            'counter++;\n'
            'var legacy;\n'
            'function helper() { return used; }\n'
            'function dead(a) { return 1; }\n'
            'const text = "dead helper unused";\n'
            '/* const ghost = 3; */\n'
            'let x = 5, y = 6;\n'
            'console.log(x);\n'
            '`;\n'
            'console.log(JSON.stringify(findUnused(src)));\n'
            'console.log(JSON.stringify(findUnused("const a = 1; console.log(a);")));\n'
            'console.log(JSON.stringify(findUnused("")));\n',
  'hint': 'Сначала вырежьте комментарии и строки, затем найдите объявления и посчитайте вхождения '
          '\\bимя\\b.',
  'expected': ['["dead","helper","legacy","text","unused"]', '[]', '[]']},
 {'id': 'j27-lint',
  'mode': 'js',
  'title': 'Мини-линтер',
  'statement': "Напишите lint(src, rules): rules — { правило: уровень }, уровень 'off' | 'warn' | "
               "'error' (для max-len — { level, max }, например { level: 'warn', max: 40 }). "
               "Строки нумеруются с 1. Правила: 'no-var' — строка содержит слово var (вне строк и "
               'комментариев не различать: ищите \\bvar\\b) → «Unexpected var, use let or const»; '
               "'eqeqeq' — есть == или != (но не === и !==) → «Expected '===' and instead saw "
               "'=='» (для != — «Expected '!==' and instead saw '!='»); 'no-console' — есть "
               "console. → «Unexpected console statement»; 'no-trailing-spaces' — строка "
               "оканчивается пробелом/табуляцией → «Trailing spaces not allowed»; 'max-len' — "
               'длина строки больше max → «This line has a length of N. Maximum allowed is M». '
               'Результат — массив { line, rule, severity, message }, отсортированный по строке, '
               "затем по порядку правил в списке выше; правила 'off' и отсутствующие пропускаются.",
  'starter': 'function lint(src, rules) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const src = ["var a = 1;  ", "if (a == 2) console.log(a != 3);", "const ok = a === 1 '
            '&& a !== 2;", "const veryLongVariableNameThatIsLonger = 1234567890;", "// var is fine '
            'in comments? no rule"].join("\\n");\n'
            'const show = (r) => console.log(JSON.stringify(lint(src, r)));\n'
            'show({ "no-var": "error", eqeqeq: "warn", "no-console": "warn", "no-trailing-spaces": '
            '"error", "max-len": { level: "warn", max: 40 } });\n'
            'show({ eqeqeq: "off", "no-var": "off" });\n'
            'show({ "max-len": { level: "error", max: 10 } });\n'
            'show({});\n',
  'hint': 'Функции-проверки для каждой строки; порядок правил — фиксированный массив.',
  'expected': ['[{"line":1,"rule":"no-var","severity":"error","message":"Unexpected var, use let '
               'or '
               'const"},{"line":1,"rule":"no-trailing-spaces","severity":"error","message":"Trailing '
               'spaces not '
               'allowed"},{"line":2,"rule":"eqeqeq","severity":"warn","message":"Expected \'===\' '
               'and instead saw '
               '\'==\'"},{"line":2,"rule":"eqeqeq","severity":"warn","message":"Expected \'!==\' '
               'and instead saw '
               '\'!=\'"},{"line":2,"rule":"no-console","severity":"warn","message":"Unexpected '
               'console statement"},{"line":4,"rule":"max-len","severity":"warn","message":"This '
               'line has a length of 52. Maximum allowed is '
               '40"},{"line":5,"rule":"no-var","severity":"error","message":"Unexpected var, use '
               'let or const"}]',
               '[]',
               '[{"line":1,"rule":"max-len","severity":"error","message":"This line has a length '
               'of 12. Maximum allowed is '
               '10"},{"line":2,"rule":"max-len","severity":"error","message":"This line has a '
               'length of 32. Maximum allowed is '
               '10"},{"line":3,"rule":"max-len","severity":"error","message":"This line has a '
               'length of 30. Maximum allowed is '
               '10"},{"line":4,"rule":"max-len","severity":"error","message":"This line has a '
               'length of 52. Maximum allowed is '
               '10"},{"line":5,"rule":"max-len","severity":"error","message":"This line has a '
               'length of 35. Maximum allowed is 10"}]',
               '[]']},
 {'id': 'j27-rule-config',
  'mode': 'js',
  'title': 'Нормализация настроек правил',
  'statement': 'Напишите normalizeRules(config): config — { правило: настройка }. Настройка — '
               "уровень ('off' | 'warn' | 'error' | 0 | 1 | 2) или массив [уровень, ...опции]. "
               "Результат — { правило: { level, options } }, level — всегда строка 'off' | 'warn' "
               "| 'error' (0 → off, 1 → warn, 2 → error), options — массив (пустой, если опций "
               "нет). Неизвестный уровень — Error(`Invalid level for rule 'ПРАВИЛО'`). Ключи "
               'сохраняют порядок.',
  'starter': 'function normalizeRules(config) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (c) => { try { console.log(JSON.stringify(normalizeRules(c))); } catch (e) '
            '{ console.log("!" + e.message); } };\n'
            't({ eqeqeq: "error", "no-console": 1, "no-var": 0, semi: ["error", "always"], '
            '"max-len": [2, { code: 100 }, "extra"], quotes: ["warn"] });\n'
            't({});\n'
            't({ a: "fatal" }); t({ a: 3 }); t({ a: [] }); t({ a: ["bad", 1] });\n',
  'hint': 'Таблица уровней; для массива — первый элемент уровень, остальные опции.',
  'expected': ['{"eqeqeq":{"level":"error","options":[]},"no-console":{"level":"warn","options":[]},"no-var":{"level":"off","options":[]},"semi":{"level":"error","options":["always"]},"max-len":{"level":"error","options":[{"code":100},"extra"]},"quotes":{"level":"warn","options":[]}}',
               '{}',
               "!Invalid level for rule 'a'",
               "!Invalid level for rule 'a'",
               "!Invalid level for rule 'a'",
               "!Invalid level for rule 'a'"]},
 {'id': 'j27-flat-config',
  'mode': 'js',
  'title': 'Плоская конфигурация ESLint',
  'statement': 'Напишите rulesFor(file, configs): configs — массив объектов { files?, ignores?, '
               'rules? } (плоская конфигурация, применяются по порядку). Объект только с ignores '
               '(без files и rules) — глобальное игнорирование: если файл подходит под любую из '
               'масок, результат null. Остальные объекты применяются к файлу, если нет files (все '
               'файлы) или файл подходит под любую маску из files, и не подходит под ignores '
               'объекта; их rules сливаются по ключам, поздние перекрывают ранние. Верните объект '
               'правил. Маски — как globToRegExp (уже есть в заготовке); маска без «/» '
               'сравнивается с именем файла в любом каталоге, с «/» — с полным путём.',
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
             'function rulesFor(file, configs) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const configs = [\n'
            '  { ignores: ["dist/**", "*.min.js"] },\n'
            '  { rules: { semi: "error", "no-var": "error" } },\n'
            '  { files: ["src/**/*.ts"], rules: { "no-var": "off", "@ts/no-any": "warn" } },\n'
            '  { files: ["*.test.ts"], rules: { "no-console": "off" } },\n'
            '  { files: ["src/**/*.ts"], ignores: ["src/legacy/**"], rules: { strict: "error" } '
            '},\n'
            '];\n'
            'for (const f of ["src/a.ts", "src/legacy/old.ts", "dist/x.js", "lib/a.min.js", '
            '"tools/run.js", "src/deep/a.test.ts", "a.test.ts"]) console.log(f, '
            'JSON.stringify(rulesFor(f, configs)));\n',
  'hint': 'Функция matches(file, pattern) с учётом basename; затем один проход по configs.',
  'expected': ['src/a.ts {"semi":"error","no-var":"off","@ts/no-any":"warn","strict":"error"}',
               'src/legacy/old.ts {"semi":"error","no-var":"off","@ts/no-any":"warn"}',
               'dist/x.js null',
               'lib/a.min.js null',
               'tools/run.js {"semi":"error","no-var":"error"}',
               'src/deep/a.test.ts '
               '{"semi":"error","no-var":"off","@ts/no-any":"warn","no-console":"off","strict":"error"}',
               'a.test.ts {"semi":"error","no-var":"error","no-console":"off"}']},
 {'id': 'j27-apply-fixes',
  'mode': 'js',
  'title': 'Применение автоисправлений',
  'statement': 'Напишите applyFixes(text, fixes): fixes — массив { range: [start, end], text } '
               '(замена text.slice(start, end) на новую строку; start ≤ end). Исправления '
               'применяются по возрастанию start; при пересечении с уже принятым исправлением '
               '(start меньше конца принятого) — пропускается. Вставка в ту же точку (start === '
               'end принятого) допустима. Равные по start сортируются по порядку в массиве. '
               'Верните { output, applied, skipped } — число применённых и пропущенных. Исходный '
               'массив fixes не изменять.',
  'starter': 'function applyFixes(text, fixes) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (s, f) => console.log(JSON.stringify(applyFixes(s, f)));\n'
            't("var a = 1; var b = 2;", [{ range: [0, 3], text: "let" }, { range: [11, 14], text: '
            '"let" }]);\n'
            't("var a = 1; var b = 2;", [{ range: [11, 14], text: "let" }, { range: [0, 3], text: '
            '"let" }]);\n'
            't("abcdef", [{ range: [1, 4], text: "X" }, { range: [2, 3], text: "Y" }, { range: [4, '
            '5], text: "Z" }]);\n'
            't("abc", [{ range: [1, 1], text: "-" }, { range: [1, 1], text: "+" }]);\n'
            't("abc", [{ range: [0, 1], text: "X" }, { range: [1, 1], text: "!" }]);\n'
            't("abc", []);\n'
            'const fx = [{ range: [2, 3], text: "Q" }, { range: [0, 1], text: "P" }]; '
            'applyFixes("abc", fx); console.log(fx[0].text);\n',
  'hint': 'Отсортируйте копию (устойчиво), пройдите, отслеживая конец последнего принятого; '
          'собирайте результат по кускам.',
  'expected': ['{"output":"let a = 1; let b = 2;","applied":2,"skipped":0}',
               '{"output":"let a = 1; let b = 2;","applied":2,"skipped":0}',
               '{"output":"aXZf","applied":2,"skipped":1}',
               '{"output":"a-+bc","applied":2,"skipped":0}',
               '{"output":"X!bc","applied":2,"skipped":0}',
               '{"output":"abc","applied":0,"skipped":0}',
               'Q']},
 {'id': 'j27-walk-ast',
  'mode': 'js',
  'title': 'Обход дерева (AST)',
  'statement': 'Напишите walk(node, visitor) и findAll(node, type). Узел — объект { type, ... }; '
               'дети — значения полей, являющиеся узлами (объект с полем type) или массивами узлов '
               '(в порядке полей объекта). walk вызывает visitor.enter(node, parent) перед обходом '
               'детей и visitor.leave(node, parent) после; если enter вернул false — дети этого '
               'узла пропускаются (leave всё равно вызывается). Порядок — в глубину, слева '
               'направо. findAll возвращает массив узлов с данным type в порядке входа (enter).',
  'starter': 'function walk(node, visitor, parent = null) {\n'
             '}\n'
             'function findAll(node, type) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const ast = { type: "Program", body: [\n'
            '  { type: "VarDecl", name: "a", init: { type: "Num", value: 1 } },\n'
            '  { type: "ExprStmt", expr: { type: "Call", callee: { type: "Ident", name: "f" }, '
            'args: [{ type: "Num", value: 2 }, { type: "Ident", name: "a" }] } },\n'
            '] };\n'
            'const log = [];\n'
            'walk(ast, { enter(n, p) { log.push("+" + n.type + (p ? "<" + p.type : "")); }, '
            'leave(n) { log.push("-" + n.type); } });\n'
            'console.log(log.join(" "));\n'
            'const log2 = [];\n'
            'walk(ast, { enter(n) { log2.push(n.type); return n.type !== "Call"; }, leave(n) { if '
            '(n.type === "Call") log2.push("leave-call"); } });\n'
            'console.log(log2.join(" "));\n'
            'console.log(findAll(ast, "Num").map((n) => n.value).join(","), findAll(ast, '
            '"Ident").map((n) => n.name).join(","), findAll(ast, "Nope").length);\n',
  'hint': 'Функция children(node) собирает узлы из полей; walk рекурсивен.',
  'expected': ['+Program +VarDecl<Program +Num<VarDecl -Num -VarDecl +ExprStmt<Program '
               '+Call<ExprStmt +Ident<Call -Ident +Num<Call -Num +Ident<Call -Ident -Call '
               '-ExprStmt -Program',
               'Program VarDecl Num ExprStmt Call leave-call',
               '1,2 f,a 0']},
 {'id': 'j27-pretty-print',
  'mode': 'js',
  'title': 'Печать структур по ширине (как Prettier)',
  'statement': 'Напишите format(value, width = 40): печатает значение в стиле JSON (строки в '
               'двойных кавычках; ключи объектов — без кавычек, если это идентификатор, иначе в '
               'кавычках) по правилам: если вся запись помещается в width символов (с учётом '
               'отступа уровня) — одной строкой: «[1, 2, 3]», «{ a: 1, b: 2 }» (пробелы внутри '
               'фигурных скобок, пустые «[]» и «{}»); иначе — каждый элемент на своей строке с '
               'отступом 2 пробела на уровень и запятой после каждого, кроме последнего; '
               'закрывающая скобка — на отдельной строке с отступом родителя. Отступ текущего '
               'уровня включается в проверку ширины (уровень × 2 + длина однострочной записи ≤ '
               'width; для значения внутри объекта длина записи включает «ключ: »).',
  'starter': 'function format(value, width = 40) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'console.log(format([1, 2, 3]));\n'
            'console.log(format({ a: 1, b: "x", "c-d": true }));\n'
            'console.log(format({ name: "Alexander", items: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, '
            '12], nested: { deep: { deeper: [1, 2] } } }));\n'
            'console.log(format([{ id: 1, tags: ["a", "b"] }, { id: 2, tags: [] }, {}], 30));\n'
            'console.log(format("str"), format(null), format([]), format({}));\n'
            'console.log(format({ k: [10000000000, 20000000000, 30000000000] }, 24));\n',
  'hint': 'Рекурсивная функция fmt(value, level, prefixLen): сначала однострочный вариант, '
          'проверьте ширину.',
  'expected': ['[1, 2, 3]',
               '{ a: 1, b: "x", "c-d": true }',
               '{',
               '  name: "Alexander",',
               '  items: [',
               '    1,',
               '    2,',
               '    3,',
               '    4,',
               '    5,',
               '    6,',
               '    7,',
               '    8,',
               '    9,',
               '    10,',
               '    11,',
               '    12',
               '  ],',
               '  nested: { deep: { deeper: [1, 2] } }',
               '}',
               '[',
               '  { id: 1, tags: ["a", "b"] },',
               '  { id: 2, tags: [] },',
               '  {}',
               ']',
               '"str" null [] {}',
               '{',
               '  k: [',
               '    10000000000,',
               '    20000000000,',
               '    30000000000',
               '  ]',
               '}']},
 {'id': 'j27-quotes',
  'mode': 'js',
  'title': 'Нормализация кавычек',
  'statement': 'Напишите normalizeQuotes(src, quote = \'"\'): строковые литералы в «\'…\'» и «"…"» '
               'приводятся к кавычкам quote. Литерал не меняется, если внутри него больше символов '
               'целевой кавычки, чем другой (тогда выгоднее оставить как есть). При замене: '
               'экранирование целевой кавычки внутри добавляется (\\"), а у другой кавычки лишнее '
               "экранирование снимается (\\' → '). Шаблонные строки в обратных кавычках и "
               'комментарии (// и /* */) не трогаются, но их содержимое не должно сбивать разбор '
               'строк. Остальной текст не меняется.',
  'starter': 'function normalizeQuotes(src, quote = \'"\') {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (s, q) => console.log(normalizeQuotes(s, q));\n'
            't("const a = \'x\', b = \\"y\\";");\n'
            't("const s = \'say \\"hi\\"\';");\n'
            't("const s = \'it\\\\\'s\';");\n'
            't(\'const s = "it\\\'s";\', "\'");\n'
            't("const m = \'a \\"b\\" \\\\\'c\\\\\'\';");\n'
            't("// \'comment\' stays\\nconst a = \'q\'; /* \'block\' */ const t = `\'tpl\'`;");\n'
            't("const e = \'\';", \'"\');\n'
            't("x = \'a\' + \'b\'", "\'");\n',
  'hint': 'Токенизируйте по очереди: комментарий, шаблон, строка, прочее; строки переписывайте.',
  'expected': ['const a = "x", b = "y";',
               'const s = \'say "hi"\';',
               'const s = "it\'s";',
               'const s = "it\'s";',
               'const m = "a \\"b\\" \'c\'";',
               "// 'comment' stays",
               'const a = "q"; /* \'block\' */ const t = `\'tpl\'`;',
               'const e = "";',
               "x = 'a' + 'b'"]},
 {'id': 'j27-asi',
  'mode': 'js',
  'title': 'Опасные строки без точки с запятой',
  'statement': 'Напишите findAsiHazards(src): без точек с запятой возможна беда — строка, '
               'начинающаяся с «(», «[», «`», «+», «-», «/» (не начало комментария «//» и «/*»), '
               '«*» продолжает предыдущее выражение. Верните отсортированный массив номеров строк '
               '(с 1), которые начинаются (после пробелов) с одного из этих символов, при условии '
               'что ближайшая предыдущая непустая строка не заканчивается на «;», «{», «}», «,», '
               '«(», «[» (после обрезки пробелов и без учёта комментариев «// …» в конце) и не '
               'является началом файла. Пустые строки и строки-комментарии (// …) пропускаются при '
               'поиске предыдущей.',
  'starter': 'function findAsiHazards(src) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const t = (s) => console.log(JSON.stringify(findAsiHazards(s)));\n'
            't("const a = 1\\n(function () {})()");\n'
            't("const a = 1;\\n(function () {})()");\n'
            't("let x = y\\n[1, 2].forEach(f)");\n'
            't("let x = y\\n`tpl`.length");\n'
            't("a = b\\n+c");\n'
            't("a = b\\n// note\\n\\n-c");\n'
            't("a = b // trailing\\n(c)");\n'
            't("if (x) {\\n  (y)()\\n}");\n'
            't("f(\\n  [1]\\n)");\n'
            't("a = b\\n/* c */ d\\n// e");\n'
            't("(first)");\n'
            't("x = 1,\\n[2]");\n',
  'hint': 'Для каждой строки найдите предыдущую значимую; уберите хвостовой // комментарий и '
          'пробелы.',
  'expected': ['[2]', '[]', '[2]', '[2]', '[2]', '[4]', '[2]', '[]', '[]', '[]', '[]', '[]']},
 {'id': 'j27-sort-imports',
  'mode': 'js',
  'title': 'Сортировка импортов',
  'statement': 'Напишите sortImports(lines): lines — строки import (по одной в строке вида «import '
               "… from 'модуль';» или «import 'модуль';»). Верните новый массив строк, "
               'сгруппированных и отсортированных: группы идут по порядку — 1) встроенные '
               '(«node:…» в модуле), 2) пакеты (модуль не начинается с «.» и «/»), 3) '
               'относительные («./», «../»); внутри группы — по имени модуля (сравнение строк как '
               'есть); при равных модулях порядок исходный. Между непустыми группами вставляется '
               "пустая строка (''). Дубликаты строк не удаляются.",
  'starter': 'function sortImports(lines) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const lines = [\n'
            '  "import b from \'./b.js\';", "import fs from \'node:fs\';", "import React from '
            '\'react\';", "import \'./side.css\';", "import a from \'../a.js\';",\n'
            '  "import zod from \'zod\';", "import path from \'node:path\';", "import lodash from '
            '\\"lodash\\";", "import { x } from \'./b.js\';", "import c from \'/abs.js\';",\n'
            '];\n'
            'console.log(JSON.stringify(sortImports(lines), null, 1));\n'
            'console.log(JSON.stringify(sortImports(["import z from \'./z\';", "import y from '
            '\'./y\';"])));\n'
            'console.log(JSON.stringify(sortImports([])));\n',
  'hint': 'Извлеките модуль регулярным выражением; ключ сортировки — (группа, модуль, исходный '
          'индекс).',
  'expected': ['[',
               ' "import fs from \'node:fs\';",',
               ' "import path from \'node:path\';",',
               ' "",',
               ' "import lodash from \\"lodash\\";",',
               ' "import React from \'react\';",',
               ' "import zod from \'zod\';",',
               ' "",',
               ' "import a from \'../a.js\';",',
               ' "import b from \'./b.js\';",',
               ' "import { x } from \'./b.js\';",',
               ' "import \'./side.css\';",',
               ' "import c from \'/abs.js\';"',
               ']',
               '["import y from \'./y\';","import z from \'./z\';"]',
               '[]']},
 {'id': 'j27-editorconfig',
  'mode': 'js',
  'title': 'Разбор .editorconfig',
  'statement': 'Напишите parseEditorConfig(text) и editorConfigFor(sections, file). '
               'parseEditorConfig: строки; «#» и «;» в начале — комментарии; «[маска]» открывает '
               'секцию; «ключ = значение» (ключ в нижнем регистре, пробелы обрезаются) относится к '
               'последней секции (до первой секции — игнорируется). Значения: «true»/«false» → '
               'boolean, целые числа → number, остальное — строка (в нижнем регистре для известных '
               'значений не приводить). Результат — массив { pattern, props }. editorConfigFor: '
               'применяются подходящие секции по порядку (поздние перекрывают); маска: «*» — все '
               'файлы; «*.ext» — по расширению; «*.{a,b}» — любое из расширений; точное имя файла '
               '(без «/») сравнивается с именем файла в любом каталоге. Возвращает объединённый '
               'объект свойств.',
  'starter': 'function parseEditorConfig(text) {\n'
             '}\n'
             'function editorConfigFor(sections, file) {\n'
             '}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const text = `\n'
            '# top comment\n'
            'root = true\n'
            '[*]\n'
            'indent_style = space\n'
            'indent_size = 2\n'
            'end_of_line = lf\n'
            'insert_final_newline = true\n'
            '\n'
            '; makefiles use tabs\n'
            '[Makefile]\n'
            'indent_style = tab\n'
            '\n'
            '[*.{md,txt}]\n'
            'trim_trailing_whitespace = false\n'
            'max_line_length = 100\n'
            '\n'
            '[*.js]\n'
            'indent_size = 4\n'
            '`;\n'
            'const s = parseEditorConfig(text);\n'
            'console.log(JSON.stringify(s));\n'
            'for (const f of ["src/a.js", "README.md", "Makefile", "sub/Makefile", "data.json", '
            '"notes.txt"]) console.log(f, JSON.stringify(editorConfigFor(s, f)));\n'
            'console.log(JSON.stringify(parseEditorConfig("")));\n',
  'hint': 'Маску преобразуйте в RegExp: *.{a,b} → \\.(a|b)$; сравнивайте с basename.',
  'expected': ['[{"pattern":"*","props":{"indent_style":"space","indent_size":2,"end_of_line":"lf","insert_final_newline":true}},{"pattern":"Makefile","props":{"indent_style":"tab"}},{"pattern":"*.{md,txt}","props":{"trim_trailing_whitespace":false,"max_line_length":100}},{"pattern":"*.js","props":{"indent_size":4}}]',
               'src/a.js '
               '{"indent_style":"space","indent_size":4,"end_of_line":"lf","insert_final_newline":true}',
               'README.md '
               '{"indent_style":"space","indent_size":2,"end_of_line":"lf","insert_final_newline":true,"trim_trailing_whitespace":false,"max_line_length":100}',
               'Makefile '
               '{"indent_style":"tab","indent_size":2,"end_of_line":"lf","insert_final_newline":true}',
               'sub/Makefile '
               '{"indent_style":"tab","indent_size":2,"end_of_line":"lf","insert_final_newline":true}',
               'data.json '
               '{"indent_style":"space","indent_size":2,"end_of_line":"lf","insert_final_newline":true}',
               'notes.txt '
               '{"indent_style":"space","indent_size":2,"end_of_line":"lf","insert_final_newline":true,"trim_trailing_whitespace":false,"max_line_length":100}',
               '[]']},
 {'id': 'j27-lint-staged',
  'mode': 'js',
  'title': 'Команды lint-staged',
  'statement': 'Напишите planCommands(files, config): files — изменённые файлы, config — { маска: '
               'команда | [команды] }. Маска: «*.ext», «*.{a,b}» или точное имя (сравнение с '
               'именем файла в любом каталоге). Для каждой маски (в порядке config) возьмите '
               'подходящие файлы (в порядке files); если их нет — маска пропускается. Каждая '
               'команда маски даёт запись { cmd, files }, где cmd — строка команды + пробел + '
               'имена файлов; имя файла с пробелом берётся в двойные кавычки. Записи идут в '
               'порядке: маски по порядку конфигурации, внутри — команды по порядку. Результат — '
               'массив строк-команд.',
  'starter': 'function planCommands(files, config) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const config = { "*.{ts,tsx}": ["eslint --fix", "prettier --write"], "*.css": '
            '"stylelint --fix", "package.json": ["sort-package-json"], "*.md": "prettier --write" '
            '};\n'
            'const t = (f) => console.log(JSON.stringify(planCommands(f, config)));\n'
            't(["src/a.ts", "src/b.tsx", "styles/main.css", "README.md"]);\n'
            't(["a.js"]);\n'
            't(["pkg/package.json", "package.json", "my file.md", "x.ts"]);\n'
            't([]);\n',
  'hint': 'Функция matches(pattern, file); затем двойной цикл по маскам и командам.',
  'expected': ['["eslint --fix src/a.ts src/b.tsx","prettier --write src/a.ts '
               'src/b.tsx","stylelint --fix styles/main.css","prettier --write README.md"]',
               '[]',
               '["eslint --fix x.ts","prettier --write x.ts","sort-package-json pkg/package.json '
               'package.json","prettier --write \\"my file.md\\""]',
               '[]']},
 {'id': 'j27-ci-jobs',
  'mode': 'js',
  'title': 'Какие задачи CI запускать',
  'statement': 'Напишите planJobs(changed, rules, needs): changed — изменённые файлы, rules — [{ '
               'paths: [маски], job }], needs — { job: [задачи-зависимости] }. Маска: «**» — любой '
               'файл; «dir/**» — файлы внутри каталога; «*.ext» — по расширению в любом каталоге; '
               'точное имя файла. Задача запускается, если подходит хотя бы одно изменение хотя бы '
               'под одну маску её правил. Затем добавьте все транзитивные зависимости запущенных '
               'задач. Верните массив задач в порядке запуска: зависимости раньше зависящих; среди '
               "готовых — по алфавиту. Цикл зависимостей — Error('Circular needs').",
  'starter': 'function planJobs(changed, rules, needs) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const rules = [\n'
            '  { paths: ["src/**", "*.ts"], job: "lint" }, { paths: ["src/**"], job: "test" }, { '
            'paths: ["docs/**", "*.md"], job: "docs" },\n'
            '  { paths: ["package.json", "package-lock.json"], job: "install" }, { paths: ["**"], '
            'job: "audit" },\n'
            '];\n'
            'const needs = { lint: ["install"], test: ["install", "lint"], docs: [], install: [], '
            'audit: [] };\n'
            'const t = (c, n = needs) => { try { console.log(JSON.stringify(c), planJobs(c, rules, '
            'n).join(" ")); } catch (e) { console.log("!" + e.message); } };\n'
            't(["src/a.ts"]); t(["docs/guide.md"]); t(["README.md"]); t(["package.json"]); t([]); '
            't(["tools/x.sh"]); t(["src/x.ts", "docs/y.md"]);\n'
            't(["src/a.ts"], { lint: ["test"], test: ["lint"] });\n',
  'hint': 'Сначала множество запущенных задач с замыканием по needs, затем топологическая '
          'сортировка с выбором минимального имени.',
  'expected': ['["src/a.ts"] audit install lint test',
               '["docs/guide.md"] audit docs',
               '["README.md"] audit docs',
               '["package.json"] audit install',
               '[]',
               '["tools/x.sh"] audit',
               '["src/x.ts","docs/y.md"] audit docs install lint test',
               '!Circular needs']},
 {'id': 'j27-tsconfig-diff',
  'mode': 'js',
  'title': 'Различия tsconfig',
  'statement': 'Напишите diffCompilerOptions(a, b): a и b — compilerOptions. Результат { added, '
               'removed, changed, weakened }. added — ключи только в b, removed — только в a, '
               'changed — { key, from, to } для общих ключей с разными значениями (сравнение '
               'JSON.stringify); всё по алфавиту ключа. weakened — ключи из списка строгих '
               '(strict, noImplicitAny, strictNullChecks, noUncheckedIndexedAccess, '
               'exactOptionalPropertyTypes, noImplicitReturns), которые были true в a и стали '
               'false или исчезли в b (по алфавиту).',
  'starter': 'function diffCompilerOptions(a, b) {\n}\n',
  'driver': '/*__DRIVER__*/\n'
            '\n'
            'const a = { strict: true, target: "ES2020", noImplicitAny: true, '
            'noUncheckedIndexedAccess: true, lib: ["dom"], noEmit: true };\n'
            'const b = { strict: false, target: "ES2022", lib: ["dom", "es2022"], skipLibCheck: '
            'true, noEmit: true, exactOptionalPropertyTypes: true };\n'
            'console.log(JSON.stringify(diffCompilerOptions(a, b)));\n'
            'console.log(JSON.stringify(diffCompilerOptions(a, a)));\n'
            'console.log(JSON.stringify(diffCompilerOptions({}, { strict: true })));\n',
  'hint': 'Объединение ключей, затем ветвление; weakened — отдельный фильтр по списку.',
  'expected': ['{"added":["exactOptionalPropertyTypes","skipLibCheck"],"removed":["noImplicitAny","noUncheckedIndexedAccess"],"changed":[{"key":"lib","from":["dom"],"to":["dom","es2022"]},{"key":"strict","from":true,"to":false},{"key":"target","from":"ES2020","to":"ES2022"}],"weakened":["noImplicitAny","noUncheckedIndexedAccess","strict"]}',
               '{"added":[],"removed":[],"changed":[],"weakened":[]}',
               '{"added":["strict"],"removed":[],"changed":[],"weakened":[]}']}]}
