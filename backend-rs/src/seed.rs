//! Сид содержимого курса из тех же исходников, что и у Python-бэкенда: учебники (`textbook/**/*.md`) и SQL-файлы
//! (`sql/books.sql`, `sql/{tasks,quizzes,answers}`). SQL выполняется во временной SQLite в памяти, строки переносятся в
//! SurrealDB. Прогресс пользователей сид не трогает. Пересев — только если исходники изменились (хеш в `meta:seed`).

use std::path::{Path, PathBuf};

use anyhow::Context;
use rusqlite::Connection as Sqlite;
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use uuid::Uuid;

use crate::{config::Config, db::Db};

/// Фиксированное пространство имён для стабильных id уроков (то же, что в Python-бэкенде).
const NS: Uuid = Uuid::from_u128(0xd3a7c0de_0000_4000_8000_4b6f6b6f726f);

/// Таблицы содержимого в порядке записи: (имя таблицы, строки).
pub struct Content {
    pub tables: Vec<(&'static str, Vec<Value>)>,
    pub hash: String,
}

fn walk(dir: &Path, out: &mut Vec<PathBuf>) -> std::io::Result<()> {
    for entry in std::fs::read_dir(dir)? {
        let p = entry?.path();
        if p.is_dir() {
            walk(&p, out)?;
        } else if p.extension().is_some_and(|e| e == "md") {
            out.push(p);
        }
    }
    Ok(())
}

struct Chapter {
    num: i64,
    title: String,
    lessons: Vec<String>,
}
struct Section {
    title: String,
    chapters: Vec<Chapter>,
}
struct Book {
    id: i64,
    sections: Vec<Section>,
}

/// Разбор учебников: `#BOOK n`, `#SECTION название`, `#CHAPTER n | название`, затем строки текста урока.
fn parse_textbooks(dir: &Path) -> anyhow::Result<(Vec<Book>, Vec<u8>)> {
    let mut files = Vec::new();
    walk(dir, &mut files).with_context(|| format!("каталог учебников {}", dir.display()))?;
    files.sort();
    let mut books: Vec<Book> = Vec::new();
    let mut raw = Vec::new(); // содержимое для хеша
    let (mut book, mut section, mut chapter): (Option<usize>, Option<usize>, Option<usize>) = (None, None, None);
    for path in &files {
        let text = std::fs::read_to_string(path)?;
        raw.extend_from_slice(path.to_string_lossy().as_bytes());
        raw.extend_from_slice(text.as_bytes());
        for line in text.lines() {
            let line = line.trim();
            if line.is_empty() {
                continue;
            }
            if let Some(rest) = line.strip_prefix("#BOOK ") {
                let id: i64 = rest.trim().parse().with_context(|| format!("строка #BOOK в {}: {line}", path.display()))?;
                let idx = match books.iter().position(|b| b.id == id) {
                    Some(i) => i,
                    None => {
                        books.push(Book { id, sections: Vec::new() });
                        books.len() - 1
                    }
                };
                book = Some(idx);
                section = None;
                chapter = None;
            } else if let Some(rest) = line.strip_prefix("#SECTION ") {
                let bi = match book {
                    Some(i) => i,
                    None => {
                        let i = match books.iter().position(|b| b.id == 1) {
                            Some(i) => i,
                            None => {
                                books.push(Book { id: 1, sections: Vec::new() });
                                books.len() - 1
                            }
                        };
                        book = Some(i);
                        i
                    }
                };
                books[bi].sections.push(Section { title: rest.trim().to_string(), chapters: Vec::new() });
                section = Some(books[bi].sections.len() - 1);
                chapter = None;
            } else if let Some(rest) = line.strip_prefix("#CHAPTER ") {
                let (num, title) = rest.split_once('|').with_context(|| format!("строка #CHAPTER в {}: {line}", path.display()))?;
                let num: i64 = num.trim().parse().with_context(|| format!("номер главы в {}: {line}", path.display()))?;
                let (Some(bi), Some(si)) = (book, section) else {
                    anyhow::bail!("глава вне раздела в {}: {line}", path.display());
                };
                books[bi].sections[si].chapters.push(Chapter { num, title: title.trim().to_string(), lessons: Vec::new() });
                chapter = Some(books[bi].sections[si].chapters.len() - 1);
            } else {
                let (Some(bi), Some(si), Some(ci)) = (book, section, chapter) else {
                    anyhow::bail!("урок вне главы в {}: {}", path.display(), line.chars().take(60).collect::<String>());
                };
                // литеральное \n в исходнике — граница абзацев
                books[bi].sections[si].chapters[ci].lessons.push(line.replace("\\n", "\n"));
            }
        }
    }
    // файлы глав самодостаточны и повторяют #SECTION: подряд идущие одинаковые разделы склеиваем
    for b in &mut books {
        let mut merged: Vec<Section> = Vec::new();
        for s in std::mem::take(&mut b.sections) {
            match merged.last_mut() {
                Some(last) if last.title == s.title => last.chapters.extend(s.chapters),
                _ => merged.push(s),
            }
        }
        b.sections = merged;
    }
    books.sort_by_key(|b| b.id);
    // каждый абзац урока — отдельная часть (слайд)
    for b in &mut books {
        for s in &mut b.sections {
            for c in &mut s.chapters {
                if c.lessons.len() == 1 {
                    c.lessons = c.lessons[0].split("\n\n").map(str::trim).filter(|p| !p.is_empty()).map(String::from).collect();
                }
            }
        }
    }
    Ok((books, raw))
}

fn sql_files(dir: &Path) -> anyhow::Result<Vec<PathBuf>> {
    let mut files: Vec<PathBuf> = std::fs::read_dir(dir)
        .with_context(|| format!("каталог SQL {}", dir.display()))?
        .filter_map(|e| e.ok().map(|e| e.path()))
        .filter(|p| p.extension().is_some_and(|e| e == "sql"))
        .collect();
    files.sort();
    Ok(files)
}

fn run_sql(lite: &Sqlite, files: &[PathBuf], raw: &mut Vec<u8>) -> anyhow::Result<()> {
    for f in files {
        let text = std::fs::read_to_string(f)?;
        raw.extend_from_slice(text.as_bytes());
        lite.execute_batch(&text).with_context(|| format!("SQL-файл {}", f.display()))?;
    }
    Ok(())
}

fn col_text(r: &rusqlite::Row, i: usize) -> rusqlite::Result<Value> {
    Ok(match r.get::<_, Option<String>>(i)? {
        Some(s) => Value::String(s),
        None => Value::Null,
    })
}

/// Слайды глав из файлов данных: глава проверяется (все сцены компилируются), затем раскладывается на строки
/// `slide_chapters` (рубрика и число слайдов) и `slides` (по строке на слайд; тело — блоки документом).
fn load_slides(dir: &Path, raw: &mut Vec<u8>) -> anyhow::Result<(Vec<Value>, Vec<Value>)> {
    let (mut chapters, mut slides) = (Vec::new(), Vec::new());
    if !dir.is_dir() {
        return Ok((chapters, slides));
    }
    let mut files: Vec<PathBuf> = std::fs::read_dir(dir)?.filter_map(Result::ok).map(|e| e.path()).filter(|p| p.extension().is_some_and(|e| e == "json")).collect();
    files.sort();
    for f in files {
        let bytes = std::fs::read(&f)?;
        raw.extend_from_slice(f.file_name().and_then(|n| n.to_str()).unwrap_or("").as_bytes());
        raw.extend_from_slice(&bytes);
        let ch: content::Chapter = serde_json::from_slice(&bytes).with_context(|| format!("слайды {}", f.display()))?;
        ch.check().map_err(|e| anyhow::anyhow!("{}: {e}", f.display()))?;
        chapters.push(json!({ "book": ch.book, "chapter": ch.chapter, "rubric": ch.rubric, "slides": ch.slides.len() }));
        for (idx, s) in ch.slides.iter().enumerate() {
            slides.push(json!({
                "book": ch.book, "chapter": ch.chapter, "idx": idx, "title": s.title, "sub": s.sub, "short": s.short, "main": s.main,
                "body": serde_json::to_value(&s.body)?,
            }));
        }
    }
    Ok((chapters, slides))
}

/// Читает исходники и собирает строки всех таблиц содержимого. Блокирующая работа (файлы, SQLite).
pub fn load(cfg: &Config) -> anyhow::Result<Content> {
    let (books, mut raw) = parse_textbooks(&cfg.textbook_dir())?;
    let sql = cfg.sql_dir();
    let lite = Sqlite::open_in_memory()?;

    let books_sql = sql.join("books.sql");
    run_sql(&lite, &[books_sql], &mut raw)?;
    for dir in ["tasks", "quizzes", "answers"] {
        run_sql(&lite, &sql_files(&sql.join(dir))?, &mut raw)?;
    }

    let mut meta_books: Vec<(i64, Value)> = Vec::new();
    {
        let mut st = lite.prepare("SELECT id, title, ord, slug, slides_dir, icon, audio_prefix FROM books ORDER BY ord")?;
        let rows = st.query_map([], |r| {
            Ok((
                r.get::<_, i64>(0)?,
                json!({
                    "bid": r.get::<_, i64>(0)?, "title": r.get::<_, String>(1)?, "ord": r.get::<_, i64>(2)?,
                    "slug": col_text(r, 3)?, "slides_dir": col_text(r, 4)?, "icon": col_text(r, 5)?, "audio_prefix": col_text(r, 6)?,
                }),
            ))
        })?;
        for r in rows {
            meta_books.push(r?);
        }
    }
    let prefix_of = |bid: i64| -> String {
        meta_books
            .iter()
            .find(|(id, _)| *id == bid)
            .and_then(|(_, v)| v.get("audio_prefix").and_then(Value::as_str).filter(|s| !s.is_empty()).map(String::from))
            .unwrap_or_else(|| format!("b{bid}-ch"))
    };

    let (mut sections, mut chapters, mut lessons) = (Vec::new(), Vec::new(), Vec::new());
    let (mut sid, mut cid) = (0i64, 0i64);
    for b in &books {
        let prefix = prefix_of(b.id);
        for (s_ord, s) in b.sections.iter().enumerate() {
            sid += 1;
            sections.push(json!({ "sid": sid, "bid": b.id, "title": s.title, "ord": s_ord }));
            for c in &s.chapters {
                cid += 1;
                chapters.push(json!({ "cid": cid, "sid": sid, "bid": b.id, "num": c.num, "title": c.title }));
                for (l_ord, text) in c.lessons.iter().enumerate() {
                    let lid = Uuid::new_v5(&NS, format!("{prefix}{}-l{l_ord}", c.num).as_bytes()).simple().to_string();
                    lessons.push(json!({ "lid": lid, "cid": cid, "bid": b.id, "ord": l_ord, "text": text }));
                }
            }
        }
    }

    let mut tasks = Vec::new();
    {
        let mut st = lite.prepare("SELECT book_id, chapter, id, ord, mode, title, statement, starter, hint, spec FROM tasks ORDER BY book_id, chapter, ord")?;
        let rows = st.query_map([], |r| {
            Ok(json!({
                "book": r.get::<_, i64>(0)?, "chapter": r.get::<_, i64>(1)?, "tid": r.get::<_, String>(2)?, "ord": r.get::<_, i64>(3)?,
                "mode": col_text(r, 4)?, "title": col_text(r, 5)?, "statement": col_text(r, 6)?, "starter": col_text(r, 7)?,
                "hint": col_text(r, 8)?, "spec": r.get::<_, String>(9)?,
            }))
        })?;
        for r in rows {
            tasks.push(r?);
        }
    }

    let mut quizzes = Vec::new();
    {
        let mut st = lite.prepare("SELECT book_id, chapter, kind, title FROM quizzes ORDER BY book_id, chapter")?;
        let rows = st.query_map([], |r| {
            Ok(json!({ "book": r.get::<_, i64>(0)?, "chapter": r.get::<_, i64>(1)?, "kind": r.get::<_, String>(2)?, "title": r.get::<_, String>(3)? }))
        })?;
        for r in rows {
            quizzes.push(r?);
        }
    }
    let mut quiz_questions = Vec::new();
    {
        let mut st = lite.prepare("SELECT book_id, chapter, ord, q, options, answer, expl FROM quiz_questions ORDER BY book_id, chapter, ord")?;
        let rows = st.query_map([], |r| {
            let options: Value = serde_json::from_str(&r.get::<_, String>(4)?).unwrap_or(Value::Array(Vec::new()));
            Ok(json!({
                "book": r.get::<_, i64>(0)?, "chapter": r.get::<_, i64>(1)?, "ord": r.get::<_, i64>(2)?, "q": r.get::<_, String>(3)?,
                "options": options, "answer": r.get::<_, i64>(5)?, "expl": col_text(r, 6)?,
            }))
        })?;
        for r in rows {
            quiz_questions.push(r?);
        }
    }

    let mut answer_sets = Vec::new();
    {
        let mut st = lite.prepare("SELECT book_id, chapter, title FROM answer_sets ORDER BY book_id, chapter")?;
        let rows = st.query_map([], |r| Ok(json!({ "book": r.get::<_, i64>(0)?, "chapter": r.get::<_, i64>(1)?, "title": r.get::<_, String>(2)? })))?;
        for r in rows {
            answer_sets.push(r?);
        }
    }
    let mut answer_tasks = Vec::new();
    {
        let mut st = lite.prepare("SELECT book_id, chapter, ord, q, answers, hint FROM answer_tasks ORDER BY book_id, chapter, ord")?;
        let rows = st.query_map([], |r| {
            let answers: Value = serde_json::from_str(&r.get::<_, String>(4)?).unwrap_or(Value::Array(Vec::new()));
            Ok(json!({
                "book": r.get::<_, i64>(0)?, "chapter": r.get::<_, i64>(1)?, "ord": r.get::<_, i64>(2)?, "q": r.get::<_, String>(3)?,
                "answers": answers, "hint": col_text(r, 5)?,
            }))
        })?;
        for r in rows {
            answer_tasks.push(r?);
        }
    }

    let (slide_chapters, slides) = load_slides(&cfg.slides_dir(), &mut raw)?;
    let lab_tasks = crate::labs::load(&cfg.labs_dir(), &mut raw)?;

    let hash = Sha256::digest(&raw).iter().map(|b| format!("{b:02x}")).collect::<String>();
    Ok(Content {
        tables: vec![
            ("books", meta_books.into_iter().map(|(_, v)| v).collect()),
            ("sections", sections),
            ("chapters", chapters),
            ("lessons", lessons),
            ("tasks", tasks),
            ("quizzes", quizzes),
            ("quiz_questions", quiz_questions),
            ("answer_sets", answer_sets),
            ("answer_tasks", answer_tasks),
            ("slide_chapters", slide_chapters),
            ("slides", slides),
            ("lab_tasks", lab_tasks),
        ],
        hash,
    })
}

/// Записывает содержимое в SurrealDB: таблицы очищаются и заполняются заново порциями.
pub async fn write(db: &Db, content: Content) -> anyhow::Result<()> {
    for (table, rows) in content.tables {
        db.query(format!("DELETE {table}")).await?.check()?;
        let step = match table {
            "tasks" => 100,
            "slides" => 20,
            "lab_tasks" => 10,
            _ => 400,
        };
        let total = rows.len();
        for chunk in rows.chunks(step) {
            db.query(format!("INSERT INTO {table} $rows")).bind(("rows", chunk.to_vec())).await?.check()?;
        }
        tracing::info!("сид: {table} — {total}");
    }
    db.query("UPSERT meta:seed SET hash = $h").bind(("h", content.hash)).await?.check()?;
    Ok(())
}

/// Сид по режиму `SEED`: `auto` — только если исходники изменились, `always` — всегда, `off` — никогда.
pub async fn run(db: &Db, cfg: &Config) -> anyhow::Result<()> {
    if cfg.seed == "off" {
        return Ok(());
    }
    let cfg2 = cfg.clone();
    let content = tokio::task::spawn_blocking(move || load(&cfg2)).await??;
    if cfg.seed != "always" {
        let mut res = db.query("SELECT VALUE hash FROM meta:seed").await?;
        let have: Vec<String> = res.take(0)?;
        let books: Vec<i64> = {
            let mut r = db.query("SELECT VALUE bid FROM books LIMIT 1").await?;
            r.take(0)?
        };
        if have.first().is_some_and(|h| *h == content.hash) && !books.is_empty() {
            tracing::info!("сид: исходники не изменились, пропускаю");
            return Ok(());
        }
    }
    write(db, content).await
}
