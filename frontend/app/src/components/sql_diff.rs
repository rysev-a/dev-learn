//! Comparison of an SQL query result with the reference: the student's result on the left, the correct one on the right. Differing values are highlighted in both
//! tables, extra and missing rows are marked, and the headers of extra and missing columns are highlighted.
//!
//! The server check compares values by position (column names do not matter), so here rows and columns are matched
//! by position too; a name difference is shown as a soft note. The comparison is pure functions (`align`, `compare`) with tests,
//! the components only draw the ready model.

use std::collections::{HashMap, VecDeque};

use api::dto::RowsView;
use leptos::prelude::*;
use serde_json::Value;

use super::sql_schema::cell_text;

type Row = Vec<Value>;

/// Whose table: the student's (`Got`) or the reference (`Exp`).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Side {
    Got,
    Exp,
}

impl Side {
    fn class(self) -> &'static str {
        match self {
            Side::Got => "got",
            Side::Exp => "exp",
        }
    }

    /// Highlight of the "other side's" value: for the student - extra (`extra`), for the reference - missing (`missing`).
    fn mark(self) -> Mark {
        match self {
            Side::Got => Mark::Extra,
            Side::Exp => Mark::Missing,
        }
    }
}

/// Highlight of a cell or header (CSS classes `extra` and `missing`).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Mark {
    None,
    Extra,
    Missing,
}

impl Mark {
    fn class(self) -> &'static str {
        match self {
            Mark::None => "",
            Mark::Extra => "extra",
            Mark::Missing => "missing",
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum RowState {
    Ok,
    /// the row exists on both sides, but the values differ
    Diff,
    /// extra row (the student has it, the reference does not)
    Extra,
    /// missing row (the reference has it, the student does not)
    Missing,
}

impl RowState {
    fn class(self) -> &'static str {
        match self {
            RowState::Ok => "sd-ok",
            RowState::Diff => "sd-diff",
            RowState::Extra => "sd-extra",
            RowState::Missing => "sd-missing",
        }
    }
}

/// Result of matching a row: state and "pair" - the row number on the other side it is compared with cell by cell.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct Aligned {
    state: RowState,
    pair: Option<usize>,
}

const OK: Aligned = Aligned { state: RowState::Ok, pair: None };

/// Values are equal: numbers by value (`1` and `1.0`), empty with empty.
fn same(a: Option<&Value>, b: Option<&Value>) -> bool {
    match (a.unwrap_or(&Value::Null), b.unwrap_or(&Value::Null)) {
        (Value::Number(x), Value::Number(y)) => x.as_f64() == y.as_f64(),
        (x, y) => x == y,
    }
}

/// Row key for finding matches: numbers are normalized, as in `same`.
fn row_key(row: &Row) -> String {
    row.iter()
        .map(|v| match v {
            Value::Number(n) => n.as_f64().map_or_else(|| n.to_string(), |f| f.to_string()),
            other => other.to_string(),
        })
        .collect::<Vec<_>>()
        .join("\u{1f}")
}

fn rows_equal(a: &Row, b: &Row) -> bool {
    a.len() == b.len() && a.iter().zip(b).all(|(x, y)| same(Some(x), Some(y)))
}

/// Row matching: for each row of the result and the reference - state and pair for per-cell highlighting.
///
/// With order, rows are compared by index, the remainder is extra or missing. Without order, matching rows are removed first
/// (taking duplicates into account), and the remaining extra and missing ones are paired in turn.
fn align(got: &[Row], exp: &[Row], ordered: bool) -> (Vec<Aligned>, Vec<Aligned>) {
    let mut gs = vec![OK; got.len()];
    let mut es = vec![OK; exp.len()];
    let (extra, missing): (Vec<usize>, Vec<usize>) = if ordered {
        let n = got.len().min(exp.len());
        for i in (0..n).filter(|&i| !rows_equal(&got[i], &exp[i])) {
            gs[i] = Aligned { state: RowState::Diff, pair: Some(i) };
            es[i] = Aligned { state: RowState::Diff, pair: Some(i) };
        }
        ((n..got.len()).collect(), (n..exp.len()).collect())
    } else {
        let mut pool: HashMap<String, VecDeque<usize>> = HashMap::new();
        for (i, r) in exp.iter().enumerate() {
            pool.entry(row_key(r)).or_default().push_back(i);
        }
        let extra: Vec<usize> = got.iter().enumerate().filter(|(_, r)| pool.get_mut(&row_key(r)).and_then(VecDeque::pop_front).is_none()).map(|(i, _)| i).collect();
        let mut missing: Vec<usize> = pool.into_values().flatten().collect();
        missing.sort_unstable();
        (extra, missing)
    };
    // in ordered mode too the remainder is an unpaired tail; without order extra and missing ones are paired in turn
    let paired = if ordered { 0 } else { extra.len().min(missing.len()) };
    for (&g, &e) in extra.iter().zip(&missing).take(paired) {
        gs[g] = Aligned { state: RowState::Diff, pair: Some(e) };
        es[e] = Aligned { state: RowState::Diff, pair: Some(g) };
    }
    for &g in &extra[paired..] {
        gs[g] = Aligned { state: RowState::Extra, pair: None };
    }
    for &e in &missing[paired..] {
        es[e] = Aligned { state: RowState::Missing, pair: None };
    }
    (gs, es)
}

