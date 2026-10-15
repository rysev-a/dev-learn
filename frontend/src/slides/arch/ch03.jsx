// Слайды для «Архитектура компьютера», глава 3 — «Текст и защита данных».
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
      <span>АРХИТЕКТУРА КОМПЬЮТЕРА / ЛОГИКА И ЧИСЛА / ГЛАВА 3</span>
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
      title={"Текст — это числа"}
      sub={"Глава 3 · Логика и числа"}
      main={"Каждому символу присвоен номер; а чтобы данные не испортились, к ним добавляют избыточность."}
    >
      <div className="s-grid2">
        {[["ASCII", "Старый стандарт", "7 бит, английский алфавит"], ["Unicode", "Единый номер", "Кодовая точка для каждого символа"], ["UTF-8", "Запись в байтах", "От 1 до 4 байт на символ"], ["CRC · Hamming", "Защита от ошибок", "Обнаружить и даже исправить"]].map(([big, t, d]) => (
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
      title={"ASCII"}
      sub={"Семь бит на символ"}
      main={"Строчная и заглавная буквы отличаются одним битом (32)."}
    >
      <PyCode>{`print(ord("A"), chr(66), ord("a") - ord("A"), chr(ord("a") ^ 0x20))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"65 B 32 A"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Кодовые страницы и «крякозябры»"}
      sub={"Один байт — разные буквы"}
      main={"Прочитали текст не в той кодировке — получили мусор."}
    >
      <PyCode>{`text = "Привет"
raw = text.encode("cp1251")
print(raw.hex(), raw.decode("koi8-r"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"cff0e8e2e5f2 оПХБЕР"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Unicode"}
      sub={"Номер для каждого символа"}
      main={"Кодовая точка — это только номер; запись в байтах — отдельный вопрос."}
    >
      <PyCode>{`print(ord("Ж"), hex(ord("Ж")), "U+%04X" % ord("Ж"))
print(ord("€"), hex(ord("😀")))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1046 0x416 U+0416\n8364 0x1f600"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"UTF-8"}
      sub={"Переменная длина"}
      main={"Первый байт задаёт длину, остальные начинаются с 10 — начало символа всегда находится."}
    >
      <PyCode>{`for ch in "AЖ€😀":
    b = ch.encode()
    print(ch, len(b), " ".join(format(x, "08b") for x in b))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"A 1 01000001\nЖ 2 11010000 10010110\n€ 3 11100010 10000010 10101100\n😀 4 11110000 10011111 10011000 10000000"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Кодируем «Ж» вручную"}
      sub={"Раскладываем биты по шаблону"}
      main={"Для двух байт: 110xxxxx 10xxxxxx — в шаблон вставляются 11 бит кодовой точки."}
    >
      <PyCode>{`cp = ord("Ж")
b1 = 0b11000000 | (cp >> 6)
b2 = 0b10000000 | (cp & 0b111111)
print(hex(cp), hex(b1), hex(b2), bytes([b1, b2]).decode())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0x416 0xd0 0x96 Ж"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Символы и байты"}
      sub={"Длина строки — не размер в байтах"}
      main={"Для пользователя важно число символов, для сети и диска — число байтов."}
    >
      <PyCode>{`s = "привет"
print(len(s), len(s.encode()), len("😀"), len("😀".encode()))
print(len("é"), len("e\\u0301"), "é" == "e\\u0301")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"6 12 1 4\n1 2 False"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Бит чётности"}
      sub={"Самая простая защита"}
      main={"Один лишний бит обнаруживает одиночную ошибку, но не две и не говорит, где она."}
    >
      <PyCode>{`def parity_bit(x):
    return bin(x).count("1") % 2

data = 0b1011001
word = (data << 1) | parity_bit(data)
print(format(word, "08b"), parity_bit(word))
print(parity_bit(word ^ 0b100))
print(parity_bit(word ^ 0b101))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"10110010 0\n1\n0"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Контрольная сумма"}
      sub={"Защита блока данных"}
      main={"Простая сумма не замечает перестановку байтов — нужна зависимость от позиции."}
    >
      <PyCode>{`def checksum(data):
    return sum(data) % 256

a = bytes([10, 20, 30, 40])
b = bytes([10, 30, 20, 40])
print(checksum(a), checksum(b), a == b)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"100 100 False"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"CRC"}
      sub={"Деление многочленов"}
      main={"Остаток от деления на многочлен учитывает каждый бит и его позицию; в сетях — CRC32."}
    >
      <PyCode>{`def crc8(data, poly=0x07):
    crc = 0
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ poly) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc

print(hex(crc8(b"123456789")), hex(crc8(b"123456780")))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0xf4 0xcb"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Код Хэмминга"}
      sub={"Исправляем ошибку"}
      main={"Синдром из трёх проверок прямо указывает номер перевёрнутого бита."}
    >
      <PyCode>{`def encode(d1, d2, d3, d4):
    p1, p2, p3 = d1 ^ d2 ^ d4, d1 ^ d3 ^ d4, d2 ^ d3 ^ d4
    return [p1, p2, d1, p3, d2, d3, d4]

def correct(w):
    s1 = w[0] ^ w[2] ^ w[4] ^ w[6]
    s2 = w[1] ^ w[2] ^ w[5] ^ w[6]
    s3 = w[3] ^ w[4] ^ w[5] ^ w[6]
    pos = s1 + 2 * s2 + 4 * s3
    if pos:
        w[pos - 1] ^= 1
    return pos, w

w = encode(1, 0, 1, 1)
w[4] ^= 1
print(correct(w))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(5, [0, 1, 1, 0, 0, 1, 1])"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Криптографические хэши"}
      sub={"Защита от подмены"}
      main={"Лавинный эффект: один изменённый бит — совершенно другой отпечаток."}
    >
      <PyCode>{`import hashlib

a = hashlib.sha256(b"hello").hexdigest()
b = hashlib.sha256(b"hellp").hexdigest()
print(a[:16], b[:16])
print(sum(x != y for x, y in zip(a, b)), "из", len(a))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"2cf24dba5fb0a30e fdd7585e08c4e2af\n63 из 64"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Кодировка нужна всегда явная; защита от ошибок — это плата избыточными битами."}
    >
      <div className="s-grid2">
        {[["UTF-8", "Кодировка", "Явно указывайте её"], ["len ≠ bytes", "Символы и байты", "Не путайте при обрезании"], ["parity · CRC", "Обнаружение", "От бита до многочлена"], ["Hamming", "Исправление", "Синдром — номер ошибки"]].map(([big, t, d]) => (
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
export const SLIDES_AR3 = {
  "14:3": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_AR3).
export const SLIDE_TITLES_AR3 = {
  "14:3": [
    "Текст и защита данных",
    "ASCII",
    "Кодовые страницы",
    "Unicode",
    "UTF-8",
    "Кодирование вручную",
    "Символы и байты",
    "Бит чётности",
    "Контрольная сумма",
    "CRC",
    "Код Хэмминга",
    "Хэши",
    "Итоги",
  ],
};
