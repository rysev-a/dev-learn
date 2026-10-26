-- Таблица упражнений. Выполнение этого файла очищает её: дальше идут файлы книг с INSERT.
-- Полная инициализация: sqlite3 say.db < app/data/sql/tasks/*.sql (файлы выполняются по порядку имён).
CREATE TABLE IF NOT EXISTS tasks (
    book_id   INTEGER NOT NULL,
    chapter   INTEGER NOT NULL,
    id        TEXT    NOT NULL,
    ord       INTEGER NOT NULL,
    mode      TEXT,
    title     TEXT,
    statement TEXT,
    starter   TEXT,
    hint      TEXT,
    spec      TEXT    NOT NULL DEFAULT '{}',
    PRIMARY KEY (book_id, chapter, id)
);
CREATE INDEX IF NOT EXISTS tasks_by_chapter ON tasks (book_id, chapter, ord);
DELETE FROM tasks;
