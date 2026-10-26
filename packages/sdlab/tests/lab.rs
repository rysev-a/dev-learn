//! Данные упражнений: самопроверка (порт `sd-selfcheck`), serde round-trip, серверная проверка, сборка под wasm.

mod common;

use std::collections::HashSet;

use sdlab::verify::{problems, self_check};
use sdlab::{parse_solution, verify, verify_raw, Kind, LabChapter, ParamValue, Problem, SdEdge, SdNode, SdState};

#[test]
fn data_is_complete() {
    let chapters = common::chapters();
    assert_eq!(chapters.len(), 24);
    for (i, c) in chapters.iter().enumerate() {
        assert_eq!((c.book, c.chapter, c.lab.as_str()), (18, i as u32 + 1, "sd"));
    }
    assert_eq!(chapters.iter().map(|c| c.tasks.len()).sum::<usize>(), 149);
}

/// Исходная схема не решает упражнение, эталон решает, компоненты эталона — в палитре, id уникальны.
#[test]
fn self_check_all_tasks() {
    let mut ids = HashSet::new();
    let mut bad = Vec::new();
    for c in common::chapters() {
        for t in &c.tasks {
            assert!(ids.insert(t.id.clone()), "id повторяется: {}", t.id);
            let r = self_check(t);
            if !r.is_ok() {
                bad.push(format!(
                    "{}: исходная не проходит ({} из {} целей), эталон проходит: {}, вне палитры: {:?}, много узлов: {}",
                    t.id,
                    r.start_failed,
                    r.start.len(),
                    r.solution.iter().all(|g| g.ok),
                    r.outside,
                    r.too_many
                ));
            }
        }
    }
    assert!(bad.is_empty(), "проблемы:\n{}", bad.join("\n"));
}

#[test]
fn serde_round_trip() {
    for c in common::chapters() {
        // файл данных → текст → тот же файл
        let pretty = sdlab::pretty::to_string(&c).expect("запись");
        assert_eq!(LabChapter::parse(&pretty).expect("чтение"), c, "глава {}", c.chapter);
        // обычный serde_json (без нашего форматирования)
        let compact = serde_json::to_string(&c).expect("запись");
        let back: LabChapter = serde_json::from_str(&compact).expect("чтение");
        assert_eq!(back, c, "глава {}", c.chapter);
        // и через дерево значений
        let v = serde_json::to_value(&c).expect("значение");
        let back: LabChapter = serde_json::from_value(v).expect("чтение");
        assert_eq!(back, c);
    }
}

/// Файл на диске — ровно то, что пишет форматировщик (правки руками не ломают формат молча).
#[test]
fn files_are_canonical() {
    for c in common::chapters() {
        let name = sdlab::data::file_name(c.book, c.chapter);
        let text = std::fs::read_to_string(common::data_dir().join(&name)).expect("чтение");
        assert_eq!(text, sdlab::pretty::to_string(&c).expect("запись"), "{name}: файл не в каноническом виде (cargo run --bin import)");
    }
}

