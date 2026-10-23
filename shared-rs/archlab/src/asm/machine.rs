//! Эмулятор процессора «Мини-8»: память команд отдельно, память данных (виртуальный диск) — 256 байт.
//! Порт `machine.ts`.

use super::isa::*;
use serde::{Deserialize, Serialize};

/// Что видит интерфейс после очередного шага.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MachineView {
    pub regs: Vec<u8>,
    pub pc: i32,
    pub mem: Vec<u8>,
    pub halted: bool,
    pub error: Option<String>,
    pub steps: u64,
    /// Адрес памяти, который прочитала/записала последняя команда.
    pub last_read: Option<usize>,
    pub last_write: Option<usize>,
    /// Какой регистр изменила последняя команда.
    pub last_reg: Option<usize>,
}

/// Лимит шагов по умолчанию (защита от бесконечного цикла).
pub const RUN_LIMIT: u64 = 100_000;

/// Эмулятор.
#[derive(Debug, Clone)]
pub struct Machine {
    pub program: Vec<u16>,
    pub regs: [u8; REG_COUNT],
    pub mem: [u8; MEM_SIZE],
    pub pc: i32,
    pub halted: bool,
    pub error: Option<String>,
    pub steps: u64,
    pub last_read: Option<usize>,
    pub last_write: Option<usize>,
    pub last_reg: Option<usize>,
}

impl Machine {
    /// Машина с программой и начальным содержимым диска (недостающее — нули).
    pub fn new(program: &[u16], disk: &[u8]) -> Machine {
        let mut mem = [0u8; MEM_SIZE];
        for (i, b) in disk.iter().take(MEM_SIZE).enumerate() {
            mem[i] = *b;
        }
        Machine {
            program: program.to_vec(),
            regs: [0; REG_COUNT],
            mem,
            pc: 0,
            halted: false,
            error: None,
            steps: 0,
            last_read: None,
            last_write: None,
            last_reg: None,
        }
    }

    /// Можно выполнять дальше.
    pub fn running(&self) -> bool {
        !self.halted && self.error.is_none()
    }

    /// Выполнить одну команду.
    pub fn step(&mut self) {
        if !self.running() {
            return;
        }
        if self.pc < 0 || self.pc as usize >= self.program.len() {
            self.error = Some(format!("Счётчик команд вышел за пределы программы (адрес {}). Не забыли hlt в конце?", self.pc));
            return;
        }
        let word = self.program[self.pc as usize];
        let d = decode(word);
        self.last_read = None;
        self.last_write = None;
        self.last_reg = None;

        let (a, b, c) = (d.a as usize, d.b as usize, d.c as usize);
        let (rb, rc) = (self.regs[b] as i32, self.regs[c & 7] as i32);
        let addr = ((rb + to_signed(d.c as i32, 6)) & 0xff) as usize;
        let mut next = self.pc + 1;

        let Some(def) = d.def else {
            self.error = Some(format!("Неизвестная команда {} по адресу {}", disassemble(word), self.pc));
            return;
        };
        let set_reg = |m: &mut Machine, r: usize, v: i32| {
            if r != 0 {
                m.regs[r] = (v & 0xff) as u8;
                m.last_reg = Some(r);
            }
        };
        match def.mnemonic {
            "hlt" => {
                self.halted = true;
                next = self.pc;
            }
            "li" => set_reg(self, a, (word & 0xff) as i32),
            "add" => set_reg(self, a, rb + rc),
            "sub" => set_reg(self, a, rb - rc),
            "and" => set_reg(self, a, rb & rc),
            "or" => set_reg(self, a, rb | rc),
            "xor" => set_reg(self, a, rb ^ rc),
            "addi" => set_reg(self, a, rb + to_signed(d.c as i32, 6)),
            "lb" => {
                self.last_read = Some(addr);
                let v = self.mem[addr] as i32;
                set_reg(self, a, v);
            }
            "sb" => {
                self.last_write = Some(addr);
                self.mem[addr] = self.regs[a];
            }
            "beq" => {
                if self.regs[a] == self.regs[b] {
                    next = self.pc + to_signed(d.c as i32, 6);
                }
            }
            "bne" => {
                if self.regs[a] != self.regs[b] {
                    next = self.pc + to_signed(d.c as i32, 6);
                }
            }
            "bltu" => {
                if self.regs[a] < self.regs[b] {
                    next = self.pc + to_signed(d.c as i32, 6);
                }
            }
            "bgeu" => {
                if self.regs[a] >= self.regs[b] {
                    next = self.pc + to_signed(d.c as i32, 6);
                }
            }
            "jmp" => next = self.pc + to_signed((word & 0xfff) as i32, 12),
            _ => {
                self.error = Some(format!("Неизвестная команда {} по адресу {}", disassemble(word), self.pc));
                return;
            }
        }
        self.steps += 1;
        self.pc = next;
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
            regs: self.regs.to_vec(),
            pc: self.pc,
            mem: self.mem.to_vec(),
            halted: self.halted,
            error: self.error.clone(),
            steps: self.steps,
            last_read: self.last_read,
            last_write: self.last_write,
            last_reg: self.last_reg,
        }
    }
}
