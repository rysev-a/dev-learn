import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow } from "./cl.tsx";
import { py } from "./cl.tsx";

/* «Python как первый язык», глава 24: генераторы глубже — send, throw, close, yield from. */

// 1. От поставщика к сопрограмме
export const V01 = scene({
  labels: ["Поставщик", "Двусторонний обмен", "Сопрограмма"],
  caption: [
    "Раньше генератор только отдавал значения: next — и получили",
    "Теперь он ещё принимает значения, ошибки и сигнал на закрытие",
    "Приостанавливаемая функция с двусторонним обменом — это корутина; на ней выросли асинхронные программы",
  ],
  frames: [
    [
      Box("g", 90, 70, 100, 30, "генератор", "b", { size: 11 }),
      Box("c", 270, 70, 100, 30, "вызывающий", "m", { size: 11 }),
      arrow("e", 204, 70, 140, 70, "g"),
    ],
    [
      Box("g", 90, 70, 100, 30, "генератор", "b", { size: 11 }),
      Box("c", 270, 70, 100, 30, "вызывающий", "m", { size: 11 }),
      arrow("e1", 204, 58, 140, 58, "g"),
      arrow("e2", 140, 82, 204, 82, "y"),
      Tx("n", 180, 118, "send · throw · close", { size: 10, c: "y" }),
    ],
    [
      Box("a", 90, 70, 110, 30, "корутина", "g", { size: 12 }),
      Box("b", 260, 70, 110, 30, "async / await", "y", { size: 11 }),
      arrow("e", 146, 70, 204, 70, "y"),
    ],
  ],
});

// 2. Жизненный цикл
export const V02 = scene({
  labels: ["Четыре состояния", "Первый запрос", "Ранний send"],
  caption: [
    "Создан → работает → приостановлен на yield → закрыт; состояние показывает inspect.getgeneratorstate",
    "Первый запрос — обычный next: тело выполняется до первого yield",
    "send(5) в только что созданный генератор — TypeError: принимать пока нечему",
  ],
  frames: [
    [
      Box("a", 56, 70, 80, 30, "CREATED", "b", { size: 9.5 }),
      Box("b", 150, 70, 80, 30, "RUNNING", "y", { size: 9.5 }),
      Box("c", 240, 40, 90, 26, "SUSPENDED", "g", { size: 9 }),
      Box("d", 320, 100, 70, 26, "CLOSED", "m", { size: 9 }),
      arrow("e1", 96, 70, 110, 70, "m"),
      arrow("e2", 190, 62, 200, 50, "m"),
      arrow("e3", 280, 52, 308, 90, "m"),
    ],
    [
      py(
        "c",
        24,
        44,
        [
          "def gen():",
          "    print('старт')",
          "    yield 1",
          "g = gen()      # CREATED",
          "next(g)        # старт, SUSPENDED",
        ],
        [1, 2, 4],
        {
          size: 10.5,
          lh: 22,
          w: 310,
        },
      ),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "g = gen()",
          "g.send(5)",
          "# TypeError: can't send non-None",
          "# value to a just-started generator",
        ],
        undefined,
        {
          size: 10.5,
          lh: 22,
          w: 310,
          bad: [1, 2, 3],
        },
      ),
    ],
  ],
});

