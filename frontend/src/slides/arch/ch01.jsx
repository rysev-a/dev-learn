// Слайды для «Архитектура компьютера», глава 1 — «Биты и логические вентили».
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
      <span>АРХИТЕКТУРА КОМПЬЮТЕРА / ЛОГИКА И ЧИСЛА / ГЛАВА 1</span>
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
      title={"От вентиля до сумматора"}
      sub={"Глава 1 · Логика и числа"}
      main={"Любой компьютер — это сигналы двух уровней и переключатели, которые превращают одни сигналы в другие."}
    >
      <div className="s-grid2">
        {[["0 · 1", "Бит", "Два уровня напряжения"], ["AND · OR · NOT", "Вентили", "Простейшие кирпичики логики"], ["ΣΣΣ", "Сумматор", "Складываем из вентилей"], ["Q", "Память", "Обратная связь даёт защёлку"]].map(([big, t, d]) => (
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
      title={"Бит: ноль или единица"}
      sub={"Почему компьютер двоичный"}
      main={"Два уровня различить надёжно даже в шуме; десять — нет. Восемь бит — байт."}
    >
      <div className="s-cols">
        <Node kind="" mono={true} title={"0"} sub={"низкое напряжение"} />
        <Node kind="green" mono={true} title={"1"} sub={"высокое напряжение"} />
        <Node kind="" mono={true} title={"8 бит = 1 байт"} sub={"256 разных значений"} />
      </div>
      <PyCode>{`print(2 ** 1, 2 ** 8, 2 ** 16, 2 ** 32)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2 256 65536 4294967296"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Вентили И, ИЛИ, НЕ"}
      sub={"Три базовых вентиля"}
      main={"«И» — единица, когда обе единицы; «ИЛИ» — когда хоть одна; «НЕ» переворачивает бит."}
    >
      <PyCode>{`def AND(a, b): return a & b
def OR(a, b): return a | b
def NOT(a): return 1 - a

print("a b AND OR")
for a in (0, 1):
    for b in (0, 1):
        print(a, b, AND(a, b), OR(a, b))
print(NOT(0), NOT(1))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"a b AND OR\n0 0 0 0\n0 1 0 1\n1 0 0 1\n1 1 1 1\n1 0"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"XOR и NAND"}
      sub={"Сравнение и универсальный вентиль"}
      main={"XOR — единица, когда входы различны. NAND = «И» с перевёрнутым результатом."}
    >
      <PyCode>{`def XOR(a, b): return a ^ b
def NAND(a, b): return 1 - (a & b)

for a in (0, 1):
    for b in (0, 1):
        print(a, b, "xor", XOR(a, b), "nand", NAND(a, b))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0 0 xor 0 nand 1\n0 1 xor 1 nand 1\n1 0 xor 1 nand 1\n1 1 xor 0 nand 0"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Всё из одного NAND"}
      sub={"Универсальность и законы Де Моргана"}
      main={"NOT, AND и OR собираются из одних NAND; перебор четырёх входов доказывает равенство."}
    >
      <PyCode>{`def NAND(a, b): return 1 - (a & b)

def NOT(a): return NAND(a, a)
def AND(a, b): return NOT(NAND(a, b))
def OR(a, b): return NAND(NOT(a), NOT(b))

pairs = [(a, b) for a in (0, 1) for b in (0, 1)]
print(all(AND(a, b) == a & b for a, b in pairs))
print(all(OR(a, b) == a | b for a, b in pairs))
print(all(NOT(a) == 1 - a for a in (0, 1)))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True\nTrue\nTrue"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Полусумматор"}
      sub={"Сложение двух битов"}
      main={"Сумма — это XOR, перенос — это AND. Два вентиля складывают два бита."}
    >
      <PyCode>{`def half_adder(a, b):
    return a ^ b, a & b   # (сумма, перенос)

for a in (0, 1):
    for b in (0, 1):
        s, c = half_adder(a, b)
        print(a, "+", b, "=", c, s)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0 + 0 = 0 0\n0 + 1 = 0 1\n1 + 0 = 0 1\n1 + 1 = 1 0"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Полный сумматор"}
      sub={"Два слагаемых и перенос"}
      main={"Два полусумматора и OR дают один разряд сложения с переносом."}
    >
      <PyCode>{`def half_adder(a, b):
    return a ^ b, a & b

def full_adder(a, b, cin):
    s1, c1 = half_adder(a, b)
    s2, c2 = half_adder(s1, cin)
    return s2, c1 | c2

print(full_adder(1, 1, 0))
print(full_adder(1, 1, 1))
print(full_adder(0, 1, 1))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(0, 1)\n(1, 1)\n(0, 1)"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Сумматор со сквозным переносом"}
      sub={"Цепочка полных сумматоров"}
      main={"Перенос бежит от младшего разряда к старшему — время растёт с числом разрядов."}
    >
      <PyCode>{`def full_adder(a, b, cin):
    s = a ^ b ^ cin
    return s, (a & b) | (cin & (a ^ b))

def add_bits(x, y, width=4):
    carry, out = 0, 0
    for i in range(width):
        s, carry = full_adder((x >> i) & 1, (y >> i) & 1, carry)
        out |= s << i
    return out, carry

print(add_bits(5, 3))
print(add_bits(9, 9))
print(add_bits(15, 1))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(8, 0)\n(2, 1)\n(0, 1)"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Мультиплексор"}
      sub={"Выбираем один из входов"}
      main={"Мультиплексор — переключатель: управляющий бит решает, какой вход пойдёт на выход."}
    >
      <PyCode>{`def mux(sel, a, b):
    return (a & (1 - sel)) | (b & sel)

print(mux(0, 1, 0), mux(1, 1, 0))
print(mux(0, 0, 1), mux(1, 0, 1))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 0\n0 1"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Защёлка: бит памяти"}
      sub={"Обратная связь запоминает"}
      main={"Два вентиля NOR с перекрёстной связью хранят бит, пока на входах нули."}
    >
      <PyCode>{`def nor(a, b): return 1 - (a | b)

class SRLatch:
    def __init__(self):
        self.q, self.nq = 0, 1
    def step(self, s, r):
        for _ in range(3):          # даём схеме установиться
            self.q, self.nq = nor(r, self.nq), nor(s, self.q)
        return self.q

l = SRLatch()
print(l.step(1, 0), l.step(0, 0), l.step(0, 1), l.step(0, 0))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1 1 0 0"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Такт, триггер, регистр"}
      sub={"Память меняется по сигналу часов"}
      main={"Регистр принимает новое значение только в момент такта; частота — тактов в секунду."}
    >
      <PyCode>{`class Register:
    def __init__(self):
        self.value = 0
    def tick(self, data, load):
        if load:
            self.value = data
        return self.value

r = Register()
print(r.tick(42, 1), r.tick(7, 0), r.tick(7, 1))
print(3_000_000_000, "тактов в секунду при 3 ГГц")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"42 42 7\n3000000000 тактов в секунду при 3 ГГц"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"АЛУ: считаем всё и выбираем"}
      sub={"Арифметико-логическое устройство"}
      main={"АЛУ вычисляет все результаты параллельно, а мультиплексор по коду операции выбирает один."}
    >
      <PyCode>{`def alu(op, a, b, width=8):
    mask = (1 << width) - 1
    results = {
        "ADD": (a + b) & mask,
        "AND": a & b,
        "OR": a | b,
        "XOR": a ^ b,
    }
    return results[op]

print(alu("ADD", 200, 100), alu("AND", 12, 10), alu("OR", 12, 10), alu("XOR", 12, 10))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"44 8 14 6"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Из нескольких видов вентилей собирается арифметика, выбор и память — это всё, что нужно процессору."}
    >
      <div className="s-grid2">
        {[["NAND", "Универсальный", "Из него — любая схема"], ["XOR + AND", "Полусумматор", "Сумма и перенос"], ["MUX", "Выбор", "Данные и операции"], ["CLK", "Такт", "Регистры меняются по сигналу"]].map(([big, t, d]) => (
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
export const SLIDES_AR1 = {
  "14:1": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_AR1).
export const SLIDE_TITLES_AR1 = {
  "14:1": [
    "От вентиля до сумматора",
    "Бит",
    "И, ИЛИ, НЕ",
    "XOR и NAND",
    "Универсальность NAND",
    "Полусумматор",
    "Полный сумматор",
    "Сквозной перенос",
    "Мультиплексор",
    "Защёлка",
    "Такт и регистр",
    "АЛУ",
    "Итоги",
  ],
};
