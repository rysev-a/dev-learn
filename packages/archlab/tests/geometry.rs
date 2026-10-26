//! Геометрия и вспомогательное для интерфейса: те же числа и строки, что у TypeScript
//! (`inputYs`, `pinPos`, `wirePath`, `createsCycle`, раскладка блоков, автопроводка, временная диаграмма).

mod common;

use archlab::blocks::*;
use archlab::layout::*;
use archlab::model::*;
use archlab::wave::{build_wave, Sample};
use common::*;
use serde_json::{json, Value};
use std::collections::{BTreeMap, HashMap, HashSet};

fn ymap(v: &Value) -> YMap {
    YMap(v.as_array().expect("карта").iter().map(|p| (p[0].as_str().expect("имя").to_string(), p[1].as_f64().expect("y"))).collect())
}

fn ymap_json(m: &YMap) -> Value {
    json!(m.iter().map(|(k, y)| json!([k, y])).collect::<Vec<_>>())
}

fn point(p: &Point) -> Value {
    json!({"x": p.x, "y": p.y})
}

#[test]
fn board_geometry_matches_typescript() {
    let g = golden();
    let geo = &g["geometry"];
    for e in geo["input_ys"].as_array().expect("input_ys") {
        let ids: Vec<InputId> = serde_json::from_value(e["ids"].clone()).expect("ids");
        assert!(json_eq(&ymap_json(&input_ys(&ids)), &e["ys"]), "input_ys {ids:?}");
    }
    for e in geo["output_ys"].as_array().expect("output_ys") {
        let outs: Vec<String> = serde_json::from_value(e["outputs"].clone()).expect("outputs");
        assert!(json_eq(&ymap_json(&output_ys(&outs)), &e["ys"]), "output_ys {outs:?}");
    }
    for e in geo["pin_pos"].as_array().expect("pin_pos") {
        let gates: Vec<GateInstance> = serde_json::from_value(e["gates"].clone()).expect("gates");
        let input_y = if e["input_y"].is_null() { legacy_input_ys() } else { ymap(&e["input_y"]) };
        let output_y = if e["output_y"].is_null() { YMap::default() } else { ymap(&e["output_y"]) };
        let refs: Vec<PinRef> = serde_json::from_value(e["refs"].clone()).expect("refs");
        for (r, want) in refs.iter().zip(e["pos"].as_array().expect("pos")) {
            assert!(json_eq(&point(&pin_pos(r, &gates, &output_y, &input_y)), want), "pin_pos {r:?}");
        }
    }
    for e in geo["wire_path"].as_array().expect("wire_path") {
        let a: Point = serde_json::from_value(e["a"].clone()).expect("a");
        let b: Point = serde_json::from_value(e["b"].clone()).expect("b");
        assert_eq!(wire_path(a, b), e["path"].as_str().expect("path"));
    }
    let lab = lab();
    let lib = lab.reference_library();
    for e in geo["cycles"].as_array().expect("cycles") {
        let (section, id) = (e["section"].as_str().expect("s"), e["id"].as_str().expect("id"));
        let (_, spec) = lab.circuit_task(section, id).expect("упражнение");
        let c = archlab::check::circuit_of(spec, spec.solution.as_ref().expect("эталон"), &lib);
        for (p, want) in e["proposals"].as_array().expect("proposals").iter().zip(e["result"].as_array().expect("result")) {
            let from: PinRef = serde_json::from_value(p["from"].clone()).expect("from");
            let to: PinRef = serde_json::from_value(p["to"].clone()).expect("to");
            assert_eq!(creates_cycle(&c, &from, &to), want.as_bool().expect("bool"), "{section}/{id}: {from:?} → {to:?}");
        }
    }
}

fn defs_by_id() -> HashMap<String, BlockDef> {
    let lab = lab();
    let mut defs: HashMap<String, BlockDef> = lab.reference_library().defs().map(|d| (d.id.clone(), (**d).clone())).collect();
    for b in archlab::cpu8::cpu8_blocks().all() {
        defs.insert(b.def.id.clone(), b.def.clone());
    }
    defs
}

fn side_name(s: PinSide) -> &'static str {
    if s == PinSide::In {
        "in"
    } else {
        "out"
    }
}

