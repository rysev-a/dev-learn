import { scene } from "./alg.tsx";
import { Box, rs } from "./rs.tsx";

/* Глава 10 книги «Изучаем Rust»: функции и условные конструкции — def и fn. */

const pair = (a: string, b: string, ca = "m", cb = "g", y = 60) => [
  Box("pa", 90, y, 130, 34, a, ca, { size: 10 }),
  Box("pb", 270, y, 130, 34, b, cb, { size: 10 }),
];

// 1. Введение
export const V01 = scene({
  labels: ["def → fn", "Скобки вместо отступов", "Что заменяется"],
  caption: [
    "Большая часть питоновского кода переводится на Rust почти один в один",
    "Двоеточие и отступ → фигурные скобки; elif → else if",
    "Где Python даёт свободу, а Rust нет — разберём, чем её заменить",
  ],
  frames: [
    [...pair("def f(a):", "fn f(a: i32) -> i32", "m", "g")],
    [
      rs(
        "c",
        20,
        30,
        ["if x > 0:", "    y = 1", "elif x < 0:", "    y = -1"],
        undefined,
        { w: 160, size: 11, lh: 20 },
      ),
      rs(
        "d",
        190,
        30,
        ["if x > 0 {", "    y = 1", "} else if x < 0 {", "    y = -1", "}"],
        undefined,
        { w: 160, size: 9.5, lh: 20 },
      ),
    ],
    [
      ...["аргументы", "*args", "yield", "try"].map((t, i) =>
        Box(`a${i}`, 50 + i * 86, 66, 76, 30, t, "y", { size: 10 }),
      ),
    ],
  ],
});

// 2. Сигнатуры
export const V02 = scene({
  labels: ["Python", "Rust", "Обобщения"],
  caption: [
    "def add(a, b): — типы не обязательны; аннотации интерпретатор не проверяет",
    "fn add(a: i32, b: i32) -> i32 — типы обязательны, проверка при каждом вызове",
    "Универсальный код — через обобщения: fn add<T: Add>(a: T, b: T) -> T",
  ],
  frames: [
    [
      rs(
        "c",
        30,
        50,
        ["def add(a, b):", "    return a + b", 'add(1, 2); add("а", "б")'],
        undefined,
        { w: 300, size: 11.5, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["fn add(a: i32, b: i32) -> i32 {", "    a + b", "}"],
        [0],
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "fn add<T: std::ops::Add<Output = T>>(",
          "    a: T, b: T) -> T {",
          "    a + b",
          "}",
        ],
        [0],
        { w: 340, size: 9, lh: 20 },
      ),
    ],
  ],
});

// 3. Значения по умолчанию
export const V03 = scene({
  labels: ["Нет default", "Option", "Строитель"],
  caption: [
    'def hi(name="мир"): — в Rust нельзя: параметры без значений по умолчанию и без имён',
    'Принять Option<&str> и подставить unwrap_or("мир"), либо написать две функции',
    "Собрать параметры в структуру со значениями по умолчанию — шаблон «строитель»",
  ],
  frames: [
    [
      rs(
        "c",
        30,
        50,
        ['def hi(name="мир"): ...', '// fn hi(name = "мир")  ✕'],
        [1],
        { w: 300, size: 12, lh: 26, bad: [1] },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "fn hi(name: Option<&str>) {",
          '    let n = name.unwrap_or("мир");',
          "}",
        ],
        [1],
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        [
          "Config::default()",
          '    .name("Аня")',
          "    .retries(3)",
          "    .build()",
        ],
        undefined,
        { w: 340, size: 11.5, lh: 22 },
      ),
    ],
  ],
});

// 4. *args и **kwargs
export const V04 = scene({
  labels: ["*args → срез", "Разные типы", "**kwargs"],
  caption: [
    "*args → параметр-срез: fn total(v: &[i32]) — передаём массив или вектор",
    "Значения разных типов — структура или перечисление",
    "**kwargs → структура с полями или HashMap; у макросов (println!) число аргументов произвольно",
  ],
  frames: [
    [
      rs(
        "c",
        30,
        50,
        ["def total(*args): ...", "fn total(v: &[i32]) -> i32"],
        [1],
        { w: 310, size: 11, lh: 26 },
      ),
    ],
    [...pair('(1, "а", 2.5)', "struct / enum", "b", "g")],
    [...pair("**kwargs", "struct Options { … }", "m", "g")],
  ],
});

