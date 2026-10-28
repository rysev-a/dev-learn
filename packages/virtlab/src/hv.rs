//! Mini-hypervisor model (chapter 2): the student plays the virtual machine monitor.
//!
//! The guest runs a program without privileges. Ordinary instructions execute directly, while on privileged ones the CPU raises
//! a trap, and the monitor must correctly emulate the action on the guest's virtual state. The POPF instruction in ring 1
//! does not trap (the x86 hole) until binary translation is enabled.
//!
//! One exercise goal per program: complete the program, choosing the correct emulation at each trap (the goal identifier
//! equals [`Program::id`]). The student's action history is kept by [`Session`] (same as the `HvLab.tsx` handlers);
//! for server-side re-checking the history is recorded as [`Run`] and replayed by [`replay`].

use serde::{Deserialize, Serialize};

use crate::error::SpecError;
use crate::goal::Goal;

/// Guest program: instructions as text ("ADD 3", "CLI", "POPF 1"…).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Program {
    /// Program identifier (also the goal identifier).
    pub id: String,
    /// Tab title.
    pub title: String,
    /// Program instructions.
    pub code: Vec<String>,
    /// Goal text.
    pub goal: String,
}

impl Program {
    /// Exercise goal for this program.
    pub fn as_goal(&self) -> Goal {
        Goal::new(self.id.clone(), self.goal.clone())
    }

    /// Validation: the program is non-empty and all instructions parse.
    pub fn validate(&self) -> Result<(), SpecError> {
        for c in &self.code {
            Instr::parse(c).map_err(|e| SpecError::new(i18n::trf!("program {0}: {1}", self.id, e)))?;
        }
        if self.code.is_empty() {
            return Err(SpecError::new(i18n::trf!("program {0}: empty", self.id)));
        }
        Ok(())
    }
}

/// Guest instruction.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Instr {
    /// `ADD n` — ordinary instruction, executes directly.
    Add(i64),
    /// `CLI` — disable interrupts.
    Cli,
    /// `STI` — enable interrupts.
    Sti,
    /// `WRCR3 n` — write to CR3.
    Wrcr3(i64),
    /// `RDCR3` — read CR3 into the accumulator.
    Rdcr3,
    /// `HLT` — halt the processor.
    Hlt,
    /// `IRQ n` — external interrupt for the guest.
    Irq(i64),
    /// `POPF n` — load flags.
    Popf(i64),
    /// Any other instruction: executes directly and changes nothing (like `default` in TypeScript).
    Other,
}

impl Instr {
    /// Parse an instruction of the form "NAME" or "NAME number".
    pub fn parse(text: &str) -> Result<Instr, SpecError> {
        let mut it = text.split(' ');
        let op = it.next().unwrap_or("");
        let arg = it.next();
        let num = |name: &str| -> Result<i64, SpecError> {
            arg.and_then(|a| a.parse::<i64>().ok())
                .ok_or_else(|| SpecError::new(i18n::trf!("command “{0}”: {1} requires an integer", text, name)))
        };
        Ok(match op {
            "ADD" => Instr::Add(num("ADD")?),
            "CLI" => Instr::Cli,
            "STI" => Instr::Sti,
            "WRCR3" => Instr::Wrcr3(num("WRCR3")?),
            "RDCR3" => Instr::Rdcr3,
            "HLT" => Instr::Hlt,
            "IRQ" => Instr::Irq(num("IRQ")?),
            "POPF" => Instr::Popf(num("POPF")?),
            _ => Instr::Other,
        })
    }
}

/// Virtual guest state and run counters.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct GuestState {
    /// Index of the current instruction.
    pub pc: usize,
    /// Accumulator.
    pub acc: i64,
    /// Virtual interrupt flag IF.
    pub vif: i64,
    /// Virtual CR3.
    pub vcr3: i64,
    /// Queue of interrupts waiting to be enabled.
    pub queue: Vec<i64>,
    /// Interrupts delivered to the guest.
    pub delivered: Vec<i64>,
    /// Step log (for display).
    pub log: Vec<String>,
    /// Number of wrong monitor choices.
    pub mistakes: u32,
    /// There was an instruction the monitor missed (POPF without translation).
    pub silent: bool,
    /// Guest halted (HLT).
    pub halted: bool,
}

