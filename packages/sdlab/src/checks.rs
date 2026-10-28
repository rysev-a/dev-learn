//! Цели упражнения: каждая превращается в строку «условие — выполнено / нет — почему».

use crate::engine::{base_units, evaluate};
use crate::jsfmt;
use crate::kinds;
use crate::types::{EvalOptions, EvalResult, FailKind, Goal, GoalResult, Kind, Op, ParamValue, SdNode, SdState, Workload};

fn label(k: Kind) -> String {
    k.label().to_lowercase()
}

/// Что ломается при отказе, в родительном падеже: «схема переживает отказ …».
pub fn fail_label(f: FailKind) -> &'static str {
    match f {
        FailKind::Zone => i18n::tr("an availability zone"),
        FailKind::Region => i18n::tr("the region"),
        FailKind::Deploy => i18n::tr("a new-version rollout"),
        FailKind::Component(k) => match k {
            Kind::App => i18n::tr("one app server"),
            Kind::Lb => i18n::tr("one load balancer"),
            Kind::Db => i18n::tr("the database leader"),
            Kind::Cache => i18n::tr("the cache"),
            Kind::Cdn => "CDN",
            Kind::Queue => i18n::tr("the queue"),
            Kind::Worker => i18n::tr("one worker"),
            Kind::Gateway => i18n::tr("one gateway"),
            Kind::Search => i18n::tr("one search replica"),
            Kind::Ws => i18n::tr("one WebSocket gateway"),
            Kind::Blob => i18n::tr("the object storage"),
            Kind::Limiter => i18n::tr("the rate limiter"),
            Kind::Monitor => i18n::tr("the monitoring"),
            Kind::Clients => i18n::tr("the users"),
            Kind::Auth => i18n::tr("one auth service"),
            Kind::Geo => i18n::tr("one geo service"),
            Kind::Ml => i18n::tr("one ranking service"),
            Kind::Pay => i18n::tr("one payment channel"),
            Kind::Stream => i18n::tr("the event stream"),
            Kind::Notify => i18n::tr("one notification service"),
            Kind::Analytics => i18n::tr("one analytics node"),
        },
    }
}

/// Условие цели словами.
pub fn describe(g: &Goal) -> String {
    use jsfmt::{num, pct, pct0};
    match g {
        Goal::Capacity { max } => i18n::trf!("no component is loaded above {0}%", pct0(*max)),
        Goal::Util { kind, max } => i18n::trf!("{0} is loaded at most {1}%", label(*kind), pct0(*max)),
        Goal::P99 { max } => i18n::trf!("p99 latency is at most {0} ms", num(*max)),
        Goal::P50 { max } => i18n::trf!("average latency is at most {0} ms", num(*max)),
        Goal::Success { min } => i18n::trf!("at least {0} of requests are served successfully", pct(*min)),
        Goal::Availability { min } => i18n::trf!("diagram availability is at least {0}", pct(*min)),
        Goal::Cost { max } => i18n::trf!("cost is at most ${0} per month", num(*max)),
        Goal::Has { kind, min } => match min {
            Some(m) if *m > 1.0 => i18n::trf!("the diagram has {0} (at least {1})", label(*kind), num(*m)),
            _ => i18n::trf!("the diagram has {0}", label(*kind)),
        },
        Goal::Lacks { kind } => i18n::trf!("the diagram has no “{0}” component", label(*kind)),
        Goal::Link { from, to } => i18n::trf!("{0} is connected to the “{1}” component", label(*from), label(*to)),
        Goal::Hit { min } => i18n::trf!("the cache serves at least {0}% of reads", pct0(*min)),
        Goal::CdnHit { min } => i18n::trf!("the CDN serves at least {0}% of static content", pct0(*min)),
        Goal::Survive { fail } => i18n::trf!("the diagram survives the failure of {0}", fail_label(*fail)),
        Goal::Param { kind, key, op, value } => {
            let name = kinds::param_spec(*kind, key).map_or(key.as_str(), |p| p.label);
            format!("{}: {} {} {}", label(*kind), name, op.as_str(), value.as_text())
        }
        Goal::Lag { max } => i18n::trf!("the queue drains after the peak in at most {0} s", num(*max)),
        Goal::ReplicaLag { max } => i18n::trf!("replica lag is at most {0} ms", num(*max)),
        Goal::ShardShare { max } => i18n::trf!("the busiest shard receives at most {0}% of data and requests", pct0(*max)),
        Goal::NoSpof { kinds } => i18n::trf!("no single point of failure: {0}", kinds.iter().map(|k| label(*k)).collect::<Vec<_>>().join(", ")),
    }
}

