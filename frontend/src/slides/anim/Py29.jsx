import { scene } from "./alg.jsx";
import { Tx } from "./hw.jsx";
import { Box, arrow } from "./cl.jsx";
import { py } from "./cl.jsx";

/* «Python как первый язык», глава 29: декораторы глубже. */

// 1. Декораторы везде
export const V01 = scene({
  labels: ["Функции", "Методы и классы", "Метапрограммирование"],
  caption: [
    "Простой декоратор принимает функцию и возвращает обёртку — это вы уже умеете",
    "На практике их ставят друг на друга, настраивают параметрами, применяют к методам, к классам, к async-функциям",
    "Декораторы — самая мягкая форма метапрограммирования: кода, который работает с кодом",
  ],
  frames: [
    [
      py("c", 70, 56, ["@timed", "def compute(x):", "    return x * x"], [0], {
        size: 12,
        lh: 26,
        w: 220,
      }),
    ],
    [
      ...["функции", "методы", "классы", "async-функции"].map((t, i) =>
        Box(
          `b${i}`,
          62 + (i % 2) * 130,
          50 + Math.floor(i / 2) * 40,
          112,
          26,
          t,
          "b",
          { size: 10.5 },
        ),
      ),
      Box("d", 308, 70, 80, 30, "@deco", "y", { size: 12 }),
      arrow("e1", 268, 70, 256, 70, "y"),
    ],
    [
      Box("a", 90, 70, 110, 30, "декораторы", "g", { size: 11.5 }),
      Box("b", 270, 50, 110, 26, "метаклассы", "m", { size: 10.5 }),
      Box("c", 270, 92, 110, 26, "ast, dis", "m", { size: 10.5 }),
      arrow("e1", 146, 66, 214, 52, "g"),
      arrow("e2", 146, 74, 214, 90, "g"),
    ],
  ],
});

// 2. Порядок применения
export const V02 = scene({
  labels: ["Два декоратора", "Применяется снизу вверх", "Читается сверху вниз"],
  caption: [
    "@bold над @italic над функцией: два слоя разметки",
    "Сначала italic оборачивает функцию, затем bold — результат: bold(italic(f))",
    "При вызове сначала срабатывает верхний слой; снаружи тег bold: <b><i>текст</i></b>",
  ],
  frames: [
    [
      py(
        "c",
        70,
        50,
        ["@bold", "@italic", "def text():", "    return 'привет'"],
        undefined,
        {
          size: 12,
          lh: 24,
          w: 220,
        },
      ),
    ],
    [
      Box("b", 180, 76, 170, 74, "bold", "y", { size: 9, dash: true, o: 0.5 }),
      Box("i", 180, 76, 110, 44, "italic", "g", {
        size: 9,
        dash: true,
        o: 0.6,
      }),
      Box("f", 180, 76, 60, 24, "text", "b", { size: 11 }),
    ],
    [
      Box("o", 180, 56, 200, 28, "<b><i>привет</i></b>", "g", { size: 12 }),
      Tx("n", 180, 112, "применяется снизу вверх, читается сверху вниз", {
        size: 10,
      }),
    ],
  ],
});

// 3. Со скобками и без
export const V03 = scene({
  labels: ["Две записи", "func=None", "Развилка"],
  caption: [
    "Хочется писать и @repeat, и @repeat(times=3) — один декоратор для обеих записей",
    "Первый параметр — функция со значением по умолчанию None, настройки — только по имени",
    "Передали функцию — оборачиваем сразу; нет — возвращаем настоящий декоратор, который дождётся функции",
  ],
  frames: [
    [
      py(
        "c",
        70,
        50,
        [
          "@repeat",
          "def hello(): ...",
          "",
          "@repeat(times=3)",
          "def hello(): ...",
        ],
        undefined,
        {
          size: 11.5,
          lh: 20,
          w: 220,
        },
      ),
    ],
    [
      py(
        "c",
        24,
        56,
        [
          "def repeat(func=None, *, times=2):",
          "    ...",
          "# настройки — только по имени",
        ],
        [0],
        {
          size: 10.5,
          lh: 26,
          w: 310,
        },
      ),
    ],
    [
      py(
        "c",
        24,
        40,
        [
          "def repeat(func=None, *, times=2):",
          "    def decorate(f):",
          "        ...wrapper...",
          "        return wrapper",
          "    if func is not None:",
          "        return decorate(func)",
          "    return decorate",
        ],
        [4, 5, 6],
        {
          size: 10,
          lh: 17,
          w: 320,
        },
      ),
    ],
  ],
});

