"""Задачи книги «Изучаем Rust»: главы 1–5."""

TASKS: dict[int, list[dict]] = {
    1: [
        {
            "id": "rs-fizzbuzz",
            "mode": "rust",
            "title": "FizzBuzz",
            "statement": (
                "Напишите функцию fizzbuzz(n: u32) -> String: 'FizzBuzz', если n "
                "делится на 15, 'Fizz' — на 3, 'Buzz' — на 5, иначе само число "
                "строкой. Код ученика дополняется скрытой функцией main."
            ),
            "starter": "fn fizzbuzz(n: u32) -> String {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let line: Vec<String> = (1..=15).map(fizzbuzz).collect();\n"
                "    println!(\"{}\", line.join(\" \"));\n"
                "    println!(\"{} {}\", fizzbuzz(30), fizzbuzz(97));\n"
                "}\n"
            ),
            "expected": ["1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz", "FizzBuzz 97"],
            "hint": "if / else if / else — выражение: последняя строка каждой ветки без точки с запятой и есть результат.",
        },
        {
            "id": "rs-celsius",
            "mode": "rust",
            "title": "Градусы Цельсия и Фаренгейта",
            "statement": (
                "Напишите функцию to_fahrenheit(c: f64) -> f64 по формуле c · 9 / 5 "
                "+ 32 и to_celsius(f: f64) -> f64 (обратную). Вывод в проверке — с "
                "одним знаком после запятой."
            ),
            "starter": "fn to_fahrenheit(c: f64) -> f64 {\n    todo!()\n}\n\nfn to_celsius(f: f64) -> f64 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for c in [-40.0, 0.0, 36.6, 100.0] {\n"
                "        println!(\"{:.1} -> {:.1}\", c, to_fahrenheit(c));\n"
                "    }\n"
                "    println!(\"{:.1}\", to_celsius(212.0));\n"
                "    println!(\"{:.1}\", to_celsius(to_fahrenheit(21.5)));\n"
                "}\n"
            ),
            "expected": ["-40.0 -> -40.0", "0.0 -> 32.0", "36.6 -> 97.9", "100.0 -> 212.0", "100.0", "21.5"],
            "hint": "Числа с плавающей точкой пишутся с точкой: 9.0 / 5.0; целые и дробные в Rust не смешиваются.",
        },
        {
            "id": "rs-factorial",
            "mode": "rust",
            "title": "Факториал в цикле",
            "statement": (
                "Напишите функцию factorial(n: u64) -> u64 с циклом (0! = 1). "
                "Рекурсию не используйте."
            ),
            "starter": "fn factorial(n: u64) -> u64 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for n in [0, 1, 5, 10, 20] {\n"
                "        println!(\"{}! = {}\", n, factorial(n));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["0! = 1", "1! = 1", "5! = 120", "10! = 3628800", "20! = 2432902008176640000"],
            "hint": "let mut result = 1; for i in 2..=n { result *= i; } result",
        },
        {
            "id": "rs-is-prime",
            "mode": "rust",
            "title": "Простое число",
            "statement": (
                "Напишите функцию is_prime(n: u32) -> bool: true для простых (0 и 1 "
                "не простые). Проверка подаёт числа до миллиона."
            ),
            "starter": "fn is_prime(n: u32) -> bool {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let primes: Vec<u32> = (0..30).filter(|&n| is_prime(n)).collect();\n"
                "    println!(\"{:?}\", primes);\n"
                "    println!(\"{} {} {}\", is_prime(97), is_prime(1_000_003), is_prime(999_999));\n"
                "    let count = (0..200_000).filter(|&n| is_prime(n)).count();\n"
                "    println!(\"{}\", count);\n"
                "}\n"
            ),
            "expected": ["[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]", "true true false", "17984"],
            "hint": "Достаточно проверить делители d, пока d·d ≤ n.",
        },
        {
            "id": "rs-digit-sum",
            "mode": "rust",
            "title": "Сумма цифр",
            "statement": (
                "Напишите функцию digit_sum(n: u64) -> u32: сумма десятичных цифр "
                "числа."
            ),
            "starter": "fn digit_sum(n: u64) -> u32 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for n in [0, 7, 123, 99999, 18446744073709551615] {\n"
                "        println!(\"{} -> {}\", n, digit_sum(n));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["0 -> 0", "7 -> 7", "123 -> 6", "99999 -> 45", "18446744073709551615 -> 87"],
            "hint": "Остаток от деления на 10 — последняя цифра; приведение типов — через as.",
        },
        {
            "id": "rs-collatz",
            "mode": "rust",
            "title": "Гипотеза Коллатца",
            "statement": (
                "Напишите функцию collatz_steps(n: u64) -> u32: сколько шагов "
                "нужно, чтобы из n получить 1, если чётное делится на 2, а нечётное "
                "заменяется на 3n + 1 (для 1 — 0 шагов)."
            ),
            "starter": "fn collatz_steps(n: u64) -> u32 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for n in [1, 2, 3, 6, 27, 97, 871] {\n"
                "        println!(\"{} -> {}\", n, collatz_steps(n));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["1 -> 0", "2 -> 1", "3 -> 7", "6 -> 8", "27 -> 111", "97 -> 118", "871 -> 178"],
            "hint": "if — выражение, его можно присвоить: n = if n % 2 == 0 { n / 2 } else { 3 * n + 1 };",
        },
        {
            "id": "rs-sign",
            "mode": "rust",
            "title": "Знак числа",
            "statement": (
                "Напишите функцию sign(n: i32) -> &'static str: 'negative', 'zero' "
                "или 'positive'. Без return и без mut."
            ),
            "starter": "fn sign(n: i32) -> &'static str {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for n in [-5, 0, 42, i32::MIN, i32::MAX] {\n"
                "        println!(\"{} {}\", n, sign(n));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["-5 negative", "0 zero", "42 positive", "-2147483648 negative", "2147483647 positive"],
            "hint": "Каждая ветка if возвращает строковый литерал — без точки с запятой.",
        },
        {
            "id": "rs-gcd",
            "mode": "rust",
            "title": "Наибольший общий делитель",
            "statement": (
                "Напишите функцию gcd(a: u64, b: u64) -> u64 по алгоритму Евклида "
                "(gcd(a, 0) = a)."
            ),
            "starter": "fn gcd(a: u64, b: u64) -> u64 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for (a, b) in [(12, 18), (17, 5), (0, 9), (9, 0), (1_000_000_007, 998_244_353), (48, 180)] {\n"
                "        println!(\"gcd({}, {}) = {}\", a, b, gcd(a, b));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["gcd(12, 18) = 6", "gcd(17, 5) = 1", "gcd(0, 9) = 9", "gcd(9, 0) = 9", "gcd(1000000007, 998244353) = 1", "gcd(48, 180) = 12"],
            "hint": "Пока b != 0: (a, b) = (b, a % b).",
        },
    ],
    2: [
        {
            "id": "rs-own-return",
            "mode": "rust",
            "title": "Передать владение и вернуть его",
            "statement": (
                "Напишите функцию shout(s: String) -> String, которая забирает "
                "строку во владение, дописывает в конец '!' и возвращает её. "
                "Копировать (clone) нельзя."
            ),
            "starter": "fn shout(s: String) -> String {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let a = String::from(\"hello\");\n"
                "    let a = shout(a);\n"
                "    let b = shout(shout(String::new()));\n"
                "    println!(\"{} [{}]\", a, b);\n"
                "}\n"
            ),
            "expected": ["hello! [!!]"],
            "hint": "Параметр можно объявить изменяемым: fn shout(mut s: String). Вернуть строку — просто выражение s без точки с запятой.",
        },
        {
            "id": "rs-borrow-count",
            "mode": "rust",
            "title": "Заимствование для чтения",
            "statement": (
                "Напишите функцию count_vowels(s: &str) -> usize: число гласных "
                "латинских букв a, e, i, o, u (в любом регистре)."
            ),
            "starter": "fn count_vowels(s: &str) -> usize {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let owned = String::from(\"Ownership And Borrowing\");\n"
                "    println!(\"{}\", count_vowels(&owned));\n"
                "    println!(\"{}\", count_vowels(\"rhythm\"));\n"
                "    println!(\"{} {}\", count_vowels(\"\"), count_vowels(\"AEIOU aeiou\"));\n"
                "    println!(\"{}\", owned);\n"
                "}\n"
            ),
            "expected": ["7", "0", "0 10", "Ownership And Borrowing"],
            "hint": "&str принимает и &String, и литерал; chars() перебирает символы.",
        },
        {
            "id": "rs-mut-borrow",
            "mode": "rust",
            "title": "Изменяемое заимствование",
            "statement": (
                "Напишите функцию make_title(s: &mut String): первая буква "
                "становится заглавной, остальные — строчными (только латиница; "
                "пустая строка не меняется)."
            ),
            "starter": "fn make_title(s: &mut String) {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let mut a = String::from(\"hELLO wORLD\");\n"
                "    make_title(&mut a);\n"
                "    let mut b = String::new();\n"
                "    make_title(&mut b);\n"
                "    let mut c = String::from(\"x\");\n"
                "    make_title(&mut c);\n"
                "    println!(\"{} [{}] {}\", a, b, c);\n"
                "}\n"
            ),
            "expected": ["Hello world [] X"],
            "hint": "Через &mut String можно присвоить новое значение: *s = new_string.",
        },
        {
            "id": "rs-first-word",
            "mode": "rust",
            "title": "Срез: первое слово",
            "statement": (
                "Напишите функцию first_word(s: &str) -> &str: часть строки до "
                "первого пробела (вся строка, если пробелов нет). Без выделения "
                "памяти."
            ),
            "starter": "fn first_word(s: &str) -> &str {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let text = String::from(\"hello brave new world\");\n"
                "    println!(\"[{}]\", first_word(&text));\n"
                "    println!(\"[{}] [{}] [{}]\", first_word(\"single\"), first_word(\"\"), first_word(\"a b\"));\n"
                "    println!(\"[{}]\", first_word(\"привет мир\"));\n"
                "}\n"
            ),
            "expected": ["[hello]", "[single] [] [a]", "[привет]"],
            "hint": "s.find(' ') возвращает Option<usize>; срез — &s[..i].",
        },
        {
            "id": "rs-move-tuple",
            "mode": "rust",
            "title": "Перемещение внутри кортежа",
            "statement": (
                "Напишите функцию swap(pair: (String, String)) -> (String, String), "
                "меняющую элементы местами без clone."
            ),
            "starter": "fn swap(pair: (String, String)) -> (String, String) {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let p = (String::from(\"left\"), String::from(\"right\"));\n"
                "    let q = swap(p);\n"
                "    println!(\"{} {}\", q.0, q.1);\n"
                "    let r = swap(swap(q));\n"
                "    println!(\"{} {}\", r.0, r.1);\n"
                "}\n"
            ),
            "expected": ["right left", "right left"],
            "hint": "Деструктуризация let (a, b) = pair; перемещает оба поля.",
        },
        {
            "id": "rs-slice-stats",
            "mode": "rust",
            "title": "Срезы векторов",
            "statement": (
                "Напишите функции sum(v: &[i32]) -> i64 и largest(v: &[i32]) -> i32 "
                "(вектор не пуст). Они должны принимать и &Vec<i32>, и часть "
                "массива."
            ),
            "starter": "fn sum(v: &[i32]) -> i64 {\n    todo!()\n}\n\nfn largest(v: &[i32]) -> i32 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let v = vec![3, -1, 9, 4, 9, 0];\n"
                "    println!(\"{} {}\", sum(&v), largest(&v));\n"
                "    println!(\"{} {}\", sum(&v[1..4]), largest(&v[1..4]));\n"
                "    let a = [i32::MAX, i32::MAX];\n"
                "    println!(\"{} {}\", sum(&a), largest(&a));\n"
                "}\n"
            ),
            "expected": ["24 9", "12 9", "4294967294 2147483647"],
            "hint": "Сумму накапливайте в i64, чтобы не переполниться; for &x in v берёт копии чисел.",
        },
        {
            "id": "rs-reverse-slice",
            "mode": "rust",
            "title": "Разворот на месте",
            "statement": (
                "Напишите функцию reverse_in_place(v: &mut [i32]): переверните срез "
                "на месте попарной перестановкой, без метода reverse и без нового "
                "вектора."
            ),
            "starter": "fn reverse_in_place(v: &mut [i32]) {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let mut a = vec![1, 2, 3, 4, 5];\n"
                "    reverse_in_place(&mut a);\n"
                "    println!(\"{:?}\", a);\n"
                "    reverse_in_place(&mut a[1..4]);\n"
                "    println!(\"{:?}\", a);\n"
                "    let mut e: Vec<i32> = Vec::new();\n"
                "    reverse_in_place(&mut e);\n"
                "    println!(\"{:?}\", e);\n"
                "}\n"
            ),
            "expected": ["[5, 4, 3, 2, 1]", "[5, 2, 3, 4, 1]", "[]"],
            "hint": "v.swap(i, j) меняет два элемента; идти нужно до середины.",
        },
        {
            "id": "rs-append-all",
            "mode": "rust",
            "title": "Две ссылки на разные данные",
            "statement": (
                "Напишите функцию append_all(dest: &mut Vec<i32>, src: &[i32]): "
                "допишите в dest все элементы src, умноженные на 2."
            ),
            "starter": "fn append_all(dest: &mut Vec<i32>, src: &[i32]) {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let mut a = vec![1];\n"
                "    let b = vec![10, 20, 30];\n"
                "    append_all(&mut a, &b);\n"
                "    println!(\"{:?} {:?}\", a, b);\n"
                "    append_all(&mut a, &[]);\n"
                "    println!(\"{:?}\", a);\n"
                "}\n"
            ),
            "expected": ["[1, 20, 40, 60] [10, 20, 30]", "[1, 20, 40, 60]"],
            "hint": "Одна изменяемая ссылка и одна неизменяемая на РАЗНЫЕ данные — это допустимо.",
        },
    ],
    3: [
        {
            "id": "rs-struct-rect",
            "mode": "rust",
            "title": "Структура с методами",
            "statement": (
                "Дополните impl Rectangle: ассоциированная функция new(w: u32, h: "
                "u32) -> Rectangle, метод area(&self) -> u32, perimeter(&self) -> "
                "u32, is_square(&self) -> bool и can_hold(&self, other: &Rectangle) "
                "-> bool (other помещается целиком — обе стороны строго меньше)."
            ),
            "starter": "struct Rectangle {\n    w: u32,\n    h: u32,\n}\n\nimpl Rectangle {\n    fn new(w: u32, h: u32) -> Rectangle {\n        todo!()\n    }\n    fn area(&self) -> u32 {\n        todo!()\n    }\n    fn perimeter(&self) -> u32 {\n        todo!()\n    }\n    fn is_square(&self) -> bool {\n        todo!()\n    }\n    fn can_hold(&self, other: &Rectangle) -> bool {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let big = Rectangle::new(10, 8);\n"
                "    let small = Rectangle::new(4, 4);\n"
                "    println!(\"{} {} {}\", big.area(), big.perimeter(), big.is_square());\n"
                "    println!(\"{} {}\", small.is_square(), big.can_hold(&small));\n"
                "    println!(\"{}\", small.can_hold(&big));\n"
                "    println!(\"{}\", big.can_hold(&Rectangle::new(10, 1)));\n"
                "}\n"
            ),
            "expected": ["80 36 false", "true true", "false", "false"],
            "hint": "Rectangle { w, h } — сокращённая запись, когда имена параметров совпадают с полями.",
        },
        {
            "id": "rs-enum-shape",
            "mode": "rust",
            "title": "Перечисление с данными",
            "statement": (
                "Опишите метод area(&self) -> f64 для enum Shape: Circle(радиус) — "
                "π r² (std::f64::consts::PI), Rect(a, b) — a·b, Triangle(a, b, c) — "
                "по формуле Герона."
            ),
            "starter": "enum Shape {\n    Circle(f64),\n    Rect(f64, f64),\n    Triangle(f64, f64, f64),\n}\n\nimpl Shape {\n    fn area(&self) -> f64 {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let shapes = vec![Shape::Circle(1.0), Shape::Rect(3.0, 4.5), Shape::Triangle(3.0, 4.0, 5.0), Shape::Circle(0.0)];\n"
                "    for s in &shapes {\n"
                "        println!(\"{:.3}\", s.area());\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["3.142", "13.500", "6.000", "0.000"],
            "hint": "match self { Shape::Circle(r) => ..., ... } — ссылки на поля приходят автоматически.",
        },
        {
            "id": "rs-parse-command",
            "mode": "rust",
            "title": "Разбор команды в Option",
            "statement": (
                "Опишите parse(line: &str) -> Option<Command>: 'go north' → "
                "Go(\"north\".to_string()), 'take lamp' → Take(\"lamp\".to_string()), "
                "'look' → Look, 'quit' → Quit; любая другая строка (в том числе "
                "'go' без аргумента) — None. Слова разделены одним пробелом."
            ),
            "starter": "#[derive(Debug, PartialEq)]\nenum Command {\n    Go(String),\n    Take(String),\n    Look,\n    Quit,\n}\n\nfn parse(line: &str) -> Option<Command> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for line in [\"go north\", \"take lamp\", \"look\", \"quit\", \"go\", \"dance\", \"\", \"take a b\"] {\n"
                "        println!(\"{:?} -> {:?}\", line, parse(line));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["\"go north\" -> Some(Go(\"north\"))", "\"take lamp\" -> Some(Take(\"lamp\"))", "\"look\" -> Some(Look)", "\"quit\" -> Some(Quit)", "\"go\" -> None", "\"dance\" -> None", "\"\" -> None", "\"take a b\" -> None"],
            "hint": "Срез-образец: match parts.as_slice() { [\"go\", dir] => ..., _ => None }.",
        },
        {
            "id": "rs-checked-div",
            "mode": "rust",
            "title": "Option вместо исключения",
            "statement": (
                "Напишите checked_div(a: i32, b: i32) -> Option<i32> (None при "
                "делении на ноль и при переполнении i32::MIN / -1) и average(v: "
                "&[i32]) -> Option<f64> (None для пустого среза)."
            ),
            "starter": "fn checked_div(a: i32, b: i32) -> Option<i32> {\n    todo!()\n}\n\nfn average(v: &[i32]) -> Option<f64> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?} {:?} {:?}\", checked_div(7, 2), checked_div(7, 0), checked_div(i32::MIN, -1));\n"
                "    println!(\"{:?} {:?}\", average(&[1, 2, 4]), average(&[]));\n"
                "    println!(\"{:?}\", average(&[i32::MAX, i32::MAX]));\n"
                "}\n"
            ),
            "expected": ["Some(3) None None", "Some(2.3333333333333335) None", "Some(2147483647.0)"],
            "hint": "Сумму считайте в i64; Some(x) / None — два варианта Option.",
        },
        {
            "id": "rs-traffic-light",
            "mode": "rust",
            "title": "Автомат светофора",
            "statement": (
                "Опишите методы enum Light { Red, Yellow, Green }: next(&self) -> "
                "Light (Red → Green → Yellow → Red) и seconds(&self) -> u32 (Red "
                "30, Yellow 5, Green 25)."
            ),
            "starter": "#[derive(Debug, Clone, Copy)]\nenum Light {\n    Red,\n    Yellow,\n    Green,\n}\n\nimpl Light {\n    fn next(&self) -> Light {\n        todo!()\n    }\n    fn seconds(&self) -> u32 {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let mut l = Light::Red;\n"
                "    let mut total = 0;\n"
                "    for _ in 0..7 {\n"
                "        println!(\"{:?} {}\", l, l.seconds());\n"
                "        total += l.seconds();\n"
                "        l = l.next();\n"
                "    }\n"
                "    println!(\"{}\", total);\n"
                "}\n"
            ),
            "expected": ["Red 30", "Green 25", "Yellow 5", "Red 30", "Green 25", "Yellow 5", "Red 30", "150"],
            "hint": "match должен покрывать все варианты — компилятор проверит.",
        },
        {
            "id": "rs-counter-struct",
            "mode": "rust",
            "title": "Структура с изменяемым состоянием",
            "statement": (
                "Дополните Counter: new(step: u32), метод tick(&mut self) "
                "увеличивает значение на step, get(&self) -> u32 и reset(&mut self) "
                "обнуляет."
            ),
            "starter": "struct Counter {\n    value: u32,\n    step: u32,\n}\n\nimpl Counter {\n    fn new(step: u32) -> Counter {\n        todo!()\n    }\n    fn tick(&mut self) {\n        todo!()\n    }\n    fn get(&self) -> u32 {\n        todo!()\n    }\n    fn reset(&mut self) {\n        todo!()\n    }\n}\n",
            "driver": (
                "fn main() {\n"
                "    let mut c = Counter::new(5);\n"
                "    for _ in 0..4 {\n"
                "        c.tick();\n"
                "    }\n"
                "    println!(\"{}\", c.get());\n"
                "    c.reset();\n"
                "    c.tick();\n"
                "    println!(\"{}\", c.get());\n"
                "}\n"
            ),
            "expected": ["20", "5"],
            "hint": "Методам, которые меняют состояние, нужен &mut self; вызывающая переменная — mut.",
        },
        {
            "id": "rs-apply-op",
            "mode": "rust",
            "title": "Операции как перечисление",
            "statement": (
                "Напишите apply(op: Op, a: i64, b: i64) -> Option<i64> для enum Op "
                "{ Add, Sub, Mul, Div }: Div при b = 0 даёт None; переполнение не "
                "обрабатывать."
            ),
            "starter": "#[derive(Debug, Clone, Copy)]\nenum Op {\n    Add,\n    Sub,\n    Mul,\n    Div,\n}\n\nfn apply(op: Op, a: i64, b: i64) -> Option<i64> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for op in [Op::Add, Op::Sub, Op::Mul, Op::Div] {\n"
                "        println!(\"{:?}: {:?} {:?}\", op, apply(op, 12, 4), apply(op, 7, 0));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["Add: Some(16) Some(7)", "Sub: Some(8) Some(7)", "Mul: Some(48) Some(0)", "Div: Some(3) None"],
            "hint": "match op { Op::Add => Some(a + b), ... } — каждая ветка возвращает Option.",
        },
        {
            "id": "rs-describe-option",
            "mode": "rust",
            "title": "if let и match по Option",
            "statement": (
                "Напишите describe(n: Option<i32>) -> String: None → \"nothing\", "
                "Some(0) → \"zero\", Some(x) при x < 0 → \"negative x\" (число "
                "подставьте), иначе \"positive x\"."
            ),
            "starter": "fn describe(n: Option<i32>) -> String {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for n in [None, Some(0), Some(-7), Some(42)] {\n"
                "        println!(\"{}\", describe(n));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["nothing", "zero", "negative -7", "positive 42"],
            "hint": "Охранное условие в ветке: Some(x) if x < 0 => ...",
        },
    ],
    4: [
        {
            "id": "rs-dedup-sorted",
            "mode": "rust",
            "title": "Уникальные значения",
            "statement": (
                "Напишите unique_sorted(v: Vec<i32>) -> Vec<i32>: вектор без "
                "повторов, по возрастанию."
            ),
            "starter": "fn unique_sorted(v: Vec<i32>) -> Vec<i32> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", unique_sorted(vec![5, 3, 5, 1, 3, 9, -2, 1]));\n"
                "    println!(\"{:?}\", unique_sorted(vec![]));\n"
                "    println!(\"{:?}\", unique_sorted(vec![7; 5]));\n"
                "}\n"
            ),
            "expected": ["[-2, 1, 3, 5, 9]", "[]", "[7]"],
            "hint": "sort() и dedup() работают на месте; dedup убирает только соседние повторы.",
        },
        {
            "id": "rs-word-count",
            "mode": "rust",
            "title": "Частоты слов",
            "statement": (
                "Напишите word_count(text: &str) -> Vec<(String, usize)>: слова "
                "(разделены пробельными символами, регистр приводится к нижнему) и "
                "сколько раз они встретились; порядок — по убыванию частоты, при "
                "равенстве — по алфавиту."
            ),
            "starter": "use std::collections::HashMap;\n\nfn word_count(text: &str) -> Vec<(String, usize)> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for (w, n) in word_count(\"the cat and The dog and THE bird\") {\n"
                "        println!(\"{} {}\", w, n);\n"
                "    }\n"
                "    println!(\"{}\", word_count(\"\").len());\n"
                "}\n"
            ),
            "expected": ["the 3", "and 2", "bird 1", "cat 1", "dog 1", "0"],
            "hint": "entry(ключ).or_insert(0) возвращает &mut счётчик; сортировка sort_by с .then().",
        },
        {
            "id": "rs-reverse-words",
            "mode": "rust",
            "title": "Слова в обратном порядке",
            "statement": (
                "Напишите reverse_words(s: &str) -> String: слова (по пробельным "
                "символам) в обратном порядке, через один пробел."
            ),
            "starter": "fn reverse_words(s: &str) -> String {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"[{}]\", reverse_words(\"one two  three\"));\n"
                "    println!(\"[{}] [{}]\", reverse_words(\"\"), reverse_words(\"  solo  \"));\n"
                "    println!(\"[{}]\", reverse_words(\"привет, большой мир\"));\n"
                "}\n"
            ),
            "expected": ["[three two one]", "[] [solo]", "[мир большой привет,]"],
            "hint": "split_whitespace() сам пропускает лишние пробелы; join собирает Vec<&str> в строку.",
        },
        {
            "id": "rs-anagram",
            "mode": "rust",
            "title": "Анаграммы",
            "statement": (
                "Напишите is_anagram(a: &str, b: &str) -> bool: состоят ли строки "
                "из одних и тех же букв (регистр не важен, пробелы игнорируются)."
            ),
            "starter": "fn is_anagram(a: &str, b: &str) -> bool {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{} {}\", is_anagram(\"Listen\", \"Silent\"), is_anagram(\"a gentleman\", \"elegant man\"));\n"
                "    println!(\"{} {}\", is_anagram(\"abc\", \"abd\"), is_anagram(\"\", \"\"));\n"
                "    println!(\"{}\", is_anagram(\"Слон\", \"нос л\"));\n"
                "}\n"
            ),
            "expected": ["true true", "false true", "true"],
            "hint": "Отсортированные списки букв равны ⇔ строки — анаграммы.",
        },
        {
            "id": "rs-char-freq",
            "mode": "rust",
            "title": "Частоты символов",
            "statement": (
                "Напишите char_freq(s: &str) -> BTreeMap<char, usize>: сколько раз "
                "каждый символ встречается в строке (без пробелов)."
            ),
            "starter": "use std::collections::BTreeMap;\n\nfn char_freq(s: &str) -> BTreeMap<char, usize> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let m = char_freq(\"hello world\");\n"
                "    let parts: Vec<String> = m.iter().map(|(c, n)| format!(\"{}{}\", c, n)).collect();\n"
                "    println!(\"{}\", parts.join(\" \"));\n"
                "    println!(\"{:?}\", char_freq(\"ёё я\"));\n"
                "    println!(\"{}\", char_freq(\"\").len());\n"
                "}\n"
            ),
            "expected": ["d1 e1 h1 l3 o2 r1 w1", "{'я': 1, 'ё': 2}", "0"],
            "hint": "BTreeMap хранит ключи по порядку — вывод получается стабильным.",
        },
        {
            "id": "rs-group-by-len",
            "mode": "rust",
            "title": "Группировка слов по длине",
            "statement": (
                "Напишите group_by_len(words: &[&str]) -> BTreeMap<usize, "
                "Vec<String>>: длина слова в символах → слова в порядке появления."
            ),
            "starter": "use std::collections::BTreeMap;\n\nfn group_by_len(words: &[&str]) -> BTreeMap<usize, Vec<String>> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    let g = group_by_len(&[\"a\", \"bb\", \"cc\", \"d\", \"эхо\", \"abc\", \"\"]);\n"
                "    for (len, ws) in &g {\n"
                "        println!(\"{} {:?}\", len, ws);\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["0 [\"\"]", "1 [\"a\", \"d\"]", "2 [\"bb\", \"cc\"]", "3 [\"эхо\", \"abc\"]"],
            "hint": "entry(len).or_default() даёт &mut Vec<String> — и сразу push.",
        },
        {
            "id": "rs-two-sum",
            "mode": "rust",
            "title": "Два числа с заданной суммой",
            "statement": (
                "Напишите two_sum(nums: &[i32], target: i32) -> Option<(usize, "
                "usize)>: индексы i < j, для которых nums[i] + nums[j] == target; "
                "если вариантов несколько — с наименьшим j, затем с наименьшим i. "
                "Решение за один проход с HashMap: проверка подаёт 200 000 чисел."
            ),
            "starter": "use std::collections::HashMap;\n\nfn two_sum(nums: &[i32], target: i32) -> Option<(usize, usize)> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", two_sum(&[2, 7, 11, 15], 9));\n"
                "    println!(\"{:?}\", two_sum(&[3, 2, 4], 6));\n"
                "    println!(\"{:?}\", two_sum(&[1, 2, 3], 100));\n"
                "    println!(\"{:?}\", two_sum(&[], 1));\n"
                "    println!(\"{:?}\", two_sum(&[5, 5], 10));\n"
                "    let big: Vec<i32> = (0..200_000).map(|i| i * 3).collect();\n"
                "    println!(\"{:?}\", two_sum(&big, 599_991 + 3));\n"
                "}\n"
            ),
            "expected": ["Some((0, 1))", "Some((1, 2))", "None", "None", "Some((0, 1))", "Some((99998, 100000))"],
            "hint": "Для каждого x спросите словарь: нет ли уже числа target − x; затем запомните x с его индексом.",
        },
        {
            "id": "rs-utf8-len",
            "mode": "rust",
            "title": "Символы и байты",
            "statement": (
                "Напишите sizes(s: &str) -> (usize, usize): число символов и число "
                "байтов строки; и is_ascii_only(s: &str) -> bool."
            ),
            "starter": "fn sizes(s: &str) -> (usize, usize) {\n    todo!()\n}\n\nfn is_ascii_only(s: &str) -> bool {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for s in [\"hello\", \"привет\", \"€5\", \"😀\", \"\"] {\n"
                "        println!(\"{:?} {:?} {}\", s, sizes(s), is_ascii_only(s));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["\"hello\" (5, 5) true", "\"привет\" (6, 12) false", "\"€5\" (2, 4) false", "\"😀\" (1, 4) false", "\"\" (0, 0) true"],
            "hint": "s.len() — байты, s.chars().count() — символы.",
        },
    ],
    5: [
        {
            "id": "rs-parse-age",
            "mode": "rust",
            "title": "Result с текстом ошибки",
            "statement": (
                "Напишите parse_age(s: &str) -> Result<u8, String>: число 0…150 или "
                "ошибка. Тексты ошибок: \"not a number\" (не разобралось как "
                "u8-совместимое целое; пустая строка тоже), \"too old\" (больше 150)."
            ),
            "starter": "fn parse_age(s: &str) -> Result<u8, String> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for s in [\"42\", \" 7 \", \"150\", \"151\", \"abc\", \"\", \"-3\", \"99999999999\"] {\n"
                "        println!(\"{:?} -> {:?}\", s, parse_age(s));\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["\"42\" -> Ok(42)", "\" 7 \" -> Ok(7)", "\"150\" -> Ok(150)", "\"151\" -> Err(\"too old\")", "\"abc\" -> Err(\"not a number\")", "\"\" -> Err(\"not a number\")", "\"-3\" -> Err(\"not a number\")", "\"99999999999\" -> Err(\"not a number\")"],
            "hint": "parse::<u32>() возвращает Result; сопоставьте Ok(n) if n <= 150, Ok(_) и Err(_).",
        },
        {
            "id": "rs-sum-numbers",
            "mode": "rust",
            "title": "Оператор ? и ParseIntError",
            "statement": (
                "Напишите sum_numbers(s: &str) -> Result<i64, "
                "std::num::ParseIntError>: сумма целых чисел, разделённых запятыми "
                "(пробелы вокруг чисел допустимы; пустая строка — сумма 0). Первая "
                "же ошибка разбора возвращается наверх оператором ?."
            ),
            "starter": "fn sum_numbers(s: &str) -> Result<i64, std::num::ParseIntError> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for s in [\"1,2,3\", \" 10 , -4 \", \"\", \"5,x,7\", \"9223372036854775807\"] {\n"
                "        match sum_numbers(s) {\n"
                "            Ok(n) => println!(\"ok {}\", n),\n"
                "            Err(e) => println!(\"err {}\", e),\n"
                "        }\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["ok 6", "ok 6", "ok 0", "err invalid digit found in string", "ok 9223372036854775807"],
            "hint": "part.trim().parse::<i64>()? — вопросительный знак возвращает ошибку из функции или даёт значение.",
        },
        {
            "id": "rs-custom-error",
            "mode": "rust",
            "title": "Свой тип ошибки",
            "statement": (
                "Реализуйте Display для enum ConfigError и функцию parse_line(line: "
                "&str) -> Result<(String, i32), ConfigError>: строка 'ключ=число'. "
                "Нет '=' → ConfigError::MissingEquals; пустой ключ → EmptyKey; "
                "значение не число → BadValue(значение). Display: 'missing =', "
                "'empty key', 'bad value: <значение>'."
            ),
            "starter": "use std::fmt;\n\n#[derive(Debug, PartialEq)]\nenum ConfigError {\n    MissingEquals,\n    EmptyKey,\n    BadValue(String),\n}\n\nimpl fmt::Display for ConfigError {\n    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {\n        todo!()\n    }\n}\n\nfn parse_line(line: &str) -> Result<(String, i32), ConfigError> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    for line in [\"port=8080\", \" retries = 3 \", \"port\", \"=5\", \"port=abc\", \"x=-1\"] {\n"
                "        match parse_line(line) {\n"
                "            Ok((k, v)) => println!(\"ok {} {}\", k, v),\n"
                "            Err(e) => println!(\"err {} ({:?})\", e, e),\n"
                "        }\n"
                "    }\n"
                "}\n"
            ),
            "expected": ["ok port 8080", "ok retries 3", "err missing = (MissingEquals)", "err empty key (EmptyKey)", "err bad value: abc (BadValue(\"abc\"))", "ok x -1"],
            "hint": "split_once('=').ok_or(ConfigError::MissingEquals)? — Option превращается в Result; map_err меняет тип ошибки.",
        },
        {
            "id": "rs-first-even",
            "mode": "rust",
            "title": "Option в Result",
            "statement": (
                "Напишите first_even(v: &[i32]) -> Result<i32, String>: первое "
                "чётное число или Err(\"no even numbers\")."
            ),
            "starter": "fn first_even(v: &[i32]) -> Result<i32, String> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", first_even(&[1, 3, 8, 10]));\n"
                "    println!(\"{:?}\", first_even(&[1, 3, 5]));\n"
                "    println!(\"{:?}\", first_even(&[]));\n"
                "    println!(\"{:?}\", first_even(&[-4]));\n"
                "}\n"
            ),
            "expected": ["Ok(8)", "Err(\"no even numbers\")", "Err(\"no even numbers\")", "Ok(-4)"],
            "hint": "find возвращает Option; ok_or_else превращает None в Err.",
        },
        {
            "id": "rs-math-error",
            "mode": "rust",
            "title": "Ошибки вычислений",
            "statement": (
                "Напишите safe_div(a: f64, b: f64) -> Result<f64, MathError> и "
                "safe_sqrt(x: f64) -> Result<f64, MathError>; enum MathError { "
                "DivideByZero, NegativeSqrt } уже есть."
            ),
            "starter": "#[derive(Debug, PartialEq)]\nenum MathError {\n    DivideByZero,\n    NegativeSqrt,\n}\n\nfn safe_div(a: f64, b: f64) -> Result<f64, MathError> {\n    todo!()\n}\n\nfn safe_sqrt(x: f64) -> Result<f64, MathError> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?} {:?}\", safe_div(9.0, 4.0), safe_div(1.0, 0.0));\n"
                "    println!(\"{:?} {:?}\", safe_sqrt(16.0), safe_sqrt(-1.0));\n"
                "    let r = safe_div(10.0, 4.0).and_then(safe_sqrt);\n"
                "    println!(\"{:?}\", r);\n"
                "}\n"
            ),
            "expected": ["Ok(2.25) Err(DivideByZero)", "Ok(4.0) Err(NegativeSqrt)", "Ok(1.5811388300841898)"],
            "hint": "Err(MathError::DivideByZero) и Ok(значение) — два варианта Result.",
        },
        {
            "id": "rs-from-conversion",
            "mode": "rust",
            "title": "Автоматическое преобразование ошибок",
            "statement": (
                "Реализуйте From<std::num::ParseIntError> для AppError (вариант "
                "Parse(String) — текст ошибки через to_string()) и функцию "
                "add_strs(a: &str, b: &str) -> Result<i32, AppError>: сумма двух "
                "чисел; переполнение i32 даёт AppError::Overflow. В теле должен "
                "использоваться оператор ?."
            ),
            "starter": "#[derive(Debug, PartialEq)]\nenum AppError {\n    Parse(String),\n    Overflow,\n}\n\nimpl From<std::num::ParseIntError> for AppError {\n    fn from(e: std::num::ParseIntError) -> AppError {\n        todo!()\n    }\n}\n\nfn add_strs(a: &str, b: &str) -> Result<i32, AppError> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", add_strs(\"2\", \" 40\"));\n"
                "    println!(\"{:?}\", add_strs(\"x\", \"1\"));\n"
                "    println!(\"{:?}\", add_strs(\"1\", \"\"));\n"
                "    println!(\"{:?}\", add_strs(\"2147483647\", \"1\"));\n"
                "}\n"
            ),
            "expected": ["Ok(42)", "Err(Parse(\"invalid digit found in string\"))", "Err(Parse(\"cannot parse integer from empty string\"))", "Err(Overflow)"],
            "hint": "? вызывает From::from для преобразования типа ошибки; checked_add возвращает Option.",
        },
        {
            "id": "rs-collect-results",
            "mode": "rust",
            "title": "Все или ничего",
            "statement": (
                "Напишите parse_all(items: &[&str]) -> Result<Vec<i32>, String>: "
                "все строки в числа; при первой же ошибке — Err(\"bad item: "
                "<строка>\") (оператор ? или явный return)."
            ),
            "starter": "fn parse_all(items: &[&str]) -> Result<Vec<i32>, String> {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{:?}\", parse_all(&[\"1\", \"2\", \"-3\"]));\n"
                "    println!(\"{:?}\", parse_all(&[\"1\", \"x\", \"y\"]));\n"
                "    println!(\"{:?}\", parse_all(&[]));\n"
                "}\n"
            ),
            "expected": ["Ok([1, 2, -3])", "Err(\"bad item: x\")", "Ok([])"],
            "hint": "map_err(|_| format!(...))? — превратить ошибку в свою строку и вернуть наверх.",
        },
        {
            "id": "rs-parse-or-default",
            "mode": "rust",
            "title": "Запасное значение",
            "statement": (
                "Напишите parse_or(s: &str, default: i32) -> i32 и parse_port(s: "
                "&str) -> u16: если не разобралось (или порт вне 1…65535) — 8080."
            ),
            "starter": "fn parse_or(s: &str, default: i32) -> i32 {\n    todo!()\n}\n\nfn parse_port(s: &str) -> u16 {\n    todo!()\n}\n",
            "driver": (
                "fn main() {\n"
                "    println!(\"{} {} {}\", parse_or(\"12\", 0), parse_or(\"x\", -1), parse_or(\"\", 7));\n"
                "    println!(\"{} {} {} {}\", parse_port(\"443\"), parse_port(\"0\"), parse_port(\"70000\"), parse_port(\"http\"));\n"
                "}\n"
            ),
            "expected": ["12 -1 7", "443 8080 8080 8080"],
            "hint": "unwrap_or(default) — безопасный вариант unwrap; диапазон: (1..=65535).contains(&p).",
        },
    ],
}
