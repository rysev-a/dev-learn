// Слайды для «Изучаем Rust», глава 6 — «Трейты и обобщённые типы».
// Тот же дизайн-код, что и в главах 1–5: палитра, IBM Plex Mono / Inter,
// рубрика + номер, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

const RS_KW = new Set([
  "fn", "let", "mut", "pub", "struct", "enum", "impl", "match", "if", "else",
  "for", "while", "loop", "return", "use", "mod", "crate", "self", "Self",
  "move", "ref", "const", "static", "type", "where", "async", "await",
  "unsafe", "trait", "dyn", "in", "as", "break", "continue",
]);
const RS_TY = new Set([
  "i8", "i16", "i32", "i64", "i128", "isize", "u8", "u16", "u32", "u64",
  "u128", "usize", "f32", "f64", "bool", "char", "str", "String", "Vec",
  "Option", "Result", "Box", "Rc", "Arc", "RefCell", "HashMap",
]);

// Крошечный токенизатор Rust: комментарии, строки, времена жизни, ключевые
// слова, типы, макросы, числа, вызовы функций. Достаточно для слайдов.
function rsSpan(src) {
  const out = [];
  const re =
    /(\/\/[^\n]*)|("(?:[^"\\]|\\.)*")|('(\w+)\b)|(\b\d[\d_]*(?:\.\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*!)|([A-Za-z_][A-Za-z0-9_]*)|(\s+|.)/g;
  let m;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, life, num, mac, word] = m;
    if (com) out.push(<span key={out.length} className="rs-com">{tok}</span>);
    else if (str) out.push(<span key={out.length} className="rs-str">{tok}</span>);
    else if (life) out.push(<span key={out.length} className="rs-life">{tok}</span>);
    else if (num) out.push(<span key={out.length} className="rs-num">{tok}</span>);
    else if (mac) out.push(<span key={out.length} className="rs-mac">{tok}</span>);
    else if (word) {
      let cls = "";
      if (RS_KW.has(word)) cls = "rs-kw";
      else if (RS_TY.has(word)) cls = "rs-ty";
      else if (/^[A-Z]/.test(word)) cls = "rs-ty";
      else if (src[re.lastIndex] === "(") cls = "rs-fn";
      out.push(
        cls ? (
          <span key={out.length} className={cls}>{word}</span>
        ) : (
          <span key={out.length}>{word}</span>
        ),
      );
    } else out.push(<span key={out.length}>{tok}</span>);
  }
  return out;
}

function PyCode({ children }) {
  return <pre className="rs-code">{rsSpan(children)}</pre>;
}

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>ИЗУЧАЕМ RUST / ЯЗЫК ГЛУБЖЕ / ГЛАВА 6</span>
      <span>{String(n).padStart(2, "0")} / 13</span>
    </div>
  );
}

function Slide({ n, title, sub, main, children }) {
  return (
    <div className="slide">
      <Rubric n={n} />
      <h3 className="s-title">{title}</h3>
      {sub && <p className="s-sub">{sub}</p>}
      <div className="s-divider" />
      <div className="s-body">{children}</div>
      {main && (
        <div className="s-main">
          <span className="s-main-label">ГЛАВНОЕ</span>
          <span className="s-main-text">{main}</span>
        </div>
      )}
    </div>
  );
}

function Node({ mono, title, sub, kind }) {
  return (
    <div className={`s-node ${kind || ""}`}>
      <span className={mono ? "s-node-mono" : "s-node-title"}>{title}</span>
      {sub && <span className="s-node-sub">{sub}</span>}
    </div>
  );
}

