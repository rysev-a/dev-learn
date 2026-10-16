import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, rs, slot } from "./rs.tsx";
import type { SceneItem } from "./dsl.ts";
import type { Extra } from "./dsl.ts";

/* Глава 19 книги «Изучаем Rust»: трейты и обобщённые типы. */

const py = (id: string, x: number, y: number, lines: string[], hl: number[], extra: Extra = {}): SceneItem => ({
  t: "code",
  id,
  x,
  y,
  lines,
  hl,
  size: 9.5,
  lh: 13,
  w: 200,
  ...extra,
});

// 1. Утка и контракт
export const V01 = scene({
  labels: ["Питон: утка", "Раст: контракт", "Когда ошибка"],
  caption: [
    "В питоне годится любой объект с нужным методом, но проверка идёт при запуске строки",
    "В расте требование записано в сигнатуре: подойдёт любой T, реализующий Shape — и это проверяет компилятор",
    "Ошибка питона всплывает на пользователе, ошибка раста — при сборке",
  ],
  frames: [
    [
      py(
        "c",
        20,
        40,
        [
          "def total(shapes):",
          "    return sum(s.area() for s in shapes)",
          "",
          "total([Circle(1), 42])  # 💥 при запуске",
        ],
        [3],
        { w: 320, size: 9.5, lh: 16, bad: [3] },
      ),
    ],
    [
      rs(
        "c",
        14,
        40,
        [
          "trait Shape { fn area(&self) -> f64; }",
          "",
          "fn total<T: Shape>(v: &[T]) -> f64 {",
          "    v.iter().map(|s| s.area()).sum()",
          "}",
        ],
        [2],
        { w: 340, size: 9.5, lh: 16 },
      ),
    ],
    [
      Box("p", 100, 50, 140, 28, "питон: во время работы", "r", { size: 9 }),
      Box("r", 100, 100, 140, 28, "раст: при сборке", "g", { size: 9 }),
      {
        t: "bar",
        id: "b1",
        x: 280,
        y: 70,
        w: 24,
        hh: 40,
        max: 100,
        c: "r",
        text: "",
      },
      {
        t: "bar",
        id: "b2",
        x: 330,
        y: 70,
        w: 24,
        hh: 8,
        max: 100,
        c: "g",
        text: "",
      },
      Tx("n", 180, 140, "чем раньше ошибка — тем дешевле", { size: 9.5 }),
    ],
  ],
});

// 2. Обобщения
export const V02 = scene({
  labels: ["Параметр типа", "Без ограничения", "С трейтом"],
  caption: [
    "Функция пишется один раз: T — любое имя типа, которое подставит вызывающий",
    "Но сравнить два T нельзя: не у каждого типа есть «больше» — компилятор не пропустит",
    "Ограничение T: PartialOrd говорит, что подойдут только сравнимые типы — и ошибка исчезает",
  ],
  frames: [
    [
      rs(
        "c",
        14,
        40,
        ["fn largest<T>(v: &[T]) -> &T {", "    // ...", "}"],
        [0],
        { w: 300, size: 10.5, lh: 17 },
      ),
      Box("a", 95, 120, 104, 24, "largest(&[1, 5, 3])", "b", { size: 8 }),
      Box("b", 245, 120, 116, 24, 'largest(&["a", "z"])', "b", { size: 8 }),
    ],
    [
      rs(
        "c",
        14,
        30,
        [
          "fn largest<T>(v: &[T]) -> &T {",
          "    let mut m = &v[0];",
          "    for x in v { if x > m { m = x; } }",
          "    m",
          "}",
        ],
        [2],
        { w: 340, size: 9.5, lh: 16, bad: [2] },
      ),
      Box(
        "e",
        180,
        128,
        330,
        30,
        "error[E0369]: binary operation `>` cannot be\napplied to type `&T`",
        "r",
        { size: 8 },
      ),
    ],
    [
      rs(
        "c",
        14,
        40,
        [
          "fn largest<T: PartialOrd>(v: &[T]) -> &T {",
          "    let mut m = &v[0];",
          "    for x in v { if x > m { m = x; } }",
          "    m",
          "}",
        ],
        [0],
        { w: 340, size: 9, lh: 16 },
      ),
      Tx("n", 180, 140, "теперь годятся i32, f64, &str, String…", {
        size: 9.5,
        c: "g",
      }),
    ],
  ],
});

