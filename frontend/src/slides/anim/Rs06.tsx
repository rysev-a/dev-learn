import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, rs } from "./rs.tsx";

/* Глава 6 книги «Изучаем Rust»: строки — &str и String. */

// 1. Две строки
export const V01 = scene({
  labels: ["Две строки", "&str", "String"],
  caption: [
    "В Python строка одна и неизменяемая; в Rust два типа: &str и String",
    "&str — ссылка на текст: читаем, но не владеем",
    "String — строка во владении программы: можно растить и менять",
  ],
  frames: [
    [
      Box("a", 90, 60, 130, 34, "Python: str", "m", { size: 11 }),
      Box("b", 270, 60, 130, 34, "Rust: &str, String", "g", { size: 10.5 }),
    ],
    [Box("a", 180, 60, 200, 40, "&str — смотреть", "b", { size: 12 })],
    [Box("a", 180, 60, 200, 40, "String — владеть", "g", { size: 12 })],
  ],
});

// 2. Литералы
export const V02 = scene({
  labels: ["Литерал", "Сырые строки", "Многострочные"],
  caption: [
    '"текст" имеет тип &\'static str: он лежит в самой программе и не меняется',
    'r"C:\\dir" и r#"…"…"## — сырые строки, ничего не экранируют',
    "Обратная косая черта в конце строки продолжает литерал на следующей строке",
  ],
  frames: [
    [
      rs("c", 30, 50, ['let s: &str = "привет";', "// только чтение"], [0], {
        w: 310,
        size: 12,
        lh: 24,
      }),
    ],
    [
      rs(
        "c",
        20,
        40,
        ['let p = r"C:\\Users\\bob";', 'let q = r#"он сказал "да""#;'],
        [0, 1],
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        ['let s = "первая \\', '    вторая";', '// "первая вторая"'],
        [0, 1],
        { w: 340, size: 11, lh: 22 },
      ),
    ],
  ],
});

// 3. String
export const V03 = scene({
  labels: ["Создание", "push и push_str", "Куча и ёмкость"],
  caption: [
    'String::from("…"), "…".to_string(), String::new() — три способа',
    "let mut s = String::new(); s.push('а'); s.push_str(\"бв\"); — дописываем",
    "В стеке — указатель, длина, ёмкость; сами байты лежат в куче и растут при необходимости",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        30,
        [
          'let a = String::from("раст");',
          'let b = "раст".to_string();',
          "let c = String::new();",
        ],
        undefined,
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        [
          "let mut s = String::new();",
          "s.push('а');",
          's.push_str("бв");   // "абв"',
        ],
        [1, 2],
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      Box("p", 80, 40, 120, 26, "ptr →", "b", { size: 10 }),
      Box("l", 80, 70, 120, 26, "len = 6", "b", { size: 10 }),
      Box("c", 80, 100, 120, 26, "cap = 8", "b", { size: 10 }),
      Box("h", 270, 66, 120, 80, "байты в куче", "g", { size: 10 }),
    ],
  ],
});

// 4. Склейка
export const V04 = scene({
  labels: ["+", "format!", "join"],
  caption: [
    "s1 + &s2: слева String, справа &str; s1 после этого использовать нельзя — + забирает левую строку",
    'format!("{} {}", a, b) ничего не забирает и работает как f-строка',
    '["а", "б", "в"].join(", ") — склейка списка через разделитель',
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          'let s1 = String::from("ab");',
          'let s2 = String::from("cd");',
          "let s3 = s1 + &s2;   // s1 забрана",
        ],
        [2],
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ['let name = "Аня";', 'let t = format!("Привет, {name}!");'],
        [1],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ['let v = ["а", "б", "в"];', 'let s = v.join(", ");   // "а, б, в"'],
        [1],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
  ],
});

