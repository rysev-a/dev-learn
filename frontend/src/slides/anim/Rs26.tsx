import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, rs, slot } from "./rs.tsx";

/* Глава 26 книги «Изучаем Rust»: текст и форматирование. */

const pair = (a: string, b: string, ca = "m", cb = "g", y = 60) => [
  Box("pa", 90, y, 130, 34, a, ca, { size: 10 }),
  Box("pb", 270, y, 130, 34, b, cb, { size: 10 }),
];
const row = (pre: string, items: (string|number)[], c = "g", y = 66, size = 10.5) =>
  items.map((t: string|number, i: number) =>
    Box(`${pre}${i}`, 50 + i * 86, y, 76, 30, t, c, { size }),
  );

// 1. Введение
export const V01 = scene({
  labels: ["Инструментарий", "Что разберём", "Без пакетов"],
  caption: [
    "Методы char и str, шаблоны, форматирование, Display и Debug, разбор",
    "Парсеры конфигов, логи, консольные утилиты, форматтеры",
    "Стандартная библиотека делает много даже без внешних пакетов",
  ],
  frames: [
    [...row("a", ["char", "str", "fmt", "parse"], "b")],
    [...row("a", ["логи", "конфиги", "CLI", "таблицы"], "g", 66, 9.5)],
    [Box("a", 180, 60, 230, 34, "std — часто достаточно", "y", { size: 12 })],
  ],
});

// 2. char
export const V02 = scene({
  labels: ["Категории", "Цифры", "Кодировка"],
  caption: [
    "is_alphabetic, is_numeric, is_whitespace, is_uppercase — правила Unicode; is_ascii_* быстрее",
    "to_digit(radix) → Option<u32>, char::from_digit(d, radix) — в обе стороны",
    "len_utf8, encode_utf8, escape_debug, escape_default — размер и экранирование",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "c.is_alphabetic()   c.is_whitespace()",
          "c.is_ascii_digit()   c.is_uppercase()",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "'f'.to_digit(16)             // Some(15)",
          "char::from_digit(15, 16)      // Some('f')",
        ],
        undefined,
        { w: 340, size: 10, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["'я'.len_utf8()      // 2", "'\\n'.escape_debug()   // \\n"],
        undefined,
        { w: 340, size: 11, lh: 26 },
      ),
    ],
  ],
});

// 3. Разбиение
export const V03 = scene({
  labels: [
    "splitn, rsplit",
    "terminator, inclusive",
    "split_once, strip_prefix",
  ],
  caption: [
    "split, splitn(n), rsplit, rsplitn(n) — по разделителю, с лимитом, с конца",
    "split_terminator — без пустого хвоста; split_inclusive — разделитель остаётся в конце куска",
    "split_once → пара; strip_prefix, strip_suffix → Option; matches, match_indices, find, rfind",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          '"a,b,c".splitn(2, \',\')   // "a", "b,c"',
          "\"a,b,c\".rsplit(',')       // c b a",
        ],
        undefined,
        { w: 340, size: 9.5, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "\"a\\nb\\n\".split_terminator('\\n')   // a b",
          '"a\\nb".split_inclusive(\'\\n\')      // "a\\n", "b"',
        ],
        undefined,
        { w: 340, size: 8, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          '"get /x".strip_prefix("get ")   // Some("/x")',
          "\"k=v\".split_once('=')",
        ],
        undefined,
        { w: 340, size: 9, lh: 26 },
      ),
    ],
  ],
});

// 4. Шаблоны
export const V04 = scene({
  labels: ["Pattern", "Замыкание", "trim_matches"],
  caption: [
    "Шаблон — char, &str, [char; N], &[char] или замыкание, возвращающее bool",
    "s.split(|c: char| c == ',' || c.is_whitespace()) — по любому из условий",
    "trim_matches, trim_start_matches, trim_end_matches убирают символы по шаблону",
  ],
  frames: [
    [...row("a", ["char", "&str", "[char]", "|c| …"], "b", 66, 10)],
    [
      rs("c", 20, 50, ["s.split(|c: char| c == ',' || c == ';')"], [0], {
        w: 340,
        size: 10,
        lh: 28,
      }),
    ],
    [
      rs("c", 20, 50, ['",,a,b,,".trim_matches(\',\')   // "a,b"'], [0], {
        w: 340,
        size: 11,
        lh: 28,
      }),
    ],
  ],
});

