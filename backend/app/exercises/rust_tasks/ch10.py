"""Задачи книги «Изучаем Rust»: глава 10 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {10: [{'id': 'r10-args-sum',
       'mode': 'rust',
       'title': 'Python *args → срез',
       'statement': 'Python: def total(*args): return sum(args). Напишите total(v: &[i64]) -> i64, которая '
                    'принимает любое количество чисел через срез.',
       'starter': 'fn total(v: &[i64]) -> i64 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", total(&[1, 2, 3]));\n'
                 '    println!("{}", total(&[]));\n'
                 '    println!("{}", total(&vec![10, -4]));\n'
                 '}\n',
       'hint': 'v.iter().sum() — сумма элементов.',
       'expected': ['6', '0', '6']},
      {'id': 'r10-default-arg',
       'mode': 'rust',
       'title': 'Значение по умолчанию',
       'statement': 'Python: def hi(name="мир"): return f"Привет, {name}!". Напишите hi(name: Option<&str>) '
                    '-> String, подставляя «мир» при None.',
       'starter': 'fn hi(name: Option<&str>) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n    println!("{}", hi(None));\n    println!("{}", hi(Some("Аня")));\n}\n',
       'hint': 'unwrap_or("мир") подставит значение по умолчанию.',
       'expected': ['Привет, мир!', 'Привет, Аня!']},
      {'id': 'r10-floor-divmod',
       'mode': 'rust',
       'title': 'divmod как в Python',
       'statement': 'Python: divmod(-7, 2) == (-4, 1). Напишите py_divmod(a: i32, b: i32) -> (i32, i32) с '
                    'питоновскими частным (округление вниз) и остатком (знак делителя), b ≠ 0.',
       'starter': 'fn py_divmod(a: i32, b: i32) -> (i32, i32) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", py_divmod(7, 2));\n'
                 '    println!("{:?}", py_divmod(-7, 2));\n'
                 '    println!("{:?}", py_divmod(7, -2));\n'
                 '    println!("{:?}", py_divmod(-7, -2));\n'
                 '    println!("{:?}", py_divmod(6, 3));\n'
                 '}\n',
       'hint': 'Если остаток не нуль и его знак не совпадает со знаком делителя — сдвиньте частное вниз.',
       'expected': ['(3, 1)', '(-4, 1)', '(-4, -1)', '(3, -1)', '(2, 0)']},
      {'id': 'r10-chain-compare',
       'mode': 'rust',
       'title': 'Цепочка сравнений',
       'statement': 'Python: lo < x < hi. Напишите strictly_between(x: i32, lo: i32, hi: i32) -> bool — x '
                    'строго между lo и hi.',
       'starter': 'fn strictly_between(x: i32, lo: i32, hi: i32) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", strictly_between(5, 1, 10));\n'
                 '    println!("{}", strictly_between(1, 1, 10));\n'
                 '    println!("{}", strictly_between(10, 1, 10));\n'
                 '    println!("{}", strictly_between(0, 1, 10));\n'
                 '}\n',
       'hint': 'Две проверки через &&.',
       'expected': ['true', 'false', 'false', 'false']},
      {'id': 'r10-elif-chain',
       'mode': 'rust',
       'title': 'elif → else if',
       'statement': "Python: if/elif для категорий температуры. Напишите category(t: i32) -> &'static str: "
                    '«мороз» при t < 0, «холодно» при t < 10, «тепло» при t < 25, иначе «жарко».',
       'starter': "fn category(t: i32) -> &'static str {\n    todo!()\n}\n",
       'driver': 'fn main() {\n'
                 '    for t in [-5, 0, 9, 10, 24, 25, 40] {\n'
                 '        println!("{} {}", t, category(t));\n'
                 '    }\n'
                 '}\n',
       'hint': 'Цепочка if / else if / else — одно выражение.',
       'expected': ['-5 мороз', '0 холодно', '9 холодно', '10 тепло', '24 тепло', '25 жарко', '40 жарко']},
      {'id': 'r10-match-grade',
       'mode': 'rust',
       'title': 'match вместо if-цепочки',
       'statement': "Напишите grade(score: u32) -> char через match с диапазонами: 90..=100 → 'A', 80..=89 → "
                    "'B', 70..=79 → 'C', 60..=69 → 'D', иначе 'F'.",
       'starter': 'fn grade(score: u32) -> char {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for s in [100, 90, 89, 75, 60, 59, 0] {\n'
                 '        print!("{}", grade(s));\n'
                 '    }\n'
                 '    println!();\n'
                 '}\n',
       'hint': 'Образцы-диапазоны с ..=',
       'expected': ['AABCDFF']},
      {'id': 'r10-match-tuple',
       'mode': 'rust',
       'title': 'FizzBuzz через match',
       'statement': 'Напишите fizz(n: u32) -> String: «FizzBuzz» / «Fizz» / «Buzz» / число. Используйте '
                    'match по кортежу (n % 3, n % 5).',
       'starter': 'fn fizz(n: u32) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for n in 1..=15 {\n'
                 '        print!("{} ", fizz(n));\n'
                 '    }\n'
                 '    println!();\n'
                 '}\n',
       'hint': 'match (a, b) { (0, 0) => …, (0, _) => … }',
       'expected': ['1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz']},
      {'id': 'r10-fn-pointer',
       'mode': 'rust',
       'title': 'Передача функции',
       'statement': 'Python: def apply(f, x): return f(x). Напишите apply(f: fn(i32) -> i32, x: i32) -> i32.',
       'starter': 'fn apply(f: fn(i32) -> i32, x: i32) -> i32 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    fn double(x: i32) -> i32 {\n'
                 '        x * 2\n'
                 '    }\n'
                 '    fn neg(x: i32) -> i32 {\n'
                 '        -x\n'
                 '    }\n'
                 '    println!("{}", apply(double, 21));\n'
                 '    println!("{}", apply(neg, 5));\n'
                 '    println!("{}", apply(|x| x * x, 7));\n'
                 '}\n',
       'hint': 'Параметр f вызывается как обычная функция: f(x).',
       'expected': ['42', '-5', '49']},
      {'id': 'r10-apply-twice',
       'mode': 'rust',
       'title': 'Применить дважды',
       'statement': 'Напишите apply_twice(f, x): применить функцию f к x два раза. Параметр f объявите как '
                    'impl Fn(i32) -> i32.',
       'starter': 'fn apply_twice(f: impl Fn(i32) -> i32, x: i32) -> i32 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", apply_twice(|x| x + 3, 10));\n'
                 '    let k = 5;\n'
                 '    println!("{}", apply_twice(|x| x * k, 2));\n'
                 '    println!("{}", apply_twice(|x| -x, 9));\n'
                 '}\n',
       'hint': 'f(f(x)); замыкание может захватывать k.',
       'expected': ['16', '50', '9']},
      {'id': 'r10-compose',
       'mode': 'rust',
       'title': 'Композиция функций',
       'statement': 'Python: lambda x: f(g(x)). Напишите compose(f, g, x) = f(g(x)) для f, g: impl Fn(i32) '
                    '-> i32.',
       'starter': 'fn compose(f: impl Fn(i32) -> i32, g: impl Fn(i32) -> i32, x: i32) -> i32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", compose(|x| x + 1, |x| x * 2, 10));\n'
                 '    println!("{}", compose(|x| x * 2, |x| x + 1, 10));\n'
                 '}\n',
       'hint': 'f(g(x)) — сначала g, потом f.',
       'expected': ['21', '22']},
      {'id': 'r10-any-neg',
       'mode': 'rust',
       'title': 'any',
       'statement': 'Python: any(x < 0 for x in v). Напишите has_negative(v: &[i32]) -> bool с помощью '
                    'iter().any.',
       'starter': 'fn has_negative(v: &[i32]) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", has_negative(&[1, 2, 3]));\n'
                 '    println!("{}", has_negative(&[1, -2, 3]));\n'
                 '    println!("{}", has_negative(&[]));\n'
                 '}\n',
       'hint': 'v.iter().any(|&x| x < 0)',
       'expected': ['false', 'true', 'false']},
      {'id': 'r10-all-pos',
       'mode': 'rust',
       'title': 'all',
       'statement': 'Python: all(x > 0 for x in v). Напишите all_positive(v: &[i32]) -> bool (для пустого '
                    'среза — true).',
       'starter': 'fn all_positive(v: &[i32]) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", all_positive(&[1, 2, 3]));\n'
                 '    println!("{}", all_positive(&[1, 0, 3]));\n'
                 '    println!("{}", all_positive(&[]));\n'
                 '}\n',
       'hint': 'all для пустой последовательности даёт true.',
       'expected': ['true', 'false', 'true']},
      {'id': 'r10-index-of',
       'mode': 'rust',
       'title': 'list.index без исключения',
       'statement': 'Python: v.index(x) бросает ValueError, если элемента нет. Напишите index_of(v: &[i32], '
                    'x: i32) -> Option<usize> методом position.',
       'starter': 'fn index_of(v: &[i32], x: i32) -> Option<usize> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", index_of(&[5, 7, 9, 7], 7));\n'
                 '    println!("{:?}", index_of(&[5, 7], 1));\n'
                 '    println!("{:?}", index_of(&[], 1));\n'
                 '}\n',
       'hint': 'iter().position(|&e| e == x)',
       'expected': ['Some(1)', 'None', 'None']},
      {'id': 'r10-zip-dot',
       'mode': 'rust',
       'title': 'zip',
       'statement': 'Python: sum(a * b for a, b in zip(xs, ys)). Напишите dot(xs: &[i32], ys: &[i32]) -> i32 '
                    'с помощью zip (длина — по короткому срезу).',
       'starter': 'fn dot(xs: &[i32], ys: &[i32]) -> i32 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", dot(&[1, 2, 3], &[4, 5, 6]));\n'
                 '    println!("{}", dot(&[1, 2, 3], &[10, 10]));\n'
                 '    println!("{}", dot(&[], &[1]));\n'
                 '}\n',
       'hint': 'xs.iter().zip(ys.iter()).map(|(a, b)| a * b).sum()',
       'expected': ['32', '30', '0']},
      {'id': 'r10-comprehension',
       'mode': 'rust',
       'title': 'Генератор списка',
       'statement': 'Python: [x * x for x in v if x % 2 == 0]. Напишите even_squares(v: &[i32]) -> Vec<i32>.',
       'starter': 'fn even_squares(v: &[i32]) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", even_squares(&[1, 2, 3, 4, 5, 6]));\n'
                 '    println!("{:?}", even_squares(&[1, 3]));\n'
                 '    println!("{:?}", even_squares(&[-2, 0]));\n'
                 '}\n',
       'hint': 'filter → map → collect',
       'expected': ['[4, 16, 36]', '[]', '[4, 0]']},
      {'id': 'r10-lens',
       'mode': 'rust',
       'title': 'Длины слов',
       'statement': 'Python: [len(w) for w in words]. Напишите lens(words: &[&str]) -> Vec<usize>: число '
                    'символов (не байтов!) в каждом слове.',
       'starter': 'fn lens(words: &[&str]) -> Vec<usize> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n    println!("{:?}", lens(&["привет", "hi", "日本語", ""]));\n}\n',
       'hint': 'chars().count() — символы.',
       'expected': ['[6, 2, 3, 0]']},
      {'id': 'r10-longest',
       'mode': 'rust',
       'title': 'max с ключом',
       'statement': "Python: max(words, key=len). Напишите longest<'a>(words: &[&'a str]) -> &'a str — самое "
                    'длинное по числу символов слово (при равенстве — первое). Срез не пуст.',
       'starter': "fn longest<'a>(words: &[&'a str]) -> &'a str {\n    todo!()\n}\n",
       'driver': 'fn main() {\n'
                 '    println!("{}", longest(&["a", "ccc", "bb", "ddd"]));\n'
                 '    println!("{}", longest(&["один"]));\n'
                 '    println!("{}", longest(&["аб", "вг", "дежз"]));\n'
                 '}\n',
       'hint': 'Сравнивайте количество символов.',
       'expected': ['ccc', 'один', 'дежз']},
      {'id': 'r10-digits-sum',
       'mode': 'rust',
       'title': 'sum(map(int, str(n)))',
       'statement': 'Python: sum(int(c) for c in str(n)). Напишите digit_sum(n: u64) -> u32 через '
                    'n.to_string() и chars().',
       'starter': 'fn digit_sum(n: u64) -> u32 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", digit_sum(0));\n'
                 '    println!("{}", digit_sum(12345));\n'
                 '    println!("{}", digit_sum(9_999_999_999));\n'
                 '}\n',
       'hint': 'c.to_digit(10).unwrap()',
       'expected': ['0', '15', '90']},
      {'id': 'r10-loop-value',
       'mode': 'rust',
       'title': 'while True',
       'statement': 'Python: while True: … break. Напишите first_pow2_above(n: u64) -> u64: наименьшая '
                    'степень двойки, строго большая n. Используйте loop и break со значением.',
       'starter': 'fn first_pow2_above(n: u64) -> u64 {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", first_pow2_above(0));\n'
                 '    println!("{}", first_pow2_above(1));\n'
                 '    println!("{}", first_pow2_above(1000));\n'
                 '    println!("{}", first_pow2_above(1 << 40));\n'
                 '}\n',
       'hint': 'break p; возвращает значение из loop.',
       'expected': ['1', '2', '1024', '2199023255552']},
      {'id': 'r10-for-else',
       'mode': 'rust',
       'title': 'for–else без else',
       'statement': 'Python: for-else для проверки простоты. Напишите is_prime(n: u32) -> bool (n ≥ 2 → true '
                    'для простых). Для n < 2 — false. Перебирайте делители до √n.',
       'starter': 'fn is_prime(n: u32) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for n in [0, 1, 2, 3, 4, 17, 18, 97, 7919, 1_000_000_007] {\n'
                 '        println!("{} {}", n, is_prime(n));\n'
                 '    }\n'
                 '}\n',
       'hint': 'Ранний return false внутри цикла; true — после цикла.',
       'expected': ['0 false',
                    '1 false',
                    '2 true',
                    '3 true',
                    '4 false',
                    '17 true',
                    '18 false',
                    '97 true',
                    '7919 true',
                    '1000000007 true']},
      {'id': 'r10-step-range',
       'mode': 'rust',
       'title': 'range со шагом',
       'statement': 'Python: list(range(start, stop, step)). Напишите range_step(start: i32, stop: i32, '
                    'step: usize) -> Vec<i32> (step > 0, stop не включается).',
       'starter': 'fn range_step(start: i32, stop: i32, step: usize) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", range_step(0, 10, 3));\n'
                 '    println!("{:?}", range_step(5, 5, 1));\n'
                 '    println!("{:?}", range_step(-3, 4, 2));\n'
                 '}\n',
       'hint': '(start..stop).step_by(step).collect()',
       'expected': ['[0, 3, 6, 9]', '[]', '[-3, -1, 1, 3]']},
      {'id': 'r10-enumerate-lines',
       'mode': 'rust',
       'title': 'enumerate с единицы',
       'statement': 'Python: for i, line in enumerate(lines, 1): print(f"{i}: {line}"). Напишите '
                    'numbered(lines: &[&str]) -> Vec<String> строки вида «1: …».',
       'starter': 'fn numbered(lines: &[&str]) -> Vec<String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for l in numbered(&["раз", "два", "три"]) {\n'
                 '        println!("{}", l);\n'
                 '    }\n'
                 '}\n',
       'hint': 'enumerate даёт индекс с нуля — прибавьте 1.',
       'expected': ['1: раз', '2: два', '3: три']},
      {'id': 'r10-try-except',
       'mode': 'rust',
       'title': 'try/except → Result',
       'statement': 'Python: int(s) в try/except. Напишите parse_age(s: &str) -> Result<u8, String>: '
                    'Ok(возраст) для целых 0..=150, иначе Err("…"): «не число», если разбор не удался, и '
                    '«вне диапазона» для чисел вне 0..=150.',
       'starter': 'fn parse_age(s: &str) -> Result<u8, String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for s in ["30", " 7 ", "abc", "200", "-1", "150"] {\n'
                 '        println!("{:?}", parse_age(s));\n'
                 '    }\n'
                 '}\n',
       'hint': 'match s.parse() с ранним return Err(…).',
       'expected': ['Ok(30)',
                    'Ok(7)',
                    'Err("не число")',
                    'Err("вне диапазона")',
                    'Err("вне диапазона")',
                    'Ok(150)']},
      {'id': 'r10-raise',
       'mode': 'rust',
       'title': 'raise → Err',
       'statement': 'Python: def sqrt(x): if x < 0: raise ValueError. Напишите safe_sqrt(x: f64) -> '
                    'Result<f64, String>: Err("отрицательное"), если x < 0, иначе Ok(√x).',
       'starter': 'fn safe_sqrt(x: f64) -> Result<f64, String> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", safe_sqrt(16.0));\n'
                 '    println!("{:?}", safe_sqrt(-1.0));\n'
                 '    println!("{:?}", safe_sqrt(0.0));\n'
                 '}\n',
       'hint': 'Err(String::from("…")) и Ok(x.sqrt()).',
       'expected': ['Ok(4.0)', 'Err("отрицательное")', 'Ok(0.0)']},
      {'id': 'r10-question-mark',
       'mode': 'rust',
       'title': 'Оператор ?',
       'statement': 'Напишите sum_two(a: &str, b: &str) -> Result<i32, std::num::ParseIntError>: разберите '
                    'обе строки и верните сумму. Используйте оператор ? вместо match.',
       'starter': 'fn sum_two(a: &str, b: &str) -> Result<i32, std::num::ParseIntError> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", sum_two("2", " 3"));\n'
                 '    println!("{}", sum_two("2", "x").is_err());\n'
                 '    println!("{}", sum_two("", "5").is_err());\n'
                 '}\n',
       'hint': 'let x: i32 = a.trim().parse()?; при ошибке функция сразу возвращает Err.',
       'expected': ['Ok(5)', 'true', 'true']},
      {'id': 'r10-first-even',
       'mode': 'rust',
       'title': 'Option из поиска',
       'statement': 'Python: next((x for x in v if x % 2 == 0), None). Напишите first_even(v: &[i32]) -> '
                    'Option<i32>.',
       'starter': 'fn first_even(v: &[i32]) -> Option<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", first_even(&[1, 3, 4, 6]));\n'
                 '    println!("{:?}", first_even(&[1, 3]));\n'
                 '    println!("{:?}", first_even(&[]));\n'
                 '}\n',
       'hint': 'iter().copied().find(…) возвращает Option.',
       'expected': ['Some(4)', 'None', 'None']},
      {'id': 'r10-password',
       'mode': 'rust',
       'title': 'Проверка пароля',
       'statement': 'Напишите is_valid(s: &str) -> bool: длина не меньше 8 символов, есть хотя бы одна цифра '
                    'и хотя бы одна заглавная буква. Используйте ранние return.',
       'starter': 'fn is_valid(s: &str) -> bool {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for p in ["abc", "abcdefgh", "abcdefg1", "Abcdefg1", "Пароль123", "пароль123"] {\n'
                 '        println!("{} {}", p, is_valid(p));\n'
                 '    }\n'
                 '}\n',
       'hint': 'Три проверки: длина, цифра, заглавная.',
       'expected': ['abc false',
                    'abcdefgh false',
                    'abcdefg1 false',
                    'Abcdefg1 true',
                    'Пароль123 true',
                    'пароль123 false']},
      {'id': 'r10-clamp-all',
       'mode': 'rust',
       'title': 'Зажать все',
       'statement': 'Python: [max(lo, min(hi, x)) for x in v]. Напишите clamp_all(v: &[i32], lo: i32, hi: '
                    'i32) -> Vec<i32>.',
       'starter': 'fn clamp_all(v: &[i32], lo: i32, hi: i32) -> Vec<i32> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", clamp_all(&[-5, 0, 5, 10, 15], 0, 10));\n'
                 '    println!("{:?}", clamp_all(&[], 0, 1));\n'
                 '}\n',
       'hint': 'x.max(lo).min(hi)',
       'expected': ['[0, 0, 5, 10, 10]', '[]']},
      {'id': 'r10-config-default',
       'mode': 'rust',
       'title': 'Строитель вместо kwargs',
       'statement': 'Python: def window(width=800, height=600, title="окно"). Реализуйте структуру Config { '
                    'width: u32, height: u32, title: String } с функцией default() (800, 600, «окно») и '
                    'методами-«строителями» with_width(mut self, w: u32) -> Config и with_title(mut self, t: '
                    '&str) -> Config.',
       'starter': 'struct Config {\n'
                  '    width: u32,\n'
                  '    height: u32,\n'
                  '    title: String,\n'
                  '}\n'
                  '\n'
                  'impl Config {\n'
                  '    fn default() -> Config {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn with_width(mut self, w: u32) -> Config {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn with_title(mut self, t: &str) -> Config {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a = Config::default();\n'
                 '    println!("{} {} {}", a.width, a.height, a.title);\n'
                 '    let b = Config::default().with_width(1920).with_title("игра");\n'
                 '    println!("{} {} {}", b.width, b.height, b.title);\n'
                 '}\n',
       'hint': 'Метод принимает self по значению, меняет поле и возвращает self — цепочку можно продолжать.',
       'expected': ['800 600 окно', '1920 600 игра']},
      {'id': 'r10-gcd-lcm',
       'mode': 'rust',
       'title': 'НОД и НОК',
       'statement': 'Напишите gcd(a: u64, b: u64) -> u64 (Евклид) и lcm(a: u64, b: u64) -> u64 (НОК = a / '
                    'gcd · b); lcm(0, x) = 0.',
       'starter': 'fn gcd(a: u64, b: u64) -> u64 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn lcm(a: u64, b: u64) -> u64 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", gcd(48, 18));\n'
                 '    println!("{}", lcm(4, 6));\n'
                 '    println!("{}", lcm(0, 5));\n'
                 '    println!("{}", lcm(21, 6));\n'
                 '}\n',
       'hint': 'Сначала делите, потом умножайте — так число не переполнится.',
       'expected': ['6', '12', '0', '42']}]}
