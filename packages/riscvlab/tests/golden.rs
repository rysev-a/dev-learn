//! Дифференциальные тесты: результаты Rust совпадают с «золотыми» результатами прежней реализации на TypeScript.

mod common;

use common::*;
use riscvlab::isa::{self, Ext, Fmt};
use riscvlab::machine::{Machine, Options, MMIO_MAP};
use riscvlab::project::{crc32, make_zip, project_files, project_zip};
use riscvlab::task::{verify, Outcome};
use riscvlab::{assemble, RAM_SIZE};

fn fmt_name(f: Fmt) -> &'static str {
    match f {
        Fmt::R => "R",
        Fmt::I => "I",
        Fmt::SH => "SH",
        Fmt::L => "L",
        Fmt::S => "S",
        Fmt::B => "B",
        Fmt::U => "U",
        Fmt::J => "J",
        Fmt::JR => "JR",
        Fmt::SYS => "SYS",
    }
}

#[test]
fn isa_tables_match_ts() {
    let g = load_golden().isa;
    assert_eq!(g.abi, isa::ABI_NAMES.to_vec());
    assert_eq!(g.ops.len(), isa::OPS.len());
    for (a, b) in g.ops.iter().zip(isa::OPS) {
        assert_eq!(a.mnemonic, b.mnemonic);
        assert_eq!(a.fmt, fmt_name(b.fmt), "{}", a.mnemonic);
        assert_eq!(a.opcode, b.opcode, "{}", a.mnemonic);
        assert_eq!(a.f3, b.f3, "{}", a.mnemonic);
        assert_eq!(a.f7, b.f7, "{}", a.mnemonic);
        assert_eq!(a.ext, if b.ext == Ext::M { "M" } else { "I" });
        assert_eq!(a.meaning, b.meaning);
        assert_eq!(a.example, b.example);
    }
    for (i, o) in isa::OPS.iter().enumerate() {
        assert_eq!(o.op as usize, i, "порядок таблицы и перечисления: {}", o.mnemonic);
        assert_eq!(o.op.mnemonic(), o.mnemonic);
    }
    assert_eq!(g.pseudo.len(), isa::PSEUDO.len());
    for (a, b) in g.pseudo.iter().zip(isa::PSEUDO) {
        assert_eq!((a.example.as_str(), a.becomes.as_str()), (b.example, b.becomes));
    }
    assert_eq!(g.mmio.len(), MMIO_MAP.len());
    for (a, b) in g.mmio.iter().zip(MMIO_MAP) {
        assert_eq!((a.name.as_str(), a.addr, a.note.as_str()), (b.name, b.addr, b.note));
    }
    for r in &g.reg_names {
        assert_eq!(isa::reg_num(&r.name), r.num, "регистр «{}»", r.name);
    }
}

#[test]
fn decode_disassemble_and_fields_match_ts() {
    let g = load_golden();
    assert!(g.decode.len() > 2000);
    for d in &g.decode {
        let got = isa::decode(d.word);
        let ctx = format!("слово {:#010x}", d.word);
        assert_eq!(got.op.map(|o| o.mnemonic()), d.op.as_deref(), "{ctx}");
        assert_eq!((got.rd, got.rs1, got.rs2, got.imm), (d.rd, d.rs1, d.rs2, d.imm), "{ctx}");
        assert_eq!(isa::disassemble(d.word), d.dis, "{ctx}");
        let f = isa::fields_of(d.word);
        assert_eq!(f.fmt.letter(), d.fields.fmt, "{ctx}");
        assert_eq!(f.fields.len(), d.fields.fields.len(), "{ctx}");
        for (a, b) in f.fields.iter().zip(&d.fields.fields) {
            assert_eq!(
                (a.name.as_str(), a.bits.as_str(), a.cls.css()),
                (b.name.as_str(), b.bits.as_str(), b.cls.as_str()),
                "{ctx}"
            );
        }
    }
}