// 5. Изменение String
export const V05 = scene({
  labels: ["insert, remove", "truncate, retain", "replace_range, drain"],
  caption: [
    "insert(i, c), insert_str(i, s), remove(i) → char, pop() → Option<char>",
    "truncate(n), clear(), retain(|c| …) — укоротить, очистить, оставить нужное",
    'replace_range(a..b, "…"), drain(a..b); позиции — байтовые и на границах символов (is_char_boundary)',
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["s.insert(0, '>');", 's.insert_str(1, " ");', "let c = s.remove(0);"],
        undefined,
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["s.truncate(5);", "s.retain(|c| c != ' ');"],
        undefined,
        { w: 340, size: 11.5, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ['s.replace_range(0..3, "abc");', "s.is_char_boundary(i)"],
        undefined,
        { w: 340, size: 11, lh: 28 },
      ),
    ],
  ],
});

// 6. Язык формата
export const V06 = scene({
  labels: ["Грамматика", "Ширина из аргумента", "Типы"],
  caption: [
    "{:[заполнитель][выравнивание][знак][#][0][ширина][.точность][тип]}",
    "{:>w$} — ширина из именованной переменной; {:.*} — точность из предыдущего аргумента",
    "пусто — Display, ? — Debug, x X — hex, b — двоичная, o — восьмеричная, e — научная; # — префикс и pretty",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ["{:*^+#010.3x}", "// fill align sign alt zero width .prec type"],
        [0],
        { w: 340, size: 11, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          'println!("{:>w$}", x, w = 8);',
          'println!("{:.*}", 2, 3.14159);   // 3.14',
        ],
        undefined,
        { w: 340, size: 9.5, lh: 26 },
      ),
    ],
    [...row("a", ["{}", "{:?}", "{:x}", "{:b}"], "b", 66, 12)],
  ],
});

// 7. Display
export const V07 = scene({
  labels: ["write!", "pad", "Debug-помощники"],
  caption: [
    "fmt(&self, f: &mut Formatter) -> fmt::Result — частей записывают write!(f, …)",
    'f.pad("текст") уважает ширину и выравнивание; f.width(), f.precision(), f.alternate() — параметры',
    "debug_struct, debug_list, debug_map, debug_tuple дают единый вывод и работают с {:#?}",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {",
          '    write!(f, "({}, {})", self.x, self.y)',
          "}",
        ],
        [1],
        { w: 340, size: 8.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          'f.pad("text")      // ширина, выравнивание',
          "f.alternate()      // флаг #",
        ],
        undefined,
        { w: 340, size: 11, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ['f.debug_struct("P")', '    .field("x", &self.x)', "    .finish()"],
        undefined,
        { w: 340, size: 11, lh: 24 },
      ),
    ],
  ],
});

// 8. Разбор
export const V08 = scene({
  labels: ["ParseIntError", "from_str_radix", "Дробные и bool"],
  caption: [
    "Знак допустим, пробелы и «_» — нет; ошибка ParseIntError: kind() — Empty, InvalidDigit, PosOverflow…",
    'i32::from_str_radix("ff", 16); префиксы 0x и 0b нужно убрать вручную',
    'f64: точка, экспонента, inf, nan; bool: только "true" и "false"; char — строка из одного символа',
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          '"12".parse::<i32>()    // Ok(12)',
          '"".parse::<i32>()      // Err(Empty)',
          '"1_0".parse::<i32>()   // Err(InvalidDigit)',
        ],
        undefined,
        { w: 340, size: 9.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          'i32::from_str_radix("ff", 16)   // Ok(255)',
          'i32::from_str_radix("101", 2)  // Ok(5)',
        ],
        undefined,
        { w: 340, size: 9.5, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          '"1e3".parse::<f64>()    // 1000',
          '"true".parse::<bool>()',
          '"x".parse::<char>()',
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
  ],
});

