"""Очередь проверок кода: API кладёт решение в таблицу `exec_jobs`, воркер забирает его, запускает в песочнице
и возвращает результат. Сам API контейнеры не запускает: воркер может быть потоком внутри процесса
(`SAY_RUNNER=local`, по умолчанию) или отдельным демоном на другой машине (`SAY_RUNNER=remote`, `backend/worker.py`):
он сам приходит за заданиями по HTTPS, ему не нужен ни доступ к базе, ни открытые порты.

Жизнь задания: queued → running (аренда `lease_until`, продлевается сердцебиением воркера; не продлилась —
задание возвращается в очередь, после `MAX_ATTEMPTS` попыток завершается ошибкой) → done (результат и попытка записаны).
Одинаковые решения одной и той же версии задачи не проверяются заново: результат лежит в `exec_cache`."""

import hashlib
import json
import sqlite3
import time
import uuid

from app.accounts import practice
from app.exercises import store

LIGHT, HEAVY = "light", "heavy"
LANES = (LIGHT, HEAVY)
QUEUE_LIMIT = 300  # заданий в очереди, после которых новые отклоняются
LEASE_SEC = 45  # аренда задания; воркер продлевает её каждые несколько секунд
MAX_ATTEMPTS = 2
CACHE_TTL = 7 * 24 * 3600
KEEP_DONE_SEC = 24 * 3600
WORKER_ALIVE_SEC = 30
MAX_RESULT_BYTES = 600_000
MAX_TEXT = 20_000

SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS exec_jobs (
        id TEXT PRIMARY KEY,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        chapter INTEGER NOT NULL,
        task_id TEXT NOT NULL,
        code TEXT NOT NULL,
        key TEXT NOT NULL,
        lane TEXT NOT NULL,
        status TEXT NOT NULL,
        worker TEXT,
        attempts INTEGER NOT NULL DEFAULT 0,
        result TEXT,
        created_at REAL NOT NULL,
        started_at REAL,
        lease_until REAL,
        finished_at REAL
    )
    """,
    "CREATE INDEX IF NOT EXISTS exec_jobs_queue ON exec_jobs (status, lane, created_at)",
    "CREATE INDEX IF NOT EXISTS exec_jobs_user ON exec_jobs (user_id, status)",
    """
    CREATE TABLE IF NOT EXISTS exec_cache (
        key TEXT PRIMARY KEY,
        result TEXT NOT NULL,
        created_at REAL NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS exec_workers (
        name TEXT PRIMARY KEY,
        lanes TEXT NOT NULL,
        slots INTEGER NOT NULL,
        seen REAL NOT NULL
    )
    """,
]


class JobError(Exception):
    """Ошибка постановки в очередь: `code` — HTTP-статус, `args[0]` — текст для пользователя."""

    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code


def init_jobs(conn: sqlite3.Connection) -> None:
    for stmt in SCHEMA:
        conn.execute(stmt)


def lane_of(task: dict) -> str:
    """Компиляторы (rust, c) занимают ядра надолго — у них своя полоса; python и js проверяются быстро."""
    return HEAVY if task.get("mode") in ("rust", "c") else LIGHT


def cache_key(task: dict, code: str) -> str:
    spec = json.dumps(store._enc(task), sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(f"{hashlib.sha256(spec.encode()).hexdigest()}\0{code}".encode()).hexdigest()


# --- постановка ----------------------------------------------------------------------------

def submit(conn: sqlite3.Connection, user_id: int, book: int, chapter: int, task: dict, code: str, runner_ok: bool) -> str:
    """Ставит решение в очередь (или сразу отдаёт кэшированный результат); возвращает id задания."""
    t = time.time()
    reap(conn, t)
    busy = conn.execute(
        "SELECT 1 FROM exec_jobs WHERE user_id = ? AND status IN ('queued', 'running') LIMIT 1", (user_id,)
    ).fetchone()
    if busy:
        raise JobError(429, "Предыдущая проверка ещё идёт")
    key = cache_key(task, code)
    job_id = uuid.uuid4().hex
    lane = lane_of(task)
    row = conn.execute("SELECT result FROM exec_cache WHERE key = ? AND created_at > ?", (key, t - CACHE_TTL)).fetchone()
    cached = json.loads(row["result"]) if row else None
    if cached is None:
        if not runner_ok:
            raise JobError(503, "Проверка кода временно недоступна: сервер проверки не отвечает. Попробуйте чуть позже.")
        queued = conn.execute("SELECT COUNT(*) FROM exec_jobs WHERE status = 'queued'").fetchone()[0]
        if queued >= QUEUE_LIMIT:
            raise JobError(503, "Очередь проверок переполнена — попробуйте через минуту.")
    conn.execute(
        """
        INSERT INTO exec_jobs (id, user_id, book_id, chapter, task_id, code, key, lane, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'queued', ?)
        """,
        (job_id, user_id, book, chapter, task["id"], code, key, lane, t),
    )
    if cached is not None:
        finish(conn, job_id, cached, cache=False)
    return job_id


def _normalize(result: dict) -> dict:
    """Результат от воркера: только известные поля и разумные размеры."""
    status = str(result.get("status", "error"))
    items = result.get("results")
    results = [r for r in items if isinstance(r, dict)][:100] if isinstance(items, list) else []
    out = {
        "status": status,
        "results": results,
        "stdout": str(result.get("stdout", ""))[:MAX_TEXT],
        "stderr": str(result.get("stderr", ""))[:MAX_TEXT],
    }
    if len(json.dumps(out, ensure_ascii=False)) > MAX_RESULT_BYTES:
        return {"status": "error", "results": [], "stdout": "", "stderr": "Результат проверки слишком большой."}
    return out


def finish(conn: sqlite3.Connection, job_id: str, result: dict, cache: bool = True) -> dict:
    """Записывает попытку и итог; успешные проверки кладёт в кэш."""
    job = conn.execute("SELECT * FROM exec_jobs WHERE id = ?", (job_id,)).fetchone()
    result = _normalize(result)
    total = len(result["results"])
    passed = sum(1 for r in result["results"] if r.get("ok"))
    solved = result["status"] == "ok" and total > 0 and passed == total
    attempt = practice.record_attempt(
        conn, job["user_id"], job["book_id"], job["chapter"], job["task_id"], job["code"], passed, total, solved
    )
    payload = {**result, "passed": passed, "total": total, "solved": solved, "attempt": attempt}
    t = time.time()
    conn.execute(
        "UPDATE exec_jobs SET status = 'done', result = ?, finished_at = ?, lease_until = NULL WHERE id = ?",
        (json.dumps(payload, ensure_ascii=False), t, job_id),
    )
    if cache and result["status"] == "ok":
        conn.execute("INSERT OR REPLACE INTO exec_cache (key, result, created_at) VALUES (?, ?, ?)", (job["key"], json.dumps(result, ensure_ascii=False), t))
    return payload


def get_for_user(conn: sqlite3.Connection, job_id: str, user_id: int) -> dict | None:
    """Состояние задания для клиента: queued (с местом в очереди), running или done (с результатом)."""
    job = conn.execute("SELECT * FROM exec_jobs WHERE id = ? AND user_id = ?", (job_id, user_id)).fetchone()
    if job is None:
        return None
    if job["status"] == "done":
        return {"state": "done", **json.loads(job["result"])}
    if job["status"] == "running":
        return {"state": "running"}
    ahead = conn.execute(
        "SELECT COUNT(*) FROM exec_jobs WHERE status = 'queued' AND lane = ? AND created_at < ?", (job["lane"], job["created_at"])
    ).fetchone()[0]
    return {"state": "queued", "position": ahead + 1}


# --- воркеры -------------------------------------------------------------------------------

def claim(conn: sqlite3.Connection, worker: str, lanes: list[str]) -> dict | None:
    """Отдаёт воркеру самое старое задание из его полос или None. Аренда выдаётся атомарно одним UPDATE."""
    lanes = [x for x in lanes if x in LANES]
    if not lanes:
        return None
    t = time.time()
    reap(conn, t)
    marks = ",".join("?" * len(lanes))
    job = conn.execute(
        f"""
        UPDATE exec_jobs SET status = 'running', worker = ?, started_at = ?, lease_until = ?, attempts = attempts + 1
        WHERE id = (SELECT id FROM exec_jobs WHERE status = 'queued' AND lane IN ({marks}) ORDER BY created_at LIMIT 1)
        RETURNING *
        """,
        (worker, t, t + LEASE_SEC, *lanes),
    ).fetchone()
    if job is None:
        return None
    task = store.find(conn, job["book_id"], job["chapter"], job["task_id"])
    if task is None:
        finish(conn, job["id"], {"status": "error", "stderr": "Задача удалена."}, cache=False)
        return None
    return {"id": job["id"], "lane": job["lane"], "task": store._enc(task), "code": job["code"], "lease": LEASE_SEC}


def complete(conn: sqlite3.Connection, job_id: str, worker: str, result: dict) -> bool:
    """Принимает результат от воркера, которому задание выдано; чужой или просроченный ответ отклоняется."""
    row = conn.execute("SELECT status, worker FROM exec_jobs WHERE id = ?", (job_id,)).fetchone()
    if row is None or row["status"] != "running" or row["worker"] != worker:
        return False
    finish(conn, job_id, result)
    return True


def ping(conn: sqlite3.Connection, name: str, lanes: list[str], slots: int, jobs: list[str]) -> None:
    """Сердцебиение воркера: отмечает, что он жив, и продлевает аренду выполняющихся заданий."""
    t = time.time()
    conn.execute(
        "INSERT INTO exec_workers (name, lanes, slots, seen) VALUES (?, ?, ?, ?) "
        "ON CONFLICT (name) DO UPDATE SET lanes = excluded.lanes, slots = excluded.slots, seen = excluded.seen",
        (name, ",".join(lanes), slots, t),
    )
    for job_id in jobs[:100]:
        conn.execute(
            "UPDATE exec_jobs SET lease_until = ? WHERE id = ? AND worker = ? AND status = 'running'", (t + LEASE_SEC, job_id, name)
        )


def reap(conn: sqlite3.Connection, t: float) -> None:
    """Возвращает в очередь задания с просроченной арендой (воркер пропал) и чистит старые записи."""
    for job in conn.execute("SELECT id, attempts FROM exec_jobs WHERE status = 'running' AND lease_until < ?", (t,)).fetchall():
        if job["attempts"] >= MAX_ATTEMPTS:
            finish(conn, job["id"], {"status": "error", "stderr": "Сервер проверки не ответил. Попробуйте ещё раз."}, cache=False)
        else:
            conn.execute("UPDATE exec_jobs SET status = 'queued', worker = NULL, lease_until = NULL WHERE id = ?", (job["id"],))
    conn.execute("DELETE FROM exec_jobs WHERE status = 'done' AND finished_at < ?", (t - KEEP_DONE_SEC,))
    conn.execute("DELETE FROM exec_cache WHERE created_at < ?", (t - CACHE_TTL,))
    conn.execute("DELETE FROM exec_workers WHERE seen < ?", (t - 3600,))


def workers_alive(conn: sqlite3.Connection) -> int:
    return conn.execute("SELECT COUNT(*) FROM exec_workers WHERE seen > ?", (time.time() - WORKER_ALIVE_SEC,)).fetchone()[0]


def status(conn: sqlite3.Connection) -> dict:
    count = lambda s: conn.execute("SELECT COUNT(*) FROM exec_jobs WHERE status = ?", (s,)).fetchone()[0]  # noqa: E731
    return {"queued": count("queued"), "running": count("running"), "workers": workers_alive(conn)}
