//! Процессор «Мини-8»: эмулятор и машина на вентилях ведут себя одинаково на случайных программах;
//! быстрый симулятор ловит петли, память и такт работают.

use archlab::asm::isa::*;
use archlab::asm::{assemble, Machine};
use archlab::cpu8::{cpu8_blocks, CompiledSim, GateMachine};
use archlab::model::*;

struct Lcg(u64);
impl Lcg {
    fn next(&mut self) -> u64 {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        self.0 >> 33
    }
    fn below(&mut self, n: u64) -> u64 {
        self.next() % n
    }
}

/// Случайная корректная программа из `len` команд: все форматы, переходы только вперёд внутри программы.
fn random_program(r: &mut Lcg, len: usize) -> Vec<u16> {
    let mut words = Vec::new();
    for i in 0..len {
        let (a, b, c) = (r.below(8) as u16, r.below(8) as u16, r.below(8) as u16);
        let imm6 = r.below(64) as i32 - 32;
        let w = match r.below(13) {
            0 => (1 << 12) | (a << 9) | r.below(256) as u16, // li
            1 => pack(2, a, b, c as i32),
            2 => pack(3, a, b, c as i32),
            3 => pack(4, a, b, c as i32),
            4 => pack(5, a, b, c as i32),
            5 => pack(6, a, b, c as i32),
            6 => pack(7, a, b, imm6),
            7 => pack(8, a, b, imm6),
            8 => pack(9, a, b, imm6),
            9..=11 => {
                // условный переход вперёд (но не дальше конца программы), чтобы не зациклиться навсегда
                let max_fwd = ((len - 1 - i) as i32).min(31);
                let off = if max_fwd > 0 { r.below(max_fwd as u64 + 1) as i32 } else { 0 };
                pack(10 + r.below(4) as u16, a, b, off)
            }
            _ => (14 << 12) | ((((len - 1 - i) as i32).min(40) as u16).min(r.below(6) as u16 + 1) & 0xfff), // jmp вперёд
        };
        words.push(w);
    }
    words.push(0); // hlt
    words
}

#[test]
fn gate_machine_equals_emulator_on_random_programs() {
    let mut r = Lcg(0x5eed_2026);
    let disk: Vec<u8> = (0..256).map(|i| (i * 37 + 11) as u8).collect();
    for n in 0..40 {
        let program = random_program(&mut r, 8 + (n % 24));
        let mut e = Machine::new(&program, &disk);
        let mut g = GateMachine::new(&program, &disk).expect("машина");
        for step in 0..120 {
            e.step();
            g.step();
            assert_eq!(e.regs.to_vec(), g.regs(), "программа {n}, шаг {step}: регистры\n{:?}", program.iter().map(|w| disassemble(*w)).collect::<Vec<_>>());
            assert_eq!(e.pc as u32, g.pc(), "программа {n}, шаг {step}: счётчик команд");
            assert_eq!(e.halted, g.halted, "программа {n}, шаг {step}: остановка");
            assert_eq!(e.error, g.error, "программа {n}, шаг {step}: ошибка");
        }
        assert_eq!(e.view().mem, g.view().mem, "программа {n}: диск");
        assert_eq!(e.view().last_write, g.view().last_write, "программа {n}: последняя запись");
    }
}

#[test]
fn assembler_and_disassembler_agree() {
    // каждая команда из таблицы ассемблируется и возвращается тем же текстом (кроме перехода: он показывает смещение)
    for op in OPS {
        let asm = assemble(op.example.replace("конец", "+0").replace("цикл", "+0").replace("дальше", "+0").as_str());
        assert!(asm.errors.is_empty(), "{}: {:?}", op.example, asm.errors);
        assert_eq!(asm.words.len(), 1);
        assert_eq!(decode(asm.words[0]).opcode, op.opcode, "{}", op.example);
    }
    for p in PSEUDO {
        let asm = assemble(&format!("{}\nметка: hlt", p.example));
        assert!(asm.errors.is_empty(), "{}: {:?}", p.example, asm.errors);
    }
    assert_eq!(disassemble(pack(7, 1, 2, -5)), "addi r1, r2, -5");
    assert_eq!(disassemble(0xf000), ".word 0xf000");
}

#[test]
fn combinational_loop_is_an_error() {
    let c = Circuit::new(
        vec![
            GateInstance { id: "a".into(), ty: GateType::Not, x: 0.0, y: 0.0 },
            GateInstance { id: "b".into(), ty: GateType::Not, x: 0.0, y: 0.0 },
        ],
        vec![
            Wire { id: "1".into(), from: PinRef::out("a"), to: PinRef::inp("b", PinKind::In0) },
            Wire { id: "2".into(), from: PinRef::out("b"), to: PinRef::inp("a", PinKind::In0) },
        ],
    );
    let err = CompiledSim::new(&c).expect_err("петля");
    assert!(err.to_string().starts_with("В схеме есть петля без триггера"), "{err}");
    // с триггером в петле — можно
    let mut c = c;
    c.gates[1] = GateInstance { id: "b".into(), ty: GateType::Dff, x: 0.0, y: 0.0 };
    c.wires.push(Wire { id: "3".into(), from: PinRef::out("clk"), to: PinRef::inp("b", PinKind::In1) });
    let mut sim = CompiledSim::new(&c).expect("петля через триггер");
    sim.pulse("clk").expect("такт");
    assert_eq!(sim.get("b"), Some(1), "NOT от нуля — единица по фронту");
    sim.pulse("clk").expect("такт");
    assert_eq!(sim.get("b"), Some(0));
    assert!(sim.pulse("нет такого").is_err());
}

#[test]
fn processor_has_the_documented_size() {
    let blocks = cpu8_blocks();
    assert_eq!(blocks.all().len(), 29);
    let cpu = archlab::cpu8::cpu_expansion().expect("процессор");
    assert_eq!(cpu.circuit.natives.len(), 2, "ПЗУ и диск");
    let sim = CompiledSim::new(&cpu.circuit).expect("компиляция");
    // 1254 вентилей в схеме: 1189 комбинационных и 65 триггеров (7 регистров по 8 бит, счётчик команд и триггер остановки)
    assert_eq!((sim.gate_count, sim.dff_count), (1189, 65));
}

#[test]
fn memory_loading_is_checked() {
    let cpu = archlab::cpu8::cpu_expansion().expect("процессор");
    let mut sim = CompiledSim::new(&cpu.circuit).expect("компиляция");
    assert!(sim.load_rom("нет", &[1]).is_err());
    assert!(sim.load_ram("rom__mem", &[1]).is_err(), "ПЗУ — не ОЗУ");
    sim.load_rom("rom__mem", &[0x1234]).expect("ПЗУ");
    sim.load_ram("ram__mem", &[7, 8, 9]).expect("ОЗУ");
    assert_eq!(sim.memory("ram__mem").expect("память")[..4], [7, 8, 9, 0]);
    assert_eq!(sim.memory("rom__mem").expect("память")[0], 0x1234);
    assert!(sim.has_native("ram__mem") && !sim.has_native("x"));
}
