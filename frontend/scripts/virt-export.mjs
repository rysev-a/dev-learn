// «Золотые» результаты моделей лаборатории книги «Виртуализация» (frontend/src/virtlab/*.ts) на наборах входов:
// по ним дифференциальные тесты крейта shared-rs/virtlab проверяют, что Rust-модели совпадают с TypeScript бит в бит.
// Обработчики интерфейса (HvLab, VirtqLab, Qcow2Lab, NumaLab, MigrationLab), где живёт логика целей, повторены здесь
// дословно (они в компонентах React и из-за этого не импортируются).
// Запуск: node scripts/virt-export.mjs [файл вывода]   (по умолчанию ../shared-rs/virtlab/tests/golden/virt.json)
import { build } from "esbuild";
import fs from "fs";
import os from "os";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outFile = path.resolve(process.argv[2] || path.join(root, "../shared-rs/virtlab/tests/golden/virt.json"));
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "virt-export-"));
const dir = path.join(root, "src/virtlab");

const entry = `
import * as hv from ${JSON.stringify(path.join(dir, "hv.ts"))};
import * as ept from ${JSON.stringify(path.join(dir, "ept.ts"))};
import * as vq from ${JSON.stringify(path.join(dir, "virtq.ts"))};
import * as numa from ${JSON.stringify(path.join(dir, "numa.ts"))};
import * as qc from ${JSON.stringify(path.join(dir, "qcow2.ts"))};
import * as mg from ${JSON.stringify(path.join(dir, "migration.ts"))};
export { hv, ept, vq, numa, qc, mg };
`;
fs.writeFileSync(path.join(tmp, "entry.ts"), entry);
await build({
  entryPoints: [path.join(tmp, "entry.ts")], bundle: true, platform: "node", format: "cjs", outfile: path.join(tmp, "bundle.cjs"),
  nodePaths: [path.join(root, "node_modules")], logLevel: "error",
});
const { hv, ept, vq, numa, qc, mg } = await import(pathToFileURL(path.join(tmp, "bundle.cjs")).href).then((m) => m.default ?? m);

// детерминированный ГПСЧ для наборов входов (не из моделей)
function rng(seed) {
  let x = seed >>> 0;
  return (n) => {
    x = (Math.imul(x, 1664525) + 1013904223) >>> 0;
    return (x >>> 8) % n;
  };
}

/* ---------------- hv ---------------- */
function hvGolden() {
  const programs = hv.PROGRAMS.map((p) => ({ id: p.id, title: p.title, code: p.code, goal: p.goal, expected: hv.expected(p.code) }));
  // идеальный проход каждой программы с трансляцией и без неё
  const walks = [];
  for (const p of hv.PROGRAMS)
    for (const translate of [false, true]) {
      let s = hv.initial();
      const steps = [];
      for (let guard = 0; guard < 50 && !s.halted && p.code[s.pc] !== undefined; guard++) {
        const ins = p.code[s.pc];
        const info = hv.inspect(ins, s, translate);
        let next;
        if (info.kind === "silent") next = { ...s, pc: s.pc + 1, queue: [...s.queue], delivered: [...s.delivered], silent: true };
        else next = hv.apply(ins, s);
        steps.push({ ins, state: s, inspection: info, after: next });
        s = next;
      }
      walks.push({ program: p.id, translate, steps });
    }
  // отдельные пробы: каждая команда на нескольких состояниях
  const states = [
    hv.initial(),
    { ...hv.initial(), vif: 0, queue: [1, 2], delivered: [9], acc: 5, vcr3: 7, pc: 3 },
    { ...hv.initial(), vif: 1, acc: -2, vcr3: 4096, pc: 1, mistakes: 2 },
  ];
  const probes = [];
  for (const ins of ["ADD 3", "ADD -4", "CLI", "STI", "WRCR3 4096", "WRCR3 0", "RDCR3", "HLT", "IRQ 1", "IRQ 7", "POPF 1", "POPF 0", "NOP"])
    for (const state of states)
      for (const translate of [false, true])
        probes.push({ ins, state, translate, inspection: hv.inspect(ins, state, translate), after: hv.apply(ins, state) });
  return { programs, walks, probes };
}

