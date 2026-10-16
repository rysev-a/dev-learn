// Постепенное включение noUncheckedIndexedAccess: каталоги из COVERED проверяются со строгим доступом по индексу
// (ошибка в них проваливает проверку), остальные только считаются. Когда каталог дочищен — добавьте его в COVERED;
// когда все — перенесите флаг в tsconfig.json и удалите этот скрипт. Запуск: npm run typecheck
import { execFileSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const COVERED = ["src/App.tsx", "src/main.tsx", "src/types.ts", "src/components", "src/lib", "src/pages", "src/netlab", "src/virtlab", "src/lab"];

let out = "";
try {
  execFileSync("npx", ["tsc", "-p", ".", "--noUncheckedIndexedAccess"], { cwd: root, encoding: "utf8", stdio: ["ignore", "pipe", "pipe"] });
} catch (e) {
  out = String(e.stdout ?? "");
}
const errors = out.split("\n").filter((l) => /\): error TS/.test(l));
const bad = errors.filter((l) => COVERED.some((c) => l.startsWith(c)));
const rest = errors.length - bad.length;
if (bad.length) {
  console.error(bad.join("\n"));
  console.error(`index-check: ${bad.length} ошибок в уже дочищенных каталогах`);
  process.exit(1);
}
console.log(`index-check: дочищенные каталоги чисты; в остальных осталось ошибок: ${rest}`);
