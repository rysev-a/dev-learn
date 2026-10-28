//! RV32IM processor: registers, memory, peripherals. One "step" is one instruction.
//!
//! Address map of the "soft" processor — as on the educational FPGA board:
//! * `0x0000_0000 … 0x0000_3FFF` — 16 KiB of RAM (instructions, data, stack);
//! * `0x1000_0000` UART: writing a byte — output a character; reading `+4` — "transmitter ready" (1);
//! * `0x1000_1000` LEDs: write — light up (low 8 bits); read — what was written;
//! * `0x1000_1004` switches: read — their state (8 bits);
//! * `0x1000_2000` timer: read — number of executed instructions (low 32 bits).

use serde::{Deserialize, Serialize};

use crate::asm::{RAM_SIZE, STACK_TOP};
use crate::isa::{decode, disassemble, Op};
use crate::js::hex32;

/// UART: write a byte.
pub const UART_TX: u32 = 0x1000_0000;
/// UART: status (always "ready").
pub const UART_STATUS: u32 = 0x1000_0004;
/// LEDs.
pub const LEDS: u32 = 0x1000_1000;
/// Switches.
pub const SWITCHES: u32 = 0x1000_1004;
/// Timer: number of executed instructions.
pub const TIMER: u32 = 0x1000_2000;

/// Reference row for device addresses.
#[derive(Clone, Copy, Debug)]
pub struct MmioRegion {
    /// device name
    pub name: &'static str,
    /// device address
    pub addr: u32,
    /// explanation for the reference
    pub note: &'static str,
}

/// Devices visible to the program as ordinary addresses.
pub const MMIO_MAP: &[MmioRegion] = &[
    MmioRegion {
        name: i18n::t!("UART — output"), addr: UART_TX, note: i18n::t!("sb: the written byte appears in the console")
    },
    MmioRegion {
        name: i18n::t!("UART — status"), addr: UART_STATUS, note: i18n::t!("lw: 1 when the next byte can be sent")
    },
    MmioRegion {
        name: i18n::t!("LEDs"), addr: LEDS, note: i18n::t!("sw: the low 8 bits light LED0…LED7")
    },
    MmioRegion {
        name: i18n::t!("Switches"), addr: SWITCHES, note: i18n::t!("lw: the 8 switches SW0…SW7")
    },
    MmioRegion { name: i18n::t!("Timer"), addr: TIMER, note: i18n::t!("lw: how many instructions have been executed so far") },
];

/// Default step limit for `run` (as in the UI).
pub const DEFAULT_MAX_STEPS: u64 = 1_000_000;

/// LED log entry: on which cycle and what was written.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct LedEvent {
    /// on which cycle (how many instructions have been executed)
    pub cycle: u64,
    /// written value (8 bits)
    pub value: u8,
}

/// Snapshot of the machine state for checks and the UI.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct View {
    /// registers, unsigned
    pub regs: Vec<u32>,
    /// program counter (if it went negative — as two's complement modulo 2³²)
    pub pc: u32,
    /// memory (`RAM_SIZE` bytes)
    pub mem: Vec<u8>,
    /// how many instructions have been executed
    pub steps: u64,
    /// the program has halted (ebreak or exit)
    pub halted: bool,
    /// return code, if the program called exit
    pub exit_code: Option<i32>,
    /// machine error message, if it broke
    pub error: Option<String>,
    /// everything the program printed (UART or write), as UTF-8 text
    pub uart: String,
    /// LEDs: last written value
    pub leds: u8,
    /// log of LED writes
    pub led_log: Vec<LedEvent>,
    /// address of the last memory read/write and which register the last instruction changed
    pub last_read: Option<u32>,
    /// address of the last write
    pub last_write: Option<u32>,
    /// which register the last instruction changed
    pub last_reg: Option<u8>,
    /// text of the last executed instruction
    pub last_insn: String,
}

/// Run parameters.
#[derive(Clone, Copy, Debug, Default)]
pub struct Options {
    /// switch positions
    pub switches: u8,
    /// address to start from
    pub entry: u32,
}

/// One trace entry: what was executed and what changed.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TraceStep {
    /// address of the executed instruction
    pub pc: u32,
    /// its text
    pub insn: String,
    /// address of the last memory or device read
    pub last_read: Option<u32>,
    /// address of the last write
    pub last_write: Option<u32>,
    /// which register the last instruction changed
    pub last_reg: Option<u8>,
    /// registers after the instruction
    pub regs: Vec<u32>,
    /// number of executed instructions after the step
    pub steps: u64,
}

