import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, rs } from "./rs.tsx";

/* Глава 22 книги «Изучаем Rust»: модули, тесты и cargo. */

const sh = (id, x, y, lines, hl, extra = {}) => ({
  t: "code",
  id,
  x,
  y,
  lines,
  hl,
  size: 9.5,
  lh: 14,
  w: 200,
  ...extra,
});
const toml = sh;

// 1. Введение
export const V01 = scene({
  labels: ["Питон: набор утилит", "Раст: cargo", "Одна структура"],
  caption: [
    "В питоне проект — это venv, pip, pytest, black, mypy и конфиги для каждого",
    "В расте всё делает cargo: создаёт проект, собирает, запускает, тестирует, форматирует и скачивает зависимости",
    "Структура одинакова у всех проектов: Cargo.toml, src/, tests/ — открыв чужой репозиторий, вы знаете, где что",
  ],
  frames: [
    [
      ...["venv", "pip", "pytest", "black", "mypy"].map((t, i) =>
        Box(`a${i}`, 50 + i * 66, 70, 58, 28, t, "b", { size: 9 }),
      ),
      Tx("n", 180, 118, "каждая утилита — свой конфиг", { size: 9.5 }),
    ],
    [
      Box("c", 180, 50, 120, 34, "cargo", "g", { size: 14 }),
      ...["build", "run", "test", "fmt", "doc"].map((t, i) =>
        Box(`b${i}`, 50 + i * 66, 120, 58, 26, t, "y", { size: 9 }),
      ),
      ...[0, 1, 2, 3, 4].map((i) =>
        arrow(`e${i}`, 180 + (i - 2) * 20, 68, 50 + i * 66, 106, "g"),
      ),
    ],
    [
      sh(
        "t",
        30,
        30,
        [
          "my_app/",
          "├── Cargo.toml",
          "├── Cargo.lock",
          "├── src/",
          "│   ├── main.rs",
          "│   └── lib.rs",
          "└── tests/",
        ],
        [1, 3, 6],
        { w: 200, size: 10, lh: 17 },
      ),
    ],
  ],
});

// 2. cargo
export const V02 = scene({
  labels: ["new, build, run", "check, test, fmt", "debug и release"],
  caption: [
    "cargo new создаёт пакет; build собирает; run собирает и запускает; результат лежит в target/",
    "check только проверяет типы (быстро), test запускает тесты, fmt приводит к единому стилю, clippy ищет подозрительное",
    "Отладочная сборка быстрая и проверяет переполнение; релизная оптимизируется — как -O0 и -O3 у компилятора C",
  ],
  frames: [
    [
      sh(
        "c",
        20,
        40,
        [
          "$ cargo new hello",
          "$ cd hello",
          "$ cargo run",
          "   Compiling hello v0.1.0",
          "Hello, world!",
        ],
        [2],
        { w: 320, size: 10.5, lh: 18 },
      ),
    ],
    [
      ...["check", "test", "fmt", "clippy", "doc"].map((t, i) =>
        Box(`a${i}`, 50 + i * 66, 60, 58, 28, t, i === 0 ? "g" : "b", {
          size: 9,
        }),
      ),
      Tx("n", 180, 110, "check: типы без генерации кода", { size: 9.5 }),
      Tx("n2", 180, 130, "быстрее build в разы", { size: 9, c: "g" }),
    ],
    [
      Box("d", 90, 50, 120, 28, "debug (по умолчанию)", "y", { size: 9 }),
      Box("r", 270, 50, 120, 28, "--release", "g", { size: 9.5 }),
      {
        t: "bar",
        id: "b1",
        x: 90,
        y: 124,
        w: 40,
        hh: 16,
        max: 100,
        c: "y",
        text: "",
      },
      {
        t: "bar",
        id: "b2",
        x: 270,
        y: 124,
        w: 40,
        hh: 70,
        max: 100,
        c: "g",
        text: "",
      },
      Tx("l", 180, 144, "скорость программы", { size: 9 }),
    ],
  ],
});

