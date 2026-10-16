"""Квизы в БД: загрузка из SQL-файлов и API — вопросы без ответов, ответ после выбора, одна попытка на вопрос.
Запуск: uv run python -m unittest discover -s tests -t .  (Docker не нужен)."""

import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app import config
from app.quizzes import store


class QuizSqlTest(unittest.TestCase):
    def test_sql_files_load_and_are_consistent(self):
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        total = store.reload_quizzes(conn)
        self.assertGreater(total, 1200)
        for (book, chapter), answers in store.answers_map(conn).items():
            quiz = store.get_quiz(conn, book, chapter)
            self.assertIsNotNone(quiz, f"{book}:{chapter}")
            self.assertEqual(len(quiz["questions"]), len(answers))
            for i, q in enumerate(quiz["questions"]):
                self.assertTrue(0 <= q["answer"] < len(q["options"]), f"{book}:{chapter} #{i + 1}")
                self.assertEqual(len(set(q["options"])), len(q["options"]), f"{book}:{chapter} #{i + 1}: одинаковые варианты")
                self.assertTrue(q["expl"], f"{book}:{chapter} #{i + 1}: нет пояснения")
        # перезагрузка идемпотентна
        self.assertEqual(store.reload_quizzes(conn), total)
        conn.close()

    def test_plain_sqlite_can_run_files(self):
        conn = sqlite3.connect(":memory:")
        for f in store.sql_files():
            conn.executescript(f.read_text(encoding="utf-8"))
        self.assertGreater(conn.execute("SELECT COUNT(*) FROM quiz_questions").fetchone()[0], 1200)
        conn.close()


class QuizApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls._old = config.DB_PATH
        config.DB_PATH = Path(cls._tmp.name) / "q.db"
        from app.main import app

        cls._ctx = TestClient(app)
        cls.c = cls._ctx.__enter__()

    def setUp(self):
        r = self.c.post("/api/auth/login", json={"login": "student", "password": "student"})
        self.assertEqual(r.status_code, 200)

    @classmethod
    def tearDownClass(cls):
        cls._ctx.__exit__(None, None, None)
        config.DB_PATH = cls._old
        cls._tmp.cleanup()

    def test_questions_come_without_answers(self):
        d = self.c.get("/api/quizzes/13/5").json()
        self.assertEqual(len(d["questions"]), len(d["reveal"]))
        for q in d["questions"]:
            self.assertEqual(set(q), {"q", "options"})
        self.assertTrue(all(r is None for r in d["reveal"]))
        self.assertNotIn('"answer"', json.dumps(d["questions"]))

    def test_answer_reveals_once_and_is_final(self):
        c = self.c
        c.delete("/api/progress/quiz", params={"book": 13, "chapter": 6})
        a = c.post("/api/quizzes/13/6/answer", json={"question": 0, "pick": 0}).json()
        self.assertIn(a["answer"], range(4))
        self.assertTrue(a["expl"])
        # повторный выбор другого варианта ничего не меняет
        other = (a["pick"] + 1) % 4
        b = c.post("/api/quizzes/13/6/answer", json={"question": 0, "pick": other}).json()
        self.assertEqual(b["pick"], a["pick"])
        d = c.get("/api/quizzes/13/6").json()
        self.assertEqual(d["reveal"][0], {"answer": a["answer"], "expl": a["expl"]})
        self.assertTrue(all(r is None for r in d["reveal"][1:]))
        p = c.get("/api/progress").json()
        self.assertEqual(p["quiz"]["13:6"][0], a["pick"])
        self.assertEqual(p["quizRight"]["13:6"], 1 if a["pick"] == a["answer"] else 0)
        # стереть можно, подставить выбранное задним числом — нельзя
        self.assertEqual(c.put("/api/progress/quiz", json={"book": 13, "chapter": 6, "picks": [0]}).status_code, 405)
        c.delete("/api/progress/quiz", params={"book": 13, "chapter": 6})
        self.assertTrue(all(r is None for r in c.get("/api/quizzes/13/6").json()["reveal"]))

    def test_bad_requests(self):
        c = self.c
        self.assertEqual(c.post("/api/quizzes/13/6/answer", json={"question": 99, "pick": 0}).status_code, 404)
        self.assertEqual(c.post("/api/quizzes/13/6/answer", json={"question": 0, "pick": 9}).status_code, 422)
        self.assertEqual(c.get("/api/quizzes/13/999").status_code, 404)
        self.assertEqual(c.get("/api/quizzes").json()["13"]["5"], 5)
        c.cookies.clear()
        self.assertEqual(c.get("/api/quizzes/13/5").status_code, 401)


if __name__ == "__main__":
    unittest.main()
