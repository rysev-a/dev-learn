import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, rs } from "./rs.tsx";

/* Глава 30 книги «Изучаем Rust»: асинхронность в Python и в Rust. */

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
  labels: [
    "Ожидание",
    "Один поток, много задач",
    "Конкурентность и параллелизм",
  ],
  caption: [
    "Большую часть времени сервер ждёт: ответ, диск, база данных",
    "Десять тысяч соединений нельзя вести десятью тысячами потоков ОС: один поток переключается между задачами",
    "Конкурентность — много дел в процессе; параллелизм — несколько выполняются в один момент на разных ядрах",
  ],
  frames: [
    [...row("a", ["запрос", "ждём…", "ответ"], "b", 66, 11)],
    [
      Box("t", 180, 40, 100, 26, "поток", "g", { size: 11 }),
      ...[0, 1, 2, 3].map((i) =>
        Box(`k${i}`, 60 + i * 80, 100, 66, 28, `задача ${i + 1}`, "b", {
          size: 9,
        }),
      ),
    ],
    [
      ...pair(
        "конкурентность\nпереключение",
        "параллелизм\nразные ядра",
        "b",
        "g",
      ),
    ],
  ],
});

// 2. asyncio
export const V02 = scene({
  labels: ["Три способа", "Event loop", "Блокировка"],
  caption: [
    "Python: потоки (ограничены GIL), процессы (дорогая пересылка данных), asyncio",
    "async def и await: корутина отдаёт управление циклу событий в одном потоке",
    "time.sleep внутри корутины замораживает весь цикл — самая частая ошибка",
  ],
  frames: [
    [...row("a", ["потоки", "процессы", "asyncio"], "m", 66, 10.5)],
    [
      rs(
        "c",
        20,
        40,
        [
          "async def fetch():",
          "    await asyncio.sleep(1)",
          "asyncio.run(main())",
        ],
        [1],
        { w: 340, size: 11, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["async def bad():", "    time.sleep(5)   # весь цикл стоит"],
        [1],
        { w: 340, size: 11, lh: 28, bad: [1] },
      ),
    ],
  ],
});

// 3. Корутины Python
export const V03 = scene({
  labels: ["Корутина-объект", "create_task", "gather"],
  caption: [
    "Вызов async-функции без await создаёт объект и ничего не делает: «coroutine was never awaited»",
    "create_task ставит корутину в очередь цикла: она стартует при ближайшем переключении",
    "gather запускает несколько и собирает результаты; wait_for ограничивает время",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "c = fetch()      # объект, не запущен",
          "await c         # теперь работает",
        ],
        [0],
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "t = asyncio.create_task(fetch())",
          "# запустится сразу при переключении",
        ],
        [0],
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
    [
      rs("c", 20, 50, ["a, b = await asyncio.gather(f(1), f(2))"], undefined, {
        w: 340,
        size: 10.5,
        lh: 28,
      }),
    ],
  ],
});

// 4. Future в Rust
export const V04 = scene({
  labels: ["async fn → Future", "Конечный автомат", "Ленивость"],
  caption: [
    "async fn возвращает значение типа impl Future<Output = T>",
    "Это конечный автомат: хранит локальные переменные и точку остановки, размер известен при сборке, без кучи",
    "Пока никто не вызвал poll, ни одна строка тела не выполнена — строже, чем create_task в Python",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "async fn get() -> u32 { 5 }",
          "let f = get();   // Future, ещё не выполнено",
        ],
        [1],
        { w: 340, size: 10, lh: 28 },
      ),
    ],
    [Box("a", 180, 60, 230, 40, "состояние: x, y, шаг 2", "g", { size: 11.5 })],
    [
      ...pair(
        "Python:\ncreate_task стартует",
        "Rust:\nничего без poll",
        "m",
        "g",
      ),
    ],
  ],
});

