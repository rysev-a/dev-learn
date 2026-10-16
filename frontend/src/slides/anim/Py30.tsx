import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow } from "./cl.tsx";
import { py } from "./cl.tsx";

/* «Python как первый язык», глава 30: интроспекция и модуль inspect. */

// 1. Программа изучает себя
export const V01 = scene({
  labels: ["Вопросы к объекту", "Инструменты", "Где применяют"],
  caption: [
    "Во время работы программа может спросить: что ты такое, что у тебя есть, как тебя вызывать?",
    "type, dir, getattr, inspect.signature, getsource — набор инструментов интроспекции",
    "Отладчики, тесты, документация, сериализация, внедрение зависимостей — всё стоит на рефлексии",
  ],
  frames: [
    [
      Box("o", 90, 70, 100, 34, "объект", "g", { size: 12 }),
      Box("a", 270, 38, 120, 22, "что ты такое?", "b", { size: 10 }),
      Box("b", 270, 70, 120, 22, "что у тебя есть?", "b", { size: 10 }),
      Box("c", 270, 102, 120, 22, "как тебя вызвать?", "b", { size: 10 }),
      arrow("e1", 146, 62, 208, 40, "b"),
      arrow("e2", 146, 70, 208, 70, "b"),
      arrow("e3", 146, 78, 208, 100, "b"),
    ],
    [
      ...[
        "type()",
        "dir()",
        "getattr()",
        "signature()",
        "getsource()",
        "currentframe()",
      ].map((t, i) =>
        Box(
          `t${i}`,
          62 + (i % 3) * 118,
          54 + Math.floor(i / 3) * 40,
          104,
          26,
          t,
          "g",
          { size: 10.5 },
        ),
      ),
    ],
    [
      ...[
        "отладчики",
        "тесты",
        "документация",
        "сериализация",
        "внедрение зависимостей",
      ].map((t, i) =>
        Box(
          `t${i}`,
          62 + (i % 3) * 118,
          50 + Math.floor(i / 3) * 40,
          108,
          26,
          t,
          "b",
          { size: i === 4 ? 8 : 10 },
        ),
      ),
    ],
  ],
});

// 2. Типы
export const V02 = scene({
  labels: ["Тип значения", "__mro__", "__subclasses__"],
  caption: [
    "type(x) — класс значения; isinstance учитывает наследование, issubclass сравнивает классы",
    "__bases__ — непосредственные родители, __mro__ — полный порядок поиска имён",
    "__subclasses__() — известные потомки: базовый класс сам находит плагины без реестра",
  ],
  frames: [
    [
      py(
        "c",
        40,
        50,
        [
          "type(3)              # int",
          "isinstance(True, int)    # True",
          "issubclass(bool, int)   # True",
        ],
        undefined,
        {
          size: 11,
          lh: 26,
          w: 290,
        },
      ),
    ],
    [
      Box("a", 70, 70, 80, 28, "bool", "g", { size: 11 }),
      Box("b", 180, 70, 80, 28, "int", "b", { size: 11 }),
      Box("c", 290, 70, 80, 28, "object", "m", { size: 11 }),
      arrow("e1", 112, 70, 138, 70, "b"),
      arrow("e2", 222, 70, 248, 70, "b"),
      Tx("n", 180, 118, "bool.__mro__", { size: 10 }),
    ],
    [
      Box("a", 180, 36, 100, 26, "Plugin", "g", { size: 11 }),
      Box("b", 100, 100, 90, 26, "JsonPlugin", "b", { size: 9.5 }),
      Box("c", 260, 100, 90, 26, "CsvPlugin", "b", { size: 9.5 }),
      arrow("e1", 150, 50, 112, 88, "b"),
      arrow("e2", 210, 50, 248, 88, "b"),
      Tx("n", 180, 146, "Plugin.__subclasses__()", { size: 10 }),
    ],
  ],
});

