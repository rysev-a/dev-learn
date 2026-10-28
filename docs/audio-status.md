# Voice-over status

As of 16.10.2026: **all audio has been deleted** (`backend/data/audio/` is empty) to keep the project light. The voice-over will be
generated once at the end, when all chapters of all books are ready. For now the slides run on virtual clocks
(≈ 14 characters per second), and the paragraph text is shown by the "Voice-over" window.

## How the voice-over will work

- Each lesson paragraph is a separate wav (`<uuid5>.wav`); the id is computed from the book's `AUDIO_PREFIX`, the chapter number and the
  paragraph number (`backend/src/seed.rs`; the previous implementation is `app/books/seed.py` in the `legacy-react-python` tag).
- Generation: the engine is `voice/engine.py` (kokoro-ru; the model — `cd voice && uv run download_model.py`, ~640 MB); a script that
  reads `backend/data/textbook`, splits the chapters into paragraphs and writes wav files to `backend/data/audio/<uuid5>.wav` (skipping ready ones)
  will be written when it is time for the voice-over, modeled on `backend/seed_textbook.py` from the `legacy-react-python` tag.
- The voice is kokoro-ru (`sveta`); one chapter (13 parts) is synthesized in 1.5–2 minutes.
- After the voice-over, the `cues` in the slides must be recalculated from the pauses in the wav (currently they are based on the share of characters), and the running backend
  must be restarted: it caches durations.
