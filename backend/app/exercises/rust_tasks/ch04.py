"""Задачи книги «Изучаем Rust»: глава 4 (код проверяется rustc в песочнице)."""

TASKS: dict[int, list[dict]] = {4: [{'id': 'r4-add',
      'mode': 'rust',
      'title': 'Сумма двух',
      'statement': 'Напишите функцию add, которая принимает два числа i32 и возвращает их сумму.',
      'starter': 'fn add(a: i32, b: i32) -> i32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", add(2, 3));\n'
                '    println!("{}", add(-10, 4));\n'
                '    println!("{}", add(0, 0));\n'
                '}\n',
      'hint': 'Последнее выражение без точки с запятой станет результатом: a + b',
      'expected': ['5', '-6', '0']},
     {'id': 'r4-square',
      'mode': 'rust',
      'title': 'Квадрат числа',
      'statement': 'Напишите функцию square(x: i32) -> i32, возвращающую квадрат числа.',
      'starter': 'fn square(x: i32) -> i32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", square(7));\n'
                '    println!("{}", square(-3));\n'
                '    println!("{}", square(0));\n'
                '}\n',
      'hint': 'x * x — без return и без точки с запятой.',
      'expected': ['49', '9', '0']},
     {'id': 'r4-is-even',
      'mode': 'rust',
      'title': 'Чётное число',
      'statement': 'Напишите функцию is_even(n: i32) -> bool: true для чётных чисел, включая отрицательные и '
                   'ноль.',
      'starter': 'fn is_even(n: i32) -> bool {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for n in [4, 7, 0, -2, -3] {\n'
                '        println!("{} {}", n, is_even(n));\n'
                '    }\n'
                '}\n',
      'hint': 'Остаток от деления на 2 равен нулю. Для отрицательных n % 2 тоже -1 или 0: сравнение с 0 '
              'подходит.',
      'expected': ['4 true', '7 false', '0 true', '-2 true', '-3 false']},
     {'id': 'r4-max-of-two',
      'mode': 'rust',
      'title': 'Большее из двух',
      'statement': 'Напишите функцию max_of_two(a, b), возвращающую большее из двух i32. Используйте if–else '
                   'как выражение.',
      'starter': 'fn max_of_two(a: i32, b: i32) -> i32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", max_of_two(3, 9));\n'
                '    println!("{}", max_of_two(9, 3));\n'
                '    println!("{}", max_of_two(-5, -5));\n'
                '    println!("{}", max_of_two(-1, -8));\n'
                '}\n',
      'hint': 'if a > b { a } else { b } — блок с выражениями без точек с запятой.',
      'expected': ['9', '9', '-5', '-1']},
     {'id': 'r4-abs-diff',
      'mode': 'rust',
      'title': 'Разность по модулю',
      'statement': 'Напишите функцию abs_diff(a, b): расстояние между числами |a − b| для i32. Не '
                   'используйте готовый метод — только if–else и вычитание.',
      'starter': 'fn abs_diff(a: i32, b: i32) -> i32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", abs_diff(10, 3));\n'
                '    println!("{}", abs_diff(3, 10));\n'
                '    println!("{}", abs_diff(-4, 6));\n'
                '    println!("{}", abs_diff(5, 5));\n'
                '}\n',
      'hint': 'Из большего вычтите меньшее.',
      'expected': ['7', '7', '10', '0']},
     {'id': 'r4-area-rect',
      'mode': 'rust',
      'title': 'Площадь и периметр',
      'statement': 'Напишите две функции для прямоугольника с целыми сторонами: area(w, h) — площадь и '
                   'perimeter(w, h) — периметр.',
      'starter': 'fn area(w: i32, h: i32) -> i32 {\n'
                 '    todo!()\n'
                 '}\n'
                 '\n'
                 'fn perimeter(w: i32, h: i32) -> i32 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", area(4, 5));\n'
                '    println!("{}", perimeter(4, 5));\n'
                '    println!("{}", area(10, 10));\n'
                '    println!("{}", perimeter(1, 1));\n'
                '}\n',
      'hint': 'area: w * h; perimeter: 2 * (w + h).',
      'expected': ['20', '18', '100', '4']},
     {'id': 'r4-c-to-f',
      'mode': 'rust',
      'title': 'Цельсий в Фаренгейт',
      'statement': 'Напишите функцию c_to_f(c: f64) -> f64: градусы Цельсия в Фаренгейты по формуле c · 9 / '
                   '5 + 32.',
      'starter': 'fn c_to_f(c: f64) -> f64 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:.1}", c_to_f(0.0));\n'
                '    println!("{:.1}", c_to_f(100.0));\n'
                '    println!("{:.1}", c_to_f(-40.0));\n'
                '    println!("{:.1}", c_to_f(36.6));\n'
                '}\n',
      'hint': 'Числа в формуле — дробные литералы: 9.0, 5.0, 32.0.',
      'expected': ['32.0', '212.0', '-40.0', '97.9']},
     {'id': 'r4-greet',
      'mode': 'rust',
      'title': 'Приветствие',
      'statement': 'Напишите функцию greet(name: &str) -> String, возвращающую строку «Привет, <имя>!». '
                   'Используйте макрос format!.',
      'starter': 'fn greet(name: &str) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n    println!("{}", greet("Аня"));\n    println!("{}", greet("мир"));\n}\n',
      'hint': 'format!("Привет, {}!", name) возвращает String, а не печатает.',
      'expected': ['Привет, Аня!', 'Привет, мир!']},
     {'id': 'r4-divmod',
      'mode': 'rust',
      'title': 'Частное и остаток',
      'statement': 'Напишите функцию divmod(a, b) -> (i32, i32): частное и остаток от деления a на b (b > 0, '
                   'a ≥ 0).',
      'starter': 'fn divmod(a: i32, b: i32) -> (i32, i32) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let (q, r) = divmod(17, 5);\n'
                '    println!("{} {}", q, r);\n'
                '    let p = divmod(9, 3);\n'
                '    println!("{} {}", p.0, p.1);\n'
                '}\n',
      'hint': 'Верните кортеж (a / b, a % b).',
      'expected': ['3 2', '3 0']},
     {'id': 'r4-min-max3',
      'mode': 'rust',
      'title': 'Наименьшее и наибольшее',
      'statement': 'Напишите функцию min_max(a, b, c) -> (i32, i32): наименьшее и наибольшее из трёх чисел. '
                   'Можно пользоваться методами a.min(b) и a.max(b).',
      'starter': 'fn min_max(a: i32, b: i32, c: i32) -> (i32, i32) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", min_max(3, 9, 1));\n'
                '    println!("{:?}", min_max(-5, -2, -9));\n'
                '    println!("{:?}", min_max(7, 7, 7));\n'
                '}\n',
      'hint': 'a.min(b).min(c) и a.max(b).max(c)',
      'expected': ['(1, 9)', '(-9, -2)', '(7, 7)']},
     {'id': 'r4-sign',
      'mode': 'rust',
      'title': 'Знак числа',
      'statement': 'Напишите функцию sign(n: i32) -> i32: 1 для положительных, -1 для отрицательных, 0 для '
                   'нуля. Одним выражением if – else if – else.',
      'starter': 'fn sign(n: i32) -> i32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for n in [5, -3, 0, 100, -100] {\n'
                '        println!("{}", sign(n));\n'
                '    }\n'
                '}\n',
      'hint': 'Цепочка if … else if … else — одно выражение; все ветки i32.',
      'expected': ['1', '-1', '0', '1', '-1']},
     {'id': 'r4-clamp',
      'mode': 'rust',
      'title': 'Зажать в диапазон',
      'statement': 'Напишите функцию clamp(x, lo, hi): если x меньше lo — вернуть lo, если больше hi — hi, '
                   'иначе x. Используйте ранний return.',
      'starter': 'fn clamp(x: i32, lo: i32, hi: i32) -> i32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", clamp(5, 0, 10));\n'
                '    println!("{}", clamp(-5, 0, 10));\n'
                '    println!("{}", clamp(50, 0, 10));\n'
                '    println!("{}", clamp(0, 0, 10));\n'
                '}\n',
      'hint': 'Два раннего return, затем x — итоговое выражение.',
      'expected': ['5', '0', '10', '0']},
     {'id': 'r4-factorial',
      'mode': 'rust',
      'title': 'Факториал',
      'statement': 'Напишите функцию fact(n: u64) -> u64: факториал n! (0! = 1). Решите рекурсией.',
      'starter': 'fn fact(n: u64) -> u64 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n    for n in [0, 1, 5, 10, 20] {\n        println!("{}", fact(n));\n    }\n}\n',
      'hint': 'База: n ≤ 1 → 1. Шаг: n * fact(n - 1).',
      'expected': ['1', '1', '120', '3628800', '2432902008176640000']},
     {'id': 'r4-fib',
      'mode': 'rust',
      'title': 'Числа Фибоначчи',
      'statement': 'Напишите функцию fib(n: u32) -> u64 рекурсией: fib(0) = 0, fib(1) = 1, fib(n) = fib(n−1) '
                   '+ fib(n−2).',
      'starter': 'fn fib(n: u32) -> u64 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for n in 0..=10 {\n'
                '        print!("{} ", fib(n));\n'
                '    }\n'
                '    println!();\n'
                '    println!("{}", fib(25));\n'
                '}\n',
      'hint': 'Для n < 2 результат равен самому n; приведите его к u64 через as.',
      'expected': ['0 1 1 2 3 5 8 13 21 34 55', '75025']},
     {'id': 'r4-gcd',
      'mode': 'rust',
      'title': 'НОД рекурсией',
      'statement': 'Напишите функцию gcd(a: u32, b: u32) -> u32 — наибольший общий делитель алгоритмом '
                   'Евклида: gcd(a, 0) = a, иначе gcd(b, a % b).',
      'starter': 'fn gcd(a: u32, b: u32) -> u32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", gcd(48, 18));\n'
                '    println!("{}", gcd(17, 5));\n'
                '    println!("{}", gcd(100, 0));\n'
                '    println!("{}", gcd(1_000_000_007, 998_244_353));\n'
                '}\n',
      'hint': 'Рекурсия сокращает пару (a, b) до (b, a % b), пока b не станет нулём.',
      'expected': ['6', '1', '100', '1']},
     {'id': 'r4-power',
      'mode': 'rust',
      'title': 'Возведение в степень',
      'statement': 'Напишите функцию power(base: i64, exp: u32) -> i64 рекурсией, без pow: power(x, 0) = 1, '
                   'power(x, n) = x · power(x, n−1).',
      'starter': 'fn power(base: i64, exp: u32) -> i64 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", power(2, 10));\n'
                '    println!("{}", power(3, 4));\n'
                '    println!("{}", power(-2, 3));\n'
                '    println!("{}", power(7, 0));\n'
                '}\n',
      'hint': 'База: exp == 0 → 1.',
      'expected': ['1024', '81', '-8', '1']},
     {'id': 'r4-sum-to',
      'mode': 'rust',
      'title': 'Сумма до n',
      'statement': 'Напишите функцию sum_to(n: u32) -> u32 рекурсией: 1 + 2 + … + n (sum_to(0) = 0).',
      'starter': 'fn sum_to(n: u32) -> u32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", sum_to(0));\n'
                '    println!("{}", sum_to(5));\n'
                '    println!("{}", sum_to(100));\n'
                '}\n',
      'hint': 'n + sum_to(n - 1)',
      'expected': ['0', '15', '5050']},
     {'id': 'r4-leap',
      'mode': 'rust',
      'title': 'Високосный год',
      'statement': 'Напишите функцию is_leap(year: u32) -> bool: год високосный, если делится на 4, кроме '
                   'годов, делящихся на 100, но не на 400.',
      'starter': 'fn is_leap(year: u32) -> bool {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for y in [2000, 1900, 2024, 2023, 2100, 1600] {\n'
                '        println!("{} {}", y, is_leap(y));\n'
                '    }\n'
                '}\n',
      'hint': 'Условие целиком — одно логическое выражение с &&, ||.',
      'expected': ['2000 true', '1900 false', '2024 true', '2023 false', '2100 false', '1600 true']},
     {'id': 'r4-between',
      'mode': 'rust',
      'title': 'Попадает в диапазон',
      'statement': 'Напишите функцию in_range(x, lo, hi) -> bool: true, если lo ≤ x ≤ hi (границы входят).',
      'starter': 'fn in_range(x: i32, lo: i32, hi: i32) -> bool {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", in_range(5, 1, 10));\n'
                '    println!("{}", in_range(1, 1, 10));\n'
                '    println!("{}", in_range(10, 1, 10));\n'
                '    println!("{}", in_range(11, 1, 10));\n'
                '    println!("{}", in_range(0, 1, 10));\n'
                '}\n',
      'hint': 'x >= lo && x <= hi',
      'expected': ['true', 'true', 'true', 'false', 'false']},
     {'id': 'r4-swap',
      'mode': 'rust',
      'title': 'Поменять местами',
      'statement': 'Напишите функцию swap(p: (i32, i32)) -> (i32, i32), возвращающую пару с переставленными '
                   'элементами.',
      'starter': 'fn swap(p: (i32, i32)) -> (i32, i32) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{:?}", swap((1, 2)));\n'
                '    println!("{:?}", swap((-5, 100)));\n'
                '}\n',
      'hint': 'Доступ по номеру: p.0 и p.1; вернуть новый кортеж.',
      'expected': ['(2, 1)', '(100, -5)']},
     {'id': 'r4-stats',
      'mode': 'rust',
      'title': 'Сумма и среднее',
      'statement': 'Напишите функцию stats(a, b, c) -> (i32, f64): сумма трёх чисел и их среднее '
                   'арифметическое (как f64).',
      'starter': 'fn stats(a: i32, b: i32, c: i32) -> (i32, f64) {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    let (s, avg) = stats(4, 7, 10);\n'
                '    println!("{} {:.2}", s, avg);\n'
                '    let (s, avg) = stats(1, 2, 2);\n'
                '    println!("{} {:.2}", s, avg);\n'
                '}\n',
      'hint': 'Сначала sum, затем кортеж (sum, sum as f64 / 3.0).',
      'expected': ['21 7.00', '5 1.67']},
     {'id': 'r4-digit-sum',
      'mode': 'rust',
      'title': 'Сумма цифр',
      'statement': 'Напишите функцию digit_sum(n: u32) -> u32 рекурсией: сумма десятичных цифр числа. '
                   'digit_sum(0) = 0, иначе n % 10 + digit_sum(n / 10).',
      'starter': 'fn digit_sum(n: u32) -> u32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", digit_sum(0));\n'
                '    println!("{}", digit_sum(123));\n'
                '    println!("{}", digit_sum(99999));\n'
                '    println!("{}", digit_sum(4_000_000_000));\n'
                '}\n',
      'hint': 'Последняя цифра — n % 10, остальные — n / 10.',
      'expected': ['0', '6', '45', '4']},
     {'id': 'r4-count-digits',
      'mode': 'rust',
      'title': 'Количество цифр',
      'statement': 'Напишите функцию count_digits(n: u64) -> u32: сколько цифр в десятичной записи n (для 0 '
                   '— одна цифра).',
      'starter': 'fn count_digits(n: u64) -> u32 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", count_digits(0));\n'
                '    println!("{}", count_digits(9));\n'
                '    println!("{}", count_digits(10));\n'
                '    println!("{}", count_digits(123456789));\n'
                '    println!("{}", count_digits(18_446_744_073_709_551_615));\n'
                '}\n',
      'hint': 'Если число меньше 10 — одна цифра; иначе 1 + количество цифр у n / 10.',
      'expected': ['1', '1', '2', '9', '20']},
     {'id': 'r4-hypot',
      'mode': 'rust',
      'title': 'Гипотенуза',
      'statement': 'Напишите функцию hypot(a: f64, b: f64) -> f64: длина гипотенузы √(a² + b²).',
      'starter': 'fn hypot(a: f64, b: f64) -> f64 {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", hypot(3.0, 4.0));\n'
                '    println!("{:.4}", hypot(1.0, 1.0));\n'
                '    println!("{}", hypot(5.0, 12.0));\n'
                '}\n',
      'hint': '(a * a + b * b).sqrt()',
      'expected': ['5', '1.4142', '13']},
     {'id': 'r4-fix-no-return-type',
      'mode': 'rust',
      'title': 'Исправьте: нет типа результата',
      'statement': 'Функция double должна возвращать удвоенное число, но в сигнатуре нет типа результата. '
                   'Исправьте сигнатуру — тело менять не нужно.',
      'starter': 'fn double(x: i32) {\n    x * 2\n}\n',
      'driver': 'fn main() {\n    println!("{}", double(21));\n    println!("{}", double(-4));\n}\n',
      'hint': 'Добавьте -> i32 после скобок параметров.',
      'expected': ['42', '-8']},
     {'id': 'r4-fix-semicolon',
      'mode': 'rust',
      'title': 'Исправьте: лишняя точка с запятой',
      'statement': 'Функция cube возвращает () вместо i32 из-за точки с запятой в конце. Исправьте.',
      'starter': 'fn cube(x: i32) -> i32 {\n    x * x * x;\n}\n',
      'driver': 'fn main() {\n    println!("{}", cube(3));\n    println!("{}", cube(-2));\n}\n',
      'hint': 'Уберите ; в последней строке.',
      'expected': ['27', '-8']},
     {'id': 'r4-fix-types',
      'mode': 'rust',
      'title': 'Исправьте: целое и дробное',
      'statement': 'Функция average должна вернуть среднее двух целых как f64, но (a + b) — целое, а делить '
                   'его нужно на дробное 2.0. Исправьте тело функции: average(3, 4) = 3.5.',
      'starter': 'fn average(a: i32, b: i32) -> f64 {\n    (a + b) / 2.0\n}\n',
      'driver': 'fn main() {\n    println!("{}", average(3, 4));\n    println!("{}", average(10, 20));\n}\n',
      'hint': 'Сумму надо привести к f64: (a + b) as f64 / 2.0',
      'expected': ['3.5', '15']},
     {'id': 'r4-compose',
      'mode': 'rust',
      'title': 'Функции вместе',
      'statement': 'В коде уже есть функция add. Напишите triple(x), которая возвращает 3·x, используя '
                   'только add (без операции *).',
      'starter': 'fn add(a: i32, b: i32) -> i32 {\n'
                 '    a + b\n'
                 '}\n'
                 '\n'
                 'fn triple(x: i32) -> i32 {\n'
                 '    todo!()\n'
                 '}\n',
      'driver': 'fn main() {\n'
                '    println!("{}", triple(5));\n'
                '    println!("{}", triple(-7));\n'
                '    println!("{}", triple(0));\n'
                '}\n',
      'hint': 'add(add(x, x), x) — вызов внутри вызова.',
      'expected': ['15', '-21', '0']},
     {'id': 'r4-fizz',
      'mode': 'rust',
      'title': 'FizzBuzz для одного числа',
      'statement': 'Напишите функцию fizz(n: u32) -> String: «FizzBuzz», если n делится на 15, «Fizz» — на '
                   '3, «Buzz» — на 5, иначе само число строкой. Одним выражением if – else if.',
      'starter': 'fn fizz(n: u32) -> String {\n    todo!()\n}\n',
      'driver': 'fn main() {\n'
                '    for n in [1, 3, 5, 15, 7, 30, 98] {\n'
                '        println!("{}", fizz(n));\n'
                '    }\n'
                '}\n',
      'hint': 'Сначала проверяйте деление на 15. Число в строку превращает n.to_string().',
      'expected': ['1', 'Fizz', 'Buzz', 'FizzBuzz', '7', 'FizzBuzz', '98']},
     {'id': 'r4-bmi-class',
      'mode': 'rust',
      'title': 'Категория ИМТ',
      'statement': "Напишите функцию category(bmi: f64) -> &'static str: «недостаток» при bmi < 18.5, "
                   '«норма» при bmi < 25.0, «избыток» при bmi < 30.0, иначе «ожирение».',
      'starter': "fn category(bmi: f64) -> &'static str {\n    todo!()\n}\n",
      'driver': 'fn main() {\n'
                '    for b in [17.0, 18.5, 22.9, 25.0, 29.9, 35.0] {\n'
                '        println!("{}", category(b));\n'
                '    }\n'
                '}\n',
      'hint': "Строковые литералы — &'static str: возвращать их из ветвей можно сразу.",
      'expected': ['недостаток', 'норма', 'норма', 'избыток', 'избыток', 'ожирение']}]}