// 3. Трейт и impl
export const V03 = scene({
  labels: ["trait", "impl для типов", "Правило сироты"],
  caption: [
    "Трейт — набор методов, которые тип обязуется предоставить: ближайший аналог — ABC или Protocol питона",
    "Реализация пишется отдельно от типа: Circle и Rect реализуют один трейт, и даже чужому типу можно добавить свой трейт",
    "Нельзя реализовать чужой трейт для чужого типа: две библиотеки не смогут договориться",
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
          "    fn name(&self) -> String;",
          "}",
        ],
        undefined,
        { w: 280, size: 10.5, lh: 18 },
      ),
    ],
    [
      Box("t", 180, 36, 130, 26, "trait Shape", "y", { size: 10 }),
      Box("c", 90, 112, 100, 28, "impl for Circle", "b", { size: 9 }),
      Box("r", 270, 112, 100, 28, "impl for Rect", "b", { size: 9 }),
      arrow("e1", 120, 98, 160, 50, "g"),
      arrow("e2", 240, 98, 200, 50, "g"),
    ],
    [
      Box("a", 80, 56, 110, 28, "крейт A: impl\nDisplay for Vec", "r", {
        size: 8,
      }),
      Box("b", 280, 56, 110, 28, "крейт B: impl\nDisplay for Vec", "r", {
        size: 8,
      }),
      Tx("x", 180, 56, "✕", { size: 18, c: "r" }),
      Tx("n", 180, 116, "нужно владеть хотя бы трейтом или типом", {
        size: 9.5,
      }),
    ],
  ],
});

// 4. Методы по умолчанию
export const V04 = scene({
  labels: ["Обязательный и готовый", "Переопределение", "Супертрейт"],
  caption: [
    "Обязательный метод пишет тип, а методы с телом в трейте приходят бесплатно — так устроен Iterator",
    "Любой готовый метод можно переопределить, если у типа есть более быстрый способ",
    "Трейт может требовать другого: чтобы быть Shape, тип обязан реализовать Debug — но данных у трейта нет",
  ],
  frames: [
    [
      rs(
        "c",
        14,
        36,
        [
          "trait Shape {",
          "    fn area(&self) -> f64;       // обязателен",
          "    fn describe(&self) -> String {",
          '        format!("площадь {:.1}", self.area())',
          "    }",
          "}",
        ],
        [1, 2],
        { w: 340, size: 9, lh: 16 },
      ),
    ],
    [
      rs(
        "c",
        14,
        40,
        [
          "impl Shape for Square {",
          "    fn area(&self) -> f64 { self.0 * self.0 }",
          "    fn describe(&self) -> String {",
          '        "квадрат".into()   // своё"',
          "    }",
          "}",
        ],
        [2, 3],
        { w: 340, size: 9, lh: 16 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "trait Shape: Debug {",
          "    fn area(&self) -> f64;",
          "}",
          "// поля и наследование данных — нет",
        ],
        [0],
        { w: 300, size: 10.5, lh: 18 },
      ),
    ],
  ],
});

