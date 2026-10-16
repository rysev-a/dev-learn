"""Задачи книги «Изучаем Rust»: глава 13 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {13: [{'id': 'r13-class-basic',
       'mode': 'rust',
       'title': 'Класс → struct',
       'statement': 'Python: class Dog с name и методом speak() → «<имя>: гав!». Напишите структуру Dog { '
                    'name: String }, функцию new(name: &str) -> Dog и метод speak(&self) -> String.',
       'starter': 'struct Dog {\n'
                  '    name: String,\n'
                  '}\n'
                  '\n'
                  'impl Dog {\n'
                  '    fn new(name: &str) -> Dog {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn speak(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let d = Dog::new("Бобик");\n'
                 '    println!("{}", d.speak());\n'
                 '    println!("{}", Dog::new("Шарик").speak());\n'
                 '}\n',
       'hint': 'format!("{}: гав!", self.name)',
       'expected': ['Бобик: гав!', 'Шарик: гав!']},
      {'id': 'r13-property',
       'mode': 'rust',
       'title': 'property',
       'statement': 'Python: @property celsius / fahrenheit. Структура Temp { celsius: f64 } с методом '
                    'fahrenheit(&self) -> f64 (c · 9/5 + 32) и set_fahrenheit(&mut self, f: f64) (обновляет '
                    'celsius).',
       'starter': 'struct Temp {\n'
                  '    celsius: f64,\n'
                  '}\n'
                  '\n'
                  'impl Temp {\n'
                  '    fn fahrenheit(&self) -> f64 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn set_fahrenheit(&mut self, f: f64) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut t = Temp { celsius: 100.0 };\n'
                 '    println!("{}", t.fahrenheit());\n'
                 '    t.set_fahrenheit(32.0);\n'
                 '    println!("{}", t.celsius);\n'
                 '    t.set_fahrenheit(212.0);\n'
                 '    println!("{}", t.celsius);\n'
                 '}\n',
       'hint': 'Формулы: c·9/5+32 и (f−32)·5/9.',
       'expected': ['212', '0', '100']},
      {'id': 'r13-classmethod',
       'mode': 'rust',
       'title': 'classmethod',
       'statement': 'Python: Color.from_hex("#ff8000"). Структура Color { r: u8, g: u8, b: u8 } и '
                    'ассоциированная функция from_hex(s: &str) -> Color для строки вида «#rrggbb» '
                    '(используйте u8::from_str_radix(&s[1..3], 16).unwrap()).',
       'starter': 'struct Color {\n'
                  '    r: u8,\n'
                  '    g: u8,\n'
                  '    b: u8,\n'
                  '}\n'
                  '\n'
                  'impl Color {\n'
                  '    fn from_hex(s: &str) -> Color {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let c = Color::from_hex("#ff8000");\n'
                 '    println!("{} {} {}", c.r, c.g, c.b);\n'
                 '    let d = Color::from_hex("#000a0b");\n'
                 '    println!("{} {} {}", d.r, d.g, d.b);\n'
                 '}\n',
       'hint': 'u8::from_str_radix(&s[1..3], 16).unwrap()',
       'expected': ['255 128 0', '0 10 11']},
      {'id': 'r13-composition',
       'mode': 'rust',
       'title': 'Композиция вместо наследования',
       'statement': 'Python: class Employee(Person). Структуры Person { name: String } и Employee { person: '
                    'Person, salary: u32 }; у Employee метод describe(&self) -> String: «<имя> зарабатывает '
                    '<salary>».',
       'starter': 'struct Person {\n'
                  '    name: String,\n'
                  '}\n'
                  '\n'
                  'struct Employee {\n'
                  '    person: Person,\n'
                  '    salary: u32,\n'
                  '}\n'
                  '\n'
                  'impl Employee {\n'
                  '    fn describe(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let e = Employee { person: Person { name: String::from("Аня") }, salary: 120 };\n'
                 '    println!("{}", e.describe());\n'
                 '}\n',
       'hint': 'self.person.name — поле вложенной структуры.',
       'expected': ['Аня зарабатывает 120']},
      {'id': 'r13-trait-basic',
       'mode': 'rust',
       'title': 'Первый трейт',
       'statement': 'Трейт Animal с методом sound(&self) -> String; структуры Dog и Cat реализуют его: «гав» '
                    'и «мяу». Функция chorus(a: &impl Animal) -> String возвращает звук, повторённый три '
                    'раза через пробел.',
       'starter': 'trait Animal {\n'
                  '    fn sound(&self) -> String;\n'
                  '}\n'
                  '\n'
                  'struct Dog;\n'
                  'struct Cat;\n'
                  '\n'
                  'impl Animal for Dog {\n'
                  '    fn sound(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Animal for Cat {\n'
                  '    fn sound(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn chorus(a: &impl Animal) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n    println!("{}", chorus(&Dog));\n    println!("{}", chorus(&Cat));\n}\n',
       'hint': 'impl Animal for Dog { … } — отдельный блок для каждого типа.',
       'expected': ['гав гав гав', 'мяу мяу мяу']},
      {'id': 'r13-trait-default',
       'mode': 'rust',
       'title': 'Метод по умолчанию',
       'statement': 'Трейт Greeter: метод name(&self) -> String обязателен, а greet(&self) -> String имеет '
                    'реализацию по умолчанию: «Привет, <имя>!». Структура English реализует только name; '
                    'структура Formal переопределяет greet: «Здравствуйте, <имя>.».',
       'starter': 'trait Greeter {\n'
                  '    fn name(&self) -> String;\n'
                  '    fn greet(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'struct English;\n'
                  'struct Formal;\n'
                  '\n'
                  'impl Greeter for English {\n'
                  '    fn name(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Greeter for Formal {\n'
                  '    fn name(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn greet(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", English.greet());\n'
                 '    println!("{}", Formal.greet());\n'
                 '}\n',
       'hint': 'Метод по умолчанию вызывает обязательный: self.name().',
       'expected': ['Привет, друг!', 'Здравствуйте, коллега.']},
      {'id': 'r13-dyn-shapes',
       'mode': 'rust',
       'title': 'Вектор фигур',
       'statement': 'Трейт Shape с area(&self) -> f64; структуры Circle { r }, Rect { w, h } реализуют его '
                    '(π ≈ 3.14159). Функция total_area(shapes: &[Box<dyn Shape>]) -> f64 — сумма площадей.',
       'starter': 'trait Shape {\n'
                  '    fn area(&self) -> f64;\n'
                  '}\n'
                  '\n'
                  'struct Circle {\n'
                  '    r: f64,\n'
                  '}\n'
                  'struct Rect {\n'
                  '    w: f64,\n'
                  '    h: f64,\n'
                  '}\n'
                  '\n'
                  'impl Shape for Circle {\n'
                  '    fn area(&self) -> f64 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  'impl Shape for Rect {\n'
                  '    fn area(&self) -> f64 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn total_area(shapes: &[Box<dyn Shape>]) -> f64 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let v: Vec<Box<dyn Shape>> = vec![Box::new(Circle { r: 1.0 }), Box::new(Rect { w: 2.0, '
                 'h: 3.0 })];\n'
                 '    println!("{:.5}", total_area(&v));\n'
                 '    println!("{}", total_area(&[]) == 0.0);\n'
                 '}\n',
       'hint': 'shapes.iter().map(|s| s.area()).sum()',
       'expected': ['9.14159', 'true']},
      {'id': 'r13-display',
       'mode': 'rust',
       'title': 'Display для точки',
       'statement': 'Реализуйте fmt::Display для структуры Point { x: i32, y: i32 }: вывод «(x, y)». Тогда '
                    'println!("{}", p) и p.to_string() дадут «(1, -2)».',
       'starter': 'use std::fmt;\n'
                  '\n'
                  'struct Point {\n'
                  '    x: i32,\n'
                  '    y: i32,\n'
                  '}\n'
                  '\n'
                  'impl fmt::Display for Point {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let p = Point { x: 1, y: -2 };\n'
                 '    println!("{}", p);\n'
                 '    println!("{}", p.to_string().len());\n'
                 '    println!("[{}]", Point { x: 0, y: 0 });\n'
                 '}\n',
       'hint': 'write!(f, "({}, {})", self.x, self.y)',
       'expected': ['(1, -2)', '7', '[(0, 0)]']},
      {'id': 'r13-debug-derive',
       'mode': 'rust',
       'title': 'Debug и PartialEq',
       'statement': 'Добавьте структуре Pair { a: i32, b: i32 } атрибуты derive(Debug, PartialEq, Clone), '
                    'чтобы работали печать {:?}, сравнение == и clone().',
       'starter': 'struct Pair {\n    a: i32,\n    b: i32,\n}\n',
       'driver': 'fn main() {\n'
                 '    let p = Pair { a: 1, b: 2 };\n'
                 '    let q = p.clone();\n'
                 '    println!("{:?}", p);\n'
                 '    println!("{}", p == q);\n'
                 '    println!("{}", p == Pair { a: 1, b: 3 });\n'
                 '}\n',
       'hint': '#[derive(Debug, PartialEq, Clone)] над struct.',
       'expected': ['Pair { a: 1, b: 2 }', 'true', 'false']},
      {'id': 'r13-ord-derive',
       'mode': 'rust',
       'title': 'Порядок версий',
       'statement': 'Структура Version(u32, u32, u32) с derive(PartialEq, Eq, PartialOrd, Ord, Debug): '
                    'версии сравниваются лексикографически. Дополните функцию newest(v: &[Version]) -> '
                    'Version, вернув наибольшую (v не пуст; Version нужно ещё Clone и Copy).',
       'starter': 'struct Version(u32, u32, u32);\n\nfn newest(v: &[Version]) -> Version {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let v = [Version(1, 9, 0), Version(2, 0, 1), Version(2, 0, 0)];\n'
                 '    println!("{:?}", newest(&v));\n'
                 '    println!("{}", Version(1, 10, 0) > Version(1, 9, 99));\n'
                 '}\n',
       'hint': 'derive(Ord) сравнивает поля по порядку; iter().max().',
       'expected': ['Version(2, 0, 1)', 'true']},
      {'id': 'r13-vec2-add',
       'mode': 'rust',
       'title': 'Сложение векторов',
       'statement': 'Реализуйте для Vec2 { x: f64, y: f64 } операторы + и − (трейты Add и Sub). '
                    'Derive(Debug, PartialEq, Clone, Copy) уже есть.',
       'starter': 'use std::ops::{Add, Sub};\n'
                  '\n'
                  '#[derive(Debug, PartialEq, Clone, Copy)]\n'
                  'struct Vec2 {\n'
                  '    x: f64,\n'
                  '    y: f64,\n'
                  '}\n'
                  '\n'
                  'impl Add for Vec2 {\n'
                  '    type Output = Vec2;\n'
                  '    fn add(self, o: Vec2) -> Vec2 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Sub for Vec2 {\n'
                  '    type Output = Vec2;\n'
                  '    fn sub(self, o: Vec2) -> Vec2 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a = Vec2 { x: 1.0, y: 2.0 };\n'
                 '    let b = Vec2 { x: 0.5, y: -1.0 };\n'
                 '    println!("{:?}", a + b);\n'
                 '    println!("{:?}", a - b);\n'
                 '    println!("{:?}", a + b - b == a);\n'
                 '}\n',
       'hint': 'Складывайте покомпонентно.',
       'expected': ['Vec2 { x: 1.5, y: 1.0 }', 'Vec2 { x: 0.5, y: 3.0 }', 'true']},
      {'id': 'r13-vec2-scalar',
       'mode': 'rust',
       'title': 'Умножение на число',
       'statement': 'Для Vec2 реализуйте Mul<f64> (вектор × число) и Neg (унарный минус).',
       'starter': 'use std::ops::{Mul, Neg};\n'
                  '\n'
                  '#[derive(Debug, PartialEq, Clone, Copy)]\n'
                  'struct Vec2 {\n'
                  '    x: f64,\n'
                  '    y: f64,\n'
                  '}\n'
                  '\n'
                  'impl Mul<f64> for Vec2 {\n'
                  '    type Output = Vec2;\n'
                  '    fn mul(self, k: f64) -> Vec2 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Neg for Vec2 {\n'
                  '    type Output = Vec2;\n'
                  '    fn neg(self) -> Vec2 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a = Vec2 { x: 1.0, y: -2.0 };\n'
                 '    println!("{:?}", a * 3.0);\n'
                 '    println!("{:?}", -a);\n'
                 '    println!("{:?}", -(a * 0.5));\n'
                 '}\n',
       'hint': 'impl Mul<f64> for Vec2 — тип правого операнда в угловых скобках.',
       'expected': ['Vec2 { x: 3.0, y: -6.0 }', 'Vec2 { x: -1.0, y: 2.0 }', 'Vec2 { x: -0.5, y: 1.0 }']},
      {'id': 'r13-vec2-dot',
       'mode': 'rust',
       'title': 'Скалярное произведение',
       'statement': 'Для Vec2 реализуйте Mul<Vec2> с Output = f64 (скалярное произведение): a * b = a.x·b.x '
                    '+ a.y·b.y.',
       'starter': 'use std::ops::Mul;\n'
                  '\n'
                  '#[derive(Debug, Clone, Copy)]\n'
                  'struct Vec2 {\n'
                  '    x: f64,\n'
                  '    y: f64,\n'
                  '}\n'
                  '\n'
                  'impl Mul<Vec2> for Vec2 {\n'
                  '    type Output = f64;\n'
                  '    fn mul(self, o: Vec2) -> f64 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a = Vec2 { x: 1.0, y: 2.0 };\n'
                 '    let b = Vec2 { x: 3.0, y: 4.0 };\n'
                 '    println!("{}", a * b);\n'
                 '    println!("{}", a * Vec2 { x: 0.0, y: 0.0 });\n'
                 '}\n',
       'hint': 'Output может быть другого типа, чем сами операнды.',
       'expected': ['11', '0']},
      {'id': 'r13-add-assign',
       'mode': 'rust',
       'title': '+=',
       'statement': 'Для Money(i64) (копейки) реализуйте Add и AddAssign, чтобы работали a + b и a += b. '
                    'Derive(Debug, Clone, Copy, PartialEq) уже есть.',
       'starter': 'use std::ops::{Add, AddAssign};\n'
                  '\n'
                  '#[derive(Debug, Clone, Copy, PartialEq)]\n'
                  'struct Money(i64);\n'
                  '\n'
                  'impl Add for Money {\n'
                  '    type Output = Money;\n'
                  '    fn add(self, o: Money) -> Money {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl AddAssign for Money {\n'
                  '    fn add_assign(&mut self, o: Money) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut m = Money(100);\n'
                 '    m += Money(250);\n'
                 '    println!("{:?}", m);\n'
                 '    println!("{:?}", m + Money(5));\n'
                 '    println!("{:?}", m);\n'
                 '}\n',
       'hint': 'add_assign принимает &mut self и ничего не возвращает.',
       'expected': ['Money(350)', 'Money(355)', 'Money(350)']},
      {'id': 'r13-index',
       'mode': 'rust',
       'title': 'Индексация матрицы',
       'statement': 'Структура Matrix { w: usize, data: Vec<i32> } (построчно). Реализуйте Index<(usize, '
                    'usize)> и IndexMut<(usize, usize)>, чтобы работало m[(r, c)] для чтения и записи.',
       'starter': 'use std::ops::{Index, IndexMut};\n'
                  '\n'
                  'struct Matrix {\n'
                  '    w: usize,\n'
                  '    data: Vec<i32>,\n'
                  '}\n'
                  '\n'
                  'impl Index<(usize, usize)> for Matrix {\n'
                  '    type Output = i32;\n'
                  '    fn index(&self, (r, c): (usize, usize)) -> &i32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl IndexMut<(usize, usize)> for Matrix {\n'
                  '    fn index_mut(&mut self, (r, c): (usize, usize)) -> &mut i32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut m = Matrix { w: 3, data: vec![0; 6] };\n'
                 '    m[(1, 2)] = 7;\n'
                 '    m[(0, 0)] += 5;\n'
                 '    println!("{} {} {}", m[(1, 2)], m[(0, 0)], m[(1, 1)]);\n'
                 '    println!("{:?}", m.data);\n'
                 '}\n',
       'hint': '&self.data[r * self.w + c] и &mut …',
       'expected': ['7 5 0', '[5, 0, 0, 0, 0, 7]']},
      {'id': 'r13-fraction',
       'mode': 'rust',
       'title': 'Дробь',
       'statement': 'Структура Frac { n: i64, d: i64 } с функцией new(n, d) -> Frac, сокращающей дробь по '
                    'НОД и держащей знаменатель положительным, и операторами Add, Mul, а также Display «n/d» '
                    '(при d = 1 — просто «n»).',
       'starter': 'use std::fmt;\n'
                  'use std::ops::{Add, Mul};\n'
                  '\n'
                  '#[derive(Debug, Clone, Copy, PartialEq)]\n'
                  'struct Frac {\n'
                  '    n: i64,\n'
                  '    d: i64,\n'
                  '}\n'
                  '\n'
                  'fn gcd(a: i64, b: i64) -> i64 {\n'
                  '    if b == 0 { a.abs() } else { gcd(b, a % b) }\n'
                  '}\n'
                  '\n'
                  'impl Frac {\n'
                  '    fn new(n: i64, d: i64) -> Frac {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Add for Frac {\n'
                  '    type Output = Frac;\n'
                  '    fn add(self, o: Frac) -> Frac {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Mul for Frac {\n'
                  '    type Output = Frac;\n'
                  '    fn mul(self, o: Frac) -> Frac {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl fmt::Display for Frac {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a = Frac::new(1, 2);\n'
                 '    let b = Frac::new(1, 3);\n'
                 '    println!("{}", a + b);\n'
                 '    println!("{}", a * b);\n'
                 '    println!("{}", Frac::new(2, 4));\n'
                 '    println!("{}", Frac::new(3, -6));\n'
                 '    println!("{}", Frac::new(1, 2) + Frac::new(1, 2));\n'
                 '}\n',
       'hint': 'Сначала сокращайте по НОД, затем нормализуйте знак знаменателя.',
       'expected': ['5/6', '1/6', '1/2', '-1/2', '1']},
      {'id': 'r13-iterator',
       'mode': 'rust',
       'title': 'Свой итератор',
       'statement': 'Структура Countdown { n: u32 } реализует Iterator<Item = u32>: next() отдаёт n, n−1, …, '
                    '1, затем None.',
       'starter': 'struct Countdown {\n'
                  '    n: u32,\n'
                  '}\n'
                  '\n'
                  'impl Iterator for Countdown {\n'
                  '    type Item = u32;\n'
                  '    fn next(&mut self) -> Option<u32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    for x in (Countdown { n: 3 }) {\n'
                 '        print!("{} ", x);\n'
                 '    }\n'
                 '    println!();\n'
                 '    let s: u32 = Countdown { n: 100 }.sum();\n'
                 '    println!("{}", s);\n'
                 '    let v: Vec<u32> = Countdown { n: 5 }.filter(|x| x % 2 == 1).collect();\n'
                 '    println!("{:?}", v);\n'
                 '}\n',
       'hint': 'Состояние хранится в self; когда n == 0 — None. Остальные методы итератора достаются даром.',
       'expected': ['3 2 1', '5050', '[5, 3, 1]']},
      {'id': 'r13-fib-iter',
       'mode': 'rust',
       'title': 'Итератор Фибоначчи',
       'statement': 'Структура Fib { a: u64, b: u64 } реализует Iterator<Item = u64>: 0, 1, 1, 2, 3, 5, … '
                    '(бесконечный). Добавьте функцию fib() -> Fib, возвращающую начальное состояние.',
       'starter': 'struct Fib {\n'
                  '    a: u64,\n'
                  '    b: u64,\n'
                  '}\n'
                  '\n'
                  'fn fib() -> Fib {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'impl Iterator for Fib {\n'
                  '    type Item = u64;\n'
                  '    fn next(&mut self) -> Option<u64> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let v: Vec<u64> = fib().take(10).collect();\n'
                 '    println!("{:?}", v);\n'
                 '    println!("{:?}", fib().skip(50).next());\n'
                 '    println!("{:?}", fib().take_while(|&x| x < 100).last());\n'
                 '}\n',
       'hint': 'Бесконечный итератор — всегда Some; ограничивает take.',
       'expected': ['[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]', 'Some(12586269025)', 'Some(89)']},
      {'id': 'r13-drop',
       'mode': 'rust',
       'title': 'Drop',
       'statement': 'Структура Noisy { name: String } печатает при уничтожении «drop <имя>». Реализуйте '
                    'Drop; порядок вывода покажет driver.',
       'starter': 'struct Noisy {\n'
                  '    name: String,\n'
                  '}\n'
                  '\n'
                  'impl Drop for Noisy {\n'
                  '    fn drop(&mut self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let _a = Noisy { name: String::from("a") };\n'
                 '    {\n'
                 '        let _b = Noisy { name: String::from("b") };\n'
                 '        println!("inner");\n'
                 '    }\n'
                 '    let c = Noisy { name: String::from("c") };\n'
                 '    drop(c);\n'
                 '    println!("end");\n'
                 '}\n',
       'hint': 'println!("drop {}", self.name)',
       'expected': ['inner', 'drop b', 'drop c', 'end', 'drop a']},
      {'id': 'r13-default',
       'mode': 'rust',
       'title': 'Default',
       'statement': 'Структура Settings { volume: u8, name: String, muted: bool } с derive(Debug, Default). '
                    'Добавьте derive и напишите функцию quiet() -> Settings: значения по умолчанию, но muted '
                    '= true (через ..Default::default()).',
       'starter': 'struct Settings {\n'
                  '    volume: u8,\n'
                  '    name: String,\n'
                  '    muted: bool,\n'
                  '}\n'
                  '\n'
                  'fn quiet() -> Settings {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", Settings::default());\n'
                 '    println!("{:?}", quiet());\n'
                 '}\n',
       'hint': '#[derive(Debug, Default)] и ..Default::default().',
       'expected': ['Settings { volume: 0, name: "", muted: false }',
                    'Settings { volume: 0, name: "", muted: true }']},
      {'id': 'r13-builder',
       'mode': 'rust',
       'title': 'Строитель с цепочкой',
       'statement': 'Структура Pizza { size: u32, cheese: bool, toppings: Vec<String> }. Напишите '
                    'Pizza::new(size), методы with_cheese(mut self) -> Pizza и with_topping(mut self, t: '
                    '&str) -> Pizza, а также describe(&self) -> String вида «30 см, сыр, начинки: гриб, лук» '
                    '(без сыра — без «сыр»; без начинок — без «начинки»).',
       'starter': 'struct Pizza {\n'
                  '    size: u32,\n'
                  '    cheese: bool,\n'
                  '    toppings: Vec<String>,\n'
                  '}\n'
                  '\n'
                  'impl Pizza {\n'
                  '    fn new(size: u32) -> Pizza {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn with_cheese(mut self) -> Pizza {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn with_topping(mut self, t: &str) -> Pizza {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn describe(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", '
                 'Pizza::new(30).with_cheese().with_topping("гриб").with_topping("лук").describe());\n'
                 '    println!("{}", Pizza::new(25).describe());\n'
                 '    println!("{}", Pizza::new(40).with_topping("ананас").describe());\n'
                 '}\n',
       'hint': 'Методы-строители принимают self по значению и возвращают его.',
       'expected': ['30 см, сыр, начинки: гриб, лук', '25 см', '40 см, начинки: ананас']},
      {'id': 'r13-newtype',
       'mode': 'rust',
       'title': 'Newtype: обёртка вектора',
       'statement': 'Реализуйте fmt::Display для обёртки struct Wrapper(Vec<String>): вывод «[a, b, c]» '
                    '(элементы через запятую с пробелом).',
       'starter': 'use std::fmt;\n'
                  '\n'
                  'struct Wrapper(Vec<String>);\n'
                  '\n'
                  'impl fmt::Display for Wrapper {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let w = Wrapper(vec![String::from("a"), String::from("b"), String::from("c")]);\n'
                 '    println!("{}", w);\n'
                 '    println!("{}", Wrapper(vec![]));\n'
                 '}\n',
       'hint': 'self.0 — вектор внутри обёртки.',
       'expected': ['[a, b, c]', '[]']},
      {'id': 'r13-stack-struct',
       'mode': 'rust',
       'title': 'Стек как структура',
       'statement': 'Структура Stack { items: Vec<i32> } с методами new(), push(&mut self, x), pop(&mut '
                    'self) -> Option<i32>, peek(&self) -> Option<i32>, len(&self) -> usize и is_empty(&self) '
                    '-> bool.',
       'starter': 'struct Stack {\n'
                  '    items: Vec<i32>,\n'
                  '}\n'
                  '\n'
                  'impl Stack {\n'
                  '    fn new() -> Stack {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn push(&mut self, x: i32) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn pop(&mut self) -> Option<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn peek(&self) -> Option<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn len(&self) -> usize {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn is_empty(&self) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut s = Stack::new();\n'
                 '    println!("{} {:?}", s.is_empty(), s.pop());\n'
                 '    s.push(1);\n'
                 '    s.push(2);\n'
                 '    println!("{:?} {}", s.peek(), s.len());\n'
                 '    println!("{:?} {:?} {:?}", s.pop(), s.pop(), s.pop());\n'
                 '}\n',
       'hint': 'Методы делегируют вектору внутри.',
       'expected': ['true None', 'Some(2) 2', 'Some(2) Some(1) None']},
      {'id': 'r13-queue-struct',
       'mode': 'rust',
       'title': 'Очередь на двух стеках',
       'statement': 'Реализуйте очередь Queue { inbox: Vec<i32>, outbox: Vec<i32> } с push(x), pop() -> '
                    'Option<i32> (FIFO) и len(). Когда outbox пуст, переложите в него все элементы inbox в '
                    'обратном порядке.',
       'starter': 'struct Queue {\n'
                  '    inbox: Vec<i32>,\n'
                  '    outbox: Vec<i32>,\n'
                  '}\n'
                  '\n'
                  'impl Queue {\n'
                  '    fn new() -> Queue {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn push(&mut self, x: i32) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn pop(&mut self) -> Option<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn len(&self) -> usize {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut q = Queue::new();\n'
                 '    q.push(1);\n'
                 '    q.push(2);\n'
                 '    q.push(3);\n'
                 '    println!("{:?}", q.pop());\n'
                 '    q.push(4);\n'
                 '    println!("{:?} {:?} {:?} {:?}", q.pop(), q.pop(), q.pop(), q.pop());\n'
                 '    println!("{}", q.len());\n'
                 '}\n',
       'hint': 'Перекладывание из inbox в outbox переворачивает порядок.',
       'expected': ['Some(1)', 'Some(2) Some(3) Some(4) None', '0']},
      {'id': 'r13-trait-plugins',
       'mode': 'rust',
       'title': 'Плагины',
       'statement': 'Трейт Plugin { fn name(&self) -> String; fn run(&self, x: i32) -> i32; }. Структуры '
                    'Doubler и AddN { n: i32 } его реализуют (имена «doubler» и «add»). Функция pipeline(ps: '
                    '&[Box<dyn Plugin>], x: i32) -> i32 последовательно применяет плагины.',
       'starter': 'trait Plugin {\n'
                  '    fn name(&self) -> String;\n'
                  '    fn run(&self, x: i32) -> i32;\n'
                  '}\n'
                  '\n'
                  'struct Doubler;\n'
                  'struct AddN {\n'
                  '    n: i32,\n'
                  '}\n'
                  '\n'
                  'impl Plugin for Doubler {\n'
                  '    fn name(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn run(&self, x: i32) -> i32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Plugin for AddN {\n'
                  '    fn name(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn run(&self, x: i32) -> i32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn pipeline(ps: &[Box<dyn Plugin>], x: i32) -> i32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let ps: Vec<Box<dyn Plugin>> = vec![Box::new(Doubler), Box::new(AddN { n: 5 }), '
                 'Box::new(Doubler)];\n'
                 '    println!("{}", pipeline(&ps, 3));\n'
                 '    let names: Vec<String> = ps.iter().map(|p| p.name()).collect();\n'
                 '    println!("{}", names.join(","));\n'
                 '}\n',
       'hint': 'Цикл по &[Box<dyn Plugin>] и вызов p.run(v).',
       'expected': ['22', 'doubler,add,doubler']},
      {'id': 'r13-generic-trait',
       'mode': 'rust',
       'title': 'Обобщённая функция с трейтом',
       'statement': 'Напишите функцию largest<T: PartialOrd + Copy>(v: &[T]) -> T, возвращающую наибольший '
                    'элемент среза (не пуст). Она должна работать и для i32, и для f64, и для char.',
       'starter': 'fn largest<T: PartialOrd + Copy>(v: &[T]) -> T {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", largest(&[3, 9, 2]));\n'
                 '    println!("{}", largest(&[1.5, -2.0]));\n'
                 '    println!("{}", largest(&[\'a\', \'я\', \'z\']));\n'
                 '}\n',
       'hint': 'Ограничение T: PartialOrd + Copy позволяет сравнивать и копировать.',
       'expected': ['9', '1.5', 'я']},
      {'id': 'r13-from-trait',
       'mode': 'rust',
       'title': 'From для преобразований',
       'statement': 'Структура Celsius(f64) и Fahrenheit(f64). Реализуйте From<Celsius> for Fahrenheit (c · '
                    '9/5 + 32); тогда Fahrenheit::from(c) и c.into() работают.',
       'starter': 'struct Celsius(f64);\n'
                  'struct Fahrenheit(f64);\n'
                  '\n'
                  'impl From<Celsius> for Fahrenheit {\n'
                  '    fn from(c: Celsius) -> Fahrenheit {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let f = Fahrenheit::from(Celsius(100.0));\n'
                 '    println!("{}", f.0);\n'
                 '    let g: Fahrenheit = Celsius(-40.0).into();\n'
                 '    println!("{}", g.0);\n'
                 '}\n',
       'hint': 'Fahrenheit(c.0 * 9.0 / 5.0 + 32.0)',
       'expected': ['212', '-40']},
      {'id': 'r13-partial-eq-manual',
       'mode': 'rust',
       'title': 'Своё равенство',
       'statement': 'Структура Name(String): два имени равны без учёта регистра. Реализуйте PartialEq '
                    'вручную (метод eq).',
       'starter': 'struct Name(String);\n'
                  '\n'
                  'impl PartialEq for Name {\n'
                  '    fn eq(&self, other: &Name) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a = Name(String::from("Аня"));\n'
                 '    let b = Name(String::from("аНЯ"));\n'
                 '    let c = Name(String::from("Боря"));\n'
                 '    println!("{}", a == b);\n'
                 '    println!("{}", a == c);\n'
                 '    println!("{}", a != c);\n'
                 '}\n',
       'hint': 'Сравнивайте нижние регистры строк.',
       'expected': ['true', 'false', 'true']},
      {'id': 'r13-partial-ord-manual',
       'mode': 'rust',
       'title': 'Своя сортировка',
       'statement': 'Структура Prio(u32): порядок обратный — большее число «меньше» (идёт раньше). '
                    'Реализуйте PartialOrd вручную (partial_cmp). PartialEq выведен через derive.',
       'starter': '#[derive(PartialEq, Debug)]\n'
                  'struct Prio(u32);\n'
                  '\n'
                  'impl PartialOrd for Prio {\n'
                  '    fn partial_cmp(&self, other: &Prio) -> Option<std::cmp::Ordering> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = vec![Prio(2), Prio(9), Prio(5)];\n'
                 '    v.sort_by(|a, b| a.partial_cmp(b).unwrap());\n'
                 '    println!("{:?}", v);\n'
                 '    println!("{}", Prio(9) < Prio(2));\n'
                 '}\n',
       'hint': 'Поменяйте местами операнды: other.0.partial_cmp(&self.0).',
       'expected': ['[Prio(9), Prio(5), Prio(2)]', 'true']},
      {'id': 'r13-trait-zero',
       'mode': 'rust',
       'title': 'Трейт со статической функцией',
       'statement': 'Трейт Zero { fn zero() -> Self; }. Реализуйте его для i32 и f64. Функция sum_all<T: '
                    'Zero + std::ops::Add<Output = T> + Copy>(v: &[T]) -> T складывает элементы, начиная с '
                    'T::zero().',
       'starter': 'trait Zero {\n'
                  '    fn zero() -> Self;\n'
                  '}\n'
                  '\n'
                  'impl Zero for i32 {\n'
                  '    fn zero() -> i32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Zero for f64 {\n'
                  '    fn zero() -> f64 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn sum_all<T: Zero + std::ops::Add<Output = T> + Copy>(v: &[T]) -> T {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", sum_all(&[1, 2, 3]));\n'
                 '    println!("{}", sum_all(&[0.5, 0.25]));\n'
                 '    println!("{}", sum_all::<i32>(&[]));\n'
                 '}\n',
       'hint': 'T::zero() вызывается через имя параметра типа.',
       'expected': ['6', '0.75', '0']}]}
