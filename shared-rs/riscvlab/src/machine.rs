//! Процессор RV32IM: регистры, память, периферия. Один «шаг» — одна команда.
//!
//! Карта адресов «мягкого» процессора — как в учебной плате на ПЛИС:
//! * `0x0000_0000 … 0x0000_3FFF` — оперативная память 16 КиБ (команды, данные, стек);
//! * `0x1000_0000` UART: запись байта — вывод символа; чтение `+4` — «передатчик готов» (1);
//! * `0x1000_1000` светодиоды: запись — зажечь (младшие 8 бит); чтение — что записано;
//! * `0x1000_1004` переключатели: чтение — их состояние (8 бит);
//! * `0x1000_2000` таймер: чтение — число выполненных команд (младшие 32 бита).

use serde::{Deserialize, Serialize};

use crate::asm::{RAM_SIZE, STACK_TOP};
use crate::isa::{decode, disassemble, Op};
use crate::js::hex32;

/// UART: запись байта.
pub const UART_TX: u32 = 0x1000_0000;
/// UART: состояние (всегда «готов»).
pub const UART_STATUS: u32 = 0x1000_0004;
/// Светодиоды.
pub const LEDS: u32 = 0x1000_1000;
/// Переключатели.
pub const SWITCHES: u32 = 0x1000_1004;
/// Таймер: число выполненных команд.
pub const TIMER: u32 = 0x1000_2000;

/// Строка справочника по адресам устройств.
#[derive(Clone, Copy, Debug)]
pub struct MmioRegion {
    /// название устройства
    pub name: &'static str,
    /// адрес устройства
    pub addr: u32,
    /// пояснение для справочника
    pub note: &'static str,
}

/// Устройства, видные программе как обычные адреса.
pub const MMIO_MAP: &[MmioRegion] = &[
    MmioRegion {
        name: "UART — вывод", addr: UART_TX, note: "sb: записанный байт появляется в консоли"
    },
    MmioRegion {
        name: "UART — состояние", addr: UART_STATUS, note: "lw: 1, когда можно слать следующий байт"
    },
    MmioRegion {
        name: "Светодиоды", addr: LEDS, note: "sw: младшие 8 бит зажигают LED0…LED7"
    },
    MmioRegion {
        name: "Переключатели", addr: SWITCHES, note: "lw: 8 переключателей SW0…SW7"
    },
    MmioRegion { name: "Таймер", addr: TIMER, note: "lw: сколько команд уже выполнено" },
];

/// Лимит шагов по умолчанию для `run` (как в интерфейсе).
pub const DEFAULT_MAX_STEPS: u64 = 1_000_000;

/// Запись в журнале светодиодов: на каком такте и что записали.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct LedEvent {
    /// на каком такте (сколько команд уже выполнено)
    pub cycle: u64,
    /// записанное значение (8 бит)
    pub value: u8,
}

/// Снимок состояния машины для проверок и интерфейса.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct View {
    /// регистры без знака
    pub regs: Vec<u32>,
    /// счётчик команд (если он ушёл в отрицательные — как дополнение до 2³²)
    pub pc: u32,
    /// память (`RAM_SIZE` байт)
    pub mem: Vec<u8>,
    /// сколько команд выполнено
    pub steps: u64,
    /// программа остановилась (ebreak или exit)
    pub halted: bool,
    /// код возврата, если программа вызвала exit
    pub exit_code: Option<i32>,
    /// сообщение об ошибке машины, если она сломалась
    pub error: Option<String>,
    /// всё, что программа вывела (UART или write), как текст UTF-8
    pub uart: String,
    /// светодиоды: последнее записанное значение
    pub leds: u8,
    /// журнал записей в светодиоды
    pub led_log: Vec<LedEvent>,
    /// адрес последнего чтения/записи памяти и какой регистр изменила последняя команда
    pub last_read: Option<u32>,
    /// адрес последней записи
    pub last_write: Option<u32>,
    /// какой регистр изменила последняя команда
    pub last_reg: Option<u8>,
    /// текст последней выполненной команды
    pub last_insn: String,
}

