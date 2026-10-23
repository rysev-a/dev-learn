//! Чистая логика интерфейса лаборатории RISC-V: подготовка данных для отрисовки (регистры, листинг, окно памяти,
//! светодиоды), сборка машины под тест задачи и итог запуска. Всё без DOM и сигналов — проверяется `cargo test`.

use riscvlab::{
    asm::{AsmLine, AsmResult},
    isa::{fields_of, ABI_NAMES},
    machine::{Machine, DEFAULT_MAX_STEPS},
    task::TaskSpec,
    verify, Options, STACK_TOP,
};

/// Сколько байт видно в окне памяти (16 строк по 16 байт).
pub const WINDOW_BYTES: u32 = 0x100;

/// Окно памяти: что показывает и с какого адреса.
#[derive(Clone, Copy, Debug)]
pub struct MemWindow {
    pub title: &'static str,
    pub from: u32,
}

/// Окна памяти: команды, данные, вершина стека.
pub const WINDOWS: [MemWindow; 3] = [
    MemWindow { title: "Команды (0x0000)", from: 0x0000 },
    MemWindow { title: "Данные (0x1000)", from: 0x1000 },
    MemWindow { title: "Стек (вершина)", from: STACK_TOP - WINDOW_BYTES },
];

/// Окно, в которое попадает адрес: после команды окно перескакивает туда, где она читала или писала.
pub fn window_for(addr: u32) -> Option<usize> {
    WINDOWS.iter().position(|w| addr >= w.from && addr < w.from + WINDOW_BYTES)
}

/// Адрес в четыре шестнадцатеричные цифры, прописными (для счётчика команд и памяти).
pub fn hex_addr(n: u32) -> String {
    format!("{n:04X}")
}

/// Снимок машины без памяти: то, что рисуют регистры, строка состояния, периферия и консоль.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Status {
    pub regs: Vec<u32>,
    pub pc: u32,
    pub steps: u64,
    pub halted: bool,
    pub error: Option<String>,
    pub exit_code: Option<i32>,
    pub uart: String,
    pub leds: u8,
    pub last_insn: String,
    pub last_reg: Option<u8>,
}

impl Status {
    pub fn of(m: &Machine) -> Status {
        Status {
            regs: m.regs.iter().map(|r| *r as u32).collect(),
            pc: m.pc as u32,
            steps: m.steps,
            halted: m.halted,
            error: m.error.clone(),
            exit_code: m.exit_code,
            uart: m.uart_text(),
            leds: m.leds,
            last_insn: m.last_insn.clone(),
            last_reg: m.last_reg,
        }
    }

    /// Можно ли выполнить ещё одну команду.
    pub fn can_step(&self) -> bool {
        !self.halted && self.error.is_none()
    }
}

/// Регистр в сетке: ABI-имя, значение со знаком и в шестнадцатеричном виде.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct RegRow {
    pub num: usize,
    pub name: &'static str,
    pub signed: i32,
    pub hex: String,
    pub changed: bool,
}

/// Строки сетки регистров x0…x31 (`last_reg` подсвечивается как изменённый последней командой).
pub fn reg_rows(regs: &[u32], last_reg: Option<u8>) -> Vec<RegRow> {
    ABI_NAMES
        .iter()
        .enumerate()
        .map(|(num, name)| {
            let value = regs.get(num).copied().unwrap_or(0);
            RegRow { num, name, signed: value as i32, hex: format!("{value:08x}"), changed: last_reg.is_some_and(|r| usize::from(r) == num) }
        })
        .collect()
}

/// Поле команды в листинге: цвет, биты и название (для подсказки и легенды).
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct FieldView {
    pub cls: &'static str,
    pub bits: String,
    pub name: String,
}

/// Строка листинга «Машинный код».
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ListingRow {
    pub addr: u32,
    pub addr_hex: String,
    pub word_hex: String,
    pub text: String,
    pub pseudo: bool,
    /// буква формата (R, I, S, B, U, J, SYS или «?»)
    pub fmt: &'static str,
    pub fields: Vec<FieldView>,
}

