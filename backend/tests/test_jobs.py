"""Очередь проверок кода: постановка, выдача воркеру, аренда, кэш, токен. Docker не нужен: воркер изображаем сами.

Запуск из каталога backend/:  uv run python -m unittest discover -s tests -t ."""

import tempfile
import time
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app import config
from app.books.service import db
from app.exercises import jobs

TOKEN = {"Authorization": "Bearer test-token"}
OK = {"status": "ok", "results": [{"ok": True, "got": "1", "expected": "1", "error": None}], "stdout": "", "stderr": ""}


class JobsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls._old = (config.DB_PATH, config.RUNNER_MODE, config.WORKER_TOKEN)
        config.DB_PATH = Path(cls._tmp.name) / "test.db"
        config.RUNNER_MODE = "remote"
        config.WORKER_TOKEN = "test-token"
        from app.main import app

        cls._ctx = TestClient(app)
        cls.client = cls._ctx.__enter__()
        cls.client.post("/api/auth/login", json={"login": "student", "password": "student"})
        cls.py = cls.client.get("/api/exercises/13/5").json()["tasks"][0]["id"]
        cls.rs = cls.client.get("/api/exercises/10/1").json()["tasks"][0]["id"]

    @classmethod
    def tearDownClass(cls):
        cls._ctx.__exit__(None, None, None)
        config.DB_PATH, config.RUNNER_MODE, config.WORKER_TOKEN = cls._old
        cls._tmp.cleanup()

    def setUp(self):
        with db() as conn:
            conn.execute("DELETE FROM exec_jobs")
            conn.execute("DELETE FROM exec_cache")
            conn.execute("DELETE FROM exec_workers")

    def submit(self, code="x = 1", task=None, book=13, chapter=5):
        return self.client.post("/api/exercises/run", json={"book": book, "chapter": chapter, "task": task or self.py, "code": code})

    def ping(self, name="w1", lanes=("light", "heavy")):
        r = self.client.post("/internal/worker/ping", headers=TOKEN, json={"name": name, "lanes": list(lanes), "slots": 2})
        self.assertEqual(r.status_code, 204)

    def claim(self, name="w1", lanes=("light",)):
        return self.client.post("/internal/worker/claim", headers=TOKEN, json={"name": name, "lanes": list(lanes), "wait": 0})

    def test_unavailable_without_workers(self):
        self.assertFalse(self.client.get("/api/exercises/runner/status").json()["available"])
        r = self.submit()
        self.assertEqual(r.status_code, 503)
        self.assertIn("временно недоступна", r.json()["detail"])

    def test_full_cycle(self):
        self.ping()
        self.assertTrue(self.client.get("/api/exercises/runner/status").json()["available"])
        r = self.submit("x = 1")
        self.assertEqual(r.status_code, 202)
        job_id = r.json()["id"]
        self.assertEqual((r.json()["state"], r.json()["position"]), ("queued", 1))
        self.assertEqual(self.submit("x = 2").status_code, 429)  # одна проверка на пользователя

        c = self.claim()
        self.assertEqual(c.status_code, 200)
        job = c.json()
        self.assertEqual((job["id"], job["code"], job["lane"]), (job_id, "x = 1", "light"))
        self.assertIn("mode", job["task"])  # воркеру уходит полное определение задачи
        self.assertEqual(self.client.get(f"/api/exercises/run/{job_id}").json()["state"], "running")
        self.assertEqual(self.claim().status_code, 204)

        # чужой воркер и неверный токен
        bad = self.client.post(f"/internal/worker/jobs/{job_id}/result", headers=TOKEN, json={"name": "other", "result": OK})
        self.assertEqual(bad.status_code, 409)
        self.assertEqual(self.client.post("/internal/worker/ping", headers={"Authorization": "Bearer nope"}, json={"name": "w", "lanes": []}).status_code, 401)

        done = self.client.post(f"/internal/worker/jobs/{job_id}/result", headers=TOKEN, json={"name": "w1", "result": OK})
        self.assertEqual(done.status_code, 204)
        state = self.client.get(f"/api/exercises/run/{job_id}").json()
        self.assertEqual((state["state"], state["solved"], state["passed"], state["total"]), ("done", True, 1, 1))
        self.assertEqual(self.client.get(f"/api/exercises/13/5/{self.py}/attempts").json()["attempts"][0]["status"], "ok")
        # повторный результат не принимается
        again = self.client.post(f"/internal/worker/jobs/{job_id}/result", headers=TOKEN, json={"name": "w1", "result": OK})
        self.assertEqual(again.status_code, 409)

        # тот же код — готовый результат из кэша, без воркера
        cached = self.submit("x = 1")
        self.assertEqual(cached.status_code, 202)
        self.assertEqual((cached.json()["state"], cached.json()["solved"]), ("done", True))

    def test_lanes_are_separate(self):
        self.ping()
        r = self.submit("fn main() {}", task=self.rs, book=10, chapter=1)
        self.assertEqual(r.status_code, 202)
        self.assertEqual(self.claim(lanes=("light",)).status_code, 204)  # rust — в тяжёлой полосе
        got = self.claim(lanes=("heavy",))
        self.assertEqual((got.status_code, got.json()["lane"]), (200, "heavy"))

    def test_lease_expires_and_job_returns_to_queue(self):
        self.ping()
        job_id = self.submit().json()["id"]
        self.assertEqual(self.claim().status_code, 200)
        with db() as conn:
            conn.execute("UPDATE exec_jobs SET lease_until = ?", (time.time() - 1,))
        again = self.claim("w2")  # воркер пропал — задание достаётся другому
        self.assertEqual((again.status_code, again.json()["id"]), (200, job_id))
        with db() as conn:
            self.assertEqual(conn.execute("SELECT attempts FROM exec_jobs WHERE id = ?", (job_id,)).fetchone()[0], 2)
            conn.execute("UPDATE exec_jobs SET lease_until = ?", (time.time() - 1,))
        self.ping("w2")
        state = None
        for _ in range(2):  # попытки кончились: ошибка вместо бесконечного ожидания
            self.claim("w3")
            state = self.client.get(f"/api/exercises/run/{job_id}").json()
        self.assertEqual((state["state"], state["status"]), ("done", "error"))
        self.assertFalse(state["solved"])

    def test_ping_extends_lease(self):
        self.ping()
        job_id = self.submit().json()["id"]
        self.claim()
        with db() as conn:
            conn.execute("UPDATE exec_jobs SET lease_until = ?", (time.time() + 1,))
        r = self.client.post("/internal/worker/ping", headers=TOKEN, json={"name": "w1", "lanes": ["light"], "slots": 1, "jobs": [job_id]})
        self.assertEqual(r.status_code, 204)
        with db() as conn:
            self.assertGreater(conn.execute("SELECT lease_until FROM exec_jobs").fetchone()[0], time.time() + jobs.LEASE_SEC - 5)

    def test_queue_limit_and_foreign_job(self):
        self.ping()
        old = jobs.QUEUE_LIMIT
        jobs.QUEUE_LIMIT = 0
        try:
            self.assertEqual(self.submit().status_code, 503)
        finally:
            jobs.QUEUE_LIMIT = old
        job_id = self.submit().json()["id"]
        other = TestClient(self.client.app)
        other.post("/api/auth/login", json={"login": "programmer", "password": "programmer"})
        self.assertEqual(other.get(f"/api/exercises/run/{job_id}").status_code, 404)  # чужую проверку не видно

    def test_internal_api_is_closed_without_token_config(self):
        config.WORKER_TOKEN = ""
        try:
            self.assertEqual(self.client.post("/internal/worker/ping", headers=TOKEN, json={"name": "w", "lanes": []}).status_code, 404)
        finally:
            config.WORKER_TOKEN = "test-token"


if __name__ == "__main__":
    unittest.main()
