"""Задачи книги «Изучаем Rust»: глава 29 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {29: [{'id': 'r29-clone-manual',
       'mode': 'rust',
       'title': 'Свой Clone',
       'statement': 'Структура Doc { title: String, version: u32 }. Реализуйте Clone вручную так, чтобы клон '
                    'получал версию на единицу больше, а заголовок — тот же.',
       'starter': 'struct Doc {\n'
                  '    title: String,\n'
                  '    version: u32,\n'
                  '}\n'
                  '\n'
                  'impl Clone for Doc {\n'
                  '    fn clone(&self) -> Doc {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a = Doc { title: String::from("план"), version: 1 };\n'
                 '    let b = a.clone();\n'
                 '    let c = b.clone();\n'
                 '    println!("{} {} {}", a.version, b.version, c.version);\n'
                 '    println!("{}", b.title);\n'
                 '}\n',
       'hint': 'Поля клонируем по отдельности, у version прибавляем единицу.',
       'expected': ['1 2 3', 'план']},
      {'id': 'r29-copy-derive',
       'mode': 'rust',
       'title': 'Copy и Clone',
       'statement': 'Структура Point { x: i32, y: i32 }: добавьте derive так, чтобы значения копировались '
                    'при присваивании (Copy, Clone) и печатались (Debug).',
       'starter': 'struct Point {\n    x: i32,\n    y: i32,\n}\n',
       'driver': 'fn main() {\n'
                 '    let a = Point { x: 1, y: 2 };\n'
                 '    let b = a;\n'
                 '    println!("{:?} {:?}", a, b);\n'
                 '}\n',
       'hint': '#[derive(Debug, Clone, Copy)]',
       'expected': ['Point { x: 1, y: 2 } Point { x: 1, y: 2 }']},
      {'id': 'r29-default-manual',
       'mode': 'rust',
       'title': 'Default вручную',
       'statement': 'Структура Settings { volume: u8, name: String, ratio: f64 }. Реализуйте Default '
                    'вручную: громкость 50, имя «по умолчанию», коэффициент 1.5.',
       'starter': 'struct Settings {\n'
                  '    volume: u8,\n'
                  '    name: String,\n'
                  '    ratio: f64,\n'
                  '}\n'
                  '\n'
                  'impl Default for Settings {\n'
                  '    fn default() -> Settings {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let s = Settings::default();\n'
                 '    println!("{} {} {}", s.volume, s.name, s.ratio);\n'
                 '    let t = Settings { volume: 10, ..Default::default() };\n'
                 '    println!("{} {}", t.volume, t.name);\n'
                 '}\n',
       'hint': 'impl Default for Settings — функция default().',
       'expected': ['50 по умолчанию 1.5', '10 по умолчанию']},
      {'id': 'r29-partial-eq-cross',
       'mode': 'rust',
       'title': 'Равенство разных типов',
       'statement': 'Структуры Meters(f64) и Feet(f64). Реализуйте PartialEq<Feet> for Meters: равны, если '
                    'значения совпадают с точностью до 0.001 (1 м = 3.28084 фута).',
       'starter': 'struct Meters(f64);\n'
                  'struct Feet(f64);\n'
                  '\n'
                  'impl PartialEq<Feet> for Meters {\n'
                  '    fn eq(&self, other: &Feet) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", Meters(1.0) == Feet(3.28084));\n'
                 '    println!("{}", Meters(2.0) == Feet(3.0));\n'
                 '    println!("{}", Meters(0.0) != Feet(1.0));\n'
                 '}\n',
       'hint': 'Сравнивайте после перевода в футы с допуском.',
       'expected': ['true', 'false', 'true']},
      {'id': 'r29-ord-manual',
       'mode': 'rust',
       'title': 'Порядок задач',
       'statement': 'Структура Task { pri: u32, name: String }. Реализуйте Ord так, чтобы большая priority '
                    'считалась «больше», а при равенстве — имя по алфавиту раньше считалось «больше» '
                    '(обратный порядок имени). Добавьте PartialOrd, Eq, PartialEq.',
       'starter': 'use std::cmp::Ordering;\n'
                  '\n'
                  '#[derive(PartialEq, Eq, Debug)]\n'
                  'struct Task {\n'
                  '    pri: u32,\n'
                  '    name: String,\n'
                  '}\n'
                  '\n'
                  'impl Ord for Task {\n'
                  '    fn cmp(&self, other: &Task) -> Ordering {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl PartialOrd for Task {\n'
                  '    fn partial_cmp(&self, other: &Task) -> Option<Ordering> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    use std::collections::BinaryHeap;\n'
                 '    let mut h = BinaryHeap::new();\n'
                 '    for (p, n) in [(2, "b"), (5, "z"), (5, "a"), (1, "x")] {\n'
                 '        h.push(Task { pri: p, name: n.to_string() });\n'
                 '    }\n'
                 '    while let Some(t) = h.pop() {\n'
                 '        print!("{}{} ", t.pri, t.name);\n'
                 '    }\n'
                 '    println!();\n'
                 '}\n',
       'hint': 'then(other.name.cmp(&self.name)) переворачивает порядок имён.',
       'expected': ['5a 5z 2b 1x']},
      {'id': 'r29-hash-manual',
       'mode': 'rust',
       'title': 'Хеш без учёта регистра',
       'statement': 'Структура CiKey(String): равна другой без учёта регистра. Реализуйте PartialEq, Eq и '
                    'Hash вручную согласованно (хешируйте строку в нижнем регистре), чтобы HashSet<CiKey> '
                    'считал «Rust» и «rUST» одним ключом.',
       'starter': 'use std::hash::{Hash, Hasher};\n'
                  '\n'
                  'struct CiKey(String);\n'
                  '\n'
                  'impl PartialEq for CiKey {\n'
                  '    fn eq(&self, o: &CiKey) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  'impl Eq for CiKey {}\n'
                  'impl Hash for CiKey {\n'
                  '    fn hash<H: Hasher>(&self, h: &mut H) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    use std::collections::HashSet;\n'
                 '    let mut s = HashSet::new();\n'
                 '    for w in ["Rust", "rUST", "Go", "RUST", "go"] {\n'
                 '        s.insert(CiKey(w.to_string()));\n'
                 '    }\n'
                 '    println!("{}", s.len());\n'
                 '}\n',
       'hint': 'Хеш и равенство используют один и тот же приведённый ключ.',
       'expected': ['2']},
      {'id': 'r29-from-tuple',
       'mode': 'rust',
       'title': 'From для структуры',
       'statement': 'Структура Rgb(u8, u8, u8). Реализуйте From<(u8, u8, u8)>, From<[u8; 3]> и From<Rgb> for '
                    'u32 (0xRRGGBB).',
       'starter': 'struct Rgb(u8, u8, u8);\n'
                  '\n'
                  'impl From<(u8, u8, u8)> for Rgb {\n'
                  '    fn from(t: (u8, u8, u8)) -> Rgb {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  'impl From<[u8; 3]> for Rgb {\n'
                  '    fn from(a: [u8; 3]) -> Rgb {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  'impl From<Rgb> for u32 {\n'
                  '    fn from(c: Rgb) -> u32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a: Rgb = (255, 128, 0).into();\n'
                 '    let b = Rgb::from([1, 2, 3]);\n'
                 '    let n: u32 = a.into();\n'
                 '    println!("{:#08x}", n);\n'
                 '    println!("{}", u32::from(b));\n'
                 '}\n',
       'hint': 'Сдвиги << 16 и << 8.',
       'expected': ['0xff8000', '66051']},
      {'id': 'r29-try-from',
       'mode': 'rust',
       'title': 'TryFrom',
       'statement': 'Структура Percent(u8). Реализуйте TryFrom<i32> for Percent: Ok для 0..=100, иначе '
                    'Err(String) «вне диапазона: <n>».',
       'starter': '#[derive(Debug, PartialEq)]\n'
                  'struct Percent(u8);\n'
                  '\n'
                  'impl TryFrom<i32> for Percent {\n'
                  '    type Error = String;\n'
                  '    fn try_from(n: i32) -> Result<Percent, String> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", Percent::try_from(55));\n'
                 '    println!("{:?}", Percent::try_from(101));\n'
                 '    let r: Result<Percent, _> = (-5).try_into();\n'
                 '    println!("{:?}", r);\n'
                 '}\n',
       'hint': '(0..=100).contains(&n)',
       'expected': ['Ok(Percent(55))', 'Err("вне диапазона: 101")', 'Err("вне диапазона: -5")']},
      {'id': 'r29-as-ref',
       'mode': 'rust',
       'title': 'AsRef для обёртки',
       'statement': 'Структура Name(String). Реализуйте AsRef<str> for Name и напишите функцию shout(x: impl '
                    'AsRef<str>) -> String (в верхнем регистре), которая принимает и &str, и String, и Name.',
       'starter': 'struct Name(String);\n'
                  '\n'
                  'impl AsRef<str> for Name {\n'
                  '    fn as_ref(&self) -> &str {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn shout(x: impl AsRef<str>) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", shout("привет"));\n'
                 '    println!("{}", shout(String::from("rust")));\n'
                 '    println!("{}", shout(Name(String::from("аня"))));\n'
                 '}\n',
       'hint': '&self.0 — String приводится к &str.',
       'expected': ['ПРИВЕТ', 'RUST', 'АНЯ']},
      {'id': 'r29-deref',
       'mode': 'rust',
       'title': 'Deref для обёртки',
       'statement': 'Структура Stack(Vec<i32>). Реализуйте Deref<Target = Vec<i32>> и DerefMut, чтобы у '
                    'Stack работали методы вектора len(), last(), push() напрямую.',
       'starter': 'struct Stack(Vec<i32>);\n'
                  '\n'
                  'impl std::ops::Deref for Stack {\n'
                  '    type Target = Vec<i32>;\n'
                  '    fn deref(&self) -> &Vec<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  'impl std::ops::DerefMut for Stack {\n'
                  '    fn deref_mut(&mut self) -> &mut Vec<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut s = Stack(vec![1, 2]);\n'
                 '    s.push(3);\n'
                 '    println!("{} {:?}", s.len(), s.last());\n'
                 '    println!("{}", s.iter().sum::<i32>());\n'
                 '}\n',
       'hint': 'Верните ссылку на внутренний вектор.',
       'expected': ['3 Some(3)', '6']},
      {'id': 'r29-index',
       'mode': 'rust',
       'title': 'Index для сетки',
       'statement': 'Структура Grid { w: usize, cells: Vec<char> }. Реализуйте Index<(usize, usize)> и '
                    'IndexMut<(usize, usize)>: g[(x, y)] — клетка в столбце x и строке y.',
       'starter': 'struct Grid {\n'
                  '    w: usize,\n'
                  '    cells: Vec<char>,\n'
                  '}\n'
                  '\n'
                  'impl std::ops::Index<(usize, usize)> for Grid {\n'
                  '    type Output = char;\n'
                  '    fn index(&self, (x, y): (usize, usize)) -> &char {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  'impl std::ops::IndexMut<(usize, usize)> for Grid {\n'
                  '    fn index_mut(&mut self, (x, y): (usize, usize)) -> &mut char {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 "    let mut g = Grid { w: 3, cells: vec!['.'; 6] };\n"
                 "    g[(1, 1)] = '#';\n"
                 "    g[(2, 0)] = '@';\n"
                 '    let s: String = g.cells.iter().collect();\n'
                 '    println!("{}", s);\n'
                 '    println!("{}", g[(1, 1)]);\n'
                 '}\n',
       'hint': 'Индекс в плоском векторе: y * w + x.',
       'expected': ['..@.#.', '#']},
      {'id': 'r29-iterator-impl',
       'mode': 'rust',
       'title': 'Свой Iterator: Range со шагом',
       'statement': 'Структура Stepper { cur: i32, end: i32, step: i32 } (step > 0). Реализуйте '
                    'Iterator<Item = i32>: от cur до end (не включая) с шагом step.',
       'starter': 'struct Stepper {\n'
                  '    cur: i32,\n'
                  '    end: i32,\n'
                  '    step: i32,\n'
                  '}\n'
                  '\n'
                  'impl Iterator for Stepper {\n'
                  '    type Item = i32;\n'
                  '    fn next(&mut self) -> Option<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let v: Vec<i32> = Stepper { cur: 0, end: 10, step: 3 }.collect();\n'
                 '    println!("{:?}", v);\n'
                 '    println!("{}", Stepper { cur: 5, end: 5, step: 1 }.count());\n'
                 '    let s: i32 = Stepper { cur: 1, end: 100, step: 7 }.filter(|x| x % 2 == 0).sum();\n'
                 '    println!("{}", s);\n'
                 '}\n',
       'hint': 'Пока cur < end — отдаём и сдвигаем.',
       'expected': ['[0, 3, 6, 9]', '0', '350']},
      {'id': 'r29-into-iterator',
       'mode': 'rust',
       'title': 'IntoIterator для своей коллекции',
       'statement': 'Структура Bag { items: Vec<String> }. Реализуйте IntoIterator для Bag (по значению) и '
                    'для &Bag (по ссылке), чтобы работали for x in bag и for x in &bag.',
       'starter': 'struct Bag {\n'
                  '    items: Vec<String>,\n'
                  '}\n'
                  '\n'
                  'impl IntoIterator for Bag {\n'
                  '    type Item = String;\n'
                  '    type IntoIter = std::vec::IntoIter<String>;\n'
                  '    fn into_iter(self) -> Self::IntoIter {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  "impl<'a> IntoIterator for &'a Bag {\n"
                  "    type Item = &'a String;\n"
                  "    type IntoIter = std::slice::Iter<'a, String>;\n"
                  '    fn into_iter(self) -> Self::IntoIter {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let b = Bag { items: vec![String::from("a"), String::from("bb")] };\n'
                 '    for x in &b {\n'
                 '        print!("{} ", x.len());\n'
                 '    }\n'
                 '    println!();\n'
                 '    let mut total = String::new();\n'
                 '    for x in b {\n'
                 '        total.push_str(&x);\n'
                 '    }\n'
                 '    println!("{}", total);\n'
                 '}\n',
       'hint': 'Делегируйте вектору: into_iter() и iter().',
       'expected': ['1 2', 'abb']},
      {'id': 'r29-from-iterator',
       'mode': 'rust',
       'title': 'FromIterator',
       'statement': 'Структура Bag { items: Vec<String> }. Реализуйте FromIterator<&str> for Bag, чтобы '
                    'коллект из итератора строк работал: let b: Bag = words.into_iter().collect();',
       'starter': 'struct Bag {\n'
                  '    items: Vec<String>,\n'
                  '}\n'
                  '\n'
                  "impl<'a> FromIterator<&'a str> for Bag {\n"
                  "    fn from_iter<I: IntoIterator<Item = &'a str>>(it: I) -> Bag {\n"
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let b: Bag = "раз два три".split(\' \').collect();\n'
                 '    println!("{:?}", b.items);\n'
                 '    let e: Bag = std::iter::empty().collect();\n'
                 '    println!("{}", e.items.len());\n'
                 '}\n',
       'hint': 'Соберите вектор String из итератора &str.',
       'expected': ['["раз", "два", "три"]', '0']},
      {'id': 'r29-extend-sum',
       'mode': 'rust',
       'title': 'Extend и Sum',
       'statement': 'Структура Money(i64). Реализуйте std::iter::Sum for Money (сумма значений Money) и '
                    'Extend<Money>… для упрощения — только Sum и Add (Money + Money).',
       'starter': 'use std::ops::Add;\n'
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
                  'impl std::iter::Sum for Money {\n'
                  '    fn sum<I: Iterator<Item = Money>>(it: I) -> Money {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let total: Money = [Money(100), Money(250), Money(-50)].into_iter().sum();\n'
                 '    println!("{:?}", total);\n'
                 '    let z: Money = Vec::<Money>::new().into_iter().sum();\n'
                 '    println!("{:?}", z);\n'
                 '}\n',
       'hint': 'fold(Money(0), |a, b| a + b)',
       'expected': ['Money(300)', 'Money(0)']},
      {'id': 'r29-fn-param',
       'mode': 'rust',
       'title': 'Fn, FnMut, FnOnce',
       'statement': 'Напишите три функции: call_twice(f: impl Fn() -> i32) -> i32 (сумма двух вызовов), '
                    'call_mut(mut f: impl FnMut()) — вызвать 3 раза, call_once(f: impl FnOnce() -> String) '
                    '-> String — вызвать один раз.',
       'starter': 'fn call_twice(f: impl Fn() -> i32) -> i32 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn call_mut(mut f: impl FnMut()) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn call_once(f: impl FnOnce() -> String) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let k = 5;\n'
                 '    println!("{}", call_twice(|| k * 2));\n'
                 '    let mut count = 0;\n'
                 '    call_mut(|| count += 1);\n'
                 '    println!("{}", count);\n'
                 '    let s = String::from("перемещено");\n'
                 '    println!("{}", call_once(move || s));\n'
                 '}\n',
       'hint': 'FnOnce можно вызвать только один раз: f() без повторов.',
       'expected': ['20', '3', 'перемещено']},
      {'id': 'r29-boxed-fns',
       'mode': 'rust',
       'title': 'Список замыканий',
       'statement': 'Напишите compose_all(fs: Vec<Box<dyn Fn(i32) -> i32>>) -> Box<dyn Fn(i32) -> i32>: '
                    'функция, применяющая все по порядку.',
       'starter': 'fn compose_all(fs: Vec<Box<dyn Fn(i32) -> i32>>) -> Box<dyn Fn(i32) -> i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let f = compose_all(vec![Box::new(|x| x + 1), Box::new(|x| x * 10), Box::new(|x| x - '
                 '3)]);\n'
                 '    println!("{}", f(4));\n'
                 '    println!("{}", f(0));\n'
                 '    let id = compose_all(vec![]);\n'
                 '    println!("{}", id(7));\n'
                 '}\n',
       'hint': 'Box::new(move |x| fs.iter().fold(x, |acc, f| f(acc)))',
       'expected': ['47', '7', '7']},
      {'id': 'r29-error-source',
       'mode': 'rust',
       'title': 'Ошибка с причиной',
       'statement': 'Объявлены ConfigError { path: String, cause: std::num::ParseIntError }. Реализуйте '
                    'Display («ошибка в <path>»), Error и source() (возвращает Some(&self.cause)).',
       'starter': 'use std::fmt;\n'
                  'use std::error::Error;\n'
                  '\n'
                  '#[derive(Debug)]\n'
                  'struct ConfigError {\n'
                  '    path: String,\n'
                  '    cause: std::num::ParseIntError,\n'
                  '}\n'
                  '\n'
                  'impl fmt::Display for ConfigError {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Error for ConfigError {\n'
                  "    fn source(&self) -> Option<&(dyn Error + 'static)> {\n"
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let cause = "x".parse::<i32>().unwrap_err();\n'
                 '    let e = ConfigError { path: String::from("app.toml"), cause };\n'
                 '    println!("{}", e);\n'
                 '    println!("{}", e.source().is_some());\n'
                 '    println!("{}", e.source().unwrap());\n'
                 '    let b: Box<dyn Error> = Box::new(e);\n'
                 '    println!("{}", b);\n'
                 '}\n',
       'hint': 'source() возвращает Option<&dyn Error>.',
       'expected': ['ошибка в app.toml', 'true', 'invalid digit found in string', 'ошибка в app.toml']},
      {'id': 'r29-error-from',
       'mode': 'rust',
       'title': 'Объединение ошибок',
       'statement': 'Объявите enum AppError { Parse(std::num::ParseIntError), Neg(i64) } с '
                    'From<ParseIntError>, Display и Error. Функция positive(s: &str) -> Result<i64, '
                    'AppError> парсит число и возвращает Err(Neg(n)) для отрицательных.',
       'starter': 'use std::fmt;\n'
                  '\n'
                  '#[derive(Debug)]\n'
                  'enum AppError {\n'
                  '    Parse(std::num::ParseIntError),\n'
                  '    Neg(i64),\n'
                  '}\n'
                  '\n'
                  'impl fmt::Display for AppError {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  'impl std::error::Error for AppError {}\n'
                  'impl From<std::num::ParseIntError> for AppError {\n'
                  '    fn from(e: std::num::ParseIntError) -> AppError {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn positive(s: &str) -> Result<i64, AppError> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", positive("42").unwrap());\n'
                 '    println!("{}", positive("-7").unwrap_err());\n'
                 '    println!("{}", positive("abc").unwrap_err());\n'
                 '}\n',
       'hint': '? превращает ParseIntError в AppError через From.',
       'expected': ['42', 'отрицательное: -7', 'разбор: invalid digit found in string']},
      {'id': 'r29-send-sync',
       'mode': 'rust',
       'title': 'Send и Sync',
       'statement': 'Напишите функции assert_send<T: Send>() и assert_sync<T: Sync>() (пустые, проверка при '
                    'компиляции), а в main (driver) проверяется, что String и Vec<i32> — Send, а '
                    'Arc<Mutex<i32>> — Send и Sync. Ваше решение — только объявления функций.',
       'starter': 'fn assert_send<T: Send>() {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn assert_sync<T: Sync>() {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    assert_send::<String>();\n'
                 '    assert_send::<Vec<i32>>();\n'
                 '    assert_send::<std::sync::Arc<std::sync::Mutex<i32>>>();\n'
                 '    assert_sync::<std::sync::Arc<std::sync::Mutex<i32>>>();\n'
                 '    assert_sync::<i32>();\n'
                 '    println!("ok");\n'
                 '}\n',
       'hint': 'Пустое тело: проверка происходит при подстановке типа.',
       'expected': ['ok']},
      {'id': 'r29-any-downcast',
       'mode': 'rust',
       'title': 'Динамический тип',
       'statement': 'Напишите describe(v: &dyn std::any::Any) -> String: «целое N» для i32, «строка S» для '
                    'String, «дробное X» для f64, иначе «неизвестно» (downcast_ref).',
       'starter': 'fn describe(v: &dyn std::any::Any) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", describe(&5i32));\n'
                 '    println!("{}", describe(&String::from("привет")));\n'
                 '    println!("{}", describe(&2.5f64));\n'
                 '    println!("{}", describe(&\'c\'));\n'
                 '    println!("{}", describe(&"str"));\n'
                 '}\n',
       'hint': 'downcast_ref::<T>() возвращает Option<&T>.',
       'expected': ['целое 5', 'строка привет', 'дробное 2.5', 'неизвестно', 'неизвестно']},
      {'id': 'r29-cow',
       'mode': 'rust',
       'title': 'Cow',
       'statement': 'Напишите normalize(s: &str) -> std::borrow::Cow<str>: если в строке есть табуляции, '
                    'вернуть Owned с табуляциями, заменёнными пробелами, иначе — Borrowed без копирования. '
                    'Driver проверяет вариант.',
       'starter': 'fn normalize(s: &str) -> std::borrow::Cow<str> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    use std::borrow::Cow;\n'
                 '    let a = normalize("a\\tb");\n'
                 '    let b = normalize("ab");\n'
                 '    println!("{} {}", a, matches!(a, Cow::Owned(_)));\n'
                 '    println!("{} {}", b, matches!(b, Cow::Borrowed(_)));\n'
                 '}\n',
       'hint': 'Cow::Borrowed(s) — без копирования; Cow::Owned(String).',
       'expected': ['a b true', 'ab true']},
      {'id': 'r29-phantom',
       'mode': 'rust',
       'title': 'Типизированные идентификаторы',
       'statement': 'Структура Id<T> { n: u32, _m: PhantomData<T> }. Реализуйте new(n), get(&self) и '
                    'Clone/Copy/PartialEq/Debug вручную без ограничений на T (derive потребовал бы Clone для '
                    'T). Типы User и Order — пустые структуры. Сравнение Id<User> с Id<Order> не должно '
                    'компилироваться (проверять нечем — просто используйте PhantomData).',
       'starter': 'use std::marker::PhantomData;\n'
                  '\n'
                  'struct User;\n'
                  'struct Order;\n'
                  '\n'
                  'struct Id<T> {\n'
                  '    n: u32,\n'
                  '    _m: PhantomData<T>,\n'
                  '}\n'
                  '\n'
                  'impl<T> Id<T> {\n'
                  '    fn new(n: u32) -> Id<T> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn get(&self) -> u32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl<T> Clone for Id<T> {\n'
                  '    fn clone(&self) -> Id<T> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  'impl<T> Copy for Id<T> {}\n'
                  'impl<T> PartialEq for Id<T> {\n'
                  '    fn eq(&self, o: &Id<T>) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let u: Id<User> = Id::new(7);\n'
                 '    let v = u;\n'
                 '    let o: Id<Order> = Id::new(7);\n'
                 '    println!("{} {}", u.get(), u == v);\n'
                 '    println!("{}", o.get());\n'
                 '}\n',
       'hint': 'PhantomData — значение без данных: Id { n, _m: PhantomData }.',
       'expected': ['7 true', '7']},
      {'id': 'r29-borrow-lookup',
       'mode': 'rust',
       'title': 'Borrow и поиск',
       'statement': 'Напишите find_len(m: &std::collections::HashMap<String, usize>, key: &str) -> usize: '
                    'значение по ключу или 0 — поиск по &str в карте с ключом String (обоснование — трейт '
                    'Borrow<str>).',
       'starter': 'fn find_len(m: &std::collections::HashMap<String, usize>, key: &str) -> usize {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut m = std::collections::HashMap::new();\n'
                 '    m.insert(String::from("a"), 5);\n'
                 '    println!("{} {}", find_len(&m, "a"), find_len(&m, "b"));\n'
                 '}\n',
       'hint': 'm.get(key) принимает &str, потому что String: Borrow<str>.',
       'expected': ['5 0']},
      {'id': 'r29-display-debug',
       'mode': 'rust',
       'title': 'Display и Debug вместе',
       'statement': 'Структура Ver(u32, u32, u32). Реализуйте Display «1.2.3» и derive(Debug); функция '
                    'show(v: &impl std::fmt::Display) -> String возвращает «версия <v>».',
       'starter': 'use std::fmt;\n'
                  '\n'
                  '#[derive(Debug)]\n'
                  'struct Ver(u32, u32, u32);\n'
                  '\n'
                  'impl fmt::Display for Ver {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn show(v: &impl fmt::Display) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let v = Ver(1, 2, 3);\n'
                 '    println!("{}", show(&v));\n'
                 '    println!("{:?}", v);\n'
                 '    println!("{}", v.to_string());\n'
                 '    println!("{}", show(&42));\n'
                 '}\n',
       'hint': 'Display даёт to_string() бесплатно.',
       'expected': ['версия 1.2.3', 'Ver(1, 2, 3)', '1.2.3', 'версия 42']},
      {'id': 'r29-generic-bound',
       'mode': 'rust',
       'title': 'Ограничения трейтов',
       'statement': 'Напишите largest_by_key<T, K: Ord>(items: &[T], key: impl Fn(&T) -> K) -> Option<&T>: '
                    'элемент с наибольшим ключом (при равенстве — первый).',
       'starter': 'fn largest_by_key<T, K: Ord>(items: &[T], key: impl Fn(&T) -> K) -> Option<&T> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let words = ["aa", "bbbb", "c", "dddd"];\n'
                 '    println!("{:?}", largest_by_key(&words, |w| w.len()));\n'
                 '    println!("{:?}", largest_by_key(&[3i32, -9, 5], |x| x.abs()));\n'
                 '    println!("{:?}", largest_by_key(&Vec::<i32>::new(), |x| *x));\n'
                 '}\n',
       'hint': 'Заменяйте best только при строго большем ключе.',
       'expected': ['Some("bbbb")', 'Some(-9)', 'None']},
      {'id': 'r29-trait-assoc',
       'mode': 'rust',
       'title': 'Ассоциированный тип',
       'statement': 'Трейт Container { type Item; fn first(&self) -> Option<&Self::Item>; fn size(&self) -> '
                    'usize; }. Реализуйте его для структуры Words(Vec<String>) (Item = String).',
       'starter': 'trait Container {\n'
                  '    type Item;\n'
                  '    fn first(&self) -> Option<&Self::Item>;\n'
                  '    fn size(&self) -> usize;\n'
                  '}\n'
                  '\n'
                  'struct Words(Vec<String>);\n'
                  '\n'
                  'impl Container for Words {\n'
                  '    type Item = String;\n'
                  '    fn first(&self) -> Option<&String> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn size(&self) -> usize {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let w = Words(vec![String::from("a"), String::from("b")]);\n'
                 '    println!("{:?} {}", w.first(), w.size());\n'
                 '    println!("{:?}", Words(vec![]).first());\n'
                 '}\n',
       'hint': 'type Item = String; делегируйте методы вектору.',
       'expected': ['Some("a") 2', 'None']},
      {'id': 'r29-supertrait',
       'mode': 'rust',
       'title': 'Супертрейт',
       'statement': 'Трейт Named: fmt::Display + ... — объявите trait Entity: std::fmt::Display { fn '
                    'id(&self) -> u32; fn label(&self) -> String { format!("#{} {}", self.id(), self) } }. '
                    'Реализуйте Entity и Display для структуры Item { id: u32, name: String } (Display '
                    'печатает имя).',
       'starter': 'use std::fmt;\n'
                  '\n'
                  'trait Entity: fmt::Display {\n'
                  '    fn id(&self) -> u32;\n'
                  '    fn label(&self) -> String {\n'
                  '        format!("#{} {}", self.id(), self)\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'struct Item {\n'
                  '    id: u32,\n'
                  '    name: String,\n'
                  '}\n'
                  '\n'
                  'impl fmt::Display for Item {\n'
                  '    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  'impl Entity for Item {\n'
                  '    fn id(&self) -> u32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let i = Item { id: 7, name: String::from("болт") };\n'
                 '    println!("{}", i.label());\n'
                 '    println!("{}", i);\n'
                 '}\n',
       'hint': 'Супертрейт гарантирует, что Display доступен внутри метода по умолчанию.',
       'expected': ['#7 болт', 'болт']},
      {'id': 'r29-blanket',
       'mode': 'rust',
       'title': 'Общая реализация',
       'statement': 'Трейт Shout { fn shout(&self) -> String; }. Реализуйте его сразу для всех типов, у '
                    'которых есть Display (impl<T: Display> Shout for T): текст в верхнем регистре с «!».',
       'starter': 'use std::fmt::Display;\n'
                  '\n'
                  'trait Shout {\n'
                  '    fn shout(&self) -> String;\n'
                  '}\n'
                  '\n'
                  'impl<T: Display> Shout for T {\n'
                  '    fn shout(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", "привет".shout());\n'
                 '    println!("{}", 42.shout());\n'
                 '    println!("{}", 2.5.shout());\n'
                 '    println!("{}", String::from("ok").shout());\n'
                 '}\n',
       'hint': 'Общая реализация (blanket impl) действует для любого T: Display.',
       'expected': ['ПРИВЕТ!', '42!', '2.5!', 'OK!']},
      {'id': 'r29-unsized',
       'mode': 'rust',
       'title': '?Sized',
       'statement': 'Напишите byte_len<T: ?Sized + AsRef<[u8]>>(x: &T) -> usize: длина в байтах для str, '
                    'срезов и векторов (ослабление Sized позволяет принимать str и [u8] напрямую).',
       'starter': 'fn byte_len<T: ?Sized + AsRef<[u8]>>(x: &T) -> usize {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", byte_len("привет"));\n'
                 '    println!("{}", byte_len(&b"ab"[..]));\n'
                 '    println!("{}", byte_len(&vec![1u8, 2, 3]));\n'
                 '    println!("{}", byte_len(&String::from("яя")));\n'
                 '}\n',
       'hint': 'x.as_ref().len(); T: ?Sized разрешает str и [u8].',
       'expected': ['12', '2', '3', '4']}]}