fn cmp(a: &ParamValue, op: Op, b: &ParamValue) -> bool {
    match op {
        Op::Eq => a == b,
        Op::Ne => a != b,
        Op::Ge => a.to_number() >= b.to_number(),
        Op::Le => a.to_number() <= b.to_number(),
    }
}

/// Есть ли у компонента резерв (для цели `no_spof`).
fn redundant(n: &SdNode) -> bool {
    match n.kind {
        Kind::Lb
        | Kind::App
        | Kind::Gateway
        | Kind::Worker
        | Kind::Ws
        | Kind::Auth
        | Kind::Geo
        | Kind::Ml
        | Kind::Pay
        | Kind::Notify
        | Kind::Analytics
        | Kind::Search => base_units(n) >= 2.0,
        Kind::Cache => n.num("replicas") >= 1.0,
        Kind::Db => n.num("replicas") >= 1.0 && n.flag("failover"),
        Kind::Queue | Kind::Stream => n.num("partitions") >= 3.0,
        _ => true,
    }
}

/// Проверка целей по схеме. `base` — готовый расчёт без отказов (чтобы не считать дважды).
pub fn check_goals(state: &SdState, wl: &Workload, goals: &[Goal], base: Option<&EvalResult>) -> Vec<GoalResult> {
    let computed;
    let r = match base {
        Some(b) => b,
        None => {
            computed = evaluate(state, wl, &EvalOptions::default());
            &computed
        }
    };
    goals.iter().map(|g| check_goal(state, wl, g, r)).collect()
}

