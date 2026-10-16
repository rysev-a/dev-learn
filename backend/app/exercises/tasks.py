"""Упражнения с проверкой в Docker: доступ к определениям задач.

Задачи лежат в пакетах по книгам: py_tasks/ («Python как первый язык», book 13),
algo_tasks/ («Алгоритмы», book 7), arch_tasks/ («Архитектура компьютера»,
book 14), linux_tasks/ («Linux», book 8), db_tasks/ («Базы данных», book 9) и
rust_tasks/ («Изучаем Rust», book 10), c_tasks/ («От assembler к языку C», book 16) и
virt_tasks/ («Виртуализация», book 17); ключ — номер главы.
"""

from app.exercises import schema_view
from app.exercises.algo_tasks import ALGO_TASKS
from app.exercises.arch_tasks import ARCH_TASKS
from app.exercises.c_tasks import C_TASKS
from app.exercises.db_tasks import DB_TASKS
from app.exercises.js_tasks import JS_TASKS
from app.exercises.linux_tasks import LINUX_TASKS
from app.exercises.py_tasks import PY_TASKS
from app.exercises.rust_tasks import RUST_TASKS
from app.exercises.net_tasks import NET_TASKS
from app.exercises.virt_tasks import VIRT_TASKS

BOOK_TASKS: dict[int, dict[int, list[dict]]] = {
    13: PY_TASKS,
    7: ALGO_TASKS,
    8: LINUX_TASKS,
    9: DB_TASKS,
    10: RUST_TASKS,
    11: JS_TASKS,
    14: ARCH_TASKS,
    16: C_TASKS,
    15: NET_TASKS,
    17: VIRT_TASKS,
}


def chapter_tasks(book_id: int, chapter: int) -> list[dict] | None:
    """Публичные определения задач (без тестов) для клиента."""
    tasks = BOOK_TASKS.get(book_id, {}).get(chapter)
    if not tasks:
        return None
    out = []
    for t in tasks:
        item = {
            k: t.get(k, "")
            for k in ("id", "mode", "title", "statement", "starter", "hint")
        }
        if t.get("mode") == "sql" and t.get("setup"):
            item["dataset"] = schema_view.dataset_key(t["setup"])
        out.append(item)
    return out


def chapter_datasets(book_id: int, chapter: int) -> dict[str, dict]:
    """Схема и данные учебных баз SQL-задач главы: {ключ набора: описание}."""
    out: dict[str, dict] = {}
    for t in BOOK_TASKS.get(book_id, {}).get(chapter, []):
        if t.get("mode") == "sql" and t.get("setup"):
            key = schema_view.dataset_key(t["setup"])
            if key not in out:
                out[key] = schema_view.dataset(t["setup"])
    return out


def find_task(book_id: int, chapter: int, task_id: str) -> dict | None:
    for t in BOOK_TASKS.get(book_id, {}).get(chapter, []):
        if t["id"] == task_id:
            return t
    return None
