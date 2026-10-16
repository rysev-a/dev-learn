"""Задачи книги «Современный Frontend», глава 4 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {4: [{'id': 'j4-greet',
      'mode': 'js',
      'title': 'Шаблонная строка: приветствие',
      'statement': 'Напишите функцию greet(name): она возвращает строку «Привет, <name>!» (например, '
                   '«Привет, мир!»). Используйте шаблонную строку в обратных кавычках.',
      'starter': 'function greet(name) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(greet("мир"));\n'
                'console.log(greet("Ада"));\n'
                'console.log(__count("`") >= 2 ? "шаблон есть" : "нет шаблона");\n',
      'hint': 'return `Привет, ${name}!`;',
      'expected': ['Привет, мир!', 'Привет, Ада!', 'шаблон есть']},
     {'id': 'j4-run-log',
      'mode': 'js',
      'title': 'console.log: три строки',
      'statement': 'Напишите функцию run(): она печатает через console.log три строки — «JavaScript», число '
                   '42 и значение true — каждую отдельным вызовом.',
      'starter': 'function run() {\n}\n',
      'driver': '/*__DRIVER__*/\nrun();\n',
      'hint': 'console.log("JavaScript"); console.log(42); console.log(true);',
      'expected': ['JavaScript', '42', 'true']},
     {'id': 'j4-type-of',
      'mode': 'js',
      'title': 'Тип значения: null и массив',
      'statement': 'Напишите функцию typeName(v): она возвращает строку с именем типа, как typeof, но для '
                   'null — «null», а для массива — «array».',
      'starter': 'function typeName(v) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const v of [1, "a", true, null, undefined, [], {}, 10n, () => 1, Symbol("s")]) '
                'console.log(typeName(v));\n',
      'hint': 'Сначала проверьте null и Array.isArray, затем верните typeof v.',
      'expected': ['number',
                   'string',
                   'boolean',
                   'null',
                   'undefined',
                   'array',
                   'object',
                   'bigint',
                   'function',
                   'symbol']},
     {'id': 'j4-count-falsy',
      'mode': 'js',
      'title': 'Сколько ложных значений',
      'statement': 'Напишите функцию countFalsy(arr): она возвращает, сколько элементов массива при проверке '
                   'в условии считаются ложными.',
      'starter': 'function countFalsy(arr) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(countFalsy([0, 1, "", "0", null, undefined, NaN, [], {}, false]));\n'
                'console.log(countFalsy([]));\n'
                'console.log(countFalsy([1, 2, 3]));\n'
                'console.log(countFalsy([0, -0, 0n, "", false]));\n',
      'hint': 'if (!x) n++ — для 0n тоже верно: ложно и оно.',
      'expected': ['6', '0', '0', '5']},
     {'id': 'j4-default',
      'mode': 'js',
      'title': 'Значение по умолчанию: только для null и undefined',
      'statement': 'Напишите функцию orDefault(x, d): она возвращает d, только если x равен null или '
                   'undefined; для 0, пустой строки и false возвращается сам x. Операторы || и && '
                   'использовать нельзя.',
      'starter': 'function orDefault(x, d) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'for (const x of [0, "", false, null, undefined, "a"]) '
                'console.log(JSON.stringify(orDefault(x, 7)) ?? "undefined");\n'
                'console.log(__count("|" + "|") + __count("&" + "&"));\n',
      'hint': 'Оператор ?? выбирает правую часть только для null и undefined.',
      'expected': ['0', '""', 'false', '7', '7', '"a"', '0']},
     {'id': 'j4-safe-name',
      'mode': 'js',
      'title': 'Безопасный путь: user?.profile?.name',
      'statement': 'Напишите функцию userName(user): она возвращает user.profile.name, а если на пути '
                   'встретилось null или undefined — строку «аноним». Условных операторов if и тернарного ? '
                   ': не используйте, достаточно ?. и ??.',
      'starter': 'function userName(user) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(userName({ profile: { name: "Ада" } }));\n'
                'console.log(userName({ profile: null }));\n'
                'console.log(userName(undefined));\n'
                'console.log(userName({ profile: { name: "" } }) === "" ? "пустое имя сохранено" : '
                '"потеряно");\n'
                'console.log(__count("if" + " (") + __count("if" + "("));\n',
      'hint': 'return user?.profile?.name ?? "аноним";',
      'expected': ['Ада', 'аноним', 'аноним', 'пустое имя сохранено', '0']},
     {'id': 'j4-money',
      'mode': 'js',
      'title': 'Деньги без хвоста 0.30000000000000004',
      'statement': 'Напишите функцию addMoney(a, b): она складывает две суммы в рублях с копейками и '
                   'возвращает результат, округлённый до копеек (двух знаков после запятой), чтобы 0.1 + 0.2 '
                   'давало ровно 0.3.',
      'starter': 'function addMoney(a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(addMoney(0.1, 0.2));\n'
                'console.log(addMoney(1.15, 2.35));\n'
                'console.log(addMoney(10, 0.07));\n'
                'console.log(addMoney(0.1, 0.2) === 0.3);\n',
      'hint': 'Math.round((a + b) * 100) / 100',
      'expected': ['0.3', '3.5', '10.07', 'true']},
     {'id': 'j4-is-safe',
      'mode': 'js',
      'title': 'Безопасное целое',
      'statement': 'Напишите функцию isSafe(n): она возвращает true, если n — целое число, по модулю не '
                   'превышающее 2 в 53-й степени минус 1 (Number.MAX_SAFE_INTEGER). Number.isSafeInteger '
                   'использовать нельзя.',
      'starter': 'function isSafe(n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'for (const n of [0, 5, -5, 2 ** 53 - 1, 2 ** 53, -(2 ** 53), 1.5, NaN, Infinity, "7"]) '
                'console.log(isSafe(n));\n'
                'console.log(__count("isSafe" + "Integer"));\n',
      'hint': 'Number.isInteger(n) и Math.abs(n) <= 2 ** 53 - 1; не забудьте проверить тип.',
      'expected': ['true',
                   'true',
                   'true',
                   'true',
                   'false',
                   'false',
                   'false',
                   'false',
                   'false',
                   'false',
                   '0']},
     {'id': 'j4-same-value',
      'mode': 'js',
      'title': 'Равенство с учётом NaN',
      'statement': 'Напишите функцию sameValue(a, b): она возвращает true, если a === b или если оба '
                   'значения — NaN. Object.is использовать нельзя.',
      'starter': 'function sameValue(a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(sameValue(NaN, NaN));\n'
                'console.log(sameValue(1, 1));\n'
                'console.log(sameValue(0, "0"));\n'
                'console.log(sameValue(null, undefined));\n'
                'console.log(sameValue("a", "a"));\n'
                'console.log(sameValue(NaN, 1));\n'
                'console.log(__count("Obje" + "ct.is"));\n',
      'hint': 'NaN — единственное значение, не равное себе: x !== x.',
      'expected': ['true', 'true', 'false', 'false', 'true', 'false', '0']},
     {'id': 'j4-factorial',
      'mode': 'js',
      'title': 'Факториал на BigInt',
      'statement': 'Напишите функцию factorial(n): n — обычное целое число от 0 до 30; функция возвращает n! '
                   'в виде строки, точной для любых n (используйте BigInt).',
      'starter': 'function factorial(n) {\n}\n',
      'driver': '/*__DRIVER__*/\nfor (const n of [0, 1, 5, 20, 25, 30]) console.log(factorial(n));\n',
      'hint': 'Начните с 1n, умножайте на BigInt(i); результат — String(r).',
      'expected': ['1',
                   '1',
                   '120',
                   '2432902008176640000',
                   '15511210043330985984000000',
                   '265252859812191058636308480000000']},
     {'id': 'j4-char-count',
      'mode': 'js',
      'title': 'Сколько символов в строке',
      'statement': 'Напишите функцию charCount(s): она возвращает число настоящих символов строки (эмодзи '
                   'считается за один), а не единиц UTF-16. Цикл for-of или оператор расширения помогут.',
      'starter': 'function charCount(s) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const s of ["", "abc", "привет", "😀", "a😀b", "👍👍👍"]) console.log(charCount(s));\n',
      'hint': 'for (const ch of s) n++;',
      'expected': ['0', '3', '6', '1', '3', '3']},
     {'id': 'j4-reverse',
      'mode': 'js',
      'title': 'Разворот строки по символам',
      'statement': 'Напишите функцию reverse(s): она возвращает строку, в которой символы идут в обратном '
                   'порядке; эмодзи должны остаться целыми.',
      'starter': 'function reverse(s) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const s of ["", "abc", "привет", "a😀b", "👍x"]) console.log(reverse(s));\n',
      'hint': '[...s].reverse().join("")',
      'expected': ['cba', 'тевирп', 'b😀a', 'x👍']},
     {'id': 'j4-palindrome',
      'mode': 'js',
      'title': 'Палиндром',
      'statement': 'Напишите функцию isPalindrome(s): она возвращает true, если строка читается одинаково в '
                   'обе стороны без учёта регистра, пробелов и знаков препинания («А роза упала на лапу '
                   'Азора»).',
      'starter': 'function isPalindrome(s) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const s of ["А роза упала на лапу Азора", "level", "Hello", "", "Был ли Лиль бы?", '
                '"12321", "ab"]) console.log(isPalindrome(s));\n',
      'hint': 'toLowerCase, затем replace(/[^\\p{L}\\p{N}]/gu, "") и сравнение с развёрнутой строкой.',
      'expected': ['true', 'true', 'false', 'true', 'false', 'true', 'false']},
     {'id': 'j4-title-case',
      'mode': 'js',
      'title': 'Каждое слово с заглавной',
      'statement': 'Напишите функцию titleCase(s): слова разделены одним пробелом; у каждого слова первая '
                   'буква становится заглавной, остальные — строчными.',
      'starter': 'function titleCase(s) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(titleCase("hello world"));\n'
                'console.log(titleCase("ИВАН иванов"));\n'
                'console.log(titleCase("a"));\n'
                'console.log(titleCase(""));\n'
                'console.log(titleCase("jAVA sCRIPT is fun"));\n',
      'hint': 'split(" "), у каждого слова slice(0, 1).toUpperCase() + slice(1).toLowerCase(), затем join.',
      'expected': ['Hello World', 'Иван Иванов', 'A', '', 'Java Script Is Fun']},
     {'id': 'j4-vowels',
      'mode': 'js',
      'title': 'Гласные в русском тексте',
      'statement': 'Напишите функцию countVowels(s): она считает русские гласные буквы (а, е, ё, и, о, у, ы, '
                   'э, ю, я) в любом регистре.',
      'starter': 'function countVowels(s) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const s of ["Привет, мир!", "", "ААаа", "Шпаргалка", "rhythm", "Ёлка и яблоко"]) '
                'console.log(countVowels(s));\n',
      'hint': '"аеёиоуыэюя".includes(ch) для каждого символа строки в нижнем регистре.',
      'expected': ['3', '0', '4', '3', '0', '6']},
     {'id': 'j4-template-user',
      'mode': 'js',
      'title': 'Шаблон: имя и возраст',
      'statement': 'Напишите функцию formatUser(name, age): она возвращает строку вида «Ада (36)». Склеивать '
                   'оператором + нельзя — используйте шаблонную строку.',
      'starter': 'function formatUser(name, age) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(formatUser("Ада", 36));\n'
                'console.log(formatUser("Линус", 55));\n'
                'console.log(__count("`") >= 2 ? "шаблон" : "нет шаблона");\n'
                'console.log(__count(" + "));\n',
      'hint': 'return `${name} (${age})`;',
      'expected': ['Ада (36)', 'Линус (55)', 'шаблон', '0']},
     {'id': 'j4-truncate',
      'mode': 'js',
      'title': 'Обрезка строки с многоточием',
      'statement': 'Напишите функцию truncate(s, n): если длина s не больше n, вернуть s; иначе вернуть '
                   'первые n - 1 символов и «…». Длина результата всегда не больше n.',
      'starter': 'function truncate(s, n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(truncate("JavaScript", 20));\n'
                'console.log(truncate("JavaScript", 10));\n'
                'console.log(truncate("JavaScript", 5));\n'
                'console.log(truncate("", 3));\n'
                'console.log(truncate("привет мир", 7));\n',
      'hint': 's.length <= n ? s : s.slice(0, n - 1) + "…"',
      'expected': ['JavaScript', 'JavaScript', 'Java…', '', 'привет…']},
     {'id': 'j4-fix-const',
      'mode': 'js',
      'title': 'Исправьте: const и сумма',
      'statement': 'Функция sumAll должна возвращать сумму чисел массива, но падает с TypeError: Assignment '
                   'to constant variable. Исправьте объявление.',
      'starter': 'function sumAll(arr) {\n'
                 '  const total = 0;\n'
                 '  for (const x of arr) {\n'
                 '    total += x;\n'
                 '  }\n'
                 '  return total;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(sumAll([1, 2, 3]));\n'
                'console.log(sumAll([]));\n'
                'console.log(sumAll([10, -4]));\n',
      'hint': 'Накапливаемое значение меняется, поэтому объявите его через let.',
      'expected': ['6', '0', '6']},
     {'id': 'j4-fix-for-in',
      'mode': 'js',
      'title': 'Исправьте: for…in вместо for…of',
      'statement': 'Функция sumAll2 должна суммировать значения массива, но вместо этого склеивает его '
                   'индексы в строку. Исправьте цикл.',
      'starter': 'function sumAll2(arr) {\n'
                 '  let total = 0;\n'
                 '  for (const x in arr) {\n'
                 '    total += x;\n'
                 '  }\n'
                 '  return total;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(sumAll2([5, 6, 7]));\n'
                'console.log(sumAll2([]));\n'
                'console.log(sumAll2([1]));\n',
      'hint': 'for…in перебирает имена свойств (строки «0», «1»…), а нужны значения — for…of.',
      'expected': ['18', '0', '1']},
     {'id': 'j4-fizzbuzz',
      'mode': 'js',
      'title': 'FizzBuzz',
      'statement': 'Напишите функцию fizzBuzz(n): она возвращает массив из n строк для чисел от 1 до n: '
                   '«FizzBuzz» для кратных 15, «Fizz» для кратных 3, «Buzz» для кратных 5, иначе само число '
                   'в виде строки.',
      'starter': 'function fizzBuzz(n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(fizzBuzz(15)));\n'
                'console.log(JSON.stringify(fizzBuzz(0)));\n'
                'console.log(JSON.stringify(fizzBuzz(5)));\n',
      'hint': 'Сначала проверьте кратность 15, потом 3 и 5.',
      'expected': ['["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]',
                   '[]',
                   '["1","2","Fizz","4","Buzz"]']},
     {'id': 'j4-range',
      'mode': 'js',
      'title': 'Диапазон чисел',
      'statement': 'Напишите функцию range(a, b, step = 1): она возвращает массив чисел от a (включительно) '
                   'до b (не включая) с шагом step; при step > 0 это возрастающая последовательность, при '
                   'step < 0 — убывающая. При step === 0 бросьте RangeError.',
      'starter': 'function range(a, b, step = 1) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(range(0, 5)));\n'
                'console.log(JSON.stringify(range(2, 10, 3)));\n'
                'console.log(JSON.stringify(range(5, 0, -2)));\n'
                'console.log(JSON.stringify(range(3, 3)));\n'
                'try { range(0, 5, 0); } catch (e) { console.log(e.name); }\n',
      'hint': 'Два цикла: при step > 0 условие i < b, при step < 0 условие i > b.',
      'expected': ['[0,1,2,3,4]', '[2,5,8]', '[5,3,1]', '[]', 'RangeError']},
     {'id': 'j4-sum-digits',
      'mode': 'js',
      'title': 'Сумма цифр',
      'statement': 'Напишите функцию sumDigits(n): n — неотрицательное целое число; функция возвращает сумму '
                   'его десятичных цифр. Строки и массивы использовать нельзя — только арифметику.',
      'starter': 'function sumDigits(n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'for (const n of [0, 7, 123, 99999, 1000, 2 ** 31]) console.log(sumDigits(n));\n'
                'console.log(__count("String" + "(") + __count("toStr" + "ing") + __count("[" + "...") + '
                '__count("`"));\n',
      'hint': 'n % 10 — последняя цифра, Math.floor(n / 10) — число без неё.',
      'expected': ['0', '7', '6', '45', '1', '47', '0']},
     {'id': 'j4-clone',
      'mode': 'js',
      'title': 'Копия объекта',
      'statement': 'Напишите функцию cloneUser(user): она возвращает новый объект с теми же полями, так что '
                   'изменение копии не затрагивает оригинал.',
      'starter': 'function cloneUser(user) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const u = { name: "Ада", age: 36 };\n'
                'const c = cloneUser(u);\n'
                'c.age = 40;\n'
                'c.extra = true;\n'
                'console.log(JSON.stringify(u));\n'
                'console.log(JSON.stringify(c));\n'
                'console.log(u === c);\n',
      'hint': 'Оператор расширения: { ...user }',
      'expected': ['{"name":"Ада","age":36}', '{"name":"Ада","age":40,"extra":true}', 'false']},
     {'id': 'j4-push-in-place',
      'mode': 'js',
      'title': 'Изменить на месте или вернуть новое',
      'statement': 'Напишите две функции. pushIn(list, x) добавляет x в конец переданного массива (изменяет '
                   'его) и ничего не возвращает. withItem(list, x) возвращает новый массив с добавленным x, '
                   'не меняя исходный.',
      'starter': 'function pushIn(list, x) {\n}\n\nfunction withItem(list, x) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const a = [1, 2];\n'
                'console.log(pushIn(a, 3));\n'
                'console.log(JSON.stringify(a));\n'
                'const b = withItem(a, 4);\n'
                'console.log(JSON.stringify(a));\n'
                'console.log(JSON.stringify(b));\n'
                'console.log(a === b);\n',
      'hint': 'push меняет массив, [...list, x] создаёт новый.',
      'expected': ['undefined', '[1,2,3]', '[1,2,3]', '[1,2,3,4]', 'false']},
     {'id': 'j4-safe-parse',
      'mode': 'js',
      'title': 'Безопасный разбор JSON',
      'statement': 'Напишите функцию safeParse(text): она возвращает { ok: true, value } для корректного '
                   'JSON и { ok: false, error: e.name } — если разбор бросил исключение.',
      'starter': 'function safeParse(text) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(safeParse(\'{"a":1}\')));\n'
                'console.log(JSON.stringify(safeParse("[1,2]")));\n'
                'console.log(JSON.stringify(safeParse("{")));\n'
                'console.log(JSON.stringify(safeParse("")));\n'
                'console.log(JSON.stringify(safeParse("null")));\n',
      'hint': 'try { … JSON.parse … } catch (e) { … e.name … }',
      'expected': ['{"ok":true,"value":{"a":1}}',
                   '{"ok":true,"value":[1,2]}',
                   '{"ok":false,"error":"SyntaxError"}',
                   '{"ok":false,"error":"SyntaxError"}',
                   '{"ok":true,"value":null}']},
     {'id': 'j4-divide',
      'mode': 'js',
      'title': 'Своё исключение: деление на ноль',
      'statement': 'Напишите функцию divide(a, b): она возвращает a / b, а при b === 0 бросает RangeError с '
                   'сообщением «Деление на ноль».',
      'starter': 'function divide(a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(divide(10, 4));\n'
                'console.log(divide(-9, 3));\n'
                'try {\n'
                '  divide(1, 0);\n'
                '} catch (e) {\n'
                '  console.log(e.name + ": " + e.message);\n'
                '  console.log(e instanceof RangeError);\n'
                '}\n',
      'hint': 'throw new RangeError("Деление на ноль");',
      'expected': ['2.5', '-3', 'RangeError: Деление на ноль', 'true']},
     {'id': 'j4-error-name',
      'mode': 'js',
      'title': 'Имя ошибки',
      'statement': 'Напишите функцию errorName(fn): она вызывает fn без аргументов; если fn бросила '
                   'исключение — возвращает его имя (поле name), иначе — строку «ok».',
      'starter': 'function errorName(fn) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(errorName(() => nope));\n'
                'console.log(errorName(() => null.x));\n'
                'console.log(errorName(() => new Array(-1)));\n'
                'console.log(errorName(() => JSON.parse("{")));\n'
                'console.log(errorName(() => 1 + 1));\n'
                'console.log(errorName(() => { throw new Error("x"); }));\n',
      'hint': 'try { fn(); return "ok"; } catch (e) { return e.name; }',
      'expected': ['ReferenceError', 'TypeError', 'RangeError', 'SyntaxError', 'ok', 'Error']},
     {'id': 'j4-type-counts',
      'mode': 'js',
      'title': 'Подсчёт типов',
      'statement': 'Напишите функцию typeCounts(arr): она возвращает объект, где ключ — результат typeof для '
                   'элемента, а значение — сколько таких элементов в массиве.',
      'starter': 'function typeCounts(arr) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const show = (o) => '
                'console.log(JSON.stringify(Object.fromEntries(Object.entries(o).sort())));\n'
                'show(typeCounts([1, "a", 2, null, undefined, true, "b", {}, []]));\n'
                'show(typeCounts([]));\n'
                'show(typeCounts([10n, 1n, 1]));\n',
      'hint': 'out[t] = (out[t] ?? 0) + 1',
      'expected': ['{"boolean":1,"number":2,"object":3,"string":2,"undefined":1}',
                   '{}',
                   '{"bigint":2,"number":1}']},
     {'id': 'j4-first-defined',
      'mode': 'js',
      'title': 'Первое определённое значение',
      'statement': 'Напишите функцию firstDefined(arr): она возвращает первый элемент массива, который не '
                   'null и не undefined (0, пустая строка и false подходят!), или undefined, если таких нет.',
      'starter': 'function firstDefined(arr) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(firstDefined([null, undefined, 0, 5])));\n'
                'console.log(JSON.stringify(firstDefined([undefined, "", "a"])));\n'
                'console.log(JSON.stringify(firstDefined([null, false])));\n'
                'console.log(firstDefined([null, undefined]));\n'
                'console.log(firstDefined([]));\n',
      'hint': 'x != null — единственный случай, где допустимо нестрогое сравнение; или проверьте оба '
              'значения явно.',
      'expected': ['0', '""', 'false', 'undefined', 'undefined']},
     {'id': 'j4-parse-num',
      'mode': 'js',
      'title': 'Строка → число или null',
      'statement': 'Напишите функцию parseNum(s): она превращает строку в число функцией Number и возвращает '
                   'его; для пустой строки, строки из пробелов и всего, что даёт NaN, возвращает null.',
      'starter': 'function parseNum(s) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const s of ["42", "3.5", "", "   ", "abc", "1e3", "12px", "-7", "0x10"]) '
                'console.log(JSON.stringify(parseNum(s)));\n',
      'hint': 'Number("") равен 0 — пустые строки нужно отсечь заранее.',
      'expected': ['42', '3.5', 'null', 'null', 'null', '1000', 'null', '-7', '16']}]}
