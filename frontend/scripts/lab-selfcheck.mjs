// Самопроверка лаборатории: эталонные решения проходят проверку упражнений.
//   схемы (режим таблицы) — эталонные нетлисты дают целевые таблицы;
//   ассемблер Мини-8 и RISC-V — эталонные программы доходят до верного итога на эмуляторах.
// Запуск: cd frontend && node scripts/lab-selfcheck.mjs
import { build } from "esbuild";
import { mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

const dir = mkdtempSync(join(tmpdir(), "lab-check-"));
const entry = join(dir, "entry.ts");
const root = new URL("../src/lab/", import.meta.url).pathname;
writeFileSync(
  entry,
  `
import { SECTIONS } from "${root}sections/sections";
import { SECTION_SOLUTIONS } from "${root}exercises/logic-gates/solutions";
import { inputsForRow, outputValue } from "${root}exercises/logic-gates/circuit.model";
import { TASKS as ASM } from "${root}asm/tasks";
import { assemble as asmAssemble } from "${root}asm/assembler";
import { Machine } from "${root}asm/machine";
import { RV_TASKS, fullSource } from "${root}riscv/rv-tasks";
import { REAL_TASKS } from "${root}riscv/rv-real-tasks";
import { assemble as rvAssemble } from "${root}riscv/rv-asm";
import { RvMachine } from "${root}riscv/rv-machine";

function circuitFrom(ex, net, outs) {
  const labels = ex.labels ?? ex.inputs;
  const gid = (n) => "g_" + n;
  const resolve = (name) => {
    const li = labels.indexOf(name);
    if (li >= 0) return ex.inputs[li];
    if (name in net) return gid(name);
    throw new Error("нет источника " + name);
  };
  let w = 0;
  const wire = (from, to, pin) => ({ id: "w" + ++w, from: { node: from, pin: "out" }, to: { node: to, pin } });
  const gates = [];
  const wires = [];
  for (const [name, [type, a, b]] of Object.entries(net)) {
    gates.push({ id: gid(name), type, x: 0, y: 0 });
    wires.push(wire(resolve(a), gid(name), "in0"));
    if (type !== "NOT") wires.push(wire(resolve(b), gid(name), "in1"));
  }
  for (const [o, src] of Object.entries(outs)) wires.push(wire(resolve(src), o, "in0"));
  return { gates, wires };
}

export function run() {
  const bad = [];
  let n = 0;
  for (const s of SECTIONS) {
    const sols = SECTION_SOLUTIONS[s.slug] ?? {};
    for (const ex of s.exercises) {
      const sol = sols[ex.id];
      if (!sol || (ex.mode ?? "table") !== "table" || ex.kind === "blocks") continue;
      n++;
      const c = circuitFrom(ex, sol.net, sol.outs);
      for (let row = 0; row < ex.target.length; row++) {
        const inputs = inputsForRow(ex.inputs, row);
        const got = ex.outputs.map((o) => outputValue(c, inputs, o));
        if (JSON.stringify(got) !== JSON.stringify(ex.target[row])) {
          bad.push(s.slug + "/" + ex.id + " строка " + row);
          break;
        }
      }
    }
  }
  for (const t of ASM) {
    n++;
    const a = asmAssemble(t.solution);
    if (a.errors.length) { bad.push("asm/" + t.id + ": ошибки ассемблера"); continue; }
    const m = new Machine(a.words, t.disk);
    m.run(100000);
    const v = m.view();
    if (v.error || !v.halted || !t.check(v.mem).ok) bad.push("asm/" + t.id);
  }
  for (const [kind, list] of [["riscv", RV_TASKS], ["real", REAL_TASKS]]) {
    for (const t of list) {
      n++;
      const a = rvAssemble(fullSource(t.solution, t));
      if (a.errors.length) { bad.push(kind + "/" + t.id + ": ошибки ассемблера"); continue; }
      const m = new RvMachine(a.image, { switches: t.switches, entry: a.entry });
      m.run(200000);
      const v = m.view();
      if (v.error || !v.halted || !t.check(v, a.symbols).ok) bad.push(kind + "/" + t.id);
    }
  }
  return { n, bad };
}
`,
);
const out = join(dir, "entry.mjs");
await build({ entryPoints: [entry], bundle: true, platform: "node", format: "esm", outfile: out, logLevel: "error" });
const { run } = await import(pathToFileURL(out).href);
const { n, bad } = run();
console.log(`проверено решений: ${n}`);
if (bad.length) {
  console.log("не прошли:\n  " + bad.join("\n  "));
  process.exit(1);
}
console.log("всё в порядке");
