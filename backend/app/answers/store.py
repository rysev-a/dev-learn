"""Задачи с вводом ответа (дискретная математика) в БД: таблицы `answer_sets` и `answer_tasks`.

Верные ответы лежат только на сервере: клиент получает условие и подсказку, а ответ проверяет сервер
(app/answers/router.py), показать ответ нельзя — так задумано курсом. Если база потеряна, задачи возвращают
SQL-файлы `app/data/sql/answers` (см. app/sqlseed.py); файлы строит из исходников `frontend/content/exercises`
скрипт `frontend/scripts/export-answers.mjs` (`npm run answers:export`)."""

import json
import re
import sqlite3
from pathlib import Path

from app import config, sqlseed


def sql_files() -> list[Path]:
    return sqlseed.sql_files(config.ANSWERS_SQL_DIR)


def reload_answers(conn: sqlite3.Connection) -> int:
    return sqlseed.reload(conn, config.ANSWERS_SQL_DIR, "answer_tasks")


def ensure_answers(conn: sqlite3.Connection) -> None:
    sqlseed.ensure(conn, config.ANSWERS_SQL_DIR, "answer_tasks")


# --- проверка ответа ----------------------------------------------------------------------

def normalize(value: object) -> str:
    """Пробелы, регистр, запятая как десятичный разделитель (первая запятая перед цифрой)."""
    s = re.sub(r"\s+", " ", str(value).strip().lower())
    return re.sub(r",(\d)", r".\1", s, count=1)


_NUM = re.compile(r"^-?\d+(\.\d+)?$")


def is_correct(given: str, answers: list[str]) -> bool:
    a = normalize(given)
    if not a:
        return False
    for ans in answers:
        b = normalize(ans)
        if _NUM.match(a) and _NUM.match(b):
            if abs(float(a) - float(b)) < 1e-9:
                return True
        elif a == b:
            return True
    return False


# --- запросы ------------------------------------------------------------------------------

def counts(conn: sqlite3.Connection) -> dict[int, dict[int, int]]:
    out: dict[int, dict[int, int]] = {}
    for r in conn.execute("SELECT book_id, chapter, COUNT(*) n FROM answer_tasks GROUP BY book_id, chapter"):
        out.setdefault(r["book_id"], {})[r["chapter"]] = r["n"]
    return out


def get_set(conn: sqlite3.Connection, book_id: int, chapter: int) -> dict | None:
    """{title, tasks: [{q, answers, hint}]} — вместе с ответами (наружу их не отдаёт никто, кроме проверки)."""
    head = conn.execute(
        "SELECT title FROM answer_sets WHERE book_id = ? AND chapter = ?", (book_id, chapter)
    ).fetchone()
    if head is None:
        return None
    rows = conn.execute(
        "SELECT q, answers, hint FROM answer_tasks WHERE book_id = ? AND chapter = ? ORDER BY ord",
        (book_id, chapter),
    ).fetchall()
    return {
        "title": head["title"],
        "tasks": [{"q": r["q"], "answers": json.loads(r["answers"]), "hint": r["hint"] or ""} for r in rows],
    }
