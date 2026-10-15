"""Задачи книги «Изучаем Rust»: главы 1–5 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {1: [{'id': 'r1-format',
      'mode': 'rust',
      'title': 'Форматирование: питонские f-строки в Rust',
      'statement': 'Напишите fn row(label: &str, n: u32) -> String, которая собирает строку через format!: '
                   'метка по левому краю в 6 позициях, затем «|», число по правому краю в 6 позициях, «|», '
                   'число в шестнадцатеричном виде с префиксом 0x и шириной 6 (с нулями слева), «|», '
                   'двоичная запись в 8 разрядов. Например, row("abc", 42) → "abc   |    '
                   '42|0x002a|00101010".',
      'starter': 'fn row(label: &str, n: u32) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", row("abc", 42));\n'
                '    println!("{}", row("x", 255));\n'
                '    println!("{}", row("long", 7));\n'
                '}\n',
      'hint': 'В format! спецификации пишут после двоеточия: {n:>6} — вправо в 6 позиций, {n:#06x} — hex с '
              '0x и нулями, {n:08b} — двоичное.',
      'expected': ['abc   |    42|0x002a|00101010',
                   'x     |   255|0x00ff|11111111',
                   'long  |     7|0x0007|00000111']},
     {'id': 'r1-fahrenheit',
      'mode': 'rust',
      'title': 'Градусы: целые и дробные не смешиваются',
      'statement': 'Напишите to_fahrenheit(c: f64) -> f64 по формуле c · 9 / 5 + 32 и to_celsius(f: f64) -> '
                   'f64. В питоне 9 / 5 тоже дробное; в расте в формуле с f64 нужны литералы 9.0 и 5.0.',
      'starter': 'fn to_fahrenheit(c: f64) -> f64 {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn to_celsius(f: f64) -> f64 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    for c in [-40.0, 0.0, 36.6, 100.0] {\n'
                '        println!("{:.1} -> {:.1}", c, to_fahrenheit(c));\n'
                '    }\n'
                '    println!("{:.1}", to_celsius(212.0));\n'
                '    println!("{:.1}", to_celsius(to_fahrenheit(21.5)));\n'
                '}\n',
      'hint': 'Целый литерал 9 имеет тип i32 и не умножается на f64: пишите 9.0.',
      'expected': ['-40.0 -> -40.0', '0.0 -> 32.0', '36.6 -> 97.9', '100.0 -> 212.0', '100.0', '21.5']},
     {'id': 'r1-fizzbuzz',
      'mode': 'rust',
      'title': 'FizzBuzz: if — это выражение',
      'statement': 'Напишите fizzbuzz(n: u32) -> String: «FizzBuzz» при делимости на 15, «Fizz» — на 3, '
                   '«Buzz» — на 5, иначе число. Слово return не используйте: пусть значением функции будет '
                   'само выражение if / else.',
      'starter': 'fn fizzbuzz(n: u32) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!("ret", "urn ")).count();\n'
                '    let line: Vec<String> = (1..=15).map(fizzbuzz).collect();\n'
                '    println!("{}", line.join(" "));\n'
                '    println!("{} {}", fizzbuzz(30), fizzbuzz(97));\n'
                '    println!("early exits: {}", bad0);\n'
                '}\n',
      'hint': 'Каждая ветка заканчивается значением без точки с запятой; обе ветки должны давать String.',
      'expected': ['1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz',
                   'FizzBuzz 97',
                   'early exits: 0']},
     {'id': 'r1-mut-fix',
      'mode': 'rust',
      'title': 'Исправьте: переменная без mut',
      'statement': 'Код не компилируется: компилятор не даёт менять неизменяемую переменную. Исправьте '
                   'функцию sum_to(n: u32) -> u32 (сумма чисел от 1 до n включительно) минимальной правкой.',
      'starter': 'fn sum_to(n: u32) -> u32 {\n'
                 '    let total = 0;\n'
                 '    for i in 1..=n {\n'
                 '        total += i;\n'
                 '    }\n'
                 '    total\n'
                 '}\n',
      'driver': 'fn main() {\n    println!("{} {} {}", sum_to(0), sum_to(10), sum_to(100));\n}\n',
      'hint': 'let mut total = 0; — слово mut разрешает изменять значение на месте.',
      'expected': ['0 55 5050']},
     {'id': 'r1-shadowing',
      'mode': 'rust',
      'title': 'Затенение: смена типа под тем же именем',
      'statement': 'Напишите fn double_text(input: &str) -> i32: обрежьте пробелы по краям (trim), разберите '
                   'число (parse) и верните его, умноженное на 2. Используйте затенение: три раза let input '
                   '= ... с одним именем, тип меняется с &str на i32. Ввод всегда корректен (можно unwrap).',
      'starter': 'fn double_text(input: &str) -> i32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!("let in", "put = ")).count();\n'
                '    for s in ["21", "  -4 ", "\\t100\\n"] {\n'
                '        println!("{}", double_text(s));\n'
                '    }\n'
                '    println!("shadow lets: {}", bad0 >= 2);\n'
                '}\n',
      'hint': 'let input: i32 = input.parse().unwrap(); — справа ещё старая &str, слева уже новая i32.',
      'expected': ['42', '-8', '200', 'shadow lets: true']},
     {'id': 'r1-overflow-modes',
      'mode': 'rust',
      'title': 'Переполнение: четыре способа',
      'statement': 'Напишите fn add_modes(a: u8, b: u8) -> (u8, Option<u8>, u8, (u8, bool)): результат '
                   'сложения по четырём правилам — с заворачиванием (wrapping), с проверкой (checked: None '
                   'при переполнении), с насыщением (saturating) и overflowing (значение и флаг). Питон '
                   'переполнения не знает, а процессор — знает.',
      'starter': 'fn add_modes(a: u8, b: u8) -> (u8, Option<u8>, u8, (u8, bool)) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for (a, b) in [(1, 2), (200, 55), (200, 56), (255, 255)] {\n'
                '        println!("{a}+{b}: {:?}", add_modes(a, b));\n'
                '    }\n'
                '}\n',
      'hint': 'У целых есть методы wrapping_add, checked_add, saturating_add, overflowing_add.',
      'expected': ['1+2: (3, Some(3), 3, (3, false))',
                   '200+55: (255, Some(255), 255, (255, false))',
                   '200+56: (0, None, 255, (0, true))',
                   '255+255: (254, None, 255, (254, true))']},
     {'id': 'r1-casts',
      'mode': 'rust',
      'title': 'Приведение as: отрезать биты',
      'statement': 'Напишите fn casts(x: i32) -> (u8, i8, u16, f64): значение x, приведённое as к u8, i8 и '
                   'u16, и x как f64, делённое на 2. Посмотрите, как as отрезает старшие биты '
                   '(дополнительный код из главы про числа) — исключений нет.',
      'starter': 'fn casts(x: i32) -> (u8, i8, u16, f64) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for x in [65, 300, -1, 70000, -129] {\n'
                '        println!("{x}: {:?}", casts(x));\n'
                '    }\n'
                '    println!("{}", 3.99_f64 as i32);\n'
                '    println!("{}", (-1.5_f64) as u8);\n'
                '    println!("{}", 300.0_f64 as u8);\n'
                '    println!("{}", 65u8 as char);\n'
                '}\n',
      'hint': 'x as u8 берёт младшие 8 бит; x as i8 трактует их как число со знаком.',
      'expected': ['65: (65, 65, 65, 32.5)',
                   '300: (44, 44, 300, 150.0)',
                   '-1: (255, -1, 65535, -0.5)',
                   '70000: (112, 112, 4464, 35000.0)',
                   '-129: (127, 127, 65407, -64.5)',
                   '3',
                   '0',
                   '255',
                   'A']},
     {'id': 'r1-popcount',
      'mode': 'rust',
      'title': 'Подсчёт единиц руками',
      'statement': 'Напишите fn popcount(mut n: u32) -> u32 — число единичных битов — циклом со сдвигом и '
                   'маской (n & 1, n >> 1). Метод count_ones использовать нельзя: проверка ищет его в вашем '
                   'коде.',
      'starter': 'fn popcount(mut n: u32) -> u32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!("count", "_ones")).count();\n'
                '    for n in [0u32, 1, 7, 255, 1 << 31, u32::MAX, 0b1010_1010] {\n'
                '        println!("{n:#b}: {}", popcount(n));\n'
                '    }\n'
                '    println!("builtin used: {}", bad0);\n'
                '}\n',
      'hint': 'while n != 0 { count += n & 1; n >>= 1; } — сдвиг вправо отбрасывает младший бит.',
      'expected': ['0b0: 0',
                   '0b1: 1',
                   '0b111: 3',
                   '0b11111111: 8',
                   '0b10000000000000000000000000000000: 1',
                   '0b11111111111111111111111111111111: 32',
                   '0b10101010: 4',
                   'builtin used: 0']},
     {'id': 'r1-pydivmod',
      'mode': 'rust',
      'title': 'Деление как в Python',
      'statement': 'Напишите fn py_divmod(a: i32, b: i32) -> (i32, i32): целое деление и остаток по правилам '
                   'питона (a // b, a % b): частное округляется вниз, остаток имеет знак делителя. Раст по '
                   'умолчанию округляет к нулю, а остаток берёт знак делимого.',
      'starter': 'fn py_divmod(a: i32, b: i32) -> (i32, i32) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for (a, b) in [(7, 2), (-7, 2), (7, -2), (-7, -2), (6, 3), (-6, 3), (0, 5)] {\n'
                '        println!("{a} // {b} = {:?}", py_divmod(a, b));\n'
                '    }\n'
                '}\n',
      'hint': 'Если остаток не нулевой и его знак не совпадает со знаком b, уменьшите частное на 1 и '
              'добавьте b к остатку.',
      'expected': ['7 // 2 = (3, 1)',
                   '-7 // 2 = (-4, 1)',
                   '7 // -2 = (-4, -1)',
                   '-7 // -2 = (3, -1)',
                   '6 // 3 = (2, 0)',
                   '-6 // 3 = (-2, 0)',
                   '0 // 5 = (0, 0)']},
     {'id': 'r1-float-eq',
      'mode': 'rust',
      'title': 'Сравнение дробных с допуском',
      'statement': 'Напишите fn approx_eq(a: f64, b: f64) -> bool: числа равны, если |a − b| не больше 1e-9 '
                   '· max(1, |a|, |b|). Точное сравнение 0.1 + 0.2 == 0.3 ложно в любом языке — вспомните '
                   'главу про числа.',
      'starter': 'fn approx_eq(a: f64, b: f64) -> bool {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{} {}", 0.1 + 0.2 == 0.3, approx_eq(0.1 + 0.2, 0.3));\n'
                '    let mut s = 0.0;\n'
                '    for _ in 0..10 {\n'
                '        s += 0.1;\n'
                '    }\n'
                '    println!("{} {}", s == 1.0, approx_eq(s, 1.0));\n'
                '    println!("{} {}", approx_eq(1e12, 1e12 + 1.0), approx_eq(1.0, 1.001));\n'
                '    println!("{} {}", approx_eq(0.0, 1e-12), approx_eq(0.0, 1e-3));\n'
                '}\n',
      'hint': 'У f64 есть методы abs() и max(): (a - b).abs() <= 1e-9 * масштаб.',
      'expected': ['false true', 'false true', 'true false', 'true false']},
     {'id': 'r1-tuple-minmax',
      'mode': 'rust',
      'title': 'Кортеж как результат',
      'statement': 'Напишите fn min_max(a: i32, b: i32, c: i32) -> (i32, i32): наименьшее и наибольшее из '
                   'трёх. Результат разбирается на части: let (lo, hi) = min_max(...).',
      'starter': 'fn min_max(a: i32, b: i32, c: i32) -> (i32, i32) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for (a, b, c) in [(1, 2, 3), (9, -4, 5), (7, 7, 7), (-1, -9, -5)] {\n'
                '        let (lo, hi) = min_max(a, b, c);\n'
                '        println!("{lo} {hi}");\n'
                '    }\n'
                '}\n',
      'hint': 'Методы min и max можно соединять цепочкой: a.min(b).min(c).',
      'expected': ['1 3', '-4 9', '7 7', '-9 -1']},
     {'id': 'r1-array-reverse',
      'mode': 'rust',
      'title': 'Массив на стеке: копия, а не ссылка',
      'statement': 'Напишите fn reversed(a: [i32; 5]) -> [i32; 5] — новый массив в обратном порядке (индексы '
                   'и цикл for). Массив известного размера копируется целиком: пройдите по ячейкам и '
                   'убедитесь, что исходник не изменился.',
      'starter': 'fn reversed(a: [i32; 5]) -> [i32; 5] {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let a = [1, 2, 3, 4, 5];\n'
                '    let b = reversed(a);\n'
                '    println!("{:?} {:?}", a, b);\n'
                '    println!("{:?}", reversed([10, 0, -3, 8, 8]));\n'
                '}\n',
      'hint': 'let mut out = [0; 5]; — массив из пяти нулей; out[4 - i] = a[i].',
      'expected': ['[1, 2, 3, 4, 5] [5, 4, 3, 2, 1]', '[8, 8, -3, 0, 10]']},
     {'id': 'r1-sum-squares',
      'mode': 'rust',
      'title': 'Диапазоны: сумма квадратов',
      'statement': 'Напишите fn sum_squares(n: u64) -> u64: сумма i² для i от 1 до n включительно (диапазон '
                   '1..=n и цикл for).',
      'starter': 'fn sum_squares(n: u64) -> u64 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for n in [0, 1, 3, 10, 1000] {\n'
                '        println!("{n}: {}", sum_squares(n));\n'
                '    }\n'
                '}\n',
      'hint': '1..=n включает n, а 1..n — нет.',
      'expected': ['0: 0', '1: 1', '3: 14', '10: 385', '1000: 333833500']},
     {'id': 'r1-loop-break',
      'mode': 'rust',
      'title': 'loop с break-значением',
      'statement': 'Напишите fn first_square_over(limit: u32) -> u32: наименьшее n, для которого n · n > '
                   'limit. Используйте loop, а результат верните через break n — у цикла loop есть значение.',
      'starter': 'fn first_square_over(limit: u32) -> u32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!("bre", "ak n")).count();\n'
                '    for limit in [0, 1, 50, 99, 100, 10_000] {\n'
                '        println!("{limit}: {}", first_square_over(limit));\n'
                '    }\n'
                '    println!("break with value: {}", bad0 > 0);\n'
                '}\n',
      'hint': 'loop { if условие { break значение; } ... } — значение break становится значением всего loop.',
      'expected': ['0: 1', '1: 2', '50: 8', '99: 10', '100: 11', '10000: 101', 'break with value: true']},
     {'id': 'r1-labeled-break',
      'mode': 'rust',
      'title': 'Метки циклов',
      'statement': 'Напишите fn find_pair(target: u32) -> Option<(u32, u32)>: пара (a, b), a ≤ b, обе от 2 '
                   'до 50, с произведением target. Первая найденная пара при переборе a по возрастанию, '
                   "затем b. Нет пары — None. Для выхода из двух циклов сразу используйте метку 'outer.",
      'starter': 'fn find_pair(target: u32) -> Option<(u32, u32)> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!("break ", "\'outer")).count();\n'
                '    for t in [4, 42, 97, 2500, 2501, 6] {\n'
                '        println!("{t}: {:?}", find_pair(t));\n'
                '    }\n'
                '    println!("labeled: {}", bad0 > 0);\n'
                '}\n',
      'hint': "'outer: for a in ... { for b in ... { if ... { break 'outer; } } } — метка называет цикл, "
              'который прерываем.',
      'expected': ['4: Some((2, 2))',
                   '42: Some((2, 21))',
                   '97: None',
                   '2500: Some((50, 50))',
                   '2501: None',
                   '6: Some((2, 3))',
                   'labeled: true']},
     {'id': 'r1-match-ranges',
      'mode': 'rust',
      'title': 'match по диапазонам',
      'statement': 'Напишите fn classify(n: i32) -> &\'static str через match: n < 0 → "negative", 0 → '
                   '"zero", 1..=9 → "digit", 10..=99 → "two-digit", остальное → "big". Шаблоны диапазонов '
                   'пишутся как 1..=9.',
      'starter': "fn classify(n: i32) -> &'static str {\n    todo!()\n}\n",
      'driver': 'fn main() {\n'
                '    for n in [-100, -1, 0, 5, 9, 10, 99, 100, 123456] {\n'
                '        println!("{n}: {}", classify(n));\n'
                '    }\n'
                '}\n',
      'hint': 'match обязан покрыть все значения; последняя ветка _ => ... ловит остальное.',
      'expected': ['-100: negative',
                   '-1: negative',
                   '0: zero',
                   '5: digit',
                   '9: digit',
                   '10: two-digit',
                   '99: two-digit',
                   '100: big',
                   '123456: big']},
     {'id': 'r1-semicolon-fix',
      'mode': 'rust',
      'title': 'Исправьте: лишняя точка с запятой',
      'statement': 'Функция cube должна возвращать куб числа, но не компилируется: из-за лишнего знака она '
                   'возвращает (). Исправьте одну строку.',
      'starter': 'fn cube(x: i64) -> i64 {\n    x * x * x;\n}\n',
      'driver': 'fn main() {\n    println!("{} {} {}", cube(3), cube(-2), cube(0));\n}\n',
      'hint': 'Выражение без точки с запятой в конце блока — его значение.',
      'expected': ['27 -8 0']},
     {'id': 'r1-const',
      'mode': 'rust',
      'title': 'Константы',
      'statement': 'Объявите константы SECS_PER_MINUTE = 60, SECS_PER_HOUR = 3600 и SECS_PER_DAY = 86400 '
                   '(тип u32) и напишите fn to_seconds(days: u32, hours: u32, minutes: u32) -> u32. У '
                   'констант тип обязателен, а имена — в верхнем регистре.',
      'starter': 'fn to_seconds(days: u32, hours: u32, minutes: u32) -> u32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{} {} {}", SECS_PER_MINUTE, SECS_PER_HOUR, SECS_PER_DAY);\n'
                '    println!("{}", to_seconds(0, 0, 90));\n'
                '    println!("{}", to_seconds(1, 2, 3));\n'
                '    println!("{}", to_seconds(10, 0, 0));\n'
                '}\n',
      'hint': 'const NAME: u32 = 60; — вне функции, тип пишется обязательно.',
      'expected': ['60 3600 86400', '5400', '93780', '864000']},
     {'id': 'r1-text-stats',
      'mode': 'rust',
      'title': 'Символы и байты',
      'statement': 'Напишите fn text_stats(s: &str) -> (usize, usize): (длина в байтах, число символов). В '
                   'питоне len(s) считает символы; в расте len() — байты, а символы считают через '
                   'chars().count().',
      'starter': 'fn text_stats(s: &str) -> (usize, usize) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for s in ["hello", "привет", "日本語", "a😀b", ""] {\n'
                '        println!("{:?} -> {:?}", s, text_stats(s));\n'
                '    }\n'
                '}\n',
      'hint': 's.len() — байты, s.chars().count() — символы.',
      'expected': ['"hello" -> (5, 5)',
                   '"привет" -> (12, 6)',
                   '"日本語" -> (9, 3)',
                   '"a😀b" -> (6, 3)',
                   '"" -> (0, 0)']},
     {'id': 'r1-utf8-hex',
      'mode': 'rust',
      'title': 'Байты UTF-8 в шестнадцатеричном виде',
      'statement': 'Напишите fn hex_bytes(s: &str) -> String: байты строки в UTF-8, каждый как две '
                   'шестнадцатеричные цифры, через пробел. Сверьтесь с главой про символы: «Ж» — d0 96.',
      'starter': 'fn hex_bytes(s: &str) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for s in ["A", "Ж", "€", "привет", "😀"] {\n'
                '        println!("{s}: {}", hex_bytes(s));\n'
                '    }\n'
                '}\n',
      'hint': 's.bytes() даёт u8; format!("{b:02x}") — две hex-цифры; join(" ") склеивает.',
      'expected': ['A: 41',
                   'Ж: d0 96',
                   '€: e2 82 ac',
                   'привет: d0 bf d1 80 d0 b8 d0 b2 d0 b5 d1 82',
                   '😀: f0 9f 98 80']},
     {'id': 'r1-endianness',
      'mode': 'rust',
      'title': 'Порядок байтов в числе',
      'statement': 'Напишите fn byte_orders(n: u32) -> (String, String): байты числа n в порядке '
                   'little-endian и big-endian, в hex через пробел. Методы u32::to_le_bytes и to_be_bytes.',
      'starter': 'fn byte_orders(n: u32) -> (String, String) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for n in [0x12345678u32, 1, 0xdeadbeef, 256] {\n'
                '        let (le, be) = byte_orders(n);\n'
                '        println!("{n:#x}: LE [{le}] BE [{be}]");\n'
                '    }\n'
                '}\n',
      'hint': 'to_le_bytes() возвращает [u8; 4] — массив на стеке; обойдите его итератором .iter().',
      'expected': ['0x12345678: LE [78 56 34 12] BE [12 34 56 78]',
                   '0x1: LE [01 00 00 00] BE [00 00 00 01]',
                   '0xdeadbeef: LE [ef be ad de] BE [de ad be ef]',
                   '0x100: LE [00 01 00 00] BE [00 00 01 00]']},
     {'id': 'r1-twos-complement',
      'mode': 'rust',
      'title': 'Дополнительный код вручную',
      'statement': 'Напишите fn to_bits(n: i8) -> String (8 двоичных цифр дополнительного кода: приведите n '
                   'as u8 и выведите {:08b}) и fn from_bits(bits: &str) -> i8 (разберите строку '
                   'u8::from_str_radix(bits, 2) и приведите as i8).',
      'starter': 'fn to_bits(n: i8) -> String {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn from_bits(bits: &str) -> i8 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    for n in [5, -5, 0, 127, -128, -1] {\n'
                '        let b = to_bits(n);\n'
                '        println!("{n}: {b} -> {}", from_bits(&b));\n'
                '    }\n'
                '}\n',
      'hint': 'as между целыми одной ширины ничего не вычисляет — меняет трактовку тех же восьми бит.',
      'expected': ['5: 00000101 -> 5',
                   '-5: 11111011 -> -5',
                   '0: 00000000 -> 0',
                   '127: 01111111 -> 127',
                   '-128: 10000000 -> -128',
                   '-1: 11111111 -> -1']},
     {'id': 'r1-sizes',
      'mode': 'rust',
      'title': 'Размеры типов в памяти',
      'statement': "Напишите fn sizes() -> Vec<(&'static str, usize)>: пары (имя типа, std::mem::size_of) "
                   'для: u8, i32, u64, char, bool, (u8, u32), [u16; 5], &str, usize — именно в этом порядке. '
                   'Обратите внимание на выравнивание кортежа и на то, что &str — это два слова (указатель и '
                   'длина).',
      'starter': "fn sizes() -> Vec<(&'static str, usize)> {\n    todo!()\n}\n",
      'driver': 'fn main() {\n'
                '    for (name, bytes) in sizes() {\n'
                '        println!("{name}: {bytes}");\n'
                '    }\n'
                '}\n',
      'hint': 'size_of::<T>() — функция времени компиляции. Кортеж (u8, u32) занимает 8 байт: u32 выровнен '
              'по четырём.',
      'expected': ['u8: 1',
                   'i32: 4',
                   'u64: 8',
                   'char: 4',
                   'bool: 1',
                   '(u8, u32): 8',
                   '[u16; 5]: 10',
                   '&str: 16',
                   'usize: 8']},
     {'id': 'r1-stack-direction',
      'mode': 'rust',
      'title': 'Куда растёт стек',
      'statement': 'Драйвер вызывает вложенные функции и записывает адреса их локальных переменных в срез '
                   'addrs (от внешнего вызова к внутреннему). Напишите fn grows_down(addrs: &[usize]) -> '
                   'bool: true, если каждый следующий адрес строго меньше предыдущего (стек растёт к меньшим '
                   'адресам, как в главе про процессор).',
      'starter': 'fn grows_down(addrs: &[usize]) -> bool {\n    todo!()\n}\n',
      'driver': '#[inline(never)]\n'
                'fn level(depth: u32, out: &mut Vec<usize>) {\n'
                '    let marker = std::hint::black_box(depth);\n'
                '    out.push(&marker as *const u32 as usize);\n'
                '    if depth > 0 {\n'
                '        level(depth - 1, out);\n'
                '    }\n'
                '    std::hint::black_box(&marker);\n'
                '}\n'
                '\n'
                'fn main() {\n'
                '    let mut addrs = Vec::new();\n'
                '    level(5, &mut addrs);\n'
                '    println!("{} frames", addrs.len());\n'
                '    println!("grows down: {}", grows_down(&addrs));\n'
                '    println!("{}", grows_down(&[10, 20, 30]));\n'
                '    println!("{}", grows_down(&[30, 20, 10]));\n'
                '    println!("{}", grows_down(&[5]));\n'
                '}\n',
      'hint': 'Срез &[usize] — вид на массив чисел: перебирайте индексы 1..addrs.len().',
      'expected': ['6 frames', 'grows down: true', 'false', 'true', 'true']},
     {'id': 'r1-recursion-limit',
      'mode': 'rust',
      'title': 'Глубокая рекурсия против стека',
      'statement': 'Рекурсивная sum_to(n) строит кадр на каждый шаг и для n = 20 миллионов переполняет стек '
                   '(в питоне это был бы RecursionError на тысяче). Перепишите sum_to циклом с тем же '
                   'результатом.',
      'starter': 'fn sum_to(n: u64) -> u64 {\n'
                 '    if n == 0 {\n'
                 '        0\n'
                 '    } else {\n'
                 '        n + std::hint::black_box(sum_to(n - 1))\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n    println!("{}", sum_to(10));\n    println!("{}", sum_to(20_000_000));\n}\n',
      'hint': 'Каждый рекурсивный вызов — новый кадр на стеке; цикл использует один кадр.',
      'expected': ['55', '200000010000000']},
     {'id': 'r1-sum-words',
      'mode': 'rust',
      'title': 'Разбор чисел из строки',
      'statement': 'Напишите fn sum_words(line: &str) -> i64: сумма целых чисел, записанных через пробелы '
                   '(split_whitespace и parse). В питоне это sum(map(int, line.split())); тип для parse раст '
                   'требует указать.',
      'starter': 'fn sum_words(line: &str) -> i64 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for line in ["1 2 3", "  10   -4  5 ", "42", "", "9000000000 1"] {\n'
                '        println!("{:?} -> {}", line, sum_words(line));\n'
                '    }\n'
                '}\n',
      'hint': 'let n: i64 = word.parse().unwrap(); — тип из аннотации выбирает разбор.',
      'expected': ['"1 2 3" -> 6',
                   '"  10   -4  5 " -> 11',
                   '"42" -> 42',
                   '"" -> 0',
                   '"9000000000 1" -> 9000000001']},
     {'id': 'r1-calendar',
      'mode': 'rust',
      'title': 'Високосный год и дни в месяце',
      'statement': 'Напишите fn is_leap(year: u32) -> bool и fn days_in_month(year: u32, month: u32) -> u32 '
                   '(match по номеру месяца, в феврале учитывайте високосность). Для месяца вне 1..=12 '
                   'вызовите panic!("bad month") — паника как в питоне ValueError, но без перехвата.',
      'starter': 'fn is_leap(year: u32) -> bool {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn days_in_month(year: u32, month: u32) -> u32 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    for y in [1900, 2000, 2023, 2024] {\n'
                '        println!("{y}: leap={} feb={}", is_leap(y), days_in_month(y, 2));\n'
                '    }\n'
                '    let total: u32 = (1..=12).map(|m| days_in_month(2024, m)).sum();\n'
                '    println!("{total}");\n'
                '}\n',
      'hint': 'Шаблон 1 | 3 | 5 объединяет несколько значений в одной ветке match.',
      'expected': ['1900: leap=false feb=28',
                   '2000: leap=true feb=29',
                   '2023: leap=false feb=28',
                   '2024: leap=true feb=29',
                   '366']},
     {'id': 'r1-iter-chain',
      'mode': 'rust',
      'title': 'Цепочка итераторов вместо генератора',
      'statement': 'Напишите fn sum_even_squares(n: u32) -> u32 — сумма квадратов чётных чисел от 1 до n — '
                   'одной цепочкой (1..=n).filter(..).map(..).sum() и fn count_vowels(s: &str) -> usize — '
                   'число гласных a e i o u (без учёта регистра). В питоне это генераторные выражения.',
      'starter': 'fn sum_even_squares(n: u32) -> u32 {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn count_vowels(s: &str) -> usize {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    for n in [0, 1, 2, 10, 100] {\n'
                '        println!("{n}: {}", sum_even_squares(n));\n'
                '    }\n'
                '    for s in ["Hello World", "rhythm", "AEIOU", "Привет", "education"] {\n'
                '        println!("{s}: {}", count_vowels(s));\n'
                '    }\n'
                '}\n',
      'hint': 'Замыкание |x| x % 2 == 0 — как lambda x: x % 2 == 0; sum() и count() «съедают» итератор.',
      'expected': ['0: 0',
                   '1: 0',
                   '2: 4',
                   '10: 220',
                   '100: 171700',
                   'Hello World: 3',
                   'rhythm: 0',
                   'AEIOU: 5',
                   'Привет: 0',
                   'education: 5']},
     {'id': 'r1-gcd-lcm',
      'mode': 'rust',
      'title': 'НОД, НОК и защита от переполнения',
      'statement': 'Напишите fn gcd(a: u64, b: u64) -> u64 (алгоритм Евклида в цикле) и fn lcm(a: u64, b: '
                   'u64) -> Option<u64>: наименьшее общее кратное или None, если результат не помещается в '
                   'u64 (используйте checked_mul).',
      'starter': 'fn gcd(a: u64, b: u64) -> u64 {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn lcm(a: u64, b: u64) -> Option<u64> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{} {} {}", gcd(12, 18), gcd(17, 5), gcd(0, 9));\n'
                '    println!("{:?} {:?}", lcm(4, 6), lcm(0, 5));\n'
                '    println!("{:?}", lcm(1 << 40, (1 << 40) + 1));\n'
                '    println!("{:?}", lcm(u64::MAX, 2));\n'
                '}\n',
      'hint': 'lcm = a / gcd * b; умножение проверяйте методом checked_mul — он вернёт None при '
              'переполнении.',
      'expected': ['6 1 9', 'Some(12) Some(0)', 'None', 'None']},
     {'id': 'r1-to-base',
      'mode': 'rust',
      'title': 'Число в любой системе счисления',
      'statement': 'Напишите fn to_base(mut n: u32, base: u32) -> String: запись n в системе с основанием '
                   '2..=36, цифры 0-9 и a-z. Для 0 вернуть "0". Python: format(n, \'b\') и int(s, base); '
                   'здесь вы пишете это сами (char::from_digit).',
      'starter': 'fn to_base(mut n: u32, base: u32) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for (n, b) in [(0, 2), (5, 2), (255, 16), (255, 2), (123456, 36), (35, 36), (64, 8)] {\n'
                '        println!("{n} base {b}: {}", to_base(n, b));\n'
                '    }\n'
                '}\n',
      'hint': 'Остатки получаются от младшей цифры к старшей — соберите их в Vec и переверните rev().',
      'expected': ['0 base 2: 0',
                   '5 base 2: 101',
                   '255 base 16: ff',
                   '255 base 2: 11111111',
                   '123456 base 36: 2n9c',
                   '35 base 36: z',
                   '64 base 8: 100']}],
 2: [{'id': 'r2-drop-impl',
      'mode': 'rust',
      'title': 'Drop: убираем за собой',
      'statement': 'Тип Guard хранит имя. Реализуйте для него Drop так, чтобы при уничтожении печаталась '
                   'строка «drop <имя>». Остальное сделает компилятор: он сам вставит вызовы на закрывающих '
                   'скобках и в обратном порядке.',
      'starter': 'struct Guard {\n'
                 '    name: String,\n'
                 '}\n'
                 '\n'
                 'impl Drop for Guard {\n'
                 '    fn drop(&mut self) {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let _a = Guard { name: String::from("a") };\n'
                '    {\n'
                '        let _b = Guard { name: String::from("b") };\n'
                '        let _c = Guard { name: String::from("c") };\n'
                '        println!("inner");\n'
                '    }\n'
                '    let d = Guard { name: String::from("d") };\n'
                '    drop(d);\n'
                '    println!("end");\n'
                '}\n',
      'hint': 'В drop достаточно println!("drop {}", self.name); вызывать его самому не нужно.',
      'expected': ['inner', 'drop c', 'drop b', 'drop d', 'end', 'drop a']},
     {'id': 'r2-scope-order',
      'mode': 'rust',
      'title': 'Порядок уничтожения: режиссируем вывод',
      'statement': 'Тип Guard уже готов: new печатает «make <имя>», а при уничтожении печатается «drop '
                   '<имя>». Напишите функцию scenario(), чтобы программа напечатала ровно такие строки: make '
                   'a, make b, drop b, mid, make c, drop c, end, drop a. Подсказка: что-то нужно уничтожить '
                   'вручную, что-то — закрывающей скобкой блока.',
      'starter': "struct Guard(&'static str);\n"
                 '\n'
                 'impl Guard {\n'
                 "    fn new(name: &'static str) -> Guard {\n"
                 '        println!("make {name}");\n'
                 '        Guard(name)\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'impl Drop for Guard {\n'
                 '    fn drop(&mut self) {\n'
                 '        println!("drop {}", self.0);\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'fn scenario() {\n'
                 '    // ваш код\n'
                 '}\n',
      'driver': 'fn main() {\n    scenario();\n}\n',
      'hint': 'drop(b) уничтожает b сразу; внутренний блок { … } уничтожает c на своей скобке; a живёт до '
              'конца функции.',
      'expected': ['make a', 'make b', 'drop b', 'mid', 'make c', 'drop c', 'end', 'drop a']},
     {'id': 'r2-move-fix',
      'mode': 'rust',
      'title': 'Исправьте: значение использовано после переезда',
      'statement': 'Код не компилируется: let upper = name; перемещает строку, и дальше name использовать '
                   'нельзя. Исправьте describe так, чтобы функция возвращала «<исходная> -> <заглавными>»: '
                   'например, «rust -> RUST».',
      'starter': 'fn describe(name: String) -> String {\n'
                 '    let upper = name;\n'
                 '    format!("{} -> {}", name, upper.to_uppercase())\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", describe(String::from("rust")));\n'
                '    println!("{}", describe(String::from("привет")));\n'
                '}\n',
      'hint': 'Нужны две независимые строки — значит, одну из них создайте через .clone().',
      'expected': ['rust -> RUST', 'привет -> ПРИВЕТ']},
     {'id': 'r2-return-ownership',
      'mode': 'rust',
      'title': 'Вернуть владение: кортеж и цепочка',
      'statement': 'Функции забирают строку по значению. exclaim(s) дописывает в конец «!» и возвращает '
                   'строку. measure(s) возвращает пару (строка, длина в байтах), чтобы вызывающий не потерял '
                   'владение.',
      'starter': 'fn exclaim(s: String) -> String {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn measure(s: String) -> (String, usize) {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let s = String::from("привет");\n'
                '    let s = exclaim(s);\n'
                '    let (s, n) = measure(s);\n'
                '    println!("{s} {n}");\n'
                '    let (s, n) = measure(exclaim(s));\n'
                '    println!("{s} {n}");\n'
                '}\n',
      'hint': 'Параметр, который меняется, объявляют как mut s. Длину возьмите до того, как отдадите s в '
              'кортеж.',
      'expected': ['привет! 13', 'привет!! 14']},
     {'id': 'r2-array-copy',
      'mode': 'rust',
      'title': 'Массивы и кортежи копируются',
      'statement': 'Массив [i32; 4] и кортеж (i32, i32) целиком лежат на стеке и копируются побитно. '
                   'Напишите doubled(a) — массив с удвоенными элементами и swapped(p) — кортеж с '
                   'переставленными местами числами. После вызова исходные значения остаются доступными.',
      'starter': 'fn doubled(a: [i32; 4]) -> [i32; 4] {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn swapped(p: (i32, i32)) -> (i32, i32) {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let a = [1, 2, 3, 4];\n'
                '    let b = doubled(a);\n'
                '    println!("{:?} {:?}", a, b);\n'
                '    let p = (7, 9);\n'
                '    let q = swapped(p);\n'
                '    println!("{:?} {:?}", p, q);\n'
                '}\n',
      'hint': 'Параметр mut a — это локальная копия; исходный массив у вызывающего не меняется.',
      'expected': ['[1, 2, 3, 4] [2, 4, 6, 8]', '(7, 9) (9, 7)']},
     {'id': 'r2-derive-copy',
      'mode': 'rust',
      'title': 'Исправьте: сделайте Point копируемым',
      'statement': 'Код не компилируется: Point переезжает в shift, а потом используется снова. Тип состоит '
                   'из двух i32, поэтому его можно сделать Copy. Правьте только атрибут derive над '
                   'структурой (Debug нужен для вывода).',
      'starter': '#[derive(Debug)]\n'
                 'struct Point {\n'
                 '    x: i32,\n'
                 '    y: i32,\n'
                 '}\n'
                 '\n'
                 'fn shift(p: Point, dx: i32, dy: i32) -> Point {\n'
                 '    Point { x: p.x + dx, y: p.y + dy }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let p = Point { x: 1, y: 2 };\n'
                '    let q = shift(p, 10, 20);\n'
                '    println!("{:?} {:?}", p, q);\n'
                '    println!("{} байт", std::mem::size_of::<Point>());\n'
                '}\n',
      'hint': '#[derive(Debug, Clone, Copy)] — Copy требует и Clone.',
      'expected': ['Point { x: 1, y: 2 } Point { x: 11, y: 22 }', '8 байт']},
     {'id': 'r2-two-clones',
      'mode': 'rust',
      'title': 'Ровно два клона',
      'statement': 'Напишите triple(s) → (String, String, String): три одинаковые строки. Условие: в коде '
                   'ровно два вызова .clone() — третья строка получается перемещением самой s. Каждый лишний '
                   'клон — лишний malloc и memcpy.',
      'starter': 'fn triple(s: String) -> (String, String, String) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                '    println!("{:?}", triple(String::from("ab")));\n'
                '    let (x, y, z) = triple(String::from("xyz"));\n'
                '    println!("{}", x == y && y == z);\n'
                '    println!("clones: {}", bad0);\n'
                '}\n',
      'hint': 'Порядок важен: сначала клоны, а последним — сама s, которая переезжает в кортеж.',
      'expected': ['("ab", "ab", "ab")', 'true', 'clones: 2']},
     {'id': 'r2-box-new',
      'mode': 'rust',
      'title': 'Box: значение в куче',
      'statement': 'Напишите boxed_sum(a, b) → Box<i32> с суммой, положенной в кучу, и unbox_double(b: '
                   'Box<i32>) → i32: удвоенное значение из коробки (звёздочка разыменовывает Box).',
      'starter': 'fn boxed_sum(a: i32, b: i32) -> Box<i32> {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn unbox_double(b: Box<i32>) -> i32 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let b = boxed_sum(20, 22);\n'
                '    println!("{}", b);\n'
                '    println!("{}", unbox_double(b));\n'
                '    println!("{} {} {}", std::mem::size_of::<i32>(), std::mem::size_of::<Box<i32>>(), '
                'std::mem::size_of::<String>());\n'
                '}\n',
      'hint': 'Box::new(значение) кладёт значение в кучу; *b достаёт его обратно.',
      'expected': ['42', '84', '4 8 24']},
     {'id': 'r2-box-list',
      'mode': 'rust',
      'title': 'Список на Box: рекурсивный тип',
      'statement': 'Перечисление List хранит голову и хвост в Box. Напишите range_list(from, to) — список '
                   'from, from+1, …, to (включительно; пустой, если from > to), sum(list) — сумму, '
                   'to_vec(list) — элементы в порядке списка. Функции забирают список по значению.',
      'starter': 'enum List {\n'
                 '    Cons(i32, Box<List>),\n'
                 '    Nil,\n'
                 '}\n'
                 'use List::{Cons, Nil};\n'
                 '\n'
                 'fn range_list(from: i32, to: i32) -> List {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn sum(list: List) -> i32 {\n'
                 '    match list {\n'
                 '        Nil => todo!(),\n'
                 '        Cons(v, rest) => todo!(),\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'fn to_vec(list: List) -> Vec<i32> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", sum(range_list(1, 10)));\n'
                '    println!("{:?}", to_vec(range_list(3, 7)));\n'
                '    println!("{:?} {}", to_vec(range_list(5, 1)), sum(Nil));\n'
                '    println!("{}", std::mem::size_of::<Box<List>>());\n'
                '}\n',
      'hint': '*rest достаёт список из коробки и переносит владение; на Nil рекурсия заканчивается.',
      'expected': ['55', '[3, 4, 5, 6, 7]', '[] 0', '8']},
     {'id': 'r2-recursive-fix',
      'mode': 'rust',
      'title': 'Исправьте: тип бесконечного размера',
      'statement': 'Выражение Expr содержит другие выражения прямо внутри себя — размер такого типа '
                   'бесконечен, и код не собирается. Исправьте определение enum (функция eval и её *a, *b '
                   'уже написаны для Box).',
      'starter': 'enum Expr {\n'
                 '    Num(i64),\n'
                 '    Add(Expr, Expr),\n'
                 '    Mul(Expr, Expr),\n'
                 '}\n'
                 '\n'
                 'fn eval(e: Expr) -> i64 {\n'
                 '    match e {\n'
                 '        Expr::Num(n) => n,\n'
                 '        Expr::Add(a, b) => eval(*a) + eval(*b),\n'
                 '        Expr::Mul(a, b) => eval(*a) * eval(*b),\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    use Expr::*;\n'
                '    let e = Add(Box::new(Num(2)), Box::new(Mul(Box::new(Num(3)), Box::new(Num(4)))));\n'
                '    println!("{}", eval(e));\n'
                '    println!("{}", eval(Mul(Box::new(Num(-5)), Box::new(Num(6)))));\n'
                '}\n',
      'hint': 'Рекурсивные поля нужно положить в Box<Expr>: тогда размер определяется указателем.',
      'expected': ['14', '-30']},
     {'id': 'r2-field-order',
      'mode': 'rust',
      'title': 'Порядок полей — порядок drop',
      'statement': 'Поля структуры уничтожаются в порядке объявления. Сейчас при уничтожении Pair сначала '
                   'печатается «drop right». Измените определение структуры (конструктор new не трогайте) '
                   'так, чтобы сначала шло «drop left», а затем «drop right».',
      'starter': "struct Guard(&'static str);\n"
                 '\n'
                 'impl Guard {\n'
                 "    fn new(name: &'static str) -> Guard {\n"
                 '        println!("make {name}");\n'
                 '        Guard(name)\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'impl Drop for Guard {\n'
                 '    fn drop(&mut self) {\n'
                 '        println!("drop {}", self.0);\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'struct Pair {\n'
                 '    right: Guard,\n'
                 '    left: Guard,\n'
                 '}\n'
                 '\n'
                 'impl Pair {\n'
                 '    fn new() -> Pair {\n'
                 '        let left = Guard::new("left");\n'
                 '        let right = Guard::new("right");\n'
                 '        Pair { right, left }\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    {\n'
                '        let _p = Pair::new();\n'
                '        println!("alive");\n'
                '    }\n'
                '    println!("done");\n'
                '}\n',
      'hint': 'Поля структуры освобождаются сверху вниз, как они записаны в определении.',
      'expected': ['make left', 'make right', 'alive', 'drop left', 'drop right', 'done']},
     {'id': 'r2-option-take',
      'mode': 'rust',
      'title': 'Option::take: вынуть и оставить None',
      'statement': 'Структура Slot хранит необязательную строку. Реализуйте put(&mut self, s) — положить '
                   'строку и вернуть прежнюю (Option<String>), take(&mut self) — забрать строку, оставив '
                   'None, и is_empty(&self). Подсказка: у Option есть методы replace и take. Ссылки &self и '
                   '&mut self — тема следующей главы: пока считайте их разрешением читать или менять Slot на '
                   'месте.',
      'starter': 'struct Slot {\n'
                 '    item: Option<String>,\n'
                 '}\n'
                 '\n'
                 'impl Slot {\n'
                 '    fn put(&mut self, s: String) -> Option<String> {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn take(&mut self) -> Option<String> {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn is_empty(&self) -> bool {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut s = Slot { item: None };\n'
                '    println!("{:?}", s.put(String::from("a")));\n'
                '    println!("{:?}", s.put(String::from("b")));\n'
                '    println!("{:?}", s.take());\n'
                '    println!("{:?} {}", s.take(), s.is_empty());\n'
                '}\n',
      'hint': 'self.item.replace(s) и self.item.take() возвращают старое значение, не копируя его.',
      'expected': ['None', 'Some("a")', 'Some("b")', 'None true']},
     {'id': 'r2-mem-swap',
      'mode': 'rust',
      'title': 'mem::swap и mem::take',
      'statement': 'rotate(a, b, c) сдвигает значения по кругу: a получает значение b, b — значение c, c — '
                   'прежнее значение a. Копировать строки нельзя — используйте std::mem::swap. drain(log) '
                   'возвращает содержимое строки и оставляет её пустой (std::mem::take).',
      'starter': 'fn rotate(a: &mut String, b: &mut String, c: &mut String) {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn drain(log: &mut String) -> String {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut a = String::from("1");\n'
                '    let mut b = String::from("2");\n'
                '    let mut c = String::from("3");\n'
                '    rotate(&mut a, &mut b, &mut c);\n'
                '    println!("{a} {b} {c}");\n'
                '    let mut log = String::from("boot ok");\n'
                '    let got = drain(&mut log);\n'
                '    println!("{:?} {:?}", got, log);\n'
                '}\n',
      'hint': 'Два свопа подряд: сначала (a, b), затем (b, c). mem::take оставляет String::default(), то '
              'есть пустую строку.',
      'expected': ['2 3 1', '"boot ok" ""']},
     {'id': 'r2-rc-count',
      'mode': 'rust',
      'title': 'Rc: много владельцев одного значения',
      'statement': 'Напишите share(s, n) → Vec<Rc<String>> (n ≥ 1): вектор из n владельцев ОДНОЙ строки в '
                   'куче. Данные копироваться не должны: создайте один Rc, а остальные получите через '
                   'Rc::clone.',
      'starter': 'use std::rc::Rc;\n\nfn share(s: &str, n: usize) -> Vec<Rc<String>> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let v = share("hello", 4);\n'
                '    println!("{} {}", v.len(), Rc::strong_count(&v[0]));\n'
                '    println!("{}", v.iter().all(|r| Rc::ptr_eq(r, &v[0])));\n'
                '    println!("{}", v[3]);\n'
                '    drop(v);\n'
                '}\n',
      'hint': 'Rc::clone(&first) увеличивает счётчик и не копирует строку; последний владелец — сама first.',
      'expected': ['4 4', 'true', 'hello']},
     {'id': 'r2-rc-drop',
      'mode': 'rust',
      'title': 'Rc: уничтожение при последнем владельце',
      'statement': 'Guard печатает «drop shared», когда уничтожается. Напишите fan_out(g, n) → '
                   'Vec<Rc<Guard>> (n ≥ 1): n владельцев одного Guard, исходный g перемещается внутрь (клон '
                   'создаёт ещё одного владельца, перемещение — нет).',
      'starter': 'use std::rc::Rc;\n'
                 '\n'
                 "struct Guard(&'static str);\n"
                 '\n'
                 'impl Drop for Guard {\n'
                 '    fn drop(&mut self) {\n'
                 '        println!("drop {}", self.0);\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'fn fan_out(g: Rc<Guard>, n: usize) -> Vec<Rc<Guard>> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut v = fan_out(Rc::new(Guard("shared")), 3);\n'
                '    println!("owners: {}", Rc::strong_count(&v[0]));\n'
                '    v.pop();\n'
                '    println!("owners: {}", Rc::strong_count(&v[0]));\n'
                '    v.pop();\n'
                '    println!("owners: {}", Rc::strong_count(&v[0]));\n'
                '    println!("last");\n'
                '    v.pop();\n'
                '    println!("end");\n'
                '}\n',
      'hint': 'Значение уничтожается ровно один раз — когда счётчик достигает нуля. Лишних клонов быть не '
              'должно.',
      'expected': ['owners: 3', 'owners: 2', 'owners: 1', 'last', 'drop shared', 'end']},
     {'id': 'r2-loop-move',
      'mode': 'rust',
      'title': 'Исправьте: значение переехало в первой итерации',
      'statement': 'Функция repeat должна вернуть n копий строки. Компилятор ругается: s перемещена в push '
                   'на первой итерации цикла. Исправьте минимальной правкой.',
      'starter': 'fn repeat(s: String, n: usize) -> Vec<String> {\n'
                 '    let mut v = Vec::new();\n'
                 '    for _ in 0..n {\n'
                 '        v.push(s);\n'
                 '    }\n'
                 '    v\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", repeat(String::from("ab"), 3));\n'
                '    println!("{:?}", repeat(String::from("x"), 0));\n'
                '}\n',
      'hint': 'В каждую ячейку нужна своя строка: push(s.clone()).',
      'expected': ['["ab", "ab", "ab"]', '[]']},
     {'id': 'r2-index-move',
      'mode': 'rust',
      'title': 'Исправьте: нельзя вынуть элемент по индексу',
      'statement': 'split_first(names) → (String, Vec<String>): первое имя и оставшиеся. names[0] не '
                   'компилируется — из вектора нельзя вынуть владение по индексу. Исправьте, не используя '
                   'clone: у Vec есть метод, который удаляет элемент и отдаёт его владельцу.',
      'starter': 'fn split_first(mut names: Vec<String>) -> (String, Vec<String>) {\n'
                 '    let first = names[0];\n'
                 '    names.remove(0);\n'
                 '    (first, names)\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                '    let (first, rest) = split_first(vec![String::from("anna"), String::from("bob"), '
                'String::from("carl")]);\n'
                '    println!("first={first} rest={:?}", rest);\n'
                '    println!("clones: {}", bad0);\n'
                '}\n',
      'hint': 'remove(0) удаляет элемент и возвращает его — владение переходит к вам.',
      'expected': ['first=anna rest=["bob", "carl"]', 'clones: 0']},
     {'id': 'r2-pipeline',
      'mode': 'rust',
      'title': 'Конвейер: владение перетекает из функции в функцию',
      'statement': 'Напишите три функции, которые забирают вектор и возвращают его: append(v, x) — добавить '
                   'в конец; dedup_sorted(v) — отсортировать по возрастанию и убрать повторы; top(v, k) — '
                   'оставить k наибольших в порядке убывания.',
      'starter': 'fn append(v: Vec<i32>, x: i32) -> Vec<i32> {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn dedup_sorted(v: Vec<i32>) -> Vec<i32> {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn top(v: Vec<i32>, k: usize) -> Vec<i32> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let v = vec![5, 3, 5, 1, 9];\n'
                '    let v = append(append(v, 7), 3);\n'
                '    let v = dedup_sorted(v);\n'
                '    println!("{:?}", v);\n'
                '    println!("{:?}", top(v, 3));\n'
                '    println!("{:?}", top(dedup_sorted(vec![2, 2, 1]), 5));\n'
                '}\n',
      'hint': 'Параметр с mut можно менять внутри; после изменения верните его, и владение уйдёт дальше по '
              'цепочке.',
      'expected': ['[1, 3, 5, 7, 9]', '[9, 7, 5]', '[2, 1]']},
     {'id': 'r2-struct-update',
      'mode': 'rust',
      'title': 'Структура: пересобрать с новым полем',
      'statement': 'Config владеет строкой. with_name(c, name) возвращает конфигурацию с новым именем и '
                   'остальными полями прежними — используйте синтаксис обновления структуры «..c». '
                   'into_parts(c) разбирает конфигурацию на (имя, число попыток).',
      'starter': '#[derive(Debug)]\n'
                 'struct Config {\n'
                 '    name: String,\n'
                 '    retries: u32,\n'
                 '    verbose: bool,\n'
                 '}\n'
                 '\n'
                 'fn with_name(c: Config, name: &str) -> Config {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn into_parts(c: Config) -> (String, u32) {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let c = Config { name: String::from("old"), retries: 3, verbose: true };\n'
                '    let c = with_name(c, "new");\n'
                '    println!("{:?}", c);\n'
                '    println!("{:?}", into_parts(c));\n'
                '}\n',
      'hint': 'Config { name: ..., ..c } берёт недостающие поля из c; старое имя при этом просто '
              'уничтожится.',
      'expected': ['Config { name: "new", retries: 3, verbose: true }', '("new", 3)']},
     {'id': 'r2-shadow-drop',
      'mode': 'rust',
      'title': 'RAII: блокировка отпускается сама',
      'statement': 'Lock имитирует блокировку: Lock::acquire(name) печатает «lock <name>» и возвращает '
                   'значение, а при уничтожении печатается «unlock <name>». Реализуйте acquire и Drop. '
                   'Следите за затенением: второй let l не уничтожает первую блокировку.',
      'starter': 'struct Lock {\n'
                 '    name: String,\n'
                 '}\n'
                 '\n'
                 'impl Lock {\n'
                 '    fn acquire(name: &str) -> Lock {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'impl Drop for Lock {\n'
                 '    fn drop(&mut self) {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let l = Lock::acquire("A");\n'
                '    let l = Lock::acquire("B");\n'
                '    {\n'
                '        let _x = Lock::acquire("C");\n'
                '    }\n'
                '    println!("body {}", l.name);\n'
                '}\n',
      'hint': 'Затенение скрывает имя, но не уничтожает значение: A живёт до конца функции и освобождается '
              'последней.',
      'expected': ['lock A', 'lock B', 'lock C', 'unlock C', 'body B', 'unlock B', 'unlock A']},
     {'id': 'r2-underscore',
      'mode': 'rust',
      'title': 'Подчёркивание: _ и _name',
      'statement': 'Guard печатает «make <имя>» при создании и «drop <имя>» при уничтожении. Напишите '
                   'probe() так, чтобы вывод был: make temp, drop temp, make keep, body, drop keep. '
                   'Значение, присвоенное голому «_», уничтожается сразу; значение в переменной _keep живёт '
                   'до конца блока.',
      'starter': "struct Guard(&'static str);\n"
                 '\n'
                 'impl Guard {\n'
                 "    fn new(name: &'static str) -> Guard {\n"
                 '        println!("make {name}");\n'
                 '        Guard(name)\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'impl Drop for Guard {\n'
                 '    fn drop(&mut self) {\n'
                 '        println!("drop {}", self.0);\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'fn probe() {\n'
                 '    // ваш код\n'
                 '}\n',
      'driver': 'fn main() {\n    probe();\n}\n',
      'hint': 'let _ = … не создаёт привязки, значение умирает на этой же строке; let _keep = … привязку '
              'создаёт.',
      'expected': ['make temp', 'drop temp', 'make keep', 'body', 'drop keep']},
     {'id': 'r2-sizes',
      'mode': 'rust',
      'title': 'Copy или нет: три типа',
      'statement': 'Опишите три типа. Meters(f64) — копируемый. Segment { from: Meters, to: Meters } — тоже '
                   'копируемый. Label { text: String } — не копируемый (владеет кучей). Добавьте нужные '
                   'derive к определениям. Программа проверит Copy и напечатает размеры: 8, 24 и 16 байт.',
      'starter': 'struct Meters(f64);\n'
                 '\n'
                 'struct Segment {\n'
                 '    from: Meters,\n'
                 '    to: Meters,\n'
                 '}\n'
                 '\n'
                 'struct Label {\n'
                 '    text: String,\n'
                 '}\n',
      'driver': 'fn need_copy<T: Copy>(_: T) {}\n'
                '\n'
                'fn main() {\n'
                '    need_copy(Meters(1.5));\n'
                '    need_copy(Segment { from: Meters(0.0), to: Meters(2.0) });\n'
                '    let l = Label { text: String::from("a") };\n'
                '    let _m = l;\n'
                '    println!("{} {} {}", std::mem::size_of::<Meters>(), std::mem::size_of::<Label>(), '
                'std::mem::size_of::<Segment>());\n'
                '}\n',
      'hint': 'Copy можно получить только у типа, все поля которого Copy; для Copy нужен ещё и Clone: '
              '#[derive(Clone, Copy)].',
      'expected': ['8 24 16']},
     {'id': 'r2-capacity',
      'mode': 'rust',
      'title': 'Ёмкость растёт: String::push',
      'statement': 'Напишите capacity_trace(n) → Vec<usize>: создайте пустую String::new(), n раз добавьте '
                   "символ 'x' и верните все различные значения ёмкости (capacity) в порядке появления, "
                   'начиная с начальной. Видно, как буфер в куче растёт рывками, а не на каждом символе.',
      'starter': 'fn capacity_trace(n: usize) -> Vec<usize> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", capacity_trace(0));\n'
                '    println!("{:?}", capacity_trace(100));\n'
                '    println!("{:?}", capacity_trace(1000));\n'
                '}\n',
      'hint': 'Запоминайте последнее увиденное значение ёмкости и добавляйте новое только если оно '
              'изменилось.',
      'expected': ['[0]', '[0, 8, 16, 32, 64, 128]', '[0, 8, 16, 32, 64, 128, 256, 512, 1024]']},
     {'id': 'r2-move-ptr',
      'mode': 'rust',
      'title': 'Переезд не трогает кучу',
      'statement': 'as_ptr() возвращает адрес буфера в куче. move_keeps_buffer(s) переносит строку в новую '
                   'переменную и возвращает, остался ли адрес буфера тем же (true). clone_new_buffer(s) '
                   'клонирует строку и возвращает, отличается ли адрес копии от адреса оригинала (true).',
      'starter': 'fn move_keeps_buffer(s: String) -> bool {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn clone_new_buffer(s: String) -> bool {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", move_keeps_buffer(String::from("hello world")));\n'
                '    println!("{}", clone_new_buffer(String::from("hello world")));\n'
                '}\n',
      'hint': 'Запомните s.as_ptr() до переезда и сравните с as_ptr() у новой переменной.',
      'expected': ['true', 'true']},
     {'id': 'r2-stack-list',
      'mode': 'rust',
      'title': 'Стек на связном списке из Box',
      'statement': 'Реализуйте стек на односвязном списке. Stack::new() — пустой; push(v) кладёт значение в '
                   'начало; pop() снимает и возвращает Option<i32>; peek(&self) показывает верхнее без '
                   'снятия. Хранится голова Option<Box<Node>>: при push старую голову забирайте через '
                   'take().',
      'starter': 'struct Node {\n'
                 '    val: i32,\n'
                 '    next: Option<Box<Node>>,\n'
                 '}\n'
                 '\n'
                 'struct Stack {\n'
                 '    head: Option<Box<Node>>,\n'
                 '}\n'
                 '\n'
                 'impl Stack {\n'
                 '    fn new() -> Stack {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn push(&mut self, v: i32) {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn pop(&mut self) -> Option<i32> {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn peek(&self) -> Option<i32> {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut s = Stack::new();\n'
                '    println!("{:?} {:?}", s.pop(), s.peek());\n'
                '    for i in 1..=4 {\n'
                '        s.push(i * 10);\n'
                '    }\n'
                '    println!("{:?}", s.peek());\n'
                '    println!("{:?} {:?}", s.pop(), s.pop());\n'
                '    s.push(99);\n'
                '    let mut out = Vec::new();\n'
                '    while let Some(v) = s.pop() {\n'
                '        out.push(v);\n'
                '    }\n'
                '    println!("{:?} {:?}", out, s.peek());\n'
                '}\n',
      'hint': 'push: let old = self.head.take(); затем self.head = Some(Box::new(Node { val: v, next: old '
              '})). pop: take() и перенос n.next в head.',
      'expected': ['None None', 'Some(40)', 'Some(40) Some(30)', '[99, 20, 10] None']},
     {'id': 'r2-reverse-list',
      'mode': 'rust',
      'title': 'Разворот списка перемещениями',
      'statement': 'Напишите reverse(head) → Option<Box<Node>>: разверните односвязный список, не создавая '
                   'новых узлов и не клонируя — только переставляя указатели (владение узлов переходит по '
                   'цепочке). Условие: ни одного .clone().',
      'starter': 'struct Node {\n'
                 '    val: i32,\n'
                 '    next: Option<Box<Node>>,\n'
                 '}\n'
                 '\n'
                 'fn reverse(head: Option<Box<Node>>) -> Option<Box<Node>> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn build(v: &[i32]) -> Option<Box<Node>> {\n'
                '    let mut head = None;\n'
                '    for &x in v.iter().rev() {\n'
                '        head = Some(Box::new(Node { val: x, next: head }));\n'
                '    }\n'
                '    head\n'
                '}\n'
                '\n'
                'fn dump(mut l: Option<Box<Node>>) -> Vec<i32> {\n'
                '    let mut out = Vec::new();\n'
                '    while let Some(n) = l {\n'
                '        out.push(n.val);\n'
                '        l = n.next;\n'
                '    }\n'
                '    out\n'
                '}\n'
                '\n'
                'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                '    println!("{:?}", dump(reverse(build(&[1, 2, 3, 4, 5]))));\n'
                '    println!("{:?}", dump(reverse(build(&[7]))));\n'
                '    println!("{:?}", dump(reverse(build(&[]))));\n'
                '    println!("clones: {}", bad0);\n'
                '}\n',
      'hint': 'Идём по списку: отцепляем хвост через node.next.take(), направляем next на уже развёрнутую '
              'часть, и node становится новой головой.',
      'expected': ['[5, 4, 3, 2, 1]', '[7]', '[]', 'clones: 0']},
     {'id': 'r2-bst-insert',
      'mode': 'rust',
      'title': 'Двоичное дерево на Option<Box<…>>',
      'statement': 'Узел дерева владеет левым и правым поддеревом через Option<Box<TNode>>. Напишите '
                   'insert(link, key) → Link: вставка в дерево поиска (повторы игнорируются), функция '
                   'забирает дерево и возвращает его обратно; и in_order(link, out) — обход слева направо с '
                   'записью ключей в out. Подсказка: поддерево перед рекурсией забирайте через take().',
      'starter': 'struct TNode {\n'
                 '    key: i32,\n'
                 '    left: Link,\n'
                 '    right: Link,\n'
                 '}\n'
                 '\n'
                 'type Link = Option<Box<TNode>>;\n'
                 '\n'
                 'fn insert(link: Link, key: i32) -> Link {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn in_order(link: Link, out: &mut Vec<i32>) {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut root: Link = None;\n'
                '    for k in [5, 3, 8, 1, 4, 7, 9, 3, 5] {\n'
                '        root = insert(root, k);\n'
                '    }\n'
                '    let mut out = Vec::new();\n'
                '    in_order(root, &mut out);\n'
                '    println!("{:?}", out);\n'
                '    let mut empty = Vec::new();\n'
                '    in_order(None, &mut empty);\n'
                '    println!("{}", empty.len());\n'
                '}\n',
      'hint': 'Some(mut n) → сравните ключи, перезапишите n.left или n.right результатом '
              'insert(n.left.take(), key) и верните Some(n).',
      'expected': ['[1, 3, 4, 5, 7, 8, 9]', '0']},
     {'id': 'r2-rc-tail',
      'mode': 'rust',
      'title': 'Rc: общий хвост у двух списков',
      'statement': 'Cons-список, у которого хвост лежит в Rc. Напишите shared_tail() → (Rc<List>, Rc<List>, '
                   'Rc<List>): хвост [10] и два списка a = 1 → хвост, b = 2 → хвост, которые делят один '
                   'хвост без копирования (вернуть кортеж (tail, a, b)). И sum(&List) — сумма элементов.',
      'starter': 'use std::rc::Rc;\n'
                 '\n'
                 'enum List {\n'
                 '    Cons(i32, Rc<List>),\n'
                 '    Nil,\n'
                 '}\n'
                 'use List::{Cons, Nil};\n'
                 '\n'
                 'fn shared_tail() -> (Rc<List>, Rc<List>, Rc<List>) {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn sum(l: &List) -> i32 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let (tail, a, b) = shared_tail();\n'
                '    println!("{}", Rc::strong_count(&tail));\n'
                '    println!("{} {} {}", sum(&tail), sum(&a), sum(&b));\n'
                '    drop(a);\n'
                '    println!("{}", Rc::strong_count(&tail));\n'
                '}\n',
      'hint': 'Хвост создайте один раз и в каждый из двух списков отдайте Rc::clone(&tail): счётчик хвоста '
              'станет 3.',
      'expected': ['3', '10 11 12', '2']},
     {'id': 'r2-sizeof',
      'mode': 'rust',
      'title': 'Размеры типов: стек и куча',
      'statement': 'Напишите sizes() → [usize; 7]: std::mem::size_of для типов u8, i32, Box<i32>, String, '
                   'Vec<u8>, Option<Box<i32>>, Option<i32> — именно в этом порядке. Обратите внимание на 24 '
                   'байта у String и Vec (три слова) и на то, что Option<Box<i32>> не толще указателя.',
      'starter': 'fn sizes() -> [usize; 7] {\n    todo!()\n}\n',
      'driver': 'fn main() {\n    println!("{:?}", sizes());\n}\n',
      'hint': 'size_of::<Тип>() — дженерик-функция из std::mem; тип пишут в угловых скобках.',
      'expected': ['[1, 4, 8, 24, 24, 8, 8]']},
     {'id': 'r2-moved-args',
      'mode': 'rust',
      'title': 'Исправьте: аргументы переехали в longest',
      'statement': 'report возвращает «<самая длинная> (из <a> и <b>)». Но longest забирает обе строки, и в '
                   'format! их уже нет. Исправьте report: нужны ровно два клона, а longest менять не нужно.',
      'starter': 'fn longest(a: String, b: String) -> String {\n'
                 '    if a.len() >= b.len() { a } else { b }\n'
                 '}\n'
                 '\n'
                 'fn report(a: String, b: String) -> String {\n'
                 '    let winner = longest(a, b);\n'
                 '    format!("{winner} (из {a} и {b})")\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                '    println!("{}", report(String::from("apple"), String::from("fig")));\n'
                '    println!("{}", report(String::from("kiwi"), String::from("plum")));\n'
                '    println!("clones: {}", bad0);\n'
                '}\n',
      'hint': 'longest(a.clone(), b.clone()) отдаёт функции копии, а оригиналы остаются у report.',
      'expected': ['apple (из apple и fig)', 'kiwi (из kiwi и plum)', 'clones: 2']}],
 3: [{'id': 'r3-count-vowels',
      'mode': 'rust',
      'title': 'Заём для чтения: &str',
      'statement': 'Напишите count_vowels(s: &str) -> usize: сколько в строке гласных. Гласные — русские а е '
                   'ё и о у ы э ю я и латинские a e i o u, регистр не важен. Функция только читает: после '
                   'вызова строка остаётся у владельца.',
      'starter': 'fn count_vowels(s: &str) -> usize {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let s = String::from("Привет, Rust");\n'
                '    println!("{}", count_vowels(&s));\n'
                '    println!("{s}");\n'
                '    println!("{} {}", count_vowels("ЁЖ AEIOU"), count_vowels(""));\n'
                '}\n',
      'hint': 's.chars() перебирает символы; to_lowercase() у char возвращает итератор — возьмите первый '
              'символ через .next().unwrap().',
      'expected': ['3', 'Привет, Rust', '6 0']},
     {'id': 'r3-add-all',
      'mode': 'rust',
      'title': '&mut Vec и срез: пишем через ссылку',
      'statement': 'Напишите add_all(dst: &mut Vec<i32>, extra: &[i32]): дописать в конец dst все элементы '
                   'среза extra (копируя числа). Вызывающий передаёт &mut v и &[..]: в вызове сразу видно, '
                   'кто читается, а кто меняется.',
      'starter': 'fn add_all(dst: &mut Vec<i32>, extra: &[i32]) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let mut v = vec![1];\n'
                '    add_all(&mut v, &[2, 3]);\n'
                '    add_all(&mut v, &[]);\n'
                '    let more = vec![4, 5];\n'
                '    add_all(&mut v, &more);\n'
                '    println!("{:?} {:?}", v, more);\n'
                '}\n',
      'hint': 'for &x in extra даёт числа по значению (i32 — Copy); затем dst.push(x).',
      'expected': ['[1, 2, 3, 4, 5] [4, 5]']},
     {'id': 'r3-swap-ends',
      'mode': 'rust',
      'title': 'Меняем концы среза',
      'statement': 'Напишите swap_ends(v: &mut [i32]): поменять местами первый и последний элементы среза. '
                   'Для пустого среза и среза из одного элемента ничего не делать. Функция должна принимать '
                   'и массив, и вектор, и часть вектора.',
      'starter': 'fn swap_ends(v: &mut [i32]) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let mut a = [1, 2, 3, 4];\n'
                '    swap_ends(&mut a);\n'
                '    let mut v = vec![10, 20, 30];\n'
                '    swap_ends(&mut v);\n'
                '    swap_ends(&mut v[1..]);\n'
                '    let mut one = [7];\n'
                '    swap_ends(&mut one);\n'
                '    let mut none: [i32; 0] = [];\n'
                '    swap_ends(&mut none);\n'
                '    println!("{:?} {:?} {:?} {:?}", a, v, one, none);\n'
                '}\n',
      'hint': 'У среза есть метод swap(i, j); не забудьте про длину меньше двух.',
      'expected': ['[4, 2, 3, 1] [30, 10, 20] [7] []']},
     {'id': 'r3-fix-two-mut',
      'mode': 'rust',
      'title': 'Исправьте: две изменяемые ссылки сразу',
      'statement': 'Компилятор не даёт держать две изменяемые ссылки на один вектор одновременно. Исправьте '
                   'build так, чтобы он возвращал [1, 2], оставив работу через &mut: заём должен закончиться '
                   'до того, как начнётся следующий.',
      'starter': 'fn build() -> Vec<i32> {\n'
                 '    let mut v = Vec::new();\n'
                 '    let a = &mut v;\n'
                 '    let b = &mut v;\n'
                 '    a.push(1);\n'
                 '    b.push(2);\n'
                 '    v\n'
                 '}\n',
      'driver': 'fn main() {\n    println!("{:?}", build());\n}\n',
      'hint': 'Первая ссылка живёт до последнего использования: используйте её полностью, и только потом '
              'берите вторую.',
      'expected': ['[1, 2]']},
     {'id': 'r3-fix-read-push',
      'mode': 'rust',
      'title': 'Исправьте: ссылка на элемент и push',
      'statement': 'grow_with_first должна дописать в конец вектора сначала число 100, а затем копию его '
                   'первого элемента. Код не компилируется: ссылка first ещё жива, когда вызывается '
                   'push(100). Исправьте минимально: число можно скопировать из-под ссылки.',
      'starter': 'fn grow_with_first(v: &mut Vec<i32>) {\n'
                 '    let first = &v[0];\n'
                 '    v.push(100);\n'
                 '    v.push(*first);\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut v = vec![5, 7];\n'
                '    grow_with_first(&mut v);\n'
                '    println!("{:?}", v);\n'
                '    grow_with_first(&mut v);\n'
                '    println!("{:?}", v);\n'
                '}\n',
      'hint': 'let first = v[0]; — i32 копируется, заём сразу заканчивается.',
      'expected': ['[5, 7, 100, 5]', '[5, 7, 100, 5, 100, 5]']},
     {'id': 'r3-fix-dangle',
      'mode': 'rust',
      'title': 'Исправьте: ссылка на локальную строку',
      'statement': 'greeting строит строку «Привет, <имя>!» и пытается вернуть ссылку на неё, но локальная '
                   'строка уничтожается при выходе из функции. Исправьте: верните владение, а не ссылку.',
      'starter': 'fn greeting(name: &str) -> &str {\n    let s = format!("Привет, {name}!");\n    &s\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", greeting("Rust"));\n'
                '    let g = greeting("мир");\n'
                '    println!("{} ({} байт)", g, g.len());\n'
                '}\n',
      'hint': 'Тип результата — String; последнее выражение функции может быть самим format!.',
      'expected': ['Привет, Rust!', 'Привет, мир! (21 байт)']},
     {'id': 'r3-longest',
      'mode': 'rust',
      'title': 'Время жизни: longest',
      'statement': "Напишите longest<'a>(a: &'a str, b: &'a str) -> &'a str: вернуть более длинную строку "
                   '(по байтам); при равной длине — первую. Результат — ссылка на один из аргументов, а не '
                   'новая строка.',
      'starter': "fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {\n    todo!()\n}\n",
      'driver': 'fn main() {\n'
                '    let s1 = String::from("abcd");\n'
                '    let n;\n'
                '    {\n'
                '        let s2 = String::from("xyz");\n'
                '        n = longest(&s1, &s2).len();\n'
                '    }\n'
                '    println!("{n}");\n'
                '    println!("{} {}", longest("aa", "bb"), longest("привет", "hello"));\n'
                '}\n',
      'hint': "Сравните len() и верните ту ссылку, которая подходит; аннотации 'a уже в сигнатуре.",
      'expected': ['4', 'aa привет']},
     {'id': 'r3-first-word',
      'mode': 'rust',
      'title': 'Срез первого слова',
      'statement': 'Напишите first_word(s: &str) -> &str: первое слово — подряд идущие непробельные символы; '
                   'ведущие пробельные символы пропускаются; если слов нет, вернуть пустую строку. Результат '
                   '— срез исходной строки, а не новая строка.',
      'starter': 'fn first_word(s: &str) -> &str {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for s in ["hello world", "  padded  text", "", "   ", "один", "тут много слов"] {\n'
                '        println!("{:?}", first_word(s));\n'
                '    }\n'
                '    let owned = String::from("take me home");\n'
                '    let w = first_word(&owned);\n'
                '    println!("{} {}", w, w.as_ptr() == owned.as_ptr());\n'
                '}\n',
      'hint': 'split_whitespace().next() возвращает Option<&str>; unwrap_or("") даёт пустой срез.',
      'expected': ['"hello"', '"padded"', '""', '""', '"один"', '"тут"', 'take true']},
     {'id': 'r3-lifetime-fix',
      'mode': 'rust',
      'title': 'Исправьте: нет времени жизни у результата',
      'statement': 'pick(a, b, first) возвращает a или b в зависимости от флага. Компилятор не знает, к '
                   'какому аргументу привязан результат. Допишите параметр времени жизни в сигнатуру.',
      'starter': 'fn pick(a: &str, b: &str, first: bool) -> &str {\n    if first { a } else { b }\n}\n',
      'driver': 'fn main() {\n'
                '    let x = String::from("левая");\n'
                '    let y = String::from("правая");\n'
                '    println!("{} {}", pick(&x, &y, true), pick(&x, &y, false));\n'
                '}\n',
      'hint': "fn pick<'a>(a: &'a str, b: &'a str, first: bool) -> &'a str.",
      'expected': ['левая правая']},
     {'id': 'r3-slice-split',
      'mode': 'rust',
      'title': 'Две половины одного среза',
      'statement': 'Напишите halves(v: &[i32]) -> (&[i32], &[i32]): левая половина длиной len/2 (округление '
                   'вниз) и остаток. Данные не копируются: обе части — срезы исходного.',
      'starter': 'fn halves(v: &[i32]) -> (&[i32], &[i32]) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let v = vec![1, 2, 3, 4, 5];\n'
                '    let (l, r) = halves(&v);\n'
                '    println!("{:?} {:?}", l, r);\n'
                '    println!("{} {}", l.as_ptr() == v.as_ptr(), r.as_ptr() == v[2..].as_ptr());\n'
                '    println!("{:?}", halves(&[]));\n'
                '    println!("{:?}", halves(&[9]));\n'
                '}\n',
      'hint': 'У среза есть метод split_at(mid), который возвращает пару срезов.',
      'expected': ['[1, 2] [3, 4, 5]', 'true true', '([], [])', '([], [9])']},
     {'id': 'r3-max-mut',
      'mode': 'rust',
      'title': 'Option<&mut T>: ссылка на максимум',
      'statement': 'Напишите max_mut(v: &mut [i32]) -> Option<&mut i32>: изменяемая ссылка на наибольший '
                   'элемент (None для пустого среза). Через неё вызывающий сможет записать в массив новое '
                   'значение.',
      'starter': 'fn max_mut(v: &mut [i32]) -> Option<&mut i32> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let mut v = [3, 9, 2];\n'
                '    if let Some(m) = max_mut(&mut v) {\n'
                '        *m = 0;\n'
                '    }\n'
                '    println!("{:?}", v);\n'
                '    if let Some(m) = max_mut(&mut v) {\n'
                '        *m += 100;\n'
                '    }\n'
                '    println!("{:?}", v);\n'
                '    println!("{:?}", max_mut(&mut []));\n'
                '}\n',
      'hint': 'iter_mut() выдаёт &mut i32; max_by_key(|x| **x) выбирает наибольший, не копируя элементы.',
      'expected': ['[3, 0, 2]', '[103, 0, 2]', 'None']},
     {'id': 'r3-fix-nll',
      'mode': 'rust',
      'title': 'Исправьте: прочитали, а потом push',
      'statement': 'log_and_grow возвращает последний элемент вектора и добавляет в конец 100. Ссылка last '
                   'ещё нужна, когда вызывается push. Исправьте так, чтобы функция вернула последний элемент '
                   'ДО добавления (для [1, 2] вернуть 2).',
      'starter': 'fn log_and_grow(v: &mut Vec<i32>) -> i32 {\n'
                 '    let last = v.last().unwrap();\n'
                 '    v.push(100);\n'
                 '    *last\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut v = vec![1, 2];\n'
                '    println!("{}", log_and_grow(&mut v));\n'
                '    println!("{}", log_and_grow(&mut v));\n'
                '    println!("{:?}", v);\n'
                '}\n',
      'hint': 'Достаточно разыменовать сразу: let last = *v.last().unwrap(); — заём закончится на этой '
              'строке.',
      'expected': ['2', '100', '[1, 2, 100, 100]']},
     {'id': 'r3-iter-kinds',
      'mode': 'rust',
      'title': 'Три способа обойти вектор',
      'statement': 'sum_ref(v: &Vec<i32>) → сумма (цикл по ссылке); double_in_place(v: &mut Vec<i32>) — '
                   'удвоить все элементы на месте (изменяемые ссылки); consume(v: Vec<i32>) → i32 — сумма с '
                   'забором элементов (вектор уничтожается).',
      'starter': 'fn sum_ref(v: &Vec<i32>) -> i32 {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn double_in_place(v: &mut Vec<i32>) {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn consume(v: Vec<i32>) -> i32 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut v = vec![1, 2, 3];\n'
                '    println!("{}", sum_ref(&v));\n'
                '    double_in_place(&mut v);\n'
                '    println!("{:?}", v);\n'
                '    println!("{}", consume(v));\n'
                '}\n',
      'hint': 'for x in v (v: &Vec) даёт &i32; v.iter_mut() — &mut i32 (значение меняют через *x); for x in '
              'v (v: Vec) — i32.',
      'expected': ['6', '[2, 4, 6]', '12']},
     {'id': 'r3-parser',
      'mode': 'rust',
      'title': "Структура со ссылкой: Parser<'a>",
      'statement': 'Parser хранит срез текста и позицию. Parser::new(text) создаёт разборщик; next_word(&mut '
                   'self) возвращает следующее слово (непробельные символы) как срез ИСХОДНОГО текста или '
                   'None, когда слов больше нет. Слова должны жить столько же, сколько текст, а не столько, '
                   "сколько сам разборщик (&'a str в результате).",
      'starter': "struct Parser<'a> {\n"
                 "    text: &'a str,\n"
                 '    pos: usize,\n'
                 '}\n'
                 '\n'
                 "impl<'a> Parser<'a> {\n"
                 "    fn new(text: &'a str) -> Parser<'a> {\n"
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 "    fn next_word(&mut self) -> Option<&'a str> {\n"
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let text = String::from("  hello   rust world ");\n'
                '    let mut words = Vec::new();\n'
                '    {\n'
                '        let mut p = Parser::new(&text);\n'
                '        while let Some(w) = p.next_word() {\n'
                '            words.push(w);\n'
                '        }\n'
                '    }\n'
                '    println!("{:?}", words);\n'
                '    let mut q = Parser::new("привет мир");\n'
                '    println!("{:?} {:?} {:?}", q.next_word(), q.next_word(), q.next_word());\n'
                '    println!("{:?}", Parser::new("   ").next_word());\n'
                '}\n',
      'hint': 'Ищите начало слова после trim_start, конец — по первому пробельному символу; сдвигайте '
              'self.pos за слово.',
      'expected': ['["hello", "rust", "world"]', 'Some("привет") Some("мир") None', 'None']},
     {'id': 'r3-method-forms',
      'mode': 'rust',
      'title': 'Три формы self',
      'statement': 'Counter считает события. new() — со нулём; get(&self) читает значение; inc(&mut self) '
                   'увеличивает на 1; finish(self) забирает счётчик и возвращает итог. Выберите для каждого '
                   'метода нужную форму: после finish использовать счётчик уже нельзя.',
      'starter': 'struct Counter {\n'
                 '    n: u32,\n'
                 '}\n'
                 '\n'
                 'impl Counter {\n'
                 '    fn new() -> Counter {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn get(&self) -> u32 {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn inc(&mut self) {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn finish(self) -> u32 {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut c = Counter::new();\n'
                '    println!("{}", c.get());\n'
                '    c.inc();\n'
                '    c.inc();\n'
                '    c.inc();\n'
                '    println!("{}", c.get());\n'
                '    println!("{}", c.finish());\n'
                '}\n',
      'hint': 'Сигнатуры уже даны: &self читает, &mut self меняет поле через self.n += 1, self передаёт поле '
              'дальше.',
      'expected': ['0', '3', '3']},
     {'id': 'r3-fix-method-self',
      'mode': 'rust',
      'title': 'Исправьте: метод меняет поле через &self',
      'statement': 'add должен увеличить количество монет, но метод принимает &self — менять поле через '
                   'разделяемую ссылку нельзя. Исправьте сигнатуру метода (вызывающий код уже использует let '
                   'mut).',
      'starter': 'struct Wallet {\n'
                 '    coins: u32,\n'
                 '}\n'
                 '\n'
                 'impl Wallet {\n'
                 '    fn add(&self, n: u32) {\n'
                 '        self.coins += n;\n'
                 '    }\n'
                 '\n'
                 '    fn total(&self) -> u32 {\n'
                 '        self.coins\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut w = Wallet { coins: 1 };\n'
                '    w.add(4);\n'
                '    w.add(5);\n'
                '    println!("{}", w.total());\n'
                '}\n',
      'hint': 'fn add(&mut self, n: u32) — изменяемая ссылка на self.',
      'expected': ['10']},
     {'id': 'r3-swap-values',
      'mode': 'rust',
      'title': 'Обмен через две &mut без mem::swap',
      'statement': 'Напишите swap_values(a: &mut i32, b: &mut i32): поменять значения местами, не используя '
                   'std::mem::swap и метод swap. Две &mut на РАЗНЫЕ значения проверщик допускает; в '
                   'вызывающем коде обе переменные объявлены mut.',
      'starter': 'fn swap_values(a: &mut i32, b: &mut i32) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!("sw", "ap(")).count();\n'
                '    let mut x = 1;\n'
                '    let mut y = 2;\n'
                '    swap_values(&mut x, &mut y);\n'
                '    println!("{x} {y}");\n'
                '    swap_values(&mut x, &mut y);\n'
                '    println!("{x} {y}");\n'
                '    println!("swap calls: {}", bad0);\n'
                '}\n',
      'hint': 'Нужна временная переменная: tmp = *a; *a = *b; *b = tmp;',
      'expected': ['2 1', '1 2', 'swap calls: 0']},
     {'id': 'r3-reborrow',
      'mode': 'rust',
      'title': 'Перезаимствование: передаём &mut дальше',
      'statement': 'bump(x: &mut i32) прибавляет единицу — он уже готов. Напишите bump_n(x: &mut i32, n: '
                   'u32): вызвать bump ровно n раз с тем же x. &mut не копируется, но передача в функцию '
                   'создаёт временный заём, и x можно использовать снова.',
      'starter': 'fn bump(x: &mut i32) {\n'
                 '    *x += 1;\n'
                 '}\n'
                 '\n'
                 'fn bump_n(x: &mut i32, n: u32) {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut v = 10;\n'
                '    bump_n(&mut v, 5);\n'
                '    println!("{v}");\n'
                '    bump_n(&mut v, 0);\n'
                '    bump(&mut v);\n'
                '    println!("{v}");\n'
                '}\n',
      'hint': 'В цикле просто пишите bump(x); — каждый вызов заимствует x на время вызова.',
      'expected': ['15', '16']},
     {'id': 'r3-split-halves-mut',
      'mode': 'rust',
      'title': 'split_at_mut: два писателя, разные части',
      'statement': 'Напишите reshape(v: &mut [i32]): левую половину (len/2 элементов) обнулить, а каждый '
                   'элемент правой половины заменить суммой соответствующих исходных элементов левой и '
                   'правой (для пары i: right[i] = left_old[i] + right_old[i]; если правая половина длиннее, '
                   'лишний последний остаётся прежним). Используйте split_at_mut: две изменяемые ссылки на '
                   'непересекающиеся части разрешены.',
      'starter': 'fn reshape(v: &mut [i32]) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let mut a = [1, 2, 3, 4, 5, 6];\n'
                '    reshape(&mut a);\n'
                '    println!("{:?}", a);\n'
                '    let mut b = vec![5, 6, 7];\n'
                '    reshape(&mut b);\n'
                '    println!("{:?}", b);\n'
                '    let mut c: Vec<i32> = vec![];\n'
                '    reshape(&mut c);\n'
                '    println!("{:?}", c);\n'
                '}\n',
      'hint': 'let (left, right) = v.split_at_mut(mid); — обе части можно менять одновременно.',
      'expected': ['[0, 0, 0, 5, 7, 9]', '[0, 11, 7]', '[]']},
     {'id': 'r3-fix-iter-invalidate',
      'mode': 'rust',
      'title': 'Исправьте: изменяем вектор во время обхода',
      'statement': 'dup_evens дописывает в конец вектора копии всех чётных чисел (порядок: исходные '
                   'элементы, затем копии чётных в исходном порядке). Цикл по &v держит заём, а push меняет '
                   'вектор — не компилируется. Исправьте: сначала соберите копии, потом добавьте.',
      'starter': 'fn dup_evens(mut v: Vec<i32>) -> Vec<i32> {\n'
                 '    for x in &v {\n'
                 '        if x % 2 == 0 {\n'
                 '            v.push(*x);\n'
                 '        }\n'
                 '    }\n'
                 '    v\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", dup_evens(vec![1, 2, 3, 4]));\n'
                '    println!("{:?}", dup_evens(vec![]));\n'
                '    println!("{:?}", dup_evens(vec![7, 9]));\n'
                '}\n',
      'hint': 'Заведите отдельный вектор extra, заполните его в цикле, а после цикла вызовите '
              'v.extend(extra).',
      'expected': ['[1, 2, 3, 4, 2, 4]', '[]', '[7, 9]']},
     {'id': 'r3-initial-char',
      'mode': 'rust',
      'title': 'Срез по границе символа',
      'statement': 'initial(s: &str) -> &str возвращает первый символ строки как срез (пустая строка → '
                   'пустой срез). Заготовка берёт один БАЙТ и падает на кириллице: границы среза обязаны '
                   'попадать на границу символа UTF-8. Исправьте.',
      'starter': 'fn initial(s: &str) -> &str {\n    &s[..1]\n}\n',
      'driver': 'fn main() {\n'
                '    for s in ["rust", "привет", "Ёж", "", "я"] {\n'
                '        println!("{:?}", initial(s));\n'
                '    }\n'
                '}\n',
      'hint': 'char_indices() выдаёт пары (байтовое смещение, символ): смещение второго символа — конец '
              'первого; если второго нет, подойдёт вся строка.',
      'expected': ['"r"', '"п"', '"Ё"', '""', '"я"']},
     {'id': 'r3-stack-addr',
      'mode': 'rust',
      'title': 'Стек растёт вниз',
      'statement': 'Напишите inner(outer: usize) -> bool с атрибутом #[inline(never)]: заведите локальную '
                   'переменную, получите её адрес (as *const u64 as usize) и верните, меньше ли он адреса '
                   'outer. И grows_down() -> bool: локальная переменная, её адрес передаётся в inner. '
                   'Результат должен быть true: кадр вложенного вызова лежит ниже. Значения оберните в '
                   'std::hint::black_box, чтобы оптимизатор их не убрал.',
      'starter': '#[inline(never)]\n'
                 'fn inner(outer: usize) -> bool {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn grows_down() -> bool {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n    println!("{}", grows_down());\n}\n',
      'hint': 'let y = black_box(0u64); let ay = &y as *const u64 as usize; — то же в grows_down; в inner '
              'сравнивайте ay < outer.',
      'expected': ['true']},
     {'id': 'r3-ptr-eq',
      'mode': 'rust',
      'title': 'Равны значения или это один объект',
      'statement': 'same_text(a, b) — true, если строки равны по содержимому (==). same_object(a, b) — true, '
                   'только если обе ссылки указывают на ОДИН объект в памяти (std::ptr::eq). Это аналоги == '
                   'и is из питона.',
      'starter': 'fn same_text(a: &String, b: &String) -> bool {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn same_object(a: &String, b: &String) -> bool {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let x = String::from("hi");\n'
                '    let y = String::from("hi");\n'
                '    println!("{} {}", same_text(&x, &y), same_object(&x, &y));\n'
                '    println!("{} {}", same_text(&x, &x), same_object(&x, &x));\n'
                '}\n',
      'hint': 'a == b сравнивает значения за ссылками; ptr::eq(a, b) — сами адреса.',
      'expected': ['true false', 'true true']},
     {'id': 'r3-trim-all',
      'mode': 'rust',
      'title': 'Срезы в векторе: trim_all',
      'statement': "Напишите trim_all<'a>(lines: &[&'a str]) -> Vec<&'a str>: вектор срезов, каждый обрезан "
                   'по краям от пробельных символов. Новых строк не создаётся — только срезы исходных строк, '
                   "поэтому результат живёт столько же, сколько исходные тексты (время жизни 'a).",
      'starter': "fn trim_all<'a>(lines: &[&'a str]) -> Vec<&'a str> {\n    todo!()\n}\n",
      'driver': 'fn main() {\n'
                '    let text = String::from("  alpha \\n beta\\t");\n'
                "    let parts: Vec<&str> = text.split('\\n').collect();\n"
                '    let t = trim_all(&parts);\n'
                '    println!("{:?}", t);\n'
                '    println!("{:?}", trim_all(&["  ", "x ", ""]));\n'
                '}\n',
      'hint': "s.trim() у &'a str возвращает &'a str; соберите результат через map(...).collect().",
      'expected': ['["alpha", "beta"]', '["", "x", ""]']},
     {'id': 'r3-longest-word',
      'mode': 'rust',
      'title': 'Самое длинное слово',
      'statement': 'Напишите longest_word(text: &str) -> &str: самое длинное слово текста (слова разделены '
                   'пробельными символами; длина — в символах, не в байтах; при равенстве — первое; пустой '
                   'текст → ""). Верните срез текста.',
      'starter': 'fn longest_word(text: &str) -> &str {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", longest_word("a bb ccc dd"));\n'
                '    println!("{:?}", longest_word("привет мир кот"));\n'
                '    println!("{:?}", longest_word("ab cd"));\n'
                '    println!("{:?}", longest_word("  "));\n'
                '}\n',
      'hint': 'Храните лучший срез в переменной типа &str и заменяйте её, когда нашли слово длиннее по '
              'chars().count().',
      'expected': ['"ccc"', '"привет"', '"ab"', '""']},
     {'id': 'r3-struct-ref-fix',
      'mode': 'rust',
      'title': 'Исправьте: у структуры со ссылкой нет времени жизни',
      'statement': 'Highlight хранит срез текста и смещение, mark(text, from, to) строит выделение. '
                   'Компилятор требует указать время жизни. Допишите параметры в определение структуры и в '
                   'сигнатуру функции.',
      'starter': 'struct Highlight {\n'
                 '    text: &str,\n'
                 '    start: usize,\n'
                 '}\n'
                 '\n'
                 'fn mark(text: &str, from: usize, to: usize) -> Highlight {\n'
                 '    Highlight { text: &text[from..to], start: from }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let doc = String::from("borrow checker is strict");\n'
                '    let h = mark(&doc, 7, 14);\n'
                '    println!("{} @ {}", h.text, h.start);\n'
                '}\n',
      'hint': "struct Highlight<'a> { text: &'a str, … } и fn mark<'a>(text: &'a str, …) -> Highlight<'a>.",
      'expected': ['checker @ 7']},
     {'id': 'r3-fix-outlive',
      'mode': 'rust',
      'title': 'Исправьте: значение живёт недостаточно долго',
      'statement': 'outer_len сравнивает входную строку с временной строкой и возвращает длину большей. '
                   'Ссылка result переживает временную строку b, и компилятор отказывается собирать код. '
                   'Исправьте, не меняя longest и не выводя b за пределы блока: длину нужно взять, пока b '
                   'ещё жива.',
      'starter': "fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {\n"
                 '    if a.len() >= b.len() { a } else { b }\n'
                 '}\n'
                 '\n'
                 'fn outer_len(a: &str) -> usize {\n'
                 '    let result;\n'
                 '    {\n'
                 '        let b = String::from("temporary");\n'
                 '        result = longest(a, &b);\n'
                 '    }\n'
                 '    result.len()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", outer_len("hi"));\n'
                '    println!("{}", outer_len("a longer phrase here"));\n'
                '}\n',
      'hint': 'Замените result на число: n = longest(a, &b).len(); внутри блока.',
      'expected': ['9', '20']},
     {'id': 'r3-longest-row',
      'mode': 'rust',
      'title': 'Ссылка на самую длинную строку сетки',
      'statement': 'grid — вектор строк (векторов). longest_row(grid: &[Vec<i32>]) -> Option<&Vec<i32>> '
                   'возвращает ссылку на самую длинную строку (при равенстве — первую; пустая сетка → None). '
                   'push_to_longest(grid: &mut [Vec<i32>], x) добавляет x в конец той же самой строки '
                   '(первой из самых длинных).',
      'starter': 'fn longest_row(grid: &[Vec<i32>]) -> Option<&Vec<i32>> {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn push_to_longest(grid: &mut [Vec<i32>], x: i32) {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut grid = vec![vec![1], vec![2, 3], vec![4, 5], vec![]];\n'
                '    println!("{:?}", longest_row(&grid));\n'
                '    push_to_longest(&mut grid, 9);\n'
                '    println!("{:?}", grid);\n'
                '    println!("{:?}", longest_row(&[]));\n'
                '    let mut empty: Vec<Vec<i32>> = vec![];\n'
                '    push_to_longest(&mut empty, 1);\n'
                '    println!("{:?}", empty);\n'
                '}\n',
      'hint': 'Для push нужен индекс: найдите его читающим обходом (заём закончится), а потом возьмите &mut '
              'grid[i].',
      'expected': ['Some([2, 3])', '[[1], [2, 3, 9], [4, 5], []]', 'None', '[]']},
     {'id': 'r3-first-negative',
      'mode': 'rust',
      'title': 'Option<&mut i32>: первое отрицательное',
      'statement': 'Напишите first_negative(v: &mut [i32]) -> Option<&mut i32>: изменяемая ссылка на первый '
                   'отрицательный элемент (None, если таких нет). Через неё вызывающий исправляет значение '
                   'прямо в массиве.',
      'starter': 'fn first_negative(v: &mut [i32]) -> Option<&mut i32> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let mut v = [3, -1, 4, -5];\n'
                '    while let Some(x) = first_negative(&mut v) {\n'
                '        *x = 0;\n'
                '    }\n'
                '    println!("{:?}", v);\n'
                '    println!("{:?}", first_negative(&mut [1, 2]));\n'
                '}\n',
      'hint': 'iter_mut().find(|x| **x < 0): в замыкании x имеет тип &&mut i32, поэтому две звёздочки.',
      'expected': ['[3, 0, 4, 0]', 'None']},
     {'id': 'r3-fix-report',
      'mode': 'rust',
      'title': 'Исправьте: ссылка на первый элемент и clear',
      'statement': 'report(names) возвращает строку «первое — <имя>; осталось <N>» и очищает вектор. Ссылка '
                   'first на элемент вектора ещё нужна, когда вектор очищается. Исправьте: сделайте '
                   'независимую копию имени.',
      'starter': 'fn report(names: &mut Vec<String>) -> String {\n'
                 '    let first = &names[0];\n'
                 '    names.clear();\n'
                 '    format!("первое — {}; осталось {}", first, names.len())\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut names = vec![String::from("anna"), String::from("bob")];\n'
                '    println!("{}", report(&mut names));\n'
                '    println!("{:?}", names);\n'
                '}\n',
      'hint': 'names[0].clone() даёт новую String, не связанную с вектором.',
      'expected': ['первое — anna; осталось 0', '[]']}],
 4: [{'id': 'r4-point-new',
      'mode': 'rust',
      'title': 'Структура и методы: Point',
      'statement': 'Опишите методы Point: origin() — точка (0, 0); new(x, y); manhattan(&self, other: '
                   '&Point) → |dx| + |dy|; translate(&mut self, dx, dy) — сдвинуть на месте.',
      'starter': 'struct Point {\n'
                 '    x: i32,\n'
                 '    y: i32,\n'
                 '}\n'
                 '\n'
                 'impl Point {\n'
                 '    fn origin() -> Point {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn new(x: i32, y: i32) -> Point {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn manhattan(&self, other: &Point) -> i32 {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn translate(&mut self, dx: i32, dy: i32) {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let o = Point::origin();\n'
                '    let mut p = Point::new(3, -4);\n'
                '    println!("{}", p.manhattan(&o));\n'
                '    p.translate(-3, 4);\n'
                '    println!("{} {} {}", p.x, p.y, p.manhattan(&o));\n'
                '}\n',
      'hint': 'Сокращённая запись поля: Point { x, y }, если имена параметров совпадают с именами полей.',
      'expected': ['7', '0 0 0']},
     {'id': 'r4-rect-methods',
      'mode': 'rust',
      'title': 'Прямоугольник: &self, &mut self',
      'statement': 'Rect { w, h } (u32). Методы: area(&self), perimeter(&self), is_square(&self), '
                   'can_hold(&self, other: &Rect) — помещается ли other целиком (обе стороны строго меньше '
                   'или равны) и scale(&mut self, k: u32) — умножить обе стороны на k.',
      'starter': 'struct Rect {\n'
                 '    w: u32,\n'
                 '    h: u32,\n'
                 '}\n'
                 '\n'
                 'impl Rect {\n'
                 '    fn area(&self) -> u32 {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn perimeter(&self) -> u32 {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn is_square(&self) -> bool {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn can_hold(&self, other: &Rect) -> bool {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn scale(&mut self, k: u32) {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut r = Rect { w: 4, h: 3 };\n'
                '    let small = Rect { w: 2, h: 2 };\n'
                '    println!("{} {} {}", r.area(), r.perimeter(), r.is_square());\n'
                '    println!("{} {}", r.can_hold(&small), small.can_hold(&r));\n'
                '    r.scale(2);\n'
                '    println!("{} {}", r.w, r.h);\n'
                '    println!("{}", Rect { w: 5, h: 5 }.is_square());\n'
                '}\n',
      'hint': 'В can_hold сравнивайте обе стороны: self.w >= other.w && self.h >= other.h.',
      'expected': ['12 14 false', 'true false', '8 6', 'true']},
     {'id': 'r4-derive-debug',
      'mode': 'rust',
      'title': 'derive: Debug, Clone, PartialEq, Default',
      'statement': 'Код не собирается: драйвер печатает User через {:?}, клонирует, сравнивает через == и '
                   'создаёт значение по умолчанию. Добавьте над структурой один атрибут derive с нужными '
                   'четырьмя именами.',
      'starter': 'struct User {\n    name: String,\n    age: u32,\n    active: bool,\n}\n',
      'driver': 'fn main() {\n'
                '    let u = User { name: String::from("Анна"), age: 30, active: true };\n'
                '    let v = u.clone();\n'
                '    println!("{:?}", u);\n'
                '    println!("{}", u == v);\n'
                '    let d = User::default();\n'
                '    println!("{:?} {}", d, d == u);\n'
                '    println!("{:#?}", v);\n'
                '}\n',
      'hint': '#[derive(Debug, Clone, PartialEq, Default)] — все поля уже умеют всё это, поэтому derive '
              'сработает.',
      'expected': ['User { name: "Анна", age: 30, active: true }',
                   'true',
                   'User { name: "", age: 0, active: false } false',
                   'User {',
                   '    name: "Анна",',
                   '    age: 30,',
                   '    active: true,',
                   '}']},
     {'id': 'r4-display-impl',
      'mode': 'rust',
      'title': 'Display вручную',
      'statement': 'Реализуйте std::fmt::Display: для Point — «(x, y)»; для Temp — «21.5°C» или «70.7°F» '
                   '(одно знак после запятой). Тогда работают {} и to_string().',
      'starter': 'use std::fmt;\n'
                 '\n'
                 'struct Point {\n'
                 '    x: i32,\n'
                 '    y: i32,\n'
                 '}\n'
                 '\n'
                 'enum Temp {\n'
                 '    C(f64),\n'
                 '    F(f64),\n'
                 '}\n'
                 '\n'
                 'impl fmt::Display for Point {\n'
                 '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'impl fmt::Display for Temp {\n'
                 '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let p = Point { x: 3, y: -1 };\n'
                '    println!("{} [{:>10}]", p, p.to_string());\n'
                '    println!("{} {}", Temp::C(21.5), Temp::F(70.66));\n'
                '}\n',
      'hint': 'write!(f, "({}, {})", self.x, self.y); для Temp — match self { Temp::C(t) => write!(...), ... '
              '}.',
      'expected': ['(3, -1) [   (3, -1)]', '21.5°C 70.7°F']},
     {'id': 'r4-repr-c',
      'mode': 'rust',
      'title': 'Выравнивание: repr(C) и порядок полей',
      'statement': 'Три структуры с полями u8, u32, u8. Tight — по умолчанию (раст сам переставляет поля): 8 '
                   'байт. Wide — те же поля, но в раскладке языка си (#[repr(C)]): 12 байт. Packed — '
                   '#[repr(C)], но поля расположите так, чтобы размер стал 8. Заготовка даёт для всех трёх '
                   'размер 8: исправьте Wide и Packed.',
      'starter': 'struct Tight {\n'
                 '    a: u8,\n'
                 '    b: u32,\n'
                 '    c: u8,\n'
                 '}\n'
                 '\n'
                 'struct Wide {\n'
                 '    a: u8,\n'
                 '    b: u32,\n'
                 '    c: u8,\n'
                 '}\n'
                 '\n'
                 'struct Packed {\n'
                 '    a: u8,\n'
                 '    b: u32,\n'
                 '    c: u8,\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    use std::mem::{align_of, size_of};\n'
                '    println!("{} {} {}", size_of::<Tight>(), size_of::<Wide>(), size_of::<Packed>());\n'
                '    println!("{}", align_of::<Wide>());\n'
                '}\n',
      'hint': 'В repr(C) поля идут по порядку, и после каждого вставляется выравнивание: u8, [3 пустых], '
              'u32, u8, [3 пустых] = 12. Поставьте u32 первым.',
      'expected': ['8 12 8', '4']},
     {'id': 'r4-enum-shape',
      'mode': 'rust',
      'title': 'enum Shape: площадь и периметр',
      'statement': 'Shape — Circle(r), Rect(w, h) или Tri(a, b, c) (стороны). area(&self) → f64 (для '
                   'треугольника — формула Герона), perimeter(&self) → f64. π берите из '
                   'std::f64::consts::PI.',
      'starter': 'use std::f64::consts::PI;\n'
                 '\n'
                 'enum Shape {\n'
                 '    Circle(f64),\n'
                 '    Rect(f64, f64),\n'
                 '    Tri(f64, f64, f64),\n'
                 '}\n'
                 '\n'
                 'impl Shape {\n'
                 '    fn area(&self) -> f64 {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn perimeter(&self) -> f64 {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let shapes = [Shape::Circle(1.0), Shape::Rect(3.0, 4.0), Shape::Tri(3.0, 4.0, 5.0)];\n'
                '    for s in &shapes {\n'
                '        println!("{:.2} {:.2}", s.area(), s.perimeter());\n'
                '    }\n'
                '}\n',
      'hint': 'match self даёт привязки-ссылки: r, w, h — это &f64, арифметика с ними работает.',
      'expected': ['3.14 6.28', '12.00 14.00', '6.00 12.00']},
     {'id': 'r4-enum-size',
      'mode': 'rust',
      'title': 'Размеры перечислений',
      'statement': 'Напишите sizes() → [usize; 6]: size_of для Dir (перечисление из четырёх вариантов без '
                   'данных), Option<u8>, Option<u32>, Option<Box<i32>>, Option<&str>, Result<u8, u8> — в '
                   'этом порядке. Подумайте, где нужен тег, а где его заменяет ниша.',
      'starter': 'enum Dir {\n'
                 '    N,\n'
                 '    E,\n'
                 '    S,\n'
                 '    W,\n'
                 '}\n'
                 '\n'
                 'fn sizes() -> [usize; 6] {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let _ = [Dir::N, Dir::E, Dir::S, Dir::W];\n'
                '    println!("{:?}", sizes());\n'
                '}\n',
      'hint': 'size_of::<Тип>() из std::mem; Option<&str> — это срез (16 байт) с нишей в указателе.',
      'expected': ['[1, 2, 8, 8, 16, 2]']},
     {'id': 'r4-match-coin',
      'mode': 'rust',
      'title': 'match: монеты',
      'statement': 'enum Coin { Penny, Nickel, Dime, Quarter(u32) } — у четвертака есть год чеканки. '
                   'cents(&Coin) → u32: 1, 5, 10 и 25; но четвертак до 1980 года (не включая) считается '
                   'коллекционным и стоит 100. total(&[Coin]) → u32 — сумма.',
      'starter': 'enum Coin {\n'
                 '    Penny,\n'
                 '    Nickel,\n'
                 '    Dime,\n'
                 '    Quarter(u32),\n'
                 '}\n'
                 '\n'
                 'fn cents(c: &Coin) -> u32 {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn total(coins: &[Coin]) -> u32 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let v = [Coin::Penny, Coin::Dime, Coin::Quarter(1999), Coin::Quarter(1960), '
                'Coin::Nickel];\n'
                '    println!("{}", total(&v));\n'
                '    println!("{} {}", cents(&Coin::Quarter(1980)), cents(&Coin::Quarter(1979)));\n'
                '    println!("{}", total(&[]));\n'
                '}\n',
      'hint': 'Ветвь с охраной Quarter(year) if *year < 1980 должна идти раньше общей Quarter(_).',
      'expected': ['141', '25 100', '0']},
     {'id': 'r4-match-ranges',
      'mode': 'rust',
      'title': 'match: диапазоны, | , @ и охрана',
      'statement': 'classify(n: i32) → String одним match: отрицательное → "negative"; 0 → "zero"; цифра '
                   '1..=9 → "digit N" (с самим числом); 10, 20 или 30 → "round"; остальные чётные → "even"; '
                   'прочие → "odd".',
      'starter': 'fn classify(n: i32) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for n in [-5, 0, 7, 20, 14, 15, 100, 11] {\n'
                '        println!("{n}: {}", classify(n));\n'
                '    }\n'
                '}\n',
      'hint': 'Порядок ветвей важен: специальные случаи выше общих. Шаблон d @ 1..=9 привязывает число к '
              'имени d.',
      'expected': ['-5: negative',
                   '0: zero',
                   '7: digit 7',
                   '20: round',
                   '14: even',
                   '15: odd',
                   '100: even',
                   '11: odd']},
     {'id': 'r4-match-tuple',
      'mode': 'rust',
      'title': 'match по кортежу: FizzBuzz без if',
      'statement': 'fizzbuzz(n: u32) → String одним match по паре (n % 3, n % 5): «FizzBuzz», «Fizz», «Buzz» '
                   'или само число. Слово if в коде использовать нельзя.',
      'starter': 'fn fizzbuzz(n: u32) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!("i", "f ")).count();\n'
                '    let line: Vec<String> = (1..=15).map(fizzbuzz).collect();\n'
                '    println!("{}", line.join(" "));\n'
                '    println!("{} {}", fizzbuzz(30), fizzbuzz(31));\n'
                '    println!("ifs: {}", bad0);\n'
                '}\n',
      'hint': 'Образец (0, _) означает: остаток по 3 равен нулю, остаток по 5 не важен.',
      'expected': ['1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz', 'FizzBuzz 31', 'ifs: 0']},
     {'id': 'r4-match-slice',
      'mode': 'rust',
      'title': 'Образцы на срезах',
      'statement': 'describe(v: &[i32]) → String одним match с образцами срезов: пустой → "empty"; один '
                   'элемент → "one: X"; два → "two: A, B"; больше → "many: FIRST..LAST" (первый и '
                   'последний).',
      'starter': 'fn describe(v: &[i32]) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", describe(&[]));\n'
                '    println!("{}", describe(&[7]));\n'
                '    println!("{}", describe(&[1, 2]));\n'
                '    println!("{}", describe(&[1, 2, 3, 4, 5]));\n'
                '    println!("{}", describe(&vec![9, 8, 7]));\n'
                '}\n',
      'hint': 'Образец [first, .., last] подходит срезу из двух и более элементов; двухэлементный образец '
              'поставьте раньше.',
      'expected': ['empty', 'one: 7', 'two: 1, 2', 'many: 1..5', 'many: 9..7']},
     {'id': 'r4-option-div',
      'mode': 'rust',
      'title': 'Option и оператор ?',
      'statement': 'safe_div(a, b) → Option<i32> (None при b == 0). parse_pair(s) → Option<(i32, i32)>: '
                   'строка вида "3,4" (без пробелов), любая ошибка → None. ratio(s) → Option<i32>: разобрать '
                   'пару и безопасно разделить; здесь используйте оператор ?. Вызов unwrap() запрещён.',
      'starter': 'fn safe_div(a: i32, b: i32) -> Option<i32> {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn parse_pair(s: &str) -> Option<(i32, i32)> {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn ratio(s: &str) -> Option<i32> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!("unw", "rap(")).count();\n'
                '    for s in ["12,4", "7,0", "x,1", "5", "-9,3", "1,2,3"] {\n'
                '        println!("{:?}", ratio(s));\n'
                '    }\n'
                '    println!("{:?} {:?}", safe_div(1, 0), parse_pair("8,2"));\n'
                '    println!("unwraps: {}", bad0);\n'
                '}\n',
      'hint': 'l.parse::<i32>().ok()? превращает Result в Option и сразу возвращает None при ошибке; '
              "split_once(',') тоже Option.",
      'expected': ['Some(3)', 'None', 'None', 'None', 'Some(-3)', 'None', 'None Some((8, 2))', 'unwraps: 0']},
     {'id': 'r4-option-combinators',
      'mode': 'rust',
      'title': 'Комбинаторы Option без match',
      'statement': 'first_even_square(v) → Option<i32>: квадрат первого чётного числа. name_len(name: '
                   'Option<&str>) → usize: длина имени или 0. parse_or(s, default) → i32: число из строки '
                   'или default. Условие: ни match, ни if let — только методы Option и Result (map, '
                   'and_then, unwrap_or, find...).',
      'starter': 'fn first_even_square(v: &[i32]) -> Option<i32> {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn name_len(name: Option<&str>) -> usize {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn parse_or(s: &str, default: i32) -> i32 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!("mat", "ch ")).count();\n'
                '    let bad1 = src.matches(concat!("if ", "let ")).count();\n'
                '    println!("{:?} {:?}", first_even_square(&[3, 5, 6, 8]), first_even_square(&[1, 3]));\n'
                '    println!("{} {}", name_len(Some("Анна")), name_len(None));\n'
                '    println!("{} {} {}", parse_or(" 42 ", 0), parse_or("abc", -1), parse_or("", 7));\n'
                '    println!("banned: {} {}", bad0, bad1);\n'
                '}\n',
      'hint': 'find возвращает Option<&i32>; map превращает значение внутри. Для разбора строки: '
              's.trim().parse().unwrap_or(default).',
      'expected': ['Some(36) None', '8 0', '42 -1 7', 'banned: 0 0']},
     {'id': 'r4-let-else',
      'mode': 'rust',
      'title': 'let else и if let',
      'statement': 'parse_kv(line) → String: строка вида "ключ=значение"; через let else разобрать по '
                   'первому «=», иначе вернуть "bad"; результат — «ключ -> значение» (обе части с '
                   'обрезанными пробелами). show(o: Option<i32>) → String: «got N», если число есть, иначе '
                   '«nothing» — через if let / else.',
      'starter': 'fn parse_kv(line: &str) -> String {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn show(o: Option<i32>) -> String {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", parse_kv("name = rust"));\n'
                '    println!("{}", parse_kv("novalue"));\n'
                '    println!("{}", parse_kv("a=b=c"));\n'
                '    println!("{} {}", show(Some(5)), show(None));\n'
                '}\n',
      'hint': 'let Some((k, v)) = … else { return …; }; — после этой строки k и v уже обычные срезы.',
      'expected': ['name -> rust', 'bad', 'a -> b=c', 'got 5 nothing']},
     {'id': 'r4-rpn',
      'mode': 'rust',
      'title': 'Стек и while let: обратная польская запись',
      'statement': 'eval_rpn(tokens: &[&str]) → Option<i64>: вычислить выражение в обратной польской записи: '
                   'числа и операторы + - * /. Стек — Vec<i64>. None, если не хватает операндов, делитель '
                   'равен нулю, токен не распознан или в конце на стеке не ровно одно число.',
      'starter': 'fn eval_rpn(tokens: &[&str]) -> Option<i64> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", eval_rpn(&["3", "4", "+", "2", "*"]));\n'
                '    println!("{:?}", eval_rpn(&["5", "1", "2", "+", "4", "*", "+", "3", "-"]));\n'
                '    println!("{:?}", eval_rpn(&["1", "+"]));\n'
                '    println!("{:?}", eval_rpn(&["4", "0", "/"]));\n'
                '    println!("{:?}", eval_rpn(&["1", "2"]));\n'
                '    println!("{:?}", eval_rpn(&["x"]));\n'
                '    println!("{:?}", eval_rpn(&[]));\n'
                '}\n',
      'hint': 'Для оператора достаньте b = pop()?, затем a = pop()? (порядок!). Остальные токены разберите '
              'как числа через parse().ok()?.',
      'expected': ['Some(14)', 'Some(14)', 'None', 'None', 'None', 'None', 'None']},
     {'id': 'r4-state-machine',
      'mode': 'rust',
      'title': 'Автомат состояний: дверь',
      'statement': 'Door — Open, Closed, Locked(код). apply(self, Action) → Door: Open + Close → Closed; '
                   'Closed + Open → Open; Closed + Lock(c) → Locked(c); Locked(c) + Unlock(x) → Closed, если '
                   'x == c, иначе остаётся Locked(c). Любое другое действие — состояние не меняется. Метод '
                   'принимает self по значению.',
      'starter': '#[derive(Debug, PartialEq)]\n'
                 'enum Door {\n'
                 '    Open,\n'
                 '    Closed,\n'
                 '    Locked(u32),\n'
                 '}\n'
                 '\n'
                 'enum Action {\n'
                 '    Open,\n'
                 '    Close,\n'
                 '    Lock(u32),\n'
                 '    Unlock(u32),\n'
                 '}\n'
                 '\n'
                 'impl Door {\n'
                 '    fn apply(self, action: Action) -> Door {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    use Action::*;\n'
                '    let mut d = Door::Open;\n'
                '    for a in [Lock(1), Close, Lock(1234), Open, Unlock(1), Unlock(1234), Open] {\n'
                '        d = d.apply(a);\n'
                '        println!("{:?}", d);\n'
                '    }\n'
                '    println!("{}", Door::Closed.apply(Close) == Door::Closed);\n'
                '}\n',
      'hint': 'Матч по паре (self, action) читается как таблица переходов; последняя ветвь (state, _) => '
              'state возвращает прежнее состояние.',
      'expected': ['Open',
                   'Closed',
                   'Locked(1234)',
                   'Locked(1234)',
                   'Locked(1234)',
                   'Closed',
                   'Open',
                   'true']},
     {'id': 'r4-direction',
      'mode': 'rust',
      'title': 'enum без данных: Direction',
      'statement': 'Direction — N, E, S, W (derive Debug, Clone, Copy, PartialEq). turn_right(self), '
                   'turn_left(self), opposite(self), from_char(c: char) → Option<Direction> (буквы N E S W в '
                   'любом регистре) и to_char(self) → char (заглавная).',
      'starter': '#[derive(Debug, Clone, Copy, PartialEq)]\n'
                 'enum Direction {\n'
                 '    N,\n'
                 '    E,\n'
                 '    S,\n'
                 '    W,\n'
                 '}\n'
                 '\n'
                 'impl Direction {\n'
                 '    fn turn_right(self) -> Direction {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn turn_left(self) -> Direction {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn opposite(self) -> Direction {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn from_char(c: char) -> Option<Direction> {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn to_char(self) -> char {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut d = Direction::N;\n'
                '    for _ in 0..5 {\n'
                '        print!("{} ", d.to_char());\n'
                '        d = d.turn_right();\n'
                '    }\n'
                '    println!();\n'
                '    println!("{:?} {:?}", Direction::W.turn_left(), Direction::E.opposite());\n'
                '    println!("{:?} {:?} {:?}", Direction::from_char(\'s\'), Direction::from_char(\'W\'), '
                "Direction::from_char('x'));\n"
                '}\n',
      'hint': 'Тип Copy: self по значению можно использовать повторно. opposite — два поворота направо.',
      'expected': ['N E S W N', 'S W', 'Some(S) Some(W) None']},
     {'id': 'r4-fix-match-ref',
      'mode': 'rust',
      'title': 'Исправьте: нельзя переместить из заимствованного',
      'statement': 'display_name возвращает прозвище, а если его нет — имя. Метод получает &Person, а match '
                   'пытается ПЕРЕМЕСТИТЬ строку из поля за ссылкой. Исправьте так, чтобы Person остался у '
                   'владельца.',
      'starter': 'struct Person {\n'
                 '    name: String,\n'
                 '    nickname: Option<String>,\n'
                 '}\n'
                 '\n'
                 'fn display_name(p: &Person) -> String {\n'
                 '    match p.nickname {\n'
                 '        Some(n) => n,\n'
                 '        None => p.name.clone(),\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let a = Person { name: String::from("Александр"), nickname: Some(String::from("Саша")) '
                '};\n'
                '    let b = Person { name: String::from("Борис"), nickname: None };\n'
                '    println!("{} {}", display_name(&a), display_name(&b));\n'
                '    println!("{} {}", a.name, display_name(&a));\n'
                '}\n',
      'hint': 'match &p.nickname даёт привязку n: &String; вернуть нужно владельца — n.clone().',
      'expected': ['Саша Борис', 'Александр Саша']},
     {'id': 'r4-match-mut',
      'mode': 'rust',
      'title': 'Изменение внутри Option',
      'statement': 'increment_if_some(o: &mut Option<i32>) — прибавить 1, если значение есть. take_or(o: '
                   '&mut Option<String>, default: &str) → String: забрать значение из o (в o остаётся None) '
                   'или вернуть default. append_default(o: &mut Option<Vec<i32>>, x) — добавить x в вектор; '
                   'если вектора ещё нет, создать.',
      'starter': 'fn increment_if_some(o: &mut Option<i32>) {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn take_or(o: &mut Option<String>, default: &str) -> String {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn append_default(o: &mut Option<Vec<i32>>, x: i32) {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut a = Some(5);\n'
                '    let mut b: Option<i32> = None;\n'
                '    increment_if_some(&mut a);\n'
                '    increment_if_some(&mut b);\n'
                '    println!("{:?} {:?}", a, b);\n'
                '    let mut s = Some(String::from("hi"));\n'
                '    println!("{} {} {:?}", take_or(&mut s, "def"), take_or(&mut s, "def"), s);\n'
                '    let mut v = None;\n'
                '    append_default(&mut v, 1);\n'
                '    append_default(&mut v, 2);\n'
                '    println!("{:?}", v);\n'
                '}\n',
      'hint': 'if let Some(x) = o даёт x: &mut i32 (match ergonomics); o.take() и get_or_insert_with '
              'избавляют от лишних match.',
      'expected': ['Some(6) None', 'hi def None', 'Some([1, 2])']},
     {'id': 'r4-fix-move-in-match',
      'mode': 'rust',
      'title': 'Исправьте: значение переехало в match',
      'statement': 'describe сначала разбирает msg через match, а затем печатает его же через {:?}. match '
                   'перемещает строку из варианта, и msg после него недоступно. Исправьте минимальной '
                   'правкой (data нужны и текст, и сам msg).',
      'starter': 'fn describe(msg: Option<String>) -> String {\n'
                 '    let text = match msg {\n'
                 '        Some(s) => s,\n'
                 '        None => String::from("пусто"),\n'
                 '    };\n'
                 '    format!("{text} ({:?})", msg)\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", describe(Some(String::from("привет"))));\n'
                '    println!("{}", describe(None));\n'
                '}\n',
      'hint': 'match &msg разбирает ссылку: привязка s — &String, а msg остаётся целым.',
      'expected': ['привет (Some("привет"))', 'пусто (None)']},
     {'id': 'r4-expr-eval',
      'mode': 'rust',
      'title': 'Дерево выражений: eval',
      'statement': 'Expr — Num(i64), Add, Mul (по два Box<Expr>) и Neg (один). Напишите eval(e: &Expr) → i64 '
                   'рекурсивным match. Ссылка на Box<Expr> автоматически приводится к &Expr, так что eval(a) '
                   'работает.',
      'starter': 'enum Expr {\n'
                 '    Num(i64),\n'
                 '    Add(Box<Expr>, Box<Expr>),\n'
                 '    Mul(Box<Expr>, Box<Expr>),\n'
                 '    Neg(Box<Expr>),\n'
                 '}\n'
                 '\n'
                 'fn eval(e: &Expr) -> i64 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn num(n: i64) -> Box<Expr> {\n'
                '    Box::new(Expr::Num(n))\n'
                '}\n'
                '\n'
                'fn main() {\n'
                '    let e = Expr::Add(num(2), Box::new(Expr::Mul(num(3), Box::new(Expr::Neg(num(4))))));\n'
                '    println!("{}", eval(&e));\n'
                '    println!("{}", eval(&Expr::Num(7)));\n'
                '    println!("{}", eval(&Expr::Neg(Box::new(Expr::Neg(num(5))))));\n'
                '}\n',
      'hint': 'Num(n) даёт n: &i64 — разыменуйте: *n. Для Neg: -eval(a).',
      'expected': ['-10', '7', '5']},
     {'id': 'r4-expr-show',
      'mode': 'rust',
      'title': 'Дерево выражений: show',
      'statement': 'Тот же Expr. Напишите show(e: &Expr) → String: Num → число; Add → «(A + B)»; Mul → «(A * '
                   'B)»; Neg → «-A».',
      'starter': 'enum Expr {\n'
                 '    Num(i64),\n'
                 '    Add(Box<Expr>, Box<Expr>),\n'
                 '    Mul(Box<Expr>, Box<Expr>),\n'
                 '    Neg(Box<Expr>),\n'
                 '}\n'
                 '\n'
                 'fn show(e: &Expr) -> String {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn num(n: i64) -> Box<Expr> {\n'
                '    Box::new(Expr::Num(n))\n'
                '}\n'
                '\n'
                'fn main() {\n'
                '    let e = Expr::Add(num(2), Box::new(Expr::Mul(num(3), Box::new(Expr::Neg(num(4))))));\n'
                '    println!("{}", show(&e));\n'
                '    println!("{}", show(&Expr::Num(-7)));\n'
                '}\n',
      'hint': 'Для вложенных частей вызывайте show(a), show(b) и вставляйте результаты в format!.',
      'expected': ['(2 + (3 * -4))', '-7']},
     {'id': 'r4-derive-ord',
      'mode': 'rust',
      'title': 'derive(Ord): порядок полей — порядок сравнения',
      'statement': 'Version { major, minor, patch } выводит PartialOrd и Ord, но поля записаны в '
                   'неправильном порядке, поэтому версии сортируются неверно. Исправьте определение '
                   'структуры, ничего больше не меняя: 1.2.9 < 1.10.0 < 2.0.0.',
      'starter': '#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]\n'
                 'struct Version {\n'
                 '    patch: u32,\n'
                 '    minor: u32,\n'
                 '    major: u32,\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut v = vec![\n'
                '        Version { major: 2, minor: 0, patch: 0 },\n'
                '        Version { major: 1, minor: 10, patch: 0 },\n'
                '        Version { major: 1, minor: 2, patch: 9 },\n'
                '        Version { major: 1, minor: 2, patch: 10 },\n'
                '    ];\n'
                '    v.sort();\n'
                '    for x in &v {\n'
                '        print!("{}.{}.{} ", x.major, x.minor, x.patch);\n'
                '    }\n'
                '    println!();\n'
                '    let m = v.iter().max().unwrap();\n'
                '    println!("{}.{}.{} {}", m.major, m.minor, m.patch, v[0] < v[1]);\n'
                '}\n',
      'hint': 'Лексикографическое сравнение идёт в порядке полей в определении: сначала major, потом minor, '
              'потом patch.',
      'expected': ['1.2.9 1.2.10 1.10.0 2.0.0', '2.0.0 true']},
     {'id': 'r4-default',
      'mode': 'rust',
      'title': 'Default вручную и ..Default::default()',
      'statement': 'Settings: retries: u32, timeout_ms: u64, verbose: bool, name: String, proxy: '
                   'Option<String>. Реализуйте Default: retries 3, timeout_ms 5000, verbose false, name '
                   '"app", proxy None. quiet() → Settings: все значения по умолчанию, кроме retries = 0 '
                   '(используйте ..Default::default()).',
      'starter': '#[derive(Debug)]\n'
                 'struct Settings {\n'
                 '    retries: u32,\n'
                 '    timeout_ms: u64,\n'
                 '    verbose: bool,\n'
                 '    name: String,\n'
                 '    proxy: Option<String>,\n'
                 '}\n'
                 '\n'
                 'impl Default for Settings {\n'
                 '    fn default() -> Settings {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'fn quiet() -> Settings {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", Settings::default());\n'
                '    println!("{:?}", quiet());\n'
                '    let s = Settings { verbose: true, ..Settings::default() };\n'
                '    println!("{} {}", s.verbose, s.name);\n'
                '}\n',
      'hint': 'Синтаксис обновления: Settings { retries: 0, ..Default::default() } берёт остальные поля из '
              'значения по умолчанию.',
      'expected': ['Settings { retries: 3, timeout_ms: 5000, verbose: false, name: "app", proxy: None }',
                   'Settings { retries: 0, timeout_ms: 5000, verbose: false, name: "app", proxy: None }',
                   'true app']},
     {'id': 'r4-builder',
      'mode': 'rust',
      'title': 'Строитель: цепочка методов с self',
      'statement': 'RequestBuilder собирает запрос. new(url), header(self, k, v) → Self (добавить '
                   'заголовок), timeout(self, t: u32) → Self, build(self) → Request. '
                   'Request::describe(&self) → String: «GET <url> timeout=<t> [k: v, k2: v2]»; без '
                   'заголовков — «[]». Таймаут по умолчанию 30. Методы принимают self по значению и '
                   'возвращают его обратно.',
      'starter': 'struct Request {\n'
                 '    url: String,\n'
                 '    headers: Vec<(String, String)>,\n'
                 '    timeout: u32,\n'
                 '}\n'
                 '\n'
                 'struct RequestBuilder {\n'
                 '    url: String,\n'
                 '    headers: Vec<(String, String)>,\n'
                 '    timeout: u32,\n'
                 '}\n'
                 '\n'
                 'impl RequestBuilder {\n'
                 '    fn new(url: &str) -> RequestBuilder {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn header(mut self, k: &str, v: &str) -> RequestBuilder {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn timeout(mut self, t: u32) -> RequestBuilder {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn build(self) -> Request {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'impl Request {\n'
                 '    fn describe(&self) -> String {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let r = RequestBuilder::new("http://a.b/")\n'
                '        .header("Accept", "text/html")\n'
                '        .timeout(5)\n'
                '        .header("X-Id", "7")\n'
                '        .build();\n'
                '    println!("{}", r.describe());\n'
                '    println!("{}", RequestBuilder::new("/x").build().describe());\n'
                '}\n',
      'hint': 'Каждый метод изменяет self и возвращает его: self.headers.push(...); self.',
      'expected': ['GET http://a.b/ timeout=5 [Accept: text/html, X-Id: 7]', 'GET /x timeout=30 []']},
     {'id': 'r4-inventory',
      'mode': 'rust',
      'title': 'Инвентарь: &, &mut и Option<&T>',
      'statement': 'Item { name: String, qty: u32, price_cents: u64 }. total_value(items: &[Item]) → u64 — '
                   'сумма qty × price. cheapest(items: &[Item]) → Option<&Item> — позиция с наименьшей ценой '
                   'за штуку (первая из равных; пустой список → None). restock(items: &mut [Item], name: '
                   '&str, n: u32) → bool — увеличить qty позиции с таким именем, true если нашли.',
      'starter': 'struct Item {\n'
                 '    name: String,\n'
                 '    qty: u32,\n'
                 '    price_cents: u64,\n'
                 '}\n'
                 '\n'
                 'fn total_value(items: &[Item]) -> u64 {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn cheapest(items: &[Item]) -> Option<&Item> {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn restock(items: &mut [Item], name: &str, n: u32) -> bool {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut items = vec![\n'
                '        Item { name: "pen".into(), qty: 10, price_cents: 150 },\n'
                '        Item { name: "book".into(), qty: 2, price_cents: 1200 },\n'
                '        Item { name: "clip".into(), qty: 100, price_cents: 5 },\n'
                '        Item { name: "tape".into(), qty: 1, price_cents: 5 },\n'
                '    ];\n'
                '    println!("{}", total_value(&items));\n'
                '    println!("{}", cheapest(&items).map(|i| i.name.as_str()).unwrap_or("-"));\n'
                '    println!("{} {}", restock(&mut items, "book", 3), restock(&mut items, "gum", 1));\n'
                '    println!("{} {}", items[1].qty, total_value(&items));\n'
                '    println!("{}", cheapest(&[]).is_none());\n'
                '}\n',
      'hint': 'Для restock: for it in items.iter_mut() даёт &mut Item; return true прямо из цикла.',
      'expected': ['4405', 'clip', 'true false', '5 8005', 'true']},
     {'id': 'r4-matrix',
      'mode': 'rust',
      'title': 'Матрица в одном Vec: row-major',
      'statement': 'Matrix { rows, cols, data: Vec<i32> } хранит элементы построчно: индекс (r, c) → r * '
                   'cols + c (как двумерный массив в памяти). new(rows, cols) — нули; get(&self, r, c) → '
                   'Option<i32> (None вне границ); set(&mut self, r, c, v) → bool (false вне границ); '
                   'transpose(&self) → Matrix.',
      'starter': 'struct Matrix {\n'
                 '    rows: usize,\n'
                 '    cols: usize,\n'
                 '    data: Vec<i32>,\n'
                 '}\n'
                 '\n'
                 'impl Matrix {\n'
                 '    fn new(rows: usize, cols: usize) -> Matrix {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn get(&self, r: usize, c: usize) -> Option<i32> {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn set(&mut self, r: usize, c: usize, v: i32) -> bool {\n'
                 '        todo!()\n'
                 '    }\n'
                 '\n'
                 '    fn transpose(&self) -> Matrix {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut m = Matrix::new(2, 3);\n'
                '    let mut k = 1;\n'
                '    for r in 0..2 {\n'
                '        for c in 0..3 {\n'
                '            m.set(r, c, k);\n'
                '            k += 1;\n'
                '        }\n'
                '    }\n'
                '    println!("{:?}", m.data);\n'
                '    let t = m.transpose();\n'
                '    println!("{} {} {:?}", t.rows, t.cols, t.data);\n'
                '    println!("{:?} {:?} {}", m.get(1, 2), m.get(2, 0), m.set(0, 3, 1));\n'
                '}\n',
      'hint': 'Индекс в одномерном Vec: r * cols + c; при транспонировании у новой матрицы строк столько, '
              'сколько столбцов у старой.',
      'expected': ['[1, 2, 3, 4, 5, 6]', '3 2 [1, 4, 2, 5, 3, 6]', 'Some(6) None false']},
     {'id': 'r4-value-tree',
      'mode': 'rust',
      'title': 'Размеченное объединение: Value',
      'statement': 'Value — Int(i64), Float(f64), Text(String) или List(Vec<Value>). total(&Value) → f64 — '
                   'сумма всех чисел (в том числе вложенных в списки; текст не считается). depth(&Value) → '
                   'usize: 0 для не списка, для списка — 1 + наибольшая глубина элементов (пустой список — '
                   '1). texts(&Value) → Vec<String> — все строки в порядке обхода.',
      'starter': 'enum Value {\n'
                 '    Int(i64),\n'
                 '    Float(f64),\n'
                 '    Text(String),\n'
                 '    List(Vec<Value>),\n'
                 '}\n'
                 '\n'
                 'fn total(v: &Value) -> f64 {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn depth(v: &Value) -> usize {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn texts(v: &Value) -> Vec<String> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    use Value::*;\n'
                '    let v = List(vec![\n'
                '        Int(2),\n'
                '        Text("a".into()),\n'
                '        List(vec![Float(1.5), List(vec![Text("b".into()), Int(10)])]),\n'
                '        Text("c".into()),\n'
                '    ]);\n'
                '    println!("{} {} {:?}", total(&v), depth(&v), texts(&v));\n'
                '    println!("{} {} {:?}", total(&Int(5)), depth(&List(vec![])), texts(&Float(1.0)));\n'
                '}\n',
      'hint': 'Список обрабатывается рекурсивно: items.iter().map(total).sum(); max() по пустому итератору '
              'даёт None — подойдёт unwrap_or(0).',
      'expected': ['13.5 3 ["a", "b", "c"]', '5 1 []']},
     {'id': 'r4-json',
      'mode': 'rust',
      'title': 'Рендер JSON из enum',
      'statement': 'Json — Null, Bool, Num(f64), Str(String), Arr(Vec<Json>), Obj(Vec<(String, Json)>). '
                   'render(&self) → String: компактный JSON без пробелов: null, true/false, число как в {}, '
                   'строка в двойных кавычках (экранируйте \\" и \\\\), массив [a,b], объект {"k":v,...} в '
                   'порядке вектора.',
      'starter': 'enum Json {\n'
                 '    Null,\n'
                 '    Bool(bool),\n'
                 '    Num(f64),\n'
                 '    Str(String),\n'
                 '    Arr(Vec<Json>),\n'
                 '    Obj(Vec<(String, Json)>),\n'
                 '}\n'
                 '\n'
                 'impl Json {\n'
                 '    fn render(&self) -> String {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    use Json::*;\n'
                '    let j = Obj(vec![\n'
                '        ("name".to_string(), Str("Анна \\"Ню\\"".to_string())),\n'
                '        ("age".to_string(), Num(30.0)),\n'
                '        ("pi".to_string(), Num(3.5)),\n'
                '        ("tags".to_string(), Arr(vec![Bool(true), Null, Str("a\\\\b".to_string())])),\n'
                '        ("empty".to_string(), Arr(vec![])),\n'
                '    ]);\n'
                '    println!("{}", j.render());\n'
                '    println!("{}", Null.render());\n'
                '}\n',
      'hint': 'Вспомогательная функция quote(s) экранирует символы по одному; в format! фигурные скобки '
              'удваивают: {{ и }}.',
      'expected': ['{"name":"Анна \\"Ню\\"","age":30,"pi":3.5,"tags":[true,null,"a\\\\b"],"empty":[]}',
                   'null']},
     {'id': 'r4-event-log',
      'mode': 'rust',
      'title': 'Журнал событий: struct-варианты',
      'statement': 'Event — Login { user }, Logout { user }, Purchase { user, cents: u32 } '
                   '(struct-варианты). summarize(events: &[Event]) → (usize, u32, Vec<String>): число '
                   'входов, сумма покупок в центах и имена пользователей, которые остались в системе (вошли '
                   'и не вышли) — в порядке последнего входа без выхода.',
      'starter': 'enum Event {\n'
                 '    Login { user: String },\n'
                 '    Logout { user: String },\n'
                 '    Purchase { user: String, cents: u32 },\n'
                 '}\n'
                 '\n'
                 'fn summarize(events: &[Event]) -> (usize, u32, Vec<String>) {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let ev = vec![\n'
                '        Event::Login { user: "ann".into() },\n'
                '        Event::Login { user: "bob".into() },\n'
                '        Event::Purchase { user: "ann".into(), cents: 500 },\n'
                '        Event::Logout { user: "ann".into() },\n'
                '        Event::Login { user: "cat".into() },\n'
                '        Event::Purchase { user: "cat".into(), cents: 250 },\n'
                '        Event::Logout { user: "zed".into() },\n'
                '    ];\n'
                '    println!("{:?}", summarize(&ev));\n'
                '    println!("{:?}", summarize(&[]));\n'
                '}\n',
      'hint': 'Образец Event::Purchase { cents, .. } берёт нужное поле и пропускает остальные.',
      'expected': ['(3, 750, ["bob", "cat"])', '(0, 0, [])']}],
 5: [{'id': 'r5-vec-stats',
      'mode': 'rust',
      'title': 'Vec: минимум, максимум, среднее',
      'statement': 'stats(v: &[i32]) → Option<(i32, i32, f64)>: минимум, максимум и среднее арифметическое; '
                   'для пустого среза — None.',
      'starter': 'fn stats(v: &[i32]) -> Option<(i32, i32, f64)> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", stats(&[3, -1, 4, 1, 5]));\n'
                '    println!("{:?}", stats(&[7]));\n'
                '    println!("{:?}", stats(&[]));\n'
                '    println!("{:?}", stats(&vec![i32::MAX, i32::MAX]));\n'
                '}\n',
      'hint': 'min() и max() возвращают Option<&i32>; сумму считайте в i64, чтобы не переполнить i32.',
      'expected': ['Some((-1, 5, 2.4))',
                   'Some((7, 7, 7.0))',
                   'None',
                   'Some((2147483647, 2147483647, 2147483647.0))']},
     {'id': 'r5-vec-clean',
      'mode': 'rust',
      'title': 'Vec: retain, sort, dedup',
      'statement': 'clean(v: &mut Vec<i32>) приводит вектор в порядок на месте: убирает отрицательные числа, '
                   'сортирует по возрастанию, убирает повторы. Новый вектор создавать не нужно.',
      'starter': 'fn clean(v: &mut Vec<i32>) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let mut v = vec![5, -2, 3, 5, 0, -7, 3, 9, 0];\n'
                '    clean(&mut v);\n'
                '    println!("{:?}", v);\n'
                '    let mut e: Vec<i32> = vec![-1, -2];\n'
                '    clean(&mut e);\n'
                '    println!("{:?} {}", e, e.is_empty());\n'
                '}\n',
      'hint': 'retain(|&x| x >= 0) оставляет подходящие элементы; dedup убирает соседние повторы, поэтому '
              'сначала sort.',
      'expected': ['[0, 3, 5, 9]', '[] true']},
     {'id': 'r5-chunks',
      'mode': 'rust',
      'title': 'Срезы Vec: chunks и windows',
      'statement': 'chunked(v, n) → Vec<Vec<i32>>: разбить на куски по n элементов (последний может быть '
                   'короче; n ≥ 1). window_sums(v, k) → Vec<i32>: суммы всех подряд идущих окон длины k (k ≥ '
                   '1; если окно не помещается — пустой вектор).',
      'starter': 'fn chunked(v: &[i32], n: usize) -> Vec<Vec<i32>> {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn window_sums(v: &[i32], k: usize) -> Vec<i32> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", chunked(&[1, 2, 3, 4, 5, 6, 7], 3));\n'
                '    println!("{:?}", chunked(&[], 2));\n'
                '    println!("{:?}", window_sums(&[1, 2, 3, 4, 5], 2));\n'
                '    println!("{:?}", window_sums(&[1, 2], 3));\n'
                '    println!("{:?}", window_sums(&[4, 4, 4], 3));\n'
                '}\n',
      'hint': 'chunks(n) и windows(k) — методы срезов; каждый элемент — тоже срез, to_vec() копирует его.',
      'expected': ['[[1, 2, 3], [4, 5, 6], [7]]', '[]', '[3, 5, 7, 9]', '[]', '[12]']},
     {'id': 'r5-vec-reallocs',
      'mode': 'rust',
      'title': 'Сколько раз вырастет буфер',
      'statement': 'reallocs(n, start_cap) → usize: создайте Vec<u64> через with_capacity(start_cap), '
                   'добавьте n чисел и верните, сколько раз за это изменилась ёмкость (capacity). Сравните с '
                   'reallocs(100, 100): ровно ноль — резервировать ёмкость заранее выгодно.',
      'starter': 'fn reallocs(n: usize, start_cap: usize) -> usize {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{} {}", reallocs(0, 0), reallocs(1, 0));\n'
                '    println!("{} {}", reallocs(100, 0), reallocs(100, 100));\n'
                '    println!("{} {}", reallocs(1000, 0), reallocs(1000, 1000));\n'
                '    println!("{}", reallocs(100, 60));\n'
                '}\n',
      'hint': 'Запоминайте последнюю ёмкость и считайте, сколько раз она менялась после push.',
      'expected': ['0 1', '6 0', '9 0', '1']},
     {'id': 'r5-drain-evens',
      'mode': 'rust',
      'title': 'Разделить вектор на месте',
      'statement': 'take_evens(v: &mut Vec<i32>) → Vec<i32>: убрать из v все чётные числа и вернуть их в '
                   'прежнем порядке; в v остаются нечётные (тоже в прежнем порядке). Копировать элементы не '
                   'нужно: числа просто переезжают.',
      'starter': 'fn take_evens(v: &mut Vec<i32>) -> Vec<i32> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let mut v = vec![1, 2, 3, 4, 5, 6, 8];\n'
                '    let e = take_evens(&mut v);\n'
                '    println!("{:?} {:?}", e, v);\n'
                '    let mut w: Vec<i32> = vec![];\n'
                '    println!("{:?} {:?}", take_evens(&mut w), w);\n'
                '}\n',
      'hint': 'drain(..) выдаёт элементы с владением; partition делит их на два вектора по условию.',
      'expected': ['[2, 4, 6, 8] [1, 3, 5]', '[] []']},
     {'id': 'r5-pascal',
      'mode': 'rust',
      'title': 'Vec<Vec<>>: треугольник Паскаля',
      'statement': 'pascal(n) → Vec<Vec<u64>>: первые n строк треугольника Паскаля (в первой строке одна '
                   'единица). Каждая строка строится из предыдущей.',
      'starter': 'fn pascal(n: usize) -> Vec<Vec<u64>> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for row in pascal(6) {\n'
                '        println!("{:?}", row);\n'
                '    }\n'
                '    println!("{}", pascal(0).len());\n'
                '    println!("{}", pascal(60)[59][30]);\n'
                '}\n',
      'hint': 'Внутренний элемент равен сумме двух элементов предыдущей строки: rows[i-1][j-1] + '
              'rows[i-1][j].',
      'expected': ['[1]',
                   '[1, 1]',
                   '[1, 2, 1]',
                   '[1, 3, 3, 1]',
                   '[1, 4, 6, 4, 1]',
                   '[1, 5, 10, 10, 5, 1]',
                   '0',
                   '59132290782430712']},
     {'id': 'r5-iter-pipeline',
      'mode': 'rust',
      'title': 'Итераторы вместо циклов',
      'statement': 'sum_sq_odd(v) → i32 — сумма квадратов нечётных; dot(a, b) → i32 — скалярное произведение '
                   '(zip); running_max(v) → Vec<i32> — максимум на каждом префиксе (scan). Слово for в коде '
                   'использовать нельзя — только адаптеры итераторов.',
      'starter': 'fn sum_sq_odd(v: &[i32]) -> i32 {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn dot(a: &[i32], b: &[i32]) -> i32 {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn running_max(v: &[i32]) -> Vec<i32> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!("fo", "r ")).count();\n'
                '    println!("{}", sum_sq_odd(&[1, 2, 3, 4, 5]));\n'
                '    println!("{}", dot(&[1, 2, 3], &[4, 5, 6]));\n'
                '    println!("{:?}", running_max(&[3, 1, 4, 1, 5, 2, 6]));\n'
                '    println!("{} {:?}", dot(&[1, 2], &[3]), running_max(&[]));\n'
                '    println!("loops: {}", bad0);\n'
                '}\n',
      'hint': 'scan(начальное, |состояние, элемент| …) хранит изменяемое состояние между шагами и возвращает '
              'Some(следующее значение).',
      'expected': ['35', '32', '[3, 3, 4, 4, 5, 5, 6]', '3 []', 'loops: 0']},
     {'id': 'r5-closure-capture',
      'mode': 'rust',
      'title': 'Замыкания и захват',
      'statement': 'count_above(v, threshold) → usize: сколько элементов больше порога (порог захватывается '
                   'замыканием). running_total(v) → Vec<i32>: нарастающие суммы; замыкание изменяет '
                   'захваченную переменную sum. apply_n(f: fn(i32) -> i32, n, x) → i32: применить функцию n '
                   'раз.',
      'starter': 'fn count_above(v: &[i32], threshold: i32) -> usize {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn running_total(v: &[i32]) -> Vec<i32> {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn apply_n(f: fn(i32) -> i32, n: u32, x: i32) -> i32 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn double(x: i32) -> i32 {\n'
                '    x * 2\n'
                '}\n'
                '\n'
                'fn main() {\n'
                '    println!("{} {}", count_above(&[1, 5, 10, 15], 5), count_above(&[], 0));\n'
                '    println!("{:?}", running_total(&[1, 2, 3, 4]));\n'
                '    println!("{} {}", apply_n(double, 5, 1), apply_n(|x| x - 1, 3, 10));\n'
                '}\n',
      'hint': 'Замыкание |&x| sum += x … изменяет внешнюю sum — она должна быть mut; функция принимается как '
              'fn(i32) -> i32, и обычное замыкание без захвата подходит.',
      'expected': ['2 0', '[1, 3, 6, 10]', '32 7']},
     {'id': 'r5-fix-collect',
      'mode': 'rust',
      'title': 'Исправьте: collect без типа',
      'statement': 'squares_sum возводит элементы в квадрат, собирает их и суммирует. Компилятор не может '
                   'определить, в какую коллекцию собирать. Исправьте одной правкой.',
      'starter': 'fn squares_sum(v: &[i32]) -> i32 {\n'
                 '    let squares = v.iter().map(|x| x * x).collect();\n'
                 '    squares.iter().sum()\n'
                 '}\n',
      'driver': 'fn main() {\n    println!("{} {}", squares_sum(&[1, 2, 3]), squares_sum(&[]));\n}\n',
      'hint': 'collect::<Vec<i32>>() или тип у переменной: let squares: Vec<i32> = ….',
      'expected': ['14 0']},
     {'id': 'r5-caesar',
      'mode': 'rust',
      'title': 'String: шифр Цезаря',
      'statement': 'caesar(s: &str, k: u8) → String: сдвинуть каждую латинскую букву на k вперёд по кругу (0 '
                   '≤ k ≤ 25), регистр сохранить; остальные символы (в том числе кириллицу) оставить как '
                   'есть.',
      'starter': 'fn caesar(s: &str, k: u8) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", caesar("Hello, World!", 3));\n'
                '    println!("{}", caesar("xyz XYZ", 3));\n'
                '    println!("{}", caesar("привет abc", 1));\n'
                '    println!("{}", caesar(&caesar("Round trip", 7), 19));\n'
                '}\n',
      'hint': "c as u8 - b'a' + k даёт позицию в алфавите; % 26 заворачивает по кругу; collect() из "
              'итератора char в String.',
      'expected': ['Khoor, Zruog!', 'abc ABC', 'привет bcd', 'Round trip']},
     {'id': 'r5-utf8-stats',
      'mode': 'rust',
      'title': 'Символы и байты',
      'statement': 'char_stats(s) → (usize, usize): число символов и число байт. is_palindrome(s) → bool: '
                   'палиндром, если игнорировать регистр и все символы, кроме букв и цифр. reverse_words(s) '
                   '→ String: слова в обратном порядке, через один пробел.',
      'starter': 'fn char_stats(s: &str) -> (usize, usize) {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn is_palindrome(s: &str) -> bool {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn reverse_words(s: &str) -> String {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?} {:?}", char_stats("привет"), char_stats("abc"));\n'
                '    println!("{} {}", is_palindrome("А роза упала на лапу Азора"), is_palindrome("не '
                'палиндром"));\n'
                '    println!("{}", is_palindrome("A man, a plan, a canal: Panama"));\n'
                '    println!("{:?}", reverse_words("  один  два три "));\n'
                '}\n',
      'hint': 'Соберите Vec<char> из букв и цифр в нижнем регистре и сравните его с самим собой в обратном '
              'порядке.',
      'expected': ['(6, 12) (3, 3)', 'true false', 'true', '"три два один"']},
     {'id': 'r5-title-case',
      'mode': 'rust',
      'title': 'Первая буква заглавная',
      'statement': 'title_case(s) → String: каждое слово с заглавной буквы, остальные буквы строчные '
                   '(работает и с кириллицей); слова разделяются в результате ровно одним пробелом.',
      'starter': 'fn title_case(s: &str) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", title_case("hELLO   wORLD"));\n'
                '    println!("{}", title_case("привет мир"));\n'
                '    println!("{:?}", title_case("   "));\n'
                '    println!("{}", title_case("rust"));\n'
                '}\n',
      'hint': 'chars() даёт первую букву, а остаток — cs.as_str(); to_uppercase() возвращает итератор, '
              'соберите его в String.',
      'expected': ['Hello World', 'Привет Мир', '""', 'Rust']},
     {'id': 'r5-fix-string-add',
      'mode': 'rust',
      'title': 'Исправьте: + забрал строку',
      'statement': 'join3 склеивает три строки и дописывает «(из a b c)». Оператор + забирает левый операнд, '
                   'и a после него использовать нельзя. Исправьте, чтобы функция вернула, например, «xyz (из '
                   'x y z)».',
      'starter': 'fn join3(a: String, b: String, c: String) -> String {\n'
                 '    let ab = a + &b;\n'
                 '    let abc = ab + &c;\n'
                 '    format!("{abc} (из {a} {b} {c})")\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", join3("x".into(), "y".into(), "z".into()));\n'
                '    println!("{}", join3("при".into(), "вет".into(), "!".into()));\n'
                '}\n',
      'hint': 'format! не забирает аргументы, поэтому после него строки остаются доступны.',
      'expected': ['xyz (из x y z)', 'привет! (из при вет !)']},
     {'id': 'r5-word-count',
      'mode': 'rust',
      'title': 'HashMap и entry: частоты слов',
      'statement': 'word_count(text) → Vec<(String, usize)>: слова (последовательности букв; всё остальное — '
                   'разделители; регистр не важен) с количеством вхождений, отсортированные по убыванию '
                   'количества, затем по алфавиту. Подсчёт — через entry.',
      'starter': 'use std::collections::HashMap;\n'
                 '\n'
                 'fn word_count(text: &str) -> Vec<(String, usize)> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let r = word_count("The fox, the DOG; the end. Fox? dog!");\n'
                '    println!("{:?}", r);\n'
                '    println!("{:?}", word_count("Привет, привет, мир!"));\n'
                '    println!("{:?}", word_count("...  "));\n'
                '}\n',
      'hint': 'split(|c: char| !c.is_alphabetic()) разбивает по небуквам; *m.entry(слово).or_insert(0) += 1 '
              'считает; сортировка — sort_by с then.',
      'expected': ['[("the", 3), ("dog", 2), ("fox", 2), ("end", 1)]', '[("привет", 2), ("мир", 1)]', '[]']},
     {'id': 'r5-group-by-len',
      'mode': 'rust',
      'title': 'Группировка по длине',
      'statement': 'group_by_len(words: &[&str]) → BTreeMap<usize, Vec<String>>: ключ — длина слова в '
                   'символах, значение — слова этой длины в порядке появления. Используйте '
                   'entry(…).or_insert_with(Vec::new).',
      'starter': 'use std::collections::BTreeMap;\n'
                 '\n'
                 'fn group_by_len(words: &[&str]) -> BTreeMap<usize, Vec<String>> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let m = group_by_len(&["a", "bb", "cc", "d", "привет", "eee", "мир", "ё"]);\n'
                '    println!("{:?}", m);\n'
                '    println!("{}", group_by_len(&[]).len());\n'
                '}\n',
      'hint': 'or_insert_with(Vec::new) создаёт пустой вектор только если ключа ещё нет; push вызывается на '
              'возвращённой &mut.',
      'expected': ['{1: ["a", "d", "ё"], 2: ["bb", "cc"], 3: ["eee", "мир"], 6: ["привет"]}', '0']},
     {'id': 'r5-two-sum',
      'mode': 'rust',
      'title': 'Два числа за один проход: HashMap',
      'statement': 'two_sum(v: &[i64], target) → Option<(usize, usize)>: индексы i < j с v[i] + v[j] = '
                   'target; из всех пар нужна та, у которой j наименьшее (при равных j — наименьшее i). '
                   'Входы большие, поэтому двойной цикл не уложится в лимит: используйте HashMap «значение → '
                   'индекс» и один проход.',
      'starter': 'fn two_sum(v: &[i64], target: i64) -> Option<(usize, usize)> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", two_sum(&[2, 7, 11, 15], 9));\n'
                '    println!("{:?}", two_sum(&[3, 3], 6));\n'
                '    println!("{:?}", two_sum(&[1, 2, 3], 100));\n'
                '    let n = 400_000usize;\n'
                '    let v: Vec<i64> = (0..n as i64).map(|i| i * 3 + 1).collect();\n'
                '    let target = v[n - 2] + v[n - 1];\n'
                '    println!("{:?}", two_sum(&v, target));\n'
                '}\n',
      'hint': 'Идите по элементам; для текущего x проверьте, есть ли в таблице target - x, и только потом '
              'кладите x в таблицу.',
      'expected': ['Some((0, 1))', 'Some((0, 1))', 'None', 'Some((399998, 399999))']},
     {'id': 'r5-anagrams',
      'mode': 'rust',
      'title': 'Анаграммы: ключ из отсортированных букв',
      'statement': 'anagram_groups(words: &[&str]) → Vec<Vec<String>>: сгруппируйте слова-анаграммы (регистр '
                   'не важен, но слова сохраняются как есть). Верните только группы из двух и более слов; '
                   'слова внутри группы — в порядке появления; группы — в порядке возрастания ключа (букв '
                   'слова по алфавиту).',
      'starter': 'fn anagram_groups(words: &[&str]) -> Vec<Vec<String>> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", anagram_groups(&["listen", "silent", "enlist", "google", "gogole", '
                '"cat", "act", "Tac", "dog"]));\n'
                '    println!("{:?}", anagram_groups(&["один", "два"]));\n'
                '    println!("{:?}", anagram_groups(&[]));\n'
                '}\n',
      'hint': 'Ключ группы — слово, у которого буквы отсортированы; BTreeMap сам упорядочит группы по ключу.',
      'expected': ['[["cat", "act", "Tac"], ["google", "gogole"], ["listen", "silent", "enlist"]]',
                   '[]',
                   '[]']},
     {'id': 'r5-merge-counts',
      'mode': 'rust',
      'title': 'Слияние словарей с владением',
      'statement': 'merge_counts(a, b) → BTreeMap<String, i32>: объединить два словаря счётчиков, складывая '
                   'значения для общих ключей. Оба словаря передаются по значению: ключи-строки должны '
                   'переехать, а не копироваться.',
      'starter': 'use std::collections::{BTreeMap, HashMap};\n'
                 '\n'
                 'fn merge_counts(a: HashMap<String, i32>, b: HashMap<String, i32>) -> BTreeMap<String, i32> '
                 '{\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                '    let mut a = HashMap::new();\n'
                '    a.insert(String::from("x"), 1);\n'
                '    a.insert(String::from("y"), 2);\n'
                '    let mut b = HashMap::new();\n'
                '    b.insert(String::from("y"), 10);\n'
                '    b.insert(String::from("z"), 5);\n'
                '    println!("{:?}", merge_counts(a, b));\n'
                '    println!("{:?}", merge_counts(HashMap::new(), HashMap::new()));\n'
                '    println!("clones: {}", bad0);\n'
                '}\n',
      'hint': 'into_iter() у HashMap отдаёт пары (String, i32) с владением; chain соединяет два итератора.',
      'expected': ['{"x": 1, "y": 12, "z": 5}', '{}', 'clones: 0']},
     {'id': 'r5-fix-key-move',
      'mode': 'rust',
      'title': 'Исправьте: ключ переехал в таблицу',
      'statement': 'index(words) → (HashMap<String, usize>, usize): отображение «слово → последний индекс» и '
                   'суммарная длина всех слов в байтах. Код не собирается: w переезжает в insert, а затем '
                   'читается. Исправьте минимальной правкой.',
      'starter': 'use std::collections::HashMap;\n'
                 '\n'
                 'fn index(words: Vec<String>) -> (HashMap<String, usize>, usize) {\n'
                 '    let mut m = HashMap::new();\n'
                 '    let mut total = 0;\n'
                 '    for (i, w) in words.into_iter().enumerate() {\n'
                 '        m.insert(w, i);\n'
                 '        total += w.len();\n'
                 '    }\n'
                 '    (m, total)\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let src = include_str!("main.rs");\n'
                '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                '    let (m, total) = index(vec!["aa".into(), "b".into(), "aa".into(), "привет".into()]);\n'
                '    let mut items: Vec<_> = m.iter().collect();\n'
                '    items.sort();\n'
                '    println!("{:?} {}", items, total);\n'
                '    println!("clones: {}", bad0);\n'
                '}\n',
      'hint': 'Прочитайте w.len() до insert: после insert строка принадлежит таблице. Клонировать не нужно.',
      'expected': ['[("aa", 2), ("b", 1), ("привет", 3)] 17', 'clones: 0']},
     {'id': 'r5-parse-age',
      'mode': 'rust',
      'title': 'Result<u8, String> и виды ошибок разбора',
      'statement': 'parse_age(s) → Result<u8, String>: разберите строку как u8 и верните понятное сообщение: '
                   'пустая строка → "пусто"; не число (в том числе отрицательное) → "не число"; больше 255 → '
                   '"слишком велико"; число больше 150 → "нереальный возраст". Вид ошибки узнают через '
                   'e.kind() и IntErrorKind.',
      'starter': 'use std::num::IntErrorKind;\n'
                 '\n'
                 'fn parse_age(s: &str) -> Result<u8, String> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    for s in ["42", "", "abc", "-5", "300", "200", "150", "0"] {\n'
                '        println!("{:?} -> {:?}", s, parse_age(s));\n'
                '    }\n'
                '}\n',
      'hint': 'Охрана в match: Ok(n) if n > 150 => …; для ошибок — match e.kind() { IntErrorKind::Empty => '
              '…, … }.',
      'expected': ['"42" -> Ok(42)',
                   '"" -> Err("пусто")',
                   '"abc" -> Err("не число")',
                   '"-5" -> Err("не число")',
                   '"300" -> Err("слишком велико")',
                   '"200" -> Err("нереальный возраст")',
                   '"150" -> Ok(150)',
                   '"0" -> Ok(0)']},
     {'id': 'r5-question-mark',
      'mode': 'rust',
      'title': 'Оператор ?: цепочка разборов',
      'statement': 'sum_strs(a, b) → Result<i32, ParseIntError>: разобрать обе строки и сложить; '
                   'average(items: &[&str]) → Result<f64, ParseIntError>: среднее значение чисел (пустой '
                   'набор → 0.0). Оператор ? обязателен.',
      'starter': 'use std::num::ParseIntError;\n'
                 '\n'
                 'fn sum_strs(a: &str, b: &str) -> Result<i32, ParseIntError> {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn average(items: &[&str]) -> Result<f64, ParseIntError> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", sum_strs("3", " 4 "));\n'
                '    match sum_strs("3", "x") {\n'
                '        Ok(v) => println!("{v}"),\n'
                '        Err(e) => println!("ошибка: {e}"),\n'
                '    }\n'
                '    println!("{:?}", average(&["1", "2", "4"]));\n'
                '    println!("{:?} {}", average(&[]), average(&["1", ""]).is_err());\n'
                '    match average(&["99999999999"]) {\n'
                '        Ok(v) => println!("{v}"),\n'
                '        Err(e) => println!("ошибка: {e}"),\n'
                '    }\n'
                '}\n',
      'hint': 'let x: i32 = a.trim().parse()?; — при ошибке функция сразу вернёт Err.',
      'expected': ['Ok(7)',
                   'ошибка: invalid digit found in string',
                   'Ok(2.3333333333333335)',
                   'Ok(0.0) true',
                   'ошибка: number too large to fit in target type']},
     {'id': 'r5-custom-error',
      'mode': 'rust',
      'title': 'Своя ошибка: enum, Display, From',
      'statement': 'AppError — Empty, Parse(ParseIntError), Negative(i32). Реализуйте Display («пустая '
                   'строка» / «не число: <причина>» / «отрицательное: N»), std::error::Error и '
                   'From<ParseIntError>, затем parse_positive(s) → Result<u32, AppError>: строка с '
                   'обрезанными пробелами; пустая → Empty; не число → Parse (через ?); меньше нуля → '
                   'Negative.',
      'starter': 'use std::fmt;\n'
                 'use std::num::ParseIntError;\n'
                 '\n'
                 '#[derive(Debug)]\n'
                 'enum AppError {\n'
                 '    Empty,\n'
                 '    Parse(ParseIntError),\n'
                 '    Negative(i32),\n'
                 '}\n'
                 '\n'
                 'impl fmt::Display for AppError {\n'
                 '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'fn parse_positive(s: &str) -> Result<u32, AppError> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    for s in ["17", "  ", "x1", "-3", " 0 "] {\n'
                '        match parse_positive(s) {\n'
                '            Ok(n) => println!("ok {n}"),\n'
                '            Err(e) => println!("{e}"),\n'
                '        }\n'
                '    }\n'
                '    let e: Box<dyn std::error::Error> = Box::new(AppError::Negative(-1));\n'
                '    println!("{e}");\n'
                '    println!("{:?}", parse_positive(""));\n'
                '}\n',
      'hint': 'impl From<ParseIntError> for AppError { fn from(e) -> AppError { AppError::Parse(e) } } — '
              'тогда ? преобразует ошибку сам.',
      'expected': ['ok 17',
                   'пустая строка',
                   'не число: invalid digit found in string',
                   'отрицательное: -3',
                   'ok 0',
                   'отрицательное: -1',
                   'Err(Empty)']},
     {'id': 'r5-box-dyn-error',
      'mode': 'rust',
      'title': 'Box<dyn Error>: любая ошибка',
      'statement': 'run(a, b) → Result<i32, Box<dyn Error>>: разобрать оба аргумента как i32 (ошибка разбора '
                   'пробрасывается через ?) и разделить a на b; при b == 0 вернуть собственную ошибку '
                   '«деление на ноль» (строку можно превратить в Box<dyn Error> через .into()).',
      'starter': 'use std::error::Error;\n'
                 '\n'
                 'fn run(a: &str, b: &str) -> Result<i32, Box<dyn Error>> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    for (a, b) in [("84", "2"), ("1", "0"), ("x", "1"), ("5", ""), ("-9", "3")] {\n'
                '        match run(a, b) {\n'
                '            Ok(v) => println!("{v}"),\n'
                '            Err(e) => println!("ошибка: {e}"),\n'
                '        }\n'
                '    }\n'
                '}\n',
      'hint': 'Err("текст".into()) строит Box<dyn Error> из строки; ? сам упаковывает ParseIntError.',
      'expected': ['42',
                   'ошибка: деление на ноль',
                   'ошибка: invalid digit found in string',
                   'ошибка: cannot parse integer from empty string',
                   '-3']},
     {'id': 'r5-map-err',
      'mode': 'rust',
      'title': 'map_err: понятное сообщение',
      'statement': 'read_port(s) → Result<u16, String>: порт из строки. Ошибка разбора превращается в «bad '
                   "port '<s>': <причина>» через map_err, а значение 0 — в «port 0 reserved». Допустимые "
                   'значения: 1..=65535.',
      'starter': 'fn read_port(s: &str) -> Result<u16, String> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for s in ["8080", "0", "70000", "http", " 443 ", ""] {\n'
                '        println!("{:?}", read_port(s));\n'
                '    }\n'
                '}\n',
      'hint': 'map_err(|e| format!(…)) меняет только ошибку; после него ? пробрасывает уже String.',
      'expected': ['Ok(8080)',
                   'Err("port 0 reserved")',
                   'Err("bad port \'70000\': number too large to fit in target type")',
                   'Err("bad port \'http\': invalid digit found in string")',
                   'Ok(443)',
                   'Err("bad port \'\': cannot parse integer from empty string")']},
     {'id': 'r5-collect-result',
      'mode': 'rust',
      'title': 'collect в Result<Vec<_>, _>',
      'statement': 'parse_all(items) → Result<Vec<i32>, ParseIntError>: разобрать все строки; при первой '
                   'ошибке вернуть её (один collect). sum_valid(items) → i32: сумма только корректных чисел, '
                   'ошибки пропускаются (filter_map + ok).',
      'starter': 'use std::num::ParseIntError;\n'
                 '\n'
                 'fn parse_all(items: &[&str]) -> Result<Vec<i32>, ParseIntError> {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn sum_valid(items: &[&str]) -> i32 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", parse_all(&["1", " 2 ", "3"]));\n'
                '    println!("{:?}", parse_all(&["1", "x", "3", "y"]));\n'
                '    println!("{:?}", parse_all(&[]));\n'
                '    println!("{} {}", sum_valid(&["1", "x", "30", ""]), sum_valid(&[]));\n'
                '}\n',
      'hint': 'collect() в Result<Vec<_>, _> берёт итератор из Result и останавливается на первой ошибке; '
              'ok() превращает Result в Option.',
      'expected': ['Ok([1, 2, 3])', 'Err(ParseIntError { kind: InvalidDigit })', 'Ok([])', '31 0']},
     {'id': 'r5-ok-or',
      'mode': 'rust',
      'title': 'ok_or: из Option в Result',
      'statement': 'lookup(m: &HashMap<&str, i32>, key) → Result<i32, String>: значение по ключу или ошибка '
                   '«нет ключа <key>» (ok_or_else). first_digit(s) → Result<u32, String>: значение первой '
                   'цифры строки или ошибка «нет цифр» (используйте chars, find и to_digit).',
      'starter': 'use std::collections::HashMap;\n'
                 '\n'
                 'fn lookup(m: &HashMap<&str, i32>, key: &str) -> Result<i32, String> {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn first_digit(s: &str) -> Result<u32, String> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut m = HashMap::new();\n'
                '    m.insert("a", 1);\n'
                '    m.insert("b", 2);\n'
                '    println!("{:?} {:?}", lookup(&m, "a"), lookup(&m, "z"));\n'
                '    println!("{:?} {:?} {:?}", first_digit("abc7x9"), first_digit("none"), '
                'first_digit(""));\n'
                '}\n',
      'hint': 'get возвращает Option<&i32>; copied() даёт Option<i32>; ok_or_else(|| …) превращает None в '
              'Err.',
      'expected': ['Ok(1) Err("нет ключа z")', 'Ok(7) Err("нет цифр") Err("нет цифр")']},
     {'id': 'r5-fix-question-mark',
      'mode': 'rust',
      'title': 'Исправьте: ? в функции без Result',
      'statement': 'double разбирает строку и удваивает число. Оператор ? использован в функции, которая '
                   'возвращает просто i32 — компилятор отвечает ошибкой. Исправьте сигнатуру (результат — '
                   'Result<i32, ParseIntError>), тело меняется минимально.',
      'starter': 'use std::num::ParseIntError;\n'
                 '\n'
                 'fn double(s: &str) -> i32 {\n'
                 '    let n: i32 = s.trim().parse()?;\n'
                 '    n * 2\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?} {:?}", double("21"), double(" -4 "));\n'
                '    println!("{}", double("z").is_err());\n'
                '}\n',
      'hint': 'Тип функции — Result<i32, ParseIntError>, последнее выражение — Ok(n * 2).',
      'expected': ['Ok(42) Ok(-8)', 'true']},
     {'id': 'r5-unwind-drop',
      'mode': 'rust',
      'title': 'Паника разматывает стек и вызывает drop',
      'statement': 'Guard печатает «drop g» при уничтожении. Напишите risky(): создайте Guard и затем '
                   'вызовите panic!("boom"). Драйвер перехватит панику через catch_unwind и покажет, что '
                   'Guard всё равно был уничтожен: сначала выведется «drop g», затем «caught».',
      'starter': "struct Guard(&'static str);\n"
                 '\n'
                 'impl Drop for Guard {\n'
                 '    fn drop(&mut self) {\n'
                 '        println!("drop {}", self.0);\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'fn risky() {\n'
                 '    // создайте Guard и вызовите panic!\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    std::panic::set_hook(Box::new(|_| {}));\n'
                '    let r = std::panic::catch_unwind(|| risky());\n'
                '    println!("{}", if r.is_err() { "caught" } else { "no panic" });\n'
                '}\n',
      'hint': 'let _g = Guard("g"); — привязка с именем живёт до конца функции, и при панике drop вызывается '
              'во время размотки.',
      'expected': ['drop g', 'caught']},
     {'id': 'r5-retry',
      'mode': 'rust',
      'title': 'Повторные попытки: замыкание FnMut',
      'statement': 'retry(n, f) → Result<i32, String>: вызывайте f(попытка) для попыток 1, 2, …, n, пока не '
                   'получите Ok; верните первый Ok или последнюю ошибку (n = 0 → «нет попыток»). f — '
                   'замыкание FnMut(u32) -> Result<i32, String>, оно может менять захваченные переменные.',
      'starter': 'fn retry(n: u32, mut f: impl FnMut(u32) -> Result<i32, String>) -> Result<i32, String> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut calls = 0;\n'
                '    let r = retry(5, |k| {\n'
                '        calls += 1;\n'
                '        if k < 3 { Err(format!("fail {k}")) } else { Ok(k as i32 * 10) }\n'
                '    });\n'
                '    println!("{:?} calls={}", r, calls);\n'
                '    println!("{:?}", retry(3, |k| Err(format!("fail {k}"))));\n'
                '    println!("{:?}", retry(0, |_| Ok(1)));\n'
                '}\n',
      'hint': 'Храните последнюю ошибку в переменной и возвращайте её после цикла; Ok — сразу через return.',
      'expected': ['Ok(30) calls=3', 'Err("fail 3")', 'Err("нет попыток")']},
     {'id': 'r5-config-parser',
      'mode': 'rust',
      'title': 'Разбор конфигурации с номерами строк',
      'statement': 'parse_config(text) → Result<BTreeMap<String, String>, String>: строки «ключ = значение»; '
                   'пустые строки и строки, начинающиеся с «#», пропускаются; пробелы по краям ключа и '
                   "значения обрезаются. Первая же ошибка: «line N: нет '='», «line N: пустой ключ» или "
                   '«line N: дубликат ключа K» (N — номер строки с единицы).',
      'starter': 'use std::collections::BTreeMap;\n'
                 '\n'
                 'fn parse_config(text: &str) -> Result<BTreeMap<String, String>, String> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", parse_config("# comment\\nname = app\\n\\nport=8080\\nmode =  fast = '
                'yes\\n"));\n'
                '    println!("{:?}", parse_config("a=1\\nbroken\\nb=2"));\n'
                '    println!("{:?}", parse_config("a=1\\n = 5"));\n'
                '    println!("{:?}", parse_config("x=1\\ny=2\\nx=3"));\n'
                '    println!("{:?}", parse_config(""));\n'
                '}\n',
      'hint': "lines().enumerate() даёт индекс с нуля — добавьте 1; split_once('=') делит по первому знаку "
              'равенства.',
      'expected': ['Ok({"mode": "fast = yes", "name": "app", "port": "8080"})',
                   'Err("line 2: нет \'=\'")',
                   'Err("line 2: пустой ключ")',
                   'Err("line 3: дубликат ключа x")',
                   'Ok({})']}]}
