// Слайды для «Изучаем Python», глава 16 — «Файлы».
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
      <span>ИЗУЧАЕМ ПИТОН / ИСКЛЮЧЕНИЯ И ФАЙЛЫ / ГЛАВА 16</span>
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
      title={"Файлы"}
      sub={"Глава 16 · Исключения и файлы"}
      main={"Файлы дают программе память: сохранить, прочитать, обработать данные «со стороны»."}
    >
      <div className="s-grid2">
        {[["open()", "Открыть", "Путь и режим: r, w, a, x, b"], ["with", "Закрыть само", "Контекстный менеджер"], ["for line in f", "Построчно", "Большие файлы — без памяти"], ["encoding", "Кодировка", "Всегда явно: utf-8"]].map(([big, t, d]) => (
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
      title={"open и режимы"}
      sub={"Файл открывают — и закрывают"}
      main={"Для текста всегда указывайте encoding; открытый файл обязан быть закрыт."}
    >
      <PyCode>{`f = open("demo.txt", "w", encoding="utf-8")
f.write("привет\\n")
f.close()
print(open("demo.txt", encoding="utf-8").read())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"привет"}</Cmd>
      <div className="s-cols">
        <Node kind="" mono={true} title={"r"} sub={"Чтение (по умолчанию)"} />
        <Node kind="amber" mono={true} title={"w"} sub={"Запись: затирает файл!"} />
        <Node kind="" mono={true} title={"a"} sub={"Дописывание в конец"} />
        <Node kind="" mono={true} title={"x"} sub={"Создание: падает, если файл есть"} />
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Конструкция with"}
      sub={"Закрывается само — даже при ошибке"}
      main={"Забыть закрыть файл при with невозможно."}
    >
      <PyCode>{`with open("demo.txt", "w", encoding="utf-8") as f:
    f.write("привет\\nмир\\n")

with open("demo.txt", encoding="utf-8") as f:
    text = f.read()
print(text)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"привет\nмир"}</Cmd>
      <div className="s-note">{"read() тянет весь файл в память — для маленьких файлов."}</div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Построчное чтение"}
      sub={"Файл сам перебирается циклом for"}
      main={"В памяти лежит одна строка: так читают файлы любого размера."}
    >
      <PyCode>{`with open("demo.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip().upper())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"ПРИВЕТ\nМИР"}</Cmd>
      <div className="s-note">{"Каждая строка кончается \\n — обычно его убирают методом strip()."}</div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Запись"}
      sub={"write не добавляет перевод строки"}
      main={"Писать можно только строки: число сначала превращают через str."}
    >
      <PyCode>{`with open("log.txt", "w", encoding="utf-8") as f:
    f.write("первая")            # без \\n — склеится
    f.write("вторая\\n")
    print("третья", file=f)      # print сам добавит \\n

with open("log.txt", "a", encoding="utf-8") as f:
    f.write(str(42) + "\\n")

print(open("log.txt", encoding="utf-8").read())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"перваявторая\nтретья\n42"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Кодировки и байты"}
      sub={"Текст в файле — это байты"}
      main={"В двоичном режиме работают с bytes: картинки, архивы, любые не текстовые данные."}
    >
      <PyCode>{`data = "привет".encode("utf-8")
print(data)
print(len("привет"), len(data))
print(data.decode("utf-8"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"b'\\xd0\\xbf\\xd1\\x80\\xd0\\xb8\\xd0\\xb2\\xd0\\xb5\\xd1\\x82'\n6 12\nпривет"}</Cmd>
      <div className="s-note">{"Открыли UTF-8 как другую кодировку — UnicodeDecodeError или «кракозябры»."}</div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Позиция в файле"}
      sub={"tell и seek, чтение порциями"}
      main={"Прочитали до конца — повторный read() вернёт пустую строку: нужна перемотка."}
    >
      <PyCode>{`with open("demo.txt", encoding="utf-8") as f:
    print(f.read(3))
    print(f.tell())
    f.seek(0)
    print(f.readline().strip())
    print(f.read().strip())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"при\n6\nпривет\nмир"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Как устроен with"}
      sub={"__enter__ при входе, __exit__ при выходе"}
      main={"with гарантирует уборку: свой менеджер — класс с двумя методами."}
    >
      <PyCode>{`class Timer:
    def __enter__(self):
        self.items = 0
        return self
    def __exit__(self, exc_type, exc, tb):
        print("выход:", exc_type.__name__ if exc_type else "без ошибок")

with Timer() as t:
    t.items = 5
print(t.items)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"выход: без ошибок\n5"}</Cmd>
      <div className="s-note">{"Короче — декоратор contextmanager из contextlib (после генераторов)."}</div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Ошибки файлов"}
      sub={"Потомки OSError"}
      main={"try — вокруг open: открыть и поймать надёжнее, чем проверить заранее."}
    >
      <PyCode>{`try:
    with open("нет_такого.txt", encoding="utf-8") as f:
        data = f.read()
except FileNotFoundError:
    print("файл не найден")
except PermissionError:
    print("нет прав")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"файл не найден"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Типовые задачи"}
      sub={"Открыли, перебрали строки, закрылось само"}
      main={"Циклы, строки, словари, исключения и файлы работают как единый механизм."}
    >
      <PyCode>{`counts = {}
with open("demo.txt", encoding="utf-8") as f:
    for line in f:
        for word in line.split():
            counts[word] = counts.get(word, 0) + 1
print(counts)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'привет': 1, 'мир': 1}"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Временные файлы"}
      sub={"Модуль tempfile"}
      main={"Безопасно: нет риска затереть чужое; идеально для тестов."}
    >
      <PyCode>{`import os
import tempfile

with tempfile.TemporaryDirectory() as folder:
    path = os.path.join(folder, "data.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write("временные данные")
    print(os.path.exists(path))
print(os.path.exists(path))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True\nFalse"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Типичные ошибки"}
      sub={"Режим w затирает сразу"}
      main={"Две привычки решают почти всё: with и явная кодировка."}
    >
      <PyCode>{`with open("demo.txt", "w", encoding="utf-8") as f:
    pass                      # затёрли файл!

with open("demo.txt", encoding="utf-8") as f:
    print(repr(f.read()))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"''"}</Cmd>
      <div className="s-note">{"Ещё: относительный путь считается от папки запуска; число вместо строки в write; read() на огромном файле."}</div>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итог"}
      sub={"Глава 16 · Исключения и файлы"}
      main={"with + encoding='utf-8' — две привычки на всю жизнь."}
    >
      <div className="s-grid2">
        {[["open · r w a x b", "Открытие", "Режимы; w затирает, a дописывает"], ["with · for line in f", "Чтение", "Закрывается само; большие файлы — построчно"], ["write · print(file=f)", "Запись", "Нет \\n сам по себе; только строки"], ["OSError", "Ошибки", "FileNotFoundError, PermissionError — вокруг open"]].map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
      <div className="s-note">{"Дальше — пути и форматы: pathlib, json и csv."}</div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P16 = {
  "13:16": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P16).
export const SLIDE_TITLES_P16 = {
  "13:16": [
    "Файлы",
    "open и режимы",
    "Конструкция with",
    "Построчно",
    "Запись",
    "Кодировки и байты",
    "Позиция в файле",
    "Как устроен with",
    "Ошибки файлов",
    "Типовые задачи",
    "Временные файлы",
    "Типичные ошибки",
    "Итог",
  ],
};