// --- table model --------------------------------------------------------------------------------

#[derive(Clone, Debug, PartialEq)]
struct Header {
    name: String,
    mark: Mark,
    title: Option<&'static str>,
}

#[derive(Clone, Debug, PartialEq)]
struct CellModel {
    text: String,
    /// `extra`/`missing`, plus `num` for numbers
    class: String,
}

#[derive(Clone, Debug, PartialEq)]
struct RowModel {
    class: &'static str,
    cells: Vec<CellModel>,
}

/// One comparison table, ready to display.
#[derive(Clone, Debug, PartialEq)]
struct TableModel {
    side: Side,
    title: &'static str,
    total: usize,
    shown: usize,
    headers: Vec<Header>,
    rows: Vec<RowModel>,
}

/// Source data of one side and its "counterpart".
struct SideInput<'a> {
    side: Side,
    cols: &'a [String],
    rows: &'a [Row],
    total: usize,
    status: &'a [Aligned],
    other_rows: &'a [Row],
    other_width: usize,
}

fn width_of(cols: &[String], rows: &[Row]) -> usize {
    rows.iter().map(Vec::len).fold(cols.len(), usize::max)
}

fn cell_model(side: Side, row: &Row, aligned: Aligned, peer: Option<&Row>, j: usize) -> CellModel {
    let value = row.get(j);
    let mark = match aligned.state {
        RowState::Extra => Mark::Extra,
        RowState::Missing => Mark::Missing,
        RowState::Diff if j >= peer.map_or(0, Vec::len) || !same(value, peer.and_then(|p| p.get(j))) => side.mark(),
        _ => Mark::None,
    };
    let mut class = mark.class().to_string();
    if value.is_some_and(Value::is_number) {
        class.push_str(if class.is_empty() { "num" } else { " num" });
    }
    CellModel { text: value.map(cell_text).unwrap_or_default(), class }
}

fn table_model(width: usize, input: SideInput) -> TableModel {
    let SideInput { side, cols, rows, total, status, other_rows, other_width } = input;
    let headers = (0..width)
        .map(|j| {
            // a column absent on the other side: extra for the student, missing for the reference
            let lacking = j >= other_width;
            Header {
                name: cols.get(j).cloned().unwrap_or_else(|| format!("col{}", j + 1)),
                mark: if lacking { side.mark() } else { Mark::None },
                title: lacking.then_some(match side {
                    Side::Got => i18n::tr("extra column"),
                    Side::Exp => i18n::tr("this column is missing from your result"),
                }),
            }
        })
        .collect();
    let rows_model = rows
        .iter()
        .zip(status)
        .map(|(row, &aligned)| {
            let peer = aligned.pair.and_then(|p| other_rows.get(p));
            RowModel { class: aligned.state.class(), cells: (0..width).map(|j| cell_model(side, row, aligned, peer, j)).collect() }
        })
        .collect();
    TableModel {
        side,
        title: match side {
            Side::Got => i18n::tr("your result"),
            Side::Exp => i18n::tr("expected result"),
        },
        total,
        shown: rows.len(),
        headers,
        rows: rows_model,
    }
}

