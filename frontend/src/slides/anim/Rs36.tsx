import { scene } from "./alg.tsx";
import { Box, arrow, note, rs } from "./rs.tsx";

/* Глава 36 книги «Изучаем Rust»: Tokio — сеть и асинхронный ввод-вывод. */

const code = { w: 340, size: 9.5, lh: 14 };
const bytes = (pre: string, x: number, y: number, items: (string | number)[], c = "b", w = 22) =>
  items.map((t, i) => Box(`${pre}${i}`, x + i * (w + 4), y, w, 20, t, c, { size: 9 }));

// 1. Ввод-вывод без блокировок
export const V01 = scene({
  labels: ["Поток на клиента", "Задача на клиента", "epoll"],
  caption: [
    "10 000 клиентов — 10 000 потоков и гигабайты памяти",
    "Ждущая задача спит и не занимает поток: потоков — единицы",
    "ОС сообщает токио (epoll/kqueue), какой сокет готов",
  ],
  frames: [
    [...[0, 1, 2, 3, 4, 5].map((i) => Box(`t${i}`, 40 + i * 56, 70, 48, 40, "поток", "r", { size: 8.5 })), note("n", 180, 130, "память на стеки: гигабайты", "r")],
    [Box("th", 70, 80, 90, 50, "1–4 потока", "g", { size: 10 }), ...[0, 1, 2, 3, 4, 5].map((i) => Box(`c${i}`, 190 + (i % 3) * 50, 55 + Math.floor(i / 3) * 50, 44, 34, `задача ${i + 1}`, "b", { size: 8 }))],
    [Box("os", 70, 80, 90, 44, "ядро ОС\nepoll", "b", { size: 10 }), arrow("e", 120, 80, 156, 80, "g"), Box("tk", 220, 80, 110, 44, "tokio\nпланировщик", "g", { size: 10 }), note("n", 180, 130, "готов сокет 7 → разбудить задачу", "g")],
  ],
});

// 2. Слушаем и подключаемся
export const V02 = scene({
  labels: ["bind и accept", "Порт 0", "connect"],
  caption: [
    "TcpListener::bind(addr).await, потом accept().await ждёт клиента",
    "Порт 0 — ОС выбирает свободный; local_addr() покажет какой",
    "TcpStream::connect(addr).await: клиент и сервер в разных задачах одной программы",
  ],
  frames: [
    [rs("c", 10, 14, ["let l = TcpListener::bind(\"127.0.0.1:8080\").await?;", "let (sock, addr) = l.accept().await?;"], [1], { ...code, size: 9, lh: 18 })],
    [rs("c", 10, 14, ["let l = TcpListener::bind(\"127.0.0.1:0\").await?;", "let port = l.local_addr()?.port();"], [1], { ...code, size: 9, lh: 18 })],
    [Box("c", 70, 80, 100, 34, "клиент\nconnect", "b", { size: 10 }), arrow("e", 125, 80, 235, 80, "g"), Box("s", 290, 80, 100, 34, "сервер\naccept", "b", { size: 10 }), note("n", 180, 120, "127.0.0.1:порт", "m")],
  ],
});

// 3. Читаем и пишем
export const V03 = scene({
  labels: ["read", "Ноль = конец", "write_all"],
  caption: [
    "read(&mut buf) читает сколько есть — возможно, меньше, чем просили",
    "read вернул 0 — собеседник закрыл соединение (EOF)",
    "write_all пишет всё целиком; write может записать лишь часть",
  ],
  frames: [
    [rs("c", 10, 14, ["let mut buf = [0u8; 64];", "let n = sock.read(&mut buf).await?;"], [1], { ...code, lh: 18 }), ...bytes("b", 120, 90, ["п", "р", "и", "в"], "g"), note("n", 180, 126, "n = 4, хотя буфер на 64", "y")],
    [rs("c", 10, 14, ["match sock.read(&mut buf).await? {", "    0 => break,        // EOF", "    n => handle(&buf[..n]),", "}"], [1], { ...code, lh: 16 })],
    [rs("c", 10, 14, ["sock.write_all(b\"hello\").await?;", "sock.flush().await?;"], [0], { ...code, lh: 18 }), note("n", 180, 90, "write_all повторяет write, пока не запишет всё", "g")],
  ],
});