// 5. Стандартные трейты
export const V05 = scene({
  labels: ["Печать и копии", "Равенство и порядок", "Операторы"],
  caption: [
    "Debug и Display печатают, Clone и Copy копируют, Default строит значение по умолчанию",
    "PartialEq и Eq — равенство, PartialOrd и Ord — порядок, Hash — хеш: большинство берётся через derive",
    "Оператор — это метод трейта: a + b превращается в Add::add(a, b), поэтому комплексные числа пишутся как формулы",
  ],
  frames: [
    [
      ...["Debug", "Display", "Clone", "Copy", "Default"].map((t, i) =>
        Box(`c${i}`, 60 + i * 60, 70, 54, 28, t, i < 2 ? "y" : "b", {
          size: 8.5,
        }),
      ),
      Tx("n", 180, 118, "{:?}   {}   .clone()   =   Default::default()", {
        size: 9,
        mono: true,
      }),
    ],
    [
      ...["PartialEq", "Eq", "PartialOrd", "Ord", "Hash"].map((t, i) =>
        Box(`c${i}`, 56 + i * 62, 70, 58, 28, t, "b", { size: 7.5 }),
      ),
      Tx("n", 180, 118, "#[derive(PartialEq, Eq, PartialOrd, Ord, Hash)]", {
        size: 8.5,
        mono: true,
      }),
    ],
    [
      rs(
        "c",
        14,
        30,
        [
          "impl Add for Complex {",
          "    type Output = Complex;",
          "    fn add(self, o: Complex) -> Complex {",
          "        Complex::new(self.re + o.re, self.im + o.im)",
          "    }",
          "}",
          "let z = a + b;   // Add::add(a, b)",
        ],
        [6],
        { w: 350, size: 8.5, lh: 15 },
      ),
    ],
  ],
});

// 6. Мономорфизация
export const V06 = scene({
  labels: ["Один исходник", "Копия на тип", "Цена"],
  caption: [
    "Обобщённая функция написана один раз — но это шаблон, а не готовый код",
    "Для каждого типа, с которым вызвали, компилятор создаёт отдельную копию, оптимизированную под него, и вызывает её напрямую",
    "Скорость как у ручного копирования; цена — размер программы, нагрузка на кэш команд и время сборки",
  ],
  frames: [
    [
      Box("g", 180, 70, 180, 40, "fn largest<T>(…)", "y", { size: 11 }),
      Tx("n", 180, 118, "один шаблон", { size: 9.5 }),
    ],
    [
      Box("g", 70, 40, 110, 28, "largest<T>", "y", { size: 9.5 }),
      Box("a", 240, 36, 130, 26, "largest::<i32>", "g", { size: 9 }),
      Box("b", 240, 70, 130, 26, "largest::<f64>", "g", { size: 9 }),
      Box("c", 240, 104, 130, 26, "largest::<&str>", "g", { size: 9 }),
      arrow("e1", 126, 46, 174, 38, "g"),
      arrow("e2", 126, 50, 174, 70, "g"),
      arrow("e3", 126, 56, 174, 102, "g"),
    ],
    [
      {
        t: "bar",
        id: "s1",
        x: 90,
        y: 120,
        w: 40,
        hh: 30,
        max: 100,
        c: "b",
        text: "",
      },
      {
        t: "bar",
        id: "s2",
        x: 210,
        y: 120,
        w: 40,
        hh: 80,
        max: 100,
        c: "y",
        text: "",
      },
      Tx("l1", 90, 140, "размер кода", { size: 8.5 }),
      Tx("l2", 210, 140, "размер кода", { size: 8.5 }),
      Tx("a1", 90, 18, "dyn", { size: 9, mono: true }),
      Tx("a2", 210, 18, "дженерики", { size: 9, mono: true }),
      Tx("n", 310, 80, "быстро,\nно больше", { size: 8.5 }),
    ],
  ],
});

