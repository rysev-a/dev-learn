// Строит backend/app/exercises/net_tasks/lab_manifest.json из сценариев симулятора сети
// (frontend/src/netlab): {глава: [{id, mode: "lab", title, statement, starter, hint}]}.
// Запуск: cd frontend && npm run net:manifest
import { writeFileSync } from "node:fs";
import { NET_CHAPTERS, netTasks } from "../src/netlab/registry.js";

const manifest = {};
for (const n of Object.keys(NET_CHAPTERS))
  manifest[n] = netTasks(Number(n)).map((t) => ({ id: t.id, mode: "lab", title: t.title, statement: t.text, starter: "", hint: t.hint }));
writeFileSync(new URL("../../backend/app/exercises/net_tasks/lab_manifest.json", import.meta.url), JSON.stringify(manifest, null, 1) + "\n");
console.log("manifest:", Object.entries(manifest).map(([n, l]) => `${n}:${l.length}`).join(" "));
