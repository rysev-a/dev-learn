import { scene } from "./alg.jsx";
import { Tx } from "./hw.jsx";
import { Box, arrow } from "./cl.jsx";
import { py } from "./cl.jsx";

/* «Python как первый язык», глава 46: асинхронные итераторы, генераторы и менеджеры контекста. */

// 1. Поток и ожидание
export const V01 = scene({
  labels: ["Поток значений", "Обычный for", "async for"],
  caption: [
    "Страницы ответа, строки из соединения, события брокера: каждый элемент приходит не сразу",
    "Обычный for блокирует: пока ждём элемент, вся программа стоит",
    "async for отдаёт управление циклу событий на время ожидания — другие задачи работают",
  ],
  frames: [
    [
      ...[0, 1, 2, 3].map((i) =>
        Box(`i${i}`, 64 + i * 76, 70, 56, 28, `#${i + 1}`, "b", { size: 11 }),
      ),
      Tx("n", 180, 118, "элементы приходят по одному, с задержками", {
        size: 10,
      }),
    ],
    [
      Box("a", 90, 70, 110, 30, "for x in …", "r", { size: 11.5 }),
      Box("b", 270, 70, 130, 30, "всё стоит, ждём", "r", { size: 10.5 }),
      arrow("e", 146, 70, 204, 70, "r"),
    ],
    [
      Box("a", 90, 56, 120, 28, "async for x in …", "g", { size: 10 }),
      Box("b", 270, 56, 130, 28, "ждём элемент", "g", { size: 10.5 }),
      Box("c", 270, 100, 130, 28, "другие задачи идут", "y", { size: 10 }),
      arrow("e", 152, 56, 204, 56, "g"),
    ],
  ],
});

// 2. Протокол
export const V02 = scene({
  labels: ["__aiter__", "__anext__", "Конец потока"],
  caption: [
    "Асинхронный итератор: __aiter__ возвращает сам итератор",
    "__anext__ — корутина: async for делает await от неё на каждом шаге",
    "Нет элементов — __anext__ поднимает StopAsyncIteration; встроенные aiter() и anext() — с Python 3.10",
  ],
  frames: [
    [
      py(
        "c",
        30,
        56,
        [
          "class Countdown:",
          "    def __init__(self, n): self.n = n",
          "    def __aiter__(self):",
          "        return self",
        ],
        [2, 3],
        {
          size: 11,
          lh: 26,
          w: 320,
        },
      ),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "    async def __anext__(self):",
          "        if self.n <= 0:",
          "            raise StopAsyncIteration",
          "        self.n -= 1",
          "        return self.n + 1",
        ],
        [0],
        {
          size: 10.5,
          lh: 22,
          w: 330,
        },
      ),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "async for x in Countdown(3):",
          "    print(x)          # 3 2 1",
          "it = aiter(obj)",
          "first = await anext(it)",
        ],
        [0, 2, 3],
        {
          size: 11,
          lh: 24,
          w: 320,
        },
      ),
    ],
  ],
});

// 3. Асинхронный генератор
export const V03 = scene({
  labels: ["async def + yield", "await внутри", "Ограничение"],
  caption: [
    "async def с yield внутри — асинхронный генератор: вызов даёт асинхронный итератор",
    "Внутри допустимы и await, и yield; состояние между запросами сохраняется как у обычного генератора",
    "return со значением в асинхронном генераторе — синтаксическая ошибка; пустой return разрешён",
  ],
  frames: [
    [
      py(
        "c",
        30,
        56,
        [
          "async def countdown(n):",
          "    while n > 0:",
          "        yield n",
          "        n -= 1",
        ],
        [0, 2],
        {
          size: 11.5,
          lh: 26,
          w: 300,
        },
      ),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "async def ticks(n):",
          "    for i in range(n):",
          "        await asyncio.sleep(1)",
          "        yield i",
        ],
        [2, 3],
        {
          size: 11.5,
          lh: 26,
          w: 300,
        },
      ),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "async def gen():",
          "    yield 1",
          "    return 42   # SyntaxError",
          "    return      # можно",
        ],
        undefined,
        {
          size: 11.5,
          lh: 26,
          w: 300,
          bad: [2],
        },
      ),
    ],
  ],
});

