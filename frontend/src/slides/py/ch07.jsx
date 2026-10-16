import { makeSlide } from "../SlideFrame.tsx";
// Слайды для «Python как первый язык», глава 7 — «Списки: перебор и копирование».
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

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / ДАННЫЕ И ЦИКЛЫ / ГЛАВА 7", 13);

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

const Arr = () => <span className="s-arr">→</span>;

// --- сцены ---------------------------------------------------------------

function S01() {
  const topics = [
    ["enumerate · zip", "Перебор", "Номера и параллельный обход двух списков"],
    ["[[ ]]", "Вложенные", "Список списков — таблица, два индекса подряд"],
    ["b = a", "Ссылки", "Присваивание не копирует: список один, имён два"],
    [".copy()", "Копии", "Настоящая копия — и почему она поверхностная"],
  ];
  return (
    <Slide
      n={1}
      title="Списки: перебор и копирование"
      sub="Глава 7 · Данные и циклы"
      main="Самая коварная тема главы — ссылки и копии: на ней спотыкаются даже опытные."
    >
      <div className="s-grid2">
        {topics.map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <p className="s-hint">
        Нужен номер элемента, обход двух колонок сразу, таблица из списков и
        копия, которую можно править без страха.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Перебор с номером"
      sub="enumerate отдаёт пары: номер и элемент"
      main="Один заголовок цикла вместо счётчика, len и индексации."
    >
      <PyCode>{`names = ["Аня", "Борис", "Вера"]
for i, name in enumerate(names, start=1):
    print(i, name)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 Аня\n2 Борис\n3 Вера"}</Cmd>
      <div className="s-note">
        Без start счёт идёт с нуля; start=1 даёт привычную нумерацию с единицы.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Два списка сразу"
      sub="zip смыкает списки зубец за зубцом"
      main="Зип останавливается на самом коротком списке — хвост молча теряется."
    >
      <PyCode>{`names = ["Аня", "Борис"]
scores = [5, 4]
for name, score in zip(names, scores):
    print(name, score)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Аня 5\nБорис 4"}</Cmd>
      <div className="s-note">
        Умеет и три списка, и больше — просто перечисляйте их через запятую.
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Из одного списка — другой"
      sub="Фильтрация и преобразование"
      main="Пустой результат, цикл, условие, аппенд — исходный список остаётся нетронутым."
    >
      <PyCode>{`nums = [1, 2, 3, 4, 5, 6]
result = []
for x in nums:
    if x % 2 == 0:
        result.append(x * x)
print(result)    # [4, 16, 36]`}</PyCode>
      <div className="s-cols">
        <Node mono title="if ..." sub="Фильтрация: отобрать подходящие" />
        <Node kind="green" mono title="append(x * x)" sub="Преобразование: положить новое" />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Аппенд, эктенд, инсёрт"
      sub="Один элемент или много — и куда именно"
      main="Аппенд кладёт коробку целиком, эктенд высыпает содержимое коробки."
    >
      <PyCode>{`a = [1, 2]
a.append([3, 4])    # [1, 2, [3, 4]]
b = [1, 2]
b.extend([3, 4])    # [1, 2, 3, 4]
b.insert(0, 99)     # [99, 1, 2, 3, 4]
print([0] * 3, [1] + [2])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[0, 0, 0] [1, 2]"}</Cmd>
      <div className="s-note">
        Плюс собирает новый список, остальные методы меняют на месте.
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Вложенные списки"
      sub="Список строк, а строка — тоже список"
      main="Клетка таблицы достаётся двумя индексами подряд: строка, потом столбец."
    >
      <PyCode>{`grid = [[1, 2, 3], [4, 5, 6]]
print(grid[1][2])    # 6
grid[0][0] = 99
for row in grid:
    print(row)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"6\n[99, 2, 3]\n[4, 5, 6]"}</Cmd>
      <div className="s-note">
        Перебор таблицы — два вложенных цикла: внешний по строкам, внутренний по
        элементам.
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Ссылки"
      sub="b = a вешает на список вторую табличку"
      main="Список — дом, имя — адрес на конверте: скопировали конверт, дом остался один."
    >
      <PyCode>{`a = [1, 2, 3]
b = a
b.append(4)
print(a)    # [1, 2, 3, 4] — тот же список!`}</PyCode>
      <div className="s-cols">
        <Node mono title="a" sub="имя" />
        <Arr />
        <Node kind="amber" mono title="[1, 2, 3, 4]" sub="один список в памяти" />
        <Arr />
        <Node mono title="b" sub="второе имя" />
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Настоящая копия"
      sub="Срез, метод copy или функция list"
      main="Копия поверхностная: вложенные списки остаются общими."
    >
      <PyCode>{`a = [1, 2, 3]
b = a.copy()      # или a[:] или list(a)
b.append(4)
print(a, b)       # [1, 2, 3] [1, 2, 3, 4]`}</PyCode>
      <div className="s-cols">
        <Node kind="green" mono title="a.copy()" sub="Новый независимый список" />
        <Node kind="amber" mono title="[[1], [2]]" sub="Строки таблицы по-прежнему общие — нужна глубокая копия" />
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Равенство и тождество"
      sub="== сравнивает содержимое, is — объект"
      main="Для «одинаковы ли данные» — всегда двойное равно."
    >
      <PyCode>{`a = [1, 2]
b = a.copy()
c = a
print(a == b)    # True  — содержимое одинаково
print(a is b)    # False — разные объекты
print(a is c)    # True  — один и тот же`}</PyCode>
      <div className="s-note">
        Порядок важен: те же числа в другом порядке — уже неравные списки.
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Не меняйте список в цикле"
      sub="Удаление сдвигает элементы — цикл перепрыгивает"
      main="Собирайте новый список или идите по копии: for x in nums[:]."
    >
      <PyCode>{`nums = [1, -2, -3, 4]
for x in nums:
    if x < 0:
        nums.remove(x)
print(nums)    # [1, -3, 4] — минус три уцелел!`}</PyCode>
      <PyCode>{`result = []
for x in nums:
    if x >= 0:
        result.append(x)    # честный способ`}</PyCode>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Ещё методы"
      sub="index, count, переворот, срезы со сводками"
      main="За каждой строкой в одну команду стоит цикл — просто спрятанный внутри."
    >
      <PyCode>{`nums = [5, 3, 5, 1]
print(nums.index(3))    # 1 — позиция первого вхождения
print(nums.count(5))    # 2 — сколько раз
print(nums[::-1])       # [1, 5, 3, 5] — перевёрнутая копия
print(max(nums[:2]))    # 5 — максимум первых двух`}</PyCode>
      <div className="s-note">
        Нет элемента — index падает с ошибкой: сначала проверьте вхождение словом
        in.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Типичные ловушки"
      sub="Аппенд возвращает ничего; умножение копирует ссылку"
      main="Строки таблицы строят циклом — на каждом витке свежий список."
    >
      <PyCode>{`nums = [3, 1]
nums = nums.append(5)
print(nums)            # None — список затёрт!

grid = [[0] * 3] * 3   # три ссылки на одну строку
grid[0][0] = 7
print(grid)            # [[7, 0, 0], [7, 0, 0], [7, 0, 0]]`}</PyCode>
      <div className="s-note">
        И ещё: пустой список — ошибка для nums[0] и nums.pop(); сначала проверьте
        длину.
      </div>
    </Slide>
  );
}

function S13() {
  const topics = [
    ["enumerate · zip", "Перебор", "Номера с нуля или с start; два списка сразу"],
    ["[[ ]]", "Вложенные", "Таблица: grid[строка][столбец]"],
    ["b = a  ≠  copy", "Ссылки и копии", "Копия — срез, .copy(), list(); поверхностная"],
    ["== · is", "Сравнение", "Содержимое против тождества объектов"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 7 · Данные и циклы"
      main="Не удаляйте элементы из списка, по которому идёте циклом."
    >
      <div className="s-grid2">
        {topics.map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">
        Следующая глава — сортировка и генераторы списков: сжатые записи,
        превращающие десять строк в одну.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P7 = {
  "13:7": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P7).
export const SLIDE_TITLES_P7 = {
  "13:7": [
    "Перебор и копирование",
    "Перебор с номером",
    "Два списка сразу",
    "Из списка — список",
    "Аппенд, эктенд, инсёрт",
    "Вложенные списки",
    "Ссылки",
    "Настоящая копия",
    "== и is",
    "Не менять в цикле",
    "Ещё методы",
    "Типичные ловушки",
    "Итог",
  ],
};
