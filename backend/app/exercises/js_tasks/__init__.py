"""Код-задачи книги «Современный Frontend» (book 11), ключ — номер главы.

Режим js: код ученика и скрытый драйвер собираются в один ES-модуль (main.mjs) и
выполняются Node 22 (образ node:22-alpine) в песочнице без сети; сравнивается
построчный вывод console.log. Тестов DOM нет: браузерные API проверяются на
собственных мини-моделях (дерево узлов, шина событий) и на чистых функциях.
Задачи лежат по файлу на главу (`chNN.py`, словарь `TASKS = {N: [...]}`); пакет подхватывает их сам.
"""

import importlib
import pkgutil

JS_TASKS: dict[int, list[dict]] = {}
for _m in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
    if _m.name.startswith("ch"):
        JS_TASKS.update(importlib.import_module(f"{__name__}.{_m.name}").TASKS)
