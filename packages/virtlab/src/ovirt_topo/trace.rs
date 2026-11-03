//! The path of an operation over the board: which objects talk to each other, over which networks, and where the path breaks.

use serde::{Deserialize, Serialize};

use super::eval::management_path;
use super::{Evaluation, HostStatus, Kind, Rel, Role, Topology};

/// An operation whose path is followed.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "op", rename_all = "snake_case")]
pub enum Op {
    /// The engine sends a command to the host (VDSM).
    EngineToHost {
        /// Host identifier.
        host: String,
    },
    /// Start a VM.
    StartVm {
        /// VM identifier.
        vm: String,
    },
    /// Live-migrate a VM to another host of its cluster.
    Migrate {
        /// VM identifier.
        vm: String,
    },
    /// Fence a host: the engine asks another Up host of the data center (the fence proxy) to power-cycle it through its fence agent.
    Fence {
        /// Host identifier.
        host: String,
    },
}

/// One step of a path: a message from one object to another.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Hop {
    /// Sender.
    pub from: String,
    /// Receiver.
    pub to: String,
    /// Links of the board the message goes over (they are highlighted), as `(source, target)` of the link.
    pub links: Vec<(String, String)>,
    /// The step works.
    pub ok: bool,
    /// What happens here, or why it breaks.
    pub text: String,
}

/// Path of an operation.
#[derive(Clone, Debug, PartialEq, Eq, Default)]
pub struct Trace {
    /// Steps in order.
    pub hops: Vec<Hop>,
    /// All steps work.
    pub ok: bool,
}

impl Trace {
    fn finish(hops: Vec<Hop>) -> Trace {
        let ok = !hops.is_empty() && hops.iter().all(|h| h.ok);
        Trace { hops, ok }
    }
}

fn name(t: &Topology, id: &str) -> String {
    t.node(id).map(|n| n.name.clone()).unwrap_or_default()
}

fn engine_to_host(t: &Topology, host: &str) -> Hop {
    match management_path(t, host) {
        Some((engine, net)) => Hop {
            from: engine.into(),
            to: host.into(),
            links: vec![(engine.into(), net.into()), (net.into(), host.into())],
            ok: true,
            text: i18n::trf!(
                "the engine sends the command to VDSM of “{0}” over the management network “{1}”",
                name(t, host),
                name(t, net)
            ),
        },
        None => Hop {
            from: t.of_kind(Kind::Engine).next().map(|e| e.id.clone()).unwrap_or_default(),
            to: host.into(),
            links: vec![],
            ok: false,
            text: i18n::trf!("the engine cannot reach “{0}”: no management network between them", name(t, host)),
        },
    }
}

/// Hops of the checks a host does before it can run a VM: networks of the virtual NICs and the disks.
fn vm_needs(t: &Topology, ev: &Evaluation, vm: &str, host: &str) -> Vec<Hop> {
    let mut hops = vec![];
    let host_dc = t.dc_of_host(host).map(|d| d.id.clone());
    for n in t.sources(vm, Rel::Vnic) {
        let ok = t.linked(&n.id, host);
        hops.push(Hop {
            from: host.into(),
            to: n.id.clone(),
            links: vec![(n.id.clone(), host.into())],
            ok,
            text: if ok {
                i18n::trf!("the virtual NIC of the VM is plugged into the network “{0}” on the host", n.name)
            } else {
                i18n::trf!(
                    "the network “{0}” is not assigned to the host: the virtual NIC has nowhere to connect",
                    n.name
                )
            },
        });
    }
    for d in t.sources(vm, Rel::Disk) {
        let same_dc = host_dc.as_deref().is_some_and(|dc| t.linked(dc, &d.id));
        let sees = t.linked(&d.id, host);
        let active = ev.domain(&d.id).is_some_and(|e| e.status == super::DomainStatus::Active);
        let ok = same_dc && sees && active;
        hops.push(Hop {
            from: host.into(),
            to: d.id.clone(),
            links: vec![(d.id.clone(), host.into())],
            ok,
            text: if ok {
                i18n::trf!("the host opens the disk of the VM on the storage domain “{0}”", d.name)
            } else if !same_dc {
                i18n::trf!("the domain “{0}” belongs to another data center than the host", d.name)
            } else if !sees {
                i18n::trf!("the host does not see the storage domain “{0}”", d.name)
            } else {
                i18n::trf!("the storage domain “{0}” is not active", d.name)
            },
        });
    }
    hops
}

/// The network over which two hosts of a cluster can talk: a migration network first, then the management one.
pub fn migration_network<'a>(t: &'a Topology, a: &str, b: &str) -> Option<&'a super::Node> {
    let common =
        |role: Role| t.of_kind(Kind::Network).find(|n| n.role() == role && t.linked(&n.id, a) && t.linked(&n.id, b));
    common(Role::Migration).or_else(|| common(Role::Management))
}

/// The host a VM of `src` would be migrated to: another Up host of the same cluster (the first in the order of the links).
pub fn migration_target<'a>(t: &'a Topology, ev: &Evaluation, src: &str) -> Option<&'a super::Node> {
    let cluster = t.cluster_of_host(src)?;
    t.targets(&cluster.id, Rel::Member)
        .find(|h| h.id != src && ev.host(&h.id).is_some_and(|e| e.status == HostStatus::Up))
}

