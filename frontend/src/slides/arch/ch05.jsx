// Слайды для «Архитектура компьютера», глава 5 — «Команды, стек и ассемблер».
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
      <span>АРХИТЕКТУРА КОМПЬЮТЕРА / ПРОЦЕССОР / ГЛАВА 5</span>
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
      title={"Язык процессора"}
      sub={"Глава 5 · Процессор"}
      main={"Набор команд — договор между железом и программой; ассемблер — его читаемая запись."}
    >
      <div className="s-grid2">
        {[["ISA", "Набор команд", "Что умеет процессор"], ["[R1 + 4]", "Адресация", "Откуда брать операнды"], ["CALL · RET", "Стек", "Функции и рекурсия"], ["loop:", "Ассемблер", "Имена и метки вместо чисел"]].map(([big, t, d]) => (
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
      title={"Что входит в ISA"}
      sub={"Регистры, команды, память"}
      main={"Число бит кода операции ограничивает число команд: n бит — 2ⁿ команд."}
    >
      <PyCode>{`for bits in (4, 6, 8):
    print(bits, "бит кода операции →", 2 ** bits, "команд")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"4 бит кода операции → 16 команд\n6 бит кода операции → 64 команд\n8 бит кода операции → 256 команд"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Классы команд"}
      sub={"Данные, арифметика, управление"}
      main={"В реальных программах много пересылок и переходов — их и ускоряют в первую очередь."}
    >
      <PyCode>{`from collections import Counter

CLASS = {"LDI": "данные", "MOV": "данные", "ADD": "арифметика",
         "SUB": "арифметика", "JNZ": "управление", "HLT": "управление"}
prog = ["LDI", "LDI", "ADD", "SUB", "JNZ", "HLT"]
print(Counter(CLASS[op] for op in prog))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Counter({'данные': 2, 'арифметика': 2, 'управление': 2})"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Режимы адресации"}
      sub={"Откуда берётся операнд"}
      main={"Число, регистр, адрес, адрес в регистре, база + смещение — так работают указатели и массивы."}
    >
      <PyCode>{`mem = [10, 20, 30, 40]
regs = {"R1": 2}

print(5)                          # непосредственная: число в команде
print(regs["R1"])                 # регистровая
print(mem[1])                     # прямая: адрес в команде
print(mem[regs["R1"]])            # косвенная через регистр
print(mem[1 + regs["R1"]])        # индексная: база + смещение`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"5\n2\n20\n30\n40"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Ассемблер"}
      sub={"Метки и два прохода"}
      main={"Первый проход запоминает адреса меток, второй подставляет их вместо имён."}
    >
      <PyCode>{`source = """
    LDI R0 0
    LDI R1 3
    LDI R2 1
loop:
    ADD R0 R1
    SUB R1 R2
    JNZ loop
    HLT
"""

def assemble(text):
    lines = [l.split(";")[0].strip() for l in text.splitlines()]
    labels, code = {}, []
    for l in filter(None, lines):
        if l.endswith(":"):
            labels[l[:-1]] = len(code)
        else:
            code.append(l.split())
    return [(op, *[labels[a] if a in labels else int(a) if a.isdigit() else a for a in args])
            for op, *args in code]

print(assemble(source))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[('LDI', 'R0', 0), ('LDI', 'R1', 3), ('LDI', 'R2', 1), ('ADD', 'R0', 'R1'), ('SUB', 'R1', 'R2'), ('JNZ', 3), ('HLT',)]"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Машинный код"}
      sub={"Мнемоники становятся числами"}
      main={"Команда — слово из полей; дизассемблер делает обратное преобразование."}
    >
      <PyCode>{`OPS = {"HLT": 0, "LDI": 1, "ADD": 3, "SUB": 4, "JNZ": 13}
REG = {"R0": 0, "R1": 1, "R2": 2, "R3": 3}

def encode(op, *a):
    if op == "LDI":
        return OPS[op] << 12 | REG[a[0]] << 10 | a[1]
    if op in ("ADD", "SUB"):
        return OPS[op] << 12 | REG[a[0]] << 10 | REG[a[1]] << 8
    if op == "JNZ":
        return OPS[op] << 12 | a[0]
    return OPS[op] << 12

ws = [encode("LDI", "R1", 5), encode("ADD", "R0", "R1"), encode("SUB", "R1", "R2"), encode("JNZ", 3), encode("HLT")]
print([format(w, "04x") for w in ws])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"['1405', '3100', '4600', 'd003', '0000']"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Стек"}
      sub={"Последним пришёл — первым вышел"}
      main={"Указатель стека хранит вершину; положить — уменьшить указатель и записать; взять — прочитать и увеличить."}
    >
      <PyCode>{`mem = [0] * 8
sp = len(mem)

def push(x):
    global sp
    sp -= 1
    mem[sp] = x

def pop():
    global sp
    x = mem[sp]
    sp += 1
    return x

push(1); push(2); push(3)
print(pop(), pop(), mem, sp)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3 2 [0, 0, 0, 0, 0, 3, 2, 1] 7"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"CALL и RET"}
      sub={"Вызов и возврат"}
      main={"CALL кладёт адрес возврата и прыгает; RET берёт адрес со стека — вложенность любой глубины."}
    >
      <PyCode>{`stack = []

def call(pc, target):
    stack.append(pc + 1)
    return target

def ret():
    return stack.pop()

pc = 10
pc = call(pc, 50); print(pc, stack)
pc = call(pc, 90); print(pc, stack)
pc = ret(); print(pc)
pc = ret(); print(pc)`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"50 [11]\n90 [11, 51]\n51\n11"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Кадр вызова и рекурсия"}
      sub={"Стек конечен"}
      main={"Каждый вызов занимает место на стеке; слишком глубокая рекурсия переполняет его."}
    >
      <PyCode>{`import sys

def depth(n):
    return 0 if n == 0 else 1 + depth(n - 1)

print(depth(500), sys.getrecursionlimit())
try:
    depth(10 ** 6)
except RecursionError:
    print("стек переполнен")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"500 1000\nстек переполнен"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"RISC и CISC"}
      sub={"Два подхода к набору команд"}
      main={"RISC — мало простых команд одной длины; CISC — богатые команды разной длины."}
    >
      <PyCode>{`risc = ["lw t0, b", "lw t1, c", "add t2, t0, t1", "sw t2, a"]   # a = b + c
cisc = ["mov eax, [b]", "add eax, [c]", "mov [a], eax"]
print(len(risc), len(cisc))
print("RISC: 4 байта на команду →", len(risc) * 4, "байт")`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"4 3\nRISC: 4 байта на команду → 16 байт"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Системные вызовы"}
      sub={"Граница между программой и ядром"}
      main={"Специальная команда переводит процессор в режим ядра и передаёт управление обработчику."}
    >
      <PyCode>{`SYSCALLS = {1: "write", 2: "exit"}

def syscall(num, arg):
    return f"ядро выполняет {SYSCALLS[num]}({arg!r})"

print(syscall(1, "привет"))
print(syscall(2, 0))`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"ядро выполняет write('привет')\nядро выполняет exit(0)"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"От выражения к командам"}
      sub={"Стековая машина"}
      main={"Обход дерева выражения снизу вверх даёт последовательность команд для стековой машины."}
    >
      <PyCode>{`import ast

OPS = {ast.Add: "ADD", ast.Sub: "SUB", ast.Mult: "MUL"}

def compile_expr(node):
    if isinstance(node, ast.Constant):
        return [("PUSH", node.value)]
    return compile_expr(node.left) + compile_expr(node.right) + [(OPS[type(node.op)],)]

code = compile_expr(ast.parse("(1 + 2) * 3", mode="eval").body)
print(code)

stack = []
for op, *a in code:
    if op == "PUSH":
        stack.append(a[0])
    else:
        y, x = stack.pop(), stack.pop()
        stack.append(x + y if op == "ADD" else x - y if op == "SUB" else x * y)
print(stack[-1])`}</PyCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[('PUSH', 1), ('PUSH', 2), ('ADD',), ('PUSH', 3), ('MUL',)]\n9"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Ассемблер, стек и вызовы — мост между языками высокого уровня и железом."}
    >
      <div className="s-grid2">
        {[["ISA", "Договор", "Регистры, команды, адресация"], ["asm → hex", "Ассемблер", "Метки и мнемоники → числа"], ["push · pop", "Стек", "Адреса возврата и кадры"], ["syscall", "Ядро", "Граница приложения и ОС"]].map(([big, t, d]) => (
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
export const SLIDES_AR5 = {
  "14:5": [
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

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_AR5).
export const SLIDE_TITLES_AR5 = {
  "14:5": [
    "Язык процессора",
    "ISA",
    "Классы команд",
    "Режимы адресации",
    "Ассемблер",
    "Машинный код",
    "Стек",
    "CALL и RET",
    "Кадры и рекурсия",
    "RISC и CISC",
    "Системные вызовы",
    "Компиляция выражения",
    "Итоги",
  ],
};
