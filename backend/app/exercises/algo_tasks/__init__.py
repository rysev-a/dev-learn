"""Код-задачи книги «Алгоритмы и структуры данных» (book 7), ключ — номер главы.

Решения пишутся на Python. Эффективность проверяется не «на глаз»: скрытый
драйвер считает обращения к данным или подаёт такие большие входы, что
квадратичное решение не укладывается в лимит песочницы. Каждая глава —
модуль chNN.py с таблицей TASKS; _kept.py хранит задачи, переехавшие из
старых глав.
"""

import importlib
import pkgutil

ALGO_TASKS: dict[int, list[dict]] = {}
for _m in sorted(m.name for m in pkgutil.iter_modules(__path__) if m.name.startswith("ch")):
    ALGO_TASKS.update(importlib.import_module(f"{__name__}.{_m}").TASKS)
