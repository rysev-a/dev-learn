"""Локальный воркер: потоки внутри процесса API берут задания из очереди (jobs.claim) и запускают их в песочнице.
Тот же путь, что у внешнего воркера (backend/worker.py), только без сети."""

import threading

from app import config
from app.books.service import db
from app.exercises import jobs, runner, store


def parse_slots(spec: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for part in spec.split(","):
        lane, _, n = part.partition(":")
        if lane.strip() in jobs.LANES and n.strip().isdigit():
            out[lane.strip()] = int(n)
    return out


class LocalWorkers:
    def __init__(self, slots: dict[str, int]):
        self.slots = slots
        self.name = "local"
        self._stop = threading.Event()
        self._threads: list[threading.Thread] = []
        self._busy: set[str] = set()
        self._lock = threading.Lock()

    def start(self) -> None:
        runner.remove_stale_containers()
        for lane, n in self.slots.items():
            for i in range(n):
                t = threading.Thread(target=self._loop, args=(lane,), name=f"say-worker-{lane}-{i}", daemon=True)
                t.start()
                self._threads.append(t)
        t = threading.Thread(target=self._beat, name="say-worker-beat", daemon=True)
        t.start()
        self._threads.append(t)

    def stop(self) -> None:
        self._stop.set()
        for t in self._threads:
            t.join(timeout=2)

    def _beat(self) -> None:
        while not self._stop.is_set():
            with self._lock:
                busy = list(self._busy)
            try:
                with db() as conn:
                    jobs.ping(conn, self.name, list(self.slots), sum(self.slots.values()), busy)
            except Exception:  # noqa: BLE001 — сердцебиение не должно падать из-за временной ошибки базы
                pass
            self._stop.wait(5)

    def _loop(self, lane: str) -> None:
        while not self._stop.is_set():
            try:
                with db() as conn:
                    job = jobs.claim(conn, self.name, [lane])
            except Exception:  # noqa: BLE001
                job = None
            if job is None:
                self._stop.wait(0.3)
                continue
            with self._lock:
                self._busy.add(job["id"])
            try:
                result = runner.run_task(store._dec(job["task"]), job["code"])
            except Exception as e:  # noqa: BLE001 — ошибка раннера не должна оставлять задание «висеть»
                result = {"status": "error", "results": [], "stdout": "", "stderr": f"Ошибка проверяющего сервера: {e}"}
            finally:
                with self._lock:
                    self._busy.discard(job["id"])
            with db() as conn:
                jobs.complete(conn, job["id"], self.name, result)


def start_local() -> LocalWorkers | None:
    if config.RUNNER_MODE != "local":
        return None
    w = LocalWorkers(parse_slots(config.LOCAL_SLOTS))
    w.start()
    return w

