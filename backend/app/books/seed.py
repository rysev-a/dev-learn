"""Сид курса: парсинг учебников, запись в БД, генерация аудио.

Учебники лежат в app/data/textbook/*.md. Формат файла:

    #BOOK <id>            (опционально; по умолчанию 1)
    #SECTION <название>
    #CHAPTER <номер> | <название>
    <текст урока одной строкой, абзацы — литеральными \n\n>

Каждый абзац урока — отдельная часть (слайд + свой wav). Аудио: id частей
выводятся через uuid5 из номера главы и индекса части, поэтому повторный сид
не перегенерирует уже синтезированные wav-файлы.

CLI (из каталога backend/):

    uv run seed_textbook.py                # БД + недостающее аудио
    uv run seed_textbook.py --no-audio     # только перестроить БД
    uv run seed_textbook.py --audio-only   # только догенерировать аудио
"""

import argparse
import re
import sqlite3
import uuid

from app import config
from app.books.service import db, init_db

BOOK_RE = re.compile(r"^#BOOK\s+(\d+)$")
CHAPTER_RE = re.compile(r"^#CHAPTER\s+(\d+)\s*\|\s*(.+)$")

# фиксированное пространство имён для стабильных id уроков
NS = uuid.UUID("d3a7c0de-0000-4000-8000-4b6f6b6f726f")

# Порядок книг в левом меню — по плану курса (course.MD): дискретная математика,
# Python, алгоритмы, операционные системы, базы данных, Rust, JavaScript.
# Книги «Архитектура компьютера» и «Системный дизайн» из плана ещё не написаны.
BOOKS = [
    (12, "Дискретная математика", 0),
    (13, "Изучаем Python", 1),
    (7, "Алгоритмы: продвинутый уровень", 2),
    (8, "Linux: от шелла до ядра", 3),
    (9, "Базы данных: под капотом", 4),
    (10, "Изучаем Rust", 5),
    (11, "Изучаем JavaScript", 6),
]
# uuid5 source prefix per book
AUDIO_PREFIX = {
    7: "algx-ch",
    8: "lin-ch",
    9: "dbx-ch",
    10: "rust-ch",
    11: "js-ch",
    12: "dm-ch",
    13: "learn-py-ch",
}


def split_paragraph_parts(books: list[dict]) -> None:
    """Каждый абзац урока — отдельная часть: свой слайд и свой wav-файл.

    Так слайд начинает играть с чистого листа, а не с хвоста предыдущей
    фразы. Разбиваются все главы всех книг, исключений нет."""
    for book in books:
        for sec in book["sections"]:
            for ch in sec["chapters"]:
                if len(ch["lessons"]) == 1:
                    ch["lessons"] = [
                        p.strip() for p in ch["lessons"][0].split("\n\n") if p.strip()
                    ]


def parse() -> list[dict]:
    """Return [{book_id, sections: [{title, chapters: [{num, title, lessons}]}]}]."""
    books: dict[int, dict] = {}
    book = section = chapter = None
    for path in sorted(config.TEXTBOOK_DIR.rglob("*.md")):
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("#BOOK "):
                m = BOOK_RE.match(line)
                if not m:
                    raise ValueError(f"bad book line in {path}: {line}")
                bid = int(m.group(1))
                book = books.setdefault(bid, {"book_id": bid, "sections": []})
                section = chapter = None
            elif line.startswith("#SECTION "):
                if book is None:
                    book = books.setdefault(1, {"book_id": 1, "sections": []})
                section = {
                    "title": line.removeprefix("#SECTION ").strip(),
                    "chapters": [],
                }
                book["sections"].append(section)
                chapter = None
            elif line.startswith("#CHAPTER "):
                m = CHAPTER_RE.match(line)
                if not m or section is None:
                    raise ValueError(f"bad chapter line in {path}: {line}")
                num, title = int(m.group(1)), m.group(2).strip()
                chapter = {"num": num, "title": title, "lessons": []}
                section["chapters"].append(chapter)
            else:
                if chapter is None:
                    raise ValueError(f"lesson outside chapter in {path}: {line[:60]}")
                # literal \n in the source line marks paragraph breaks for TTS/UI
                chapter["lessons"].append(line.replace("\\n", "\n"))
    # chapter files are self-contained and repeat #SECTION; merge consecutive ones
    for book in books.values():
        merged = []
        for sec in book["sections"]:
            if merged and merged[-1]["title"] == sec["title"]:
                merged[-1]["chapters"].extend(sec["chapters"])
            else:
                merged.append(sec)
        book["sections"] = merged
    return [books[k] for k in sorted(books)]


