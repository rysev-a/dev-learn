"""Checks that `synth.py` computes the same lesson ids and paragraphs as the backend seed (no model needed): `python3 voice/test_synth.py`.

The expected ids were taken from `GET /api/chapters/{id}?lang=en` of a running backend (book 12, chapter 1); if the seed changes how it makes ids,
this fails, and the machine voice would otherwise be written under names the backend never asks for.
"""

import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("synth", Path(__file__).with_name("synth.py"))
synth = importlib.util.module_from_spec(spec)
spec.loader.exec_module(synth)

prefixes = synth.audio_prefixes()
assert prefixes[12] == "dm-ch" and prefixes[19] == "ladm-ch", prefixes

books = synth.parse_textbooks(synth.DATA / "en" / "textbook")
paragraphs = books[12][1]
assert len(paragraphs) == 13, len(paragraphs)
assert paragraphs[0].startswith("Discrete mathematics. Chapter 1."), paragraphs[0][:40]
assert all(p == p.strip() and "\\n" not in p for p in paragraphs)

ids = [synth.lesson_id("en", prefixes[12], 1, i) for i in range(3)]
assert ids == ["6b51b0557c545945b9d3a81082b28173", "e99a32f95f105ec9bbcb3b2996a424f7", "47cf368e66015ce4ab9957fc0ae75753"], ids
assert synth.lesson_id("en", "dm-ch", 1, 0) != synth.lesson_id("ru", "dm-ch", 1, 0)
print("ok")
