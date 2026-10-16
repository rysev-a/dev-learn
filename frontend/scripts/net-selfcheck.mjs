// Самопроверка лаборатории сетей: на исходной сети хотя бы одна цель не выполнена, а после
// шагов эталонного решения выполнены все. Запуск: cd frontend && node scripts/net-selfcheck.mjs
import { NET_CHAPTERS } from "../src/netlab/registry.ts";
import { applyOps, checkGoals } from "../src/netlab/check.ts";

let bad = 0;
for (const [ch, list] of Object.entries(NET_CHAPTERS)) {
  for (const s of list) {
    const start = checkGoals(s.build(), s.goals);
    const startOk = start.every((r) => r.ok);
    let solved;
    try {
      const st = s.build();
      solved = checkGoals(applyOps(st, typeof s.solution === "function" ? s.solution(st) : s.solution), s.goals);
    } catch (e) {
      console.log(`✗ ${ch}/${s.id}: решение упало: ${e.message}`);
      bad++;
      continue;
    }
    const ok = solved.every((r) => r.ok);
    if (startOk || !ok) {
      bad++;
      console.log(`✗ ${ch}/${s.id}: ${startOk ? "уже решено в заготовке; " : ""}${ok ? "" : "эталон не проходит"}`);
      for (const r of (startOk ? start : solved).filter((r) => !r.ok || startOk))
        console.log(`    ${r.ok ? "✓" : "✗"} ${r.text}: ${r.detail}`);
    } else {
      console.log(`✓ ${ch}/${s.id}: заготовка не проходит (${start.filter((r) => !r.ok).length} из ${start.length}), эталон проходит`);
    }
  }
}
process.exit(bad ? 1 : 0);
