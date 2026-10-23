//! Цели достижимы: для каждого упражнения есть последовательность действий, достигающая всех целей, и сервер её принимает.
//! Плюс отрицательные случаи проверки (`verify`): подделанные данные отклоняются.

use serde_json::{json, Value};
use virtlab::labfile::build_chapters;
use virtlab::{hv, migration, numa, qcow2, verify_with, virtq, GoalStatus, Spec, Strictness, Task};

const DEFINITIONS: &str = include_str!("../data/tasks.json");

fn task(id: &str) -> Task {
    build_chapters(DEFINITIONS)
        .expect("главы собираются")
        .into_iter()
        .flat_map(|c| c.tasks)
        .find(|t| t.id == id)
        .unwrap_or_else(|| panic!("нет упражнения {id}"))
}

fn statuses(t: &Task, submitted: &Value) -> Vec<(String, GoalStatus)> {
    t.verify(submitted).goals.into_iter().map(|g| (g.id, g.status)).collect()
}

fn all_verified(t: &Task, submitted: &Value) {
    let v = t.verify(submitted);
    assert!(v.solved, "{}: {:?}", t.id, v);
    assert!(v.goals.iter().all(|g| g.status == GoalStatus::Verified), "{}: {:?}", t.id, v);
    // и в строгом режиме
    assert!(verify_with(&t.spec, submitted, Strictness::Strict).solved);
}

fn status_of(t: &Task, submitted: &Value, goal: &str) -> GoalStatus {
    statuses(t, submitted).into_iter().find(|(id, _)| id == goal).map(|(_, s)| s).unwrap()
}

fn is_rejected(s: &GoalStatus) -> bool {
    matches!(s, GoalStatus::Rejected { .. })
}

// ---------------------------------------------------------------- hv

fn programs(t: &Task) -> Vec<hv::Program> {
    match &t.spec {
        Spec::Hv { programs } => programs.clone(),
        _ => panic!("не hv"),
    }
}

#[test]
fn hv_ideal_runs_reach_every_goal() {
    let t = task("virt-sim-hv");
    let mut submitted = serde_json::Map::new();
    for p in programs(&t) {
        let translate = hv::needs_translation(&p).unwrap();
        let run = hv::ideal_run(&p, translate).unwrap();
        let fin = hv::replay(&p, &run).unwrap();
        assert!(fin.ok && fin.mistakes == 0, "{}", p.id);
        submitted.insert(p.id.clone(), json!({ "translate": translate, "mistakes": 0, "trace": run.steps }));
    }
    // POPF нужна трансляция, остальным — нет
    assert!(hv::needs_translation(&programs(&t)[2]).unwrap());
    assert!(!hv::needs_translation(&programs(&t)[0]).unwrap());
    all_verified(&t, &Value::Object(submitted));
}

#[test]
fn hv_popf_without_translation_fails_and_silent_is_counted() {
    let t = task("virt-sim-hv");
    let p = programs(&t).into_iter().find(|p| p.id == "popf").unwrap();
    let run = hv::ideal_run(&p, false).unwrap();
    assert!(run.steps.contains(&hv::Step::Silent));
    let fin = hv::replay(&p, &run).unwrap();
    assert!(!fin.ok && fin.state.silent && fin.state.vif == 0);
    // сервер отклоняет такой прогон, даже если клиент заявил «успех»
    let sub = json!({ "popf": { "translate": false, "mistakes": 0, "trace": run.steps } });
    assert!(is_rejected(&status_of(&t, &sub, "popf")));
}

#[test]
fn hv_session_behaves_like_the_react_lab() {
    let p = programs(&task("virt-sim-hv")).into_iter().find(|p| p.id == "irq").unwrap();
    let mut s = hv::Session::new(&p.code, false).unwrap();
    assert!(!s.started());
    assert!(s.set_translate(true));
    // CLI — ловушка: шаг заблокирован, неверный выбор — ошибка, состояние не меняется
    assert_eq!(s.step(), hv::Stepped::Blocked);
    assert!(matches!(s.choose("vif ← 1"), hv::Choice::Wrong { .. }));
    assert_eq!(s.state().mistakes, 1);
    assert_eq!(s.state().pc, 0);
    assert_eq!(s.choose("несуществующий вариант"), hv::Choice::Invalid);
    assert_eq!(s.choose("виртуальный флаг vif ← 0"), hv::Choice::Applied);
    assert!(s.started());
    assert!(!s.set_translate(false), "после запуска трансляцию менять нельзя");
    // IRQ при vif = 0: верно только «поставить в очередь»
    assert!(matches!(s.choose("доставить гостю сейчас"), hv::Choice::Wrong { .. }));
    assert_eq!(s.choose("поставить в очередь"), hv::Choice::Applied);
    assert_eq!(s.choose("поставить в очередь"), hv::Choice::Applied);
    assert_eq!(s.state().queue, vec![1, 2]);
    assert_eq!(s.choose("vif ← 1 и доставить очередь"), hv::Choice::Applied);
    assert_eq!(s.state().delivered, vec![1, 2]);
    let hv::Choice::Finished(f) = s.choose("остановить виртуальный процессор гостя")
    else {
        panic!("ожидалась остановка")
    };
    assert!(f.ok);
    assert_eq!(f.mistakes, 2);
    assert_eq!(s.current(), None);
    assert_eq!(s.state().log.len(), 5);
}

