"""Задачи книги «Изучаем Rust»: глава 26 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {26: [{'id': 'r26-char-class',
       'mode': 'rust',
       'title': 'Классы символов',
       'statement': 'Напишите classify(s: &str) -> (usize, usize, usize, usize): число букв, цифр, '
                    'пробельных и прочих символов (по правилам Unicode: is_alphabetic, is_numeric, '
                    'is_whitespace).',
       'starter': 'fn classify(s: &str) -> (usize, usize, usize, usize) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", classify("Привет, мир 2026!"));\n'
                 '    println!("{:?}", classify(""));\n'
                 '    println!("{:?}", classify("a1 ٣"));\n'
                 '}\n',
       'hint': 'Четыре счётчика и цепочка if / else if.',
       'expected': ['(9, 4, 2, 2)', '(0, 0, 0, 0)', '(1, 2, 1, 0)']},
      {'id': 'r26-hex-digits',
       'mode': 'rust',
       'title': 'Цифры в разных системах',
       'statement': 'Напишите hex_sum(s: &str) -> u32: сумма значений шестнадцатеричных цифр строки '
                    '(to_digit(16)); не-hex-символы пропускаются.',
       'starter': 'fn hex_sum(s: &str) -> u32 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", hex_sum("ff"));\n'
                 '    println!("{}", hex_sum("1A z 0"));\n'
                 '    println!("{}", hex_sum(""));\n'
                 '}\n',
       'hint': 'filter_map(|c| c.to_digit(16))',
       'expected': ['30', '11', '0']},
      {'id': 'r26-from-digit',
       'mode': 'rust',
       'title': 'Число в строку любой системы',
       'statement': 'Напишите to_radix(n: u32, radix: u32) -> String: запись n в системе счисления radix '
                    '(2…36) строчными буквами; для 0 — «0». Используйте char::from_digit.',
       'starter': 'fn to_radix(n: u32, radix: u32) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{} {} {}", to_radix(255, 16), to_radix(5, 2), to_radix(0, 8));\n'
                 '    println!("{}", to_radix(123456, 36));\n'
                 '    println!("{}", to_radix(u32::MAX, 2));\n'
                 '}\n',
       'hint': 'Остатки от деления — цифры в обратном порядке.',
       'expected': ['ff 101 0', '2n9c', '11111111111111111111111111111111']},
      {'id': 'r26-split-multi',
       'mode': 'rust',
       'title': 'Разбить по нескольким разделителям',
       'statement': 'Напишите tokens(s: &str) -> Vec<String>: слова, разделённые любым из символов «,», «;», '
                    '«:» или пробельным; пустые куски пропускаются.',
       'starter': 'fn tokens(s: &str) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", tokens("a, b;c:d  e,,f"));\n'
                 '    println!("{:?}", tokens(""));\n'
                 '    println!("{:?}", tokens(";;;"));\n'
                 '}\n',
       'hint': 'split принимает замыкание-шаблон.',
       'expected': ['["a", "b", "c", "d", "e", "f"]', '[]', '[]']},
      {'id': 'r26-splitn',
       'mode': 'rust',
       'title': 'splitn',
       'statement': 'Напишите parse_cmd(line: &str) -> (String, String): команда и остальная строка. Делить '
                    "по первому пробелу (splitn(2, ' ')); если пробела нет — вторая часть пуста. Остаток не "
                    'триммить.',
       'starter': 'fn parse_cmd(line: &str) -> (String, String) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", parse_cmd("echo hello  world"));\n'
                 '    println!("{:?}", parse_cmd("quit"));\n'
                 '    println!("{:?}", parse_cmd(""));\n'
                 '}\n',
       'hint': "splitn(2, ' ') не делит остаток.",
       'expected': ['("echo", "hello  world")', '("quit", "")', '("", "")']},
      {'id': 'r26-strip-prefix',
       'mode': 'rust',
       'title': 'strip_prefix',
       'statement': 'Напишите command(line: &str) -> String: «ECHO <текст>» → текст; «UP <текст>» → текст в '
                    'верхнем регистре; иначе «неизвестная команда». Используйте strip_prefix.',
       'starter': 'fn command(line: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", command("ECHO привет"));\n'
                 '    println!("{}", command("UP привет"));\n'
                 '    println!("{}", command("DOWN x"));\n'
                 '    println!("[{}]", command("ECHO "));\n'
                 '}\n',
       'hint': 'strip_prefix возвращает Option<&str>.',
       'expected': ['привет', 'ПРИВЕТ', 'неизвестная команда', '[]']},
      {'id': 'r26-split-inclusive',
       'mode': 'rust',
       'title': 'Предложения',
       'statement': 'Напишите sentences(s: &str) -> Vec<String>: разбейте текст на предложения, оставляя '
                    'знак конца (. ! ?) в конце каждого, и уберите пробелы по краям. split_inclusive с '
                    'замыканием.',
       'starter': 'fn sentences(s: &str) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", sentences("Привет. Как дела? Отлично!"));\n'
                 '    println!("{:?}", sentences("без точки"));\n'
                 '    println!("{:?}", sentences(""));\n'
                 '}\n',
       'hint': 'split_inclusive оставляет разделитель в куске.',
       'expected': ['["Привет.", "Как дела?", "Отлично!"]', '["без точки"]', '[]']},
      {'id': 'r26-trim-matches',
       'mode': 'rust',
       'title': 'Убрать обрамление',
       'statement': 'Напишите unquote(s: &str) -> String: убрать с обоих концов любые кавычки «"» и «\'» и '
                    'пробелы (trim_matches с замыканием).',
       'starter': 'fn unquote(s: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("[{}]", unquote("  \\"привет\\"  "));\n'
                 '    println!("[{}]", unquote("\'a b\'"));\n'
                 '    println!("[{}]", unquote("\\"\\""));\n'
                 '}\n',
       'hint': 'trim_matches(|c| …) режет с обоих концов.',
       'expected': ['[привет]', '[a b]', '[]']},
      {'id': 'r26-match-indices',
       'mode': 'rust',
       'title': 'Позиции вхождений',
       'statement': 'Напишите positions(text: &str, pat: &str) -> Vec<usize>: байтовые позиции всех '
                    '(непересекающихся) вхождений pat (match_indices); pat не пуст.',
       'starter': 'fn positions(text: &str, pat: &str) -> Vec<usize> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", positions("abcabcab", "ab"));\n'
                 '    println!("{:?}", positions("привет привет", "ив"));\n'
                 '    println!("{:?}", positions("aaaa", "aa"));\n'
                 '}\n',
       'hint': 'match_indices возвращает (позиция, совпадение).',
       'expected': ['[0, 3, 6]', '[4, 17]', '[0, 2]']},
      {'id': 'r26-rfind-ext',
       'mode': 'rust',
       'title': 'Расширение файла',
       'statement': 'Напишите extension(name: &str) -> Option<&str>: расширение после последней точки; None, '
                    'если точки нет, точка в начале (скрытый файл «.bashrc») или в конце.',
       'starter': 'fn extension(name: &str) -> Option<&str> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", extension("archive.tar.gz"));\n'
                 '    println!("{:?}", extension("README"));\n'
                 '    println!("{:?}", extension(".bashrc"));\n'
                 '    println!("{:?}", extension("file."));\n'
                 '}\n',
       'hint': "rfind('.') и срез после точки.",
       'expected': ['Some("gz")', 'None', 'None', 'None']},
      {'id': 'r26-string-edit',
       'mode': 'rust',
       'title': 'Правки на месте',
       'statement': 'Напишите censor(s: &mut String, bad: &str): заменить первое вхождение bad звёздочками '
                    'той же длины в символах (replace_range) — если bad нет, ничего не менять.',
       'starter': 'fn censor(s: &mut String, bad: &str) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut s = String::from("это плохое слово");\n'
                 '    censor(&mut s, "плохое");\n'
                 '    println!("{}", s);\n'
                 '    censor(&mut s, "нет");\n'
                 '    println!("{}", s);\n'
                 '}\n',
       'hint': 'find даёт байтовый индекс; диапазон — i..i + bad.len().',
       'expected': ['это ****** слово', 'это ****** слово']},
      {'id': 'r26-retain-clean',
       'mode': 'rust',
       'title': 'Оставить только буквы',
       'statement': 'Напишите letters_only(s: &mut String): оставьте в строке только буквы (retain + '
                    'is_alphabetic).',
       'starter': 'fn letters_only(s: &mut String) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut s = String::from("a1б2 в!3");\n'
                 '    letters_only(&mut s);\n'
                 '    println!("{}", s);\n'
                 '}\n',
       'hint': 's.retain(|c| c.is_alphabetic())',
       'expected': ['aбв']},
      {'id': 'r26-truncate-char',
       'mode': 'rust',
       'title': 'Обрезать по символам',
       'statement': 'Напишите truncate_chars(s: &str, n: usize) -> String: первые n символов; если строка '
                    'длиннее, в конце «…». (не байтов; не резать посреди символа).',
       'starter': 'fn truncate_chars(s: &str, n: usize) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", truncate_chars("привет, мир", 6));\n'
                 '    println!("{}", truncate_chars("мир", 6));\n'
                 '    println!("{}", truncate_chars("😀😀😀😀", 2));\n'
                 '    println!("[{}]", truncate_chars("", 3));\n'
                 '}\n',
       'hint': 'chars().take(n).collect::<String>()',
       'expected': ['привет…', 'мир', '😀😀…', '[]']},
      {'id': 'r26-fmt-table',
       'mode': 'rust',
       'title': 'Таблица',
       'statement': 'Напишите table(rows: &[(&str, f64)]) -> Vec<String>: строки «<имя, ширина по самому '
                    'длинному> | <число вправо в поле 8 с двумя знаками>»; имя — по левому краю.',
       'starter': 'fn table(rows: &[(&str, f64)]) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for l in table(&[("яблоко", 3.5), ("груша", 12.349), ("слива", 100.0)]) {\n'
                 '        println!("{}", l);\n'
                 '    }\n'
                 '}\n',
       'hint': '{:<w$} и {:>8.2}',
       'expected': ['яблоко |     3.50', 'груша  |    12.35', 'слива  |   100.00']},
      {'id': 'r26-fmt-radix',
       'mode': 'rust',
       'title': 'Системы счисления форматом',
       'statement': 'Напишите formats(n: u32) -> Vec<String>: n в десятичной, шестнадцатеричной (с префиксом '
                    '0x, 4 цифры с нулями), двоичной (8 цифр с нулями) и восьмеричной системах: для 255 → '
                    '["255", "0x00ff", "11111111", "377"].',
       'starter': 'fn formats(n: u32) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n    println!("{:?}", formats(255));\n    println!("{:?}", formats(5));\n}\n',
       'hint': '{:#06x}, {:08b}, {:o}',
       'expected': ['["255", "0x00ff", "11111111", "377"]', '["5", "0x0005", "00000101", "5"]']},
      {'id': 'r26-fmt-sign',
       'mode': 'rust',
       'title': 'Знак и точность',
       'statement': 'Напишите signed(x: f64) -> String: число с явным знаком и двумя знаками после запятой, '
                    'выровненное по центру в поле 9 символов с заполнителем «.»: signed(3.14159) = '
                    '«..+3.14..».',
       'starter': 'fn signed(x: f64) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", signed(3.14159));\n'
                 '    println!("{}", signed(-0.5));\n'
                 '    println!("{}", signed(100.0));\n'
                 '}\n',
       'hint': '{:.^+9.2} — заполнитель «.», центр, знак, ширина 9, точность 2.',
       'expected': ['..+3.14..', '..-0.50..', '.+100.00.']},
      {'id': 'r26-fmt-dynamic',
       'mode': 'rust',
       'title': 'Ширина из аргумента',
       'statement': 'Напишите pad_left(s: &str, width: usize, fill: char) -> String: выровняйте s вправо до '
                    'ширины width в символах, добавляя слева символ fill (формат не принимает заполнитель из '
                    'переменной — добавьте его вручную). Если s не короче width — вернуть как есть.',
       'starter': 'fn pad_left(s: &str, width: usize, fill: char) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", pad_left("42", 5, \'0\'));\n'
                 '    println!("{}", pad_left("привет", 3, \'-\'));\n'
                 '    println!("{}", pad_left("", 3, \'*\'));\n'
                 '}\n',
       'hint': 'Количество заполнителей — width - n.',
       'expected': ['00042', 'привет', '***']},
      {'id': 'r26-display-money',
       'mode': 'rust',
       'title': 'Display для денег',
       'statement': 'Структура Money(i64) хранит копейки. Реализуйте Display: «123.05 ₽» для 12305, «-0.99 '
                    '₽» для −99, «0.00 ₽» для 0.',
       'starter': 'use std::fmt;\n'
                  '\n'
                  'struct Money(i64);\n'
                  '\n'
                  'impl fmt::Display for Money {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", Money(12305));\n'
                 '    println!("{}", Money(-99));\n'
                 '    println!("{}", Money(0));\n'
                 '    println!("{}", Money(5));\n'
                 '}\n',
       'hint': 'Знак отдельно, рубли a / 100, копейки {:02}.',
       'expected': ['123.05 ₽', '-0.99 ₽', '0.00 ₽', '0.05 ₽']},
      {'id': 'r26-display-pad',
       'mode': 'rust',
       'title': 'Display, уважающий ширину',
       'statement': 'Структура Name(String) реализует Display через f.pad(&self.0), чтобы работали ширина и '
                    'выравнивание: «[{:>8}]» для Name("Аня") даёт «[     Аня]».',
       'starter': 'use std::fmt;\n'
                  '\n'
                  'struct Name(String);\n'
                  '\n'
                  'impl fmt::Display for Name {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let n = Name(String::from("Аня"));\n'
                 '    println!("[{:>8}]", n);\n'
                 '    println!("[{:<8}]", n);\n'
                 '    println!("[{:^8}]", n);\n'
                 '    println!("[{:.2}]", n);\n'
                 '}\n',
       'hint': 'f.pad учитывает ширину, выравнивание и точность (обрезку).',
       'expected': ['[     Аня]', '[Аня     ]', '[  Аня   ]', '[Ан]']},
      {'id': 'r26-debug-manual',
       'mode': 'rust',
       'title': 'Debug вручную',
       'statement': 'Структура User { name: String, age: u32, secret: String } — реализуйте Debug вручную '
                    'через debug_struct так, чтобы поле secret не печаталось (вывод «User { name: "Аня", '
                    'age: 30 }»).',
       'starter': 'use std::fmt;\n'
                  '\n'
                  'struct User {\n'
                  '    name: String,\n'
                  '    age: u32,\n'
                  '    secret: String,\n'
                  '}\n'
                  '\n'
                  'impl fmt::Debug for User {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let u = User { name: String::from("Аня"), age: 30, secret: String::from("пароль") };\n'
                 '    println!("{:?}", u);\n'
                 '    println!("{:#?}", u);\n'
                 '    let _ = &u.secret;\n'
                 '}\n',
       'hint': 'debug_struct("User").field(…).finish()',
       'expected': ['User { name: "Аня", age: 30 }', 'User {', '    name: "Аня",', '    age: 30,', '}']},
      {'id': 'r26-display-matrix',
       'mode': 'rust',
       'title': 'Display матрицы',
       'statement': 'Структура Matrix(Vec<Vec<i32>>) реализует Display: строки через перевод строки (без '
                    'пустой строки в конце), числа в строке через пробел, каждое в поле шириной 3 вправо: «  '
                    '1  2», «  3  4».',
       'starter': 'use std::fmt;\n'
                  '\n'
                  'struct Matrix(Vec<Vec<i32>>);\n'
                  '\n'
                  'impl fmt::Display for Matrix {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let m = Matrix(vec![vec![1, 2], vec![30, -4]]);\n'
                 '    println!("{}", m);\n'
                 '    println!("[{}]", Matrix(vec![]));\n'
                 '}\n',
       'hint': 'writeln!(f)? между строками, write!(f, "{:>3}", x)? для чисел.',
       'expected': ['  1  2', ' 30 -4', '[]']},
      {'id': 'r26-parse-kv',
       'mode': 'rust',
       'title': 'Разбор «ключ=значение»',
       'statement': 'Напишите parse_kv(line: &str) -> Option<(String, i32)>: «name = 42» → ("name", 42); '
                    'None, если нет «=», ключ пуст или значение не целое.',
       'starter': 'fn parse_kv(line: &str) -> Option<(String, i32)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", parse_kv("name = 42"));\n'
                 '    println!("{:?}", parse_kv("x=-7"));\n'
                 '    println!("{:?}", parse_kv("= 5"));\n'
                 '    println!("{:?}", parse_kv("a = b"));\n'
                 '    println!("{:?}", parse_kv("нет"));\n'
                 '}\n',
       'hint': 'split_once, trim, parse().ok()?',
       'expected': ['Some(("name", 42))', 'Some(("x", -7))', 'None', 'None', 'None']},
      {'id': 'r26-parse-csv',
       'mode': 'rust',
       'title': 'CSV-строка в числа',
       'statement': 'Напишите parse_row(s: &str) -> Result<Vec<f64>, String>: числа через запятую (с '
                    'пробелами вокруг); при ошибке — Err(«плохое поле: <поле>»).',
       'starter': 'fn parse_row(s: &str) -> Result<Vec<f64>, String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", parse_row("1.5, 2, -3e2"));\n'
                 '    println!("{:?}", parse_row("1, x, 3"));\n'
                 '    println!("{:?}", parse_row(""));\n'
                 '}\n',
       'hint': 'collect::<Result<Vec<_>, _>>()',
       'expected': ['Ok([1.5, 2.0, -300.0])', 'Err("плохое поле: x")', 'Err("плохое поле: ")']},
      {'id': 'r26-parse-radix',
       'mode': 'rust',
       'title': 'Число с префиксом',
       'statement': 'Напишите parse_num(s: &str) -> Option<i64>: десятичное, с префиксом 0x (hex), 0b '
                    '(двоичное) или 0o (восьмеричное); знак «-» допустим перед префиксом. Подчёркивания '
                    'игнорируются.',
       'starter': 'fn parse_num(s: &str) -> Option<i64> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for s in ["42", "0xff", "-0b101", "0o17", "1_000", "0xZZ", "", "-"] {\n'
                 '        println!("{:?}", parse_num(s));\n'
                 '    }\n'
                 '}\n',
       'hint': 'Сначала снимите знак и подчёркивания, затем проверьте префиксы.',
       'expected': ['Some(42)', 'Some(255)', 'Some(-5)', 'Some(15)', 'Some(1000)', 'None', 'None', 'None']},
      {'id': 'r26-word-freq-fmt',
       'mode': 'rust',
       'title': 'Отчёт о частотах',
       'statement': 'Напишите report(text: &str) -> Vec<String>: слова в нижнем регистре и их частоты; '
                    'строки «слово: N», по убыванию N, при равных — по алфавиту.',
       'starter': 'fn report(text: &str) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for l in report("Да нет да НЕТ да может") {\n'
                 '        println!("{}", l);\n'
                 '    }\n'
                 '}\n',
       'hint': 'Счётчики в Vec пар, затем sort_by.',
       'expected': ['да: 3', 'нет: 2', 'может: 1']},
      {'id': 'r26-wrap-text',
       'mode': 'rust',
       'title': 'Выравнивание по ширине',
       'statement': 'Напишите center_lines(text: &str, width: usize) -> Vec<String>: каждую строку текста '
                    '(lines) выровнять по центру в поле width (форматом {:^w$}); строки длиннее width не '
                    'менять.',
       'starter': 'fn center_lines(text: &str, width: usize) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for l in center_lines("а\\nбвг\\nдежзи", 6) {\n'
                 '        println!("[{}]", l);\n'
                 '    }\n'
                 '    println!("{}", center_lines("", 5).len());\n'
                 '}\n',
       'hint': 'format!("{:^w$}", l, w = width)',
       'expected': ['[  а   ]', '[ бвг  ]', '[дежзи ]', '0']},
      {'id': 'r26-case-convert',
       'mode': 'rust',
       'title': 'snake_case в CamelCase',
       'statement': 'Напишите to_camel(s: &str) -> String: «my_var_name» → «MyVarName» (разделитель «_»; '
                    'пустые куски пропускаются).',
       'starter': 'fn to_camel(s: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", to_camel("my_var_name"));\n'
                 '    println!("{}", to_camel("__a__b_"));\n'
                 '    println!("[{}]", to_camel(""));\n'
                 '    println!("{}", to_camel("привет_мир"));\n'
                 '}\n',
       'hint': 'Первая буква каждого куска — в верхний регистр.',
       'expected': ['MyVarName', 'AB', '[]', 'ПриветМир']},
      {'id': 'r26-camel-to-snake',
       'mode': 'rust',
       'title': 'CamelCase в snake_case',
       'statement': 'Напишите to_snake(s: &str) -> String: «MyVarName» → «my_var_name» (перед каждой '
                    'заглавной, кроме первой буквы, ставится «_»).',
       'starter': 'fn to_snake(s: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", to_snake("MyVarName"));\n'
                 '    println!("{}", to_snake("x"));\n'
                 '    println!("{}", to_snake("ПриветМир"));\n'
                 '    println!("[{}]", to_snake(""));\n'
                 '}\n',
       'hint': 'out.extend(c.to_lowercase()) — to_lowercase возвращает итератор.',
       'expected': ['my_var_name', 'x', 'привет_мир', '[]']},
      {'id': 'r26-caesar-unicode',
       'mode': 'rust',
       'title': 'Шифр Виженера',
       'statement': 'Напишите vigenere(text: &str, key: &str) -> String: шифр Виженера для латинских '
                    'строчных букв (a–z); ключ — строчные буквы, не пуст; ключ продвигается только на буквах '
                    'текста; остальные символы без изменений.',
       'starter': 'fn vigenere(text: &str, key: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", vigenere("attack at dawn", "lemon"));\n'
                 '    println!("{}", vigenere("abc", "a"));\n'
                 '    println!("{}", vigenere("привет", "b"));\n'
                 '}\n',
       'hint': 'Позиция в ключе j увеличивается только на латинской букве.',
       'expected': ['lxfopv ef rnhr', 'abc', 'привет']},
      {'id': 'r26-utf8-len',
       'mode': 'rust',
       'title': 'Байты символов',
       'statement': 'Напишите byte_lens(s: &str) -> Vec<(char, usize)>: каждый символ и сколько байт он '
                    'занимает в UTF-8 (len_utf8).',
       'starter': 'fn byte_lens(s: &str) -> Vec<(char, usize)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", byte_lens("aя世😀"));\n'
                 '    println!("{:?}", byte_lens(""));\n'
                 '}\n',
       'hint': 'c.len_utf8() — 1…4.',
       'expected': ["[('a', 1), ('я', 2), ('世', 3), ('😀', 4)]", '[]']}]}
