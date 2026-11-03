//! Which objects may be linked and what a link means; the checks of the board state.

use std::collections::BTreeMap;

use super::{param_error, Edge, Kind, Topology, MAX_NAME, MAX_NODES};

/// Relation a link stands for. The direction follows the table in [`rel`].
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Rel {
    /// The engine manages a data center.
    Manages,
    /// A data center contains a cluster.
    Contains,
    /// A cluster has a host as a member.
    Member,
    /// A host runs a VM.
    Runs,
    /// A network is defined in a data center.
    Defined,
    /// A network is attached to a cluster.
    Attached,
    /// A network is assigned to a NIC of a host.
    Assigned,
    /// The engine has a NIC in a network.
    EngineNic,
    /// A storage domain is attached to a data center.
    Domain,
    /// A host sees (is connected to) a storage domain.
    Sees,
    /// A VM has a virtual NIC in a network.
    Vnic,
    /// A VM has a disk on a storage domain.
    Disk,
    /// A fence agent (power management) belongs to a host.
    Fence,
    /// A VM is a member of an affinity group.
    Affine,
    /// A VM is backed up by a backup.
    BackupOf,
    /// A user is granted a permission.
    Grants,
    /// A permission applies to an object (and everything under it).
    OnObject,
    /// A storage domain is replicated to another one (the target is the replica copy).
    Replica,
}

impl Rel {
    /// Name for the student.
    pub fn label(self) -> &'static str {
        match self {
            Rel::Manages => i18n::tr("manages"),
            Rel::Contains => i18n::tr("contains"),
            Rel::Member => i18n::tr("member of the cluster"),
            Rel::Runs => i18n::tr("runs"),
            Rel::Defined => i18n::tr("defined in the data center"),
            Rel::Attached => i18n::tr("attached to the cluster"),
            Rel::Assigned => i18n::tr("assigned to the host NIC"),
            Rel::EngineNic => i18n::tr("engine NIC"),
            Rel::Domain => i18n::tr("attached to the data center"),
            Rel::Sees => i18n::tr("connected to the host"),
            Rel::Vnic => i18n::tr("virtual NIC"),
            Rel::Disk => i18n::tr("disk"),
            Rel::Fence => i18n::tr("power management of the host"),
            Rel::Affine => i18n::tr("member of the affinity group"),
            Rel::BackupOf => i18n::tr("backed up by"),
            Rel::Grants => i18n::tr("granted"),
            Rel::OnObject => i18n::tr("applies to"),
            Rel::Replica => i18n::tr("replicated to"),
        }
    }
}

/// Relation of a link from an object of one kind to an object of another (`None`: the objects are not linked directly).
pub fn rel(from: Kind, to: Kind) -> Option<Rel> {
    Some(match (from, to) {
        (Kind::Engine, Kind::DataCenter) => Rel::Manages,
        (Kind::DataCenter, Kind::Cluster) => Rel::Contains,
        (Kind::Cluster, Kind::Host) => Rel::Member,
        (Kind::Host, Kind::Vm) => Rel::Runs,
        (Kind::DataCenter, Kind::Network) => Rel::Defined,
        (Kind::Network, Kind::Cluster) => Rel::Attached,
        (Kind::Network, Kind::Host) => Rel::Assigned,
        (Kind::Engine, Kind::Network) => Rel::EngineNic,
        (Kind::DataCenter, Kind::StorageDomain) => Rel::Domain,
        (Kind::StorageDomain, Kind::Host) => Rel::Sees,
        (Kind::Network, Kind::Vm) => Rel::Vnic,
        (Kind::StorageDomain, Kind::Vm) => Rel::Disk,
        (Kind::FenceAgent, Kind::Host) => Rel::Fence,
        (Kind::AffinityGroup, Kind::Vm) => Rel::Affine,
        (Kind::Vm, Kind::Backup) => Rel::BackupOf,
        (Kind::User, Kind::Permission) => Rel::Grants,
        (
            Kind::Permission,
            Kind::DataCenter | Kind::Cluster | Kind::Host | Kind::Vm | Kind::StorageDomain | Kind::Network,
        ) => Rel::OnObject,
        (Kind::StorageDomain, Kind::StorageDomain) => Rel::Replica,
        _ => return None,
    })
}