#[test]
fn hv_verify_rejects_forged_data() {
    let t = task("virt-sim-hv");
    let ps = programs(&t);
    let base = ps.iter().find(|p| p.id == "base").unwrap();
    let run = hv::ideal_run(base, false).unwrap();
    // число ошибок не совпадает с записью
    let sub = json!({ "base": { "translate": false, "mistakes": 3, "trace": run.steps } });
    assert!(is_rejected(&status_of(&t, &sub, "base")));
    // неполная запись: гость не остановлен
    let short: Vec<_> = run.steps[..run.steps.len() - 1].to_vec();
    let sub = json!({ "base": { "translate": false, "mistakes": 0, "trace": short } });
    assert!(is_rejected(&status_of(&t, &sub, "base")));
    // действие, невозможное на этой команде (первая команда — ADD, а не ловушка)
    let sub = json!({ "base": { "translate": false, "mistakes": 0, "trace": [{"step": "silent"}] } });
    assert!(is_rejected(&status_of(&t, &sub, "base")));
    // неверная форма
    let sub = json!({ "base": { "translate": "yes" } });
    assert!(is_rejected(&status_of(&t, &sub, "base")));
    // прежний клиент: POPF без трансляции — отказ; остальное — без перепроверки
    let legacy = json!({
        "base": { "translate": false, "mistakes": 0 },
        "irq": { "translate": false, "mistakes": 1 },
        "popf": { "translate": false, "mistakes": 0 },
    });
    assert_eq!(status_of(&t, &legacy, "base"), GoalStatus::Unverified);
    assert!(is_rejected(&status_of(&t, &legacy, "popf")));
    assert!(!t.verify(&legacy).solved);
    let legacy_ok = json!({
        "base": { "translate": false, "mistakes": 0 },
        "irq": { "translate": false, "mistakes": 1 },
        "popf": { "translate": true, "mistakes": 0 },
    });
    assert!(t.verify(&legacy_ok).solved, "прежний клиент принимается по структуре");
    assert!(!verify_with(&t.spec, &legacy_ok, Strictness::Strict).solved);
}

// ---------------------------------------------------------------- ept

#[test]
fn ept_solutions_reach_every_goal() {
    let t = task("virt-sim-ept");
    let sub = json!({
        "walk": { "mode": "ept", "guest": "1G", "host": "1G", "workload": "one" },
        "scan": { "mode": "shadow", "guest": "4K", "host": "4K", "workload": "scan" },
        "random": { "mode": "ept", "guest": "1G", "host": "1G", "workload": "random" },
        "fork": { "mode": "ept", "guest": "1G", "host": "1G", "workload": "fork" },
    });
    all_verified(&t, &sub);
}

