"""API упражнений: список задач главы, запуск кода в песочнице, история попыток."""

import threading
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.accounts import practice
from app.accounts.deps import current_user
from app.books.service import db
from app.exercises import runner, tasks

router = APIRouter(prefix="/api/exercises", tags=["exercises"])

User = Annotated[dict, Depends(current_user)]
MAX_CODE = 20_000  # символов в одном решении
MAX_DRAFT = 200_000  # черновик: у схем из вентилей решение — JSON и бывает крупным


@router.get("")
def summary():
    """Сколько код-упражнений в каждой главе: {книга: {глава: число}} — для дашборда."""
    return {
        str(book): {str(ch): n for ch, n in chapters.items()}
        for book, chapters in tasks.summary().items()
    }


@router.get("/{book_id}/{chapter}")
def list_tasks(book_id: int, chapter: int):
    items = tasks.chapter_tasks(book_id, chapter)
    if items is None:
        raise HTTPException(404, "У этой главы нет код-упражнений")
    return {"tasks": items, "datasets": tasks.chapter_datasets(book_id, chapter)}


@router.get("/{book_id}/{chapter}/state")
def chapter_state(book_id: int, chapter: int, user: User):
    """Статусы и черновики пользователя по задачам главы."""
    with db() as conn:
        return practice.chapter_state(conn, user["id"], book_id, chapter)


class DraftIn(BaseModel):
    code: str = Field(max_length=MAX_DRAFT)


@router.put("/{book_id}/{chapter}/{task_id}/draft", status_code=204)
def save_draft(book_id: int, chapter: int, task_id: str, body: DraftIn, user: User):
    if tasks.find_task(book_id, chapter, task_id) is None:
        raise HTTPException(404, "Задача не найдена")
    with db() as conn:
        practice.save_draft(conn, user["id"], book_id, chapter, task_id, body.code)


@router.get("/{book_id}/{chapter}/{task_id}/attempts")
def task_attempts(book_id: int, chapter: int, task_id: str, user: User):
    """История попыток пользователя по задаче: от новых к старым, с кодом."""
    if tasks.find_task(book_id, chapter, task_id) is None:
        raise HTTPException(404, "Задача не найдена")
    with db() as conn:
        return {"attempts": practice.attempts(conn, user["id"], book_id, chapter, task_id)}


class SolvedIn(BaseModel):
    solution: str = Field(default="", max_length=MAX_DRAFT)


@router.put("/{book_id}/{chapter}/{task_id}/solved", status_code=204)
def mark_lab_solved(book_id: int, chapter: int, task_id: str, body: SolvedIn, user: User):
    """Интерактивное упражнение (схема, ассемблер) решено — проверка прошла в браузере.
    Принимается только для задач режима lab; решение записывается как попытка."""
    task = tasks.find_task(book_id, chapter, task_id)
    if task is None or task.get("mode") != "lab":
        raise HTTPException(404, "Задача не найдена")
    with db() as conn:
        practice.record_attempt(
            conn, user["id"], book_id, chapter, task_id, body.solution, 1, 1, True
        )
        if body.solution:  # решение же и есть «черновик»: оно вернётся на доску при входе
            practice.save_draft(conn, user["id"], book_id, chapter, task_id, body.solution)


class RunIn(BaseModel):
    book: int
    chapter: int
    task: str
    code: str = Field(max_length=MAX_CODE)


# У каждого пользователя одновременно идёт не больше одной проверки: каждая — это
# контейнер Docker, и очередь из них легко положит машину.
_running: set[int] = set()
_running_lock = threading.Lock()


@router.post("/run")
def run_code(body: RunIn, user: User):
    task = tasks.find_task(body.book, body.chapter, body.task)
    if task is None:
        raise HTTPException(404, "Задача не найдена")
    if task.get("mode") == "lab":
        raise HTTPException(422, "Это упражнение проверяется в браузере, а не в песочнице")
    if not body.code.strip():
        raise HTTPException(422, "Пустой код — нечего проверять")

    uid = user["id"]
    with _running_lock:
        if uid in _running:
            raise HTTPException(429, "Предыдущая проверка ещё идёт")
        _running.add(uid)
    try:
        result = runner.run_task(task, body.code)
    finally:
        with _running_lock:
            _running.discard(uid)

    total = len(result["results"])
    passed = sum(1 for r in result["results"] if r.get("ok"))
    solved = result["status"] == "ok" and total > 0 and passed == total
    with db() as conn:
        attempt = practice.record_attempt(
            conn, uid, body.book, body.chapter, body.task, body.code, passed, total, solved
        )
    return {**result, "passed": passed, "total": total, "solved": solved, "attempt": attempt}
