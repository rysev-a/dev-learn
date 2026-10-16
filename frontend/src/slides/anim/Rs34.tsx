import { scene } from "./alg.tsx";
import type { SceneItem } from "./dsl.ts";
import { Box, arrow, note, rs } from "./rs.tsx";

/* Глава 34 книги «Изучаем Rust»: Tokio — время, таймеры и select!. */

const code = { w: 340, size: 9.5, lh: 14 };
// ось времени 0…300 мс → x = 30…330
const X = (ms: number) => 30 + ms;
// отрезок на оси: от a до b мс, на высоте y
const span = (id: string, a: number, b: number, y: number, text: string, c = "g", h = 22): SceneItem =>
  Box(id, (X(a) + X(b)) / 2, y, Math.max(b - a - 2, 14), h, text, c, { size: 8.5 });
const axis = (y: number): SceneItem[] => [
  { t: "line", id: "ax", x1: 30, y1: y, x2: 336, y2: y, c: "m", w: 1.2 },
  note("t0", 30, y + 12, "0", "m"),
  note("t1", 130, y + 12, "100 мс", "m"),
  note("t2", 230, y + 12, "200 мс", "m"),
];
const tick = (id: string, ms: number, y: number, c = "g"): SceneItem => Box(id, X(ms), y, 10, 16, "", c);

// 1. Ждать, не блокируя
export const V01 = scene({
  labels: ["thread::sleep", "tokio::time::sleep", "Правило"],
  caption: [
    "std::thread::sleep усыпляет поток: три задачи на нём стоят",
    "tokio::time::sleep().await отдаёт поток: остальные задачи работают",
    "Внутри async — только tokio::time::sleep; блокировать поток нельзя",
  ],
  frames: [
    [
      Box("th", 60, 90, 80, 90, "поток", "m", { size: 10 }),
      Box("a", 200, 40, 120, 26, "задача A: спит", "r", { size: 9 }),
      Box("b", 200, 90, 120, 26, "задача B: ждёт", "r", { size: 9 }),
      Box("c", 200, 140, 120, 26, "задача C: ждёт", "r", { size: 9 }),
    ],
    [
      Box("th", 60, 90, 80, 90, "поток", "g", { size: 10 }),
      Box("a", 200, 40, 120, 26, "A: ждёт таймер", "m", { size: 9 }),
      Box("b", 200, 90, 120, 26, "B: работает", "g", { size: 9 }),
      Box("c", 200, 140, 120, 26, "C: работает", "g", { size: 9 }),
    ],
    [
      rs("c", 10, 40, ["std::thread::sleep(d);            // ✗ блокирует", "tokio::time::sleep(d).await;      // ✓ только задача"], [1], { ...code, bad: [0], lh: 22 }),
    ],
  ],
});

// 2. sleep и Instant
export const V02 = scene({
  labels: ["sleep", "sleep_until", "Монотонность"],
  caption: [
    "sleep(100 мс): завершится не раньше срока, но может чуть позже",
    "sleep_until(t) ждёт до момента t — удобно для общего дедлайна",
    "Instant монотонен: не зависит от перевода часов; elapsed() показывает прошедшее",
  ],
  frames: [
    [rs("c", 10, 14, ["sleep(Duration::from_millis(100)).await;"], [0], code), ...axis(110), span("s", 0, 100, 80, "sleep 100 мс")],
    [rs("c", 10, 14, ["let t = Instant::now() + Duration::from_millis(150);", "sleep_until(t).await;"], [1], code), ...axis(110), span("s", 0, 150, 80, "sleep_until(start + 150 мс)")],
    [rs("c", 10, 14, ["let start = Instant::now();", "work().await;", "println!(\"{:?}\", start.elapsed());"], [2], { ...code, lh: 15 }), Box("g", 180, 110, 240, 26, "Instant: только вперёд", "g", { size: 10 })],
  ],
});

