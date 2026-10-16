"""Исходные определения упражнений (Python-модули по книгам).

Задачи лежат в пакетах по книгам (ключ — номер главы): algo_tasks (7, «Алгоритмы»),
linux_tasks (8, «Погружаемся в Unix»), db_tasks (9, «Базы данных»), rust_tasks (10),
js_tasks (11, «Современный Frontend»), py_tasks (13, «Python как первый язык»),
arch_tasks (14, лаборатория в браузере), net_tasks (15, «Компьютерные сети»),
c_tasks (16, «От assembler к языку C»), virt_tasks (17, «Виртуализация»).
"""

from app.exercises.algo_tasks import ALGO_TASKS
from app.exercises.arch_tasks import ARCH_TASKS
from app.exercises.c_tasks import C_TASKS
from app.exercises.db_tasks import DB_TASKS
from app.exercises.js_tasks import JS_TASKS
from app.exercises.linux_tasks import LINUX_TASKS
from app.exercises.py_tasks import PY_TASKS
from app.exercises.net_tasks import NET_TASKS
from app.exercises.rust_tasks import RUST_TASKS
from app.exercises.virt_tasks import VIRT_TASKS

BOOK_TASKS: dict[int, dict[int, list[dict]]] = {
    7: ALGO_TASKS,
    8: LINUX_TASKS,
    9: DB_TASKS,
    10: RUST_TASKS,
    11: JS_TASKS,
    13: PY_TASKS,
    14: ARCH_TASKS,
    15: NET_TASKS,
    16: C_TASKS,
    17: VIRT_TASKS,
}

# Во время работы приложение эти модули не читает: задачи лежат в БД (app/exercises/store.py),
# а в БД они попадают из SQL-файлов в app/data/sql/tasks. Сами SQL-файлы строит из BOOK_TASKS
# скрипт export_tasks.py; тест tests/test_tasks.py следит, чтобы файлы не отставали от модулей.
