"""Упражнения в БД: таблица `tasks`, кодек определений и загрузка из SQL-файлов.

Источник правды для работающего приложения — таблица `tasks`. Если база потеряна, её заполняют заново
SQL-файлы из `app/data/sql/tasks` (`00-schema.sql` создаёт таблицу и очищает её, `NN-<книга>.sql` добавляют
задачи): `sqlite3 say.db < app/data/sql/tasks/*.sql` или `uv run seed_textbook.py` / первый запуск сервера.
Сами файлы строит `export_tasks.py` из Python-модулей (`app.exercises.sources`).

Определение задачи — словарь: поля, которые видит клиент (id, mode, title, statement, starter, hint), лежат
отдельными столбцами, всё остальное (тесты, эталонный вывод, драйвер, setup, flags…) — в `spec` как JSON.
Кортежи Python в JSON не различаются со списками, а для задач режима func это важно, поэтому они хранятся
как {"__tuple__": [...]} и возвращаются кортежами."""

import json
import sqlite3
from pathlib import Path

from app import config, sqlseed

PUBLIC_FIELDS = ("mode", "title", "statement", "starter", "hint")
COLUMNS = ("book_id", "chapter", "id", "ord", *PUBLIC_FIELDS, "spec")


# --- кодек --------------------------------------------------------------------------------

def _enc(o):
    if isinstance(o, tuple):
        return {"__tuple__": [_enc(x) for x in o]}
    if isinstance(o, list):
        return [_enc(x) for x in o]
    if isinstance(o, dict):
        for k in o:
            if not isinstance(k, str):
                raise TypeError(f"ключ словаря в определении задачи должен быть строкой: {k!r}")
        return {k: _enc(v) for k, v in o.items()}
    return o


def _dec(o):
    if isinstance(o, dict):
        if set(o) == {"__tuple__"}:
            return tuple(_dec(x) for x in o["__tuple__"])
        return {k: _dec(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_dec(x) for x in o]
    return o


def split_task(task: dict) -> tuple[dict, str]:
    """Определение → (публичные поля, spec JSON): чтобы строка таблицы описывала задачу без потерь."""
    public = {k: task[k] for k in ("id", *PUBLIC_FIELDS) if k in task}
    spec = {k: v for k, v in task.items() if k not in public}
    return public, json.dumps(_enc(spec), ensure_ascii=False, allow_nan=False, sort_keys=True)


def join_task(row: sqlite3.Row) -> dict:
    """Строка таблицы → определение задачи, как в исходных модулях."""
    task: dict = {"id": row["id"]}
    for k in PUBLIC_FIELDS:
        if row[k] is not None:
            task[k] = row[k]
    task.update(_dec(json.loads(row["spec"])))
    return task


# --- SQL-файлы ----------------------------------------------------------------------------

def sql_files() -> list[Path]:
    return sqlseed.sql_files(config.TASKS_SQL_DIR)


def reload_tasks(conn: sqlite3.Connection) -> int:
    """Пересоздать таблицу задач из SQL-файлов (одной транзакцией); вернуть число задач."""
    return sqlseed.reload(conn, config.TASKS_SQL_DIR, "tasks")


def ensure_tasks(conn: sqlite3.Connection) -> None:
    """Первый запуск или потерянная база: если задач в БД нет, загрузить их из SQL-файлов."""
    sqlseed.ensure(conn, config.TASKS_SQL_DIR, "tasks")


# --- запросы ------------------------------------------------------------------------------

def counts(conn: sqlite3.Connection) -> dict[int, dict[int, int]]:
    out: dict[int, dict[int, int]] = {}
    for r in conn.execute("SELECT book_id, chapter, COUNT(*) n FROM tasks GROUP BY book_id, chapter"):
        out.setdefault(r["book_id"], {})[r["chapter"]] = r["n"]
    return out


def chapter_rows(conn: sqlite3.Connection, book_id: int, chapter: int) -> list[dict]:
    rows = conn.execute(
        "SELECT * FROM tasks WHERE book_id = ? AND chapter = ? ORDER BY ord", (book_id, chapter)
    ).fetchall()
    return [join_task(r) for r in rows]


def find(conn: sqlite3.Connection, book_id: int, chapter: int, task_id: str) -> dict | None:
    r = conn.execute(
        "SELECT * FROM tasks WHERE book_id = ? AND chapter = ? AND id = ?", (book_id, chapter, task_id)
    ).fetchone()
    return join_task(r) if r else None


# --- выгрузка в SQL (для export_tasks.py) -------------------------------------------------

def _lit(v) -> str:
    if v is None:
        return "NULL"
    if isinstance(v, int):
        return str(v)
    if "\x00" in v:
        raise ValueError("NUL в тексте задачи")
    return "'" + v.replace("'", "''") + "'"


def insert_sql(book_id: int, chapter: int, ord_: int, task: dict) -> str:
    public, spec = split_task(task)
    values = [book_id, chapter, public["id"], ord_, *(public.get(k) for k in PUBLIC_FIELDS), spec]
    return f"({', '.join(_lit(v) for v in values)})"


def book_sql(book_id: int, title: str, chapters: dict[int, list[dict]]) -> str:
    """По одному INSERT на задачу: обычный sqlite3 и любые лимиты длины запроса переживают такой файл."""
    head = f"INSERT INTO tasks ({', '.join(COLUMNS)}) VALUES "
    lines = [f"-- Упражнения книги {book_id} «{title}». Файл строит export_tasks.py — руками не правьте.", ""]
    for ch in sorted(chapters):
        for i, t in enumerate(chapters[ch]):
            lines.append(f"{head}{insert_sql(book_id, ch, i, t)};")
    return "\n".join(lines) + "\n"


SCHEMA_SQL = """-- Таблица упражнений. Выполнение этого файла очищает её: дальше идут файлы книг с INSERT.
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
"""
