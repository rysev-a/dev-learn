//! API response DTOs. Fields mirror the backend JSON; anything that may be missing is `Option` or `#[serde(default)]`.

use std::collections::HashMap;

use serde::Deserialize;
use serde_json::Value;

/// `{book: {chapter: count}}` — how many quizzes/tasks each chapter has.
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
    /// Languages the book is fully available in (Russian is always there); an old server lacks the field.
    #[serde(default)]
    pub langs: Vec<String>,
}

impl Book {
    /// Whether the book exists in language `code` (`ru`, `en`); without a language list we assume it does.
    pub fn in_language(&self, code: &str) -> bool {
        self.langs.is_empty() || self.langs.iter().any(|l| l == code)
    }
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

/// Chapter part: one lesson paragraph (= one slide).
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct Lesson {
    pub id: String,
    pub ord: usize,
    pub text: String,
    pub audio: String,
    /// voice-over duration, seconds (0 — no file)
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

// --- progress -----------------------------------------------------------------------------------

/// All of a user's progress; keys are `"book:chapter"`.
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

/// What `DELETE /api/progress` erases: exercises (statuses, drafts, attempts, answers) or all progress.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum ResetScope {
    Practice,
    All,
}

impl ResetScope {
    /// Value of the `scope` parameter in the request URL.
    pub fn param(self) -> &'static str {
        match self {
            ResetScope::Practice => "practice",
            ResetScope::All => "all",
        }
    }
}

// --- quizzes and answers -----------------------------------------------------------------------------

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
    /// answer and explanation for questions the user has already answered
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
    /// solved tasks: number → accepted answer
    #[serde(default)]
    pub solved: HashMap<String, String>,
}

#[derive(Deserialize)]
pub(crate) struct Verdict {
    pub ok: bool,
}

// --- code exercises -------------------------------------------------------------------------

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
    /// boards shown beside the results (the oVirt board tasks of book 17)
    #[serde(default)]
    pub board: Option<TaskBoards>,
}

/// Boards of a code task: the boards of its tests (the answer is plain data) and the scenarios its repaired boards are judged by (the code returns a board).
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct TaskBoards {
    /// which board model the boards belong to: `ovirt_topo` (default), `lvm_board` or `net_board`
    #[serde(default = "default_board_kind")]
    pub kind: String,
    #[serde(default)]
    pub boards: Vec<Value>,
    #[serde(default)]
    pub checks: Vec<BoardCheck>,
}

fn default_board_kind() -> String {
    "ovirt_topo".into()
}

impl Default for TaskBoards {
    fn default() -> Self {
        TaskBoards { kind: default_board_kind(), boards: Vec::new(), checks: Vec::new() }
    }
}

