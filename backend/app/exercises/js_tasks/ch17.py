"""Задачи книги «Современный Frontend», глава 17 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {17: [{'id': 'j17-form-entries',
       'mode': 'js',
       'title': 'Что попадёт в данные формы',
       'statement': 'Форма — массив элементов { tag: "input"|"select"|"textarea"|"button", type?, name?, '
                    'value?, checked?, disabled?, multiple?, options?: [{ value, selected }] } в порядке '
                    'документа. Напишите функцию formEntries(elements, submitter = null) → массив пар [name, '
                    'value] по правилам HTML: элементы без name или disabled пропускаются; input type '
                    'checkbox/radio — только checked (значение value или «on», если не задано); input типов '
                    'button, reset, image, submit и тег button — только если это submitter (кнопка, которой '
                    'отправили); select без multiple — выбранная опция (если ни одной не выбрано — первая); '
                    'select multiple — пара на каждую выбранную; textarea и прочие input — value (пустая '
                    'строка, если нет); input type file без файла пропускается (в этой модели: value === '
                    'undefined).',
       'starter': 'function formEntries(elements, submitter) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const ok = { tag: "button", type: "submit", name: "send", value: "yes" }, other = { tag: '
                 '"button", type: "submit", name: "draft", value: "1" };\n'
                 'const form = [\n'
                 '  { tag: "input", type: "text", name: "name", value: "Ада" }, { tag: "input", type: '
                 '"text", value: "без имени" }, { tag: "input", type: "text", name: "off", value: "x", '
                 'disabled: true },\n'
                 '  { tag: "input", type: "checkbox", name: "agree", checked: true }, { tag: "input", type: '
                 '"checkbox", name: "news", value: "yes", checked: false }, { tag: "input", type: '
                 '"checkbox", name: "tags", value: "a", checked: true }, { tag: "input", type: "checkbox", '
                 'name: "tags", value: "b", checked: true },\n'
                 '  { tag: "input", type: "radio", name: "size", value: "s" }, { tag: "input", type: '
                 '"radio", name: "size", value: "m", checked: true },\n'
                 '  { tag: "select", name: "city", options: [{ value: "msk" }, { value: "spb", selected: '
                 'true }] }, { tag: "select", name: "first", options: [{ value: "one" }, { value: "two" }] '
                 '},\n'
                 '  { tag: "select", name: "multi", multiple: true, options: [{ value: "x", selected: true '
                 '}, { value: "y" }, { value: "z", selected: true }] },\n'
                 '  { tag: "textarea", name: "bio" }, { tag: "input", type: "file", name: "photo" }, { tag: '
                 '"input", type: "hidden", name: "csrf", value: "tok" }, ok, other,\n'
                 '];\n'
                 'console.log(JSON.stringify(formEntries(form, ok)));\n'
                 'console.log(JSON.stringify(formEntries(form, null)).length, '
                 'JSON.stringify(formEntries(form, other)).includes("draft"), JSON.stringify(formEntries([], '
                 'ok)));\n',
       'hint': 'Пройдите по элементам в порядке документа; для каждого вида — своё правило.',
       'expected': ['[["name","Ада"],["agree","on"],["tags","a"],["tags","b"],["size","m"],["city","spb"],["first","one"],["multi","x"],["multi","z"],["bio",""],["csrf","tok"],["send","yes"]]',
                    '155 true []']},
      {'id': 'j17-urlencoded',
       'mode': 'js',
       'title': 'application/x-www-form-urlencoded',
       'statement': 'Напишите функции encodeForm(entries) → строка «k=v&k2=v2» (пары [имя, значение]): имена '
                    'и значения кодируются как в формах — пробел становится «+», символы вне набора A–Z a–z '
                    '0–9 * - . _ кодируются в процентную запись UTF-8 (заглавные hex-цифры); и '
                    'decodeForm(str) → массив пар [имя, значение] в порядке появления (пустая строка → []; '
                    '«+» → пробел; «%XX» декодируется; пара без «=» — значение пустая строка; неверный % — '
                    'оставить как есть). encodeURIComponent и URLSearchParams использовать нельзя.',
       'starter': 'function encodeForm(entries) {\n}\nfunction decodeForm(str) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'console.log(encodeForm([["name", "Ада Лавлейс"], ["q", "a&b=c"], ["k", "~!\'()"], ["sp", '
                 '"a b+c"], ["e", ""]]));\n'
                 'console.log(encodeForm([]), encodeForm([["a", "1"], ["a", "2"]]), encodeForm([["ключ", '
                 '"😀"]]));\n'
                 'console.log(JSON.stringify(decodeForm("name=%D0%90%D0%B4%D0%B0+%D0%9B&q=a%26b%3Dc&flag&e=&x=%ZZ&y=100%")));\n'
                 'console.log(JSON.stringify(decodeForm("")), JSON.stringify(decodeForm("a=1&a=2")), '
                 'JSON.stringify(decodeForm("a=b=c")));\n'
                 'const pairs = [["x y", "é+ü"], ["a&b", "c=d"], ["ж", "\\n"]];\n'
                 'console.log(JSON.stringify(decodeForm(encodeForm(pairs))) === JSON.stringify(pairs));\n'
                 'console.log(__count("encodeURI" + "Component") + __count("URLSear" + "chParams"));\n',
       'hint': 'Кодируйте UTF-8 байты; при декодировании накапливайте байты подряд идущих %XX и собирайте '
               'строку.',
       'expected': ['name=%D0%90%D0%B4%D0%B0+%D0%9B%D0%B0%D0%B2%D0%BB%D0%B5%D0%B9%D1%81&q=a%26b%3Dc&k=%7E%21%27%28%29&sp=a+b%2Bc&e=',
                    ' a=1&a=2 %D0%BA%D0%BB%D1%8E%D1%87=%F0%9F%98%80',
                    '[["name","Ада Л"],["q","a&b=c"],["flag",""],["e",""],["x","%ZZ"],["y","100%"]]',
                    '[] [["a","1"],["a","2"]] [["a","b=c"]]',
                    'true',
                    '0']},
      {'id': 'j17-multipart',
       'mode': 'js',
       'title': 'multipart/form-data',
       'statement': 'Напишите функцию buildMultipart(parts, boundary): parts — массив { name, value } '
                    '(текстовое поле) или { name, filename, type, data (строка) }; тело: для каждой части '
                    '«--boundary\\r\\n» + «Content-Disposition: form-data; name=\\"имя\\"» (для файла '
                    'добавляется «; filename=\\"имя\\"» и строка «Content-Type: тип») + пустая строка + '
                    'данные + «\\r\\n»; в конце «--boundary--\\r\\n». И функцию parseMultipart(body, '
                    'boundary) → массив тех же объектов (value для текстовых, filename/type/data для файлов; '
                    'name/filename — без экранирования). Кавычки внутри имён экранируйте как %22.',
       'starter': 'function buildMultipart(parts, boundary) {\n'
                  '}\n'
                  'function parseMultipart(body, boundary) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const parts = [{ name: "title", value: "Привет\\nмир" }, { name: "photo", filename: '
                 '"a\\"b.txt", type: "text/plain", data: "строка 1\\r\\nстрока 2" }, { name: "empty", value: '
                 '"" }];\n'
                 'const body = buildMultipart(parts, "XYZ");\n'
                 'console.log(JSON.stringify(body));\n'
                 'console.log(JSON.stringify(canon(parseMultipart(body, "XYZ"))) === '
                 'JSON.stringify(canon(parts)));\n'
                 'console.log(JSON.stringify(canon(parseMultipart(body, "XYZ"))));\n'
                 'console.log(JSON.stringify(buildMultipart([], "B")), '
                 'JSON.stringify(parseMultipart("--B--\\r\\n", "B")));\n',
       'hint': 'Разделитель --boundary, заголовки части, пустая строка, данные; при разборе делите по '
               'разделителю.',
       'expected': ['"--XYZ\\r\\nContent-Disposition: form-data; '
                    'name=\\"title\\"\\r\\n\\r\\nПривет\\nмир\\r\\n--XYZ\\r\\nContent-Disposition: '
                    'form-data; name=\\"photo\\"; filename=\\"a%22b.txt\\"\\r\\nContent-Type: '
                    'text/plain\\r\\n\\r\\nстрока 1\\r\\nстрока 2\\r\\n--XYZ\\r\\nContent-Disposition: '
                    'form-data; name=\\"empty\\"\\r\\n\\r\\n\\r\\n--XYZ--\\r\\n"',
                    'true',
                    '[{"name":"title","value":"Привет\\nмир"},{"data":"строка 1\\r\\nстрока '
                    '2","filename":"a\\"b.txt","name":"photo","type":"text/plain"},{"name":"empty","value":""}]',
                    '"--B--\\r\\n" []']},
      {'id': 'j17-formdata',
       'mode': 'js',
       'title': 'Свой FormData',
       'statement': 'Напишите класс MyFormData: append(name, value), set(name, value) (заменяет все значения '
                    'этого имени одним — на позиции первого, если оно было, иначе в конец), get(name) '
                    '(первое значение или null), getAll(name), has(name), delete(name), entries() (итератор '
                    'пар в порядке добавления), [Symbol.iterator], keys(), values(), forEach(cb), и '
                    'статический MyFormData.from(entries); значения приводятся к строке (кроме '
                    'объектов-файлов: объект с полем name сохраняется как есть).',
       'starter': 'class MyFormData {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const f = new MyFormData();\n'
                 'f.append("a", 1); f.append("b", "x"); f.append("a", true); f.append("c", null);\n'
                 'console.log(JSON.stringify([...f]), f.get("a"), f.get("zzz"), '
                 'JSON.stringify(f.getAll("a")), f.has("b"), f.has("B"));\n'
                 'f.set("a", "один"); console.log(JSON.stringify([...f]));\n'
                 'f.set("new", 5); f.set("b", { name: "file.txt", size: 3 }); '
                 'console.log(JSON.stringify([...f.entries()]), typeof f.get("b"));\n'
                 'f.delete("c"); console.log(JSON.stringify([...f.keys()]), '
                 'JSON.stringify([...f.values()]));\n'
                 'const log = []; f.forEach((v, k) => log.push(k)); console.log(log.join());\n'
                 'console.log(JSON.stringify([...MyFormData.from([["x", 1], ["x", 2]])]), [...new '
                 'MyFormData()].length);\n',
       'hint': 'Внутри — массив пар; set заменяет первое вхождение и удаляет остальные.',
       'expected': ['[["a","1"],["b","x"],["a","true"],["c","null"]] 1 null ["1","true"] true false',
                    '[["a","один"],["b","x"],["c","null"]]',
                    '[["a","один"],["b",{"name":"file.txt","size":3}],["c","null"],["new","5"]] object',
                    '["a","b","new"] ["один",{"name":"file.txt","size":3},"5"]',
                    'a,b,new',
                    '[["x","1"],["x","2"]] 0']},
      {'id': 'j17-search-params',
       'mode': 'js',
       'title': 'Свой URLSearchParams',
       'statement': 'Напишите класс MySearchParams(init): init — строка («?a=1&b=2» или «a=1&b=2»), массив '
                    'пар или объект. Методы: get(name) (первое значение или null), getAll(name), has(name), '
                    'append(name, value), set(name, value) (как у FormData), delete(name), sort() (по имени, '
                    'стабильно), toString() (кодирование как в формах: пробел → «+», остальное — процентная '
                    'запись; безопасные символы A–Za–z0–9*-._), size, entries(). Разбор: «+» — пробел, «%XX» '
                    'декодируется; пара без «=» даёт пустое значение. Используйте собственное кодирование '
                    '(encodeURIComponent и URLSearchParams использовать нельзя).',
       'starter': 'class MySearchParams {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'const p = new '
                 'MySearchParams("?q=%D0%BF%D0%BE%D0%B8%D1%81%D0%BA+%D1%82%D0%B5%D1%81%D1%82&tag=a&tag=b&flag&x=1=2");\n'
                 'console.log(p.get("q"), JSON.stringify(p.getAll("tag")), JSON.stringify(p.get("flag")), '
                 'p.get("x"), p.get("none"), p.has("flag"), p.size);\n'
                 'p.append("tag", "c"); p.set("q", "новый запрос"); p.delete("flag"); p.set("tag", "один");\n'
                 'console.log(p.toString());\n'
                 'p.sort(); console.log(p.toString(), JSON.stringify([...p.entries()]));\n'
                 'console.log(new MySearchParams({ a: 1, b: "x y" }).toString(), new MySearchParams([["k", '
                 '"v"], ["k", "w"]]).toString(), new MySearchParams("").toString() === "", new '
                 'MySearchParams("a=1&&b=2").size);\n'
                 'console.log(__count("encodeURI" + "Component") + __count("new URLSe" + "archParams"));\n',
       'hint': 'Внутри — массив пар; кодирование и декодирование — как в задаче про urlencoded.',
       'expected': ['поиск тест ["a","b"] "" 1=2 null true 5',
                    'q=%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9+%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81&tag=%D0%BE%D0%B4%D0%B8%D0%BD&x=1%3D2',
                    'q=%D0%BD%D0%BE%D0%B2%D1%8B%D0%B9+%D0%B7%D0%B0%D0%BF%D1%80%D0%BE%D1%81&tag=%D0%BE%D0%B4%D0%B8%D0%BD&x=1%3D2 '
                    '[["q","новый запрос"],["tag","один"],["x","1=2"]]',
                    'a=1&b=x+y k=v&k=w true 2',
                    '0']},
      {'id': 'j17-validity',
       'mode': 'js',
       'title': 'ValidityState',
       'statement': 'Поле: { type, value, required, min, max, minLength, maxLength, pattern, step, multiple '
                    '}. Напишите функцию validity(field) → { valueMissing, typeMismatch, patternMismatch, '
                    'tooLong, tooShort, rangeUnderflow, rangeOverflow, stepMismatch, valid } (булевы). '
                    "Правила: пустое значение (строка ''), если не required, не нарушает ничего; "
                    "valueMissing = required и value === ''; typeMismatch для type=email (простой шаблон "
                    '«что-то@что-то.что-то» без пробелов; при multiple — список через запятую) и url '
                    '(схема://…); patternMismatch — значение целиком не подходит под pattern (регулярное '
                    'выражение «^(?:pattern)$»); tooLong/tooShort — длина (в символах Unicode) сравнивается '
                    'с maxLength/minLength; для type=number и range: значение — число (нечисло — '
                    'typeMismatch? нет: badInput считаем typeMismatch), rangeUnderflow/Overflow — по '
                    'min/max; stepMismatch — (value - min(0 по умолчанию)) не делится на step (допуск 1e-9). '
                    'valid — нет ни одного нарушения.',
       'starter': 'function validity(field) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const show = (f) => { const v = validity(f); const bad = Object.keys(v).filter((k) => v[k] '
                 '&& k !== "valid"); console.log(JSON.stringify(f.value), f.type ?? "text", v.valid ? "ok" : '
                 'bad.join("+")); };\n'
                 'show({ type: "text", value: "", required: true }); show({ type: "text", value: "" }); '
                 'show({ type: "text", value: "abc", pattern: "[a-z]+" }); show({ type: "text", value: '
                 '"abc1", pattern: "[a-z]+" });\n'
                 'show({ type: "text", value: "😀😀😀", maxLength: 2 }); show({ type: "text", value: "ab", '
                 'minLength: 3 }); show({ type: "text", value: "abcd", minLength: 2, maxLength: 4 });\n'
                 'show({ type: "email", value: "ada@x.ru" }); show({ type: "email", value: "ada@x" }); '
                 'show({ type: "email", value: "a@b.c, d@e.f", multiple: true }); show({ type: "email", '
                 'value: "a@b.c, oops", multiple: true });\n'
                 'show({ type: "url", value: "https://x.ru/a" }); show({ type: "url", value: "x.ru" });\n'
                 'show({ type: "number", value: "5", min: 1, max: 10 }); show({ type: "number", value: "0", '
                 'min: 1 }); show({ type: "number", value: "11", max: 10 }); show({ type: "number", value: '
                 '"abc" });\n'
                 'show({ type: "number", value: "7", min: 1, step: 3 }); show({ type: "number", value: "8", '
                 'min: 1, step: 3 }); show({ type: "number", value: "0.3", step: 0.1 }); show({ type: '
                 '"number", value: "2.5", step: 1 });\n'
                 'show({ type: "number", value: "", required: true, min: 1 }); show({ type: "range", value: '
                 '"50", min: 0, max: 100, step: 10 });\n',
       'hint': 'Каждое нарушение — независимая проверка; пустое необязательное поле не нарушает ничего.',
       'expected': ['"" text valueMissing',
                    '"" text ok',
                    '"abc" text ok',
                    '"abc1" text patternMismatch',
                    '"😀😀😀" text tooLong',
                    '"ab" text tooShort',
                    '"abcd" text ok',
                    '"ada@x.ru" email ok',
                    '"ada@x" email typeMismatch',
                    '"a@b.c, d@e.f" email ok',
                    '"a@b.c, oops" email typeMismatch',
                    '"https://x.ru/a" url ok',
                    '"x.ru" url typeMismatch',
                    '"5" number ok',
                    '"0" number rangeUnderflow',
                    '"11" number rangeOverflow',
                    '"abc" number typeMismatch',
                    '"7" number ok',
                    '"8" number stepMismatch',
                    '"0.3" number ok',
                    '"2.5" number stepMismatch',
                    '"" number valueMissing',
                    '"50" range ok']},
      {'id': 'j17-form-validate',
       'mode': 'js',
       'title': 'Проверка всей формы',
       'statement': 'Правила заданы схемой { поле: [{ test(value, values) → boolean, message }] } (по '
                    'порядку). Напишите функцию validateForm(schema, values) → { valid, errors: { поле: '
                    'первое сообщение }, firstInvalid: имя первого неверного поля по порядку схемы или null, '
                    'summary: [сообщения всех полей через «поле: сообщение» в порядке схемы] }. Правила '
                    'можно писать с доступом ко всем значениям (для «пароли совпадают»). Поле, для которого '
                    'правила не заданы, игнорируется; если для поля есть ошибки — берётся только первая.',
       'starter': 'function validateForm(schema, values) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const schema = {\n'
                 '  name: [{ test: (v) => !!v, message: "обязательно" }, { test: (v) => v.length >= 2, '
                 'message: "слишком коротко" }],\n'
                 '  email: [{ test: (v) => /@/.test(v ?? ""), message: "нужна @" }],\n'
                 '  password: [{ test: (v) => (v ?? "").length >= 8, message: "минимум 8 символов" }],\n'
                 '  repeat: [{ test: (v, all) => v === all.password, message: "пароли не совпадают" }],\n'
                 '};\n'
                 'const show = (v) => console.log(JSON.stringify(canon(validateForm(schema, v))));\n'
                 'show({ name: "Ада", email: "a@b", password: "12345678", repeat: "12345678" });\n'
                 'show({ name: "", email: "x", password: "123", repeat: "456" });\n'
                 'show({ name: "А", email: "x@y", password: "12345678", repeat: "x" });\n'
                 'show({});\n'
                 'console.log(JSON.stringify(validateForm({}, { a: 1 })));\n',
       'hint': 'Для каждого поля прогоните правила по порядку и остановитесь на первом нарушении.',
       'expected': ['{"errors":{},"firstInvalid":null,"summary":[],"valid":true}',
                    '{"errors":{"email":"нужна @","name":"обязательно","password":"минимум 8 '
                    'символов","repeat":"пароли не совпадают"},"firstInvalid":"name","summary":["name: '
                    'обязательно","email: нужна @","password: минимум 8 символов","repeat: пароли не '
                    'совпадают"],"valid":false}',
                    '{"errors":{"name":"слишком коротко","repeat":"пароли не '
                    'совпадают"},"firstInvalid":"name","summary":["name: слишком коротко","repeat: пароли не '
                    'совпадают"],"valid":false}',
                    '{"errors":{"email":"нужна @","name":"обязательно","password":"минимум 8 '
                    'символов"},"firstInvalid":"name","summary":["name: обязательно","email: нужна '
                    '@","password: минимум 8 символов"],"valid":false}',
                    '{"valid":true,"errors":{},"firstInvalid":null,"summary":[]}']},
      {'id': 'j17-password-strength',
       'mode': 'js',
       'title': 'Надёжность пароля',
       'statement': 'Напишите функцию passwordStrength(pw) → { score (0–4), level: "очень '
                    'слабый"|"слабый"|"средний"|"хороший"|"отличный", hints: [...] }. Баллы: +1 за длину ≥ '
                    '8, +1 за длину ≥ 12, +1 за наличие хотя бы трёх из четырёх классов (строчные, '
                    'заглавные, цифры, прочие символы), +1 за отсутствие слабых признаков (нет подряд 3 '
                    'одинаковых символов, не из списка популярных «123456», «password», «qwerty», «111111», '
                    '«пароль», не состоит только из цифр); итог ограничьте 4; пустой пароль — 0. hints — '
                    'рекомендации в порядке: «Добавьте длину», «Смешайте регистры, цифры и символы», '
                    '«Избегайте повторов и популярных паролей» (только для тех критериев, которые не '
                    'выполнены).',
       'starter': 'function passwordStrength(pw) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'for (const p of ["", "123456", "password", "abcdefgh", "Abcdefg1", "Abcdefg1!xyz", '
                 '"aaaBBB111!!!", "Тест-пароль-2024", "qwerty", "12345678", "Zx9$kLm2"]) '
                 'console.log(JSON.stringify(p), JSON.stringify(passwordStrength(p)));\n',
       'hint': 'Четыре независимых критерия; hints — для невыполненных.',
       'expected': ['"" {"score":0,"level":"очень слабый","hints":["Добавьте длину","Смешайте регистры, '
                    'цифры и символы","Избегайте повторов и популярных паролей"]}',
                    '"123456" {"score":0,"level":"очень слабый","hints":["Добавьте длину","Смешайте '
                    'регистры, цифры и символы","Избегайте повторов и популярных паролей"]}',
                    '"password" {"score":1,"level":"слабый","hints":["Добавьте длину","Смешайте регистры, '
                    'цифры и символы","Избегайте повторов и популярных паролей"]}',
                    '"abcdefgh" {"score":2,"level":"средний","hints":["Добавьте длину","Смешайте регистры, '
                    'цифры и символы"]}',
                    '"Abcdefg1" {"score":3,"level":"хороший","hints":["Добавьте длину"]}',
                    '"Abcdefg1!xyz" {"score":4,"level":"отличный","hints":[]}',
                    '"aaaBBB111!!!" {"score":3,"level":"хороший","hints":["Избегайте повторов и популярных '
                    'паролей"]}',
                    '"Тест-пароль-2024" {"score":4,"level":"отличный","hints":[]}',
                    '"qwerty" {"score":0,"level":"очень слабый","hints":["Добавьте длину","Смешайте '
                    'регистры, цифры и символы","Избегайте повторов и популярных паролей"]}',
                    '"12345678" {"score":1,"level":"слабый","hints":["Добавьте длину","Смешайте регистры, '
                    'цифры и символы","Избегайте повторов и популярных паролей"]}',
                    '"Zx9$kLm2" {"score":3,"level":"хороший","hints":["Добавьте длину"]}']},
      {'id': 'j17-luhn',
       'mode': 'js',
       'title': 'Номер карты: Luhn, бренд, формат',
       'statement': 'Напишите функции luhn(number) → boolean (алгоритм Луна; пробелы и дефисы игнорируются; '
                    'нецифры — false; длина 12–19), brand(number) → «visa» (начинается на 4), «mastercard» '
                    '(51–55 или 2221–2720), «mir» (2200–2204), «amex» (34 или 37), иначе «unknown»; '
                    'formatCard(number) → группы по 4 цифры через пробел (для amex — 4-6-5), '
                    'maskCard(number) → «•••• •••• •••• 1234» (показывает последние 4, группы как в '
                    'formatCard, скрытые цифры заменены на «•»).',
       'starter': 'function luhn(number) {\n'
                  '}\n'
                  'function brand(number) {\n'
                  '}\n'
                  'function formatCard(number) {\n'
                  '}\n'
                  'function maskCard(number) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const cards = ["4111 1111 1111 1111", "5555-5555-5555-4444", "2221000000000009", "2204 '
                 '0000 0000 0000", "378282246310005", "6011111111111117", "4111111111111112", "1234", "4111 '
                 '1111 1111 111a", "5105105105105100", "2720 9999 0000 0004"];\n'
                 'for (const c of cards) console.log(JSON.stringify(c), luhn(c), brand(c), '
                 'JSON.stringify(formatCard(c)), JSON.stringify(maskCard(c)));\n',
       'hint': 'Luhn: каждая вторая цифра справа удваивается; формат и маска — по группам.',
       'expected': ['"4111 1111 1111 1111" true visa "4111 1111 1111 1111" "•••• •••• •••• 1111"',
                    '"5555-5555-5555-4444" true mastercard "5555 5555 5555 4444" "•••• •••• •••• 4444"',
                    '"2221000000000009" true mastercard "2221 0000 0000 0009" "•••• •••• •••• 0009"',
                    '"2204 0000 0000 0000" true mir "2204 0000 0000 0000" "•••• •••• •••• 0000"',
                    '"378282246310005" true amex "3782 822463 10005" "•••• •••• •••0 005"',
                    '"6011111111111117" true unknown "6011 1111 1111 1117" "•••• •••• •••• 1117"',
                    '"4111111111111112" false visa "4111 1111 1111 1112" "•••• •••• •••• 1112"',
                    '"1234" false unknown "1234" "1234"',
                    '"4111 1111 1111 111a" false visa "4111 1111 1111 111a" "•••• •••• •••• 111a"',
                    '"5105105105105100" true mastercard "5105 1051 0510 5100" "•••• •••• •••• 5100"',
                    '"2720 9999 0000 0004" false mastercard "2720 9999 0000 0004" "•••• •••• •••• 0004"']},
      {'id': 'j17-dates',
       'mode': 'js',
       'title': 'Даты в полях ввода',
       'statement': 'Напишите функции parseDate(str) → { y, m, d } или null: формат YYYY-MM-DD (как у input '
                    'type=date), проверка существования дня (31 февраля, 29 февраля не в високосный год — '
                    'null); formatDate({ y, m, d }, "DD.MM.YYYY") → строка (поддержите шаблоны DD, MM, YYYY, '
                    'YY); age(birth, today) → полных лет (оба — объекты { y, m, d }); inRange(date, min, '
                    'max) — включительно (min, max могут быть null); и daysBetween(a, b) → число дней (b - '
                    'a, может быть отрицательным) через григорианский календарь без Date.',
       'starter': 'function parseDate(str) {\n'
                  '}\n'
                  'function formatDate(date, pattern) {\n'
                  '}\n'
                  'function age(birth, today) {\n'
                  '}\n'
                  'function inRange(date, min, max) {\n'
                  '}\n'
                  'function daysBetween(a, b) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'import * as __fs from "node:fs";\n'
                 'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                 '"DRIVER__*/")[0];\n'
                 'const __count = (p) => __src.split(p).length - 1;\n'
                 'for (const s of ["2024-02-29", "2023-02-29", "2024-13-01", "2024-04-31", "2000-02-29", '
                 '"1900-02-29", "2024-1-1", "abc", "0001-01-01", "2024-12-31"]) console.log(s, '
                 'JSON.stringify(parseDate(s)));\n'
                 'const d = { y: 2024, m: 3, d: 5 };\n'
                 'console.log(formatDate(d, "DD.MM.YYYY"), formatDate(d, "YY/MM/DD"), formatDate(d, "YYYY"), '
                 'formatDate({ y: 987, m: 1, d: 9 }, "DD-MM-YYYY"));\n'
                 'console.log(age({ y: 2000, m: 6, d: 15 }, { y: 2024, m: 6, d: 14 }), age({ y: 2000, m: 6, '
                 'd: 15 }, { y: 2024, m: 6, d: 15 }), age({ y: 2024, m: 1, d: 1 }, { y: 2024, m: 1, d: 1 }), '
                 'age({ y: 2000, m: 2, d: 29 }, { y: 2001, m: 2, d: 28 }));\n'
                 'console.log(inRange(d, null, null), inRange(d, { y: 2024, m: 3, d: 5 }, null), inRange(d, '
                 '{ y: 2024, m: 3, d: 6 }, null), inRange(d, null, { y: 2024, m: 3, d: 4 }), inRange(d, { y: '
                 '2020, m: 1, d: 1 }, { y: 2025, m: 1, d: 1 }));\n'
                 'console.log(daysBetween({ y: 2024, m: 1, d: 1 }, { y: 2024, m: 12, d: 31 }), daysBetween({ '
                 'y: 2023, m: 1, d: 1 }, { y: 2024, m: 1, d: 1 }), daysBetween({ y: 2024, m: 3, d: 1 }, { y: '
                 '2024, m: 2, d: 1 }), daysBetween(d, d), daysBetween({ y: 1970, m: 1, d: 1 }, { y: 2000, m: '
                 '1, d: 1 }), daysBetween({ y: 1900, m: 1, d: 1 }, { y: 2000, m: 1, d: 1 }));\n'
                 'console.log(__count("new " + "Date"));\n',
       'hint': 'Проверка дня по таблице длин месяцев с учётом високосного года; разница — через порядковый '
               'номер дня.',
       'expected': ['2024-02-29 {"y":2024,"m":2,"d":29}',
                    '2023-02-29 null',
                    '2024-13-01 null',
                    '2024-04-31 null',
                    '2000-02-29 {"y":2000,"m":2,"d":29}',
                    '1900-02-29 null',
                    '2024-1-1 null',
                    'abc null',
                    '0001-01-01 {"y":1,"m":1,"d":1}',
                    '2024-12-31 {"y":2024,"m":12,"d":31}',
                    '05.03.2024 24/03/05 2024 09-01-0987',
                    '23 24 0 0',
                    'true true false false true',
                    '365 365 -29 0 10957 36524',
                    '0']},
      {'id': 'j17-dirty',
       'mode': 'js',
       'title': 'Изменения в форме',
       'statement': 'Напишите функции diffForm(initial, current) → { changed: { поле: { from, to } }, added: '
                    '[поля, которых не было], removed: [поля, которых больше нет], dirty: boolean } '
                    '(сравнение значений — глубокое для массивов и объектов: порядок элементов массивов '
                    'важен, ключи объектов — нет; порядок полей в массивах результата — по порядку ключей: '
                    'сначала initial, затем current), и reset(initial) → глубокую копию, которую форма '
                    'примет как начальное состояние (изменения копии не затрагивают initial).',
       'starter': 'function diffForm(initial, current) {\n}\nfunction reset(initial) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const init = { name: "Ада", tags: ["a", "b"], addr: { city: "Лондон", zip: 1 }, bio: "" '
                 '};\n'
                 'const show = (cur) => console.log(JSON.stringify(canon(diffForm(init, cur))));\n'
                 'show({ name: "Ада", tags: ["a", "b"], addr: { zip: 1, city: "Лондон" }, bio: "" });\n'
                 'show({ name: "Ада Л.", tags: ["a", "b"], addr: { city: "Лондон", zip: 1 }, bio: "" });\n'
                 'show({ name: "Ада", tags: ["b", "a"], addr: { city: "Париж", zip: 1 }, bio: "", extra: 1 '
                 '});\n'
                 'show({ name: "Ада", tags: ["a", "b"] });\n'
                 'show({});\n'
                 'const r = reset(init); r.addr.city = "X"; r.tags.push("c");\n'
                 'console.log(init.addr.city, init.tags.length, JSON.stringify(diffForm(init, init).dirty), '
                 'r !== init);\n',
       'hint': 'Глубокое сравнение; три категории: изменённые, добавленные, удалённые.',
       'expected': ['{"added":[],"changed":{},"dirty":false,"removed":[]}',
                    '{"added":[],"changed":{"name":{"from":"Ада","to":"Ада Л."}},"dirty":true,"removed":[]}',
                    '{"added":["extra"],"changed":{"addr":{"from":{"city":"Лондон","zip":1},"to":{"city":"Париж","zip":1}},"tags":{"from":["a","b"],"to":["b","a"]}},"dirty":true,"removed":[]}',
                    '{"added":[],"changed":{},"dirty":true,"removed":["addr","bio"]}',
                    '{"added":[],"changed":{},"dirty":true,"removed":["name","tags","addr","bio"]}',
                    'Лондон 2 false true']},
      {'id': 'j17-autosave',
       'mode': 'js',
       'title': 'Автосохранение черновика',
       'statement': 'Даны виртуальные часы FAKE (now, setTimeout, clearTimeout, advance) и хранилище storage '
                    '(getItem, setItem, removeItem — как у Web Storage). Напишите функцию createDraft(key, '
                    'storage, timers, { delay = 500, maxWait = 3000, version = 1 }): возвращает { '
                    'update(values) (отложенное сохранение: через delay мс после последнего update, но не '
                    'позже maxWait с первого несохранённого update), load() → values или null (читает JSON '
                    '{version, savedAt, values}; другая версия или повреждённый JSON → null и запись '
                    'удаляется), clear() (отменяет ожидание и удаляет запись), flush() (сохранить '
                    'немедленно, если есть несохранённое) }. savedAt — timers.now().',
       'starter': 'function createDraft(key, storage, timers, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 '\n'
                 'const FAKE = () => { let t = 0; const timers = new Map(); let id = 1; return { now: () => '
                 't, setTimeout(fn, ms) { const i = id++; timers.set(i, { at: t + ms, fn }); return i; }, '
                 'clearTimeout(i) { timers.delete(i); }, advance(ms) { const end = t + ms; for (;;) { const '
                 'due = [...timers].filter(([, x]) => x.at <= end).sort((a, b) => a[1].at - b[1].at || a[0] '
                 '- b[0])[0]; if (!due) break; timers.delete(due[0]); t = due[1].at; due[1].fn(); } t = end; '
                 '}, pending: () => timers.size }; };\n'
                 'const store = () => { const m = new Map(); return { getItem: (k) => (m.has(k) ? m.get(k) : '
                 'null), setItem: (k, v) => m.set(k, String(v)), removeItem: (k) => m.delete(k), raw: m }; '
                 '};\n'
                 'const c = FAKE(), s = store();\n'
                 'const d = createDraft("form", s, c, { delay: 500, maxWait: 2000, version: 2 });\n'
                 'd.update({ a: 1 }); c.advance(300); d.update({ a: 2 }); c.advance(300); '
                 'console.log(s.raw.size, d.load());\n'
                 'c.advance(200); console.log(s.raw.size, JSON.stringify(d.load()), '
                 'JSON.parse(s.raw.get("form")).savedAt);\n'
                 'for (let i = 0; i < 10; i++) { d.update({ i }); c.advance(400); } '
                 'console.log(JSON.stringify(d.load()), c.now());\n'
                 'c.advance(500); console.log(JSON.stringify(d.load()), c.pending());\n'
                 'd.update({ z: 1 }); d.flush(); console.log(JSON.stringify(d.load()), c.pending()); '
                 'd.flush();\n'
                 'd.update({ q: 1 }); d.clear(); c.advance(5000); console.log(d.load(), s.raw.size);\n'
                 's.setItem("form", JSON.stringify({ version: 1, values: { old: true } })); '
                 'console.log(d.load(), s.raw.size);\n'
                 's.setItem("form", "{плохой json"); console.log(d.load(), s.raw.size);\n',
       'hint': 'Два таймера: «после паузы» и «не позже maxWait»; сохранение отменяет оба.',
       'expected': ['0 null',
                    '1 {"a":2} 800',
                    '{"i":9} 4800',
                    '{"i":9} 0',
                    '{"z":1} 0',
                    'null 0',
                    'null 0',
                    'null 0']},
      {'id': 'j17-set-cookie',
       'mode': 'js',
       'title': 'Разбор и сборка Set-Cookie',
       'statement': 'Напишите функции parseSetCookie(header) → { name, value, path?, domain?, expires? '
                    '(строка), maxAge? (число), secure (boolean), httpOnly (boolean), sameSite? (в нижнем '
                    'регистре: strict/lax/none) } (имена атрибутов без учёта регистра; значение куки может '
                    'содержать «=»; значение декодируется decodeURIComponent, если это возможно, иначе '
                    'остаётся как есть; домен — без ведущей точки в нижнем регистре) и serializeCookie(name, '
                    'value, options) → строка: «имя=значение» (значение кодируется encodeURIComponent) + '
                    'атрибуты в порядке Domain, Path, Expires, Max-Age, SameSite (Strict|Lax|None), Secure, '
                    'HttpOnly; для SameSite=None без Secure бросьте Error("SameSite=None требует Secure").',
       'starter': 'function parseSetCookie(header) {\n'
                  '}\n'
                  'function serializeCookie(name, value, options) {\n'
                  '}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const show = (h) => console.log(JSON.stringify(canon(parseSetCookie(h))));\n'
                 'show("sid=abc123; Path=/; Max-Age=3600; Secure; HttpOnly; SameSite=Lax");\n'
                 'show("theme=dark");\n'
                 'show("tok=a=b=c; DOMAIN=.Example.COM; expires=Wed, 21 Oct 2026 07:28:00 GMT; '
                 'samesite=NONE");\n'
                 'show("name=%D0%90%D0%B4%D0%B0; path=/app");\n'
                 'show("bad=%E0%A4%A; secure");\n'
                 'console.log(serializeCookie("a", "b c"));\n'
                 'console.log(serializeCookie("sid", "значение", { path: "/", domain: "x.ru", maxAge: 60, '
                 'sameSite: "lax", secure: true, httpOnly: true }));\n'
                 'console.log(serializeCookie("t", "1", { expires: "Wed, 21 Oct 2026 07:28:00 GMT", '
                 'sameSite: "NONE", secure: true }));\n'
                 'try { serializeCookie("t", "1", { sameSite: "none" }); } catch (e) { '
                 'console.log(e.message); }\n',
       'hint': 'Разбейте по «;», первая часть — имя=значение; остальные — атрибуты по имени без учёта '
               'регистра.',
       'expected': ['{"httpOnly":true,"maxAge":3600,"name":"sid","path":"/","sameSite":"lax","secure":true,"value":"abc123"}',
                    '{"httpOnly":false,"name":"theme","secure":false,"value":"dark"}',
                    '{"domain":"example.com","expires":"Wed, 21 Oct 2026 07:28:00 '
                    'GMT","httpOnly":false,"name":"tok","sameSite":"none","secure":false,"value":"a=b=c"}',
                    '{"httpOnly":false,"name":"name","path":"/app","secure":false,"value":"Ада"}',
                    '{"httpOnly":false,"name":"bad","secure":true,"value":"%E0%A4%A"}',
                    'a=b%20c',
                    'sid=%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D0%B5; Domain=x.ru; Path=/; Max-Age=60; '
                    'SameSite=Lax; Secure; HttpOnly',
                    't=1; Expires=Wed, 21 Oct 2026 07:28:00 GMT; SameSite=None; Secure',
                    'SameSite=None требует Secure']},
      {'id': 'j17-cookie-jar',
       'mode': 'js',
       'title': 'Хранилище куки (cookie jar)',
       'statement': 'Напишите класс CookieJar(now): store(url, setCookieHeader) (разбирает заголовок '
                    '(простой разбор Set-Cookie: name=value и атрибуты Domain, Path, Max-Age, Secure, '
                    'HttpOnly) и сохраняет; домен по умолчанию — host из url (host-only: подходит только '
                    'точному хосту); с Domain=x.ru — для x.ru и поддоменов; путь по умолчанию — каталог пути '
                    'url (до последнего «/», «/» если пути нет); Max-Age ≤ 0 удаляет куки; Secure-куки '
                    'принимаются только с https), и cookieHeader(url) → строка «a=1; b=2» для запроса: '
                    'подходящие по домену, пути (префикс по границе сегмента), секретности (Secure — только '
                    'https); не просроченные; порядок — длинный путь первым, затем более раннее создание. '
                    'Дубликат (name, domain, path) заменяет прежний.',
       'starter': 'class CookieJar {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let t = 0;\n'
                 'const jar = new CookieJar(() => t);\n'
                 'jar.store("https://shop.example.com/cart/view", "sid=1; Path=/; Secure");\n'
                 'jar.store("https://shop.example.com/cart/view", "cart=2");\n'
                 'jar.store("https://shop.example.com/", "wide=3; Domain=example.com; Path=/");\n'
                 'jar.store("https://shop.example.com/a/b/c", "deep=4; Path=/a/b");\n'
                 'jar.store("http://shop.example.com/", "insecure=5; Secure");\n'
                 'jar.store("https://evil.com/", "stolen=6; Domain=example.com");\n'
                 'console.log(jar.cookieHeader("https://shop.example.com/cart/view"));\n'
                 'console.log(jar.cookieHeader("https://shop.example.com/cart"), "|", '
                 'jar.cookieHeader("https://shop.example.com/a/b/c/d"));\n'
                 'console.log(jar.cookieHeader("http://shop.example.com/cart/view"), "|", '
                 'jar.cookieHeader("https://example.com/"), "|", '
                 'jar.cookieHeader("https://api.example.com/x"));\n'
                 'jar.store("https://shop.example.com/cart/view", "cart=22"); '
                 'console.log(jar.cookieHeader("https://shop.example.com/cart/view"));\n'
                 'jar.store("https://shop.example.com/x", "temp=7; Path=/; Max-Age=10"); '
                 'console.log(jar.cookieHeader("https://shop.example.com/x").includes("temp=7"));\n'
                 't = 10001; console.log(jar.cookieHeader("https://shop.example.com/x").includes("temp"));\n'
                 'jar.store("https://shop.example.com/x", "sid=; Path=/; Max-Age=0"); '
                 'console.log(jar.cookieHeader("https://shop.example.com/x"));\n'
                 'console.log(jar.cookieHeader("https://shop.example.com/cartoon"));\n',
       'hint': 'Куки: {name, value, domain, hostOnly, path, secure, expires}; проверки домена, пути, Secure '
               'и срока при сборке заголовка.',
       'expected': ['cart=2; sid=1; wide=3',
                    'cart=2; sid=1; wide=3 | deep=4; sid=1; wide=3',
                    'cart=2; wide=3 | wide=3 | wide=3',
                    'cart=22; sid=1; wide=3',
                    'true',
                    'false',
                    'wide=3',
                    'wide=3']},
      {'id': 'j17-samesite',
       'mode': 'js',
       'title': 'SameSite: отправлять ли куки',
       'statement': 'Запрос описан: { initiator (адрес страницы-инициатора), target (адрес запроса), method, '
                    'topLevel (навигация верхнего уровня?), type: "navigation"|"subresource"|"form"|"fetch" '
                    '}; куки — { sameSite: "strict"|"lax"|"none"|undefined (по умолчанию как lax), secure }. '
                    'Напишите функцию sameSiteOf(url1, url2) → true, если у адресов один «сайт» (схема и '
                    'домен регистрации: последние две части хоста; localhost и IP — как есть), и '
                    'shouldSend(cookie, request): none — отправляется всегда (но cookie.secure должен быть '
                    'true и target — https, иначе нет); strict — только если сайты совпадают; lax (и '
                    'undefined) — если сайты совпадают, либо запрос — навигация верхнего уровня (topLevel) '
                    'методом GET; Secure-куки не отправляются на http. Для запросов в пределах одного сайта '
                    'все режимы отправляют (кроме Secure на http).',
       'starter': 'function sameSiteOf(url1, url2) {\n}\nfunction shouldSend(cookie, request) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'console.log(sameSiteOf("https://a.example.com/x", "https://b.example.com/y"), '
                 'sameSiteOf("https://example.com", "http://example.com"), sameSiteOf("https://example.com", '
                 '"https://example.org"), sameSiteOf("http://localhost:3000", "http://localhost:8080"), '
                 'sameSiteOf("http://127.0.0.1", "http://127.0.0.2"));\n'
                 'const req = (extra) => ({ initiator: "https://site.com/p", target: "https://site.com/api", '
                 'method: "GET", topLevel: false, type: "fetch", ...extra });\n'
                 'const cross = { initiator: "https://evil.com/", target: "https://site.com/api" };\n'
                 'const cases = [\n'
                 '  ["same strict", { sameSite: "strict", secure: true }, req()],\n'
                 '  ["cross strict nav", { sameSite: "strict", secure: true }, req({ ...cross, topLevel: '
                 'true, type: "navigation" })],\n'
                 '  ["cross lax nav GET", { sameSite: "lax", secure: true }, req({ ...cross, topLevel: true, '
                 'type: "navigation" })],\n'
                 '  ["cross lax nav POST", { sameSite: "lax", secure: true }, req({ ...cross, topLevel: '
                 'true, type: "navigation", method: "POST" })],\n'
                 '  ["cross lax fetch", { sameSite: "lax", secure: true }, req({ ...cross })],\n'
                 '  ["cross default img", { secure: true }, req({ ...cross, type: "subresource" })],\n'
                 '  ["cross none secure", { sameSite: "none", secure: true }, req({ ...cross })],\n'
                 '  ["cross none insecure", { sameSite: "none", secure: false }, req({ ...cross })],\n'
                 '  ["same secure on http", { sameSite: "lax", secure: true }, req({ target: '
                 '"http://site.com/x", initiator: "http://site.com/" })],\n'
                 '  ["same plain on http", { sameSite: "strict", secure: false }, req({ target: '
                 '"http://site.com/x", initiator: "http://site.com/" })],\n'
                 '  ["none on http", { sameSite: "none", secure: true }, req({ ...cross, target: '
                 '"http://site.com/x" })],\n'
                 '];\n'
                 'for (const [n, c, r] of cases) console.log(n.padEnd(20), shouldSend(c, r));\n',
       'hint': 'Сначала Secure/https, затем режим: none, same-site, strict, lax (только навигация GET '
               'верхнего уровня).',
       'expected': ['true false false true false',
                    'same strict          true',
                    'cross strict nav     false',
                    'cross lax nav GET    true',
                    'cross lax nav POST   false',
                    'cross lax fetch      false',
                    'cross default img    false',
                    'cross none secure    true',
                    'cross none insecure  false',
                    'same secure on http  false',
                    'same plain on http   true',
                    'none on http         false']},
      {'id': 'j17-storage',
       'mode': 'js',
       'title': 'Свой Storage',
       'statement': 'Напишите класс MyStorage(quota = 5000): как Web Storage: getItem(key) (null, если нет), '
                    'setItem(key, value) (значения приводятся к строке; «размер» записи — длина ключа + '
                    'длина значения; если сумма размеров всех записей после записи превысит quota — бросить '
                    'ошибку с name «QuotaExceededError» и ничего не менять), removeItem, clear, key(i) (ключ '
                    'по порядку добавления или null), length, и подписчики: onChange(fn) → функция отписки; '
                    'fn вызывается как событие storage: { key, oldValue, newValue } (для clear — key: null; '
                    'запись того же значения событие не генерирует; removeItem несуществующего — тоже).',
       'starter': 'class MyStorage {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const s = new MyStorage(30);\n'
                 'const log = [];\n'
                 'const off = s.onChange((e) => log.push(`${e.key}:${e.oldValue}→${e.newValue}`));\n'
                 's.setItem("a", 1); s.setItem("b", { x: 1 }); s.setItem("a", "1"); s.setItem("a", "22");\n'
                 'console.log(s.length, s.getItem("a"), s.getItem("b"), s.getItem("zzz"), s.key(0), '
                 's.key(1), s.key(2), log.join(" | "));\n'
                 'log.length = 0;\n'
                 'try { s.setItem("big", "x".repeat(30)); } catch (e) { console.log(e.name, s.length, '
                 's.getItem("big")); }\n'
                 's.setItem("a", "x".repeat(10)); console.log(s.getItem("a").length);\n'
                 'try { s.setItem("a", "x".repeat(40)); } catch (e) { console.log(e.name, '
                 's.getItem("a").length); }\n'
                 's.removeItem("b"); s.removeItem("b"); console.log(log.join(" | ").slice(0, 60), '
                 's.length);\n'
                 'off(); s.setItem("c", "1"); s.clear(); s.clear(); console.log(s.length, log.length);\n'
                 'const s2 = new MyStorage(); const l2 = []; s2.onChange((e) => l2.push(e.key)); '
                 's2.setItem("k", "v"); s2.clear(); console.log(l2.join(), s2.key(0));\n',
       'hint': 'Map; размер — сумма длин ключей и значений; событие генерируется только при реальном '
               'изменении.',
       'expected': ['2 22 [object Object] null a b null a:null→1 | b:null→[object Object] | a:1→22',
                    'QuotaExceededError 2 null',
                    '10',
                    'QuotaExceededError 10',
                    'a:22→xxxxxxxxxx | b:[object Object]→null 1',
                    '0 2',
                    'k, null']},
      {'id': 'j17-ttl-storage',
       'mode': 'js',
       'title': 'Хранилище с TTL, пространством имён и версиями',
       'statement': 'Напишите функцию createCache(storage, { namespace, version, now, migrations = {} }): '
                    'возвращает { set(key, value, ttlMs?), get(key, fallback = null), remove(key), keys(), '
                    'purge() }. Записи лежат в storage под ключом «namespace:v<version>:key» как JSON { '
                    'value, expires (ms | null) }; get возвращает fallback для отсутствующих, просроченных '
                    '(запись при этом удаляется) и повреждённых (удаляются); keys() — ключи текущего '
                    'пространства и версии без префикса (не просроченные); purge() — удалить просроченные '
                    'записи и записи старых версий этого namespace (ключи «namespace:v<другая>:…»), вернуть '
                    'число удалённых. Миграции: если для ключа нет записи текущей версии, но есть записи '
                    'прошлой (version - 1) и в migrations[version] задана функция value → newValue, get '
                    'переносит значение (migrate), сохраняет под новым ключом и удаляет старую. storage — { '
                    'getItem, setItem, removeItem, key(i), length }.',
       'starter': 'function createCache(storage, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const mem = () => { const m = new Map(); return { getItem: (k) => (m.has(k) ? m.get(k) : '
                 'null), setItem: (k, v) => m.set(k, String(v)), removeItem: (k) => m.delete(k), key: (i) => '
                 '[...m.keys()][i] ?? null, get length() { return m.size; }, raw: m }; };\n'
                 'let t = 0; const st = mem();\n'
                 'const c1 = createCache(st, { namespace: "app", version: 1, now: () => t });\n'
                 'c1.set("user", { name: "Ада" }); c1.set("temp", 1, 100); c1.set("zero", 0);\n'
                 'console.log(JSON.stringify(c1.get("user")), c1.get("none"), c1.get("none", "запас"), '
                 'c1.get("zero"), JSON.stringify(c1.keys()));\n'
                 't = 100; console.log(c1.get("temp", "истёк"), st.raw.has("app:v1:temp"), '
                 'JSON.stringify(c1.keys()));\n'
                 'st.setItem("app:v1:broken", "{oops"); console.log(c1.get("broken", "битый"), '
                 'st.raw.has("app:v1:broken"));\n'
                 'const c2 = createCache(st, { namespace: "app", version: 2, now: () => t, migrations: { 2: '
                 '(u) => ({ ...u, fullName: u.name }) } });\n'
                 'console.log(JSON.stringify(c2.get("user")), st.raw.has("app:v1:user"), '
                 'st.raw.has("app:v2:user"), JSON.stringify(c2.keys()));\n'
                 'c1.set("legacy", 1); st.setItem("other:v1:x", "{}"); c2.set("x", 1, 10); t = 200;\n'
                 'console.log(c2.purge(), JSON.stringify([...st.raw.keys()].sort()));\n'
                 'c2.remove("user"); console.log(c2.get("user", "нет"), c2.keys().length);\n',
       'hint': 'Префикс namespace:vN:; чтение с проверкой срока и повреждения; миграция из предыдущей версии '
               'при get.',
       'expected': ['{"name":"Ада"} null запас 0 ["user","temp","zero"]',
                    'истёк false ["user","zero"]',
                    'битый false',
                    '{"name":"Ада","fullName":"Ада"} false true ["user"]',
                    '3 ["app:v2:user","other:v1:x"]',
                    'нет 0']},
      {'id': 'j17-tab-sync',
       'mode': 'js',
       'title': 'Синхронизация вкладок по событию storage',
       'statement': 'Две вкладки пишут настройки в общее хранилище. Каждая запись — { value, ts (время '
                    'записи, мс), tab (id вкладки) }. Напишите функцию createSynced(tabId, storage, now, '
                    'key): возвращает { set(settingName, value) (записывает в общий объект JSON по ключу '
                    'key; значение настройки хранится как { value, ts, tab }), get(settingName), '
                    'onStorage(event) → массив имён настроек, которые изменились для этой вкладки (event = { '
                    'key, newValue (строка JSON) }; игнорирует чужие ключи; применяет «последняя запись '
                    'побеждает» по ts, при равенстве — по id вкладки в алфавитном порядке (больший '
                    'побеждает); записи своей вкладки игнорирует) }. Локальный кэш хранит текущие значения: '
                    'get читает его.',
       'starter': 'function createSynced(tabId, storage, now, key) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const mem = () => { const m = new Map(); return { getItem: (k) => (m.has(k) ? m.get(k) : '
                 'null), setItem: (k, v) => m.set(k, v) }; };\n'
                 'const shared = mem(); let t = 0;\n'
                 'const A = createSynced("A", shared, () => t, "settings"), B = createSynced("B", shared, () '
                 '=> t, "settings");\n'
                 'const deliver = (to, from) => to.onStorage({ key: "settings", newValue: '
                 'shared.getItem("settings") });\n'
                 't = 10; A.set("theme", "dark"); console.log(JSON.stringify(deliver(B)), B.get("theme"), '
                 'A.get("theme"));\n'
                 't = 20; B.set("lang", "ru"); t = 30; console.log(JSON.stringify(deliver(A)), '
                 'A.get("lang"), JSON.stringify(deliver(A)));\n'
                 't = 40; A.set("theme", "light"); t = 40; B.set("theme", "blue");\n'
                 'console.log(JSON.stringify(deliver(A)), A.get("theme"), JSON.stringify(deliver(B)), '
                 'B.get("theme"));\n'
                 'console.log(JSON.stringify(A.onStorage({ key: "other", newValue: "{}" })), '
                 'JSON.stringify(A.onStorage({ key: "settings", newValue: null })), '
                 'JSON.stringify(A.onStorage({ key: "settings", newValue: shared.getItem("settings") })));\n'
                 't = 50; A.set("theme", "green"); console.log(JSON.stringify(deliver(B)), '
                 'B.get("theme"));\n',
       'hint': 'Кэш значений с метаданными; правило победителя — большее ts, при равенстве — больший id '
               'вкладки.',
       'expected': ['["theme"] dark dark',
                    '["lang"] ru []',
                    '["theme"] blue [] blue',
                    '[] [] []',
                    '["theme"] green']},
      {'id': 'j17-idb-store',
       'mode': 'js',
       'title': 'Хранилище объектов как в IndexedDB',
       'statement': 'Напишите класс ObjectStore({ keyPath?, autoIncrement = false }): методы add(value, '
                    'key?) → ключ (если запись с таким ключом уже есть — ошибка с name «ConstraintError»; '
                    'ключ берётся из value[keyPath], либо из автоинкремента (1, 2, …; при указании числового '
                    'ключа вручную счётчик подтягивается), либо из аргумента key; если ключа нет совсем — '
                    'DataError), put(value, key?) (создать или заменить), get(key) (копия значения или '
                    'undefined), delete(key), clear(), getAll() (копии в порядке ключей: числа по '
                    'возрастанию раньше строк, строки — по алфавиту), getAllKeys(), count(). Значения '
                    'хранятся копиями (structuredClone): изменение полученного объекта не меняет хранилище.',
       'starter': 'class ObjectStore {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const err = (f) => { try { return f(); } catch (e) { return e.name; } };\n'
                 'const users = new ObjectStore({ keyPath: "id" });\n'
                 'console.log(users.add({ id: 2, name: "Борис" }), users.add({ id: 1, name: "Ада" }), err(() '
                 '=> users.add({ id: 1, name: "Дубль" })), users.put({ id: 1, name: "Ада Л." }), err(() => '
                 'users.add({ name: "без ключа" })));\n'
                 'console.log(JSON.stringify(users.getAll()), JSON.stringify(users.getAllKeys()), '
                 'users.count());\n'
                 'const u = users.get(1); u.name = "ИЗМЕНЕНО"; console.log(users.get(1).name, '
                 'users.get(99));\n'
                 'const log = new ObjectStore({ autoIncrement: true });\n'
                 'console.log(log.add("a"), log.add("b"), log.add("c", 10), log.add("d"), err(() => '
                 'log.add("e", 2)), log.put("f", 2), JSON.stringify(log.getAll()));\n'
                 'const kv = new ObjectStore();\n'
                 'console.log(kv.add({ v: 1 }, "x"), kv.add({ v: 2 }, 5), kv.add({ v: 3 }, "a"), err(() => '
                 'kv.add({ v: 4 })), JSON.stringify(kv.getAllKeys()));\n'
                 'const auto = new ObjectStore({ keyPath: "id", autoIncrement: true }); const o = { title: '
                 '"t" };\n'
                 'console.log(auto.add(o), JSON.stringify(auto.get(1)), o.id, auto.add({ id: 7 }), '
                 'auto.add({ title: "next" }), auto.count());\n'
                 'kv.delete("x"); console.log(kv.count()); kv.clear(); console.log(kv.count());\n',
       'hint': 'Map ключ → копия; счётчик автоинкремента подтягивается при числовых ключах.',
       'expected': ['2 1 ConstraintError 1 DataError',
                    '[{"id":1,"name":"Ада Л."},{"id":2,"name":"Борис"}] [1,2] 2',
                    'Ада Л. undefined',
                    '1 2 10 11 ConstraintError 2 ["a","f","c","d"]',
                    'x 5 a DataError [5,"a","x"]',
                    '1 {"title":"t","id":1} undefined 7 8 3',
                    '2',
                    '0']},
      {'id': 'j17-idb-index',
       'mode': 'js',
       'title': 'Индексы и диапазоны ключей',
       'statement': 'Даны записи (массив объектов). Напишите KeyRange: статические bound(lower, upper, '
                    'lowerOpen = false, upperOpen = false), lowerBound(x, open = false), upperBound(x, open '
                    '= false), only(x) и метод includes(key) (сравнение через обычные <, >). И функцию '
                    'createIndex(records, keyPath, { unique = false }) → объект { get(key) (первая запись с '
                    'таким значением или undefined), getAll(rangeOrKey?) (записи, отсортированные по '
                    'значению индекса (стабильно по исходному порядку), отфильтрованные диапазоном или '
                    'конкретным значением), count(range?), keys() (отсортированные уникальные значения), '
                    'openCursor(range, direction = "next"|"prev") → массив записей в нужном порядке }. При '
                    'unique = true дубликат значения — Error с name «ConstraintError» при создании индекса. '
                    'Записи без значения по keyPath в индекс не попадают.',
       'starter': 'class KeyRange {\n}\nfunction createIndex(records, keyPath, options) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const people = [{ n: "Ада", age: 36 }, { n: "Борис", age: 25 }, { n: "Вера", age: 36 }, { '
                 'n: "Глеб", age: 41 }, { n: "Дина", age: 25 }, { n: "Ёж" }];\n'
                 'const idx = createIndex(people, "age");\n'
                 'const names = (xs) => xs.map((p) => p.n).join();\n'
                 'console.log(names(idx.getAll()), "|", names(idx.getAll(36)), "|", '
                 'names(idx.getAll(KeyRange.bound(25, 36))), "|", names(idx.getAll(KeyRange.bound(25, 36, '
                 'true, false))), "|", names(idx.getAll(KeyRange.bound(25, 36, false, true))));\n'
                 'console.log(names(idx.getAll(KeyRange.lowerBound(36))), "|", '
                 'names(idx.getAll(KeyRange.lowerBound(36, true))), "|", '
                 'names(idx.getAll(KeyRange.upperBound(25))), "|", names(idx.getAll(KeyRange.upperBound(25, '
                 'true))), "|", idx.count(), idx.count(KeyRange.only(25)), idx.count(99));\n'
                 'console.log(idx.get(25).n, idx.get(7), JSON.stringify(idx.keys()), '
                 'names(idx.openCursor(undefined, "prev")), "|", '
                 'names(idx.openCursor(KeyRange.lowerBound(30), "prev")));\n'
                 'const r = KeyRange.bound(1, 5, true, true); console.log(r.includes(1), r.includes(2), '
                 'r.includes(5), KeyRange.only("a").includes("a"), KeyRange.lowerBound("m").includes("z"), '
                 'KeyRange.upperBound("m").includes("z"));\n'
                 'try { createIndex(people, "age", { unique: true }); } catch (e) { console.log(e.name); }\n'
                 'console.log(createIndex(people, "n", { unique: true }).keys().length, createIndex([], '
                 '"x").count(), createIndex([{ a: { b: 1 } }, { a: { b: 0 } }], "a.b").getAll().map((o) => '
                 'o.a.b).join());\n',
       'hint': 'Записи с ключами отсортируйте стабильно; диапазон — объект с проверкой includes(key).',
       'expected': ['Борис,Дина,Ада,Вера,Глеб | Ада,Вера | Борис,Дина,Ада,Вера | Ада,Вера | Борис,Дина',
                    'Ада,Вера,Глеб | Глеб | Борис,Дина |  | 5 2 0',
                    'Борис undefined [25,36,41] Глеб,Вера,Ада,Дина,Борис | Глеб,Вера,Ада',
                    'false true false true true false',
                    'ConstraintError',
                    '6 0 0,1']},
      {'id': 'j17-idb-tx',
       'mode': 'js',
       'title': 'Транзакции с откатом',
       'statement': 'Напишите функцию createDb(initial) → { transaction(fn) }: данные — объект «хранилище → '
                    'объект ключ → значение». transaction(fn) вызывает fn(tx) с объектом tx = { get(store, '
                    'key), put(store, key, value), delete(store, key), abort() }; пока транзакция идёт, '
                    'изменения видны только ей (внутри — читает свои записи), при нормальном завершении fn '
                    '(включая возвращённое значение) изменения применяются атомарно ко всей базе; если fn '
                    'бросила исключение или вызван tx.abort() — все изменения откатываются, исключение '
                    'пробрасывается (для abort — бросается Error с name «AbortError»). Возвращает результат '
                    'fn. Метод snapshot() — копия данных базы. Неизвестное хранилище — NotFoundError.',
       'starter': 'function createDb(initial) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const db = createDb({ accounts: { a: 100, b: 50 }, log: {} });\n'
                 'const transfer = (from, to, sum) => db.transaction((tx) => {\n'
                 '  const fb = tx.get("accounts", from), tb = tx.get("accounts", to);\n'
                 '  tx.put("accounts", from, fb - sum);\n'
                 '  if (fb - sum < 0) throw new Error("недостаточно средств");\n'
                 '  tx.put("accounts", to, tb + sum);\n'
                 '  tx.put("log", String(Object.keys(db.snapshot().log).length + 1), { from, to, sum });\n'
                 '  return fb - sum;\n'
                 '});\n'
                 'console.log(transfer("a", "b", 30), JSON.stringify(db.snapshot()));\n'
                 'try { transfer("b", "a", 500); } catch (e) { console.log(e.message, '
                 'JSON.stringify(db.snapshot().accounts)); }\n'
                 'try { db.transaction((tx) => { tx.put("accounts", "c", 1); tx.abort(); }); } catch (e) { '
                 'console.log(e.name, JSON.stringify(db.snapshot().accounts)); }\n'
                 'try { db.transaction((tx) => tx.get("nothing", "x")); } catch (e) { console.log(e.name); '
                 '}\n'
                 'console.log(db.transaction((tx) => { tx.put("accounts", "d", 7); return tx.get("accounts", '
                 '"d"); }), db.snapshot().accounts.d);\n'
                 'const s = db.snapshot(); s.accounts.a = -1; console.log(db.snapshot().accounts.a);\n'
                 'db.transaction((tx) => { tx.delete("accounts", "d"); }); '
                 'console.log(JSON.stringify(db.snapshot().accounts));\n',
       'hint': 'Работайте над копией данных и подменяйте её, только если fn завершилась без исключения.',
       'expected': ['70 {"accounts":{"a":70,"b":80},"log":{"1":{"from":"a","to":"b","sum":30}}}',
                    'недостаточно средств {"a":70,"b":80}',
                    'AbortError {"a":70,"b":80}',
                    'NotFoundError',
                    '7 7',
                    '70',
                    '{"a":70,"b":80}']},
      {'id': 'j17-migrations',
       'mode': 'js',
       'title': 'Миграции схемы по версиям',
       'statement': 'Напишите функцию runMigrations(db, migrations, targetVersion): db = { version, data } '
                    '(version — текущая; data — произвольный объект); migrations — массив { version, '
                    'up(data) → новыеДанные } (по возрастанию номера). Применяются по порядку все миграции с '
                    'version > db.version и ≤ targetVersion; каждая получает глубокую копию данных; после '
                    'успеха версия обновляется до версии этой миграции; если миграция бросает исключение — '
                    'вся операция откатывается (db остаётся в исходной версии с исходными данными), '
                    'исключение пробрасывается с добавлением в сообщение «миграция v<N>: …». Возвращает { '
                    'version, data, applied: [номера] } — не изменяя переданный db. Если targetVersion '
                    'меньше db.version — Error("Понижение версии не поддерживается").',
       'starter': 'function runMigrations(db, migrations, targetVersion) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const migs = [\n'
                 '  { version: 1, up: (d) => ({ ...d, users: [] }) },\n'
                 '  { version: 2, up: (d) => ({ ...d, users: d.users.concat({ name: "root" }) }) },\n'
                 '  { version: 3, up: (d) => ({ ...d, users: d.users.map((u) => ({ ...u, role: "admin" })) '
                 '}) },\n'
                 '  { version: 4, up: () => { throw new Error("сломано"); } },\n'
                 '  { version: 5, up: (d) => ({ ...d, five: true }) },\n'
                 '];\n'
                 'const db = Object.freeze({ version: 0, data: Object.freeze({ app: "x" }) });\n'
                 'const show = (r) => console.log(r.version, JSON.stringify(r.data), '
                 'JSON.stringify(r.applied));\n'
                 'show(runMigrations(db, migs, 3));\n'
                 'show(runMigrations({ version: 2, data: { users: [{ name: "a" }] } }, migs, 3));\n'
                 'show(runMigrations(db, migs, 0));\n'
                 'show(runMigrations({ version: 3, data: { z: 1 } }, migs, 3));\n'
                 'for (const [d, t] of [[db, 5], [{ version: 3, data: {} }, 2]]) { try { runMigrations(d, '
                 'migs, t); } catch (e) { console.log(e.message); } }\n'
                 'console.log(db.version, JSON.stringify(db.data));\n'
                 'const mutating = [{ version: 1, up: (d) => { d.touched = true; return d; } }];\n'
                 'const src = { version: 0, data: { a: 1 } }; runMigrations(src, mutating, 1); '
                 'console.log(JSON.stringify(src));\n',
       'hint': 'Копируйте данные перед каждой миграцией; применяйте только версии в диапазоне (db.version, '
               'target].',
       'expected': ['3 {"app":"x","users":[{"name":"root","role":"admin"}]} [1,2,3]',
                    '3 {"users":[{"name":"a","role":"admin"}]} [3]',
                    '0 {"app":"x"} []',
                    '3 {"z":1} []',
                    'миграция v4: сломано',
                    'Понижение версии не поддерживается',
                    '0 {"app":"x"}',
                    '{"version":0,"data":{"a":1}}']},
      {'id': 'j17-url-normalize',
       'mode': 'js',
       'title': 'Нормализация адреса',
       'statement': 'Напишите функцию normalizeUrl(str, base?) → строка: разбирает адрес (относительный — '
                    'относительно base), приводит схему и хост к нижнему регистру, убирает стандартные порты '
                    '(:80 для http, :443 для https), убирает фрагмент (#…), убирает параметры реклама '
                    '(utm_*, fbclid, gclid, yclid), сортирует остальные параметры по имени (стабильно), '
                    'убирает пустую «?», схлопывает «.» и «..» в пути, убирает завершающий «/» у пути '
                    'длиннее одного символа и приводит процентное кодирование к заглавным hex-цифрам. '
                    'Некорректный адрес — TypeError. И функцию sameResource(a, b) — совпадение '
                    'нормализованных адресов.',
       'starter': 'function normalizeUrl(str, base) {\n}\nfunction sameResource(a, b) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'for (const [s, b] of [["HTTP://Example.COM:80/a/b/../c/?z=1&a=2&utm_source=x#top"], '
                 '["https://x.ru:443/path/"], ["https://x.ru/"], ["https://x.ru:8443/a"], '
                 '["/rel/./p?b=2&a=1&a=0", "https://base.org/dir/"], ["../up", "https://base.org/a/b/"], '
                 '["https://x.ru/%d0%b0?fbclid=1&gclid=2&q=%d1%8f"], ["https://x.ru/p?"], '
                 '["https://x.ru?yclid=5"]]) console.log(normalizeUrl(s, b));\n'
                 'for (const bad of ["не адрес", "http://"]) { try { normalizeUrl(bad); } catch (e) { '
                 'console.log(e.name); } }\n'
                 'console.log(sameResource("https://X.ru/a/?b=1&a=2", '
                 '"https://x.ru/a?a=2&b=1&utm_medium=m#frag"), sameResource("https://x.ru/a", '
                 '"https://x.ru/b"));\n',
       'hint': 'Класс URL делает основную работу; добавьте фильтрацию и сортировку параметров, порты и слэш '
               'в конце.',
       'expected': ['http://example.com/a/c?a=2&z=1',
                    'https://x.ru/path',
                    'https://x.ru/',
                    'https://x.ru:8443/a',
                    'https://base.org/rel/p?a=1&a=0&b=2',
                    'https://base.org/a/up',
                    'https://x.ru/%D0%B0?q=%D1%8F',
                    'https://x.ru/p',
                    'https://x.ru/',
                    'TypeError',
                    'TypeError',
                    'true false']},
      {'id': 'j17-query-nested',
       'mode': 'js',
       'title': 'Параметры запроса со вложенностью',
       'statement': 'Напишите функции parseNested(query) и stringifyNested(obj): формат как в популярных '
                    'библиотеках: «a=1&a=2» → { a: ["1", "2"] }, «tags[]=x&tags[]=y» → { tags: ["x", "y"] }, '
                    '«user[name]=Ада&user[age]=36» → { user: { name: "Ада", age: "36" } }, '
                    '«list[0]=a&list[1]=b» → { list: ["a", "b"] } (числовые индексы дают массив), глубина '
                    'любая («a[b][c]=1»); значения — строки (декодируйте %XX и «+»); пустой запрос — {}; '
                    'ведущий «?» допустим. stringifyNested — обратная: массивы как «k[]=v» (по одному на '
                    'элемент), объекты как «k[sub]=v», числа и булевы — строками, null/undefined '
                    'пропускаются; ключи и значения кодируются encodeURIComponent (скобки в ключах — не '
                    'кодируются).',
       'starter': 'function parseNested(query) {\n}\nfunction stringifyNested(obj) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'for (const q of ["a=1&a=2", "tags[]=x&tags[]=y", '
                 '"user[name]=%D0%90%D0%B4%D0%B0&user[age]=36", "list[0]=a&list[1]=b", '
                 '"a[b][c]=1&a[b][d]=2", "?x=1+2&y=", "", "flag", "p[q][]=1&p[q][]=2"]) '
                 'console.log(JSON.stringify(q), JSON.stringify(parseNested(q)));\n'
                 'for (const o of [{ a: 1, b: "x y" }, { tags: ["a", "b"] }, { user: { name: "Ада", langs: '
                 '["ru", "en"] } }, { n: null, u: undefined, t: true, z: 0 }, {}, { a: { b: { c: [1, 2] } } '
                 '}]) console.log(stringifyNested(o));\n',
       'hint': 'Разберите ключ на путь [имя, подключ1, …]; для «[]» добавляйте в массив, для чисел и имён — '
               'по ключу.',
       'expected': ['"a=1&a=2" {"a":["1","2"]}',
                    '"tags[]=x&tags[]=y" {"tags":["x","y"]}',
                    '"user[name]=%D0%90%D0%B4%D0%B0&user[age]=36" {"user":{"name":"Ада","age":"36"}}',
                    '"list[0]=a&list[1]=b" {"list":["a","b"]}',
                    '"a[b][c]=1&a[b][d]=2" {"a":{"b":{"c":"1","d":"2"}}}',
                    '"?x=1+2&y=" {"x":"1 2","y":""}',
                    '"" {}',
                    '"flag" {"flag":""}',
                    '"p[q][]=1&p[q][]=2" {"p":{"q":["1","2"]}}',
                    'a=1&b=x%20y',
                    'tags[]=a&tags[]=b',
                    'user[name]=%D0%90%D0%B4%D0%B0&user[langs][]=ru&user[langs][]=en',
                    't=true&z=0',
                    '',
                    'a[b][c][]=1&a[b][c][]=2']},
      {'id': 'j17-history',
       'mode': 'js',
       'title': 'Модель History API',
       'statement': 'Напишите класс MyHistory(initialUrl, initialState = null): pushState(state, url) '
                    '(добавляет запись после текущей, отбрасывая «вперёд»), replaceState(state, url), '
                    'back(), forward(), go(delta) (за пределами — ничего не происходит) — переходы по '
                    'истории асинхронны в браузере, но в модели синхронны и вызывают popstate-слушателей: { '
                    'state, url } (для pushState/replaceState popstate не вызывается), свойства length, '
                    'state, url (текущая), index, и метод onPopState(fn) → отписка. relative url в pushState '
                    'разрешается относительно текущего адреса (используйте класс URL), а адрес другого '
                    'origin — Error с name «SecurityError».',
       'starter': 'class MyHistory {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const h = new MyHistory("https://app.ru/", { page: "home" });\n'
                 'const pops = [];\n'
                 'const off = h.onPopState((e) => pops.push(`${e.url.replace("https://app.ru", '
                 '"")}:${JSON.stringify(e.state)}`));\n'
                 'h.pushState({ page: "list" }, "/items"); h.pushState({ page: "item", id: 7 }, '
                 '"/items/7?tab=1"); h.pushState(null, "../8");\n'
                 'console.log(h.length, h.index, h.url, JSON.stringify(h.state), pops.length);\n'
                 'h.back(); h.back(); console.log(h.index, h.url, JSON.stringify(h.state), pops.join(" | '
                 '")); pops.length = 0;\n'
                 'h.pushState({ page: "new" }, "/items/new"); console.log(h.length, h.url);\n'
                 'h.forward(); console.log(h.index, pops.length);\n'
                 'h.replaceState({ page: "replaced" }, "/items/NEW"); console.log(h.length, h.url, '
                 'JSON.stringify(h.state));\n'
                 'h.go(-5); h.go(0); console.log(h.index, pops.length);\n'
                 'h.go(-2); console.log(h.index, pops.join(" | ")); pops.length = 0;\n'
                 'off(); h.forward(); console.log(h.index, pops.length);\n'
                 'try { h.pushState(null, "https://evil.com/x"); } catch (e) { console.log(e.name, '
                 'h.length); }\n'
                 'h.pushState(5); console.log(h.url, h.state);\n',
       'hint': 'Массив записей и текущий индекс; pushState обрезает «вперёд»; popstate — только при '
               'go/back/forward.',
       'expected': ['4 3 https://app.ru/8 null 0',
                    '1 https://app.ru/items {"page":"list"} /items/7?tab=1:{"page":"item","id":7} | '
                    '/items:{"page":"list"}',
                    '3 https://app.ru/items/new',
                    '2 0',
                    '3 https://app.ru/items/NEW {"page":"replaced"}',
                    '2 0',
                    '0 /:{"page":"home"}',
                    '1 0',
                    'SecurityError 3',
                    'https://app.ru/items 5']},
      {'id': 'j17-router-match',
       'mode': 'js',
       'title': 'Сопоставление маршрутов',
       'statement': 'Напишите функцию createRouter(routes): routes — массив { path, name }; шаблон пути: '
                    'статические сегменты, «:param», «:param?» (необязательный, только в конце), «*» '
                    "(остаток пути в params['*']), «:id(\\\\d+)» (параметр с регулярным ограничением). "
                    'Возвращает функцию match(url) → { name, params, query } или null: url — строка вида '
                    '«/users/42?tab=info#x» (фрагмент отбрасывается; query разбирается в объект строк; '
                    'повтор ключей — массив); завершающий «/» игнорируется; регистр путей важен; params '
                    'декодируются; выигрывает самый специфичный маршрут: больше статических сегментов, при '
                    'равенстве — раньше в списке (а не просто порядок объявления: «/users/new» побеждает '
                    '«/users/:id»).',
       'starter': 'function createRouter(routes) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const canon = (x) => (Array.isArray(x) ? x.map(canon) : x && typeof x === "object" ? '
                 'Object.fromEntries(Object.keys(x).sort().map((k) => [k, canon(x[k])])) : x);\n'
                 'const match = createRouter([\n'
                 '  { path: "/", name: "home" }, { path: "/users", name: "users" }, { path: "/users/new", '
                 'name: "user-new" }, { path: "/users/:id(\\\\d+)", name: "user" }, { path: "/users/:name", '
                 'name: "user-by-name" },\n'
                 '  { path: "/users/:id/posts/:post?", name: "posts" }, { path: "/files/*", name: "files" }, '
                 '{ path: "/Case", name: "case" },\n'
                 ']);\n'
                 'for (const u of ["/", "/users", "/users/", "/users/new", "/users/42", "/users/ada", '
                 '"/users/42/posts", "/users/42/posts/7?x=1&x=2#h", "/files/a/b/c.txt", "/files/", '
                 '"/users/%D0%90%D0%B4%D0%B0", "/case", "/Case", "/nope", "/users/42/extra/zzz", '
                 '"/users?tab=info&q=a+b"]) { const m = match(u); console.log(u, m ? '
                 'JSON.stringify(canon(m)) : null); }\n',
       'hint': 'Скомпилируйте шаблоны в сегменты; найдите все подходящие и выберите по числу статических '
               'сегментов.',
       'expected': ['/ {"name":"home","params":{},"query":{}}',
                    '/users {"name":"users","params":{},"query":{}}',
                    '/users/ {"name":"users","params":{},"query":{}}',
                    '/users/new {"name":"user-new","params":{},"query":{}}',
                    '/users/42 {"name":"user","params":{"id":"42"},"query":{}}',
                    '/users/ada {"name":"user-by-name","params":{"name":"ada"},"query":{}}',
                    '/users/42/posts {"name":"posts","params":{"id":"42"},"query":{}}',
                    '/users/42/posts/7?x=1&x=2#h '
                    '{"name":"posts","params":{"id":"42","post":"7"},"query":{"x":["1","2"]}}',
                    '/files/a/b/c.txt {"name":"files","params":{"*":"a/b/c.txt"},"query":{}}',
                    '/files/ {"name":"files","params":{"*":""},"query":{}}',
                    '/users/%D0%90%D0%B4%D0%B0 {"name":"user-by-name","params":{"name":"Ада"},"query":{}}',
                    '/case null',
                    '/Case {"name":"case","params":{},"query":{}}',
                    '/nope null',
                    '/users/42/extra/zzz null',
                    '/users?tab=info&q=a+b {"name":"users","params":{},"query":{"q":"a b","tab":"info"}}']},
      {'id': 'j17-spa-link',
       'mode': 'js',
       'title': 'Перехватывать ли клик по ссылке',
       'statement': 'Напишите функцию shouldIntercept(event, link, location): event = { button, ctrlKey, '
                    'metaKey, shiftKey, altKey, defaultPrevented }, link = { href (абсолютный адрес), '
                    'target?, download?, rel?, hasAttribute? }, location = { origin, pathname, search }. '
                    'Возвращает true, если роутер должен перехватить клик (вызвать pushState): левая кнопка '
                    '(button 0), без модификаторов и без defaultPrevented; link.target пуст или «_self»; нет '
                    'download; rel не содержит «external»; origin ссылки совпадает с location.origin; ссылка '
                    'не ведёт на тот же адрес с одним лишь фрагментом (тот же pathname+search и непустой '
                    '#hash — браузер сам прокрутит к якорю: false); протоколы mailto:, tel:, javascript: и '
                    'не-http(s) — false. И функцию toPath(href, location) → «pathname + search + hash» для '
                    'pushState.',
       'starter': 'function shouldIntercept(event, link, location) {\n}\nfunction toPath(href) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const loc = { origin: "https://app.ru", pathname: "/docs", search: "?v=1" };\n'
                 'const ev = (extra = {}) => ({ button: 0, ctrlKey: false, metaKey: false, shiftKey: false, '
                 'altKey: false, defaultPrevented: false, ...extra });\n'
                 'const cases = [\n'
                 '  ["обычная", ev(), { href: "https://app.ru/about" }], ["ctrl", ev({ ctrlKey: true }), { '
                 'href: "https://app.ru/about" }], ["meta", ev({ metaKey: true }), { href: '
                 '"https://app.ru/about" }], ["средняя", ev({ button: 1 }), { href: "https://app.ru/about" '
                 '}],\n'
                 '  ["prevented", ev({ defaultPrevented: true }), { href: "https://app.ru/about" }], '
                 '["_blank", ev(), { href: "https://app.ru/about", target: "_blank" }], ["_self", ev(), { '
                 'href: "https://app.ru/about", target: "_self" }],\n'
                 '  ["download", ev(), { href: "https://app.ru/f.zip", download: "" }], ["external", ev(), { '
                 'href: "https://app.ru/x", rel: "noopener external" }], ["чужой", ev(), { href: '
                 '"https://other.org/x" }], ["http↔https", ev(), { href: "http://app.ru/x" }],\n'
                 '  ["якорь", ev(), { href: "https://app.ru/docs?v=1#part" }], ["тот же без якоря", ev(), { '
                 'href: "https://app.ru/docs?v=1" }], ["якорь на другой", ev(), { href: '
                 '"https://app.ru/other#part" }], ["другой query", ev(), { href: '
                 '"https://app.ru/docs?v=2#part" }],\n'
                 '  ["mailto", ev(), { href: "mailto:a@b.ru" }], ["tel", ev(), { href: "tel:+7999" }], '
                 '["javascript", ev(), { href: "javascript:void(0)" }], ["битая", ev(), { href: "не адрес" '
                 '}],\n'
                 '];\n'
                 'for (const [n, e, l] of cases) console.log(n.padEnd(18), shouldIntercept(e, l, loc));\n'
                 'console.log(toPath("https://app.ru/a/b?x=1#h"), toPath("https://app.ru"), '
                 'toPath("https://app.ru/?q=ж"));\n',
       'hint': 'Серия независимых проверок; для якоря сравните pathname и search с текущими.',
       'expected': ['обычная            true',
                    'ctrl               false',
                    'meta               false',
                    'средняя            false',
                    'prevented          false',
                    '_blank             false',
                    '_self              true',
                    'download           false',
                    'external           false',
                    'чужой              false',
                    'http↔https         false',
                    'якорь              false',
                    'тот же без якоря   true',
                    'якорь на другой    true',
                    'другой query       true',
                    'mailto             false',
                    'tel                false',
                    'javascript         false',
                    'битая              false',
                    '/a/b?x=1#h / /?q=%D0%B6']},
      {'id': 'j17-scroll-restore',
       'mode': 'js',
       'title': 'Восстановление прокрутки',
       'statement': 'Напишите функцию createScrollManager(history): history — объект с массивом записей и '
                    'текущим индексом (интерфейс: getCurrentKey() → уникальный ключ текущей записи, '
                    'определяемый снаружи). Возвращает { save(scrollY) (запоминает прокрутку под текущим '
                    'ключом), onNavigate(key, kind, hash) → куда прокрутить: kind "push" — 0 (или якорь, '
                    'если hash непуст — верните { anchor: hash }); kind "pop" (назад/вперёд) — сохранённая '
                    'позиция этого key или 0; kind "replace" — не менять (null) }, clear(key) }. Результат — '
                    'число (прокрутить к Y), { anchor } или null. Ключи не должны перетираться при повторном '
                    'посещении одного адреса в разных записях истории.',
       'starter': 'function createScrollManager(history) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'let current = "k1";\n'
                 'const mgr = createScrollManager({ getCurrentKey: () => current });\n'
                 'mgr.save(500); current = "k2"; mgr.save(1200); current = "k3"; mgr.save(0);\n'
                 'const show = (...a) => console.log(JSON.stringify(mgr.onNavigate(...a)));\n'
                 'show("k4", "push", ""); show("k4", "push", "#faq"); show("k2", "pop"); show("k1", "pop"); '
                 'show("k3", "pop"); show("kX", "pop"); show("k4", "replace", "");\n'
                 'mgr.clear("k2"); show("k2", "pop");\n'
                 'current = "k1"; mgr.save(40); show("k1", "pop");\n'
                 'current = "k5"; mgr.save(77); current = "k6"; mgr.save(88); show("k5", "pop"); show("k6", '
                 '"pop");\n',
       'hint': 'Map «ключ записи → прокрутка»; для push возвращайте 0 или якорь, для pop — сохранённое '
               'значение.',
       'expected': ['0', '{"anchor":"#faq"}', '1200', '500', '0', '0', 'null', '0', '40', '77', '88']},
      {'id': 'j17-quota-store',
       'mode': 'js',
       'title': 'Квота и вытеснение (LRU)',
       'statement': 'Напишите класс QuotaStore(quota): как хранилище с лимитом (суммарный размер значений ≤ '
                    'quota; размер значения — его длина в символах): set(key, value, { persist = false }) — '
                    'записывает; если места не хватает, вытесняются самые давно использованные (по get/set) '
                    'НЕ-persist записи, пока не освободится место; если даже после вытеснения всех '
                    'не-persist места нет — бросается ошибка с name «QuotaExceededError» и ничего не '
                    'меняется (вытеснение откатывается); get(key) → значение или undefined и обновляет '
                    '«давность»; delete(key); keys() → ключи от самого давнего к самому свежему; used() → '
                    'занятый размер; estimate() → { usage, quota }. Запись, превышающая quota сама по себе, '
                    '— QuotaExceededError.',
       'starter': 'class QuotaStore {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'const err = (f) => { try { f(); return "ok"; } catch (e) { return e.name; } };\n'
                 'const s = new QuotaStore(10);\n'
                 's.set("a", "1234"); s.set("b", "1234"); console.log(s.keys().join(), s.used());\n'
                 's.get("a"); s.set("c", "123"); console.log(s.keys().join(), s.used());\n'
                 's.set("d", "123456"); console.log(s.keys().join(), s.used(), '
                 'JSON.stringify(s.estimate()));\n'
                 'console.log(err(() => s.set("huge", "x".repeat(11))), s.keys().join());\n'
                 'const p = new QuotaStore(10); p.set("keep", "123456", { persist: true }); p.set("tmp", '
                 '"123");\n'
                 'console.log(err(() => p.set("more", "12345")), p.keys().join(), p.used());\n'
                 'console.log(err(() => p.set("tmp2", "1234")), p.keys().join());\n'
                 'p.set("keep", "12", { persist: true }); console.log(p.used(), p.get("keep"), '
                 'p.get("zzz"));\n'
                 'p.delete("keep"); console.log(p.keys().join(), p.used());\n'
                 'const q = new QuotaStore(5); q.set("x", "12345"); q.set("x", "123"); console.log(q.used(), '
                 'q.keys().join());\n',
       'hint': 'Map сохраняет порядок вставки: «освежить» запись — удалить и вставить заново; вытеснение — '
               'от начала.',
       'expected': ['a,b 8',
                    'a,c 7',
                    'c,d 9 {"usage":9,"quota":10}',
                    'QuotaExceededError c,d',
                    'QuotaExceededError keep,tmp 9',
                    'ok keep,tmp2',
                    '6 12 undefined',
                    'tmp2 4',
                    '3 x']},
      {'id': 'j17-phone-mask',
       'mode': 'js',
       'title': 'Маска телефона',
       'statement': 'Напишите функции maskPhone(input) → строка вида «+7 (999) 123-45-67» и '
                    'unmaskPhone(masked) → «79991234567». Правила: берутся только цифры; если первая цифра 8 '
                    'или 7 — это код страны (8 заменяется на 7); если первая цифра другая (и ввод не пуст) — '
                    'считается, что код страны 7 уже подразумевается и цифра относится к номеру; цифр '
                    'максимум 11, лишние отбрасываются; маска строится постепенно по мере ввода: «7» → «+7», '
                    '«79» → «+7 (9», «79991» → «+7 (999) 1», «799912» → «+7 (999) 12», после 7-й цифры '
                    'добавляется «-», после 9-й — «-»; пустой ввод → «». Скобка закрывается только когда '
                    'есть хотя бы одна цифра после кода оператора.',
       'starter': 'function maskPhone(input) {\n}\nfunction unmaskPhone(masked) {\n}\n',
       'driver': '/*__DRIVER__*/\n'
                 'for (const s of ["", "abc", "7", "8", "9", "79", "79991", "799912", "7999123", "79991234", '
                 '"799912345", "7999123456", "79991234567", "799912345678999", "8 (999) 123-45-67", "+7 999 '
                 '123 45 67", "999 123", "+7 (99"]) console.log(JSON.stringify(s), '
                 'JSON.stringify(maskPhone(s)), JSON.stringify(unmaskPhone(maskPhone(s))));\n',
       'hint': 'Сначала нормализуйте цифры (код страны, максимум 11), затем собирайте маску по длине.',
       'expected': ['"" "" ""',
                    '"abc" "" ""',
                    '"7" "+7" "7"',
                    '"8" "+7" "7"',
                    '"9" "+7 (9" "79"',
                    '"79" "+7 (9" "79"',
                    '"79991" "+7 (999) 1" "79991"',
                    '"799912" "+7 (999) 12" "799912"',
                    '"7999123" "+7 (999) 123" "7999123"',
                    '"79991234" "+7 (999) 123-4" "79991234"',
                    '"799912345" "+7 (999) 123-45" "799912345"',
                    '"7999123456" "+7 (999) 123-45-6" "7999123456"',
                    '"79991234567" "+7 (999) 123-45-67" "79991234567"',
                    '"799912345678999" "+7 (999) 123-45-67" "79991234567"',
                    '"8 (999) 123-45-67" "+7 (999) 123-45-67" "79991234567"',
                    '"+7 999 123 45 67" "+7 (999) 123-45-67" "79991234567"',
                    '"999 123" "+7 (999) 123" "7999123"',
                    '"+7 (99" "+7 (99" "799"']}]}
