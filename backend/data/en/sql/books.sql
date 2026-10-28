-- Titles of the books available in English. A book is listed here only when it is translated completely
-- (textbook, slides, quiz and exercises); the other books are shown in Russian.
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
    (12, 'dm', 'Discrete Mathematics', 0, 'dm', 'sigma', 'dm-ch'),
    (13, 'py', 'Python as a First Language', 1, 'py', 'python', 'learn-py-ch'),
    (14, 'arch', 'Computer Architecture', 3, 'arch', 'chip', 'arch-ch'),
    (15, 'net', 'Computer Networks', 6, 'networks', 'network', 'net-ch'),
    (17, 'virt', 'Virtualization', 7, 'virtualization', 'nested', 'virt-ch'),
    (11, 'js', 'Modern Frontend', 10, 'js', 'js', 'js-ch'),
    (18, 'sd', 'System Design', 11, 'system-design', 'layers', 'sd-ch');
