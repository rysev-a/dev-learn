"""Собирает пары из paths_lesson8.py в один файл experiments/tour.wav
с голосовыми метками: «Пара 1: слэш либ. Транслит. … Латиница. …»

Запуск: uv run python experiments/make_tour.py
Слушать: afplay experiments/tour.wav
"""

import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tts import synthesize_to_wav

OUT = Path(__file__).parent
VOICE = "sveta"

PAIRS = [
    ("01-lib-translit", "02-lib-latin", "слэш либ"),
    ("03-dev-translit", "04-dev-latin", "слэш дев"),
    ("05-proc-translit", "06-proc-latin", "слэш прок"),
    ("07-etc-translit", "08-etc-latin", "слэш ет-си"),
    ("09-varlog-translit", "10-varlog-latin", "слэш вар слэш лог"),
    ("11-usrbin-translit", "12-usrbin-latin", "слэш ю-эс-эр слэш бин"),
    ("13-tmp-translit", "14-tmp-latin", "слэш темп"),
    ("15-mnt-translit", "16-mnt-latin", "слэш эм-эн-ти"),
    ("17-tree-translit", "18-tree-latin", "структура дерева"),
]

GAP_S = 0.5


def read_wav(path: Path) -> wave.Wave_read:
    return wave.open(str(path), "rb")


def main() -> None:
    labels: dict[str, Path] = {}
    spoken = {
        "Транслит:": "lab-translit",
        "Латиница:": "lab-latin",
    }
    for text, name in spoken.items():
        p = OUT / f"_{name}.wav"
        synthesize_to_wav(text, VOICE, p)
        labels[text] = p
    for i, (_, _, term) in enumerate(PAIRS, 1):
        p = OUT / f"_lab-pair{i}.wav"
        synthesize_to_wav(f"Пара {i}: {term}.", VOICE, p)
        labels[f"pair{i}"] = p

    out_path = OUT / "tour.wav"
    params = None
    with wave.open(str(out_path), "wb") as wout:

        def add(path: Path) -> None:
            nonlocal params
            with read_wav(path) as win:
                cur = (win.getnchannels(), win.getsampwidth(), win.getframerate())
                if params is None:
                    params = cur
                    wout.setnchannels(cur[0])
                    wout.setsampwidth(cur[1])
                    wout.setframerate(cur[2])
                wout.writeframes(win.readframes(win.getnframes()))

        def gap() -> None:
            silence = b"\x00" * int(params[2] * GAP_S) * params[0] * params[1]
            wout.writeframes(silence)

        for i, (a, b, _) in enumerate(PAIRS, 1):
            add(labels[f"pair{i}"])
            gap()
            add(labels["Транслит:"])
            gap()
            add(OUT / f"{a}.wav")
            gap()
            add(labels["Латиница:"])
            gap()
            add(OUT / f"{b}.wav")
            gap()

    w = read_wav(out_path)
    print(f"tour.wav готов: {w.getnframes() / w.getframerate():.0f} сек")
    print("Слушать:  afplay experiments/tour.wav")


if __name__ == "__main__":
    main()
