// Слайды для «Python как первый язык», глава 13 — «Классы: методы и свойства».
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
      <span>PYTHON КАК ПЕРВЫЙ ЯЗЫК / КЛАССЫ / ГЛАВА 13</span>
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
      title={"Классы: методы и свойства"}
      sub={"Глава 13 · Классы"}
      main={"Собственные объекты начинают вести себя как части самого языка."}
    >
      <div className="s-grid2">
        {[["__add__ · __eq__", "Операторы", "Плюс, равно и сравнение — это методы"], ["__len__ · []", "Контейнеры", "len, индексы и in для своего класса"], ["@property", "Свойства", "Метод, который выглядит как атрибут"], ["@classmethod", "Методы класса", "Альтернативные конструкторы"]].map(([big, t, d]) => (
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
      title={"Операторы — это методы"}
      sub={"a + b вызывает a.__add__(b)"}
      main={"Метод оператора не меняет исходные объекты, а возвращает новый."}
    >
      <PyCode>{`class Vec:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)
    def __repr__(self):
        return f"Vec({self.x}, {self.y})"

print(Vec(1, 2) + Vec(3, 4))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Vec(4, 6)"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Равенство и хеш"}
      sub={"__eq__ сравнивает по значению"}
      main={"Описали __eq__ — описывайте и __hash__, иначе объект нельзя взять в ключ словаря."}
    >
      <PyCode>{`class P:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))

print(P(1, 2) == P(1, 2), P(1, 2) is P(1, 2))
d = {P(1, 2): "точка"}
print(P(1, 2) in d)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True False\nTrue"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Порядок и сортировка"}
      sub={"__lt__ учит объекты сравниваться"}
      main={"Есть __lt__ — работают sorted, min и max без параметра key."}
    >
      <PyCode>{`class Card:
    def __init__(self, rank):
        self.rank = rank
    def __lt__(self, other):
        return self.rank < other.rank
    def __repr__(self):
        return f"Card({self.rank})"

cards = [Card(7), Card(2), Card(9)]
print(sorted(cards))
print(max(cards))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[Card(2), Card(7), Card(9)]\nCard(9)"}</Cmd>
      <div className="s-note">{"Остальные операторы порядка достраивает декоратор total_ordering из functools."}</div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Свой контейнер"}
      sub={"__len__, __getitem__, __contains__"}
      main={"Хотите, чтобы объект вёл себя как список, — реализуйте нужные методы."}
    >
      <PyCode>{`class Playlist:
    def __init__(self, songs):
        self._songs = songs
    def __len__(self):
        return len(self._songs)
    def __getitem__(self, i):
        return self._songs[i]
    def __contains__(self, s):
        return s in self._songs

p = Playlist(["a", "b", "c"])
print(len(p), p[1], "c" in p, bool(Playlist([])))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3 b True False"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Свойство property"}
      sub={"Метод, который читается как атрибут"}
      main={"Хранится способ получить значение, а не само значение — оно всегда актуально."}
    >
      <PyCode>{`class Rect:
    def __init__(self, w, h):
        self.w, self.h = w, h
    @property
    def area(self):
        return self.w * self.h

r = Rect(3, 4)
print(r.area)
r.w = 10
print(r.area)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"12\n40"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Сеттер и проверка"}
      sub={"Присваивание под охраной класса"}
      main={"Снаружи — обычное присваивание, внутри — проверка; значение хранится в _age."}
    >
      <PyCode>{`class Person:
    def __init__(self, age):
        self.age = age            # вызовет сеттер
    @property
    def age(self):
        return self._age
    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("возраст не может быть отрицательным")
        self._age = value

p = Person(20)
p.age = 21
print(p.age)
p.age = -1`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"21\nValueError: возраст не может быть отрицательным"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Метод класса"}
      sub={"@classmethod получает cls"}
      main={"Нужен другой способ создать объект — пишите метод класса «из чего-то»."}
    >
      <PyCode>{`class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    @classmethod
    def from_string(cls, s):
        x, y = s.split(",")
        return cls(int(x), int(y))

p = Point.from_string("3,4")
print(p.x, p.y)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3 4"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Статический метод"}
      sub={"Функция внутри класса ради порядка"}
      main={"Обычный метод знает объект, метод класса — класс, статический — никого."}
    >
      <PyCode>{`class Temp:
    @staticmethod
    def c_to_f(c):
        return c * 9 / 5 + 32

print(Temp.c_to_f(100))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"212.0"}</Cmd>
      <div className="s-cols">
        <Node kind="" mono={true} title={"self"} sub={"Обычный метод"} />
        <Node kind="" mono={true} title={"cls"} sub={"Метод класса"} />
        <Node kind="green" mono={true} title={"—"} sub={"Статический метод"} />
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Подчёркивания в именах"}
      sub={"_x, __x и __x__"}
      main={"Это соглашения, а не замки: они делают код предсказуемым для всех, кто знает язык."}
    >
      <PyCode>{`class A:
    def __init__(self):
        self._internal = 1     # договорённость
        self.__mangled = 2     # искажение имени

a = A()
print(a._internal)
print(a._A__mangled)
print(hasattr(a, "__mangled"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1\n2\nFalse"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Пример: библиотека"}
      sub={"Всё вместе: стр, лен, сравнение, свойство"}
      main={"Код читается как описание предметной области: ничего лишнего."}
    >
      <PyCode>{`class Book:
    def __init__(self, title, year):
        self.title, self.year = title, year
    def __lt__(self, other):
        return self.year < other.year
    def __str__(self):
        return f"{self.title} ({self.year})"

class Library:
    def __init__(self):
        self._books = []
    def add(self, book):
        self._books.append(book)
    def __len__(self):
        return len(self._books)
    @property
    def oldest(self):
        return min(self._books)

lib = Library()
lib.add(Book("Мастер и Маргарита", 1967))
lib.add(Book("Война и мир", 1869))
print(len(lib), lib.oldest)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2 Война и мир (1869)"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"__eq__ без __hash__"}
      main={"Метод оператора возвращает новый объект; внутри сеттера храните значение в _имени."}
    >
      <PyCode>{`class P:
    def __init__(self, x):
        self.x = x
    def __eq__(self, other):
        return self.x == other.x

d = {P(1): "a"}`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"TypeError: unhashable type: 'P'"}</Cmd>
      <div className="s-note">{"Ещё: свойство без сеттера (AttributeError), рекурсия в сеттере, путаница self и cls."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 13 · Классы"}
      main={"Только нужная магия: реализуйте те методы, которые действительно нужны."}
    >
      <div className="s-grid2">
        {[["__add__ · __eq__ · __lt__", "Операторы", "eq — вместе с hash; lt — для сортировки"], ["__len__ · __getitem__", "Контейнер", "len, [], in для своего класса"], ["@property · .setter", "Свойства", "Вычисляемое значение и проверка записи"], ["@classmethod · @staticmethod", "Методы класса", "cls для альтернативных конструкторов"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — наследование и композиция."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P13 = {
  "13:13": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P13).
export const SLIDE_TITLES_P13 = {
  "13:13": [
    "Методы и свойства",
    "Операторы — методы",
    "Равенство и хеш",
    "Порядок и сортировка",
    "Свой контейнер",
    "property",
    "Сеттер",
    "classmethod",
    "staticmethod",
    "Подчёркивания",
    "Пример: библиотека",
    "Типичные ошибки",
    "Итог",
  ],
};
