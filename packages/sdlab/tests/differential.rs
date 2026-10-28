//! Differential tests: `evaluate` and `check_goals` match the golden results of the TypeScript engine.

mod common;

use sdlab::import::{Case, CaseState};
use sdlab::layout::place;
use sdlab::ports::{suggest_edges, AUTO_RADIUS};
use sdlab::{check_goals, evaluate, EvalResult, Task};

const TOL: f64 = 1e-9;

fn opt_close(name: &str, a: Option<f64>, b: Option<f64>, ctx: &str) {
    match (a, b) {
        (None, None) => {}
        (Some(x), Some(y)) => assert!(common::close(x, y, TOL), "{ctx}: {name}: {x} vs {y}"),
        _ => panic!("{ctx}: {name}: {a:?} vs {b:?}"),
    }
}

fn compare(got: &EvalResult, want: &EvalResult, ctx: &str) {
    for (name, a, b) in [
        ("p50", got.p50, want.p50),
        ("p99", got.p99, want.p99),
        ("success", got.success, want.success),
        ("availability", got.availability, want.availability),
        ("cost", got.cost, want.cost),
    ] {
        assert!(common::close(a, b, TOL), "{ctx}: {name}: {a} vs {b}");
    }
    opt_close("hit", got.hit, want.hit, ctx);
    opt_close("cdn_hit", got.cdn_hit, want.cdn_hit, ctx);
    opt_close("lag_sec", got.lag_sec, want.lag_sec, ctx);
    opt_close("replica_lag_ms", got.replica_lag_ms, want.replica_lag_ms, ctx);
    opt_close("max_shard_share", got.max_shard_share, want.max_shard_share, ctx);
    assert_eq!(got.entry, want.entry, "{ctx}: entry");
    assert_eq!(got.warnings, want.warnings, "{ctx}: warnings");
    let ids = |r: &EvalResult| r.loads.iter().map(|(id, _)| id.to_owned()).collect::<Vec<_>>();
    assert_eq!(ids(got), ids(want), "{ctx}: order and set of loads");
    for ((id, a), (_, b)) in got.loads.iter().zip(want.loads.iter()) {
        for (name, x, y) in [("load", a.load, b.load), ("cap", a.cap, b.cap), ("util", a.util, b.util), ("units", a.units, b.units)] {
            assert!(common::close(x, y, TOL), "{ctx}: loads[{id}].{name}: {x} vs {y}");
        }
        assert_eq!(a.status, b.status, "{ctx}: loads[{id}].status");
        assert_eq!(a.note, b.note, "{ctx}: loads[{id}].note");
    }
}

fn run_case(task: &Task, c: &Case, count: &mut usize) {
    let ctx = format!("{} / {}", task.id, c.label);
    let state = match &c.state {
        CaseState::Ref(r) if r == "start" => task.spec.start.clone(),
        CaseState::Ref(r) if r == "solution" => task.spec.solution.clone(),
        CaseState::Ref(r) => panic!("{ctx}: unknown reference {r}"),
        CaseState::Inline(s) => {
            let mut s = s.clone();
            s.normalize();
            s
        }
    };
    let wl = c.workload.as_ref().unwrap_or(&task.spec.workload);
    let got = evaluate(&state, wl, &c.opts);
    compare(&got, &c.result, &ctx);
    if let Some(goals) = &c.goals {
        let got_goals = check_goals(&state, wl, &task.spec.goals, None);
        assert_eq!(got_goals.len(), goals.len(), "{ctx}: goal count");
        for (i, (g, w)) in got_goals.iter().zip(goals).enumerate() {
            assert_eq!(g, w, "{ctx}: goal {i}");
        }
    }
    *count += 1;
}

#[test]
fn evaluate_and_goals_match_typescript() {
    locales::set_locale(i18n::Locale::Ru);
    let chapters = common::chapters();
    let golden = common::golden();
    assert_eq!(chapters.len(), golden.len());
    let mut count = 0;
    for (ch, g) in chapters.iter().zip(&golden) {
        assert_eq!((ch.book, ch.chapter), (g.book, g.chapter));
        assert_eq!(ch.tasks.len(), g.tasks.len());
        for (task, gt) in ch.tasks.iter().zip(&g.tasks) {
            assert_eq!(task.id, gt.id);
            for c in &gt.cases {
                run_case(task, c, &mut count);
            }
        }
    }
    assert!(count > 2000, "golden cases: {count}");
    eprintln!("golden cases matched: {count}");
}

/// Node positions of the starting designs in the data were produced by the TypeScript `place`; the Rust version must give the same.
#[test]
fn layout_matches_typescript() {
    locales::set_locale(i18n::Locale::Ru);
    for ch in common::chapters() {
        for t in &ch.tasks {
            for (name, s) in [("start", &t.spec.start), ("solution", &t.spec.solution)] {
                // no positions — lay out; those that existed must not move on a repeated layout
                let mut blank = s.clone();
                for n in &mut blank.nodes {
                    n.x = -1.0;
                    n.y = -1.0;
                }
                let placed = place(&blank);
                for (a, b) in placed.nodes.iter().zip(&s.nodes) {
                    // positions in the data may have been shifted by hand in the scenario; compare only the auto-placed ones
                    assert!(common::close(a.x, b.x, 0.0) && common::close(a.y, b.y, 0.0), "{} {name}: node {}: ({}, {}) vs ({}, {})", t.id, a.id, a.x, a.y, b.x, b.y);
                }
                assert_eq!(&place(s), s, "{} {name}: re-placing changes the diagram", t.id);
            }
        }
    }
}

#[test]
fn suggest_edges_match_typescript() {
    locales::set_locale(i18n::Locale::Ru);
    let chapters = common::chapters();
    let golden = common::golden();
    let mut count = 0;
    for (ch, g) in chapters.iter().zip(&golden) {
        for (task, gt) in ch.tasks.iter().zip(&g.tasks) {
            for s in &gt.suggest {
                let n = task.spec.solution.node(&s.node).expect("reference node");
                let stripped = sdlab::SdState {
                    nodes: task.spec.solution.nodes.clone(),
                    edges: task.spec.solution.edges.iter().filter(|e| e.from != n.id && e.to != n.id).cloned().collect(),
                };
                let got = suggest_edges(&stripped, n, &[], AUTO_RADIUS);
                assert_eq!(got, s.edges, "{} / auto-links of node {}", task.id, s.node);
                count += 1;
            }
        }
    }
    assert!(count > 300, "auto-link cases: {count}");
}
