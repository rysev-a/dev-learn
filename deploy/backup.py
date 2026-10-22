"""Ежедневная копия SQLite (онлайн-копия через sqlite3 backup API) в каталог /backups; хранятся последние KEEP копий."""

import os
import sqlite3
import time
from datetime import datetime
from pathlib import Path

DB = Path(os.environ.get("SAY_DB", "/data/say.db"))
OUT = Path(os.environ.get("SAY_BACKUP_DIR", "/backups"))
EVERY = int(os.environ.get("SAY_BACKUP_EVERY", "86400"))
KEEP = int(os.environ.get("SAY_BACKUP_KEEP", "14"))


def backup() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not DB.exists():
        print("база ещё не создана, пропускаю", flush=True)
        return
    dest = OUT / f"say-{datetime.now():%Y%m%d-%H%M%S}.db"
    src = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=30)
    dst = sqlite3.connect(dest)
    with dst:
        src.backup(dst)
    src.close()
    dst.close()
    for old in sorted(OUT.glob("say-*.db"))[:-KEEP]:
        old.unlink()
    print(f"копия: {dest} ({dest.stat().st_size // 1024} КБ)", flush=True)


if __name__ == "__main__":
    time.sleep(60)
    while True:
        try:
            backup()
        except Exception as e:  # noqa: BLE001 — копия не должна ронять контейнер
            print(f"ошибка копии: {e}", flush=True)
        time.sleep(EVERY)
