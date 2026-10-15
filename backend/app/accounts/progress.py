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

router = APIRouter(prefix="/api/progress", tags=["progress"])

User = Annotated[dict, Depends(current_user)]
Book = Annotated[int, Field(ge=1, le=1000)]
Chapter = Annotated[int, Field(ge=1, le=1000)]


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
    return {"slides": slides, "quiz": quiz, "answers": answers, "code": code}


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


class QuizIn(BaseModel):
    book: Book
    chapter: Chapter
    # выбранные варианты по порядку вопросов; null — без ответа
    picks: list[int | None] = Field(max_length=100)


@router.put("/quiz", status_code=204)
def save_quiz(body: QuizIn, user: User):
    with db() as conn:
        if all(p is None for p in body.picks):
            conn.execute(
                "DELETE FROM quiz_picks WHERE user_id = ? AND book_id = ? AND chapter = ?",
                (user["id"], body.book, body.chapter),
            )
            return
        conn.execute(
            """
            INSERT INTO quiz_picks (user_id, book_id, chapter, picks, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (user_id, book_id, chapter)
            DO UPDATE SET picks = excluded.picks, updated_at = excluded.updated_at
            """,
            (user["id"], body.book, body.chapter, json.dumps(body.picks), iso(now())),
        )


class AnswersIn(BaseModel):
    book: Book
    chapter: Chapter
    # номер задачи → принятый ответ (только решённые)
    solved: dict[int, Annotated[str, Field(max_length=200)]] = Field(max_length=200)


@router.put("/answers", status_code=204)
def save_answers(body: AnswersIn, user: User):
    with db() as conn:
        conn.execute(
            "DELETE FROM answer_solved WHERE user_id = ? AND book_id = ? AND chapter = ?",
            (user["id"], body.book, body.chapter),
        )
        conn.executemany(
            "INSERT INTO answer_solved (user_id, book_id, chapter, task_idx, answer) VALUES (?, ?, ?, ?, ?)",
            [(user["id"], body.book, body.chapter, i, a) for i, a in body.solved.items()],
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
