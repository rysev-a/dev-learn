//! Course content seed from the sources in `data/`: textbooks (`textbook/**/*.md`) and SQL files
//! (`sql/books.sql`, `sql/{tasks,quizzes,answers}`). SQL is run in a temporary in-memory SQLite, rows are moved into
//! SurrealDB. The seed does not touch user progress. Reseed only if the sources changed (hash in `meta:seed`).

use std::path::{Path, PathBuf};

use anyhow::Context;
use rusqlite::Connection as Sqlite;
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use uuid::Uuid;

use crate::{config::Config, db::Db, lang::Lang};

/// Fixed namespace for stable lesson ids (do not change: audio ids depend on it).
const NS: Uuid = Uuid::from_u128(0xd3a7c0de_0000_4000_8000_4b6f6b6f726f);

/// Content tables in write order: (table name, rows).
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

/// Textbook parsing: `#BOOK n`, `#SECTION title`, `#CHAPTER n | title`, then the lesson text lines.
fn parse_textbooks(dir: &Path) -> anyhow::Result<(Vec<Book>, Vec<u8>)> {
    let mut files = Vec::new();
    walk(dir, &mut files).with_context(|| format!("textbooks directory {}", dir.display()))?;
    files.sort();
    let mut books: Vec<Book> = Vec::new();
    let mut raw = Vec::new(); // content for the hash
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
                let id: i64 = rest.trim().parse().with_context(|| format!("#BOOK line in {}: {line}", path.display()))?;
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
                let (num, title) = rest.split_once('|').with_context(|| format!("#CHAPTER line in {}: {line}", path.display()))?;
                let num: i64 = num.trim().parse().with_context(|| format!("chapter number in {}: {line}", path.display()))?;
                let (Some(bi), Some(si)) = (book, section) else {
                    anyhow::bail!("chapter outside a section in {}: {line}", path.display());
                };
                books[bi].sections[si].chapters.push(Chapter { num, title: title.trim().to_string(), lessons: Vec::new() });
                chapter = Some(books[bi].sections[si].chapters.len() - 1);
            } else {
                let (Some(bi), Some(si), Some(ci)) = (book, section, chapter) else {
                    anyhow::bail!("lesson outside a chapter in {}: {}", path.display(), line.chars().take(60).collect::<String>());
                };
                // a literal \n in the source is the paragraph boundary
                books[bi].sections[si].chapters[ci].lessons.push(line.replace("\\n", "\n"));
            }
        }
    }
    // chapter files are self-contained and repeat #SECTION: consecutive identical sections are merged
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
    // every lesson paragraph is a separate part (slide)
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
        .with_context(|| format!("SQL directory {}", dir.display()))?
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
        lite.execute_batch(&text).with_context(|| format!("SQL file {}", f.display()))?;
    }
    Ok(())
}

fn col_text(r: &rusqlite::Row, i: usize) -> rusqlite::Result<Value> {
    Ok(match r.get::<_, Option<String>>(i)? {
        Some(s) => Value::String(s),
        None => Value::Null,
    })
}


fn read_quizzes(lite: &Sqlite) -> anyhow::Result<Vec<Value>> {
    let mut st = lite.prepare("SELECT book_id, chapter, kind, title FROM quizzes ORDER BY book_id, chapter")?;
    let rows = st.query_map([], |r| {
        Ok(json!({ "book": r.get::<_, i64>(0)?, "chapter": r.get::<_, i64>(1)?, "kind": r.get::<_, String>(2)?, "title": r.get::<_, String>(3)? }))
    })?;
    Ok(rows.collect::<Result<_, _>>()?)
}

