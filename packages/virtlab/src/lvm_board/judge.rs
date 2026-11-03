//! Judging a board produced by the student's code (the Python tasks of level 3: `fix(board)` returns the repaired board).
//!
//! The code runs in the worker sandbox; the backend gets the board it printed and asks the model whether the scenario is solved. The scenario is the
//! starting board, the workload and the goals of a pack, so the verdict is the same as for a board built by hand.

use super::{pack, GoalResult, Scenario, Topology};

/// The verdict on a board.
#[derive(Clone, Debug, PartialEq)]
pub struct Judgement {
    /// The board is acceptable and every goal holds.
    pub reached: bool,
    /// Why the board is not acceptable at all (broken rules, other objects than the starting ones).
    pub invalid: Option<String>,
    /// The goals and whether each holds.
    pub goals: Vec<GoalResult>,
}

/// The scenario `scenario` of the pack `pack_id`.
pub fn find(pack_id: &str, scenario: &str) -> Option<Scenario> {
    pack(pack_id)?.0.into_iter().find(|s| s.id == scenario)
}

/// Judges the board given as JSON (`{nodes, edges}`, positions optional). The objects must be the ones of the starting board: the code repairs the links
/// and the parameters, it does not invent a new environment.
pub fn judge(pack_id: &str, scenario: &str, board_json: &str) -> Result<Judgement, String> {
    let sc = find(pack_id, scenario).ok_or_else(|| format!("unknown scenario {pack_id}/{scenario}"))?;
    let board: Topology = serde_json::from_str(board_json).map_err(|e| format!("not a board: {e}"))?;
    let same = board.nodes.len() == sc.start.nodes.len()
        && board.nodes.iter().all(|n| sc.start.node(&n.id).is_some_and(|s| s.kind == n.kind));
    let invalid = if same { sc.invalid(&board) } else { Some("The board must keep the objects it started with".to_string()) };
    let goals = sc.results(&board);
    Ok(Judgement { reached: invalid.is_none() && goals.iter().all(|g| g.ok), invalid, goals })
}
