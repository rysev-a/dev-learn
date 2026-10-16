-- Квизы на теорию. Выполнение этого файла очищает таблицы: дальше идут файлы книг с INSERT.
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