// 3. timeout
export const V03 = scene({
  labels: ["Успел", "Не успел", "Цепочка"],
  caption: [
    "Фьючер уложился в срок — получаем Ok(значение)",
    "Срок вышел — Err(Elapsed), а фьючер отбрасывается",
    "Таймаут можно поставить на целую цепочку шагов; побочные эффекты не откатываются",
  ],
  frames: [
    [rs("c", 10, 14, ["timeout(ms(200), fetch()).await"], [0], code), ...axis(110), span("f", 0, 80, 80, "fetch"), Box("r", 280, 80, 80, 26, "Ok(..)", "g", { size: 10 })],
    [rs("c", 10, 14, ["timeout(ms(100), fetch()).await"], [0], code), ...axis(110), span("f", 0, 100, 80, "fetch…", "r"), Box("r", 280, 80, 90, 26, "Err(Elapsed)", "r", { size: 9.5 })],
    [rs("c", 10, 14, ["timeout(ms(300), async {", "    let a = step1().await;", "    step2(a).await", "}).await"], [0, 3], { ...code, lh: 14 }), Box("n", 180, 120, 250, 26, "один срок на оба шага", "g", { size: 9.5 })],
  ],
});

// 4. interval
export const V04 = scene({
  labels: ["Создание", "Тики", "Без дрейфа"],
  caption: [
    "interval(100 мс) создаёт расписание; первый tick() срабатывает сразу",
    "Дальше тики идут каждые 100 мс от момента запуска",
    "Работа внутри тика не сдвигает расписание: пауза сокращается сама",
  ],
  frames: [
    [rs("c", 10, 14, ["let mut iv = interval(ms(100));", "iv.tick().await;   // сразу"], [1], code), ...axis(110), tick("k0", 0, 85)],
    [rs("c", 10, 14, ["loop { iv.tick().await; work(); }"], [0], code), ...axis(110), tick("k0", 0, 85), tick("k1", 100, 85), tick("k2", 200, 85), tick("k3", 300, 85)],
    [rs("c", 10, 14, ["loop { iv.tick().await; work(); }"], [0], code), ...axis(110), tick("k0", 0, 85), tick("k1", 100, 85), tick("k2", 200, 85), span("w1", 0, 60, 62, "work", "y", 14), span("w2", 100, 140, 62, "work", "y", 14), note("n", 270, 45, "ритм ровный", "g")],
  ],
});

// 5. Пропущенные тики
export const V05 = scene({
  labels: ["Опоздание", "Burst и Delay", "Skip"],
  caption: [
    "Работа заняла 180 мс при периоде 100 — тик на 100-й мс пропущен",
    "Burst нагоняет подряд (180, 200, 300); Delay сдвигает расписание (180, 280)",
    "Skip отбрасывает пропущенный тик и ждёт ближайший по исходной сетке (200, 300)",
  ],
  frames: [
    [span("w", 0, 180, 50, "work 180 мс", "y"), tick("k1", 100, 90, "r"), note("n", 180, 150, "тик 100 пропущен", "r"), ...axis(110)],
    [
      note("b", 14, 30, "Burst", "g", { anchor: "start" }),
      tick("b1", 180, 48), tick("b2", 200, 48), tick("b3", 300, 48),
      note("d", 14, 76, "Delay", "g", { anchor: "start" }),
      tick("d1", 180, 94), tick("d2", 280, 94),
      ...axis(125),
    ],
    [
      note("s", 14, 36, "Skip", "g", { anchor: "start" }),
      tick("s1", 200, 56), tick("s2", 300, 56),
      note("x", 180, 96, "100 пропущен,\nследующий — 200", "g"),
      ...axis(125),
    ],
  ],
});

// 6. Дедлайны и сброс
export const V06 = scene({
  labels: ["Общий дедлайн", "timeout_at", "reset"],
  caption: [
    "Дедлайн — момент: три шага делят один общий срок и не растягивают его",
    "timeout_at ограничивает каждый шаг тем же моментом",
    "Sleep после pin! можно сбросить: каждый приход данных отодвигает срок простоя",
  ],
  frames: [
    [...axis(110), span("a", 0, 90, 50, "шаг 1", "b"), span("b", 90, 180, 50, "шаг 2", "b"), span("c", 180, 270, 50, "шаг 3", "b"), note("d", 270, 80, "дедлайн", "r"), { t: "line", id: "dl", x1: X(270), y1: 30, x2: X(270), y2: 110, c: "r", dash: true }],
    [rs("c", 10, 14, ["let end = Instant::now() + secs(5);", "timeout_at(end, step1()).await?;", "timeout_at(end, step2()).await?;"], [1, 2], { ...code, lh: 14 })],
    [rs("c", 10, 14, ["let mut idle = pin!(sleep(secs(30)));", "…", "idle.as_mut().reset(Instant::now() + secs(30));"], [2], { ...code, lh: 15 }), note("n", 180, 100, "каждый пакет продлевает срок", "g")],
  ],
});