// 3. send
export const V03 = scene({
  labels: ["yield как выражение", "send(10)", "send(20)", "Среднее"],
  caption: [
    "У yield есть значение: x = yield — то, что прислали через send",
    "send(10): генератор просыпается, x = 10, считает среднее и снова останавливается на yield",
    "send(20): тот же код, сумма и счётчик сохранились в локальных переменных",
    "send возвращает то, что отдал следующий yield, — актуальное среднее",
  ],
  frames: [
    [
      py(
        "c",
        24,
        44,
        [
          "def averager():",
          "    total = count = 0",
          "    avg = None",
          "    while True:",
          "        x = yield avg",
          "        total += x",
          "        count += 1",
          "        avg = total / count",
        ],
        [4],
        {
          size: 10,
          lh: 17,
          w: 320,
        },
      ),
    ],
    [
      py(
        "c",
        24,
        44,
        [
          "def averager():",
          "    total = count = 0",
          "    avg = None",
          "    while True:",
          "        x = yield avg",
          "        total += x",
          "        count += 1",
          "        avg = total / count",
        ],
        [5, 6, 7],
        {
          size: 10,
          lh: 17,
          w: 320,
        },
      ),
      Box("s", 300, 50, 80, 34, "total=10\ncount=1", "g", { size: 9 }),
    ],
    [
      py(
        "c",
        24,
        44,
        [
          "def averager():",
          "    total = count = 0",
          "    avg = None",
          "    while True:",
          "        x = yield avg",
          "        total += x",
          "        count += 1",
          "        avg = total / count",
        ],
        [5, 6, 7],
        {
          size: 10,
          lh: 17,
          w: 320,
        },
      ),
      Box("s", 300, 50, 80, 34, "total=30\ncount=2", "g", { size: 9 }),
    ],
    [
      py(
        "c",
        30,
        50,
        [
          "avg = averager()",
          "next(avg)",
          "avg.send(10)    # 10.0",
          "avg.send(20)    # 15.0",
          "avg.send(30)    # 20.0",
        ],
        [2, 3, 4],
        {
          size: 11,
          lh: 22,
          w: 300,
        },
      ),
    ],
  ],
});

// 4. Заведение корутины
export const V04 = scene({
  labels: ["Забыли next", "Декоратор", "send(None)"],
  caption: [
    "Корутину нужно «завести»: первый next доведёт её до yield; забыли — первая отправка падает",
    "Маленький декоратор создаёт генератор и сразу делает первый запрос",
    "send(None) равносилен next — тоже годится для заведения",
  ],
  frames: [
    [
      py(
        "c",
        40,
        56,
        ["avg = averager()", "avg.send(10)   # TypeError!"],
        undefined,
        {
          size: 11,
          lh: 26,
          w: 280,
          bad: [1],
        },
      ),
    ],
    [
      py(
        "c",
        24,
        40,
        [
          "def primed(func):",
          "    def wrapper(*args):",
          "        gen = func(*args)",
          "        next(gen)",
          "        return gen",
          "    return wrapper",
        ],
        [2, 3],
        {
          size: 10.5,
          lh: 20,
          w: 300,
        },
      ),
    ],
    [
      py(
        "c",
        40,
        56,
        [
          "g = averager()",
          "g.send(None)   # = next(g)",
          "g.send(10)     # 10.0",
        ],
        [1],
        {
          size: 11,
          lh: 24,
          w: 280,
        },
      ),
    ],
  ],
});

// 5. throw
export const V05 = scene({
  labels: ["Вбросить ошибку", "Перехват", "Не перехватили"],
  caption: [
    "gen.throw(ValueError) вбрасывает исключение в точку остановки — будто на месте yield стоит raise",
    "Генератор перехватил его и продолжил: throw возвращает следующее отданное значение",
    "Не перехватил — исключение вылетает наружу вызывающему",
  ],
  frames: [
    [
      Box("c", 70, 70, 100, 30, "вызывающий", "m", { size: 10.5 }),
      Box("g", 270, 70, 110, 30, "yield ← raise", "r", { size: 10.5 }),
      arrow("e", 124, 70, 212, 70, "r"),
      Tx("n", 180, 112, "gen.throw(ValueError)", { size: 10.5, c: "r" }),
    ],
    [
      py(
        "c",
        24,
        40,
        [
          "def counter():",
          "    n = 0",
          "    while True:",
          "        try:",
          "            yield n",
          "            n += 1",
          "        except ValueError:",
          "            n = 0   # сброс",
        ],
        [6, 7],
        {
          size: 10,
          lh: 17,
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
          "def gen():",
          "    yield 1",
          "g = gen(); next(g)",
          "g.throw(KeyError)",
          "# KeyError вылетел наружу",
        ],
        [3, 4],
        {
          size: 11,
          lh: 22,
          w: 300,
          bad: [4],
        },
      ),
    ],
  ],
});

