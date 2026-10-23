//! Данные упражнений и проверка решений: порт самопроверки лаборатории, формат файлов, поведение `verify`.

mod common;

use common::*;
use riscvlab::export::{Export, ExportChapter, ExportTask};
use riscvlab::task::{
    full_source, verify, Check, Lab, LabChapter, Outcome, Profile, RegInit, Task, TaskSpec, Test, MAX_PROGRAM_BYTES,
};
use riscvlab::{assemble, Machine, Options};

fn chapters() -> [LabChapter; 2] {
    [load_chapter(16), load_chapter(17)]
}

#[test]
fn data_files_have_the_expected_shape() {
    let [c16, c17] = chapters();
    assert_eq!((c16.book, c16.chapter, c16.lab), (14, 16, Lab::Riscv));
    assert_eq!((c17.book, c17.chapter, c17.lab), (14, 17, Lab::Riscv));
    let ids16: Vec<&str> = c16.tasks.iter().map(|t| t.id.as_str()).collect();
    assert_eq!(
        ids16,
        [
            "uart-hi",
            "uart-string",
            "leds",
            "switches-invert",
            "sum-100",
            "upper",
            "factorial",
            "sort-words",
            "timer-blink"
        ]
    );
    let ids17: Vec<&str> = c17.tasks.iter().map(|t| t.id.as_str()).collect();
    assert_eq!(
        ids17,
        ["real-hello", "real-print-uint", "real-fizzbuzz", "real-fib", "real-sort-print", "real-exit-code"]
    );
    for t in c16.tasks.iter().chain(&c17.tasks) {
        assert!(!t.title.is_empty() && !t.statement.is_empty() && !t.hint.is_empty(), "{}", t.id);
        assert!(!t.spec.starter.is_empty() && !t.spec.reference.is_empty(), "{}", t.id);
        assert_eq!(t.spec.tests.len(), 1, "{}", t.id);
    }
    assert!(c16.tasks.iter().all(|t| t.spec.profile == Profile::Board));
    assert!(c17.tasks.iter().all(|t| t.spec.profile == Profile::Linux));
}

#[test]
fn data_files_round_trip_through_serde() {
    for n in [16, 17] {
        let path = data_dir().join(format!("14-{n}.json"));
        let text = std::fs::read_to_string(&path).expect("файл");
        let chapter = LabChapter::from_json(&text).expect("разбор");
        // канонический вид: запись даёт тот же текст, а разбор записанного — ту же главу
        assert_eq!(chapter.to_canonical_json().expect("запись"), text, "14-{n}.json не канонический");
        assert_eq!(LabChapter::from_json(&chapter.to_canonical_json().expect("запись")).expect("разбор"), chapter);
        // и на уровне значений JSON ничего не потеряно
        let a: serde_json::Value = serde_json::from_str(&text).expect("json");
        let b = serde_json::to_value(&chapter).expect("значение");
        assert_eq!(a, b);
    }
}

#[test]
fn reference_solutions_pass_every_test() {
    // порт самопроверки лаборатории: эталоны доходят до верного итога
    let mut n = 0;
    for c in chapters() {
        for t in &c.tasks {
            let v = verify(&t.spec, &t.spec.reference);
            assert!(v.ok, "{}: {}", t.id, v.message);
            assert_eq!(v.outcome, Outcome::Passed, "{}", t.id);
            assert_eq!(v.tests.len(), t.spec.tests.len());
            assert!(v.tests.iter().all(|x| x.ok && x.steps > 0), "{}", t.id);
            assert!(v.errors.is_empty());
            n += 1;
        }
    }
    assert_eq!(n, 15);
}

#[test]
fn starters_and_empty_programs_do_not_pass() {
    for c in chapters() {
        for t in &c.tasks {
            let s = verify(&t.spec, &t.spec.starter);
            assert!(!s.ok, "заготовка {} проходит задачу", t.id);
            assert!(s.errors.is_empty(), "заготовка {} не собирается: {:?}", t.id, s.errors);
            let e = verify(&t.spec, "");
            assert!(!e.ok, "пустая программа проходит {}", t.id);
            assert_eq!(e.outcome, Outcome::Fault, "{}: пустая программа — непонятная команда", t.id);
        }
    }
}