fn read_quiz_questions(lite: &Sqlite) -> anyhow::Result<Vec<Value>> {
    let mut st = lite.prepare("SELECT book_id, chapter, ord, q, options, answer, expl FROM quiz_questions ORDER BY book_id, chapter, ord")?;
    let rows = st.query_map([], |r| {
        let options: Value = serde_json::from_str(&r.get::<_, String>(4)?).unwrap_or(Value::Array(Vec::new()));
        Ok(json!({
            "book": r.get::<_, i64>(0)?, "chapter": r.get::<_, i64>(1)?, "ord": r.get::<_, i64>(2)?, "q": r.get::<_, String>(3)?,
            "options": options, "answer": r.get::<_, i64>(5)?, "expl": col_text(r, 6)?,
        }))
    })?;
    Ok(rows.collect::<Result<_, _>>()?)
}

fn read_answer_sets(lite: &Sqlite) -> anyhow::Result<Vec<Value>> {
    let mut st = lite.prepare("SELECT book_id, chapter, title FROM answer_sets ORDER BY book_id, chapter")?;
    let rows = st.query_map([], |r| Ok(json!({ "book": r.get::<_, i64>(0)?, "chapter": r.get::<_, i64>(1)?, "title": r.get::<_, String>(2)? })))?;
    Ok(rows.collect::<Result<_, _>>()?)
}

fn read_answer_tasks(lite: &Sqlite) -> anyhow::Result<Vec<Value>> {
    let mut st = lite.prepare("SELECT book_id, chapter, ord, q, answers, hint FROM answer_tasks ORDER BY book_id, chapter, ord")?;
    let rows = st.query_map([], |r| {
        let answers: Value = serde_json::from_str(&r.get::<_, String>(4)?).unwrap_or(Value::Array(Vec::new()));
        Ok(json!({
            "book": r.get::<_, i64>(0)?, "chapter": r.get::<_, i64>(1)?, "ord": r.get::<_, i64>(2)?, "q": r.get::<_, String>(3)?,
            "answers": answers, "hint": col_text(r, 5)?,
        }))
    })?;
    Ok(rows.collect::<Result<_, _>>()?)
}

fn read_books(lite: &Sqlite) -> anyhow::Result<Vec<(i64, Value)>> {
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
    Ok(rows.collect::<Result<_, _>>()?)
}

/// Chapter slides from the data files: the chapter is validated (all scenes compile), then split into rows
/// `slide_chapters` (rubric and slide count) and `slides` (a row per slide; the body is blocks as a document).
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
        let ch: content::Chapter = serde_json::from_slice(&bytes).with_context(|| format!("slides {}", f.display()))?;
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


/// Translation tables in write order.
const I18N_TABLES: [&str; 12] = [
    "books_i18n",
    "sections_i18n",
    "chapters_i18n",
    "lessons_i18n",
    "quizzes_i18n",
    "quiz_questions_i18n",
    "answer_sets_i18n",
    "answer_tasks_i18n",
    "slide_chapters_i18n",
    "slides_i18n",
    "tasks_i18n",
    "lab_tasks_i18n",
];