/// Параметры запуска.
#[derive(Clone, Copy, Debug, Default)]
pub struct Options {
    /// положение переключателей
    pub switches: u8,
    /// с какого адреса начинать
    pub entry: u32,
}

/// Одна запись трассы: что выполнено и что изменилось.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TraceStep {
    /// адрес выполненной команды
    pub pc: u32,
    /// её текст
    pub insn: String,
    /// адрес последнего чтения памяти или устройства
    pub last_read: Option<u32>,
    /// адрес последней записи
    pub last_write: Option<u32>,
    /// какой регистр изменила последняя команда
    pub last_reg: Option<u8>,
    /// регистры после команды
    pub regs: Vec<u32>,
    /// число выполненных команд после шага
    pub steps: u64,
}

/// Процессор RV32IM с памятью и периферией.
#[derive(Clone, Debug)]
pub struct Machine {
    /// регистры
    pub regs: [i32; 32],
    /// память (`RAM_SIZE` байт)
    pub mem: Vec<u8>,
    /// счётчик команд
    pub pc: i64,
    /// сколько команд выполнено
    pub steps: u64,
    /// программа остановилась (ebreak или exit)
    pub halted: bool,
    /// код возврата, если программа вызвала exit
    pub exit_code: Option<i32>,
    /// сообщение об ошибке машины, если она сломалась
    pub error: Option<String>,
    /// всё, что программа вывела (байты)
    pub uart: Vec<u8>,
    /// светодиоды: последнее записанное значение
    pub leds: u8,
    /// журнал записей в светодиоды
    pub led_log: Vec<LedEvent>,
    /// положение переключателей (8 бит)
    pub switches: u8,
    /// адрес последнего чтения памяти или устройства
    pub last_read: Option<u32>,
    /// адрес последней записи
    pub last_write: Option<u32>,
    /// какой регистр изменила последняя команда
    pub last_reg: Option<u8>,
    /// текст последней выполненной команды
    pub last_insn: String,
}

impl Machine {
    /// Машина с образом памяти; `sp` — вершина стека, как задаёт загрузчик.
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

    /// Положить значение в регистр до запуска (x0 не меняется).
    pub fn set_reg(&mut self, reg: u8, value: i32) {
        if reg != 0 && usize::from(reg) < 32 {
            self.regs[usize::from(reg)] = value;
        }
    }

    /// Машина ещё может выполнять команды.
    pub fn running(&self) -> bool {
        !self.halted && self.error.is_none()
    }

    fn fault(&mut self, message: String) {
        self.error = Some(message);
    }

