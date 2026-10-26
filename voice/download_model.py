"""Download kokoro-ru model files into voice/models/kokoro-ru/ (one-time setup).

Run from voice/: uv run python download_model.py
"""

from pathlib import Path

from huggingface_hub import snapshot_download

REPO = "zaakirio/kokoro-ru"
DEST = str(Path(__file__).resolve().parent / "models" / "kokoro-ru")

path = snapshot_download(
    repo_id=REPO,
    local_dir=DEST,
    allow_patterns=[
        "config.json",
        "kokoro-config.json",
        "ru_g2p.py",
        "espeak-data/*",
        "kokoro-ru-v2-base.pth",
        "kokoro-ru-v2-dima.pth",
        "voices/sveta.pt",
        "voices/masha.pt",
        "voices/dima.pt",
    ],
)
print("downloaded to:", path)
