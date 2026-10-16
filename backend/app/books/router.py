"""Роутер курса: книги, разделы, главы и аудио уроков."""

import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from app import config
from app.books.service import (
    audio_duration,
    audio_file_path,
    concat_wavs,
    db,
    safe_filename,
    table_exists,
)

router = APIRouter(prefix="/api")


@router.get("/books")
def books():
    with db() as conn:
        if not table_exists(conn, "books"):
            return []
        rows = conn.execute(
            """
            SELECT b.id, b.title, b.slug, b.slides_dir, b.icon,
              (SELECT COUNT(*) FROM sections s WHERE s.book_id = b.id) AS sections_count,
              (SELECT COUNT(*) FROM chapters c JOIN sections s ON s.id = c.section_id
               WHERE s.book_id = b.id) AS lessons_count,
              (SELECT COUNT(*) FROM lessons l
               JOIN chapters c ON c.id = l.chapter_id
               JOIN sections s ON s.id = c.section_id
               WHERE s.book_id = b.id) AS parts_count
            FROM books b ORDER BY b.ord
            """
        ).fetchall()
    return [dict(r) for r in rows]


@router.get("/books/{book_id}/course")
def book_course(book_id: int):
    with db() as conn:
        if not table_exists(conn, "sections"):
            return []
        sections = conn.execute(
            "SELECT * FROM sections WHERE book_id = ? ORDER BY ord", (book_id,)
        ).fetchall()
        chapters = conn.execute(
            """
            SELECT c.*,
              (SELECT COUNT(*) FROM lessons l WHERE l.chapter_id = c.id) AS parts_count
            FROM chapters c JOIN sections s ON s.id = c.section_id
            WHERE s.book_id = ? ORDER BY c.id
            """,
            (book_id,),
        ).fetchall()
    by_section = {}
    for ch in chapters:
        by_section.setdefault(ch["section_id"], []).append(
            {
                "id": ch["id"],
                "num": ch["num"],
                "title": ch["title"],
                "parts_count": ch["parts_count"],
            }
        )
    return [
        {"id": s["id"], "title": s["title"], "chapters": by_section.get(s["id"], [])}
        for s in sections
    ]


@router.get("/chapters/{chapter_id}")
def chapter(chapter_id: int):
    with db() as conn:
        ch = conn.execute(
            """
            SELECT c.*, s.title AS section_title FROM chapters c
            JOIN sections s ON s.id = c.section_id WHERE c.id = ?
            """,
            (chapter_id,),
        ).fetchone()
        if ch is None:
            raise HTTPException(404, "Chapter not found")
        lessons = conn.execute(
            "SELECT id, ord, text FROM lessons WHERE chapter_id = ? ORDER BY ord",
            (chapter_id,),
        ).fetchall()
        lessons = [
            {
                "id": l["id"],
                "ord": l["ord"],
                "text": l["text"],
                "audio": f"/api/lesson/{l['id']}/audio",
                "dur": round(audio_duration(l["id"]), 1),
            }
            for l in lessons
        ]
    return {
        "id": ch["id"],
        "num": ch["num"],
        "title": ch["title"],
        "section": ch["section_title"],
        "lessons": lessons,
    }


@router.get("/lesson/{lesson_id}/audio")
def lesson_audio(lesson_id: str):
    path = audio_file_path(lesson_id)
    if path is None:
        raise HTTPException(404, "Audio not found")
    return FileResponse(path, media_type="audio/wav")


@router.get("/lesson/{lesson_id}/download")
def lesson_download(lesson_id: str):
    with db() as conn:
        row = conn.execute(
            """
            SELECT l.ord, c.num AS chapter_num, c.title AS chapter_title
            FROM lessons l JOIN chapters c ON c.id = l.chapter_id
            WHERE l.id = ?
            """,
            (lesson_id,),
        ).fetchone()
    path = audio_file_path(lesson_id)
    if path is None or row is None:
        raise HTTPException(404, "Audio not found")
    name = (
        f"Урок {row['chapter_num']}. {safe_filename(row['chapter_title'])}"
        f" — часть {row['ord'] + 1}.wav"
    )
    return FileResponse(path, media_type="audio/wav", filename=name)


@router.get("/chapters/{chapter_id}/download")
def chapter_download(chapter_id: int):
    with db() as conn:
        ch = conn.execute(
            "SELECT c.* FROM chapters c WHERE c.id = ?",
            (chapter_id,),
        ).fetchone()
        if ch is None:
            raise HTTPException(404, "Chapter not found")
        lessons = conn.execute(
            "SELECT id FROM lessons WHERE chapter_id = ? ORDER BY ord",
            (chapter_id,),
        ).fetchall()
    paths = [p for l in lessons if (p := audio_file_path(l["id"])) is not None]
    if not paths:
        raise HTTPException(404, "Audio not found")
    tmp = config.AUDIO_DIR / f"dl-{uuid.uuid4().hex}.wav"
    try:
        concat_wavs(paths, tmp)
    except ValueError:
        tmp.unlink(missing_ok=True)
        raise HTTPException(500, "Mismatched audio formats")
    except Exception:
        tmp.unlink(missing_ok=True)
        raise HTTPException(500, "Failed to assemble audio")
    name = f"Урок {ch['num']}. {safe_filename(ch['title'])}.wav"
    return FileResponse(
        tmp,
        media_type="audio/wav",
        filename=name,
        background=BackgroundTask(tmp.unlink, missing_ok=True),
    )
