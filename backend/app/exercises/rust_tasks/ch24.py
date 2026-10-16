"""Задачи книги «Изучаем Rust»: глава 24 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {24: [{'id': 'r24-opt-map',
       'mode': 'rust',
       'title': 'Option::map',
       'statement': 'Напишите double_opt(x: Option<i32>) -> Option<i32>: удвоить значение внутри, None '
                    'оставить None (без match).',
       'starter': 'fn double_opt(x: Option<i32>) -> Option<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n    println!("{:?} {:?}", double_opt(Some(4)), double_opt(None));\n}\n',
       'hint': 'x.map(|v| v * 2)',
       'expected': ['Some(8) None']},
      {'id': 'r24-opt-and-then',
       'mode': 'rust',
       'title': 'and_then',
       'statement': 'Напишите safe_half(x: Option<i32>) -> Option<i32>: половина числа, если оно чётное, '
                    'иначе None; для None — None. Используйте and_then.',
       'starter': 'fn safe_half(x: Option<i32>) -> Option<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?} {:?} {:?}", safe_half(Some(10)), safe_half(Some(7)), safe_half(None));\n'
                 '}\n',
       'hint': 'and_then принимает функцию, возвращающую Option.',
       'expected': ['Some(5) None None']},
      {'id': 'r24-opt-filter',
       'mode': 'rust',
       'title': 'filter',
       'statement': 'Напишите positive(x: Option<i32>) -> Option<i32>: оставить значение, только если оно > '
                    '0.',
       'starter': 'fn positive(x: Option<i32>) -> Option<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?} {:?} {:?} {:?}", positive(Some(5)), positive(Some(-1)), '
                 'positive(Some(0)), positive(None));\n'
                 '}\n',
       'hint': 'x.filter(|v| *v > 0)',
       'expected': ['Some(5) None None None']},
      {'id': 'r24-opt-or',
       'mode': 'rust',
       'title': 'unwrap_or_else',
       'statement': 'Напишите name_or_default(n: Option<&str>) -> String: имя, либо «аноним#» + длина слова '
                    '«аноним» (так вычисляется лениво) — без match и if.',
       'starter': 'fn name_or_default(n: Option<&str>) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", name_or_default(Some("Аня")));\n'
                 '    println!("{}", name_or_default(None));\n'
                 '}\n',
       'hint': 'map + unwrap_or_else(|| …)',
       'expected': ['Аня', 'аноним#6']},
      {'id': 'r24-opt-ok-or',
       'mode': 'rust',
       'title': 'ok_or',
       'statement': 'Напишите first_or_err(v: &[i32]) -> Result<i32, String>: первый элемент или '
                    'Err("пусто") (first, copied, ok_or).',
       'starter': 'fn first_or_err(v: &[i32]) -> Result<i32, String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n    println!("{:?} {:?}", first_or_err(&[7, 8]), first_or_err(&[]));\n}\n',
       'hint': 'v.first().copied().ok_or(…)',
       'expected': ['Ok(7) Err("пусто")']},
      {'id': 'r24-opt-zip',
       'mode': 'rust',
       'title': 'Option::zip',
       'statement': 'Напишите both(a: Option<i32>, b: Option<i32>) -> Option<(i32, i32)>: пара, если оба '
                    'Some, иначе None (метод zip).',
       'starter': 'fn both(a: Option<i32>, b: Option<i32>) -> Option<(i32, i32)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?} {:?} {:?}", both(Some(1), Some(2)), both(Some(1), None), both(None, '
                 'None));\n'
                 '}\n',
       'hint': 'a.zip(b)',
       'expected': ['Some((1, 2)) None None']},
      {'id': 'r24-opt-take',
       'mode': 'rust',
       'title': 'Option::take',
       'statement': 'Напишите pop_front(slot: &mut Option<String>) -> Option<String>: вынуть значение из '
                    'слота, оставив None (метод take).',
       'starter': 'fn pop_front(slot: &mut Option<String>) -> Option<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut s = Some(String::from("a"));\n'
                 '    println!("{:?}", pop_front(&mut s));\n'
                 '    println!("{:?}", s);\n'
                 '    println!("{:?}", pop_front(&mut s));\n'
                 '}\n',
       'hint': 'take() оставляет None.',
       'expected': ['Some("a")', 'None', 'None']},
      {'id': 'r24-res-map-err',
       'mode': 'rust',
       'title': 'map_err',
       'statement': 'Напишите parse_pos(s: &str) -> Result<u32, String>: разобрать неотрицательное число, '
                    'при ошибке — Err с текстом «плохое число: <s>» (map_err).',
       'starter': 'fn parse_pos(s: &str) -> Result<u32, String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", parse_pos("42"));\n'
                 '    println!("{:?}", parse_pos("-3"));\n'
                 '    println!("{:?}", parse_pos("x"));\n'
                 '}\n',
       'hint': 'map_err превращает тип ошибки.',
       'expected': ['Ok(42)', 'Err("плохое число: -3")', 'Err("плохое число: x")']},
      {'id': 'r24-res-and-then',
       'mode': 'rust',
       'title': 'Result::and_then',
       'statement': 'Напишите parse_and_sqrt(s: &str) -> Result<f64, String>: разобрать f64 (ошибка «не '
                    'число») и взять корень (ошибка «отрицательное» при < 0). Цепочка and_then.',
       'starter': 'fn parse_and_sqrt(s: &str) -> Result<f64, String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", parse_and_sqrt("16"));\n'
                 '    println!("{:?}", parse_and_sqrt("-4"));\n'
                 '    println!("{:?}", parse_and_sqrt("abc"));\n'
                 '}\n',
       'hint': 'map_err, затем and_then.',
       'expected': ['Ok(4.0)', 'Err("отрицательное")', 'Err("не число")']},
      {'id': 'r24-res-ok',
       'mode': 'rust',
       'title': 'Result → Option',
       'statement': 'Напишите numbers(items: &[&str]) -> Vec<i32>: разберите все строки в i32 и оставьте '
                    'только удавшиеся (filter_map с ok()).',
       'starter': 'fn numbers(items: &[&str]) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n    println!("{:?}", numbers(&["1", "x", "3", "", "-5"]));\n}\n',
       'hint': 'filter_map(|s| s.parse().ok())',
       'expected': ['[1, 3, -5]']},
      {'id': 'r24-res-collect',
       'mode': 'rust',
       'title': 'collect в Result',
       'statement': 'Напишите all_numbers(items: &[&str]) -> Result<Vec<i32>, String>: все строки в числа '
                    'или Err(<первая плохая строка>). Подсказка: collect умеет собирать Result<Vec<_>, _>.',
       'starter': 'fn all_numbers(items: &[&str]) -> Result<Vec<i32>, String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", all_numbers(&["1", "2", "3"]));\n'
                 '    println!("{:?}", all_numbers(&["1", "x", "y"]));\n'
                 '    println!("{:?}", all_numbers(&[]));\n'
                 '}\n',
       'hint': 'iter().map(…).collect::<Result<Vec<_>, _>>()',
       'expected': ['Ok([1, 2, 3])', 'Err("x")', 'Ok([])']},
      {'id': 'r24-res-unwrap-default',
       'mode': 'rust',
       'title': 'unwrap_or_default',
       'statement': 'Напишите to_i32(s: &str) -> i32: число из строки или 0 (parse + unwrap_or_default).',
       'starter': 'fn to_i32(s: &str) -> i32 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n    println!("{} {} {}", to_i32("12"), to_i32("x"), to_i32(""));\n}\n',
       'hint': 'unwrap_or_default берёт 0 из типа.',
       'expected': ['12 0 0']},
      {'id': 'r24-mem-swap',
       'mode': 'rust',
       'title': 'mem::swap',
       'statement': 'Напишите swap_values(a: &mut i32, b: &mut i32): поменять значения местами функцией '
                    'std::mem::swap.',
       'starter': 'fn swap_values(a: &mut i32, b: &mut i32) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let (mut x, mut y) = (1, 2);\n'
                 '    swap_values(&mut x, &mut y);\n'
                 '    println!("{} {}", x, y);\n'
                 '}\n',
       'hint': 'std::mem::swap(a, b) принимает две изменяемые ссылки.',
       'expected': ['2 1']},
      {'id': 'r24-vec-swap',
       'mode': 'rust',
       'title': 'Vec::swap',
       'statement': 'Напишите swap_items(v: &mut Vec<i32>, a: usize, b: usize): поменять местами элементы с '
                    'индексами a и b (метод v.swap).',
       'starter': 'fn swap_items(v: &mut Vec<i32>, a: usize, b: usize) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![1, 2, 3, 4];\n'
                 '    swap_items(&mut v, 0, 3);\n'
                 '    println!("{:?}", v);\n'
                 '}\n',
       'hint': 'v.swap(a, b) — безопасный обмен двух элементов.',
       'expected': ['[4, 2, 3, 1]']},
      {'id': 'r24-mem-replace',
       'mode': 'rust',
       'title': 'mem::replace',
       'statement': 'Напишите set_name(name: &mut String, new: &str) -> String: заменить значение и вернуть '
                    'старое (mem::replace).',
       'starter': 'fn set_name(name: &mut String, new: &str) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut n = String::from("Аня");\n'
                 '    let old = set_name(&mut n, "Боря");\n'
                 '    println!("{} {}", old, n);\n'
                 '}\n',
       'hint': 'std::mem::replace(name, new.to_string())',
       'expected': ['Аня Боря']},
      {'id': 'r24-mem-take',
       'mode': 'rust',
       'title': 'mem::take',
       'statement': 'Напишите drain_all(v: &mut Vec<String>) -> Vec<String>: вернуть все элементы и оставить '
                    'вектор пустым (mem::take).',
       'starter': 'fn drain_all(v: &mut Vec<String>) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![String::from("a"), String::from("b")];\n'
                 '    let got = drain_all(&mut v);\n'
                 '    println!("{:?} {:?}", got, v);\n'
                 '}\n',
       'hint': 'std::mem::take(v)',
       'expected': ['["a", "b"] []']},
      {'id': 'r24-cmp-then',
       'mode': 'rust',
       'title': 'Сравнение по нескольким полям',
       'statement': 'Напишите sort_people(v: &mut Vec<(String, u32)>): отсортировать пары (имя, возраст) по '
                    'возрасту по убыванию, при равных — по имени по возрастанию (cmp и then).',
       'starter': 'fn sort_people(v: &mut Vec<(String, u32)>) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![(String::from("Боря"), 30), (String::from("Аня"), 30), '
                 '(String::from("Вера"), 25)];\n'
                 '    sort_people(&mut v);\n'
                 '    println!("{:?}", v);\n'
                 '}\n',
       'hint': 'b.1.cmp(&a.1).then(a.0.cmp(&b.0))',
       'expected': ['[("Аня", 30), ("Боря", 30), ("Вера", 25)]']},
      {'id': 'r24-cmp-reverse',
       'mode': 'rust',
       'title': 'Reverse',
       'statement': 'Напишите top_three(v: &[i32]) -> Vec<i32>: три наибольших по убыванию (sort_by_key с '
                    'Reverse; если элементов меньше трёх — все).',
       'starter': 'fn top_three(v: &[i32]) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", top_three(&[5, 1, 9, 3, 7, 7]));\n'
                 '    println!("{:?}", top_three(&[2]));\n'
                 '}\n',
       'hint': 'sort_by_key(|x| Reverse(*x))',
       'expected': ['[9, 7, 7]', '[2]']},
      {'id': 'r24-cmp-clamp',
       'mode': 'rust',
       'title': 'clamp',
       'statement': 'Напишите normalize(v: &[f64]) -> Vec<f64>: ограничить каждое число диапазоном [0.0, '
                    '1.0] (метод clamp).',
       'starter': 'fn normalize(v: &[f64]) -> Vec<f64> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n    println!("{:?}", normalize(&[-0.5, 0.25, 1.5, 1.0]));\n}\n',
       'hint': 'x.clamp(0.0, 1.0)',
       'expected': ['[0.0, 0.25, 1.0, 1.0]']},
      {'id': 'r24-cmp-total',
       'mode': 'rust',
       'title': 'Сортировка дробных',
       'statement': 'Напишите sort_floats(v: &mut Vec<f64>): по возрастанию, с NaN в конце (метод '
                    'total_cmp).',
       'starter': 'fn sort_floats(v: &mut Vec<f64>) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![3.5, f64::NAN, -1.0, 2.0, 0.0];\n'
                 '    sort_floats(&mut v);\n'
                 '    println!("{:?}", v);\n'
                 '}\n',
       'hint': 'a.total_cmp(b) задаёт полный порядок.',
       'expected': ['[-1.0, 0.0, 2.0, 3.5, NaN]']},
      {'id': 'r24-conv-from',
       'mode': 'rust',
       'title': 'From и Into',
       'statement': 'Структура Rgb(u8, u8, u8) объявлена. Реализуйте From<(u8, u8, u8)> for Rgb и From<u32> '
                    'for Rgb (значение 0xRRGGBB), чтобы работали Rgb::from(…) и .into().',
       'starter': 'struct Rgb(u8, u8, u8);\n'
                  '\n'
                  'impl From<(u8, u8, u8)> for Rgb {\n'
                  '    fn from(t: (u8, u8, u8)) -> Rgb {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl From<u32> for Rgb {\n'
                  '    fn from(x: u32) -> Rgb {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a = Rgb::from((1, 2, 3));\n'
                 '    let b: Rgb = 0xFF8000.into();\n'
                 '    println!("{} {} {}", a.0, a.1, a.2);\n'
                 '    println!("{} {} {}", b.0, b.1, b.2);\n'
                 '}\n',
       'hint': 'Сдвиги >> 16 и >> 8, приведение к u8 отрезает старшие биты.',
       'expected': ['1 2 3', '255 128 0']},
      {'id': 'r24-conv-fromstr',
       'mode': 'rust',
       'title': 'FromStr',
       'statement': 'Реализуйте FromStr для Point { x: i32, y: i32 }: разбор строки вида «3,-4» '
                    '(Err(String), если не два числа через запятую). Тогда работает "3,-4".parse::<Point>().',
       'starter': 'use std::str::FromStr;\n'
                  '\n'
                  '#[derive(Debug, PartialEq)]\n'
                  'struct Point {\n'
                  '    x: i32,\n'
                  '    y: i32,\n'
                  '}\n'
                  '\n'
                  'impl FromStr for Point {\n'
                  '    type Err = String;\n'
                  '    fn from_str(s: &str) -> Result<Point, String> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", "3,-4".parse::<Point>());\n'
                 '    println!("{:?}", " 1 , 2 ".parse::<Point>());\n'
                 '    println!("{:?}", "1;2".parse::<Point>());\n'
                 '    println!("{:?}", "a,2".parse::<Point>());\n'
                 '}\n',
       'hint': "split_once(',') и parse; ? для ошибок.",
       'expected': ['Ok(Point { x: 3, y: -4 })',
                    'Ok(Point { x: 1, y: 2 })',
                    'Err("нет запятой")',
                    'Err("плохой x")']},
      {'id': 'r24-conv-asref',
       'mode': 'rust',
       'title': 'AsRef<str>',
       'statement': 'Напишите shout(s: impl AsRef<str>) -> String: строка в верхнем регистре с «!» на конце. '
                    'Функция должна принимать и &str, и String.',
       'starter': 'fn shout(s: impl AsRef<str>) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", shout("привет"));\n'
                 '    println!("{}", shout(String::from("rust")));\n'
                 '}\n',
       'hint': 's.as_ref() — получить &str из любой формы.',
       'expected': ['ПРИВЕТ!', 'RUST!']},
      {'id': 'r24-conv-tryfrom',
       'mode': 'rust',
       'title': 'TryFrom',
       'statement': 'Напишите to_byte(n: i32) -> Option<u8>: n как u8, если помещается (0..=255), иначе '
                    'None. Используйте u8::try_from(n).ok().',
       'starter': 'fn to_byte(n: i32) -> Option<u8> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?} {:?} {:?} {:?}", to_byte(200), to_byte(256), to_byte(-1), to_byte(0));\n'
                 '}\n',
       'hint': 'try_from возвращает Result; ok() превращает в Option.',
       'expected': ['Some(200) None None Some(0)']},
      {'id': 'r24-iter-successors',
       'mode': 'rust',
       'title': 'successors',
       'statement': 'Напишите powers_of_two(limit: u64) -> Vec<u64>: степени двойки 1, 2, 4, … не больше '
                    'limit (iter::successors + take_while).',
       'starter': 'fn powers_of_two(limit: u64) -> Vec<u64> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", powers_of_two(100));\n'
                 '    println!("{:?}", powers_of_two(0));\n'
                 '    println!("{}", powers_of_two(u64::MAX).len());\n'
                 '}\n',
       'hint': 'successors(Some(1), |&x| x.checked_mul(2)) — останавливается при переполнении.',
       'expected': ['[1, 2, 4, 8, 16, 32, 64]', '[]', '64']},
      {'id': 'r24-iter-from-fn',
       'mode': 'rust',
       'title': 'from_fn',
       'statement': 'Напишите collatz(n: u64) -> Vec<u64>: последовательность Коллатца из n до 1 '
                    'включительно (iter::from_fn с состоянием в замыкании).',
       'starter': 'fn collatz(n: u64) -> Vec<u64> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", collatz(6));\n'
                 '    println!("{:?}", collatz(1));\n'
                 '    println!("{}", collatz(27).len());\n'
                 '}\n',
       'hint': 'Состояние хранится в Option<u64> внутри замыкания.',
       'expected': ['[6, 3, 10, 5, 16, 8, 4, 2, 1]', '[1]', '112']},
      {'id': 'r24-iter-chain-zip',
       'mode': 'rust',
       'title': 'chain и zip',
       'statement': 'Напишите interleave(a: &[i32], b: &[i32]) -> Vec<i32>: чередование элементов a и b (a0, '
                    'b0, a1, b1, …), хвост более длинного добавляется в конец.',
       'starter': 'fn interleave(a: &[i32], b: &[i32]) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", interleave(&[1, 2, 3], &[10, 20]));\n'
                 '    println!("{:?}", interleave(&[], &[5]));\n'
                 '    println!("{:?}", interleave(&[1], &[2]));\n'
                 '}\n',
       'hint': 'min длин, цикл по общей части и хвост.',
       'expected': ['[1, 10, 2, 20, 3]', '[5]', '[1, 2]']},
      {'id': 'r24-iter-cycle',
       'mode': 'rust',
       'title': 'cycle',
       'statement': 'Напишите repeat_to(v: &[i32], n: usize) -> Vec<i32>: первые n элементов бесконечного '
                    'повторения v (cycle + take); для пустого v — пустой вектор.',
       'starter': 'fn repeat_to(v: &[i32], n: usize) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", repeat_to(&[1, 2, 3], 7));\n'
                 '    println!("{:?}", repeat_to(&[], 4));\n'
                 '}\n',
       'hint': 'cycle() на пустом срезе даёт пустой итератор.',
       'expected': ['[1, 2, 3, 1, 2, 3, 1]', '[]']},
      {'id': 'r24-iter-fold',
       'mode': 'rust',
       'title': 'fold',
       'statement': 'Напишите digits_to_num(d: &[u8]) -> u64: число из цифр (d = [1, 2, 3] → 123) через '
                    'fold.',
       'starter': 'fn digits_to_num(d: &[u8]) -> u64 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", digits_to_num(&[1, 2, 3]));\n'
                 '    println!("{}", digits_to_num(&[]));\n'
                 '    println!("{}", digits_to_num(&[9, 9, 9, 9, 9, 9, 9, 9, 9, 9]));\n'
                 '}\n',
       'hint': 'acc * 10 + цифра.',
       'expected': ['123', '0', '9999999999']},
      {'id': 'r24-iter-minmax',
       'mode': 'rust',
       'title': 'min_by_key и max_by',
       'statement': 'Напишите shortest_longest(words: &[&str]) -> Option<(String, String)>: самое короткое и '
                    'самое длинное слова (по числу символов; при равенстве — первое для короткого и '
                    'последнее для длинного, как делают min_by_key и max_by_key). Для пустого — None.',
       'starter': 'fn shortest_longest(words: &[&str]) -> Option<(String, String)> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", shortest_longest(&["aa", "b", "cc", "ddd", "eee"]));\n'
                 '    println!("{:?}", shortest_longest(&[]));\n'
                 '}\n',
       'hint': 'min_by_key и max_by_key.',
       'expected': ['Some(("b", "eee"))', 'None']}]}