// 4. Методы
export const V04 = scene({
  labels: ["Обычный метод", "Верно", "Неверно"],
  caption: [
    "Метод в момент определения — обычная функция, self проходит через обёртку как первый аргумент",
    "@classmethod, @staticmethod и @property создают дескрипторы и ставятся самыми верхними",
    "Наоборот — ваша обёртка получит дескриптор вместо функции и сломается",
  ],
  frames: [
    [
      py(
        "c",
        24,
        50,
        [
          "class Api:",
          "    @logged",
          "    def get(self, url):",
          "        ...",
          "# wrapper(self, url)",
        ],
        [1],
        {
          size: 11,
          lh: 22,
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
          "class Api:",
          "    @classmethod",
          "    @logged",
          "    def make(cls): ...",
        ],
        [1, 2],
        {
          size: 11.5,
          lh: 24,
          w: 280,
        },
      ),
      Tx("n", 180, 146, "дескриптор — сверху", { size: 10, c: "g" }),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "class Api:",
          "    @logged",
          "    @classmethod",
          "    def make(cls): ...",
        ],
        undefined,
        {
          size: 11.5,
          lh: 24,
          w: 280,
          bad: [1, 2],
        },
      ),
      Tx("n", 180, 146, "wrapper получит classmethod-объект", {
        size: 10,
        c: "r",
      }),
    ],
  ],
});

// 5. Декораторы классов
export const V05 = scene({
  labels: ["Класс на входе", "Регистрация", "dataclass"],
  caption: [
    "Декоратор класса получает готовый класс и возвращает его — изменённым или другим",
    "Частые задачи: добавить в реестр, проверить атрибуты, достроить методы, подменить одиночкой",
    "@dataclass — декоратор, который по аннотациям достраивает __init__, __repr__, __eq__",
  ],
  frames: [
    [
      Box("a", 70, 70, 80, 30, "class\nPlugin", "b", { size: 10 }),
      Box("d", 180, 70, 90, 30, "@decorator", "y", { size: 10.5 }),
      Box("c", 300, 70, 80, 30, "class\nPlugin'", "g", { size: 10 }),
      arrow("e1", 112, 70, 134, 70, "y"),
      arrow("e2", 226, 70, 258, 70, "y"),
    ],
    [
      py(
        "c",
        24,
        44,
        [
          "PLUGINS = {}",
          "",
          "def plugin(cls):",
          "    PLUGINS[cls.__name__] = cls",
          "    return cls",
        ],
        [3, 4],
        {
          size: 11,
          lh: 22,
          w: 300,
        },
      ),
    ],
    [
      py(
        "c",
        30,
        46,
        ["@dataclass", "class Point:", "    x: int", "    y: int"],
        [0],
        {
          size: 11.5,
          lh: 22,
          w: 220,
        },
      ),
      Box("m", 295, 76, 100, 70, "__init__\n__repr__\n__eq__", "g", {
        size: 9.5,
      }),
    ],
  ],
});

// 6. wraps
export const V06 = scene({
  labels: ["Без wraps", "С wraps", "__wrapped__"],
  caption: [
    "Без @wraps у обёрнутой функции чужое имя и пустая справка: compute.__name__ == 'wrapper'",
    "functools.wraps копирует имя, документацию и модуль",
    "А ещё кладёт ссылку __wrapped__ на оригинал — по ней inspect.signature показывает настоящие параметры",
  ],
  frames: [
    [
      py(
        "c",
        40,
        50,
        [
          "compute.__name__   # 'wrapper'",
          "compute.__doc__    # None",
          "help(compute)       # (*args, **kwargs)",
        ],
        undefined,
        {
          size: 11,
          lh: 24,
          w: 290,
          bad: [0, 1, 2],
        },
      ),
    ],
    [
      py(
        "c",
        40,
        50,
        [
          "@functools.wraps(func)",
          "def wrapper(*args, **kwargs):",
          "    ...",
          "compute.__name__   # 'compute'",
        ],
        [0, 3],
        {
          size: 11,
          lh: 24,
          w: 290,
        },
      ),
    ],
    [
      Box("w", 90, 70, 100, 30, "wrapper", "b", { size: 11 }),
      Box("o", 270, 70, 100, 30, "оригинал", "g", { size: 11 }),
      arrow("e", 142, 70, 218, 70, "g"),
      Tx("n", 180, 56, "__wrapped__", { size: 10 }),
      Tx("m", 180, 118, "inspect.signature идёт по ссылке", {
        size: 10,
        c: "g",
      }),
    ],
  ],
});

