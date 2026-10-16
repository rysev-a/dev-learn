// Правила строгости, которые не выражаются флагами tsc: явный any и подавление ошибок типов запрещены.
// Запуск: npm run typecheck (после tsc)
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../src");
const RULES = [
  [/(?<!:):\s*any\b|<any>|\bas any\b|\bany\[\]/, "явный any"],
  [/@ts-(ignore|nocheck|expect-error)/, "подавление ошибок типов"],
];
const bad = [];
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (/\.(ts|tsx)$/.test(e.name))
      fs.readFileSync(p, "utf8").split("\n").forEach((line, i) => {
        for (const [rx, what] of RULES) if (rx.test(line.replace(/\/\/.*$/, "")) ) bad.push(`${path.relative(root, p)}:${i + 1}: ${what}`);
      });
  }
})(root);
if (bad.length) {
  console.error(bad.join("\n"));
  process.exit(1);
}
console.log("ts-guard: нарушений нет");
