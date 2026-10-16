"""Центральные пути приложения — всё считается от файлов пакета, не от CWD."""

import os
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent

# backend/app/data — книги, аудио, база
DATA_DIR = APP_DIR / "data"
TEXTBOOK_DIR = DATA_DIR / "textbook"
AUDIO_DIR = DATA_DIR / "audio"
# SQL для начального заполнения БД: упражнения (см. app/exercises/store.py)
TASKS_SQL_DIR = DATA_DIR / "sql" / "tasks"
QUIZZES_SQL_DIR = DATA_DIR / "sql" / "quizzes"
ANSWERS_SQL_DIR = DATA_DIR / "sql" / "answers"
# SAY_DB — другая база (тесты, проверка на копии), по умолчанию рабочая say.db
DB_PATH = Path(os.environ.get("SAY_DB") or DATA_DIR / "say.db")

# backend/app/voice/models — чекпоинты kokoro-ru
VOICE_MODELS_DIR = APP_DIR / "voice" / "models"
KOKORO_MODEL_DIR = VOICE_MODELS_DIR / "kokoro-ru"
