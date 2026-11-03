//! Python tasks whose answer is a board (book 17 the oVirt board, book 19 the LVM and the Linux network boards): the student's `fix(board)` runs in the
//! worker sandbox, the hidden driver prints the repaired board, one JSON line per scenario, and the model decides whether the scenario is solved
//! (`virtlab::{ovirt_topo,lvm_board,net_board}::judge`). The worker only runs the code; the verdict is made here, so it is the same as for a board built by hand.
//!
//! The task keys in `spec`: `board_check` — the list of `{pack, scenario}` the boards belong to (one printed line per entry), `board_view` — the boards of
//! the tests are shown beside the results (level 2, the answer is plain data), `board_kind` — which model the boards of a `board_view` task belong to
//! (`ovirt_topo` by default, `lvm_board`, `net_board`; the kind of a `board_check` task follows from its packs).

use serde_json::{json, Value};

/// The `{pack, scenario}` pairs of a level-3 task, in the order of the printed boards.
pub fn checks(task: &Value) -> Vec<(String, String)> {
    task.get("board_check")
        .and_then(Value::as_array)
        .map(|a| a.iter().filter_map(|c| Some((c.get("pack")?.as_str()?.to_string(), c.get("scenario")?.as_str()?.to_string()))).collect())
        .unwrap_or_default()
}

/// The board model a pack belongs to.
fn kind_of_pack(pack: &str) -> &'static str {
    if pack == virtlab::lvm_board::FIX_PACK || virtlab::lvm_board::pack_ids().contains(&pack) {
        "lvm_board"
    } else if pack == virtlab::net_board::FIX_PACK || virtlab::net_board::pack_ids().contains(&pack) {
        "net_board"
    } else {
        "ovirt_topo"
    }
}

/// The board model of a task: its packs decide, otherwise the `board_kind` key (the oVirt board by default).
pub fn kind(task: &Value) -> &'static str {
    if let Some((pack, _)) = checks(task).first() {
        return kind_of_pack(pack);
    }
    match task.get("board_kind").and_then(Value::as_str) {
        Some("lvm_board") => "lvm_board",
        Some("net_board") => "net_board",
        _ => "ovirt_topo",
    }
}

/// The verdict of the model of `pack` on a printed board: (reached, why the board is invalid).
fn judge_board(pack: &str, scenario: &str, line: &str) -> Result<(bool, Option<String>), String> {
    match kind_of_pack(pack) {
        "lvm_board" => virtlab::lvm_board::judge(pack, scenario, line).map(|j| (j.reached, j.invalid)),
        "net_board" => virtlab::net_board::judge(pack, scenario, line).map(|j| (j.reached, j.invalid)),
        _ => virtlab::ovirt_topo::judge(pack, scenario, line).map(|j| (j.reached, j.invalid)),
    }
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
    Some(json!({ "kind": kind(task), "boards": boards, "checks": checks.iter().map(|(p, s)| json!({ "pack": p, "scenario": s })).collect::<Vec<_>>() }))
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
        .map(|((pack, scenario), line)| match judge_board(pack, scenario, line) {
            Ok((reached, invalid)) => json!({ "ok": reached, "board": serde_json::from_str::<Value>(line).unwrap_or(Value::Null), "error": invalid }),
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
    fn the_kind_follows_the_packs_or_the_key() {
        assert_eq!(kind(&task()), "ovirt_topo");
        assert_eq!(kind(&json!({ "board_check": [{ "pack": "virt-sim-lvm-grow", "scenario": "extend" }] })), "lvm_board");
        assert_eq!(kind(&json!({ "board_check": [{ "pack": "virt-sim-net-nat", "scenario": "build" }] })), "net_board");
        assert_eq!(kind(&json!({ "board_view": true, "board_kind": "net_board" })), "net_board");
        assert_eq!(kind(&json!({ "board_view": true })), "ovirt_topo");
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
