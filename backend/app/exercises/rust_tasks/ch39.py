"""Задачи книги «Изучаем Rust»: глава 39 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {39: [{'id': 'r39-bit-tricks',
       'mode': 'rust',
       'title': 'Битовые трюки',
       'statement': 'Напишите без готовых методов count_ones, is_power_of_two и reverse_bits: '
                    'lowest_set_bit(n: u32) -> u32 (само младшее «горящее» значение, 0 для 0), is_pow2(n: '
                    'u64) -> bool (0 — нет), parity(n: u32) -> bool (число единичных битов нечётно) и '
                    'reverse8(n: u8) -> u8 (биты в обратном порядке).',
       'starter': 'fn lowest_set_bit(n: u32) -> u32 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn is_pow2(n: u64) -> bool {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn parity(n: u32) -> bool {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn reverse8(n: u8) -> u8 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{} {} {} {}", lowest_set_bit(0), lowest_set_bit(12), '
                 'lowest_set_bit(0x8000_0000), lowest_set_bit(7));\n'
                 '    println!("{} {} {} {}", is_pow2(0), is_pow2(1), is_pow2(1 << 40), is_pow2(96));\n'
                 '    println!("{} {} {} {}", parity(0), parity(1), parity(3), parity(0b1011_0000));\n'
                 '    println!("{:08b} {:08b} {:08b}", reverse8(0b0000_0001), reverse8(0b1011_0000), '
                 'reverse8(0xFF));\n'
                 '}\n',
       'expected': ['0 4 2147483648 1',
                    'false true true false',
                    'false true false true',
                    '10000000 00001101 11111111'],
       'hint': 'n & n.wrapping_neg() выделяет младшую единицу; n & (n - 1) сбрасывает её.'},
      {'id': 'r39-header',
       'mode': 'rust',
       'title': 'Разбор двоичного заголовка',
       'statement': 'Формат заголовка (8 байт): магическое число 0xCAFE (u16, старший байт первым), версия '
                    '(u8), длина данных (u32, младший байт первым), флаги (u8). Напишите parse_header(b: '
                    '&[u8]) -> Option<(u8, u32, u8)> (версия, длина, флаги; None — если байтов меньше 8 или '
                    'магия не совпала) и build_header(version: u8, len: u32, flags: u8) -> [u8; 8].',
       'starter': 'fn parse_header(b: &[u8]) -> Option<(u8, u32, u8)> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn build_header(version: u8, len: u32, flags: u8) -> [u8; 8] {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let h = build_header(2, 0x0001_0203, 0b101);\n'
                 '    println!("{:02x?}", h);\n'
                 '    println!("{:?}", parse_header(&h));\n'
                 '    println!("{:?} {:?}", parse_header(&h[..7]), parse_header(&[0xCA, 0xFF, 1, 0, 0, 0, 0, '
                 '0]));\n'
                 '    let mut longer = h.to_vec();\n'
                 '    longer.extend_from_slice(&[9, 9, 9]);\n'
                 '    println!("{:?}", parse_header(&longer));\n'
                 '}\n',
       'expected': ['[ca, fe, 02, 03, 02, 01, 00, 05]',
                    'Some((2, 66051, 5))',
                    'None None',
                    'Some((2, 66051, 5))'],
       'hint': 'u16::from_be_bytes([b[0], b[1]]), u32::from_le_bytes([...4 байта...]); массив байтов '
               'собирайте из to_be_bytes / to_le_bytes.'},
      {'id': 'r39-varint',
       'mode': 'rust',
       'title': 'Varint с проверкой ошибок',
       'statement': 'Напишите varint_encode(n: u64) -> Vec<u8> и varint_decode(b: &[u8]) -> Result<(u64, '
                    "usize), &'static str>: число и сколько байтов прочитано. Ошибки: пустой вход или "
                    'оборвавшаяся запись (все байты с признаком продолжения) → "truncated"; запись длиннее '
                    '10 байтов или не помещающаяся в u64 → "overflow".',
       'starter': 'fn varint_encode(n: u64) -> Vec<u8> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  "fn varint_decode(b: &[u8]) -> Result<(u64, usize), &'static str> {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    for n in [0u64, 1, 127, 128, 300, 16384, u32::MAX as u64, u64::MAX] {\n'
                 '        let e = varint_encode(n);\n'
                 '        println!("{} {} {:?}", n, e.len(), varint_decode(&e) == Ok((n, e.len())));\n'
                 '    }\n'
                 '    println!("{:?} {:?}", varint_decode(&[]), varint_decode(&[0x80, 0x80]));\n'
                 '    println!("{:?}", varint_decode(&[0xff; 11]));\n'
                 '    println!("{:?}", varint_decode(&[0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, '
                 '0x02]));\n'
                 '    println!("{:?}", varint_decode(&[0xac, 0x02, 0xff]));\n'
                 '}\n',
       'expected': ['0 1 true',
                    '1 1 true',
                    '127 1 true',
                    '128 2 true',
                    '300 2 true',
                    '16384 3 true',
                    '4294967295 5 true',
                    '18446744073709551615 10 true',
                    'Err("truncated") Err("truncated")',
                    'Err("overflow")',
                    'Err("overflow")',
                    'Ok((300, 2))'],
       'hint': 'Каждый байт даёт 7 бит со сдвигом 7·i; десятый байт может нести только один значащий бит.'},
      {'id': 'r39-crc32',
       'mode': 'rust',
       'title': 'CRC-32 по таблице',
       'statement': 'Напишите crc32(data: &[u8]) -> u32 (многочлен 0xEDB88320 в отражённом виде, начальное '
                    'значение 0xFFFFFFFF, итог инвертируется) — как zlib.crc32 в питоне. Проверка подаёт 8 '
                    'МБ данных.',
       'starter': 'fn crc32(data: &[u8]) -> u32 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:08x} {:08x} {:08x}", crc32(b""), crc32(b"hello"), crc32(b"123456789"));\n'
                 '    let big: Vec<u8> = (0..8_000_000u32).map(|i| (i % 251) as u8).collect();\n'
                 '    println!("{:08x}", crc32(&big));\n'
                 '}\n',
       'expected': ['00000000 3610a686 cbf43926', '37ac4d4a'],
       'hint': 'Таблицу из 256 значений считайте один раз перед циклом по данным.'},
      {'id': 'r39-base64',
       'mode': 'rust',
       'title': 'Base64',
       'statement': "Напишите base64_encode(data: &[u8]) -> String (алфавит A–Z a–z 0–9 + /, добивка '=') и "
                    'base64_decode(s: &str) -> Option<Vec<u8>> (None при недопустимом символе или неверной '
                    'длине).',
       'starter': 'fn base64_encode(data: &[u8]) -> String {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn base64_decode(s: &str) -> Option<Vec<u8>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    for s in ["", "f", "fo", "foo", "foob", "fooba", "foobar", "Привет"] {\n'
                 '        let e = base64_encode(s.as_bytes());\n'
                 '        let d = base64_decode(&e).unwrap();\n'
                 '        println!("{:?} {} {}", s, e, d == s.as_bytes());\n'
                 '    }\n'
                 '    println!("{:?} {:?} {:?}", base64_decode("Zm9v!"), base64_decode("Zm9"), '
                 'base64_decode("Zg=A"));\n'
                 '    println!("{}", base64_encode(&[0xff, 0xfe, 0xfd]));\n'
                 '}\n',
       'expected': ['""  true',
                    '"f" Zg== true',
                    '"fo" Zm8= true',
                    '"foo" Zm9v true',
                    '"foob" Zm9vYg== true',
                    '"fooba" Zm9vYmE= true',
                    '"foobar" Zm9vYmFy true',
                    '"Привет" 0J/RgNC40LLQtdGC true',
                    'None None None',
                    '//79'],
       'hint': 'Три байта = 24 бита = четыре шестибитных индекса в алфавите; недостающие байты — нули, а в '
               "выводе знаки '='."},
      {'id': 'r39-bitset',
       'mode': 'rust',
       'title': 'Битовое множество и решето',
       'statement': 'Дополните BitSet: new(len), set(i), clear(i), get(i), count() -> u32, ones() -> '
                    'Vec<usize> (номера единиц по возрастанию), union_with(&mut self, other: &BitSet). Затем '
                    'напишите primes_below(n: usize) -> Vec<usize> — решето Эратосфена на BitSet (проверка: '
                    'n = 20 миллионов).',
       'starter': 'struct BitSet {\n'
                  '    words: Vec<u64>,\n'
                  '    len: usize,\n'
                  '}\n'
                  '\n'
                  'impl BitSet {\n'
                  '    fn new(len: usize) -> BitSet {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn set(&mut self, i: usize) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn clear(&mut self, i: usize) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn get(&self, i: usize) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn count(&self) -> u32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn ones(&self) -> Vec<usize> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn union_with(&mut self, other: &BitSet) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn primes_below(n: usize) -> Vec<usize> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut a = BitSet::new(130);\n'
                 '    for i in [0, 5, 64, 129] {\n'
                 '        a.set(i);\n'
                 '    }\n'
                 '    let mut b = BitSet::new(130);\n'
                 '    b.set(5);\n'
                 '    b.set(100);\n'
                 '    a.union_with(&b);\n'
                 '    a.clear(0);\n'
                 '    println!("{:?} {} {} {}", a.ones(), a.count(), a.get(100), a.get(0));\n'
                 '    println!("{:?} {}", primes_below(30), primes_below(2).len());\n'
                 '    let p = primes_below(20_000_000);\n'
                 '    println!("{} {:?}", p.len(), p.last());\n'
                 '}\n',
       'expected': ['[5, 64, 100, 129] 4 true false',
                    '[2, 3, 5, 7, 11, 13, 17, 19, 23, 29] 0',
                    '1270607 Some(19999999)'],
       'hint': 'trailing_zeros() + w &= w - 1 перебирают единичные биты слова; решето: пометьте кратные i, '
               'начиная с i·i.'},
      {'id': 'r39-cpu',
       'mode': 'rust',
       'title': 'Эмулятор процессора',
       'statement': 'Реализуйте run(prog: &[Instr], limit: u32) -> Result<Cpu, Trap>. Процессор: регистры '
                    'regs: [u8; 4], память mem: [u8; 16], pc, zero, steps. Команды: Ldi(r, v), Mov(a, b), '
                    'Add(a, b), Sub(a, b) (оборачивающие, обновляют флаг zero по результату), Ld(r, addr), '
                    'St(r, addr), Jmp(t), Jz(t), Jnz(t), Hlt (останавливает; тоже считается шагом). Ловушки: '
                    'адрес памяти ≥ 16 → Trap::BadAddress(addr), pc ≥ длины программы без Hlt → '
                    'Trap::PcOutOfRange(pc), больше limit шагов → Trap::Timeout. Каждое выполнение команды '
                    'увеличивает steps.',
       'starter': '#[derive(Debug, Clone, Copy)]\n'
                  'enum Instr {\n'
                  '    Ldi(usize, u8),\n'
                  '    Mov(usize, usize),\n'
                  '    Add(usize, usize),\n'
                  '    Sub(usize, usize),\n'
                  '    Ld(usize, usize),\n'
                  '    St(usize, usize),\n'
                  '    Jmp(usize),\n'
                  '    Jz(usize),\n'
                  '    Jnz(usize),\n'
                  '    Hlt,\n'
                  '}\n'
                  '\n'
                  '#[derive(Debug, PartialEq)]\n'
                  'enum Trap {\n'
                  '    BadAddress(usize),\n'
                  '    PcOutOfRange(usize),\n'
                  '    Timeout,\n'
                  '}\n'
                  '\n'
                  '#[derive(Debug)]\n'
                  'struct Cpu {\n'
                  '    regs: [u8; 4],\n'
                  '    mem: [u8; 16],\n'
                  '    pc: usize,\n'
                  '    zero: bool,\n'
                  '    steps: u32,\n'
                  '}\n'
                  '\n'
                  'fn run(prog: &[Instr], limit: u32) -> Result<Cpu, Trap> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    use Instr::*;\n'
                 '    let sum = [Ldi(0, 0), Ldi(1, 5), Ldi(2, 1), Add(0, 1), Sub(1, 2), Jnz(3), Hlt];\n'
                 '    let c = run(&sum, 1000).unwrap();\n'
                 '    println!("{:?} {} {}", c.regs, c.steps, c.zero);\n'
                 '    let mem = [Ldi(0, 42), St(0, 3), Ldi(0, 0), Ld(1, 3), Hlt];\n'
                 '    let c = run(&mem, 100).unwrap();\n'
                 '    println!("{:?} {:?}", c.regs, &c.mem[..5]);\n'
                 '    println!("{:?}", run(&[Ldi(0, 1), St(0, 16)], 100).err());\n'
                 '    println!("{:?}", run(&[Ldi(0, 1)], 100).err());\n'
                 '    println!("{:?}", run(&[Jmp(0)], 50).err());\n'
                 '    println!("{:?}", run(&[Ldi(0, 250), Ldi(1, 10), Add(0, 1), Hlt], 10).map(|c| '
                 '(c.regs[0], c.zero)));\n'
                 '    println!("{:?}", run(&[Jmp(7)], 10).err());\n'
                 '}\n',
       'expected': ['[15, 0, 1, 0] 19 true',
                    '[0, 42, 0, 0] [0, 0, 0, 42, 0]',
                    'Some(BadAddress(16))',
                    'Some(PcOutOfRange(1))',
                    'Some(Timeout)',
                    'Ok((4, false))',
                    'Some(PcOutOfRange(7))'],
       'hint': 'Проверяйте pc перед чтением команды; ?-оператор вместе с ok_or превращает выход за массив в '
               'Trap.'},
      {'id': 'r39-encode-instr',
       'mode': 'rust',
       'title': 'Машинный код команд',
       'statement': 'Кодируйте команды в два байта: байт 0 = код операции << 4 | a << 2 | b, байт 1 = число '
                    'или адрес (0, если нет). Коды: Hlt 0, Ldi 1, Mov 2, Add 3, Sub 4, Ld 5, St 6, Jmp 7, Jz '
                    '8, Jnz 9. Для Ldi(r, v): a = r, байт 1 = v; для Mov/Add/Sub(a, b): a, b; для Ld(r, '
                    'addr) и St(r, addr): a = r, байт 1 = addr (адрес ≤ 255); для переходов: байт 1 = цель. '
                    'Напишите encode(i: &Instr) -> [u8; 2] и decode(b: [u8; 2]) -> Option<Instr> (None для '
                    'неизвестного кода операции).',
       'starter': '#[derive(Debug, Clone, Copy, PartialEq)]\n'
                  'enum Instr {\n'
                  '    Ldi(usize, u8),\n'
                  '    Mov(usize, usize),\n'
                  '    Add(usize, usize),\n'
                  '    Sub(usize, usize),\n'
                  '    Ld(usize, usize),\n'
                  '    St(usize, usize),\n'
                  '    Jmp(usize),\n'
                  '    Jz(usize),\n'
                  '    Jnz(usize),\n'
                  '    Hlt,\n'
                  '}\n'
                  '\n'
                  'fn encode(i: &Instr) -> [u8; 2] {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn decode(b: [u8; 2]) -> Option<Instr> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    use Instr::*;\n'
                 '    let prog = [Ldi(1, 5), Add(0, 1), Sub(1, 2), Jnz(3), Ld(2, 200), St(3, 17), Mov(3, 0), '
                 'Jz(9), Jmp(0), Hlt];\n'
                 '    for i in &prog {\n'
                 '        let e = encode(i);\n'
                 '        println!("{:02x} {:02x} {}", e[0], e[1], decode(e) == Some(*i));\n'
                 '    }\n'
                 '    println!("{:?} {:?}", decode([0xA0, 0]), decode([0xF3, 9]));\n'
                 '}\n',
       'expected': ['14 05 true',
                    '31 00 true',
                    '46 00 true',
                    '90 03 true',
                    '58 c8 true',
                    '6c 11 true',
                    '2c 00 true',
                    '80 09 true',
                    '70 00 true',
                    '00 00 true',
                    'None None'],
       'hint': 'Поля байта 0 собираются сдвигами: op << 4 | a << 2 | b; разбор — обратными сдвигами и маской '
               '3.'},
      {'id': 'r39-cache',
       'mode': 'rust',
       'title': 'Симулятор кэша',
       'statement': 'Напишите cache_sim(trace: &[u64], lines: usize, line_size: u64) -> (u64, u64): кэш с '
                    'прямым отображением (как в курсе по архитектуре): блок = адрес / line_size, строка = '
                    'блок % lines, тег = блок / lines; верните (попадания, промахи). Проверка: 5 миллионов '
                    'обращений.',
       'starter': 'fn cache_sim(trace: &[u64], lines: usize, line_size: u64) -> (u64, u64) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'struct Lcg(u64);\n'
                 'impl Lcg {\n'
                 '    fn next(&mut self) -> u64 {\n'
                 '        self.0 = '
                 'self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);\n'
                 '        self.0 >> 33\n'
                 '    }\n'
                 '}\n'
                 'fn main() {\n'
                 '    println!("{:?}", cache_sim(&[0, 4, 8, 16, 0, 64, 0], 4, 16));\n'
                 '    println!("{:?} {:?}", cache_sim(&[], 4, 16), cache_sim(&[0, 0, 0], 4, 16));\n'
                 '    let seq: Vec<u64> = (0..1_000_000u64).map(|i| i * 4).collect();\n'
                 '    println!("{:?}", cache_sim(&seq, 64, 64));\n'
                 '    let mut rng = Lcg(1);\n'
                 '    let rnd: Vec<u64> = (0..5_000_000).map(|_| rng.next() % 100_000).collect();\n'
                 '    let (h, m) = cache_sim(&rnd, 1024, 64);\n'
                 '    println!("{}", h + m);\n'
                 '}\n',
       'expected': ['(3, 4)', '(0, 0) (2, 1)', '(937500, 62500)', '5000000'],
       'hint': 'Таблица тегов Vec<Option<u64>>; сравнивайте tags[idx] с Some(tag).'},
      {'id': 'r39-alu-flags',
       'mode': 'rust',
       'title': 'АЛУ с флагами',
       'statement': 'Напишите alu(op: &str, a: u8, b: u8) -> (u8, bool, bool, bool, bool): op — "ADD" или '
                    '"SUB"; результат и флаги (zero, negative, carry, overflow). carry — перенос при '
                    'сложении или заём (a < b) при вычитании; overflow — знаковое переполнение (операнды как '
                    'числа в дополнительном коде).',
       'starter': 'fn alu(op: &str, a: u8, b: u8) -> (u8, bool, bool, bool, bool) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for (op, a, b) in [("ADD", 100, 100), ("ADD", 255, 1), ("ADD", 127, 1), ("ADD", 128, '
                 '128), ("SUB", 5, 7), ("SUB", 128, 1), ("SUB", 0, 0), ("SUB", 127, 255)] {\n'
                 '        println!("{} {} {} {:?}", op, a, b, alu(op, a, b));\n'
                 '    }\n'
                 '}\n',
       'expected': ['ADD 100 100 (200, false, true, false, true)',
                    'ADD 255 1 (0, true, false, true, false)',
                    'ADD 127 1 (128, false, true, false, true)',
                    'ADD 128 128 (0, true, false, true, true)',
                    'SUB 5 7 (254, false, true, true, false)',
                    'SUB 128 1 (127, false, false, false, true)',
                    'SUB 0 0 (0, true, false, false, false)',
                    'SUB 127 255 (128, false, true, true, true)'],
       'hint': 'overflowing_add/sub возвращают (результат, признак); для знакового переполнения выполните ту '
               'же операцию над i8.'}]}
