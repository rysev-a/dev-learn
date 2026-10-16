"""Выгрузка упражнений из Python-модулей в SQL-файлы для инициализации БД (app/data/sql/tasks).

uv run export_tasks.py          # переписать SQL-файлы
uv run export_tasks.py --check  # только проверить, что файлы не отстали от модулей (код возврата 1, если отстали)

Порядок работы с упражнениями: правим модули в app/exercises/*_tasks, запускаем этот скрипт, коммитим SQL вместе
с правкой; в БД задачи попадают при `uv run seed_textbook.py` или на первом запуске сервера (пустая таблица)."""

import sqlite3
import sys

from app import config
from app.books.meta import load_books
from app.exercises import sources, store

def book_names() -> dict[int, tuple[str, str]]:
    """{id книги: (короткое имя, название)} из app/data/sql/books.sql"""
    conn = sqlite3.connect(":memory:")
    load_books(conn)
    return {r[0]: (r[1], r[2]) for r in conn.execute("SELECT id, slug, title FROM books")}


def expected_files() -> dict[str, str]:
    """{имя файла: содержимое}"""
    files = {"00-schema.sql": store.SCHEMA_SQL}
    names = book_names()
    for book_id, chapters in sorted(sources.BOOK_TASKS.items()):
        if book_id not in names:
            raise SystemExit(f"книги {book_id} нет в app/data/sql/books.sql")
        slug, title = names[book_id]
        files[f"{book_id:02d}-{slug}.sql"] = store.book_sql(book_id, f"{slug} — {title}", chapters)
    return files


def main() -> int:
    files = expected_files()
    config.TASKS_SQL_DIR.mkdir(parents=True, exist_ok=True)
    stale = []
    for name, text in files.items():
        path = config.TASKS_SQL_DIR / name
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            stale.append(name)
            if "--check" not in sys.argv:
                path.write_text(text, encoding="utf-8")
    extra = [p.name for p in store.sql_files() if p.name not in files]
    if "--check" in sys.argv:
        for name in stale:
            print("отстал от модулей:", name)
        for name in extra:
            print("лишний файл:", name)
        return 1 if stale or extra else 0
    for name in extra:
        (config.TASKS_SQL_DIR / name).unlink()
    print(f"записано файлов: {len(stale)} из {len(files)}; удалено лишних: {len(extra)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
