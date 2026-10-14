"""Сервис курса: соединение с БД, схема, аудио-файлы и их длительности."""

import re
import sqlite3
import wave
from pathlib import Path

from app import config


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            ord INTEGER NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sections (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL DEFAULT 1 REFERENCES books(id),
            title TEXT NOT NULL,
            ord INTEGER NOT NULL
        )
        """
    )
    scols = {r["name"] for r in conn.execute("PRAGMA table_info(sections)")}
    if "book_id" not in scols:
        conn.execute(
            "ALTER TABLE sections ADD COLUMN book_id INTEGER NOT NULL DEFAULT 1"
        )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY,
            section_id INTEGER NOT NULL REFERENCES sections(id),
            num INTEGER NOT NULL,
            title TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS lessons (
            id TEXT PRIMARY KEY,
            chapter_id INTEGER NOT NULL REFERENCES chapters(id),
            ord INTEGER NOT NULL,
            text TEXT NOT NULL
        )
        """
    )


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    return (
        conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
        ).fetchone()
        is not None
    )


def audio_file_path(item_id: str) -> Path | None:
    p = config.AUDIO_DIR / f"{item_id}.wav"
    return p if p.is_file() else None


_audio_dur_cache: dict[str, float] = {}


def audio_duration(item_id: str) -> float:
    """Длительность аудио части в секундах (0, если файла нет)."""
    if item_id in _audio_dur_cache:
        return _audio_dur_cache[item_id]
    dur = 0.0
    path = audio_file_path(item_id)
    if path is not None:
        try:
            with wave.open(str(path), "rb") as w:
                dur = w.getnframes() / w.getframerate()
        except wave.Error:
            dur = 0.0
    # Нулевые длительности не кэшируем: файл мог быть ещё не сгенерирован.
    if dur > 0:
        _audio_dur_cache[item_id] = dur
    return dur


def safe_filename(s: str) -> str:
    return re.sub(r'[\\/:*?"<>|]+', " ", s).strip()[:80]


def concat_wavs(paths: list[Path], out: Path) -> None:
    params = None
    with wave.open(str(out), "wb") as wout:
        for p in paths:
            with wave.open(str(p), "rb") as win:
                cur = (win.getnchannels(), win.getsampwidth(), win.getframerate())
                if params is None:
                    params = cur
                    wout.setnchannels(cur[0])
                    wout.setsampwidth(cur[1])
                    wout.setframerate(cur[2])
                elif cur != params:
                    raise ValueError(f"mismatched wav formats: {p}")
                wout.writeframes(win.readframes(win.getnframes()))
