"""Упражнения с проверкой в Docker: доступ к определениям задач.

Сами задачи лежат в app/exercises/py_tasks/ (по разделам курса).
"""

from app.exercises.py_tasks import PY_TASKS


def chapter_tasks(book_id: int, chapter: int) -> list[dict] | None:
    """Публичные определения задач (без тестов) для клиента."""
    if book_id != 13:
        return None
    tasks = PY_TASKS.get(chapter)
    if not tasks:
        return None
    return [
        {k: t[k] for k in ("id", "mode", "title", "statement", "starter", "hint")}
        for t in tasks
    ]


def find_task(book_id: int, chapter: int, task_id: str) -> dict | None:
    if book_id != 13:
        return None
    for t in PY_TASKS.get(chapter, []):
        if t["id"] == task_id:
            return t
    return None
