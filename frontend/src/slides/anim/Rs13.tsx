import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, rs, slot } from "./rs.tsx";

/* Глава 13 книги «Изучаем Rust»: классы, трейты и перегрузка операторов. */

const pair = (a: string, b: string, ca = "m", cb = "g", y = 60) => [
  Box("pa", 90, y, 130, 34, a, ca, { size: 10 }),
  Box("pb", 270, y, 130, 34, b, cb, { size: 10 }),
];

// 1. Введение
export const V01 = scene({
  labels: ["class", "struct, impl, trait", "Операторы — трейты"],
  caption: [
    "Python: данные и поведение в классе, наследование, методы __dunder__",
    "Rust: struct — данные, impl — методы, trait — общее поведение; наследования нет",
    "Перегрузка операторов — тоже трейты из стандартной библиотеки",
  ],
  frames: [
    [...pair("class", "struct + impl", "m", "g")],
    [
      ...["struct", "impl", "trait"].map((t, i) =>
        Box(`a${i}`, 70 + i * 110, 66, 90, 34, t, "g", { size: 12 }),
      ),
    ],
    [...pair("__add__", "impl Add", "m", "g")],
  ],
});

// 2. Класс
export const V02 = scene({
  labels: ["__init__ → new", "self", "pub"],
  caption: [
    "Конструкторов нет: экземпляр — литерал структуры; по договорённости пишут функцию new",
    "Первый параметр говорит, что делает метод: &self читает, &mut self меняет, self забирает",
    "Всё приватно по умолчанию и видно в модуле; pub открывает доступ — подчёркивания не нужны",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["impl User {", "    fn new(name: &str) -> User { … }", "}"],
        [1],
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      ...["&self", "&mut self", "self"].map((t, i) =>
        Box(`a${i}`, 70 + i * 110, 66, 90, 34, t, ["g", "y", "r"][i], {
          size: 11,
        }),
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "pub struct User {",
          "    pub name: String,",
          "    age: u32,   // приватное",
          "}",
        ],
        [1],
        { w: 340, size: 10.5, lh: 22 },
      ),
    ],
  ],
});

// 3. Свойства
export const V03 = scene({
  labels: ["@property → геттер", "setter", "@classmethod → new"],
  caption: [
    "Атрибута-свойства нет: геттер — обычный метод fn name(&self) -> &str",
    "Сеттер — метод с &mut self: fn set_age(&mut self, v: u32)",
    "@classmethod и @staticmethod → ассоциированные функции без self: User::new(…), Config::default()",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["fn name(&self) -> &str {", "    &self.name", "}"],
        [0],
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        ["fn set_age(&mut self, v: u32) {", "    self.age = v;", "}"],
        [0],
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ['let u = User::new("Аня");', "let c = Config::default();"],
        undefined,
        { w: 340, size: 12, lh: 28 },
      ),
    ],
  ],
});

// 4. Наследование
export const V04 = scene({
  labels: ["Нет наследования", "Композиция", "Без алмаза"],
  caption: [
    "У структур нет наследования полей и методов",
    "Структура содержит другую в поле и вызывает её методы; общее поведение — в трейте",
    "Нет проблемы алмаза и хрупкого базового класса: изменение базы не ломает потомков",
  ],
  frames: [
    [
      Box("a", 90, 40, 100, 28, "Animal", "m", { size: 11 }),
      Box("b", 90, 110, 100, 28, "Dog", "m", { size: 11 }),
      arrow("e", 90, 56, 90, 96, "m"),
      Tx("x", 270, 80, "✕ в Rust", { size: 13, c: "r" }),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "struct Dog {",
          "    animal: Animal,   // внутри",
          "    tricks: u32,",
          "}",
        ],
        [1],
        { w: 340, size: 11, lh: 22 },
      ),
    ],
    [
      Box("a", 180, 60, 250, 34, "хрупкий базовый класс → нет", "g", {
        size: 11,
      }),
    ],
  ],
});