// 9. Регистр
export const V09 = scene({
  labels: ["Unicode-правила", "ASCII-варианты", "Сравнение"],
  caption: [
    "to_uppercase и to_lowercase возвращают новую строку по правилам Unicode: «ß» → «SS»",
    "to_ascii_uppercase, make_ascii_uppercase (на месте), eq_ignore_ascii_case — быстро и только для латиницы",
    "Порядок строк — по байтам; правильная сортировка по-русски — внешние локали",
  ],
  frames: [
    [...pair('"ß".to_uppercase()', '"SS"', "b", "g")],
    [
      rs(
        "c",
        20,
        50,
        ["s.make_ascii_uppercase();", "a.eq_ignore_ascii_case(b)"],
        undefined,
        { w: 340, size: 11.5, lh: 28 },
      ),
    ],
    [...pair("байты ≠ алфавит", "локали — crate", "m", "y")],
  ],
});

// 10. Приёмы
export const V10 = scene({
  labels: ["Строки и токены", "Ключ = значение", "Таблица"],
  caption: [
    "lines() — без символа конца строки; split_whitespace(); посимвольный разбор с peekable()",
    "split_once('=') → trim → parse; числа через запятую: split → map(parse) → collect::<Result<_, _>>()",
    "Выравнивание таблиц: width = самое длинное слово; {:<width$}; ширина экрана иероглифов — unicode-width",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["for line in text.lines() { }", "let mut it = s.chars().peekable();"],
        undefined,
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let (k, v) = line.split_once('=')?;",
          "let n: i32 = v.trim().parse()?;",
        ],
        undefined,
        { w: 340, size: 10, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "let w = names.iter().map(|n| n.len()).max().unwrap();",
          'println!("{:<w$} {}", name, score, w = w);',
        ],
        undefined,
        { w: 340, size: 8.5, lh: 28 },
      ),
    ],
  ],
});

// 11. За пределами std
export const V11 = scene({
  labels: ["regex, unicode-*", "serde, nom", "Консоль"],
  caption: [
    "regex — линейное время без отката; unicode-segmentation, unicode-normalization, encoding_rs",
    "serde — JSON, TOML, CSV; nom и pest — собственные грамматики",
    "comfy-table, colored — таблицы и цвета в терминале; подключайте, когда std не хватает",
  ],
  frames: [
    [...row("a", ["regex", "unicode-", "encoding_rs"], "b", 66, 9)],
    [...pair("serde", "nom · pest", "g", "g")],
    [...pair("comfy-table", "colored", "b", "b")],
  ],
});

// 12. Литералы
export const V12 = scene({
  labels: ["Экранирование", "Сырые и байтовые", "Макросы компиляции"],
  caption: [
    '"\\n\\t\\\\\\"\\u{1F600}" — экранирование; окончание строки с \\ продолжает литерал',
    'r#"…"# ничего не экранирует; b"…" — срез байтов &[u8] для протоколов',
    "concat!, stringify!, include_str!, env!, file!, line!, module_path! — на этапе сборки",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ['"строка\\tс табом\\nи переносом"', '"\\u{1F600}"'],
        undefined,
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ['r#"он сказал "да""#', 'b"GET /"   // &[u8; 5]'],
        undefined,
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ['include_str!("data.txt")', 'concat!("a", 1, true)'],
        undefined,
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Шпаргалка", "Дальше"],
  caption: [
    "char — категории и цифры; str — split-семейство и шаблоны; String — insert, retain, replace_range",
    "Единый язык формата; свои Display и Debug; FromStr и kind() для ошибок разбора",
    "Следующая глава — ввод-вывод: Read, Write, BufRead, файлы и пути",
  ],
  frames: [
    [...row("a", ["char", "str", "fmt", "parse"], "g")],
    [
      rs(
        "c",
        20,
        40,
        ["let (k, v) = line.split_once('=')?;", 'println!("{:>8.2}", x);'],
        undefined,
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
    [
      Box("a", 180, 60, 250, 34, "Read · Write · BufRead · Path · fs", "b", {
        size: 10.5,
      }),
    ],
  ],
});
