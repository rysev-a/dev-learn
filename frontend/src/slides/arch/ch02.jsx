// Слайды для «Архитектура компьютера», глава 2 — «Числа в компьютере».
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
      <span>АРХИТЕКТУРА КОМПЬЮТЕРА / ЛОГИКА И ЧИСЛА / ГЛАВА 2</span>
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
      title={"Числа из битов"}
      sub={"Глава 2 · Логика и числа"}
      main={"Число в компьютере — это фиксированное число битов и договорённость о том, как их читать."}
    >
      <div className="s-grid2">
        {[["2 · 16", "Системы счисления", "Двоичная и шестнадцатеричная"], ["−128 … 127", "Знаковые числа", "Дополнительный код"], ["<< >> & |", "Битовые операции", "Маски, флаги, сдвиги"], ["IEEE 754", "Дробные числа", "Знак, порядок, мантисса"]].map(([big, t, d]) => (
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
      title={"Позиционная система"}
      sub={"Двоичная запись"}
      main={"Цифры умножаются на степени основания; перевод — деление на два с остатками."}
    >
      <PyCode>{`print(bin(13), int("1101", 2), format(13, "08b"))

n, bits = 13, []
while n:
    bits.append(n % 2)
    n //= 2
print(bits[::-1])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0b1101 13 00001101\n[1, 1, 0, 1]"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Шестнадцатеричная система"}
      sub={"Одна цифра — четыре бита"}
      main={"Байт — две шестнадцатеричные цифры; перевод в двоичную запись — без вычислений."}
    >
      <PyCode>{`print(hex(255), 0xFF, format(0xA5, "08b"))

r, g, b = 255, 136, 0
print(f"#{r:02x}{g:02x}{b:02x}")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0xff 255 10100101\n#ff8800"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Фиксированная ширина и переполнение"}
      sub={"Арифметика по модулю"}
      main={"В n битах арифметика идёт по модулю 2ⁿ: после 255 снова 0, а ноль минус единица — 255."}
    >
      <PyCode>{`x = 250
print((x + 10) & 0xFF, (0 - 1) & 0xFF, 2 ** 8 - 1)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"4 255 255"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Знак и величина"}
      sub={"Очевидный способ — неудобный"}
      main={"Старший бит — знак: получаются два нуля, а для сложения нужны разные схемы."}
    >
      <PyCode>{`def from_sign_magnitude(b):
    return -(b & 0x7F) if b & 0x80 else b

print(from_sign_magnitude(0b00000000))
print(from_sign_magnitude(0b10000000))   # «минус ноль»
print(from_sign_magnitude(0b10000101))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0\n0\n-5"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Дополнительный код"}
      sub={"Инвертировать и прибавить единицу"}
      main={"−x записывается как 2ⁿ − x: один нуль и диапазон от −128 до 127 в восьми битах."}
    >
      <PyCode>{`def to_twos(n, w=8):
    return n & ((1 << w) - 1)

def from_twos(b, w=8):
    return b - (1 << w) if b >> (w - 1) else b

print(format(to_twos(-5), "08b"), from_twos(0b11111011))
print(from_twos(0b10000000), from_twos(0b01111111))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"11111011 -5\n-128 127"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Сложение и вычитание"}
      sub={"Один сумматор для всех"}
      main={"Знаковые и беззнаковые числа складываются одинаково; переполнение — одинаковый знак, а результат другой."}
    >
      <PyCode>{`def from_twos(b, w=8):
    return b - (1 << w) if b >> (w - 1) else b

raw = (100 + 100) & 0xFF
print(raw, from_twos(raw))      # знаковое переполнение
print(from_twos((7 - 9) & 0xFF))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"200 -56\n-2"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Маски и флаги"}
      sub={"Установить, сбросить, переключить, проверить"}
      main={"Одно число — набор независимых переключателей; маска выбирает нужный бит."}
    >
      <PyCode>{`flags = 0
flags |= 1 << 3
flags |= 1 << 0
print(format(flags, "08b"))
flags &= ~(1 << 3)
print(format(flags, "08b"), bool(flags & 1))
flags ^= 1 << 7
print(format(flags, "08b"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"00001001\n00000001 True\n10000001"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Сдвиги"}
      sub={"Умножение и деление на степень двойки"}
      main={"Сдвиг влево — умножение на 2ᵏ, вправо — деление; арифметический сдвиг копирует знак."}
    >
      <PyCode>{`x = 13
print(x << 1, x << 3, x >> 1, x >> 2)
print(-8 >> 1, -1 >> 5, (-8 & 0xFF) >> 1)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"26 104 6 3\n-4 -1 124"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Числа с плавающей точкой"}
      sub={"Знак, порядок, мантисса"}
      main={"В 32 битах: 1 бит знака, 8 бит порядка (смещение 127), 23 бита мантиссы."}
    >
      <PyCode>{`import struct

def parts(x):
    b = struct.unpack(">I", struct.pack(">f", x))[0]
    return b >> 31, (b >> 23) & 0xFF, b & 0x7FFFFF

print(parts(1.0))
print(parts(-2.5))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(0, 127, 0)\n(1, 128, 2097152)"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Погрешность дробных чисел"}
      sub={"0.1 + 0.2 ≠ 0.3"}
      main={"Сравнивайте дроби с допуском; бесконечность и NaN — особые значения."}
    >
      <PyCode>{`import math

print(0.1 + 0.2, 0.1 + 0.2 == 0.3, math.isclose(0.1 + 0.2, 0.3))
print(float("inf") - float("inf"), 2 ** 53 + 1.0 == 2 ** 53)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0.30000000000000004 False True\nnan True"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Порядок байтов"}
      sub={"Big-endian и little-endian"}
      main={"В сети — от старшего к младшему; у большинства процессоров — от младшего к старшему."}
    >
      <PyCode>{`n = 0x12345678
print(n.to_bytes(4, "big").hex(), n.to_bytes(4, "little").hex())
print(int.from_bytes(bytes([0x78, 0x56, 0x34, 0x12]), "little") == n)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"12345678 78563412\nTrue"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Числа конечны и приближённы: ширина, знак, порядок байтов и погрешность нужно помнить всегда."}
    >
      <div className="s-grid2">
        {[["mod 2ⁿ", "Переполнение", "Арифметика по модулю"], ["~x + 1", "Доп. код", "Один сумматор для всех"], ["& | ^ << >>", "Биты", "Маски, флаги, сдвиги"], ["float32", "Дроби", "Приближённые значения"]].map(([big, t, d]) => (
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
export const SLIDES_AR2 = {
  "14:2": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_AR2).
export const SLIDE_TITLES_AR2 = {
  "14:2": [
    "Числа из битов",
    "Двоичная система",
    "Hex",
    "Переполнение",
    "Знак и величина",
    "Доп. код",
    "Сложение в доп. коде",
    "Маски и флаги",
    "Сдвиги",
    "IEEE 754",
    "Погрешность",
    "Порядок байтов",
    "Итоги",
  ],
};
