//! RISC-V lab exercises as data, and solution checking.
//!
//! * [`LabChapter`] — chapter data file (`backend/data/labs/arch/<book>-<chapter>.json`);
//! * [`TaskSpec`] — everything needed for the check: starter, reference solution, task data, tests;
//! * [`verify`] — assembles the submitted program text, runs all the task's tests and issues a verdict.
//!   This is what the server does on `PUT /api/exercises/14/<chapter>/<id>/solved`.

use serde::{Deserialize, Serialize};

use crate::asm::{assemble, AsmError, AsmResult, RAM_SIZE};
use crate::isa::reg_name;
use crate::js::json_quote;
use crate::machine::{Machine, Options, View, DEFAULT_MAX_STEPS};

/// Longest program text the server will check (bytes).
pub const MAX_PROGRAM_BYTES: usize = 256 * 1024;

/// Default step limit per test (as in the UI).
pub const DEFAULT_TASK_STEPS: u64 = 200_000;

/// Which lab.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Lab {
    /// RISC-V: chapters 16 and 17 of book 14
    Riscv,
}

/// Environment the program runs in.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Profile {
    /// educational board: `ebreak` halts, UART console, LEDs, switches, timer (chapter 16)
    Board,
    /// real program: `write` and `exit` as in Linux, `_start` entry point (chapter 17)
    Linux,
}

/// Chapter data file.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct LabChapter {
    /// book number
    pub book: u32,
    /// chapter number
    pub chapter: u32,
    /// which lab
    pub lab: Lab,
    /// tasks
    pub tasks: Vec<Task>,
}

/// Exercise.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Task {
    /// task identifier
    pub id: String,
    /// title
    pub title: String,
    /// statement
    pub statement: String,
    /// hint
    pub hint: String,
    /// exercise specification
    pub spec: TaskSpec,
}

/// Exercise specification.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct TaskSpec {
    /// environment the programs run in
    pub profile: Profile,
    /// program starter
    pub starter: String,
    /// reference solution (not sent to the client, see [`TaskSpec::without_reference`]; the field is absent in the server response)
    #[serde(default)]
    pub reference: String,
    /// task data: assembler text of the `.data` section; appended to the program and not editable
    pub data: String,
    /// what counts as a "hang": how many instructions to execute per test
    #[serde(default = "default_steps")]
    pub max_steps: u64,
    /// tests
    pub tests: Vec<Test>,
}

fn default_steps() -> u64 {
    DEFAULT_TASK_STEPS
}

/// One test: inputs and expectation.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Test {
    /// switch positions (8 bits)
    #[serde(default)]
    pub switches: u8,
    /// registers set before the run (except sp, which the loader sets if not specified)
    #[serde(default, skip_serializing_if = "Vec::is_empty")]
    pub regs: Vec<RegInit>,
    /// what the result should be
    pub check: Check,
}

/// Initial register value.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct RegInit {
    /// register number x0…x31
    pub reg: u8,
    /// value
    pub value: i32,
}

/// Check of the final machine state after halting. Texts are as in the previous TypeScript version.
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case", deny_unknown_fields)]
pub enum Check {
    /// exactly this text in the console
    Uart {
        /// expected output
        expected: String,
        /// message on success
        ok: String,
    },
    /// LEDs lit in the pattern
    Leds {
        /// expected eight bits
        expected: u8,
        /// message on success
        ok: String,
        /// appended to the error message
        #[serde(default, skip_serializing_if = "String::is_empty")]
        bad_suffix: String,
    },
    /// a number in the register
    Reg {
        /// register number x0…x31
        reg: u8,
        /// expected value (signed)
        expected: i32,
        /// message on success
        ok: String,
    },
    /// a string lies at the label (read up to the zero byte)
    MemCstr {
        /// label name
        symbol: String,
        /// expected string
        expected: String,
        /// message on success
        ok: String,
    },
    /// an array of 32-bit words lies at the label
    MemWords {
        /// label name
        symbol: String,
        /// expected words, signed
        expected: Vec<i32>,
        /// message on success
        ok: String,
    },
    /// sp has returned to the top of memory
    StackReturned,
    /// all checks in order; the message is that of the first failed one, otherwise `ok`
    All {
        /// nested checks
        checks: Vec<Check>,
        /// message on success
        ok: String,
    },
    /// the LED toggled `toggles` times in the pattern 1, 0, 1, 0…, each state held for at least `min_gap` cycles
    Blink {
        /// how many toggles are needed
        toggles: u32,
        /// minimum hold time between toggles, in cycles
        min_gap: u64,
        /// message on success
        ok: String,
    },
    /// the program finished with an exit call: output and return code
    Run {
        /// expected output
        stdout: String,
        /// expected return code
        code: i32,
        /// message on success
        ok: String,
    },
}

/// Outcome of checking one condition.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CheckResult {
    /// everything passed
    pub ok: bool,
    /// message text
    pub message: String,
}

fn ok(message: &str) -> CheckResult {
    CheckResult { ok: true, message: message.to_string() }
}
fn bad(message: String) -> CheckResult {
    CheckResult { ok: false, message }
}

