//! Python tasks whose answer is a board (book 17, the oVirt board): the student's `fix(board)` runs in the worker sandbox, the hidden driver prints the
//! repaired board, one JSON line per scenario, and the model decides whether the scenario is solved (`virtlab::ovirt_topo::judge`). The worker only runs the
//! code; the verdict is made here, so it is the same as for a board built by hand.
//!
//! The task keys in `spec`: `board_check` — the list of `{pack, scenario}` the boards belong to (one printed line per entry), `board_view` — the boards of
//! the tests are shown beside the results (level 2, the answer is plain data).

use serde_json::{json, Value};

/// The `{pack, scenario}` pairs of a level-3 task, in the order of the printed boards.
pub fn checks(task: &Value) -> Vec<(String, String)> {
    task.get("board_check")
        .and_then(Value::as_array)
        .map(|a| a.iter().filter_map(|c| Some((c.get("pack")?.as_str()?.to_string(), c.get("scenario")?.as_str()?.to_string()))).collect())
        .unwrap_or_default()
}

/// What the interface shows of a task: the boards of the tests (level 2) and the scenarios to judge (level 3).
pub fn view(task: &Value) -> Option<Value> {
    let checks = checks(task);
    let boards: Vec<Value> = if task.get("board_view").and_then(Value::as_bool) == Some(true) {
        task.get("tests").and_then(Value::as_array).map(|t| t.iter().filter_map(|t| t.get("args")?.as_array()?.first().cloned()).collect()).unwrap_or_default()
    } else {
        Vec::new()
    };
    if checks.is_empty() && boards.is_empty() {
        return None;
    }
    Some(json!({ "boards": boards, "checks": checks.iter().map(|(p, s)| json!({ "pack": p, "scenario": s })).collect::<Vec<_>>() }))
}

/// Replaces the worker's text comparison by the verdicts of the model: one result per scenario, with the printed board. A run that did not print a board
/// for every scenario (a crash, a timeout) keeps the worker's result.
pub fn judge(task: &Value, result: &mut Value) {
    let checks = checks(task);
    if checks.is_empty() || result["status"] != "ok" {
        return;
    }
    let printed = result["results"].as_array().and_then(|r| r.first()).and_then(|r| r["got"].as_str()).unwrap_or("").to_string();
    let lines: Vec<&str> = printed.lines().map(str::trim).filter(|l| !l.is_empty()).collect();
    if lines.len() != checks.len() {
        return;
    }
    let items: Vec<Value> = checks
        .iter()
        .zip(&lines)
        .map(|((pack, scenario), line)| match virtlab::ovirt_topo::judge(pack, scenario, line) {
            Ok(j) => json!({ "ok": j.reached, "board": serde_json::from_str::<Value>(line).unwrap_or(Value::Null), "error": j.invalid }),
            Err(e) => json!({ "ok": false, "error": e }),
        })
        .collect();
    result["results"] = Value::Array(items);
}

#[cfg(test)]
mod tests {
    use super::*;

    fn task() -> Value {
        json!({ "board_check": [{ "pack": "virt-sim-ovirt-storage-2", "scenario": "no-connection" }] })
    }

    #[test]
    fn a_crash_keeps_the_workers_result() {
        let mut r = json!({ "status": "ok", "results": [{ "ok": false, "got": "", "error": "NameError" }] });
        judge(&task(), &mut r);
        assert_eq!(r["results"][0]["error"], "NameError");
    }

    #[test]
    fn the_unrepaired_board_is_not_accepted_and_the_reference_is() {
        let (scs, sol) = virtlab::ovirt_topo::pack("virt-sim-ovirt-storage-2").unwrap();
        let sc = scs.iter().find(|s| s.id == "no-connection").unwrap();
        for (board, want) in [(&sc.start, false), (&sol["no-connection"], true)] {
            let mut r = json!({ "status": "ok", "results": [{ "ok": false, "got": serde_json::to_string(board).unwrap() }] });
            judge(&task(), &mut r);
            assert_eq!(r["results"][0]["ok"], want);
            assert!(r["results"][0]["board"].is_object());
        }
    }
}
