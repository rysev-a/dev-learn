"""Работа с пользователями и сессиями в БД."""

import sqlite3
from datetime import datetime, timedelta, timezone

from app.accounts.security import (
    hash_password,
    new_session_token,
    token_hash,
    verify_password,
)

SESSION_DAYS = 30

# Временные учётные записи для разработки; пароли совпадают с логинами.
DEFAULT_USERS = [
    ("student@mail.com", "student", "student"),
    ("programmer@mail.com", "programmer", "programmer"),
]


def now() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def public_user(row: sqlite3.Row) -> dict:
    return {"id": row["id"], "email": row["email"], "login": row["login"]}


def create_user(conn: sqlite3.Connection, email: str, login: str, password: str) -> dict:
    """Создаёт пользователя; ValueError — если email или логин заняты."""
    taken = conn.execute(
        "SELECT email, login FROM users WHERE email = ? OR login = ?", (email, login)
    ).fetchone()
    if taken is not None:
        if taken["email"].lower() == email.lower():
            raise ValueError("Этот email уже зарегистрирован")
        raise ValueError("Этот логин уже занят")
    cur = conn.execute(
        "INSERT INTO users (email, login, password_hash, created_at) VALUES (?, ?, ?, ?)",
        (email, login, hash_password(password), iso(now())),
    )
    row = conn.execute("SELECT * FROM users WHERE id = ?", (cur.lastrowid,)).fetchone()
    return public_user(row)


def ensure_default_users(conn: sqlite3.Connection) -> None:
    for email, login, password in DEFAULT_USERS:
        exists = conn.execute(
            "SELECT 1 FROM users WHERE login = ? OR email = ?", (login, email)
        ).fetchone()
        if exists is None:
            create_user(conn, email, login, password)


def authenticate(conn: sqlite3.Connection, ident: str, password: str) -> dict | None:
    """Пользователь по логину или email и паролю; None — если не подошло."""
    row = conn.execute(
        "SELECT * FROM users WHERE login = ? OR email = ?", (ident, ident)
    ).fetchone()
    if row is None:
        # одинаковое время ответа для существующего и несуществующего логина
        verify_password(password, hash_password("x"))
        return None
    return public_user(row) if verify_password(password, row["password_hash"]) else None


def start_session(conn: sqlite3.Connection, user_id: int) -> str:
    conn.execute("DELETE FROM sessions WHERE expires_at < ?", (iso(now()),))
    token = new_session_token()
    conn.execute(
        "INSERT INTO sessions (token_hash, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
        (
            token_hash(token),
            user_id,
            iso(now()),
            iso(now() + timedelta(days=SESSION_DAYS)),
        ),
    )
    return token


def user_by_token(conn: sqlite3.Connection, token: str) -> dict | None:
    row = conn.execute(
        """
        SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id
        WHERE s.token_hash = ? AND s.expires_at > ?
        """,
        (token_hash(token), iso(now())),
    ).fetchone()
    return public_user(row) if row else None


def end_session(conn: sqlite3.Connection, token: str) -> None:
    conn.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash(token),))