impl Default for GuestState {
    fn default() -> Self {
        initial()
    }
}

/// Initial guest state.
pub fn initial() -> GuestState {
    GuestState {
        pc: 0,
        acc: 0,
        vif: 1,
        vcr3: 0,
        queue: vec![],
        delivered: vec![],
        log: vec![],
        mistakes: 0,
        silent: false,
        halted: false,
    }
}

/// Emulation option at a trap.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct TrapOption {
    /// Option text.
    pub label: String,
    /// Whether the option is correct.
    pub ok: bool,
    /// Explanation (for a wrong one — why it is not allowed).
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub why: Option<String>,
}

/// What happens on an instruction.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "kind", rename_all = "snake_case")]
pub enum Inspection {
    /// The instruction executes directly on the CPU.
    Direct,
    /// The instruction silently failed, there was no trap.
    Silent {
        /// Explanation.
        why: String,
    },
    /// Trap: the monitor chooses an emulation.
    Trap {
        /// Trap title.
        title: String,
        /// Options (in model order; the UI may shuffle them).
        options: Vec<TrapOption>,
    },
}

fn opt(label: impl Into<String>, ok: bool, why: Option<&str>) -> TrapOption {
    TrapOption { label: label.into(), ok, why: why.map(str::to_string) }
}

/// What happens on instruction `ins` in state `s` (`translate` — whether binary translation is enabled).
pub fn inspect(ins: &Instr, s: &GuestState, translate: bool) -> Inspection {
    let trap = |title: String, options: Vec<TrapOption>| Inspection::Trap { title, options };
    match ins {
        Instr::Add(_) | Instr::Other => Inspection::Direct,
        Instr::Cli => trap(
            i18n::tr("CLI — disable interrupts").into(),
            vec![
                opt(i18n::tr("virtual flag vif ← 0"), true, None),
                opt(
                    i18n::tr("run CLI on the real CPU"),
                    false,
                    Some(i18n::tr("the monitor would stop receiving timer interrupts and lose control")),
                ),
                opt("vif ← 1", false, Some(i18n::tr("this is the opposite action"))),
            ],
        ),
        Instr::Sti => trap(
            i18n::tr("STI — enable interrupts").into(),
            vec![
                opt(i18n::tr("vif ← 1 and deliver the queue"), true, None),
                opt(i18n::tr("vif ← 1, keep the queue"), false, Some(i18n::tr("interrupts that arrived earlier would never reach the guest"))),
                opt(
                    i18n::tr("run STI on the real CPU"),
                    false,
                    Some(i18n::tr("the real flag is already on: the guest would not get its own state")),
                ),
            ],
        ),
        Instr::Wrcr3(n) => trap(
            i18n::trf!("MOV CR3, {0} — switch page tables", n),
            vec![
                opt(i18n::trf!("virtual vcr3 ← {0}", n), true, None),
                opt(
                    i18n::trf!("write {0} to the real CR3", n),
                    false,
                    Some(i18n::tr("the guest would gain access to foreign memory: the monitor owns the real CR3")),
                ),
                opt(format!("acc ← {n}"), false, Some(i18n::tr("the command writes to CR3, not to the accumulator"))),
            ],
        ),
        Instr::Rdcr3 => trap(
            i18n::tr("MOV acc, CR3 — read the page tables").into(),
            vec![
                opt(i18n::tr("acc ← virtual vcr3"), true, None),
                opt(i18n::tr("acc ← real CR3"), false, Some(i18n::tr("the guest would see the host's real state instead of its own"))),
                opt("vcr3 ← 0", false, Some(i18n::tr("a read must not change anything"))),
            ],
        ),
        Instr::Hlt => trap(
            i18n::tr("HLT — halt the CPU").into(),
            vec![
                opt(i18n::tr("halt the guest's virtual CPU"), true, None),
                opt(i18n::tr("halt the real CPU"), false, Some(i18n::tr("all other guests and the monitor itself would halt"))),
                opt(i18n::tr("do nothing"), false, Some(i18n::tr("the guest is waiting for an interrupt, and the host CPU would spin in vain"))),
            ],
        ),
        Instr::Irq(n) => trap(
            i18n::trf!("external interrupt {0} for the guest", n),
            vec![
                opt(i18n::tr("deliver to the guest now"), s.vif == 1, Some(i18n::tr("the guest has disabled interrupts: it cannot be delivered"))),
                opt(i18n::tr("put in the queue"), s.vif == 0, Some(i18n::tr("the guest has enabled interrupts: no reason to wait"))),
            ],
        ),
        Instr::Popf(n) => {
            if !translate {
                return Inspection::Silent {
                    why: i18n::tr("In ring 1 the POPF instruction cannot change the IF flag, yet it does not raise a trap either: nothing happened, and the monitor never found out.")
                        .into(),
                };
            }
            trap(
                i18n::trf!("POPF {0} — load flags (after translation — a monitor call)", n),
                vec![
                    opt(format!("vif ← {n}"), true, None),
                    opt(i18n::tr("ignore it, as the CPU does"), false, Some(i18n::tr("that is why translation was enabled"))),
                    opt(
                        i18n::tr("run POPF on the real CPU"),
                        false,
                        Some(i18n::tr("the real IF must not depend on the guest")),
                    ),
                ],
            )
        }
    }
}