// 5. Возврат
export const V05 = scene({
  labels: ["Кортежем", "None → ()", "Option и Result"],
  caption: [
    "return a, b → fn f() -> (i32, i32) { (a, b) }; результат — последнее выражение",
    "Нет return → None; в Rust без стрелки возвращается ()",
    "Значения может не быть — Option<T>; операция может не получиться — Result<T, E>",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["return a, b", "(a, b)   // Rust: последнее выражение"],
        [1],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
    [...pair("None", "()", "m", "g")],
    [...pair("Option<T>\nнет значения", "Result<T, E>\nошибка", "y", "r")],
  ],
});

// 6. Функции как значения
export const V06 = scene({
  labels: ["Указатель на функцию", "Замыкание", "Передача"],
  caption: [
    "Обычную функцию передают по имени; её тип — fn(i32) -> i32",
    "lambda x: x + 1 → |x| x + 1: замыкание может захватывать переменные",
    "apply(f, 5) — функция принимает другую функцию; подробно — в главе про итераторы",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ["fn inc(x: i32) -> i32 { x + 1 }", "let f: fn(i32) -> i32 = inc;"],
        [1],
        { w: 340, size: 10, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["let f = |x| x + 1;", "let k = 10;", "let g = |x| x + k;   // захват"],
        [0, 2],
        { w: 340, size: 11, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["fn apply(f: fn(i32) -> i32, x: i32) -> i32 {", "    f(x)", "}"],
        [0],
        { w: 340, size: 9.5, lh: 24 },
      ),
    ],
  ],
});

// 7. Документация
export const V07 = scene({
  labels: ["docstring", "///", "Doctest"],
  caption: [
    "Python: строка в тройных кавычках сразу после def",
    "Rust: /// перед функцией, разметка Markdown; cargo doc собирает сайт документации",
    "Пример кода в комментарии запускается как тест (cargo test) — документация не устареет",
  ],
  frames: [
    [
      rs("c", 30, 40, ["def f(x):", '    """Удваивает x."""'], undefined, {
        w: 300,
        size: 12,
        lh: 26,
      }),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "/// Удваивает число.",
          "fn double(x: i32) -> i32 {",
          "    x * 2",
          "}",
        ],
        [0],
        { w: 340, size: 11, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        ["/// ```", "/// assert_eq!(double(2), 4);", "/// ```"],
        [1],
        { w: 340, size: 11, lh: 22 },
      ),
    ],
  ],
});

// 8. Условия
export const V08 = scene({
  labels: ["if / else if", "Только bool", "and, or, not"],
  caption: [
    "if / elif / else → if / else if / else; скобки вокруг условия не нужны",
    "if lst: и if not x: нельзя — явное сравнение: if !v.is_empty()",
    "and, or, not → &&, ||, !; x if c else y → if c { x } else { y }; in → contains",
  ],
  frames: [
    [...pair("elif", "else if", "m", "g")],
    [...pair("if lst:", "if !v.is_empty()", "m", "g")],
    [
      rs(
        "c",
        20,
        40,
        ["a and not b   →   a && !b", "x in v          →   v.contains(&x)"],
        undefined,
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
  ],
});

// 9. match и цепочки
export const V09 = scene({
  labels: ["Цепочка 1 < x < 10", "match", "Охранники"],
  caption: [
    "Цепочки сравнений нет: пишите x > 1 && x < 10 или (2..10).contains(&x)",
    "match-case Python 3.10 → match: диапазоны, | и разбор структур, все случаи обязательны",
    "Охранник: Some(n) if n > 0 => … — дополнительное условие в ветке",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "1 < x < 10          # Python",
          "x > 1 && x < 10   // Rust",
          "(2..10).contains(&x)",
        ],
        [1, 2],
        { w: 340, size: 10.5, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        [
          "match n {",
          '    0 => "ноль",',
          '    1 | 2 => "мало",',
          '    3..=9 => "средне",',
          '    _ => "много",',
          "}",
        ],
        [2, 3],
        { w: 340, size: 10, lh: 18 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "match x {",
          '    Some(n) if n > 0 => "плюс",',
          '    Some(_) => "не плюс",',
          '    None => "нет",',
          "}",
        ],
        [1],
        { w: 340, size: 10, lh: 20 },
      ),
    ],
  ],
});

