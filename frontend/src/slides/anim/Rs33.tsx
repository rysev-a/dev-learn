import { scene } from "./alg.tsx";
import { Box, arrow, rs } from "./rs.tsx";

/* Глава 33 книги «Изучаем Rust»: Tokio — рантайм, #[tokio::main] и spawn. */

const pair = (a: string, b: string, ca = "m", cb = "g", y = 60) => [
  Box("pa", 90, y, 130, 34, a, ca, { size: 10 }),
  Box("pb", 270, y, 130, 34, b, cb, { size: 10 }),
];
const row = (pre: string, items: (string|number)[], c = "g", y = 66, size = 10.5) =>
  items.map((t: string|number, i: number) =>
    Box(`${pre}${i}`, 50 + i * 86, y, 76, 30, t, c, { size }),
  );

// 1. Введение
export const V01 = scene({
  labels: ["Из чего состоит", "Флаги", "full"],
  caption: [
    "Планировщик задач, драйвер I/O, таймеры, пул блокирующих задач",
    "Флаги: rt, rt-multi-thread, macros, time, net, io-util, fs, sync, signal, process",
    'В учебных примерах — features = ["full"]; в проектах — точнее, чтобы сократить сборку',
  ],
  frames: [
    [...row("a", ["планировщик", "I/O", "таймеры", "blocking"], "b", 66, 9)],
    [...row("a", ["rt", "time", "net", "sync"], "g")],
    [
      rs("c", 20, 50, ['tokio = { version = "1", features = ["full"] }'], [0], {
        w: 340,
        size: 9.5,
        lh: 28,
      }),
    ],
  ],
});

// 2. #[tokio::main]
export const V02 = scene({
  labels: ["Макрос", "Параметры", "#[tokio::test]"],
  caption: [
    "async fn main() обычной главной быть не может: макрос создаёт рантайм и вызывает block_on",
    'flavor = "current_thread" | "multi_thread", worker_threads = N, start_paused = true',
    "#[tokio::test] делает то же для каждого теста; по умолчанию — однопоточный рантайм",
  ],
  frames: [
    [
      rs("c", 20, 40, ["#[tokio::main]", "async fn main() { … }"], [0], {
        w: 340,
        size: 12,
        lh: 26,
      }),
    ],
    [
      rs(
        "c",
        20,
        40,
        ['#[tokio::main(flavor = "multi_thread", worker_threads = 4)]'],
        [0],
        { w: 340, size: 8.5, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["#[tokio::test]", "async fn works() { assert_eq!(f().await, 5); }"],
        [0],
        { w: 340, size: 10, lh: 28 },
      ),
    ],
  ],
});

// 3. Типы рантайма
export const V03 = scene({
  labels: ["multi_thread", "Work-stealing", "current_thread"],
  caption: [
    "Пул рабочих потоков (по числу ядер); у каждого локальная очередь задач",
    "Пустой поток крадёт задачи у соседей; слот LIFO для последней разбуженной задачи",
    "Один поток: проще, предсказуемее, без Send; для тестов и небольших утилит",
  ],
  frames: [
    [
      ...[0, 1, 2, 3].map((i) =>
        Box(`t${i}`, 60 + i * 80, 66, 66, 34, `поток ${i + 1}`, "g", {
          size: 10,
        }),
      ),
    ],
    [
      Box("a", 90, 60, 130, 34, "поток 1: пусто", "y", { size: 10 }),
      arrow("e", 156, 60, 204, 60, "g"),
      Box("b", 270, 60, 130, 34, "поток 2: 5 задач", "b", { size: 10 }),
    ],
    [Box("a", 180, 66, 200, 40, "один поток, все задачи", "g", { size: 12 })],
  ],
});

// 4. Builder и Handle
export const V04 = scene({
  labels: ["Builder", "Handle", "block_on"],
  caption: [
    'Builder::new_multi_thread().worker_threads(4).thread_name("w").enable_all().build()',
    "Handle::current() — лёгкая ссылка на рантайм: запуск задач из обычных потоков",
    "rt.block_on(fut) запускает фьючер в текущем потоке; drop(rt) отменяет задачи на ближайшем .await",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        30,
        [
          "let rt = Builder::new_multi_thread()",
          "    .worker_threads(4)",
          "    .enable_all()",
          "    .build()?;",
        ],
        [1, 2],
        { w: 340, size: 10.5, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "let h = Handle::current();",
          "std::thread::spawn(move || { h.spawn(async { … }); });",
        ],
        [0],
        { w: 340, size: 9, lh: 28 },
      ),
    ],
    [
      rs("c", 20, 50, ["let r = rt.block_on(async { 1 + 1 });"], [0], {
        w: 340,
        size: 11,
        lh: 28,
      }),
    ],
  ],
});