/// `0b` and eight binary digits.
fn bin8(n: u32) -> String {
    format!("0b{:08b}", n & 0xff)
}

fn word_at(mem: &[u8], a: usize) -> i32 {
    let b = |k: usize| i32::from(mem.get(a + k).copied().unwrap_or(0));
    b(0) | (b(1) << 8) | (b(2) << 16) | (b(3) << 24)
}

/// String up to the zero byte; bytes as Latin-1 character codes (that is how the previous check read it).
fn cstr_at(mem: &[u8], a: Option<u32>) -> String {
    let Some(a) = a else { return String::new() };
    let mut s = String::new();
    let mut i = a as usize;
    while i < mem.len() && mem[i] != 0 {
        s.push(char::from(mem[i]));
        i += 1;
    }
    s
}

impl Check {
    /// Check the machine state after halting. `symbols` — addresses of the program's labels.
    pub fn evaluate(&self, v: &View, symbols: &std::collections::BTreeMap<String, u32>) -> CheckResult {
        match self {
            Check::Uart { expected, ok: okm } => {
                if &v.uart == expected {
                    ok(okm)
                } else {
                    bad(i18n::trf!("The console shows {0}, but {1} was expected", json_quote(&v.uart), json_quote(expected)))
                }
            }
            Check::Leds { expected, ok: okm, bad_suffix } => {
                if v.leds == *expected {
                    ok(okm)
                } else {
                    bad(i18n::trf!("The LEDs show {0}, but {1} was expected{2}", bin8(u32::from(v.leds)), bin8(u32::from(*expected)), bad_suffix))
                }
            }
            Check::Reg { reg, expected, ok: okm } => {
                let got = v.regs.get(usize::from(*reg)).copied().unwrap_or(0);
                if got == *expected as u32 {
                    ok(okm)
                } else {
                    bad(i18n::trf!("{0} holds {1}, but {2} was expected", reg_name(*reg), got as i32, expected))
                }
            }
            Check::MemCstr { symbol, expected, ok: okm } => {
                let got = cstr_at(&v.mem, symbols.get(symbol).copied());
                if &got == expected {
                    ok(okm)
                } else {
                    bad(i18n::trf!("Memory holds “{0}”, but “{1}” was expected", got, expected))
                }
            }
            Check::MemWords { symbol, expected, ok: okm } => {
                let base = symbols.get(symbol).copied().unwrap_or(0) as usize;
                let got: Vec<i32> = (0..expected.len()).map(|i| word_at(&v.mem, base + 4 * i)).collect();
                if &got == expected {
                    ok(okm)
                } else {
                    let join = |w: &[i32]| w.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(", ");
                    bad(i18n::trf!("Memory holds {0}, but {1} was expected", join(&got), join(expected)))
                }
            }
            Check::StackReturned => {
                let sp = v.regs.get(2).copied().unwrap_or(0);
                if sp == RAM_SIZE as u32 {
                    ok("")
                } else {
                    bad(i18n::trf!("The stack did not return to its place: sp = 0x{0}, but it must be 0x{1}", format!("{:x}", sp), format!("{:x}", RAM_SIZE)))
                }
            }
            Check::All { checks, ok: okm } => {
                for c in checks {
                    let r = c.evaluate(v, symbols);
                    if !r.ok {
                        return r;
                    }
                }
                ok(okm)
            }
            Check::Blink { toggles, min_gap, ok: okm } => {
                // keep only real toggles: writing the same value is not an event
                let mut changes: Vec<(u64, u8)> = Vec::new();
                let mut prev = 0u8;
                for e in &v.led_log {
                    if e.value != prev {
                        changes.push((e.cycle, e.value));
                    }
                    prev = e.value;
                }
                if (changes.len() as u64) < u64::from(*toggles) {
                    return bad(i18n::trf!("The LED toggled {0} time(s), but {1} are needed", changes.len(), toggles));
                }
                for (i, (cycle, value)) in changes.iter().enumerate() {
                    let want = u8::from(i % 2 == 0);
                    if *value != want {
                        return bad(i18n::trf!("Toggle {0}: LED = {1}, but it must alternate 1, 0, 1, 0…", i + 1, value));
                    }
                    if i > 0 {
                        let gap = cycle - changes[i - 1].0;
                        if gap < *min_gap {
                            return bad(i18n::trf!("Between toggles {0} and {1} only {2} cycles passed, but at least {3} are needed", i, i + 1, gap, min_gap));
                        }
                    }
                }
                ok(okm)
            }
            Check::Run { stdout, code, ok: okm } => {
                let Some(exit) = v.exit_code else {
                    return bad(
                        i18n::tr("The program did not finish with an exit call: you need li a7, 93 and ecall (the exit code goes in a0).")
                            .to_string(),
                    );
                };
                if &v.uart != stdout {
                    return bad(i18n::trf!("The output is {0}, but {1} was expected", json_quote(&v.uart), json_quote(stdout)));
                }
                if exit != *code {
                    return bad(i18n::trf!("Exit code {0}, but {1} was expected", exit, code));
                }
                ok(okm)
            }
        }
    }
}

