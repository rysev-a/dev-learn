//! Student solution as data: reading a saved draft and writing the circuit to JSON that the server understands
//! (`archlab::verify`). Pure functions — no interface.

use archlab::{
    blocks::{BlockInstance, BlockSolution, BusWire, GateSolution, Solution},
    exercise::Build,
    model::{GateInstance, UidGen, Wire},
};

/// Student circuit: what is on the board (gates and wires or blocks and buses).
#[derive(Clone, Debug, Default, PartialEq)]
pub struct Drawing {
    pub gates: Vec<GateInstance>,
    pub wires: Vec<Wire>,
    pub instances: Vec<BlockInstance>,
    pub bus_wires: Vec<BusWire>,
}

impl Drawing {
    /// Solution to submit: from gates or from blocks — as the exercise requires.
    pub fn solution(&self, build: Build) -> Solution {
        match build {
            Build::Gates => Solution::Gate(GateSolution { gates: self.gates.clone(), wires: self.wires.clone() }),
            Build::Blocks => Solution::Block(BlockSolution { instances: self.instances.clone(), bus_wires: self.bus_wires.clone() }),
        }
    }

    /// Solution JSON (fields `gates`/`wires` or `instances`/`bus_wires`).
    pub fn json(&self, build: Build) -> String {
        serde_json::to_string(&self.solution(build)).unwrap_or_default()
    }

    /// Nothing is on the board.
    #[cfg(test)]
    pub fn is_empty(&self, build: Build) -> bool {
        match build {
            Build::Gates => self.gates.is_empty() && self.wires.is_empty(),
            Build::Blocks => self.instances.is_empty() && self.bus_wires.is_empty(),
        }
    }

    /// Take the ids already used so that new ones (`g3`, `w7`) do not collide with old ones.
    pub fn reserve_ids(&self, uid: &mut UidGen) {
        let ids: Vec<&str> = self.gates.iter().map(|g| g.id.as_str()).chain(self.wires.iter().map(|w| w.id.as_str())).collect();
        uid.reserve(&ids);
    }
}

/// Circuit from a saved draft; empty or of a foreign shape (not what the exercise needs) — an empty board.
pub fn restore(draft: &str, build: Build) -> Drawing {
    if draft.trim().is_empty() {
        return Drawing::default();
    }
    match (Solution::from_json(draft), build) {
        (Ok(Solution::Gate(g)), Build::Gates) => Drawing { gates: g.gates, wires: g.wires, ..Drawing::default() },
        (Ok(Solution::Block(b)), Build::Blocks) => Drawing { instances: b.instances, bus_wires: b.bus_wires, ..Drawing::default() },
        _ => Drawing::default(),
    }
}

/// First free block instance id of the form `i<n>`, starting from `block count + 1`.
pub fn next_instance_id(instances: &[BlockInstance]) -> String {
    let mut n = instances.len() + 1;
    while instances.iter().any(|i| i.id == format!("i{n}")) {
        n += 1;
    }
    format!("i{n}")
}

#[cfg(test)]
mod tests {
    use super::*;
    use archlab::model::{GateType, PinKind, PinRef};

    fn sample() -> Drawing {
        Drawing {
            gates: vec![GateInstance { id: "g1".into(), ty: GateType::Not, x: 200.0, y: 100.0 }],
            wires: vec![Wire { id: "w2".into(), from: PinRef::out("A"), to: PinRef::inp("g1", PinKind::In0) }],
            ..Drawing::default()
        }
    }

    #[test]
    fn gate_drawing_round_trips_through_json() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let d = sample();
        let json = d.json(Build::Gates);
        assert!(json.contains("\"gates\"") && json.contains("\"wires\""));
        assert_eq!(restore(&json, Build::Gates), d);
    }

    #[test]
    fn block_drawing_round_trips_and_reads_the_old_camel_case_field() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let d = Drawing {
            instances: vec![BlockInstance { id: "i1".into(), block_id: "rom".into(), x: 10.0, y: 20.0 }],
            bus_wires: vec![],
            ..Drawing::default()
        };
        let json = d.json(Build::Blocks);
        assert!(json.contains("bus_wires"));
        assert_eq!(restore(&json, Build::Blocks), d);
        let old = r#"{"instances":[{"id":"i1","blockId":"rom","x":10,"y":20}],"busWires":[]}"#;
        assert_eq!(restore(old, Build::Blocks), d);
    }

    #[test]
    fn foreign_or_broken_drafts_give_an_empty_board() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let gates_json = sample().json(Build::Gates);
        assert!(restore(&gates_json, Build::Blocks).is_empty(Build::Blocks));
        assert_eq!(restore("", Build::Gates), Drawing::default());
        assert_eq!(restore("not json", Build::Gates), Drawing::default());
        assert_eq!(restore("[1,2]", Build::Gates), Drawing::default());
    }

    #[test]
    fn new_ids_continue_after_the_saved_ones() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let d = sample();
        let mut uid = UidGen::new();
        d.reserve_ids(&mut uid);
        assert_eq!(uid.next("g"), "g3");
    }

    #[test]
    fn instance_ids_skip_the_taken_ones() {
        let _ru = locales::guard(i18n::Locale::Ru);
        let mk = |id: &str| BlockInstance { id: id.into(), block_id: "x".into(), x: 0.0, y: 0.0 };
        assert_eq!(next_instance_id(&[]), "i1");
        assert_eq!(next_instance_id(&[mk("i2")]), "i3");
        assert_eq!(next_instance_id(&[mk("i1"), mk("i3")]), "i4");
    }
}
