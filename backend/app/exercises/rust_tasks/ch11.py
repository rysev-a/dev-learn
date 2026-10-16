"""Задачи книги «Изучаем Rust»: глава 11 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {11: [{'id': 'r11-char-len',
       'mode': 'rust',
       'title': 'len в символах',
       'statement': 'Python: len(s). Напишите char_len(s: &str) -> usize — число символов (не байтов).',
       'starter': 'fn char_len(s: &str) -> usize {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", char_len("привет"));\n'
                 '    println!("{}", char_len("a😀b"));\n'
                 '    println!("{}", char_len(""));\n'
                 '}\n',
       'hint': 's.chars().count()',
       'expected': ['6', '3', '0']},
      {'id': 'r11-first-last',
       'mode': 'rust',
       'title': 's[0] и s[-1]',
       'statement': 'Python: s[0] и s[-1]. Напишите first_last(s: &str) -> Option<(char, char)>: первая и '
                    'последняя буквы или None для пустой строки.',
       'starter': 'fn first_last(s: &str) -> Option<(char, char)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", first_last("привет"));\n'
                 '    println!("{:?}", first_last("я"));\n'
                 '    println!("{:?}", first_last(""));\n'
                 '}\n',
       'hint': 'Оператор ? вернёт None, если буквы нет.',
       'expected': ["Some(('п', 'т'))", "Some(('я', 'я'))", 'None']},
      {'id': 'r11-nth-char',
       'mode': 'rust',
       'title': 'Символ по номеру',
       'statement': 'Python: s[i]. Напишите char_at(s: &str, i: usize) -> Option<char>.',
       'starter': 'fn char_at(s: &str, i: usize) -> Option<char> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", char_at("привет", 2));\n'
                 '    println!("{:?}", char_at("привет", 6));\n'
                 '    println!("{:?}", char_at("", 0));\n'
                 '}\n',
       'hint': 's.chars().nth(i)',
       'expected': ["Some('и')", 'None', 'None']},
      {'id': 'r11-substring',
       'mode': 'rust',
       'title': 'Срез по символам',
       'statement': 'Python: s[a:b] (по символам). Напишите substr(s: &str, a: usize, b: usize) -> String — '
                    'символы с номерами a..b (b не включается), для границ за пределами строки — то, что '
                    'есть.',
       'starter': 'fn substr(s: &str, a: usize, b: usize) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", substr("привет, мир", 0, 6));\n'
                 '    println!("{}", substr("привет, мир", 8, 20));\n'
                 '    println!("{}", substr("abc", 2, 2));\n'
                 '}\n',
       'hint': 'skip(a).take(b - a) по chars().',
       'expected': ['привет', 'мир']},
      {'id': 'r11-strip',
       'mode': 'rust',
       'title': 'strip',
       'statement': 'Python: s.strip(). Напишите clean(s: &str) -> String: обрежьте пробелы по краям и '
                    'сделайте строчными все буквы.',
       'starter': 'fn clean(s: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("[{}]", clean("  Hello World \\n"));\n'
                 '    println!("[{}]", clean("ПРИВЕТ"));\n'
                 '    println!("[{}]", clean("   "));\n'
                 '}\n',
       'hint': 'trim(), затем to_lowercase().',
       'expected': ['[hello world]', '[привет]', '[]']},
      {'id': 'r11-find-minus-one',
       'mode': 'rust',
       'title': 'find без -1',
       'statement': 'Python: s.find(sub) возвращает -1, если нет. Напишите find_py(s: &str, sub: &str) -> '
                    'i32 с таким же поведением, но позиция — номер символа, а не байта.',
       'starter': 'fn find_py(s: &str, sub: &str) -> i32 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", find_py("hello", "ll"));\n'
                 '    println!("{}", find_py("привет", "ве"));\n'
                 '    println!("{}", find_py("abc", "z"));\n'
                 '}\n',
       'hint': 'find даёт байтовую позицию; число символов до неё — s[..i].chars().count().',
       'expected': ['2', '3', '-1']},
      {'id': 'r11-count-sub',
       'mode': 'rust',
       'title': 'str.count',
       'statement': 'Python: s.count(sub). Напишите count_sub(s: &str, sub: &str) -> usize: число '
                    'непересекающихся вхождений (sub не пуста).',
       'starter': 'fn count_sub(s: &str, sub: &str) -> usize {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", count_sub("abababa", "aba"));\n'
                 '    println!("{}", count_sub("мама мыла раму", "ма"));\n'
                 '    println!("{}", count_sub("abc", "z"));\n'
                 '}\n',
       'hint': 's.matches(sub).count()',
       'expected': ['2', '2', '0']},
      {'id': 'r11-replace-first',
       'mode': 'rust',
       'title': 'replace с лимитом',
       'statement': 'Python: s.replace(a, b, 1). Напишите replace_first(s: &str, a: &str, b: &str) -> String '
                    '— заменить только первое вхождение.',
       'starter': 'fn replace_first(s: &str, a: &str, b: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", replace_first("a-b-c", "-", "+"));\n'
                 '    println!("{}", replace_first("abc", "z", "y"));\n'
                 '    println!("{}", replace_first("раз раз раз", "раз", "два"));\n'
                 '}\n',
       'hint': 'replacen(a, b, n)',
       'expected': ['a+b-c', 'abc', 'два раз раз']},
      {'id': 'r11-split-comma',
       'mode': 'rust',
       'title': 'split',
       'statement': "Python: [p.strip() for p in s.split(',')]. Напишите split_trim(s: &str) -> Vec<String>.",
       'starter': 'fn split_trim(s: &str) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", split_trim("a, b ,c"));\n'
                 '    println!("{:?}", split_trim("один"));\n'
                 '    println!("{:?}", split_trim(""));\n'
                 '}\n',
       'hint': "split(',') → map(trim, to_string) → collect",
       'expected': ['["a", "b", "c"]', '["один"]', '[""]']},
      {'id': 'r11-split-once',
       'mode': 'rust',
       'title': 'Ключ и значение',
       'statement': "Python: k, v = line.split('=', 1). Напишите kv(line: &str) -> Option<(String, String)> "
                    'через split_once; ключ и значение без пробелов по краям.',
       'starter': 'fn kv(line: &str) -> Option<(String, String)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", kv("name = Аня"));\n'
                 '    println!("{:?}", kv("a=b=c"));\n'
                 '    println!("{:?}", kv("нет равно"));\n'
                 '}\n',
       'hint': 'split_once возвращает Option<(&str, &str)>.',
       'expected': ['Some(("name", "Аня"))', 'Some(("a", "b=c"))', 'None']},
      {'id': 'r11-words',
       'mode': 'rust',
       'title': 'Слова текста',
       'statement': 'Python: s.split(). Напишите words(s: &str) -> Vec<&str> через split_whitespace.',
       'starter': 'fn words(s: &str) -> Vec<&str> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", words("  раз   два\\tтри\\nчетыре "));\n'
                 '    println!("{:?}", words(""));\n'
                 '}\n',
       'hint': 'split_whitespace().collect()',
       'expected': ['["раз", "два", "три", "четыре"]', '[]']},
      {'id': 'r11-join',
       'mode': 'rust',
       'title': 'join',
       'statement': "Python: ', '.join(words). Напишите join_comma(words: &[&str]) -> String.",
       'starter': 'fn join_comma(words: &[&str]) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", join_comma(&["a", "b", "c"]));\n'
                 '    println!("[{}]", join_comma(&[]));\n'
                 '    println!("{}", join_comma(&["один"]));\n'
                 '}\n',
       'hint': 'words.join(", ")',
       'expected': ['a, b, c', '[]', 'один']},
      {'id': 'r11-fstring',
       'mode': 'rust',
       'title': 'f-строка',
       'statement': 'Python: f"{name}: {score:>5.1f}". Напишите line(name: &str, score: f64) -> String: имя, '
                    'двоеточие, пробел и очки с одним знаком после запятой, выровненные вправо в поле '
                    'шириной 5.',
       'starter': 'fn line(name: &str, score: f64) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("[{}]", line("Аня", 93.456));\n'
                 '    println!("[{}]", line("Боря", 7.0));\n'
                 '    println!("[{}]", line("Вера", 100.0));\n'
                 '}\n',
       'hint': '{:>5.1} — ширина 5, одна цифра после точки.',
       'expected': ['[Аня:  93.5]', '[Боря:   7.0]', '[Вера: 100.0]']},
      {'id': 'r11-title-case',
       'mode': 'rust',
       'title': 'title()',
       'statement': 'Python: s.title() для слов, разделённых пробелами. Напишите title(s: &str) -> String: '
                    'каждое слово с заглавной буквы, остальные строчные; слова через один пробел.',
       'starter': 'fn title(s: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", title("hello wORLD"));\n'
                 '    println!("{}", title("  привет   мир "));\n'
                 '    println!("[{}]", title(""));\n'
                 '}\n',
       'hint': 'Первую букву — в верхний регистр, остальное — в нижний.',
       'expected': ['Hello World', 'Привет Мир', '[]']},
      {'id': 'r11-startswith',
       'mode': 'rust',
       'title': 'startswith и endswith',
       'statement': "Python: s.startswith(('http://', 'https://')). Напишите is_url(s: &str) -> bool: строка "
                    'начинается с http:// или https://.',
       'starter': 'fn is_url(s: &str) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", is_url("http://a.ru"));\n'
                 '    println!("{}", is_url("https://a.ru/x"));\n'
                 '    println!("{}", is_url("ftp://a.ru"));\n'
                 '    println!("{}", is_url(""));\n'
                 '}\n',
       'hint': 'Две проверки starts_with через ||.',
       'expected': ['true', 'true', 'false', 'false']},
      {'id': 'r11-isdigit',
       'mode': 'rust',
       'title': 'isdigit',
       'statement': 'Python: s.isdigit(). Напишите all_digits(s: &str) -> bool: строка непуста и состоит '
                    'только из ASCII-цифр.',
       'starter': 'fn all_digits(s: &str) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", all_digits("12345"));\n'
                 '    println!("{}", all_digits("12a"));\n'
                 '    println!("{}", all_digits(""));\n'
                 '    println!("{}", all_digits("٣٤"));\n'
                 '}\n',
       'hint': 'chars().all(|c| c.is_ascii_digit()) и !s.is_empty()',
       'expected': ['true', 'false', 'false', 'false']},
      {'id': 'r11-ord-chr',
       'mode': 'rust',
       'title': 'ord и chr',
       'statement': 'Python: chr(ord(c) + 1). Напишите next_char(c: char) -> Option<char>: следующий по коду '
                    'символ (None, если кода нет).',
       'starter': 'fn next_char(c: char) -> Option<char> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", next_char(\'a\'));\n'
                 '    println!("{:?}", next_char(\'я\'));\n'
                 '    println!("{:?}", next_char(\'\\u{10FFFF}\'));\n'
                 '}\n',
       'hint': 'char::from_u32 возвращает None, если число — не символ.',
       'expected': ["Some('b')", "Some('ѐ')", 'None']},
      {'id': 'r11-caesar-ru',
       'mode': 'rust',
       'title': 'Шифр Цезаря для русского',
       'statement': 'Напишите caesar_ru(s: &str, k: u32) -> String: сдвиг строчных русских букв а–я (33 '
                    'буквы, включая ё) на k позиций вперёд по кругу; прочие символы не менять. Алфавит: '
                    '«абвгдеёжзийклмнопрстуфхцчшщъыьэюя».',
       'starter': 'fn caesar_ru(s: &str, k: u32) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", caesar_ru("привет, мир!", 3));\n'
                 '    println!("{}", caesar_ru("яя", 1));\n'
                 '    println!("{}", caesar_ru("abc", 5));\n'
                 '}\n',
       'hint': 'Найдите позицию буквы в векторе алфавита и сдвиньте по модулю его длины.',
       'expected': ['тулезх, плу!', 'аа', 'abc']},
      {'id': 'r11-reverse-words',
       'mode': 'rust',
       'title': 'Слова в обратном порядке',
       'statement': "Python: ' '.join(s.split()[::-1]). Напишите reverse_words(s: &str) -> String.",
       'starter': 'fn reverse_words(s: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", reverse_words("раз два три"));\n'
                 '    println!("{}", reverse_words("  один  "));\n'
                 '    println!("[{}]", reverse_words(""));\n'
                 '}\n',
       'hint': 'split_whitespace().rev() и join(" ")',
       'expected': ['три два раз', 'один', '[]']},
      {'id': 'r11-anagram',
       'mode': 'rust',
       'title': 'Анаграммы',
       'statement': 'Python: sorted(a) == sorted(b). Напишите is_anagram(a: &str, b: &str) -> bool без учёта '
                    'регистра и пробелов.',
       'starter': 'fn is_anagram(a: &str, b: &str) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", is_anagram("Лунь", "Нуль"));\n'
                 '    println!("{}", is_anagram("a b c", "cba"));\n'
                 '    println!("{}", is_anagram("abc", "abd"));\n'
                 '}\n',
       'hint': 'Нормализуйте обе строки: без пробелов, в нижнем регистре, отсортированные.',
       'expected': ['true', 'true', 'false']},
      {'id': 'r11-char-freq',
       'mode': 'rust',
       'title': 'Частоты символов',
       'statement': 'Python: Counter(s). Напишите top_char(s: &str) -> Option<(char, usize)>: самый частый '
                    'символ и его счёт; при равенстве — тот, что встретился раньше. Для пустой строки — '
                    'None. Используйте Vec пар (char, usize) без HashMap.',
       'starter': 'fn top_char(s: &str) -> Option<(char, usize)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", top_char("abracadabra"));\n'
                 '    println!("{:?}", top_char("ааб"));\n'
                 '    println!("{:?}", top_char("абв"));\n'
                 '    println!("{:?}", top_char(""));\n'
                 '}\n',
       'hint': 'Храните пары в векторе; обновляйте найденную или добавляйте новую.',
       'expected': ["Some(('a', 5))", "Some(('а', 2))", "Some(('а', 1))", 'None']},
      {'id': 'r11-wrap',
       'mode': 'rust',
       'title': 'Перенос строк',
       'statement': 'Напишите wrap(text: &str, width: usize) -> Vec<String>: разбейте слова по строкам так, '
                    'чтобы каждая строка (слова через пробел) была не длиннее width символов (слово длиннее '
                    'width — на отдельной строке).',
       'starter': 'fn wrap(text: &str, width: usize) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for l in wrap("раз два три четыре пять шесть семь", 10) {\n'
                 '        println!("[{}]", l);\n'
                 '    }\n'
                 '    println!("{}", wrap("", 5).len());\n'
                 '    println!("{:?}", wrap("длинноеслово ок", 5));\n'
                 '}\n',
       'hint': 'Копите текущую строку cur и отправляйте её в результат, когда слово не помещается.',
       'expected': ['[раз два]', '[три четыре]', '[пять шесть]', '[семь]', '0', '["длинноеслово", "ок"]']},
      {'id': 'r11-vowels',
       'mode': 'rust',
       'title': 'Гласные и согласные',
       'statement': 'Напишите count_vowels(s: &str) -> (usize, usize): число русских гласных «аеёиоуыэюя» и '
                    'число остальных букв (регистр не важен; не буквы не считаются).',
       'starter': 'fn count_vowels(s: &str) -> (usize, usize) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", count_vowels("Привет, Мир!"));\n'
                 '    println!("{:?}", count_vowels("123"));\n'
                 '    println!("{:?}", count_vowels("Ёжик"));\n'
                 '}\n',
       'hint': 'Сначала проверяйте принадлежность гласным, затем is_alphabetic.',
       'expected': ['(3, 6)', '(0, 0)', '(2, 2)']},
      {'id': 'r11-compress',
       'mode': 'rust',
       'title': 'Сжатие повторов',
       'statement': 'Напишите rle(s: &str) -> String: каждый ряд одинаковых символов заменяется на символ и '
                    'число повторов («aaabcc» → «a3b1c2»).',
       'starter': 'fn rle(s: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", rle("aaabcc"));\n'
                 '    println!("{}", rle("ббббб"));\n'
                 '    println!("[{}]", rle(""));\n'
                 '    println!("{}", rle("abc"));\n'
                 '}\n',
       'hint': 'peekable() позволяет подсмотреть следующий символ.',
       'expected': ['a3b1c2', 'б5', '[]', 'a1b1c1']},
      {'id': 'r11-unrle',
       'mode': 'rust',
       'title': 'Распаковка',
       'statement': 'Обратная задача: unrle(s: &str) -> String распаковывает вид «a3b1c2» (после каждой '
                    'буквы идут цифры её количества) в «aaabcc». Буквы — любые не-цифры.',
       'starter': 'fn unrle(s: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", unrle("a3b1c2"));\n'
                 '    println!("{}", unrle("б5"));\n'
                 '    println!("[{}]", unrle(""));\n'
                 '    println!("{}", unrle("x12"));\n'
                 '}\n',
       'hint': 'Накапливайте цифры в num и сбрасывайте при новой букве.',
       'expected': ['aaabcc', 'ббббб', '[]', 'xxxxxxxxxxxx']},
      {'id': 'r11-bytes-hex',
       'mode': 'rust',
       'title': 'encode → hex',
       'statement': 'Python: s.encode().hex(). Напишите to_hex(s: &str) -> String: байты UTF-8, каждый двумя '
                    'шестнадцатеричными цифрами без пробелов.',
       'starter': 'fn to_hex(s: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", to_hex("A"));\n'
                 '    println!("{}", to_hex("Ж"));\n'
                 '    println!("{}", to_hex("привет"));\n'
                 '    println!("[{}]", to_hex(""));\n'
                 '}\n',
       'hint': 'format!("{:02x}", b) для каждого байта.',
       'expected': ['41', 'd096', 'd0bfd180d0b8d0b2d0b5d182', '[]']},
      {'id': 'r11-from-bytes',
       'mode': 'rust',
       'title': 'decode с ошибкой',
       'statement': 'Python: b.decode() может бросить UnicodeDecodeError. Напишите decode(b: &[u8]) -> '
                    'Result<String, String>: Ok(строка) или Err("плохой UTF-8").',
       'starter': 'fn decode(b: &[u8]) -> Result<String, String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", decode(&[208, 159, 209, 128]));\n'
                 '    println!("{:?}", decode(&[0xff, 0xfe]));\n'
                 '    println!("{:?}", decode(&[]));\n'
                 '}\n',
       'hint': 'String::from_utf8(b.to_vec())',
       'expected': ['Ok("Пр")', 'Err("плохой UTF-8")', 'Ok("")']},
      {'id': 'r11-lossy',
       'mode': 'rust',
       'title': 'from_utf8_lossy',
       'statement': 'Напишите safe_text(b: &[u8]) -> String: превратите байты в строку, подменяя неверные '
                    'последовательности символом «�» (метод String::from_utf8_lossy и to_string).',
       'starter': 'fn safe_text(b: &[u8]) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", safe_text(&[104, 105]));\n'
                 '    println!("{}", safe_text(&[104, 0xff, 105]));\n'
                 '}\n',
       'hint': 'from_utf8_lossy возвращает Cow; to_string делает String.',
       'expected': ['hi', 'h�i']},
      {'id': 'r11-sort-ci',
       'mode': 'rust',
       'title': 'Сортировка без учёта регистра',
       'statement': 'Python: sorted(words, key=str.lower). Напишите sort_ci(words: &[&str]) -> Vec<String>: '
                    'слова по алфавиту без учёта регистра; при равенстве — исходный порядок (сортировка '
                    'устойчива).',
       'starter': 'fn sort_ci(words: &[&str]) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", sort_ci(&["banana", "Apple", "cherry", "apple", "Banana"]));\n'
                 '    println!("{:?}", sort_ci(&["я", "А", "б"]));\n'
                 '}\n',
       'hint': 'sort_by_key(|w| w.to_lowercase())',
       'expected': ['["Apple", "apple", "banana", "Banana", "cherry"]', '["А", "б", "я"]']},
      {'id': 'r11-build',
       'mode': 'rust',
       'title': 'Строим длинную строку',
       'statement': 'Напишите numbers(n: u32) -> String: числа 1…n через запятую без пробелов («1,2,3»). '
                    'Используйте String::with_capacity и push_str. Для n = 0 — пустая строка.',
       'starter': 'fn numbers(n: u32) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", numbers(5));\n'
                 '    println!("[{}]", numbers(0));\n'
                 '    let big = numbers(100000);\n'
                 '    println!("{} {}", big.len(), &big[big.len() - 12..]);\n'
                 '}\n',
       'hint': 'push_str в цикле и запятая перед каждым числом, кроме первого.',
       'expected': ['1,2,3,4,5', '[]', '588894 99999,100000']}]}