// 3. Модули
export const V03 = scene({
  labels: ["Дерево модулей", "Пути", "use"],
  caption: [
    "Крейт — дерево модулей: mod объявляет модуль, содержимое лежит в скобках или в файле с тем же именем",
    "Путь идёт от корня (crate::), от текущего модуля (self::) или от родителя (super::)",
    "use приносит имя в область видимости; as переименовывает, фигурные скобки подтягивают несколько имён",
  ],
  frames: [
    [
      Box("r", 180, 30, 80, 24, "crate", "y", { size: 10 }),
      Box("a", 100, 80, 80, 24, "net", "b", { size: 10 }),
      Box("b", 260, 80, 80, 24, "db", "b", { size: 10 }),
      Box("c", 60, 130, 70, 22, "tcp", "g", { size: 9 }),
      Box("d", 150, 130, 70, 22, "udp", "g", { size: 9 }),
      arrow("e1", 150, 42, 120, 68, "g"),
      arrow("e2", 210, 42, 240, 68, "g"),
      arrow("e3", 80, 92, 64, 120, "g"),
      arrow("e4", 120, 92, 140, 120, "g"),
    ],
    [
      rs(
        "c",
        14,
        36,
        [
          "crate::net::tcp::connect()",
          "self::helper()",
          "super::config::load()",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        14,
        36,
        [
          "use std::collections::{HashMap, HashSet};",
          "use std::fmt::Result as FmtResult;",
          "use crate::net::tcp::*;",
        ],
        undefined,
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
  ],
});

// 4. Видимость
export const V04 = scene({
  labels: ["Закрыто по умолчанию", "Варианты pub", "Инварианты"],
  caption: [
    "Всё, что не помечено pub, видно только внутри своего модуля и его потомков",
    "pub — всем, pub(crate) — внутри крейта, pub(super) — родителю; поля структур закрываются отдельно",
    "Закрытое поле = нельзя собрать структуру в обход конструктора, значит конструктор гарантирует инвариант",
  ],
  frames: [
    [
      rs(
        "c",
        14,
        30,
        [
          "mod bank {",
          "    fn audit() {}            // закрыто",
          "    pub fn deposit() {}       // открыто",
          "}",
          "bank::deposit();  // ok",
          "bank::audit();    // ✕ E0603",
        ],
        [5],
        { w: 340, size: 9, lh: 16, bad: [5] },
      ),
    ],
    [
      ...[
        ["pub", "всем", "g"],
        ["pub(crate)", "внутри крейта", "y"],
        ["pub(super)", "родителю", "b"],
        ["(ничего)", "модулю и детям", "m"],
      ].map(([a, b, c], i) =>
        Box(`v${i}`, 90, 36 + i * 32, 130, 24, `${a} — ${b}`, c, { size: 8.5 }),
      ),
    ],
    [
      rs(
        "c",
        14,
        30,
        [
          "pub struct Percent(u8);   // поле закрыто",
          "impl Percent {",
          "    pub fn new(n: u8) -> Option<Percent> {",
          "        (n <= 100).then(|| Percent(n))",
          "    }",
          "}",
        ],
        [2, 3],
        { w: 350, size: 9, lh: 16 },
      ),
    ],
  ],
});

// 5. Реэкспорт
export const V05 = scene({
  labels: ["Глубокие пути", "pub use", "Prelude"],
  caption: [
    "Без реэкспорта пользователю пришлось бы писать длинную цепочку: mylib::shapes::circle::Circle",
    "pub use shapes::circle::Circle; — тип доступен коротко: mylib::Circle, а внутренняя структура остаётся вашим делом",
    "Часто используемое собирают в prelude и подключают одной строкой: use mylib::prelude::*;",
  ],
  frames: [
    [
      rs(
        "c",
        14,
        56,
        [
          "use mylib::shapes::circle::Circle;",
          "use mylib::shapes::rect::Rect;",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 22 },
      ),
      Tx("n", 180, 126, "утечка внутренней структуры", { size: 9.5, c: "y" }),
    ],
    [
      rs(
        "c",
        14,
        40,
        [
          "// lib.rs",
          "mod shapes;                // закрыт",
          "pub use shapes::circle::Circle;",
          "pub use shapes::rect::Rect;",
        ],
        [2, 3],
        { w: 340, size: 10, lh: 18 },
      ),
      Tx("n", 180, 128, "use mylib::{Circle, Rect};", {
        size: 9.5,
        mono: true,
        c: "g",
      }),
    ],
    [
      rs(
        "c",
        14,
        40,
        [
          "pub mod prelude {",
          "    pub use crate::{Circle, Rect, Shape};",
          "}",
          "use mylib::prelude::*;",
        ],
        [3],
        { w: 340, size: 10, lh: 18 },
      ),
    ],
  ],
});

// 6. Зависимости
export const V06 = scene({
  labels: ["Cargo.toml", "Cargo.lock", "Features"],
  caption: [
    'serde = "1.0" — «любая совместимая начиная с 1.0»; карго выберет самую новую из ветки 1.x',
    "Cargo.lock хранит точные версии, и каждая сборка получается одинаковой; для приложений его коммитят",
    'features включают нужный код: serde = { version = "1", features = ["derive"] } — лишнее не собирается',
  ],
  frames: [
    [
      toml(
        "c",
        14,
        30,
        [
          "[package]",
          'name = "hello"',
          'version = "0.1.0"',
          'edition = "2021"',
          "",
          "[dependencies]",
          'serde = "1.0"',
          'rand = "0.8"',
        ],
        [6, 7],
        { w: 340, size: 10, lh: 15 },
      ),
    ],
    [
      toml(
        "c",
        14,
        40,
        [
          "[[package]]",
          'name = "serde"',
          'version = "1.0.203"',
          'checksum = "a3f5…"',
        ],
        [2],
        { w: 340, size: 10.5, lh: 18 },
      ),
      Tx("n", 180, 128, "точная версия и хеш: воспроизводимо", {
        size: 9.5,
        c: "g",
      }),
    ],
    [
      toml(
        "c",
        14,
        40,
        [
          "[dependencies]",
          'serde = { version = "1", features = ["derive"] }',
          "",
          "[dev-dependencies]",
          'tempfile = "3"   # только для тестов',
        ],
        [1, 4],
        { w: 350, size: 8.5, lh: 18 },
      ),
    ],
  ],
});

// 7. Документация
export const V07 = scene({
  labels: ["Комментарий ///", "Doc-тест", "cargo doc"],
  caption: [
    "Три косые черты — документация элемента; //! описывает весь модуль или крейт",
    "Блок с кодом внутри комментария запускается как настоящий тест командой cargo test: документация не устаревает молча",
    "cargo doc строит страницы, как на docs.rs: в них видно сигнатуры, примеры и ссылки",
  ],
  frames: [
    [
      rs(
        "c",
        14,
        36,
        [
          "/// Возвращает сумму двух чисел.",
          "///",
          "/// # Панике",
          "/// Не паникует.",
          "pub fn add(a: i32, b: i32) -> i32 { a + b }",
        ],
        [0],
        { w: 350, size: 9.5, lh: 17 },
      ),
    ],
    [
      rs(
        "c",
        14,
        30,
        [
          "/// ```",
          "/// assert_eq!(mylib::add(2, 3), 5);",
          "/// ```",
          "pub fn add(a: i32, b: i32) -> i32 { ... }",
          "// cargo test → Doc-tests mylib ... ok",
        ],
        [1, 4],
        { w: 350, size: 9, lh: 17 },
      ),
    ],
    [
      Box("a", 70, 56, 90, 28, "///\nкомментарии", "b", { size: 9 }),
      arrow("e", 120, 56, 200, 56, "g"),
      Box("b", 290, 56, 110, 28, "target/doc/\nHTML-страницы", "g", {
        size: 9,
      }),
      Tx("n", 180, 110, "cargo doc --open", { size: 10, mono: true }),
    ],
  ],
});

// 8. Модульные тесты
export const V08 = scene({
  labels: ["#[cfg(test)]", "Макросы assert", "should_panic и Result"],
  caption: [
    "Тесты лежат рядом с кодом в модуле tests; атрибут cfg(test) включает его только при cargo test",
    "assert! проверяет условие, assert_eq! и assert_ne! показывают обе стороны при провале",
    "#[should_panic] ожидает панику; тест может вернуть Result и пользоваться ? — тогда Err означает провал",
  ],
  frames: [
    [
      rs(
        "c",
        14,
        30,
        [
          "#[cfg(test)]",
          "mod tests {",
          "    use super::*;",
          "    #[test]",
          "    fn adds() { assert_eq!(add(2, 3), 5); }",
          "}",
        ],
        [0, 3],
        { w: 350, size: 9.5, lh: 17 },
      ),
    ],
    [
      rs(
        "c",
        14,
        40,
        [
          "assert!(is_even(4));",
          "assert_eq!(add(2, 2), 4);",
          "assert_ne!(add(2, 2), 5);",
          "// left: 5  right: 4   ← при провале",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 18 },
      ),
    ],
    [
      rs(
        "c",
        14,
        30,
        [
          "#[test]",
          '#[should_panic(expected = "деление на ноль")]',
          "fn div_by_zero() { div(1, 0); }",
          "#[test]",
          "fn parses() -> Result<(), ParseIntError> {",
          '    assert_eq!("7".parse::<i32>()?, 7);',
          "    Ok(())",
          "}",
        ],
        [1, 4],
        { w: 350, size: 8.5, lh: 15 },
      ),
    ],
  ],
});

// 9. Интеграционные тесты
export const V09 = scene({
  labels: ["Папка tests/", "Крейт-клиент", "lib + тонкий main"],
  caption: [
    "Каждый файл в tests/ — отдельный крейт: он подключает библиотеку как внешний пользователь",
    "Поэтому видны только pub-элементы: контракт проверяется так, как его увидит пользователь",
    "Исполняемый крейт делают тонким: main вызывает библиотеку, а вся логика покрыта тестами библиотеки",
  ],
  frames: [
    [
      rs(
        "c",
        14,
        30,
        [
          "my_app/",
          "├── src/lib.rs",
          "├── src/main.rs",
          "└── tests/",
          "    ├── api.rs",
          "    └── common/mod.rs",
        ],
        [3, 4, 5],
        { w: 220, size: 10, lh: 17 },
      ),
      Tx("n", 290, 70, "тест-файл =\nотдельный крейт", { size: 9, c: "g" }),
    ],
    [
      Box("t", 80, 70, 110, 34, "tests/api.rs", "b", { size: 10 }),
      arrow("e", 134, 70, 214, 70, "g"),
      Box("l", 290, 70, 110, 34, "mylib\n(только pub)", "g", { size: 9.5 }),
      Tx("n", 180, 126, "use mylib::add;  — как у пользователя", {
        size: 9,
        mono: true,
      }),
    ],
    [
      Box("m", 70, 60, 90, 30, "main.rs\n3 строки", "b", { size: 9.5 }),
      arrow("e", 116, 60, 196, 60, "g"),
      Box("l", 280, 60, 130, 44, "lib.rs\nвся логика\n+ тесты", "g", {
        size: 9,
      }),
    ],
  ],
});

// 10. Хорошие тесты
export const V10 = scene({
  labels: ["Подготовь–выполни–проверь", "Таблица случаев", "Сломай и проверь"],
  caption: [
    "Подготовить данные, выполнить действие, проверить результат: три части, одна проверка по смыслу на тест",
    "Таблица пар «вход → ожидаемое» прогоняется одним циклом; главное — граничные случаи: пусто, ноль, максимум, минус",
    "Мутационная проверка: нарочно сломайте реализацию — хотя бы один тест обязан покраснеть",
  ],
  frames: [
    [
      rs(
        "c",
        14,
        36,
        [
          "let mut s = Stack::new();      // arrange",
          "s.push(1);                     // act",
          "assert_eq!(s.pop(), Some(1));  // assert",
        ],
        [0, 1, 2],
        { w: 350, size: 9, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        14,
        30,
        [
          "let cases = [(0, 0), (1, 1), (-1, 1),",
          "             (i32::MAX, i32::MAX)];",
          "for (x, want) in cases {",
          "    assert_eq!(abs(x), want);",
          "}",
        ],
        [0, 1],
        { w: 350, size: 9.5, lh: 17 },
      ),
    ],
    [
      Box("g", 100, 50, 150, 26, "верная реализация: 0 провалов", "g", {
        size: 8,
      }),
      Box("m", 90, 90, 110, 26, "мутант: abs → x", "r", { size: 8.5 }),
      Box("r", 280, 90, 110, 26, "провалов ≥ 1", "g", { size: 9 }),
      arrow("e", 146, 90, 224, 90, "g"),
      Tx("n", 180, 140, "тесты, которые не краснеют — не тесты", { size: 9.5 }),
    ],
  ],
});

// 11. Ошибки библиотеки
export const V11 = scene({
  labels: ["Перечисление ошибок", "source()", "non_exhaustive"],
  caption: [
    "Публичная функция возвращает Result со своим enum: Display для людей, Error для экосистемы, From для ?",
    "Метод source() отдаёт причину — так строятся цепочки «не удалось прочитать конфиг: неверное число»",
    "#[non_exhaustive] разрешает позже добавлять варианты без ломки совместимости; паниковать можно лишь при нарушении контракта",
  ],
  frames: [
    [
      rs(
        "c",
        14,
        30,
        [
          "#[derive(Debug)]",
          "pub enum ConfigError {",
          "    Missing(String),",
          "    BadNumber(ParseIntError),",
          "}",
        ],
        [1],
        { w: 340, size: 10, lh: 17 },
      ),
    ],
    [
      Box("a", 70, 60, 100, 28, "ConfigError", "y", { size: 10 }),
      arrow("e", 120, 60, 200, 60, "g"),
      Box("b", 290, 60, 120, 28, "ParseIntError\n(причина)", "b", { size: 9 }),
      Tx("n", 180, 110, "err.source()", { size: 10, mono: true }),
    ],
    [
      rs(
        "c",
        14,
        40,
        [
          "#[non_exhaustive]",
          "pub enum Error { A, B }",
          "// клиенты обязаны писать _ => …",
          "// → можно добавить C без major-релиза",
        ],
        [0],
        { w: 350, size: 9.5, lh: 20 },
      ),
    ],
  ],
});

// 12. cfg, const и глобальное
export const V12 = scene({
  labels: ["cfg", "const fn", "Атомики и OnceLock"],
  caption: [
    "#[cfg(...)] и cfg!(...) выбирают код под ОС, разрядность, режим сборки или фичу — лишнее даже не компилируется",
    "const fn и const вычисляются при сборке: таблица квадратов лежит прямо в исполняемом файле",
    "Глобальный счётчик — AtomicUsize; значение, которое надо создать один раз, — OnceLock; изменяемые static требуют unsafe",
  ],
  frames: [
    [
      rs(
        "c",
        14,
        36,
        [
          '#[cfg(target_os = "linux")]',
          "fn sep() -> char { '/' }",
          "if cfg!(debug_assertions) { /* отладка */ }",
        ],
        [0],
        { w: 340, size: 9.5, lh: 20 },
      ),
    ],
    [
      rs(
        "c",
        14,
        36,
        [
          "const fn sq(x: u32) -> u32 { x * x }",
          "const TABLE: [u32; 4] = [sq(1), sq(2), sq(3), sq(4)];",
          "// 1, 4, 9, 16 — в .rodata",
        ],
        [1],
        { w: 350, size: 9, lh: 20 },
      ),
    ],
    [
      rs(
        "c",
        14,
        30,
        [
          "static NEXT: AtomicUsize = AtomicUsize::new(0);",
          "fn id() -> usize { NEXT.fetch_add(1, Ordering::Relaxed) }",
          "static CFG: OnceLock<String> = OnceLock::new();",
        ],
        [0, 2],
        { w: 350, size: 8.5, lh: 20 },
      ),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Проект", "Качество", "Дальше"],
  caption: [
    "cargo — одна утилита на всё; крейты и модули с закрытой по умолчанию видимостью; pub use формирует интерфейс",
    "Версии и features управляют зависимостями, документация запускается как тесты, а хорошие тесты ловят сломанную реализацию",
    "Дальше — потоки и общее состояние: Mutex, каналы, Arc и гонки данных",
  ],
  frames: [
    [
      Box("a", 70, 66, 100, 34, "cargo", "g", { size: 12 }),
      Box("b", 180, 66, 100, 34, "крейты\nи модули", "b", { size: 9.5 }),
      Box("c", 290, 66, 100, 34, "pub use", "y", { size: 10.5 }),
    ],
    [
      Box("a", 70, 66, 100, 34, "версии\nи features", "b", { size: 9.5 }),
      Box("b", 180, 66, 100, 34, "doc-тесты", "y", { size: 10 }),
      Box("c", 290, 66, 100, 34, "мутации", "g", { size: 10.5 }),
    ],
    [
      Box("a", 70, 66, 100, 34, "thread", "b", { size: 11 }),
      Box("b", 180, 66, 100, 34, "Mutex\nArc", "y", { size: 10 }),
      Box("c", 290, 66, 100, 34, "каналы", "g", { size: 10.5 }),
    ],
  ],
});
