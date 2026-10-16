"""Упражнения с проверкой в Docker: доступ к определениям задач.

Задачи лежат в таблице `tasks` БД (app/exercises/store.py); в БД они попадают из SQL-файлов
app/data/sql/tasks, а те строит из Python-модулей по книгам export_tasks.py. Здесь — только чтение."""

from functools import lru_cache

from app.books.service import db
from app.exercises import schema_view, store


def summary() -> dict[int, dict[int, int]]:
    """Сколько код-упражнений в каждой главе: {книга: {глава: число}}."""
    with db() as conn:
        return store.counts(conn)


def chapter_tasks(book_id: int, chapter: int) -> list[dict] | None:
    """Публичные определения задач (без тестов) для клиента."""
    with db() as conn:
        tasks = store.chapter_rows(conn, book_id, chapter)
    if not tasks:
        return None
    out = []
    for t in tasks:
        item = {k: t.get(k, "") for k in ("id", "mode", "title", "statement", "starter", "hint")}
        if t.get("mode") == "sql" and t.get("setup"):
            item["dataset"] = schema_view.dataset_key(t["setup"])
        out.append(item)
    return out


@lru_cache(maxsize=256)
def _dataset(setup: str) -> dict:
    return schema_view.dataset(setup)


def chapter_datasets(book_id: int, chapter: int) -> dict[str, dict]:
    """Схема и данные учебных баз SQL-задач главы: {ключ набора: описание}."""
    with db() as conn:
        tasks = store.chapter_rows(conn, book_id, chapter)
    out: dict[str, dict] = {}
    for t in tasks:
        if t.get("mode") == "sql" and t.get("setup"):
            key = schema_view.dataset_key(t["setup"])
            if key not in out:
                out[key] = _dataset(t["setup"])
    return out


def find_task(book_id: int, chapter: int, task_id: str) -> dict | None:
    with db() as conn:
        return store.find(conn, book_id, chapter, task_id)
