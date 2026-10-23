// Выгрузка лаборатории «Архитектура компьютера» (глава 6–15 книги 14) в данные для Rust-крейта shared-rs/archlab.
// Из TS-исходников (frontend/src/lab, без React) собирает:
//   1. главы с упражнениями в каноническом виде (snake_case): условия, спецификации проверки, эталонные решения;
//   2. «золотые» результаты TS-движка: проверки эталонов и их искажений, значения узлов схем на наборах входов,
//      цепочки settle, разворачивание блоков, блоки и трассы процессора Мини-8, ассемблер.
// Запуск: cd frontend && node scripts/arch-export.mjs [выгрузка.json] [golden.json]
//   по умолчанию: /tmp/arch-export.json и ../shared-rs/archlab/tests/golden.json
// Дальше: cd shared-rs/archlab && cargo run --release --bin import -- <выгрузка.json> ../../backend/app/data
import { build } from "esbuild";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const lab = path.join(root, "src/lab");
const outData = path.resolve(process.argv[2] ?? path.join(os.tmpdir(), "arch-export.json"));
const outGolden = path.resolve(process.argv[3] ?? path.join(root, "../shared-rs/archlab/tests/golden.json"));
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "arch-export-"));

/* Главы книги 14: те же, что в src/lab/registry.ts (его не импортируем — он тянет RISC-V). Сверяем с исходником ниже. */
const CIRCUIT_CHAPTERS = { 6: "simple-circuits", 7: "mux", 8: "latches", 9: "adders", 10: "registers", 11: "alu", 12: "memory", 13: "decoder", 14: "cpu" };
const ASM_CHAPTER = 15;
const registrySrc = fs.readFileSync(path.join(lab, "registry.ts"), "utf8");
for (const [n, slug] of Object.entries(CIRCUIT_CHAPTERS)) {
  if (!new RegExp(`${n}:\\s*\\{\\s*kind:\\s*"circuit",\\s*slug:\\s*"${slug}"`).test(registrySrc))
    throw new Error(`registry.ts разошёлся с экспортёром: глава ${n} должна быть «${slug}»`);
}
if (!new RegExp(`${ASM_CHAPTER}:\\s*\\{\\s*kind:\\s*"asm"`).test(registrySrc)) throw new Error("registry.ts: глава 15 — не asm");

