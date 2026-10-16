"""Код-задачи книги «Изучаем Rust» (book 10), ключ — номер главы; по файлу на главу (chNN.py).

Режим rust: код ученика и скрытый драйвер (функция main) собираются в один
файл и компилируются rustc в песочнице без сети (образ rust:1.97-slim);
сравнивается построчный вывод программы. Внешние крейты недоступны —
только стандартная библиотека; сеть возможна лишь через loopback.
Задачи с полем `crates` (главы про асинхронность) идут в образ say-rust-tokio:1
с заранее собранными tokio, futures, tokio-stream, tokio-util и bytes.
"""

import importlib
import pkgutil

RUST_TASKS: dict[int, list[dict]] = {}
for _m in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
    if _m.name.startswith("ch"):
        RUST_TASKS.update(importlib.import_module(f"{__name__}.{_m.name}").TASKS)
