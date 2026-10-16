import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, rs, slot } from "./rs.tsx";

/* Глава 8 книги «Изучаем Rust»: структуры, перечисления, Option и Result. */

// 1. Свои типы
export const V01 = scene({
  labels: ["Зачем свои типы", "struct и enum", "impl"],
  caption: [
    "Для больших программ нужны свои типы: пользователь, точка, цвет, статус",
    "struct — несколько полей в одном типе; enum — одно из нескольких значений",
    "impl — блок методов: данные и поведение рядом, без наследования",
  ],
  frames: [
    [
      Box("a", 70, 60, 90, 34, "User", "b", { size: 12 }),
      Box("b", 180, 60, 90, 34, "Point", "b", { size: 12 }),
      Box("c", 290, 60, 90, 34, "Status", "b", { size: 12 }),
    ],
    [
      Box("a", 90, 60, 130, 40, "struct\nполя", "g", { size: 11.5 }),
      Box("b", 270, 60, 130, 40, "enum\nварианты", "y", { size: 11.5 }),
    ],
    [
      rs("c", 30, 40, ["impl User {", "    fn greet(&self) { … }", "}"], [0], {
        w: 300,
        size: 12,
        lh: 24,
      }),
    ],
  ],
});

// 2. struct
export const V02 = scene({
  labels: ["Объявление", "Создание", "Поля"],
  caption: [
    "struct User { name: String, age: u32 } — поля с именами и типами",
    'User { name: String::from("Аня"), age: 30 } — указываем все поля по именам, порядок не важен',
    "u.name, u.age — доступ к полю через точку; это новый тип, его не спутать с чужим",
  ],
  frames: [
    [
      rs(
        "c",
        30,
        36,
        ["struct User {", "    name: String,", "    age: u32,", "}"],
        [0],
        { w: 300, size: 12, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        [
          "let u = User {",
          '    name: String::from("Аня"),',
          "    age: 30,",
          "};",
        ],
        [1, 2],
        { w: 340, size: 11, lh: 22 },
      ),
    ],
    [
      Box("a", 90, 60, 130, 40, 'u.name\n"Аня"', "b", { size: 11 }),
      Box("b", 270, 60, 130, 40, "u.age\n30", "g", { size: 11 }),
    ],
  ],
});

// 3. Изменение и сокращения
export const V03 = scene({
  labels: ["let mut", "Сокращённая запись", "Обновление и derive"],
  caption: [
    "Поле меняется, только если вся структура объявлена mut; отдельно сделать поле mut нельзя",
    "Если переменная названа как поле, пишем одно имя: User { name, age }",
    "..old копирует остальные поля; #[derive(Debug)] включает печать через {:?}",
  ],
  frames: [
    [
      rs("c", 30, 40, ["let mut u = User { … };", "u.age += 1;   // ✓"], [1], {
        w: 300,
        size: 12,
        lh: 26,
      }),
    ],
    [
      rs(
        "c",
        30,
        40,
        ['let name = String::from("Аня");', "let u = User { name, age: 30 };"],
        [1],
        { w: 310, size: 11, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        [
          "#[derive(Debug)]",
          "struct User { … }",
          "let v = User { age: 31, ..u };",
          'println!("{:?}", v);',
        ],
        [0, 2],
        { w: 340, size: 10.5, lh: 22 },
      ),
    ],
  ],
});

// 4. impl и &self
export const V04 = scene({
  labels: ["impl", "&self читает", "Вызов"],
  caption: [
    "impl User { … } — функции внутри пишут методы; первый параметр self — «тот, у кого вызвали»",
    "&self — метод только читает; в теле поля берутся через self.name",
    "u.greet() — вызов как в Python: данные и поведение рядом",
  ],
  frames: [
    [
      rs(
        "c",
        30,
        40,
        [
          "impl User {",
          "    fn greet(&self) -> String {",
          '        format!("Привет, {}", self.name)',
          "    }",
          "}",
        ],
        [1],
        { w: 320, size: 9.5, lh: 20 },
      ),
    ],
    [
      Box("a", 90, 66, 130, 40, "&self\n(только чтение)", "b", { size: 11 }),
      Box("b", 270, 66, 130, 40, "self.name\nself.age", "g", { size: 11 }),
    ],
    [
      rs(
        "c",
        30,
        50,
        ["let u = User { … };", 'u.greet()   // "Привет, Аня"'],
        [1],
        { w: 310, size: 12, lh: 26 },
      ),
    ],
  ],
});

// 5. &mut self и new
export const V05 = scene({
  labels: ["&mut self", "self целиком", "new"],
  caption: [
    "&mut self — метод меняет поля; вызывать можно только у let mut",
    "self без амперсанда забирает экземпляр: после вызова им пользоваться нельзя (подробнее — в главе про владение)",
    "Ассоциированная функция без self: User::new(…) — договорённость, не особое слово языка",
  ],
  frames: [
    [
      rs(
        "c",
        30,
        40,
        ["fn birthday(&mut self) {", "    self.age += 1;", "}"],
        [0, 1],
        { w: 310, size: 12, lh: 24 },
      ),
    ],
    [
      Box("a", 90, 60, 130, 40, "&self\nчитает", "g", { size: 11 }),
      Box("b", 180, 60, 100, 40, "&mut self\nменяет", "y", { size: 10 }),
      Box("c", 290, 60, 100, 40, "self\nзабирает", "r", { size: 10.5 }),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "impl User {",
          "    fn new(name: &str, age: u32) -> User {",
          "        User { name: name.to_string(), age }",
          "    }",
          "}",
        ],
        [1],
        { w: 340, size: 9, lh: 20 },
      ),
    ],
  ],
});

