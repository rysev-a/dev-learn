import { scene } from "./alg.tsx";
import { Box, arrow, rs, pair, rsRow } from "./rs.tsx";

/* Глава 32 книги «Изучаем Rust»: async и await — автоматы и Pin. */

// 1. Введение
export const V01 = scene({
  labels: ["Что делает компилятор", "Что объясним", "Самая сложная часть"],
  caption: [
    "async fn превращается в конечный автомат — посмотрим, в какой именно",
    "Автоматы, Pin, заимствования, Send, async-замыкания, async fn в трейтах, рекурсия, отмена",
    "Понимание этой темы отличает уверенного автора async-кода от начинающего",
  ],
  frames: [
    [...pair("async fn", "автомат", "b", "g")],
    [...rsRow("a", ["автомат", "Pin", "Send", "отмена"], "b")],
    [Box("a", 180, 60, 230, 34, "Pin · Send · 'static", "y", { size: 12 })],
  ],
});

// 2. Десахаринг
export const V02 = scene({
  labels: ["async fn = fn + async-блок", "Анонимный тип", "Время жизни"],
  caption: [
    "async fn f(x: u32) -> String ≈ fn f(x: u32) -> impl Future<Output = String> { async move { … } }",
    "Тип async-блока анонимен и не пишется; в сигнатурах — impl Future",
    "Аргументы попадают в фьючер: ссылка-параметр привязывает время жизни фьючера к аргументу",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        40,
        [
          "async fn f(x: u32) -> String { … }",
          "// ≈",
          "fn f(x: u32) -> impl Future<Output = String> { async move { … } }",
        ],
        [0, 2],
        { w: 340, size: 8.5, lh: 24 },
      ),
    ],
    [Box("a", 180, 60, 230, 34, "тип: {async block#1}", "y", { size: 11.5 })],
    [
      rs(
        "c",
        20,
        50,
        [
          "fn longest<'a>(x: &'a str, y: &'a str)",
          "    -> impl Future<Output = &'a str> + 'a",
        ],
        [1],
        { w: 340, size: 9.5, lh: 28 },
      ),
    ],
  ],
});

