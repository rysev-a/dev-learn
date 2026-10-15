// Слайды для «Изучаем Rust», глава 10 — «Потоки и общее состояние».
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
      <span>ИЗУЧАЕМ RUST / ЯЗЫК ГЛУБЖЕ / ГЛАВА 10</span>
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
      title={"Бесстрашная параллельность"}
      sub={"Глава 10 · Язык глубже"}
      main={"Владение и заимствование превращают гонки данных в ошибки компиляции."}
    >
      <div className="s-grid2">
        {[["spawn · join", "Потоки", "move и scope"], ["mpsc", "Каналы", "Передача владения"], ["Arc<Mutex<T>>", "Общее состояние", "Блокировки и атомики"], ["Send · Sync", "Безопасность", "Проверяет компилятор"]].map(([big, t, d]) => (
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
      title={"spawn и join"}
      sub={"move-замыкание"}
      main={"Поток может пережить функцию, поэтому данные в замыкание передают через move."}
    >
      <PyCode>{`use std::thread;

fn main() {
    let v = vec![1, 2, 3];
    let handle = thread::spawn(move || {
        let sum: i32 = v.iter().sum();
        sum * 2
    });
    println!("{}", handle.join().unwrap());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"12"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Потоки с областью видимости"}
      sub={"thread::scope"}
      main={"Внутри scope потоки заимствуют данные — копий и счётчиков ссылок не нужно."}
    >
      <PyCode>{`use std::thread;

fn main() {
    let data = vec![1, 2, 3, 4, 5, 6];
    let (left, right) = data.split_at(3);
    let (a, b) = thread::scope(|s| {
        let h1 = s.spawn(|| left.iter().sum::<i32>());
        let h2 = s.spawn(|| right.iter().sum::<i32>());
        (h1.join().unwrap(), h2.join().unwrap())
    });
    println!("{} {} {}", a, b, data.len());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"6 15 6"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Каналы"}
      sub={"mpsc: много производителей — один потребитель"}
      main={"Отправка передаёт значение во владение; когда все передатчики уничтожены, приёмник завершает цикл."}
    >
      <PyCode>{`use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();
    let mut handles = vec![];
    for id in 0..3 {
        let tx = tx.clone();
        handles.push(thread::spawn(move || {
            tx.send((id, id * 10)).unwrap();
        }));
    }
    drop(tx);
    for h in handles {
        h.join().unwrap();
    }
    let mut got: Vec<(i32, i32)> = rx.iter().collect();
    got.sort();
    println!("{:?}", got);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[(0, 0), (1, 10), (2, 20)]"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Arc<Mutex<T>>"}
      sub={"Общее состояние"}
      main={"Arc — общее владение между потоками, Mutex — доступ по одному; защитник держит блокировку."}
    >
      <PyCode>{`use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut hs = vec![];
    for _ in 0..8 {
        let c = Arc::clone(&counter);
        hs.push(thread::spawn(move || {
            for _ in 0..1000 {
                *c.lock().unwrap() += 1;
            }
        }));
    }
    for h in hs {
        h.join().unwrap();
    }
    println!("{} {}", *counter.lock().unwrap(), Arc::strong_count(&counter));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"8000 1"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Отравление мьютекса"}
      sub={"Паника под блокировкой"}
      main={"Паника при удержании блокировки отравляет мьютекс; данные можно достать из ошибки."}
    >
      <PyCode>{`use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let m = Arc::new(Mutex::new(vec![1]));
    {
        let mut g = m.lock().unwrap();
        g.push(2);
    }
    let m2 = Arc::clone(&m);
    let r = thread::spawn(move || {
        let _g = m2.lock().unwrap();
        panic!("boom");
    })
    .join();
    println!("{} {}", r.is_err(), m.is_poisoned());
    let data = m.lock().unwrap_or_else(|e| e.into_inner());
    println!("{:?}", *data);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"true true\n[1, 2]"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"RwLock и атомики"}
      sub={"Много читателей, простые счётчики"}
      main={"RwLock пускает много читателей и одного писателя; атомики заменяют мьютекс для чисел и флагов."}
    >
      <PyCode>{`use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{Arc, RwLock};
use std::thread;

fn main() {
    let cfg = Arc::new(RwLock::new(String::from("v1")));
    let hits = Arc::new(AtomicU64::new(0));
    let hs: Vec<_> = (0..4)
        .map(|_| {
            let (cfg, hits) = (Arc::clone(&cfg), Arc::clone(&hits));
            thread::spawn(move || {
                let _r = cfg.read().unwrap();
                hits.fetch_add(10, Ordering::Relaxed);
            })
        })
        .collect();
    for h in hs {
        h.join().unwrap();
    }
    *cfg.write().unwrap() = "v2".to_string();
    println!("{} {}", cfg.read().unwrap(), hits.load(Ordering::SeqCst));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"v2 40"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Send и Sync"}
      sub={"Компилятор не пустит Rc в поток"}
      main={"Rc не Send: счётчик не атомарный — программа с гонкой на нём просто не соберётся."}
    >
      <PyCode>{`use std::rc::Rc;
use std::thread;

fn main() {
    let a = Rc::new(5);
    let h = thread::spawn(move || println!("{}", a));
    h.join().unwrap();
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"error[E0277]: `Rc<i32>` cannot be sent between threads safely"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Пул рабочих потоков"}
      sub={"Канал задач + канал результатов"}
      main={"Приёмник один, поэтому его делят через Arc<Mutex<Receiver>>; закрытие канала завершает рабочих."}
    >
      <PyCode>{`use std::sync::{mpsc, Arc, Mutex};
use std::thread;

fn main() {
    let (job_tx, job_rx) = mpsc::channel::<u64>();
    let (res_tx, res_rx) = mpsc::channel::<(u64, u64)>();
    let job_rx = Arc::new(Mutex::new(job_rx));
    let workers: Vec<_> = (0..3)
        .map(|_| {
            let rx = Arc::clone(&job_rx);
            let tx = res_tx.clone();
            thread::spawn(move || loop {
                let job = rx.lock().unwrap().recv();
                match job {
                    Ok(n) => tx.send((n, n * n)).unwrap(),
                    Err(_) => break,
                }
            })
        })
        .collect();
    drop(res_tx);
    for n in 1..=6 {
        job_tx.send(n).unwrap();
    }
    drop(job_tx);
    for w in workers {
        w.join().unwrap();
    }
    let mut r: Vec<_> = res_rx.iter().collect();
    r.sort();
    println!("{:?}", r);
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[(1, 1), (2, 4), (3, 9), (4, 16), (5, 25), (6, 36)]"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Параллельная свёртка"}
      sub={"chunks + scope"}
      main={"Режем массив на куски, считаем в потоках, складываем — но сначала измерьте, стоит ли."}
    >
      <PyCode>{`use std::thread;

fn par_sum(v: &[u64], parts: usize) -> u64 {
    let size = (v.len() + parts - 1) / parts;
    thread::scope(|s| {
        let hs: Vec<_> = v
            .chunks(size)
            .map(|c| s.spawn(move || c.iter().sum::<u64>()))
            .collect();
        hs.into_iter().map(|h| h.join().unwrap()).sum()
    })
}

fn main() {
    let v: Vec<u64> = (1..=1000).collect();
    println!("{} {}", par_sum(&v, 4), par_sum(&v, 7));
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"500500 500500"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Condvar"}
      sub={"Ждать события, а не данные"}
      main={"Условную переменную всегда проверяют в цикле: пробуждение бывает ложным."}
    >
      <PyCode>{`use std::sync::{Arc, Condvar, Mutex};
use std::thread;

fn main() {
    let pair = Arc::new((Mutex::new(false), Condvar::new()));
    let p2 = Arc::clone(&pair);
    let t = thread::spawn(move || {
        let (lock, cv) = &*p2;
        *lock.lock().unwrap() = true;
        cv.notify_one();
    });
    let (lock, cv) = &*pair;
    let mut ready = lock.lock().unwrap();
    while !*ready {
        ready = cv.wait(ready).unwrap();
    }
    println!("ready {}", *ready);
    drop(ready);
    t.join().unwrap();
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"ready true"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Потоки или async"}
      sub={"Выбор инструмента"}
      main={"Потоки — для вычислений и небольшого числа задач; async — для тысяч ожидающих соединений."}
    >
      <PyCode>{`use std::thread;

fn main() {
    let h = thread::Builder::new()
        .name("worker-1".into())
        .spawn(|| thread::current().name().unwrap().to_string())
        .unwrap();
    println!("{}", h.join().unwrap());
    let r = thread::spawn(|| {
        if true {
            panic!("oops");
        }
        5
    })
    .join();
    println!("{}", r.is_err());
}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"worker-1\ntrue"}</Cmd>
      <div className="s-note">{"Асинхронный код (tokio) использует те же Send/Sync: у каждого потока своего стека нет, а ожидание не занимает поток."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Безопасная параллельность — свойство системы типов, а не дисциплины программиста."}
    >
      <div className="s-grid2">
        {[["move · scope", "Данные в потоки", "Владение или заимствование"], ["mpsc · Mutex", "Общение", "Каналы и блокировки"], ["Atomic · RwLock", "Лёгкая синхронизация", "Счётчики, читатели"], ["Send · Sync", "Стражи", "Гонки не компилируются"]].map(([big, t, d]) => (
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
export const SLIDES_R10 = {
  "10:10": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R10).
export const SLIDE_TITLES_R10 = {
  "10:10": [
    "Потоки в Rust",
    "spawn и join",
    "thread::scope",
    "Каналы",
    "Arc и Mutex",
    "Отравление",
    "RwLock и атомики",
    "Send и Sync",
    "Пул потоков",
    "Параллельная сумма",
    "Condvar",
    "Потоки или async",
    "Итоги",
  ],
};
