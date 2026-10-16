"""API квизов: вопросы без ответов; ответ и пояснение выдаются после выбора варианта."""

import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.accounts.deps import current_user
from app.accounts.service import iso, now
from app.books.service import db
from app.quizzes import store

router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])

User = Annotated[dict, Depends(current_user)]


@router.get("")
def summary():
    """Сколько вопросов в квизе каждой главы: {книга: {глава: число}}."""
    with db() as conn:
        return {str(b): {str(c): n for c, n in chs.items()} for b, chs in store.counts(conn).items()}


def _picks(conn, uid: int, book_id: int, chapter: int) -> list[int | None]:
    r = conn.execute(
        "SELECT picks FROM quiz_picks WHERE user_id = ? AND book_id = ? AND chapter = ?",
        (uid, book_id, chapter),
    ).fetchone()
    return json.loads(r["picks"]) if r else []


@router.get("/{book_id}/{chapter}")
def get_quiz(book_id: int, chapter: int, user: User):
    """Вопросы с вариантами. `reveal[i]` — ответ и пояснение для вопросов, на которые пользователь уже ответил."""
    with db() as conn:
        quiz = store.get_quiz(conn, book_id, chapter)
        if quiz is None:
            raise HTTPException(404, "У этой главы нет вопросов")
        picks = _picks(conn, user["id"], book_id, chapter)
    reveal = [
        {"answer": q["answer"], "expl": q["expl"]} if i < len(picks) and picks[i] is not None else None
        for i, q in enumerate(quiz["questions"])
    ]
    return {
        "kind": quiz["kind"],
        "title": quiz["title"],
        "questions": [{"q": q["q"], "options": q["options"]} for q in quiz["questions"]],
        "reveal": reveal,
    }


class AnswerIn(BaseModel):
    question: int = Field(ge=0, le=500)
    pick: int = Field(ge=0, le=50)


@router.post("/{book_id}/{chapter}/answer")
def answer(book_id: int, chapter: int, body: AnswerIn, user: User):
    """Записать выбор и вернуть верный ответ. На вопрос отвечают один раз: повторный запрос
    ничего не меняет и возвращает то же самое."""
    with db() as conn:
        quiz = store.get_quiz(conn, book_id, chapter)
        if quiz is None or body.question >= len(quiz["questions"]):
            raise HTTPException(404, "Вопрос не найден")
        q = quiz["questions"][body.question]
        if body.pick >= len(q["options"]):
            raise HTTPException(422, "Нет такого варианта")
        total = len(quiz["questions"])
        picks = (_picks(conn, user["id"], book_id, chapter) + [None] * total)[:total]
        if picks[body.question] is None:
            picks[body.question] = body.pick
            conn.execute(
                """
                INSERT INTO quiz_picks (user_id, book_id, chapter, picks, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT (user_id, book_id, chapter)
                DO UPDATE SET picks = excluded.picks, updated_at = excluded.updated_at
                """,
                (user["id"], book_id, chapter, json.dumps(picks), iso(now())),
            )
        return {
            "pick": picks[body.question],
            "answer": q["answer"],
            "expl": q["expl"],
            "right": store.right_count(quiz, picks),
        }