// 5. UTF-8
export const V05 = scene({
  labels: ["Байты на символ", "len() ≠ символы", "chars().count()"],
  caption: [
    "UTF-8: латиница — 1 байт, кириллица — 2, иероглифы — 3, эмодзи — 4",
    '"привет".len() = 12: len считает байты, а не символы',
    '"привет".chars().count() = 6 — число символов',
  ],
  frames: [
    [
      ...["a — 1", "я — 2", "世 — 3", "😀 — 4"].map((t, i) =>
        Box(`a${i}`, 50 + i * 86, 66, 76, 30, t, ["g", "b", "y", "r"][i], {
          size: 10,
        }),
      ),
    ],
    [
      Box("a", 180, 40, 220, 28, "п р и в е т", "b", { size: 12 }),
      Tx("n", 180, 100, "6 символов × 2 = 12 байт", { size: 11 }),
    ],
    [
      rs(
        "c",
        30,
        50,
        [
          'let s = "привет";',
          "s.len()            // 12",
          "s.chars().count() // 6",
        ],
        [1, 2],
        { w: 300, size: 12, lh: 22 },
      ),
    ],
  ],
});

// 6. Индексы и срезы
export const V06 = scene({
  labels: ["Индекса нет", "Срез по байтам", "get"],
  caption: [
    "s[0] не компилируется: символ может занимать несколько байтов",
    "&s[0..4] — первые два русских символа; граница в середине символа — паника",
    "s.get(0..3) вернёт None вместо паники; n-й символ — s.chars().nth(n)",
  ],
  frames: [
    [
      rs("c", 30, 50, ['let s = "привет";', "let c = s[0];   // ✕"], [1], {
        w: 300,
        size: 12,
        lh: 24,
        bad: [1],
      }),
    ],
    [
      rs(
        "c",
        20,
        40,
        ['&s[0..4]   // "пр"', "&s[0..3]   // panic: не граница"],
        [1],
        { w: 340, size: 11, lh: 26, bad: [1] },
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        ["s.get(0..3)         // None", "s.chars().nth(2)    // Some('и')"],
        [0, 1],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
  ],
});

// 7. Перебор
export const V07 = scene({
  labels: ["chars и bytes", "split_whitespace и lines", "split"],
  caption: [
    "chars — символы, bytes — байты, char_indices — пары (позиция, символ)",
    "split_whitespace делит по пробелам, lines — по строкам",
    "split(',') делит по любому разделителю; collect собирает результат в Vec",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        30,
        [
          "for c in s.chars() { }",
          "for b in s.bytes() { }",
          "for (i, c) in s.char_indices() { }",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "for w in text.split_whitespace() { }",
          "for line in text.lines() { }",
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
        ["let parts: Vec<&str> =", "    \"a,b,c\".split(',').collect();"],
        [1],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
  ],
});

// 8. Методы
export const V08 = scene({
  labels: ["Поиск", "Преобразование", "Новое значение"],
  caption: [
    "contains, starts_with, ends_with, find (позиция или None)",
    "to_uppercase, to_lowercase, replace, trim",
    "Методы возвращают новую строку; исходная не меняется — результат нужно сохранить",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        30,
        [
          's.contains("ра")',
          's.starts_with("Ра")',
          's.find("т")     // Some(..)',
        ],
        undefined,
        { w: 340, size: 11, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        ["s.to_uppercase()", 's.replace("а", "о")', '"  x  ".trim()   // "x"'],
        undefined,
        { w: 340, size: 11, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["let up = s.to_uppercase();", "// s по-прежнему прежняя"],
        [0],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
  ],
});

// 9. split и parse
export const V09 = scene({
  labels: ["Разделить", "Превратить", "Ошибки"],
  caption: [
    "\"1, 2, 3\".split(',') — три куска, у каждого ещё пробелы: trim",
    "parse::<i32>() превращает кусок в число; собираем в Vec<i32>",
    "Если слово не число, parse вернёт ошибку: unwrap остановит программу, а можно пропустить или заменить",
  ],
  frames: [
    [
      Box("a", 70, 66, 70, 30, '"1"', "b", { size: 11 }),
      Box("b", 180, 66, 70, 30, '" 2"', "b", { size: 11 }),
      Box("c", 290, 66, 70, 30, '" 3"', "b", { size: 11 }),
    ],
    [
      rs(
        "c",
        20,
        30,
        [
          'let v: Vec<i32> = "1, 2, 3"',
          "    .split(',')",
          "    .map(|x| x.trim().parse().unwrap())",
          "    .collect();",
        ],
        [2, 3],
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
    [
      Box("a", 90, 60, 130, 34, '"abc".parse()\nErr', "r", { size: 10 }),
      Box("b", 270, 60, 130, 34, "unwrap → паника\nunwrap_or(0)", "y", {
        size: 10,
      }),
    ],
  ],
});

// 10. Сравнение и преобразование
export const V10 = scene({
  labels: ["==", "&str ↔ String", "Параметры функций"],
  caption: [
    "String и &str сравниваются через ==; порядок < и > — по байтам: заглавные раньше строчных",
    "&s или s.as_str() — из String в &str; to_string(), String::from — обратно",
    "Функции лучше принимать &str: подойдут и литерал, и &String; возвращать String для нового текста",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          'String::from("a") == "a"   // true',
          '"Z" < "a"                // true',
        ],
        undefined,
        { w: 340, size: 10, lh: 26 },
      ),
    ],
    [
      Box("a", 90, 60, 130, 34, "String\n→ &s", "b", { size: 10.5 }),
      Box("b", 270, 60, 130, 34, "&str\n→ to_string()", "g", { size: 10.5 }),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["fn shout(s: &str) -> String {", "    s.to_uppercase()", "}"],
        [0],
        { w: 340, size: 11, lh: 24 },
      ),
    ],
  ],
});

// 11. Форматирование
export const V11 = scene({
  labels: ["Ширина и выравнивание", "Точность и {:?}", "Имена"],
  caption: [
    "{:>10} — вправо, {:<10} — влево, {:^10} — по центру; {:*^10} — со своим заполнителем",
    "{:.2} — два знака после запятой; {:?} — отладочный вывод; {:#?} — красивый многострочный",
    "{name} прямо в строке, как в f-строках; {0} и {x} — по номеру и по имени",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        30,
        [
          'println!("[{:>6}]", "ab");   // [    ab]',
          'println!("[{:<6}]", "ab");   // [ab    ]',
          'println!("[{:^6}]", "ab");   // [  ab  ]',
        ],
        undefined,
        { w: 340, size: 9, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        36,
        [
          'println!("{:.2}", 3.14159);   // 3.14',
          'println!("{:?}", "текст");     // "текст"',
          'println!("{:?}", (1, 2));',
        ],
        undefined,
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["let n = 5;", 'println!("{n} + {n} = {}", n + n);'],
        [1],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
  ],
});

// 12. После Python
export const V12 = scene({
  labels: ["Две строки", "Длина и индексы", "Методы"],
  caption: [
    "Python: одна str; Rust: &str для чтения, String для владения и изменения",
    "Python: длина и индексы по символам; Rust: len в байтах, символы — через chars, s[i] нельзя",
    "f-строки → format!; strip → trim; join и split на месте; + забирает левую строку",
  ],
  frames: [
    [
      Box("a", 90, 60, 130, 34, "str", "m", { size: 12 }),
      Box("b", 270, 60, 130, 34, "&str / String", "g", { size: 11 }),
    ],
    [
      Box("a", 90, 60, 130, 34, "len → символы", "m", { size: 10.5 }),
      Box("b", 270, 60, 130, 34, "len → байты", "g", { size: 10.5 }),
    ],
    [
      Box("a", 90, 60, 130, 34, 'f"{x}"', "m", { size: 11 }),
      Box("b", 270, 60, 130, 34, 'format!("{x}")', "g", { size: 10.5 }),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Шпаргалка", "Дальше"],
  caption: [
    "&str читаем, String владеем; длина в байтах; символы — chars; срезы по границам символов",
    "format! для склейки; split, trim, parse — разбор; {:>10} {:.2} {:?} — формат",
    "Следующая глава — кортежи, массивы и векторы",
  ],
  frames: [
    [
      ...["&str", "String", "chars", "format!"].map((t, i) =>
        Box(`a${i}`, 50 + i * 86, 66, 76, 30, t, "g", { size: 10.5 }),
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        [
          "let words: Vec<&str> = text.split_whitespace().collect();",
          "let n = words.len();",
          "let up = text.to_uppercase();",
        ],
        undefined,
        { w: 340, size: 8.5, lh: 22 },
      ),
    ],
    [
      Box("a", 180, 60, 240, 34, "(i32, f64) · [i32; 3] · Vec<i32>", "b", {
        size: 10.5,
      }),
    ],
  ],
});
