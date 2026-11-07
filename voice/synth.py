#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12,<3.14"
# dependencies = [
#     "kokoro>=0.9.4",
#     "soundfile>=0.14.0",
#     "en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
# ]
# ///
"""English reference voice-over: the paragraphs of the English textbook read by Kokoro (American English), one take per slide.

The reading is added to the slide's recordings (`RECORDS_DIR`, by default `media/records`: `en/<book>/<chapter>/<slide>/<take>.wav`) as an ordinary take
marked by a file `<take>.machine` with the voice's name. The recordings window lists it as "Machine voice" next to the author's own takes; it can be chosen
as the slide's voice-over, deleted and replaced like them. It is a model to listen to and repeat, not the final voice-over.

    uv run --script voice/synth.py 12 --chapter 1          # book 12, chapter 1 (all its slides)
    uv run --script voice/synth.py 12                      # the whole book
    uv run --script voice/synth.py 12 -c 1 -s 0 --force    # one slide, again (the same take is replaced)
    uv run --script voice/synth.py 12 -c 1 --list          # slides and their takes, nothing is synthesized

A slide that already has a machine take is skipped (`--force` reads it again). A new take gets the next free number, so the author's takes keep theirs and
the first take of a slide (the default voice-over) is not changed when it already exists. The model (Kokoro-82M, ~330 MB) is downloaded on the first run.
It needs Python 3.12 or 3.13 (the dependencies of its English text processing do not build on 3.14 yet), `uv` finds it by itself.
The Russian voice-over engine is `engine.py`.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "backend" / "data"
SAMPLE_RATE = 24000
DEFAULT_VOICE = "af_heart"


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


def slide_dir(records: Path, lang: str, book: int, chapter: int, slide: int) -> Path:
    """Where the takes of a slide live, as in `backend/src/records.rs`: Russian is the root, another language has its own folder."""
    base = records if lang == "ru" else records / lang
    return base / str(book) / str(chapter) / str(slide)


def machine_take(directory: Path) -> int | None:
    """The number of the slide's machine take (a wav with a `.machine` marker), if there is one."""
    for marker in sorted(directory.glob("*.machine")) if directory.is_dir() else []:
        if marker.stem.isdigit() and marker.with_suffix(".wav").exists():
            return int(marker.stem)
    return None


def next_take(directory: Path) -> int:
    """The next free take number: after every numbered file of the folder (takes, markers and scores), as the backend numbers a new recording."""
    used = [int(p.name.split(".")[0]) for p in directory.iterdir() if p.name.split(".")[0].isdigit()] if directory.is_dir() else []
    return max(used, default=0) + 1


def main() -> None:
    ap = argparse.ArgumentParser(description="English reference voice-over of the slides (Kokoro).")
    ap.add_argument("book", type=int, help="book number, e.g. 12")
    ap.add_argument("-c", "--chapter", type=int, action="append", help="chapter number (repeatable); default: every chapter of the book")
    ap.add_argument("-s", "--slide", type=int, help="slide number, from 0; default: every slide")
    ap.add_argument("--voice", default=DEFAULT_VOICE, help=f"Kokoro voice, default {DEFAULT_VOICE} (others: af_bella, af_nicole, am_michael, am_puck; bf_*/bm_* are British)")
    ap.add_argument("--speed", type=float, default=1.0, help="speaking speed, 1.0 is normal; slower (0.85-0.95) is easier to repeat")
    ap.add_argument("--force", action="store_true", help="synthesize again the slides that already have a file")
    ap.add_argument("--list", action="store_true", help="only list the slides, their ids and whether a file exists")
    ap.add_argument("--records-dir", default=os.environ.get("RECORDS_DIR") or str(ROOT / "media" / "records"), help="the recordings folder of the backend (default: RECORDS_DIR or media/records)")
    args = ap.parse_args()

    lang = "en"
    books = parse_textbooks(DATA / lang / "textbook")
    if args.book not in books:
        raise SystemExit(f"book {args.book} has no English textbook in {DATA / lang / 'textbook'}")
    chapters = books[args.book]
    wanted = args.chapter or sorted(chapters)
    for num in wanted:
        if num not in chapters:
            raise SystemExit(f"book {args.book} has no chapter {num} (there are {min(chapters)}..{max(chapters)})")

    records = Path(args.records_dir)
    todo = []
    for num in wanted:
        for slide, text in enumerate(chapters[num]):
            if args.slide is not None and slide != args.slide:
                continue
            todo.append((num, slide, text, slide_dir(records, lang, args.book, num, slide)))
    if args.slide is not None and not todo:
        raise SystemExit(f"no slide {args.slide} in the chosen chapters")

    if args.list:
        for num, slide, text, directory in todo:
            machine = machine_take(directory)
            own = len([p for p in directory.glob("*.wav") if p.stem.isdigit()]) - (machine is not None) if directory.is_dir() else 0
            print(f"{args.book}/{num}/{slide}  machine take: {machine if machine else '-'}  own takes: {own}  {len(text)} chars")
        return

    todo = [t for t in todo if args.force or machine_take(t[3]) is None]
    if not todo:
        print("nothing to do: every slide has a machine take (--force reads them again)")
        return

    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline

    started = time.time()
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")  # "a" - American English
    print(f"model ready in {time.time() - started:.0f} s; {len(todo)} slides, voice {args.voice}, speed {args.speed}", flush=True)
    total = 0.0
    for num, slide, text, directory in todo:
        began = time.time()
        # Kokoro reads a paragraph as sentence-sized pieces; the pieces are joined as they come (the pauses are the model's own)
        text = re.sub(r"\s+", " ", text).strip()
        pieces = [np.asarray(audio, dtype=np.float32) for _, _, audio in pipeline(text, voice=args.voice, speed=args.speed) if audio is not None]
        if not pieces:
            raise SystemExit(f"{args.book}/{num}/{slide}: nothing was synthesized")
        samples = np.concatenate(pieces)
        directory.mkdir(parents=True, exist_ok=True)
        take = machine_take(directory) or next_take(directory)
        wav = directory / f"{take}.wav"
        # the marker first, then the wav under its final name in one step: the backend lists a take by its wav, so it never sees a half-made take
        (directory / f"{take}.machine").write_text(args.voice, encoding="utf-8")
        (directory / f"{take}.score.json").unlink(missing_ok=True)  # a check of the replaced reading does not belong to the new one
        tmp = directory / f"{take}.part"
        sf.write(str(tmp), samples, SAMPLE_RATE, format="WAV", subtype="PCM_16")
        tmp.replace(wav)
        seconds = len(samples) / SAMPLE_RATE
        total += seconds
        print(f"{args.book}/{num}/{slide}: {seconds:5.1f} s of sound in {time.time() - began:4.1f} s -> take {take}", flush=True)
    print(f"done: {total / 60:.1f} min of sound in {time.time() - started:.0f} s; takes in {records / lang}")


if __name__ == "__main__":
    sys.exit(main())