// 5. spawn
export const V05 = scene({
  labels: ["spawn → JoinHandle", "Send + 'static", "JoinError"],
  caption: [
    "tokio::spawn(fut) запускает задачу и возвращает JoinHandle<T>; выброшенный хэндл — задача продолжает работу",
    "Фьючер обязан быть Send + 'static: всё, что в нём, принадлежит ему",
    ".await хэндла → Result<T, JoinError>: паника в задаче изолирована (is_panic), отмена — is_cancelled; abort(), is_finished()",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ["let h = tokio::spawn(async { 5 });", "let v = h.await?;"],
        [0],
        { w: 340, size: 11, lh: 28 },
      ),
    ],
    [...pair("Send", "'static", "b", "b")],
    [
      rs(
        "c",
        20,
        40,
        [
          "match h.await {",
          "    Ok(v) => …,",
          "    Err(e) if e.is_panic() => …,",
          "    Err(e) => …,   // is_cancelled",
          "}",
        ],
        [2],
        { w: 340, size: 9.5, lh: 20 },
      ),
    ],
  ],
});

// 6. JoinSet
export const V06 = scene({
  labels: ["Набор задач", "join_next", "Безопасное уничтожение"],
  caption: [
    "JoinSet хранит набор самостоятельных задач; spawn добавляет; аналог TaskGroup",
    "join_next().await — результаты по мере завершения; abort_all, shutdown; порядок — завершения",
    "Drop набора отменяет все задачи — утечек нет; порядок запуска — прикладывайте индекс",
  ],
  frames: [
    [
      ...[0, 1, 2].map((i) =>
        Box(`t${i}`, 80 + i * 100, 66, 80, 34, `задача ${i + 1}`, "b", {
          size: 10,
        }),
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["while let Some(r) = set.join_next().await {", "    let v = r?;", "}"],
        [0],
        { w: 340, size: 10, lh: 26 },
      ),
    ],
    [Box("a", 180, 60, 230, 34, "drop(set) → abort всех", "y", { size: 12 })],
  ],
});

// 7. spawn_blocking
export const V07 = scene({
  labels: ["spawn_blocking", "block_in_place", "Файлы"],
  caption: [
    "Замыкание в отдельном пуле (до 512 потоков), результат — JoinHandle; отменить после старта нельзя",
    "block_in_place превращает текущий рабочий поток в блокирующий — только multi_thread; тяжёлые вычисления — rayon",
    "tokio::fs внутри использует тот же пул: файловый ввод-вывод у ОС не везде асинхронный",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ["let r = tokio::task::spawn_blocking(|| heavy()).await?;"],
        [0],
        { w: 340, size: 9, lh: 28 },
      ),
    ],
    [
      rs("c", 20, 50, ["tokio::task::block_in_place(|| heavy());"], [0], {
        w: 340,
        size: 11,
        lh: 28,
      }),
    ],
    [...pair("tokio::fs", "spawn_blocking", "b", "g")],
  ],
});

// 8. LocalSet
export const V08 = scene({
  labels: ["!Send-задачи", "LocalSet", "Когда"],
  caption: [
    "Задача с Rc внутри не Send: tokio::spawn её не примет",
    "LocalSet::new().run_until(async { spawn_local(…) }) — задачи на одном потоке",
    "GUI, код, привязанный к потоку; в серверах почти не нужен — но решает ошибку «future is not Send»",
  ],
  frames: [
    [...pair("Rc в задаче", "spawn ✕", "r", "r")],
    [
      rs(
        "c",
        20,
        50,
        [
          "let local = LocalSet::new();",
          "local.run_until(async {",
          "    tokio::task::spawn_local(async { … }).await",
          "}).await;",
        ],
        [2],
        { w: 340, size: 9, lh: 22 },
      ),
    ],
    [...row("a", ["GUI", "потоки"], "b", 66, 10.5)],
  ],
});