const entry = String.raw`
import { SECTIONS } from "__LAB__/sections/sections.ts";
import { SECTION_SOLUTIONS, BLOCK_SOLUTIONS } from "__LAB__/exercises/logic-gates/solutions.ts";
import * as CM from "__LAB__/exercises/logic-gates/circuit.model.ts";
import * as BL from "__LAB__/exercises/logic-gates/blocks.ts";
import { TASKS as ASM } from "__LAB__/asm/tasks.ts";
import { assemble } from "__LAB__/asm/assembler.ts";
import { Machine } from "__LAB__/asm/machine.ts";
import { disassemble } from "__LAB__/asm/isa.ts";
import { GateMachine, cpuExpansion } from "__LAB__/cpu8/gate-machine.ts";
import { CPU8_BLOCKS } from "__LAB__/cpu8/blocks.ts";
import { suggestWires } from "__LAB__/exercises/logic-gates/auto-wire.ts";
import * as LY from "__LAB__/exercises/logic-gates/block-layout.ts";
import * as IF from "__LAB__/exercises/logic-gates/interfaces.ts";
import { buildWave } from "__LAB__/exercises/logic-gates/lab/wave.ts";

const nul = (v) => (v === undefined ? null : v);
const hexOf = (bytes) => Array.from(bytes, (b) => b.toString(16).padStart(2, "0")).join("");

/* ---------- эталонные решения: нетлисты → схемы с раскладкой ---------- */
function netCircuit(ex, net, outs) {
  const labels = ex.labels ?? ex.inputs;
  const gid = (n) => "g_" + n;
  const resolve = (name) => {
    const li = labels.indexOf(name);
    if (li >= 0) return ex.inputs[li];
    if (name in net) return gid(name);
    throw new Error(ex.id + ": нет источника " + name);
  };
  let w = 0;
  const wire = (from, to, pin) => ({ id: "w" + ++w, from: { node: from, pin: "out" }, to: { node: to, pin } });
  const gates = [];
  const wires = [];
  const depth = new Map();
  const depthOf = (name, seen = new Set()) => {
    if (!(name in net)) return 0;
    if (depth.has(name)) return depth.get(name);
    if (seen.has(name)) return 0;
    seen.add(name);
    const [, a, b] = net[name];
    const d = 1 + Math.max(srcDepth(a, seen), b === undefined ? 0 : srcDepth(b, seen));
    depth.set(name, d);
    return d;
  };
  const srcDepth = (n, seen) => (labels.indexOf(n) >= 0 ? 0 : depthOf(n, seen));
  const cols = new Map();
  for (const [name, [type, a, b]] of Object.entries(net)) {
    const d = depthOf(name);
    const idx = cols.get(d) ?? 0;
    cols.set(d, idx + 1);
    gates.push({ id: gid(name), type, x: Math.min(690, 150 + Math.max(0, d - 1) * 90), y: 12 + (idx % 7) * 56 });
    wires.push(wire(resolve(a), gid(name), "in0"));
    if (type !== "NOT") wires.push(wire(resolve(b), gid(name), "in1"));
  }
  for (const [o, src] of Object.entries(outs)) wires.push(wire(resolve(src), o, "in0"));
  return { gates, wires };
}

const refs = new Map(); // "slug/id" → решение (как в TS)
for (const sec of SECTIONS) {
  for (const ex of sec.exercises) {
    const bs = BLOCK_SOLUTIONS[ex.id];
    const ns = SECTION_SOLUTIONS[sec.slug]?.[ex.id];
    if (bs && sec.slug === "cpu") refs.set(sec.slug + "/" + ex.id, bs);
    else if (ns) refs.set(sec.slug + "/" + ex.id, netCircuit(ex, ns.net, ns.outs));
  }
}
const store = {
  load: (pk, id) => { const sec = SECTIONS.find((s) => s.progressKey === pk); return sec ? refs.get(sec.slug + "/" + id) : undefined; },
  save() {},
};
const lib = BL.createLibrary(SECTIONS, store);

const solOut = (sol) =>
  sol === undefined ? null
  : sol.instances
    ? { instances: sol.instances.map((i) => ({ id: i.id, block_id: i.blockId, x: i.x, y: i.y })),
        bus_wires: sol.busWires.map((w) => ({ id: w.id, from: w.from, to: w.to })) }
  : sol.native
    ? { native: sol.native, addr: sol.addr, din: sol.din ?? null, we: sol.we ?? null, clk: sol.clk ?? null, dout: sol.dout }
  : { gates: sol.gates, wires: sol.wires };

const circuitOf = (ex, sol) =>
  BL.isBlockSolution(sol) ? BL.expand(sol, BL.interfaceOfExercise(ex), lib.lookup).circuit : { gates: sol.gates, wires: sol.wires };

/* ---------- проверка: таблица и сценарий (то, что в интерфейсе делают CircuitLab и CheckPanel) ---------- */
function checkTable(ex, circuit) {
  const rows = ex.target.map((t, row) => {
    const inputs = CM.inputsForRow(ex.inputs, row);
    const actuals = ex.outputs.map((o) => CM.outputValue(circuit, inputs, o));
    return { actuals: actuals.map(nul), ok: actuals.every((a, i) => a === t[i]) };
  });
  const passed = rows.filter((r) => r.ok).length;
  return { ok: rows.length > 0 && passed === rows.length, passed, total: rows.length };
}

/** Перестановки списка в лексикографическом порядке индексов (как archlab::check::permutations). */
function perms(arr) {
  if (arr.length <= 1) return [arr];
  return arr.flatMap((x, i) => perms([...arr.slice(0, i), ...arr.slice(i + 1)]).map((p) => [x, ...p]));
}

/** Безголовый «идеальный ученик»: проходит шаги сценария по порядку (см. archlab::check::run_steps). */
function checkSteps(ex, circuit) {
  let inputs = CM.zeroInputs();
  let last = new Map();
  const settle = () => { const r = CM.settleCircuit(circuit, inputs, last); last = r.stable ? r.values : new Map(); return r.values; };
  settle();
  const clock = ex.clock ?? null;
  const ticks = !!ex.ticks && clock !== null;
  const steps = ex.steps ?? [];
  const meets = (st, values) => ex.outputs.every((o) => st.expect[o] === undefined || values.get(o) === st.expect[o]);
  let passed = 0;
  const got = [];
  for (const st of steps) {
    let values;
    let ok;
    if (ticks) {
      for (const id of ex.inputs) if (id !== clock) inputs[id] = st.inputs[id] ?? inputs[id];
      inputs[clock] = 0;
      values = settle();
      const n = st.inputs[clock] === 1 ? (st.pulses ?? 1) : 0; // CLK = 0 в шаге — такт не подаётся
      for (let p = 1; p <= n; p++) {
        inputs[clock] = 1;
        values = settle();
        if (p < n) { inputs[clock] = 0; settle(); }
      }
      ok = meets(st, values);
    } else {
      // без такта: сначала все тумблеры сразу, затем (если не вышло) по одному во всех порядках
      const start = { inputs: { ...inputs }, last };
      const changed = ex.inputs.filter((id) => st.inputs[id] !== undefined && st.inputs[id] !== inputs[id]);
      const attempt = (order) => {
        inputs = { ...start.inputs }; last = start.last;
        if (order === null) { for (const id of changed) inputs[id] = st.inputs[id]; values = settle(); }
        else for (const id of order) { inputs[id] = st.inputs[id]; values = settle(); }
        return meets(st, values);
      };
      ok = attempt(null);
      const firstValues = values;
      if (!ok && changed.length >= 2 && changed.length <= 5) {
        for (const order of perms(changed)) if (attempt(order)) { ok = true; break; }
        if (!ok) values = firstValues;
      }
    }
    got.push(ex.outputs.map((o) => nul(values.get(o))));
    if (!ok) break;
    passed++;
    if (ticks) { inputs[clock] = 0; settle(); }
  }
  return { ok: steps.length > 0 && passed === steps.length, passed, total: steps.length, got };
}

const check = (ex, circuit) => ((ex.mode ?? "table") === "steps" ? checkSteps(ex, circuit) : checkTable(ex, circuit));

/* ---------- генератор и кодирование значений ---------- */
function lcg(seed) {
  let s = seed >>> 0;
  return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s >>> 8; };
}
const hashStr = (s) => { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h >>> 0; };
const inputsFromInt = (v) => Object.fromEntries(CM.INPUT_IDS.map((id, i) => [id, (v >> i) & 1]));

function encoder() {
  const keysets = [];
  const enc = (map) => {
    const keys = [...map.keys()].sort();
    const sig = keys.join("\u0001");
    let ks = keysets.findIndex((k) => k.join("\u0001") === sig);
    if (ks < 0) { ks = keysets.length; keysets.push(keys); }
    return { ks, v: keys.map((k) => { const x = map.get(k); return x === undefined ? "?" : String(x); }).join("") };
  };
  return { enc, keysets };
}

function evalAndSettle(circuit, vectors) {
  const { enc, keysets } = encoder();
  const evals = vectors.map((v) => enc(CM.evaluateCircuit(circuit, inputsFromInt(v))));
  let last = new Map();
  const settles = vectors.map((v) => {
    const r = CM.settleCircuit(circuit, inputsFromInt(v), last);
    last = r.stable ? r.values : new Map();
    return { stable: r.stable, ...enc(r.values) };
  });
  return { keysets, evals, settles };
}

function fingerprint(circuit) {
  const s = circuit.gates.map((g) => g.id + ":" + g.type).join("|") + "#" +
    circuit.wires.map((w) => w.from.node + ">" + w.to.node + ":" + w.to.pin).join("|") + "#" +
    (circuit.natives ?? []).map((n) => [n.id, n.kind, n.addr.join(","), (n.din ?? []).join(","), n.we, n.clk, n.dout.join(",")].join("/")).join("|");
  return { gates: circuit.gates.length, wires: circuit.wires.length, natives: (circuit.natives ?? []).length, hash: hashStr(s) };
}

const NEXT_TYPE = { AND: "OR", OR: "AND", NOR: "NAND", NAND: "NOR", XOR: "XNOR", XNOR: "XOR", NOT: "NOT", DFF: "DFF" };

function mutate(base, m) {
  if (m.drop_wire !== undefined) return { gates: base.gates, wires: base.wires.filter((_, i) => i !== m.drop_wire) };
  if (m.retype) return { gates: base.gates.map((g, i) => (i === m.retype[0] ? { ...g, type: m.retype[1] } : g)), wires: base.wires };
  return base;
}

/* ---------- данные глав ---------- */
function exerciseSpec(sec, ex, sol) {
  return {
    kind: "circuit",
    section: sec.slug,
    mode: ex.mode ?? "table",
    build: ex.kind ?? "gates",
    inputs: ex.inputs,
    labels: ex.labels ?? [],
    outputs: ex.outputs,
    target: ex.target,
    allowed: ex.allowed,
    steps: (ex.steps ?? []).map((s) => ({ inputs: s.inputs, expect: s.expect, text: s.text, pulses: s.pulses ?? null })),
    ports: (ex.ports ?? []).map((p) => ({ name: p.name, type: p.type, nodes: p.nodes })),
    block: ex.block ?? null,
    blocks: ex.blocks ?? [],
    clock: ex.clock ?? null,
    ticks: !!ex.ticks,
    formula: ex.formula,
    success: ex.success,
    solution: solOut(sol),
  };
}

const CIRCUIT_CHAPTERS = __CHAPTERS__;
const ASM_CHAPTER = __ASM__;

export function run() {
  const chapters = [];
  const noSolution = [];
  for (const [n, slug] of Object.entries(CIRCUIT_CHAPTERS)) {
    const sec = SECTIONS.find((s) => s.slug === slug);
    chapters.push({
      book: 14, chapter: Number(n), lab: "arch",
      tasks: sec.exercises.map((ex) => {
        const sol = refs.get(slug + "/" + ex.id);
        if (!sol) noSolution.push(slug + "/" + ex.id);
        return { id: ex.id, title: ex.title, statement: ex.task, hint: ex.hint, spec: exerciseSpec(sec, ex, sol) };
      }),
    });
  }
  chapters.push({
    book: 14, chapter: ASM_CHAPTER, lab: "arch",
    tasks: ASM.map((t) => {
      const expected = t.expected;
      return {
        id: t.id, title: t.title, statement: t.text, hint: t.hint,
        spec: {
          kind: "asm", starter: t.starter, solution: t.solution,
          disk: hexOf(t.disk), expected: hexOf(expected),
          regions: t.regions.map((r) => ({ name: r.name, from: r.from, length: r.length })),
        },
      };
    }),
  });

  /* ---------- золотые результаты ---------- */
  const golden = { version: 1, circuits: [], verdicts: [], blocks: [], expansions: [], asm: [], assembler: [], cpu8: [], noSolution };

  const rnd = lcg(20261023);
  for (const sec of SECTIONS) {
    for (const ex of sec.exercises) {
      const key = sec.slug + "/" + ex.id;
      const sol = refs.get(key);
      if (!sol) continue;
      const circuit = circuitOf(ex, sol);
      const base = { section: sec.slug, id: ex.id };
      const empty = BL.isBlockSolution(sol) ? { gates: [], wires: [] } : { gates: [], wires: [] };
      const vectors = Array.from({ length: 10 }, () => rnd() & 63);
      const mutations = [{}];
      if (!BL.isBlockSolution(sol)) {
        const nw = circuit.wires.length;
        const step = Math.max(1, Math.floor(nw / 4));
        for (let i = 0; i < nw && mutations.length < 6; i += step) mutations.push({ drop_wire: i });
        for (let j = 0; j < circuit.gates.length && mutations.length < 9; j += Math.max(1, Math.floor(circuit.gates.length / 3))) {
          const t = NEXT_TYPE[circuit.gates[j].type];
          if (t !== circuit.gates[j].type) mutations.push({ retype: [j, t] });
        }
      }
      for (const m of mutations) {
        const c = mutate(circuit, m);
        const r = check(ex, c);
        golden.circuits.push({ ...base, mutation: m, vectors, verdict: { ok: r.ok, passed: r.passed, total: r.total, got: r.got ?? null }, ...evalAndSettle(c, vectors) });
      }
      const er = check(ex, empty);
      golden.verdicts.push({ ...base, reference: { ok: check(ex, circuit).ok }, empty: { ok: er.ok, passed: er.passed, total: er.total } });
      if (BL.isBlockSolution(sol)) golden.expansions.push({ ...base, fingerprint: fingerprint(circuit) });
    }
  }

  /* особые схемы: циклы, генерация, «?», триггеры без такта, цепочки выходов, дубли и несуществующие узлы */
  const G = (id, type, x = 0, y = 0) => ({ id, type, x, y });
  const Wr = (id, from, node, pin = "in0") => ({ id, from: { node: from, pin: "out" }, to: { node, pin } });
  const specials = {
    osc: { gates: [G("g1", "NOT")], wires: [Wr("w1", "g1", "g1"), Wr("w2", "g1", "Y")] },
    "sr-nor": { gates: [G("q", "NOR"), G("nq", "NOR")], wires: [Wr("a", "A", "q"), Wr("b", "nq", "q", "in1"), Wr("c", "B", "nq"), Wr("d", "q", "nq", "in1"), Wr("e", "q", "Q"), Wr("f", "nq", "nQ")] },
    "sr-nand": { gates: [G("q", "NAND"), G("nq", "NAND")], wires: [Wr("a", "A", "q"), Wr("b", "nq", "q", "in1"), Wr("c", "B", "nq"), Wr("d", "q", "nq", "in1"), Wr("e", "q", "Q")] },
    dangling: { gates: [G("a", "AND"), G("o", "OR"), G("x", "XOR"), G("n", "NOT"), G("nand", "NAND"), G("nor", "NOR"), G("xn", "XNOR")],
      wires: [Wr("1", "A", "a"), Wr("2", "B", "o", "in1"), Wr("3", "C", "x"), Wr("4", "a", "n"), Wr("5", "o", "nand"), Wr("6", "A", "nor"), Wr("7", "x", "xn"), Wr("8", "o", "Y"), Wr("9", "a", "Z"), Wr("10", "n", "P"), Wr("11", "nand", "Q"), Wr("12", "nor", "R"), Wr("13", "xn", "S")] },
    "dff-chain": { gates: [G("f0", "DFF"), G("f1", "DFF"), G("f2", "DFF")],
      wires: [Wr("1", "B", "f0"), Wr("2", "A", "f0", "in1"), Wr("3", "f0", "f1"), Wr("4", "A", "f1", "in1"), Wr("5", "f1", "f2"), Wr("6", "A", "f2", "in1"), Wr("7", "f2", "Q")] },
    "dff-no-clk": { gates: [G("f0", "DFF")], wires: [Wr("1", "B", "f0"), Wr("2", "f0", "Q")] },
    "dff-gated-clk": { gates: [G("f0", "DFF"), G("g", "AND"), G("n", "NOT")],
      wires: [Wr("1", "n", "f0"), Wr("2", "A", "g"), Wr("3", "B", "g", "in1"), Wr("4", "g", "f0", "in1"), Wr("5", "f0", "n"), Wr("6", "f0", "Q")] },
    toggle: { gates: [G("n", "NOT"), G("ff", "DFF")], wires: [Wr("1", "ff", "n"), Wr("2", "n", "ff"), Wr("3", "A", "ff", "in1"), Wr("4", "ff", "Q")] },
    "out-chain": { gates: [G("g", "AND")], wires: [Wr("1", "A", "g"), Wr("2", "B", "g", "in1"), Wr("3", "g", "Y"), Wr("4", "Y", "Z"), Wr("5", "Z", "T")] },
    "unknown-source": { gates: [G("g", "OR")], wires: [Wr("1", "nowhere", "g"), Wr("2", "A", "g", "in1"), Wr("3", "g", "Y")] },
    "dup-wires": { gates: [G("g", "AND")], wires: [Wr("1", "A", "g"), Wr("2", "B", "g"), Wr("3", "C", "g", "in1"), Wr("4", "D", "g", "in1"), Wr("5", "g", "Y")] },
    "ring3": { gates: [G("a", "NOT"), G("b", "NOT"), G("c", "NOT")], wires: [Wr("1", "c", "a"), Wr("2", "a", "b"), Wr("3", "b", "c"), Wr("4", "c", "Y")] },
    "latch-hold": { gates: [G("a", "OR"), G("n", "NOT"), G("h", "AND")], wires: [Wr("1", "A", "a"), Wr("2", "h", "a", "in1"), Wr("3", "B", "n"), Wr("4", "a", "h"), Wr("5", "n", "h", "in1"), Wr("6", "h", "Q")] },
  };
  golden.specials = [];
  for (const [name, circuit] of Object.entries(specials)) {
    const vectors = Array.from({ length: 24 }, () => rnd() & 63);
    golden.specials.push({ name, circuit, vectors, ...evalAndSettle(circuit, vectors) });
  }
  // генерация: защёлка, у которой отпустили S = R = 1, и генератор, включённый определённым значением
  const oscGated = { gates: [G("o", "OR"), G("g", "NOT")], wires: [Wr("1", "A", "o"), Wr("2", "g", "o", "in1"), Wr("3", "o", "g"), Wr("4", "g", "Y")] };
  for (const [name, circuit, vectors] of [
    ["sr-nor-race", specials["sr-nor"], [0, 1, 3, 0, 2, 3, 0, 1, 0, 3, 3, 0]],
    ["sr-nand-race", specials["sr-nand"], [3, 0, 3, 1, 3, 2, 0, 3, 3]],
    ["osc-gated", oscGated, [0, 1, 0, 1, 1, 0, 0, 1, 0]],
  ]) golden.specials.push({ name, circuit, vectors, ...evalAndSettle(circuit, vectors) });

  /* сценарии, где важен порядок переключения тумблеров: отпускание S = R = 1 у защёлки на ИЛИ-НЕ */
  golden.steps_cases = [];
  {
    const latch = specials["sr-nor"]; // A = R, B = S
    const mk = (steps) => ({ inputs: ["A", "B"], outputs: ["Q", "nQ"], mode: "steps", steps: steps.map(([a, b, q, nq]) => ({ inputs: { A: a, B: b }, expect: { Q: q, nQ: nq }, text: "шаг" })) });
    for (const [name, ex] of [
      ["release-needs-order", mk([[0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 1, 0]])],
      ["release-impossible", mk([[0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 1, 1]])],
      ["plain", mk([[0, 1, 1, 0], [0, 0, 1, 0], [1, 0, 0, 1], [0, 0, 0, 1]])],
    ]) {
      const r = checkSteps(ex, latch);
      golden.steps_cases.push({ name, ex, circuit: latch, verdict: { ok: r.ok, passed: r.passed, total: r.total, got: r.got } });
    }
  }

  /* геометрия: пины, провода, циклы, раскладка блоков, автопроводка, временная диаграмма */
  const ents = (o) => Object.entries(o);
  const geometry = { input_ys: [], output_ys: [], pin_pos: [], wire_path: [], cycles: [], boxes: [], side_boxes: [], free_spot: [], auto_wire: [], wave: [] };
  const idLists = [["A"], ["A", "B"], ["A", "B", "C"], ["A", "B", "C", "D"], ["A", "B", "C", "D", "E"], ["A", "B", "C", "D", "E", "F"]];
  for (const ids of idLists) geometry.input_ys.push({ ids, ys: ents(CM.inputYs(ids)) });
  const outLists = [[], ["Y"], ["Y", "nY"], ["Y1", "Y0"], ["W3", "W2", "W1", "W0"], ["Acc1", "Acc0", "Z", "N", "Pe"], ["Y0", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7"]];
  for (const outs of outLists) geometry.output_ys.push({ outputs: outs, ys: ents(CM.outputYs(outs)) });
  {
    const types = ["AND", "OR", "NOR", "NOT", "NAND", "XOR", "XNOR", "DFF"];
    const gates = types.map((t, i) => ({ id: "g" + i, type: t, x: 200 + i * 7.5, y: 100 + i * 3 }));
    const inY = CM.inputYs(["A", "B", "C", "D"]);
    const outY = CM.outputYs(["Y", "nY"]);
    const refsList = [...gates.flatMap((g) => ["out", "in0", "in1"].map((pin) => ({ node: g.id, pin }))),
      { node: "A", pin: "out" }, { node: "D", pin: "out" }, { node: "Y", pin: "in0" }, { node: "nY", pin: "in0" }, { node: "zzz", pin: "in0" }, { node: "zzz", pin: "out" }];
    for (const maps of [[inY, outY], [undefined, undefined]]) {
      geometry.pin_pos.push({ gates, input_y: maps[0] ? ents(maps[0]) : null, output_y: maps[1] ? ents(maps[1]) : null,
        refs: refsList, pos: refsList.map((r) => CM.pinPos(r, gates, maps[1] ?? {}, maps[0] ?? undefined)) });
    }
    const pts = [[[100, 80], [200, 80]], [[100, 80], [140, 300]], [[0, 0], [500, 120]], [[300, 50], [10, 400]], [[50.5, 20.25], [60.75, 21]]];
    for (const [a, b] of pts) geometry.wire_path.push({ a: { x: a[0], y: a[1] }, b: { x: b[0], y: b[1] }, path: CM.wirePath({ x: a[0], y: a[1] }, { x: b[0], y: b[1] }) });
  }
  for (const sec of SECTIONS) {
    for (const ex of sec.exercises.slice(0, 40)) {
      const sol = refs.get(sec.slug + "/" + ex.id);
      if (!sol || BL.isBlockSolution(sol) || sol.gates.length < 2) continue;
      const c = { gates: sol.gates, wires: sol.wires };
      const proposals = [];
      for (const a of c.gates.slice(0, 4)) for (const b of c.gates.slice(0, 4)) for (const pin of ["in0", "in1"])
        proposals.push({ from: { node: a.id, pin: "out" }, to: { node: b.id, pin } });
      proposals.push({ from: { node: "A", pin: "out" }, to: { node: c.gates[0].id, pin: "in0" } });
      geometry.cycles.push({ section: sec.slug, id: ex.id, proposals, result: proposals.map((p) => CM.createsCycle(c, p.from, p.to)) });
    }
  }
  /* автопроводка: берём вентиль эталонной схемы, «снимаем» его с доски и кладём чуть в стороне */
  for (const sec of SECTIONS) {
    for (const ex of sec.exercises) {
      const sol = refs.get(sec.slug + "/" + ex.id);
      if (!sol || BL.isBlockSolution(sol) || sol.gates.length < 2 || sol.gates.length > 14) continue;
      const k = Math.floor(sol.gates.length / 2);
      const gate0 = sol.gates[k];
      const gate = { ...gate0, x: gate0.x + 13, y: gate0.y - 7 };
      const others = sol.gates.filter((g) => g.id !== gate0.id);
      const wires = sol.wires.filter((w) => w.from.node !== gate0.id && w.to.node !== gate0.id);
      const inputYMap = CM.inputYs(ex.inputs);
      const outputYMap = CM.outputYs(ex.outputs);
      const stepsMode = ex.mode === "steps";
      for (const radius of [undefined, 300, 60]) {
        const first = suggestWires({ gate, gates: others, wires, inputYMap, outputYMap, stepsMode, radius });
        const again = suggestWires({ gate: { ...gate, x: gate.x + 5 }, gates: others, wires, inputYMap, outputYMap, stepsMode, radius, keep: first });
        geometry.auto_wire.push({ section: sec.slug, id: ex.id, gate, gates: others, wires, input_y: ents(inputYMap), output_y: ents(outputYMap),
          steps_mode: stepsMode, radius: radius ?? null, first, again_gate: { ...gate, x: gate.x + 5 }, again });
      }
    }
  }
  /* раскладка блоков: порты блоков процессора и упражнений, свёрнутые и раскрытые */
  {
    const defs = [...lib.defs.values(), ...[...CPU8_BLOCKS.values()].map((b) => b.def)];
    for (const def of defs) {
      const expandable = def.ports.filter((p) => !IF.isSimple(p.type)).map((p) => LY.rowKey({ node: "x", port: p.name, path: "" }));
      for (const open of [[], expandable]) {
        const box = LY.layoutBox("x", def.title, def.ports, new Set(open), { x: 150, y: 30, w: LY.BLOCK_W }, "block");
        geometry.boxes.push({ id: def.id, expanded: open, h: box.h,
          rows: box.rows.map((r) => ({ key: r.key, name: r.name, type: r.type, depth: r.depth, side: r.side, y: r.y, expandable: r.expandable, expanded: r.expanded, nodes: r.nodes })),
          pins: box.rows.map((r) => LY.pinCenter(box, r)) });
      }
      const sb = LY.sideBoxes(def.ports, new Set(), 880);
      geometry.side_boxes.push({ id: def.id, in_h: sb.inBox.h, out_h: sb.outBox.h, in_rows: sb.inBox.rows.map((r) => [r.key, r.y, r.side]), out_rows: sb.outBox.rows.map((r) => [r.key, r.y, r.side]) });
    }
    const takenSets = [[], [{ x: 162, y: 20 }], [{ x: 162, y: 20 }, { x: 368, y: 20 }, { x: 162, y: 170 }], Array.from({ length: 12 }, (_, i) => ({ x: 162 + (i % 3) * 206, y: 20 + Math.floor(i / 3) * 150 }))];
    for (const taken of takenSets) for (const w of [880, 1400, 500])
      geometry.free_spot.push({ taken, board_w: w, spot: LY.freeSpot(taken, w) });
  }
  /* временная диаграмма: история изменений идеального ученика */
  for (const sec of SECTIONS) {
    for (const ex of sec.exercises) {
      if ((ex.mode ?? "table") !== "steps") continue;
      const sol = refs.get(sec.slug + "/" + ex.id);
      if (!sol || BL.isBlockSolution(sol) || geometry.wave.length > 12) continue;
      const circuit = { gates: sol.gates, wires: sol.wires };
      const inputs = CM.zeroInputs();
      let last = new Map();
      const samples = [];
      const snap = () => {
        const r = CM.settleCircuit(circuit, inputs, last); last = r.stable ? r.values : new Map();
        samples.push({ inputs: Object.fromEntries(ex.inputs.map((id) => [id, inputs[id]])), outputs: Object.fromEntries(ex.outputs.map((o) => [o, nul(r.values.get(o))])) });
      };
      snap();
      for (const st of ex.steps) { for (const id of ex.inputs) inputs[id] = st.inputs[id] ?? inputs[id]; snap(); if (ex.clock) { const c = ex.clock; const v = inputs[c]; inputs[c] = 0; snap(); inputs[c] = v; } }
      const wave = buildWave(samples.map((x) => ({ inputs: x.inputs, outputs: Object.fromEntries(ents(x.outputs).map(([k, v]) => [k, v === null ? undefined : v])) })), ex);
      geometry.wave.push({ section: sec.slug, id: ex.id, samples, wave });
    }
  }
  golden.geometry = geometry;

  /* блоки процессора Мини-8 как данные: определения и решения */
  for (const [id, b] of CPU8_BLOCKS) {
    golden.blocks.push({ id, def: { id: b.def.id, title: b.def.title, inputs: b.def.inputs, outputs: b.def.outputs,
      ports: b.def.ports.map((p) => ({ name: p.name, type: p.type, dir: p.dir, nodes: p.nodes })) }, solution: solOut(b.solution) });
  }
  const cpuExp = cpuExpansion();
  golden.cpuExpansion = fingerprint(cpuExp.circuit);

  /* ассемблер: исходники → слова, строки, метки, ошибки */
  const snippets = [
    "", "  hlt", "li r1, 5\nhlt", "li r1, 255\nli r2, -128\nli r3, 256", "li r1, 'A'\nli r2, '\\n'\nli r3, '\\0'\nli r4, '\\''", "li r1, 0x7F\nli r2, 0b1010\nli r3, -0x10\nli r4, +7",
    "add r1, r2, r3\nsub r4, r5, r6\nand r7, r0, r1\nor r1, r2, r3\nxor r2, r3, r4", "addi r1, r2, 31\naddi r1, r2, -32\naddi r1, r2, 32\naddi r1, r2, -33",
    "lb r1, 0(r2)\nsb r3, -5(r4)\nlb r1, (r2)\nsb r3, 31(r7)\nlb r1, 32(r2)", "lb r1, r2\nlb r1 0(r2)\nlb r1, 0(r9)", "start:\n  jmp start\n  j start\n  hlt",
    "a: b: hlt", "метка:\n  li r1, 1\n  beqz r1, метка\n  bnez r1, метка\n  hlt", "x:\nx:\n hlt", "1abc: hlt", "li r1, 1 ; комментарий\nli r2, 2 # другой\n; целая строка\n# ещё",
    "li r1, ';'\nli r2, '#'\nli r3, ','", ".equ N, 10\nli r1, N\naddi r2, r2, N\n.equ M, 'x'\nli r3, M", ".equ\n.equ X\n.equ X, 1, 2\n.equ 1X, 5\n.equ Y, zzz",
    "nop\nmv r1, r2\ninc r3\ndec r4\nbeqz r1, f\nbnez r2, f\nbgtu r1, r2, f\nbleu r1, r2, f\nj f\nf: hlt", "nop 1\nmv r1\ninc\ndec r1, r2\nbeqz r1\nbgtu r1, r2\nj", "foo r1\nBAR", "HLT\nLi R1, 5\nADD r1, R2, ZERO\nsub zero, r1, r1",
    "beq r1, r2, nowhere", "beq r1, r2, 5\nbne r1, r2, -3\nbltu r1, r2, 31\nbgeu r1, r2, 32\nbeq r1, r2, -33", "jmp 2047\njmp -2048\njmp 2048\njmp -2049", "jmp +3\nhlt\nhlt\nhlt",
    "li r1\nli r1, 2, 3\nli 5, 5\nli r1, abc", "hlt 1", "add r1, r2\nadd r1, r2, r3, r4\nadd r1, r2, 5", "li r8, 1\nli r-1, 1", "  \t li   r1 ,  7  \n\t hlt  ", "li r1, 1\r\nli r2, 2\r\nhlt\r\n",
    "loop:\n  addi r1, r1, 1\n  bne r1, r2, loop\n  hlt", "li r1, 1\nli r2, 2\nloop: beq r1, r2, done\n  inc r1\n  j loop\ndone: hlt", "li r1, 0x\nli r2, 0b\nli r3, 0b102\nli r4, 12abc", "li r1, ''\nli r2, 'ab'\nli r3, '", "li r1, 'я'",
    "x: li r1, 1\n   jmp x", "метка: nop\nМетка: nop\nj метка", "_a: hlt\nj _a", "end: hlt\n" + "nop\n".repeat(300),
  ];
  for (const src of snippets) {
    const r = assemble(src);
    golden.assembler.push({ source: src, words: r.words, lines: r.lines, labels: r.labels, errors: r.errors, disasm: r.words.map((w) => disassemble(w)) });
  }
  for (let w = 0; w < 65536; w += 257) golden.assembler.push({ source: null, word: w, disasm: disassemble(w) });

  /* процессор Мини-8: эмулятор и машина на вентилях на заданиях главы 15 и на отдельных программах */
  const view = (m) => { const v = m.view(); return { regs: v.regs, pc: v.pc, mem: hexOf(v.mem), halted: v.halted, error: v.error, steps: v.steps, last_read: v.lastRead, last_write: v.lastWrite, last_reg: v.lastReg }; };
  const progs = [];
  for (const t of ASM) progs.push({ name: "task:" + t.id, source: t.solution, disk: Array.from(t.disk), task: t.id });
  const D0 = new Array(256).fill(0);
  const extra = {
    alu: "li r1, 200\nli r2, 100\nadd r3, r1, r2\nsub r4, r2, r1\nand r5, r1, r2\nor r6, r1, r2\nxor r7, r1, r2\nhlt",
    imm: "li r1, 10\naddi r2, r1, -5\naddi r3, r2, 31\naddi r4, r3, -32\nmv r5, r4\nnop\ninc r6\ndec r7\nhlt",
    mem: "li r1, 0x20\nli r2, 0xAB\nsb r2, 0(r1)\nsb r2, 1(r1)\nlb r3, 1(r1)\nlb r4, -1(r1)\nsb r3, -32(r1)\nhlt",
    branches: "li r1, 3\nli r2, 5\nbltu r1, r2, a\nli r3, 1\na: bgeu r2, r1, b\nli r4, 1\nb: bne r1, r2, c\nli r5, 1\nc: beq r1, r1, d\nli r6, 1\nd: bgeu r1, r2, e\nli r7, 9\ne: hlt",
    jmpback: "li r1, 5\nloop: dec r1\nbnez r1, loop\nli r2, 77\nj end\nli r3, 1\nend: hlt",
    zero: "li r0, 5\naddi r0, r0, 1\nadd r1, r0, r0\nhlt",
    runoff: "li r1, 1\nli r2, 2",
    forever: "loop: j loop",
    sum: "li r1, 0\nli r2, 1\nli r3, 11\nloop: add r1, r1, r2\ninc r2\nbne r2, r3, loop\nhlt",
  };
  for (const [name, source] of Object.entries(extra)) progs.push({ name, source, disk: D0, task: null });
  for (const p of progs) {
    const a = assemble(p.source);
    if (a.errors.length) throw new Error("пример " + p.name + ": " + JSON.stringify(a.errors));
    const entry = { name: p.name, source: p.source, disk: hexOf(Uint8Array.from(p.disk)), words: a.words };
    const m = new Machine(a.words, p.disk);
    const first = [];
    const g = new GateMachine(a.words, p.disk);
    const gfirst = [];
    for (let i = 0; i < 24; i++) {
      m.step(); g.step();
      first.push({ regs: [...m.regs], pc: m.pc, halted: m.halted, error: m.error });
      gfirst.push({ regs: g.regs(), pc: g.pc, halted: g.halted, error: g.error });
    }
    const limit = p.name === "forever" ? 2000 : 100000;
    const m2 = new Machine(a.words, p.disk); m2.run(limit);
    const g2 = new GateMachine(a.words, p.disk); g2.run(limit);
    entry.emu_first = first; entry.gate_first = gfirst;
    entry.limit = limit; entry.emu = view(m2); entry.gate = view(g2);
    if (p.task) {
      const t = ASM.find((x) => x.id === p.task);
      entry.check = t.check(m2.view().mem);
      // искажения итоговой памяти: расхождения в одном и нескольких байтах
      const checks = [];
      const mem = m2.view().mem;
      const variants = [[], [0x10], [0x10, 0x11, 0x12], [0x0e], [0xff], [0x00, 0x7f]];
      for (const diffs of variants) {
        const mm = Uint8Array.from(mem);
        for (const a of diffs) mm[a] = (mm[a] + (a % 2 ? 1 : 33)) & 0xff;
        const r = t.check(mm);
        checks.push({ mem: hexOf(mm), ok: r.ok, message: r.message });
      }
      entry.checks = checks;
    }
    golden.cpu8.push(entry);
  }
  return { chapters, golden };
}
`;

