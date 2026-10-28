//! Block catalog of the "Mini-8" processor.
//! Everything is built from AND, OR, NOT, XOR gates and the DFF flip-flop — the very ones the student built on the board.
//! Small blocks (multiplexer, full adder, register bit) are reused in larger ones:
//! a byte register is eight bit registers, the register file is seven byte registers and two multiplexers.
//! Port of `cpu8/blocks.ts`.

use super::builders::*;
use crate::blocks::*;
use crate::interfaces::Iface::{self, *};
use std::collections::HashMap;
use std::sync::OnceLock;

/// Instruction numbers (opcodes) — as in `asm::isa`.
mod op {
    pub const HLT: usize = 0;
    pub const LI: usize = 1;
    pub const ADD: usize = 2;
    pub const SUB: usize = 3;
    pub const AND: usize = 4;
    pub const OR: usize = 5;
    pub const XOR: usize = 6;
    pub const ADDI: usize = 7;
    pub const LB: usize = 8;
    pub const SB: usize = 9;
    pub const BEQ: usize = 10;
    pub const BNE: usize = 11;
    pub const BLTU: usize = 12;
    pub const BGEU: usize = 13;
    pub const JMP: usize = 14;
    pub const ALL: [usize; 15] = [HLT, LI, ADD, SUB, AND, OR, XOR, ADDI, LB, SB, BEQ, BNE, BLTU, BGEU, JMP];
}

const BITS: [usize; 8] = [0, 1, 2, 3, 4, 5, 6, 7];

fn s(x: &str) -> String {
    x.to_string()
}

fn pairs(list: &[(String, String)]) -> Vec<(String, String)> {
    list.to_vec()
}

