import { makeSlide } from "../SlideFrame.jsx";
// Слайды для «Python как первый язык», глава 9 — «Словари».
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

const Slide = makeSlide("PYTHON КАК ПЕРВЫЙ ЯЗЫК / СЛОВАРИ И КОРТЕЖИ / ГЛАВА 9", 13);

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
      title={"Словари"}
      sub={"Глава 9 · Словари и кортежи"}
      main={"Словарь ищет по осмысленному имени-ключу, а не по номеру — и делает это мгновенно."}
    >
      <div className="s-grid2">
        {[["{k: v}", "Словарь", "Пары «ключ — значение» в фигурных скобках"], ["d[key]", "Доступ", "По ключу, а не по номеру"], [".get()", "Мягко", "Значение по умолчанию вместо ошибки"], [".items()", "Перебор", "Пары целиком: ключ и значение"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <p className="s-hint">{"Телефон по имени, цена по названию, настройка по слову — так мы ищем в жизни."}</p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Создание словаря"}
      sub={"Пары через запятую, ключ и значение через двоеточие"}
      main={"Ключи уникальны, значения — любые: числа, строки, списки, даже словари."}
    >
      <PyCode>{`prices = {"яблоко": 50, "банан": 70}
empty = {}
print(prices)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'яблоко': 50, 'банан': 70}"}</Cmd>
      <div className="s-cols">
        <Node kind="" mono={true} title={"\"яблоко\""} sub={"Ключ — по нему ищем"} />
        <Node kind="green" mono={true} title={"50"} sub={"Значение — то, что нашли"} />
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Доступ по ключу"}
      sub={"В квадратных скобках — ключ, а не номер"}
      main={"Ключ обязан существовать: иначе Питон остановит программу ошибкой ключа."}
    >
      <PyCode>{`prices = {"яблоко": 50, "банан": 70}
print(prices["яблоко"])   # 50
print(prices["киви"])     # ошибка!`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"50\nKeyError: 'киви'"}</Cmd>
      <div className="s-note">{"Код читается сам: prices[\"яблоко\"], а не prices[0]."}</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Метод get"}
      sub={"Вежливый доступ: без ошибки, с запасным значением"}
      main={"Скобки — когда ключ обязан быть. get — когда его отсутствие обычное дело."}
    >
      <PyCode>{`prices = {"яблоко": 50}
print(prices.get("киви"))       # None
print(prices.get("киви", 0))    # 0 — по умолчанию`}</PyCode>
      <div className="s-cols">
        <Node kind="" mono={true} title={"d[key]"} sub={"Нет ключа — ошибка: громкий баг"} />
        <Node kind="green" mono={true} title={"d.get(key, 0)"} sub={"Нет ключа — запасное значение"} />
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Добавить и изменить"}
      sub={"Присваивание по ключу делает и то и другое"}
      main={"Нет ключа — пара добавится, есть — значение заменится. Словарь помнит порядок вставки."}
    >
      <PyCode>{`prices = {"яблоко": 50, "банан": 70}
prices["киви"] = 90      # новая пара
prices["яблоко"] = 55    # замена
print(prices)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'яблоко': 55, 'банан': 70, 'киви': 90}"}</Cmd>
      <div className="s-note">{"Индексов нет: вопрос не «что третье», а «что лежит под этим именем»."}</div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Проверка ключа: in"}
      sub={"Слово in смотрит ключи, а не значения"}
      main={"Поиск по ключу мгновенный — хоть десять пар, хоть десять миллионов."}
    >
      <PyCode>{`prices = {"яблоко": 50, "банан": 70}
print("яблоко" in prices)       # True
print(50 in prices)             # False — это значение
print(50 in prices.values())    # True`}</PyCode>
      <div className="s-note">{"Почему так быстро — разбирали в курсе алгоритмов: хеш-таблицы."}</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Удаление"}
      sub={"del и pop — по ключу, len считает пары"}
      main={"У списка remove ищет значение, у словаря всё делается по ключу."}
    >
      <PyCode>{`prices = {"яблоко": 50, "банан": 70, "киви": 90}
del prices["киви"]
print(prices.pop("банан"))   # 70
print(prices, len(prices))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"70\n{'яблоко': 50} 1"}</Cmd>
      <div className="s-note">{"pop(key, 0) не упадёт, если ключа нет; clear() очищает всё."}</div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Перебор словаря"}
      sub={"Ключи, значения или пары целиком"}
      main={"Лучший способ — items(): два имени в заголовке цикла, пара раскладывается сама."}
    >
      <PyCode>{`prices = {"яблоко": 50, "банан": 70}
for name, price in prices.items():
    print(name, price)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"яблоко 50\nбанан 70"}</Cmd>
      <div className="s-cols">
        <Node kind="" mono={true} title={"for k in d"} sub={"Ключи"} />
        <Node kind="" mono={true} title={".values()"} sub={"Значения"} />
        <Node kind="green" mono={true} title={".items()"} sub={"Пары"} />
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Подсчёт частот"}
      sub={"Классика обработки данных"}
      main={"Шаблон «get с нулём плюс один» заменяет отдельный счётчик на каждое слово."}
    >
      <PyCode>{`words = ["да", "нет", "да"]
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
print(counts)    # {'да': 2, 'нет': 1}`}</PyCode>
      <div className="s-note">{"Первое «да»: get вернул 0, прибавили 1. Второе: взяли 1, прибавили ещё 1."}</div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Какие бывают ключи"}
      sub={"Неизменяемые: числа, строки, кортежи"}
      main={"Ключи сравниваются точно: «Яблоко» и «яблоко» — две разные пары."}
    >
      <PyCode>{`d = {}
d[(1, 2)] = "клетка"    # кортеж — можно
d[[1, 2]] = "ошибка"   # TypeError: unhashable`}</PyCode>
      <div className="s-cols">
        <Node kind="green" mono={true} title={"str  int  tuple"} sub={"Годятся в ключи"} />
        <Node kind="amber" mono={true} title={"list  dict"} sub={"Изменяемые — нельзя"} />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Ссылки и копии"}
      sub={"Те же правила, что у списков"}
      main={"b = a — одно имя на двоих; настоящая копия — .copy() или dict(a), и она поверхностная."}
    >
      <PyCode>{`a = {"x": 1}
b = a             # тот же словарь
c = a.copy()      # настоящая копия
b["x"] = 99
print(a, c)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'x': 99} {'x': 1}"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Ключ, который не нашёлся, и размер при переборе"}
      main={"Читаете ненадёжный ключ — берите get. Перебираете словарь — не меняйте его размер."}
    >
      <PyCode>{`prices = {"яблоко": 50}
print(prices["киви"])        # KeyError — берите get
for k in prices:
    prices["новый"] = 1       # RuntimeError: размер изменился`}</PyCode>
      <div className="s-note">{"Ещё: in смотрит ключи; регистр и пробелы важны; индексов у словаря нет."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 9 · Словари и кортежи"}
      main={"Словарь — пары «ключ — значение»: читаем, меняем и удаляем по ключу."}
    >
      <div className="s-grid2">
        {[["{k: v}", "Словарь", "Фигурные скобки; ключи уникальны и неизменяемы"], ["d[k] · .get", "Чтение", "Скобки — строго, get — мягко"], ["in · del · pop", "Ключи", "in проверяет ключи, del и pop удаляют пару"], [".items()", "Перебор", "Пары; get(w, 0) + 1 — частоты"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — приёмы со словарями: слияние, генераторы, вложенные данные, группировка, сортировка."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P9 = {
  "13:9": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P9).
export const SLIDE_TITLES_P9 = {
  "13:9": [
    "Словари",
    "Создание словаря",
    "Доступ по ключу",
    "Метод get",
    "Добавить и изменить",
    "Проверка ключа: in",
    "Удаление",
    "Перебор словаря",
    "Подсчёт частот",
    "Какие бывают ключи",
    "Ссылки и копии",
    "Типичные ошибки",
    "Итог",
  ],
};
