import { scene } from "./alg.tsx";
import { Tx } from "./hw.tsx";
import { Box, arrow } from "./cl.tsx";
import { py } from "./cl.tsx";

/* «Python как первый язык», глава 40: абстрактные классы (abc). */

// 1. Контракт
export const V01 = scene({
  labels: ["Утиная типизация", "Вопросы роста", "Контракт"],
  caption: [
    "Умеет крякать — значит, утка: для небольших программ этого достаточно",
    "Какие методы обязан иметь объект? Что, если разработчик забыл один? Узнать до выполнения, а не после релиза?",
    "Абстрактный класс — контракт: обещание, которое должны выполнить все наследники",
  ],
  frames: [
    [
      Box("a", 90, 70, 110, 34, "крякает?", "b", { size: 12 }),
      Box("b", 270, 70, 110, 34, "значит, утка", "g", { size: 12 }),
      arrow("e", 146, 70, 214, 70, "g"),
    ],
    [
      Tx("q1", 180, 40, "какие методы нужны?", { size: 11 }),
      Tx("q2", 180, 76, "что, если забыли один?", { size: 11 }),
      Tx("q3", 180, 112, "узнать до релиза?", { size: 11, c: "y" }),
    ],
    [
      Box("c", 180, 36, 140, 28, "контракт", "y", { size: 12 }),
      Box("a", 90, 110, 100, 26, "Наследник 1", "g", { size: 10 }),
      Box("b", 270, 110, 100, 26, "Наследник 2", "g", { size: 10 }),
      arrow("e1", 150, 50, 106, 96, "y"),
      arrow("e2", 210, 50, 254, 96, "y"),
    ],
  ],
});

// 2. ABC и abstractmethod
export const V02 = scene({
  labels: ["Объявление", "Нельзя создать", "Наследник"],
  caption: [
    "Наследуем от ABC и помечаем обязательные методы @abstractmethod",
    "Создать экземпляр нельзя: TypeError перечислит нереализованные методы",
    "Наследник, реализовавший всё, создаётся без проблем; забытый метод обнаруживается при создании объекта",
  ],
  frames: [
    [
      py(
        "c",
        24,
        44,
        [
          "from abc import ABC, abstractmethod",
          "",
          "class Shape(ABC):",
          "    @abstractmethod",
          "    def area(self): ...",
        ],
        [3, 4],
        {
          size: 10.5,
          lh: 22,
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
          "Shape()",
          "# TypeError: Can't instantiate abstract",
          "# class Shape without an implementation",
          "# for abstract method 'area'",
        ],
        undefined,
        {
          size: 10.5,
          lh: 24,
          w: 320,
          bad: [0, 1, 2, 3],
        },
      ),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "class Rect(Shape):",
          "    def __init__(self, w, h): ...",
          "    def area(self):",
          "        return self.w * self.h",
          "Rect(2, 3).area()   # 6",
        ],
        [2, 3],
        {
          size: 10.5,
          lh: 22,
          w: 320,
        },
      ),
    ],
  ],
});

// 3. Как это устроено
export const V03 = scene({
  labels: ["ABCMeta", "Проверка", "Без ABC"],
  caption: [
    "У ABC метакласс ABCMeta: при создании класса он собирает имена абстрактных методов в __abstractmethods__",
    "Проверка — при создании экземпляра: множество не пусто — создание отклоняется",
    "Забыли унаследоваться от ABC — декоратор молча игнорируется; проверьте абстрактность тестом",
  ],
  frames: [
    [
      Box("a", 90, 70, 110, 30, "ABCMeta", "y", { size: 12 }),
      Box("b", 270, 70, 150, 30, "__abstractmethods__", "g", { size: 10 }),
      arrow("e", 146, 70, 192, 70, "g"),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "Shape.__abstractmethods__",
          "# frozenset({'area'})",
          "Rect.__abstractmethods__",
          "# frozenset()",
        ],
        [0, 1],
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
        56,
        [
          "class Shape:            # нет ABC!",
          "    @abstractmethod",
          "    def area(self): ...",
          "Shape()    # создался: проверки нет",
        ],
        undefined,
        {
          size: 10.5,
          lh: 24,
          w: 320,
          bad: [0, 3],
        },
      ),
    ],
  ],
});

