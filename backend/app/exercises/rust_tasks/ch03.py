"""Задачи книги «Изучаем Rust»: глава 3 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {3: [{'id': 'r3-i32-default',
      'mode': 'rust',
      'title': 'Целое по умолчанию',
      'statement': 'Объявите n = 2147483647 (это i32::MAX) и напечатайте n. Затем напечатайте значение '
                   'константы i32::MIN. Две строки.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '2147483647\n'
                   '-2147483648',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'i32::MIN — константа типа; печатается как обычное число.',
      'standalone': True,
      'expected': ['2147483647', '-2147483648']},
     {'id': 'r3-u8-range',
      'mode': 'rust',
      'title': 'Границы u8 и i8',
      'statement': 'Напечатайте через пробел u8::MIN, u8::MAX, i8::MIN, i8::MAX: «0 255 -128 127».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '0 255 -128 127',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'println!("{} {} {} {}", u8::MIN, …);',
      'standalone': True,
      'expected': ['0 255 -128 127']},
     {'id': 'r3-i64-big',
      'mode': 'rust',
      'title': 'Большое число',
      'statement': 'Объявите big: i64 = 5_000_000_000 и напечатайте big * 2 («10000000000»). С типом i32 '
                   'такое число не поместилось бы.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '10000000000',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Явный тип i64 после двоеточия.',
      'standalone': True,
      'expected': ['10000000000']},
     {'id': 'r3-size-of',
      'mode': 'rust',
      'title': 'Размеры типов',
      'statement': 'Напечатайте размеры в байтах типов u8, i32, f64, char, bool — по одному на строке: 1, 4, '
                   '8, 4, 1. Функция: std::mem::size_of::<T>().\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '1\n'
                   '4\n'
                   '8\n'
                   '4\n'
                   '1',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Тип указывают в угловых скобках: size_of::<u8>().',
      'standalone': True,
      'expected': ['1', '4', '8', '4', '1']},
     {'id': 'r3-int-division',
      'mode': 'rust',
      'title': 'Целое деление и остаток',
      'statement': 'Напечатайте три строки: 17 / 5, 17 % 5 и 17.0 / 5.0. Ожидается «3», «2» и «3.4».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '3\n'
                   '2\n'
                   '3.4',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Целые числа дают целый результат, дробные — дробный.',
      'standalone': True,
      'expected': ['3', '2', '3.4']},
     {'id': 'r3-neg-rem',
      'mode': 'rust',
      'title': 'Остаток с отрицательным',
      'statement': 'Напечатайте -7 / 2, -7 % 2 и (-7_i32).rem_euclid(2) — по строке: «-3», «-1», «1». '
                   'Остаток в Rust берёт знак делимого, rem_euclid — всегда неотрицательный.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '-3\n'
                   '-1\n'
                   '1',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'В питоне -7 // 2 = -4, а в расте целое деление отсекает к нулю.',
      'standalone': True,
      'expected': ['-3', '-1', '1']},
     {'id': 'r3-pow',
      'mode': 'rust',
      'title': 'Степени',
      'statement': 'Напечатайте 2^10 (методом pow для целого) и 1.5^3 (методом powi для дробного): «1024» и '
                   '«3.375».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '1024\n'
                   '3.375',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': '2_i32.pow(10); 1.5_f64.powi(3)',
      'standalone': True,
      'expected': ['1024', '3.375']},
     {'id': 'r3-checked',
      'mode': 'rust',
      'title': 'checked_add',
      'statement': 'Напечатайте результат 250_u8.checked_add(5) и 250_u8.checked_add(10) — по строке. Метод '
                   'возвращает Option: «Some(255)» и «None». Для вывода Option используйте {:?}.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'Some(255)\n'
                   'None',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'println!("{:?}", …) — отладочный вывод.',
      'standalone': True,
      'expected': ['Some(255)', 'None']},
     {'id': 'r3-wrapping',
      'mode': 'rust',
      'title': 'Оборот по кругу',
      'statement': 'Напечатайте 250_u8.wrapping_add(10) («4»), 250_u8.saturating_add(10) («255») и '
                   '5_u8.wrapping_sub(10) («251») — три строки.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '4\n'
                   '255\n'
                   '251',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'wrapping — по кругу, saturating — упирается в границу.',
      'standalone': True,
      'expected': ['4', '255', '251']},
     {'id': 'r3-overflowing',
      'mode': 'rust',
      'title': 'overflowing_add',
      'statement': 'Напечатайте 200_u8.overflowing_add(100) и 20_u8.overflowing_add(100) — результат пара: '
                   '«(44, true)» и «(120, false)». Для пары используйте {:?}.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '(44, true)\n'
                   '(120, false)',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Пара (результат, было_ли_переполнение).',
      'standalone': True,
      'expected': ['(44, true)', '(120, false)']},
     {'id': 'r3-fix-overflow',
      'mode': 'rust',
      'title': 'Исправьте: константа не влезает',
      'statement': 'Программа не собирается: число 300 не помещается в u8. Замените тип на подходящий (u16), '
                   'чтобы напечатать «300».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '300',
      'starter': 'fn main() {\n    let x: u8 = 300;\n    println!("{}", x);\n}\n',
      'driver': '',
      'hint': 'u8 вмещает до 255; u16 — до 65535.',
      'standalone': True,
      'expected': ['300']},
     {'id': 'r3-hex-bin',
      'mode': 'rust',
      'title': 'Системы счисления',
      'statement': 'Напечатайте число 255 как «ff» (формат {:x}), как «11111111» (формат {:b}) и как «377» '
                   '(формат {:o}) — три строки.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'ff\n'
                   '11111111\n'
                   '377',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': '{:x} — шестнадцатеричная, {:b} — двоичная, {:o} — восьмеричная запись.',
      'standalone': True,
      'expected': ['ff', '11111111', '377']},
     {'id': 'r3-f64-ops',
      'mode': 'rust',
      'title': 'Дробная арифметика',
      'statement': 'Напечатайте две строки: 10.0 / 4.0 и 10.0 % 4.0 — «2.5» и «2».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '2.5\n'
                   '2',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Остаток определён и для дробных чисел.',
      'standalone': True,
      'expected': ['2.5', '2']},
     {'id': 'r3-float-compare',
      'mode': 'rust',
      'title': 'Неточность дробных',
      'statement': 'Напечатайте 0.1 + 0.2 (будет «0.30000000000000004»), затем результат сравнения 0.1 + 0.2 '
                   '== 0.3 («false»), затем сравнение с допуском: ((0.1 + 0.2) - 0.3).abs() < 1e-9 '
                   '(«true»).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '0.30000000000000004\n'
                   'false\n'
                   'true',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Дробные числа сравнивают через допуск, а не через ==.',
      'standalone': True,
      'expected': ['0.30000000000000004', 'false', 'true']},
     {'id': 'r3-round-family',
      'mode': 'rust',
      'title': 'Округление',
      'statement': 'x = 2.5. Напечатайте x.floor(), x.ceil(), x.round(), x.trunc() — по строке: «2», «3», '
                   '«3», «2» (дробные результаты, печатаются без .0 при выводе через {}).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '2\n'
                   '3\n'
                   '3\n'
                   '2',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'floor — вниз, ceil — вверх, round — к ближайшему (0.5 — от нуля), trunc — отбросить дробь.',
      'standalone': True,
      'expected': ['2', '3', '3', '2']},
     {'id': 'r3-sqrt-hypot',
      'mode': 'rust',
      'title': 'Гипотенуза',
      'statement': 'Катеты 3.0 и 4.0. Напечатайте длину гипотенузы через sqrt: «5».\n\nОжидаемый вывод:\n5',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': '(a * a + b * b).sqrt() — метод sqrt у дробного числа.',
      'standalone': True,
      'expected': ['5']},
     {'id': 'r3-nan-inf',
      'mode': 'rust',
      'title': 'inf и NaN',
      'statement': 'Напечатайте 1.0 / 0.0, -1.0 / 0.0 и 0.0 / 0.0 (три строки: «inf», «-inf», «NaN»), а '
                   'затем (0.0_f64 / 0.0).is_nan() («true»).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'inf\n'
                   '-inf\n'
                   'NaN\n'
                   'true',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Тип f64 указан, чтобы компилятор понял метод is_nan.',
      'standalone': True,
      'expected': ['inf', '-inf', 'NaN', 'true']},
     {'id': 'r3-as-cast',
      'mode': 'rust',
      'title': 'Приведения as',
      'statement': 'Напечатайте по строке: 3.99_f64 as i32 («3»), 300_i32 as u8 («44»), -1_i32 as u32 '
                   '(«4294967295»), 65_u8 as char («A»).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '3\n'
                   '44\n'
                   '4294967295\n'
                   'A',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'as отрезает биты и дробную часть.',
      'standalone': True,
      'expected': ['3', '44', '4294967295', 'A']},
     {'id': 'r3-fix-mix',
      'mode': 'rust',
      'title': 'Исправьте: смешанные типы',
      'statement': 'Нельзя сложить i32 и f64 без преобразования. Исправьте программу так, чтобы вывод был '
                   '«7.5».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '7.5',
      'starter': 'fn main() {\n    let a: i32 = 3;\n    let b: f64 = 4.5;\n    println!("{}", a + b);\n}\n',
      'driver': '',
      'hint': 'a as f64 + b',
      'standalone': True,
      'expected': ['7.5']},
     {'id': 'r3-from',
      'mode': 'rust',
      'title': 'From без потерь',
      'statement': 'Объявите a: u8 = 200 и b: i64 = 5_000_000_000. Напечатайте сумму i64::from(a) + b: '
                   '«5000000200».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '5000000200',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'i64::from(a) безопасно расширяет u8 до i64.',
      'standalone': True,
      'expected': ['5000000200']},
     {'id': 'r3-try-from',
      'mode': 'rust',
      'title': 'try_from',
      'statement': 'Напечатайте u8::try_from(200_i32).is_ok() и u8::try_from(300_i32).is_ok() — «true» и '
                   '«false».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'true\n'
                   'false',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'try_from возвращает Result; .is_ok() — «получилось ли».',
      'standalone': True,
      'expected': ['true', 'false']},
     {'id': 'r3-parse',
      'mode': 'rust',
      'title': 'Разбор числа из текста',
      'statement': 'Разберите строки «41» и «3.5» в i32 и f64 методом parse с unwrap. Напечатайте сумму n + '
                   '1 и произведение x * 2.0: «42» и «7».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '42\n'
                   '7',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'let n: i32 = "41".parse().unwrap(); — тип берётся из аннотации.',
      'standalone': True,
      'expected': ['42', '7']},
     {'id': 'r3-parse-fail',
      'mode': 'rust',
      'title': 'parse с ошибкой',
      'statement': 'Для строк «12», «abc» и «-5» напечатайте, получилось ли превратить в i32: «true», '
                   '«false», «true» (метод parse::<i32>().is_ok()).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'true\n'
                   'false\n'
                   'true',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Тип можно указать через turbofish: parse::<i32>().',
      'standalone': True,
      'expected': ['true', 'false', 'true']},
     {'id': 'r3-bool-ops',
      'mode': 'rust',
      'title': 'Логика',
      'statement': 'Пусть a = true, b = false. Напечатайте a && b, a || b, !a, a && !b — по строке: «false», '
                   '«true», «false», «true».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'false\n'
                   'true\n'
                   'false\n'
                   'true',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': '&& — «и», || — «или», ! — «не».',
      'standalone': True,
      'expected': ['false', 'true', 'false', 'true']},
     {'id': 'r3-compare-chain',
      'mode': 'rust',
      'title': 'Сравнения',
      'statement': 'x = 15. Напечатайте результаты: x > 10, x == 15, x != 15, x >= 20, и попадание в '
                   'диапазон x >= 10 && x <= 20 — пять строк: true, true, false, false, true.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'true\n'
                   'true\n'
                   'false\n'
                   'false\n'
                   'true',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Результат сравнения — bool, его можно печатать прямо.',
      'standalone': True,
      'expected': ['true', 'true', 'false', 'false', 'true']},
     {'id': 'r3-fix-if-int',
      'mode': 'rust',
      'title': 'Исправьте: условие не bool',
      'statement': 'В if стоит число — это ошибка. Исправьте условие так, чтобы напечатать «не ноль» для n = '
                   '5.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'не ноль',
      'starter': 'fn main() {\n    let n = 5;\n    if n {\n        println!("не ноль");\n    }\n}\n',
      'driver': '',
      'hint': 'Условие — явное сравнение n != 0.',
      'standalone': True,
      'expected': ['не ноль']},
     {'id': 'r3-char-basic',
      'mode': 'rust',
      'title': 'Символы',
      'statement': "c = 'ж'. Напечатайте сам символ, затем его код через as u32 («1078»), затем "
                   "c.is_alphabetic() («true»), и '7'.is_numeric() («true») — по строке.\n"
                   '\n'
                   'Ожидаемый вывод:\n'
                   'ж\n'
                   '1078\n'
                   'true\n'
                   'true',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': "'ж' as u32 — код символа в Юникоде.",
      'standalone': True,
      'expected': ['ж', '1078', 'true', 'true']},
     {'id': 'r3-char-case',
      'mode': 'rust',
      'title': 'Регистр символа',
      'statement': "Для 'q' напечатайте c.to_ascii_uppercase() («Q»), для 'Я' — "
                   "c.to_lowercase().next().unwrap() («я») и символ-цифру '8'.to_digit(10).unwrap() + 1 "
                   '(«9») — три строки.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'Q\n'
                   'я\n'
                   '9',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'to_lowercase возвращает итератор — берём первый символ через next().unwrap().',
      'standalone': True,
      'expected': ['Q', 'я', '9']},
     {'id': 'r3-char-shift',
      'mode': 'rust',
      'title': 'Сдвиг по алфавиту',
      'statement': "Возьмите 'a' и напечатайте символ, следующий за ним в таблице (через as u8 + 1 as char): "
                   "«b». Затем так же получите 'z' из 'a' + 25: «z».\n"
                   '\n'
                   'Ожидаемый вывод:\n'
                   'b\n'
                   'z',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': '(c as u8 + 1) as char',
      'standalone': True,
      'expected': ['b', 'z']},
     {'id': 'r3-final-types',
      'mode': 'rust',
      'title': 'Итоговая: сводка типов',
      'statement': "Объявите n: i32 = -17, x: f64 = 2.5, ok: bool = true, c: char = 'Я'. Напечатайте четыре "
                   'строки через пробел в формате «n=-17 x=2.5 ok=true c=Я», затем отдельной строкой n.abs() '
                   'as f64 * x («42.5»).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'n=-17 x=2.5 ok=true c=Я\n'
                   '42.5',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Сначала приведите n.abs() к f64 через as, затем умножьте на x.',
      'standalone': True,
      'expected': ['n=-17 x=2.5 ok=true c=Я', '42.5']}]}
