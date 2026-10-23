// Выгрузка упражнений лаборатории «Системный дизайн» (книга 18) в JSON: по файлу на главу — сценарии как данные
// и «золотые» результаты TypeScript-движка (evaluate, checkGoals) для дифференциальных тестов Rust-крейта `shared-rs/sdlab`.
// Один раз переводит сценарии из кода в данные; дальше `cargo run --bin import` (shared-rs/sdlab) пишет канонические файлы
// backend/app/data/labs/sd. Запуск: node scripts/sd-export.mjs <каталог вывода>
import { build } from "esbuild";
import fs from "fs";
import os from "os";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outDir = path.resolve(process.argv[2] || "sd-export");
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "sd-export-"));
const sd = path.join(root, "src/sdlab");

const entry = `
export { SD_CHAPTERS, SD_BOOK } from ${JSON.stringify(path.join(sd, "registry.ts"))};
export { evaluate, canLink } from ${JSON.stringify(path.join(sd, "engine.ts"))};
export { checkGoals } from ${JSON.stringify(path.join(sd, "checks.ts"))};
export { KINDS, KIND_ORDER, defaultParams } from ${JSON.stringify(path.join(sd, "kinds.ts"))};
export { reaches, suggestEdges } from ${JSON.stringify(path.join(sd, "ports.ts"))};
`;
fs.writeFileSync(path.join(tmp, "entry.ts"), entry);
await build({
  entryPoints: [path.join(tmp, "entry.ts")], bundle: true, platform: "node", format: "esm", outfile: path.join(tmp, "bundle.mjs"),
  nodePaths: [path.join(root, "node_modules")], logLevel: "error",
});
const T = await import(pathToFileURL(path.join(tmp, "bundle.mjs")).href);

/* ---------- детерминированный генератор случайных схем (mulberry32) ---------- */

