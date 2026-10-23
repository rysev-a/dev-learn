"""Выгрузка определений упражнений книги 17 из labs.py в tasks.json (вход бинаря `import`).

Запуск (из корня репозитория): python3 -I shared-rs/virtlab/data/export_labs.py
"""
import json
import pathlib

root = pathlib.Path(__file__).resolve().parents[3]
ns: dict = {}
exec((root / "backend/app/exercises/virt_tasks/labs.py").read_text(encoding="utf-8"), ns)
out = [
    {"chapter": ch, "id": t["id"], "title": t["title"], "statement": t["statement"], "hint": t["hint"]}
    for ch, tasks in sorted(ns["LAB_TASKS"].items())
    for t in tasks
]
(pathlib.Path(__file__).parent / "tasks.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"упражнений: {len(out)}")
