"""Тесты кабинета: вход, регистрация, прогресс, история попыток.

Запуск из каталога backend/:  uv run python -m unittest discover -s tests -t .
База — временная, рабочая say.db не затрагивается; Docker не нужен.
"""

import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app import config
from app.accounts import practice
from app.books.service import db
from app.exercises import router


class AccountsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls._old_db = config.DB_PATH
        config.DB_PATH = Path(cls._tmp.name) / "test.db"
        from app.main import app

        cls._ctx = TestClient(app)
        cls.client = cls._ctx.__enter__()

    @classmethod
    def tearDownClass(cls):
        cls._ctx.__exit__(None, None, None)
        config.DB_PATH = cls._old_db
        cls._tmp.cleanup()

    def setUp(self):
        self.client.cookies.clear()

    def login(self, login="student", password="student"):
        r = self.client.post("/api/auth/login", json={"login": login, "password": password})
        self.assertEqual(r.status_code, 200, r.text)
        return r.json()

    # --- вход и регистрация ---

    def test_default_users_can_login_by_login_and_email(self):
        self.assertEqual(self.login("student", "student")["email"], "student@mail.com")
        self.client.cookies.clear()
        self.assertEqual(self.login("programmer@mail.com", "programmer")["login"], "programmer")

    def test_wrong_password_and_unknown_user_are_rejected(self):
        for ident, pw in [("student", "nope"), ("ghost", "student")]:
            r = self.client.post("/api/auth/login", json={"login": ident, "password": pw})
            self.assertEqual(r.status_code, 401)

    def test_me_requires_session_and_logout_ends_it(self):
        self.assertEqual(self.client.get("/api/auth/me").status_code, 401)
        self.login()
        self.assertEqual(self.client.get("/api/auth/me").json()["login"], "student")
        self.assertEqual(self.client.post("/api/auth/logout").status_code, 204)
        self.assertEqual(self.client.get("/api/auth/me").status_code, 401)

    def test_register_validates_and_rejects_duplicates(self):
        ok = {"email": "new@mail.com", "login": "newbie", "password": "secret1"}
        self.assertEqual(self.client.post("/api/auth/register", json=ok).status_code, 201)
        # после регистрации пользователь сразу вошёл
        self.assertEqual(self.client.get("/api/auth/me").json()["login"], "newbie")
        self.client.cookies.clear()
        dup_login = {**ok, "email": "other@mail.com"}
        dup_email = {**ok, "login": "other"}
        self.assertEqual(self.client.post("/api/auth/register", json=dup_login).status_code, 409)
        self.assertEqual(self.client.post("/api/auth/register", json=dup_email).status_code, 409)
        # регистр в логине и email не различается
        upper = {"email": "NEW@mail.com", "login": "NEWBIE", "password": "secret1"}
        self.assertEqual(self.client.post("/api/auth/register", json=upper).status_code, 409)
        for bad in (
            {**ok, "email": "no-at"},
            {**ok, "login": "a b"},
            {**ok, "login": "ab"},
            {**ok, "password": "123"},
        ):
            self.assertEqual(self.client.post("/api/auth/register", json=bad).status_code, 422)

    def test_password_is_not_stored_in_plain_text(self):
        with db() as conn:
            row = conn.execute("SELECT password_hash FROM users WHERE login = 'student'").fetchone()
        self.assertTrue(row["password_hash"].startswith("scrypt$"))
        self.assertNotIn("student", row["password_hash"].split("$", 5)[-1])

    # --- прогресс ---

    def test_progress_requires_login(self):
        self.assertEqual(self.client.get("/api/progress").status_code, 401)
        self.assertEqual(
            self.client.post("/api/progress/slides", json={"book": 13, "chapter": 5, "slide": 0}).status_code,
            401,
        )

    def test_progress_roundtrip_and_isolation_between_users(self):
        self.login("student", "student")
        c = self.client
        self.assertEqual(c.post("/api/progress/slides", json={"book": 13, "chapter": 5, "slide": 2}).status_code, 204)
        c.post("/api/progress/slides", json={"book": 13, "chapter": 5, "slide": 2})  # повтор — без дублей
        c.post("/api/progress/slides", json={"book": 13, "chapter": 5, "slide": 0})
        c.put("/api/progress/quiz", json={"book": 13, "chapter": 5, "picks": [0, 2, None, None, None]})
        c.put("/api/progress/answers", json={"book": 12, "chapter": 1, "solved": {"0": "5", "2": "8"}})
        p = c.get("/api/progress").json()
        self.assertEqual(p["slides"]["13:5"], [0, 2])
        self.assertEqual(p["quiz"]["13:5"], [0, 2, None, None, None])
        self.assertEqual(p["answers"]["12:1"], {"0": "5", "2": "8"})

        # пустые ответы удаляют запись
        c.put("/api/progress/quiz", json={"book": 13, "chapter": 5, "picks": [None, None]})
        self.assertNotIn("13:5", c.get("/api/progress").json()["quiz"])

        # другой пользователь ничего этого не видит
        c.cookies.clear()
        self.login("programmer", "programmer")
        self.assertEqual(c.get("/api/progress").json()["slides"], {})

    def test_reset_scopes(self):
        self.login("student", "student")
        c = self.client
        c.post("/api/progress/slides", json={"book": 7, "chapter": 1, "slide": 1})
        with db() as conn:
            uid = conn.execute("SELECT id FROM users WHERE login = 'student'").fetchone()["id"]
            practice.record_attempt(conn, uid, 13, 5, "t1", "print(1)", 1, 1, True)
        self.assertEqual(c.delete("/api/progress", params={"scope": "practice"}).status_code, 204)
        p = c.get("/api/progress").json()
        self.assertEqual(p["code"], {})
        self.assertIn("7:1", p["slides"])  # слайды практика не трогает
        self.assertEqual(c.delete("/api/progress", params={"scope": "all"}).status_code, 204)
        self.assertEqual(c.get("/api/progress").json()["slides"], {})
        self.assertEqual(c.delete("/api/progress", params={"scope": "x"}).status_code, 422)

    # --- упражнения ---

    def test_attempts_history_and_sticky_solved_status(self):
        with db() as conn:
            uid = conn.execute("SELECT id FROM users WHERE login = 'student'").fetchone()["id"]
            practice.record_attempt(conn, uid, 13, 6, "t", "a = 1", 0, 2, False)
            first = practice.chapter_state(conn, uid, 13, 6)["status"]["t"]
            practice.record_attempt(conn, uid, 13, 6, "t", "a = 2", 2, 2, True)
            practice.record_attempt(conn, uid, 13, 6, "t", "a = 3", 1, 2, False)
            state = practice.chapter_state(conn, uid, 13, 6)
            history = practice.attempts(conn, uid, 13, 6, "t")
        self.assertEqual(first, "bad")
        self.assertEqual(state["status"]["t"], "ok")  # неудача решённое не снимает
        self.assertEqual([h["code"] for h in history], ["a = 3", "a = 2", "a = 1"])  # новые первыми

    def test_history_is_capped(self):
        with db() as conn:
            uid = conn.execute("SELECT id FROM users WHERE login = 'student'").fetchone()["id"]
            for i in range(practice.HISTORY_LIMIT + 5):
                practice.record_attempt(conn, uid, 13, 7, "cap", f"x = {i}", 0, 1, False)
            history = practice.attempts(conn, uid, 13, 7, "cap")
        self.assertEqual(len(history), practice.HISTORY_LIMIT)
        self.assertEqual(history[0]["code"], f"x = {practice.HISTORY_LIMIT + 4}")

    def test_exercise_endpoints_need_login_and_known_task(self):
        c = self.client
        self.assertEqual(
            c.post("/api/exercises/run", json={"book": 13, "chapter": 5, "task": "x", "code": "1"}).status_code,
            401,
        )
        self.login()
        r = c.post("/api/exercises/run", json={"book": 13, "chapter": 5, "task": "нет-такой", "code": "print(1)"})
        self.assertEqual(r.status_code, 404)
        self.assertEqual(c.put("/api/exercises/13/5/нет-такой/draft", json={"code": "x"}).status_code, 404)

    def test_draft_roundtrip(self):
        self.login()
        c = self.client
        tasks = c.get("/api/exercises/13/5").json()["tasks"]
        tid = tasks[0]["id"]
        self.assertEqual(c.put(f"/api/exercises/13/5/{tid}/draft", json={"code": "word = 1"}).status_code, 204)
        self.assertEqual(c.get("/api/exercises/13/5/state").json()["drafts"][tid], "word = 1")
        too_big = {"code": "x" * (router.MAX_DRAFT + 1)}
        self.assertEqual(c.put(f"/api/exercises/13/5/{tid}/draft", json=too_big).status_code, 422)

    def test_lab_tasks_are_solved_in_browser_and_recorded(self):
        """Книга 14: упражнения лаборатории проверяются в браузере; сервер принимает итог."""
        c = self.client
        tasks = c.get("/api/exercises/14/6").json()["tasks"]
        self.assertTrue(tasks and all(t["mode"] == "lab" for t in tasks))
        tid = tasks[0]["id"]
        self.assertEqual(c.put(f"/api/exercises/14/6/{tid}/solved", json={"solution": "{}"}).status_code, 401)
        self.login()
        self.assertEqual(c.put(f"/api/exercises/14/6/{tid}/solved", json={"solution": '{"gates":[]}'}).status_code, 204)
        state = c.get("/api/exercises/14/6/state").json()
        self.assertEqual(state["status"][tid], "ok")
        self.assertEqual(state["drafts"][tid], '{"gates":[]}')  # решение возвращается на доску при входе
        self.assertEqual(c.get(f"/api/exercises/14/6/{tid}/attempts").json()["attempts"][0]["status"], "ok")
        # решённым можно отметить только лабораторную задачу: у кода в песочнице проверка на сервере
        py = c.get("/api/exercises/13/5").json()["tasks"][0]["id"]
        self.assertEqual(c.put(f"/api/exercises/13/5/{py}/solved", json={"solution": "x"}).status_code, 404)
        # запуск в песочнице для лабораторной задачи не предусмотрен
        r = c.post("/api/exercises/run", json={"book": 14, "chapter": 6, "task": tid, "code": "x"})
        self.assertEqual(r.status_code, 422)


if __name__ == "__main__":
    unittest.main()
