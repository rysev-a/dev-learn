//! The path of a ping over the board: which hosts talk to each other, over which links, and where the path breaks.

use std::collections::{BTreeMap, VecDeque};

use serde::{Deserialize, Serialize};

use super::eval::{address, host_of, published, resolve};
use super::{rel, Kind};
use super::{Evaluation, Rel, Topology};

/// An operation whose path is followed.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "op", rename_all = "snake_case")]
pub enum Op {
    /// A ping from one host to another (a namespace, a VM or the outside network).
    Ping {
        /// Sender identifier.
        from: String,
        /// Receiver identifier.
        to: String,
    },
    /// The outside network connects to a published host inside.
    Publish {
        /// Outside network identifier.
        external: String,
        /// The host (or its interface) the DNAT rule forwards to.
        target: String,
    },
}

/// One step of a path: a packet from one object to another.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Hop {
    /// Sender.
    pub from: String,
    /// Receiver.
    pub to: String,
    /// Links of the board the packet goes over (they are highlighted), as `(source, target)` of the link.
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

fn name(t: &Topology, id: &str) -> String {
    t.node(id).map(|n| n.name.clone()).unwrap_or_else(|| id.to_string())
}

/// The links of the board between two interfaces (the shortest chain over cables, veth pairs, ports, slaves and parents).
fn board_path(t: &Topology, a: &str, b: &str) -> Vec<(String, String)> {
    let l2 = |e: &super::Edge| {
        let (Some(x), Some(y)) = (t.node(&e.from), t.node(&e.to)) else { return false };
        !matches!(rel(x.kind, y.kind), Some(Rel::Lives | Rel::On | Rel::Forwards) | None)
    };
    let mut prev: BTreeMap<&str, (&str, &super::Edge)> = BTreeMap::new();
    let mut queue = VecDeque::from([a]);
    let mut seen = vec![a];
    while let Some(cur) = queue.pop_front() {
        if cur == b {
            break;
        }
        for e in t.edges.iter().filter(|e| l2(e)) {
            let next = if e.from == cur {
                e.to.as_str()
            } else if e.to == cur {
                e.from.as_str()
            } else {
                continue;
            };
            if !seen.contains(&next) {
                seen.push(next);
                prev.insert(next, (cur, e));
                queue.push_back(next);
            }
        }
    }
    let mut out = vec![];
    let mut cur = b;
    while let Some((p, e)) = prev.get(cur) {
        out.push((e.from.clone(), e.to.clone()));
        cur = p;
    }
    out.reverse();
    out
}

fn hop(from: &str, to: &str, links: Vec<(String, String)>, ok: bool, text: String) -> Hop {
    Hop { from: from.into(), to: to.into(), links, ok, text }
}

fn addr_of(t: &Topology, id: &str) -> String {
    address(t, id).unwrap_or_default()
}

/// Follows an operation over the board.
pub fn trace(t: &Topology, ev: &Evaluation, op: &Op) -> Trace {
    match op {
        Op::Ping { from, to } => ping_trace(t, ev, from, to),
        Op::Publish { external, target } => publish_trace(t, ev, external, target),
    }
}

fn finish(hops: Vec<Hop>) -> Trace {
    let ok = !hops.is_empty() && hops.iter().all(|h| h.ok);
    Trace { hops, ok }
}

fn ping_trace(t: &Topology, ev: &Evaluation, from: &str, to: &str) -> Trace {
    let r = resolve(t, ev, from, to, true);
    let (a, b) = (name(t, from), name(t, to));
    let mut hops = vec![];
    if r.reach.ok() {
        match (r.legs.as_slice(), &r.router) {
            ([(ia, ib)], None) => hops.push(hop(
                from,
                to,
                board_path(t, ia, ib),
                true,
                i18n::trf!("“{0}” ({1}) sends the packet straight to “{2}” ({3}): same network, same segment", a, addr_of(t, ia), b, addr_of(t, ib)),
            )),
            ([(ia, g_in), (g_out, ib)], Some(router)) => {
                let rn = name(t, router);
                hops.push(hop(
                    from,
                    router,
                    board_path(t, ia, g_in),
                    true,
                    i18n::trf!("“{0}” sends the packet for another network to its default gateway “{1}” ({2})", a, rn, addr_of(t, g_in)),
                ));
                if let Some(rule) = &r.nat {
                    hops.push(hop(
                        router,
                        router,
                        vec![],
                        true,
                        i18n::trf!("“{0}” forwards the packet and the rule “{1}” puts its own address as the source", rn, name(t, rule)),
                    ));
                } else {
                    hops.push(hop(router, router, vec![], true, i18n::trf!("“{0}” forwards the packet between its networks", rn)));
                }
                hops.push(hop(
                    router,
                    to,
                    board_path(t, g_out, ib),
                    true,
                    i18n::trf!("“{0}” delivers it to “{1}” ({2}); the reply comes back the same way", rn, b, addr_of(t, ib)),
                ));
            }
            _ => hops.push(hop(from, to, vec![], true, i18n::trf!("“{0}” reaches “{1}”", a, b))),
        }
        return finish(hops);
    }
    // failure: the part that works, then the step that breaks
    if let Some(router) = &r.router {
        if let Some(g_in) = ev.endpoints_of(router).first().map(|e| e.iface.clone()) {
            let rn = name(t, router);
            hops.push(hop(
                from,
                router,
                vec![],
                true,
                i18n::trf!("“{0}” sends the packet for another network to its default gateway “{1}” ({2})", a, rn, addr_of(t, &g_in)),
            ));
            hops.push(hop(router, to, vec![], false, i18n::trf!("“{0}” cannot deliver it to “{1}”: {2}", rn, b, r.reach.text())));
            return finish(hops);
        }
    }
    hops.push(hop(from, to, vec![], false, i18n::trf!("“{0}” cannot reach “{1}”: {2}", a, b, r.reach.text())));
    finish(hops)
}

fn publish_trace(t: &Topology, ev: &Evaluation, external: &str, target: &str) -> Trace {
    let reach = published(t, ev, external, target);
    let (e, g) = (name(t, external), name(t, target));
    let host = host_of(t, target).unwrap_or_else(|| target.to_string());
    let router = t
        .of_kind(Kind::Nat)
        .find(|n| n.param_text("kind") == "dnat" && t.linked(&n.id, target))
        .and_then(|n| t.targets(&n.id, Rel::On).into_iter().next().map(|r| r.id.clone()));
    let mut hops = vec![];
    match (&router, reach.ok()) {
        (Some(r), true) => {
            let rn = name(t, r);
            hops.push(hop(external, r, vec![], true, i18n::trf!("“{0}” connects to the published port of “{1}”", e, rn)));
            hops.push(hop(r, &host, vec![], true, i18n::trf!("the DNAT rule of “{0}” sends the connection on to “{1}”", rn, g)));
            hops.push(hop(&host, external, vec![], true, i18n::tr("the answer goes back through the router and the connection is established").to_string()));
        }
        (Some(r), false) => {
            let rn = name(t, r);
            hops.push(hop(external, r, vec![], true, i18n::trf!("“{0}” connects to the published port of “{1}”", e, rn)));
            hops.push(hop(r, &host, vec![], false, i18n::trf!("the connection cannot reach “{0}”: {1}", g, reach.text())));
        }
        (None, _) => hops.push(hop(external, &host, vec![], false, i18n::trf!("“{0}” cannot reach “{1}”: {2}", e, g, reach.text()))),
    }
    finish(hops)
}