/// RV32IM processor with memory and peripherals.
#[derive(Clone, Debug)]
pub struct Machine {
    /// registers
    pub regs: [i32; 32],
    /// memory (`RAM_SIZE` bytes)
    pub mem: Vec<u8>,
    /// program counter
    pub pc: i64,
    /// how many instructions have been executed
    pub steps: u64,
    /// the program has halted (ebreak or exit)
    pub halted: bool,
    /// return code, if the program called exit
    pub exit_code: Option<i32>,
    /// machine error message, if it broke
    pub error: Option<String>,
    /// everything the program printed (bytes)
    pub uart: Vec<u8>,
    /// LEDs: last written value
    pub leds: u8,
    /// log of LED writes
    pub led_log: Vec<LedEvent>,
    /// switch positions (8 bits)
    pub switches: u8,
    /// address of the last memory or device read
    pub last_read: Option<u32>,
    /// address of the last write
    pub last_write: Option<u32>,
    /// which register the last instruction changed
    pub last_reg: Option<u8>,
    /// text of the last executed instruction
    pub last_insn: String,
}

impl Machine {
    /// Machine with a memory image; `sp` — top of the stack, as set by the loader.
    pub fn new(image: &[u8], opts: Options) -> Machine {
        let mut mem = vec![0u8; RAM_SIZE];
        let n = image.len().min(RAM_SIZE);
        mem[..n].copy_from_slice(&image[..n]);
        let mut regs = [0i32; 32];
        regs[2] = STACK_TOP as i32;
        Machine {
            regs,
            mem,
            pc: i64::from(opts.entry),
            steps: 0,
            halted: false,
            exit_code: None,
            error: None,
            uart: Vec::new(),
            leds: 0,
            led_log: Vec::new(),
            switches: opts.switches,
            last_read: None,
            last_write: None,
            last_reg: None,
            last_insn: String::new(),
        }
    }

    /// Put a value into a register before the run (x0 does not change).
    pub fn set_reg(&mut self, reg: u8, value: i32) {
        if reg != 0 && usize::from(reg) < 32 {
            self.regs[usize::from(reg)] = value;
        }
    }

    /// The machine can still execute instructions.
    pub fn running(&self) -> bool {
        !self.halted && self.error.is_none()
    }

    fn fault(&mut self, message: String) {
        self.error = Some(message);
    }

    /* ---------- memory and peripherals ---------- */

    fn load(&mut self, addr: i64, size: u32) -> Option<u32> {
        let a = addr as u32;
        self.last_read = Some(a);
        if a >= 0x1000_0000 {
            return match a & !3 {
                UART_STATUS => Some(1),
                LEDS => Some(u32::from(self.leds)),
                SWITCHES => Some(u32::from(self.switches)),
                TIMER => Some(self.steps as u32),
                UART_TX => Some(0),
                _ => {
                    self.fault(i18n::trf!("Read from address {0}: there is no device there", hex32(a)));
                    None
                }
            };
        }
        if a as usize + size as usize > RAM_SIZE {
            self.fault(i18n::trf!("Read from address {0} is outside memory (0x0 … {1})", hex32(a), hex32(RAM_SIZE as u32 - 1)));
            return None;
        }
        if !a.is_multiple_of(size) {
            self.fault(i18n::trf!("Misaligned read at address {0}: a {1} must be at an address that is a multiple of {2}", hex32(a), if size == 4 { i18n::tr("word") } else { i18n::tr("halfword") }, size));
            return None;
        }
        let mut v: u32 = 0;
        for k in (0..size).rev() {
            v = (v << 8) | u32::from(self.mem[(a + k) as usize]);
        }
        Some(v)
    }

    fn store(&mut self, addr: i64, size: u32, value: u32) -> bool {
        let a = addr as u32;
        self.last_write = Some(a);
        if a >= 0x1000_0000 {
            return match a & !3 {
                UART_TX => {
                    self.uart.push(value as u8);
                    true
                }
                LEDS => {
                    self.leds = value as u8;
                    self.led_log.push(LedEvent { cycle: self.steps, value: self.leds });
                    true
                }
                _ => {
                    self.fault(i18n::trf!("Write to address {0}: this device cannot be written", hex32(a)));
                    false
                }
            };
        }
        if a as usize + size as usize > RAM_SIZE {
            self.fault(i18n::trf!("Write to address {0} is outside memory (0x0 … {1})", hex32(a), hex32(RAM_SIZE as u32 - 1)));
            return false;
        }
        if !a.is_multiple_of(size) {
            self.fault(i18n::trf!("Misaligned write at address {0}: a {1} must be at an address that is a multiple of {2}", hex32(a), if size == 4 { i18n::tr("word") } else { i18n::tr("halfword") }, size));
            return false;
        }
        for k in 0..size {
            self.mem[(a + k) as usize] = (value >> (8 * k)) as u8;
        }
        true
    }

    /* ---------- execution ---------- */