// 4. Постраничная загрузка
export const V04 = scene({
  labels: ["Страница", "Элементы по одному", "Пустая страница"],
  caption: [
    "Генератор просит у сервера страницу и отдаёт её элементы по одному",
    "Потребитель видит обычный async for по элементам и не думает про страницы; память — на одну страницу",
    "Пустой ответ — конец потока; если потребителю хватило, он выходит из цикла — лишние запросы не происходят",
  ],
  frames: [
    [
      py(
        "c",
        24,
        36,
        [
          "async def items(fetch):",
          "    page = 1",
          "    while True:",
          "        batch = await fetch(page)",
          "        if not batch:",
          "            return",
          "        for x in batch:",
          "            yield x",
          "        page += 1",
        ],
        [3],
        {
          size: 9.5,
          lh: 15,
          w: 330,
        },
      ),
    ],
    [
      Box("p", 70, 70, 80, 36, "страница 1\n[a, b, c]", "b", { size: 8.5 }),
      ...["a", "b", "c"].map((t, i) =>
        Box(`i${i}`, 180 + i * 50, 70, 40, 28, t, "g", { size: 12 }),
      ),
      arrow("e", 112, 70, 152, 70, "g"),
      Tx("n", 230, 116, "async for x in items(fetch)", { size: 10 }),
    ],
    [
      Box("p", 80, 70, 100, 36, "страница 3\n[ ]", "r", { size: 9.5 }),
      Box("e", 270, 70, 120, 30, "конец потока", "m", { size: 11 }),
      arrow("e1", 134, 70, 208, 70, "m"),
    ],
  ],
});

// 5. Асинхронные включения
export const V05 = scene({
  labels: ["async for в списке", "С условием", "Цена"],
  caption: [
    "[x async for x in source()] собирает список из асинхронного источника",
    "Можно добавить условие и await внутри выражения; доступно только внутри async-функции",
    "Результат — целый список в памяти: лень потеряна; удобно в тестах",
  ],
  frames: [
    [
      py(
        "c",
        30,
        56,
        [
          "async def main():",
          "    xs = [x async for x in source()]",
          "    return xs",
        ],
        [1],
        {
          size: 11.5,
          lh: 28,
          w: 320,
        },
      ),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "evens = [x async for x in source()",
          "         if x % 2 == 0]",
          "names = [await get(i) for i in ids]",
        ],
        [0, 1, 2],
        {
          size: 10.5,
          lh: 28,
          w: 330,
        },
      ),
    ],
    [
      Box("a", 90, 70, 110, 30, "лень", "g", { size: 12 }),
      Box("b", 270, 70, 110, 30, "весь список", "r", { size: 11.5 }),
      arrow("e", 146, 70, 214, 70, "r"),
      Tx("n", 180, 118, "в памяти целиком", { size: 10 }),
    ],
  ],
});

// 6. async with
export const V06 = scene({
  labels: ["__aenter__ и __aexit__", "Кто так устроен", "Подавление"],
  caption: [
    "async with вызывает корутины __aenter__ и __aexit__: и открытие, и закрытие могут ждать",
    "Блокировки и семафоры asyncio, TaskGroup, timeout, сетевые соединения, транзакции баз данных",
    "Правила подавления те же: истина из __aexit__ гасит ошибку",
  ],
  frames: [
    [
      py(
        "c",
        24,
        44,
        [
          "class Conn:",
          "    async def __aenter__(self):",
          "        await self.connect()",
          "        return self",
          "    async def __aexit__(self, et, ev, tb):",
          "        await self.close()",
        ],
        [1, 4],
        {
          size: 10,
          lh: 20,
          w: 330,
        },
      ),
    ],
    [
      ...[
        "Lock",
        "Semaphore",
        "TaskGroup",
        "timeout",
        "соединение",
        "транзакция",
      ].map((t, i) =>
        Box(
          `b${i}`,
          62 + (i % 3) * 118,
          54 + Math.floor(i / 3) * 40,
          106,
          26,
          t,
          "g",
          { size: 10.5 },
        ),
      ),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "async def __aexit__(self, et, ev, tb):",
          "    await self.close()",
          "    return et is KeyError   # гасим",
        ],
        [2],
        {
          size: 10.5,
          lh: 26,
          w: 330,
        },
      ),
    ],
  ],
});

// 7. asynccontextmanager и AsyncExitStack
export const V07 = scene({
  labels: ["Декоратор", "try/finally", "AsyncExitStack"],
  caption: [
    "@asynccontextmanager превращает асинхронный генератор в менеджер контекста",
    "До yield — открытие, после — закрытие; try/finally гарантирует уборку при ошибке",
    "AsyncExitStack хранит стопку менеджеров и закрывает их в обратном порядке — для переменного числа ресурсов",
  ],
  frames: [
    [
      py(
        "c",
        24,
        44,
        [
          "@asynccontextmanager",
          "async def connection(url):",
          "    conn = await open_conn(url)",
          "    try:",
          "        yield conn",
          "    finally:",
          "        await conn.close()",
        ],
        [0],
        {
          size: 10,
          lh: 19,
          w: 330,
        },
      ),
    ],
    [
      py(
        "c",
        24,
        44,
        [
          "@asynccontextmanager",
          "async def connection(url):",
          "    conn = await open_conn(url)",
          "    try:",
          "        yield conn",
          "    finally:",
          "        await conn.close()",
        ],
        [2, 4, 6],
        {
          size: 10,
          lh: 19,
          w: 330,
        },
      ),
    ],
    [
      py(
        "c",
        24,
        50,
        [
          "async with AsyncExitStack() as stack:",
          "    for url in urls:",
          "        c = await stack.enter_async_context(",
          "            connection(url))",
          "# закрытие — в обратном порядке",
        ],
        [2, 3],
        {
          size: 10,
          lh: 22,
          w: 330,
        },
      ),
    ],
  ],
});