#[test]
fn ept_verify_rejects_wrong_configs() {
    let t = task("virt-sim-ept");
    // 4K/4K в EPT — 24 обращения на промах: цель «не больше 15» не выполнена
    let sub = json!({ "walk": { "mode": "ept", "guest": "4K", "host": "4K", "workload": "one" } });
    assert!(is_rejected(&status_of(&t, &sub, "walk")));
    // режим «теневые» не засчитывает цель про вложенные таблицы
    let sub = json!({ "walk": { "mode": "shadow", "guest": "1G", "host": "1G", "workload": "one" } });
    assert!(is_rejected(&status_of(&t, &sub, "walk")));
    // сканирование в EPT дороже 15 000?  4K/4K: 2048 × (24 + 1) = 51 200
    let sub = json!({ "scan": { "mode": "ept", "guest": "4K", "host": "4K", "workload": "scan" } });
    assert!(is_rejected(&status_of(&t, &sub, "scan")));
    // запуск на чужой нагрузке не засчитывается
    let sub = json!({ "fork": { "mode": "ept", "guest": "1G", "host": "1G", "workload": "random" } });
    assert!(is_rejected(&status_of(&t, &sub, "fork")));
    // теневые таблицы на «fork»: 500 выходов по 1000
    let sub = json!({ "fork": { "mode": "shadow", "guest": "1G", "host": "1G", "workload": "fork" } });
    assert!(is_rejected(&status_of(&t, &sub, "fork")));
    // мусор и неизвестная нагрузка
    assert!(is_rejected(&status_of(&t, &json!({ "fork": { "mode": "x" } }), "fork")));
    assert!(is_rejected(&status_of(
        &t,
        &json!({ "fork": { "mode": "ept", "guest": "4K", "host": "4K", "workload": "nope" } }),
        "fork"
    )));
    // нет целей — нет решения
    let v = t.verify(&json!({}));
    assert!(!v.solved && v.goals.iter().all(|g| g.status == GoalStatus::Missing));
    assert!(!t.verify(&json!(null)).solved);
    assert!(!t.verify(&json!([1, 2])).solved);
}

// ---------------------------------------------------------------- virtq

fn virtq_actions() -> Vec<virtq::Action> {
    use virtq::Action::*;
    vec![
        // batch: две пачки по 3 без подавления — 6 буферов, 2 оповещения
        Post { n: 3 },
        Post { n: 3 },
        // overflow: свободно 2, а кладём 3
        Post { n: 3 },
        // suppress: сбросили очередь, включили подавление, 10 буферов одним оповещением
        Reset,
        Suppress { on: true },
        Post { n: 3 },
        Post { n: 3 },
        Device,
        Device,
        Reap,
        Post { n: 3 },
        Device,
        Reap,
        Post { n: 1 },
    ]
}

#[test]
fn virtq_trace_reaches_every_goal() {
    let t = task("virt-sim-virtqueue");
    let Spec::Virtq { size, goals } = &t.spec else { panic!() };
    let mut s = virtq::Session::new(*size, goals);
    for a in virtq_actions() {
        s.act(&a);
    }
    assert!(s.solved(), "{:?}", s.done());
    assert_eq!(s.done(), ["batch", "overflow", "suppress"]);
    let sub = json!({ "batch": { "trace": virtq_actions() }, "overflow": { "trace": virtq_actions() }, "suppress": { "trace": virtq_actions() } });
    all_verified(&t, &sub);
}

#[test]
fn virtq_model_rules() {
    let t = task("virt-sim-virtqueue");
    let Spec::Virtq { size, goals } = &t.spec else { panic!() };
    let mut s = virtq::Session::new(*size, goals);
    assert_eq!(s.device(), virtq::Note::DeviceIdle);
    assert_eq!(s.post(3), virtq::Note::Notified { n: 3 });
    assert_eq!(s.post(1), virtq::Note::Notified { n: 1 }, "без подавления звонят после каждой отправки");
    s.set_suppress(true);
    assert_eq!(s.post(1), virtq::Note::Quiet { n: 1 }, "устройство занято — звонок не нужен");
    assert_eq!(s.post(4), virtq::Note::Overflow { need: 4, free: 3 });
    assert!(s.state().overflow);
    assert_eq!(s.post(3), virtq::Note::Quiet { n: 3 });
    assert!(!s.state().overflow);
    assert_eq!(virtq::free(*size, s.state()), 0);
    for _ in 0..8 {
        assert_eq!(s.device(), virtq::Note::Processed);
    }
    assert!(!s.state().busy, "доступное кольцо опустело — устройство заснуло");
    assert_eq!(s.device(), virtq::Note::DeviceIdle);
    s.reap();
    assert_eq!(s.state().used, 0);
    // с подавлением, но при спящем устройстве — звонят
    assert_eq!(s.post(1), virtq::Note::Notified { n: 1 });
}