// 6. close
export const V06 = scene({
  labels: ["close()", "finally", "Не отдавайте"],
  caption: [
    "close() вбрасывает в точку остановки особое исключение GeneratorExit — ловить его не нужно",
    "Стек раскручивается, и блоки finally выполняются: здесь закрывают файлы и соединения",
    "Если после close генератор попробует отдать значение — RuntimeError; сборщик мусора вызывает close сам, но не полагайтесь на это",
  ],
  frames: [
    [
      Box("c", 70, 70, 100, 30, "g.close()", "b", { size: 11 }),
      Box("g", 270, 70, 150, 30, "GeneratorExit в yield", "y", { size: 10 }),
      arrow("e", 124, 70, 192, 70, "y"),
    ],
    [
      py(
        "c",
        24,
        44,
        [
          "def reader(path):",
          "    f = open(path)",
          "    try:",
          "        for line in f:",
          "            yield line",
          "    finally:",
          "        f.close()   # выполнится",
        ],
        [5, 6],
        {
          size: 10,
          lh: 18,
          w: 310,
        },
      ),
    ],
    [
      py(
        "c",
        24,
        50,
        [
          "try:",
          "    yield 1",
          "except GeneratorExit:",
          "    yield 2    # RuntimeError",
          "# generator ignored GeneratorExit",
        ],
        undefined,
        {
          size: 11,
          lh: 22,
          w: 310,
          bad: [3, 4],
        },
      ),
    ],
  ],
});

// 7. return в генераторе
export const V07 = scene({
  labels: ["return значение", "StopIteration.value", "for молчит"],
  caption: [
    "Генератор может завершиться return со значением: итог — сумма, число обработанных",
    "Значение лежит в атрибуте value исключения StopIteration",
    "Цикл for его отбрасывает, а next и send позволяют перехватить; главный потребитель — yield from",
  ],
  frames: [
    [
      py(
        "c",
        30,
        50,
        [
          "def summing(items):",
          "    total = 0",
          "    for x in items:",
          "        total += x",
          "        yield x",
          "    return total",
        ],
        [5],
        {
          size: 10.5,
          lh: 20,
          w: 300,
        },
      ),
    ],
    [
      py(
        "c",
        30,
        50,
        [
          "g = summing([1, 2, 3])",
          "next(g); next(g); next(g)",
          "next(g)",
          "# StopIteration: 6",
        ],
        [3],
        {
          size: 11,
          lh: 24,
          w: 300,
        },
      ),
      Box("v", 300, 130, 80, 26, "value = 6", "g", { size: 10 }),
    ],
    [
      py(
        "c",
        30,
        50,
        [
          "for x in summing([1, 2, 3]):",
          "    print(x)     # 1 2 3",
          "# 6 отброшено",
        ],
        undefined,
        {
          size: 11,
          lh: 24,
          w: 300,
        },
      ),
    ],
  ],
});

// 8. yield from
export const V08 = scene({
  labels: ["Делегирование", "Прозрачный канал", "Результат"],
  caption: [
    "yield from inner() передаёт работу вложенному генератору: его значения уходят наружу",
    "send и throw пробрасываются внутрь, а close доходит до вложенного — внешний генератор прозрачен",
    "Значение return вложенного становится значением выражения yield from",
  ],
  frames: [
    [
      Box("o", 60, 70, 80, 30, "вызывающий", "m", { size: 9.5 }),
      Box("m", 180, 70, 80, 30, "outer", "b", { size: 11 }),
      Box("i", 300, 70, 80, 30, "inner", "g", { size: 11 }),
      arrow("e1", 258, 82, 224, 82, "g"),
      arrow("e2", 138, 82, 104, 82, "g"),
    ],
    [
      Box("o", 60, 70, 80, 30, "вызывающий", "m", { size: 9.5 }),
      Box("m", 180, 70, 80, 30, "outer", "b", { size: 11 }),
      Box("i", 300, 70, 80, 30, "inner", "g", { size: 11 }),
      arrow("e1", 104, 62, 138, 62, "y"),
      arrow("e2", 224, 62, 258, 62, "y"),
      Tx("n", 180, 124, "send / throw / close — насквозь", {
        size: 10,
        c: "y",
      }),
    ],
    [
      py(
        "c",
        30,
        50,
        [
          "def outer():",
          "    total = yield from summing([1, 2])",
          "    print('итог', total)   # 3",
        ],
        [1],
        {
          size: 11,
          lh: 24,
          w: 310,
        },
      ),
    ],
  ],
});

