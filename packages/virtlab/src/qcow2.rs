//! qcow2 layer chain model (chapter 9).
//!
//! The chain is a vector of layers from the top one (current, all writes go there) to the base. A read goes down to the first layer
//! that has the cluster; each layer check is a table lookup. A snapshot is a new empty top layer. Merging (commit)
//! moves the top layer's clusters into the one below. Rollback discards the top layer.
//!
//! Goals depend on the action history ([`Qcow2Rule`]): deep read, chain shortening, write rollback. The history is kept by
//! [`Session`] (same as `Qcow2Lab.tsx`); for server-side re-checking actions are recorded as [`Action`]
//! and replayed by [`replay`].

use std::collections::BTreeMap;

use serde::{Deserialize, Serialize};

use crate::goal::Goal;

/// Number of clusters in the exercise.
pub const CLUSTERS: u32 = 8;

/// Layer: clusters allocated in it (number → data).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Layer {
    /// Layer name.
    pub name: String,
    /// Allocated clusters.
    pub data: BTreeMap<u32, String>,
}

/// Chain of a single base layer with clusters `base`.
pub fn initial_chain(base: &BTreeMap<u32, String>) -> Vec<Layer> {
    vec![Layer { name: i18n::tr("base").into(), data: base.clone() }]
}

/// Snapshot: an empty layer "layer n" is added on top.
pub fn snapshot(chain: &[Layer], n: u32) -> Vec<Layer> {
    let mut v = Vec::with_capacity(chain.len() + 1);
    v.push(Layer { name: i18n::trf!("layer {0}", n), data: BTreeMap::new() });
    v.extend_from_slice(chain);
    v
}

/// Write data `d` to cluster `c`: goes to the top layer; `copy_up` — the cluster already existed below or above (copy-on-write).
pub fn write(chain: &[Layer], c: u32, d: &str) -> (Vec<Layer>, bool) {
    let Some((top, rest)) = chain.split_first() else {
        return (vec![], false);
    };
    let below = rest.iter().any(|l| l.data.contains_key(&c)) || top.data.contains_key(&c);
    let mut top = top.clone();
    top.data.insert(c, d.to_string());
    let mut v = Vec::with_capacity(chain.len());
    v.push(top);
    v.extend_from_slice(rest);
    (v, below)
}

/// Result of reading a cluster.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct ReadResult {
    /// Data (absent in every layer — zeros are read, `None`).
    pub value: Option<String>,
    /// Depth of the layer where the cluster was found (0 — top).
    pub depth: Option<usize>,
    /// Layer table lookups.
    pub lookups: usize,
    /// Name of the layer where the cluster was found.
    pub layer: Option<String>,
}

/// Read cluster `c` down the chain.
pub fn read(chain: &[Layer], c: u32) -> ReadResult {
    for (i, l) in chain.iter().enumerate() {
        if let Some(v) = l.data.get(&c) {
            return ReadResult { value: Some(v.clone()), depth: Some(i), lookups: i + 1, layer: Some(l.name.clone()) };
        }
    }
    ReadResult { value: None, depth: None, lookups: chain.len(), layer: None }
}

/// Merge: the top layer's clusters move into the one below; `None` — there is only one layer.
pub fn commit(chain: &[Layer]) -> Option<Vec<Layer>> {
    if chain.len() < 2 {
        return None;
    }
    let mut next = chain[1].clone();
    for (k, v) in &chain[0].data {
        next.data.insert(*k, v.clone());
    }
    let mut v = Vec::with_capacity(chain.len() - 1);
    v.push(next);
    v.extend_from_slice(&chain[2..]);
    Some(v)
}

/// Rollback: the top layer is discarded; `None` — there is only one layer.
pub fn revert(chain: &[Layer]) -> Option<Vec<Layer>> {
    if chain.len() < 2 {
        return None;
    }
    Some(chain[1..].to_vec())
}

/// Goal rule.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum Qcow2Rule {
    /// Read a found cluster with a chain at least `min_chain` long, and the read costs at least `min_lookups` lookups.
    Deep {
        /// Minimum chain length at the time of the read.
        min_chain: usize,
        /// Minimum table lookups.
        min_lookups: usize,
    },
    /// The chain was once at least `min_chain` long, and after merging became at most `max_after`.
    Squash {
        /// Minimum peak chain length during the session.
        min_chain: usize,
        /// Chain length after merging at most.
        max_after: usize,
    },
    /// Write a cluster to the top layer, roll the layer back and read that cluster: the data is now different.
    Rollback,
}

/// Exercise goal.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Qcow2Goal {
    /// Goal identifier.
    pub id: String,
    /// Goal text.
    pub text: String,
    /// Rule.
    pub rule: Qcow2Rule,
}

impl Qcow2Goal {
    /// Goal for display.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.text.clone())
    }
}

/// Student action.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "op", rename_all = "snake_case")]
pub enum Action {
    /// Snapshot.
    Snapshot,
    /// Write data to a cluster.
    Write {
        /// Cluster number.
        cluster: u32,
        /// Data.
        data: String,
    },
    /// Read a cluster.
    Read {
        /// Cluster number.
        cluster: u32,
    },
    /// Merge the top layer.
    Commit,
    /// Roll back the top layer.
    Revert,
}

/// What happened on the action (for the caption under the diagram).
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Note {
    /// Snapshot taken.
    Snapshot,
    /// Write done; `copy_up` — the cluster existed in some layer (copy-on-write).
    Write {
        /// Copy-on-write.
        copy_up: bool,
    },
    /// Read done.
    Read(ReadResult),
    /// Merge done.
    Committed,
    /// Merge impossible: only one layer.
    CommitImpossible,
    /// Rollback done; `had_data` — the discarded layer had writes.
    Reverted {
        /// The discarded layer had writes.
        had_data: bool,
    },
    /// Rollback impossible: only one layer.
    RevertImpossible,
}

