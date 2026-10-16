import { scene } from "./alg.jsx";
import { Tx } from "./hw.jsx";
import { Box, arrow, rs, slot } from "./rs.jsx";

/* Глава 11 книги «Изучаем Rust»: строки — str из Python и String из Rust. */

const pair = (a, b, ca = "m", cb = "g", y = 60) => [
  Box("pa", 90, y, 130, 34, a, ca, { size: 10 }),
  Box("pb", 270, y, 130, 34, b, cb, { size: 10 }),
];

// 1. Введение
export const V01 = scene({
  labels: ["Таблица соответствий", "Что разберём", "Цель"],
  caption: [
    "Каждой привычной строковой операции Python — её запись в Rust",
    "Индексы, методы, split и join, форматирование, символы, юникод, байты",
    "После главы любой текстовый скрипт переписывается на Rust",
  ],
  frames: [
    [...pair("str", "&str / String", "m", "g")],
    [
      ...["индексы", "методы", "split", "формат", "юникод", "байты"].map(
        (t, i) => Box(`a${i}`, 36 + i * 58, 66, 52, 28, t, "b", { size: 8 }),
      ),
    ],
    [Box("a", 180, 60, 230, 34, "script.py  →  main.rs", "g", { size: 12 })],
  ],
});

// 2. Два типа
export const V02 = scene({
  labels: ["&str читает", "String владеет", "Преобразования"],
  caption: [
    "&str — чужой текст: параметры функций и срезы",
    "String — собственный текст: поля структур и возвращаемые значения",
    "&s → &str; to_string(), String::from(…), into() → String",
  ],
  frames: [
    [Box("a", 180, 60, 220, 40, "fn f(s: &str)", "b", { size: 12 })],
    [Box("a", 180, 60, 220, 40, "struct { name: String }", "g", { size: 11 })],
    [
      Box("a", 90, 60, 130, 34, "String → &str\n&s", "b", { size: 10 }),
      Box("b", 270, 60, 130, 34, "&str → String\nto_string()", "g", {
        size: 10,
      }),
    ],
  ],
});

// 3. Длина и индексы
export const V03 = scene({
  labels: ["len", "s[0] и s[-1]", "Срезы"],
  caption: [
    "Python: len(s) — символы; Rust: len() — байты; символы — chars().count()",
    "s[0] ✕; первая — s.chars().next(), последняя — s.chars().last()",
    "Срез &s[a..b] по границам символов; в середине символа — паника",
  ],
  frames: [
    [...pair('len("привет")\n= 6', '"привет".len()\n= 12', "m", "g")],
    [
      rs(
        "c",
        20,
        40,
        [
          "s[0]            # Python",
          "s.chars().next()   // Option<char>",
          "s.chars().last()   // Option<char>",
        ],
        [1, 2],
        { w: 340, size: 10, lh: 24 },
      ),
    ],
    [
      rs("c", 20, 40, ['&s[0..4]   // "пр"', "&s[0..3]   // panic"], [1], {
        w: 340,
        size: 12,
        lh: 26,
        bad: [1],
      }),
    ],
  ],
});

// 4. Методы
export const V04 = scene({
  labels: ["strip → trim", "lower, startswith", "find → Option"],
  caption: [
    "strip → trim; lstrip → trim_start; rstrip → trim_end",
    "lower, upper → to_lowercase, to_uppercase; startswith, endswith → starts_with, ends_with; in → contains",
    "Python find возвращает -1; Rust find — Option<usize>: Some(позиция) или None",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["s.strip()      →   s.trim()", "s.lstrip()     →   s.trim_start()"],
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
          "s.lower()       →   s.to_lowercase()",
          "s.startswith(p) →   s.starts_with(p)",
          "p in s          →   s.contains(p)",
        ],
        undefined,
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
    [...pair("find → -1", "find → None", "r", "g")],
  ],
});

