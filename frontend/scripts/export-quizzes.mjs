// Выгрузка квизов из исходников (content/quizzes) в SQL-файлы для инициализации БД (backend/app/data/sql/quizzes).
//   npm run quizzes:export   — переписать файлы
//   npm run quizzes:check    — проверить, что файлы не отстали от исходников (код возврата 1, если отстали)
// В приложение исходники не попадают: сервер отдаёт вопросы без ответов, а ответ — после выбора варианта.
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { QUIZZES } from "../content/quizzes/index.ts";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outDir = path.resolve(root, "../backend/app/data/sql/quizzes");
const BOOKS = {
  7: ["algo", "Алгоритмы и структуры данных"],
  8: ["linux", "Погружаемся в Unix"],
  9: ["db", "Базы данных"],
  10: ["rust", "Изучаем Rust"],
  11: ["js", "Современный Frontend"],
  12: ["dm", "Дискретная математика"],
  13: ["py", "Python как первый язык"],
  14: ["arch", "Архитектура компьютера"],
  15: ["net", "Компьютерные сети"],
  16: ["c", "От assembler к языку C"],
  17: ["virt", "Виртуализация"],
};

const SCHEMA = `-- Квизы на теорию. Выполнение этого файла очищает таблицы: дальше идут файлы книг с INSERT.
-- Полная инициализация: sqlite3 say.db < app/data/sql/quizzes/*.sql (файлы выполняются по порядку имён).
CREATE TABLE IF NOT EXISTS quizzes (
    book_id INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    kind    TEXT    NOT NULL DEFAULT 'theory',
    title   TEXT    NOT NULL,
    PRIMARY KEY (book_id, chapter)
);
CREATE TABLE IF NOT EXISTS quiz_questions (
    book_id INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    ord     INTEGER NOT NULL,
    q       TEXT    NOT NULL,
    options TEXT    NOT NULL,
    answer  INTEGER NOT NULL,
    expl    TEXT,
    PRIMARY KEY (book_id, chapter, ord)
);
DELETE FROM quiz_questions;
DELETE FROM quizzes;
`;

const lit = (v) => {
  if (typeof v === "number") return String(v);
  if (v.includes("\0")) throw new Error("NUL в тексте квиза");
  return `'${v.replaceAll("'", "''")}'`;
};

function files() {
  const out = { "00-schema.sql": SCHEMA };
  const byBook = {};
  for (const [key, quiz] of Object.entries(QUIZZES)) {
    const [book, chapter] = key.split(":").map(Number);
    (byBook[book] ??= []).push([chapter, quiz]);
  }
  for (const book of Object.keys(byBook).map(Number).sort((a, b) => a - b)) {
    const info = BOOKS[book];
    if (!info) throw new Error(`нет имени для книги ${book}: добавьте в BOOKS (scripts/export-quizzes.mjs)`);
    const lines = [`-- Квизы книги ${book} «${info[1]}». Файл строит scripts/export-quizzes.mjs — руками не правьте.`, ""];
    for (const [chapter, quiz] of byBook[book].sort((a, b) => a[0] - b[0])) {
      lines.push(`INSERT INTO quizzes (book_id, chapter, kind, title) VALUES (${book}, ${chapter}, ${lit(quiz.kind)}, ${lit(quiz.title)});`);
      quiz.questions.forEach((q, i) => {
        if (!(q.answer >= 0 && q.answer < q.options.length)) throw new Error(`${book}:${chapter} вопрос ${i + 1}: answer вне вариантов`);
        lines.push(
          `INSERT INTO quiz_questions (book_id, chapter, ord, q, options, answer, expl) VALUES (${book}, ${chapter}, ${i}, ${lit(q.q)}, ${lit(JSON.stringify(q.options))}, ${q.answer}, ${lit(q.expl ?? "")});`,
        );
      });
    }
    out[`${String(book).padStart(2, "0")}-${info[0]}.sql`] = lines.join("\n") + "\n";
  }
  return out;
}

const check = process.argv.includes("--check");
const want = files();
fs.mkdirSync(outDir, { recursive: true });
const existing = fs.readdirSync(outDir).filter((f) => f.endsWith(".sql"));
const stale = Object.keys(want).filter((f) => !fs.existsSync(path.join(outDir, f)) || fs.readFileSync(path.join(outDir, f), "utf8") !== want[f]);
const extra = existing.filter((f) => !(f in want));
if (check) {
  stale.forEach((f) => console.log("отстал от исходников:", f));
  extra.forEach((f) => console.log("лишний файл:", f));
  process.exit(stale.length || extra.length ? 1 : 0);
}
for (const f of stale) fs.writeFileSync(path.join(outDir, f), want[f]);
for (const f of extra) fs.unlinkSync(path.join(outDir, f));
console.log(`записано файлов: ${stale.length} из ${Object.keys(want).length}; удалено лишних: ${extra.length}`);
