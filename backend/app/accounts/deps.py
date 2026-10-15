"""Зависимость FastAPI: текущий пользователь по cookie сессии."""

from fastapi import Cookie, HTTPException

from app.accounts import service
from app.books.service import db

COOKIE = "say_session"


def current_user(say_session: str | None = Cookie(default=None)) -> dict:
    if not say_session:
        raise HTTPException(401, "Нужно войти")
    with db() as conn:
        user = service.user_by_token(conn, say_session)
    if user is None:
        raise HTTPException(401, "Сессия истекла — войдите снова")
    return user
