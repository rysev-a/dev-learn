-- Метаданные книг: порядок в меню, короткое имя, каталог слайдов во фронтенде, иконка и префикс id аудио.
-- Источник правды — этот файл: сервер применяет его при запуске и при `uv run seed_textbook.py`, вручную —
-- `sqlite3 say.db < app/data/sql/books.sql`. Новая книга = строка здесь (+ учебник, слайды, квизы, задачи).
-- Порядок книг (ord) — по плану курса: дискретная математика, Python, алгоритмы, архитектура компьютера,
-- C, операционные системы, сети, виртуализация, базы данных, Rust, JavaScript.
-- icon — имя иконки в frontend/src/components/BookIcon.tsx; slides_dir — каталог в frontend/src/slides;
-- audio_prefix — префикс для uuid5 id частей урока (меняя его, вы пересоздаёте всё аудио книги).
CREATE TABLE IF NOT EXISTS books (
    id           INTEGER PRIMARY KEY,
    title        TEXT NOT NULL,
    ord          INTEGER NOT NULL,
    slug         TEXT,
    slides_dir   TEXT,
    icon         TEXT,
    audio_prefix TEXT
);
INSERT INTO books (id, slug, title, ord, slides_dir, icon, audio_prefix) VALUES
    (12, 'dm',    'Дискретная математика',        0, 'dm',             'sigma',    'dm-ch'),
    (13, 'py',    'Python как первый язык',       1, 'py',             'python',   'learn-py-ch'),
    (7,  'algo',  'Алгоритмы и структуры данных', 2, 'algo',           'tree',     'algx-ch'),
    (14, 'arch',  'Архитектура компьютера',       3, 'arch',           'chip',     'arch-ch'),
    (16, 'c',     'От assembler к языку C',       4, 'learn-c',        'brackets', 'c-ch'),
    (8,  'linux', 'Погружаемся в Unix',           5, 'linux',          'terminal', 'lin-ch'),
    (15, 'net',   'Компьютерные сети',            6, 'networks',       'network',  'net-ch'),
    (17, 'virt',  'Виртуализация',                7, 'virtualization', 'nested',   'virt-ch'),
    (9,  'db',    'Базы данных',                  8, 'db',             'database', 'dbx-ch'),
    (10, 'rust',  'Изучаем Rust',                 9, 'learn-rust',     'rust',     'rust-ch'),
    (11, 'js',    'Современный Frontend',        10, 'js',             'js',       'js-ch'),
    (18, 'sd',    'Системный дизайн',            11, 'system-design',  'layers',   'sd-ch')
ON CONFLICT (id) DO UPDATE SET
    title = excluded.title, ord = excluded.ord, slug = excluded.slug,
    slides_dir = excluded.slides_dir, icon = excluded.icon, audio_prefix = excluded.audio_prefix;