// 7. where и impl Trait
export const V07 = scene({
  labels: ["where", "impl Trait в аргументе", "impl Trait в результате"],
  caption: [
    "Когда ограничений много, их выносят в блок where: так читается, и не нужен длинный список в скобках",
    "В аргументе «impl Trait» означает «любой тип с этим трейтом» — тот же мономорфный код, записанный короче",
    "В результате он прячет конкретный тип — например длинный итератор — и обещает только «нечто итерируемое»",
  ],
  frames: [
    [
      rs(
        "c",
        14,
        36,
        [
          "fn show_all<T, U>(a: &[T], b: U)",
          "where",
          "    T: Display + Clone,",
          "    U: Into<String>,",
          "{ ... }",
        ],
        [1, 2, 3],
        { w: 340, size: 9.5, lh: 17 },
      ),
    ],
    [
      rs(
        "c",
        14,
        50,
        [
          "fn print_all(items: &[impl Display]) {",
          '    for i in items { println!("{i}"); }',
          "}",
        ],
        [0],
        { w: 340, size: 9.5, lh: 18 },
      ),
      Tx("n", 180, 130, "= fn print_all<T: Display>(items: &[T])", {
        size: 9,
        mono: true,
      }),
    ],
    [
      rs(
        "c",
        14,
        46,
        [
          "fn evens(limit: u32) -> impl Iterator<Item = u32> {",
          "    (0..limit).filter(|n| n % 2 == 0)",
          "}",
        ],
        [0],
        { w: 350, size: 9, lh: 18 },
      ),
      Tx("n", 180, 128, "тип — Filter<Range<u32>, closure> — спрятан", {
        size: 9,
        mono: true,
      }),
    ],
  ],
});

// 8. dyn Trait
export const V08 = scene({
  labels: ["Разнородный список", "Толстый указатель", "Таблица методов"],
  caption: [
    "Список Vec<Box<dyn Shape>> хранит круги и прямоугольники вместе: тип известен только во время работы",
    "Box<dyn Shape> — два слова на стеке: адрес данных и адрес таблицы виртуальных методов (16 байт)",
    "В таблице: drop, размер, выравнивание и указатели на методы; вызов — косвенный переход, как по указателю на функцию в C",
  ],
  frames: [
    [
      Tx("t", 180, 20, "Vec<Box<dyn Shape>>", { size: 9.5, mono: true }),
      Box("a", 70, 70, 80, 36, "Circle\nr = 1.0", "g", { size: 9 }),
      Box("b", 180, 70, 80, 36, "Rect\n2 × 3", "b", { size: 9 }),
      Box("c", 290, 70, 80, 36, "Square\n4", "y", { size: 9 }),
      Tx("n", 180, 126, "в куче: разные типы и размеры", { size: 9 }),
    ],
    [
      slot("p", 70, 70, "Box<dyn Shape>", "data · vtable", "g", {
        w: 110,
        h: 44,
        size: 8,
      }),
      Box("d", 270, 44, 100, 28, "данные: Circle", "y", { size: 9 }),
      Box("v", 270, 100, 100, 28, "vtable Circle", "b", { size: 9 }),
      arrow("e1", 126, 64, 220, 46, "g"),
      arrow("e2", 126, 76, 220, 98, "b"),
      Tx("n", 70, 112, "16 байт", { size: 9 }),
    ],
    [
      Box("v0", 130, 30, 200, 22, "drop_in_place", "m", { size: 8.5 }),
      Box("v1", 130, 54, 200, 22, "size = 8", "m", { size: 8.5 }),
      Box("v2", 130, 78, 200, 22, "align = 8", "m", { size: 8.5 }),
      Box("v3", 130, 102, 200, 22, "area → Circle::area", "g", { size: 8.5 }),
      Box("v4", 130, 126, 200, 22, "name → Circle::name", "g", { size: 8.5 }),
      arrow("e", 245, 102, 280, 102, "g"),
      Tx("n", 300, 102, "call [vtable+24]", { size: 8, mono: true }),
    ],
  ],
});

