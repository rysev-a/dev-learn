"""CLI-утилита сида курса. Логика — в app.books.seed.

uv run seed_textbook.py                # БД + недостающее аудио
uv run seed_textbook.py --no-audio     # только перестроить БД
uv run seed_textbook.py --audio-only   # только догенерировать аудио
"""

from app.books.seed import main

if __name__ == "__main__":
    main()
