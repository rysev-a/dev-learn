"""Упражнения в БД: SQL-файлы не отстают от Python-модулей, загрузка из них восстанавливает задачи без потерь,
а API читает их из таблицы. Запуск: uv run python -m unittest discover -s tests -t .  (Docker не нужен)."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

import export_tasks
from app import config
from app.exercises import sources, store


class TasksSqlTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = sqlite3.connect(":memory:")
        cls.conn.row_factory = sqlite3.Row
        store.reload_tasks(cls.conn)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_sql_files_are_up_to_date(self):
        """Правили модуль задач и забыли `uv run export_tasks.py` — тест напомнит."""
        for name, text in export_tasks.expected_files().items():
            path = config.TASKS_SQL_DIR / name
            self.assertTrue(path.exists(), f"нет {name}: uv run export_tasks.py")
            self.assertEqual(path.read_text(encoding="utf-8"), text, f"{name} отстал: uv run export_tasks.py")
        self.assertEqual({p.name for p in store.sql_files()}, set(export_tasks.expected_files()))

    def test_roundtrip_is_lossless(self):
        """Из БД задача возвращается ровно такой же, как в модуле, включая кортежи."""
        n = 0
        for book, chapters in sources.BOOK_TASKS.items():
            for chapter, items in chapters.items():
                loaded = store.chapter_rows(self.conn, book, chapter)
                self.assertEqual(loaded, items, f"книга {book}, глава {chapter}")
                n += len(items)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0], n)

    def test_tuples_survive(self):
        spec = store.split_task({"id": "x", "tests": [{"args": [(1, 2)], "expected": (1, 9)}]})[1]
        row = {"id": "x", **{k: None for k in store.PUBLIC_FIELDS}, "spec": spec}
        self.assertEqual(store.join_task(row)["tests"][0]["expected"], (1, 9))
        self.assertIsInstance(store.join_task(row)["tests"][0]["args"][0], tuple)

    def test_reload_is_idempotent_and_replaces(self):
        before = self.conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        self.conn.execute("INSERT INTO tasks (book_id, chapter, id, ord, spec) VALUES (99, 1, 'junk', 0, '{}')")
        store.reload_tasks(self.conn)
        self.assertEqual(self.conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0], before)

    def test_ensure_fills_empty_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            conn = sqlite3.connect(Path(tmp) / "empty.db")
            conn.row_factory = sqlite3.Row
            store.ensure_tasks(conn)
            self.assertGreater(conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0], 4000)
            conn.close()

    def test_files_run_in_plain_sqlite(self):
        """Файлы пригодны и для `sqlite3 say.db < *.sql`: каждый выполняется как есть, по порядку."""
        conn = sqlite3.connect(":memory:")
        for f in store.sql_files():
            conn.executescript(f.read_text(encoding="utf-8"))
        self.assertEqual(
            conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0],
            sum(len(items) for chapters in sources.BOOK_TASKS.values() for items in chapters.values()),
        )


if __name__ == "__main__":
    unittest.main()
