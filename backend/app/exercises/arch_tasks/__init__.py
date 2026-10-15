"""Упражнения книги «Архитектура компьютера» (book 14), ключ — номер главы.

Это не код на Python: упражнения интерактивные — сборка схем из вентилей, ассемблер,
RISC-V (лаборатория `frontend/src/lab`), и проверяются в браузере. Здесь — только
манифест `lab_manifest.json` (id, название и условие каждого упражнения): по нему
считается прогресс и принимаются статусы решённых упражнений. Манифест строится
скриптом `frontend/scripts/lab-manifest.mjs` из данных лаборатории.
"""

import json
from pathlib import Path

_MANIFEST = Path(__file__).with_name("lab_manifest.json")

ARCH_TASKS: dict[int, list[dict]] = (
    {int(ch): items for ch, items in json.loads(_MANIFEST.read_text(encoding="utf-8")).items()}
    if _MANIFEST.exists()
    else {}
)