/// The fence agent (power management) of a host.
pub fn fence_agent<'a>(t: &'a Topology, host: &str) -> Option<&'a super::Node> {
    t.sources(host, Rel::Fence).next()
}

/// The fence proxy of a host: the first other host of its data center (board order) that is Up in `ev`. `ev` may be the evaluation of a
/// different board than `t` (for example after the loss of the host itself), as long as the identifiers agree.
pub fn fence_proxy<'a>(t: &'a Topology, ev: &Evaluation, host: &str) -> Option<&'a super::Node> {
    let dc = t.dc_of_host(host)?;
    t.hosts_of_dc(&dc.id).find(|h| h.id != host && ev.host_up(&h.id))
}

fn fence(t: &Topology, ev: &Evaluation, host: &str) -> Trace {
    let host_name = name(t, host);
    let proxy = fence_proxy(t, ev, host);
    let agent = fence_agent(t, host);
    let mut hops = vec![];
    match proxy {
        Some(p) => {
            let (links, over) = match management_path(t, &p.id) {
                Some((engine, net)) => (
                    vec![(engine.to_string(), net.to_string()), (net.to_string(), p.id.clone())],
                    name(t, net),
                ),
                None => (vec![], String::new()),
            };
            hops.push(Hop {
                from: t.of_kind(Kind::Engine).next().map(|e| e.id.clone()).unwrap_or_default(),
                to: p.id.clone(),
                links,
                ok: true,
                text: i18n::trf!(
                    "the engine asks “{0}”, the fence proxy, to power-manage “{1}” (over the management network “{2}”)",
                    p.name,
                    host_name,
                    over
                ),
            });
        }
        None => hops.push(Hop {
            from: t.of_kind(Kind::Engine).next().map(|e| e.id.clone()).unwrap_or_default(),
            to: host.into(),
            links: vec![],
            ok: false,
            text: i18n::trf!(
                "there is no other Up host in the data center of “{0}” to act as the fence proxy",
                host_name
            ),
        }),
    }
    match (agent, proxy) {
        (None, _) => hops.push(Hop {
            from: proxy.map_or_else(|| host.to_string(), |p| p.id.clone()),
            to: host.into(),
            links: vec![],
            ok: false,
            text: i18n::trf!("“{0}” has no fence agent: power management is not configured, so the host cannot be fenced", host_name),
        }),
        (Some(a), Some(p)) => {
            hops.push(Hop {
                from: p.id.clone(),
                to: a.id.clone(),
                links: vec![],
                ok: true,
                text: i18n::trf!("the proxy “{0}” sends the fence command to the agent “{1}”", p.name, a.name),
            });
            hops.push(Hop {
                from: a.id.clone(),
                to: host.into(),
                links: vec![(a.id.clone(), host.into())],
                ok: true,
                text: i18n::trf!("the agent “{0}” powers “{1}” off and on over its power interface", a.name, host_name),
            });
        }
        (Some(_), None) => {}
    }
    Trace::finish(hops)
}

/// Follow the operation over the board.
pub fn trace(t: &Topology, ev: &Evaluation, op: &Op) -> Trace {
    match op {
        Op::EngineToHost { host } => Trace::finish(vec![engine_to_host(t, host)]),
        Op::Fence { host } => fence(t, ev, host),
        Op::StartVm { vm } => {
            let Some(host) = t.host_of_vm(vm) else {
                return Trace::finish(vec![Hop {
                    from: vm.clone(),
                    to: vm.clone(),
                    links: vec![],
                    ok: false,
                    text: i18n::trf!("the VM “{0}” is not placed on a host", name(t, vm)),
                }]);
            };
            let mut hops = vec![engine_to_host(t, &host.id)];
            hops.extend(vm_needs(t, ev, vm, &host.id));
            Trace::finish(hops)
        }
        Op::Migrate { vm } => {
            let Some(src) = t.host_of_vm(vm) else {
                return Trace::finish(vec![Hop {
                    from: vm.clone(),
                    to: vm.clone(),
                    links: vec![],
                    ok: false,
                    text: i18n::trf!("the VM “{0}” is not placed on a host", name(t, vm)),
                }]);
            };
            let target = migration_target(t, ev, &src.id);
            let Some(dst) = target else {
                return Trace::finish(vec![Hop {
                    from: src.id.clone(),
                    to: src.id.clone(),
                    links: vec![],
                    ok: false,
                    text: i18n::tr(
                        "there is no other Up host in the cluster to migrate to (a VM never leaves its cluster)",
                    )
                    .to_string(),
                }]);
            };
            let mut hops = vec![engine_to_host(t, &src.id)];
            hops.push(match migration_network(t, &src.id, &dst.id) {
                Some(net) => Hop {
                    from: src.id.clone(),
                    to: dst.id.clone(),
                    links: vec![(net.id.clone(), src.id.clone()), (net.id.clone(), dst.id.clone())],
                    ok: true,
                    text: i18n::trf!(
                        "the memory of the VM goes from “{0}” to “{1}” over the network “{2}”",
                        src.name,
                        dst.name,
                        net.name
                    ),
                },
                None => Hop {
                    from: src.id.clone(),
                    to: dst.id.clone(),
                    links: vec![],
                    ok: false,
                    text: i18n::trf!(
                        "no migration or management network is assigned to both “{0}” and “{1}”",
                        src.name,
                        dst.name
                    ),
                },
            });
            hops.extend(vm_needs(t, ev, vm, &dst.id));
            Trace::finish(hops)
        }
    }
}
