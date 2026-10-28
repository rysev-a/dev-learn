//! The "Mini-8" processor: the emulator and the gate-level machine behave identically on random programs;
//! the fast simulator catches loops, memory and the clock work.

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

/// Random valid program of `len` instructions: all formats, jumps only forward within the program.
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
                // conditional jump forward (but not past the end of the program) so it never loops forever
                let max_fwd = ((len - 1 - i) as i32).min(31);
                let off = if max_fwd > 0 { r.below(max_fwd as u64 + 1) as i32 } else { 0 };
                pack(10 + r.below(4) as u16, a, b, off)
            }
            _ => (14 << 12) | ((((len - 1 - i) as i32).min(40) as u16).min(r.below(6) as u16 + 1) & 0xfff), // jmp forward
        };
        words.push(w);
    }
    words.push(0); // hlt
    words
}

#[test]
fn gate_machine_equals_emulator_on_random_programs() {
    locales::set_locale(i18n::Locale::Ru);
    let mut r = Lcg(0x5eed_2026);
    let disk: Vec<u8> = (0..256).map(|i| (i * 37 + 11) as u8).collect();
    for n in 0..40 {
        let program = random_program(&mut r, 8 + (n % 24));
        let mut e = Machine::new(&program, &disk);
        let mut g = GateMachine::new(&program, &disk).expect("machine");
        for step in 0..120 {
            e.step();
            g.step();
            assert_eq!(e.regs.to_vec(), g.regs(), "program {n}, step {step}: registers\n{:?}", program.iter().map(|w| disassemble(*w)).collect::<Vec<_>>());
            assert_eq!(e.pc as u32, g.pc(), "program {n}, step {step}: program counter");
            assert_eq!(e.halted, g.halted, "program {n}, step {step}: halt");
            assert_eq!(e.error, g.error, "program {n}, step {step}: error");
        }
        assert_eq!(e.view().mem, g.view().mem, "program {n}: disk");
        assert_eq!(e.view().last_write, g.view().last_write, "program {n}: last write");
    }
}

#[test]
fn assembler_and_disassembler_agree() {
    locales::set_locale(i18n::Locale::Ru);
    // every instruction from the table assembles and comes back as the same text (except the jump: it shows the offset)
    for op in OPS {
        let asm = assemble(op.example.replace("end", "+0").replace("loop", "+0").replace("next", "+0").as_str());
        assert!(asm.errors.is_empty(), "{}: {:?}", op.example, asm.errors);
        assert_eq!(asm.words.len(), 1);
        assert_eq!(decode(asm.words[0]).opcode, op.opcode, "{}", op.example);
    }
    for p in PSEUDO {
        let asm = assemble(&format!("{}\nlabel: hlt", p.example));
        assert!(asm.errors.is_empty(), "{}: {:?}", p.example, asm.errors);
    }
    assert_eq!(disassemble(pack(7, 1, 2, -5)), "addi r1, r2, -5");
    assert_eq!(disassemble(0xf000), ".word 0xf000");
}

#[test]
fn combinational_loop_is_an_error() {
    locales::set_locale(i18n::Locale::Ru);
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
    let err = CompiledSim::new(&c).expect_err("loop");
    assert!(err.to_string().starts_with("В схеме есть петля без триггера"), "{err}");
    // with a flip-flop in the loop — allowed
    let mut c = c;
    c.gates[1] = GateInstance { id: "b".into(), ty: GateType::Dff, x: 0.0, y: 0.0 };
    c.wires.push(Wire { id: "3".into(), from: PinRef::out("clk"), to: PinRef::inp("b", PinKind::In1) });
    let mut sim = CompiledSim::new(&c).expect("loop through a flip-flop");
    sim.pulse("clk").expect("clock");
    assert_eq!(sim.get("b"), Some(1), "NOT of zero is one on the edge");
    sim.pulse("clk").expect("clock");
    assert_eq!(sim.get("b"), Some(0));
    assert!(sim.pulse("no such").is_err());
}

#[test]
fn processor_has_the_documented_size() {
    locales::set_locale(i18n::Locale::Ru);
    let blocks = cpu8_blocks();
    assert_eq!(blocks.all().len(), 29);
    let cpu = archlab::cpu8::cpu_expansion().expect("processor");
    assert_eq!(cpu.circuit.natives.len(), 2, "ROM and disk");
    let sim = CompiledSim::new(&cpu.circuit).expect("compilation");
    // 1254 gates in the circuit: 1189 combinational and 65 flip-flops (7 registers of 8 bits, program counter and the halt flip-flop)
    assert_eq!((sim.gate_count, sim.dff_count), (1189, 65));
}

#[test]
fn memory_loading_is_checked() {
    locales::set_locale(i18n::Locale::Ru);
    let cpu = archlab::cpu8::cpu_expansion().expect("processor");
    let mut sim = CompiledSim::new(&cpu.circuit).expect("compilation");
    assert!(sim.load_rom("none", &[1]).is_err());
    assert!(sim.load_ram("rom__mem", &[1]).is_err(), "ROM is not RAM");
    sim.load_rom("rom__mem", &[0x1234]).expect("ROM");
    sim.load_ram("ram__mem", &[7, 8, 9]).expect("RAM");
    assert_eq!(sim.memory("ram__mem").expect("memory")[..4], [7, 8, 9, 0]);
    assert_eq!(sim.memory("rom__mem").expect("memory")[0], 0x1234);
    assert!(sim.has_native("ram__mem") && !sim.has_native("x"));
}
