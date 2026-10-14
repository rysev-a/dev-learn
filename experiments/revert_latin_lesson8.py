"""Откат латинизации урока 12-linux-01.md к транслиту (эксперимент признан
неудачным на слух). Обратные пары к latinize_lesson8.py.

Контент-фикс сохранён: «слэш мэдиа» вместо ошибочного «слэш ю-эф-эр».

Запуск: uv run python experiments/revert_latin_lesson8.py
"""

import re
from pathlib import Path

F = Path(__file__).parent.parent / "textbook" / "8-linux" / "12-linux-01.md"

# (старое, новое, ожидаемое число замен); сначала контекстные, потом одиночные
REVERTS = [
    ("а /etc/fstab делает это постоянным", "а еф-стаб делает это постоянным", 1),
    ("в файл настроек /etc/fstab", "в файл настроек ет-си эф-стаб", 1),
    ("в /etc, /var/log и /proc", "в ет-си, вар лог и проц", 1),
    (
        "где /etc — настройки, /var — растущее, а /proc, /sys и /dev — окна",
        "где ет-си — настройки, вар — растущее, а проц, сис и дев — окна",
        1,
    ),
    ("/usr/bin", "слэш ю-эф-эр слэш бин", 1),
    ("/media — подключаемые флешки", "слэш мэдиа — подключаемые флешки", 1),
    ("/proc — окно", "Слэш проц — окно", 1),
    ("/sys — окно", "Слэш сис — окно", 1),
    ("/dev — файлы устройств", "Слэш дев — файлы устройств", 1),
    ("/etc", "слэш ет-си", 1),
    ("/var", "слэш вар", 1),
    ("/home", "слэш хоум", 1),
    ("/root", "слэш рут", 1),
    ("/tmp", "слэш темп", 1),
    ("/bin", "слэш бин", 1),
    ("/lib", "слэш либ", 1),
    ("командой du", "командой дэ-ю", 1),
    ("командой df", "командой дэ-эф", 1),
]


def main() -> None:
    t = F.read_text()
    for old, new, expected in REVERTS:
        n = t.count(old)
        if n != expected:
            raise SystemExit(f"ОШИБКА: {old!r} найдено {n} раз, ожидалось {expected}")
        t = t.replace(old, new)
    # в тексте урока не должно остаться латиницы (литеральные \n — часть формата)
    content = "\n".join(line for line in t.splitlines() if not line.startswith("#"))
    content = content.replace("\\n", "")
    latin = re.findall(r"[A-Za-z]+", content)
    if latin:
        raise SystemExit(f"ОШИБКА: осталась латиница: {latin}")
    F.write_text(t)
    print(f"OK: {len(REVERTS)} обратных замен, латиницы в уроке нет")


if __name__ == "__main__":
    main()