/// Листинг: слово машинного кода, разбор по полям и исходный текст каждой команды.
pub fn listing_rows(lines: &[AsmLine]) -> Vec<ListingRow> {
    lines
        .iter()
        .map(|l| {
            let parts = fields_of(l.word);
            ListingRow {
                addr: l.addr,
                addr_hex: format!("{:04x}", l.addr),
                word_hex: format!("{:08x}", l.word),
                text: l.text.clone(),
                pseudo: l.pseudo,
                fmt: parts.fmt.letter(),
                fields: parts
                    .fields
                    .into_iter()
                    .map(|f| FieldView { cls: f.cls.css(), bits: f.bits, name: f.name })
                    .collect(),
            }
        })
        .collect()
}

/// Байт в сетке памяти.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct MemCell {
    pub addr: u32,
    pub hex: String,
    pub ch: char,
    pub read: bool,
    pub written: bool,
}

impl MemCell {
    /// Класс ячейки: `read` — прочитан последней командой, `written` — записан.
    pub fn class(&self) -> &'static str {
        match (self.read, self.written) {
            (false, false) => "lab-cell",
            (true, false) => "lab-cell read",
            (false, true) => "lab-cell written",
            (true, true) => "lab-cell read written",
        }
    }
}

/// Строка сетки памяти: адрес первого байта и 16 ячеек.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct MemRow {
    pub addr: u32,
    pub cells: Vec<MemCell>,
}

/// Окно памяти: `rows` строк по 16 байт начиная с `base`; за пределами памяти — нули.
pub fn mem_rows(mem: &[u8], base: u32, rows: usize, last_read: Option<u32>, last_write: Option<u32>) -> Vec<MemRow> {
    (0..rows as u32)
        .map(|row| {
            let addr = base + row * 16;
            let cells = (0..16)
                .map(|col| {
                    let a = addr + col;
                    let byte = mem.get(a as usize).copied().unwrap_or(0);
                    let ch = if (32..127).contains(&byte) { char::from(byte) } else { '·' };
                    MemCell { addr: a, hex: format!("{byte:02X}"), ch, read: last_read == Some(a), written: last_write == Some(a) }
                })
                .collect();
            MemRow { addr, cells }
        })
        .collect()
}

/// Светодиоды слева направо: LED7 … LED0 и горит ли каждый (так же рисуются и переключатели).
pub fn led_cells(value: u8) -> [(u8, bool); 8] {
    std::array::from_fn(|k| {
        let i = 7 - k as u8;
        (i, (value >> i) & 1 == 1)
    })
}

/// Код возврата так, как его видит оболочка: младший байт.
pub fn exit_code_text(code: i32) -> String {
    format!("код возврата: {}", code & 0xff)
}

/// Итог запуска: плашка «Задание выполнено!» или «Пока не то» с пояснением.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct RunResult {
    pub ok: bool,
    pub message: String,
}

impl RunResult {
    fn ok(message: String) -> Self {
        Self { ok: true, message }
    }
    fn bad(message: String) -> Self {
        Self { ok: false, message }
    }
}

/// Лимит шагов на запуск: из задачи, а если там ноль — общий.
pub fn run_limit(spec: &TaskSpec) -> u64 {
    if spec.max_steps == 0 {
        DEFAULT_MAX_STEPS
    } else {
        spec.max_steps
    }
}

/// Машина для запуска из интерфейса: образ программы, переключатели и регистры первого теста задачи.
/// Пока в программе есть ошибки ассемблера, запускать нечего.
pub fn build_machine(spec: &TaskSpec, asm: &AsmResult) -> Option<Machine> {
    if !asm.errors.is_empty() {
        return None;
    }
    let test = spec.tests.first();
    let mut m = Machine::new(&asm.image, Options { switches: test.map_or(0, |t| t.switches), entry: asm.entry });
    for r in test.iter().flat_map(|t| t.regs.iter()) {
        m.set_reg(r.reg, r.value);
    }
    Some(m)
}

/// Положение переключателей для показа: как в первом тесте задачи.
pub fn switches_of(spec: &TaskSpec) -> u8 {
    spec.tests.first().map_or(0, |t| t.switches)
}

