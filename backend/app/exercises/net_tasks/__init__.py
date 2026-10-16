"""Упражнения книги «Компьютерные сети» (book 15), ключ — номер главы.

Это не код на Python: упражнения интерактивные — симулятор сети в браузере
(`frontend/src/netlab`): ученик соединяет устройства кабелями, настраивает адреса, маски,
шлюзы, маршруты, NAT и файрвол, запускает ping и traceroute; цели сценария проверяются в
браузере. Здесь — только манифест `lab_manifest.json` (id, название и условие каждого
упражнения): по нему считается прогресс и принимаются статусы решённых упражнений.
Манифест строится скриптом `frontend/scripts/net-manifest.mjs` из данных симулятора.
Главы 9 («Сокеты в программе») и 14 («Веб-API») — код на Python: сокеты работают через loopback внутри песочницы.
"""

import json
from pathlib import Path

from app.exercises.net_tasks import ch09, ch14

_MANIFEST = Path(__file__).with_name("lab_manifest.json")

NET_TASKS: dict[int, list[dict]] = (
    {int(ch): items for ch, items in json.loads(_MANIFEST.read_text(encoding="utf-8")).items()}
    if _MANIFEST.exists()
    else {}
)
# Главы 9 и 14 — настоящий код на Python (песочница Docker, loopback-сокеты), а не лаборатория.
NET_TASKS.update(ch09.TASKS)
NET_TASKS.update(ch14.TASKS)
