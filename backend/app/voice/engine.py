"""Local Russian TTS engine: kokoro-ru (Kokoro-82M fine-tune) on CPU.

Lazy singleton: the model (~330MB in RAM, ~2.4GB peak) loads on first use.
Dima uses a separate checkpoint, so switching to/from him reloads the model.
"""

import importlib.util
import re
import threading

import numpy as np
import soundfile as sf
import torch

from app import config

MODEL_DIR = config.KOKORO_MODEL_DIR
AUDIO_DIR = config.AUDIO_DIR

SAMPLE_RATE = 24000
MAX_IPA = 480  # Kokoro style packs are indexed up to 510; stay safe
MAX_CHARS = 360  # IPA runs ~1.3x the Russian char count
PARA_PAUSE_S = 0.4  # silence inserted between paragraphs

VOICES = ("sveta", "masha", "dima")
VOICE_CHECKPOINT = {
    "sveta": "kokoro-ru-v2-base.pth",
    "masha": "kokoro-ru-v2-base.pth",
    "dima": "kokoro-ru-v2-dima.pth",
}

_SENTENCE_RE = re.compile(r"[^.!?\n…;]+[.!?\n…;]*")

_engine = None
_engine_lock = threading.Lock()


class _Engine:
    def __init__(self):
        spec = importlib.util.spec_from_file_location("ru_g2p", MODEL_DIR / "ru_g2p.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.g2p = module.RuG2P()

        from kokoro import KModel

        self.kmodel_cls = KModel
        self.checkpoint = None
        self.model = None
        self.packs: dict[str, torch.Tensor] = {}

    def _ensure_model(self, voice: str):
        ckpt = VOICE_CHECKPOINT[voice]
        if self.model is None or ckpt != self.checkpoint:
            print(f"[tts] loading {ckpt} ...")
            self.model = self.kmodel_cls(
                repo_id="zaakirio/kokoro-ru",
                model=str(MODEL_DIR / ckpt),
            ).eval()
            self.checkpoint = ckpt
        if voice not in self.packs:
            self.packs[voice] = torch.load(
                MODEL_DIR / "voices" / f"{voice}.pt",
                map_location="cpu",
                weights_only=False,
            )

    def synth(self, text: str, voice: str = "sveta") -> np.ndarray:
        self._ensure_model(voice)
        pack = self.packs[voice]

        parts = []
        for para in self._paragraphs(text):
            if parts:
                parts.append(np.zeros(int(SAMPLE_RATE * PARA_PAUSE_S)))
            for chunk in self._chunks(para):
                ipa, _oov = self.g2p(chunk)
                if not ipa:
                    continue
                style = pack[min(len(ipa) - 1, 509)]
                with torch.no_grad():
                    audio = self.model(ipa, style, 1.0, return_output=True).audio
                parts.append(audio.float().cpu().numpy())
        if not parts:
            raise ValueError("nothing synthesized")
        return np.concatenate(parts)

    def _paragraphs(self, text: str) -> list[str]:
        return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    def _chunks(self, text: str) -> list[str]:
        """Split into sentence-ish pieces whose IPA won't exceed MAX_IPA."""
        sentences = [s.strip() for s in _SENTENCE_RE.findall(text) if s.strip()]
        chunks, buf = [], ""
        for s in sentences:
            candidate = f"{buf} {s}".strip()
            # IPA is roughly 1.0-1.3x the char count for Russian; cap conservatively
            if len(candidate) > MAX_CHARS and buf:
                chunks.append(buf)
                buf = s
            else:
                buf = candidate
        if buf:
            chunks.append(buf)
        return chunks


def get_engine() -> _Engine:
    global _engine
    if _engine is None:
        with _engine_lock:
            if _engine is None:
                _engine = _Engine()
    return _engine


def synthesize_to_wav(text: str, voice: str, out_path) -> float:
    """Generate audio for text and write a wav file. Returns duration in seconds."""
    if voice not in VOICES:
        raise ValueError(f"unknown voice '{voice}'")
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    audio = get_engine().synth(text, voice)
    sf.write(str(out_path), audio, SAMPLE_RATE)
    return len(audio) / SAMPLE_RATE