/// Relations where an object of the target kind has exactly one source.
fn single_parent(r: Rel) -> bool {
    matches!(
        r,
        Rel::Manages | Rel::Contains | Rel::Member | Rel::Runs | Rel::Defined | Rel::Domain | Rel::Fence | Rel::Grants | Rel::Replica
    )
}

/// Relations where an object of the source kind has exactly one target.
fn single_target(r: Rel) -> bool {
    matches!(r, Rel::OnObject)
}

/// A violated rule: the link it is about (index in `edges`) or the board as a whole, and the explanation.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Problem {
    /// Index of the link, if the problem is about one.
    pub edge: Option<usize>,
    /// What is wrong, for the student.
    pub text: String,
}

fn about(edge: usize, text: &str) -> Problem {
    Problem { edge: Some(edge), text: text.to_string() }
}

/// Every rule the board state breaks. A state built with [`connect_error`] and [`prune`] has no problems; the server rejects a hand-made one.
pub fn problems(t: &Topology) -> Vec<Problem> {
    let mut out = vec![];
    let mut ids = std::collections::BTreeSet::new();
    for n in &t.nodes {
        if n.id.is_empty() || !ids.insert(n.id.as_str()) {
            out.push(Problem {
                edge: None,
                text: i18n::tr("object identifiers must be unique and not empty").to_string(),
            });
        }
        if n.name.chars().count() > MAX_NAME || !n.x.is_finite() || !n.y.is_finite() {
            out.push(Problem { edge: None, text: i18n::tr("an object has an invalid name or position").to_string() });
        }
        if let Some(text) = param_error(n) {
            out.push(Problem { edge: None, text });
        }
    }
    if t.nodes.len() > MAX_NODES {
        out.push(Problem { edge: None, text: i18n::trf!("at most {0} objects are allowed", MAX_NODES) });
    }
    if t.of_kind(Kind::Engine).count() > 1 {
        out.push(Problem { edge: None, text: i18n::tr("a single engine manages the environment").to_string() });
    }
    if t.edges.len() > MAX_NODES * 4 {
        out.push(Problem { edge: None, text: i18n::tr("too many links").to_string() });
        return out;
    }
    let mut seen: BTreeMap<(Rel, &str), usize> = BTreeMap::new();
    let mut seen_from: BTreeMap<(Rel, &str), usize> = BTreeMap::new();
    let mut pairs = std::collections::BTreeSet::new();
    for (i, Edge { from, to }) in t.edges.iter().enumerate() {
        let (Some(a), Some(b)) = (t.node(from), t.node(to)) else {
            out.push(about(i, i18n::tr("a link leads to an unknown object")));
            continue;
        };
        if from == to {
            out.push(about(i, i18n::tr("an object cannot be linked to itself")));
            continue;
        }
        let Some(r) = rel(a.kind, b.kind) else {
            out.push(about(i, i18n::tr("in oVirt these objects are not linked directly")));
            continue;
        };
        if !pairs.insert((from.as_str(), to.as_str())) {
            out.push(about(i, i18n::tr("these objects are already linked")));
            continue;
        }
        if single_parent(r) && seen.insert((r, to.as_str()), i).is_some() {
            out.push(about(i, single_parent_text(r)));
            continue;
        }
        if single_target(r) && seen_from.insert((r, from.as_str()), i).is_some() {
            out.push(about(i, single_target_text(r)));
            continue;
        }
        if let Some(text) = context_error(t, r, from, to) {
            out.push(about(i, text));
        }
    }
    out
}

fn single_parent_text(r: Rel) -> &'static str {
    match r {
        Rel::Manages => i18n::tr("a data center is managed by one engine"),
        Rel::Contains => i18n::tr("a cluster belongs to one data center"),
        Rel::Member => i18n::tr("a host belongs to one cluster"),
        Rel::Runs => i18n::tr("a VM runs on one host at a time"),
        Rel::Defined => i18n::tr("a logical network belongs to one data center"),
        Rel::Fence => i18n::tr("a host has one fence agent"),
        Rel::Grants => i18n::tr("a permission belongs to one user"),
        Rel::Replica => i18n::tr("a domain is the replica of one primary domain only"),
        _ => i18n::tr("a storage domain is attached to one data center only"),
    }
}

