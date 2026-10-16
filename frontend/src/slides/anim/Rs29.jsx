import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow, rs, slot } from "./rs.tsx";

/* Глава 29 книги «Изучаем Rust»: каталог трейтов стандартной библиотеки. */

const pair = (a, b, ca = "m", cb = "g", y = 60) => [
  Box("pa", 90, y, 130, 34, a, ca, { size: 10 }),
  Box("pb", 270, y, 130, 34, b, cb, { size: 10 }),
];
const row = (pre, items, c = "g", y = 66, size = 10.5) =>
  items.map((t, i) =>
    Box(`${pre}${i}`, 50 + i * 86, y, 76, 30, t, c, { size }),
  );

// 1. Введение
export const V01 = scene({
  labels: ["Словарь языка", "Группы", "derive или вручную"],
  caption: [
    "Ограничения на параметры функции — описание того, что ей нужно от типа",
    "Копирование, сравнение, преобразования, разыменование, итерация, замыкания, ошибки, маркеры",
    "Что обещает трейт, когда его выводят derive, а когда пишут руками",
  ],
  frames: [
    [
      rs("c", 20, 50, ["fn f<T: Clone + Debug + Ord>(x: T)"], [0], {
        w: 340,
        size: 10.5,
        lh: 28,
      }),
    ],
    [...row("a", ["Clone", "Eq / Ord", "From", "Iterator"], "b")],
    [...pair("#[derive(…)]", "impl … for …", "g", "y")],
  ],
});

