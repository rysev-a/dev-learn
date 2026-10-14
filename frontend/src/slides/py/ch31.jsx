// Слайды для «Изучаем Python», глава 31 — «Конкурентность: потоки, процессы и GIL».
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
      <span>ИЗУЧАЕМ ПИТОН / АСИНХРОННОСТЬ / ГЛАВА 31</span>
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
      title={"Конкурентность"}
      sub={"Глава 31 · Асинхронность"}
      main={"Сначала выясните, что тормозит: вычисления или ожидание — от этого зависит инструмент."}
    >
      <div className="s-grid2">
        {[["threading", "Потоки", "Общая память; хороши для ожидания"], ["GIL", "Блокировка", "Чистые вычисления потоки не ускоряют"], ["concurrent.futures", "Пулы", "map, submit, Future"], ["multiprocessing", "Процессы", "Для вычислений; данные копируются"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <p className="s-hint">{"Конкурентность — задачи идут вперемешку; параллельность — одновременно на разных ядрах."}</p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Потоки"}
      sub={"Thread, start, join"}
      main={"Ожидания идут одновременно: три потока по 0,2 с занимают около 0,2 с, а не 0,6."}
    >
      <PyCode>{`import threading
import time

results = []

def work(name):
    time.sleep(0.2)
    results.append(name)

start = time.perf_counter()
threads = [threading.Thread(target=work, args=(n,)) for n in "abc"]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(sorted(results), time.perf_counter() - start < 0.5)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['a', 'b', 'c'] True"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Гонка и Lock"}
      sub={"Общая память — источник бед"}
      main={"Берите замок через with: он снимется сам, даже если внутри случится ошибка."}
    >
      <PyCode>{`import threading

count = 0
lock = threading.Lock()

def inc(n):
    global count
    for _ in range(n):
        with lock:
            count += 1

threads = [threading.Thread(target=inc, args=(50000,)) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(count)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"200000"}</Cmd>
      <div className="s-note">{"Без замка результат был бы меньше и каждый раз разный: «прочитать, прибавить, записать» не неделимо."}</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"GIL"}
      sub={"Глобальная блокировка интерпретатора"}
      main={"GIL отпускается на ожидании: потоки — для ввода-вывода, процессы — для вычислений."}
    >
      <PyCode>{`import sys

print(hasattr(sys, "_is_gil_enabled"), sys._is_gil_enabled())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True True"}</Cmd>
      <div className="s-cols">
        <Node kind="green" mono={true} title={"ввод-вывод"} sub={"Сеть, диск, сон — потоки ускоряют"} />
        <Node kind="amber" mono={true} title={"вычисления"} sub={"Чистый Python — потоки не помогают"} />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"ThreadPoolExecutor"}
      sub={"map, submit, as_completed"}
      main={"Исключение из задачи хранится во фьючере и поднимается при чтении результата."}
    >
      <PyCode>{`from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def fetch(n):
    time.sleep(0.1)
    return n * n

def boom():
    raise ValueError("сбой")

with ThreadPoolExecutor(max_workers=4) as pool:
    print(list(pool.map(fetch, [1, 2, 3, 4])))
    futures = [pool.submit(fetch, n) for n in (5, 6)]
    print(sorted(f.result() for f in as_completed(futures)))
    try:
        pool.submit(boom).result()
    except ValueError as e:
        print("из потока:", e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[1, 4, 9, 16]\n[25, 36]\nиз потока: сбой"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Процессы"}
      sub={"ProcessPoolExecutor: тот же интерфейс"}
      main={"Аргументы и результаты должны сериализоваться; запуск защищайте проверкой главного модуля."}
    >
      <div className="s-cols">
        <Node kind="" mono={true} title={"with ProcessPoolExecutor() as pool:"} sub={"тот же map и submit, что у потоков"} />
        <Node kind="green" mono={true} title={"if __name__ == \"__main__\":"} sub={"обязательно: иначе дочерние процессы запустят сами себя"} />
        <Node kind="amber" mono={true} title={"лямбды, замыкания"} sub={"через границу процессов не проходят"} />
      </div>
      <div className="s-note">{"У каждого процесса свой интерпретатор и свой GIL: на нескольких ядрах вычисления идут действительно параллельно."}</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Очереди"}
      sub={"Производитель и потребитель"}
      main={"Очередь потокобезопасна: меньше общего состояния — меньше гонок."}
    >
      <PyCode>{`import queue
import threading

q = queue.Queue()
results = []

def consumer():
    while True:
        item = q.get()
        if item is None:          # сигнал остановки
            break
        results.append(item * 2)

t = threading.Thread(target=consumer)
t.start()
for i in range(5):
    q.put(i)
q.put(None)
t.join()
print(results)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[0, 2, 4, 6, 8]"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Event и Semaphore"}
      sub={"Сигналы и ограничения"}
      main={"Никогда не ждите вечно: у ожиданий есть таймаут."}
    >
      <PyCode>{`import threading
import time

stop = threading.Event()
ticks = []

def worker():
    while not stop.is_set():
        ticks.append(1)
        stop.wait(0.05)

t = threading.Thread(target=worker)
t.start()
time.sleep(0.2)
stop.set()
t.join()
print(len(ticks) >= 2, stop.is_set())

sem = threading.Semaphore(2)
print(sem.acquire(), sem.acquire(), sem.acquire(timeout=0.05))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True True\nTrue True False"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Детали потоков"}
      sub={"Имена, локальные данные, фоновые потоки"}
      main={"Остановить поток снаружи нельзя — только попросить через Event."}
    >
      <PyCode>{`import threading

local = threading.local()

def work(n):
    local.value = n
    print(local.value, threading.current_thread().name)

t = threading.Thread(target=work, args=(7,), name="рабочий")
t.start()
t.join()
print(hasattr(local, "value"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"7 рабочий\nFalse"}</Cmd>
      <div className="s-note">{"daemon=True — поток не мешает завершению программы; обычные потоки программа ждёт."}</div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Как выбрать"}
      sub={"Три вопроса"}
      main={"Чаще всего достаточно пула потоков для сети и пула процессов для расчётов."}
    >
      <div className="s-cols">
        <Node kind="" mono={true} title={"Что тормозит?"} sub={"ожидание → потоки / asyncio; вычисления → процессы"} />
        <Node kind="" mono={true} title={"Сколько дел сразу?"} sub={"десятки → потоки; тысячи соединений → asyncio"} />
        <Node kind="" mono={true} title={"Нужна общая память?"} sub={"потоки — да; процессы — нет, данные копируются"} />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Измеряйте"}
      sub={"perf_counter до и после"}
      main={"Закон Амдала: неделимая часть работы ограничивает выигрыш; для мелочи пул — вред."}
    >
      <PyCode>{`import time
from concurrent.futures import ThreadPoolExecutor

def request(_):
    time.sleep(0.1)

t0 = time.perf_counter()
for i in range(10):
    request(i)
seq = time.perf_counter() - t0

t0 = time.perf_counter()
with ThreadPoolExecutor(10) as pool:
    list(pool.map(request, range(10)))
par = time.perf_counter() - t0
print(seq > 0.9, par < 0.5, seq / par > 3)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True True True"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Исключение в потоке не доходит до основного"}
      main={"Без фьючера ошибка потока только печатается — и вы можете её не заметить."}
    >
      <PyCode>{`import threading

def broken():
    raise ValueError("сбой")

t = threading.Thread(target=broken)
t.start()
t.join()
print("основной поток дожил:", t.is_alive())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"основной поток дожил: False"}</Cmd>
      <div className="s-note">{"Ещё: гонки без замка, забытый join, взаимная блокировка, потоки для вычислений, лямбды в процессах, ожидание в очереди без сигнала остановки."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 31 · Асинхронность"}
      main={"Для ожидания — потоки, для расчётов — процессы, для тысяч соединений — asyncio."}
    >
      <div className="s-grid2">
        {[["Thread · Lock", "Потоки", "Общие данные — под замком или через Queue"], ["GIL", "Ограничение", "Один поток исполняет байткод; на ожидании отпускается"], ["ThreadPool · ProcessPool", "Пулы", "map, submit, Future, as_completed"], ["Event · Semaphore", "Синхронизация", "Сигналы, ограничения, таймауты"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — asyncio: тысячи дел в одном потоке."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P31 = {
  "13:31": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P31).
export const SLIDE_TITLES_P31 = {
  "13:31": [
    "Конкурентность",
    "Потоки",
    "Гонка и Lock",
    "GIL",
    "Пул потоков",
    "Процессы",
    "Очереди",
    "Event и Semaphore",
    "Детали потоков",
    "Как выбрать",
    "Измеряйте",
    "Типичные ошибки",
    "Итог",
  ],
};
