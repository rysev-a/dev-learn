// Выгрузка лаборатории RISC-V (книга 14, главы 16 и 17) для крейта shared-rs/riscvlab.
//
// Пишет два файла:
//  1) выгрузка упражнений (аргумент 1, по умолчанию riscv-export.json): условия, подсказки, заготовки, эталонные программы,
//     данные заданий и проверки в виде данных — их читает `cargo run --release --bin import -- <выгрузка> <каталог данных>`;
//  2) «золотые» результаты прежней реализации на TypeScript (аргумент 2, по умолчанию shared-rs/riscvlab/tests/golden.json):
//     декодер, ассемблер, исполнение и трассы, вердикты по множеству программ — с ними сверяются тесты Rust (бит в бит).
//
// Проверки упражнений в TypeScript — замыкания, поэтому вид проверки каждой задачи записан здесь вручную (таблица CHECKS), а
// ожидаемые значения берутся из прогона эталона и сверяются с самой проверкой (эталон проходит, искажённый результат — нет).
// Запуск: cd frontend && node scripts/riscv-export.mjs [выгрузка.json] [golden.json]
import { build } from "esbuild";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "..");
const outExport = path.resolve(process.argv[2] || "riscv-export.json");
const outGolden = path.resolve(process.argv[3] || path.resolve(root, "../shared-rs/riscvlab/tests/golden.json"));
const lab = path.join(root, "src/lab/riscv");

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "riscv-export-"));
const entryFile = path.join(tmp, "entry.ts");
fs.writeFileSync(
  entryFile,
  `
export * as isa from ${JSON.stringify(path.join(lab, "rv-isa"))};
export * as asm from ${JSON.stringify(path.join(lab, "rv-asm"))};
export * as machine from ${JSON.stringify(path.join(lab, "rv-machine"))};
export * as tasks from ${JSON.stringify(path.join(lab, "rv-tasks"))};
export * as real from ${JSON.stringify(path.join(lab, "rv-real-tasks"))};
export * as project from ${JSON.stringify(path.join(lab, "rv-project"))};
export * as zip from ${JSON.stringify(path.join(lab, "zip"))};
`,
);
const bundle = path.join(tmp, "entry.mjs");
await build({ entryPoints: [entryFile], bundle: true, platform: "node", format: "esm", outfile: bundle, logLevel: "error" });
const { isa, asm, machine, tasks, real, project, zip } = await import(pathToFileURL(bundle).href);

const RUN_LIMIT = 200_000;
const hex = (n) => (n >>> 0).toString(16).padStart(8, "0");

/* ============================================================
   Упражнения: проверки как данные
   ============================================================ */

const cstr = (mem, a) => {
  let s = "";
  while (a < mem.length && mem[a] !== 0) s += String.fromCharCode(mem[a++] ?? 0);
  return s;
};
const wordAt = (mem, a) => (mem[a] ?? 0) | ((mem[a + 1] ?? 0) << 8) | ((mem[a + 2] ?? 0) << 16) | ((mem[a + 3] ?? 0) << 24);

/** Вид проверки каждой задачи; значения берутся из прогона эталона (`v` — вид машины, `sym` — метки). */
const CHECKS = {
  "uart-hi": (v) => ({ kind: "uart", expected: v.uart }),
  "uart-string": (v) => ({ kind: "uart", expected: v.uart }),
  leds: (v) => ({ kind: "leds", expected: v.leds }),
  "switches-invert": (v) => ({ kind: "leds", expected: v.leds, bad_suffix: " — инверсия 1011 0010" }),
  "sum-100": (v) => ({ kind: "reg", reg: 10, expected: v.regs[10] | 0 }),
  upper: (v, sym) => ({ kind: "mem_cstr", symbol: "text", expected: cstr(v.mem, sym.text) }),
  factorial: (v) => ({ kind: "all", checks: [{ kind: "reg", reg: 10, expected: v.regs[10] | 0, ok: "" }, { kind: "stack_returned" }] }),
  "sort-words": (v, sym) => ({
    kind: "mem_words",
    symbol: "arr",
    expected: Array.from({ length: 8 }, (_, i) => wordAt(v.mem, sym.arr + 4 * i)),
  }),
  "timer-blink": () => ({ kind: "blink", toggles: 8, min_gap: 200 }),
};
for (const id of ["real-hello", "real-print-uint", "real-fizzbuzz", "real-fib", "real-sort-print", "real-exit-code"]) {
  CHECKS[id] = (v) => ({ kind: "run", stdout: v.uart, code: v.exitCode | 0 });
}

function runTask(t, program) {
  const a = asm.assemble(tasks.fullSource(program, t));
  if (a.errors.length) return { a, v: null, m: null };
  const m = new machine.RvMachine(a.image, { switches: t.switches, entry: a.entry });
  m.run(RUN_LIMIT);
  return { a, v: m.view(), m };
}

/** Вердикт прежней реализации (то, что показывает интерфейс). */
function tsVerdict(t, program) {
  const { a, v } = runTask(t, program);
  if (!v) return { ok: false, outcome: "asm_errors", errors: a.errors };
  if (v.error) return { ok: false, outcome: "fault", message: v.error, steps: v.steps };
  const r = t.check(v, a.symbols);
  return { ok: r.ok, outcome: r.ok ? "passed" : "wrong", message: r.message, steps: v.steps };
}

function exportTask(t, profile) {
  const { a, v } = runTask(t, t.solution);
  if (!v || v.error || !v.halted) throw new Error(`эталон ${t.id} не доходит до остановки`);
  const res = t.check(v, a.symbols);
  if (!res.ok) throw new Error(`эталон ${t.id} не проходит проверку: ${res.message}`);
  const make = CHECKS[t.id];
  if (!make) throw new Error(`нет описания проверки для ${t.id}`);
  const check = make(v, a.symbols);
  // сообщение об успехе берём у самой проверки; у внутренних проверок оно пустое
  if (check.kind !== "stack_returned" && check.kind !== "all") check.ok = res.message;
  if (check.kind === "all") check.ok = res.message;
  return {
    id: t.id,
    title: t.title,
    text: t.text,
    hint: t.hint,
    starter: t.starter,
    solution: t.solution,
    data: t.data,
    switches: t.switches ?? 0,
    max_steps: t.maxSteps ?? RUN_LIMIT,
    check,
  };
}

