//! Порт `lab-selfcheck` и проверки API: эталонные решения проходят, пустые — нет, `verify` отклоняет
//! неверные формы, данные переживают круг serde, составные блоки собираются из решений ученика.

mod common;

use archlab::blocks::*;
use archlab::check::{verify, verify_asm, MAX_GATES};
use archlab::exercise::*;
use archlab::model::*;
use archlab::registry;
use archlab::{ArchLab, DraftStore};
use common::*;

fn solution_json(c: &CircuitSpec) -> String {
    serde_json::to_string(c.solution.as_ref().expect("эталон")).expect("serde")
}

#[test]
fn reference_solutions_pass_and_empty_fail() {
    let lab = lab();
    let lib = lab.reference_library();
    let (mut circuits, mut asm) = (0, 0);
    for ch in lab.chapters() {
        for t in &ch.tasks {
            match &t.spec {
                Spec::Circuit(c) => {
                    circuits += 1;
                    let v = verify(t, &solution_json(c), &lib);
                    assert!(v.ok, "{}/{}: эталон не прошёл: {}", ch.chapter, t.id, v.message);
                    assert_eq!(v.passed, v.total, "{}/{}", ch.chapter, t.id);
                    let empty = match c.build {
                        Build::Gates => r#"{"gates":[],"wires":[]}"#,
                        Build::Blocks => r#"{"instances":[],"bus_wires":[]}"#,
                    };
                    assert!(!verify(t, empty, &lib).ok, "{}/{}: пустое решение прошло", ch.chapter, t.id);
                }
                Spec::Asm(a) => {
                    asm += 1;
                    let v = verify(t, &a.solution, &lib);
                    assert!(v.ok, "asm/{}: эталон не прошёл: {}", t.id, v.message);
                    assert!(!verify(t, &a.starter, &lib).ok, "asm/{}: заготовка прошла", t.id);
                }
            }
        }
    }
    assert_eq!((circuits, asm), (95, 8));
}

#[test]
fn chapters_follow_registry() {
    let lab = lab();
    for n in registry::chapters() {
        let ch = lab.chapter(n).unwrap_or_else(|| panic!("нет главы {n}"));
        assert_eq!(ch.book, 14);
        match registry::lab_kind(n).expect("тип") {
            registry::LabKind::Circuit(slug) => {
                assert!(ch.tasks.iter().all(|t| matches!(&t.spec, Spec::Circuit(c) if c.section == slug)), "глава {n}");
                assert_eq!(registry::chapter_of_slug(slug), Some(n));
            }
            registry::LabKind::Asm => assert!(ch.tasks.iter().all(|t| matches!(t.spec, Spec::Asm(_)))),
        }
    }
    let counts: Vec<usize> = registry::chapters().map(|n| lab.chapter(n).expect("глава").tasks.len()).collect();
    assert_eq!(counts.iter().sum::<usize>(), 103);
    assert_eq!(registry::lab_kind(16), None, "RISC-V — не этот крейт");
}

#[test]
fn legacy_camel_case_solutions_are_accepted() {
    let lab = lab();
    let lib = lab.reference_library();
    let (t, c) = lab.circuit_task("cpu", "fetch").expect("fetch");
    let json = solution_json(c).replace("bus_wires", "busWires").replace("block_id", "blockId");
    assert!(json.contains("busWires") && json.contains("blockId"));
    assert!(verify(t, &json, &lib).ok);
}

