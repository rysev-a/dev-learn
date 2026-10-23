"""Прогресс обучения пользователя: слайды, вопросы, упражнения.

Всё привязано к (книга, номер главы). Клиент одним запросом забирает весь прогресс
(`GET /api/progress`) для дашборда и вкладок, а дальше пишет точечные изменения."""

import json
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from app.accounts.deps import current_user
from app.accounts.service import iso, now
from app.books.service import db
from app.quizzes import store

router = APIRouter(prefix="/api/progress", tags=["progress"])

User = Annotated[dict, Depends(current_user)]
Book = Annotated[int, Field(ge=1, le=1000)]
Chapter = Annotated[int, Field(ge=0, le=1000)]


@router.get("")
def get_progress(user: User):
    uid = user["id"]
    with db() as conn:
        slides: dict[str, list[int]] = {}
        for r in conn.execute(
            "SELECT book_id, chapter, slide FROM slide_views WHERE user_id = ? ORDER BY slide",
            (uid,),
        ):
            slides.setdefault(f"{r['book_id']}:{r['chapter']}", []).append(r["slide"])

        quiz = {
            f"{r['book_id']}:{r['chapter']}": json.loads(r["picks"])
            for r in conn.execute(
                "SELECT book_id, chapter, picks FROM quiz_picks WHERE user_id = ?", (uid,)
            )
        }

        correct = store.answers_map(conn)
        quiz_right = {
            key: sum(1 for p, a in zip(picks, correct.get(tuple(map(int, key.split(":"))), [])) if p == a)
            for key, picks in quiz.items()
        }

        answers: dict[str, dict[str, str]] = {}
        for r in conn.execute(
            "SELECT book_id, chapter, task_idx, answer FROM answer_solved WHERE user_id = ?",
            (uid,),
        ):
            answers.setdefault(f"{r['book_id']}:{r['chapter']}", {})[str(r["task_idx"])] = r[
                "answer"
            ]

        code: dict[str, dict[str, str]] = {}
        for r in conn.execute(
            "SELECT book_id, chapter, task_id, status FROM code_status WHERE user_id = ?",
            (uid,),
        ):
            code.setdefault(f"{r['book_id']}:{r['chapter']}", {})[r["task_id"]] = r["status"]
    return {"slides": slides, "quiz": quiz, "quizRight": quiz_right, "answers": answers, "code": code}


class SlideIn(BaseModel):
    book: Book
    chapter: Chapter
    slide: int = Field(ge=0, le=500)


@router.post("/slides", status_code=204)
def mark_slide(body: SlideIn, user: User):
    with db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO slide_views (user_id, book_id, chapter, slide) VALUES (?, ?, ?, ?)",
            (user["id"], body.book, body.chapter, body.slide),
        )


@router.delete("/quiz", status_code=204)
def reset_quiz(book: Annotated[int, Query(ge=1, le=1000)], chapter: Annotated[int, Query(ge=0, le=1000)], user: User):
    """Пройти квиз заново. Выбранные варианты записывает только POST /api/quizzes/…/answer (иначе ответы
    можно было бы «выбрать» для всех вопросов и тут же получить верные), здесь их можно лишь стереть."""
    with db() as conn:
        conn.execute(
            "DELETE FROM quiz_picks WHERE user_id = ? AND book_id = ? AND chapter = ?",
            (user["id"], book, chapter),
        )


@router.delete("", status_code=204)
def reset_progress(user: User, scope: Annotated[str, Query(pattern="^(practice|all)$")]):
    """Сбросить упражнения (статусы, черновики, история) или весь прогресс."""
    tables = ["code_status", "code_drafts", "code_attempts", "answer_solved"]
    if scope == "all":
        tables += ["slide_views", "quiz_picks"]
    with db() as conn:
        for t in tables:
            conn.execute(f"DELETE FROM {t} WHERE user_id = ?", (user["id"],))  # noqa: S608