// 7. Время в тестах
export const V07 = scene({
  labels: ["Настоящее ожидание", "Пауза времени", "advance"],
  caption: [
    "Тест на часовой таймаут ждал бы час — медленно и ненадёжно",
    "С test-util время стоит; когда все задачи ждут, оно мгновенно перематывается",
    "advance(d) перематывает время вручную; тест проходит за миллисекунды",
  ],
  frames: [
    [Box("a", 180, 70, 300, 30, "тест ждёт 3600 секунд…", "r", { size: 10 })],
    [rs("c", 10, 14, ["#[tokio::test(start_paused = true)]", "async fn t() { sleep(hours(1)).await; }"], [0], { ...code, lh: 16 }), Box("g", 180, 100, 200, 26, "проходит за мс", "g", { size: 10 })],
    [rs("c", 10, 14, ["time::pause();", "time::advance(secs(10)).await;"], [1], { ...code, lh: 16 }), Box("g", 180, 100, 240, 26, "feature = \"test-util\"", "y", { size: 9.5 })],
  ],
});

// 8. select!
export const V08 = scene({
  labels: ["Два фьючера", "Победитель", "Проигравший"],
  caption: [
    "select! запускает ожидание обоих фьючеров — в одной задаче",
    "Первый завершившийся выигрывает: выполняется его блок кода",
    "Второй фьючер отбрасывается — его работа прекращается",
  ],
  frames: [
    [rs("c", 10, 14, ["select! {", "    v = a() => println!(\"{v}\"),", "    _ = sleep(ms(50)) => println!(\"тайм-аут\"),", "}"], undefined, { ...code, lh: 14 }), ...axis(120), span("a", 0, 200, 95, "a()", "b", 16), span("t", 0, 50, 75, "sleep", "b", 16)],
    [rs("c", 10, 14, ["select! {", "    v = a() => println!(\"{v}\"),", "    _ = sleep(ms(50)) => println!(\"тайм-аут\"),", "}"], [2], { ...code, lh: 14 }), ...axis(120), span("a", 0, 200, 95, "a()", "b", 16), span("t", 0, 50, 75, "sleep", "g", 16)],
    [rs("c", 10, 14, ["select! {", "    v = a() => println!(\"{v}\"),", "    _ = sleep(ms(50)) => println!(\"тайм-аут\"),", "}"], [2], { ...code, lh: 14 }), ...axis(120), span("a", 0, 50, 95, "a() ✗", "r", 16), span("t", 0, 50, 75, "sleep", "g", 16)],
  ],
});

// 9. Ветки select!
export const V09 = scene({
  labels: ["if", "else", "biased"],
  caption: [
    "if после фьючера отключает ветку на этой итерации; не совпал образец — тоже",
    "Когда отключены все ветки — выполняется else; без него макрос паникует",
    "По умолчанию порядок опроса случаен; biased; опрашивает сверху вниз",
  ],
  frames: [
    [rs("c", 10, 14, ["select! {", "    x = rx.recv(), if open => handle(x),", "    _ = tick.tick() => beat(),", "}"], [1], { ...code, lh: 14, size: 9 })],
    [rs("c", 10, 14, ["select! {", "    Some(x) = rx.recv() => handle(x),", "    else => break,", "}"], [2], { ...code, lh: 14 }), note("n", 180, 100, "канал закрыт → else", "g")],
    [rs("c", 10, 14, ["select! {", "    biased;", "    _ = shutdown.recv() => break,", "    x = rx.recv() => handle(x),", "}"], [1, 2], { ...code, lh: 14 }), note("n", 290, 100, "остановка\nпервой", "g")],
  ],
});