// 9. Рекурсивный обход
export const V09 = scene({
  labels: ["Вложенные списки", "Рекурсия", "Строки — листья"],
  caption: [
    "Нужно развернуть [1, [2, [3, 4]], 5] в плоскую последовательность любой глубины",
    "Если элемент — список, делегируем самой себе через yield from; иначе отдаём элемент",
    "Строки считаем листьями: иначе бесконечная рекурсия, ведь строка состоит из строк",
  ],
  frames: [
    [
      Box("a", 180, 30, 160, 24, "[1, [2, [3, 4]], 5]", "b", { size: 10 }),
      Box("b", 120, 74, 60, 22, "[2, [3, 4]]", "b", { size: 8.5 }),
      Box("c", 190, 116, 50, 22, "[3, 4]", "b", { size: 9 }),
      arrow("e1", 160, 42, 130, 62, "m"),
      arrow("e2", 120, 86, 170, 106, "m"),
    ],
    [
      py(
        "c",
        20,
        44,
        [
          "def flatten(items):",
          "    for x in items:",
          "        if isinstance(x, list):",
          "            yield from flatten(x)",
          "        else:",
          "            yield x",
        ],
        [3, 5],
        {
          size: 10.5,
          lh: 20,
          w: 320,
        },
      ),
    ],
    [
      py(
        "c",
        20,
        44,
        [
          "if isinstance(x, (list, tuple)):",
          "    yield from flatten(x)",
          "else:",
          "    yield x   # 'ab' — лист",
        ],
        [0, 3],
        {
          size: 10.5,
          lh: 22,
          w: 320,
        },
      ),
    ],
  ],
});

// 10. Конвейер корутин
export const V10 = scene({
  labels: ["Проталкивание", "Фильтр", "Закрытие"],
  caption: [
    "Источник посылает значения send первой стадии; данные идут не вытягиванием, а проталкиванием",
    "Каждая стадия — генератор с бесконечным циклом: принял, что-то сделал, передал следующей",
    "Закрывать цепочку принято с источника, чтобы finally выполнились по порядку",
  ],
  frames: [
    [
      Box("a", 56, 70, 76, 30, "источник", "b", { size: 10.5 }),
      Box("b", 180, 70, 76, 30, "фильтр", "g", { size: 10.5 }),
      Box("c", 304, 70, 76, 30, "приёмник", "b", { size: 10.5 }),
      arrow("e1", 96, 70, 140, 70, "y"),
      arrow("e2", 220, 70, 262, 70, "y"),
      Tx("n", 180, 116, "send →", { size: 10.5, c: "y" }),
    ],
    [
      py(
        "c",
        24,
        44,
        [
          "def keep(pred, target):",
          "    while True:",
          "        item = yield",
          "        if pred(item):",
          "            target.send(item)",
        ],
        [2, 3, 4],
        {
          size: 10.5,
          lh: 22,
          w: 310,
        },
      ),
    ],
    [
      Box("a", 56, 70, 76, 30, "источник", "r", { size: 10.5 }),
      Box("b", 180, 70, 76, 30, "фильтр", "m", { size: 10.5 }),
      Box("c", 304, 70, 76, 30, "приёмник", "m", { size: 10.5 }),
      Tx("n", 180, 118, "close() — по порядку, слева направо", {
        size: 10,
        c: "y",
      }),
    ],
  ],
});