#[test]
fn block_layout_matches_typescript() {
    let g = golden();
    let geo = &g["geometry"];
    let defs = defs_by_id();
    for e in geo["boxes"].as_array().expect("boxes") {
        let id = e["id"].as_str().expect("id");
        let def = &defs[id];
        let open: HashSet<String> = e["expanded"].as_array().expect("expanded").iter().map(|k| k.as_str().expect("k").to_string()).collect();
        let b = layout_box("x", &def.title, &def.iface.ports, &open, (150.0, 30.0, BLOCK_W), BoxKind::Block);
        assert!(json_eq(&json!(b.h), &e["h"]), "{id}: высота");
        let rows: Vec<Value> = b
            .rows
            .iter()
            .map(|r| {
                json!({"key": r.key, "name": r.name, "type": r.ty.name(), "depth": r.depth, "side": side_name(r.side),
                       "y": r.y, "expandable": r.expandable, "expanded": r.expanded, "nodes": r.nodes})
            })
            .collect();
        assert!(json_eq(&json!(rows), &e["rows"]), "{id}: строки портов");
        let pins: Vec<Value> = b.rows.iter().map(|r| point(&pin_center(&b, r))).collect();
        assert!(json_eq(&json!(pins), &e["pins"]), "{id}: пины");
    }
    for e in geo["side_boxes"].as_array().expect("side_boxes") {
        let id = e["id"].as_str().expect("id");
        let (i, o) = side_boxes(&defs[id].iface.ports, &HashSet::new(), 880.0, 16.0);
        assert!(json_eq(&json!(i.h), &e["in_h"]) && json_eq(&json!(o.h), &e["out_h"]), "{id}: высоты колонок");
        let rows = |b: &BoxLayout| json!(b.rows.iter().map(|r| json!([r.key, r.y, side_name(r.side)])).collect::<Vec<_>>());
        assert!(json_eq(&rows(&i), &e["in_rows"]) && json_eq(&rows(&o), &e["out_rows"]), "{id}: строки колонок");
    }
    for e in geo["free_spot"].as_array().expect("free_spot") {
        let taken: Vec<(f64, f64)> = e["taken"].as_array().expect("taken").iter().map(|p| (p["x"].as_f64().expect("x"), p["y"].as_f64().expect("y"))).collect();
        let (x, y) = free_spot(&taken, e["board_w"].as_f64().expect("w"));
        assert!(json_eq(&json!({"x": x, "y": y}), &e["spot"]), "free_spot {taken:?}");
    }
}

fn auto_json(list: &[AutoWire]) -> Value {
    json!(list.iter().map(|a| json!({"from": a.from, "to": a.to, "a": point(&a.a), "b": point(&a.b)})).collect::<Vec<_>>())
}

fn auto_from_json(v: &Value) -> Vec<AutoWire> {
    v.as_array()
        .expect("список")
        .iter()
        .map(|a| AutoWire {
            from: serde_json::from_value(a["from"].clone()).expect("from"),
            to: serde_json::from_value(a["to"].clone()).expect("to"),
            a: serde_json::from_value(a["a"].clone()).expect("a"),
            b: serde_json::from_value(a["b"].clone()).expect("b"),
        })
        .collect()
}

#[test]
fn auto_wire_matches_typescript() {
    let g = golden();
    let list = g["geometry"]["auto_wire"].as_array().expect("auto_wire");
    assert!(list.len() > 100);
    let mut nonempty = 0;
    for e in list {
        let label = format!("{}/{} радиус {}", e["section"], e["id"], e["radius"]);
        let gate: GateInstance = serde_json::from_value(e["gate"].clone()).expect("gate");
        let gates: Vec<GateInstance> = serde_json::from_value(e["gates"].clone()).expect("gates");
        let wires: Vec<Wire> = serde_json::from_value(e["wires"].clone()).expect("wires");
        let (input_y, output_y) = (ymap(&e["input_y"]), ymap(&e["output_y"]));
        let radius = e["radius"].as_f64();
        let steps_mode = e["steps_mode"].as_bool().expect("steps_mode");
        let first = suggest_wires(&AutoWireInput { gate: &gate, gates: &gates, wires: &wires, input_y: &input_y, output_y: &output_y, steps_mode, radius, keep: &[] });
        assert!(json_eq(&auto_json(&first), &e["first"]), "{label}: первая подстановка\nrust: {}\nts:   {}", auto_json(&first), e["first"]);
        nonempty += !first.is_empty() as usize;
        let moved: GateInstance = serde_json::from_value(e["again_gate"].clone()).expect("again_gate");
        let again = suggest_wires(&AutoWireInput { gate: &moved, gates: &gates, wires: &wires, input_y: &input_y, output_y: &output_y, steps_mode, radius, keep: &auto_from_json(&e["first"]) });
        assert!(json_eq(&auto_json(&again), &e["again"]), "{label}: повторная подстановка");
    }
    assert!(nonempty > 100, "непустых подстановок: {nonempty}");
}