// 3. Состояния
export const V03 = scene({
  labels: ["Точки .await", "Живые переменные", "poll"],
  caption: [
    "Тело делится по .await: состояние «до начала», по одному на точку, «готово»",
    "В состоянии хранятся только переменные, живые после точки; размер — самый большой набор",
    "poll начинает с текущего состояния, выполняет до следующей точки и возвращает Pending или Ready",
  ],
  frames: [
    [...rsRow("a", ["начало", "после 1", "после 2", "готово"], "b", 66, 10)],
    [
      rs(
        "c",
        20,
        40,
        [
          "let a = f().await;   // a жива после",
          "let t = tmp();          // t не живёт через .await",
          "g(a).await;",
        ],
        [0],
        { w: 340, size: 8.5, lh: 26 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "match self.state {",
          "    S0 => { … Pending / S1 }",
          "    S1 => { … Ready }",
          "}",
        ],
        undefined,
        { w: 340, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 4. Самоссылка
export const V04 = scene({
  labels: ["Ссылка внутрь себя", "Перемещение ломает", "Нужен Pin"],
  caption: [
    "buf = [0; 16]; let s = &buf[..]; x.await; — срез указывает внутрь того же автомата",
    "Если автомат переместить (в вектор, в функцию), buf переедет, а s останется на старом месте",
    "Обычный Rust не умеет создавать самоссылающиеся значения безопасно — async обязан, и решение — Pin",
  ],
  frames: [
    [
      Box("b", 100, 66, 90, 34, "buf", "b", { size: 11 }),
      Box("s", 260, 66, 90, 34, "s → buf", "y", { size: 11 }),
      arrow("e", 230, 66, 150, 66, "y"),
    ],
    [
      Box("b", 100, 66, 90, 34, "buf (новое)", "g", { size: 10 }),
      Box("s", 260, 66, 90, 34, "s → старое ✕", "r", { size: 10 }),
    ],
    [
      Box("a", 180, 60, 230, 34, "Pin: значение не сдвинется", "g", {
        size: 12,
      }),
    ],
  ],
});

// 5. Pin
export const V05 = scene({
  labels: ["Обещание", "Unpin", "Как закрепить"],
  caption: [
    "Pin<P> обещает: значение не будет перемещено, пока не уничтожено; poll принимает Pin<&mut Self>",
    "Unpin — «можно двигать и закреплённым»: почти все типы Unpin; автомат async-блока — нет",
    "Box::pin(f) — в куче; pin!(f) — на стеке; Pin::new(&mut f) — только для Unpin",
  ],
  frames: [
    [...pair("Pin<&mut T>", "T не сдвинется", "b", "g")],
    [...pair("i32, String\nUnpin", "async-блок\n!Unpin", "g", "y")],
    [
      rs(
        "c",
        20,
        40,
        [
          "let a = Box::pin(fut);",
          "let b = std::pin::pin!(fut);",
          "let c = Pin::new(&mut unpin_fut);",
        ],
        undefined,
        { w: 340, size: 10, lh: 24 },
      ),
    ],
  ],
});

// 6. Pin на практике
export const V06 = scene({
  labels: ["BoxFuture", "select! и pin!", "pin-project"],
  caption: [
    "Pin<Box<dyn Future<Output = T> + Send>> так частый, что в futures есть синоним BoxFuture",
    "select! и повторное ожидание: закрепить фьючер pin!, затем в цикле опрашивать через .as_mut()",
    "Проекция поля-фьючера в своём комбинаторе — пакет pin-project, а не ручной unsafe",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "type BoxFuture<'a, T> =",
          "    Pin<Box<dyn Future<Output = T> + Send + 'a>>;",
        ],
        [1],
        { w: 340, size: 9, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        40,
        [
          "let mut f = pin!(slow());",
          "loop { select! { _ = &mut f => break, _ = tick() => {} } }",
        ],
        [0],
        { w: 340, size: 8, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["#[pin_project]", "struct Map<F> { #[pin] inner: F }"],
        [0],
        { w: 340, size: 10.5, lh: 28 },
      ),
    ],
  ],
});

// 7. Async-замыкания
export const V07 = scene({
  labels: ["Замыкание → async-блок", "async |x| …", "AsyncFn"],
  caption: [
    "|x| async move { x + 1 } — обычное замыкание, возвращающее фьючер; вызывается много раз",
    "Rust 1.85: async |x| x + 1 — настоящие async-замыкания; лучше работают с заимствованиями",
    "Трейты AsyncFn, AsyncFnMut, AsyncFnOnce для обобщённых функций над асинхронными обратными вызовами",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ["let f = |x: u32| async move { x + 1 };", "f(1).await"],
        [0],
        { w: 340, size: 10, lh: 28 },
      ),
    ],
    [
      rs("c", 20, 50, ["let f = async |x: u32| x + 1;", "f(1).await"], [0], {
        w: 340,
        size: 11,
        lh: 28,
      }),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "async fn apply(f: impl AsyncFn(u32) -> u32) -> u32 {",
          "    f(1).await",
          "}",
        ],
        [0],
        { w: 340, size: 9, lh: 26 },
      ),
    ],
  ],
});

// 8. Заимствования
export const V08 = scene({
  labels: ["Ссылки через .await", "spawn требует 'static", "Владение"],
  caption: [
    "Ссылка может жить через .await, если данные переживают фьючер",
    "tokio::spawn не принимает ссылок на локальные переменные родителя: родитель завершится раньше",
    "Передавайте владение: move, клоны Arc, каналы — самая частая причина ошибок у новичков",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        [
          "async fn f(s: &str) -> usize {",
          "    sleep().await;",
          "    s.len()",
          "}",
        ],
        undefined,
        { w: 340, size: 10.5, lh: 24 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          'let s = String::from("a");',
          'tokio::spawn(async { println!("{}", &s); });  // ✕ \'static',
        ],
        [1],
        { w: 340, size: 8.5, lh: 28, bad: [1] },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          'let s = Arc::new(String::from("a"));',
          "let s2 = s.clone();",
          'tokio::spawn(async move { println!("{}", s2); });',
        ],
        [2],
        { w: 340, size: 9, lh: 24 },
      ),
    ],
  ],
});

