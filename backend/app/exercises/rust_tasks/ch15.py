"""Задачи книги «Изучаем Rust»: глава 15 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {15: [{'id': 'r15-drop-impl',
       'mode': 'rust',
       'title': 'Drop: убираем за собой',
       'statement': 'Тип Guard хранит имя. Реализуйте для него Drop так, чтобы при уничтожении печаталась '
                    'строка «drop <имя>». Остальное сделает компилятор: он сам вставит вызовы на закрывающих '
                    'скобках и в обратном порядке.',
       'starter': 'struct Guard {\n'
                  '    name: String,\n'
                  '}\n'
                  '\n'
                  'impl Drop for Guard {\n'
                  '    fn drop(&mut self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let _a = Guard { name: String::from("a") };\n'
                 '    {\n'
                 '        let _b = Guard { name: String::from("b") };\n'
                 '        let _c = Guard { name: String::from("c") };\n'
                 '        println!("inner");\n'
                 '    }\n'
                 '    let d = Guard { name: String::from("d") };\n'
                 '    drop(d);\n'
                 '    println!("end");\n'
                 '}\n',
       'hint': 'В drop достаточно println!("drop {}", self.name); вызывать его самому не нужно.',
       'expected': ['inner', 'drop c', 'drop b', 'drop d', 'end', 'drop a']},
      {'id': 'r15-scope-order',
       'mode': 'rust',
       'title': 'Порядок уничтожения: режиссируем вывод',
       'statement': 'Тип Guard уже готов: new печатает «make <имя>», а при уничтожении печатается «drop '
                    '<имя>». Напишите функцию scenario(), чтобы программа напечатала ровно такие строки: '
                    'make a, make b, drop b, mid, make c, drop c, end, drop a. Подсказка: что-то нужно '
                    'уничтожить вручную, что-то — закрывающей скобкой блока.',
       'starter': "struct Guard(&'static str);\n"
                  '\n'
                  'impl Guard {\n'
                  "    fn new(name: &'static str) -> Guard {\n"
                  '        println!("make {name}");\n'
                  '        Guard(name)\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Drop for Guard {\n'
                  '    fn drop(&mut self) {\n'
                  '        println!("drop {}", self.0);\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn scenario() {\n'
                  '    // ваш код\n'
                  '}\n',
       'driver': 'fn main() {\n    scenario();\n}\n',
       'hint': 'drop(b) уничтожает b сразу; внутренний блок { … } уничтожает c на своей скобке; a живёт до '
               'конца функции.',
       'expected': ['make a', 'make b', 'drop b', 'mid', 'make c', 'drop c', 'end', 'drop a']},
      {'id': 'r15-move-fix',
       'mode': 'rust',
       'title': 'Исправьте: значение использовано после переезда',
       'statement': 'Код не компилируется: let upper = name; перемещает строку, и дальше name использовать '
                    'нельзя. Исправьте describe так, чтобы функция возвращала «<исходная> -> <заглавными>»: '
                    'например, «rust -> RUST».',
       'starter': 'fn describe(name: String) -> String {\n'
                  '    let upper = name;\n'
                  '    format!("{} -> {}", name, upper.to_uppercase())\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", describe(String::from("rust")));\n'
                 '    println!("{}", describe(String::from("привет")));\n'
                 '}\n',
       'hint': 'Нужны две независимые строки — значит, одну из них создайте через .clone().',
       'expected': ['rust -> RUST', 'привет -> ПРИВЕТ']},
      {'id': 'r15-return-ownership',
       'mode': 'rust',
       'title': 'Вернуть владение: кортеж и цепочка',
       'statement': 'Функции забирают строку по значению. exclaim(s) дописывает в конец «!» и возвращает '
                    'строку. measure(s) возвращает пару (строка, длина в байтах), чтобы вызывающий не '
                    'потерял владение.',
       'starter': 'fn exclaim(s: String) -> String {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn measure(s: String) -> (String, usize) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let s = String::from("привет");\n'
                 '    let s = exclaim(s);\n'
                 '    let (s, n) = measure(s);\n'
                 '    println!("{s} {n}");\n'
                 '    let (s, n) = measure(exclaim(s));\n'
                 '    println!("{s} {n}");\n'
                 '}\n',
       'hint': 'Параметр, который меняется, объявляют как mut s. Длину возьмите до того, как отдадите s в '
               'кортеж.',
       'expected': ['привет! 13', 'привет!! 14']},
      {'id': 'r15-array-copy',
       'mode': 'rust',
       'title': 'Массивы и кортежи копируются',
       'statement': 'Массив [i32; 4] и кортеж (i32, i32) целиком лежат на стеке и копируются побитно. '
                    'Напишите doubled(a) — массив с удвоенными элементами и swapped(p) — кортеж с '
                    'переставленными местами числами. После вызова исходные значения остаются доступными.',
       'starter': 'fn doubled(a: [i32; 4]) -> [i32; 4] {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn swapped(p: (i32, i32)) -> (i32, i32) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a = [1, 2, 3, 4];\n'
                 '    let b = doubled(a);\n'
                 '    println!("{:?} {:?}", a, b);\n'
                 '    let p = (7, 9);\n'
                 '    let q = swapped(p);\n'
                 '    println!("{:?} {:?}", p, q);\n'
                 '}\n',
       'hint': 'Параметр mut a — это локальная копия; исходный массив у вызывающего не меняется.',
       'expected': ['[1, 2, 3, 4] [2, 4, 6, 8]', '(7, 9) (9, 7)']},
      {'id': 'r15-derive-copy',
       'mode': 'rust',
       'title': 'Исправьте: сделайте Point копируемым',
       'statement': 'Код не компилируется: Point переезжает в shift, а потом используется снова. Тип состоит '
                    'из двух i32, поэтому его можно сделать Copy. Правьте только атрибут derive над '
                    'структурой (Debug нужен для вывода).',
       'starter': '#[derive(Debug)]\n'
                  'struct Point {\n'
                  '    x: i32,\n'
                  '    y: i32,\n'
                  '}\n'
                  '\n'
                  'fn shift(p: Point, dx: i32, dy: i32) -> Point {\n'
                  '    Point { x: p.x + dx, y: p.y + dy }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let p = Point { x: 1, y: 2 };\n'
                 '    let q = shift(p, 10, 20);\n'
                 '    println!("{:?} {:?}", p, q);\n'
                 '    println!("{} байт", std::mem::size_of::<Point>());\n'
                 '}\n',
       'hint': '#[derive(Debug, Clone, Copy)] — Copy требует и Clone.',
       'expected': ['Point { x: 1, y: 2 } Point { x: 11, y: 22 }', '8 байт']},
      {'id': 'r15-two-clones',
       'mode': 'rust',
       'title': 'Ровно два клона',
       'statement': 'Напишите triple(s) → (String, String, String): три одинаковые строки. Условие: в коде '
                    'ровно два вызова .clone() — третья строка получается перемещением самой s. Каждый '
                    'лишний клон — лишний malloc и memcpy.',
       'starter': 'fn triple(s: String) -> (String, String, String) {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                 '    println!("{:?}", triple(String::from("ab")));\n'
                 '    let (x, y, z) = triple(String::from("xyz"));\n'
                 '    println!("{}", x == y && y == z);\n'
                 '    println!("clones: {}", bad0);\n'
                 '}\n',
       'hint': 'Порядок важен: сначала клоны, а последним — сама s, которая переезжает в кортеж.',
       'expected': ['("ab", "ab", "ab")', 'true', 'clones: 2']},
      {'id': 'r15-box-new',
       'mode': 'rust',
       'title': 'Box: значение в куче',
       'statement': 'Напишите boxed_sum(a, b) → Box<i32> с суммой, положенной в кучу, и unbox_double(b: '
                    'Box<i32>) → i32: удвоенное значение из коробки (звёздочка разыменовывает Box).',
       'starter': 'fn boxed_sum(a: i32, b: i32) -> Box<i32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn unbox_double(b: Box<i32>) -> i32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let b = boxed_sum(20, 22);\n'
                 '    println!("{}", b);\n'
                 '    println!("{}", unbox_double(b));\n'
                 '    println!("{} {} {}", std::mem::size_of::<i32>(), std::mem::size_of::<Box<i32>>(), '
                 'std::mem::size_of::<String>());\n'
                 '}\n',
       'hint': 'Box::new(значение) кладёт значение в кучу; *b достаёт его обратно.',
       'expected': ['42', '84', '4 8 24']},
      {'id': 'r15-box-list',
       'mode': 'rust',
       'title': 'Список на Box: рекурсивный тип',
       'statement': 'Перечисление List хранит голову и хвост в Box. Напишите range_list(from, to) — список '
                    'from, from+1, …, to (включительно; пустой, если from > to), sum(list) — сумму, '
                    'to_vec(list) — элементы в порядке списка. Функции забирают список по значению.',
       'starter': 'enum List {\n'
                  '    Cons(i32, Box<List>),\n'
                  '    Nil,\n'
                  '}\n'
                  'use List::{Cons, Nil};\n'
                  '\n'
                  'fn range_list(from: i32, to: i32) -> List {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn sum(list: List) -> i32 {\n'
                  '    match list {\n'
                  '        Nil => todo!(),\n'
                  '        Cons(v, rest) => todo!(),\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn to_vec(list: List) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", sum(range_list(1, 10)));\n'
                 '    println!("{:?}", to_vec(range_list(3, 7)));\n'
                 '    println!("{:?} {}", to_vec(range_list(5, 1)), sum(Nil));\n'
                 '    println!("{}", std::mem::size_of::<Box<List>>());\n'
                 '}\n',
       'hint': '*rest достаёт список из коробки и переносит владение; на Nil рекурсия заканчивается.',
       'expected': ['55', '[3, 4, 5, 6, 7]', '[] 0', '8']},
      {'id': 'r15-recursive-fix',
       'mode': 'rust',
       'title': 'Исправьте: тип бесконечного размера',
       'statement': 'Выражение Expr содержит другие выражения прямо внутри себя — размер такого типа '
                    'бесконечен, и код не собирается. Исправьте определение enum (функция eval и её *a, *b '
                    'уже написаны для Box).',
       'starter': 'enum Expr {\n'
                  '    Num(i64),\n'
                  '    Add(Expr, Expr),\n'
                  '    Mul(Expr, Expr),\n'
                  '}\n'
                  '\n'
                  'fn eval(e: Expr) -> i64 {\n'
                  '    match e {\n'
                  '        Expr::Num(n) => n,\n'
                  '        Expr::Add(a, b) => eval(*a) + eval(*b),\n'
                  '        Expr::Mul(a, b) => eval(*a) * eval(*b),\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    use Expr::*;\n'
                 '    let e = Add(Box::new(Num(2)), Box::new(Mul(Box::new(Num(3)), Box::new(Num(4)))));\n'
                 '    println!("{}", eval(e));\n'
                 '    println!("{}", eval(Mul(Box::new(Num(-5)), Box::new(Num(6)))));\n'
                 '}\n',
       'hint': 'Рекурсивные поля нужно положить в Box<Expr>: тогда размер определяется указателем.',
       'expected': ['14', '-30']},
      {'id': 'r15-field-order',
       'mode': 'rust',
       'title': 'Порядок полей — порядок drop',
       'statement': 'Поля структуры уничтожаются в порядке объявления. Сейчас при уничтожении Pair сначала '
                    'печатается «drop right». Измените определение структуры (конструктор new не трогайте) '
                    'так, чтобы сначала шло «drop left», а затем «drop right».',
       'starter': "struct Guard(&'static str);\n"
                  '\n'
                  'impl Guard {\n'
                  "    fn new(name: &'static str) -> Guard {\n"
                  '        println!("make {name}");\n'
                  '        Guard(name)\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Drop for Guard {\n'
                  '    fn drop(&mut self) {\n'
                  '        println!("drop {}", self.0);\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'struct Pair {\n'
                  '    right: Guard,\n'
                  '    left: Guard,\n'
                  '}\n'
                  '\n'
                  'impl Pair {\n'
                  '    fn new() -> Pair {\n'
                  '        let left = Guard::new("left");\n'
                  '        let right = Guard::new("right");\n'
                  '        Pair { right, left }\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    {\n'
                 '        let _p = Pair::new();\n'
                 '        println!("alive");\n'
                 '    }\n'
                 '    println!("done");\n'
                 '}\n',
       'hint': 'Поля структуры освобождаются сверху вниз, как они записаны в определении.',
       'expected': ['make left', 'make right', 'alive', 'drop left', 'drop right', 'done']},
      {'id': 'r15-option-take',
       'mode': 'rust',
       'title': 'Option::take: вынуть и оставить None',
       'statement': 'Структура Slot хранит необязательную строку. Реализуйте put(&mut self, s) — положить '
                    'строку и вернуть прежнюю (Option<String>), take(&mut self) — забрать строку, оставив '
                    'None, и is_empty(&self). Подсказка: у Option есть методы replace и take. Ссылки &self и '
                    '&mut self — тема следующей главы: пока считайте их разрешением читать или менять Slot '
                    'на месте.',
       'starter': 'struct Slot {\n'
                  '    item: Option<String>,\n'
                  '}\n'
                  '\n'
                  'impl Slot {\n'
                  '    fn put(&mut self, s: String) -> Option<String> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn take(&mut self) -> Option<String> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn is_empty(&self) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut s = Slot { item: None };\n'
                 '    println!("{:?}", s.put(String::from("a")));\n'
                 '    println!("{:?}", s.put(String::from("b")));\n'
                 '    println!("{:?}", s.take());\n'
                 '    println!("{:?} {}", s.take(), s.is_empty());\n'
                 '}\n',
       'hint': 'self.item.replace(s) и self.item.take() возвращают старое значение, не копируя его.',
       'expected': ['None', 'Some("a")', 'Some("b")', 'None true']},
      {'id': 'r15-mem-swap',
       'mode': 'rust',
       'title': 'mem::swap и mem::take',
       'statement': 'rotate(a, b, c) сдвигает значения по кругу: a получает значение b, b — значение c, c — '
                    'прежнее значение a. Копировать строки нельзя — используйте std::mem::swap. drain(log) '
                    'возвращает содержимое строки и оставляет её пустой (std::mem::take).',
       'starter': 'fn rotate(a: &mut String, b: &mut String, c: &mut String) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn drain(log: &mut String) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut a = String::from("1");\n'
                 '    let mut b = String::from("2");\n'
                 '    let mut c = String::from("3");\n'
                 '    rotate(&mut a, &mut b, &mut c);\n'
                 '    println!("{a} {b} {c}");\n'
                 '    let mut log = String::from("boot ok");\n'
                 '    let got = drain(&mut log);\n'
                 '    println!("{:?} {:?}", got, log);\n'
                 '}\n',
       'hint': 'Два свопа подряд: сначала (a, b), затем (b, c). mem::take оставляет String::default(), то '
               'есть пустую строку.',
       'expected': ['2 3 1', '"boot ok" ""']},
      {'id': 'r15-rc-count',
       'mode': 'rust',
       'title': 'Rc: много владельцев одного значения',
       'statement': 'Напишите share(s, n) → Vec<Rc<String>> (n ≥ 1): вектор из n владельцев ОДНОЙ строки в '
                    'куче. Данные копироваться не должны: создайте один Rc, а остальные получите через '
                    'Rc::clone.',
       'starter': 'use std::rc::Rc;\n\nfn share(s: &str, n: usize) -> Vec<Rc<String>> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    let v = share("hello", 4);\n'
                 '    println!("{} {}", v.len(), Rc::strong_count(&v[0]));\n'
                 '    println!("{}", v.iter().all(|r| Rc::ptr_eq(r, &v[0])));\n'
                 '    println!("{}", v[3]);\n'
                 '    drop(v);\n'
                 '}\n',
       'hint': 'Rc::clone(&first) увеличивает счётчик и не копирует строку; последний владелец — сама first.',
       'expected': ['4 4', 'true', 'hello']},
      {'id': 'r15-rc-drop',
       'mode': 'rust',
       'title': 'Rc: уничтожение при последнем владельце',
       'statement': 'Guard печатает «drop shared», когда уничтожается. Напишите fan_out(g, n) → '
                    'Vec<Rc<Guard>> (n ≥ 1): n владельцев одного Guard, исходный g перемещается внутрь (клон '
                    'создаёт ещё одного владельца, перемещение — нет).',
       'starter': 'use std::rc::Rc;\n'
                  '\n'
                  "struct Guard(&'static str);\n"
                  '\n'
                  'impl Drop for Guard {\n'
                  '    fn drop(&mut self) {\n'
                  '        println!("drop {}", self.0);\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn fan_out(g: Rc<Guard>, n: usize) -> Vec<Rc<Guard>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut v = fan_out(Rc::new(Guard("shared")), 3);\n'
                 '    println!("owners: {}", Rc::strong_count(&v[0]));\n'
                 '    v.pop();\n'
                 '    println!("owners: {}", Rc::strong_count(&v[0]));\n'
                 '    v.pop();\n'
                 '    println!("owners: {}", Rc::strong_count(&v[0]));\n'
                 '    println!("last");\n'
                 '    v.pop();\n'
                 '    println!("end");\n'
                 '}\n',
       'hint': 'Значение уничтожается ровно один раз — когда счётчик достигает нуля. Лишних клонов быть не '
               'должно.',
       'expected': ['owners: 3', 'owners: 2', 'owners: 1', 'last', 'drop shared', 'end']},
      {'id': 'r15-loop-move',
       'mode': 'rust',
       'title': 'Исправьте: значение переехало в первой итерации',
       'statement': 'Функция repeat должна вернуть n копий строки. Компилятор ругается: s перемещена в push '
                    'на первой итерации цикла. Исправьте минимальной правкой.',
       'starter': 'fn repeat(s: String, n: usize) -> Vec<String> {\n'
                  '    let mut v = Vec::new();\n'
                  '    for _ in 0..n {\n'
                  '        v.push(s);\n'
                  '    }\n'
                  '    v\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", repeat(String::from("ab"), 3));\n'
                 '    println!("{:?}", repeat(String::from("x"), 0));\n'
                 '}\n',
       'hint': 'В каждую ячейку нужна своя строка: push(s.clone()).',
       'expected': ['["ab", "ab", "ab"]', '[]']},
      {'id': 'r15-index-move',
       'mode': 'rust',
       'title': 'Исправьте: нельзя вынуть элемент по индексу',
       'statement': 'split_first(names) → (String, Vec<String>): первое имя и оставшиеся. names[0] не '
                    'компилируется — из вектора нельзя вынуть владение по индексу. Исправьте, не используя '
                    'clone: у Vec есть метод, который удаляет элемент и отдаёт его владельцу.',
       'starter': 'fn split_first(mut names: Vec<String>) -> (String, Vec<String>) {\n'
                  '    let first = names[0];\n'
                  '    names.remove(0);\n'
                  '    (first, names)\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                 '    let (first, rest) = split_first(vec![String::from("anna"), String::from("bob"), '
                 'String::from("carl")]);\n'
                 '    println!("first={first} rest={:?}", rest);\n'
                 '    println!("clones: {}", bad0);\n'
                 '}\n',
       'hint': 'remove(0) удаляет элемент и возвращает его — владение переходит к вам.',
       'expected': ['first=anna rest=["bob", "carl"]', 'clones: 0']},
      {'id': 'r15-pipeline',
       'mode': 'rust',
       'title': 'Конвейер: владение перетекает из функции в функцию',
       'statement': 'Напишите три функции, которые забирают вектор и возвращают его: append(v, x) — добавить '
                    'в конец; dedup_sorted(v) — отсортировать по возрастанию и убрать повторы; top(v, k) — '
                    'оставить k наибольших в порядке убывания.',
       'starter': 'fn append(v: Vec<i32>, x: i32) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn dedup_sorted(v: Vec<i32>) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn top(v: Vec<i32>, k: usize) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let v = vec![5, 3, 5, 1, 9];\n'
                 '    let v = append(append(v, 7), 3);\n'
                 '    let v = dedup_sorted(v);\n'
                 '    println!("{:?}", v);\n'
                 '    println!("{:?}", top(v, 3));\n'
                 '    println!("{:?}", top(dedup_sorted(vec![2, 2, 1]), 5));\n'
                 '}\n',
       'hint': 'Параметр с mut можно менять внутри; после изменения верните его, и владение уйдёт дальше по '
               'цепочке.',
       'expected': ['[1, 3, 5, 7, 9]', '[9, 7, 5]', '[2, 1]']},
      {'id': 'r15-struct-update',
       'mode': 'rust',
       'title': 'Структура: пересобрать с новым полем',
       'statement': 'Config владеет строкой. with_name(c, name) возвращает конфигурацию с новым именем и '
                    'остальными полями прежними — используйте синтаксис обновления структуры «..c». '
                    'into_parts(c) разбирает конфигурацию на (имя, число попыток).',
       'starter': '#[derive(Debug)]\n'
                  'struct Config {\n'
                  '    name: String,\n'
                  '    retries: u32,\n'
                  '    verbose: bool,\n'
                  '}\n'
                  '\n'
                  'fn with_name(c: Config, name: &str) -> Config {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn into_parts(c: Config) -> (String, u32) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let c = Config { name: String::from("old"), retries: 3, verbose: true };\n'
                 '    let c = with_name(c, "new");\n'
                 '    println!("{:?}", c);\n'
                 '    println!("{:?}", into_parts(c));\n'
                 '}\n',
       'hint': 'Config { name: ..., ..c } берёт недостающие поля из c; старое имя при этом просто '
               'уничтожится.',
       'expected': ['Config { name: "new", retries: 3, verbose: true }', '("new", 3)']},
      {'id': 'r15-shadow-drop',
       'mode': 'rust',
       'title': 'RAII: блокировка отпускается сама',
       'statement': 'Lock имитирует блокировку: Lock::acquire(name) печатает «lock <name>» и возвращает '
                    'значение, а при уничтожении печатается «unlock <name>». Реализуйте acquire и Drop. '
                    'Следите за затенением: второй let l не уничтожает первую блокировку.',
       'starter': 'struct Lock {\n'
                  '    name: String,\n'
                  '}\n'
                  '\n'
                  'impl Lock {\n'
                  '    fn acquire(name: &str) -> Lock {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Drop for Lock {\n'
                  '    fn drop(&mut self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let l = Lock::acquire("A");\n'
                 '    let l = Lock::acquire("B");\n'
                 '    {\n'
                 '        let _x = Lock::acquire("C");\n'
                 '    }\n'
                 '    println!("body {}", l.name);\n'
                 '}\n',
       'hint': 'Затенение скрывает имя, но не уничтожает значение: A живёт до конца функции и освобождается '
               'последней.',
       'expected': ['lock A', 'lock B', 'lock C', 'unlock C', 'body B', 'unlock B', 'unlock A']},
      {'id': 'r15-underscore',
       'mode': 'rust',
       'title': 'Подчёркивание: _ и _name',
       'statement': 'Guard печатает «make <имя>» при создании и «drop <имя>» при уничтожении. Напишите '
                    'probe() так, чтобы вывод был: make temp, drop temp, make keep, body, drop keep. '
                    'Значение, присвоенное голому «_», уничтожается сразу; значение в переменной _keep живёт '
                    'до конца блока.',
       'starter': "struct Guard(&'static str);\n"
                  '\n'
                  'impl Guard {\n'
                  "    fn new(name: &'static str) -> Guard {\n"
                  '        println!("make {name}");\n'
                  '        Guard(name)\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'impl Drop for Guard {\n'
                  '    fn drop(&mut self) {\n'
                  '        println!("drop {}", self.0);\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn probe() {\n'
                  '    // ваш код\n'
                  '}\n',
       'driver': 'fn main() {\n    probe();\n}\n',
       'hint': 'let _ = … не создаёт привязки, значение умирает на этой же строке; let _keep = … привязку '
               'создаёт.',
       'expected': ['make temp', 'drop temp', 'make keep', 'body', 'drop keep']},
      {'id': 'r15-sizes',
       'mode': 'rust',
       'title': 'Copy или нет: три типа',
       'statement': 'Опишите три типа. Meters(f64) — копируемый. Segment { from: Meters, to: Meters } — тоже '
                    'копируемый. Label { text: String } — не копируемый (владеет кучей). Добавьте нужные '
                    'derive к определениям. Программа проверит Copy и напечатает размеры: 8, 24 и 16 байт.',
       'starter': 'struct Meters(f64);\n'
                  '\n'
                  'struct Segment {\n'
                  '    from: Meters,\n'
                  '    to: Meters,\n'
                  '}\n'
                  '\n'
                  'struct Label {\n'
                  '    text: String,\n'
                  '}\n',
       'driver': 'fn need_copy<T: Copy>(_: T) {}\n'
                 '\n'
                 'fn main() {\n'
                 '    need_copy(Meters(1.5));\n'
                 '    need_copy(Segment { from: Meters(0.0), to: Meters(2.0) });\n'
                 '    let l = Label { text: String::from("a") };\n'
                 '    let _m = l;\n'
                 '    println!("{} {} {}", std::mem::size_of::<Meters>(), std::mem::size_of::<Label>(), '
                 'std::mem::size_of::<Segment>());\n'
                 '}\n',
       'hint': 'Copy можно получить только у типа, все поля которого Copy; для Copy нужен ещё и Clone: '
               '#[derive(Clone, Copy)].',
       'expected': ['8 24 16']},
      {'id': 'r15-capacity',
       'mode': 'rust',
       'title': 'Ёмкость растёт: String::push',
       'statement': 'Напишите capacity_trace(n) → Vec<usize>: создайте пустую String::new(), n раз добавьте '
                    "символ 'x' и верните все различные значения ёмкости (capacity) в порядке появления, "
                    'начиная с начальной. Видно, как буфер в куче растёт рывками, а не на каждом символе.',
       'starter': 'fn capacity_trace(n: usize) -> Vec<usize> {\n    todo!()\n}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", capacity_trace(0));\n'
                 '    println!("{:?}", capacity_trace(100));\n'
                 '    println!("{:?}", capacity_trace(1000));\n'
                 '}\n',
       'hint': 'Запоминайте последнее увиденное значение ёмкости и добавляйте новое только если оно '
               'изменилось.',
       'expected': ['[0]', '[0, 8, 16, 32, 64, 128]', '[0, 8, 16, 32, 64, 128, 256, 512, 1024]']},
      {'id': 'r15-move-ptr',
       'mode': 'rust',
       'title': 'Переезд не трогает кучу',
       'statement': 'as_ptr() возвращает адрес буфера в куче. move_keeps_buffer(s) переносит строку в новую '
                    'переменную и возвращает, остался ли адрес буфера тем же (true). clone_new_buffer(s) '
                    'клонирует строку и возвращает, отличается ли адрес копии от адреса оригинала (true).',
       'starter': 'fn move_keeps_buffer(s: String) -> bool {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn clone_new_buffer(s: String) -> bool {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{}", move_keeps_buffer(String::from("hello world")));\n'
                 '    println!("{}", clone_new_buffer(String::from("hello world")));\n'
                 '}\n',
       'hint': 'Запомните s.as_ptr() до переезда и сравните с as_ptr() у новой переменной.',
       'expected': ['true', 'true']},
      {'id': 'r15-stack-list',
       'mode': 'rust',
       'title': 'Стек на связном списке из Box',
       'statement': 'Реализуйте стек на односвязном списке. Stack::new() — пустой; push(v) кладёт значение в '
                    'начало; pop() снимает и возвращает Option<i32>; peek(&self) показывает верхнее без '
                    'снятия. Хранится голова Option<Box<Node>>: при push старую голову забирайте через '
                    'take().',
       'starter': 'struct Node {\n'
                  '    val: i32,\n'
                  '    next: Option<Box<Node>>,\n'
                  '}\n'
                  '\n'
                  'struct Stack {\n'
                  '    head: Option<Box<Node>>,\n'
                  '}\n'
                  '\n'
                  'impl Stack {\n'
                  '    fn new() -> Stack {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn push(&mut self, v: i32) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn pop(&mut self) -> Option<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '\n'
                  '    fn peek(&self) -> Option<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut s = Stack::new();\n'
                 '    println!("{:?} {:?}", s.pop(), s.peek());\n'
                 '    for i in 1..=4 {\n'
                 '        s.push(i * 10);\n'
                 '    }\n'
                 '    println!("{:?}", s.peek());\n'
                 '    println!("{:?} {:?}", s.pop(), s.pop());\n'
                 '    s.push(99);\n'
                 '    let mut out = Vec::new();\n'
                 '    while let Some(v) = s.pop() {\n'
                 '        out.push(v);\n'
                 '    }\n'
                 '    println!("{:?} {:?}", out, s.peek());\n'
                 '}\n',
       'hint': 'push: let old = self.head.take(); затем self.head = Some(Box::new(Node { val: v, next: old '
               '})). pop: take() и перенос n.next в head.',
       'expected': ['None None', 'Some(40)', 'Some(40) Some(30)', '[99, 20, 10] None']},
      {'id': 'r15-reverse-list',
       'mode': 'rust',
       'title': 'Разворот списка перемещениями',
       'statement': 'Напишите reverse(head) → Option<Box<Node>>: разверните односвязный список, не создавая '
                    'новых узлов и не клонируя — только переставляя указатели (владение узлов переходит по '
                    'цепочке). Условие: ни одного .clone().',
       'starter': 'struct Node {\n'
                  '    val: i32,\n'
                  '    next: Option<Box<Node>>,\n'
                  '}\n'
                  '\n'
                  'fn reverse(head: Option<Box<Node>>) -> Option<Box<Node>> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn build(v: &[i32]) -> Option<Box<Node>> {\n'
                 '    let mut head = None;\n'
                 '    for &x in v.iter().rev() {\n'
                 '        head = Some(Box::new(Node { val: x, next: head }));\n'
                 '    }\n'
                 '    head\n'
                 '}\n'
                 '\n'
                 'fn dump(mut l: Option<Box<Node>>) -> Vec<i32> {\n'
                 '    let mut out = Vec::new();\n'
                 '    while let Some(n) = l {\n'
                 '        out.push(n.val);\n'
                 '        l = n.next;\n'
                 '    }\n'
                 '    out\n'
                 '}\n'
                 '\n'
                 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                 '    println!("{:?}", dump(reverse(build(&[1, 2, 3, 4, 5]))));\n'
                 '    println!("{:?}", dump(reverse(build(&[7]))));\n'
                 '    println!("{:?}", dump(reverse(build(&[]))));\n'
                 '    println!("clones: {}", bad0);\n'
                 '}\n',
       'hint': 'Идём по списку: отцепляем хвост через node.next.take(), направляем next на уже развёрнутую '
               'часть, и node становится новой головой.',
       'expected': ['[5, 4, 3, 2, 1]', '[7]', '[]', 'clones: 0']},
      {'id': 'r15-bst-insert',
       'mode': 'rust',
       'title': 'Двоичное дерево на Option<Box<…>>',
       'statement': 'Узел дерева владеет левым и правым поддеревом через Option<Box<TNode>>. Напишите '
                    'insert(link, key) → Link: вставка в дерево поиска (повторы игнорируются), функция '
                    'забирает дерево и возвращает его обратно; и in_order(link, out) — обход слева направо с '
                    'записью ключей в out. Подсказка: поддерево перед рекурсией забирайте через take().',
       'starter': 'struct TNode {\n'
                  '    key: i32,\n'
                  '    left: Link,\n'
                  '    right: Link,\n'
                  '}\n'
                  '\n'
                  'type Link = Option<Box<TNode>>;\n'
                  '\n'
                  'fn insert(link: Link, key: i32) -> Link {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn in_order(link: Link, out: &mut Vec<i32>) {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut root: Link = None;\n'
                 '    for k in [5, 3, 8, 1, 4, 7, 9, 3, 5] {\n'
                 '        root = insert(root, k);\n'
                 '    }\n'
                 '    let mut out = Vec::new();\n'
                 '    in_order(root, &mut out);\n'
                 '    println!("{:?}", out);\n'
                 '    let mut empty = Vec::new();\n'
                 '    in_order(None, &mut empty);\n'
                 '    println!("{}", empty.len());\n'
                 '}\n',
       'hint': 'Some(mut n) → сравните ключи, перезапишите n.left или n.right результатом '
               'insert(n.left.take(), key) и верните Some(n).',
       'expected': ['[1, 3, 4, 5, 7, 8, 9]', '0']},
      {'id': 'r15-rc-tail',
       'mode': 'rust',
       'title': 'Rc: общий хвост у двух списков',
       'statement': 'Cons-список, у которого хвост лежит в Rc. Напишите shared_tail() → (Rc<List>, Rc<List>, '
                    'Rc<List>): хвост [10] и два списка a = 1 → хвост, b = 2 → хвост, которые делят один '
                    'хвост без копирования (вернуть кортеж (tail, a, b)). И sum(&List) — сумма элементов.',
       'starter': 'use std::rc::Rc;\n'
                  '\n'
                  'enum List {\n'
                  '    Cons(i32, Rc<List>),\n'
                  '    Nil,\n'
                  '}\n'
                  'use List::{Cons, Nil};\n'
                  '\n'
                  'fn shared_tail() -> (Rc<List>, Rc<List>, Rc<List>) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn sum(l: &List) -> i32 {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let (tail, a, b) = shared_tail();\n'
                 '    println!("{}", Rc::strong_count(&tail));\n'
                 '    println!("{} {} {}", sum(&tail), sum(&a), sum(&b));\n'
                 '    drop(a);\n'
                 '    println!("{}", Rc::strong_count(&tail));\n'
                 '}\n',
       'hint': 'Хвост создайте один раз и в каждый из двух списков отдайте Rc::clone(&tail): счётчик хвоста '
               'станет 3.',
       'expected': ['3', '10 11 12', '2']},
      {'id': 'r15-sizeof',
       'mode': 'rust',
       'title': 'Размеры типов: стек и куча',
       'statement': 'Напишите sizes() → [usize; 7]: std::mem::size_of для типов u8, i32, Box<i32>, String, '
                    'Vec<u8>, Option<Box<i32>>, Option<i32> — именно в этом порядке. Обратите внимание на 24 '
                    'байта у String и Vec (три слова) и на то, что Option<Box<i32>> не толще указателя.',
       'starter': 'fn sizes() -> [usize; 7] {\n    todo!()\n}\n',
       'driver': 'fn main() {\n    println!("{:?}", sizes());\n}\n',
       'hint': 'size_of::<Тип>() — дженерик-функция из std::mem; тип пишут в угловых скобках.',
       'expected': ['[1, 4, 8, 24, 24, 8, 8]']},
      {'id': 'r15-moved-args',
       'mode': 'rust',
       'title': 'Исправьте: аргументы переехали в longest',
       'statement': 'report возвращает «<самая длинная> (из <a> и <b>)». Но longest забирает обе строки, и в '
                    'format! их уже нет. Исправьте report: нужны ровно два клона, а longest менять не нужно.',
       'starter': 'fn longest(a: String, b: String) -> String {\n'
                  '    if a.len() >= b.len() { a } else { b }\n'
                  '}\n'
                  '\n'
                  'fn report(a: String, b: String) -> String {\n'
                  '    let winner = longest(a, b);\n'
                  '    format!("{winner} (из {a} и {b})")\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                 '    println!("{}", report(String::from("apple"), String::from("fig")));\n'
                 '    println!("{}", report(String::from("kiwi"), String::from("plum")));\n'
                 '    println!("clones: {}", bad0);\n'
                 '}\n',
       'hint': 'longest(a.clone(), b.clone()) отдаёт функции копии, а оригиналы остаются у report.',
       'expected': ['apple (из apple и fig)', 'kiwi (из kiwi и plum)', 'clones: 2']}]}
