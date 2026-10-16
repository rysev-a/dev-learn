"""Задачи книги «Изучаем Rust»: глава 6 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {6: [{'id': 'r6-literal',
      'mode': 'rust',
      'title': 'Литерал и длина',
      'statement': 'Объявите s = "Привет, мир!" и напечатайте две строки: саму строку, затем «bytes=…» и '
                   '«chars=…» в одной строке: «bytes=21 chars=12».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'Привет, мир!\n'
                   'bytes=21 chars=12',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'len() — байты, chars().count() — символы.',
      'standalone': True,
      'expected': ['Привет, мир!', 'bytes=21 chars=12']},
     {'id': 'r6-string-new',
      'mode': 'rust',
      'title': 'Строим String',
      'statement': 'Создайте пустую изменяемую String, допишите push_str("Rust"), push(\' \'), '
                   'push_str("любит"), push(\' \'), push_str("тебя") и напечатайте «Rust любит тебя».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'Rust любит тебя',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'push принимает символ в одинарных кавычках, push_str — строку.',
      'standalone': True,
      'expected': ['Rust любит тебя']},
     {'id': 'r6-concat-plus',
      'mode': 'rust',
      'title': 'Склейка плюсом',
      'statement': 'Склейте String a = «раз» и &str «два» оператором +, затем добавьте «три» и напечатайте '
                   '«раздватри». Левый операнд плюса — String.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'раздватри',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Слева String, справа &str.',
      'standalone': True,
      'expected': ['раздватри']},
     {'id': 'r6-format',
      'mode': 'rust',
      'title': 'format!',
      'statement': 'name = "Аня", age = 30. С помощью format! соберите в переменную строку «Аня, 30 лет» и '
                   'напечатайте её.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'Аня, 30 лет',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'format!("{}, {} лет", name, age)',
      'standalone': True,
      'expected': ['Аня, 30 лет']},
     {'id': 'r6-join',
      'mode': 'rust',
      'title': 'join',
      'statement': 'Склейте слова ["сыр", "хлеб", "молоко"] методом join с разделителем ", " и напечатайте '
                   '«сыр, хлеб, молоко».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'сыр, хлеб, молоко',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'words.join(", ")',
      'standalone': True,
      'expected': ['сыр, хлеб, молоко']},
     {'id': 'r6-repeat',
      'mode': 'rust',
      'title': 'Повторение',
      'statement': 'Напечатайте строку из 20 тире «--------------------» методом repeat, затем «Rust» и '
                   'снова 20 тире.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '--------------------\n'
                   'Rust\n'
                   '--------------------',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': '"-".repeat(20)',
      'standalone': True,
      'expected': ['--------------------', 'Rust', '--------------------']},
     {'id': 'r6-upper-lower',
      'mode': 'rust',
      'title': 'Регистр',
      'statement': 's = "Привет, Мир". Напечатайте s.to_uppercase() и s.to_lowercase() — две строки: '
                   '«ПРИВЕТ, МИР» и «привет, мир».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'ПРИВЕТ, МИР\n'
                   'привет, мир',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Методы возвращают новую строку.',
      'standalone': True,
      'expected': ['ПРИВЕТ, МИР', 'привет, мир']},
     {'id': 'r6-trim-replace',
      'mode': 'rust',
      'title': 'trim и replace',
      'statement': 's = "   много   пробелов   ". Напечатайте trim, а затем replace("много", "мало") у '
                   'обрезанной строки: «много   пробелов» и «мало   пробелов».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'много   пробелов\n'
                   'мало   пробелов',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'trim убирает пробелы только по краям.',
      'standalone': True,
      'expected': ['много   пробелов', 'мало   пробелов']},
     {'id': 'r6-contains',
      'mode': 'rust',
      'title': 'Поиск подстроки',
      'statement': 'text = "Rust — язык системного программирования". Напечатайте три строки: '
                   'contains("язык"), starts_with("Rust"), ends_with("Go") → true, true, false.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'true\n'
                   'true\n'
                   'false',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Результат каждого метода — bool.',
      'standalone': True,
      'expected': ['true', 'true', 'false']},
     {'id': 'r6-find',
      'mode': 'rust',
      'title': 'find',
      'statement': 'text = "hello world". Напечатайте позицию первого вхождения «o» (find, это Option, '
                   'поэтому добавьте unwrap) и позицию «wor»: «4» и «6».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '4\n'
                   '6',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'find возвращает Option<usize>; unwrap достаёт значение.',
      'standalone': True,
      'expected': ['4', '6']},
     {'id': 'r6-chars-loop',
      'mode': 'rust',
      'title': 'Перебор символов',
      'statement': 'Для строки "раст" напечатайте каждый символ на отдельной строке циклом for по chars().\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'р\n'
                   'а\n'
                   'с\n'
                   'т',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'for c in "раст".chars() { … }',
      'standalone': True,
      'expected': ['р', 'а', 'с', 'т']},
     {'id': 'r6-count-vowels',
      'mode': 'rust',
      'title': 'Гласные',
      'statement': 'В строке "Программирование на Rust" посчитайте русские гласные «аеёиоуыэюя» (регистр не '
                   'важен: сначала в нижний). Напечатайте «8».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '8',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': '"…".contains(c) умеет искать символ.',
      'standalone': True,
      'expected': ['8']},
     {'id': 'r6-reverse',
      'mode': 'rust',
      'title': 'Развернуть строку',
      'statement': 'Разверните строку "привет" методами chars().rev().collect::<String>() и напечатайте '
                   '«тевирп».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'тевирп',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'chars().rev() и collect в String.',
      'standalone': True,
      'expected': ['тевирп']},
     {'id': 'r6-palindrome',
      'mode': 'rust',
      'title': 'Палиндром',
      'statement': 'Проверьте, является ли «А роза упала на лапу Азора» палиндромом, игнорируя пробелы и '
                   'регистр. Напечатайте «true».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'true',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Уберите пробелы, приведите к нижнему регистру, сравните с перевёрнутой.',
      'standalone': True,
      'expected': ['true']},
     {'id': 'r6-words-count',
      'mode': 'rust',
      'title': 'Количество слов',
      'statement': 'Посчитайте слова в строке "  раз  два   три четыре " методом split_whitespace().count(): '
                   '«4».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '4',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'split_whitespace игнорирует лишние пробелы.',
      'standalone': True,
      'expected': ['4']},
     {'id': 'r6-split-parse-sum',
      'mode': 'rust',
      'title': 'Сумма чисел из строки',
      'statement': 'Из строки "10, 20, 30, 5" извлеките числа (split по запятой, trim, parse::<i32>) и '
                   'напечатайте сумму «65».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '65',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'part.trim().parse::<i32>().unwrap()',
      'standalone': True,
      'expected': ['65']},
     {'id': 'r6-lines',
      'mode': 'rust',
      'title': 'Строки текста',
      'statement': 'text = "раз\\nдва\\nтри". Напечатайте каждую строку с номером в формате «1: раз», «2: '
                   'два», «3: три» (lines и enumerate).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '1: раз\n'
                   '2: два\n'
                   '3: три',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'enumerate даёт пары (номер, значение); номер с нуля.',
      'standalone': True,
      'expected': ['1: раз', '2: два', '3: три']},
     {'id': 'r6-slice',
      'mode': 'rust',
      'title': 'Срез строки',
      'statement': 'text = "Hello, Rust!". Напечатайте срезы: &text[0..5], &text[7..11] и &text[7..] — '
                   '«Hello», «Rust» и «Rust!».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'Hello\n'
                   'Rust\n'
                   'Rust!',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Для ASCII-строки байты совпадают с символами.',
      'standalone': True,
      'expected': ['Hello', 'Rust', 'Rust!']},
     {'id': 'r6-nth-char',
      'mode': 'rust',
      'title': 'n-й символ',
      'statement': 's = "привет". Напечатайте третий символ (индекс 2, через chars().nth(2)) и последний '
                   '(chars().last()). Ожидается «и» и «т». Оба — Option, воспользуйтесь unwrap.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'и\n'
                   'т',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'nth(n) возвращает Option<char>.',
      'standalone': True,
      'expected': ['и', 'т']},
     {'id': 'r6-char-indices',
      'mode': 'rust',
      'title': 'Позиции символов',
      'statement': 'Для строки "аб" напечатайте пары «позиция символ» методом char_indices: «0 а» и «2 б» '
                   '(русская буква — 2 байта).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '0 а\n'
                   '2 б',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'char_indices выдаёт смещение в байтах.',
      'standalone': True,
      'expected': ['0 а', '2 б']},
     {'id': 'r6-format-width',
      'mode': 'rust',
      'title': 'Выравнивание',
      'statement': 'Напечатайте три строки: число 42 в поле шириной 8 с выравниванием вправо («[      42]»), '
                   'слово «Rust» влево в поле 8 («[Rust    ]») и «hi» по центру в поле 8 с заполнителем «*» '
                   '(«[***hi***]»).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '[      42]\n'
                   '[Rust    ]\n'
                   '[***hi***]',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': '{:>8}, {:<8}, {:*^8}',
      'standalone': True,
      'expected': ['[      42]', '[Rust    ]', '[***hi***]']},
     {'id': 'r6-format-float',
      'mode': 'rust',
      'title': 'Точность дробного',
      'statement': 'x = 3.14159265. Напечатайте x с 0, 2 и 4 знаками после запятой — «3», «3.14», «3.1416» '
                   '(по строке).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '3\n'
                   '3.14\n'
                   '3.1416',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': '{:.0}, {:.2}, {:.4}',
      'standalone': True,
      'expected': ['3', '3.14', '3.1416']},
     {'id': 'r6-format-zero-pad',
      'mode': 'rust',
      'title': 'Нули слева',
      'statement': 'Напечатайте число 7 как «007» (поле ширины 3, нули слева: {:03}), а 255 в '
                   'шестнадцатеричной записи с нулями в поле 4 и префиксом 0x: «0x00ff» (формат {:#06x}).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '007\n'
                   '0x00ff',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': '{:03} и {:#06x}',
      'standalone': True,
      'expected': ['007', '0x00ff']},
     {'id': 'r6-debug-format',
      'mode': 'rust',
      'title': 'Отладочный формат',
      'statement': 'Напечатайте строку "привет\\n" через {:?} (в кавычках и с экранированием: «"привет\\n"») '
                   'и кортеж (1, "a", 2.5) через {:?}: «(1, "a", 2.5)».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '"привет\\n"\n'
                   '(1, "a", 2.5)',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': '{:?} — отладочное представление.',
      'standalone': True,
      'expected': ['"привет\\n"', '(1, "a", 2.5)']},
     {'id': 'r6-compare',
      'mode': 'rust',
      'title': 'Сравнение строк',
      'statement': 'Напечатайте: «apple» < «banana» (true), «Zebra» < «apple» (true, заглавные раньше) и '
                   'String::from("abc") == "abc" (true).\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'true\n'
                   'true\n'
                   'true',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Строки сравниваются по байтам.',
      'standalone': True,
      'expected': ['true', 'true', 'true']},
     {'id': 'r6-fn-shout',
      'mode': 'rust',
      'title': 'Крик',
      'statement': 'Напишите функцию shout(s: &str) -> String: строка в верхнем регистре с тремя '
                   'восклицательными знаками в конце.',
      'starter': 'fn shout(s: &str) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n    println!("{}", shout("привет"));\n    println!("{}", shout("Rust"));\n}\n',
      'hint': 'format!("{}!!!", s.to_uppercase())',
      'expected': ['ПРИВЕТ!!!', 'RUST!!!']},
     {'id': 'r6-fn-count-char',
      'mode': 'rust',
      'title': 'Сколько раз встречается',
      'statement': 'Напишите функцию count_char(s: &str, ch: char) -> usize: сколько раз символ ch '
                   'встречается в s.',
      'starter': 'fn count_char(s: &str, ch: char) -> usize {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", count_char("абракадабра", \'а\'));\n'
                '    println!("{}", count_char("hello", \'z\'));\n'
                '    println!("{}", count_char("", \'a\'));\n'
                '}\n',
      'hint': 'Цикл по chars и счётчик.',
      'expected': ['5', '0', '0']},
     {'id': 'r6-fn-first-word',
      'mode': 'rust',
      'title': 'Первое слово',
      'statement': 'Напишите функцию first_word(s: &str) -> &str: первое слово строки (до первого пробела; '
                   'если пробелов нет — вся строка).',
      'starter': 'fn first_word(s: &str) -> &str {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", first_word("hello world"));\n'
                '    println!("{}", first_word("один"));\n'
                '    println!("{}", first_word("привет мир"));\n'
                '}\n',
      'hint': "find(' ') возвращает позицию пробела; срез &s[..i].",
      'expected': ['hello', 'один', 'привет']},
     {'id': 'r6-fn-capitalize',
      'mode': 'rust',
      'title': 'Заглавная первая буква',
      'statement': 'Напишите функцию capitalize(s: &str) -> String: первая буква заглавная, остальные без '
                   'изменений (пустая строка — пустая).',
      'starter': 'fn capitalize(s: &str) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", capitalize("привет"));\n'
                '    println!("{}", capitalize("rust"));\n'
                '    println!("[{}]", capitalize(""));\n'
                '}\n',
      'hint': 'chars().next() даёт первую букву, остаток — chars.as_str().',
      'expected': ['Привет', 'Rust', '[]']},
     {'id': 'r6-fn-caesar',
      'mode': 'rust',
      'title': 'Шифр Цезаря',
      'statement': 'Напишите функцию caesar(s: &str, shift: u8) -> String для латиницы a–z: каждую строчную '
                   'букву сдвиньте на shift вперёд по кругу (z → a), остальные символы не меняйте.',
      'starter': 'fn caesar(s: &str, shift: u8) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", caesar("hello, world", 3));\n'
                '    println!("{}", caesar("xyz", 3));\n'
                '    println!("{}", caesar("abc", 0));\n'
                '}\n',
      'hint': "Номер буквы: c as u8 - b'a'; сдвиг по модулю 26; обратно + b'a'.",
      'expected': ['khoor, zruog', 'abc', 'abc']}]}
