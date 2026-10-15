"""Упражнения с кодом в кабинете: статусы, черновики и история попыток."""

import sqlite3

from app.accounts.service import iso, now

HISTORY_LIMIT = 50


def record_attempt(
    conn: sqlite3.Connection,
    user_id: int,
    book: int,
    chapter: int,
    task: str,
    code: str,
    passed: int,
    total: int,
    solved: bool,
) -> dict:
    """Записывает попытку и обновляет статус. Решённое остаётся решённым навсегда:
    неудачная попытка статус «ok» не снимает."""
    status = "ok" if solved else "bad"
    created = iso(now())
    cur = conn.execute(
        """
        INSERT INTO code_attempts
          (user_id, book_id, chapter, task_id, code, status, passed, total, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, book, chapter, task, code, status, passed, total, created),
    )
    conn.execute(
        """
        INSERT INTO code_status (user_id, book_id, chapter, task_id, status, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT (user_id, book_id, chapter, task_id) DO UPDATE SET
          status = CASE WHEN code_status.status = 'ok' THEN 'ok' ELSE excluded.status END,
          updated_at = excluded.updated_at
        """,
        (user_id, book, chapter, task, status, created),
    )
    # хранится не больше HISTORY_LIMIT последних попыток по задаче
    conn.execute(
        """
        DELETE FROM code_attempts WHERE user_id = ? AND book_id = ? AND chapter = ?
          AND task_id = ? AND id NOT IN (
            SELECT id FROM code_attempts WHERE user_id = ? AND book_id = ? AND chapter = ?
              AND task_id = ? ORDER BY id DESC LIMIT ?
          )
        """,
        (user_id, book, chapter, task, user_id, book, chapter, task, HISTORY_LIMIT),
    )
    return {"id": cur.lastrowid, "status": status, "created_at": created}


def save_draft(
    conn: sqlite3.Connection, user_id: int, book: int, chapter: int, task: str, code: str
) -> None:
    conn.execute(
        """
        INSERT INTO code_drafts (user_id, book_id, chapter, task_id, code, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT (user_id, book_id, chapter, task_id)
        DO UPDATE SET code = excluded.code, updated_at = excluded.updated_at
        """,
        (user_id, book, chapter, task, code, iso(now())),
    )


def chapter_state(conn: sqlite3.Connection, user_id: int, book: int, chapter: int) -> dict:
    status = {
        r["task_id"]: r["status"]
        for r in conn.execute(
            "SELECT task_id, status FROM code_status WHERE user_id = ? AND book_id = ? AND chapter = ?",
            (user_id, book, chapter),
        )
    }
    drafts = {
        r["task_id"]: r["code"]
        for r in conn.execute(
            "SELECT task_id, code FROM code_drafts WHERE user_id = ? AND book_id = ? AND chapter = ?",
            (user_id, book, chapter),
        )
    }
    return {"status": status, "drafts": drafts}


def attempts(
    conn: sqlite3.Connection, user_id: int, book: int, chapter: int, task: str
) -> list[dict]:
    rows = conn.execute(
        """
        SELECT id, code, status, passed, total, created_at FROM code_attempts
        WHERE user_id = ? AND book_id = ? AND chapter = ? AND task_id = ?
        ORDER BY id DESC LIMIT ?
        """,
        (user_id, book, chapter, task, HISTORY_LIMIT),
    ).fetchall()
    return [dict(r) for r in rows]
