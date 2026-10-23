//! Дифференциальные тесты: результаты Rust совпадают с «золотыми» результатами TypeScript-движка
//! бит в бит — значения узлов, цепочки `settle`, проверки эталонов и их искажений, блоки и трассы процессора.

mod common;

use archlab::asm::{assemble, isa::disassemble, Machine};
use archlab::check::{check_table, circuit_of, run_steps};
use archlab::cpu8::{cpu8_blocks, cpu_expansion, GateMachine};
use archlab::eval::{evaluate_circuit, settle_circuit};
use archlab::exercise::{CircuitSpec, Mode, Spec};
use archlab::model::*;
use common::*;
use serde_json::{json, Value};

fn hex_bytes(s: &str) -> Vec<u8> {
    (0..s.len() / 2).map(|i| u8::from_str_radix(&s[2 * i..2 * i + 2], 16).expect("hex")).collect()
}

fn inputs_from_int(v: u64) -> InputState {
    let mut s = InputState::zero();
    for (i, id) in INPUT_IDS.iter().enumerate() {
        s.set(*id, ((v >> i) & 1) as Bit);
    }
    s
}

/// Значения узлов как в экспортёре: ключи по порядку, символы 0/1/?.
fn encode(values: &Values) -> (Vec<String>, String) {
    let mut keys: Vec<String> = values.keys().cloned().collect();
    keys.sort();
    let v = keys
        .iter()
        .map(|k| match values[k] {
            None => '?',
            Some(b) => char::from(b'0' + b),
        })
        .collect();
    (keys, v)
}

fn check_encoded(label: &str, got: &Values, want: &Value, keysets: &[Value]) {
    let (keys, v) = encode(got);
    let ks = want["ks"].as_u64().expect("ks") as usize;
    let want_keys: Vec<String> = keysets[ks].as_array().expect("keys").iter().map(|k| k.as_str().expect("key").to_string()).collect();
    assert_eq!(keys, want_keys, "{label}: набор узлов");
    assert_eq!(v, want["v"].as_str().expect("v"), "{label}: значения узлов");
}

fn nv(v: &Value) -> NodeValue {
    v.as_u64().map(|b| b as Bit)
}

#[test]
fn circuits_match_typescript() {
    let lab = lab();
    let lib = lab.reference_library();
    let g = golden();
    let mut n = 0;
    for entry in g["circuits"].as_array().expect("circuits") {
        let (section, id) = (entry["section"].as_str().expect("s"), entry["id"].as_str().expect("id"));
        let label = format!("{section}/{id} {}", entry["mutation"]);
        let (_, spec) = lab.circuit_task(section, id).expect("упражнение");
        let sol = spec.solution.as_ref().expect("эталон");
        let mut circuit = circuit_of(spec, sol, &lib);
        if let Some(i) = entry["mutation"]["drop_wire"].as_u64() {
            circuit.wires.remove(i as usize);
        }
        if let Some(m) = entry["mutation"]["retype"].as_array() {
            let j = m[0].as_u64().expect("j") as usize;
            circuit.gates[j].ty = serde_json::from_value(m[1].clone()).expect("тип");
        }

        // проверка упражнения
        let want = &entry["verdict"];
        match spec.mode {
            Mode::Table => {
                let t = check_table(spec, &circuit);
                assert_eq!(t.ok, want["ok"], "{label}: ok");
                assert_eq!(t.matched as u64, want["passed"], "{label}: совпало строк");
                assert_eq!(t.rows.len() as u64, want["total"], "{label}: строк");
            }
            Mode::Steps => {
                let s = run_steps(spec, &circuit);
                assert_eq!(s.ok, want["ok"], "{label}: ok");
                assert_eq!(s.passed as u64, want["passed"], "{label}: пройдено шагов");
                assert_eq!(s.total as u64, want["total"], "{label}: шагов");
                let want_got: Vec<Vec<NodeValue>> =
                    want["got"].as_array().expect("got").iter().map(|r| r.as_array().expect("row").iter().map(nv).collect()).collect();
                assert_eq!(s.got, want_got, "{label}: выходы по шагам");
            }
        }

        // значения узлов и цепочка settle
        let vectors: Vec<u64> = entry["vectors"].as_array().expect("vectors").iter().map(|v| v.as_u64().expect("v")).collect();
        let keysets = entry["keysets"].as_array().expect("keysets");
        for (i, v) in vectors.iter().enumerate() {
            let inputs = inputs_from_int(*v);
            check_encoded(&format!("{label} eval {v}"), &evaluate_circuit(&circuit, &inputs), &entry["evals"][i], keysets);
        }
        let mut last = Values::new();
        for (i, v) in vectors.iter().enumerate() {
            let r = settle_circuit(&circuit, &inputs_from_int(*v), &last);
            last = if r.stable { r.values.clone() } else { Values::new() };
            let want = &entry["settles"][i];
            assert_eq!(r.stable, want["stable"], "{label} settle {i}: устойчивость");
            check_encoded(&format!("{label} settle {i}"), &r.values, want, keysets);
        }
        n += 1;
    }
    assert!(n > 600, "проверено схем: {n}");
}