fn build_blocks() -> Vec<GeneratedBlock> {
    let mut blocks: Vec<GeneratedBlock> = Vec::new();

    /* ===================== Bits ===================== */

    blocks.push(gate_block(
        "c8-mux2",
        i18n::tr("Multiplexer 2→1 (bit)"),
        &[pin("s", Bit), pin("d0", Bit), pin("d1", Bit), pout("y", Bit)],
        |g| {
            let ns = g.not("s");
            g.out("y", g.or(g.and("d0", &ns), g.and("d1", "s")));
        },
    ));

    blocks.push(gate_block(
        "c8-ha",
        i18n::tr("Half adder"),
        &[pin("a", Bit), pin("b", Bit), pout("sum", Bit), pout("cout", Bit)],
        |g| {
            g.out("sum", g.xor("a", "b"));
            g.out("cout", g.and("a", "b"));
        },
    ));

    blocks.push(gate_block(
        "c8-fa",
        i18n::tr("Full adder"),
        &[pin("a", Bit), pin("b", Bit), pin("cin", Bit), pout("sum", Bit), pout("cout", Bit)],
        |g| {
            let p = g.xor("a", "b");
            g.out("sum", g.xor(&p, "cin"));
            g.out("cout", g.or(g.and("a", "b"), g.and(&p, "cin")));
        },
    ));

    blocks.push(gate_block(
        "c8-reg1",
        i18n::tr("Register bit with write"),
        &[pin("d", Bit), pin("load", Bit), pin("clk", Clk), pout("q", Bit)],
        |g| {
            // "itself or the new value": at load = 0 the flip-flop receives its own output
            let nl = g.not("load");
            let keep = g.and("q_ff", &nl);
            let take = g.and("d", "load");
            g.dff_at("q_ff", g.or(&keep, &take), "clk");
            g.out("q", "q_ff");
        },
    ));

    blocks.push(gate_block(
        "c8-alu1",
        i18n::tr("ALU bit slice"),
        &[
            pin("a", Bit),
            pin("b", Bit),
            pin("cin", Bit),
            pin("sub", Bit),
            pin("sAdd", Bit),
            pin("sAnd", Bit),
            pin("sOr", Bit),
            pin("sXor", Bit),
            pin("sB", Bit),
            pout("res", Bit),
            pout("cout", Bit),
        ],
        |g| {
            // arithmetic: on subtraction B is inverted and the carry into the least significant bit is 1
            let bx = g.xor("b", "sub");
            let p = g.xor("a", &bx);
            let sum = g.xor(&p, "cin");
            g.out("cout", g.or(g.and("a", &bx), g.and(&p, "cin")));
            // logic: all results are computed at once, and the control signals select the needed one
            let t_add = g.and(&sum, "sAdd");
            let t_and = g.and(g.and("a", "b"), "sAnd");
            let t_or = g.and(g.or("a", "b"), "sOr");
            let t_xor = g.and(g.xor("a", "b"), "sXor");
            let t_b = g.and("b", "sB");
            g.out("res", g.or_all(&[t_add, t_and, t_or, t_xor, t_b]));
        },
    ));

    blocks.push(gate_block(
        "c8-cmp0",
        i18n::tr("Compare: lowest bit"),
        &[pin("x", Bit), pin("y", Bit), pout("lt", Bit), pout("eq", Bit)],
        |g| {
            g.out("lt", g.and(g.not("x"), "y"));
            g.out("eq", g.xnor("x", "y"));
        },
    ));

    blocks.push(gate_block(
        "c8-cmp1",
        i18n::tr("Compare: bit slice"),
        &[pin("x", Bit), pin("y", Bit), pin("ltIn", Bit), pout("lt", Bit), pout("eq", Bit)],
        |g| {
            // x < y if in this bit x = 0 and y = 1, or the bits are equal and the lower bits already gave "less"
            let eq = g.xnor("x", "y");
            g.out("lt", g.or(g.and(g.not("x"), "y"), g.and(&eq, "ltIn")));
            g.out("eq", &eq);
        },
    ));

    blocks.push(gate_block("c8-and8", i18n::tr("AND of eight"), &[pin("x", Byte), pout("y", Bit)], |g| {
        let xs: Vec<String> = BITS.iter().map(|i| bit("x", *i)).collect();
        g.out("y", g.and_all(&xs));
    }));

    blocks.push(gate_block("c8-zero8", i18n::tr("Zero byte"), &[pin("a", Clk), pout("y", Byte)], |g| {
        // a signal AND its inverse — always 0
        let z = g.and("a", g.not("a"));
        for i in BITS {
            g.out(bit("y", i), &z);
        }
    }));

    blocks.push(gate_block("c8-one8", i18n::tr("Constant 1 (byte)"), &[pin("a", Clk), pout("y", Byte)], |g| {
        let z = g.and("a", g.not("a"));
        g.out(bit("y", 0), g.not(&z));
        for i in &BITS[1..] {
            g.out(bit("y", *i), &z);
        }
    }));

    blocks.push(gate_block(
        "c8-wdec",
        i18n::tr("Write decoder"),
        &[pin("s", Reg3), pin("we", Bit), pout("en", Oh8)],
        |g| {
            let (s2, s1, s0) = (bit("s", 2), bit("s", 1), bit("s", 0));
            let (n2, n1, n0) = (g.not(&s2), g.not(&s1), g.not(&s0));
            let pair = [g.and(&n1, &n0), g.and(&n1, &s0), g.and(&s1, &n0), g.and(&s1, &s0)];
            for k in 0..8usize {
                let hi = if k >> 2 != 0 { &s2 } else { &n2 };
                let t = g.and(hi, &pair[k & 3]);
                g.out(field("en", &format!("H{k}")), g.and(&t, "we"));
            }
        },
    ));

    /* ===================== Control ===================== */

    blocks.push(gate_block("c8-decode", i18n::tr("Instruction decoder"), &[pin("op", Op4), pout("ctl", Ctrl)], |g| {
        let o: Vec<String> = (0..4).map(|i| bit("op", i)).collect();
        let neg: Vec<String> = o.iter().map(|x| g.not(x)).collect();
        let lit = |i: usize, v: usize| if v != 0 { &o[i] } else { &neg[i] };
        // the "high" and "low" bit pairs of the opcode — four variants each
        let hi: Vec<String> = (0..4usize).map(|k| g.and(lit(3, k >> 1), lit(2, k & 1))).collect();
        let lo: Vec<String> = (0..4usize).map(|k| g.and(lit(1, k >> 1), lit(0, k & 1))).collect();
        let mut m: HashMap<usize, String> = HashMap::new();
        for code in op::ALL {
            let v = g.and(&hi[code >> 2], &lo[code & 3]);
            m.insert(code, v);
        }
        let any = |codes: &[usize]| {
            let xs: Vec<&String> = codes.iter().map(|c| &m[c]).collect();
            g.or_all(&xs)
        };
        let set = |name: &str, src: &str| g.out(field("ctl", name), src);
        use op::*;
        set("regWrite", &any(&[LI, ADD, SUB, AND, OR, XOR, ADDI, LB]));
        set("selAdd", &any(&[ADD, SUB, ADDI, LB, SB]));
        set("selAnd", &m[&AND]);
        set("selOr", &m[&OR]);
        set("selXor", &m[&XOR]);
        set("selB", &m[&LI]);
        set("sub", &m[&SUB]);
        set("useImm6", &any(&[ADDI, LB, SB]));
        set("useImm8", &m[&LI]);
        set("load", &m[&LB]);
        set("store", &m[&SB]);
        set("isBeq", &m[&BEQ]);
        set("isBne", &m[&BNE]);
        set("isBltu", &m[&BLTU]);
        set("isBgeu", &m[&BGEU]);
        set("isJmp", &m[&JMP]);
        set("isHlt", &m[&HLT]);
        set("isR", &any(&[ADD, SUB, AND, OR, XOR]));
    }));

    blocks.push(gate_block(
        "c8-branch",
        i18n::tr("Branch decision"),
        &[pin("ctl", Ctrl), pin("eq", Bit), pin("lt", Bit), pout("take", Bit)],
        |g| {
            let c = |f: &str| field("ctl", f);
            let t1 = g.and(c("isBeq"), "eq");
            let t2 = g.and(c("isBne"), g.not("eq"));
            let t3 = g.and(c("isBltu"), "lt");
            let t4 = g.and(c("isBgeu"), g.not("lt"));
            g.out("take", g.or_all(&[t1, t2, t3, t4]));
        },
    ));

    blocks.push(gate_block(
        "c8-halt",
        i18n::tr("Halt"),
        &[pin("clk", Clk), pin("isHlt", Bit), pout("halted", Bit), pout("run", Bit)],
        |g| {
            // once hlt is seen, the flip-flop holds one until the end of the run
            g.dff_at("h_ff", g.or("h_ff", "isHlt"), "clk");
            g.out("halted", "h_ff");
            g.out("run", g.not("h_ff"));
        },
    ));

    blocks.push(gate_block(
        "c8-gate-en",
        i18n::tr("Write enables"),
        &[pin("ctl", Ctrl), pin("run", Bit), pout("pcEn", Bit), pout("regWe", Bit), pout("ramWe", Bit)],
        |g| {
            // while the processor is not halted: the program counter steps (except hlt), the register and the disk write on command
            g.out("pcEn", g.and("run", g.not(field("ctl", "isHlt"))));
            g.out("regWe", g.and("run", field("ctl", "regWrite")));
            g.out("ramWe", g.and("run", field("ctl", "store")));
        },
    ));

    let mut imm_links: Vec<(String, String)> = Vec::new();
    // six bits sign-extended to a byte
    for i in 0..6 {
        imm_links.push((bit("instr", i), bit("imm6", i)));
    }
    imm_links.push((bit("instr", 5), bit("imm6", 6)));
    imm_links.push((bit("instr", 5), bit("imm6", 7)));
    // the eight low bits of the instruction — the number for li and the offset for jmp
    for i in BITS {
        imm_links.push((bit("instr", i), bit("imm8", i)));
    }
    blocks.push(wire_block(
        "c8-immgen",
        i18n::tr("Immediates from instruction"),
        &[pin("instr", Instr16), pout("imm6", Byte), pout("imm8", Byte)],
        &pairs(&imm_links),
    ));

    /* ===================== Byte blocks ===================== */

    blocks.push(hier_block(
        "c8-mux2x8",
        i18n::tr("Multiplexer 2→1 (byte)"),
        &[pin("s", Bit), pin("d0", Byte), pin("d1", Byte), pout("y", Byte)],
        |h| {
            for i in BITS {
                h.inst(&format!("m{i}"), "c8-mux2");
                h.link("$.s", &format!("m{i}.s"))
                    .link(&format!("$.d0.B{i}"), &format!("m{i}.d0"))
                    .link(&format!("$.d1.B{i}"), &format!("m{i}.d1"))
                    .link(&format!("m{i}.y"), &format!("$.y.B{i}"));
            }
        },
    ));

    blocks.push(hier_block(
        "c8-mux2x3",
        i18n::tr("Multiplexer 2→1 (register number)"),
        &[pin("s", Bit), pin("d0", Reg3), pin("d1", Reg3), pout("y", Reg3)],
        |h| {
            for i in [0, 1, 2] {
                h.inst(&format!("m{i}"), "c8-mux2");
                h.link("$.s", &format!("m{i}.s"))
                    .link(&format!("$.d0.R{i}"), &format!("m{i}.d0"))
                    .link(&format!("$.d1.R{i}"), &format!("m{i}.d1"))
                    .link(&format!("m{i}.y"), &format!("$.y.R{i}"));
            }
        },
    ));

    blocks.push(hier_block(
        "c8-reg8",
        i18n::tr("8-bit register"),
        &[pin("d", Byte), pin("load", Bit), pin("clk", Clk), pout("q", Byte)],
        |h| {
            for i in BITS {
                h.inst(&format!("b{i}"), "c8-reg1");
                h.link(&format!("$.d.B{i}"), &format!("b{i}.d"))
                    .link("$.load", &format!("b{i}.load"))
                    .link("$.clk", &format!("b{i}.clk"))
                    .link(&format!("b{i}.q"), &format!("$.q.B{i}"));
            }
        },
    ));

    blocks.push(hier_block(
        "c8-add8",
        i18n::tr("8-bit adder"),
        &[pin("a", Byte), pin("b", Byte), pout("s", Byte)],
        |h| {
            for i in BITS {
                h.inst(&format!("s{i}"), if i == 0 { "c8-ha" } else { "c8-fa" });
                h.link(&format!("$.a.B{i}"), &format!("s{i}.a"))
                    .link(&format!("$.b.B{i}"), &format!("s{i}.b"))
                    .link(&format!("s{i}.sum"), &format!("$.s.B{i}"));
                if i > 0 {
                    h.link(&format!("s{}.cout", i - 1), &format!("s{i}.cin"));
                }
            }
        },
    ));

    blocks.push(hier_block(
        "c8-alu8",
        i18n::tr("8-bit ALU"),
        &[
            pin("a", Byte),
            pin("b", Byte),
            pin("sub", Bit),
            pin("sAdd", Bit),
            pin("sAnd", Bit),
            pin("sOr", Bit),
            pin("sXor", Bit),
            pin("sB", Bit),
            pout("res", Byte),
        ],
        |h| {
            for i in BITS {
                h.inst(&format!("s{i}"), "c8-alu1");
                h.link(&format!("$.a.B{i}"), &format!("s{i}.a"))
                    .link(&format!("$.b.B{i}"), &format!("s{i}.b"))
                    .link(&format!("s{i}.res"), &format!("$.res.B{i}"));
                for sig in ["sub", "sAdd", "sAnd", "sOr", "sXor", "sB"] {
                    h.link(&format!("$.{sig}"), &format!("s{i}.{sig}"));
                }
                // the carry runs from the least significant bit to the most significant; subtraction is adding NOT-B and one
                let cin = if i == 0 { s("$.sub") } else { format!("s{}.cout", i - 1) };
                h.link(&cin, &format!("s{i}.cin"));
            }
        },
    ));

    blocks.push(hier_block(
        "c8-cmp8",
        i18n::tr("Byte compare"),
        &[pin("x", Byte), pin("y", Byte), pout("eq", Bit), pout("lt", Bit)],
        |h| {
            for i in BITS {
                h.inst(&format!("c{i}"), if i == 0 { "c8-cmp0" } else { "c8-cmp1" });
                h.link(&format!("$.x.B{i}"), &format!("c{i}.x")).link(&format!("$.y.B{i}"), &format!("c{i}.y"));
                if i > 0 {
                    h.link(&format!("c{}.lt", i - 1), &format!("c{i}.ltIn"));
                }
            }
            h.inst("all", "c8-and8");
            for i in BITS {
                h.link(&format!("c{i}.eq"), &format!("all.x.B{i}"));
            }
            h.link("all.y", "$.eq").link("c7.lt", "$.lt");
        },
    ));

    /* ===================== Registers and program counter ===================== */

    blocks.push(hier_block(
        "c8-mux4x8",
        i18n::tr("Multiplexer 4→1 (byte)"),
        &[pin("s", Word2), pin("d0", Byte), pin("d1", Byte), pin("d2", Byte), pin("d3", Byte), pout("y", Byte)],
        |h| {
            h.inst("lo", "c8-mux2x8").inst("hi", "c8-mux2x8").inst("top", "c8-mux2x8");
            h.link("$.s.D0", "lo.s").link("$.d0", "lo.d0").link("$.d1", "lo.d1");
            h.link("$.s.D0", "hi.s").link("$.d2", "hi.d0").link("$.d3", "hi.d1");
            h.link("$.s.D1", "top.s").link("lo.y", "top.d0").link("hi.y", "top.d1").link("top.y", "$.y");
        },
    ));

    let mut mux8_specs: Vec<PortSpec> = vec![pin("s", Reg3)];
    mux8_specs.extend(BITS.iter().map(|i| pin(format!("d{i}"), Byte)));
    mux8_specs.push(pout("y", Byte));
    blocks.push(hier_block("c8-mux8x8", i18n::tr("Multiplexer 8→1 (byte)"), &mux8_specs, |h| {
        h.inst("lo", "c8-mux4x8").inst("hi", "c8-mux4x8").inst("top", "c8-mux2x8");
        for (m, base) in [("lo", 0usize), ("hi", 4)] {
            h.link("$.s.R1", &format!("{m}.s.D1")).link("$.s.R0", &format!("{m}.s.D0"));
            for k in [0usize, 1, 2, 3] {
                h.link(&format!("$.d{}", base + k), &format!("{m}.d{k}"));
            }
        }
        h.link("$.s.R2", "top.s").link("lo.y", "top.d0").link("hi.y", "top.d1").link("top.y", "$.y");
    }));

    let mut rf_specs: Vec<PortSpec> = vec![
        pin("clk", Clk),
        pin("we", Bit),
        pin("wsel", Reg3),
        pin("wdata", Byte),
        pin("rsel1", Reg3),
        pin("rsel2", Reg3),
        pout("rd1", Byte),
        pout("rd2", Byte),
    ];
    rf_specs.extend((1..=7).map(|k| pout(format!("r{k}"), Byte)));
    blocks.push(hier_block("c8-regfile", i18n::tr("Register file"), &rf_specs, |h| {
        h.inst("wdec", "c8-wdec").inst("z", "c8-zero8").inst("m1", "c8-mux8x8").inst("m2", "c8-mux8x8");
        h.link("$.wsel", "wdec.s").link("$.we", "wdec.we");
        h.link("$.clk", "z.a").link("z.y", "m1.d0").link("z.y", "m2.d0"); // r0 is always zero
        for k in 1..=7 {
            h.inst(&format!("r{k}"), "c8-reg8");
            h.link("$.clk", &format!("r{k}.clk"))
                .link("$.wdata", &format!("r{k}.d"))
                .link(&format!("wdec.en.H{k}"), &format!("r{k}.load"))
                .link(&format!("r{k}.q"), &format!("m1.d{k}"))
                .link(&format!("r{k}.q"), &format!("m2.d{k}"))
                .link(&format!("r{k}.q"), &format!("$.r{k}"));
        }
        h.link("$.rsel1", "m1.s").link("$.rsel2", "m2.s").link("m1.y", "$.rd1").link("m2.y", "$.rd2");
    }));

    blocks.push(hier_block(
        "c8-pc",
        i18n::tr("Program counter"),
        &[
            pin("clk", Clk),
            pin("run", Bit),
            pin("take", Bit),
            pin("isJmp", Bit),
            pin("imm6", Byte),
            pin("imm8", Byte),
            pout("pc", Byte),
        ],
        |h| {
            h.inst("reg", "c8-reg8").inst("add", "c8-add8").inst("one", "c8-one8");
            h.inst("stepJ", "c8-mux2x8").inst("step", "c8-mux2x8");
            // step: +1 by default; for jmp — the offset from the instruction; for a conditional jump — the short offset
            h.link("$.clk", "one.a").link("$.isJmp", "stepJ.s").link("one.y", "stepJ.d0").link("$.imm8", "stepJ.d1");
            h.link("$.take", "step.s").link("stepJ.y", "step.d0").link("$.imm6", "step.d1");
            h.link("reg.q", "add.a").link("step.y", "add.b").link("add.s", "reg.d");
            h.link("$.clk", "reg.clk").link("$.run", "reg.load").link("reg.q", "$.pc");
        },
    ));

    /* ===================== Memory ===================== */

    blocks.push(native_block("c8-rom", i18n::tr("ROM: program"), &[pin("addr", Byte), pout("word", Instr16)], |def| NativeSolution {
        native: crate::model::NativeKind::Rom,
        addr: nodes_of("addr", Byte),
        din: None,
        we: None,
        clk: None,
        dout: def.iface.ports[1].nodes.clone(),
    }));

    blocks.push(native_block(
        "c8-ram",
        i18n::tr("Disk (data memory)"),
        &[pin("addr", Byte), pin("din", Byte), pin("we", Bit), pin("clk", Clk), pout("dout", Byte)],
        |def| NativeSolution {
            native: crate::model::NativeKind::Ram,
            addr: nodes_of("addr", Byte),
            din: Some(nodes_of("din", Byte)),
            we: Some(s("we")),
            clk: Some(s("clk")),
            dout: def.iface.ports[4].nodes.clone(),
        },
    ));

    /* ===================== Processor ===================== */

    let mut cpu_specs: Vec<PortSpec> = vec![pin("clk", Clk), pout("pc", Byte), pout("halted", Bit)];
    cpu_specs.extend((1..=7).map(|k| pout(format!("r{k}"), Byte)));
    blocks.push(hier_block("c8-cpu", i18n::tr("“Mini-8” processor"), &cpu_specs, |h| {
        // left to right: fetch and decode → registers and operands → ALU, comparison and disk
        let col = |n: usize, y: f64| (150.0 + n as f64 * 196.0, y);
        let put = |h: &mut HierBuilder, id: &str, block: &str, at: (f64, f64)| {
            h.inst_at(id, block, at.0, at.1);
        };
        put(h, "pc", "c8-pc", col(0, 20.0));
        put(h, "rom", "c8-rom", col(0, 230.0));
        put(h, "imm", "c8-immgen", col(0, 330.0));
        put(h, "dec", "c8-decode", col(0, 440.0));
        put(h, "halt", "c8-halt", col(0, 540.0));
        put(h, "en", "c8-gate-en", col(0, 650.0));
        put(h, "rf", "c8-regfile", col(1, 20.0));
        put(h, "p2s", "c8-mux2x3", col(1, 310.0));
        put(h, "opm1", "c8-mux2x8", col(1, 440.0));
        put(h, "opm2", "c8-mux2x8", col(1, 570.0));
        put(h, "wb", "c8-mux2x8", col(1, 700.0));
        put(h, "alu", "c8-alu8", col(2, 20.0));
        put(h, "cmp", "c8-cmp8", col(2, 300.0));
        put(h, "br", "c8-branch", col(2, 410.0));
        put(h, "ram", "c8-ram", col(2, 550.0));

        // fetch: program counter → ROM → instruction split into parts
        h.link("pc.pc", "rom.addr").link("rom.word", "imm.instr").link("rom.word.op", "dec.op");
        h.link("imm.imm6", "pc.imm6").link("imm.imm8", "pc.imm8");

        // registers: where to write (field A), what to read (B) and the second operand (C or A)
        h.link("rom.word.a", "rf.wsel").link("rom.word.b", "rf.rsel1");
        h.link("rom.word.a", "p2s.d0");
        for i in [2, 1, 0] {
            h.link(&format!("rom.word.c.I{i}"), &format!("p2s.d1.R{i}"));
        }
        h.link("dec.ctl.isR", "p2s.s").link("p2s.y", "rf.rsel2");

        // ALU: the first operand is register B, the second is a register or the number from the instruction
        h.link("dec.ctl.useImm6", "opm1.s").link("rf.rd2", "opm1.d0").link("imm.imm6", "opm1.d1");
        h.link("dec.ctl.useImm8", "opm2.s").link("opm1.y", "opm2.d0").link("imm.imm8", "opm2.d1");
        h.link("rf.rd1", "alu.a").link("opm2.y", "alu.b");
        h.link("dec.ctl.sub", "alu.sub").link("dec.ctl.selAdd", "alu.sAdd").link("dec.ctl.selAnd", "alu.sAnd");
        h.link("dec.ctl.selOr", "alu.sOr").link("dec.ctl.selXor", "alu.sXor").link("dec.ctl.selB", "alu.sB");

        // jumps: comparison of two registers and the decision
        h.link("rf.rd2", "cmp.x").link("rf.rd1", "cmp.y");
        h.link("dec.ctl", "br.ctl").link("cmp.eq", "br.eq").link("cmp.lt", "br.lt");
        h.link("br.take", "pc.take").link("dec.ctl.isJmp", "pc.isJmp");

        // disk: the ALU computes the address, register A goes to the write
        h.link("alu.res", "ram.addr").link("rf.rd2", "ram.din");
        h.link("dec.ctl.load", "wb.s").link("alu.res", "wb.d0").link("ram.dout", "wb.d1").link("wb.y", "rf.wdata");

        // enables and halt
        h.link("dec.ctl.isHlt", "halt.isHlt").link("halt.run", "en.run").link("dec.ctl", "en.ctl");
        h.link("en.pcEn", "pc.run").link("en.regWe", "rf.we").link("en.ramWe", "ram.we");
        h.link("$.clk", "pc.clk").link("$.clk", "rf.clk").link("$.clk", "ram.clk").link("$.clk", "halt.clk");

        // what is visible from outside
        h.link("pc.pc", "$.pc").link("halt.halted", "$.halted");
        for k in 1..=7 {
            h.link(&format!("rf.r{k}"), &format!("$.r{k}"));
        }
    }));

    blocks
}