    /* ---------- память и периферия ---------- */

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
                    self.fault(format!("Чтение по адресу {}: там нет устройства", hex32(a)));
                    None
                }
            };
        }
        if a as usize + size as usize > RAM_SIZE {
            self.fault(format!(
                "Чтение по адресу {} за пределами памяти (0x0 … {})",
                hex32(a),
                hex32(RAM_SIZE as u32 - 1)
            ));
            return None;
        }
        if !a.is_multiple_of(size) {
            self.fault(format!(
                "Невыровненное чтение по адресу {}: {} должно лежать по адресу, кратному {}",
                hex32(a),
                if size == 4 { "слово" } else { "полуслово" },
                size
            ));
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
                    self.fault(format!("Запись по адресу {}: это устройство нельзя записывать", hex32(a)));
                    false
                }
            };
        }
        if a as usize + size as usize > RAM_SIZE {
            self.fault(format!(
                "Запись по адресу {} за пределами памяти (0x0 … {})",
                hex32(a),
                hex32(RAM_SIZE as u32 - 1)
            ));
            return false;
        }
        if !a.is_multiple_of(size) {
            self.fault(format!(
                "Невыровненная запись по адресу {}: {} должно лежать по адресу, кратному {}",
                hex32(a),
                if size == 4 { "слово" } else { "полуслово" },
                size
            ));
            return false;
        }
        for k in 0..size {
            self.mem[(a + k) as usize] = (value >> (8 * k)) as u8;
        }
        true
    }

    /* ---------- выполнение ---------- */

    /// Выполнить одну команду (ничего не делает, если машина остановлена или сломана).
    pub fn step(&mut self) {
        if !self.running() {
            return;
        }
        let pc = self.pc;
        self.last_read = None;
        self.last_write = None;
        self.last_reg = None;
        if pc % 4 != 0 || pc < 0 || pc + 4 > RAM_SIZE as i64 {
            self.fault(format!(
                "Счётчик команд вышел из памяти (адрес {}). Не забыли ebreak в конце?",
                hex32(pc as u32)
            ));
            return;
        }
        let p = pc as usize;
        let word = u32::from_le_bytes([self.mem[p], self.mem[p + 1], self.mem[p + 2], self.mem[p + 3]]);
        let d = decode(word);
        self.last_insn = disassemble(word);
        let Some(op) = d.op else {
            self.fault(format!(
                "Непонятная команда {} по адресу {}. Возможно, программа дошла до конца без ebreak или «убежала» в данные",
                hex32(word),
                hex32(pc as u32)
            ));
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
            // деление на ноль даёт −1, переполнение (−2³¹ / −1) — −2³¹ (так задаёт спецификация)
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
            self.fault(format!(
                "Переход на адрес {}, не кратный 4 — здесь команды только по четыре байта",
                hex32(next as u32)
            ));
            return;
        }
        self.steps += 1;
        self.pc = if self.halted { pc } else { next };
    }

    /// Системные вызовы в стиле Linux RISC-V: номер — в a7, аргументы — в a0…a2.
    fn syscall(&mut self) -> bool {
        let n = self.regs[17];
        match n {
            93 => {
                // exit(код)
                self.halted = true;
                self.exit_code = Some(self.regs[10]);
                true
            }
            64 => {
                // write(fd, буфер, длина): только fd = 1 (консоль)
                if self.regs[10] != 1 {
                    self.fault(format!(
                        "write: поддерживается только fd = 1 (консоль), а в a0 лежит {}",
                        self.regs[10]
                    ));
                    return false;
                }
                let (buf, len) = (self.regs[11] as u32 as usize, self.regs[12] as u32 as usize);
                if buf + len > RAM_SIZE {
                    self.fault(format!("write: буфер {} + {} выходит за пределы памяти", hex32(buf as u32), len));
                    return false;
                }
                let chunk = self.mem[buf..buf + len].to_vec();
                self.uart.extend_from_slice(&chunk);
                self.regs[10] = len as u32 as i32;
                self.last_reg = Some(10);
                true
            }
            _ => {
                self.fault(format!("ecall: система не умеет вызов номер {n} (a7). Доступны 93 — exit и 64 — write."));
                false
            }
        }
    }

    /// Выполнять, пока машина не остановится, но не больше `max_steps` команд.
    /// Если лимит исчерпан, машина считается сломанной («цикл не заканчивается»).
    pub fn run(&mut self, max_steps: u64) {
        let mut left = max_steps;
        while self.running() && left > 0 {
            left -= 1;
            self.step();
        }
        if self.running() {
            self.fault(format!("Превышен лимит в {max_steps} шагов — похоже, цикл не заканчивается."));
        }
    }

    /// То же, что `run`, но с записью трассы: по записи на каждую выполненную команду (не больше `max_trace`).
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
            self.fault(format!("Превышен лимит в {max_steps} шагов — похоже, цикл не заканчивается."));
        }
        trace
    }

    /// Всё, что вывела программа, как текст (неверный UTF-8 заменяется на U+FFFD, начальная метка порядка байтов
    /// отбрасывается — как у `TextDecoder`).
    pub fn uart_text(&self) -> String {
        let s = String::from_utf8_lossy(&self.uart);
        s.strip_prefix('\u{feff}').map_or_else(|| s.to_string(), str::to_string)
    }

    /// Снимок состояния.
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