// 10. Циклы
export const V10 = scene({
  labels: ["range", "while и loop", "Нет for-else"],
  caption: [
    "for i in range(n) → for i in 0..n; шаг — step_by, обратно — rev(); enumerate и zip есть",
    "while → while; while True → loop; break может вернуть значение; метки выходят из вложенных циклов",
    "У цикла нет ветки else: поиск пишут флагом или методами find и any",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "for i in range(n):        for i in 0..n {",
          "for i in range(10, 0, -1): for i in (1..=10).rev()",
        ],
        undefined,
        { w: 340, size: 7.5, lh: 26 },
      ),
    ],
    [...pair("while True:", "loop { … }", "m", "g")],
    [
      rs(
        "c",
        20,
        40,
        [
          "let found = v.iter().any(|&x| x == 7);",
          "let pos = v.iter().position(|&x| x == 7);",
        ],
        undefined,
        { w: 340, size: 9, lh: 26 },
      ),
    ],
  ],
});

// 11. Ошибки
export const V11 = scene({
  labels: ["Нет исключений", "?", "panic!"],
  caption: [
    "try / except → Result: функция сама говорит о возможной ошибке в типе",
    "Оператор ? передаёт ошибку вызывающей функции — как raise, но видно в сигнатуре",
    "panic! — для неисправимого (аналог raise без перехвата); assert! — проверка условий",
  ],
  frames: [
    [...pair("try:\n    … except", "match / ?\nна Result", "m", "g")],
    [
      rs(
        "c",
        20,
        40,
        [
          "fn read() -> Result<i32, ParseIntError> {",
          '    let n = "5".parse::<i32>()?;',
          "    Ok(n)",
          "}",
        ],
        [1],
        { w: 340, size: 9, lh: 22 },
      ),
    ],
    [...pair("raise Exception", 'panic!("…")', "m", "r")],
  ],
});

// 12. Генераторы
export const V12 = scene({
  labels: ["yield → Iterator", "Включение", "any и all"],
  caption: [
    "Генераторы Python → итераторы Rust: всё, у чего есть next(), работает в for и в цепочках",
    "[x*2 for x in v if x > 0] → v.iter().filter(…).map(…).collect()",
    "any(…) и all(…) → методы any и all итераторов; цепочка компилируется в обычный цикл",
  ],
  frames: [
    [...pair("yield x", "impl Iterator\nfn next()", "m", "g")],
    [
      rs(
        "c",
        20,
        40,
        [
          "let r: Vec<i32> = v.iter()",
          "    .filter(|x| **x > 0)",
          "    .map(|x| x * 2)",
          "    .collect();",
        ],
        [1, 2],
        { w: 340, size: 10.5, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["v.iter().any(|&x| x > 9)", "v.iter().all(|&x| x > 0)"],
        undefined,
        { w: 340, size: 11, lh: 26 },
      ),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Шпаргалка", "Дальше"],
  caption: [
    "def → fn; типы обязательны; нет default и *args; результат — последнее выражение",
    "if и match — выражения; нет цепочек сравнений и for-else; нет исключений; генераторы → итераторы",
    "Следующая глава — строки: str из Python и String с &str из Rust",
  ],
  frames: [
    [
      ...["fn", "типы", "match", "Result"].map((t, i) =>
        Box(`a${i}`, 50 + i * 86, 66, 76, 30, t, "g", { size: 11 }),
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        [
          "fn f(x: i32) -> Option<i32> {",
          "    if x > 0 { Some(x) } else { None }",
          "}",
        ],
        undefined,
        { w: 340, size: 9.5, lh: 24 },
      ),
    ],
    [Box("a", 180, 60, 240, 34, "str ↔ String / &str", "b", { size: 11.5 })],
  ],
});
