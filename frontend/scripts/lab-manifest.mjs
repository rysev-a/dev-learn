// Строит backend/app/exercises/arch_tasks/lab_manifest.json из данных лаборатории
// (frontend/src/lab): {глава: [{id, mode: "lab", title, statement, starter, hint}]}.
// Запуск: cd frontend && node scripts/lab-manifest.mjs
import { build } from "esbuild";
import { writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

const dir = mkdtempSync(join(tmpdir(), "lab-manifest-"));
const out = join(dir, "reg.mjs");
await build({ entryPoints: ["src/lab/registry.js"], bundle: true, platform: "node", format: "esm", outfile: out, logLevel: "error" });
const { LAB_CHAPTERS, labTasks } = await import(pathToFileURL(out).href);
const manifest = {};
for (const n of Object.keys(LAB_CHAPTERS))
  manifest[n] = labTasks(Number(n)).map((t) => ({ id: t.id, mode: "lab", title: t.title, statement: t.text, starter: "", hint: t.hint }));
const target = "../backend/app/exercises/arch_tasks/lab_manifest.json";
writeFileSync(target, JSON.stringify(manifest, null, 1) + "\n");
console.log("manifest:", Object.entries(manifest).map(([n, l]) => `${n}:${l.length}`).join(" "));
