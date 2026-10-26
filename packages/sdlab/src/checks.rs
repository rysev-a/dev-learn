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
        FailKind::Zone => "зоны доступности",
        FailKind::Region => "региона",
        FailKind::Deploy => "выкладки новой версии",
        FailKind::Component(k) => match k {
            Kind::App => "одного сервера приложения",
            Kind::Lb => "одного балансировщика",
            Kind::Db => "лидера базы данных",
            Kind::Cache => "кэша",
            Kind::Cdn => "CDN",
            Kind::Queue => "очереди",
            Kind::Worker => "одного обработчика",
            Kind::Gateway => "одного шлюза",
            Kind::Search => "одной реплики поиска",
            Kind::Ws => "одного WebSocket-шлюза",
            Kind::Blob => "объектного хранилища",
            Kind::Limiter => "ограничителя",
            Kind::Monitor => "мониторинга",
            Kind::Clients => "пользователей",
            Kind::Auth => "одного сервиса входа",
            Kind::Geo => "одного геосервиса",
            Kind::Ml => "одного сервиса ранжирования",
            Kind::Pay => "одного платёжного канала",
            Kind::Stream => "потока событий",
            Kind::Notify => "одного сервиса уведомлений",
            Kind::Analytics => "одного узла аналитики",
        },
    }
}

