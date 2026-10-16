"""API задач с вводом ответа: условия и подсказки без ответов; ответ проверяет сервер."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from app.accounts.deps import current_user
from app.answers import store
from app.books.service import db

router = APIRouter(prefix="/api/answers", tags=["answers"])

User = Annotated[dict, Depends(current_user)]


@router.get("")
def summary():
    """Сколько задач с вводом ответа в каждой главе: {книга: {глава: число}}."""
    with db() as conn:
        return {str(b): {str(c): n for c, n in chs.items()} for b, chs in store.counts(conn).items()}


def _solved(conn, uid: int, book_id: int, chapter: int) -> dict[str, str]:
    return {
        str(r["task_idx"]): r["answer"]
        for r in conn.execute(
            "SELECT task_idx, answer FROM answer_solved WHERE user_id = ? AND book_id = ? AND chapter = ?",
            (uid, book_id, chapter),
        )
    }


@router.get("/{book_id}/{chapter}")
def get_set(book_id: int, chapter: int, user: User):
    """Условия и подсказки; `solved` — решённые пользователем задачи с принятым ответом."""
    with db() as conn:
        aset = store.get_set(conn, book_id, chapter)
        if aset is None:
            raise HTTPException(404, "У этой главы нет упражнений с вводом ответа")
        solved = _solved(conn, user["id"], book_id, chapter)
    return {
        "kind": "practice",
        "title": aset["title"],
        "tasks": [{"q": t["q"], "hint": t["hint"]} for t in aset["tasks"]],
        "solved": solved,
    }


class CheckIn(BaseModel):
    task: int = Field(ge=0, le=500)
    value: str = Field(max_length=200)


@router.post("/{book_id}/{chapter}/check")
def check(book_id: int, chapter: int, body: CheckIn, user: User):
    """Проверить ответ. Верный записывается как решённый (решённое остаётся решённым); неверный ничего не меняет и
    верного ответа не раскрывает."""
    with db() as conn:
        aset = store.get_set(conn, book_id, chapter)
        if aset is None or body.task >= len(aset["tasks"]):
            raise HTTPException(404, "Задача не найдена")
        ok = store.is_correct(body.value, aset["tasks"][body.task]["answers"])
        if ok:
            conn.execute(
                "INSERT OR REPLACE INTO answer_solved (user_id, book_id, chapter, task_idx, answer) VALUES (?, ?, ?, ?, ?)",
                (user["id"], book_id, chapter, body.task, body.value.strip()),
            )
        return {"ok": ok}


@router.delete("", status_code=204)
def reset(book: Annotated[int, Query(ge=1, le=1000)], chapter: Annotated[int, Query(ge=1, le=1000)], user: User):
    """Начать упражнения главы заново."""
    with db() as conn:
        conn.execute(
            "DELETE FROM answer_solved WHERE user_id = ? AND book_id = ? AND chapter = ?",
            (user["id"], book, chapter),
        )