// 4. Тело и свойства
export const V04 = scene({
  labels: ["Тело у абстрактного", "Свойство", "Порядок"],
  caption: [
    "У абстрактного метода может быть тело: наследник вызовет его через super() и дополнит",
    "Абстрактные бывают и свойства, и фабрики: @property или @classmethod сверху, @abstractmethod ниже",
    "Тогда наследники обязаны определить и свойство, и фабрику — весь контракт целиком",
  ],
  frames: [
    [
      py(
        "c",
        24,
        44,
        [
          "@abstractmethod",
          "def describe(self):",
          "    return 'общая часть'",
          "# наследник:",
          "def describe(self):",
          "    return super().describe() + '+своё'",
        ],
        [2, 5],
        {
          size: 10,
          lh: 20,
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
          "@property",
          "@abstractmethod",
          "def name(self): ...",
          "",
          "@classmethod",
          "@abstractmethod",
          "def create(cls): ...",
        ],
        [0, 1, 4, 5],
        {
          size: 10,
          lh: 18,
          w: 320,
        },
      ),
    ],
    [
      Box("a", 90, 56, 110, 28, "@property", "g", { size: 11 }),
      Box("b", 90, 100, 130, 28, "@abstractmethod", "y", { size: 10.5 }),
      Box("c", 270, 78, 90, 28, "def name", "b", { size: 11 }),
      arrow("e1", 90, 72, 90, 86, "m"),
      arrow("e2", 156, 100, 226, 82, "m"),
      Tx("n", 270, 118, "сверху → вниз", { size: 10 }),
    ],
  ],
});

// 5. Шаблонный метод
export const V05 = scene({
  labels: ["Алгоритм из шагов", "Свой шаг", "Порядок неизменен"],
  caption: [
    "Базовый класс содержит готовый алгоритм: заголовок, тело, подвал",
    "Заголовок и подвал общие, а тело — абстрактный шаг: у каждого отчёта своё",
    "Наследник пишет только недостающие шаги, порядок вызовов остаётся прежним — так устроены жизненные циклы фреймворков",
  ],
  frames: [
    [
      Box("a", 70, 70, 90, 30, "header()", "g", { size: 11 }),
      Box("b", 180, 70, 90, 30, "body()", "y", { size: 11 }),
      Box("c", 290, 70, 90, 30, "footer()", "g", { size: 11 }),
      arrow("e1", 116, 70, 134, 70, "m"),
      arrow("e2", 226, 70, 244, 70, "m"),
      Tx("n", 180, 118, "render()", { size: 11 }),
    ],
    [
      py(
        "c",
        24,
        44,
        [
          "class Report(ABC):",
          "    def render(self):",
          "        return self.header() + self.body() + self.footer()",
          "    @abstractmethod",
          "    def body(self): ...",
        ],
        [2, 3, 4],
        {
          size: 9.5,
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
          "class Sales(Report):",
          "    def body(self):",
          "        return 'продажи: 42'",
          "Sales().render()",
        ],
        [1, 2, 3],
        {
          size: 11,
          lh: 24,
          w: 320,
        },
      ),
    ],
  ],
});

// 6. Виртуальные наследники
export const V06 = scene({
  labels: ["register", "__subclasshook__", "Sized"],
  caption: [
    "ABC.register(Cls) объявляет класс подклассом без наследования — isinstance подтвердит",
    "__subclasshook__ задаёт условие автоматически: любой класс с нужным методом считается наследником",
    "Так устроены Sized и Iterable: объект с __len__ уже Sized, хотя ни от кого не наследуется",
  ],
  frames: [
    [
      py(
        "c",
        30,
        56,
        [
          "Quacker.register(Duck)",
          "isinstance(Duck(), Quacker)   # True",
          "issubclass(Duck, Quacker)   # True",
        ],
        [0],
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
        24,
        44,
        [
          "class HasLen(ABC):",
          "    @classmethod",
          "    def __subclasshook__(cls, C):",
          "        if cls is HasLen:",
          "            return hasattr(C, '__len__')",
          "        return NotImplemented",
        ],
        [4],
        {
          size: 10,
          lh: 20,
          w: 330,
        },
      ),
    ],
    [
      Box("a", 90, 70, 110, 30, "class Box:\n__len__", "b", { size: 9.5 }),
      Box("b", 270, 70, 100, 30, "Sized", "g", { size: 12 }),
      arrow("e", 146, 70, 218, 70, "g", { dash: true }),
      Tx("n", 180, 118, "isinstance(Box(), Sized) → True", { size: 10 }),
    ],
  ],
});