// 3. dir и vars
export const V03 = scene({
  labels: ["dir", "vars", "Разница"],
  caption: [
    "dir(obj) — отсортированный список всех доступных имён, включая унаследованные и специальные",
    "vars(obj) — словарь собственных атрибутов экземпляра (obj.__dict__); у объектов со слотами его нет",
    "dir отвечает «что доступно», vars — «что хранится именно здесь»",
  ],
  frames: [
    [
      py(
        "c",
        30,
        50,
        [
          "class P:",
          "    def __init__(self): self.x = 1",
          "    def move(self): ...",
          "dir(P())   # ['__class__', ..., 'move', 'x']",
        ],
        [3],
        {
          size: 10,
          lh: 22,
          w: 330,
        },
      ),
    ],
    [
      py(
        "c",
        30,
        50,
        ["p = P()", "vars(p)    # {'x': 1}", "p.__dict__ is vars(p)   # True"],
        [1],
        {
          size: 11,
          lh: 26,
          w: 300,
        },
      ),
    ],
    [
      Box("a", 90, 70, 120, 34, "dir(obj)\nвсё доступное", "b", { size: 9.5 }),
      Box("b", 270, 70, 120, 34, "vars(obj)\nсобственное", "g", { size: 9.5 }),
    ],
  ],
});

// 4. Доступ по имени
export const V04 = scene({
  labels: ["getattr", "Диспетчер команд", "Осторожно"],
  caption: [
    "getattr(obj, name, default), setattr, hasattr, delattr — доступ к атрибуту по имени-строке",
    "Команда пользователя превращается в имя метода: getattr(self, 'cmd_' + name)",
    "Имя из внешнего мира нельзя подставлять без проверки: префикс или белый список обязательны",
  ],
  frames: [
    [
      py(
        "c",
        30,
        50,
        [
          "getattr(p, 'x')",
          "getattr(p, 'z', None)   # запасное",
          "setattr(p, 'x', 5)",
          "hasattr(p, 'move')",
        ],
        undefined,
        {
          size: 11.5,
          lh: 24,
          w: 300,
        },
      ),
    ],
    [
      py(
        "c",
        24,
        44,
        [
          "def run(self, name, *args):",
          "    handler = getattr(self, 'cmd_' + name, None)",
          "    if handler is None:",
          "        raise ValueError(name)",
          "    return handler(*args)",
        ],
        [1],
        {
          size: 10,
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
          "getattr(obj, user_input)   # опасно",
          "getattr(obj, 'cmd_' + user_input)",
        ],
        undefined,
        {
          size: 11,
          lh: 28,
          w: 310,
          bad: [0],
        },
      ),
      Tx("n", 180, 130, "сначала проверьте имя", { size: 10, c: "y" }),
    ],
  ],
});

// 5. Виды объектов
export const V05 = scene({
  labels: ["Предикаты", "Не по имени", "Зачем"],
  caption: [
    "inspect.isclass, isfunction, ismethod, iscoroutinefunction, isgeneratorfunction отвечают, что перед вами",
    "callable() только говорит, можно ли вызвать, а предикаты различают виды",
    "Декоратор для async, сериализатор классов, запуск тестов только для функций — везде нужна различимость",
  ],
  frames: [
    [
      ...[
        "isclass",
        "isfunction",
        "ismethod",
        "iscoroutinefunction",
        "isgeneratorfunction",
      ].map((t, i) =>
        Box(
          `b${i}`,
          56 + (i % 3) * 125,
          50 + Math.floor(i / 3) * 40,
          i === 3 || i === 4 ? 118 : 104,
          26,
          t,
          "g",
          { size: 8.5 },
        ),
      ),
    ],
    [
      py(
        "c",
        40,
        50,
        [
          "callable(len)            # True",
          "callable(Point)          # True",
          "inspect.isclass(Point)   # True",
          "inspect.isclass(len)     # False",
        ],
        [2, 3],
        {
          size: 10.5,
          lh: 24,
          w: 300,
        },
      ),
    ],
    [
      Box("a", 90, 60, 130, 28, "async-декоратор", "b", { size: 10 }),
      Box("b", 90, 100, 130, 28, "запуск тестов", "b", { size: 10 }),
      Box("c", 270, 60, 120, 28, "iscoroutinefunction", "g", { size: 8.5 }),
      Box("d", 270, 100, 120, 28, "isfunction", "g", { size: 10 }),
      arrow("e1", 156, 60, 208, 60, "g"),
      arrow("e2", 156, 100, 208, 100, "g"),
    ],
  ],
});