/// Everything the widget draws: difference summary, two tables and a note about renamed columns.
#[derive(Clone, Debug, PartialEq)]
struct Comparison {
    summary: Vec<String>,
    got: TableModel,
    exp: TableModel,
    renamed: bool,
}

fn compare(r: &RowsView) -> Comparison {
    let (got_width, exp_width) = (width_of(&r.got_cols, &r.got_rows), width_of(&r.exp_cols, &r.exp_rows));
    let width = got_width.max(exp_width);
    let (gs, es) = align(&r.got_rows, &r.exp_rows, r.ordered);
    let count = |s: &[Aligned], state| s.iter().filter(|a| a.state == state).count();
    let (extra, missing, diff) = (count(&gs, RowState::Extra), count(&es, RowState::Missing), count(&gs, RowState::Diff));
    let (got_total, exp_total) = (r.got_total.unwrap_or(r.got_rows.len()), r.exp_total.unwrap_or(r.exp_rows.len()));

    let mut summary = Vec::new();
    if got_width != exp_width {
        summary.push(if got_width > exp_width { i18n::trf!("you have more columns: {} instead of {}", got_width, exp_width) } else { i18n::trf!("missing columns: {} instead of {}", got_width, exp_width) });
    }
    if got_total != exp_total {
        summary.push(i18n::trf!("you have {} rows, expected {}", got_total, exp_total));
    }
    for (n, text) in [(diff, i18n::tr("rows differ")), (extra, i18n::tr("extra rows")), (missing, i18n::tr("missing rows"))] {
        if n > 0 {
            summary.push(format!("{text}: {n}"));
        }
    }
    if r.ordered {
        summary.push(i18n::tr("row order matters").to_string());
    }

    // the server does not check column names, but it is useful for the student to see the mismatch
    let renamed = !r.exp_cols.is_empty() && r.got_cols.len() == r.exp_cols.len() && r.got_cols.iter().zip(&r.exp_cols).any(|(g, e)| g.to_lowercase() != e.to_lowercase());
    // if the reference has no column names, take the student's
    let exp_cols = if r.exp_cols.is_empty() { &r.got_cols } else { &r.exp_cols };
    Comparison {
        summary,
        got: table_model(width, SideInput { side: Side::Got, cols: &r.got_cols, rows: &r.got_rows, total: got_total, status: &gs, other_rows: &r.exp_rows, other_width: exp_width }),
        exp: table_model(width, SideInput { side: Side::Exp, cols: exp_cols, rows: &r.exp_rows, total: exp_total, status: &es, other_rows: &r.got_rows, other_width: got_width }),
        renamed,
    }
}

// --- components ---------------------------------------------------------------------------------

fn row_view(row: RowModel, n: usize) -> impl IntoView {
    let cells = row.cells.into_iter().map(|c| view! { <td class=c.class>{c.text}</td> }).collect_view();
    view! { <tr class=row.class><td class="sd-n">{n}</td>{cells}</tr> }
}

#[component]
fn SideTable(model: TableModel) -> impl IntoView {
    let width = model.headers.len();
    let head = model.headers.into_iter().map(|h| view! { <th class=h.mark.class() title=h.title>{h.name}</th> }).collect_view();
    let body = if model.rows.is_empty() {
        view! { <tr><td class="sd-empty" colspan={width + 1}>{i18n::tr("empty")}</td></tr> }.into_any()
    } else {
        model.rows.into_iter().enumerate().map(|(i, r)| row_view(r, i + 1)).collect_view().into_any()
    };
    let more = (model.total > model.shown).then(|| view! { <p class="sd-more">{i18n::trf!("Showing the first {} of {} rows.", model.shown, model.total)}</p> });
    view! {
        <div class=format!("sd-side {}", model.side.class())>
            <div class="sd-title">
                <span class="s-label">{model.title}</span>
                <span class="sd-count">{format!("{} {}", model.total, i18n::plural(model.total as u64, "row", "rows"))}</span>
            </div>
            <div class="sd-scroll">
                <table class="sd-t">
                    <thead><tr><th class="sd-n">"#"</th>{head}</tr></thead>
                    <tbody>{body}</tbody>
                </table>
            </div>
            {more}
        </div>
    }
}

