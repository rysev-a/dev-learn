// Слайды для «Архитектура компьютера», глава 8 — «Виртуальная память».
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
      <span>АРХИТЕКТУРА КОМПЬЮТЕРА / ПАМЯТЬ И ПРОИЗВОДИТЕЛЬНОСТЬ / ГЛАВА 8</span>
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
      title={"Своё адресное пространство"}
      sub={"Глава 8 · Память и производительность"}
      main={"Каждый процесс видит собственные адреса; процессор на лету превращает их в физические."}
    >
      <div className="s-grid2">
        {[["VPN | offset", "Страницы", "Виртуальный адрес"], ["page table", "Таблица", "Страница → кадр"], ["TLB", "Кэш переводов", "Прячет цену обхода"], ["page fault", "Прерывание", "Подкачка по требованию"]].map(([big, t, d]) => (
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
      title={"Зачем нужна виртуальная память"}
      sub={"Один адрес — два места"}
      main={"Один и тот же виртуальный адрес в двух процессах указывает на разные физические."}
    >
      <PyCode>{`table_a = {1: 7}       # виртуальная страница → физический кадр
table_b = {1: 3}
vaddr = 0x1234
for name, t in (("A", table_a), ("B", table_b)):
    frame = t[vaddr >> 12]
    print(name, hex((frame << 12) | (vaddr & 0xFFF)))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"A 0x7234\nB 0x3234"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Страницы и кадры"}
      sub={"Номер страницы и смещение"}
      main={"Страница 4 КиБ: старшие биты адреса — номер страницы, младшие 12 бит — смещение, оно не меняется."}
    >
      <PyCode>{`PAGE = 4096
for addr in (0, 4095, 4096, 0x12345):
    print(hex(addr), addr // PAGE, addr % PAGE)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0x0 0 0\n0xfff 0 4095\n0x1000 1 0\n0x12345 18 837"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Таблица страниц"}
      sub={"Перевод адреса"}
      main={"Нет записи или бит присутствия сброшен — страничное прерывание (page fault)."}
    >
      <PyCode>{`table = [7, None, 3]            # номер страницы → номер кадра

def translate(vaddr):
    vpn, off = vaddr >> 12, vaddr & 0xFFF
    if vpn >= len(table) or table[vpn] is None:
        return "page fault"
    return (table[vpn] << 12) | off

print(hex(translate(0x0042)), translate(0x1000), hex(translate(0x2ABC)), translate(0x9000))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0x7042 page fault 0x3abc page fault"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Флаги записи таблицы"}
      sub={"Присутствие, запись, пользователь, обращение, изменение"}
      main={"Биты обращения и изменения помогают ОС решать, какие страницы выгружать и сохранять."}
    >
      <PyCode>{`PRESENT, WRITE, USER, ACCESSED, DIRTY = 1, 2, 4, 32, 64
pte = (5 << 12) | PRESENT | WRITE | DIRTY
print(hex(pte), pte >> 12, bool(pte & PRESENT), bool(pte & USER), bool(pte & DIRTY))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0x5043 5 True False True"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Размер таблицы"}
      sub={"Почему таблица многоуровневая"}
      main={"Плоская таблица для 48 бит — 512 ГиБ на процесс; таблицы по 512 записей в 4 уровня почти не занимают места."}
    >
      <PyCode>{`va_bits, page_bits, pte = 48, 12, 8
pages = 2 ** (va_bits - page_bits)
print(pages, pages * pte // 2 ** 30, "ГиБ")
per_table = 2 ** page_bits // pte
print(per_table, "записей в таблице", (va_bits - page_bits) // 9, "уровня")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"68719476736 512 ГиБ\n512 записей в таблице 4 уровня"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Обход многоуровневой таблицы"}
      sub={"Четыре зависимых чтения"}
      main={"Каждый уровень — отдельное обращение к памяти; пустые ветви просто не создаются."}
    >
      <PyCode>{`root = {2: {5: {1: {3: 77}}}}      # индексы четырёх уровней → кадр

def walk(indexes):
    node = root
    for i in indexes:
        node = node.get(i)
        if node is None:
            return "page fault"
    return node

print(walk([2, 5, 1, 3]), walk([2, 5, 1, 4]), walk([0, 0, 0, 0]))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"77 page fault page fault"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"TLB"}
      sub={"Кэш трансляций"}
      main={"Несколько десятков последних переводов — и обход таблиц нужен лишь при промахе."}
    >
      <PyCode>{`from collections import OrderedDict

def tlb_sim(pages, size):
    tlb, hits = OrderedDict(), 0
    for p in pages:
        if p in tlb:
            hits += 1
            tlb.move_to_end(p)
        else:
            if len(tlb) == size:
                tlb.popitem(last=False)
            tlb[p] = True
    return hits

trace = [1, 2, 3] * 100
print(tlb_sim(trace, 4), tlb_sim(trace, 2), len(trace))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"297 0 300"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Подкачка по требованию"}
      sub={"Страница загружается при первом обращении"}
      main={"ОС читает страницу с диска, обновляет таблицу и повторяет команду — программа видит лишь паузу."}
    >
      <PyCode>{`resident, faults = set(), 0
for page in [0, 1, 0, 2, 1, 0, 3]:
    if page not in resident:
        faults += 1                  # ОС читает страницу с диска
        resident.add(page)
print(faults, sorted(resident))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"4 [0, 1, 2, 3]"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Выбор страницы для выгрузки"}
      sub={"FIFO и аномалия Биледи"}
      main={"У FIFO больше памяти может дать больше прерываний; LRU и «часы» ближе к идеалу."}
    >
      <PyCode>{`def fifo_faults(trace, frames):
    mem, faults = [], 0
    for p in trace:
        if p not in mem:
            faults += 1
            if len(mem) == frames:
                mem.pop(0)
            mem.append(p)
    return faults

trace = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
print(fifo_faults(trace, 3), fifo_faults(trace, 4))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"9 10"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Пробуксовка"}
      sub={"Рабочее множество не помещается"}
      main={"Цикл по 5 страницам при 4 кадрах — прерывание на каждое обращение; при 5 кадрах — только первые."}
    >
      <PyCode>{`def lru_faults(trace, frames):
    mem, faults = [], 0
    for p in trace:
        if p in mem:
            mem.remove(p)
        else:
            faults += 1
            if len(mem) == frames:
                mem.pop(0)
        mem.append(p)
    return faults

loop = [0, 1, 2, 3, 4] * 10
print(lru_faults(loop, 4), lru_faults(loop, 5))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"50 5"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Копирование при записи"}
      sub={"Общие кадры до первой записи"}
      main={"После fork кадры общие; копия делается только тому, кто пишет."}
    >
      <PyCode>{`memory = {1: "данные"}
parent = {0: 1}
child = dict(parent)               # fork: таблица копируется, кадры общие
print(parent[0] == child[0], len(memory))

def write(table, vpn, value):
    frame = table[vpn]
    if sum(f == frame for t in (parent, child) for f in t.values()) > 1:
        new = max(memory) + 1
        memory[new] = memory[frame]
        table[vpn] = frame = new
    memory[frame] = value

write(child, 0, "новые")
print(parent[0] != child[0], len(memory), memory[parent[0]], memory[child[0]])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"True 1\nTrue 2 данные новые"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Виртуальная память — защита, удобство и экономия; плата — перевод адресов, который скрывает TLB."}
    >
      <div className="s-grid2">
        {[["VPN → frame", "Перевод", "Таблицы страниц"], ["4 уровня", "Экономия", "Многоуровневые таблицы"], ["TLB", "Скорость", "Кэш переводов"], ["COW", "fork", "Копия при записи"]].map(([big, t, d]) => (
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
export const SLIDES_AR8 = {
  "14:8": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_AR8).
export const SLIDE_TITLES_AR8 = {
  "14:8": [
    "Виртуальная память",
    "Зачем нужна",
    "Страницы и кадры",
    "Таблица страниц",
    "Флаги страницы",
    "Размер таблицы",
    "Обход таблиц",
    "TLB",
    "Подкачка",
    "Замещение страниц",
    "Пробуксовка",
    "Copy-on-write",
    "Итоги",
  ],
};