// 6. signature
export const V06 = scene({
  labels: ["Подпись", "Виды параметров", "bind"],
  caption: [
    "inspect.signature(func) — подпись: параметры, значения по умолчанию, аннотации",
    "Виды параметров: POSITIONAL_ONLY, POSITIONAL_OR_KEYWORD, VAR_POSITIONAL, KEYWORD_ONLY, VAR_KEYWORD",
    "sig.bind(*args, **kw) привязывает вызов к подписи или поднимает TypeError — основа проверок и внедрения зависимостей",
  ],
  frames: [
    [
      py(
        "c",
        24,
        50,
        [
          "def f(a, /, b, c=1, *args, d, **kw): ...",
          "sig = inspect.signature(f)",
          "# (a, /, b, c=1, *args, d, **kw)",
        ],
        [1],
        {
          size: 10,
          lh: 24,
          w: 340,
        },
      ),
    ],
    [
      ...[
        ["a", "POSITIONAL_ONLY", "b"],
        ["b, c", "POS_OR_KW", "g"],
        ["*args", "VAR_POSITIONAL", "y"],
        ["d", "KEYWORD_ONLY", "v"],
        ["**kw", "VAR_KEYWORD", "r"],
      ]
        .map(([n, k, c], i) => [
          Box(`n${i}`, 64, 30 + i * 28, 70, 22, n!, c, { size: 10 }),
          Box(`k${i}`, 210, 30 + i * 28, 140, 22, k!, c, { size: 9 }),
        ])
        .flat(),
    ],
    [
      py(
        "c",
        24,
        50,
        [
          "bound = sig.bind(1, 2, d=4)",
          "bound.apply_defaults()",
          "bound.arguments",
          "# {'a': 1, 'b': 2, 'c': 1, 'args': (), 'd': 4, 'kw': {}}",
        ],
        [2],
        {
          size: 9.5,
          lh: 24,
          w: 340,
        },
      ),
    ],
  ],
});

// 7. Атрибуты функций
export const V07 = scene({
  labels: ["Имя и справка", "__code__", "__closure__"],
  caption: [
    "Функция — объект: __name__, __qualname__, __doc__, __module__, __defaults__, __annotations__",
    "В __code__ — скомпилированное тело: co_argcount, co_varnames, co_consts, co_freevars",
    "В __closure__ — ячейки захваченных переменных: cell_contents показывает, что унесла вложенная функция",
  ],
  frames: [
    [
      py(
        "c",
        30,
        50,
        [
          "f.__name__       # 'f'",
          "f.__qualname__   # 'outer.<locals>.f'",
          "f.__doc__",
          "f.__defaults__   # (1,)",
        ],
        undefined,
        {
          size: 11,
          lh: 24,
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
          "code = f.__code__",
          "code.co_argcount    # 2",
          "code.co_varnames    # ('a', 'b', 'tmp')",
          "code.co_freevars    # ('k',)",
        ],
        [1, 2, 3],
        {
          size: 10.5,
          lh: 24,
          w: 310,
        },
      ),
    ],
    [
      py(
        "c",
        30,
        40,
        [
          "def make(k):",
          "    def f(x): return x * k",
          "    return f",
          "f = make(3)",
          "f.__closure__[0].cell_contents   # 3",
        ],
        [4],
        {
          size: 10.5,
          lh: 22,
          w: 320,
        },
      ),
    ],
  ],
});