// 4. Эхо-сервер
export const V04 = scene({
  labels: ["Цикл accept", "spawn на клиента", "Задача-обработчик"],
  caption: [
    "Бесконечный цикл: accept() принимает очередного клиента",
    "tokio::spawn запускает отдельную задачу — цикл сразу ждёт следующего",
    "Задача читает и пишет обратно, пока не получит EOF; сокет закроется сам",
  ],
  frames: [
    [rs("c", 10, 14, ["loop {", "    let (sock, _) = listener.accept().await?;", "    // …", "}"], [1], { ...code, lh: 16 })],
    [rs("c", 10, 14, ["loop {", "    let (sock, _) = listener.accept().await?;", "    tokio::spawn(async move { handle(sock).await });", "}"], [2], { ...code, lh: 16, size: 9 })],
    [rs("c", 10, 14, ["async fn handle(mut s: TcpStream) {", "    let mut buf = [0u8; 1024];", "    while let Ok(n) = s.read(&mut buf).await {", "        if n == 0 { break; }", "        s.write_all(&buf[..n]).await.ok();", "    }", "}"], [3, 4], { ...code, lh: 14, size: 9 })],
  ],
});

// 5. Строки и буферы
export const V05 = scene({
  labels: ["BufReader", "lines()", "read_line"],
  caption: [
    "BufReader накапливает прочитанное и отдаёт по строкам",
    "lines().next_line().await — строка без перевода строки; None на конце",
    "read_line дописывает в String и возвращает число байт (0 — конец)",
  ],
  frames: [
    [Box("r", 70, 80, 100, 34, "сокет", "b", { size: 10 }), Box("b", 180, 80, 100, 34, "BufReader\nбуфер", "g", { size: 9.5 }), Box("l", 300, 80, 80, 34, "строки", "b", { size: 10 }), arrow("e1", 120, 80, 130, 80, "m"), arrow("e2", 230, 80, 258, 80, "m")],
    [rs("c", 10, 14, ["let mut lines = BufReader::new(sock).lines();", "while let Some(l) = lines.next_line().await? {", "    println!(\"{l}\");", "}"], [1], { ...code, lh: 16, size: 9 })],
    [rs("c", 10, 14, ["let mut s = String::new();", "let n = reader.read_line(&mut s).await?;", "// n == 0 → конец потока"], [1], { ...code, lh: 18 })],
  ],
});

// 6. Обрамление
export const V06 = scene({
  labels: ["Поток без границ", "Длина + данные", "Разделитель"],
  caption: [
    "Два сообщения слились в одно чтение — границ в TCP нет",
    "4 байта длины, затем ровно столько байт данных",
    "Или разделитель: перевод строки в текстовых протоколах",
  ],
  frames: [
    [...bytes("a", 50, 60, ["H", "e", "l", "l", "o", "W", "o", "r", "l", "d"], "y", 22), note("n", 180, 100, "«Hello» и «World» — одно чтение?", "y")],
    [...bytes("h", 50, 70, [0, 0, 0, 5], "g", 24), ...bytes("d", 160, 70, ["H", "e", "l", "l", "o"], "b", 24), note("n", 180, 110, "заголовок — длина 5, дальше — 5 байт", "g")],
    [...bytes("d", 40, 70, ["H", "e", "l", "l", "o", "\\n", "W", "o", "r", "l", "d", "\\n"], "b", 22), note("n", 180, 110, "\\n отделяет сообщения", "g")],
  ],
});