#[test]
fn reference_and_empty_verdicts_match_typescript() {
    let lab = lab();
    let lib = lab.reference_library();
    let g = golden();
    for entry in g["verdicts"].as_array().expect("verdicts") {
        let (section, id) = (entry["section"].as_str().expect("s"), entry["id"].as_str().expect("id"));
        let (_, spec): (_, &CircuitSpec) = lab.circuit_task(section, id).expect("упражнение");
        let sol = spec.solution.as_ref().expect("эталон");
        let c = circuit_of(spec, sol, &lib);
        let ok = match spec.mode {
            Mode::Table => check_table(spec, &c).ok,
            Mode::Steps => run_steps(spec, &c).ok,
        };
        assert_eq!(ok, entry["reference"]["ok"], "{section}/{id}: эталон");
        let empty = Circuit::default();
        let (eok, passed, total) = match spec.mode {
            Mode::Table => {
                let t = check_table(spec, &empty);
                (t.ok, t.matched, t.rows.len())
            }
            Mode::Steps => {
                let s = run_steps(spec, &empty);
                (s.ok, s.passed, s.total)
            }
        };
        assert_eq!((eok, passed as u64, total as u64), (entry["empty"]["ok"].as_bool().expect("ok"), entry["empty"]["passed"].as_u64().expect("p"), entry["empty"]["total"].as_u64().expect("t")), "{section}/{id}: пустая схема");
    }
}

#[test]
fn block_expansions_match_typescript() {
    let lab = lab();
    let lib = lab.reference_library();
    let g = golden();
    let list = g["expansions"].as_array().expect("expansions");
    assert_eq!(list.len(), 4, "decode-bus, fetch, exec, cpu");
    for e in list {
        let (section, id) = (e["section"].as_str().expect("s"), e["id"].as_str().expect("id"));
        let (_, spec) = lab.circuit_task(section, id).expect("упражнение");
        let c = circuit_of(spec, spec.solution.as_ref().expect("эталон"), &lib);
        let fp = &e["fingerprint"];
        assert_eq!(
            fingerprint(&c),
            (fp["gates"].as_u64().expect("g") as usize, fp["wires"].as_u64().expect("w") as usize, fp["natives"].as_u64().expect("n") as usize, fp["hash"].as_u64().expect("h") as u32),
            "{section}/{id}: плоская схема"
        );
    }
}