/* ---------------- ept ---------------- */
function eptGolden() {
  const sizes = ["4K", "2M", "1G"];
  const modes = ["shadow", "ept"];
  const walks = [];
  const runs = [];
  for (const mode of modes)
    for (const guest of sizes)
      for (const host of sizes) {
        walks.push({ mode, guest, host, walk: ept.walkCost(mode, guest, host) });
        for (const w of ept.WORKLOADS) {
          const r = ept.simulate({ mode, guest, host, workload: w.id });
          runs.push({
            mode, guest, host, workload: w.id,
            result: { walk: r.walk, accesses: r.accesses, misses: r.misses, hits: r.hits, exits: r.exits, cost: r.cost, eff_page: r.effPage },
            goals: ept.GOALS.filter((g) => g.workload === w.id && g.check(r, { mode, guest, host })).map((g) => g.id),
          });
        }
      }
  const workloads = ept.WORKLOADS.map((w) => {
    const t = w.make();
    return {
      id: w.id, title: w.title, note: w.note, len: t.addrs.length, maps: t.maps,
      sum: t.addrs.reduce((a, b) => a + b, 0), first: t.addrs.slice(0, 8), last: t.addrs.slice(-8),
    };
  });
  return { goals: ept.GOALS.map((g) => ({ id: g.id, text: g.text, workload: g.workload })), workloads, walks, runs };
}

/* ---------------- virtq (логика целей — как в VirtqLab) ---------------- */
function virtqGolden() {
  const r = rng(2024);
  const sequences = [];
  for (let q = 0; q < 25; q++) {
    let s = vq.initial();
    let suppress = false;
    const done = [];
    const steps = [];
    const mark = (next) => {
      for (const g of vq.GOALS) if (g.check(next, { suppress }) && !done.includes(g.id)) done.push(g.id);
    };
    for (let i = 0; i < 40; i++) {
      const pick = r(10);
      let act;
      if (pick < 3) act = { op: "post", n: [1, 3, 2, 4, 6][r(5)] };
      else if (pick < 6) act = { op: "device" };
      else if (pick < 8) act = { op: "reap" };
      else if (pick < 9) act = { op: "suppress", on: !suppress };
      else act = r(3) === 0 ? { op: "reset" } : { op: "post", n: 3 };
      if (act.op === "post") {
        const t = vq.post(s, act.n, suppress);
        s = t;
        mark(s);
      } else if (act.op === "device") {
        if (s.busy && s.avail !== 0) {
          s = vq.device(s);
          mark(s);
        }
      } else if (act.op === "reap") {
        s = vq.reap(s);
        mark(s);
      } else if (act.op === "suppress") suppress = act.on;
      else s = vq.initial();
      steps.push({ action: act, suppress, state: s, free: vq.free(s), done: [...done] });
    }
    sequences.push(steps);
  }
  return { size: vq.SIZE, goals: vq.GOALS.map((g) => ({ id: g.id, text: g.text })), sequences };
}

/* ---------------- numa ---------------- */
function numaGolden() {
  const r = rng(77);
  const places = ["0", "1", "wide"];
  const scenarios = numa.SCENARIOS.map((sc) => {
    const cases = [];
    for (let i = 0; i < 120; i++) {
      const vnuma = r(2) === 1;
      const plan = Object.fromEntries(sc.vms.map((v) => [v.name, { cpu: places[r(3)], mem: places[r(3)], vnuma }]));
      const ev = numa.evaluate(sc.vms, plan);
      const accepted = !ev.over && !(ev.avg > sc.max + 1e-9);
      cases.push({ plan, load: ev.load, over: ev.over, per: ev.per, avg: ev.avg, accepted });
    }
    return { id: sc.id, title: sc.title, vms: sc.vms, goal: sc.goal, max: sc.max, cases };
  });
  const remote = [];
  for (const cpu of places) for (const mem of places) for (const vnuma of [false, true]) remote.push({ cpu, mem, vnuma, remote: numa.remote(cpu, mem, vnuma) });
  return { nodes: numa.NODES, scenarios, remote };
}

