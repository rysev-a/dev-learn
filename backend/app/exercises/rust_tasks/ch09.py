"""Задачи книги «Изучаем Rust»: глава 9 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {9: [{'id': 'r9-shadowing',
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
     {'id': 'r9-overflow-modes',
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
     {'id': 'r9-casts',
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
     {'id': 'r9-popcount',
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
     {'id': 'r9-pydivmod',
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
     {'id': 'r9-float-eq',
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
     {'id': 'r9-tuple-minmax',
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
     {'id': 'r9-array-reverse',
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
     {'id': 'r9-text-stats',
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
     {'id': 'r9-utf8-hex',
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
     {'id': 'r9-endianness',
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
     {'id': 'r9-twos-complement',
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
     {'id': 'r9-sizes',
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
     {'id': 'r9-stack-direction',
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
     {'id': 'r9-recursion-limit',
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
     {'id': 'r9-calendar',
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
     {'id': 'r9-gcd-lcm',
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
     {'id': 'r9-to-base',
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
                   '64 base 8: 100']},
     {'id': 'r9-getsizeof',
      'mode': 'rust',
      'title': 'Размеры вместо getsizeof',
      'statement': 'В Python sys.getsizeof(5) возвращает 28. Напечатайте через size_of размеры в байтах для '
                   'i8, i16, i32, i64, i128, f32, f64, bool, char, (u8, u32), [i32; 10] — одной строкой '
                   'через пробел: «1 2 4 8 16 4 8 1 4 8 40».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '1 2 4 8 16 4 8 1 4 8 40',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'use std::mem::size_of; size_of::<T>().',
      'standalone': True,
      'expected': ['1 2 4 8 16 4 8 1 4 8 40']},
     {'id': 'r9-div-modes',
      'mode': 'rust',
      'title': 'Четыре результата деления',
      'statement': 'Для a = -7 и b = 2 напечатайте четыре строки: a / b, a % b, a.div_euclid(b), '
                   'a.rem_euclid(b). Ожидается «-3», «-1», «-4», «1» (в Python: -7 // 2 = -4 и -7 % 2 = 1).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '-3\n'
                   '-1\n'
                   '-4\n'
                   '1',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'div_euclid и rem_euclid совпадают с питоновскими // и % при положительном делителе.',
      'standalone': True,
      'expected': ['-3', '-1', '-4', '1']},
     {'id': 'r9-u128-factorial',
      'mode': 'rust',
      'title': 'Факториал 30 без bigint',
      'statement': 'В Python 30! считается без проблем. В Rust он помещается в u128. Посчитайте 30! циклом и '
                   'напечатайте «265252859812191058636308480000000».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '265252859812191058636308480000000',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Тип u128: let mut f: u128 = 1;',
      'standalone': True,
      'expected': ['265252859812191058636308480000000']},
     {'id': 'r9-fact-checked',
      'mode': 'rust',
      'title': 'Факториал с проверкой переполнения',
      'statement': 'Напишите функцию fact(n: u32) -> Option<u64>: n! или None, если результат не помещается '
                   'в u64 (используйте checked_mul).',
      'starter': 'fn fact(n: u32) -> Option<u64> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", fact(5));\n'
                '    println!("{:?}", fact(20));\n'
                '    println!("{:?}", fact(21));\n'
                '    println!("{:?}", fact(0));\n'
                '}\n',
      'hint': 'checked_mul возвращает Option; оператор ? выходит из функции с None.',
      'expected': ['Some(120)', 'Some(2432902008176640000)', 'None', 'Some(1)']},
     {'id': 'r9-py-round',
      'mode': 'rust',
      'title': 'Округление как в Python',
      'statement': 'Напишите функцию py_round(x: f64) -> i64: округление к ближайшему целому, а половинки — '
                   'к чётному (как round в Python: 0.5 → 0, 1.5 → 2, 2.5 → 2, −0.5 → 0, −1.5 → −2).',
      'starter': 'fn py_round(x: f64) -> i64 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for x in [0.5, 1.5, 2.5, -0.5, -1.5, 2.4, 2.6, -2.5] {\n'
                '        print!("{} ", py_round(x));\n'
                '    }\n'
                '    println!();\n'
                '}\n',
      'hint': 'x.round() округляет половинки от нуля; если результат нечётный, а x — ровно половинка, '
              'вернитесь на единицу к нулю.',
      'expected': ['0 2 2 0 -2 2 3 -2']},
     {'id': 'r9-py-index',
      'mode': 'rust',
      'title': 'Отрицательные индексы',
      'statement': 'Напишите функцию py_get(v: &[i32], i: i32) -> Option<i32>: как v[i] в Python — '
                   'отрицательный индекс считается с конца, выход за границы даёт None.',
      'starter': 'fn py_get(v: &[i32], i: i32) -> Option<i32> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let v = [10, 20, 30];\n'
                '    println!("{:?}", py_get(&v, 0));\n'
                '    println!("{:?}", py_get(&v, -1));\n'
                '    println!("{:?}", py_get(&v, -3));\n'
                '    println!("{:?}", py_get(&v, 3));\n'
                '    println!("{:?}", py_get(&v, -4));\n'
                '}\n',
      'hint': 'Приведите len к i32, прибавьте его к отрицательному индексу и проверьте границы.',
      'expected': ['Some(10)', 'Some(30)', 'Some(10)', 'None', 'None']},
     {'id': 'r9-to-bytes',
      'mode': 'rust',
      'title': 'to_bytes вручную',
      'statement': 'Напишите функции to_le(n: u32) -> [u8; 4] и from_le(b: [u8; 4]) -> u32 без to_le_bytes — '
                   'через сдвиги >> и << и маску 0xFF.',
      'starter': 'fn to_le(n: u32) -> [u8; 4] {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn from_le(b: [u8; 4]) -> u32 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", to_le(258));\n'
                '    println!("{:?}", to_le(0xDEADBEEF));\n'
                '    println!("{}", from_le([2, 1, 0, 0]));\n'
                '    println!("{}", from_le(to_le(123456789)));\n'
                '}\n',
      'hint': 'Младший байт — n & 0xFF; следующий — (n >> 8) & 0xFF.',
      'expected': ['[2, 1, 0, 0]', '[239, 190, 173, 222]', '258', '123456789']},
     {'id': 'r9-struct-layout',
      'mode': 'rust',
      'title': 'Размер структуры',
      'statement': 'Объявите две структуры с атрибутом #[repr(C)]: A { a: u8, b: u32, c: u8 } и B { b: u32, '
                   'a: u8, c: u8 }. Напечатайте size_of::<A>() и size_of::<B>(): «12» и «8» — из-за добивки '
                   'между полями.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '12\n'
                   '8',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': '#[repr(C)] фиксирует порядок полей; порядок влияет на размер.',
      'standalone': True,
      'expected': ['12', '8']},
     {'id': 'r9-strings-len',
      'mode': 'rust',
      'title': 'len в байтах и в символах',
      'statement': 'Для слов «привет», «hello», «日本語», «😀» напечатайте по строке: слово, число байт и число '
                   'символов через пробел: «привет 12 6», «hello 5 5», «日本語 9 3», «😀 4 1».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'привет 12 6\n'
                   'hello 5 5\n'
                   '日本語 9 3\n'
                   '😀 4 1',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'len() — байты, chars().count() — символы.',
      'standalone': True,
      'expected': ['привет 12 6', 'hello 5 5', '日本語 9 3', '😀 4 1']},
     {'id': 'r9-copy-vs-clone',
      'mode': 'rust',
      'title': 'Копия строки',
      'statement': 'Создайте a = String::from("раст"), клон b = a.clone(), допишите к b строку "!" и '
                   'напечатайте обе: «раст» и «раст!». В Python для этого пришлось бы вызывать copy.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'раст\n'
                   'раст!',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'clone() делает полную копию, поэтому a остаётся цела.',
      'standalone': True,
      'expected': ['раст', 'раст!']},
     {'id': 'r9-bool-sum',
      'mode': 'rust',
      'title': 'bool — не число',
      'statement': 'В Python sum([True, False, True]) = 2. В Rust bool нельзя складывать. Посчитайте число '
                   'true в векторе [true, false, true, true, false] двумя способами: фильтром '
                   '(iter().filter(|b| **b).count()) и приведением (b as i32). Напечатайте две строки «3» и '
                   '«3».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '3\n'
                   '3',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'true as i32 == 1; *x разыменовывает ссылку.',
      'standalone': True,
      'expected': ['3', '3']},
     {'id': 'r9-mixed-average',
      'mode': 'rust',
      'title': 'Среднее без смешивания типов',
      'statement': 'В Python sum(v) / len(v) работает сразу. Для v = [3, 4, 4, 6] из i32 напечатайте среднее '
                   'как дробное с двумя знаками: «4.25».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '4.25',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Приведите и сумму, и длину к f64.',
      'standalone': True,
      'expected': ['4.25']}]}