#[test]
fn reference_run_details_match_the_statements() {
    // отдельные факты из условий задач
    let [c16, c17] = chapters();
    let run = |t: &Task| {
        let asm = assemble(&t.spec.full_source(&t.spec.reference));
        assert!(asm.errors.is_empty(), "{}: {:?}", t.id, asm.errors);
        let mut m = Machine::new(&asm.image, Options { switches: t.spec.tests[0].switches, entry: asm.entry });
        m.run(t.spec.max_steps);
        m
    };
    let m = run(c16.task("sum-100").expect("задача"));
    assert_eq!(m.regs[10], 5050);
    let m = run(c16.task("factorial").expect("задача"));
    assert_eq!((m.regs[10], m.regs[2]), (720, 0x4000));
    let m = run(c16.task("uart-hi").expect("задача"));
    assert_eq!(m.uart_text(), "Hi!\n");
    let m = run(c17.task("real-hello").expect("задача"));
    assert_eq!((m.uart_text().as_str(), m.exit_code), ("Hello, RISC-V!\n", Some(0)));
    let m = run(c17.task("real-exit-code").expect("задача"));
    assert_eq!(m.exit_code, Some(8), "гласных в «programming in assembly is fun»");
    let m = run(c17.task("real-print-uint").expect("задача"));
    assert_eq!(m.uart_text(), "0\n7\n1234567\n4294967295\n");
    let m = run(c17.task("real-fib").expect("задача"));
    assert!(m.uart_text().starts_with("0\n1\n1\n2\n3\n5\n") && m.uart_text().ends_with("233\n377\n"));
}

#[test]
fn wrong_programs_get_readable_messages() {
    let [c16, c17] = chapters();
    let t = c16.task("leds").expect("задача");
    let v = verify(&t.spec, "  li t0, 0x10001000\n  li t1, 0x5A\n  sw t1, 0(t0)\n  ebreak\n");
    assert_eq!((v.ok, v.outcome), (false, Outcome::Wrong));
    assert_eq!(v.message, "Светодиоды 0b01011010, а ожидалось 0b10100101");

    let t = c16.task("switches-invert").expect("задача");
    let v = verify(&t.spec, "  ebreak\n");
    assert_eq!(v.message, "Светодиоды 0b00000000, а ожидалось 0b01001101 — инверсия 1011 0010");

    let t = c17.task("real-hello").expect("задача");
    assert_eq!(
        verify(&t.spec, "  .globl _start\n_start:\n  ebreak\n").message,
        "Программа не завершилась вызовом exit: нужно li a7, 93 и ecall (код возврата — в a0)."
    );
    let v = verify(&t.spec, "_start:\n  li a0, 4\n  li a7, 93\n  ecall\n");
    assert_eq!(v.message, "Вывод \"\", а ожидалось \"Hello, RISC-V!\\n\"");
}

#[test]
fn assembler_errors_are_reported_with_all_lines() {
    let [c16, _] = chapters();
    let t = c16.task("sum-100").expect("задача");
    let v = verify(&t.spec, "  foo a0\n  addi a0, a0\n  ebreak\n");
    assert_eq!((v.ok, v.outcome), (false, Outcome::AsmErrors));
    assert_eq!(v.errors.len(), 2);
    assert_eq!((v.errors[0].line, v.errors[1].line), (1, 2));
    assert_eq!(v.message, "Строка 1: Неизвестная команда «foo»");
    assert!(v.tests.is_empty());
}

#[test]
fn faults_and_step_limit() {
    let [c16, _] = chapters();
    let t = c16.task("sum-100").expect("задача");
    let v = verify(&t.spec, "l:\n  j l\n");
    assert_eq!(v.outcome, Outcome::Fault);
    assert_eq!(v.message, "Превышен лимит в 200000 шагов — похоже, цикл не заканчивается.");
    assert_eq!(v.tests[0].steps, 200_000);
    let v = verify(&t.spec, "  li t0, 0x1001\n  lw a0, 0(t0)\n  ebreak\n");
    assert!(v.message.starts_with("Невыровненное чтение по адресу 0x00001001"), "{}", v.message);
}

#[test]
fn oversized_program_is_rejected_without_assembling() {
    let [c16, _] = chapters();
    let t = c16.task("sum-100").expect("задача");
    let v = verify(&t.spec, &"nop\n".repeat(MAX_PROGRAM_BYTES / 4 + 10));
    assert_eq!(v.outcome, Outcome::AsmErrors);
    assert!(v.message.contains("слишком длинная"));
}

#[test]
fn without_reference_hides_only_the_reference() {
    let [c16, _] = chapters();
    let open = c16.without_references();
    for (a, b) in c16.tasks.iter().zip(&open.tasks) {
        assert_eq!(b.spec.reference, "");
        assert_eq!((&a.spec.starter, &a.spec.data, &a.spec.tests), (&b.spec.starter, &b.spec.data, &b.spec.tests));
        assert_eq!((&a.id, &a.title, &a.statement, &a.hint), (&b.id, &b.title, &b.statement, &b.hint));
        // проверка работает и без эталона: вердикт тот же
        assert_eq!(verify(&b.spec, &a.spec.reference), verify(&a.spec, &a.spec.reference));
    }
    assert!(!serde_json::to_string(&open).expect("json").contains("li   t0, 0x10001000   # светодиоды"));
}

fn spec_with(tests: Vec<Test>) -> TaskSpec {
    TaskSpec {
        profile: Profile::Board,
        starter: String::new(),
        reference: String::new(),
        data: "w:\n  .word 7\n".into(),
        max_steps: 1000,
        tests,
    }
}

