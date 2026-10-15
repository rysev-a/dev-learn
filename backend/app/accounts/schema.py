"""Схема таблиц пользователей. Курс (книги, главы) пересоздаётся сидом, а эти таблицы —
данные пользователей, их сид не трогает. Прогресс привязан к паре (книга, номер главы),
а не к id главы: id меняются при пересиде."""

import sqlite3

SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT NOT NULL UNIQUE COLLATE NOCASE,
        login TEXT NOT NULL UNIQUE COLLATE NOCASE,
        password_hash TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS sessions (
        token_hash TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        created_at TEXT NOT NULL,
        expires_at TEXT NOT NULL
    )
    """,
    # просмотренные слайды
    """
    CREATE TABLE IF NOT EXISTS slide_views (
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        book_id INTEGER NOT NULL,
        chapter INTEGER NOT NULL,
        slide INTEGER NOT NULL,
        PRIMARY KEY (user_id, book_id, chapter, slide)
    )
    """,
    # ответы на вопросы: JSON-список выбранных вариантов (null — без ответа)
    """
    CREATE TABLE IF NOT EXISTS quiz_picks (
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        book_id INTEGER NOT NULL,
        chapter INTEGER NOT NULL,
        picks TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        PRIMARY KEY (user_id, book_id, chapter)
    )
    """,
    # решённые упражнения с вводом ответа (дискретная математика)
    """
    CREATE TABLE IF NOT EXISTS answer_solved (
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        book_id INTEGER NOT NULL,
        chapter INTEGER NOT NULL,
        task_idx INTEGER NOT NULL,
        answer TEXT NOT NULL,
        PRIMARY KEY (user_id, book_id, chapter, task_idx)
    )
    """,
    # упражнения с кодом: статус, черновик, история попыток
    """
    CREATE TABLE IF NOT EXISTS code_status (
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        book_id INTEGER NOT NULL,
        chapter INTEGER NOT NULL,
        task_id TEXT NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('ok', 'bad')),
        updated_at TEXT NOT NULL,
        PRIMARY KEY (user_id, book_id, chapter, task_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS code_drafts (
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        book_id INTEGER NOT NULL,
        chapter INTEGER NOT NULL,
        task_id TEXT NOT NULL,
        code TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        PRIMARY KEY (user_id, book_id, chapter, task_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS code_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        book_id INTEGER NOT NULL,
        chapter INTEGER NOT NULL,
        task_id TEXT NOT NULL,
        code TEXT NOT NULL,
        status TEXT NOT NULL,
        passed INTEGER NOT NULL,
        total INTEGER NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS code_attempts_task
    ON code_attempts (user_id, book_id, chapter, task_id, id)
    """,
]


def init_accounts(conn: sqlite3.Connection) -> None:
    for stmt in SCHEMA:
        conn.execute(stmt)
