-- Задачи с вводом ответа (дискретная математика). Выполнение этого файла очищает таблицы: дальше идут файлы книг.
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