// 11. Планировщик
export const V11 = scene({
  labels: ["Очередь задач", "Шаг и уступка", "В конец очереди"],
  caption: [
    "Несколько генераторов-задач стоят в очереди; планировщик берёт первую",
    "Запрашивает один шаг: yield означает «готов уступить управление»",
    "Если задача не завершена — в конец очереди; завершилась (StopIteration) — убрана; переключаются только на yield",
  ],
  frames: [
    [
      ...["A", "B", "C"].map((t, i) =>
        Box(`t${i}`, 80 + i * 70, 56, 56, 30, t, "b", { size: 12 }),
      ),
      Box("p", 290, 56, 90, 30, "планировщик", "g", { size: 9.5 }),
      arrow("e", 252, 56, 244, 56, "g"),
    ],
    [
      Box("t0", 80, 56, 56, 30, "A", "g", { size: 12 }),
      Box("t1", 150, 56, 56, 30, "B", "b", { size: 12 }),
      Box("t2", 220, 56, 56, 30, "C", "b", { size: 12 }),
      Tx("n", 180, 112, "next(A) → до ближайшего yield", { size: 10.5 }),
    ],
    [
      Box("t1", 80, 56, 56, 30, "B", "b", { size: 12 }),
      Box("t2", 150, 56, 56, 30, "C", "b", { size: 12 }),
      Box("t0", 220, 56, 56, 30, "A", "g", { size: 12 }),
      Tx("n", 180, 112, "A встала в конец — по кругу", { size: 10.5, c: "g" }),
    ],
  ],
});

// 12. Путь к async/await
export const V12 = scene({
  labels: ["Корутины на генераторах", "async/await", "Тот же принцип"],
  caption: [
    "Раньше асинхронный код писали на генераторах и yield from; старый декоратор asyncio.coroutine удалён в Python 3.11",
    "Появились async def и await: корутины стали отдельным видом объектов",
    "await — приостановка с возвратом управления планировщику, как yield from, только строже и понятнее",
  ],
  frames: [
    [
      py(
        "c",
        30,
        56,
        ["@asyncio.coroutine", "def fetch():", "    data = yield from get()"],
        undefined,
        {
          size: 11,
          lh: 24,
          w: 300,
        },
      ),
    ],
    [
      py("c", 30, 56, ["async def fetch():", "    data = await get()"], [1], {
        size: 11.5,
        lh: 28,
        w: 300,
      }),
    ],
    [
      Box("a", 90, 70, 100, 30, "yield from", "b", { size: 11 }),
      Box("b", 270, 70, 90, 30, "await", "g", { size: 12 }),
      arrow("e", 142, 70, 222, 70, "g"),
      Tx("n", 180, 116, "приостановка + возврат планировщику", { size: 10 }),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: [
    "Состояния",
    "send / throw / close",
    "return и yield from",
    "Применение",
  ],
  caption: [
    "Четыре состояния; первый запрос всегда next",
    "send — значение в yield, throw — исключение, close — GeneratorExit, уборка в finally",
    "return попадает в StopIteration.value, а yield from делегирует работу и возвращает результат",
    "Рекурсивные обходы, конвейеры корутин, планировщики — и в итоге асинхронные программы",
  ],
  frames: [
    [
      Box("a", 70, 70, 84, 28, "created", "b", { size: 10.5 }),
      Box("b", 180, 70, 84, 28, "suspended", "g", { size: 10.5 }),
      Box("c", 290, 70, 84, 28, "closed", "m", { size: 10.5 }),
      arrow("e1", 114, 70, 134, 70, "m"),
      arrow("e2", 226, 70, 246, 70, "m"),
    ],
    [
      Box("a", 70, 70, 84, 28, "send(x)", "g", { size: 10.5 }),
      Box("b", 180, 70, 84, 28, "throw(E)", "r", { size: 10.5 }),
      Box("c", 290, 70, 84, 28, "close()", "y", { size: 10.5 }),
    ],
    [
      Box("a", 100, 70, 130, 28, "return → value", "b", { size: 10.5 }),
      Box("b", 270, 70, 110, 28, "yield from", "g", { size: 10.5 }),
    ],
    [
      Box("a", 70, 56, 100, 26, "обходы", "b", { size: 10.5 }),
      Box("b", 190, 56, 100, 26, "конвейеры", "b", { size: 10.5 }),
      Box("c", 310, 56, 100, 26, "планировщики", "b", { size: 9.5 }),
      Box("d", 190, 108, 120, 28, "async / await", "g", { size: 11 }),
    ],
  ],
});