// 8. Уборка за генератором
export const V08 = scene({
  labels: ["Выход из цикла", "aclose", "aclosing"],
  caption: [
    "break из async for оставляет генератор приостановленным: его finally не выполнится сразу",
    "aclose() вбрасывает GeneratorExit в точку yield — очистка происходит сразу",
    "contextlib.aclosing оформляет это блоком: при выходе вызывается aclose(); asyncio.run при завершении закрывает остатки, но надеяться не стоит",
  ],
  frames: [
    [
      py(
        "c",
        24,
        50,
        [
          "async for x in numbers():",
          "    if x == 2:",
          "        break",
          "# finally внутри numbers() — ещё нет!",
        ],
        [2],
        {
          size: 10.5,
          lh: 24,
          w: 330,
          bad: [3],
        },
      ),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "gen = numbers()",
          "async for x in gen: ...",
          "await gen.aclose()   # очистка сейчас",
        ],
        [2],
        {
          size: 11,
          lh: 26,
          w: 320,
        },
      ),
    ],
    [
      py(
        "c",
        24,
        50,
        [
          "from contextlib import aclosing",
          "async with aclosing(numbers()) as gen:",
          "    async for x in gen:",
          "        if x == 2:",
          "            break",
        ],
        [1],
        {
          size: 10.5,
          lh: 24,
          w: 330,
        },
      ),
    ],
  ],
});

// 9. asend и athrow
export const V09 = scene({
  labels: ["asend", "athrow", "Обычно — очереди"],
  caption: [
    "asend(value) отправляет значение в yield — как send, но его нужно ждать: await gen.asend(1)",
    "athrow(exc) вбрасывает исключение в точку yield; aclose() вбрасывает завершение",
    "Двунаправленные потоки обычно строят на очередях, но механика та же, что у обычных генераторов",
  ],
  frames: [
    [
      py(
        "c",
        30,
        56,
        [
          "x = await gen.asend(10)",
          "# yield получает 10,",
          "# возвращается следующий yield",
        ],
        [0],
        {
          size: 11,
          lh: 26,
          w: 320,
        },
      ),
    ],
    [
      py(
        "c",
        30,
        56,
        ["await gen.athrow(ValueError)", "await gen.aclose()"],
        [0, 1],
        {
          size: 11.5,
          lh: 28,
          w: 320,
        },
      ),
    ],
    [
      Box("a", 90, 70, 110, 30, "asend/athrow", "m", { size: 10.5 }),
      Box("b", 270, 70, 110, 30, "asyncio.Queue", "g", { size: 11 }),
      Tx("n", 180, 118, "в повседневном коде — очереди", { size: 10 }),
    ],
  ],
});

// 10. Конвейеры
export const V10 = scene({
  labels: ["Стадии", "Давление назад", "Очередь между стадиями"],
  caption: [
    "Источник → преобразование → пачки → запись: каждая стадия — async for по предыдущей",
    "Каждое значение производится, только когда потребитель его запросил — естественное давление назад",
    "Нужна настоящая параллельность стадий — между ними ставят очередь; несколько потоков сливают в один через общую очередь",
  ],
  frames: [
    [
      ...["источник", "map", "batched", "запись"].map((t, i) =>
        Box(`b${i}`, 52 + i * 86, 70, 70, 28, t, "g", { size: 10 }),
      ),
      ...[0, 1, 2].map((i) =>
        arrow(`e${i}`, 88 + i * 86, 70, 102 + i * 86, 70, "g"),
      ),
    ],
    [
      ...["источник", "map", "batched", "запись"].map((t, i) =>
        Box(`b${i}`, 52 + i * 86, 70, 70, 28, t, "g", { size: 10 }),
      ),
      ...[0, 1, 2].map((i) =>
        arrow(`e${i}`, 102 + i * 86, 98, 88 + i * 86, 98, "y", { bend: 0 }),
      ),
      Tx("n", 180, 126, "запрос идёт справа налево", { size: 10, c: "y" }),
    ],
    [
      Box("a", 56, 70, 76, 28, "стадия 1", "g", { size: 10 }),
      Box("q", 180, 70, 76, 28, "Queue", "y", { size: 11.5 }),
      Box("b", 304, 70, 76, 28, "стадия 2", "g", { size: 10 }),
      arrow("e1", 96, 70, 140, 70, "y"),
      arrow("e2", 220, 70, 264, 70, "y"),
    ],
  ],
});

