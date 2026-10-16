import { scene } from "./alg.jsx";
import { Tx } from "./hw.jsx";
import { Box, arrow, cc } from "./cl.jsx";

/* «Python как первый язык», глава 20: контейнеры, вызываемые объекты, менеджеры контекста. */

const py = (id, x, y, lines, hl, extra = {}) =>
  cc(id, x, y, lines, hl, { lang: "py", ...extra });

// 1. Общие умения контейнеров
const types = ["list", "dict", "set", "str"];
const skills = ["len(x)", "x[i]", "i in x", "for i in x"];
export const V01 = scene({
  labels: ["Одни умения", "Протоколы", "Ваш класс"],
  caption: [
    "Список, словарь, множество, строка — все умеют len, [], in и for",
    "Эти умения описаны специальными методами: __len__, __getitem__, __contains__, __iter__",
    "Реализуйте несколько методов — и ваш класс станет полноправным контейнером",
  ],
  frames: [
    [
      ...types.map((t, i) =>
        Box(`t${i}`, 52 + i * 86, 36, 70, 24, t, "b", { size: 11 }),
      ),
      ...skills.map((s, i) =>
        Box(`s${i}`, 52 + i * 86, 96, 72, 24, s, "g", { size: 9.5 }),
      ),
    ],
    [
      ...skills.map((s, i) =>
        Box(`s${i}`, 90, 30 + i * 30, 90, 22, s, "g", { size: 10 }),
      ),
      ...["__len__", "__getitem__", "__contains__", "__iter__"].map((m, i) =>
        Box(`m${i}`, 260, 30 + i * 30, 110, 22, m, "y", { size: 10 }),
      ),
      ...[0, 1, 2, 3].map((i) =>
        arrow(`e${i}`, 136, 30 + i * 30, 202, 30 + i * 30, "y"),
      ),
    ],
    [
      Box("a", 90, 70, 110, 34, "class Deck", "g", { size: 12 }),
      Box("b", 260, 70, 120, 34, "как list", "b", {
        size: 8.5,
      }),
      arrow("e", 146, 70, 198, 70, "g"),
    ],
  ],
});

// 2. Последовательность
export const V02 = scene({
  labels: ["Два метода", "Перебор", "Бесплатно"],
  caption: [
    "Для последовательности достаточно __len__ и __getitem__; нет индекса — IndexError",
    "Без __iter__ Питон перебирает индексы 0, 1, 2… пока не получит IndexError — по нему перебор останавливается",
    "Заработают for, in, reversed и отрицательные индексы (если передать работу внутреннему списку)",
  ],
  frames: [
    [
      py(
        "c",
        24,
        40,
        [
          "class Playlist:",
          "    def __init__(self, tracks):",
          "        self._t = list(tracks)",
          "    def __len__(self):",
          "        return len(self._t)",
          "    def __getitem__(self, i):",
          "        return self._t[i]",
        ],
        [3, 4, 5, 6],
        {
          size: 9.5,
          lh: 16,
          w: 300,
        },
      ),
    ],
    [
      ...[0, 1, 2].map((i) =>
        Box(`i${i}`, 60 + i * 70, 60, 54, 26, `[${i}]`, "g", { size: 11 }),
      ),
      Box("x", 270, 60, 80, 26, "[3] IndexError", "r", { size: 9 }),
      ...[0, 1, 2].map((i) =>
        arrow(`a${i}`, 90 + i * 70, 60, 106 + i * 70 - 8, 60, "g"),
      ),
      Tx("n", 180, 112, "for t in playlist: — стоп на IndexError", {
        size: 10,
      }),
    ],
    [
      Box("a", 90, 44, 140, 24, "for t in playlist", "g", { size: 10 }),
      Box("b", 90, 78, 140, 24, "'x' in playlist", "g", { size: 10 }),
      Box("c", 90, 112, 140, 24, "reversed(playlist)", "g", { size: 10 }),
      Box("d", 270, 78, 130, 36, "playlist[-1]\nработает", "y", { size: 9.5 }),
    ],
  ],
});

