"""Определения код-задач книги «Python как первый язык» (book 13) по разделам.

Ключ — номер главы. Режимы проверки:
- stdout: программа запускается, сравнивается построчный вывод;
- func: из решения вызывается функция с аргументами тестов и
  сравнивается возвращённое значение (кортежи — настоящими кортежами).

Клиенту отдаются только statement/starter/hint — тесты остаются на бэкенде.
"""

from app.exercises.py_tasks import asyncs, asyncs2, basics, data, datamodel, design, files, functional, generators2, internals, intro, iterators, metaprog, oop, projects, stdlib

PY_TASKS: dict[int, list[dict]] = {
    **intro.TASKS,
    **basics.TASKS,
    **data.TASKS,
    **oop.TASKS,
    **files.TASKS,
    **iterators.TASKS,
    **datamodel.TASKS,
    **generators2.TASKS,
    **functional.TASKS,
    **metaprog.TASKS,
    **design.TASKS,
    **internals.TASKS,
    **projects.TASKS,
    **stdlib.TASKS,
    **asyncs.TASKS,
    **asyncs2.TASKS,
}