// 9. Статика или динамика
export const V09 = scene({
  labels: ["Прямой вызов", "Через таблицу", "Что выбрать"],
  caption: [
    "Обобщения: вызов известен при сборке — прямой переход, который можно встроить и оптимизировать",
    "Трейт-объект: адрес метода читается из таблицы во время работы — косвенный переход, встроить нельзя",
    "Начинайте с обобщений, берите dyn, когда нужна разнородность или плагины; объектом можно сделать не любой трейт",
  ],
  frames: [
    [
      Box("c", 60, 70, 70, 28, "вызов", "b", { size: 10 }),
      arrow("e", 96, 70, 144, 70, "g"),
      Box("f", 190, 70, 80, 28, "area_circle", "g", { size: 9 }),
      Tx("n", 180, 120, "call area_circle  (может стать inline)", {
        size: 9,
        mono: true,
      }),
    ],
    [
      Box("c", 50, 70, 60, 28, "вызов", "b", { size: 10 }),
      arrow("e1", 80, 70, 114, 70, "g"),
      Box("v", 150, 70, 60, 28, "vtable", "y", { size: 9 }),
      arrow("e2", 180, 70, 224, 70, "g"),
      Box("f", 270, 70, 80, 28, "Circle::area", "g", { size: 9 }),
      Tx("n", 180, 120, "call [vtable+24]  — косвенный", {
        size: 9,
        mono: true,
      }),
    ],
    [
      Box("a", 90, 44, 130, 24, "обобщения: скорость", "g", { size: 9 }),
      Box("b", 90, 78, 130, 24, "dyn: разнородность", "y", { size: 9 }),
      Box("c", 90, 112, 130, 24, "dyn: плагины", "y", { size: 9 }),
      Box(
        "d",
        270,
        78,
        130,
        50,
        "нельзя в dyn:\nSelf по значению,\nобобщённые методы",
        "r",
        { size: 8 },
      ),
    ],
  ],
});

// 10. Ассоциированные типы
export const V10 = scene({
  labels: ["Iterator", "Свой итератор", "Константы в трейте"],
  caption: [
    "Ассоциированный тип Item объявлен внутри трейта: у каждой реализации он один, и не нужен лишний параметр в сигнатурах",
    "Для структуры Fib достаточно метода next — map, filter, take и sum приходят готовыми",
    "В трейте можно объявить и константу: у каждого типа свой SIDES, известный при сборке и не занимающий места в данных",
  ],
  frames: [
    [
      rs(
        "c",
        14,
        40,
        [
          "trait Iterator {",
          "    type Item;",
          "    fn next(&mut self) -> Option<Self::Item>;",
          "}",
        ],
        [1],
        { w: 340, size: 10, lh: 18 },
      ),
    ],
    [
      rs(
        "c",
        14,
        26,
        [
          "struct Fib { a: u64, b: u64 }",
          "impl Iterator for Fib {",
          "    type Item = u64;",
          "    fn next(&mut self) -> Option<u64> {",
          "        let r = self.a;",
          "        (self.a, self.b) = (self.b, self.a + self.b);",
          "        Some(r)",
          "    }",
          "}",
        ],
        [2, 3],
        { w: 350, size: 8.5, lh: 14 },
      ),
    ],
    [
      rs(
        "c",
        14,
        40,
        [
          "trait Polygon {",
          "    const SIDES: u32;",
          "}",
          "impl Polygon for Triangle { const SIDES: u32 = 3; }",
          "// Triangle::SIDES == 3",
        ],
        [1],
        { w: 350, size: 9, lh: 17 },
      ),
    ],
  ],
});

// 11. Обобщённые структуры
export const V11 = scene({
  labels: ["Stack<T>", "Условный impl", "Общая реализация"],
  caption: [
    "Stack<i32> и Stack<String> — разные типы с разной раскладкой: компилятор подставляет T и считает размер заново",
    "Блок impl<T: Display> добавляет методы только для тех T, которые умеют печататься",
    "«Для всякого T: Display реализуй ToString» — одна общая реализация и метод to_string у чисел, строк и ваших типов",
  ],
  frames: [
    [
      rs(
        "c",
        14,
        30,
        [
          "struct Stack<T> { items: Vec<T> }",
          "impl<T> Stack<T> {",
          "    fn push(&mut self, x: T) { self.items.push(x) }",
          "}",
        ],
        [0],
        { w: 350, size: 9, lh: 16 },
      ),
      Box("a", 110, 128, 120, 24, "Stack<i32>: 24 байта", "g", { size: 8.5 }),
      Box("b", 260, 128, 120, 24, "Stack<String>", "b", { size: 8.5 }),
    ],
    [
      rs(
        "c",
        14,
        40,
        [
          "impl<T: Display> Stack<T> {",
          "    fn show(&self) -> String { ... }",
          "}",
          "// Stack<Vec<u8>>::show — нет",
        ],
        [0],
        { w: 340, size: 9.5, lh: 18 },
      ),
    ],
    [
      rs(
        "c",
        14,
        40,
        [
          "impl<T: Display> ToString for T {",
          "    fn to_string(&self) -> String { ... }",
          "}",
        ],
        [0],
        { w: 340, size: 9.5, lh: 18 },
      ),
      Tx(
        "n",
        180,
        118,
        '5.to_string()   "hi".to_string()   point.to_string()',
        { size: 8.5, mono: true },
      ),
    ],
  ],
});