const exportData = {
  version: 1,
  chapters: [
    { book: 14, chapter: 16, profile: "board", tasks: tasks.RV_TASKS.map((t) => exportTask(t, "board")) },
    { book: 14, chapter: 17, profile: "linux", tasks: real.REAL_TASKS.map((t) => exportTask(t, "linux")) },
  ],
};
fs.mkdirSync(path.dirname(outExport), { recursive: true });
fs.writeFileSync(outExport, JSON.stringify(exportData, null, 1) + "\n");

/* ============================================================
   Золотые результаты
   ============================================================ */

const golden = { version: 1 };

/* ---------- таблица команд ---------- */
golden.isa = {
  abi: [...isa.ABI_NAMES],
  ops: isa.OPS.map((o) => ({ mnemonic: o.mnemonic, fmt: o.fmt, opcode: o.opcode, f3: o.f3 ?? null, f7: o.f7 ?? null, ext: o.ext, meaning: o.meaning, example: o.example })),
  pseudo: isa.PSEUDO.map((p) => ({ example: p.example, becomes: p.becomes })),
  mmio: machine.MMIO_MAP.map((m) => ({ name: m.name, addr: m.addr, note: m.note })),
  reg_names: ["x0", "x5", "X7", " t0 ", "FP", "fp", "Zero", "x31", "x32", "x01", "x", "x-1", "sp", "s11", "s12", "a8", "t6", "T6", ""].map((n) => ({
    name: n,
    num: isa.regNum(n) ?? null,
  })),
};

/* ---------- декодер и дизассемблер ---------- */
let seed = 0x1234abcd;
const rnd = () => {
  seed ^= seed << 13;
  seed >>>= 0;
  seed ^= seed >>> 17;
  seed ^= seed << 5;
  seed >>>= 0;
  return seed;
};
const pick = (arr) => arr[rnd() % arr.length];

const words = new Set();
for (let i = 0; i < 1500; i++) words.add(rnd());
for (const o of isa.OPS) {
  for (let k = 0; k < 12; k++) {
    // слово с «правильными» кодом, f3 и f7 и случайными остальными битами
    let w = rnd();
    w = (w & ~0x7f) | o.opcode;
    if (o.f3 !== undefined) w = (w & ~(7 << 12)) | (o.f3 << 12);
    if (o.f7 !== undefined && (o.fmt === "R" || o.fmt === "SH")) w = (w & ~(0x7f << 25)) | (o.f7 << 25);
    words.add(w >>> 0);
  }
}
for (const w of [0, 0xffffffff, isa.ECALL, isa.EBREAK, 0x00000073 | (1 << 7), 0x00100073 | (1 << 15), 0x80000000, 0x7fffffff]) words.add(w >>> 0);

const fieldsView = (f) => ({ fmt: f.fmt, fields: f.fields.map((x) => ({ name: x.name, bits: x.bits, cls: x.cls })) });
golden.decode = [...words].map((w) => {
  const d = isa.decode(w);
  return {
    word: w,
    op: d.op?.mnemonic ?? null,
    rd: d.rd,
    rs1: d.rs1,
    rs2: d.rs2,
    imm: d.imm,
    dis: isa.disassemble(w),
    fields: fieldsView(isa.fieldsOf(w)),
  };
});