// 6. Кортежные структуры
export const V06 = scene({
  labels: ["Кортежная структура", "Новый тип", "Юнит-структура"],
  caption: [
    "struct Color(u8, u8, u8); — поля без имён, доступ c.0, c.1, c.2",
    "Метры и футы — оба числа, но разные типы: сложить по ошибке нельзя",
    "struct Marker; — без полей, нужна как метка; для данных лучше структура с именами полей",
  ],
  frames: [
    [
      rs(
        "c",
        30,
        40,
        [
          "struct Color(u8, u8, u8);",
          "let red = Color(255, 0, 0);",
          "red.0   // 255",
        ],
        [0, 2],
        { w: 310, size: 11.5, lh: 22 },
      ),
    ],
    [
      Box("a", 90, 60, 130, 36, "Meters(f64)", "b", { size: 11 }),
      Box("b", 270, 60, 130, 36, "Feet(f64)", "y", { size: 11 }),
      Tx("n", 180, 116, "Meters + Feet ✕", { size: 10.5, c: "r" }),
    ],
    [
      rs("c", 30, 50, ["struct Marker;", "let m = Marker;"], undefined, {
        w: 300,
        size: 13,
        lh: 24,
      }),
    ],
  ],
});

// 7. enum
export const V07 = scene({
  labels: ["Варианты", "Значение", "Точность"],
  caption: [
    "enum Direction { Up, Down, Left, Right } — значение — один из перечисленных вариантов",
    "Direction::Up — имя типа и вариант через ::",
    'Нельзя написать "вверху" или передать число 7: компилятор знает все варианты',
  ],
  frames: [
    [
      ...["Up", "Down", "Left", "Right"].map((t, i) =>
        Box(`a${i}`, 50 + i * 86, 66, 76, 32, t, "g", { size: 11 }),
      ),
    ],
    [
      rs("c", 30, 50, ["let d = Direction::Up;"], [0], {
        w: 310,
        size: 12.5,
        lh: 26,
      }),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["let d = Direction::Upp;   // ✕", "let e: Direction = 7;   // ✕"],
        [0, 1],
        { w: 340, size: 10.5, lh: 26, bad: [0, 1] },
      ),
    ],
  ],
});

// 8. Данные в вариантах
export const V08 = scene({
  labels: ["Варианты с данными", "Разные формы", "Один тип"],
  caption: [
    "Circle(f64) хранит радиус, Rect(f64, f64) — две стороны",
    "Каждый вариант имеет свои данные: в Python пришлось бы писать несколько классов",
    "Все варианты вместе — один тип Shape: размер значения равен самому большому варианту плюс метка",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        30,
        ["enum Shape {", "    Circle(f64),", "    Rect(f64, f64),", "}"],
        [1, 2],
        { w: 340, size: 12, lh: 22 },
      ),
    ],
    [
      Box("a", 90, 60, 130, 40, "Circle(2.0)", "g", { size: 11 }),
      Box("b", 270, 60, 130, 40, "Rect(3.0, 4.0)", "b", { size: 10.5 }),
    ],
    [
      Box("a", 180, 56, 260, 46, "тип Shape: один из вариантов", "y", {
        size: 11,
      }),
    ],
  ],
});

// 9. match
export const V09 = scene({
  labels: ["Образец с данными", "Все варианты", "Новый вариант"],
  caption: [
    "match shape { Shape::Circle(r) => …, Shape::Rect(a, b) => … } — данные достаются в переменные",
    "Компилятор проверяет, что учтён каждый вариант",
    "Добавили вариант — все match без него не собираются: компилятор показывает места, где нужно поменять код",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        30,
        [
          "match shape {",
          "    Shape::Circle(r) => 3.14 * r * r,",
          "    Shape::Rect(a, b) => a * b,",
          "}",
        ],
        [1, 2],
        { w: 340, size: 10, lh: 22 },
      ),
    ],
    [
      Box("a", 90, 60, 130, 36, "Circle ✓", "g", { size: 11 }),
      Box("b", 270, 60, 130, 36, "Rect ✓", "g", { size: 11 }),
    ],
    [
      Box("a", 90, 60, 130, 36, "Triangle (новый)", "y", { size: 10 }),
      Box("b", 270, 60, 130, 36, "✕ non-exhaustive", "r", { size: 10 }),
    ],
  ],
});