/// All processor blocks: descriptions, contents, order as in the catalog.
pub struct Cpu8Blocks {
    list: Vec<GeneratedBlock>,
    index: HashMap<String, usize>,
}

impl Cpu8Blocks {
    /// Block by id.
    pub fn get(&self, id: &str) -> Option<&GeneratedBlock> {
        self.index.get(id).map(|i| &self.list[*i])
    }

    /// All blocks in catalog order.
    pub fn all(&self) -> &[GeneratedBlock] {
        &self.list
    }

    /// Block library in the form the block board expects (view only).
    pub fn library(&self) -> BlockLibrary {
        let mut lib = BlockLibrary::default();
        for b in &self.list {
            lib.insert(b.def.clone(), Some(b.solution.clone()), String::new());
        }
        lib
    }
}

impl BlockLookup for Cpu8Blocks {
    fn lookup(&self, id: &str) -> Option<BlockEntry> {
        let b = self.get(id)?;
        Some((std::sync::Arc::new(b.def.clone()), std::sync::Arc::new(b.solution.clone())))
    }
}

/// Processor block catalog; built once.
pub fn cpu8_blocks() -> &'static Cpu8Blocks {
    static BLOCKS: OnceLock<Cpu8Blocks> = OnceLock::new();
    BLOCKS.get_or_init(|| {
        let list = build_blocks();
        let index = list.iter().enumerate().map(|(i, b)| (b.def.id.clone(), i)).collect();
        Cpu8Blocks { list, index }
    })
}

/// Block description by id; `None` if there is no such block.
pub fn cpu8_def(id: &str) -> Option<&'static BlockDef> {
    cpu8_blocks().get(id).map(|b| &b.def)
}

#[allow(dead_code)]
fn _types(_: Iface) {}
