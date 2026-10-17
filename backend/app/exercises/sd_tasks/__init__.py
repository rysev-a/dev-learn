"""Упражнения книги «Системный дизайн» (book 18), ключ — номер главы.

Это не код на Python: упражнения интерактивные — схема высоконагруженного сервиса в браузере
(`frontend/src/sdlab`): ученик собирает её из компонентов (CDN, балансировщик, серверы, кэш,
очереди, базы), а модель считает загрузку, задержку, доступность и стоимость под заданной нагрузкой;
цели проверяются в браузере. Здесь — только манифест `lab_manifest.json` (id, название и условие
каждого упражнения): по нему считается прогресс и принимаются статусы решённых упражнений.
Манифест строится скриптом `frontend/scripts/sd-manifest.mjs` из данных лаборатории.
"""

import json
from pathlib import Path

_MANIFEST = Path(__file__).with_name("lab_manifest.json")

SD_TASKS: dict[int, list[dict]] = (
    {int(ch): items for ch, items in json.loads(_MANIFEST.read_text(encoding="utf-8")).items()}
    if _MANIFEST.exists()
    else {}
)