// 7. split
export const V07 = scene({
  labels: ["Один сокет", "into_split", "Две задачи"],
  caption: [
    "Сокет и читает, и пишет — но заимствовать его в двух местах нельзя",
    "into_split даёт читающую и пишущую половины с владением",
    "Половины уходят в разные задачи: читать и писать одновременно",
  ],
  frames: [
    [Box("s", 180, 80, 120, 44, "TcpStream", "b", { size: 12 })],
    [Box("s", 70, 80, 100, 40, "TcpStream", "b", { size: 10 }), arrow("e", 120, 80, 156, 80, "g"), Box("r", 270, 50, 130, 30, "OwnedReadHalf", "g", { size: 9.5 }), Box("w", 270, 110, 130, 30, "OwnedWriteHalf", "g", { size: 9.5 })],
    [Box("r", 90, 50, 130, 30, "задача: читает", "g", { size: 10 }), Box("w", 90, 110, 130, 30, "задача: пишет", "g", { size: 10 }), Box("s", 290, 80, 100, 40, "сокет", "b", { size: 10 }), arrow("e1", 156, 50, 240, 70, "m"), arrow("e2", 156, 110, 240, 92, "m")],
  ],
});

// 8. Закрытие
export const V08 = scene({
  labels: ["Закрыли запись", "Ответ", "Обрыв"],
  caption: [
    "shutdown() у пишущей половины: «я всё отправил» — собеседник получит EOF",
    "Читающая сторона осталась открытой — можно дождаться ответа",
    "Обрыв: ConnectionReset, BrokenPipe, UnexpectedEof — обрабатываем внутри задачи",
  ],
  frames: [
    [Box("c", 70, 80, 100, 34, "клиент", "b", { size: 10 }), arrow("e", 125, 70, 235, 70, "g"), note("n", 180, 54, "запрос … EOF", "g"), Box("s", 290, 80, 100, 34, "сервер", "b", { size: 10 })],
    [Box("c", 70, 80, 100, 34, "клиент", "b", { size: 10 }), arrow("e", 235, 90, 125, 90, "g"), note("n", 180, 106, "ответ", "g"), Box("s", 290, 80, 100, 34, "сервер", "b", { size: 10 })],
    [rs("c", 10, 14, ["match s.read(&mut buf).await {", "    Err(e) if e.kind() == ConnectionReset => log(e),", "    Err(e) => return Err(e),", "    Ok(n) => …,", "}"], [1], { ...code, lh: 15, size: 9 })],
  ],
});

// 9. UDP
export const V09 = scene({
  labels: ["send_to и recv_from", "Границы сохраняются", "Нет гарантий"],
  caption: [
    "Соединения нет: адрес получателя указывается в каждом send_to",
    "Два отправления — два чтения: слияния и разбиения нет",
    "Потери, повторы и перестановки возможны — надёжность строят выше",
  ],
  frames: [
    [rs("c", 10, 14, ["let s = UdpSocket::bind(\"127.0.0.1:0\").await?;", "s.send_to(b\"ping\", peer).await?;", "let (n, from) = s.recv_from(&mut buf).await?;"], [1, 2], { ...code, lh: 18, size: 9 })],
    [...bytes("a", 60, 60, ["a", "b"], "g", 28), ...bytes("c", 60, 100, ["c", "d"], "g", 28), note("n", 270, 80, "две датаграммы,\nдва recv_from", "g")],
    [Box("a", 90, 60, 140, 28, "потеряна ✗", "r", { size: 10 }), Box("b", 270, 60, 140, 28, "пришла дважды", "y", { size: 10 }), note("n", 180, 110, "игры, видео, поиск в сети", "m")],
  ],
});

// 10. Таймауты и остановка
export const V10 = scene({
  labels: ["Зависшее чтение", "timeout", "Сигнал остановки"],
  caption: [
    "Собеседник замолчал, соединение открыто — задача ждёт вечно",
    "timeout(d, read) ограничивает ожидание: Err(Elapsed)",
    "Цикл accept слушает сигнал остановки: сервер завершается корректно",
  ],
  frames: [
    [Box("t", 180, 80, 240, 40, "read().await …… (тишина)", "r", { size: 11 })],
    [rs("c", 10, 14, ["match timeout(secs(5), s.read(&mut buf)).await {", "    Ok(Ok(n)) => …,", "    Ok(Err(e)) => …,", "    Err(_) => drop(s),   // молчит слишком долго", "}"], [3], { ...code, lh: 15, size: 9 })],
    [rs("c", 10, 14, ["loop {", "    select! {", "        r = listener.accept() => spawn_client(r?),", "        _ = shutdown.recv() => break,", "    }", "}"], [3], { ...code, lh: 15 })],
  ],
});