/// Итог запуска, когда машина остановилась (иначе `None`). Сначала проверяется тест, по которому шёл запуск, и только
/// потом вся задача (`verify` — то же, что сделает сервер): так ученик не получит «выполнено», а затем отказ.
pub fn evaluate(spec: &TaskSpec, asm: &AsmResult, m: &Machine, program: &str) -> Option<RunResult> {
    if let Some(e) = &m.error {
        return Some(RunResult::bad(e.clone()));
    }
    if !m.halted {
        return None;
    }
    let Some(test) = spec.tests.first() else {
        return Some(RunResult::bad("У задачи нет тестов".to_string()));
    };
    let checked = test.check.evaluate(&m.view(), &asm.symbols);
    if !checked.ok {
        return Some(RunResult::bad(checked.message));
    }
    let verdict = verify(spec, program);
    Some(if verdict.ok { RunResult::ok(checked.message) } else { RunResult::bad(verdict.message) })
}

#[cfg(test)]
mod tests {
    use super::*;
    use riscvlab::{assemble, task::LabChapter};
    use serde_json::Value;

    #[test]
    fn address_is_four_uppercase_hex_digits() {
        assert_eq!(hex_addr(0x1a0), "01A0");
        assert_eq!(hex_addr(0x4000), "4000");
    }

    #[test]
    fn memory_windows_cover_text_data_and_stack() {
        assert_eq!(window_for(0), Some(0));
        assert_eq!(window_for(0xff), Some(0));
        assert_eq!(window_for(0x100), None);
        assert_eq!(window_for(0x1000), Some(1));
        assert_eq!(window_for(STACK_TOP - 1), Some(2));
        assert_eq!(window_for(0x1000_0000), None, "устройства вне окон");
    }

    #[test]
    fn registers_show_signed_and_hex_values() {
        let mut regs = vec![0u32; 32];
        regs[10] = 0xffff_fffe;
        let rows = reg_rows(&regs, Some(10));
        assert_eq!(rows.len(), 32);
        assert_eq!((rows[10].name, rows[10].signed, rows[10].hex.as_str(), rows[10].changed), ("a0", -2, "fffffffe", true));
        assert!(!rows[11].changed);
        assert_eq!(reg_rows(&[], None)[2].hex, "00000000", "недостающие регистры — нули");
    }

    #[test]
    fn listing_splits_every_word_into_fields() {
        let asm = assemble("  addi a0, zero, 5\n  ebreak\n");
        let rows = listing_rows(&asm.lines);
        assert_eq!(rows.len(), 2);
        assert_eq!((rows[0].addr_hex.as_str(), rows[0].word_hex.as_str(), rows[0].fmt), ("0000", "00500513", "I"));
        assert_eq!(rows[0].fields.iter().map(|f| f.bits.len()).sum::<usize>(), 32);
        assert_eq!(rows[0].fields[0].cls, "imm");
        assert_eq!(rows[1].fmt, "SYS");
    }

    #[test]
    fn memory_grid_marks_access_and_prints_ascii() {
        let mut mem = vec![0u8; 0x200];
        mem[0x10] = b'A';
        mem[0x11] = 7;
        let rows = mem_rows(&mem, 0, 2, Some(0x10), Some(0x11));
        assert_eq!(rows.len(), 2);
        assert_eq!(rows[1].addr, 16);
        let (a, b) = (&rows[1].cells[0], &rows[1].cells[1]);
        assert_eq!((a.hex.as_str(), a.ch, a.class()), ("41", 'A', "lab-cell read"));
        assert_eq!((b.hex.as_str(), b.ch, b.class()), ("07", '·', "lab-cell written"));
        let tail = mem_rows(&mem[..8], 0, 1, None, None);
        assert_eq!(tail[0].cells[15].hex, "00", "за концом памяти — нули");
    }

    #[test]
    fn leds_go_from_seven_down_to_zero() {
        let cells = led_cells(0b1010_0101);
        assert_eq!(cells[0], (7, true));
        assert_eq!(cells[1], (6, false));
        assert_eq!(cells[7], (0, true));
    }

