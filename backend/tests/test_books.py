"""Метаданные книг (app/data/sql/books.sql): файл применим как есть, а ссылки из него ведут на существующее —
каталог слайдов, иконку, учебник, задачи и квизы. Запуск: uv run python -m unittest discover -s tests -t ."""

import re
import sqlite3
import unittest

from app import config
from app.books import meta, seed
from app.exercises import store as task_store
from app.quizzes import store as quiz_store

FRONTEND = config.APP_DIR.parent.parent / "frontend" / "src"


class BooksMetaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(":memory:")
        cls.conn.row_factory = sqlite3.Row
        meta.load_books(cls.conn)
        cls.books = {r["id"]: dict(r) for r in cls.conn.execute("SELECT * FROM books")}

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_idempotent_and_complete(self):
        before = meta.load_books(self.conn)
        self.assertEqual(meta.load_books(self.conn), before)
        for b in self.books.values():
            for col in ("slug", "slides_dir", "icon", "audio_prefix", "title"):
                self.assertTrue(b[col], f"книга {b['id']}: пустое поле {col}")
        self.assertEqual(len({b["ord"] for b in self.books.values()}), len(self.books), "порядок книг неоднозначен")
        self.assertEqual(len({b["audio_prefix"] for b in self.books.values()}), len(self.books))

    def test_slides_dirs_and_icons_exist(self):
        icons = set(re.findall(r"^  (\w+): \(", (FRONTEND / "components" / "BookIcon.tsx").read_text(encoding="utf-8"), re.M))
        for b in self.books.values():
            self.assertTrue((FRONTEND / "slides" / b["slides_dir"]).is_dir(), f"нет каталога слайдов {b['slides_dir']}")
            self.assertIn(b["icon"], icons, f"нет иконки {b['icon']} в BookIcon.tsx")

    def test_every_book_with_content_is_registered(self):
        textbook_ids = {int(m) for p in config.TEXTBOOK_DIR.rglob("*.md") for m in re.findall(r"^#BOOK\s+(\d+)$", p.read_text(encoding="utf-8"), re.M)}
        self.assertLessEqual(textbook_ids, set(self.books), "учебник книги, которой нет в books.sql")
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        task_store.reload_tasks(conn)
        quiz_store.reload_quizzes(conn)
        self.assertLessEqual({r[0] for r in conn.execute("SELECT DISTINCT book_id FROM tasks")}, set(self.books))
        self.assertLessEqual({r[0] for r in conn.execute("SELECT DISTINCT book_id FROM quizzes")}, set(self.books))
        conn.close()

    def test_seed_uses_prefixes_from_metadata(self):
        self.assertEqual(meta.audio_prefix(self.conn, 13), "learn-py-ch")
        self.assertEqual(meta.audio_prefix(self.conn, 999), "b999-ch")
        self.assertFalse(hasattr(seed, "AUDIO_PREFIX"))


if __name__ == "__main__":
    unittest.main()
