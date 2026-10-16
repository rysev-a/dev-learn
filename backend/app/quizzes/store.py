"""Квизы на теорию в БД: таблицы `quizzes` и `quiz_questions`, загрузка из SQL-файлов, запросы.

Правильные ответы лежат только на сервере: клиент получает вопросы и варианты, а ответ и пояснение — после того,
как пользователь выбрал вариант (app/quizzes/router.py). Если база потеряна, квизы возвращают SQL-файлы
`app/data/sql/quizzes` (`00-schema.sql` создаёт таблицы и очищает их, `NN-<книга>.sql` — вставки):
сервер заполняет пустые таблицы сам, `uv run seed_textbook.py --no-audio` перезагружает их, а вручную —
`sqlite3 say.db < app/data/sql/quizzes/*.sql`. Файлы строит из исходников `frontend/content/quizzes`
скрипт `frontend/scripts/export-quizzes.mjs` (`npm run quizzes:export`)."""

import json
import sqlite3
from pathlib import Path

from app import config


def sql_files() -> list[Path]:
    return sorted(config.QUIZZES_SQL_DIR.glob("*.sql"))


def reload_quizzes(conn: sqlite3.Connection) -> int:
    """Пересоздать квизы из SQL-файлов одной транзакцией; вернуть число вопросов."""
    files = sql_files()
    if not files:
        raise FileNotFoundError(f"нет SQL-файлов квизов в {config.QUIZZES_SQL_DIR}")
    script = "BEGIN;\n" + "\n".join(f.read_text(encoding="utf-8") for f in files) + "\nCOMMIT;\n"
    try:
        conn.executescript(script)
    except Exception:
        conn.rollback()
        raise
    return conn.execute("SELECT COUNT(*) FROM quiz_questions").fetchone()[0]


def ensure_quizzes(conn: sqlite3.Connection) -> None:
    """Первый запуск или потерянная база: нет квизов — загрузить из SQL-файлов."""
    exists = conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='quiz_questions'").fetchone()
    if not exists or conn.execute("SELECT COUNT(*) FROM quiz_questions").fetchone()[0] == 0:
        reload_quizzes(conn)


def counts(conn: sqlite3.Connection) -> dict[int, dict[int, int]]:
    out: dict[int, dict[int, int]] = {}
    for r in conn.execute("SELECT book_id, chapter, COUNT(*) n FROM quiz_questions GROUP BY book_id, chapter"):
        out.setdefault(r["book_id"], {})[r["chapter"]] = r["n"]
    return out


def get_quiz(conn: sqlite3.Connection, book_id: int, chapter: int) -> dict | None:
    """{title, kind, questions: [{q, options, answer, expl}]} — вместе с ответами (наружу их отдаёт только роутер)."""
    head = conn.execute(
        "SELECT title, kind FROM quizzes WHERE book_id = ? AND chapter = ?", (book_id, chapter)
    ).fetchone()
    if head is None:
        return None
    rows = conn.execute(
        "SELECT q, options, answer, expl FROM quiz_questions WHERE book_id = ? AND chapter = ? ORDER BY ord",
        (book_id, chapter),
    ).fetchall()
    return {
        "title": head["title"],
        "kind": head["kind"],
        "questions": [
            {"q": r["q"], "options": json.loads(r["options"]), "answer": r["answer"], "expl": r["expl"] or ""}
            for r in rows
        ],
    }


def answers_map(conn: sqlite3.Connection) -> dict[tuple[int, int], list[int]]:
    """Верные ответы всех квизов: {(книга, глава): [ответ по порядку вопросов]} — для подсчёта прогресса."""
    out: dict[tuple[int, int], list[int]] = {}
    for r in conn.execute("SELECT book_id, chapter, answer FROM quiz_questions ORDER BY book_id, chapter, ord"):
        out.setdefault((r["book_id"], r["chapter"]), []).append(r["answer"])
    return out


def right_count(quiz: dict, picks: list[int | None]) -> int:
    return sum(1 for p, q in zip(picks, quiz["questions"]) if p is not None and p == q["answer"])
