"""Код-задачи книги «Изучаем Rust» (book 10), ключ — номер главы; по файлу на главу (chNN.py).

Режим rust: код ученика и скрытый драйвер (функция main) собираются в один
файл и компилируются rustc в песочнице без сети (образ rust:1.97-slim);
сравнивается построчный вывод программы. Сеть возможна лишь через loopback.
Задачи с полем `crates` (асинхронность, чат на axum) идут в образ say-rust-crates:1
с заранее собранными tokio, axum, sqlx (PostgreSQL), serde, tower, tungstenite и др.;
задачи с полем `postgres` получают ещё и запущенный PostgreSQL (база chat, пользователь postgres).
"""

import importlib
import pkgutil

RUST_TASKS: dict[int, list[dict]] = {}
for _m in sorted(pkgutil.iter_modules(__path__), key=lambda m: m.name):
    if _m.name.startswith("ch"):
        RUST_TASKS.update(importlib.import_module(f"{__name__}.{_m.name}").TASKS)
