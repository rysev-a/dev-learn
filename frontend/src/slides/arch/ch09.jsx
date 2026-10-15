// Слайды для «Архитектура компьютера», глава 9 — «Ввод-вывод, шины и диски».
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
      <span>АРХИТЕКТУРА КОМПЬЮТЕРА / ВВОД-ВЫВОД И ПАРАЛЛЕЛИЗМ / ГЛАВА 9</span>
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
      title={"Связь с внешним миром"}
      sub={"Глава 9 · Ввод-вывод и параллелизм"}
      main={"Устройства в тысячи раз медленнее процессора — вся архитектура ввода-вывода не даёт им тормозить остальное."}
    >
      <div className="s-grid2">
        {[["MMIO", "Регистры устройства", "В адресном пространстве"], ["IRQ", "Прерывания", "Устройство зовёт процессор"], ["DMA", "Прямой доступ", "Копирует без процессора"], ["HDD · SSD · RAID", "Хранилища", "Скорость и надёжность"]].map(([big, t, d]) => (
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
      title={"Шины"}
      sub={"Ширина × частота"}
      main={"Пропускная способность — число байт за передачу, умноженное на передач в секунду."}
    >
      <PyCode>{`def bandwidth(width_bits, mt_per_s):
    return width_bits / 8 * mt_per_s / 1000      # ГБ/с

print(bandwidth(64, 3200), bandwidth(32, 33))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"25.6 0.132"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Регистры в адресном пространстве"}
      sub={"Ввод-вывод, отображённый на память"}
      main={"Обычная запись по «особому» адресу — это команда устройству."}
    >
      <PyCode>{`memory, out = {}, []

def write(addr, value):
    if addr == 0x8000:            # регистр данных «консоли»
        out.append(chr(value))
    else:
        memory[addr] = value

for ch in "Привет":
    write(0x8000, ord(ch))
write(0x10, 42)
print("".join(out), memory)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Привет {16: 42}"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Опрос"}
      sub={"Крутимся в цикле и ждём"}
      main={"Просто и быстро реагирует, но всё время ожидания процессор занят пустой работой."}
    >
      <PyCode>{`def poll(ready_after):
    cycles = 0
    while cycles < ready_after:
        cycles += 1                # читаем регистр состояния
    return cycles

print(poll(1000), "тактов впустую")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"1000 тактов впустую"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Прерывания"}
      sub={"Таблица векторов"}
      main={"Устройство зовёт само: процессор сохраняет состояние, прыгает в обработчик и возвращается."}
    >
      <PyCode>{`handlers = {0: "таймер", 1: "клавиатура", 14: "page fault"}   # таблица векторов
for irq in [1, 0, 14, 1]:
    print("IRQ", irq, "→", handlers[irq])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"IRQ 1 → клавиатура\nIRQ 0 → таймер\nIRQ 14 → page fault\nIRQ 1 → клавиатура"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Опрос или прерывания"}
      sub={"Цена зависит от частоты событий"}
      main={"При редких событиях выгоднее прерывания, при потоке — опрос пачками (гибрид, как NAPI в Linux)."}
    >
      <PyCode>{`irq_cost = 2000          # тактов на одно прерывание
poll_cost = 50           # тактов на одну проверку
for rate in (10, 1000, 100000):      # событий в секунду
    print(rate, rate * irq_cost, 1000 * poll_cost)   # прерывания и опрос 1000 раз/с`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"10 20000 50000\n1000 2000000 50000\n100000 200000000 50000"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"DMA"}
      sub={"Прямой доступ к памяти"}
      main={"Процессор только ставит задачу; данные переносит контроллер, по завершении — одно прерывание."}
    >
      <PyCode>{`size = 4096
cpu_copy = size * 2        # прочитать байт и записать байт
dma_setup = 100            # записать адрес, размер, направление
print(cpu_copy, dma_setup)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"8192 100"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Жёсткий диск"}
      sub={"Поиск + оборот + передача"}
      main={"Одно случайное обращение — около 12 мс: диск делает меньше сотни таких операций в секунду."}
    >
      <PyCode>{`rpm = 7200
rot_ms = 60_000 / rpm / 2           # в среднем пол-оборота
seek_ms = 8
transfer_ms = 4096 / (150 * 10 ** 6) * 1000
print(round(rot_ms, 2), round(seek_ms + rot_ms + transfer_ms, 2))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"4.17 12.19"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Планирование запросов к диску"}
      sub={"FCFS и ближайший запрос"}
      main={"Упорядочить запросы — меньше путь головки; лифт (SCAN) ещё и не оставляет запросы голодать."}
    >
      <PyCode>{`def fcfs(start, reqs):
    pos, total = start, 0
    for r in reqs:
        total += abs(r - pos)
        pos = r
    return total

def sstf(start, reqs):
    pos, total, left = start, 0, list(reqs)
    while left:
        nxt = min(left, key=lambda r: abs(r - pos))
        total += abs(nxt - pos)
        pos = nxt
        left.remove(nxt)
    return total

reqs = [98, 183, 37, 122, 14, 124, 65, 67]
print(fcfs(53, reqs), sstf(53, reqs))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"640 236"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"SSD"}
      sub={"Флеш: пишем страницы, стираем блоки"}
      main={"Контроллер пишет изменения в новое место и позже стирает блоки целиком — без перезаписи на месте."}
    >
      <PyCode>{`pages_per_block = 256
in_place = pages_per_block      # перезаписать весь блок ради одной страницы
ftl = 1                         # записать одну новую страницу
print(in_place, ftl, in_place // ftl, "×")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"256 1 256 ×"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"RAID с чётностью"}
      sub={"XOR восстанавливает потерянный диск"}
      main={"Контрольный блок — XOR остальных: любой потерянный блок равен XOR всех уцелевших."}
    >
      <PyCode>{`d1, d2, d3 = 0b1010, 0b0110, 0b1111
parity = d1 ^ d2 ^ d3
print(format(parity, "04b"))
restored = d1 ^ d3 ^ parity        # диск 2 вышел из строя
print(restored == d2)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0011\nTrue"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Буферизация"}
      sub={"Системные вызовы дороги"}
      main={"Писать блоками по 4 КиБ вместо побайтной записи — в тысячи раз меньше вызовов."}
    >
      <PyCode>{`data = b"x" * 10000
unbuffered = len(data)                 # по одному байту — вызов на каждый
buffered = -(-len(data) // 4096)       # блоками по 4 КиБ
print(unbuffered, buffered)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"10000 3"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Ввод-вывод — это компромисс между простотой, нагрузкой на процессор и скоростью."}
    >
      <div className="s-grid2">
        {[["MMIO · IRQ", "Устройства", "Регистры и прерывания"], ["DMA", "Копирование", "Без участия CPU"], ["seek + rot", "Диск", "Порядок запросов важен"], ["XOR parity", "RAID", "Переживает потерю диска"]].map(([big, t, d]) => (
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
export const SLIDES_AR9 = {
  "14:9": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_AR9).
export const SLIDE_TITLES_AR9 = {
  "14:9": [
    "Ввод-вывод",
    "Шины",
    "MMIO",
    "Опрос",
    "Прерывания",
    "Опрос или прерывания",
    "DMA",
    "HDD",
    "Планирование диска",
    "SSD",
    "RAID",
    "Буферизация",
    "Итоги",
  ],
};
