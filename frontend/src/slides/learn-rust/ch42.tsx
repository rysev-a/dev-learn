import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, RsCode } from "../widgets.tsx";
// Слайды для «Изучаем Rust», глава 42 — «Маршрутизатор и многопоточный сервер».
// Тот же дизайн-код, что и в главах 1–5: палитра, IBM Plex Mono / Inter,
// рубрика + номер, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

const Slide = makeSlide("ИЗУЧАЕМ RUST / ВЕБ-СЕРВЕР / ГЛАВА 42", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"От разбора к приложению"}
      sub={"Глава 42 · Веб-сервер"}
      main={"Маршруты, слои, состояние, пул потоков, лимиты и тесты — всё из стандартной библиотеки."}
    >
      <div className="s-grid2">
        {([["GET /users/:id", "Маршруты", "Параметры по сегментам"], ["middleware", "Слои", "Журнал, доступ"], ["Arc<Mutex<_>>", "Состояние", "Общее для запросов"], ["ThreadPool", "Пул", "Мягкая остановка"]] as const).map(([big, t, d]) => (
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
      title={"Маршрутизатор"}
      sub={"404 против 405"}
      main={"Шаблон нашёлся, а метод нет — 405; шаблона нет вовсе — 404."}
    >
      <RsCode>{`type Handler = fn(&str) -> String;

struct Router {
    routes: Vec<(String, String, Handler)>,
}

impl Router {
    fn new() -> Router {
        Router { routes: Vec::new() }
    }
    fn add(&mut self, method: &str, path: &str, h: Handler) {
        self.routes.push((method.to_string(), path.to_string(), h));
    }
    fn dispatch(&self, method: &str, path: &str) -> (u16, String) {
        let mut path_exists = false;
        for (m, p, h) in &self.routes {
            if p == path {
                if m == method {
                    return (200, h(path));
                }
                path_exists = true;
            }
        }
        if path_exists {
            (405, "method not allowed".into())
        } else {
            (404, "not found".into())
        }
    }
}

fn home(_: &str) -> String {
    "home".into()
}
fn about(_: &str) -> String {
    "about".into()
}

fn main() {
    let mut r = Router::new();
    r.add("GET", "/", home);
    r.add("GET", "/about", about);
    println!("{:?}", r.dispatch("GET", "/about"));
    println!("{:?}", r.dispatch("POST", "/about"));
    println!("{:?}", r.dispatch("GET", "/zzz"));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(200, \"about\")\n(405, \"method not allowed\")\n(404, \"not found\")"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Параметры в адресе"}
      sub={"/users/:id"}
      main={"Сопоставляем по сегментам: число совпадает, :имя запоминается, остальное — дословно."}
    >
      <RsCode>{`fn match_route(pattern: &str, path: &str) -> Option<Vec<(String, String)>> {
    let p: Vec<&str> = pattern.trim_matches('/').split('/').collect();
    let q: Vec<&str> = path.trim_matches('/').split('/').collect();
    if p.len() != q.len() {
        return None;
    }
    let mut params = Vec::new();
    for (a, b) in p.iter().zip(q.iter()) {
        if let Some(name) = a.strip_prefix(':') {
            params.push((name.to_string(), b.to_string()));
        } else if a != b {
            return None;
        }
    }
    Some(params)
}

fn main() {
    println!("{:?}", match_route("/users/:id/posts/:post", "/users/42/posts/7"));
    println!("{:?}", match_route("/users/:id", "/users"));
    println!("{:?}", match_route("/users/:id", "/accounts/5"));
    println!("{:?}", match_route("/", "/"));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Some([(\"id\", \"42\"), (\"post\", \"7\")])\nNone\nNone\nSome([])"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Слои (middleware)"}
      sub={"Обработчик → обработчик"}
      main={"Слой берёт обработчик и возвращает обёрнутый; порядок обёртывания — порядок выполнения."}
    >
      <RsCode>{`use std::cell::RefCell;
use std::rc::Rc;

struct Request {
    path: String,
    auth: Option<String>,
}

#[derive(Debug)]
struct Response {
    status: u16,
    body: String,
}

type Handler = Box<dyn Fn(&Request) -> Response>;

fn logging(next: Handler, log: Rc<RefCell<Vec<String>>>) -> Handler {
    Box::new(move |req| {
        log.borrow_mut().push(format!("-> {}", req.path));
        let r = next(req);
        log.borrow_mut().push(format!("<- {}", r.status));
        r
    })
}

fn require_auth(next: Handler) -> Handler {
    Box::new(move |req| {
        if req.auth.as_deref() == Some("secret") {
            next(req)
        } else {
            Response { status: 401, body: "unauthorized".into() }
        }
    })
}

fn main() {
    let log = Rc::new(RefCell::new(Vec::new()));
    let app: Handler = Box::new(|_| Response { status: 200, body: "ok".into() });
    let app = logging(require_auth(app), log.clone());
    println!("{:?}", app(&Request { path: "/a".into(), auth: Some("secret".into()) }));
    println!("{:?}", app(&Request { path: "/b".into(), auth: None }));
    println!("{:?}", log.borrow());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Response { status: 200, body: \"ok\" }\nResponse { status: 401, body: \"unauthorized\" }\n[\"-> /a\", \"<- 200\", \"-> /b\", \"<- 401\"]"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Общее состояние"}
      sub={"Arc<Mutex<_>> и маленькие методы"}
      main={"Блокировка берётся внутри метода на короткое время и не утекает наружу."}
    >
      <RsCode>{`use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::thread;

#[derive(Clone)]
struct AppState {
    counters: Arc<Mutex<HashMap<String, u64>>>,
}

fn hit(state: &AppState, path: &str) -> u64 {
    let mut m = state.counters.lock().unwrap();
    let c = m.entry(path.to_string()).or_insert(0);
    *c += 1;
    *c
}

fn main() {
    let state = AppState { counters: Arc::new(Mutex::new(HashMap::new())) };
    let hs: Vec<_> = (0..4)
        .map(|_| {
            let s = state.clone();
            thread::spawn(move || {
                for _ in 0..250 {
                    hit(&s, "/home");
                }
            })
        })
        .collect();
    for h in hs {
        h.join().unwrap();
    }
    println!("{} {}", hit(&state, "/home"), hit(&state, "/other"));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1001 1"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Хранилище дел"}
      sub={"Слой данных без знания о сети"}
      main={"Хранилище не знает про HTTP, протокол не знает про хранилище — каждое проверяется отдельно."}
    >
      <RsCode>{`use std::collections::BTreeMap;

#[derive(Debug, Clone)]
struct Todo {
    title: String,
    done: bool,
}

struct Store {
    next: u32,
    items: BTreeMap<u32, Todo>,
}

impl Store {
    fn new() -> Store {
        Store { next: 1, items: BTreeMap::new() }
    }
    fn create(&mut self, title: &str) -> u32 {
        let id = self.next;
        self.next += 1;
        self.items.insert(id, Todo { title: title.into(), done: false });
        id
    }
    fn complete(&mut self, id: u32) -> Result<(), String> {
        self.items.get_mut(&id).map(|t| t.done = true).ok_or_else(|| format!("todo {} not found", id))
    }
    fn delete(&mut self, id: u32) -> bool {
        self.items.remove(&id).is_some()
    }
}

fn main() {
    let mut s = Store::new();
    let a = s.create("write chapter");
    let b = s.create("test server");
    println!("{} {} {:?}", a, b, s.complete(a));
    println!("{:?} {}", s.complete(9), s.delete(b));
    println!("{:?}", s.items);
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 2 Ok(())\nErr(\"todo 9 not found\") true\n{1: Todo { title: \"write chapter\", done: true }}"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Пул потоков"}
      sub={"Очередь заданий и мягкая остановка"}
      main={"Drop закрывает канал и ждёт рабочих: принятые задания выполняются до конца."}
    >
      <RsCode>{`use std::sync::{mpsc, Arc, Mutex};
use std::thread;

type Job = Box<dyn FnOnce() + Send + 'static>;

struct Pool {
    workers: Vec<thread::JoinHandle<()>>,
    tx: Option<mpsc::Sender<Job>>,
}

impl Pool {
    fn new(n: usize) -> Pool {
        let (tx, rx) = mpsc::channel::<Job>();
        let rx = Arc::new(Mutex::new(rx));
        let workers = (0..n)
            .map(|_| {
                let rx = Arc::clone(&rx);
                thread::spawn(move || loop {
                    let job = rx.lock().unwrap().recv();
                    match job {
                        Ok(j) => j(),
                        Err(_) => break,
                    }
                })
            })
            .collect();
        Pool { workers, tx: Some(tx) }
    }
    fn execute<F: FnOnce() + Send + 'static>(&self, f: F) {
        self.tx.as_ref().unwrap().send(Box::new(f)).unwrap();
    }
}

impl Drop for Pool {
    fn drop(&mut self) {
        drop(self.tx.take());
        for w in self.workers.drain(..) {
            w.join().unwrap();
        }
    }
}

fn main() {
    let results = Arc::new(Mutex::new(Vec::new()));
    {
        let pool = Pool::new(3);
        for i in 0..8 {
            let r = Arc::clone(&results);
            pool.execute(move || {
                r.lock().unwrap().push(i * i);
            });
        }
    }
    let mut v = results.lock().unwrap().clone();
    v.sort();
    println!("{:?}", v);
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[0, 1, 4, 9, 16, 25, 36, 49]"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Остановка сервера"}
      sub={"Неблокирующий accept и флаг"}
      main={"Блокирующий accept снаружи не прервать: нужен неблокирующий сокет и атомарный флаг остановки."}
    >
      <RsCode>{`use std::net::{TcpListener, TcpStream};
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::Arc;
use std::thread;
use std::time::Duration;

fn main() {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    listener.set_nonblocking(true).unwrap();
    let addr = listener.local_addr().unwrap();
    let stop = Arc::new(AtomicBool::new(false));
    let accepted = Arc::new(AtomicUsize::new(0));
    let (flag, count) = (Arc::clone(&stop), Arc::clone(&accepted));
    let server = thread::spawn(move || {
        while !flag.load(Ordering::SeqCst) {
            match listener.accept() {
                Ok(_) => {
                    count.fetch_add(1, Ordering::SeqCst);
                }
                Err(_) => thread::sleep(Duration::from_millis(2)),
            }
        }
    });
    let clients: Vec<TcpStream> = (0..3).map(|_| TcpStream::connect(addr).unwrap()).collect();
    while accepted.load(Ordering::SeqCst) < 3 {
        thread::sleep(Duration::from_millis(2));
    }
    stop.store(true, Ordering::SeqCst);
    server.join().unwrap();
    println!("accepted {} of {}", accepted.load(Ordering::SeqCst), clients.len());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"accepted 3 of 3"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Ограничение скорости"}
      sub={"Ведро с жетонами"}
      main={"Время — параметр функции, поэтому поведение проверяется без ожидания."}
    >
      <RsCode>{`struct TokenBucket {
    capacity: f64,
    tokens: f64,
    rate: f64,
    last: f64,
}

impl TokenBucket {
    fn new(capacity: f64, rate: f64) -> TokenBucket {
        TokenBucket { capacity, tokens: capacity, rate, last: 0.0 }
    }
    fn allow(&mut self, now: f64) -> bool {
        self.tokens = (self.tokens + (now - self.last) * self.rate).min(self.capacity);
        self.last = now;
        if self.tokens >= 1.0 {
            self.tokens -= 1.0;
            true
        } else {
            false
        }
    }
}

fn main() {
    let mut b = TokenBucket::new(3.0, 1.0);
    let r: Vec<bool> = [0.0, 0.1, 0.2, 0.3, 1.5, 1.6, 10.0].iter().map(|&t| b.allow(t)).collect();
    println!("{:?}", r);
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[true, true, true, false, true, false, true]"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Интеграционный тест"}
      sub={"Настоящий сервер на свободном порту"}
      main={"Сервер в потоке с ограничением числа соединений, клиентская функция — и обычные проверки."}
    >
      <RsCode>{`use std::io::{Read, Write};
use std::net::{SocketAddr, TcpListener, TcpStream};
use std::thread;

fn start_server() -> (SocketAddr, thread::JoinHandle<()>) {
    let l = TcpListener::bind("127.0.0.1:0").unwrap();
    let addr = l.local_addr().unwrap();
    let h = thread::spawn(move || {
        for s in l.incoming().take(2) {
            let mut s = s.unwrap();
            let mut buf = [0u8; 256];
            let n = s.read(&mut buf).unwrap();
            let line = String::from_utf8_lossy(&buf[..n]);
            let body = if line.starts_with("GET /ping") { "pong" } else { "?" };
            write!(s, "HTTP/1.1 200 OK\\r\\nContent-Length: {}\\r\\nConnection: close\\r\\n\\r\\n{}", body.len(), body).unwrap();
        }
    });
    (addr, h)
}

fn http_get(addr: SocketAddr, path: &str) -> (u16, String) {
    let mut c = TcpStream::connect(addr).unwrap();
    c.write_all(format!("GET {} HTTP/1.1\\r\\nHost: t\\r\\n\\r\\n", path).as_bytes()).unwrap();
    let mut out = String::new();
    c.read_to_string(&mut out).unwrap();
    let (head, body) = out.split_once("\\r\\n\\r\\n").unwrap();
    let code = head.split(' ').nth(1).unwrap().parse().unwrap();
    (code, body.to_string())
}

fn main() {
    let (addr, h) = start_server();
    println!("{:?}", http_get(addr, "/ping"));
    println!("{:?}", http_get(addr, "/other"));
    h.join().unwrap();
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(200, \"pong\")\n(200, \"?\")"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Метрики"}
      sub={"Атомарные счётчики"}
      main={"Счётчики безопасны из любого потока; метод вывода превращает их в текст для мониторинга."}
    >
      <RsCode>{`use std::sync::atomic::{AtomicU64, Ordering};

struct Metrics {
    requests: AtomicU64,
    errors: AtomicU64,
    bytes: AtomicU64,
}

impl Metrics {
    fn record(&self, status: u16, bytes: u64) {
        self.requests.fetch_add(1, Ordering::Relaxed);
        if status >= 500 {
            self.errors.fetch_add(1, Ordering::Relaxed);
        }
        self.bytes.fetch_add(bytes, Ordering::Relaxed);
    }
    fn render(&self) -> String {
        format!(
            "requests_total {}\\nerrors_total {}\\nbytes_total {}",
            self.requests.load(Ordering::Relaxed),
            self.errors.load(Ordering::Relaxed),
            self.bytes.load(Ordering::Relaxed)
        )
    }
}

fn main() {
    let m = Metrics { requests: AtomicU64::new(0), errors: AtomicU64::new(0), bytes: AtomicU64::new(0) };
    for (s, b) in [(200, 120), (404, 40), (500, 10), (200, 300)] {
        m.record(s, b);
    }
    println!("{}", m.render());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"requests_total 4\nerrors_total 1\nbytes_total 470"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Настройки приложения"}
      sub={"Флаги, значения по умолчанию, понятные ошибки"}
      main={"Структура Config + разбор флагов: все ошибки — значения Result с понятным текстом."}
    >
      <RsCode>{`struct Config {
    addr: String,
    workers: usize,
    max_body: usize,
}

impl Config {
    fn from_args(args: &[&str]) -> Result<Config, String> {
        let mut c = Config { addr: "127.0.0.1:8080".into(), workers: 4, max_body: 1 << 20 };
        let mut it = args.iter();
        while let Some(&a) = it.next() {
            let v = it.next().ok_or_else(|| format!("missing value for {}", a))?;
            match a {
                "--addr" => c.addr = v.to_string(),
                "--workers" => c.workers = v.parse().map_err(|_| "bad workers".to_string())?,
                "--max-body" => c.max_body = v.parse().map_err(|_| "bad max-body".to_string())?,
                other => return Err(format!("unknown flag {}", other)),
            }
        }
        Ok(c)
    }
}

fn main() {
    let c = Config::from_args(&["--workers", "8", "--addr", "0.0.0.0:3000"]).unwrap();
    println!("{} {} {}", c.addr, c.workers, c.max_body);
    println!("{:?}", Config::from_args(&["--workers"]).err());
    println!("{:?}", Config::from_args(&["--port", "1"]).err());
    println!("{:?}", Config::from_args(&["--workers", "x"]).err());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0.0.0.0:3000 8 1048576\nSome(\"missing value for --workers\")\nSome(\"unknown flag --port\")\nSome(\"bad workers\")"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Всё, что делают фреймворки, теперь видно: маршруты, слои, пул, лимиты, метрики."}
    >
      <div className="s-grid2">
        {([["route", "Маршруты", "404, 405, параметры"], ["wrap(handler)", "Слои", "Сквозное поведение"], ["pool · flag", "Параллелизм", "Пул и остановка"], ["bucket · tests", "Надёжность", "Лимиты и интеграционные тесты"]] as const).map(([big, t, d]) => (
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
export const SLIDES_R42 = {
  "10:42": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R42).
export const SLIDE_TITLES_R42 = {
  "10:42": [
    "Маршрутизатор и пул",
    "Маршрутизатор",
    "Параметры маршрута",
    "Слои",
    "Общее состояние",
    "CRUD-хранилище",
    "Пул потоков",
    "Остановка",
    "Token bucket",
    "Тест сервера",
    "Метрики",
    "Настройки",
    "Итоги",
  ],
};
