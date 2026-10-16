import { scene } from "./alg.jsx";
import { Tx } from "./hw.jsx";
import { Box, arrow, rs, slot } from "./rs.jsx";

/* Глава 31 книги «Изучаем Rust»: Future, Poll и Waker. */

const pair = (a, b, ca = "m", cb = "g", y = 60) => [
  Box("pa", 90, y, 130, 34, a, ca, { size: 10 }),
  Box("pb", 270, y, 130, 34, b, cb, { size: 10 }),
];
const row = (pre, items, c = "g", y = 66, size = 10.5) =>
  items.map((t, i) =>
    Box(`${pre}${i}`, 50 + i * 86, y, 76, 30, t, c, { size }),
  );

// 1. Введение
export const V01 = scene({
  labels: ["Своими руками", "Только std", "Без магии"],
  caption: [
    "Свои фьючеры, вейкер, исполнитель и таймер — чтобы async и await перестали быть магией",
    "Всё живёт в std::future и std::task: один трейт, два типа и несколько помощников",
    "async и await — механика конечных автоматов",
  ],
  frames: [
    [...row("a", ["Future", "Waker", "block_on", "Timer"], "b")],
    [...pair("std::future", "std::task", "b", "b")],
    [Box("a", 180, 60, 230, 34, "async = автомат", "g", { size: 12 })],
  ],
});

// 2. Future и Poll
export const V02 = scene({
  labels: ["trait Future", "Poll", "Не блокирует"],
  caption: [
    "fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>",
    "Poll::Ready(T) — готово; Poll::Pending — ещё нет, зайдите позже",
    "poll вызывает исполнитель и он не блокирует: либо значение есть, либо Pending",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "trait Future {",
          "    type Output;",
          "    fn poll(self: Pin<&mut Self>, cx: &mut Context) -> Poll<Self::Output>;",
          "}",
        ],
        [2],
        { w: 340, size: 7.5, lh: 22 },
      ),
    ],
    [...pair("Ready(5)", "Pending", "g", "y")],
    [
      Box("a", 90, 60, 130, 34, "исполнитель", "b", { size: 11 }),
      arrow("e", 156, 60, 204, 60, "g"),
      Box("b", 270, 60, 130, 34, "poll()", "g", { size: 11 }),
    ],
  ],
});

// 3. Pending требует wake
export const V03 = scene({
  labels: ["Pending → ждём", "wake()", "Забытый wake"],
  caption: [
    "Фьючер вернул Pending — исполнитель больше не опрашивает его, пока не получит сигнал",
    "Сигнал — вызов waker.wake(): от ОС, другого потока, таймера или самого фьючера (wake_by_ref перед Pending)",
    "Pending без будущего wake — задача зависает навсегда и молча",
  ],
  frames: [
    [
      Box("a", 180, 60, 230, 34, "Pending → в очередь ожидания", "y", {
        size: 11,
      }),
    ],
    [
      rs("c", 20, 50, ["cx.waker().wake_by_ref();", "Poll::Pending"], [0], {
        w: 340,
        size: 12,
        lh: 28,
      }),
    ],
    [
      Box("a", 180, 60, 230, 34, "Pending без wake ✕ — зависание", "r", {
        size: 11,
      }),
    ],
  ],
});

// 4. Waker
export const V04 = scene({
  labels: ["Дескриптор задачи", "Wake для Arc", "noop"],
  caption: [
    "Waker клонируется, передаётся в другой поток и вызывается; внутри — указатель и таблица из четырёх функций",
    "Проще, чем RawWaker: impl Wake for Task { fn wake(self: Arc<Self>) } и Waker::from(arc)",
    "Waker::noop() — вейкер-пустышка для тестов, когда вы сами опрашиваете фьючер в цикле",
  ],
  frames: [
    [...row("a", ["clone", "wake", "wake_by_ref", "drop"], "b", 66, 9)],
    [
      rs(
        "c",
        20,
        40,
        [
          "impl Wake for Task {",
          "    fn wake(self: Arc<Self>) { /* в очередь */ }",
          "}",
          "let w = Waker::from(task_arc);",
        ],
        undefined,
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["let mut cx = Context::from_waker(Waker::noop());"],
        [0],
        { w: 340, size: 9.5, lh: 28 },
      ),
    ],
  ],
});