// 5. Трейт
export const V05 = scene({
  labels: ["Объявление", "Реализация", "ABC и Protocol"],
  caption: [
    "trait Shape { fn area(&self) -> f64; } — список обязательных методов",
    "impl Shape for Circle { … } — реализацию пишут отдельно, даже для чужого типа; неполную не пропустит компилятор",
    "Python ABC и Protocol — ближайшие родственники",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        ["trait Shape {", "    fn area(&self) -> f64;", "}"],
        [1],
        { w: 340, size: 11.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "impl Shape for Circle {",
          "    fn area(&self) -> f64 {",
          "        3.14159 * self.r * self.r",
          "    }",
          "}",
        ],
        [0],
        { w: 340, size: 9.5, lh: 20 },
      ),
    ],
    [...pair("ABC / Protocol", "trait", "m", "g")],
  ],
});

// 6. Полиморфизм
export const V06 = scene({
  labels: ["Метод по умолчанию", "impl Trait", "dyn Trait"],
  caption: [
    "Метод с телом в трейте даёт реализацию «бесплатно»; тип может её заменить",
    "Статический полиморфизм: fn f(s: &impl Shape) — своя версия для каждого типа, быстро",
    "Динамический: Vec<Box<dyn Shape>> — разные типы в одном векторе, вызов через таблицу методов",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "trait Shape {",
          "    fn area(&self) -> f64;",
          "    fn describe(&self) -> String {",
          '        format!("{}", self.area())',
          "    }",
          "}",
        ],
        [2, 3],
        { w: 340, size: 8.5, lh: 18 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["fn show(s: &impl Shape) {", '    println!("{}", s.area());', "}"],
        [0],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "let v: Vec<Box<dyn Shape>> = vec![",
          "    Box::new(Circle { r: 1.0 }),",
          "    Box::new(Rect { w: 2.0, h: 3.0 }),",
          "];",
        ],
        [0],
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
  ],
});

// 7. Display и Debug
export const V07 = scene({
  labels: ["__str__ → Display", "__repr__ → Debug", "to_string"],
  caption: [
    "Display — для пользователя: impl fmt::Display, пишется вручную, печать через {}",
    "Debug — для программиста: #[derive(Debug)], печать через {:?}",
    "Реализовали Display — to_string() работает автоматически",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "impl fmt::Display for P {",
          "    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {",
          '        write!(f, "({}, {})", self.x, self.y)',
          "    }",
          "}",
        ],
        [0, 2],
        { w: 340, size: 7.5, lh: 20 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "#[derive(Debug)]",
          "struct P { x: i32, y: i32 }",
          'println!("{:?}", p);   // P { x: 1, y: 2 }',
        ],
        [0],
        { w: 340, size: 10, lh: 24 },
      ),
    ],
    [
      rs("c", 20, 50, ["let s: String = p.to_string();", '// "(1, 2)"'], [0], {
        w: 340,
        size: 12,
        lh: 28,
      }),
    ],
  ],
});

// 8. Сравнение
export const V08 = scene({
  labels: ["__eq__ → PartialEq", "__lt__ → PartialOrd", "Hash и Eq"],
  caption: [
    "#[derive(PartialEq)] — == и != по всем полям",
    "#[derive(PartialOrd)] — порядок лексикографический по полям; особый — partial_cmp вручную",
    "__hash__ → #[derive(Hash)]; Eq и Ord — только для типов, где сравнение определено всегда (у f64 есть NaN)",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ["#[derive(PartialEq)]", "struct P { x: i32, y: i32 }", "p == q"],
        [0],
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "#[derive(PartialOrd, PartialEq)]",
          "struct V(u32, u32);",
          "V(1, 9) < V(2, 0)   // true",
        ],
        [0, 2],
        { w: 340, size: 10, lh: 24 },
      ),
    ],
    [
      Box("a", 90, 60, 130, 34, "f64: PartialOrd\n(есть NaN)", "y", {
        size: 10,
      }),
      Box("b", 270, 60, 130, 34, "i32: Ord", "g", { size: 11 }),
    ],
  ],
});

// 9. Операторы
export const V09 = scene({
  labels: ["__add__ → Add", "Output", "+= и индекс"],
  caption: [
    "impl Add for V { type Output = V; fn add(self, o: V) -> V { … } } — оператор + для своего типа",
    "Тип результата — ассоциированный Output: скалярное произведение двух векторов вернёт число",
    "AddAssign для +=, Index и IndexMut для v[i]; Sub, Mul, Div, Rem, Neg — рядом в std::ops",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        30,
        [
          "impl Add for V {",
          "    type Output = V;",
          "    fn add(self, o: V) -> V {",
          "        V { x: self.x + o.x, y: self.y + o.y }",
          "    }",
          "}",
        ],
        [0, 2],
        { w: 340, size: 8.5, lh: 18 },
      ),
    ],
    [...pair("V + V → V", "V * V → f64", "g", "y")],
    [
      rs(
        "c",
        20,
        40,
        [
          "impl AddAssign for V { … }   // +=",
          "impl Index<usize> for V { … }   // v[i]",
        ],
        undefined,
        { w: 340, size: 9, lh: 26 },
      ),
    ],
  ],
});