// 10. Безопасность отмены
export const V10 = scene({
  labels: ["recv безопасен", "read_exact небезопасен", "Читайте документацию"],
  caption: [
    "recv() отбросили — сообщение осталось в канале, ничего не потеряно",
    "read_exact успел прочитать 3 из 8 байт и отброшен — эти 3 байта потеряны",
    "У каждой функции tokio есть раздел «Cancel safety» — читайте перед select!",
  ],
  frames: [
    [Box("ch", 90, 70, 110, 34, "канал: [A][B]", "b", { size: 10 }), arrow("e", 150, 70, 200, 70, "m"), Box("f", 270, 70, 120, 34, "recv() отброшен", "m", { size: 9.5 }), note("n", 180, 120, "сообщения на месте ✓", "g")],
    [Box("ch", 90, 70, 130, 34, "поток: ■■■□□□□□", "b", { size: 10 }), Box("f", 280, 70, 130, 34, "read_exact ✗", "r", { size: 10 }), note("n", 180, 120, "3 байта прочитаны и потеряны", "r")],
    [Box("a", 90, 70, 150, 36, "Cancel safety:\nyes", "g", { size: 10 }), Box("b", 270, 70, 150, 36, "Cancel safety:\nno", "r", { size: 10 })],
  ],
});

// 11. select! в цикле
export const V11 = scene({
  labels: ["Пересоздание", "pin! и &mut", "Три источника"],
  caption: [
    "Фьючер, созданный в каждой итерации, начинает работу заново — прогресс теряется",
    "Создаём до цикла, закрепляем pin! и передаём по &mut — продолжится с того же места",
    "Типичный цикл: сообщения, периодический сигнал и остановка",
  ],
  frames: [
    [rs("c", 10, 14, ["loop {", "    select! {", "        _ = sleep(secs(1)) => …,   // заново каждый раз", "        x = rx.recv() => …,", "    }", "}"], [2], { ...code, lh: 14, size: 9 })],
    [rs("c", 10, 14, ["let sl = pin!(sleep(secs(1)));", "loop {", "    select! {", "        _ = &mut sl => break,", "        x = rx.recv() => …,", "    }", "}"], [0, 3], { ...code, lh: 14, size: 9.5 })],
    [Box("a", 70, 60, 100, 30, "канал", "b", { size: 10 }), Box("b", 180, 60, 100, 30, "тик", "b", { size: 10 }), Box("c", 290, 60, 100, 30, "стоп", "r", { size: 10 }), Box("s", 180, 120, 160, 30, "select! в loop", "g", { size: 10 }), arrow("e1", 100, 76, 150, 108, "m"), arrow("e2", 180, 76, 180, 106, "m"), arrow("e3", 260, 76, 210, 108, "m")],
  ],
});

// 12. Повторы и пауза
export const V12 = scene({
  labels: ["Попытки с timeout", "Растущая пауза", "Предел"],
  caption: [
    "На каждую попытку — таймаут: зависший вызов не блокирует всё",
    "Паузы растут вдвое: 100, 200, 400 мс; к ним добавляют случайный разброс",
    "Число попыток ограничено: после последней неудачи возвращаем ошибку",
  ],
  frames: [
    [...axis(110), span("a1", 0, 40, 70, "1", "r", 20), span("a2", 80, 120, 70, "2", "r", 20), span("a3", 200, 240, 70, "3", "g", 20)],
    [...axis(110), span("a1", 0, 40, 70, "1", "r", 20), span("p1", 40, 80, 50, "100", "y", 14), span("a2", 80, 120, 70, "2", "r", 20), span("p2", 120, 200, 50, "200", "y", 14), span("a3", 200, 240, 70, "3", "g", 20)],
    [rs("c", 10, 14, ["for n in 0..5 {", "    if let Ok(v) = timeout(ms(50), op()).await { return v; }", "    sleep(delay << n).await;", "}", "Err(Error::GaveUp)"], [4], { ...code, lh: 14, size: 9 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Время", "select!", "Дальше"],
  caption: [
    "sleep, timeout, interval, дедлайны — управление временем без блокировки потока",
    "select!: первый победил, остальные отброшены; помните о безопасности отмены",
    "Следующая тема — каналы и синхронизация между задачами",
  ],
  frames: [
    [Box("a", 65, 60, 110, 30, "sleep", "g", { size: 10 }), Box("b", 180, 60, 110, 30, "timeout", "g", { size: 10 }), Box("c", 295, 60, 110, 30, "interval", "g", { size: 10 })],
    [Box("a", 90, 60, 130, 30, "select!", "g", { size: 11 }), Box("b", 270, 60, 130, 30, "cancel safety", "y", { size: 10 })],
    [rs("c", 20, 50, ["let (tx, mut rx) = mpsc::channel(8);"], [0], { ...code, size: 10.5, lh: 20 }), arrow("a", 180, 100, 180, 124, "g")],
  ],
});