#[test]
fn assembler_matches_ts() {
    let g = load_golden();
    let mut with_errors = 0;
    for a in &g.asm {
        let r = assemble(&a.source);
        let want = &a.result;
        let name = &a.name;
        let errs: Vec<(u32, &str)> = r.errors.iter().map(|e| (e.line, e.message.as_str())).collect();
        let want_errs: Vec<(u32, &str)> = want.errors.iter().map(|e| (e.line, e.message.as_str())).collect();
        assert_eq!(errs, want_errs, "{name}: ошибки");
        if !want.errors.is_empty() {
            with_errors += 1;
        }
        assert_eq!(
            (r.text_size, r.data_size, r.entry),
            (want.text_size, want.data_size, want.entry),
            "{name}: размеры"
        );
        assert_eq!(r.symbols, want.symbols, "{name}: метки");
        assert_eq!(r.image.len(), RAM_SIZE);
        let lines: Vec<_> = r.lines.iter().map(|l| (l.line, l.addr, l.word, l.text.clone(), l.pseudo)).collect();
        let want_lines: Vec<_> =
            want.lines.iter().map(|l| (l.line, l.addr, l.word, l.text.clone(), l.pseudo)).collect();
        assert_eq!(lines, want_lines, "{name}: листинг");
        assert_eq!(fnv(&r.image), want.image_hash, "{name}: образ памяти");
    }
    assert!(g.asm.len() > 80 && with_errors > 20, "образцов {}, с ошибками {with_errors}", g.asm.len());
}

fn machine_for(r: &GRun) -> Machine {
    let mut image = unhex(&r.image_hex);
    image.resize(RAM_SIZE, 0);
    let mut m = Machine::new(&image, Options { switches: r.switches, entry: r.entry });
    for (reg, v) in &r.regs_init {
        m.set_reg(*reg, *v);
    }
    m
}

fn final_of(m: &Machine) -> GFinal {
    let v = m.view();
    GFinal {
        regs: v.regs,
        pc: v.pc,
        steps: v.steps,
        halted: v.halted,
        exit_code: v.exit_code,
        error: v.error,
        uart: v.uart,
        leds: v.leds,
        led_log: v.led_log.iter().map(|e| GLed { cycle: e.cycle, value: e.value }).collect(),
        last_read: v.last_read,
        last_write: v.last_write,
        last_reg: v.last_reg,
        last_insn: v.last_insn,
        mem_hash: fnv(&v.mem),
    }
}

#[test]
fn execution_and_traces_match_ts() {
    let g = load_golden();
    let (mut traced, mut faulted, mut halted) = (0, 0, 0);
    for r in &g.runs {
        let mut m = machine_for(r);
        if let Some(want) = &r.trace {
            let got = m.run_traced(r.max_steps, want.len());
            let got: Vec<GTrace> = got
                .into_iter()
                .map(|t| GTrace {
                    pc: t.pc,
                    insn: t.insn,
                    last_read: t.last_read,
                    last_write: t.last_write,
                    last_reg: t.last_reg,
                    regs: t.regs,
                    steps: t.steps,
                })
                .collect();
            assert_eq!(got.len(), want.len(), "{}: длина трассы", r.name);
            for (i, (a, b)) in got.iter().zip(want).enumerate() {
                assert_eq!(a, b, "{}: шаг {i} трассы", r.name);
            }
            traced += 1;
        } else {
            m.run(r.max_steps);
        }
        assert_eq!(final_of(&m), r.fin, "{}: итоговое состояние", r.name);
        if r.fin.error.is_some() {
            faulted += 1;
        }
        if r.fin.halted {
            halted += 1;
        }
    }
    assert!(
        g.runs.len() > 350 && traced >= 12 && faulted > 100 && halted > 40,
        "прогонов {}, трасс {traced}, ошибок {faulted}, остановок {halted}",
        g.runs.len()
    );
}

#[test]
fn run_traced_equals_run() {
    // трасса не меняет исход: то же состояние, что и у обычного run
    let g = load_golden();
    for r in g.runs.iter().filter(|r| r.name.starts_with("task:") || r.name.starts_with("limit:")) {
        let mut a = machine_for(r);
        let mut b = machine_for(r);
        a.run(r.max_steps);
        b.run_traced(r.max_steps, 1_000_000);
        assert_eq!(final_of(&a), final_of(&b), "{}", r.name);
    }
}