#[test]
fn virtq_verify_traces_and_legacy() {
    let t = task("virt-sim-virtqueue");
    // запись, в которой цель «suppress» не достигается
    let sub = json!({ "suppress": { "trace": [{"op": "post", "n": 3}] } });
    assert!(is_rejected(&status_of(&t, &sub, "suppress")));
    // неизвестное действие
    let sub = json!({ "batch": { "trace": [{"op": "explode"}] } });
    assert!(is_rejected(&status_of(&t, &sub, "batch")));
    // слишком длинная запись
    let long: Vec<_> = (0..virtlab::verify::MAX_TRACE + 1).map(|_| json!({"op": "device"})).collect();
    assert!(is_rejected(&status_of(&t, &json!({ "batch": { "trace": long } }), "batch")));
    // прежний клиент присылает true: принимается по структуре, но не проверен
    let legacy = json!({ "batch": true, "overflow": true, "suppress": true });
    let v = t.verify(&legacy);
    assert!(v.solved);
    assert!(v.goals.iter().all(|g| g.status == GoalStatus::Unverified));
    assert!(!verify_with(&t.spec, &legacy, Strictness::Strict).solved);
    // false — «цели нет», как в JavaScript
    assert_eq!(status_of(&t, &json!({ "batch": false }), "batch"), GoalStatus::Missing);
}

// ---------------------------------------------------------------- qcow2

fn qcow2_actions() -> Vec<qcow2::Action> {
    use qcow2::Action::*;
    vec![
        // deep: цепочка из 4 слоёв, кластер 0 лежит в базе — 4 обращения
        Snapshot,
        Snapshot,
        Snapshot,
        Read { cluster: 0 },
        // squash: две склейки — из 4 слоёв остаётся 2
        Commit,
        Commit,
        // rollback: запись в верхний слой, откат, чтение — данные прежние
        Snapshot,
        Write { cluster: 0, data: "E".into() },
        Revert,
        Read { cluster: 0 },
    ]
}

#[test]
fn qcow2_trace_reaches_every_goal() {
    let t = task("virt-sim-qcow2");
    let Spec::Qcow2 { base, goals, .. } = &t.spec else { panic!() };
    let mut s = qcow2::Session::new(&virtlab::spec::base_map(base), goals);
    for a in qcow2_actions() {
        s.act(&a);
    }
    assert!(s.solved(), "{:?}", s.done());
    assert_eq!(s.done(), ["deep", "squash", "rollback"]);
    assert_eq!(s.chain().len(), 2);
    let tr = json!({ "trace": qcow2_actions() });
    all_verified(&t, &json!({ "deep": tr, "squash": tr, "rollback": tr }));
}

#[test]
fn qcow2_model_rules() {
    let base = qcow2::default_base();
    let chain = qcow2::initial_chain(&base);
    let c = qcow2::snapshot(&chain, 1);
    let (c, copy_up) = qcow2::write(&c, 0, "Z");
    assert!(copy_up, "кластер 0 лежал в базе — копирование при записи");
    let (c, copy_up) = qcow2::write(&c, 7, "Y");
    assert!(!copy_up);
    let r = qcow2::read(&c, 0);
    assert_eq!((r.value.as_deref(), r.depth, r.lookups, r.layer.as_deref()), (Some("Z"), Some(0), 1, Some("слой 1")));
    let r = qcow2::read(&c, 1);
    assert_eq!((r.value.as_deref(), r.depth, r.lookups, r.layer.as_deref()), (Some("B"), Some(1), 2, Some("база")));
    let r = qcow2::read(&c, 5);
    assert_eq!((r.value, r.depth, r.lookups), (None, None, 2));
    let merged = qcow2::commit(&c).unwrap();
    assert_eq!(merged.len(), 1);
    assert_eq!(merged[0].name, "база");
    assert_eq!(merged[0].data[&0], "Z");
    assert!(qcow2::commit(&merged).is_none());
    assert!(qcow2::revert(&merged).is_none());
    assert_eq!(qcow2::revert(&c).unwrap(), chain);
}

#[test]
fn qcow2_verify_traces_and_legacy() {
    let t = task("virt-sim-qcow2");
    // чтение из базы при цепочке в 2 слоя — «deep» не достигается
    let sub = json!({ "deep": { "trace": [{"op": "snapshot"}, {"op": "read", "cluster": 0}] } });
    assert!(is_rejected(&status_of(&t, &sub, "deep")));
    // откат без чтения не подтверждает «rollback»
    let sub = json!({ "rollback": { "trace": [{"op": "snapshot"}, {"op": "write", "cluster": 0, "data": "E"}, {"op": "revert"}] } });
    assert!(is_rejected(&status_of(&t, &sub, "rollback")));
    let legacy = json!({ "deep": true, "squash": true, "rollback": true });
    assert!(t.verify(&legacy).solved);
    assert!(!verify_with(&t.spec, &legacy, Strictness::Strict).solved);
}

// ---------------------------------------------------------------- numa