// 7. Состояние
export const V07 = scene({
  labels: ["Атрибут обёртки", "Класс-декоратор", "__get__ для методов"],
  caption: [
    "Простое состояние хранят в атрибуте самой обёртки: wrapper.calls += 1",
    "Если состояния много — декоратор-класс с __call__: объект хранит данные и вызывается как функция",
    "Экземпляр класса сам не становится методом: нужен __get__ из протокола дескрипторов, как у функций",
  ],
  frames: [
    [
      py(
        "c",
        24,
        44,
        [
          "def counted(func):",
          "    @wraps(func)",
          "    def wrapper(*a, **kw):",
          "        wrapper.calls += 1",
          "        return func(*a, **kw)",
          "    wrapper.calls = 0",
          "    return wrapper",
        ],
        [3, 5],
        {
          size: 10,
          lh: 17,
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
          "class CallCounter:",
          "    def __init__(self, func):",
          "        self.func = func",
          "        self.calls = 0",
          "    def __call__(self, *a, **kw):",
          "        self.calls += 1",
          "        return self.func(*a, **kw)",
        ],
        [3, 4, 5],
        {
          size: 10,
          lh: 17,
          w: 310,
        },
      ),
    ],
    [
      py(
        "c",
        24,
        56,
        [
          "def __get__(self, obj, objtype=None):",
          "    if obj is None:",
          "        return self",
          "    return types.MethodType(self, obj)",
        ],
        [3],
        {
          size: 10.5,
          lh: 22,
          w: 310,
        },
      ),
    ],
  ],
});

// 8. Асинхронные функции
export const V08 = scene({
  labels: ["Ловушка", "Асинхронная обёртка", "Универсальный"],
  caption: [
    "Обычная обёртка получит от async-функции корутину, не дождётся её — время и повторы посчитаются неверно",
    "Нужна обёртка async def с await: результат дожидаются",
    "Универсальный декоратор выбирает обёртку по inspect.iscoroutinefunction(func)",
  ],
  frames: [
    [
      py(
        "c",
        24,
        50,
        [
          "def timed(func):",
          "    def wrapper(*a):",
          "        start = time()",
          "        result = func(*a)   # корутина!",
          "        print(time() - start)",
        ],
        [3],
        {
          size: 10.5,
          lh: 22,
          w: 310,
          bad: [3],
        },
      ),
    ],
    [
      py(
        "c",
        24,
        56,
        [
          "async def wrapper(*a):",
          "    start = time()",
          "    result = await func(*a)",
          "    print(time() - start)",
          "    return result",
        ],
        [2],
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
        24,
        56,
        [
          "if inspect.iscoroutinefunction(func):",
          "    return async_wrapper",
          "return sync_wrapper",
        ],
        [0],
        {
          size: 11,
          lh: 26,
          w: 310,
        },
      ),
    ],
  ],
});

// 9. Регистрирующие декораторы
export const V09 = scene({
  labels: ["Маршруты", "Таблица", "Момент срабатывания"],
  caption: [
    "Декоратор принимает адрес и запоминает функцию — обёртки нет, функция возвращается как есть",
    "Так работают маршруты веб-фреймворков, обработчики событий, команды консоли, плагины и тесты",
    "Регистрация происходит при определении, то есть при импорте модуля; не импортировали — не зарегистрировалось",
  ],
  frames: [
    [
      py(
        "c",
        24,
        50,
        [
          "@route('/home')",
          "def home(): ...",
          "",
          "@route('/about')",
          "def about(): ...",
        ],
        [0, 3],
        {
          size: 11,
          lh: 22,
          w: 300,
        },
      ),
    ],
    [
      Box("t", 90, 70, 110, 70, "ROUTES", "y", { size: 11 }),
      Box("a", 270, 50, 130, 24, "'/home' → home", "g", { size: 9.5 }),
      Box("b", 270, 90, 130, 24, "'/about' → about", "g", { size: 9.5 }),
      arrow("e1", 146, 54, 204, 50, "g"),
      arrow("e2", 146, 86, 204, 90, "g"),
    ],
    [
      Box("a", 90, 70, 110, 30, "import app", "b", { size: 11 }),
      Box("b", 270, 70, 130, 30, "таблица заполнена", "g", { size: 10 }),
      arrow("e", 146, 70, 202, 70, "g"),
      Tx("n", 180, 118, "при определении, а не при вызове", { size: 10 }),
    ],
  ],
});

