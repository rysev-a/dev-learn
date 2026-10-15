// Слайды для «Архитектура компьютера», глава 6 — «Иерархия памяти и кэш».
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
      <span>АРХИТЕКТУРА КОМПЬЮТЕРА / ПАМЯТЬ И ПРОИЗВОДИТЕЛЬНОСТЬ / ГЛАВА 6</span>
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
      title={"Лестница памяти"}
      sub={"Глава 6 · Память и производительность"}
      main={"Между быстрым процессором и медленной памятью ставят слои кэша: маленькие, быстрые, с копиями нужных данных."}
    >
      <div className="s-grid2">
        {[["L1 · L2 · L3", "Иерархия", "Быстрее — меньше"], ["tag | index | off", "Адрес в кэше", "Три поля"], ["LRU · FIFO", "Замещение", "Что вытеснить"], ["AMAT", "Средний доступ", "Попадание + промахи"]].map(([big, t, d]) => (
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
      title={"Задержки уровней"}
      sub={"Сотни тактов против единиц"}
      main={"Обращение к ОЗУ в сотни раз медленнее регистра — отсюда необходимость кэша."}
    >
      <PyCode>{`levels = [("L1", 1), ("L2", 4), ("L3", 15), ("RAM", 80), ("SSD", 100_000)]
for name, ns in levels:
    print(name, ns, "нс", ns * 3, "тактов")   # 3 ГГц = 3 такта на нс`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"L1 1 нс 3 тактов\nL2 4 нс 12 тактов\nL3 15 нс 45 тактов\nRAM 80 нс 240 тактов\nSSD 100000 нс 300000 тактов"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"SRAM и DRAM"}
      sub={"Из чего сделана память"}
      main={"SRAM — шесть транзисторов на бит, быстрая и дорогая; DRAM — транзистор и конденсатор, плотная, но медленная."}
    >
      <PyCode>{`sram_bit = 6          # транзисторов на бит
dram_bit = 1          # транзистор + конденсатор
mib = 8 * 2 ** 20     # бит в одном мебибайте
print(sram_bit * mib, dram_bit * mib)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"50331648 8388608"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Локальность"}
      sub={"Временная и пространственная"}
      main={"Соседние адреса читаются вместе: последовательный обход затрагивает в разы меньше кэш-строк."}
    >
      <PyCode>{`LINE = 64

def lines(addrs):
    return len({a // LINE for a in addrs})

seq = range(0, 1024 * 4, 4)          # 1024 числа подряд
strided = range(0, 1024 * 64, 64)    # 1024 чтения через строку
print(lines(seq), lines(strided))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"64 1024"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Адрес: тег, индекс, смещение"}
      sub={"Как кэш ищет строку"}
      main={"Смещение — байт в строке, индекс — место в кэше, тег подтверждает, что строка та самая."}
    >
      <PyCode>{`def split(addr, offset_bits=6, index_bits=4):
    offset = addr & (2 ** offset_bits - 1)
    index = (addr >> offset_bits) & (2 ** index_bits - 1)
    tag = addr >> (offset_bits + index_bits)
    return tag, index, offset

print(split(0x12345))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(72, 13, 5)"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Кэш с прямым отображением"}
      sub={"Одно место для каждого блока"}
      main={"Быстро проверять, но блоки с одинаковым индексом вытесняют друг друга — конфликтные промахи."}
    >
      <PyCode>{`class DirectCache:
    def __init__(self, lines=4, size=16):
        self.lines, self.size = lines, size
        self.tags = [None] * lines
        self.hits = self.misses = 0

    def access(self, addr):
        block = addr // self.size
        index, tag = block % self.lines, block // self.lines
        if self.tags[index] == tag:
            self.hits += 1
        else:
            self.misses += 1
            self.tags[index] = tag

c = DirectCache()
for a in [0, 4, 8, 16, 0, 64, 0]:
    c.access(a)
print(c.hits, c.misses)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3 4"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Наборно-ассоциативный кэш"}
      sub={"Несколько мест в наборе"}
      main={"Индекс выбирает набор, блок может лежать в любой строке набора — конфликтов меньше."}
    >
      <PyCode>{`def simulate(trace, sets, ways, size=16):
    cache = [[] for _ in range(sets)]      # LRU: самый старый — первый
    hits = 0
    for addr in trace:
        block = addr // size
        s = cache[block % sets]
        if block in s:
            hits += 1
            s.remove(block)
        elif len(s) == ways:
            s.pop(0)
        s.append(block)
    return hits

trace = [0, 64, 0, 64, 0, 64]
print(simulate(trace, 4, 1), simulate(trace, 2, 2))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0 4"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Политики замещения"}
      sub={"Что выбросить из набора"}
      main={"LRU держит недавно использованное; FIFO выбрасывает самое старое по времени загрузки."}
    >
      <PyCode>{`def run(trace, cap, policy):
    cache, hits = [], 0
    for b in trace:
        if b in cache:
            hits += 1
            if policy == "LRU":
                cache.remove(b)
                cache.append(b)
        else:
            if len(cache) == cap:
                cache.pop(0)
            cache.append(b)
    return hits

trace = [1, 2, 3, 1, 4, 1, 5, 1, 6, 1]
print(run(trace, 3, "LRU"), run(trace, 3, "FIFO"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"4 3"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Политики записи"}
      sub={"Write-through и write-back"}
      main={"Отложенная запись отправляет в память только вытесняемые «грязные» строки — записей меньше."}
    >
      <PyCode>{`writes = [5, 5, 5, 5, 9, 9]     # адреса, в которые пишет программа
print("write-through:", len(writes), "записей в память")
dirty = set(writes)
print("write-back:", len(dirty), "записи при вытеснении")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"write-through: 6 записей в память\nwrite-back: 2 записи при вытеснении"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Среднее время доступа"}
      sub={"AMAT"}
      main={"AMAT = время попадания + доля промахов × штраф; для уровней формула вкладывается."}
    >
      <PyCode>{`def amat(hit, miss_rate, penalty):
    return hit + miss_rate * penalty

l2 = amat(10, 0.2, 200)     # 10 + 0.2 × 200 = 50
l1 = amat(1, 0.05, l2)      # 1 + 0.05 × 50 = 3.5
print(l2, l1)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"50.0 3.5"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Порядок обхода массива"}
      sub={"По строкам и по столбцам"}
      main={"Обход по строкам использует каждую загруженную строку кэша целиком; по столбцам — только одну ячейку."}
    >
      <PyCode>{`def misses(n, order, lines=64, size=64, elem=4):
    tags, m = [None] * lines, 0
    for a in range(n):
        for b in range(n):
            i, j = (a, b) if order == "row" else (b, a)
            blk = (i * n + j) * elem // size
            if tags[blk % lines] != blk // lines:
                tags[blk % lines] = blk // lines
                m += 1
    return m

print(misses(64, "row"), misses(64, "col"))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"256 4096"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Кэш в программах"}
      sub={"lru_cache и не только"}
      main={"Везде те же вопросы: что хранить, сколько, что выбрасывать и когда данные устарели."}
    >
      <PyCode>{`from functools import lru_cache

@lru_cache(maxsize=2)
def square(x):
    return x * x

for x in [1, 2, 1, 3, 1, 2]:
    square(x)
print(square.cache_info())`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"CacheInfo(hits=2, misses=4, maxsize=2, currsize=2)"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Кэш работает благодаря локальности; пишите код так, чтобы обращаться к соседним адресам."}
    >
      <div className="s-grid2">
        {[["локальность", "Основа кэша", "Время и пространство"], ["tag·index·off", "Адрес", "Попадание или промах"], ["ways", "Ассоциативность", "Меньше конфликтов"], ["AMAT", "Оценка", "hit + miss × штраф"]].map(([big, t, d]) => (
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
export const SLIDES_AR6 = {
  "14:6": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_AR6).
export const SLIDE_TITLES_AR6 = {
  "14:6": [
    "Иерархия памяти",
    "Задержки",
    "SRAM и DRAM",
    "Локальность",
    "Тег, индекс, смещение",
    "Прямое отображение",
    "Ассоциативность",
    "LRU и FIFO",
    "Политики записи",
    "AMAT",
    "Строки и столбцы",
    "Кэш в программах",
    "Итоги",
  ],
};