#[test]
fn cpu8_blocks_match_typescript() {
    let g = golden();
    let want = g["blocks"].as_array().expect("blocks");
    let have = cpu8_blocks().all();
    assert_eq!(have.len(), want.len(), "число блоков");
    for (b, w) in have.iter().zip(want) {
        assert_eq!(b.def.id, w["id"].as_str().expect("id"), "порядок блоков");
        let def = serde_json::to_value(&b.def).expect("def");
        assert!(json_eq(&def, &w["def"]), "{}: описание\nrust: {def}\nts:   {}", b.def.id, w["def"]);
        let sol = serde_json::to_value(&b.solution).expect("solution");
        assert!(json_eq(&sol, &w["solution"]), "{}: содержимое", b.def.id);
    }
    let fp = &g["cpuExpansion"];
    let exp = cpu_expansion().expect("процессор разворачивается");
    assert_eq!(
        fingerprint(&exp.circuit),
        (fp["gates"].as_u64().expect("g") as usize, fp["wires"].as_u64().expect("w") as usize, fp["natives"].as_u64().expect("n") as usize, fp["hash"].as_u64().expect("h") as u32),
        "плоская схема процессора"
    );
}

#[test]
fn assembler_matches_typescript() {
    let g = golden();
    let mut sources = 0;
    for e in g["assembler"].as_array().expect("assembler") {
        if e["source"].is_null() {
            let w = e["word"].as_u64().expect("word") as u16;
            assert_eq!(disassemble(w), e["disasm"].as_str().expect("disasm"), "слово {w:#06x}");
            continue;
        }
        sources += 1;
        let src = e["source"].as_str().expect("source");
        let r = assemble(src);
        let got = json!({
            "words": r.words, "lines": r.lines, "labels": r.labels, "errors": r.errors,
        });
        let want = json!({ "words": e["words"], "lines": e["lines"], "labels": e["labels"], "errors": e["errors"] });
        assert!(json_eq(&got, &want), "ассемблер на {src:?}\nrust: {got}\nts:   {want}");
        let dis: Vec<String> = r.words.iter().map(|w| disassemble(*w)).collect();
        assert_eq!(json!(dis), e["disasm"], "дизассемблер на {src:?}");
    }
    assert!(sources > 35, "исходников: {sources}");
}

fn view_json(v: &archlab::asm::MachineView) -> Value {
    json!({
        "regs": v.regs, "pc": v.pc, "mem": v.mem.iter().map(|b| format!("{b:02x}")).collect::<String>(),
        "halted": v.halted, "error": v.error, "steps": v.steps,
        "last_read": v.last_read, "last_write": v.last_write, "last_reg": v.last_reg,
    })
}

#[test]
fn cpu8_traces_match_typescript() {
    let g = golden();
    let list = g["cpu8"].as_array().expect("cpu8");
    assert!(list.len() >= 17);
    for e in list {
        let name = e["name"].as_str().expect("name");
        let disk = hex_bytes(e["disk"].as_str().expect("disk"));
        let asm = assemble(e["source"].as_str().expect("source"));
        assert!(asm.errors.is_empty(), "{name}: {:?}", asm.errors);
        assert_eq!(json!(asm.words), e["words"], "{name}: машинный код");
        let limit = e["limit"].as_u64().expect("limit");

        // эмулятор: первые шаги и итог
        let mut m = Machine::new(&asm.words, &disk);
        for (i, w) in e["emu_first"].as_array().expect("emu_first").iter().enumerate() {
            m.step();
            assert_eq!(json!({"regs": m.regs.to_vec(), "pc": m.pc, "halted": m.halted, "error": m.error}), *w, "{name}: эмулятор, шаг {i}");
        }
        let mut m = Machine::new(&asm.words, &disk);
        m.run(limit);
        assert_eq!(view_json(&m.view()), e["emu"], "{name}: эмулятор, итог");

        // процессор на вентилях: то же самое
        let mut gm = GateMachine::new(&asm.words, &disk).expect("машина на вентилях");
        for (i, w) in e["gate_first"].as_array().expect("gate_first").iter().enumerate() {
            gm.step();
            assert_eq!(json!({"regs": gm.regs(), "pc": gm.pc(), "halted": gm.halted, "error": gm.error}), *w, "{name}: вентили, шаг {i}");
        }
        let mut gm = GateMachine::new(&asm.words, &disk).expect("машина на вентилях");
        gm.run(limit);
        assert_eq!(view_json(&gm.view()), e["gate"], "{name}: вентили, итог");

        // сверка диска с ожидаемым
        if let Some(task) = e.get("check").filter(|c| !c.is_null()) {
            let lab = lab();
            let id = name.strip_prefix("task:").expect("task:");
            let Spec::Asm(spec) = &lab.task(15, id).expect("задача").spec else { panic!("не asm") };
            let r = archlab::asm::tasks::compare(&m.mem, &spec.expected.0);
            assert_eq!((r.ok, r.message.as_str()), (task["ok"].as_bool().expect("ok"), task["message"].as_str().expect("m")), "{name}: сверка");
            for c in e["checks"].as_array().expect("checks") {
                let mem = hex_bytes(c["mem"].as_str().expect("mem"));
                let r = archlab::asm::tasks::compare(&mem, &spec.expected.0);
                assert_eq!((r.ok, r.message.as_str()), (c["ok"].as_bool().expect("ok"), c["message"].as_str().expect("m")), "{name}: сверка искажённого диска");
            }
        }
    }
}

