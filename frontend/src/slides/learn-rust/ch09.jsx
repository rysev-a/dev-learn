// Слайды для «Изучаем Rust», глава 9 — «Модули, тесты и карго».
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
      <span>ИЗУЧАЕМ RUST / ЯЗЫК ГЛУБЖЕ / ГЛАВА 9</span>
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
      title={"Как устроен проект"}
      sub={"Глава 9 · Язык глубже"}
      main={"Модули организуют код, карго собирает и тестирует, тесты живут рядом с кодом."}
    >
      <div className="s-grid2">
        {[["mod · pub · use", "Модули", "Пространства имён"], ["Cargo.toml", "Манифест", "Зависимости и профили"], ["#[test]", "Тесты", "Модульные и интеграционные"], ["///", "Документация", "Примеры — тоже тесты"]].map(([big, t, d]) => (
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
      title={"Крейт, пакет, модуль"}
      sub={"Три уровня организации"}
      main={"Крейт — единица компиляции, пакет — крейты с манифестом, модуль — дерево имён внутри крейта."}
    >
      <div className="s-cols">
        <Node kind="" mono={true} title={"крейт"} sub={"программа или библиотека"} />
        <Node kind="green" mono={true} title={"пакет (Cargo.toml)"} sub={"один или несколько крейтов"} />
        <Node kind="" mono={true} title={"модуль"} sub={"пространство имён внутри крейта"} />
      </div>
      <div className="s-note">{"Корень дерева модулей — src/main.rs (программа) или src/lib.rs (библиотека); остальное подключается объявлением mod."}</div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Видимость"}
      sub={"Всё приватно, пока не написано pub"}
      main={"Публичная структура с приватными полями создаётся только через функции своего модуля."}
    >
      <PyCode>{`mod bank {
    pub struct Account {
        owner: String,
        balance: i64,
    }

    impl Account {
        pub fn open(owner: &str) -> Account {
            Account { owner: owner.to_string(), balance: 0 }
        }
        pub fn deposit(&mut self, n: i64) {
            if n > 0 {
                self.balance += n;
            }
        }
        pub fn balance(&self) -> i64 {
            self.balance
        }
        pub fn owner(&self) -> &str {
            &self.owner
        }
    }
}

fn main() {
    let mut a = bank::Account::open("Ann");
    a.deposit(50);
    a.deposit(-5);
    println!("{} {}", a.owner(), a.balance());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Ann 50"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"use, super, as, pub use"}
      sub={"Пути и псевдонимы"}
      main={"super — родительский модуль; as — псевдоним; pub use открывает короткий путь пользователям."}
    >
      <PyCode>{`mod shapes {
    pub mod circle {
        pub fn area(r: f64) -> f64 {
            super::PI * r * r
        }
    }
    pub mod square {
        pub fn area(s: f64) -> f64 {
            s * s
        }
    }
    const PI: f64 = 3.14;
    pub use self::circle::area as circle_area;
}

use shapes::square::{self, area as sq_area};

fn main() {
    println!("{:.2}", shapes::circle_area(2.0));
    println!("{} {}", sq_area(3.0), square::area(1.5));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"12.56\n9 2.25"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Модули и файлы"}
      sub={"mod config; ищет файл"}
      main={"Сначала объявляете mod в коде — потом файл подтягивается; забытый mod — частая ошибка."}
    >
      <PyCode>{`mod network {
    pub mod server {
        pub fn start() -> String {
            format!("server on {}", crate::config::PORT)
        }
    }
}

mod config {
    pub const PORT: u16 = 8080;
}

fn main() {
    println!("{}", network::server::start());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"server on 8080"}</Cmd>
      <div className="s-note">{"В файлах: src/main.rs — mod network; mod config; · src/network/mod.rs — pub mod server; · src/network/server.rs · src/config.rs"}</div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Cargo.toml и команды"}
      sub={"Манифест и ежедневные команды"}
      main={"cargo run, check, test, fmt, clippy — пять команд на каждый день; Cargo.lock фиксирует версии."}
    >
      <div className="s-cols">
        <Node kind="" mono={true} title={"cargo run · build"} sub={"собрать и запустить / собрать"} />
        <Node kind="green" mono={true} title={"cargo check"} sub={"быстрая проверка типов"} />
        <Node kind="" mono={true} title={"cargo test · fmt · clippy"} sub={"тесты, формат, подсказки"} />
      </div>
      <div className="s-note">{"[package] name, version, edition = \"2021\" · [dependencies] serde = \"1\" · [profile.release] opt-level = 3"}</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Модульные тесты"}
      sub={"#[test] и assert_eq!"}
      main={"Тесты лежат рядом с кодом в модуле tests с #[cfg(test)] и видят даже приватные функции."}
    >
      <PyCode>{`pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn is_even(n: i32) -> bool {
    n % 2 == 0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn adds() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn private_works() {
        assert!(is_even(4));
        assert_ne!(add(1, 1), 3);
    }
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"test tests::adds ... ok\ntest tests::private_works ... ok\ntest result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Виды тестов"}
      sub={"should_panic, Result, интеграционные"}
      main={"Тест может ожидать панику или возвращать Result; интеграционные тесты в tests/ видят только публичный API."}
    >
      <PyCode>{`pub fn divide(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err("div by zero".to_string())
    } else {
        Ok(a / b)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    #[should_panic(expected = "index out of bounds")]
    fn panics() {
        let v: Vec<i32> = vec![];
        let _ = v[3];
    }

    #[test]
    fn returns_result() -> Result<(), String> {
        assert_eq!(divide(8, 2)?, 4);
        Ok(())
    }

    #[test]
    fn error_case() {
        assert_eq!(divide(1, 0), Err("div by zero".to_string()));
    }
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"test tests::error_case ... ok\ntest tests::panics - should panic ... ok\ntest tests::returns_result ... ok\ntest result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Документация и атрибуты"}
      sub={"///, //!, derive, cfg"}
      main={"Примеры в /// запускаются как тесты; cfg! вычисляется при компиляции."}
    >
      <PyCode>{`//! Крошечная библиотека.

/// Складывает два числа.
///
/// \`\`\`
/// assert_eq!(add(1, 2), 3);
/// \`\`\`
#[inline]
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[derive(Debug, Default)]
#[allow(dead_code)]
struct Settings {
    verbose: bool,
    level: u8,
}

fn main() {
    println!("{:?}", Settings::default());
    println!("{} {}", cfg!(target_pointer_width = "64"), cfg!(test));
    println!("{}", add(2, 3));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Settings { verbose: false, level: 0 }\ntrue false\n5"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"main возвращает Result"}
      sub={"Box<dyn Error> и ?"}
      main={"Тонкий main вызывает библиотеку; ошибка из main печатается и даёт ненулевой код выхода."}
    >
      <PyCode>{`use std::error::Error;
use std::fmt;

#[derive(Debug)]
struct ParseError(String);

impl fmt::Display for ParseError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "parse error: {}", self.0)
    }
}
impl Error for ParseError {}

fn parse(s: &str) -> Result<i32, Box<dyn Error>> {
    let n: i32 = s.parse()?;
    if n < 0 {
        return Err(Box::new(ParseError(s.to_string())));
    }
    Ok(n)
}

fn main() -> Result<(), Box<dyn Error>> {
    println!("{}", parse("42")?);
    if let Err(e) = parse("-1") {
        println!("{}", e);
    }
    if let Err(e) = parse("abc") {
        println!("{}", e);
    }
    Ok(())
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"42\nparse error: -1\ninvalid digit found in string"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Идиомы API"}
      sub={"Default, Builder, FromStr"}
      main={"Знакомые трейты делают API предсказуемым: parse::<Point>(), ..Default::default(), цепочки строителя."}
    >
      <PyCode>{`use std::str::FromStr;

#[derive(Debug, Default, Clone, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

impl FromStr for Point {
    type Err = String;
    fn from_str(s: &str) -> Result<Point, String> {
        let (a, b) = s.split_once(',').ok_or("no comma")?;
        Ok(Point {
            x: a.trim().parse().map_err(|_| "bad x")?,
            y: b.trim().parse().map_err(|_| "bad y")?,
        })
    }
}

struct Server {
    host: String,
    port: u16,
    tls: bool,
}

struct ServerBuilder {
    host: String,
    port: u16,
    tls: bool,
}

impl ServerBuilder {
    fn new(host: &str) -> Self {
        ServerBuilder { host: host.into(), port: 80, tls: false }
    }
    fn port(mut self, p: u16) -> Self {
        self.port = p;
        self
    }
    fn tls(mut self, t: bool) -> Self {
        self.tls = t;
        self
    }
    fn build(self) -> Server {
        Server { host: self.host, port: self.port, tls: self.tls }
    }
}

fn main() {
    println!("{:?}", "3, 4".parse::<Point>());
    println!("{:?}", "3;4".parse::<Point>());
    let p = Point { x: 7, ..Default::default() };
    let s = ServerBuilder::new("example.org").port(443).tls(true).build();
    println!("{:?} {}:{} {}", p, s.host, s.port, s.tls);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Ok(Point { x: 3, y: 4 })\nErr(\"no comma\")\nPoint { x: 7, y: 0 } example.org:443 true"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"const, static, рабочее пространство"}
      sub={"Глобальные значения"}
      main={"const подставляется в код; изменяемую static делают атомарной; пакеты проекта объединяют в workspace."}
    >
      <PyCode>{`use std::sync::atomic::{AtomicUsize, Ordering};

const LIMITS: [u32; 3] = [10, 100, 1000];
static NEXT_ID: AtomicUsize = AtomicUsize::new(1);

fn next_id() -> usize {
    NEXT_ID.fetch_add(1, Ordering::SeqCst)
}

fn main() {
    println!("{} {} {}", next_id(), next_id(), next_id());
    println!("{}", LIMITS.iter().sum::<u32>());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 2 3\n1110"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Тонкий main, библиотека с тестами, привычные идиомы — так выглядит хороший проект на Rust."}
    >
      <div className="s-grid2">
        {[["pub · use", "Модули", "Видимость и пути"], ["cargo", "Инструмент", "Сборка, тесты, формат"], ["#[test]", "Тесты", "Модульные, doc, интеграционные"], ["Default · FromStr", "Идиомы", "Предсказуемый API"]].map(([big, t, d]) => (
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
export const SLIDES_R9 = {
  "10:9": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R9).
export const SLIDE_TITLES_R9 = {
  "10:9": [
    "Проект на Rust",
    "Крейт, пакет, модуль",
    "pub и приватность",
    "use и пути",
    "Модули и файлы",
    "Cargo.toml",
    "Модульные тесты",
    "Виды тестов",
    "Документация и атрибуты",
    "main → Result",
    "Default, Builder, FromStr",
    "const и static",
    "Итоги",
  ],
};
