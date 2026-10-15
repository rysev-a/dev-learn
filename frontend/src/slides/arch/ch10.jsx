// Слайды для «Архитектура компьютера», глава 10 — «Параллелизм: многоядерность, когерентность, SIMD и GPU».
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
      <span>АРХИТЕКТУРА КОМПЬЮТЕРА / ВВОД-ВЫВОД И ПАРАЛЛЕЛИЗМ / ГЛАВА 10</span>
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
      title={"Параллельные процессоры"}
      sub={"Глава 10 · Ввод-вывод и параллелизм"}
      main={"Частота упёрлась в тепло — скорость растёт за счёт параллелизма."}
    >
      <div className="s-grid2">
        {[["N cores", "Многоядерность", "Несколько ядер на кристалле"], ["MESI", "Когерентность", "Согласованные кэши"], ["CAS", "Атомарность", "Гонки и блокировки"], ["SIMD · GPU", "Данные", "Одна команда — много значений"]].map(([big, t, d]) => (
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
      title={"Стена мощности"}
      sub={"Почему частота перестала расти"}
      main={"Мощность растёт почти как куб частоты: два ядра вдвое медленнее — та же работа за четверть энергии."}
    >
      <PyCode>{`power = lambda f: f ** 3          # напряжение растёт вместе с частотой
print(power(1), 2 * power(0.5))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 0.25"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Виды параллелизма"}
      sub={"Команды, данные, потоки, машины"}
      main={"Закон Амдала ограничивает масштабирование: 95% параллельной работы дают на 64 ядрах всего ~15×."}
    >
      <PyCode>{`def amdahl(p, n):
    return 1 / ((1 - p) + p / n)

print(round(amdahl(0.95, 8), 2), round(amdahl(0.95, 64), 2))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"5.93 15.42"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Проблема когерентности"}
      sub={"У каждого ядра свой кэш"}
      main={"Одна переменная — несколько копий: без протокола ядра увидят разные значения."}
    >
      <PyCode>{`memory = {"x": 1}
cache0, cache1 = {"x": 1}, {"x": 1}
cache0["x"] = 5               # ядро 0 записало только в свой кэш
print(cache1["x"], memory["x"])   # ядро 1 видит старое`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 1"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Протокол MESI"}
      sub={"Modified · Exclusive · Shared · Invalid"}
      main={"Запись делает остальные копии недействительными — изменённая копия всегда единственная."}
    >
      <PyCode>{`def access(states, core, op):
    others = [i for i in range(len(states)) if i != core]
    if op == "R":
        if states[core] == "I":
            if any(states[i] != "I" for i in others):
                for i in others:
                    if states[i] in "ME":
                        states[i] = "S"
                states[core] = "S"
            else:
                states[core] = "E"
    else:
        for i in others:
            states[i] = "I"
        states[core] = "M"
    return "".join(states)

s = ["I", "I"]
for core, op in [(0, "R"), (1, "R"), (0, "W"), (1, "R")]:
    print(core, op, access(s, core, op))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0 R EI\n1 R SS\n0 W MI\n1 R SS"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Ложное разделение"}
      sub={"Разные переменные в одной кэш-строке"}
      main={"Потоки не пересекаются логически, но строка «пинг-понгом» летает между ядрами."}
    >
      <PyCode>{`def ping_pong(writes, line=64):
    last, moves = {}, 0
    for core, addr in writes:
        block = addr // line
        if last.get(block, core) != core:
            moves += 1
        last[block] = core
    return moves

same_line = [(0, 0), (1, 8)] * 5       # разные переменные, одна строка
diff_lines = [(0, 0), (1, 64)] * 5
print(ping_pong(same_line), ping_pong(diff_lines))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"9 0"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Гонка данных"}
      sub={"Увеличение счётчика не атомарно"}
      main={"load → add → store: если два потока прочитали одно значение, одно прибавление теряется."}
    >
      <PyCode>{`def run(order):
    counter, regs = 0, {}
    for t, step in order:
        if step == "load":
            regs[t] = counter
        else:
            counter = regs[t] + 1
    return counter

print(run([(0, "load"), (0, "store"), (1, "load"), (1, "store")]))
print(run([(0, "load"), (1, "load"), (0, "store"), (1, "store")]))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2\n1"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Атомарные операции"}
      sub={"Compare-and-swap"}
      main={"CAS записывает новое значение только если старое совпало — повторяйте цикл до успеха."}
    >
      <PyCode>{`class Cell:
    def __init__(self, v):
        self.v = v

    def cas(self, expected, new):       # в железе — одна неделимая команда
        if self.v == expected:
            self.v = new
            return True
        return False

c = Cell(5)
print(c.cas(5, 6), c.cas(5, 7), c.v)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True False 6"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Модель памяти"}
      sub={"Перестановки и барьеры"}
      main={"Если разрешить переставлять запись и чтение, появляется результат (0, 0), невозможный при последовательном порядке."}
    >
      <PyCode>{`from itertools import permutations

ops = [(0, "W", "x"), (0, "R", "y"), (1, "W", "y"), (1, "R", "x")]

def outcomes(allow_reorder):
    res = set()
    for perm in permutations(range(4)):
        if not allow_reorder and (perm.index(0) > perm.index(1) or perm.index(2) > perm.index(3)):
            continue
        mem, r = {"x": 0, "y": 0}, {}
        for i in perm:
            t, kind, var = ops[i]
            if kind == "W":
                mem[var] = 1
            else:
                r[t] = mem[var]
        res.add((r[0], r[1]))
    return sorted(res)

print(outcomes(False))
print(outcomes(True))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[(0, 1), (1, 0), (1, 1)]\n[(0, 0), (0, 1), (1, 0), (1, 1)]"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"SIMD"}
      sub={"Одна команда — много значений"}
      main={"Вектор в 256 бит — 8 чисел float32: в 8 раз меньше команд на массив."}
    >
      <PyCode>{`n, width = 1024, 8
print(n, -(-n // width))              # скалярных и векторных команд
a = [1, 2, 3, 4, 5, 6, 7, 8]
b = [10] * 8
print([x + y for x, y in zip(a, b)])    # одна векторная команда на 8 пар`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1024 128\n[11, 12, 13, 14, 15, 16, 17, 18]"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"GPU"}
      sub={"SIMT и расхождение потоков"}
      main={"Потоки варпа выполняют одну команду: при разных ветвях условия выполняются обе — время суммируется."}
    >
      <PyCode>{`def warp_steps(conditions, then_cost, else_cost):
    steps = 0
    if any(conditions):
        steps += then_cost
    if not all(conditions):
        steps += else_cost
    return steps

print(warp_steps([True] * 32, 10, 10), warp_steps([True] * 31 + [False], 10, 10))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"10 20"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Энергоэффективность и ускорители"}
      sub={"Операций на ватт"}
      main={"Специализированные блоки в десятки раз эффективнее универсальных ядер на ватт."}
    >
      <PyCode>{`chips = {"CPU": (200, 100), "GPU": (10000, 300), "NPU": (4000, 15)}   # (GFLOPS, ватт)
for name, (gflops, watt) in chips.items():
    print(name, round(gflops / watt, 1))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"CPU 2.0\nGPU 33.3\nNPU 266.7"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Параллелизм даёт скорость, но требует согласования: кэшей, доступа к данным и порядка записей."}
    >
      <div className="s-grid2">
        {[["f³", "Мощность", "Почему ядер много"], ["MESI", "Кэши", "Один владелец изменений"], ["CAS", "Данные", "Атомарные операции"], ["SIMT", "GPU", "Много однородных потоков"]].map(([big, t, d]) => (
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
export const SLIDES_AR10 = {
  "14:10": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_AR10).
export const SLIDE_TITLES_AR10 = {
  "14:10": [
    "Параллельные процессоры",
    "Стена мощности",
    "Виды параллелизма",
    "Когерентность",
    "MESI",
    "False sharing",
    "Гонка данных",
    "CAS",
    "Модель памяти",
    "SIMD",
    "GPU",
    "Ускорители",
    "Итоги",
  ],
};
