import { makeSlide } from "../SlideFrame.tsx";
import { Cmd, RsCode } from "../widgets.tsx";
// Слайды для «Изучаем Rust», глава 39 — «Биты, байты и эмулятор процессора».
// Тот же дизайн-код, что и в главах 1–5: палитра, IBM Plex Mono / Inter,
// рубрика + номер, «ГЛАВНОЕ» внизу. Один абзац урока = один слайд.

const Slide = makeSlide("ИЗУЧАЕМ RUST / ПРИМЕНЯЕМ: АРХИТЕКТУРА / ГЛАВА 39", 13);

// --- сцены ---------------------------------------------------------------

function S01() {
  return (
    <Slide
      n={1}
      title={"Rust близко к железу"}
      sub={"Глава 39 · Применяем: архитектура"}
      main={"Фиксированные типы, явные приведения и битовые методы делают низкоуровневый код безопасным."}
    >
      <div className="s-grid2">
        {([["as · wrapping", "Целые", "Ширина и знак"], ["to_be_bytes", "Байты", "Порядок явный"], ["size_of · repr(C)", "Память", "Размер и выравнивание"], ["enum Instr", "Эмулятор", "Матч покрывает все команды"]] as const).map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

function S02() {
  return (
    <Slide
      n={2}
      title={"Целые типы и приведения"}
      sub={"as — всегда явно"}
      main={"Знак переинтерпретирует биты, сужение отбрасывает старшие, дробное насыщается."}
    >
      <RsCode>{`fn main() {
    let a: u8 = 200;
    let b = a as i8;
    let c = -1i32 as u32;
    let d = 300i32 as u8;
    let e = -1.9f64 as i32;
    let f = 1e20f64 as i32;
    println!("{} {} {} {} {}", b, c, d, e, f);
    println!("{} {}", u8::MAX, i8::MIN);
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"-56 4294967295 44 -1 2147483647\n255 -128"}</Cmd>
    </Slide>
  );
}

function S03() {
  return (
    <Slide
      n={3}
      title={"Битовые методы"}
      sub={"count_ones, rotate, swap_bytes"}
      main={"Методы целых компилируются в одну команду процессора — вручную циклами их писать не нужно."}
    >
      <RsCode>{`fn main() {
    let x: u32 = 0b1011_0000;
    println!("{} {} {}", x.count_ones(), x.leading_zeros(), x.trailing_zeros());
    println!("{:#x} {:#x}", x.rotate_left(28), x.swap_bytes());
    let mask = 0b0000_1111u32;
    println!("{:08b} {:08b} {:08b}", x & mask, x | mask, x ^ mask);
    println!("{}", (x >> 4) & 1);
    println!("{}", x & x.wrapping_neg());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3 24 4\n0xb 0xb0000000\n00000000 10111111 10111111\n1\n16"}</Cmd>
    </Slide>
  );
}

function S04() {
  return (
    <Slide
      n={4}
      title={"Порядок байтов"}
      sub={"to_be_bytes, from_le_bytes"}
      main={"Порядок указывают в имени метода: разбор двоичных форматов превращается в работу с массивами."}
    >
      <RsCode>{`fn main() {
    let n: u32 = 0x1234_5678;
    println!("{:02x?} {:02x?}", n.to_be_bytes(), n.to_le_bytes());
    println!("{:#x}", u32::from_le_bytes([0x78, 0x56, 0x34, 0x12]));
    println!("{}", u16::from_be_bytes([1, 2]));
    println!("{}", cfg!(target_endian = "little"));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[12, 34, 56, 78] [78, 56, 34, 12]\n0x12345678\n258\ntrue"}</Cmd>
    </Slide>
  );
}

function S05() {
  return (
    <Slide
      n={5}
      title={"Размер и выравнивание"}
      sub={"size_of, align_of, repr(C)"}
      main={"Rust переставляет поля ради размера; repr(C) фиксирует порядок как в C; Option<Box<T>> — без накладных расходов."}
    >
      <RsCode>{`use std::mem::{align_of, size_of};

struct A {
    a: u8,
    b: u32,
    c: u8,
}
#[repr(C)]
struct B {
    a: u8,
    b: u32,
    c: u8,
}
struct C {
    a: u8,
    c: u8,
    b: u32,
}

fn main() {
    println!("{} {}", size_of::<A>(), align_of::<A>());
    println!("{} {}", size_of::<B>(), align_of::<B>());
    println!("{}", size_of::<C>());
    println!("{} {} {}", size_of::<Option<Box<i32>>>(), size_of::<Option<u32>>(), size_of::<char>());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"8 4\n12 4\n8\n8 8 4"}</Cmd>
    </Slide>
  );
}

function S06() {
  return (
    <Slide
      n={6}
      title={"Дробные числа изнутри"}
      sub={"to_bits и from_bits"}
      main={"to_bits безопасно показывает IEEE 754; NaN не равно даже себе."}
    >
      <RsCode>{`fn main() {
    let x = 1.0f32;
    println!("{:#010x}", x.to_bits());
    println!("{:#010x}", (-2.5f32).to_bits());
    println!("{}", f32::from_bits(0x40490fdb));
    println!("{}", 0.1f32 + 0.2f32 == 0.3f32);
    println!("{} {}", f64::NAN == f64::NAN, f64::NAN.is_nan());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0x3f800000\n0xc0200000\n3.1415927\ntrue\nfalse true"}</Cmd>
    </Slide>
  );
}

function S07() {
  return (
    <Slide
      n={7}
      title={"Числа переменной длины"}
      sub={"varint (LEB128)"}
      main={"Семь бит данных в байте, старший бит — «есть продолжение»: малые числа занимают один байт."}
    >
      <RsCode>{`fn varint_encode(mut n: u64) -> Vec<u8> {
    let mut out = Vec::new();
    loop {
        let byte = (n & 0x7f) as u8;
        n >>= 7;
        if n == 0 {
            out.push(byte);
            break;
        }
        out.push(byte | 0x80);
    }
    out
}

fn varint_decode(bytes: &[u8]) -> (u64, usize) {
    let (mut n, mut shift) = (0u64, 0);
    for (i, &b) in bytes.iter().enumerate() {
        n |= ((b & 0x7f) as u64) << shift;
        if b & 0x80 == 0 {
            return (n, i + 1);
        }
        shift += 7;
    }
    (n, bytes.len())
}

fn main() {
    for n in [0u64, 127, 128, 300, 16384] {
        let e = varint_encode(n);
        println!("{} {:?} {:?}", n, e, varint_decode(&e));
    }
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"0 [0] (0, 1)\n127 [127] (127, 1)\n128 [128, 1] (128, 2)\n300 [172, 2] (300, 2)\n16384 [128, 128, 1] (16384, 3)"}</Cmd>
    </Slide>
  );
}

function S08() {
  return (
    <Slide
      n={8}
      title={"CRC32 по таблице"}
      sub={"Контрольная сумма"}
      main={"Таблица из 256 значений — один шаг на байт; результат совпадает с zlib.crc32 из Python."}
    >
      <RsCode>{`fn crc32(data: &[u8]) -> u32 {
    let mut table = [0u32; 256];
    for i in 0..256u32 {
        let mut c = i;
        for _ in 0..8 {
            c = if c & 1 != 0 { 0xEDB88320 ^ (c >> 1) } else { c >> 1 };
        }
        table[i as usize] = c;
    }
    let mut crc = !0u32;
    for &b in data {
        crc = table[((crc ^ b as u32) & 0xff) as usize] ^ (crc >> 8);
    }
    !crc
}

fn main() {
    println!("{:08x} {:08x}", crc32(b"hello"), crc32(b"123456789"));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"3610a686 cbf43926"}</Cmd>
    </Slide>
  );
}

function S09() {
  return (
    <Slide
      n={9}
      title={"Битовое множество"}
      sub={"Vec<u64> вместо Vec<bool>"}
      main={"Номер слова — i / 64, бит внутри — i % 64; подсчёт — count_ones."}
    >
      <RsCode>{`struct BitSet {
    words: Vec<u64>,
}

impl BitSet {
    fn new(len: usize) -> BitSet {
        BitSet { words: vec![0; (len + 63) / 64] }
    }
    fn set(&mut self, i: usize) {
        self.words[i / 64] |= 1 << (i % 64);
    }
    fn get(&self, i: usize) -> bool {
        self.words[i / 64] >> (i % 64) & 1 == 1
    }
    fn count(&self) -> u32 {
        self.words.iter().map(|w| w.count_ones()).sum()
    }
}

fn main() {
    let mut s = BitSet::new(200);
    for i in (0..200).step_by(3) {
        s.set(i);
    }
    println!("{} {} {} {}", s.get(3), s.get(4), s.count(), s.words.len());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"true false 67 4"}</Cmd>
    </Slide>
  );
}

function S10() {
  return (
    <Slide
      n={10}
      title={"Эмулятор: устройство"}
      sub={"Регистры, счётчик, команды-перечисление"}
      main={"Набор команд — enum: матч не даст забыть обработать новую команду."}
    >
      <RsCode>{`#[derive(Debug, Clone, Copy)]
enum Instr {
    Ldi(usize, u8),
    Add(usize, usize),
    Sub(usize, usize),
    Jnz(usize),
    Hlt,
}

struct Cpu {
    regs: [u8; 4],
    pc: usize,
    zero: bool,
    steps: u32,
}

impl Cpu {
    fn new() -> Cpu {
        Cpu { regs: [0; 4], pc: 0, zero: false, steps: 0 }
    }
}

fn main() {
    let c = Cpu::new();
    println!("{:?} {} {} {}", c.regs, c.pc, c.zero, c.steps);
    println!("{:?}", Instr::Ldi(1, 5));
    println!("{}", std::mem::size_of::<Instr>());
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[0, 0, 0, 0] 0 false 0\nLdi(1, 5)\n24"}</Cmd>
    </Slide>
  );
}

function S11() {
  return (
    <Slide
      n={11}
      title={"Эмулятор: исполнение"}
      sub={"Цикл выборки и матч"}
      main={"Арифметика оборачивающая, как в железе; сумма 1..5 даёт 15 за 19 шагов — как на питоне."}
    >
      <RsCode>{`#[derive(Debug, Clone, Copy)]
enum Instr {
    Ldi(usize, u8),
    Add(usize, usize),
    Sub(usize, usize),
    Jnz(usize),
    Hlt,
}

struct Cpu {
    regs: [u8; 4],
    pc: usize,
    zero: bool,
    steps: u32,
}

fn run(prog: &[Instr]) -> Cpu {
    let mut cpu = Cpu { regs: [0; 4], pc: 0, zero: false, steps: 0 };
    while cpu.pc < prog.len() {
        let ins = prog[cpu.pc];
        cpu.pc += 1;
        cpu.steps += 1;
        match ins {
            Instr::Ldi(r, v) => cpu.regs[r] = v,
            Instr::Add(a, b) => {
                cpu.regs[a] = cpu.regs[a].wrapping_add(cpu.regs[b]);
                cpu.zero = cpu.regs[a] == 0;
            }
            Instr::Sub(a, b) => {
                cpu.regs[a] = cpu.regs[a].wrapping_sub(cpu.regs[b]);
                cpu.zero = cpu.regs[a] == 0;
            }
            Instr::Jnz(t) => {
                if !cpu.zero {
                    cpu.pc = t;
                }
            }
            Instr::Hlt => break,
        }
    }
    cpu
}

fn main() {
    use Instr::*;
    let prog = [Ldi(0, 0), Ldi(1, 5), Ldi(2, 1), Add(0, 1), Sub(1, 2), Jnz(3), Hlt];
    let cpu = run(&prog);
    println!("{:?} {}", cpu.regs, cpu.steps);
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"[15, 0, 1, 0] 19"}</Cmd>
    </Slide>
  );
}

function S12() {
  return (
    <Slide
      n={12}
      title={"Память и ловушки"}
      sub={"Result вместо паники"}
      main={"Выход за границы и переполнение стека — значения перечисления Trap, а не падение программы."}
    >
      <RsCode>{`#[derive(Debug)]
enum Trap {
    OutOfBounds(usize),
    StackOverflow,
}

struct Memory {
    bytes: Vec<u8>,
}

impl Memory {
    fn read(&self, addr: usize) -> Result<u8, Trap> {
        self.bytes.get(addr).copied().ok_or(Trap::OutOfBounds(addr))
    }
    fn write(&mut self, addr: usize, v: u8) -> Result<(), Trap> {
        *self.bytes.get_mut(addr).ok_or(Trap::OutOfBounds(addr))? = v;
        Ok(())
    }
}

struct Stack {
    sp: usize,
    mem: Memory,
}

impl Stack {
    fn push(&mut self, v: u8) -> Result<(), Trap> {
        if self.sp == 0 {
            return Err(Trap::StackOverflow);
        }
        self.sp -= 1;
        self.mem.write(self.sp, v)
    }
}

fn main() {
    let mut st = Stack { sp: 4, mem: Memory { bytes: vec![0; 4] } };
    for v in 1..=5 {
        println!("{:?}", st.push(v));
    }
    println!("{:?} {:?}", st.mem.read(3), st.mem.read(9));
}`}</RsCode>
      <div className="s-label">НА ЭКРАНЕ</div>
      <Cmd>{"Ok(())\nOk(())\nOk(())\nOk(())\nErr(StackOverflow)\nOk(1) Err(OutOfBounds(9))"}</Cmd>
    </Slide>
  );
}

function S13() {
  return (
    <Slide
      n={13}
      title={"Итоги главы"}
      sub={"Что мы узнали"}
      main={"Rust выражает машинные понятия типами: ширина, порядок байтов, ловушки — всё видно в коде."}
    >
      <div className="s-grid2">
        {([["u8 … u128", "Целые", "as, wrapping, checked"], ["be · le", "Байты", "Порядок в имени метода"], ["varint · CRC", "Кодирование", "Сдвиги и маски"], ["Result<_, Trap>", "Эмулятор", "Ошибки как данные"]] as const).map(([big, t, d]) => (
          <div className="s-topic" key={t}>
            <span className="s-topic-big">{big}</span>
            <span className="s-divider" />
            <span className="s-node-title">{t}</span>
            <span className="s-node-sub">{d}</span>
          </div>
        ))}
      </div>
    </Slide>
  );
}

// Реестр: «book:chapter» → список слайдов, по одному на абзац урока.
export const SLIDES_R39 = {
  "10:39": [
    S01,
    S02,
    S03,
    S04,
    S05,
    S06,
    S07,
    S08,
    S09,
    S10,
    S11,
    S12,
    S13,
  ],
};

// Короткие названия для списка слайдов в фулскрине (порядок = SLIDES_R39).
export const SLIDE_TITLES_R39 = {
  "10:39": [
    "Биты и байты",
    "Приведения",
    "Битовые методы",
    "Порядок байтов",
    "Размер и выравнивание",
    "Дробные числа",
    "Varint",
    "CRC32",
    "Битовое множество",
    "Устройство эмулятора",
    "Исполнение",
    "Память и ловушки",
    "Итоги",
  ],
};
