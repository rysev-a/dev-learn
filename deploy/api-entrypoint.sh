#!/bin/sh
# Сид содержимого курса (книги, главы, задачи, квизы) и запуск API. Прогресс пользователей сид не трогает.
set -e
if [ "${SAY_SEED:-1}" = "1" ]; then
  python seed_textbook.py --no-audio
fi
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips='*'
