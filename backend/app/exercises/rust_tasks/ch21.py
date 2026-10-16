"""Задачи книги «Изучаем Rust»: глава 21 (код проверяется rustc в песочнице; драйвер — скрытая функция main)."""

TASKS: dict[int, list[dict]] = {21: [{'id': 'r21-longest',
       'mode': 'rust',
       'title': 'Метки времени жизни: longest и пары',
       'statement': "longest<'a>(a, b) → &'a str — более длинная по числу символов (при равенстве первая). "
                    "first_two<'a>(s) → (&'a str, &'a str) — первые два слова строки (пустая строка вместо "
                    "отсутствующего). shorter_of<'a>(words: &[&'a str]) → Option<&'a str> — самое короткое "
                    'слово (первое при равенстве).',
       'starter': "fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {\n"
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  "fn first_two<'a>(s: &'a str) -> (&'a str, &'a str) {\n"
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  "fn shorter_of<'a>(words: &[&'a str]) -> Option<&'a str> {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{} {}", longest("привет", "hello"), longest("ab", "cd"));\n'
                 '    println!("{:?} {:?} {:?}", first_two("  one two three"), first_two("solo"), '
                 'first_two(""));\n'
                 '    println!("{:?} {:?}", shorter_of(&["pear", "fig", "kiwi", "fog"]), shorter_of(&[]));\n'
                 '}\n',
       'hint': "Метка 'a на всех ссылках говорит: результат живёт не дольше обоих аргументов; в shorter_of "
               "слова несут 'a внутри среза.",
       'expected': ['привет ab', '("one", "two") ("solo", "") ("", "")', 'Some("fig") None']},
      {'id': 'r21-two-lifetimes',
       'mode': 'rust',
       'title': 'Две независимые метки',
       'statement': "pick_first<'a, 'b>(a: &'a str, _b: &'b str) → &'a str всегда возвращает a. В драйвере "
                    'вторая строка умирает раньше результата — это допустимо только с ДВУМЯ метками. '
                    "Реализуйте также between<'a, 'b>(text: &'a str, left: &'b str, right: &'b str) → "
                    "Option<&'a str> — часть text между первым left и следующим right.",
       'starter': "fn pick_first<'a, 'b>(a: &'a str, _b: &'b str) -> &'a str {\n"
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  "fn between<'a, 'b>(text: &'a str, left: &'b str, right: &'b str) -> Option<&'a str> {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a = String::from("долгоживущая");\n'
                 '    let r;\n'
                 '    {\n'
                 '        let b = String::from("короткая");\n'
                 '        r = pick_first(&a, &b);\n'
                 '    }\n'
                 '    println!("{}", r);\n'
                 '    let text = String::from("x=[alpha]; y=[beta]");\n'
                 '    let found;\n'
                 '    {\n'
                 '        let (l, rr) = (String::from("["), String::from("]"));\n'
                 '        found = between(&text, &l, &rr);\n'
                 '    }\n'
                 '    println!("{:?}", found);\n'
                 '    println!("{:?} {:?}", between("no brackets", "[", "]"), between("[open", "[", "]"));\n'
                 '}\n',
       'hint': "Каждой ссылке — своя метка: результат привязан только к 'a, а 'b может закончиться раньше.",
       'expected': ['долгоживущая', 'Some("alpha")', 'None None']},
      {'id': 'r21-split-kv',
       'mode': 'rust',
       'title': 'Срезы без копирования: key=value',
       'statement': "split_kv<'a>(line: &'a str) → Option<(&'a str, &'a str)> — «ключ=значение»: ключ и "
                    'значение без пробелов по краям; None, если нет «=» или ключ пустой. '
                    "parse_lines<'a>(text: &'a str) → Vec<(&'a str, &'a str)> — все корректные строки. "
                    'Результат — срезы исходного текста, копий нет.',
       'starter': "fn split_kv<'a>(line: &'a str) -> Option<(&'a str, &'a str)> {\n"
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  "fn parse_lines<'a>(text: &'a str) -> Vec<(&'a str, &'a str)> {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?} {:?} {:?}", split_kv(" a = 1 "), split_kv("=x"), split_kv("novalue"));\n'
                 '    let text = String::from("host = example.org\\nbad line\\nport=8080\\n=oops\\nmode '
                 '=");\n'
                 '    let kv = parse_lines(&text);\n'
                 '    println!("{:?}", kv);\n'
                 '    let (k, _) = kv[0];\n'
                 '    let off = k.as_ptr() as usize - text.as_ptr() as usize;\n'
                 '    println!("указывает в исходный текст: {}", off < text.len());\n'
                 '}\n',
       'hint': 'trim() возвращает срез той же строки — копии не создаются; filter_map(split_kv) подходит, '
               'потому что split_kv принимает &str.',
       'expected': ['Some(("a", "1")) None None',
                    '[("host", "example.org"), ("port", "8080"), ("mode", "")]',
                    'указывает в исходный текст: true']},
      {'id': 'r21-tokens-iterator',
       'mode': 'rust',
       'title': "Итератор срезов: Tokens<'a>",
       'statement': "Tokens<'a> хранит остаток текста и выдаёт слова (непробельные куски) как &'a str — без "
                    "копирования. Реализуйте Tokens::new(text) и Iterator<Item = &'a str>. Слова должны быть "
                    'срезами исходной строки (тот же буфер).',
       'starter': "struct Tokens<'a> {\n"
                  "    rest: &'a str,\n"
                  '}\n'
                  '\n'
                  "impl<'a> Tokens<'a> {\n"
                  "    fn new(text: &'a str) -> Tokens<'a> {\n"
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  "impl<'a> Iterator for Tokens<'a> {\n"
                  "    type Item = &'a str;\n"
                  "    fn next(&mut self) -> Option<&'a str> {\n"
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let text = String::from("  привет  мир\\tи\\nвсе ");\n'
                 '    let words: Vec<&str> = Tokens::new(&text).collect();\n'
                 '    println!("{:?}", words);\n'
                 '    let inside = words.iter().all(|w| {\n'
                 '        let p = w.as_ptr() as usize;\n'
                 '        p >= text.as_ptr() as usize && p + w.len() <= text.as_ptr() as usize + text.len()\n'
                 '    });\n'
                 '    println!("{}", inside);\n'
                 '    println!("{}", Tokens::new("a b c d").count());\n'
                 '    println!("{:?}", Tokens::new("   ").next());\n'
                 '    println!("{:?}", Tokens::new("x").map(str::len).sum::<usize>());\n'
                 '}\n',
       'hint': "split_at(end) делит срез на слово и остаток — оба с тем же временем жизни 'a.",
       'expected': ['["привет", "мир", "и", "все"]', 'true', '4', 'None', '1']},
      {'id': 'r21-fix-capture',
       'mode': 'rust',
       'title': 'Исправьте: итератор захватывает ссылку',
       'statement': 'evens_of возвращает итератор по чётным числам вектора, но компилятор жалуется: скрытый '
                    'тип захватывает время жизни ссылки, которого нет в ограничениях. Допишите в сигнатуру '
                    'метку, связывающую итератор с аргументом.',
       'starter': 'fn evens_of(v: &Vec<i32>) -> impl Iterator<Item = i32> {\n'
                  '    v.iter().copied().filter(|x| x % 2 == 0)\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let v = vec![1, 2, 3, 4, 5, 6];\n'
                 '    println!("{:?}", evens_of(&v).collect::<Vec<_>>());\n'
                 '    println!("{}", evens_of(&v).sum::<i32>());\n'
                 '    println!("{}", evens_of(&Vec::new()).count());\n'
                 '}\n',
       'hint': "+ '_ означает: итератор живёт не дольше заимствованного аргумента.",
       'expected': ['[2, 4, 6]', '12', '0']},
      {'id': 'r21-static-table',
       'mode': 'rust',
       'title': "'static: таблицы и константы",
       'statement': 'static NAMES: [&str; 4] = ["север", "восток", "юг", "запад"]. direction_name(i: usize) '
                    "→ &'static str (индекс по кругу), direction_index(name: &str) → Option<usize>, "
                    "turn(from: &str, steps: i32) → Option<&'static str> — повернуть на steps четвертей "
                    '(может быть отрицательным). const QUARTER: i32 = 90.',
       'starter': 'static NAMES: [&str; 4] = ["север", "восток", "юг", "запад"];\n'
                  'const QUARTER: i32 = 90;\n'
                  '\n'
                  "fn direction_name(i: usize) -> &'static str {\n"
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn direction_index(name: &str) -> Option<usize> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  "fn turn(from: &str, steps: i32) -> Option<&'static str> {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{} {} {}", direction_name(0), direction_name(5), direction_name(11));\n'
                 '    println!("{:?} {:?}", direction_index("юг"), direction_index("вверх"));\n'
                 '    println!("{:?} {:?} {:?}", turn("север", 1), turn("север", -1), turn("запад", 6));\n'
                 '    println!("{:?}", turn("x", 1));\n'
                 '    println!("{}", QUARTER * 4);\n'
                 '}\n',
       'hint': 'rem_euclid(4) даёт неотрицательный остаток даже для отрицательных поворотов.',
       'expected': ['север восток запад',
                    'Some(2) None',
                    'Some("восток") Some("запад") Some("восток")',
                    'None',
                    '360']},
      {'id': 'r21-box-list',
       'mode': 'rust',
       'title': 'Список на Box: длина, сумма, разворот',
       'statement': 'List { Cons(i32, Box<List>), Nil }. len(&List), sum(&List), to_vec(&List), '
                    'reverse(List) → List (забирает список и переставляет звенья, без новых выделений через '
                    'clone), from_slice(&[i32]) → List.',
       'starter': 'enum List {\n'
                  '    Cons(i32, Box<List>),\n'
                  '    Nil,\n'
                  '}\n'
                  'use List::{Cons, Nil};\n'
                  '\n'
                  'fn from_slice(v: &[i32]) -> List {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn len(l: &List) -> usize {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn sum(l: &List) -> i32 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn to_vec(l: &List) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn reverse(l: List) -> List {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                 '    let l = from_slice(&[1, 2, 3, 4]);\n'
                 '    println!("{} {} {:?}", len(&l), sum(&l), to_vec(&l));\n'
                 '    let r = reverse(l);\n'
                 '    println!("{:?}", to_vec(&r));\n'
                 '    println!("{:?} {}", to_vec(&from_slice(&[])), len(&Nil));\n'
                 '    println!("clones: {}", bad0);\n'
                 '}\n',
       'hint': 'fold справа налево (rev()) собирает список с головой в начале; reverse переносит каждое '
               'звено в новый список.',
       'expected': ['4 10 [1, 2, 3, 4]', '[4, 3, 2, 1]', '[] 0', 'clones: 0']},
      {'id': 'r21-box-tree',
       'mode': 'rust',
       'title': 'Двоичное дерево поиска на Box',
       'statement': 'Tree { root: Option<Box<Node>> } с методами insert(&mut self, k) (дубликаты '
                    'игнорируются), contains(&self, k) → bool, height(&self) → usize (пустое — 0), '
                    'in_order(&self) → Vec<i32>, min(&self) → Option<i32>.',
       'starter': 'struct Node {\n'
                  '    key: i32,\n'
                  '    left: Option<Box<Node>>,\n'
                  '    right: Option<Box<Node>>,\n'
                  '}\n'
                  '\n'
                  'struct Tree {\n'
                  '    root: Option<Box<Node>>,\n'
                  '}\n'
                  '\n'
                  'impl Tree {\n'
                  '    fn new() -> Tree {\n'
                  '        Tree { root: None }\n'
                  '    }\n'
                  '    fn insert(&mut self, k: i32) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn contains(&self, k: i32) -> bool {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn height(&self) -> usize {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn in_order(&self) -> Vec<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn min(&self) -> Option<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut t = Tree::new();\n'
                 '    println!("{} {:?} {}", t.height(), t.min(), t.contains(1));\n'
                 '    for k in [5, 3, 8, 1, 4, 7, 9, 3, 5, 2] {\n'
                 '        t.insert(k);\n'
                 '    }\n'
                 '    println!("{:?}", t.in_order());\n'
                 '    println!("{} {:?} {} {}", t.height(), t.min(), t.contains(7), t.contains(6));\n'
                 '    let mut chain = Tree::new();\n'
                 '    for k in 1..=6 {\n'
                 '        chain.insert(k);\n'
                 '    }\n'
                 '    println!("{}", chain.height());\n'
                 '}\n',
       'hint': 'В insert идите вниз по &mut Option<Box<Node>>: пока Some — выбирайте сторону, а на None '
               'запишите новый узел.',
       'expected': ['0 None false', '[1, 2, 3, 4, 5, 7, 8, 9]', '4 Some(1) true false', '6']},
      {'id': 'r21-box-dyn-state',
       'mode': 'rust',
       'title': 'Состояния через Box<dyn State>',
       'statement': "Трейт State: name(&self) → &'static str и next(self: Box<Self>, event: &str) → Box<dyn "
                    'State>. Реализуйте Idle → ("start") Running → ("pause") Paused → ("resume") Running; из '
                    'Running по "stop" → Idle; Paused по "stop" → Idle; неизвестное событие оставляет '
                    "состояние. run(events: &[&str]) → Vec<&'static str> — имена состояний после каждого "
                    'события.',
       'starter': 'trait State {\n'
                  "    fn name(&self) -> &'static str;\n"
                  '    fn next(self: Box<Self>, event: &str) -> Box<dyn State>;\n'
                  '}\n'
                  '\n'
                  'struct Idle;\n'
                  'struct Running;\n'
                  'struct Paused;\n'
                  '\n'
                  '// impl State для трёх типов\n'
                  '\n'
                  "fn run(events: &[&str]) -> Vec<&'static str> {\n"
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    println!("{:?}", run(&["start", "pause", "resume", "stop", "stop"]));\n'
                 '    println!("{:?}", run(&["pause", "start", "bogus", "pause", "stop"]));\n'
                 '    println!("{:?}", run(&[]));\n'
                 '    println!("{}", std::mem::size_of::<Box<dyn State>>());\n'
                 '}\n',
       'hint': 'self: Box<Self> позволяет забрать и вернуть себя же (_ => self) или заменить другим '
               'состоянием.',
       'expected': ['["running", "paused", "running", "idle", "idle"]',
                    '["idle", "running", "running", "paused", "idle"]',
                    '[]',
                    '16']},
      {'id': 'r21-box-sizes',
       'mode': 'rust',
       'title': 'Размеры указателей и Box',
       'statement': 'sizes() → [usize; 8]: size_of для &u8, Box<u8>, Box<[u8; 100]>, &[u8], Box<dyn Fn()>, '
                    'Option<Box<u8>>, Option<&u8>, Rc<[u8; 100]> — в таком порядке. Какие из них одно слово, '
                    'а какие два?',
       'starter': 'use std::rc::Rc;\n\nfn sizes() -> [usize; 8] {\n    todo!()\n}\n',
       'driver': 'fn main() {\n    println!("{:?}", sizes());\n}\n',
       'hint': 'Срез и dyn хранят дополнительное слово; массив известной длины — обычный указатель; Option '
               'над указателем не толще указателя.',
       'expected': ['[8, 8, 8, 16, 16, 8, 8, 8]']},
      {'id': 'r21-mybox-deref',
       'mode': 'rust',
       'title': 'Свой умный указатель: Deref',
       'statement': 'MyBox<T>(T) с new(x). Реализуйте Deref (Target = T) и DerefMut. После этого '
                    'hello(&MyBox<String>) принимает &str благодаря приведению по разыменованию, а *b даёт '
                    'внутреннее значение. shout(b: &MyBox<String>) → String вызывает метод строки напрямую.',
       'starter': 'use std::ops::{Deref, DerefMut};\n'
                  '\n'
                  'struct MyBox<T>(T);\n'
                  '\n'
                  'impl<T> MyBox<T> {\n'
                  '    fn new(x: T) -> MyBox<T> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  '// impl Deref и DerefMut для MyBox<T>\n'
                  '\n'
                  'fn hello(name: &str) -> String {\n'
                  '    format!("Привет, {name}!")\n'
                  '}\n'
                  '\n'
                  'fn shout(b: &MyBox<String>) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let b = MyBox::new(String::from("мир"));\n'
                 '    println!("{}", hello(&b));\n'
                 '    println!("{} {}", shout(&b), b.len());\n'
                 '    let mut n = MyBox::new(5);\n'
                 '    *n += 10;\n'
                 '    println!("{}", *n);\n'
                 '    let mut s = MyBox::new(String::from("a"));\n'
                 '    s.push_str("bc");\n'
                 '    println!("{}", *s);\n'
                 '}\n',
       'hint': 'deref возвращает &self.0; DerefMut — &mut self.0. Приведение &MyBox<String> → &String → &str '
               'делает компилятор.',
       'expected': ['Привет, мир!', 'МИР 6', '15', 'abc']},
      {'id': 'r21-deref-slice',
       'mode': 'rust',
       'title': 'Deref к срезу: Sorted',
       'statement': 'Sorted хранит Vec<i32> в отсортированном виде. new(v) сортирует; insert(&mut self, x) '
                    'вставляет на нужное место (бинарный поиск); Deref<Target = [i32]> даёт len(), iter(), '
                    'first(), contains() и срезы без повторения методов.',
       'starter': 'use std::ops::Deref;\n'
                  '\n'
                  'struct Sorted(Vec<i32>);\n'
                  '\n'
                  'impl Sorted {\n'
                  '    fn new(mut v: Vec<i32>) -> Sorted {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn insert(&mut self, x: i32) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  '// impl Deref for Sorted { Target = [i32] }\n',
       'driver': 'fn main() {\n'
                 '    let mut s = Sorted::new(vec![5, 1, 4]);\n'
                 '    s.insert(3);\n'
                 '    s.insert(9);\n'
                 '    s.insert(0);\n'
                 '    println!("{} {:?} {:?}", s.len(), s.first(), s.last());\n'
                 '    println!("{:?}", s.iter().collect::<Vec<_>>());\n'
                 '    println!("{} {}", s.contains(&4), s.contains(&7));\n'
                 '    println!("{:?} {:?}", &s[1..3], s.binary_search(&9));\n'
                 '}\n',
       'hint': 'Target = [i32], deref возвращает &self.0 — вектор автоматически превращается в срез.',
       'expected': ['6 Some(0) Some(9)', '[0, 1, 3, 4, 5, 9]', 'true false', '[1, 3] Ok(5)']},
      {'id': 'r21-drop-order',
       'mode': 'rust',
       'title': 'Порядок Drop: журнал',
       'statement': 'Guard(name, log) при уничтожении дописывает в общий журнал «drop name». Реализуйте '
                    'Drop. scenario(log) создаёт Guard a, b, c в одном блоке, затем вложенный блок с d, '
                    'затем явно drop(b) и в конце возвращает журнал. Проверьте порядок: переменные умирают в '
                    'обратном порядке объявления.',
       'starter': 'use std::cell::RefCell;\n'
                  'use std::rc::Rc;\n'
                  '\n'
                  'struct Guard {\n'
                  "    name: &'static str,\n"
                  '    log: Rc<RefCell<Vec<String>>>,\n'
                  '}\n'
                  '\n'
                  '// impl Drop for Guard\n'
                  '\n'
                  'fn scenario() -> Vec<String> {\n'
                  '    let log = Rc::new(RefCell::new(Vec::new()));\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n    for line in scenario() {\n        println!("{line}");\n    }\n}\n',
       'hint': 'Журнал общий: Rc<RefCell<Vec<String>>>; в drop пишем через log.borrow_mut().push(...).',
       'expected': ['inner', 'drop d', 'drop b', 'end of block', 'drop c', 'drop a']},
      {'id': 'r21-forget-and-moves',
       'mode': 'rust',
       'title': 'drop, forget и перемещение',
       'statement': "Guard(&'static str) печатает «drop <имя>» при уничтожении, consume(g) печатает "
                    '«consume». Напишите trace(): создайте Guard a, b, c; передайте b в consume (Guard умрёт '
                    'внутри); затем напечатайте «mid»; отдайте c в std::mem::forget (деструктор не '
                    'вызывается); напечатайте «end». Что будет с a?',
       'starter': "struct Guard(&'static str);\n"
                  '\n'
                  'impl Drop for Guard {\n'
                  '    fn drop(&mut self) {\n'
                  '        println!("drop {}", self.0);\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  'fn consume(_g: Guard) {\n'
                  '    println!("consume");\n'
                  '}\n'
                  '\n'
                  'fn trace() {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n    trace();\n}\n',
       'hint': 'consume(b) забирает b: drop b сработает на выходе из consume; forget(c) не запускает drop; a '
               'умирает на скобке.',
       'expected': ['consume', 'drop b', 'mid', 'end', 'drop a']},
      {'id': 'r21-raii-transaction',
       'mode': 'rust',
       'title': 'RAII: транзакция откатывается сама',
       'statement': "Tx<'a> заимствует &'a mut Vec<i32> («базу»). begin(db) запоминает исходный размер; "
                    'push(&mut self, x) добавляет число; commit(self) фиксирует; если Tx уничтожена без '
                    'commit, Drop откатывает базу к исходной длине. Так «изменения» не просочатся при ошибке '
                    'или раннем выходе.',
       'starter': "struct Tx<'a> {\n"
                  "    db: &'a mut Vec<i32>,\n"
                  '    start_len: usize,\n'
                  '    committed: bool,\n'
                  '}\n'
                  '\n'
                  "impl<'a> Tx<'a> {\n"
                  "    fn begin(db: &'a mut Vec<i32>) -> Tx<'a> {\n"
                  '        todo!()\n'
                  '    }\n'
                  '    fn push(&mut self, x: i32) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn commit(mut self) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n'
                  '\n'
                  '// impl Drop for Tx\n',
       'driver': 'fn main() {\n'
                 '    let mut db = vec![1, 2];\n'
                 '    {\n'
                 '        let mut tx = Tx::begin(&mut db);\n'
                 '        tx.push(3);\n'
                 '        tx.push(4);\n'
                 '        tx.commit();\n'
                 '    }\n'
                 '    println!("{:?}", db);\n'
                 '    {\n'
                 '        let mut tx = Tx::begin(&mut db);\n'
                 '        tx.push(99);\n'
                 '        tx.push(100);\n'
                 '    }\n'
                 '    println!("{:?}", db);\n'
                 '    fn risky(db: &mut Vec<i32>, fail: bool) -> Result<(), String> {\n'
                 '        let mut tx = Tx::begin(db);\n'
                 '        tx.push(7);\n'
                 '        if fail {\n'
                 '            return Err("boom".into());\n'
                 '        }\n'
                 '        tx.commit();\n'
                 '        Ok(())\n'
                 '    }\n'
                 '    println!("{:?} {:?}", risky(&mut db, true), db);\n'
                 '    println!("{:?} {:?}", risky(&mut db, false), db);\n'
                 '}\n',
       'hint': 'commit(mut self) выставляет флаг и сам Tx умирает на выходе: Drop видит committed = true и '
               'ничего не откатывает.',
       'expected': ['[1, 2, 3, 4]', '[1, 2, 3, 4]', 'Err("boom") [1, 2, 3, 4]', 'Ok(()) [1, 2, 3, 4, 7]']},
      {'id': 'r21-rc-counts',
       'mode': 'rust',
       'title': 'Rc: следим за счётчиком',
       'statement': 'counts() → Vec<usize>: создайте Rc<String>, запишите strong_count; клонируйте дважды — '
                    'снова запишите; в вложенном блоке сделайте ещё клон и запишите; после блока и после '
                    'drop одного клона — запишите. Всего шесть чисел.',
       'starter': 'use std::rc::Rc;\n'
                  '\n'
                  'fn counts() -> Vec<usize> {\n'
                  '    let a = Rc::new(String::from("данные"));\n'
                  '    let mut out = vec![Rc::strong_count(&a)];\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n    println!("{:?}", counts());\n}\n',
       'hint': 'strong_count после каждого действия: 1, 3, 4, 3, 2, 1 — клон увеличивает, выход из блока и '
               'drop уменьшают.',
       'expected': ['[1, 3, 4, 3, 2, 1]']},
      {'id': 'r21-shared-account',
       'mode': 'rust',
       'title': 'Rc<RefCell<Account>>: общий счёт',
       'statement': 'Account { balance: i64 }. Два владельца делят один счёт через Rc<RefCell<Account>>. '
                    'deposit(acc, n) и withdraw(acc, n) → Result<(), String> «недостаточно средств: нужно N, '
                    'есть M»; transfer(from, to, n) → Result<(), String> переводит между двумя счетами (если '
                    'from и to — один и тот же счёт, перевод ничего не меняет).',
       'starter': 'use std::cell::RefCell;\n'
                  'use std::rc::Rc;\n'
                  '\n'
                  'struct Account {\n'
                  '    balance: i64,\n'
                  '}\n'
                  '\n'
                  'type Shared = Rc<RefCell<Account>>;\n'
                  '\n'
                  'fn deposit(acc: &Shared, n: i64) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn withdraw(acc: &Shared, n: i64) -> Result<(), String> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn transfer(from: &Shared, to: &Shared, n: i64) -> Result<(), String> {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let a: Shared = Rc::new(RefCell::new(Account { balance: 100 }));\n'
                 '    let a2 = Rc::clone(&a);\n'
                 '    let b: Shared = Rc::new(RefCell::new(Account { balance: 5 }));\n'
                 '    deposit(&a2, 50);\n'
                 '    println!("{}", a.borrow().balance);\n'
                 '    println!("{:?}", withdraw(&a, 500));\n'
                 '    println!("{:?} {} {}", transfer(&a, &b, 120), a.borrow().balance, '
                 'b.borrow().balance);\n'
                 '    println!("{:?} {}", transfer(&a, &a2, 30), a.borrow().balance);\n'
                 '    println!("{:?}", transfer(&b, &a, 1000));\n'
                 '    println!("{}", Rc::strong_count(&a));\n'
                 '}\n',
       'hint': 'Если from и to — один счёт, второй borrow_mut вызвал бы панику: проверьте Rc::ptr_eq '
               'заранее.',
       'expected': ['150',
                    'Err("недостаточно средств: нужно 500, есть 150")',
                    'Ok(()) 30 125',
                    'Ok(()) 30',
                    'Err("недостаточно средств: нужно 1000, есть 125")',
                    '2']},
      {'id': 'r21-rc-diamond',
       'mode': 'rust',
       'title': 'Общие узлы: Rc в графе без циклов',
       'statement': 'Node { val: i32, kids: Vec<Rc<Node>> }. total(&Node) → i32 — сумма по всем путям (общий '
                    'узел считается каждый раз), unique_total(&Node) → i32 — каждый узел один раз (множество '
                    'адресов *const Node). refs(&Rc<Node>) → usize — strong_count.',
       'starter': 'use std::collections::HashSet;\n'
                  'use std::rc::Rc;\n'
                  '\n'
                  'struct Node {\n'
                  '    val: i32,\n'
                  '    kids: Vec<Rc<Node>>,\n'
                  '}\n'
                  '\n'
                  'fn total(n: &Node) -> i32 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn unique_total(n: &Node) -> i32 {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn refs(n: &Rc<Node>) -> usize {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let shared = Rc::new(Node { val: 10, kids: vec![] });\n'
                 '    let left = Rc::new(Node { val: 1, kids: vec![Rc::clone(&shared)] });\n'
                 '    let right = Rc::new(Node { val: 2, kids: vec![Rc::clone(&shared)] });\n'
                 '    let root = Node { val: 100, kids: vec![left, right] };\n'
                 '    println!("{} {}", total(&root), unique_total(&root));\n'
                 '    println!("{}", refs(&shared));\n'
                 '    drop(root);\n'
                 '    println!("{}", refs(&shared));\n'
                 '}\n',
       'hint': 'Адрес узла — n as *const Node; множество seen не даёт посетить общий узел дважды.',
       'expected': ['123 113', '3', '1']},
      {'id': 'r21-refcell-try',
       'mode': 'rust',
       'title': 'RefCell: try_borrow без паники',
       'statement': 'probe() → Vec<bool>: создайте RefCell<i32>; запишите результаты is_ok() такой '
                    'последовательности: try_borrow_mut() на свободной ячейке; try_borrow() при живом '
                    'изменяемом заимствовании; try_borrow_mut() при живом разделяемом; try_borrow() при двух '
                    'разделяемых; try_borrow_mut() после освобождения всего.',
       'starter': 'use std::cell::RefCell;\n'
                  '\n'
                  'fn probe() -> Vec<bool> {\n'
                  '    let c = RefCell::new(0);\n'
                  '    let mut out = Vec::new();\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n    println!("{:?}", probe());\n}\n',
       'hint': 'Живой Ref или RefMut — это переменная в области видимости; блоки { … } освобождают '
               'заимствование.',
       'expected': ['[true, false, false, true, true]']},
      {'id': 'r21-cell-counter',
       'mode': 'rust',
       'title': 'Cell: счётчик через &self',
       'statement': 'Stats хранит hits: Cell<u32> и last: Cell<Option<i32>>. touch(&self, x) увеличивает '
                    'hits и запоминает x в last; hits() и last() возвращают значения. Все методы принимают '
                    '&self — изменение внутри общей ссылки (внутренняя изменяемость без RefCell).',
       'starter': 'use std::cell::Cell;\n'
                  '\n'
                  'struct Stats {\n'
                  '    hits: Cell<u32>,\n'
                  '    last: Cell<Option<i32>>,\n'
                  '}\n'
                  '\n'
                  'impl Stats {\n'
                  '    fn new() -> Stats {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn touch(&self, x: i32) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn hits(&self) -> u32 {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn last(&self) -> Option<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let s = Stats::new();\n'
                 '    let r1 = &s;\n'
                 '    let r2 = &s;\n'
                 '    r1.touch(5);\n'
                 '    r2.touch(7);\n'
                 '    r1.touch(-1);\n'
                 '    println!("{} {:?}", s.hits(), s.last());\n'
                 '    println!("{} {}", std::mem::size_of::<Cell<u32>>(), std::mem::size_of::<Stats>());\n'
                 '}\n',
       'hint': 'Cell::get/set работают с копируемыми значениями без выдачи ссылок — поэтому им не нужны '
               'проверки при запуске.',
       'expected': ['3 Some(-1)', '4 12']},
      {'id': 'r21-observer-weak',
       'mode': 'rust',
       'title': 'Наблюдатели на Weak',
       'statement': 'Subject хранит Vec<Weak<RefCell<Vec<String>>>> — «почтовые ящики» наблюдателей. '
                    'subscribe(&mut self, inbox: &Rc<RefCell<Vec<String>>>) добавляет слабую ссылку; '
                    'publish(&mut self, msg) → usize кладёт сообщение в живые ящики, удаляет умершие и '
                    'возвращает число доставленных.',
       'starter': 'use std::cell::RefCell;\n'
                  'use std::rc::{Rc, Weak};\n'
                  '\n'
                  'struct Subject {\n'
                  '    inboxes: Vec<Weak<RefCell<Vec<String>>>>,\n'
                  '}\n'
                  '\n'
                  'impl Subject {\n'
                  '    fn new() -> Subject {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn subscribe(&mut self, inbox: &Rc<RefCell<Vec<String>>>) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn publish(&mut self, msg: &str) -> usize {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut subj = Subject::new();\n'
                 '    let a = Rc::new(RefCell::new(Vec::new()));\n'
                 '    let b = Rc::new(RefCell::new(Vec::new()));\n'
                 '    subj.subscribe(&a);\n'
                 '    subj.subscribe(&b);\n'
                 '    println!("{}", subj.publish("первое"));\n'
                 '    drop(b);\n'
                 '    println!("{}", subj.publish("второе"));\n'
                 '    println!("{:?}", a.borrow());\n'
                 '    println!("{} {}", Rc::strong_count(&a), Rc::weak_count(&a));\n'
                 '    println!("{}", Subject::new().publish("никому"));\n'
                 '}\n',
       'hint': 'Rc::downgrade(&rc) — слабая ссылка; upgrade() вернёт None, когда владельцев не осталось.',
       'expected': ['2', '1', '["первое", "второе"]', '1 1', '0']},
      {'id': 'r21-parent-weak',
       'mode': 'rust',
       'title': 'Дерево с Weak на родителя',
       'statement': 'Node { name: String, parent: RefCell<Weak<Node>>, kids: RefCell<Vec<Rc<Node>>> }. '
                    'new(name) → Rc<Node>; add_child(parent: &Rc<Node>, child: Rc<Node>) прикрепляет ребёнка '
                    'и записывает слабую ссылку на родителя; path(n: &Rc<Node>) → String — путь от корня '
                    '«a/b/c».',
       'starter': 'use std::cell::RefCell;\n'
                  'use std::rc::{Rc, Weak};\n'
                  '\n'
                  'struct Node {\n'
                  '    name: String,\n'
                  '    parent: RefCell<Weak<Node>>,\n'
                  '    kids: RefCell<Vec<Rc<Node>>>,\n'
                  '}\n'
                  '\n'
                  'fn new(name: &str) -> Rc<Node> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn add_child(parent: &Rc<Node>, child: Rc<Node>) {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn path(n: &Rc<Node>) -> String {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let root = new("usr");\n'
                 '    let bin = new("bin");\n'
                 '    let tool = new("cargo");\n'
                 '    add_child(&root, Rc::clone(&bin));\n'
                 '    add_child(&bin, Rc::clone(&tool));\n'
                 '    println!("{} | {} | {}", path(&root), path(&bin), path(&tool));\n'
                 '    println!("{} {}", Rc::strong_count(&bin), Rc::weak_count(&bin));\n'
                 '    println!("{} {}", Rc::strong_count(&root), Rc::weak_count(&root));\n'
                 '    drop(root);\n'
                 '    println!("{}", path(&bin));\n'
                 '}\n',
       'hint': 'Родитель держит детей сильно (kids), а ребёнок родителя — слабо (parent), поэтому цикла нет '
               'и после drop(root) корень освобождается.',
       'expected': ['usr | usr/bin | usr/bin/cargo', '2 1', '1 1', 'bin']},
      {'id': 'r21-cycle-leak',
       'mode': 'rust',
       'title': 'Цикл Rc: утечка и её устранение',
       'statement': 'cycle_counts() → Vec<usize>: создайте два узла Node { next: RefCell<Option<Rc<Node>>> '
                    '}; запишите strong_count обоих; замкните их друг на друга и запишите снова; разорвите '
                    'цикл (take()) и запишите ещё раз. Всего шесть чисел: a, b до; a, b в цикле; a, b после.',
       'starter': 'use std::cell::RefCell;\n'
                  'use std::rc::Rc;\n'
                  '\n'
                  'struct Node {\n'
                  '    next: RefCell<Option<Rc<Node>>>,\n'
                  '}\n'
                  '\n'
                  'fn cycle_counts() -> Vec<usize> {\n'
                  '    let a = Rc::new(Node { next: RefCell::new(None) });\n'
                  '    let b = Rc::new(Node { next: RefCell::new(None) });\n'
                  '    let mut out = vec![Rc::strong_count(&a), Rc::strong_count(&b)];\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n    println!("{:?}", cycle_counts());\n}\n',
       'hint': 'Пока цикл замкнут, у каждого узла счётчик 2 — после выхода из функции они бы не '
               'освободились; take() разрывает связь.',
       'expected': ['[1, 1, 2, 2, 1, 2]']},
      {'id': 'r21-arc-basics',
       'mode': 'rust',
       'title': 'Arc: счётчик, try_unwrap и make_mut',
       'statement': 'arc_demo() → (usize, bool, Vec<i32>, Vec<i32>): создайте Arc<Vec<i32>> из [1, 2, 3]; '
                    'клонируйте; запишите strong_count; попытка Arc::try_unwrap при двух владельцах '
                    '(is_err); затем через Arc::make_mut у клона добавьте 4 (копия, потому что владельцев '
                    'двое) — верните оригинал и изменённый клон.',
       'starter': 'use std::sync::Arc;\n'
                  '\n'
                  'fn arc_demo() -> (usize, bool, Vec<i32>, Vec<i32>) {\n'
                  '    let a = Arc::new(vec![1, 2, 3]);\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n    println!("{:?}", arc_demo());\n}\n',
       'hint': 'try_unwrap возвращает Err, пока есть другие владельцы; make_mut клонирует данные, если Arc '
               'не единственный.',
       'expected': ['(2, true, [1, 2, 3], [1, 2, 3, 4])']},
      {'id': 'r21-cow-normalize',
       'mode': 'rust',
       'title': 'Cow: копируем только при необходимости',
       'statement': 'normalize(s: &str) → Cow<str>: если в строке есть табы или подряд идущие пробелы, '
                    'вернуть исправленную копию (табы → пробел, серии пробелов → один); иначе вернуть '
                    'Cow::Borrowed без копии. is_borrowed(c) → bool — Cow ли заимствован.',
       'starter': 'use std::borrow::Cow;\n'
                  '\n'
                  'fn normalize(s: &str) -> Cow<str> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn is_borrowed(c: &Cow<str>) -> bool {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    for s in ["ok text", "a  b", "x\\ty", "  ", ""] {\n'
                 '        let n = normalize(s);\n'
                 '        println!("{:?} -> {:?} borrowed={}", s, n, is_borrowed(&n));\n'
                 '    }\n'
                 '    let src = "unchanged";\n'
                 '    let n = normalize(src);\n'
                 '    println!("{}", n.as_ptr() == src.as_ptr());\n'
                 '}\n',
       'hint': 'В ветке без правок возвращайте Cow::Borrowed(s) — тот же адрес, без копии.',
       'expected': ['"ok text" -> "ok text" borrowed=true',
                    '"a  b" -> "a b" borrowed=false',
                    '"x\\ty" -> "x y" borrowed=false',
                    '"  " -> " " borrowed=false',
                    '"" -> "" borrowed=true',
                    'true']},
      {'id': 'r21-mem-replace',
       'mode': 'rust',
       'title': 'mem::replace, take и swap',
       'statement': 'Machine { state: State, items: Vec<String>, name: String }. finish(&mut self) → State — '
                    'перевести состояние в Done и вернуть прежнее (mem::replace); drain_items(&mut self) → '
                    'Vec<String> — забрать все элементы (mem::take); swap_name(&mut self, other: &mut '
                    'Machine) — поменять имена местами (mem::swap).',
       'starter': 'use std::mem;\n'
                  '\n'
                  '#[derive(Debug, PartialEq)]\n'
                  'enum State {\n'
                  '    New,\n'
                  '    Busy(u32),\n'
                  '    Done,\n'
                  '}\n'
                  '\n'
                  'struct Machine {\n'
                  '    state: State,\n'
                  '    items: Vec<String>,\n'
                  '    name: String,\n'
                  '}\n'
                  '\n'
                  'impl Machine {\n'
                  '    fn finish(&mut self) -> State {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn drain_items(&mut self) -> Vec<String> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn swap_name(&mut self, other: &mut Machine) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let src = include_str!("main.rs");\n'
                 '    let bad0 = src.matches(concat!(".clo", "ne()")).count();\n'
                 '    let mut a = Machine { state: State::Busy(3), items: vec!["x".into(), "y".into()], '
                 'name: "alpha".into() };\n'
                 '    let mut b = Machine { state: State::New, items: vec![], name: "beta".into() };\n'
                 '    println!("{:?} {:?}", a.finish(), a.state);\n'
                 '    println!("{:?} {:?}", a.drain_items(), a.items);\n'
                 '    a.swap_name(&mut b);\n'
                 '    println!("{} {}", a.name, b.name);\n'
                 '    println!("{:?} {:?}", b.finish(), b.finish());\n'
                 '    println!("clones: {}", bad0);\n'
                 '}\n',
       'hint': 'mem::replace(&mut поле, новое) возвращает старое; mem::take подставляет Default (пустой '
               'Vec).',
       'expected': ['Busy(3) Done', '["x", "y"] []', 'beta alpha', 'New Done', 'clones: 0']},
      {'id': 'r21-intern',
       'mode': 'rust',
       'title': 'Интернирование строк: Rc<str>',
       'statement': 'Interner хранит HashMap<String, Rc<str>>. intern(&mut self, s: &str) → Rc<str> '
                    'возвращает один и тот же Rc для равных строк (память выделяется один раз); len(&self) → '
                    'usize — число различных строк; total_refs(&self) → usize — сумма strong_count по всем '
                    'записям.',
       'starter': 'use std::collections::HashMap;\n'
                  'use std::rc::Rc;\n'
                  '\n'
                  'struct Interner {\n'
                  '    map: HashMap<String, Rc<str>>,\n'
                  '}\n'
                  '\n'
                  'impl Interner {\n'
                  '    fn new() -> Interner {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn intern(&mut self, s: &str) -> Rc<str> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn len(&self) -> usize {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn total_refs(&self) -> usize {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut i = Interner::new();\n'
                 '    let a = i.intern("привет");\n'
                 '    let b = i.intern("мир");\n'
                 '    let c = i.intern("привет");\n'
                 '    println!("{} {}", Rc::ptr_eq(&a, &c), Rc::ptr_eq(&a, &b));\n'
                 '    println!("{} {}", i.len(), i.total_refs());\n'
                 '    drop(c);\n'
                 '    println!("{}", i.total_refs());\n'
                 '    println!("{} {}", &*a, std::mem::size_of::<Rc<str>>());\n'
                 '}\n',
       'hint': 'Rc<str> — толстый указатель (адрес и длина); Rc::from(&str) копирует байты один раз в блок с '
               'счётчиками.',
       'expected': ['true false', '2 5', '4', 'привет 16']},
      {'id': 'r21-arena-tree',
       'mode': 'rust',
       'title': 'Дерево в арене: индексы вместо указателей',
       'statement': 'Arena { nodes: Vec<Item> } с Item { name, parent: Option<usize>, kids: Vec<usize> }. '
                    'add(name, parent: Option<usize>) → usize — id нового узла (и запись в kids родителя); '
                    'depth(id) → usize — число предков; path(id) → String «a/b/c»; leaves(&self) → Vec<&str> '
                    '— имена узлов без детей в порядке id. Ни Rc, ни RefCell.',
       'starter': 'struct Item {\n'
                  '    name: String,\n'
                  '    parent: Option<usize>,\n'
                  '    kids: Vec<usize>,\n'
                  '}\n'
                  '\n'
                  'struct Arena {\n'
                  '    nodes: Vec<Item>,\n'
                  '}\n'
                  '\n'
                  'impl Arena {\n'
                  '    fn new() -> Arena {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn add(&mut self, name: &str, parent: Option<usize>) -> usize {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn depth(&self, id: usize) -> usize {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn path(&self, id: usize) -> String {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn leaves(&self) -> Vec<&str> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut a = Arena::new();\n'
                 '    let root = a.add("src", None);\n'
                 '    let lib = a.add("lib", Some(root));\n'
                 '    let main = a.add("main", Some(root));\n'
                 '    let util = a.add("util", Some(lib));\n'
                 '    println!("{} {} {}", a.depth(root), a.depth(lib), a.depth(util));\n'
                 '    println!("{} | {}", a.path(util), a.path(main));\n'
                 '    println!("{:?}", a.leaves());\n'
                 '    println!("{}", a.nodes[root].kids.len());\n'
                 '}\n',
       'hint': 'Связи — индексы в одном Vec: добавляя узел, допишите его id в kids родителя.',
       'expected': ['0 1 2', 'src/lib/util | src/main', '["main", "util"]', '2']},
      {'id': 'r21-persistent-list',
       'mode': 'rust',
       'title': 'Неизменяемый список с общим хвостом',
       'statement': 'type Link = Option<Rc<Node>>; Node { val, next: Link }. push(list: &Link, v) → Link '
                    'создаёт новую голову, делящую хвост со старым списком; to_vec(&Link); len(&Link); '
                    'tail_refs(list: &Link) → usize — strong_count головы (сколько списков делят этот '
                    'хвост).',
       'starter': 'use std::rc::Rc;\n'
                  '\n'
                  'struct Node {\n'
                  '    val: i32,\n'
                  '    next: Link,\n'
                  '}\n'
                  'type Link = Option<Rc<Node>>;\n'
                  '\n'
                  'fn push(list: &Link, v: i32) -> Link {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn to_vec(list: &Link) -> Vec<i32> {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn len(list: &Link) -> usize {\n'
                  '    todo!()\n'
                  '}\n'
                  '\n'
                  'fn tail_refs(list: &Link) -> usize {\n'
                  '    todo!()\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let base = push(&push(&None, 3), 2);\n'
                 '    let a = push(&base, 1);\n'
                 '    let b = push(&base, 100);\n'
                 '    println!("{:?} {:?} {:?}", to_vec(&base), to_vec(&a), to_vec(&b));\n'
                 '    println!("{} {}", len(&a), len(&None));\n'
                 '    println!("{} {}", tail_refs(&base), tail_refs(&a));\n'
                 '    drop(a);\n'
                 '    println!("{}", tail_refs(&base));\n'
                 '}\n',
       'hint': 'list.clone() у Option<Rc<…>> копирует лишь указатель и увеличивает счётчик: хвост общий.',
       'expected': ['[2, 3] [1, 2, 3] [100, 2, 3]', '3 0', '3 1', '2']},
      {'id': 'r21-dlist-weak',
       'mode': 'rust',
       'title': 'Двусвязный список: Rc вперёд, Weak назад',
       'statement': 'DList { head: Option<Rc<RefCell<DNode>>>, tail: Option<Rc<RefCell<DNode>>> } с DNode { '
                    'val, next: Option<Rc<RefCell<DNode>>>, prev: Option<Weak<RefCell<DNode>>> }. '
                    'push_back(v); push_front(v); pop_back() → Option<i32>; forward() → Vec<i32> (по next); '
                    'backward() → Vec<i32> (по prev от хвоста).',
       'starter': 'use std::cell::RefCell;\n'
                  'use std::rc::{Rc, Weak};\n'
                  '\n'
                  'type Link = Option<Rc<RefCell<DNode>>>;\n'
                  '\n'
                  'struct DNode {\n'
                  '    val: i32,\n'
                  '    next: Link,\n'
                  '    prev: Option<Weak<RefCell<DNode>>>,\n'
                  '}\n'
                  '\n'
                  'struct DList {\n'
                  '    head: Link,\n'
                  '    tail: Link,\n'
                  '}\n'
                  '\n'
                  'impl DList {\n'
                  '    fn new() -> DList {\n'
                  '        DList { head: None, tail: None }\n'
                  '    }\n'
                  '    fn push_back(&mut self, v: i32) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn push_front(&mut self, v: i32) {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn pop_back(&mut self) -> Option<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn forward(&self) -> Vec<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '    fn backward(&self) -> Vec<i32> {\n'
                  '        todo!()\n'
                  '    }\n'
                  '}\n',
       'driver': 'fn main() {\n'
                 '    let mut l = DList::new();\n'
                 '    println!("{:?} {:?}", l.forward(), l.pop_back());\n'
                 '    l.push_back(2);\n'
                 '    l.push_back(3);\n'
                 '    l.push_front(1);\n'
                 '    l.push_back(4);\n'
                 '    println!("{:?} {:?}", l.forward(), l.backward());\n'
                 '    println!("{:?} {:?}", l.pop_back(), l.pop_back());\n'
                 '    println!("{:?} {:?}", l.forward(), l.backward());\n'
                 '    l.pop_back();\n'
                 '    l.pop_back();\n'
                 '    println!("{:?} {:?} {}", l.forward(), l.pop_back(), l.head.is_none() && '
                 'l.tail.is_none());\n'
                 '}\n',
       'hint': 'Вперёд (next) — сильные Rc, назад (prev) — Weak; при pop_back не забудьте обнулить next у '
               'нового хвоста.',
       'expected': ['[] None',
                    '[1, 2, 3, 4] [4, 3, 2, 1]',
                    'Some(4) Some(3)',
                    '[1, 2] [2, 1]',
                    '[] None true']}]}
