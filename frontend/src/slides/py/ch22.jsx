import { makeSlide } from "../SlideFrame.tsx";
// Слайды для «Python как первый язык», глава 22 — «Итераторы».
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

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / ИТЕРАТОРЫ И ГЕНЕРАТОРЫ / ГЛАВА 22", 13);

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
      title={"Итераторы"}
      sub={"Глава 22 · Итераторы и генераторы"}
      main={"Один протокол стоит за циклом for, list, sum, zip — и за вашими собственными классами."}
    >
      <div className="s-grid2">
        {[["iter · next", "Протокол", "Итерируемый отдаёт итератор, итератор — значения"], ["StopIteration", "Конец", "Сигнал «элементы закончились»"], ["__iter__ · __next__", "Свой итератор", "Класс с двумя методами"], ["lazy", "Лень", "Значения рождаются по требованию"]].map(([big, t, d]) => (
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
      title={"Итерируемый и итератор"}
      sub={"iter() отдаёт итератор, next() — следующее значение"}
      main={"Список — итерируемый, но не итератор: next(список) — ошибка."}
    >
      <PyCode>{`nums = [10, 20]
it = iter(nums)
print(next(it), next(it))
try:
    next(it)
except StopIteration:
    print("конец")
try:
    next(nums)
except TypeError as e:
    print(e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"10 20\nконец\n'list' object is not an iterator"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Как работает for"}
      sub={"iter, затем next до StopIteration"}
      main={"Любой for можно переписать через while True, try и except StopIteration."}
    >
      <PyCode>{`nums = [1, 2, 3]
it = iter(nums)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
    print(x)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1\n2\n3"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Одноразовость"}
      sub={"Итератор идёт только вперёд"}
      main={"Файл, zip, enumerate, map и filter — итераторы; range — итерируемый, он многоразовый."}
    >
      <PyCode>{`it = iter([1, 2, 3])
print(list(it))
print(list(it))        # исчерпан
r = range(3)
print(list(r), list(r))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[1, 2, 3]\n[]\n[0, 1, 2] [0, 1, 2]"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Свой итератор"}
      sub={"__iter__ возвращает self, __next__ — значение"}
      main={"Аккуратно подними StopIteration в нужный момент — иначе цикл не завершится."}
    >
      <PyCode>{`class Countdown:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        return self
    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

print(list(Countdown(3)))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[3, 2, 1]"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Многоразовый итерируемый"}
      sub={"__iter__ каждый раз создаёт новый итератор"}
      main={"Коллекции — итерируемые, итераторы создаются по требованию."}
    >
      <PyCode>{`class Repeat:
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        return iter(range(self.n))      # каждый раз новый

r = Repeat(3)
print(list(r), list(r))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[0, 1, 2] [0, 1, 2]"}</Cmd>
      <div className="s-note">{"Если __iter__ вернёт self — класс станет одноразовым."}</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Помощники"}
      sub={"enumerate, zip, reversed, next со значением"}
      main={"Что понимает одна функция-потребитель, понимают все: list, tuple, sum, max, join, in."}
    >
      <PyCode>{`words = ["a", "b", "c"]
print(list(enumerate(words, 1)))
print(list(zip(words, [1, 2, 3])))
print(list(reversed(words)))
print(next(iter(()), "пусто"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[(1, 'a'), (2, 'b'), (3, 'c')]\n[('a', 1), ('b', 2), ('c', 3)]\n['c', 'b', 'a']\nпусто"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Распаковка и потребители"}
      sub={"Звёздочка, sum, max, next с запасным значением"}
      main={"next(поток, значение) безопасно берёт один элемент — удобно для поиска первого подходящего."}
    >
      <PyCode>{`a, *rest = iter([1, 2, 3, 4])
print(a, rest)
print(*[1, 2, 3])
print(sum(x for x in range(5)), max(iter([3, 9, 2])))
gen = (n for n in [5, 8, 12] if n > 6)
print(next(gen), next(gen, None), next(gen, None))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 [2, 3, 4]\n1 2 3\n10 9\n8 12 None"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Ленивость"}
      sub={"Значения рождаются по требованию"}
      main={"Вместо «посчитать всё, потом отобрать» — «описать конвейер и тянуть по одному»."}
    >
      <PyCode>{`big = range(10**12)
print(len(big), big[-1])
nums = map(str, range(3))
print(type(nums).__name__)     # ничего не посчитано
print(list(nums))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1000000000000 999999999999\nmap\n['0', '1', '2']"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Бесконечные итераторы"}
      sub={"Числа Фибоначчи без конца"}
      main={"Бесконечный поток всегда ограничивайте: брейк, счётчик или условие."}
    >
      <PyCode>{`class Fib:
    def __init__(self):
        self.a, self.b = 0, 1
    def __iter__(self):
        return self
    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        return self.a

for i, x in enumerate(Fib()):
    if i == 8:
        break
    print(x, end=" ")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 1 2 3 5 8 13 21"}</Cmd>
      <div className="s-note">{"list(Fib()) никогда не вернётся и съест всю память."}</div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Словари и итерация"}
      sub={"Представления keys, values, items"}
      main={"Размер словаря во время перебора менять нельзя: итератор потеряет согласованность."}
    >
      <PyCode>{`d = {"a": 1, "b": 2}
for k in d:
    print(k, end=" ")
print(list(d.items()))
print(list(reversed(d)))
try:
    for k in d:
        d["c"] = 3
except RuntimeError as e:
    print(e)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"a b [('a', 1), ('b', 2)]\n['b', 'a']\ndictionary changed size during iteration"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Исчерпанный итератор"}
      main={"Итератор — одноразовый курсор, итерируемый — источник свежих курсоров."}
    >
      <PyCode>{`f = open("demo.txt", "w", encoding="utf-8")
f.write("1\\n2\\n")
f.close()

f = open("demo.txt", encoding="utf-8")
print(list(f))
print(list(f))        # файл — итератор: второй проход пуст
f.close()`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['1\\n', '2\\n']\n[]"}</Cmd>
      <div className="s-note">{"Ещё: next(список), итерируемый класс с return self, нет StopIteration, list(бесконечный)."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 22 · Итераторы и генераторы"}
      main={"Итератор — одноразовый курсор; итерируемый — источник свежих курсоров."}
    >
      <div className="s-grid2">
        {[["iter · next", "Протокол", "for = iter + повторяющийся next"], ["StopIteration", "Конец", "Сигнал, что элементы закончились"], ["__iter__ · __next__", "Свой класс", "Многоразовый — iter создаёт новый итератор"], ["lazy", "Лень", "Память — на один элемент; бесконечное — ограничивать"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — генераторы: самый короткий способ писать итераторы."}</div>
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
    "Итераторы",
    "Итерируемый и итератор",
    "Как работает for",
    "Одноразовость",
    "Свой итератор",
    "Многоразовый класс",
    "Помощники",
    "Распаковка",
    "Ленивость",
    "Бесконечные итераторы",
    "Словари",
    "Типичные ошибки",
    "Итог",
  ],
};