// 9. Send
export const V09 = scene({
  labels: ["Не-Send через .await", "Guard std::Mutex", "Решения"],
  caption: [
    "Rc, ссылки без Sync и MutexGuard, живущие через .await, делают фьючер !Send — spawn не соберётся",
    "Страж std::sync::Mutex через .await: не Send и риск тупика",
    "Освободить до .await (блок), tokio::sync::Mutex или не держать замок через ожидание",
  ],
  frames: [
    [...pair("Rc через .await", "future: !Send", "r", "r")],
    [
      rs(
        "c",
        20,
        50,
        [
          "let g = m.lock().unwrap();",
          "sleep().await;   // ✕ guard через await",
          "use(&g);",
        ],
        [1],
        { w: 340, size: 9.5, lh: 24, bad: [1] },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        [
          "{ let g = m.lock().unwrap(); *g += 1; }   // освободили",
          "sleep().await;",
        ],
        [0],
        { w: 340, size: 9, lh: 28 },
      ),
    ],
  ],
});

// 10. async в трейтах
export const V10 = scene({
  labels: ["Стабильно с 1.75", "dyn Trait", "async-trait"],
  caption: [
    "trait Source { async fn get(&self) -> u32; } — статическая диспетчеризация",
    "Для Box<dyn Source> не годится: нужно вручную возвращать BoxFuture",
    "Пакет async-trait делает это автоматически ценой аллокации; в обобщённом коде — Send-ограничения",
  ],
  frames: [
    [
      rs(
        "c",
        20,
        50,
        ["trait Source {", "    async fn get(&self) -> u32;", "}"],
        [1],
        { w: 340, size: 11, lh: 26 },
      ),
    ],
    [
      rs("c", 20, 50, ["fn get(&self) -> BoxFuture<'_, u32>;"], undefined, {
        w: 340,
        size: 10.5,
        lh: 28,
      }),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["#[async_trait]", "trait Source { async fn get(&self) -> u32; }"],
        [0],
        { w: 340, size: 10, lh: 28 },
      ),
    ],
  ],
});

// 11. Рекурсия и размер
export const V11 = scene({
  labels: ["Бесконечный размер", "Box::pin", "Большие фьючеры"],
  caption: [
    "async fn не вызывает себя напрямую: размер автомата включал бы сам себя",
    "Упакуйте рекурсивный вызов: Box::pin(fact(n - 1)).await",
    "Большие значения через .await раздувают автомат: храните в куче; size_of_val; clippy::large_futures",
  ],
  frames: [
    [
      Box("a", 180, 60, 230, 34, "размер = размер + размер…", "r", {
        size: 11,
      }),
    ],
    [
      rs("c", 20, 50, ["Box::pin(fact(n - 1)).await"], [0], {
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
        ["let buf = vec![0u8; 1_000_000];   // в куче", "work().await;"],
        [0],
        { w: 340, size: 10, lh: 28 },
      ),
    ],
  ],
});

// 12. Отмена
export const V12 = scene({
  labels: ["Любой .await — возможный конец", "Cancel safety", "Нет async Drop"],
  caption: [
    "Фьючер могут отбросить на любом .await: промежуточное состояние в локальных переменных пропадёт",
    "Пример: часть данных уже прочитана в локальный буфер, чтение отменили в select! — данные потеряны",
    "Асинхронного Drop в языке нет: очистка с ожиданием — явный метод close().await или отдельная задача",
  ],
  frames: [
    [Box("a", 180, 60, 230, 34, "… .await ✂ drop", "y", { size: 12 })],
    [
      rs(
        "c",
        20,
        50,
        [
          "let n = rx.read(&mut buf).await?;   // часть в buf",
          "select!{ … }   // отмена → buf пропал",
        ],
        [1],
        { w: 340, size: 8.5, lh: 28 },
      ),
    ],
    [
      rs(
        "c",
        20,
        50,
        ["conn.close().await;   // явно", "// а не impl Drop с .await"],
        [0],
        { w: 340, size: 11, lh: 28 },
      ),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Запомнить", "Правила", "Дальше"],
  caption: [
    "async-блок — автомат с состояниями по .await; ссылки внутри → Pin; почти всё Unpin, кроме автоматов",
    "spawn: Send + 'static — владение, Arc, move; guard std Mutex не через .await; рекурсия — Box::pin; код выдерживает отмену",
    "Следующая глава — tokio: рантайм, #[tokio::main], spawn, JoinSet",
  ],
  frames: [
    [...rsRow("a", ["автомат", "Pin", "Send", "'static"], "g")],
    [...rsRow("a", ["move", "Arc", "Box::pin", "cancel"], "b")],
    [Box("a", 180, 60, 230, 34, "tokio: spawn · JoinSet", "b", { size: 12 })],
  ],
});