/// Условие цели словами.
pub fn describe(g: &Goal) -> String {
    use jsfmt::{num, pct, pct0};
    match g {
        Goal::Capacity { max } => format!("ни один компонент не загружен больше чем на {}%", pct0(*max)),
        Goal::Util { kind, max } => format!("{} загружен не больше чем на {}%", label(*kind), pct0(*max)),
        Goal::P99 { max } => format!("задержка p99 не больше {} мс", num(*max)),
        Goal::P50 { max } => format!("средняя задержка не больше {} мс", num(*max)),
        Goal::Success { min } => format!("успешно обслуживается не меньше {} запросов", pct(*min)),
        Goal::Availability { min } => format!("доступность схемы не ниже {}", pct(*min)),
        Goal::Cost { max } => format!("стоимость не больше ${} в месяц", num(*max)),
        Goal::Has { kind, min } => match min {
            Some(m) if *m > 1.0 => format!("в схеме есть {} (не меньше {})", label(*kind), num(*m)),
            _ => format!("в схеме есть {}", label(*kind)),
        },
        Goal::Lacks { kind } => format!("в схеме нет компонента «{}»", label(*kind)),
        Goal::Link { from, to } => format!("{} соединён с компонентом «{}»", label(*from), label(*to)),
        Goal::Hit { min } => format!("кэш отдаёт не меньше {}% чтений", pct0(*min)),
        Goal::CdnHit { min } => format!("CDN отдаёт не меньше {}% статики", pct0(*min)),
        Goal::Survive { fail } => format!("схема переживает отказ {}", fail_label(*fail)),
        Goal::Param { kind, key, op, value } => {
            let name = kinds::param_spec(*kind, key).map_or(key.as_str(), |p| p.label);
            format!("{}: {} {} {}", label(*kind), name, op.as_str(), value.as_text())
        }
        Goal::Lag { max } => format!("очередь разбирается после пика не дольше чем за {} с", num(*max)),
        Goal::ReplicaLag { max } => format!("отставание реплик не больше {} мс", num(*max)),
        Goal::ShardShare { max } => format!("на самый нагруженный шард приходится не больше {}% данных и запросов", pct0(*max)),
        Goal::NoSpof { kinds } => format!("нет единой точки отказа: {}", kinds.iter().map(|k| label(*k)).collect::<Vec<_>>().join(", ")),
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
                None => done(false, "нагрузка никуда не доходит".into()),
                Some((id, util)) => {
                    let name = state.node(id).map_or(id, |n| n.name.as_str());
                    done(util <= *max, format!("самый загруженный — «{name}»: {}%", pct0(util)))
                }
            }
        }
        Goal::Util { kind, max } => {
            let ns: Vec<&SdNode> = state.of_kind(*kind).collect();
            if ns.is_empty() {
                return done(false, "компонента нет".into());
            }
            let worst = ns.iter().map(|n| r.loads.get(&n.id).map_or(0.0, |l| l.util)).fold(f64::NEG_INFINITY, f64::max);
            done(worst <= *max, format!("сейчас {}%", pct0(worst)))
        }
        Goal::P99 { max } => done(r.entry && r.p99 <= *max, if r.entry { format!("сейчас {} мс", num(r.p99)) } else { "запросы не доходят до обработки".into() }),
        Goal::P50 { max } => done(r.entry && r.p50 <= *max, if r.entry { format!("сейчас {} мс", num(r.p50)) } else { "запросы не доходят до обработки".into() }),
        Goal::Success { min } => done(r.success >= *min, format!("сейчас {}", pct(r.success))),
        Goal::Availability { min } => done(r.availability >= *min, format!("сейчас {}", pct(r.availability))),
        Goal::Cost { max } => done(r.cost <= *max, format!("сейчас ${}", num(r.cost))),
        Goal::Has { kind, min } => {
            let n = count(*kind);
            let need = min.unwrap_or(1.0);
            done(n as f64 >= need, format!("на схеме: {n}"))
        }
        Goal::Lacks { kind } => {
            let n = count(*kind);
            done(n == 0, format!("на схеме: {n}"))
        }
        Goal::Link { from, to } => {
            let ok = state.edges.iter().any(|e| state.of_kind(*to).any(|t| t.id == e.to) && state.node(&e.from).is_some_and(|f| f.kind == *from));
            done(ok, if ok { "связь есть".into() } else { "связи нет".into() })
        }
        Goal::Hit { min } => done(r.hit.unwrap_or(0.0) >= *min, r.hit.map_or("кэша нет".into(), |h| format!("сейчас {}%", pct0(h)))),
        Goal::CdnHit { min } => done(r.cdn_hit.unwrap_or(0.0) >= *min, r.cdn_hit.map_or("CDN нет".into(), |h| format!("сейчас {}%", pct0(h)))),
        Goal::Survive { fail } => {
            let f = evaluate(state, wl, &EvalOptions::fail(*fail));
            let ok = f.entry && f.success >= 0.99;
            done(ok, if ok { "после отказа всё работает".into() } else { format!("после отказа успешно {}", pct(if f.entry { f.success } else { 0.0 })) })
        }
        Goal::Param { kind, key, op, value } => {
            let ns: Vec<&SdNode> = state.of_kind(*kind).collect();
            let ok = !ns.is_empty() && ns.iter().all(|n| cmp(n.param(key), *op, value));
            let detail = if ns.is_empty() {
                "компонента нет".to_owned()
            } else {
                format!("сейчас {}", ns.iter().map(|n| n.param(key).as_text().into_owned()).collect::<Vec<_>>().join(", "))
            };
            done(ok, detail)
        }
        Goal::Lag { max } => {
            let ok = r.lag_sec.is_some_and(|l| l <= *max);
            let detail = match r.lag_sec {
                None => "очереди нет".to_owned(),
                Some(l) if l >= 999.0 => "очередь не разбирается".to_owned(),
                Some(l) => format!("сейчас {} с", num(l)),
            };
            done(ok, detail)
        }
        Goal::ReplicaLag { max } => done(
            r.replica_lag_ms.is_some_and(|l| l <= *max),
            r.replica_lag_ms.map_or("реплик нет".into(), |l| format!("сейчас {} мс", num(l))),
        ),
        Goal::ShardShare { max } => done(
            r.max_shard_share.is_some_and(|l| l <= *max),
            r.max_shard_share.map_or("базы нет".into(), |l| format!("сейчас {}%", pct0(l))),
        ),
        Goal::NoSpof { kinds } => {
            let bad: Vec<&str> = kinds.iter().flat_map(|k| state.of_kind(*k).filter(|n| !redundant(n)).map(|n| n.name.as_str())).collect();
            let present = kinds.iter().any(|k| count(*k) > 0);
            let detail = if !bad.is_empty() {
                format!("единственные: {}", bad.join(", "))
            } else if present {
                "резервирование есть".to_owned()
            } else {
                "компонентов нет".to_owned()
            };
            done(present && bad.is_empty(), detail)
        }
    }
}

/// Все ли цели выполнены.
pub fn all_ok(rs: &[GoalResult]) -> bool {
    rs.iter().all(|r| r.ok)
}