// 5. Рантайм
export const V05 = scene({
  labels: ["Нет в std", "tokio, smol, embassy", "Выбор"],
  caption: [
    "В языке: async, await, Future, Poll, Context, Waker; цикла событий, таймеров и сети нет",
    "tokio — самый распространённый; async-std, smol; embassy — микроконтроллеры; futures — общие инструменты",
    "Библиотеки привязаны к рантайму; выбор влияет на всю программу",
  ],
  frames: [
    [...pair("язык\nFuture, Poll", "библиотека\nрантайм", "b", "y")],
    [...row("a", ["tokio", "async-std", "smol", "embassy"], "g", 66, 10)],
    [Box("a", 180, 60, 230, 34, "tokio — по умолчанию", "y", { size: 12 })],
  ],
});

// 6. Синтаксис
export const V06 = scene({
  labels: ["async fn", ".await", "async-блок"],
  caption: [
    "async fn get() -> String — объявление; в Python — async def",
    "Ожидание — постфиксное: fetch().await, а не await fetch(); цепочки: req.await?.json().await?",
    "async move { … } — фьючер из куска кода; .await допустим только внутри async-контекста",
  ],
  frames: [
    [...pair("async def f():", "async fn f()", "m", "g")],
    [...pair("await fetch()", "fetch().await", "m", "g")],
    [
      rs("c", 20, 50, ["let f = async move {", "    work().await", "};"], [0], {
        w: 340,
        size: 11.5,
        lh: 26,
      }),
    ],
  ],
});

// 7. Комбинаторы
export const V07 = scene({
  labels: ["gather ↔ join!", "create_task ↔ spawn", "TaskGroup ↔ JoinSet"],
  caption: [
    "asyncio.gather → join! (кортеж результатов), try_join! — остановка на первой ошибке",
    "create_task → spawn (возвращает JoinHandle), wait_for → timeout, as_completed → FuturesUnordered",
    "TaskGroup → JoinSet; run_in_executor → spawn_blocking; Queue → mpsc; Lock → Mutex",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "let (a, b) = join!(f(1), f(2)).await;",
          "let r = try_join!(f(1), f(2))?;",
        ],
        undefined,
        { w: 340, size: 10, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["let h = tokio::spawn(f());", "let v = h.await?;"],
        [0],
        { w: 340, size: 11.5, lh: 28 },
      ),
    ],
    [...row("a", ["JoinSet", "blocking", "mpsc", "Mutex"], "g", 66, 10)],
  ],
});

// 8. Блокировка
export const V08 = scene({
  labels: ["Не блокировать", "spawn_blocking", "CPU-вычисления"],
  caption: [
    "Блокирующий вызов в async-задаче занимает рабочий поток и тормозит остальные задачи",
    "run_in_executor → tokio::task::spawn_blocking: код идёт в отдельный пул, результат — фьючер",
    "Тяжёлые вычисления — rayon или обычные потоки; задача должна быстро доходить до следующего .await",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "async fn bad() {",
          "    std::thread::sleep(d);   // блокирует поток",
          "}",
        ],
        [1],
        { w: 340, size: 10.5, lh: 26, bad: [1] },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["let r = tokio::task::spawn_blocking(|| heavy()).await?;"],
        [0],
        { w: 340, size: 9.5, lh: 28 },
      ),
    ],
    [...pair("async: ожидание", "rayon: вычисления", "b", "g")],
  ],
});

