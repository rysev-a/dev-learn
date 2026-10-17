// Самопроверка лаборатории «Системный дизайн»: в исходной схеме хотя бы одна цель не выполнена,
// а в эталонной выполнены все. Запуск: cd frontend && npm run sd:check
import { SD_CHAPTERS } from "../src/sdlab/registry.ts";
import { checkGoals } from "../src/sdlab/checks.ts";

let bad = 0;
let total = 0;
const ids = new Set();
for (const [ch, list] of Object.entries(SD_CHAPTERS)) {
  for (const s of list) {
    total++;
    if (ids.has(s.id)) {
      console.log(`✗ ${ch}/${s.id}: повторяется id`);
      bad++;
    }
    ids.add(s.id);
    const start = checkGoals(s.start, s.workload, s.goals);
    const startOk = start.every((r) => r.ok);
    const sol = checkGoals(s.solution, s.workload, s.goals);
    const ok = sol.every((r) => r.ok);
    const kinds = new Set(s.solution.nodes.map((n) => n.kind));
    const outside = [...kinds].filter((k) => k !== "clients" && k !== "monitor" && !s.palette.includes(k) && !s.start.nodes.some((n) => n.kind === k));
    if (startOk || !ok || outside.length || s.solution.nodes.length > (s.maxNodes ?? 14)) {
      bad++;
      console.log(`✗ ${ch}/${s.id}: ${startOk ? "уже решено в исходной схеме; " : ""}${ok ? "" : "эталон не проходит; "}${outside.length ? `компоненты вне палитры: ${outside.join(", ")}; ` : ""}`);
      for (const r of startOk ? start : sol.filter((r) => !r.ok)) console.log(`    ${r.ok ? "✓" : "✗"} ${r.text}: ${r.detail}`);
    } else {
      console.log(`✓ ${ch}/${s.id}: исходная схема не проходит (${start.filter((r) => !r.ok).length} из ${start.length}), эталон проходит`);
    }
  }
}
console.log(`упражнений: ${total}, проблем: ${bad}`);
process.exit(bad ? 1 : 0);