#[test]
fn alu_table_matches_ts() {
    let g = load_golden();
    assert!(g.alu.len() > 4000);
    for (mn, a, b, want) in &g.alu {
        let o = isa::op_by_mnemonic(mn).expect("команда");
        let word = match o.fmt {
            Fmt::R => isa::enc_r(o, 12, 10, 11),
            Fmt::SH => isa::enc_sh(o, 12, 10, *b),
            _ => isa::enc_i(o, 12, 10, *b),
        };
        let mut image = vec![0u8; RAM_SIZE];
        image[..4].copy_from_slice(&word.to_le_bytes());
        image[4..8].copy_from_slice(&isa::EBREAK.to_le_bytes());
        let mut m = Machine::new(&image, Options::default());
        m.set_reg(10, *a);
        if o.fmt == Fmt::R {
            m.set_reg(11, *b);
        }
        m.run(10);
        assert_eq!(m.regs[12], *want, "{mn} {a} {b}");
    }
}

fn mutate(program: &str, mutation: &str, line: Option<usize>) -> String {
    let lines: Vec<&str> = program.split('\n').collect();
    match (mutation, line) {
        ("drop", Some(i)) => {
            lines.iter().enumerate().filter(|(j, _)| *j != i).map(|(_, l)| *l).collect::<Vec<_>>().join("\n")
        }
        ("dup", Some(i)) => {
            let mut out: Vec<&str> = lines[..=i].to_vec();
            out.push(lines[i]);
            out.extend_from_slice(&lines[i + 1..]);
            out.join("\n")
        }
        _ => program.to_string(),
    }
}

#[test]
fn verdicts_match_ts() {
    let g = load_golden();
    let chapters = [load_chapter(16), load_chapter(17)];
    let mut stats = std::collections::BTreeMap::<String, usize>::new();
    for row in &g.verdicts {
        let task = chapters.iter().find_map(|c| c.task(&row.task)).unwrap_or_else(|| panic!("нет задачи {}", row.task));
        let program = match row.mutation.as_str() {
            "solution" => task.spec.reference.clone(),
            "starter" => task.spec.starter.clone(),
            "empty" => String::new(),
            "hand" => row.program.clone().expect("текст программы"),
            m => mutate(&task.spec.reference, m, row.line),
        };
        let v = verify(&task.spec, &program);
        let ctx = format!("{} / {} / {:?}", row.task, row.mutation, row.line);
        let want = &row.verdict;
        assert_eq!(v.ok, want.ok, "{ctx}: ok");
        let outcome = serde_json::to_value(v.outcome).expect("serde");
        assert_eq!(outcome.as_str(), Some(want.outcome.as_str()), "{ctx}: исход");
        if v.outcome == Outcome::AsmErrors {
            let got: Vec<(u32, &str)> = v.errors.iter().map(|e| (e.line, e.message.as_str())).collect();
            let w: Vec<(u32, &str)> = want.errors.iter().flatten().map(|e| (e.line, e.message.as_str())).collect();
            assert_eq!(got, w, "{ctx}: ошибки ассемблера");
        } else {
            assert_eq!(Some(&v.message), want.message.as_ref(), "{ctx}: сообщение");
            assert_eq!(v.tests.first().map(|t| t.steps), want.steps, "{ctx}: число шагов");
        }
        *stats.entry(want.outcome.clone()).or_default() += 1;
    }
    // выборка должна задевать все исходы
    for k in ["passed", "wrong", "fault", "asm_errors"] {
        assert!(stats.get(k).copied().unwrap_or(0) >= 5, "мало примеров исхода {k}: {stats:?}");
    }
}

#[test]
fn project_and_zip_match_ts() {
    let g = load_golden().project;
    let files = project_files(&g.source);
    assert_eq!(files.len(), g.files.len());
    for (a, b) in files.iter().zip(&g.files) {
        assert_eq!(
            (a.name.as_str(), a.content.as_str(), a.note.as_str()),
            (b.name.as_str(), b.content.as_str(), b.note.as_str())
        );
    }
    assert_eq!(project_files(&format!("{}\n", g.source))[0].content, g.source_with_newline);
    assert_eq!(hex(&make_zip(&project_zip(&files))), g.zip_hex);
    for (s, c) in &g.crc {
        assert_eq!(crc32(s.as_bytes()), *c, "crc32({s:?})");
    }
}

fn hex(b: &[u8]) -> String {
    b.iter().map(|x| format!("{x:02x}")).collect()
}
