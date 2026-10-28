//! Lab exercises as data: chapter, task, check specification.
//!
//! Data file — `backend/data/labs/arch/<book>-<chapter:02>.json` ([`LabChapter`]); the task's `spec`
//! field holds everything the client and the server need. The reference solution (`solution`) is not
//! sent to the client by the backend — see [`Task::for_client`].

use crate::blocks::{BlockInterface, BlockPort, Dir, Solution};
use crate::interfaces::Iface;
use crate::model::{Bit, GateType, InputId};
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// Number of the "Computer Architecture" book.
pub const ARCH_BOOK: u32 = 14;

/// One data file: a book chapter with lab exercises.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct LabChapter {
    pub book: u32,
    pub chapter: u32,
    /// Always `"arch"` for this crate.
    pub lab: String,
    pub tasks: Vec<Task>,
}

/// Exercise: title, statement, hint and check specification.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Task {
    pub id: String,
    pub title: String,
    pub statement: String,
    pub hint: String,
    pub spec: Spec,
}

impl Task {
    /// Copy for the client: without the reference solution.
    pub fn for_client(&self) -> Task {
        let mut t = self.clone();
        match &mut t.spec {
            Spec::Circuit(c) => c.solution = None,
            Spec::Asm(a) => a.solution = String::new(),
        }
        t
    }
}

/// Exercise specification: a circuit (chapters 6–14) or an assembler program (chapter 15).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
#[allow(clippy::large_enum_variant)]
pub enum Spec {
    Circuit(CircuitSpec),
    Asm(AsmSpec),
}

/// How a circuit exercise is checked.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Mode {
    /// Comparison with a truth table.
    Table,
    /// Step-by-step scenario (sequential circuit).
    Steps,
}

/// What the solution is built from.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Build {
    /// From gates.
    Gates,
    /// From ready-made blocks connected by buses.
    Blocks,
}

/// One scenario step for sequential circuits.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Step {
    /// Required toggle state (all active inputs are listed).
    pub inputs: BTreeMap<InputId, Bit>,
    /// Expected output values; an output missing here is not checked on this step.
    pub expect: BTreeMap<String, Bit>,
    /// Step explanation.
    pub text: String,
    /// How many clock pulses to apply before this step (one by default; a step with CLK = 0 — no clock).
    #[serde(default)]
    pub pulses: Option<u32>,
}

/// Group of exercise nodes combined into one port of the given type.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct PortDecl {
    pub name: String,
    #[serde(rename = "type")]
    pub ty: Iface,
    /// Exercise nodes (inputs A–F or output names) in the type's bit order: most significant first.
    pub nodes: Vec<String>,
}

/// A solved exercise becomes a block with this id.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BlockMeta {
    pub id: String,
    pub title: String,
}

/// Circuit exercise.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct CircuitSpec {
    /// Section (slug from the registry): `simple-circuits`, `mux`, …
    pub section: String,
    pub mode: Mode,
    pub build: Build,
    /// Inputs on the board (physical nodes A–F).
    pub inputs: Vec<InputId>,
    /// Input labels (in `inputs` order); empty — the ids themselves.
    #[serde(default)]
    pub labels: Vec<String>,
    /// Output names on the board.
    pub outputs: Vec<String>,
    /// Target table: 2^inputs rows, each row has a value for every output.
    #[serde(default)]
    pub target: Vec<Vec<Bit>>,
    /// Which gates are available in the palette.
    #[serde(default)]
    pub allowed: Vec<GateType>,
    #[serde(default)]
    pub steps: Vec<Step>,
    #[serde(default)]
    pub ports: Vec<PortDecl>,
    #[serde(default)]
    pub block: Option<BlockMeta>,
    /// Which blocks are available in the palette (for `build = blocks`).
    #[serde(default)]
    pub blocks: Vec<String>,
    /// Which input is the clock.
    #[serde(default)]
    pub clock: Option<InputId>,
    /// Steps are reached by clock pulses.
    #[serde(default)]
    pub ticks: bool,
    /// Formula for the title after winning.
    pub formula: String,
    /// Explanation after winning.
    pub success: String,
    /// Reference solution — server only.
    #[serde(default)]
    pub solution: Option<Solution>,
}

impl CircuitSpec {
    /// Input label on the board.
    pub fn label_of(&self, id: InputId) -> String {
        let i = self.inputs.iter().position(|x| *x == id);
        i.and_then(|i| self.labels.get(i).cloned()).unwrap_or_else(|| id.as_str().to_string())
    }

    /// Labels of all inputs in order.
    pub fn labels_or_ids(&self) -> Vec<String> {
        self.inputs.iter().map(|i| self.label_of(*i)).collect()
    }

    /// Exercise interface: its nodes grouped into ports (`interfaceOfExercise`).
    pub fn interface(&self) -> BlockInterface {
        let inputs: Vec<String> = self.inputs.iter().map(|i| i.as_str().to_string()).collect();
        BlockInterface {
            labels: (!self.labels.is_empty()).then(|| self.labels.clone()),
            outputs: self.outputs.clone(),
            ports: self
                .ports
                .iter()
                .map(|p| BlockPort {
                    name: p.name.clone(),
                    ty: p.ty,
                    dir: if p.nodes.iter().all(|n| inputs.contains(n)) { Dir::In } else { Dir::Out },
                    nodes: p.nodes.clone(),
                })
                .collect(),
            inputs,
        }
    }
}

/// Disk area that the interface labels above the memory grid.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct DiskRegion {
    pub name: String,
    pub from: usize,
    pub length: usize,
}

/// Bytes as a string of hex pairs (`"00ff"`) — compact in JSON.
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct HexBytes(pub Vec<u8>);

impl Serialize for HexBytes {
    fn serialize<S: serde::Serializer>(&self, s: S) -> Result<S::Ok, S::Error> {
        let text: String = self.0.iter().map(|b| format!("{b:02x}")).collect();
        s.serialize_str(&text)
    }
}

impl<'de> Deserialize<'de> for HexBytes {
    fn deserialize<D: serde::Deserializer<'de>>(d: D) -> Result<Self, D::Error> {
        let text = String::deserialize(d)?;
        if text.len() % 2 != 0 || !text.is_ascii() {
            return Err(serde::de::Error::custom(i18n::tr("expected a string of hexadecimal pairs")));
        }
        let bytes = (0..text.len() / 2)
            .map(|i| u8::from_str_radix(&text[2 * i..2 * i + 2], 16).map_err(serde::de::Error::custom))
            .collect::<Result<Vec<u8>, D::Error>>()?;
        Ok(HexBytes(bytes))
    }
}

/// Mini-8 assembler exercise: disk and expected memory after halting.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct AsmSpec {
    /// Program starter.
    pub starter: String,
    /// Reference solution — server only.
    #[serde(default)]
    pub solution: String,
    /// Initial disk contents (256 bytes).
    pub disk: HexBytes,
    /// What the memory must be after halting (256 bytes).
    pub expected: HexBytes,
    pub regions: Vec<DiskRegion>,
}
