#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "kokoro>=0.9.4",
#     "soundfile>=0.14.0",
#     "en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
# ]
# ///
"""English reference voice-over: the paragraphs of the English textbook read by Kokoro (American English), one wav per slide.

The wav files go where the backend looks for the lesson audio (`AUDIO_DIR`, by default `backend/data/audio`) under the lesson id the seed computes,
so the player reads a slide with this voice until the author's own recording of the slide is chosen. It is a model to listen to and repeat, not the final voice-over.

    uv run --script voice/synth.py 12 --chapter 1          # book 12, chapter 1 (all its slides)
    uv run --script voice/synth.py 12                      # the whole book
    uv run --script voice/synth.py 12 -c 1 -s 0 --force    # one slide, again
    uv run --script voice/synth.py 12 -c 1 --list          # slides and their ids, nothing is synthesized

Ready files are skipped (`--force` makes them again). The model (Kokoro-82M, ~330 MB) is downloaded on the first run. It needs Python 3.12 or 3.13
(the dependencies of its English text processing do not build on 3.14 yet), `uv` finds it by itself. The Russian voice-over engine is `engine.py`.
"""

import argparse
import os
import re
import sqlite3
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "backend" / "data"
# the same namespace as `NS` in backend/src/seed.rs: lesson ids must match the ones the seed gives the lessons
NS = uuid.UUID(int=0xD3A7C0DE_0000_4000_8000_4B6F6B6F726F)
SAMPLE_RATE = 24000
DEFAULT_VOICE = "af_heart"


def audio_prefixes() -> dict[int, str]:
    """`audio_prefix` of every book from `backend/data/sql/books.sql` (executed in memory, as the seed does)."""
    db = sqlite3.connect(":memory:")
    db.executescript((DATA / "sql" / "books.sql").read_text(encoding="utf-8"))
    return {bid: prefix for bid, prefix in db.execute("SELECT id, audio_prefix FROM books")}


def parse_textbooks(directory: Path) -> dict[int, dict[int, list[str]]]:
    """`{book: {chapter: [paragraphs]}}` the way `parse_textbooks` in backend/src/seed.rs reads the `*.md` files: `#BOOK n`, `#SECTION t`,
    `#CHAPTER n | t`, then the lesson lines; a literal `\\n` is a line break, and a chapter with a single line is split into paragraphs by a blank line."""
    books: dict[int, dict[int, list[str]]] = {}
    book = chapter = None
    for path in sorted(directory.rglob("*.md")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("#BOOK "):
                book, chapter = int(line[6:].strip()), None
                books.setdefault(book, {})
            elif line.startswith("#SECTION "):
                chapter = None
            elif line.startswith("#CHAPTER "):
                chapter = int(line[9:].split("|", 1)[0].strip())
                books[book].setdefault(chapter, [])
            else:
                if book is None or chapter is None:
                    raise SystemExit(f"{path}: a lesson outside a chapter: {line[:60]}")
                books[book][chapter].append(line.replace("\\n", "\n"))
    for chapters in books.values():
        for num, lessons in chapters.items():
            if len(lessons) == 1:
                chapters[num] = [p.strip() for p in lessons[0].split("\n\n") if p.strip()]
    return books


def lesson_id(lang: str, prefix: str, chapter: int, slide: int) -> str:
    """The id the seed gives a lesson of a translated book (`<lang>:<prefix><chapter>-l<slide>`, a uuid5 without dashes)."""
    return uuid.uuid5(NS, f"{lang}:{prefix}{chapter}-l{slide}").hex


def main() -> None:
    ap = argparse.ArgumentParser(description="English reference voice-over of the slides (Kokoro).")
    ap.add_argument("book", type=int, help="book number, e.g. 12")
    ap.add_argument("-c", "--chapter", type=int, action="append", help="chapter number (repeatable); default: every chapter of the book")
    ap.add_argument("-s", "--slide", type=int, help="slide number, from 0; default: every slide")
    ap.add_argument("--voice", default=DEFAULT_VOICE, help=f"Kokoro voice, default {DEFAULT_VOICE} (others: af_bella, af_nicole, am_michael, am_puck; bf_*/bm_* are British)")
    ap.add_argument("--speed", type=float, default=1.0, help="speaking speed, 1.0 is normal; slower (0.85-0.95) is easier to repeat")
    ap.add_argument("--force", action="store_true", help="synthesize again the slides that already have a file")
    ap.add_argument("--list", action="store_true", help="only list the slides, their ids and whether a file exists")
    ap.add_argument("--audio-dir", default=os.environ.get("AUDIO_DIR") or str(DATA / "audio"), help="where the wav files go (default: AUDIO_DIR or backend/data/audio)")
    args = ap.parse_args()

    lang = "en"
    books = parse_textbooks(DATA / lang / "textbook")
    if args.book not in books:
        raise SystemExit(f"book {args.book} has no English textbook in {DATA / lang / 'textbook'}")
    prefix = audio_prefixes().get(args.book) or f"b{args.book}-ch"
    chapters = books[args.book]
    wanted = args.chapter or sorted(chapters)
    for num in wanted:
        if num not in chapters:
            raise SystemExit(f"book {args.book} has no chapter {num} (there are {min(chapters)}..{max(chapters)})")

    audio_dir = Path(args.audio_dir)
    todo = []
    for num in wanted:
        for slide, text in enumerate(chapters[num]):
            if args.slide is not None and slide != args.slide:
                continue
            path = audio_dir / f"{lesson_id(lang, prefix, num, slide)}.wav"
            todo.append((num, slide, text, path))
    if args.slide is not None and not todo:
        raise SystemExit(f"no slide {args.slide} in the chosen chapters")

    if args.list:
        for num, slide, text, path in todo:
            print(f"{args.book}/{num}/{slide}  {path.name}  {'ready' if path.exists() else '-'}  {len(text)} chars")
        return

    todo = [t for t in todo if args.force or not t[3].exists()]
    if not todo:
        print("nothing to do: every slide has a file (--force makes them again)")
        return

    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline

    audio_dir.mkdir(parents=True, exist_ok=True)
    started = time.time()
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")  # "a" - American English
    print(f"model ready in {time.time() - started:.0f} s; {len(todo)} slides, voice {args.voice}, speed {args.speed}", flush=True)
    total = 0.0
    for num, slide, text, path in todo:
        began = time.time()
        # Kokoro reads a paragraph as sentence-sized pieces; the pieces are joined as they come (the pauses are the model's own)
        text = re.sub(r"\s+", " ", text).strip()
        pieces = [np.asarray(audio, dtype=np.float32) for _, _, audio in pipeline(text, voice=args.voice, speed=args.speed) if audio is not None]
        if not pieces:
            raise SystemExit(f"{args.book}/{num}/{slide}: nothing was synthesized")
        samples = np.concatenate(pieces)
        # write to a temporary name and rename, so a half-written file is never served
        tmp = path.with_suffix(".part")
        sf.write(str(tmp), samples, SAMPLE_RATE, format="WAV", subtype="PCM_16")
        tmp.replace(path)
        seconds = len(samples) / SAMPLE_RATE
        total += seconds
        print(f"{args.book}/{num}/{slide}: {seconds:5.1f} s of sound in {time.time() - began:4.1f} s -> {path.name}", flush=True)
    print(f"done: {total / 60:.1f} min of sound in {time.time() - started:.0f} s; files in {audio_dir}")


if __name__ == "__main__":
    sys.exit(main())