const code = entry
  .replaceAll("__LAB__", lab)
  .replace("__CHAPTERS__", JSON.stringify(CIRCUIT_CHAPTERS))
  .replace("__ASM__", String(ASM_CHAPTER));
fs.writeFileSync(path.join(tmp, "entry.ts"), code);
await build({
  entryPoints: [path.join(tmp, "entry.ts")], bundle: true, platform: "node", format: "esm",
  outfile: path.join(tmp, "bundle.mjs"), nodePaths: [path.join(root, "node_modules")], logLevel: "error",
});
const m = await import(pathToFileURL(path.join(tmp, "bundle.mjs")).href);
const { chapters, golden } = m.run();
fs.mkdirSync(path.dirname(outData), { recursive: true });
fs.mkdirSync(path.dirname(outGolden), { recursive: true });
fs.writeFileSync(outData, JSON.stringify({ chapters }));
fs.writeFileSync(outGolden, JSON.stringify(golden));
const tasks = chapters.reduce((s, c) => s + c.tasks.length, 0);
console.log(`глав ${chapters.length}, упражнений ${tasks} → ${outData}`);
console.log(`золото: схем ${golden.circuits.length}, проверок ${golden.verdicts.length}, блоков ${golden.blocks.length}, ассемблер ${golden.assembler.length}, программ ${golden.cpu8.length} → ${outGolden}`);
if (golden.noSolution.length) console.log("без эталонного решения:", golden.noSolution.join(", "));
fs.rmSync(tmp, { recursive: true, force: true });