// 5. Простые фьючеры
export const V05 = scene({
  labels: ["Ready", "YieldOnce", "CountDown"],
  caption: [
    "Ready<T>: при первом poll вынимает значение из Option и возвращает Ready",
    "YieldOnce: первый poll — wake_by_ref и Pending, второй — Ready(()): аналог передачи управления",
    "CountDown: отсчитывает число опросов; async-код компилятор превращает в такие же структуры",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "struct Ready<T>(Option<T>);",
          "fn poll(..) -> Poll<T> {",
          "    Poll::Ready(self.0.take().unwrap())",
          "}",
        ],
        [2],
        { w: 340, size: 9.5, lh: 22 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "if self.done { Poll::Ready(()) } else {",
          "    self.done = true;",
          "    cx.waker().wake_by_ref();",
          "    Poll::Pending",
          "}",
        ],
        [2],
        { w: 340, size: 9.5, lh: 20 },
      ),
    ],
    [...row("a", ["3", "2", "1", "go"], "b", 66, 12)],
  ],
});

// 6. block_on
export const V06 = scene({
  labels: ["Крутим в цикле", "park и unpark", "Ложные пробуждения"],
  caption: [
    "Простой block_on: poll в цикле с noop-вейкером — работает, но жжёт процессор",
    "Лучше: waker будит поток через thread::unpark, а после Pending цикл вызывает thread::park",
    "park может вернуться и без wake — просто опросите снова: это безвредно",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        30,
        [
          "loop {",
          "    match fut.as_mut().poll(&mut cx) {",
          "        Poll::Ready(v) => return v,",
          "        Poll::Pending => {}",
          "    }",
          "}",
        ],
        undefined,
        { w: 340, size: 9.5, lh: 18 },
      ),
    ],
    [...pair("poll → Pending\npark()", "wake()\nunpark()", "y", "g")],
    [
      Box("a", 180, 60, 240, 34, "пробуждение ≠ готовность", "y", {
        size: 11.5,
      }),
    ],
  ],
});

// 7. Таймер
export const V07 = scene({
  labels: ["Поток-таймер", "Общее состояние", "Новый waker"],
  caption: [
    "Delay при первом poll запускает поток: sleep, поставить флаг, вызвать wake",
    "Флаг и вейкер лежат в Arc<Mutex<…>>: гонка «событие пришло до сохранения вейкера» невозможна",
    "При каждом poll сохраняйте самый свежий вейкер: задачу могли перенести на другой исполнитель",
  ],
  frames: [
    [
      Box("a", 90, 60, 130, 34, "поток: sleep(d)", "b", { size: 10.5 }),
      arrow("e", 156, 60, 204, 60, "g"),
      Box("b", 270, 60, 130, 34, "флаг + wake()", "g", { size: 10.5 }),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "struct Shared { done: bool, waker: Option<Waker> }",
          "state: Arc<Mutex<Shared>>",
        ],
        [1],
        { w: 340, size: 9, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["s.waker = Some(cx.waker().clone());", "Poll::Pending"],
        [0],
        { w: 340, size: 11, lh: 28 },
      ),
    ],
  ],
});

// 8. Комбинаторы
export const V08 = scene({
  labels: ["Map", "Join", "Select"],
  caption: [
    "Map: опрашивает внутренний фьючер и применяет функцию к результату",
    "Join: хранит два фьючера и два результата, опрашивает оба, пока не получит оба — как gather",
    "Select: возвращает результат первого готового; для полей-фьючеров нужна проекция Pin (pin-project) или Box::pin",
  ],
  frames: [
    [
      ...pair("Future<A>", "Future<B>", "b", "g"),
      arrow("e", 156, 60, 204, 60, "g"),
      Tx("t", 180, 100, "map(f)", { size: 11, mono: true }),
    ],
    [
      Box("a", 90, 60, 130, 34, "A: Ready(1)", "g", { size: 11 }),
      Box("b", 270, 60, 130, 34, "B: Pending", "y", { size: 11 }),
      Tx("t", 180, 108, "Join → Pending", { size: 11 }),
    ],
    [
      Box("a", 90, 60, 130, 34, "A: Pending", "y", { size: 11 }),
      Box("b", 270, 60, 130, 34, "B: Ready(2)", "g", { size: 11 }),
      Tx("t", 180, 108, "Select → Ready(B)", { size: 11 }),
    ],
  ],
});