/// One scenario of a pack, the way the server names it.
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct BoardCheck {
    pub pack: String,
    pub scenario: String,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct ChapterTasks {
    pub tasks: Vec<Task>,
    /// schemas and data of the SQL tasks' sample databases (used to draw the ERD); key is `Task::dataset`
    #[serde(default)]
    pub datasets: HashMap<String, SqlDataset>,
}

// --- SQL task sample databases ---------------------------------------------------------------------

/// A column's foreign key: which column of which table it references.
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct SqlForeignKey {
    pub table: String,
    pub column: String,
}

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct SqlColumn {
    pub name: String,
    /// declared column type (`INTEGER`, `TEXT`, …; may be empty for views)
    #[serde(default, rename = "type", deserialize_with = "null_default")]
    pub data_type: String,
    #[serde(default)]
    pub pk: bool,
    #[serde(default)]
    pub notnull: bool,
    #[serde(default)]
    pub fk: Option<SqlForeignKey>,
}

/// Table or view: columns and the first rows (`total` is the total row count).
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct SqlTable {
    pub name: String,
    /// `table` or `view`
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

/// A "foreign key → parent" relation.
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

/// Missing and `null` both give the default value (the sandbox returns `null` when the query had no columns).
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

/// Result tables of an SQL task: the learner's (`got_*`) and the correct one (`exp_*`); `*_rows` are only the first rows, `*_total` is how many there are in all.
#[derive(Clone, Debug, Default, PartialEq, Deserialize)]
pub struct RowsView {
    /// row order matters for checking
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

/// A single check test.
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
    /// result kind: `rows` — SQL query tables (see `rows`), `text` — text (query plans)
    #[serde(default)]
    pub kind: Option<String>,
    /// the board the code returned, with the model's verdict in `ok` (the board tasks)
    #[serde(default)]
    pub board: Option<Value>,
    #[serde(flatten)]
    pub rows: RowsView,
}

impl TestResult {
    /// SQL query result shown as two tables.
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

/// State of a job in the check queue.
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

// --- sign-in ---------------------------------------------------------------------------------------

#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct User {
    pub id: String,
    pub email: String,
    #[serde(default)]
    pub profile: Value,
}

impl User {
    /// Name from the profile, otherwise the part of the email before "@".
    pub fn display(&self) -> String {
        self.profile.get("name").and_then(Value::as_str).filter(|n| !n.trim().is_empty()).map(String::from).unwrap_or_else(|| self.email.split('@').next().unwrap_or(&self.email).to_string())
    }
}

/// Identity: user, roles and (on sign-in) the session token.
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
                    { "name": "customers", "kind": "table", "total": 1, "rows": [[1, "Ann"]],
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
        let named: User = serde_json::from_value(json!({ "id": "1", "email": "a@b.c", "profile": { "name": "Ann" } })).unwrap();
        let bare: User = serde_json::from_value(json!({ "id": "2", "email": "student@mail.com", "profile": {} })).unwrap();
        assert_eq!(named.display(), "Ann");
        assert_eq!(bare.display(), "student");
    }
}

/// Lab exercise: statement and scenario (`spec` is the lab data; it has no reference solution).
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

/// Chapter lab exercises: lab kind (`sd`, `net`, `arch`, `riscv`, `virt`) and the exercises in order.
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct LabChapter {
    pub lab: String,
    pub tasks: Vec<LabTask>,
}

/// A recorded take of a slide (author tool).
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct Take {
    pub id: i64,
    /// length, seconds
    pub dur: f64,
    /// time of recording, seconds since the epoch
    pub at: u64,
    /// the pronunciation check of this take, if it was made
    #[serde(default)]
    pub assessment: Option<Assessment>,
}

/// The pronunciation check of a take (scores are 0..100): the whole take and every word of the text.
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct Assessment {
    /// time of the check, seconds since the epoch
    pub at: u64,
    /// the overall score
    pub pron: f64,
    pub accuracy: f64,
    pub fluency: f64,
    pub completeness: f64,
    /// rhythm and intonation; English only
    #[serde(default)]
    pub prosody: Option<f64>,
    #[serde(default)]
    pub words: Vec<AssessedWord>,
}

/// A word of the text with its score. `error` is `None`, `Omission` (not said), `Insertion` (extra) or `Mispronunciation`;
/// `pause` is `None`, `UnexpectedBreak` or `MissingBreak`.
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct AssessedWord {
    pub word: String,
    pub accuracy: f64,
    pub error: String,
    pub pause: String,
    #[serde(default)]
    pub phonemes: Vec<AssessedPhoneme>,
}

/// A sound of a word (IPA for English) and how well it was pronounced.
#[derive(Clone, Debug, PartialEq, Deserialize)]
pub struct AssessedPhoneme {
    pub phoneme: String,
    pub accuracy: f64,
}

/// The recordings of a slide in the interface language: the takes, the chosen one (it voices the slide) with its address and length.
#[derive(Clone, Debug, Default, PartialEq, Deserialize)]
pub struct Takes {
    pub takes: Vec<Take>,
    pub selected: Option<i64>,
    pub audio: Option<String>,
    #[serde(default)]
    pub dur: f64,
}
