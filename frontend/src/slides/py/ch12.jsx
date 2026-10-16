import { makeSlide } from "../SlideFrame.tsx";
// Слайды для «Python как первый язык», глава 12 — «Классы».
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

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / КЛАССЫ / ГЛАВА 12", 13);

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
      title={"Классы"}
      sub={"Глава 12 · Классы"}
      main={"Класс объединяет данные и действия над ними в один тип."}
    >
      <div className="s-grid2">
        {[["class Dog:", "Класс", "Чертёж: из него делают объекты-экземпляры"], ["__init__", "Конструктор", "Задаёт начальные данные при создании"], ["self", "Методы", "Функции внутри класса; self — сам объект"], ["__str__", "Вывод", "Как объект показывается человеку"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <p className="s-hint">{"Строка, список, словарь — тоже классы; теперь делаем свои типы."}</p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Класс и объект"}
      sub={"Чертёж и то, что по нему сделано"}
      main={"Из одного класса — сколько угодно экземпляров, и каждый живёт сам по себе."}
    >
      <PyCode>{`class Dog:
    pass

d = Dog()
print(type(d))
print(isinstance(d, Dog))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"<class '__main__.Dog'>\nTrue"}</Cmd>
      <div className="s-note">{"Имена классов — с заглавной буквы: так их отличают от функций."}</div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Конструктор и атрибуты"}
      sub={"__init__ вызывается при создании объекта"}
      main={"Конструктор гарантирует: любой объект рождается в полном порядке."}
    >
      <PyCode>{`class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

d = Dog("Шарик", 3)
print(d.name, d.age)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Шарик 3"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Методы"}
      sub={"Функции внутри класса"}
      main={"Данные и действия рядом: чтобы понять объект, достаточно прочитать его класс."}
    >
      <PyCode>{`class Counter:
    def __init__(self):
        self.value = 0

    def inc(self):
        self.value += 1

c = Counter()
c.inc()
c.inc()
print(c.value)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Что такое self"}
      sub={"Сам объект, у которого вызвали метод"}
      main={"Метод один на всех, а данные у каждого экземпляра свои."}
    >
      <PyCode>{`class Counter:
    def __init__(self):
        self.value = 0
    def inc(self):
        self.value += 1

a = Counter()
b = Counter()
a.inc()
print(a.value, b.value)
Counter.inc(a)      # то же, что a.inc()
print(a.value)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 0\n2"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Атрибуты класса и экземпляра"}
      sub={"Общее для всех — и своё у каждого"}
      main={"Изменяемые данные создавайте в __init__, а не на уровне класса."}
    >
      <PyCode>{`class Dog:
    legs = 4                  # общий
    def __init__(self, name):
        self.name = name      # свой

a, b = Dog("А"), Dog("Б")
print(a.legs, b.legs, Dog.legs)

class Bad:
    items = []                # ловушка: список на всех

x, y = Bad(), Bad()
x.items.append(1)
print(y.items)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"4 4 4\n[1]"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Объекты и ссылки"}
      sub={"Присваивание не копирует"}
      main={"Объект ведёт себя как пакет с адресом: два имени могут указывать на один экземпляр."}
    >
      <PyCode>{`class Box:
    def __init__(self, v):
        self.v = v

a = Box(1)
b = a              # одно имя на двоих
b.v = 99
print(a.v)
print(Box(1) == Box(1))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"99\nFalse"}</Cmd>
      <div className="s-note">{"== по умолчанию сравнивает сами объекты, а не их данные: настроим в следующей главе."}</div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"__str__ и __repr__"}
      sub={"Как объект выглядит в print и в консоли"}
      main={"__str__ — для человека, __repr__ — для разработчика."}
    >
      <PyCode>{`class Dog:
    def __init__(self, name, age):
        self.name, self.age = name, age
    def __str__(self):
        return f"Собака {self.name}, {self.age} г."
    def __repr__(self):
        return f"Dog({self.name!r}, {self.age})"

d = Dog("Шарик", 3)
print(d)
print(repr(d))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Собака Шарик, 3 г.\nDog('Шарик', 3)"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Инкапсуляция"}
      sub={"Класс охраняет свои правила"}
      main={"Одно подчёркивание — «внутреннее, не трогайте»; правки идут через методы."}
    >
      <PyCode>{`class Account:
    def __init__(self):
        self._balance = 0
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("сумма должна быть положительной")
        self._balance += amount
    def balance(self):
        return self._balance

a = Account()
a.deposit(100)
print(a.balance())
a.deposit(-5)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"100\nValueError: сумма должна быть положительной"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Объекты в коллекциях"}
      sub={"Списки и словари — с осмысленными элементами"}
      main={"Всё про списки и словари работает дальше — только элементы стали богаче."}
    >
      <PyCode>{`class Dog:
    def __init__(self, name, age):
        self.name, self.age = name, age

dogs = [Dog("Рекс", 5), Dog("Бим", 2), Dog("Лаки", 8)]
print([d.name for d in dogs if d.age > 3])

def get_age(d):
    return d.age

print([d.name for d in sorted(dogs, key=get_age)])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['Рекс', 'Лаки']\n['Бим', 'Рекс', 'Лаки']"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Как придумать класс"}
      sub={"Существительные — классы, глаголы — методы"}
      main={"Снаружи видны только понятные операции — как устроено внутри, знать не нужно."}
    >
      <PyCode>{`class Stack:
    def __init__(self):
        self._items = []
    def push(self, x):
        self._items.append(x)
    def pop(self):
        return self._items.pop()
    def is_empty(self):
        return not self._items

s = Stack()
s.push(1)
s.push(2)
print(s.pop(), s.is_empty())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2 False"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Забытый self"}
      main={"В описании метода self обязателен, а внутри метода атрибут — всегда self.имя."}
    >
      <PyCode>{`class A:
    def hello():        # забыт self
        return "hi"

A().hello()`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"TypeError: A.hello() takes 0 positional arguments but 1 was given"}</Cmd>
      <div className="s-note">{"Ещё: _init_ вместо __init__, список на уровне класса, метод без скобок, опечатка в имени атрибута."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 12 · Классы"}
      main={"Класс — чертёж типа, объект — экземпляр; инит задаёт данные, self — сам объект."}
    >
      <div className="s-grid2">
        {[["class · __init__", "Класс и объект", "Атрибуты экземпляра свои, класса — общие"], ["def m(self)", "Методы", "self — первым параметром, внутри self.атрибут"], ["a = b", "Ссылки", "Не копирует; == по умолчанию сравнивает объекты"], ["__str__ · _x", "Вывод и порядок", "str для людей; подчёркивание — внутреннее"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — магические методы, свойства и методы класса."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P12 = {
  "13:12": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P12).
export const SLIDE_TITLES_P12 = {
  "13:12": [
    "Классы",
    "Класс и объект",
    "Конструктор",
    "Методы",
    "Что такое self",
    "Атрибуты класса",
    "Объекты и ссылки",
    "__str__ и __repr__",
    "Инкапсуляция",
    "Объекты в коллекциях",
    "Как придумать класс",
    "Типичные ошибки",
    "Итог",
  ],
};
