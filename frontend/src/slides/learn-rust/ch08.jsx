// Слайды для «Изучаем Rust», глава 8 — «Время жизни и умные указатели».
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
      <span>ИЗУЧАЕМ RUST / ЯЗЫК ГЛУБЖЕ / ГЛАВА 8</span>
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
      title={"Кто кого переживает"}
      sub={"Глава 8 · Язык глубже"}
      main={"Времена жизни не дают ссылке пережить данные; умные указатели управляют владением."}
    >
      <div className="s-grid2">
        {[["'a", "Времена жизни", "Связи между ссылками"], ["Box<T>", "Куча", "Один владелец"], ["Rc · RefCell", "Общее владение", "Счётчик и внутренняя изменяемость"], ["Weak", "Без циклов", "Слабые ссылки"]].map(([big, t, d]) => (
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
      title={"Висячая ссылка"}
      sub={"Ошибка, которую ловит компилятор"}
      main={"Ссылка не может пережить значение, на которое указывает."}
    >
      <PyCode>{`fn main() {
    let r;
    {
        let x = 5;
        r = &x;
    }
    println!("{}", r);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"error[E0597]: `x` does not live long enough"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Аннотация времени жизни"}
      sub={"longest<'a>"}
      main={"Результат живёт не дольше обоих аргументов — аннотации описывают связи, но не меняют время жизни."}
    >
      <PyCode>{`fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {
    if a.len() >= b.len() {
        a
    } else {
        b
    }
}

fn main() {
    let s1 = String::from("long string");
    let result;
    {
        let s2 = String::from("xyz");
        result = longest(s1.as_str(), s2.as_str()).to_string();
    }
    println!("{}", result);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"long string"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Структуры со ссылками и 'static"}
      sub={"Правила умолчания"}
      main={"Параметр времени жизни у структуры; 'static — на всё время работы программы."}
    >
      <PyCode>{`struct Excerpt<'a> {
    part: &'a str,
}

impl<'a> Excerpt<'a> {
    fn first_word(&self) -> &str {
        self.part.split(' ').next().unwrap_or("")
    }
}

fn first(s: &str) -> &str {
    &s[..1]
}

fn main() {
    let text = String::from("Call me Ishmael. Some years ago...");
    let e = Excerpt { part: &text[..15] };
    println!("{} | {}", e.part, e.first_word());
    let msg: &'static str = "lives forever";
    println!("{} {}", first("rust"), msg);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Call me Ishmael | Call\nr lives forever"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Box<T>"}
      sub={"Значение в куче, рекурсивные типы"}
      main={"Коробка делает размер рекурсивного типа конечным: значение и один указатель."}
    >
      <PyCode>{`enum List {
    Cons(i32, Box<List>),
    Nil,
}
use List::{Cons, Nil};

fn sum(l: &List) -> i32 {
    match l {
        Cons(v, rest) => v + sum(rest),
        Nil => 0,
    }
}

fn main() {
    let list = Cons(1, Box::new(Cons(2, Box::new(Cons(3, Box::new(Nil))))));
    println!("{}", sum(&list));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"6"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Drop"}
      sub={"Очистка привязана к значению"}
      main={"Значения освобождаются в обратном порядке объявления; drop() уничтожает досрочно."}
    >
      <PyCode>{`struct Guard(&'static str);

impl Drop for Guard {
    fn drop(&mut self) {
        println!("drop {}", self.0);
    }
}

fn main() {
    let _a = Guard("a");
    let b = Guard("b");
    {
        let _c = Guard("c");
        println!("inner");
    }
    drop(b);
    println!("end");
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"inner\ndrop c\ndrop b\nend\ndrop a"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Rc<T>"}
      sub={"Общее владение"}
      main={"clone увеличивает счётчик, а не копирует данные; ноль — значение освобождается."}
    >
      <PyCode>{`use std::rc::Rc;

fn main() {
    let a = Rc::new(String::from("shared"));
    println!("{}", Rc::strong_count(&a));
    let b = Rc::clone(&a);
    {
        let _c = Rc::clone(&a);
        println!("{}", Rc::strong_count(&a));
    }
    println!("{} {}", Rc::strong_count(&a), b);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1\n3\n2 shared"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"RefCell<T>"}
      sub={"Внутренняя изменяемость"}
      main={"Правила заимствования проверяются во время работы: нарушение — паника или Err у try_*."}
    >
      <PyCode>{`use std::cell::RefCell;

fn main() {
    let c = RefCell::new(vec![1, 2]);
    c.borrow_mut().push(3);
    println!("{:?}", c.borrow());
    let r1 = c.borrow();
    println!("{}", c.try_borrow_mut().is_err());
    println!("{}", r1.len());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[1, 2, 3]\ntrue\n3"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Rc<RefCell<T>>"}
      sub={"Много владельцев, каждый меняет"}
      main={"Связка даёт общее изменяемое состояние; держите изменяющий доступ как можно короче."}
    >
      <PyCode>{`use std::cell::RefCell;
use std::rc::Rc;

struct Account {
    balance: i32,
}

fn main() {
    let acc = Rc::new(RefCell::new(Account { balance: 100 }));
    let a = Rc::clone(&acc);
    let b = Rc::clone(&acc);
    a.borrow_mut().balance -= 30;
    b.borrow_mut().balance += 5;
    println!("{} {}", acc.borrow().balance, Rc::strong_count(&acc));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"75 3"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Weak<T>"}
      sub={"Разрываем циклы"}
      main={"Слабая ссылка не удерживает значение: upgrade() вернёт Some, только пока оно живо."}
    >
      <PyCode>{`use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Node {
    name: String,
    parent: RefCell<Weak<Node>>,
    children: RefCell<Vec<Rc<Node>>>,
}

fn node(name: &str) -> Rc<Node> {
    Rc::new(Node {
        name: name.to_string(),
        parent: RefCell::new(Weak::new()),
        children: RefCell::new(vec![]),
    })
}

fn main() {
    let root = node("root");
    let leaf = node("leaf");
    *leaf.parent.borrow_mut() = Rc::downgrade(&root);
    root.children.borrow_mut().push(Rc::clone(&leaf));
    println!("{}", leaf.parent.borrow().upgrade().map(|p| p.name.clone()).unwrap_or_default());
    println!("{} {}", Rc::strong_count(&root), Rc::weak_count(&root));
    println!("{} {}", root.children.borrow().len(), leaf.name);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"root\n1 1\n1 leaf"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Cow: копировать по необходимости"}
      sub={"Выбор указателя"}
      main={"Cow хранит ссылку или владеющее значение — копирование только когда оно нужно."}
    >
      <PyCode>{`use std::borrow::Cow;

fn clean(s: &str) -> Cow<str> {
    if s.contains(' ') {
        Cow::Owned(s.replace(' ', "_"))
    } else {
        Cow::Borrowed(s)
    }
}

fn main() {
    for s in ["no_spaces", "has some spaces"] {
        let c = clean(s);
        let kind = match &c {
            Cow::Borrowed(_) => "borrowed",
            Cow::Owned(_) => "owned",
        };
        println!("{} {}", c, kind);
    }
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"no_spaces borrowed\nhas_some_spaces owned"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Дерево поиска"}
      sub={"Option<Box<Node>>"}
      main={"Память дерева освобождается рекурсивно, без сборщика мусора и без утечек."}
    >
      <PyCode>{`struct Node {
    key: i32,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

impl Node {
    fn new(key: i32) -> Self {
        Node { key, left: None, right: None }
    }
    fn insert(&mut self, key: i32) {
        let slot = if key < self.key { &mut self.left } else { &mut self.right };
        match slot {
            Some(n) => n.insert(key),
            None => *slot = Some(Box::new(Node::new(key))),
        }
    }
    fn inorder(&self, out: &mut Vec<i32>) {
        if let Some(l) = &self.left {
            l.inorder(out);
        }
        out.push(self.key);
        if let Some(r) = &self.right {
            r.inorder(out);
        }
    }
}

fn main() {
    let mut root = Node::new(5);
    for k in [3, 8, 1, 4, 9] {
        root.insert(k);
    }
    let mut v = Vec::new();
    root.inorder(&mut v);
    println!("{:?}", v);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[1, 3, 4, 5, 8, 9]"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Выбирайте указатель по вопросу: сколько владельцев, один ли поток, нужно ли менять?"}
    >
      <div className="s-grid2">
        {[["&'a T", "Ссылка", "Не переживает значение"], ["Box · Rc · Arc", "Владение", "Один или много"], ["RefCell", "Изменение", "Проверка при запуске"], ["Weak · Cow", "Тонкости", "Циклы и копии"]].map(([big, t, d]) => (
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
export const SLIDES_R8 = {
  "10:8": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R8).
export const SLIDE_TITLES_R8 = {
  "10:8": [
    "Время жизни и указатели",
    "Висячая ссылка",
    "Аннотация 'a",
    "Структура со ссылкой",
    "Box",
    "Drop",
    "Rc",
    "RefCell",
    "Rc<RefCell>",
    "Weak",
    "Cow",
    "Двоичное дерево",
    "Итоги",
  ],
};
