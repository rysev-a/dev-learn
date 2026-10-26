//! DTO ответов API. Поля повторяют JSON бэкенда; всё, что может отсутствовать, — `Option` или `#[serde(default)]`.

use std::collections::HashMap;

use serde::Deserialize;
use serde_json::Value;

/// `{книга: {глава: число}}` — сколько квизов/задач в каждой главе.
pub type Counts = HashMap<String, HashMap<String, i64>>;

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct Book {
    pub id: i64,
    pub title: String,
    pub slug: Option<String>,
    pub slides_dir: Option<String>,
    pub icon: Option<String>,
    pub sections_count: i64,
    pub lessons_count: i64,
    pub parts_count: i64,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct Section {
    pub id: i64,
    pub title: String,
    pub chapters: Vec<ChapterRef>,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct ChapterRef {
    pub id: i64,
    pub num: i64,
    pub title: String,
    pub parts_count: i64,
}

/// Часть главы: один абзац урока (= один слайд).
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct Lesson {
    pub id: String,
    pub ord: usize,
    pub text: String,
    pub audio: String,
    /// длительность озвучки, секунды (0 — файла нет)
    pub dur: f64,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct Chapter {
    pub id: i64,
    pub num: i64,
    pub title: String,
    pub section: String,
    pub lessons: Vec<Lesson>,
}

// --- прогресс -----------------------------------------------------------------------------------

/// Весь прогресс пользователя; ключи — `"книга:глава"`.
#[derive(Clone, Debug, Default, PartialEq, Deserialize)]
pub struct Progress {
    #[serde(default)]
    pub slides: HashMap<String, Vec<usize>>,
    #[serde(default)]
    pub quiz: HashMap<String, Vec<Option<usize>>>,
    #[serde(default, rename = "quizRight")]
    pub quiz_right: HashMap<String, usize>,
    #[serde(default)]
    pub answers: HashMap<String, HashMap<String, String>>,
    #[serde(default)]
    pub code: HashMap<String, HashMap<String, String>>,
}

pub fn progress_key(book: i64, chapter: i64) -> String {
    format!("{book}:{chapter}")
}

/// Что стирает `DELETE /api/progress`: упражнения (статусы, черновики, попытки, ответы) или весь прогресс.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ResetScope {
    Practice,
    All,
}

impl ResetScope {
    /// Значение параметра `scope` в адресе запроса.
    pub fn param(self) -> &'static str {
        match self {
            ResetScope::Practice => "practice",
            ResetScope::All => "all",
        }
    }
}

// --- квизы и ответы -----------------------------------------------------------------------------

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct Question {
    pub q: String,
    pub options: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct Reveal {
    pub answer: usize,
    #[serde(default)]
    pub expl: String,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct Quiz {
    pub kind: String,
    pub title: String,
    pub questions: Vec<Question>,
    /// ответ и пояснение для вопросов, на которые пользователь уже ответил
    pub reveal: Vec<Option<Reveal>>,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct QuizAnswer {
    pub pick: usize,
    pub answer: usize,
    #[serde(default)]
    pub expl: String,
    pub right: usize,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct AnswerTask {
    pub q: String,
    #[serde(default)]
    pub hint: String,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct PracticeSet {
    pub title: String,
    pub tasks: Vec<AnswerTask>,
    /// решённые задачи: номер → принятый ответ
    #[serde(default)]
    pub solved: HashMap<String, String>,
}

#[derive(Deserialize)]
pub(crate) struct Verdict {
    pub ok: bool,
}

// --- упражнения с кодом -------------------------------------------------------------------------

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct Task {
    pub id: String,
    #[serde(default)]
    pub mode: String,
    #[serde(default)]
    pub title: String,
    #[serde(default)]
    pub statement: String,
    #[serde(default)]
    pub starter: String,
    #[serde(default)]
    pub hint: String,
    #[serde(default)]
    pub dataset: Option<String>,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct ChapterTasks {
    pub tasks: Vec<Task>,
    /// схемы и данные учебных баз SQL-задач (рисуют ERD); ключ — `Task::dataset`
    #[serde(default)]
    pub datasets: HashMap<String, SqlDataset>,
}

// --- учебные базы SQL-задач ---------------------------------------------------------------------

/// Внешний ключ столбца: на какой столбец какой таблицы он ссылается.
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct SqlForeignKey {
    pub table: String,
    pub column: String,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct SqlColumn {
    pub name: String,
    /// объявленный тип столбца (`INTEGER`, `TEXT`, …; у представлений бывает пустым)
    #[serde(default, rename = "type", deserialize_with = "null_default")]
    pub data_type: String,
    #[serde(default)]
    pub pk: bool,
    #[serde(default)]
    pub notnull: bool,
    #[serde(default)]
    pub fk: Option<SqlForeignKey>,
}

/// Таблица или представление: столбцы и первые строки (`total` — сколько строк всего).
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct SqlTable {
    pub name: String,
    /// `table` или `view`
    #[serde(default)]
    pub kind: String,
    pub columns: Vec<SqlColumn>,
    #[serde(default)]
    pub rows: Vec<Vec<Value>>,
    #[serde(default)]
    pub total: usize,
}

impl SqlTable {
    pub fn is_view(&self) -> bool {
        self.kind == "view"
    }
}

/// Связь «внешний ключ → родитель».
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct SqlRelation {
    pub from: String,
    pub from_col: String,
    pub to: String,
    pub to_col: String,
}

#[derive(Clone, Debug, Default, PartialEq, Deserialize)]
pub struct SqlDataset {
    #[serde(default)]
    pub tables: Vec<SqlTable>,
    #[serde(default)]
    pub relations: Vec<SqlRelation>,
}

/// Отсутствующее и `null` — значение по умолчанию (песочница отдаёт `null`, если у запроса не было столбцов).
fn null_default<'de, D, T>(de: D) -> Result<T, D::Error>
where
    D: serde::Deserializer<'de>,
    T: Default + Deserialize<'de>,
{
    Ok(Option::<T>::deserialize(de)?.unwrap_or_default())
}

#[derive(Clone, Debug, Default, PartialEq, Deserialize)]
pub struct ChapterState {
    #[serde(default)]
    pub status: HashMap<String, String>,
    #[serde(default)]
    pub drafts: HashMap<String, String>,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct Attempt {
    pub id: i64,
    pub code: String,
    pub status: String,
    pub passed: i64,
    pub total: i64,
    pub created_at: String,
}

#[derive(Deserialize)]
pub(crate) struct Attempts {
    pub attempts: Vec<Attempt>,
}

/// Таблицы результата SQL-задачи: полученная ученицей (`got_*`) и верная (`exp_*`); `*_rows` — только первые строки, `*_total` — сколько их всего.
#[derive(Clone, Debug, Default, PartialEq, Deserialize)]
pub struct RowsView {
    /// порядок строк важен для проверки
    #[serde(default, deserialize_with = "null_default")]
    pub ordered: bool,
    #[serde(default, deserialize_with = "null_default")]
    pub got_cols: Vec<String>,
    #[serde(default, deserialize_with = "null_default")]
    pub got_rows: Vec<Vec<Value>>,
    #[serde(default)]
    pub got_total: Option<usize>,
    #[serde(default, deserialize_with = "null_default")]
    pub exp_cols: Vec<String>,
    #[serde(default, deserialize_with = "null_default")]
    pub exp_rows: Vec<Vec<Value>>,
    #[serde(default)]
    pub exp_total: Option<usize>,
}

/// Один тест проверки.
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct TestResult {
    #[serde(default)]
    pub ok: bool,
    #[serde(default)]
    pub args: Option<String>,
    #[serde(default)]
    pub got: Value,
    #[serde(default)]
    pub expected: Value,
    #[serde(default)]
    pub error: Option<String>,
    /// вид результата: `rows` — таблицы SQL-запроса (см. `rows`), `text` — текст (планы запросов)
    #[serde(default)]
    pub kind: Option<String>,
    #[serde(flatten)]
    pub rows: RowsView,
}

impl TestResult {
    /// Результат SQL-запроса, который показывают двумя таблицами.
    pub fn is_rows(&self) -> bool {
        self.kind.as_deref() == Some("rows")
    }
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct AttemptInfo {
    pub id: i64,
    pub status: String,
    pub created_at: String,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct RunResult {
    pub status: String,
    #[serde(default)]
    pub results: Vec<TestResult>,
    #[serde(default)]
    pub stdout: String,
    #[serde(default)]
    pub stderr: String,
    #[serde(default)]
    pub passed: i64,
    #[serde(default)]
    pub total: i64,
    #[serde(default)]
    pub solved: bool,
    #[serde(default)]
    pub attempt: Option<AttemptInfo>,
}

/// Состояние задания в очереди проверок.
#[derive(Clone, Debug, PartialEq, Deserialize)]
#[serde(tag = "state", rename_all = "lowercase")]
pub enum RunState {
    Queued {
        #[serde(default)]
        position: Option<i64>,
    },
    Running,
    Done(RunResult),
}

// --- вход ---------------------------------------------------------------------------------------

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct User {
    pub id: String,
    pub email: String,
    #[serde(default)]
    pub profile: Value,
}

impl User {
    /// Имя из профиля, иначе часть email до «@».
    pub fn display(&self) -> String {
        self.profile.get("name").and_then(Value::as_str).filter(|n| !n.trim().is_empty()).map(String::from).unwrap_or_else(|| self.email.split('@').next().unwrap_or(&self.email).to_string())
    }
}

/// Личность: пользователь, роли и (при входе) токен сессии.
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct Identity {
    pub user: User,
    #[serde(default)]
    pub token: Option<String>,
    #[serde(default)]
    pub roles: Vec<String>,
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn reset_scope_matches_the_backend_parameter() {
        assert_eq!(ResetScope::Practice.param(), "practice");
        assert_eq!(ResetScope::All.param(), "all");
    }

    #[test]
    fn run_state_variants_parse_by_the_state_tag() {
        let q: RunState = serde_json::from_value(json!({ "state": "queued", "position": 3 })).unwrap();
        assert_eq!(q, RunState::Queued { position: Some(3) });
        assert_eq!(serde_json::from_value::<RunState>(json!({ "state": "running" })).unwrap(), RunState::Running);
        let d: RunState = serde_json::from_value(json!({
            "state": "done", "status": "ok", "passed": 1, "total": 1, "solved": true,
            "results": [{ "ok": true, "got": "1991\n", "expected": "1991\n", "error": null }],
            "stdout": "", "stderr": "", "attempt": { "id": 2, "status": "ok", "created_at": "2026-10-22T16:00:00+00:00" }
        }))
        .unwrap();
        match d {
            RunState::Done(r) => {
                assert!(r.solved);
                assert_eq!(r.results.len(), 1);
                assert_eq!(r.attempt.unwrap().id, 2);
            }
            other => panic!("{other:?}"),
        }
    }

    #[test]
    fn sql_result_tables_and_datasets_parse_with_nulls() {
        let r: TestResult = serde_json::from_value(json!({
            "ok": false, "got": "x", "expected": "y", "error": null, "kind": "rows", "ordered": true,
            "got_cols": null, "got_rows": [[1, "a", null]], "got_total": 1,
            "exp_cols": ["id", "name"], "exp_rows": [[1, "a"], [2, "b"]], "exp_total": 2
        }))
        .unwrap();
        assert!(r.is_rows() && r.rows.ordered);
        assert!(r.rows.got_cols.is_empty());
        assert_eq!(r.rows.got_rows[0].len(), 3);
        assert_eq!((r.rows.got_total, r.rows.exp_total), (Some(1), Some(2)));
        let plain: TestResult = serde_json::from_value(json!({ "ok": true, "got": "1", "expected": "1" })).unwrap();
        assert!(!plain.is_rows() && plain.rows == RowsView::default());

        let t: ChapterTasks = serde_json::from_value(json!({
            "tasks": [{ "id": "s01-1", "mode": "sql", "dataset": "k" }],
            "datasets": { "k": {
                "tables": [
                    { "name": "customers", "kind": "table", "total": 1, "rows": [[1, "Аня"]],
                      "columns": [{ "name": "id", "type": "INTEGER", "pk": true, "notnull": true, "fk": null }, { "name": "name", "type": "TEXT", "pk": false, "notnull": false }] },
                    { "name": "orders", "kind": "view", "total": 0, "rows": [],
                      "columns": [{ "name": "customer_id", "type": "INTEGER", "pk": false, "notnull": false, "fk": { "table": "customers", "column": "id" } }] }
                ],
                "relations": [{ "from": "orders", "from_col": "customer_id", "to": "customers", "to_col": "id" }]
            } }
        }))
        .unwrap();
        let d = &t.datasets["k"];
        assert_eq!(d.tables.len(), 2);
        assert!(d.tables[1].is_view() && !d.tables[0].is_view());
        assert!(d.tables[0].columns[0].pk && d.tables[1].columns[0].fk.is_some());
        assert_eq!(d.tables[0].columns[1].data_type, "TEXT");
        assert_eq!(d.relations[0].to, "customers");
    }

    #[test]
    fn progress_tolerates_missing_sections_and_null_picks() {
        let p: Progress = serde_json::from_value(json!({ "quiz": { "12:1": [1, null, 2] }, "quizRight": { "12:1": 2 } })).unwrap();
        assert_eq!(p.quiz["12:1"], vec![Some(1), None, Some(2)]);
        assert_eq!(p.quiz_right["12:1"], 2);
        assert!(p.slides.is_empty());
        assert_eq!(progress_key(12, 1), "12:1");
    }

    #[test]
    fn user_display_falls_back_to_the_email_name() {
        let named: User = serde_json::from_value(json!({ "id": "1", "email": "a@b.c", "profile": { "name": "Аня" } })).unwrap();
        let bare: User = serde_json::from_value(json!({ "id": "2", "email": "student@mail.com", "profile": {} })).unwrap();
        assert_eq!(named.display(), "Аня");
        assert_eq!(bare.display(), "student");
    }
}

/// Упражнение-лаборатория: условие и сценарий (`spec` — данные лаборатории; эталонного решения в нём нет).
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct LabTask {
    pub id: String,
    pub title: String,
    #[serde(default)]
    pub statement: String,
    #[serde(default)]
    pub hint: String,
    pub spec: serde_json::Value,
}

/// Лабораторные упражнения главы: вид лаборатории (`sd`, `net`, `arch`, `riscv`, `virt`) и упражнения по порядку.
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct LabChapter {
    pub lab: String,
    pub tasks: Vec<LabTask>,
}
