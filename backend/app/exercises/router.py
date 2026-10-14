"""API упражнений: список задач главы и запуск кода в песочнице."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.exercises import runner, tasks

router = APIRouter(prefix="/api/exercises", tags=["exercises"])


@router.get("/{book_id}/{chapter}")
def list_tasks(book_id: int, chapter: int):
    items = tasks.chapter_tasks(book_id, chapter)
    if items is None:
        raise HTTPException(404, "У этой главы нет код-упражнений")
    return {"tasks": items}


class RunIn(BaseModel):
    book: int
    chapter: int
    task: str
    code: str


@router.post("/run")
def run_code(body: RunIn):
    task = tasks.find_task(body.book, body.chapter, body.task)
    if task is None:
        raise HTTPException(404, "Задача не найдена")
    if not body.code.strip():
        raise HTTPException(422, "Пустой код — нечего проверять")
    return runner.run_task(task, body.code)
