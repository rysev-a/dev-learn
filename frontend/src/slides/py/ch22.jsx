// Слайды для «Изучаем Python», глава 22 — «functools и operator».
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
      <span>ИЗУЧАЕМ ПИТОН / ФУНКЦИОНАЛЬНОЕ ПРОГРАММИРОВАНИЕ / ГЛАВА 22</span>
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
      title={"functools и operator"}
      sub={"Глава 22 · Функциональное программирование"}
      main={"Многие типичные приёмы уже написаны за нас в стандартной библиотеке."}
    >
      <div className="s-grid2">
        {[["reduce", "Свёртка", "Сложить набор в одно значение"], ["partial", "Фиксация", "Зафиксировать часть аргументов"], ["lru_cache", "Кеш", "Запомнить результаты функции"], ["itemgetter", "operator", "Операторы как функции для key"]].map(([big, t, d]) => (
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
      title={"reduce"}
      sub={"Функция двух аргументов, набор, начальное значение"}
      main={"Начальное значение защищает от пустого набора; для сумм и максимумов берите встроенные."}
    >
      <PyCode>{`from functools import reduce
import operator

print(reduce(operator.mul, [1, 2, 3, 4]))
print(reduce(lambda acc, s: acc + "-" + s, ["а", "б", "в"]))
print(reduce(operator.add, [], 0))
try:
    reduce(operator.add, [])
except TypeError as e:
    print(e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"24\nа-б-в\n0\nreduce() of empty iterable with no initial value"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"partial"}
      sub={"Часть аргументов уже подставлена"}
      main={"Заменяет лямбду, в которой просто подставляются готовые значения."}
    >
      <PyCode>{`from functools import partial

from_bin = partial(int, base=2)
print(from_bin("101"), from_bin("1111"))
power_of_2 = partial(pow, 2)
print(list(map(power_of_2, [1, 2, 3])))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"5 15\n[2, 4, 8]"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"lru_cache"}
      sub={"Повторный вызов с теми же аргументами — из кеша"}
      main={"Аргументы должны быть хешируемыми, а результат — зависеть только от аргументов."}
    >
      <PyCode>{`from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(80))
print(fib.cache_info())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"23416728348467685\nCacheInfo(hits=78, misses=81, maxsize=None, currsize=81)"}</Cmd>
      <div className="s-note">{"Без кеша fib(80) пересчитывалась бы миллиарды лет."}</div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"total_ordering и cached_property"}
      sub={"Меньше методов — тот же результат"}
      main={"__eq__ и один оператор порядка — остальное достроит декоратор."}
    >
      <PyCode>{`from functools import total_ordering, cached_property

@total_ordering
class Version:
    def __init__(self, n):
        self.n = n
    def __eq__(self, other):
        return self.n == other.n
    def __lt__(self, other):
        return self.n < other.n

print(Version(1) < Version(2), Version(3) >= Version(2), Version(2) > Version(5))

class Data:
    @cached_property
    def heavy(self):
        print("считаю")
        return 42

d = Data()
print(d.heavy, d.heavy)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True True False\nсчитаю\n42 42"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"singledispatch"}
      sub={"Перегрузка по типу первого аргумента"}
      main={"Новый тип добавляется регистрацией — без правки исходной функции."}
    >
      <PyCode>{`from functools import singledispatch

@singledispatch
def show(x):
    return f"что-то: {x}"

@show.register(int)
def _(x):
    return f"число {x}"

@show.register(list)
def _(x):
    return f"список из {len(x)}"

print(show(5), show([1, 2]), show("a"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"число 5 список из 2 что-то: a"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"operator: операторы как функции"}
      sub={"add, mul, lt, pow"}
      main={"Вместо лямбды с одним оператором — готовая и более быстрая функция."}
    >
      <PyCode>{`import operator
from functools import reduce

print(operator.add(2, 3), operator.mul(4, 5), operator.lt(1, 2))
print(list(map(operator.pow, [2, 3], [3, 2])))
print(reduce(operator.mul, range(1, 6)))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"5 20 True\n[8, 9]\n120"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"itemgetter, attrgetter, methodcaller"}
      sub={"Лучшие параметры для key"}
      main={"Несколько ключей в itemgetter — сортировка по нескольким полям в одну строку."}
    >
      <PyCode>{`from operator import itemgetter, attrgetter, methodcaller

users = [{"name": "Аня", "age": 31}, {"name": "Боря", "age": 25}]
print(sorted(users, key=itemgetter("age"))[0]["name"])
rows = [("б", 2), ("а", 2), ("в", 1)]
print(sorted(rows, key=itemgetter(1, 0)))

class P:
    def __init__(self, year):
        self.year = year

print([p.year for p in sorted([P(2000), P(1990)], key=attrgetter("year"))])
print(list(map(methodcaller("upper"), ["а", "б"])))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Боря\n[('в', 1), ('а', 2), ('б', 2)]\n[1990, 2000]\n['А', 'Б']"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"cmp_to_key"}
      sub={"Старая схема сравнения двух элементов"}
      main={"Нужно сортировать «чужим» способом — переходник превращает сравнение в ключ."}
    >
      <PyCode>{`from functools import cmp_to_key

def compare(a, b):
    return len(a) - len(b) or (a > b) - (a < b)

print(sorted(["bb", "a", "cc", "b"], key=cmp_to_key(compare)))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['a', 'b', 'bb', 'cc']"}</Cmd>
      <div className="s-note">{"Функция сравнения возвращает отрицательное число, ноль или положительное."}</div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Конвейер без лямбд"}
      sub={"Отобрать, упорядочить, свернуть"}
      main={"Пользуйтесь инструментом, который делает текст короче без потери ясности."}
    >
      <PyCode>{`from operator import itemgetter

sales = [{"dept": "ИТ", "sum": 120}, {"dept": "HR", "sum": 70},
         {"dept": "ИТ", "sum": 30}, {"dept": "HR", "sum": 200}]
big = filter(lambda s: s["sum"] >= 50, sales)
ordered = sorted(big, key=itemgetter("dept", "sum"))
print([(s["dept"], s["sum"]) for s in ordered])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[('HR', 70), ('HR', 200), ('ИТ', 120)]"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Сочетания инструментов"}
      sub={"Маленькие кирпичики складываются"}
      main={"Сначала смотрите, нет ли нужного в стандартной библиотеке, потом пишите своё."}
    >
      <PyCode>{`from functools import partial, reduce
import operator

print(list(map(partial(int, base=16), ["ff", "10", "a"])))
print(reduce(operator.or_, [1, 2, 4]))
print(list(map(operator.methodcaller("strip"), [" а ", "б "])))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[255, 16, 10]\n7\n['а', 'б']"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"reduce без начального значения, кеш для списков"}
      main={"Спросите себя: что станет с функцией при повторном вызове?"}
    >
      <PyCode>{`from functools import lru_cache, reduce

try:
    reduce(lambda a, b: a + b, [])
except TypeError:
    print("reduce без начального значения")

@lru_cache
def total(xs):
    return sum(xs)

try:
    total([1, 2])
except TypeError as e:
    print(e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"reduce без начального значения\nunhashable type: 'list'"}</Cmd>
      <div className="s-note">{"Ещё: кеш функции с побочными эффектами; кеш без maxsize на бесконечных данных; itemgetter с несколькими ключами возвращает кортеж."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 22 · Функциональное программирование"}
      main={"Готовые инструменты экономят часы: reduce, partial, lru_cache, itemgetter."}
    >
      <div className="s-grid2">
        {[["reduce · partial", "Функции", "Свёртка и фиксация аргументов"], ["lru_cache · cached_property", "Кеш", "Запомнить результат; хешируемые аргументы"], ["total_ordering · singledispatch", "Классы и типы", "Меньше методов; реализация по типу"], ["itemgetter · attrgetter", "operator", "Лучшие ключи для sorted и max"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — itertools: потоки значений."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P22 = {
  "13:22": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P22).
export const SLIDE_TITLES_P22 = {
  "13:22": [
    "functools и operator",
    "reduce",
    "partial",
    "lru_cache",
    "total_ordering",
    "singledispatch",
    "operator",
    "itemgetter и друзья",
    "cmp_to_key",
    "Конвейер без лямбд",
    "Сочетания",
    "Типичные ошибки",
    "Итог",
  ],
};
