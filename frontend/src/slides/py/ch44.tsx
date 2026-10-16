import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, Node, PyCode } from "../widgets.tsx";
// Слайды для «Python как первый язык», глава 44 — «asyncio: корутины и async/await».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / АСИНХРОННОСТЬ / ГЛАВА 44", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"asyncio"}
      sub={"Глава 44 · Асинхронность"}
      main={"Один поток, тысячи дел: корутины добровольно уступают управление на await."}
    >
      <div className="s-grid2">
        {[["async def · await", "Корутины", "Заготовка работы и точка переключения"], ["create_task · gather", "Конкурентность", "Задачи и ожидание нескольких"], ["timeout · cancel", "Время", "Таймауты и отмена"], ["Queue · Semaphore", "Взаимодействие", "Очереди и ограничения"]].map(([big, t, d]) => (
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
      title={"Корутина"}
      sub={"async def и asyncio.run"}
      main={"Вызов async-функции не выполняет тело: он возвращает корутину, которую нужно запустить."}
    >
      <PyCode>{`import asyncio

async def hello(name):
    return f"привет, {name}"

coro = hello("Аня")
print(type(coro).__name__)
print(asyncio.run(coro))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"coroutine\nпривет, Аня"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"await и asyncio.sleep"}
      sub={"Точка переключения"}
      main={"time.sleep внутри async-функции замораживает весь цикл событий — используйте asyncio.sleep."}
    >
      <PyCode>{`import asyncio
import time

async def main():
    start = time.perf_counter()
    await asyncio.sleep(0.1)
    await asyncio.sleep(0.1)
    return time.perf_counter() - start

print(asyncio.run(main()) >= 0.2)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True"}</Cmd>
      <div className="s-note">{"Два await подряд — последовательно: чтобы дела накладывались, нужны задачи."}</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Задачи"}
      sub={"create_task ставит корутину в расписание"}
      main={"Три ожидания по 0,2 с накладываются: около 0,2 с вместо 0,6. Ссылку на задачу сохраняйте."}
    >
      <PyCode>{`import asyncio
import time

async def job(name, delay):
    await asyncio.sleep(delay)
    return name

async def main():
    start = time.perf_counter()
    tasks = [asyncio.create_task(job(n, 0.2)) for n in "abc"]
    results = [await t for t in tasks]
    return results, time.perf_counter() - start < 0.5

print(asyncio.run(main()))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(['a', 'b', 'c'], True)"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"gather"}
      sub={"Результаты — в порядке передачи"}
      main={"return_exceptions=True превращает ошибки в элементы результата — разбираете сами."}
    >
      <PyCode>{`import asyncio

async def fetch(n):
    await asyncio.sleep(0.3 - n * 0.1)
    if n == 2:
        raise ValueError("сбой")
    return n * 10

async def main():
    print(await asyncio.gather(fetch(0), fetch(1)))
    res = await asyncio.gather(*(fetch(n) for n in range(4)), return_exceptions=True)
    print(res)

asyncio.run(main())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[0, 10]\n[0, 10, ValueError('сбой'), 30]"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Таймаут и отмена"}
      sub={"asyncio.timeout и task.cancel"}
      main={"CancelledError не глотайте; finally выполнится и при отмене — для уборки."}
    >
      <PyCode>{`import asyncio

async def slow():
    try:
        await asyncio.sleep(10)
    finally:
        print("уборка")

async def main():
    try:
        async with asyncio.timeout(0.1):
            await slow()
    except TimeoutError:
        print("таймаут")
    t = asyncio.create_task(slow())
    await asyncio.sleep(0.05)
    t.cancel()
    try:
        await t
    except asyncio.CancelledError:
        print("отменена", t.cancelled())

asyncio.run(main())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"уборка\nтаймаут\nуборка\nотменена True"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"TaskGroup"}
      sub={"Структурная конкурентность"}
      main={"Упала одна задача — остальные отменяются, а ошибки собираются в группу (except*)."}
    >
      <PyCode>{`import asyncio

async def ok(n):
    await asyncio.sleep(0.05)
    return n

async def bad():
    await asyncio.sleep(0.01)
    raise ValueError("сбой")

async def main():
    async with asyncio.TaskGroup() as tg:
        a = tg.create_task(ok(1))
        b = tg.create_task(ok(2))
    print(a.result(), b.result())
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(ok(3))
            tg.create_task(bad())
    except* ValueError as eg:
        print("группа:", [str(e) for e in eg.exceptions])

asyncio.run(main())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 2\nгруппа: ['сбой']"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"async for и async with"}
      sub={"Асинхронные итераторы, генераторы, менеджеры"}
      main={"Методы с приставкой «а»: __anext__, __aenter__, __aexit__."}
    >
      <PyCode>{`import asyncio

async def ticker(n):
    for i in range(n):
        await asyncio.sleep(0.01)
        yield i

class Conn:
    async def __aenter__(self):
        print("открыли")
        return self
    async def __aexit__(self, *exc):
        print("закрыли")

async def main():
    async with Conn():
        async for x in ticker(3):
            print(x)
    print([x async for x in ticker(2)])

asyncio.run(main())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"открыли\n0\n1\n2\nзакрыли\n[0, 1]"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"asyncio.Queue"}
      sub={"Пул воркеров"}
      main={"Без замков и гонок: переключение происходит только на await. maxsize замедляет производителя."}
    >
      <PyCode>{`import asyncio

async def worker(name, q, out):
    while True:
        item = await q.get()
        out.append((name, item * 2))
        q.task_done()

async def main():
    q, out = asyncio.Queue(), []
    workers = [asyncio.create_task(worker(n, q, out)) for n in "ab"]
    for i in range(5):
        await q.put(i)
    await q.join()
    for w in workers:
        w.cancel()
    print(sorted(item for _, item in out))

asyncio.run(main())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[0, 2, 4, 6, 8]"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Semaphore"}
      sub={"Не больше N одновременно"}
      main={"Потоковые замки здесь не годятся: они блокируют цикл. Используйте asyncio-версии."}
    >
      <PyCode>{`import asyncio

active = peak = 0

async def request(sem):
    global active, peak
    async with sem:
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0.02)
        active -= 1

async def main():
    sem = asyncio.Semaphore(3)
    await asyncio.gather(*(request(sem) for _ in range(10)))
    print(peak)

asyncio.run(main())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Блокирующий код: to_thread"}
      sub={"Вынести наружу цикла событий"}
      main={"Цикл отвечает за ожидание; блокирующую работу — в потоки или процессы."}
    >
      <PyCode>{`import asyncio
import time

def blocking():
    time.sleep(0.2)
    return "готово"

async def main():
    start = time.perf_counter()
    results = await asyncio.gather(*(asyncio.to_thread(blocking) for _ in range(5)))
    print(results[0], len(results), time.perf_counter() - start < 0.8)

asyncio.run(main())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"готово 5 True"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Забытый await"}
      main={"Блокирующий вызов в корутине подводит всех остальных; корутина без await не выполнится."}
    >
      <PyCode>{`import asyncio
import gc
import warnings

async def work():
    return 1

async def main():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        work()                       # забыли await
        gc.collect()
    print(len(w) >= 1, "never awaited" in str(w[0].message))
    print(await work())

asyncio.run(main())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True True\n1"}</Cmd>
      <div className="s-note">{"Ещё: asyncio.run внутри цикла, потерянная ссылка на задачу, проглоченный CancelledError, тысячи задач без ограничения, ожидание без таймаута."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 44 · Асинхронность"}
      main={"Модель кооперативная: корутина должна уступать — иначе подведёт всех."}
    >
      <div className="s-grid2">
        {[["async def · await", "Основа", "asyncio.run запускает цикл событий"], ["create_task · gather · TaskGroup", "Конкурентность", "Задачи, порядок результатов, структурность"], ["timeout · cancel", "Время", "Не ждать вечно; отмену не глотать"], ["Queue · Semaphore · to_thread", "Приёмы", "Воркеры, лимиты, блокирующий код"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — asyncio на практике: сеть, структура программы, тесты, веб."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P44 = {
  "13:44": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P44).
export const SLIDE_TITLES_P44 = {
  "13:44": [
    "asyncio",
    "Корутина",
    "await и sleep",
    "Задачи",
    "gather",
    "Таймаут и отмена",
    "TaskGroup",
    "async for и async with",
    "Queue",
    "Semaphore",
    "to_thread",
    "Типичные ошибки",
    "Итог",
  ],
};
