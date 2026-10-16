// Слайды для «Python как первый язык», глава 45 — «asyncio на практике: сеть, структура, тесты, веб».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const PY_KW = new Set([
  "print", "for", "in", "not", "and", "or", "if", "else", "while", "is",
  "True", "False", "None", "def", "return",
]);

// Крошечный токенизатор Python: комментарии, строки, числа, ключевые слова,
// вызовы функций. Достаточно для слайдов.
function pySpan(src) {
  const out = [];
  const re =
    /(#[^\n]*)|("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')|(\b\d[\d_]*(?:\.\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*)|(\s+|.)/g;
  let m;
  while ((m = re.exec(src)) !== null) {
    const [tok, com, str, num, word] = m;
    if (com) out.push(<span key={out.length} className="rs-com">{tok}</span>);
    else if (str) out.push(<span key={out.length} className="rs-str">{tok}</span>);
    else if (num) out.push(<span key={out.length} className="rs-num">{tok}</span>);
    else if (word) {
      let cls = "";
      if (PY_KW.has(word)) cls = "rs-kw";
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
  return <pre className="rs-code">{pySpan(children)}</pre>;
}

function Rubric({ n }) {
  return (
    <div className="s-rubric">
      <span>PYTHON КАК ПЕРВЫЙ ЯЗЫК / АСИНХРОННОСТЬ / ГЛАВА 45</span>
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
      title={"asyncio на практике"}
      sub={"Глава 45 · Асинхронность"}
      main={"Асинхронность родилась ради сети: большую часть времени программа ждёт чужие ответы."}
    >
      <div className="s-grid2">
        {[["streams", "Сеть", "start_server, open_connection"], ["TaskGroup · Event", "Каркас", "main(), корректная остановка"], ["retry · timeout", "Устойчивость", "Повторы с растущей задержкой"], ["IsolatedAsyncioTestCase", "Тесты", "Корутины на настоящем цикле"]].map(([big, t, d]) => (
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
      title={"Потоки ввода-вывода"}
      sub={"Читатель и писатель"}
      main={"Один поток обслуживает тысячи клиентов: пока обработчик ждёт данных, цикл занят другими."}
    >
      <div className="s-cols">
        <Node kind="" mono={true} title={"await asyncio.open_connection(host, port)"} sub={"клиент: (reader, writer)"} />
        <Node kind="green" mono={true} title={"await asyncio.start_server(handler, host, port)"} sub={"сервер: handler(reader, writer) на каждое подключение"} />
        <Node kind="" mono={true} title={"await reader.readline() · writer.write(...) · await writer.drain()"} sub={"чтение, запись, ожидание отправки"} />
      </div>
      <div className="s-note">{"Готовые веб-клиенты (aiohttp, httpx) построены на тех же принципах: пулы соединений и таймауты."}</div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Эхо-сервер"}
      sub={"Сервер и клиент в одной программе"}
      main={"Порт 0 — «любой свободный»: удобно для примеров и тестов."}
    >
      <PyCode>{`import asyncio

async def handle(reader, writer):
    line = await reader.readline()
    writer.write(line.decode().upper().encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle, "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]
    async with server:
        reader, writer = await asyncio.open_connection("127.0.0.1", port)
        writer.write("привет\\n".encode())
        await writer.drain()
        print((await reader.readline()).decode().strip())
        writer.close()
        await writer.wait_closed()

asyncio.run(main())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"ПРИВЕТ"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Асинхронные подпроцессы"}
      sub={"create_subprocess_exec"}
      main={"Те же правила безопасности: аргументы списком, без склейки из пользовательского ввода, с таймаутом."}
    >
      <PyCode>{`import asyncio
import sys

async def run(code):
    proc = await asyncio.create_subprocess_exec(
        sys.executable, "-c", code, stdout=asyncio.subprocess.PIPE)
    out, _ = await proc.communicate()
    return proc.returncode, out.decode().strip()

async def main():
    print(await asyncio.gather(run("print(1 + 1)"), run("print('привет')")))

asyncio.run(main())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[(0, '2'), (0, 'привет')]"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Каркас программы"}
      sub={"main(), Event остановки, TaskGroup"}
      main={"Один asyncio.run в конце файла; остановка — через событие, а не через «убить задачи»."}
    >
      <PyCode>{`import asyncio

async def worker(name, stop):
    ticks = 0
    try:
        while not stop.is_set():
            ticks += 1
            await asyncio.sleep(0.01)
    finally:
        print(name, "остановлен", ticks > 0)

async def main():
    stop = asyncio.Event()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker("а", stop))
        tg.create_task(worker("б", stop))
        await asyncio.sleep(0.1)
        stop.set()

asyncio.run(main())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"а остановлен True\nб остановлен True"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Шаблон: первый успешный"}
      sub={"asyncio.wait и FIRST_COMPLETED"}
      main={"Ветвление, ограничение семафором, конвейеры на очередях — комбинируются как кирпичики."}
    >
      <PyCode>{`import asyncio

async def source(name, delay):
    await asyncio.sleep(delay)
    return name

async def main():
    tasks = [asyncio.create_task(source(n, d)) for n, d in
             [("медленный", 0.3), ("быстрый", 0.05), ("средний", 0.15)]]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for t in pending:
        t.cancel()
    print(done.pop().result(), len(pending))

asyncio.run(main())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"быстрый 2"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Повторы с задержкой"}
      sub={"Экспоненциальный backoff"}
      main={"Повторять можно только безопасные действия; платёж — нет, пока не уверены, что он не прошёл."}
    >
      <PyCode>{`import asyncio

attempts = []

async def flaky():
    attempts.append(1)
    if len(attempts) < 3:
        raise ConnectionError("нет связи")
    return "успех"

async def retry(func, tries=5, base=0.01):
    for i in range(tries):
        try:
            return await func()
        except ConnectionError:
            if i == tries - 1:
                raise
            await asyncio.sleep(base * 2 ** i)

print(asyncio.run(retry(flaky)), len(attempts))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"успех 3"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Тесты корутин"}
      sub={"IsolatedAsyncioTestCase"}
      main={"Проверяйте логику и порядок событий, а не секунды: тест не должен гоняться с планировщиком."}
    >
      <PyCode>{`import asyncio
import io
import unittest

async def double_later(x):
    await asyncio.sleep(0.01)
    return x * 2

class T(unittest.IsolatedAsyncioTestCase):
    async def test_double(self):
        self.assertEqual(await double_later(21), 42)

    async def test_gather(self):
        self.assertEqual(await asyncio.gather(double_later(1), double_later(2)), [2, 4])

r = unittest.TextTestRunner(stream=io.StringIO()).run(unittest.defaultTestLoader.loadTestsFromTestCase(T))
print(r.testsRun, r.wasSuccessful())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2 True"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Отладка"}
      sub={"debug=True, имена задач, all_tasks"}
      main={"Режим отладки показывает не-ожидавшиеся корутины и долгие блокировки цикла; давайте задачам имена."}
    >
      <PyCode>{`import asyncio

async def job():
    await asyncio.sleep(0.05)

async def main():
    t = asyncio.create_task(job(), name="загрузка")
    await asyncio.sleep(0)
    names = sorted(x.get_name() for x in asyncio.all_tasks() if x is not asyncio.current_task())
    print(names)
    await t

asyncio.run(main(), debug=True)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['загрузка']"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Веб на asyncio"}
      sub={"ASGI и FastAPI"}
      main={"Блокирующий вызов в async-обработчике останавливает весь сервер: ожидание — циклу, блокировку — потокам."}
    >
      <div className="s-cols">
        <Node kind="" mono={true} title={"@app.get(\"/items\")"} sub={"async def handler(): data = await db.fetch(...)"} />
        <Node kind="green" mono={true} title={"await"} sub={"пока обработчик ждёт базу, сервер обслуживает остальных"} />
        <Node kind="amber" mono={true} title={"def handler()"} sub={"обычная функция фреймворк сам запускает в пуле потоков"} />
      </div>
      <div className="s-note">{"Наш бэкенд курса — на FastAPI: те же цикл событий, задачи и ожидания."}</div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"contextvars"}
      sub={"Переменные, своя у каждой задачи"}
      main={"Номер запроса в журнале — без передачи по всем функциям."}
    >
      <PyCode>{`import asyncio
import contextvars

request_id = contextvars.ContextVar("request_id", default="-")

async def log(msg):
    print(request_id.get(), msg)

async def handle(rid):
    request_id.set(rid)
    await asyncio.sleep(0.01)
    await log("обработка")

async def main():
    await asyncio.gather(handle("r1"), handle("r2"))
    await log("снаружи")

asyncio.run(main())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"r1 обработка\nr2 обработка\n- снаружи"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Блокирующий вызов вместо await"}
      main={"Одна блокировка в корутине — и три «параллельных» дела идут по очереди."}
    >
      <PyCode>{`import asyncio
import time

async def bad():
    time.sleep(0.1)

async def good():
    await asyncio.sleep(0.1)

async def run(f):
    t0 = time.perf_counter()
    await asyncio.gather(f(), f(), f())
    return time.perf_counter() - t0

print(asyncio.run(run(bad)) >= 0.3, asyncio.run(run(good)) < 0.25)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True True"}</Cmd>
      <div className="s-note">{"Ещё: нет таймаута на сеть, повтор без паузы, незакрытый writer, нет аккуратной остановки, тысячи задач без ограничения."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 45 · Асинхронность"}
      main={"Вы завершили раздел об асинхронности и всю книгу по Питону — дальше алгоритмы."}
    >
      <div className="s-grid2">
        {[["start_server · open_connection", "Сеть", "Читатель и писатель; подпроцессы корутинами"], ["main() · TaskGroup · Event", "Каркас", "Один run, корректная остановка"], ["timeout · retry", "Устойчивость", "Таймауты и повторы только безопасного"], ["IsolatedAsyncioTestCase", "Тесты и отладка", "debug=True, имена задач, contextvars"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — алгоритмы на Python."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P45 = {
  "13:45": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P45).
export const SLIDE_TITLES_P45 = {
  "13:45": [
    "asyncio на практике",
    "Потоки сети",
    "Эхо-сервер",
    "Подпроцессы",
    "Каркас программы",
    "Первый успешный",
    "Повторы с задержкой",
    "Тесты корутин",
    "Отладка",
    "Веб на asyncio",
    "contextvars",
    "Типичные ошибки",
    "Итог",
  ],
};
