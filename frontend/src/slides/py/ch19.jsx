// Слайды для «Изучаем Python», глава 19 — «Генераторы».
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
      <span>ИЗУЧАЕМ ПИТОН / ИТЕРАТОРЫ И ГЕНЕРАТОРЫ / ГЛАВА 19</span>
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
      title={"Генераторы"}
      sub={"Глава 19 · Итераторы и генераторы"}
      main={"Слово yield превращает функцию в итератор — без класса и без StopIteration."}
    >
      <div className="s-grid2">
        {[["yield", "Генератор", "Функция, которая отдаёт значения порциями"], ["( x for ... )", "Выражение", "Ленивый брат генератора списка"], ["a | b | c", "Конвейер", "Генераторы друг в друга"], ["yield from", "Делегирование", "Отдать всё из вложенного источника"]].map(([big, t, d]) => (
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
      title={"Функция с yield"}
      sub={"Вызов создаёт генератор и ничего не выполняет"}
      main={"return отдаёт и завершает; yield отдаёт и приостанавливает, помня всё состояние."}
    >
      <PyCode>{`def countdown(n):
    while n > 0:
        yield n
        n -= 1

g = countdown(3)
print(type(g).__name__)
print(next(g), next(g), next(g))
print(list(countdown(2)))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"generator\n3 2 1\n[2, 1]"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Порядок выполнения"}
      sub={"Код внутри идёт ровно настолько, насколько просят значений"}
      main={"Перемежающееся выполнение двух программ — вызывающей и генератора — суть генераторов."}
    >
      <PyCode>{`def gen():
    print("старт")
    yield 1
    print("середина")
    yield 2
    print("конец")

g = gen()
print("создали")
print(next(g))
print(next(g))
try:
    next(g)
except StopIteration:
    print("StopIteration")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"создали\nстарт\n1\nсередина\n2\nконец\nStopIteration"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Генератор — это итератор"}
      sub={"Всё из прошлой главы работает"}
      main={"Нужно перебрать дважды — вызовите генераторную функцию заново: каждый вызов — новый курсор."}
    >
      <PyCode>{`def squares(n):
    for i in range(n):
        yield i * i

g = squares(4)
print(list(g))
print(list(g))
print(sum(squares(4)), 9 in squares(4))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[0, 1, 4, 9]\n[]\n14 True"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Бесконечные генераторы"}
      sub={"Вечный цикл и yield"}
      main={"Ни класса, ни хранения последовательности: значения рождаются и забываются."}
    >
      <PyCode>{`def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

for i, x in enumerate(fib()):
    if i == 10:
        break
    print(x, end=" ")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0 1 1 2 3 5 8 13 21 34"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Генераторное выражение"}
      sub={"Круглые скобки вместо квадратных"}
      main={"Нужно один раз свернуть в число — выражение; нужен список для повторного обхода — генератор списка."}
    >
      <PyCode>{`s = sum(x * x for x in range(1_000_000))
print(s)
gen = (x * x for x in range(3))
print(type(gen).__name__, list(gen))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"333332833333500000\ngenerator [0, 1, 4]"}</Cmd>
      <div className="s-note">{"Миллион квадратов посчитан без списка в памяти."}</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Конвейеры"}
      sub={"Каждый этап — маленькая функция"}
      main={"Через цепочку течёт по одному элементу: файл на сто гигабайт обрабатывается так же, как на сто килобайт."}
    >
      <PyCode>{`def lines():
    for t in ["  Привет ", "", "МИР  ", "  ", "Да"]:
        yield t

def non_empty(src):
    for s in src:
        if s.strip():
            yield s

def cleaned(src):
    for s in src:
        yield s.strip().lower()

print(list(cleaned(non_empty(lines()))))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['привет', 'мир', 'да']"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"yield from"}
      sub={"Отдать всё из вложенного источника"}
      main={"Рекурсивный обход вложенных структур — в пять строк."}
    >
      <PyCode>{`def flat(items):
    for x in items:
        if isinstance(x, list):
            yield from flat(x)
        else:
            yield x

print(list(flat([1, [2, [3, 4]], 5])))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[1, 2, 3, 4, 5]"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"send: значения внутрь"}
      sub={"yield — ещё и выражение"}
      main={"Основа корутин и асинхронного программирования: функция приостанавливается и уступает."}
    >
      <PyCode>{`def averager():
    total, n = 0, 0
    avg = None
    while True:
        x = yield avg
        total += x
        n += 1
        avg = total / n

g = averager()
next(g)               # дошли до первого yield
print(g.send(10), g.send(20), g.send(30))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"10.0 15.0 20.0"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Менеджеры контекста"}
      sub={"@contextmanager и один yield"}
      main={"До yield — вход в with, после — выход; try/finally гарантирует уборку при ошибке."}
    >
      <PyCode>{`from contextlib import contextmanager

@contextmanager
def tag(name):
    print(f"<{name}>")
    try:
        yield
    finally:
        print(f"</{name}>")

with tag("p"):
    print("текст")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"<p>\nтекст\n</p>"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Типовые приёмы"}
      sub={"Пачки, скользящие пары, страницы"}
      main={"Потребитель не знает, как устроен источник, а источник — зачем нужны значения."}
    >
      <PyCode>{`def chunks(items, n):
    for i in range(0, len(items), n):
        yield items[i:i + n]

def pairs(items):
    return zip(items, items[1:])

print(list(chunks([1, 2, 3, 4, 5], 2)))
print(list(pairs([1, 2, 3, 4])))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[[1, 2], [3, 4], [5]]\n[(1, 2), (2, 3), (3, 4)]"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Генератор ничего не делает, пока не попросят"}
      main={"Главный критерий — понятность: сложное выражение перепишите функцией с yield."}
    >
      <PyCode>{`def gen():
    print("не напечатается без next")
    yield 1

g = gen()               # ничего не выполнено
print("создан")
print(list(g), list(g))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"создан\nне напечатается без next\n[1] []"}</Cmd>
      <div className="s-note">{"Ещё: повторный проход по генератору, бесконечный без ограничения, return со значением внутри генератора."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 19 · Итераторы и генераторы"}
      main={"Генераторы — самый короткий способ писать итераторы и ленивые конвейеры."}
    >
      <div className="s-grid2">
        {[["yield", "Генераторная функция", "Лениво и по порядку; одноразовая"], ["(x for ...)", "Выражение", "Свернуть без списка в памяти"], ["yield from", "Делегирование", "Рекурсивные обходы"], ["@contextmanager", "with на генераторе", "До yield — вход, после — выход"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — функциональное программирование: функции как значения, lambda, замыкания и декораторы."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P19 = {
  "13:19": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P19).
export const SLIDE_TITLES_P19 = {
  "13:19": [
    "Генераторы",
    "Функция с yield",
    "Порядок выполнения",
    "Генератор — итератор",
    "Бесконечные генераторы",
    "Генераторное выражение",
    "Конвейеры",
    "yield from",
    "send",
    "contextmanager",
    "Типовые приёмы",
    "Типичные ошибки",
    "Итог",
  ],
};