// 3. Срезы
export const V03 = scene({
  labels: ["Объект среза", "indices", "Свой тип"],
  caption: [
    "items[1:3] передаёт в __getitem__ объект slice(1, 3, None)",
    "slice.indices(len) выдаёт готовые начало, конец и шаг с учётом отрицательных значений",
    "Если нужен контейнер того же типа — проверьте isinstance(key, slice) и оберните результат",
  ],
  frames: [
    [
      py(
        "c",
        50,
        56,
        ["items[1:3]", "# → items.__getitem__(slice(1, 3, None))"],
        [1],
        {
          size: 11,
          lh: 28,
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
          "s = slice(-3, None)",
          "s.indices(5)     # (2, 5, 1)",
          "s.indices(10)    # (7, 10, 1)",
        ],
        [1, 2],
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
        24,
        44,
        [
          "def __getitem__(self, key):",
          "    if isinstance(key, slice):",
          "        return Playlist(self._t[key])",
          "    return self._t[key]",
        ],
        [1, 2],
        {
          size: 10.5,
          lh: 22,
          w: 310,
        },
      ),
    ],
  ],
});

// 4. Запись и удаление
export const V04 = scene({
  labels: ["Запись", "Удаление", "Какие ошибки"],
  caption: [
    "obj[k] = v вызывает __setitem__ — здесь можно проверять ключи и значения",
    "del obj[k] вызывает __delitem__",
    "Соглашение об ошибках: IndexError для последовательностей, KeyError для отображений; нет метода — нет операции",
  ],
  frames: [
    [
      py(
        "c",
        24,
        48,
        [
          "def __setitem__(self, key, value):",
          "    if not isinstance(key, str):",
          "        raise TypeError(key)",
          "    self._d[key] = value",
        ],
        [1, 2, 3],
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
        ["def __delitem__(self, key):", "    del self._d[key]"],
        [1],
        {
          size: 11,
          lh: 26,
          w: 310,
        },
      ),
      Tx("n", 180, 130, "нет ключа → KeyError из словаря", {
        size: 10,
        c: "y",
      }),
    ],
    [
      Box("a", 90, 50, 110, 28, "последовательность", "b", { size: 8.5 }),
      Box("b", 270, 50, 100, 28, "IndexError", "r", { size: 10.5 }),
      Box("c", 90, 100, 110, 28, "отображение", "g", { size: 10 }),
      Box("d", 270, 100, 100, 28, "KeyError", "r", { size: 10.5 }),
      arrow("e1", 146, 50, 218, 50, "r"),
      arrow("e2", 146, 100, 218, 100, "r"),
    ],
  ],
});

// 5. Проверка вхождения
export const V05 = scene({
  labels: ["__contains__", "Запасные пути", "Цена"],
  caption: [
    "x in obj вызывает obj.__contains__(x)",
    "Нет __contains__ — Питон пробует __iter__, а затем __getitem__ с индексами 0, 1, 2…",
    "Перебор медленный, поэтому если проверка может быть дешёвой, напишите __contains__ — например, для координат",
  ],
  frames: [
    [
      Box("a", 90, 70, 110, 30, "x in obj", "b", { size: 12 }),
      Box("b", 270, 70, 130, 30, "__contains__(x)", "g", { size: 10.5 }),
      arrow("e", 146, 70, 204, 70, "g"),
    ],
    [
      Box("a", 180, 36, 190, 24, "1. __contains__", "m", { size: 10 }),
      Box("b", 180, 72, 190, 24, "2. __iter__ — перебор", "y", { size: 10 }),
      Box("c", 180, 108, 190, 24, "3. __getitem__(0, 1, 2…)", "y", {
        size: 10,
      }),
    ],
    [
      py(
        "c",
        24,
        48,
        [
          "def __contains__(self, pos):",
          "    x, y = pos",
          "    return 0 <= x < self.w and 0 <= y < self.h",
        ],
        [2],
        {
          size: 10.5,
          lh: 24,
          w: 310,
        },
      ),
      Tx("n", 180, 130, "два неравенства вместо обхода всех клеток", {
        size: 10,
        c: "g",
      }),
    ],
  ],
});