def seed_db(books: list[dict]) -> list[dict]:
    """Rebuild course tables. Returns flat [{id, text, book}] list for audio gen."""
    lessons = []
    with sqlite3.connect(config.DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        init_db(conn)
        for bid, title, ord_ in BOOKS:
            conn.execute(
                "INSERT INTO books (id, title, ord) VALUES (?, ?, ?) "
                "ON CONFLICT(id) DO UPDATE SET title = excluded.title, ord = excluded.ord",
                (bid, title, ord_),
            )
        conn.execute("DELETE FROM lessons")
        conn.execute("DELETE FROM chapters")
        conn.execute("DELETE FROM sections")
        for book in books:
            bid = book["book_id"]
            prefix = AUDIO_PREFIX.get(bid, f"b{bid}-ch")
            for s_ord, section in enumerate(book["sections"]):
                cur = conn.execute(
                    "INSERT INTO sections (book_id, title, ord) VALUES (?, ?, ?)",
                    (bid, section["title"], s_ord),
                )
                section_id = cur.lastrowid
                for ch in section["chapters"]:
                    cur = conn.execute(
                        "INSERT INTO chapters (section_id, num, title) VALUES (?, ?, ?)",
                        (section_id, ch["num"], ch["title"]),
                    )
                    chapter_id = cur.lastrowid
                    for l_ord, text in enumerate(ch["lessons"]):
                        lesson_id = uuid.uuid5(NS, f"{prefix}{ch['num']}-l{l_ord}").hex
                        conn.execute(
                            "INSERT INTO lessons (id, chapter_id, ord, text) VALUES (?, ?, ?, ?)",
                            (lesson_id, chapter_id, l_ord, text),
                        )
                        lessons.append({"id": lesson_id, "text": text, "book": bid})
        conn.commit()
    return lessons


def lessons_from_db() -> list[dict]:
    """Все части курса из БД — для режима --audio-only."""
    with db() as conn:
        rows = conn.execute(
            """
            SELECT l.id, l.text, s.book_id AS book FROM lessons l
            JOIN chapters c ON c.id = l.chapter_id
            JOIN sections s ON s.id = c.section_id
            ORDER BY s.book_id, s.ord, c.id, l.ord
            """
        ).fetchall()
    return [dict(r) for r in rows]


def generate_audio(lessons: list[dict]):
    # Импорт внутри функции: torch тяжёлый, в режиме --no-audio он не нужен
    from app.voice import engine

    done = 0
    skipped = 0
    total = len(lessons)
    for i, l in enumerate(lessons, 1):
        out = config.AUDIO_DIR / f"{l['id']}.wav"
        if out.exists():
            skipped += 1
            continue
        dur = engine.synthesize_to_wav(l["text"], "sveta", out)
        done += 1
        print(f"[{i}/{total}] book {l['book']} {dur:.1f}s -> {out.name}", flush=True)
    print(f"generated {done}, skipped {skipped}")


def main() -> None:
    ap = argparse.ArgumentParser(
        prog="seed_textbook",
        description="Сид книг из учебников в SQLite и генерация аудио (kokoro-ru).",
    )
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument(
        "--no-audio", action="store_true", help="только перестроить БД, без синтеза"
    )
    mode.add_argument(
        "--audio-only",
        action="store_true",
        help="только догенерировать аудио из текущей БД, без пересидa",
    )
    args = ap.parse_args()

    if args.audio_only:
        ls = lessons_from_db()
        print(f"lessons in db: {len(ls)}")
        generate_audio(ls)
        print("done")
        return

    all_books = parse()
    split_paragraph_parts(all_books)
    n_sec = sum(len(b["sections"]) for b in all_books)
    n_ch = sum(len(s["chapters"]) for b in all_books for s in b["sections"])
    n_l = sum(
        len(c["lessons"])
        for b in all_books
        for s in b["sections"]
        for c in s["chapters"]
    )
    print(
        f"parsed {len(all_books)} books, {n_sec} sections, {n_ch} chapters, {n_l} lessons"
    )
    ls = seed_db(all_books)
    if not args.no_audio:
        generate_audio(ls)
    print("done")


if __name__ == "__main__":
    main()