#[test]
fn several_tests_and_initial_registers() {
    // два теста с разными переключателями: инверсия считается по входу
    let invert = |sw: u8, want: u8| Test {
        switches: sw,
        regs: vec![],
        check: Check::Leds { expected: want, ok: format!("ok {sw}"), bad_suffix: String::new() },
    };
    let spec = spec_with(vec![invert(0b1011_0010, 0b0100_1101), invert(0b0000_1111, 0b1111_0000)]);
    let prog = "  li t0, 0x10001004\n  li t1, 0x10001000\n  lw t2, 0(t0)\n  not t2, t2\n  sw t2, 0(t1)\n  ebreak\n";
    let v = verify(&spec, prog);
    assert!(v.ok, "{}", v.message);
    assert_eq!(v.message, "ok 15", "при успехе — сообщение последнего теста");
    assert_eq!(v.tests.len(), 2);
    // а эта программа верна только для первого входа: сообщение — по первому неудавшемуся
    let fixed = "  li t1, 0x10001000\n  li t2, 0x4d\n  sw t2, 0(t1)\n  ebreak\n";
    let v = verify(&spec, fixed);
    assert!(!v.ok);
    assert_eq!(v.outcome, Outcome::Wrong);
    assert_eq!(v.message, "Светодиоды 0b01001101, а ожидалось 0b11110000");
    assert_eq!(v.tests.iter().map(|t| t.ok).collect::<Vec<_>>(), [true, false]);

    // начальные регистры и данные задания по метке
    let t = Test {
        switches: 0,
        regs: vec![RegInit { reg: 10, value: 40 }, RegInit { reg: 0, value: 99 }],
        check: Check::Reg { reg: 11, expected: 47, ok: "сумма".into() },
    };
    let spec = spec_with(vec![t]);
    let v = verify(&spec, "  la t0, w\n  lw t1, 0(t0)\n  add a1, a0, t1\n  ebreak\n");
    assert!(v.ok, "{}", v.message);
    assert_eq!(full_source("x", "d"), "x\n.data\nd\n");
    // без тестов проверять нечего
    assert!(!verify(&spec_with(vec![]), "ebreak").ok);
}

#[test]
fn check_json_shape_is_stable() {
    let c: Check =
        serde_json::from_str(r#"{"kind":"mem_words","symbol":"arr","expected":[1,-2],"ok":"ок"}"#).expect("разбор");
    assert_eq!(c, Check::MemWords { symbol: "arr".into(), expected: vec![1, -2], ok: "ок".into() });
    assert_eq!(serde_json::to_string(&Check::StackReturned).expect("json"), r#"{"kind":"stack_returned"}"#);
    // опечатка в названии поля — ошибка, а не молчаливая потеря
    assert!(serde_json::from_str::<Check>(r#"{"kind":"uart","expected":"x","ok":"y","oops":1}"#).is_err());
    assert!(serde_json::from_str::<Check>(r#"{"kind":"nope"}"#).is_err());
}

fn export_task(id: &str, solution: &str, check: Check) -> ExportTask {
    ExportTask {
        id: id.into(),
        title: "t".into(),
        text: "s".into(),
        hint: "h".into(),
        starter: "  ebreak\n".into(),
        solution: solution.into(),
        data: String::new(),
        switches: 0,
        max_steps: None,
        check,
    }
}

#[test]
fn export_conversion_validates_tasks() {
    let leds = |v: u8| Check::Leds { expected: v, ok: "ок".into(), bad_suffix: String::new() };
    let good = "  li t0, 0x10001000\n  li t1, 5\n  sw t1, 0(t0)\n  ebreak\n";
    let ch = |tasks| ExportChapter { book: 14, chapter: 16, profile: Profile::Board, tasks };
    let ok = ch(vec![export_task("a", good, leds(5))]).into_lab_chapter().expect("глава");
    assert_eq!((ok.book, ok.chapter, ok.lab), (14, 16, Lab::Riscv));
    assert_eq!(ok.tasks[0].statement, "s");
    assert_eq!(ok.tasks[0].spec.max_steps, 200_000);
    // эталон не проходит
    let e = ch(vec![export_task("a", good, leds(6))]).into_lab_chapter().expect_err("ошибка");
    assert!(e.to_string().contains("эталон задачи a не проходит"), "{e}");
    // пустая программа проходит — задача бессмысленна
    // (пустая программа до `.data` ничего не делает, но данные задания могут вернуться в `.text`)
    let mut t = export_task("b", "ebreak\n", Check::Uart { expected: String::new(), ok: "ок".into() });
    t.data = ".text\n  ebreak\n".into();
    let e = ch(vec![t]).into_lab_chapter().expect_err("ошибка");
    assert!(e.to_string().contains("пустая программа проходит задачу b"), "{e}");
    // формат файла выгрузки
    let text = r#"{"version":1,"chapters":[{"book":14,"chapter":17,"profile":"linux","tasks":[]}]}"#;
    let ex: Export = serde_json::from_str(text).expect("выгрузка");
    assert_eq!(ex.chapters[0].profile, Profile::Linux);
}
