"""Задачи книги «Изучаем Rust»: глава 19 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {19: [{'id': 'r19-largest',
       'mode': 'rust',
       'title': 'Обобщённая функция: наибольший элемент',
       'statement': 'Напишите largest<T: PartialOrd>(v: &[T]) → Option<&T>: ссылка на наибольший элемент '
                    'среза (при равных — первый), None для пустого среза. Функция должна работать и с '
                    'числами, и с дробными, и со строками.',
       'starter': 'fn largest<T: PartialOrd>(v: &[T]) -> Option<&T> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", largest(&[3, 9, 2, 9]));\n'
                 '    println!("{:?}", largest(&[1.5, -2.0, 0.25]));\n'
                 '    println!("{:?}", largest(&["pear", "apple", "zebra", "mango"]));\n'
                 '    let e: [i32; 0] = [];\n'
                 '    println!("{:?}", largest(&e));\n'
                 '}\n',
       'hint': 'v.first()? даёт первый элемент или сразу возвращает None; сравнивайте ссылки: x > best.',
       'expected': ['Some(9)', 'Some(1.5)', 'Some("zebra")', 'None']},
      {'id': 'r19-fix-bound',
       'mode': 'rust',
       'title': 'Исправьте: у T нет сравнения',
       'statement': 'max_of возвращает большее из двух значений. Код не компилируется: компилятор не знает, '
                    'что T умеет сравниваться. Исправьте сигнатуру — добавьте ограничение трейта, тело '
                    'менять не нужно.',
       'starter': 'fn max_of<T>(a: T, b: T) -> T {\n    if a > b { a } else { b }\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", max_of(3, 9));\n'
                 '    println!("{}", max_of("pear", "apple"));\n'
                 '    println!("{}", max_of(2.5, -1.0));\n'
                 '    println!("{}", max_of(\'a\', \'z\'));\n'
                 '}\n',
       'hint': 'fn max_of<T: PartialOrd>(…) — после двоеточия идёт трейт, который нужен для знака >.',
       'expected': ['9', 'pear', '2.5', 'z']},
      {'id': 'r19-pair',
       'mode': 'rust',
       'title': 'Обобщённая структура Pair<T>',
       'statement': 'Pair<T> хранит два значения одного типа. new(a, b); swap(self) → Pair<T> с '
                    'переставленными значениями; larger(&self) → &T — ссылка на большее (доступна только для '
                    'T: PartialOrd; при равенстве — первое).',
       'starter': 'struct Pair<T> {\n'
                  '    a: T,\n'
                  '    b: T,\n'
                  '}\n'
                  '\n'
                  'impl<T> Pair<T> {\n'
                  '    fn new(a: T, b: T) -> Pair<T> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn swap(self) -> Pair<T> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl<T: PartialOrd> Pair<T> {\n'
                  '    fn larger(&self) -> &T {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let p = Pair::new(3, 8);\n'
                 '    println!("{}", p.larger());\n'
                 '    let q = p.swap();\n'
                 '    println!("{} {}", q.a, q.b);\n'
                 '    let s = Pair::new(String::from("kiwi"), String::from("fig")).swap();\n'
                 '    println!("{} {} {}", s.a, s.b, s.larger());\n'
                 '}\n',
       'hint': 'swap забирает self по значению, поэтому поля можно просто переставить без клонирования.',
       'expected': ['8', '8 3', 'fig kiwi kiwi']},
      {'id': 'r19-trait-shape',
       'mode': 'rust',
       'title': 'Трейт Shape и реализации',
       'statement': 'Трейт Shape уже объявлен: area(&self) → f64 и name(&self) → String. Реализуйте его для '
                    'Circle (радиус), Rect (две стороны) и Square (сторона): имена «circle», «rect», '
                    '«square». total_area(shapes: &[Box<dyn Shape>]) → f64 — сумма площадей.',
       'starter': 'use std::f64::consts::PI;\n'
                  '\n'
                  'trait Shape {\n'
                  '    fn area(&self) -> f64;\n'
                  '    fn name(&self) -> String;\n'
                  '}\n'
                  '\n'
                  'struct Circle(f64);\n'
                  'struct Rect(f64, f64);\n'
                  'struct Square(f64);\n'
                  '\n'
                  'impl Shape for Circle {\n'
                  '    fn area(&self) -> f64 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn name(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  '// реализуйте Shape для Rect и Square\n'
                  '\n'
                  'fn total_area(shapes: &[Box<dyn Shape>]) -> f64 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let shapes: Vec<Box<dyn Shape>> = vec![Box::new(Circle(1.0)), Box::new(Rect(2.0, '
                 '3.0)), Box::new(Square(4.0))];\n'
                 '    for s in &shapes {\n'
                 '        println!("{} {:.2}", s.name(), s.area());\n'
                 '    }\n'
                 '    println!("{:.3}", total_area(&shapes));\n'
                 '    println!("{}", total_area(&[]) == 0.0);\n'
                 '}\n',
       'hint': 'Для Rect: self.0 * self.1. total_area: shapes.iter().map(|s| s.area()).sum().',
       'expected': ['circle 3.14', 'rect 6.00', 'square 16.00', '25.142', 'true']},
      {'id': 'r19-default-method',
       'mode': 'rust',
       'title': 'Метод по умолчанию и переопределение',
       'statement': 'Трейт Describe: обязательный метод name(&self) → String и метод по умолчанию '
                    'describe(&self) → String = «<name>: описание отсутствует». Реализуйте для Cat '
                    '(используйте метод по умолчанию) и для Dog (переопределите describe: «<name> лает»).',
       'starter': 'trait Describe {\n'
                  '    fn name(&self) -> String;\n'
                  '    // добавьте describe с реализацией по умолчанию\n'
                  '}\n'
                  '\n'
                  'struct Cat;\n'
                  'struct Dog {\n'
                  '    nick: String,\n'
                  '}\n'
                  '\n'
                  '// impl Describe for Cat / Dog\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", Cat.describe());\n'
                 '    let d = Dog { nick: "Рекс".into() };\n'
                 '    println!("{} | {}", d.name(), d.describe());\n'
                 '}\n',
       'hint': 'В трейте у describe есть тело, а в impl для Cat его не пишут; для Dog пишут свой describe.',
       'expected': ['cat: описание отсутствует', 'Рекс | Рекс лает']},
      {'id': 'r19-supertrait',
       'mode': 'rust',
       'title': 'Супертрейт: Named: Display',
       'statement': 'Трейт Tagged требует Display (супертрейт): tag(&self) → String по умолчанию '
                    '«<ЗНАЧЕНИЕ>» — результат Display, обёрнутый в угловые скобки. Реализуйте Tagged для '
                    'Point (Display — «(x, y)») и для u32 (Display уже есть).',
       'starter': 'use std::fmt;\n'
                  '\n'
                  'struct Point {\n'
                  '    x: i32,\n'
                  '    y: i32,\n'
                  '}\n'
                  '\n'
                  '// impl fmt::Display for Point — «(x, y)»\n'
                  '\n'
                  'trait Tagged: fmt::Display {\n'
                  '    // tag по умолчанию\n'
                  '}\n'
                  '\n'
                  '// impl Tagged for Point и для u32\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", Point { x: 1, y: -2 }.tag());\n'
                 '    println!("{}", 42u32.tag());\n'
                 '}\n',
       'hint': 'Внутри трейта можно пользоваться Display у self благодаря супертрейту: format!("<{}>", '
               'self).',
       'expected': ['<(1, -2)>', '<42>']},
      {'id': 'r19-ops-complex',
       'mode': 'rust',
       'title': 'Операторы: комплексные числа',
       'statement': 'Для Complex { re, im } (f64, Copy) реализуйте Add, Sub, Mul, Neg и Display в виде '
                    '«1+2i» / «1-2i» (числа через {}, знак перед мнимой частью, модуль мнимой части). '
                    'Умножение: (a+bi)(c+di) = (ac−bd) + (ad+bc)i.',
       'starter': 'use std::fmt;\n'
                  'use std::ops::{Add, Mul, Neg, Sub};\n'
                  '\n'
                  '#[derive(Debug, Clone, Copy, PartialEq)]\n'
                  'struct Complex {\n'
                  '    re: f64,\n'
                  '    im: f64,\n'
                  '}\n'
                  '\n'
                  '// impl Add, Sub, Mul, Neg, Display\n',
       'driver': 'fn main() {\n'
                 '    let a = Complex { re: 1.0, im: 2.0 };\n'
                 '    let b = Complex { re: 3.0, im: -1.0 };\n'
                 '    println!("{} {} {}", a + b, a - b, a * b);\n'
                 '    println!("{} {}", -a, (a * b) * -b);\n'
                 '    println!("{}", a == Complex { re: 1.0, im: 2.0 });\n'
                 '}\n',
       'hint': 'Каждая операция — метод своего трейта с type Output = Complex; Neg строит значение с '
               'обратными знаками.',
       'expected': ['4+1i -2+3i 5+5i', '-1-2i -20-10i', 'true']},
      {'id': 'r19-ops-assign-index',
       'mode': 'rust',
       'title': 'AddAssign, Mul<f64> и Index',
       'statement': 'Vec2 { x, y } (f64, Copy): реализуйте AddAssign (v += w), Mul<f64> (v * 2.0) и '
                    'Mul<Vec2> for f64 (2.0 * v). Grid { w, h, data } хранит клетки построчно: Index<(usize, '
                    'usize)> и IndexMut<(usize, usize)> по (строка, столбец).',
       'starter': 'use std::ops::{AddAssign, Index, IndexMut, Mul};\n'
                  '\n'
                  '#[derive(Debug, Clone, Copy, PartialEq)]\n'
                  'struct Vec2 {\n'
                  '    x: f64,\n'
                  '    y: f64,\n'
                  '}\n'
                  '\n'
                  'struct Grid {\n'
                  '    w: usize,\n'
                  '    h: usize,\n'
                  '    data: Vec<i32>,\n'
                  '}\n'
                  '\n'
                  'impl Grid {\n'
                  '    fn new(h: usize, w: usize) -> Grid {\n'
                  '        Grid { w, h, data: vec![0; w * h] }\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  '// impl AddAssign, Mul<f64>, Mul<Vec2> for f64, Index, IndexMut\n',
       'driver': 'fn main() {\n'
                 '    let mut v = Vec2 { x: 1.0, y: 2.0 };\n'
                 '    v += Vec2 { x: 0.5, y: 0.5 };\n'
                 '    println!("{:?} {:?} {:?}", v, v * 2.0, 3.0 * v);\n'
                 '    let mut g = Grid::new(2, 3);\n'
                 '    g[(0, 1)] = 7;\n'
                 '    g[(1, 2)] += 5;\n'
                 '    g[(1, 2)] *= 2;\n'
                 '    println!("{} {} {:?}", g[(0, 1)], g[(1, 2)], g.data);\n'
                 '}\n',
       'hint': 'Index возвращает ссылку: &self.data[r * self.w + c]; IndexMut — изменяемую ссылку на тот же '
               'элемент.',
       'expected': ['Vec2 { x: 1.5, y: 2.5 } Vec2 { x: 3.0, y: 5.0 } Vec2 { x: 4.5, y: 7.5 }',
                    '7 10 [0, 7, 0, 0, 0, 10]']},
      {'id': 'r19-ord-card',
       'mode': 'rust',
       'title': 'Ручной Ord: масть, затем ранг',
       'statement': 'Card { rank: u8, suit: Suit } с Suit: Clubs < Diamonds < Hearts < Spades. Порядок карт: '
                    'сначала масть, затем ранг (поля в структуре идут в другом порядке, поэтому derive не '
                    'подойдёт). Реализуйте Ord и PartialOrd вручную (partial_cmp вызывает cmp); PartialEq и '
                    'Eq — derive.',
       'starter': 'use std::cmp::Ordering;\n'
                  '\n'
                  '#[derive(Debug, Clone, Copy, PartialEq, Eq)]\n'
                  'enum Suit {\n'
                  '    Clubs,\n'
                  '    Diamonds,\n'
                  '    Hearts,\n'
                  '    Spades,\n'
                  '}\n'
                  '\n'
                  '#[derive(Debug, Clone, Copy, PartialEq, Eq)]\n'
                  'struct Card {\n'
                  '    rank: u8,\n'
                  '    suit: Suit,\n'
                  '}\n'
                  '\n'
                  '// impl Ord for Card и PartialOrd for Card\n',
       'driver': 'fn main() {\n'
                 '    use Suit::*;\n'
                 '    let mut v = vec![\n'
                 '        Card { rank: 10, suit: Hearts },\n'
                 '        Card { rank: 2, suit: Spades },\n'
                 '        Card { rank: 14, suit: Clubs },\n'
                 '        Card { rank: 3, suit: Hearts },\n'
                 '        Card { rank: 2, suit: Clubs },\n'
                 '    ];\n'
                 '    v.sort();\n'
                 '    for c in &v {\n'
                 '        print!("{}{:?} ", c.rank, c.suit);\n'
                 '    }\n'
                 '    println!();\n'
                 '    println!("{:?}", v.iter().max());\n'
                 '    println!("{}", Card { rank: 2, suit: Spades } > Card { rank: 14, suit: Hearts });\n'
                 '}\n',
       'hint': 'Сравните кортежи (масть как число, ранг): у кортежей порядок лексикографический, а Suit as '
               'u8 берёт номер варианта.',
       'expected': ['2Clubs 14Clubs 3Hearts 10Hearts 2Spades',
                    'Some(Card { rank: 2, suit: Spades })',
                    'true']},
      {'id': 'r19-partialord-float',
       'mode': 'rust',
       'title': 'Полный порядок для f64: total_cmp',
       'statement': 'f64 не реализует Ord из-за NaN. Оберните число: Score(f64) и реализуйте PartialEq, Eq, '
                    'PartialOrd и Ord через f64::total_cmp (NaN считается наибольшим). Тогда Vec<Score> '
                    'можно отсортировать методом sort.',
       'starter': 'use std::cmp::Ordering;\n'
                  '\n'
                  '#[derive(Debug, Clone, Copy)]\n'
                  'struct Score(f64);\n'
                  '\n'
                  '// impl PartialEq, Eq, PartialOrd, Ord for Score\n',
       'driver': 'fn main() {\n'
                 '    let mut v: Vec<Score> = [3.5, -1.0, f64::NAN, 2.0, -0.0, 0.0].iter().map(|&x| '
                 'Score(x)).collect();\n'
                 '    v.sort();\n'
                 '    println!("{:?}", v.iter().map(|s| s.0).collect::<Vec<_>>());\n'
                 '    println!("{:?}", v.iter().max().map(|s| s.0.is_nan()));\n'
                 '    println!("{}", Score(1.0) < Score(2.0));\n'
                 '}\n',
       'hint': 'cmp = self.0.total_cmp(&other.0); остальные три трейта выражаются через него.',
       'expected': ['[-1.0, -0.0, 0.0, 2.0, 3.5, NaN]', 'Some(true)', 'true']},
      {'id': 'r19-mono-name',
       'mode': 'rust',
       'title': 'Мономорфизация: тип и размер',
       'statement': 'Напишите describe<T>(_: &T) → String: «<имя типа> = <размер> байт» — имя через '
                    'std::any::type_name::<T>(), размер через size_of::<T>(). Каждый вызов с новым T — это '
                    'отдельная копия функции, которую компилятор создал при сборке.',
       'starter': 'fn describe<T>(_: &T) -> String {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", describe(&1i32));\n'
                 '    println!("{}", describe(&1u8));\n'
                 '    println!("{}", describe(&"text"));\n'
                 '    println!("{}", describe(&vec![1u8, 2]));\n'
                 '    println!("{}", describe(&(1i32, 2u8)));\n'
                 '    println!("{}", describe(&Some(Box::new(3i32))));\n'
                 '}\n',
       'hint': 'type_name и size_of — функции std; тип указывают через turbofish: type_name::<T>().',
       'expected': ['i32 = 4 байт',
                    'u8 = 1 байт',
                    '&str = 16 байт',
                    'alloc::vec::Vec<u8> = 24 байт',
                    '(i32, u8) = 8 байт',
                    'core::option::Option<alloc::boxed::Box<i32>> = 8 байт']},
      {'id': 'r19-dyn-size',
       'mode': 'rust',
       'title': 'Размер толстого указателя',
       'statement': 'Напишите sizes() → [usize; 5]: size_of для &i32, &dyn Shape, Box<dyn Shape>, &[i32], '
                    'Box<i32> — в таком порядке. Какие из них «толстые» (два слова), а какие — обычные '
                    'указатели?',
       'starter': 'trait Shape {\n'
                  '    fn area(&self) -> f64;\n'
                  '}\n'
                  '\n'
                  'fn sizes() -> [usize; 5] {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'struct Unit;\n'
                 'impl Shape for Unit {\n'
                 '    fn area(&self) -> f64 {\n'
                 '        1.0\n'
                 '    }\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    println!("{:?}", sizes());\n'
                 '    let b: Box<dyn Shape> = Box::new(Unit);\n'
                 '    println!("{}", b.area());\n'
                 '}\n',
       'hint': 'Срез и трейт-объект хранят дополнительное слово: длину или адрес vtable.',
       'expected': ['[8, 16, 16, 16, 8]', '1']},
      {'id': 'r19-impl-trait-arg',
       'mode': 'rust',
       'title': 'impl Trait в аргументе',
       'statement': 'join_all(items: &[impl Display], sep: &str) → String: элементы, склеенные разделителем. '
                    'print_each(items: impl IntoIterator<Item = impl Display>) → Vec<String>: каждый элемент '
                    'в виде строки «[x]».',
       'starter': 'use std::fmt::Display;\n'
                  '\n'
                  'fn join_all(items: &[impl Display], sep: &str) -> String {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn print_each(items: impl IntoIterator<Item = impl Display>) -> Vec<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", join_all(&[1, 2, 3], "-"));\n'
                 '    println!("{}", join_all(&["a", "b"], ", "));\n'
                 '    println!("{}", join_all(&[1.5, 2.25], " | "));\n'
                 '    println!("{:?}", print_each(vec![10, 20]));\n'
                 '    println!("{:?}", print_each(["x", "y", "z"]));\n'
                 '    println!("{:?}", print_each(1..=3));\n'
                 '}\n',
       'hint': 'to_string() есть у любого Display; IntoIterator принимает и вектор, и массив, и диапазон.',
       'expected': ['1-2-3',
                    'a, b',
                    '1.5 | 2.25',
                    '["[10]", "[20]"]',
                    '["[x]", "[y]", "[z]"]',
                    '["[1]", "[2]", "[3]"]']},
      {'id': 'r19-impl-trait-return',
       'mode': 'rust',
       'title': 'impl Trait в результате',
       'statement': 'evens(limit) → impl Iterator<Item = u32>: чётные числа меньше limit; squares(v: &[i32]) '
                    "→ impl Iterator<Item = i32> + '_: квадраты элементов среза. Конкретный тип итератора "
                    'наружу не раскрывается.',
       'starter': 'fn evens(limit: u32) -> impl Iterator<Item = u32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  "fn squares(v: &[i32]) -> impl Iterator<Item = i32> + '_ {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", evens(10).collect::<Vec<_>>());\n'
                 '    println!("{}", evens(1000).sum::<u32>());\n'
                 '    let data = vec![1, -2, 3];\n'
                 '    println!("{:?}", squares(&data).collect::<Vec<_>>());\n'
                 '    println!("{}", squares(&data).max().unwrap());\n'
                 '}\n',
       'hint': "В evens достаточно (0..limit).filter(...) — компилятор сам выведет тип; '_ связывает время "
               'жизни итератора со срезом.',
       'expected': ['[0, 2, 4, 6, 8]', '249500', '[1, 4, 9]', '9']},
      {'id': 'r19-where-clause',
       'mode': 'rust',
       'title': 'Блок where',
       'statement': 'count_matching<T, F>(v: &[T], pred: F) → usize where F: Fn(&T) → bool. show_pairs<K, '
                    'V>(items: &[(K, V)]) → String where K: Display, V: Debug: «ключ=значение» (значение '
                    'через {:?}) через «; ». Ограничения пишите в where.',
       'starter': 'use std::fmt::{Debug, Display};\n'
                  '\n'
                  'fn count_matching<T, F>(v: &[T], pred: F) -> usize\n'
                  'where\n'
                  '    F: Fn(&T) -> bool,\n'
                  '{\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn show_pairs<K, V>(items: &[(K, V)]) -> String\n'
                  'where\n'
                  '    K: Display,\n'
                  '    V: Debug,\n'
                  '{\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", count_matching(&[1, 2, 3, 4, 5], |x| x % 2 == 1));\n'
                 '    println!("{}", count_matching(&["a", "bb", "ccc"], |s| s.len() > 1));\n'
                 '    println!("{}", show_pairs(&[("a", 1), ("b", 2)]));\n'
                 '    println!("{}", show_pairs(&[(1, "x"), (2, "y")]));\n'
                 '    println!("{:?}", show_pairs::<i32, i32>(&[]));\n'
                 '}\n',
       'hint': 'filter(|x| pred(x)) — внутри filter элемент имеет тип &&T, а pred ждёт &T; при вызове '
               'pred(x) раст сам разыменует.',
       'expected': ['3', '2', 'a=1; b=2', '1="x"; 2="y"', '""']},
      {'id': 'r19-plugin-registry',
       'mode': 'rust',
       'title': 'Плагины: Vec<Box<dyn Plugin>>',
       'statement': 'Трейт Plugin: name(&self) → &str и run(&mut self, input: &str) → String. Реализуйте '
                    'Upper (переводит в верхний регистр), Reverse (переворачивает символы) и Counter '
                    '(возвращает «#N: input», где N — номер вызова с единицы). run_all(plugins: &mut '
                    '[Box<dyn Plugin>], input) → Vec<String> «имя: результат».',
       'starter': 'trait Plugin {\n'
                  '    fn name(&self) -> &str;\n'
                  '    fn run(&mut self, input: &str) -> String;\n'
                  '}\n'
                  '\n'
                  'struct Upper;\n'
                  'struct Reverse;\n'
                  'struct Counter {\n'
                  '    calls: u32,\n'
                  '}\n'
                  '\n'
                  '// impl Plugin для трёх типов\n'
                  '\n'
                  'fn run_all(plugins: &mut [Box<dyn Plugin>], input: &str) -> Vec<String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut ps: Vec<Box<dyn Plugin>> = vec![Box::new(Upper), Box::new(Reverse), '
                 'Box::new(Counter { calls: 0 })];\n'
                 '    for line in run_all(&mut ps, "привет") {\n'
                 '        println!("{line}");\n'
                 '    }\n'
                 '    println!("{:?}", run_all(&mut ps, "abc"));\n'
                 '    println!("{}", std::mem::size_of::<Box<dyn Plugin>>());\n'
                 '}\n',
       'hint': 'Метод run изменяет плагин, поэтому нужен iter_mut(); имя возьмите заранее (to_string), иначе '
               'заём от name() помешает вызвать run.',
       'expected': ['upper: ПРИВЕТ',
                    'reverse: тевирп',
                    'counter: #1: привет',
                    '["upper: ABC", "reverse: cba", "counter: #2: abc"]',
                    '16']},
      {'id': 'r19-fib-iterator',
       'mode': 'rust',
       'title': 'Свой итератор: Фибоначчи',
       'statement': 'Структура Fib реализует Iterator<Item = u64>: 0, 1, 1, 2, 3, 5, … (бесконечно; при '
                    'переполнении итератор заканчивается — используйте checked_add). Fib::new() создаёт '
                    'начало ряда. Все адаптеры (take, filter, sum) приходят сами.',
       'starter': 'struct Fib {\n'
                  '    a: u64,\n'
                  '    b: u64,\n'
                  '}\n'
                  '\n'
                  'impl Fib {\n'
                  '    fn new() -> Fib {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Iterator for Fib {\n'
                  '    type Item = u64;\n'
                  '\n'
                  '    fn next(&mut self) -> Option<u64> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", Fib::new().take(10).collect::<Vec<_>>());\n'
                 '    println!("{}", Fib::new().take_while(|&x| x < 4_000_000).filter(|x| x % 2 == '
                 '0).sum::<u64>());\n'
                 '    println!("{:?}", Fib::new().skip(5).step_by(3).take(4).collect::<Vec<_>>());\n'
                 '    println!("{}", Fib::new().count());\n'
                 '    println!("{:?}", Fib::new().last());\n'
                 '}\n',
       'hint': 'Верните текущее a, затем сдвиньте пару (a, b) = (b, a + b); checked_add с ? завершит '
               'итератор при переполнении.',
       'expected': ['[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]',
                    '4613732',
                    '[5, 21, 89, 377]',
                    '92',
                    'Some(4660046610375530309)']},
      {'id': 'r19-steps-double-ended',
       'mode': 'rust',
       'title': 'Итератор с двух концов',
       'statement': 'Steps { cur, end, step } — как диапазон с шагом: next выдаёт cur, cur+step, … пока < '
                    'end; next_back выдаёт последний элемент (последний шаг перед end). Реализуйте Iterator '
                    'и DoubleEndedIterator; тогда работает .rev(). Считайте, что step ≥ 1, end ≥ cur.',
       'starter': 'struct Steps {\n'
                  '    cur: u32,\n'
                  '    end: u32,\n'
                  '    step: u32,\n'
                  '}\n'
                  '\n'
                  'impl Steps {\n'
                  '    fn new(start: u32, end: u32, step: u32) -> Steps {\n'
                  '        Steps { cur: start, end, step }\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Iterator for Steps {\n'
                  '    type Item = u32;\n'
                  '    fn next(&mut self) -> Option<u32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl DoubleEndedIterator for Steps {\n'
                  '    fn next_back(&mut self) -> Option<u32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", Steps::new(0, 10, 3).collect::<Vec<_>>());\n'
                 '    println!("{:?}", Steps::new(0, 10, 3).rev().collect::<Vec<_>>());\n'
                 '    let mut s = Steps::new(1, 20, 4);\n'
                 '    println!("{:?} {:?} {:?}", s.next(), s.next_back(), s.next());\n'
                 '    println!("{:?}", s.collect::<Vec<_>>());\n'
                 '    println!("{:?}", Steps::new(5, 5, 1).next_back());\n'
                 '}\n',
       'hint': 'next_back: сколько шагов помещается до end — (end - cur - 1) / step; последний элемент cur + '
               'n*step, и end сдвигается на него.',
       'expected': ['[0, 3, 6, 9]', '[9, 6, 3, 0]', 'Some(1) Some(17) Some(5)', '[9, 13]', 'None']},
      {'id': 'r19-assoc-const',
       'mode': 'rust',
       'title': 'Константа в трейте',
       'statement': 'Трейт Polygon: const SIDES: u32 и метод по умолчанию angle_sum() → u32 = (SIDES − 2) × '
                    '180. Реализуйте для Triangle (3), Square (4), Hexagon (6). total_sides<A: Polygon, B: '
                    'Polygon>() → u32 — сумма SIDES двух типов (без значений: тип передают параметром).',
       'starter': 'trait Polygon {\n'
                  '    const SIDES: u32;\n'
                  '    // angle_sum по умолчанию\n'
                  '}\n'
                  '\n'
                  'struct Triangle;\n'
                  'struct Square;\n'
                  'struct Hexagon;\n'
                  '\n'
                  '// impl Polygon для трёх типов\n'
                  '\n'
                  'fn total_sides<A: Polygon, B: Polygon>() -> u32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{} {} {}", Triangle::SIDES, Square::angle_sum(), Hexagon::angle_sum());\n'
                 '    println!("{}", total_sides::<Triangle, Hexagon>());\n'
                 '    println!("{}", total_sides::<Square, Square>());\n'
                 '    println!("{}", std::mem::size_of::<Hexagon>());\n'
                 '}\n',
       'hint': 'Внутри трейта константу называют Self::SIDES; у типа без данных size_of равен нулю.',
       'expected': ['3 360 720', '9', '8', '0']},
      {'id': 'r19-generic-stack',
       'mode': 'rust',
       'title': 'Stack<T> и условный impl',
       'statement': 'Stack<T> на Vec<T>: new, push, pop → Option<T>, peek → Option<&T>, len, is_empty. '
                    'Отдельный блок impl<T: Display> Stack<T> добавляет show() → String: элементы от вершины '
                    'к основанию через « > » (пустой — «(пусто)»).',
       'starter': 'use std::fmt::Display;\n'
                  '\n'
                  'struct Stack<T> {\n'
                  '    items: Vec<T>,\n'
                  '}\n'
                  '\n'
                  'impl<T> Stack<T> {\n'
                  '    fn new() -> Stack<T> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn push(&mut self, x: T) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn pop(&mut self) -> Option<T> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn peek(&self) -> Option<&T> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn len(&self) -> usize {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn is_empty(&self) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl<T: Display> Stack<T> {\n'
                  '    fn show(&self) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut s = Stack::new();\n'
                 '    println!("{} {}", s.is_empty(), s.show());\n'
                 '    for i in [1, 2, 3] {\n'
                 '        s.push(i);\n'
                 '    }\n'
                 '    println!("{} {:?} {}", s.len(), s.peek(), s.show());\n'
                 '    println!("{:?} {:?}", s.pop(), s.pop());\n'
                 '    let mut t: Stack<String> = Stack::new();\n'
                 '    t.push("a".into());\n'
                 '    t.push("b".into());\n'
                 '    println!("{}", t.show());\n'
                 '    let mut v: Stack<Vec<u8>> = Stack::new();\n'
                 '    v.push(vec![1]);\n'
                 '    println!("{} {}", v.len(), std::mem::size_of::<Stack<u8>>());\n'
                 '}\n',
       'hint': 'show идёт по items.iter().rev() — вершина стека в конце вектора.',
       'expected': ['true (пусто)', '3 Some(3) 3 > 2 > 1', 'Some(3) Some(2)', 'b > a', '1 24']},
      {'id': 'r19-blanket-impl',
       'mode': 'rust',
       'title': 'Общая реализация для всех T: Display',
       'statement': 'Трейт Shout с методом shout(&self) → String. Одной общей реализацией impl<T: Display> '
                    'Shout for T сделайте метод доступным у чисел, строк и ваших типов: результат — текст в '
                    'верхнем регистре с «!» в конце. Для Money(i64) реализуйте Display («<n> руб.»).',
       'starter': 'use std::fmt::{self, Display};\n'
                  '\n'
                  'trait Shout {\n'
                  '    fn shout(&self) -> String;\n'
                  '}\n'
                  '\n'
                  '// impl<T: Display> Shout for T\n'
                  '\n'
                  'struct Money(i64);\n'
                  '\n'
                  '// impl Display for Money\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", "hello".shout());\n'
                 '    println!("{}", 42.shout());\n'
                 '    println!("{}", 2.5f32.shout());\n'
                 '    println!("{}", \'x\'.shout());\n'
                 '    println!("{}", Money(99).shout());\n'
                 '    println!("{}", String::from("привет").shout());\n'
                 '}\n',
       'hint': 'Общая реализация сработает для любого типа с Display — в том числе для Money после '
               'реализации Display.',
       'expected': ['HELLO!', '42!', '2.5!', 'X!', '99 РУБ.!', 'ПРИВЕТ!']},
      {'id': 'r19-from-into',
       'mode': 'rust',
       'title': 'From и Into: температуры',
       'statement': 'Celsius(f64) и Fahrenheit(f64). Реализуйте From<Celsius> for Fahrenheit (f = c·9/5 + '
                    '32) и From<Fahrenheit> for Celsius. to_f(t: impl Into<Fahrenheit>) → f64 принимает '
                    'любую из шкал. Into получается бесплатно.',
       'starter': '#[derive(Debug, Clone, Copy)]\n'
                  'struct Celsius(f64);\n'
                  '#[derive(Debug, Clone, Copy)]\n'
                  'struct Fahrenheit(f64);\n'
                  '\n'
                  '// impl From<Celsius> for Fahrenheit и From<Fahrenheit> for Celsius\n'
                  '\n'
                  'fn to_f(t: impl Into<Fahrenheit>) -> f64 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let f: Fahrenheit = Celsius(100.0).into();\n'
                 '    println!("{:.1}", f.0);\n'
                 '    let c = Celsius::from(Fahrenheit(212.0));\n'
                 '    println!("{:.1}", c.0);\n'
                 '    println!("{:.1} {:.1}", to_f(Celsius(-40.0)), to_f(Fahrenheit(50.0)));\n'
                 '    println!("{:.1}", to_f(Fahrenheit(32.0)));\n'
                 '}\n',
       'hint': 'impl From<A> for B даёт A::into() → B без дополнительного кода; to_f просто вызывает '
               't.into().',
       'expected': ['212.0', '100.0', '-40.0 50.0', '32.0']},
      {'id': 'r19-try-from',
       'mode': 'rust',
       'title': 'TryFrom: проверенное значение',
       'statement': 'Percent(u8) хранит число от 0 до 100. Реализуйте TryFrom<i32> for Percent с Error = '
                    'String: «вне диапазона: N» при N < 0 или N > 100. parse_all(v: &[i32]) → '
                    'Result<Vec<Percent>, String> — все или первая ошибка.',
       'starter': '#[derive(Debug, PartialEq)]\n'
                  'struct Percent(u8);\n'
                  '\n'
                  '// impl TryFrom<i32> for Percent\n'
                  '\n'
                  'fn parse_all(v: &[i32]) -> Result<Vec<Percent>, String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", Percent::try_from(50));\n'
                 '    println!("{:?}", Percent::try_from(101));\n'
                 '    let r: Result<Percent, _> = (-5).try_into();\n'
                 '    println!("{:?}", r);\n'
                 '    println!("{:?}", parse_all(&[0, 10, 100]));\n'
                 '    println!("{:?}", parse_all(&[10, 200, -1]));\n'
                 '}\n',
       'hint': 'try_into появляется бесплатно; collect в Result<Vec<_>, _> остановится на первой ошибке.',
       'expected': ['Ok(Percent(50))',
                    'Err("вне диапазона: 101")',
                    'Err("вне диапазона: -5")',
                    'Ok([Percent(0), Percent(10), Percent(100)])',
                    'Err("вне диапазона: 200")']},
      {'id': 'r19-fromstr',
       'mode': 'rust',
       'title': 'FromStr: разбор Point',
       'statement': 'Point { x, y } (i32). Реализуйте FromStr: «3,4» (пробелы вокруг чисел допускаются). '
                    'Ошибки ParsePointError: Missing — нет запятой или частей больше двух; BadNumber(строка) '
                    '— часть не число. После этого работает "3,4".parse::<Point>().',
       'starter': 'use std::str::FromStr;\n'
                  '\n'
                  '#[derive(Debug, PartialEq)]\n'
                  'struct Point {\n'
                  '    x: i32,\n'
                  '    y: i32,\n'
                  '}\n'
                  '\n'
                  '#[derive(Debug, PartialEq)]\n'
                  'enum ParsePointError {\n'
                  '    Missing,\n'
                  '    BadNumber(String),\n'
                  '}\n'
                  '\n'
                  '// impl FromStr for Point\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", "3,4".parse::<Point>());\n'
                 '    println!("{:?}", " 5 , -6 ".parse::<Point>());\n'
                 '    println!("{:?}", "7".parse::<Point>());\n'
                 '    println!("{:?}", "a,1".parse::<Point>());\n'
                 '    println!("{:?}", "1,2,3".parse::<Point>());\n'
                 '    let p: Point = "0,0".parse().unwrap();\n'
                 '    println!("{}", p == Point { x: 0, y: 0 });\n'
                 '}\n',
       'hint': "Разбейте по ',', проверьте длину, а числа разбирайте замыканием с map_err и оператором ?.",
       'expected': ['Ok(Point { x: 3, y: 4 })',
                    'Ok(Point { x: 5, y: -6 })',
                    'Err(Missing)',
                    'Err(BadNumber("a"))',
                    'Err(Missing)',
                    'true']},
      {'id': 'r19-asref',
       'mode': 'rust',
       'title': 'AsRef: принять всё похожее на строку',
       'statement': 'total_len<S: AsRef<str>>(items: &[S]) → usize — сумма длин в байтах (подойдут &str и '
                    'String). checksum<B: AsRef<[u8]>>(b: B) → u32 — сумма байтов (подойдут Vec<u8>, массив, '
                    '&str, String).',
       'starter': 'fn total_len<S: AsRef<str>>(items: &[S]) -> usize {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn checksum<B: AsRef<[u8]>>(b: B) -> u32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", total_len(&["ab", "cde"]));\n'
                 '    println!("{}", total_len(&[String::from("привет"), String::from("x")]));\n'
                 '    println!("{}", checksum(vec![1u8, 2, 3]));\n'
                 '    println!("{}", checksum([10u8, 20]));\n'
                 '    println!("{}", checksum("AB"));\n'
                 '    println!("{}", checksum(String::from("a")));\n'
                 '}\n',
       'hint': 'as_ref() даёт &str или &[u8] — дальше обычная работа со срезом.',
       'expected': ['5', '13', '6', '30', '131', '97']},
      {'id': 'r19-sum-trait',
       'mode': 'rust',
       'title': 'impl Sum для своего типа',
       'statement': 'Money(i64) (Copy): реализуйте Add и два трейта std::iter::Sum — для Money и для &Money, '
                    'чтобы работали v.iter().sum::<Money>() и v.into_iter().sum::<Money>().',
       'starter': 'use std::iter::Sum;\n'
                  'use std::ops::Add;\n'
                  '\n'
                  '#[derive(Debug, Clone, Copy, PartialEq)]\n'
                  'struct Money(i64);\n'
                  '\n'
                  '// impl Add, Sum<Money>, Sum<&Money>\n',
       'driver': 'fn main() {\n'
                 '    let v = vec![Money(100), Money(250), Money(-30)];\n'
                 '    let by_ref: Money = v.iter().sum();\n'
                 '    let by_val = v.clone().into_iter().sum::<Money>();\n'
                 '    println!("{:?} {:?} {}", by_ref, by_val, by_ref == by_val);\n'
                 '    println!("{:?}", Vec::<Money>::new().into_iter().sum::<Money>());\n'
                 '    println!("{:?}", (1..=4).map(|n| Money(n * 10)).sum::<Money>());\n'
                 '}\n',
       'hint': 'Sum — это свёртка fold с начальным Money(0); для &Money разыменуйте элемент.',
       'expected': ['Money(320) Money(320) true', 'Money(0)', 'Money(100)']},
      {'id': 'r19-default-generic',
       'mode': 'rust',
       'title': 'Default в обобщённом коде',
       'statement': 'defaults<A: Default, B: Default>() → (A, B) — пара значений по умолчанию. or_default<T: '
                    'Default + PartialEq>(v: T) → Option<T>: None, если значение равно умолчанию. Settings '
                    '(derive Default): retries: u32, name: String, verbose: bool, ratio: f64, tags: '
                    'Vec<String>.',
       'starter': 'fn defaults<A: Default, B: Default>() -> (A, B) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn or_default<T: Default + PartialEq>(v: T) -> Option<T> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'struct Settings {\n'
                  '    retries: u32,\n'
                  '    name: String,\n'
                  '    verbose: bool,\n'
                  '    ratio: f64,\n'
                  '    tags: Vec<String>,\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let (a, b): (i32, String) = defaults();\n'
                 '    println!("{:?} {:?}", a, b);\n'
                 '    let t = defaults::<bool, Vec<u8>>();\n'
                 '    println!("{:?}", t);\n'
                 '    println!("{:?} {:?} {:?}", or_default(0), or_default(5), or_default(String::new()));\n'
                 '    println!("{:?}", or_default(String::from("x")));\n'
                 '    println!("{:?}", Settings::default());\n'
                 '    println!("{:?}", Settings { retries: 3, ..Default::default() });\n'
                 '}\n',
       'hint': 'T::default() доступен благодаря ограничению; для Settings достаточно #[derive(Debug, '
               'Default)].',
       'expected': ['0 ""',
                    '(false, [])',
                    'None Some(5) None',
                    'Some("x")',
                    'Settings { retries: 0, name: "", verbose: false, ratio: 0.0, tags: [] }',
                    'Settings { retries: 3, name: "", verbose: false, ratio: 0.0, tags: [] }']},
      {'id': 'r19-visitor',
       'mode': 'rust',
       'title': 'Visitor с ассоциированным типом',
       'statement': 'Expr — Num(i64), Add(Box<Expr>, Box<Expr>), Mul(Box<Expr>, Box<Expr>). Трейт Visitor '
                    'имеет type Out и методы num(n), add(a, b), mul(a, b) (результаты уже обработанных '
                    'частей). Напишите walk<V: Visitor>(e: &Expr, v: &mut V) → V::Out и два посетителя: Eval '
                    '(Out = i64) и Show (Out = String: «(a + b)», «(a * b)», число).',
       'starter': 'enum Expr {\n'
                  '    Num(i64),\n'
                  '    Add(Box<Expr>, Box<Expr>),\n'
                  '    Mul(Box<Expr>, Box<Expr>),\n'
                  '}\n'
                  '\n'
                  'trait Visitor {\n'
                  '    type Out;\n'
                  '    fn num(&mut self, n: i64) -> Self::Out;\n'
                  '    fn add(&mut self, a: Self::Out, b: Self::Out) -> Self::Out;\n'
                  '    fn mul(&mut self, a: Self::Out, b: Self::Out) -> Self::Out;\n'
                  '}\n'
                  '\n'
                  'fn walk<V: Visitor>(e: &Expr, v: &mut V) -> V::Out {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'struct Eval;\n'
                  'struct Show;\n'
                  '\n'
                  '// impl Visitor for Eval и Show\n',
       'driver': 'fn num(n: i64) -> Box<Expr> {\n'
                 '    Box::new(Expr::Num(n))\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    let e = Expr::Add(num(2), Box::new(Expr::Mul(num(3), num(4))));\n'
                 '    println!("{}", walk(&e, &mut Eval));\n'
                 '    println!("{}", walk(&e, &mut Show));\n'
                 '    println!("{}", walk(&Expr::Num(-5), &mut Show));\n'
                 '}\n',
       'hint': 'walk сначала обходит дочерние узлы, а потом передаёт их результаты методу посетителя.',
       'expected': ['14', '(2 + (3 * 4))', '-5']},
      {'id': 'r19-type-state',
       'mode': 'rust',
       'title': 'Состояния в типе: Door<Open> и Door<Closed>',
       'statement': 'Door<S> хранит счётчик открываний и PhantomData<S>. Door<Closed>::new() → закрытая; у '
                    'Door<Closed> есть open(self) → Door<Open> (счётчик +1); у Door<Open> — close(self) → '
                    'Door<Closed> и opened(&self) → u32. Состояние — часть типа: вызвать open у открытой '
                    'двери нельзя, и в памяти это ничего не стоит.',
       'starter': 'use std::marker::PhantomData;\n'
                  '\n'
                  'struct Open;\n'
                  'struct Closed;\n'
                  '\n'
                  'struct Door<S> {\n'
                  '    opened: u32,\n'
                  '    _s: PhantomData<S>,\n'
                  '}\n'
                  '\n'
                  '// impl Door<Closed> { new, open }\n'
                  '// impl Door<Open> { close, opened }\n',
       'driver': 'fn main() {\n'
                 '    let d = Door::new();\n'
                 '    let d = d.open();\n'
                 '    println!("{}", d.opened());\n'
                 '    let d = d.close().open().close().open();\n'
                 '    println!("{}", d.opened());\n'
                 '    println!("{} {}", std::mem::size_of::<Door<Open>>(), '
                 'std::mem::size_of::<Door<Closed>>());\n'
                 '    println!("{} {}", std::mem::size_of::<Open>(), '
                 'std::mem::size_of::<PhantomData<Closed>>());\n'
                 '}\n',
       'hint': 'Состояние хранится только в типе: PhantomData ничего не занимает, поэтому размер Door равен '
               'размеру счётчика.',
       'expected': ['1', '3', '4 4', '0 0']},
      {'id': 'r19-top-n',
       'mode': 'rust',
       'title': 'Обобщённый топ-N по трейту',
       'statement': 'Трейт Scored: score(&self) → i64. top_n<T: Scored + Clone>(items: &[T], n: usize) → '
                    'Vec<T>: n лучших по убыванию счёта (при равных счетах сохраняется исходный порядок — '
                    'сортировка устойчива). best<T: Scored>(items: &[T]) → Option<&T>: первый элемент с '
                    'наибольшим счётом. Player { name, points } реализует Scored.',
       'starter': 'trait Scored {\n'
                  '    fn score(&self) -> i64;\n'
                  '}\n'
                  '\n'
                  '#[derive(Debug, Clone)]\n'
                  'struct Player {\n'
                  '    name: String,\n'
                  '    points: i64,\n'
                  '}\n'
                  '\n'
                  '// impl Scored for Player\n'
                  '\n'
                  'fn top_n<T: Scored + Clone>(items: &[T], n: usize) -> Vec<T> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn best<T: Scored>(items: &[T]) -> Option<&T> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let p = |n: &str, s| Player { name: n.to_string(), points: s };\n'
                 '    let v = vec![p("ann", 50), p("bob", 80), p("cat", 80), p("dan", 10), p("eve", 65)];\n'
                 '    let top = top_n(&v, 3);\n'
                 '    let names: Vec<&str> = top.iter().map(|x| x.name.as_str()).collect();\n'
                 '    println!("{:?}", names);\n'
                 '    println!("{:?}", top_n(&v, 10).len());\n'
                 '    println!("{:?}", best(&v).map(|x| &x.name));\n'
                 '    println!("{:?}", best::<Player>(&[]).is_none());\n'
                 '}\n',
       'hint': 'sort_by устойчив: для равных счетов порядок исходного среза сохраняется; truncate(n) '
               'оставляет первые n.',
       'expected': ['["bob", "cat", "eve"]', '5', 'Some("bob")', 'true']}]}