function Cmd({ children }) {
  return (
    <div className="s-cmd">
      <pre>{children}</pre>
    </div>
  );
}

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Один код — много типов"}
      sub={"Глава 6 · Язык глубже"}
      main={"Обобщения пишут код один раз для многих типов, трейты говорят, что тип умеет."}
    >
      <div className="s-grid2">
        {[["<T>", "Обобщения", "Параметры типов"], ["trait", "Контракт", "Набор методов"], ["impl Trait", "Ограничения", "Что нужно от типа"], ["dyn Trait", "Динамика", "Разнородные коллекции"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Обобщённая функция"}
      sub={"Параметр типа и ограничение"}
      main={"T: PartialOrd + Copy — «любой тип, который можно сравнивать и копировать»."}
    >
      <PyCode>{`fn largest<T: PartialOrd + Copy>(items: &[T]) -> T {
    let mut best = items[0];
    for &x in items {
        if x > best {
            best = x;
        }
    }
    best
}

fn main() {
    println!("{}", largest(&[3, 9, 2]));
    println!("{}", largest(&['a', 'z', 'k']));
    println!("{}", largest(&[1.5, 0.2]));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"9\nz\n1.5"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Обобщённая структура"}
      sub={"Point<T>"}
      main={"impl<T> — для всех типов; impl Point<f64> — только для дробных."}
    >
      <PyCode>{`struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

impl Point<f64> {
    fn dist(&self) -> f64 {
        (self.x * self.x + self.y * self.y).sqrt()
    }
}

fn main() {
    let a = Point { x: 3, y: 4 };
    let b = Point { x: 3.0, y: 4.0 };
    println!("{} {}", a.x(), b.dist());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3 5"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Трейт — контракт"}
      sub={"Метод для разных типов"}
      main={"Любой тип может реализовать трейт — и вызывать метод одинаково."}
    >
      <PyCode>{`trait Summary {
    fn summarize(&self) -> String;
}

struct Post {
    title: String,
    likes: u32,
}
struct Tweet {
    text: String,
}

impl Summary for Post {
    fn summarize(&self) -> String {
        format!("{} ({} likes)", self.title, self.likes)
    }
}
impl Summary for Tweet {
    fn summarize(&self) -> String {
        format!("tweet: {}", self.text)
    }
}

fn main() {
    let p = Post { title: "Rust".to_string(), likes: 42 };
    let t = Tweet { text: "hi".to_string() };
    println!("{}", p.summarize());
    println!("{}", t.summarize());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Rust (42 likes)\ntweet: hi"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Методы по умолчанию"}
      sub={"Реализовать нужно только обязательное"}
      main={"Метод по умолчанию вызывает другие методы трейта; тип может его переопределить."}
    >
      <PyCode>{`trait Greeter {
    fn name(&self) -> String;
    fn greet(&self) -> String {
        format!("Hello, {}!", self.name())
    }
}

struct En;
struct Ru;

impl Greeter for En {
    fn name(&self) -> String {
        "world".to_string()
    }
}
impl Greeter for Ru {
    fn name(&self) -> String {
        "мир".to_string()
    }
    fn greet(&self) -> String {
        format!("Привет, {}!", self.name())
    }
}

fn main() {
    println!("{}", En.greet());
    println!("{}", Ru.greet());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Hello, world!\nПривет, мир!"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Трейты в параметрах"}
      sub={"where и impl Trait"}
      main={"Длинные ограничения выносят в where; короткая форма — impl Trait прямо в типе."}
    >
      <PyCode>{`use std::fmt::Display;

fn show_all<T>(items: &[T]) -> String
where
    T: Display,
{
    items.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(", ")
}

fn print_twice(x: impl Display) {
    println!("{x} {x}");
}

fn main() {
    println!("{}", show_all(&[1, 2, 3]));
    print_twice("hey");
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1, 2, 3\nhey hey"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Возврат impl Trait"}
      sub={"Несколько ограничений"}
      main={"Функция возвращает «что-то с таким трейтом», но всегда один конкретный тип."}
    >
      <PyCode>{`use std::fmt::{Debug, Display};

fn make_adder(n: i32) -> impl Fn(i32) -> i32 {
    move |x| x + n
}

fn describe<T: Debug + Display>(x: T) -> String {
    format!("{x} / {x:?}")
}

fn main() {
    let add5 = make_adder(5);
    println!("{}", add5(10));
    println!("{}", describe("hi"));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"15\nhi / \"hi\""}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Стандартные трейты и derive"}
      sub={"Одна строка — готовая реализация"}
      main={"Debug, Clone, PartialEq, Default и другие компилятор выводит сам."}
    >
      <PyCode>{`#[derive(Debug, Clone, PartialEq, Default)]
struct Config {
    name: String,
    retries: u32,
}

fn main() {
    let a = Config::default();
    let mut b = a.clone();
    b.retries = 3;
    println!("{:?} {}", a, a == b);
    println!("{:?}", b);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Config { name: \"\", retries: 0 } false\nConfig { name: \"\", retries: 3 }"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Display и операторы"}
      sub={"Операторы — это трейты"}
      main={"Сложение — трейт Add; печать для людей — трейт Display."}
    >
      <PyCode>{`use std::fmt;
use std::ops::Add;

#[derive(Debug, Clone, Copy)]
struct V2 {
    x: i32,
    y: i32,
}

impl Add for V2 {
    type Output = V2;
    fn add(self, o: V2) -> V2 {
        V2 { x: self.x + o.x, y: self.y + o.y }
    }
}

impl fmt::Display for V2 {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

fn main() {
    let c = V2 { x: 1, y: 2 } + V2 { x: 10, y: 20 };
    println!("{}", c);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(11, 22)"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Трейт-объекты"}
      sub={"Разные типы в одной коллекции"}
      main={"Box<dyn Shape>: метод выбирается во время работы по таблице методов."}
    >
      <PyCode>{`trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> &str;
}

struct Sq(f64);
struct Circ(f64);

impl Shape for Sq {
    fn area(&self) -> f64 {
        self.0 * self.0
    }
    fn name(&self) -> &str {
        "square"
    }
}
impl Shape for Circ {
    fn area(&self) -> f64 {
        3.14159 * self.0 * self.0
    }
    fn name(&self) -> &str {
        "circle"
    }
}

fn main() {
    let shapes: Vec<Box<dyn Shape>> = vec![Box::new(Sq(2.0)), Box::new(Circ(1.0))];
    for s in &shapes {
        println!("{} {:.2}", s.name(), s.area());
    }
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"square 4.00\ncircle 3.14"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Мономорфизация"}
      sub={"Цена динамики"}
      main={"Обобщения разворачиваются в код под каждый тип; ссылка на dyn — два слова вместо одного."}
    >
      <PyCode>{`use std::mem::size_of;

trait T {
    fn f(&self) -> i32;
}
struct A(i32);
impl T for A {
    fn f(&self) -> i32 {
        self.0
    }
}

fn main() {
    println!("{}", size_of::<&A>());
    println!("{}", size_of::<&dyn T>());
    println!("{}", size_of::<Box<dyn T>>());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"8\n16\n16"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Связанные типы и правило сирот"}
      sub={"Итератор своими руками"}
      main={"Реализовать можно только свой трейт или для своего типа — иначе библиотеки конфликтовали бы."}
    >
      <PyCode>{`struct Countdown(u32);

impl Iterator for Countdown {
    type Item = u32;
    fn next(&mut self) -> Option<u32> {
        if self.0 == 0 {
            None
        } else {
            self.0 -= 1;
            Some(self.0 + 1)
        }
    }
}

fn main() {
    let v: Vec<u32> = Countdown(3).collect();
    println!("{:?}", v);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[3, 2, 1]"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Обобщения + трейты = гибкость без накладных расходов; dyn — когда нужна разнородность."}
    >
      <div className="s-grid2">
        {[["<T: Trait>", "Обобщения", "Мономорфизация"], ["derive", "Стандартные трейты", "Debug, Clone, Eq…"], ["Add · Display", "Операторы", "Тоже трейты"], ["Box<dyn>", "Динамика", "Таблица методов"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_R6 = {
  "10:6": [
    S01,
    S02,
    S03,
    S04,
    S05,
    S06,
    S07,
    S08,
    S09,
    S10,
    S11,
    S12,
    S13,
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R6).
export const SLIDE_TITLES_R6 = {
  "10:6": [
    "Трейты и обобщения",
    "Обобщённая функция",
    "Обобщённая структура",
    "Трейт",
    "Методы по умолчанию",
    "Трейт-параметры",
    "Возврат impl Trait",
    "Derive",
    "Display и Add",
    "dyn Trait",
    "Мономорфизация",
    "Связанные типы",
    "Итоги",
  ],
};