/// Apply the correct emulation (or direct execution) of an instruction to the state.
pub fn apply(ins: &Instr, s: &GuestState) -> GuestState {
    let mut t = s.clone();
    t.pc += 1;
    match ins {
        Instr::Add(n) => t.acc += n,
        Instr::Cli => t.vif = 0,
        Instr::Sti => {
            t.vif = 1;
            let q = std::mem::take(&mut t.queue);
            t.delivered.extend(q);
        }
        Instr::Wrcr3(n) => t.vcr3 = *n,
        Instr::Rdcr3 => t.acc = t.vcr3,
        Instr::Hlt => t.halted = true,
        Instr::Irq(n) => {
            if t.vif != 0 {
                t.delivered.push(*n);
            } else {
                t.queue.push(*n);
            }
        }
        Instr::Popf(n) => t.vif = *n,
        Instr::Other => {}
    }
    t
}

/// Expected virtual state after correct emulation of the whole program.
pub fn expected(code: &[Instr]) -> GuestState {
    code.iter().fold(initial(), |s, i| apply(i, &s))
}

/// Outcome of a program run (guest halted).
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Finish {
    /// State is correct: the monitor missed no instruction, and acc, vif, vcr3 and delivered interrupts match the expected ones.
    pub ok: bool,
    /// Number of wrong choices during the run.
    pub mistakes: u32,
    /// Final state.
    pub state: GuestState,
    /// Expected state under correct emulation.
    pub want: GuestState,
}

/// Result of the "Step" button.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Stepped {
    /// Nothing to step: the program is halted or finished, or the instruction traps (a choice is needed).
    Blocked,
    /// Instruction executed directly.
    Direct,
    /// Instruction silently failed (POPF without translation).
    Silent {
        /// Explanation for the student.
        why: String,
    },
}

/// Result of choosing an option at a trap.
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Choice {
    /// There is no trap now, or no such option.
    Invalid,
    /// Wrong option: the mistake is recorded, the state is unchanged.
    Wrong {
        /// Why it is not allowed.
        why: String,
    },
    /// Correct option, the program continues.
    Applied,
    /// Correct option, the guest halted: the run is over.
    Finished(Box<Finish>),
}

/// A program run by the student: the same actions as in `HvLab.tsx` (step, choice at a trap, restart).
#[derive(Clone, Debug)]
pub struct Session {
    raw: Vec<String>,
    code: Vec<Instr>,
    translate: bool,
    state: GuestState,
    want: GuestState,
    finish: Option<Finish>,
}

