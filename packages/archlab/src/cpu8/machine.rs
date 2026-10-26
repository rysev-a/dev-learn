//! Процессор «Мини-8», собранный из вентилей, с тем же интерфейсом, что у эмулятора:
//! шаг, запуск до остановки, текущее состояние. Один шаг — один такт: целая команда.
//! Порт `cpu8/gate-machine.ts`.

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

/// Процессор в виде схемы разворачивается один раз — это самая дорогая часть, дальше можно запускать сколько угодно.
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

/// Скомпилированный процессор (пустой, без программы); копируется для каждой машины.
fn template() -> Result<&'static CompiledSim, String> {
    static TEMPLATE: OnceLock<Result<CompiledSim, String>> = OnceLock::new();
    TEMPLATE
        .get_or_init(|| {
            let exp = cpu_expansion().ok_or("нет блока c8-cpu")?;
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

/// Машина на вентилях.
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
    /// Машина с программой и начальным содержимым диска.
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

    /// Можно выполнять дальше.
    pub fn running(&self) -> bool {
        !self.halted && self.error.is_none()
    }

    /// Счётчик команд.
    pub fn pc(&self) -> u32 {
        self.sim.read(pc_nodes()).unwrap_or(0)
    }

    /// Регистры r0…r7: нулевой всегда ноль.
    pub fn regs(&self) -> Vec<u8> {
        let mut v = vec![0u8];
        v.extend(reg_nodes().iter().map(|nodes| self.sim.read(nodes).unwrap_or(0) as u8));
        v
    }

    fn memory(&self) -> Vec<u16> {
        self.sim.memory(RAM).unwrap_or_default()
    }

    /// Выполнить одну команду (один такт).
    pub fn step(&mut self) {
        if !self.running() {
            return;
        }
        if self.pc() as usize >= self.program.len() {
            self.error = Some(format!("Счётчик команд вышел за пределы программы (адрес {}). Не забыли hlt в конце?", self.pc()));
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

        // что изменила команда — для подсветки на диске и у регистров
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

    /// Выполнять до остановки, ошибки или лимита шагов.
    pub fn run(&mut self, max_steps: u64) {
        let mut left = max_steps;
        while self.running() && left > 0 {
            left -= 1;
            self.step();
        }
        if self.running() {
            self.error = Some(format!("Превышен лимит в {max_steps} шагов — похоже, цикл не заканчивается."));
        }
    }

    /// Состояние для интерфейса.
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
