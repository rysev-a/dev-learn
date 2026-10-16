// Общее для скриптов выгрузки содержимого (квизы, задачи с вводом ответа) в SQL-файлы для инициализации БД.
import fs from "fs";
import { DatabaseSync } from "node:sqlite";
import path from "path";
import { fileURLToPath } from "url";

export const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
export const backend = path.resolve(root, "../backend");

/** SQL-литерал: число или строка в одинарных кавычках */
export const lit = (v) => {
  if (typeof v === "number") return String(v);
  if (v.includes("\0")) throw new Error("NUL в тексте");
  return `'${v.replaceAll("'", "''")}'`;
};

/** {id книги: [slug, название]} из backend/app/data/sql/books.sql — единственного места, где они заданы */
export function books() {
  const db = new DatabaseSync(":memory:");
  db.exec(fs.readFileSync(path.join(backend, "app/data/sql/books.sql"), "utf8"));
  return Object.fromEntries(db.prepare("SELECT id, slug, title FROM books").all().map((r) => [r.id, [r.slug, r.title]]));
}

/** Записать (или проверить с --check) набор файлов {имя: текст} в каталог; лишние .sql удаляются */
export function sync(outDir, files, check) {
  fs.mkdirSync(outDir, { recursive: true });
  const existing = fs.readdirSync(outDir).filter((f) => f.endsWith(".sql"));
  const stale = Object.keys(files).filter((f) => !fs.existsSync(path.join(outDir, f)) || fs.readFileSync(path.join(outDir, f), "utf8") !== files[f]);
  const extra = existing.filter((f) => !(f in files));
  if (check) {
    stale.forEach((f) => console.log("отстал от исходников:", f));
    extra.forEach((f) => console.log("лишний файл:", f));
    process.exit(stale.length || extra.length ? 1 : 0);
  }
  for (const f of stale) fs.writeFileSync(path.join(outDir, f), files[f]);
  for (const f of extra) fs.unlinkSync(path.join(outDir, f));
  console.log(`записано файлов: ${stale.length} из ${Object.keys(files).length}; удалено лишних: ${extra.length}`);
}

/** Разложить {«книга:глава»: значение} по книгам: {книга: [[глава, значение], …]}, главы по возрастанию */
export function byBook(table) {
  const out = {};
  for (const [key, value] of Object.entries(table)) {
    const [book, chapter] = key.split(":").map(Number);
    (out[book] ??= []).push([chapter, value]);
  }
  for (const list of Object.values(out)) list.sort((a, b) => a[0] - b[0]);
  return out;
}
