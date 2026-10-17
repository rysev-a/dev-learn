// Строит backend/app/exercises/sd_tasks/lab_manifest.json из сценариев лаборатории «Системный дизайн»
// (frontend/src/sdlab): {глава: [{id, mode: "lab", title, statement, starter, hint}]}.
// Запуск: cd frontend && npm run sd:manifest
import { writeFileSync } from "node:fs";
import { SD_CHAPTERS, sdTasks } from "../src/sdlab/registry.ts";

const manifest = {};
for (const n of Object.keys(SD_CHAPTERS))
  manifest[n] = sdTasks(Number(n)).map((t) => ({ id: t.id, mode: "lab", title: t.title, statement: t.text, starter: "", hint: t.hint }));
writeFileSync(new URL("../../backend/app/exercises/sd_tasks/lab_manifest.json", import.meta.url), JSON.stringify(manifest, null, 1) + "\n");
console.log("manifest:", Object.entries(manifest).map(([n, l]) => `${n}:${l.length}`).join(" "));
