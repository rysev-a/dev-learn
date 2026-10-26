"""Воркер проверки кода: забирает задания у основного сервера и запускает их в песочнице Docker.

Работает на отдельной машине (например, в VM на домашнем сервере). Ему нужен только исходящий HTTPS до основного
сервера: ни открытых портов, ни доступа к базе. Только стандартная библиотека Python и Docker с образами
(python:3.13-slim, rust:1.97-slim, node:22-alpine, say-rust-crates:1).

    SAY_WORKER_TOKEN=… uv run worker.py --server https://say.example.com --name home-1 --light 4 --heavy 2

На основном сервере: SAY_RUNNER=remote и тот же SAY_WORKER_TOKEN. Сигнал остановки (Ctrl+C, SIGTERM) дожидается
выполняющихся проверок."""

import argparse
import json
import os
import signal
import sys
import threading
import time
import urllib.error
import urllib.request

import runner

PING_EVERY = 10
LANES_ORDER = ("light", "heavy")


def decode(o):
    """Кортежи в определении задачи приходят как {"__tuple__": [...]} (как в app/exercises/store.py)."""
    if isinstance(o, dict):
        if set(o) == {"__tuple__"}:
            return tuple(decode(x) for x in o["__tuple__"])
        return {k: decode(v) for k, v in o.items()}
    if isinstance(o, list):
        return [decode(x) for x in o]
    return o


class Server:
    def __init__(self, base: str, token: str):
        self.base = base.rstrip("/")
        self.token = token

    def post(self, path: str, body: dict, timeout: float = 15) -> tuple[int, dict | None]:
        req = urllib.request.Request(
            self.base + path,
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.token}"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read()
                return r.status, (json.loads(raw) if raw else None)
        except urllib.error.HTTPError as e:
            return e.code, None


class Worker:
    def __init__(self, server: Server, name: str, slots: dict[str, int]):
        self.server = server
        self.name = name
        self.slots = {k: v for k, v in slots.items() if v > 0}
        self.stop = threading.Event()
        self.busy: set[str] = set()
        self.lock = threading.Lock()

    def log(self, msg: str) -> None:
        print(time.strftime("%H:%M:%S"), msg, flush=True)

    def beat(self) -> None:
        while not self.stop.is_set():
            with self.lock:
                jobs = list(self.busy)
            try:
                self.server.post(
                    "/internal/worker/ping",
                    {"name": self.name, "lanes": list(self.slots), "slots": sum(self.slots.values()), "jobs": jobs},
                )
            except (OSError, ValueError) as e:
                self.log(f"сервер недоступен: {e}")
            self.stop.wait(PING_EVERY)

    def loop(self, lane: str) -> None:
        backoff = 1.0
        while not self.stop.is_set():
            try:
                code, job = self.server.post(
                    "/internal/worker/claim",
                    {"name": self.name, "lanes": [lane], "slots": sum(self.slots.values()), "wait": 20},
                    timeout=40,
                )
            except (OSError, ValueError) as e:
                self.log(f"claim: {e}")
                self.stop.wait(backoff)
                backoff = min(backoff * 2, 30)
                continue
            if code in (401, 404):
                self.log("сервер отклонил токен воркера (проверьте SAY_WORKER_TOKEN и SAY_RUNNER=remote на сервере)")
                self.stop.wait(30)
                continue
            if code != 200 or not job:
                backoff = 1.0 if code in (200, 204) else min(backoff * 2, 30)
                if code not in (200, 204):
                    self.stop.wait(backoff)
                continue
            backoff = 1.0
            self.run_job(job)

    def run_job(self, job: dict) -> None:
        jid = job["id"]
        with self.lock:
            self.busy.add(jid)
        t0 = time.time()
        try:
            result = runner.run_task(decode(job["task"]), job["code"])
        except Exception as e:  # noqa: BLE001 — ошибка раннера не должна оставлять задание без ответа
            result = {"status": "error", "results": [], "stdout": "", "stderr": f"Ошибка проверяющего сервера: {e}"}
        finally:
            with self.lock:
                self.busy.discard(jid)
        for attempt in range(5):
            try:
                code, _ = self.server.post(f"/internal/worker/jobs/{jid}/result", {"name": self.name, "result": result})
            except (OSError, ValueError) as e:
                self.log(f"результат {jid[:8]}: {e}")
                self.stop.wait(2 * (attempt + 1))
                continue
            if code == 409:
                self.log(f"результат {jid[:8]} не принят: аренда истекла")
            break
        self.log(f"{job['lane']:5} {jid[:8]} {result.get('status')} {time.time() - t0:.1f} с")

    def run(self) -> None:
        removed = runner.remove_stale_containers()
        self.log(f"воркер {self.name}: полосы {self.slots}, убрано старых контейнеров: {removed}")
        threads = [threading.Thread(target=self.beat, daemon=True)]
        for lane, n in self.slots.items():
            threads += [threading.Thread(target=self.loop, args=(lane,)) for _ in range(n)]
        for t in threads:
            t.start()
        try:
            while any(t.is_alive() for t in threads[1:]):
                time.sleep(0.5)
        except KeyboardInterrupt:
            self.stop.set()
        for t in threads[1:]:
            t.join()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--server", default=os.environ.get("SAY_SERVER", "http://127.0.0.1:8000"))
    ap.add_argument("--token", default=os.environ.get("SAY_WORKER_TOKEN", ""))
    ap.add_argument("--name", default=os.environ.get("SAY_WORKER_NAME", os.uname().nodename))
    ap.add_argument("--light", type=int, default=3, help="одновременных проверок python/js")
    ap.add_argument("--heavy", type=int, default=1, help="одновременных проверок rust/c")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Нужен токен: --token или SAY_WORKER_TOKEN")
    w = Worker(Server(a.server, a.token), a.name, {"light": a.light, "heavy": a.heavy})
    signal.signal(signal.SIGTERM, lambda *_: w.stop.set())
    w.run()


if __name__ == "__main__":
    main()
