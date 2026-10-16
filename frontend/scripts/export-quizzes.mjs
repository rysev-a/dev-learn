// Выгрузка квизов из исходников (content/quizzes) в SQL-файлы для инициализации БД (backend/app/data/sql/quizzes).
//   npm run quizzes:export   — переписать файлы
//   npm run quizzes:check    — проверить, что файлы не отстали от исходников (код возврата 1, если отстали)
// В приложение исходники не попадают: сервер отдаёт вопросы без ответов, а ответ — после выбора варианта.
import path from "path";
import { QUIZZES } from "../content/quizzes/index.ts";
import { backend, books, byBook, lit, sync } from "./lib/sqlexport.mjs";

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


function files() {
  const names = books();
  const out = { "00-schema.sql": SCHEMA };
  for (const [book, chapters] of Object.entries(byBook(QUIZZES))) {
    const info = names[book];
    if (!info) throw new Error(`нет книги ${book}: добавьте её в backend/app/data/sql/books.sql`);
    const lines = [`-- Квизы книги ${book} «${info[1]}». Файл строит scripts/export-quizzes.mjs — руками не правьте.`, ""];
    for (const [chapter, quiz] of chapters) {
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

sync(path.join(backend, "app/data/sql/quizzes"), files(), process.argv.includes("--check"));
