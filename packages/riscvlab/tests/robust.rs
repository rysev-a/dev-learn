//! Устойчивость: мусор на входе не роняет ассемблер и машину (в том числе в отладочной сборке с проверкой переполнений).

use riscvlab::task::{verify, Check, Profile, Test};
use riscvlab::{assemble, Machine, Options, TaskSpec};

#[test]
fn extreme_numbers_do_not_panic() {
    let src = "
  li a0, 0xffffffffffffffffffff
  li a0, 99999999999999999999
  la a0, 0x7fffffffffffffff
  la a0, -0x7fffffffffffffff
  call 0x7fffffffffffffff
  lui a0, %hi(0x7fffffffffffffff)
  addi a0, a0, %lo(0x7fffffffffffffff)
  j 0x7fffffffffffffff
  beq a0, a0, -0x7fffffffffffffff
  .data
  .word 0xffffffffffffffffffff, -0xffffffffffffffffffff, 1-0xffffffffffffffffffff
  .space 99999999999999999999
  .space 0xffffffffffff
  .align 99
  .align 31
  .balign 9223372036854775807
  .balign 0x7fffffffffffffff
  .byte 0xffffffffffffffffffff
";
    let r = assemble(src);
    assert!(!r.errors.is_empty());
}

#[test]
fn weird_text_does_not_panic() {
    // псевдослучайные строки из «неудобных» символов
    let alphabet: Vec<char> = "ab01 \t\r\n,:()%'\"\\+-#;/.$_xX😀ЖжЁё\u{0}\u{a0}\u{2028}\u{feff}é".chars().collect();
    let mut seed: u64 = 0x9e37_79b9_7f4a_7c15;
    let mut next = || {
        seed ^= seed << 13;
        seed ^= seed >> 7;
        seed ^= seed << 17;
        seed
    };
    for _ in 0..4000 {
        let len = (next() % 60) as usize;
        let s: String = (0..len).map(|_| alphabet[(next() % alphabet.len() as u64) as usize]).collect();
        let r = assemble(&s);
        // что бы ни собралось, машина обязана это пережить
        let mut m = Machine::new(&r.image, Options { switches: 3, entry: r.entry });
        m.run(500);
        let _ = m.view();
    }
    // токены ассемблера вперемешку
    let toks = [
        "add", "lw", "li", "la", "%hi(", "%lo(", ".word", ".asciz", "\"", "'", "a0", "(", ")", ",", ":", "x", "1", "-",
        "+", "lab", "\n", " ", ".equ", ".space", "jalr", "beqz", "call",
    ];
    for _ in 0..4000 {
        let n = 1 + (next() % 24) as usize;
        let s: String = (0..n)
            .map(|_| toks[(next() % toks.len() as u64) as usize])
            .collect::<Vec<_>>()
            .join(if next() & 1 == 0 { " " } else { "" });
        let _ = assemble(&s);
    }
}

#[test]
fn verify_never_panics_on_junk_programs() {
    let spec = TaskSpec {
        profile: Profile::Board,
        starter: String::new(),
        reference: String::new(),
        data: String::new(),
        max_steps: 2000,
        tests: vec![Test { switches: 0, regs: vec![], check: Check::Uart { expected: "x".into(), ok: "ok".into() } }],
    };
    for p in [
        "",
        "\0",
        "li a0, 0x",
        "lw a0, 0(a0",
        "ebreak",
        ".data\n.word 0\n",
        "l: j l",
        "\u{feff}\u{feff}",
        &"a:".repeat(1000),
    ] {
        let v = verify(&spec, p);
        assert!(!v.ok, "{p:?}");
    }
}
