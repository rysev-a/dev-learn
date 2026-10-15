// Слайды для «Архитектура компьютера», глава 7 — «Конвейер и производительность».
// Тот же дизайн-код, что и в эталоне: тёмная палитра, IBM Plex Mono / Inter,
// рубрика + номер, схема, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.
// Отличие: примеры кода на Python с подсветкой синтаксиса (классы rs-*).

const PY_KW = new Set([
  "print", "for", "in", "not", "and", "or", "if", "else", "while", "is",
  "True", "False", "None", "def", "return", "class", "import", "from", "elif",
  "lambda", "with", "assert", "raise", "break", "continue", "pass", "yield",
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
      <span>АРХИТЕКТУРА КОМПЬЮТЕРА / ПАМЯТЬ И ПРОИЗВОДИТЕЛЬНОСТЬ / ГЛАВА 7</span>
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
      title={"Конвейер команд"}
      sub={"Глава 7 · Память и производительность"}
      main={"Пока одна команда исполняется, следующая декодируется, а третья читается из памяти."}
    >
      <div className="s-grid2">
        {[["IC × CPI ÷ f", "Железный закон", "Время программы"], ["IF ID EX MEM WB", "Конвейер", "Стадии в совмещении"], ["RAW · branch", "Конфликты", "Пузыри и обходы"], ["Amdahl", "Ускорение", "Ограничено долей"]].map(([big, t, d]) => (
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
      title={"Железный закон производительности"}
      sub={"Три множителя"}
      main={"Время = число команд × CPI ÷ частота; улучшение одного множителя может ухудшить другой."}
    >
      <PyCode>{`def exec_time(ic, cpi, ghz):
    return ic * cpi / (ghz * 1e9)

print(exec_time(10 ** 9, 1.5, 3))   # 1 млрд команд, CPI 1.5, 3 ГГц
print(exec_time(10 ** 9, 1.0, 2))   # проще и медленнее по частоте`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0.5\n0.5"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Идея конвейера"}
      sub={"Стирка — сушка — глажка"}
      main={"Время одной команды не меняется, но завершается по команде за такт: n команд за 5 + n − 1 такт вместо 5n."}
    >
      <PyCode>{`stages = 5
for n in (1, 5, 100):
    seq, pipe = stages * n, stages + n - 1
    print(n, seq, pipe, round(seq / pipe, 2))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 5 5 1.0\n5 25 9 2.78\n100 500 104 4.81"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Диаграмма конвейера"}
      sub={"Каждая команда сдвинута на такт"}
      main={"С пятого такта все стадии заняты: идеальный CPI равен единице."}
    >
      <PyCode>{`stages = ["IF", "ID", "EX", "MEM", "WB"]
for i in range(3):
    row = [""] * i + stages
    print(" ".join(f"{s:<3}" for s in row).rstrip())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"IF  ID  EX  MEM WB\n    IF  ID  EX  MEM WB\n        IF  ID  EX  MEM WB"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Конфликты и зависимости"}
      sub={"Структурные, по данным, по управлению"}
      main={"«Чтение после записи» (RAW): следующая команда читает регистр, который ещё не записан."}
    >
      <PyCode>{`prog = [("ADD", "R1", "R2", "R3"),   # (операция, приёмник, источники…)
        ("SUB", "R4", "R1", "R5"),
        ("AND", "R6", "R7", "R8"),
        ("OR", "R9", "R1", "R4")]
for i, (op, dest, *srcs) in enumerate(prog):
    for j in range(i + 1, len(prog)):
        if dest in prog[j][2:]:
            print(f"RAW: {i} → {j}")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"RAW: 0 → 1\nRAW: 0 → 3\nRAW: 1 → 3"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Пузыри и обходы"}
      sub={"Сколько тактов теряем"}
      main={"Без обходов зависимая команда ждёт 2 такта (соседняя) или 1; обход (forwarding) убирает паузу."}
    >
      <PyCode>{`def stalls(distance, forwarding):
    if forwarding:
        return 0
    return max(0, 3 - distance)

print([stalls(d, False) for d in (1, 2, 3, 4)], stalls(1, True))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[2, 1, 0, 0] 0"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Зависимость от загрузки"}
      sub={"Исключение, которое обходы не лечат"}
      main={"Данные из памяти готовы поздно: нужна пауза на 1 такт — её заполняют перестановкой команд."}
    >
      <PyCode>{`prog = [("LW", "R1"), ("ADD", "R2", "R1"), ("SUB", "R3", "R4"), ("LW", "R5"), ("OR", "R6", "R7")]
load_use = [i for i in range(len(prog) - 1)
            if prog[i][0] == "LW" and prog[i][1] in prog[i + 1][2:]]
print(load_use, "→ пауз:", len(load_use))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[0] → пауз: 1"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Конфликты по управлению"}
      sub={"Цена неверного предсказания"}
      main={"Ошибка предсказания сбрасывает уже начатые команды: CPI растёт на долю_веток × ошибки × штраф."}
    >
      <PyCode>{`branch_share, miss_rate, penalty = 0.20, 0.10, 3
cpi = 1 + branch_share * miss_rate * penalty
print(round(cpi, 2))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1.06"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Предсказатель переходов"}
      sub={"Двухбитный счётчик"}
      main={"Прогноз меняется после двух ошибок подряд: цикл проигрывает один переход, а не два."}
    >
      <PyCode>{`def predict(history, bits):
    state, correct = 0, 0
    for taken in history:
        if bits == 1:
            guess = state == 1
            state = int(taken)
        else:
            guess = state >= 2
            state = min(3, state + 1) if taken else max(0, state - 1)
        correct += guess == taken
    return correct

loop = ([True] * 9 + [False]) * 10      # цикл на 10 итераций
print(predict(loop, 1), predict(loop, 2), len(loop))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"80 88 100"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Суперскалярность"}
      sub={"Несколько команд за такт"}
      main={"Ширина машины не помогает, если команды выстроены в цепочку зависимостей — критический путь."}
    >
      <PyCode>{`deps = {0: [], 1: [], 2: [0, 1], 3: [2], 4: [], 5: [3, 4]}

def depth(i):
    return 1 + max((depth(d) for d in deps[i]), default=0)

print(max(depth(i) for i in deps), len(deps))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"4 6"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Закон Амдала"}
      sub={"Ускорение части — не всего"}
      main={"Даже бесконечное ускорение 90% программы даёт не более 10×: оставшиеся 10% — узкое место."}
    >
      <PyCode>{`def amdahl(p, s):
    return 1 / ((1 - p) + p / s)

print(round(amdahl(0.9, 10), 2), round(amdahl(0.9, 1e9), 2), round(amdahl(0.5, 4), 2))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"5.26 10.0 1.6"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Как сравнивать процессоры"}
      sub={"MIPS и частота обманывают"}
      main={"Честная метрика — время реальной программы, а не число команд в секунду."}
    >
      <PyCode>{`cpus = {"A": (4000, 10 ** 9), "B": (2500, 5 * 10 ** 8)}   # (MIPS, команд в программе)
for name, (mips, n) in cpus.items():
    print(name, n / (mips * 10 ** 6), "с")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"A 0.25 с\nB 0.2 с"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Конвейер даёт пропускную способность; конфликты и ошибки предсказания возвращают потерянные такты."}
    >
      <div className="s-grid2">
        {[["CPI → 1", "Конвейер", "Стадии в совмещении"], ["forwarding", "Обходы", "Убирают зависимость"], ["2-bit", "Предсказание", "Меньше сбросов"], ["1 / (1−p+p/s)", "Амдал", "Узкое место остаётся"]].map(([big, t, d]) => (
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

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_AR7 = {
  "14:7": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_AR7).
export const SLIDE_TITLES_AR7 = {
  "14:7": [
    "Конвейер команд",
    "Железный закон",
    "Идея конвейера",
    "Диаграмма",
    "Конфликты",
    "Пузыри и обходы",
    "Загрузка и использование",
    "Переходы",
    "Предсказатель",
    "Суперскалярность",
    "Закон Амдала",
    "Сравнение процессоров",
    "Итоги",
  ],
};
