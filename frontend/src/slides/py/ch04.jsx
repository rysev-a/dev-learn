// Слайды для «Изучаем Python», глава 4 — «Циклы».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

const PY_KW = new Set([
  "print", "def", "if", "elif", "else", "for", "while", "in", "not", "and",
  "or", "return", "import", "from", "True", "False", "None", "class", "with",
  "break", "continue",
]);

// Крошечный токенизатор Питона: комментарии, строки, числа, ключевые слова,
// вызовы функций. Достаточно для слайдов.
function pySpan(src) {
  const out = [];
  const re =
    /(#[^\n]*)|("(?:[^"\\]|\\.)*")|('(?:[^'\\]|\\.)*')|(\b\d[\d_]*(?:\.\d+)?\b)|([A-Za-z_][A-Za-z0-9_]*)|(\s+|.)/g;
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
      <span>ИЗУЧАЕМ ПИТОН / ДАННЫЕ И ЦИКЛЫ / ГЛАВА 4</span>
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

const Arr = () => <span className="s-arr">→</span>;

// --- сцены ---------------------------------------------------------------

function S01() {
  const topics = [
    ["while", "Вайл", "Пока условие истинно — тело повторяется"],
    ["for", "Фор", "Для каждого элемента из…"],
    ["range", "Рэндж", "Числовые серии: ноль, один, два…"],
    ["break · continue", "Выход и пропуск", "Брейк закрывает цикл, континуе — виток"],
  ];
  return (
    <Slide
      n={1}
      title="Циклы"
      sub="Глава 4 · Данные и циклы"
      main="Действие пишется один раз — выполняется столько, сколько нужно."
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
        Условия дали программе развилки, но каждое действие пока выполняется
        один раз. Цикл убирает это ограничение: обработать тысячу писем одним
        куском кода — реальная задача, а не подвиг.
      </p>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title="Цикл вайл"
      sub="Читается как «пока»"
      main="Пока условие истинно, тело цикла повторяется снова и снова."
    >
      <PyCode>{`n = 3
while n > 0:
    print(n)
    n = n - 1`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3\n2\n1"}</Cmd>
      <div className="s-note">
        Отступы те же, что в условиях: тело цикла — всё, что сдвинуто вправо.
      </div>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title="Вечный цикл"
      sub="Условие, которое никогда не станет ложным"
      main="Внутри тела что-то должно меняться — тогда у условия есть шанс стать ложным."
    >
      <PyCode>{`n = 3
while n > 0:
    print(n)
    # счётчик не меняется — цикл вечен!`}</PyCode>
      <div className="s-cols">
        <Node kind="amber" title="Программа замирает" sub="Работает изо всех сил — без всякого прогресса" />
        <Node kind="green" title="Таймаут спасает" sub="Тренажёр останавливает код, не уложившийся в лимит" />
      </div>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title="Цикл фор"
      sub="Читается как «для каждого элемента из»"
      main="Ни счётчиков, ни границ, ни ручного шага — только суть задачи."
    >
      <PyCode>{`for ch in "привет":
    print(ch)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"п\nр\nи\nв\nе\nт"}</Cmd>
      <div className="s-note">
        На каждом витке переменная ch получает очередной символ слова.
      </div>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title="Рэндж"
      sub="Числовые серии для повтора"
      main="Правая граница в рэндже никогда не включается."
    >
      <PyCode>{`for i in range(5):
    print(i)`}</PyCode>
      <Cmd>{"0\n1\n2\n3\n4"}</Cmd>
      <div className="s-cols">
        <Node mono title="range(1, 6)" sub="От одного до пяти — шесть не попадёт" />
        <Node mono title="range(0, 10, 2)" sub="Третий аргумент — шаг: 0 2 4 6 8" />
      </div>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title="Накопитель"
      sub="Копилка, которая растёт на каждом витке"
      main="Меняются начальное значение и действие — так считаются суммы, счётчики и произведения."
    >
      <PyCode>{`total = 0
for i in range(1, 101):
    total += i
print(total)`}</PyCode>
      <Cmd>{"5050"}</Cmd>
      <div className="s-cols">
        <Node mono title="total += i" sub="Плюс-равно: прибавь и запиши обратно в ту же переменную" />
        <Node kind="green" mono title="range(1, 101)" sub="Граница 101 — чтобы включить сто" />
      </div>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title="Брейк"
      sub="Немедленный выход из цикла"
      main="Брейк экономит витки и делает намерение явным: дальше идти не нужно."
    >
      <PyCode>{`for ch in "abc3def":
    if ch in "0123456789":
        print(ch)
        break`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3"}</Cmd>
      <div className="s-note">
        Первую цифру нашли — остаток строки проверять незачем.
      </div>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title="Континуе"
      sub="Пропустить остаток тела — к следующему витку"
      main="Брейк закрывает цикл целиком, континуе — лишь один виток."
    >
      <PyCode>{`for i in range(1, 11):
    if i % 2 == 0:
        continue
    print(i)`}</PyCode>
      <Cmd>{"1\n3\n5\n7\n9"}</Cmd>
      <div className="s-note">
        Остаток от деления на два равен нулю — число чётное, печатать не нужно.
      </div>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title="Вайл тру и брейк"
      sub="Бесконечный цикл с выходом по условию внутри"
      main="Выход в середине тела честнее натянутого условия сверху: точка выхода видна глазами."
    >
      <PyCode>{`while True:
    cmd = input("Команда: ")
    if cmd == "стоп":
        break
    print(cmd)`}</PyCode>
      <div className="s-cols">
        <Node kind="green" mono title="while True" sub="«Повторяй всегда» — так строят меню и опросы" />
        <Node mono title="break" sub="Срабатывает, когда пользователь ввёл «стоп»" />
      </div>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title="Вложенные циклы"
      sub="Цикл внутри цикла — работа умножается"
      main="На каждый виток внешнего внутренний проходит целиком."
    >
      <PyCode>{`for row in range(1, 4):
    for col in range(1, 4):
        print(row * col, end="  ")
    print()`}</PyCode>
      <Cmd>{"1  2  3\n2  4  6\n3  6  9"}</Cmd>
      <div className="s-cols">
        <Node mono title="row" sub="Внешний цикл: перебирает строки" />
        <Node mono title="col" sub="Внутренний цикл: перебирает столбцы" />
      </div>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title="Накопитель строк"
      sub="Собираем новую строку из символов старой"
      main="Строки неизменяемы: не правим старую, а каждый раз собираем новую."
    >
      <PyCode>{`word = "привет"
rev = ""
for ch in word:
    rev = ch + rev
print(rev)`}</PyCode>
      <Cmd>{"тевирп"}</Cmd>
      <div className="s-note">
        Каждая буква приписывается в начало результата — первая уезжает в самый конец.
      </div>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title="Типичные ошибки"
      sub="Три ловушки, на которых спотыкаются все"
      main="Фор — когда известно, по чему идём. Вайл — когда идём «пока не случится»."
    >
      <PyCode>{`# хотим числа от 1 до 5 — а получаем от 1 до 4
for i in range(1, 5):
    print(i)`}</PyCode>
      <div className="s-cols">
        <Node kind="amber" mono title="range(1, 5)" sub="Правая граница не включается — нужна range(1, 6)" />
        <Node kind="amber" title="Счётчик вайл" sub="Забыли менять — получили вечный цикл" />
      </div>
      <div className="s-note">
        Ошибка на единицу — самая коварная: код работает, но делает на один
        шаг меньше, чем хочется.
      </div>
    </Slide>
  );
}

function S13() {
  const topics = [
    ["while", "Вайл", "Повторяет тело, пока условие истинно"],
    ["for", "Фор", "Перебор элементов; числа даёт range"],
    ["break", "Брейк", "Немедленный выход из цикла"],
    ["continue", "Континуе", "Пропуск одного витка"],
  ];
  return (
    <Slide
      n={13}
      title="Итог"
      sub="Глава 4 · Данные и циклы"
      main="Действие пишется один раз — выполняется столько, сколько нужно."
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
        Циклам нужен простор: следующая глава — списки, центральный тип данных
        Питона. Сотни значений в одной переменной — и перебор их всех одним
        фором.
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_P4 = {
  "13:4": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_P4).
export const SLIDE_TITLES_P4 = {
  "13:4": [
    "Циклы",
    "Цикл вайл",
    "Вечный цикл",
    "Цикл фор",
    "Рэндж",
    "Накопитель",
    "Брейк",
    "Континуе",
    "Вайл тру и брейк",
    "Вложенные циклы",
    "Накопитель строк",
    "Типичные ошибки",
    "Итог",
  ],
};