// 9. Параллелизм
export const V09 = scene({
  labels: ["Один поток", "Work-stealing", "Send"],
  caption: [
    "asyncio: один поток, задачи не выполняются одновременно — гонок нет, ядра не используются",
    "tokio по умолчанию многопоточный: пул рабочих потоков и кража работы; задача может менять поток между .await",
    "spawn требует Send + 'static: данные, живущие через .await, безопасно переходят между потоками — гонок данных нет",
  ],
  frames: [
    [
      Box("t", 180, 40, 100, 26, "1 поток", "m", { size: 11 }),
      ...[0, 1, 2].map((i) =>
        Box(`k${i}`, 80 + i * 100, 100, 70, 28, `задача ${i + 1}`, "b", {
          size: 9,
        }),
      ),
    ],
    [
      ...[0, 1, 2, 3].map((i) =>
        Box(`t${i}`, 60 + i * 80, 40, 66, 26, `поток ${i + 1}`, "g", {
          size: 9,
        }),
      ),
      ...[0, 1, 2, 3, 4].map((i) =>
        Box(`k${i}`, 50 + i * 65, 100, 56, 26, `${i + 1}`, "b", { size: 10 }),
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "tokio::spawn(async move { … })",
          "// требует: Future: Send + 'static",
        ],
        [1],
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
  ],
});

// 10. Отмена
export const V10 = scene({
  labels: ["task.cancel()", "drop(future)", "Безопасность к отмене"],
  caption: [
    "Python: cancel() бросает CancelledError в точке await — задача может перехватить и прибраться",
    "Rust: уничтоженный фьючер просто перестаёт существовать; остановка — на ближайшей точке .await, Drop освобождает значения",
    "Отмена: select!, timeout, abort() хэндла; код должен выдерживать остановку между любыми двумя .await",
  ],
  frames: [
    [
      rs("c", 20, 50, ["t.cancel()   # CancelledError в await"], [0], {
        w: 340,
        size: 11,
        lh: 28,
      }),
    ],
    [
      rs("c", 20, 50, ["drop(fut);   // работа остановлена"], [0], {
        w: 340,
        size: 12,
        lh: 28,
      }),
    ],
    [...row("a", ["select!", "timeout", "abort()"], "y", 66, 11)],
  ],
});

// 11. Цена
export const V11 = scene({
  labels: ["Python", "Rust", "Масштаб"],
  caption: [
    "Корутина Python — объект на куче, килобайты и микросекунды на переключение",
    "Задача tokio — автомат размером с состояние (десятки байтов), переключение — десятки наносекунд",
    "Сотни тысяч задач и миллионы соединений на одной машине — норма для Rust",
  ],
  frames: [
    [Box("a", 180, 66, 220, 40, "≈ килобайты, мкс", "m", { size: 12 })],
    [Box("a", 180, 66, 220, 40, "≈ десятки байтов, нс", "g", { size: 12 })],
    [
      ...row("a", ["10²", "10⁴", "10⁶"], "g", 66, 14),
      Tx("n", 180, 118, "задач на машину", { size: 10 }),
    ],
  ],
});

// 12. Когда что
export const V12 = scene({
  labels: ["Когда async", "Когда потоки", "Мост block_on"],
  caption: [
    "Много задач, в основном ожидание: серверы, прокси, чаты, краулеры, клиенты баз данных",
    "Мало задач и вычисления: потоки или rayon; смешанные программы — async-ядро и вычислительный пул",
    "Из обычного кода в async — block_on запускает фьючер до конца в текущем потоке; «окраска функций»",
  ],
  frames: [
    [...row("a", ["серверы", "прокси", "чаты", "краулеры"], "g", 66, 10)],
    [...pair("потоки\nrayon", "async-ядро\n+ пул", "b", "g")],
    [
      rs(
        "c",
        20,
        50,
        ["fn main() {", "    block_on(async { work().await });", "}"],
        [1],
        { w: 340, size: 10.5, lh: 26 },
      ),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Соответствия", "Правила", "Дальше"],
  caption: [
    "gather → join!; create_task → spawn; run_in_executor → spawn_blocking; TaskGroup → JoinSet; cancel → drop",
    "Future ленив, рантайм из библиотеки, tokio многопоточен и требует Send, блокировать нельзя",
    "Следующая глава: Future, Poll и Waker — своими руками",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "gather      → join!",
          "create_task → spawn",
          "TaskGroup   → JoinSet",
          "cancel      → drop",
        ],
        undefined,
        { w: 340, size: 11, lh: 22 },
      ),
    ],
    [
      ...row(
        "a",
        ["ленивость", "рантайм", "Send", "не блокировать"],
        "g",
        66,
        8.5,
      ),
    ],
    [Box("a", 180, 60, 250, 34, "Future · Poll · Waker", "b", { size: 12 })],
  ],
});