#[test]
fn verify_rejects_bad_submissions() {
    let lab = lab();
    let lib = lab.reference_library();
    let (xor, xor_spec) = lab.circuit_task("simple-circuits", "xor").expect("xor");
    let good = solution_json(xor_spec);
    assert!(verify(xor, &good, &lib).ok);

    // не JSON и не схема
    assert!(!verify(xor, "не json", &lib).ok);
    assert!(verify(xor, "[1,2]", &lib).message.contains("объектом"));
    assert!(verify(xor, "{}", &lib).message.contains("ожидалась схема"));
    // схема не той формы
    let v = verify(xor, r#"{"instances":[],"bus_wires":[]}"#, &lib);
    assert!(!v.ok && v.message.contains("из вентилей"), "{}", v.message);
    // недоступный элемент: в «xor» нет XOR
    let cheat = r#"{"gates":[{"id":"x","type":"XOR","x":0,"y":0}],"wires":[
        {"id":"1","from":{"node":"A","pin":"out"},"to":{"node":"x","pin":"in0"}},
        {"id":"2","from":{"node":"B","pin":"out"},"to":{"node":"x","pin":"in1"}},
        {"id":"3","from":{"node":"x","pin":"out"},"to":{"node":"Y","pin":"in0"}}]}"#;
    let v = verify(xor, cheat, &lib);
    assert!(!v.ok && v.message.contains("XOR недоступен"), "{}", v.message);
    // провод от несуществующего узла и от выключенного входа
    let ghost = good.replacen("\"node\":\"A\"", "\"node\":\"nowhere\"", 1);
    assert!(verify(xor, &ghost, &lib).message.contains("такого входа или элемента нет"));
    let (and, _) = lab.circuit_task("simple-circuits", "and").expect("and");
    let off = r#"{"gates":[{"id":"g","type":"AND","x":0,"y":0}],"wires":[
        {"id":"1","from":{"node":"A","pin":"out"},"to":{"node":"g","pin":"in0"}},
        {"id":"2","from":{"node":"F","pin":"out"},"to":{"node":"g","pin":"in1"}},
        {"id":"3","from":{"node":"g","pin":"out"},"to":{"node":"Y","pin":"in0"}}]}"#;
    assert!(verify(and, off, &lib).message.contains("«F»"));
    // слишком большая схема
    let gate = r#"{"id":"g#","type":"AND","x":0,"y":0}"#;
    let many: Vec<String> = (0..=MAX_GATES).map(|i| gate.replace('#', &i.to_string())).collect();
    let big = format!(r#"{{"gates":[{}],"wires":[]}}"#, many.join(","));
    assert!(verify(and, &big, &lib).message.contains("Слишком большая"));
    // имя элемента занято выходом
    let named = good.replace("g_o", "Y");
    assert!(!verify(xor, &named, &lib).ok);
}

#[test]
fn blocks_exercise_checks_palette_and_locks() {
    let lab = lab();
    let (fetch, spec) = lab.circuit_task("cpu", "fetch").expect("fetch");
    let json = solution_json(spec);
    // все блоки закрыты (ученик ничего не решил): блок reg2 недоступен
    let closed = lab.library(&DraftStore::new());
    let v = verify(fetch, &json, &closed);
    assert!(!v.ok && v.message.contains("закрыт") && v.message.contains("Двухбитный регистр"), "{}", v.message);
    // блок вне палитры
    let outside = json.replace("\"block_id\": \"rom\"", "\"block_id\": \"sequencer\"").replace("\"block_id\":\"rom\"", "\"block_id\":\"sequencer\"");
    let v = verify(fetch, &outside, &lab.reference_library());
    assert!(!v.ok && v.message.contains("недоступен"), "{}", v.message);
}

#[test]
fn library_is_built_from_students_solutions() {
    // как `hydrateLab`: решённое переносится между главами, из него собираются блоки
    let lab = lab();
    let mut drafts: Vec<(u32, String, String)> = Vec::new();
    for ch in lab.chapters() {
        for t in &ch.tasks {
            if let Spec::Circuit(c) = &t.spec {
                // «решены» только упражнения, из которых получаются блоки для «Выборки команд»
                let needed = ["reg2-load", "rom4x4", "next-pc"].contains(&t.id.as_str());
                if needed {
                    drafts.push((ch.chapter, t.id.clone(), solution_json(c)));
                }
            }
        }
    }
    assert_eq!(drafts.len(), 3);
    let store = DraftStore::from_drafts(&lab, drafts.iter().map(|(c, i, j)| (*c, i.as_str(), j.as_str())));
    let lib = lab.library(&store);
    for open in ["reg2", "rom", "next-pc", "adapter-w2a", "adapter-a2w"] {
        assert!(lib.available(open), "{open} должен быть открыт");
    }
    for closed in ["decoder", "sequencer", "fetch", "exec", "operand", "flags"] {
        assert!(!lib.available(closed), "{closed} должен быть закрыт");
        assert!(lib.lock_hint(closed).starts_with("Решите «"), "{}", lib.lock_hint(closed));
    }
    let (fetch, spec) = lab.circuit_task("cpu", "fetch").expect("fetch");
    assert!(verify(fetch, &solution_json(spec), &lib).ok, "выборка собирается из решений ученика");
    // испорченный черновик пропускается
    let mut s = DraftStore::new();
    assert!(!s.add("cpu", "reg2-load", "{}"));
    assert!(!s.add("cpu", "reg2-load", "мусор"));
}