fn single_target_text(_r: Rel) -> &'static str {
    i18n::tr("a permission applies to one object")
}

/// Rules that depend on the rest of the board (the order of adding links does not matter).
fn context_error(t: &Topology, r: Rel, from: &str, to: &str) -> Option<&'static str> {
    match r {
        Rel::Attached => {
            let net_dc = t.sources(from, Rel::Defined).next();
            let cl_dc = t.dc_of_cluster(to);
            match (net_dc, cl_dc) {
                (None, _) => Some(i18n::tr("define the network in a data center first")),
                (_, None) => Some(i18n::tr("put the cluster into a data center first")),
                (Some(a), Some(b)) if a.id != b.id => Some(i18n::tr("the network is defined in another data center")),
                _ => None,
            }
        }
        Rel::Assigned => match t.cluster_of_host(to) {
            None => Some(i18n::tr("add the host to a cluster first")),
            Some(c) if !t.linked(from, &c.id) => Some(i18n::tr("attach the network to the cluster of the host first")),
            _ => None,
        },
        Rel::Sees => {
            let dom_dc = t.sources(from, Rel::Domain).next();
            let host_dc = t.dc_of_host(to);
            match (dom_dc, host_dc) {
                (None, _) => Some(i18n::tr("attach the storage domain to a data center first")),
                (_, None) => Some(i18n::tr("put the host into a cluster of a data center first")),
                (Some(a), Some(b)) if a.id != b.id => Some(i18n::tr("the host is in another data center")),
                _ => None,
            }
        }
        Rel::Replica => {
            // a replica is a copy, not a source of further copies (this also rules out cycles)
            let replicated_on = t.edges.iter().filter(|e| e.from != e.to).any(|e| {
                (e.to == from && t.node(&e.from).is_some_and(|n| n.kind == Kind::StorageDomain))
                    || (e.from == to && t.node(&e.to).is_some_and(|n| n.kind == Kind::StorageDomain))
            });
            replicated_on.then(|| i18n::tr("a replica is a copy: it cannot be replicated further"))
        }
        _ => None,
    }
}

/// Why the link `from → to` cannot be added to the board (`None`: it can). The direction is the one of [`rel`].
pub fn connect_error(t: &Topology, from: &str, to: &str) -> Option<String> {
    if from == to {
        return Some(i18n::tr("an object cannot be linked to itself").to_string());
    }
    let (Some(a), Some(b)) = (t.node(from), t.node(to)) else {
        return Some(i18n::tr("a link leads to an unknown object").to_string());
    };
    if rel(a.kind, b.kind).is_none() {
        return Some(i18n::tr("in oVirt these objects are not linked directly").to_string());
    }
    let mut next = t.clone();
    next.edges.push(Edge::new(from, to));
    let index = next.edges.len() - 1;
    problems(&next).into_iter().find(|p| p.edge == Some(index)).map(|p| p.text)
}

/// Why an object of this kind cannot be added to the board (`None`: it can).
pub fn add_error(t: &Topology, kind: Kind, max_nodes: usize) -> Option<String> {
    if t.nodes.len() >= max_nodes.min(MAX_NODES) {
        return Some(i18n::trf!("at most {0} objects are allowed", max_nodes.min(MAX_NODES)));
    }
    if kind == Kind::Engine && t.of_kind(Kind::Engine).next().is_some() {
        return Some(i18n::tr("a single engine manages the environment").to_string());
    }
    None
}

/// Drop the links that no longer make sense (after an object or a link was removed). Returns how many were dropped.
pub fn prune(t: &mut Topology) -> usize {
    let mut dropped = 0;
    loop {
        let bad = problems(t).into_iter().find_map(|p| p.edge);
        match bad {
            Some(i) => {
                t.edges.remove(i);
                dropped += 1;
            }
            None => return dropped,
        }
    }
}