/* ---------------- qcow2 (логика целей — как в Qcow2Lab) ---------------- */
function qcowGolden() {
  const r = rng(555);
  const letters = "EFGHIJKLMNOPQRSTUVWXYZ".split("");
  const strip = (chain) => chain.map((l) => ({ name: l.name, data: l.data }));
  const sequences = [];
  for (let q = 0; q < 30; q++) {
    let chain = qc.initialChain();
    let maxLen = 1;
    let snaps = 0;
    let dropped = null;
    const done = [];
    const mark = (id) => {
      if (!done.includes(id)) done.push(id);
    };
    const steps = [];
    const set = (c) => {
      chain = c;
      maxLen = Math.max(maxLen, c.length);
    };
    for (let i = 0; i < 30; i++) {
      const pick = r(10);
      const cluster = r(8);
      let act;
      let out = null;
      if (pick < 2) {
        act = { op: "snapshot" };
        snaps += 1;
        set(qc.snapshot(chain, snaps));
      } else if (pick < 5) {
        act = { op: "write", cluster, data: letters[r(letters.length)] };
        const w = qc.write(chain, cluster, act.data);
        set(w.chain);
        out = { copy_up: w.copyUp };
      } else if (pick < 8) {
        act = { op: "read", cluster };
        const rd = qc.read(chain, cluster);
        out = { value: rd.value, depth: rd.depth, lookups: rd.lookups, layer: rd.layer };
        if (rd.value != null && rd.lookups >= 4 && chain.length >= 4) mark("deep");
        const d = dropped;
        if (d && cluster in d && rd.value !== d[cluster]) {
          mark("rollback");
          dropped = null;
        }
      } else if (pick < 9) {
        act = { op: "commit" };
        const c = qc.commit(chain);
        out = { ok: c !== null };
        if (c) {
          set(c);
          if (maxLen >= 4 && c.length <= 2) mark("squash");
        }
      } else {
        act = { op: "revert" };
        const c = qc.revert(chain);
        out = { ok: c !== null };
        if (c) {
          const top = chain[0].data;
          dropped = Object.keys(top).length ? { ...top } : null;
          set(c);
        }
      }
      steps.push({ action: act, out, chain: strip(chain), max_len: maxLen, done: [...done] });
    }
    sequences.push(steps);
  }
  return { clusters: qc.CLUSTERS, base: qc.initialChain()[0].data, goals: qc.GOALS, sequences };
}

/* ---------------- migration ---------------- */
function migrationGolden() {
  const cases = [];
  const rows = [];
  for (const sc of mg.SCENARIOS)
    for (const downtimeMs of [20, 100, 300, 600, 1000])
      for (const autoConverge of [false, true])
        for (const compress of [false, true])
          for (const postcopyAfter of [null, 1, 2, 3, 4, 5, 6]) {
            const input = { dirty: sc.dirty, bw: sc.bw, downtimeMs, autoConverge, compress, postcopyAfter };
            const result = mg.simulate(input);
            cases.push({ scenario: sc.id, input, result, ok: sc.check(result) });
          }
  // произвольные скорости, в т. ч. без необязательных полей и с малой памятью
  for (const dirty of [0, 100, 1250, 1300, 4000, 9000])
    for (const bw of [125, 1250, 5000])
      rows.push({ input: { dirty, bw, downtimeMs: 300 }, result: mg.simulate({ dirty, bw, downtimeMs: 300 }) });
  rows.push({ input: { dirty: 500, bw: 1250, downtimeMs: 100, mem: 1024 }, result: mg.simulate({ dirty: 500, bw: 1250, downtimeMs: 100, mem: 1024 }) });
  return {
    mem_mib: mg.MEM_MIB,
    scenarios: mg.SCENARIOS.map((s) => ({ id: s.id, title: s.title, dirty: s.dirty, bw: s.bw, goal: s.goal, hint: s.hint })),
    cases,
    rows,
  };
}

const out = { hv: hvGolden(), ept: eptGolden(), virtq: virtqGolden(), numa: numaGolden(), qcow2: qcowGolden(), migration: migrationGolden() };
fs.mkdirSync(path.dirname(outFile), { recursive: true });
fs.writeFileSync(outFile, JSON.stringify(out));
console.log(`золотые данные virtlab → ${outFile} (${(fs.statSync(outFile).size / 1024).toFixed(0)} КиБ)`);
fs.rmSync(tmp, { recursive: true, force: true });