function seedOf(str) {
  let h = 2166136261;
  for (const c of str) h = Math.imul(h ^ c.charCodeAt(0), 16777619);
  return h >>> 0;
}
function mulberry32(a) {
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const clone = (x) => JSON.parse(JSON.stringify(x));

function randomParam(spec, rng) {
  if (spec.type === "int") return spec.min + Math.floor(rng() * (spec.max - spec.min + 1));
  if (spec.type === "bool") return rng() < 0.5;
  return spec.options[Math.floor(rng() * spec.options.length)].value;
}

/** случайная правка эталона: параметры, лишние узлы и связи, нагрузка — чтобы пройти как можно больше веток движка */
function mutate(solution, wl0, rng) {
  const s = clone(solution);
  const wl = clone(wl0);
  const pick = (arr) => arr[Math.floor(rng() * arr.length)];
  for (const n of s.nodes) {
    if (n.kind === "clients") continue;
    for (const spec of T.KINDS[n.kind].params) if (rng() < 0.3) n.params[spec.key] = randomParam(spec, rng);
  }
  const extra = rng() < 0.7 ? 1 + Math.floor(rng() * 3) : 0;
  for (let i = 0; i < extra; i++) {
    const kind = pick(T.KIND_ORDER);
    const node = { id: `${kind}_m${i}`, kind, name: T.KINDS[kind].label, x: 100 + i * 40, y: 100 + i * 40, params: T.defaultParams(kind) };
    for (const spec of T.KINDS[kind].params) if (rng() < 0.4) node.params[spec.key] = randomParam(spec, rng);
    const tryLink = (a, b) => {
      if (a.id === b.id || !T.canLink(a.kind, b.kind)) return;
      if (s.edges.some((e) => e.from === a.id && e.to === b.id)) return;
      if (T.reaches(s.edges, b.id, a.id)) return;
      s.edges.push({ from: a.id, to: b.id });
    };
    s.nodes.push(node);
    for (const o of s.nodes) {
      if (rng() < 0.45) tryLink(o, node);
      if (rng() < 0.45) tryLink(node, o);
    }
  }
  for (let i = 0; i < 4; i++) {
    const a = pick(s.nodes);
    const b = pick(s.nodes);
    if (a.id !== b.id && T.canLink(a.kind, b.kind) && !s.edges.some((e) => e.from === a.id && e.to === b.id) && !T.reaches(s.edges, b.id, a.id) && rng() < 0.5)
      s.edges.push({ from: a.id, to: b.id });
  }
  if (s.edges.length && rng() < 0.3) s.edges.splice(Math.floor(rng() * s.edges.length), 1);
  const f = pick([0.3, 0.7, 1, 1, 1.5, 3, 10]);
  for (const k of ["static", "read", "write"]) if (wl[k]) wl[k] = Math.round(wl[k] * pick([0.3, 0.7, 1, 1.5, 3, 10]) * 10) / 10;
  if (rng() < 0.3) wl.dataGB = Math.round(wl.dataGB * f * 10) / 10 || 1;
  if (rng() < 0.2) wl.hotSet = pick([0.05, 0.2, 0.6, 1]);
  if (rng() < 0.4) wl.hotKey = pick([0, 0.1, 0.3, 0.6]);
  if (rng() < 0.4) wl.searchShare = pick([0, 0.1, 0.4, 1]);
  if (rng() < 0.3) wl.connections = pick([1000, 20000, 200000]);
  if (rng() < 0.3) wl.msgPerConn = pick([0.1, 1, 5]);
  if (rng() < 0.3) wl.spikeSec = pick([0, 10, 60]);
  if (rng() < 0.3) wl.monotonic = rng() < 0.5;
  if (rng() < 0.3) wl.fanout = pick([0, 20, 200, 2000]);
  if (rng() < 0.3) wl.geoUpdates = pick([0, 300, 5000]);
  if (rng() < 0.3) wl.mediaTB = pick([0, 2, 50]);
  if (rng() < 0.4) wl.calls = Object.fromEntries(["auth", "geo", "ml", "pay"].filter(() => rng() < 0.6).map((k) => [k, pick([0.1, 0.3, 1])]));
  return { state: s, workload: wl };
}

/* ---------- золотые результаты ---------- */

let nonFinite = 0;
const finiteCheck = (r) => {
  const walk = (v) => {
    if (typeof v === "number" && !Number.isFinite(v)) nonFinite++;
    else if (v && typeof v === "object") Object.values(v).forEach(walk);
  };
  walk(r);
  return r;
};

function goldenCases(sc) {
  const cases = [];
  const add = (label, state, workload, opts, withGoals) => {
    const wl = workload ?? sc.workload;
    const c = { label, state, opts, result: finiteCheck(T.evaluate(typeof state === "string" ? sc[state] : state, wl, opts)) };
    if (workload) c.workload = workload;
    if (withGoals) c.goals = T.checkGoals(typeof state === "string" ? sc[state] : state, wl, sc.goals);
    cases.push(c);
  };
  add("start", "start", null, {}, true);
  add("solution", "solution", null, {}, true);
  const kinds = [...new Set(sc.solution.nodes.map((n) => n.kind))].filter((k) => k !== "clients" && k !== "monitor");
  for (const f of ["zone", "region", "deploy", ...kinds.slice(0, 3)]) add(`solution fail:${f}`, "solution", null, { fail: f });
  const startKinds = [...new Set(sc.start.nodes.map((n) => n.kind))].filter((k) => k !== "clients" && k !== "monitor");
  for (const f of ["zone", ...startKinds.slice(0, 1)]) add(`start fail:${f}`, "start", null, { fail: f });
  const firstNode = sc.solution.nodes.find((n) => n.kind !== "clients");
  if (firstNode) add("solution down", "solution", null, { down: [firstNode.id] });
  const rng = mulberry32(seedOf(sc.id));
  for (let i = 0; i < 6; i++) {
    const m = mutate(sc.solution, sc.workload, rng);
    const fail = rng() < 0.5 ? ["zone", "region", "deploy", ...T.KIND_ORDER][Math.floor(rng() * (3 + T.KIND_ORDER.length))] : undefined;
    const opts = fail ? { fail } : {};
    if (!fail && rng() < 0.15) opts.down = [m.state.nodes[Math.floor(rng() * m.state.nodes.length)].id];
    add(`mutant ${i}${fail ? ` fail:${fail}` : ""}`, m.state, m.workload, opts, i < 3);
  }
  return cases;
}

/** автосвязи: для нескольких узлов эталона убираем их связи и спрашиваем, какие связи подставит поле */
function suggestCases(sc) {
  const out = [];
  for (const n of sc.solution.nodes.filter((x) => x.kind !== "clients").slice(0, 4)) {
    const stripped = { nodes: sc.solution.nodes, edges: sc.solution.edges.filter((e) => e.from !== n.id && e.to !== n.id) };
    out.push({ node: n.id, edges: T.suggestEdges(stripped, n, [], 230) });
  }
  return out;
}

fs.mkdirSync(outDir, { recursive: true });
let tasks = 0;
let cases = 0;
for (const [ch, list] of Object.entries(T.SD_CHAPTERS)) {
  const out = {
    book: T.SD_BOOK,
    chapter: Number(ch),
    tasks: list.map((s) => {
      const golden = { cases: goldenCases(s), suggest: suggestCases(s) };
      cases += golden.cases.length;
      tasks++;
      return { ...s, golden };
    }),
  };
  fs.writeFileSync(path.join(outDir, `${T.SD_BOOK}-${String(ch).padStart(2, "0")}.json`), JSON.stringify(out));
}
console.log(`упражнений ${tasks}, золотых случаев ${cases}, нечисловых значений в результатах ${nonFinite} → ${outDir}`);
fs.rmSync(tmp, { recursive: true, force: true });
