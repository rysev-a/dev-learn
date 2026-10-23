//! Общее для тестов: золотые результаты прежней реализации на TypeScript и данные курса.
#![allow(dead_code)]

use std::collections::BTreeMap;
use std::path::PathBuf;

use riscvlab::task::{chapter_file_name, LabChapter};
use serde::Deserialize;

/// Каталог данных лабораторий (общий с остальным бэкендом).
pub fn data_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../backend/app/data/labs/arch")
}

/// Загрузить главу из данных курса.
pub fn load_chapter(chapter: u32) -> LabChapter {
    let path = data_dir().join(chapter_file_name(14, chapter));
    let text = std::fs::read_to_string(&path).unwrap_or_else(|e| panic!("нет файла {}: {e}", path.display()));
    LabChapter::from_json(&text).unwrap_or_else(|e| panic!("{}: {e}", path.display()))
}

pub fn load_golden() -> Golden {
    let path = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/golden.json");
    let text = std::fs::read_to_string(&path).unwrap_or_else(|e| panic!("нет {}: {e}", path.display()));
    serde_json::from_str(&text).unwrap_or_else(|e| panic!("golden.json: {e}"))
}

/// Из hex-строки в байты.
pub fn unhex(s: &str) -> Vec<u8> {
    (0..s.len() / 2).map(|i| u8::from_str_radix(&s[2 * i..2 * i + 2], 16).expect("hex")).collect()
}

/// FNV-1a, как в выгрузке.
pub fn fnv(bytes: &[u8]) -> u32 {
    let mut h: u32 = 0x811c_9dc5;
    for b in bytes {
        h ^= u32::from(*b);
        h = h.wrapping_mul(0x0100_0193);
    }
    h
}

#[derive(Deserialize)]
pub struct Golden {
    pub isa: GIsa,
    pub decode: Vec<GDecode>,
    pub asm: Vec<GAsm>,
    pub verdicts: Vec<GVerdictRow>,
    pub runs: Vec<GRun>,
    pub alu: Vec<(String, i32, i32, i32)>,
    pub project: GProject,
}

#[derive(Deserialize)]
pub struct GIsa {
    pub abi: Vec<String>,
    pub ops: Vec<GOp>,
    pub pseudo: Vec<GPseudo>,
    pub mmio: Vec<GMmio>,
    pub reg_names: Vec<GRegName>,
}

#[derive(Deserialize)]
pub struct GOp {
    pub mnemonic: String,
    pub fmt: String,
    pub opcode: u32,
    pub f3: Option<u32>,
    pub f7: Option<u32>,
    pub ext: String,
    pub meaning: String,
    pub example: String,
}

#[derive(Deserialize)]
pub struct GPseudo {
    pub example: String,
    pub becomes: String,
}

#[derive(Deserialize)]
pub struct GMmio {
    pub name: String,
    pub addr: u32,
    pub note: String,
}

#[derive(Deserialize)]
pub struct GRegName {
    pub name: String,
    pub num: Option<u8>,
}

#[derive(Deserialize)]
pub struct GField {
    pub name: String,
    pub bits: String,
    pub cls: String,
}

#[derive(Deserialize)]
pub struct GFields {
    pub fmt: String,
    pub fields: Vec<GField>,
}

#[derive(Deserialize)]
pub struct GDecode {
    pub word: u32,
    pub op: Option<String>,
    pub rd: u8,
    pub rs1: u8,
    pub rs2: u8,
    pub imm: i32,
    pub dis: String,
    pub fields: GFields,
}

#[derive(Deserialize, Debug, PartialEq, Eq)]
pub struct GErr {
    pub line: u32,
    pub message: String,
}

#[derive(Deserialize, Debug, PartialEq, Eq)]
pub struct GLine {
    pub line: u32,
    pub addr: u32,
    pub word: u32,
    pub text: String,
    pub pseudo: bool,
}

#[derive(Deserialize)]
pub struct GAsmResult {
    pub errors: Vec<GErr>,
    pub text_size: usize,
    pub data_size: usize,
    pub entry: u32,
    pub symbols: BTreeMap<String, u32>,
    pub lines: Vec<GLine>,
    pub image_hash: u32,
}

#[derive(Deserialize)]
pub struct GAsm {
    pub name: String,
    pub source: String,
    pub result: GAsmResult,
}

#[derive(Deserialize)]
pub struct GVerdict {
    pub ok: bool,
    pub outcome: String,
    pub message: Option<String>,
    pub errors: Option<Vec<GErr>>,
    pub steps: Option<u64>,
}

#[derive(Deserialize)]
pub struct GVerdictRow {
    pub task: String,
    pub mutation: String,
    pub line: Option<usize>,
    pub program: Option<String>,
    pub verdict: GVerdict,
}

#[derive(Deserialize, Debug, PartialEq, Eq)]
pub struct GLed {
    pub cycle: u64,
    pub value: u8,
}

#[derive(Deserialize, Debug, PartialEq, Eq)]
pub struct GFinal {
    pub regs: Vec<u32>,
    pub pc: u32,
    pub steps: u64,
    pub halted: bool,
    pub exit_code: Option<i32>,
    pub error: Option<String>,
    pub uart: String,
    pub leds: u8,
    pub led_log: Vec<GLed>,
    pub last_read: Option<u32>,
    pub last_write: Option<u32>,
    pub last_reg: Option<u8>,
    pub last_insn: String,
    pub mem_hash: u32,
}

#[derive(Deserialize, Debug, PartialEq, Eq)]
pub struct GTrace {
    pub pc: u32,
    pub insn: String,
    pub last_read: Option<u32>,
    pub last_write: Option<u32>,
    pub last_reg: Option<u8>,
    pub regs: Vec<u32>,
    pub steps: u64,
}

#[derive(Deserialize)]
pub struct GRun {
    pub name: String,
    pub image_hex: String,
    pub regs_init: Vec<(u8, i32)>,
    pub switches: u8,
    pub entry: u32,
    pub max_steps: u64,
    #[serde(rename = "final")]
    pub fin: GFinal,
    pub trace: Option<Vec<GTrace>>,
}

#[derive(Deserialize)]
pub struct GProjectFile {
    pub name: String,
    pub content: String,
    pub note: String,
}

#[derive(Deserialize)]
pub struct GProject {
    pub source: String,
    pub files: Vec<GProjectFile>,
    pub zip_hex: String,
    pub source_with_newline: String,
    pub crc: Vec<(String, u32)>,
}