// 12. Преобразования
export const V12 = scene({
  labels: ["From и Into", "TryFrom", "FromStr и parse"],
  caption: [
    "impl From<A> for B даёт бесплатный a.into(); оператор ? использует From, чтобы преобразовать ошибку",
    "TryFrom — то же, но с возможной ошибкой: u8::try_from(300) вернёт Err",
    'FromStr позволяет вызвать "…".parse::<MyType>(); AsRef принимает «всё, что похоже на строку или срез»',
  ],
  frames: [
    [
      Box("a", 60, 70, 70, 28, "ParseIntError", "r", { size: 8 }),
      Box("b", 300, 70, 100, 28, "AppError::Parse", "y", { size: 8.5 }),
      arrow("e", 96, 70, 250, 70, "g"),
      Tx("t", 180, 52, "From::from", { size: 9, mono: true }),
      Tx("n", 180, 110, "a.into()   и   ?", { size: 9, mono: true }),
    ],
    [
      rs(
        "c",
        14,
        50,
        [
          "let a = u8::try_from(200)?;   // Ok(200)",
          "let b = u8::try_from(300);    // Err",
        ],
        [1],
        { w: 350, size: 9.5, lh: 20 },
      ),
    ],
    [
      Box("s", 60, 70, 80, 28, '"10,20"', "b", { size: 9 }),
      arrow("e", 100, 70, 140, 70, "g"),
      Tx("t", 120, 54, ".parse()", { size: 9, mono: true }),
      Box("p", 260, 70, 130, 28, "Point { x: 10, y: 20 }", "g", { size: 8.5 }),
      Tx("n", 180, 118, "impl FromStr for Point", { size: 9, mono: true }),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Три инструмента", "Цена", "Дальше"],
  caption: [
    "Обобщения пишут код один раз, трейты описывают поведение, ограничения связывают их",
    "Мономорфизация: скорость за размер; dyn: разнородность за косвенный вызов",
    "Дальше — замыкания и итераторы: они строятся на этих же трейтах (Fn, FnMut, FnOnce, Iterator)",
  ],
  frames: [
    [
      Box("a", 70, 66, 100, 34, "обобщения\nT", "b", { size: 9.5 }),
      Box("b", 180, 66, 100, 34, "трейты\nповедение", "y", { size: 9.5 }),
      Box("c", 290, 66, 100, 34, "ограничения\nT: Trait", "g", { size: 9.5 }),
    ],
    [
      Box("a", 100, 56, 160, 28, "static: быстро, больше кода", "g", {
        size: 9,
      }),
      Box("b", 100, 96, 160, 28, "dyn: гибко, косвенный вызов", "y", {
        size: 9,
      }),
      Tx("n", 290, 76, "16 байт\nу &dyn", { size: 9, mono: true }),
    ],
    [
      rs(
        "c",
        40,
        50,
        [
          "let add = |a, b| a + b;",
          "let evens: Vec<_> = v.iter()",
          "    .filter(|x| *x % 2 == 0).collect();",
        ],
        undefined,
        { w: 300, size: 10, lh: 18 },
      ),
      Tx("n", 180, 124, "замыкания и итераторы", { size: 9.5, c: "g" }),
    ],
  ],
});
