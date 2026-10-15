// Слайды для «Изучаем Rust», глава 7 — «Замыкания и итераторы».
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
      <span>ИЗУЧАЕМ RUST / ЯЗЫК ГЛУБЖЕ / ГЛАВА 7</span>
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
      title={"Замыкания и итераторы"}
      sub={"Глава 7 · Язык глубже"}
      main={"Замыкания берут значения из окружения, итераторы строят ленивые конвейеры — вместе они заменяют циклы."}
    >
      <div className="s-grid2">
        {[["|x| x + 1", "Замыкания", "Безымянные функции"], ["Fn · FnMut · FnOnce", "Захват", "Ссылка, &mut или владение"], ["map · filter", "Адаптеры", "Ленивая цепочка"], ["collect · sum", "Потребители", "Запускают и сворачивают"]].map(([big, t, d]) => (
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
      title={"Замыкание"}
      sub={"Безымянная функция с окружением"}
      main={"Параметры — между чертами; значения снаружи замыкание захватывает само."}
    >
      <PyCode>{`fn main() {
    let add = |a: i32, b: i32| a + b;
    let offset = 10;
    let shift = |x: i32| x + offset;
    println!("{} {}", add(2, 3), shift(5));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"5 15"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Три способа захвата"}
      sub={"Fn, FnMut, FnOnce"}
      main={"Читает — Fn; меняет — FnMut; расходует захваченное — FnOnce; move передаёт владение."}
    >
      <PyCode>{`fn main() {
    let mut count = 0;
    let mut inc = || {
        count += 1;
        count
    };
    println!("{} {}", inc(), inc());
    println!("{}", count);
    let name = String::from("rust");
    let consume = move || format!("hello {}", name);
    println!("{}", consume());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 2\n2\nhello rust"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Замыкания как значения"}
      sub={"Параметр, результат, коробка"}
      main={"F: Fn(i32) -> i32 принимает любое подходящее замыкание; Box<dyn Fn> хранит разные в одном векторе."}
    >
      <PyCode>{`fn apply<F: Fn(i32) -> i32>(f: F, x: i32) -> i32 {
    f(x)
}

fn main() {
    let double = |x| x * 2;
    println!("{}", apply(double, 21));
    let ops: Vec<Box<dyn Fn(i32) -> i32>> = vec![Box::new(|x| x + 1), Box::new(|x| x * x)];
    let r: Vec<i32> = ops.iter().map(|f| f(7)).collect();
    println!("{:?}", r);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"42\n[8, 49]"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Итератор"}
      sub={"Трейт Iterator и метод next"}
      main={"next возвращает Some(значение), а в конце — None; цикл for просто вызывает его."}
    >
      <PyCode>{`fn main() {
    let v = vec![10, 20];
    let mut it = v.iter();
    println!("{:?}", it.next());
    println!("{:?}", it.next());
    println!("{:?}", it.next());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Some(10)\nSome(20)\nNone"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Три способа обойти коллекцию"}
      sub={"iter, iter_mut, into_iter"}
      main={"Читать, менять на месте или потребить — прямое продолжение правил владения."}
    >
      <PyCode>{`fn main() {
    let mut v = vec![1, 2, 3];
    let s: Vec<String> = v.iter().map(|x| x.to_string()).collect();
    println!("{}", s.join(" "));
    for x in v.iter_mut() {
        *x *= 10;
    }
    println!("{:?}", v);
    let total: i32 = v.into_iter().sum();
    println!("{}", total);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 2 3\n[10, 20, 30]\n60"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Адаптеры"}
      sub={"map, filter, enumerate, zip, chain, rev"}
      main={"Адаптеры принимают итератор и возвращают новый — их цепляют слева направо."}
    >
      <PyCode>{`fn main() {
    let a = [1, 2, 3, 4, 5, 6];
    let r: Vec<i32> = a.iter().filter(|&&x| x % 2 == 0).map(|x| x * x).collect();
    println!("{:?}", r);
    let pairs: Vec<(usize, char)> = "abc".chars().enumerate().collect();
    println!("{:?}", pairs);
    let z: Vec<(i32, &str)> = vec![1, 2].into_iter().zip(["a", "b", "c"]).collect();
    println!("{:?}", z);
    let c: Vec<i32> = (1..3).chain(7..9).rev().collect();
    println!("{:?}", c);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[4, 16, 36]\n[(0, 'a'), (1, 'b'), (2, 'c')]\n[(1, \"a\"), (2, \"b\")]\n[8, 7, 2, 1]"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Потребители"}
      sub={"sum, count, max, fold, any, find"}
      main={"Потребитель запускает цепочку и сворачивает её в итог; any и all останавливаются раньше."}
    >
      <PyCode>{`fn main() {
    let v = vec![3, 8, 1, 9, 4];
    println!("{} {}", v.iter().sum::<i32>(), v.iter().count());
    println!("{:?} {:?}", v.iter().max(), v.iter().min());
    println!("{}", v.iter().fold(0, |acc, x| acc * 2 + x));
    println!("{} {}", v.iter().any(|&x| x > 8), v.iter().all(|&x| x > 1));
    println!("{:?} {:?}", v.iter().find(|&&x| x > 5), v.iter().position(|&x| x == 1));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"25 5\nSome(9) Some(1)\n138\ntrue false\nSome(8) Some(2)"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Ленивость"}
      sub={"Пока не вызван потребитель — ничего"}
      main={"Элементы идут по цепочке по одному; промежуточных коллекций нет."}
    >
      <PyCode>{`fn main() {
    let it = (1..4).map(|x| {
        println!("map {}", x);
        x * 2
    });
    println!("created");
    let v: Vec<i32> = it.collect();
    println!("{:?}", v);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"created\nmap 1\nmap 2\nmap 3\n[2, 4, 6]"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"collect во что угодно"}
      sub={"Vec, String, HashMap, Result"}
      main={"Тип результата выбирает коллекцию; итератор Result собирается в Result<Vec<_>, _>."}
    >
      <PyCode>{`use std::collections::HashMap;

fn main() {
    let s: String = vec!['r', 'u', 's', 't'].into_iter().collect();
    let m: HashMap<&str, i32> = vec![("a", 1), ("b", 2)].into_iter().collect();
    let ok: Result<Vec<i32>, _> = "1 2 3".split(' ').map(|x| x.parse::<i32>()).collect();
    let bad: Result<Vec<i32>, _> = "1 x 3".split(' ').map(|x| x.parse::<i32>()).collect();
    println!("{} {}", s, m["b"]);
    println!("{:?}", ok);
    println!("{}", bad.is_err());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"rust 2\nOk([1, 2, 3])\ntrue"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Окна, куски и сортировка"}
      sub={"windows, chunks, sort_by_key"}
      main={"Готовые заготовки не выделяют память; цепочки разворачиваются в тот же цикл, что и ручной."}
    >
      <PyCode>{`fn main() {
    let v = [1, 4, 9, 16, 25];
    let diffs: Vec<i32> = v.windows(2).map(|w| w[1] - w[0]).collect();
    println!("{:?}", diffs);
    let sums: Vec<i32> = v.chunks(2).map(|c| c.iter().sum()).collect();
    println!("{:?}", sums);
    let mut words = vec!["pear", "fig", "banana"];
    words.sort_by_key(|w| w.len());
    println!("{:?}", words);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[3, 5, 7, 9]\n[5, 25, 25]\n[\"fig\", \"pear\", \"banana\"]"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Ещё адаптеры"}
      sub={"flat_map, take_while, scan, peekable"}
      main={"Ленивость позволяет брать нужное из бесконечного диапазона."}
    >
      <PyCode>{`fn main() {
    let v: Vec<char> = vec!["ab", "cd"].iter().flat_map(|s| s.chars()).collect();
    println!("{:?}", v);
    let squares: Vec<u32> = (1..).map(|x| x * x).take_while(|&x| x < 50).collect();
    println!("{:?}", squares);
    let running: Vec<i32> = [1, 2, 3, 4]
        .iter()
        .scan(0, |acc, &x| {
            *acc += x;
            Some(*acc)
        })
        .collect();
    println!("{:?}", running);
    let mut p = [1, 2, 3].iter().peekable();
    println!("{:?}", p.peek());
    println!("{:?}", p.next());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['a', 'b', 'c', 'd']\n[1, 4, 9, 16, 25, 36, 49]\n[1, 3, 6, 10]\nSome(1)\nSome(1)"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Замыкания + итераторы = короткий, выразительный и быстрый код."}
    >
      <div className="s-grid2">
        {[["move", "Владение", "Замыкание забирает значения"], ["next()", "Итератор", "Some / None"], ["lazy", "Ленивость", "Работа только по запросу"], ["collect", "Результат", "Любая коллекция или Result"]].map(([big, t, d]) => (
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
export const SLIDES_R7 = {
  "10:7": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R7).
export const SLIDE_TITLES_R7 = {
  "10:7": [
    "Замыкания и итераторы",
    "Замыкание",
    "Захват и трейты",
    "Замыкание как значение",
    "Итератор",
    "iter, iter_mut, into_iter",
    "Адаптеры",
    "Потребители",
    "Ленивость",
    "collect",
    "Окна и куски",
    "flat_map, scan, peekable",
    "Итоги",
  ],
};
