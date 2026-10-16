"""Метаданные книг: порядок, имя, каталог слайдов, иконка, префикс id аудио — из app/data/sql/books.sql.

Файл применяется как есть (upsert по id), поэтому его можно выполнять сколько угодно раз, в том числе на
рабочей базе: книги, главы и прогресс пользователей не затрагиваются."""

import sqlite3

from app import config

BOOKS_SQL = config.DATA_DIR / "sql" / "books.sql"
COLUMNS = {"slug": "TEXT", "slides_dir": "TEXT", "icon": "TEXT", "audio_prefix": "TEXT"}


def migrate(conn: sqlite3.Connection) -> None:
    """Добавить столбцы метаданных в `books`, созданную прежней версией."""
    have = {r[1] for r in conn.execute("PRAGMA table_info(books)")}
    if not have:  # таблицы ещё нет — её создаст books.sql
        return
    for name, typ in COLUMNS.items():
        if name not in have:
            conn.execute(f"ALTER TABLE books ADD COLUMN {name} {typ}")


def load_books(conn: sqlite3.Connection) -> int:
    migrate(conn)
    conn.executescript(BOOKS_SQL.read_text(encoding="utf-8"))
    return conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]


def audio_prefix(conn: sqlite3.Connection, book_id: int) -> str:
    r = conn.execute("SELECT audio_prefix FROM books WHERE id = ?", (book_id,)).fetchone()
    return r[0] if r and r[0] else f"b{book_id}-ch"
