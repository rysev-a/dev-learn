//! The "Mini-8" processor built from gates, with the same interface as the emulator:
//! step, run until halt, current state. One step — one clock cycle: a whole instruction.
//! Port of `cpu8/gate-machine.ts`.

use super::blocks::cpu8_blocks;
use super::builders::nodes_of;
use super::fast::CompiledSim;
use crate::asm::isa::{MEM_SIZE, PROGRAM_MAX};
use crate::asm::MachineView;
use crate::blocks::{expand, Expansion};
use crate::interfaces::Iface;
use std::sync::OnceLock;

const ROM: &str = "rom__mem";
const RAM: &str = "ram__mem";
const CLK: &str = "clk";

/// The processor circuit is expanded once — that is the most expensive part; after that it can be run any number of times.
pub fn cpu_expansion() -> Option<&'static Expansion> {
    static CACHED: OnceLock<Option<Expansion>> = OnceLock::new();
    CACHED
        .get_or_init(|| {
            let blocks = cpu8_blocks();
            let cpu = blocks.get("c8-cpu")?;
            Some(expand(&cpu.solution, &cpu.def.iface, blocks))
        })
        .as_ref()
}

/// Compiled processor (empty, without a program); copied for every machine.
fn template() -> Result<&'static CompiledSim, String> {
    static TEMPLATE: OnceLock<Result<CompiledSim, String>> = OnceLock::new();
    TEMPLATE
        .get_or_init(|| {
            let exp = cpu_expansion().ok_or(i18n::tr("no block c8-cpu"))?;
            CompiledSim::new(&exp.circuit).map_err(|e| e.to_string())
        })
        .as_ref()
        .map_err(Clone::clone)
}

fn reg_nodes() -> &'static [Vec<String>] {
    static NODES: OnceLock<Vec<Vec<String>>> = OnceLock::new();
    NODES.get_or_init(|| (1..=7).map(|k| nodes_of(&format!("r{k}"), Iface::Byte)).collect())
}

fn pc_nodes() -> &'static [String] {
    static NODES: OnceLock<Vec<String>> = OnceLock::new();
    NODES.get_or_init(|| nodes_of("pc", Iface::Byte))
}

/// Gate-level machine.
#[derive(Debug, Clone)]
pub struct GateMachine {
    pub sim: CompiledSim,
    pub program: Vec<u16>,
    pub steps: u64,
    pub halted: bool,
    pub error: Option<String>,
    pub last_read: Option<usize>,
    pub last_write: Option<usize>,
    pub last_reg: Option<usize>,
}

impl GateMachine {
    /// Machine with a program and initial disk contents.
    pub fn new(program: &[u16], disk: &[u8]) -> Result<GateMachine, String> {
        let mut sim = template()?.clone();
        let rom: Vec<u16> = program.iter().copied().take(PROGRAM_MAX).collect();
        sim.load_rom(ROM, &rom)?;
        sim.load_ram(RAM, disk)?;
        Ok(GateMachine {
            sim,
            program: program.to_vec(),
            steps: 0,
            halted: false,
            error: None,
            last_read: None,
            last_write: None,
            last_reg: None,
        })
    }

    /// Can continue executing.
    pub fn running(&self) -> bool {
        !self.halted && self.error.is_none()
    }

    /// Program counter.
    pub fn pc(&self) -> u32 {
        self.sim.read(pc_nodes()).unwrap_or(0)
    }

    /// Registers r0…r7: the zero register is always zero.
    pub fn regs(&self) -> Vec<u8> {
        let mut v = vec![0u8];
        v.extend(reg_nodes().iter().map(|nodes| self.sim.read(nodes).unwrap_or(0) as u8));
        v
    }

    fn memory(&self) -> Vec<u16> {
        self.sim.memory(RAM).unwrap_or_default()
    }

    /// Execute one instruction (one clock cycle).
    pub fn step(&mut self) {
        if !self.running() {
            return;
        }
        if self.pc() as usize >= self.program.len() {
            self.error = Some(i18n::trf!("Program counter ran past the end of the program (address {0}). Forgot hlt at the end?", self.pc()));
            return;
        }
        let regs_before = self.regs();
        let mem_before = self.memory();
        if let Err(e) = self.sim.pulse(CLK) {
            self.error = Some(e);
            return;
        }
        self.steps += 1;
        self.halted = self.sim.get("halted") == Some(1);

        // what the instruction changed — for highlighting on the disk and at the registers
        let regs_after = self.regs();
        let mem_after = self.memory();
        self.last_reg = regs_after.iter().zip(&regs_before).position(|(a, b)| a != b);
        let mut written = None;
        for i in 0..MEM_SIZE {
            if mem_after.get(i) != mem_before.get(i) {
                written = Some(i);
            }
        }
        self.last_write = written;
        self.last_read = None;
    }

    /// Run until halt, error or the step limit.
    pub fn run(&mut self, max_steps: u64) {
        let mut left = max_steps;
        while self.running() && left > 0 {
            left -= 1;
            self.step();
        }
        if self.running() {
            self.error = Some(i18n::trf!("Step limit of {0} exceeded — the loop probably never ends.", max_steps));
        }
    }

    /// State for the interface.
    pub fn view(&self) -> MachineView {
        MachineView {
            regs: self.regs(),
            pc: self.pc() as i32,
            mem: self.memory().iter().map(|w| *w as u8).collect(),
            halted: self.halted,
            error: self.error.clone(),
            steps: self.steps,
            last_read: self.last_read,
            last_write: self.last_write,
            last_reg: self.last_reg,
        }
    }
}
