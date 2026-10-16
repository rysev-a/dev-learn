"""Задачи книги «Изучаем Rust»: глава 17 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {17: [{'id': 'r17-point-new',
       'mode': 'rust',
       'title': 'Структура и методы: Point',
       'statement': 'Опишите методы Point: origin() — точка (0, 0); new(x, y); manhattan(&self, other: '
                    '&Point) → |dx| + |dy|; translate(&mut self, dx, dy) — сдвинуть на месте.',
       'starter': 'struct Point {\n'
                  '    x: i32,\n'
                  '    y: i32,\n'
                  '}\n'
                  '\n'
                  'impl Point {\n'
                  '    fn origin() -> Point {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn new(x: i32, y: i32) -> Point {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn manhattan(&self, other: &Point) -> i32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn translate(&mut self, dx: i32, dy: i32) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let o = Point::origin();\n'
                 '    let mut p = Point::new(3, -4);\n'
                 '    println!("{}", p.manhattan(&o));\n'
                 '    p.translate(-3, 4);\n'
                 '    println!("{} {} {}", p.x, p.y, p.manhattan(&o));\n'
                 '}\n',
       'hint': 'Сокращённая запись поля: Point { x, y }, если имена параметров совпадают с именами полей.',
       'expected': ['7', '0 0 0']},
      {'id': 'r17-rect-methods',
       'mode': 'rust',
       'title': 'Прямоугольник: &self, &mut self',
       'statement': 'Rect { w, h } (u32). Методы: area(&self), perimeter(&self), is_square(&self), '
                    'can_hold(&self, other: &Rect) — помещается ли other целиком (обе стороны строго меньше '
                    'или равны) и scale(&mut self, k: u32) — умножить обе стороны на k.',
       'starter': 'struct Rect {\n'
                  '    w: u32,\n'
                  '    h: u32,\n'
                  '}\n'
                  '\n'
                  'impl Rect {\n'
                  '    fn area(&self) -> u32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn perimeter(&self) -> u32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn is_square(&self) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn can_hold(&self, other: &Rect) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn scale(&mut self, k: u32) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut r = Rect { w: 4, h: 3 };\n'
                 '    let small = Rect { w: 2, h: 2 };\n'
                 '    println!("{} {} {}", r.area(), r.perimeter(), r.is_square());\n'
                 '    println!("{} {}", r.can_hold(&small), small.can_hold(&r));\n'
                 '    r.scale(2);\n'
                 '    println!("{} {}", r.w, r.h);\n'
                 '    println!("{}", Rect { w: 5, h: 5 }.is_square());\n'
                 '}\n',
       'hint': 'В can_hold сравнивайте обе стороны: self.w >= other.w && self.h >= other.h.',
       'expected': ['12 14 false', 'true false', '8 6', 'true']},
      {'id': 'r17-derive-debug',
       'mode': 'rust',
       'title': 'derive: Debug, Clone, PartialEq, Default',
       'statement': 'Код не собирается: драйвер печатает User через {:?}, клонирует, сравнивает через == и '
                    'создаёт значение по умолчанию. Добавьте над структурой один атрибут derive с нужными '
                    'четырьмя именами.',
       'starter': 'struct User {\n    name: String,\n    age: u32,\n    active: bool,\n}\n',
       'driver': 'fn main() {\n'
                 '    let u = User { name: String::from("Анна"), age: 30, active: true };\n'
                 '    let v = u.clone();\n'
                 '    println!("{:?}", u);\n'
                 '    println!("{}", u == v);\n'
                 '    let d = User::default();\n'
                 '    println!("{:?} {}", d, d == u);\n'
                 '    println!("{:#?}", v);\n'
                 '}\n',
       'hint': '#[derive(Debug, Clone, PartialEq, Default)] — все поля уже умеют всё это, поэтому derive '
               'сработает.',
       'expected': ['User { name: "Анна", age: 30, active: true }',
                    'true',
                    'User { name: "", age: 0, active: false } false',
                    'User {',
                    '    name: "Анна",',
                    '    age: 30,',
                    '    active: true,',
                    '}']},
      {'id': 'r17-display-impl',
       'mode': 'rust',
       'title': 'Display вручную',
       'statement': 'Реализуйте std::fmt::Display: для Point — «(x, y)»; для Temp — «21.5°C» или «70.7°F» '
                    '(одно знак после запятой). Тогда работают {} и to_string().',
       'starter': 'use std::fmt;\n'
                  '\n'
                  'struct Point {\n'
                  '    x: i32,\n'
                  '    y: i32,\n'
                  '}\n'
                  '\n'
                  'enum Temp {\n'
                  '    C(f64),\n'
                  '    F(f64),\n'
                  '}\n'
                  '\n'
                  'impl fmt::Display for Point {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl fmt::Display for Temp {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let p = Point { x: 3, y: -1 };\n'
                 '    println!("{} [{:>10}]", p, p.to_string());\n'
                 '    println!("{} {}", Temp::C(21.5), Temp::F(70.66));\n'
                 '}\n',
       'hint': 'write!(f, "({}, {})", self.x, self.y); для Temp — match self { Temp::C(t) => write!(...), '
               '... }.',
       'expected': ['(3, -1) [   (3, -1)]', '21.5°C 70.7°F']},
      {'id': 'r17-repr-c',
       'mode': 'rust',
       'title': 'Выравнивание: repr(C) и порядок полей',
       'statement': 'Три структуры с полями u8, u32, u8. Tight — по умолчанию (раст сам переставляет поля): '
                    '8 байт. Wide — те же поля, но в раскладке языка си (#[repr(C)]): 12 байт. Packed — '
                    '#[repr(C)], но поля расположите так, чтобы размер стал 8. Заготовка даёт для всех трёх '
                    'размер 8: исправьте Wide и Packed.',
       'starter': 'struct Tight {\n'
                  '    a: u8,\n'
                  '    b: u32,\n'
                  '    c: u8,\n'
                  '}\n'
                  '\n'
                  'struct Wide {\n'
                  '    a: u8,\n'
                  '    b: u32,\n'
                  '    c: u8,\n'
                  '}\n'
                  '\n'
                  'struct Packed {\n'
                  '    a: u8,\n'
                  '    b: u32,\n'
                  '    c: u8,\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    use std::mem::{align_of, size_of};\n'
                 '    println!("{} {} {}", size_of::<Tight>(), size_of::<Wide>(), size_of::<Packed>());\n'
                 '    println!("{}", align_of::<Wide>());\n'
                 '}\n',
       'hint': 'В repr(C) поля идут по порядку, и после каждого вставляется выравнивание: u8, [3 пустых], '
               'u32, u8, [3 пустых] = 12. Поставьте u32 первым.',
       'expected': ['8 12 8', '4']},
      {'id': 'r17-enum-shape',
       'mode': 'rust',
       'title': 'enum Shape: площадь и периметр',
       'statement': 'Shape — Circle(r), Rect(w, h) или Tri(a, b, c) (стороны). area(&self) → f64 (для '
                    'треугольника — формула Герона), perimeter(&self) → f64. π берите из '
                    'std::f64::consts::PI.',
       'starter': 'use std::f64::consts::PI;\n'
                  '\n'
                  'enum Shape {\n'
                  '    Circle(f64),\n'
                  '    Rect(f64, f64),\n'
                  '    Tri(f64, f64, f64),\n'
                  '}\n'
                  '\n'
                  'impl Shape {\n'
                  '    fn area(&self) -> f64 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn perimeter(&self) -> f64 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let shapes = [Shape::Circle(1.0), Shape::Rect(3.0, 4.0), Shape::Tri(3.0, 4.0, 5.0)];\n'
                 '    for s in &shapes {\n'
                 '        println!("{:.2} {:.2}", s.area(), s.perimeter());\n'
                 '    }\n'
                 '}\n',
       'hint': 'match self даёт привязки-ссылки: r, w, h — это &f64, арифметика с ними работает.',
       'expected': ['3.14 6.28', '12.00 14.00', '6.00 12.00']},
      {'id': 'r17-enum-size',
       'mode': 'rust',
       'title': 'Размеры перечислений',
       'statement': 'Напишите sizes() → [usize; 6]: size_of для Dir (перечисление из четырёх вариантов без '
                    'данных), Option<u8>, Option<u32>, Option<Box<i32>>, Option<&str>, Result<u8, u8> — в '
                    'этом порядке. Подумайте, где нужен тег, а где его заменяет ниша.',
       'starter': 'enum Dir {\n'
                  '    N,\n'
                  '    E,\n'
                  '    S,\n'
                  '    W,\n'
                  '}\n'
                  '\n'
                  'fn sizes() -> [usize; 6] {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let _ = [Dir::N, Dir::E, Dir::S, Dir::W];\n'
                 '    println!("{:?}", sizes());\n'
                 '}\n',
       'hint': 'size_of::<Тип>() из std::mem; Option<&str> — это срез (16 байт) с нишей в указателе.',
       'expected': ['[1, 2, 8, 8, 16, 2]']},
      {'id': 'r17-match-coin',
       'mode': 'rust',
       'title': 'match: монеты',
       'statement': 'enum Coin { Penny, Nickel, Dime, Quarter(u32) } — у четвертака есть год чеканки. '
                    'cents(&Coin) → u32: 1, 5, 10 и 25; но четвертак до 1980 года (не включая) считается '
                    'коллекционным и стоит 100. total(&[Coin]) → u32 — сумма.',
       'starter': 'enum Coin {\n'
                  '    Penny,\n'
                  '    Nickel,\n'
                  '    Dime,\n'
                  '    Quarter(u32),\n'
                  '}\n'
                  '\n'
                  'fn cents(c: &Coin) -> u32 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn total(coins: &[Coin]) -> u32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let v = [Coin::Penny, Coin::Dime, Coin::Quarter(1999), Coin::Quarter(1960), '
                 'Coin::Nickel];\n'
                 '    println!("{}", total(&v));\n'
                 '    println!("{} {}", cents(&Coin::Quarter(1980)), cents(&Coin::Quarter(1979)));\n'
                 '    println!("{}", total(&[]));\n'
                 '}\n',
       'hint': 'Ветвь с охраной Quarter(year) if *year < 1980 должна идти раньше общей Quarter(_).',
       'expected': ['141', '25 100', '0']},
      {'id': 'r17-match-ranges',
       'mode': 'rust',
       'title': 'match: диапазоны, | , @ и охрана',
       'statement': 'classify(n: i32) → String одним match: отрицательное → "negative"; 0 → "zero"; цифра '
                    '1..=9 → "digit N" (с самим числом); 10, 20 или 30 → "round"; остальные чётные → "even"; '
                    'прочие → "odd".',
       'starter': 'fn classify(n: i32) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    for n in [-5, 0, 7, 20, 14, 15, 100, 11] {\n'
                 '        println!("{n}: {}", classify(n));\n'
                 '    }\n'
                 '}\n',
       'hint': 'Порядок ветвей важен: специальные случаи выше общих. Шаблон d @ 1..=9 привязывает число к '
               'имени d.',
       'expected': ['-5: negative',
                    '0: zero',
                    '7: digit 7',
                    '20: round',
                    '14: even',
                    '15: odd',
                    '100: even',
                    '11: odd']},
      {'id': 'r17-match-tuple',
       'mode': 'rust',
       'title': 'match по кортежу: FizzBuzz без if',
       'statement': 'fizzbuzz(n: u32) → String одним match по паре (n % 3, n % 5): «FizzBuzz», «Fizz», '
                    '«Buzz» или само число. Слово if в коде использовать нельзя.',
       'starter': 'fn fizzbuzz(n: u32) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!("i", "f ")).count();\n'
                 '    let line: Vec<String> = (1..=15).map(fizzbuzz).collect();\n'
                 '    println!("{}", line.join(" "));\n'
                 '    println!("{} {}", fizzbuzz(30), fizzbuzz(31));\n'
                 '    println!("ifs: {}", bad0);\n'
                 '}\n',
       'hint': 'Образец (0, _) означает: остаток по 3 равен нулю, остаток по 5 не важен.',
       'expected': ['1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz', 'FizzBuzz 31', 'ifs: 0']},
      {'id': 'r17-match-slice',
       'mode': 'rust',
       'title': 'Образцы на срезах',
       'statement': 'describe(v: &[i32]) → String одним match с образцами срезов: пустой → "empty"; один '
                    'элемент → "one: X"; два → "two: A, B"; больше → "many: FIRST..LAST" (первый и '
                    'последний).',
       'starter': 'fn describe(v: &[i32]) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", describe(&[]));\n'
                 '    println!("{}", describe(&[7]));\n'
                 '    println!("{}", describe(&[1, 2]));\n'
                 '    println!("{}", describe(&[1, 2, 3, 4, 5]));\n'
                 '    println!("{}", describe(&vec![9, 8, 7]));\n'
                 '}\n',
       'hint': 'Образец [first, .., last] подходит срезу из двух и более элементов; двухэлементный образец '
               'поставьте раньше.',
       'expected': ['empty', 'one: 7', 'two: 1, 2', 'many: 1..5', 'many: 9..7']},
      {'id': 'r17-option-div',
       'mode': 'rust',
       'title': 'Option и оператор ?',
       'statement': 'safe_div(a, b) → Option<i32> (None при b == 0). parse_pair(s) → Option<(i32, i32)>: '
                    'строка вида "3,4" (без пробелов), любая ошибка → None. ratio(s) → Option<i32>: '
                    'разобрать пару и безопасно разделить; здесь используйте оператор ?. Вызов unwrap() '
                    'запрещён.',
       'starter': 'fn safe_div(a: i32, b: i32) -> Option<i32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn parse_pair(s: &str) -> Option<(i32, i32)> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn ratio(s: &str) -> Option<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!("unw", "rap(")).count();\n'
                 '    for s in ["12,4", "7,0", "x,1", "5", "-9,3", "1,2,3"] {\n'
                 '        println!("{:?}", ratio(s));\n'
                 '    }\n'
                 '    println!("{:?} {:?}", safe_div(1, 0), parse_pair("8,2"));\n'
                 '    println!("unwraps: {}", bad0);\n'
                 '}\n',
       'hint': 'l.parse::<i32>().ok()? превращает Result в Option и сразу возвращает None при ошибке; '
               "split_once(',') тоже Option.",
       'expected': ['Some(3)',
                    'None',
                    'None',
                    'None',
                    'Some(-3)',
                    'None',
                    'None Some((8, 2))',
                    'unwraps: 0']},
      {'id': 'r17-option-combinators',
       'mode': 'rust',
       'title': 'Комбинаторы Option без match',
       'statement': 'first_even_square(v) → Option<i32>: квадрат первого чётного числа. name_len(name: '
                    'Option<&str>) → usize: длина имени или 0. parse_or(s, default) → i32: число из строки '
                    'или default. Условие: ни match, ни if let — только методы Option и Result (map, '
                    'and_then, unwrap_or, find...).',
       'starter': 'fn first_even_square(v: &[i32]) -> Option<i32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn name_len(name: Option<&str>) -> usize {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn parse_or(s: &str, default: i32) -> i32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!("mat", "ch ")).count();\n'
                 '    let bad1 = src.matches(concat!("if ", "let ")).count();\n'
                 '    println!("{:?} {:?}", first_even_square(&[3, 5, 6, 8]), first_even_square(&[1, 3]));\n'
                 '    println!("{} {}", name_len(Some("Анна")), name_len(None));\n'
                 '    println!("{} {} {}", parse_or(" 42 ", 0), parse_or("abc", -1), parse_or("", 7));\n'
                 '    println!("banned: {} {}", bad0, bad1);\n'
                 '}\n',
       'hint': 'find возвращает Option<&i32>; map превращает значение внутри. Для разбора строки: '
               's.trim().parse().unwrap_or(default).',
       'expected': ['Some(36) None', '8 0', '42 -1 7', 'banned: 0 0']},
      {'id': 'r17-let-else',
       'mode': 'rust',
       'title': 'let else и if let',
       'statement': 'parse_kv(line) → String: строка вида "ключ=значение"; через let else разобрать по '
                    'первому «=», иначе вернуть "bad"; результат — «ключ -> значение» (обе части с '
                    'обрезанными пробелами). show(o: Option<i32>) → String: «got N», если число есть, иначе '
                    '«nothing» — через if let / else.',
       'starter': 'fn parse_kv(line: &str) -> String {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn show(o: Option<i32>) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", parse_kv("name = rust"));\n'
                 '    println!("{}", parse_kv("novalue"));\n'
                 '    println!("{}", parse_kv("a=b=c"));\n'
                 '    println!("{} {}", show(Some(5)), show(None));\n'
                 '}\n',
       'hint': 'let Some((k, v)) = … else { return …; }; — после этой строки k и v уже обычные срезы.',
       'expected': ['name -> rust', 'bad', 'a -> b=c', 'got 5 nothing']},
      {'id': 'r17-rpn',
       'mode': 'rust',
       'title': 'Стек и while let: обратная польская запись',
       'statement': 'eval_rpn(tokens: &[&str]) → Option<i64>: вычислить выражение в обратной польской '
                    'записи: числа и операторы + - * /. Стек — Vec<i64>. None, если не хватает операндов, '
                    'делитель равен нулю, токен не распознан или в конце на стеке не ровно одно число.',
       'starter': 'fn eval_rpn(tokens: &[&str]) -> Option<i64> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", eval_rpn(&["3", "4", "+", "2", "*"]));\n'
                 '    println!("{:?}", eval_rpn(&["5", "1", "2", "+", "4", "*", "+", "3", "-"]));\n'
                 '    println!("{:?}", eval_rpn(&["1", "+"]));\n'
                 '    println!("{:?}", eval_rpn(&["4", "0", "/"]));\n'
                 '    println!("{:?}", eval_rpn(&["1", "2"]));\n'
                 '    println!("{:?}", eval_rpn(&["x"]));\n'
                 '    println!("{:?}", eval_rpn(&[]));\n'
                 '}\n',
       'hint': 'Для оператора достаньте b = pop()?, затем a = pop()? (порядок!). Остальные токены разберите '
               'как числа через parse().ok()?.',
       'expected': ['Some(14)', 'Some(14)', 'None', 'None', 'None', 'None', 'None']},
      {'id': 'r17-state-machine',
       'mode': 'rust',
       'title': 'Автомат состояний: дверь',
       'statement': 'Door — Open, Closed, Locked(код). apply(self, Action) → Door: Open + Close → Closed; '
                    'Closed + Open → Open; Closed + Lock(c) → Locked(c); Locked(c) + Unlock(x) → Closed, '
                    'если x == c, иначе остаётся Locked(c). Любое другое действие — состояние не меняется. '
                    'Метод принимает self по значению.',
       'starter': '#[derive(Debug, PartialEq)]\n'
                  'enum Door {\n'
                  '    Open,\n'
                  '    Closed,\n'
                  '    Locked(u32),\n'
                  '}\n'
                  '\n'
                  'enum Action {\n'
                  '    Open,\n'
                  '    Close,\n'
                  '    Lock(u32),\n'
                  '    Unlock(u32),\n'
                  '}\n'
                  '\n'
                  'impl Door {\n'
                  '    fn apply(self, action: Action) -> Door {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    use Action::*;\n'
                 '    let mut d = Door::Open;\n'
                 '    for a in [Lock(1), Close, Lock(1234), Open, Unlock(1), Unlock(1234), Open] {\n'
                 '        d = d.apply(a);\n'
                 '        println!("{:?}", d);\n'
                 '    }\n'
                 '    println!("{}", Door::Closed.apply(Close) == Door::Closed);\n'
                 '}\n',
       'hint': 'Матч по паре (self, action) читается как таблица переходов; последняя ветвь (state, _) => '
               'state возвращает прежнее состояние.',
       'expected': ['Open',
                    'Closed',
                    'Locked(1234)',
                    'Locked(1234)',
                    'Locked(1234)',
                    'Closed',
                    'Open',
                    'true']},
      {'id': 'r17-direction',
       'mode': 'rust',
       'title': 'enum без данных: Direction',
       'statement': 'Direction — N, E, S, W (derive Debug, Clone, Copy, PartialEq). turn_right(self), '
                    'turn_left(self), opposite(self), from_char(c: char) → Option<Direction> (буквы N E S W '
                    'в любом регистре) и to_char(self) → char (заглавная).',
       'starter': '#[derive(Debug, Clone, Copy, PartialEq)]\n'
                  'enum Direction {\n'
                  '    N,\n'
                  '    E,\n'
                  '    S,\n'
                  '    W,\n'
                  '}\n'
                  '\n'
                  'impl Direction {\n'
                  '    fn turn_right(self) -> Direction {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn turn_left(self) -> Direction {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn opposite(self) -> Direction {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn from_char(c: char) -> Option<Direction> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn to_char(self) -> char {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut d = Direction::N;\n'
                 '    for _ in 0..5 {\n'
                 '        print!("{} ", d.to_char());\n'
                 '        d = d.turn_right();\n'
                 '    }\n'
                 '    println!();\n'
                 '    println!("{:?} {:?}", Direction::W.turn_left(), Direction::E.opposite());\n'
                 '    println!("{:?} {:?} {:?}", Direction::from_char(\'s\'), Direction::from_char(\'W\'), '
                 "Direction::from_char('x'));\n"
                 '}\n',
       'hint': 'Тип Copy: self по значению можно использовать повторно. opposite — два поворота направо.',
       'expected': ['N E S W N', 'S W', 'Some(S) Some(W) None']},
      {'id': 'r17-fix-match-ref',
       'mode': 'rust',
       'title': 'Исправьте: нельзя переместить из заимствованного',
       'statement': 'display_name возвращает прозвище, а если его нет — имя. Метод получает &Person, а match '
                    'пытается ПЕРЕМЕСТИТЬ строку из поля за ссылкой. Исправьте так, чтобы Person остался у '
                    'владельца.',
       'starter': 'struct Person {\n'
                  '    name: String,\n'
                  '    nickname: Option<String>,\n'
                  '}\n'
                  '\n'
                  'fn display_name(p: &Person) -> String {\n'
                  '    match p.nickname {\n'
                  '        Some(n) => n,\n'
                  '        None => p.name.clone(),\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a = Person { name: String::from("Александр"), nickname: Some(String::from("Саша")) '
                 '};\n'
                 '    let b = Person { name: String::from("Борис"), nickname: None };\n'
                 '    println!("{} {}", display_name(&a), display_name(&b));\n'
                 '    println!("{} {}", a.name, display_name(&a));\n'
                 '}\n',
       'hint': 'match &p.nickname даёт привязку n: &String; вернуть нужно владельца — n.clone().',
       'expected': ['Саша Борис', 'Александр Саша']},
      {'id': 'r17-match-mut',
       'mode': 'rust',
       'title': 'Изменение внутри Option',
       'statement': 'increment_if_some(o: &mut Option<i32>) — прибавить 1, если значение есть. take_or(o: '
                    '&mut Option<String>, default: &str) → String: забрать значение из o (в o остаётся None) '
                    'или вернуть default. append_default(o: &mut Option<Vec<i32>>, x) — добавить x в вектор; '
                    'если вектора ещё нет, создать.',
       'starter': 'fn increment_if_some(o: &mut Option<i32>) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn take_or(o: &mut Option<String>, default: &str) -> String {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn append_default(o: &mut Option<Vec<i32>>, x: i32) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut a = Some(5);\n'
                 '    let mut b: Option<i32> = None;\n'
                 '    increment_if_some(&mut a);\n'
                 '    increment_if_some(&mut b);\n'
                 '    println!("{:?} {:?}", a, b);\n'
                 '    let mut s = Some(String::from("hi"));\n'
                 '    println!("{} {} {:?}", take_or(&mut s, "def"), take_or(&mut s, "def"), s);\n'
                 '    let mut v = None;\n'
                 '    append_default(&mut v, 1);\n'
                 '    append_default(&mut v, 2);\n'
                 '    println!("{:?}", v);\n'
                 '}\n',
       'hint': 'if let Some(x) = o даёт x: &mut i32 (match ergonomics); o.take() и get_or_insert_with '
               'избавляют от лишних match.',
       'expected': ['Some(6) None', 'hi def None', 'Some([1, 2])']},
      {'id': 'r17-fix-move-in-match',
       'mode': 'rust',
       'title': 'Исправьте: значение переехало в match',
       'statement': 'describe сначала разбирает msg через match, а затем печатает его же через {:?}. match '
                    'перемещает строку из варианта, и msg после него недоступно. Исправьте минимальной '
                    'правкой (data нужны и текст, и сам msg).',
       'starter': 'fn describe(msg: Option<String>) -> String {\n'
                  '    let text = match msg {\n'
                  '        Some(s) => s,\n'
                  '        None => String::from("пусто"),\n'
                  '    };\n'
                  '    format!("{text} ({:?})", msg)\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", describe(Some(String::from("привет"))));\n'
                 '    println!("{}", describe(None));\n'
                 '}\n',
       'hint': 'match &msg разбирает ссылку: привязка s — &String, а msg остаётся целым.',
       'expected': ['привет (Some("привет"))', 'пусто (None)']},
      {'id': 'r17-expr-eval',
       'mode': 'rust',
       'title': 'Дерево выражений: eval',
       'statement': 'Expr — Num(i64), Add, Mul (по два Box<Expr>) и Neg (один). Напишите eval(e: &Expr) → '
                    'i64 рекурсивным match. Ссылка на Box<Expr> автоматически приводится к &Expr, так что '
                    'eval(a) работает.',
       'starter': 'enum Expr {\n'
                  '    Num(i64),\n'
                  '    Add(Box<Expr>, Box<Expr>),\n'
                  '    Mul(Box<Expr>, Box<Expr>),\n'
                  '    Neg(Box<Expr>),\n'
                  '}\n'
                  '\n'
                  'fn eval(e: &Expr) -> i64 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn num(n: i64) -> Box<Expr> {\n'
                 '    Box::new(Expr::Num(n))\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    let e = Expr::Add(num(2), Box::new(Expr::Mul(num(3), Box::new(Expr::Neg(num(4))))));\n'
                 '    println!("{}", eval(&e));\n'
                 '    println!("{}", eval(&Expr::Num(7)));\n'
                 '    println!("{}", eval(&Expr::Neg(Box::new(Expr::Neg(num(5))))));\n'
                 '}\n',
       'hint': 'Num(n) даёт n: &i64 — разыменуйте: *n. Для Neg: -eval(a).',
       'expected': ['-10', '7', '5']},
      {'id': 'r17-expr-show',
       'mode': 'rust',
       'title': 'Дерево выражений: show',
       'statement': 'Тот же Expr. Напишите show(e: &Expr) → String: Num → число; Add → «(A + B)»; Mul → «(A '
                    '* B)»; Neg → «-A».',
       'starter': 'enum Expr {\n'
                  '    Num(i64),\n'
                  '    Add(Box<Expr>, Box<Expr>),\n'
                  '    Mul(Box<Expr>, Box<Expr>),\n'
                  '    Neg(Box<Expr>),\n'
                  '}\n'
                  '\n'
                  'fn show(e: &Expr) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn num(n: i64) -> Box<Expr> {\n'
                 '    Box::new(Expr::Num(n))\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    let e = Expr::Add(num(2), Box::new(Expr::Mul(num(3), Box::new(Expr::Neg(num(4))))));\n'
                 '    println!("{}", show(&e));\n'
                 '    println!("{}", show(&Expr::Num(-7)));\n'
                 '}\n',
       'hint': 'Для вложенных частей вызывайте show(a), show(b) и вставляйте результаты в format!.',
       'expected': ['(2 + (3 * -4))', '-7']},
      {'id': 'r17-derive-ord',
       'mode': 'rust',
       'title': 'derive(Ord): порядок полей — порядок сравнения',
       'statement': 'Version { major, minor, patch } выводит PartialOrd и Ord, но поля записаны в '
                    'неправильном порядке, поэтому версии сортируются неверно. Исправьте определение '
                    'структуры, ничего больше не меняя: 1.2.9 < 1.10.0 < 2.0.0.',
       'starter': '#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]\n'
                  'struct Version {\n'
                  '    patch: u32,\n'
                  '    minor: u32,\n'
                  '    major: u32,\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![\n'
                 '        Version { major: 2, minor: 0, patch: 0 },\n'
                 '        Version { major: 1, minor: 10, patch: 0 },\n'
                 '        Version { major: 1, minor: 2, patch: 9 },\n'
                 '        Version { major: 1, minor: 2, patch: 10 },\n'
                 '    ];\n'
                 '    v.sort();\n'
                 '    for x in &v {\n'
                 '        print!("{}.{}.{} ", x.major, x.minor, x.patch);\n'
                 '    }\n'
                 '    println!();\n'
                 '    let m = v.iter().max().unwrap();\n'
                 '    println!("{}.{}.{} {}", m.major, m.minor, m.patch, v[0] < v[1]);\n'
                 '}\n',
       'hint': 'Лексикографическое сравнение идёт в порядке полей в определении: сначала major, потом minor, '
               'потом patch.',
       'expected': ['1.2.9 1.2.10 1.10.0 2.0.0', '2.0.0 true']},
      {'id': 'r17-default',
       'mode': 'rust',
       'title': 'Default вручную и ..Default::default()',
       'statement': 'Settings: retries: u32, timeout_ms: u64, verbose: bool, name: String, proxy: '
                    'Option<String>. Реализуйте Default: retries 3, timeout_ms 5000, verbose false, name '
                    '"app", proxy None. quiet() → Settings: все значения по умолчанию, кроме retries = 0 '
                    '(используйте ..Default::default()).',
       'starter': '#[derive(Debug)]\n'
                  'struct Settings {\n'
                  '    retries: u32,\n'
                  '    timeout_ms: u64,\n'
                  '    verbose: bool,\n'
                  '    name: String,\n'
                  '    proxy: Option<String>,\n'
                  '}\n'
                  '\n'
                  'impl Default for Settings {\n'
                  '    fn default() -> Settings {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn quiet() -> Settings {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", Settings::default());\n'
                 '    println!("{:?}", quiet());\n'
                 '    let s = Settings { verbose: true, ..Settings::default() };\n'
                 '    println!("{} {}", s.verbose, s.name);\n'
                 '}\n',
       'hint': 'Синтаксис обновления: Settings { retries: 0, ..Default::default() } берёт остальные поля из '
               'значения по умолчанию.',
       'expected': ['Settings { retries: 3, timeout_ms: 5000, verbose: false, name: "app", proxy: None }',
                    'Settings { retries: 0, timeout_ms: 5000, verbose: false, name: "app", proxy: None }',
                    'true app']},
      {'id': 'r17-builder',
       'mode': 'rust',
       'title': 'Строитель: цепочка методов с self',
       'statement': 'RequestBuilder собирает запрос. new(url), header(self, k, v) → Self (добавить '
                    'заголовок), timeout(self, t: u32) → Self, build(self) → Request. '
                    'Request::describe(&self) → String: «GET <url> timeout=<t> [k: v, k2: v2]»; без '
                    'заголовков — «[]». Таймаут по умолчанию 30. Методы принимают self по значению и '
                    'возвращают его обратно.',
       'starter': 'struct Request {\n'
                  '    url: String,\n'
                  '    headers: Vec<(String, String)>,\n'
                  '    timeout: u32,\n'
                  '}\n'
                  '\n'
                  'struct RequestBuilder {\n'
                  '    url: String,\n'
                  '    headers: Vec<(String, String)>,\n'
                  '    timeout: u32,\n'
                  '}\n'
                  '\n'
                  'impl RequestBuilder {\n'
                  '    fn new(url: &str) -> RequestBuilder {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn header(mut self, k: &str, v: &str) -> RequestBuilder {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn timeout(mut self, t: u32) -> RequestBuilder {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn build(self) -> Request {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Request {\n'
                  '    fn describe(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let r = RequestBuilder::new("http://a.b/")\n'
                 '        .header("Accept", "text/html")\n'
                 '        .timeout(5)\n'
                 '        .header("X-Id", "7")\n'
                 '        .build();\n'
                 '    println!("{}", r.describe());\n'
                 '    println!("{}", RequestBuilder::new("/x").build().describe());\n'
                 '}\n',
       'hint': 'Каждый метод изменяет self и возвращает его: self.headers.push(...); self.',
       'expected': ['GET http://a.b/ timeout=5 [Accept: text/html, X-Id: 7]', 'GET /x timeout=30 []']},
      {'id': 'r17-inventory',
       'mode': 'rust',
       'title': 'Инвентарь: &, &mut и Option<&T>',
       'statement': 'Item { name: String, qty: u32, price_cents: u64 }. total_value(items: &[Item]) → u64 — '
                    'сумма qty × price. cheapest(items: &[Item]) → Option<&Item> — позиция с наименьшей '
                    'ценой за штуку (первая из равных; пустой список → None). restock(items: &mut [Item], '
                    'name: &str, n: u32) → bool — увеличить qty позиции с таким именем, true если нашли.',
       'starter': 'struct Item {\n'
                  '    name: String,\n'
                  '    qty: u32,\n'
                  '    price_cents: u64,\n'
                  '}\n'
                  '\n'
                  'fn total_value(items: &[Item]) -> u64 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn cheapest(items: &[Item]) -> Option<&Item> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn restock(items: &mut [Item], name: &str, n: u32) -> bool {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut items = vec![\n'
                 '        Item { name: "pen".into(), qty: 10, price_cents: 150 },\n'
                 '        Item { name: "book".into(), qty: 2, price_cents: 1200 },\n'
                 '        Item { name: "clip".into(), qty: 100, price_cents: 5 },\n'
                 '        Item { name: "tape".into(), qty: 1, price_cents: 5 },\n'
                 '    ];\n'
                 '    println!("{}", total_value(&items));\n'
                 '    println!("{}", cheapest(&items).map(|i| i.name.as_str()).unwrap_or("-"));\n'
                 '    println!("{} {}", restock(&mut items, "book", 3), restock(&mut items, "gum", 1));\n'
                 '    println!("{} {}", items[1].qty, total_value(&items));\n'
                 '    println!("{}", cheapest(&[]).is_none());\n'
                 '}\n',
       'hint': 'Для restock: for it in items.iter_mut() даёт &mut Item; return true прямо из цикла.',
       'expected': ['4405', 'clip', 'true false', '5 8005', 'true']},
      {'id': 'r17-matrix',
       'mode': 'rust',
       'title': 'Матрица в одном Vec: row-major',
       'statement': 'Matrix { rows, cols, data: Vec<i32> } хранит элементы построчно: индекс (r, c) → r * '
                    'cols + c (как двумерный массив в памяти). new(rows, cols) — нули; get(&self, r, c) → '
                    'Option<i32> (None вне границ); set(&mut self, r, c, v) → bool (false вне границ); '
                    'transpose(&self) → Matrix.',
       'starter': 'struct Matrix {\n'
                  '    rows: usize,\n'
                  '    cols: usize,\n'
                  '    data: Vec<i32>,\n'
                  '}\n'
                  '\n'
                  'impl Matrix {\n'
                  '    fn new(rows: usize, cols: usize) -> Matrix {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn get(&self, r: usize, c: usize) -> Option<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn set(&mut self, r: usize, c: usize, v: i32) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn transpose(&self) -> Matrix {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut m = Matrix::new(2, 3);\n'
                 '    let mut k = 1;\n'
                 '    for r in 0..2 {\n'
                 '        for c in 0..3 {\n'
                 '            m.set(r, c, k);\n'
                 '            k += 1;\n'
                 '        }\n'
                 '    }\n'
                 '    println!("{:?}", m.data);\n'
                 '    let t = m.transpose();\n'
                 '    println!("{} {} {:?}", t.rows, t.cols, t.data);\n'
                 '    println!("{:?} {:?} {}", m.get(1, 2), m.get(2, 0), m.set(0, 3, 1));\n'
                 '}\n',
       'hint': 'Индекс в одномерном Vec: r * cols + c; при транспонировании у новой матрицы строк столько, '
               'сколько столбцов у старой.',
       'expected': ['[1, 2, 3, 4, 5, 6]', '3 2 [1, 4, 2, 5, 3, 6]', 'Some(6) None false']},
      {'id': 'r17-value-tree',
       'mode': 'rust',
       'title': 'Размеченное объединение: Value',
       'statement': 'Value — Int(i64), Float(f64), Text(String) или List(Vec<Value>). total(&Value) → f64 — '
                    'сумма всех чисел (в том числе вложенных в списки; текст не считается). depth(&Value) → '
                    'usize: 0 для не списка, для списка — 1 + наибольшая глубина элементов (пустой список — '
                    '1). texts(&Value) → Vec<String> — все строки в порядке обхода.',
       'starter': 'enum Value {\n'
                  '    Int(i64),\n'
                  '    Float(f64),\n'
                  '    Text(String),\n'
                  '    List(Vec<Value>),\n'
                  '}\n'
                  '\n'
                  'fn total(v: &Value) -> f64 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn depth(v: &Value) -> usize {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn texts(v: &Value) -> Vec<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    use Value::*;\n'
                 '    let v = List(vec![\n'
                 '        Int(2),\n'
                 '        Text("a".into()),\n'
                 '        List(vec![Float(1.5), List(vec![Text("b".into()), Int(10)])]),\n'
                 '        Text("c".into()),\n'
                 '    ]);\n'
                 '    println!("{} {} {:?}", total(&v), depth(&v), texts(&v));\n'
                 '    println!("{} {} {:?}", total(&Int(5)), depth(&List(vec![])), texts(&Float(1.0)));\n'
                 '}\n',
       'hint': 'Список обрабатывается рекурсивно: items.iter().map(total).sum(); max() по пустому итератору '
               'даёт None — подойдёт unwrap_or(0).',
       'expected': ['13.5 3 ["a", "b", "c"]', '5 1 []']},
      {'id': 'r17-json',
       'mode': 'rust',
       'title': 'Рендер JSON из enum',
       'statement': 'Json — Null, Bool, Num(f64), Str(String), Arr(Vec<Json>), Obj(Vec<(String, Json)>). '
                    'render(&self) → String: компактный JSON без пробелов: null, true/false, число как в {}, '
                    'строка в двойных кавычках (экранируйте \\" и \\\\), массив [a,b], объект {"k":v,...} в '
                    'порядке вектора.',
       'starter': 'enum Json {\n'
                  '    Null,\n'
                  '    Bool(bool),\n'
                  '    Num(f64),\n'
                  '    Str(String),\n'
                  '    Arr(Vec<Json>),\n'
                  '    Obj(Vec<(String, Json)>),\n'
                  '}\n'
                  '\n'
                  'impl Json {\n'
                  '    fn render(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    use Json::*;\n'
                 '    let j = Obj(vec![\n'
                 '        ("name".to_string(), Str("Анна \\"Ню\\"".to_string())),\n'
                 '        ("age".to_string(), Num(30.0)),\n'
                 '        ("pi".to_string(), Num(3.5)),\n'
                 '        ("tags".to_string(), Arr(vec![Bool(true), Null, Str("a\\\\b".to_string())])),\n'
                 '        ("empty".to_string(), Arr(vec![])),\n'
                 '    ]);\n'
                 '    println!("{}", j.render());\n'
                 '    println!("{}", Null.render());\n'
                 '}\n',
       'hint': 'Вспомогательная функция quote(s) экранирует символы по одному; в format! фигурные скобки '
               'удваивают: {{ и }}.',
       'expected': ['{"name":"Анна \\"Ню\\"","age":30,"pi":3.5,"tags":[true,null,"a\\\\b"],"empty":[]}',
                    'null']},
      {'id': 'r17-event-log',
       'mode': 'rust',
       'title': 'Журнал событий: struct-варианты',
       'statement': 'Event — Login { user }, Logout { user }, Purchase { user, cents: u32 } '
                    '(struct-варианты). summarize(events: &[Event]) → (usize, u32, Vec<String>): число '
                    'входов, сумма покупок в центах и имена пользователей, которые остались в системе (вошли '
                    'и не вышли) — в порядке последнего входа без выхода.',
       'starter': 'enum Event {\n'
                  '    Login { user: String },\n'
                  '    Logout { user: String },\n'
                  '    Purchase { user: String, cents: u32 },\n'
                  '}\n'
                  '\n'
                  'fn summarize(events: &[Event]) -> (usize, u32, Vec<String>) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let ev = vec![\n'
                 '        Event::Login { user: "ann".into() },\n'
                 '        Event::Login { user: "bob".into() },\n'
                 '        Event::Purchase { user: "ann".into(), cents: 500 },\n'
                 '        Event::Logout { user: "ann".into() },\n'
                 '        Event::Login { user: "cat".into() },\n'
                 '        Event::Purchase { user: "cat".into(), cents: 250 },\n'
                 '        Event::Logout { user: "zed".into() },\n'
                 '    ];\n'
                 '    println!("{:?}", summarize(&ev));\n'
                 '    println!("{:?}", summarize(&[]));\n'
                 '}\n',
       'hint': 'Образец Event::Purchase { cents, .. } берёт нужное поле и пропускает остальные.',
       'expected': ['(3, 750, ["bob", "cat"])', '(0, 0, [])']}]}