    /// Execute one instruction (does nothing if the machine is halted or broken).
    pub fn step(&mut self) {
        if !self.running() {
            return;
        }
        let pc = self.pc;
        self.last_read = None;
        self.last_write = None;
        self.last_reg = None;
        if pc % 4 != 0 || pc < 0 || pc + 4 > RAM_SIZE as i64 {
            self.fault(i18n::trf!("The program counter left memory (address {0}). Did you forget ebreak at the end?", hex32(pc as u32)));
            return;
        }
        let p = pc as usize;
        let word = u32::from_le_bytes([self.mem[p], self.mem[p + 1], self.mem[p + 2], self.mem[p + 3]]);
        let d = decode(word);
        self.last_insn = disassemble(word);
        let Some(op) = d.op else {
            self.fault(i18n::trf!("Unrecognized instruction {0} at address {1}. The program may have reached the end without ebreak, or “run away” into the data", hex32(word), hex32(pc as u32)));
            return;
        };

        let a = self.regs[usize::from(d.rs1)];
        let b = self.regs[usize::from(d.rs2)];
        let imm = d.imm;
        let mut next = pc + 4;
        let mut result: Option<i32> = None;

        match op {
            Op::Add => result = Some(a.wrapping_add(b)),
            Op::Sub => result = Some(a.wrapping_sub(b)),
            Op::Sll => result = Some(a << (b & 31)),
            Op::Slt => result = Some(i32::from(a < b)),
            Op::Sltu => result = Some(i32::from((a as u32) < (b as u32))),
            Op::Xor => result = Some(a ^ b),
            Op::Srl => result = Some(((a as u32) >> (b & 31)) as i32),
            Op::Sra => result = Some(a >> (b & 31)),
            Op::Or => result = Some(a | b),
            Op::And => result = Some(a & b),
            Op::Mul => result = Some(a.wrapping_mul(b)),
            Op::Mulh => result = Some(((i64::from(a) * i64::from(b)) >> 32) as i32),
            Op::Mulhsu => result = Some(((i64::from(a) * i64::from(b as u32)) >> 32) as i32),
            Op::Mulhu => result = Some(((u64::from(a as u32) * u64::from(b as u32)) >> 32) as i32),
            // division by zero gives −1, overflow (−2³¹ / −1) gives −2³¹ (as the specification requires)
            Op::Div => result = Some(if b == 0 { -1 } else { a.wrapping_div(b) }),
            Op::Divu => result = Some(if b == 0 { -1 } else { ((a as u32) / (b as u32)) as i32 }),
            Op::Rem => result = Some(if b == 0 { a } else { a.wrapping_rem(b) }),
            Op::Remu => result = Some(if b == 0 { a } else { ((a as u32) % (b as u32)) as i32 }),

            Op::Addi => result = Some(a.wrapping_add(imm)),
            Op::Slti => result = Some(i32::from(a < imm)),
            Op::Sltiu => result = Some(i32::from((a as u32) < (imm as u32))),
            Op::Xori => result = Some(a ^ imm),
            Op::Ori => result = Some(a | imm),
            Op::Andi => result = Some(a & imm),
            Op::Slli => result = Some(a << imm),
            Op::Srli => result = Some(((a as u32) >> imm) as i32),
            Op::Srai => result = Some(a >> imm),

            Op::Lb => {
                let Some(v) = self.load(i64::from(a) + i64::from(imm), 1) else { return };
                result = Some(((v << 24) as i32) >> 24);
            }
            Op::Lh => {
                let Some(v) = self.load(i64::from(a) + i64::from(imm), 2) else { return };
                result = Some(((v << 16) as i32) >> 16);
            }
            Op::Lw => {
                let Some(v) = self.load(i64::from(a) + i64::from(imm), 4) else { return };
                result = Some(v as i32);
            }
            Op::Lbu => {
                let Some(v) = self.load(i64::from(a) + i64::from(imm), 1) else { return };
                result = Some(v as i32);
            }
            Op::Lhu => {
                let Some(v) = self.load(i64::from(a) + i64::from(imm), 2) else { return };
                result = Some(v as i32);
            }
            Op::Sb => {
                if !self.store(i64::from(a) + i64::from(imm), 1, b as u32) {
                    return;
                }
            }
            Op::Sh => {
                if !self.store(i64::from(a) + i64::from(imm), 2, b as u32) {
                    return;
                }
            }
            Op::Sw => {
                if !self.store(i64::from(a) + i64::from(imm), 4, b as u32) {
                    return;
                }
            }

            Op::Beq => {
                if a == b {
                    next = pc + i64::from(imm);
                }
            }
            Op::Bne => {
                if a != b {
                    next = pc + i64::from(imm);
                }
            }
            Op::Blt => {
                if a < b {
                    next = pc + i64::from(imm);
                }
            }
            Op::Bge => {
                if a >= b {
                    next = pc + i64::from(imm);
                }
            }
            Op::Bltu => {
                if (a as u32) < (b as u32) {
                    next = pc + i64::from(imm);
                }
            }
            Op::Bgeu => {
                if (a as u32) >= (b as u32) {
                    next = pc + i64::from(imm);
                }
            }

            Op::Jal => {
                result = Some((pc + 4) as i32);
                next = pc + i64::from(imm);
            }
            Op::Jalr => {
                result = Some((pc + 4) as i32);
                next = i64::from(((i64::from(a) + i64::from(imm)) as i32) & !1);
            }
            Op::Lui => result = Some(((imm as u32) << 12) as i32),
            Op::Auipc => result = Some((pc as i32).wrapping_add(((imm as u32) << 12) as i32)),

            Op::Ebreak => self.halted = true,
            Op::Ecall => {
                if !self.syscall() {
                    return;
                }
            }
        }

        if let Some(v) = result {
            if d.rd != 0 {
                self.regs[usize::from(d.rd)] = v;
                self.last_reg = Some(d.rd);
            }
        }
        self.regs[0] = 0;
        if !self.halted && next % 4 != 0 {
            self.fault(i18n::trf!("Jump to address {0}, which is not a multiple of 4 — instructions here are only four bytes long", hex32(next as u32)));
            return;
        }
        self.steps += 1;
        self.pc = if self.halted { pc } else { next };
    }