#[test]
fn wave_matches_typescript() {
    let g = golden();
    let lab = lab();
    let list = g["geometry"]["wave"].as_array().expect("wave");
    assert!(list.len() >= 10);
    for e in list {
        let (section, id) = (e["section"].as_str().expect("s"), e["id"].as_str().expect("id"));
        let (_, spec) = lab.circuit_task(section, id).expect("упражнение");
        let samples: Vec<Sample> = e["samples"]
            .as_array()
            .expect("samples")
            .iter()
            .map(|s| Sample {
                inputs: serde_json::from_value::<BTreeMap<InputId, Bit>>(s["inputs"].clone()).expect("inputs"),
                outputs: s["outputs"].as_object().expect("outputs").iter().map(|(k, v)| (k.clone(), v.as_u64().map(|b| b as Bit))).collect(),
            })
            .collect();
        let w = build_wave(&samples, spec);
        let want = &e["wave"];
        assert!(json_eq(&json!(w.height), &want["height"]), "{section}/{id}: высота");
        assert!(json_eq(&json!(w.cols), &want["cols"]), "{section}/{id}: колонки");
        assert!(json_eq(&json!(w.last_x), &want["lastX"]), "{section}/{id}: lastX");
        let rows = want["rows"].as_array().expect("rows");
        assert_eq!(w.rows.len(), rows.len());
        for (r, t) in w.rows.iter().zip(rows) {
            assert_eq!(r.label, t["label"].as_str().expect("label"), "{section}/{id}");
            assert_eq!(serde_json::to_value(r.kind).expect("kind"), t["kind"], "{section}/{id}: {}", r.label);
            assert_eq!(r.top, t["top"].as_f64().expect("top"));
            assert_eq!(r.d, t["d"].as_str().expect("d"), "{section}/{id}: {} d", r.label);
            assert_eq!(r.dx, t["dx"].as_str().expect("dx"), "{section}/{id}: {} dx", r.label);
        }
    }
}

#[test]
fn small_pieces() {
    use archlab::interfaces::*;
    // типы совместимы только по имени
    assert!(!can_connect(Iface::Word2, Iface::Addr2));
    assert!(can_connect(Iface::Word2, Iface::Word2));
    assert_eq!(Iface::Instr.width(), 4);
    assert_eq!(Iface::Ctrl.width(), 18);
    assert_eq!(Iface::Instr16.width(), 16);
    assert_eq!(leaf_paths(Iface::Instr, ""), ["op.Op1", "op.Op0", "k.D1", "k.D0"]);
    assert_eq!(leaf_paths(Iface::Bit, ""), [""]);
    let s = slice_of(Iface::Instr16, "c.I3").expect("поле");
    assert_eq!((s.ty, s.offset, s.length), (Iface::Bit, 12, 1));
    let s = slice_of(Iface::Instr, "k").expect("поле");
    assert_eq!((s.ty, s.offset, s.length), (Iface::Word2, 2, 2));
    assert!(slice_of(Iface::Instr, "zzz").is_none());
    assert_eq!(child_fields(Iface::Instr, "k").iter().map(|f| f.path.as_str()).collect::<Vec<_>>(), ["k.D1", "k.D0"]);
    assert_eq!(bus_text(&[Some(1), None, Some(0)]), "1?0");
    assert_eq!(Iface::parse("Phases"), Some(Iface::Phases));
    assert_eq!(Iface::parse("Nope"), None);
    // выдача id
    let mut u = UidGen::new();
    u.reserve(&["g3", "w7", "x"]);
    assert_eq!(u.next("g"), "g8");
    assert_eq!(u.next("w"), "w9");
    // тумблеры
    let mut st = InputState::zero();
    st.set(InputId::A, 1);
    st.set(InputId::C, 1);
    assert_eq!(st.row(&[InputId::A, InputId::B, InputId::C]), 0b101);
    assert_eq!(inputs_for_row(&[InputId::A, InputId::B, InputId::C], 0b011).0, [0, 1, 1, 0, 0, 0]);
}