// 8. Исходный код и кадры
export const V08 = scene({
  labels: ["getsource", "Кадры", "Кто вызвал"],
  caption: [
    "inspect.getsource, getfile, getdoc читают определение; у объектов из консоли и exec исходника нет",
    "inspect.currentframe() — кадр текущей функции; у него есть f_back — кадр вызвавшей",
    "Так журнал узнаёт, откуда его вызвали; ссылки на кадры после работы лучше удалять — иначе циклы и память",
  ],
  frames: [
    [
      py(
        "c",
        30,
        50,
        [
          "inspect.getsource(f)   # текст def",
          "inspect.getfile(f)     # путь к .py",
          "inspect.getdoc(f)      # справка",
        ],
        undefined,
        {
          size: 11,
          lh: 26,
          w: 300,
        },
      ),
    ],
    [
      Box("a", 70, 40, 100, 24, "main()", "m", { size: 10.5 }),
      Box("b", 70, 80, 100, 24, "handler()", "m", { size: 10.5 }),
      Box("c", 70, 120, 100, 24, "log()  ← frame", "g", { size: 10 }),
      arrow("e1", 70, 106, 70, 94, "g"),
      arrow("e2", 70, 66, 70, 54, "g"),
      Tx("n", 250, 80, "f_back →\nf_code.co_name\nf_lineno", { size: 10 }),
    ],
    [
      py(
        "c",
        24,
        44,
        [
          "def log(msg):",
          "    frame = inspect.currentframe().f_back",
          "    name = frame.f_code.co_name",
          "    print(f'[{name}] {msg}')",
          "    del frame",
        ],
        [1, 2, 4],
        {
          size: 10,
          lh: 22,
          w: 330,
        },
      ),
    ],
  ],
});

// 9. Аннотации
export const V09 = scene({
  labels: ["__annotations__", "get_type_hints", "annotationlib"],
  caption: [
    "У функции и класса есть словарь аннотаций, но в нём бывают строки",
    "typing.get_type_hints приводит их к настоящим типам",
    "В Python 3.14 аннотации вычисляются лениво — для чтения добавлен модуль annotationlib; не читайте словарь напрямую",
  ],
  frames: [
    [
      py(
        "c",
        30,
        56,
        [
          "def f(a: int, b: 'Point') -> str: ...",
          "f.__annotations__",
          "# {'a': int, 'b': 'Point', 'return': str}",
        ],
        [1, 2],
        {
          size: 10.5,
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
          "typing.get_type_hints(f)",
          "# {'a': int, 'b': Point, 'return': str}",
          "# строки превращены в типы",
        ],
        [0],
        {
          size: 10.5,
          lh: 26,
          w: 320,
        },
      ),
    ],
    [
      Box("a", 90, 60, 120, 28, "get_type_hints", "g", { size: 10.5 }),
      Box("b", 270, 60, 120, 28, "annotationlib", "y", { size: 10.5 }),
      Tx("n", 180, 112, "стандартные функции, а не словарь", { size: 10 }),
    ],
  ],
});

// 10. Модули
export const V10 = scene({
  labels: ["Импорт по имени", "Загруженные", "Плагины"],
  caption: [
    "importlib.import_module('pkg.mod') подключает модуль по строке — имя может прийти из настроек",
    "sys.modules — уже загруженные; у модуля есть __name__ и __file__",
    "Плагины: pkgutil перечисляет подмодули, importlib.metadata читает точки входа — без явного списка",
  ],
  frames: [
    [
      py(
        "c",
        30,
        56,
        [
          "mod = importlib.import_module('json')",
          "func = getattr(mod, 'dumps')",
          "func({'a': 1})",
        ],
        [0, 1],
        {
          size: 11,
          lh: 26,
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
          "'json' in sys.modules",
          "json.__name__    # 'json'",
          "json.__file__    # путь к файлу",
        ],
        undefined,
        {
          size: 11,
          lh: 26,
          w: 300,
        },
      ),
    ],
    [
      Box("a", 70, 70, 100, 30, "пакет\nplugins/", "b", { size: 9.5 }),
      Box("b", 190, 70, 100, 30, "iter_modules", "g", { size: 10 }),
      Box("c", 306, 70, 90, 30, "import_module", "y", { size: 9 }),
      arrow("e1", 120, 70, 140, 70, "g"),
      arrow("e2", 240, 70, 262, 70, "y"),
    ],
  ],
});

