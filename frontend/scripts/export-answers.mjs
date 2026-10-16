// Выгрузка задач с вводом ответа (content/exercises) в SQL-файлы для инициализации БД (backend/app/data/sql/answers).
//   npm run answers:export   — переписать файлы
//   npm run answers:check    — проверить, что файлы не отстали от исходников (код возврата 1, если отстали)
// В приложение исходники не попадают: сервер отдаёт условия и подсказки без ответов и сам проверяет введённое.
import path from "path";
import { EXERCISES } from "../content/exercises/index.ts";
import { backend, books, byBook, lit, sync } from "./lib/sqlexport.mjs";

const SCHEMA = `-- Задачи с вводом ответа (дискретная математика). Выполнение этого файла очищает таблицы: дальше идут файлы книг.
-- Полная инициализация: sqlite3 say.db < app/data/sql/answers/*.sql (файлы выполняются по порядку имён).
CREATE TABLE IF NOT EXISTS answer_sets (
    book_id INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    title   TEXT    NOT NULL,
    PRIMARY KEY (book_id, chapter)
);
CREATE TABLE IF NOT EXISTS answer_tasks (
    book_id INTEGER NOT NULL,
    chapter INTEGER NOT NULL,
    ord     INTEGER NOT NULL,
    q       TEXT    NOT NULL,
    answers TEXT    NOT NULL,
    hint    TEXT,
    PRIMARY KEY (book_id, chapter, ord)
);
DELETE FROM answer_tasks;
DELETE FROM answer_sets;
`;

function files() {
  const names = books();
  const out = { "00-schema.sql": SCHEMA };
  for (const [book, chapters] of Object.entries(byBook(EXERCISES))) {
    const info = names[book];
    if (!info) throw new Error(`нет книги ${book}: добавьте её в backend/app/data/sql/books.sql`);
    const lines = [`-- Задачи с вводом ответа, книга ${book} «${info[1]}». Файл строит scripts/export-answers.mjs — руками не правьте.`, ""];
    for (const [chapter, set] of chapters) {
      lines.push(`INSERT INTO answer_sets (book_id, chapter, title) VALUES (${book}, ${chapter}, ${lit(set.title)});`);
      set.tasks.forEach((t, i) => {
        if (!t.answers.length) throw new Error(`${book}:${chapter} задача ${i + 1}: нет ответов`);
        lines.push(
          `INSERT INTO answer_tasks (book_id, chapter, ord, q, answers, hint) VALUES (${book}, ${chapter}, ${i}, ${lit(t.q)}, ${lit(JSON.stringify(t.answers))}, ${lit(t.hint ?? "")});`,
        );
      });
    }
    out[`${String(book).padStart(2, "0")}-${info[0]}.sql`] = lines.join("\n") + "\n";
  }
  return out;
}

sync(path.join(backend, "app/data/sql/answers"), files(), process.argv.includes("--check"));