// 9. Task-local и наблюдение
export const V09 = scene({
  labels: ["task_local!", "Номер задачи", "Наблюдение"],
  caption: [
    "task_local! — значение на задачу, как contextvars в Python; KEY.scope(v, fut) задаёт его на время фьючера",
    "tokio::task::id() — номер задачи",
    "tracing и tokio-console показывают живые задачи, время опроса и ожидания: зависшие задачи видны",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "tokio::task_local! { static REQ: u32; }",
          "REQ.scope(7, async { REQ.get() }).await",
        ],
        [1],
        { w: 340, size: 9, lh: 28 },
      ),
    ],
    [
      rs("c", 20, 50, ["let id = tokio::task::id();"], [0], {
        w: 340,
        size: 12,
        lh: 28,
      }),
    ],
    [...pair("tracing", "tokio-console", "b", "g")],
  ],
});

// 10. Кооперативное планирование
export const V10 = scene({
  labels: ["Бюджет", "Вычисления без .await", "Правило"],
  caption: [
    "У каждой задачи бюджет: 128 операций; потом ресурс сам возвращает Pending и отдаёт слово другим",
    "Долгий цикл без .await занимает поток целиком: нужны yield_now() или spawn_blocking",
    "Между двумя .await — не больше десятков микросекунд работы",
  ],
  frames: [
    [Box("a", 180, 66, 200, 40, "бюджет: 128", "g", { size: 12 })],
    [
      rs(
        "c",
        20,
        40,
        ["loop {", "    heavy_step();   // нет .await — поток занят", "}"],
        [1],
        { w: 340, size: 10.5, lh: 26, bad: [1] },
      ),
    ],
    [
      Box("a", 180, 60, 230, 34, "между .await — микросекунды", "y", {
        size: 11.5,
      }),
    ],
  ],
});

// 11. Завершение
export const V11 = scene({
  labels: ["Конец main", "shutdown_timeout", "Ctrl-C"],
  caption: [
    "Вернулась main — рантайм уничтожен, незавершённые задачи отменены, деструкторы вызваны (в Python — предупреждение)",
    "Дожидайтесь важных задач явно: JoinHandle, JoinSet; shutdown_timeout даёт время на выход",
    "tokio::signal::ctrl_c().await — фьючер, просыпающийся по сигналу: основа корректной остановки сервера",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "#[tokio::main]",
          "async fn main() {",
          "    tokio::spawn(work());   // main вышла → work отменена",
          "}",
        ],
        [2],
        { w: 340, size: 8.5, lh: 22 },
      ),
    ],
    [
      rs("c", 20, 50, ["rt.shutdown_timeout(Duration::from_secs(5));"], [0], {
        w: 340,
        size: 10,
        lh: 28,
      }),
    ],
    [
      rs("c", 20, 50, ["tokio::signal::ctrl_c().await?;"], [0], {
        w: 340,
        size: 12,
        lh: 28,
      }),
    ],
  ],
});

// 12. Тесты
export const V12 = scene({
  labels: ["#[tokio::test]", "pause и advance", "В песочнице"],
  caption: [
    "Отдельный рантайм на каждый тест; по умолчанию однопоточный — детерминированно",
    "test-util: time::pause() замораживает время, advance(d) двигает вперёд — тест «на час» проходит мгновенно",
    "В нашей песочнице test-util не включён — упражнения используют настоящие короткие паузы",
  ],
  frames: [
    [
      rs("c", 20, 50, ["#[tokio::test]", "async fn t() { … }"], [0], {
        w: 340,
        size: 12,
        lh: 28,
      }),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "tokio::time::pause();",
          "tokio::time::advance(Duration::from_secs(3600)).await;",
        ],
        undefined,
        { w: 340, size: 9, lh: 28 },
      ),
    ],
    [Box("a", 180, 60, 230, 34, "паузы по 5–50 мс", "y", { size: 12 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Шпаргалка", "Дальше"],
  caption: [
    "tokio::main создаёт рантайм; Builder настраивает; Handle запускает из других потоков; spawn → JoinHandle; JoinSet собирает",
    "spawn_blocking и block_in_place — для блокирующего; LocalSet — для !Send; планирование кооперативно; завершение — явно",
    "Следующая глава — время: sleep, interval, timeout, select!",
  ],
  frames: [
    [...row("a", ["main", "Builder", "spawn", "JoinSet"], "g")],
    [
      rs(
        "c",
        20,
        40,
        ["spawn → JoinHandle<T>", "spawn_blocking → пул", "LocalSet → !Send"],
        undefined,
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      Box("a", 180, 60, 230, 34, "sleep · interval · timeout · select!", "b", {
        size: 10,
      }),
    ],
  ],
});
