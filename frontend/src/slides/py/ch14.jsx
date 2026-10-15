// Слайды для «Python как первый язык», глава 14 — «Наследование и композиция».
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
      <span>PYTHON КАК ПЕРВЫЙ ЯЗЫК / КЛАССЫ / ГЛАВА 14</span>
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
      title={"Наследование и композиция"}
      sub={"Глава 14 · Классы"}
      main={"Наследование выражает «является», композиция — «имеет»: выбор определяет гибкость кода."}
    >
      <div className="s-grid2">
        {[["class B(A)", "Наследование", "Потомок берёт всё у родителя"], ["super()", "Родитель", "Вызвать версию из базового класса"], ["voice()", "Полиморфизм", "Один интерфейс — разные реализации"], ["self.engine", "Композиция", "Объект внутри объекта"]].map(([big, t, d]) => (
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
      title={"Наследование"}
      sub={"В скобках — родитель"}
      main={"Связь «является»: собака — животное, поэтому наследование уместно."}
    >
      <PyCode>{`class Animal:
    def __init__(self, name):
        self.name = name
    def hello(self):
        return f"Я {self.name}"

class Dog(Animal):
    pass

d = Dog("Шарик")
print(d.hello(), isinstance(d, Animal), issubclass(Dog, Animal))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Я Шарик True True"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Переопределение и super"}
      sub={"Заменить поведение — или дополнить"}
      main={"Переопределяя метод, решайте, нужна ли родительская версия, и вызывайте её через super()."}
    >
      <PyCode>{`class Animal:
    def __init__(self, name):
        self.name = name
    def voice(self):
        return "неизвестный звук"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
    def voice(self):
        return "гав"

d = Dog("Шарик", "овчарка")
print(d.name, d.breed, d.voice())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Шарик овчарка гав"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Полиморфизм"}
      sub={"Один вызов — разные ответы"}
      main={"Добавили класс — цикл без правок заговорил по-новому. Нужен только метод с тем же именем."}
    >
      <PyCode>{`class Animal:
    def voice(self):
        return "..."

class Dog(Animal):
    def voice(self):
        return "гав"

class Cat(Animal):
    def voice(self):
        return "мяу"

class Duck:                      # не наследник, но умеет voice
    def voice(self):
        return "кря"

for a in [Dog(), Cat(), Duck()]:
    print(a.voice())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"гав\nмяу\nкря"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Порядок разрешения методов"}
      sub={"Множественное наследование и __mro__"}
      main={"Множественное наследование чаще всего — для примесей; сомневаетесь — берите композицию."}
    >
      <PyCode>{`class A:
    def who(self):
        return "A"

class B(A):
    pass

class C(A):
    def who(self):
        return "C"

class D(B, C):
    pass

print(D().who())
print([k.__name__ for k in D.__mro__])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"C\n['D', 'B', 'C', 'A', 'object']"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Абстрактные классы"}
      sub={"Контракт: потомок обязан реализовать"}
      main={"Шаблон без самостоятельных объектов: пока не реализованы все абстрактные методы, создать экземпляр нельзя."}
    >
      <PyCode>{`from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...

class Sq(Shape):
    def __init__(self, a):
        self.a = a
    def area(self):
        return self.a ** 2

print(Sq(3).area())
Shape()`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"9\nTypeError: Can't instantiate abstract class Shape without an implementation for abstract method 'area'"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Композиция"}
      sub={"Автомобиль имеет двигатель"}
      main={"Предпочитайте композицию: части можно менять, не трогая остальное."}
    >
      <PyCode>{`class Engine:
    def start(self):
        return "двигатель запущен"

class Car:
    def __init__(self):
        self.engine = Engine()     # «имеет»
    def go(self):
        return self.engine.start() + ", поехали"

print(Car().go())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"двигатель запущен, поехали"}</Cmd>
      <div className="s-cols">
        <Node kind="" mono={true} title={"Dog(Animal)"} sub={"«является» → наследование"} />
        <Node kind="green" mono={true} title={"Car.engine"} sub={"«имеет» → композиция"} />
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"isinstance и type"}
      sub={"Проверка типов"}
      main={"isinstance учитывает иерархию, type — нет; а питонично — пробовать, а не проверять."}
    >
      <PyCode>{`class Animal:
    pass

class Dog(Animal):
    pass

d = Dog()
print(type(d) is Animal, isinstance(d, Animal))
print(hasattr(d, "voice"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"False True\nFalse"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Магические методы и потомки"}
      sub={"Универсальный __repr__"}
      main={"Переопределяя метод, сохраняйте его смысл: потомка можно подставить везде, где ждали родителя."}
    >
      <PyCode>{`class Base:
    def __init__(self, x):
        self.x = x
    def __repr__(self):
        return f"{type(self).__name__}({self.x})"

class Child(Base):
    pass

print(Base(1), Child(2))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Base(1) Child(2)"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Примеси"}
      sub={"Маленький класс — одна способность"}
      main={"Миксин добавляет умение без «является»: подмешали — и класс получил to_dict."}
    >
      <PyCode>{`class DictMixin:
    def to_dict(self):
        return dict(self.__dict__)

class User(DictMixin):
    def __init__(self, name):
        self.name = name

print(User("Аня").to_dict())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'name': 'Аня'}"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Пример: фигуры"}
      sub={"Общий интерфейс сверху, разные реализации снизу"}
      main={"Новая фигура добавляется одним классом — остальной код не меняется."}
    >
      <PyCode>{`from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): ...
    def __str__(self):
        return f"{type(self).__name__}: {self.area():.1f}"

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return 3.14159 * self.r ** 2

class Rect(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h

def get_area(s):
    return s.area()

shapes = [Circle(1), Rect(2, 3)]
for s in sorted(shapes, key=get_area, reverse=True):
    print(s)
print(sum(s.area() for s in shapes))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Rect: 6.0\nCircle: 3.1\n9.14159"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Забытый super().__init__()"}
      main={"Наследование — не способ «переиспользовать код»: без связи «является» нужна композиция."}
    >
      <PyCode>{`class A:
    def __init__(self):
        self.x = 1

class B(A):
    def __init__(self):
        self.y = 2           # забыли super().__init__()

print(B().x)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"AttributeError: 'B' object has no attribute 'x'"}</Cmd>
      <div className="s-note">{"Ещё: слишком глубокие иерархии, другая сигнатура у переопределённого метода, ромб без понимания MRO."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 14 · Классы"}
      main={"Мы закончили с классами: теперь вы описываете собственные типы данных."}
    >
      <div className="s-grid2">
        {[["class B(A)", "Наследование", "«Является»; super() вызывает родителя"], ["voice()", "Полиморфизм", "Общий интерфейс, утиная типизация"], ["ABC", "Абстрактные классы", "Контракт для потомков"], ["self.engine", "Композиция", "«Имеет» — гибче наследования"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — исключения и файлы: как программа справляется с ошибками и общается с внешним миром."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P14 = {
  "13:14": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P14).
export const SLIDE_TITLES_P14 = {
  "13:14": [
    "Наследование и композиция",
    "Наследование",
    "Переопределение и super",
    "Полиморфизм",
    "MRO",
    "Абстрактные классы",
    "Композиция",
    "isinstance и type",
    "Магия и потомки",
    "Примеси",
    "Пример: фигуры",
    "Типичные ошибки",
    "Итог",
  ],
};