// 2. Копирование
export const V02 = scene({
  labels: ["Clone", "Copy", "Drop"],
  caption: [
    "Clone — явная копия: вызов виден и может быть дорогим",
    "Copy — копирование тривиально; присваивание не перемещает; только если все поля Copy и нет Drop",
    "Drop — освобождение при уничтожении значения: автоматический, вручную не вызывается (только drop(x))",
  ],
  frames: [
    [
      rs("c", 20, 50, ["let b = a.clone();"], [0], {
        w: 340,
        size: 12,
        lh: 28,
      }),
    ],
    [...pair("i32, char, bool\nCopy", "String, Vec\nне Copy", "g", "r")],
    [
      rs(
        "c",
        20,
        50,
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

// 3. Сравнение
export const V03 = scene({
  labels: ["PartialEq и Eq", "PartialOrd и Ord", "Hash"],
  caption: [
    "PartialEq: == и !=; Eq — равенство полное (x == x): у f64 его нет из-за NaN",
    "PartialOrd: порядок может быть неопределён; Ord — полный: нужен для sort, BTreeMap, BinaryHeap",
    "Hash согласован с Eq: равные значения дают одинаковый хеш — иначе HashMap потеряет ключи",
  ],
  frames: [
    [...pair("f64\nPartialEq", "i32\nEq", "y", "g")],
    [...pair("f64\nPartialOrd", "i32, String\nOrd", "y", "g")],
    [
      rs(
        "c",
        20,
        50,
        [
          "#[derive(PartialEq, Eq, PartialOrd, Ord, Hash)]",
          "struct Key(u32, String);",
        ],
        [0],
        { w: 340, size: 8.5, lh: 28 },
      ),
    ],
  ],
});

// 4. Default
export const V04 = scene({
  labels: ["Default", "derive", "..Default::default()"],
  caption: [
    "Default::default(): 0, пустая строка, пустой вектор, false — разумное значение типа",
    "#[derive(Default)], если все поля Default; вручную — для настроек с особыми значениями",
    "Config { port: 80, ..Default::default() } — остальные поля стандартные; unwrap_or_default, or_default",
  ],
  frames: [
    [...row("a", ["0", '""', "vec![]", "false"], "g", 66, 11)],
    [
      rs(
        "c",
        20,
        50,
        ["#[derive(Default)]", "struct Config { port: u16, name: String }"],
        [0],
        { w: 340, size: 10, lh: 28 },
      ),
    ],
    [
      rs("c", 20, 50, ["Config { port: 80, ..Default::default() }"], [0], {
        w: 340,
        size: 9.5,
        lh: 28,
      }),
    ],
  ],
});

// 5. Преобразования
export const V05 = scene({
  labels: ["From и Into", "TryFrom, AsRef, Borrow", "ToOwned и Cow"],
  caption: [
    "From<A> for B — безошибочное преобразование; Into получается само",
    "TryFrom — с ошибкой; AsRef и AsMut — «как ссылка на другой тип»; Borrow — согласован с Hash и Eq",
    "ToOwned создаёт владеющую версию; Cow откладывает копирование до первой необходимости",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ["impl From<u8> for Level { … }", "let l: Level = 3u8.into();"],
        [1],
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
    [...row("a", ["TryFrom", "AsRef", "Borrow"], "b", 66, 10)],
    [
      rs(
        "c",
        20,
        50,
        [
          "fn f(s: &str) -> Cow<str> {",
          "    if ok { Cow::Borrowed(s) } else { Cow::Owned(fix(s)) }",
          "}",
        ],
        undefined,
        { w: 340, size: 8, lh: 26 },
      ),
    ],
  ],
});

// 6. Строка ↔ значение
export const V06 = scene({
  labels: ["FromStr", "ToString", "Остальные форматы"],
  caption: [
    "FromStr даёт s.parse::<T>(); ошибка — ассоциированный тип Err",
    "ToString реализован автоматически для любого типа с Display",
    "LowerHex, UpperHex, Binary, Octal, LowerExp, Pointer — для {:x}, {:X}, {:b}, {:o}, {:e}, {:p}",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ["impl FromStr for Point { … }", 'let p: Point = "1,2".parse()?;'],
        [1],
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
    [...pair("Display", "to_string()", "b", "g")],
    [...row("a", ["{:x}", "{:b}", "{:o}", "{:e}"], "b", 66, 12)],
  ],
});

// 7. Deref
export const V07 = scene({
  labels: ["Deref", "Приведение", "Index"],
  caption: [
    "Deref превращает тип в «умную ссылку»: Box<T>, Rc<T>, String → str, Vec<T> → [T]",
    "Компилятор сам применяет Deref там, где нужна другая ссылка: &String → &str, &Vec<T> → &[T]",
    "Index и IndexMut — квадратные скобки; не используйте Deref для имитации наследования",
  ],
  frames: [
    [...pair("String", "str", "b", "g"), arrow("e", 156, 60, 204, 60, "g")],
    [
      rs(
        "c",
        20,
        50,
        ["fn f(s: &str) { }", 'f(&String::from("a"));   // &String → &str'],
        [1],
        { w: 340, size: 10, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["impl Index<usize> for Row { … }", "let x = row[2];"],
        undefined,
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
  ],
});

// 8. Итерация
export const V08 = scene({
  labels: ["Iterator", "IntoIterator, FromIterator", "Родственники"],
  caption: [
    "Iterator: один метод next() даёт десятки готовых",
    "IntoIterator — цикл for по типу; FromIterator — collect; Extend — добавить в готовую коллекцию",
    "DoubleEndedIterator (rev), ExactSizeIterator (len), Sum и Product для своих типов",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "impl Iterator for Count {",
          "    fn next(&mut self) -> Option<…> { … }",
          "}",
        ],
        [1],
        { w: 340, size: 10, lh: 26 },
      ),
    ],
    [...row("a", ["for x in c", "collect()", "extend()"], "b", 66, 10)],
    [...row("a", ["rev", "len", "sum", "product"], "g", 66, 11)],
  ],
});

// 9. Замыкания
export const V09 = scene({
  labels: ["FnOnce", "FnMut", "Fn"],
  caption: [
    "FnOnce — можно вызвать один раз, забирает захваченное",
    "FnMut — вызывается много раз и меняет состояние",
    "Fn — много раз, ничего не меняет; в параметре пишут самый свободный подходящий; Box<dyn Fn> — для хранения",
  ],
  frames: [
    [Box("a", 180, 66, 200, 40, "FnOnce\nзабирает", "r", { size: 11.5 })],
    [
      Box("a", 180, 66, 200, 40, "FnMut\nменяет состояние", "y", {
        size: 11.5,
      }),
    ],
    [Box("a", 180, 66, 200, 40, "Fn\nтолько читает", "g", { size: 11.5 })],
  ],
});

// 10. Ошибки
export const V10 = scene({
  labels: ["Error", "Box<dyn Error>", "thiserror, anyhow"],
  caption: [
    "Error требует Display и Debug; метод source() — причина, так строят цепочку ошибок",
    "Box<dyn Error + Send + Sync> принимает любую; ? превращает ошибки через From",
    "thiserror — для библиотек; anyhow — для приложений: универсальная ошибка с контекстом",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "impl std::error::Error for MyError {",
          "    fn source(&self) -> Option<&(dyn Error + 'static)> { … }",
          "}",
        ],
        [1],
        { w: 340, size: 8, lh: 26 },
      ),
    ],
    [
      rs("c", 20, 50, ["fn run() -> Result<(), Box<dyn Error>> { … }"], [0], {
        w: 340,
        size: 9.5,
        lh: 28,
      }),
    ],
    [...pair("thiserror\nбиблиотеки", "anyhow\nприложения", "b", "g")],
  ],
});

// 11. Маркеры
export const V11 = scene({
  labels: ["Send и Sync", "Sized", "PhantomData"],
  caption: [
    "Send — можно передать в другой поток; Sync — можно ссылаться из нескольких; автоматические",
    "Rc не Send (счётчик не атомарный); Arc и Mutex — Send + Sync; Sized — размер известен, ?Sized — для срезов",
    "PhantomData<T> — метка типа без хранения значений",
  ],
  frames: [
    [...pair("Rc\nне Send", "Arc, Mutex\nSend + Sync", "r", "g")],
    [...pair("T: Sized", "T: ?Sized\n(str, [T], dyn)", "b", "g")],
    [
      rs("c", 20, 50, ["struct Id<T> { n: u32, _m: PhantomData<T> }"], [0], {
        w: 340,
        size: 9.5,
        lh: 28,
      }),
    ],
  ],
});

// 12. Any
export const V12 = scene({
  labels: ["dyn Any", "downcast_ref", "type_name"],
  caption: [
    "Any — узнать тип значения во время работы программы",
    "downcast_ref::<T>() → Option<&T>: превращает &dyn Any в конкретный тип",
    "TypeId и type_name — сравнение и имя типа; чаще лучше enum или трейт: проверка статическая",
  ],
  frames: [
    [
      rs("c", 20, 50, ["let v: Box<dyn Any> = Box::new(5i32);"], [0], {
        w: 340,
        size: 10.5,
        lh: 28,
      }),
    ],
    [
      rs("c", 20, 50, ["if let Some(n) = v.downcast_ref::<i32>() { }"], [0], {
        w: 340,
        size: 10,
        lh: 28,
      }),
    ],
    [
      rs("c", 20, 50, ['std::any::type_name::<T>()   // "i32"'], undefined, {
        w: 340,
        size: 10.5,
        lh: 28,
      }),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Каталог", "Правило", "Дальше"],
  caption: [
    "Clone, Copy, Eq, Ord, Hash, Default, From, AsRef, Deref, Iterator, Fn, Error, Send, Sync, Any",
    "Выводите derive всё, что можно; вручную — для особого поведения",
    "Следующий раздел — асинхронность: Python asyncio и async Rust с tokio",
  ],
  frames: [
    [...row("a", ["Clone", "Ord", "From", "Iterator"], "g")],
    [...pair("derive", "impl вручную", "g", "y")],
    [Box("a", 180, 60, 250, 34, "async · await · tokio", "b", { size: 12 })],
  ],
});