// 9. Исполнитель
export const V09 = scene({
  labels: ["Task и очередь", "wake → в очередь", "Цикл"],
  caption: [
    "Задача — Arc<Task> с Mutex<Option<Pin<Box<dyn Future>>>>; spawn кладёт её в очередь (канал)",
    "Вейкер при вызове кладёт задачу обратно в канал — так задача просыпается",
    "Цикл: взять задачу, создать вейкер, poll; Ready — выбросить; Pending — ждать wake; пусто — выйти",
  ],
  frames: [
    [
      ...[0, 1, 2].map((i) =>
        Box(`t${i}`, 80 + i * 100, 60, 80, 34, `task ${i + 1}`, "b", {
          size: 10.5,
        }),
      ),
      Tx("q", 180, 112, "очередь готовых", { size: 10 }),
    ],
    [
      Box("a", 90, 60, 130, 34, "wake()", "g", { size: 11 }),
      arrow("e", 156, 60, 204, 60, "g"),
      Box("b", 270, 60, 130, 34, "в очередь", "b", { size: 11 }),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "while let Ok(task) = queue.recv() {",
          "    // poll(task); Pending → ждать wake",
          "}",
        ],
        [0],
        { w: 340, size: 9.5, lh: 26 },
      ),
    ],
  ],
});

// 10. Автомат
export const V10 = scene({
  labels: ["Состояния", "Переходы", "size_of_val"],
  caption: [
    "async fn с двумя .await → enum: Start, ЖдёмПервое, ЖдёмВторое, Done; в каждом — только нужные дальше переменные",
    "poll: match по состоянию; внутренний poll Pending → остаёмся; Ready → к следующему",
    "Размер фьючера — самое большое состояние: проверяется size_of_val(&async_block)",
  ],
  frames: [
    [
      ...["Start", "Wait1", "Wait2", "Done"].map((t, i) =>
        Box(`a${i}`, 50 + i * 86, 66, 76, 30, t, "b", { size: 10.5 }),
      ),
    ],
    [
      Box("a", 70, 66, 70, 30, "Wait1", "b", { size: 10.5 }),
      arrow("e", 110, 66, 170, 66, "g"),
      Box("b", 210, 66, 70, 30, "Wait2", "b", { size: 10.5 }),
      Tx("t", 180, 110, "Ready → следующий", { size: 10 }),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "let f = async { let big = [0u8; 100]; tick().await; big.len() };",
          'println!("{}", size_of_val(&f));',
        ],
        [1],
        { w: 340, size: 8, lh: 28 },
      ),
    ],
  ],
});

// 11. Ловушки
export const V11 = scene({
  labels: ["Pending без wake", "Poll после Ready", "Блокировка в poll"],
  caption: [
    "Зависание: вернули Pending и забыли организовать wake",
    "Poll после Ready — поведение не определено, может быть паника: оборачивайте в Fuse",
    "Блокирующий вызов внутри poll замораживает исполнитель; потерянный и устаревший вейкер; гонка флага и вейкера — мьютекс",
  ],
  frames: [
    [Box("a", 180, 60, 230, 34, "Pending, wake нет ✕", "r", { size: 11.5 })],
    [Box("a", 180, 60, 230, 34, "Ready → ещё poll ✕", "r", { size: 11.5 })],
    [Box("a", 180, 60, 230, 34, "sleep() в poll ✕", "r", { size: 11.5 })],
  ],
});

// 12. Настоящие рантаймы
export const V12 = scene({
  labels: ["Драйвер I/O", "Колесо таймеров", "asyncio"],
  caption: [
    "tokio: драйвер mio (epoll, kqueue, io_uring) — готовность сокета → wake задачи",
    "Колесо таймеров хранит задержки по времени срабатывания; пул потоков с очередями и кражей работы",
    "asyncio устроен так же, но с одним потоком и селектором: различие — где лежит автомат и кто его опрашивает",
  ],
  frames: [
    [...pair("epoll\nготов сокет", "wake()\nзадача", "b", "g")],
    [...row("a", ["10 мс", "50 мс", "1 с", "5 с"], "b", 66, 10)],
    [...pair("asyncio\n1 поток", "tokio\nпул потоков", "m", "g")],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Шпаргалка", "Дальше"],
  caption: [
    "Future::poll → Ready или Pending; перед Pending — будущий wake; Waker — дескриптор задачи",
    "block_on = цикл + park; таймер — поток + флаг + wake; исполнитель — очередь + wake; async → автомат",
    "Следующая глава — async и await подробно: конечные автоматы, Pin, async-блоки и async fn в трейтах",
  ],
  frames: [
    [...row("a", ["poll", "Pending", "wake", "Waker"], "g")],
    [
      rs(
        "c",
        20,
        40,
        [
          "block_on  = poll + park",
          "timer     = thread + flag + wake",
          "executor  = queue + wake",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      Box("a", 180, 60, 230, 34, "Pin · автоматы · async fn", "b", {
        size: 12,
      }),
    ],
  ],
});