// 10. Детали
export const V10 = scene({
  labels: ["Ссылки", "Согласованность", "Newtype"],
  caption: [
    "Операторы реализуют и для ссылок: &a + &b — без лишних копий",
    "Нельзя реализовать чужой трейт для чужого типа: две библиотеки не конфликтуют",
    "Обход — обёртка из одного поля: struct Meters(f64); — шаблон newtype",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ["impl Add<&V> for &V { … }", "let c = &a + &b;   // a и b целы"],
        [1],
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
    [
      Box("a", 90, 60, 130, 34, "чужой трейт\n+ чужой тип ✕", "r", {
        size: 10,
      }),
      Box("b", 270, 60, 130, 34, "свой трейт\nили свой тип ✓", "g", {
        size: 10,
      }),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["struct Wrapper(Vec<String>);", "impl fmt::Display for Wrapper { … }"],
        [0],
        { w: 340, size: 10, lh: 28 },
      ),
    ],
  ],
});

// 11. Итераторы и Drop
export const V11 = scene({
  labels: ["__iter__ → Iterator", "IntoIterator", "__exit__ → Drop"],
  caption: [
    "Реализуйте next() — и тип получит for и десятки готовых методов",
    "IntoIterator позволяет брать тип в for по значению и по ссылке",
    "Контекстный менеджер заменяет Drop: drop вызывается, когда значение выходит из области видимости — блок with не нужен",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "impl Iterator for Count {",
          "    type Item = u32;",
          "    fn next(&mut self) -> Option<u32> { … }",
          "}",
        ],
        [2],
        { w: 340, size: 9, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["for x in my_collection { … }", "for x in &my_collection { … }"],
        undefined,
        { w: 340, size: 11, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "impl Drop for File {",
          "    fn drop(&mut self) { /* закрыть */ }",
          "}",
        ],
        [1],
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
  ],
});

// 12. dataclass
export const V12 = scene({
  labels: ["@dataclass → derive", "Default", "Clone и Copy"],
  caption: [
    "@dataclass → #[derive(Debug, Clone, PartialEq)]: печать, копия и сравнение — в одну строку",
    "#[derive(Default)] и User { age: 30, ..Default::default() } — значения по умолчанию",
    "Clone — глубокая копия; Copy — копирование при присваивании, только для простых данных",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "#[derive(Debug, Clone, PartialEq)]",
          "struct User { name: String, age: u32 }",
        ],
        [0],
        { w: 340, size: 9.5, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "#[derive(Default)]",
          "let u = User { age: 30, ..Default::default() };",
        ],
        [1],
        { w: 340, size: 9, lh: 28 },
      ),
    ],
    [...pair("Clone\nглубокая копия", "Copy\nтолько простое", "b", "g")],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Соответствия", "Дальше"],
  caption: [
    "class → struct + impl; __init__ → new; property → геттер; наследование → композиция и трейты",
    "__str__ → Display; __repr__ → Debug; __eq__ → PartialEq; __add__ → Add; __iter__ → Iterator; __exit__ → Drop",
    "Следующая глава — словари Python, HashMap и множества",
  ],
  frames: [
    [
      ...["struct", "impl", "trait", "derive"].map((t, i) =>
        Box(`a${i}`, 50 + i * 86, 66, 76, 30, t, "g", { size: 10.5 }),
      ),
    ],
    [
      rs(
        "c",
        20,
        30,
        [
          "__str__  → Display",
          "__eq__   → PartialEq",
          "__add__  → Add",
          "__iter__ → Iterator",
        ],
        undefined,
        { w: 340, size: 11, lh: 22 },
      ),
    ],
    [
      Box("a", 180, 60, 250, 34, "dict ↔ HashMap · set ↔ HashSet", "b", {
        size: 10.5,
      }),
    ],
  ],
});
