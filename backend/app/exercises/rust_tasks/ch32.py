"""Задачи книги «Изучаем Rust»: глава 32 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {32: [{'id': 'r32-desugar',
       'mode': 'rust',
       'title': 'Десахаринг async fn',
       'statement': 'Напишите функцию double(x: u32) -> impl Future<Output = u32> без ключевого слова async '
                    'в сигнатуре: тело — async move-блок, возвращающий x * 2.',
       'starter': 'use std::future::Future;\n'
                  '\n'
                  'fn double(x: u32) -> impl Future<Output = u32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    println!("{}", double(21).await);\n'
                 '    let f = double(5);\n'
                 '    println!("{}", f.await + double(1).await);\n'
                 '}\n',
       'hint': 'async fn f(x) -> T ≈ fn f(x) -> impl Future<Output = T> { async move { … } }.',
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['42', '12']},
      {'id': 'r32-lifetime-future',
       'mode': 'rust',
       'title': 'Время жизни фьючера',
       'statement': "Напишите fn longer<'a>(a: &'a str, b: &'a str) -> impl Future<Output = &'a str> + 'a: "
                    'async-блок возвращает более длинную строку (по числу символов; при равенстве — a).',
       'starter': 'use std::future::Future;\n'
                  '\n'
                  "fn longer<'a>(a: &'a str, b: &'a str) -> impl Future<Output = &'a str> + 'a {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    let x = String::from("привет");\n'
                 '    let y = String::from("мир");\n'
                 '    println!("{}", longer(&x, &y).await);\n'
                 '    println!("{}", longer("ab", "cd").await);\n'
                 '}\n',
       'hint': "Время жизни 'a входит в тип фьючера.",
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['привет', 'ab']},
      {'id': 'r32-block-question',
       'mode': 'rust',
       'title': '? в async-блоке',
       'statement': 'Выполните async-блок, разбирающий «12» и «30» в числа с ? и возвращающий их сумму. Тип '
                    'ошибки блока нужно указать: Ok::<i32, std::num::ParseIntError>(…). Напечатайте '
                    '«Ok(42)»; затем то же для «12» и «x» — «true» (признак ошибки).\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'Ok(42)\n'
                    'true',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Ok::<T, E>(…) подсказывает компилятору тип ошибки.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['Ok(42)', 'true']},
      {'id': 'r32-ref-across-await',
       'mode': 'rust',
       'title': 'Ссылка через .await',
       'statement': 'Напишите async fn sum_with_yield(v: &[i32]) -> i32: суммируйте элементы, на каждом шаге '
                    'делая tokio::task::yield_now().await (ссылка на срез живёт через .await).',
       'starter': 'async fn sum_with_yield(v: &[i32]) -> i32 {\n    todo!()\n}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    let v = vec![1, 2, 3, 4];\n'
                 '    println!("{}", sum_with_yield(&v).await);\n'
                 '    println!("{}", sum_with_yield(&v[1..3]).await);\n'
                 '    println!("{}", sum_with_yield(&[]).await);\n'
                 '}\n',
       'hint': 'Срез-параметр — ссылка; фьючер живёт, пока она действительна.',
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['10', '5', '0']},
      {'id': 'r32-box-future',
       'mode': 'rust',
       'title': 'BoxFuture',
       'statement': "Напишите fn make(n: u32) -> BoxFuture<'static, u32> (futures::future::BoxFuture): "
                    'фьючер, который засыпает n мс и возвращает n·n. Затем driver собирает вектор таких '
                    'фьючеров и выполняет join_all.',
       'starter': 'use futures::future::BoxFuture;\n'
                  '\n'
                  "fn make(n: u32) -> BoxFuture<'static, u32> {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    let v: Vec<BoxFuture<u32>> = (1..=4).map(make).collect();\n'
                 '    println!("{:?}", futures::future::join_all(v).await);\n'
                 '}\n',
       'hint': 'Box::pin(async move { … }) подходит под BoxFuture.',
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['[1, 4, 9, 16]']},
      {'id': 'r32-pin-new',
       'mode': 'rust',
       'title': 'Pin::new для Unpin',
       'statement': 'Напишите poll_ready_now<F: Future + Unpin>(f: &mut F) -> Option<F::Output>: один опрос '
                    'с Waker::noop() через Pin::new(f); None при Pending.',
       'starter': 'use std::future::Future;\n'
                  'use std::pin::Pin;\n'
                  'use std::task::{Context, Poll, Waker};\n'
                  '\n'
                  'fn poll_ready_now<F: Future + Unpin>(f: &mut F) -> Option<F::Output> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    let mut r = futures::future::ready(5);\n'
                 '    println!("{:?}", poll_ready_now(&mut r));\n'
                 '    let mut p = futures::future::pending::<i32>();\n'
                 '    println!("{:?}", poll_ready_now(&mut p));\n'
                 '}\n',
       'hint': 'ready() и pending() из futures — Unpin.',
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['Some(5)', 'None']},
      {'id': 'r32-pin-select-loop',
       'mode': 'rust',
       'title': 'pin! и повторный select!',
       'statement': 'Закрепите макросом tokio::pin! долгий фьючер (сон 100 мс, возвращает «готово») и в '
                    'цикле select! ждите либо его (&mut fut), либо тик interval(30 мс). Считайте тики, пока '
                    'не придёт «готово». Напечатайте «готово» и «тиков>=2: true».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'готово\n'
                    'тиков>=2: true',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': '&mut fut в select! не отменяет фьючер на повторных итерациях.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['готово', 'тиков>=2: true']},
      {'id': 'r32-pin-mut-api',
       'mode': 'rust',
       'title': 'Pin<&mut T>',
       'statement': 'Структура Counter { n: u32 } (Unpin). Напишите fn bump(mut p: Pin<&mut Counter>): '
                    'увеличить n на 1 через p.as_mut().get_mut().',
       'starter': 'use std::pin::Pin;\n'
                  '\n'
                  'struct Counter {\n'
                  '    n: u32,\n'
                  '}\n'
                  '\n'
                  'fn bump(mut p: Pin<&mut Counter>) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    let mut c = Counter { n: 0 };\n'
                 '    bump(Pin::new(&mut c));\n'
                 '    bump(Pin::new(&mut c));\n'
                 '    let mut b = Box::pin(Counter { n: 10 });\n'
                 '    bump(b.as_mut());\n'
                 '    println!("{} {}", c.n, b.n);\n'
                 '}\n',
       'hint': 'get_mut доступен только для Unpin-типов.',
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['2 11']},
      {'id': 'r32-poll-fn',
       'mode': 'rust',
       'title': 'poll_fn',
       'statement': "Напишите fn countdown(mut n: u32) -> impl Future<Output = &'static str> через "
                    'std::future::poll_fn: пока n > 0 — уменьшить, wake_by_ref и Pending; затем '
                    'Ready("пуск"). Driver считает число опросов.',
       'starter': 'use std::future::{poll_fn, Future};\n'
                  'use std::task::Poll;\n'
                  '\n'
                  "fn countdown(mut n: u32) -> impl Future<Output = &'static str> {\n"
                  '    poll_fn(move |cx| {\n'
                  '        todo!()\n'
                  '    })\n'
                  '}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    println!("{}", countdown(5).await);\n'
                 '    use std::sync::atomic::{AtomicUsize, Ordering};\n'
                 '    static POLLS: AtomicUsize = AtomicUsize::new(0);\n'
                 '    let f = std::future::poll_fn(|cx| { POLLS.fetch_add(1, Ordering::SeqCst); '
                 'cx.waker().wake_by_ref(); if POLLS.load(Ordering::SeqCst) < 4 { std::task::Poll::Pending } '
                 'else { std::task::Poll::Ready(()) } });\n'
                 '    f.await;\n'
                 '    println!("{}", POLLS.load(Ordering::SeqCst));\n'
                 '}\n',
       'hint': 'poll_fn превращает замыкание в Future.',
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['пуск', '4']},
      {'id': 'r32-pending-timeout',
       'mode': 'rust',
       'title': 'ready и pending',
       'statement': 'Покажите: tokio::time::timeout(50 мс) над std::future::pending::<u8>() даёт Err — '
                    'напечатайте «таймаут»; над std::future::ready(7) даёт Ok(7) — «7».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'таймаут\n'
                    '7',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'pending никогда не завершается; ready завершается сразу.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['таймаут', '7']},
      {'id': 'r32-into-future',
       'mode': 'rust',
       'title': 'IntoFuture',
       'statement': 'Структура Request { url: String } реализует std::future::IntoFuture так, чтобы '
                    'Request::new("x").await возвращал «ответ от x» (Output = String; IntoFuture = '
                    'Pin<Box<dyn Future<Output = String>>>; внутри — sleep 5 мс).',
       'starter': 'use std::future::{Future, IntoFuture};\n'
                  'use std::pin::Pin;\n'
                  '\n'
                  'struct Request {\n'
                  '    url: String,\n'
                  '}\n'
                  '\n'
                  'impl Request {\n'
                  '    fn new(u: &str) -> Request {\n'
                  '        Request { url: u.to_string() }\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl IntoFuture for Request {\n'
                  '    type Output = String;\n'
                  '    type IntoFuture = Pin<Box<dyn Future<Output = String>>>;\n'
                  '    fn into_future(self) -> Self::IntoFuture {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    println!("{}", Request::new("a.ru").await);\n'
                 '    let (x, y) = tokio::join!(Request::new("1"), Request::new("2"));\n'
                 '    println!("{} / {}", x, y);\n'
                 '}\n',
       'hint': 'await вызывает into_future для типа, реализующего IntoFuture.',
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['ответ от a.ru', 'ответ от 1 / ответ от 2']},
      {'id': 'r32-async-closure',
       'mode': 'rust',
       'title': 'Async-замыкание',
       'statement': 'Напишите async fn apply_all(items: &[i32], f: impl AsyncFn(i32) -> i32) -> Vec<i32>: '
                    'применить f к каждому элементу последовательно (с .await). В driver передаются '
                    'async-замыкания (Rust ≥ 1.85).',
       'starter': 'async fn apply_all(items: &[i32], f: impl AsyncFn(i32) -> i32) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    let k = 10;\n'
                 '    let r = apply_all(&[1, 2, 3], async |x| {\n'
                 '        tokio::task::yield_now().await;\n'
                 '        x * k\n'
                 '    })\n'
                 '    .await;\n'
                 '    println!("{:?}", r);\n'
                 '    println!("{:?}", apply_all(&[], async |x| x).await);\n'
                 '}\n',
       'hint': 'Ограничение impl AsyncFn(i32) -> i32; вызов f(x).await.',
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['[10, 20, 30]', '[]']},
      {'id': 'r32-closure-future',
       'mode': 'rust',
       'title': 'Замыкание, возвращающее фьючер',
       'statement': 'Напишите fn make_adder(k: i32) -> impl Fn(i32) -> Pin<Box<dyn Future<Output = i32>>>: '
                    'замыкание, которое для x возвращает упакованный фьючер x + k (после yield_now).',
       'starter': 'use std::future::Future;\n'
                  'use std::pin::Pin;\n'
                  '\n'
                  'fn make_adder(k: i32) -> impl Fn(i32) -> Pin<Box<dyn Future<Output = i32>>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    let add5 = make_adder(5);\n'
                 '    println!("{}", add5(1).await);\n'
                 '    println!("{}", add5(10).await);\n'
                 '    let r = futures::future::join_all((0..3).map(|i| add5(i))).await;\n'
                 '    println!("{:?}", r);\n'
                 '}\n',
       'hint': 'Замыкание move, внутри — Box::pin(async move { … }).',
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['6', '15', '[5, 6, 7]']},
      {'id': 'r32-spawn-arc',
       'mode': 'rust',
       'title': 'Данные для задач: Arc',
       'statement': 'Разделите вектор 1..=1000 на 4 части (по 250), посчитайте сумму каждой в отдельной '
                    'задаче spawn (данные — Arc<Vec<u64>>, диапазон — копия индексов), сложите результаты: '
                    '500500.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '500500',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Arc::clone в каждую задачу; async move забирает клон.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['500500']},
      {'id': 'r32-fix-static',
       'mode': 'rust',
       'title': "Исправьте: 'static в spawn",
       'statement': 'Программа не собирается: задача spawn использует ссылку на локальную переменную. '
                    'Исправьте так, чтобы она печатала «длина 6».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'длина 6',
       'starter': '#[tokio::main]\n'
                  'async fn main() {\n'
                  '    let s = String::from("привет");\n'
                  '    let h = tokio::spawn(async {\n'
                  '        println!("длина {}", s.chars().count());\n'
                  '    });\n'
                  '    h.await.unwrap();\n'
                  '}\n',
       'driver': '',
       'hint': 'Добавьте move и отдайте строку в задачу.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['длина 6']},
      {'id': 'r32-fix-send-guard',
       'mode': 'rust',
       'title': 'Исправьте: guard через .await',
       'statement': 'Программа не собирается: std::sync::MutexGuard удерживается через .await, и фьючер '
                    'перестаёт быть Send. Исправьте (освободите guard до .await), чтобы напечатать «счётчик '
                    '3».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'счётчик 3',
       'starter': 'use std::sync::{Arc, Mutex};\n'
                  '\n'
                  '#[tokio::main]\n'
                  'async fn main() {\n'
                  '    let c = Arc::new(Mutex::new(0));\n'
                  '    let c2 = c.clone();\n'
                  '    tokio::spawn(async move {\n'
                  '        for _ in 0..3 {\n'
                  '            let mut g = c2.lock().unwrap();\n'
                  '            *g += 1;\n'
                  '            tokio::time::sleep(std::time::Duration::from_millis(5)).await;\n'
                  '        }\n'
                  '    })\n'
                  '    .await\n'
                  '    .unwrap();\n'
                  '    println!("счётчик {}", c.lock().unwrap());\n'
                  '}\n',
       'driver': '',
       'hint': 'Заключите lock() в отдельный блок { … } перед .await.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['счётчик 3']},
      {'id': 'r32-fix-rc',
       'mode': 'rust',
       'title': 'Исправьте: Rc в задаче',
       'statement': 'Rc не Send, поэтому spawn не принимает такую задачу. Замените Rc на Arc, чтобы '
                    'напечатать «сумма 6».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'сумма 6',
       'starter': 'use std::rc::Rc;\n'
                  '\n'
                  '#[tokio::main]\n'
                  'async fn main() {\n'
                  '    let data = Rc::new(vec![1, 2, 3]);\n'
                  '    let d = data.clone();\n'
                  '    let s = tokio::spawn(async move { d.iter().sum::<i32>() }).await.unwrap();\n'
                  '    println!("сумма {}", s);\n'
                  '}\n',
       'driver': '',
       'hint': 'Arc вместо Rc: счётчик ссылок атомарный.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['сумма 6']},
      {'id': 'r32-async-trait-static',
       'mode': 'rust',
       'title': 'async fn в трейте',
       'statement': 'Трейт Store { async fn get(&self, k: &str) -> Option<String>; }. Реализуйте для '
                    'MemStore(HashMap<String, String>): после yield_now вернуть значение (клон) или None. '
                    'Функция lookup(s: &impl Store, k: &str) -> String возвращает значение или «нет».',
       'starter': 'use std::collections::HashMap;\n'
                  '\n'
                  'trait Store {\n'
                  '    async fn get(&self, k: &str) -> Option<String>;\n'
                  '}\n'
                  '\n'
                  'struct MemStore(HashMap<String, String>);\n'
                  '\n'
                  'impl Store for MemStore {\n'
                  '    async fn get(&self, k: &str) -> Option<String> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'async fn lookup(s: &impl Store, k: &str) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    let mut m = HashMap::new();\n'
                 '    m.insert(String::from("a"), String::from("1"));\n'
                 '    let s = MemStore(m);\n'
                 '    println!("{} {}", lookup(&s, "a").await, lookup(&s, "b").await);\n'
                 '}\n',
       'hint': 'async fn в трейте — статическая диспетчеризация, вызов через impl Store.',
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['1 нет']},
      {'id': 'r32-async-trait-dyn',
       'mode': 'rust',
       'title': 'Динамические асинхронные трейты',
       'statement': "Трейт Source { fn name(&self) -> String; fn get(&self) -> BoxFuture<'_, u32>; } "
                    '(futures::future::BoxFuture). Реализуйте для Fast (сразу 1) и Slow (sleep 10 мс, затем '
                    '2). Функция total(v: &[Box<dyn Source>]) -> u32 — сумма get().await.',
       'starter': 'use futures::future::BoxFuture;\n'
                  '\n'
                  'trait Source {\n'
                  '    fn name(&self) -> String;\n'
                  "    fn get(&self) -> BoxFuture<'_, u32>;\n"
                  '}\n'
                  '\n'
                  'struct Fast;\n'
                  'struct Slow;\n'
                  '\n'
                  'impl Source for Fast {\n'
                  '    fn name(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  "    fn get(&self) -> BoxFuture<'_, u32> {\n"
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Source for Slow {\n'
                  '    fn name(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  "    fn get(&self) -> BoxFuture<'_, u32> {\n"
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'async fn total(v: &[Box<dyn Source>]) -> u32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    let v: Vec<Box<dyn Source>> = vec![Box::new(Fast), Box::new(Slow), Box::new(Fast)];\n'
                 '    println!("{}", total(&v).await);\n'
                 '    println!("{}", v.iter().map(|s| s.name()).collect::<Vec<_>>().join(","));\n'
                 '}\n',
       'hint': "BoxFuture<'_, u32> позволяет использовать dyn Source.",
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['4', 'fast,slow,fast']},
      {'id': 'r32-async-recursion',
       'mode': 'rust',
       'title': 'Асинхронная рекурсия по дереву',
       'statement': 'Объявлено дерево enum Tree { Leaf(u32), Node(Vec<Tree>) }. Напишите fn sum(t: &Tree) -> '
                    "BoxFuture<'_, u32> — рекурсивная сумма листьев (на каждом узле yield_now).",
       'starter': 'use futures::future::BoxFuture;\n'
                  '\n'
                  'enum Tree {\n'
                  '    Leaf(u32),\n'
                  '    Node(Vec<Tree>),\n'
                  '}\n'
                  '\n'
                  "fn sum(t: &Tree) -> BoxFuture<'_, u32> {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    let t = Tree::Node(vec![Tree::Leaf(1), Tree::Node(vec![Tree::Leaf(2), Tree::Leaf(3)]), '
                 'Tree::Leaf(4)]);\n'
                 '    println!("{}", sum(&t).await);\n'
                 '    println!("{}", sum(&Tree::Node(vec![])).await);\n'
                 '}\n',
       'hint': 'Рекурсивный вызов оборачивается в Box::pin.',
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['10', '0']},
      {'id': 'r32-cancel-guard',
       'mode': 'rust',
       'title': 'Учёт отмен',
       'statement': 'Структура Guard увеличивает общий счётчик в Drop, если задача не завершилась (флаг done '
                    '== false). Запустите 5 задач с timeout 20 мс: у трёх сон 100 мс, у двух — 5 мс. '
                    'Напечатайте число отменённых «3».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '3',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Drop срабатывает при отмене по таймауту.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['3']},
      {'id': 'r32-cancel-safe-recv',
       'mode': 'rust',
       'title': 'recv безопасен к отмене',
       'statement': 'В select! по mpsc::Receiver::recv и таймеру (sleep 5 мс в цикле) отправитель шлёт числа '
                    '1…10 с паузой 2 мс. Убедитесь, что все 10 сообщений получены, несмотря на отмену recv '
                    'при срабатывании таймера: напечатайте сумму «55».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '55',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'recv безопасен к отмене: сообщение не теряется.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['55']},
      {'id': 'r32-abort-cleanup',
       'mode': 'rust',
       'title': 'Очистка при abort',
       'statement': 'Задача держит Guard, который в Drop печатает «очистка». Запустите задачу (спит 1 с), '
                    'через 20 мс abort() и дождитесь результата. Ожидается: «старт», «очистка», «отменена: '
                    'true».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'старт\n'
                    'очистка\n'
                    'отменена: true',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'abort уничтожает фьючер: Drop выполняется.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['старт', 'очистка', 'отменена: true']},
      {'id': 'r32-join-all-box',
       'mode': 'rust',
       'title': 'Фьючеры разных типов в цикле',
       'statement': 'В цикле создайте три фьючера разных async-блоков (число, строка длины, булево) как '
                    'Pin<Box<dyn Future<Output = String>>> (результат превращайте в String), выполните '
                    'join_all и напечатайте «["42", "3", "true"]».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '["42", "3", "true"]',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Box::pin приводит разные async-блоки к одному типу.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['["42", "3", "true"]']},
      {'id': 'r32-future-ext',
       'mode': 'rust',
       'title': 'Цепочка FutureExt',
       'statement': 'С помощью futures::FutureExt соберите цепочку: ready(3).map(|x| x + 1).then(|x| async '
                    'move { x * 10 }).boxed(); напечатайте результат 40. Затем lazy-фьючер '
                    '(futures::future::lazy) вернёт «лениво»: напечатайте его.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '40\n'
                    'лениво',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'FutureExt: map, then, boxed.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['40', 'лениво']},
      {'id': 'r32-shared',
       'mode': 'rust',
       'title': 'Shared',
       'statement': 'Создайте фьючер, который увеличивает глобальный счётчик AtomicUsize и возвращает '
                    '«результат»; превратите его в Shared (FutureExt::shared) и дождитесь двумя клонами '
                    'одновременно через join!. Напечатайте оба результата и счётчик: счётчик должен быть 1.\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'результат результат\n'
                    '1',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'Shared выполняет внутренний фьючер один раз и раздаёт результат клонам.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['результат результат', '1']},
      {'id': 'r32-select-future',
       'mode': 'rust',
       'title': 'futures::future::select',
       'statement': 'С помощью futures::future::select (функция, не макрос) определите, какой из двух '
                    'фьючеров (сон 50 и 10 мс) завершился первым. Напечатайте «второй»; затем дождитесь и '
                    'оставшегося — напечатайте «оба готовы».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'второй\n'
                    'оба готовы',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'select возвращает Either и «остаток» — неготовый фьючер.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['второй', 'оба готовы']},
      {'id': 'r32-try-join-all',
       'mode': 'rust',
       'title': 'try_join_all',
       'statement': 'futures::future::try_join_all: три фьючера с Result<u32, String>: Ok(1), Ok(2), Ok(3) — '
                    '«Ok([1, 2, 3])»; затем замените средний на Err("сбой") — получите «Err("сбой")».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    'Ok([1, 2, 3])\n'
                    'Err("сбой")',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'try_join_all собирает Ok в вектор или возвращает первую ошибку.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['Ok([1, 2, 3])', 'Err("сбой")']},
      {'id': 'r32-buffered',
       'mode': 'rust',
       'title': 'Ограниченная параллельность',
       'statement': 'stream::iter(0..8).map(|i| work(i)).buffered(3): work увеличивает счётчик «в работе», '
                    'спит 10 мс, уменьшает и запоминает максимум. Напечатайте результаты по порядку [0, 1, '
                    '4, 9, 16, 25, 36, 49] и «макс одновременных<=3: true».\n'
                    '\n'
                    'Ожидаемый вывод:\n'
                    '[0, 1, 4, 9, 16, 25, 36, 49]\n'
                    'макс одновременных<=3: true',
       'starter': '#[tokio::main]\nasync fn main() {\n    // ваш код\n}\n',
       'driver': '',
       'hint': 'buffered(n) сохраняет порядок; buffer_unordered(n) — по готовности.',
       'standalone': True,
       'crates': ['tokio'],
       'expected': ['[0, 1, 4, 9, 16, 25, 36, 49]', 'макс одновременных<=3: true']},
      {'id': 'r32-size-compare',
       'mode': 'rust',
       'title': 'Размеры фьючеров',
       'statement': 'Напишите sizes() -> (usize, usize, usize): size_of_val трёх async-блоков: пустого '
                    '(async {}), держащего через .await массив [0u8; 512] и такого же, но хранящего массив в '
                    'Box (vec![0u8; 512] в куче). Проверьте: первый < 64, второй ≥ 512, третий < 128.',
       'starter': 'fn sizes() -> (usize, usize, usize) {\n    todo!()\n}\n',
       'driver': '#[tokio::main]\n'
                 'async fn main() {\n'
                 '    let (a, b, c) = sizes();\n'
                 '    println!("{} {} {}", a < 64, b >= 512, c < 128);\n'
                 '}\n',
       'hint': 'Вектор хранит данные в куче, в автомате — только три слова.',
       'standalone': False,
       'crates': ['tokio'],
       'expected': ['true true true']}]}