    /// System calls in the style of Linux RISC-V: number in a7, arguments in a0…a2.
    fn syscall(&mut self) -> bool {
        let n = self.regs[17];
        match n {
            93 => {
                // exit(code)
                self.halted = true;
                self.exit_code = Some(self.regs[10]);
                true
            }
            64 => {
                // write(fd, buffer, length): only fd = 1 (console)
                if self.regs[10] != 1 {
                    self.fault(i18n::trf!("write: only fd = 1 (console) is supported, but a0 holds {0}", self.regs[10]));
                    return false;
                }
                let (buf, len) = (self.regs[11] as u32 as usize, self.regs[12] as u32 as usize);
                if buf + len > RAM_SIZE {
                    self.fault(i18n::trf!("write: buffer {0} + {1} goes beyond memory", hex32(buf as u32), len));
                    return false;
                }
                let chunk = self.mem[buf..buf + len].to_vec();
                self.uart.extend_from_slice(&chunk);
                self.regs[10] = len as u32 as i32;
                self.last_reg = Some(10);
                true
            }
            _ => {
                self.fault(i18n::trf!("ecall: the system does not support call number {0} (a7). Available: 93 — exit and 64 — write.", n));
                false
            }
        }
    }

    /// Run until the machine halts, but no more than `max_steps` instructions.
    /// If the limit is exhausted, the machine is considered broken ("the loop does not terminate").
    pub fn run(&mut self, max_steps: u64) {
        let mut left = max_steps;
        while self.running() && left > 0 {
            left -= 1;
            self.step();
        }
        if self.running() {
            self.fault(i18n::trf!("Limit of {0} steps exceeded — the loop probably never ends.", max_steps));
        }
    }

    /// Same as `run`, but with a trace: one entry per executed instruction (no more than `max_trace`).
    pub fn run_traced(&mut self, max_steps: u64, max_trace: usize) -> Vec<TraceStep> {
        let mut trace = Vec::new();
        let mut left = max_steps;
        while self.running() && left > 0 {
            left -= 1;
            let (pc, before) = (self.pc as u32, self.steps);
            self.step();
            if self.steps != before && trace.len() < max_trace {
                trace.push(TraceStep {
                    pc,
                    insn: self.last_insn.clone(),
                    last_read: self.last_read,
                    last_write: self.last_write,
                    last_reg: self.last_reg,
                    regs: self.regs.iter().map(|r| *r as u32).collect(),
                    steps: self.steps,
                });
            }
        }
        if self.running() {
            self.fault(i18n::trf!("Limit of {0} steps exceeded — the loop probably never ends.", max_steps));
        }
        trace
    }

    /// Everything the program printed, as text (invalid UTF-8 is replaced with U+FFFD, a leading byte order mark
    /// is dropped — as with `TextDecoder`).
    pub fn uart_text(&self) -> String {
        let s = String::from_utf8_lossy(&self.uart);
        s.strip_prefix('\u{feff}').map_or_else(|| s.to_string(), str::to_string)
    }

    /// State snapshot.
    pub fn view(&self) -> View {
        View {
            regs: self.regs.iter().map(|r| *r as u32).collect(),
            pc: self.pc as u32,
            mem: self.mem.clone(),
            steps: self.steps,
            halted: self.halted,
            exit_code: self.exit_code,
            error: self.error.clone(),
            uart: self.uart_text(),
            leds: self.leds,
            led_log: self.led_log.clone(),
            last_read: self.last_read,
            last_write: self.last_write,
            last_reg: self.last_reg,
            last_insn: self.last_insn.clone(),
        }
    }
}