/// Two tables side by side - the student's result and the correct one - with differences highlighted and a summary above them.
#[component]
pub fn SqlDiff(rows: RowsView) -> impl IntoView {
    let Comparison { summary, got, exp, renamed } = compare(&rows);
    view! {
        <div class="sd">
            {(!summary.is_empty()).then(|| view! { <p class="sd-sum">{summary.join(" · ")}</p> })}
            <div class="sd-grid">
                <SideTable model=got />
                <SideTable model=exp />
            </div>
            <p class="sd-legend">
                <span class="sd-key extra"></span>{i18n::tr(" an extra or wrong value in your result")}
                <span class="sd-key missing"></span>{i18n::tr(" what is missing or what it should be")}
                {renamed.then(|| view! { <span class="sd-note">{i18n::tr("Column names differ from the reference — the check ignores them.")}</span> })}
            </p>
        </div>
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    fn rows(v: Value) -> Vec<Row> {
        serde_json::from_value(v).unwrap()
    }

    fn states(a: &[Aligned]) -> Vec<RowState> {
        a.iter().map(|x| x.state).collect()
    }

    fn view(got: Value, exp: Value, ordered: bool) -> RowsView {
        let (got, exp) = (rows(got), rows(exp));
        RowsView { ordered, got_total: Some(got.len()), exp_total: Some(exp.len()), got_rows: got, exp_rows: exp, ..RowsView::default() }
    }

    #[test]
    fn equal_tables_have_no_differences_in_both_modes() {
        let t = json!([[1, "a"], [2, "b"]]);
        for ordered in [false, true] {
            let (g, e) = align(&rows(t.clone()), &rows(t.clone()), ordered);
            assert_eq!(states(&g), [RowState::Ok; 2]);
            assert_eq!(states(&e), [RowState::Ok; 2]);
        }
    }

    #[test]
    fn unordered_ignores_row_order_and_counts_duplicates() {
        let (g, e) = align(&rows(json!([[2], [1], [1]])), &rows(json!([[1], [1], [2]])), false);
        assert_eq!(states(&g), [RowState::Ok; 3]);
        assert_eq!(states(&e), [RowState::Ok; 3]);
        // an extra repetition is an extra row, not a match
        let (g, e) = align(&rows(json!([[1], [1], [1]])), &rows(json!([[1], [1]])), false);
        assert_eq!(states(&g), [RowState::Ok, RowState::Ok, RowState::Extra]);
        assert_eq!(states(&e), [RowState::Ok; 2]);
    }

    #[test]
    fn unordered_pairs_leftovers_in_turn_then_marks_the_tail() {
        let (g, e) = align(&rows(json!([[1, "a"], [2, "x"], [9, "z"]])), &rows(json!([[1, "a"], [2, "b"]])), false);
        assert_eq!(states(&g), [RowState::Ok, RowState::Diff, RowState::Extra]);
        assert_eq!(states(&e), [RowState::Ok, RowState::Diff]);
        assert_eq!(g[1].pair, Some(1));
        assert_eq!(e[1].pair, Some(1));
        let (g, e) = align(&rows(json!([[1]])), &rows(json!([[1], [5], [6]])), false);
        assert_eq!(states(&g), [RowState::Ok]);
        assert_eq!(states(&e), [RowState::Ok, RowState::Missing, RowState::Missing]);
    }

    #[test]
    fn ordered_compares_by_position_and_marks_tails() {
        let (g, e) = align(&rows(json!([[2], [1], [7]])), &rows(json!([[1], [1]])), true);
        assert_eq!(states(&g), [RowState::Diff, RowState::Ok, RowState::Extra]);
        assert_eq!(states(&e), [RowState::Diff, RowState::Ok]);
        assert_eq!(g[0].pair, Some(0));
        let (g, e) = align(&rows(json!([[1]])), &rows(json!([[1], [2]])), true);
        assert_eq!(states(&g), [RowState::Ok]);
        assert_eq!(states(&e), [RowState::Ok, RowState::Missing]);
    }

    #[test]
    fn numbers_compare_by_value_and_null_equals_missing() {
        assert!(same(Some(&json!(1)), Some(&json!(1.0))));
        assert!(!same(Some(&json!(1)), Some(&json!("1"))));
        assert!(same(Some(&Value::Null), None));
        let (g, _) = align(&rows(json!([[1.0, null]])), &rows(json!([[1, null]])), false);
        assert_eq!(states(&g), [RowState::Ok]);
    }

    #[test]
    fn cells_of_a_changed_row_are_marked_only_where_values_differ() {
        let c = compare(&view(json!([[1, "x"]]), json!([[1, "b"]]), false));
        let cells = &c.got.rows[0].cells;
        assert_eq!((cells[0].class.as_str(), cells[1].class.as_str()), ("num", "extra"));
        let cells = &c.exp.rows[0].cells;
        assert_eq!((cells[0].class.as_str(), cells[1].class.as_str()), ("num", "missing"));
        assert_eq!(c.got.rows[0].class, "sd-diff");
    }

    #[test]
    fn extra_and_missing_rows_mark_every_cell() {
        let c = compare(&view(json!([[1], [2]]), json!([[1], [3], [4]]), true));
        assert_eq!(c.got.rows[1].class, "sd-diff");
        let c = compare(&view(json!([[1], [2]]), json!([[1]]), true));
        assert_eq!(c.got.rows[1].class, "sd-extra");
        assert_eq!(c.got.rows[1].cells[0].class, "extra num");
        let c = compare(&view(json!([[1]]), json!([[1], ["x"]]), true));
        assert_eq!(c.exp.rows[1].cells[0].class, "missing");
    }

    #[test]
    fn missing_columns_are_marked_in_the_headers_and_cells_stay_empty() {
        let mut v = view(json!([[1]]), json!([[1, "a"]]), false);
        v.got_cols = vec!["id".into()];
        v.exp_cols = vec!["id".into(), "name".into()];
        let c = compare(&v);
        // the student has no second column: the header is positional, and the missing column of the reference is marked
        assert_eq!(c.got.headers.len(), 2);
        assert_eq!(c.got.headers[1].name, "col2");
        assert_eq!(c.exp.headers[1].mark, Mark::Missing);
        assert_eq!(c.exp.headers[1].title, Some("this column is missing from your result"));
        assert_eq!(c.got.headers[0].mark, Mark::None);
        assert_eq!(c.got.rows[0].cells[1].text, "");
        assert!(c.summary.contains(&"missing columns: 1 instead of 2".to_string()));
        // a column that is extra for the student
        let c = compare(&view(json!([[1, 2]]), json!([[1]]), false));
        assert_eq!(c.got.headers[1].mark, Mark::Extra);
        assert_eq!(c.got.headers[1].title, Some("extra column"));
        assert!(c.summary.contains(&"you have more columns: 2 instead of 1".to_string()));
    }

    #[test]
    fn summary_lists_counts_and_ordering() {
        let c = compare(&view(json!([[1], [2], [9]]), json!([[1], [3]]), true));
        assert_eq!(c.summary, ["you have 3 rows, expected 2", "rows differ: 1", "extra rows: 1", "row order matters"]);
        let c = compare(&view(json!([[1]]), json!([[1]]), false));
        assert!(c.summary.is_empty());
    }

    #[test]
    fn totals_beyond_the_shown_rows_are_kept() {
        let mut v = view(json!([[1]]), json!([[1]]), false);
        v.got_total = Some(250);
        let c = compare(&v);
        assert_eq!((c.got.total, c.got.shown), (250, 1));
        assert!(c.summary.iter().any(|s| s == "you have 250 rows, expected 1"));
    }

    #[test]
    fn renamed_columns_are_noticed_case_insensitively() {
        let mut v = view(json!([[1]]), json!([[1]]), false);
        v.got_cols = vec!["ID".into()];
        v.exp_cols = vec!["id".into()];
        assert!(!compare(&v).renamed);
        v.got_cols = vec!["number".into()];
        assert!(compare(&v).renamed);
        // reference without names - nothing to compare, headers are taken from the student
        v.exp_cols.clear();
        let c = compare(&v);
        assert!(!c.renamed);
        assert_eq!(c.exp.headers[0].name, "number");
    }

    #[test]
    fn headers_fall_back_to_positional_names() {
        let c = compare(&view(json!([[1, 2]]), json!([[1, 2]]), false));
        assert_eq!(c.got.headers.iter().map(|h| h.name.as_str()).collect::<Vec<_>>(), ["col1", "col2"]);
    }

    #[test]
    fn empty_results_do_not_panic() {
        let c = compare(&RowsView::default());
        assert!(c.summary.is_empty() && c.got.rows.is_empty() && c.got.headers.is_empty());
    }
}