#[test]
fn composite_gates_lock_hints() {
    let lab = lab();
    assert_eq!(lab.gate_lock_hint(GateType::Xor), "Соберите «Исключающее ИЛИ» (практика «Простые схемы»)");
    assert_eq!(lab.gate_lock_hint(GateType::And), "");
    assert!(archlab::progress::is_composite(GateType::Dff));
    assert!(!archlab::progress::is_composite(GateType::Nor));
    let solved = |slug: &str, id: &str| slug == "simple-circuits" && id == "xor";
    assert!(archlab::progress::is_gate_unlocked(GateType::Xnor, &solved));
    assert!(!archlab::progress::is_gate_unlocked(GateType::Dff, &solved));
    assert!(archlab::progress::is_gate_unlocked(GateType::And, &solved));
}

#[test]
fn asm_verdicts() {
    let lab = lab();
    let Spec::Asm(a) = &lab.task(15, "patch-byte").expect("задача").spec else { panic!() };
    assert!(verify_asm(a, &a.solution).ok);
    // ошибка ассемблера: строка и текст как в TS
    let v = verify_asm(a, "li r1\nhlt");
    assert!(!v.ok);
    assert_eq!(v.message, "Строка 1: «li» принимает 2 операнда: li rd, число");
    // не остановилась в лимит
    let v = verify_asm(a, "цикл: j цикл");
    assert_eq!(v.message, "Превышен лимит в 100000 шагов — похоже, цикл не заканчивается.");
    // забыли hlt
    assert!(verify_asm(a, "li r1, 1").message.contains("вышел за пределы программы"));
    // не то на диске
    let v = verify_asm(a, "li r1, 'X'\nli r2, 0x10\nsb r1, 0(r2)\nhlt");
    assert_eq!(v.message, "Адрес 0x10: ожидалось 0x4A «J», а лежит 0x58 «X»");
}

#[test]
fn for_client_hides_references() {
    let lab = lab();
    for ch in lab.chapters() {
        for t in lab.tasks_for_client(ch.chapter) {
            match t.spec {
                Spec::Circuit(c) => assert!(c.solution.is_none()),
                Spec::Asm(a) => assert!(a.solution.is_empty()),
            }
        }
    }
    let json = serde_json::to_string(&lab.tasks_for_client(6)).expect("serde");
    assert!(!json.contains("\"gates\":"), "клиенту уходят условия без схем эталонов");
}

#[test]
fn chapter_files_round_trip() {
    for n in registry::chapters() {
        let path = data_dir().join(format!("14-{n:02}.json"));
        let text = std::fs::read_to_string(&path).expect("файл");
        let ch: LabChapter = serde_json::from_str(&text).expect("разбор");
        assert_eq!(archlab::format::canonical_json(&ch).expect("serde"), text, "{}: файл не канонический", path.display());
        // и через значение: ничего не потеряно и не добавлено
        let again: LabChapter = serde_json::from_value(serde_json::to_value(&ch).expect("v")).expect("разбор");
        assert_eq!(again, ch);
    }
}

#[test]
fn solutions_round_trip() {
    let lab = lab();
    for ch in lab.chapters() {
        for t in &ch.tasks {
            if let Spec::Circuit(c) = &t.spec {
                let sol = c.solution.as_ref().expect("эталон");
                let back = Solution::from_json(&serde_json::to_string(sol).expect("serde")).expect("разбор");
                assert_eq!(&back, sol, "{}", t.id);
            }
        }
    }
    for b in archlab::cpu8::cpu8_blocks().all() {
        let back = Solution::from_json(&serde_json::to_string(&b.solution).expect("serde")).expect("разбор");
        assert_eq!(back, b.solution, "{}", b.def.id);
    }
}

#[test]
fn duplicate_or_foreign_files_are_rejected() {
    let lab = lab();
    let ch = lab.chapter(6).expect("глава").clone();
    let mut foreign = ch.clone();
    foreign.lab = "riscv".into();
    assert!(ArchLab::from_chapters(vec![foreign]).is_err());
    assert!(ArchLab::from_chapters(vec![ch.clone(), ch]).is_err());
    let mut dup = lab.chapter(6).expect("глава").clone();
    dup.tasks.push(dup.tasks[0].clone());
    assert!(ArchLab::from_chapters(vec![dup]).is_err());
}

#[test]
fn deserialized_types_are_typed() {
    // набор значений конечен — это типы, а не строки
    let lab = lab();
    let (_, c) = lab.circuit_task("registers", "dff").expect("dff");
    assert_eq!(c.mode, Mode::Steps);
    assert_eq!(c.build, Build::Gates);
    assert_eq!(c.clock, Some(InputId::B));
    let (_, c) = lab.circuit_task("cpu", "cpu").expect("cpu");
    assert_eq!(c.build, Build::Blocks);
    assert!(c.ticks);
    assert_eq!(c.steps[0].pulses, Some(4));
    assert_eq!(c.ports[3].ty, archlab::interfaces::Iface::Phases);
}