// 6. Кортеж как ключ
const gridCells = (hot) => {
  const out = [];
  for (let r = 0; r < 3; r++)
    for (let c = 0; c < 4; c++)
      out.push(
        Box(
          `g${r}${c}`,
          44 + c * 36,
          40 + r * 32,
          32,
          28,
          `${c},${r}`,
          hot && hot[0] === c && hot[1] === r ? "g" : "m",
          {
            size: 8.5,
          },
        ),
      );
  return out;
};
export const V06 = scene({
  labels: ["Поле", "grid[2, 1]", "Границы"],
  caption: [
    "Ключ в квадратных скобках не обязан быть числом: поле можно адресовать парой координат",
    "grid[2, 1] передаёт в __getitem__ кортеж (2, 1); метод разбирает его и берёт клетку",
    "Выход за поле — IndexError: перебор и поведение совпадают с остальными последовательностями",
  ],
  frames: [
    [...gridCells(null), Tx("n", 270, 70, "колонка,\nстрока", { size: 9.5 })],
    [
      ...gridCells([2, 1]),
      py("c", 205, 60, ["grid[2, 1]", "# key = (2, 1)"], [1], {
        size: 10,
        lh: 20,
        w: 140,
      }),
    ],
    [
      ...gridCells([2, 1]),
      py("c", 205, 56, ["grid[9, 9]", "# IndexError"], undefined, {
        size: 10,
        lh: 20,
        w: 140,
        bad: [1],
      }),
    ],
  ],
});

// 7. Mapping
export const V07 = scene({
  labels: ["Три метода", "Бесплатно", "Изменяемые"],
  caption: [
    "От Mapping достаточно трёх методов: __getitem__ (KeyError, если ключа нет), __iter__ и __len__",
    "Остальное уже есть: keys, values, items, get, in, ==",
    "MutableMapping дополнительно требует __setitem__ и __delitem__",
  ],
  frames: [
    [
      Box("m", 180, 28, 120, 24, "class M(Mapping)", "b", { size: 10.5 }),
      ...["__getitem__", "__iter__", "__len__"].map((t, i) =>
        Box(`r${i}`, 70 + i * 110, 80, 98, 26, t, "g", { size: 10 }),
      ),
    ],
    [
      ...["__getitem__", "__iter__", "__len__"].map((t, i) =>
        Box(`r${i}`, 70 + i * 110, 36, 98, 22, t, "g", { size: 9.5 }),
      ),
      ...["keys()", "values()", "items()", "get()", "in", "=="].map((t, i) =>
        Box(
          `f${i}`,
          62 + (i % 3) * 100,
          90 + Math.floor(i / 3) * 34,
          80,
          24,
          t,
          "y",
          { size: 10.5 },
        ),
      ),
    ],
    [
      Box("m", 180, 28, 190, 24, "class M(MutableMapping)", "b", {
        size: 10.5,
      }),
      ...[
        "__getitem__",
        "__iter__",
        "__len__",
        "__setitem__",
        "__delitem__",
      ].map((t, i) =>
        Box(
          `r${i}`,
          62 + (i % 3) * 112,
          78 + Math.floor(i / 3) * 36,
          104,
          24,
          t,
          i > 2 ? "r" : "g",
          { size: 9.5 },
        ),
      ),
    ],
  ],
});

// 8. Наследование от встроенных
export const V08 = scene({
  labels: ["Обход", "UserDict", "__missing__"],
  caption: [
    "Наследник dict не вызывает ваш __setitem__ из update: проверка обойдена",
    "UserDict написан на питоне и честно вызывает ваши методы — используйте его",
    "У наследника dict метод __missing__ вызывается при отсутствии ключа; на нём построен defaultdict",
  ],
  frames: [
    [
      py(
        "c",
        24,
        44,
        [
          "class Strict(dict):",
          "    def __setitem__(self, k, v):",
          "        assert isinstance(k, str)",
          "        super().__setitem__(k, v)",
          "s.update({1: 2})   # проверку обошли",
        ],
        undefined,
        {
          size: 9.5,
          lh: 18,
          w: 320,
          bad: [4],
        },
      ),
    ],
    [
      Box("a", 90, 60, 110, 30, "dict (на C)", "r", { size: 10.5 }),
      Box("b", 260, 60, 130, 30, "UserDict (на Python)", "g", { size: 9.5 }),
      Tx("n", 180, 120, "второй уважает ваши переопределения", {
        size: 10,
        c: "g",
      }),
    ],
    [
      py(
        "c",
        24,
        50,
        [
          "class Upper(dict):",
          "    def __missing__(self, key):",
          "        self[key] = key.upper()",
          "        return self[key]",
          "d = Upper(); d['a']   # 'A'",
        ],
        [1, 2, 3],
        {
          size: 10,
          lh: 20,
          w: 320,
        },
      ),
    ],
  ],
});