// 11. Применения
export const V11 = scene({
  labels: ["Представление", "Конфигурации", "Фреймворки"],
  caption: [
    "Универсальный __repr__ и сериализация класса в словарь собираются из vars и полей",
    "Тесты находят по префиксу test_, а командная строка строится по подписи функции",
    "Внедрение зависимостей: фреймворк смотрит на параметры и аннотации вашей функции и сам решает, что передать",
  ],
  frames: [
    [
      py(
        "c",
        30,
        56,
        [
          "def to_dict(obj):",
          "    return dict(vars(obj))",
          "to_dict(p)   # {'x': 1, 'y': 2}",
        ],
        [1],
        {
          size: 11,
          lh: 26,
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
          "for name in dir(module):",
          "    if name.startswith('test_'):",
          "        getattr(module, name)()",
        ],
        [1, 2],
        {
          size: 11,
          lh: 26,
          w: 310,
        },
      ),
    ],
    [
      py(
        "c",
        30,
        50,
        [
          "def handler(db: Database, user: User): ...",
          "# фреймворк: signature(handler)",
          "# → найти Database и User, передать",
        ],
        [1, 2],
        {
          size: 10.5,
          lh: 26,
          w: 320,
        },
      ),
    ],
  ],
});

// 12. Подводные камни
export const V12 = scene({
  labels: ["Искажённые имена", "Встроенные на C", "Явное лучше"],
  caption: [
    "Имя __secret в классе искажается в _Class__secret — читать надо под искажённым именем",
    "У некоторых встроенных функций на C подпись узнать нельзя: signature поднимет ValueError",
    "Рефлексия замедляет и усложняет чтение — где хватает прямого вызова, берите его",
  ],
  frames: [
    [
      py(
        "c",
        30,
        56,
        ["class A:", "    __secret = 1", "vars(A)   # '_A__secret'"],
        [2],
        {
          size: 11,
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
          "inspect.signature(len)",
          "inspect.signature(print)",
          "# иногда ValueError: no signature found",
        ],
        undefined,
        {
          size: 10.5,
          lh: 26,
          w: 320,
          bad: [2],
        },
      ),
    ],
    [
      Box("a", 90, 60, 130, 30, "p.move()", "g", { size: 11 }),
      Box("b", 270, 60, 130, 30, "getattr(p, 'move')()", "y", { size: 9 }),
      Tx("n", 180, 112, "прямой вызов проще отлаживать", { size: 10 }),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Типы", "Атрибуты", "inspect", "Модули"],
  caption: [
    "type, isinstance, __mro__, __subclasses__ отвечают о типах",
    "dir и vars показывают атрибуты, getattr и setattr работают с ними по имени",
    "inspect различает виды объектов, читает signature, исходный код и стек вызовов",
    "import_module подключает модули по строке — основа плагинов и фреймворков",
  ],
  frames: [
    [
      Box("a", 90, 70, 100, 30, "type()", "g", { size: 11 }),
      Box("b", 210, 70, 100, 30, "__mro__", "g", { size: 11 }),
      Box("c", 320, 70, 70, 30, "subclasses", "g", { size: 8.5 }),
    ],
    [
      Box("a", 90, 70, 100, 30, "dir / vars", "b", { size: 11 }),
      Box("b", 260, 70, 130, 30, "getattr / setattr", "b", { size: 10.5 }),
    ],
    [
      Box("a", 70, 70, 100, 30, "signature", "y", { size: 11 }),
      Box("b", 190, 70, 100, 30, "getsource", "y", { size: 11 }),
      Box("c", 310, 70, 100, 30, "currentframe", "y", { size: 10 }),
    ],
    [
      Box("a", 90, 70, 130, 30, "import_module", "g", { size: 10.5 }),
      Box("b", 270, 70, 110, 30, "плагины", "g", { size: 11 }),
      arrow("e", 146, 70, 214, 70, "g"),
    ],
  ],
});