impl TaskSpec {
    /// Copy without the reference solution — what the backend sends to the client.
    pub fn without_reference(&self) -> TaskSpec {
        TaskSpec { reference: String::new(), ..self.clone() }
    }

    /// Full program text: what the student wrote plus the task data.
    pub fn full_source(&self, user: &str) -> String {
        full_source(user, &self.data)
    }
}

/// Full program text: what the student wrote plus the task data.
pub fn full_source(user: &str, data: &str) -> String {
    format!("{user}\n.data\n{data}\n")
}

/// How the check ended.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum Outcome {
    /// all tests passed
    Passed,
    /// the program halted, but the result is wrong
    Wrong,
    /// the machine broke: invalid instruction, out-of-memory access, step limit
    Fault,
    /// the program did not assemble (or is too long)
    AsmErrors,
}

/// Outcome of one test.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TestVerdict {
    /// everything passed
    pub ok: bool,
    /// message text
    pub message: String,
    /// how many instructions were executed
    pub steps: u64,
}

/// Verdict on the solution.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Verdict {
    /// everything passed
    pub ok: bool,
    /// how the check ended
    pub outcome: Outcome,
    /// message to the student: the first failed test, otherwise the last one
    pub message: String,
    /// assembler errors (line numbers refer to the full text: program plus task data)
    pub errors: Vec<AsmError>,
    /// tests
    pub tests: Vec<TestVerdict>,
}

fn failed(outcome: Outcome, message: String, errors: Vec<AsmError>) -> Verdict {
    Verdict { ok: false, outcome, message, errors, tests: Vec::new() }
}

/// Run the assembled program under the test's conditions and check the result.
pub fn run_test(spec: &TaskSpec, asm: &AsmResult, test: &Test) -> (CheckResult, Outcome, u64) {
    let mut m = Machine::new(&asm.image, Options { switches: test.switches, entry: asm.entry });
    for r in &test.regs {
        m.set_reg(r.reg, r.value);
    }
    m.run(if spec.max_steps == 0 { DEFAULT_MAX_STEPS } else { spec.max_steps });
    let steps = m.steps;
    if let Some(e) = &m.error {
        return (CheckResult { ok: false, message: e.clone() }, Outcome::Fault, steps);
    }
    let r = test.check.evaluate(&m.view(), &asm.symbols);
    let outcome = if r.ok { Outcome::Passed } else { Outcome::Wrong };
    (r, outcome, steps)
}

/// Solution check: assemble the submitted program text and run all the task's tests.
pub fn verify(spec: &TaskSpec, program: &str) -> Verdict {
    if program.len() > MAX_PROGRAM_BYTES {
        let msg =
            i18n::trf!("The program is too long: {0} bytes, but at most {1} are checked", program.len(), MAX_PROGRAM_BYTES);
        return failed(Outcome::AsmErrors, msg.clone(), vec![AsmError { line: 1, message: msg }]);
    }
    let asm = assemble(&spec.full_source(program));
    if let Some(first) = asm.errors.first() {
        let msg = i18n::trf!("Line {0}: {1}", first.line, first.message);
        return failed(Outcome::AsmErrors, msg, asm.errors.clone());
    }
    if spec.tests.is_empty() {
        return failed(Outcome::Wrong, i18n::tr("The task has no tests").to_string(), Vec::new());
    }
    let mut tests = Vec::new();
    // the outcome is by the first failed test, or by the last one if all passed
    let mut summary: Option<(Outcome, String)> = None;
    for t in &spec.tests {
        let (r, o, steps) = run_test(spec, &asm, t);
        if summary.as_ref().is_none_or(|(prev, _)| *prev == Outcome::Passed) {
            summary = Some((o, r.message.clone()));
        }
        tests.push(TestVerdict { ok: r.ok, message: r.message, steps });
    }
    let (outcome, message) = summary.unwrap_or((Outcome::Wrong, String::new()));
    Verdict { ok: outcome == Outcome::Passed, outcome, message, errors: Vec::new(), tests }
}

impl LabChapter {
    /// Parse a chapter data file.
    pub fn from_json(text: &str) -> Result<LabChapter, serde_json::Error> {
        serde_json::from_str(text)
    }

    /// Canonical JSON of the file (indented, with a trailing newline).
    pub fn to_canonical_json(&self) -> Result<String, serde_json::Error> {
        let mut s = serde_json::to_string_pretty(self)?;
        s.push('\n');
        Ok(s)
    }

    /// Task by id.
    pub fn task(&self, id: &str) -> Option<&Task> {
        self.tasks.iter().find(|t| t.id == id)
    }

    /// Copy of the chapter without reference solutions — for the client.
    pub fn without_references(&self) -> LabChapter {
        LabChapter {
            tasks: self.tasks.iter().map(|t| Task { spec: t.spec.without_reference(), ..t.clone() }).collect(),
            ..self.clone()
        }
    }
}

/// Chapter data file name: `<book>-<chapter:02>.json`.
pub fn chapter_file_name(book: u32, chapter: u32) -> String {
    format!("{book}-{chapter:02}.json")
}