#[test]
fn special_circuits_match_typescript() {
    let g = golden();
    let list = g["specials"].as_array().expect("specials");
    assert!(list.len() >= 15);
    for e in list {
        let name = e["name"].as_str().expect("name");
        let circuit: Circuit = serde_json::from_value(e["circuit"].clone()).expect("схема");
        let vectors: Vec<u64> = e["vectors"].as_array().expect("vectors").iter().map(|v| v.as_u64().expect("v")).collect();
        let keysets = e["keysets"].as_array().expect("keysets");
        for (i, v) in vectors.iter().enumerate() {
            check_encoded(&format!("{name} eval {v}"), &evaluate_circuit(&circuit, &inputs_from_int(*v)), &e["evals"][i], keysets);
        }
        let mut last = Values::new();
        for (i, v) in vectors.iter().enumerate() {
            let r = settle_circuit(&circuit, &inputs_from_int(*v), &last);
            last = if r.stable { r.values.clone() } else { Values::new() };
            assert_eq!(r.stable, e["settles"][i]["stable"], "{name} settle {i}: устойчивость");
            check_encoded(&format!("{name} settle {i}"), &r.values, &e["settles"][i], keysets);
        }
    }
}

#[test]
fn step_order_fallback_matches_typescript() {
    let g = golden();
    for e in g["steps_cases"].as_array().expect("steps_cases") {
        let name = e["name"].as_str().expect("name");
        let spec: CircuitSpec = serde_json::from_value(json!({
            "section": "x", "mode": "steps", "build": "gates", "formula": "", "success": "",
            "inputs": e["ex"]["inputs"], "outputs": e["ex"]["outputs"],
            "steps": e["ex"]["steps"].as_array().expect("steps").iter().map(|s| json!({"inputs": s["inputs"], "expect": s["expect"], "text": s["text"]})).collect::<Vec<_>>(),
        }))
        .expect("спецификация");
        let circuit: Circuit = serde_json::from_value(e["circuit"].clone()).expect("схема");
        let s = run_steps(&spec, &circuit);
        let want = &e["verdict"];
        assert_eq!((s.ok, s.passed as u64, s.total as u64), (want["ok"].as_bool().expect("ok"), want["passed"].as_u64().expect("p"), want["total"].as_u64().expect("t")), "{name}");
        let want_got: Vec<Vec<NodeValue>> = want["got"].as_array().expect("got").iter().map(|r| r.as_array().expect("row").iter().map(nv).collect()).collect();
        assert_eq!(s.got, want_got, "{name}: выходы по шагам");
    }
    // отпускание S = R = 1 удаётся только при определённом порядке: все сразу не проходит, по одному — проходит
    let case = g["steps_cases"].as_array().expect("steps_cases").iter().find(|c| c["name"] == "release-needs-order").expect("случай");
    assert_eq!(case["verdict"]["ok"], true);
}
