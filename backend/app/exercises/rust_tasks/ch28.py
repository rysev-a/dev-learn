"""Задачи книги «Изучаем Rust»: глава 28 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {28: [{'id': 'r28-duration-hms',
       'mode': 'rust',
       'title': 'Часы, минуты, секунды',
       'statement': 'Напишите hms(d: Duration) -> String: формат «ЧЧ:ММ:СС» (часы могут быть больше 24; доли '
                    'секунды отбросить).',
       'starter': 'use std::time::Duration;\n\nfn hms(d: Duration) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", hms(Duration::from_secs(3725)));\n'
                 '    println!("{}", hms(Duration::from_millis(59999)));\n'
                 '    println!("{}", hms(Duration::from_secs(100 * 3600 + 5)));\n'
                 '}\n',
       'hint': 'as_secs() даёт целые секунды.',
       'expected': ['01:02:05', '00:00:59', '100:00:05']},
      {'id': 'r28-duration-parse',
       'mode': 'rust',
       'title': 'Разбор «1h30m15s»',
       'statement': 'Напишите parse_duration(s: &str) -> Option<Duration>: суммарная длительность из '
                    'последовательности «<число><единица>» с единицами h, m, s; недопустимая строка или '
                    'пустая — None.',
       'starter': 'use std::time::Duration;\n'
                  '\n'
                  'fn parse_duration(s: &str) -> Option<Duration> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", parse_duration("1h30m15s"));\n'
                 '    println!("{:?}", parse_duration("90s"));\n'
                 '    println!("{:?}", parse_duration("5"));\n'
                 '    println!("{:?}", parse_duration("2x"));\n'
                 '    println!("{:?}", parse_duration(""));\n'
                 '}\n',
       'hint': 'Накапливайте цифры; при букве — умножьте на единицу.',
       'expected': ['Some(5415s)', 'Some(90s)', 'None', 'None', 'None']},
      {'id': 'r28-duration-arith',
       'mode': 'rust',
       'title': 'Арифметика длительностей',
       'statement': 'Напишите total(parts: &[Duration]) -> Duration (сумма) и average(parts: &[Duration]) -> '
                    'Option<Duration> (среднее; для пустого — None).',
       'starter': 'use std::time::Duration;\n'
                  '\n'
                  'fn average(parts: &[Duration]) -> Option<Duration> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn total(parts: &[Duration]) -> Duration {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let v = [Duration::from_millis(500), Duration::from_secs(2), '
                 'Duration::from_millis(1500)];\n'
                 '    println!("{:?}", total(&v));\n'
                 '    println!("{:?}", total(&[]));\n'
                 '    println!("{:?}", average(&v));\n'
                 '    println!("{:?}", average(&[]));\n'
                 '}\n',
       'hint': 'Duration реализует Sum; деление Duration / u32.',
       'expected': ['4s', '0ns', 'Some(1.333333333s)', 'None']},
      {'id': 'r28-duration-checked',
       'mode': 'rust',
       'title': 'Безопасное вычитание',
       'statement': 'Напишите remaining(deadline: Duration, spent: Duration) -> Duration: сколько осталось '
                    '(ноль, если время вышло) — saturating_sub.',
       'starter': 'use std::time::Duration;\n'
                  '\n'
                  'fn remaining(deadline: Duration, spent: Duration) -> Duration {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", remaining(Duration::from_secs(10), Duration::from_secs(3)));\n'
                 '    println!("{:?}", remaining(Duration::from_secs(3), Duration::from_secs(10)));\n'
                 '}\n',
       'hint': 'saturating_sub не паникует.',
       'expected': ['7s', '0ns']},
      {'id': 'r28-epoch-days',
       'mode': 'rust',
       'title': 'Секунды с 1970 года в дату',
       'statement': 'Напишите civil_from_secs(secs: u64) -> (u32, u32, u32): год, месяц и день (UTC) по '
                    'секундам с 1 января 1970 года. Алгоритм «civil from days»: z = дни + 719468; era = z / '
                    '146097; doe = z − era·146097; yoe = (doe − doe/1460 + doe/36524 − doe/146096) / 365; y '
                    '= yoe + era·400; doy = doe − (365·yoe + yoe/4 − yoe/100); mp = (5·doy + 2) / 153; d = '
                    'doy − (153·mp + 2)/5 + 1; m = mp + 3 при mp < 10, иначе mp − 9; y + 1, если m ≤ 2.',
       'starter': 'fn civil_from_secs(secs: u64) -> (u32, u32, u32) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", civil_from_secs(0));\n'
                 '    println!("{:?}", civil_from_secs(86399));\n'
                 '    println!("{:?}", civil_from_secs(951782400));\n'
                 '    println!("{:?}", civil_from_secs(1709164800));\n'
                 '    println!("{:?}", civil_from_secs(4102444800));\n'
                 '}\n',
       'hint': 'Целочисленная арифметика с i64; деление отсекает к нулю — для положительных чисел это то, '
               'что нужно.',
       'expected': ['(1970, 1, 1)', '(1970, 1, 1)', '(2000, 2, 29)', '(2024, 2, 29)', '(2100, 1, 1)']},
      {'id': 'r28-instant-measure',
       'mode': 'rust',
       'title': 'Измерение',
       'statement': 'Напишите time_it<F: FnOnce() -> u64>(f: F) -> (u64, Duration): вызовите f ровно один '
                    'раз и верните её результат вместе с измеренной через Instant длительностью.',
       'starter': 'use std::time::Duration;\n'
                  '\n'
                  'fn time_it<F: FnOnce() -> u64>(f: F) -> (u64, Duration) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let (r, d) = time_it(|| (1..=1000u64).sum());\n'
                 '    println!("{} {}", r, d < Duration::from_secs(5));\n'
                 '    let (_, d2) = time_it(|| { std::thread::sleep(Duration::from_millis(30)); 0 });\n'
                 '    println!("{}", d2 >= Duration::from_millis(30));\n'
                 '}\n',
       'hint': 'Instant::now(), вызов, elapsed().',
       'expected': ['500500 true', 'true']},
      {'id': 'r28-checked-ops',
       'mode': 'rust',
       'title': 'Безопасные операции',
       'statement': 'Напишите safe_sum(v: &[i32]) -> Option<i32>: сумма с проверкой переполнения (None, если '
                    'не поместилась).',
       'starter': 'fn safe_sum(v: &[i32]) -> Option<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", safe_sum(&[1, 2, 3]));\n'
                 '    println!("{:?}", safe_sum(&[i32::MAX, 1]));\n'
                 '    println!("{:?}", safe_sum(&[]));\n'
                 '    println!("{:?}", safe_sum(&[i32::MIN, -1]));\n'
                 '}\n',
       'hint': 'try_fold с checked_add.',
       'expected': ['Some(6)', 'None', 'Some(0)', 'None']},
      {'id': 'r28-pow-mod',
       'mode': 'rust',
       'title': 'Степень по модулю',
       'statement': 'Напишите pow_mod(base: u64, exp: u64, m: u64) -> u64: base^exp mod m (m ≥ 1) быстрым '
                    'возведением; промежуточные произведения в u128.',
       'starter': 'fn pow_mod(base: u64, exp: u64, m: u64) -> u64 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", pow_mod(2, 10, 1000));\n'
                 '    println!("{}", pow_mod(3, 200, 13));\n'
                 '    println!("{}", pow_mod(7, 0, 5));\n'
                 '    println!("{}", pow_mod(2, 1_000_000_007, 998_244_353));\n'
                 '    println!("{}", pow_mod(10, 18, 1_000_000_000_000_000_000));\n'
                 '}\n',
       'hint': 'Возведение по битам показателя; u128 вмещает произведение двух u64.',
       'expected': ['24', '9', '1', '132727571', '0']},
      {'id': 'r28-bits-count',
       'mode': 'rust',
       'title': 'Биты',
       'statement': 'Напишите bit_stats(x: u32) -> (u32, u32, u32): число единиц, ведущих нулей и замыкающих '
                    'нулей (x ≠ 0 — штатно; для 0 методы вернут 32).',
       'starter': 'fn bit_stats(x: u32) -> (u32, u32, u32) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", bit_stats(0b1011000));\n'
                 '    println!("{:?}", bit_stats(1));\n'
                 '    println!("{:?}", bit_stats(u32::MAX));\n'
                 '    println!("{:?}", bit_stats(0));\n'
                 '}\n',
       'hint': 'Три метода целого.',
       'expected': ['(3, 25, 3)', '(1, 31, 0)', '(32, 0, 0)', '(0, 32, 32)']},
      {'id': 'r28-is-pow2',
       'mode': 'rust',
       'title': 'Степень двойки',
       'statement': 'Напишите round_up_pow2(n: u32) -> u32: наименьшая степень двойки не меньше n (для 0 — '
                    '1). Используйте метод next_power_of_two.',
       'starter': 'fn round_up_pow2(n: u32) -> u32 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for n in [0, 1, 2, 3, 17, 64, 65, 1 << 30] {\n'
                 '        print!("{} ", round_up_pow2(n));\n'
                 '    }\n'
                 '    println!();\n'
                 '}\n',
       'hint': 'u32::next_power_of_two.',
       'expected': ['1 1 2 4 32 64 128 1073741824']},
      {'id': 'r28-gray',
       'mode': 'rust',
       'title': 'Код Грея',
       'statement': 'Напишите gray(n: u32) -> u32: n ^ (n >> 1) и ungray(g: u32) -> u32 — обратное '
                    'преобразование (ungray(gray(n)) == n).',
       'starter': 'fn gray(n: u32) -> u32 {\n    todo!()\n}\n\nfn ungray(g: u32) -> u32 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for n in 0..8 {\n'
                 '        print!("{:03b} ", gray(n));\n'
                 '    }\n'
                 '    println!();\n'
                 '    println!("{}", (0..10000).all(|n| ungray(gray(n)) == n));\n'
                 '}\n',
       'hint': 'Обратное: xor всех сдвигов вправо.',
       'expected': ['000 001 011 010 110 111 101 100', 'true']},
      {'id': 'r28-rotate-bytes',
       'mode': 'rust',
       'title': 'Порядок байтов',
       'statement': 'Напишите swap_endian(x: u32) -> u32 без swap_bytes — через to_le_bytes и from_be_bytes.',
       'starter': 'fn swap_endian(x: u32) -> u32 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:#x}", swap_endian(0x12345678));\n'
                 '    println!("{}", swap_endian(swap_endian(77)) == 77);\n'
                 '}\n',
       'hint': 'Байты записываем в одном порядке, читаем в другом.',
       'expected': ['0x78563412', 'true']},
      {'id': 'r28-isqrt',
       'mode': 'rust',
       'title': 'Целый корень',
       'statement': 'Напишите isqrt(n: u64) -> u64: наибольшее r с r·r ≤ n (бинарный поиск или метод isqrt, '
                    'если он доступен). Проверка на больших значениях, включая u64::MAX.',
       'starter': 'fn isqrt(n: u64) -> u64 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for n in [0u64, 1, 2, 3, 4, 15, 16, 17, 1_000_000_000_000, u64::MAX] {\n'
                 '        print!("{} ", isqrt(n));\n'
                 '    }\n'
                 '    println!();\n'
                 '}\n',
       'hint': 'Бинарный поиск по r; умножение — в u128.',
       'expected': ['0 1 1 1 2 3 4 4 1000000 4294967295']},
      {'id': 'r28-float-round',
       'mode': 'rust',
       'title': 'Округление до знаков',
       'statement': 'Напишите round_to(x: f64, digits: u32) -> f64: округлить до digits знаков после запятой '
                    '(round, умножение и деление на 10^digits).',
       'starter': 'fn round_to(x: f64, digits: u32) -> f64 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", round_to(3.14159, 2));\n'
                 '    println!("{}", round_to(2.5, 0));\n'
                 '    println!("{}", round_to(-1.005, 1));\n'
                 '    println!("{}", round_to(1234.5678, 0));\n'
                 '}\n',
       'hint': '10f64.powi(digits as i32)',
       'expected': ['3.14', '3', '-1', '1235']},
      {'id': 'r28-float-compare',
       'mode': 'rust',
       'title': 'Сравнение с допуском',
       'statement': 'Напишите approx_eq(a: f64, b: f64, rel: f64) -> bool: |a − b| ≤ rel · max(|a|, |b|, '
                    '1.0).',
       'starter': 'fn approx_eq(a: f64, b: f64, rel: f64) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", approx_eq(0.1 + 0.2, 0.3, 1e-9));\n'
                 '    println!("{}", approx_eq(1e10, 1e10 + 1.0, 1e-9));\n'
                 '    println!("{}", approx_eq(1.0, 1.1, 1e-3));\n'
                 '    println!("{}", approx_eq(f64::NAN, f64::NAN, 1e-3));\n'
                 '}\n',
       'hint': 'NaN не равен ничему: сравнение даёт false.',
       'expected': ['true', 'true', 'false', 'false']},
      {'id': 'r28-mean-std',
       'mode': 'rust',
       'title': 'Среднее и отклонение',
       'statement': 'Напишите stats(v: &[f64]) -> Option<(f64, f64)>: среднее и стандартное отклонение (по '
                    'формуле для всей совокупности, делим на n); для пустого — None.',
       'starter': 'fn stats(v: &[f64]) -> Option<(f64, f64)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", stats(&[2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]));\n'
                 '    println!("{:?}", stats(&[]));\n'
                 '    println!("{:?}", stats(&[3.0]));\n'
                 '}\n',
       'hint': 'Две суммы: значений и квадратов отклонений.',
       'expected': ['Some((5.0, 2.0))', 'None', 'Some((3.0, 0.0))']},
      {'id': 'r28-hypot-dist',
       'mode': 'rust',
       'title': 'Расстояния',
       'statement': 'Напишите path_len(points: &[(f64, f64)]) -> f64: длина ломаной через все точки по '
                    'порядку (hypot).',
       'starter': 'fn path_len(points: &[(f64, f64)]) -> f64 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", path_len(&[(0.0, 0.0), (3.0, 4.0), (3.0, 10.0)]));\n'
                 '    println!("{}", path_len(&[(1.0, 1.0)]) == 0.0);\n'
                 '}\n',
       'hint': 'windows(2) и hypot.',
       'expected': ['11', 'true']},
      {'id': 'r28-nan-sort',
       'mode': 'rust',
       'title': 'Сортировка с NaN',
       'statement': 'Напишите sorted_floats(v: &[f64]) -> Vec<f64>: копия по возрастанию с NaN в конце '
                    '(total_cmp).',
       'starter': 'fn sorted_floats(v: &[f64]) -> Vec<f64> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", sorted_floats(&[2.5, f64::NAN, -1.0, f64::INFINITY, 0.0]));\n'
                 '}\n',
       'hint': 'total_cmp задаёт полный порядок.',
       'expected': ['[-1.0, 0.0, 2.5, inf, NaN]']},
      {'id': 'r28-nonzero',
       'mode': 'rust',
       'title': 'NonZero',
       'statement': 'Напишите to_nonzero(v: &[u32]) -> Vec<Option<std::num::NonZeroU32>>: каждое число как '
                    'NonZeroU32 (None для нуля).',
       'starter': 'fn to_nonzero(v: &[u32]) -> Vec<Option<std::num::NonZeroU32>> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let r = to_nonzero(&[3, 0, 7]);\n'
                 '    println!("{:?}", r);\n'
                 '    println!("{}", std::mem::size_of::<Option<std::num::NonZeroU32>>() == '
                 'std::mem::size_of::<u32>());\n'
                 '}\n',
       'hint': 'NonZeroU32::new(x) возвращает Option.',
       'expected': ['[Some(3), None, Some(7)]', 'true']},
      {'id': 'r28-wrapping-hash',
       'mode': 'rust',
       'title': 'Хеш с оборотом',
       'statement': 'Напишите fnv1a(data: &[u8]) -> u32: хеш FNV-1a: h = 2166136261; для каждого байта h ^= '
                    'байт; h = h * 16777619 (с оборотом — wrapping_mul).',
       'starter': 'fn fnv1a(data: &[u8]) -> u32 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:#010x}", fnv1a(b""));\n'
                 '    println!("{:#010x}", fnv1a(b"a"));\n'
                 '    println!("{:#010x}", fnv1a(b"foobar"));\n'
                 '}\n',
       'hint': 'wrapping_mul не паникует при переполнении.',
       'expected': ['0x811c9dc5', '0xe40c292c', '0xbf9cf968']},
      {'id': 'r28-lcg',
       'mode': 'rust',
       'title': 'Свой генератор',
       'statement': 'Реализуйте struct Lcg { state: u64 } с функцией new(seed: u64) и методом next(&mut '
                    'self) -> u64: state = state · 6364136223846793005 + 1442695040888963407 (с оборотом); '
                    'результат — state >> 33. Одинаковое зерно даёт одинаковую последовательность.',
       'starter': 'struct Lcg {\n'
                  '    state: u64,\n'
                  '}\n'
                  '\n'
                  'impl Lcg {\n'
                  '    fn new(seed: u64) -> Lcg {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn next(&mut self) -> u64 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut a = Lcg::new(42);\n'
                 '    let mut b = Lcg::new(42);\n'
                 '    let va: Vec<u64> = (0..3).map(|_| a.next()).collect();\n'
                 '    let vb: Vec<u64> = (0..3).map(|_| b.next()).collect();\n'
                 '    println!("{:?}", va);\n'
                 '    println!("{}", va == vb);\n'
                 '    let mut c = Lcg::new(7);\n'
                 '    let mut sum = 0u64;\n'
                 '    for _ in 0..1000 {\n'
                 '        sum += c.next() % 10;\n'
                 '    }\n'
                 '    println!("{}", sum);\n'
                 '}\n',
       'hint': 'Используйте wrapping_mul и wrapping_add.',
       'expected': ['[1220265334, 484179026, 886563538]', 'true', '4369']},
      {'id': 'r28-shuffle',
       'mode': 'rust',
       'title': 'Перемешивание',
       'statement': 'Напишите shuffle(v: &mut [i32], seed: u64): перемешайте на месте алгоритмом Фишера — '
                    'Йетса с генератором xorshift: x ^= x << 13; x ^= x >> 7; x ^= x << 17 (u64, зерно — '
                    'состояние; зерно 0 заменить на 1); для i от len−1 до 1 меняйте v[i] и v[x % (i + 1)].',
       'starter': 'fn shuffle(v: &mut [i32], seed: u64) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v: Vec<i32> = (1..=10).collect();\n'
                 '    shuffle(&mut v, 12345);\n'
                 '    println!("{:?}", v);\n'
                 '    let mut s = v.clone();\n'
                 '    s.sort();\n'
                 '    println!("{:?}", s);\n'
                 '    let mut w: Vec<i32> = (1..=10).collect();\n'
                 '    shuffle(&mut w, 12345);\n'
                 '    println!("{}", v == w);\n'
                 '}\n',
       'hint': 'Замыкание next() хранит состояние x.',
       'expected': ['[1, 4, 9, 6, 5, 3, 8, 2, 7, 10]', '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]', 'true']},
      {'id': 'r28-size-table',
       'mode': 'rust',
       'title': 'Размеры в байтах',
       'statement': 'Напишите sizes() -> Vec<(String, usize)>: пары (название, size_of) для типов: u8, u64, '
                    'char, &u8, &[u8], String, Option<u32>, Option<&u8>, (u8, u32), [u16; 5], Box<u8>, '
                    'Option<Box<u8>>.',
       'starter': 'fn sizes() -> Vec<(String, usize)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n    for (n, s) in sizes() {\n        println!("{} {}", n, s);\n    }\n}\n',
       'hint': 'size_of::<T>() для каждого типа.',
       'expected': ['u8 1',
                    'u64 8',
                    'char 4',
                    '&u8 8',
                    '&[u8] 16',
                    'String 24',
                    'Option<u32> 8',
                    'Option<&u8> 8',
                    '(u8, u32) 8',
                    '[u16; 5] 10',
                    'Box<u8> 8',
                    'Option<Box<u8>> 8']},
      {'id': 'r28-struct-packing',
       'mode': 'rust',
       'title': 'Порядок полей',
       'statement': 'Напишите packing() -> (usize, usize, usize): размеры трёх структур: A { a: u8, b: u32, '
                    'c: u8 } без repr, A_C — та же с #[repr(C)], B { b: u32, a: u8, c: u8 } с #[repr(C)]. '
                    'Структуры объявите внутри функции или рядом.',
       'starter': 'fn packing() -> (usize, usize, usize) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n    println!("{:?}", packing());\n}\n',
       'hint': 'Структуры нужно объявить перед функцией.',
       'expected': ['(8, 12, 8)']},
      {'id': 'r28-discriminant',
       'mode': 'rust',
       'title': 'Тот же вариант',
       'statement': 'Объявлен enum Shape { Circle(f64), Rect(f64, f64), Dot }. Напишите same_kind(a: &Shape, '
                    'b: &Shape) -> bool: true, если у значений один вариант (mem::discriminant).',
       'starter': 'enum Shape {\n'
                  '    Circle(f64),\n'
                  '    Rect(f64, f64),\n'
                  '    Dot,\n'
                  '}\n'
                  '\n'
                  'fn same_kind(a: &Shape, b: &Shape) -> bool {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", same_kind(&Shape::Circle(1.0), &Shape::Circle(9.0)));\n'
                 '    println!("{}", same_kind(&Shape::Circle(1.0), &Shape::Rect(1.0, 2.0)));\n'
                 '    println!("{}", same_kind(&Shape::Dot, &Shape::Dot));\n'
                 '}\n',
       'hint': 'discriminant сравнивается через ==.',
       'expected': ['true', 'false', 'true']},
      {'id': 'r28-float-bits',
       'mode': 'rust',
       'title': 'Биты числа с плавающей точкой',
       'statement': 'Напишите float_parts(x: f32) -> (u32, u32, u32): знак (0/1), смещённая экспонента (8 '
                    'бит) и мантисса (23 бита) через to_bits.',
       'starter': 'fn float_parts(x: f32) -> (u32, u32, u32) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", float_parts(1.0));\n'
                 '    println!("{:?}", float_parts(-2.5));\n'
                 '    println!("{:?}", float_parts(0.0));\n'
                 '    println!("{:?}", float_parts(f32::INFINITY));\n'
                 '}\n',
       'hint': 'x.to_bits() — u32 с теми же битами.',
       'expected': ['(0, 127, 0)', '(1, 128, 2097152)', '(0, 0, 0)', '(0, 255, 0)']},
      {'id': 'r28-mem-take-state',
       'mode': 'rust',
       'title': 'Автомат и mem::replace',
       'statement': 'Объявлен enum State { Idle, Running(u32), Done(String) }. Напишите finish(s: &mut '
                    'State) -> Option<u32>: если Running(n) — заменить на Done(«готово за n»), вернуть '
                    'Some(n); иначе ничего не менять и вернуть None. Используйте mem::replace.',
       'starter': 'enum State {\n'
                  '    Idle,\n'
                  '    Running(u32),\n'
                  '    Done(String),\n'
                  '}\n'
                  '\n'
                  'fn finish(s: &mut State) -> Option<u32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut a = State::Running(5);\n'
                 '    println!("{:?}", finish(&mut a));\n'
                 '    if let State::Done(t) = &a { println!("{}", t); }\n'
                 '    let mut b = State::Idle;\n'
                 '    println!("{:?}", finish(&mut b));\n'
                 '    println!("{}", matches!(b, State::Idle));\n'
                 '}\n',
       'hint': 'Заберите значение через replace, затем запишите нужное состояние.',
       'expected': ['Some(5)', 'готово за 5', 'None', 'true']},
      {'id': 'r28-leap-days',
       'mode': 'rust',
       'title': 'Дни между датами',
       'statement': 'Напишите days_between(y1: i64, m1: u32, d1: u32, y2: i64, m2: u32, d2: u32) -> i64: '
                    'сколько дней от первой даты до второй по григорианскому календарю (отрицательное, если '
                    'вторая раньше). Подсказка: переведите каждую дату в «номер дня» алгоритмом '
                    'days_from_civil.',
       'starter': 'fn days_between(y1: i64, m1: u32, d1: u32, y2: i64, m2: u32, d2: u32) -> i64 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", days_between(2024, 1, 1, 2024, 12, 31));\n'
                 '    println!("{}", days_between(2000, 2, 28, 2000, 3, 1));\n'
                 '    println!("{}", days_between(1970, 1, 1, 2026, 10, 16));\n'
                 '    println!("{}", days_between(2026, 10, 16, 2026, 10, 1));\n'
                 '}\n',
       'hint': 'days_from_civil: сдвиг года для января и февраля, 400-летние эры.',
       'expected': ['365', '2', '20742', '-15']},
      {'id': 'r28-timeout-loop',
       'mode': 'rust',
       'title': 'Ждать с таймаутом',
       'statement': 'Напишите spin_for(limit: Duration) -> bool: в цикле проверяйте Instant::elapsed(), пока '
                    'не пройдёт limit; верните true, если реально прошло не меньше limit (всегда true).',
       'starter': 'use std::time::Duration;\n\nfn spin_for(limit: Duration) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", spin_for(Duration::from_millis(20)));\n'
                 '    println!("{}", spin_for(Duration::ZERO));\n'
                 '}\n',
       'hint': 'while t.elapsed() < limit {}',
       'expected': ['true', 'true']},
      {'id': 'r28-system-time',
       'mode': 'rust',
       'title': 'Секунды с 1970 года',
       'statement': 'Напишите unix_now() -> u64: число секунд с начала 1970 года '
                    '(SystemTime::now().duration_since(UNIX_EPOCH)); результат при проверке должен быть '
                    'больше 1.7 миллиарда.',
       'starter': 'fn unix_now() -> u64 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let t = unix_now();\n'
                 '    println!("{}", t > 1_700_000_000);\n'
                 '    println!("{}", t < 4_000_000_000);\n'
                 '}\n',
       'hint': 'duration_since возвращает Result — unwrap.',
       'expected': ['true', 'true']}]}