#[test]
fn numa_plans_reach_every_goal() {
    let t = task("virt-sim-numa");
    let sub = json!({
        "small": {
            "A": {"cpu": "0", "mem": "0", "vnuma": false}, "B": {"cpu": "0", "mem": "0", "vnuma": false},
            "C": {"cpu": "1", "mem": "1", "vnuma": false}, "D": {"cpu": "1", "mem": "1", "vnuma": false},
        },
        "wide": {
            "E": {"cpu": "wide", "mem": "wide", "vnuma": true},
            "F": {"cpu": "0", "mem": "0", "vnuma": true}, "G": {"cpu": "1", "mem": "1", "vnuma": true},
        },
    });
    all_verified(&t, &sub);
}

#[test]
fn numa_verify_rejects_bad_plans() {
    let t = task("virt-sim-numa");
    // всё на узле 0 не помещается (16 ядер на 8)
    let all0: Value = json!({"A": {"cpu": "0", "mem": "0", "vnuma": false}, "B": {"cpu": "0", "mem": "0", "vnuma": false},
        "C": {"cpu": "0", "mem": "0", "vnuma": false}, "D": {"cpu": "0", "mem": "0", "vnuma": false}});
    assert!(is_rejected(&status_of(&t, &json!({ "small": all0 }), "small")));
    // помещается, но память и процессоры на разных узлах: удалённых 25% при пороге 0
    let remote = json!({"A": {"cpu": "0", "mem": "1", "vnuma": false}, "B": {"cpu": "0", "mem": "0", "vnuma": false},
        "C": {"cpu": "1", "mem": "1", "vnuma": false}, "D": {"cpu": "1", "mem": "1", "vnuma": false}});
    assert!(is_rejected(&status_of(&t, &json!({ "small": remote }), "small")));
    // большая машина без виртуальной топологии: 0,5 × 12 / 16 = 37,5% > 20%
    let novnuma = json!({"E": {"cpu": "wide", "mem": "wide", "vnuma": false},
        "F": {"cpu": "0", "mem": "0", "vnuma": false}, "G": {"cpu": "1", "mem": "1", "vnuma": false}});
    assert!(is_rejected(&status_of(&t, &json!({ "wide": novnuma }), "wide")));
    // не хватает машины в плане, несуществующий узел
    assert!(is_rejected(&status_of(&t, &json!({ "small": {"A": {"cpu": "0", "mem": "0", "vnuma": false}} }), "small")));
    let ghost = json!({"A": {"cpu": "5", "mem": "0", "vnuma": false}, "B": {"cpu": "0", "mem": "0", "vnuma": false},
        "C": {"cpu": "1", "mem": "1", "vnuma": false}, "D": {"cpu": "1", "mem": "1", "vnuma": false}});
    assert!(is_rejected(&status_of(&t, &json!({ "small": ghost }), "small")));
    // размещение, не прошедшее вторую цель, не засчитывает всё упражнение
    let ok_small = json!({
        "A": {"cpu": "0", "mem": "0", "vnuma": false}, "B": {"cpu": "0", "mem": "0", "vnuma": false},
        "C": {"cpu": "1", "mem": "1", "vnuma": false}, "D": {"cpu": "1", "mem": "1", "vnuma": false},
    });
    let v = t.verify(&json!({ "small": ok_small }));
    assert!(!v.solved);
    assert_eq!(v.goals[0].status, GoalStatus::Verified);
    assert_eq!(v.goals[1].status, GoalStatus::Missing);
}

#[test]
fn numa_threshold_boundary() {
    // граница: средняя доля ровно 0,1875 (vnuma) проходит порог 0,2, а 0,375 — нет
    let nodes = numa::default_nodes();
    let sc = numa::default_scenarios().remove(1);
    let mut plan = numa::default_plan(&sc.vms);
    plan.insert("E".into(), numa::Placement { cpu: numa::Place::Wide, mem: numa::Place::Wide, vnuma: true });
    plan.insert("G".into(), numa::Placement { cpu: numa::Place::Node(1), mem: numa::Place::Node(1), vnuma: false });
    let ev = numa::evaluate(&nodes, &sc.vms, &plan).unwrap();
    assert!(!ev.over);
    assert_eq!(ev.avg, 0.1875);
    assert!(matches!(numa::accept(&nodes, &sc, &plan).unwrap(), numa::Accept::Ok { .. }));
}

// ---------------------------------------------------------------- migration