// 11. Отмена и таймауты
export const V11 = scene({
  labels: ["timeout вокруг цикла", "Отмена проходит", "Не подавлять"],
  caption: [
    "async with asyncio.timeout(5): async for … — по истечении времени в точку ожидания вбрасывается отмена",
    "Цикл прерывается, блоки finally выполняются, ресурсы закрываются",
    "CancelledError подавлять нельзя: перехватывайте конкретные ошибки и после обработки поднимайте отмену дальше",
  ],
  frames: [
    [
      py(
        "c",
        24,
        56,
        [
          "async with asyncio.timeout(5):",
          "    async for x in stream():",
          "        process(x)",
        ],
        [0],
        {
          size: 11,
          lh: 26,
          w: 330,
        },
      ),
    ],
    [
      Box("a", 70, 70, 90, 28, "ожидание", "b", { size: 11 }),
      Box("b", 180, 70, 80, 28, "отмена", "r", { size: 11 }),
      Box("c", 290, 70, 90, 28, "finally", "g", { size: 11 }),
      arrow("e1", 116, 70, 138, 70, "r"),
      arrow("e2", 222, 70, 244, 70, "g"),
    ],
    [
      py(
        "c",
        24,
        56,
        [
          "try:",
          "    await work()",
          "except Exception:   # не BaseException!",
          "    log()",
          "    raise",
        ],
        [2, 4],
        {
          size: 10.5,
          lh: 22,
          w: 330,
        },
      ),
    ],
  ],
});

// 12. Тестирование
export const V12 = scene({
  labels: ["IsolatedAsyncioTestCase", "Поддельные источники", "Уборка"],
  caption: [
    "Класс IsolatedAsyncioTestCase запускает async-тесты на настоящем цикле событий",
    "Источники заменяют генераторами с sleep(0): этого хватает, чтобы передать управление; результат собирают включением",
    "Для проверки уборки положите запись в finally и убедитесь, что она появилась сразу после выхода — тесты быстрые и стабильные",
  ],
  frames: [
    [
      py(
        "c",
        24,
        50,
        [
          "class T(IsolatedAsyncioTestCase):",
          "    async def test_stream(self):",
          "        got = [x async for x in fake()]",
          "        self.assertEqual(got, [1, 2, 3])",
        ],
        [1, 2, 3],
        {
          size: 10,
          lh: 22,
          w: 340,
        },
      ),
    ],
    [
      py(
        "c",
        24,
        56,
        [
          "async def fake():",
          "    for i in (1, 2, 3):",
          "        await asyncio.sleep(0)",
          "        yield i",
        ],
        [2],
        {
          size: 11,
          lh: 26,
          w: 320,
        },
      ),
    ],
    [
      py(
        "c",
        24,
        56,
        [
          "async def src():",
          "    try:",
          "        yield 1",
          "    finally:",
          "        log.append('закрыт')",
        ],
        [3, 4],
        {
          size: 11,
          lh: 24,
          w: 320,
        },
      ),
    ],
  ],
});

// 13. Ошибки и итоги
export const V13 = scene({
  labels: ["Типичные ошибки", "Протоколы", "Рекомендации"],
  caption: [
    "for по асинхронному итератору — ошибка; return со значением в асинхронном генераторе; break без aclose; блокирующий вызов внутри потока; широкий except, глотающий отмену",
    "__aiter__/__anext__ и StopAsyncIteration; async def + yield; __aenter__/__aexit__ или @asynccontextmanager",
    "Закрывайте генераторы через aclosing, стройте конвейеры, не забывайте про отмену",
  ],
  frames: [
    [
      ...[
        "for вместо async for",
        "return значение",
        "break без aclose",
        "блокировка в потоке",
        "except: глотает отмену",
      ].map((t, i) =>
        Box(
          `e${i}`,
          94 + (i % 2) * 172,
          36 + Math.floor(i / 2) * 36,
          160,
          26,
          t,
          "r",
          { size: 9.5 },
        ),
      ),
    ],
    [
      Box("a", 70, 56, 100, 26, "__anext__", "g", { size: 10.5 }),
      Box("b", 180, 56, 100, 26, "async def + yield", "g", { size: 8.5 }),
      Box("c", 290, 56, 100, 26, "__aenter__", "g", { size: 10.5 }),
      Tx("n", 180, 108, "StopAsyncIteration · @asynccontextmanager", {
        size: 9.5,
      }),
    ],
    [
      Box("a", 70, 70, 100, 28, "aclosing", "g", { size: 11 }),
      Box("b", 180, 70, 100, 28, "конвейеры", "g", { size: 11 }),
      Box("c", 290, 70, 100, 28, "отмена", "g", { size: 11 }),
    ],
  ],
});