impl Session {
    /// New run of program `code`.
    pub fn new(code: &[String], translate: bool) -> Result<Session, SpecError> {
        let parsed = code.iter().map(|c| Instr::parse(c)).collect::<Result<Vec<_>, _>>()?;
        let want = expected(&parsed);
        Ok(Session { raw: code.to_vec(), code: parsed, translate, state: initial(), want, finish: None })
    }

    /// Current guest state.
    pub fn state(&self) -> &GuestState {
        &self.state
    }

    /// Outcome, if the run ended with the guest halting.
    pub fn finish(&self) -> Option<&Finish> {
        self.finish.as_ref()
    }

    /// Whether binary translation is enabled.
    pub fn translate(&self) -> bool {
        self.translate
    }

    /// The run has already started (translation cannot be changed).
    pub fn started(&self) -> bool {
        self.state.pc > 0 || !self.state.log.is_empty()
    }

    /// Enable/disable translation; before starting. `false` — the run has started, nothing changed.
    pub fn set_translate(&mut self, on: bool) -> bool {
        if self.started() {
            return false;
        }
        self.translate = on;
        true
    }

    /// Restart (translation setting is kept).
    pub fn reset(&mut self) {
        self.state = initial();
        self.finish = None;
    }

    /// Current instruction (as text), if the guest is not halted and the program is not finished.
    pub fn current(&self) -> Option<&str> {
        if self.state.halted {
            return None;
        }
        self.raw.get(self.state.pc).map(String::as_str)
    }

    /// What happens on the current instruction.
    pub fn inspect(&self) -> Option<Inspection> {
        if self.state.halted {
            return None;
        }
        self.code.get(self.state.pc).map(|i| inspect(i, &self.state, self.translate))
    }

    /// The "Step" button: a direct instruction executes, a "silent" one too (changing nothing), at a trap the step is blocked.
    pub fn step(&mut self) -> Stepped {
        let (Some(ins), Some(info)) = (self.code.get(self.state.pc).cloned(), self.inspect()) else {
            return Stepped::Blocked;
        };
        let text = self.raw[self.state.pc].clone();
        match info {
            Inspection::Trap { .. } => Stepped::Blocked,
            Inspection::Direct => {
                let mut t = apply(&ins, &self.state);
                t.log.push(i18n::trf!("{0} — directly on the CPU", text));
                self.state = t;
                Stepped::Direct
            }
            Inspection::Silent { why } => {
                let mut t = self.state.clone();
                t.pc += 1;
                t.silent = true;
                t.log.push(i18n::trf!("{0} — no trap, nothing changed", text));
                self.state = t;
                Stepped::Silent { why }
            }
        }
    }

    /// Choose an option at a trap by its text.
    pub fn choose(&mut self, label: &str) -> Choice {
        let (Some(ins), Some(Inspection::Trap { options, .. })) =
            (self.code.get(self.state.pc).cloned(), self.inspect())
        else {
            return Choice::Invalid;
        };
        let Some(o) = options.iter().find(|o| o.label == label) else {
            return Choice::Invalid;
        };
        if !o.ok {
            self.state.mistakes += 1;
            return Choice::Wrong { why: o.why.clone().unwrap_or_default() };
        }
        let text = self.raw[self.state.pc].clone();
        let mut t = apply(&ins, &self.state);
        t.log.push(i18n::trf!("{0} — trap: {1}", text, o.label));
        self.state = t;
        if self.state.halted {
            let f = self.make_finish();
            self.finish = Some(f.clone());
            return Choice::Finished(Box::new(f));
        }
        Choice::Applied
    }

    fn make_finish(&self) -> Finish {
        let (s, w) = (&self.state, &self.want);
        let ok = !s.silent && s.acc == w.acc && s.vif == w.vif && s.vcr3 == w.vcr3 && s.delivered == w.delivered;
        Finish { ok, mistakes: s.mistakes, state: s.clone(), want: w.clone() }
    }
}

/// One student action in a recorded run.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "step", rename_all = "snake_case")]
pub enum Step {
    /// "Step" on a direct instruction.
    Direct,
    /// "Step" on an instruction that did not trap (POPF without translation).
    Silent,
    /// Option choice at a trap (option text; a wrong choice is recorded too — it counts as a mistake).
    Trap {
        /// Text of the chosen option.
        label: String,
    },
}