fn migration_sub() -> Value {
    json!({
        "calm": { "dirty": 300, "bw": 1250, "downtimeMs": 100, "autoConverge": false, "compress": false, "postcopyAfter": null },
        "busy": { "dirty": 2000, "bw": 1250, "downtimeMs": 50, "autoConverge": true, "compress": true, "postcopyAfter": null },
        "wild": { "dirty": 6000, "bw": 1250, "downtimeMs": 100, "autoConverge": false, "compress": false, "postcopyAfter": 1 },
    })
}

#[test]
fn migration_params_reach_every_goal() {
    let t = task("virt-sim-migration");
    all_verified(&t, &migration_sub());
    // и сами симуляции дают нужные исходы
    let scs = migration::default_scenarios();
    let r = migration::simulate(&scs[0].input(100.0, false, false, None));
    assert_eq!(r.outcome, migration::Outcome::Precopy);
    assert!(r.downtime <= 100);
    let r = migration::simulate(&scs[2].input(100.0, false, false, Some(1)));
    assert_eq!((r.outcome, r.downtime), (migration::Outcome::Postcopy, 20));
}

#[test]
fn migration_verify_rejects_cheating() {
    let t = task("virt-sim-migration");
    let mut sub = migration_sub();
    // «активный гость» без замедления не сходится
    sub["busy"] = json!({ "dirty": 2000, "bw": 1250, "downtimeMs": 600, "autoConverge": false, "compress": false, "postcopyAfter": null });
    assert!(is_rejected(&status_of(&t, &sub, "busy")));
    // подмена скоростей сценария: гость почти не пишет
    sub["busy"] = json!({ "dirty": 1, "bw": 1250, "downtimeMs": 100, "autoConverge": false, "compress": false, "postcopyAfter": null });
    assert!(is_rejected(&status_of(&t, &sub, "busy")));
    // допустимый простой вне слайдера: огромный порог «решает» любую цель
    sub["calm"] = json!({ "dirty": 300, "bw": 1250, "downtimeMs": 1.0e9, "autoConverge": false, "compress": false, "postcopyAfter": null });
    assert!(is_rejected(&status_of(&t, &sub, "calm")));
    sub["calm"] = json!({ "dirty": 300, "bw": 1250, "downtimeMs": 5, "autoConverge": false, "compress": false, "postcopyAfter": null });
    assert!(is_rejected(&status_of(&t, &sub, "calm")));
    // post-copy после 0 или 99 кругов
    sub["wild"] = json!({ "dirty": 6000, "bw": 1250, "downtimeMs": 100, "autoConverge": false, "compress": false, "postcopyAfter": 0 });
    assert!(is_rejected(&status_of(&t, &sub, "wild")));
    sub["wild"] = json!({ "dirty": 6000, "bw": 1250, "downtimeMs": 100, "autoConverge": false, "compress": false, "postcopyAfter": 99 });
    assert!(is_rejected(&status_of(&t, &sub, "wild")));
    // меньше памяти — легче мигрировать
    sub["wild"] = json!({ "dirty": 6000, "bw": 1250, "downtimeMs": 100, "postcopyAfter": 1, "mem": 1024 });
    assert!(is_rejected(&status_of(&t, &sub, "wild")));
    // необязательные поля прежнего клиента можно опустить
    sub["calm"] = json!({ "dirty": 300, "bw": 1250, "downtimeMs": 100 });
    assert_eq!(status_of(&t, &sub, "calm"), GoalStatus::Verified);
    // отрицательные и нечисловые значения
    sub["calm"] = json!({ "dirty": 300, "bw": 1250, "downtimeMs": -100 });
    assert!(is_rejected(&status_of(&t, &sub, "calm")));
    sub["calm"] = json!({ "dirty": "300" });
    assert!(is_rejected(&status_of(&t, &sub, "calm")));
}

// ---------------------------------------------------------------- общее

#[test]
fn every_spec_has_goals_and_is_valid() {
    for c in build_chapters(DEFINITIONS).unwrap() {
        for t in &c.tasks {
            t.spec.validate().unwrap();
            let goals = t.spec.goals();
            assert!(goals.len() >= 2, "{}", t.id);
            assert!(goals.iter().all(|g| !g.text.is_empty()));
            // пустое решение — не решено, ни одна цель не засчитана
            let v = t.verify(&json!({}));
            assert!(!v.solved);
            assert_eq!(v.goals.len(), goals.len());
        }
    }
    assert_eq!(virtlab::LAB_IDS.len(), 6);
    for id in virtlab::LAB_IDS {
        assert!(virtlab::builtin(id).is_some(), "{id}");
    }
    assert!(virtlab::builtin("virt-sim-nope").is_none());
}