// 7. collections.abc
export const V07 = scene({
  labels: ["Готовые контракты", "Sequence", "Проверки"],
  caption: [
    "В collections.abc — Sequence, Mapping, Set, Iterable, Iterator, Callable и другие",
    "Для Sequence нужны __len__ и __getitem__; перебор, in, count, index, reversed появятся сами",
    "isinstance(x, Iterable) принимает любой итерируемый объект, а не только список",
  ],
  frames: [
    [
      ...["Sequence", "Mapping", "Set", "Iterable", "Iterator", "Callable"].map(
        (t, i) =>
          Box(
            `b${i}`,
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
      Box("a", 90, 44, 130, 24, "__len__", "g", { size: 10.5 }),
      Box("b", 90, 78, 130, 24, "__getitem__", "g", { size: 10.5 }),
      ...["__iter__", "__contains__", "count", "index", "__reversed__"].map(
        (t, i) =>
          Box(`m${i}`, 260, 30 + i * 28, 104, 22, t, "y", { size: 9.5 }),
      ),
    ],
    [
      py(
        "c",
        30,
        56,
        [
          "isinstance([], Iterable)       # True",
          "isinstance({}, Iterable)       # True",
          "isinstance(5, Iterable)        # False",
        ],
        undefined,
        {
          size: 10.5,
          lh: 26,
          w: 320,
        },
      ),
    ],
  ],
});

// 8. numbers
export const V08 = scene({
  labels: ["Числовая башня", "Integral", "Универсальность"],
  caption: [
    "Number ⊃ Complex ⊃ Real ⊃ Rational ⊃ Integral: каждый следующий уже предыдущего",
    "isinstance(x, Integral) принимает целые любых видов — int, bool, числа из сторонних библиотек",
    "Универсальные функции проверяйте по абстрактным классам, но часто лучше просто попробовать операцию",
  ],
  frames: [
    [
      ...["Number", "Complex", "Real", "Rational", "Integral"].map((t, i) =>
        Box(
          `n${i}`,
          180,
          24 + i * 30,
          220 - i * 36,
          22,
          t,
          ["m", "b", "g", "y", "v"][i],
          { size: 10.5 },
        ),
      ),
    ],
    [
      py(
        "c",
        40,
        56,
        [
          "isinstance(True, Integral)    # True",
          "isinstance(3.5, Integral)    # False",
          "isinstance(Fraction(1,2), Rational)",
        ],
        undefined,
        {
          size: 10.5,
          lh: 26,
          w: 310,
        },
      ),
    ],
    [
      Box("a", 90, 70, 110, 30, "Number", "g", { size: 12 }),
      Box("b", 270, 70, 110, 30, "ваш тип тоже", "b", { size: 10.5 }),
      Tx("n", 180, 118, "подойдут и чужие типы", { size: 10 }),
    ],
  ],
});

// 9. Принцип подстановки
export const V09 = scene({
  labels: ["Подстановка", "Не требуйте больше", "Не обещайте меньше"],
  caption: [
    "Наследник должен годиться везде, где требуется базовый класс (принцип Лисков)",
    "Базовый метод принимает любые числа, а наследник отвергает отрицательные — программа сломается неожиданно",
    "Базовый возвращает список, а наследник — None: контракт — не только названия, но и смысл; записывайте его в документации",
  ],
  frames: [
    [
      Box("a", 90, 70, 110, 30, "Base", "b", { size: 12 }),
      Box("b", 270, 70, 110, 30, "Child", "g", { size: 12 }),
      arrow("e", 216, 70, 146, 70, "g"),
      Tx("n", 180, 118, "везде, где ждут Base", { size: 10 }),
    ],
    [
      Box("a", 90, 60, 130, 28, "Base: любое число", "b", { size: 9.5 }),
      Box("b", 270, 60, 130, 28, "Child: x ≥ 0 ✗", "r", { size: 10 }),
      Tx("n", 180, 112, "нельзя ужесточать вход", { size: 10, c: "r" }),
    ],
    [
      Box("a", 90, 60, 130, 28, "Base → список", "b", { size: 10 }),
      Box("b", 270, 60, 130, 28, "Child → None ✗", "r", { size: 10 }),
      Tx("n", 180, 112, "нельзя ослаблять результат", { size: 10, c: "r" }),
    ],
  ],
});

// 10. Хранилища
export const V10 = scene({
  labels: ["Интерфейс", "Реализации", "Подмена в тестах"],
  caption: [
    "Storage описывает, что умеет любое хранилище: read и write",
    "Реализации: в памяти, на диске, в облаке — все выполняют контракт",
    "Приложение принимает Storage и не знает реализацию; в тестах подставляется простая замена (внедрение зависимостей)",
  ],
  frames: [
    [
      Box("s", 180, 50, 160, 34, "Storage (ABC)", "y", { size: 12 }),
      Box("r", 110, 110, 90, 22, "read()", "g", { size: 10.5 }),
      Box("w", 250, 110, 90, 22, "write()", "g", { size: 10.5 }),
    ],
    [
      Box("s", 180, 34, 140, 26, "Storage", "y", { size: 11 }),
      ...["Memory", "Disk", "Cloud"].map((t, i) =>
        Box(`i${i}`, 70 + i * 110, 112, 84, 26, t, "g", { size: 10.5 }),
      ),
      ...[0, 1, 2].map((i) =>
        arrow(`e${i}`, 70 + i * 110, 100, 140 + i * 40, 48, "m"),
      ),
    ],
    [
      Box("a", 70, 70, 80, 28, "приложение", "b", { size: 9 }),
      Box("s", 180, 70, 80, 28, "Storage", "y", { size: 11 }),
      Box("m", 296, 50, 80, 24, "Memory (тест)", "g", { size: 8 }),
      Box("d", 296, 92, 80, 24, "Disk (прод)", "g", { size: 8.5 }),
      arrow("e1", 112, 70, 138, 70, "y"),
      arrow("e2", 222, 66, 254, 54, "g"),
      arrow("e3", 222, 74, 254, 88, "g"),
    ],
  ],
});

// 11. Ловушки
export const V11 = scene({
  labels: ["Пустое тело", "Слишком много", "Лишний слой"],
  caption: [
    "Абстрактный метод с pass: наследник вызовет его через super() и не заметит проблемы — поднимайте NotImplementedError или пишите осмысленное тело",
    "Контракт из десяти обязательных методов трудно выполнить — держите его небольшим",
    "Реализация одна и меняться не будет? Абстрактный слой лишний — не превращайте в ABC каждый класс",
  ],
  frames: [
    [
      py(
        "c",
        30,
        56,
        [
          "@abstractmethod",
          "def save(self):",
          "    pass          # тихая пустота",
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
      ...Array.from({ length: 10 }, (_, i) =>
        Box(
          `m${i}`,
          44 + (i % 5) * 68,
          54 + Math.floor(i / 5) * 36,
          60,
          24,
          `m${i + 1}()`,
          "r",
          { size: 10 },
        ),
      ),
      Tx("n", 180, 132, "10 обязательных — многовато", { size: 10, c: "r" }),
    ],
    [
      Box("a", 90, 70, 110, 30, "ABC", "m", { size: 12 }),
      Box("b", 270, 70, 110, 30, "единственная\nреализация", "b", { size: 9 }),
      Tx("n", 180, 118, "слой не нужен", { size: 10.5, c: "y" }),
    ],
  ],
});

// 12. Три способа
export const V12 = scene({
  labels: ["Утки", "ABC", "Protocol"],
  caption: [
    "Утиная типизация: проста, но проверяется лишь при выполнении — для небольших скриптов хватает",
    "Абстрактные классы: проверка при создании объекта, нужны наследование, дают общие реализации и isinstance",
    "Протоколы: проверяются статически и не требуют наследования — следующая глава",
  ],
  frames: [
    [
      Box("a", 90, 70, 110, 34, "утки", "b", { size: 13 }),
      Box("b", 270, 70, 120, 34, "проверка при вызове", "m", { size: 9 }),
    ],
    [
      Box("a", 90, 70, 110, 34, "ABC", "g", { size: 13 }),
      Box("b", 270, 70, 130, 34, "проверка при создании", "g", { size: 9 }),
    ],
    [
      Box("a", 90, 70, 110, 34, "Protocol", "y", { size: 12 }),
      Box("b", 270, 70, 130, 34, "статическая проверка", "y", { size: 9 }),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["ABC", "Шаблонный метод", "Виртуальные", "Принципы"],
  caption: [
    "Наследуем ABC, помечаем @abstractmethod: пока не реализовано всё — экземпляр не создать",
    "Шаблонный метод строит алгоритм из общих и абстрактных шагов",
    "register и __subclasshook__ создают виртуальных наследников; collections.abc даёт готовые реализации",
    "Принцип подстановки и разумная небольшая иерархия",
  ],
  frames: [
    [
      Box("a", 90, 70, 100, 30, "ABC", "g", { size: 13 }),
      Box("b", 260, 70, 140, 30, "@abstractmethod", "y", { size: 10.5 }),
    ],
    [
      Box("a", 70, 70, 80, 28, "общий шаг", "g", { size: 10 }),
      Box("b", 180, 70, 80, 28, "абстрактный", "y", { size: 9.5 }),
      Box("c", 290, 70, 80, 28, "общий шаг", "g", { size: 10 }),
    ],
    [
      Box("a", 90, 70, 110, 30, "register", "b", { size: 11 }),
      Box("b", 270, 70, 130, 30, "__subclasshook__", "b", { size: 10 }),
    ],
    [
      Box("a", 90, 70, 110, 30, "Лисков", "y", { size: 12 }),
      Box("b", 270, 70, 130, 30, "малый контракт", "g", { size: 10.5 }),
    ],
  ],
});