// 11. Потоки данных
export const V11 = scene({
  labels: ["Stream", "Операции", "copy и duplex"],
  caption: [
    "Stream — асинхронный итератор: next().await даёт значения со временем",
    "StreamExt: map, filter, take, collect; ReceiverStream оборачивает канал",
    "io::copy переливает байты из читателя в писателя; duplex — пара потоков в памяти для тестов",
  ],
  frames: [
    [rs("c", 10, 14, ["let mut s = tokio_stream::iter(1..=3);", "while let Some(x) = s.next().await {", "    println!(\"{x}\");", "}"], [1], { ...code, lh: 16 })],
    [rs("c", 10, 14, ["let v: Vec<_> = iter(1..=10)", "    .filter(|x| x % 2 == 0)", "    .take(3)", "    .collect().await;", "// [2, 4, 6]"], [1, 2, 3], { ...code, lh: 15 })],
    [Box("a", 70, 60, 100, 30, "читатель", "b", { size: 10 }), arrow("e", 120, 60, 156, 60, "g"), Box("b", 290, 60, 100, 30, "писатель", "b", { size: 10 }), rs("c", 10, 106, ["io::copy(&mut r, &mut w).await?;", "let (a, b) = io::duplex(64);   // пара в памяти"], undefined, { ...code, lh: 16, size: 9 })],
  ],
});

// 12. Файлы и блокирующее
export const V12 = scene({
  labels: ["tokio::fs", "spawn_blocking", "DNS и Unix"],
  caption: [
    "Файловые операции идут в пуле потоков; интерфейс привычный",
    "Тяжёлый или блокирующий код — в spawn_blocking: рабочие потоки не замораживаются",
    "lookup_host разрешает имена; UnixListener — сокеты по пути в файловой системе",
  ],
  frames: [
    [rs("c", 10, 14, ["fs::write(\"/tmp/a.txt\", b\"hi\").await?;", "let s = fs::read_to_string(\"/tmp/a.txt\").await?;"], [0, 1], { ...code, lh: 18, size: 9 })],
    [rs("c", 10, 14, ["let h = tokio::task::spawn_blocking(|| {", "    heavy_sum()         // блокирующая работа", "});", "let v = h.await?;"], [0, 1], { ...code, lh: 16 })],
    [rs("c", 10, 14, ["for a in lookup_host(\"example.org:443\").await? { … }", "let l = UnixListener::bind(\"/tmp/s.sock\")?;"], [0, 1], { ...code, lh: 18, size: 9 })],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Сервер и клиент", "Протокол", "Дальше"],
  caption: [
    "accept + spawn на сервере, connect на клиенте; read вернул 0 — конец",
    "TCP — поток: нужны кадры; сплит, shutdown, UDP — по задаче; везде таймауты",
    "Следующая тема — отмена, нагрузка и остановка в настоящем приложении",
  ],
  frames: [
    [Box("a", 65, 60, 110, 28, "accept + spawn", "g", { size: 9.5 }), Box("b", 180, 60, 110, 28, "connect", "g", { size: 10 }), Box("c", 295, 60, 110, 28, "read → 0 = EOF", "g", { size: 9.5 })],
    [Box("a", 65, 60, 110, 28, "кадры: длина", "b", { size: 9.5 }), Box("b", 180, 60, 110, 28, "split  shutdown", "b", { size: 9 }), Box("c", 295, 60, 110, 28, "таймауты", "b", { size: 10 })],
    [rs("c", 20, 50, ["let token = CancellationToken::new();"], [0], { ...code, size: 10.5, lh: 20 }), arrow("a", 180, 100, 180, 124, "g")],
  ],
});
