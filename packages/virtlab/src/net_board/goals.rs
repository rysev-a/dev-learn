//! Goals and scenarios of the network board.

use serde::{Deserialize, Serialize};

use super::eval::{ping, published};
use super::{evaluate, problems, Evaluation, IfaceStatus, Kind, Topology};
use crate::goal::Goal;

/// A condition on the board that the scenario wants.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum NetGoal {
    /// A ping from one host to another goes through (namespaces, VMs and the outside network are hosts).
    Ping {
        /// Sender identifier.
        from: String,
        /// Receiver identifier.
        to: String,
    },
    /// A ping from one host to another does not go through (isolation).
    NoPing {
        /// Sender identifier.
        from: String,
        /// Receiver identifier.
        to: String,
    },
    /// The outside network reaches the host (or interface) a DNAT rule publishes.
    Published {
        /// Outside network identifier.
        external: String,
        /// Target of the DNAT rule.
        target: String,
    },
    /// After the loss of an object (a NIC that failed, a cable pulled out) the ping still goes through.
    SurviveLoss {
        /// The object that is lost.
        node: String,
        /// Sender identifier.
        from: String,
        /// Receiver identifier.
        to: String,
    },
    /// Every interface has a link.
    Healthy,
    /// At least this many objects of the kind.
    Has {
        /// Kind.
        node: Kind,
        /// Minimum.
        min: u32,
    },
    /// At most this many objects of the kind.
    AtMost {
        /// Kind.
        node: Kind,
        /// Maximum.
        max: u32,
    },
    /// No object of the kind.
    Lacks {
        /// Kind.
        node: Kind,
    },
    /// The object has the parameter value (`param_text` of the object: the default counts).
    ParamOf {
        /// Object identifier.
        id: String,
        /// Parameter.
        key: String,
        /// Value as text.
        value: String,
    },
    /// The link `from → to` exists (the direction of the model: see [`rel`](super::rel)).
    Linked {
        /// Source identifier.
        from: String,
        /// Target identifier.
        to: String,
    },
}

/// Verdict on one goal.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct GoalResult {
    /// The goal holds.
    pub ok: bool,
    /// The goal text.
    pub text: String,
}

/// The name of an object on the board, or its identifier when the board has no such object.
fn nm(t: &Topology, id: &str) -> String {
    t.node(id).map_or_else(|| id.to_string(), |n| n.name.clone())
}

impl NetGoal {
    /// The goal as a sentence (objects are named by their identifiers; see [`NetGoal::describe_for`]).
    pub fn describe(&self) -> String {
        self.describe_for(&Topology::default())
    }

    /// The goal as a sentence; the objects it names are shown by their names on the board.
    pub fn describe_for(&self, t: &Topology) -> String {
        match self {
            NetGoal::Ping { from, to } => i18n::trf!("“{0}” can ping “{1}”", nm(t, from), nm(t, to)),
            NetGoal::NoPing { from, to } => i18n::trf!("“{0}” cannot ping “{1}” (they are isolated)", nm(t, from), nm(t, to)),
            NetGoal::Published { external, target } => i18n::trf!("“{0}” reaches the published port of “{1}”", nm(t, external), nm(t, target)),
            NetGoal::SurviveLoss { node, from, to } => {
                i18n::trf!("if “{0}” is lost, “{1}” can still ping “{2}”", nm(t, node), nm(t, from), nm(t, to))
            }
            NetGoal::Healthy => i18n::tr("every interface is up and has a link").to_string(),
            NetGoal::Has { node, min } => i18n::trf!("at least {0} × {1}", min, node.label()),
            NetGoal::AtMost { node, max } => i18n::trf!("at most {0} × {1}", max, node.label()),
            NetGoal::Lacks { node } => i18n::trf!("no {0}", node.label()),
            NetGoal::ParamOf { id, key, value } => i18n::trf!("“{0}” has {1} = {2}", nm(t, id), key, value),
            NetGoal::Linked { from, to } => i18n::trf!("“{0}” → “{1}” are linked", nm(t, from), nm(t, to)),
        }
    }

    /// The goal holds on the board.
    pub fn check(&self, t: &Topology, ev: &Evaluation) -> bool {
        let count = |k: Kind| t.of_kind(k).count() as u64;
        match self {
            NetGoal::Ping { from, to } => ping(t, ev, from, to).ok(),
            NetGoal::NoPing { from, to } => !ping(t, ev, from, to).ok(),
            NetGoal::Published { external, target } => published(t, ev, external, target).ok(),
            NetGoal::SurviveLoss { node, from, to } => {
                let after = t.without(node);
                let ev_after = evaluate(&after);
                ping(&after, &ev_after, from, to).ok()
            }
            NetGoal::Healthy => !ev.ifaces.is_empty() && ev.ifaces.iter().all(|i| i.status == IfaceStatus::Ok),
            NetGoal::Has { node, min } => count(*node) >= u64::from(*min),
            NetGoal::AtMost { node, max } => count(*node) <= u64::from(*max),
            NetGoal::Lacks { node } => count(*node) == 0,
            NetGoal::ParamOf { id, key, value } => t.node(id).is_some_and(|n| &n.param_text(key) == value),
            NetGoal::Linked { from, to } => t.linked(from, to),
        }
    }
}

fn default_max_nodes() -> u32 {
    28
}

/// One exercise of the board: a story, a starting board and the goals.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Scenario {
    /// Identifier (the key of the solution).
    pub id: String,
    /// Title (an English key; shown with `tr_dyn`).
    pub title: String,
    /// What is going on.
    pub story: String,
    /// What the student has to achieve, in a sentence.
    pub goal: String,
    /// A hint.
    pub hint: String,
    /// Kinds the student may add.
    pub palette: Vec<Kind>,
    /// The most objects on the board.
    #[serde(default = "default_max_nodes")]
    pub max_nodes: u32,
    /// The board at the start.
    pub start: Topology,
    /// Goals; all must hold.
    pub goals: Vec<NetGoal>,
}

impl Scenario {
    /// The scenario as an exercise goal.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.title.clone())
    }

    /// The board evaluated.
    pub fn evaluate(&self, t: &Topology) -> Evaluation {
        evaluate(t)
    }

    /// Results of every goal on the board.
    pub fn results(&self, t: &Topology) -> Vec<GoalResult> {
        let ev = self.evaluate(t);
        self.goals.iter().map(|g| GoalResult { ok: g.check(t, &ev), text: g.describe_for(t) }).collect()
    }

    /// Why the board cannot be accepted at all (broken rules, kinds outside the palette, too many objects).
    pub fn invalid(&self, t: &Topology) -> Option<String> {
        if let Some(p) = problems(t).into_iter().next() {
            return Some(p.text);
        }
        if t.nodes.len() > self.max_nodes as usize {
            return Some(i18n::trf!("at most {0} objects are allowed", self.max_nodes));
        }
        for n in &t.nodes {
            let from_start = self.start.node(&n.id).is_some_and(|s| s.kind == n.kind);
            if !from_start && !self.palette.contains(&n.kind) {
                return Some(i18n::trf!("“{0}” is not available in this exercise", n.kind.label()));
            }
        }
        None
    }

    /// The board is acceptable and every goal holds.
    pub fn reached(&self, t: &Topology) -> bool {
        self.invalid(t).is_none() && self.results(t).iter().all(|r| r.ok)
    }
}
