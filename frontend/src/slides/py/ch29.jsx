// Слайды для «Изучаем Python», глава 29 — «Данные и типы: dataclasses, enum, typing, copy».
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
      <span>ИЗУЧАЕМ ПИТОН / СТАНДАРТНАЯ БИБЛИОТЕКА / ГЛАВА 29</span>
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
      title={"Данные и типы"}
      sub={"Глава 29 · Стандартная библиотека"}
      main={"Типы описывают предметную область: аккуратные данные — аккуратный проект."}
    >
      <div className="s-grid2">
        {[["@dataclass", "Датакласс", "Запись без шаблонного кода"], ["Enum", "Перечисление", "Именованные константы вместо магических чисел"], ["x: int", "Подсказки типов", "Документация и статический анализ"], ["copy · deepcopy", "Копирование", "Поверхностное и глубокое"]].map(([big, t, d]) => (
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
      title={"dataclass"}
      sub={"Конструктор, repr и сравнение — автоматически"}
      main={"Аннотации в датаклассе — описание полей, а не проверка значений."}
    >
      <PyCode>{`from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int = 18

u = User("Аня", 20)
print(u)
print(u == User("Аня", 20), User("Боря"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"User(name='Аня', age=20)\nTrue User(name='Боря', age=18)"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Параметры и инструменты"}
      sub={"field, frozen, order, __post_init__"}
      main={"Изменяемые значения по умолчанию — только через field(default_factory=...)."}
    >
      <PyCode>{`from dataclasses import dataclass, field, asdict, replace

@dataclass(frozen=True, order=True)
class Item:
    name: str
    price: int
    tags: tuple = ()

a, b = Item("а", 5), Item("б", 3)
print(sorted([a, b])[0].name, asdict(a))
print(replace(a, price=10))
try:
    a.price = 1
except Exception as e:
    print(type(e).__name__)

@dataclass
class Cart:
    items: list = field(default_factory=list)
    def __post_init__(self):
        self.count = len(self.items)

print(Cart([1, 2]).count, Cart().items)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"а {'name': 'а', 'price': 5, 'tags': ()}\nItem(name='а', price=10, tags=())\nFrozenInstanceError\n2 []"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Что выбрать"}
      sub={"dict, tuple, namedtuple, dataclass, class"}
      main={"Структура важнее — датакласс; поведение важнее — обычный класс."}
    >
      <div className="s-cols">
        <Node kind="" mono={true} title={"dict"} sub={"Свободная структура: ответ сервиса, настройки"} />
        <Node kind="" mono={true} title={"tuple"} sub={"Маленькая запись из функции"} />
        <Node kind="green" mono={true} title={"namedtuple"} sub={"Неизменяемая запись без логики"} />
        <Node kind="green" mono={true} title={"dataclass"} sub={"Типизированные поля, возможно изменяемые"} />
        <Node kind="amber" mono={true} title={"class"} sub={"Поведение и сложная инициализация"} />
      </div>
      <div className="s-note">{"Если вокруг записи много методов — пора на полноценный класс."}</div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Enum"}
      sub={"Именованные константы"}
      main={"Опечатка в имени члена вызывает ошибку сразу, а редактор подсказывает варианты."}
    >
      <PyCode>{`from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

print(Color.RED, Color.RED.name, Color.RED.value)
print(Color(2), Color["BLUE"], list(Color))
print(Color.RED is Color(1))
try:
    Color(9)
except ValueError as e:
    print(e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Color.RED RED 1\nColor.GREEN Color.BLUE [<Color.RED: 1>, <Color.GREEN: 2>, <Color.BLUE: 3>]\nTrue\n9 is not a valid Color"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Варианты перечислений"}
      sub={"str-Enum, Flag, IntEnum"}
      main={"К перечислению можно добавлять методы: тогда каждый член умеет что-то делать."}
    >
      <PyCode>{`from enum import Enum, IntEnum, Flag, auto

class Status(str, Enum):
    NEW = "new"
    DONE = "done"
    def is_final(self):
        return self is Status.DONE

class Perm(Flag):
    R = auto()
    W = auto()
    X = auto()

rw = Perm.R | Perm.W
print(Status("done").is_final(), Status.NEW == "new")
print(rw, Perm.W in rw, Perm.X in rw)

class Level(IntEnum):
    LOW = 1
    HIGH = 3

print(Level.LOW < Level.HIGH, Level.HIGH + 1)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True True\nPerm.R|W True False\nTrue 4"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Подсказки типов"}
      sub={"Аннотации параметров и результата"}
      main={"Питон ничего не проверяет: подсказки читают человек, редактор и анализатор."}
    >
      <PyCode>{`def add(a: int, b: int = 0) -> int:
    return a + b

def first(items: list[str]) -> str | None:
    return items[0] if items else None

print(add(1, 2), first(["а"]), first([]))
print(add.__annotations__)
print(add("a", "b"))        # не проверяется!`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3 а None\n{'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}\nab"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Зачем подсказки"}
      sub={"Callable, Literal, Any"}
      main={"Честная документация, поиск ошибок до запуска, лучшие подсказки редактора."}
    >
      <PyCode>{`from typing import Callable, Literal, Any

def apply(f: Callable[[int], int], x: int) -> int:
    return f(x)

Mode = Literal["r", "w"]

def open_mode(m: Mode) -> str:
    return f"режим {m}"

def parse(v: Any) -> int:
    return int(v)

print(apply(abs, -5), open_mode("r"), parse("7"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"5 режим r 7"}</Cmd>
      <div className="s-note">{"Статический анализатор (mypy, pyright) заметит строку там, где нужно число."}</div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"TypedDict, NamedTuple, Protocol"}
      sub={"Типы для структур и интерфейсов"}
      main={"Протокол — формализованная утиная типизация: подходит любой объект с нужными методами."}
    >
      <PyCode>{`from typing import TypedDict, NamedTuple, Protocol

class Movie(TypedDict):
    title: str
    year: int

class Point(NamedTuple):
    x: int
    y: int

class Speaker(Protocol):
    def speak(self) -> str: ...

class Dog:
    def speak(self) -> str:
        return "гав"

def talk(s: Speaker) -> str:
    return s.speak()

m: Movie = {"title": "Матрица", "year": 1999}
print(m["year"], Point(1, 2), talk(Dog()))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1999 Point(x=1, y=2) гав"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"match / case"}
      sub={"Структурное сопоставление"}
      main={"Образец _ — «подходит всё»; его ставят последним, иначе часть значений останется без ответа."}
    >
      <PyCode>{`def run(cmd):
    match cmd:
        case ["go", int(n)]:
            return f"идём на {n}"
        case ["say", *words]:
            return " ".join(words)
        case {"type": "quit"}:
            return "выход"
        case _:
            return "не понял"

print(run(["go", 10]), run(["say", "а", "б"]), run({"type": "quit"}), run(5))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"идём на 10 а б выход не понял"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"copy и deepcopy"}
      sub={"Поверхностная и глубокая копия"}
      main={"Для вложенных изменяемых данных, которые должны стать независимыми, нужен deepcopy."}
    >
      <PyCode>{`import copy

a = [[1, 2], [3]]
shallow = copy.copy(a)
deep = copy.deepcopy(a)
a[0].append(99)
print(shallow[0], deep[0])
print(shallow is a, shallow[0] is a[0], deep[0] is a[0])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[1, 2, 99] [1, 2]\nFalse True False"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Изменяемое по умолчанию в датаклассе"}
      main={"Подсказки — обещание: устаревшая хуже, чем её отсутствие; внешние данные проверяйте на лету."}
    >
      <PyCode>{`from dataclasses import dataclass, field

try:
    @dataclass
    class Bad:
        items: list = []
except ValueError as e:
    print(e)

@dataclass
class Good:
    items: list = field(default_factory=list)

print(Good().items is Good().items)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"mutable default <class 'list'> for field items is not allowed: use default_factory\nFalse"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 29 · Стандартная библиотека"}
      main={"Опишите данные аккуратно — и код останется понятным через годы."}
    >
      <div className="s-grid2">
        {[["@dataclass", "Датаклассы", "field, frozen, order, replace, asdict"], ["Enum · Flag", "Перечисления", "Имена вместо магических чисел"], ["typing · match", "Типы и разбор", "Подсказки, TypedDict, Protocol, match"], ["copy · deepcopy", "Копирование", "Вложенное — deepcopy"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — тестирование."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P29 = {
  "13:29": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P29).
export const SLIDE_TITLES_P29 = {
  "13:29": [
    "Данные и типы",
    "dataclass",
    "Параметры dataclass",
    "Что выбрать",
    "Enum",
    "Варианты Enum",
    "Подсказки типов",
    "Зачем подсказки",
    "Структуры и протоколы",
    "match / case",
    "copy и deepcopy",
    "Типичные ошибки",
    "Итог",
  ],
};
