"""Упражнения с проверкой в Docker: доступ к определениям задач.

Задачи лежат в пакетах по книгам: py_tasks/ («Изучаем Python», book 13),
algo_tasks/ («Алгоритмы», book 7), arch_tasks/ («Архитектура компьютера»,
book 14) и linux_tasks/ («Linux», book 8); ключ — номер главы.
"""

from app.exercises.algo_tasks import ALGO_TASKS
from app.exercises.arch_tasks import ARCH_TASKS
from app.exercises.linux_tasks import LINUX_TASKS
from app.exercises.py_tasks import PY_TASKS

BOOK_TASKS: dict[int, dict[int, list[dict]]] = {
    13: PY_TASKS,
    7: ALGO_TASKS,
    8: LINUX_TASKS,
    14: ARCH_TASKS,
}


def chapter_tasks(book_id: int, chapter: int) -> list[dict] | None:
    """Публичные определения задач (без тестов) для клиента."""
    tasks = BOOK_TASKS.get(book_id, {}).get(chapter)
    if not tasks:
        return None
    return [
        {k: t[k] for k in ("id", "mode", "title", "statement", "starter", "hint")}
        for t in tasks
    ]


def find_task(book_id: int, chapter: int, task_id: str) -> dict | None:
    for t in BOOK_TASKS.get(book_id, {}).get(chapter, []):
        if t["id"] == task_id:
            return t
    return None
