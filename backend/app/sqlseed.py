"""Начальное заполнение БД из SQL-файлов каталога: упражнения, квизы, задачи с вводом ответа.

Каждый каталог — это `00-schema.sql` (создаёт таблицы и очищает их) и файлы с INSERT; их можно выполнить и обычным
`sqlite3 say.db < каталог/*.sql`. Здесь — то же из приложения: перезагрузка одной транзакцией и «заполнить, если пусто»."""

import sqlite3
from pathlib import Path


def sql_files(directory: Path) -> list[Path]:
    return sorted(directory.glob("*.sql"))


def reload(conn: sqlite3.Connection, directory: Path, count_table: str) -> int:
    """Пересоздать таблицы из SQL-файлов каталога (одной транзакцией); вернуть число строк в count_table."""
    files = sql_files(directory)
    if not files:
        raise FileNotFoundError(f"нет SQL-файлов в {directory}")
    script = "BEGIN;\n" + "\n".join(f.read_text(encoding="utf-8") for f in files) + "\nCOMMIT;\n"
    try:
        conn.executescript(script)
    except Exception:
        conn.rollback()
        raise
    return conn.execute(f"SELECT COUNT(*) FROM {count_table}").fetchone()[0]  # noqa: S608


def ensure(conn: sqlite3.Connection, directory: Path, count_table: str) -> None:
    """Первый запуск или потерянная база: таблицы нет или она пуста — загрузить из SQL-файлов."""
    exists = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (count_table,)).fetchone()
    if not exists or conn.execute(f"SELECT COUNT(*) FROM {count_table}").fetchone()[0] == 0:  # noqa: S608
        reload(conn, directory, count_table)