/// Exercise progress: layer chain, bookkeeping counters and achieved goals — as in `Qcow2Lab.tsx`.
#[derive(Clone, Debug)]
pub struct Session {
    goals: Vec<Qcow2Goal>,
    chain: Vec<Layer>,
    max_len: usize,
    snaps: u32,
    dropped: Option<BTreeMap<u32, String>>,
    done: Vec<String>,
}

impl Session {
    /// New exercise: base layer with clusters `base`.
    pub fn new(base: &BTreeMap<u32, String>, goals: &[Qcow2Goal]) -> Session {
        Session { goals: goals.to_vec(), chain: initial_chain(base), max_len: 1, snaps: 0, dropped: None, done: vec![] }
    }

    /// Layer chain (top first).
    pub fn chain(&self) -> &[Layer] {
        &self.chain
    }

    /// Peak chain length during the session.
    pub fn max_len(&self) -> usize {
        self.max_len
    }

    /// Identifiers of achieved goals (in order of achievement).
    pub fn done(&self) -> &[String] {
        &self.done
    }

    /// Whether all goals are achieved.
    pub fn solved(&self) -> bool {
        self.goals.iter().all(|g| self.done.contains(&g.id))
    }

    fn mark(&mut self, pred: impl Fn(&Qcow2Rule) -> bool) {
        for g in &self.goals {
            if pred(&g.rule) && !self.done.contains(&g.id) {
                self.done.push(g.id.clone());
            }
        }
    }

    fn set_chain(&mut self, c: Vec<Layer>) {
        self.max_len = self.max_len.max(c.len());
        self.chain = c;
    }

    /// Snapshot.
    pub fn snapshot(&mut self) -> Note {
        self.snaps += 1;
        let c = snapshot(&self.chain, self.snaps);
        self.set_chain(c);
        Note::Snapshot
    }

    /// Write.
    pub fn write(&mut self, cluster: u32, data: &str) -> Note {
        let (c, copy_up) = write(&self.chain, cluster, data);
        self.set_chain(c);
        Note::Write { copy_up }
    }

    /// Read.
    pub fn read(&mut self, cluster: u32) -> Note {
        let r = read(&self.chain, cluster);
        let len = self.chain.len();
        if r.value.is_some() {
            let lookups = r.lookups;
            self.mark(|rule| matches!(rule, Qcow2Rule::Deep { min_chain, min_lookups } if lookups >= *min_lookups && len >= *min_chain));
        }
        // rollback is confirmed if a cluster written to the discarded layer now reads differently (or not at all)
        if let Some(d) = &self.dropped {
            if let Some(old) = d.get(&cluster) {
                if r.value.as_ref() != Some(old) {
                    self.mark(|rule| matches!(rule, Qcow2Rule::Rollback));
                    self.dropped = None;
                }
            }
        }
        Note::Read(r)
    }

    /// Merge the top layer.
    pub fn commit(&mut self) -> Note {
        let Some(c) = commit(&self.chain) else {
            return Note::CommitImpossible;
        };
        self.set_chain(c);
        let (max_len, len) = (self.max_len, self.chain.len());
        self.mark(|rule| matches!(rule, Qcow2Rule::Squash { min_chain, max_after } if max_len >= *min_chain && len <= *max_after));
        Note::Committed
    }

    /// Roll back the top layer.
    pub fn revert(&mut self) -> Note {
        let Some(c) = revert(&self.chain) else {
            return Note::RevertImpossible;
        };
        let top = &self.chain[0].data;
        let had_data = !top.is_empty();
        self.dropped = if had_data { Some(top.clone()) } else { None };
        self.set_chain(c);
        Note::Reverted { had_data }
    }

    /// Perform a recorded action.
    pub fn act(&mut self, a: &Action) -> Note {
        match a {
            Action::Snapshot => self.snapshot(),
            Action::Write { cluster, data } => self.write(*cluster, data),
            Action::Read { cluster } => self.read(*cluster),
            Action::Commit => self.commit(),
            Action::Revert => self.revert(),
        }
    }
}

/// Replay recorded actions and return the achieved goals.
pub fn replay(base: &BTreeMap<u32, String>, goals: &[Qcow2Goal], actions: &[Action]) -> Vec<String> {
    let mut s = Session::new(base, goals);
    for a in actions {
        s.act(a);
    }
    s.done
}

/// Default base clusters: 0–3 = A–D.
pub fn default_base() -> BTreeMap<u32, String> {
    [(0, "A"), (1, "B"), (2, "C"), (3, "D")].into_iter().map(|(k, v)| (k, v.to_string())).collect()
}

/// Default goals (chapter 9 exercise).
pub fn default_goals() -> Vec<Qcow2Goal> {
    vec![
        Qcow2Goal {
            id: "deep".into(),
            text: i18n::tr("Read a cluster from the base with a chain of 4 or more layers: the read costs 4 or more lookups").into(),
            rule: Qcow2Rule::Deep { min_chain: 4, min_lookups: 4 },
        },
        Qcow2Goal {
            id: "squash".into(),
            text: i18n::tr("Merge the layers (commit) so that the 4-layer chain shrinks to two").into(),
            rule: Qcow2Rule::Squash { min_chain: 4, max_after: 2 },
        },
        Qcow2Goal {
            id: "rollback".into(),
            text: i18n::tr("Write a cluster to the top layer, roll the layer back — and make sure the old data is back").into(),
            rule: Qcow2Rule::Rollback,
        },
    ]
}