/// Recorded run: setting and actions. The client may attach it to the solution, the server replays it.
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct Run {
    /// Whether binary translation was enabled.
    pub translate: bool,
    /// Actions in order.
    pub steps: Vec<Step>,
}

/// Replay a recorded run on a program. Error — the record does not match the model (the action is impossible on this
/// instruction, extra actions after the guest halted, the program was not run to a halt).
pub fn replay(program: &Program, run: &Run) -> Result<Finish, SpecError> {
    let mut s = Session::new(&program.code, run.translate)?;
    for (i, st) in run.steps.iter().enumerate() {
        if s.finish().is_some() {
            return Err(SpecError::new(i18n::trf!("action {0}: after the guest halted", i + 1)));
        }
        let bad = |what: &str| SpecError::new(i18n::trf!("action {0}: {1}", i + 1, what));
        match st {
            Step::Direct => match s.inspect() {
                Some(Inspection::Direct) => {
                    s.step();
                }
                _ => return Err(bad(i18n::tr("the command is not direct"))),
            },
            Step::Silent => match s.inspect() {
                Some(Inspection::Silent { .. }) => {
                    s.step();
                }
                _ => return Err(bad(i18n::tr("the command is not “silent”"))),
            },
            Step::Trap { label } => {
                if s.choose(label) == Choice::Invalid {
                    return Err(bad(i18n::tr("there is no such trap or option")));
                }
            }
        }
    }
    s.finish().cloned().ok_or_else(|| SpecError::new(i18n::tr("the program did not run until the guest halted")))
}

/// Ideal program run: the correct option at every trap. If a "silent" instruction is met without translation,
/// the run continues and ends with an incorrect outcome ([`Finish::ok`] = `false`).
pub fn ideal_run(program: &Program, translate: bool) -> Result<Run, SpecError> {
    let mut s = Session::new(&program.code, translate)?;
    let mut steps = vec![];
    for _ in 0..(program.code.len() * 2 + 4) {
        match s.inspect() {
            None => break,
            Some(Inspection::Direct) => {
                s.step();
                steps.push(Step::Direct);
            }
            Some(Inspection::Silent { .. }) => {
                s.step();
                steps.push(Step::Silent);
            }
            Some(Inspection::Trap { options, .. }) => {
                let Some(o) = options.iter().find(|o| o.ok) else {
                    return Err(SpecError::new(i18n::tr("the trap has no correct option")));
                };
                s.choose(&o.label);
                steps.push(Step::Trap { label: o.label.clone() });
            }
        }
    }
    Ok(Run { translate, steps })
}

/// Whether the program needs binary translation: without it an instruction that does not trap is encountered.
pub fn needs_translation(program: &Program) -> Result<bool, SpecError> {
    Ok(ideal_run(program, false)?.steps.contains(&Step::Silent))
}

/// Default programs (chapter 2 exercise).
pub fn default_programs() -> Vec<Program> {
    let p = |id: &str, title: &str, code: &[&str], goal: &str| Program {
        id: id.into(),
        title: title.into(),
        code: code.iter().map(|c| c.to_string()).collect(),
        goal: goal.into(),
    };
    vec![
        p(
            "base",
            i18n::tr("Privileged instructions"),
            &["ADD 3", "CLI", "WRCR3 4096", "ADD 2", "RDCR3", "STI", "HLT"],
            i18n::tr("Run the program: at every trap choose the correct emulation"),
        ),
        p(
            "irq",
            i18n::tr("Interrupts"),
            &["CLI", "IRQ 1", "IRQ 2", "STI", "HLT"],
            i18n::tr("Do not lose interrupts: they wait in the queue until the guest enables them"),
        ),
        p(
            "popf",
            i18n::tr("The POPF problem"),
            &["CLI", "POPF 1", "ADD 2", "HLT"],
            i18n::tr("Run the program so that POPF changes the virtual IF flag"),
        ),
    ]
}