// 5. split и join
export const V05 = scene({
  labels: ["split", "split_once, lines", "join"],
  caption: [
    "split → split: итератор, собирается в вектор collect(); split() без аргументов → split_whitespace()",
    'splitlines → lines; rsplit; split_once("=") — по первому вхождению, возвращает Option',
    "sep.join(list) → слайс.join(sep)",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["s.split(\",\")    →   s.split(',').collect::<Vec<_>>()"],
        undefined,
        { w: 340, size: 8.5, lh: 26 },
      ),
      rs("d", 20, 90, ["s.split()      →   s.split_whitespace()"], undefined, {
        w: 340,
        size: 9,
        lh: 26,
      }),
    ],
    [
      rs(
        "c",
        20,
        40,
        ['"k=v".split_once(\'=\')   // Some(("k", "v"))', "text.lines()"],
        [0],
        { w: 340, size: 9.5, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ['", ".join(words)   # Python', 'words.join(", ")   // Rust'],
        [1],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
  ],
});

// 6. Форматирование
export const V06 = scene({
  labels: ["f-строка → format!", "Спецификаторы", "Проверка при сборке"],
  caption: [
    'f"{x}" → format!("{x}"); format и print работают одинаково',
    "{:>8}, {:<8}, {:^8}, {:.2}, {:08.3}, {:?} — как в Python, почти один в один",
    "Python проверяет f-строку при запуске, Rust — при компиляции: опечатка в имени не соберётся",
  ],
  frames: [
    [...pair('f"{x}"', 'format!("{x}")', "m", "g")],
    [
      rs(
        "c",
        20,
        40,
        ["{:>8}   {:<8}   {:^8}", "{:.2}   {:08.3}   {:?}"],
        undefined,
        { w: 340, size: 12, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ['format!("{nme}")   // ✕ cannot find', "// value `nme` in this scope"],
        [0],
        { w: 340, size: 11, lh: 26, bad: [0] },
      ),
    ],
  ],
});

// 7. Построение
export const V07 = scene({
  labels: ["join в Python", "push_str", "with_capacity"],
  caption: [
    "Python: s += x в цикле дорого; собирают список и делают join",
    "Rust: String растёт амортизированно за константное время — push_str в цикле быстр",
    "String::with_capacity(n) — память выделяется один раз; retain, clear, insert_str меняют на месте",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["parts = []", "for x in data: parts.append(x)", 's = "".join(parts)'],
        [2],
        { w: 340, size: 10.5, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["let mut s = String::new();", "for x in &data { s.push_str(x); }"],
        [1],
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["let mut s = String::with_capacity(100);", "s.retain(|c| c != ' ');"],
        [0, 1],
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
  ],
});

// 8. Сравнение и сортировка
export const V08 = scene({
  labels: ["Сравнение", "sort", "Без учёта регистра"],
  caption: [
    "== по значению, порядок по байтам UTF-8; заглавные идут раньше строчных",
    "words.sort() — на месте; русские буквы после латинских",
    "sort_by_key(|w| w.to_lowercase()); локализованной сортировки в std нет",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ['"Z" < "a"    // true', '"a" < "я"    // true'],
        undefined,
        { w: 340, size: 12, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ['let mut w = vec!["b", "A", "я"];', 'w.sort();   // ["A", "b", "я"]'],
        [1],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
    [
      rs("c", 20, 40, ["w.sort_by_key(|s| s.to_lowercase());"], [0], {
        w: 340,
        size: 10.5,
        lh: 26,
      }),
    ],
  ],
});

// 9. Символы
export const V09 = scene({
  labels: ["ord и chr", "Проверки", "Регистр и ß"],
  caption: [
    "ord(c) → c as u32; chr(n) → char::from_u32(n) — Option, не каждое число символ",
    "is_alphabetic, is_numeric, is_whitespace, is_uppercase, is_ascii_digit; to_digit(10)",
    "to_uppercase() у char возвращает итератор: «ß» в верхнем регистре — «SS»",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "'я' as u32               // 1103",
          "char::from_u32(1103)      // Some('я')",
        ],
        [0, 1],
        { w: 340, size: 10, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        [
          "c.is_alphabetic()   c.is_numeric()",
          "c.is_whitespace()   c.is_uppercase()",
          "'7'.to_digit(10)    // Some(7)",
        ],
        undefined,
        { w: 340, size: 10, lh: 22 },
      ),
    ],
    [...pair("'ß'.to_uppercase()", '→ "SS"', "b", "y")],
  ],
});

// 10. Юникод
export const V10 = scene({
  labels: ["Кодовые точки", "Графемы", "Нормализация"],
  caption: [
    "chars() и len() Python считают кодовые точки: é — один символ или два (e + ´)",
    "Что видит человек — графемный кластер; в std его нет, нужен пакет unicode-segmentation",
    "Нормализация NFC и NFD — пакет unicode-normalization (в Python — unicodedata)",
  ],
  frames: [
    [...pair("é — 1 точка", "e + ´ — 2 точки", "b", "y")],
    [
      Box("a", 180, 56, 260, 40, "👨‍👩‍👧  — 5 кодовых точек, 1 графема", "g", {
        size: 10,
      }),
    ],
    [...pair("unicodedata\n.normalize", "unicode-\nnormalization", "m", "g")],
  ],
});

// 11. Байты
export const V11 = scene({
  labels: ["encode / as_bytes", "decode / from_utf8", "lossy и кодировки"],
  caption: [
    "s.encode() → s.as_bytes() (срез без копирования) или to_vec() (копия)",
    "b.decode() → String::from_utf8(b): Result — байты могут быть не UTF-8",
    "from_utf8_lossy подменяет неверные байты символом �; cp1251 и koi8-r — пакет encoding_rs",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["s.encode()      # Python", "s.as_bytes()    // &[u8]"],
        [1],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["String::from_utf8(bytes)", "// Ok(String) или Err(…)"],
        [0],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["String::from_utf8_lossy(&bytes)", "// подменит неверные байты на �"],
        [0],
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
  ],
});

// 12. Безопасность
export const V12 = scene({
  labels: ["Всегда UTF-8", "Граница", "OsString и Path"],
  caption: [
    "Любая строка Rust — корректный UTF-8: так гарантирует тип",
    "Ошибки декодирования возможны только на границе: чтение файла, сети, байтов",
    "Имена файлов и пути не обязаны быть юникодом: OsString и Path, перед выводом — явное преобразование",
  ],
  frames: [
    [Box("a", 180, 60, 240, 40, "String ⇒ валидный UTF-8", "g", { size: 12 })],
    [
      Box("a", 90, 60, 130, 34, "байты\nснаружи", "m", { size: 10.5 }),
      arrow("e", 156, 60, 204, 60, "g"),
      Box("b", 270, 60, 130, 34, "from_utf8\nResult", "y", { size: 10.5 }),
    ],
    [...pair("OsString", "Path", "b", "b")],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Шпаргалка", "Дальше"],
  caption: [
    "len в байтах; индексации нет; find → Option; split → итератор; format! проверяется при сборке",
    "push_str и with_capacity вместо join; юникод — кодовые точки; граница UTF-8 — Result",
    "Следующая глава — списки Python, массивы и векторы Rust",
  ],
  frames: [
    [
      ...["len", "find", "split", "format!"].map((t, i) =>
        Box(`a${i}`, 50 + i * 86, 66, 76, 30, t, "g", { size: 10.5 }),
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let words: Vec<&str> = s.split_whitespace().collect();",
          'let t = words.join(" ");',
        ],
        undefined,
        { w: 340, size: 8.5, lh: 26 },
      ),
    ],
    [Box("a", 180, 60, 240, 34, "list ↔ [T; N] / Vec<T>", "b", { size: 11.5 })],
  ],
});
