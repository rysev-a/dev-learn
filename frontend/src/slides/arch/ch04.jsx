// Слайды для «Архитектура компьютера», глава 4 — «Процессор: регистры и цикл команд».
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
      <span>АРХИТЕКТУРА КОМПЬЮТЕРА / ПРОЦЕССОР / ГЛАВА 4</span>
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
      title={"Как работает процессор"}
      sub={"Глава 4 · Процессор"}
      main={"Процессор снова и снова читает команду, разбирает её и выполняет — миллиарды раз в секунду."}
    >
      <div className="s-grid2">
        {[["R0 … R3", "Регистры", "Сверхбыстрая память внутри"], ["PC", "Счётчик команд", "Адрес следующей команды"], ["ALU", "Вычисления", "Операции и флаги"], ["JMP · JZ", "Переходы", "Ветвления и циклы"]].map(([big, t, d]) => (
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
      title={"Схема фон Неймана"}
      sub={"Программа — тоже данные"}
      main={"Команды и данные лежат в одной памяти; программу можно загрузить, заменить и даже написать другой программой."}
    >
      <PyCode>{`memory = [("LDI", "R0", 5), ("HLT",), 42]
print(memory[2], memory[0])
memory[0] = ("LDI", "R0", 7)   # программа — тоже данные
print(memory[0])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"42 ('LDI', 'R0', 5)\n('LDI', 'R0', 7)"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Регистры"}
      sub={"Память внутри процессора"}
      main={"Регистры читаются и пишутся за такт; есть общего назначения, счётчик команд и флаги."}
    >
      <PyCode>{`class CPU:
    def __init__(self):
        self.regs = {"R0": 0, "R1": 0, "R2": 0, "R3": 0}
        self.pc = 0                          # счётчик команд
        self.flags = {"Z": 0, "N": 0, "C": 0}

cpu = CPU()
cpu.regs["R1"] = 40
print(cpu.pc, cpu.regs["R1"], cpu.flags)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0 40 {'Z': 0, 'N': 0, 'C': 0}"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Формат команды"}
      sub={"Поля внутри слова"}
      main={"Код операции + номера регистров + число: поля упаковываются сдвигами и достаются масками."}
    >
      <PyCode>{`def pack(op, rd, rs, imm):
    return (op << 12) | (rd << 10) | (rs << 8) | imm

def unpack(word):
    return word >> 12, (word >> 10) & 3, (word >> 8) & 3, word & 0xFF

w = pack(0b0010, 1, 2, 0x2A)
print(format(w, "016b"), hex(w))
print(unpack(w))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0010011000101010 0x262a\n(2, 1, 2, 42)"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Цикл «выборка — декодирование — исполнение»"}
      sub={"Что делает процессор вечно"}
      main={"Прочитать команду, сдвинуть PC, разобрать, выполнить, записать результат — и снова."}
    >
      <PyCode>{`program = [("LDI", "R0", 7), ("LDI", "R1", 5), ("ADD", "R0", "R1"), ("HLT",)]
pc = 0
for step in range(4):
    ir = program[pc]            # выборка
    pc += 1                     # PC указывает на следующую
    print(step, "PC=%d" % pc, ir[0])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0 PC=1 LDI\n1 PC=2 LDI\n2 PC=3 ADD\n3 PC=4 HLT"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Процессор на питоне"}
      sub={"Четыре регистра и три команды"}
      main={"Уже три команды позволяют сложить числа; результат остаётся в регистре."}
    >
      <PyCode>{`def run(program):
    regs = {"R0": 0, "R1": 0, "R2": 0, "R3": 0}
    pc = 0
    while True:
        op, *args = program[pc]       # выборка и декодирование
        pc += 1
        if op == "LDI":
            regs[args[0]] = args[1]
        elif op == "ADD":
            regs[args[0]] += regs[args[1]]
        elif op == "HLT":
            return regs

print(run([("LDI", "R0", 2), ("LDI", "R1", 40), ("ADD", "R0", "R1"), ("HLT",)]))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'R0': 42, 'R1': 40, 'R2': 0, 'R3': 0}"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Флаги"}
      sub={"Как закончилась операция"}
      main={"Z — результат нулевой, N — отрицательный, C — перенос или заём, V — знаковое переполнение."}
    >
      <PyCode>{`def sub_flags(a, b):
    res = (a - b) & 0xFF
    return {"Z": int(res == 0), "N": res >> 7, "C": int(a < b)}

print(sub_flags(5, 5))
print(sub_flags(3, 5))
print(sub_flags(9, 4))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'Z': 1, 'N': 0, 'C': 0}\n{'Z': 0, 'N': 1, 'C': 1}\n{'Z': 0, 'N': 0, 'C': 0}"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"Переходы"}
      sub={"Ветвления и циклы"}
      main={"Переход — это запись нового адреса в PC; условный переход смотрит на флаг."}
    >
      <PyCode>{`def run(program):
    r = {"R0": 0, "R1": 0, "R2": 0}
    pc, z, steps = 0, 0, 0
    while program[pc][0] != "HLT":
        op, *a = program[pc]
        pc += 1
        steps += 1
        if op == "LDI":
            r[a[0]] = a[1]
        elif op in ("ADD", "SUB"):
            r[a[0]] += r[a[1]] if op == "ADD" else -r[a[1]]
            z = int(r[a[0]] == 0)
        elif op == "JNZ" and not z:
            pc = a[0]
    return r["R0"], steps

prog = [("LDI", "R0", 0), ("LDI", "R1", 5), ("LDI", "R2", 1),
        ("ADD", "R0", "R1"), ("SUB", "R1", "R2"), ("JNZ", 3), ("HLT",)]
print(run(prog))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"(15, 18)"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Устройство управления"}
      sub={"Код операции превращается в действие"}
      main={"Жёсткая логика быстра, микрокод гибок; в модели роль декодера играет таблица."}
    >
      <PyCode>{`def op_add(r, a): r[a[0]] += r[a[1]]
def op_sub(r, a): r[a[0]] -= r[a[1]]
def op_ldi(r, a): r[a[0]] = a[1]

TABLE = {"ADD": op_add, "SUB": op_sub, "LDI": op_ldi}

r = {"R0": 0, "R1": 0}
for op, *a in [("LDI", "R0", 10), ("LDI", "R1", 3), ("SUB", "R0", "R1")]:
    TABLE[op](r, a)
print(r)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"{'R0': 7, 'R1': 3}"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Такты и CPI"}
      sub={"Сколько времени занимает программа"}
      main={"Время = число команд × CPI ÷ частота. Три способа ускорить: меньше команд, меньше тактов, выше частота."}
    >
      <PyCode>{`cycles = {"LDI": 1, "ADD": 1, "LD": 3, "JNZ": 2}
trace = ["LDI", "LD", "ADD", "JNZ", "ADD", "JNZ"]
total = sum(cycles[op] for op in trace)
print(total, round(total / len(trace), 2))
print(round(total / 3, 2), "нс")   # 3 ГГц = 3 такта на наносекунду`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"10 1.67\n3.33 нс"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Шины и объём памяти"}
      sub={"Сколько адресов можно назвать"}
      main={"n линий адреса — 2ⁿ ячеек: поэтому 32-битным системам не хватило памяти."}
    >
      <PyCode>{`for bits in (8, 16, 32):
    print(bits, 2 ** bits, "байт")
print(2 ** 32 // 2 ** 30, "ГиБ")
print(2 ** 64 // 2 ** 60, "ЭиБ")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"8 256 байт\n16 65536 байт\n32 4294967296 байт\n4 ГиБ\n16 ЭиБ"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"ISA и микроархитектура"}
      sub={"Интерфейс и реализация"}
      main={"Одна и та же программа даёт тот же результат на разных реализациях, только за разное число тактов."}
    >
      <PyCode>{`program = ["LDI", "LDI", "ADD", "HLT"]
simple = {"LDI": 3, "ADD": 4, "HLT": 1}
fast = {"LDI": 1, "ADD": 1, "HLT": 1}
print(sum(simple[i] for i in program), sum(fast[i] for i in program))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"11 4"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Процессор — это регистры, АЛУ, устройство управления и бесконечный цикл команд."}
    >
      <div className="s-grid2">
        {[["fetch → exec", "Цикл команд", "Выборка, декодирование, исполнение"], ["Z N C V", "Флаги", "Основа условных переходов"], ["JMP · JZ", "Переходы", "Меняют PC"], ["CPI", "Производительность", "Команды × такты ÷ частота"]].map(([big, t, d]) => (
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
export const SLIDES_AR4 = {
  "14:4": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_AR4).
export const SLIDE_TITLES_AR4 = {
  "14:4": [
    "Как работает процессор",
    "Фон Нейман",
    "Регистры",
    "Формат команды",
    "Цикл команд",
    "Простой процессор",
    "Флаги",
    "Переходы",
    "Устройство управления",
    "Такты и CPI",
    "Шины",
    "ISA и микроархитектура",
    "Итоги",
  ],
};
