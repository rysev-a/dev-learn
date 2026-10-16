import { makeSlide } from "../SlideFrame.tsx";
// Слайды для «Python как первый язык», глава 28 — «itertools».
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

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / ФУНКЦИОНАЛЬНОЕ ПРОГРАММИРОВАНИЕ / ГЛАВА 28", 13);

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
      title={"itertools"}
      sub={"Глава 28 · Функциональное программирование"}
      main={"Ленивые потоки: бесконечные счётчики, склейка, группировка и комбинаторика."}
    >
      <div className="s-grid2">
        {[["count · cycle", "Потоки", "Бесконечные источники значений"], ["islice · chain", "Нарезка и склейка", "Срезы и объединения итераторов"], ["accumulate · groupby", "Итоги и группы", "Нарастающие суммы, соседние группы"], ["product · combinations", "Комбинаторика", "Перебор вариантов"]].map(([big, t, d]) => (
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
      title={"Бесконечные потоки"}
      sub={"count, cycle, repeat"}
      main={"Бесконечный поток всегда ограничивайте: islice, takewhile или break."}
    >
      <PyCode>{`from itertools import count, cycle, repeat, islice

print(list(islice(count(10, 5), 4)))
print(list(islice(cycle("ABC"), 7)))
print(list(repeat("x", 3)))
for i, ch in zip(count(1), "abc"):
    print(i, ch)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[10, 15, 20, 25]\n['A', 'B', 'C', 'A', 'B', 'C', 'A']\n['x', 'x', 'x']\n1 a\n2 b\n3 c"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"islice"}
      sub={"Срез для итераторов"}
      main={"Итератор продвигается: взятые и пропущенные элементы израсходованы."}
    >
      <PyCode>{`from itertools import islice

it = iter(range(100))
print(list(islice(it, 3)))
print(list(islice(it, 2, 5)))       # пропустить 2, взять 3
print(list(islice("abcdefgh", 0, None, 3)))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[0, 1, 2]\n[5, 6, 7]\n['a', 'd', 'g']"}</Cmd>
      <div className="s-note">{"Отрицательных индексов нет: итератор не знает своей длины."}</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"chain и zip_longest"}
      sub={"Склеить потоки и выровнять разной длины"}
      main={"zip теряет хвост более длинного; zip_longest хранит всё."}
    >
      <PyCode>{`from itertools import chain, zip_longest

print(list(chain([1, 2], (3,), "ab")))
print(list(chain.from_iterable([[1], [2, 3], []])))
print(list(zip([1, 2, 3], "ab")))
print(list(zip_longest([1, 2, 3], "ab", fillvalue="-")))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[1, 2, 3, 'a', 'b']\n[1, 2, 3]\n[(1, 'a'), (2, 'b')]\n[(1, 'a'), (2, 'b'), (3, '-')]"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"accumulate"}
      sub={"Нарастающие итоги"}
      main={"reduce отдаёт только итог, accumulate — все промежуточные шаги."}
    >
      <PyCode>{`from itertools import accumulate
import operator

nums = [1, 2, 3, 4]
print(list(accumulate(nums)))
print(list(accumulate(nums, operator.mul)))
print(list(accumulate([3, 1, 4, 1, 5], max)))
print(list(accumulate(nums, initial=100)))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[1, 3, 6, 10]\n[1, 2, 6, 24]\n[3, 3, 4, 4, 5]\n[100, 101, 103, 106, 110]"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Отбор в потоках"}
      sub={"takewhile, dropwhile, filterfalse, compress"}
      main={"takewhile останавливается и не читает дальше — для бесконечных потоков это спасение."}
    >
      <PyCode>{`from itertools import takewhile, dropwhile, filterfalse, compress

nums = [1, 3, 5, 6, 7, 9]
print(list(takewhile(lambda x: x % 2 == 1, nums)))
print(list(dropwhile(lambda x: x % 2 == 1, nums)))
print(list(filterfalse(lambda x: x % 2 == 1, nums)))
print(list(compress("ABCDE", [1, 0, 1, 0, 1])))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[1, 3, 5]\n[6, 7, 9]\n[6]\n['A', 'C', 'E']"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"groupby"}
      sub={"Группирует только соседние элементы"}
      main={"Сначала отсортируйте по тому же ключу; группу превращайте в список сразу."}
    >
      <PyCode>{`from itertools import groupby

words = ["аб", "ав", "ба", "бб", "аг"]
for key, group in groupby(words, key=lambda w: w[0]):
    print(key, list(group))
print("— с сортировкой —")
for key, group in groupby(sorted(words), key=lambda w: w[0]):
    print(key, list(group))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"а ['аб', 'ав']\nб ['ба', 'бб']\nа ['аг']\n— с сортировкой —\nа ['аб', 'ав', 'аг']\nб ['ба', 'бб']"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Комбинаторика"}
      sub={"product, permutations, combinations"}
      main={"Результаты ленивые: перебирайте по одному и останавливайтесь, когда нашли нужное."}
    >
      <PyCode>{`from itertools import product, permutations, combinations

print(list(product("ab", [1, 2])))
print(list(permutations([1, 2, 3], 2)))
print(list(combinations("abc", 2)))
print(len(list(permutations(range(5)))), len(list(combinations(range(5), 2))))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[('a', 1), ('a', 2), ('b', 1), ('b', 2)]\n[(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]\n[('a', 'b'), ('a', 'c'), ('b', 'c')]\n120 10"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"starmap, pairwise, tee"}
      sub={"Мелкие, но полезные инструменты"}
      main={"pairwise — готовое скользящее окно из двух; tee копирует итератор, исходный трогать нельзя."}
    >
      <PyCode>{`from itertools import starmap, pairwise, tee
import operator

print(list(starmap(operator.mul, [(2, 3), (4, 5)])))
print(list(pairwise([1, 2, 4, 7])))
a, b = tee(iter([1, 2, 3]))
print(list(a), list(b))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[6, 20]\n[(1, 2), (2, 4), (4, 7)]\n[1, 2, 3] [1, 2, 3]"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Рецепты"}
      sub={"Из примитивов — нужные функции"}
      main={"Многие «хитрые» задачи тривиальны, если знать подходящий кирпичик."}
    >
      <PyCode>{`from itertools import chain, islice

def take(n, it):
    return list(islice(it, n))

def flatten(list_of_lists):
    return list(chain.from_iterable(list_of_lists))

def unique(items):
    seen = {}
    for x in items:
        if x not in seen:
            seen[x] = True
            yield x

print(take(3, iter(range(10))))
print(flatten([[1, 2], [3], []]))
print(list(unique([3, 1, 3, 2, 1])))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[0, 1, 2]\n[1, 2, 3]\n[3, 1, 2]"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Задачи в одну строку"}
      sub={"Пары, нарастающий итог, повторы подряд"}
      main={"Узнавать задачу, за которой стоит один из этих инструментов, — главный навык."}
    >
      <PyCode>{`from itertools import combinations, accumulate, groupby, islice, count

names = ["Аня", "Боря", "Вера"]
print(list(combinations(names, 2)))
print(list(accumulate([1, -2, 3, -4])))
print("".join(k for k, _ in groupby("ааббвввб")))
print(list(islice((n * n for n in count(1)), 4)))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[('Аня', 'Боря'), ('Аня', 'Вера'), ('Боря', 'Вера')]\n[1, -1, 2, -2]\nабвб\n[1, 4, 9, 16]"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"groupby без сортировки и недействительные группы"}
      main={"Ленивые потоки нужно ограничивать и не использовать повторно."}
    >
      <PyCode>{`from itertools import groupby

data = [1, 2, 1, 1]
print([(k, len(list(g))) for k, g in groupby(data)])   # без sorted — дробится
print([(k, list(g)) for k, g in list(groupby([1, 1, 2]))])   # группы недействительны`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[(1, 1), (2, 1), (1, 2)]\n[(1, []), (2, [])]"}</Cmd>
      <div className="s-note">{"Ещё: исчерпанные tee и permutations, размер комбинаторики, путаница permutations и combinations."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 28 · Функциональное программирование"}
      main={"С функциональным программированием закончили — дальше стандартная библиотека."}
    >
      <div className="s-grid2">
        {[["count · islice", "Потоки", "Бесконечные источники и срезы"], ["chain · accumulate", "Склейка и итоги", "Объединить, накопить"], ["groupby", "Группы", "Соседние элементы; сначала sorted"], ["product · combinations", "Комбинаторика", "Ленивый перебор вариантов"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — стандартная библиотека: коллекции, числа, даты, регулярные выражения."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P28 = {
  "13:28": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P28).
export const SLIDE_TITLES_P28 = {
  "13:28": [
    "itertools",
    "Бесконечные потоки",
    "islice",
    "chain и zip_longest",
    "accumulate",
    "Отбор в потоках",
    "groupby",
    "Комбинаторика",
    "starmap, pairwise, tee",
    "Рецепты",
    "Задачи в одну строку",
    "Типичные ошибки",
    "Итог",
  ],
};