// 9. __call__
export const V09 = scene({
  labels: ["Объект как функция", "Состояние", "callable"],
  caption: [
    "__call__ позволяет вызывать экземпляр круглыми скобками",
    "В отличие от функции, объект помнит состояние: счётчик вызовов, кэш, настраиваемый множитель",
    "callable(x) говорит, можно ли вызвать значение; функции, классы и методы вызываются так же",
  ],
  frames: [
    [
      py(
        "c",
        24,
        44,
        [
          "class Multiplier:",
          "    def __init__(self, k):",
          "        self.k = k",
          "    def __call__(self, x):",
          "        return x * self.k",
          "triple = Multiplier(3); triple(5)",
        ],
        [3, 4],
        {
          size: 9.5,
          lh: 18,
          w: 320,
        },
      ),
    ],
    [
      py(
        "c",
        30,
        46,
        [
          "counter = Counter()",
          "counter()   # 1",
          "counter()   # 2",
          "counter()   # 3",
        ],
        undefined,
        {
          size: 11.5,
          lh: 24,
          w: 200,
        },
      ),
      Box("s", 280, 70, 70, 36, "count\n3", "g", { size: 10 }),
    ],
    [
      ...["len", "Point", "obj.method", "Mult(3)", "42"].map((t, i) =>
        Box(`c${i}`, 56 + i * 62, 56, 56, 24, t, i < 4 ? "g" : "r", {
          size: 8,
        }),
      ),
      Tx("n", 180, 100, "callable → True, True, True, True, False", {
        size: 9.5,
      }),
    ],
  ],
});

// 10. with
export const V10 = scene({
  labels: ["Вход", "Блок", "Выход", "Ошибка"],
  caption: [
    "with obj as name: вызывает obj.__enter__() и записывает результат в name",
    "Выполняется тело блока",
    "Затем всегда вызывается obj.__exit__(None, None, None) — подготовка и уборка выступают парой",
    "Если в блоке случилась ошибка, __exit__ получает (тип, исключение, трассировка); истина — подавить, иначе ошибка полетит дальше",
  ],
  frames: [
    [
      Box("a", 70, 70, 100, 30, "__enter__", "g", { size: 11 }),
      Box("b", 180, 70, 80, 30, "блок", "m", { size: 11 }),
      Box("c", 290, 70, 100, 30, "__exit__", "m", { size: 11 }),
      arrow("e1", 122, 70, 138, 70, "m"),
      arrow("e2", 222, 70, 238, 70, "m"),
    ],
    [
      Box("a", 70, 70, 100, 30, "__enter__", "m", { size: 11 }),
      Box("b", 180, 70, 80, 30, "блок", "g", { size: 11 }),
      Box("c", 290, 70, 100, 30, "__exit__", "m", { size: 11 }),
      arrow("e1", 122, 70, 138, 70, "m"),
      arrow("e2", 222, 70, 238, 70, "m"),
    ],
    [
      Box("a", 70, 70, 100, 30, "__enter__", "m", { size: 11 }),
      Box("b", 180, 70, 80, 30, "блок", "m", { size: 11 }),
      Box("c", 290, 70, 100, 30, "__exit__", "g", { size: 11 }),
      arrow("e1", 122, 70, 138, 70, "m"),
      arrow("e2", 222, 70, 238, 70, "g"),
    ],
    [
      Box("a", 70, 56, 100, 30, "__enter__", "m", { size: 11 }),
      Box("b", 180, 56, 80, 30, "блок ✗", "r", { size: 11 }),
      Box("c", 290, 56, 100, 30, "__exit__(exc…)", "y", { size: 10 }),
      arrow("e1", 122, 56, 138, 56, "m"),
      arrow("e2", 222, 56, 238, 56, "r"),
      Tx("n", 180, 112, "True → ошибка подавлена; иначе летит дальше", {
        size: 10,
        c: "y",
      }),
    ],
  ],
});