    #[test]
    fn exit_code_is_one_byte() {
        assert_eq!(exit_code_text(3), "код возврата: 3");
        assert_eq!(exit_code_text(-1), "код возврата: 255");
        assert_eq!(exit_code_text(256), "код возврата: 0");
    }

    /// Задачи глав 16 и 17 в том виде, как их отдаёт сервер (без эталона), и эталонные программы к ним.
    fn chapters() -> Vec<(String, TaskSpec, String)> {
        let dir = concat!(env!("CARGO_MANIFEST_DIR"), "/../../backend/app/data/labs/arch");
        let mut out = Vec::new();
        for file in ["14-16.json", "14-17.json"] {
            let text = std::fs::read_to_string(format!("{dir}/{file}")).expect("файл данных главы");
            let chapter = LabChapter::from_json(&text).expect("данные главы");
            let raw: Value = serde_json::from_str(&text).expect("json");
            for (task, raw_task) in chapter.tasks.iter().zip(raw["tasks"].as_array().expect("tasks")) {
                let mut spec = raw_task["spec"].clone();
                spec.as_object_mut().expect("spec").remove("reference");
                let public: TaskSpec = serde_json::from_value(spec).expect("спецификация без эталона разбирается");
                assert!(public.reference.is_empty());
                out.push((task.id.clone(), public, task.spec.reference.clone()));
            }
        }
        out
    }

    #[test]
    fn reference_programs_pass_and_starters_do_not() {
        let tasks = chapters();
        assert_eq!(tasks.len(), 15);
        for (id, spec, reference) in tasks {
            let run = |program: &str| {
                let asm = assemble(&spec.full_source(program));
                let mut m = build_machine(&spec, &asm).unwrap_or_else(|| panic!("{id}: ошибки ассемблера: {:?}", asm.errors));
                m.run(run_limit(&spec));
                evaluate(&spec, &asm, &m, program)
            };
            let good = run(&reference).unwrap_or_else(|| panic!("{id}: эталон не остановился"));
            assert!(good.ok, "{id}: {}", good.message);
            if let Some(r) = run(&spec.starter) {
                assert!(!r.ok, "{id}: заготовка не должна проходить");
            }
        }
    }

    #[test]
    fn stepping_does_not_report_until_the_machine_halts() {
        let spec: TaskSpec = serde_json::from_value(serde_json::json!({
            "profile": "board", "starter": "", "data": "",
            "tests": [{ "check": { "kind": "reg", "reg": 10, "expected": 5, "ok": "готово" } }],
        }))
        .expect("спецификация");
        let program = "  li a0, 5\n  ebreak\n";
        let asm = assemble(&spec.full_source(program));
        let mut m = build_machine(&spec, &asm).expect("собралось");
        m.step();
        assert_eq!(evaluate(&spec, &asm, &m, program), None);
        m.step();
        assert_eq!(evaluate(&spec, &asm, &m, program), Some(RunResult { ok: true, message: "готово".into() }));
    }

    #[test]
    fn machine_is_not_built_from_a_broken_program() {
        let spec: TaskSpec = serde_json::from_value(serde_json::json!({
            "profile": "board", "starter": "", "data": "", "tests": [],
        }))
        .expect("спецификация");
        assert!(build_machine(&spec, &assemble("  blah a0\n")).is_none());
        assert_eq!(run_limit(&spec), riscvlab::task::DEFAULT_TASK_STEPS);
    }

    #[test]
    fn machine_takes_switches_and_registers_from_the_first_test() {
        let spec: TaskSpec = serde_json::from_value(serde_json::json!({
            "profile": "board", "starter": "", "data": "",
            "tests": [{ "switches": 178, "regs": [{ "reg": 10, "value": 7 }],
                        "check": { "kind": "leds", "expected": 0, "ok": "ок" } }],
        }))
        .expect("спецификация");
        let m = build_machine(&spec, &assemble("  ebreak\n")).expect("собралось");
        assert_eq!((m.switches, m.regs[10]), (178, 7));
        assert_eq!(switches_of(&spec), 178);
    }
}
