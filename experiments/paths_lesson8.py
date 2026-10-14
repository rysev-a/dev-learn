"""Эксперимент: транслит («слэш либ») vs латиница («/lib») в тексте урока.

G2P прогоняет латиницу через английский espeak — короткие пути совпадают
с русским произношением, длинные ломаются. Слушаем и решаем.

Запуск:  uv run python experiments/paths_lesson8.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tts import synthesize_to_wav

OUT = Path(__file__).parent
VOICE = "sveta"

CLIPS: list[tuple[str, str]] = [
    # «счастливые» пути: английское чтение совпадает с русским
    ("01-lib-translit", "Системные библиотеки лежат в слэш либ."),
    ("02-lib-latin", "Системные библиотеки лежат в /lib."),
    ("03-dev-translit", "Файлы устройств живут в слэш дев."),
    ("04-dev-latin", "Файлы устройств живут в /dev."),
    ("05-proc-translit", "Ядро показывает процессы в слэш прок."),
    ("06-proc-latin", "Ядро показывает процессы в /proc."),
    # «сломанные» пути
    ("07-etc-translit", "Конфигурация всей системы живёт в слэш ет-си."),
    ("08-etc-latin", "Конфигурация всей системы живёт в /etc."),
    ("09-varlog-translit", "Логи растут в слэш вар слэш лог."),
    ("10-varlog-latin", "Логи растут в /var/log."),
    ("11-usrbin-translit", "Исполняемые программы — в слэш ю-эс-эр слэш бин."),
    ("12-usrbin-latin", "Исполняемые программы — в /usr/bin."),
    ("13-tmp-translit", "Временные файлы — в слэш темп."),
    ("14-tmp-latin", "Временные файлы — в /tmp."),
    ("15-mnt-translit", "Флешки появляются в слэш эм-эн-ти."),
    ("16-mnt-latin", "Флешки появляются в /mnt."),
    # ped. вопрос: слышит ли ученик структуру дерева без слова «слэш»
    ("17-tree-translit", "Слэш ет-си, слэш вар, слэш хоум — ветки одного корня."),
    ("18-tree-latin", "/etc, /var, /home — ветки одного корня."),
]


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name, text in CLIPS:
        dur = synthesize_to_wav(text, VOICE, OUT / f"{name}.wav")
        print(f"{name}.wav  {dur:4.1f}s")
    print("\nСравнить парами (транслит -> латиница):")
    for i in range(1, len(CLIPS), 2):
        a, b = CLIPS[i - 1][0], CLIPS[i][0]
        print(f"  afplay experiments/{a}.wav && afplay experiments/{b}.wav")


if __name__ == "__main__":
    main()