#[test]
fn legacy_names_are_accepted() {
    // имена из TypeScript-версии: dataGB, searchShare, camelCase-параметры
    let json = r#"{"static":1,"read":2,"write":3,"dataGB":4,"hotSet":0.5,"searchShare":0.1,"mediaTB":2,"calls":{"auth":1}}"#;
    let w: sdlab::Workload = serde_json::from_str(json).expect("разбор");
    assert_eq!((w.static_rps, w.read_rps, w.write_rps, w.data_gb), (1.0, 2.0, 3.0, 4.0));
    assert_eq!((w.search_share, w.media_tb), (Some(0.1), Some(2.0)));
    let n: SdNode = serde_json::from_str(r#"{"id":"c","kind":"cache","params":{"sizeGB":8}}"#).expect("разбор");
    assert_eq!(n.num("size_gb"), 8.0);
    assert_eq!(n.name, "");
}

fn task(id: &str) -> sdlab::Task {
    common::chapters().into_iter().flat_map(|c| c.tasks).find(|t| t.id == id).expect("упражнение есть")
}

#[test]
fn verify_accepts_solutions_and_rejects_start() {
    let mut accepted = 0;
    for c in common::chapters() {
        for t in &c.tasks {
            let v = verify(&t.spec, &t.spec.solution);
            assert!(v.ok, "{}: эталон не принят: {:?} {:?}", t.id, v.problems, v.reason());
            assert_eq!(v.goals.len(), t.spec.goals.len());
            let v = verify(&t.spec, &t.spec.start);
            assert!(!v.ok, "{}: исходная схема принята", t.id);
            // решение приходит строкой — как его присылает клиент
            let raw = serde_json::to_string(&t.spec.solution).expect("запись");
            assert!(verify_raw(&t.spec, &raw).expect("разбор").ok, "{}", t.id);
            accepted += 1;
        }
    }
    assert_eq!(accepted, 149);
}

#[test]
fn parse_solution_is_tolerant() {
    let t = task("sd01-wire");
    let s = &t.spec.solution;
    let plain = serde_json::to_string(s).expect("запись");
    // обёртки и двойная сериализация
    let wrapped = format!(r#"{{"state": {plain}}}"#);
    let double = serde_json::to_string(&plain).expect("запись");
    for raw in [plain.clone(), wrapped, double] {
        assert_eq!(&parse_solution(&raw).expect("разбор"), s);
    }
    // без названий и координат (старые черновики)
    let bare = r#"{"nodes":[{"id":"users","kind":"clients"},{"id":"app","kind":"app"},{"id":"db","kind":"db"}],
                  "edges":[{"from":"users","to":"app"},{"from":"app","to":"db"}]}"#;
    let parsed = parse_solution(bare).expect("разбор");
    assert_eq!(parsed.nodes[0].name, "Пользователи");
    assert!(verify(&t.spec, &parsed).ok);
    // мусор — ошибка, а не паника
    for junk in ["", "null", "[]", "{}", r#"{"nodes": 5}"#, r#"{"nodes":[{"id":1}]}"#, r#""x""#, r#"{"nodes":[{"id":"a","kind":"nope"}]}"#] {
        assert!(parse_solution(junk).is_err(), "принято: {junk}");
    }
    assert!(parse_solution(&"x".repeat(2 << 20)).is_err());
}

#[test]
fn verify_rejects_cheating() {
    let t = task("sd01-fleet");
    let sol = t.spec.solution.clone();
    let reject = |s: &SdState, what: &str| {
        let v = verify(&t.spec, s);
        assert!(!v.ok, "принято: {what}");
        v
    };

    // слишком много узлов (и расчёт не запускается)
    let mut s = sol.clone();
    for i in 0..20 {
        s.nodes.push(SdNode::new(&format!("x{i}"), Kind::App, &[]));
    }
    let v = reject(&s, "много узлов");
    assert!(v.problems.iter().any(|p| matches!(p, Problem::TooManyNodes { .. })));
    assert!(v.goals.is_empty());

    // компонент вне палитры
    let mut s = sol.clone();
    s.nodes.push(SdNode::new("c", Kind::Cache, &[]));
    assert!(reject(&s, "вне палитры").problems.iter().any(|p| matches!(p, Problem::OutsidePalette { kind: Kind::Cache, .. })));

    // значение вне диапазона: сто тысяч серверов решили бы любую нагрузку
    let mut s = sol.clone();
    s.nodes.iter_mut().find(|n| n.id == "app").expect("узел").params.insert("instances".into(), ParamValue::Num(100000.0));
    assert!(reject(&s, "вне диапазона").problems.iter().any(|p| matches!(p, Problem::BadParam { .. })));

    // дробное и неизвестный параметр
    let mut s = sol.clone();
    let app = s.nodes.iter_mut().find(|n| n.id == "app").expect("узел");
    app.params.insert("instances".into(), ParamValue::Num(2.5));
    app.params.insert("magic".into(), ParamValue::Bool(true));
    let v = reject(&s, "дробное и неизвестное");
    assert_eq!(v.problems.iter().filter(|p| matches!(p, Problem::BadParam { .. })).count(), 2);

    // скрытый параметр (в этом упражнении повторы к БД не настраиваются)
    let mut s = sol.clone();
    s.nodes.iter_mut().find(|n| n.id == "app").expect("узел").params.insert("weight".into(), ParamValue::Num(10.0));
    assert!(reject(&s, "скрытый параметр").problems.iter().any(|p| matches!(p, Problem::HiddenParam { .. })));

    // цикл, повтор, связь к несуществующему и недопустимая связь
    let mut s = sol.clone();
    s.edges.push(SdEdge::new("lb", "lb"));
    s.edges.push(SdEdge::new("users", "lb"));
    s.edges.push(SdEdge::new("app", "ghost"));
    s.edges.push(SdEdge::new("db", "app"));
    let ps = problems(&t.spec, &s);
    assert!(ps.iter().any(|p| matches!(p, Problem::Cycle { .. })));
    assert!(ps.iter().any(|p| matches!(p, Problem::DuplicateEdge { .. })));
    assert!(ps.iter().any(|p| matches!(p, Problem::UnknownEdgeEnd { .. })));
    assert!(ps.iter().any(|p| matches!(p, Problem::BadLink { .. })));

    // нет пользователей, два пользователя, повтор id, пустая схема
    let mut s = sol.clone();
    s.nodes.retain(|n| n.kind != Kind::Clients);
    s.edges.retain(|e| e.from != "users");
    assert!(reject(&s, "без пользователей").problems.contains(&Problem::NoClients));
    let mut s = sol.clone();
    s.nodes.push(SdNode::new("users2", Kind::Clients, &[]));
    assert!(reject(&s, "два клиента").problems.iter().any(|p| matches!(p, Problem::ManyClients { .. })));
    let mut s = sol.clone();
    s.nodes.push(s.nodes[1].clone());
    assert!(reject(&s, "повтор id").problems.iter().any(|p| matches!(p, Problem::DuplicateNode { .. })));
    assert!(reject(&SdState::default(), "пусто").problems.contains(&Problem::Empty));
    assert!(sol.nodes.len() <= t.spec.max_nodes());
}

/// Схема с циклом не приводит к бесконечной рекурсии: лишняя связь отбрасывается с предупреждением.
#[test]
fn evaluate_survives_cycles() {
    let t = task("sd01-fleet");
    let mut s = t.spec.solution.clone();
    s.edges.push(SdEdge::new("lb", "lb"));
    s.edges.push(SdEdge::new("app", "lb"));
    let r = sdlab::evaluate(&s, &t.spec.workload, &Default::default());
    assert!(r.warnings.iter().any(|w| w.contains("цикл")), "{:?}", r.warnings);
    let base = sdlab::evaluate(&t.spec.solution, &t.spec.workload, &Default::default());
    assert_eq!(r.p50, base.p50);
    assert_eq!(r.success, base.success);
}

#[test]
fn client_copy_has_no_solution() {
    let t = task("sd01-wire");
    let c = t.spec.without_solution();
    assert!(c.solution.nodes.is_empty());
    assert_eq!(c.goals, t.spec.goals);
}

/// Крейт собирается под wasm32 (если цель установлена в тулчейне).
#[test]
fn builds_for_wasm() {
    let sysroot = std::process::Command::new("rustc").args(["--print", "sysroot"]).output().expect("rustc");
    let sysroot = String::from_utf8_lossy(&sysroot.stdout).trim().to_owned();
    if !std::path::Path::new(&sysroot).join("lib/rustlib/wasm32-unknown-unknown").exists() {
        eprintln!("цель wasm32-unknown-unknown не установлена — пропуск");
        return;
    }
    let target_dir = std::env::temp_dir().join("sdlab-wasm-check");
    let cargo = std::env::var("CARGO").unwrap_or_else(|_| "cargo".into());
    let out = std::process::Command::new(cargo)
        .args(["check", "--lib", "--target", "wasm32-unknown-unknown", "--manifest-path"])
        .arg(concat!(env!("CARGO_MANIFEST_DIR"), "/Cargo.toml"))
        .env("CARGO_TARGET_DIR", target_dir)
        .output()
        .expect("запуск cargo");
    assert!(out.status.success(), "{}", String::from_utf8_lossy(&out.stderr));
}
