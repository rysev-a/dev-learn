"""Checks of the file handling in `synth.py` (no model needed): `python3 voice/test_synth.py`.

The folder layout and the take numbering must match `backend/src/records.rs`, otherwise the machine voice would be written where the backend never looks.
"""

import importlib.util
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location("synth", Path(__file__).with_name("synth.py"))
synth = importlib.util.module_from_spec(spec)
spec.loader.exec_module(synth)

books = synth.parse_textbooks(synth.DATA / "en" / "textbook")
paragraphs = books[12][1]
assert len(paragraphs) == 13, len(paragraphs)
assert paragraphs[0].startswith("Discrete mathematics. Chapter 1."), paragraphs[0][:40]
assert all(p == p.strip() and "\\n" not in p for p in paragraphs)

records = Path("/r")
assert synth.slide_dir(records, "en", 12, 1, 0) == Path("/r/en/12/1/0")
assert synth.slide_dir(records, "ru", 12, 1, 0) == Path("/r/12/1/0")

with tempfile.TemporaryDirectory() as tmp:
    d = Path(tmp) / "slide"
    assert synth.next_take(d) == 1 and synth.machine_take(d) is None  # a slide without a folder
    d.mkdir()
    (d / "1.wav").write_bytes(b"x")
    (d / "selected").write_text("1")
    assert synth.next_take(d) == 2 and synth.machine_take(d) is None  # the author's take, no machine take
    (d / "2.wav").write_bytes(b"x")
    (d / "2.machine").write_text("af_heart")
    (d / "2.score.json").write_text("{}")
    assert synth.machine_take(d) == 2 and synth.next_take(d) == 3
    (d / "5.machine").write_text("af_heart")  # a marker without its wav is not a take
    assert synth.machine_take(d) == 2 and synth.next_take(d) == 6
print("ok")