// 10. Практические декораторы
export const V10 = scene({
  labels: ["Надёжность", "Контроль", "Скорость"],
  caption: [
    "retry с растущей паузой и timed — несколько строк на десятки функций",
    "Проверка прав, предупреждение об устаревшей функции (warnings.warn), проверка аргументов по аннотациям",
    "@lru_cache(maxsize=…) кэширует вызовы; cache_info() показывает попадания и промахи",
  ],
  frames: [
    [
      Box("a", 100, 56, 120, 30, "@retry(times=3)", "g", { size: 10.5 }),
      Box("b", 260, 56, 120, 30, "@timed", "g", { size: 11 }),
      Tx("n", 180, 112, "повтор при временной ошибке · замер времени", {
        size: 10,
      }),
    ],
    [
      Box("a", 70, 56, 100, 28, "@require_admin", "b", { size: 9.5 }),
      Box("b", 180, 56, 100, 28, "@deprecated", "b", { size: 10 }),
      Box("c", 290, 56, 100, 28, "@checked", "b", { size: 10.5 }),
      Tx("n", 180, 112, "права · предупреждение · типы по аннотациям", {
        size: 10,
      }),
    ],
    [
      py(
        "c",
        40,
        50,
        [
          "@lru_cache(maxsize=256)",
          "def fib(n): ...",
          "fib.cache_info()",
          "# hits=…, misses=…",
        ],
        [0],
        {
          size: 11,
          lh: 24,
          w: 280,
        },
      ),
    ],
  ],
});

// 11. Типы декораторов
export const V11 = scene({
  labels: ["Подпись", "ParamSpec", "Зачем"],
  caption: [
    "Для проверки типов обёртка должна принимать те же аргументы, что и оригинал",
    "В typing для этого есть ParamSpec и Callable[P, R]: они описывают чужую подпись",
    "Аннотируйте декораторы библиотеки — тогда редакторы подскажут параметры пользователям",
  ],
  frames: [
    [
      Box("a", 90, 70, 110, 30, "f(x: int) → str", "b", { size: 10 }),
      Box("b", 270, 70, 130, 30, "wrapper(*args, **kw)", "r", { size: 9 }),
      Tx("n", 180, 118, "подсказки потеряны", { size: 10, c: "r" }),
    ],
    [
      py(
        "c",
        24,
        50,
        [
          "P = ParamSpec('P')",
          "R = TypeVar('R')",
          "def deco(f: Callable[P, R]) -> Callable[P, R]:",
          "    ...",
        ],
        [2],
        {
          size: 10,
          lh: 22,
          w: 330,
        },
      ),
    ],
    [
      Box("a", 90, 70, 110, 30, "редактор", "b", { size: 11 }),
      Box("b", 270, 70, 130, 30, "видит параметры f", "g", { size: 10 }),
      arrow("e", 146, 70, 202, 70, "g"),
    ],
  ],
});

// 12. Типичные ошибки
export const V12 = scene({
  labels: ["Не вернули результат", "Не вернули обёртку", "Побочные эффекты"],
  caption: [
    "Обёртка не возвращает результат оригинала — функции стали возвращать None",
    "Декоратор не возвращает wrapper — имя функции теперь указывает на None",
    "Код в теле декоратора выполняется при импорте; а если логика не повторяется, декоратор вообще не нужен",
  ],
  frames: [
    [
      py(
        "c",
        30,
        56,
        ["def wrapper(*a, **kw):", "    func(*a, **kw)   # нет return"],
        undefined,
        {
          size: 11,
          lh: 26,
          w: 300,
          bad: [1],
        },
      ),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "def deco(func):",
          "    def wrapper(*a): ...",
          "    # забыли: return wrapper",
        ],
        undefined,
        {
          size: 11,
          lh: 26,
          w: 300,
          bad: [2],
        },
      ),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "def deco(func):",
          "    print('загрузка!')   # при импорте",
          "    return func",
        ],
        undefined,
        {
          size: 11,
          lh: 26,
          w: 300,
          bad: [1],
        },
      ),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Порядок", "Параметры", "Методы и классы", "Состояние и async"],
  caption: [
    "Снизу вверх применяются, сверху вниз читаются; @classmethod, @staticmethod и @property — самые верхние",
    "func=None и настройки только по имени — одна запись для обоих вариантов",
    "Декоратор класса получает готовый класс; всегда @wraps",
    "Состояние — атрибут обёртки или класс с __get__; для async — async-обёртка",
  ],
  frames: [
    [
      Box("a", 90, 56, 120, 28, "@верхний", "y", { size: 11 }),
      Box("b", 90, 96, 120, 28, "@нижний", "g", { size: 11 }),
      Tx("n", 270, 76, "снизу вверх", { size: 11, c: "g" }),
    ],
    [
      py("c", 40, 66, ["@repeat", "@repeat(times=3)"], undefined, {
        size: 12.5,
        lh: 28,
        w: 260,
      }),
    ],
    [
      Box("a", 90, 70, 120, 30, "@wraps(func)", "g", { size: 11 }),
      Box("b", 260, 70, 120, 30, "декоратор класса", "b", { size: 10 }),
    ],
    [
      Box("a", 90, 70, 120, 30, "__get__", "g", { size: 11 }),
      Box("b", 260, 70, 120, 30, "async def wrapper", "y", { size: 10 }),
    ],
  ],
});