fn check_goal(state: &SdState, wl: &Workload, g: &Goal, r: &EvalResult) -> GoalResult {
    use jsfmt::{num, pct, pct0};
    let text = describe(g);
    let done = |ok: bool, detail: String| GoalResult { ok, text: text.clone(), detail };
    let count = |k: Kind| state.of_kind(k).count();
    match g {
        Goal::Capacity { max } => {
            // самый загруженный: при равенстве — первый по порядку узлов
            let mut worst: Option<(&str, f64)> = None;
            for (id, l) in r.loads.iter() {
                if l.status == crate::types::NodeStatus::Idle {
                    continue;
                }
                if worst.is_none_or(|(_, u)| l.util > u) {
                    worst = Some((id, l.util));
                }
            }
            match worst {
                None => done(false, i18n::tr("the load reaches nothing").into()),
                Some((id, util)) => {
                    let name = state.node(id).map_or(id, |n| n.name.as_str());
                    done(util <= *max, i18n::trf!("the busiest is “{0}”: {1}%", name, pct0(util)))
                }
            }
        }
        Goal::Util { kind, max } => {
            let ns: Vec<&SdNode> = state.of_kind(*kind).collect();
            if ns.is_empty() {
                return done(false, i18n::tr("no such component").into());
            }
            let worst = ns.iter().map(|n| r.loads.get(&n.id).map_or(0.0, |l| l.util)).fold(f64::NEG_INFINITY, f64::max);
            done(worst <= *max, i18n::trf!("now {0}%", pct0(worst)))
        }
        Goal::P99 { max } => done(r.entry && r.p99 <= *max, if r.entry { i18n::trf!("now {0} ms", num(r.p99)) } else { i18n::tr("requests do not reach processing").into() }),
        Goal::P50 { max } => done(r.entry && r.p50 <= *max, if r.entry { i18n::trf!("now {0} ms", num(r.p50)) } else { i18n::tr("requests do not reach processing").into() }),
        Goal::Success { min } => done(r.success >= *min, i18n::trf!("now {0}", pct(r.success))),
        Goal::Availability { min } => done(r.availability >= *min, i18n::trf!("now {0}", pct(r.availability))),
        Goal::Cost { max } => done(r.cost <= *max, i18n::trf!("now ${0}", num(r.cost))),
        Goal::Has { kind, min } => {
            let n = count(*kind);
            let need = min.unwrap_or(1.0);
            done(n as f64 >= need, i18n::trf!("in the diagram: {0}", n))
        }
        Goal::Lacks { kind } => {
            let n = count(*kind);
            done(n == 0, i18n::trf!("in the diagram: {0}", n))
        }
        Goal::Link { from, to } => {
            let ok = state.edges.iter().any(|e| state.of_kind(*to).any(|t| t.id == e.to) && state.node(&e.from).is_some_and(|f| f.kind == *from));
            done(ok, if ok { i18n::tr("link exists").into() } else { i18n::tr("no link").into() })
        }
        Goal::Hit { min } => done(r.hit.unwrap_or(0.0) >= *min, r.hit.map_or(i18n::tr("no cache").into(), |h| i18n::trf!("now {0}%", pct0(h)))),
        Goal::CdnHit { min } => done(r.cdn_hit.unwrap_or(0.0) >= *min, r.cdn_hit.map_or(i18n::tr("no CDN").into(), |h| i18n::trf!("now {0}%", pct0(h)))),
        Goal::Survive { fail } => {
            let f = evaluate(state, wl, &EvalOptions::fail(*fail));
            let ok = f.entry && f.success >= 0.99;
            done(ok, if ok { i18n::tr("everything works after the failure").into() } else { i18n::trf!("after the failure {0} succeed", pct(if f.entry { f.success } else { 0.0 })) })
        }
        Goal::Param { kind, key, op, value } => {
            let ns: Vec<&SdNode> = state.of_kind(*kind).collect();
            let ok = !ns.is_empty() && ns.iter().all(|n| cmp(n.param(key), *op, value));
            let detail = if ns.is_empty() {
                i18n::tr("no such component").to_owned()
            } else {
                i18n::trf!("now {0}", ns.iter().map(|n| n.param(key).as_text().into_owned()).collect::<Vec<_>>().join(", "))
            };
            done(ok, detail)
        }
        Goal::Lag { max } => {
            let ok = r.lag_sec.is_some_and(|l| l <= *max);
            let detail = match r.lag_sec {
                None => i18n::tr("no queue").to_owned(),
                Some(l) if l >= 999.0 => i18n::tr("the queue is not draining").to_owned(),
                Some(l) => i18n::trf!("now {0} s", num(l)),
            };
            done(ok, detail)
        }
        Goal::ReplicaLag { max } => done(
            r.replica_lag_ms.is_some_and(|l| l <= *max),
            r.replica_lag_ms.map_or(i18n::tr("no replicas").into(), |l| i18n::trf!("now {0} ms", num(l))),
        ),
        Goal::ShardShare { max } => done(
            r.max_shard_share.is_some_and(|l| l <= *max),
            r.max_shard_share.map_or(i18n::tr("no database").into(), |l| i18n::trf!("now {0}%", pct0(l))),
        ),
        Goal::NoSpof { kinds } => {
            let bad: Vec<&str> = kinds.iter().flat_map(|k| state.of_kind(*k).filter(|n| !redundant(n)).map(|n| n.name.as_str())).collect();
            let present = kinds.iter().any(|k| count(*k) > 0);
            let detail = if !bad.is_empty() {
                i18n::trf!("only one: {0}", bad.join(", "))
            } else if present {
                i18n::tr("redundancy is in place").to_owned()
            } else {
                i18n::tr("no components").to_owned()
            };
            done(present && bad.is_empty(), detail)
        }
    }
}

/// Все ли цели выполнены.
pub fn all_ok(rs: &[GoalResult]) -> bool {
    rs.iter().all(|r| r.ok)
}
