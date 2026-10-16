"""Задачи книги «Современный Frontend», глава 5 (код + скрытый драйвер выполняются Node 22 в песочнице)."""

TASKS: dict[int, list[dict]] = {5: [{'id': 'j5-divmod',
      'mode': 'js',
      'title': 'Деление с остатком по правилам C',
      'statement': 'Напишите функцию divmod(a, b): она возвращает массив [q, r], где q — целая часть деления '
                   'с отбрасыванием дроби к нулю, а r — остаток от деления, знак которого совпадает со '
                   'знаком делимого (оператор %).',
      'starter': 'function divmod(a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const [a, b] of [[7, 2], [-7, 2], [7, -2], [-7, -2], [0, 5], [9, 3]]) '
                'console.log(JSON.stringify(divmod(a, b)));\n',
      'hint': 'Math.trunc(a / b) и a % b',
      'expected': ['[3,1]', '[-3,-1]', '[-3,1]', '[3,-1]', '[0,0]', '[3,0]']},
     {'id': 'j5-floormod',
      'mode': 'js',
      'title': 'Остаток как в Python',
      'statement': 'Напишите функцию mod(a, b), b > 0: остаток от деления, который всегда лежит в диапазоне '
                   'от 0 до b - 1 (для отрицательного a тоже), как a % b в Python.',
      'starter': 'function mod(a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const [a, b] of [[7, 3], [-7, 3], [-1, 5], [0, 4], [10, 5], [-10, 5], [-11, 5]]) '
                'console.log(mod(a, b));\n'
                'console.log(Object.is(mod(-10, 5), 0));\n',
      'hint': '((a % b) + b) % b. Проверьте, что результат -0 не получается.',
      'expected': ['1', '2', '4', '0', '0', '0', '4', 'true']},
     {'id': 'j5-is-even',
      'mode': 'js',
      'title': 'Чётное ли число (с отрицательными)',
      'statement': 'Напишите функцию isEven(n): она возвращает true для чётных целых, включая отрицательные; '
                   'для нечётных — false. Остаток от деления на 2 у отрицательных чисел бывает -1: учтите '
                   'это.',
      'starter': 'function isEven(n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const n of [0, 1, 2, -1, -2, -3, 100, 2 ** 40 + 1]) console.log(isEven(n));\n',
      'hint': 'n % 2 === 0: -0 === 0 тоже истина.',
      'expected': ['true', 'false', 'true', 'false', 'true', 'false', 'true', 'false']},
     {'id': 'j5-clamp',
      'mode': 'js',
      'title': 'Ограничить число диапазоном',
      'statement': 'Напишите функцию clamp(x, lo, hi): она возвращает lo, если x < lo, hi, если x > hi, и x '
                   'в остальных случаях. Если x — NaN, верните NaN.',
      'starter': 'function clamp(x, lo, hi) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const x of [5, -3, 12, 0, 10, NaN]) console.log(clamp(x, 0, 10));\n'
                'console.log(clamp(2.5, 1, 2));\n',
      'hint': 'Math.min(hi, Math.max(lo, x)) — Math.max и Math.min возвращают NaN, если среди аргументов '
              'NaN.',
      'expected': ['5', '0', '10', '0', '10', 'NaN', '2']},
     {'id': 'j5-to-int32',
      'mode': 'js',
      'title': 'Отбросить дробь побитовым оператором',
      'statement': 'Напишите функцию toInt(x): она отбрасывает дробную часть числа (к нулю) с помощью '
                   'побитового оператора, без Math.trunc, Math.floor, parseInt и Number. Для NaN должен '
                   'получиться 0.',
      'starter': 'function toInt(x) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'for (const x of [5.9, -5.9, 0.5, -0.5, NaN, 123, 2 ** 31 + 0.5]) console.log(toInt(x));\n'
                'console.log(__count("Math." + "trunc") + __count("Math." + "floor") + __count("pars" + '
                '"eInt"));\n',
      'hint': 'x | 0 — 32-битное целое со знаком.',
      'expected': ['5', '-5', '0', '0', '0', '123', '-2147483648', '0']},
     {'id': 'j5-add-nums',
      'mode': 'js',
      'title': 'Сложить числа в строках',
      'statement': 'Напишите функцию addNums(a, b): аргументы — числа или строки с числами (например, «5» и '
                   '1); функция возвращает их сумму как число, а не склейку.',
      'starter': 'function addNums(a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(addNums("5", 1));\n'
                'console.log(addNums("2.5", "0.5"));\n'
                'console.log(addNums(3, 4));\n'
                'console.log(addNums("10", "20") === 30);\n'
                'console.log(addNums("", 5));\n'
                'console.log(addNums("x", 1));\n',
      'hint': 'Number(a) + Number(b) — или унарный плюс.',
      'expected': ['6', '3', '7', 'true', '5', 'NaN']},
     {'id': 'j5-concat-all',
      'mode': 'js',
      'title': 'Склеить всё в строку',
      'statement': 'Напишите функцию joinAll(arr): она возвращает одну строку из всех элементов массива, '
                   'записанных подряд без разделителей (числа, булевы значения, null и undefined '
                   'записываются как их обычное строковое представление: «null», «undefined»).',
      'starter': 'function joinAll(arr) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(joinAll([1, "a", true, null, undefined, 2.5]));\n'
                'console.log(joinAll([]) === "");\n'
                'console.log(joinAll([[1, 2], [3]]));\n'
                'console.log(joinAll([{}]));\n',
      'hint': 'Не используйте join: он превращает null и undefined в пустую строку. Нужен String(x).',
      'expected': ['1atruenullundefined2.5', 'true', '1,23', '[object Object]']},
     {'id': 'j5-to-bool',
      'mode': 'js',
      'title': 'Явное приведение к булеву',
      'statement': 'Напишите функцию toBool(x): она возвращает true или false по правилам истинности (как '
                   'Boolean(x)), но без вызова Boolean и без двойного отрицания «!!».',
      'starter': 'function toBool(x) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'for (const x of [0, 1, "", "0", null, undefined, NaN, [], {}, -1, false, 0n]) '
                'console.log(toBool(x));\n'
                'console.log(__count("Bool" + "ean(") + __count("!" + "!"));\n',
      'hint': 'x ? true : false',
      'expected': ['false',
                   'true',
                   'false',
                   'true',
                   'false',
                   'false',
                   'false',
                   'true',
                   'true',
                   'true',
                   'false',
                   'false',
                   '0']},
     {'id': 'j5-parse-int',
      'mode': 'js',
      'title': 'Целое из пикселей',
      'statement': 'Напишите функцию px(s): она читает значение вроде «12px» или «-5px» и возвращает число; '
                   'если строка не начинается с числа, возвращает null. Основание системы счисления укажите '
                   'явно.',
      'starter': 'function px(s) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const s of ["12px", "-5px", "px12", "", "0", "007", "3.9em", " 42 "]) '
                'console.log(JSON.stringify(px(s)));\n',
      'hint': 'parseInt(s, 10), затем проверка на NaN.',
      'expected': ['12', '-5', 'null', 'null', '0', '7', '3', '42']},
     {'id': 'j5-parse-price',
      'mode': 'js',
      'title': 'Цена с запятой',
      'statement': 'Напишите функцию parsePrice(s): строка вроде «3,50 ₽» или «1299.9 руб» — верните число '
                   '(3.5 и 1299.9). Десятичный разделитель может быть запятой. Если числа нет — NaN.',
      'starter': 'function parsePrice(s) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const s of ["3,50 ₽", "1299.9 руб", "100", "бесплатно", "0,05"]) '
                'console.log(parsePrice(s));\n',
      'hint': 'parseFloat(s.replace(",", "."))',
      'expected': ['3.5', '1299.9', '100', 'NaN', '0.05']},
     {'id': 'j5-loose-table',
      'mode': 'js',
      'title': '== и === рядом',
      'statement': 'Напишите функцию eqPair(a, b): она возвращает массив из двух булевых значений: результат '
                   'нестрогого сравнения a == b и строгого a === b (именно в таком порядке). Ничего больше '
                   'проверять не нужно — запустите и изучите таблицу в выводе.',
      'starter': 'function eqPair(a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const pairs = [[1, "1"], [0, ""], [0, "0"], ["", "0"], [null, undefined], [null, 0], [0, '
                'false], [[], false], [NaN, NaN], ["a", "a"], [[1], 1], [undefined, 0]];\n'
                'for (const [a, b] of pairs) console.log(JSON.stringify(eqPair(a, b)));\n',
      'hint': 'return [a == b, a === b];',
      'expected': ['[true,false]',
                   '[true,false]',
                   '[true,false]',
                   '[false,false]',
                   '[true,false]',
                   '[false,false]',
                   '[true,false]',
                   '[true,false]',
                   '[false,false]',
                   '[true,true]',
                   '[true,false]',
                   '[false,false]']},
     {'id': 'j5-is-numeric',
      'mode': 'js',
      'title': 'Похоже ли на число',
      'statement': 'Напишите функцию isNumeric(v): true, если v — конечное число или непустая строка (без '
                   'пробелов по краям), которая Number превращает в конечное число. Всё остальное — false '
                   '(включая NaN, Infinity, пустую строку, «  » и «abc»).',
      'starter': 'function isNumeric(v) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const v of [5, "5", "-2.5", "1e3", "", "  ", " 5", "abc", NaN, Infinity, "Infinity", '
                'null, undefined, true, [], "0x10"]) console.log(isNumeric(v));\n',
      'hint': 'Для строк: trim() не должен менять строку и быть непустым; затем Number.isFinite(Number(v)).',
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
                   'false',
                   'false',
                   'false',
                   'false',
                   'false',
                   'true']},
     {'id': 'j5-compare-versions',
      'mode': 'js',
      'title': 'Сравнение версий',
      'statement': 'Напишите функцию compareVersions(a, b): версии записаны через точки («1.10.2»); верните '
                   '-1, если a < b, 1, если a > b, и 0, если равны. Части сравниваются как числа («1.10» '
                   'больше «1.9»); недостающая часть считается нулём.',
      'starter': 'function compareVersions(a, b) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const [a, b] of [["1.10", "1.9"], ["1.2.3", "1.2.3"], ["2.0", "2"], ["0.9", "0.10"], '
                '["1.0.1", "1"], ["3", "10"]]) console.log(compareVersions(a, b));\n',
      'hint': 'Разбейте по «.», приведите части к числам и сравните по порядку.',
      'expected': ['1', '0', '0', '-1', '1', '-1']},
     {'id': 'j5-sort-numeric',
      'mode': 'js',
      'title': 'Сортировка чисел',
      'statement': 'Напишите функцию sortNumbers(arr): она возвращает новый массив, отсортированный по '
                   'возрастанию как числа; исходный массив не меняется. Помните, что sort без функции '
                   'сравнивает строки.',
      'starter': 'function sortNumbers(arr) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const a = [10, 9, 1, 100, 25, -3];\n'
                'console.log(JSON.stringify(sortNumbers(a)));\n'
                'console.log(JSON.stringify(a));\n'
                'console.log(JSON.stringify(sortNumbers([])));\n'
                'console.log(JSON.stringify(sortNumbers([2, 1])));\n',
      'hint': '[...arr].sort((a, b) => a - b)',
      'expected': ['[-3,1,9,10,25,100]', '[10,9,1,100,25,-3]', '[]', '[1,2]']},
     {'id': 'j5-sort-ru',
      'mode': 'js',
      'title': 'Сортировка по русскому алфавиту',
      'statement': 'Напишите функцию sortWords(words): она возвращает новый массив строк, отсортированных по '
                   'правилам русского языка (ё рядом с е), с помощью localeCompare и локали «ru». Исходный '
                   'массив не меняйте.',
      'starter': 'function sortWords(words) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(JSON.stringify(sortWords(["яблоко", "ёж", "арбуз", "еж", "бананы", '
                '"Арбуз"])));\n'
                'console.log(JSON.stringify(sortWords([])));\n',
      'hint': 'a.localeCompare(b, "ru")',
      'expected': ['["арбуз","Арбуз","бананы","еж","ёж","яблоко"]', '[]']},
     {'id': 'j5-approx',
      'mode': 'js',
      'title': 'Сравнение дробных чисел',
      'statement': 'Напишите функцию approxEqual(a, b, eps = 1e-9): она возвращает true, если модуль '
                   'разности чисел не больше eps. Для 0.1 + 0.2 и 0.3 результат — true.',
      'starter': 'function approxEqual(a, b, eps = 1e-9) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(approxEqual(0.1 + 0.2, 0.3));\n'
                'console.log(approxEqual(1, 1.1));\n'
                'console.log(approxEqual(1, 1.05, 0.1));\n'
                'console.log(approxEqual(5, 5));\n'
                'console.log(approxEqual(NaN, NaN));\n',
      'hint': 'Math.abs(a - b) <= eps',
      'expected': ['true', 'false', 'true', 'true', 'false']},
     {'id': 'j5-round-away',
      'mode': 'js',
      'title': 'Округление «от нуля»',
      'statement': 'Напишите функцию roundHalfAway(x): округляет до целого, а половинки отдаёт в сторону от '
                   'нуля: 2.5 → 3, -2.5 → -3, -2.4 → -2. Math.round для отрицательных половинок даёт другое.',
      'starter': 'function roundHalfAway(x) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const x of [2.5, -2.5, 2.4, -2.4, 0.5, -0.5, 3, -7.5, 1.49]) '
                'console.log(roundHalfAway(x));\n',
      'hint': 'Math.sign(x) * Math.round(Math.abs(x))',
      'expected': ['3', '-3', '2', '-2', '1', '-1', '3', '-8', '1']},
     {'id': 'j5-thousands',
      'mode': 'js',
      'title': 'Разряды тысяч',
      'statement': 'Напишите функцию thousands(n): n — целое число; верните строку, где разряды отделены '
                   'пробелом: 1234567 → «1 234 567», -1000 → «-1 000». Intl и toLocaleString использовать '
                   'нельзя.',
      'starter': 'function thousands(n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'for (const n of [0, 12, 999, 1000, 1234567, -1000, -999, 100000, 2 ** 31]) '
                'console.log(thousands(n));\n'
                'console.log(__count("In" + "tl") + __count("toLocal" + "eString"));\n',
      'hint': 'Идите по цифрам; пробел ставьте перед цифрой, если до конца остаётся число цифр, кратное '
              'трём.',
      'expected': ['0',
                   '12',
                   '999',
                   '1 000',
                   '1 234 567',
                   '-1 000',
                   '-999',
                   '100 000',
                   '2 147 483 648',
                   '0']},
     {'id': 'j5-fill-defaults',
      'mode': 'js',
      'title': 'Значения по умолчанию через ??=',
      'statement': 'Напишите функцию fillDefaults(opts): она записывает в объект значения по умолчанию, если '
                   'поле отсутствует (null или undefined): size = 10, name = «аноним», debug = false. '
                   'Существующие значения, включая 0, пустую строку и false, остаются. Верните тот же '
                   'объект. Оператор || использовать нельзя.',
      'starter': 'function fillDefaults(opts) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(JSON.stringify(fillDefaults({})));\n'
                'console.log(JSON.stringify(fillDefaults({ size: 0, name: "", debug: true })));\n'
                'console.log(JSON.stringify(fillDefaults({ size: null, name: undefined })));\n'
                'const o = {};\n'
                'console.log(fillDefaults(o) === o);\n'
                'console.log(__count("|" + "|"));\n',
      'hint': 'opts.size ??= 10;',
      'expected': ['{"size":10,"name":"аноним","debug":false}',
                   '{"size":0,"name":"","debug":true}',
                   '{"size":10,"name":"аноним","debug":false}',
                   'true',
                   '0']},
     {'id': 'j5-tally',
      'mode': 'js',
      'title': 'Подсчёт слов',
      'statement': 'Напишите функцию tally(words): она возвращает объект, ключи которого — слова, а значения '
                   '— сколько раз слово встретилось. Используйте оператор ??=.',
      'starter': 'function tally(words) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'console.log(JSON.stringify(tally(["a", "b", "a", "c", "a", "b"])));\n'
                'console.log(JSON.stringify(tally([])));\n'
                'console.log(JSON.stringify(tally(["x"])));\n'
                'console.log(__count("?" + "?=") >= 1 ? "??= есть" : "нет ??=");\n',
      'hint': 'counts[w] ??= 0; counts[w]++;',
      'expected': ['{"a":3,"b":2,"c":1}', '{}', '{"x":1}', '??= есть']},
     {'id': 'j5-flags',
      'mode': 'js',
      'title': 'Флаги: маски и биты',
      'statement': 'Напишите четыре функции для работы с набором флагов в одном числе: hasFlag(mask, f) — '
                   'установлен ли флаг f; setFlag(mask, f) — вернуть маску с установленным f; '
                   'clearFlag(mask, f) — со сброшенным; toggleFlag(mask, f) — с переключённым. Флаги — '
                   'степени двойки (1, 2, 4, …).',
      'starter': 'function hasFlag(mask, f) {\n'
                 '}\n'
                 '\n'
                 'function setFlag(mask, f) {\n'
                 '}\n'
                 '\n'
                 'function clearFlag(mask, f) {\n'
                 '}\n'
                 '\n'
                 'function toggleFlag(mask, f) {\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'const READ = 1, WRITE = 2, EXEC = 4;\n'
                'let m = 0;\n'
                'm = setFlag(m, READ);\n'
                'm = setFlag(m, EXEC);\n'
                'console.log(m, hasFlag(m, READ), hasFlag(m, WRITE), hasFlag(m, EXEC));\n'
                'm = toggleFlag(m, WRITE);\n'
                'console.log(m);\n'
                'm = clearFlag(m, READ);\n'
                'console.log(m, hasFlag(m, READ));\n'
                'console.log(clearFlag(7, 2), toggleFlag(5, 5), setFlag(7, 4));\n',
      'hint': '& проверяет, | устанавливает, & ~ сбрасывает, ^ переключает.',
      'expected': ['5 true false true', '7', '6 false', '5 0 7']},
     {'id': 'j5-popcount',
      'mode': 'js',
      'title': 'Сколько единиц в числе',
      'statement': 'Напишите функцию bitCount(n): n — неотрицательное целое меньше 2 в 32-й степени; верните '
                   'количество единичных бит. Используйте побитовые операторы, без toString(2) и без '
                   'регулярных выражений.',
      'starter': 'function bitCount(n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'for (const n of [0, 1, 7, 8, 255, 2 ** 31, 2 ** 32 - 1, 1023, 0b101010]) '
                'console.log(bitCount(n));\n'
                'console.log(__count("toSt" + "ring"));\n',
      'hint': 'Сдвигайте через >>> (беззнаковый) и складывайте n & 1.',
      'expected': ['0', '1', '3', '1', '8', '1', '32', '10', '3', '0']},
     {'id': 'j5-pow2',
      'mode': 'js',
      'title': 'Степень двойки',
      'statement': 'Напишите функцию isPowerOfTwo(n): true для 1, 2, 4, 8 … (n — целое число меньше 2 в 31-й '
                   'степени); для 0 и отрицательных false. Цикл и логарифмы не используйте — только '
                   'побитовые операторы.',
      'starter': 'function isPowerOfTwo(n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'import * as __fs from "node:fs";\n'
                'const __src = __fs.readFileSync("/sandbox/main.mjs", "utf8").split("/*__" + '
                '"DRIVER__*/")[0];\n'
                'const __count = (p) => __src.split(p).length - 1;\n'
                'for (const n of [1, 2, 3, 4, 6, 8, 1024, 1023, 0, -2, -8, 2 ** 30]) '
                'console.log(isPowerOfTwo(n));\n'
                'console.log(__count("for" + " (") + __count("wh" + "ile") + __count("Math." + "log"));\n',
      'hint': 'n & (n - 1) сбрасывает младший единичный бит.',
      'expected': ['true',
                   'true',
                   'false',
                   'true',
                   'false',
                   'true',
                   'true',
                   'false',
                   'false',
                   'false',
                   'false',
                   'true',
                   '0']},
     {'id': 'j5-wrap32',
      'mode': 'js',
      'title': 'Свернуть до 32 бит',
      'statement': 'Напишите функцию wrap32(n): она возвращает 32-битное число со знаком, в которое '
                   '«сворачивается» целое n, как в C для int32_t: wrap32(2 ** 31) = -2147483648, wrap32(2 ** '
                   '32 + 5) = 5.',
      'starter': 'function wrap32(n) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const n of [0, 1, 2 ** 31 - 1, 2 ** 31, 2 ** 32, 2 ** 32 + 5, -(2 ** 31) - 1, '
                '3000000000]) console.log(wrap32(n));\n',
      'hint': 'n | 0',
      'expected': ['0', '1', '2147483647', '-2147483648', '0', '5', '2147483647', '-1294967296']},
     {'id': 'j5-classify',
      'mode': 'js',
      'title': 'Что за значение',
      'statement': 'Напишите функцию kind(v): она возвращает строку: «null», «array», «date», «regexp», '
                   '«function», «object» (для остальных объектов) или результат typeof для примитивов. Для '
                   'даты и регулярного выражения используйте instanceof.',
      'starter': 'function kind(v) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'for (const v of [null, [], new Date(0), /a/, () => 1, {}, 5, "s", undefined, true, 1n, new '
                'Map()]) console.log(kind(v));\n',
      'hint': 'Порядок проверок важен: сначала null, затем массив, дата, регулярное выражение.',
      'expected': ['null',
                   'array',
                   'date',
                   'regexp',
                   'function',
                   'object',
                   'number',
                   'string',
                   'undefined',
                   'boolean',
                   'bigint',
                   'object']},
     {'id': 'j5-own-vs-in',
      'mode': 'js',
      'title': 'Собственное или унаследованное',
      'statement': 'Напишите функцию keyInfo(obj, key): она возвращает «own», если свойство key есть у '
                   'самого объекта, «inherited», если оно только в цепочке прототипов (оператор in), и '
                   '«none», если его нет вовсе.',
      'starter': 'function keyInfo(obj, key) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const o = { a: 1, b: undefined };\n'
                'for (const k of ["a", "b", "toString", "c", "constructor"]) console.log(keyInfo(o, k));\n'
                'console.log(keyInfo([], "length"));\n'
                'console.log(keyInfo(Object.create({ x: 1 }), "x"));\n',
      'hint': 'Object.hasOwn(obj, key) — собственное; key in obj — любое, включая унаследованное.',
      'expected': ['own', 'own', 'inherited', 'none', 'inherited', 'own', 'inherited']},
     {'id': 'j5-money-object',
      'mode': 'js',
      'title': 'Объект, который ведёт себя как число и строка',
      'statement': 'Напишите функцию makeMoney(cents): она возвращает объект с методами valueOf() (число — '
                   'сумма в копейках) и toString() (строка вида «12.34 ₽»). Тогда m * 2 даёт удвоенные '
                   'копейки, а `${m}` — текст.',
      'starter': 'function makeMoney(cents) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'const m = makeMoney(1234);\n'
                'console.log(m * 2);\n'
                'console.log(`${m}`);\n'
                'console.log(m + 1);\n'
                'console.log(String(makeMoney(5)));\n'
                'console.log(makeMoney(100) > makeMoney(99));\n'
                'console.log(Number(makeMoney(7)));\n',
      'hint': 'valueOf возвращает число, toString — строку; (cents / 100).toFixed(2) + " ₽".',
      'expected': ['2468', '12.34 ₽', '1235', '0.05 ₽', 'true', '7']},
     {'id': 'j5-fix-chain',
      'mode': 'js',
      'title': 'Исправьте: цепочка сравнений',
      'statement': 'Функция inRange(x) должна возвращать true, если x строго больше 0 и строго меньше 10. '
                   'Сейчас она использует цепочку 0 < x < 10 и ошибается для x ≥ 10. Исправьте.',
      'starter': 'function inRange(x) {\n  return 0 < x < 10;\n}\n',
      'driver': '/*__DRIVER__*/\nfor (const x of [5, 0, 10, 15, -1, 9.99, 100]) console.log(inRange(x));\n',
      'hint': 'x > 0 && x < 10',
      'expected': ['true', 'false', 'false', 'false', 'false', 'true', 'false']},
     {'id': 'j5-eval-rpn',
      'mode': 'js',
      'title': 'Калькулятор в обратной польской записи',
      'statement': 'Напишите функцию evalRpn(tokens): токены — массив строк с числами и операторами + - * /; '
                   'верните результат вычисления в обратной польской записи, например ["3", "4", "+", "2", '
                   '"*"] → 14. Числа приводите к числу явно; деление дробное.',
      'starter': 'function evalRpn(tokens) {\n}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(evalRpn(["3", "4", "+", "2", "*"]));\n'
                'console.log(evalRpn(["5", "1", "2", "+", "4", "*", "+", "3", "-"]));\n'
                'console.log(evalRpn(["7", "2", "/"]));\n'
                'console.log(evalRpn(["10"]));\n'
                'console.log(evalRpn(["2", "3", "-"]));\n'
                'console.log(evalRpn(["1.5", "2", "*"]));\n',
      'hint': 'Стек: числа кладите, оператор снимает два значения и кладёт результат. Не забудьте Number(t) '
              '— иначе + склеит строки.',
      'expected': ['14', '14', '3.5', '10', '-1', '3']},
     {'id': 'j5-fix-concat',
      'mode': 'js',
      'title': 'Исправьте: цены из формы — строки',
      'statement': 'Функция total(prices) принимает массив цен, записанных строками («10», «2.5»), и должна '
                   'вернуть их сумму числом. Сейчас вместо суммы получается склейка. Исправьте.',
      'starter': 'function total(prices) {\n'
                 '  let sum = 0;\n'
                 '  for (const p of prices) {\n'
                 '    sum = sum + p;\n'
                 '  }\n'
                 '  return sum;\n'
                 '}\n',
      'driver': '/*__DRIVER__*/\n'
                'console.log(total(["10", "2.5", "7.5"]));\n'
                'console.log(total([]));\n'
                'console.log(total(["1"]));\n'
                'console.log(typeof total(["4", "5"]));\n',
      'hint': 'Number(p) перед сложением.',
      'expected': ['20', '0', '1', 'number']}]}
