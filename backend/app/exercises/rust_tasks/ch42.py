"""Задачи книги «Изучаем Rust»: глава 42 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {42: [{'id': 'r42-match-route',
       'mode': 'rust',
       'title': 'Сопоставление маршрута',
       'statement': 'Напишите match_route(pattern: &str, path: &str) -> Option<BTreeMap<String, String>>: '
                    "сегменты через '/', ведущие и хвостовые '/' игнорируются. Сегмент шаблона ':имя' "
                    "захватывает один сегмент пути; последний сегмент '*имя' захватывает весь остаток пути "
                    "(сегменты через '/', может быть пустым); остальные сегменты должны совпасть дословно. "
                    "Число сегментов без '*' должно совпасть.",
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'fn match_route(pattern: &str, path: &str) -> Option<BTreeMap<String, String>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", match_route("/users/:id/posts/:post", "/users/42/posts/7/"));\n'
                 '    println!("{:?} {:?}", match_route("/users/:id", "/users"), match_route("/users/:id", '
                 '"/accounts/5"));\n'
                 '    println!("{:?} {:?}", match_route("/", "/"), match_route("/", "/x"));\n'
                 '    println!("{:?}", match_route("/static/*path", "/static/css/site/main.css"));\n'
                 '    println!("{:?} {:?}", match_route("/static/*path", "/static"), '
                 'match_route("/static/*path", "/other/a"));\n'
                 '    println!("{:?}", match_route("/a/:x/*rest", "/a/1/b/c"));\n'
                 '}\n',
       'expected': ['Some({"id": "42", "post": "7"})',
                    'None None',
                    'Some({}) None',
                    'Some({"path": "css/site/main.css"})',
                    'Some({"path": ""}) None',
                    'Some({"rest": "b/c", "x": "1"})'],
       'hint': "Разберите оба пути на сегменты и идите по шаблону: ':' — захват, '*' — хвост (return), иначе "
               '— равенство.'},
      {'id': 'r42-router',
       'mode': 'rust',
       'title': 'Маршрутизатор с 404 и 405',
       'statement': 'Дополните Router: new(), add(&mut self, method, pattern, handler) и handle(&self, '
                    'method, path) -> (u16, String): первая запись, у которой совпали метод и шаблон, '
                    'вызывает обработчик с параметрами и возвращает (200, результат). Если ни одна не '
                    'подошла, но шаблон совпал для другого метода — (405, "method not allowed"); если шаблон '
                    'не совпал нигде — (404, "not found"). Функция match_route уже написана.',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  'type Params = BTreeMap<String, String>;\n'
                  'type Handler = Box<dyn Fn(&Params) -> String>;\n'
                  '\n'
                  'fn match_route(pattern: &str, path: &str) -> Option<Params> {\n'
                  "    let segs = |s: &str| -> Vec<String> { s.split('/').filter(|x| !x.is_empty()).map(|x| "
                  'x.to_string()).collect() };\n'
                  '    let (p, q) = (segs(pattern), segs(path));\n'
                  '    if p.len() != q.len() {\n'
                  '        return None;\n'
                  '    }\n'
                  '    let mut params = Params::new();\n'
                  '    for (a, b) in p.iter().zip(q.iter()) {\n'
                  "        if let Some(name) = a.strip_prefix(':') {\n"
                  '            params.insert(name.to_string(), b.clone());\n'
                  '        } else if a != b {\n'
                  '            return None;\n'
                  '        }\n'
                  '    }\n'
                  '    Some(params)\n'
                  '}\n'
                  '\n'
                  'struct Router {\n'
                  '    routes: Vec<(String, String, Handler)>,\n'
                  '}\n'
                  '\n'
                  'impl Router {\n'
                  '    fn new() -> Router {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn add(&mut self, method: &str, pattern: &str, h: Handler) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn handle(&self, method: &str, path: &str) -> (u16, String) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut r = Router::new();\n'
                 '    r.add("GET", "/users/new", Box::new(|_| "new form".to_string()));\n'
                 '    r.add("GET", "/users/:id", Box::new(|p| format!("user {}", p["id"])));\n'
                 '    r.add("DELETE", "/users/:id", Box::new(|p| format!("deleted {}", p["id"])));\n'
                 '    r.add("GET", "/", Box::new(|_| "home".to_string()));\n'
                 '    for (m, p) in [("GET", "/users/new"), ("GET", "/users/42"), ("DELETE", "/users/7"), '
                 '("POST", "/users/7"), ("GET", "/nope"), ("GET", "/"), ("PUT", "/")] {\n'
                 '        println!("{} {} -> {:?}", m, p, r.handle(m, p));\n'
                 '    }\n'
                 '}\n',
       'expected': ['GET /users/new -> (200, "new form")',
                    'GET /users/42 -> (200, "user 42")',
                    'DELETE /users/7 -> (200, "deleted 7")',
                    'POST /users/7 -> (405, "method not allowed")',
                    'GET /nope -> (404, "not found")',
                    'GET / -> (200, "home")',
                    'PUT / -> (405, "method not allowed")'],
       'hint': 'Один проход: запоминайте, совпал ли шаблон при другом методе; результат — после цикла.'},
      {'id': 'r42-middleware',
       'mode': 'rust',
       'title': 'Цепочка слоёв',
       'statement': 'Типы: Handler = Rc<dyn Fn(&Request) -> Response>, Layer = Rc<dyn Fn(&Request, &Handler) '
                    '-> Response> (слой получает запрос и «следующий» обработчик). Напишите compose(layers: '
                    'Vec<Layer>, endpoint: Handler) -> Handler: первый слой в списке — самый внешний '
                    '(вызывается первым), последний вызывает endpoint.',
       'starter': 'use std::rc::Rc;\n'
                  '\n'
                  'struct Request {\n'
                  '    path: String,\n'
                  '    auth: Option<String>,\n'
                  '}\n'
                  '\n'
                  '#[derive(Debug, PartialEq)]\n'
                  'struct Response {\n'
                  '    status: u16,\n'
                  '    body: String,\n'
                  '}\n'
                  '\n'
                  'type Handler = Rc<dyn Fn(&Request) -> Response>;\n'
                  'type Layer = Rc<dyn Fn(&Request, &Handler) -> Response>;\n'
                  '\n'
                  'fn compose(layers: Vec<Layer>, endpoint: Handler) -> Handler {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'use std::cell::RefCell;\n'
                 '\n'
                 'fn main() {\n'
                 '    let log: Rc<RefCell<Vec<String>>> = Rc::new(RefCell::new(Vec::new()));\n'
                 '    let l1 = Rc::clone(&log);\n'
                 '    let logging: Layer = Rc::new(move |req, next| {\n'
                 '        l1.borrow_mut().push(format!("in {}", req.path));\n'
                 '        let r = next(req);\n'
                 '        l1.borrow_mut().push(format!("out {}", r.status));\n'
                 '        r\n'
                 '    });\n'
                 '    let auth: Layer = Rc::new(|req, next| {\n'
                 '        if req.auth.as_deref() == Some("secret") {\n'
                 '            next(req)\n'
                 '        } else {\n'
                 '            Response { status: 401, body: "unauthorized".to_string() }\n'
                 '        }\n'
                 '    });\n'
                 '    let l2 = Rc::clone(&log);\n'
                 '    let tag: Layer = Rc::new(move |req, next| {\n'
                 '        l2.borrow_mut().push("tag".to_string());\n'
                 '        let mut r = next(req);\n'
                 "        r.body.push('!');\n"
                 '        r\n'
                 '    });\n'
                 '    let endpoint: Handler = Rc::new(|req| Response { status: 200, body: format!("hello '
                 '{}", req.path) });\n'
                 '    let app = compose(vec![logging, auth, tag], endpoint);\n'
                 '    println!("{:?}", app(&Request { path: "/a".into(), auth: Some("secret".into()) }));\n'
                 '    println!("{:?}", app(&Request { path: "/b".into(), auth: None }));\n'
                 '    println!("{:?}", log.borrow());\n'
                 '    let bare = compose(vec![], Rc::new(|_| Response { status: 204, body: String::new() '
                 '}));\n'
                 '    println!("{:?}", bare(&Request { path: "/".into(), auth: None }));\n'
                 '}\n',
       'expected': ['Response { status: 200, body: "hello /a!" }',
                    'Response { status: 401, body: "unauthorized" }',
                    '["in /a", "tag", "out 200", "in /b", "out 401"]',
                    'Response { status: 204, body: "" }'],
       'hint': 'Оборачивайте с конца: последний слой — вокруг endpoint, предпоследний — вокруг получившегося '
               'и так далее; layer и next перемещаются в замыкание.'},
      {'id': 'r42-todo-api',
       'mode': 'rust',
       'title': 'REST-интерфейс списка дел',
       'statement': 'Хранилище Store уже написано. Напишите handle(store: &Mutex<Store>, method: &str, path: '
                    '&str, body: &str) -> (u16, String): GET /todos → (200, JSON-массив по возрастанию id: '
                    '[{"id":1,"title":"a","done":false}], пустой — []); POST /todos (тело — название без '
                    'кавычек, обрезается; пустое → (400, "empty title")) → (201, {"id":N}); GET /todos/ID → '
                    '(200, объект) или (404, "not found"); нечисловой ID → (400, "bad id"); PUT '
                    '/todos/ID/done → (200, "done") или 404; DELETE /todos/ID → (204, "") или 404. Известный '
                    'путь с другим методом — (405, "method not allowed"); неизвестный путь — (404, "not '
                    'found").',
       'starter': 'use std::collections::BTreeMap;\n'
                  'use std::sync::Mutex;\n'
                  '\n'
                  'struct Todo {\n'
                  '    title: String,\n'
                  '    done: bool,\n'
                  '}\n'
                  '\n'
                  'struct Store {\n'
                  '    next: u32,\n'
                  '    items: BTreeMap<u32, Todo>,\n'
                  '}\n'
                  '\n'
                  'impl Store {\n'
                  '    fn new() -> Store {\n'
                  '        Store { next: 1, items: BTreeMap::new() }\n'
                  '    }\n'
                  '    fn create(&mut self, title: &str) -> u32 {\n'
                  '        let id = self.next;\n'
                  '        self.next += 1;\n'
                  '        self.items.insert(id, Todo { title: title.to_string(), done: false });\n'
                  '        id\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn handle(store: &Mutex<Store>, method: &str, path: &str, body: &str) -> (u16, String) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let s = Mutex::new(Store::new());\n'
                 '    for (m, p, b) in [\n'
                 '        ("GET", "/todos", ""),\n'
                 '        ("POST", "/todos", "  write chapter "),\n'
                 '        ("POST", "/todos", "test server"),\n'
                 '        ("POST", "/todos", "   "),\n'
                 '        ("GET", "/todos/1", ""),\n'
                 '        ("PUT", "/todos/1/done", ""),\n'
                 '        ("GET", "/todos", ""),\n'
                 '        ("GET", "/todos/9", ""),\n'
                 '        ("GET", "/todos/abc", ""),\n'
                 '        ("DELETE", "/todos/2", ""),\n'
                 '        ("DELETE", "/todos/2", ""),\n'
                 '        ("PATCH", "/todos", ""),\n'
                 '        ("GET", "/todos/1/done", ""),\n'
                 '        ("GET", "/nope", ""),\n'
                 '    ] {\n'
                 '        println!("{} {} -> {:?}", m, p, handle(&s, m, p, b));\n'
                 '    }\n'
                 '}\n',
       'expected': ['GET /todos -> (200, "[]")',
                    'POST /todos -> (201, "{\\"id\\":1}")',
                    'POST /todos -> (201, "{\\"id\\":2}")',
                    'POST /todos -> (400, "empty title")',
                    'GET /todos/1 -> (200, "{\\"id\\":1,\\"title\\":\\"write chapter\\",\\"done\\":false}")',
                    'PUT /todos/1/done -> (200, "done")',
                    'GET /todos -> (200, "[{\\"id\\":1,\\"title\\":\\"write '
                    'chapter\\",\\"done\\":true},{\\"id\\":2,\\"title\\":\\"test '
                    'server\\",\\"done\\":false}]")',
                    'GET /todos/9 -> (404, "not found")',
                    'GET /todos/abc -> (400, "bad id")',
                    'DELETE /todos/2 -> (204, "")',
                    'DELETE /todos/2 -> (404, "not found")',
                    'PATCH /todos -> (405, "method not allowed")',
                    'GET /todos/1/done -> (405, "method not allowed")',
                    'GET /nope -> (404, "not found")'],
       'hint': 'Разбейте путь на сегменты и сопоставляйте срез: ["todos"], ["todos", id], ["todos", id, '
               '"done"]; блокировку берите один раз в начале.'},
      {'id': 'r42-thread-pool',
       'mode': 'rust',
       'title': 'Пул потоков',
       'statement': 'Реализуйте ThreadPool: new(n) запускает n рабочих потоков, execute(&self, f) отправляет '
                    "задание (FnOnce + Send + 'static) в общую очередь, а Drop закрывает очередь и "
                    'дожидается всех рабочих (принятые задания выполняются до конца).',
       'starter': 'use std::sync::{mpsc, Arc, Mutex};\n'
                  'use std::thread;\n'
                  '\n'
                  "type Job = Box<dyn FnOnce() + Send + 'static>;\n"
                  '\n'
                  'struct ThreadPool {\n'
                  '    workers: Vec<thread::JoinHandle<()>>,\n'
                  '    tx: Option<mpsc::Sender<Job>>,\n'
                  '}\n'
                  '\n'
                  'impl ThreadPool {\n'
                  '    fn new(n: usize) -> ThreadPool {\n'
                  '        todo!()\n'
                  '    }\n'
                  "    fn execute<F: FnOnce() + Send + 'static>(&self, f: F) {\n"
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Drop for ThreadPool {\n'
                  '    fn drop(&mut self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'use std::sync::atomic::{AtomicUsize, Ordering};\n'
                 '\n'
                 'fn main() {\n'
                 '    let done = Arc::new(AtomicUsize::new(0));\n'
                 '    let running = Arc::new(AtomicUsize::new(0));\n'
                 '    let peak = Arc::new(AtomicUsize::new(0));\n'
                 '    {\n'
                 '        let pool = ThreadPool::new(4);\n'
                 '        for _ in 0..40 {\n'
                 '            let (d, r, p) = (Arc::clone(&done), Arc::clone(&running), Arc::clone(&peak));\n'
                 '            pool.execute(move || {\n'
                 '                let now = r.fetch_add(1, Ordering::SeqCst) + 1;\n'
                 '                p.fetch_max(now, Ordering::SeqCst);\n'
                 '                std::thread::sleep(std::time::Duration::from_millis(5));\n'
                 '                r.fetch_sub(1, Ordering::SeqCst);\n'
                 '                d.fetch_add(1, Ordering::SeqCst);\n'
                 '            });\n'
                 '        }\n'
                 '    }\n'
                 '    println!("{} {}", done.load(Ordering::SeqCst), peak.load(Ordering::SeqCst) <= 4);\n'
                 '    let empty = ThreadPool::new(2);\n'
                 '    drop(empty);\n'
                 '    println!("ok");\n'
                 '}\n',
       'expected': ['40 true', 'ok'],
       'hint': 'Приёмник один — оберните его в Arc<Mutex<_>>; в Drop сначала закройте канал (take + drop), '
               'потом join.'},
      {'id': 'r42-serve-until',
       'mode': 'rust',
       'title': 'Сервер с мягкой остановкой',
       'statement': 'Напишите serve_until(listener: TcpListener, stop: Arc<AtomicBool>, handler: '
                    'fn(TcpStream)) -> usize: переведите сокет в неблокирующий режим и, пока флаг stop не '
                    'поднят, принимайте соединения (каждое передаётся в handler в этом же потоке); если '
                    'принимать нечего — спите 2 мс. Верните число обработанных соединений.',
       'starter': 'use std::net::{TcpListener, TcpStream};\n'
                  'use std::sync::atomic::AtomicBool;\n'
                  'use std::sync::Arc;\n'
                  '\n'
                  'fn serve_until(listener: TcpListener, stop: Arc<AtomicBool>, handler: fn(TcpStream)) -> '
                  'usize {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'use std::io::{Read, Write};\n'
                 'use std::net::{TcpListener, TcpStream};\n'
                 'use std::sync::atomic::{AtomicBool, Ordering};\n'
                 'use std::sync::Arc;\n'
                 'use std::thread;\n'
                 'use std::time::Duration;\n'
                 '\n'
                 'fn upper(mut s: TcpStream) {\n'
                 '    let mut buf = [0u8; 64];\n'
                 '    let n = s.read(&mut buf).unwrap();\n'
                 '    s.write_all(&buf[..n].to_ascii_uppercase()).unwrap();\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    let listener = TcpListener::bind("127.0.0.1:0").unwrap();\n'
                 '    let addr = listener.local_addr().unwrap();\n'
                 '    let stop = Arc::new(AtomicBool::new(false));\n'
                 '    let flag = Arc::clone(&stop);\n'
                 '    let server = thread::spawn(move || serve_until(listener, flag, upper));\n'
                 '    for word in ["alpha", "beta", "gamma"] {\n'
                 '        let mut c = TcpStream::connect(addr).unwrap();\n'
                 '        c.write_all(word.as_bytes()).unwrap();\n'
                 '        let mut reply = String::new();\n'
                 '        c.read_to_string(&mut reply).unwrap();\n'
                 '        println!("{}", reply);\n'
                 '    }\n'
                 '    thread::sleep(Duration::from_millis(20));\n'
                 '    stop.store(true, Ordering::SeqCst);\n'
                 '    println!("handled {}", server.join().unwrap());\n'
                 '    let l2 = TcpListener::bind("127.0.0.1:0").unwrap();\n'
                 '    let stopped = Arc::new(AtomicBool::new(true));\n'
                 '    println!("handled {}", serve_until(l2, stopped, upper));\n'
                 '}\n',
       'expected': ['ALPHA', 'BETA', 'GAMMA', 'handled 3', 'handled 0'],
       'hint': 'accept() неблокирующего сокета возвращает ошибку WouldBlock, если соединений нет; принятому '
               'потоку верните блокирующий режим.'},
      {'id': 'r42-rate-limiter',
       'mode': 'rust',
       'title': 'Ограничитель по клиентам',
       'statement': 'Реализуйте RateLimiter: new(capacity: f64, rate: f64) (у каждого нового ключа ведро '
                    'полное; last = момент первого обращения) и allow(&mut self, key: &str, now: f64) -> '
                    'bool: ведро пополняется на (now − last) · rate, не больше capacity; запрос стоит один '
                    'жетон. Клиенты не влияют друг на друга. Время приходит неубывающим для одного ключа.',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'struct RateLimiter {\n'
                  '    capacity: f64,\n'
                  '    rate: f64,\n'
                  '    buckets: HashMap<String, (f64, f64)>,\n'
                  '}\n'
                  '\n'
                  'impl RateLimiter {\n'
                  '    fn new(capacity: f64, rate: f64) -> RateLimiter {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn allow(&mut self, key: &str, now: f64) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut rl = RateLimiter::new(2.0, 0.5);\n'
                 '    let calls = [("a", 0.0), ("a", 0.0), ("a", 0.0), ("b", 0.0), ("a", 1.0), ("a", 2.0), '
                 '("a", 2.0), ("b", 0.5), ("b", 4.0), ("b", 4.0), ("b", 4.0)];\n'
                 '    let r: Vec<String> = calls.iter().map(|&(k, t)| format!("{}@{}={}", k, t, rl.allow(k, '
                 't))).collect();\n'
                 '    println!("{}", r.join(" "));\n'
                 '    let mut hot = RateLimiter::new(1.0, 1000.0);\n'
                 '    let allowed = (0..100_000).filter(|&i| hot.allow(&format!("c{}", i % 10), i as f64 / '
                 '1000.0)).count();\n'
                 '    println!("{}", allowed);\n'
                 '}\n',
       'expected': ['a@0=true a@0=true a@0=false b@0=true a@1=false a@2=true a@2=false b@0.5=true b@4=true '
                    'b@4=true b@4=false',
                    '100000'],
       'hint': 'Состояние ключа — пара (жетоны, последнее время); обновляйте её и при отказе (жетоны '
               'пополнились).'},
      {'id': 'r42-histogram',
       'mode': 'rust',
       'title': 'Гистограмма задержек',
       'statement': 'Реализуйте Histogram::new(bounds: &[u64]) (верхние границы корзин в мс по возрастанию), '
                    'observe(&mut self, ms: u64) и render(&self, name: &str) -> String в стиле Prometheus: '
                    'для каждой границы строка name_bucket{le="B"} N, где N — число наблюдений ≤ B '
                    '(накопительно); затем name_bucket{le="+Inf"} (все наблюдения), name_count и name_sum. '
                    'Строки разделены \\n, без завершающего.',
       'starter': 'struct Histogram {\n'
                  '    bounds: Vec<u64>,\n'
                  '    counts: Vec<u64>,\n'
                  '    total: u64,\n'
                  '    sum: u64,\n'
                  '}\n'
                  '\n'
                  'impl Histogram {\n'
                  '    fn new(bounds: &[u64]) -> Histogram {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn observe(&mut self, ms: u64) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn render(&self, name: &str) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut h = Histogram::new(&[10, 50, 100]);\n'
                 '    for ms in [3, 10, 11, 49, 50, 99, 250, 1000] {\n'
                 '        h.observe(ms);\n'
                 '    }\n'
                 '    println!("{}", h.render("latency_ms"));\n'
                 '    println!("{}", Histogram::new(&[]).render("x"));\n'
                 '}\n',
       'expected': ['latency_ms_bucket{le="10"} 2',
                    'latency_ms_bucket{le="50"} 5',
                    'latency_ms_bucket{le="100"} 6',
                    'latency_ms_bucket{le="+Inf"} 8',
                    'latency_ms_count 8',
                    'latency_ms_sum 1472',
                    'x_bucket{le="+Inf"} 0',
                    'x_count 0',
                    'x_sum 0'],
       'hint': 'Накопительные корзины: наблюдение увеличивает счётчик каждой границы, которая не меньше '
               'значения.'},
      {'id': 'r42-parse-args',
       'mode': 'rust',
       'title': 'Разбор командной строки',
       'statement': 'Напишите parse_args(args: &[&str]) -> Result<Options, String> (Options дана): '
                    "'--name=value' и '--name value' → options[name] = value; '--flag' без значения "
                    "(следующий элемент начинается с '-' или это конец списка) → flags содержит flag; '-v', "
                    "'-vv', '-vvv' → verbose += число букв v; '--' — всё остальное позиционные аргументы; "
                    'прочее — позиционные. Ошибки: \'-x\' с буквой, не v → Err("unknown option -x"); '
                    '\'--=v\' → Err("empty option name").',
       'starter': 'use std::collections::BTreeMap;\n'
                  '\n'
                  '#[derive(Debug, Default, PartialEq)]\n'
                  'struct Options {\n'
                  '    options: BTreeMap<String, String>,\n'
                  '    flags: Vec<String>,\n'
                  '    verbose: u32,\n'
                  '    positional: Vec<String>,\n'
                  '}\n'
                  '\n'
                  'fn parse_args(args: &[&str]) -> Result<Options, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", parse_args(&["--port=8080", "--host", "localhost", "-vv", "--debug", '
                 '"file.txt", "-v", "--", "--not-an-option", "-x"]));\n'
                 '    println!("{:?}", parse_args(&[]));\n'
                 '    println!("{:?}", parse_args(&["--a", "--b", "val", "pos"]));\n'
                 '    println!("{:?} {:?} {:?}", parse_args(&["-x"]), parse_args(&["--=v"]), '
                 'parse_args(&["--"]));\n'
                 '    println!("{:?}", parse_args(&["-"]));\n'
                 '}\n',
       'expected': ['Ok(Options { options: {"debug": "file.txt", "host": "localhost", "port": "8080"}, '
                    'flags: [], verbose: 3, positional: ["--not-an-option", "-x"] })',
                    'Ok(Options { options: {}, flags: [], verbose: 0, positional: [] })',
                    'Ok(Options { options: {"b": "val"}, flags: ["a"], verbose: 0, positional: ["pos"] })',
                    'Err("unknown option -x") Err("empty option name") Ok(Options { options: {}, flags: [], '
                    'verbose: 0, positional: [] })',
                    'Ok(Options { options: {}, flags: [], verbose: 0, positional: ["-"] })'],
       'hint': 'Один цикл с индексом: у «--имя» значение берётся из следующего элемента, если он не '
               "начинается с '-'."}]}