fn rows_of<'a>(tables: &'a [(&'static str, Vec<Value>)], name: &str) -> &'a [Value] {
    tables.iter().find(|(n, _)| *n == name).map(|(_, r)| r.as_slice()).unwrap_or(&[])
}

fn with_lang(mut v: Value, lang: Lang) -> Value {
    if let Some(o) = v.as_object_mut() {
        o.insert("lang".into(), json!(lang.code()));
    }
    v
}

/// Content translation: the directory `data/<language>/` with the same files as the Russian one (textbooks, slides, `sql/books.sql`,
/// `sql/{quizzes,answers}`). A book is translated as a whole; keys (chapter and section ids, chapter numbers, number of paragraphs, slides, questions and
/// options) must match the Russian ones - otherwise user progress ("book + chapter + number") would drift, and the seed fails.
fn load_translation(cfg: &Config, lang: Lang, ru: &[(&'static str, Vec<Value>)], raw: &mut Vec<u8>) -> anyhow::Result<Vec<(&'static str, Vec<Value>)>> {
    let root = cfg.lang_dir(lang);
    raw.extend_from_slice(lang.code().as_bytes());

    let (books, text_raw) = parse_textbooks(&root.join("textbook"))?;
    raw.extend_from_slice(&text_raw);
    let sql = root.join("sql");
    let lite = Sqlite::open_in_memory()?;
    run_sql(&lite, &[sql.join("books.sql")], raw)?;
    // table schema is shared with the Russian one (file `00-schema.sql`), rows are translated
    for dir in ["quizzes", "answers"] {
        let mut files = vec![cfg.sql_dir().join(dir).join("00-schema.sql")];
        if sql.join(dir).is_dir() {
            files.extend(sql_files(&sql.join(dir))?.into_iter().filter(|f| f.file_name().is_some_and(|n| n != "00-schema.sql")));
        }
        run_sql(&lite, &files, raw)?;
    }
    let meta_books = read_books(&lite)?;
    let prefix_of = |bid: i64| -> String {
        meta_books
            .iter()
            .find(|(id, _)| *id == bid)
            .and_then(|(_, v)| v.get("audio_prefix").and_then(Value::as_str).filter(|s| !s.is_empty()).map(String::from))
            .unwrap_or_else(|| format!("b{bid}-ch"))
    };

    // section and chapter ids are the Russian ones: client addresses do not depend on the language
    let sid_of: std::collections::HashMap<(i64, i64), i64> = rows_of(ru, "sections").iter().map(|r| ((r["bid"].as_i64().unwrap_or(0), r["ord"].as_i64().unwrap_or(0)), r["sid"].as_i64().unwrap_or(0))).collect();
    let cid_of: std::collections::HashMap<(i64, i64), i64> = rows_of(ru, "chapters").iter().map(|r| ((r["bid"].as_i64().unwrap_or(0), r["num"].as_i64().unwrap_or(0)), r["cid"].as_i64().unwrap_or(0))).collect();

    let (mut sections, mut chapters, mut lessons) = (Vec::new(), Vec::new(), Vec::new());
    for b in &books {
        let prefix = prefix_of(b.id);
        for (s_ord, s) in b.sections.iter().enumerate() {
            let sid = *sid_of.get(&(b.id, s_ord as i64)).with_context(|| format!("book {}: the Russian version has no section #{}", b.id, s_ord + 1))?;
            sections.push(with_lang(json!({ "sid": sid, "bid": b.id, "title": s.title, "ord": s_ord }), lang));
            for c in &s.chapters {
                let cid = *cid_of.get(&(b.id, c.num)).with_context(|| format!("book {}: the Russian version has no chapter {}", b.id, c.num))?;
                chapters.push(with_lang(json!({ "cid": cid, "sid": sid, "bid": b.id, "num": c.num, "title": c.title }), lang));
                for (l_ord, text) in c.lessons.iter().enumerate() {
                    let lid = Uuid::new_v5(&NS, format!("{}:{prefix}{}-l{l_ord}", lang.code(), c.num).as_bytes()).simple().to_string();
                    lessons.push(with_lang(json!({ "lid": lid, "cid": cid, "bid": b.id, "ord": l_ord, "text": text }), lang));
                }
            }
        }
    }

    let (slide_chapters, slides) = load_slides(&root.join("slides"), raw)?;
    let task_texts = load_task_texts(&root.join("tasks"), raw)?;
    let lab_texts = crate::labs::load_texts(&root.join("labs"), raw)?;
    let tag = |rows: Vec<Value>| -> Vec<Value> { rows.into_iter().map(|v| with_lang(v, lang)).collect() };
    let out: Vec<(&'static str, Vec<Value>)> = vec![
        ("books_i18n", tag(meta_books.into_iter().map(|(_, v)| v).collect())),
        ("sections_i18n", sections),
        ("chapters_i18n", chapters),
        ("lessons_i18n", lessons),
        ("quizzes_i18n", tag(read_quizzes(&lite)?)),
        ("quiz_questions_i18n", tag(read_quiz_questions(&lite)?)),
        ("answer_sets_i18n", tag(read_answer_sets(&lite)?)),
        ("answer_tasks_i18n", tag(read_answer_tasks(&lite)?)),
        ("slide_chapters_i18n", tag(slide_chapters)),
        ("slides_i18n", tag(slides)),
        ("tasks_i18n", tag(task_texts)),
        ("lab_tasks_i18n", tag(lab_texts)),
    ];
    debug_assert!(out.iter().all(|(n, _)| I18N_TABLES.contains(n)));
    check_translation(lang, ru, &out)?;
    check_starters(ru, &out)?;
    check_lab_texts(ru, &out)?;
    Ok(out)
}

/// Keys of one book's rows: the fields forming the key and, if needed, the content shape (option count, right answer).
fn keys_of(rows: &[Value], book_field: &str, book: i64, key: &dyn Fn(&Value) -> String) -> std::collections::BTreeSet<String> {
    rows.iter().filter(|r| r[book_field].as_i64() == Some(book)).map(key).collect()
}

/// Translated code-task texts: files `<language>/tasks/<book>-<chapter>.json` - `{book, chapter, tasks: [{id, title, statement, hint, starter?}]}`.
/// Tests, drivers and references stay Russian (the shared `tasks` table); starter code is translated only in comments.
fn load_task_texts(dir: &std::path::Path, raw: &mut Vec<u8>) -> anyhow::Result<Vec<Value>> {
    let mut rows = Vec::new();
    if !dir.is_dir() {
        return Ok(rows);
    }
    let mut files: Vec<_> = std::fs::read_dir(dir)?.filter_map(Result::ok).map(|e| e.path()).filter(|p| p.extension().is_some_and(|e| e == "json")).collect();
    files.sort();
    for f in files {
        let bytes = std::fs::read(&f)?;
        raw.extend_from_slice(f.to_string_lossy().as_bytes());
        raw.extend_from_slice(&bytes);
        let ch: Value = serde_json::from_slice(&bytes).with_context(|| format!("tasks {}", f.display()))?;
        let (book, chapter) = (ch["book"].as_i64().unwrap_or(0), ch["chapter"].as_i64().unwrap_or(0));
        for t in ch["tasks"].as_array().with_context(|| format!("{}: no tasks", f.display()))? {
            let mut row = json!({ "book": book, "chapter": chapter, "tid": t["id"], "title": t["title"], "statement": t["statement"], "hint": t["hint"] });
            if let Some(starter) = t.get("starter").filter(|v| v.is_string()) {
                row["starter"] = starter.clone();
            }
            rows.push(row);
        }
    }
    Ok(rows)
}

/// Code without comments: in translated starter code everything except comments matches the Russian one.
fn code_skeleton(code: &str) -> String {
    // block comments `/* ... */` are removed entirely (as in C, Rust, SQL), the others - from `#`, `//` or `--` to the end of the line
    let mut text = String::with_capacity(code.len());
    let mut rest = code;
    while let Some(start) = rest.find("/*") {
        text.push_str(&rest[..start]);
        match rest[start..].find("*/") {
            Some(end) => rest = &rest[start + end + 2..],
            None => {
                rest = "";
                break;
            }
        }
    }
    text.push_str(rest);
    text.lines().map(|l| l.split('#').next().unwrap_or("").split("//").next().unwrap_or("").split("--").next().unwrap_or("").trim_end()).collect::<Vec<_>>().join("\n")
}

/// Lab texts: each translated chapter has the same exercises as the Russian data, and the `spec_text` paths point at scenario strings.
fn check_lab_texts(ru: &[(&'static str, Vec<Value>)], tr: &[(&'static str, Vec<Value>)]) -> anyhow::Result<()> {
    let base: std::collections::HashMap<(i64, i64, String), &Value> =
        rows_of(ru, "lab_tasks").iter().map(|r| ((r["book"].as_i64().unwrap_or(0), r["chapter"].as_i64().unwrap_or(0), r["tid"].as_str().unwrap_or("").to_string()), r)).collect();
    let mut seen: std::collections::BTreeMap<(i64, i64), std::collections::BTreeSet<String>> = Default::default();
    for r in rows_of(tr, "lab_tasks_i18n") {
        let (book, chapter, tid) = (r["book"].as_i64().unwrap_or(0), r["chapter"].as_i64().unwrap_or(0), r["tid"].as_str().unwrap_or("").to_string());
        let ru_row = base.get(&(book, chapter, tid.clone())).with_context(|| format!("lab {book}:{chapter}/{tid}: no such exercise in the Russian data"))?;
        for path in r["spec_text"].as_object().into_iter().flatten().map(|(p, _)| p) {
            anyhow::ensure!(ru_row["spec"].pointer(path).is_some_and(Value::is_string), "lab {book}:{chapter}/{tid}: the scenario has no string at path {path}");
        }
        seen.entry((book, chapter)).or_default().insert(tid);
    }
    for ((book, chapter), tids) in seen {
        let want: std::collections::BTreeSet<String> = base.keys().filter(|k| k.0 == book && k.1 == chapter).map(|k| k.2.clone()).collect();
        anyhow::ensure!(want == tids, "lab {book}:{chapter}: the translation's exercise set does not match the Russian one");
    }
    Ok(())
}

/// Starter code of a translated task differs from the Russian one only in comments.
fn check_starters(ru: &[(&'static str, Vec<Value>)], tr: &[(&'static str, Vec<Value>)]) -> anyhow::Result<()> {
    let base: std::collections::HashMap<(i64, i64, String), &str> =
        rows_of(ru, "tasks").iter().map(|r| ((r["book"].as_i64().unwrap_or(0), r["chapter"].as_i64().unwrap_or(0), r["tid"].as_str().unwrap_or("").to_string()), r["starter"].as_str().unwrap_or(""))).collect();
    for r in rows_of(tr, "tasks_i18n") {
        let (Some(starter), key) = (r["starter"].as_str(), (r["book"].as_i64().unwrap_or(0), r["chapter"].as_i64().unwrap_or(0), r["tid"].as_str().unwrap_or("").to_string())) else { continue };
        if let Some(ru_starter) = base.get(&key) {
            anyhow::ensure!(code_skeleton(ru_starter) == code_skeleton(starter), "task {}:{}/{}: the translated starter code changes more than comments", key.0, key.1, key.2);
        }
    }
    Ok(())
}

/// For each translated book the key sets of Russian and translated rows match in all tables.
fn check_translation(lang: Lang, ru: &[(&'static str, Vec<Value>)], tr: &[(&'static str, Vec<Value>)]) -> anyhow::Result<()> {
    let fields = |r: &Value, names: &[&str]| names.iter().map(|n| r[*n].to_string()).collect::<Vec<_>>().join("/");
    let options_len = |r: &Value| r["options"].as_array().map_or(0, Vec::len);
    type Key = Box<dyn Fn(&Value) -> String>;
    let specs: Vec<(&str, &str, &str, Key)> = vec![
        ("sections", "sections_i18n", "bid", Box::new(move |r| fields(r, &["sid", "ord"]))),
        ("chapters", "chapters_i18n", "bid", Box::new(move |r| fields(r, &["cid", "sid", "num"]))),
        ("lessons", "lessons_i18n", "bid", Box::new(move |r| fields(r, &["cid", "ord"]))),
        ("quizzes", "quizzes_i18n", "book", Box::new(move |r| fields(r, &["chapter", "kind"]))),
        ("quiz_questions", "quiz_questions_i18n", "book", Box::new(move |r| format!("{}|{}|{}", fields(r, &["chapter", "ord", "answer"]), options_len(r), r["answer"]))),
        ("answer_sets", "answer_sets_i18n", "book", Box::new(move |r| fields(r, &["chapter"]))),
        ("answer_tasks", "answer_tasks_i18n", "book", Box::new(move |r| fields(r, &["chapter", "ord"]))),
        ("slide_chapters", "slide_chapters_i18n", "book", Box::new(move |r| fields(r, &["chapter", "slides"]))),
        ("slides", "slides_i18n", "book", Box::new(move |r| fields(r, &["chapter", "idx"]))),
        ("tasks", "tasks_i18n", "book", Box::new(move |r| fields(r, &["chapter", "tid"]))),
        ("lab_tasks", "lab_tasks_i18n", "book", Box::new(move |r| fields(r, &["chapter", "tid"]))),
    ];
    for book in rows_of(tr, "books_i18n").iter().filter_map(|b| b["bid"].as_i64()) {
        for (base, i18n, book_field, key) in &specs {
            let (want, have) = (keys_of(rows_of(ru, base), book_field, book, key.as_ref()), keys_of(rows_of(tr, i18n), book_field, book, key.as_ref()));
            if want != have {
                let missing: Vec<_> = want.difference(&have).take(3).cloned().collect();
                let extra: Vec<_> = have.difference(&want).take(3).cloned().collect();
                anyhow::bail!("book {book}, {} / {}: translation structure does not match the Russian one (missing: {missing:?}; extra: {extra:?})", base, lang.code());
            }
        }
    }
    Ok(())
}

/// Reads the sources and builds the rows of all content tables. Blocking work (files, SQLite).
pub fn load(cfg: &Config) -> anyhow::Result<Content> {
    let (books, mut raw) = parse_textbooks(&cfg.textbook_dir())?;
    let sql = cfg.sql_dir();
    let lite = Sqlite::open_in_memory()?;

    let books_sql = sql.join("books.sql");
    run_sql(&lite, &[books_sql], &mut raw)?;
    for dir in ["tasks", "quizzes", "answers"] {
        run_sql(&lite, &sql_files(&sql.join(dir))?, &mut raw)?;
    }

    let meta_books = read_books(&lite)?;
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

    let quizzes = read_quizzes(&lite)?;
    let quiz_questions = read_quiz_questions(&lite)?;
    let answer_sets = read_answer_sets(&lite)?;
    let answer_tasks = read_answer_tasks(&lite)?;

    let (slide_chapters, slides) = load_slides(&cfg.slides_dir(), &mut raw)?;
    let lab_tasks = crate::labs::load(&cfg.labs_dir(), &mut raw)?;

    let mut tables: Vec<(&'static str, Vec<Value>)> = vec![
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
    ];
    for lang in Lang::ALL.into_iter().filter(|l| *l != Lang::Ru) {
        if cfg.lang_dir(lang).is_dir() {
            let translated = load_translation(cfg, lang, &tables, &mut raw).with_context(|| format!("translation '{}'", lang.code()))?;
            tables.extend(translated);
        }
    }

    let hash = Sha256::digest(&raw).iter().map(|b| format!("{b:02x}")).collect::<String>();
    Ok(Content { tables, hash })
}

/// Writes the content to SurrealDB: tables are cleared and refilled in batches.
pub async fn write(db: &Db, content: Content) -> anyhow::Result<()> {
    for (table, rows) in content.tables {
        db.query(format!("DELETE {table}")).await?.check()?;
        let step = match table.trim_end_matches("_i18n") {
            "tasks" => 100,
            "slides" => 20,
            "lab_tasks" => 10,
            _ => 400,
        };
        let total = rows.len();
        for chunk in rows.chunks(step) {
            db.query(format!("INSERT INTO {table} $rows")).bind(("rows", chunk.to_vec())).await?.check()?;
        }
        tracing::info!("seed: {table} - {total}");
    }
    db.query("UPSERT meta:seed SET hash = $h").bind(("h", content.hash)).await?.check()?;
    Ok(())
}

/// Seed by the `SEED` mode: `auto` - only if the sources changed, `always` - always, `off` - never.
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
            tracing::info!("seed: sources unchanged, skipping");
            return Ok(());
        }
    }
    write(db, content).await
}
