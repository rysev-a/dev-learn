"""API входа: регистрация, вход, выход, текущий пользователь."""

from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from pydantic import BaseModel, StringConstraints

from app import config
from app.accounts import service
from app.accounts.deps import COOKIE, current_user
from app.books.service import db

router = APIRouter(prefix="/api/auth", tags=["auth"])

Email = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        max_length=254,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    ),
]
Login = Annotated[
    str, StringConstraints(strip_whitespace=True, pattern=r"^[A-Za-z0-9_.-]{3,32}$")
]
Password = Annotated[str, StringConstraints(min_length=6, max_length=128)]


class RegisterIn(BaseModel):
    email: Email
    login: Login
    password: Password


class LoginIn(BaseModel):
    # логин или email
    login: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=254)]
    password: Annotated[str, StringConstraints(min_length=1, max_length=128)]


def _set_session(response: Response, token: str) -> None:
    response.set_cookie(
        COOKIE,
        token,
        max_age=service.SESSION_DAYS * 86400,
        httponly=True,
        samesite="lax",
        secure=config.SECURE_COOKIE,
        path="/",
    )


@router.post("/register", status_code=201)
def register(body: RegisterIn, response: Response):
    with db() as conn:
        try:
            user = service.create_user(conn, body.email, body.login, body.password)
        except ValueError as e:
            raise HTTPException(409, str(e)) from None
        _set_session(response, service.start_session(conn, user["id"]))
    return user


@router.post("/login")
def login(body: LoginIn, response: Response):
    with db() as conn:
        user = service.authenticate(conn, body.login, body.password)
        if user is None:
            raise HTTPException(401, "Неверный логин или пароль")
        _set_session(response, service.start_session(conn, user["id"]))
    return user


@router.post("/logout", status_code=204)
def logout(response: Response, say_session: str | None = Cookie(default=None)):
    if say_session:
        with db() as conn:
            service.end_session(conn, say_session)
    response.delete_cookie(COOKIE, path="/")


@router.get("/me")
def me(user: Annotated[dict, Depends(current_user)]):
    return user