// 10. Option
export const V10 = scene({
  labels: ["Some и None", "Нет null", "Как работать"],
  caption: [
    "Option<T> — «значение или ничего»: Some(x) или None",
    "В других языках пустая ссылка валит программу; в Rust значение, которого может не быть, всегда Option",
    "match, if let Some(x) = …, unwrap(), unwrap_or(0) — варианты работы",
  ],
  frames: [
    [
      Box("a", 90, 60, 130, 36, "Some(5)", "g", { size: 12 }),
      Box("b", 270, 60, 130, 36, "None", "m", { size: 12 }),
    ],
    [
      Box("a", 90, 60, 130, 36, "null → падение", "r", { size: 10.5 }),
      Box("b", 270, 60, 130, 36, "Option → проверка", "g", { size: 10.5 }),
    ],
    [
      rs(
        "c",
        20,
        30,
        [
          "if let Some(x) = v.first() {",
          '    println!("{x}");',
          "}",
          "let n = v.first().copied().unwrap_or(0);",
        ],
        [0, 3],
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
  ],
});

// 11. Result
export const V11 = scene({
  labels: ["Ok и Err", "parse", "Позже"],
  caption: [
    "Result<T, E> — операция может не получиться: Ok(значение) или Err(ошибка)",
    '"5".parse::<i32>() → Ok(5); "x".parse::<i32>() → Err(…)',
    "Подробно — в главе про обработку ошибок; результат нельзя «забыть проверить»",
  ],
  frames: [
    [
      Box("a", 90, 60, 130, 36, "Ok(5)", "g", { size: 12 }),
      Box("b", 270, 60, 130, 36, "Err(…)", "r", { size: 12 }),
    ],
    [
      rs(
        "c",
        20,
        40,
        ['"5".parse::<i32>()   // Ok(5)', '"x".parse::<i32>()   // Err(..)'],
        undefined,
        { w: 340, size: 11, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "match s.parse::<i32>() {",
          '    Ok(n) => println!("{n}"),',
          '    Err(e) => println!("ошибка: {e}"),',
          "}",
        ],
        [1, 2],
        { w: 340, size: 9.5, lh: 20 },
      ),
    ],
  ],
});

// 12. После Python
export const V12 = scene({
  labels: ["class → struct + impl", "Enum и None", "Исключения"],
  caption: [
    "Класс → struct и impl; __init__ → new; dataclass → struct с #[derive]; наследования нет — есть трейты",
    "Enum в Python — константы; в Rust — тип с данными; None → Option",
    "Исключения → Result; ошибка «у None нет атрибута» невозможна: компилятор не пропустит",
  ],
  frames: [
    [
      Box("a", 90, 60, 130, 34, "class User", "m", { size: 11 }),
      Box("b", 270, 60, 130, 34, "struct + impl", "g", { size: 11 }),
    ],
    [
      Box("a", 90, 60, 130, 34, "None", "m", { size: 12 }),
      Box("b", 270, 60, 130, 34, "Option<T>", "g", { size: 12 }),
    ],
    [
      Box("a", 90, 60, 130, 34, "try / except", "m", { size: 11 }),
      Box("b", 270, 60, 130, 34, "Result<T, E>", "g", { size: 11 }),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Шпаргалка", "Дальше"],
  caption: [
    "struct — поля, impl — методы, enum — варианты с данными, match — обработка всех",
    "Option — «значение или ничего», Result — «получилось или ошибка»",
    "Дальше раздел «Rust после Python»: сравним все темы по очереди и закрепим",
  ],
  frames: [
    [
      ...["struct", "impl", "enum", "match"].map((t, i) =>
        Box(`a${i}`, 50 + i * 86, 66, 76, 30, t, "g", { size: 11 }),
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        [
          "struct P { x: i32 }",
          "impl P { fn new(x: i32) -> P { P { x } } }",
          "enum E { A, B(i32) }",
          "let o: Option<i32> = Some(1);",
        ],
        undefined,
        { w: 340, size: 8.5, lh: 22 },
      ),
    ],
    [
      Box("a", 180, 60, 240, 34, "Python → Rust: типы, функции, …", "b", {
        size: 10.5,
      }),
    ],
  ],
});
