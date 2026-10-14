# AGENTS.md — правила проекта «say»

Аудиокурс: FastAPI + SQLite (`backend/`, приложение `backend/app/`), React+Vite
фронт (`frontend/`), TTS kokoro-ru (`backend/app/voice/`), контент в
`backend/app/data/textbook/<id>-<slug>/*.md`, аудио в `backend/app/data/audio/`.

## Структура backend

- `backend/app/main.py` — FastAPI-приложение, подключает роутеры.
- `backend/app/config.py` — все пути (данные, аудио, БД, модели).
- `backend/app/books/` — всё по книгам: `router.py` (API курса),
  `service.py` (БД, аудио-файлы), `seed.py` (парсинг учебников + сид).
- `backend/app/voice/` — всё по озвучке: `engine.py` (kokoro-ru),
  `download_model.py`, `models/` (чекпоинты).
- `backend/app/exercises/` — проверка кода в Docker-песочнице: `tasks.py`
  (определения задач, пока только «Изучаем Python», book 13), `runner.py`
  (запуск в `python:3.13-slim`: без сети, лимиты памяти/CPU/процессов,
  таймаут), `router.py` (`GET /api/exercises/{book}/{chapter}`,
  `POST /api/exercises/run`). Тесты остаются на бэкенде, клиенту отдаются
  только условие, заготовка и подсказка.
- `backend/app/data/` — книги в текстовом виде (`textbook/`), аудио (`audio/`),
  база (`say.db`).
- Запуск backend: `cd backend && uv run uvicorn app.main:app` (порт 8000).

## Контент: новые книги

**Новые книги добавляются только со слайдами.** Для книги обязательно:

1. Учебник в `backend/app/data/textbook/<id>-<slug>/<slug>-NN.md` (формат:
   `#BOOK`, `#SECTION`, `#CHAPTER N | Название`, текст урока одной строкой,
   абзацы — литеральными `\n\n`).
2. Слайды для КАЖДОЙ главы в `frontend/src/slides/<slug>/chNN.jsx`
   (формат — самодостаточный файл по образцу `frontend/src/slides/algo/ch01.jsx`;
   экспорт `SLIDES_<Xn> = { "<bookId>:<N>": [...] }` + `SLIDE_TITLES_<Xn>`;
   число сцен = числу абзацев урока). Подключить в `frontend/src/lib/slides.js`.
3. Квизы на теорию для каждой главы в `frontend/src/quizzes/<slug>.js`
   (`kind: "theory"`, 5 вопросов), подключить в `frontend/src/lib/quizzes.js`.
4. Регистрация книги в `backend/app/books/seed.py` (BOOKS, AUDIO_PREFIX, при
   необходимости SPLIT_CHAPTERS) и сид: `cd backend && uv run seed_textbook.py`
   (флаги: `--no-audio` — только БД, `--audio-only` — только аудио).

## Упражнения: что есть

- Квизы (`frontend/src/quizzes/`) — только теория, `kind: "theory"`.
- Упражнения с вводом ответа — «Дискретная математика»
  (`frontend/src/exercises/dm.js`, реестр `lib/exercises.js`, ключ
  `"<bookId>:<N>"`, компонент `Exercises.jsx`). Проверка в браузере —
  сравнением с эталонами (`answers`), без запуска кода.
- Упражнения с кодом — «Изучаем Python» (компонент `CodeExercises.jsx`):
  простая `textarea`, проверка **только на сервере** в Docker-песочнице
  (`backend/app/exercises/`); решённые задачи помечаются в `localStorage`.
  Нужен запущенный Docker и образ `python:3.13-slim`.

## Что убрано и не возвращать

- Отображение текста урока в интерфейсе — только слайды и аудио.
- Проверка кода в браузере: чекеры, CodeMirror, Pyodide, web-tree-sitter
  удалены из зависимостей и из `frontend/public/`. Код проверяется только
  через Docker-песочницу (`app/exercises/`).
- Код-квизы: квизы только на теорию.

## Прочее

- Слайд-файлы не должны импортировать ничего (самодостаточные) и не должны
  вводить новые CSS-классы — только существующие из `frontend/src/App.css`.
- Сборка фронта: `cd frontend && npm run build`.
- `tasks/` — исходные планы курсов (algo, arch_oc, db_learn), не код.
  `experiments/` — пробы произношения для TTS; wav и логи не коммитим.
- Python-код держим в `backend/`; пути считать от файлов пакета
  (`app/config.py`), не от CWD.
