"""Задачи книги «Изучаем Rust»: глава 8 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {8: [{'id': 'r8-struct-create',
      'mode': 'rust',
      'title': 'Первая структура',
      'statement': 'Объявите структуру Point с полями x и y типа i32. Создайте точку (3, -4) и напечатайте '
                   '«x=3 y=-4».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'x=3 y=-4',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'struct Point { x: i32, y: i32 }; Point { x: 3, y: -4 }.',
      'standalone': True,
      'expected': ['x=3 y=-4']},
     {'id': 'r8-struct-mut',
      'mode': 'rust',
      'title': 'Меняем поле',
      'statement': 'Объявите структуру Counter { value: u32 }, создайте изменяемый экземпляр со значением 0 '
                   'и трижды увеличьте value на 5. Напечатайте «15».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '15',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'let mut c — иначе поле не изменить.',
      'standalone': True,
      'expected': ['15']},
     {'id': 'r8-struct-debug',
      'mode': 'rust',
      'title': 'Печать через Debug',
      'statement': 'Структуре Book { title: &str, pages: u32 } добавьте #[derive(Debug)] и напечатайте '
                   'экземпляр {:?} и красиво {:#?}. Для книги «Rust», 500 страниц: сначала «Book { title: '
                   '"Rust", pages: 500 }», затем многострочный вид.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'Book { title: "Rust", pages: 500 }\n'
                   'Book {\n'
                   '    title: "Rust",\n'
                   '    pages: 500,\n'
                   '}',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': "#[derive(Debug)] над структурой; поле-ссылка требует 'static: &'static str.",
      'standalone': True,
      'expected': ['Book { title: "Rust", pages: 500 }',
                   'Book {',
                   '    title: "Rust",',
                   '    pages: 500,',
                   '}']},
     {'id': 'r8-struct-shorthand',
      'mode': 'rust',
      'title': 'Сокращённая инициализация',
      'statement': 'Напишите функцию make_user(name: &str, age: u32) -> User, где User { name: String, age: '
                   'u32 }, используя сокращённую запись (name и age совпадают с полями; для name нужно '
                   'name.to_string()). Напечатайте «Аня 30».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'Аня 30',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'let name = name.to_string(); затем User { name, age }.',
      'standalone': True,
      'expected': ['Аня 30']},
     {'id': 'r8-struct-update',
      'mode': 'rust',
      'title': 'Обновление структуры',
      'statement': 'Config { width, height, title: &\'static str }. Создайте base (800, 600, "окно"), затем '
                   'big — копия с width = 1920 через ..base. Напечатайте «1920x600 окно».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '1920x600 окно',
      'starter': 'fn main() {\n    // ваш код\n}\n',
      'driver': '',
      'hint': 'Config { width: 1920, ..base }',
      'standalone': True,
      'expected': ['1920x600 окно']},
     {'id': 'r8-impl-area',
      'mode': 'rust',
      'title': 'Метод area',
      'statement': 'Для структуры Rect { w: u32, h: u32 } напишите методы area(&self) -> u32 (площадь) и '
                   'perimeter(&self) -> u32 (периметр).',
      'starter': 'struct Rect {\n'
                 '    w: u32,\n'
                 '    h: u32,\n'
                 '}\n'
                 '\n'
                 'impl Rect {\n'
                 '    fn area(&self) -> u32 {\n'
                 '        todo!()\n'
                 '    }\n'
                 '    fn perimeter(&self) -> u32 {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let r = Rect { w: 3, h: 5 };\n'
                '    println!("{} {}", r.area(), r.perimeter());\n'
                '    let s = Rect { w: 10, h: 10 };\n'
                '    println!("{} {}", s.area(), s.perimeter());\n'
                '}\n',
      'hint': 'self.w * self.h; 2 * (self.w + self.h)',
      'expected': ['15 16', '100 40']},
     {'id': 'r8-impl-new',
      'mode': 'rust',
      'title': 'Конструктор new',
      'statement': 'Добавьте структуре Circle { r: f64 } ассоциированную функцию new(r: f64) -> Circle и '
                   'метод area(&self) -> f64 (π ≈ 3.14159).',
      'starter': 'struct Circle {\n'
                 '    r: f64,\n'
                 '}\n'
                 '\n'
                 'impl Circle {\n'
                 '    fn new(r: f64) -> Circle {\n'
                 '        todo!()\n'
                 '    }\n'
                 '    fn area(&self) -> f64 {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let c = Circle::new(2.0);\n'
                '    println!("{:.3}", c.area());\n'
                '    println!("{:.1}", Circle::new(1.0).area());\n'
                '}\n',
      'hint': 'Circle::new(r) — функция без self.',
      'expected': ['12.566', '3.1']},
     {'id': 'r8-impl-mut-self',
      'mode': 'rust',
      'title': 'Счётчик с методами',
      'statement': 'Структуре Counter { n: u32 } добавьте методы new() -> Counter (n = 0), inc(&mut self), '
                   'add(&mut self, k: u32) и get(&self) -> u32.',
      'starter': 'struct Counter {\n'
                 '    n: u32,\n'
                 '}\n'
                 '\n'
                 'impl Counter {\n'
                 '    fn new() -> Counter {\n'
                 '        todo!()\n'
                 '    }\n'
                 '    fn inc(&mut self) {\n'
                 '        todo!()\n'
                 '    }\n'
                 '    fn add(&mut self, k: u32) {\n'
                 '        todo!()\n'
                 '    }\n'
                 '    fn get(&self) -> u32 {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut c = Counter::new();\n'
                '    c.inc();\n'
                '    c.inc();\n'
                '    c.add(10);\n'
                '    println!("{}", c.get());\n'
                '}\n',
      'hint': '&mut self позволяет менять self.n.',
      'expected': ['12']},
     {'id': 'r8-bank-account',
      'mode': 'rust',
      'title': 'Банковский счёт',
      'statement': 'Реализуйте Account { balance: i64 }: new(), deposit(&mut self, x: i64), withdraw(&mut '
                   'self, x: i64) -> bool (false и без изменений, если средств не хватает; true и списание — '
                   'иначе), balance(&self) -> i64.',
      'starter': 'struct Account {\n'
                 '    balance: i64,\n'
                 '}\n'
                 '\n'
                 'impl Account {\n'
                 '    fn new() -> Account {\n'
                 '        todo!()\n'
                 '    }\n'
                 '    fn deposit(&mut self, x: i64) {\n'
                 '        todo!()\n'
                 '    }\n'
                 '    fn withdraw(&mut self, x: i64) -> bool {\n'
                 '        todo!()\n'
                 '    }\n'
                 '    fn balance(&self) -> i64 {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut a = Account::new();\n'
                '    a.deposit(100);\n'
                '    println!("{}", a.withdraw(30));\n'
                '    println!("{}", a.withdraw(100));\n'
                '    println!("{}", a.balance());\n'
                '}\n',
      'hint': 'Проверка баланса внутри withdraw, возвращаем bool.',
      'expected': ['true', 'false', '70']},
     {'id': 'r8-point-distance',
      'mode': 'rust',
      'title': 'Расстояние между точками',
      'statement': 'У структуры Point { x: f64, y: f64 } напишите метод dist(&self, other: &Point) -> f64 — '
                   'евклидово расстояние.',
      'starter': 'struct Point {\n'
                 '    x: f64,\n'
                 '    y: f64,\n'
                 '}\n'
                 '\n'
                 'impl Point {\n'
                 '    fn dist(&self, other: &Point) -> f64 {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let a = Point { x: 0.0, y: 0.0 };\n'
                '    let b = Point { x: 3.0, y: 4.0 };\n'
                '    println!("{}", a.dist(&b));\n'
                '    println!("{}", b.dist(&a));\n'
                '    println!("{}", a.dist(&a));\n'
                '}\n',
      'hint': 'other передаётся ссылкой: a.dist(&b).',
      'expected': ['5', '5', '0']},
     {'id': 'r8-tuple-struct',
      'mode': 'rust',
      'title': 'Кортежная структура',
      'statement': 'Объявите структуру Meters(f64) и функцию to_feet(m: Meters) -> f64: перевод метров в '
                   'футы (1 м = 3.28084 фута).',
      'starter': 'struct Meters(f64);\n\nfn to_feet(m: Meters) -> f64 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:.3}", to_feet(Meters(10.0)));\n'
                '    println!("{:.3}", to_feet(Meters(0.5)));\n'
                '}\n',
      'hint': 'Доступ к полю кортежной структуры — m.0.',
      'expected': ['32.808', '1.640']},
     {'id': 'r8-color-struct',
      'mode': 'rust',
      'title': 'Цвет и яркость',
      'statement': 'Структура Color(u8, u8, u8) — RGB. Напишите функцию brightness(c: &Color) -> u32: '
                   'среднее трёх компонент (целое деление на 3).',
      'starter': 'struct Color(u8, u8, u8);\n\nfn brightness(c: &Color) -> u32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", brightness(&Color(255, 0, 0)));\n'
                '    println!("{}", brightness(&Color(255, 255, 255)));\n'
                '    println!("{}", brightness(&Color(10, 20, 31)));\n'
                '}\n',
      'hint': 'Сложите как u32, иначе u8 переполнится.',
      'expected': ['85', '255', '20']},
     {'id': 'r8-enum-basic',
      'mode': 'rust',
      'title': 'Направления',
      'statement': 'Enum Direction { Up, Down, Left, Right } и функция opposite(d: Direction) -> Direction, '
                   'возвращающая противоположное направление. Для вывода добавьте derive(Debug).',
      'starter': '#[derive(Debug)]\n'
                 'enum Direction {\n'
                 '    Up,\n'
                 '    Down,\n'
                 '    Left,\n'
                 '    Right,\n'
                 '}\n'
                 '\n'
                 'fn opposite(d: Direction) -> Direction {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", opposite(Direction::Up));\n'
                '    println!("{:?}", opposite(Direction::Left));\n'
                '    println!("{:?}", opposite(Direction::Right));\n'
                '}\n',
      'hint': 'match по четырём вариантам.',
      'expected': ['Down', 'Right', 'Left']},
     {'id': 'r8-enum-coin',
      'mode': 'rust',
      'title': 'Монеты',
      'statement': 'Enum Coin { Penny, Nickel, Dime, Quarter } и функция value(c: &Coin) -> u32 в центах: 1, '
                   '5, 10, 25.',
      'starter': 'enum Coin {\n'
                 '    Penny,\n'
                 '    Nickel,\n'
                 '    Dime,\n'
                 '    Quarter,\n'
                 '}\n'
                 '\n'
                 'fn value(c: &Coin) -> u32 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let coins = [Coin::Quarter, Coin::Dime, Coin::Penny, Coin::Penny];\n'
                '    let mut total = 0;\n'
                '    for c in &coins {\n'
                '        total += value(c);\n'
                '    }\n'
                '    println!("{}", total);\n'
                '}\n',
      'hint': 'match c { Coin::Penny => 1, … }',
      'expected': ['37']},
     {'id': 'r8-enum-shape',
      'mode': 'rust',
      'title': 'Фигуры',
      'statement': 'Enum Shape { Circle(f64), Rect(f64, f64), Square(f64) } и функция area(s: &Shape) -> f64 '
                   '(π ≈ 3.14159).',
      'starter': 'enum Shape {\n'
                 '    Circle(f64),\n'
                 '    Rect(f64, f64),\n'
                 '    Square(f64),\n'
                 '}\n'
                 '\n'
                 'fn area(s: &Shape) -> f64 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{:.3}", area(&Shape::Circle(2.0)));\n'
                '    println!("{}", area(&Shape::Rect(3.0, 4.5)));\n'
                '    println!("{}", area(&Shape::Square(5.0)));\n'
                '}\n',
      'hint': 'В образце сразу достаём данные: Shape::Rect(w, h).',
      'expected': ['12.566', '13.5', '25']},
     {'id': 'r8-enum-method',
      'mode': 'rust',
      'title': 'Метод у enum',
      'statement': 'Enum Light { Red, Yellow, Green } с методом next(&self) -> Light: цикл Red → Green → '
                   'Yellow → Red. Derive(Debug).',
      'starter': '#[derive(Debug)]\n'
                 'enum Light {\n'
                 '    Red,\n'
                 '    Yellow,\n'
                 '    Green,\n'
                 '}\n'
                 '\n'
                 'impl Light {\n'
                 '    fn next(&self) -> Light {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut l = Light::Red;\n'
                '    for _ in 0..4 {\n'
                '        print!("{:?} ", l);\n'
                '        l = l.next();\n'
                '    }\n'
                '    println!();\n'
                '}\n',
      'hint': 'Методы у enum пишутся в impl, как у struct.',
      'expected': ['Red Green Yellow Red']},
     {'id': 'r8-option-find',
      'mode': 'rust',
      'title': 'Поиск с Option',
      'statement': 'Напишите функцию find(v: &[i32], x: i32) -> Option<usize>: индекс первого вхождения x '
                   'или None.',
      'starter': 'fn find(v: &[i32], x: i32) -> Option<usize> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", find(&[5, 7, 9, 7], 7));\n'
                '    println!("{:?}", find(&[5, 7, 9], 4));\n'
                '    println!("{:?}", find(&[], 1));\n'
                '}\n',
      'hint': 'return Some(i) внутри цикла, в конце None.',
      'expected': ['Some(1)', 'None', 'None']},
     {'id': 'r8-option-divide',
      'mode': 'rust',
      'title': 'Безопасное деление',
      'statement': 'Напишите функцию safe_div(a: i32, b: i32) -> Option<i32>: None при b == 0, иначе '
                   'частное.',
      'starter': 'fn safe_div(a: i32, b: i32) -> Option<i32> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", safe_div(10, 2));\n'
                '    println!("{:?}", safe_div(7, 0));\n'
                '    println!("{:?}", safe_div(-9, 3));\n'
                '}\n',
      'hint': 'Ветки if возвращают None и Some(…).',
      'expected': ['Some(5)', 'None', 'Some(-3)']},
     {'id': 'r8-option-unwrap-or',
      'mode': 'rust',
      'title': 'unwrap_or',
      'statement': 'Напишите функцию first_or(v: &[i32], default: i32) -> i32: первый элемент или default, '
                   'если срез пуст. Используйте v.first() и unwrap_or.',
      'starter': 'fn first_or(v: &[i32], default: i32) -> i32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", first_or(&[4, 5], 0));\n'
                '    println!("{}", first_or(&[], -1));\n'
                '}\n',
      'hint': 'v.first() даёт Option<&i32>; unwrap_or(&default), затем звёздочка.',
      'expected': ['4', '-1']},
     {'id': 'r8-option-match',
      'mode': 'rust',
      'title': 'match по Option',
      'statement': 'Напишите функцию describe(x: Option<i32>) -> String: «нет значения» для None, «ноль» для '
                   'Some(0), «число N» (N — значение) иначе.',
      'starter': 'fn describe(x: Option<i32>) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", describe(None));\n'
                '    println!("{}", describe(Some(0)));\n'
                '    println!("{}", describe(Some(42)));\n'
                '}\n',
      'hint': 'Образец Some(0) — до общего Some(n).',
      'expected': ['нет значения', 'ноль', 'число 42']},
     {'id': 'r8-if-let',
      'mode': 'rust',
      'title': 'if let',
      'statement': 'Напишите функцию print_first(v: &[&str]): если срез не пуст — печатает «первый: …», '
                   'иначе «пусто». Используйте if let Some(x) = v.first().',
      'starter': 'fn print_first(v: &[&str]) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n    print_first(&["a", "b"]);\n    print_first(&[]);\n}\n',
      'hint': 'if let Some(x) = … { } else { }',
      'expected': ['первый: a', 'пусто']},
     {'id': 'r8-result-parse',
      'mode': 'rust',
      'title': 'Result из parse',
      'statement': 'Напишите функцию to_num(s: &str) -> Result<i32, String>: Ok(число), если строка — целое, '
                   'иначе Err("не число: <s>").',
      'starter': 'fn to_num(s: &str) -> Result<i32, String> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", to_num("42"));\n'
                '    println!("{:?}", to_num("abc"));\n'
                '    println!("{:?}", to_num("-7"));\n'
                '}\n',
      'hint': 'match s.parse::<i32>() { Ok(n) => …, Err(_) => … }',
      'expected': ['Ok(42)', 'Err("не число: abc")', 'Ok(-7)']},
     {'id': 'r8-result-div',
      'mode': 'rust',
      'title': 'Деление с ошибкой',
      'statement': 'Напишите функцию divide(a: f64, b: f64) -> Result<f64, String>: Err("деление на ноль"), '
                   'если b == 0.0, иначе Ok(частное).',
      'starter': 'fn divide(a: f64, b: f64) -> Result<f64, String> {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", divide(1.0, 4.0));\n'
                '    println!("{:?}", divide(5.0, 0.0));\n'
                '}\n',
      'hint': 'Err(String::from("…")) и Ok(a / b)',
      'expected': ['Ok(0.25)', 'Err("деление на ноль")']},
     {'id': 'r8-struct-vec',
      'mode': 'rust',
      'title': 'Вектор структур',
      'statement': 'Структура Student { name: String, grade: u32 }. Напишите функцию best(students: '
                   '&[Student]) -> &str: имя студента с максимальной оценкой (первого из лучших). Список не '
                   'пуст.',
      'starter': 'struct Student {\n'
                 '    name: String,\n'
                 '    grade: u32,\n'
                 '}\n'
                 '\n'
                 'fn best(students: &[Student]) -> &str {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let list = vec![\n'
                '        Student { name: String::from("Аня"), grade: 4 },\n'
                '        Student { name: String::from("Боря"), grade: 5 },\n'
                '        Student { name: String::from("Вера"), grade: 5 },\n'
                '    ];\n'
                '    println!("{}", best(&list));\n'
                '}\n',
      'hint': 'Храните ссылку top на лучшего студента.',
      'expected': ['Боря']},
     {'id': 'r8-inventory',
      'mode': 'rust',
      'title': 'Склад',
      'statement': 'Структура Item { name: String, qty: u32 }. Функция total(items: &[Item]) -> u32 — '
                   'суммарное количество, и функция find_qty(items: &[Item], name: &str) -> Option<u32>.',
      'starter': 'struct Item {\n'
                 '    name: String,\n'
                 '    qty: u32,\n'
                 '}\n'
                 '\n'
                 'fn total(items: &[Item]) -> u32 {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn find_qty(items: &[Item], name: &str) -> Option<u32> {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let items = vec![\n'
                '        Item { name: String::from("гвозди"), qty: 120 },\n'
                '        Item { name: String::from("болты"), qty: 45 },\n'
                '    ];\n'
                '    println!("{}", total(&items));\n'
                '    println!("{:?}", find_qty(&items, "болты"));\n'
                '    println!("{:?}", find_qty(&items, "гайки"));\n'
                '}\n',
      'hint': 'it.name == name — сравнение String и &str работает.',
      'expected': ['165', 'Some(45)', 'None']},
     {'id': 'r8-traffic-fsm',
      'mode': 'rust',
      'title': 'Автомат статусов заказа',
      'statement': 'Enum Status { New, Paid, Shipped, Done }. Метод advance(&self) -> Status переводит в '
                   'следующий статус (Done остаётся Done), а is_final(&self) -> bool истинен только для '
                   'Done. Derive(Debug).',
      'starter': '#[derive(Debug)]\n'
                 'enum Status {\n'
                 '    New,\n'
                 '    Paid,\n'
                 '    Shipped,\n'
                 '    Done,\n'
                 '}\n'
                 '\n'
                 'impl Status {\n'
                 '    fn advance(&self) -> Status {\n'
                 '        todo!()\n'
                 '    }\n'
                 '    fn is_final(&self) -> bool {\n'
                 '        todo!()\n'
                 '    }\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    let mut s = Status::New;\n'
                '    while !s.is_final() {\n'
                '        print!("{:?} ", s);\n'
                '        s = s.advance();\n'
                '    }\n'
                '    println!("{:?}", s);\n'
                '}\n',
      'hint': 'matches!(self, Status::Done) — короткая проверка варианта.',
      'expected': ['New Paid Shipped Done']},
     {'id': 'r8-fix-mut-struct',
      'mode': 'rust',
      'title': 'Исправьте: структура без mut',
      'statement': 'Программа не собирается: поле меняется у неизменяемой структуры. Исправьте объявление; '
                   'результат «11».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '11',
      'starter': 'struct S {\n'
                 '    n: i32,\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    let s = S { n: 10 };\n'
                 '    s.n += 1;\n'
                 '    println!("{}", s.n);\n'
                 '}\n',
      'driver': '',
      'hint': 'Добавьте mut к переменной s.',
      'standalone': True,
      'expected': ['11']},
     {'id': 'r8-fix-missing-variant',
      'mode': 'rust',
      'title': 'Исправьте: match без всех вариантов',
      'statement': 'match не покрывает вариант Blue. Допишите ветку так, чтобы вывод был «синий» для '
                   'Color::Blue.\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   'синий',
      'starter': 'enum Color {\n'
                 '    Red,\n'
                 '    Green,\n'
                 '    Blue,\n'
                 '}\n'
                 '\n'
                 "fn name(c: Color) -> &'static str {\n"
                 '    match c {\n'
                 '        Color::Red => "красный",\n'
                 '        Color::Green => "зелёный",\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    println!("{}", name(Color::Blue));\n'
                 '}\n',
      'driver': '',
      'hint': 'Добавьте Color::Blue => "синий",',
      'standalone': True,
      'expected': ['синий']},
     {'id': 'r8-fix-self',
      'mode': 'rust',
      'title': 'Исправьте: метод без &mut self',
      'statement': 'Метод inc должен менять поле, но объявлен с &self. Исправьте сигнатуру; результат «2».\n'
                   '\n'
                   'Ожидаемый вывод:\n'
                   '2',
      'starter': 'struct C {\n'
                 '    n: u32,\n'
                 '}\n'
                 '\n'
                 'impl C {\n'
                 '    fn inc(&self) {\n'
                 '        self.n += 1;\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    let mut c = C { n: 1 };\n'
                 '    c.inc();\n'
                 '    println!("{}", c.n);\n'
                 '}\n',
      'driver': '',
      'hint': 'Замените &self на &mut self.',
      'standalone': True,
      'expected': ['2']},
     {'id': 'r8-vec-of-enum',
      'mode': 'rust',
      'title': 'Список покупок',
      'statement': 'Enum Item { Apple(u32), Milk(f64) } (число яблок и литры молока). Функция '
                   'describe(items: &[Item]) -> String: для каждого элемента «N яблок» или «X л молока», '
                   'через «; ».',
      'starter': 'enum Item {\n'
                 '    Apple(u32),\n'
                 '    Milk(f64),\n'
                 '}\n'
                 '\n'
                 'fn describe(items: &[Item]) -> String {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", describe(&[Item::Apple(3), Item::Milk(1.5)]));\n'
                '    println!("{}", describe(&[]));\n'
                '    println!("{}", describe(&[Item::Milk(2.0)]));\n'
                '}\n',
      'hint': 'Соберите строки в Vec<String> и склейте join("; ").',
      'expected': ['3 яблок; 1.5 л молока', '', '2 л молока']}]}
