"""Задачи книги «Изучаем Rust»: главы 6–10."""

TASKS: dict[int, list[dict]] = {
    6: [
        {
            "id": "rs6-largest",
            "mode": "rust",
            "title": "Обобщённый максимум",
            "statement": (
                "Напишите обобщённую функцию largest<T: PartialOrd + Copy>(items: "
                "&[T]) -> Option<T>: наибольший элемент или None для пустого среза."
            ),
            "starter": "fn largest<T: PartialOrd + Copy>(items: &[T]) -> Option<T> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", largest(&[3, 9, 2]));\n"
                "    println!(\"{:?}\", largest(&['q', 'a', 'z']));\n"
                "    println!(\"{:?}\", largest(&[1.5, -0.2]));\n"
                "    println!(\"{:?}\", largest::<i32>(&[]));\n"
                "}\n"
            ),
            "expected": ["Some(9)", "Some('z')", "Some(1.5)", "None"],
            "hint": "Оператор ? работает и с Option: пустой срез сразу вернёт None.",
        },
        {
            "id": "rs6-pair",
            "mode": "rust",
            "title": "Обобщённая пара",
            "statement": (
                "Дополните Pair<T>: new(a, b), swap(self) -> Pair<T>, и метод "
                "larger(&self) -> T (только для T: PartialOrd + Copy) — большее из "
                "двух."
            ),
            "starter": "struct Pair<T> {\n    a: T,\n    b: T,\n}\n\nimpl<T> Pair<T> {\n    fn new(a: T, b: T) -> Pair<T> {\n        todo!()\n    }\n    fn swap(self) -> Pair<T> {\n        todo!()\n    }\n}\n\nimpl<T: PartialOrd + Copy> Pair<T> {\n    fn larger(&self) -> T {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let p = Pair::new(3, 8);\n"
                "    println!(\"{}\", p.larger());\n"
                "    let q = p.swap();\n"
                "    println!(\"{} {}\", q.a, q.b);\n"
                "    let s = Pair::new(\"x\".to_string(), \"y\".to_string()).swap();\n"
                "    println!(\"{} {}\", s.a, s.b);\n"
                "    println!(\"{}\", Pair::new(2.5, 2.4).larger());\n"
                "}\n"
            ),
            "expected": ["8", "8 3", "y x", "2.5"],
            "hint": "swap забирает self во владение — можно перемещать поля без clone. Второй impl-блок добавляет метод только при выполнении ограничений.",
        },
        {
            "id": "rs6-trait-default",
            "mode": "rust",
            "title": "Свой трейт с методом по умолчанию",
            "statement": (
                "Реализуйте трейт Animal для Dog и Cat: name(&self) -> String "
                "('Rex', 'Tom'), sound(&self) -> String ('woof', 'meow'). Метод "
                "speak(&self) -> String по умолчанию уже написан: 'Rex says woof'; "
                "для Cat переопределите его: 'Tom purrs'."
            ),
            "starter": "trait Animal {\n    fn name(&self) -> String;\n    fn sound(&self) -> String;\n    fn speak(&self) -> String {\n        format!(\"{} says {}\", self.name(), self.sound())\n    }\n}\n\nstruct Dog;\nstruct Cat;\n\n// impl Animal for Dog ...\n// impl Animal for Cat ...\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{}\", Dog.speak());\n"
                "    println!(\"{}\", Cat.speak());\n"
                "    println!(\"{} {}\", Dog.sound(), Cat.name());\n"
                "}\n"
            ),
            "expected": ["Rex says woof", "Tom purrs", "woof Tom"],
            "hint": "impl Animal for Dog { fn name(&self) -> String {...} fn sound(&self) -> String {...} }; speak у собаки не пишем.",
        },
        {
            "id": "rs6-dyn-shapes",
            "mode": "rust",
            "title": "Фигуры в одной коллекции",
            "statement": (
                "Реализуйте трейт Shape для Rect { w, h } и Circle { r } (area и "
                "perimeter, π = std::f64::consts::PI) и функцию total_area(shapes: "
                "&[Box<dyn Shape>]) -> f64."
            ),
            "starter": "trait Shape {\n    fn area(&self) -> f64;\n    fn perimeter(&self) -> f64;\n}\n\nstruct Rect {\n    w: f64,\n    h: f64,\n}\nstruct Circle {\n    r: f64,\n}\n\n// impl Shape for Rect ...\n// impl Shape for Circle ...\n\nfn total_area(shapes: &[Box<dyn Shape>]) -> f64 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let shapes: Vec<Box<dyn Shape>> = vec![Box::new(Rect { w: 3.0, h: 4.0 }), Box::new(Circle { r: 1.0 }), Box::new(Rect { w: 1.0, h: 1.0 })];\n"
                "    println!(\"{:.3}\", total_area(&shapes));\n"
                "    println!(\"{:.3}\", shapes[1].perimeter());\n"
                "    println!(\"{:.1}\", total_area(&[]));\n"
                "}\n"
            ),
            "expected": ["16.142", "6.283", "-0.0"],
            "hint": "Box<dyn Shape> хранит любую реализацию; sum() по итератору f64 даёт сумму.",
        },
        {
            "id": "rs6-stack",
            "mode": "rust",
            "title": "Обобщённый стек",
            "statement": (
                "Реализуйте Stack<T>: new(), push(&mut self, T), pop(&mut self) -> "
                "Option<T>, peek(&self) -> Option<&T>, len(&self) -> usize, "
                "is_empty(&self) -> bool. Внутри — Vec<T>."
            ),
            "starter": "struct Stack<T> {\n    items: Vec<T>,\n}\n\nimpl<T> Stack<T> {\n    fn new() -> Stack<T> {\n        todo!()\n    }\n    fn push(&mut self, x: T) {\n        todo!()\n    }\n    fn pop(&mut self) -> Option<T> {\n        todo!()\n    }\n    fn peek(&self) -> Option<&T> {\n        todo!()\n    }\n    fn len(&self) -> usize {\n        todo!()\n    }\n    fn is_empty(&self) -> bool {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let mut s: Stack<i32> = Stack::new();\n"
                "    println!(\"{} {:?}\", s.is_empty(), s.pop());\n"
                "    s.push(1);\n"
                "    s.push(2);\n"
                "    s.push(3);\n"
                "    println!(\"{:?} {}\", s.peek(), s.len());\n"
                "    println!(\"{:?} {:?}\", s.pop(), s.pop());\n"
                "    let mut t = Stack::new();\n"
                "    t.push(\"a\".to_string());\n"
                "    println!(\"{:?} {}\", t.peek(), t.is_empty());\n"
                "}\n"
            ),
            "expected": ["true None", "Some(3) 3", "Some(3) Some(2)", "Some(\"a\") false"],
            "hint": "Каждый метод — делегирование соответствующему методу Vec.",
        },
        {
            "id": "rs6-complex",
            "mode": "rust",
            "title": "Комплексные числа: операторы и Display",
            "statement": (
                "Реализуйте для Complex { re: f64, im: f64 } трейты Add, Mul (по "
                "правилам комплексных чисел: (a+bi)(c+di) = (ac−bd) + (ad+bc)i) и "
                "Display в виде '3+4i' (целые вещественные значения печатать как "
                "есть — используйте {} для f64; мнимая часть с знаком: '1-2i')."
            ),
            "starter": "use std::fmt;\nuse std::ops::{Add, Mul};\n\n#[derive(Debug, Clone, Copy, PartialEq)]\nstruct Complex {\n    re: f64,\n    im: f64,\n}\n\n// impl Add for Complex ...\n// impl Mul for Complex ...\n// impl fmt::Display for Complex ...\n",
            "driver": (
                "fn main() {\n"
                "    let a = Complex { re: 1.0, im: 2.0 };\n"
                "    let b = Complex { re: 3.0, im: -1.0 };\n"
                "    println!(\"{}\", a + b);\n"
                "    println!(\"{}\", a * b);\n"
                "    println!(\"{}\", a * a);\n"
                "    println!(\"{}\", Complex { re: 0.0, im: 0.0 } + Complex { re: 2.5, im: 0.5 });\n"
                "}\n"
            ),
            "expected": ["4+1i", "5+5i", "-3+4i", "2.5+0.5i"],
            "hint": "В Display для отрицательной мнимой части знак уже внутри числа: выводим re, затем im и букву i.",
        },
        {
            "id": "rs6-count-where",
            "mode": "rust",
            "title": "Обобщения с замыканием",
            "statement": (
                "Напишите count_where<T, F>(items: &[T], pred: F) -> usize where F: "
                "Fn(&T) -> bool и apply_n<F>(n: usize, f: F) -> Vec<usize> where F: "
                "Fn(usize) -> usize (значения f(0), f(1), …, f(n−1))."
            ),
            "starter": "fn count_where<T, F>(items: &[T], pred: F) -> usize\nwhere\n    F: Fn(&T) -> bool,\n{\n    todo!()\n}\n\nfn apply_n<F>(n: usize, f: F) -> Vec<usize>\nwhere\n    F: Fn(usize) -> usize,\n{\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{}\", count_where(&[1, 5, 8, 12, 3], |&x| x > 4));\n"
                "    let words = [\"apple\", \"fig\", \"banana\"];\n"
                "    println!(\"{}\", count_where(&words, |w| w.len() > 3));\n"
                "    println!(\"{}\", count_where::<i32, _>(&[], |_| true));\n"
                "    println!(\"{:?}\", apply_n(5, |i| i * i));\n"
                "    let k = 10;\n"
                "    println!(\"{:?}\", apply_n(3, move |i| i + k));\n"
                "}\n"
            ),
            "expected": ["3", "2", "0", "[0, 1, 4, 9, 16]", "[10, 11, 12]"],
            "hint": "Fn(&T) -> bool вызывается как обычная функция: pred(x).",
        },
        {
            "id": "rs6-fib-iterator",
            "mode": "rust",
            "title": "Свой итератор",
            "statement": (
                "Реализуйте Iterator для структуры Fib: она выдаёт числа Фибоначчи "
                "0, 1, 1, 2, 3, 5, … (тип Item = u64) и заканчивается, когда "
                "следующее число не помещается в u64."
            ),
            "starter": "struct Fib {\n    a: u64,\n    b: u64,\n}\n\nimpl Fib {\n    fn new() -> Fib {\n        Fib { a: 0, b: 1 }\n    }\n}\n\n// impl Iterator for Fib ...\n",
            "driver": (
                "fn main() {\n"
                "    let first: Vec<u64> = Fib::new().take(10).collect();\n"
                "    println!(\"{:?}\", first);\n"
                "    println!(\"{}\", Fib::new().count());\n"
                "    println!(\"{:?}\", Fib::new().last());\n"
                "    let even: u64 = Fib::new().take_while(|&x| x < 100).filter(|x| x % 2 == 0).sum();\n"
                "    println!(\"{}\", even);\n"
                "}\n"
            ),
            "expected": ["[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]", "92", "Some(4660046610375530309)", "44"],
            "hint": "Достаточно реализовать next; take, count, filter, sum появятся сами. checked_add возвращает None при переполнении.",
        },
        {
            "id": "rs6-card-ord",
            "mode": "rust",
            "title": "Порядок для своего типа",
            "statement": (
                "Реализуйте Ord и PartialOrd для Card { rank: u8, suit: char }: "
                "сначала по rank, при равенстве — по suit (в алфавитном порядке). "
                "PartialEq и Eq уже выведены. Должна работать сортировка sort()."
            ),
            "starter": "use std::cmp::Ordering;\n\n#[derive(Debug, PartialEq, Eq, Clone)]\nstruct Card {\n    rank: u8,\n    suit: char,\n}\n\n// impl Ord for Card ...\n// impl PartialOrd for Card ...\n",
            "driver": (
                "fn main() {\n"
                "    let mut cards = vec![\n"
                "        Card { rank: 10, suit: 'h' },\n"
                "        Card { rank: 2, suit: 's' },\n"
                "        Card { rank: 10, suit: 'c' },\n"
                "        Card { rank: 7, suit: 'd' },\n"
                "    ];\n"
                "    cards.sort();\n"
                "    for c in &cards {\n"
                "        println!(\"{}{}\", c.rank, c.suit);\n"
                "    }\n"
                "    println!(\"{}\", cards[0] < cards[1]);\n"
                "    println!(\"{:?}\", cards.iter().max());\n"
                "}\n"
            ),
            "expected": ["2s", "7d", "10c", "10h", "true", "Some(Card { rank: 10, suit: 'h' })"],
            "hint": "cmp сравнивает rank, затем .then(...) — suit; partial_cmp просто оборачивает cmp в Some.",
        },
    ],
    7: [
        {
            "id": "rs7-compose",
            "mode": "rust",
            "title": "Композиция функций",
            "statement": (
                "Напишите compose(f, g) -> impl Fn(i32) -> i32: результат — функция "
                "x ↦ g(f(x)). Параметры f и g — любые замыкания Fn(i32) -> i32."
            ),
            "starter": "fn compose(f: impl Fn(i32) -> i32, g: impl Fn(i32) -> i32) -> impl Fn(i32) -> i32 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let inc_then_double = compose(|x| x + 1, |x| x * 2);\n"
                "    println!(\"{} {}\", inc_then_double(4), inc_then_double(-1));\n"
                "    let k = 100;\n"
                "    let c = compose(move |x| x + k, |x| x - 1);\n"
                "    println!(\"{}\", c(5));\n"
                "    let id = compose(|x| x, |x| x);\n"
                "    println!(\"{}\", id(42));\n"
                "}\n"
            ),
            "expected": ["10 0", "104", "42"],
            "hint": "Замыкание должно владеть f и g: добавьте move.",
        },
        {
            "id": "rs7-counter",
            "mode": "rust",
            "title": "Счётчик-замыкание",
            "statement": (
                "Напишите make_counter(start: u32, step: u32) -> impl FnMut() -> "
                "u32: каждый вызов возвращает текущее значение и увеличивает его на "
                "step."
            ),
            "starter": "fn make_counter(start: u32, step: u32) -> impl FnMut() -> u32 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let mut a = make_counter(0, 1);\n"
                "    let mut b = make_counter(100, 10);\n"
                "    println!(\"{} {} {}\", a(), a(), a());\n"
                "    println!(\"{} {}\", b(), b());\n"
                "    println!(\"{}\", a());\n"
                "}\n"
            ),
            "expected": ["0 1 2", "100 110", "3"],
            "hint": "Состояние живёт внутри замыкания: let mut current = start; move || {...}",
        },
        {
            "id": "rs7-evens-squared",
            "mode": "rust",
            "title": "Конвейер из адаптеров",
            "statement": (
                "Напишите evens_squared(v: &[i32]) -> Vec<i32>: квадраты чётных "
                "элементов в исходном порядке. Только итераторы, без циклов for."
            ),
            "starter": "fn evens_squared(v: &[i32]) -> Vec<i32> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", evens_squared(&[1, 2, 3, 4, 5, 6]));\n"
                "    println!(\"{:?}\", evens_squared(&[]));\n"
                "    println!(\"{:?}\", evens_squared(&[-4, 7, 0]));\n"
                "}\n"
            ),
            "expected": ["[4, 16, 36]", "[]", "[16, 0]"],
            "hint": "filter(|&&x| ...) — у filter ссылка на ссылку; map(|&x| ...) разыменовывает элемент.",
        },
        {
            "id": "rs7-longest-word",
            "mode": "rust",
            "title": "Самое длинное слово",
            "statement": (
                "Напишите longest_word(s: &str) -> Option<&str>: самое длинное "
                "слово строки (по символам); при равенстве длин — первое из них; "
                "для строки без слов — None."
            ),
            "starter": "fn longest_word(s: &str) -> Option<&str> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", longest_word(\"a quick brown fox\"));\n"
                "    println!(\"{:?}\", longest_word(\"one two six\"));\n"
                "    println!(\"{:?}\", longest_word(\"   \"));\n"
                "    println!(\"{:?}\", longest_word(\"привет мир\"));\n"
                "}\n"
            ),
            "expected": ["Some(\"quick\")", "Some(\"one\")", "None", "Some(\"привет\")"],
            "hint": "max_by_key при равенстве возвращает ПОСЛЕДНИЙ элемент — здесь это ловушка; сравнивайте строго «больше».",
        },
        {
            "id": "rs7-running-sum",
            "mode": "rust",
            "title": "Нарастающий итог",
            "statement": (
                "Напишите running_sum(v: &[i32]) -> Vec<i64>: i-й элемент — сумма "
                "первых i + 1 элементов (через scan)."
            ),
            "starter": "fn running_sum(v: &[i32]) -> Vec<i64> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", running_sum(&[1, 2, 3, 4]));\n"
                "    println!(\"{:?}\", running_sum(&[]));\n"
                "    println!(\"{:?}\", running_sum(&[i32::MAX, i32::MAX, -5]));\n"
                "}\n"
            ),
            "expected": ["[1, 3, 6, 10]", "[]", "[2147483647, 4294967294, 4294967289]"],
            "hint": "scan хранит накопитель: *acc += x; Some(*acc).",
        },
        {
            "id": "rs7-dot-product",
            "mode": "rust",
            "title": "Скалярное произведение",
            "statement": (
                "Напишите dot(a: &[i32], b: &[i32]) -> i64 (пары по позициям, "
                "лишние элементы длинного среза игнорируются) и mean(v: &[f64]) -> "
                "Option<f64>."
            ),
            "starter": "fn dot(a: &[i32], b: &[i32]) -> i64 {\n    todo!()\n}\n\nfn mean(v: &[f64]) -> Option<f64> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{} {}\", dot(&[1, 2, 3], &[4, 5, 6]), dot(&[1, 2, 3, 4], &[1, 1]));\n"
                "    println!(\"{}\", dot(&[i32::MAX], &[i32::MAX]));\n"
                "    println!(\"{:?} {:?}\", mean(&[1.0, 2.0, 6.0]), mean(&[]));\n"
                "}\n"
            ),
            "expected": ["32 3", "4611686014132420609", "Some(3.0) None"],
            "hint": "zip останавливается на более коротком; sum::<i64>() / sum::<f64>() задают тип суммы.",
        },
        {
            "id": "rs7-parse-numbers",
            "mode": "rust",
            "title": "collect в Result",
            "statement": (
                "Напишите parse_numbers(s: &str) -> Result<Vec<i32>, "
                "std::num::ParseIntError>: числа через пробел; на первой же ошибке "
                "— Err. Пустая строка даёт Ok(пустой вектор). Одной цепочкой с "
                "collect."
            ),
            "starter": "fn parse_numbers(s: &str) -> Result<Vec<i32>, std::num::ParseIntError> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", parse_numbers(\"1 2 -3\"));\n"
                "    println!(\"{:?}\", parse_numbers(\"\"));\n"
                "    match parse_numbers(\"4 five 6\") {\n"
                "        Ok(v) => println!(\"ok {:?}\", v),\n"
                "        Err(e) => println!(\"err {}\", e),\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["Ok([1, 2, -3])", "Ok([])", "err invalid digit found in string"],
            "hint": "Итератор Result<i32, E> собирается прямо в Result<Vec<i32>, E>.",
        },
        {
            "id": "rs7-run-lengths",
            "mode": "rust",
            "title": "Сжатие повторов",
            "statement": (
                "Напишите run_lengths(v: &[i32]) -> Vec<(i32, usize)>: подряд "
                "идущие равные элементы заменяются парой (значение, длина серии)."
            ),
            "starter": "fn run_lengths(v: &[i32]) -> Vec<(i32, usize)> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", run_lengths(&[1, 1, 2, 2, 2, 1, 3]));\n"
                "    println!(\"{:?}\", run_lengths(&[]));\n"
                "    println!(\"{:?}\", run_lengths(&[7, 7, 7]));\n"
                "}\n"
            ),
            "expected": ["[(1, 2), (2, 3), (1, 1), (3, 1)]", "[]", "[(7, 3)]"],
            "hint": "fold с вектором в качестве накопителя: смотрим last_mut() — продолжаем серию или начинаем новую.",
        },
        {
            "id": "rs7-apply-all",
            "mode": "rust",
            "title": "Список замыканий",
            "statement": (
                "Напишите apply_all(x: i32, fs: &[Box<dyn Fn(i32) -> i32>]) -> "
                "Vec<i32>: результаты всех функций для x, и apply_chain(x: i32, fs: "
                "&[Box<dyn Fn(i32) -> i32>]) -> i32: результат последовательного "
                "применения (выход одной — вход следующей)."
            ),
            "starter": "fn apply_all(x: i32, fs: &[Box<dyn Fn(i32) -> i32>]) -> Vec<i32> {\n    todo!()\n}\n\nfn apply_chain(x: i32, fs: &[Box<dyn Fn(i32) -> i32>]) -> i32 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let k = 3;\n"
                "    let fs: Vec<Box<dyn Fn(i32) -> i32>> = vec![Box::new(|x| x + 1), Box::new(move |x| x * k), Box::new(|x| x - 10)];\n"
                "    println!(\"{:?}\", apply_all(5, &fs));\n"
                "    println!(\"{}\", apply_chain(5, &fs));\n"
                "    println!(\"{}\", apply_chain(7, &[]));\n"
                "}\n"
            ),
            "expected": ["[6, 15, -5]", "8", "7"],
            "hint": "fold(x, |acc, f| f(acc)) — свёртка со стартовым значением x.",
        },
    ],
    8: [
        {
            "id": "rs8-longest",
            "mode": "rust",
            "title": "Времена жизни в сигнатурах",
            "statement": (
                "Напишите longest_of_three<'a>(a: &'a str, b: &'a str, c: &'a str) "
                "-> &'a str (самая длинная по байтам; при равенстве — более ранняя) "
                "и pick_first<'a>(a: &'a str, _b: &str) -> &'a str — возвращает a "
                "(второй аргумент может жить короче)."
            ),
            "starter": "fn longest_of_three<'a>(a: &'a str, b: &'a str, c: &'a str) -> &'a str {\n    todo!()\n}\n\nfn pick_first<'a>(a: &'a str, _b: &str) -> &'a str {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let outer = String::from(\"outer-long\");\n"
                "    let r;\n"
                "    {\n"
                "        let tmp = String::from(\"tmp\");\n"
                "        r = pick_first(&outer, &tmp);\n"
                "    }\n"
                "    println!(\"{}\", r);\n"
                "    println!(\"{}\", longest_of_three(\"aa\", \"bbbb\", \"cc\"));\n"
                "    println!(\"{}\", longest_of_three(\"xx\", \"yy\", \"zz\"));\n"
                "    println!(\"{}\", longest_of_three(\"a\", \"bb\", \"ccc\"));\n"
                "}\n"
            ),
            "expected": ["outer-long", "bbbb", "xx", "ccc"],
            "hint": "Все три аргумента и результат связаны одним 'a; у pick_first результат связан только с первым аргументом.",
        },
        {
            "id": "rs8-parser",
            "mode": "rust",
            "title": "Структура со ссылкой",
            "statement": (
                "Реализуйте Tokenizer<'a> { src: &'a str }: new(src), "
                "next_token(&mut self) -> Option<&'a str> — следующее слово (слова "
                "разделены пробельными символами), и remaining(&self) -> &'a str — "
                "ещё не прочитанная часть без ведущих пробелов. Токены не "
                "копируются — это срезы исходной строки."
            ),
            "starter": "struct Tokenizer<'a> {\n    src: &'a str,\n}\n\nimpl<'a> Tokenizer<'a> {\n    fn new(src: &'a str) -> Tokenizer<'a> {\n        todo!()\n    }\n    fn next_token(&mut self) -> Option<&'a str> {\n        todo!()\n    }\n    fn remaining(&self) -> &'a str {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let text = String::from(\"  let x =   42 ;\");\n"
                "    let mut t = Tokenizer::new(&text);\n"
                "    let first = t.next_token();\n"
                "    let second = t.next_token();\n"
                "    println!(\"{:?} {:?}\", first, second);\n"
                "    println!(\"[{}]\", t.remaining());\n"
                "    let mut count = 0;\n"
                "    while let Some(_) = t.next_token() {\n"
                "        count += 1;\n"
                "    }\n"
                "    println!(\"{} {:?} [{}]\", count, t.next_token(), t.remaining());\n"
                "}\n"
            ),
            "expected": ["Some(\"let\") Some(\"x\")", "[=   42 ;]", "3 None []"],
            "hint": "Токены — срезы, поэтому метод возвращает &'a str (время жизни исходной строки), а не время жизни &mut self.",
        },
        {
            "id": "rs8-box-list",
            "mode": "rust",
            "title": "Список на Box",
            "statement": (
                "Дан enum List { Cons(i32, Box<List>), Nil }. Напишите "
                "from_slice(v: &[i32]) -> List, sum(l: &List) -> i32, len(l: &List) "
                "-> usize и to_vec(l: &List) -> Vec<i32> (в порядке списка)."
            ),
            "starter": "enum List {\n    Cons(i32, Box<List>),\n    Nil,\n}\nuse List::{Cons, Nil};\n\nfn from_slice(v: &[i32]) -> List {\n    todo!()\n}\n\nfn sum(l: &List) -> i32 {\n    todo!()\n}\n\nfn len(l: &List) -> usize {\n    todo!()\n}\n\nfn to_vec(l: &List) -> Vec<i32> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let l = from_slice(&[4, 8, 15, 16]);\n"
                "    println!(\"{} {} {:?}\", sum(&l), len(&l), to_vec(&l));\n"
                "    let e = from_slice(&[]);\n"
                "    println!(\"{} {} {:?}\", sum(&e), len(&e), to_vec(&e));\n"
                "}\n"
            ),
            "expected": ["43 4 [4, 8, 15, 16]", "0 0 []"],
            "hint": "v.split_first() даёт (голова, хвост); Box::new(from_slice(хвост)) — продолжение списка.",
        },
        {
            "id": "rs8-drop-order",
            "mode": "rust",
            "title": "Порядок вызова drop",
            "statement": (
                "Реализуйте Drop для Logger: в момент уничтожения в общий журнал "
                "log (Rc<RefCell<Vec<String>>>) дописывается строка \"drop <имя>\". "
                "Структура и конструктор Logger::new(name, log) уже есть."
            ),
            "starter": "use std::cell::RefCell;\nuse std::rc::Rc;\n\nstruct Logger {\n    name: String,\n    log: Rc<RefCell<Vec<String>>>,\n}\n\nimpl Logger {\n    fn new(name: &str, log: &Rc<RefCell<Vec<String>>>) -> Logger {\n        Logger { name: name.to_string(), log: Rc::clone(log) }\n    }\n}\n\n// impl Drop for Logger ...\n",
            "driver": (
                "fn main() {\n"
                "    let log = Rc::new(RefCell::new(Vec::new()));\n"
                "    {\n"
                "        let _a = Logger::new(\"a\", &log);\n"
                "        let b = Logger::new(\"b\", &log);\n"
                "        {\n"
                "            let _c = Logger::new(\"c\", &log);\n"
                "        }\n"
                "        drop(b);\n"
                "        log.borrow_mut().push(\"end of scope\".to_string());\n"
                "    }\n"
                "    let boxed: Vec<Logger> = vec![Logger::new(\"x\", &log), Logger::new(\"y\", &log)];\n"
                "    drop(boxed);\n"
                "    println!(\"{:?}\", log.borrow());\n"
                "    println!(\"{}\", Rc::strong_count(&log));\n"
                "}\n"
            ),
            "expected": ["[\"drop c\", \"drop b\", \"end of scope\", \"drop a\", \"drop x\", \"drop y\"]", "1"],
            "hint": "fn drop(&mut self) вызывается компилятором сам; запись в журнал: self.log.borrow_mut().push(...).",
        },
        {
            "id": "rs8-tree-rc",
            "mode": "rust",
            "title": "Дерево с общими узлами",
            "statement": (
                "Дано TreeNode { val: i32, children: Vec<Rc<RefCell<TreeNode>>> }. "
                "Напишите sum(node: &Rc<RefCell<TreeNode>>) -> i32 (сумма значений "
                "поддерева) и add_all(node: &Rc<RefCell<TreeNode>>, delta: i32) "
                "(прибавить delta ко всем значениям поддерева)."
            ),
            "starter": "use std::cell::RefCell;\nuse std::rc::Rc;\n\nstruct TreeNode {\n    val: i32,\n    children: Vec<Rc<RefCell<TreeNode>>>,\n}\n\nfn sum(node: &Rc<RefCell<TreeNode>>) -> i32 {\n    todo!()\n}\n\nfn add_all(node: &Rc<RefCell<TreeNode>>, delta: i32) {\n    todo!()\n}\n",
            "driver": (
                "fn leaf(v: i32) -> Rc<RefCell<TreeNode>> {\n"
                "    Rc::new(RefCell::new(TreeNode { val: v, children: vec![] }))\n"
                "}\n"
                "\n"
                "fn main() {\n"
                "    let shared = leaf(10);\n"
                "    let a = Rc::new(RefCell::new(TreeNode { val: 1, children: vec![Rc::clone(&shared), leaf(2)] }));\n"
                "    let root = Rc::new(RefCell::new(TreeNode { val: 100, children: vec![Rc::clone(&a), Rc::clone(&shared)] }));\n"
                "    println!(\"{}\", sum(&root));\n"
                "    add_all(&a, 5);\n"
                "    println!(\"{} {}\", sum(&root), shared.borrow().val);\n"
                "    println!(\"{}\", Rc::strong_count(&shared));\n"
                "}\n"
            ),
            "expected": ["123", "143 15", "3"],
            "hint": "borrow() для чтения, borrow_mut() для записи; держите изменяющий доступ только к текущему узлу — потомков берёт отдельный вызов.",
        },
        {
            "id": "rs8-shared-account",
            "mode": "rust",
            "title": "Общий счёт на Rc<RefCell>",
            "statement": (
                "Дано Account { balance: i64 } в Rc<RefCell<>>. Напишите "
                "transfer(from, to, amount: i64) -> Result<(), String>: если amount "
                "≤ 0 — Err(\"invalid amount\"); если у from не хватает денег — "
                "Err(\"insufficient funds\"); если from и to — один и тот же счёт "
                "(Rc::ptr_eq) — Ok(()) без изменений; иначе перевести."
            ),
            "starter": "use std::cell::RefCell;\nuse std::rc::Rc;\n\nstruct Account {\n    balance: i64,\n}\n\nfn transfer(from: &Rc<RefCell<Account>>, to: &Rc<RefCell<Account>>, amount: i64) -> Result<(), String> {\n    todo!()\n}\n",
            "driver": (
                "fn acc(b: i64) -> Rc<RefCell<Account>> {\n"
                "    Rc::new(RefCell::new(Account { balance: b }))\n"
                "}\n"
                "\n"
                "fn main() {\n"
                "    let a = acc(100);\n"
                "    let b = acc(5);\n"
                "    println!(\"{:?}\", transfer(&a, &b, 30));\n"
                "    println!(\"{:?}\", transfer(&a, &b, 100));\n"
                "    println!(\"{:?}\", transfer(&a, &b, 0));\n"
                "    println!(\"{:?}\", transfer(&a, &a, 10));\n"
                "    println!(\"{} {}\", a.borrow().balance, b.borrow().balance);\n"
                "}\n"
            ),
            "expected": ["Ok(())", "Err(\"insufficient funds\")", "Err(\"invalid amount\")", "Ok(())", "70 35"],
            "hint": "Сравнивайте счета через Rc::ptr_eq; иначе borrow_mut() дважды у одного RefCell приведёт к панике.",
        },
        {
            "id": "rs8-weak-chain",
            "mode": "rust",
            "title": "Слабые ссылки на начальство",
            "statement": (
                "Дано Employee { name: String, boss: RefCell<Weak<Employee>> }. "
                "Напишите chain_of_command(e: &Rc<Employee>) -> Vec<String>: имя "
                "сотрудника, затем его начальника, начальника начальника и т. д. "
                "(пока слабая ссылка жива)."
            ),
            "starter": "use std::cell::RefCell;\nuse std::rc::{Rc, Weak};\n\nstruct Employee {\n    name: String,\n    boss: RefCell<Weak<Employee>>,\n}\n\nfn chain_of_command(e: &Rc<Employee>) -> Vec<String> {\n    todo!()\n}\n",
            "driver": (
                "fn emp(name: &str) -> Rc<Employee> {\n"
                "    Rc::new(Employee { name: name.to_string(), boss: RefCell::new(Weak::new()) })\n"
                "}\n"
                "\n"
                "fn main() {\n"
                "    let ceo = emp(\"ceo\");\n"
                "    let cto = emp(\"cto\");\n"
                "    let dev = emp(\"dev\");\n"
                "    *cto.boss.borrow_mut() = Rc::downgrade(&ceo);\n"
                "    *dev.boss.borrow_mut() = Rc::downgrade(&cto);\n"
                "    println!(\"{:?}\", chain_of_command(&dev));\n"
                "    println!(\"{:?}\", chain_of_command(&ceo));\n"
                "    drop(ceo);\n"
                "    println!(\"{:?}\", chain_of_command(&dev));\n"
                "    println!(\"{}\", Rc::weak_count(&cto));\n"
                "}\n"
            ),
            "expected": ["[\"dev\", \"cto\", \"ceo\"]", "[\"ceo\"]", "[\"dev\", \"cto\"]", "1"],
            "hint": "upgrade() возвращает Option<Rc<Employee>>: пока начальник жив — идём выше, иначе цепочка заканчивается.",
        },
        {
            "id": "rs8-bst",
            "mode": "rust",
            "title": "Двоичное дерево поиска",
            "statement": (
                "Дополните Bst: insert(&mut self, key) (дубликаты игнорируются), "
                "contains(&self, key) -> bool, height(&self) -> usize (пустое "
                "дерево — 0, один узел — 1) и min(&self) -> Option<i32>. Внутри — "
                "Option<Box<Node>>."
            ),
            "starter": "struct Node {\n    key: i32,\n    left: Option<Box<Node>>,\n    right: Option<Box<Node>>,\n}\n\nstruct Bst {\n    root: Option<Box<Node>>,\n}\n\nimpl Bst {\n    fn new() -> Bst {\n        Bst { root: None }\n    }\n    fn insert(&mut self, key: i32) {\n        todo!()\n    }\n    fn contains(&self, key: i32) -> bool {\n        todo!()\n    }\n    fn height(&self) -> usize {\n        todo!()\n    }\n    fn min(&self) -> Option<i32> {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let mut t = Bst::new();\n"
                "    println!(\"{} {:?} {}\", t.height(), t.min(), t.contains(1));\n"
                "    for k in [50, 30, 70, 20, 40, 60, 80, 30, 10] {\n"
                "        t.insert(k);\n"
                "    }\n"
                "    println!(\"{} {:?}\", t.height(), t.min());\n"
                "    println!(\"{} {} {}\", t.contains(60), t.contains(65), t.contains(10));\n"
                "    let mut chain = Bst::new();\n"
                "    for k in 1..=100 {\n"
                "        chain.insert(k);\n"
                "    }\n"
                "    println!(\"{} {:?}\", chain.height(), chain.min());\n"
                "}\n"
            ),
            "expected": ["0 None false", "4 Some(10)", "true false true", "100 Some(1)"],
            "hint": "Итеративная вставка через &mut Option<Box<Node>>: идём вниз, пока слот занят, и записываем новый узел в пустой.",
        },
        {
            "id": "rs8-cow-normalize",
            "mode": "rust",
            "title": "Cow: копировать только при необходимости",
            "statement": (
                "Напишите normalize(s: &str) -> Cow<str>: удаляет пробелы по краям "
                "и приводит к нижнему регистру (ASCII). Если строка уже в "
                "нормальном виде (ни пробелов по краям, ни заглавных ASCII-букв) — "
                "верните Cow::Borrowed без копирования; иначе Cow::Owned."
            ),
            "starter": "use std::borrow::Cow;\n\nfn normalize(s: &str) -> Cow<str> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for s in [\"already\", \"  Padded Text  \", \"UPPER\", \"\", \"ünïcode Ok\"] {\n"
                "        let c = normalize(s);\n"
                "        let kind = match &c {\n"
                "            Cow::Borrowed(_) => \"borrowed\",\n"
                "            Cow::Owned(_) => \"owned\",\n"
                "        };\n"
                "        println!(\"[{}] {}\", c, kind);\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["[already] borrowed", "[padded text] owned", "[upper] owned", "[] borrowed", "[ünïcode ok] owned"],
            "hint": "Сначала проверьте, нужна ли работа: trim() == s и нет заглавных; только тогда Borrowed.",
        },
    ],
    9: [
        {
            "id": "rs9-visibility",
            "mode": "rust",
            "title": "Видимость в модуле",
            "statement": (
                "Модуль geometry написан, но снаружи ничего не доступно. Расставьте "
                "pub так, чтобы заработали: Point::new, поля x и y нельзя трогать "
                "напрямую (только методы x(), y()), функция distance(a, b) -> f64, "
                "а приватная функция square остаётся скрытой."
            ),
            "starter": "mod geometry {\n    struct Point {\n        x: f64,\n        y: f64,\n    }\n\n    impl Point {\n        fn new(x: f64, y: f64) -> Point {\n            Point { x, y }\n        }\n        fn x(&self) -> f64 {\n            self.x\n        }\n        fn y(&self) -> f64 {\n            self.y\n        }\n    }\n\n    fn square(v: f64) -> f64 {\n        v * v\n    }\n\n    fn distance(a: &Point, b: &Point) -> f64 {\n        (square(a.x - b.x) + square(a.y - b.y)).sqrt()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let a = geometry::Point::new(0.0, 0.0);\n"
                "    let b = geometry::Point::new(3.0, 4.0);\n"
                "    println!(\"{} {} {}\", a.x(), b.y(), geometry::distance(&a, &b));\n"
                "}\n"
            ),
            "expected": ["0 4 5"],
            "hint": "pub нужен у структуры, у конструктора и методов, у distance; поля x и y оставьте приватными.",
        },
        {
            "id": "rs9-reexport",
            "mode": "rust",
            "title": "Реэкспорт и пути",
            "statement": (
                "Внутри mod util лежат вложенные модули math и text. Добавьте в "
                "util строки pub use, чтобы снаружи работали util::gcd, util::lcm и "
                "util::title_case (а не util::math::gcd). Недостающие импорты "
                "внутри модулей допишите сами."
            ),
            "starter": "mod util {\n    pub mod math {\n        pub fn gcd(a: u64, b: u64) -> u64 {\n            if b == 0 { a } else { gcd(b, a % b) }\n        }\n        pub fn lcm(a: u64, b: u64) -> u64 {\n            a / gcd(a, b) * b\n        }\n    }\n\n    pub mod text {\n        pub fn title_case(s: &str) -> String {\n            s.split(' ')\n                .map(|w| {\n                    let mut c = w.chars();\n                    match c.next() {\n                        Some(f) => f.to_uppercase().collect::<String>() + c.as_str(),\n                        None => String::new(),\n                    }\n                })\n                .collect::<Vec<_>>()\n                .join(\" \")\n        }\n    }\n\n    // pub use ...\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{} {}\", util::gcd(48, 18), util::lcm(4, 6));\n"
                "    println!(\"{}\", util::title_case(\"hello big world\"));\n"
                "    println!(\"{}\", util::math::gcd(7, 3));\n"
                "}\n"
            ),
            "expected": ["6 12", "Hello Big World", "1"],
            "hint": "pub use self::math::{gcd, lcm}; — имена появляются на уровне util.",
        },
        {
            "id": "rs9-fromstr-rgb",
            "mode": "rust",
            "title": "FromStr для цвета",
            "statement": (
                "Реализуйте FromStr для Rgb: '#rrggbb' (шестнадцатеричные цифры "
                "любого регистра) → Rgb { r, g, b }. Ошибки (Err(String)): строка "
                "не начинается с '#' или длина не 7 → \"bad format\"; "
                "нешестнадцатеричный символ → \"bad digit\". Метод to_hex(&self) -> "
                "String возвращает '#rrggbb' строчными буквами."
            ),
            "starter": "use std::str::FromStr;\n\n#[derive(Debug, PartialEq)]\nstruct Rgb {\n    r: u8,\n    g: u8,\n    b: u8,\n}\n\nimpl Rgb {\n    fn to_hex(&self) -> String {\n        todo!()\n    }\n}\n\nimpl FromStr for Rgb {\n    type Err = String;\n    fn from_str(s: &str) -> Result<Rgb, String> {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", \"#ff8800\".parse::<Rgb>());\n"
                "    println!(\"{:?}\", \"#FFFFFF\".parse::<Rgb>());\n"
                "    println!(\"{:?} {:?} {:?}\", \"ff8800\".parse::<Rgb>(), \"#12\".parse::<Rgb>(), \"#gg0000\".parse::<Rgb>());\n"
                "    let c: Rgb = \"#0a0B0c\".parse().unwrap();\n"
                "    println!(\"{}\", c.to_hex());\n"
                "}\n"
            ),
            "expected": ["Ok(Rgb { r: 255, g: 136, b: 0 })", "Ok(Rgb { r: 255, g: 255, b: 255 })", "Err(\"bad format\") Err(\"bad format\") Err(\"bad digit\")", "#0a0b0c"],
            "hint": "u8::from_str_radix(&s[1..3], 16) разбирает пару цифр; {:02x} печатает байт двумя шестнадцатеричными цифрами.",
        },
        {
            "id": "rs9-builder",
            "mode": "rust",
            "title": "Паттерн «строитель»",
            "statement": (
                "Реализуйте HttpRequest и строитель RequestBuilder: "
                "RequestBuilder::new(url) (метод по умолчанию \"GET\", без заголовков "
                "и тела), method(self, &str), header(self, name, value) (можно "
                "несколько), body(self, &str) и build(self) -> HttpRequest. У "
                "HttpRequest — поля method, url, headers: Vec<(String, String)>, "
                "body: Option<String>."
            ),
            "starter": "struct HttpRequest {\n    method: String,\n    url: String,\n    headers: Vec<(String, String)>,\n    body: Option<String>,\n}\n\nstruct RequestBuilder {\n    // поля строителя\n}\n\nimpl RequestBuilder {\n    fn new(url: &str) -> RequestBuilder {\n        todo!()\n    }\n    fn method(self, m: &str) -> RequestBuilder {\n        todo!()\n    }\n    fn header(self, name: &str, value: &str) -> RequestBuilder {\n        todo!()\n    }\n    fn body(self, b: &str) -> RequestBuilder {\n        todo!()\n    }\n    fn build(self) -> HttpRequest {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let r = RequestBuilder::new(\"/users\").build();\n"
                "    println!(\"{} {} {} {:?}\", r.method, r.url, r.headers.len(), r.body);\n"
                "    let p = RequestBuilder::new(\"/login\")\n"
                "        .method(\"POST\")\n"
                "        .header(\"Content-Type\", \"text/plain\")\n"
                "        .header(\"X-Id\", \"7\")\n"
                "        .body(\"hello\")\n"
                "        .build();\n"
                "    println!(\"{} {} {:?} {:?}\", p.method, p.url, p.headers, p.body);\n"
                "}\n"
            ),
            "expected": ["GET /users 0 None", "POST /login [(\"Content-Type\", \"text/plain\"), (\"X-Id\", \"7\")] Some(\"hello\")"],
            "hint": "Каждый метод принимает mut self и возвращает self — так работают цепочки вызовов.",
        },
        {
            "id": "rs9-default-config",
            "mode": "rust",
            "title": "Default и обновление структуры",
            "statement": (
                "Реализуйте Default для Config вручную: host = \"localhost\", port = "
                "8080, debug = false, workers = 4. Затем напишите "
                "with_overrides(port: Option<u16>, debug: Option<bool>) -> Config: "
                "значения из Some заменяют умолчания."
            ),
            "starter": "#[derive(Debug, Clone, PartialEq)]\nstruct Config {\n    host: String,\n    port: u16,\n    debug: bool,\n    workers: u32,\n}\n\nimpl Default for Config {\n    fn default() -> Config {\n        todo!()\n    }\n}\n\nfn with_overrides(port: Option<u16>, debug: Option<bool>) -> Config {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", Config::default());\n"
                "    println!(\"{:?}\", with_overrides(Some(3000), None));\n"
                "    println!(\"{:?}\", with_overrides(None, Some(true)));\n"
                "    println!(\"{}\", with_overrides(None, None) == Config::default());\n"
                "}\n"
            ),
            "expected": ["Config { host: \"localhost\", port: 8080, debug: false, workers: 4 }", "Config { host: \"localhost\", port: 3000, debug: false, workers: 4 }", "Config { host: \"localhost\", port: 8080, debug: true, workers: 4 }", "true"],
            "hint": "Синтаксис обновления: Config { port: ..., ..Default::default() } берёт остальные поля из значения по умолчанию.",
        },
        {
            "id": "rs9-from-into",
            "mode": "rust",
            "title": "From и Into",
            "statement": (
                "Реализуйте From<Celsius> для Fahrenheit (f = c · 9/5 + 32), "
                "From<(i32, i32)> для Point и From<Point> для (i32, i32). После "
                "этого .into() должен работать в обе стороны."
            ),
            "starter": "#[derive(Debug, Clone, Copy)]\nstruct Celsius(f64);\n#[derive(Debug, Clone, Copy)]\nstruct Fahrenheit(f64);\n#[derive(Debug, Clone, Copy, PartialEq)]\nstruct Point {\n    x: i32,\n    y: i32,\n}\n\n// impl From<Celsius> for Fahrenheit ...\n// impl From<(i32, i32)> for Point ...\n// impl From<Point> for (i32, i32) ...\n",
            "driver": (
                "fn main() {\n"
                "    let f: Fahrenheit = Celsius(100.0).into();\n"
                "    println!(\"{:?} {:?}\", f, Fahrenheit::from(Celsius(-40.0)));\n"
                "    let p: Point = (3, 4).into();\n"
                "    let t: (i32, i32) = p.into();\n"
                "    println!(\"{:?} {:?} {}\", p, t, Point::from((3, 4)) == p);\n"
                "}\n"
            ),
            "expected": ["Fahrenheit(212.0) Fahrenheit(-40.0)", "Point { x: 3, y: 4 } (3, 4) true"],
            "hint": "Реализуйте только From — Into для обратной стороны появится автоматически.",
        },
        {
            "id": "rs9-parse-config",
            "mode": "rust",
            "title": "Библиотека с Box<dyn Error>",
            "statement": (
                "Напишите parse_config(text: &str) -> Result<Vec<(String, i32)>, "
                "Box<dyn Error>>: строки 'ключ=число' (пустые и начинающиеся с '#' "
                "пропускаются). Нет '=' — ошибка с текстом \"line N: missing '='\" (N "
                "с единицы по всем строкам), ключ не из списка port/workers/timeout "
                "— \"line N: unknown key KEY\", значение не число — ошибка разбора "
                "числа (через ?). Первая же ошибка прекращает работу."
            ),
            "starter": "use std::error::Error;\n\nfn parse_config(text: &str) -> Result<Vec<(String, i32)>, Box<dyn Error>> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for text in [\"port=80\\nworkers = 4\\n\", \"# c\\n\\nport=1\\nhost=x\", \"port 80\", \"timeout=abc\", \"\"] {\n"
                "        match parse_config(text) {\n"
                "            Ok(v) => println!(\"ok {:?}\", v),\n"
                "            Err(e) => println!(\"err {}\", e),\n"
                "        }\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["ok [(\"port\", 80), (\"workers\", 4)]", "err line 4: unknown key host", "err line 1: missing '='", "err invalid digit found in string", "ok []"],
            "hint": ".into() превращает String в Box<dyn Error>; ? делает то же для ParseIntError.",
        },
        {
            "id": "rs9-version",
            "mode": "rust",
            "title": "Версии: FromStr, Display, Ord",
            "statement": (
                "Реализуйте для Version { major, minor, patch } (все u32): FromStr "
                "('1.2.3' → версия; иначе Err(\"bad version\")), Display ('1.2.3'). "
                "Порядок уже выведен через derive(PartialOrd, Ord) — убедитесь, что "
                "поля идут в нужной последовательности. Напишите newest(items: "
                "&[&str]) -> Option<String>: самая новая из корректных версий."
            ),
            "starter": "use std::fmt;\nuse std::str::FromStr;\n\n#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]\nstruct Version {\n    // поля\n}\n\n// impl FromStr for Version ...\n// impl fmt::Display for Version ...\n\nfn newest(items: &[&str]) -> Option<String> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", \"1.10.2\".parse::<Version>());\n"
                "    println!(\"{:?} {:?}\", \"1.2\".parse::<Version>(), \"1.x.3\".parse::<Version>());\n"
                "    println!(\"{:?}\", newest(&[\"1.2.9\", \"1.10.0\", \"bad\", \"1.9.99\"]));\n"
                "    println!(\"{:?}\", newest(&[\"x\"]));\n"
                "    let a: Version = \"2.0.0\".parse().unwrap();\n"
                "    let b: Version = \"1.99.99\".parse().unwrap();\n"
                "    println!(\"{} {}\", a > b, a);\n"
                "}\n"
            ),
            "expected": ["Ok(Version { major: 1, minor: 10, patch: 2 })", "Err(\"bad version\") Err(\"bad version\")", "Some(\"1.10.0\")", "None", "true 2.0.0"],
            "hint": "Порядок полей в структуре задаёт лексикографический порядок derive(Ord): major, minor, patch.",
        },
        {
            "id": "rs9-static-counter",
            "mode": "rust",
            "title": "Глобальный счётчик",
            "statement": (
                "Напишите next_ticket() -> u32 с глобальным атомарным счётчиком "
                "(static AtomicU32, начинается с 1000) — каждый вызов возвращает "
                "следующий номер — и reset_tickets(). Потокобезопасность "
                "обеспечивается атомарной операцией."
            ),
            "starter": "use std::sync::atomic::{AtomicU32, Ordering};\n\nstatic TICKETS: AtomicU32 = AtomicU32::new(1000);\n\nfn next_ticket() -> u32 {\n    todo!()\n}\n\nfn reset_tickets() {\n    todo!()\n}\n",
            "driver": (
                "use std::thread;\n"
                "\n"
                "fn main() {\n"
                "    println!(\"{} {} {}\", next_ticket(), next_ticket(), next_ticket());\n"
                "    reset_tickets();\n"
                "    let handles: Vec<_> = (0..4).map(|_| thread::spawn(|| (0..250).map(|_| next_ticket()).max().unwrap())).collect();\n"
                "    let max = handles.into_iter().map(|h| h.join().unwrap()).max().unwrap();\n"
                "    println!(\"{} {}\", max >= 1999, next_ticket());\n"
                "}\n"
            ),
            "expected": ["1000 1001 1002", "true 2000"],
            "hint": "fetch_add возвращает старое значение и увеличивает счётчик атомарно.",
        },
    ],
    10: [
        {
            "id": "rs10-par-sum",
            "mode": "rust",
            "title": "Параллельная сумма",
            "statement": (
                "Напишите par_sum(v: &[u64], parts: usize) -> u64: разделите срез "
                "на parts частей (последняя может быть короче) и просуммируйте их в "
                "потоках thread::scope. parts ≥ 1; срез может быть пустым."
            ),
            "starter": "use std::thread;\n\nfn par_sum(v: &[u64], parts: usize) -> u64 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let v: Vec<u64> = (1..=100_000).collect();\n"
                "    println!(\"{} {} {}\", par_sum(&v, 1), par_sum(&v, 4), par_sum(&v, 1000));\n"
                "    println!(\"{} {}\", par_sum(&[], 3), par_sum(&[7], 5));\n"
                "}\n"
            ),
            "expected": ["5000050000 5000050000 5000050000", "0 7"],
            "hint": "chunks(size) выдаёт срезы; каждый срез — в s.spawn(...) внутри scope; join возвращает частичную сумму.",
        },
        {
            "id": "rs10-word-count-par",
            "mode": "rust",
            "title": "Подсчёт слов в потоках",
            "statement": (
                "Напишите count_words(texts: Vec<String>) -> BTreeMap<String, "
                "usize>: по одному потоку на текст считает слова (по пробельным "
                "символам, в нижнем регистре), результаты объединяются в общую "
                "таблицу."
            ),
            "starter": "use std::collections::BTreeMap;\n\nfn count_words(texts: Vec<String>) -> BTreeMap<String, usize> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let r = count_words(vec![\"the cat\".to_string(), \"The dog the end\".to_string(), \"\".to_string(), \"cat CAT\".to_string()]);\n"
                "    println!(\"{:?}\", r);\n"
                "    println!(\"{}\", count_words(vec![]).len());\n"
                "}\n"
            ),
            "expected": ["{\"cat\": 3, \"dog\": 1, \"end\": 1, \"the\": 3}", "0"],
            "hint": "Каждый поток возвращает свою таблицу через join; слияние — в основном потоке.",
        },
        {
            "id": "rs10-pipeline",
            "mode": "rust",
            "title": "Конвейер из потоков",
            "statement": (
                "Напишите run_pipeline(items: Vec<i32>) -> Vec<i32>: первый "
                "поток-стадия возводит число в квадрат, второй прибавляет 1; стадии "
                "соединены каналами, порядок результатов сохраняется. Основной "
                "поток собирает итог."
            ),
            "starter": "use std::sync::mpsc;\nuse std::thread;\n\nfn run_pipeline(items: Vec<i32>) -> Vec<i32> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", run_pipeline(vec![1, 2, 3, 4]));\n"
                "    println!(\"{:?}\", run_pipeline(vec![]));\n"
                "    println!(\"{:?}\", run_pipeline((-3..=3).collect()));\n"
                "}\n"
            ),
            "expected": ["[2, 5, 10, 17]", "[]", "[10, 5, 2, 1, 2, 5, 10]"],
            "hint": "Каждая стадия — поток с циклом for x in rx; когда предыдущий передатчик уничтожен, цикл заканчивается и закрывает следующий канал.",
        },
        {
            "id": "rs10-counter",
            "mode": "rust",
            "title": "Общий счётчик",
            "statement": (
                "Напишите count_parallel(threads: usize, per_thread: u64) -> u64: "
                "запустите threads потоков, каждый прибавляет к общему счётчику "
                "Arc<Mutex<u64>> единицу per_thread раз; верните итог."
            ),
            "starter": "use std::sync::{Arc, Mutex};\nuse std::thread;\n\nfn count_parallel(threads: usize, per_thread: u64) -> u64 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{}\", count_parallel(8, 10_000));\n"
                "    println!(\"{}\", count_parallel(1, 5));\n"
                "    println!(\"{}\", count_parallel(0, 100));\n"
                "    println!(\"{}\", count_parallel(16, 0));\n"
                "}\n"
            ),
            "expected": ["80000", "5", "0", "0"],
            "hint": "Каждый поток получает свой клон Arc; блокировку берите на каждый шаг или один раз на весь цикл.",
        },
        {
            "id": "rs10-transfers",
            "mode": "rust",
            "title": "Переводы без взаимной блокировки",
            "statement": (
                "Напишите transfer(accounts: &[Mutex<i64>], from: usize, to: usize, "
                "amount: i64) -> bool: если from == to или на счёте не хватает "
                "денег — false и ничего не меняется; иначе перевести и вернуть "
                "true. Блокировки берите всегда в порядке возрастания индекса, "
                "чтобы встречные переводы из разных потоков не зашли в тупик."
            ),
            "starter": "use std::sync::Mutex;\n\nfn transfer(accounts: &[Mutex<i64>], from: usize, to: usize, amount: i64) -> bool {\n    todo!()\n}\n",
            "driver": (
                "use std::sync::Arc;\n"
                "use std::thread;\n"
                "\n"
                "fn main() {\n"
                "    let accounts: Arc<Vec<Mutex<i64>>> = Arc::new((0..4).map(|_| Mutex::new(1000)).collect());\n"
                "    println!(\"{} {}\", transfer(&accounts, 0, 1, 2000), transfer(&accounts, 2, 2, 1));\n"
                "    let hs: Vec<_> = (0..8)\n"
                "        .map(|t| {\n"
                "            let acc = Arc::clone(&accounts);\n"
                "            thread::spawn(move || {\n"
                "                for i in 0..2000 {\n"
                "                    let from = (t + i) % 4;\n"
                "                    let to = (t * 3 + i * 7 + 1) % 4;\n"
                "                    transfer(&acc, from, to, 7);\n"
                "                }\n"
                "            })\n"
                "        })\n"
                "        .collect();\n"
                "    for h in hs {\n"
                "        h.join().unwrap();\n"
                "    }\n"
                "    let total: i64 = accounts.iter().map(|m| *m.lock().unwrap()).sum();\n"
                "    println!(\"{}\", total);\n"
                "}\n"
            ),
            "expected": ["false false", "4000"],
            "hint": "Захватывайте мьютексы в порядке индексов независимо от направления перевода; потом решайте, где источник и приёмник.",
        },
        {
            "id": "rs10-cache",
            "mode": "rust",
            "title": "Кэш с RwLock",
            "statement": (
                "Напишите Cache::get_or_compute(&self, key: u64, compute: impl "
                "Fn(u64) -> u64) -> u64: сначала читает через RwLock (read), при "
                "промахе берёт write и ПОВТОРНО проверяет, не успел ли другой поток "
                "вычислить значение; вычисление для ключа выполняется ровно один "
                "раз."
            ),
            "starter": "use std::collections::HashMap;\nuse std::sync::RwLock;\n\nstruct Cache {\n    map: RwLock<HashMap<u64, u64>>,\n}\n\nimpl Cache {\n    fn new() -> Cache {\n        Cache { map: RwLock::new(HashMap::new()) }\n    }\n    fn get_or_compute(&self, key: u64, compute: impl Fn(u64) -> u64) -> u64 {\n        todo!()\n    }\n}\n",
            "driver": (
                "use std::sync::atomic::{AtomicUsize, Ordering};\n"
                "use std::sync::Arc;\n"
                "use std::thread;\n"
                "\n"
                "fn main() {\n"
                "    let cache = Arc::new(Cache::new());\n"
                "    let calls = Arc::new(AtomicUsize::new(0));\n"
                "    let hs: Vec<_> = (0..8)\n"
                "        .map(|_| {\n"
                "            let (cache, calls) = (Arc::clone(&cache), Arc::clone(&calls));\n"
                "            thread::spawn(move || {\n"
                "                let mut sum = 0;\n"
                "                for k in 0..50u64 {\n"
                "                    sum += cache.get_or_compute(k, |x| {\n"
                "                        calls.fetch_add(1, Ordering::SeqCst);\n"
                "                        x * x\n"
                "                    });\n"
                "                }\n"
                "                sum\n"
                "            })\n"
                "        })\n"
                "        .collect();\n"
                "    let sums: Vec<u64> = hs.into_iter().map(|h| h.join().unwrap()).collect();\n"
                "    println!(\"{:?}\", sums.iter().all(|&s| s == sums[0]));\n"
                "    println!(\"{} {}\", sums[0], calls.load(Ordering::SeqCst));\n"
                "}\n"
            ),
            "expected": ["true", "40425 50"],
            "hint": "Классическая двойная проверка: read → промах → write → снова get → вычислить и вставить. Защитник read должен быть освобождён до write.",
        },
        {
            "id": "rs10-map-parallel",
            "mode": "rust",
            "title": "Параллельное отображение с сохранением порядка",
            "statement": (
                "Напишите map_parallel<F>(items: Vec<u64>, workers: usize, f: F) -> "
                "Vec<u64> where F: Fn(u64) -> u64 + Send + Sync + 'static: "
                "применить f ко всем элементам в нескольких потоках, результат — в "
                "исходном порядке. workers ≥ 1."
            ),
            "starter": "use std::sync::Arc;\nuse std::thread;\n\nfn map_parallel<F>(items: Vec<u64>, workers: usize, f: F) -> Vec<u64>\nwhere\n    F: Fn(u64) -> u64 + Send + Sync + 'static,\n{\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let v: Vec<u64> = (1..=20).collect();\n"
                "    println!(\"{:?}\", map_parallel(v.clone(), 3, |x| x * x));\n"
                "    println!(\"{:?}\", map_parallel(vec![], 4, |x| x + 1));\n"
                "    let offset = 100;\n"
                "    println!(\"{:?}\", map_parallel(vec![1, 2, 3], 10, move |x| x + offset));\n"
                "    let big: Vec<u64> = (0..100_000).collect();\n"
                "    let r = map_parallel(big, 8, |x| x % 7);\n"
                "    println!(\"{} {}\", r.len(), r.iter().sum::<u64>());\n"
                "}\n"
            ),
            "expected": ["[1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, 324, 361, 400]", "[]", "[101, 102, 103]", "100000 299995"],
            "hint": "Порядок сохраняется, если потоки получают последовательные куски, а результаты склеиваются в порядке join.",
        },
        {
            "id": "rs10-ping-pong",
            "mode": "rust",
            "title": "Пинг-понг между потоками",
            "statement": (
                "Напишите ping_pong(rounds: u32) -> Vec<String>: два потока "
                "обмениваются сообщениями через два канала; результат — список "
                "строк \"ping 0\", \"pong 0\", \"ping 1\", \"pong 1\", … в точном порядке "
                "(по rounds раундов)."
            ),
            "starter": "use std::sync::mpsc;\nuse std::thread;\n\nfn ping_pong(rounds: u32) -> Vec<String> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", ping_pong(3));\n"
                "    println!(\"{:?}\", ping_pong(0));\n"
                "    println!(\"{}\", ping_pong(1000).len());\n"
                "}\n"
            ),
            "expected": ["[\"ping 0\", \"pong 0\", \"ping 1\", \"pong 1\", \"ping 2\", \"pong 2\"]", "[]", "2000"],
            "hint": "Основной поток играет роль «ping»: отправил число, дождался ответа recv(), записал — и следующий раунд.",
        },
        {
            "id": "rs10-bounded-queue",
            "mode": "rust",
            "title": "Ограниченная очередь на Condvar",
            "statement": (
                "Реализуйте BoundedQueue<T> (Mutex<VecDeque<T>> + две Condvar): "
                "new(cap), push(&self, T) блокируется, пока очередь полна, "
                "pop(&self) -> T блокируется, пока пуста. Все методы — &self, чтобы "
                "очередь можно было разделить через Arc."
            ),
            "starter": "use std::collections::VecDeque;\nuse std::sync::{Condvar, Mutex};\n\nstruct BoundedQueue<T> {\n    items: Mutex<VecDeque<T>>,\n    not_full: Condvar,\n    not_empty: Condvar,\n    cap: usize,\n}\n\nimpl<T> BoundedQueue<T> {\n    fn new(cap: usize) -> BoundedQueue<T> {\n        todo!()\n    }\n    fn push(&self, x: T) {\n        todo!()\n    }\n    fn pop(&self) -> T {\n        todo!()\n    }\n}\n",
            "driver": (
                "use std::sync::Arc;\n"
                "use std::thread;\n"
                "\n"
                "fn main() {\n"
                "    let q = Arc::new(BoundedQueue::new(3));\n"
                "    let producer = {\n"
                "        let q = Arc::clone(&q);\n"
                "        thread::spawn(move || {\n"
                "            for i in 1..=1000u64 {\n"
                "                q.push(i);\n"
                "            }\n"
                "        })\n"
                "    };\n"
                "    let consumer = {\n"
                "        let q = Arc::clone(&q);\n"
                "        thread::spawn(move || {\n"
                "            let mut sum = 0;\n"
                "            let mut in_order = true;\n"
                "            let mut prev = 0;\n"
                "            for _ in 0..1000 {\n"
                "                let x = q.pop();\n"
                "                in_order &= x == prev + 1;\n"
                "                prev = x;\n"
                "                sum += x;\n"
                "            }\n"
                "            (sum, in_order)\n"
                "        })\n"
                "    };\n"
                "    producer.join().unwrap();\n"
                "    println!(\"{:?}\", consumer.join().unwrap());\n"
                "}\n"
            ),
            "expected": ["(500500, true)"],
            "hint": "wait(guard) отпускает мьютекс и возвращает защитник при пробуждении — всегда в цикле while/loop.",
        },
    ],
}