// 11. contextmanager
export const V11 = scene({
  labels: ["Генератор", "До yield", "После yield"],
  caption: [
    "@contextmanager превращает функцию-генератор в менеджер контекста",
    "Всё до yield — вход; значение yield попадает в «as»",
    "Всё после yield — выход; try/finally гарантирует уборку и при ошибке",
  ],
  frames: [
    [
      py(
        "c",
        24,
        40,
        [
          "from contextlib import contextmanager",
          "",
          "@contextmanager",
          "def tag(name):",
          "    print(f'<{name}>')",
          "    try:",
          "        yield",
          "    finally:",
          "        print(f'</{name}>')",
        ],
        undefined,
        {
          size: 9.5,
          lh: 15,
          w: 320,
        },
      ),
    ],
    [
      py(
        "c",
        24,
        40,
        [
          "from contextlib import contextmanager",
          "",
          "@contextmanager",
          "def tag(name):",
          "    print(f'<{name}>')",
          "    try:",
          "        yield",
          "    finally:",
          "        print(f'</{name}>')",
        ],
        [4, 5, 6],
        {
          size: 9.5,
          lh: 15,
          w: 320,
        },
      ),
    ],
    [
      py(
        "c",
        24,
        40,
        [
          "from contextlib import contextmanager",
          "",
          "@contextmanager",
          "def tag(name):",
          "    print(f'<{name}>')",
          "    try:",
          "        yield",
          "    finally:",
          "        print(f'</{name}>')",
        ],
        [7, 8],
        {
          size: 9.5,
          lh: 15,
          w: 320,
        },
      ),
    ],
  ],
});

// 12. Игровое поле
export const V12 = scene({
  labels: ["Длина и клетки", "Контейнер и with", "Всё вместе"],
  caption: [
    "Grid: __len__ — число клеток, __getitem__/__setitem__ по кортежу (x, y), __contains__ для координат",
    "__iter__ перебирает клетки, __call__ собирает копию с другой заливкой",
    "Менеджер контекста откатывает все изменения, если внутри блока случилась ошибка",
  ],
  frames: [
    [
      ...["__len__", "__getitem__", "__setitem__", "__contains__"].map((t, i) =>
        Box(
          `m${i}`,
          70 + (i % 2) * 130,
          50 + Math.floor(i / 2) * 36,
          118,
          26,
          t,
          "g",
          { size: 10.5 },
        ),
      ),
    ],
    [
      ...["__iter__", "__call__"].map((t, i) =>
        Box(`m${i}`, 70 + i * 130, 56, 118, 26, t, "b", { size: 10.5 }),
      ),
      Tx("n", 180, 110, "перебор клеток · копия с заливкой", { size: 10 }),
    ],
    [
      py(
        "c",
        30,
        50,
        [
          "with grid.transaction():",
          "    grid[1, 1] = '#'",
          "    grid[9, 9] = '#'   # IndexError",
          "# поле вернулось к прежнему виду",
        ],
        [3],
        {
          size: 10.5,
          lh: 22,
          w: 320,
        },
      ),
    ],
  ],
});

// 13. Итоги
export const V13 = scene({
  labels: ["Последовательность", "Запись и in", "Отображения", "Вызов и with"],
  caption: [
    "__len__ и __getitem__ с IndexError; срез приходит объектом slice",
    "__setitem__, __delitem__ и __contains__ — запись, удаление, вхождение",
    "Отображения строят на абстрактных классах коллекций, а не на наследовании от dict",
    "__call__ делает объект вызываемым, __enter__ и __exit__ — менеджером контекста",
  ],
  frames: [
    [
      Box("a", 90, 70, 100, 30, "__len__", "g", { size: 11 }),
      Box("b", 250, 70, 110, 30, "__getitem__", "g", { size: 11 }),
    ],
    [
      Box("a", 70, 70, 100, 30, "__setitem__", "y", { size: 10.5 }),
      Box("b", 180, 70, 100, 30, "__delitem__", "y", { size: 10.5 }),
      Box("c", 290, 70, 100, 30, "__contains__", "y", { size: 10.5 }),
    ],
    [
      Box("a", 90, 70, 130, 30, "Mapping", "b", { size: 11 }),
      Box("b", 260, 70, 130, 30, "UserDict", "b", { size: 11 }),
    ],
    [
      Box("a", 90, 70, 100, 30, "__call__", "g", { size: 11 }),
      Box("b", 210, 70, 100, 30, "__enter__", "g", { size: 11 }),
      Box("c", 320, 70, 80, 30, "__exit__", "g", { size: 11 }),
    ],
  ],
});
