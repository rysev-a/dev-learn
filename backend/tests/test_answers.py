"""Задачи с вводом ответа в БД: загрузка из SQL, проверка ответа на сервере, ответ не раскрывается.
Запуск: uv run python -m unittest discover -s tests -t ."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app import config
from app.answers import store


class CheckerTest(unittest.TestCase):
    def test_normalization_and_numbers(self):
        self.assertTrue(store.is_correct("  ДА ", ["да"]))
        self.assertTrue(store.is_correct("6.0", ["6"]))
        self.assertTrue(store.is_correct("0,5", ["0.5"]))
        self.assertTrue(store.is_correct("1  2", ["1 2"]))
        self.assertFalse(store.is_correct("", ["0"]))
        self.assertFalse(store.is_correct("7", ["6"]))
        self.assertTrue(store.is_correct("истинно", ["да", "истинно"]))

    def test_sql_files_load(self):
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        total = store.reload_answers(conn)
        self.assertGreaterEqual(total, 70)
        for book, chapters in store.counts(conn).items():
            for chapter, n in chapters.items():
                aset = store.get_set(conn, book, chapter)
                self.assertEqual(len(aset["tasks"]), n)
                for t in aset["tasks"]:
                    self.assertTrue(t["answers"] and t["q"])
        self.assertEqual(store.reload_answers(conn), total)
        conn.close()


class AnswersApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls._old = config.DB_PATH
        config.DB_PATH = Path(cls._tmp.name) / "a.db"
        from app.main import app

        cls._ctx = TestClient(app)
        cls.c = cls._ctx.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls._ctx.__exit__(None, None, None)
        config.DB_PATH = cls._old
        cls._tmp.cleanup()

    def setUp(self):
        self.assertEqual(self.c.post("/api/auth/login", json={"login": "student", "password": "student"}).status_code, 200)

    def test_no_answers_leak_and_check_flow(self):
        c = self.c
        c.delete("/api/answers", params={"book": 12, "chapter": 1})
        d = c.get("/api/answers/12/1").json()
        self.assertNotIn("answers", d["tasks"][0])
        self.assertEqual(d["solved"], {})
        self.assertFalse(c.post("/api/answers/12/1/check", json={"task": 0, "value": "999"}).json()["ok"])
        self.assertEqual(c.get("/api/answers/12/1").json()["solved"], {})  # неверный ответ ничего не записал
        self.assertTrue(c.post("/api/answers/12/1/check", json={"task": 0, "value": "1"}).json()["ok"])
        self.assertEqual(c.get("/api/answers/12/1").json()["solved"], {"0": "1"})
        self.assertEqual(c.get("/api/progress").json()["answers"]["12:1"], {"0": "1"})
        self.assertEqual(c.delete("/api/answers", params={"book": 12, "chapter": 1}).status_code, 204)
        self.assertEqual(c.get("/api/answers/12/1").json()["solved"], {})

    def test_errors_and_counts(self):
        c = self.c
        self.assertEqual(c.post("/api/answers/12/1/check", json={"task": 99, "value": "1"}).status_code, 404)
        self.assertEqual(c.get("/api/answers/12/99").status_code, 404)
        self.assertIn(c.put("/api/progress/answers", json={}).status_code, (404, 405))
        self.assertEqual(c.get("/api/answers").json()["12"]["1"], 7)
        c.cookies.clear()
        self.assertEqual(c.get("/api/answers/12/1").status_code, 401)


if __name__ == "__main__":
    unittest.main()