/* ---------- ассемблер ---------- */
const fnv = (bytes) => {
  let h = 0x811c9dc5;
  for (const b of bytes) {
    h ^= b;
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h >>> 0;
};
const asmView = (r) => ({
  errors: r.errors.map((e) => ({ line: e.line, message: e.message })),
  text_size: r.textSize,
  data_size: r.dataSize,
  entry: r.entry,
  symbols: r.symbols,
  lines: r.lines.map((l) => ({ line: l.line, addr: l.addr, word: l.word, text: l.text, pseudo: l.pseudo })),
  image_hash: fnv(r.image),
});

/** Короткие программы: возможности ассемблера и все виды ошибок. */
const SNIPPETS = {
  empty: "",
  comments_only: "# ничего\n; и это\n// и это\n",
  basic: "start:\n  addi a0, zero, 5\n  add a1, a0, a0\n  ebreak\n",
  upper_case: "  ADDI A0, ZERO, 5\n  Add a1, A0, a0\n  EBREAK\n",
  regs_forms: "  add x1, x2, x3\n  add fp, s0, x31\n  add t6, t5, T4\n",
  pseudo_all:
    "top:\n  nop\n  mv a0, a1\n  not a0, a1\n  neg a0, a1\n  seqz a0, a1\n  snez a0, a1\n  j top\n  jal top\n  jr a0\n  ret\n  beqz a0, top\n  bnez a0, top\n  blez a0, top\n  bgez a0, top\n  bltz a0, top\n  bgtz a0, top\n  bgt a0, a1, top\n  ble a0, a1, top\n  bgtu a0, a1, top\n  bleu a0, a1, top\n  call top\n  tail top\n  la a0, top\n",
  li_values:
    "  li a0, 0\n  li a0, 2047\n  li a0, 2048\n  li a0, -2048\n  li a0, -2049\n  li a0, 0x12345000\n  li a0, 0x12345678\n  li a0, 0xFFFFFFFF\n  li a0, 0x7fffffff\n  li a0, -0x80000000\n  li a0, 0x80000000\n  li a0, 4096\n  li a0, 0xfffff800\n  li a0, 0x7ff\n  li a0, 'A'\n  li a0, 1+2\n  li a0, 100-1\n",
  li_too_big: "  li a0, 0x100000000\n  li a0, -0x80000001\n",
  li_label: "main:\n  li a0, main\n",
  la_forward: "  la a0, later\n  la a1, later\n  ebreak\nlater:\n  nop\n",
  call_far: "  call f\n  ebreak\n  .space 3000\nf:\n  ret\n",
  branches: "a:\n  beq a0, a1, b\n  bne a0, a1, a\n  blt a0, a1, b\n  bge a0, a1, a\n  bltu a0, a1, b\nb:\n  bgeu a0, a1, a\n",
  branch_numeric: "  beq a0, a1, 8\n  beq a0, a1, -4\n  beq a0, a1, 3\n  jal ra, 100\n  jal 6\n",
  branch_far: "start:\n  beq a0, a1, end\n  .space 5000\nend:\n  nop\n",
  jal_forms: "f:\n  jal ra, f\n  jal f\n  j f\n  jal\n  jal a0, f, 3\n  j\n",
  jalr_forms: "  jalr ra, 0(t0)\n  jalr t0\n  jalr ra, t0, 4\n  jalr ra, 4 (t0)\n  jalr ra, (t0)\n  jalr ra, t0\n  jalr\n",
  loads_stores:
    "  lw a0, 4(a1)\n  lw a0, (a1)\n  lw a0, -4(sp)\n  lb a0, 0(a1)\n  lbu a0, 1(a1)\n  lh a0, 2 (a1)\n  lhu a0, 2( a1 )\n  sw a0, 8(sp)\n  sb a0, 0(t0)\n  sh a0, 2(t0)\n",
  mem_errors: "  lw a0, 4\n  lw a0, 4(a1\n  lw a0, 5000(a1)\n  lw a0, 4(zz)\n  sw a0\n  sw a0, 0(a1), 4\n  lw a0, )(\n  lw a0, 4()\n  lw a0, 4( )\n  lw a0, a(b(c)\n",
  shifts: "  slli a0, a1, 0\n  slli a0, a1, 31\n  slli a0, a1, 32\n  srli a0, a1, -1\n  srai a0, a1, 5\n  sll a0, a1, a2\n",
  immediates: "  addi a0, a0, 2047\n  addi a0, a0, 2048\n  addi a0, a0, -2048\n  addi a0, a0, -2049\n  andi a0, a0, 0xff\n  xori a0, a0, -1\n  ori a0, a0, 0b101\n  slti a0, a0, 'x'\n",
  lui_auipc: "  lui a0, 0x12345\n  lui a0, 0xfffff\n  lui a0, 0x100000\n  lui a0, -1\n  lui a0, -0x80000\n  lui a0, -0x80001\n  auipc a0, 1\n",
  m_ext: "  mul a0, a1, a2\n  mulh a0, a1, a2\n  mulhsu a0, a1, a2\n  mulhu a0, a1, a2\n  div a0, a1, a2\n  divu a0, a1, a2\n  rem a0, a1, a2\n  remu a0, a1, a2\n",
  hi_lo: "  lui a0, %hi(var)\n  addi a0, a0, %lo(var)\n  lw a1, %lo(var)(a0)\n  .data\nvar:\n  .word 7\n",
  hi_lo_numbers: "  lui a0, %hi(0x12345fff)\n  addi a0, a0, %lo(0x12345fff)\n  lui a0, %hi(-1)\n  addi a0, a0, %lo(0xfff)\n  lui a0, %hi()\n  addi a0, a0, %lo(0x800)\n",
  equ: "  .equ N, 10\n  .set M, N+5\n  li a0, N\n  li a1, M\n  li a2, K\n  .equ K, 3\n  .equ 5, 7\n  .equ X\n  .equ Y, 1, 2\n  .equ Z, nolabel\n",
  data_all:
    "  .data\nb:\n  .byte 1, 2, 0xff, -1, 'a'\nh:\n  .half 0x1234, -2\n  .short 7\nw:\n  .word 0xdeadbeef, -1, b, h+2, w-b\ns:\n  .ascii \"abc\"\n  .asciz \"de\\n\\t\\\\\\\"\"\n  .string \"x\", \"y\"\n  .space 5\n  .zero 3\n  .skip 2\n  .align 2\n  .balign 8\nend:\n  .word end\n",
  data_errors: "  .data\n  .byte\n  .word nolabel\n  .ascii abc\n  .ascii \"abc\n  .space\n  .space -1\n  .space x\n  .align\n  .align -1\n  .balign 0\n  .foo 1\n  .word 1 +\n  .byte 'ab'\n  .byte '\\q'\n",
  strings_special:
    "  .data\na:\n  .asciz \"é Ж\"\nb:\n  .asciz \"😀\"\nc:\n  .asciz \"a#b;c//d\"\nd:\n  .asciz \"\\x\\q\\0\"\ne:\n  .ascii \"\" \"z\"\n",
  char_literals: "  li a0, 'a'\n  li a0, '\\n'\n  li a0, '\\''\n  li a0, '\\\\'\n  li a0, ' '\n  li a0, '+'\n  li a0, '-'\n  li a0, 'a'+1\n  li a0, '😀'\n  li a0, 'ab'\n  li a0, ''\n",
  expressions:
    "  .data\nx:\n  .word 1+2, 10-3, 5 - 2, - 5, 5 -, +5, 1 + + 2, 0b1010, 0B11, 0X1f, 0xZ, 0x, 12ab, a b\n",
  expression_labels: "  .data\nx:\n  .word x, x+4, y-x, x+nolabel\ny:\n  .word 0\n",
  duplicate_labels: "a:\na:\n  nop\nb: b: nop\n",
  labels_forms: "one: two: nop\nthree :\n  nop\n  four:nop\n",
  cyrillic: "метка:\n  j метка\nЁлка_2:\n  la a0, Ёлка_2\n  .equ Размер, 4\n  li a0, Размер\n",
  idents: ".x:\n  nop\n$y:\n  nop\n_z9:\n  j _z9\n9bad:\n  nop\n",
  unknown: "  foo a0, a1\n  Bar\n  addx a0, a0, a0\n",
  operand_counts: "  add a0, a1\n  addi a0, a1\n  lw a0\n  nop a0\n  ret a0\n  ebreak a0\n  mv a0\n  not a0, a1, a2\n  li a0\n  la a0\n  call a, b\n  beqz a0\n  bgt a0, a1\n  lui a0\n  jalr a0, a1, a2, a3\n  ecall 1\n",
  bad_registers: "  add a0, a1, a9\n  add q0, a1, a2\n  mv a0, x32\n  lw a0, 0(x32)\n  addi , a0, 1\n  add a0, , a2\n  lui 5, 5\n",
  bad_numbers: "  addi a0, a0, abc\n  addi a0, a0, 1+\n  addi a0, a0, 1.5\n  addi a0, a0, 0x\n  addi a0, a0, (1)\n  addi a0, a0, %hi(\n  addi a0, a0, %hi(1\n  addi a0, a0, %lo(1)+2\n",
  wrong_section: "  .data\n  addi a0, a0, 1\n  .text\n  addi a0, a0, 1\n",
  sections: "  .section .text\n  nop\n  .section .rodata\nr:\n  .word 1\n  .section .data\nd:\n  .word 2\n  .bss\nz:\n  .space 8\n  .text\n  nop\n  .globl _start\n  .type f, @function\n  .size f, 4\n  .option norvc\n  .attribute arch, \"rv32im\"\n  .file \"a.s\"\n",
  entry_start: "  nop\n  .globl _start\n_start:\n  nop\n  ebreak\n",
  text_too_long: "  .space 5000\n  nop\n",
  data_too_big: "  .data\n  .space 3500\n",
  align_text: "  nop\n  .align 4\n  nop\n  .balign 8\n  nop\nx:\n  .word x\n",
  data_in_text: "  .word 1, 2\nlab:\n  .byte 3\n  .align 2\n  nop\n  .half 0\n",
  crlf: "start:\r\n  nop\r\n  j start\r\n",
  lone_cr: "  nop\r  nop\n",
  whitespace: "\tnop\t# tab\n\u00a0nop\n  nop\u00a0\n\u3000nop\n",
  comments_quotes: "  .data\n  .asciz \"# not a comment\"  # real comment\n  .ascii \"a\\\"b\" ; c\n  .byte ';' \n  .byte '#'\n",
  mnemonic_directive_case: "  .TEXT\n  .WORD 1\n  .Data\n  .WORD 2\n",
  forward_equ_li: "  li a0, LATER\n  .equ LATER, 5\n",
  long_label_chain: "a: b: c: d: nop\n  j a\n  j d\n",
  jump_label_as_expression: "start:\n  nop\n  j start+4\n  j start-4\n  beq a0, a0, start+8\n  la a0, start+4\n",
  big_hex: "  .data\n  .word 0xffffffff, 0x1ffffffff, 4294967296, -4294967297\n  .byte 256, 257, -129\n  .half 65536, 65537\n",
  deep_parens: "  lw a0, (4)(a1)\n  lw a0, 4(a1)(a2)\n  lw a0, 4 ( a1 ) \n",
  space_forms: "  .data\na:\n  .space 0\n  .space 0x10\nb:\n  .space 'a'\n",
  empty_operands: "  .word\n  .word ,\n  .word 1,\n  .byte 1,,2\n",
};

golden.asm = Object.entries(SNIPPETS).map(([name, source]) => ({ name, source, result: asmView(asm.assemble(source)) }));

/* ---------- ассемблер: «суп» из случайных кусков (проверка сообщений на мусоре) ---------- */
{
  const mnems = [...isa.OPS.map((o) => o.mnemonic), ...isa.PSEUDO.map((p) => p.example.split(" ")[0]), "foo", "ADD", "Li", ".word", ".byte", ".half", ".equ", ".ascii", ".asciz", ".space", ".align", ".balign", ".data", ".text", ".bar", ".section", ".globl"];
  const regsV = ["a0", "a1", "t0", "sp", "ra", "zero", "x5", "x31", "fp", "s11", "q1", "x32", "A0", "", "a0 a1"];
  const nums = ["0", "1", "-1", "5", "2047", "2048", "-2048", "-2049", "0xff", "0x7fffffff", "0xffffffff", "0x100000000", "'a'", "'\\n'", "1+2", "3 - 1", "- 4", "7 -", "%hi(lab)", "%lo(lab)", "%hi(0x12345678)", "lab", "lab+4", "other-lab", "nolabel", "4(sp)", "(a0)", "-8(a1)", "0(", "(", ")", "\"str\"", "\"a\\n\"", "\"unterminated", "x", "1.5", "0b11", "0x", "31", "32", "4096", "-4"];
  const sep = [", ", ",", " , ", " "];
  const lines = [];
  for (let n = 0; n < 220; n++) {
    const prog = [];
    const k = 3 + (rnd() % 6);
    for (let i = 0; i < k; i++) {
      let line = "";
      if (rnd() % 5 === 0) line += pick(["lab", "other", "lab", "x1", "метка"]) + ": ";
      line += pick(mnems);
      const nops = rnd() % 5;
      const ops = [];
      for (let j = 0; j < nops; j++) ops.push(rnd() % 2 ? pick(regsV) : pick(nums));
      let body = "";
      ops.forEach((o, j) => (body += (j ? pick(sep) : " ") + o));
      line += body;
      if (rnd() % 8 === 0) line += " # коммент";
      prog.push(line);
    }
    lines.push(prog.join("\n") + "\n");
  }
  lines.forEach((source, n) => golden.asm.push({ name: `soup:${n}`, source, result: asmView(asm.assemble(source)) }));
}

/* ---------- ассемблер: почти верные программы со случайной порчей одного операнда ---------- */
{
  const R = ["a0", "a1", "t0", "sp", "ra", "zero", "x5", "x31", "fp", "s11", "t6"];
  const N = ["0", "1", "-1", "5", "100", "2047", "-2048", "0xff", "'a'", "N", "N+1", "%lo(lab)", "0b101", "31"];
  const L = ["lab", "other", "back", "lab+4", "8", "-4", "back-4"];
  const JUNK = ["", "zz", "x32", "2048", "-2049", "0x", "1+", "lab(", "(a0)", "%hi(", "\"s\"", "1.5", "a0 a1", "other-", "'ab'", "4096"];
  const r = () => pick(R);
  const n = () => pick(N);
  const l = () => pick(L);
  const mem = () => pick(["0(a0)", "4(sp)", "-4(t0)", "(a1)", "8 (a0)", "N(a1)", "%lo(lab)(a0)", "2047(sp)"]);
  const forms = [];
  for (const o of isa.OPS) {
    const m = o.mnemonic;
    if (o.fmt === "R") forms.push(() => [m, r(), r(), r()]);
    else if (o.fmt === "I") forms.push(() => [m, r(), r(), n()]);
    else if (o.fmt === "SH") forms.push(() => [m, r(), r(), String(rnd() % 33)]);
    else if (o.fmt === "L" || o.fmt === "S") forms.push(() => [m, r(), mem()]);
    else if (o.fmt === "B") forms.push(() => [m, r(), r(), l()]);
    else if (o.fmt === "U") forms.push(() => [m, r(), pick(["0x12345", "1", "%hi(lab)", "0xfffff", "-1", "N"])]);
    else if (o.fmt === "J") forms.push(() => [m, r(), l()]);
    else if (o.fmt === "JR") forms.push(() => pick([[m, r(), mem()], [m, r(), r(), n()], [m, r()]]));
    else forms.push(() => [m]);
  }
  for (const m of ["nop", "ret"]) forms.push(() => [m]);
  for (const m of ["mv", "not", "neg", "seqz", "snez"]) forms.push(() => [m, r(), r()]);
  forms.push(() => ["li", r(), pick(["0", "5", "4096", "0x12345678", "0xffffffff", "-2049", "N", "'x'", "100000"])]);
  forms.push(() => ["la", r(), l()]);
  forms.push(() => ["call", l()], () => ["tail", l()], () => ["j", l()], () => ["jal", l()], () => ["jr", r()]);
  for (const m of ["beqz", "bnez", "blez", "bgez", "bltz", "bgtz"]) forms.push(() => [m, r(), l()]);
  for (const m of ["bgt", "ble", "bgtu", "bleu"]) forms.push(() => [m, r(), r(), l()]);
  const dirs = [
    () => ["  .equ N, " + pick(["3", "0x10", "'a'", "N", "lab"])],
    () => ["  .word " + [n(), l(), n()].join(", ")],
    () => ["  .byte " + [n(), n()].join(", ")],
    () => ["  .half " + n()],
    () => ["  .asciz " + pick(['"hi"', '"a\\tb"', "hi", '"x\\"y"'])],
    () => ["  .space " + pick(["4", "0", "-1", "N", "lab"])],
    () => ["  .align " + pick(["2", "0", "3", "-1"])],
    () => ["  .data"],
    () => ["  .text"],
  ];
  const fmtLine = (parts) => {
    if (parts.length === 1 && parts[0].startsWith("  .")) return parts[0];
    return "  " + parts[0] + (parts.length > 1 ? " " + parts.slice(1).join(pick([", ", ", ", ","])) : "");
  };
  const progs = [];
  for (let c = 0; c < 260; c++) {
    const src = [".equ N, 7", "lab:", "back:"];
    const k = 4 + (rnd() % 8);
    for (let i = 0; i < k; i++) {
      const parts = rnd() % 12 === 0 ? pick(dirs)() : pick(forms)();
      if (rnd() % 7 === 0 && parts.length > 1 && !parts[0].startsWith("  .")) parts[1 + (rnd() % (parts.length - 1))] = pick(JUNK);
      src.push(fmtLine(parts));
      if (rnd() % 6 === 0) src.push(pick(["other:", "x:", "back2:"]));
    }
    src.push("other:", "  ebreak");
    progs.push(src.join("\n") + "\n");
  }
  progs.forEach((source, i) => golden.asm.push({ name: `near:${i}`, source, result: asmView(asm.assemble(source)) }));
  const okCount = golden.asm.filter((a) => a.name.startsWith("near:") && a.result.errors.length === 0).length;
  console.log(`почти верных программ без ошибок: ${okCount} из ${progs.length}`);
}

/* ---------- программы задач: решения, заготовки, искажённые варианты ---------- */
const taskPrograms = [];
const allTasks = [
  ...tasks.RV_TASKS.map((t) => ({ t, chapter: 16 })),
  ...real.REAL_TASKS.map((t) => ({ t, chapter: 17 })),
];
for (const { t } of allTasks) {
  const full = tasks.fullSource(t.solution, t);
  golden.asm.push({ name: `task:${t.id}:solution`, source: full, result: asmView(asm.assemble(full)) });
  const fullStarter = tasks.fullSource(t.starter, t);
  golden.asm.push({ name: `task:${t.id}:starter`, source: fullStarter, result: asmView(asm.assemble(fullStarter)) });
  taskPrograms.push({ task: t.id, mutation: "solution", program: t.solution });
  taskPrograms.push({ task: t.id, mutation: "starter", program: t.starter });
  taskPrograms.push({ task: t.id, mutation: "empty", program: "" });
  const lines = t.solution.split("\n");
  lines.forEach((_, i) => {
    taskPrograms.push({ task: t.id, mutation: "drop", line: i, program: lines.filter((__, j) => j !== i).join("\n") });
    taskPrograms.push({ task: t.id, mutation: "dup", line: i, program: [...lines.slice(0, i + 1), lines[i], ...lines.slice(i + 1)].join("\n") });
  });
}

/** Написанные вручную неверные решения (полный текст хранится в выгрузке). */
const HAND = {
  "uart-hi": [
    "  li t0, 0x10000000\n  li t1, 72\n  sb t1, 0(t0)\n  ebreak\n",
    "  li t0, 0x10000000\n  li t1, 'H'\n  sb t1, 0(t0)\n  li t1, 'i'\n  sb t1, 0(t0)\n  li t1, '!'\n  sb t1, 0(t0)\n  ebreak\n",
    "  li t0, 0x10000004\n  sb zero, 0(t0)\n  ebreak\n",
    "  li t0, 0x10000008\n  lw t1, 0(t0)\n  ebreak\n",
  ],
  "uart-string": ["  ebreak\n", "  la t1, msg\n  lw a0, 1(t1)\n  ebreak\n", "loop:\n  j loop\n"],
  leds: [
    "  li t0, 0x10001000\n  li t1, 0x5A\n  sw t1, 0(t0)\n  ebreak\n",
    "  li t0, 0x10001000\n  li t1, 0x1A5\n  sw t1, 0(t0)\n  ebreak\n",
    "  li t0, 0x10001000\n  li t1, 0xA5\n  sh t1, 2(t0)\n  ebreak\n",
  ],
  "switches-invert": [
    "  ebreak\n",
    "  li t0, 0x10001004\n  li t1, 0x10001000\n  lw t2, 0(t0)\n  sw t2, 0(t1)\n  ebreak\n",
    "  li t0, 0x10001004\n  sw zero, 0(t0)\n  ebreak\n",
  ],
  "sum-100": ["  li a0, 5051\n  ebreak\n", "  li a0, -1\n  ebreak\n", "  li a0, 5050\n  ebreak\n"],
  upper: ["  ebreak\n", "  la t0, text\n  li t1, 'Z'\n  sb t1, 0(t0)\n  ebreak\n"],
  factorial: [
    "  li a0, 720\n  ebreak\n",
    "  li a0, 720\n  addi sp, sp, -16\n  ebreak\n",
    "  li a0, 6\n  call fact\n  ebreak\nfact:\n  ret\n",
    "  li a0, 720\n  li sp, 0x2000\n  ebreak\n",
  ],
  "sort-words": [
    "  ebreak\n",
    "  la t0, arr\n  li t1, 0\n  sw t1, 0(t0)\n  ebreak\n",
    "  la t0, arr\n  lw t1, 0(t0)\n  lw t2, 4(t0)\n  sw t2, 0(t0)\n  sw t1, 4(t0)\n  ebreak\n",
  ],
  "timer-blink": [
    "  li t0, 0x10001000\n  li t1, 1\n  sw t1, 0(t0)\n  ebreak\n",
    "  li t0, 0x10001000\n  li t1, 2\n  sw t1, 0(t0)\n  ebreak\n",
    // восемь переключений без пауз
    "  li t0, 0x10001000\n  li t2, 8\n  li t3, 1\nl:\n  sw t3, 0(t0)\n  xori t3, t3, 1\n  addi t2, t2, -1\n  bnez t2, l\n  ebreak\n",
    // паузы по 100 тактов
    "  li t0, 0x10001000\n  li t1, 0x10002000\n  li t2, 8\n  li t3, 1\nl:\n  sw t3, 0(t0)\n  lw t4, 0(t1)\n  addi t4, t4, 100\nw:\n  lw t5, 0(t1)\n  bltu t5, t4, w\n  xori t3, t3, 1\n  addi t2, t2, -1\n  bnez t2, l\n  ebreak\n",
    // повторная запись того же значения не считается переключением
    "  li t0, 0x10001000\n  li t1, 0x10002000\n  li t2, 9\n  li t3, 1\nl:\n  sw t3, 0(t0)\n  sw t3, 0(t0)\n  lw t4, 0(t1)\n  addi t4, t4, 250\nw:\n  lw t5, 0(t1)\n  bltu t5, t4, w\n  xori t3, t3, 1\n  addi t2, t2, -1\n  bnez t2, l\n  ebreak\n",
  ],
  "real-hello": [
    "  .globl _start\n  .text\n_start:\n  li a0, 0\n  li a7, 93\n  ecall\n",
    "  .globl _start\n  .text\n_start:\n  li a0, 2\n  la a1, msg\n  li a2, 15\n  li a7, 64\n  ecall\n  li a0, 0\n  li a7, 93\n  ecall\n  .section .rodata\nmsg:\n  .ascii \"Hello, RISC-V!\\n\"\n",
    "  .globl _start\n  .text\n_start:\n  li a0, 1\n  la a1, msg\n  li a2, 15\n  li a7, 64\n  ecall\n  li a0, 3\n  li a7, 93\n  ecall\n  .section .rodata\nmsg:\n  .ascii \"Hello, RISC-V!\\n\"\n",
    "  .globl _start\n  .text\n_start:\n  li a0, 1\n  li a1, 0x8000\n  li a2, 4\n  li a7, 64\n  ecall\n",
    "  .globl _start\n  .text\n_start:\n  li a7, 17\n  ecall\n",
    "  .globl _start\n  .text\n_start:\n  ebreak\n",
  ],
  "real-print-uint": ["  .globl _start\n  .text\n_start:\n  li a0, 0\n  li a7, 93\n  ecall\n"],
  "real-fizzbuzz": ["  .globl _start\n  .text\n_start:\n  li a0, 0\n  li a7, 93\n  ecall\n"],
  "real-fib": ["  .globl _start\n  .text\n_start:\n  li a0, 7\n  li a7, 93\n  ecall\n"],
  "real-sort-print": ["  .globl _start\n  .text\n_start:\n  li a0, 0\n  li a7, 93\n  ecall\n"],
  "real-exit-code": [
    "  .globl _start\n  .text\n_start:\n  li a0, 5\n  li a7, 93\n  ecall\n",
    "  .globl _start\n  .text\n_start:\n  li a0, 12\n  li a7, 93\n  ecall\n",
    "  .globl _start\n  .text\n_start:\n  li a0, -1\n  li a7, 93\n  ecall\n",
    "  .globl _start\n  .text\n_start:\n  li a0, 256\n  li a7, 93\n  ecall\n",
  ],
};
for (const [id, list] of Object.entries(HAND)) list.forEach((program, k) => taskPrograms.push({ task: id, mutation: "hand", line: k, program }));

const byId = Object.fromEntries(allTasks.map(({ t }) => [t.id, t]));
golden.verdicts = taskPrograms.map((p) => {
  const row = { task: p.task, mutation: p.mutation, verdict: tsVerdict(byId[p.task], p.program) };
  if (p.line !== undefined) row.line = p.line;
  if (p.mutation === "hand") row.program = p.program;
  return row;
});
for (const { t } of allTasks) {
  // решения-ровесники: id того, кто прошёл, нужен только для самопроверки
  const v = golden.verdicts.find((r) => r.task === t.id && r.mutation === "solution");
  if (!v.verdict.ok) throw new Error(`эталон ${t.id} не проходит: ${JSON.stringify(v.verdict)}`);
}

/* ---------- исполнение ---------- */
const memHash = (mem) => fnv(mem);
const summary = (m) => {
  const v = m.view();
  return {
    regs: v.regs,
    pc: v.pc >>> 0,
    steps: v.steps,
    halted: v.halted,
    exit_code: v.exitCode,
    error: v.error,
    uart: v.uart,
    leds: v.leds,
    led_log: v.ledLog.map((e) => ({ cycle: e.cycle, value: e.value })),
    last_read: v.lastRead,
    last_write: v.lastWrite,
    last_reg: v.lastReg,
    last_insn: v.lastInsn,
    mem_hash: memHash(v.mem),
  };
};

const imageOf = (wordsArr) => {
  const img = new Uint8Array(asm.RAM_SIZE);
  wordsArr.forEach((w, i) => {
    for (let k = 0; k < 4; k++) img[4 * i + k] = (w >>> (8 * k)) & 0xff;
  });
  return img;
};

/** Запуск образа: начальные регистры, лимит шагов, трасса первых `traceLimit` шагов. */
function runCase(name, image, { regs = {}, switches = 0, entry = 0, maxSteps = 500, traceLimit = 0 } = {}) {
  const m = new machine.RvMachine(image, { switches, entry });
  for (const [r, v] of Object.entries(regs)) m.regs[Number(r)] = v;
  let trace;
  if (traceLimit > 0) {
    trace = [];
    let left = maxSteps;
    while (m.running && left-- > 0) {
      const pc = m.pc >>> 0;
      const before = m.steps;
      m.step();
      if (m.steps !== before && trace.length < traceLimit) {
        trace.push({
          pc,
          insn: m.lastInsn,
          last_read: m.lastRead,
          last_write: m.lastWrite,
          last_reg: m.lastReg,
          regs: Array.from(m.regs, (x) => x >>> 0),
          steps: m.steps,
        });
      }
    }
    if (m.running) m.error = `Превышен лимит в ${maxSteps} шагов — похоже, цикл не заканчивается.`;
  } else {
    m.run(maxSteps);
  }
  const row = {
    name,
    image_hex: Buffer.from(image).toString("hex").replace(/(00)+$/, ""),
    regs_init: Object.entries(regs).map(([r, v]) => [Number(r), v | 0]),
    switches,
    entry,
    max_steps: maxSteps,
    final: summary(m),
  };
  if (trace) row.trace = trace;
  return row;
}

golden.runs = [];

// трассы настоящих программ
for (const id of ["sum-100", "factorial", "sort-words", "upper", "uart-string", "timer-blink", "switches-invert", "real-fizzbuzz", "real-print-uint", "real-sort-print", "real-exit-code", "real-hello"]) {
  const t = byId[id];
  const a = asm.assemble(tasks.fullSource(t.solution, t));
  golden.runs.push(runCase(`task:${id}`, a.image, { switches: t.switches ?? 0, entry: a.entry, maxSteps: RUN_LIMIT, traceLimit: 200 }));
}

// ошибки исполнения
const FAULTS = {
  unaligned_lw: "  li t0, 0x1001\n  lw a0, 0(t0)\n  ebreak\n",
  unaligned_sw: "  li t0, 0x1002\n  sw a0, 0(t0)\n  ebreak\n",
  unaligned_lh: "  li t0, 0x1001\n  lh a0, 0(t0)\n  ebreak\n",
  unaligned_sh: "  li t0, 0x1001\n  sh a0, 0(t0)\n  ebreak\n",
  load_oob: "  li t0, 0x4000\n  lw a0, 0(t0)\n  ebreak\n",
  load_edge: "  li t0, 0x3ffc\n  lw a0, 0(t0)\n  lb a1, 3(t0)\n  ebreak\n",
  store_oob: "  li t0, 0x7ffffffc\n  sw a0, 0(t0)\n  ebreak\n",
  load_neg_addr: "  li t0, -4\n  lw a0, 0(t0)\n  ebreak\n",
  load_no_device: "  li t0, 0x10000008\n  lw a0, 0(t0)\n  ebreak\n",
  load_no_device_hi: "  li t0, 0xfffffff0\n  lw a0, 0(t0)\n  ebreak\n",
  store_status: "  li t0, 0x10000004\n  sw a0, 0(t0)\n  ebreak\n",
  store_timer: "  li t0, 0x10002000\n  sw a0, 0(t0)\n  ebreak\n",
  devices_read:
    "  li t0, 0x10000000\n  li t1, 0x10001000\n  li t2, 0x10002000\n  lw a0, 0(t0)\n  lw a1, 4(t0)\n  lw a2, 0(t1)\n  lw a3, 4(t1)\n  lw a4, 0(t2)\n  lbu a5, 1(t1)\n  ebreak\n",
  uart_bytes: "  li t0, 0x10000000\n  li t1, 0xd0\n  sb t1, 0(t0)\n  li t1, 0x9f\n  sb t1, 0(t0)\n  li t1, 0xff\n  sb t1, 1(t0)\n  li t1, 0xc3\n  sb t1, 0(t0)\n  li t1, 0xa9\n  sb t1, 0(t0)\n  ebreak\n",
  uart_bom: "  li t0, 0x10000000\n  li t1, 0xef\n  sb t1, 0(t0)\n  li t1, 0xbb\n  sb t1, 0(t0)\n  li t1, 0xbf\n  sb t1, 0(t0)\n  li t1, 0x41\n  sb t1, 0(t0)\n  ebreak\n",
  no_instruction: "  nop\n",
  pc_out: "  j 0x7000\n",
  jalr_misaligned: "  li t0, 2\n  jalr ra, 0(t0)\n  ebreak\n",
  jalr_odd_clears_bit: "  li t0, 9\n  jalr ra, 0(t0)\n  ebreak\n",
  jalr_negative: "  li t0, -8\n  jalr zero, 0(t0)\n",
  branch_misaligned: "  beq zero, zero, 2\n",
  infinite_loop: "l:\n  j l\n",
  unknown_ecall: "  li a7, 17\n  ecall\n",
  write_bad_fd: "  li a0, 2\n  li a7, 64\n  ecall\n",
  write_oob: "  li a0, 1\n  li a1, 0x3fff\n  li a2, 10\n  li a7, 64\n  ecall\n",
  write_neg_len: "  li a0, 1\n  li a1, 0\n  li a2, -1\n  li a7, 64\n  ecall\n",
  write_ok: "  li a0, 1\n  la a1, d\n  li a2, 3\n  li a7, 64\n  ecall\n  mv s0, a0\n  li a0, 7\n  li a7, 93\n  ecall\n  .data\nd:\n  .ascii \"xyz\"\n",
  exit_neg: "  li a0, -3\n  li a7, 93\n  ecall\n",
  stack_pointer: "  mv a0, sp\n  addi sp, sp, -16\n  sw ra, 12(sp)\n  lw a1, 12(sp)\n  ebreak\n",
  x0_write: "  addi zero, zero, 5\n  lui zero, 1\n  jal zero, 4\n  mv a0, zero\n  ebreak\n",
  timer_reads: "  li t0, 0x10002000\n  lw a0, 0(t0)\n  lw a1, 0(t0)\n  nop\n  lw a2, 0(t0)\n  ebreak\n",
  leds_log: "  li t0, 0x10001000\n  li t1, 1\n  sw t1, 0(t0)\n  li t1, 0x1ff\n  sw t1, 0(t0)\n  sb zero, 0(t0)\n  lw a0, 0(t0)\n  ebreak\n",
  switches_read: "  li t0, 0x10001004\n  lw a0, 0(t0)\n  ebreak\n",
  big_program_loop: "  li t0, 3000\nl:\n  addi t0, t0, -1\n  bnez t0, l\n  ebreak\n",
};
for (const [name, src] of Object.entries(FAULTS)) {
  const a = asm.assemble(src);
  if (a.errors.length) throw new Error(`образец ${name} не собирается: ${JSON.stringify(a.errors)}`);
  golden.runs.push(runCase(`fault:${name}`, a.image, { entry: a.entry, switches: 0b10100101, maxSteps: name === "big_program_loop" ? 20000 : 1000, traceLimit: name === "infinite_loop" ? 20 : 0 }));
}
// таймер и лимит шагов: лимит меньше длины программы
{
  const a = asm.assemble("  li t0, 5\nl:\n  addi t0, t0, -1\n  bnez t0, l\n  ebreak\n");
  golden.runs.push(runCase("limit:short", a.image, { maxSteps: 7, traceLimit: 10 }));
  golden.runs.push(runCase("limit:exact", a.image, { maxSteps: 12, traceLimit: 20 }));
  golden.runs.push(runCase("limit:enough", a.image, { maxSteps: 13, traceLimit: 20 }));
}

// случайные программы: слова с кодированием по форматам, пары значений и адресов в регистрах
const SPECIAL = [0, 1, -1, 2, 0x7fffffff, -0x80000000, 0x80000000 | 0, 0x1000, 0x1004, 0x3ffc, 0x3ff0, 0x10000000, 0x10000004, 0x10001000, 0x10001004, 0x10002000, 0xdeadbeef | 0, 31, 32, 4, -4, 0x2000];
const rndVal = () => (rnd() & 3 ? pick(SPECIAL) : rnd() | 0);
const R_OPS = isa.OPS.filter((o) => o.fmt === "R");
const I_OPS = isa.OPS.filter((o) => o.fmt === "I");
const SH_OPS = isa.OPS.filter((o) => o.fmt === "SH");
const L_OPS = isa.OPS.filter((o) => o.fmt === "L");
const S_OPS = isa.OPS.filter((o) => o.fmt === "S");
const B_OPS = isa.OPS.filter((o) => o.fmt === "B");
const byName = (m) => isa.opByMnemonic(m);
const reg = () => 1 + (rnd() % 31);
// приёмник результата: не x0…x4 (в x3 и x4 лежат безопасные адреса) и не a7 (там номер вызова)
const dreg = () => {
  const r = 5 + (rnd() % 27);
  return r === 17 ? 18 : r;
};
// основа адреса для загрузок и записей: чаще безопасная, иногда случайная
const abase = () => (rnd() % 8 === 0 ? reg() : 3 + (rnd() & 1));
const smallImm = () => (rnd() % 64) - 32;

function randomInsn() {
  const kind = rnd() % 12;
  switch (kind) {
    case 0:
    case 1:
      return isa.encR(pick(R_OPS), dreg(), reg(), reg());
    case 2:
    case 3:
      return isa.encI(pick(I_OPS), dreg(), reg(), rnd() & 3 ? smallImm() : (rnd() % 4096) - 2048);
    case 4:
      return isa.encSH(pick(SH_OPS), dreg(), reg(), rnd() % 32);
    case 5:
      return isa.encI(pick(L_OPS), dreg(), abase(), 4 * (rnd() % 16) - (rnd() % 8 === 0 ? 1 : 0));
    case 6:
      return isa.encS(pick(S_OPS), reg(), abase(), 4 * (rnd() % 16) - (rnd() % 8 === 0 ? 1 : 0));
    case 7: {
      // переход вперёд на 1…4 команды, чтобы не зациклиться
      const off = 4 * (1 + (rnd() % 4));
      return isa.encB(pick(B_OPS), reg(), reg(), off);
    }
    case 8:
      return isa.encU(byName(rnd() & 1 ? "lui" : "auipc"), dreg(), rnd() & 0xfffff);
    case 9:
      return isa.encJ(byName("jal"), rnd() & 1 ? 0 : dreg(), 4 * (1 + (rnd() % 3)));
    case 10:
      return rnd() % 4 === 0 ? isa.encI(byName("jalr"), dreg(), reg(), (rnd() % 8) * 2) : isa.encI(byName("addi"), dreg(), reg(), smallImm());
    default:
      return rnd() % 16 ? isa.encI(byName("addi"), dreg(), reg(), smallImm()) : isa.ECALL;
  }
}

for (let c = 0; c < 250; c++) {
  const n = 24 + (rnd() % 24);
  const w = Array.from({ length: n }, () => randomInsn());
  w.push(isa.EBREAK);
  const regs = {};
  for (let r = 1; r < 32; r++) if (r !== 2 || rnd() & 1) regs[r] = rndVal();
  regs[3] = 0x2000 + 4 * (rnd() % 64);
  regs[4] = 0x3000 + 4 * (rnd() % 64);
  if (rnd() % 8 === 0) regs[3] = rndVal();
  regs[17] = pick([93, 64, 5, 93]);
  regs[10] = rnd() % 4 ? 1 : rndVal();
  regs[11] = 0x2000 + (rnd() % 64);
  regs[12] = rnd() % 16;
  golden.runs.push(runCase(`fuzz:${c}`, imageOf(w), { regs, switches: rnd() & 0xff, maxSteps: 200 }));
}

// случайные слова целиком (в том числе не-команды) и запуск с нулевой точки
for (let c = 0; c < 100; c++) {
  const w = Array.from({ length: 16 }, () => rnd());
  golden.runs.push(runCase(`noise:${c}`, imageOf(w), { maxSteps: 50 }));
}

/* ---------- таблица АЛУ: все регистровые команды на парах краевых значений ---------- */
const VALS = [0, 1, -1, 2, 7, -7, 31, 32, 0x7fffffff, -0x80000000, 0x12345678, 0xdeadbeef | 0, 0x80000001 | 0, 65535, -65536];
golden.alu = [];
for (const o of R_OPS) {
  for (const a of VALS) {
    for (const b of VALS) {
      const img = imageOf([isa.encR(o, 12, 10, 11), isa.EBREAK]);
      const m = new machine.RvMachine(img, {});
      m.regs[10] = a;
      m.regs[11] = b;
      m.run(10);
      golden.alu.push([o.mnemonic, a, b, m.regs[12]]);
    }
  }
}
for (const o of [...I_OPS, ...SH_OPS]) {
  for (const a of VALS) {
    for (const imm of o.fmt === "SH" ? [0, 1, 5, 31] : [0, 1, -1, 7, 2047, -2048, 255, -256]) {
      const w = o.fmt === "SH" ? isa.encSH(o, 12, 10, imm) : isa.encI(o, 12, 10, imm);
      const m = new machine.RvMachine(imageOf([w, isa.EBREAK]), {});
      m.regs[10] = a;
      m.run(10);
      golden.alu.push([o.mnemonic, a, imm, m.regs[12]]);
    }
  }
}

/* ---------- проект и архив ---------- */
{
  const src = "  .globl _start\n_start:\n  li a7, 93\n  ecall";
  const files = project.projectFiles(src);
  const bytes = zip.makeZip(project.projectZip(files));
  golden.project = {
    source: src,
    files: files.map((f) => ({ name: f.name, content: f.content, note: f.note })),
    zip_hex: Buffer.from(bytes).toString("hex"),
    source_with_newline: project.projectFiles(src + "\n")[0].content,
    crc: [
      ["", zip.crc32(new Uint8Array())],
      ["123456789", zip.crc32(new TextEncoder().encode("123456789"))],
      ["программа", zip.crc32(new TextEncoder().encode("программа"))],
    ],
  };
}

fs.mkdirSync(path.dirname(outGolden), { recursive: true });
fs.writeFileSync(outGolden, JSON.stringify(golden) + "\n");
console.log(
  `выгрузка: ${outExport} (задач: ${exportData.chapters.map((c) => `${c.chapter}:${c.tasks.length}`).join(" ")});` +
    ` золото: ${outGolden} (слов: ${golden.decode.length}, ассемблер: ${golden.asm.length}, прогонов: ${golden.runs.length}, вердиктов: ${golden.verdicts.length}, АЛУ: ${golden.alu.length})`,
);
